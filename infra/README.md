# ??? ARKANA STORE - Infraestrutura Azure

> **Infrastructure as Code (IaC) usando Bicep**  
> **Provisiona todos os recursos Azure necessários**

---

## ?? ARQUIVOS

```
infra/
??? main.bicep                 # Template principal
??? main.parameters.json       # Parâmetros de deploy
??? README.md                  # Este arquivo
```

---

## ?? DEPLOY RÁPIDO

### **Opção 1: Via Script PowerShell**

```powershell
.\scripts\deploy-azure.ps1
```

---

### **Opção 2: Azure CLI Direto**

```powershell
# 1. Login
az login

# 2. Criar Resource Group
az group create `
    --name arkana-store-rg `
    --location brazilsouth

# 3. Deploy infraestrutura
az deployment group create `
    --resource-group arkana-store-rg `
    --template-file infra/main.bicep `
    --parameters infra/main.parameters.json
```

---

## ?? RECURSOS CRIADOS

### **1. App Service Plan** (Linux)
```
Nome: arkana-store-plan-prod
SKU: B1 (Basic)
OS: Linux
Runtime: Python 3.11
```

---

### **2. Web App**
```
Nome: arkana-store-prod
Stack: Python 3.11
Features:
- HTTPS only
- Always On (B1+)
- Application Insights
- Deployment slots (S1+)
```

---

### **3. Storage Account**
```
Nome: arkana{uniqueString}
Replicação: LRS
Tier: Standard
Containers:
- backups/  (SQLite backups)
- uploads/  (product images)
```

---

### **4. Application Insights**
```
Nome: arkana-store-insights-prod
Features:
- Request tracking
- Error monitoring
- Performance metrics
- Custom events
```

---

### **5. Log Analytics Workspace**
```
Nome: arkana-store-logs-prod
Retention: 30 days
Features:
- Centralized logging
- Query interface (KQL)
- Alerts
```

---

## ?? PARÂMETROS CUSTOMIZÁVEIS

### **main.parameters.json**:

```json
{
  "appName": "arkana-store",           // Nome base
  "location": "brazilsouth",           // Região Azure
  "environment": "prod",               // dev/staging/prod
  "appServicePlanSku": "B1"           // F1/B1/S1/P1v2
}
```

---

## ?? CUSTOS POR SKU

| SKU | vCPU | RAM | Storage | Custo/mês |
|-----|------|-----|---------|-----------|
| **F1** (Free) | Shared | 1GB | 1GB | **GRÁTIS** |
| **B1** (Basic) | 1 | 1.75GB | 10GB | **~R$ 60** |
| **S1** (Standard) | 1 | 1.75GB | 50GB | **~R$ 350** |
| **P1v2** (Premium) | 1 | 3.5GB | 250GB | **~R$ 800** |

**Recomendação**:
- ?? **Testes**: F1 (grátis)
- ?? **Produção**: B1 (básico)
- ?? **Alto tráfego**: S1 (standard)

---

## ?? CUSTOMIZAR DEPLOYMENT

### **Alterar região**:

```bicep
param location string = 'eastus'  // ou brazilsouth, westeurope
```

Regiões disponíveis:
```powershell
az account list-locations --query "[].{Name:name, DisplayName:displayName}" -o table
```

---

### **Alterar SKU**:

```json
{
  "appServicePlanSku": {
    "value": "S1"  // F1, B1, S1, P1v2
  }
}
```

---

### **Adicionar deployment slot** (staging):

```bicep
resource stagingSlot 'Microsoft.Web/sites/slots@2022-09-01' = {
  parent: webApp
  name: 'staging'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
  }
}
```

---

## ?? OUTPUTS DO BICEP

Após deploy, o Bicep retorna:

```json
{
  "webAppUrl": "https://arkana-store-prod.azurewebsites.net",
  "webAppName": "arkana-store-prod",
  "storageAccountName": "arkanaXXXXXXXX",
  "applicationInsightsKey": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "applicationInsightsConnectionString": "InstrumentationKey=..."
}
```

Ver outputs:
```powershell
az deployment group show `
    --resource-group arkana-store-rg `
    --name main `
    --query properties.outputs
```

---

## ??? DELETAR INFRAESTRUTURA

### **CUIDADO**: Isso remove TUDO!

```powershell
# Deletar Resource Group inteiro
az group delete `
    --name arkana-store-rg `
    --yes `
    --no-wait
```

**Alternativa** (deletar só Web App):
```powershell
az webapp delete `
    --name arkana-store-prod `
    --resource-group arkana-store-rg
```

---

## ?? REFERÊNCIAS

- ?? [Azure Bicep Docs](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- ?? [App Service Docs](https://learn.microsoft.com/azure/app-service/)
- ?? [Python on Azure](https://learn.microsoft.com/azure/app-service/quickstart-python)

---

**??? ARKANA - Infrastructure as Code**

*Ávila Inc - Cloud Architecture* ??
