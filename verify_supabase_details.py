#!/usr/bin/env python3
"""
Helper script to verify Supabase connection details
"""

import re
from urllib.parse import urlparse

def verify_connection_string(connection_string):
    """Verify if a connection string looks valid"""
    print("🔍 Verifying connection string format...")
    
    try:
        # Parse the URL
        parsed = urlparse(connection_string)
        
        print(f"✅ URL format is valid")
        print(f"📍 Host: {parsed.hostname}")
        print(f"🔢 Port: {parsed.port}")
        print(f"🗄️  Database: {parsed.path.lstrip('/')}")
        print(f"👤 User: {parsed.username}")
        print(f"🔑 Password: {'*' * len(parsed.password) if parsed.password else 'None'}")
        
        # Check if it's a Supabase URL
        if parsed.hostname and 'supabase.co' in parsed.hostname:
            print("✅ Hostname contains 'supabase.co'")
            
            # Extract project reference
            project_ref = parsed.hostname.replace('db.', '').replace('.supabase.co', '')
            print(f"📋 Project reference: {project_ref}")
            
            # Check if project reference looks valid (should be alphanumeric)
            if re.match(r'^[a-zA-Z0-9]+$', project_ref):
                print("✅ Project reference format looks valid")
            else:
                print("⚠️  Project reference contains special characters")
                
        else:
            print("❌ Hostname doesn't look like a Supabase URL")
            
    except Exception as e:
        print(f"❌ Error parsing connection string: {e}")

def show_instructions():
    """Show instructions for finding Supabase details"""
    print("\n" + "="*60)
    print("📋 WHERE TO FIND SUPABASE CONNECTION DETAILS")
    print("="*60)
    print()
    print("1. 🏠 Go to: https://supabase.com/dashboard")
    print("2. 🔧 Click 'Settings' (gear icon) in left sidebar")
    print("3. 🗄️  Click 'Database' in settings menu")
    print("4. 📋 Scroll down to 'Connection string' section")
    print("5. 📋 Copy the 'URI' connection string")
    print()
    print("📝 The connection string should look like:")
    print("   postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres")
    print()
    print("🔍 Also check 'Settings' → 'General' for your Project Reference ID")
    print("="*60)

if __name__ == "__main__":
    show_instructions()
    
    # Test current connection string
    print("\n🔍 Testing your current connection string:")
    current_url = "postgresql://postgres:iter8password&$123@db.eousczgdnqjsnjnkcswq.supabase.co:5432/postgres"
    verify_connection_string(current_url)
    
    print("\n💡 If the project reference looks wrong, get the correct one from Supabase dashboard!") 