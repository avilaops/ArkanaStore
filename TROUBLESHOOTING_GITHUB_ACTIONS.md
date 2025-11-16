# ?? TROUBLESHOOTING - GITHUB ACTIONS ARKANA

> **Soluções para problemas comuns do deployment**  
> **Data**: 16/01/2025

---

## ? PROBLEMA REPORTADO

**Sintoma**: "o github actions não deu certo"

**Causas possíveis**:
1. Secret `AZURE_WEBAPP_PUBLISH_PROFILE` não configurado
2. Erro de sintaxe no workflow YAML
3. Recursos Azure não existem ainda
4. Permissões insuficientes

---

## ? SOLUÇÃO IMPLEMENTADA

### **Mudança**: Workflow simplificado para **Azure Static Web Apps**

**ANTES** (App Service - complexo):
```yaml
- Deploy to Azure Web App
  with:
    app-name: arkana-store
    publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

**DEPOIS** (Static Web Apps - simples):
```yaml
- Build And Deploy
  uses: Azure/static-web-apps-deploy@v1
  with:
    azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
```

**Vantagens Static Web Apps**:
- ? **GRÁTIS** até 100GB bandwidth/mês
- ? **HTTPS automático**
- ? **CDN global incluído**
- ? **Staging automático** (PR previews)
- ? **Sem servidor Python** necessário (APIs via Functions)
- ? **Deploy mais rápido** (~30 segundos)

---

## ?? CONFIGURAR AGORA (3 Passos)

### **PASSO 1: Criar Azure Static Web App**

#### **Opção A: Via Portal Azure** (Recomendado - mais fácil)

1. **Acesse**: https://portal.azure.com

2. **Criar recurso**:
   ```
   Buscar: "Static Web Apps"
   ? Criar
   ```

3. **Preencher**:
   ```
   Subscription: <sua subscription>
   Resource Group: arkana-store-rg (criar novo)
   Name: arkana-store
   Plan: Free
   Region: Brazil South
   
   Deployment:
   Source: GitHub
   Organization: avilaops
   Repository: ArkanaStore
   Branch: main
   
   Build Details:
   Build Presets: Custom
   App location: /
   Api location: automation/admin
   Output location: /
   ```

4. **Review + Create**

5. **Após criação**:
   - Azure vai criar um **commit automático** no seu repo
   - Esse commit adiciona o secret `AZURE_STATIC_WEB_APPS_API_TOKEN` automaticamente!
   - GitHub Actions já começa a rodar!

---

#### **Opção B: Via Azure CLI** (Avançado)

```powershell
# 1. Login
az login

# 2. Criar Static Web App
az staticwebapp create `
    --name arkana-store `
    --resource-group arkana-store-rg `
    --source https://github.com/avilaops/ArkanaStore `
    --location brazilsouth `
    --branch main `
    --app-location "/" `
    --api-location "automation/admin" `
    --output-location "/" `
    --login-with-github

# 3. Obter API token
az staticwebapp secrets list `
    --name arkana-store `
    --resource-group arkana-store-rg `
    --query "properties.apiKey" -o tsv
