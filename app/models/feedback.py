"""
Feedback model for todo/feedback management.
"""

from sqlalchemy import Column, String, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class Feedback(BaseModel):
    """
    Feedback model for todo/feedback management.
    
    Supports:
    - Different feedback types (todo, feedback, suggestion, etc.)
    - User-specific feedback entries
    - Startup-specific feedback
    """
    
    __tablename__ = "feedback"
    
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the user who created this feedback"
    )
    feedback_type = Column(
        String(50),
        nullable=False,
        index=True,
        comment="Type of feedback (todo, feedback, suggestion, etc.)"
    )
    feedback = Column(
        Text,
        nullable=False,
        comment="The actual feedback content"
    )
    startup_name = Column(
        String(255),
        nullable=True,
        index=True,
        comment="Name of the startup this feedback relates to"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_feedback_user_type", "user_id", "feedback_type"),
        Index("idx_feedback_startup", "startup_name"),
        Index("idx_feedback_created_at", "created_at"),
    )
    
    def __repr__(self) -> str:
        """String representation of the feedback."""
        return f"<Feedback(id={self.id}, user_id={self.user_id}, type={self.feedback_type})>"
    
    @property
    def is_todo(self) -> bool:
        """Check if this feedback is a todo item."""
        return self.feedback_type.lower() in ["todo", "task", "action"]
    
    @property
    def is_feedback(self) -> bool:
        """Check if this feedback is a feedback item."""
        return self.feedback_type.lower() in ["feedback", "suggestion", "comment"] 