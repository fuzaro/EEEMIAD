# 🧾 LEDGER DE ENFORCEMENT · [Sistema]

*Registro vivo de cada flag: o que governa, em que estado está, como falha e quem decidiu*

> [!IMPORTANT]
> **Invariante de manutenção:** todo flip de flag ou mudança de postura **edita este ledger no mesmo commit** do manifesto ou do código. Um flip sem entrada aqui é um furo de governança.

```yaml
system: [nome]
updated: YYYY-MM-DD
head_sha: [sha curto]
```

Legenda · Estado: `OFF` `SHADOW` `ENFORCE` `RETIRED` · Postura: **FC** fail-closed e loud · **FO-D** fail-open com buffer durável · **FO** fail-open (⚠ em gate) · n/a não é gate

| Flag | Default (código) | Valor (deploy) | Estado | Garantia | Postura de falha | ADR | Última RC (nível R15) |
|---|---|---|---|---|---|---|---|
| `EXEMPLO_READ_AUTH_MODE` | `off` (`config.py:71`) | `"enforce"` (`deploy.yaml:112`) | **ENFORCE** | leituras exigem credencial | tri-estado: inválido=401 · dependência=503 **FC** | ADR-012 | nível 4, 2026-07-10 |
| `EXEMPLO_AUDIT_SINK_MODE` | `off` | `"shadow"` | **SHADOW** | evento gravado durável | **FO-D** (buffer) | ADR-014 | nível 2 |
| `EXEMPLO_LEGACY_STUB_ENABLED` | `false` | `"false"` | **OFF** ✅ | stub aposentável | n/a | ADR-009 | zero consumidores em `tests/` |

## Flags fantasma detectadas (Fase 8)

| Flag | Declarada em | Consumidores (AST) | Ação |
|---|---|---|---|
| `EXEMPLO_AUTH_ENABLED` | `config.py:43` | **0** | remover ou dar consumidor |

## Não-flags que se comportam como gate

| Item | Estado | Postura | Ref |
|---|---|---|---|
| chave de assinatura persistida | ✅ | restart preserva sessões | ADR-0xx |
