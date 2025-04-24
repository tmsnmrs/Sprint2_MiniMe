import os
import openai
from typing import List, Optional
from app.types import ChatMessage, MarketingTask, ChatResponse
from app.handlers.task_handlers import get_task, get_task_prompt

class ChatManager:
    """Manages chat interactions and responses"""
    
    def __init__(self):
        self.conversation_history: List[dict] = []
        self.current_task: Optional[str] = None
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_response(self, message: str, task_id: Optional[str] = None) -> dict:
        """Process a message and return a response"""
        # Update current task if provided
        if task_id:
            self.current_task = task_id

        # Add message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        try:
            # If we have a current task, get task-specific response
            if self.current_task:
                task = get_task(self.current_task)
                if task:
                    # Get task-specific prompt
                    task_prompt = get_task_prompt(self.current_task)
                    
                    # Prepare messages for the API call
                    messages = [
                        {"role": "system", "content": task_prompt},
                        *self.conversation_history[-3:]  # Include last 3 messages for context
                    ]
                    
                    # Get response from OpenAI
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    response_content = response.choices[0].message.content
                else:
                    response_content = "I couldn't find information about this task. Please try another one."
            else:
                # Handle general conversation
                if "help" in message.lower():
                    response_content = "I can help you with various marketing tasks. Try selecting one of the tasks above to get started!"
                else:
                    response_content = "I'm here to help with specific marketing tasks. Please select a task from above to get started!"

            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_content
            })

            return {"content": response_content}

        except Exception as e:
            error_message = f"I encountered an error: {str(e)}. Please try again or select a different task."
            return {"content": error_message}
    
    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []

    async def get_response_from_ai(self, user_message: str) -> str:
        """Get a response from the AI for a user message"""
        # Check if the message is a task selection
        if user_message.startswith("/task "):
            task_id = user_message[6:].strip()
            try:
                task = get_task(task_id)
                self.current_task = task
                return get_task_prompt(task)
            except ValueError as e:
                return str(e)

        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            *[{"role": m.role, "content": m.content} for m in self.conversation_history],
            {"role": "user", "content": user_message}
        ]

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_system_prompt(self) -> str:
        """Get the system prompt based on the current context"""
        base_prompt = """You are a knowledgeable and helpful marketing assistant. 
        Your goal is to help users develop effective marketing strategies and content.
        Be specific, practical, and provide actionable advice."""

        if self.current_task:
            task_context = f"""
            Currently working on: {self.current_task.description}
            Required inputs: {', '.join(self.current_task.required_inputs)}
            Expected outputs: {', '.join(self.current_task.example_outputs)}
            Please guide the user through this task step by step.
            """
            return base_prompt + task_context

        return base_prompt 