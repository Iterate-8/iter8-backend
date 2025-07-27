"""
UserInteraction model for tracking user interactions.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import BaseModel


class UserInteraction(BaseModel):
    """
    UserInteraction model for tracking user interactions.
    
    Tracks:
    - User interactions during sessions
    - Interaction types and timestamps
    - Element information and additional data in JSON format
    """
    
    __tablename__ = "user_interactions"
    
    session_id = Column(
        String,
        nullable=False,
        index=True,
        comment="Session identifier this interaction belongs to"
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the user who performed this interaction"
    )
    interaction_type = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Type of interaction (click, scroll, form_submit, etc.)"
    )
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Timestamp when the interaction occurred"
    )
    url = Column(
        String,
        nullable=True,
        comment="URL where the interaction occurred"
    )
    element_info = Column(
        JSONB,
        nullable=True,
        comment="Information about the element interacted with"
    )
    data = Column(
        JSONB,
        nullable=True,
        comment="Additional data related to the interaction"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_user_interactions_session", "session_id"),
        Index("idx_user_interactions_user", "user_id"),
        Index("idx_user_interactions_type", "interaction_type"),
        Index("idx_user_interactions_timestamp", "timestamp"),
        Index("idx_user_interactions_session_user", "session_id", "user_id"),
    )
    
    def __repr__(self) -> str:
        """String representation of the user interaction."""
        return f"<UserInteraction(id={self.id}, session_id={self.session_id}, type={self.interaction_type})>"
    
    @property
    def interaction_data(self) -> dict:
        """Get the interaction data as a dictionary."""
        return {
            "id": str(self.id),
            "session_id": self.session_id,
            "user_id": str(self.user_id),
            "interaction_type": self.interaction_type,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "url": self.url,
            "element_info": self.element_info,
            "data": self.data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        } 