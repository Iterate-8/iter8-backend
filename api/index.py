"""
Vercel serverless entry point - simplified for serverless compatibility.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import os

# Import configuration and schema
from app.config import settings
from app.graphql.schema import schema

# Create FastAPI app without lifespan events for serverless
app = FastAPI(
    title="Iter8 Backend - GraphQL API (Vercel)",
    description="FastAPI GraphQL Backend with Supabase Integration",
    version="1.0.0",
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL router
graphql_app = GraphQLRouter(schema, graphiql=True, path="/")
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Iter8 Backend - GraphQL API (Vercel)",
        "version": "1.0.0",
        "graphql": "/graphql",
        "health": "/health",
        "platform": "Vercel Serverless"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "platform": "Vercel",
        "environment": os.environ.get("ENVIRONMENT", "production")
    }
