#!/usr/bin/env python3
"""
Test the exact connection string format from Supabase
"""

import asyncio
import asyncpg
from urllib.parse import urlparse, unquote

# Your exact connection string from Supabase
DATABASE_URL = "postgresql://postgres:iter8password&$123@db.eousczgdnqjsnjnkcswq.supabase.co:5432/postgres"

async def test_exact_connection():
    """Test the exact connection string"""
    try:
        print("🔍 Testing exact Supabase connection string...")
        print(f"Original URL: {DATABASE_URL}")
        
        # Parse the URL
        parsed = urlparse(DATABASE_URL)
        
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
        
        # Test with asyncpg
        print("\n🔒 Testing with asyncpg...")
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl='require'
        )
        
        print("✅ Connection successful!")
        
        # Test query
        result = await conn.fetchval("SELECT version()")
        print(f"📊 PostgreSQL: {result}")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        
        # Try to ping the host
        print(f"\n🔍 Trying to ping {host}...")
        import subprocess
        try:
            result = subprocess.run(['ping', '-c', '1', host], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ Host is reachable")
            else:
                print("❌ Host is not reachable")
                print(f"Error: {result.stderr}")
        except Exception as ping_error:
            print(f"❌ Ping failed: {ping_error}")

if __name__ == "__main__":
    asyncio.run(test_exact_connection()) 