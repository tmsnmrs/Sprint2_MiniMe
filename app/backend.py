import os
import openai
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.types import ChatMessage, MarketingTask, ChatResponse
from app.handlers.task_handlers import get_task, get_task_prompt, get_task_handler, BaseTaskHandler

class ChatManager:
    """Manages chat interactions and responses"""
    
    def __init__(self):
        self.conversation_history: List[ChatMessage] = []
        self.current_task: Optional[str] = None
        self.current_handler: Optional[BaseTaskHandler] = None
        self.context_window_size: int = 10
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        openai.api_key = api_key

    def get_response(self, message: str, task_id: Optional[str] = None) -> ChatResponse:
        """Process a message and return a response"""
        try:
            # Create user message with metadata
            user_message = ChatMessage(
                role="user",
                content=message,
                task_id=task_id or self.current_task
            )
            self.add_to_history(user_message)

            # Handle task selection
            if task_id:
                return self._handle_task_selection(task_id)

            # Handle task-specific interaction
            if self.current_task and self.current_handler:
                return self._handle_task_interaction(message)

            # Handle general conversation
            return self._handle_general_conversation(message)

        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            error_message = "I encountered an error. Please try again or select a different task."
            error_chat_message = ChatMessage(
                role="assistant",
                content=error_message,
                task_id=self.current_task
            )
            self.add_to_history(error_chat_message)
            return ChatResponse(
                content=error_message,
                task_id=self.current_task,
                message_id=error_chat_message.message_id,
                timestamp=error_chat_message.timestamp
            )

    def _handle_task_selection(self, task_id: str) -> ChatResponse:
        """Handle selection of a new task"""
        self.current_task = task_id
        task = get_task(task_id)
        
        if not task:
            return ChatResponse(
                content="I couldn't find information about this task. Please try another one.",
                task_id=task_id
            )

        # Initialize task handler
        self.current_handler = get_task_handler(task_id, task)
        
        # Get first step
        first_step = self.current_handler.start()
        response_content = (
            f"I'll help you with {task.title}. {task.description}\n\n"
            f"Let's get started! {first_step.prompt}"
        )
        
        assistant_message = ChatMessage(
            role="assistant",
            content=response_content,
            task_id=task_id
        )
        self.add_to_history(assistant_message)
        
        return ChatResponse(
            content=response_content,
            task_id=task_id,
            message_id=assistant_message.message_id,
            timestamp=assistant_message.timestamp
        )

    def _handle_task_interaction(self, message: str) -> ChatResponse:
        """Handle interaction within a task"""
        if not self.current_handler:
            return self._handle_general_conversation(message)

        # Process the input with the task handler
        result = self.current_handler.process_input(message)
        
        # Prepare response based on result
        if result["status"] == "in_progress":
            response_content = (
                f"Great! I've recorded your input.\n\n"
                f"Next, {result['message']}"
            )
        else:  # completed
            response_content = (
                f"Perfect! We've completed this task. Here's a summary:\n\n"
                f"{result['message']}\n\n"
                f"Would you like to start another task or discuss something specific about these results?"
            )
            # Reset handler but keep task context
            self.current_handler = None

        assistant_message = ChatMessage(
            role="assistant",
            content=response_content,
            task_id=self.current_task
        )
        self.add_to_history(assistant_message)
        
        return ChatResponse(
            content=response_content,
            task_id=self.current_task,
            message_id=assistant_message.message_id,
            timestamp=assistant_message.timestamp
        )

    def _handle_general_conversation(self, message: str) -> ChatResponse:
        """Handle general conversation outside of tasks"""
        if "help" in message.lower():
            response_content = "I can help you with various marketing tasks. Try selecting one of the tasks above to get started!"
        else:
            response_content = "I'm here to help with specific marketing tasks. Please select a task from above to get started!"

        assistant_message = ChatMessage(
            role="assistant",
            content=response_content,
            task_id=None
        )
        self.add_to_history(assistant_message)
        
        return ChatResponse(
            content=response_content,
            task_id=None,
            message_id=assistant_message.message_id,
            timestamp=assistant_message.timestamp
        )

    def add_to_history(self, message: ChatMessage) -> None:
        """Add a message to the conversation history"""
        self.conversation_history.append(message)

    def get_context_messages(self) -> List[ChatMessage]:
        """Get the most recent messages for context"""
        return self.conversation_history[-self.context_window_size:]

    def get_task_messages(self, task_id: str) -> List[ChatMessage]:
        """Get all messages related to a specific task"""
        return [msg for msg in self.conversation_history if msg.task_id == task_id]

    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []
        self.current_task = None
        self.current_handler = None

    def get_current_task(self) -> Optional[str]:
        """Get the current task ID"""
        return self.current_task

    def set_current_task(self, task_id: Optional[str]) -> None:
        """Set the current task ID"""
        self.current_task = task_id
        self.current_handler = None  # Reset handler when changing tasks

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