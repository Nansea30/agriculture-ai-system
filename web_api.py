#!/usr/bin/env python3
"""
Web API for Agriculture AI System
Simple HTTP server for web-based access
"""

import asyncio
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ManagerAgent

class AgricultureAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Agriculture AI API"""
    
    def __init__(self, *args, **kwargs):
        # Initialize manager agent
        if not hasattr(AgricultureAPIHandler, 'manager'):
            AgricultureAPIHandler.manager = ManagerAgent()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_index_page()
        elif self.path == '/api/health':
            self.send_json_response({'status': 'healthy', 'message': 'Agriculture AI System is running'})
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/query':
            self.handle_query_request()
        else:
            self.send_404()
    
    def handle_query_request(self):
        """Handle agriculture query requests"""
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract query and location
            query = data.get('query', '')
            location = data.get('location', None)
            
            if not query:
                self.send_json_response({'error': 'Query is required'}, status=400)
                return
            
            # Process query using asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response = loop.run_until_complete(
                    self.manager.process_query(query, location)
                )
                
                # Convert response to JSON
                result = {
                    'query': query,
                    'location': location,
                    'response': response.response,
                    'category': response.category.value,
                    'language': response.language,
                    'source': response.source,
                    'confidence': response.confidence
                }
                
                self.send_json_response(result)
                
            finally:
                loop.close()
                
        except json.JSONDecodeError:
            self.send_json_response({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)
    
    def serve_index_page(self):
        """Serve the main HTML page"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌾 Agriculture AI System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .voice-controls {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-top: 10px;
        }
        .voice-btn {
            background-color: #FF6B6B;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .voice-btn:hover {
            background-color: #FF5252;
            transform: scale(1.05);
        }
        .voice-btn.listening {
            background-color: #4CAF50;
            animation: pulse 1.5s infinite;
        }
        .voice-btn.speaking {
            background-color: #2196F3;
            animation: pulse 1.5s infinite;
        }
        .voice-btn:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
            transform: none;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .voice-status {
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .voice-status.listening {
            background-color: #E8F5E8;
            color: #4CAF50;
        }
        .voice-status.processing {
            background-color: #E3F2FD;
            color: #2196F3;
        }
        .voice-status.error {
            background-color: #FFEBEE;
            color: #F44336;
        }
        .language-selector {
            display: flex;
            gap: 5px;
            align-items: center;
            margin-left: 10px;
        }
        .language-selector select {
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 15px;
            background-color: white;
            font-size: 12px;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .query-form {
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        textarea {
            height: 80px;
            resize: vertical;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .response-area {
            background-color: #f9f9f9;
            border: 2px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-top: 20px;
            min-height: 100px;
        }
        .loading {
            text-align: center;
            color: #666;
        }
        .response-content {
            white-space: pre-wrap;
            line-height: 1.6;
        }
        .metadata {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
        }
        .examples {
            background-color: #e8f5e8;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .examples h3 {
            margin-top: 0;
            color: #2d5a2d;
        }
        .examples ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .examples li {
            margin-bottom: 5px;
            cursor: pointer;
            color: #4CAF50;
        }
        .examples li:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌾 Agriculture AI System</h1>
        <p>AI-Powered Decision Support for Indian Farmers</p>
        <p><strong>Multilingual • Real-time • Reliable</strong></p>
    </div>
    
    <div class="container">
        <div class="examples">
            <h3>📚 Example Queries (Click to try):</h3>
            <strong>🌤️ Weather:</strong>
            <ul>
                <li onclick="setQuery('What is the weather forecast for Delhi?', 'Delhi')">What is the weather forecast for Delhi?</li>
                <li onclick="setQuery('Will it rain tomorrow in Mumbai?', 'Mumbai')">Will it rain tomorrow in Mumbai?</li>
            </ul>
            
            <strong>🌾 Crop Recommendations:</strong>
            <ul>
                <li onclick="setQuery('Which crop should I grow in kharif season?', 'Punjab')">Which crop should I grow in kharif season?</li>
                <li onclick="setQuery('Rice cultivation guide', 'West Bengal')">Rice cultivation guide</li>
            </ul>
            
            <strong>💰 Market Prices:</strong>
            <ul>
                <li onclick="setQuery('Current wheat price in Punjab', 'Punjab')">Current wheat price in Punjab</li>
                <li onclick="setQuery('Cotton rate today', 'Gujarat')">Cotton rate today</li>
            </ul>
            
            <strong>🐛 Pest & Disease:</strong>
            <ul>
                <li onclick="setQuery('My tomato plants have yellow leaves with brown spots', 'Maharashtra')">My tomato plants have yellow leaves with brown spots</li>
                <li onclick="setQuery('मेरे पौधे में कीट लगे हैं', 'Maharashtra')">मेरे पौधे में कीट लगे हैं (Hindi)</li>
            </ul>
            
            <strong>🏛️ Government Schemes:</strong>
            <ul>
                <li onclick="setQuery('PM Kisan scheme details', '')">PM Kisan scheme details</li>
                <li onclick="setQuery('Crop insurance information', '')">Crop insurance information</li>
            </ul>
        </div>
        
        <form class="query-form" onsubmit="submitQuery(event)">
            <div class="input-group">
                <label for="query">Your Agriculture Query:</label>
                <textarea id="query" name="query" placeholder="Ask about weather, crops, prices, irrigation, pests, or government schemes... (English/Hindi supported)" required></textarea>
                <div class="voice-controls">
                    <button type="button" id="voiceBtn" class="voice-btn" onclick="toggleVoiceRecognition()">
                        🎤 <span id="voiceBtnText">Start Voice</span>
                    </button>
                    <button type="button" id="speakBtn" class="voice-btn" onclick="speakResponse()" style="display: none;">
                        🔊 <span>Speak Answer</span>
                    </button>
                    <div id="voiceStatus" class="voice-status" style="display: none;"></div>
                    <div class="language-selector">
                        <label for="voiceLang">Voice:</label>
                        <select id="voiceLang" onchange="updateVoiceLanguage()">
                            <option value="en-US">English</option>
                            <option value="hi-IN">हिन्दी</option>
                            <option value="mr-IN">मराठी</option>
                            <option value="bn-IN">বাংলা</option>
                            <option value="te-IN">తెలుగు</option>
                            <option value="ta-IN">தமிழ்</option>
                            <option value="gu-IN">ગુજરાતી</option>
                            <option value="kn-IN">ಕನ್ನಡ</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="input-group">
                <label for="location">Location (Optional):</label>
                <input type="text" id="location" name="location" placeholder="e.g., Delhi, Mumbai, Punjab, Maharashtra...">
            </div>
            
            <button type="submit" id="submitBtn">🚀 Get AI Advice</button>
        </form>
        
        <div id="response" class="response-area" style="display: none;">
            <div id="responseContent"></div>
        </div>
    </div>

    <script>
        // Voice Recognition Variables
        let recognition;
        let isListening = false;
        let speechSynthesis = window.speechSynthesis;
        let currentUtterance = null;
        let lastResponse = '';
        let currentVoiceLang = 'en-US';

        // Initialize Speech Recognition
        function initSpeechRecognition() {
            if ('webkitSpeechRecognition' in window) {
                recognition = new webkitSpeechRecognition();
            } else if ('SpeechRecognition' in window) {
                recognition = new SpeechRecognition();
            } else {
                console.log('Speech recognition not supported');
                document.getElementById('voiceBtn').style.display = 'none';
                return false;
            }
            
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = currentVoiceLang;
            
            recognition.onstart = function() {
                isListening = true;
                updateVoiceButton('listening');
                showVoiceStatus('🎤 Listening...', 'listening');
            };
            
            recognition.onresult = function(event) {
                let finalTranscript = '';
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                if (finalTranscript) {
                    document.getElementById('query').value = finalTranscript;
                    showVoiceStatus('✓ Voice captured!', 'processing');
                    setTimeout(() => hideVoiceStatus(), 2000);
                } else if (interimTranscript) {
                    document.getElementById('query').value = interimTranscript;
                }
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                let errorMsg = 'Voice recognition error';
                switch(event.error) {
                    case 'no-speech':
                        errorMsg = 'No speech detected';
                        break;
                    case 'network':
                        errorMsg = 'Network error';
                        break;
                    case 'not-allowed':
                        errorMsg = 'Microphone access denied';
                        break;
                }
                showVoiceStatus('❌ ' + errorMsg, 'error');
                isListening = false;
                updateVoiceButton('idle');
                setTimeout(() => hideVoiceStatus(), 3000);
            };
            
            recognition.onend = function() {
                isListening = false;
                updateVoiceButton('idle');
            };
            
            return true;
        }
        
        // Toggle Voice Recognition
        function toggleVoiceRecognition() {
            if (!recognition) {
                if (!initSpeechRecognition()) {
                    alert('Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.');
                    return;
                }
            }
            
            if (isListening) {
                recognition.stop();
                isListening = false;
                updateVoiceButton('idle');
                hideVoiceStatus();
            } else {
                recognition.lang = currentVoiceLang;
                recognition.start();
            }
        }
        
        // Update Voice Button State
        function updateVoiceButton(state) {
            const btn = document.getElementById('voiceBtn');
            const btnText = document.getElementById('voiceBtnText');
            
            btn.className = 'voice-btn';
            
            switch(state) {
                case 'listening':
                    btn.classList.add('listening');
                    btnText.textContent = 'Stop Voice';
                    break;
                case 'processing':
                    btn.disabled = true;
                    btnText.textContent = 'Processing...';
                    break;
                case 'idle':
                default:
                    btn.disabled = false;
                    btnText.textContent = 'Start Voice';
                    break;
            }
        }
        
        // Show Voice Status
        function showVoiceStatus(message, type) {
            const status = document.getElementById('voiceStatus');
            status.textContent = message;
            status.className = 'voice-status ' + type;
            status.style.display = 'block';
        }
        
        // Hide Voice Status
        function hideVoiceStatus() {
            document.getElementById('voiceStatus').style.display = 'none';
        }
        
        // Update Voice Language
        function updateVoiceLanguage() {
            currentVoiceLang = document.getElementById('voiceLang').value;
            if (recognition) {
                recognition.lang = currentVoiceLang;
            }
        }
        
        // Speech Synthesis Functions
        function speakResponse() {
            if (!lastResponse) {
                alert('No response to speak. Please ask a question first.');
                return;
            }
            
            // Stop any current speech
            if (speechSynthesis.speaking) {
                speechSynthesis.cancel();
                updateSpeakButton('idle');
                return;
            }
            
            // Create utterance
            currentUtterance = new SpeechSynthesisUtterance(lastResponse);
            
            // Set voice language
            const voices = speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => voice.lang.startsWith(currentVoiceLang.substring(0, 2)));
            if (preferredVoice) {
                currentUtterance.voice = preferredVoice;
            }
            
            // Configure speech parameters
            currentUtterance.rate = 0.9;
            currentUtterance.pitch = 1.0;
            currentUtterance.volume = 1.0;
            
            // Event handlers
            currentUtterance.onstart = function() {
                updateSpeakButton('speaking');
            };
            
            currentUtterance.onend = function() {
                updateSpeakButton('idle');
            };
            
            currentUtterance.onerror = function(event) {
                console.error('Speech synthesis error:', event.error);
                updateSpeakButton('idle');
            };
            
            // Start speaking
            speechSynthesis.speak(currentUtterance);
        }
        
        // Update Speak Button State
        function updateSpeakButton(state) {
            const btn = document.getElementById('speakBtn');
            const btnSpan = btn.querySelector('span');
            
            btn.className = 'voice-btn';
            
            switch(state) {
                case 'speaking':
                    btn.classList.add('speaking');
                    btnSpan.textContent = 'Stop Speaking';
                    break;
                case 'idle':
                default:
                    btnSpan.textContent = 'Speak Answer';
                    break;
            }
        }
        
        // Initialize on page load
        window.addEventListener('load', function() {
            // Load voices
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = function() {
                    // Voices loaded
                };
            }
            
            // Check if speech recognition is supported
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                document.getElementById('voiceBtn').style.display = 'none';
                console.log('Speech recognition not supported in this browser');
            }
        });
        
        function setQuery(query, location) {
            document.getElementById('query').value = query;
            document.getElementById('location').value = location;
        }
        
        async function submitQuery(event) {
            event.preventDefault();
            
            const query = document.getElementById('query').value;
            const location = document.getElementById('location').value;
            const responseDiv = document.getElementById('response');
            const responseContent = document.getElementById('responseContent');
            const submitBtn = document.getElementById('submitBtn');
            
            // Show loading state
            responseDiv.style.display = 'block';
            responseContent.innerHTML = '<div class="loading">🤖 Processing your query...</div>';
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Processing...';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: query,
                        location: location || null
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const confidence = Math.round(data.confidence * 100);
                    
                    // Store response for voice synthesis
                    lastResponse = data.response;
                    
                    // Show speak button
                    document.getElementById('speakBtn').style.display = 'flex';
                    
                    // Update voice language if response is in different language
                    if (data.language === 'hi') {
                        document.getElementById('voiceLang').value = 'hi-IN';
                        currentVoiceLang = 'hi-IN';
                    } else if (data.language === 'en') {
                        document.getElementById('voiceLang').value = 'en-US';
                        currentVoiceLang = 'en-US';
                    }
                    
                    responseContent.innerHTML = `
                        <div class="response-content">${data.response}</div>
                        <div class="metadata">
                            📊 Confidence: ${confidence}% | 
                            📂 Category: ${data.category} | 
                            🔍 Source: ${data.source}
                            ${data.language !== 'en' ? ` | 🌐 Language: ${data.language}` : ''}
                            | 🎙️ <button onclick="speakResponse()" style="background: none; border: none; color: #4CAF50; cursor: pointer; text-decoration: underline;">Click to hear response</button>
                        </div>
                    `;
                } else {
                    responseContent.innerHTML = `<div style="color: red;">❌ Error: ${data.error}</div>`;
                    lastResponse = '';
                    document.getElementById('speakBtn').style.display = 'none';
                }
            } catch (error) {
                responseContent.innerHTML = `<div style="color: red;">❌ Network Error: ${error.message}</div>`;
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 Get AI Advice';
            }
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_404(self):
        """Send 404 response"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 - Not Found</h1>')
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{self.date_time_string()}] {format % args}")

def run_web_server(port=8080):
    """Run the web server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, AgricultureAPIHandler)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║              🌾 AGRICULTURE AI SYSTEM - WEB API              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✅ Server Status: RUNNING                                   ║
║  🌐 Access URL: http://localhost:{port}                       ║
║  📱 API Endpoint: http://localhost:{port}/api/query           ║
║                                                              ║
║  Features Available:                                         ║
║  • Weather forecasts and alerts                             ║
║  • Crop recommendations                                      ║
║  • Market prices (MSP comparison)                           ║
║  • Irrigation guidance                                       ║
║  • Pest and disease diagnosis                               ║
║  • Government schemes information                           ║
║  • Multilingual support (Hindi/English)                    ║
║                                                              ║
║  📖 Open http://localhost:{port} in your browser to start    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        httpd.shutdown()
        print("✅ Server stopped successfully")

if __name__ == "__main__":
    import sys
    
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8080.")
    
    run_web_server(port)
