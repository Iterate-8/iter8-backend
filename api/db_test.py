"""
Test database connection endpoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import asyncpg

app = FastAPI()

@app.get("/")
async def test_db():
    try:
        # Try to connect to database
        db_url = os.environ.get("DATABASE_URL", "not set")
        
        if db_url == "not set":
            return {"error": "DATABASE_URL not set in environment variables"}
        
        # Parse URL
        from urllib.parse import urlparse, unquote
        parsed = urlparse(db_url)
        
        conn = await asyncpg.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            password=unquote(parsed.password) if parsed.password else "",
            database=parsed.path.lstrip("/"),
            ssl='require',
            timeout=10
        )
        
        # Test query
        result = await conn.fetchval("SELECT 1")
        await conn.close()
        
        return {
            "status": "success",
            "message": "Database connection successful!",
            "result": result,
            "host": parsed.hostname
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "db_url_set": "DATABASE_URL" in os.environ
        }

