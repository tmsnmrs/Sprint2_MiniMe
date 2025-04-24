from typing import Dict, List
from pydantic import BaseModel

class RAGConfig(BaseModel):
    """Configuration for the RAG system"""
    # Embedding configuration
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    
    # Chunking configuration
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # Retrieval configuration
    top_k: int = 3
    similarity_threshold: float = 0.7
    
    # Vector store configuration
    index_name: str = "minime-marketing"
    namespace: str = "marketing-knowledge"
    
    # Marketing domains for knowledge organization
    marketing_domains: List[str] = [
        "brand-analysis",
        "target-audience",
        "product-benefits",
        "value-proposition",
        "product-positioning",
        "messaging",
        "brand-archetype",
        "creative-strategy",
        "copywriting"
    ]
    
    # Domain descriptions for context
    domain_descriptions: Dict[str, str] = {
        "brand-analysis": "Product and brand analysis methodology",
        "target-audience": "Customer segmentation and audience analysis",
        "product-benefits": "Product feature and benefit analysis",
        "value-proposition": "Value proposition development",
        "product-positioning": "Market positioning strategies",
        "messaging": "Product messaging and communication",
        "brand-archetype": "Brand personality and archetype selection",
        "creative-strategy": "Creative marketing strategy development",
        "copywriting": "Marketing content creation and copywriting"
    }

# Create default configuration instance
default_config = RAGConfig() 