# Hugging Face Spaces Deployment Script
# Run this script to deploy the backend to Hugging Face Spaces

param(
    [string]$SpaceName = "rag-question-generator-api",
    [string]$Username = "santosh1707",
    [string]$HFToken = "",  # Optional: pass your Hugging Face token
    [switch]$UseSSH = $false
)

Write-Host "=== Hugging Face Backend Deployment ===" -ForegroundColor Cyan

# 1. Clone the Space repository
Write-Host "`n1. Cloning Space repository..." -ForegroundColor Yellow

if ($UseSSH) {
    $spaceRepo = "git@hf.space:$Username/$SpaceName.git"
} else {
    $spaceRepo = "https://huggingface.co/spaces/$Username/$SpaceName"
}

git clone $spaceRepo
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to clone repository. Make sure the Space is created at $spaceRepo" -ForegroundColor Red
    Write-Host "Note: If using HTTPS, you may need to provide an access token when prompted." -ForegroundColor Yellow
    exit 1
}

cd $SpaceName

# 2. Copy necessary files from project
Write-Host "`n2. Copying project files..." -ForegroundColor Yellow
$projectRoot = "..\"

# Create directories if they don't exist
New-Item -ItemType Directory -Force -Path "data" | Out-Null
New-Item -ItemType Directory -Force -Path "data/vector_store" | Out-Null
New-Item -ItemType Directory -Force -Path "data/uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "data/pdf" | Out-Null
New-Item -ItemType Directory -Force -Path "data/textfiles" | Out-Null
New-Item -ItemType Directory -Force -Path "data/docx" | Out-Null
New-Item -ItemType Directory -Force -Path "data/pptx" | Out-Null

# Copy files
Copy-Item "$projectRoot\Dockerfile" -Force
Copy-Item "$projectRoot\huggingface.yml" -Force
Copy-Item "$projectRoot\requirements.txt" -Force
Copy-Item -Recurse -Force "$projectRoot\backend" -Force
Copy-Item -Recurse -Force "$projectRoot\src" -Force
if (Test-Path "$projectRoot\.dockerignore") { Copy-Item "$projectRoot\.dockerignore" -Force }
if (Test-Path "$projectRoot\.gitignore") { Copy-Item "$projectRoot\.gitignore" -Force }

# Create .gitkeep for empty directories
New-Item -Path "data/uploads/.gitkeep" -Force | Out-Null
New-Item -Path "data/vector_store/.gitkeep" -Force | Out-Null
New-Item -Path "data/pdf/.gitkeep" -Force | Out-Null
New-Item -Path "data/textfiles/.gitkeep" -Force | Out-Null
New-Item -Path "data/docx/.gitkeep" -Force | Out-Null
New-Item -Path "data/pptx/.gitkeep" -Force | Out-Null

# 3. Copy .dockerignore (already copied above)
Write-Host "`n3. .dockerignore configured..." -ForegroundColor Yellow

# 4. Commit and push
Write-Host "`n4. Committing and pushing to Hugging Face..." -ForegroundColor Yellow
git add .
git commit -m "Deploy RAG Question Generator Backend - automated"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Deployment successful!" -ForegroundColor Green
    Write-Host "`nYour Space will be available at: https://huggingface.co/spaces/$Username/$SpaceName" -ForegroundColor Cyan
    Write-Host "`nDon't forget to set these environment variables in Space Settings → Variables:" -ForegroundColor Yellow
    Write-Host "  - GROQ_API_KEY" -ForegroundColor White
    Write-Host "  - GEMINI_API_KEY" -ForegroundColor White
    Write-Host "  - MISTRAL_API_KEY" -ForegroundColor White
    Write-Host "  - HUGGINGFACEHUB_API_TOKEN" -ForegroundColor White
    Write-Host "  - PORT=8000" -ForegroundColor White
} else {
    Write-Host "`n❌ Push failed. Check your git credentials and try again." -ForegroundColor Red
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
