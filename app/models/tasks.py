from pydantic import BaseModel
from typing import List

class MarketingTask(BaseModel):
    """Model for marketing tasks"""
    id: str
    title: str
    description: str
    required_inputs: List[str]
    example_outputs: List[str] 