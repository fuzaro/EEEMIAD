# 🧾 ENFORCEMENT LEDGER · [System]

*Living record of every flag: what it governs, its state, how it fails and who decided*

> [!IMPORTANT]
> **Maintenance invariant:** every flag flip or posture change **edits this ledger in the same commit** as the manifest or code. A flip without a row here is a governance hole.

```yaml
system: [name]
updated: YYYY-MM-DD
head_sha: [short sha]
```

Legend · State: `OFF` `SHADOW` `ENFORCE` `RETIRED` · Posture: **FC** fail-closed and loud · **FO-D** fail-open with durable buffer · **FO** fail-open (⚠ on a gate) · n/a not a gate

| Flag | Default (code) | Value (deploy) | State | Guarantee | Failure posture | ADR | Last RC (R15 level) |
|---|---|---|---|---|---|---|---|
| `EXAMPLE_READ_AUTH_MODE` | `off` (`config.py:71`) | `"enforce"` (`deploy.yaml:112`) | **ENFORCE** | reads require credential | tri-state: invalid=401 · dependency=503 **FC** | ADR-012 | level 4, 2026-07-10 |
| `EXAMPLE_AUDIT_SINK_MODE` | `off` | `"shadow"` | **SHADOW** | event durably recorded | **FO-D** (buffer) | ADR-014 | level 2 |
| `EXAMPLE_LEGACY_STUB_ENABLED` | `false` | `"false"` | **OFF** ✅ | retirable stub | n/a | ADR-009 | zero consumers in `tests/` |

## Ghost flags detected (Phase 8)

| Flag | Declared in | Consumers (AST) | Action |
|---|---|---|---|
| `EXAMPLE_AUTH_ENABLED` | `config.py:43` | **0** | remove or give it a consumer |

## Non-flags that behave as gates

| Item | State | Posture | Ref |
|---|---|---|---|
| persisted signing key | ✅ | restart preserves sessions | ADR-0xx |
