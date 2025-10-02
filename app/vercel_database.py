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
    # Parse the connection URL
    from urllib.parse import urlparse, unquote, parse_qs
    
    # Clean up the database URL - handle both postgres:// and postgresql://
    db_url = settings.database_url.replace('postgres://', 'postgresql://')
    
    parsed = urlparse(db_url)
    user = parsed.username
    password = unquote(parsed.password) if parsed.password else ""
    host = parsed.hostname
    port = parsed.port or 6543
    database = parsed.path.lstrip("/") or "postgres"
    
    # Parse query parameters (like pgbouncer=true)
    query_params = parse_qs(parsed.query)
    
    # Create direct connection (no pooling for serverless)
    connection = None
    try:
        # Connect using individual parameters for better compatibility
        connection = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl='require',
            timeout=30,
            command_timeout=30,
            server_settings={
                'application_name': 'vercel_serverless'
            }
        )
        logger.debug(f"Database connection established to {host}:{port}")
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        logger.error(f"Connection attempted to: {host}:{port} as user: {user}")
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
