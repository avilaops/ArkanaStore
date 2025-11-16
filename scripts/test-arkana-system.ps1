# ===================================================================
# ?? TESTE AUTOMÁTICO - ARKANA STORE V2
# ===================================================================
# 
# Testa toda a stack: Site, Database, Campanhas
# 
# Uso: .\test-arkana-system.ps1
# 
# Data: 16/11/2025

Write-Host "`n" -NoNewline
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "?? ARKANA STORE V2 - TESTE AUTOMÁTICO" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0

# ===================================================================
# TESTE 1: Verificar Arquivos
# ===================================================================

Write-Host "?? TESTE 1: Verificando arquivos..." -ForegroundColor Blue

$requiredFiles = @(
    "arkana-store-v2.html",
    "arkana-admin-panel.html",
    "automation\admin\arkana_database.py",
    "automation\admin\api_server.py",
    "automation\admin\requirements.txt",
    "config\.env.arkana.production"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ? $file" -ForegroundColor Green
    } else {
        Write-Host "  ? $file (NÃO ENCONTRADO)" -ForegroundColor Red
        $ErrorCount++
    }
}

# ===================================================================
# TESTE 2: Verificar Python
# ===================================================================

Write-Host "`n?? TESTE 2: Verificando Python..." -ForegroundColor Blue

try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ? Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ? Python NÃO instalado!" -ForegroundColor Red
    Write-Host "  ?? Instalar: winget install Python.Python.3.12" -ForegroundColor Yellow
    $ErrorCount++
}

# ===================================================================
# TESTE 3: Testar Database
# ===================================================================

Write-Host "`n??? TESTE 3: Testando SQLite Database..." -ForegroundColor Blue

try {
    Push-Location "automation\admin"
    
    $dbTest = python -c @"
from arkana_database import ArkanaDatabase
db = ArkanaDatabase()
print('? Database OK')
db.close()
"@
    
    Write-Host "  $dbTest" -ForegroundColor Green
    
    # Verificar se arquivo foi criado
    if (Test-Path "..\..\data\arkana_store.db") {
        $dbSize = (Get-Item "..\..\data\arkana_store.db").Length
        Write-Host "  ? Database criado: $dbSize bytes" -ForegroundColor Green
    } else {
        Write-Host "  ? Database NÃO foi criado" -ForegroundColor Red
        $ErrorCount++
    }
    
    Pop-Location
    
} catch {
    Write-Host "  ? Erro ao testar database: $_" -ForegroundColor Red
    $ErrorCount++
    Pop-Location
}

# ===================================================================
# TESTE 4: Verificar Templates Email
# ===================================================================

Write-Host "`n?? TESTE 4: Verificando templates email..." -ForegroundColor Blue

$marketingPath = "C:\Users\nicol\OneDrive\Avila\1.1 - Avilainc\Marketing"

$templates = @(
    "Promo_Campaign.html",
    "Newsletter.html",
    "Followup.html",
    "Outreach.html"
)

foreach ($template in $templates) {
    $fullPath = Join-Path $marketingPath $template
    if (Test-Path $fullPath) {
        Write-Host "  ? $template" -ForegroundColor Green
    } else {
        Write-Host "  ?? $template (usará fallback)" -ForegroundColor Yellow
    }
}

# ===================================================================
# TESTE 5: Abrir Sites (Browser Test)
# ===================================================================

Write-Host "`n?? TESTE 5: Abrindo sites no navegador..." -ForegroundColor Blue

try {
    Start-Process "arkana-store-v2.html"
    Write-Host "  ? Site cliente aberto!" -ForegroundColor Green
    
    Start-Sleep -Seconds 2
    
    Start-Process "arkana-admin-panel.html"
    Write-Host "  ? Painel admin aberto!" -ForegroundColor Green
    
} catch {
    Write-Host "  ? Erro ao abrir sites: $_" -ForegroundColor Red
    $ErrorCount++
}

# ===================================================================
# TESTE 6: API Health Check (se rodando)
# ===================================================================

Write-Host "`n?? TESTE 6: Verificando API..." -ForegroundColor Blue

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing -TimeoutSec 2 2>$null
    $health = $response.Content | ConvertFrom-Json
    
    if ($health.status -eq "ok") {
        Write-Host "  ? API rodando: $($health.service) v$($health.version)" -ForegroundColor Green
    }
    
} catch {
    Write-Host "  ?? API offline (não iniciada)" -ForegroundColor Yellow
    Write-Host "  ?? Para iniciar: cd automation\admin; python api_server.py" -ForegroundColor Cyan
}

# ===================================================================
# RESUMO
# ===================================================================

Write-Host "`n" -NoNewline
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "?? RESUMO DO TESTE" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

if ($ErrorCount -eq 0) {
    Write-Host "? TODOS OS TESTES PASSARAM!" -ForegroundColor Green
    Write-Host ""
    Write-Host "?? Sistema Arkana Store V2 está funcionando!" -ForegroundColor Green
    Write-Host ""
    Write-Host "?? Próximos passos:" -ForegroundColor Cyan
    Write-Host "  1. Veja os sites abertos no navegador" -ForegroundColor White
    Write-Host "  2. Teste o toggle dia/noite (canto superior direito)" -ForegroundColor White
    Write-Host "  3. Clique 'Comprar' e veja o formulário de cadastro" -ForegroundColor White
    Write-Host "  4. (Opcional) Inicie a API: cd automation\admin; python api_server.py" -ForegroundColor White
    
} else {
    Write-Host "?? $ErrorCount erro(s) encontrado(s)" -ForegroundColor Red
    Write-Host ""
    Write-Host "?? Verifique os erros acima e corrija" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ===================================================================
# MENU INTERATIVO
# ===================================================================

Write-Host "O que deseja fazer?" -ForegroundColor Cyan
Write-Host "  1. Abrir site cliente (arkana-store-v2.html)" -ForegroundColor White
Write-Host "  2. Abrir painel admin" -ForegroundColor White
Write-Host "  3. Iniciar backend API" -ForegroundColor White
Write-Host "  4. Testar database SQLite" -ForegroundColor White
Write-Host "  5. Ver documentação" -ForegroundColor White
Write-Host "  6. Sair" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Escolha uma opção (1-6)"

switch ($choice) {
    "1" { 
        Start-Process "arkana-store-v2.html"
        Write-Host "? Site aberto!" -ForegroundColor Green
    }
    "2" { 
        Start-Process "arkana-admin-panel.html"
        Write-Host "? Painel aberto!" -ForegroundColor Green
    }
    "3" { 
        Write-Host "?? Iniciando API..." -ForegroundColor Yellow
        Push-Location "automation\admin"
        python api_server.py
        Pop-Location
    }
    "4" { 
        Write-Host "?? Testando database..." -ForegroundColor Yellow
        Push-Location "automation\admin"
        python arkana_database.py
        Pop-Location
    }
    "5" { 
        Start-Process "SISTEMA_V2_SQLITE_CAMPANHAS.md"
        Write-Host "? Documentação aberta!" -ForegroundColor Green
    }
    "6" { 
        Write-Host "?? Até logo!" -ForegroundColor Cyan
    }
    default {
        Write-Host "? Opção inválida" -ForegroundColor Red
    }
}
