import requests
from typing import Dict, Any, List, Optional
from frontend.core import get_frontend_settings, get_frontend_logger

logger = get_frontend_logger("api_client")
settings = get_frontend_settings()


class APIClient:
    def __init__(self):
        self.base_url = settings.backend_api_url
        logger.info(f"APIClient initialized with base URL: {self.base_url}")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug(f"{method} request to {url}")
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None
    
    def health_check(self) -> bool:
        response = self._make_request("GET", "/api/v1/health")
        return response is not None and response.get("status") == "healthy"
    
    def create_session(self) -> Optional[str]:
        logger.info("Creating new session")
        response = self._make_request("POST", "/api/v1/session")
        if response:
            session_id = response.get("session_id")
            logger.info(f"Session created: {session_id}")
            return session_id
        return None
    
    def create_conversation(self, session_id: str) -> Optional[Dict[str, Any]]:
        logger.info(f"Creating conversation for session: {session_id}")
        response = self._make_request(
            "POST",
            "/api/v1/conversation",
            json={"session_id": session_id}
        )
        if response:
            logger.info(f"Conversation created: {response.get('conversation_id')}")
            return response
        return None
    
    def send_message(
        self, 
        session_id: str, 
        conversation_id: str, 
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        action: Optional[str] = None,
        widget_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        logger.info(f"Sending message in conversation: {conversation_id}")
        response = self._make_request(
            "POST",
            "/api/v1/chat",
            json={
                "session_id": session_id,
                "conversation_id": conversation_id,
                "message": message,
                "metadata": metadata or {},
                "action": action,
                "widget_data": widget_data
            }
        )
        return response
    
    def get_conversation_history(
        self, 
        session_id: str, 
        conversation_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        logger.info(f"Fetching conversation history: {conversation_id}")
        response = self._make_request(
            "GET",
            f"/api/v1/conversation/{session_id}/{conversation_id}"
        )
        if response:
            return response.get("messages", [])
        return None


api_client = APIClient()

