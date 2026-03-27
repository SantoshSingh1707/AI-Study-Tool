# Deploy Frontend to Vercel
param(
    [string]$FrontendPath = "frontend",
    [switch]$Force = $false
)

Write-Host "=== Vercel Frontend Deployment ===" -ForegroundColor Cyan

# Check if in correct directory
if (-not (Test-Path $FrontendPath)) {
    Write-Host "Error: Frontend directory not found at $FrontendPath" -ForegroundColor Red
    exit 1
}

cd $FrontendPath

# Check if .env.local exists
if (-not (Test-Path ".env.local")) {
    Write-Host "Warning: .env.local not found. Creating from example..." -ForegroundColor Yellow
    Copy-Item ".env.local.example" ".env.local"
}

# Check if .env.production exists
if (-not (Test-Path ".env.production")) {
    Write-Host "Warning: .env.production not found. Creating..." -ForegroundColor Yellow
    @"
VITE_API_URL=https://santosh1707-rag-question-generator-api.hf.space
"@ | Out-File -FilePath ".env.production" -Encoding UTF8
}

# Build the project first
Write-Host "`n1. Building frontend..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Build failed" -ForegroundColor Red
    exit 1
}

# Deploy to Vercel
Write-Host "`n2. Deploying to Vercel..." -ForegroundColor Yellow

if ($Force) {
    vercel --prod --force
} else {
    vercel --prod
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Frontend deployed successfully!" -ForegroundColor Green
    Write-Host "`nIMPORTANT: Set production environment variable in Vercel dashboard:" -ForegroundColor Cyan
    Write-Host "  VITE_API_URL=https://santosh1707-rag-question-generator-api.hf.space" -ForegroundColor White
    Write-Host "`nThen trigger a redeploy for the change to take effect." -ForegroundColor Yellow
} else {
    Write-Host "`n❌ Deployment failed. Check the errors above." -ForegroundColor Red
}

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
