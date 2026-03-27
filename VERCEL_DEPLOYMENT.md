# 🚀 Deployment Guide: Hugging Face + Vercel

This guide covers deploying the RAG Question Maker with **Hugging Face Spaces (backend)** and **Vercel (frontend)**.

---

## 📋 Prerequisites

- **GitHub account** (for source control)
- **Hugging Face account** (free at [huggingface.co](https://huggingface.co))
- **Vercel account** (free at [vercel.com](https://vercel.com))
- **API Keys**:
  - Mistral AI API key (from [mistral.ai](https://mistral.ai))
  - Groq API key (optional, from [groq.com](https://groq.com))
  - Google Gemini API key (optional, from [makersuite.google.com](https://makersuite.google.com))

---

## 🏗️ Architecture

```
Vercel (Frontend) → Hugging Face Spaces (Backend) → Mistral AI / Groq / Gemini
    │                       │
    └──────HTTP─────────────┘
```

---

## Part 1: Deploy Backend to Hugging Face Spaces

### 1.1 Create Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in:
   - **Owner**: `santosh1707` (your username)
   - **Space name**: `rag-question-generator-api`
   - **SDK**: `Docker`
   - **Hardware**: `CPU basic` (free tier)
   - **Public/Private**: Your choice
4. Click **"Create Space"**

### 1.2 Prepare Deployment Files

From your local project root:

```powershell
# These files should already exist:
# - Dockerfile
# - backend/ (directory with main.py, config.py, etc.)
# - src/ (RAG modules)
# - requirements.txt
# - huggingface.yml (optional config)
# - .dockerignore
```

### 1.3 Deploy to Hugging Face

Use the provided deployment script:

```powershell
cd "C:\Users\Santosh\Desktop\ML-Project-Deployment\RAG-Project\Question-maker"
.\deploy-huggingface.ps1
```

The script will:
- Clone your Space repository
- Copy necessary files (Dockerfile, backend/, src/, requirements.txt)
- Set up directory structure
- Commit and push

**Alternative - Manual:**

```bash
# Clone the Space
git clone https://huggingface.co/spaces/santosh1707/rag-question-generator-api
cd rag-question-generator-api

# Copy project files
cp -r ../backend ./
cp -r ../src ./
cp ../Dockerfile ./
cp ../requirements.txt ./
cp ../huggingface.yml ./

# Create data directories
mkdir -p data/vector_store data/uploads data/pdf data/textfiles data/docx data/pptx
touch data/vector_store/.gitkeep data/uploads/.gitkeep

# Commit and push
git add .
git commit -m "Deploy backend"
git push origin main
```

### 1.4 Set Environment Variables

In your Hugging Face Space → **Settings** → **Variables**, add:

| Variable | Value | Required |
|----------|-------|----------|
| `MISTRAL_API_KEY` | Your Mistral API key | Yes |
| `GROQ_API_KEY` | Your Groq API key (optional) | No |
| `GEMINI_API_KEY` | Your Gemini API key (optional) | No |
| `HUGGINGFACEHUB_API_TOKEN` | Your Hugging Face token | Yes (for model downloads) |
| `PORT` | `8000` | Yes |

**Get Hugging Face token:** https://huggingface.co/settings/tokens → New token (Full access)

### 1.5 Wait for Build

- Hugging Face will automatically build your Docker image (5-10 minutes)
- Monitor progress on your Space page
- Once complete, test the health endpoint:
  ```
  https://santosh1707-rag-question-generator-api.hf.space/health
  ```

**Expected response:**
```json
{
  "status": "healthy",
  "documents_count": 0,
  "available_sources": []
}
```

---

## Part 2: Deploy Frontend to Vercel

### 2.1 Prepare Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Create local environment file:
   ```bash
   cp .env.local.example .env.local
   ```

   The `.env.local` should contain:
   ```
   VITE_API_URL=http://localhost:8000
   ```

   (For local development only - production is set in Vercel)

### 2.2 Deploy to Vercel

**Option A: Using Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy from frontend directory
cd frontend
vercel --prod
```

The CLI will guide you through setup. Accept defaults or specify:
- Project name: `question-maker-frontend`
- root directory: `.`

**Option B: Already Linked Project**

Your frontend is already linked to a Vercel project. Simply push:

```bash
cd frontend
git add .
git commit -m "Configure for Hugging Face backend"
git push origin main
```

Vercel will automatically deploy.

### 2.3 Set Production Environment Variable

After deployment, set the production API URL:

```bash
cd frontend
vercel env add VITE_API_URL production --value "https://santosh1707-rag-question-generator-api.hf.space" --yes
```

Or manually:
1. Go to Vercel Dashboard → Your project → Settings → Environment Variables
2. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://santosh1707-rag-question-generator-api.hf.space`
   - **Environment**: `Production`
3. Save and **redeploy** the project

### 2.4 Verify Deployment

1. Once deployed, open your Vercel URL (e.g., `https://frontend-xxx.vercel.app`)
2. Open browser DevTools → Console and Network tabs
3. Try uploading a document and generating questions
4. Check that API calls succeed (status 200)

---

## 🔧 Troubleshooting

### CORS Issues

Backend CORS is configured to allow all origins (`"*"`). If you still see CORS errors:
- Ensure backend is running and accessible
- Check backend logs in Hugging Face
- Verify backend URL in Vercel environment variables

### Backend Not Accessible

1. Verify backend health:
   ```
   https://santosh1707-rag-question-generator-api.hf.space/health
   ```
   Should return JSON with `"status":"healthy"`

2. Check backend environment variables are set correctly in Hugging Face

3. Check backend logs in Hugging Face Space → **Logs** tab

### MIME Type Errors (JS not loading)

If frontend shows "Failed to load module script" errors:
- The `vercel.json` routing configuration should properly serve static assets
- We've fixed this - if issues persist, check that `/assets/` files are being served correctly

### Build Fails on Hugging Face

Common causes:
- Missing environment variables (all required API keys)
- Network timeouts during model download (sentence-transformers downloads on first run)
- Increase Docker build timeout in Space settings (if needed)

### API Timeouts

LLM generation can take 30-60 seconds. If requests timeout:
- Backend timeout is configured for 5 minutes
- Check backend logs for errors (model loading, API rate limits)
- Ensure Mistral API key has credits

---

## 🔐 Environment Variables Reference

### Vercel (Frontend)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend API URL: `https://santosh1707-rag-question-generator-api.hf.space` |

### Hugging Face (Backend)

| Variable | Required | Description |
|----------|----------|-------------|
| `MISTRAL_API_KEY` | Yes | Mistral AI API key (for LLM) |
| `GROQ_API_KEY` | No | Groq API key (alternative LLM) |
| `GEMINI_API_KEY` | No | Google Gemini API key (alternative LLM) |
| `HUGGINGFACEHUB_API_TOKEN` | Yes | Hugging Face token (for embedding model downloads) |

---

## 📊 Deployment Checklist

- [ ] Backend Space created on Hugging Face
- [ ] Backend environment variables set (MISTRAL_API_KEY, HUGGINGFACEHUB_API_TOKEN, PORT=8000)
- [ ] Backend build completed successfully
- [ ] Backend health endpoint returns healthy status
- [ ] Frontend deployed to Vercel
- [ ] Vercel environment variable `VITE_API_URL` set to Hugging Face backend URL
- [ ] Frontend loads without console errors
- [ ] Can upload a document (PDF, TXT, DOCX, PPTX)
- [ ] Can generate quiz questions
- [ ] Can generate learning content (summary/key notes)

---

## 🔄 Updates & Redeployment

### Frontend Updates

Push to GitHub (triggers Vercel auto-deploy):
```bash
cd frontend
git add .
git commit -m "Update frontend"
git push origin main
```

Or manually:
```bash
cd frontend
vercel --prod --force
```

### Backend Updates

Push to GitHub (triggers Hugging Face auto-rebuild):
```bash
git add backend/ src/ Dockerfile requirements.txt
git commit -m "Update backend"
git push origin main
```

Or manually trigger rebuild in Hugging Face Space → **Settings** → **Recalculate**.

---

## 📝 Live URLs

**Frontend (Vercel):**
- Production: https://frontend-psi-eight-61.vercel.app
- Inspect: https://vercel.com/santosh102969-6116s-projects/frontend

**Backend (Hugging Face):**
- https://santosh1707-rag-question-generator-api.hf.space
- Health: https://santosh1707-rag-question-generator-api.hf.space/health

---

## 💡 Production Considerations

1. **Rate Limiting**: Add rate limiting to backend API endpoints
2. **File Size Limits**: Current limit is reasonable; large files may timeout
3. **Persistence**: Hugging Face Spaces have ephemeral storage - vector store persists across restarts but consider backup strategy
4. **API Key Security**: Never commit `.env` files; use platform environment variables
5. **Monitoring**: Monitor Hugging Face Space logs and Vercel function logs
6. **Custom Domains**: Add custom domains in both platforms if needed
7. **Cost Management**: Both platforms have free tiers with usage limits

---

## 🎉 Done!

Your RAG Question Maker is now live! Share the Vercel frontend URL with users.

For issues, check:
- **Vercel logs**: Dashboard → Project → Functions
- **Hugging Face logs**: Space → Logs tab
- **Browser console**: DevTools → Console & Network
