# ? CHECKLIST DE REORGANIZAÇÃO - ARKHANASTORE

> **Versão**: 1.0.0  
> **Data**: 16/11/2025  
> **Tempo Estimado**: 1-2 horas  
> **Autor**: Ávila AI Assistant

---

## ?? OBJETIVO

Reorganizar o projeto ArkhanaStore de estrutura caótica para estrutura profissional Ávila Framework.

### **Antes (Caótico)**
```
? 10 zips de backup manual no root
? Arquivos temporários não deletados
? Nomenclatura inconsistente
? Sem controle de versão Git
```

### **Depois (Profissional)**
```
? Estrutura modular (docs/, clients/, scripts/, archives/)
? Backups arquivados por data
? Nomenclatura padronizada
? Git inicializado e configurado
```

---

## ?? CHECKLIST COMPLETO

### **FASE 1: PREPARAÇÃO (15 min)**

#### **1.1 Backup de Segurança**
- [ ] Fazer backup completo do diretório atual
  ```powershell
  $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
  Compress-Archive -Path "C:\Users\nicol\OneDrive\Avila\Avilaops\Products\ArkhanaStore\*" `
                   -DestinationPath "C:\Users\nicol\OneDrive\Avila\Backups\ArkhanaStore_$timestamp.zip"
  ```
- [ ] Verificar tamanho do backup (deve ter ~50MB)
- [ ] Confirmar backup está em local seguro

#### **1.2 Verificar Estado Atual**
- [ ] Executar script de análise:
  ```powershell
  .\scripts\check-project-structure.ps1
  ```
- [ ] Listar todos os arquivos:
  ```powershell
  Get-ChildItem -Recurse -File | Select-Object Name, Length | Out-File "arquivo_estrutura_atual.txt"
  ```
- [ ] Revisar lista e identificar arquivos críticos

#### **1.3 Confirmar Permissões**
- [ ] Verificar permissões de escrita no diretório
- [ ] Confirmar que nenhum arquivo está aberto em outros programas
- [ ] Fechar Visual Studio, VS Code, e outros IDEs

---

### **FASE 2: CRIAR ESTRUTURA MODULAR (10 min)**

#### **2.1 Criar Diretórios Principais**
- [ ] Criar `docs/`
  ```powershell
  New-Item -Path "docs" -ItemType Directory -Force
  ```
- [ ] Criar `clients/`
  ```powershell
  New-Item -Path "clients" -ItemType Directory -Force
  ```
- [ ] Criar `scripts/`
  ```powershell
  New-Item -Path "scripts" -ItemType Directory -Force
  ```
- [ ] Criar `archives/`
  ```powershell
  New-Item -Path "archives" -ItemType Directory -Force
  ```
- [ ] Criar `.backups/` (Git-ignored)
  ```powershell
  New-Item -Path ".backups" -ItemType Directory -Force
  ```

#### **2.2 Criar Subdiretórios**

**Em `docs/`:**
- [ ] `docs/atendimento/`
- [ ] `docs/scripts_atendimento/`
- [ ] `docs/ia_assistiva/`

**Em `clients/`:**
- [ ] `clients/arkana_store/`
- [ ] `clients/arkana_store/propostas/`
- [ ] `clients/arkana_store/documentos/`
- [ ] `clients/arkana_store/metricas/`

**Em `scripts/`:**
- [ ] `scripts/atendimento/`
- [ ] `scripts/ia_assistiva/`
- [ ] `scripts/metricas/`
- [ ] `scripts/reorganization/`
- [ ] `scripts/utilities/`

**Em `archives/`:**
- [ ] `archives/2025-11/`
- [ ] `archives/2025-11/backups/`
- [ ] `archives/2025-11/reports/`
- [ ] `archives/2025-11/temp/`

---

### **FASE 3: MOVER DOCUMENTAÇÃO (20 min)**

#### **3.1 Documentação Principal**
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Padrao_Atendimento_Excelencia.md` ? `docs/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Readme_Avila_Inc_Padrao_Atendimento.md` ? `docs/README_Atendimento.md`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Sumario_Executivo.md` ? `docs/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Quick_Start.md` ? `docs/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Changelog.md` ? `docs/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Contributing.md` ? `docs/`

#### **3.2 Scripts de Atendimento**
- [ ] Mover conteúdo de `Avila_Inc_Padrao_Atendimento/Scripts/` ? `docs/scripts_atendimento/`

#### **3.3 IA Assistiva**
- [ ] Mover conteúdo de `Avila_Inc_Padrao_Atendimento/Ia_Assistiva/` ? `docs/ia_assistiva/`

---

### **FASE 4: CONSOLIDAR CLIENTE ARKANA (15 min)**

#### **4.1 Dossiê Principal**
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Dossie.md` ? `clients/arkana_store/dossie.md`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Dossie_Atendimento_Completo.md` ? `clients/arkana_store/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Historico_Atendimento.md` ? `clients/arkana_store/`

#### **4.2 Planos de Ação**
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Plano_Acao_Shopify_Suspensao.md` ? `clients/arkana_store/`

