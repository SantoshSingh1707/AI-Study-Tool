# Development startup script (Windows PowerShell)

Write-Host "🚀 Starting RAG Question Generator in Development Mode..." -ForegroundColor Green

# Check if backend virtual env exists
if (-not (Test-Path "backend\.venv")) {
    Write-Host "📦 Creating backend virtual environment..." -ForegroundColor Yellow
    cd backend
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    cd ..
} else {
    Write-Host "✅ Backend venv found" -ForegroundColor Green
}

# Check if frontend node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install
    cd ..
} else {
    Write-Host "✅ Frontend dependencies found" -ForegroundColor Green
}

# Check .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "📋 Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "🔑 Please edit .env and add your MISTRAL_API_KEY" -ForegroundColor Cyan
    Read-Host "Press Enter when ready..."
}

# Start services in separate windows
Write-Host ""
Write-Host "Starting backend..." -ForegroundColor Green
Start-PowerShell -ScriptBlock {
    cd backend
    .\.venv\Scripts\Activate.ps1
    uvicorn main:app --reload --port 8000
}

Write-Host "Starting frontend..." -ForegroundColor Green
Start-PowerShell -ScriptBlock {
    cd frontend
    npm run dev
}

Write-Host ""
Write-Host "✅ Both services started!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close the PowerShell windows to stop services." -ForegroundColor Yellow
