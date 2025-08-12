#!/bin/bash

# Agriculture AI System - Deployment Script
# Usage: ./deploy.sh [development|production|docker]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default deployment type
DEPLOY_TYPE=${1:-development}

echo -e "${GREEN}🌾 Agriculture AI System - Deployment Script${NC}"
echo -e "${YELLOW}Deployment type: $DEPLOY_TYPE${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✅ Python version: $python_version${NC}"

case $DEPLOY_TYPE in
    "development")
        echo -e "${YELLOW}🔧 Setting up development environment...${NC}"
        
        # Create virtual environment if it doesn't exist
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi
        
        # Activate virtual environment
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
        
        echo -e "${GREEN}✅ Development environment ready!${NC}"
        echo -e "${YELLOW}To start the server, run:${NC}"
        echo "  source venv/bin/activate"
        echo "  python web_api.py"
        ;;
        
    "production")
        echo -e "${YELLOW}🚀 Setting up production environment...${NC}"
        
        # Install system dependencies
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv nginx
        elif command_exists yum; then
            sudo yum update -y
            sudo yum install -y python3-pip python3-venv nginx
        fi
        
        # Create production user
        if ! id "agriculture" &>/dev/null; then
            sudo useradd -r -s /bin/bash -m agriculture
        fi
        
        # Setup application directory
        sudo mkdir -p /opt/agriculture-ai
        sudo chown agriculture:agriculture /opt/agriculture-ai
        sudo cp -r . /opt/agriculture-ai/
        
        # Install dependencies
        cd /opt/agriculture-ai
        sudo -u agriculture python3 -m venv venv
        sudo -u agriculture venv/bin/pip install --upgrade pip
        sudo -u agriculture venv/bin/pip install -r requirements.txt
        sudo -u agriculture venv/bin/pip install gunicorn
        
        # Create systemd service
        sudo tee /etc/systemd/system/agriculture-ai.service > /dev/null <<EOF
[Unit]
Description=Agriculture AI System
After=network.target

[Service]
Type=notify
User=agriculture
Group=agriculture
WorkingDirectory=/opt/agriculture-ai
Environment=PATH=/opt/agriculture-ai/venv/bin
ExecStart=/opt/agriculture-ai/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8080 web_api:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF
        
        # Start and enable service
        sudo systemctl daemon-reload
        sudo systemctl enable agriculture-ai
        sudo systemctl start agriculture-ai
        
        echo -e "${GREEN}✅ Production deployment complete!${NC}"
        echo -e "${YELLOW}Service status:${NC}"
        sudo systemctl status agriculture-ai --no-pager
        ;;
        
    "docker")
        echo -e "${YELLOW}🐳 Setting up Docker deployment...${NC}"
        
        # Check Docker installation
        if ! command_exists docker; then
            echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
            exit 1
        fi
        
        if ! command_exists docker-compose; then
            echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
            exit 1
        fi
        
        # Build and start containers
        echo "Building Docker image..."
        docker-compose build
        
        echo "Starting containers..."
        docker-compose up -d
        
        echo -e "${GREEN}✅ Docker deployment complete!${NC}"
        echo -e "${YELLOW}Container status:${NC}"
        docker-compose ps
        
        echo -e "${YELLOW}To view logs:${NC}"
        echo "  docker-compose logs -f agriculture-ai"
        
        echo -e "${YELLOW}To stop:${NC}"
        echo "  docker-compose down"
        ;;
        
    *)
        echo -e "${RED}❌ Invalid deployment type. Use: development, production, or docker${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${YELLOW}Access the application at: http://localhost:8080${NC}"
echo -e "${YELLOW}API endpoint: http://localhost:8080/api/query${NC}"
echo -e "${YELLOW}Voice demo: http://localhost:8080/voice_demo.html${NC}"
