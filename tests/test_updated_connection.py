#!/usr/bin/env python3
"""
Test connection with updated password using connection pooling
"""

import asyncio
import asyncpg

async def test_connection_pooling():
    """Test connection using Supabase connection pooling"""
    
    # Connection pooling details
    host = "aws-0-us-east-1.pooler.supabase.com"
    port = 6543
    user = "postgres.eousczgdnqjsnjnkcswq"
    password = "iter8passwordstrong$$$$"
    database = "postgres"
    
    print("🔍 Testing connection pooling with updated password...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Database: {database}")
    
    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                ssl='require',
                command_timeout=10
            ),
            timeout=12
        )
        
        print("✅ Connection successful!")
        
        # Test a query
        result = await conn.fetchval("SELECT version()")
        print(f"📊 PostgreSQL: {result}")
        
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
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

async def main():
    """Main function"""
    print("="*60)
    print("🔍 TESTING UPDATED CONNECTION")
    print("="*60)
    print()
    
    success = await test_connection_pooling()
    
    if success:
        print("\n🎉 SUCCESS! Update your .env file with:")
        print("DATABASE_URL=postgresql://postgres.eousczgdnqjsnjnkcswq:iter8passwordstrong$$$$@aws-0-us-east-1.pooler.supabase.com:6543/postgres")
    else:
        print("\n❌ Connection pooling failed")
        print("Please check your Supabase dashboard for the correct connection pooling URL")

if __name__ == "__main__":
    asyncio.run(main()) 