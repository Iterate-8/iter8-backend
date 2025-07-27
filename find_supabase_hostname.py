#!/usr/bin/env python3
"""
Script to help find the correct Supabase hostname
"""

import asyncio
import asyncpg
from urllib.parse import urlparse, unquote

def test_hostname_variations():
    """Test different possible hostname patterns"""
    
    # Your current details
    current_host = "db.eousczgdnqjsnjnkcswq.supabase.co"
    project_ref = "eousczgdnqjsnjnkcswq"
    
    # Possible hostname variations
    variations = [
        f"db.{project_ref}.supabase.co",
        f"{project_ref}.supabase.co",
        f"db.{project_ref}.supabase.com",
        f"{project_ref}.supabase.com",
        f"db.{project_ref}.supabase.net",
        f"{project_ref}.supabase.net",
    ]
    
    print("🔍 Testing different hostname variations...")
    print(f"Project reference: {project_ref}")
    print()
    
    for hostname in variations:
        print(f"Testing: {hostname}")
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '1', hostname], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                print(f"✅ {hostname} - REACHABLE!")
                return hostname
            else:
                print(f"❌ {hostname} - Not reachable")
        except Exception as e:
            print(f"❌ {hostname} - Error: {e}")
        print()
    
    return None

async def test_connection_with_hostname(hostname):
    """Test connection with a specific hostname"""
    try:
        print(f"🔒 Testing connection to {hostname}...")
        
        conn = await asyncpg.connect(
            host=hostname,
            port=5432,
            user="postgres",
            password="iter8password&$123",
            database="postgres",
            ssl='require'
        )
        
        print("✅ Connection successful!")
        
        result = await conn.fetchval("SELECT version()")
        print(f"📊 PostgreSQL: {result}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

async def main():
    """Main function"""
    print("="*60)
    print("🔍 SUPABASE HOSTNAME FINDER")
    print("="*60)
    print()
    
    # Test hostname variations
    working_hostname = test_hostname_variations()
    
    if working_hostname:
        print(f"🎯 Found working hostname: {working_hostname}")
        print()
        
        # Test connection
        success = await test_connection_with_hostname(working_hostname)
        
        if success:
            print()
            print("🎉 SUCCESS! Use this connection string:")
            print(f"postgresql://postgres:iter8password&$123@{working_hostname}:5432/postgres")
        else:
            print("❌ Hostname is reachable but connection failed")
    else:
        print("❌ No working hostname found")
        print()
        print("🔧 Please check your Supabase dashboard for the correct connection string")

if __name__ == "__main__":
    asyncio.run(main()) 