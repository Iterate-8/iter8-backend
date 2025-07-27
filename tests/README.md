# Tests

This directory contains test files for the FastAPI GraphQL backend.

## Test Files

### API Tests
- **`test_api_manual.py`** - Comprehensive manual test script that tests all major API endpoints
- **`test_graphql.py`** - Pytest-based tests for GraphQL operations (may have version compatibility issues)
- **`run_tests.py`** - A test runner script that orchestrates running all tests and provides a summary

### Database Connection Tests (Troubleshooting)
These files were created during database connection troubleshooting and can be used for debugging:

- **`test_db_connection.py`** - Basic database connection test
- **`test_production_db.py`** - Production database connection test with SSL
- **`test_supabase_connection.py`** - Supabase-specific connection tests
- **`test_updated_connection.py`** - Updated connection test with pooling
- **`test_exact_connection.py`** - Exact connection string test
- **`test_psycopg2_connection.py`** - Synchronous psycopg2 connection test
- **`quick_db_test.py`** - Quick database connection test with different SSL modes

## How to Run Tests

### Option 1: Use the Test Runner (Recommended)
```bash
# Make sure your backend is running first
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, run all tests
python tests/run_tests.py
```

### Option 2: Run Manual API Tests Only
```bash
# Make sure your backend is running first
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, run manual tests
python tests/test_api_manual.py
```

### Option 3: Run Individual Test Functions
```python
# Import specific test functions
from tests.test_api_manual import test_health_check, test_create_feedback

# Run individual tests
test_health_check()
feedback_id = test_create_feedback()
```

### Option 4: Run Pytest Tests (if compatible)
```bash
pytest tests/test_graphql.py -v
```

### Option 5: Database Connection Troubleshooting
If you're having database connection issues, you can run these diagnostic tests:

```bash
# Test basic connection
python tests/test_db_connection.py

# Test production database
python tests/test_production_db.py

# Test Supabase connection
python tests/test_supabase_connection.py

# Quick connection test
python tests/quick_db_test.py
```

## Test Coverage

### API Tests Cover:
- ✅ Health check endpoint (`/health`)
- ✅ Root endpoint (`/`)
- ✅ GraphQL introspection
- ✅ Create feedback mutation
- ✅ Get feedback list query
- ✅ Filter feedback by startup name
- ✅ Error handling and response validation

### Database Tests Cover:
- ✅ Basic database connectivity
- ✅ SSL connection handling
- ✅ Connection pooling
- ✅ Supabase-specific configurations
- ✅ Different driver compatibility (asyncpg, psycopg2)

## Prerequisites

Make sure you have the required dependencies:
```bash
pip install requests pytest pytest-asyncio httpx asyncpg psycopg2-binary
```

## Notes

- The manual API tests are more reliable than pytest tests due to version compatibility issues
- Always ensure your backend is running before executing API tests
- Database connection tests require proper `.env` configuration
- Tests will automatically check if the backend is running and provide helpful error messages
- The test runner provides a comprehensive summary of all test results
- Database connection tests are primarily for troubleshooting and debugging purposes 