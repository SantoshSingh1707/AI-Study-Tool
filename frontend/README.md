# RAG Question Generator

An AI-powered study tool that generates quiz questions and learning content from uploaded documents using Retrieval-Augmented Generation (RAG).

## 🌟 Features

- **Upload Documents**: PDF, TXT, DOCX, PPTX formats supported
- **Generate Quiz Questions**: Multiple choice questions with varying difficulty levels
- **Generate Learning Content**: Summaries and key notes from documents
- **RAG Architecture**: Uses ChromaDB vector store with sentence-transformers embeddings
- **Multi-LLM Support**: Mistral AI, Groq, or Google Gemini for generation
- **Modern UI**: React frontend with beautiful, responsive design

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Vercel        │  ← Frontend (React + Vite)
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│ Hugging Face    │  ← Backend (FastAPI)
│ Spaces          │  → RAG Engine
│ (Backend)       │  → Vector DB (Chroma)
└────────┬────────┘
         │ API Calls
         ▼
    ┌─────────┐
    │  LLM    │  ← Mistral / Groq / Gemini
    │ Service │
    └─────────┘
```

---

## 🚀 Quick Start

### Live Deployment

**Frontend:** https://frontend-psi-eight-61.vercel.app
**Backend:** https://santosh1707-rag-question-generator-api.hf.space

### Local Development

#### Prerequisites

- Python 3.11+
- Node.js 18+
- API keys for at least one LLM provider (Mistral, Groq, or Gemini)

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run backend
uvicorn main:app --reload --port 8000
```

Backend runs at: http://localhost:8000
API docs: http://localhost:8000/docs

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Edit .env.local if using custom backend URL

# Run development server
npm run dev
```

Frontend runs at: http://localhost:5173

---

## 📖 API Documentation

### Health Check

```
GET /health
```

Returns backend health status and document count.

### Upload Document

```
POST /api/upload
Content-Type: multipart/form-data

Form data: file (PDF, TXT, DOCX, PPTX)
```

Response:
```json
{
  "success": true,
  "message": "Successfully processed file.pdf",
  "chunks_added": 15,
  "pages_processed": 3
}
```

### List Documents

```
GET /api/documents
```

Response:
```json
{
  "sources": ["file1.pdf", "file2.txt"],
  "total_chunks": 42
}
```

### Delete Document

```
DELETE /api/documents/{source_name}
```

### Generate Quiz

```
POST /api/generate/quiz
Content-Type: application/json

{
  "difficulty": "Medium",
  "num_questions": 5,
  "top_k": 10,
  "min_score": 0.2,
  "source_filter": ["file1.pdf"],
  "topic": "specific topic (optional)",
  "question_types": ["MCQ", "TrueFalse", "ShortAnswer"]
}
```

### Generate Learning Content

```
POST /api/generate/learning
Content-Type: application/json

{
  "mode": "Summary",  // or "Key Notes"
  "top_k": 20,
  "source_filter": ["file1.pdf"],
  "topic": "specific topic (optional)"
}
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Local embedding model (multi-qa-MiniLM-L6-cos-v1)
- **LangChain**: RAG orchestration
- **Mistral AI / Groq / Gemini**: LLM for content generation
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client
- **Zustand**: State management
- **React Router**: Navigation
- **Framer Motion**: Animations

### Deployment
- **Hugging Face Spaces**: Backend hosting (Docker)
- **Vercel**: Frontend hosting
- **GitHub**: Source control

---

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration classes
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Hugging Face deployment
│   └── data/             # Vector store & uploads
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service
│   │   ├── store/        # Zustand stores
│   │   └── utils/        # Utilities
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json       # Vercel config
├── src/                  # RAG modules (used by backend)
│   ├── data_loader.py    # Document processing
│   ├── embedding.py      # Embedding manager
│   ├── vector_store.py   # ChromaDB wrapper
│   └── search.py         # RAG retrieval & generation
├── data/                 # Local data (optional)
├── deploy-huggingface.ps1  # Backend deployment script
├── deploy-vercel.ps1       # Frontend deployment script
└── README.md
```

---

## 🔧 Configuration

### Backend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MISTRAL_API_KEY` | Yes* | Mistral AI API key |
| `GROQ_API_KEY` | No | Groq API key |
| `GEMINI_API_KEY` | No | Gemini API key |
| `HUGGINGFACEHUB_API_TOKEN` | Yes | Hugging Face token for models |
| `PORT` | Yes (default: 8000) | Server port |

*At least one LLM API key is required

### Frontend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend API URL (e.g., `https://your-backend.hf.space`) |

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 📦 Deployment

See detailed guides:
- **[VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)** - Complete deployment instructions for Hugging Face + Vercel

Quick deploy scripts:
```powershell
# Deploy backend to Hugging Face
.\deploy-huggingface.ps1

# Deploy frontend to Vercel
.\deploy-vercel.ps1
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🐛 Troubleshooting

### Backend Issues

- **Model download fails**: Ensure `HUGGINGFACEHUB_API_TOKEN` is set and has permissions
- **LLM generation fails**: Check API key credits and rate limits
- **Out of memory**: Reduce batch sizes or use smaller embedding model

### Frontend Issues

- **CORS errors**: Backend must allow your frontend origin (already configured to allow all)
- **Assets not loading**: Check Vercel `vercel.json` routing configuration
- **Build fails**: Ensure Node.js 18+ and run `npm install`

---

## 📞 Support

For issues and feature requests, please open an issue on GitHub.
