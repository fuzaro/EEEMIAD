# 05. The Ten Empirical Refinement Rules (R1 to R10)
## Anatomy of the "Plausible Answer Family"

---

### 1. The Diagnosis: The Plausible Answer Family

> **Definition:**  
> A computation that returns a **well-formed, valid, and properly typed** value for a question that **was never asked**, rendering it **indistinguishable from the correct answer**.

The defect is never a broken syntax error or an unhandled crash. The defect is that the value is **correct for a different question**. Consequently, it passes human pull request reviews and glides through shallow automated test suites: **because it looks like an answer**.

#### The 11 Historic Empirical Instances by Layer:
1. **Code Layer:** Security admission gate fed with caller-supplied `subject` in request JSON body (gate passed, but evaluated a fabricated subject).
2. **Code Layer:** OpenFGA `check` against non-existent relation returning a `deny` identical to a legitimate access denial.
3. **Code Layer:** Endpoint returning `status=success` with fabricated `tokens_used=142` masking transport failure.
4. **Data Layer:** Constant `quality_score=0.8` recorded across 6,301 rows being read as live empirical telemetry.
5. **Data Layer:** `prior_source="kin"` recorded over scaffolding mocks, claiming Bayesian learning where only placeholders existed.
6. **Data Layer:** `anchored:false` recorded over an empty segment (an assertion lacking a subject).
7. **Specification Layer:** Document claiming `authorized ANN: Real` for vector search capabilities that were not yet coded.
8. **Test Layer:** Security perimeter test passing green because it measured divergence against a dormant shadow engine.
9. **Test Layer:** Assertion passing for the wrong reason: the test fixture never seeded the target tuple into the database.
10. **ADR Layer:** ADR-011 justifying a wall "per Phase 1 evidence" while admitting in the same section that the metric was "NOT instrumented".
11. **Telemetry Layer:** The very monitoring probes built to detect anomalies carried diluted denominators that converted non-exercised paths into false proofs of safety.

---

### 2. The Ten Operational Rules (R1 to R10)

#### R1 — A Boolean in a Three-State Domain is the Family Signature
Whenever a field must represent *"no subject"* or *"unknown state"* and offers only `true`/`false`, `false` mutates into a lie:
- `allowed:false` for an invalid credential (conflating policy denial with transport authentication failure).
- `success:false` for transport failure.
- **Remediation:** Enforce ternary enums: `real | curated | unknown` or `permit | deny | unauthenticated`.

#### R2 — Every Measurement Carries a Disagreeable Pair
In every empirical case observed, it was the **pair of metrics** that surfaced the lie, never a single metric in isolation:
- `t0` versus `pos_estanque`.
- Probe with literal dev token versus probe with malformed bearer.
- `occurred_at` versus `recorded_at`.
> **Golden Rule:** *A measurement lacking a counter-balancing companion is not a measurement; it is an assertion.*

#### R3 — Evidence of Existence is Not Evidence of Reachability
- Endpoint implemented in Python $\ne$ route reachable over the service mesh.
- Token mint endpoint open $\ne$ credential accepted downstream.
- Service responding on `127.0.0.1` $\ne$ reachable across container networking.

#### R4 — Before Reading Production Time Series, Name the Generating Process
Drops in success rates or windows of silence can simply be artifacts of hourly batch jobs or model shard rotations. No p-value or variance metric is valid without aligning it against the batch schedule.

#### R5 — Race Rates Normalize by Opportunities, Not by Total Operations
If the denominator includes thousands of trivial filler operations, a failure rate of `0/793` appears statistically significant, when in reality the race window was only exercised **2 times**. Always normalize against true conflict opportunities.

#### R6 — Unexercised $\ne$ Passed
A gate that did not run did not pass. Zero failures under an insufficient sample size is merely an **inconclusive observation**, never proof of stability.

#### R7 — Fail-Closed Protects Decisions; Fail-Open Protects Evidence
- When a component guards an **authorization decision**, the failure mode must strictly be **Fail-Closed**.
- When a component guards the **integrity of an audit trail of an event that already occurred**, Fail-Closed destroys evidence (refusing to log deletes the proof of the event). Audit streams must adopt **Fail-Open with durable append-only buffers**.

#### R8 — Assertions on Code are Syntactic (AST), Never Textual
Docstrings and comments deceive text-based searches (*grep/regex*):
- A comment containing `REVOKE admin` looks like an active revocation to grep.
- A docstring mentioning `is_platform_admin` looks like an executed guard.
> **Mandate:** Automated code verifications operate strictly upon the **Abstract Syntax Tree (AST)**.

#### R9 — Correcting a Premise Demands Sweeping All Dependent Decisions
If an amendment updates an underlying topology assumption (e.g., "we now have two writers instead of one"), the author must audit and reconcile every dependent ADR and specification in the cascade.

#### R10 — In a Non-Converging Audit, Order by Rate of Degradation
When faced with dozens of open findings, ordering by theoretical "severity" breeds analysis paralysis. Order instead by **what degrades while you wait**: databases accumulating corrupt rows or logs lying with every invocation take absolute priority over cosmetic refactoring.
