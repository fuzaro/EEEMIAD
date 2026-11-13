# Specification · Audit Sink (evolutionary-arc example)

```yaml
component: audit-sink
status: Active
governing_adr: ADR-EXAMPLE-arc (illustrative)
flag: AUDIT_SINK_MODE
```

## 1. Property

Every audit event emitted by the application is durably recorded, even when the downstream audit store is unavailable.

**Refutation condition:** an event accepted by the application that is neither stored nor present in the durable buffer refutes the arc.

## 2. Flag contract

| Attribute | Value |
|---|---|
| Default in code | `off` (behaviour-neutral) |
| Domain | `off \| shadow \| enforce` |
| Deploy value | explicit in the manifest, even when equal to the default |
| Out-of-domain value | hard error at boot (never silent fallback) |
| Ledger row | see `templates/en/flag-ledger-template.md` |

## 3. Behaviour by state

| State | Who decides | Real adapter | Scaffold provenance | Intent log |
|---|---|---|---|---|
| `off` | stub | not called | `scaffold` | — |
| `shadow` | stub | called, result logged | `scaffold` | `stub_ok` vs `real_ok` (disagreeable pair) |
| `enforce` | real | decides | `real` | — |

## 4. M11 failure-mode row

| Operation | Error condition | Failure class | Degradation posture | Observable |
|---|---|---|---|---|
| `record(event)` in `enforce` | store unavailable | transient | **Fail-open with durable buffer** (R7) | `stored=false`, event in buffer, loud log line |
| `record(event)` in `shadow` | store unavailable | transient | product unaffected; divergence logged | `intent_log[-1].diverged == true` |
| boot | flag outside domain | hard | **Fail-closed** at boot | `FlagError` |

## 5. Exit gate

- `shadow`: zero divergences over ≥ N real opportunities (N declared in the charter), with the generating process named (R4).
- `enforce`: fault-injection battery green; live reproduction of the property and of the refutation (ground truth level 4).
- Flag retired only after the declared observation window and when `grep -rl AUDIT_SINK_MODE tests/` returns nothing outside this example.
