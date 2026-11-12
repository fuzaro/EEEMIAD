# 07. Catalog of Diagnosed Anti-Patterns
## Critical Hazards in AI Software Engineering (§6 and §11)

---

### 1. Structural Anti-Patterns (§6)

#### §6.1 Ratify-and-Write
- **Symptom:** Proposing an architectural choice in the same document that marks it accepted, circumventing deliberate debate and counter-argument.
- **Remediation:** Drafts are always initialized as `status=proposed`. Acceptance requires an independent reflective review or human sign-off.

#### §6.2 Composite Release with Heterogeneous Risk
- **Symptom:** Packaging a low-risk documentation fix together with an irreversible database migration or token rotation under a single release tag.
- **Risk:** Reviewers approve the release based on the triviality of the first part, missing the existential risk of the second.
- **Remediation:** The homogeneous risk principle: destructive changes deploy alone.

#### §6.3 Idempotency-as-False-Safety
- **Symptom:** Labeling a shell script as "idempotent" to reassure the team, when individual sub-steps perform irreversible actions (such as credential rekeying).
- **Remediation:** Idempotency defines *convergent final state*, not "safe-to-rerun". The pre-flight checklist must evaluate the blast radius of each sub-action, not the wrapper.

#### §6.4 Soft Gate Without Promotion Criteria
- **Symptom:** Introducing a new security gate in non-blocking "best-effort" mode without locking the exact calendar date or sample size for enforcing it.
- **Consequence:** Morphs into perpetual technical debt.
- **Remediation:** Every shadow gate is bound to an automated cut-over trigger.

#### §6.5 Spec Prescribing What Already Exists
- **Symptom:** Specifications describing already-deployed services using forward-looking phrasing like "it is proposed to implement".
- **Remediation:** Phase 8 sweeps ensure specifications maintain active present-tense living parity.

#### §6.6 Hierarchy Inversion (Anti-Pattern 10.7)
- **Symptom:** Code deviates from the specification; instead of fixing the code or raising an ADR, the specification is watered down to match the defect.
- **Remediation:** Upward reconciliation mandate: specification and ADRs govern code. Code never wins simply because it is deployed.

#### §6.7 Config-as-State Outside Source Control
- **Symptom:** Critical control parameters, access gates, or routing flags living solely in ephemeral runtime variables or manual operator memories.
- **Remediation:** *"If it governs behavior, it lives in Git source control."*

#### §6.8 Capitulation to the Convenient Layer
- **Symptom:** When investigating a drift between layers, accepting the first easy explanation without checking higher-level governing ADRs.
- **Remediation:** Always verify against the highest authoritative document governing the domain.

---

### 2. The §11 Dialectic: Permanent Improvisation vs. Permanent Governance

```
               [ THE DANGER ZONE ]
      Permanent Improvisation (§11a)
      - No specs, no ADRs, no contracts
      - LLM improvises on every prompt
      - Human becomes a perpetual bug debugger
      - Collapse via hallucination & spec-rot
                    ▲
                    │  (The Dialectical Tension)
                    ▼
      Permanent Governance (§11b)
      - Paralyzing ceremonial overhead
      - Infinite audits that never ship to prod
      - Specifications so dense they cost more than code
      - Abstraction leverage = 0
               [ THE DANGER ZONE ]
```

> **The EEEMIAD Balance Point:**  
> We do not practice governance for bureaucratic vanity. Specifications must be **dense enough to extinguish structural hallucination**, yet **abstract enough to maintain agent leverage**. All governance checks are automated as mechanical queries.
