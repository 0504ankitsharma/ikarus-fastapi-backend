from typing import List, Dict, Optional
import logging
from app.models import Product, RecommendedProduct, GeneratedDescription
from app.services.embedding_service import embedding_service
from app.services.genai_service import genai_service
from app.database import vector_db
from app.utils.data_loader import data_loader

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.products_indexed = False
    
    def index_products(self):
        """Index all products in vector database"""
        try:
            if self.products_indexed:
                logger.info("Products already indexed")
                return
            
            logger.info("Starting product indexing...")
            products = data_loader.get_products()
            
            vectors = []
            for product in products:
                try:
                    # Create embedding
                    embedding = embedding_service.encode_product(product)
                    
                    # Prepare metadata
                    metadata = {
                        "uniq_id": product.uniq_id,
                        "title": product.title,
                        "brand": product.brand or "",
                        "price": product.price or "",
                        "categories": ",".join(product.categories) if product.categories else "",
                        "material": product.material or "",
                        "color": product.color or ""
                    }
                    
                    vectors.append((product.uniq_id, embedding, metadata))
                    
                except Exception as e:
                    logger.error(f"Error processing product {product.uniq_id}: {str(e)}")
                    continue
            
            # Batch upsert to Pinecone
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                vector_db.upsert_vectors(batch)
                logger.info(f"Indexed {i + len(batch)}/{len(vectors)} products")
            
            self.products_indexed = True
            logger.info(f"Successfully indexed {len(vectors)} products")
            
        except Exception as e:
            logger.error(f"Error indexing products: {str(e)}")
            raise
    
    def get_recommendations(self, query: str, top_k: int = 5, 
                          include_description: bool = True) -> List[RecommendedProduct]:
        """Get product recommendations based on query"""
        try:
            # Ensure products are indexed
            if not self.products_indexed:
                self.index_products()
            
            # Enhance query using GenAI
            enhanced_query = genai_service.enhance_query(query)
            logger.info(f"Enhanced query: {enhanced_query}")
            
            # Create query embedding
            query_embedding = embedding_service.encode_text(enhanced_query)
            
            # Search in vector database
            results = vector_db.query_vectors(query_embedding, top_k=top_k)
            
            # Convert results to RecommendedProduct
            recommendations = []
            for match in results:
                # Get full product details
                product = data_loader.get_product_by_id(match.id)
                
                if product:
                    # Generate description if requested
                    generated_desc = None
                    if include_description:
                        generated_desc = genai_service.generate_product_description(product)
                    
                    recommendations.append(RecommendedProduct(
                        product=product,
                        score=float(match.score),
                        generated_description=generated_desc
                    ))
            
            logger.info(f"Found {len(recommendations)} recommendations for query: {query}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            raise
    
    def get_similar_products(self, product_id: str, top_k: int = 5) -> List[RecommendedProduct]:
        """Get similar products based on a product ID"""
        try:
            # Get the product
            product = data_loader.get_product_by_id(product_id)
            if not product:
                logger.warning(f"Product not found: {product_id}")
                return []
            
            # Create embedding for the product
            product_embedding = embedding_service.encode_product(product)
            
            # Search for similar products
            results = vector_db.query_vectors(product_embedding, top_k=top_k + 1)
            
            # Convert results (skip the first one as it's the same product)
            recommendations = []
            for match in results[1:]:
                similar_product = data_loader.get_product_by_id(match.id)
                if similar_product:
                    recommendations.append(RecommendedProduct(
                        product=similar_product,
                        score=float(match.score),
                        generated_description=None
                    ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting similar products: {str(e)}")
            raise

# Global instance
recommendation_service = RecommendationService()