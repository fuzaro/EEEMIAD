# REALITY-CHECK: [Brief / Mudança Alvo]
## Primeiro Artefato Emitido pelo Agente Executivo (§4.4)

```yaml
brief_reference: BRIEF-[XXX]
author: Agente Executivo (Code)
execution_date: YYYY-MM-DD
git_head_sha: [sha curto]
environment: [local-dev | cluster-staging | CI]
verdict: [GREENLIGHT | DRIFT_DETECTED | BLOCKED]
```

---

## 1. Verificação de Âncoras Citadas no Brief

| Âncora Citada no Brief | Estado Real Observado no Código | Status | Evidência (Comando / Linha Real) |
|---|---|:---:|---|
| `caminho/arquivo.py:L120` | Função existe na linha 134 (drift de 14 linhas) | ✅ OK | `grep -n "def nome_funcao"` |
| `saturn.users` (tabela) | Tabela inexistente no schema do banco | ❌ DRIFT | `\dt saturn.*` (tabela não encontrada) |
| `OIDC_ENABLED="true"` | Variável ativa no Nomad template | ✅ OK | `nomad job inspect ...` |

---

## 2. Relatório de Desvios (*Drift Report*)
> *Se algum arquivo, assinatura ou precondição divergir do assumido pelo Brief, documente aqui antes de tocar em qualquer código.*

- **Desvio 1:** [Descrição do desvio e impacto na implementação].
- **Recomendação do Executor:** [Voltar ao Cowork para emenda de ADR ou prosseguir com ajuste de linha].

---

## 3. Veredito de Pré-Voo
- [ ] **GREENLIGHT:** Âncoras confirmadas, precondições de estado satisfeitas, seguro para codar.
- [ ] **DRIFT_DETECTED:** Divergência material encontrada; brief pausado para reavaliação do Cowork.
