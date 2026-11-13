# 🔎 REALITY-CHECK · [Target]

*First artefact before any edit: is the ground what the document assumes?*

```yaml
target: [ADR-XXX | charter ARC-XXX | spec]
author_role: [builder]
date: YYYY-MM-DD
git_head_sha: [short sha]
environment: [local | staging | production]
verdict: [GREENLIGHT | DRIFT_DETECTED | BLOCKED]
```

---

## 1. Anchors verified (symbol, not line — R14)

| Anchor cited | Observed reality | Status | Evidence (command) | R15 level |
|---|---|---|:---:|---|
| `module.py::func_x` | exists; signature `(a, b, *, tenant)` | ✅ OK | `python -c "import ast..."` | 1 |
| table `schema.table` | missing in target database | ❌ DRIFT | `\dt schema.*` | 3 |
| `FLAG_X="enforce"` | present in manifest; **0 consumers in code** | ❌ GHOST | AST sweep | 2 |

## 2. State claims in the document ("X already applied", "infra stable")

| Claim | Verified? | How | Result |
|---|:---:|---|---|
| "service credential exists" | ❌ | `secret-store get svc/credential` | missing → **state precondition fails** |

## 3. Drift report

- **Drift 1:** [description, layer where measured, impact].
- **Recommendation:** [escalate to ADR amendment | proceed with spec adjustment | block].

## 4. Verdict

- [ ] **GREENLIGHT** · anchors confirmed, preconditions satisfied, phase mechanism exists (R26).
- [ ] **DRIFT_DETECTED** · material divergence; the document returns to the decider before any edit.
- [ ] **BLOCKED** · environment unreachable to measure; **inference forbidden** (not certifiable).
