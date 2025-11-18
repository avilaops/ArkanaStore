# 🏪 ARKANA STORE

> **E-commerce Premium de Moda Contemporânea**
> Stack 100% Gratuita | Rust + WASM + MongoDB + Docker

[![CI/CD](https://github.com/avilaops/ArkanaStore/actions/workflows/ci.yml/badge.svg)](https://github.com/avilaops/ArkanaStore/actions/workflows/ci.yml)
[![Deploy](https://github.com/avilaops/ArkanaStore/actions/workflows/deploy.yml/badge.svg)](https://github.com/avilaops/ArkanaStore/actions/workflows/deploy.yml)
[![GitHub Pages](https://img.shields.io/badge/demo-live-success)](https://avilaops.github.io/ArkanaStore/)

---

## 🎯 Visão Geral

**Arkana Store** é uma plataforma de e-commerce moderna e performática, construída com tecnologias de ponta e infraestrutura 100% gratuita.

### ✨ Características Principais

- 🚀 **Frontend**: Yew (Rust WASM) - performance nativa no browser
- ⚡ **Backend**: Actix-web (Rust) - alta performance e segurança
- 🗄️ **Database**: MongoDB 7.0 - flexibilidade NoSQL
- 🔴 **Cache**: Redis 7 - velocidade em sessões e cache
- 📦 **Storage**: MinIO (S3-compatible) - armazenamento de imagens
- 🔐 **Auth**: Serviço compartilhado (auth.avila.inc)
- 🌐 **Proxy**: Traefik com SSL automático (Let's Encrypt)
- 📊 **Monitoring**: Prometheus + Grafana + Loki

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Pages                         │
│              avilaops.github.io/ArkanaStore             │
│                    (Frontend WASM)                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Traefik (Reverse Proxy)              │
│                  arkana.avila.inc (SSL)                 │
└─────────────────────────────────────────────────────────┘
          ↓                    ↓                    ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Arkana API  │    │ Auth Service │    │    MinIO     │
│  (Actix-web) │    │  (FastAPI)   │    │  (Storage)   │
└──────────────┘    └──────────────┘    └──────────────┘
     ↓      ↓              ↓                    ↓
┌─────────┐ ┌─────────┐ ┌────────────────────────────┐
│ MongoDB │ │  Redis  │ │  Prometheus + Grafana      │
└─────────┘ └─────────┘ └────────────────────────────┘
```

---

## 🚀 Quick Start

### Pré-requisitos

- Docker & Docker Compose
- Rust 1.70+ (para desenvolvimento local)
- Node.js 18+ (opcional, para ferramentas)

### 1. Clone o Repositório

```bash
git clone https://github.com/avilaops/ArkanaStore.git
cd ArkanaStore
```

### 2. Configure as Variáveis de Ambiente

```bash
cp .env.example .env
# Edite .env com suas credenciais
```

### 3. Inicie a Stack Completa

```bash
# Subir toda a infraestrutura
docker-compose -f docker-compose.avila-full.yml up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f arkana-api
```

### 4. Acesse as Aplicações

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | https://avilaops.github.io/ArkanaStore/ | Site público |
| **API** | https://arkana.avila.inc/api | Backend REST |
| **Auth** | https://auth.avila.inc | Serviço de autenticação |
| **Storage** | https://storage.arkana.avila.inc | MinIO (S3) |
| **Grafana** | https://grafana.arkana.avila.inc | Dashboards |
| **Prometheus** | https://metrics.arkana.avila.inc | Métricas |
| **Traefik** | https://traefik.arkana.avila.inc | Dashboard proxy |

---

## 🛠️ Desenvolvimento Local

### Backend (Rust + Actix-web)

```bash
cd arkana-backend

# Instalar dependências
cargo build

# Rodar testes
cargo test

# Desenvolvimento com hot-reload
cargo watch -x run

# Build release
cargo build --release
```

### Frontend (Rust + Yew + WASM)

```bash
cd arkana-frontend

# Instalar Trunk
cargo install trunk

# Desenvolvimento
trunk serve

# Build para produção
trunk build --release --public-url /ArkanaStore/
```

---

## 📦 Estrutura do Projeto

```
ArkanaStore/
├── arkana-backend/         # API Rust (Actix-web)
│   ├── src/
│   │   ├── main.rs         # Entry point
│   │   ├── config.rs       # Configuração
│   │   ├── db.rs           # MongoDB client
│   │   ├── handlers/       # Rotas REST
│   │   ├── services/       # Lógica de negócio
│   │   └── webhooks/       # Webhooks (PayPal, Stripe)
│   ├── Dockerfile
│   └── Cargo.toml
│
├── arkana-frontend/        # SPA Yew (WASM)
│   ├── src/
│   │   ├── lib.rs          # Entry point
│   │   ├── pages/          # Componentes de página
│   │   └── components/     # Componentes reutilizáveis
│   ├── static/
│   │   └── styles.css      # Estilos globais
│   ├── index.html
│   ├── Dockerfile
│   └── Cargo.toml
│
├── arkana-shared/          # Código compartilhado
│   ├── src/
│   │   └── lib.rs          # Types compartilhados
│   └── Cargo.toml
│
├── docs/                   # Site estático (GitHub Pages)
│   ├── index.html
│   └── styles.css
│
├── monitoring/             # Configurações de monitoring
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   ├── loki/
│   │   └── loki-config.yml
│   └── promtail/
│       └── promtail-config.yml
│
├── .github/
│   └── workflows/
│       ├── ci.yml          # Testes + build
│       ├── deploy.yml      # Deploy WASM → GitHub Pages
│       └── pages.yml       # Deploy docs estáticos
│
├── docker-compose.avila-full.yml  # Stack completa
├── .env                    # Variáveis de ambiente
└── README.md
```

---

## 🔄 CI/CD

### GitHub Actions

#### 1. **CI** (`.github/workflows/ci.yml`)
- ✅ Testes unitários
- ✅ Build backend (Rust)
- ✅ Build frontend (WASM)
- ✅ Lint e formatação
- 🐘 MongoDB e Redis em services

#### 2. **Deploy GitHub Pages** (`.github/workflows/deploy.yml`)
- 🎯 Trigger manual (`workflow_dispatch`)
- 📦 Build WASM com Trunk
- 🚀 Deploy para GitHub Pages
- 🌐 URL: https://avilaops.github.io/ArkanaStore/

#### 3. **Deploy Docs** (`.github/workflows/pages.yml`)
- 📄 Deploy site estático HTML/CSS
- ⚡ Automático em push para `main`

---

## 🐳 Docker

### Serviços

| Serviço | Imagem | Porta | Descrição |
|---------|--------|-------|-----------|
| **mongodb** | `mongo:7.0` | 27017 | Database principal |
| **redis** | `redis:7-alpine` | 6379 | Cache e sessões |
| **minio** | `minio/minio:latest` | 9000, 9001 | Storage S3 |
| **traefik** | `traefik:v3.0` | 80, 443 | Reverse proxy + SSL |
| **arkana-api** | Custom | 8000 | Backend Rust |
| **arkana-frontend** | Custom | 80 | Frontend WASM |
| **auth** | Custom | 8000 | Auth service (Portal) |
| **prometheus** | `prom/prometheus:latest` | 9090 | Métricas |
| **grafana** | `grafana/grafana:latest` | 3000 | Dashboards |
| **loki** | `grafana/loki:latest` | 3100 | Logs |
| **promtail** | `grafana/promtail:latest` | - | Collector logs |

### Comandos Úteis

```bash
# Subir stack
docker-compose -f docker-compose.avila-full.yml up -d

# Parar stack
docker-compose -f docker-compose.avila-full.yml down

# Rebuild e restart
docker-compose -f docker-compose.avila-full.yml up -d --build

# Ver logs
docker-compose logs -f [service]

# Entrar em container
docker exec -it arkana-mongodb mongosh
docker exec -it arkana-redis redis-cli

# Backup MongoDB
docker exec arkana-mongodb mongodump --out /backup

# Limpar volumes
docker-compose down -v
```

---

## 📊 Monitoring

### Prometheus

- **URL**: https://metrics.arkana.avila.inc
- **Configuração**: `monitoring/prometheus/prometheus.yml`
- **Targets**: API, Auth, MongoDB, Redis

### Grafana

- **URL**: https://grafana.arkana.avila.inc
- **Usuário**: `admin`
- **Senha**: Definida em `.env` (`GRAFANA_PASSWORD`)
- **Dashboards**: Importar de `monitoring/grafana/dashboards/`

### Loki + Promtail

- **Logs centralizados** de todos os containers
- **Consulta** via Grafana Explore
- **Alertas** configuráveis

---

## 🔐 Segurança

### Boas Práticas Implementadas

- ✅ **SSL/TLS** automático via Let's Encrypt
- ✅ **Secrets** via variáveis de ambiente (`.env`)
- ✅ **JWT** para autenticação
- ✅ **CORS** configurado
- ✅ **Rate limiting** (Traefik)
- ✅ **Healthchecks** em todos os serviços
- ✅ **Logs** auditáveis (Loki)

### Variáveis Sensíveis

```bash
# .env (NUNCA commitar!)
MONGO_PASSWORD=...
REDIS_PASSWORD=...
JWT_SECRET=...
SMTP_PASSWORD=...
GRAFANA_PASSWORD=...
```

---

## 🧪 Testes

```bash
# Testes unitários
cargo test --all

# Testes de integração
cargo test --test integration_tests

# Cobertura
cargo tarpaulin --out Html
```

---

## 📝 API Endpoints

### Public

```
GET  /health              # Healthcheck
GET  /api/products        # Listar produtos
GET  /api/products/:id    # Detalhes produto
POST /api/cart            # Adicionar ao carrinho
```

### Authenticated

```
GET    /api/orders        # Listar pedidos
POST   /api/orders        # Criar pedido
GET    /api/profile       # Perfil usuário
PUT    /api/profile       # Atualizar perfil
```

### Webhooks

```
POST /webhooks/paypal     # PayPal webhook
POST /webhooks/stripe     # Stripe webhook
POST /webhooks/mercadopago # MercadoPago webhook
```

---

## 🚢 Deploy em Produção

### Opção 1: VPS com Docker Compose

```bash
# No servidor
git clone https://github.com/avilaops/ArkanaStore.git
cd ArkanaStore
cp .env.example .env
# Configurar .env com credenciais de produção
docker-compose -f docker-compose.avila-full.yml up -d
```

### Opção 2: GitHub Pages (Frontend apenas)

- ✅ **Automático** via GitHub Actions
- ✅ URL: https://avilaops.github.io/ArkanaStore/
- ✅ Backend separado (API em servidor próprio)

### Backup

```bash
# Executar script de backup (OneDrive)
./scripts/backup-to-onedrive.sh
```

---

## 📚 Stack Tecnológica

### Backend
- **Rust 1.70+** - Linguagem principal
- **Actix-web 4.4** - Framework web
- **MongoDB 7.0** - Database NoSQL
- **Redis 7** - Cache
- **Sentry** - Error tracking

### Frontend
- **Yew 0.21** - Framework WASM
- **Trunk** - Build tool
- **WASM** - WebAssembly
- **CSS3** - Estilização

### DevOps
- **Docker** - Containerização
- **Traefik** - Reverse proxy
- **GitHub Actions** - CI/CD
- **Prometheus + Grafana** - Monitoring
- **Loki** - Logs

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m 'feat: adiciona nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é **privado** e de propriedade da **Ávila Inc**.

---

## 🔗 Links Úteis

- 🌐 [Site Demo](https://avilaops.github.io/ArkanaStore/)
- 📊 [Grafana](https://grafana.arkana.avila.inc)
- 📈 [Prometheus](https://metrics.arkana.avila.inc)
- 🔐 [Auth Service](https://auth.avila.inc)
- 📦 [MinIO](https://storage.arkana.avila.inc)

---

## 📞 Contato

**Ávila Inc**
- 📧 Email: dev@avila.inc
- 📱 WhatsApp: (17) 99665-6163
- 🌐 Portal: https://portal.avila.inc

---

**Stack 100% Gratuita | Performance Nativa | DevOps Moderno**

*Última atualização: 18/11/2025*
