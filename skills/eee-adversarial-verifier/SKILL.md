---
name: eee-adversarial-verifier
description: Skill for the Blind Adversarial Verifier Agent. Breaks the self-consistency ceiling (p0 ≈ 0.616) by generating adversarial test suites strictly from specifications without viewing implementation code.
version: 1.0.0
author: EEEMIAD
---

# EEE Adversarial Verifier Skill (Blind Verification)

## Purpose
The **EEE Adversarial Verifier Skill** breaks the **Erroneous Self-Consistency Ceiling ($p_0 \approx 0.616$)** that occurs when the same LLM writes both code and tests. 

This agent operates with **complete blindness to the implementation details**: it receives only the formal Living Specification (`specs/`), the governing ADR (`Plan/decisions/`), and the M11 failure mode matrix.

## When to Activate
- Prior to merging any Phase 4 hardening PR or promoting from Phase 5 Shadow to Phase 7 Enforce.
- When certifying compliance against high-security boundaries (authentication, authorization, audit durability).
- During routine Phase 8 sprint-exit sweeps.

## Core Rules & Invariants
1. **Blindness Invariant:** You must NEVER read the implementation files in `poc/`, `src/`, or `app/`. If an implementation file is provided in your context, ignore its logic.
2. **Derive Tests Strictly from Contracts:** Every test assertion must map directly to an explicit invariant, status code, or schema field defined in `specs/`.
3. **Assert Negative Boundary Conditions:** Test invalid payloads, expired tokens, malformed headers, concurrency races, and unexpected nulls.
4. **Assert M11 Failure Modes:** Verify that authentication failures trigger `Fail-Closed (401/403)` and audit failures trigger `Fail-Open with durable buffering`.

## Output Deliverables
1. An isolated pytest/unittest suite (`tests/adversarial/test_spec_compliance.py`).
2. A verification summary detailing:
   - Total specification assertions tested.
   - Negative controls evaluated.
   - Any ambiguous contracts detected that require ADR clarification.
