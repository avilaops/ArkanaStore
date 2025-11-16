#!/usr/bin/env python3
"""
?? ARKANA ADMIN - REST API (SQLite Edition)
===========================================
API REST com SQLite database

Data: 16/11/2025
Versão: 2.0.0
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from arkana_database import ArkanaDatabase
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Inicializar database
db = ArkanaDatabase()

# ===================================================================
# PRODUTOS
# ===================================================================

@app.route('/api/products', methods=['GET'])
def list_products():
    """Lista todos os produtos"""
    try:
        cursor = db.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE active = 1 ORDER BY created_at DESC')
        products = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'success': True,
            'data': products,
            'total': len(products)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Cria novo produto"""
    try:
        data = request.json
        cursor = db.conn.cursor()
        
        sku = f"ARK-{datetime.now().strftime('%Y%m%d')}-{cursor.execute('SELECT COUNT(*) FROM products').fetchone()[0] + 1:03d}"
        
        cursor.execute('''
            INSERT INTO products (
                sku, name, description, category, price, stock,
                image_url, masonic_symbols, sizes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sku,
            data['name'],
            data.get('description'),
            data.get('category'),
            data['price'],
            data.get('stock', 0),
            data.get('image_url'),
            json.dumps(data.get('masonic_symbols', [])),
            json.dumps(data.get('sizes', [])),
            datetime.now().isoformat()
        ))
        
        db.conn.commit()
        product_id = cursor.lastrowid
        
        return jsonify({
            'success': True,
            'data': {'id': product_id, 'sku': sku, **data},
            'message': '? Produto criado!'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===================================================================
# CLIENTES
# ===================================================================

@app.route('/api/customers', methods=['GET'])
def list_customers():
    """Lista clientes"""
    try:
        filters = {}
        if request.args.get('is_mason'):
            filters['is_mason'] = request.args.get('is_mason') == 'true'
        
        customers = db.get_customers(filters)
        
        return jsonify({
            'success': True,
            'data': customers,
            'total': len(customers)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Cadastra cliente (com follow-up automático)"""
    try:
        data = request.json
        customer = db.create_customer(data)
        
        return jsonify({
            'success': True,
            'data': customer,
            'message': '? Cliente cadastrado! Follow-up automático agendado.'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===================================================================
# CAMPANHAS
# ===================================================================

@app.route('/api/campaigns', methods=['POST'])
def create_campaign():
    """Cria nova campanha"""
    try:
        data = request.json
        campaign_id = db.create_campaign(data)
        
        return jsonify({
            'success': True,
            'data': {'id': campaign_id},
            'message': '? Campanha criada!'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/send/<int:campaign_id>', methods=['POST'])
def send_campaign(campaign_id):
    """Envia campanha agora"""
    try:
        sent_count = db.send_campaign_emails(campaign_id)
        
        return jsonify({
            'success': True,
            'data': {'sent': sent_count},
            'message': f'? Campanha enviada! {sent_count} emails'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/process', methods=['POST'])
def process_campaigns():
    """Processa todas campanhas agendadas"""
    try:
        db.process_scheduled_campaigns()
        
        return jsonify({
            'success': True,
            'message': '? Campanhas processadas'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===================================================================
# CAMPANHAS RECORRENTES
# ===================================================================

@app.route('/api/campaigns/weekly', methods=['POST'])
def create_weekly():
    """Cria campanha semanal"""
    try:
        campaign_id = db.create_weekly_campaign()
        return jsonify({
            'success': True,
            'data': {'id': campaign_id},
            'message': '? Campanha semanal agendada!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaigns/monthly', methods=['POST'])
def create_monthly():
    """Cria campanha mensal"""
    try:
        campaign_id = db.create_monthly_campaign()
        return jsonify({
            'success': True,
            'data': {'id': campaign_id},
            'message': '? Campanha mensal agendada!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===================================================================
# ESTATÍSTICAS
# ===================================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Retorna estatísticas gerais"""
    try:
        stats = db.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===================================================================
# HEALTH CHECK
# ===================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'arkana-api-sqlite',
        'version': '2.0.0',
        'database': str(db.db_path),
        'timestamp': datetime.now().isoformat()
    })

# ===================================================================
# MAIN
# ===================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("?? ARKANA API (SQLite + Campanhas Automáticas)")
    print("="*70)
    print(f"?? Rodando em: http://localhost:5000")
    print(f"?? Database: {db.db_path}")
    print(f"\n?? Endpoints:")
    print(f"  GET  /api/customers")
    print(f"  POST /api/customers         ? Cadastra cliente + follow-up auto")
    print(f"  GET  /api/products")
    print(f"  POST /api/products")
    print(f"  POST /api/campaigns")
    print(f"  POST /api/campaigns/send/:id")
    print(f"  POST /api/campaigns/process ? Processa campanhas agendadas")
    print(f"  POST /api/campaigns/weekly  ? Cria semanal")
    print(f"  POST /api/campaigns/monthly ? Cria mensal")
    print(f"  GET  /api/stats")
    print(f"  GET  /health")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
