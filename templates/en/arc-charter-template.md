# 📜 CHARTER · [Arc name]

*Opening contract of an EEE arc: property, refutation, flag, postures and exit gate*

```yaml
arc_id: ARC-[XXX]
governing_adr: ADR-[XXX] (status=ACCEPTED)
target_spec: specs/[component].md
flag: [FLAG_NAME]
flag_domain: [off | shadow | enforce]
flag_default_in_code: off
delegation: none # none | tiered: only after the operator's yes at the questions phase (08 §6)
request_item: [item of the request × arc matrix this arc serves, in the request's words (08 §1 step 2)]
opened: YYYY-MM-DD
owner: [deciding role or person]
```

---

## 1. Target property (R11: property, not mechanism)

> *"[One verifiable sentence. E.g. no tenant resource read is served without a valid credential.]"*

## 2. Refutation condition

> *"[Concrete observation that, if it occurs, refutes the arc. E.g. a request without a bearer that receives 200.]"*

Without this item the arc does not open.

## 3. Failure posture (M11 row)

| Operation | Error condition | Posture | Observable response |
|---|---|---|---|
| `[op]` | dependency unavailable | **Fail-closed** (decision) or **Fail-open with durable buffer** (evidence) | `[503 / buffer + loud log]` |

## 4. Phases and gates

| Phase | Deliverable | Gate to advance |
|---|---|---|
| **P1 · Thin slice (flag off)** | Complete mechanism, behaviour-neutral, tagged stubs | (1)(2)(3) battery green; debts in `xfail(strict)`; ledger and spec updated |
| **P2 · Shadow** | Intent log with disagreeable pair; divergence detection; queryable exit criterion | 0 refutations over ≥ **N = [__]** real opportunities; generating process named |
| **P3 · Hardening** | De-mock per collaborator; one M11 row per failure mode, each with an injection test | Stub's historical radius measured; verifiable retirement trigger |
| **P4 · Cut-over** | Complete pre-flight; flip and ledger in the same commit | Live reproduction of the property **and** of the refutation (level 4) |

## 5. Cut-over pre-flight (fill before the flip)

```
1. Side effects beyond the target:            ______
2. Reversible? [YES/NO] (if NO → STOP):       ______
3. Rehearsed rollback (command + time):       ______
4. State precondition (command + output):     ______
5. Composition: other gates in this window?   ______
   Product exercised? (command + result):     ______
6. Enforce mechanism exists? (AST assertion): ______
```

## 6. Observation window and retirement

- Post-enforce window before removing the flag: `[__ opportunities | __ weeks]`
- Command proving zero consumers of the flag: `grep -rl [FLAG] src/ tests/` → empty

## 7. Closure

```yaml
closed: YYYY-MM-DD
deficit_query: "[query/test that detected the deficit]"
deficit_result: 0
done_tier: done@functional
ground_truth_level: 4
```
