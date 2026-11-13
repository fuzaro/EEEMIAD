# 🔍 10 · Illustrative Cases

*How the rules show up in real incidents, told generically*

> [!NOTE]
> The cases below are distilled from incidents measured in EEE's ecosystem of origin. Service names, flags and exact numbers were removed on purpose: what matters is the **form** of the defect and the rule that catches it. Any multi-tenant platform with agents reproduces these forms.

---

## Case 1 · Three correct flips and twelve days of silence

**Form:** unexercised composition.

**What happened.** In the same deployment window, three security gates flipped from `shadow` to `enforce`: a write lock on the audit chain, a token requirement on the inference service and strict admission on the authorization service. Each flip had its own pre-flight, green tests and a responsible author. An hourly batch job that queried the authorization service to find out **who was the administrator** of an account sent no credential header. Under strict admission it started receiving `403`. The orchestrator marked each run `dead`, and **no alarm sounded**: the gate broke the **question**, not the answer. Daily task volume fell to zero for twelve days.

**What caught it.** A time-series reading with the generating process named (R4): the job is hourly, the silence was continuous, not periodic.

**Rules.**
- The pre-flight gains the **composition** item: which other gates flipped in this window, and whether the **product** was exercised with command and result.
- Rehearsed reversal: the flag went back to `shadow` in one commit; the ledger was updated in the same commit.
- The batch job's credential was provisioned **before** the new flip (state precondition), with the verification command recorded.

## Case 2 · The audit sink that erased the proof

**Form:** fail-closed where it should have been durable fail-open (R7).

**What happened.** An audit-write endpoint started returning `422` because of a decorator-order defect: the wrong function was bound to the route. The task that generated the event **proceeded**; the record of what happened in the world **was not written**. Hundreds of events were lost over a window of hours, with no visible error on the main path.

**What caught it.** A disagreeable pair (R2): count of events emitted by the producer *versus* count of records written by the sink.

**Rules.**
- An access decision fails **closed**; an evidence sink fails **open with a durable buffer**: the message goes to a persistent queue and is never discarded.
- The M11 matrix gained the missing half: failure modes of **sinks**, not only of gates.
- Negative control: a test with a corrupted payload proves the alert fires **without** aborting the chain of custody.

## Case 3 · The caller that declared itself internal

**Form:** plausible answer (classic instance) and evidence of existence without reach (R3).

**What happened.** The orchestrator read the caller type **from the request body**. An external client sending `"caller_type": "internal"` skipped the risk classifier and the tenant's quotas. The gate worked perfectly: it validated permissions over a subject **supplied by the attacker**.

**What caught it.** A reality-check with the adversarial probe: the same forged request went from `500` with the gate skipped to `403` blocked by the classifier after the arc.

**Rules.**
- Identity is derived **from the signed token at every hop**, never from the payload. Identity fields in the body are rejected (`422`).
- The arc followed `off → shadow → enforce` with an explicit flag and ledger; the living matrix of cases (legitimate internal, declared-but-unproven internal, external) became a tested decision table.
- Exit criterion in **edge** form: "no execution reaches tenant data beyond its authorized access, verified from inside the cluster".

## Case 4 · The stub that became production

**Form:** silent fallback to a stub; mock that becomes a measurement.

**What happened.** When transport to the downstream service failed, a stub path took over and returned `status=success` with a response text, a fixed token count and a synthetic audit reference. The caller never saw the failure. Elsewhere in the same system, a scaffold wrote a constant quality score to thousands of records, read downstream as live measurement.

**What caught it.** In both, a disagreeable pair: count of **distinct** values *versus* count of records (thousands of rows, **one** distinct value).

**Rules.**
- The stub was placed behind a flag with default `off`, explicit value and a loud boot log. Transport failure returns `503` with no `answer`.
- **Historical radius measured** before the fix: no real task had consumed the stub (zero sentinels across hundreds of tasks). The number entered the closure.
- Per-attribute provenance: `real | curated | unknown`; the scaffold stopped injecting values.
- Verifiable retirement trigger: the flag leaves only when the search for references in the tests returns empty.

## Case 5 · The flag that did nothing

**Form:** ghost flag and non-existent `enforce` path (R26).

**What happened.** An ADR planned the phase "flip to enforce" for a read-authentication mode. When briefing the phase, it turned out the module only emitted a *warning*: the denial path **did not exist**. In another service, an authentication flag was declared in configuration with **zero consumers** in the code.

**What caught it.** A **syntactic** assertion about the mechanism (R8): an AST search for consumers of the flag and for the denial branch, before writing the brief item.

**Rules.**
- Naming the phase in the ADR does not build it: verify the mechanism before briefing.
- The Phase 8 sweep lists flags declared without a consumer; each is removed or gains a consumer.

## Case 6 · The debt that announced its own settlement

**Form:** debt register as closure detector (R29b).

**What happened.** A negative assertion (*"policy mutation does **not** require a credential"*) was recorded as debt in `xfail(strict=True)`. When admission was implemented in another arc, the test turned `XPASS` and **failed the suite**: the debt register reported that the debt had been settled, without anyone having designed that.

**Rule.** Negative debt is always recorded `strict`: it is the `strict` that makes the register work in both directions. In an arc where the measuring instruments lied five times, it was the only one that announced good news nobody asked for.

## What the six cases have in common

| Case | The value looked like... | ...but was |
|---|---|---|
| 1 | Three correct gates | An unexercised product |
| 2 | A correctly rejected request | Destroyed proof of an event |
| 3 | A gate validating permission | A subject forged by the caller |
| 4 | Success with telemetry | A stub answering for a transport failure |
| 5 | A configurable control | A flag with no consumer |
| 6 | A test "failing as expected" | A property already true |

In all of them, **the pair of values exposed it**, never the isolated value. That is why R2 is the central rule of empirical refinement.
