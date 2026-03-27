#!/bin/bash
# Development startup script (Linux/Mac)

echo "🚀 Starting RAG Question Generator in Development Mode..."

# Check if backend virtual env exists
if [ ! -d "backend/.venv" ]; then
    echo "📦 Creating backend virtual environment..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "✅ Backend venv found"
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "✅ Frontend dependencies found"
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Copying from .env.example..."
    cp .env.example .env
    echo "🔑 Please edit .env and add your MISTRAL_API_KEY"
    read -p "Press Enter when ready..."
fi

# Start services
echo ""
echo "Starting backend..."
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both services started!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
