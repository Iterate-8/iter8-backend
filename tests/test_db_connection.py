#!/usr/bin/env python3
"""
Simple script to test database connection
"""

import asyncio
import asyncpg
from urllib.parse import urlparse, unquote
from app.config import settings

async def test_connection():
    """Test the database connection"""
    try:
        print("Testing database connection...")
        print(f"Database URL: {settings.database_url}")
        
        # Parse the URL properly
        parsed = urlparse(settings.database_url)
        
        user = parsed.username
        password = unquote(parsed.password) if parsed.password else ""
        host = parsed.hostname
        port = parsed.port or 5432
        database = parsed.path.lstrip("/")
        
        print(f"Connecting to: {host}:{port}")
        print(f"Database: {database}")
        print(f"User: {user}")
        print(f"Password: {'*' * len(password)} (hidden)")
        
        # Test connection
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        print("✅ Database connection successful!")
        
        # Test a simple query
        result = await conn.fetchval("SELECT version()")
        print(f"PostgreSQL version: {result}")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPossible issues:")
        print("1. Check if your DATABASE_URL is correct in .env file")
        print("2. Verify your Supabase project is active")
        print("3. Check if your database password is correct")
        print("4. Ensure your IP is allowed in Supabase settings")

if __name__ == "__main__":
    asyncio.run(test_connection()) 