# 🚀 Deployment Guide

This guide covers both local development and production deployment of the RAG Question Generator.

---

## 📁 Project Structure (After Migration)

```
Question-maker/
├── frontend/              # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── store/        # Zustand state management
│   │   ├── services/     # API client
│   │   ├── hooks/        # React Query hooks
│   │   ├── types/        # TypeScript definitions
│   │   └── utils/        # Helper functions
│   ├── Dockerfile
│   └── nginx.conf
├── backend/               # FastAPI
│   ├── main.py           # API server
│   ├── config.py
│   ├── routes/           # (routes embedded in main.py)
│   └── requirements.txt
├── src/                   # Original RAG engine (used by backend)
│   ├── data_loader.py
│   ├── embedding.py
│   ├── vector_store.py
│   └── search.py
├── data/                  # Shared data directory
│   ├── pdf/
│   ├── textfiles/
│   ├── docx/
│   ├── pptx/
│   └── vector_store/
├── docker-compose.yml
├── pyproject.toml        # Python dependencies (for src)
├── requirements.txt      # Original Python deps
├── README.md
└── IMPROVEMENTS.md
```

---

## 🛠️ Local Development

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **Git**

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix/Mac:
   # source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   # Copy from root .env or create new
   cp ../.env .env  # Or manually create with MISTRAL_API_KEY
   ```

5. **Run the backend**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   API will be available at: http://localhost:8000
   - Health check: http://localhost:8000/health
   - API docs: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   # The default .env.development is already configured
   # Or create .env with:
   # VITE_API_URL=http://localhost:8000
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

   App will be available at: http://localhost:5173
   - Hot reload enabled
   - API proxy configured to http://localhost:8000

### Fullstack Development

1. Start backend first (in one terminal)
2. Start frontend (in another terminal)
3. Open http://localhost:5173

---

## 🐳 Docker Deployment (Production)

### Using Docker Compose (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd Question-maker
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env and add your MISTRAL_API_KEY
   ```

3. **Build and start services**:
   ```bash
   docker-compose up -d
   ```

   This will:
   - Build backend image (Python 3.11, all dependencies)
   - Build frontend image (Node 18 + Nginx)
   - Start both services on defined ports
   - Create shared volume for data persistence

4. **Access the application**:
   - Frontend: http://localhost (port 80)
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **View logs**:
   ```bash
   docker-compose logs -f
   ```

6. **Stop services**:
   ```bash
   docker-compose down
   ```

   Add `-v` to also remove volumes (⚠️ deletes data)

### Manual Docker Build

If you want to build and run separately:

**Backend**:
```bash
cd backend
docker build -t rag-backend .
docker run -p 8000:8000 \
  -e MISTRAL_API_KEY=your_key_here \
  -v $(pwd)/../data:/app/data \
  rag-backend
```

**Frontend**:
```bash
cd frontend
docker build -t rag-frontend .
docker run -p 80:80 \
  -e VITE_API_URL=http://your-backend-url:8000 \
  rag-frontend
```

---

## ☁️ Production Deployment

### Option 1: Railway/Render (Backend) + Vercel (Frontend)

**Backend (Railway/Render)**:
1. Connect your repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `MISTRAL_API_KEY`
5. Add persistent volume for `data/` directory

**Frontend (Vercel)**:
1. Import project from GitHub
2. Root directory: `frontend`
3. Build command: `npm run build`
4. Output directory: `dist`
5. Add environment variable: `VITE_API_URL=https://your-backend-url.railway.app`

### Option 2: Single Server (Docker Compose)

For VPS/Droplet:

1. **SSH to server**
2. **Clone repo**:
   ```bash
   git clone <repo>
   cd Question-maker
   ```

3. **Create environment**:
   ```bash
   cp .env.example .env
   nano .env  # Add MISTRAL_API_KEY
   ```

4. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

5. **Setup Nginx reverse proxy** (optional but recommended):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:80;
       }

       location /api/ {
           proxy_pass http://localhost:8000;
       }
   }
   ```

6. **Setup SSL with Let's Encrypt**:
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 🔧 Configuration

### Environment Variables

**Backend (.env)**:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
# Optional: Configure ChromaDB settings via env vars in main.py
```

**Frontend (.env)**:
```env
VITE_API_URL=http://localhost:8000
```

### Data Persistence

Data is stored in:
- `data/vector_store/` - ChromaDB embeddings (persistent)
- `data/pdf/`, `data/textfiles/`, etc. - Original uploaded files

**Important**: These directories are mounted as Docker volumes to persist across restarts.

---

## ✅ Testing

### Health Check

```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","documents_count":0,"available_sources":[]}
```

### Upload Test

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

### Generate Quiz

```bash
curl -X POST "http://localhost:8000/api/generate/quiz" \
  -H "Content-Type: application/json" \
  -d '{
    "difficulty": "Medium",
    "num_questions": 5,
    "top_k": 10,
    "min_score": 0.2,
    "question_types": ["MCQ"]
  }'
```

---

## 🔍 Troubleshooting

### Backend won't start
- Check Python version (3.11+)
- Verify `MISTRAL_API_KEY` is set
- Check logs: `docker-compose logs backend`
- Ensure port 8000 is available

### Frontend can't connect to backend
- Verify backend is running: `curl http://localhost:8000/health`
- Check `VITE_API_URL` in frontend .env
- Check browser console for CORS errors
- Verify Docker network: `docker network ls`

### OCR errors
- Install system dependencies: `apt-get install -y tesseract-ocr`
- Check EasyOCR installation in logs

### Out of memory
- Reduce batch size in `vector_store.py`
- Use smaller embedding model
- Increase Docker memory limits

---

## 📈 Performance Tips

1. **Upload videos**: Use `docker-compose up --scale backend=2` for multiple backend instances
2. **Cache embeddings**: Enable persistent vector store (already enabled)
3. **CDN for frontend**: Deploy frontend to Vercel/Netlify for global CDN
4. **Database scaling**: For large document collections (>10k), consider ChromaDB cloud or pgvector
5. **GPU acceleration**: Build backend with CUDA support for faster embeddings

---

## 🔄 Updates

To update the application:

1. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

2. **Rebuild and restart**:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

**Need help?** Check issues or create a new one on GitHub.
