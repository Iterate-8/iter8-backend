#!/usr/bin/env python3
"""
Test script using psycopg2 (synchronous) connection
"""

import psycopg2
from urllib.parse import urlparse, unquote
from app.config import settings

def test_psycopg2_connection():
    """Test the database connection using psycopg2"""
    try:
        print("🔍 Testing database connection with psycopg2...")
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
        
        # Test connection with psycopg2
        print("\n🔒 Attempting connection with psycopg2...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            sslmode='require'  # Force SSL for production
        )
        
        print("✅ Database connection successful with psycopg2!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        result = cursor.fetchone()
        print(f"📊 PostgreSQL version: {result[0]}")
        
        # Test if our tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        if tables:
            print(f"📋 Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("📋 No tables found in public schema")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if your IP is in Supabase allowlist")
        print("2. Verify SSL is enabled in Supabase settings")
        print("3. Check if the project is active (not paused)")
        print("4. Verify connection pooling settings")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_psycopg2_connection() 