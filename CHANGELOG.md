# Changelog

All notable changes to EEEMIAD are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

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
