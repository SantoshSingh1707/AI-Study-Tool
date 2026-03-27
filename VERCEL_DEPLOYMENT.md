# 🚀 Deploy on Vercel

This guide covers deploying the RAG Question Maker on Vercel (frontend) and Railway (backend).

---

## 📋 Prerequisites

- **GitHub account** (Vercel integrates with GitHub)
- **Vercel account** (free at [vercel.com](https://vercel.com))
- **Railway account** for backend (free tier available)
- **Mistral AI API key** (from [mistral.ai](https://mistral.ai))

---

## 🏗️ Architecture

```
Vercel (Frontend) → Railway (Backend) → Mistral AI
    │                      │
    └──────HTTP────────────┘
```

---

## Part 1: Deploy Backend to Railway

### 1.1 Create Railway Project

1. Go to [Railway.app](https://railway.app) and sign in
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository: `SantoshSingh1707/AI-Study-Tool`
4. Choose to deploy only the `backend` directory:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 1.2 Set Environment Variables on Railway

In your Railway project settings, add these environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `MISTRAL_API_KEY` | Your Mistral API key | Required for LLM |
| `HUGGINGFACEHUB_API_TOKEN` | Your HuggingFace token (optional) | For embedding model downloads |

Railway will automatically set `PORT` environment variable.

### 1.3 Get Backend URL

After deployment, Railway will provide a URL like:
```
https://your-project.up.railway.app
```

**Save this URL** - you'll need it for the frontend configuration.

---

## Part 2: Deploy Frontend to Vercel

### 2.1 Prepare Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Create a local environment file:
   ```bash
   cp .env.local.example .env.local
   ```

3. Edit `.env.local` and set your backend URL:
   ```
   VITE_API_URL=https://your-backend.up.railway.app
   ```

   **Important**: Use `https://` for your Railway backend URL.

### 2.2 Deploy to Vercel

#### Option A: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   cd frontend
   vercel --prod
   ```

4. Follow prompts:
   - Set up and deploy? **Yes**
   - Which scope? **Your account**
   - Link to existing project? **No**
   - Project name? **rag-question-maker** (or your choice)
   - In which directory is your code located? **.** (current directory)
   - Want to override settings? **No**

5. Vercel will deploy and give you a URL like:
   ```
   https://rag-question-maker.vercel.app
   ```

#### Option B: Using Vercel Dashboard (GitHub Integration)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
5. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-backend.up.railway.app`
6. Click **"Deploy"**

### 2.3 Verify Deployment

1. Wait for Vercel to build (2-3 minutes)
2. Once deployed, open your Vercel URL
3. The frontend should load and connect to your backend
4. Try uploading a document to test the connection

---

## 🔧 Troubleshooting

### CORS Issues

If you see CORS errors in the browser console:

1. Check that the backend VITE_API_URL is correct
2. Ensure backend CORS allows your Vercel frontend domain
3. The current backend config allows all origins (`"*"`), but you may want to restrict it later

### Backend Connection Fails

1. Verify backend is running on Railway
2. Check that `VITE_API_URL` environment variable is set correctly in Vercel
3. Test the backend API directly:
   ```
   https://your-backend.up.railway.app/health
   ```
   Should return: `{"status":"healthy",...}`

### Build Errors on Vercel

If the build fails:
1. Ensure Node.js version is 18+ (Vercel uses this by default)
2. Check that all dependencies in `package.json` are correct
3. Ensure `vite.config.js` doesn't have any OS-specific paths

### Upload Not Working

1. Check browser DevTools → Network tab for `/api/upload` request
2. Verify the request goes to `https://your-backend.up.railway.app/api/upload`
3. Check Railway logs for any errors (large files may timeout)

---

## 🔐 Environment Variables Reference

### Vercel (Frontend)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend API URL (e.g., `https://your-app.up.railway.app`) |

### Railway (Backend)

| Variable | Required | Description |
|----------|----------|-------------|
| `MISTRAL_API_KEY` | Yes | Mistral AI API key |
| `HUGGINGFACEHUB_API_TOKEN` | No | HuggingFace token for model downloads |

---

## 📊 Deployment Checklist

- [ ] Backend deployed to Railway
- [ ] Backend health endpoint returns `{"status":"healthy"}`
- [ ] Mistral API key set in Railway environment
- [ ] Frontend `.env.local` updated with backend URL
- [ ] Frontend deployed to Vercel
- [ ] Vercel environment variable `VITE_API_URL` set
- [ ] Frontend loads without errors
- [ ] Can upload a document and see it in the list
- [ ] Can generate quiz/questions

---

## 🔄 Updates & Redeployment

### Frontend Updates

Push to GitHub → Vercel will auto-deploy (if enabled):
```bash
git add .
git commit -m "Update frontend"
git push origin main
```

Or manually redeploy from Vercel dashboard.

### Backend Updates

Railway will auto-deploy on GitHub push:
```bash
git add backend/
git commit -m "Update backend"
git push origin main
```

Or manually trigger redeploy from Railway dashboard.

---

## 💡 Production Considerations

1. **Add Custom Domain**: In Vercel dashboard, add your own domain
2. **Enable HTTPS**: Automatic with Vercel
3. **Monitor Backend**: Railway provides logs and metrics
4. **Rate Limiting**: Consider adding rate limiting to backend
5. **File Size Limits**: Railway has memory limits; large PDFs may fail
6. **Database Persistence**: Railway volumes persist but may be reset; consider external storage
7. **API Key Security**: Never commit `.env` files; use Railway/Vercel env vars

---

## 🎉 Done!

Your RAG Question Maker is now live on the internet! Share the Vercel URL with others.

For issues, check:
- Vercel logs: Dashboard → Project → Functions
- Railway logs: Dashboard → Project → Logs
- Browser console for CORS/network errors
