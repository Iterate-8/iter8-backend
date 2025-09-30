"""
Vercel-optimized FastAPI application.
This version is optimized for serverless deployment on Vercel.
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from mangum import Mangum

from app.config import settings
from app.vercel_database import get_db
from app.graphql.vercel_schema import schema

# Configure logging for Vercel
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application without lifespan events for serverless
app = FastAPI(
    title="Iter8 Backend - GraphQL API",
    description="FastAPI GraphQL Backend with Supabase Integration for Todo/Feedback Management",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    # No lifespan manager for serverless - connections are managed per request
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create GraphQL router
graphql_app = GraphQLRouter(
    schema,
    graphiql=settings.debug,  # Enable GraphiQL in development
    path="/"
)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Iter8 Backend - GraphQL API (Vercel)",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else "Not available in production",
        "graphql": "/graphql",
        "health": "/health",
        "platform": "Vercel Serverless"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "message": "FastAPI GraphQL Backend is running on Vercel",
        "environment": settings.environment,
        "debug": settings.debug,
        "platform": "Vercel Serverless"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    HTTP exception handler.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


# Wrap the FastAPI app with Mangum for AWS Lambda compatibility (Vercel uses this under the hood)
handler = Mangum(app)
