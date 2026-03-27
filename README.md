# RAG Question Generator

> Transform any document into interactive quizzes and study materials using AI

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react)](https://reactjs.org/)
[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-027BBD?style=flat)](https://mistral.ai/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat&logo=huggingface)](https://huggingface.co)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat&logo=vercel)](https://vercel.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade **Retrieval Augmented Generation (RAG)** application that converts your documents into personalized learning experiences. Upload PDFs, Word docs, or PowerPoint presentations and instantly generate interactive quizzes, flashcards, and comprehensive study notes powered by AI.

---

## 🌟 Live Deployment

**🎯 Frontend (Vercel):** https://frontend-psi-eight-61.vercel.app
**🔧 Backend (Hugging Face):** https://santosh1707-rag-question-generator-api.hf.space

---

## ✨ Features

- 📄 **Multi-Format Upload** - PDF, TXT, DOCX, PPTX support
- 🤖 **AI-Powered Generation** - Quiz questions, summaries, key notes
- 🎯 **Smart RAG** - ChromaDB vector store with sentence-transformers
- 🔄 **Multi-LLM Support** - Mistral AI, Groq, or Gemini
- 📱 **Modern UI** - Responsive React frontend with glassmorphic design
- ☁️ **Serverless Deployment** - Hugging Face Spaces + Vercel

---

## 🏗️ Architecture

```
Vercel Frontend (React) → Hugging Face Backend (FastAPI) → LLM APIs
```

---

## 🚀 Quick Start

### For Users

1. Visit **https://frontend-psi-eight-61.vercel.app**
2. Upload a document (PDF, TXT, DOCX, or PPTX)
3. Configure quiz settings (difficulty, number of questions)
4. Generate and review questions
5. Or switch to "Learning" mode for summaries

### For Developers (Local)

#### Prerequisites
- Python 3.11+
- Node.js 18+
- API keys: Mistral AI, Hugging Face

#### Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix/Mac

pip install -r requirements.txt

# Set environment variables (copy .env.example)
cp .env.example .env
# Edit .env: add MISTRAL_API_KEY, HUGGINGFACEHUB_API_TOKEN

uvicorn main:app --reload --port 8000
```

Backend: http://localhost:8000
API docs: http://localhost:8000/docs

#### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Frontend: http://localhost:5173

---

## 📖 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check with statistics |
| `/api/upload` | POST | Upload document (PDF, TXT, DOCX, PPTX) |
| `/api/documents` | GET | List all source documents |
| `/api/documents/{name}` | DELETE | Delete a source document |
| `/api/generate/quiz` | POST | Generate quiz questions |
| `/api/generate/learning` | POST | Generate summaries/key notes |

Full interactive docs at: `http://localhost:8000/docs` (when backend running)

---

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)

**Backend:**
- FastAPI
- ChromaDB (vector database)
- Sentence-Transformers (embeddings)
- LangChain (RAG orchestration)
- Mistral AI / Groq / Gemini (LLM)

**Deployment:**
- Docker (Hugging Face Spaces)
- Vercel (frontend hosting)

---

## 📁 Project Structure

```
Question-maker/
├── frontend/          # React + Vite app (deployed to Vercel)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/   # API client
│   │   ├── store/      # Zustand state
│   │   └── utils/
│   ├── package.json
│   └── vercel.json
├── backend/           # FastAPI app (deployed to Hugging Face)
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── data/          # Vector store & uploads
├── src/               # RAG engine modules
│   ├── data_loader.py
│   ├── embedding.py
│   ├── vector_store.py
│   └── search.py
├── data/              # Local data (optional)
├── deploy-huggingface.ps1  # Backend deployment
├── deploy-vercel.ps1       # Frontend deployment
├── VERCEL_DEPLOYMENT.md   # Detailed deployment guide
├── DEPLOYMENT.md          # Full deployment guide
└── DEPLOY_QUICKSTART.md   # Quick 5-min deployment
```

---

## 🔧 Configuration

### Backend Environment Variables

Required for Hugging Face deployment:

| Variable | Required | Description |
|----------|----------|-------------|
| `MISTRAL_API_KEY` | Yes | Mistral AI API key |
| `GROQ_API_KEY` | No | Groq API key (alternative) |
| `GEMINI_API_KEY` | No | Gemini API key (alternative) |
| `HUGGINGFACEHUB_API_TOKEN` | Yes | Hugging Face token |
| `PORT` | Yes | Port number (8000) |

### Frontend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend URL (e.g., `https://santosh1707-rag-question-generator-api.hf.space`) |

---

## 🚢 Deployment

### One-Command Deploy

```powershell
# Deploy backend to Hugging Face
.\deploy-huggingface.ps1

# Deploy frontend to Vercel
.\deploy-vercel.ps1
```

### Manual Deploy

See detailed guides:
- **[DEPLOY_QUICKSTART.md](./DEPLOY_QUICKSTART.md)** - Fast 5-minute guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Comprehensive documentation
- **[VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)** - Vercel-specific details

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Full test suite
python run_tests.py
```

---

## 📝 Environment Setup

### Local Development

1. **Backend**: Copy `.env.example` to `backend/.env` and add API keys
2. **Frontend**: Copy `frontend/.env.local.example` to `frontend/.env.local`

### Production (Hugging Face)

1. Go to your Space → Settings → Variables
2. Add all required environment variables
3. Wait for build (5-10 minutes)

### Production (Vercel)

1. Vercel Dashboard → Project → Settings → Environment Variables
2. Add `VITE_API_URL` with your Hugging Face backend URL
3. Redeploy

---

## 📊 Current Deployment

| Component | Platform | Status | URL |
|-----------|----------|--------|-----|
| Frontend | Vercel | ✅ Live | https://frontend-psi-eight-61.vercel.app |
| Backend | Hugging Face Spaces | ✅ Live | https://santosh1707-rag-question-generator-api.hf.space |

---

## 🔍 Troubleshooting

### Backend won't start
- ✅ Check environment variables are set
- ✅ Verify API keys are valid
- ✅ Check Hugging Face Space logs

### Frontend can't connect
- ✅ Backend health check passes? `GET /health`
- ✅ `VITE_API_URL` correct in Vercel?
- ✅ Backend CORS allows all origins (default)

### Upload fails
- ✅ File size < 50MB
- ✅ Format: PDF, TXT, DOCX, PPTX
- ✅ Backend has sufficient memory

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) (to be created) and submit PRs.

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

---

## 📚 Documentation

- [Quick Deploy](./DEPLOY_QUICKSTART.md)
- [Full Deployment Guide](./DEPLOYMENT.md)
- [Vercel Details](./VERCEL_DEPLOYMENT.md)
- [Testing](./TESTING.md)
- [Improvements](./IMPROVEMENTS.md)

---

Built with ❤️ for learners everywhere
