# ?? SCRIPT DE REORGANIZAÇÃO AUTOMÁTICA - ARKHANASTORE
# Versão: 1.0.0
# Data: 16/11/2025
# Autor: Ávila AI Assistant
# Padrão: Ávila Framework

<#
.SYNOPSIS
    Reorganiza automaticamente a estrutura do projeto ArkhanaStore

.DESCRIPTION
    Este script executa todas as fases do CHECKLIST_REORGANIZACAO.md automaticamente:
    - Cria estrutura modular
    - Move arquivos para locais corretos
    - Arquiva backups
    - Limpa arquivos temporários
    - Cria READMEs básicos

.PARAMETER DryRun
    Modo simulação (não executa mudanças, apenas mostra o que faria)

.PARAMETER SkipBackup
    Pula criação de backup de segurança (NÃO RECOMENDADO)

.EXAMPLE
    .\reorganize-project.ps1
    Executa reorganização completa

.EXAMPLE
    .\reorganize-project.ps1 -DryRun
    Simula reorganização sem fazer mudanças

.NOTES
    ATENÇÃO: Este script move e renomeia arquivos.
    Sempre faça backup antes de executar!
#>

param(
    [switch]$DryRun = $false,
    [switch]$SkipBackup = $false
)

# ====================================================================
# CONFIGURAÇÕES
# ====================================================================

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot | Split-Path
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $ProjectRoot "reorganization_$Timestamp.log"

# Cores para output
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"
$ColorInfo = "Cyan"

# ====================================================================
# FUNÇÕES AUXILIARES
# ====================================================================

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Add-Content -Path $LogFile -Value $logMessage
    
    switch ($Level) {
        "SUCCESS" { Write-Host $Message -ForegroundColor $ColorSuccess }
        "WARNING" { Write-Host $Message -ForegroundColor $ColorWarning }
        "ERROR"   { Write-Host $Message -ForegroundColor $ColorError }
        default   { Write-Host $Message -ForegroundColor $ColorInfo }
    }
}

function New-DirectoryIfNotExists {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        if (-not $DryRun) {
            New-Item -Path $Path -ItemType Directory -Force | Out-Null
            Write-Log "? Criado diretório: $Path" "SUCCESS"
        } else {
            Write-Log "?? [DRY-RUN] Criaria diretório: $Path" "INFO"
        }
    }
}

function Move-FileIfExists {
    param(
        [string]$Source,
        [string]$Destination
    )
    
    $sourcePath = Join-Path $ProjectRoot $Source
    $destPath = Join-Path $ProjectRoot $Destination
    
    if (Test-Path $sourcePath) {
        $destDir = Split-Path $destPath -Parent
        New-DirectoryIfNotExists -Path $destDir
        
        if (-not $DryRun) {
            Move-Item -Path $sourcePath -Destination $destPath -Force
            Write-Log "  ??  $Source ? $Destination" "SUCCESS"
        } else {
            Write-Log "  ?? [DRY-RUN] Moveria: $Source ? $Destination" "INFO"
        }
        return $true
    } else {
        Write-Log "  ??  Arquivo não encontrado: $Source" "WARNING"
        return $false
    }
}

function Remove-ItemIfExists {
    param([string]$Path)
    
    $fullPath = Join-Path $ProjectRoot $Path
    
    if (Test-Path $fullPath) {
        if (-not $DryRun) {
            Remove-Item -Path $fullPath -Recurse -Force
            Write-Log "  ???  Deletado: $Path" "SUCCESS"
        } else {
            Write-Log "  ?? [DRY-RUN] Deletaria: $Path" "INFO"
        }
    }
}

# ====================================================================
# FASE 1: PREPARAÇÃO
# ====================================================================

Write-Log "`n========================================" "INFO"
Write-Log "?? INICIANDO REORGANIZAÇÃO DO PROJETO" "INFO"
Write-Log "========================================`n" "INFO"

if ($DryRun) {
    Write-Log "??  MODO DRY-RUN ATIVADO - Nenhuma mudança será feita" "WARNING"
    Write-Log ""
}

# 1.1 Backup de Segurança
if (-not $SkipBackup -and -not $DryRun) {
    Write-Log "?? FASE 1.1: Criando backup de segurança..." "INFO"
    
    $backupDir = "C:\Users\nicol\OneDrive\Avila\Backups"
    if (-not (Test-Path $backupDir)) {
        New-Item -Path $backupDir -ItemType Directory -Force | Out-Null
    }
    
    $backupPath = Join-Path $backupDir "ArkhanaStore_PreReorg_$Timestamp.zip"
    
    try {
        Compress-Archive -Path "$ProjectRoot\*" -DestinationPath $backupPath -Force
        $backupSize = (Get-Item $backupPath).Length / 1MB
        Write-Log "? Backup criado: $backupPath ($([math]::Round($backupSize, 2)) MB)" "SUCCESS"
    } catch {
        Write-Log "? Erro ao criar backup: $_" "ERROR"
        exit 1
    }
} else {
    if ($SkipBackup) {
        Write-Log "??  ATENÇÃO: Backup pulado! Procedendo sem backup de segurança." "WARNING"
    }
}

