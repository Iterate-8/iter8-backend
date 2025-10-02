"""
Vercel-optimized GraphQL schema.
"""

import strawberry
from app.graphql.vercel_queries import Query

# For now, just use queries - mutations can be added later
# This avoids the database import conflict
@strawberry.type
class Mutation:
    """Placeholder mutation for Vercel deployment."""
    
    @strawberry.mutation
    async def health_check(self) -> str:
        """Health check mutation."""
        return "Mutations will be added soon"

# Create the GraphQL schema for Vercel deployment
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
