"""
Pydantic schemas for Feedback model.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class FeedbackBase(BaseModel):
    """Base schema for feedback data."""
    
    feedback_type: str = Field(..., description="Type of feedback (todo, feedback, suggestion, etc.)")
    feedback: str = Field(..., description="The actual feedback content")
    startup_name: Optional[str] = Field(None, description="Name of the startup this feedback relates to")


class FeedbackCreate(FeedbackBase):
    """Schema for creating new feedback."""
    
    user_id: UUID = Field(..., description="User ID who created this feedback")


class FeedbackUpdate(BaseModel):
    """Schema for updating feedback."""
    
    feedback_type: Optional[str] = Field(None, description="Type of feedback (todo, feedback, suggestion, etc.)")
    feedback: Optional[str] = Field(None, description="The actual feedback content")
    startup_name: Optional[str] = Field(None, description="Name of the startup this feedback relates to")


class FeedbackResponse(FeedbackBase):
    """Schema for feedback response."""
    
    id: UUID = Field(..., description="Feedback unique identifier")
    user_id: UUID = Field(..., description="User ID who created this feedback")
    created_at: datetime = Field(..., description="Timestamp when the feedback was created")
    updated_at: datetime = Field(..., description="Timestamp when the feedback was last updated")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str
        } 