#!/bin/bash

# Agentic AI Research Assistant - Setup Script
# This script automates the initial setup process

set -e  # Exit on error

echo "🚀 Agentic AI Research Assistant - Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo "ℹ $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
fi

if ! command_exists node; then
    print_error "Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
else
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
fi

if ! command_exists npm; then
    print_error "npm is not installed. Please install npm."
    exit 1
else
    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"
fi

echo ""

# Backend setup
echo "🔧 Setting up backend..."

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || {
    print_error "Failed to activate virtual environment"
    exit 1
}
print_success "Virtual environment activated"

# Install dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Python dependencies installed"

# Setup environment file
if [ ! -f ".env" ]; then
    print_info "Creating .env file..."
    cp .env.example .env
    print_warning "Please edit backend/.env and add your API keys:"
    print_warning "  - OPENAI_API_KEY"
    print_warning "  - TAVILY_API_KEY"
else
    print_warning ".env file already exists"
fi

cd ..

echo ""

# Frontend setup
echo "🎨 Setting up frontend..."

cd frontend

# Install dependencies
print_info "Installing Node.js dependencies..."
npm install > /dev/null 2>&1
print_success "Node.js dependencies installed"

cd ..

echo ""

# Docker check (optional)
echo "🐳 Checking for Docker (optional)..."

if command_exists docker; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    print_success "Docker $DOCKER_VERSION found"
    
    if command_exists docker-compose; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | tr -d ',')
        print_success "Docker Compose $COMPOSE_VERSION found"
        print_info "You can use 'docker-compose up' to start all services"
    else
        print_warning "Docker Compose not found. Install it for easy deployment."
    fi
else
    print_warning "Docker not found. Install it for containerized deployment."
fi

echo ""

# Summary
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
print_info "Next steps:"
echo ""
echo "1. Configure your API keys:"
echo "   Edit: backend/.env"
echo "   Required: OPENAI_API_KEY, TAVILY_API_KEY"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   python main.py"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser:"
echo "   http://localhost:3000"
echo ""
print_info "Or use Docker (if installed):"
echo "   docker-compose up"
echo ""
echo "📚 For more information, see README.md or QUICKSTART.md"
echo ""
print_success "Happy researching! 🎉"

