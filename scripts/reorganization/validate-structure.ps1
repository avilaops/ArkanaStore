# ?? SCRIPT DE VALIDAÇÃO DE ESTRUTURA - ARKHANASTORE
# Versão: 1.0.0
# Data: 16/11/2025
# Autor: Ávila AI Assistant

<#
.SYNOPSIS
    Valida a estrutura do projeto ArkhanaStore após reorganização

.DESCRIPTION
    Verifica se todos os diretórios e arquivos críticos estão nos lugares corretos

.EXAMPLE
    .\validate-structure.ps1

.NOTES
    Executar após reorganização para confirmar sucesso
#>

$ErrorActionPreference = "Continue"
$ProjectRoot = $PSScriptRoot | Split-Path | Split-Path

# Cores
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"

# ====================================================================
# VALIDAÇÕES
# ====================================================================

Write-Host "`n========================================" -ForegroundColor $ColorInfo
Write-Host "?? VALIDANDO ESTRUTURA DO PROJETO" -ForegroundColor $ColorInfo
Write-Host "========================================`n" -ForegroundColor $ColorInfo

$totalChecks = 0
$passedChecks = 0
$failedChecks = 0

function Test-DirectoryStructure {
    param([string]$Path, [string]$Description)
    
    $script:totalChecks++
    $fullPath = Join-Path $ProjectRoot $Path
    
    if (Test-Path $fullPath) {
        Write-Host "? $Description" -ForegroundColor $ColorSuccess
        $script:passedChecks++
        return $true
    } else {
        Write-Host "? $Description - FALTANDO!" -ForegroundColor $ColorError
        Write-Host "   Esperado em: $Path" -ForegroundColor $ColorWarning
        $script:failedChecks++
        return $false
    }
}

# ====================================================================
# VALIDAR DIRETÓRIOS PRINCIPAIS
# ====================================================================

Write-Host "?? Diretórios Principais:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "docs" "docs/"
Test-DirectoryStructure "clients" "clients/"
Test-DirectoryStructure "scripts" "scripts/"
Test-DirectoryStructure "archives" "archives/"
Test-DirectoryStructure ".backups" ".backups/"
Write-Host ""

# ====================================================================
# VALIDAR SUBDIRETÓRIOS DOCS
# ====================================================================

Write-Host "?? Subdiretórios Documentação:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "docs\atendimento" "docs/atendimento/"
Test-DirectoryStructure "docs\scripts_atendimento" "docs/scripts_atendimento/"
Test-DirectoryStructure "docs\ia_assistiva" "docs/ia_assistiva/"
Write-Host ""

# ====================================================================
# VALIDAR CLIENTE ARKANA
# ====================================================================

Write-Host "?? Cliente Arkana Store:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "clients\arkana_store" "clients/arkana_store/"
Test-DirectoryStructure "clients\arkana_store\propostas" "clients/arkana_store/propostas/"
Test-DirectoryStructure "clients\arkana_store\documentos" "clients/arkana_store/documentos/"
Test-DirectoryStructure "clients\arkana_store\metricas" "clients/arkana_store/metricas/"
Write-Host ""

# ====================================================================
# VALIDAR SCRIPTS
# ====================================================================

Write-Host "?? Subdiretórios Scripts:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "scripts\atendimento" "scripts/atendimento/"
Test-DirectoryStructure "scripts\ia_assistiva" "scripts/ia_assistiva/"
Test-DirectoryStructure "scripts\metricas" "scripts/metricas/"
Test-DirectoryStructure "scripts\reorganization" "scripts/reorganization/"
Test-DirectoryStructure "scripts\utilities" "scripts/utilities/"
Write-Host ""

# ====================================================================
# VALIDAR ARCHIVES
# ====================================================================

Write-Host "?? Subdiretórios Archives:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "archives\2025-11" "archives/2025-11/"
Test-DirectoryStructure "archives\2025-11\backups" "archives/2025-11/backups/"
Test-DirectoryStructure "archives\2025-11\reports" "archives/2025-11/reports/"
Write-Host ""

# ====================================================================
# VALIDAR ARQUIVOS CRÍTICOS
# ====================================================================

Write-Host "?? Arquivos Críticos:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "README.md" "README.md (root)"
Test-DirectoryStructure "ANALISE_COMPLETA_ARKHANASTORE.md" "ANALISE_COMPLETA_ARKHANASTORE.md"
Test-DirectoryStructure "ESTRUTURA_PROJETO.md" "ESTRUTURA_PROJETO.md"
Test-DirectoryStructure "CHECKLIST_REORGANIZACAO.md" "CHECKLIST_REORGANIZACAO.md"
Test-DirectoryStructure ".gitignore" ".gitignore"
Write-Host ""

