
# Helix Runbook — Arkana MVP

## Objetivo
Restaurar capacidade de venda com MTTR < 30 min. Prioridade: checkout e webhook.

## Fontes de verdade
- Application Insights (workspace-based) — queries KQL.
- Sentry — erros front e functions.
- Mercado Pago — status de pagamentos.

## Severidades
- **P0**: indisponibilidade checkout ou 5xx contínuos (>=3/min)
- **P1**: webhook sem eventos 15 min
- **P2**: falhas intermitentes ou latência >1s

## Procedimentos
### P0
1. `requests | where resultCode between (500..599) | summarize by operation_Name`
2. Health check Functions: `/create-preference` 200 em <800ms.
3. Rollback último deploy se necessário.
4. Se bug confirmado: hotfix, tag, `CHANGELOG.md`.

### P1
1. Verificar fila do provedor e assinatura do webhook.
2. Reprocessar evento manualmente com payload de teste.
3. Checar idempotência (não duplicar pedido).

### P2
1. Inspecionar taxas por método de pagamento.
2. Habilitar apenas Pix/3DS como mitigação.
3. Abrir tarefa para ajuste fino.

## Boas práticas
- Logs sem PII. Não gravar cartões, CPF, endereço completo.
- Idempotência por `paymentId` + HMAC.
- Alertas testados com dados sintéticos.

## Encerramento
Escreva post-mortem curto (5 itens): causa, impacto, mitigação, correção, prevenção.
