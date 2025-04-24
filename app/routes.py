from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.models.chat import ChatMessage
from app.models.tasks import MarketingTask
from app.handlers.task_handlers import get_task, get_task_prompt
from app.backend import ChatManager

# Create router
router = APIRouter()

# Initialize chat manager
chat_manager = ChatManager()

@router.get("/tasks", response_model=List[MarketingTask])
async def get_tasks():
    """Get all available marketing tasks"""
    return list(get_task(task_id) for task_id in ["content-calendar", "email-campaign", "social-ad", "competitor-analysis"])

@router.get("/tasks/{task_id}", response_model=MarketingTask)
async def get_task_by_id(task_id: str):
    """Get a specific marketing task by ID"""
    try:
        return get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/chat", response_model=Dict[str, Any])
async def chat(message: ChatMessage):
    """Process a chat message and get AI response"""
    try:
        response = chat_manager.get_response(message.content)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 