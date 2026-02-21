#!/bin/bash

# Quick Start Script for Groq AI Assistant with React Frontend

echo "🚀 Starting Groq AI Assistant with React Frontend..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please create a .env file with:"
    echo "  GROQ_API_KEY=your_api_key_here"
    echo ""
    exit 1
fi

echo "📦 Installing backend dependencies..."
pip install -q -r requirements.txt

echo "📦 Installing frontend dependencies..."
cd frontend
npm install -q --no-fund

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "Terminal 1 - Start Backend:"
echo "  python Backend.py"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Then open your browser to:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:5000"
echo ""
