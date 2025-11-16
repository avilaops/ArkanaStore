# Plano de Ação - Reversão Suspensão Shopify | Arkana Store

> **Projeto**: Recuperação Loja Shopify Suspensa  
> **Cliente**: Marcelo Quintino / Arkana Store  
> **Status**: 🔴 CRÍTICO - EM ANDAMENTO  
> **Data Início**: 12/11/2025  
> **Responsável**: [Atribuir Consultor Senior]  
> **Prazo**: 30 dias (com revisão a cada 7 dias)

---

## 🎯 Objetivo SMART

**Específico**: Reverter suspensão da loja Shopify Arkana Store OU migrar para plataforma alternativa  
**Mensurável**: Site online e processando vendas  
**Atingível**: Baseado em casos similares de reversão bem-sucedida (benchmark: 40-60%)  
**Relevante**: Impacto direto na receita do cliente (site fora = R$ 0/dia)  
**Temporal**: 30 dias para resolução completa

---

## 📊 Baseline (Situação Atual)

| Indicador | Valor Atual |
|-----------|-------------|
| **Status da Loja** | ❌ Suspensa (desde 31/10/2025) |
| **Receita Mensal** | R$ 0 (site inacessível) |
| **Pagamentos Retidos** | [PEND: valor total] - Bloqueado por 120 dias |
| **Tráfego do Site** | 0 visitantes |
| **Perda Diária Estimada** | [PEND: calcular com cliente] |
| **Dias Parado** | 12 dias (e contando) |

**Impacto Financeiro Acumulado**:
- Perda de receita: R$ [X] (12 dias × média diária)
- Pagamentos bloqueados: R$ [Y]
- **Total em risco**: R$ [X + Y]

---

## 🔍 Diagnóstico Inicial

### Informações Conhecidas

✅ **Email de suspensão**: Recebido em 31/10/2025  
✅ **Motivo oficial**: Violação da Política de Uso Aceitável (PUA)  
✅ **Tickets Shopify**: `6550008e-ccc9-4fad-bb29-856df973c47c` e `cdb4e012-9d1c-40d8-93e5-98c49e191cac`  
✅ **Formulário de recurso**: Agência do cliente já submeteu (data: [PEND])  

### Informações Pendentes (Fase 1)

❓ **Catálogo de produtos**: O que era vendido? Algum item restrito?  
❓ **Disputas/Chargebacks**: Histórico de reclamações de clientes?  
❓ **Propriedade intelectual**: Imagens/descrições próprias ou de terceiros?  
❓ **Compliance**: Certificações Anvisa/Inmetro para produtos regulamentados?  
❓ **Histórico de avisos**: Shopify enviou warnings antes da suspensão?  

### Hipóteses de Causa Raiz

| Hipótese | Probabilidade | Ação de Validação |
|----------|---------------|-------------------|
| **Produtos restritos** (réplicas, suplementos, etc.) | Alta | Revisar catálogo completo |
| **Copyright/Marca** (uso indevido de imagens/marcas) | Média | Auditoria de propriedade intelectual |
| **Chargebacks alto** (> 1% das transações) | Média | Solicitar relatório Shopify Payments |
| **Descrições enganosas** (claims sem comprovação) | Baixa | Revisar copy dos produtos |
| **HIPAA/Dados de saúde** (se vende produtos saúde) | Baixa | Verificar categorias vendidas |

---

## 📋 Plano 30-60-90 Dias

### ⏰ Fase 0: Primeiras 24 Horas (12-13/11/2025)

**Objetivo**: Coleta de informações críticas + diagnóstico preciso

#### Tarefas

1. **[CRÍTICO]** Ligar para Marcelo Quintino  
   - **Responsável**: [Consultor Ávila]  
   - **Prazo**: Hoje, até 18h  
   - **Roteiro**: `scripts/primeiro_contato.md` + perguntas diagnóstico  
   - **Entregável**: Notas da call + lista de produtos + acesso ao painel (se possível)

