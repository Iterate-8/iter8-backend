"""
Vercel serverless entry point for the FastAPI application.
"""

import sys
from pathlib import Path

# Add parent directory to Python path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the Vercel-optimized FastAPI app
from app.vercel_main import handler

# Export for Vercel
app = handler
