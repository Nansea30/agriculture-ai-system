# 🌾 Agriculture AI System - Voice-Enabled Assistant for Indian Farmers

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Voice Commands](https://img.shields.io/badge/Voice-Enabled-orange.svg)](#voice-commands)
[![Multi-Language](https://img.shields.io/badge/Languages-8_Indian_Languages-purple.svg)](#supported-languages)

> **AI-powered decision support system for Indian farmers with multilingual voice command capabilities**

A comprehensive AI-powered decision support system designed specifically for Indian farmers. Features **voice commands in 8 Indian languages**, real-time speech recognition, and natural voice responses, making agricultural advice accessible to farmers who prefer speaking over typing.

## 🎯 Overview

This system acts as a digital agriculture extension service, capable of understanding multilingual farmer queries (Hindi, English, and other Indian languages) and providing reliable, data-driven advice. It's designed to work with Indian agriculture datasets, government APIs, and local conditions.

## ✨ Features

### 🤖 Multi-Agent Architecture
- **Manager Agent**: Orchestrates all sub-agents and routes queries
- **Translation Agent**: Handles multilingual queries and responses
- **Query Classifier**: Categorizes farmer queries automatically
- **Weather Agent**: Provides weather forecasts and agriculture alerts
- **Crop Recommendation Agent**: Suggests suitable crops and varieties
- **Market Price Agent**: Fetches current mandi prices and trends
- **Irrigation Agent**: Advises on water management and timing
- **Pest & Disease Agent**: Diagnoses crop health issues
- **Finance & Policy Agent**: Information on government schemes

### 🌍 Multilingual Support
- Native Hindi support with Devanagari script recognition
- Support for other Indian languages (Bengali, Telugu, Tamil, etc.)
- Code-switched query handling (mixing Hindi and English)
- Automatic translation of responses back to user's language

### 📊 Data Sources
- **Weather**: OpenWeatherMap API integration
- **Market Prices**: Agmarknet/eNAM API compatibility
- **Crop Information**: Krishi Vigyan Kendra datasets
- **Government Schemes**: India.gov.in agriculture portals
- **Pest/Disease**: ICAR advisory database

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection for API calls
- Optional: OpenWeather API key for live weather data

### Installation

1. **Clone or download the system:**
```bash
cd agriculture_ai_system
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (optional):**
```bash
# For live weather data
export OPENWEATHER_API_KEY="your_api_key_here"
```

### Running the Demo

```bash
python demo_cli.py
```

This will start an interactive CLI where you can test the system with various queries.

## 🎮 Usage Examples

### Weather Queries
```
English: "What is the weather forecast for Delhi?"
Hindi: "दिल्ली में कल बारिश होगी क्या?"
```

### Crop Recommendations
```
English: "Which crop should I grow in kharif season?"
Hindi: "खरीफ के मौसम में कौन सी फसल उगाऊं?"
```

### Market Prices
```
English: "Current wheat price in Punjab"
Hindi: "पंजाब में गेहूं का आज का भाव क्या है?"
```

### Pest & Disease
```
English: "My tomato plants have yellow leaves with brown spots"
Hindi: "मेरे टमाटर के पौधे में पीली पत्तियां हैं"
```

### Government Schemes
```
English: "PM Kisan scheme eligibility"
Hindi: "प्रधानमंत्री किसान योजना की जानकारी"
```

## 🏗️ System Architecture

```
┌─────────────────┐
│  Manager Agent  │ ← Main orchestrator
└─────────┬───────┘
          │
     ┌────┴────┐
     │ Translation │ ← Language detection & translation
     └────┬────┘
          │
     ┌────┴────┐
     │Classifier│ ← Query categorization
     └────┬────┘
          │
    ┌─────┴─────┐
    │Sub-Agents │ ← Specialized domain agents
    └───────────┘
```

### Agent Responsibilities

1. **Manager Agent** (`main.py`)
   - Query orchestration and routing
   - Response formatting and confidence scoring
   - Error handling and fallback responses

2. **Translation Agent** (`agents/translation_agent.py`)
   - Language detection using Unicode patterns
   - Basic Hindi-English translation
   - Response localization

3. **Query Classifier** (`agents/classifier_agent.py`)
   - Keyword-based classification
   - Pattern matching for better accuracy
   - Confidence scoring for categories

4. **Weather Agent** (`agents/weather_agent.py`)
   - OpenWeatherMap API integration
   - Agriculture-specific weather advice
   - Extreme weather warnings

5. **Crop Recommendation Agent** (`agents/crop_agent.py`)
   - Season-based crop suggestions
   - Soil type compatibility
   - Seed variety recommendations

6. **Market Price Agent** (`agents/market_agent.py`)
   - Mandi price fetching (mock implementation)
   - MSP comparison and advice
   - Market trend analysis

7. **Irrigation Agent** (`agents/irrigation_agent.py`)
   - Crop-specific irrigation schedules
   - Water requirement calculations
   - Irrigation method recommendations

8. **Pest & Disease Agent** (`agents/pest_agent.py`)
   - Symptom-based diagnosis
   - Treatment recommendations (organic & chemical)
   - Prevention strategies

9. **Finance & Policy Agent** (`agents/finance_agent.py`)
   - Government scheme information
   - Eligibility criteria and application process
   - MSP and subsidy details

## 📋 Query Categories

The system automatically categorizes queries into:

- **Weather** - Forecasts, alerts, climate information
- **Crop Recommendation** - Suitable crops, varieties, cultivation guides
- **Market Price** - Current rates, MSP, market trends
- **Irrigation** - Water management, timing, methods
- **Pest/Disease** - Diagnosis, treatment, prevention
- **Finance/Policy** - Government schemes, loans, subsidies

## 🔧 Configuration

### Environment Variables
```bash
# Weather API (optional - system works with mock data)
OPENWEATHER_API_KEY="your_openweather_api_key"

# Database connections (for production)
DATABASE_URL="your_database_connection_string"

# Logging level
LOG_LEVEL="INFO"
```

### Customizing Data Sources

To integrate real APIs, modify the relevant agent files:

1. **Weather Data**: Update `agents/weather_agent.py` with your API credentials
2. **Market Prices**: Implement Agmarknet API calls in `agents/market_agent.py`
3. **Crop Database**: Update crop data in `agents/crop_agent.py`

## 🌟 Key Features

### Reliability & Safety
- **No Hallucination**: Returns "No reliable data found" when uncertain
- **Source Attribution**: All responses cite their data sources
- **Confidence Scoring**: Each response includes confidence levels
- **Fallback Advice**: Recommends contacting local agriculture officers when needed

### Farmer-Friendly Design
- **Simple Language**: Responses in easy-to-understand terms
- **Practical Advice**: Actionable recommendations with specific steps
- **Local Context**: Considers Indian conditions, seasons, and practices
- **Multi-format Support**: Works with various query styles and languages

### Extensibility
- **Modular Architecture**: Easy to add new agents or modify existing ones
- **API Integration**: Designed for real API integration
- **Database Support**: Can be extended with persistent storage
- **Scalability**: Async architecture supports multiple concurrent users

## 🔍 Testing

### Manual Testing
Run the demo CLI and try various queries:
```bash
python demo_cli.py
```

### Agent Testing
Test individual agents:
```bash
# Test weather agent
python agents/weather_agent.py

# Test crop recommendations
python agents/crop_agent.py

# Test other agents similarly
```

## 🚀 Deployment Options

### Development
```bash
python demo_cli.py
```

### Production Web API (Optional)
```bash
# Install FastAPI dependencies
pip install fastapi uvicorn

# Create web API wrapper (not included in this demo)
# Run with uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Mobile/Web Integration
The system is designed to be integrated into:
- Mobile applications
- Web interfaces
- WhatsApp/SMS bots
- Voice assistants

## 📚 Knowledge Base

### Crop Database
- Major Indian crops (rice, wheat, cotton, sugarcane, etc.)
- Season-wise cultivation (Kharif, Rabi, Zaid)
- Soil type requirements
- Water requirements and irrigation schedules

### Government Schemes
- PM Kisan Samman Nidhi
- Pradhan Mantri Fasal Bima Yojana
- Kisan Credit Card
- PM KUSUM (Solar)
- Soil Health Card Scheme

### Market Information
- MSP rates for major crops
- State-wise price variations
- Seasonal price trends
- Market advisory

## 🤝 Contributing

To contribute to this system:

1. **Add New Agents**: Create new specialized agents for specific domains
2. **Enhance Language Support**: Improve translation capabilities
3. **Data Integration**: Connect real APIs and databases
4. **UI Development**: Build web or mobile interfaces
5. **Performance Optimization**: Improve response times and accuracy

## 📄 License

This system is designed for educational and development purposes. For production deployment, ensure proper API licensing and data usage agreements.

## 📞 Support

For farmers using this system:
- Contact your local Krishi Vigyan Kendra
- Call Kisan Call Center: 1800-180-1551
- Visit agriculture.gov.in for official information

For technical support:
- Check the troubleshooting section
- Review agent logs for debugging
- Ensure all dependencies are properly installed

## 🎯 Future Enhancements

### Planned Features
- **Voice Input/Output**: Speech recognition and text-to-speech
- **Image Analysis**: Crop and pest identification from photos
- **IoT Integration**: Sensor data integration for precision agriculture
- **Predictive Analytics**: ML models for yield and price prediction
- **Regional Customization**: State-specific advice and data

### API Integrations
- **Real-time APIs**: Live weather, market, and government data
- **Payment Integration**: For purchasing inputs and insurance
- **GPS Integration**: Location-based services and mapping
- **Social Features**: Farmer community and knowledge sharing

---

**Built for Indian farmers, by leveraging technology to make agriculture advice accessible, reliable, and actionable.** 🌾🇮🇳
