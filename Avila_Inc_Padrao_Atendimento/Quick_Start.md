# 🚀 Quick Start - Ávila Inc Atendimento

> **Para começar HOJE** com o Padrão de Atendimento de Excelência

---

## ⚡ 5 Minutos para Começar

### 1. Você é Atendente?

**Leia primeiro** (15min):
1. `PADRAO_ATENDIMENTO_EXCELENCIA.md` - Seções 1, 2 e 3
2. `scripts/primeiro_contato.md`
3. `scripts/caso_critico.md`

**Use agora**:
- Cliente novo? → `scripts/primeiro_contato.md`
- Emergência? → `scripts/caso_critico.md`
- Dúvida sobre SLA? → Ver tabela seção 2.1 do Padrão

**Registre tudo**:
- No dossiê do cliente em `clientes/[nome]/historico_atendimento.md`

---

### 2. Você é Gestor?

**Revisar** (30min):
1. `SUMARIO_EXECUTIVO.md` - Visão geral do projeto
2. `clientes/arkana_store/dossie.md` - Exemplo de dossiê completo
3. `clientes/arkana_store/plano_acao_shopify_suspensao.md` - Exemplo de plano

**Atribuir agora**:
- [ ] Consultor para caso Arkana Store
- [ ] Revisor para aprovar PRs de scripts
- [ ] Responsável por métricas (CSAT, NPS, FRT)

**Monitorar**:
- Seção 8 do `PADRAO_ATENDIMENTO_EXCELENCIA.md` (Métricas)

---

### 3. Você é Desenvolvedor/IA?

**Integrar**:
1. `ia_assistiva/prompts_atendimento.md` - 8 prompts prontos
2. `ia_assistiva/analise_conversa.py` - Script OCR já funcional

**Usar IA assistiva**:
```python
# Exemplo rápido
from analisar_conversa_whatsapp import AnalisadorConversaWhatsApp

analisador = AnalisadorConversaWhatsApp("caminho/para/imagens")
analisador.executar_analise_completa()
# Output: relatorio_analise_conversa.md
```

**Lembrar**:
- ✅ Human-in-the-loop SEMPRE
- ❌ NUNCA treinar modelo com dados de clientes
- ✅ Apenas inferência com pseudonimização

---

## 📋 Cheatsheet de Casos Comuns

| Situação | O Que Fazer | Onde Ver |
|----------|-------------|----------|
| **Cliente novo contactou** | Usar script primeiro contato | `scripts/primeiro_contato.md` |
| **Site do cliente caiu** | Escalonar para CRÍTICO | `scripts/caso_critico.md` |
| **Dúvida sobre SLA** | Conferir tabela | `PADRAO_ATENDIMENTO_EXCELENCIA.md` seção 2.1 |
| **Como registrar atendimento** | Ver estrutura de dossiê | `PADRAO_ATENDIMENTO_EXCELENCIA.md` seção 5 |
| **Cliente com dados sensíveis** | Protocolo LGPD | `PADRAO_ATENDIMENTO_EXCELENCIA.md` seção 6 |
| **IA sugeriu resposta estranha** | SEMPRE revisar e personalizar | `ia_assistiva/prompts_atendimento.md` final |
| **Quero melhorar um script** | Fazer PR | `CONTRIBUTING.md` |

---

## 🎯 Caso Urgente AGORA?

### Se é CRÍTICO (site fora, perda de receita)

**Passo 1** (5min):
```markdown
Template de resposta IMEDIATA (copie e personalize):

[Nome], URGÊNCIA RECEBIDA ✅

Seu caso foi escalado para PRIORIDADE CRÍTICA.

AÇÕES IMEDIATAS:
✅ Caso #[número] aberto
✅ Consultor senior: [Seu Nome]
✅ Análise iniciada AGORA
✅ Retorno com diagnóstico em 2 horas

RESPONSÁVEL: [Seu Nome]
📞 [WhatsApp Direto]

Att, [Nome] - Ávila Inc
```

**Passo 2** (10min):
- Abrir dossiê em `clientes/[nome_cliente]/`
- Copiar template de `clientes/arkana_store/dossie.md`
- Preencher informações básicas

**Passo 3** (2h):
- Diagnosticar problema
- Montar plano usando `clientes/arkana_store/plano_acao_shopify_suspensao.md` como base
- Enviar plano ao cliente

---

## 📞 Atalhos Rápidos

### Templates Prontos para Copiar

**Resposta de Follow-up (+24h sem resposta)**:
```markdown
Oi [Nome], tudo bem?

Enviei uma mensagem ontem sobre [problema].

Sei que o dia a dia é corrido. Se ainda for relevante, me avisa.
Senão, sem problemas - fico à disposição quando precisar!

Att, [Seu Nome] - Ávila Inc
```

**Pedido de Informação**:
```markdown
[Nome], para eu te ajudar da melhor forma, preciso de 3 informações:

1. [Pergunta 1]
2. [Pergunta 2]
3. [Pergunta 3]

Com isso, monto um plano personalizado em 24h.

Quando você tem 15-20min para conversarmos?

Att, [Seu Nome]
```

