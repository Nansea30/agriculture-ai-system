"""
Pest & Disease Agent - Identifies pest/disease issues and provides treatment recommendations
Uses ICAR advisories and symptom matching for diagnosis
"""

import asyncio
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class PestDiseaseAgent:
    """
    Identifies pest and disease issues based on symptoms and provides treatment recommendations
    """
    
    def __init__(self):
        # Disease database with symptoms and treatments
        self.disease_database = {
            'leaf_spot': {
                'symptoms': ['brown spots', 'yellow spots', 'circular spots', 'leaf spots'],
                'crops': ['tomato', 'potato', 'cotton', 'rice'],
                'type': 'fungal',
                'treatment': {
                    'organic': ['Neem oil spray', 'Copper fungicide', 'Remove affected leaves'],
                    'chemical': ['Mancozeb', 'Chlorothalonil', 'Propiconazole'],
                    'prevention': ['Proper spacing', 'Avoid overhead watering', 'Good air circulation']
                },
                'severity': 'moderate'
            },
            'blight': {
                'symptoms': ['wilting', 'brown patches', 'stem rot', 'leaf burn'],
                'crops': ['tomato', 'potato', 'chili', 'brinjal'],
                'type': 'fungal',
                'treatment': {
                    'organic': ['Bordeaux mixture', 'Baking soda spray', 'Destroy infected plants'],
                    'chemical': ['Metalaxyl', 'Dimethomorph', 'Cymoxanil'],
                    'prevention': ['Crop rotation', 'Resistant varieties', 'Proper drainage']
                },
                'severity': 'high'
            },
            'powdery_mildew': {
                'symptoms': ['white powder', 'dusty coating', 'leaf curling'],
                'crops': ['wheat', 'barley', 'pea', 'cucumber'],
                'type': 'fungal',
                'treatment': {
                    'organic': ['Milk spray', 'Neem oil', 'Sulfur dusting'],
                    'chemical': ['Triadimefon', 'Propiconazole', 'Tebuconazole'],
                    'prevention': ['Avoid overcrowding', 'Good air circulation', 'Resistant varieties']
                },
                'severity': 'moderate'
            },
            'root_rot': {
                'symptoms': ['yellowing', 'stunted growth', 'wilting', 'black roots'],
                'crops': ['tomato', 'chili', 'cotton', 'wheat'],
                'type': 'fungal',
                'treatment': {
                    'organic': ['Improve drainage', 'Trichoderma application', 'Neem cake'],
                    'chemical': ['Carbendazim', 'Thiophanate-methyl', 'Copper oxychloride'],
                    'prevention': ['Proper drainage', 'Avoid overwatering', 'Soil treatment']
                },
                'severity': 'high'
            },
            'rust': {
                'symptoms': ['orange spots', 'rust colored', 'pustules on leaves'],
                'crops': ['wheat', 'barley', 'coffee', 'beans'],
                'type': 'fungal',
                'treatment': {
                    'organic': ['Sulfur spray', 'Neem oil', 'Remove infected parts'],
                    'chemical': ['Propiconazole', 'Tebuconazole', 'Triadimefon'],
                    'prevention': ['Resistant varieties', 'Proper spacing', 'Avoid late planting']
                },
                'severity': 'high'
            }
        }
        
        # Pest database
        self.pest_database = {
            'aphids': {
                'symptoms': ['small insects', 'sticky honeydew', 'curled leaves', 'yellowing'],
                'crops': ['cotton', 'wheat', 'vegetables', 'fruits'],
                'type': 'insect',
                'treatment': {
                    'organic': ['Neem oil spray', 'Insecticidal soap', 'Ladybird beetles'],
                    'chemical': ['Imidacloprid', 'Acetamiprid', 'Dimethoate'],
                    'prevention': ['Regular monitoring', 'Encourage beneficial insects', 'Reflective mulch']
                },
                'severity': 'moderate'
            },
            'caterpillars': {
                'symptoms': ['holes in leaves', 'caterpillar presence', 'droppings', 'stem boring'],
                'crops': ['cotton', 'maize', 'rice', 'vegetables'],
                'type': 'insect',
                'treatment': {
                    'organic': ['Bt spray', 'Hand picking', 'Pheromone traps'],
                    'chemical': ['Chlorpyrifos', 'Cypermethrin', 'Emamectin benzoate'],
                    'prevention': ['Light traps', 'Crop rotation', 'Natural predators']
                },
                'severity': 'high'
            },
            'whitefly': {
                'symptoms': ['tiny white flies', 'yellowing leaves', 'sooty mold', 'stunted growth'],
                'crops': ['cotton', 'tomato', 'chili', 'brinjal'],
                'type': 'insect',
                'treatment': {
                    'organic': ['Yellow sticky traps', 'Neem oil', 'Reflective mulch'],
                    'chemical': ['Imidacloprid', 'Spiromesifen', 'Pyriproxyfen'],
                    'prevention': ['Regular monitoring', 'Remove weeds', 'Barrier crops']
                },
                'severity': 'moderate'
            },
            'thrips': {
                'symptoms': ['silvery patches', 'black spots', 'leaf curling', 'stunted growth'],
                'crops': ['onion', 'cotton', 'chili', 'flowers'],
                'type': 'insect',
                'treatment': {
                    'organic': ['Blue sticky traps', 'Neem oil', 'Predatory mites'],
                    'chemical': ['Fipronil', 'Spinosad', 'Acetamiprid'],
                    'prevention': ['Weed management', 'Mulching', 'Beneficial insects']
                },
                'severity': 'moderate'
            }
        }
        
        # Common symptoms mapping
        self.symptom_keywords = {
            'yellowing': ['yellow', 'yellowing', 'chlorosis'],
            'spots': ['spots', 'patches', 'lesions'],
            'wilting': ['wilting', 'drooping', 'sagging'],
            'holes': ['holes', 'eaten', 'damaged', 'torn'],
            'insects': ['bugs', 'insects', 'flies', 'worms'],
            'powder': ['powder', 'dusty', 'white coating'],
            'curling': ['curling', 'curled', 'twisted']
        }
    
    async def diagnose_pest_disease(self, context: Dict[str, Any]) -> 'QueryResponse':
        """
        Diagnose pest/disease issues based on symptoms described in query
        """
        from main import QueryResponse, QueryCategory
        
        try:
            query = context.get('query', '').lower()
            location = context.get('location', '')
            
            # Extract crop and symptoms from query
            crop = self.extract_crop(query)
            symptoms = self.extract_symptoms(query)
            
            if not symptoms:
                return QueryResponse(
                    category=QueryCategory.PEST_DISEASE,
                    response="Please describe the symptoms you're observing (e.g., yellow leaves, spots, holes, wilting, insects) for accurate diagnosis.",
                    language='en',
                    source="pest_disease_agent",
                    confidence=0.0
                )
            
            # Find matching diseases and pests
            disease_matches = self.match_diseases(symptoms, crop)
            pest_matches = self.match_pests(symptoms, crop)
            
            # Combine and rank matches
            all_matches = disease_matches + pest_matches
            
            if not all_matches:
                return QueryResponse(
                    category=QueryCategory.PEST_DISEASE,
                    response="No reliable diagnosis found for the described symptoms. Please consult your local plant pathologist or agriculture extension officer for proper identification.",
                    language='en',
                    source="icar_advisories",
                    confidence=0.0
                )
            
            # Sort by match score
            all_matches.sort(key=lambda x: x['score'], reverse=True)
            
            # Format diagnosis and treatment recommendations
            response = self.format_diagnosis_response(all_matches[:2], crop)  # Top 2 matches
            
            return QueryResponse(
                category=QueryCategory.PEST_DISEASE,
                response=response,
                language='en',
                source="icar_advisories",
                confidence=min(all_matches[0]['score'] / 3.0, 0.9),  # Scale confidence
                data={'matches': all_matches[:2]}
            )
            
        except Exception as e:
            logger.error(f"Pest/disease diagnosis error: {str(e)}")
            return QueryResponse(
                category=QueryCategory.PEST_DISEASE,
                response="Unable to provide pest/disease diagnosis at the moment. Please consult your local agriculture extension officer.",
                language='en',
                source="pest_agent_error",
                confidence=0.0
            )
    
    def extract_crop(self, query: str) -> Optional[str]:
        """Extract crop information from query"""
        # Get all crops from both databases
        all_crops = set()
        for disease_info in self.disease_database.values():
            all_crops.update(disease_info['crops'])
        for pest_info in self.pest_database.values():
            all_crops.update(pest_info['crops'])
        
        for crop in all_crops:
            if crop in query:
                return crop
        return None
    
    def extract_symptoms(self, query: str) -> List[str]:
        """Extract symptoms from query text"""
        symptoms = []
        
        for symptom_category, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    symptoms.append(symptom_category)
                    break
        
        # Also look for direct symptom mentions
        direct_symptoms = [
            'brown spots', 'yellow spots', 'white spots', 'black spots',
            'holes', 'wilting', 'yellowing', 'curling', 'stunted',
            'powder', 'mold', 'rot', 'rust', 'blight'
        ]
        
        for symptom in direct_symptoms:
            if symptom in query:
                symptoms.append(symptom)
        
        return list(set(symptoms))  # Remove duplicates
    
    def match_diseases(self, symptoms: List[str], crop: Optional[str]) -> List[Dict[str, Any]]:
        """Match symptoms to possible diseases"""
        matches = []
        
        for disease_name, disease_info in self.disease_database.items():
            score = 0
            
            # Check symptom matches
            for symptom in symptoms:
                if any(symptom in disease_symptom for disease_symptom in disease_info['symptoms']):
                    score += 2
                elif symptom in ' '.join(disease_info['symptoms']):
                    score += 1
            
            # Check crop compatibility
            if crop and crop in disease_info['crops']:
                score += 1
            elif not crop:
                score += 0.5  # Slight bonus if no crop specified
            
            if score > 0:
                matches.append({
                    'name': disease_name,
                    'type': 'disease',
                    'info': disease_info,
                    'score': score
                })
        
        return matches
    
    def match_pests(self, symptoms: List[str], crop: Optional[str]) -> List[Dict[str, Any]]:
        """Match symptoms to possible pests"""
        matches = []
        
        for pest_name, pest_info in self.pest_database.items():
            score = 0
            
            # Check symptom matches
            for symptom in symptoms:
                if any(symptom in pest_symptom for pest_symptom in pest_info['symptoms']):
                    score += 2
                elif symptom in ' '.join(pest_info['symptoms']):
                    score += 1
            
            # Check crop compatibility
            if crop and crop in pest_info['crops']:
                score += 1
            elif not crop:
                score += 0.5
            
            if score > 0:
                matches.append({
                    'name': pest_name,
                    'type': 'pest',
                    'info': pest_info,
                    'score': score
                })
        
        return matches
    
    def format_diagnosis_response(self, matches: List[Dict[str, Any]], crop: Optional[str]) -> str:
        """Format the diagnosis and treatment response"""
        if not matches:
            return "No diagnosis could be made based on the provided information."
        
        response = "🔍 Possible Diagnosis:\n\n"
        
        for i, match in enumerate(matches, 1):
            name = match['name'].replace('_', ' ').title()
            match_type = match['type'].title()
            info = match['info']
            severity = info['severity'].title()
            
            response += f"{i}. **{name}** ({match_type})\n"
            response += f"   Severity: {severity}\n"
            response += f"   Type: {info['type'].title()}\n"
            
            # Add symptoms
            response += f"   Common Symptoms: {', '.join(info['symptoms'][:3])}\n"
            
            # Add treatment recommendations
            response += f"\n   🌿 Organic Treatment:\n"
            for treatment in info['treatment']['organic'][:2]:
                response += f"   • {treatment}\n"
            
            response += f"\n   🧪 Chemical Treatment:\n"
            for treatment in info['treatment']['chemical'][:2]:
                response += f"   • {treatment}\n"
            
            response += f"\n   🛡️ Prevention:\n"
            for prevention in info['treatment']['prevention'][:2]:
                response += f"   • {prevention}\n"
            
            response += "\n"
        
        # Add general advice
        response += "⚠️ Important Notes:\n"
        response += "• Always read pesticide labels before application\n"
        response += "• Follow recommended dosage and safety precautions\n"
        response += "• Consult local agriculture extension officer for confirmation\n"
        response += "• Consider integrated pest management (IPM) practices\n"
        
        return response

# Example usage
async def test_pest_agent():
    """Test the pest and disease agent"""
    agent = PestDiseaseAgent()
    
    test_contexts = [
        {'query': 'my tomato plants have yellow leaves with brown spots', 'location': 'Karnataka'},
        {'query': 'cotton crop has small white insects and curled leaves', 'location': 'Gujarat'},
        {'query': 'wheat crop has orange rust colored spots', 'location': 'Punjab'},
        {'query': 'holes in maize leaves and caterpillars present', 'location': 'Maharashtra'}
    ]
    
    for context in test_contexts:
        print(f"\nTesting: {context}")
        response = await agent.diagnose_pest_disease(context)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")

if __name__ == "__main__":
    asyncio.run(test_pest_agent())
