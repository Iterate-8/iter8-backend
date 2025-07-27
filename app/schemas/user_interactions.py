"""
Pydantic schemas for UserInteraction model.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class UserInteractionBase(BaseModel):
    """Base schema for user interaction data."""
    
    session_id: str = Field(..., description="Session identifier this interaction belongs to")
    interaction_type: str = Field(..., description="Type of interaction (click, scroll, form_submit, etc.)")
    timestamp: datetime = Field(..., description="Timestamp when the interaction occurred")
    url: Optional[str] = Field(None, description="URL where the interaction occurred")
    element_info: Optional[Dict[str, Any]] = Field(None, description="Information about the element interacted with")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data related to the interaction")


class UserInteractionCreate(UserInteractionBase):
    """Schema for creating new user interaction."""
    
    user_id: UUID = Field(..., description="User ID who performed this interaction")


class UserInteractionResponse(UserInteractionBase):
    """Schema for user interaction response."""
    
    id: UUID = Field(..., description="User interaction unique identifier")
    user_id: UUID = Field(..., description="User ID who performed this interaction")
    created_at: datetime = Field(..., description="Timestamp when the interaction was created")
    updated_at: datetime = Field(..., description="Timestamp when the interaction was last updated")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str
        } 