# RAG Question Maker - Automated Deployment Script
# This script deploys the full-stack application to Railway (backend) and Vercel (frontend)

param(
    [string]$MistralApiKey,
    [string]$VercelToken,
    [string]$RailwayToken,
    [switch]$SkipBackend = $false,
    [switch]$SkipFrontend = $false,
    [switch]$Force = $false
)

# ANSI color codes
$Green = "`e[32m"
$Red = "`e[31m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"
$Bold = "`e[1m"

function Write-Color {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Info {
    param([string]$Message)
    Write-Color "ℹ️  $Message" "Cyan"
}

function Write-Success {
    param([string]$Message)
    Write-Color "✅ $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-Color "⚠️  $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-Color "❌ $Message" "Red"
}

function Write-Header {
    param([string]$Message)
    Write-Color "`n=== $Message ===" "Magenta"
}

function Test-Command {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Wait-ForBackend {
    param([string]$Url, [int]$TimeoutSeconds = 300)

    Write-Info "Waiting for backend to become healthy (timeout: ${TimeoutSeconds}s)..."

    $StartTime = Get-Date
    while ($true) {
        try {
            $Response = Invoke-RestMethod "$Url/health" -Method Get -TimeoutSec 5 -ErrorAction Stop
            if ($Response.status -eq "healthy") {
                Write-Success "Backend is healthy!"
                return $true
            }
        } catch {
            #Ignore errors, keep trying
        }

        $Elapsed = (Get-Date) - $StartTime
        if ($Elapsed.TotalSeconds -gt $TimeoutSeconds) {
            Write-Error "Backend did not become healthy within $TimeoutSeconds seconds"
            return $false
        }

        Write-Info "Backend starting... ($([math]::Round($Elapsed.TotalSeconds))s)"
        Start-Sleep -Seconds 3
    }
}

function Check-Prerequisites {
    Write-Header "Checking Prerequisites"

    $RequiredTools = @("git", "node", "npm", "python")
    $OptionalTools = @("vercel", "railway")

    $AllGood = $true

    foreach ($Tool in $RequiredTools) {
        if (Test-Command $Tool) {
            $Version = & $Tool "--version" 2>&1 | Select-Object -First 1
            Write-Success "$Tool is installed: $Version"
        } else {
            Write-Error "$Tool is NOT installed. Please install it first."
            $AllGood = $false
        }
    }

    foreach ($Tool in $OptionalTools) {
        if (Test-Command $Tool) {
            $Version = & $Tool "--version" 2>&1 | Select-Object -First 1
            Write-Success "$Tool is installed: $Version"
        } else {
            Write-Warning "$Tool is NOT installed. Install for automated deployment or use manual method."
        }
    }

    return $AllGood
}

function Install-MissingDependencies {
    Write-Header "Installing Missing Dependencies"

    # Check/Install Vercel CLI
    if (-not (Test-Command "vercel")) {
        Write-Info "Installing Vercel CLI..."
        npm install -g vercel
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Vercel CLI installed"
        } else {
            Write-Warning "Failed to install Vercel CLI. Install manually: npm i -g vercel"
        }
    }

    # Check/Install Railway CLI
    if (-not (Test-Command "railway")) {
        Write-Info "Installing Railway CLI..."
        try {
            npm install -g @railway/cli
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Railway CLI installed"
            } else {
                Write-Warning "Failed to install Railway CLI. Install manually: npm i -g @railway/cli"
            }
        } catch {
            Write-Warning "Failed to install Railway CLI. Install manually: npm i -g @railway/cli"
        }
    }
}

function Login-ToServices {
    Write-Header "Logging into Cloud Services"

    # Vercel Login
    if (Test-Command "vercel") {
        Write-Info "Logging into Vercel..."
        vercel login 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Vercel login successful"
        } else {
            Write-Warning "Vercel login failed or already logged in"
        }
    }

    # Railway Login
    if (Test-Command "railway") {
        Write-Info "Logging into Railway..."
        railway login 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Railway login successful"
        } else {
            Write-Warning "Railway login failed or already logged in"
        }
    }
}