2. **[URGENTE]** Obter cópia do recurso enviado pela agência  
   - **Responsável**: [Consultor Ávila]  
   - **Prazo**: Hoje, até 20h  
   - **Como**: Solicitar ao Marcelo forward do email/PDF  
   - **Objetivo**: Entender o que já foi argumentado, evitar duplicação

3. **[URGENTE]** Análise da Política de Uso Aceitável Shopify  
   - **Responsável**: [Analista Compliance]  
   - **Prazo**: Amanhã, 9h  
   - **Ação**: Ler PUA completa + casos de jurisprudência  
   - **Entregável**: Checklist de conformidade

4. **Benchmark de casos similares**  
   - **Responsável**: [Analista]  
   - **Prazo**: Amanhã, 12h  
   - **Fontes**: Fóruns Shopify, Reddit, grupos de e-commerce  
   - **Objetivo**: Taxa de sucesso de reversão, argumentos eficazes

**Métrica de Sucesso Fase 0**:  
✅ Diagnóstico preciso da causa raiz (confirmado ou 2-3 hipóteses principais)

---

### 📅 Fase 1: Dias 1-7 (13-19/11/2025)

**Objetivo**: Tentativa de reversão via Shopify + Preparação Plano B

#### Estratégia A: Reversão Shopify

**1.1 Preparar Documentação de Compliance**  
   - **Prazo**: 15/11 (3 dias)  
   - **Itens**:  
     - [ ] Certificações de produtos (Anvisa, Inmetro, etc.)  
     - [ ] Notas fiscais de fornecedores (comprovar origem lícita)  
     - [ ] Declaração de conformidade com PUA (modelo Ávila)  
     - [ ] Plano de adequação (se houver violação identificada)  
     - [ ] Screenshot de produtos concorrentes aprovados (se aplicável)

**1.2 Reformular Recurso (Versão Ávila)**  
   - **Prazo**: 16/11 (4 dias)  
   - **Estrutura**:  
     ```markdown
     # Recurso de Suspensão - Arkana Store

     ## 1. Resumo Executivo
     [Argumento principal em 3 linhas]

     ## 2. Contexto
     [Histórico da loja, tempo de operação, volume de vendas, CSAT]

     ## 3. Análise da Suspensão
     [Entendimento da violação alegada]

     ## 4. Evidências de Conformidade
     [Anexar docs: certificações, NFs, políticas internas]

     ## 5. Ações Corretivas Implementadas
     [O que já mudamos para estar 100% conforme]

     ## 6. Plano de Monitoramento Contínuo
     [Como garantiremos conformidade futura]

     ## 7. Solicitação
     [Reativar loja + liberar pagamentos]

     Anexos: [15+ PDFs de evidência]
     ```

**1.3 Submeter Recurso Otimizado**  
   - **Prazo**: 17/11 (5 dias)  
   - **Canal**: Formulário oficial Shopify  
   - **CC**: Email para account manager (se houver)  
   - **Follow-up**: A cada 48h até obter resposta

#### Estratégia B: Plano B (Paralelo)

**1.4 Avaliar Plataformas Alternativas**  
   - **Prazo**: 15/11 (3 dias)  
   - **Opções**:  
     | Plataforma | Custo Setup | Custo Mensal | Tempo Migração | Prós | Contras |
     |------------|-------------|--------------|----------------|------|---------|
     | WooCommerce | R$ 2.000 | R$ 300 | 7 dias | Controle total | Mais técnico |
     | VTEX | R$ 15.000 | R$ 2.500 | 30 dias | Enterprise | Caro |
     | Nuvemshop | R$ 500 | R$ 200 | 3 dias | Rápido, BR | Menos features |
     | Tray | R$ 1.000 | R$ 150 | 5 dias | Bom custo-benefício | Suporte variável |

**1.5 Orçar Migração Express (3 cotações)**  
   - **Prazo**: 16/11 (4 dias)  
   - **Agências**: [Nome 1], [Nome 2], [Nome 3]  
   - **Critério**: Prazo < 7 dias + custo razoável + portfólio comprovado

**Métrica de Sucesso Fase 1**:  
✅ Recurso submetido com documentação completa  
✅ Plano B orçado e aprovado (se necessário)

