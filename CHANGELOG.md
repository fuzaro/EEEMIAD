# Changelog

All notable changes to EEEMIAD are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [1.7.0] — 2026-11-17

A beginner's path into EEE: one command creates a new project, and one short chapter tells what to do next.

### Added
- **`starter/eee_init.py`**: creates a new project ready for EEE. Governance tree; `AGENTS.md` and a thin `CLAUDE.md` adapter; request, request × arc matrix, one-page Plan, operational state, operator decisions and evidence journal, already named after the project; templates and verifiers copied with origin and version (`eee/kit/VERSION`); single gate (`tools/gate.sh` + `tools/gate.env`). Inputs (database layout, screens, UX template) are copied into `Plan/docs/insumos/` or, with `--private`, only inventoried (name, size, hash) and left outside. It runs the gate once and records the real result as journal entry #1; never overwrites a file; refuses an existing EEE project. PT and EN; tests in `starter/test_eee_init.py`.
- **Ch. 12 Getting started** (PT and EN): prerequisites, the command, what it creates, the request, five stages driven by a coding agent with the text to paste and what the human approves, the daily routine and common problems. Ch. 08 §1 step 1 points to it.
- Templates (PT and EN): `request-template` (with the question-phase questions), `request-matrix-template`, `foundational-plan-template`, `operational-state-template`, `operator-decisions-template`.
- `gate.sh`: `HARNESS_LANG=py|ts` selects the Python verifiers or the TypeScript adapter.

### Changed
- `agents-entry-template`: the reading order includes the request item (`request_item`, matrix), as v1.6.0 required.
- `HARNESS_VERSION` 1.7.0 in every harness script.

## [1.6.0] — 2026-11-17

The remaining proposals from the validation by use (one gap in scope, two frictions in testing, one gap in live proof, one pre-flight question that caught a real defect).

### Added
- **Request × delivered** (gap L4). Ch. 08 step 2 keeps the original request in the requester's words and a request × arc matrix (each item → an arc or an explicit exclusion). The closure checklist and the Phase 8 ritual (item 10) re-read the request against the matrix: gates measure properties of code, not whether the requested code exists. Charter template: `request_item`.
- **Each battery declares the state it starts from** (friction A9). Ch. 06 §4: a stateful battery declares and prepares its own starting state (isolated database or fixture loaded in the file); shared undeclared state makes suites sabotage each other. P1 checklist line.
- **Probe-and-revert under defence in depth** (friction A10). Ch. 06 §4: the probe declares the layers it removes; each redundant layer gets a test that exercises it alone; a probe that removes every layer confirms the battery sees the property. Glossary updated.
- **Target state covered** (pre-flight question 7). Ch. 04 Phase 7: is the target environment in a state the tests never exercised (empty, just migrated, old data outside a new rule, volume)? If so, run the battery from that state before the flip. Cut-over evidence template row 7; P4 checklist.

### Changed
- **R15 level 4 declares read or write** (gap L5). Ch. 05 R15, ch. 06 §4 and the cut-over evidence template: a write into an environment holding business data uses data marked as test and removable, or stays out; a read-only level 4 does not prove the write property. P4 checklist and glossary updated.

## [1.5.0] — 2026-11-17

Driven by the same validation-by-use, after adoption: the state needed to continue the project lived only in one agent session's memory, and a copied R2 detector had fallen behind the published one, unnoticed for days because the verifiers ran one by one.

### Added
- Ch. 08 §8 **Continuity: journal, state and single gate**.
  - §8.1 **Evidence journal (permanent):** one line per relevant state change, in the same commit, with command and result; the method-finding column continues after adoption.
  - §8.2 **Operational state and harness-neutral instructions:** `AGENTS.md` as the single entry point, canonical content in neutral Markdown, tool-specific files as thin adapters checked by the gate, agent memory as a shortcut and not a source, no secret values in state.
  - §8.3 **Single gate and copied tools:** one command for every verifier, failing (never skipping) on a missing dependency; copied tools and templates declare origin and version.
- `templates/{pt,en}/evidence-journal-template.md` and `templates/{pt,en}/agents-entry-template.md`.
- `examples/verification-harness/gate.sh`: a starting single gate (hierarchy, R2, required dependencies, project suite) with tests.
- `HARNESS_VERSION` in every harness script, printed on each run; a test keeps the five scripts on the same version.
- Glossary: *evidence journal*, *operational state*, *harness adapter*, *single gate*.

### Changed
- Ch. 08 §1 step 1: the governance tree gains the "operations" rows (`AGENTS.md`, `eee/log.md`, `eee/state/`, `tools/gate.sh`); step 8 and the closure checklist refer to the single gate and the journal line.
- Ch. 08 §4 Phase 8 ritual: run the single gate; check copied tools against their declared version; journal and state up to date. Ch. 04 Phase 8 mirrors it.
- Ch. 08 §5: harness-neutral instructions as an attachment point for AI agents.

## [1.4.0] — 2026-11-15

### Added
- Ch. 08 §7 **Execution across sessions (optional)**: six rules learned from running the pre-flight, deploy and rollback of a validation-by-use from a second session that held the cluster credential: execute where the terrain and the credential are; the secret does not travel; the message is a closed packet; two keys to act; sent is not read; the peer's claim is information. Plus state that does not survive a restart, and a checklist per round.
- Task packet template: `executes_at` and `action` (`read-only | write`).
- Glossary: *two keys*.

The concrete protocol for agent sessions (message template, correction, routing) is in EEEMIAD-dual 0.3.0.

