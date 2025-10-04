"""
Serverless-optimized database connection for Vercel deployment.
Uses connection per request instead of connection pooling.
"""

import logging
import asyncpg
from typing import AsyncGenerator
from urllib.parse import urlparse, unquote
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
    if not settings.database_url:
        raise ValueError("DATABASE_URL is not set. Please configure it in Vercel Project Settings → Environment Variables.")

    # Parse connection URL robustly
    parsed = urlparse(settings.database_url)

    # Support schemes like postgresql+asyncpg
    scheme = (parsed.scheme or "postgresql").split("+")[0]
    if scheme not in {"postgres", "postgresql"}:
        logger.warning(f"Unexpected database scheme '{parsed.scheme}', proceeding as PostgreSQL")

    user = parsed.username or "postgres"
    password = unquote(parsed.password) if parsed.password else ""
    host = parsed.hostname
    port = parsed.port
    database = (parsed.path or "/postgres").lstrip("/")

    if not host:
        raise ValueError("DATABASE_URL is missing hostname")

    # Default ports: pooler usually 6543, direct 5432
    if port is None:
        if host.endswith("pooler.supabase.com"):
            port = 6543
        else:
            port = 5432
    
    # Create direct connection (no pooling for serverless)
    connection = None
    try:
        # Connect with explicit parameters. Enforce SSL for Supabase.
        connection = await asyncpg.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            timeout=30,
            command_timeout=30,
            ssl=True
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
