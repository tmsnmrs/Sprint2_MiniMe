from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    """Model for chat messages"""
    content: str
    role: Optional[str] = "user"
    task_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Model for chat responses"""
    content: str
    task_id: Optional[str] = None
    metadata: Optional[dict] = None 