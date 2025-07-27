#!/usr/bin/env python3
"""
Quick database connection test with timeout
"""

import asyncio
import asyncpg
from urllib.parse import urlparse, unquote

async def test_connection_with_timeout():
    """Test connection with timeout"""
    
    # Your corrected connection details
    host = "eousczgdnqjsnjnkcswq.supabase.co"
    port = 5432
    user = "postgres"
    password = "iter8password&$123"
    database = "postgres"
    
    print("🔍 Quick connection test with timeout...")
    print(f"Host: {host}")
    print(f"Port: {port}")
    
    # Test different configurations
    configs = [
        {"ssl": "require", "timeout": 5},
        {"ssl": "prefer", "timeout": 5},
        {"ssl": None, "timeout": 5},
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n🔧 Test {i}: SSL={config['ssl']}")
        
        try:
            # Use asyncio.wait_for for timeout
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database,
                    ssl=config['ssl'],
                    command_timeout=config['timeout']
                ),
                timeout=config['timeout'] + 2
            )
            
            print("✅ Connection successful!")
            await conn.close()
            return True
            
        except asyncio.TimeoutError:
            print("⏰ Connection timed out")
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    return False

async def test_different_ports():
    """Test different ports"""
    print("\n🔍 Testing different ports...")
    
    host = "eousczgdnqjsnjnkcswq.supabase.co"
    ports = [5432, 6543, 5433, 5434]
    
    for port in ports:
        print(f"Testing port {port}...")
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=host,
                    port=port,
                    user="postgres",
                    password="iter8password&$123",
                    database="postgres",
                    ssl="require",
                    command_timeout=3
                ),
                timeout=5
            )
            print(f"✅ Port {port} works!")
            await conn.close()
            return port
        except Exception as e:
            print(f"❌ Port {port} failed: {e}")
    
    return None

async def main():
    """Main function"""
    print("="*50)
    print("🔍 QUICK SUPABASE CONNECTION TEST")
    print("="*50)
    
    # Test with timeout
    success = await test_connection_with_timeout()
    
    if not success:
        # Test different ports
        working_port = await test_different_ports()
        
        if working_port:
            print(f"\n🎯 Found working port: {working_port}")
            print(f"Update your DATABASE_URL to use port {working_port}")
        else:
            print("\n❌ No working configuration found")
            print("Please check your Supabase dashboard for the correct connection details")

if __name__ == "__main__":
    asyncio.run(main()) 