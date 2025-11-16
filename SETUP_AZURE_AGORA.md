# ?? CONFIGURAÇÃO AZURE - GUIA COMPLETO ARKANA

> **Configure o deployment automático no Azure em 10 minutos**  
> **Status**: ? Workflow criado e commitado!  
> **Data**: 16/01/2025

---

## ?? O QUE FOI FEITO AGORA

? **Admin Panel atualizado** com identidade visual real  
? **Workflow GitHub Actions** criado (`.github/workflows/azure-deploy.yml`)  
? **Infraestrutura Bicep** criada (`infra/main.bicep`)  
? **Script PowerShell** deploy automático (`scripts/deploy-azure.ps1`)  
? **Documentação completa** (`DEPLOY_AZURE.md`)  
? **Commit & Push** realizados com sucesso!  

**Commit hash**: `df6db16`  
**Files changed**: 7 arquivos (1888+ linhas adicionadas)

---

## ?? PRÓXIMOS PASSOS (Configure Azure AGORA!)

### **OPÇÃO A: Deploy Automático via GitHub Actions** ? **Recomendado**

#### **PASSO 1: Criar Resource Group + Web App no Azure**

```powershell
# 1.1 - Login Azure
az login

# 1.2 - Criar Resource Group
az group create `
    --name arkana-store-rg `
    --location brazilsouth

# 1.3 - Deploy infraestrutura (Bicep)
az deployment group create `
    --resource-group arkana-store-rg `
    --template-file infra/main.bicep `
    --parameters infra/main.parameters.json

# 1.4 - Obter Publish Profile
az webapp deployment list-publishing-profiles `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --xml > publish-profile.xml
```

**? Recursos criados**:
- `arkana-store-plan-prod` (App Service Plan)
- `arkana-store-prod` (Web App Python 3.11)
- `arkanaXXXXXXXX` (Storage Account)
- `arkana-store-insights-prod` (Application Insights)

---

#### **PASSO 2: Configurar Secret no GitHub**

1. **Abra o arquivo** `publish-profile.xml` criado acima

2. **Copie TODO o conteúdo XML** (Ctrl+A ? Ctrl+C)

3. **Vá para GitHub**:
   - https://github.com/avilaops/ArkanaStore/settings/secrets/actions

4. **Clique**: "New repository secret"

5. **Preencha**:
   ```
   Name: AZURE_WEBAPP_PUBLISH_PROFILE
   
   Secret: <cole o XML aqui>
   ```

6. **Clique**: "Add secret"

---

#### **PASSO 3: Ativar Workflow (Deploy Automático)**

**Já está pronto!** ??

**Trigger automático** em:
- ? Push na branch `main`
- ? Alterações em `*.html`, `automation/**`

**Deploy manual**:
1. GitHub ? **Actions**
2. **Deploy Arkana Store to Azure**
3. **Run workflow** ? **Run workflow**

**Acompanhar deployment**:
- https://github.com/avilaops/ArkanaStore/actions

---

### **OPÇÃO B: Deploy Manual via Script PowerShell**

```powershell
# Executa tudo automaticamente!
.\scripts\deploy-azure.ps1 -Environment prod
```

**O script faz**:
- ? Verifica Azure CLI
- ? Login Azure (se necessário)
- ? Cria Resource Group
- ? Provisiona infraestrutura (Bicep)
- ? Cria pacote de deploy
- ? Upload para Azure
- ? Configura app settings
- ? Mostra URLs finais

**Tempo estimado**: ~5 minutos

---

## ?? CONFIGURAR SECRETS NO AZURE (Pós-Deploy)

Após deploy, configure as variáveis sensíveis:

### **Via Portal Azure**:

1. Portal Azure ? **arkana-store-prod**
2. **Configuration** ? **Application settings**
3. **+ New application setting**

**Adicione**:

