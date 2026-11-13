---
name: eee-adversarial-verifier
description: Instantiates the EEE role "who verifies". Generates an adversarial test suite strictly from the specification, the governing ADR and the M11 matrix, without reading the implementation, so that self-consistent errors cannot grade themselves.
version: 1.1.0
author: EEEMIAD
---

# 🔍 EEE Adversarial Verifier (blind verification)

## Purpose
When the same author (human or model) writes spec, code and tests, **consistently wrong** cases pass verification and stay invisible inside "verified". This skill breaks that ceiling by operating with **complete blindness to the implementation**: it receives only the living specification, the governing ADR and the M11 failure-mode matrix.

## When to activate
- Before promoting an arc from `shadow` to `enforce` (Phase 7 cut-over).
- Before merging any Phase 4 hardening change on a security or audit boundary.
- During Phase 8 sprint-exit sweeps.

## Core rules
1. **Blindness invariant.** Never read implementation files. If one is present in context, ignore its logic.
2. **Derive strictly from contracts.** Every assertion maps to an explicit invariant, status code, schema field or M11 row.
3. **Disagreeable pair (R2).** For every positive assertion, write the negative control; for every loosening, the neighbour that must stay barred.
4. **Assert M11 postures.** Decision gates fail closed (`401/403/503`, never a default identity); evidence sinks fail open with a durable buffer (nothing discarded).
5. **Test names declare the property measured (R28).**
6. **Debts are `xfail(strict=True)` (R29b).** A property the spec promises but the arc has not yet delivered is recorded strict, so its settlement announces itself.

## Deliverables
1. An isolated suite in `tests/adversarial/` (e.g. `test_spec_compliance.py`).
2. A verification summary: assertions tested, negative controls, M11 rows covered, **ambiguous contract clauses** that require an ADR clarification (never resolved by guessing).

## Prompt
See [`prompts/blind_test_generator.md`](prompts/blind_test_generator.md).
