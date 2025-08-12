"""
Market Price Agent - Fetches commodity prices from Agmarknet/eNAM API
Provides current mandi prices and market trends
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MarketPriceAgent:
    """
    Fetches market prices from Agmarknet/eNAM APIs and provides price trends
    """
    
    def __init__(self):
        # Mock price database - in production, use actual API calls
        self.price_database = {
            'wheat': {
                'states': {
                    'punjab': {'min': 2000, 'max': 2150, 'modal': 2100},
                    'haryana': {'min': 1980, 'max': 2120, 'modal': 2080},
                    'uttar pradesh': {'min': 1950, 'max': 2100, 'modal': 2050},
                    'madhya pradesh': {'min': 1920, 'max': 2080, 'modal': 2020}
                },
                'unit': 'per quintal',
                'grade': 'FAQ'
            },
            'rice': {
                'states': {
                    'punjab': {'min': 2800, 'max': 3000, 'modal': 2900},
                    'haryana': {'min': 2750, 'max': 2950, 'modal': 2850},
                    'west bengal': {'min': 2600, 'max': 2800, 'modal': 2700},
                    'andhra pradesh': {'min': 2500, 'max': 2700, 'modal': 2600}
                },
                'unit': 'per quintal',
                'grade': 'Common'
            },
            'cotton': {
                'states': {
                    'gujarat': {'min': 6500, 'max': 7200, 'modal': 6800},
                    'maharashtra': {'min': 6400, 'max': 7100, 'modal': 6750},
                    'andhra pradesh': {'min': 6300, 'max': 7000, 'modal': 6650},
                    'karnataka': {'min': 6200, 'max': 6900, 'modal': 6550}
                },
                'unit': 'per quintal',
                'grade': 'Medium'
            },
            'onion': {
                'states': {
                    'maharashtra': {'min': 1200, 'max': 1800, 'modal': 1500},
                    'karnataka': {'min': 1100, 'max': 1700, 'modal': 1400},
                    'gujarat': {'min': 1150, 'max': 1750, 'modal': 1450},
                    'andhra pradesh': {'min': 1000, 'max': 1600, 'modal': 1300}
                },
                'unit': 'per quintal',
                'grade': 'Medium'
            },
            'potato': {
                'states': {
                    'uttar pradesh': {'min': 800, 'max': 1200, 'modal': 1000},
                    'west bengal': {'min': 750, 'max': 1150, 'modal': 950},
                    'bihar': {'min': 700, 'max': 1100, 'modal': 900},
                    'gujarat': {'min': 850, 'max': 1250, 'modal': 1050}
                },
                'unit': 'per quintal',
                'grade': 'Medium'
            },
            'tomato': {
                'states': {
                    'karnataka': {'min': 500, 'max': 1500, 'modal': 1000},
                    'andhra pradesh': {'min': 400, 'max': 1400, 'modal': 900},
                    'maharashtra': {'min': 450, 'max': 1450, 'modal': 950},
                    'west bengal': {'min': 350, 'max': 1300, 'modal': 850}
                },
                'unit': 'per quintal',
                'grade': 'Medium'
            }
        }
        
        # MSP (Minimum Support Price) data for reference
        self.msp_data = {
            'wheat': 2125,
            'rice': 2040,  # Common variety
            'cotton': 6080,
            'sugarcane': 315,  # per quintal
            'maize': 1962
        }
    
    async def get_market_prices(self, context: Dict[str, Any]) -> 'QueryResponse':
        """
        Get market prices based on commodity and location
        """
        from main import QueryResponse, QueryCategory
        
        try:
            query = context.get('query', '').lower()
            location = context.get('location', '').lower() if context.get('location') else ''
            
            # Extract commodity name from query
            commodity = self.extract_commodity(query)
            
            if not commodity:
                return QueryResponse(
                    category=QueryCategory.MARKET_PRICE,
                    response="Please specify a commodity (wheat, rice, cotton, onion, potato, tomato) to get price information.",
                    language='en',
                    source="market_price_agent",
                    confidence=0.0
                )
            
            # Fetch price data
            price_data = await self.fetch_commodity_prices(commodity, location)
            
            if not price_data:
                return QueryResponse(
                    category=QueryCategory.MARKET_PRICE,
                    response=f"No reliable market price data found for {commodity}. Please check with your local mandi or try again later.",
                    language='en',
                    source="agmarknet_api",
                    confidence=0.0
                )
            
            # Format price information
            response = self.format_price_info(commodity, price_data, location)
            
            return QueryResponse(
                category=QueryCategory.MARKET_PRICE,
                response=response,
                language='en',
                source="agmarknet_api",
                confidence=0.8,
                data=price_data
            )
            
        except Exception as e:
            logger.error(f"Market price fetch error: {str(e)}")
            return QueryResponse(
                category=QueryCategory.MARKET_PRICE,
                response="Unable to fetch market prices at the moment. Please check with your local mandi for current rates.",
                language='en',
                source="market_agent_error",
                confidence=0.0
            )
    
    def extract_commodity(self, query: str) -> Optional[str]:
        """Extract commodity name from query"""
        commodities = list(self.price_database.keys())
        
        for commodity in commodities:
            if commodity in query:
                return commodity
        
        # Check for alternative names
        alternative_names = {
            'paddy': 'rice',
            'kapas': 'cotton',
            'aloo': 'potato',
            'pyaz': 'onion',
            'tamatar': 'tomato'
        }
        
        for alt_name, commodity in alternative_names.items():
            if alt_name in query:
                return commodity
        
        return None
    
    async def fetch_commodity_prices(self, commodity: str, location: str) -> Optional[Dict[str, Any]]:
        """
        Fetch commodity prices from API or database
        In production, this would call actual Agmarknet/eNAM APIs
        """
        try:
            if commodity not in self.price_database:
                return None
            
            commodity_data = self.price_database[commodity]
            
            # If location is specified, try to find state-specific prices
            if location:
                for state, prices in commodity_data['states'].items():
                    if state in location or location in state:
                        return {
                            'commodity': commodity,
                            'state': state.title(),
                            'prices': prices,
                            'unit': commodity_data['unit'],
                            'grade': commodity_data['grade'],
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'msp': self.msp_data.get(commodity)
                        }
            
            # Return average prices if no specific location found
            all_prices = list(commodity_data['states'].values())
            avg_prices = {
                'min': sum(p['min'] for p in all_prices) // len(all_prices),
                'max': sum(p['max'] for p in all_prices) // len(all_prices),
                'modal': sum(p['modal'] for p in all_prices) // len(all_prices)
            }
            
            return {
                'commodity': commodity,
                'state': 'National Average',
                'prices': avg_prices,
                'unit': commodity_data['unit'],
                'grade': commodity_data['grade'],
                'date': datetime.now().strftime('%Y-%m-%d'),
                'msp': self.msp_data.get(commodity)
            }
            
        except Exception as e:
            logger.error(f"Price fetch error: {str(e)}")
            return None
    
    def format_price_info(self, commodity: str, price_data: Dict[str, Any], location: str) -> str:
        """
        Format price information for farmer-friendly display
        """
        try:
            commodity_name = commodity.title()
            state = price_data['state']
            prices = price_data['prices']
            unit = price_data['unit']
            grade = price_data['grade']
            date = price_data['date']
            msp = price_data.get('msp')
            
            response = f"💰 {commodity_name} Market Prices - {state}\n"
            response += f"📅 Date: {date}\n\n"
            response += f"Grade: {grade}\n"
            response += f"Minimum Price: ₹{prices['min']} {unit}\n"
            response += f"Maximum Price: ₹{prices['max']} {unit}\n"
            response += f"Modal Price: ₹{prices['modal']} {unit}\n"
            
            # Add MSP comparison if available
            if msp:
                if prices['modal'] >= msp:
                    response += f"✅ MSP: ₹{msp} {unit} (Above MSP)\n"
                else:
                    response += f"⚠️ MSP: ₹{msp} {unit} (Below MSP)\n"
            
            # Add market advice
            response += self.get_market_advice(commodity, prices, msp)
            
            return response
            
        except Exception as e:
            logger.error(f"Price formatting error: {str(e)}")
            return f"Price data available for {commodity} but formatting failed."
    
    def get_market_advice(self, commodity: str, prices: Dict[str, Any], msp: Optional[int]) -> str:
        """
        Provide market advice based on current prices
        """
        advice = "\n\n📈 Market Advice:\n"
        
        modal_price = prices['modal']
        price_range = prices['max'] - prices['min']
        
        # Price volatility advice
        if price_range > (modal_price * 0.3):
            advice += "• High price volatility observed. Consider waiting for better rates.\n"
        else:
            advice += "• Stable price range. Good time for trading.\n"
        
        # MSP comparison advice
        if msp:
            if modal_price > msp * 1.1:  # 10% above MSP
                advice += f"• Excellent prices! Current rate is significantly above MSP.\n"
            elif modal_price >= msp:
                advice += f"• Good prices! Current rate is above or at MSP level.\n"
            else:
                advice += f"• Consider selling at government procurement centers for MSP.\n"
        
        # Seasonal advice
        current_month = datetime.now().month
        if commodity in ['wheat', 'rice'] and current_month in [3, 4, 5]:  # Harvest season
            advice += "• Harvest season - expect higher supply and competitive prices.\n"
        elif commodity in ['onion', 'potato'] and current_month in [11, 12, 1]:  # Peak demand
            advice += "• Peak demand season - good time to sell stored produce.\n"
        
        return advice

# Example usage
async def test_market_agent():
    """Test the market price agent"""
    agent = MarketPriceAgent()
    
    test_contexts = [
        {'query': 'wheat price today', 'location': 'Punjab'},
        {'query': 'cotton rate in Gujarat', 'location': 'Gujarat'},
        {'query': 'onion market price', 'location': 'Maharashtra'},
        {'query': 'rice price', 'location': None}
    ]
    
    for context in test_contexts:
        print(f"\nTesting: {context}")
        response = await agent.get_market_prices(context)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")

if __name__ == "__main__":
    asyncio.run(test_market_agent())
