"""
GraphQL API tests for the FastAPI backend.
"""

import pytest
import uuid
from datetime import datetime, timezone
from app.main import app


def test_health_check():
    """Test the health check endpoint."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "message" in data
    assert "environment" in data


def test_root_endpoint():
    """Test the root endpoint."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Iter8 Backend - GraphQL API"
    assert data["version"] == "1.0.0"
    assert "graphql" in data


def test_create_feedback_mutation():
    """Test creating a feedback entry."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
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
            "feedback": "Test feedback for GraphQL",
            "startupName": "Test Startup"
        }
    }
    
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "createFeedback" in data["data"]
    
    result = data["data"]["createFeedback"]
    assert result["success"] == True
    assert "Feedback created successfully" in result["message"]
    assert result["feedback"]["feedbackType"] == "todo"
    assert result["feedback"]["feedback"] == "Test feedback for GraphQL"
    assert result["feedback"]["startupName"] == "Test Startup"


def test_get_feedback_list_query():
    """Test getting feedback list."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    query = """
    query GetFeedbackList($userId: UUID, $feedbackType: String, $limit: Int, $offset: Int) {
        getFeedbackList(userId: $userId, feedbackType: $feedbackType, limit: $limit, offset: $offset) {
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
    
    test_user_id = str(uuid.uuid4())
    variables = {
        "userId": test_user_id,
        "feedbackType": "todo",
        "limit": 10,
        "offset": 0
    }
    
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "getFeedbackList" in data["data"]
    
    result = data["data"]["getFeedbackList"]
    assert result["success"] == True
    assert isinstance(result["feedbackList"], list)
    assert isinstance(result["totalCount"], int)


def test_create_session_mutation():
    """Test creating a session."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    query = """
    mutation CreateSession($input: CreateSessionInput!) {
        createSession(input: $input) {
            success
            message
            session {
                id
                userId
                sessionId
                url
                startTime
                isActive
                createdAt
            }
        }
    }
    """
    
    test_user_id = str(uuid.uuid4())
    test_session_id = f"session_{uuid.uuid4()}"
    start_time = datetime.now(timezone.utc)
    
    variables = {
        "input": {
            "userId": test_user_id,
            "sessionId": test_session_id,
            "url": "http://example.com",
            "startTime": start_time.isoformat(),
            "isActive": True
        }
    }
    
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "createSession" in data["data"]
    
    result = data["data"]["createSession"]
    assert result["success"] == True
    assert "Session created successfully" in result["message"]
    assert result["session"]["sessionId"] == test_session_id
    assert result["session"]["isActive"] == True


def test_create_user_interaction_mutation():
    """Test creating a user interaction."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    query = """
    mutation CreateUserInteraction($input: CreateUserInteractionInput!) {
        createUserInteraction(input: $input) {
            success
            message
            interaction {
                id
                sessionId
                userId
                interactionType
                timestamp
                url
                elementInfo
                data
                createdAt
            }
        }
    }
    """
    
    test_user_id = str(uuid.uuid4())
    test_session_id = f"session_{uuid.uuid4()}"
    timestamp = datetime.now(timezone.utc)
    
    variables = {
        "input": {
            "sessionId": test_session_id,
            "userId": test_user_id,
            "interactionType": "click",
            "timestamp": timestamp.isoformat(),
            "url": "http://example.com",
            "elementInfo": {"tag": "button", "id": "submit-btn"},
            "data": {"x": 100, "y": 200}
        }
    }
    
    response = client.post("/graphql", json={"query": query, "variables": variables})
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "createUserInteraction" in data["data"]
    
    result = data["data"]["createUserInteraction"]
    assert result["success"] == True
    assert "User interaction created successfully" in result["message"]
    assert result["interaction"]["interactionType"] == "click"
    assert result["interaction"]["sessionId"] == test_session_id


def test_graphql_introspection():
    """Test GraphQL introspection query."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
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
    
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "__schema" in data["data"]
    
    # Check that we have our custom types
    types = [t["name"] for t in data["data"]["__schema"]["types"]]
    assert "FeedbackType" in types
    assert "SessionType" in types
    assert "UserInteractionType" in types
    assert "Query" in types
    assert "Mutation" in types 