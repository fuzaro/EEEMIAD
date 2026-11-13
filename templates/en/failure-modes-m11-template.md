# 🧯 M11 MATRIX · Failure Modes and Degradation Posture

*Mandatory annex of every contractual spec: what happens when the dependency falls*

```yaml
component: [name]
spec_reference: specs/[component].md
governing_adr: ADR-[XXX]
```

---

## 1. Doctrine

1. **Security decisions fail closed.** Under any doubt about authentication, authorization or permission parsing, the machine denies, and logs loudly.
2. **Evidence of something that already happened fails open with a durable buffer.** A failing audit pipeline never discards the record; it retains it until downstream recovers (R7).
3. **Tri-state responses.** `invalid` (401), `denied` (403) and `could not verify` (503) are distinct states; collapsing them is the family's signature (R1).
4. **Every row has a fault-injection test.** A row without a test is intention, not posture.

## 2. Matrix per interface

| Operation | Error condition | Class | Posture | Response / action | Log and telemetry | Test |
|---|---|---|---|:---:|---|---|
| `POST /v1/items` | missing credential | hard | **Fail-closed** | `401` | security event with origin | `test_items_missing_bearer_401` |
| `POST /v1/items` | authorization service unavailable | transient | **Fail-closed** | `503` | retry with backoff; never accept unverified | `test_items_authz_down_503` |
| `POST /v1/items` | policy timeout (> limit declared in spec) | transient | **Fail-closed** | `403` | closed-world denial | `test_items_policy_timeout_denies` |
| `POST /v1/audit` | store unavailable | transient | **Fail-open with durable buffer** | `202` | event on persistent queue; alert | `test_audit_store_down_buffers` |
| `GET /v1/items/{id}` | identity derivation fails | hard | **Fail-closed** | `401` | never falls back to a default identity | `test_items_identity_resolution_fails_closed` |

## 3. Evidence sinks (the half that is usually missing)

| Sink | Failure | Posture | Buffer | Proof nothing was lost |
|---|---|---|---|---|
| audit log | database unavailable | FO-durable | persistent queue | emitted count = stored + buffered (disagreeable pair) |
| shadow intent-log | disk full | FO-durable | rotation with alert | same |