---

### 📅 Fase 2: Dias 8-30 (20/11 - 12/12/2025)

**Objetivo**: Resolução definitiva (Shopify reativado OU migração concluída)

#### Cenário A: Shopify Aprovou Recurso

**2A.1 Reativar Loja**  
   - **Prazo**: Imediato após aprovação  
   - **Checklist**:  
     - [ ] Verificar todos os produtos visíveis  
     - [ ] Testar checkout completo  
     - [ ] Confirmar domínio conectado  
     - [ ] Validar gateway de pagamento ativo  
     - [ ] Enviar email para base de clientes (loja de volta)

**2A.2 Auditar Conformidade Total**  
   - **Prazo**: 7 dias pós-reativação  
   - **Ação**:  
     - Revisar 100% dos produtos (descrições, imagens, claims)  
     - Implementar política de compliance interna  
     - Treinar equipe do cliente em PUA  
     - Configurar alertas de risco (ex: chargebacks > 0.5%)

**2A.3 Recuperar Pagamentos Retidos**  
   - **Prazo**: Conforme Shopify (pode ser imediato ou manter 120 dias)  
   - **Ação**: Negociar liberação antecipada se possível

#### Cenário B: Shopify Negou Recurso (Irreversível)

**2B.1 Migração Express**  
   - **Prazo**: 7-10 dias  
   - **Plataforma**: [Definida na Fase 1]  
   - **Etapas**:  
     - [ ] Setup inicial da plataforma  
     - [ ] Migração de produtos (via CSV ou API)  
     - [ ] Migração de clientes (se permitido)  
     - [ ] Configuração de pagamentos  
     - [ ] Configuração de frete  
     - [ ] Testes de checkout  
     - [ ] Redirecionamento de domínio  
     - [ ] Go-live

**2B.2 Comunicação com Clientes**  
   - **Prazo**: 1 dia antes do go-live  
   - **Canais**: Email, WhatsApp, redes sociais  
   - **Mensagem**:  
     ```
     Olá!

     A Arkana Store está de volta! 🎉

     Migramos para uma nova plataforma ainda melhor.
     Seu cadastro foi mantido (mesma senha).

     Novo site: www.arkanastore.com.br

     Para comemorar: [cupom de desconto/frete grátis]

     Obrigado pela paciência!
     Equipe Arkana Store
     ```

**2B.3 Disputa Shopify (Pagamentos Retidos)**  
   - **Prazo**: Paralelo à migração  
   - **Ação**:  
     - Contratar advogado especializado em direito digital  
     - Avaliar ação judicial vs. custo-benefício  
     - Negociar liberação parcial (via suporte escalado)

**Métrica de Sucesso Fase 2**:  
✅ Site online e processando vendas (Shopify OU nova plataforma)  
✅ Primeira venda concretizada  
✅ Clientes notificados e engajados

---

### 📅 Fase 3: Dias 31-90 (13/12/2025 - 12/02/2026)

**Objetivo**: Crescimento sustentável + Conformidade contínua

**3.1 Otimização Pós-Recuperação**  
   - SEO: Recuperar rankings perdidos  
   - Ads: Reativar campanhas Google/Meta  
   - Email marketing: Reengajar base

**3.2 Diversificação de Canais**  
   - Marketplace: Mercado Livre, Amazon, Magalu  
   - Social commerce: Instagram Shopping, WhatsApp Business  
   - Afiliados: Programa de indicação

**3.3 Compliance Contínuo**  
   - Auditoria mensal de produtos novos  
   - Monitoramento de chargebacks/disputas  
   - Atualização de certificações (quando expirar)

**Métrica de Sucesso Fase 3**:  
✅ Receita mensal = ou > baseline pré-suspensão  
✅ Conformidade 100% mantida  
✅ 2+ canais de venda ativos

---

## 💰 Investimento e Modelo de Negócio

### Proposta Comercial Ávila Inc

**[PEND: Aprovação direção]**

**Opção Sugerida: Projeto + Success Fee**

