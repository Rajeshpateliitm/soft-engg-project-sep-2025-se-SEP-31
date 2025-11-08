#!/bin/bash

# WasteWise Backend Run Script

echo "🚀 Starting WasteWise Backend Setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run the application
# Database will be automatically initialized on first run
echo "🌟 Starting Flask server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "🛑 Press CTRL+C to stop the server"
echo ""

python main.py

