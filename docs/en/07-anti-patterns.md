# ⚠️ 07 · Catalogue of Anti-patterns

*The measured and named traps of AI-assisted software engineering*

---

## 1. Why a catalogue

Naming the form once is worth more than fixing eleven instances. Every entry below was **observed and measured** before receiving a name; the catalogue grows by evidence, not by analogy.

## 2. Decision and document anti-patterns

### §6.1 · Ratify-and-write
- **Symptom:** proposing a decision in the same document that declares it approved. Verbal symptom: *"decisions already taken, this plan only writes the rationale"*.
- **Remedy:** drafts are born `PROPOSED`; ratification is a separate artefact citing evidence, SHA and proof level. Whoever proposes does not ratify.

### §6.5 · Spec prescribing what already exists
- **Symptom:** "it is proposed to build" for something delivered months ago. Confuses plan with reality.
- **Remedy:** the Phase 8 sweep synchronizes tense and status (`Active / Living`).

### §6.6 · Hierarchy inversion
- **Symptom:** code drifts from the spec; the spec is altered to forgive the shortcut.
- **Remedy:** upward reconciliation ([03](03-hierarchy-of-truth.md)). Code never wins by already being deployed.

### §6.8 · Capitulation to the convenient layer
- **Symptom:** when auditing a drift, accepting the first easy explanation ("the docstring said X") without checking whether an ADR above revoked the clause. One side capitulates, issues a *mea culpa*, and the real drift is masked as "a mistake".
- **Remedy:** every reconciliation claim declares its authoritative layer and confirms against the **highest** one that speaks on the matter.

### Architecture decided implicitly in an implementation plan
- **Symptom:** protocol or topology appear as a presupposition in a plan, without their own ADR. The implementation fixes the design before the debate.
- **Remedy:** every decision that constrains future alternatives has an ADR.

## 3. Release and operations anti-patterns

### §6.2 · Composite release with heterogeneous risk
- **Symptom:** cosmetic refactoring and destructive migration under the same tag. The reviewer approves for the triviality of the first and misses the risk of the second.
- **Remedy:** risk homogeneity: destructive or security changes travel alone.

### §6.3 · Idempotent as false safety
- **Symptom:** a script labelled "idempotent" performs key rotation or an irreversible migration as a side effect.
- **Remedy:** idempotency means *convergent final state*, not "safe to rerun" nor "reversible". The pre-flight enumerates the effects of **each step**, not of the wrapper. "Idempotent" is a yellow flag.

### §6.4 · Soft gate without promotion criterion
- **Symptom:** a gate introduced in non-blocking mode without a date, sample volume or metric that makes it blocking. Becomes perpetual debt.
- **Remedy:** every flag in `shadow` is born with an exit gate declared in the charter.

### §6.7 · Critical state outside the source (config-as-state)
- **Symptom:** a flag, job or posture governing behaviour that lives only at runtime or in the operator's memory. A redeploy reverts it silently.
- **Remedy:** *if it governs behaviour, it lives in the versioned source*, including the cut-over flip from the cut-over commit.

### Unexercised flip composition
- **Symptom:** several gates flip in the same window, each with a pre-flight of its own caller, none with a pre-flight of the **product**. The gate breaks the **question**, not the answer, and there is no way out from inside.
- **Remedy:** a composition item in the pre-flight: which other gates changed, and whether their product was exercised with command and result.

## 4. Scaffold and flag anti-patterns

### Mock that becomes a measurement
- **Symptom:** a constant value produced by a stub written into production data and read as live telemetry.
- **Remedy:** per-attribute provenance (`real | curated | unknown`); historical radius measured before de-mocking.

### Silent fallback to a stub
- **Symptom:** a transport failure returns `status=success` with synthetic counts because the stub path took over.
- **Remedy:** stub behind a flag with default off, explicit value and loud log; honest error (`503`) when the dependency falls.

### Ghost flag
- **Symptom:** flag declared in configuration, zero consumers in code.
- **Remedy:** Phase 8 AST sweep; the flag is removed or gains a consumer.

### Existence without a path
- **Symptom:** the artefact exists and is correct, but there is no path from it to a consumer. Review looks inside the piece and does not see it.
- **Remedy:** exit criterion in edge form; trace to the consumer. A control exposed in an interface without a consumer **fabricates trust**.

### Benign collapse
- **Symptom:** two distinct states collapse into one observable, and the survivor is the one that **requires no action**. A parameter whose seed coincides with the implemented behaviour is undetectable by observation.
- **Remedy:** only a **discordant** value tests it. The disagreeable pair here is not optional; it is the only probe that discriminates.

## 5. Measurement and test anti-patterns

### Test green for the wrong reason
- **Symptom:** the assertion passes because the fixture never wrote the data, or because it measures the divergence of a disabled shadow.
- **Remedy:** *probe-and-revert*: inject the exact defect and confirm the red before accepting the green.

### Name declaring one property, assertion measuring another
- **Symptom:** a test "flag lives in source" pinning a specific value. Fails on a legitimate flip; passes on a ghost flag with the right value.
- **Remedy:** the assertion measures the property the name declares (R28).

### Denominator that moves with the numerator
- **Symptom:** a debt register that counts only the pending; settling shrinks the register and the corpus punishes fixing.
- **Remedy:** the denominator is the **declared** (R29).

### Corroboration with a common ancestor
- **Symptom:** N artefacts agree, all descending from the same enumeration. Weight of one, appearance of N.
- **Remedy:** independence of origin before counting agreement.

## 6. The §11 dialectic: improvisation × governance

```
          [ DEATH ZONE ]                           [ DEATH ZONE ]
    Permanent improvisation (§11a)           Permanent governance (§11b)
    · no specs, ADRs, contracts              · endless ceremonies
    · the LLM improvises on every prompt     · audits that never converge in a deploy
    · the human becomes a perpetual debugger · spec as dense as the code
    · collapse by hallucination and spec-rot · abstraction leverage = 0
                     ╲                             ╱
                      ╲   ◆ equilibrium point     ╱
                       ╲  spec dense enough to eliminate
                          structural hallucination, abstract
                          enough to preserve leverage;
                          governance executable by scripts
```

> **EEE does not seek bureaucracy out of academic vanity.** The operational antidote to permanent governance is R10 (order by rate of degradation) and a Phase 8 executed by scripts, not meetings.
