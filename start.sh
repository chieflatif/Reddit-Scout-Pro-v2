#!/bin/bash

# Reddit Scout Pro - Startup Script
# This script ensures the app starts correctly every time

echo "🔍 Starting Reddit Scout Pro..."

# Change to project directory
cd "$(dirname "$0")"

# Kill any existing streamlit processes
echo "🔧 Cleaning up any existing processes..."
pkill -f streamlit > /dev/null 2>&1

# Deactivate any virtual environment that might be active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "🔄 Deactivating virtual environment..."
    deactivate > /dev/null 2>&1 || true
fi

# Wait a moment for processes to clean up
sleep 2

# Start with Poetry (which has all dependencies)
echo "🚀 Starting Reddit Scout Pro with Poetry..."
echo ""
echo "📱 The app will open at: http://localhost:8501"
echo "🛑 To stop the app, press Ctrl+C"
echo ""

# Run the app
poetry run streamlit run app.py --server.port 8501 --server.headless false

echo ""
echo "✅ Reddit Scout Pro has been stopped."
