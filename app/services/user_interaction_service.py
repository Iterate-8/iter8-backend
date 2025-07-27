"""
Service layer for user interaction management operations.
"""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.user_interactions import UserInteraction
from app.schemas.user_interactions import UserInteractionCreate

logger = logging.getLogger(__name__)


class UserInteractionService:
    """Service class for user interaction management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_interaction(self, interaction_data: UserInteractionCreate) -> UserInteraction:
        """
        Create a new user interaction.
        
        Args:
            interaction_data: User interaction creation data
            
        Returns:
            UserInteraction: Created interaction instance
            
        Raises:
            Exception: If creation fails
        """
        try:
            interaction = UserInteraction(
                session_id=interaction_data.session_id,
                user_id=interaction_data.user_id,
                interaction_type=interaction_data.interaction_type,
                timestamp=interaction_data.timestamp,
                url=interaction_data.url,
                element_info=interaction_data.element_info,
                data=interaction_data.data
            )
            
            self.db.add(interaction)
            await self.db.commit()
            await self.db.refresh(interaction)
            
            logger.info(f"Created user interaction with ID: {interaction.id}")
            return interaction
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create user interaction: {e}")
            raise
    
    async def get_interaction_by_id(self, interaction_id: UUID) -> Optional[UserInteraction]:
        """
        Get user interaction by ID.
        
        Args:
            interaction_id: Interaction unique identifier
            
        Returns:
            Optional[UserInteraction]: Interaction instance if found, None otherwise
        """
        try:
            result = await self.db.execute(
                select(UserInteraction).where(UserInteraction.id == interaction_id)
            )
            interaction = result.scalar_one_or_none()
            
            if interaction:
                logger.info(f"Retrieved user interaction with ID: {interaction_id}")
            else:
                logger.warning(f"User interaction with ID {interaction_id} not found")
                
            return interaction
            
        except Exception as e:
            logger.error(f"Failed to get user interaction by ID {interaction_id}: {e}")
            raise
    
    async def get_interactions_by_session(
        self,
        session_id: str,
        user_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[UserInteraction]:
        """
        Get user interactions by session ID.
        
        Args:
            session_id: Session identifier
            user_id: Filter by user ID
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List[UserInteraction]: List of interaction instances
        """
        try:
            query = select(UserInteraction).where(
                UserInteraction.session_id == session_id
            ).order_by(UserInteraction.timestamp.desc())
            
            if user_id:
                query = query.where(UserInteraction.user_id == user_id)
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            interactions = result.scalars().all()
            
            logger.info(f"Retrieved {len(interactions)} interactions for session: {session_id}")
            return interactions
            
        except Exception as e:
            logger.error(f"Failed to get interactions for session {session_id}: {e}")
            raise
    
    async def get_interactions_by_user(
        self,
        user_id: UUID,
        session_id: Optional[str] = None,
        interaction_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[UserInteraction]:
        """
        Get user interactions by user ID.
        
        Args:
            user_id: User unique identifier
            session_id: Filter by session ID
            interaction_type: Filter by interaction type
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List[UserInteraction]: List of interaction instances
        """
        try:
            query = select(UserInteraction).where(
                UserInteraction.user_id == user_id
            ).order_by(UserInteraction.timestamp.desc())
            
            if session_id:
                query = query.where(UserInteraction.session_id == session_id)
            
            if interaction_type:
                query = query.where(UserInteraction.interaction_type == interaction_type)
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            interactions = result.scalars().all()
            
            logger.info(f"Retrieved {len(interactions)} interactions for user: {user_id}")
            return interactions
            
        except Exception as e:
            logger.error(f"Failed to get interactions for user {user_id}: {e}")
            raise
    
    async def get_interactions_by_type(
        self,
        interaction_type: str,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[UserInteraction]:
        """
        Get user interactions by interaction type.
        
        Args:
            interaction_type: Type of interaction
            user_id: Filter by user ID
            session_id: Filter by session ID
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List[UserInteraction]: List of interaction instances
        """
        try:
            query = select(UserInteraction).where(
                UserInteraction.interaction_type == interaction_type
            ).order_by(UserInteraction.timestamp.desc())
            
            if user_id:
                query = query.where(UserInteraction.user_id == user_id)
            
            if session_id:
                query = query.where(UserInteraction.session_id == session_id)
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            interactions = result.scalars().all()
            
            logger.info(f"Retrieved {len(interactions)} interactions of type: {interaction_type}")
            return interactions
            
        except Exception as e:
            logger.error(f"Failed to get interactions of type {interaction_type}: {e}")
            raise
    
    async def update_interaction_data(
        self,
        interaction_id: UUID,
        data: Dict[str, Any]
    ) -> Optional[UserInteraction]:
        """
        Update interaction data field.
        
        Args:
            interaction_id: Interaction unique identifier
            data: New data to merge with existing data
            
        Returns:
            Optional[UserInteraction]: Updated interaction instance if found, None otherwise
        """
        try:
            interaction = await self.get_interaction_by_id(interaction_id)
            if not interaction:
                return None
            
            # Merge with existing data
            current_data = interaction.data or {}
            updated_data = {**current_data, **data}
            
            await self.db.execute(
                update(UserInteraction)
                .where(UserInteraction.id == interaction_id)
                .values(data=updated_data)
            )
            await self.db.commit()
            
            # Refresh the instance
            await self.db.refresh(interaction)
            logger.info(f"Updated interaction data for ID: {interaction_id}")
            
            return interaction
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to update interaction data {interaction_id}: {e}")
            raise
    
    async def delete_interaction(self, interaction_id: UUID) -> bool:
        """
        Delete a user interaction.
        
        Args:
            interaction_id: Interaction unique identifier
            
        Returns:
            bool: True if deleted successfully, False if not found
        """
        try:
            # Check if interaction exists
            interaction = await self.get_interaction_by_id(interaction_id)
            if not interaction:
                return False
            
            # Delete the interaction
            await self.db.execute(
                delete(UserInteraction).where(UserInteraction.id == interaction_id)
            )
            await self.db.commit()
            
            logger.info(f"Deleted user interaction with ID: {interaction_id}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to delete user interaction {interaction_id}: {e}")
            raise
    
    async def get_interaction_count(
        self,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        interaction_type: Optional[str] = None
    ) -> int:
        """
        Get count of user interactions with optional filtering.
        
        Args:
            user_id: Filter by user ID
            session_id: Filter by session ID
            interaction_type: Filter by interaction type
            
        Returns:
            int: Count of interactions
        """
        try:
            from sqlalchemy import func
            
            query = select(func.count(UserInteraction.id))
            
            if user_id:
                query = query.where(UserInteraction.user_id == user_id)
            
            if session_id:
                query = query.where(UserInteraction.session_id == session_id)
            
            if interaction_type:
                query = query.where(UserInteraction.interaction_type == interaction_type)
            
            result = await self.db.execute(query)
            count = result.scalar()
            
            return count
            
        except Exception as e:
            logger.error(f"Failed to get interaction count: {e}")
            raise
    
    async def get_interaction_summary(
        self,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Get summary of interaction types and their counts.
        
        Args:
            user_id: Filter by user ID
            session_id: Filter by session ID
            
        Returns:
            Dict[str, int]: Dictionary with interaction types and their counts
        """
        try:
            from sqlalchemy import func
            
            query = select(
                UserInteraction.interaction_type,
                func.count(UserInteraction.id).label('count')
            ).group_by(UserInteraction.interaction_type)
            
            if user_id:
                query = query.where(UserInteraction.user_id == user_id)
            
            if session_id:
                query = query.where(UserInteraction.session_id == session_id)
            
            result = await self.db.execute(query)
            summary = {row.interaction_type: row.count for row in result}
            
            logger.info(f"Generated interaction summary: {summary}")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get interaction summary: {e}")
            raise 