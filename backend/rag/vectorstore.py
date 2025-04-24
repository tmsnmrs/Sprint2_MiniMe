from typing import List, Dict, Any
import pinecone
from config.settings import PINECONE_API_KEY, PINECONE_ENVIRONMENT
from .config import default_config
from .embeddings import EmbeddingHandler

class VectorStore:
    """Handles vector storage and retrieval operations"""
    
    def __init__(self, config=default_config):
        self.config = config
        self.embedding_handler = EmbeddingHandler(config)
        
        # Initialize Pinecone
        pinecone.init(
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENVIRONMENT
        )
        
        # Create index if it doesn't exist
        if self.config.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.config.index_name,
                dimension=self.config.embedding_dimension,
                metric="cosine"
            )
        
        self.index = pinecone.Index(self.config.index_name)
    
    async def store_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Store documents in the vector store"""
        try:
            # Process documents in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                
                # Generate embeddings for the batch
                texts = [doc["text"] for doc in batch]
                embeddings = await self.embedding_handler.generate_embeddings(texts)
                
                # Prepare vectors for upsert
                vectors = []
                for j, (doc, embedding) in enumerate(zip(batch, embeddings)):
                    vector_id = f"{doc['metadata'].get('domain', 'general')}_{i + j}"
                    vectors.append((vector_id, embedding, doc['metadata']))
                
                # Upsert to Pinecone
                self.index.upsert(vectors=vectors, namespace=self.config.namespace)
        
        except Exception as e:
            raise Exception(f"Error storing documents: {str(e)}")
    
    async def similarity_search(
        self,
        query: str,
        filter: Dict[str, Any] = None,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            # Generate query embedding
            query_embedding = await self.embedding_handler.generate_embeddings([query])
            
            # Perform similarity search
            results = self.index.query(
                vector=query_embedding[0],
                namespace=self.config.namespace,
                top_k=top_k or self.config.top_k,
                filter=filter,
                include_metadata=True
            )
            
            # Filter results by similarity threshold
            filtered_results = [
                match for match in results.matches
                if match.score >= self.config.similarity_threshold
            ]
            
            return filtered_results
        
        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")
    
    def delete_documents(self, filter: Dict[str, Any] = None) -> None:
        """Delete documents from the vector store"""
        try:
            if filter:
                self.index.delete(
                    filter=filter,
                    namespace=self.config.namespace
                )
            else:
                self.index.delete(
                    delete_all=True,
                    namespace=self.config.namespace
                )
        except Exception as e:
            raise Exception(f"Error deleting documents: {str(e)}")
