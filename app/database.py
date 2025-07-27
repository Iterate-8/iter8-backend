"""
Async database connection and session management using asyncpg directly.
"""

import logging
import asyncpg
from typing import AsyncGenerator, Optional
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """Get or create the database connection pool."""
    global _pool
    if _pool is None:
        # Parse the connection URL
        from urllib.parse import urlparse, unquote
        
        parsed = urlparse(settings.database_url)
        user = parsed.username
        password = unquote(parsed.password) if parsed.password else ""
        host = parsed.hostname
        port = parsed.port or 5432
        database = parsed.path.lstrip("/")
        
        # Create connection pool
        _pool = await asyncpg.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl='require',
            min_size=1,
            max_size=10,
            command_timeout=60,
            statement_cache_size=0  # Disable statement cache for PgBouncer
        )
        logger.info("Database connection pool created successfully")
    
    return _pool


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Get a database connection from the pool.
    
    Yields:
        asyncpg.Connection: Database connection
    """
    pool = await get_pool()
    async with pool.acquire() as connection:
        try:
            yield connection
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise


async def init_db() -> None:
    """
    Initialize database tables.
    
    This function creates all tables defined in the models.
    """
    try:
        pool = await get_pool()
        async with pool.acquire() as conn:
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
            
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.warning("Continuing without database initialization")


async def close_db() -> None:
    """
    Close database connections.
    """
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connections closed successfully") 