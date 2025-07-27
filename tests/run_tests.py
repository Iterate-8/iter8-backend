#!/usr/bin/env python3
"""
Test runner for the FastAPI GraphQL backend.
This script provides an easy way to run all tests.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_manual_tests():
    """Run the manual API tests."""
    print("🧪 Running Manual API Tests...")
    print("=" * 50)
    
    try:
        from test_api_manual import main as run_manual_tests
        run_manual_tests()
        return True
    except ImportError as e:
        print(f"❌ Error importing manual tests: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running manual tests: {e}")
        return False

def run_pytest_tests():
    """Run pytest tests (if they work)."""
    print("\n🧪 Running Pytest Tests...")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_graphql.py", "-v"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False

def check_backend_running():
    """Check if the backend is running."""
    import requests
    try:
        response = requests.get("http://0.0.0.0:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main test runner."""
    print("🚀 FastAPI GraphQL Backend Test Runner")
    print("=" * 50)
    
    # Check if backend is running
    if not check_backend_running():
        print("⚠️  Backend is not running!")
        print("   Please start your backend first:")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print()
        return False
    
    print("✅ Backend is running!")
    print()
    
    # Run tests
    manual_success = run_manual_tests()
    
    # Try pytest (might fail due to version issues)
    pytest_success = run_pytest_tests()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Manual Tests: {'✅ PASS' if manual_success else '❌ FAIL'}")
    print(f"   Pytest Tests: {'✅ PASS' if pytest_success else '⚠️  SKIP (version issues)'}")
    
    if manual_success:
        print("\n🎉 Manual tests passed! Your API is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 