#### **4.3 Propostas**
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Proposta_Whatsapp.txt` ? `clients/arkana_store/propostas/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Proposta_Instagram.txt` ? `clients/arkana_store/propostas/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Solucao_Real_48h.md` ? `clients/arkana_store/propostas/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Solucao_Avila_Propria.md` ? `clients/arkana_store/propostas/`

#### **4.4 Documentos**
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Caso_Critico.md` ? `clients/arkana_store/documentos/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento/Clientes/Arkana_Store/Primeiro_Contato.md` ? `clients/arkana_store/documentos/`

---

### **FASE 5: ORGANIZAR SCRIPTS (15 min)**

#### **5.1 Scripts de Atendimento**
- [ ] Mover `Analisar_Conversa_Whatsapp.py` ? `scripts/atendimento/analisar_conversa_whatsapp.py`
- [ ] Mover `Analisar_Email.py` ? `scripts/atendimento/analisar_email.py`
- [ ] Mover `Temp _ deletar após visualização/Enviar_Proposta_Arkana.py` ? `scripts/atendimento/enviar_proposta_arkana.py`
- [ ] Mover `Temp _ deletar após visualização/Enviar_Whatsapp_Arkana.py` ? `scripts/atendimento/enviar_whatsapp_arkana.py`

#### **5.2 Utilities**
- [ ] Mover `Env_Loader.py` ? `scripts/utilities/env_loader.py`

---

### **FASE 6: ARQUIVAR BACKUPS (10 min)**

#### **6.1 Backups Python Files**
- [ ] Mover `Avila_Python_Files_20251113_065435.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Python_Files_20251113_070139.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Python_Files_20251113_070430.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Python_Files_20251113_071225.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Python_Files_20251113_071532.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Python_Files_20251113_072111.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Python_Files_20251113_072832.zip` ? `archives/2025-11/backups/`

#### **6.2 Outros Arquivos**
- [ ] Mover `Arkana_Logs_Pack.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Avila_Inc_Padrao_Atendimento.zip` ? `archives/2025-11/backups/`
- [ ] Mover `Arkana_Logs_Pack/` (diretório) ? `archives/2025-11/` (se existir descompactado)

#### **6.3 Reports**
- [ ] Renomear `(5) Whatsapp Business.md` ? `Whatsapp_Business.md`
- [ ] Mover `Whatsapp_Business.md` ? `archives/2025-11/reports/`

---

### **FASE 7: LIMPAR ARQUIVOS TEMPORÁRIOS (5 min)**

#### **7.1 Deletar Pasta Temp**
- [ ] Verificar conteúdo de `Temp _ deletar após visualização/`
- [ ] Confirmar que scripts já foram movidos
- [ ] Deletar `Temp _ deletar após visualização/` completo

#### **7.2 Limpar Cache IDE**
- [ ] Deletar `.vs/` (Visual Studio cache)
- [ ] Deletar `*.suo`, `*.user` (se existir)
- [ ] Deletar `slnx.sqlite` (se existir)

#### **7.3 Verificar Duplicados**
- [ ] Verificar se `Avila_Inc_Padrao_Atendimento/` original está vazio
- [ ] Se vazio, deletar diretório
- [ ] Se não vazio, revisar manualmente

---

### **FASE 8: CRIAR READMEs (20 min)**

#### **8.1 README Principal**
- [ ] Criar `README.md` no root com:
  - Visão geral do projeto
  - Estrutura de diretórios
  - Quick Start
  - Links para docs principais

#### **8.2 READMEs de Diretórios**
- [ ] Criar `docs/README.md` (índice de documentação)
- [ ] Criar `clients/README.md` (índice de clientes)
- [ ] Criar `scripts/README.md` (índice de scripts)
- [ ] Criar `archives/README.md` (índice de arquivos)
- [ ] Criar `clients/arkana_store/README.md` (overview do cliente)

---

### **FASE 9: CONFIGURAR GIT (15 min)**

