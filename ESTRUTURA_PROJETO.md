# ??? ESTRUTURA DO PROJETO - ARKHANASTORE

> **Versão**: 1.0.0  
> **Data**: 16/11/2025  
> **Padrão**: Ávila Framework Architecture  
> **Autor**: Ávila AI Assistant

---

## ?? ÁRVORE DE DIRETÓRIOS (Estrutura Proposta)

```
ArkhanaStore/
?
??? ?? README.md                          # Navegação principal do projeto
??? ?? ANALISE_COMPLETA_ARKHANASTORE.md   # Este documento de análise
??? ?? ESTRUTURA_PROJETO.md               # Você está aqui!
??? ?? CHECKLIST_REORGANIZACAO.md         # Passo a passo de reorganização
??? ?? CHANGELOG.md                       # Histórico de versões
??? ?? CONTRIBUTING.md                    # Como contribuir
??? ?? .gitignore                         # Arquivos ignorados pelo Git
?
??? ?? docs/                              # Documentação completa
?   ??? README.md                         # Índice da documentação
?   ??? Padrao_Atendimento_Excelencia.md  # Documento mestre (38 páginas)
?   ??? Quick_Start.md                    # Guia rápido de início
?   ??? Sumario_Executivo.md              # Resumo executivo
?   ??? Contributing.md                   # Guia de contribuição
?   ??? Changelog.md                      # Log de mudanças
?   ?
?   ??? ?? atendimento/                   # Processos de atendimento
?   ?   ??? sla_response_times.md
?   ?   ??? classificacao_demandas.md
?   ?   ??? gestao_crises.md
?   ?   ??? privacidade_lgpd.md
?   ?
?   ??? ?? scripts_atendimento/           # Scripts versionados
?   ?   ??? primeiro_contato.md
?   ?   ??? caso_critico.md
?   ?   ??? plano_acao.md
?   ?   ??? gestao_conflito.md
?   ?   ??? fora_escopo.md
?   ?
?   ??? ?? ia_assistiva/                  # Integração IA
?       ??? guidelines_ia.md
?       ??? prompts_atendimento.md
?       ??? human_in_the_loop.md
?
??? ?? clients/                           # Dossiês de clientes
?   ??? README.md                         # Índice de clientes
?   ?
?   ??? ?? arkana_store/                  # Cliente fundador
?       ??? README.md                     # Overview do cliente
?       ??? dossie.md                     # Dossiê completo
?       ??? dossie_atendimento_completo.md
?       ??? historico_atendimento.md      # Cronologia de interações
?       ??? plano_acao_shopify.md         # Plano 30-60-90 dias
?       ?
?       ??? ?? propostas/                 # Propostas enviadas
?       ?   ??? proposta_email.md
?       ?   ??? proposta_whatsapp.txt
?       ?   ??? proposta_instagram.txt
?       ?   ??? solucao_real_48h.md
?       ?
?       ??? ?? documentos/                # Docs do cliente
?       ?   ??? caso_critico.md
?       ?   ??? primeiro_contato.md
?       ?   ??? dossie.md
?       ?
?       ??? ?? metricas/                  # Métricas do cliente
?           ??? csat_scores.json
?           ??? nps_tracking.json
?           ??? roi_projection.md
?
??? ?? scripts/                           # Scripts executáveis
?   ??? README.md                         # Índice de scripts
?   ?
?   ??? ?? atendimento/                   # Automação de atendimento
?   ?   ??? analisar_conversa_whatsapp.py
?   ?   ??? analisar_email.py
?   ?   ??? enviar_proposta_arkana.py
?   ?
?   ??? ?? ia_assistiva/                  # Scripts IA
?   ?   ??? classificar_urgencia.py
?   ?   ??? sugerir_resposta.py
?   ?   ??? extrair_dados.py
?   ?   ??? detectar_risco_churn.py
?   ?
?   ??? ?? metricas/                      # Dashboards e KPIs
?   ?   ??? gerar_dashboard_sla.py
?   ?   ??? calcular_csat.py
?   ?   ??? relatorio_mensal.py
?   ?
?   ??? ?? reorganization/                # Scripts de reorganização
?   ?   ??? reorganize-project.ps1
?   ?   ??? reorganize-project.sh
?   ?   ??? check-project-structure.ps1
?   ?   ??? validate-structure.ps1
?   ?
?   ??? ?? utilities/                     # Utilitários gerais
?       ??? env_loader.py
?       ??? backup_dossies.py
?       ??? sync_to_on_core.py
?
??? ?? archives/                          # Arquivos históricos
?   ??? README.md                         # Índice de arquivos
?   ?
?   ??? ?? 2025-11/                       # Por mês/ano
?   ?   ??? ?? backups/
?   ?   ?   ??? avila_python_files_20251113_065435.zip
?   ?   ?   ??? avila_python_files_20251113_070139.zip
?   ?   ?   ??? arkana_logs_pack.zip
?   ?   ?   ??? avila_inc_padrao_atendimento.zip
?   ?   ?
?   ?   ??? ?? reports/
?   ?   ?   ??? whatsapp_business.md
?   ?   ?
?   ?   ??? ?? temp/
?   ?       ??? deleted_files_log.txt
?   ?
?   ??? ?? 2025-10/
?       ??? (arquivos antigos)
?
??? ?? .backups/                          # Backups automáticos (Git-ignored)
?   ??? daily/
?   ??? weekly/
?   ??? monthly/
?
??? ?? .github/                           # CI/CD e automação
?   ??? workflows/
?   ?   ??? backup-automation.yml
?   ?   ??? validate-structure.yml
?   ?   ??? metrics-report.yml
?   ?
?   ??? ISSUE_TEMPLATE/
?   ?   ??? bug_report.md
?   ?   ??? feature_request.md
?   ?
?   ??? PULL_REQUEST_TEMPLATE.md
?
??? ?? logs/                              # Logs de operação (Git-ignored)
?   ??? atendimento/
?   ??? scripts/
?   ??? sistema/
?
??? ?? .env                               # Variáveis ambiente (Git-ignored)
```