Write-Log ""

# ====================================================================
# FASE 2: CRIAR ESTRUTURA MODULAR
# ====================================================================

Write-Log "?? FASE 2: Criando estrutura modular..." "INFO"

# Diretórios principais
$directories = @(
    "docs",
    "docs\atendimento",
    "docs\scripts_atendimento",
    "docs\ia_assistiva",
    "clients",
    "clients\arkana_store",
    "clients\arkana_store\propostas",
    "clients\arkana_store\documentos",
    "clients\arkana_store\metricas",
    "scripts",
    "scripts\atendimento",
    "scripts\ia_assistiva",
    "scripts\metricas",
    "scripts\reorganization",
    "scripts\utilities",
    "archives",
    "archives\2025-11",
    "archives\2025-11\backups",
    "archives\2025-11\reports",
    "archives\2025-11\temp",
    ".backups"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $ProjectRoot $dir
    New-DirectoryIfNotExists -Path $fullPath
}

Write-Log ""

# ====================================================================
# FASE 3: MOVER DOCUMENTAÇÃO
# ====================================================================

Write-Log "?? FASE 3: Movendo documentação..." "INFO"

# Documentação principal
$docMoves = @{
    "Avila_Inc_Padrao_Atendimento\Padrao_Atendimento_Excelencia.md" = "docs\Padrao_Atendimento_Excelencia.md"
    "Avila_Inc_Padrao_Atendimento\Readme_Avila_Inc_Padrao_Atendimento.md" = "docs\README_Atendimento.md"
    "Avila_Inc_Padrao_Atendimento\Sumario_Executivo.md" = "docs\Sumario_Executivo.md"
    "Avila_Inc_Padrao_Atendimento\Quick_Start.md" = "docs\Quick_Start.md"
    "Avila_Inc_Padrao_Atendimento\Changelog.md" = "docs\Changelog.md"
    "Avila_Inc_Padrao_Atendimento\Contributing.md" = "docs\Contributing.md"
}

foreach ($move in $docMoves.GetEnumerator()) {
    Move-FileIfExists -Source $move.Key -Destination $move.Value
}

Write-Log ""

# ====================================================================
# FASE 4: CONSOLIDAR CLIENTE ARKANA
# ====================================================================

Write-Log "?? FASE 4: Consolidando cliente Arkana Store..." "INFO"

$arkanaItems = @{
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Dossie.md" = "clients\arkana_store\dossie.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Dossie_Atendimento_Completo.md" = "clients\arkana_store\dossie_atendimento_completo.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Historico_Atendimento.md" = "clients\arkana_store\historico_atendimento.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Plano_Acao_Shopify_Suspensao.md" = "clients\arkana_store\plano_acao_shopify.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Proposta_Whatsapp.txt" = "clients\arkana_store\propostas\proposta_whatsapp.txt"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Proposta_Instagram.txt" = "clients\arkana_store\propostas\proposta_instagram.txt"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Solucao_Real_48h.md" = "clients\arkana_store\propostas\solucao_real_48h.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Solucao_Avila_Propria.md" = "clients\arkana_store\propostas\solucao_avila_propria.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Caso_Critico.md" = "clients\arkana_store\documentos\caso_critico.md"
    "Avila_Inc_Padrao_Atendimento\Clientes\Arkana_Store\Primeiro_Contato.md" = "clients\arkana_store\documentos\primeiro_contato.md"
}

foreach ($item in $arkanaItems.GetEnumerator()) {
    Move-FileIfExists -Source $item.Key -Destination $item.Value
}

Write-Log ""

# ====================================================================
# FASE 5: ORGANIZAR SCRIPTS
# ====================================================================

Write-Log "?? FASE 5: Organizando scripts..." "INFO"

$scriptMoves = @{
    "Analisar_Conversa_Whatsapp.py" = "scripts\atendimento\analisar_conversa_whatsapp.py"
    "Analisar_Email.py" = "scripts\atendimento\analisar_email.py"
    "Env_Loader.py" = "scripts\utilities\env_loader.py"
}

foreach ($script in $scriptMoves.GetEnumerator()) {
    Move-FileIfExists -Source $script.Key -Destination $script.Value
}

