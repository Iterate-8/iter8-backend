"""
GraphQL schema and resolvers for the FastAPI backend.
"""

from .schema import schema
from .types import *
from .queries import *
from .mutations import *

__all__ = ["schema"] 