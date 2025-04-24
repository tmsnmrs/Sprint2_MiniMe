from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class ChatMessage:
    role: str
    content: str
    message_id: str = None
    timestamp: datetime = None
    task_id: Optional[str] = None
    context_used: Optional[List[dict]] = None
    
    def __post_init__(self):
        if self.message_id is None:
            self.message_id = f"msg_{int(datetime.now().timestamp())}"
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class ChatResponse:
    content: str
    task_id: Optional[str] = None
    metadata: Optional[dict] = None
    message_id: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class MarketingTask:
    id: str
    title: str
    description: str
    required_inputs: List[str]
    example_outputs: List[str] 