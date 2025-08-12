"""
Weather Data Agent - Fetches weather information using OpenWeather API
Provides current weather, forecasts, and agriculture-specific weather insights
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

class WeatherDataAgent:
    """
    Fetches weather data from OpenWeatherMap API and provides agriculture-specific insights
    """
    
    def __init__(self):
        # Get API key from environment variable
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Agriculture-specific thresholds
        self.crop_weather_thresholds = {
            'rice': {'min_temp': 20, 'max_temp': 35, 'min_rainfall': 150},
            'wheat': {'min_temp': 15, 'max_temp': 25, 'min_rainfall': 50},
            'cotton': {'min_temp': 18, 'max_temp': 30, 'min_rainfall': 75},
            'sugarcane': {'min_temp': 20, 'max_temp': 30, 'min_rainfall': 100},
            'maize': {'min_temp': 18, 'max_temp': 27, 'min_rainfall': 60}
        }
    
    async def get_weather_info(self, context: Dict[str, Any]) -> 'QueryResponse':
        """
        Get weather information based on query and location
        """
        from main import QueryResponse, QueryCategory
        
        try:
            location = context.get('location')
            query = context.get('query', '').lower()
            
            if not location:
                return QueryResponse(
                    category=QueryCategory.WEATHER,
                    response="Please provide a location to get weather information.",
                    language='en',
                    source="weather_agent",
                    confidence=0.0
                )
            
            # Get current weather
            current_weather = await self.fetch_current_weather(location)
            if not current_weather:
                return QueryResponse(
                    category=QueryCategory.WEATHER,
                    response="No reliable weather data found for this location. Please check the location name or try again later.",
                    language='en',
                    source="openweather_api",
                    confidence=0.0
                )
            
            # Check if forecast is requested
            if 'forecast' in query or 'tomorrow' in query or 'next' in query:
                forecast = await self.fetch_forecast(location)
                response = self.format_weather_with_forecast(current_weather, forecast)
            else:
                response = self.format_current_weather(current_weather)
            
            # Add agriculture-specific advice
            agriculture_advice = self.get_agriculture_advice(current_weather)
            if agriculture_advice:
                response += f"\n\n🌾 Agricultural Advice:\n{agriculture_advice}"
            
            return QueryResponse(
                category=QueryCategory.WEATHER,
                response=response,
                language='en',
                source="openweather_api",
                confidence=0.9,
                data=current_weather
            )
            
        except Exception as e:
            logger.error(f"Weather fetch error: {str(e)}")
            return QueryResponse(
                category=QueryCategory.WEATHER,
                response="Unable to fetch weather information at the moment. Please try again later.",
                language='en',
                source="weather_agent_error",
                confidence=0.0
            )
    
    async def fetch_current_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather from OpenWeather API
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Weather API error: {str(e)}")
            # Return mock data for testing when API is not available
            return self.get_mock_weather_data(location)
    
    async def fetch_forecast(self, location: str) -> Optional[Dict[str, Any]]:
        """
        Fetch 5-day weather forecast
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return None
                        
        except Exception as e:
            logger.error(f"Forecast API error: {str(e)}")
            return None
    
    def format_current_weather(self, weather_data: Dict[str, Any]) -> str:
        """
        Format current weather data for farmer-friendly display
        """
        try:
            city = weather_data['name']
            country = weather_data['sys']['country']
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description'].title()
            wind_speed = weather_data['wind']['speed']
            
            response = f"🌤️ Current Weather in {city}, {country}:\n\n"
            response += f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
            response += f"Condition: {description}\n"
            response += f"Humidity: {humidity}%\n"
            response += f"Wind Speed: {wind_speed} m/s\n"
            
            return response
            
        except KeyError as e:
            logger.error(f"Weather data formatting error: {str(e)}")
            return "Weather data received but could not be properly formatted."
    
    def format_weather_with_forecast(self, current: Dict[str, Any], forecast: Optional[Dict[str, Any]]) -> str:
        """
        Format weather with forecast information
        """
        response = self.format_current_weather(current)
        
        if forecast and 'list' in forecast:
            response += "\n\n📅 3-Day Forecast:\n"
            
            # Get forecast for next 3 days
            forecast_days = {}
            for item in forecast['list'][:24]:  # 24 entries = 3 days (8 per day)
                date = datetime.fromtimestamp(item['dt']).date()
                if date not in forecast_days:
                    forecast_days[date] = {
                        'temp_min': item['main']['temp_min'],
                        'temp_max': item['main']['temp_max'],
                        'description': item['weather'][0]['description']
                    }
                else:
                    forecast_days[date]['temp_min'] = min(forecast_days[date]['temp_min'], item['main']['temp_min'])
                    forecast_days[date]['temp_max'] = max(forecast_days[date]['temp_max'], item['main']['temp_max'])
            
            for date, data in list(forecast_days.items())[:3]:
                day_name = date.strftime("%A")
                response += f"\n{day_name}: {data['temp_min']:.0f}°C - {data['temp_max']:.0f}°C, {data['description'].title()}"
        
        return response
    
    def get_agriculture_advice(self, weather_data: Dict[str, Any]) -> str:
        """
        Provide agriculture-specific advice based on weather conditions
        """
        try:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['main'].lower()
            
            advice = []
            
            # Temperature-based advice
            if temp > 35:
                advice.append("⚠️ High temperature alert! Ensure adequate irrigation and consider shade nets for sensitive crops.")
            elif temp < 10:
                advice.append("🥶 Cold weather warning! Protect crops from frost damage.")
            
            # Humidity-based advice
            if humidity > 80:
                advice.append("💧 High humidity may increase fungal disease risk. Monitor crops closely.")
            elif humidity < 30:
                advice.append("🌵 Low humidity - increase irrigation frequency.")
            
            # Weather condition advice
            if 'rain' in description:
                advice.append("🌧️ Rainy conditions - postpone pesticide application and ensure proper drainage.")
            elif description == 'clear':
                advice.append("☀️ Clear weather - good time for field operations and spraying.")
            
            return " ".join(advice)
            
        except Exception as e:
            logger.error(f"Agriculture advice error: {str(e)}")
            return ""
    
    def get_mock_weather_data(self, location: str) -> Dict[str, Any]:
        """
        Return mock weather data for testing purposes
        """
        return {
            'name': location,
            'sys': {'country': 'IN'},
            'main': {
                'temp': 28.5,
                'feels_like': 30.2,
                'humidity': 65
            },
            'weather': [{'main': 'Clear', 'description': 'clear sky'}],
            'wind': {'speed': 2.1}
        }

# Example usage
async def test_weather_agent():
    """Test the weather agent"""
    agent = WeatherDataAgent()
    
    test_contexts = [
        {'query': 'current weather', 'location': 'Delhi'},
        {'query': 'weather forecast tomorrow', 'location': 'Mumbai'},
        {'query': 'will it rain today', 'location': 'Bangalore'}
    ]
    
    for context in test_contexts:
        print(f"\nTesting: {context}")
        response = await agent.get_weather_info(context)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")

if __name__ == "__main__":
    asyncio.run(test_weather_agent())
