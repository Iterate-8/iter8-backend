"""
Vercel serverless entry point for the FastAPI application.
"""

# Import the Vercel-optimized FastAPI app
from app.vercel_main import handler

# This handler will be called by Vercel for each request
# The handler is already configured in vercel_main.py with Mangum