#### **9.1 Criar .gitignore**
- [ ] Criar `.gitignore` no root com:
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
  ```

#### **9.2 Inicializar Repositório**
- [ ] `git init`
- [ ] `git add .`
- [ ] `git commit -m "feat: versão inicial 1.0.0 - ArkhanaStore reorganizado"`

#### **9.3 Criar Repositório GitHub**
- [ ] Criar repo privado: `avilaops/arkhana-store`
- [ ] `git remote add origin https://github.com/avilaops/arkhana-store.git`
- [ ] `git branch -M main`
- [ ] `git push -u origin main`

---

### **FASE 10: VALIDAÇÃO FINAL (10 min)**

#### **10.1 Verificar Estrutura**
- [ ] Executar script de validação:
  ```powershell
  .\scripts\validate-structure.ps1
  ```
- [ ] Confirmar que todos os arquivos estão nos lugares corretos

#### **10.2 Verificar Integridade**
- [ ] Todos os arquivos `.md` abrem sem erro?
- [ ] Todos os scripts `.py` têm sintaxe válida?
- [ ] Nenhum arquivo perdido?

#### **10.3 Testar Navegação**
- [ ] Abrir `README.md` e seguir todos os links
- [ ] Confirmar que links internos funcionam
- [ ] Confirmar que estrutura faz sentido

#### **10.4 Documentar Mudanças**
- [ ] Criar `CHANGELOG.md` no root
- [ ] Registrar versão 1.0.0 com lista de mudanças
- [ ] Adicionar data e autor

---

### **FASE 11: COMUNICAÇÃO (5 min)**

#### **11.1 Avisar Equipe**
- [ ] Enviar email/mensagem para equipe Ávila
- [ ] Anexar `ANALISE_COMPLETA_ARKHANASTORE.md`
- [ ] Explicar nova estrutura

#### **11.2 Atualizar Documentação On-Core**
- [ ] Registrar nova estrutura no sistema On
- [ ] Atualizar links em dashboards
- [ ] Notificar Archivus (agente bibliotecário)

---

## ?? SCRIPT AUTOMATIZADO (Opcional)

Se preferir automatizar todo o processo:

```powershell
# Salvar como: scripts/reorganize-project.ps1
# Executar: .\scripts\reorganize-project.ps1

# (Conteúdo do script será fornecido separadamente)
```

---

## ?? CHECKLIST DE VALIDAÇÃO

Após completar todas as fases, confirmar:

- [ ] ? Estrutura modular criada (docs/, clients/, scripts/, archives/)
- [ ] ? Documentação movida corretamente
- [ ] ? Cliente Arkana consolidado
- [ ] ? Scripts organizados
- [ ] ? Backups arquivados por data
- [ ] ? Arquivos temporários deletados
- [ ] ? Root limpo (apenas README + diretórios principais)
- [ ] ? READMEs criados em cada nível
- [ ] ? Git inicializado
- [ ] ? .gitignore configurado
- [ ] ? Primeiro commit realizado
- [ ] ? Repo GitHub criado e sincronizado
- [ ] ? Estrutura validada
- [ ] ? Equipe notificada

---

## ?? TEMPO TOTAL ESTIMADO

| Fase | Tempo |
|------|-------|
| Preparação | 15 min |
| Criar estrutura | 10 min |
| Mover documentação | 20 min |
| Consolidar cliente | 15 min |
| Organizar scripts | 15 min |
| Arquivar backups | 10 min |
| Limpar temporários | 5 min |
| Criar READMEs | 20 min |
| Configurar Git | 15 min |
| Validação final | 10 min |
| Comunicação | 5 min |
| **TOTAL** | **2 horas** |

---

## ?? EM CASO DE PROBLEMA

Se algo der errado durante a reorganização:

1. **PARE IMEDIATAMENTE**
2. **NÃO DELETE NADA MAIS**
3. **Restaure o backup**: Descompactar `ArkhanaStore_YYYYMMDD_HHMMSS.zip`
4. **Revise o checklist**: Identificar onde parou
5. **Recomeçar do ponto de parada**

---

## ?? SUPORTE

Em caso de dúvidas:
1. Revisar `ESTRUTURA_PROJETO.md`
2. Consultar `ANALISE_COMPLETA_ARKHANASTORE.md`
3. Abrir issue no GitHub
4. Contatar equipe Ávila Inc

---

**Status**: ? **CHECKLIST COMPLETO - PRONTO PARA EXECUÇÃO!**

**Próximo Passo**: Começar pela FASE 1 (Preparação).

---

*Ávila Inc - Estrutura, Clareza, Execução*  
*Data: 16/11/2025 | Versão: 1.0.0*