---

## ?? DESCRIÇÃO DOS DIRETÓRIOS

### **Root (Raiz)**
Apenas arquivos principais de navegação e configuração:
- `README.md` ? Porta de entrada do projeto
- Documentos de estrutura, análise, checklist
- `.gitignore` ? Proteção de dados sensíveis

### **`docs/` - Documentação**
Todo conhecimento, processos e guias:
- ? Padrão de Atendimento de Excelência
- ? SLA, scripts, playbooks
- ? Integração IA assistiva
- ? Compliance LGPD/GDPR

**Princípio**: Se é conhecimento, vai aqui.

### **`clients/` - Dossiês de Clientes**
Um diretório por cliente com:
- ? Dossiê completo
- ? Histórico de atendimento
- ? Planos de ação
- ? Propostas enviadas
- ? Métricas (CSAT, NPS, ROI)

**Princípio**: Tudo sobre o cliente em um só lugar.

**?? ATENÇÃO LGPD**: Este diretório contém PII (Personally Identifiable Information).
- ? Protegido por `.gitignore` (se necessário)
- ? Acesso restrito apenas equipe autorizada
- ? Pseudonimização em relatórios públicos

### **`scripts/` - Scripts Executáveis**
Scripts Python organizados por função:
- ? Atendimento (análise, envio)
- ? IA assistiva (classificação, sugestões)
- ? Métricas (dashboards, relatórios)
- ? Utilities (backup, sync)

**Princípio**: Se executa, vai aqui.

### **`archives/` - Arquivos Históricos**
Backups manuais e arquivos antigos:
- ? Organizado por data (YYYY-MM)
- ? Subpastas: `backups/`, `reports/`, `temp/`
- ? README com índice

**Princípio**: Nada é deletado, apenas arquivado.

### **`.backups/` - Backups Automáticos**
Backups gerados automaticamente:
- ? Git-ignored (não versionado)
- ? Daily, weekly, monthly
- ? Gerenciado por scripts

**Princípio**: Backups automáticos, não manuais.

### **`.github/` - CI/CD e Workflows**
Automação GitHub Actions:
- ? Backup automático de dossiês
- ? Validação de estrutura em PR
- ? Geração de métricas mensais
- ? Templates de issues/PRs

**Princípio**: Automatize tudo que for repetitivo.

---

## ?? CONVENÇÕES DE NOMENCLATURA

### **Arquivos Markdown**
```
? Padrao_Atendimento_Excelencia.md   # Title Case com underscores
? README.md                           # ALL CAPS para arquivos especiais
? dossie.md                           # lowercase para arquivos comuns
? (5) Whatsapp Business.md           # Evitar parênteses e espaços
```

