from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class ChatMessage:
    """Chat mesajı modeli"""
    role: str  # 'user' veya 'assistant'
    content: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

@dataclass
class ConversationSession:
    """Konuşma oturumu modeli"""
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def add_message(self, role: str, content: str):
        """Oturuma yeni mesaj ekle"""
        message = ChatMessage(role=role, content=content)
        self.messages.append(message)
    
    def get_conversation_context(self, max_messages: int = 10) -> List[Dict[str, str]]:
        """OpenAI API formatında konuşma bağlamını döndür"""
        recent_messages = self.messages[-max_messages:] if len(self.messages) > max_messages else self.messages
        return [{'role': msg.role, 'content': msg.content} for msg in recent_messages]
