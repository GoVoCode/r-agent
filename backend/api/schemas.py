from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime


class QuickActionButton(BaseModel):
    label: str
    action: str
    widget_type: Literal["button", "date", "time", "number"] = "button"
    widget_config: Optional[Dict[str, Any]] = None


class CreateSessionRequest(BaseModel):
    pass


class CreateSessionResponse(BaseModel):
    session_id: str


class CreateConversationRequest(BaseModel):
    session_id: str


class CreateConversationResponse(BaseModel):
    conversation_id: str
    initial_message: str
    buttons: List[QuickActionButton]


class ChatRequest(BaseModel):
    session_id: str
    conversation_id: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    action: Optional[str] = None
    widget_data: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime
    buttons: Optional[List[QuickActionButton]] = None


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime

