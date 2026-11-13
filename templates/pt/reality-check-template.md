# 🔎 REALITY-CHECK · [Alvo]

*Primeiro artefato antes de qualquer edição: o terreno é o que o documento assume?*

```yaml
target: [ADR-XXX | charter ARC-XXX | spec]
author_role: [quem constrói]
date: YYYY-MM-DD
git_head_sha: [sha curto]
environment: [local | staging | produção]
verdict: [GREENLIGHT | DRIFT_DETECTED | BLOCKED]
```

---

## 1. Âncoras verificadas (símbolo, não linha — R14)

| Âncora citada | Estado real observado | Status | Evidência (comando) | Nível R15 |
|---|---|---|:---:|---|
| `modulo.py::funcao_x` | existe; assinatura `(a, b, *, tenant)` | ✅ OK | `python -c "import ast..."` | 1 |
| tabela `schema.tabela` | inexistente no banco alvo | ❌ DRIFT | `\dt schema.*` | 3 |
| `FLAG_X="enforce"` | presente no manifesto; **0 consumidores no código** | ❌ FANTASMA | sweep AST | 2 |

## 2. Afirmações de estado do documento ("X já aplicado", "infra estável")

| Afirmação | Verificada? | Como | Resultado |
|---|:---:|---|---|
| "credencial de serviço existe" | ❌ | `secret-store get svc/credential` | não existe → **precondição de estado falha** |

## 3. Relatório de desvios (drift report)

- **Desvio 1:** [descrição, camada em que foi medido, impacto].
- **Recomendação:** [subir para emenda de ADR | prosseguir com ajuste de spec | bloquear].

## 4. Veredito

- [ ] **GREENLIGHT** · âncoras confirmadas, precondições satisfeitas, mecanismo da fase existe (R26).
- [ ] **DRIFT_DETECTED** · divergência material; o documento volta a quem decide antes de qualquer edição.
- [ ] **BLOCKED** · ambiente inalcançável para medir; **proibido inferir** (não certificável).
