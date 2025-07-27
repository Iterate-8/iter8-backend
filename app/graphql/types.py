"""
GraphQL types for the FastAPI backend.
"""

import strawberry
from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from strawberry.scalars import JSON


@strawberry.type
class FeedbackType:
    """GraphQL type for Feedback model."""
    
    id: UUID
    user_id: UUID
    feedback_type: str
    feedback: str
    startup_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_model(cls, model):
        """Create GraphQL type from SQLAlchemy model."""
        return cls(
            id=model.id,
            user_id=model.user_id,
            feedback_type=model.feedback_type,
            feedback=model.feedback,
            startup_name=model.startup_name,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


@strawberry.type
class SessionType:
    """GraphQL type for Session model."""
    
    id: UUID
    user_id: UUID
    session_id: str
    url: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[int]
    interaction_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_model(cls, model):
        """Create GraphQL type from SQLAlchemy model."""
        return cls(
            id=model.id,
            user_id=model.user_id,
            session_id=model.session_id,
            url=model.url,
            start_time=model.start_time,
            end_time=model.end_time,
            duration=model.duration,
            interaction_count=model.interaction_count,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


@strawberry.type
class UserInteractionType:
    """GraphQL type for UserInteraction model."""
    
    id: UUID
    session_id: str
    user_id: UUID
    interaction_type: str
    timestamp: datetime
    url: Optional[str]
    element_info: Optional[JSON]
    data: Optional[JSON]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_model(cls, model):
        """Create GraphQL type from SQLAlchemy model."""
        return cls(
            id=model.id,
            session_id=model.session_id,
            user_id=model.user_id,
            interaction_type=model.interaction_type,
            timestamp=model.timestamp,
            url=model.url,
            element_info=model.element_info,
            data=model.data,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


# Input types for mutations
@strawberry.input
class CreateFeedbackInput:
    """Input type for creating feedback."""
    
    user_id: UUID
    feedback_type: str
    feedback: str
    startup_name: Optional[str] = None


@strawberry.input
class UpdateFeedbackInput:
    """Input type for updating feedback."""
    
    feedback_type: Optional[str] = None
    feedback: Optional[str] = None
    startup_name: Optional[str] = None


@strawberry.input
class CreateSessionInput:
    """Input type for creating session."""
    
    user_id: UUID
    session_id: str
    url: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    interaction_count: int = 0
    is_active: bool = True


@strawberry.input
class UpdateSessionInput:
    """Input type for updating session."""
    
    url: Optional[str] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    interaction_count: Optional[int] = None
    is_active: Optional[bool] = None


@strawberry.input
class CreateUserInteractionInput:
    """Input type for creating user interaction."""
    
    session_id: str
    user_id: UUID
    interaction_type: str
    timestamp: datetime
    url: Optional[str] = None
    element_info: Optional[JSON] = None
    data: Optional[JSON] = None


# Response types
@strawberry.type
class FeedbackResponse:
    """Response type for feedback operations."""
    
    success: bool
    message: str
    feedback: Optional[FeedbackType] = None


@strawberry.type
class FeedbackListResponse:
    """Response type for feedback list operations."""
    
    success: bool
    message: str
    feedback_list: List[FeedbackType]
    total_count: int


@strawberry.type
class SessionResponse:
    """Response type for session operations."""
    
    success: bool
    message: str
    session: Optional[SessionType] = None


@strawberry.type
class SessionListResponse:
    """Response type for session list operations."""
    
    success: bool
    message: str
    sessions_list: List[SessionType]
    total_count: int


@strawberry.type
class UserInteractionResponse:
    """Response type for user interaction operations."""
    
    success: bool
    message: str
    interaction: Optional[UserInteractionType] = None


@strawberry.type
class UserInteractionListResponse:
    """Response type for user interaction list operations."""
    
    success: bool
    message: str
    interactions_list: List[UserInteractionType]
    total_count: int


@strawberry.type
class DeleteResponse:
    """Response type for delete operations."""
    
    success: bool
    message: str


@strawberry.type
class InteractionSummaryType:
    """Type for interaction summary data."""
    
    interaction_type: str
    count: int


@strawberry.type
class InteractionSummaryResponse:
    """Response type for interaction summary."""
    
    success: bool
    message: str
    summary: List[InteractionSummaryType] 