"""
GraphQL mutations using asyncpg directly.
"""

import strawberry
from typing import Optional
import uuid
from datetime import datetime
from app.database import get_db
from app.graphql.types import (
    FeedbackType, SessionType, UserInteractionType,
    FeedbackResponse, SessionResponse, UserInteractionResponse,
    DeleteResponse, CreateFeedbackInput, UpdateFeedbackInput,
    CreateSessionInput, UpdateSessionInput, CreateUserInteractionInput
)


@strawberry.type
class Mutation:
    """GraphQL Mutation type with all available mutations."""
    
    @strawberry.mutation
    async def create_feedback(self, input: CreateFeedbackInput) -> FeedbackResponse:
        """
        Create a new feedback entry.
        """
        async for db in get_db():
            try:
                feedback_id = uuid.uuid4()
                await db.execute(
                    """
                    INSERT INTO feedback (id, user_id, feedback_type, feedback, startup_name)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    feedback_id,
                    uuid.UUID(input.user_id),
                    input.feedback_type,
                    input.feedback,
                    input.startup_name
                )
                
                # Fetch the created feedback
                row = await db.fetchrow(
                    """
                    SELECT id, user_id, feedback_type, feedback, startup_name, 
                           created_at, updated_at
                    FROM feedback 
                    WHERE id = $1
                    """,
                    feedback_id
                )
                
                feedback = FeedbackType(
                    id=str(row['id']),
                    user_id=str(row['user_id']),
                    feedback_type=row['feedback_type'],
                    feedback=row['feedback'],
                    startup_name=row['startup_name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                
                return FeedbackResponse(
                    success=True,
                    message="Feedback created successfully",
                    feedback=feedback
                )
            except Exception as e:
                return FeedbackResponse(
                    success=False,
                    message=f"Failed to create feedback: {str(e)}",
                    feedback=None
                )
    
    @strawberry.mutation
    async def update_feedback(self, feedback_id: str, input: UpdateFeedbackInput) -> FeedbackResponse:
        """
        Update an existing feedback entry.
        """
        async for db in get_db():
            try:
                # Update the feedback
                result = await db.execute(
                    """
                    UPDATE feedback 
                    SET feedback_type = COALESCE($2, feedback_type),
                        feedback = COALESCE($3, feedback),
                        startup_name = COALESCE($4, startup_name),
                        updated_at = NOW()
                    WHERE id = $1
                    """,
                    uuid.UUID(feedback_id),
                    input.feedback_type,
                    input.feedback,
                    input.startup_name
                )
                
                if result == "UPDATE 0":
                    return FeedbackResponse(
                        success=False,
                        message="Feedback not found",
                        feedback=None
                    )
                
                # Fetch the updated feedback
                row = await db.fetchrow(
                    """
                    SELECT id, user_id, feedback_type, feedback, startup_name, 
                           created_at, updated_at
                    FROM feedback 
                    WHERE id = $1
                    """,
                    uuid.UUID(feedback_id)
                )
                
                feedback = FeedbackType(
                    id=str(row['id']),
                    user_id=str(row['user_id']),
                    feedback_type=row['feedback_type'],
                    feedback=row['feedback'],
                    startup_name=row['startup_name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                
                return FeedbackResponse(
                    success=True,
                    message="Feedback updated successfully",
                    feedback=feedback
                )
            except Exception as e:
                return FeedbackResponse(
                    success=False,
                    message=f"Failed to update feedback: {str(e)}",
                    feedback=None
                )
    
    @strawberry.mutation
    async def delete_feedback(self, feedback_id: str) -> DeleteResponse:
        """
        Delete a feedback entry.
        """
        async for db in get_db():
            try:
                result = await db.execute(
                    "DELETE FROM feedback WHERE id = $1",
                    uuid.UUID(feedback_id)
                )
                
                if result == "DELETE 0":
                    return DeleteResponse(
                        success=False,
                        message="Feedback not found"
                    )
                
                return DeleteResponse(
                    success=True,
                    message="Feedback deleted successfully"
                )
            except Exception as e:
                return DeleteResponse(
                    success=False,
                    message=f"Failed to delete feedback: {str(e)}"
                )
    
    @strawberry.mutation
    async def create_session(self, input: CreateSessionInput) -> SessionResponse:
        """
        Create a new session.
        """
        async for db in get_db():
            try:
                session_id = uuid.uuid4()
                await db.execute(
                    """
                    INSERT INTO sessions (id, user_id, session_id, url, start_time, is_active)
                    VALUES ($1, $2, $3, $4, NOW(), TRUE)
                    """,
                    session_id,
                    uuid.UUID(input.user_id),
                    input.session_id,
                    input.url
                )
                
                # Fetch the created session
                row = await db.fetchrow(
                    """
                    SELECT id, user_id, session_id, url, start_time, end_time,
                           duration, interaction_count, is_active, created_at, updated_at
                    FROM sessions 
                    WHERE id = $1
                    """,
                    session_id
                )
                
                session = SessionType(
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
                
                return SessionResponse(
                    success=True,
                    message="Session created successfully",
                    session=session
                )
            except Exception as e:
                return SessionResponse(
                    success=False,
                    message=f"Failed to create session: {str(e)}",
                    session=None
                )
    
    @strawberry.mutation
    async def end_session(self, session_id: str) -> SessionResponse:
        """
        End an active session.
        """
        async for db in get_db():
            try:
                # Update the session to end it
                result = await db.execute(
                    """
                    UPDATE sessions 
                    SET end_time = NOW(),
                        duration = EXTRACT(EPOCH FROM (NOW() - start_time))::INTEGER,
                        is_active = FALSE,
                        updated_at = NOW()
                    WHERE id = $1 AND is_active = TRUE
                    """,
                    uuid.UUID(session_id)
                )
                
                if result == "UPDATE 0":
                    return SessionResponse(
                        success=False,
                        message="Session not found or already ended",
                        session=None
                    )
                
                # Fetch the updated session
                row = await db.fetchrow(
                    """
                    SELECT id, user_id, session_id, url, start_time, end_time,
                           duration, interaction_count, is_active, created_at, updated_at
                    FROM sessions 
                    WHERE id = $1
                    """,
                    uuid.UUID(session_id)
                )
                
                session = SessionType(
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
                
                return SessionResponse(
                    success=True,
                    message="Session ended successfully",
                    session=session
                )
            except Exception as e:
                return SessionResponse(
                    success=False,
                    message=f"Failed to end session: {str(e)}",
                    session=None
                ) 