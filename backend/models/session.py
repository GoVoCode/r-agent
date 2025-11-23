from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import uuid4


class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Conversation(BaseModel):
    conversation_id: str = Field(default_factory=lambda: str(uuid4()))
    messages: List[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        message = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(message)
        self.updated_at = datetime.now()
        self.last_activity = datetime.now()
    
    def is_inactive(self, minutes: int = 30) -> bool:
        """Check if conversation has been inactive for specified minutes."""
        return datetime.now() - self.last_activity > timedelta(minutes=minutes)


class Session(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    conversations: Dict[str, Conversation] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    def create_conversation(self) -> str:
        conversation = Conversation()
        self.conversations[conversation.conversation_id] = conversation
        return conversation.conversation_id
    
    def get_conversation(self, conversation_id: str) -> Conversation:
        return self.conversations.get(conversation_id)

