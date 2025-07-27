# FastAPI GraphQL Backend with Supabase Integration

A production-ready GraphQL API backend using FastAPI and Python that connects to a Supabase database. This backend serves both web app and CLI applications for todo/feedback management.

## 🚀 Features

- **GraphQL API** with Strawberry GraphQL
- **Supabase Integration** with PostgreSQL database
- **Async SQLAlchemy** for database operations
- **Complete CRUD Operations** for feedback, sessions, and user interactions
- **Comprehensive Error Handling** with proper GraphQL error responses
- **CORS Support** for web app integration
- **Production Ready** with proper logging and configuration
- **Type Safety** with Pydantic validation and type hints

## 🛠 Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **Strawberry GraphQL** - GraphQL library for Python
- **SQLAlchemy** - SQL toolkit and ORM
- **Supabase** - PostgreSQL database with real-time features
- **Pydantic** - Data validation using Python type annotations
- **Asyncpg** - Async PostgreSQL driver
- **Python-dotenv** - Environment variable management

## 📋 Prerequisites

- Python 3.8+
- Supabase account and project
- PostgreSQL database (provided by Supabase)

## 🏗 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database connection and session management
│   ├── config.py               # Configuration settings
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── sessions.py
│   │   ├── feedback.py
│   │   └── user_interactions.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── sessions.py
│   │   ├── feedback.py
│   │   └── user_interactions.py
│   ├── graphql/                # GraphQL schema and resolvers
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   ├── queries.py
│   │   ├── mutations.py
│   │   └── types.py
│   └── services/               # Business logic layer
│       ├── __init__.py
│       ├── feedback_service.py
│       ├── session_service.py
│       └── user_interaction_service.py
├── requirements.txt
├── env.example
└── README.md
```

## 🗄 Database Schema

### Tables

1. **sessions** - User session tracking
   - `id` (uuid, primary key)
   - `user_id` (uuid, references auth.users.id)
   - `session_id` (text)
   - `url` (text)
   - `start_time` (timestamptz)
   - `end_time` (timestamptz)
   - `duration` (int4)
   - `interaction_count` (int4)
   - `is_active` (bool)
   - `created_at` (timestamptz)
   - `updated_at` (timestamptz)

2. **feedback** - Todo/feedback management
   - `id` (uuid, primary key)
   - `user_id` (uuid, references auth.users.id)
   - `feedback_type` (varchar)
   - `feedback` (text)
   - `startup_name` (varchar)
   - `created_at` (timestamptz)
   - `updated_at` (timestamptz)

3. **user_interactions** - User interaction tracking
   - `id` (uuid, primary key)
   - `session_id` (text)
   - `user_id` (uuid, references auth.users.id)
   - `interaction_type` (text)
   - `timestamp` (timestamptz)
   - `url` (text)
   - `element_info` (jsonb)
   - `data` (jsonb)
   - `created_at` (timestamptz)

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd iter8-backend
```

### 2. Setup with Conda (Recommended)

```bash
# Run the setup script
./setup_conda.sh

# This will:
# - Create a conda environment named 'iter8-backend'
# - Install all dependencies
# - Create a .env file from template
```

### Alternative: Manual Conda Setup

```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate iter8-backend

# Create .env file from template
cp env_template.txt .env
```

### 3. Environment Configuration

Edit the `.env` file with your actual values:

Edit `.env` with your Supabase credentials:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Application Configuration
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the Application

```bash
# Using the conda startup script (recommended)
./start_conda.sh

# Or manually
conda activate iter8-backend
python -m app.main

# Or using uvicorn directly
conda activate iter8-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 API Endpoints

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: Your deployed URL

### Available Endpoints

- **GET** `/` - API information
- **GET** `/health` - Health check
- **POST** `/graphql` - GraphQL endpoint
- **GET** `/graphql` - GraphiQL playground (development only)
- **GET** `/docs` - FastAPI documentation (development only)

## 🔍 GraphQL API

### Queries

#### Feedback Queries
```graphql
# Get feedback by ID
query GetFeedbackById($feedbackId: UUID!) {
  getFeedbackById(feedbackId: $feedbackId) {
    id
    userId
    feedbackType
    feedback
    startupName
    createdAt
    updatedAt
  }
}

# Get feedback list with filtering
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
```

#### Session Queries
```graphql
# Get session by ID
query GetSessionById($sessionId: UUID!) {
  getSessionById(sessionId: $sessionId) {
    id
    userId
    sessionId
    url
    startTime
    endTime
    duration
    interactionCount
    isActive
    createdAt
  }
}

