# AGENTS.md · [Project]

<!--
Entry-point template (EEEMIAD ch. 08 §8.2). Save as AGENTS.md at the project root.
Each tool's own files (e.g. CLAUDE.md, .cursor/rules/, .github/copilot-instructions.md,
skills and agent definitions) are adapters: they only point to this file and to the canonical folder.
The project's gate checks that this file cites only paths that exist.
-->

Instructions for people and for coding agents of any tool. This file is the **canonical entry point**; each tool's files only point here and to `eee/`.

## What this repository is

[One sentence about the system and the stack.]

## Reading order before acting

1. `eee/state/STATE.md`: the operational state (dated). Check it against the environment before acting.
2. `eee/state/decisions-operator.md`: the operator's fixed decisions. Do not reopen them.
3. The arc's charter (`specs/charters/`), the spec it cites and the ADR that governs the spec.
4. The procedure for your role in `eee/playbooks/`.

## Hierarchy of truth

| Layer | Where | Rule |
|---|---|---|
| 1 · Plan | `Plan/docs/` | purpose, invariants, budgets |
| 2 · ADR | `Plan/decisions/` | born `PROPOSED`; ratified by whoever decides, in a separate commit |
| 3 · Spec | `specs/` | 1:1 contract with the code; charters in `specs/charters/` |
| 4 · Code | [`src/`, `tests/`] | follows the spec; divergence is resolved in the layer above |

## Hard rules

1. [Private data: what never enters the repository.]
2. **Secrets never enter the repository or a message.** The state records where each credential lives, never its value.
3. **Writing to a shared environment needs two keys:** the operator's decision and their authorization in the acting session.
4. **Red test before green**, with disagreeable pair and probe-and-revert recorded.
5. **Flag and ledger in the same commit.**
6. **Journal in the same commit:** every relevant state change gets a line in `eee/log.md`.
7. **Declared proof level** (R15) on every claim about state.
8. **Humans close `done@gate`.**

## Commands

```bash
tools/gate.sh            # single gate: every verifier; a missing dependency fails it
[how to start test dependencies]
[how to run the application locally]
```

## Map of `eee/`

| Path | Content |
|---|---|
| `eee/state/` | operational state, operator decisions, environments |
| `eee/playbooks/` | per-role procedures, without tool or model names |
| `eee/kit/` | copied EEEMIAD templates, with origin and version in `eee/kit/VERSION` |
| `eee/log.md` | evidence journal, permanent |
