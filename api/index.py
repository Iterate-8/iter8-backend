"""
Vercel serverless entry point - Full GraphQL Backend with Supabase.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from mangum import Mangum
import os

# Import configuration and schema
from app.config import settings
from app.graphql.schema import schema

# Create FastAPI app (no lifespan for serverless)
app = FastAPI(
    title="Iter8 Backend - GraphQL API",
    description="FastAPI GraphQL Backend with Supabase Integration",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(",") if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create GraphQL router
graphql_app = GraphQLRouter(
    schema,
    graphiql=settings.debug,
    path="/"
)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Iter8 Backend - GraphQL API",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else "Not available in production",
        "graphql": "/graphql",
        "health": "/health",
        "platform": "Vercel Serverless"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "FastAPI GraphQL Backend is running on Vercel",
        "environment": settings.environment,
        "debug": settings.debug,
        "platform": "Vercel Serverless"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


# Export the app directly for Vercel
# Vercel's Python runtime will handle ASGI apps automatically
