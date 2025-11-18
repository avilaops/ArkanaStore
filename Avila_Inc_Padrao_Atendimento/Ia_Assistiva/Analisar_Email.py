"""
Script de Análise de Emails - Ávila Inc
Extensão do sistema de atendimento para processar emails

Funcionalidades:
1. Leitura de emails (IMAP/Outlook/Gmail)
2. Análise de conversas por thread
3. Classificação segundo diretrizes Ávila Inc
4. Integração com dossiês de clientes
"""

import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from pathlib import Path
import json
import re


class AnalisadorEmailsAvila:
    """
    Analisa emails de atendimento segundo diretrizes Ávila Inc
    Integra com o sistema de dossiês e padrão de atendimento
    """
    
    def __init__(self, servidor_email=None, usuario=None, senha=None):
        """
        Inicializa analisador de emails
        
        Args:
            servidor_email: IMAP server (ex: imap.gmail.com)
            usuario: Email da conta
            senha: Senha ou app password
        """
        self.servidor = servidor_email
        self.usuario = usuario
        self.senha = senha
        self.conexao = None
        self.emails_analisados = []
        self.analise = {}
        
    def conectar_imap(self):
        """Conecta ao servidor IMAP"""
        if not all([self.servidor, self.usuario, self.senha]):
            print("⚠️  Credenciais de email não fornecidas")
            print("   Use modo manual: analisar_email_arquivo()")
            return False
        
        try:
            print(f"📧 Conectando a {self.servidor}...")
            self.conexao = imaplib.IMAP4_SSL(self.servidor)
            self.conexao.login(self.usuario, self.senha)
            print("✅ Conectado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def buscar_emails(self, pasta="INBOX", filtro="UNSEEN", limite=50):
        """
        Busca emails na caixa de entrada
        
        Args:
            pasta: Pasta IMAP (INBOX, Sent, etc.)
            filtro: Filtro IMAP (UNSEEN, ALL, FROM "email", etc.)
            limite: Máximo de emails para processar
        """
        if not self.conexao:
            if not self.conectar_imap():
                return []
        
        try:
            self.conexao.select(pasta)
            status, mensagens = self.conexao.search(None, filtro)
            
            if status != "OK":
                print(f"❌ Erro ao buscar emails: {status}")
                return []
            
            ids_emails = mensagens[0].split()
            total = len(ids_emails)
            
            print(f"✅ Encontrados {total} emails")
            
            if total > limite:
                print(f"⚠️  Processando apenas os {limite} mais recentes")
                ids_emails = ids_emails[-limite:]
            
            return ids_emails
        
        except Exception as e:
            print(f"❌ Erro ao buscar: {e}")
            return []
    
    def processar_email(self, email_id):
        """Processa um email individual"""
        try:
            status, dados = self.conexao.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                return None
            
            mensagem_raw = dados[0][1]
            mensagem = email.message_from_bytes(mensagem_raw)
            
            # Extrair informações
            de = self._decodificar_header(mensagem.get("From"))
            para = self._decodificar_header(mensagem.get("To"))
            assunto = self._decodificar_header(mensagem.get("Subject"))
            data = mensagem.get("Date")
            
            # Extrair corpo
            corpo = self._extrair_corpo(mensagem)
            
            email_info = {
                'id': email_id.decode(),
                'de': de,
                'para': para,
                'assunto': assunto,
                'data': data,
                'corpo': corpo,
                'timestamp': datetime.now().isoformat()
            }
            
            return email_info
        
        except Exception as e:
            print(f"❌ Erro ao processar email {email_id}: {e}")
            return None
    
    def _decodificar_header(self, header):
        """Decodifica header de email"""
        if not header:
            return ""
        
        decoded = decode_header(header)
        resultado = ""
        
        for texto, encoding in decoded:
            if isinstance(texto, bytes):
                try:
                    resultado += texto.decode(encoding or 'utf-8')
                except:
                    resultado += texto.decode('utf-8', errors='ignore')
            else:
                resultado += str(texto)
        
        return resultado
    
    def _extrair_corpo(self, mensagem):
        """Extrai corpo do email (texto plano preferencialmente)"""
        corpo = ""
        
        if mensagem.is_multipart():
            for parte in mensagem.walk():
                content_type = parte.get_content_type()
                
                if content_type == "text/plain":
                    try:
                        corpo = parte.get_payload(decode=True).decode()
                        break
                    except:
                        continue
                elif content_type == "text/html" and not corpo:
                    try:
                        corpo = parte.get_payload(decode=True).decode()
                        corpo = self._html_para_texto(corpo)
                    except:
                        continue
        else:
            try:
                corpo = mensagem.get_payload(decode=True).decode()
            except:
                corpo = str(mensagem.get_payload())
        
        return corpo.strip()
    
    def _html_para_texto(self, html):
        """Converte HTML básico para texto (simples)"""
        # Remove tags HTML básicas
        texto = re.sub(r'<br\s*/?>', '\n', html)
        texto = re.sub(r'<[^>]+>', '', texto)
        texto = re.sub(r'&nbsp;', ' ', texto)
        texto = re.sub(r'&lt;', '<', texto)
        texto = re.sub(r'&gt;', '>', texto)
        texto = re.sub(r'&amp;', '&', texto)
        return texto
    
    def analisar_segundo_diretrizes_avila(self):
        """
        Analisa emails segundo filosofia Ávila Inc
        Mesmo padrão do analisador WhatsApp
        """
        print(f"\n{'='*60}")
        print("ANÁLISE SEGUNDO DIRETRIZES ÁVILA INC")
        print(f"{'='*60}\n")
        
        # Concatenar todos os emails
        texto_completo = "\n\n---\n\n".join([
            f"De: {e['de']}\nPara: {e['para']}\nAssunto: {e['assunto']}\nData: {e['data']}\n\n{e['corpo']}"
            for e in self.emails_analisados
        ])
        
        # 1. IDENTIFICAÇÃO DE CONTEXTO
        self.analise['contexto'] = self._identificar_contexto(texto_completo)
        
        # 2. CLASSIFICAÇÃO
        self.analise['classificacao'] = self._classificar_demanda(texto_completo, self.emails_analisados)
        
        # 3. QUALIDADE DE ATENDIMENTO
        self.analise['qualidade_atendimento'] = self._avaliar_atendimento(texto_completo, self.emails_analisados)
        
        # 4. PRIVACIDADE
        self.analise['privacidade'] = self._verificar_privacidade(texto_completo)
        
        # 5. THREAD/CONVERSAÇÃO
        self.analise['thread'] = self._analisar_thread(self.emails_analisados)
        
        # 6. PRÓXIMOS PASSOS
        self.analise['proximos_passos'] = self._gerar_proximos_passos()
        
        print("✅ Análise concluída\n")
    
    def _identificar_contexto(self, texto):
        """Identifica contexto do email"""
        contexto = {
            'tipo': 'indefinido',
            'resumo': '',
            'palavras_chave': [],
            'urgente': False
        }
        
        # Keywords
        keywords_custo = ['custo', 'redução', 'economia', 'despesa', 'gasto', 'caro']
        keywords_receita = ['receita', 'faturamento', 'vendas', 'lucro', 'margem', 'vender']
        keywords_operacao = ['processo', 'operação', 'sistema', 'automação', 'eficiência']
        keywords_urgente = ['urgente', 'urgência', 'imediato', 'crítico', 'problema', 'ajuda']
        
        texto_lower = texto.lower()
        
        # Classificar tipo
        if any(k in texto_lower for k in keywords_custo):
            contexto['tipo'] = 'redução_custo'
        elif any(k in texto_lower for k in keywords_receita):
            contexto['tipo'] = 'aumento_receita'
        elif any(k in texto_lower for k in keywords_operacao):
            contexto['tipo'] = 'melhoria_operacional'
        
        # Urgência
        contexto['urgente'] = any(k in texto_lower for k in keywords_urgente)
        
        # Resumo (primeiras 200 chars do corpo)
        linhas = [l.strip() for l in texto.split('\n') if l.strip() and not l.startswith('>')]
        contexto['resumo'] = ' '.join(linhas[:3])[:200]
        
        return contexto
    
    def _classificar_demanda(self, texto, emails):
        """Classifica demanda segundo impacto"""
        classificacao = {
            'impacto_financeiro': 'a_avaliar',
            'urgencia': 'normal',
            'complexidade': 'média',
            'justificativa': 'Classificação inicial automática. Requer revisão humana.',
            'numero_emails': len(emails),
            'tempo_thread': self._calcular_tempo_thread(emails)
        }
        
        # Se muitos emails na thread, pode indicar problema não resolvido
        if len(emails) > 5:
            classificacao['urgencia'] = 'urgente'
            classificacao['justificativa'] = f'Thread longa ({len(emails)} emails) sugere problema não resolvido'
        
        return classificacao
    
    def _calcular_tempo_thread(self, emails):
        """Calcula duração da thread de emails"""
        if len(emails) < 2:
            return "email único"
        
        try:
            datas = [email.utils.parsedate_to_datetime(e['data']) for e in emails if e.get('data')]
            if datas:
                delta = max(datas) - min(datas)
                return f"{delta.days} dias, {delta.seconds//3600} horas"
        except:
            pass
        
        return "não calculado"
    
    def _avaliar_atendimento(self, texto, emails):
        """Avalia qualidade do atendimento"""
        avaliacao = {
            'clareza': 'a_avaliar',
            'tempo_resposta': 'a_avaliar',
            'resolutividade': 'a_avaliar',
            'empatia': 'a_avaliar',
            'observacoes': []
        }
        
        # Contar emails enviados vs recebidos
        enviados = sum(1 for e in emails if 'avila' in e.get('de', '').lower())
        recebidos = sum(1 for e in emails if 'avila' not in e.get('de', '').lower())
        
        if enviados > 0:
            avaliacao['observacoes'].append(f'{enviados} email(s) enviado(s) pela Ávila')
        if recebidos > enviados:
            avaliacao['observacoes'].append('⚠️  Mais emails do cliente do que respostas - possível demora')
        
        return avaliacao
    
    def _verificar_privacidade(self, texto):
        """Verifica dados sensíveis (LGPD)"""
        alertas = []
        
        # CPF
        if re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', texto):
            alertas.append('⚠️  CPF detectado - verificar necessidade de anonimização')
        
        # Email
        emails_encontrados = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
        if emails_encontrados:
            alertas.append(f'ℹ️  {len(emails_encontrados)} email(s) detectado(s) - avaliar se é PII')
        
        # Telefone
        if re.search(r'\(\d{2}\)\s*\d{4,5}-\d{4}', texto):
            alertas.append('⚠️  Telefone detectado - avaliar contexto')
        
        # CNPJ
        if re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto):
            alertas.append('ℹ️  CNPJ detectado (não é PII, mas é confidencial)')
        
        return {
            'alertas': alertas,
            'conforme_lgpd': len(alertas) == 0,
            'requer_anonimizacao': any('⚠️' in a for a in alertas)
        }
    
    def _analisar_thread(self, emails):
        """Analisa padrão de conversação"""
        return {
            'total_emails': len(emails),
            'primeiro_email': emails[0]['data'] if emails else None,
            'ultimo_email': emails[-1]['data'] if emails else None,
            'participantes': list(set([e['de'] for e in emails] + [e['para'] for e in emails])),
            'assuntos': list(set([e['assunto'] for e in emails]))
        }
    
    def _gerar_proximos_passos(self):
        """Gera próximos passos segundo filosofia Ávila"""
        passos = []
        
        # Baseado na urgência
        if self.analise.get('contexto', {}).get('urgente'):
            passos.append({
                'passo': 1,
                'acao': 'Resposta imediata ao cliente',
                'prazo': '4h úteis (SLA normal) ou 2h se CRÍTICO',
                'responsavel': 'Atendimento',
                'justificativa': 'Email classificado como urgente'
            })
        
        passos.append({
            'passo': len(passos) + 1,
            'acao': 'Revisão humana da análise automática',
            'prazo': '24h úteis',
            'responsavel': 'Consultor responsável',
            'justificativa': 'Validar classificação e contexto'
        })
        
        if self.analise.get('privacidade', {}).get('requer_anonimizacao'):
            passos.append({
                'passo': len(passos) + 1,
                'acao': 'Anonimizar dados sensíveis antes de registrar',
                'prazo': 'Imediato',
                'responsavel': 'Compliance',
                'justificativa': 'Conformidade LGPD'
            })
        
        passos.append({
            'passo': len(passos) + 1,
            'acao': 'Registrar no dossiê do cliente',
            'prazo': '24h úteis',
            'responsavel': 'Atendimento',
            'justificativa': 'Princípio: todo contato relevante vira nota'
        })
        
        # Se thread longa, sugerir call
        if len(self.emails_analisados) > 5:
            passos.append({
                'passo': len(passos) + 1,
                'acao': 'Propor call/reunião em vez de continuar por email',
                'prazo': 'Próxima resposta',
                'responsavel': 'Atendimento',
                'justificativa': f'Thread com {len(self.emails_analisados)} emails - call pode ser mais eficiente'
            })
        
        return passos
    
    def gerar_relatorio(self, arquivo_saida='relatorio_analise_email.md'):
        """Gera relatório em Markdown"""
        caminho_saida = Path(arquivo_saida)
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Análise de Email - Ávila Inc\n")
            f.write(f"**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            f.write("---\n\n")
            
            # 1. THREAD DE EMAILS
            f.write("## 1. Thread de Emails Analisada\n\n")
            f.write(f"**Total de emails**: {len(self.emails_analisados)}\n\n")
            
            for idx, email_info in enumerate(self.emails_analisados, 1):
                f.write(f"### 📧 Email #{idx}\n\n")
                f.write(f"- **De**: {email_info['de']}\n")
                f.write(f"- **Para**: {email_info['para']}\n")
                f.write(f"- **Assunto**: {email_info['assunto']}\n")
                f.write(f"- **Data**: {email_info['data']}\n\n")
                f.write("**Conteúdo**:\n```\n")
                f.write(email_info['corpo'][:500])
                if len(email_info['corpo']) > 500:
                    f.write("\n[... continua ...]\n")
                f.write("\n```\n\n")
            
            # 2. ANÁLISE
            f.write("---\n\n")
            f.write("## 2. Análise Segundo Diretrizes Ávila Inc\n\n")
            
            # Contexto
            f.write("### 2.1 Contexto Identificado\n\n")
            ctx = self.analise.get('contexto', {})
            f.write(f"- **Tipo**: {ctx.get('tipo', 'indefinido')}\n")
            f.write(f"- **Urgente**: {'✅ SIM' if ctx.get('urgente') else '❌ NÃO'}\n")
            f.write(f"- **Resumo**: {ctx.get('resumo', 'N/A')}\n\n")
            
            # Classificação
            f.write("### 2.2 Classificação da Demanda\n\n")
            classif = self.analise.get('classificacao', {})
            f.write(f"- **Impacto Financeiro**: {classif.get('impacto_financeiro')}\n")
            f.write(f"- **Urgência**: {classif.get('urgencia')}\n")
            f.write(f"- **Complexidade**: {classif.get('complexidade')}\n")
            f.write(f"- **Emails na thread**: {classif.get('numero_emails')}\n")
            f.write(f"- **Duração da thread**: {classif.get('tempo_thread')}\n")
            f.write(f"- **Justificativa**: {classif.get('justificativa')}\n\n")
            
            # Thread
            f.write("### 2.3 Análise de Conversação\n\n")
            thread = self.analise.get('thread', {})
            f.write(f"- **Participantes**: {', '.join(thread.get('participantes', []))}\n")
            f.write(f"- **Assuntos discutidos**: {len(thread.get('assuntos', []))}\n\n")
            
            # Privacidade
            f.write("### 2.4 Verificação de Privacidade (LGPD/GDPR)\n\n")
            priv = self.analise.get('privacidade', {})
            f.write(f"- **Conforme LGPD**: {'✅ SIM' if priv.get('conforme_lgpd') else '⚠️  REVISAR'}\n")
            f.write(f"- **Requer Anonimização**: {'✅ SIM' if priv.get('requer_anonimizacao') else '❌ NÃO'}\n\n")
            
            if priv.get('alertas'):
                f.write("**⚠️  Alertas de Dados Sensíveis**:\n")
                for alerta in priv['alertas']:
                    f.write(f"- {alerta}\n")
                f.write("\n")
            
            # Próximos Passos
            f.write("---\n\n")
            f.write("## 3. Próximos Passos (Filosofia Ávila)\n\n")
            
            for passo in self.analise.get('proximos_passos', []):
                f.write(f"#### Passo {passo['passo']}: {passo['acao']}\n\n")
                f.write(f"- **Prazo**: {passo['prazo']}\n")
                f.write(f"- **Responsável**: {passo['responsavel']}\n")
                f.write(f"- **Justificativa**: {passo['justificativa']}\n\n")
            
            # Rodapé
            f.write("---\n\n")
            f.write("## 4. Princípios Aplicados\n\n")
            f.write("✅ **Cliente primeiro**: análise orientada a impacto\n")
            f.write("✅ **Excelência humana**: email avaliado por clareza e resolutividade\n")
            f.write("✅ **Privacidade-first**: verificação automática de dados sensíveis\n")
            f.write("✅ **Rigor analítico**: classificação estruturada\n")
            f.write("✅ **Human-in-the-loop**: requer revisão humana\n\n")
            
            f.write("---\n\n")
            f.write(f"*Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*\n")
            f.write("*Ávila Inc — Consultoria com atendimento 100% humano e IA assistiva*\n")
        
        print(f"✅ Relatório salvo: {caminho_saida}")
        return caminho_saida
    
    def processar_emails_completo(self, pasta="INBOX", filtro="UNSEEN", limite=20):
        """Pipeline completo: Buscar → Analisar → Relatório"""
        print("\n" + "="*60)
        print("ANALISADOR DE EMAILS - ÁVILA INC")
        print("="*60 + "\n")
        
        # 1. Buscar emails
        ids = self.buscar_emails(pasta, filtro, limite)
        
        if not ids:
            print("❌ Nenhum email encontrado")
            return None
        
        # 2. Processar cada email
        print(f"\n{'='*60}")
        print("PROCESSANDO EMAILS")
        print(f"{'='*60}\n")
        
        for idx, email_id in enumerate(ids, 1):
            email_info = self.processar_email(email_id)
            if email_info:
                self.emails_analisados.append(email_info)
                print(f"✅ {idx}/{len(ids)} - De: {email_info['de'][:50]}")
        
        if not self.emails_analisados:
            print("❌ Nenhum email processado com sucesso")
            return None
        
        # 3. Analisar
        self.analisar_segundo_diretrizes_avila()
        
        # 4. Relatório
        relatorio = self.gerar_relatorio()
        
        print("\n" + "="*60)
        print("✅ ANÁLISE COMPLETA FINALIZADA")
        print("="*60 + "\n")
        
        return relatorio


def analisar_arquivo_eml(caminho_arquivo):
    """
    Analisa arquivo .eml salvo localmente
    Útil para analisar emails sem conectar ao servidor
    """
    print(f"📧 Analisando arquivo: {caminho_arquivo}\n")
    
    with open(caminho_arquivo, 'rb') as f:
        mensagem = email.message_from_bytes(f.read())
    
    analisador = AnalisadorEmailsAvila()
    
    # Processar o email do arquivo
    de = analisador._decodificar_header(mensagem.get("From"))
    para = analisador._decodificar_header(mensagem.get("To"))
    assunto = analisador._decodificar_header(mensagem.get("Subject"))
    data = mensagem.get("Date")
    corpo = analisador._extrair_corpo(mensagem)
    
    email_info = {
        'id': 'arquivo_local',
        'de': de,
        'para': para,
        'assunto': assunto,
        'data': data,
        'corpo': corpo,
        'timestamp': datetime.now().isoformat()
    }
    
    analisador.emails_analisados.append(email_info)
    analisador.analisar_segundo_diretrizes_avila()
    
    return analisador.gerar_relatorio()


def main():
    """
    Função principal - Exemplo de uso
    """
    print("="*60)
    print("ANALISADOR DE EMAILS ÁVILA INC")
    print("="*60)
    print("\nModos de uso:\n")
    print("1. Conectar a servidor de email (IMAP)")
    print("2. Analisar arquivo .eml local\n")
    
    modo = input("Escolha o modo (1 ou 2): ").strip()
    
    if modo == "1":
        # Modo servidor IMAP
        print("\n📧 Configuração de Email\n")
        servidor = input("Servidor IMAP (ex: imap.gmail.com): ").strip()
        usuario = input("Email: ").strip()
        senha = input("Senha/App Password: ").strip()
        
        analisador = AnalisadorEmailsAvila(servidor, usuario, senha)
        
        print("\nFiltros disponíveis:")
        print("- UNSEEN (não lidos)")
        print("- ALL (todos)")
        print("- FROM 'email@exemplo.com'")
        print("- SUBJECT 'palavra-chave'")
        
        filtro = input("\nFiltro (Enter para UNSEEN): ").strip() or "UNSEEN"
        limite = int(input("Limite de emails (Enter para 20): ").strip() or "20")
        
        relatorio = analisador.processar_emails_completo(filtro=filtro, limite=limite)
        
        if relatorio:
            print(f"\n📄 Relatório: {relatorio}")
    
    elif modo == "2":
        # Modo arquivo local
        caminho = input("\nCaminho do arquivo .eml: ").strip()
        
        if os.path.exists(caminho):
            relatorio = analisar_arquivo_eml(caminho)
            print(f"\n📄 Relatório: {relatorio}")
        else:
            print(f"❌ Arquivo não encontrado: {caminho}")
    
    else:
        print("❌ Modo inválido")


if __name__ == "__main__":
    main()
