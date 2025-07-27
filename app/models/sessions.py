"""
Session model for tracking user sessions.
"""

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class Session(BaseModel):
    """
    Session model for tracking user sessions.
    
    Tracks:
    - User sessions with start/end times
    - Session duration and interaction counts
    - Active session status
    """
    
    __tablename__ = "sessions"
    
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the user who owns this session"
    )
    session_id = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
        comment="Unique session identifier"
    )
    url = Column(
        String,
        nullable=True,
        comment="URL where the session was started"
    )
    start_time = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="Timestamp when the session started"
    )
    end_time = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp when the session ended"
    )
    duration = Column(
        Integer,
        nullable=True,
        comment="Session duration in seconds"
    )
    interaction_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of interactions during the session"
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Whether the session is currently active"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_sessions_user_active", "user_id", "is_active"),
        Index("idx_sessions_start_time", "start_time"),
        Index("idx_sessions_end_time", "end_time"),
    )
    
    def __repr__(self) -> str:
        """String representation of the session."""
        return f"<Session(id={self.id}, user_id={self.user_id}, session_id={self.session_id})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if the session is completed (has end time)."""
        return self.end_time is not None
    
    def calculate_duration(self) -> int:
        """Calculate session duration in seconds."""
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds())
        return 0 