// ========================================================================
// ARKANA STORE - Azure Infrastructure (Bicep)
// ========================================================================
// Deploy: az deployment group create --resource-group arkana-store-rg 
//                                     --template-file infra/main.bicep
// ========================================================================

@description('Nome da aplicação')
param appName string = 'arkana-store'

@description('Região do Azure')
param location string = resourceGroup().location

@description('Ambiente (dev, staging, prod)')
@allowed([
  'dev'
  'staging'
  'prod'
])
param environment string = 'prod'

@description('SKU do App Service Plan')
@allowed([
  'F1'  // Free
  'B1'  // Basic
  'S1'  // Standard
  'P1v2' // Premium
])
param appServicePlanSku string = 'B1'

// ========================================================================
// VARIABLES
// ========================================================================

var appServicePlanName = '${appName}-plan-${environment}'
var webAppName = '${appName}-${environment}'
var storageAccountName = 'arkana${uniqueString(resourceGroup().id)}'
var applicationInsightsName = '${appName}-insights-${environment}'
var logAnalyticsName = '${appName}-logs-${environment}'

// ========================================================================
// APP SERVICE PLAN (Python + Node.js)
// ========================================================================

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: appServicePlanSku
    tier: appServicePlanSku == 'F1' ? 'Free' : (appServicePlanSku == 'B1' ? 'Basic' : 'Standard')
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true  // Linux
  }
}

// ========================================================================
// WEB APP (Frontend + Backend)
// ========================================================================

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: appServicePlanSku != 'F1'
      
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'FLASK_APP'
          value: 'automation.admin.api_server'
        }
        {
          name: 'FLASK_ENV'
          value: environment
        }
        {
          name: 'PYTHON_VERSION'
          value: '3.11'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: applicationInsights.properties.ConnectionString
        }
      ]
      
      defaultDocuments: [
        'index.html'
        'arkana-admin-panel.html'
        'arkana-store-v2.html'
      ]
      
      cors: {
        allowedOrigins: [
          '*'
        ]
        supportCredentials: false
      }
    }
  }
}

// ========================================================================
// STORAGE ACCOUNT (SQLite backups, uploads)
// ========================================================================

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: true
    minimumTlsVersion: 'TLS1_2'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

resource backupsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'backups'
  properties: {
    publicAccess: 'None'
  }
}

resource uploadsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'uploads'
  properties: {
    publicAccess: 'Blob'
  }
}

// ========================================================================
// LOG ANALYTICS WORKSPACE
// ========================================================================

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ========================================================================
// APPLICATION INSIGHTS (Monitoramento)
// ========================================================================

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: applicationInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// ========================================================================
// OUTPUTS
// ========================================================================

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output webAppName string = webApp.name
output storageAccountName string = storageAccount.name
output applicationInsightsKey string = applicationInsights.properties.InstrumentationKey
output applicationInsightsConnectionString string = applicationInsights.properties.ConnectionString
