"""
Query Classifier Agent - Categorizes farmer queries into predefined categories
Uses keyword matching and pattern recognition for classification
"""

import re
import asyncio
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class QueryClassifierAgent:
    """
    Classifies farmer queries into categories:
    Weather, Crop Recommendation, Market Price, Irrigation, Pest/Disease, Finance/Policy
    """
    
    def __init__(self):
        # Keywords for each category
        self.category_keywords = {
            'weather': [
                'weather', 'rain', 'rainfall', 'temperature', 'forecast', 'climate',
                'sunny', 'cloudy', 'storm', 'wind', 'humidity', 'monsoon'
            ],
            'crop_recommendation': [
                'crop', 'seed', 'variety', 'plant', 'sow', 'grow', 'cultivation',
                'season', 'kharif', 'rabi', 'zaid', 'recommend', 'suitable', 'best'
            ],
            'market_price': [
                'price', 'rate', 'market', 'mandi', 'cost', 'sell', 'buy',
                'wholesale', 'retail', 'commodity', 'trading'
            ],
            'irrigation': [
                'irrigation', 'water', 'watering', 'drip', 'sprinkler',
                'canal', 'bore', 'well', 'pump', 'timing'
            ],
            'pest_disease': [
                'pest', 'insect', 'bug', 'disease', 'fungus', 'virus', 'bacteria',
                'leaf', 'spot', 'blight', 'rot', 'wilt', 'aphid', 'caterpillar',
                'yellow', 'brown', 'damage', 'infestation'
            ],
            'finance_policy': [
                'loan', 'credit', 'subsidy', 'scheme', 'policy', 'government',
                'bank', 'finance', 'insurance', 'compensation', 'benefit',
                'kisan', 'pmkisan', 'fasal', 'bima'
            ]
        }
        
        # Question patterns for better classification
        self.question_patterns = {
            'weather': [
                r'weather.*forecast', r'rain.*today', r'temperature.*tomorrow',
                r'will.*rain', r'monsoon.*arrive'
            ],
            'crop_recommendation': [
                r'what.*crop.*grow', r'which.*seed.*plant', r'best.*variety',
                r'recommend.*crop', r'suitable.*season'
            ],
            'market_price': [
                r'price.*of.*', r'cost.*per.*', r'market.*rate',
                r'how much.*sell', r'current.*price'
            ],
            'irrigation': [
                r'when.*water', r'how.*irrigate', r'irrigation.*schedule',
                r'water.*requirement', r'frequency.*watering'
            ],
            'pest_disease': [
                r'pest.*problem', r'disease.*crop', r'insect.*attack',
                r'leaf.*yellow', r'plant.*sick', r'spot.*on.*leaf'
            ],
            'finance_policy': [
                r'loan.*agriculture', r'subsidy.*scheme', r'government.*benefit',
                r'insurance.*crop', r'kisan.*scheme'
            ]
        }
    
    async def classify(self, query: str) -> Dict[str, Any]:
        """
        Classify the query into one of the predefined categories
        """
        try:
            query_lower = query.lower()
            
            # Score each category based on keyword matches
            category_scores = {}
            
            for category, keywords in self.category_keywords.items():
                score = 0
                
                # Keyword matching
                for keyword in keywords:
                    if keyword in query_lower:
                        score += 1
                
                # Pattern matching (higher weight)
                if category in self.question_patterns:
                    for pattern in self.question_patterns[category]:
                        if re.search(pattern, query_lower):
                            score += 3
                
                category_scores[category] = score
            
            # Find the category with highest score
            best_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[best_category]
            
            # Calculate confidence based on score
            total_words = len(query.split())
            confidence = min(max_score / max(total_words * 0.3, 1), 1.0)
            
            # If confidence is too low, mark as unknown
            if confidence < 0.3:
                best_category = 'unknown'
                confidence = 0.2
            
            return {
                'category': best_category,
                'confidence': confidence,
                'scores': category_scores
            }
            
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            return {
                'category': 'unknown',
                'confidence': 0.0,
                'scores': {}
            }
    
    def get_category_description(self, category: str) -> str:
        """
        Get a human-readable description of the category
        """
        descriptions = {
            'weather': 'Weather information and forecasts',
            'crop_recommendation': 'Crop and seed recommendations',
            'market_price': 'Market prices and commodity rates',
            'irrigation': 'Irrigation guidance and water management',
            'pest_disease': 'Pest identification and disease management',
            'finance_policy': 'Government schemes and financial assistance',
            'unknown': 'Query category could not be determined'
        }
        return descriptions.get(category, 'Unknown category')

# Example usage and testing
async def test_classifier():
    """Test the query classifier with sample queries"""
    classifier = QueryClassifierAgent()
    
    test_queries = [
        "What is the weather forecast for tomorrow?",
        "Which crop is best for kharif season?",
        "What is the current price of wheat in Punjab?",
        "When should I irrigate my cotton crop?",
        "My tomato plants have yellow leaves, what should I do?",
        "How to apply for PM Kisan scheme?",
        "Tell me about farming",  # Low confidence query
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = await classifier.classify(query)
        print(f"Category: {result['category']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Description: {classifier.get_category_description(result['category'])}")

if __name__ == "__main__":
    asyncio.run(test_classifier())
