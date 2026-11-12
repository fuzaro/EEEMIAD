# ADR-[XXX]: [Short and Imperative Decision Title]

```yaml
status: PROPOSED # [PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED]
date: YYYY-MM-DD
deciders: [Reflective Agent (Cowork), Human Operator]
hierarchy_layer: ADR
governs: [specs/target-service.md]
justified_by: [Plan/docs/framework-principles.md §Principle X]
replaces: [] # E.g.: [ADR-012]
eee_phase: 2 # Phase 2 (Contracts) or Phase 6 (Abstraction)
```

---

## 1. Problem Context and Empirical Evidence
> *What concrete defect was observed in runtime or specification?*
> *What was the measured blast radius or security integrity risk?*

- **Empirical Origin:** [Cite finding, failing test, or live incident with commit/date].
- **Observed Symptom:** [Precise failure description].
- **Affected Principles:** [Plan-layer principles impacted].

---

## 2. Architectural Decision
> *What technical choice is formally adopted?*

- **D1 ([Sub-decision Title]):** [Imperative rule statement].
- **D2 ([Sub-decision Title]):** [Imperative rule statement].
- **D3 ([M11 Failure Posture]):** [Explicit Fail-Closed vs Fail-Open with Durable Log definition].

---

## 3. Alternatives Considered

| Alternative | Pros | Cons | Ruling |
|---|---|---|:---:|
| **Option A:** [Description] | • [Advantage] | • [Disadvantage] | **REJECTED** |
| **Option B (Selected):** [Description] | • [Advantage] | • [Disadvantage] | **ACCEPTED** |
| **Option C:** [Description] | • [Advantage] | • [Disadvantage] | **REJECTED** |

---

## 4. Accepted Consequences

### Positive
- [Gains in security, integrity, isolation, or decoupling].

### Negative / Incurred Costs
- [Additional complexity, network overhead, latency budget, or migration cost].

---

## 5. Contract Surface Introduced (§7)
- **New Invariants:** [Hard rules that must never be broken].
- **Access Control:** [Required RBAC / OpenFGA relation tuples].
- **Mandatory Audit:** [Emitted audit subjects].

---

## 6. Preconditions and Implementation Pre-Flight
- **State Precondition:** [Tuples, tables, keys that must exist before code].
- **Verification Command:** `[command]`
