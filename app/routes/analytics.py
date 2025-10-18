from fastapi import APIRouter, HTTPException
import logging
import pandas as pd
from collections import Counter
from app.models import AnalyticsResponse
from app.utils.data_loader import data_loader
import re

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)

def extract_price_value(price_str: str) -> float:
    """Extract numeric value from price string"""
    if not price_str or price_str == "":
        return 0.0
    try:
        # Remove $ and commas, then convert to float
        numeric_str = re.sub(r'[^\d.]', '', str(price_str))
        return float(numeric_str) if numeric_str else 0.0
    except:
        return 0.0

@router.get("/", response_model=AnalyticsResponse)
async def get_analytics():
    """
    Get comprehensive analytics about the product dataset
    """
    try:
        df = data_loader.get_dataframe()
        
        # Total products
        total_products = len(df)
        
        # Categories distribution
        all_categories = []
        for cats in df['categories']:
            if isinstance(cats, list):
                all_categories.extend(cats)
        categories_distribution = dict(Counter(all_categories).most_common(20))
        
        # Brand distribution
        brands = df['brand'].dropna()
        brand_distribution = dict(Counter(brands).most_common(20))
        
        # Price statistics
        df['price_numeric'] = df['price'].apply(extract_price_value)
        price_stats = {
            "min": float(df['price_numeric'][df['price_numeric'] > 0].min()) if len(df[df['price_numeric'] > 0]) > 0 else 0,
            "max": float(df['price_numeric'].max()),
            "mean": float(df['price_numeric'][df['price_numeric'] > 0].mean()) if len(df[df['price_numeric'] > 0]) > 0 else 0,
            "median": float(df['price_numeric'][df['price_numeric'] > 0].median()) if len(df[df['price_numeric'] > 0]) > 0 else 0
        }
        
        # Material distribution
        materials = df['material'].dropna()
        material_distribution = dict(Counter(materials).most_common(15))
        
        # Color distribution
        colors = df['color'].dropna()
        color_distribution = dict(Counter(colors).most_common(15))
        
        # Country distribution
        countries = df['country_of_origin'].dropna()
        country_distribution = dict(Counter(countries).most_common(10))
        
        # Top brands by product count
        top_brands = [
            {"brand": brand, "count": int(count)}
            for brand, count in Counter(brands).most_common(10)
        ]
        
        # Price ranges
        price_ranges = {
            "Under $25": int(len(df[(df['price_numeric'] > 0) & (df['price_numeric'] < 25)])),
            "$25-$50": int(len(df[(df['price_numeric'] >= 25) & (df['price_numeric'] < 50)])),
            "$50-$100": int(len(df[(df['price_numeric'] >= 50) & (df['price_numeric'] < 100)])),
            "$100-$200": int(len(df[(df['price_numeric'] >= 100) & (df['price_numeric'] < 200)])),
            "$200+": int(len(df[df['price_numeric'] >= 200]))
        }
        
        return AnalyticsResponse(
            total_products=total_products,
            categories_distribution=categories_distribution,
            brand_distribution=brand_distribution,
            price_statistics=price_stats,
            material_distribution=material_distribution,
            color_distribution=color_distribution,
            country_distribution=country_distribution,
            top_brands=top_brands,
            price_ranges=price_ranges
        )
        
    except Exception as e:
        logger.error(f"Error in get_analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products")
async def get_all_products():
    """
    Get all products (for frontend display)
    """
    try:
        products = data_loader.get_products()
        return {"products": products, "total": len(products)}
    except Exception as e:
        logger.error(f"Error in get_all_products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))