```
Nome                    | Valor
?????????????????????????????????????????????????????
SMTP_HOST               | smtp.porkbun.com
SMTP_PORT               | 587
SMTP_USER               | dev@avila.inc
SMTP_PASSWORD           | <sua_senha_smtp>
SMTP_FROM_EMAIL         | dev@avila.inc
SMTP_FROM_NAME          | Arkana Store

STRIPE_SECRET_KEY       | sk_test_... (opcional)
STRIPE_PUBLISHABLE_KEY  | pk_test_... (opcional)

MERCADOPAGO_ACCESS_TOKEN| APP_USR-... (opcional)
PAYPAL_CLIENT_ID        | ... (opcional)
```

4. **Salvar** ? Web App reinicia automaticamente

---

### **Via Azure CLI**:

```powershell
az webapp config appsettings set `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --settings `
        SMTP_HOST=smtp.porkbun.com `
        SMTP_PORT=587 `
        SMTP_USER=dev@avila.inc `
        SMTP_PASSWORD="<senha>" `
        SMTP_FROM_EMAIL=dev@avila.inc
```

---

## ?? TESTAR DEPLOYMENT

### **1. Verificar se está online**:

```powershell
# Health check
curl https://arkana-store-prod.azurewebsites.net/health

# Resposta esperada:
# {"status":"healthy","timestamp":"2025-01-16T..."}
```

---

### **2. Abrir sites**:

```powershell
# Admin Panel
Start-Process "https://arkana-store-prod.azurewebsites.net"

# Site V2 (com cadastro)
Start-Process "https://arkana-store-prod.azurewebsites.net/arkana-store-v2.html"

# Landing Page
Start-Process "https://arkana-store-prod.azurewebsites.net/arkana-store-landing.html"
```

---

### **3. Testar API REST**:

```powershell
# Listar produtos
curl https://arkana-store-prod.azurewebsites.net/api/products

# Criar cliente (teste)
curl -X POST https://arkana-store-prod.azurewebsites.net/api/customers `
     -H "Content-Type: application/json" `
     -d '{
       "name": "Teste Azure",
       "email": "teste@azure.com",
       "phone": "(17) 99999-9999",
       "cpf": "123.456.789-00"
     }'
```

---

## ?? MONITORAR DEPLOYMENT

### **Logs em Tempo Real**:

```powershell
# Stream logs
az webapp log tail `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

### **Ver Métricas (Application Insights)**:

1. Portal Azure ? **arkana-store-insights-prod**
2. **Metrics**
3. Selecione:
   - Server requests
   - Response time
   - Failed requests
   - Server exceptions

---

### **Query Logs (KQL)**:

```kusto
// Últimos 50 requests
requests
| order by timestamp desc
| take 50

// Erros nas últimas 24h
exceptions
| where timestamp > ago(24h)
| order by timestamp desc
```

---

## ?? ATUALIZAR SITE (Após Push)

### **Automático** (GitHub Actions configurado):

```powershell
# 1. Fazer alterações nos arquivos
# 2. Commit
git add arkana-store-v2.html
git commit -m "feat: nova feature"
git push origin main

# 3. GitHub Actions faz deploy automático!
# 4. Acompanhe em: https://github.com/avilaops/ArkanaStore/actions
```

**Tempo deploy**: ~3-5 minutos

---

### **Manual** (via script):

```powershell
.\scripts\deploy-azure.ps1 -Environment prod
```

---

## ?? CONFIGURAÇÃO COMPLETA (Checklist)

### **Azure Resources** ?

- [ ] Resource Group criado (`arkana-store-rg`)
- [ ] App Service Plan criado (`arkana-store-plan-prod`)
- [ ] Web App criado (`arkana-store-prod`)
- [ ] Storage Account criado
- [ ] Application Insights configurado

---

### **GitHub Actions** ?

