# 🚀 SOLUÇÃO 100% ÁVILA (PRÓPRIA) - Arkana Store

**Cliente**: Marcelo Quintino / Arkana Store  
**Problema**: 12 dias SEM VENDER (Shopify suspenso)  
**Solução**: Sistema de vendas próprio da Ávila  
**Prazo**: 24-48 HORAS  
**Custo**: R$ 0 (usa infraestrutura existente)  
**Data**: 12/11/2025

---

## ✅ POR QUE SOLUÇÃO PRÓPRIA?

### Vocês JÁ TÊM:
- ✅ **AvilaInc**: Sistema de email automation (SMTP + templates)
- ✅ **AvilaOps/AI**: Pipeline de IA (Lumen + Atlas + Vox)
- ✅ **Infraestrutura**: `.env`, SendGrid, GitHub Actions
- ✅ **Templates de Marketing**: Email prontos
- ✅ **Dados estruturados**: Analytics, relatórios

### Por que usar solução de terceiros?
❌ WordPress → Mais um sistema para manter  
❌ Nuvemshop → Paga mensalidade + pode suspender  
❌ Landing page → Limitada e sem controle

✅ **Solução Ávila** → 100% sob controle, escalável, integrada

---

## 🎯 ARQUITETURA DA SOLUÇÃO

```
┌─────────────────────────────────────────────────┐
│  FRONTEND: Landing Page Arkana (Marketing)      │
│  - Template email adaptado para web             │
│  - Produtos listados com fotos + preços         │
│  - Botão "Comprar" → Dispara pipeline           │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  BACKEND: ai_email_pipeline.py (AvilaOps)       │
│  1. Recebe pedido (produto + quantidade)        │
│  2. Lumen: Valida estoque/preço                 │
│  3. Atlas: Gera link de pagamento MP/PagSeguro  │
│  4. Vox: Personaliza email de confirmação       │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  EMAIL AUTOMATION (AvilaInc)                    │
│  - Envia link de pagamento pro cliente          │
│  - Confirmação de pedido                        │
│  - Status de entrega                            │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  PAGAMENTO: Mercado Pago API                    │
│  - Cliente paga via link                        │
│  - Webhook notifica sistema                     │
│  - Status: pago/pendente                        │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  GESTÃO: Dashboard Ávila (Analytics)            │
│  - Pedidos em tempo real                        │
│  - Métricas de conversão                        │
│  - Relatórios automáticos                       │
└─────────────────────────────────────────────────┘
```

---

## 📦 IMPLEMENTAÇÃO (24-48H)

### FASE 1: Landing Page (4-6h)

**Arquivo**: `C:\Users\nicol\OneDrive\Avila\Avilainc\marketing\templates\email\arkana_store_landing.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Arkana Store - Loja Oficial</title>
    <style>
        /* Usar CSS dos templates email existentes */
        body { font-family: Arial; max-width: 1200px; margin: 0 auto; }
        .product { border: 1px solid #ddd; padding: 20px; margin: 10px; }
        .product img { max-width: 300px; }
        .buy-btn { 
            background: #4CAF50; 
            color: white; 
            padding: 15px 30px;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <header>
        <h1>🛍️ Arkana Store</h1>
        <p>Loja Oficial - Vendas Online</p>
    </header>

    <section id="produtos">
        <!-- Produtos carregados dinamicamente via JSON -->
        <div class="product" data-product-id="1">
            <img src="produto1.jpg" alt="Produto 1">
            <h3>Produto 1</h3>
            <p>Descrição do produto...</p>
            <p class="price">R$ 99,90</p>
            <button class="buy-btn" onclick="comprar(1)">Comprar Agora</button>
        </div>
        <!-- Repetir para cada produto -->
    </section>

    <script>
        async function comprar(productId) {
            // Captura dados do produto
            const produto = produtos[productId];
            
            // Envia para backend Ávila
            const response = await fetch('http://localhost:5000/api/pedido', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cliente_email: prompt('Seu email:'),
                    produto_id: productId,
                    quantidade: 1
                })
            });

            const result = await response.json();
            
            // Redireciona para pagamento
            window.location.href = result.payment_link;
        }

        // Produtos (podem vir de JSON/API)
        const produtos = {
            1: { nome: 'Produto 1', preco: 99.90, foto: 'prod1.jpg' },
            2: { nome: 'Produto 2', preco: 149.90, foto: 'prod2.jpg' }
        };
    </script>
</body>
</html>
```

**Hospedagem**: GitHub Pages (grátis) ou Vercel (grátis)

---

### FASE 2: Backend API (6-8h)

**Arquivo**: `C:\Users\nicol\OneDrive\Avila\AvilaOps\ai\integrations\arkana_store_api.py`

