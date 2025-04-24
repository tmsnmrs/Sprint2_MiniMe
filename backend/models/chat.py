from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field

class Message(BaseModel):
    """Base message model"""
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    role: Literal["user", "assistant"] = "user"
    
class ChatMessage(Message):
    """Extended message model with metadata"""
    message_id: str = Field(default_factory=lambda: f"msg_{int(datetime.now().timestamp())}")
    context_used: Optional[List[dict]] = None
    marketing_domain: Optional[str] = None
    
class ChatHistory(BaseModel):
    """Chat history model"""
    messages: List[ChatMessage] = []
    session_id: str = Field(default_factory=lambda: f"session_{int(datetime.now().timestamp())}")
    
    def add_message(self, message: ChatMessage) -> None:
        """Add a message to the chat history"""
        self.messages.append(message)
    
    def get_recent_messages(self, limit: int = 5) -> List[ChatMessage]:
        """Get the most recent messages"""
        return self.messages[-limit:]
    
    def get_context_window(self, max_tokens: int = 2000) -> List[ChatMessage]:
        """Get messages that fit within the token window"""
        # TODO: Implement token counting logic
        return self.get_recent_messages(5)
    
    def clear_history(self) -> None:
        """Clear the chat history"""
        self.messages = []

class MarketingTask(BaseModel):
    """Marketing task model"""
    task_type: str
    description: str
    required_inputs: List[str]
    example_outputs: List[str]
    
class TaskProgress(BaseModel):
    """Task progress tracking"""
    task: MarketingTask
    current_step: int
    total_steps: int
    completed_inputs: List[str] = []
    status: Literal["not_started", "in_progress", "completed"] = "not_started"
    
    def update_progress(self, step: int) -> None:
        """Update the current step"""
        self.current_step = step
        if step >= self.total_steps:
            self.status = "completed"
        elif step > 0:
            self.status = "in_progress"
            
    def add_input(self, input_value: str) -> None:
        """Add a completed input"""
        self.completed_inputs.append(input_value)
