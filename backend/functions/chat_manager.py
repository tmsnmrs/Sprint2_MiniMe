from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from ..models.chat import ChatMessage, ChatHistory, MarketingTask, TaskProgress
from ..rag.vectorstore import VectorStore
from ..rag.config import default_config

class ChatManager:
    """Manages chat interactions and task execution"""
    
    def __init__(self, config=default_config):
        self.config = config
        self.vector_store = VectorStore(config)
        self.chat_model = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7
        )
        self.chat_history = ChatHistory()
        self.current_task: Optional[TaskProgress] = None
        
    async def process_message(self, message: str, marketing_domain: Optional[str] = None) -> ChatMessage:
        """Process a user message and generate a response"""
        try:
            # Create user message
            user_message = ChatMessage(
                content=message,
                role="user",
                marketing_domain=marketing_domain
            )
            self.chat_history.add_message(user_message)
            
            # Get relevant context from vector store
            context = await self._get_relevant_context(message, marketing_domain)
            
            # Generate response
            response = await self._generate_response(message, context)
            
            # Create assistant message
            assistant_message = ChatMessage(
                content=response,
                role="assistant",
                marketing_domain=marketing_domain,
                context_used=context
            )
            self.chat_history.add_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            error_message = ChatMessage(
                content=f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                role="assistant"
            )
            self.chat_history.add_message(error_message)
            return error_message
    
    async def _get_relevant_context(
        self,
        query: str,
        marketing_domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant context from the vector store"""
        filter_dict = {"domain": marketing_domain} if marketing_domain else None
        results = await self.vector_store.similarity_search(
            query=query,
            filter=filter_dict
        )
        return results
    
    async def _generate_response(
        self,
        message: str,
        context: List[Dict[str, Any]]
    ) -> str:
        """Generate a response using the chat model"""
        # Prepare context string
        context_str = "\n".join([
            f"Context {i+1}:\n{result.metadata.get('text', '')}"
            for i, result in enumerate(context)
        ])
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are MiniMe, a specialized marketing assistant. 
            Use the following context to provide helpful, accurate responses.
            If the context doesn't contain enough information, use your general knowledge
            but prioritize the context when available.
            
            Context:
            {context}
            """),
            ("user", "{message}")
        ])
        
        # Generate response
        chain = prompt | self.chat_model
        response = await chain.ainvoke({
            "context": context_str,
            "message": message
        })
        
        return response.content
    
    def start_task(self, task: MarketingTask) -> TaskProgress:
        """Start a new marketing task"""
        self.current_task = TaskProgress(
            task=task,
            current_step=0,
            total_steps=len(task.required_inputs)
        )
        return self.current_task
    
    def update_task_progress(self, step: int, input_value: Optional[str] = None) -> TaskProgress:
        """Update the progress of the current task"""
        if not self.current_task:
            raise ValueError("No task currently in progress")
            
        if input_value:
            self.current_task.add_input(input_value)
            
        self.current_task.update_progress(step)
        return self.current_task
    
    def get_chat_history(self, limit: Optional[int] = None) -> List[ChatMessage]:
        """Get the chat history"""
        if limit:
            return self.chat_history.get_recent_messages(limit)
        return self.chat_history.messages
    
    def clear_chat_history(self) -> None:
        """Clear the chat history"""
        self.chat_history.clear_history()
        self.current_task = None
