from pinecone import Pinecone, ServerlessSpec
from app.config import settings
import logging
from typing import List, Dict, Any
import time

logger = logging.getLogger(__name__)

class VectorDatabase:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.index = None
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize or connect to Pinecone index"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            index_names = [idx.name for idx in existing_indexes]
            
            if self.index_name not in index_names:
                logger.info(f"Creating new index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=settings.PINECONE_DIMENSION,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=settings.PINECONE_ENVIRONMENT.split('-')[0] + "-" + 
                               settings.PINECONE_ENVIRONMENT.split('-')[1] + "-" +
                               settings.PINECONE_ENVIRONMENT.split('-')[2]
                    )
                )
                # Wait for index to be ready
                time.sleep(5)
            
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone index: {str(e)}")
            raise
    
    def upsert_vectors(self, vectors: List[tuple]):
        """
        Upsert vectors to Pinecone
        vectors: List of tuples (id, embedding, metadata)
        """
        try:
            self.index.upsert(vectors=vectors)
            logger.info(f"Upserted {len(vectors)} vectors")
        except Exception as e:
            logger.error(f"Error upserting vectors: {str(e)}")
            raise
    
    def query_vectors(self, query_vector: List[float], top_k: int = 5, 
                     filter_dict: Dict = None) -> List[Dict[str, Any]]:
        """Query similar vectors from Pinecone"""
        try:
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            return results.matches
        except Exception as e:
            logger.error(f"Error querying vectors: {str(e)}")
            raise
    
    def delete_all(self):
        """Delete all vectors from index"""
        try:
            self.index.delete(delete_all=True)
            logger.info("Deleted all vectors from index")
        except Exception as e:
            logger.error(f"Error deleting vectors: {str(e)}")
            raise
    
    def get_stats(self):
        """Get index statistics"""
        try:
            return self.index.describe_index_stats()
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            raise

# Global instance
vector_db = VectorDatabase()