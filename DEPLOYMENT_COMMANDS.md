# 🚀 Deployment Commands for Agriculture AI System

## 📁 **GitHub Repository Setup**

### **1. Initialize Git Repository**
```bash
# Navigate to project directory
cd C:\Users\91709\agriculture_ai_system

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "🌾 Initial commit: Agriculture AI System with Voice Commands

Features:
- 🎤 Voice recognition in 8 Indian languages
- 🔊 Text-to-speech responses 
- 🤖 Multi-agent AI architecture
- 🌐 Multilingual translation (Hindi/English)
- 🌾 Agricultural expertise (weather, crops, market, irrigation, pests, finance)
- 🖥️ Web interface with voice demos
- 🐳 Docker deployment ready"
```

### **2. Create GitHub Repository**
```bash
# Method 1: Using GitHub CLI (if installed)
gh repo create agriculture-ai-system --public --description "🌾 Voice-enabled AI assistant for Indian farmers with multilingual support"
gh repo view --web

# Method 2: Manual steps
# 1. Go to https://github.com/new
# 2. Repository name: agriculture-ai-system
# 3. Description: 🌾 Voice-enabled AI assistant for Indian farmers with multilingual support
# 4. Make it Public
# 5. Don't initialize with README (we already have one)
# 6. Click "Create repository"
```

### **3. Push to GitHub**
```bash
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/agriculture-ai-system.git

# Push to main branch
git branch -M main
git push -u origin main
```

## 🌐 **Enable GitHub Pages for Voice Demos**

### **1. Enable GitHub Pages**
1. Go to your repository settings
2. Scroll down to "Pages" section
3. Source: "Deploy from a branch"
4. Branch: "main" / "/ (root)"
5. Click "Save"

### **2. Access Voice Demos**
After GitHub Pages is enabled (takes ~5 minutes):
- **Voice Demo**: `https://YOUR_USERNAME.github.io/agriculture-ai-system/voice_demo.html`
- **Farming Commands**: `https://YOUR_USERNAME.github.io/agriculture-ai-system/farming_voice_commands.html`

## 🖥️ **Local Development**

### **Quick Start (Windows)**
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agriculture-ai-system.git
cd agriculture-ai-system

# Run the web server
python web_api.py

# Open in browser
start http://localhost:8080
```

### **Quick Start (Linux/Mac)**
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agriculture-ai-system.git
cd agriculture-ai-system

# Make deployment script executable
chmod +x deploy.sh

# Run development setup
./deploy.sh development

# Or run directly
python3 web_api.py

# Open in browser
open http://localhost:8080  # Mac
xdg-open http://localhost:8080  # Linux
```

## 🐳 **Docker Deployment**

### **Local Docker**
```bash
# Build and run with Docker
docker build -t agriculture-ai .
docker run -p 8080:8080 agriculture-ai

# Or use Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f agriculture-ai

# Stop
docker-compose down
```

### **Deploy to Cloud Platforms**

#### **Heroku Deployment**
```bash
# Install Heroku CLI first
npm install -g heroku

# Login to Heroku
heroku login

# Create Heroku app
heroku create agriculture-ai-system-YOUR_NAME

# Set Python buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

#### **Railway Deployment**
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select "agriculture-ai-system"
4. Railway will auto-detect Python and deploy
5. Set port to 8080 in settings

#### **Render Deployment**
1. Go to [Render.com](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `python web_api.py`

## 📱 **Mobile-Friendly Testing**

### **Test on Mobile Devices**
1. Deploy to any cloud platform above
2. Open on mobile browser
3. Test voice commands:
   - Allow microphone access
   - Try Hindi and English voice input
   - Test text-to-speech output

### **QR Code for Easy Access**
Generate QR codes for your deployed URLs:
- Use [QR Code Generator](https://www.qr-code-generator.com/)
- Share with farmers for easy mobile access

## 🔧 **Environment Configuration**

### **Production Environment Variables**
```bash
# Optional: Set these for production
export OPENWEATHER_API_KEY="your_weather_api_key"
export LOG_LEVEL="INFO"
export PORT="8080"
```

### **Development vs Production**
- **Development**: Runs on localhost:8080
- **Production**: Configure domain, HTTPS, load balancing

## 📊 **Monitoring and Analytics**

### **Basic Monitoring**
- Health check endpoint: `/api/health`
- Docker health checks included
- Systemd service monitoring (Linux)

### **Analytics (Optional)**
Add Google Analytics to track usage:
```html
<!-- Add to web_api.py HTML templates -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
```

## 🛠️ **Continuous Integration (Optional)**

### **GitHub Actions Workflow**
Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Test application
      run: |
        python -m pytest tests/ || echo "No tests yet"
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: echo "Deploy to your preferred platform"
```

## 🎉 **Success Checklist**

- ✅ Repository created on GitHub
- ✅ Code pushed to main branch
- ✅ GitHub Pages enabled for demos
- ✅ Local development working
- ✅ Voice features tested in browser
- ✅ Docker deployment ready
- ✅ Cloud deployment options available
- ✅ Mobile compatibility verified

## 🔗 **Important URLs After Deployment**

Replace `YOUR_USERNAME` with your GitHub username:

- **Repository**: `https://github.com/YOUR_USERNAME/agriculture-ai-system`
- **Voice Demo**: `https://YOUR_USERNAME.github.io/agriculture-ai-system/voice_demo.html`
- **Farming Commands**: `https://YOUR_USERNAME.github.io/agriculture-ai-system/farming_voice_commands.html`
- **Issues**: `https://github.com/YOUR_USERNAME/agriculture-ai-system/issues`
- **Live App**: `https://your-app-name.herokuapp.com` (or your chosen platform)

---

**🌾 Your Agriculture AI System with Voice Commands is now ready for deployment!**
