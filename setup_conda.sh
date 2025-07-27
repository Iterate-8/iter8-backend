#!/bin/bash

# FastAPI GraphQL Backend Conda Setup Script

set -e

echo "🔧 Setting up FastAPI GraphQL Backend with Conda..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed!"
    echo "Please install Anaconda or Miniconda first:"
    echo "https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create conda environment from environment.yml
echo "📦 Creating conda environment from environment.yml..."
conda env create -f environment.yml

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env_template.txt .env
    echo "✅ .env file created!"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file with your actual values:"
    echo "   - DATABASE_URL (from Supabase)"
    echo "   - SUPABASE_URL (from Supabase)"
    echo "   - SUPABASE_ANON_KEY (from Supabase)"
    echo "   - SUPABASE_SERVICE_ROLE_KEY (from Supabase)"
    echo "   - SECRET_KEY (generate a random key)"
    echo ""
    echo "You can generate a secret key with:"
    echo "python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    echo ""
else
    echo "✅ .env file already exists!"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Supabase credentials"
echo "2. Run: ./start_conda.sh"
echo ""
echo "Or manually:"
echo "1. conda activate iter8-backend"
echo "2. python -m app.main" 