**Fase Emergencial (30 dias)**:
- **Investimento fixo**: R$ 5.000  
- **Escopo**:  
  - Diagnóstico completo  
  - Preparação e submissão de recurso  
  - Orçamento Plano B  
  - Gestão do projeto até resolução  

**Success Fee**:
- **Se recuperar pagamentos retidos**: 10% do valor recuperado  
- **Se reverter suspensão em < 15 dias**: Bônus de R$ 2.000 (pela agilidade)

**Retainer Pós-Recuperação** (opcional):
- R$ 1.500/mês  
- Compliance contínuo + consultoria e-commerce  
- Prioridade em atendimento  

---

## 📊 Métricas de Acompanhamento

### KPIs do Projeto

| Métrica | Baseline | Meta 7d | Meta 15d | Meta 30d |
|---------|----------|---------|----------|----------|
| **Status Loja** | ❌ Suspensa | ⏳ Recurso enviado | ✅ Decisão obtida | ✅ Online |
| **Receita Diária** | R$ 0 | R$ 0 | R$ [X] | R$ [Y] |
| **Produtos Conformes** | ?% | 100% | 100% | 100% |
| **Canais Ativos** | 0 | 0-1 | 1 | 2+ |

### Reuniões de Acompanhamento

- **Diária**: WhatsApp update (5min)  
- **Semanal**: Call 30min (status + próximos passos)  
- **Mensal**: Reunião executiva 1h (métricas + estratégia)

---

## 🚨 Plano de Contingência

### Se Shopify não responder em 15 dias

**Ação**: Pressionar via canais alternativos  
- Twitter público (@ShopifySupport)  
- LinkedIn (tag account managers)  
- Comunidade Shopify Partners  
- Escalar para jurídico (carta de advogado)

### Se Plano B também tiver problemas

**Ação**: Loja temporária em Linktree/Instagram  
- Catálogo em posts/stories  
- Pagamento via Pix/transferência  
- Enquanto plataforma principal não resolver

### Se cliente não tiver caixa para migração

**Ação**: Modelo de parceria  
- Ávila banca setup (R$ 2-3k)  
- Cliente paga via % das vendas (ex: 5% nos primeiros 3 meses)  
- Win-win: Ávila só ganha se cliente voltar a vender

---

## 📎 Anexos e Documentos

- [ ] **Recurso Shopify (versão agência)** - Solicitar ao cliente  
- [ ] **Catálogo completo de produtos** - Solicitar ao cliente  
- [ ] **Relatório Shopify Payments** (chargebacks, disputas) - Se acessível  
- [ ] **Certificações de produtos** - Solicitar ao cliente  
- [ ] **Cotações migração** (Fase 1) - Coletar de 3 agências  

---

## 🗒️ Observações e Riscos

### Riscos Conhecidos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Shopify não responder recurso | Média | Alto | Plano B pronto desde dia 1 |
| Pagamentos permanecem retidos 120d | Alta | Crítico | Ação judicial paralela |
| Migração > 7 dias | Baixa | Médio | Contratar agência com SLA |
| Cliente não ter caixa para investir | Média | Alto | Modelo de parceria/% vendas |

### Premissas Críticas

✅ Cliente fornecerá informações completas em 24-48h  
✅ Agência do cliente colaborará (acesso a recursos)  
✅ Violação da PUA é reversível (não é fraude grave)  
✅ Cliente tem documentação legal dos produtos  

---

## ✅ Checklist de Ações Imediatas

- [ ] **Hoje, 18h**: Ligar para Marcelo (diagnóstico)  
- [ ] **Hoje, 20h**: Obter recurso enviado pela agência  
- [ ] **Amanhã, 9h**: Análise completa da PUA Shopify  
- [ ] **Amanhã, 12h**: Benchmark de casos similares  
- [ ] **Amanhã, 18h**: Apresentar plano ao cliente (aprovação)  

---

**Última Atualização**: 12/11/2025  
**Próxima Revisão**: 13/11/2025 (após primeiro contato com cliente)

---

*Ávila Inc - Plano de Ação Executivo*  
*Confidencial - Acesso restrito à equipe do projeto*
