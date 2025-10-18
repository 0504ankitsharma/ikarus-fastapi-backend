from sentence_transformers import SentenceTransformer
from typing import List, Dict
import logging
import numpy as np
from app.config import settings
from app.models import Product

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load sentence transformer model"""
        try:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            raise
    
    def create_product_text(self, product: Product) -> str:
        """Create a text representation of product for embedding"""
        parts = []
        
        if product.title:
            parts.append(f"Title: {product.title}")
        
        if product.brand:
            parts.append(f"Brand: {product.brand}")
        
        if product.description:
            parts.append(f"Description: {product.description}")
        
        if product.categories:
            parts.append(f"Categories: {', '.join(product.categories)}")
        
        if product.material:
            parts.append(f"Material: {product.material}")
        
        if product.color:
            parts.append(f"Color: {product.color}")
        
        return " | ".join(parts)
    
    def encode_text(self, text: str) -> List[float]:
        """Encode text to embedding vector"""
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            # Ensure dimension matches Pinecone settings
            if len(embedding) < settings.PINECONE_DIMENSION:
                # Pad with zeros
                padding = np.zeros(settings.PINECONE_DIMENSION - len(embedding))
                embedding = np.concatenate([embedding, padding])
            elif len(embedding) > settings.PINECONE_DIMENSION:
                # Truncate
                embedding = embedding[:settings.PINECONE_DIMENSION]
            
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error encoding text: {str(e)}")
            raise
    
    def encode_product(self, product: Product) -> List[float]:
        """Encode product to embedding vector"""
        product_text = self.create_product_text(product)
        return self.encode_text(product_text)
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Encode multiple texts to embeddings"""
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            
            # Adjust dimensions
            adjusted_embeddings = []
            for embedding in embeddings:
                if len(embedding) < settings.PINECONE_DIMENSION:
                    padding = np.zeros(settings.PINECONE_DIMENSION - len(embedding))
                    embedding = np.concatenate([embedding, padding])
                elif len(embedding) > settings.PINECONE_DIMENSION:
                    embedding = embedding[:settings.PINECONE_DIMENSION]
                adjusted_embeddings.append(embedding.tolist())
            
            return adjusted_embeddings
        except Exception as e:
            logger.error(f"Error encoding batch: {str(e)}")
            raise

# Global instance
embedding_service = EmbeddingService()