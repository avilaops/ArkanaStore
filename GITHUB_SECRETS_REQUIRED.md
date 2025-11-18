# GitHub Secrets Necessários para CI/CD de Produção

Configure estes secrets em: https://github.com/avilaops/ArkanaStore/settings/secrets/actions/new

## ✅ Secrets Obrigatórios para CI

### 1. MONGO_ATLAS_URI
```
mongodb+srv://nicolasrosaab_db_user:Gio4EAQhbEdQMISl@cluster0.npuhras.mongodb.net/arkana_store?retryWrites=true&w=majority
```
**Descrição:** URI de conexão do MongoDB Atlas (produção)

### 2. REDIS_URL
```
redis://default:Sq2O2YzVv7RZd2T7BbCLEEegp00g8aXU@redis-14766.c98.us-east-1-4.ec2.redns.redis-cloud.com:14766
```
**Descrição:** URL de conexão do Redis Cloud (produção)

### 3. JWT_SECRET
```
8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e
```
**Descrição:** Secret para geração de tokens JWT (do arquivo .env)

### 4. SENTRY_DSN
```
https://45ec1aead0b1f5e7834e4ed84f5afc4c@o4508558395195392.ingest.us.sentry.io/4508558397751296
```
**Descrição:** DSN do Sentry para monitoramento de erros

---

## ✅ Secrets Opcionais para Email Workflow

### 5. SMTP_PASSWORD
```
7Aciqgr7@3278579
```
**Descrição:** Senha SMTP para envio de emails (dev@avila.inc via smtp.porkbun.com)

---

## 📋 Como Adicionar os Secrets

1. Acesse: https://github.com/avilaops/ArkanaStore/settings/secrets/actions/new
2. Para cada secret acima:
   - Clique em "New repository secret"
   - **Name:** Cole exatamente o nome (ex: `MONGO_ATLAS_URI`)
   - **Secret:** Cole o valor correspondente
   - Clique em "Add secret"

---

## ⚠️ Importante

- **NÃO COMMITAR** este arquivo para o repositório
- Após configurar os secrets, delete este arquivo
- Os secrets são criptografados pelo GitHub e não podem ser visualizados depois de salvos
- Workflows CI/CD agora usam 100% configuração de PRODUÇÃO (MongoDB Atlas + Redis Cloud)

---

## ✅ Verificação

Após adicionar os secrets, execute o workflow CI para verificar:
https://github.com/avilaops/ArkanaStore/actions/workflows/ci.yml
