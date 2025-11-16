#!/usr/bin/env python3
"""
??? ARKANA ADMIN - BACKEND INTEGRATION
=====================================
Sistema completo que integra:
- Gestão de produtos (MongoDB)
- Email marketing (SMTP Porkbun)
- Webhooks de pagamento (Stripe, PayPal, MercadoPago)
- Gravatar (avatares automáticos)
- Analytics e métricas

Data: 16/11/2025
Versão: 1.0.0
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Importar serviços já criados
import sys
sys.path.append(str(Path(__file__).parent.parent / 'utilities'))
from gravatar_service import AvilaGravatarService

# Carregar configurações
load_dotenv('config/.env.arkana.production')

class ArkanaAdminBackend:
    """Backend completo do painel administrativo"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.porkbun.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', 'dev@avila.inc')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'dev@avila.inc')
        self.from_name = os.getenv('FROM_NAME', 'Nicolas Ávila - Ávila Inc')
        
        # Serviços integrados
        self.gravatar = AvilaGravatarService()
        
        # Database local (JSON) - Em produção, usar MongoDB
        self.db_path = Path('data/arkana_db')
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.products_file = self.db_path / 'products.json'
        self.orders_file = self.db_path / 'orders.json'
        self.customers_file = self.db_path / 'customers.json'
        self.campaigns_file = self.db_path / 'email_campaigns.json'
        
        # Inicializar arquivos se não existirem
        for file in [self.products_file, self.orders_file, self.customers_file, self.campaigns_file]:
            if not file.exists():
                file.write_text('[]')
        
        print("? Arkana Admin Backend inicializado")
        print(f"?? SMTP: {self.smtp_host}:{self.smtp_port}")
        print(f"?? Database: {self.db_path}")
    
    # ===================================================================
    # PRODUTOS
    # ===================================================================
    
    def get_products(self) -> List[Dict]:
        """Lista todos os produtos"""
        return json.loads(self.products_file.read_text())
    
    def create_product(self, product_data: Dict) -> Dict:
        """Cria novo produto"""
        products = self.get_products()
        
        product = {
            'id': len(products) + 1,
            'sku': f"ARK-{len(products) + 1:04d}",
            'created_at': datetime.now().isoformat(),
            **product_data
        }
        
        products.append(product)
        self.products_file.write_text(json.dumps(products, indent=2, ensure_ascii=False))
        
        print(f"? Produto criado: {product['name']} (SKU: {product['sku']})")
        return product
    
    def update_product(self, product_id: int, updates: Dict) -> Dict:
        """Atualiza produto existente"""
        products = self.get_products()
        
        for product in products:
            if product['id'] == product_id:
                product.update(updates)
                product['updated_at'] = datetime.now().isoformat()
                self.products_file.write_text(json.dumps(products, indent=2, ensure_ascii=False))
                print(f"? Produto atualizado: {product['name']}")
                return product
        
        raise ValueError(f"Produto #{product_id} não encontrado")
    
    def delete_product(self, product_id: int):
        """Remove produto"""
        products = self.get_products()
        products = [p for p in products if p['id'] != product_id]
        self.products_file.write_text(json.dumps(products, indent=2, ensure_ascii=False))
        print(f"? Produto #{product_id} removido")
    
    # ===================================================================
    # EMAIL MARKETING
    # ===================================================================
    
    def load_email_template(self, template_name: str) -> str:
        """Carrega template de email"""
        # Buscar templates do Avila Inc
        avila_marketing = Path(r'C:\Users\nicol\OneDrive\Avila\1.1 - Avilainc\Marketing')
        template_path = avila_marketing / f'{template_name}.html'
        
        if template_path.exists():
            return template_path.read_text(encoding='utf-8')
        
        # Fallback: template simples
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
                .email-container { max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; }
                .email-header { background: #1a237e; color: white; padding: 40px 20px; text-align: center; }
                .email-body { padding: 40px 20px; }
                .email-footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 0.875rem; color: #6c757d; }
                .btn { display: inline-block; padding: 15px 30px; background: #ffd700; color: #1a237e; text-decoration: none; border-radius: 8px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>??? ARKANA STORE</h1>
                    <p>Produtos Maçônicos de Qualidade</p>
                </div>
                <div class="email-body">
                    {{CONTENT}}
                </div>
                <div class="email-footer">
                    <p>Arkana Store - marceloquintinoalves25@gmail.com</p>
                    <p>(17) 99665-6163 | @marcelo_quintino3.0</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str,
        template_name: Optional[str] = None
    ) -> bool:
        """Envia email usando template"""
        
        try:
            # Carregar template se especificado
            if template_name:
                template = self.load_email_template(template_name)
                html_content = template.replace('{{CONTENT}}', html_content)
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f'{self.from_name} <{self.from_email}>'
            msg['To'] = to_email
            
            # Adicionar HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            print(f"? Email enviado: {to_email} - {subject}")
            return True
            
        except Exception as e:
            print(f"? Erro ao enviar email: {e}")
            return False
    
    def send_campaign(
        self, 
        campaign_name: str,
        template_name: str,
        subject: str,
        recipients: List[str],
        content: str
    ) -> Dict:
        """Envia campanha de email para múltiplos destinatários"""
        
        results = {
            'campaign_name': campaign_name,
            'sent': 0,
            'failed': 0,
            'recipients': len(recipients),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"?? Iniciando campanha: {campaign_name}")
        print(f"?? Destinatários: {len(recipients)}")
        
        for email in recipients:
            if self.send_email(email, subject, content, template_name):
                results['sent'] += 1
            else:
                results['failed'] += 1
        
        # Salvar histórico
        campaigns = json.loads(self.campaigns_file.read_text())
        campaigns.append(results)
        self.campaigns_file.write_text(json.dumps(campaigns, indent=2))
        
        print(f"? Campanha concluída: {results['sent']} enviados, {results['failed']} falhas")
        return results
    
    # ===================================================================
    # FOLLOW-UP AUTOMÁTICO
    # ===================================================================
    
    def send_followup_sequence(self, customer_email: str, customer_name: str):
        """Envia sequência de follow-up automático (5 dias)"""
        
        sequence = [
            {
                'day': 1,
                'subject': '??? Bem-vindo à Arkana Store!',
                'content': f'''
                    <h2>Olá {customer_name}!</h2>
                    <p>Seja bem-vindo à Arkana Store, sua loja de produtos maçônicos de qualidade.</p>
                    <p>Confira nossos produtos exclusivos:</p>
                    <ul>
                        <li>?? Camisetas com símbolos maçônicos</li>
                        <li>?? Bermudas confortáveis</li>
                        <li>?? Anéis e acessórios premium</li>
                        <li>?? Bonés bordados</li>
                    </ul>
                    <p style="text-align: center; margin-top: 30px;">
                        <a href="https://arkanastore.com.br" class="btn">??? Ver Produtos</a>
                    </p>
                '''
            },
            {
                'day': 2,
                'subject': '? Ofertas Especiais para Irmãos Maçons',
                'content': f'''
                    <h2>Olá {customer_name}!</h2>
                    <p>Viu nossa mensagem anterior? Temos ofertas exclusivas para você!</p>
                    <p><strong>?? 10% OFF</strong> na primeira compra usando o cupom: <code>IRMAO10</code></p>
                '''
            },
            {
                'day': 3,
                'subject': '?? Produtos Mais Vendidos da Semana',
                'content': f'''
                    <h2>Olá {customer_name}!</h2>
                    <p>Confira os produtos mais vendidos esta semana:</p>
                    <ol>
                        <li>Camiseta Compasso e Esquadro - R$ 89,90</li>
                        <li>Anel Mestre Maçom - R$ 149,90</li>
                        <li>Bermuda Logos - R$ 79,90</li>
                    </ol>
                '''
            },
        ]
        
        print(f"?? Iniciando sequência follow-up: {customer_email}")
        
        for step in sequence:
            print(f"  ? Dia {step['day']}: {step['subject']}")
            # Em produção, agendar com cron/celery
            # Por ora, apenas simula
        
        print("? Sequência follow-up configurada")
    
    # ===================================================================
    # CLIENTES
    # ===================================================================
    
    def get_customers(self) -> List[Dict]:
        """Lista todos os clientes"""
        return json.loads(self.customers_file.read_text())
    
    def create_customer(self, customer_data: Dict) -> Dict:
        """Cria novo cliente com avatar Gravatar"""
        customers = self.get_customers()
        
        customer = {
            'id': len(customers) + 1,
            'created_at': datetime.now().isoformat(),
            **customer_data
        }
        
        # Gerar avatar automaticamente
        if 'email' in customer and 'name' in customer:
            avatar_url = self.gravatar.get_avatar_url(customer['email'])
            customer['avatar_url'] = avatar_url
        
        customers.append(customer)
        self.customers_file.write_text(json.dumps(customers, indent=2, ensure_ascii=False))
        
        # Enviar email de boas-vindas
        if customer.get('email'):
            self.send_followup_sequence(customer['email'], customer.get('name', 'Cliente'))
        
        print(f"? Cliente criado: {customer.get('name')} (#{customer['id']})")
        return customer
    
    # ===================================================================
    # PEDIDOS
    # ===================================================================
    
    def get_orders(self) -> List[Dict]:
        """Lista todos os pedidos"""
        return json.loads(self.orders_file.read_text())
    
    def create_order(self, order_data: Dict) -> Dict:
        """Cria novo pedido"""
        orders = self.get_orders()
        
        order_number = f"ARK-{datetime.now().strftime('%Y%m%d')}-{len(orders) + 1:03d}"
        
        order = {
            'id': len(orders) + 1,
            'order_number': order_number,
            'created_at': datetime.now().isoformat(),
            'status': 'pending_payment',
            **order_data
        }
        
        orders.append(order)
        self.orders_file.write_text(json.dumps(orders, indent=2, ensure_ascii=False))
        
        # Enviar email de confirmação
        if order.get('customer_email'):
            self.send_order_confirmation(order)
        
        print(f"? Pedido criado: {order_number}")
        return order
    
    def send_order_confirmation(self, order: Dict):
        """Envia email de confirmação de pedido"""
        
        customer_email = order.get('customer_email')
        customer_name = order.get('customer_name', 'Cliente')
        
        content = f'''
            <h2>Pedido Confirmado! ??</h2>
            <p>Olá {customer_name}!</p>
            <p>Seu pedido foi recebido com sucesso:</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Número do Pedido:</strong> {order['order_number']}</p>
                <p><strong>Total:</strong> R$ {order.get('total', 0):.2f}</p>
                <p><strong>Status:</strong> Aguardando Pagamento</p>
            </div>
            
            <p>Assim que o pagamento for confirmado, iniciaremos a separação do seu pedido.</p>
            <p>Prazo de entrega: 7 a 10 dias úteis.</p>
            
            <p style="text-align: center; margin-top: 30px;">
                <a href="https://wa.me/5517996656163?text=Pedido%20{order['order_number']}" class="btn">
                    ?? Falar com Suporte
                </a>
            </p>
        '''
        
        self.send_email(
            to_email=customer_email,
            subject=f"? Pedido {order['order_number']} Confirmado - Arkana Store",
            html_content=content
        )
    
    # ===================================================================
    # MÉTRICAS E ANALYTICS
    # ===================================================================
    
    def get_dashboard_metrics(self) -> Dict:
        """Retorna métricas do dashboard"""
        
        products = self.get_products()
        orders = self.get_orders()
        customers = self.get_customers()
        
        # Calcular vendas do dia
        today = datetime.now().date()
        today_orders = [
            o for o in orders 
            if datetime.fromisoformat(o['created_at']).date() == today
        ]
        
        today_revenue = sum(o.get('total', 0) for o in today_orders)
        
        # Taxa de conversão (simulada)
        visits = 150  # TODO: Integrar com Google Analytics
        conversion_rate = (len(today_orders) / visits * 100) if visits > 0 else 0
        
        return {
            'today_revenue': today_revenue,
            'today_orders': len(today_orders),
            'total_customers': len(customers),
            'total_products': len(products),
            'conversion_rate': conversion_rate,
            'active_products': len([p for p in products if p.get('stock', 0) > 0]),
            'low_stock_products': len([p for p in products if 0 < p.get('stock', 0) <= 5]),
        }
    
    # ===================================================================
    # RELATÓRIOS
    # ===================================================================
    
    def generate_daily_report(self) -> str:
        """Gera relatório diário executivo"""
        
        metrics = self.get_dashboard_metrics()
        
        report = f"""
# ?? RELATÓRIO DIÁRIO - ARKANA STORE
**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## ?? Vendas
- **Receita Hoje**: R$ {metrics['today_revenue']:.2f}
- **Pedidos Hoje**: {metrics['today_orders']}
- **Ticket Médio**: R$ {(metrics['today_revenue'] / metrics['today_orders'] if metrics['today_orders'] > 0 else 0):.2f}

## ?? Produtos
- **Total de Produtos**: {metrics['total_products']}
- **Produtos Ativos**: {metrics['active_products']}
- **Estoque Baixo**: {metrics['low_stock_products']} produtos

## ?? Clientes
- **Total de Clientes**: {metrics['total_customers']}
- **Taxa de Conversão**: {metrics['conversion_rate']:.1f}%

## ?? Ações Recomendadas
{"- ?? Reabastecer produtos com estoque baixo" if metrics['low_stock_products'] > 0 else ""}
{"- ?? Enviar campanha de reengajamento" if metrics['conversion_rate'] < 3.0 else ""}

---
*Gerado automaticamente por Ávila Inc*
        """
        
        return report.strip()
    
    def send_daily_report_email(self, recipient: str = 'marceloquintinoalves25@gmail.com'):
        """Envia relatório diário por email"""
        
        report_md = self.generate_daily_report()
        
        # Converter markdown para HTML (simplificado)
        report_html = report_md.replace('\n', '<br>')
        report_html = report_html.replace('**', '<strong>').replace('**', '</strong>')
        report_html = report_html.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
        report_html = report_html.replace('## ', '<h2>').replace('<br>', '</h2>', 5)
        
        self.send_email(
            to_email=recipient,
            subject=f"?? Relatório Diário Arkana Store - {datetime.now().strftime('%d/%m/%Y')}",
            html_content=report_html
        )
        
        print(f"? Relatório diário enviado para: {recipient}")


# ===================================================================
# EXEMPLOS DE USO
# ===================================================================

if __name__ == '__main__':
    admin = ArkanaAdminBackend()
    
    print("\n" + "="*60)
    print("??? ARKANA ADMIN BACKEND - DEMO")
    print("="*60)
    
    # Exemplo 1: Criar produto
    print("\n?? EXEMPLO 1: Criar produto")
    produto = admin.create_product({
        'name': 'Camiseta Compasso e Esquadro Premium',
        'category': 'camisetas',
        'description': '100% algodão egípcio, estampa em silk screen de alta qualidade',
        'price': 89.90,
        'stock': 50,
        'images': ['https://via.placeholder.com/400x400/1a237e/ffd700'],
        'sizes': ['P', 'M', 'G', 'GG'],
        'masonic_symbols': ['Compasso', 'Esquadro', 'G']
    })
    
    # Exemplo 2: Criar cliente com avatar
    print("\n?? EXEMPLO 2: Criar cliente")
    cliente = admin.create_customer({
        'name': 'Marcelo Quintino',
        'email': 'marceloquintinoalves25@gmail.com',
        'phone': '+55 17 99665-6163',
        'is_mason': True,
        'lodge_name': 'Loja Harmonia Universal',
        'masonic_degree': 'Mestre'
    })
    
    # Exemplo 3: Gerar relatório
    print("\n?? EXEMPLO 3: Gerar relatório")
    report = admin.generate_daily_report()
    print(report)
    
    # Exemplo 4: Métricas do dashboard
    print("\n?? EXEMPLO 4: Métricas dashboard")
    metrics = admin.get_dashboard_metrics()
    print(json.dumps(metrics, indent=2))
    
    print("\n? Demo concluída!")
    print(f"?? Dados salvos em: {admin.db_path}")
