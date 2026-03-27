# 🚀 Comprehensive Deployment Guide

This guide covers local development and production deployment of the RAG Question Generator.

---

## 📁 Project Structure

```
Question-maker/
├── frontend/              # React + Vite
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   ├── store/        # Zustand state management
│   │   ├── hooks/        # React Query hooks
│   │   ├── types/        # TypeScript definitions
│   │   └── utils/        # Helper functions
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json       # Vercel configuration
├── backend/               # FastAPI
│   ├── main.py           # API server
│   ├── config.py
│   ├── requirements.txt
│   ├── Dockerfile        # Hugging Face deployment
│   └── data/             # Local storage
├── src/                  # RAG engine modules
│   ├── data_loader.py    # Document processing
│   ├── embedding.py      # Embedding manager
│   ├── vector_store.py   # ChromaDB wrapper
│   └── search.py         # RAG retrieval & generation
├── data/                 # Local data (optional)
├── deploy-huggingface.ps1  # Backend deployment
├── deploy-vercel.ps1       # Frontend deployment
├── VERCEl_DEPLOYMENT.md  # Detailed deployment guide
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

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/Mac:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (copy from .env.example or create manually)
# Required: MISTRAL_API_KEY, HUGGINGFACEHUB_API_TOKEN

# Run the backend
uvicorn main:app --reload --port 8000
```

Backend runs at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Contains: VITE_API_URL=http://localhost:8000

# Run the development server
npm run dev
```

Frontend runs at: http://localhost:5173

### Fullstack Development

1. Start backend first (in one terminal)
2. Start frontend (in another terminal)
3. Open http://localhost:5173

---

## ☁️ Production Deployment

### Overview

Production deployment uses:
- **Hugging Face Spaces** for backend (Docker)
- **Vercel** for frontend (static build)

```
Vercel Frontend → Hugging Face Backend → LLM APIs
```

---

### Part 1: Deploy Backend to Hugging Face

#### 1.1 Create Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure:
   - **Owner**: `santosh1707` (your username)
   - **Space name**: `rag-question-generator-api`
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic` (free)
   - **Public/Private**: Your choice
4. Click **"Create Space"**

#### 1.2 Deploy Using Script

From project root:

```powershell
.\deploy-huggingface.ps1
```

The script automates:
- Cloning the Space repository
- Copying necessary files (Dockerfile, backend/, src/, requirements.txt)
- Committing and pushing

#### 1.3 Set Environment Variables

In Hugging Face Space → **Settings** → **Variables**, add:

```
MISTRAL_API_KEY=your_mistral_key
GROQ_API_KEY=your_groq_key (optional)
GEMINI_API_KEY=your_gemini_key (optional)
HUGGINGFACEHUB_API_TOKEN=your_hf_token
PORT=8000
```

#### 1.4 Wait for Build

Build takes 5-10 minutes. Monitor on your Space page.

Test when complete:
```
https://santosh1707-rag-question-generator-api.hf.space/health
```

Expected:
```json
{
  "status": "healthy",
  "documents_count": 0,
  "available_sources": []
}
```

---

### Part 2: Deploy Frontend to Vercel

#### 2.1 Prepare Frontend

```bash
cd frontend
cp .env.local.example .env.local
# Contains VITE_API_URL=http://localhost:8000 for local dev
```

#### 2.2 Deploy

**Option A: Vercel CLI**

```bash
# Install and login
npm i -g vercel
vercel login

# Deploy
vercel --prod
```

Follow prompts. Use default settings or specify:
- Project name: `question-maker-frontend`
- Root directory: `.`

**Option B: Already Linked**

If your Vercel project is already linked:

```bash
cd frontend
git add .
git commit -m "Deploy to Vercel"
git push origin main
```

Vercel auto-deploys.

#### 2.3 Configure Production Environment

After deployment, set `VITE_API_URL`:

```bash
cd frontend
vercel env add VITE_API_URL production --value "https://santosh1707-rag-question-generator-api.hf.space" --yes
```