## [1.3.0] — 2026-11-14

### Added
- Ch. 08 §6 **Task division by context level (optional)**: off by default, enabled only by the operator's *yes* at the questions phase and recorded in the charter (`delegation: none | tiered`). Three levels (local, module, system), an objective classification rule (*no mechanical gate → cannot be local*), blind checking against the gate, escalation after two failures, oracle by another author, and a per-packet record to measure whether the division saves anything.
- `templates/{pt,en}/task-packet-template.md`.
- Charter template: `delegation` field. Arc checklist: the question is asked and recorded.
- Glossary: *task packet*, *context level*.

The instantiation with agents and language models is in the sibling repository EEEMIAD-dual (v0.2.0).

## [1.2.0] — 2026-11-14

Driven by a validation-by-use: a legacy system was rebuilt arc by arc following this repository to the letter, and every point where the method helped, cost extra or stayed silent was logged. The changes below are what that log asked of the method.

### Fixed
- **`verify_hierarchy.py` no longer reports success without examining anything.** It failed open in three ways: it returned "100% compliant" when no code directory existed; it read metadata only from `---` frontmatter, so it never read the status of ADRs written in the template's own ```yaml form (including the reference example's); and it did not check Spec → ADR or ADR → Plan despite its docstring. It now fails when no code is found (`--allow-missing-code` for Phase 2), reads both metadata forms, strips inline comments, checks `governing_adr`, `justified_by` and `governs`, and always prints the counts it examined.
- **`check_falsification.py` counts R2 per group.** A test class (or a module's top-level tests) needs its own negative control; one negative test no longer vouches for a whole file. Strict `xfail` is counted as declared debt; a non-strict `xfail` is reported, since an unexpected pass would go unnoticed.

### Added
- `examples/verification-harness/typescript/`: the three closure checks for Next.js / TypeScript (`verify_hierarchy_ts.py` with bidirectional route parity, `check_falsification_ts.py` with `it.fails` as debt, `sweep_ts.py` that tells a ghost flag from one awaiting its arc).
- Harness tests covering each fix, including *a verifier that examines nothing must fail*.
- `templates/{pt,en}/cutover-evidence-template.md`: pre-flight answered, deployment artifact exercised (level 3b), live reproduction (level 4), flip and ledger, window, decision.
- Ch. 06 §3 **Flags in greenfield**: surface vs rule flags, `shadow` only with a named oracle carrying its own negative control, bi-state `off | enforce` when no runtime oracle exists.
- M11 doctrine 5: **delivery with mandatory evidence** (evidence precedes delivery; a production failure after recording keeps the record).
- Ch. 08: anonymization gate in the arc-opening checklist; `synthetic` provenance; level 3b step before the flip; **executor change** as a trigger to re-run the whole battery; harness language coverage stated.
- Glossary entries (PT/EN) for the new terms.

### Changed
- R15 level 3 split into **3a** (state in the test process) and **3b** (state in the deployment artifact): packaging defects only show at 3b.

## [1.1.0] — 2026-11-13

### Changed
- **Scope narrowed to the EEE itself.** The dual-agent instantiation (reflective/executive roles, briefs, pre-flight reality-check, decision-by-decision evaluation) moved to the sibling repository **EEEMIAD-dual**. EEE now describes three role-neutral responsibilities (decide, build, verify).
- **Generic examples.** Platform-specific service names, flags, commit hashes and numbers were removed from chapters 03, 05, 07 and 10; cases are told by their *form* and the rule that catches them.
- **Deeper construction chapter.** New chapter 06 *Evolutionary Construction: Stubs, Mocks, Flags and Arcs* with the arc lifecycle, the five scaffold rules, the flag contract and its pathologies, test integration through the arc, and the evolutionary expansion loop.
- **Academic grounding.** Chapter 09 rewritten with a referenced bibliography (Peirce, Popper, Fisher, Neyman–Pearson, Boehm, Parnas–Clements, Hoare, Dijkstra, Meyer, Saltzer–Schroeder, Perrow, Gilb, Fowler, Meszaros, Humble–Farley, Hodgson, Nygard, Basili, Kitchenham, Goodhart, Angles, Wilson, Huang, Kadavath) and an honest statement of the internal p₀ measurement (0.51 → 0.62 as an **upper bound**, not a universal constant).
- **Refinement rules extended.** Chapter 05 adds the construction-oriented rules R11, R15, R22, R26, R27, R28, R29, R29b and R30, and the two measurement forms (negative capacity vs provisioning; edge-form exit criteria).
- **Formal Markdown fixes.** Page heads normalised (single H1 + italic subtitle), LaTeX blocks that broke rendering replaced by plain text or ```math fences, consistent chapter icons and GitHub alerts.

### Added
- `docs/*/11-glossario.md` / `11-glossary.md`.
- `examples/evolutionary-arc/`: runnable pure-Python arc (`off → shadow → enforce`) with fault injection, negative control against loosening and a strict `xfail` debt register.
- Templates: `arc-charter-template.md`, `flag-ledger-template.md` (PT/EN).
- `assets/eeemiad-banner.svg`.

### Removed
- `docs/*/06-dual-agent-workflow.md`, `templates/*/brief-template.md`, `templates/*/evaluation-ledger-template.md`, `skills/eee-architect`, `skills/eee-executor` (moved to EEEMIAD-dual).

## [1.0.0] — 2026-09-28
- Initial public release: methodology docs (PT/EN), templates, skills, verification harness and reference implementation.
