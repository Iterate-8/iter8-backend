#!/bin/bash

# FastAPI GraphQL Backend Startup Script (Conda Version)

set -e

echo "🚀 Starting FastAPI GraphQL Backend with Conda..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your configuration."
    exit 1
fi

# Load environment variables
source .env

# Check if conda environment exists
if ! conda env list | grep -q "iter8-backend"; then
    echo "📦 Creating conda environment 'iter8-backend'..."
    conda create -n iter8-backend python=3.11 -y
fi

# Activate conda environment
echo "🔧 Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate iter8-backend

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if we're in development mode
if [ "$DEBUG" = "True" ]; then
    echo "🔍 Starting in development mode..."
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🔍 GraphiQL Playground: http://localhost:8000/graphql"
    echo "💚 Health Check: http://localhost:8000/health"
    
    # Start with auto-reload
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "🚀 Starting in production mode..."
    
    # Start without auto-reload
    uvicorn app.main:app --host 0.0.0.0 --port 8000
fi 