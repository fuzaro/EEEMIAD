# 🧰 Harness · TypeScript adapter

*The three mechanical closure checks of ch. 08 for Next.js / TypeScript projects (PT: adaptador TypeScript)*

The Python harness one level up reads Python code through the AST. A project in another language needs an adapter that keeps the **same contract**. This one covers Next.js App Router routes and Vitest/Jest suites. It reads code by pattern, not by a full TypeScript AST; the patterns are narrow (exported route handlers, `describe`/`it` calls, `*_MODE` flag names) and every script prints what it examined.

| Script | Contract (same as Python) | TypeScript specifics |
|---|---|---|
| [`verify_hierarchy_ts.py`](verify_hierarchy_ts.py) | Code ↔ Spec ↔ ADR ↔ Plan; flags ↔ ledger | Routes from `<api-root>/**/route.ts` exports; `[id]` maps to `{id}`; parity is **bidirectional** |
| [`check_falsification_ts.py`](check_falsification_ts.py) | R2 per group; debts counted apart | Group = `describe`; debt = `it.fails` (Vitest's strict xfail); `.skip`/`.todo` reported, never evidence |
| [`sweep_ts.py`](sweep_ts.py) | Phase 8: ghost flags, forbidden symbols, env vars ↔ deploy spec | Distinguishes a ghost flag from a flag *awaiting its arc* by reading the ledger |

```bash
python3 examples/verification-harness/typescript/verify_hierarchy_ts.py --project-root . --api-root app/src/app/api --flags-file app/src/server/flags.ts
python3 examples/verification-harness/typescript/check_falsification_ts.py --test-dir tests
python3 examples/verification-harness/typescript/sweep_ts.py --src app/src --specs specs
```

Every script prints `EEEMIAD harness <version>` from its `HARNESS_VERSION` constant. A project that copies these files records their origin and version (ch. 08 §8.3) and runs them, with its own checks, behind one gate command ([`../gate.sh`](../gate.sh) is the starting point).

Expected layout: `Plan/docs/` (or `plan/`), `Plan/decisions/` (or `adr/`), `specs/` with an enforcement ledger whose rows start with `` | `NAME_MODE` ``, and a flags module declaring every flag. Paths are flags, not assumptions.

> [!NOTE]
> The adapter was extracted from a validation-by-use of EEE (a legacy system rebuilt arc by arc). Writing it exposed that the original Python verifier reported success without examining code; both are now held to the rule *a verifier that examines nothing must not report success*.
