# 📐 ADR-[XXX] · [Short, imperative decision title]

```yaml
status: PROPOSED # PROPOSED | ACCEPTED | REJECTED | DEPRECATED | SUPERSEDED
date: YYYY-MM-DD
deciders: [deciding role, human operator]
hierarchy_layer: ADR
governs: [specs/component.md]
justified_by: [Plan/docs/principles.md §Principle X]
replaces: [] # e.g. [ADR-012]
eee_phase: 2 # 2 (contract) | 6 (abstraction after repetition)
ratified_by: null # separate artefact citing evidence, SHA and R15 level — whoever proposes does not ratify
```

---

## 1. Context and empirical evidence

- **Empirical origin:** [finding, red test or incident, with date and reference].
- **Observed symptom:** [precise description; ground-truth level R15].
- **Affected principles:** [Plan principles impacted].

## 2. Decision

- **D1 · [title]:** [imperative rule].
- **D2 · [title]:** [imperative rule].
- **D3 · Failure posture (M11):** [fail-closed for decisions; fail-open with durable buffer for evidence].
- **D4 · Flag and phases:** [`FLAG_X ∈ {off, shadow, enforce}`, default `off`; exit gate per phase].

## 3. Alternatives considered (≥ 2)

| Alternative | Pros | Cons | Ruling |
|---|---|---|:---:|
| **A ·** [description] | [advantage] | [drawback] | **REJECTED** |
| **B (selected) ·** [description] | [advantage] | [drawback] | **ACCEPTED** |
| **C ·** [description] | [advantage] | [drawback] | **REJECTED** |

## 4. Accepted consequences

- **Positive:** [security, integrity, decoupling gains].
- **Negative / accepted costs:** [complexity, latency, migration effort].

## 5. Contract surface introduced (explicit contracts)

- **New invariants:** [rules that may never be violated].
- **Access control:** [required policies].
- **Mandatory audit:** [events emitted].
- **Spec to update in the same arc (R30):** [tables, flags, jobs created by this decision].

## 6. Preconditions and dependent sweep

- **State precondition:** [tuples, tables, variables that must exist before code]. Verification command: `[command]`.
- **Decisions resting on the changed premise (R9):** [list to review].
