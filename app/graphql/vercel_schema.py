"""
Vercel-optimized GraphQL schema.
"""

import strawberry
from app.graphql.vercel_queries import Query
from app.graphql.mutations import Mutation

# Create the GraphQL schema for Vercel deployment
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