Or manually:
1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add: `VITE_API_URL` = `https://santosh1707-rag-ququestion-generator-api.hf.space`
3. Environment: Production
4. Save and **redeploy**

#### 2.4 Verify

Visit your Vercel URL. Open DevTools → Network tab.
Upload a document and verify API calls succeed.

---

## 🧪 Testing

### Health Check

```bash
curl https://santosh1707-rag-question-generator-api.hf.space/health
```

### Upload Test

```bash
curl -X POST "https://santosh1707-rag-question-generator-api.hf.space/api/upload" \
  -F "file=@document.pdf"
```

### Generate Quiz

```bash
curl -X POST "https://santosh1707-rag-question-generator-api.hf.space/api/generate/quiz" \
  -H "Content-Type: application/json" \
  -d '{
    "difficulty": "Medium",
    "num_questions": 5,
    "question_types": ["MCQ"]
  }'
```

---

## 🔧 Configuration

### Backend Environment (Hugging Face)

| Variable | Required | Description |
|----------|----------|-------------|
| `MISTRAL_API_KEY` | Yes | Mistral AI API key |
| `GROQ_API_KEY` | No | Groq API key |
| `GEMINI_API_KEY` | No | Gemini API key |
| `HUGGINGFACEHUB_API_TOKEN` | Yes | Hugging Face token |
| `PORT` | Yes | Port (8000) |

### Frontend Environment (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend URL (`.hf.space`) |

---

## 🔍 Troubleshooting

### Backend Build Fails on Hugging Face

- Check environment variables are all set
- First build downloads embedding model (~500MB) - may timeout, increase timeout in Space settings
- Check build logs in Hugging Face

### CORS Errors

Backend allows all origins (`"*"`). If CORS errors occur:
- Verify backend is running and accessible
- Check `VITE_API_URL` is correct in Vercel
- Test backend directly in browser

### Frontend Assets Not Loading

Our updated `vercel.json` should fix this. If not:
- Check that `/assets/` files are served correctly
- Clear browser cache
- Verify build output contains assets

### API Timeouts

LLM generation takes 30-60 seconds. Backend timeout is 5 minutes.
If still timing out:
- Check backend logs
- Verify LLM API keys have credits
- Reduce generated content size

---

## 📊 Deployment Checklist

- [ ] Hugging Face Space created
- [ ] Backend environment variables set
- [ ] Backend build completed
- [ ] Backend health endpoint returns `healthy`
- [ ] Vercel project exists
- [ ] Frontend deployed
- [ ] `VITE_API_URL` set in Vercel (production)
- [ ] Frontend loads without errors
- [ ] Can upload document
- [ ] Can generate quiz
- [ ] Can generate learning content

---

## 🔄 Updates & Redeployment

### Update Backend

```bash
git add backend/ src/ Dockerfile requirements.txt
git commit -m "Update backend"
git push origin main
# Hugging Face auto-rebuilds
```

Or manually: Space → Settings → Recalculate

### Update Frontend

```bash
cd frontend
git add .
git commit -m "Update frontend"
git push origin main
# Vercel auto-deploys
```

Or manually: `vercel --prod --force`

---

## 🌐 Live URLs

**Frontend**: https://frontend-psi-eight-61.vercel.app
**Backend**: https://santosh1707-rag-question-generator-api.hf.space

---

## 📚 More Information

- **Quick Start**: See `DEPLOY_QUICKSTART.md` for one-command deployment
- **Vercel Specific**: See `VERCEL_DEPLOYMENT.md` for detailed Vercel guide
- **Architecture & Local Dev**: See `README.md`
- **Testing**: See `TESTING.md`

---

## 💡 Production Tips

1. **First build is slow** - embedding model downloads (~500MB)
2. **Hugging Face free tier** has limited RAM - keep document sizes reasonable
3. **Monitor usage** to avoid exceeding free tier limits
4. **Custom domains** can be added in both platforms
5. **Cold start** - first request after inactivity takes longer

---

**Need help?** Check logs in Hugging Face (Space → Logs) and Vercel (Dashboard → Functions).
