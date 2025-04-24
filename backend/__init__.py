"""
MiniMe Backend Package
This package contains the core functionality for the MiniMe marketing assistant.
"""

from .rag.config import RAGConfig, default_config
from .rag.embeddings import EmbeddingHandler
from .rag.vectorstore import VectorStore
from .models.chat import ChatMessage, ChatHistory, MarketingTask, TaskProgress
from .functions.chat_manager import ChatManager

__all__ = [
    'RAGConfig',
    'default_config',
    'EmbeddingHandler',
    'VectorStore',
    'ChatMessage',
    'ChatHistory',
    'MarketingTask',
    'TaskProgress',
    'ChatManager'
] 