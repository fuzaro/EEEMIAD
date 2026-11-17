# 🔬 05 · The Rules of Empirical Refinement

*The anatomy of the "plausible answer family" and the rules that follow from it*

---

## 1. The diagnosis

> **Plausible answer to the wrong question:** a computation that returns a **well-formed, valid, typed** value for a question that **was not asked**, becoming **indistinguishable from the correct answer**.

The defect is never a malformed value. It is the value **right for another question**. That is why it passes human review and shallow tests: **it looks like an answer**.

The form was observed, in the ecosystem of origin, across seven distinct layers, and the most instructive layer was the last: **the family appeared inside the instruments built to detect it**.

| Layer | Typical form of the instance |
|---|---|
| **Code** | A security gate that correctly validates permission over a subject **supplied by the caller itself**. A `success` response with synthetic counts masking a transport failure. An authorization check against a non-existent relation returning a `deny` identical to a legitimate `deny`. |
| **Data** | A constant score written to thousands of records and read as a measurement. A provenance attribute of "learned" over scaffold data. `anchored:false` over an empty segment: a claim without a subject. |
| **Spec** | A capability marked "Real" for something not yet implemented. |
| **Test corpus** | A perimeter test green because it measured the divergence of a disabled shadow. A test true **for the wrong reason**: the fixture never wrote the tuple. |
| **ADR** | A justification "based on Phase 1 evidence" and, in the same section, the admission that the metric "was not instrumented". |
| **Measuring instrument** | An unfiltered aggregate, a diluted denominator, a gap measured against the predecessor instead of the sibling. |
| **Exit criterion** | A green gate reachable only by conforming to the ceiling that suppressed most observations. Such a gate does not err alone: it **ratifies** the error it measures. |

## 2. The decalogue (R1 to R10)

### R1 · A boolean in a three-state domain is the family's signature
Whenever a field must say *"no subject"* or *"unknown"* and only has `true`/`false`, the `false` becomes a lie: `allowed:false` for an invalid credential; `success:false` for a transport failure.
**Remedy:** explicit ternary domains: `real | curated | unknown`, `permit | deny | unauthenticated`, `invalid (401) | dependency unavailable (503)`.
**Corollary (R22):** the third state is **absence of evidence**, never *"evidence of an extreme value"*. Five identical samples legitimately produce zero variance: there is evidence, and maximal; what is missing is dispersion. Coercing the extreme into "absence" creates a new false negative with the fix of the old false positive.

### R2 · Every measurement carries a pair that must agree
It was the **pair** that exposed the error in every observed case, never the isolated value: time zero *versus* post-isolation; probe with a valid credential *versus* control with an invalid one; `occurred_at` *versus* `recorded_at`.
> *A measurement without a disagreeable companion is not a measurement; it is a claim.*

**Corollary (R27):** a pair that degenerates into a mirror **exactly under the failure it should detect** is not a pair. The instrument declares, in its own verdict, in which regime it is a pair and in which it is not.

### R3 · Evidence of existence is not evidence of reach
Endpoint implemented ≠ route reachable over the network. Token minting open ≠ credential accepted downstream. Service answering on `127.0.0.1` ≠ traffic routable between containers. A correct artefact **with no path to a consumer** is not detectable by inspecting the artefact.

### R4 · Before reading time series, name the generating process
Rate drops and silence windows may reflect the periodicity of a batch job or shard rotation. No p-value is valid without the generating process's calendar beside it.

### R5 · Rates normalize by real opportunities, not total operations
If the denominator includes thousands of trivial operations, `0/793` looks safe when the critical path was exercised **twice**. Normalize by confrontation opportunities. **Inverse (R29):** the denominator of a debt register is the **declared**, never the **pending**; if settling a debt shrinks the register, the metric punishes fixing. *Check:* does the denominator move when the numerator moves? Then the metric measures itself.

### R6 · Not exercised ≠ passed
A gate that did not run was not approved. Zero defects under an insufficient sample is an **inconclusive result**, never evidence of stability.

### R7 · Fail-closed protects decisions; fail-open protects evidence
When the component **decides authorization**, failing means closing. When the component guards **the integrity of the record of something that already happened**, closing destroys the record: refusing the write does not undo the event, it erases the proof. The audit log adopts **fail-open with a durable buffer**. This is the half missing from every failure-mode matrix that only tabulates gates.

### R8 · Assertions about code are syntactic (AST), never textual
Prose fools text search: `REVOKE` in a comment looks like an active revocation; a docstring citing `is_platform_admin` looks like a call. Automated checks on structure operate on the **syntax tree**. **Corollary (R14):** an anchor is a **symbol**; a line is a convenience. A symbol is verifiable and does not decay; a line decays every commit and the decay emits no signal.

### R9 · Correcting a premise requires sweeping every decision that rested on it
If an amendment changes a topological premise ("there are now two writers instead of one"), the author audits and updates every decision and spec deduced from the previous premise, including within the same document.

### R10 · In an audit that does not converge, order by rate of degradation
Ordering by "theoretical severity" breeds paralysis. Order by **what gets worse while it waits**: a corpus degrading on every submission or a log lying on every run takes priority over cosmetic refactoring. It is the operational antidote to permanent governance.

## 3. Derived construction rules

The following rules were born in later arcs and directly govern [evolutionary construction](06-evolutionary-construction.md):

| Rule | Statement |
|---|---|
| **R11 · Property, not mechanism** | Whoever decides specifies the **property** and the **refutation condition**; the query belongs to whoever executes. Prescribing *how to measure* is already mechanism. |
| **R15 · Ground-truth level** | Every state claim declares its level: **1** intent (versioned file) · **2** applied intent (registered job) · **3a** state in the test process · **3b** state in the deployment artifact (the image or package that ships) · **4** state and effect (live reproduction). Packaging defects (a dynamically loaded dependency, a file read from disk) only show up at 3b. A claim without a level is read as 4 and is usually 1. Level 4 also declares whether the reproduction **reads** or **writes**: a write into an environment holding business data uses data marked as test and removable, or stays out (the write property is then proven at 3b, and level 4 covers reads only). |
| **R26 · The phase mechanism exists** | Before planning a flip, verify syntactically that the `enforce` path **exists in the code**. Naming the phase in the ADR does not build it. |
| **R28 · The test name declares the property measured** | A test called "flag lives in source" that pins a specific value measures **posture**, not **visibility**: it fails on a legitimate flip and passes on a ghost flag with the right value. |
| **R29b · Negative debt in `xfail(strict)`** | A negative assertion recorded as `xfail(strict=True)` is, for free, a **closure detector**: when the defect is fixed, it turns `XPASS` and announces its own settlement. Debt is always recorded `strict`. |
| **R30 · Whoever decides also describes** | Every table, flag or job created under an ADR enters the spec in the same arc. Deciding without describing yields documentation that is true about what was decided and false about what exists. |

## 4. Two forms that organize measurement

### Negative capacity × negative provisioning
- **Cannot reach with what it receives** (provisioning): missing grant, tuple, credential.
- **Cannot reach even if it tries** (capacity): the barrier is structural.

Only the second proves a security limit. Reporting the first as the second is the family with a big number.

### Exit criterion in edge form, not node form
A node criterion (*"no fail-open on a gate"*) is structurally incapable of seeing a surface **without** a gate. Edge criterion: *"no execution reaches tenant data, authorization mutation or administrative privilege beyond its authorized access, verified from inside the cluster"*. The second catches the paths the first cannot see.