**Atualização durante Crise**:
```markdown
[Nome], update às [HH:MM]:

✅ [O que foi feito]
⏳ [O que está em andamento]
🎯 [Próximo marco - quando]

Att, [Seu Nome]
```

---

## 🎓 Treinamento Rápido (Novo na Equipe)

### Dia 1 (Leitura - 2h)
- [ ] `SUMARIO_EXECUTIVO.md`
- [ ] `PADRAO_ATENDIMENTO_EXCELENCIA.md` seções 1-7
- [ ] `scripts/primeiro_contato.md`

### Dia 2 (Observação - 4h)
- [ ] Acompanhar 5+ atendimentos com senior
- [ ] Ler dossiê completo de Arkana Store
- [ ] Simular resposta para 3 casos (revisar com senior)

### Dia 3 (Prática - 6h)
- [ ] Atender casos NORMAIS com supervisão
- [ ] Registrar tudo no dossiê
- [ ] Receber feedback

### Dia 4-5 (Autonomia - 8h/dia)
- [ ] Atender casos NORMAIS sozinho
- [ ] Pedir revisão apenas em casos URGENTES/CRÍTICOS
- [ ] Meta: CSAT > 4/5 em 10 atendimentos

**Certificação**: Após 20 atendimentos com CSAT > 4.5 → Atendente Certificado Ávila Inc ✅

---

## 🚨 Quando Escalonar?

### Escalonar para Supervisor se:

- Não consegue resolver caso NORMAL em 24h
- Cliente muito insatisfeito (risco de churn)
- Solicitação fora do escopo padrão
- Dúvida sobre precificação/contrato

### Escalonar para Diretor se:

- Caso CRÍTICO não resolve em 12h
- Cliente ameaça ação legal
- Conflito ético (pedido antiético/ilegal)
- Oportunidade grande (conta > R$ 50k/mês)

**Como escalonar**:
```markdown
[Supervisor/Diretor],

Caso: [Nome Cliente] - [Resumo 1 linha]
Urgência: [CRÍTICO/URGENTE]
Motivo escalação: [Por que não consegui resolver]
Ações já tomadas: [Lista]
Próximo passo sugerido: [Sua recomendação]

Prazo cliente: [quando]
Responsável atual: [Seu Nome]

[Link para dossiê]
```

---

## 💡 Dicas de Ouro

1. **Quando em dúvida, pergunte**: Melhor confirmar do que errar
2. **Registre TUDO**: "Se não está no dossiê, não aconteceu"
3. **Prometa menos, entregue mais**: Cliente ama surpresa positiva
4. **Empatia sempre**: Mesmo em caso difícil, validar sentimento
5. **Human beats IA**: Sempre revise sugestão da IA antes de enviar

---

## 📊 Checklist Diário

### Manhã (9h)
- [ ] Revisar casos pendentes
- [ ] Priorizar por urgência
- [ ] Responder mensagens overnight

### Durante o Dia
- [ ] FRT < 4h para todos
- [ ] Atualizar dossiês
- [ ] Escalonar se necessário

### Tarde (18h)
- [ ] Todos os casos têm próximo passo?
- [ ] Clientes avisados se algo pendente?
- [ ] Dossiês atualizados?
- [ ] Preparar hand-off (se necessário)

---

## 🎉 Primeiro Atendimento Perfeito

Use este checklist no seu primeiro atendimento:

1. **Recebeu mensagem**
   - [ ] Classifiquei urgência (CRÍTICO/URGENTE/NORMAL/BAIXO)
   - [ ] Marquei tempo de recebimento (para calcular FRT)

2. **Preparei resposta**
   - [ ] Usei template apropriado do `scripts/`
   - [ ] Personalizei (não copiei e colei direto)
   - [ ] Inclui: Empatia + Análise + Ação + Responsabilidade + Validação
   - [ ] Revisei português/formatação

3. **Enviei e registrei**
   - [ ] Enviei dentro do SLA (2-4h)
   - [ ] Registrei no dossiê do cliente
   - [ ] Configurei lembrete de follow-up (se necessário)

4. **Follow-up**
   - [ ] Cliente respondeu? Continuar conversa
   - [ ] Não respondeu em 24h? Enviar follow-up
   - [ ] Caso resolvido? Pedir feedback (CSAT)

**Se fez tudo isso**: Parabéns! Você acabou de fazer um atendimento padrão Ávila Inc! 🎉

---

## 📞 Ajuda Rápida

**Dúvida sobre**:
- Processo → `CONTRIBUTING.md`
- Scripts → `scripts/[nome].md`
- IA → `ia_assistiva/prompts_atendimento.md`
- Caso específico → Perguntar no #atendimento (Slack/Teams)

**Emergência AGORA**:
- WhatsApp do supervisor: [PEND: adicionar]
- Telefone do diretor: [PEND: adicionar]

---

**Versão**: 1.0.0  
**Última atualização**: 12/11/2025

---

*Ávila Inc - Excelência acessível em 5 minutos. Maestria em 5 dias.* 🚀
