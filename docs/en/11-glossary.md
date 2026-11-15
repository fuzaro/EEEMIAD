# 📖 11 · Glossary

*EEE terms in short definitions, with the chapter where each is developed*

---

| Term | Definition | See |
|---|---|---|
| **Arc** | Stretch of work that takes **one property** from "does not exist" to "on and measured", under a flag, opening with a charter and closing with a measurable gate and evidence. | [06](06-evolutionary-construction.md) |
| **Charter** | Opening contract of an arc: target property, refutation condition, flag, failure posture, exit gate, observation window. | [06](06-evolutionary-construction.md), [template](../../templates/en/arc-charter-template.md) |
| **Refutation condition** | Concrete observation that, if it occurs, proves the arc did **not** deliver the property. Without it there is no arc, there is intent. | [06](06-evolutionary-construction.md), [09](09-academic-foundation.md) |
| **Thin (vertical) slice** | Minimal implementation crossing every layer once (input → processing → output), with stubs allowed and tagged. | [04](04-cycle-phases.md) |
| **Minimum link** | Synonym of thin slice in Phase 3: the smallest end-to-end coupling that proves the pipe. | [04](04-cycle-phases.md) |
| **Stub / Mock / Fake / Dry-run** | Test doubles and scaffolds. They prove shape contracts and flow; they do **not** prove value. "The mock validates the pipe, not the measurement." | [06](06-evolutionary-construction.md) |
| **De-mock** | Replacement of a stub by the real implementation, one collaborator at a time, without changing the shape contract. | [06](06-evolutionary-construction.md) |
| **True shapes** | Property of a mock whose return is reproducible by the real implementation; exit criterion of Phase 2. | [04](04-cycle-phases.md) |
| **Flag** | Operational anchor of an arc; a contract with a neutral default in code, explicit value in deployment, domain `off \| shadow \| enforce`, M11 posture and a ledger row. | [06](06-evolutionary-construction.md) |
| **Shadow** | State in which the component computes the decision and records the divergence against current behaviour, **without deciding**. | [04](04-cycle-phases.md) |
| **Enforce** | State in which the component decides; M11 failure posture active. | [04](04-cycle-phases.md) |
| **Cut-over** | Flip from `shadow` to `enforce`, under mandatory pre-flight. | [04](04-cycle-phases.md) |
| **Pre-flight (blast radius)** | Mandatory block before any action touching production: side effects, reversibility, rehearsed rollback, state precondition, flip composition. | [04](04-cycle-phases.md), [08](08-application-guide.md) |
| **Flip composition** | Pre-flight question: which other gates changed in this window and whether their **product** was exercised. | [07](07-anti-patterns.md), [10](10-illustrative-cases.md) |
| **Ghost flag** | Flag declared in configuration with zero consumers in code, with its arc already closed. Before P1, a consumer-less flag is "awaiting its arc". | [06](06-evolutionary-construction.md), [07](07-anti-patterns.md) |
| **Enforcement ledger** | Living register of every flag: default, deployment value, state, guarantee, failure posture, ADR. Changes in the same commit as the flip. | [06](06-evolutionary-construction.md), [template](../../templates/en/flag-ledger-template.md) |
| **Config-as-state** | Anti-pattern: behaviour governed by state that lives only at runtime, outside the versioned source. | [07](07-anti-patterns.md) |
| **M11 (failure-mode matrix)** | Table declaring, per interface and error condition, the degradation posture (fail-closed, fail-open with durable buffer) and the expected response. | [05 R7](05-refinement-rules.md), [template](../../templates/en/failure-modes-m11-template.md) |
| **Fail-closed / durable fail-open** | Failure postures: the first protects a **decision**; the second protects **evidence** of something that already happened. | [05 R7](05-refinement-rules.md) |
| **Tri-state** | Response domain distinguishing `invalid` (401), `denied` (403) and `could not verify` (503). A boolean here is the family's signature. | [05 R1](05-refinement-rules.md) |
| **Plausible answer family** | Well-formed, typed value for a question that was not asked, indistinguishable from the correct answer. | [05](05-refinement-rules.md) |
| **Disagreeable pair** | Second measurement that can **disagree** with the first. "A measurement without a disagreeable companion is not a measurement; it is a claim." | [05 R2](05-refinement-rules.md) |
| **Negative control** | Test that must **fail** (or bar) to prove the positive assertion measures something. Includes the neighbour that must stay barred. | [06](06-evolutionary-construction.md) |
| **Probe-and-revert** | Inject the exact defect the test exists to catch, confirm the red, revert; only then accept the green. | [06](06-evolutionary-construction.md) |
| **Proof test** | Deliberate exercise, on a declared cadence, of a contingency mechanism whose only organic trigger is the failure it handles. | [04 Phase 8](04-cycle-phases.md) |
| **Ground-truth level (R15)** | 1 intent · 2 applied intent · 3 state · 4 state and effect. Every state claim declares its own. | [05](05-refinement-rules.md) |
| **Reality-check (RC)** | Measurement of the terrain against what a document assumes: anchors verified by symbol, preconditions at the source, drift reported before any edit. | [08](08-application-guide.md), [template](../../templates/en/reality-check-template.md) |
| **Upward reconciliation** | Resolution of drift by escalating to the higher layer (amendment ADR), never by adjusting the spec to the code. | [03](03-hierarchy-of-truth.md) |
| **Hierarchy inversion** | Anti-pattern: the spec is altered to forgive the code's shortcut. | [03](03-hierarchy-of-truth.md), [07](07-anti-patterns.md) |
| **Closure by re-evaluation** | A task closes when the verification that detected the deficit is re-run and returns zero; never on self-report. | [02](02-principles.md) |
| **DONE@tier** | Declared tier of completion: `structural`, `functional`, `gate`, `purpose`. A bare "done" is forbidden. | [02](02-principles.md) |
| **Guarantee mode** | Deterministic, threshold + confidence, or shape/judgement. Limits the reachable tier. | [02](02-principles.md) |
| **Fidelity × leverage** | Central tension: denser spec → more faithful materialization → less leverage. The target is the point where the residue of improvisation is cheap to verify. | [01](01-overview.md) |
| **Sprint-exit sweep (Phase 8)** | Mechanical end-of-cycle sweep: AST for ghosts, routes ↔ specs parity, ADR custody, `PROPOSED` ageing, proof tests. | [04](04-cycle-phases.md), [08](08-application-guide.md) |
| **Surface flag / rule flag** | A surface flag governs a route or resource (`off` → `404`); a rule flag governs a check inside an existing path (`off` → not evaluated). | [06 §3](06-evolutionary-construction.md) |
| **Named oracle** | Independent pair that `shadow` compares against when there is no current behaviour: another implementation, a hand-written query, an invariant or a fixture. Carries its own negative control. | [06 §3](06-evolutionary-construction.md) |
| **Anonymization gate** | Arc-opening line when real data is private: shape-only census, synthetic base, sentinel scan = 0 before the first commit. | [08 §3](08-application-guide.md) |
| **Executor change** | A change of person, agent or model mid-work; triggers a full re-run of the battery before accepting earlier reports. | [08 §4](08-application-guide.md) |
| **Proof levels 3a / 3b** | R15 level 3 split: 3a is state in the test process, 3b is state in the deployment artifact. Packaging defects only show at 3b. | [05](05-refinement-rules.md) |
| **Task packet** | A task closed for dispatch: allowed inputs, forbidden reads, output contract, mechanical gate and refutation. Exists only when the operator accepted the context-level division. | [08 §6](08-application-guide.md), [template](../../templates/en/task-packet-template.md) |
| **Context level (local / module / system)** | How much a task must read. Decides who executes and who checks; a task without a mechanical gate cannot be local. | [08 §6](08-application-guide.md) |
| **Two keys** | Cross-session execution rule: a remote write needs the decision in the requesting session **and** the operator's authorization in the acting session. | [08 §7](08-application-guide.md) |
| **Bamboo chime** | Metaphor of purpose: infrastructure that disappears when it works and returns attention to the human. | [00](00-manifesto.md) |
