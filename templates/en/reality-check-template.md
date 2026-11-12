# REALITY-CHECK: [Target Brief / Change]
## First Deliverable Emitted by the Executive Agent (§4.4)

```yaml
brief_reference: BRIEF-[XXX]
author: Executive Agent (Code)
execution_date: YYYY-MM-DD
git_head_sha: [short sha]
environment: [local-dev | cluster-staging | CI]
verdict: [GREENLIGHT | DRIFT_DETECTED | BLOCKED]
```

---

## 1. Verification of Anchors Cited in Brief

| Anchor Cited in Brief | Real State Observed in Codebase | Status | Evidence (Command / Real Line) |
|---|---|:---:|---|
| `path/file.py:L120` | Function exists at L134 (14-line drift) | ✅ OK | `grep -n "def function_name"` |
| `saturn.users` (table) | Table missing in database schema | ❌ DRIFT | `\dt saturn.*` (table not found) |
| `OIDC_ENABLED="true"` | Variable active in Nomad job | ✅ OK | `nomad job inspect ...` |

---

## 2. Drift Report
> *If any file, function signature, or precondition differs from brief assumptions, document here before touching code.*

- **Drift 1:** [Description of drift and implementation impact].
- **Executor Recommendation:** [Return to Cowork for ADR amendment or proceed with offset].

---

## 3. Pre-Flight Verdict
- [ ] **GREENLIGHT:** Anchors confirmed, state preconditions satisfied, safe to proceed with edits.
- [ ] **DRIFT_DETECTED:** Material divergence surfaced; brief paused for Cowork reassessment.
