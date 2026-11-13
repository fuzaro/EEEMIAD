# Changelog

All notable changes to EEEMIAD are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/).

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