- [ ] Workflow file existe (`.github/workflows/azure-deploy.yml`)
- [ ] Secret `AZURE_WEBAPP_PUBLISH_PROFILE` configurado
- [ ] Workflow testado (manual trigger)
- [ ] Deploy automático funcionando

---

### **Secrets & Configs** ??

- [ ] SMTP configurado no Azure App Settings
- [ ] Stripe keys (se usar pagamentos online)
- [ ] Mercado Pago token (opcional)
- [ ] PayPal credentials (opcional)

---

### **DNS & Domain** ?? (Opcional)

- [ ] Custom domain adicionado
- [ ] SSL certificate configurado
- [ ] HTTPS redirect habilitado

---

## ?? URLS FINAIS

Após deployment completo:

### **Produção**:
```
??? Admin Panel:
https://arkana-store-prod.azurewebsites.net

??? Site V2 (Checkout):
https://arkana-store-prod.azurewebsites.net/arkana-store-v2.html

?? Landing Page:
https://arkana-store-prod.azurewebsites.net/arkana-store-landing.html

?? API REST:
https://arkana-store-prod.azurewebsites.net/api/
?? /customers
?? /products
?? /orders
?? /email-campaigns
?? /analytics

?? Health Check:
https://arkana-store-prod.azurewebsites.net/health
```

---

### **Staging** (Opcional):

```powershell
# Criar ambiente staging
.\scripts\deploy-azure.ps1 -Environment staging

# URL:
https://arkana-store-staging.azurewebsites.net
```

---

## ?? WORKFLOW GITHUB ACTIONS

### **Arquivo**: `.github/workflows/azure-deploy.yml`

**Estrutura**:

```yaml
name: Deploy Arkana Store to Azure

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python 3.11
      - Install dependencies
      - Create deployment package
      - Deploy to Azure
      - Configure app settings
```

**Ver execuções**:
- https://github.com/avilaops/ArkanaStore/actions

---

## ?? CONTEÚDO DO DEPLOYMENT

### **Arquivos enviados ao Azure**:

```
/home/site/wwwroot/
??? index.html (arkana-admin-panel.html)
??? arkana-store-v2.html
??? arkana-store-landing.html
??? automation/
?   ??? admin/
?   ?   ??? api_server.py
?   ?   ??? arkana_database.py
?   ?   ??? arkana_admin_backend.py
?   ?   ??? requirements.txt
?   ??? utilities/
?       ??? gravatar_service.py
??? data/
?   ??? arkana_store.db (criado automaticamente)
??? web.config (Azure routing)
??? startup.sh (Python startup)
```

---

## ?? COMANDOS ÚTEIS AZURE

### **Ver informações do Web App**:

```powershell
az webapp show `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --query "{name:name, state:state, url:defaultHostName, python:linuxFxVersion}"
```

---

### **Reiniciar Web App**:

```powershell
az webapp restart `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

### **SSH no container**:

```powershell
az webapp ssh `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

Dentro do container:
```bash
# Ver arquivos
ls -la /home/site/wwwroot/

# Testar Python
python --version
python -c "from automation.admin import api_server; print('OK')"

# Ver logs
cat /home/LogFiles/application.log
```

---

### **Download logs**:

```powershell
az webapp log download `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --log-file logs.zip
```

---

## ?? IDENTIDADE VISUAL NO AZURE

Os sites deployados já incluem:

? **Paleta terrosa** (bege/madeira/concreto)  
? **Logo circular** "A ARKANA"  
? **Tipografia** Montserrat + Inter  
? **Toggle dia/noite** com LocalStorage  
? **Fotos reais** produtos (Unsplash)  
? **Textura madeira** sutil  
? **Vigas teto** (modo escuro)  

**Baseado nas fotos reais da boutique!**

---

## ?? DICAS PRO

### **1. Habilitar Always On** (B1+):