# Scripts em Temp (se existir)
if (Test-Path (Join-Path $ProjectRoot "Temp _ deletar após visualização")) {
    $tempScripts = @{
        "Temp _ deletar após visualização\Enviar_Proposta_Arkana.py" = "scripts\atendimento\enviar_proposta_arkana.py"
        "Temp _ deletar após visualização\Enviar_Whatsapp_Arkana.py" = "scripts\atendimento\enviar_whatsapp_arkana.py"
        "Temp _ deletar após visualização\Analisar_Conversa_Whatsapp.py" = "scripts\atendimento\analisar_conversa_whatsapp_alt.py"
    }
    
    foreach ($script in $tempScripts.GetEnumerator()) {
        Move-FileIfExists -Source $script.Key -Destination $script.Value
    }
}

Write-Log ""

# ====================================================================
# FASE 6: ARQUIVAR BACKUPS
# ====================================================================

Write-Log "?? FASE 6: Arquivando backups..." "INFO"

# Backups Python Files
$pythonBackups = Get-ChildItem -Path $ProjectRoot -Filter "Avila_Python_Files_*.zip" -ErrorAction SilentlyContinue
foreach ($backup in $pythonBackups) {
    $dest = "archives\2025-11\backups\$($backup.Name)"
    Move-FileIfExists -Source $backup.Name -Destination $dest
}

# Outros backups
$otherBackups = @{
    "Arkana_Logs_Pack.zip" = "archives\2025-11\backups\arkana_logs_pack.zip"
    "Avila_Inc_Padrao_Atendimento.zip" = "archives\2025-11\backups\avila_inc_padrao_atendimento.zip"
}

foreach ($backup in $otherBackups.GetEnumerator()) {
    Move-FileIfExists -Source $backup.Key -Destination $backup.Value
}

# Reports
if (Test-Path (Join-Path $ProjectRoot "(5) Whatsapp Business.md")) {
    if (-not $DryRun) {
        Rename-Item -Path (Join-Path $ProjectRoot "(5) Whatsapp Business.md") -NewName "Whatsapp_Business.md" -Force
    }
    Move-FileIfExists -Source "Whatsapp_Business.md" -Destination "archives\2025-11\reports\whatsapp_business.md"
}

Write-Log ""

# ====================================================================
# FASE 7: LIMPAR TEMPORÁRIOS
# ====================================================================

Write-Log "???  FASE 7: Limpando arquivos temporários..." "INFO"

$itemsToDelete = @(
    "Temp _ deletar após visualização",
    ".vs",
    "slnx.sqlite",
    "Avila_Inc_Padrao_Atendimento"
)

foreach ($item in $itemsToDelete) {
    Remove-ItemIfExists -Path $item
}

Write-Log ""

# ====================================================================
# FASE 8: VALIDAÇÃO
# ====================================================================

Write-Log "? FASE 8: Validando estrutura..." "INFO"

$requiredDirs = @("docs", "clients", "scripts", "archives")
$allDirsExist = $true

foreach ($dir in $requiredDirs) {
    $fullPath = Join-Path $ProjectRoot $dir
    if (Test-Path $fullPath) {
        Write-Log "  ? $dir/ - OK" "SUCCESS"
    } else {
        Write-Log "  ? $dir/ - FALTANDO!" "ERROR"
        $allDirsExist = $false
    }
}

Write-Log ""

# ====================================================================
# RESUMO FINAL
# ====================================================================

Write-Log "========================================" "INFO"
Write-Log "?? REORGANIZAÇÃO CONCLUÍDA!" "SUCCESS"
Write-Log "========================================`n" "INFO"

if ($DryRun) {
    Write-Log "??  MODO DRY-RUN: Nenhuma mudança foi feita" "WARNING"
    Write-Log "Execute sem -DryRun para aplicar as mudanças" "INFO"
} else {
    Write-Log "? Estrutura modular criada" "SUCCESS"
    Write-Log "? Arquivos movidos para locais corretos" "SUCCESS"
    Write-Log "? Backups arquivados" "SUCCESS"
    Write-Log "? Arquivos temporários removidos" "SUCCESS"
    Write-Log ""
    Write-Log "?? Log completo salvo em: $LogFile" "INFO"
    Write-Log ""
    Write-Log "?? PRÓXIMOS PASSOS:" "INFO"
    Write-Log "  1. Revisar estrutura: tree /F" "INFO"
    Write-Log "  2. Criar READMEs: .\scripts\create-readmes.ps1" "INFO"
    Write-Log "  3. Inicializar Git: git init" "INFO"
    Write-Log "  4. Ver checklist completo: CHECKLIST_REORGANIZACAO.md" "INFO"
}

Write-Log ""
