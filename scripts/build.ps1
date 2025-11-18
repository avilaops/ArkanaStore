#!/usr/bin/env pwsh
# ================================================
# ARKANA STORE - Build & Deploy Script
# ================================================

param(
    [Parameter()]
    [ValidateSet('dev', 'staging', 'prod')]
    [string]$Environment = 'dev',

    [Parameter()]
    [switch]$Deploy,

    [Parameter()]
    [switch]$SkipTests
)

Write-Host "🏛️  ARKANA STORE - Build Script" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host ""

# ================================================
# 1. Check Prerequisites
# ================================================
Write-Host "📋 Checking prerequisites..." -ForegroundColor Green

$prerequisites = @{
    "Rust"         = "rustc --version"
    "Cargo"        = "cargo --version"
    "Trunk (WASM)" = "trunk --version"
    "Python"       = "python --version"
    "Azure CLI"    = "az --version"
}

foreach ($tool in $prerequisites.Keys) {
    $cmd = $prerequisites[$tool]
    try {
        $null = Invoke-Expression $cmd 2>&1
        Write-Host "  ✅ $tool installed" -ForegroundColor Green
    }
    catch {
        Write-Host "  ❌ $tool NOT found" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# ================================================
# 2. Build Backend (Rust API)
# ================================================
Write-Host "🦀 Building Rust Backend API..." -ForegroundColor Green

Push-Location "$PSScriptRoot\arkana-backend"

if (-not $SkipTests) {
    Write-Host "  Running tests..."
    cargo test
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Backend tests failed!" -ForegroundColor Red
        Pop-Location
        exit 1
    }
}

Write-Host "  Compiling release build..."
cargo build --release

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Backend build successful!" -ForegroundColor Green
}
else {
    Write-Host "  ❌ Backend build failed!" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location
Write-Host ""

# ================================================
# 3. Build Frontend (WASM)
# ================================================
Write-Host "🌐 Building WASM Frontend..." -ForegroundColor Green

Push-Location "$PSScriptRoot\arkana-frontend"

Write-Host "  Building with Trunk..."
trunk build --release

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Frontend build successful!" -ForegroundColor Green
    Write-Host "  📦 Output: arkana-frontend/dist/" -ForegroundColor Cyan
}
else {
    Write-Host "  ❌ Frontend build failed!" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location
Write-Host ""

# ================================================
# 4. Python Admin API
# ================================================
Write-Host "🐍 Setting up Python Admin API..." -ForegroundColor Green

Push-Location "$PSScriptRoot\automation\admin"

if (-not (Test-Path "venv")) {
    Write-Host "  Creating virtual environment..."
    python -m venv venv
}

Write-Host "  Activating venv and installing dependencies..."
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Python dependencies installed!" -ForegroundColor Green
}
else {
    Write-Host "  ❌ Failed to install Python dependencies!" -ForegroundColor Red
}

Pop-Location
Write-Host ""

# ================================================
# 5. Deploy to Azure (if requested)
# ================================================
if ($Deploy) {
    Write-Host "☁️  Deploying to Azure..." -ForegroundColor Green

    $resourceGroup = "arkana-store-$Environment-rg"
    $location = "brazilsouth"

    Write-Host "  Creating resource group: $resourceGroup"
    az group create --name $resourceGroup --location $location

    Write-Host "  Deploying infrastructure..."
    az deployment group create `
        --resource-group $resourceGroup `
        --template-file "$PSScriptRoot\infra\main.bicep" `
        --parameters "$PSScriptRoot\infra\main.parameters.json" `
        --parameters environment=$Environment

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Deployment successful!" -ForegroundColor Green

        # Get web app URL
        $webAppName = "arkana-store-$Environment"
        $url = az webapp show --name $webAppName --resource-group $resourceGroup --query "defaultHostName" -o tsv
        Write-Host ""
        Write-Host "🚀 Application deployed!" -ForegroundColor Cyan
        Write-Host "   URL: https://$url" -ForegroundColor Yellow
    }
    else {
        Write-Host "  ❌ Deployment failed!" -ForegroundColor Red
        exit 1
    }
}

# ================================================
# SUMMARY
# ================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅  BUILD COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📦 Artifacts:" -ForegroundColor Yellow
Write-Host "  - Backend API: target/release/arkana-api"
Write-Host "  - Frontend WASM: arkana-frontend/dist/"
Write-Host "  - Python Admin: automation/admin/api_server.py"
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Yellow
Write-Host "  - Run backend: ./target/release/arkana-api"
Write-Host "  - Run frontend: trunk serve (dev mode)"
Write-Host "  - Run Python admin: python automation/admin/api_server.py"
Write-Host ""
Write-Host "  Or deploy with: .\scripts\build.ps1 -Deploy -Environment prod"
Write-Host ""
