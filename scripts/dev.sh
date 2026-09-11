#!/bin/bash
# Development startup script (Linux/Mac)

echo "🚀 Starting RAG Question Generator (Streamlit)..."

# Check if virtual env exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Copying from .env.example..."
    cp .env.example .env
    echo "⚙️  Using local Ollama for the LLM — no API keys needed"
fi

echo "Launching Streamlit app..."
exec .venv/bin/python -m streamlit run app.py