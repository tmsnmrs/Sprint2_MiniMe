from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from app.types import MarketingTask

@dataclass
class TaskStep:
    """Represents a single step in a task workflow"""
    step_id: str
    prompt: str
    required_input: List[str]
    validation_rules: Optional[Dict[str, Any]] = None
    next_step: Optional[str] = None

class BaseTaskHandler:
    """Base class for all task handlers"""
    def __init__(self, task: MarketingTask):
        self.task = task
        self.steps: Dict[str, TaskStep] = {}
        self.current_step: Optional[str] = None
        self.completed_steps: List[str] = []
        self.user_inputs: Dict[str, Any] = {}
        
    def start(self) -> TaskStep:
        """Start the task workflow"""
        if not self.steps:
            raise ValueError("No steps defined for this task")
        self.current_step = next(iter(self.steps))  # Get first step
        return self.steps[self.current_step]
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input for the current step"""
        if not self.current_step:
            raise ValueError("No active step")
            
        step = self.steps[self.current_step]
        
        # Store the input
        self.user_inputs[self.current_step] = user_input
        
        # Validate input if rules exist
        if step.validation_rules:
            # TODO: Implement validation
            pass
        
        # Mark step as completed
        self.completed_steps.append(self.current_step)
        
        # Move to next step if exists
        if step.next_step:
            self.current_step = step.next_step
            next_step = self.steps[step.next_step]
            return {
                "status": "in_progress",
                "next_step": next_step,
                "message": next_step.prompt
            }
        
        # Task completed
        return {
            "status": "completed",
            "message": "Task completed successfully!",
            "results": self.user_inputs
        }
    
    def get_current_step(self) -> Optional[TaskStep]:
        """Get the current step"""
        return self.steps.get(self.current_step) if self.current_step else None
    
    def get_progress(self) -> Dict[str, Any]:
        """Get task progress"""
        total_steps = len(self.steps)
        completed = len(self.completed_steps)
        return {
            "total_steps": total_steps,
            "completed_steps": completed,
            "progress_percentage": (completed / total_steps) * 100 if total_steps > 0 else 0,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps
        }

class ProductAnalysisHandler(BaseTaskHandler):
    """Handler for product analysis task"""
    def __init__(self, task: MarketingTask):
        super().__init__(task)
        self.steps = {
            "features": TaskStep(
                step_id="features",
                prompt="What are the main features of your product?",
                required_input=["features"],
                next_step="benefits"
            ),
            "benefits": TaskStep(
                step_id="benefits",
                prompt="What benefits do these features provide to your customers?",
                required_input=["benefits"],
                next_step="market_position"
            ),
            "market_position": TaskStep(
                step_id="market_position",
                prompt="Who are your main competitors and how does your product compare?",
                required_input=["competitors", "differentiators"],
                next_step="summary"
            ),
            "summary": TaskStep(
                step_id="summary",
                prompt="Let me summarize your product's unique value proposition.",
                required_input=[],
                next_step=None
            )
        }

class AudienceIdentificationHandler(BaseTaskHandler):
    """Handler for audience identification task"""
    def __init__(self, task: MarketingTask):
        super().__init__(task)
        self.steps = {
            "demographics": TaskStep(
                step_id="demographics",
                prompt="What are the key demographics of your target audience?",
                required_input=["age_range", "location", "income_level"],
                next_step="psychographics"
            ),
            "psychographics": TaskStep(
                step_id="psychographics",
                prompt="What are their interests, values, and pain points?",
                required_input=["interests", "values", "pain_points"],
                next_step="behavior"
            ),
            "behavior": TaskStep(
                step_id="behavior",
                prompt="How do they typically make purchasing decisions?",
                required_input=["buying_habits", "decision_factors"],
                next_step="summary"
            ),
            "summary": TaskStep(
                step_id="summary",
                prompt="Let me create a comprehensive audience profile based on your inputs.",
                required_input=[],
                next_step=None
            )
        }

# Task registry
TASK_HANDLERS = {
    "analyze-product": ProductAnalysisHandler,
    "identify-audience": AudienceIdentificationHandler,
    # Add more handlers as needed
}

def get_task_handler(task_id: str, task: MarketingTask) -> BaseTaskHandler:
    """Get the appropriate handler for a task"""
    handler_class = TASK_HANDLERS.get(task_id)
    if not handler_class:
        raise ValueError(f"No handler found for task: {task_id}")
    return handler_class(task)

# Existing functions
def get_task(task_id: str) -> Optional[MarketingTask]:
    """Get a task by ID"""
    # TODO: Replace with actual task definitions
    tasks = {
        "analyze-product": MarketingTask(
            id="analyze-product",
            title="Analyze my product",
            description="Understand your product's unique features and market position.",
            required_inputs=["features", "benefits", "competitors"],
            example_outputs=["unique value proposition", "market positioning statement"]
        ),
        "identify-audience": MarketingTask(
            id="identify-audience",
            title="Identify target audiences",
            description="Define and understand your ideal customer segments.",
            required_inputs=["demographics", "psychographics", "behavior"],
            example_outputs=["audience profile", "customer persona"]
        )
    }
    return tasks.get(task_id)

def get_task_prompt(task: MarketingTask) -> str:
    """Get the system prompt for a task"""
    return f"""You are helping with the task: {task.title}
    
Description: {task.description}
Required inputs: {', '.join(task.required_inputs)}
Expected outputs: {', '.join(task.example_outputs)}

Please guide the user through this task step by step, asking for necessary information
and providing insights along the way. Be specific and actionable in your guidance.""" 