### **Scripts Python**
```
? analisar_conversa_whatsapp.py      # snake_case
? enviar_proposta_arkana.py
? AnalisarConversa.py                # Evitar PascalCase
? Analisar-Conversa.py               # Evitar hífens
```

### **Diretórios**
```
? clients/                            # lowercase, plural
? scripts/
? archives/
? Clients/                            # Evitar capitalização
? script/                             # Evitar singular
```

### **Arquivos de Backup**
```
? backups/avila_python_files_YYYYMMDD_HHMMSS.zip
? backups/arkana_logs_YYYYMMDD.zip
? Avila_Python_Files_20251113_065435.zip (no root)
```

---

## ?? SEGURANÇA E PRIVACIDADE

### **Arquivos Git-Ignored**

```gitignore
# Backups automáticos
.backups/

# Logs
logs/
*.log

# Dados sensíveis
.env
.env.local
*.pem
*.key
credentials/

# IDE
.vs/
.vscode/
*.suo
*.user

# Temporários
temp/
tmp/
*.tmp
~$*

# Compilados
__pycache__/
*.pyc
*.pyo

# Dossiês de clientes (opcional - se muito sensível)
# clients/*/dossie.md
```

### **Proteção de PII**

**Dados Protegidos**:
- ? CPF, email pessoal, telefone
- ? Dados financeiros (faturamento)
- ? Senhas, credenciais
- ? Conversas completas (WhatsApp, email)

**Boas Práticas**:
1. Pseudonimização em relatórios públicos
2. Acesso granular (role-based)
3. Audit trail de todas as ações
4. Retenção mínima (após projeto: anonimizar ou excluir)

---

## ?? MÉTRICAS DE ESTRUTURA

### **Objetivos da Estrutura**

| Métrica | Meta | Como Medir |
|---------|------|------------|
| **Tempo para encontrar arquivo** | < 30s | Navegação docs/ ou clients/ |
| **Tempo onboarding novo membro** | < 4h | Ler README + Quick Start |
| **Taxa de arquivos duplicados** | 0% | Git + backups automáticos |
| **Conformidade LGPD** | 100% | Auditoria mensal |
| **Cobertura de documentação** | > 90% | % arquivos com README |

### **KPIs de Qualidade**

- ? **Cada diretório tem README**: Sim/Não
- ? **Cada cliente tem dossiê completo**: Sim/Não
- ? **Scripts têm docstrings**: > 80%
- ? **Estrutura validada em CI/CD**: A cada PR

---

## ?? PRÓXIMOS PASSOS

1. ? Criar estrutura de diretórios (script automatizado)
2. ? Mover arquivos para locais corretos
3. ? Arquivar backups em `archives/2025-11/`
4. ? Deletar arquivos temporários
5. ? Inicializar Git
6. ? Criar READMEs em cada diretório
7. ? Configurar CI/CD (GitHub Actions)
8. ? Treinar equipe na nova estrutura

---

## ?? DÚVIDAS FREQUENTES

### **P: Por que não usar uma pasta "src"?**
R: Este não é um projeto de desenvolvimento de software tradicional. É um projeto de consultoria/atendimento. A estrutura reflete isso: `docs/`, `clients/`, `scripts/`.

### **P: Por que `clients/` em vez de `clientes/`?**
R: Padronização Ávila usa inglês para nomes técnicos (diretórios, variáveis) e português para documentação (arquivos `.md`).

### **P: E se eu tiver 100 clientes?**
R: Estrutura suporta! Use subpastas por letra: `clients/a-e/`, `clients/f-j/`, etc. Ou por status: `clients/active/`, `clients/archived/`.

### **P: Posso ter múltiplos projetos de um cliente?**
R: Sim! Estrutura:
```
clients/arkana_store/
??? projeto_ecommerce/
?   ??? dossie.md
?   ??? plano_acao.md
??? projeto_marketing/
    ??? dossie.md
    ??? plano_acao.md
```

### **P: Como manter arquivos grandes fora do Git?**
R: Use Git LFS (Large File Storage) ou serviço externo (Azure Blob Storage, AWS S3). Guardar apenas link no repo.

---

**Status**: ? **ESTRUTURA DEFINIDA - PRONTO PARA IMPLEMENTAÇÃO!**

---

*Ávila Inc - Estrutura, Clareza, Execução*  
*Data: 16/11/2025 | Versão: 1.0.0*
