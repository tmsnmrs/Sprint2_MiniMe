from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class MarketingTask:
    id: str
    title: str
    description: str
    required_inputs: List[str]
    example_outputs: List[str]

@dataclass
class ChatResponse:
    content: str 