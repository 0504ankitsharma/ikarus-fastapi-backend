import google.generativeai as genai
from typing import List, Optional
import logging
from app.config import settings
from app.models import Product, GeneratedDescription
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

class GenAIService:
    def __init__(self):
        self.model = None
        self.langchain_model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Gemini API"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            
            # Initialize LangChain model
            self.langchain_model = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.7
            )
            
            logger.info("GenAI service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing GenAI: {str(e)}")
            raise
    
    def generate_product_description(self, product: Product) -> GeneratedDescription:
        """Generate creative description for a product"""
        try:
            prompt = f"""Generate a creative, engaging, and informative product description for the following furniture item:

Title: {product.title}
Brand: {product.brand or 'Unknown'}
Original Description: {product.description or 'No description available'}
Material: {product.material or 'Not specified'}
Color: {product.color or 'Not specified'}
Categories: {', '.join(product.categories) if product.categories else 'General furniture'}

Create a compelling 2-3 sentence description that highlights the product's key features, style, and benefits. Make it appealing to potential buyers."""

            response = self.model.generate_content(prompt)
            
            return GeneratedDescription(
                original=product.description,
                generated=response.text
            )
        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            # Return original description on error
            return GeneratedDescription(
                original=product.description,
                generated=product.description or "A quality furniture product."
            )
    
    def generate_conversational_response(self, user_query: str, 
                                        products: List[Product]) -> str:
        """Generate conversational response about recommended products"""
        try:
            product_summaries = []
            for i, product in enumerate(products[:5], 1):
                summary = f"{i}. {product.title}"
                if product.brand:
                    summary += f" by {product.brand}"
                if product.price:
                    summary += f" - {product.price}"
                product_summaries.append(summary)
            
            prompt = f"""You are a helpful furniture shopping assistant. A customer asked: "{user_query}"

Based on their query, here are the top recommended products:
{chr(10).join(product_summaries)}

Provide a friendly, conversational response (2-3 sentences) that:
1. Acknowledges their request
2. Briefly highlights why these recommendations match their needs
3. Encourages them to explore the options

Keep it natural and helpful."""

            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating conversational response: {str(e)}")
            return f"I found {len(products)} great options for you based on your search for '{user_query}'. Check out the recommendations below!"
    
    def enhance_query(self, query: str) -> str:
        """Enhance user query for better search results"""
        try:
            prompt = f"""Given this furniture shopping query: "{query}"

Extract and list the key search terms and concepts that would help find relevant furniture products. 
Focus on: product types, styles, materials, colors, rooms, and features.
Return only the enhanced search terms as a single line, comma-separated."""

            response = self.model.generate_content(prompt)
            enhanced = response.text.strip()
            
            # Fallback to original if enhancement fails
            return enhanced if enhanced and len(enhanced) > 0 else query
            
        except Exception as e:
            logger.error(f"Error enhancing query: {str(e)}")
            return query

# Global instance
genai_service = GenAIService()