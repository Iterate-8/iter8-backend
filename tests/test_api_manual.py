#!/usr/bin/env python3
"""
Manual API testing script for the FastAPI GraphQL backend.
Run this script to test your API endpoints manually.
"""

import requests
import json
import uuid
from datetime import datetime, timezone

# Configuration
BASE_URL = "http://0.0.0.0:8000"
GRAPHQL_URL = f"{BASE_URL}/graphql"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data}")
            return True
        else:
            print(f"❌ Health Check Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("\n🔍 Testing Root Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root Endpoint: {data}")
            return True
        else:
            print(f"❌ Root Endpoint Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Root Endpoint Error: {e}")
        return False

def test_graphql_introspection():
    """Test GraphQL introspection."""
    print("\n🔍 Testing GraphQL Introspection...")
    query = """
    query IntrospectionQuery {
        __schema {
            types {
                name
                kind
            }
        }
    }
    """
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "__schema" in data["data"]:
                types = [t["name"] for t in data["data"]["__schema"]["types"]]
                print(f"✅ GraphQL Types Found: {len(types)} types")
                print(f"   Key Types: {[t for t in types if t in ['Query', 'Mutation', 'FeedbackType', 'SessionType']]}")
                return True
            else:
                print(f"❌ GraphQL Introspection Failed: {data}")
                return False
        else:
            print(f"❌ GraphQL Introspection Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ GraphQL Introspection Error: {e}")
        return False

def test_create_feedback():
    """Test creating a feedback entry."""
    print("\n🔍 Testing Create Feedback...")
    query = """
    mutation CreateFeedback($input: CreateFeedbackInput!) {
        createFeedback(input: $input) {
            success
            message
            feedback {
                id
                userId
                feedbackType
                feedback
                startupName
                createdAt
            }
        }
    }
    """
    
    test_user_id = str(uuid.uuid4())
    variables = {
        "input": {
            "userId": test_user_id,
            "feedbackType": "todo",
            "feedback": "Test feedback from manual script",
            "startupName": "Test Startup"
        }
    }
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "createFeedback" in data["data"]:
                result = data["data"]["createFeedback"]
                if result["success"]:
                    print(f"✅ Feedback Created: {result['message']}")
                    print(f"   Feedback ID: {result['feedback']['id']}")
                    return result['feedback']['id']
                else:
                    print(f"❌ Feedback Creation Failed: {result['message']}")
                    return None
            else:
                print(f"❌ GraphQL Response Error: {data}")
                return None
        else:
            print(f"❌ Create Feedback Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Create Feedback Error: {e}")
        return None

def test_get_feedback_list():
    """Test getting feedback list."""
    print("\n🔍 Testing Get Feedback List...")
    query = """
    query GetFeedbackList($limit: Int, $offset: Int) {
        getFeedbackList(limit: $limit, offset: $offset) {
            success
            message
            feedbackList {
                id
                userId
                feedbackType
                feedback
                startupName
                createdAt
            }
            totalCount
        }
    }
    """
    
    variables = {
        "limit": 10,
        "offset": 0
    }
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "getFeedbackList" in data["data"]:
                result = data["data"]["getFeedbackList"]
                if result["success"]:
                    print(f"✅ Feedback List Retrieved: {result['message']}")
                    print(f"   Total Count: {result['totalCount']}")
                    print(f"   Feedback Items: {len(result['feedbackList'])}")
                    return True
                else:
                    print(f"❌ Get Feedback List Failed: {result['message']}")
                    return False
            else:
                print(f"❌ GraphQL Response Error: {data}")
                return False
        else:
            print(f"❌ Get Feedback List Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get Feedback List Error: {e}")
        return False

def test_get_feedback_by_startup_name():
    """Test getting feedback by startup name."""
    print("\n🔍 Testing Get Feedback by Startup Name...")
    query = """
    query GetFeedbackByStartupName($startupName: String) {
        getFeedbackList(startupName: $startupName, limit: 10, offset: 0) {
            success
            message
            feedbackList {
                id
                userId
                feedbackType
                feedback
                startupName
                createdAt
            }
            totalCount
        }
    }
    """
    
    variables = {
        "startupName": "Test Startup"
    }
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "getFeedbackList" in data["data"]:
                result = data["data"]["getFeedbackList"]
                if result["success"]:
                    print(f"✅ Feedback by Startup Name Retrieved: {result['message']}")
                    print(f"   Total Count: {result['totalCount']}")
                    print(f"   Feedback Items: {len(result['feedbackList'])}")
                    return True
                else:
                    print(f"❌ Get Feedback by Startup Name Failed: {result['message']}")
                    return False
            else:
                print(f"❌ GraphQL Response Error: {data}")
                return False
        else:
            print(f"❌ Get Feedback by Startup Name Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get Feedback by Startup Name Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Manual API Tests...")
    print("=" * 50)
    
    # Test basic endpoints
    health_ok = test_health_check()
    root_ok = test_root_endpoint()
    
    # Test GraphQL
    introspection_ok = test_graphql_introspection()
    
    # Test feedback operations
    feedback_id = test_create_feedback()
    list_ok = test_get_feedback_list()
    startup_name_ok = test_get_feedback_by_startup_name()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Root Endpoint: {'✅ PASS' if root_ok else '❌ FAIL'}")
    print(f"   GraphQL Introspection: {'✅ PASS' if introspection_ok else '❌ FAIL'}")
    print(f"   Create Feedback: {'✅ PASS' if feedback_id else '❌ FAIL'}")
    print(f"   Get Feedback List: {'✅ PASS' if list_ok else '❌ FAIL'}")
    print(f"   Get by Startup Name: {'✅ PASS' if startup_name_ok else '❌ FAIL'}")
    
    if all([health_ok, root_ok, introspection_ok, feedback_id, list_ok, startup_name_ok]):
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main() 