```powershell
az webapp config set `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --always-on true
```

**Benefício**: Web App não "dorme" (sem cold start)

---

### **2. Configurar Custom Domain**:

```powershell
# Adicionar domínio
az webapp config hostname add `
    --webapp-name arkana-store-prod `
    --resource-group arkana-store-rg `
    --hostname www.arkana.store

# SSL gratuito
az webapp config ssl create `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --hostname www.arkana.store
```

---

### **3. Habilitar Backup Automático** (S1+):

```powershell
az webapp config backup create `
    --webapp-name arkana-store-prod `
    --resource-group arkana-store-rg `
    --container-url "<storage-sas-url>" `
    --backup-name daily-backup `
    --frequency 1d `
    --retention 30
```

---

### **4. Scaling Automático** (S1+):

```powershell
# Escalar baseado em CPU
az monitor autoscale create `
    --resource-group arkana-store-rg `
    --resource arkana-store-prod `
    --resource-type Microsoft.Web/serverfarms `
    --min-count 1 `
    --max-count 5 `
    --count 1

# Regra: Escalar se CPU > 70%
az monitor autoscale rule create `
    --resource-group arkana-store-rg `
    --autoscale-name arkana-autoscale `
    --condition "Percentage CPU > 70 avg 5m" `
    --scale out 1
```

---

## ?? TROUBLESHOOTING COMUM

### **Problema 1: GitHub Actions falha no deploy**

**Solução**:
```powershell
# Verificar se secret está configurado
# GitHub ? Settings ? Secrets ? Actions
# Deve ter: AZURE_WEBAPP_PUBLISH_PROFILE

# Re-gerar publish profile
az webapp deployment list-publishing-profiles `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --xml > publish-profile-new.xml

# Atualizar secret no GitHub
```

---

### **Problema 2: Site mostra erro 500**

**Solução**:
```powershell
# Ver logs de aplicação
az webapp log tail -n arkana-store-prod -g arkana-store-rg

# Verificar se Python dependencies instalaram
az webapp ssh -n arkana-store-prod -g arkana-store-rg
# Dentro: pip list
```

---

### **Problema 3: Database não funciona**

**Solução**:
```powershell
# SSH no container
az webapp ssh -n arkana-store-prod -g arkana-store-rg

# Criar database manualmente
cd /home/site/wwwroot
python -c "from automation.admin.arkana_database import init_database; init_database()"

# Verificar
ls -la data/arkana_store.db
```

---

### **Problema 4: SMTP emails não enviam**

**Solução**:
```powershell
# Verificar app settings
az webapp config appsettings list `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --query "[?name=='SMTP_HOST']"

# Se não existir, adicionar
az webapp config appsettings set `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --settings SMTP_HOST=smtp.porkbun.com SMTP_PORT=587
```

---

## ?? MONITORAMENTO & ALERTAS

### **Criar alerta de erro**:

```powershell
# Alerta se > 10 erros em 5 minutos
az monitor metrics alert create `
    --name arkana-high-errors `
    --resource-group arkana-store-rg `
    --scopes arkana-store-prod `
    --condition "count exceptions > 10" `
    --window-size 5m `
    --evaluation-frequency 1m `
    --action email marceloquintinoalves25@gmail.com
```

---

### **Dashboard Application Insights**:

1. Portal Azure ? **arkana-store-insights-prod**
2. **Workbooks** ? **Empty Workbook**
3. Adicionar queries:

```kusto
// Requests por hora
requests
| summarize count() by bin(timestamp, 1h)
| render timechart

