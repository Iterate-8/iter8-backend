"""
Service layer for session management operations.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.sessions import Session
from app.schemas.sessions import SessionCreate, SessionUpdate

logger = logging.getLogger(__name__)


class SessionService:
    """Service class for session management operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_session(self, session_data: SessionCreate) -> Session:
        """
        Create a new session.
        
        Args:
            session_data: Session creation data
            
        Returns:
            Session: Created session instance
            
        Raises:
            Exception: If creation fails
        """
        try:
            session = Session(
                user_id=session_data.user_id,
                session_id=session_data.session_id,
                url=session_data.url,
                start_time=session_data.start_time,
                end_time=session_data.end_time,
                duration=session_data.duration,
                interaction_count=session_data.interaction_count,
                is_active=session_data.is_active
            )
            
            self.db.add(session)
            await self.db.commit()
            await self.db.refresh(session)
            
            logger.info(f"Created session with ID: {session.id}")
            return session
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to create session: {e}")
            raise
    
    async def get_session_by_id(self, session_id: UUID) -> Optional[Session]:
        """
        Get session by ID.
        
        Args:
            session_id: Session unique identifier
            
        Returns:
            Optional[Session]: Session instance if found, None otherwise
        """
        try:
            result = await self.db.execute(
                select(Session).where(Session.id == session_id)
            )
            session = result.scalar_one_or_none()
            
            if session:
                logger.info(f"Retrieved session with ID: {session_id}")
            else:
                logger.warning(f"Session with ID {session_id} not found")
                
            return session
            
        except Exception as e:
            logger.error(f"Failed to get session by ID {session_id}: {e}")
            raise
    
    async def get_session_by_session_id(self, session_id: str) -> Optional[Session]:
        """
        Get session by session_id string.
        
        Args:
            session_id: Session identifier string
            
        Returns:
            Optional[Session]: Session instance if found, None otherwise
        """
        try:
            result = await self.db.execute(
                select(Session).where(Session.session_id == session_id)
            )
            session = result.scalar_one_or_none()
            
            if session:
                logger.info(f"Retrieved session with session_id: {session_id}")
            else:
                logger.warning(f"Session with session_id {session_id} not found")
                
            return session
            
        except Exception as e:
            logger.error(f"Failed to get session by session_id {session_id}: {e}")
            raise
    
    async def get_sessions_list(
        self,
        user_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Session]:
        """
        Get list of sessions with optional filtering.
        
        Args:
            user_id: Filter by user ID
            is_active: Filter by active status
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List[Session]: List of session instances
        """
        try:
            query = select(Session).order_by(Session.created_at.desc())
            
            # Apply filters
            if user_id:
                query = query.where(Session.user_id == user_id)
            
            if is_active is not None:
                query = query.where(Session.is_active == is_active)
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = await self.db.execute(query)
            sessions_list = result.scalars().all()
            
            logger.info(f"Retrieved {len(sessions_list)} sessions")
            return sessions_list
            
        except Exception as e:
            logger.error(f"Failed to get sessions list: {e}")
            raise
    
    async def update_session(self, session_id: UUID, session_data: SessionUpdate) -> Optional[Session]:
        """
        Update an existing session.
        
        Args:
            session_id: Session unique identifier
            session_data: Session update data
            
        Returns:
            Optional[Session]: Updated session instance if found, None otherwise
        """
        try:
            # Get existing session
            session = await self.get_session_by_id(session_id)
            if not session:
                return None
            
            # Update fields
            update_data = session_data.dict(exclude_unset=True)
            if update_data:
                await self.db.execute(
                    update(Session)
                    .where(Session.id == session_id)
                    .values(**update_data)
                )
                await self.db.commit()
                
                # Refresh the instance
                await self.db.refresh(session)
                logger.info(f"Updated session with ID: {session_id}")
            
            return session
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to update session {session_id}: {e}")
            raise
    
    async def end_session(self, session_id: UUID) -> Optional[Session]:
        """
        End a session by setting end time and calculating duration.
        
        Args:
            session_id: Session unique identifier
            
        Returns:
            Optional[Session]: Updated session instance if found, None otherwise
        """
        try:
            session = await self.get_session_by_id(session_id)
            if not session:
                return None
            
            if session.is_completed:
                logger.warning(f"Session {session_id} is already completed")
                return session
            
            # Set end time and calculate duration
            end_time = datetime.now(timezone.utc)
            duration = int((end_time - session.start_time).total_seconds())
            
            update_data = {
                "end_time": end_time,
                "duration": duration,
                "is_active": False
            }
            
            await self.db.execute(
                update(Session)
                .where(Session.id == session_id)
                .values(**update_data)
            )
            await self.db.commit()
            
            # Refresh the instance
            await self.db.refresh(session)
            logger.info(f"Ended session with ID: {session_id}, duration: {duration}s")
            
            return session
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to end session {session_id}: {e}")
            raise
    
    async def increment_interaction_count(self, session_id: UUID) -> Optional[Session]:
        """
        Increment the interaction count for a session.
        
        Args:
            session_id: Session unique identifier
            
        Returns:
            Optional[Session]: Updated session instance if found, None otherwise
        """
        try:
            session = await self.get_session_by_id(session_id)
            if not session:
                return None
            
            await self.db.execute(
                update(Session)
                .where(Session.id == session_id)
                .values(interaction_count=Session.interaction_count + 1)
            )
            await self.db.commit()
            
            # Refresh the instance
            await self.db.refresh(session)
            logger.info(f"Incremented interaction count for session: {session_id}")
            
            return session
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to increment interaction count for session {session_id}: {e}")
            raise
    
    async def delete_session(self, session_id: UUID) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session unique identifier
            
        Returns:
            bool: True if deleted successfully, False if not found
        """
        try:
            # Check if session exists
            session = await self.get_session_by_id(session_id)
            if not session:
                return False
            
            # Delete the session
            await self.db.execute(
                delete(Session).where(Session.id == session_id)
            )
            await self.db.commit()
            
            logger.info(f"Deleted session with ID: {session_id}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to delete session {session_id}: {e}")
            raise
    
    async def get_active_sessions_count(self, user_id: Optional[UUID] = None) -> int:
        """
        Get count of active sessions.
        
        Args:
            user_id: Filter by user ID
            
        Returns:
            int: Count of active sessions
        """
        try:
            from sqlalchemy import func
            
            query = select(func.count(Session.id)).where(Session.is_active == True)
            
            if user_id:
                query = query.where(Session.user_id == user_id)
            
            result = await self.db.execute(query)
            count = result.scalar()
            
            return count
            
        except Exception as e:
            logger.error(f"Failed to get active sessions count: {e}")
            raise 