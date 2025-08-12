"""
Crop Recommendation Agent - Suggests suitable crops and seeds based on
soil type, weather conditions, season, and location
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class CropRecommendationAgent:
    """
    Recommends suitable crops based on environmental conditions and farmer input
    """
    
    def __init__(self):
        # Crop database with growing requirements
        self.crop_database = {
            'rice': {
                'seasons': ['kharif'],
                'soil_types': ['clay', 'loam'],
                'min_temp': 20,
                'max_temp': 35,
                'rainfall_mm': 150,
                'water_requirement': 'high',
                'duration_days': 120,
                'states': ['Punjab', 'Haryana', 'West Bengal', 'Uttar Pradesh', 'Andhra Pradesh']
            },
            'wheat': {
                'seasons': ['rabi'],
                'soil_types': ['loam', 'clay'],
                'min_temp': 15,
                'max_temp': 25,
                'rainfall_mm': 50,
                'water_requirement': 'medium',
                'duration_days': 120,
                'states': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan']
            },
            'cotton': {
                'seasons': ['kharif'],
                'soil_types': ['black', 'loam'],
                'min_temp': 18,
                'max_temp': 30,
                'rainfall_mm': 75,
                'water_requirement': 'medium',
                'duration_days': 180,
                'states': ['Gujarat', 'Maharashtra', 'Andhra Pradesh', 'Karnataka', 'Haryana']
            },
            'sugarcane': {
                'seasons': ['kharif', 'rabi'],
                'soil_types': ['loam', 'clay'],
                'min_temp': 20,
                'max_temp': 30,
                'rainfall_mm': 100,
                'water_requirement': 'high',
                'duration_days': 365,
                'states': ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat']
            },
            'maize': {
                'seasons': ['kharif', 'rabi'],
                'soil_types': ['loam', 'sandy'],
                'min_temp': 18,
                'max_temp': 27,
                'rainfall_mm': 60,
                'water_requirement': 'medium',
                'duration_days': 90,
                'states': ['Karnataka', 'Andhra Pradesh', 'Maharashtra', 'Rajasthan', 'Uttar Pradesh']
            },
            'tomato': {
                'seasons': ['kharif', 'rabi'],
                'soil_types': ['loam', 'sandy'],
                'min_temp': 20,
                'max_temp': 30,
                'rainfall_mm': 40,
                'water_requirement': 'medium',
                'duration_days': 75,
                'states': ['Karnataka', 'Andhra Pradesh', 'Maharashtra', 'West Bengal', 'Odisha']
            },
            'onion': {
                'seasons': ['rabi'],
                'soil_types': ['loam', 'sandy'],
                'min_temp': 15,
                'max_temp': 25,
                'rainfall_mm': 30,
                'water_requirement': 'low',
                'duration_days': 120,
                'states': ['Maharashtra', 'Karnataka', 'Gujarat', 'Andhra Pradesh', 'Rajasthan']
            },
            'potato': {
                'seasons': ['rabi'],
                'soil_types': ['loam', 'sandy'],
                'min_temp': 15,
                'max_temp': 20,
                'rainfall_mm': 25,
                'water_requirement': 'medium',
                'duration_days': 90,
                'states': ['Uttar Pradesh', 'West Bengal', 'Bihar', 'Gujarat', 'Madhya Pradesh']
            }
        }
        
        # Seed varieties database
        self.seed_varieties = {
            'rice': {
                'basmati': ['Pusa Basmati 1121', 'Pusa Basmati 1509', 'CSR-30'],
                'non_basmati': ['IR-64', 'Swarna', 'MTU-1010', 'BPT-5204']
            },
            'wheat': {
                'durum': ['PDW-291', 'HI-8627', 'MACS-2496'],
                'bread': ['HD-2967', 'PBW-725', 'DBW-88', 'UP-2628']
            },
            'cotton': {
                'bt_cotton': ['RCH-2', 'MRC-7017', 'PCH-2270'],
                'hybrid': ['DCH-32', 'PKVDH-1', 'G.Cot-23']
            }
        }
    
    async def recommend_crops(self, context: Dict[str, Any]) -> 'QueryResponse':
        """
        Recommend suitable crops based on the query context
        """
        from main import QueryResponse, QueryCategory
        
        try:
            query = context.get('query', '').lower()
            location = context.get('location', '').lower()
            
            # Extract information from query
            season = self.extract_season(query)
            soil_type = self.extract_soil_type(query)
            specific_crop = self.extract_crop_name(query)
            
            # If a specific crop is mentioned, provide detailed info about it
            if specific_crop:
                crop_info = self.get_crop_details(specific_crop, location, season)
                return QueryResponse(
                    category=QueryCategory.CROP_RECOMMENDATION,
                    response=crop_info,
                    language='en',
                    source="krishi_vigyan_kendra_data",
                    confidence=0.8
                )
            
            # Get current season if not specified
            if not season:
                season = self.get_current_season()
            
            # Find suitable crops
            suitable_crops = self.find_suitable_crops(location, season, soil_type)
            
            if not suitable_crops:
                return QueryResponse(
                    category=QueryCategory.CROP_RECOMMENDATION,
                    response="No reliable crop recommendations found for the specified conditions. Please consult your local Krishi Vigyan Kendra for personalized advice.",
                    language='en',
                    source="crop_recommendation_agent",
                    confidence=0.0
                )
            
            # Format recommendations
            response = self.format_crop_recommendations(suitable_crops, season, location)
            
            return QueryResponse(
                category=QueryCategory.CROP_RECOMMENDATION,
                response=response,
                language='en',
                source="krishi_vigyan_kendra_data",
                confidence=0.85,
                data={'crops': suitable_crops, 'season': season}
            )
            
        except Exception as e:
            logger.error(f"Crop recommendation error: {str(e)}")
            return QueryResponse(
                category=QueryCategory.CROP_RECOMMENDATION,
                response="Unable to provide crop recommendations at the moment. Please consult your local agriculture officer.",
                language='en',
                source="crop_agent_error",
                confidence=0.0
            )
    
    def extract_season(self, query: str) -> Optional[str]:
        """Extract season information from query"""
        if 'kharif' in query or 'monsoon' in query or 'rainy' in query:
            return 'kharif'
        elif 'rabi' in query or 'winter' in query:
            return 'rabi'
        elif 'zaid' in query or 'summer' in query:
            return 'zaid'
        return None
    
    def extract_soil_type(self, query: str) -> Optional[str]:
        """Extract soil type from query"""
        if 'clay' in query or 'heavy' in query:
            return 'clay'
        elif 'sandy' in query or 'light' in query:
            return 'sandy'
        elif 'loam' in query or 'medium' in query:
            return 'loam'
        elif 'black' in query:
            return 'black'
        return None
    
    def extract_crop_name(self, query: str) -> Optional[str]:
        """Extract specific crop name from query"""
        for crop in self.crop_database.keys():
            if crop in query:
                return crop
        return None
    
    def get_current_season(self) -> str:
        """Determine current season based on month"""
        month = datetime.now().month
        if month in [6, 7, 8, 9, 10]:  # June to October
            return 'kharif'
        elif month in [11, 12, 1, 2, 3, 4]:  # November to April
            return 'rabi'
        else:  # May
            return 'zaid'
    
    def find_suitable_crops(self, location: str, season: str, soil_type: Optional[str]) -> List[Dict[str, Any]]:
        """Find crops suitable for given conditions"""
        suitable_crops = []
        
        for crop_name, crop_data in self.crop_database.items():
            score = 0
            
            # Check season compatibility
            if season in crop_data['seasons']:
                score += 3
            
            # Check location/state compatibility
            if location and any(state.lower() in location for state in crop_data['states']):
                score += 2
            
            # Check soil compatibility
            if soil_type and soil_type in crop_data['soil_types']:
                score += 2
            elif not soil_type:  # No soil info provided
                score += 1
            
            if score >= 3:  # Minimum threshold
                suitable_crops.append({
                    'name': crop_name,
                    'score': score,
                    'data': crop_data
                })
        
        # Sort by suitability score
        suitable_crops.sort(key=lambda x: x['score'], reverse=True)
        return suitable_crops
    
    def get_crop_details(self, crop_name: str, location: str, season: Optional[str]) -> str:
        """Get detailed information about a specific crop"""
        if crop_name not in self.crop_database:
            return f"No detailed information available for {crop_name}. Please consult your local agriculture officer."
        
        crop_data = self.crop_database[crop_name]
        
        response = f"🌾 {crop_name.title()} Cultivation Guide:\n\n"
        response += f"🗓️ Growing Season: {', '.join(crop_data['seasons']).title()}\n"
        response += f"🌡️ Temperature Range: {crop_data['min_temp']}°C - {crop_data['max_temp']}°C\n"
        response += f"🌧️ Rainfall Requirement: {crop_data['rainfall_mm']}mm minimum\n"
        response += f"💧 Water Requirement: {crop_data['water_requirement'].title()}\n"
        response += f"⏰ Duration: {crop_data['duration_days']} days\n"
        response += f"🏞️ Suitable Soil: {', '.join(crop_data['soil_types']).title()}\n"
        response += f"📍 Major Growing States: {', '.join(crop_data['states'])}\n"
        
        # Add seed variety recommendations
        if crop_name in self.seed_varieties:
            response += f"\n🌱 Recommended Varieties:\n"
            for variety_type, varieties in self.seed_varieties[crop_name].items():
                response += f"• {variety_type.replace('_', ' ').title()}: {', '.join(varieties[:2])}\n"
        
        return response
    
    def format_crop_recommendations(self, crops: List[Dict[str, Any]], season: str, location: str) -> str:
        """Format crop recommendations for farmer display"""
        if not crops:
            return "No suitable crop recommendations found for the given conditions."
        
        response = f"🌾 Recommended Crops for {season.title()} Season"
        if location:
            response += f" in {location.title()}"
        response += ":\n\n"
        
        for i, crop_info in enumerate(crops[:3], 1):  # Top 3 recommendations
            crop_name = crop_info['name']
            crop_data = crop_info['data']
            
            response += f"{i}. **{crop_name.title()}**\n"
            response += f"   Duration: {crop_data['duration_days']} days\n"
            response += f"   Water Need: {crop_data['water_requirement'].title()}\n"
            response += f"   Suitable Soil: {', '.join(crop_data['soil_types']).title()}\n"
            
            # Add seed variety if available
            if crop_name in self.seed_varieties:
                varieties = list(self.seed_varieties[crop_name].values())[0]
                response += f"   Recommended Varieties: {', '.join(varieties[:2])}\n"
            
            response += "\n"
        
        response += "💡 Tip: Contact your nearest Krishi Vigyan Kendra for soil testing and personalized recommendations."
        return response

# Example usage
async def test_crop_agent():
    """Test the crop recommendation agent"""
    agent = CropRecommendationAgent()
    
    test_contexts = [
        {'query': 'what crop to grow in kharif season', 'location': 'Punjab'},
        {'query': 'rice cultivation guide', 'location': 'West Bengal'},
        {'query': 'best crop for clay soil', 'location': 'Maharashtra'},
        {'query': 'winter season crop recommendation', 'location': 'Uttar Pradesh'}
    ]
    
    for context in test_contexts:
        print(f"\nTesting: {context}")
        response = await agent.recommend_crops(context)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")

if __name__ == "__main__":
    asyncio.run(test_crop_agent())