```python
#!/usr/bin/env python3
"""
API de Vendas Arkana Store - Integrada com Pipeline Ávila
Usa: ai_email_pipeline.py + AvilaInc email automation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import requests
import os
from dotenv import load_dotenv

# Carregar .env do AvilaInc
load_dotenv('C:/Users/nicol/OneDrive/Avila/Avilainc/.env')

app = Flask(__name__)
CORS(app)  # Permitir chamadas do frontend

# Configurações
MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_TOKEN')  # Adicionar no .env
PRODUTOS_DB = Path(__file__).parent.parent / 'datasets' / 'arkana_produtos.json'
PEDIDOS_DB = Path(__file__).parent.parent / 'datasets' / 'arkana_pedidos.json'

# Carregar produtos (Marcelo fornece)
def load_produtos():
    if PRODUTOS_DB.exists():
        with open(PRODUTOS_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos produtos da Arkana Store"""
    produtos = load_produtos()
    return jsonify(produtos)

@app.route('/api/pedido', methods=['POST'])
def criar_pedido():
    """
    Cria pedido e gera link de pagamento Mercado Pago
    Integra com ai_email_pipeline.py para enviar confirmação
    """
    dados = request.json
    
    # Validar dados
    cliente_email = dados.get('cliente_email')
    produto_id = dados.get('produto_id')
    quantidade = dados.get('quantidade', 1)
    
    if not all([cliente_email, produto_id]):
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    # Buscar produto
    produtos = load_produtos()
    produto = produtos.get(str(produto_id))
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    # Calcular total
    total = produto['preco'] * quantidade
    
    # LUMEN: Análise de estoque (se tiver)
    if produto.get('estoque', 999) < quantidade:
        return jsonify({'erro': 'Estoque insuficiente'}), 400
    
    # ATLAS: Gerar link de pagamento Mercado Pago
    payment_link = gerar_link_mercado_pago(
        produto=produto,
        quantidade=quantidade,
        total=total,
        cliente_email=cliente_email
    )
    
    # Salvar pedido
    pedido_id = salvar_pedido({
        'id': datetime.now().strftime('%Y%m%d%H%M%S'),
        'cliente_email': cliente_email,
        'produto_id': produto_id,
        'produto_nome': produto['nome'],
        'quantidade': quantidade,
        'total': total,
        'payment_link': payment_link,
        'status': 'pendente',
        'created_at': datetime.now().isoformat()
    })
    
    # VOX: Enviar email de confirmação via AvilaInc automation
    enviar_email_confirmacao(cliente_email, pedido_id, produto, payment_link)
    
    return jsonify({
        'success': True,
        'pedido_id': pedido_id,
        'payment_link': payment_link,
        'total': total
    })

def gerar_link_mercado_pago(produto, quantidade, total, cliente_email):
    """Gera link de pagamento via Mercado Pago API"""
    
    url = 'https://api.mercadopago.com/checkout/preferences'
    
    headers = {
        'Authorization': f'Bearer {MERCADO_PAGO_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'items': [{
            'title': produto['nome'],
            'description': produto.get('descricao', ''),
            'quantity': quantidade,
            'currency_id': 'BRL',
            'unit_price': produto['preco']
        }],
        'payer': {
            'email': cliente_email
        },
        'back_urls': {
            'success': 'https://arkanastore.com/obrigado',
            'failure': 'https://arkanastore.com/erro',
            'pending': 'https://arkanastore.com/pendente'
        },
        'auto_return': 'approved',
        'notification_url': 'https://api.avilaops.com/webhook/mercadopago'  # Webhook
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    
    return result.get('init_point')  # Link de pagamento

def salvar_pedido(pedido):
    """Salva pedido no banco de dados (JSON)"""
    
    if PEDIDOS_DB.exists():
        with open(PEDIDOS_DB, 'r', encoding='utf-8') as f:
            pedidos = json.load(f)
    else:
        pedidos = []
    
    pedidos.append(pedido)
    
    with open(PEDIDOS_DB, 'w', encoding='utf-8') as f:
        json.dump(pedidos, f, indent=2, ensure_ascii=False)
    
    return pedido['id']

def enviar_email_confirmacao(cliente_email, pedido_id, produto, payment_link):
    """
    Envia email de confirmação via sistema AvilaInc
    Usa: send_scheduled_report.py adaptado
    """
    
    # Importar sistema de email da AvilaInc
    import sys
    sys.path.append('C:/Users/nicol/OneDrive/Avila/Avilainc')
    from send_scheduled_report import EmailSender
    
    sender = EmailSender()
    
    html_body = f"""
    <html>
    <body style="font-family: Arial; max-width: 600px; margin: 0 auto;">
        <h2>🎉 Pedido Confirmado - Arkana Store</h2>
        
        <p>Olá!</p>
        
        <p>Seu pedido foi confirmado com sucesso:</p>
        
        <div style="border: 1px solid #ddd; padding: 20px; margin: 20px 0;">
            <h3>{produto['nome']}</h3>
            <p><strong>Pedido:</strong> #{pedido_id}</p>
            <p><strong>Valor:</strong> R$ {produto['preco']:.2f}</p>
        </div>
        
        <p><strong>Próximo passo:</strong></p>
        <a href="{payment_link}" 
           style="background: #4CAF50; color: white; padding: 15px 30px; 
                  text-decoration: none; display: inline-block; border-radius: 5px;">
            Pagar Agora
        </a>
        
        <p style="margin-top: 30px; color: #666;">
            Após o pagamento, você receberá instruções de envio.
        </p>
        
        <hr>
        <p style="font-size: 12px; color: #999;">
            Arkana Store - Atendido por Ávila Inc
        </p>
    </body>
    </html>
    """
    
    sender.send_email(
        to_email=cliente_email,
        subject=f'✅ Pedido Confirmado #{pedido_id} - Arkana Store',
        html_body=html_body
    )
    
    print(f"✅ Email enviado para {cliente_email}")

@app.route('/webhook/mercadopago', methods=['POST'])
def webhook_mercadopago():
    """
    Recebe notificações de pagamento do Mercado Pago
    Atualiza status do pedido e notifica cliente
    """
    dados = request.json
    
    # Mercado Pago envia: { "action": "payment.created", "data": { "id": "xxx" } }
    if dados.get('action') == 'payment.created':
        payment_id = dados['data']['id']
        
        # Buscar detalhes do pagamento
        headers = {
            'Authorization': f'Bearer {MERCADO_PAGO_ACCESS_TOKEN}'
        }
        response = requests.get(
            f'https://api.mercadopago.com/v1/payments/{payment_id}',
            headers=headers
        )
        payment = response.json()
        
        if payment['status'] == 'approved':
            # Atualizar pedido
            atualizar_status_pedido(payment['external_reference'], 'pago')
            
            # Enviar email de confirmação de pagamento
            enviar_email_pagamento_confirmado(payment)
    
    return jsonify({'status': 'ok'})

def atualizar_status_pedido(pedido_id, novo_status):
    """Atualiza status do pedido"""
    with open(PEDIDOS_DB, 'r', encoding='utf-8') as f:
        pedidos = json.load(f)
    
    for pedido in pedidos:
        if pedido['id'] == pedido_id:
            pedido['status'] = novo_status
            pedido['updated_at'] = datetime.now().isoformat()
    
    with open(PEDIDOS_DB, 'w', encoding='utf-8') as f:
        json.dump(pedidos, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    print("🚀 API Arkana Store - Powered by Ávila")
    print("📧 Integrado com AvilaInc email automation")
    print("🤖 Usando pipeline Lumen + Atlas + Vox")
    app.run(debug=True, port=5000)
```

