#!/usr/bin/env python3
"""
??? ARKANA STORE - SQLITE DATABASE + CAMPANHAS AUTOMÁTICAS
==========================================================

Sistema completo de cadastro de clientes + email marketing automatizado

Features:
- SQLite database (clientes, produtos, pedidos)
- Campanhas automáticas (diária, semanal, mensal)
- Follow-up 5 dias (automático)
- Segmentação de clientes (maçons vs não-maçons)
- Gravatar integration (avatares)
- Email templates (Avila Inc)

Data: 16/11/2025
Versão: 2.0.0
"""

import sqlite3
import json
import smtplib
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv('../../config/.env.arkana.production')

class ArkanaDatabase:
    """Gerenciador SQLite para Arkana Store"""
    
    def __init__(self, db_path: str = 'data/arkana_store.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Retornar dicts
        
        self.create_tables()
        print(f"? Database conectado: {self.db_path}")
    
    def create_tables(self):
        """Cria tabelas do banco"""
        
        cursor = self.conn.cursor()
        
        # TABELA: Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                
                -- Dados maçônicos (opcional)
                is_mason BOOLEAN DEFAULT 0,
                lodge_name TEXT,
                masonic_degree TEXT,
                
                -- Marketing
                accept_newsletter BOOLEAN DEFAULT 1,
                avatar_url TEXT,
                
                -- Métricas
                total_orders INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0.0,
                last_purchase_at TEXT,
                
                -- Timestamps
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        ''')
        
        # TABELA: Produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                image_url TEXT,
                masonic_symbols TEXT,  -- JSON array
                sizes TEXT,            -- JSON array
                active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        ''')
        
        # TABELA: Pedidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER NOT NULL,
                
                -- Items (JSON)
                items TEXT NOT NULL,  -- JSON array
                
                -- Valores
                subtotal REAL NOT NULL,
                shipping REAL DEFAULT 0.0,
                discount REAL DEFAULT 0.0,
                total REAL NOT NULL,
                
                -- Status
                status TEXT DEFAULT 'pending_payment',
                payment_gateway TEXT,
                payment_id TEXT,
                
                -- Timestamps
                created_at TEXT NOT NULL,
                paid_at TEXT,
                shipped_at TEXT,
                delivered_at TEXT,
                
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # TABELA: Campanhas de Email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_name TEXT NOT NULL,
                campaign_type TEXT,  -- weekly, monthly, followup, promo
                subject TEXT NOT NULL,
                template_name TEXT,
                
                -- Segmentação
                target_segment TEXT,  -- all, masons, inactive, new
                
                -- Métricas
                sent_count INTEGER DEFAULT 0,
                opened_count INTEGER DEFAULT 0,
                clicked_count INTEGER DEFAULT 0,
                
                -- Status
                status TEXT DEFAULT 'draft',
                scheduled_at TEXT,
                sent_at TEXT,
                
                created_at TEXT NOT NULL
            )
        ''')
        
        # TABELA: Email Logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                campaign_id INTEGER,
                
                subject TEXT NOT NULL,
                template_used TEXT,
                
                -- Tracking
                sent_at TEXT NOT NULL,
                opened_at TEXT,
                clicked_at TEXT,
                
                -- Status
                status TEXT DEFAULT 'sent',  -- sent, opened, clicked, bounced
                
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (campaign_id) REFERENCES email_campaigns (id)
            )
        ''')
        
        self.conn.commit()
        print("? Tabelas criadas: customers, products, orders, email_campaigns, email_logs")
    
    # ===================================================================
    # CLIENTES
    # ===================================================================
    
    def create_customer(self, data: Dict) -> Dict:
        """Cadastra novo cliente"""
        
        cursor = self.conn.cursor()
        
        # Gerar avatar Gravatar
        email_hash = hashlib.md5(data['email'].lower().encode()).hexdigest()
        avatar_url = f"https://www.gravatar.com/avatar/{email_hash}?s=200&d=mp"
        
        cursor.execute('''
            INSERT INTO customers (
                name, email, phone, cpf,
                is_mason, lodge_name, masonic_degree,
                accept_newsletter, avatar_url,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['phone'],
            data['cpf'],
            data.get('is_mason', False),
            data.get('lodge_name'),
            data.get('masonic_degree'),
            data.get('accept_newsletter', True),
            avatar_url,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        customer_id = cursor.lastrowid
        
        print(f"? Cliente cadastrado: {data['name']} (ID: {customer_id})")
        
        # Se aceitou newsletter, iniciar follow-up
        if data.get('accept_newsletter'):
            self.schedule_followup_sequence(customer_id, data['email'], data['name'])
        
        return {
            'id': customer_id,
            'avatar_url': avatar_url,
            **data
        }
    
    def get_customers(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Lista clientes com filtros opcionais"""
        
        cursor = self.conn.cursor()
        
        query = 'SELECT * FROM customers'
        params = []
        
        if filters:
            conditions = []
            if 'is_mason' in filters:
                conditions.append('is_mason = ?')
                params.append(filters['is_mason'])
            if 'accept_newsletter' in filters:
                conditions.append('accept_newsletter = ?')
                params.append(filters['accept_newsletter'])
            
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    # ===================================================================
    # CAMPANHAS DE EMAIL
    # ===================================================================
    
    def schedule_followup_sequence(self, customer_id: int, email: str, name: str):
        """Agenda sequência de follow-up automático (5 dias)"""
        
        cursor = self.conn.cursor()
        
        # Sequência de 5 dias
        sequence = [
            {
                'day': 1,
                'subject': '??? Bem-vindo à Arkana Store!',
                'template': 'followup',
                'type': 'followup'
            },
            {
                'day': 2,
                'subject': '? Viu minha mensagem anterior?',
                'template': 'followup',
                'type': 'followup'
            },
            {
                'day': 3,
                'subject': '?? Cupom Especial: IRMAO10 (10% OFF)',
                'template': 'promo_campaign',
                'type': 'followup'
            },
            {
                'day': 7,
                'subject': '?? Última Chance - Desconto expira hoje!',
                'template': 'promo_campaign',
                'type': 'followup'
            }
        ]
        
        for step in sequence:
            scheduled_at = (datetime.now() + timedelta(days=step['day'])).isoformat()
            
            cursor.execute('''
                INSERT INTO email_campaigns (
                    campaign_name, campaign_type, subject, template_name,
                    target_segment, status, scheduled_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"Follow-up D+{step['day']} - {name}",
                step['type'],
                step['subject'],
                step['template'],
                f"customer_id:{customer_id}",
                'scheduled',
                scheduled_at,
                datetime.now().isoformat()
            ))
        
        self.conn.commit()
        print(f"? Follow-up agendado: {len(sequence)} emails para {name}")
    
    def create_campaign(self, campaign_data: Dict) -> int:
        """Cria nova campanha de email"""
        
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO email_campaigns (
                campaign_name, campaign_type, subject, template_name,
                target_segment, status, scheduled_at, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            campaign_data['name'],
            campaign_data.get('type', 'manual'),
            campaign_data['subject'],
            campaign_data.get('template', 'newsletter'),
            campaign_data.get('segment', 'all'),
            campaign_data.get('status', 'draft'),
            campaign_data.get('scheduled_at'),
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        campaign_id = cursor.lastrowid
        
        print(f"? Campanha criada: {campaign_data['name']} (ID: {campaign_id})")
        return campaign_id
    
    def get_campaigns_to_send(self) -> List[Dict]:
        """Busca campanhas agendadas para enviar AGORA"""
        
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute('''
            SELECT * FROM email_campaigns
            WHERE status = 'scheduled'
            AND scheduled_at <= ?
            ORDER BY scheduled_at ASC
        ''', (now,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ===================================================================
    # CAMPANHAS RECORRENTES
    # ===================================================================
    
    def create_weekly_campaign(self):
        """Cria campanha semanal automática (toda Segunda 10h)"""
        
        next_monday = datetime.now()
        days_ahead = 0 - next_monday.weekday()  # Segunda = 0
        if days_ahead <= 0:
            days_ahead += 7
        next_monday = next_monday + timedelta(days=days_ahead)
        next_monday = next_monday.replace(hour=10, minute=0, second=0)
        
        campaign_id = self.create_campaign({
            'name': f'Newsletter Semanal - {next_monday.strftime("%d/%m")}',
            'type': 'weekly',
            'subject': '??? Novidades da Semana - Arkana Store',
            'template': 'newsletter',
            'segment': 'accept_newsletter:true',
            'status': 'scheduled',
            'scheduled_at': next_monday.isoformat()
        })
        
        print(f"? Campanha semanal agendada para: {next_monday.strftime('%d/%m/%Y %H:%M')}")
        return campaign_id
    
    def create_monthly_campaign(self):
        """Cria campanha mensal (dia 1 de cada mês, 9h)"""
        
        next_month = datetime.now().replace(day=1, hour=9, minute=0, second=0)
        if next_month <= datetime.now():
            # Próximo mês
            if next_month.month == 12:
                next_month = next_month.replace(year=next_month.year + 1, month=1)
            else:
                next_month = next_month.replace(month=next_month.month + 1)
        
        campaign_id = self.create_campaign({
            'name': f'Newsletter Mensal - {next_month.strftime("%B/%Y")}',
            'type': 'monthly',
            'subject': '?? Novidades do Mês - Produtos Maçônicos',
            'template': 'newsletter',
            'segment': 'all',
            'status': 'scheduled',
            'scheduled_at': next_month.isoformat()
        })
        
        print(f"? Campanha mensal agendada para: {next_month.strftime('%d/%m/%Y')}")
        return campaign_id
    
    # ===================================================================
    # ENVIO DE EMAILS
    # ===================================================================
    
    def send_campaign_emails(self, campaign_id: int):
        """Envia emails de uma campanha"""
        
        cursor = self.conn.cursor()
        
        # Buscar campanha
        cursor.execute('SELECT * FROM email_campaigns WHERE id = ?', (campaign_id,))
        campaign = dict(cursor.fetchone())
        
        # Buscar destinatários baseado no segmento
        recipients = self.get_campaign_recipients(campaign['target_segment'])
        
        print(f"?? Enviando campanha: {campaign['campaign_name']}")
        print(f"?? Destinatários: {len(recipients)}")
        
        sent_count = 0
        
        for customer in recipients:
            try:
                # Enviar email
                success = self.send_email(
                    to_email=customer['email'],
                    to_name=customer['name'],
                    subject=campaign['subject'],
                    template_name=campaign['template_name']
                )
                
                if success:
                    sent_count += 1
                    
                    # Registrar log
                    cursor.execute('''
                        INSERT INTO email_logs (
                            customer_id, campaign_id, subject, template_used,
                            sent_at, status
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        customer['id'],
                        campaign_id,
                        campaign['subject'],
                        campaign['template_name'],
                        datetime.now().isoformat(),
                        'sent'
                    ))
                
            except Exception as e:
                print(f"  ? Erro ao enviar para {customer['email']}: {e}")
        
        # Atualizar campanha
        cursor.execute('''
            UPDATE email_campaigns
            SET sent_count = ?, status = 'sent', sent_at = ?
            WHERE id = ?
        ''', (sent_count, datetime.now().isoformat(), campaign_id))
        
        self.conn.commit()
        
        print(f"? Campanha enviada: {sent_count}/{len(recipients)} sucesso")
        return sent_count
    
    def get_campaign_recipients(self, segment: str) -> List[Dict]:
        """Busca destinatários baseado no segmento"""
        
        cursor = self.conn.cursor()
        
        # Parsear segmento
        if segment == 'all':
            query = 'SELECT * FROM customers WHERE accept_newsletter = 1'
            cursor.execute(query)
        
        elif segment.startswith('customer_id:'):
            # Seguimento específico (follow-up)
            customer_id = int(segment.split(':')[1])
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        
        elif segment == 'is_mason:true':
            cursor.execute('SELECT * FROM customers WHERE is_mason = 1 AND accept_newsletter = 1')
        
        elif segment == 'accept_newsletter:true':
            cursor.execute('SELECT * FROM customers WHERE accept_newsletter = 1')
        
        else:
            # Default: todos que aceitaram newsletter
            cursor.execute('SELECT * FROM customers WHERE accept_newsletter = 1')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def send_email(self, to_email: str, to_name: str, subject: str, template_name: str) -> bool:
        """Envia email individual"""
        
        try:
            # Carregar template
            template = self.load_email_template(template_name)
            
            # Personalizar
            html_content = template.replace('{{NAME}}', to_name)
            html_content = html_content.replace('{{EMAIL}}', to_email)
            
            # Configurar SMTP
            smtp_host = os.getenv('SMTP_HOST', 'smtp.porkbun.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            smtp_user = os.getenv('SMTP_USER', 'dev@avila.inc')
            smtp_pass = os.getenv('SMTP_PASSWORD', '')
            from_email = os.getenv('FROM_EMAIL', 'dev@avila.inc')
            from_name = os.getenv('FROM_NAME', 'Arkana Store')
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f'{from_name} <{from_email}>'
            msg['To'] = to_email
            
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                if smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            print(f"  ? Email enviado: {to_email}")
            return True
            
        except Exception as e:
            print(f"  ? Falha email: {to_email} - {e}")
            return False
    
    def load_email_template(self, template_name: str) -> str:
        """Carrega template de email do Avila Inc"""
        
        # Buscar em Marketing Avila Inc
        avila_marketing = Path(r'C:\Users\nicol\OneDrive\Avila\1.1 - Avilainc\Marketing')
        template_path = avila_marketing / f'{template_name}.html'
        
        if template_path.exists():
            return template_path.read_text(encoding='utf-8')
        
        # Fallback: template inline
        return '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; }
        .header { background: linear-gradient(135deg, #1a237e, #283593); color: white; padding: 40px 20px; text-align: center; }
        .body { padding: 40px 20px; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #666; }
        .btn { display: inline-block; padding: 15px 30px; background: #ffd700; color: #1a1a1a; text-decoration: none; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>??? ARKANA STORE</h1>
            <p>Produtos Maçônicos de Qualidade</p>
        </div>
        <div class="body">
            <h2>Olá {{NAME}}!</h2>
            <p>Confira nossas novidades e ofertas exclusivas.</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="https://arkanastore.com.br" class="btn">??? Ver Produtos</a>
            </p>
        </div>
        <div class="footer">
            <p>Arkana Store - Produtos Maçônicos</p>
            <p>marceloquintinoalves25@gmail.com | (17) 99665-6163</p>
            <p><a href="mailto:{{EMAIL}}">Cancelar inscrição</a></p>
        </div>
    </div>
</body>
</html>
        '''
    
    # ===================================================================
    # CRON / SCHEDULER
    # ===================================================================
    
    def process_scheduled_campaigns(self):
        """Processa campanhas agendadas (rodar via CRON)"""
        
        campaigns = self.get_campaigns_to_send()
        
        print(f"\n?? Verificando campanhas agendadas...")
        print(f"?? {len(campaigns)} campanha(s) para enviar")
        
        for campaign in campaigns:
            print(f"\n?? Processando: {campaign['campaign_name']}")
            self.send_campaign_emails(campaign['id'])
        
        if len(campaigns) == 0:
            print("? Nenhuma campanha agendada no momento")
    
    # ===================================================================
    # MÉTRICAS
    # ===================================================================
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas gerais"""
        
        cursor = self.conn.cursor()
        
        # Clientes
        cursor.execute('SELECT COUNT(*) as total FROM customers')
        total_customers = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM customers WHERE is_mason = 1')
        mason_customers = cursor.fetchone()['total']
        
        # Pedidos
        cursor.execute('SELECT COUNT(*) as total, SUM(total) as revenue FROM orders')
        orders_stats = dict(cursor.fetchone())
        
        # Emails
        cursor.execute('SELECT COUNT(*) as total FROM email_logs')
        total_emails = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM email_logs WHERE opened_at IS NOT NULL')
        opened_emails = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as total FROM email_logs WHERE clicked_at IS NOT NULL')
        clicked_emails = cursor.fetchone()['total']
        
        return {
            'customers': {
                'total': total_customers,
                'masons': mason_customers,
                'non_masons': total_customers - mason_customers
            },
            'orders': {
                'total': orders_stats['total'] or 0,
                'revenue': orders_stats['revenue'] or 0.0
            },
            'email_marketing': {
                'sent': total_emails,
                'opened': opened_emails,
                'clicked': clicked_emails,
                'open_rate': (opened_emails / total_emails * 100) if total_emails > 0 else 0,
                'click_rate': (clicked_emails / total_emails * 100) if total_emails > 0 else 0
            }
        }
    
    def close(self):
        """Fecha conexão"""
        self.conn.close()


# ===================================================================
# EXEMPLO DE USO
# ===================================================================

if __name__ == '__main__':
    db = ArkanaDatabase()
    
    print("\n" + "="*70)
    print("??? ARKANA SQLITE + CAMPANHAS - DEMO")
    print("="*70)
    
    # 1. Cadastrar cliente
    print("\n?? CADASTRANDO CLIENTE:")
    cliente = db.create_customer({
        'name': 'Marcelo Quintino',
        'email': 'marceloquintinoalves25@gmail.com',
        'phone': '(17) 99665-6163',
        'cpf': '123.456.789-00',
        'is_mason': True,
        'lodge_name': 'Loja Harmonia Universal',
        'masonic_degree': 'Mestre',
        'accept_newsletter': True
    })
    
    print(f"  ? ID: {cliente['id']}")
    print(f"  ? Avatar: {cliente['avatar_url']}")
    
    # 2. Criar campanhas recorrentes
    print("\n?? CRIANDO CAMPANHAS RECORRENTES:")
    db.create_weekly_campaign()
    db.create_monthly_campaign()
    
    # 3. Processar campanhas agendadas
    print("\n?? PROCESSANDO CAMPANHAS:")
    db.process_scheduled_campaigns()
    
    # 4. Estatísticas
    print("\n?? ESTATÍSTICAS:")
    stats = db.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n? Demo concluída!")
    print(f"?? Database: {db.db_path}")
    
    db.close()
