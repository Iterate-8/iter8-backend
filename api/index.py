"""
Thin Vercel serverless entry that delegates to the main FastAPI app.
Includes a safe fallback to expose startup import errors for debugging.
"""

from fastapi import FastAPI

try:
    from app.main import app as _app
    app = _app
except Exception as e:  # pragma: no cover - only for serverless cold start diagnostics
    app = FastAPI()

    @app.get("/__startup_error")
    async def startup_error():
        return {
            "error": "Failed to import app.main",
            "message": str(e)
        }
