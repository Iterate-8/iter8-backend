"""
Service layer for feedback/todo management operations.
"""

import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service class for feedback/todo management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_feedback(self, feedback_data: FeedbackCreate) -> Feedback:
        """
        Create a new feedback entry.
        
        Args:
            feedback_data: Feedback creation data
            
        Returns:
            Feedback: Created feedback instance
            
        Raises:
            Exception: If creation fails
        """
        try:
            feedback = Feedback(
                user_id=feedback_data.user_id,
                feedback_type=feedback_data.feedback_type,
                feedback=feedback_data.feedback,
                startup_name=feedback_data.startup_name
            )
            
            self.db.add(feedback)
            await self.db.commit()
            await self.db.refresh(feedback)
            
            logger.info(f"Created feedback with ID: {feedback.id}")
            return feedback
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create feedback: {e}")
            raise
    
    async def get_feedback_by_id(self, feedback_id: UUID) -> Optional[Feedback]:
        """
        Get feedback by ID.
        
        Args:
            feedback_id: Feedback unique identifier
            
        Returns:
            Optional[Feedback]: Feedback instance if found, None otherwise
        """
        try:
            result = await self.db.execute(
                select(Feedback).where(Feedback.id == feedback_id)
            )
            feedback = result.scalar_one_or_none()
            
            if feedback:
                logger.info(f"Retrieved feedback with ID: {feedback_id}")
            else:
                logger.warning(f"Feedback with ID {feedback_id} not found")
                
            return feedback
            
        except Exception as e:
            logger.error(f"Failed to get feedback by ID {feedback_id}: {e}")
            raise
    
    async def get_feedback_list(
        self,
        user_id: Optional[UUID] = None,
        feedback_type: Optional[str] = None,
        startup_name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Feedback]:
        """
        Get list of feedback entries with optional filtering.
        
        Args:
            user_id: Filter by user ID
            feedback_type: Filter by feedback type
            startup_name: Filter by startup name
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List[Feedback]: List of feedback instances
        """
        try:
            query = select(Feedback).order_by(Feedback.created_at.desc())
            
            # Apply filters
            if user_id:
                query = query.where(Feedback.user_id == user_id)
            
            if feedback_type:
                query = query.where(Feedback.feedback_type == feedback_type)
            
            if startup_name:
                query = query.where(Feedback.startup_name == startup_name)
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            feedback_list = result.scalars().all()
            
            logger.info(f"Retrieved {len(feedback_list)} feedback entries")
            return feedback_list
            
        except Exception as e:
            logger.error(f"Failed to get feedback list: {e}")
            raise
    
    async def update_feedback(self, feedback_id: UUID, feedback_data: FeedbackUpdate) -> Optional[Feedback]:
        """
        Update an existing feedback entry.
        
        Args:
            feedback_id: Feedback unique identifier
            feedback_data: Feedback update data
            
        Returns:
            Optional[Feedback]: Updated feedback instance if found, None otherwise
        """
        try:
            # Get existing feedback
            feedback = await self.get_feedback_by_id(feedback_id)
            if not feedback:
                return None
            
            # Update fields
            update_data = feedback_data.dict(exclude_unset=True)
            if update_data:
                await self.db.execute(
                    update(Feedback)
                    .where(Feedback.id == feedback_id)
                    .values(**update_data)
                )
                await self.db.commit()
                
                # Refresh the instance
                await self.db.refresh(feedback)
                logger.info(f"Updated feedback with ID: {feedback_id}")
            
            return feedback
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to update feedback {feedback_id}: {e}")
            raise
    
    async def delete_feedback(self, feedback_id: UUID) -> bool:
        """
        Delete a feedback entry.
        
        Args:
            feedback_id: Feedback unique identifier
            
        Returns:
            bool: True if deleted successfully, False if not found
        """
        try:
            # Check if feedback exists
            feedback = await self.get_feedback_by_id(feedback_id)
            if not feedback:
                return False
            
            # Delete the feedback
            await self.db.execute(
                delete(Feedback).where(Feedback.id == feedback_id)
            )
            await self.db.commit()
            
            logger.info(f"Deleted feedback with ID: {feedback_id}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to delete feedback {feedback_id}: {e}")
            raise
    
    async def get_feedback_count(
        self,
        user_id: Optional[UUID] = None,
        feedback_type: Optional[str] = None
    ) -> int:
        """
        Get count of feedback entries with optional filtering.
        
        Args:
            user_id: Filter by user ID
            feedback_type: Filter by feedback type
            
        Returns:
            int: Count of feedback entries
        """
        try:
            from sqlalchemy import func
            
            query = select(func.count(Feedback.id))
            
            if user_id:
                query = query.where(Feedback.user_id == user_id)
            
            if feedback_type:
                query = query.where(Feedback.feedback_type == feedback_type)
            
            result = await self.db.execute(query)
            count = result.scalar()
            
            return count
            
        except Exception as e:
            logger.error(f"Failed to get feedback count: {e}")
            raise 