```

**Copie o token** e adicione como secret no GitHub!

---

### **PASSO 2: Verificar Secret no GitHub**

1. **Vá para**: https://github.com/avilaops/ArkanaStore/settings/secrets/actions

2. **Verifique se existe**:
   ```
   AZURE_STATIC_WEB_APPS_API_TOKEN
   ```

3. **Se NÃO existir**:
   - Clique "New repository secret"
   - Name: `AZURE_STATIC_WEB_APPS_API_TOKEN`
   - Secret: `<token obtido no passo 1>`
   - Add secret

---

### **PASSO 3: Testar Workflow**

```powershell
# Fazer um pequeno commit para trigger
git add .github/workflows/azure-deploy.yml
git commit -m "fix: update workflow for static web apps"
git push origin main
```

**Acompanhar**:
- https://github.com/avilaops/ArkanaStore/actions

**Deploy leva**: ~30-60 segundos ?

---

## ?? COMPARAÇÃO: APP SERVICE vs STATIC WEB APPS

| Aspecto | App Service | Static Web Apps |
|---------|-------------|-----------------|
| **Custo** | R$ 60+/mês (B1) | **GRÁTIS** (100GB/mês) |
| **Setup** | Complexo | **Simples** (1 clique) |
| **Deploy** | ~5 min | **~30 seg** |
| **Backend** | Python/Node full | Functions apenas |
| **HTTPS** | Manual | **Automático** |
| **CDN** | Separado | **Incluído** |
| **Staging** | Slots pagos | **PR previews grátis** |
| **Melhor para** | Apps complexas | Sites + APIs simples |

**Recomendação Arkana**: **Static Web Apps** ??

---

## ?? VERIFICAR ERRO ATUAL DO WORKFLOW

### **Ver logs do GitHub Actions**:

1. **GitHub** ? **Actions**
2. Clique no **último workflow** (vermelho ?)
3. Clique em **"build_and_deploy"**
4. **Ver logs detalhados**

**Erros comuns**:

| Erro | Causa | Solução |
|------|-------|---------|
| `secret not found` | Secret não configurado | Adicionar secret |
| `invalid yaml` | Sintaxe YAML errada | Validar em yamllint.com |
| `resource not found` | Azure resource não existe | Criar Static Web App |
| `permission denied` | Token sem permissão | Regenerar token |

---

## ? WORKFLOW ATUALIZADO

**Arquivo**: `.github/workflows/azure-deploy.yml`

**Mudanças**:
- ? Mudou de **App Service** ? **Static Web Apps**
- ? Sintaxe simplificada
- ? Apenas 1 secret necessário
- ? Deploy mais rápido
- ? Grátis para sempre

**Commit**: Já foi feito!  
**Próximo**: Configurar Azure Static Web App

---

## ?? AÇÃO IMEDIATA

### **Execute AGORA** (Portal Azure - mais fácil):

1. **Abra**: https://portal.azure.com

2. **Criar Static Web App**:
   ```
   + Create a resource
   ? Static Web Apps
   ? Create
   
   Preencher:
   ?? Name: arkana-store
   ?? Region: Brazil South
   ?? Plan: Free
   ?? Source: GitHub
   ?? Repo: avilaops/ArkanaStore
   ?? Branch: main
   ```

3. **Autorizar GitHub** (popup)

4. **Review + Create**

5. **Aguardar** ~2 minutos

**Pronto!** ??

Azure vai:
- ? Criar o recurso
- ? Adicionar secret no GitHub automaticamente
- ? Fazer commit com workflow (pode sobrescrever o nosso)
- ? Deploy automático

---

## ?? ALTERNATIVA: DEPLOY CLOUDFLARE PAGES (Mais Simples)

Se Azure continuar dando problema, use **Cloudflare Pages** (grátis, zero config):

### **Setup em 2 minutos**:

1. **Acesse**: https://pages.cloudflare.com

2. **Connect GitHub**:
   ```
   Connect account
   ? avilaops/ArkanaStore
   ? Begin setup
   ```

3. **Configurar**:
   ```
   Project name: arkana-store
   Production branch: main
   Build command: (deixar vazio)
   Build output directory: /
   ```

4. **Save and Deploy**

**URL gerada**:
```
https://arkana-store.pages.dev
```

**Vantagens**:
- ? **100% grátis**
- ? **Deploy em 20 segundos**
- ? **CDN global Cloudflare**
- ? **HTTPS automático**
- ? **Zero configuração**
- ? **Preview deploys automáticos**

---

## ?? CHECKLIST TROUBLESHOOTING

### **GitHub Actions falhou? Verifique**:

- [ ] Workflow YAML tem sintaxe válida
  ```powershell
  # Validar localmente
  cat .github/workflows/azure-deploy.yml
  ```

- [ ] Secret configurado no GitHub
  ```
  Settings ? Secrets ? Actions
  Deve ter: AZURE_STATIC_WEB_APPS_API_TOKEN
  ```

- [ ] Azure Static Web App existe
  ```powershell
  az staticwebapp list -o table
  ```

- [ ] Branch está correta (main)
  ```powershell
  git branch --show-current
  ```

- [ ] Último commit foi pushed
  ```powershell
  git log origin/main..HEAD
  # Deve estar vazio (tudo pushed)
  ```

---

## ?? LOGS DO ERRO

**Para eu ajudar melhor, me mostre**:

1. **Screenshot** do erro no GitHub Actions
   - Ou copie a mensagem de erro

2. **Output** do último workflow:
   ```
   GitHub ? Actions ? <workflow name> ? View logs
   ```

3. **Comando** que deu erro:
   ```powershell
   git log -1 --oneline
   # Me mostre o output
   ```

---

## ?? SOLUÇÃO RÁPIDA (Enquanto Azure não funciona)

### **Deploy local com Python simples**:

```powershell
# 1. Ir para pasta automation
cd automation/admin

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar servidor local
python api_server.py

# 4. Abrir sites localmente
cd ../..
Start-Process "arkana-admin-panel.html"
Start-Process "arkana-store-v2.html"
```

**Resultado**:
- ? Backend rodando em `http://localhost:5000`
- ? Sites funcionando localmente
- ? Testa enquanto configura Azure

---

## ?? PRÓXIMA TENTATIVA

Depois de configurar Azure Static Web App:

```powershell
# Commit vazio para trigger workflow
git commit --allow-empty -m "trigger: test azure deployment"
git push origin main

# Acompanhar
Start-Process "https://github.com/avilaops/ArkanaStore/actions"
```

---

## ?? ME MOSTRE

Para eu resolver, **me mostre**:

1. **Erro do GitHub Actions** (screenshot ou texto)
2. **Último commit**: `git log -1`
3. **Secrets configurados**: Screenshot de `Settings ? Secrets`
4. **Recursos Azure**: `az staticwebapp list -o table` (se rodou CLI)

**Ou me diga**:
- ? "Qual foi a mensagem de erro?"
- ? "O secret está configurado?"
- ? "Prefere usar Cloudflare Pages invés de Azure?"

---

## ? ARQUIVOS PRONTOS (Commitados)

```
? .github/workflows/azure-deploy.yml (atualizado)
? infra/main.bicep
? scripts/deploy-azure.ps1
? DEPLOY_AZURE.md
? SETUP_AZURE_AGORA.md
```

**Status Git**:
```
Commit: df6db16
Pushed: ?
Remote: https://github.com/avilaops/ArkanaStore
```

---

**??? Aguardando informações do erro para resolver!**

*Enquanto isso, você pode testar localmente* ??
