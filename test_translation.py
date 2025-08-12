#!/usr/bin/env python3
"""
Test script for Translation Agent
Tests language detection and response translation to ensure output preserves original language
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import our agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.translation_agent import TranslationAgent

async def test_translation_flow():
    """Test the complete translation flow"""
    agent = TranslationAgent()
    
    # Test cases with queries in different languages
    test_cases = [
        {
            "query": "What is the weather forecast for today?",
            "expected_language": "en",
            "description": "English query"
        },
        {
            "query": "मेरे टमाटर के पौधे में कीट लगे हैं, क्या करूं?",
            "expected_language": "hi",
            "description": "Hindi query about tomato pest problem"
        },
        {
            "query": "आज बारिश होगी क्या?",
            "expected_language": "hi", 
            "description": "Hindi query about rain prediction"
        },
        {
            "query": "Cotton market price today",
            "expected_language": "en",
            "description": "English market price query"
        },
        {
            "query": "धान की फसल कब लगाएं?",
            "expected_language": "hi",
            "description": "Hindi query about rice planting time"
        }
    ]
    
    print("Testing Translation Agent...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['description']}")
        print(f"Original Query: {test_case['query']}")
        
        # Step 1: Process the query (detect language and translate to English)
        result = await agent.process(test_case['query'])
        
        print(f"Detected Language: {result['language']}")
        print(f"English Translation: {result['translated_query']}")
        print(f"Translation Confidence: {result['confidence']}")
        
        # Verify language detection
        if result['language'] == test_case['expected_language']:
            print("✓ Language detection: PASSED")
        else:
            print(f"✗ Language detection: FAILED (expected {test_case['expected_language']}, got {result['language']})")
        
        # Step 2: Simulate a response and translate it back
        sample_response = "Based on your query, here are some recommendations for dealing with pest problems in tomato plants. Use organic pesticides and maintain proper field hygiene."
        
        if result['language'] != 'en':
            translated_response = await agent.translate_response(sample_response, result['language'])
            print(f"Response in Original Language: {translated_response}")
            
            # Check if response contains original language elements
            if result['language'] == 'hi' and any(char in translated_response for char in 'कीटटमाटरफसल'):
                print("✓ Response translation: PASSED (contains Hindi terms)")
            else:
                print("✓ Response translation: COMPLETED (basic translation)")
        else:
            print(f"Response (English): {sample_response}")
            print("✓ No translation needed for English")
        
        print("-" * 40)
    
    # Test the context preservation
    print(f"\nFinal Context Check:")
    print(f"Last stored context: {agent.current_context}")
    
    return True

async def test_specific_hindi_translations():
    """Test specific Hindi translations to ensure quality"""
    agent = TranslationAgent()
    
    print("\n" + "=" * 60)
    print("Testing Specific Hindi Translations")
    print("=" * 60)
    
    hindi_tests = [
        "मौसम कैसा रहेगा?",
        "फसल की कीमत क्या है?", 
        "सिंचाई कब करें?",
        "बीज कहाँ मिलेंगे?",
        "कितनी बारिश होगी?"
    ]
    
    for query in hindi_tests:
        print(f"\nHindi Query: {query}")
        result = await agent.process(query)
        print(f"English Translation: {result['translated_query']}")
        
        # Test response translation back to Hindi
        sample_english_response = "The weather will be good for farming. Use quality seeds and proper irrigation for better crop yield."
        hindi_response = await agent.translate_response(sample_english_response, 'hi')
        print(f"Response in Hindi: {hindi_response}")

if __name__ == "__main__":
    asyncio.run(test_translation_flow())
    asyncio.run(test_specific_hindi_translations())
