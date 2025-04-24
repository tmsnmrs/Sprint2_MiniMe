from typing import List, Optional
import tiktoken
from langchain_openai import OpenAIEmbeddings
from .config import default_config

class EmbeddingHandler:
    """Handles text embedding operations"""
    
    def __init__(self, config=default_config):
        self.config = config
        self.embeddings = OpenAIEmbeddings(
            model=config.embedding_model,
            dimensions=config.embedding_dimension
        )
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string"""
        return len(self.tokenizer.encode(text))
    
    def chunk_text(self, text: str, metadata: Optional[dict] = None) -> List[dict]:
        """Split text into chunks with metadata"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.config.chunk_size - self.config.chunk_overlap):
            chunk_tokens = tokens[i:i + self.config.chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            
            chunk_data = {
                "text": chunk_text,
                "metadata": {
                    "chunk_index": len(chunks),
                    "token_count": len(chunk_tokens),
                    **(metadata or {})
                }
            }
            chunks.append(chunk_data)
        
        return chunks
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = await self.embeddings.aembed_documents(texts)
            return embeddings
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        return self.config.embedding_dimension
