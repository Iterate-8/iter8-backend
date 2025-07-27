"""
Pydantic schemas for Session model.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class SessionBase(BaseModel):
    """Base schema for session data."""
    
    session_id: str = Field(..., description="Unique session identifier")
    url: Optional[str] = Field(None, description="URL where the session was started")
    start_time: datetime = Field(..., description="Timestamp when the session started")
    end_time: Optional[datetime] = Field(None, description="Timestamp when the session ended")
    duration: Optional[int] = Field(None, description="Session duration in seconds")
    interaction_count: int = Field(0, description="Number of interactions during the session")
    is_active: bool = Field(True, description="Whether the session is currently active")


class SessionCreate(SessionBase):
    """Schema for creating a new session."""
    
    user_id: UUID = Field(..., description="User ID who owns this session")


class SessionUpdate(BaseModel):
    """Schema for updating a session."""
    
    url: Optional[str] = Field(None, description="URL where the session was started")
    end_time: Optional[datetime] = Field(None, description="Timestamp when the session ended")
    duration: Optional[int] = Field(None, description="Session duration in seconds")
    interaction_count: Optional[int] = Field(None, description="Number of interactions during the session")
    is_active: Optional[bool] = Field(None, description="Whether the session is currently active")


class SessionResponse(SessionBase):
    """Schema for session response."""
    
    id: UUID = Field(..., description="Session unique identifier")
    user_id: UUID = Field(..., description="User ID who owns this session")
    created_at: datetime = Field(..., description="Timestamp when the session was created")
    updated_at: datetime = Field(..., description="Timestamp when the session was last updated")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str
        } 