# Get sessions list
query GetSessionsList($userId: UUID, $isActive: Boolean, $limit: Int, $offset: Int) {
  getSessionsList(userId: $userId, isActive: $isActive, limit: $limit, offset: $offset) {
    success
    message
    sessionsList {
      id
      userId
      sessionId
      url
      startTime
      endTime
      duration
      interactionCount
      isActive
    }
    totalCount
  }
}
```

#### User Interaction Queries
```graphql
# Get user interactions by session
query GetUserInteractionsBySession($sessionId: String!, $userId: UUID, $limit: Int, $offset: Int) {
  getUserInteractionsBySession(sessionId: $sessionId, userId: $userId, limit: $limit, offset: $offset) {
    success
    message
    interactionsList {
      id
      sessionId
      userId
      interactionType
      timestamp
      url
      elementInfo
      data
    }
    totalCount
  }
}

# Get interaction summary
query GetInteractionSummary($userId: UUID, $sessionId: String) {
  getInteractionSummary(userId: $userId, sessionId: $sessionId) {
    success
    message
    summary {
      interactionType
      count
    }
  }
}
```

### Mutations

#### Feedback Mutations
```graphql
# Create feedback
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

# Update feedback
mutation UpdateFeedback($feedbackId: UUID!, $input: UpdateFeedbackInput!) {
  updateFeedback(feedbackId: $feedbackId, input: $input) {
    success
    message
    feedback {
      id
      feedbackType
      feedback
      startupName
      updatedAt
    }
  }
}

# Delete feedback
mutation DeleteFeedback($feedbackId: UUID!) {
  deleteFeedback(feedbackId: $feedbackId) {
    success
    message
  }
}
```

#### Session Mutations
```graphql
# Create session
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
    }
  }
}

# End session
mutation EndSession($sessionId: UUID!) {
  endSession(sessionId: $sessionId) {
    success
    message
    session {
      id
      endTime
      duration
      isActive
    }
  }
}

# Update session
mutation UpdateSession($sessionId: UUID!, $input: UpdateSessionInput!) {
  updateSession(sessionId: $sessionId, input: $input) {
    success
    message
    session {
      id
      url
      interactionCount
      isActive
      updatedAt
    }
  }
}
```

#### User Interaction Mutations
```graphql
# Create user interaction
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
    }
  }
}
```

## 🧪 Testing

### Basic Test Structure

Create a `tests/` directory and add test files:

```python
# tests/test_graphql.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_create_feedback():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        query = """
        mutation CreateFeedback($input: CreateFeedbackInput!) {
            createFeedback(input: $input) {
                success
                message
                feedback {
                    id
                    feedbackType
                    feedback
                }
            }
        }
        """
        
        variables = {
            "input": {
                "userId": "123e4567-e89b-12d3-a456-426614174000",
                "feedbackType": "todo",
                "feedback": "Test feedback",
                "startupName": "Test Startup"
            }
        }
        
        response = await ac.post("/graphql", json={"query": query, "variables": variables})
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["createFeedback"]["success"] == True
```

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

## 🚀 Deployment

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t iter8-backend .
docker run -p 8000:8000 --env-file .env iter8-backend
```

### Production Considerations

1. **Environment Variables**: Set `DEBUG=False` and `ENVIRONMENT=production`
2. **Database**: Use production Supabase instance
3. **Security**: Use strong `SECRET_KEY` and proper CORS origins
4. **Logging**: Configure proper log levels and output
5. **Monitoring**: Add health checks and monitoring endpoints

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SUPABASE_URL` | Supabase project URL | Required |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | Required |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | Required |
| `DEBUG` | Enable debug mode | `False` |
| `ENVIRONMENT` | Environment name | `development` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `SECRET_KEY` | JWT secret key | Required |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |

## 📚 Usage Examples

### Web App Integration

```javascript
// Create a new todo
const createTodo = async (todoData) => {
  const query = `
    mutation CreateFeedback($input: CreateFeedbackInput!) {
      createFeedback(input: $input) {
        success
        message
        feedback {
          id
          feedbackType
          feedback
          startupName
        }
      }
    }
  `;
  
  const response = await fetch('/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      variables: {
        input: {
          userId: todoData.userId,
          feedbackType: 'todo',
          feedback: todoData.content,
          startupName: todoData.startupName
        }
      }
    })
  });
  
  return response.json();
};
```

### CLI App Integration

```python
import requests
import json

def get_user_todos(user_id):
    query = """
    query GetFeedbackList($userId: UUID!, $feedbackType: String!) {
        getFeedbackList(userId: $userId, feedbackType: $feedbackType) {
            success
            feedbackList {
                id
                feedback
                startupName
                createdAt
            }
        }
    }
    """
    
    response = requests.post(
        'http://localhost:8000/graphql',
        json={
            'query': query,
            'variables': {
                'userId': user_id,
                'feedbackType': 'todo'
            }
        }
    )
    
    return response.json()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the documentation
2. Open an issue on GitHub
3. Contact the development team

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Complete GraphQL API implementation
- Supabase integration
- CRUD operations for all models
- Comprehensive error handling
- Production-ready configuration 