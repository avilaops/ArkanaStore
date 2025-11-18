
param location string = resourceGroup().location
@description('Name of the existing Azure Functions app to attach diagnostics to')
param functionAppName string

@description('Optional: Name of the Static Web App if you want activity logs streamed. If empty, SWA will not be bound here.')
param staticWebAppName string = ''

@description('Email to receive alerts')
param alertEmail string

@description('Log Analytics workspace name')
param lawName string = 'arkana-law'

@description('Application Insights component name')
param appInsightsName string = 'arkana-appinsights'

// Workspace
resource law 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: lawName
  location: location
  properties: {
    retentionInDays: 30
    features: {
      legacy: 0
      searchVersion: 1
    }
  }
}

// App Insights (workspace-based)
resource ai 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Flow_Type: 'Bluefield'
    WorkspaceResourceId: law.id
    IngestionMode: 'ApplicationInsights'
  }
}

@description('Action Group for alerting')
resource actionGroup 'Microsoft.Insights/actionGroups@2022-06-01' = {
  name: 'arkana-alerts'
  location: 'global'
  properties: {
    enabled: true
    emailReceivers: [
      {
        name: 'primary-email'
        emailAddress: alertEmail
        useCommonAlertSchema: true
      }
    ]
  }
}

// Attach diagnostic settings to the Function App for detailed logs to LAW
resource func 'Microsoft.Web/sites@2023-12-01' existing = {
  name: functionAppName
}

resource funcDiag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'send-to-law'
  scope: func
  properties: {
    workspaceId: law.id
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
    logs: [
      { category: 'AppServiceHTTPLogs', enabled: true }
      { category: 'AppServiceConsoleLogs', enabled: true }
      { category: 'AppServiceAppLogs', enabled: true }
      { category: 'AppServiceAuditLogs', enabled: true }
      { category: 'AppServiceIPSecAuditLogs', enabled: true }
      { category: 'AppServicePlatformLogs', enabled: true }
    ]
  }
}

// Optional: Activity logs for Static Web App (limited signal). Bound if provided.
resource swa 'Microsoft.Web/staticSites@2022-03-01' existing = if (staticWebAppName != '') {
  name: staticWebAppName
}

resource swaDiag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (staticWebAppName != '') {
  name: 'send-to-law'
  scope: swa
  properties: {
    workspaceId: law.id
    logs: [
      // Categories may vary by region/sku. Keep generic.
      { category: 'FunctionAppLogs', enabled: true }
      { category: 'AppRequests', enabled: true }
      { category: 'AppTraces', enabled: true }
    ]
  }
}

// ===== Alerts (Log Alerts v2) =====

@description('P0: Many 5xx on Functions in 1 minute')
resource alert_many5xx 'Microsoft.Insights/scheduledQueryRules@2022-06-15' = {
  name: 'arkana-p0-many-5xx'
  location: location
  properties: {
    description: 'Triggers when server errors exceed threshold'
    enabled: true
    evaluationFrequency: 'PT1M'
    severity: 0
    scopes: [ law.id ]
    windowSize: 'PT5M'
    criteria: {
      allOf: [
        {
          name: 'many-5xx'
          query: '''
requests
| where toint(resultCode) between (500 .. 599)
| summarize count() by bin(timestamp, 1m)
| where count_ >= 3
'''
          timeAggregation: 'Count'
          operator: 'GreaterThanOrEqual'
          threshold: 1
        }
      ]
    }
    actions: {
      actionGroups: [
        { actionGroupId: actionGroup.id }
      ]
    }
  }
}

@description('P1: Webhook not received in the last 15 minutes')
resource alert_no_webhook 'Microsoft.Insights/scheduledQueryRules@2022-06-15' = {
  name: 'arkana-p1-no-webhook-15m'
  location: location
  properties: {
    description: 'Triggers when no Mercado Pago webhook events are seen in 15 minutes'
    enabled: true
    evaluationFrequency: 'PT5M'
    severity: 1
    scopes: [ law.id ]
    windowSize: 'PT15M'
    criteria: {
      allOf: [
        {
          name: 'no-webhook'
          query: '''
customEvents
| where name == "mp_webhook_received"
| summarize count() by bin(timestamp, 15m)
| where count_ == 0
'''
          timeAggregation: 'Count'
          operator: 'Equal'
          threshold: 0
        }
      ]
    }
    actions: {
      actionGroups: [
        { actionGroupId: actionGroup.id }
      ]
    }
  }
}

@description('P2: High payment failure rate in 10 minutes')
resource alert_failed_payments 'Microsoft.Insights/scheduledQueryRules@2022-06-15' = {
  name: 'arkana-p2-high-failed-payments'
  location: location
  properties: {
    description: 'Triggers when failed payments exceed threshold in a short window'
    enabled: true
    evaluationFrequency: 'PT5M'
    severity: 2
    scopes: [ law.id ]
    windowSize: 'PT10M'
    criteria: {
      allOf: [
        {
          name: 'fail-rate'
          query: '''
let failures = customEvents | where name == "payment_failed" | summarize fails=count() by bin(timestamp, 10m);
let successes = customEvents | where name == "purchase_approved" | summarize ok=count() by bin(timestamp, 10m);
failures
| join kind=fullouter successes on timestamp
| extend ok = coalesce(ok, 0), fails = coalesce(fails, 0)
| extend rate = todouble(fails) / todouble(iif(ok==0, 1, ok))
| where fails >= 3 or rate >= 0.3
'''
          timeAggregation: 'Count'
          operator: 'GreaterThanOrEqual'
          threshold: 1
        }
      ]
    }
    actions: {
      actionGroups: [
        { actionGroupId: actionGroup.id }
      ]
    }
  }
}

output appInsightsConnectionString string = ai.properties.ConnectionString
output logAnalyticsWorkspaceId string = law.id
