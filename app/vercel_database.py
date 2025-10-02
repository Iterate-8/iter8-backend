"""
Serverless-optimized database connection for Vercel deployment.
Uses connection per request instead of connection pooling.
"""

import logging
import asyncpg
from typing import AsyncGenerator
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Get a database connection for serverless environment.
    Creates a new connection per request (suitable for Vercel).
    
    Yields:
        asyncpg.Connection: Database connection
    """
    # Parse connection URL manually to avoid asyncpg's regex issues with pooler format
    import re
    
    # Match postgresql://user:pass@host:port/database
    pattern = r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
    match = re.match(pattern, settings.database_url)
    
    if not match:
        raise ValueError(f"Invalid DATABASE_URL format")
    
    user, password, host, port, database = match.groups()
    
    # Create direct connection (no pooling for serverless)
    connection = None
    try:
        # Connect with individual parameters to avoid asyncpg URL parsing issues
        # Note: SSL is handled automatically by asyncpg for pooler connections
        connection = await asyncpg.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            timeout=30,
            command_timeout=30
        )
        logger.debug(f"Database connection established to {host}:{port}")
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        logger.error(f"Attempted connection to {host}:{port} as {user}")
        raise
    finally:
        if connection:
            await connection.close()
            logger.debug("Database connection closed")


async def init_db() -> None:
    """
    Initialize database tables for serverless environment.
    This runs on each cold start but is idempotent.
    """
    try:
        async for conn in get_db():
            # Create tables if they don't exist
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL,
                    session_id TEXT NOT NULL,
                    url TEXT,
                    start_time TIMESTAMPTZ DEFAULT NOW(),
                    end_time TIMESTAMPTZ,
                    duration INTEGER,
                    interaction_count INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL,
                    feedback_type VARCHAR(50),
                    feedback TEXT NOT NULL,
                    startup_name VARCHAR(255),
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    session_id TEXT NOT NULL,
                    user_id UUID NOT NULL,
                    interaction_type TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    url TEXT,
                    element_info JSONB,
                    data JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
            
            logger.info("Database tables ensured for serverless deployment")
            break
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.warning("Continuing without database initialization")


# For serverless, we don't need a close_db function since connections are per-request
