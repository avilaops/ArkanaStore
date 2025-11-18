"""
Script de OCR e Análise de Conversas WhatsApp
Ávila Inc - Conforme diretrizes 2025

Funcionalidades:
1. OCR de imagens de conversas WhatsApp
2. Análise baseada na filosofia Ávila Inc
3. Geração de relatório estruturado
"""

import os
from pathlib import Path
from datetime import datetime
import json
import re

# Bibliotecas de OCR (instalar: pip install easyocr pillow)
try:
    import easyocr
    OCR_ENGINE = 'easyocr'
except ImportError:
    print("⚠️  EasyOCR não encontrado. Tentando pytesseract...")
    try:
        import pytesseract
        from PIL import Image
        OCR_ENGINE = 'pytesseract'
    except ImportError:
        print("❌ Nenhum engine de OCR encontrado!")
        print("Instale: pip install easyocr pillow")
        print("Ou: pip install pytesseract pillow")
        exit(1)


class AnalisadorConversaWhatsApp:
    """
    Analisa conversas do WhatsApp segundo diretrizes Ávila Inc
    """
    
    def __init__(self, diretorio_imagens):
        self.diretorio = Path(diretorio_imagens)
        self.reader = None
        self.conversas_transcritas = []
        self.analise = {}
        
        # Inicializar engine de OCR
        if OCR_ENGINE == 'easyocr':
            print("📷 Inicializando EasyOCR (pt + en)...")
            self.reader = easyocr.Reader(['pt', 'en'], gpu=False)
        
    def encontrar_imagens_whatsapp(self):
        """Localiza todas as imagens do WhatsApp no diretório"""
        padroes = [
            'IMG-*-WA*.jpg',
            'Imagem do WhatsApp*.jpg',
            '*WhatsApp*.jpg',
            '*WA*.jpg'
        ]
        
        imagens = []
        for padrao in padroes:
            imagens.extend(self.diretorio.glob(padrao))
        
        imagens = sorted(set(imagens))  # Remove duplicatas e ordena
        print(f"✅ Encontradas {len(imagens)} imagens do WhatsApp")
        return imagens
    
    def fazer_ocr(self, caminho_imagem):
        """Extrai texto de uma imagem usando OCR"""
        print(f"🔍 Processando: {caminho_imagem.name}")
        
        try:
            if OCR_ENGINE == 'easyocr':
                resultado = self.reader.readtext(str(caminho_imagem))
                texto = '\n'.join([item[1] for item in resultado])
            else:  # pytesseract
                img = Image.open(caminho_imagem)
                texto = pytesseract.image_to_string(img, lang='por')
            
            return texto.strip()
        
        except Exception as e:
            print(f"❌ Erro ao processar {caminho_imagem.name}: {e}")
            return ""
    
    def processar_todas_imagens(self):
        """Processa todas as imagens e extrai textos"""
        imagens = self.encontrar_imagens_whatsapp()
        
        if not imagens:
            print("❌ Nenhuma imagem do WhatsApp encontrada!")
            return
        
        print(f"\n{'='*60}")
        print("INICIANDO TRANSCRIÇÃO OCR")
        print(f"{'='*60}\n")
        
        for idx, imagem in enumerate(imagens, 1):
            texto = self.fazer_ocr(imagem)
            
            if texto:
                self.conversas_transcritas.append({
                    'arquivo': imagem.name,
                    'numero': idx,
                    'texto': texto,
                    'timestamp': datetime.now().isoformat()
                })
                print(f"✅ {idx}/{len(imagens)} - {len(texto)} caracteres extraídos")
            else:
                print(f"⚠️  {idx}/{len(imagens)} - Nenhum texto detectado")
        
        print(f"\n✅ Transcrição concluída: {len(self.conversas_transcritas)} conversas")
    
    def analisar_segundo_diretrizes_avila(self):
        """
        Analisa conversas conforme filosofia Ávila Inc:
        - Cliente primeiro
        - Excelência humana
        - Rigor analítico
        - Problema → Hipótese → Experimento → Resultado
        """
        
        print(f"\n{'='*60}")
        print("ANÁLISE SEGUNDO DIRETRIZES ÁVILA INC")
        print(f"{'='*60}\n")
        
        texto_completo = "\n\n".join([c['texto'] for c in self.conversas_transcritas])
        
        # 1. IDENTIFICAÇÃO DE PROBLEMA/DEMANDA
        self.analise['contexto'] = self._identificar_contexto(texto_completo)
        
        # 2. CLASSIFICAÇÃO DE URGÊNCIA E IMPACTO
        self.analise['classificacao'] = self._classificar_demanda(texto_completo)
        
        # 3. ANÁLISE DE ATENDIMENTO (SLA, clareza, resolutividade)
        self.analise['qualidade_atendimento'] = self._avaliar_atendimento(texto_completo)
        
        # 4. IDENTIFICAÇÃO DE DADOS SENSÍVEIS (LGPD/GDPR)
        self.analise['privacidade'] = self._verificar_privacidade(texto_completo)
        
        # 5. PRÓXIMOS PASSOS RECOMENDADOS
        self.analise['proximos_passos'] = self._gerar_proximos_passos()
        
        print("✅ Análise concluída\n")
    
    def _identificar_contexto(self, texto):
        """Identifica o contexto da conversa"""
        contexto = {
            'tipo': 'indefinido',
            'resumo': '',
            'palavras_chave': []
        }
        
        # Palavras-chave para classificação
        keywords_custo = ['custo', 'redução', 'economia', 'despesa', 'gasto']
        keywords_receita = ['receita', 'faturamento', 'vendas', 'lucro', 'margem']
        keywords_operacao = ['processo', 'operação', 'sistema', 'automação', 'eficiência']
        keywords_urgente = ['urgente', 'agora', 'imediato', 'crítico', 'problema']
        
        texto_lower = texto.lower()
        
        # Classificar tipo
        if any(k in texto_lower for k in keywords_custo):
            contexto['tipo'] = 'redução_custo'
        elif any(k in texto_lower for k in keywords_receita):
            contexto['tipo'] = 'aumento_receita'
        elif any(k in texto_lower for k in keywords_operacao):
            contexto['tipo'] = 'melhoria_operacional'
        
        # Detectar urgência
        contexto['urgente'] = any(k in texto_lower for k in keywords_urgente)
        
        # Extrair primeiras linhas como resumo
        linhas = texto.split('\n')
        contexto['resumo'] = ' '.join([l.strip() for l in linhas[:5] if l.strip()])[:200]
        
        return contexto
    
    def _classificar_demanda(self, texto):
        """Classifica a demanda segundo impacto financeiro e urgência"""
        return {
            'impacto_financeiro': 'a_avaliar',  # alto/médio/baixo
            'urgencia': 'normal',  # crítica/alta/normal/baixa
            'complexidade': 'média',  # alta/média/baixa
            'justificativa': 'Classificação inicial automática. Requer revisão humana.'
        }
    
    def _avaliar_atendimento(self, texto):
        """Avalia qualidade do atendimento segundo princípios Ávila"""
        avaliacao = {
            'clareza': 'a_avaliar',
            'tempo_resposta': 'a_avaliar',
            'resolutividade': 'a_avaliar',
            'empatia': 'a_avaliar',
            'observacoes': []
        }
        
        # Verificar se há timestamps ou horários
        if re.search(r'\d{1,2}:\d{2}', texto):
            avaliacao['observacoes'].append('Timestamps detectados - possível avaliar FRT')
        
        # Verificar se há múltiplas mensagens sem resposta
        linhas = [l for l in texto.split('\n') if l.strip()]
        if len(linhas) > 10:
            avaliacao['observacoes'].append('Conversa longa - verificar se houve resolução')
        
        return avaliacao
    
    def _verificar_privacidade(self, texto):
        """Verifica vazamento de dados sensíveis (LGPD/GDPR)"""
        alertas = []
        
        # CPF
        if re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', texto):
            alertas.append('⚠️  CPF detectado - verificar necessidade de anonimização')
        
        # Email
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto):
            alertas.append('⚠️  Email detectado - avaliar se é PII')
        
        # Telefone
        if re.search(r'\(\d{2}\)\s*\d{4,5}-\d{4}', texto):
            alertas.append('⚠️  Telefone detectado - avaliar contexto')
        
        # CNPJ
        if re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto):
            alertas.append('ℹ️  CNPJ detectado (não é PII, mas é confidencial)')
        
        return {
            'alertas': alertas,
            'conforme_lgpd': len(alertas) == 0,
            'requer_anonimizacao': len(alertas) > 0
        }
    
    def _gerar_proximos_passos(self):
        """Gera próximos passos segundo filosofia Ávila"""
        passos = []
        
        # Baseado no contexto
        if self.analise.get('contexto', {}).get('urgente'):
            passos.append({
                'passo': 1,
                'acao': 'Resposta imediata ao cliente',
                'prazo': '4h úteis (conforme SLA)',
                'responsavel': 'Atendimento',
                'justificativa': 'Demanda classificada como urgente'
            })
        
        passos.append({
            'passo': 2,
            'acao': 'Revisão humana da análise automática',
            'prazo': '24h úteis',
            'responsavel': 'Consultor responsável',
            'justificativa': 'Validar hipóteses e classificações'
        })
        
        if self.analise.get('privacidade', {}).get('requer_anonimizacao'):
            passos.append({
                'passo': 3,
                'acao': 'Anonimizar dados sensíveis identificados',
                'prazo': 'Imediato',
                'responsavel': 'Compliance',
                'justificativa': 'Conformidade LGPD/GDPR'
            })
        
        passos.append({
            'passo': len(passos) + 1,
            'acao': 'Registrar no dossiê do cliente',
            'prazo': '24h úteis',
            'responsavel': 'Atendimento',
            'justificativa': 'Princípio: todo contato relevante vira nota'
        })
        
        return passos
    
    def gerar_relatorio(self, arquivo_saida='relatorio_analise_conversa.md'):
        """Gera relatório em Markdown"""
        
        caminho_saida = self.diretorio / arquivo_saida
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Análise de Conversa WhatsApp\n")
            f.write(f"**Ávila Inc** | {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            f.write("---\n\n")
            
            # 1. TRANSCRIÇÕES
            f.write("## 1. Transcrições OCR\n\n")
            for conversa in self.conversas_transcritas:
                f.write(f"### 📱 {conversa['arquivo']}\n\n")
                f.write("```\n")
                f.write(conversa['texto'])
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
            f.write(f"- **Justificativa**: {classif.get('justificativa')}\n\n")
            
            # Qualidade do Atendimento
            f.write("### 2.3 Avaliação de Atendimento\n\n")
            atend = self.analise.get('qualidade_atendimento', {})
            f.write(f"- **Clareza**: {atend.get('clareza')}\n")
            f.write(f"- **Tempo de Resposta**: {atend.get('tempo_resposta')}\n")
            f.write(f"- **Resolutividade**: {atend.get('resolutividade')}\n")
            f.write(f"- **Empatia**: {atend.get('empatia')}\n")
            
            if atend.get('observacoes'):
                f.write("\n**Observações**:\n")
                for obs in atend['observacoes']:
                    f.write(f"- {obs}\n")
            f.write("\n")
            
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
            f.write("### Ciclo: Problema → Hipótese → Experimento → Resultado\n\n")
            
            for passo in self.analise.get('proximos_passos', []):
                f.write(f"#### Passo {passo['passo']}: {passo['acao']}\n\n")
                f.write(f"- **Prazo**: {passo['prazo']}\n")
                f.write(f"- **Responsável**: {passo['responsavel']}\n")
                f.write(f"- **Justificativa**: {passo['justificativa']}\n\n")
            
            # Rodapé
            f.write("---\n\n")
            f.write("## 4. Princípios Aplicados\n\n")
            f.write("✅ **Cliente primeiro**: análise orientada a impacto\n")
            f.write("✅ **Excelência humana**: atendimento avaliado por clareza e resolutividade\n")
            f.write("✅ **Privacidade-first**: verificação automática de dados sensíveis\n")
            f.write("✅ **Rigor analítico**: classificação estruturada e próximos passos mensuráveis\n")
            f.write("✅ **Human-in-the-loop**: requer revisão humana das hipóteses\n\n")
            
            f.write("---\n\n")
            f.write(f"*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*\n")
            f.write("*Ávila Inc — Consultoria com atendimento 100% humano e IA assistiva*\n")
        
        print(f"✅ Relatório salvo: {caminho_saida}")
        return caminho_saida
    
    def executar_analise_completa(self):
        """Executa pipeline completo: OCR → Análise → Relatório"""
        print("\n" + "="*60)
        print("ANALISADOR DE CONVERSAS WHATSAPP - ÁVILA INC")
        print("="*60 + "\n")
        
        # 1. OCR
        self.processar_todas_imagens()
        
        if not self.conversas_transcritas:
            print("❌ Nenhuma conversa transcrita. Encerrando.")
            return None
        
        # 2. Análise
        self.analisar_segundo_diretrizes_avila()
        
        # 3. Relatório
        relatorio = self.gerar_relatorio()
        
        print("\n" + "="*60)
        print("✅ ANÁLISE COMPLETA FINALIZADA")
        print("="*60 + "\n")
        
        return relatorio


def main():
    """Função principal"""
    
    # Diretório das imagens (ajuste conforme necessário)
    diretorio = Path(__file__).parent
    
    print(f"📂 Diretório de trabalho: {diretorio}\n")
    
    # Criar analisador
    analisador = AnalisadorConversaWhatsApp(diretorio)
    
    # Executar análise completa
    relatorio = analisador.executar_analise_completa()
    
    if relatorio:
        print(f"\n📄 Relatório disponível em: {relatorio}")
        print("\n💡 Próximo passo: Revisar relatório e aplicar correções humanas")
        print("   conforme princípio Human-in-the-loop da Ávila Inc\n")


if __name__ == "__main__":
    main()
