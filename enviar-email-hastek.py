"""
Script para enviar email de boas-vindas ao projeto Arkana Store
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def enviar_email_hastek():
    """Envia email HTML de boas-vindas ao colaborador hastek-nex"""
    
    # Configurações SMTP
    smtp_host = os.getenv('SMTP_HOST', 'mail.avila.inc')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER', 'noreply@avila.inc')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    # Dados do email
    remetente = 'dev@avila.inc'
    destinatario = input("Digite o email do hastek-nex: ")
    assunto = '🏪 Bem-vindo ao Arkana Store - Colaborador Adicionado'
    
    # Ler HTML
    html_path = Path(__file__).parent / 'email-hastek-nex.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Criar mensagem
    msg = MIMEMultipart('alternative')
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    
    # Anexar HTML
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)
    
    # Texto alternativo (fallback)
    texto_alternativo = """
    Olá!
    
    Você foi adicionado como colaborador do repositório ArkanaStore.
    
    Repositório: https://github.com/avilaops/ArkanaStore
    Demo Live: https://avilaops.github.io/ArkanaStore/
    
    Quick Start:
    1. git clone https://github.com/avilaops/ArkanaStore.git
    2. cd ArkanaStore
    3. cp .env.example .env
    4. docker-compose -f docker-compose.avila-full.yml up -d
    
    Stack:
    - Frontend: Yew (Rust WASM)
    - Backend: Actix-web (Rust)
    - Database: MongoDB 7.0
    - Cache: Redis 7
    - Storage: MinIO
    - Monitoring: Prometheus + Grafana + Loki
    
    Dúvidas? Entre em contato:
    - Email: dev@avila.inc
    - WhatsApp: (17) 99781-1471
    
    Ávila Inc
    """
    texto_part = MIMEText(texto_alternativo, 'plain', 'utf-8')
    msg.attach(texto_part)
    
    try:
        # Conectar e enviar
        print(f"📧 Conectando ao servidor SMTP {smtp_host}:{smtp_port}...")
        
        if smtp_password:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                print(f"✅ Email enviado com sucesso para {destinatario}!")
        else:
            print("⚠️ SMTP_PASSWORD não configurado no .env")
            print("📄 HTML gerado em: email-hastek-nex.html")
            print(f"📬 Envie manualmente para: {destinatario}")
            
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        print("📄 HTML disponível em: email-hastek-nex.html")
        print("📬 Você pode copiar o conteúdo e enviar manualmente")

if __name__ == "__main__":
    print("=" * 60)
    print("🏪 ARKANA STORE - CONVITE COLABORADOR")
    print("=" * 60)
    print()
    enviar_email_hastek()
    print()
    print("=" * 60)
