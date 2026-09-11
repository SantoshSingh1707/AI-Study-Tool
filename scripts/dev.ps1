# Development startup script (Windows PowerShell)

Write-Host "🚀 Starting RAG Question Generator (Streamlit)..." -ForegroundColor Green

# Check if virtual env exists
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
} else {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
}

# Check .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "📋 Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚙️  Using local Ollama for the LLM — no API keys needed" -ForegroundColor Cyan
}

Write-Host "Launching Streamlit app..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m streamlit run app.py

Write-Host ""
Write-Host "🌐 App: http://localhost:8501" -ForegroundColor Cyan