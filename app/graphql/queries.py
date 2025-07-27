"""
GraphQL queries using asyncpg directly.
"""

import strawberry
from typing import List, Optional
import uuid
from app.database import get_db
from app.graphql.types import (
    FeedbackType, SessionType, UserInteractionType,
    FeedbackListResponse, SessionListResponse, UserInteractionListResponse,
    InteractionSummaryResponse
)


@strawberry.type
class Query:
    """GraphQL queries."""
    
    @strawberry.field
    async def get_feedback_by_id(self, id: str) -> Optional[FeedbackType]:
        """Get feedback by ID."""
        async for db in get_db():
            try:
                row = await db.fetchrow(
                    """
                    SELECT id, user_id, feedback_type, feedback, startup_name, 
                           created_at, updated_at
                    FROM feedback 
                    WHERE id = $1
                    """,
                    uuid.UUID(id)
                )
                if row:
                    return FeedbackType(
                        id=str(row['id']),
                        user_id=str(row['user_id']),
                        feedback_type=row['feedback_type'],
                        feedback=row['feedback'],
                        startup_name=row['startup_name'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                return None
            except Exception as e:
                print(f"Error getting feedback by ID: {e}")
                return None
    
    @strawberry.field
    async def get_feedback_list(
        self, 
        user_id: Optional[str] = None,
        feedback_type: Optional[str] = None,
        startup_name: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> FeedbackListResponse:
        """Get list of feedback with optional filtering."""
        async for db in get_db():
            try:
                # Build query
                query = "SELECT id, user_id, feedback_type, feedback, startup_name, created_at, updated_at FROM feedback WHERE 1=1"
                params = []
                param_count = 0
                
                if user_id:
                    param_count += 1
                    query += f" AND user_id = ${param_count}"
                    params.append(uuid.UUID(user_id))
                
                if feedback_type:
                    param_count += 1
                    query += f" AND feedback_type = ${param_count}"
                    params.append(feedback_type)
                
                if startup_name:
                    param_count += 1
                    query += f" AND startup_name ILIKE ${param_count}"
                    params.append(f"%{startup_name}%")
                
                query += " ORDER BY created_at DESC LIMIT $%d OFFSET $%d" % (param_count + 1, param_count + 2)
                params.extend([limit, offset])
                
                rows = await db.fetch(query, *params)
                
                feedback_list = [
                    FeedbackType(
                        id=str(row['id']),
                        user_id=str(row['user_id']),
                        feedback_type=row['feedback_type'],
                        feedback=row['feedback'],
                        startup_name=row['startup_name'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                    for row in rows
                ]
                
                # Get total count
                count_query = "SELECT COUNT(*) FROM feedback WHERE 1=1"
                count_params = []
                param_count = 0
                
                if user_id:
                    param_count += 1
                    count_query += f" AND user_id = ${param_count}"
                    count_params.append(uuid.UUID(user_id))
                
                if feedback_type:
                    param_count += 1
                    count_query += f" AND feedback_type = ${param_count}"
                    count_params.append(feedback_type)
                
                if startup_name:
                    param_count += 1
                    count_query += f" AND startup_name ILIKE ${param_count}"
                    count_params.append(f"%{startup_name}%")
                
                total_count = await db.fetchval(count_query, *count_params)
                
                return FeedbackListResponse(
                    success=True,
                    message="Feedback list retrieved successfully",
                    feedback_list=feedback_list,
                    total_count=total_count
                )
                
            except Exception as e:
                print(f"Error getting feedback list: {e}")
                return FeedbackListResponse(
                    success=False,
                    message=f"Error getting feedback list: {e}",
                    feedback_list=[],
                    total_count=0
                )
    
    @strawberry.field
    async def get_session_by_id(self, id: str) -> Optional[SessionType]:
        """Get session by ID."""
        async for db in get_db():
            try:
                row = await db.fetchrow(
                    """
                    SELECT id, user_id, session_id, url, start_time, end_time,
                           duration, interaction_count, is_active, created_at, updated_at
                    FROM sessions 
                    WHERE id = $1
                    """,
                    uuid.UUID(id)
                )
                if row:
                    return SessionType(
                        id=str(row['id']),
                        user_id=str(row['user_id']),
                        session_id=row['session_id'],
                        url=row['url'],
                        start_time=row['start_time'],
                        end_time=row['end_time'],
                        duration=row['duration'],
                        interaction_count=row['interaction_count'],
                        is_active=row['is_active'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                return None
            except Exception as e:
                print(f"Error getting session by ID: {e}")
                return None
    
    @strawberry.field
    async def get_sessions_list(
        self,
        user_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 10,
        offset: int = 0
    ) -> SessionListResponse:
        """Get list of sessions with optional filtering."""
        async for db in get_db():
            try:
                # Build query
                query = "SELECT id, user_id, session_id, url, start_time, end_time, duration, interaction_count, is_active, created_at, updated_at FROM sessions WHERE 1=1"
                params = []
                param_count = 0
                
                if user_id:
                    param_count += 1
                    query += f" AND user_id = ${param_count}"
                    params.append(uuid.UUID(user_id))
                
                if is_active is not None:
                    param_count += 1
                    query += f" AND is_active = ${param_count}"
                    params.append(is_active)
                
                query += " ORDER BY created_at DESC LIMIT $%d OFFSET $%d" % (param_count + 1, param_count + 2)
                params.extend([limit, offset])
                
                rows = await db.fetch(query, *params)
                
                sessions_list = [
                    SessionType(
                        id=str(row['id']),
                        user_id=str(row['user_id']),
                        session_id=row['session_id'],
                        url=row['url'],
                        start_time=row['start_time'],
                        end_time=row['end_time'],
                        duration=row['duration'],
                        interaction_count=row['interaction_count'],
                        is_active=row['is_active'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at']
                    )
                    for row in rows
                ]
                
                # Get total count
                count_query = "SELECT COUNT(*) FROM sessions WHERE 1=1"
                count_params = []
                param_count = 0
                
                if user_id:
                    param_count += 1
                    count_query += f" AND user_id = ${param_count}"
                    count_params.append(uuid.UUID(user_id))
                
                if is_active is not None:
                    param_count += 1
                    count_query += f" AND is_active = ${param_count}"
                    count_params.append(is_active)
                
                total_count = await db.fetchval(count_query, *count_params)
                
                return SessionListResponse(
                    success=True,
                    message="Sessions list retrieved successfully",
                    sessions_list=sessions_list,
                    total_count=total_count
                )
                
            except Exception as e:
                print(f"Error getting sessions list: {e}")
                return SessionListResponse(
                    success=False,
                    message=f"Error getting sessions list: {e}",
                    sessions_list=[],
                    total_count=0
                ) 