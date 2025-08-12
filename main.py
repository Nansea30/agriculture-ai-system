#!/usr/bin/env python3
"""
Multi-Agent AI System for Agriculture Decision Support in India
Manager Agent - Orchestrates all sub-agents and API calls
"""

import json
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryCategory(Enum):
    TRANSLATION = "translation"
    WEATHER = "weather"
    CROP_RECOMMENDATION = "crop_recommendation"
    MARKET_PRICE = "market_price"
    IRRIGATION = "irrigation"
    PEST_DISEASE = "pest_disease"
    FINANCE_POLICY = "finance_policy"
    UNKNOWN = "unknown"

@dataclass
class QueryResponse:
    """Standard response format for all agents"""
    category: QueryCategory
    response: str
    language: str
    source: str
    confidence: float
    data: Optional[Dict[str, Any]] = None

class ManagerAgent:
    """
    Main Manager Agent that coordinates all sub-agents
    """
    
    def __init__(self):
        self.agents = {}
        self.initialize_agents()
    
    def initialize_agents(self):
        """Initialize all sub-agents"""
        from agents.translation_agent import TranslationAgent
        from agents.classifier_agent import QueryClassifierAgent
        from agents.weather_agent import WeatherDataAgent
        from agents.crop_agent import CropRecommendationAgent
        from agents.market_agent import MarketPriceAgent
        from agents.irrigation_agent import IrrigationWeatherRiskAgent
        from agents.finance_agent import FinancePolicyAgent
        from agents.pest_agent import PestDiseaseAgent
        
        self.agents = {
            'translation': TranslationAgent(),
            'classifier': QueryClassifierAgent(),
            'weather': WeatherDataAgent(),
            'crop': CropRecommendationAgent(),
            'market': MarketPriceAgent(),
            'irrigation': IrrigationWeatherRiskAgent(),
            'finance': FinancePolicyAgent(),
            'pest': PestDiseaseAgent()
        }
    
    async def process_query(self, query: str, location: Optional[str] = None) -> QueryResponse:
        """
        Main entry point for processing farmer queries
        """
        try:
            # Step 1: Detect language and translate if needed
            translation_result = await self.agents['translation'].process(query)
            original_language = translation_result.get('language', 'en')
            english_query = translation_result.get('translated_query', query)
            
            logger.info(f"Original language: {original_language}")
            logger.info(f"English query: {english_query}")
            
            # Step 2: Classify the query
            classification = await self.agents['classifier'].classify(english_query)
            category = QueryCategory(classification.get('category', 'unknown'))
            
            logger.info(f"Query classified as: {category.value}")
            
            # Step 3: Route to appropriate agent
            response = await self.route_to_agent(category, english_query, location)
            
            # Step 4: Translate response back to original language if needed
            if original_language != 'en':
                translated_response = await self.agents['translation'].translate_response(
                    response.response, original_language
                )
                response.response = translated_response
            
            response.language = original_language
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return QueryResponse(
                category=QueryCategory.UNKNOWN,
                response="I apologize, but I encountered an error processing your query. Please try again or contact your local agriculture officer.",
                language=original_language if 'original_language' in locals() else 'en',
                source="system_error",
                confidence=0.0
            )
    
    async def route_to_agent(self, category: QueryCategory, query: str, location: Optional[str]) -> QueryResponse:
        """
        Route query to the appropriate sub-agent
        """
        context = {'query': query, 'location': location}
        
        if category == QueryCategory.WEATHER:
            return await self.agents['weather'].get_weather_info(context)
        
        elif category == QueryCategory.CROP_RECOMMENDATION:
            return await self.agents['crop'].recommend_crops(context)
        
        elif category == QueryCategory.MARKET_PRICE:
            return await self.agents['market'].get_market_prices(context)
        
        elif category == QueryCategory.IRRIGATION:
            return await self.agents['irrigation'].get_irrigation_advice(context)
        
        elif category == QueryCategory.PEST_DISEASE:
            return await self.agents['pest'].diagnose_pest_disease(context)
        
        elif category == QueryCategory.FINANCE_POLICY:
            return await self.agents['finance'].get_policy_info(context)
        
        else:
            return QueryResponse(
                category=QueryCategory.UNKNOWN,
                response="I'm not sure how to help with that query. Please rephrase your question or contact your local agriculture officer for assistance.",
                language='en',
                source="manager_agent",
                confidence=0.0
            )
    
    def format_response(self, response: QueryResponse) -> str:
        """
        Format response for display to farmer
        """
        formatted = f"{response.response}\n\n"
        
        if response.source != "system_error":
            formatted += f"📊 Source: {response.source}\n"
        
        if response.confidence < 0.7:
            formatted += "⚠️ For more accurate information, please consult your local agriculture officer.\n"
        
        return formatted

# Example usage and testing
async def main():
    """Test the manager agent with sample queries"""
    manager = ManagerAgent()
    
    # Test queries in different languages
    test_queries = [
        ("What is the weather forecast for Delhi?", "Delhi"),
        ("मेरे टमाटर के पौधे में पीली पत्तियां हैं, क्या करूं?", "Mumbai"),
        ("Cotton price today in Maharashtra", "Maharashtra"),
        ("When to irrigate wheat crop?", None),
        ("PM Kisan scheme eligibility", None)
    ]
    
    for query, location in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"Location: {location}")
        print(f"{'='*50}")
        
        response = await manager.process_query(query, location)
        formatted_response = manager.format_response(response)
        print(formatted_response)

if __name__ == "__main__":
    asyncio.run(main())
