# ?? DEPLOY ARKANA STORE NO AZURE

> **Guia completo para deploy da boutique Arkana na nuvem Azure**  
> **Data**: 16/01/2025  
> **Versão**: 2.0 (Identidade Visual Real)

---

## ?? PRÉ-REQUISITOS

### **Ferramentas Necessárias**:

```powershell
# 1. Azure CLI
winget install Microsoft.AzureCLI

# 2. Git
winget install Git.Git

# 3. Python 3.11+
winget install Python.Python.3.11

# 4. Node.js 18+ (opcional)
winget install OpenJS.NodeJS
```

### **Conta Azure**:
- ? Conta Azure ativa (https://azure.microsoft.com/free/)
- ? Subscription configurada
- ? Permissões para criar recursos

---

## ??? ARQUITETURA AZURE

```
???????????????????????????????????????????????????????????
?                    ARKANA STORE                          ?
???????????????????????????????????????????????????????????
?                                                          ?
?  ????????????????????    ????????????????????          ?
?  ?   App Service    ??????  App Service     ?          ?
?  ?   (Python 3.11)  ?    ?  Plan (Linux)    ?          ?
?  ?                  ?    ?  SKU: B1/S1      ?          ?
?  ?  - Frontend HTML ?    ????????????????????          ?
?  ?  - Backend Flask ?                                   ?
?  ?  - SQLite DB     ?                                   ?
?  ????????????????????                                   ?
?           ?                                              ?
?           ?                                              ?
?  ????????????????????    ????????????????????          ?
?  ? Storage Account  ?    ? Application      ?          ?
?  ?                  ?    ? Insights         ?          ?
?  ?  - Backups DB    ?    ?                  ?          ?
?  ?  - Uploads       ?    ?  - Logs          ?          ?
?  ?  - Static files  ?    ?  - Métricas      ?          ?
?  ????????????????????    ?  - Telemetria    ?          ?
?                          ????????????????????          ?
?                                                          ?
???????????????????????????????????????????????????????????

URLs geradas:
?? https://arkana-store-prod.azurewebsites.net
?? https://arkana-store-prod.azurewebsites.net/arkana-store-v2.html
?? https://arkana-store-prod.azurewebsites.net/arkana-store-landing.html
```

---

## ?? OPÇÃO 1: DEPLOY VIA GITHUB ACTIONS (Automático)

### **PASSO 1: Configurar Secrets no GitHub**

1. Vá para: https://github.com/avilaops/ArkanaStore/settings/secrets/actions

2. Clique em **"New repository secret"**

3. Adicione:

```
Nome: AZURE_WEBAPP_PUBLISH_PROFILE
Valor: <cole o publish profile aqui>
```

**Como obter o Publish Profile**:

```powershell
# Via Azure CLI
az webapp deployment list-publishing-profiles `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --xml
```

Ou via Portal Azure:
1. App Service ? **arkana-store-prod**
2. Overview ? **Get publish profile**
3. Copie todo o conteúdo XML

---

### **PASSO 2: Ativar Workflow**

O workflow `.github/workflows/azure-deploy.yml` já está configurado!

**Trigger automático**:
- ? Push na branch `main`
- ? Alterações em: `*.html`, `automation/**`
- ? Workflow manual (via GitHub Actions tab)

**Para deploy manual**:
1. GitHub ? **Actions**
2. **Deploy Arkana Store to Azure**
3. **Run workflow**

---

## ?? OPÇÃO 2: DEPLOY VIA SCRIPT POWERSHELL (Manual)

### **Passo a passo completo**:

```powershell
# 1. Clone repositório (se ainda não tiver)
git clone https://github.com/avilaops/ArkanaStore.git
cd ArkanaStore

# 2. Login Azure
az login

# 3. Criar Resource Group
az group create `
    --name arkana-store-rg `
    --location brazilsouth

# 4. Deploy infraestrutura (Bicep)
az deployment group create `
    --resource-group arkana-store-rg `
    --template-file infra/main.bicep `
    --parameters environment=prod

# 5. Executar script de deploy
.\scripts\deploy-azure.ps1 -Environment prod

# 6. Verificar deployment
az webapp browse --name arkana-store-prod --resource-group arkana-store-rg
```

---

## ??? OPÇÃO 3: DEPLOY MANUAL PASSO A PASSO

### **STEP 1: Criar Recursos no Azure Portal**

**1.1 - App Service Plan**:
```
Nome: arkana-store-plan-prod
Sistema Operacional: Linux
Região: Brazil South
Pricing: Basic B1 (recomendado) ou Free F1
```

**1.2 - Web App**:
```
Nome: arkana-store-prod
Runtime: Python 3.11
App Service Plan: arkana-store-plan-prod
```

**1.3 - Storage Account**:
```
Nome: arkanaXXXXXXXX (gerado automaticamente)
Replicação: LRS
Região: Brazil South
```

---

### **STEP 2: Deploy Código**

**Via Azure CLI**:

```powershell
# Criar pacote
mkdir deploy
Copy-Item "arkana-*.html" deploy\
Copy-Item automation deploy\ -Recurse

# Fazer upload
az webapp up `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --runtime "PYTHON:3.11" `
    --sku B1 `
    --location brazilsouth
```

**Via VS Code** (Azure Extension):
1. Instalar extensão: **Azure App Service**
2. Botão direito em `arkana-store-prod`
3. **Deploy to Web App...**
4. Selecionar pasta `deploy/`

---

### **STEP 3: Configurar Variáveis de Ambiente**

**Via Portal Azure**:

```
App Service ? arkana-store-prod ? Configuration ? Application settings

Adicionar:
?? FLASK_ENV = production
?? PYTHON_VERSION = 3.11
?? SCM_DO_BUILD_DURING_DEPLOYMENT = true
?? WEBSITES_PORT = 8000
```

**Via Azure CLI**:

```powershell
az webapp config appsettings set `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --settings `
        FLASK_ENV=production `
        PYTHON_VERSION=3.11 `
        SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

---

## ?? RECURSOS CRIADOS

| Recurso | Nome | Tipo | Custo Estimado |
|---------|------|------|----------------|
| **Resource Group** | arkana-store-rg | Container | Grátis |
| **App Service Plan** | arkana-store-plan-prod | B1 Linux | ~R$ 60/mês |
| **Web App** | arkana-store-prod | Python 3.11 | Incluído no Plan |
| **Storage Account** | arkanaXXXXXXXX | Standard LRS | ~R$ 5/mês |
| **Application Insights** | arkana-store-insights | Monitoring | ~R$ 10/mês |
| **Log Analytics** | arkana-store-logs | Logs | Incluído |

**?? Total estimado**: **~R$ 75/mês**

---

## ?? CONFIGURAÇÃO PÓS-DEPLOY

### **1. Configurar Custom Domain** (Opcional):

```powershell
# Adicionar domínio personalizado
az webapp config hostname add `
    --webapp-name arkana-store-prod `
    --resource-group arkana-store-rg `
    --hostname www.arkana.store

# Configurar SSL (Let's Encrypt grátis)
az webapp config ssl bind `
    --certificate-thumbprint <thumbprint> `
    --ssl-type SNI `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

### **2. Configurar Email (SMTP)**:

Adicionar no **Configuration ? Application settings**:

```
SMTP_HOST = smtp.porkbun.com
SMTP_PORT = 587
SMTP_USER = dev@avila.inc
SMTP_PASSWORD = <secret>
SMTP_FROM_EMAIL = dev@avila.inc
SMTP_FROM_NAME = Arkana Store
```

---

### **3. Habilitar HTTPS Redirect**:

```powershell
az webapp update `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --set httpsOnly=true
```

---

## ?? TESTAR DEPLOYMENT

### **1. Health Check**:

```powershell
# Via curl
curl https://arkana-store-prod.azurewebsites.net/health

# Resposta esperada:
# {"status": "healthy", "timestamp": "2025-01-16T..."}
```

---

### **2. Testar Sites**:

```powershell
# Abrir no navegador
Start-Process "https://arkana-store-prod.azurewebsites.net"
Start-Process "https://arkana-store-prod.azurewebsites.net/arkana-store-v2.html"
Start-Process "https://arkana-store-prod.azurewebsites.net/arkana-store-landing.html"
```

---

### **3. Testar API**:

```powershell
# Listar clientes
curl https://arkana-store-prod.azurewebsites.net/api/customers

# Listar produtos
curl https://arkana-store-prod.azurewebsites.net/api/products
```

---

## ?? MONITORAMENTO

### **Application Insights**:

```powershell
# Ver logs em tempo real
az monitor app-insights query `
    --app arkana-store-insights `
    --resource-group arkana-store-rg `
    --analytics-query "traces | order by timestamp desc | take 50"
```

---

### **Stream de Logs**:

```powershell
# Ver logs do servidor em tempo real
az webapp log tail `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

## ?? CI/CD WORKFLOW (GitHub Actions)

### **Arquivo**: `.github/workflows/azure-deploy.yml`

**Trigger**:
- ? Push na `main`
- ? Alterações em HTML/Python
- ? Manual (workflow_dispatch)

**Steps**:
1. ? Checkout código
2. ? Setup Python 3.11
3. ? Install dependencies
4. ? Create deployment package
5. ? Deploy to Azure Web App
6. ? Configure app settings

**Status**: Ver em https://github.com/avilaops/ArkanaStore/actions

---

## ?? SEGURANÇA

### **Secrets no GitHub**:

| Secret | Descrição |
|--------|-----------|
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Perfil de publicação do Azure |
| `SMTP_PASSWORD` | Senha SMTP (opcional) |
| `STRIPE_SECRET_KEY` | Chave Stripe (futuro) |

**Como adicionar**:
```
GitHub ? Settings ? Secrets and variables ? Actions ? New secret
```

---

### **Variáveis de Ambiente Azure**:

**NÃO commitar no Git**:
```
config/.env.arkana.production  ? Ignorado pelo .gitignore
```

**Configurar no Azure Portal**:
```
App Service ? Configuration ? Application settings ? New setting
```

---

## ?? TROUBLESHOOTING

### **Problema 1: Deploy falha**

```powershell
# Ver logs de deploy
az webapp log tail `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

### **Problema 2: Site não carrega**

```powershell
# Reiniciar Web App
az webapp restart `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

### **Problema 3: Erros Python**

```powershell
# SSH no container
az webapp ssh `
    --name arkana-store-prod `
    --resource-group arkana-store-rg

# Verificar logs
cat /home/LogFiles/application.log
```

---

### **Problema 4: Database não funciona**

```powershell
# Verificar se SQLite está criado
az webapp ssh `
    --name arkana-store-prod `
    --resource-group arkana-store-rg

# Dentro do container:
ls -la /home/site/wwwroot/data/
python automation/admin/arkana_database.py
```

---

## ?? ATUALIZAR DEPLOYMENT

### **Via GitHub (Automático)**:

```powershell
# Fazer alterações
git add .
git commit -m "feat: atualizacao site"
git push origin main

# GitHub Actions faz deploy automático!
```

---

### **Via Script (Manual)**:

```powershell
.\scripts\deploy-azure.ps1 -Environment prod
```

---

## ?? CUSTOS ESTIMADOS

### **Configuração Básica (B1)**:

```
App Service Plan B1:        R$ 60/mês
Storage Account (10GB):     R$ 5/mês
Application Insights:       R$ 10/mês
Bandwidth (5GB):            R$ 5/mês
??????????????????????????????????
TOTAL:                      ~R$ 80/mês
```

### **Configuração Free (F1)**:

```
App Service Plan F1:        GRÁTIS
Storage Account (1GB):      R$ 1/mês
Application Insights:       GRÁTIS (1GB/mês)
??????????????????????????????????
TOTAL:                      ~R$ 1/mês
```

**?? Limitações Free Tier**:
- ? Sem "Always On"
- ? 60 min/dia CPU
- ? 1GB storage
- ? Sem custom domain
- ? Suficiente para testes!

---

## ?? COMANDOS ÚTEIS

### **Ver status**:

```powershell
# Status geral
az webapp show `
    --name arkana-store-prod `
    --resource-group arkana-store-rg `
    --query "{name:name, state:state, url:defaultHostName}"

# Logs em tempo real
az webapp log tail `
    --name arkana-store-prod `
    --resource-group arkana-store-rg

# Métricas
az monitor metrics list `
    --resource arkana-store-prod `
    --resource-group arkana-store-rg `
    --resource-type Microsoft.Web/sites `
    --metric "Http5xx"
```

---

### **Gerenciar App**:

```powershell
# Reiniciar
az webapp restart -n arkana-store-prod -g arkana-store-rg

# Parar
az webapp stop -n arkana-store-prod -g arkana-store-rg

# Iniciar
az webapp start -n arkana-store-prod -g arkana-store-rg

# Deletar
az webapp delete -n arkana-store-prod -g arkana-store-rg
```

---

### **Backup Database**:

```powershell
# SSH no container
az webapp ssh -n arkana-store-prod -g arkana-store-rg

# Dentro do container:
cd /home/site/wwwroot
python -c "from automation.admin.arkana_database import backup_database; backup_database()"

# Download backup
az webapp download -n arkana-store-prod -g arkana-store-rg
```

---

## ?? ESTRUTURA DE DEPLOY

```
deploy/
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
??? config/
?   ??? .env.arkana.template
??? data/
?   ??? arkana_store.db (criado automaticamente)
??? web.config (Azure Web App config)
??? startup.sh (Python startup script)
```

---

## ?? URLs FINAIS

### **Produção**:

```
Admin Panel:
https://arkana-store-prod.azurewebsites.net

Site V2 (com cadastro):
https://arkana-store-prod.azurewebsites.net/arkana-store-v2.html

Landing Page (showcase):
https://arkana-store-prod.azurewebsites.net/arkana-store-landing.html

API REST:
https://arkana-store-prod.azurewebsites.net/api/customers
https://arkana-store-prod.azurewebsites.net/api/products
https://arkana-store-prod.azurewebsites.net/api/orders

Health Check:
https://arkana-store-prod.azurewebsites.net/health
```

---

### **Staging** (Opcional):

```
https://arkana-store-staging.azurewebsites.net
```

Para criar:
```powershell
.\scripts\deploy-azure.ps1 -Environment staging
```

---

## ? CHECKLIST PRÉ-DEPLOY

Antes de fazer deploy, verifique:

- [ ] Azure CLI instalado (`az --version`)
- [ ] Logado no Azure (`az account show`)
- [ ] Resource Group criado
- [ ] Secrets configurados no GitHub (se usar Actions)
- [ ] Arquivos `.env` NÃO estão no commit (verificar `.gitignore`)
- [ ] `requirements.txt` atualizado
- [ ] Sites HTML testados localmente
- [ ] Backend Python testado localmente

---

## ?? DEPLOY CONCLUÍDO!

Após deploy bem-sucedido, você terá:

? **3 sites HTML** no Azure  
? **API REST** funcionando (15 endpoints)  
? **SQLite database** configurado  
? **Application Insights** monitorando  
? **Storage Account** para backups  
? **HTTPS** habilitado automaticamente  
? **Logs centralizados**  

---

## ?? SUPORTE

**Problemas?**

1. Ver logs: `az webapp log tail -n arkana-store-prod -g arkana-store-rg`
2. Verificar Application Insights no Portal Azure
3. GitHub Issues: https://github.com/avilaops/ArkanaStore/issues

---

## ?? PRÓXIMOS PASSOS

Após deploy:

1. ? Testar todos os sites
2. ? Configurar custom domain (opcional)
3. ? Configurar SMTP secrets
4. ? Testar campanhas email
5. ? Configurar backups automáticos
6. ? Monitorar Application Insights

---

**??? ARKANA STORE - Agora na Nuvem Azure!**

*Powered by Ávila Inc* ??
