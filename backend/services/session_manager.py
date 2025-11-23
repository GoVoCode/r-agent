from typing import Dict, Optional
from backend.models import Session, Conversation
from backend.core import get_logger

logger = get_logger("session_manager")


class SessionManager:
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        logger.info("SessionManager initialized")
    
    def create_session(self) -> str:
        session = Session()
        self._sessions[session.session_id] = session
        logger.info(f"Created session: {session.session_id}")
        return session.session_id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        session = self._sessions.get(session_id)
        if not session:
            logger.warning(f"Session not found: {session_id}")
        return session
    
    def create_conversation(self, session_id: str) -> Optional[str]:
        session = self.get_session(session_id)
        if not session:
            return None
        
        conversation_id = session.create_conversation()
        logger.info(f"Created conversation {conversation_id} in session {session_id}")
        return conversation_id
    
    def get_conversation(self, session_id: str, conversation_id: str) -> Optional[Conversation]:
        session = self.get_session(session_id)
        if not session:
            return None
        
        conversation = session.get_conversation(conversation_id)
        if not conversation:
            logger.warning(f"Conversation {conversation_id} not found in session {session_id}")
        return conversation
    
    def delete_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        logger.warning(f"Attempted to delete non-existent session: {session_id}")
        return False


session_manager = SessionManager()

