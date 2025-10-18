from fastapi import APIRouter, HTTPException
from typing import List
import logging
import time
from app.models import (
    RecommendationRequest, 
    RecommendationResponse,
    ChatRequest,
    ChatResponse,
    ChatMessage,
    RecommendedProduct
)
from app.services.recommendation_service import recommendation_service
from app.services.genai_service import genai_service

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
logger = logging.getLogger(__name__)

@router.post("/search", response_model=RecommendationResponse)
async def search_products(request: RecommendationRequest):
    """
    Search for products based on query and get recommendations
    """
    try:
        start_time = time.time()
        
        # Get recommendations
        recommendations = recommendation_service.get_recommendations(
            query=request.query,
            top_k=request.top_k,
            include_description=request.include_description
        )
        
        processing_time = time.time() - start_time
        
        return RecommendationResponse(
            query=request.query,
            recommendations=recommendations,
            total_results=len(recommendations),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat_recommendations(request: ChatRequest):
    """
    Conversational interface for product recommendations
    """
    try:
        # Get recommendations
        recommendations = recommendation_service.get_recommendations(
            query=request.message,
            top_k=request.top_k,
            include_description=True
        )
        
        # Generate conversational response
        assistant_message = genai_service.generate_conversational_response(
            user_query=request.message,
            products=[rec.product for rec in recommendations]
        )
        
        # Update conversation history
        conversation_history = request.conversation_history.copy()
        conversation_history.append(ChatMessage(role="user", content=request.message))
        conversation_history.append(ChatMessage(role="assistant", content=assistant_message))
        
        return ChatResponse(
            message=assistant_message,
            recommendations=recommendations,
            conversation_history=conversation_history
        )
        
    except Exception as e:
        logger.error(f"Error in chat_recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar/{product_id}", response_model=List[RecommendedProduct])
async def get_similar_products(product_id: str, top_k: int = 5):
    """
    Get similar products based on a product ID
    """
    try:
        recommendations = recommendation_service.get_similar_products(
            product_id=product_id,
            top_k=top_k
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error in get_similar_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index")
async def index_products():
    """
    Manually trigger product indexing
    """
    try:
        recommendation_service.index_products()
        return {"message": "Products indexed successfully"}
    except Exception as e:
        logger.error(f"Error indexing products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))