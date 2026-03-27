#!/bin/bash

# RAG Question Maker - Automated Deployment Script (Unix/Linux/macOS)
# This script deploys the full-stack application to Railway (backend) and Vercel (frontend)

set -e  # Exit on error

# Colors
GREEN='\033[32m'
RED='\033[31m'
YELLOW='\033[33m'
BLUE='\033[34m'
MAGENTA='\033[35m'
BOLD='\033[1m'
RESET='\033[0m'

info() {
    echo -e "${BLUE}ℹ️  $1${RESET}"
}

success() {
    echo -e "${GREEN}✅ $1${RESET}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${RESET}"
}

error() {
    echo -e "${RED}❌ $1${RESET}"
}

header() {
    echo -e "\n${MAGENTA}=== $1 ===${RESET}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

wait_for_backend() {
    local url=$1
    local timeout=${2:-300}

    info "Waiting for backend to become healthy (timeout: ${timeout}s)..."

    local start_time=$(date +%s)
    while true; do
        if curl -s "$url/health" | grep -q "healthy"; then
            success "Backend is healthy!"
            return 0
        fi

        local elapsed=$(($(date +%s) - start_time))
        if [ $elapsed -gt $timeout ]; then
            error "Backend did not become healthy within ${timeout} seconds"
            return 1
        fi

        info "Backend starting... (${elapsed}s)"
        sleep 3
    done
}

check_prerequisites() {
    header "Checking Prerequisites"

    local all_good=true

    for tool in git node npm python3; do
        if check_command $tool; then
            version=$($tool --version 2>&1 | head -1)
            success "$tool is installed: $version"
        else
            error "$tool is NOT installed. Please install it first."
            all_good=false
        fi
    done

    for tool in vercel railway; do
        if check_command $tool; then
            version=$($tool --version 2>&1 | head -1)
            success "$tool is installed: $version"
        else
            warning "$tool is NOT installed. Will try to install or skip."
        fi
    done

    return $all_good
}

install_missing() {
    header "Installing Missing Dependencies"

    # Vercel CLI
    if ! check_command vercel; then
        info "Installing Vercel CLI..."
        npm install -g vercel || warning "Failed to install Vercel CLI"
    fi

    # Railway CLI
    if ! check_command railway; then
        info "Installing Railway CLI..."
        npm install -g @railway/cli || warning "Failed to install Railway CLI"
    fi
}

login_services() {
    header "Logging into Cloud Services"

    if check_command vercel; then
        info "Logging into Vercel..."
        vercel login 2>/dev/null || warning "Vercel login failed or already logged in"
    fi

    if check_command railway; then
        info "Logging into Railway..."
        railway login 2>/dev/null || warning "Railway login failed or already logged in"
    fi
}

deploy_backend() {
    header "Deploying Backend to Railway"

    if ! check_command railway; then
        error "Railway CLI not installed. Skipping backend deployment."
        return
    fi

    cd backend

    # Check if project exists
    info "Checking existing Railway projects..."
    if railway projects 2>&1 | grep -q "No projects found"; then
        info "Creating new Railway project..."
        railway init --name "rag-question-maker-backend" --template "python" 2>/dev/null || true
    fi

    # Set environment variables
    info "Setting environment variables..."
    railway variables set MISTRAL_API_KEY="$MISTRAL_API_KEY" 2>/dev/null || true
    if [ -n "$HUGGINGFACE_TOKEN" ]; then
        railway variables set HUGGINGFACEHUB_API_TOKEN="$HUGGINGFACE_TOKEN" 2>/dev/null || true
    fi

    # Deploy
    info "Deploying to Railway (this may take 5-10 minutes)..."
    railway up 2>&1 | tee railway_deploy.log

    # Get URL
    sleep 5
    backend_url=$(railway domain list 2>&1 | grep -o 'https://[^ ]*\.up\.railway\.app' | head -1)

    if [ -n "$backend_url" ]; then
        success "Backend deployed to: $backend_url"
    else
        warning "Could not determine backend URL automatically."
        read -p "Please enter your backend URL (e.g., https://xxx.up.railway.app): " backend_url
    fi

    # Wait for health
    if [ -n "$backend_url" ]; then
        wait_for_backend "$backend_url"
    fi

    cd ..
    echo $backend_url
}

deploy_frontend() {
    local backend_url=$1

    header "Deploying Frontend to Vercel"

    if ! check_command vercel; then
        error "Vercel CLI not installed. Skipping frontend deployment."
        return
    fi

    cd frontend

    # Set environment variable
    info "Setting VITE_API_URL environment variable..."
    if [ -n "$backend_url" ]; then
        export VITE_API_URL="$backend_url"
        success "VITE_API_URL set to: $backend_url"
    else
        read -p "Enter backend URL (without trailing slash): " backend_url
        export VITE_API_URL="$backend_url"
    fi

    # Write to .env.local for local testing
    echo "VITE_API_URL=$backend_url" > .env.local

    # Build and deploy
    info "Building and deploying to Vercel (production)..."
    vercel --prod 2>&1 | tee vercel_deploy.log

    # Get URL
    sleep 3
    frontend_url=$(vercel ls 2>&1 | grep -o 'https://[^ ]*\.vercel\.app' | head -1)

    if [ -n "$frontend_url" ]; then
        success "Frontend deployed to: $frontend_url"
    else
        warning "Could not determine frontend URL automatically."
        read -p "Please enter your frontend URL (e.g., https://your-app.vercel.app): " frontend_url
    fi

    cd ..
    echo $frontend_url
}

show_summary() {
    local backend_url=$1
    local frontend_url=$2

    header "Deployment Summary"

    echo -e "\n${BOLD}Backend (API):${RESET}"
    if [ -n "$backend_url" ]; then
        success "  URL: $backend_url"
        info "  Health: $backend_url/health"
        info "  Docs: $backend_url/docs"
    else
        warning "  Not deployed"
    fi

    echo -e "\n${BOLD}Frontend (Web App):${RESET}"
    if [ -n "$frontend_url" ]; then
        success "  URL: $frontend_url"
    else
        warning "  Not deployed"
    fi

    echo -e "\n${BOLD}Next Steps:${RESET}"
    info "1. Test the application at your frontend URL"
    info "2. Upload a document to verify everything works"
    info "3. Monitor logs on Railway/Vercel dashboards"
    info "4. Set up custom domains if needed"

    echo -e "\n${BOLD}Logs:${RESET}"
    info "  - Railway: railway logs (in backend/)"
    info "  - Vercel: vercel logs (in frontend/)"

    echo -e "\n${BOLD}Environment Variables:${RESET}"
    info "  - Railway: MISTRAL_API_KEY (already set)"
    info "  - Vercel: VITE_API_URL (already set)"
    echo
}

# ============ MAIN ============

header "RAG Question Maker - Automated Deployment"
info "This script will deploy your app to Railway (backend) and Vercel (frontend)"
warning "Make sure you have:"
warning "  1. Mistral AI API key"
warning "  2. Railway account (free at railway.app)"
warning "  3. Vercel account (free at vercel.com)"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    error "This script must be run from the project root directory!"
    exit 1
fi

# Get Mistral API key
if [ -z "$MISTRAL_API_KEY" ]; then
    read -p "Enter your Mistral API key: " MISTRAL_API_KEY
    if [ -z "$MISTRAL_API_KEY" ]; then
        error "Mistral API key is required!"
        exit 1
    fi
fi

# Confirmation
echo -e "\n${BOLD}Ready to deploy:${RESET}"
info "  Backend: Railway"
info "  Frontend: Vercel"
echo ""
read -p "Continue? (y/N): " confirm
if [[ ! $confirm =~ ^[yY](es)?$ ]]; then
    info "Deployment cancelled."
    exit 0
fi

# Check prerequisites
if ! check_prerequisites; then
    error "Prerequisites not met. Please install missing tools and try again."
    exit 1
fi

# Install missing CLI tools
install_missing

# Login to services
login_services

backend_url=""
frontend_url=""

# Deploy backend
if [ "$SKIP_BACKEND" != "true" ]; then
    backend_url=$(deploy_backend)
else
    info "Skipping backend deployment (SKIP_BACKEND set)"
fi

# Deploy frontend
if [ "$SKIP_FRONTEND" != "true" ]; then
    frontend_url=$(deploy_frontend "$backend_url")
else
    info "Skipping frontend deployment (SKIP_FRONTEND set)"
fi

# Show summary
show_summary "$backend_url" "$frontend_url"

# Save deployment info
deploy_info=$(cat <<EOF
{
  "timestamp": "$(date -Iseconds)",
  "backend_url": "$backend_url",
  "frontend_url": "$frontend_url",
  "mistral_api_key_set": true
}
EOF
)

echo "$deploy_info" > DEPLOYMENT_INFO.json
success "Deployment information saved to DEPLOYMENT_INFO.json"

header "Deployment Complete!"