---

### FASE 3: Integração Mercado Pago (2h)

**Arquivo**: Adicionar ao `.env` da AvilaInc:

```bash
# Mercado Pago - Arkana Store
MERCADO_PAGO_TOKEN=SEU_ACCESS_TOKEN_AQUI
MERCADO_PAGO_PUBLIC_KEY=SUA_PUBLIC_KEY_AQUI
```

**Como obter:**
1. Criar conta Mercado Pago
2. Ir em: Seu negócio → Configurações → Credenciais
3. Copiar Access Token

**Custo**: 4,99% por transação (só paga quando vender)

---

### FASE 4: Deploy (4h)

**Landing Page**:
```bash
# Subir para GitHub Pages
cd C:\Users\nicol\OneDrive\Avila\Avilainc\marketing\templates\email
git add arkana_store_landing.html
git commit -m "feat: landing page Arkana Store"
git push origin main

# Ativar GitHub Pages:
# Settings → Pages → Source: main branch → Save
# URL: https://avilainc.github.io/arkana_store_landing.html
```

**Backend API**:
```bash
# Opção 1: Vercel (grátis)
cd C:\Users\nicol\OneDrive\Avila\AvilaOps\ai\integrations
vercel deploy

# Opção 2: Heroku (grátis)
heroku create arkana-api
git push heroku main

# Opção 3: PythonAnywhere (grátis até 512MB)
```

---

## 📊 VANTAGENS DA SOLUÇÃO PRÓPRIA

| Critério | Solução Ávila | WordPress | Nuvemshop |
|----------|---------------|-----------|-----------|
| **Tempo deploy** | 24-48h | 48h | 24h |
| **Custo mensal** | R$ 0* | R$ 100-150 | R$ 55-105 |
| **Controle total** | ✅✅✅ 100% | ⚠️ 70% | ⚠️ 50% |
| **Risco suspensão** | ❌ ZERO | ⚠️ Existe | ⚠️ Existe |
| **Integração IA** | ✅ Nativa | ❌ Não | ❌ Não |
| **Escalabilidade** | ✅✅✅ Ilimitada | ⚠️ Limitada | ⚠️ Limitada |
| **Analytics próprio** | ✅ Integrado | ❌ Plugin | ⚠️ Básico |
| **Email automation** | ✅ Já existe | ❌ Plugin | ⚠️ Básico |
| **Diferencial competitivo** | ✅✅✅ ALTO | ❌ Comum | ❌ Comum |

