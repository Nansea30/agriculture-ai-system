#!/usr/bin/env python3
"""
Demo CLI Interface for Agriculture AI System
Test the multi-agent system with various farmer queries
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ManagerAgent

class DemoCLI:
    """
    Simple CLI interface for demonstrating the Agriculture AI System
    """
    
    def __init__(self):
        self.manager = ManagerAgent()
        self.session_start = datetime.now()
    
    def print_banner(self):
        """Print system banner"""
        print("="*70)
        print("🌾 AGRICULTURE AI SYSTEM - MULTI-AGENT DEMO 🌾")
        print("="*70)
        print("Welcome to the AI-powered agriculture decision support system!")
        print("This system can help with:")
        print("• Weather forecasts and alerts")
        print("• Crop recommendations")
        print("• Market prices")
        print("• Irrigation guidance")
        print("• Pest & disease diagnosis")
        print("• Government schemes & policies")
        print()
        print("Available in multiple languages (Hindi/English)")
        print("Type 'help' for examples, 'quit' to exit")
        print("="*70)
        print()
    
    def print_help(self):
        """Print help and example queries"""
        print("📚 EXAMPLE QUERIES:")
        print()
        print("🌤️  Weather:")
        print("   • What is the weather forecast for Delhi?")
        print("   • Will it rain tomorrow in Mumbai?")
        print()
        print("🌾 Crop Recommendations:")
        print("   • Which crop should I grow in kharif season?")
        print("   • Rice cultivation guide")
        print("   • Best crop for clay soil")
        print()
        print("💰 Market Prices:")
        print("   • Current wheat price in Punjab")
        print("   • Cotton rate today")
        print()
        print("💧 Irrigation:")
        print("   • When to irrigate wheat crop?")
        print("   • Water requirement for tomato")
        print("   • Drip irrigation benefits")
        print()
        print("🐛 Pest & Disease:")
        print("   • My tomato plants have yellow leaves")
        print("   • मेरे पौधे में कीट लगे हैं (Hindi)")
        print("   • Cotton crop has white insects")
        print()
        print("🏛️  Government Schemes:")
        print("   • PM Kisan scheme details")
        print("   • Crop insurance information")
        print("   • KCC loan eligibility")
        print()
        print("Type your query in English or Hindi...")
        print("-"*50)
        print()
    
    def format_response(self, response):
        """Format the response for better display"""
        print("🤖 AI Assistant Response:")
        print("─" * 50)
        print(response.response)
        print()
        
        # Show metadata
        print(f"📊 Confidence: {response.confidence:.1%}")
        print(f"📂 Category: {response.category.value}")
        print(f"🔍 Source: {response.source}")
        if response.language != 'en':
            print(f"🌐 Language: {response.language}")
        print("─" * 50)
        print()
    
    async def process_query(self, query, location=None):
        """Process a user query"""
        print(f"🔄 Processing query: '{query}'")
        if location:
            print(f"📍 Location: {location}")
        print()
        
        try:
            response = await self.manager.process_query(query, location)
            self.format_response(response)
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please try again or contact support.")
            print()
    
    def get_user_input(self):
        """Get user input with location"""
        try:
            query = input("🌾 Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                return None, None
            
            if query.lower() in ['help', 'h']:
                self.print_help()
                return 'help', None
            
            # Ask for location if not obvious from query
            location_keywords = ['delhi', 'mumbai', 'pune', 'bangalore', 'chennai', 'kolkata', 
                               'hyderabad', 'ahmedabad', 'punjab', 'haryana', 'uttar pradesh',
                               'maharashtra', 'karnataka', 'tamil nadu', 'west bengal', 'gujarat']
            
            has_location = any(keyword in query.lower() for keyword in location_keywords)
            
            if not has_location:
                location = input("📍 Location (optional, press Enter to skip): ").strip()
                location = location if location else None
            else:
                location = None
            
            return query, location
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thank you for using Agriculture AI System.")
            return None, None
        except Exception as e:
            print(f"❌ Input error: {str(e)}")
            return 'error', None
    
    async def run_demo(self):
        """Run the interactive demo"""
        self.print_banner()
        
        # Show some sample queries automatically
        print("🚀 Let me demonstrate with some sample queries first:\n")
        
        sample_queries = [
            ("What is the weather in Delhi?", "Delhi"),
            ("Which crop is best for kharif season?", "Punjab"),
            ("मेरे टमाटर के पौधे में पीली पत्तियां हैं", "Maharashtra")
        ]
        
        for query, location in sample_queries:
            await self.process_query(query, location)
            await asyncio.sleep(1)  # Small delay for better UX
        
        print("🎯 Now you can ask your own questions!\n")
        self.print_help()
        
        # Interactive loop
        while True:
            query, location = self.get_user_input()
            
            if query is None:  # User wants to quit
                break
            
            if query == 'help':  # Help command
                continue
            
            if query == 'error':  # Input error
                continue
            
            await self.process_query(query, location)
        
        # Show session summary
        session_duration = datetime.now() - self.session_start
        print(f"📊 Session duration: {session_duration}")
        print("👋 Thank you for using the Agriculture AI System!")
        print("For more information, visit your local Krishi Vigyan Kendra.")

async def main():
    """Main demo function"""
    demo = DemoCLI()
    await demo.run_demo()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        print("Please check your installation and try again.")
