"""
Vercel serverless entrypoint.

This file imports the main FastAPI app and wraps it with Mangum, the adapter
that allows ASGI applications to run in a Lambda environment (which Vercel uses).

A fallback is included to catch and report any errors during the initial
import and instantiation of the main app, which is critical for debugging
cold start failures.
"""

import traceback
from fastapi import FastAPI
from mangum import Mangum

try:
    # Attempt to import the main application instance
    from app.main import app as fast_api_app
except Exception as e:
    # If the main app fails to import, create a fallback app.
    # This fallback will respond to all requests with a detailed error message,
    # making it possible to diagnose import-level or cold-start problems.
    fast_api_app = FastAPI()
    tb_str = traceback.format_exc()

    @fast_api_app.get("/{full_path:path}")
    async def startup_error_handler(full_path: str):
        return {
            "error": "FATAL: FastAPI application failed to import or initialize.",
            "source": "api/index.py",
            "exception_type": type(e).__name__,
            "message": str(e),
            "traceback": tb_str.splitlines(),
            "path_requested": f"/{full_path}",
        }

# Vercel's Python runtime requires a callable named `app` that is an ASGI application.
# We wrap our FastAPI instance in Mangum to create this compatible handler.
app = Mangum(fast_api_app)
