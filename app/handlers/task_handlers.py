from typing import Dict, Optional
from app.types import MarketingTask

# Marketing task definitions
MARKETING_TASKS: Dict[str, MarketingTask] = {
    "content_calendar": MarketingTask(
        id="content_calendar",
        title="Create Content Calendar",
        description="Plan and organize your content strategy with a detailed calendar",
        required_inputs=["Target audience", "Content goals", "Platforms"],
        example_outputs=["Monthly content calendar", "Content themes", "Posting schedule"]
    ),
    "email_campaign": MarketingTask(
        id="email_campaign",
        title="Design Email Campaign",
        description="Create an effective email marketing campaign",
        required_inputs=["Campaign goal", "Target audience", "Key message"],
        example_outputs=["Email sequence", "Subject lines", "Call-to-action"]
    ),
    "social_media_ad": MarketingTask(
        id="social_media_ad",
        title="Create Social Media Ad",
        description="Design engaging social media advertisements",
        required_inputs=["Platform", "Target audience", "Campaign objective"],
        example_outputs=["Ad copy", "Visual guidelines", "Targeting strategy"]
    ),
    "competitor_analysis": MarketingTask(
        id="competitor_analysis",
        title="Competitor Analysis",
        description="Analyze competitors' marketing strategies",
        required_inputs=["Competitor names", "Analysis focus", "Time period"],
        example_outputs=["SWOT analysis", "Competitive advantages", "Market positioning"]
    )
}

def get_task(task_id: str) -> Optional[MarketingTask]:
    """Get a marketing task by ID"""
    return MARKETING_TASKS.get(task_id)

def get_task_prompt(task: MarketingTask) -> str:
    """Generate a prompt for a specific marketing task"""
    return f"""
    Task: {task.title}
    Description: {task.description}
    
    Required Inputs:
    {', '.join(task.required_inputs)}
    
    Example Outputs:
    {', '.join(task.example_outputs)}
    """ 