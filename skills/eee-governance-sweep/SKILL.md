---
name: eee-governance-sweep
description: Skill for the Phase 8 Evolutionary Governance Sweep. Detects dead code, orphan routes, unmanaged config-as-state, and spec-code drift via AST analysis.
version: 1.0.0
author: EEEMIAD
---

# EEE Governance Sweep Skill (Phase 8 Sweep)

## Purpose
The **EEE Governance Sweep Skill** automates the periodic health checks of the repository at the end of each release or sprint. It enforces entropy reduction, catches spec-rot early, and flags unratified architectural shortcuts.

## When to Activate
- At the conclusion of every development sprint or release cycle.
- Prior to tagging a new major or minor version.
- When preparing a brownfield codebase for formal EEEMIAD adoption.

## Checklist Executed by this Skill
1. **Route Parity Check:** AST extraction of all FastAPI/web routes cross-referenced 1:1 against living specifications.
2. **Ghost Flag Audit:** Detection of environment variables read by `os.getenv` or `config.py` that lack documentation in living specifications.
3. **M11 Coverage Scan:** Ensuring every public endpoint has an explicit entry in the failure mode matrix.
4. **ADR Aging Review:** Flagging any ADR left in `status=proposed` for more than 30 days without activity.
5. **Double-Entry Ledger Balancing:** Ensuring all identified findings are logged in the active backlog or marked `closed` with verifiable commits.
