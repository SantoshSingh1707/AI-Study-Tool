# ⚡ Quick Deployment Guide

Deploy your RAG Question Maker in 5-10 minutes using Hugging Face Spaces (backend) and Vercel (frontend).

---

## 📋 Prerequisites

- **Mistral AI API key** - Get free at [mistral.ai](https://console.mistral.ai)
- **Hugging Face account** - Free at [huggingface.co](https://huggingface.co)
- **Vercel account** - Free at [vercel.com](https://vercel.com)
- **Git** installed locally

---

## 🚀 One-Command Deployment

### **Windows (PowerShell)**

Run as Administrator in project root:

```powershell
.\deploy-huggingface.ps1
```

This scripts creates and deploys your backend to Hugging Face.

Then deploy frontend:

```powershell
.\deploy-vercel.ps1
```

### **What the scripts do:**

**deploy-huggingface.ps1:**
1. Clones your Hugging Face Space
2. Copies backend files (Dockerfile, backend/, src/, requirements.txt)
3. Commits and pushes
4. Wait for build to start on Hugging Face

**deploy-vercel.ps1:**
1. Builds frontend
2. Deploys to Vercel
3. Sets production environment variable

---

## 🔧 Manual Deployment (If Scripts Fail)

### Step 1: Backend on Hugging Face

```bash
# 1. Create Space manually on huggingface.co/spaces
#    Name: rag-question-generator-api
#    SDK: Docker

# 2. Clone your Space
git clone https://huggingface.co/spaces/santosh1707/rag-question-generator-api
cd rag-question-generator-api

# 3. Copy project files
cp -r ../backend ./
cp -r ../src ./
cp ../Dockerfile ./
cp ../requirements.txt ./
cp ../huggingface.yml ./

# Create data directories
mkdir -p data/vector_store data/uploads data/pdf data/textfiles data/docx data/pptx
touch data/vector_store/.gitkeep data/uploads/.gitkeep

# 4. Commit and push
git add .
git commit -m "Deploy backend"
git push origin main
```

**Set environment variables** in Hugging Face Space → Settings → Variables:

```
MISTRAL_API_KEY=your_key_here
GROQ_API_KEY=your_key_here (optional)
GEMINI_API_KEY=your_key_here (optional)
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
PORT=8000
```

Wait 5-10 minutes for build. Test:
```
https://santosh1707-rag-question-generator-api.hf.space/health
```

---

### Step 2: Frontend on Vercel

```bash
# Navigate to frontend
cd frontend

# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

Follow prompts:
- Link to existing project? No
- Project name: `question-maker-frontend`
- Root directory: `.`

**Set production environment variable:**

```bash
vercel env add VITE_API_URL production --value "https://santosh1707-rag-question-generator-api.hf.space" --yes
```

Or in Vercel dashboard → Settings → Environment Variables.

Wait 2-3 minutes for build.

---

## ✅ Post-Deployment Verification

### Test Backend

```bash
curl https://santosh1707-rag-question-generator-api.hf.space/health
# Expected: {"status":"healthy","documents_count":0,"available_sources":[]}
```

### Test Frontend

1. Open your Vercel URL
2. Open DevTools (F12) → Console & Network
3. Upload a PDF/TXT/DOCX/PPTX file
4. Verify:
   - Upload request succeeds (200)
   - Document appears in list
   - Can generate quiz (5 questions, ~30s)
   - Can generate learning content

---

## 📝 Environment Setup Summary

### Hugging Face (Backend)

| Variable | Value |
|----------|-------|
| `MISTRAL_API_KEY` | From mistral.ai |
| `HUGGINGFACEHUB_API_TOKEN` | From huggingface.co/settings/tokens |
| `PORT` | `8000` |

*(Groq and Gemini keys optional)*

### Vercel (Frontend)

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://santosh1707-rag-question-generator-api.hf.space` |

---

## 🎯 Expected URLs

```
Frontend: https://frontend-xxx.vercel.app (or your custom Vercel URL)
Backend:  https://santosh1707-rag-question-generator-api.hf.space
```

---

## 🔍 Quick Troubleshooting

### Backend build fails on Hugging Face
- ✅ All 5 env vars set? (MISTRAL_API_KEY, HUGGINGFACEHUB_API_TOKEN, PORT=8000)
- ✅ Check Space → Logs for errors
- ✅ First build downloads ~500MB model - may need longer timeout

### Frontend can't connect
- ✅ Backend health check passes?
- ✅ `VITE_API_URL` correct in Vercel production?
- ✅ Backend URL uses `https://`
- ✅ Backend CORS allows all origins (already configured)

### Upload fails
- ✅ File < 50MB
- ✅ Format: PDF, TXT, DOCX, PPTX
- ✅ Backend has memory (free tier ~2GB)

### Generation hangs
- ✅ LLM API key has credits
- ✅ Wait up to 60 seconds (LLM is slow)
- ✅ Check backend logs

---

## 📚 Full Documentation

For detailed explanations, see:
- **`DEPLOYMENT.md`** - Comprehensive deployment guide
- **`VERCEL_DEPLOYMENT.md`** - Vercel-specific details
- **`README.md`** - Architecture, API docs, local development
- **`TESTING.md`** - Testing procedures

---

## 🎉 Success!

Your app is live when:

✅ Frontend loads without console errors
✅ Backend health returns `healthy`
✅ Can upload a document
✅ Can generate quiz questions
✅ Can generate summaries

**Need help?** Check Hugging Face Space logs and Vercel function logs.