// Top produtos visualizados
customEvents
| where name == "product_view"
| summarize count() by tostring(customDimensions.product)
| top 10 by count_
```

---

## ?? PLANO DE DEPLOYMENT

### **Fase 1: Setup Inicial** (AGORA)

- ? Resource Group criado
- ? Infraestrutura provisionada (Bicep)
- ? GitHub Actions configurado
- ? Primeiro deploy realizado
- ? Sites online e funcionando

---

### **Fase 2: Configuração** (Próximos dias)

- [ ] SMTP secrets configurados
- [ ] Teste envio emails
- [ ] Custom domain (se tiver)
- [ ] SSL configurado
- [ ] Backup automático

---

### **Fase 3: Otimização** (Próximas semanas)

- [ ] CDN configurado (Azure Front Door ou Cloudflare)
- [ ] Cache Redis (se necessário)
- [ ] Auto-scaling configurado
- [ ] Monitoring alerts criados
- [ ] Performance tuning

---

## ?? CONTROLE DE CUSTOS

### **Ver custo atual**:

```powershell
# Custo do Resource Group
az consumption usage list `
    --query "[?contains(instanceName, 'arkana')].{Resource:instanceName, Cost:pretaxCost}" `
    -o table
```

---

### **Configurar budget alert**:

```powershell
# Alerta se custo > R$ 100/mês
az consumption budget create `
    --amount 100 `
    --budget-name arkana-budget `
    --category cost `
    --time-grain monthly `
    --resource-group arkana-store-rg
```

---

### **Reduzir custos** (se necessário):

```powershell
# Downgrade para Free Tier (F1)
az appservice plan update `
    --name arkana-store-plan-prod `
    --resource-group arkana-store-rg `
    --sku F1
```

**?? Limitações F1**:
- 60 min/dia CPU
- 1GB storage
- Sem Always On
- Sem custom domain

---

## ?? RESUMO FINAL

### **O que você tem AGORA**:

? **Workflow GitHub Actions** configurado  
? **Infraestrutura Bicep** versionada  
? **Script PowerShell** deploy automático  
? **Documentação completa** (700+ linhas)  
? **Admin Panel** com identidade visual real  
? **CI/CD pipeline** pronto para usar  

---

### **Próximo passo**:

**1. Configure o secret no GitHub** (2 minutos):
   - Vá para: https://github.com/avilaops/ArkanaStore/settings/secrets/actions
   - Adicione: `AZURE_WEBAPP_PUBLISH_PROFILE`

**2. Rode o deploy** (escolha uma opção):

**Opção A** - GitHub Actions (automático):
```powershell
git push origin main
# Acompanhe: https://github.com/avilaops/ArkanaStore/actions
```

**Opção B** - Script PowerShell (manual):
```powershell
.\scripts\deploy-azure.ps1
```

**Opção C** - Azure CLI (passo a passo):
```powershell
# Ver DEPLOY_AZURE.md seção "Deploy Manual"
```

---

### **3. Teste o site** (após deploy):

```powershell
Start-Process "https://arkana-store-prod.azurewebsites.net"
```

---

## ?? DOCUMENTAÇÃO ADICIONAL

- ?? **DEPLOY_AZURE.md** - Guia detalhado 700+ linhas
- ?? **infra/README.md** - Documentação Bicep
- ?? **IDENTIDADE_VISUAL_ARKANA_REAL.md** - Design system
- ?? **SISTEMA_V2_SQLITE_CAMPANHAS.md** - Backend completo

---

## ? ARQUIVOS COMMITADOS

```
Commit: df6db16
Branch: main
Remote: https://github.com/avilaops/ArkanaStore

Files:
? .github/workflows/azure-deploy.yml (110 linhas)
? infra/main.bicep (220 linhas)
? infra/main.parameters.json
? infra/README.md (180 linhas)
? scripts/deploy-azure.ps1 (170 linhas)
? DEPLOY_AZURE.md (700 linhas)
? arkana-admin-panel.html (atualizado com design real)

Total: 1888+ linhas adicionadas
```

---

## ?? SUCESSO!

**Tudo pronto para deploy no Azure!**

**Execute agora**:
```powershell
.\scripts\deploy-azure.ps1
```

**Ou configure GitHub Actions e faça push!**

---

**??? ARKANA STORE - Ready for Cloud Deployment!**

*Ávila Inc - DevOps & Cloud Infrastructure* ????
