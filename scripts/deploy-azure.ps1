# ========================================================================
# ARKANA STORE - Deploy Azure Script
# ========================================================================
# Uso: .\scripts\deploy-azure.ps1 [-Environment prod|staging|dev]
# ========================================================================

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'staging', 'prod')]
    [string]$Environment = 'prod',
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup = 'arkana-store-rg',
    
    [Parameter(Mandatory=$false)]
    [string]$Location = 'brazilsouth'
)

$ErrorActionPreference = 'Stop'

Write-Host "???  ARKANA STORE - Azure Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Environment:     $Environment" -ForegroundColor Yellow
Write-Host "Resource Group:  $ResourceGroup" -ForegroundColor Yellow
Write-Host "Location:        $Location" -ForegroundColor Yellow
Write-Host ""

# ========================================================================
# STEP 1: Check Azure CLI
# ========================================================================

Write-Host "?? [1/6] Verificando Azure CLI..." -ForegroundColor Blue

try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "   ? Azure CLI versão $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "   ? Azure CLI não encontrado!" -ForegroundColor Red
    Write-Host "   ?? Instale: https://learn.microsoft.com/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# ========================================================================
# STEP 2: Login Azure
# ========================================================================

Write-Host ""
Write-Host "?? [2/6] Verificando autenticação Azure..." -ForegroundColor Blue

$account = az account show 2>$null | ConvertFrom-Json

if (-not $account) {
    Write-Host "   ??  Não autenticado. Abrindo login..." -ForegroundColor Yellow
    az login
    $account = az account show | ConvertFrom-Json
}

Write-Host "   ? Logado como: $($account.user.name)" -ForegroundColor Green
Write-Host "   ?? Subscription: $($account.name)" -ForegroundColor Green

# ========================================================================
# STEP 3: Create Resource Group
# ========================================================================

Write-Host ""
Write-Host "?? [3/6] Criando Resource Group..." -ForegroundColor Blue

$rgExists = az group exists --name $ResourceGroup

if ($rgExists -eq 'false') {
    Write-Host "   ?? Criando '$ResourceGroup' em $Location..." -ForegroundColor Yellow
    az group create --name $ResourceGroup --location $Location --output none
    Write-Host "   ? Resource Group criado!" -ForegroundColor Green
} else {
    Write-Host "   ? Resource Group já existe" -ForegroundColor Green
}

# ========================================================================
# STEP 4: Deploy Infrastructure (Bicep)
# ========================================================================

Write-Host ""
Write-Host "???  [4/6] Provisionando infraestrutura Azure..." -ForegroundColor Blue

az deployment group create `
    --resource-group $ResourceGroup `
    --template-file infra/main.bicep `
    --parameters environment=$Environment `
    --output table

Write-Host "   ? Infraestrutura provisionada!" -ForegroundColor Green

# ========================================================================
# STEP 5: Get Web App Name
# ========================================================================

Write-Host ""
Write-Host "?? [5/6] Obtendo informações do Web App..." -ForegroundColor Blue

$webAppName = "arkana-store-$Environment"
$webAppUrl = "https://$webAppName.azurewebsites.net"

Write-Host "   ?? Web App: $webAppName" -ForegroundColor Green
Write-Host "   ?? URL: $webAppUrl" -ForegroundColor Green

# ========================================================================
# STEP 6: Deploy Application
# ========================================================================

Write-Host ""
Write-Host "?? [6/6] Fazendo deploy da aplicação..." -ForegroundColor Blue

# Create deployment package
$deployPath = ".\deploy"
if (Test-Path $deployPath) {
    Remove-Item $deployPath -Recurse -Force
}
New-Item -ItemType Directory -Path $deployPath | Out-Null

# Copy files
Write-Host "   ?? Copiando arquivos..." -ForegroundColor Yellow

Copy-Item "arkana-store-v2.html" "$deployPath\"
Copy-Item "arkana-store-landing.html" "$deployPath\"
Copy-Item "arkana-admin-panel.html" "$deployPath\index.html"
Copy-Item "automation" "$deployPath\" -Recurse

# Create startup script
@"
#!/bin/bash
cd /home/site/wwwroot
pip install -r automation/admin/requirements.txt
gunicorn --bind=0.0.0.0:8000 --timeout 600 automation.admin.api_server:app
"@ | Out-File "$deployPath\startup.sh" -Encoding UTF8

# Deploy using zip
Write-Host "   ?? Criando pacote de deploy..." -ForegroundColor Yellow
Compress-Archive -Path "$deployPath\*" -DestinationPath "deploy.zip" -Force

Write-Host "   ?? Fazendo upload para Azure..." -ForegroundColor Yellow
az webapp deployment source config-zip `
    --resource-group $ResourceGroup `
    --name $webAppName `
    --src "deploy.zip"

# Cleanup
Remove-Item "deploy.zip" -Force
Remove-Item $deployPath -Recurse -Force

Write-Host "   ? Deploy concluído!" -ForegroundColor Green

# ========================================================================
# SUMMARY
# ========================================================================

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "?  DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "?? URLs Disponíveis:" -ForegroundColor Yellow
Write-Host "   Admin Panel:  $webAppUrl" -ForegroundColor White
Write-Host "   Site V2:      $webAppUrl/arkana-store-v2.html" -ForegroundColor White
Write-Host "   Landing Page: $webAppUrl/arkana-store-landing.html" -ForegroundColor White
Write-Host ""
Write-Host "?? API Endpoints:" -ForegroundColor Yellow
Write-Host "   Health:       $webAppUrl/health" -ForegroundColor White
Write-Host "   Customers:    $webAppUrl/api/customers" -ForegroundColor White
Write-Host "   Products:     $webAppUrl/api/products" -ForegroundColor White
Write-Host "   Orders:       $webAppUrl/api/orders" -ForegroundColor White
Write-Host ""
Write-Host "?? Próximos Passos:" -ForegroundColor Yellow
Write-Host "   1. Configure secrets no GitHub:" -ForegroundColor White
Write-Host "      - AZURE_WEBAPP_PUBLISH_PROFILE" -ForegroundColor Gray
Write-Host "   2. Configure variáveis de ambiente no Azure Portal" -ForegroundColor White
Write-Host "   3. Acesse $webAppUrl" -ForegroundColor White
Write-Host ""
Write-Host "?? Documentação: DEPLOY_AZURE.md" -ForegroundColor Cyan
Write-Host ""
