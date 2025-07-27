#!/usr/bin/env python3
"""
Test script for production Supabase database connection
"""

import asyncio
import asyncpg
from urllib.parse import urlparse, unquote
from app.config import settings

async def test_production_connection():
    """Test the production database connection"""
    try:
        print("🔍 Testing production database connection...")
        print(f"Database URL: {settings.database_url}")
        
        # Parse the URL properly
        parsed = urlparse(settings.database_url)
        
        user = parsed.username
        password = unquote(parsed.password) if parsed.password else ""
        host = parsed.hostname
        port = parsed.port or 5432
        database = parsed.path.lstrip("/")
        
        print(f"📍 Host: {host}")
        print(f"🔢 Port: {port}")
        print(f"🗄️  Database: {database}")
        print(f"👤 User: {user}")
        print(f"🔑 Password: {'*' * len(password)} (hidden)")
        
        # Test connection with SSL
        print("\n🔒 Attempting connection with SSL...")
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl='require'  # Force SSL for production
        )
        
        print("✅ Production database connection successful!")
        
        # Test a simple query
        result = await conn.fetchval("SELECT version()")
        print(f"📊 PostgreSQL version: {result}")
        
        # Test if our tables exist
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        if tables:
            print(f"📋 Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table['table_name']}")
        else:
            print("📋 No tables found in public schema")
        
        await conn.close()
        
    except asyncpg.InvalidPasswordError:
        print("❌ Invalid password - check your database password")
    except asyncpg.InvalidAuthorizationSpecificationError:
        print("❌ Authorization failed - check your username/password")
    except asyncpg.ConnectionDoesNotExistError:
        print("❌ Connection failed - check if your IP is whitelisted")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Production troubleshooting:")
        print("1. Check if your IP is in Supabase allowlist")
        print("2. Verify SSL is enabled in Supabase settings")
        print("3. Check if the project is active (not paused)")
        print("4. Verify connection pooling settings")

if __name__ == "__main__":
    asyncio.run(test_production_connection()) 