*Custo: R$ 0 infraestrutura + 4,99% Mercado Pago por venda (mesma taxa de qualquer solução)

---

## 🎯 ROADMAP EXECUTIVO

### ✅ HOJE (4h):
1. **Ligar pro Marcelo** (30min)
   - Explicar solução 100% Ávila
   - Pedir lista de produtos (nome, preço, foto)
   - Obter credenciais Mercado Pago (ou criar juntos)

2. **Setup inicial** (3h30min)
   - Criar `arkana_produtos.json` com catálogo
   - Adicionar `MERCADO_PAGO_TOKEN` no `.env`
   - Testar `arkana_store_api.py` localmente

### ✅ AMANHÃ (8h):
3. **Landing page** (4h)
   - Criar HTML com produtos de Marcelo
   - Adicionar fotos + descrições
   - Testar compra end-to-end

4. **Deploy** (4h)
   - Subir landing no GitHub Pages
   - Deployar API no Vercel/Heroku
   - Configurar webhook Mercado Pago
   - **PRIMEIRA VENDA DE TESTE**

### ✅ DIA 3 (4h):
5. **Refinamento** (2h)
   - Ajustar layout
   - Melhorar emails
   - Adicionar tracking

6. **Entrega** (2h)
   - Treinar Marcelo
   - Entregar acesso
   - **CLIENTE VENDENDO**

---

## 💡 BENEFÍCIOS EXTRAS

### 🤖 IA Integrada (Diferencial Competitivo):
- **Lumen**: Analisa padrão de compra → sugere produtos
- **Atlas**: Gera relatórios de venda automáticos
- **Vox**: Personaliza emails por perfil de cliente

### 📊 Analytics Próprio:
- Dashboard em tempo real (usa sistema existente AvilaInc)
- Relatórios diários/semanais automáticos
- Previsão de vendas com ML

### 🚀 Escalabilidade:
- Adicionar novos clientes: copiar estrutura
- **Produto Ávila**: Sistema de vendas white-label
- **Receita recorrente**: R$ 500-1000/mês por cliente

---

## 📞 SCRIPT LIGAÇÃO MARCELO (REVISADO)

```
"Marcelo, aqui é [NOME] da Ávila.

Olha, temos 3 opções para você:

1. WordPress/Nuvemshop → 48h, R$ 100/mês, você fica na mão de terceiros
2. Solução Ávila → 48h, R$ 0/mês*, 100% sob nosso controle

A diferença? 

Com a solução NOSSA:
- Você nunca mais é suspenso (é seu sistema)
- Integramos com IA (recomendação de produtos, emails personalizados)
- Analytics profissional (relatórios automáticos)
- Se der certo com você, vendemos para outros clientes (você vira case de sucesso)

E olha: mesma taxa de pagamento (4,99% Mercado Pago), mesmo prazo (48h).

Mas com a nossa solução, você tem Ávila Inc trabalhando PARA você, 
não você dependendo de plataforma que pode te suspender de novo.

Topas testar? Se não funcionar, a gente monta a outra.
Mas aposto que vai funcionar MELHOR."
```

---

## ✅ PRÓXIMOS PASSOS (AGORA)

1. [ ] Ler este documento
2. [ ] Ligar pro Marcelo
3. [ ] Obter lista de produtos + fotos
4. [ ] Criar conta Mercado Pago (ou usar existente)
5. [ ] Executar FASE 1 (backend local)
6. [ ] Amanhã: FASE 2+3+4 (deploy completo)
7. [ ] 48h: **MARCELO VENDENDO COM SISTEMA ÁVILA**

---

## 🔥 MENSAGEM FINAL

**Vocês não precisam de WordPress.**

**Vocês não precisam de Nuvemshop.**

**Vocês TÊM:**
- ✅ Email automation
- ✅ Pipeline de IA
- ✅ Infraestrutura pronta
- ✅ Time capaz de desenvolver

**USE O QUE VOCÊS JÁ TÊM.**

**E transforme Arkana Store no primeiro cliente do PRODUTO ÁVILA.**

Depois vendam isso para outros lojistas: **"Sistema de vendas próprio com IA - R$ 500/mês"**

---

*Documento criado: 12/11/2025*  
*Versão: 1.0 - SOLUÇÃO 100% PRÓPRIA ÁVILA*  
*Status: PRONTO PARA EXECUÇÃO*