# ====================================================================
# VALIDAR DOCUMENTAÇÃO
# ====================================================================

Write-Host "?? Documentos Principais:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "docs\Padrao_Atendimento_Excelencia.md" "Padrão de Atendimento"
Test-DirectoryStructure "docs\README_Atendimento.md" "README Atendimento"
Test-DirectoryStructure "docs\Sumario_Executivo.md" "Sumário Executivo"
Write-Host ""

# ====================================================================
# VALIDAR CLIENTE ARQUIVOS
# ====================================================================

Write-Host "?? Arquivos Cliente Arkana:" -ForegroundColor $ColorInfo
Test-DirectoryStructure "clients\arkana_store\dossie.md" "Dossiê"
Test-DirectoryStructure "clients\arkana_store\historico_atendimento.md" "Histórico"
Test-DirectoryStructure "clients\arkana_store\plano_acao_shopify.md" "Plano de Ação"
Write-Host ""

# ====================================================================
# VERIFICAR ROOT LIMPO
# ====================================================================

Write-Host "?? Verificando limpeza do root:" -ForegroundColor $ColorInfo

$rootItems = Get-ChildItem -Path $ProjectRoot -File | Where-Object { 
    $_.Name -notmatch "\.md$|\.gitignore$"
}

if ($rootItems.Count -eq 0) {
    Write-Host "? Root limpo (apenas .md e .gitignore)" -ForegroundColor $ColorSuccess
    $passedChecks++
} else {
    Write-Host "??  Arquivos soltos no root:" -ForegroundColor $ColorWarning
    foreach ($item in $rootItems) {
        Write-Host "   - $($item.Name)" -ForegroundColor $ColorWarning
    }
    $failedChecks++
}
$totalChecks++

Write-Host ""

# ====================================================================
# VERIFICAR BACKUPS ARQUIVADOS
# ====================================================================

Write-Host "?? Verificando backups arquivados:" -ForegroundColor $ColorInfo

$backupsDir = Join-Path $ProjectRoot "archives\2025-11\backups"
if (Test-Path $backupsDir) {
    $backups = Get-ChildItem -Path $backupsDir -Filter "*.zip"
    if ($backups.Count -gt 0) {
        Write-Host "? $($backups.Count) backups arquivados" -ForegroundColor $ColorSuccess
        $passedChecks++
    } else {
        Write-Host "??  Nenhum backup encontrado em archives/" -ForegroundColor $ColorWarning
        $failedChecks++
    }
} else {
    Write-Host "? Diretório de backups não existe" -ForegroundColor $ColorError
    $failedChecks++
}
$totalChecks++

Write-Host ""

# ====================================================================
# ESTATÍSTICAS
# ====================================================================

$successRate = if ($totalChecks -gt 0) { 
    [math]::Round(($passedChecks / $totalChecks) * 100, 1) 
} else { 
    0 
}

Write-Host "========================================" -ForegroundColor $ColorInfo
Write-Host "?? RESULTADO DA VALIDAÇÃO" -ForegroundColor $ColorInfo
Write-Host "========================================`n" -ForegroundColor $ColorInfo

Write-Host "Total de verificações: $totalChecks" -ForegroundColor $ColorInfo
Write-Host "? Aprovadas: $passedChecks" -ForegroundColor $ColorSuccess
Write-Host "? Reprovadas: $failedChecks" -ForegroundColor $(if ($failedChecks -gt 0) { $ColorError } else { $ColorSuccess })
Write-Host "?? Taxa de sucesso: $successRate%" -ForegroundColor $(
    if ($successRate -ge 90) { $ColorSuccess }
    elseif ($successRate -ge 70) { $ColorWarning }
    else { $ColorError }
)

Write-Host ""

if ($successRate -eq 100) {
    Write-Host "?? ESTRUTURA PERFEITA!" -ForegroundColor $ColorSuccess
    Write-Host "Projeto reorganizado com sucesso!" -ForegroundColor $ColorSuccess
} elseif ($successRate -ge 90) {
    Write-Host "? ESTRUTURA BOA" -ForegroundColor $ColorSuccess
    Write-Host "Pequenos ajustes podem ser necessários" -ForegroundColor $ColorWarning
} elseif ($successRate -ge 70) {
    Write-Host "??  ESTRUTURA PARCIAL" -ForegroundColor $ColorWarning
    Write-Host "Revisar itens reprovados e completar reorganização" -ForegroundColor $ColorWarning
} else {
    Write-Host "? ESTRUTURA INCOMPLETA" -ForegroundColor $ColorError
    Write-Host "Executar reorganização novamente" -ForegroundColor $ColorError
}

Write-Host "`n========================================`n" -ForegroundColor $ColorInfo

# Retornar código de saída
exit $(if ($successRate -eq 100) { 0 } else { 1 })
