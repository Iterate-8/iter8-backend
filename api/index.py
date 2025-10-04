"""
Vercel serverless entry point - Full GraphQL Backend with Supabase.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
from mangum import Mangum
import os

# Import configuration and Vercel-optimized schema
from app.config import settings
from app.graphql.vercel_schema import schema
from app.vercel_database import get_db

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

# Create GraphQL router - mount directly at /graphql
graphql_app = GraphQLRouter(schema, graphiql=True)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql", include_in_schema=True)


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
    import os
    return {
        "status": "healthy",
        "message": "FastAPI GraphQL Backend is running on Vercel",
        "environment": settings.environment,
        "debug": settings.debug,
        "platform": "Vercel Serverless",
        "database_url_set": "DATABASE_URL" in os.environ,
        "database_url_length": len(os.environ.get("DATABASE_URL", ""))
    }

@app.get("/env-check")
async def env_check():
    """Check environment variables (for debugging)."""
    import os
    return {
        "DATABASE_URL_set": "DATABASE_URL" in os.environ,
        "SUPABASE_URL_set": "SUPABASE_URL" in os.environ,
        "SUPABASE_ANON_KEY_set": "SUPABASE_ANON_KEY" in os.environ,
        "SUPABASE_SERVICE_ROLE_KEY_set": "SUPABASE_SERVICE_ROLE_KEY" in os.environ
    }


@app.get("/db-check")
async def db_check():
    """Attempt a live DB connection and return basic info."""
    try:
        async for conn in get_db():
            ping = await conn.fetchval("select 1")
            server_version = await conn.fetchval("show server_version")
            current_user = await conn.fetchval("select current_user")
            server_addr = await conn.fetchval("select inet_server_addr()::text")
            server_port = await conn.fetchval("select inet_server_port()")
            return {
                "success": True,
                "ping": ping,
                "server_version": server_version,
                "current_user": current_user,
                "server_addr": server_addr,
                "server_port": server_port,
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
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
