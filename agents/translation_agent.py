"""
Translation Agent - Handles multilingual queries and responses
Supports Hindi, English, and other Indian languages
"""

import re
import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TranslationAgent:
    """
    Detects language and translates farmer queries to English,
    then translates responses back to original language
    """
    
    def __init__(self):
        # Store original query context for better translation
        self.current_context = {
            'original_query': '',
            'detected_language': 'en',
            'translation_confidence': 1.0
        }
        
        # Language detection patterns (basic implementation)
        self.language_patterns = {
            'hi': r'[\u0900-\u097F]',  # Devanagari script (Hindi)
            'bn': r'[\u0980-\u09FF]',  # Bengali
            'te': r'[\u0C00-\u0C7F]',  # Telugu
            'ta': r'[\u0B80-\u0BFF]',  # Tamil
            'ml': r'[\u0D00-\u0D7F]',  # Malayalam
            'kn': r'[\u0C80-\u0CFF]',  # Kannada
            'gu': r'[\u0A80-\u0AFF]',  # Gujarati
            'pa': r'[\u0A00-\u0A7F]',  # Punjabi
        }
        
        # Common agriculture terms dictionary
        self.agriculture_terms = {
            'hi': {
                'फसल': 'crop',
                'खेत': 'field',
                'बारिश': 'rain',
                'मौसम': 'weather',
                'कीट': 'pest',
                'बीमारी': 'disease',
                'पानी': 'water',
                'सिंचाई': 'irrigation',
                'बाजार': 'market',
                'दाम': 'price',
                'योजना': 'scheme',
                'सब्सिडी': 'subsidy',
                'बीज': 'seed',
                'खाद': 'fertilizer',
                'मिट्टी': 'soil',
                'धान': 'rice',
                'गेहूं': 'wheat',
                'कपास': 'cotton',
                'टमाटर': 'tomato',
                'आलू': 'potato',
                'प्याज': 'onion',
                'सब्जी': 'vegetable',
                'फल': 'fruit',
                'किसान': 'farmer',
                'खेती': 'farming',
                'उपज': 'yield',
                'नुकसान': 'damage',
                'लाभ': 'profit',
                'आय': 'income',
                'तापमान': 'temperature',
                'नमी': 'humidity',
                'हवा': 'wind'
            }
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect the primary language of the input text
        """
        # Check for Devanagari (Hindi) characters
        if re.search(self.language_patterns['hi'], text):
            return 'hi'
        
        # Check for other Indian language scripts
        for lang, pattern in self.language_patterns.items():
            if re.search(pattern, text):
                return lang
        
        # Default to English
        return 'en'
    
    async def process(self, query: str) -> Dict[str, Any]:
        """
        Process query: detect language and translate to English if needed
        """
        try:
            original_language = self.detect_language(query)
            
            # Store context for better response translation
            self.current_context = {
                'original_query': query,
                'detected_language': original_language,
                'translation_confidence': 1.0 if original_language == 'en' else 0.8
            }
            
            if original_language == 'en':
                return {
                    'language': 'en',
                    'translated_query': query,
                    'confidence': 1.0
                }
            
            # Translate to English (simplified implementation)
            english_query = await self.translate_to_english(query, original_language)
            
            return {
                'language': original_language,
                'translated_query': english_query,
                'confidence': 0.8
            }
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return {
                'language': 'en',
                'translated_query': query,
                'confidence': 0.5
            }
    
    async def translate_to_english(self, text: str, source_lang: str) -> str:
        """
        Translate text from source language to English
        This is a simplified implementation - in production, use Google Translate API or similar
        """
        if source_lang == 'hi':
            # Basic Hindi to English translation for common agriculture terms
            english_text = text
            if source_lang in self.agriculture_terms:
                for hindi_term, english_term in self.agriculture_terms[source_lang].items():
                    # Use word boundaries for better matching
                    english_text = re.sub(r'\b' + re.escape(hindi_term) + r'\b', english_term, english_text)
            
            # Handle common question patterns and sentence structures
            if 'क्या' in text:
                if 'होगी' in text or 'है' in text:
                    english_text = f"Will there be {english_text}" if 'होगी' in text else f"Is there {english_text}"
                else:
                    english_text = f"What {english_text}"
            elif 'कैसे' in text:
                english_text = f"How to {english_text}"
            elif 'कब' in text:
                english_text = f"When {english_text}"
            elif 'कहाँ' in text:
                english_text = f"Where {english_text}"
            elif 'कौन' in text:
                english_text = f"Which {english_text}"
            elif 'कितना' in text:
                english_text = f"How much {english_text}"
            
            # Clean up the translation
            english_text = re.sub(r'\s+', ' ', english_text).strip()
            return english_text
        
        # For other languages, return original text with note
        return f"[{source_lang.upper()}] {text}"
    
    async def translate_response(self, response: str, target_lang: str) -> str:
        """
        Translate response back to target language
        This is a simplified implementation - in production, use proper translation service
        """
        if target_lang == 'en':
            return response
        
        if target_lang == 'hi':
            # Basic English to Hindi translation for responses
            hindi_response = response
            
            # Common English to Hindi phrase translations
            phrase_translations = {
                'Based on your query': 'आपके प्रश्न के आधार पर',
                'Here are some recommendations': 'यहाँ कुछ सुझाव हैं',
                'You should': 'आपको चाहिए',
                'It is recommended': 'सुझाव दिया जाता है',
                'For better results': 'बेहतर परिणाम के लिए',
                'Contact your local': 'अपने स्थानीय से संपर्क करें',
                'agriculture officer': 'कृषि अधिकारी',
                'weather forecast': 'मौसम पूर्वानुमान',
                'market price': 'बाजार भाव',
                'good quality': 'अच्छी गुणवत्ता',
                'proper irrigation': 'उचित सिंचाई',
                'organic pesticides': 'जैविक कीटनाशक',
                'field hygiene': 'खेत की सफाई'
            }
            
            # Translate common phrases first
            for english_phrase, hindi_phrase in phrase_translations.items():
                hindi_response = re.sub(r'\b' + re.escape(english_phrase) + r'\b', hindi_phrase, hindi_response, flags=re.IGNORECASE)
            
            # Translate common agriculture terms back to Hindi
            english_to_hindi = {v: k for k, v in self.agriculture_terms['hi'].items()}
            for english_term, hindi_term in english_to_hindi.items():
                # Use word boundaries to avoid partial replacements
                hindi_response = re.sub(r'\b' + re.escape(english_term) + r'\b', hindi_term, hindi_response, flags=re.IGNORECASE)
            
            return hindi_response
        
        # For other languages, return original response with a note that translation is limited
        return response + f" (Note: Full translation to {target_lang.upper()} not available)"

# Example usage
async def test_translation_agent():
    """Test the translation agent"""
    agent = TranslationAgent()
    
    test_queries = [
        "What is the weather today?",
        "मेरे टमाटर के पौधे में कीट लगे हैं",
        "आज बारिश होगी क्या?",
        "Cotton price in market today"
    ]
    
    for query in test_queries:
        print(f"\nOriginal: {query}")
        result = await agent.process(query)
        print(f"Language: {result['language']}")
        print(f"Translated: {result['translated_query']}")
        print(f"Confidence: {result['confidence']}")

if __name__ == "__main__":
    asyncio.run(test_translation_agent())