function Deploy-Backend {
    Write-Header "Deploying Backend to Railway"

    if (-not (Test-Command "railway")) {
        Write-Error "Railway CLI not installed. Skipping backend deployment."
        return $null
    }

    # Navigate to backend directory
    Push-Location "backend"

    try {
        # Check if Railway project exists
        Write-Info "Checking existing Railway projects..."
        $Projects = railway projects 2>&1

        # Initialize if needed
        if ($Projects -match "No projects found") {
            Write-Info "Creating new Railway project..."
            railway init --name "rag-question-maker-backend" --template "python" 2>&1 | Out-Null
        }

        # Set environment variables
        Write-Info "Setting environment variables..."
        railway variables set MISTRAL_API_KEY="$MistralApiKey" 2>&1 | Out-Null

        if ($HuggingFaceToken) {
            railway variables set HUGGINGFACEHUB_API_TOKEN="$HuggingFaceToken" 2>&1 | Out-Null
        }

        # Deploy
        Write-Info "Deploying to Railway (this may take 5-10 minutes)..."
        railway up 2>&1 | Tee-Object -FilePath "$PWD\railway_deploy.log"

        # Get the deployed URL
        Start-Sleep -Seconds 5
        $ProjectInfo = railway status 2>&1
        $BackendUrl = $null

        if ($ProjectInfo -match "https://.*\.up\.railway\.app") {
            $BackendUrl = $Matches[0]
            Write-Success "Backend deployed to: $BackendUrl"
        } else {
            # Try to get from domains
            $Domains = railway domain list 2>&1
            if ($Domains -match "https://(.*)\.up\.railway\.app") {
                $BackendUrl = $Matches[0]
                Write-Success "Backend URL: $BackendUrl"
            } else {
                Write-Warning "Could not determine backend URL automatically."
                $BackendUrl = Read-Host "Please enter your backend URL (e.g., https://xxx.up.railway.app)"
            }
        }

        # Wait for health
        if ($BackendUrl) {
            Wait-ForBackend -Url $BackendUrl
        }

        return $BackendUrl
    } finally {
        Pop-Location
    }
}

function Deploy-Frontend {
    param([string]$BackendUrl)

    Write-Header "Deploying Frontend to Vercel"

    if (-not (Test-Command "vercel")) {
        Write-Error "Vercel CLI not installed. Skipping frontend deployment."
        return
    }

    # Navigate to frontend directory
    Push-Location "frontend"

    try {
        # Check if Vercel project exists
        Write-Info "Checking existing Vercel projects..."
        $Projects = vercel projects ls 2>&1

        $ProjectName = "rag-question-maker"

        # If project exists, pull configuration
        if ($Projects -match $ProjectName) {
            Write-Info "Pulling existing Vercel project configuration..."
            vercel pull --yes --environment=production --token=$VercelToken 2>&1 | Out-Null
        }

        # Set environment variable
        Write-Info "Setting VITE_API_URL environment variable..."
        if ($BackendUrl) {
            $env:VITE_API_URL = $BackendUrl
            Write-Success "VITE_API_URL set to: $BackendUrl"
        } else {
            $BackendUrl = Read-Host "Enter backend URL (without trailing slash)"
            $env:VITE_API_URL = $BackendUrl
        }

        # Build and deploy
        Write-Info "Building and deploying to Vercel (production)..."
        vercel --prod --token=$VercelToken 2>&1 | Tee-Object -FilePath "$PWD\vercel_deploy.log"

        # Get deployment URL
        Start-Sleep -Seconds 3
        $DeploymentInfo = vercel ls 2>&1 | Select-String -Pattern "https://.*\.vercel\.app" | Select-Object -First 1

        if ($DeploymentInfo) {
            $FrontendUrl = $DeploymentInfo.ToString().Trim()
            Write-Success "Frontend deployed to: $FrontendUrl"
        } else {
            Write-Warning "Could not determine frontend URL automatically."
            $FrontendUrl = Read-Host "Please enter your frontend URL (e.g., https://your-app.vercel.app)"
        }

        return $FrontendUrl
    } finally {
        Pop-Location
    }
}

