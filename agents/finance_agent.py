"""
Finance & Policy Agent - Provides information about government schemes, subsidies,
loans, insurance, and agricultural policies
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FinancePolicyAgent:
    """
    Provides information about agricultural finance schemes and government policies
    """
    
    def __init__(self):
        # Government schemes database
        self.schemes_database = {
            'pm_kisan': {
                'full_name': 'Pradhan Mantri Kisan Samman Nidhi',
                'type': 'direct_benefit',
                'amount': '6000 per year',
                'eligibility': [
                    'All landholding farmers',
                    'Small and marginal farmers',
                    'Must have valid Aadhaar card',
                    'Bank account linked to Aadhaar'
                ],
                'benefits': [
                    '₹2000 every 4 months (3 installments per year)',
                    'Direct cash transfer to bank account',
                    'No need to visit bank or office'
                ],
                'application_process': [
                    'Visit PM Kisan portal or CSC center',
                    'Fill application with Aadhaar, bank details',
                    'Upload land documents',
                    'Submit and track status online'
                ],
                'documents': ['Aadhaar card', 'Bank account details', 'Land ownership documents'],
                'website': 'pmkisan.gov.in'
            },
            'fasal_bima': {
                'full_name': 'Pradhan Mantri Fasal Bima Yojana',
                'type': 'crop_insurance',
                'amount': 'Up to sum insured',
                'eligibility': [
                    'All farmers (sharecroppers and tenant farmers included)',
                    'Must have insurable interest in crop',
                    'Voluntary for non-loanee farmers'
                ],
                'benefits': [
                    'Coverage against natural disasters',
                    'Low premium rates (1.5-5% of sum insured)',
                    'Quick settlement of claims',
                    'Post-harvest losses coverage'
                ],
                'application_process': [
                    'Contact bank, insurance company or CSC',
                    'Fill application form',
                    'Pay premium amount',
                    'Get insurance certificate'
                ],
                'documents': ['Aadhaar card', 'Bank account details', 'Land records', 'Sowing certificate'],
                'website': 'pmfby.gov.in'
            },
            'kisan_credit_card': {
                'full_name': 'Kisan Credit Card',
                'type': 'credit_facility',
                'amount': 'Based on land holding and crops',
                'eligibility': [
                    'All farmers (owner cultivators)',
                    'Tenant farmers and sharecroppers',
                    'Self Help Group members'
                ],
                'benefits': [
                    'Easy access to credit at low interest rates',
                    'Flexible repayment schedule',
                    'No collateral required for small loans',
                    'Insurance coverage included'
                ],
                'application_process': [
                    'Visit nearest bank branch',
                    'Fill KCC application form',
                    'Submit required documents',
                    'Bank verification and approval'
                ],
                'documents': ['Identity proof', 'Address proof', 'Land documents', 'Income certificate'],
                'website': 'agriculture.gov.in'
            },
            'soil_health_card': {
                'full_name': 'Soil Health Card Scheme',
                'type': 'advisory_service',
                'amount': 'Free of cost',
                'eligibility': [
                    'All farmers',
                    'Individual or group applications'
                ],
                'benefits': [
                    'Free soil testing',
                    'Fertilizer recommendations',
                    'Soil health status report',
                    'Improves crop productivity'
                ],
                'application_process': [
                    'Contact local agriculture department',
                    'Provide soil samples',
                    'Get soil health card within 2 weeks'
                ],
                'documents': ['Identity proof', 'Land documents'],
                'website': 'soilhealth.dac.gov.in'
            },
            'msps': {
                'full_name': 'Minimum Support Price',
                'type': 'price_support',
                'amount': 'Varies by crop and season',
                'eligibility': [
                    'All farmers',
                    'Registered with procurement agencies'
                ],
                'benefits': [
                    'Guaranteed minimum price for produce',
                    'Protection against market fluctuations',
                    'Direct purchase by government agencies'
                ],
                'application_process': [
                    'Register with local procurement center',
                    'Bring produce during procurement season',
                    'Get payment as per MSP rates'
                ],
                'documents': ['Identity proof', 'Land documents', 'Produce quality certificate'],
                'website': 'cacp.dacnet.nic.in'
            },
            'pm_kusum': {
                'full_name': 'PM Kisan Urja Suraksha evam Utthaan Mahabhiyan',
                'type': 'solar_subsidy',
                'amount': '60% central subsidy + 30% state subsidy',
                'eligibility': [
                    'All farmers and farmer groups',
                    'Cooperative societies',
                    'Panchayats and FPOs'
                ],
                'benefits': [
                    'Solar pump installation subsidy',
                    'Grid-connected solar power plants',
                    'Solarization of existing pumps',
                    'Additional income from power sale'
                ],
                'application_process': [
                    'Apply through state nodal agency',
                    'Technical feasibility assessment',
                    'Installation by empaneled vendors',
                    'Subsidy disbursement after completion'
                ],
                'documents': ['Identity proof', 'Land documents', 'Electricity connection details'],
                'website': 'pmkusum.mnre.gov.in'
            }
        }
        
        # Keywords for scheme matching
        self.scheme_keywords = {
            'pm_kisan': ['pm kisan', 'kisan samman', 'direct benefit', 'cash transfer', '6000'],
            'fasal_bima': ['crop insurance', 'fasal bima', 'insurance', 'natural disaster'],
            'kisan_credit_card': ['kcc', 'credit card', 'loan', 'credit facility'],
            'soil_health_card': ['soil health', 'soil test', 'fertilizer recommendation'],
            'msps': ['msp', 'minimum support price', 'procurement'],
            'pm_kusum': ['solar', 'kusum', 'solar pump', 'renewable energy']
        }
        
        # Current MSP rates (example data - should be updated regularly)
        self.current_msp = {
            'wheat': 2125,
            'rice': 2040,
            'cotton': 6080,
            'sugarcane': 315,
            'maize': 1962,
            'bajra': 2500,
            'jowar': 3180
        }
    
    async def get_policy_info(self, context: Dict[str, Any]) -> 'QueryResponse':
        """
        Get information about government schemes and policies
        """
        from main import QueryResponse, QueryCategory
        
        try:
            query = context.get('query', '').lower()
            location = context.get('location', '')
            
            # Check if query is about a specific scheme
            specific_scheme = self.extract_scheme(query)
            
            if specific_scheme:
                response = self.get_scheme_details(specific_scheme)
                confidence = 0.9
            elif 'msp' in query or 'minimum support price' in query:
                crop = self.extract_crop_for_msp(query)
                response = self.get_msp_info(crop)
                confidence = 0.8
            elif any(keyword in query for keyword in ['loan', 'credit', 'bank']):
                response = self.get_credit_schemes_info()
                confidence = 0.7
            elif any(keyword in query for keyword in ['insurance', 'bima']):
                response = self.get_insurance_schemes_info()
                confidence = 0.7
            elif any(keyword in query for keyword in ['subsidy', 'scheme', 'government']):
                response = self.get_general_schemes_info()
                confidence = 0.6
            else:
                response = self.get_comprehensive_policy_info()
                confidence = 0.5
            
            return QueryResponse(
                category=QueryCategory.FINANCE_POLICY,
                response=response,
                language='en',
                source="india.gov.in",
                confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"Policy information error: {str(e)}")
            return QueryResponse(
                category=QueryCategory.FINANCE_POLICY,
                response="Unable to provide policy information at the moment. Please visit your local agriculture office or check india.gov.in for current schemes.",
                language='en',
                source="finance_agent_error",
                confidence=0.0
            )
    
    def extract_scheme(self, query: str) -> Optional[str]:
        """Extract specific scheme name from query"""
        for scheme_id, keywords in self.scheme_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return scheme_id
        return None
    
    def extract_crop_for_msp(self, query: str) -> Optional[str]:
        """Extract crop name for MSP queries"""
        for crop in self.current_msp.keys():
            if crop in query:
                return crop
        return None
    
    def get_scheme_details(self, scheme_id: str) -> str:
        """Get detailed information about a specific scheme"""
        if scheme_id not in self.schemes_database:
            return f"Detailed information not available for the requested scheme."
        
        scheme = self.schemes_database[scheme_id]
        
        response = f"🏛️ {scheme['full_name']}\n\n"
        response += f"Type: {scheme['type'].replace('_', ' ').title()}\n"
        response += f"Benefit Amount: {scheme['amount']}\n\n"
        
        response += "✅ Eligibility Criteria:\n"
        for criterion in scheme['eligibility']:
            response += f"• {criterion}\n"
        
        response += "\n💰 Benefits:\n"
        for benefit in scheme['benefits']:
            response += f"• {benefit}\n"
        
        response += "\n📝 Application Process:\n"
        for step in scheme['application_process']:
            response += f"• {step}\n"
        
        response += "\n📋 Required Documents:\n"
        for doc in scheme['documents']:
            response += f"• {doc}\n"
        
        response += f"\n🌐 Official Website: {scheme['website']}\n"
        response += "\n💡 Tip: Contact your local agriculture extension officer for assistance with application."
        
        return response
    
    def get_msp_info(self, crop: Optional[str]) -> str:
        """Get MSP information for crops"""
        response = "💰 Minimum Support Price (MSP) Information:\n\n"
        
        if crop and crop in self.current_msp:
            msp_rate = self.current_msp[crop]
            response += f"{crop.title()} MSP: ₹{msp_rate} per quintal\n\n"
            response += "📍 Where to sell at MSP:\n"
            response += "• Government procurement centers\n"
            response += "• Cooperative societies\n"
            response += "• FCI (Food Corporation of India) centers\n"
            response += "• State agencies\n\n"
        else:
            response += "Current MSP Rates (2024-25):\n"
            for crop_name, rate in self.current_msp.items():
                response += f"• {crop_name.title()}: ₹{rate} per quintal\n"
            response += "\n"
        
        response += "ℹ️ Important Information:\n"
        response += "• MSP is announced by Government of India\n"
        response += "• Procurement is done through registered centers\n"
        response += "• Quality standards must be met\n"
        response += "• Bring proper documentation for sale\n"
        
        return response
    
    def get_credit_schemes_info(self) -> str:
        """Get information about agricultural credit schemes"""
        response = "🏦 Agricultural Credit Schemes:\n\n"
        
        # KCC information
        kcc_scheme = self.schemes_database['kisan_credit_card']
        response += f"1. **{kcc_scheme['full_name']}**\n"
        response += f"• Credit limit based on land holding\n"
        response += f"• Interest rate: 7% (with 3% subvention)\n"
        response += f"• Additional 3% interest subvention for timely repayment\n"
        response += f"• Website: {kcc_scheme['website']}\n\n"
        
        response += "2. **Other Credit Sources:**\n"
        response += "• Cooperative banks and societies\n"
        response += "• Regional Rural Banks (RRBs)\n"
        response += "• Commercial banks\n"
        response += "• Microfinance institutions\n\n"
        
        response += "📋 General Requirements:\n"
        response += "• Valid identity and address proof\n"
        response += "• Land ownership/cultivation documents\n"
        response += "• Income certificate\n"
        response += "• Bank account (preferably in the same bank)\n"
        
        return response
    
    def get_insurance_schemes_info(self) -> str:
        """Get information about agricultural insurance schemes"""
        response = "🛡️ Agricultural Insurance Schemes:\n\n"
        
        # PMFBY information
        pmfby_scheme = self.schemes_database['fasal_bima']
        response += f"1. **{pmfby_scheme['full_name']} (PMFBY)**\n"
        response += "• Premium rates: Kharif 2%, Rabi 1.5%, Commercial crops 5%\n"
        response += "• Coverage: All stages from pre-sowing to post-harvest\n"
        response += "• Claims settled based on Crop Cutting Experiments (CCE)\n"
        response += f"• Website: {pmfby_scheme['website']}\n\n"
        
        response += "2. **Other Insurance Options:**\n"
        response += "• Weather-based Crop Insurance Scheme (WBCIS)\n"
        response += "• Coconut Palm Insurance Scheme (CPIS)\n"
        response += "• Unified Package Insurance Scheme (UPIS)\n\n"
        
        response += "⏰ Important Deadlines:\n"
        response += "• Kharif: Apply before July 31st\n"
        response += "• Rabi: Apply before December 31st\n"
        response += "• Commercial crops: Before last date of sowing\n"
        
        return response
    
    def get_general_schemes_info(self) -> str:
        """Get overview of major agricultural schemes"""
        response = "🌾 Major Agricultural Schemes Overview:\n\n"
        
        response += "1. **Direct Benefits:**\n"
        response += f"• {self.schemes_database['pm_kisan']['full_name']} - ₹6000/year\n\n"
        
        response += "2. **Credit & Insurance:**\n"
        response += f"• {self.schemes_database['kisan_credit_card']['full_name']}\n"
        response += f"• {self.schemes_database['fasal_bima']['full_name']}\n\n"
        
        response += "3. **Technology & Infrastructure:**\n"
        response += f"• {self.schemes_database['pm_kusum']['full_name']} (Solar)\n"
        response += f"• {self.schemes_database['soil_health_card']['full_name']}\n\n"
        
        response += "4. **Price Support:**\n"
        response += "• Minimum Support Price (MSP) for 23 crops\n"
        response += "• Market intervention schemes\n\n"
        
        response += "📞 For More Information:\n"
        response += "• Visit local agriculture office\n"
        response += "• Call Kisan Call Center: 1800-180-1551\n"
        response += "• Check ministry websites: agriculture.gov.in\n"
        
        return response
    
    def get_comprehensive_policy_info(self) -> str:
        """Get comprehensive agricultural policy information"""
        response = "📊 Agricultural Policy & Finance Overview:\n\n"
        
        response += "💰 **Financial Support Available:**\n"
        response += "• Direct cash transfers (PM-Kisan)\n"
        response += "• Subsidized credit (KCC)\n"
        response += "• Crop insurance (PMFBY)\n"
        response += "• Input subsidies (fertilizers, seeds)\n"
        response += "• Equipment subsidies\n\n"
        
        response += "🏛️ **Key Government Initiatives:**\n"
        response += "• Doubling farmers' income by 2024\n"
        response += "• Digital agriculture mission\n"
        response += "• Formation of Farmer Producer Organizations (FPOs)\n"
        response += "• e-NAM (electronic National Agriculture Market)\n\n"
        
        response += "📱 **Digital Services:**\n"
        response += "• PM Kisan mobile app\n"
        response += "• Crop insurance app\n"
        response += "• e-NAM platform for online trading\n"
        response += "• Kisan Suvidha app for advisory services\n\n"
        
        response += "ℹ️ **Important Contact Numbers:**\n"
        response += "• Kisan Call Center: 1800-180-1551\n"
        response += "• PM Kisan Helpline: 155261\n"
        response += "• Soil Health Card: 1800-180-1551\n"
        
        return response

# Example usage
async def test_finance_agent():
    """Test the finance and policy agent"""
    agent = FinancePolicyAgent()
    
    test_contexts = [
        {'query': 'pm kisan scheme details', 'location': 'Maharashtra'},
        {'query': 'crop insurance information', 'location': 'Punjab'},
        {'query': 'kisan credit card eligibility', 'location': 'Karnataka'},
        {'query': 'wheat msp current rate', 'location': 'Haryana'},
        {'query': 'government subsidy schemes', 'location': 'Uttar Pradesh'}
    ]
    
    for context in test_contexts:
        print(f"\nTesting: {context}")
        response = await agent.get_policy_info(context)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")

if __name__ == "__main__":
    asyncio.run(test_finance_agent())
