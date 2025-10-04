"""
Main FastAPI application with GraphQL integration.
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter
import uvicorn

from app.config import settings
from app.database import init_db, close_db

# Detect Vercel serverless environment
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("VERCEL_URL") or os.getenv("VERCEL_ENV"))

# Choose schema based on environment: Vercel uses serverless-optimized schema
if IS_VERCEL:
    from app.graphql.vercel_schema import schema  # type: ignore
else:
    from app.graphql.schema import schema  # type: ignore

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting FastAPI GraphQL Backend...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        logger.warning("Application will start without database connection")
        logger.warning("GraphQL queries/mutations will fail until database is connected")
        # Don't raise the exception - let the app start anyway
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI GraphQL Backend...")
    try:
        await close_db()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="Iter8 Backend - GraphQL API",
    description="FastAPI GraphQL Backend with Supabase Integration for Todo/Feedback Management",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=None if IS_VERCEL else lifespan
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
    graphiql=settings.debug  # Enable GraphiQL in development
)

# Include GraphQL router
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Iter8 Backend - GraphQL API",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else "Not available in production",
        "graphql": "/graphql",
        "health": "/health",
        "platform": "Vercel Serverless" if IS_VERCEL else "Standard ASGI"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "message": "FastAPI GraphQL Backend is running",
        "environment": settings.environment,
        "debug": settings.debug,
        "platform": "Vercel Serverless" if IS_VERCEL else "Standard ASGI"
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


if __name__ == "__main__":
    """
    Run the application directly for development.
    """
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 