"""
Irrigation & Weather Risk Agent - Provides irrigation guidance and weather risk warnings
Advises on irrigation timing, water management, and extreme weather preparation
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class IrrigationWeatherRiskAgent:
    """
    Provides irrigation advice and weather risk management guidance
    """
    
    def __init__(self):
        # Crop-specific irrigation requirements
        self.irrigation_schedule = {
            'rice': {
                'water_requirement_mm': 1200,
                'critical_stages': ['transplanting', 'tillering', 'flowering', 'grain_filling'],
                'intervals': {
                    'initial': 1,      # days
                    'development': 2,
                    'mid_season': 3,
                    'late_season': 5
                },
                'flood_irrigation': True
            },
            'wheat': {
                'water_requirement_mm': 450,
                'critical_stages': ['crown_root', 'tillering', 'jointing', 'flowering'],
                'intervals': {
                    'initial': 3,
                    'development': 7,
                    'mid_season': 10,
                    'late_season': 15
                },
                'flood_irrigation': False
            },
            'cotton': {
                'water_requirement_mm': 700,
                'critical_stages': ['germination', 'squaring', 'flowering', 'boll_formation'],
                'intervals': {
                    'initial': 4,
                    'development': 7,
                    'mid_season': 10,
                    'late_season': 12
                },
                'flood_irrigation': False
            },
            'sugarcane': {
                'water_requirement_mm': 1800,
                'critical_stages': ['germination', 'tillering', 'grand_growth', 'maturation'],
                'intervals': {
                    'initial': 2,
                    'development': 5,
                    'mid_season': 7,
                    'late_season': 10
                },
                'flood_irrigation': False
            },
            'tomato': {
                'water_requirement_mm': 600,
                'critical_stages': ['transplanting', 'flowering', 'fruit_set', 'fruit_development'],
                'intervals': {
                    'initial': 2,
                    'development': 3,
                    'mid_season': 4,
                    'late_season': 6
                },
                'flood_irrigation': False
            }
        }
        
        # Weather risk thresholds
        self.weather_thresholds = {
            'high_temperature': 35,  # °C
            'low_temperature': 10,   # °C
            'high_wind_speed': 15,   # m/s
            'heavy_rainfall': 50,    # mm/day
            'drought_days': 15       # consecutive dry days
        }
        
        # Irrigation methods efficiency
        self.irrigation_efficiency = {
            'flood': 40,      # % efficiency
            'furrow': 60,
            'sprinkler': 75,
            'drip': 90,
            'micro_sprinkler': 85
        }
    
    async def get_irrigation_advice(self, context: Dict[str, Any]) -> 'QueryResponse':
        """
        Provide irrigation advice based on crop, weather, and growth stage
        """
        from main import QueryResponse, QueryCategory
        
        try:
            query = context.get('query', '').lower()
            location = context.get('location', '')
            
            # Extract crop information from query
            crop = self.extract_crop_info(query)
            growth_stage = self.extract_growth_stage(query)
            irrigation_method = self.extract_irrigation_method(query)
            
            # Check if it's a general irrigation timing question
            if 'when' in query and ('irrigate' in query or 'water' in query):
                if crop:
                    response = self.get_crop_irrigation_schedule(crop, growth_stage)
                else:
                    response = self.get_general_irrigation_advice()
            elif 'frequency' in query or 'how often' in query:
                if crop:
                    response = self.get_irrigation_frequency(crop, growth_stage)
                else:
                    response = "Please specify the crop to get irrigation frequency advice."
            elif 'method' in query or 'system' in query:
                response = self.get_irrigation_method_advice(crop, irrigation_method)
            elif 'water requirement' in query or 'how much water' in query:
                if crop:
                    response = self.get_water_requirement(crop)
                else:
                    response = "Please specify the crop to get water requirement information."
            else:
                # General irrigation advice
                response = self.get_comprehensive_irrigation_advice(crop, location)
            
            # Add weather-based warnings
            weather_warnings = self.get_weather_warnings(location)
            if weather_warnings:
                response += f"\n\n⚠️ Weather Alerts:\n{weather_warnings}"
            
            return QueryResponse(
                category=QueryCategory.IRRIGATION,
                response=response,
                language='en',
                source="irrigation_management_system",
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Irrigation advice error: {str(e)}")
            return QueryResponse(
                category=QueryCategory.IRRIGATION,
                response="Unable to provide irrigation advice at the moment. Please consult your local agriculture extension officer.",
                language='en',
                source="irrigation_agent_error",
                confidence=0.0
            )
    
    def extract_crop_info(self, query: str) -> Optional[str]:
        """Extract crop information from query"""
        crops = list(self.irrigation_schedule.keys())
        for crop in crops:
            if crop in query:
                return crop
        return None
    
    def extract_growth_stage(self, query: str) -> Optional[str]:
        """Extract growth stage information from query"""
        growth_stages = [
            'germination', 'transplanting', 'initial', 'tillering', 'development',
            'flowering', 'fruit_set', 'mid_season', 'maturation', 'late_season'
        ]
        
        for stage in growth_stages:
            if stage in query:
                return stage
        return None
    
    def extract_irrigation_method(self, query: str) -> Optional[str]:
        """Extract irrigation method from query"""
        methods = list(self.irrigation_efficiency.keys())
        for method in methods:
            if method in query:
                return method
        return None
    
    def get_crop_irrigation_schedule(self, crop: str, growth_stage: Optional[str]) -> str:
        """Get specific irrigation schedule for a crop"""
        if crop not in self.irrigation_schedule:
            return f"Irrigation schedule not available for {crop}."
        
        crop_data = self.irrigation_schedule[crop]
        
        response = f"💧 {crop.title()} Irrigation Schedule:\n\n"
        
        if growth_stage:
            # Specific stage advice
            if growth_stage in crop_data['intervals']:
                interval = crop_data['intervals'][growth_stage]
                response += f"Current Stage ({growth_stage.replace('_', ' ').title()}):\n"
                response += f"• Irrigation Interval: Every {interval} days\n"
            else:
                response += f"Growth stage '{growth_stage}' not found in database.\n"
        else:
            # Full schedule
            response += "Irrigation Intervals by Growth Stage:\n"
            for stage, days in crop_data['intervals'].items():
                response += f"• {stage.replace('_', ' ').title()}: Every {days} days\n"
        
        response += f"\nTotal Water Requirement: {crop_data['water_requirement_mm']}mm per season\n"
        
        # Critical stages
        response += f"Critical Stages (Never miss irrigation):\n"
        for stage in crop_data['critical_stages']:
            response += f"• {stage.replace('_', ' ').title()}\n"
        
        return response
    
    def get_irrigation_frequency(self, crop: str, growth_stage: Optional[str]) -> str:
        """Get irrigation frequency advice"""
        if crop not in self.irrigation_schedule:
            return f"Irrigation frequency data not available for {crop}."
        
        crop_data = self.irrigation_schedule[crop]
        
        if growth_stage and growth_stage in crop_data['intervals']:
            interval = crop_data['intervals'][growth_stage]
            response = f"💧 {crop.title()} - {growth_stage.replace('_', ' ').title()} Stage:\n"
            response += f"Irrigate every {interval} days"
        else:
            response = f"💧 {crop.title()} Irrigation Frequency:\n"
            for stage, days in crop_data['intervals'].items():
                response += f"• {stage.replace('_', ' ').title()}: Every {days} days\n"
        
        return response
    
    def get_water_requirement(self, crop: str) -> str:
        """Get water requirement information"""
        if crop not in self.irrigation_schedule:
            return f"Water requirement data not available for {crop}."
        
        crop_data = self.irrigation_schedule[crop]
        water_req = crop_data['water_requirement_mm']
        
        response = f"💧 {crop.title()} Water Requirements:\n\n"
        response += f"Total Seasonal Requirement: {water_req}mm\n"
        response += f"Daily Average: {water_req / 120:.1f}mm (assuming 120-day crop cycle)\n"
        
        # Convert to practical units
        response += f"\nFor 1 Acre Field:\n"
        response += f"• Total water needed: {water_req * 40.47:.0f} cubic meters\n"
        response += f"• Daily average: {(water_req * 40.47) / 120:.1f} cubic meters\n"
        
        return response
    
    def get_irrigation_method_advice(self, crop: Optional[str], method: Optional[str]) -> str:
        """Provide irrigation method recommendations"""
        response = "💧 Irrigation Method Recommendations:\n\n"
        
        if method:
            if method in self.irrigation_efficiency:
                efficiency = self.irrigation_efficiency[method]
                response += f"{method.title()} Irrigation:\n"
                response += f"• Water Use Efficiency: {efficiency}%\n"
                
                # Method-specific advice
                if method == 'drip':
                    response += "• Best for high-value crops like vegetables and fruits\n"
                    response += "• Reduces water consumption by 30-50%\n"
                    response += "• Prevents weed growth and soil erosion\n"
                elif method == 'sprinkler':
                    response += "• Suitable for field crops and sandy soils\n"
                    response += "• Good for areas with water scarcity\n"
                    response += "• Can be used for frost protection\n"
                elif method == 'flood':
                    response += "• Traditional method for rice cultivation\n"
                    response += "• High water consumption\n"
                    response += "• Suitable for heavy clay soils\n"
            else:
                response += f"Information not available for {method} irrigation.\n"
        else:
            # General method comparison
            response += "Method Comparison (Water Use Efficiency):\n"
            sorted_methods = sorted(self.irrigation_efficiency.items(), key=lambda x: x[1], reverse=True)
            for method, efficiency in sorted_methods:
                response += f"• {method.title()}: {efficiency}%\n"
            
            response += "\n💡 Recommendation: Choose drip or micro-sprinkler for water conservation."
        
        return response
    
    def get_general_irrigation_advice(self) -> str:
        """Provide general irrigation advice"""
        response = "💧 General Irrigation Guidelines:\n\n"
        response += "Best Time to Irrigate:\n"
        response += "• Early morning (5-8 AM) - less evaporation\n"
        response += "• Late evening (6-8 PM) - avoid if fungal diseases are a concern\n\n"
        
        response += "Signs Your Crop Needs Water:\n"
        response += "• Soil feels dry 5-10cm below surface\n"
        response += "• Leaves appear wilted during midday\n"
        response += "• Plant growth slows down\n\n"
        
        response += "Water Conservation Tips:\n"
        response += "• Use mulching to reduce evaporation\n"
        response += "• Install drip irrigation for water efficiency\n"
        response += "• Check soil moisture before irrigating\n"
        response += "• Avoid over-irrigation to prevent root diseases\n"
        
        return response
    
    def get_comprehensive_irrigation_advice(self, crop: Optional[str], location: str) -> str:
        """Provide comprehensive irrigation advice"""
        if crop and crop in self.irrigation_schedule:
            return self.get_crop_irrigation_schedule(crop, None)
        else:
            return self.get_general_irrigation_advice()
    
    def get_weather_warnings(self, location: str) -> str:
        """Get weather-based irrigation warnings (mock implementation)"""
        # In a real system, this would fetch actual weather data
        warnings = []
        
        # Mock weather conditions for demonstration
        current_temp = 32  # Assume current temperature
        wind_speed = 8     # Assume current wind speed
        
        if current_temp > self.weather_thresholds['high_temperature']:
            warnings.append(f"🌡️ High temperature ({current_temp}°C) - increase irrigation frequency")
        
        if wind_speed > self.weather_thresholds['high_wind_speed']:
            warnings.append(f"💨 High wind speed ({wind_speed} m/s) - avoid sprinkler irrigation")
        
        # Add seasonal warnings
        month = datetime.now().month
        if month in [4, 5, 6]:  # Summer months
            warnings.append("☀️ Summer season - monitor soil moisture closely")
        elif month in [7, 8, 9]:  # Monsoon months
            warnings.append("🌧️ Monsoon season - reduce irrigation, ensure proper drainage")
        
        return "\n".join(warnings) if warnings else ""

# Example usage
async def test_irrigation_agent():
    """Test the irrigation agent"""
    agent = IrrigationWeatherRiskAgent()
    
    test_contexts = [
        {'query': 'when to irrigate wheat crop', 'location': 'Punjab'},
        {'query': 'rice irrigation frequency', 'location': 'West Bengal'},
        {'query': 'drip irrigation for tomato', 'location': 'Karnataka'},
        {'query': 'water requirement for cotton', 'location': 'Gujarat'}
    ]
    
    for context in test_contexts:
        print(f"\nTesting: {context}")
        response = await agent.get_irrigation_advice(context)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")

if __name__ == "__main__":
    asyncio.run(test_irrigation_agent())