function Show-Summary {
    param([string]$BackendUrl, [string]$FrontendUrl)

    Write-Header "Deployment Summary"

    Write-Color "`nBackend (API):" $Bold
    if ($BackendUrl) {
        Write-Success "  URL: $BackendUrl"
        Write-Info "  Health: $BackendUrl/health"
        Write-Info "  Docs: $BackendUrl/docs"
    } else {
        Write-Warning "  Not deployed"
    }

    Write-Color "`nFrontend (Web App):" $Bold
    if ($FrontendUrl) {
        Write-Success "  URL: $FrontendUrl"
    } else {
        Write-Warning "  Not deployed"
    }

    Write-Color "`nNext Steps:" $Bold
    Write-Info "1. Test the application at your frontend URL"
    Write-Info "2. Upload a document to verify everything works"
    Write-Info "3. Monitor logs on Railway/Vercel dashboards"
    Write-Info "4. Set up custom domains if needed"

    Write-Color "`nLogs:" $Bold
    Write-Info "  - Railway logs: railway logs (in backend/)"
    Write-Info "  - Vercel logs: vercel logs (in frontend/)"

    Write-Color "`nEnvironment Variables:" $Bold
    Write-Info "  - Railway: MISTRAL_API_KEY (already set)"
    Write-Info "  - Vercel: VITE_API_URL (already set)"
    Write-Color "`n" $Reset
}

# Main execution
Write-Header "RAG Question Maker - Automated Deployment"
Write-Info "This script will deploy your app to Railway (backend) and Vercel (frontend)"
Write-Warning "Make sure you have:"
Write-Warning "  1. Mistral AI API key"
Write-Warning "  2. Railway account (free at railway.app)"
Write-Warning "  3. Vercel account (free at vercel.com)"
Write-Color ""

# Check if we're in the right directory
if (-not (Test-Path "backend/main.py") -or -not (Test-Path "frontend/package.json")) {
    Write-Error "This script must be run from the project root directory!"
    exit 1
}

# Get Mistral API key if not provided
if (-not $MistralApiKey) {
    $MistralApiKey = Read-Host "Enter your Mistral API key"
    if ([string]::IsNullOrWhiteSpace($MistralApiKey)) {
        Write-Error "Mistral API key is required!"
        exit 1
    }
}

# Get Vercel token if not in env
if (-not $VercelToken) {
    $VercelToken = $env:VERCEL_TOKEN
    if (-not $VercelToken) {
        Write-Warning "Vercel token not provided. Will use interactive login."
    }
}

# Get Railway token if not in env
if (-not $RailwayToken) {
    $RailwayToken = $env:RAILWAY_TOKEN
    if (-not $RailwayToken) {
        Write-Warning "Railway token not provided. Will use interactive login."
    }
}

# Ask for confirmation
Write-Color "`nReady to deploy:" $Bold
Write-Info "  Backend: Railway"
Write-Info "  Frontend: Vercel"
Write-Color ""
$Confirmation = Read-Host "Continue? (y/N)"
if ($Confirmation -notmatch "^[yY](es)?$") {
    Write-Info "Deployment cancelled."
    exit 0
}

# Check prerequisites
if (-not (Check-Prerequisites)) {
    Write-Error "Prerequisites not met. Please install missing tools and try again."
    exit 1
}

# Install missing CLI tools
Install-MissingDependencies

# Login to services
Login-ToServices

$BackendUrl = $null
$FrontendUrl = $null

# Deploy backend
if (-not $SkipBackend) {
    $BackendUrl = Deploy-Backend
} else {
    Write-Info "Skipping backend deployment (--SkipBackend flag set)"
}

# Deploy frontend
if (-not $SkipFrontend) {
    $FrontendUrl = Deploy-Frontend -BackendUrl $BackendUrl
} else {
    Write-Info "Skipping frontend deployment (--SkipFrontend flag set)"
}

# Show summary
Show-Summary -BackendUrl $BackendUrl -FrontendUrl $FrontendUrl

# Save deployment info to file
$DeployInfo = @{
    timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    backend_url = $BackendUrl
    frontend_url = $FrontendUrl
    mistral_api_key_set = $true
} | ConvertTo-Json -Depth 3

$DeployInfo | Out-File "DEPLOYMENT_INFO.json" -Encoding UTF8
Write-Success "Deployment information saved to DEPLOYMENT_INFO.json"

Write-Header "Deployment Complete!"
