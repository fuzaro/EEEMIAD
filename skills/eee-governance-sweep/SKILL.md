---
name: eee-governance-sweep
description: Runs the EEE Phase 8 sprint-exit sweep. Detects ghost flags, orphan routes, spec-code drift, config-as-state and decision-record custody gaps via AST analysis, never via text search.
version: 1.1.0
author: EEEMIAD
---

# 🧹 EEE Governance Sweep (Phase 8)

## Purpose
Keep entropy low and stop spec-rot from regenerating. The sweep is **mechanical**: AST extraction and parity checks, executed by script, so that governance consumes machine time instead of human attention.

## When to activate
- At the end of every sprint or release cycle.
- Before tagging a version.
- Before retiring a flag (end of an arc).
- When preparing a brownfield codebase for EEE adoption (Stage 1 census).

## Checklist
1. **Route parity.** AST extraction of all HTTP routes, cross-referenced 1:1 against living specs, in both directions.
2. **Ghost flags.** Environment variables and flags declared in configuration or manifests with **zero consumers** in code.
3. **Phase mechanism exists (R26).** For every flag in `shadow`, the `enforce` branch exists syntactically.
4. **Ledger parity.** Every flag in code and manifest has a row in the enforcement ledger with default, deploy value, state, posture and ADR.
5. **M11 coverage.** Every public endpoint and every evidence sink has a row in the failure-mode matrix, and each row has a fault-injection test.
6. **Decision-record custody (R13, R14).** Every ADR cited exists on the main branch; every `file:line` anchor in decision documents resolves to the symbol named beside it.
7. **ADR ageing.** Decisions left in `PROPOSED` beyond the declared window are promoted, amended or cancelled.
8. **Unexercised gates (R6) and proof tests.** Contingency mechanisms whose only organic trigger is the failure they handle are exercised deliberately, on a declared cadence.
9. **Debt register (R29b).** `xfail(strict)` tests that turned `XPASS` are promoted; the debt denominator counts declared, not pending (R29).

## Script
`scripts/sweep_codebase.py` extracts routes and environment variables via AST:

```bash
python3 skills/eee-governance-sweep/scripts/sweep_codebase.py --src ./src --specs ./specs
```
