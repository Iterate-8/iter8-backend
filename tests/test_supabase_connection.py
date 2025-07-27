#!/usr/bin/env python3
"""
Test different Supabase connection patterns
"""

import asyncio
import asyncpg
from urllib.parse import urlparse, unquote

async def test_connection_patterns():
    """Test different Supabase connection patterns"""
    
    project_ref = "eousczgdnqjsnjnkcswq"
    password = "iter8password&$123"
    
    # Different connection patterns to try
    patterns = [
        # Direct connection (what you have)
        {
            "name": "Direct DB",
            "host": f"db.{project_ref}.supabase.co",
            "port": 5432,
            "user": "postgres",
            "database": "postgres"
        },
        # Connection pooling (what you probably need)
        {
            "name": "Connection Pooling",
            "host": f"aws-0-us-east-1.pooler.supabase.com",
            "port": 6543,
            "user": f"postgres.{project_ref}",
            "database": "postgres"
        },
        # Alternative pooling
        {
            "name": "Pooling Alt",
            "host": f"db.{project_ref}.pooler.supabase.com",
            "port": 6543,
            "user": "postgres",
            "database": "postgres"
        }
    ]
    
    print("🔍 Testing different Supabase connection patterns...")
    print(f"Project reference: {project_ref}")
    print()
    
    for pattern in patterns:
        print(f"🔧 Testing: {pattern['name']}")
        print(f"   Host: {pattern['host']}")
        print(f"   Port: {pattern['port']}")
        print(f"   User: {pattern['user']}")
        
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=pattern['host'],
                    port=pattern['port'],
                    user=pattern['user'],
                    password=password,
                    database=pattern['database'],
                    ssl='require',
                    command_timeout=5
                ),
                timeout=7
            )
            
            print("✅ SUCCESS!")
            
            # Test a query
            result = await conn.fetchval("SELECT version()")
            print(f"   PostgreSQL: {result}")
            
            await conn.close()
            
            # Return the working pattern
            return pattern
            
        except asyncio.TimeoutError:
            print("⏰ Timeout")
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()
    
    return None

async def main():
    """Main function"""
    print("="*60)
    print("🔍 SUPABASE CONNECTION PATTERN TESTER")
    print("="*60)
    print()
    
    working_pattern = await test_connection_patterns()
    
    if working_pattern:
        print("\n🎉 SUCCESS! Use this connection string:")
        print(f"postgresql://{working_pattern['user']}:iter8password&$123@{working_pattern['host']}:{working_pattern['port']}/{working_pattern['database']}")
    else:
        print("\n❌ No working pattern found")
        print("\n🔧 Please check your Supabase dashboard for:")
        print("1. Connection pooling URL (not direct connection)")
        print("2. Make sure you're using the right connection type")
        print("3. Verify your project is active and not paused")

if __name__ == "__main__":
    asyncio.run(main()) 