"""
Models Package
Contains data models for the MiniMe application.
"""

from .chat import ChatMessage, ChatHistory, MarketingTask, TaskProgress

__all__ = [
    'ChatMessage',
    'ChatHistory',
    'MarketingTask',
    'TaskProgress'
] 