# M11 Failure Modes and Degradation Posture Matrix
## Mandatory Annex for Contract Specifications (§7 and §11)

```yaml
service_name: [Service / Component Name]
spec_reference: specs/[service].md
governing_adr: ADR-[XXX]
```

---

## 1. Failure Mode Matrix per Interface / Route

| Operation / Endpoint | Error Condition | Failure Class | Degradation Posture | HTTP Status / Action | Telemetry & Audit |
|---|---|---|---|:---:|---|
| `POST /v1/tasks` | Missing token | Hard Failure | **Fail-Closed** | `401 Unauthorized` | Immediate security log with client IP |
| `POST /v1/tasks` | Vault Transit down | Transient Failure | **Fail-Closed** | `503 Service Unavailable` | Retry with exponential backoff; never proceed unsigned |
| `POST /v1/audit` | Moon DB unreachable | Transient Failure | **Fail-Open with Durable Buffer** | `202 Accepted` | Push event to disk-backed JetStream stream (R7) |
| `POST /v1/access/check` | OpenFGA timeout (>100ms) | Transient Failure | **Fail-Closed** | `403 Forbidden (Timeout)` | Closed-world deny on ambiguity (ADR-040) |

---

## 2. Invariants of the M11 Doctrine
1. **Security Decisions are ALWAYS Fail-Closed:** On any ambiguity regarding token authenticity, RBAC permissions, or scope validity, the gateway rejects access.
2. **Historical Evidence Preservation is Fail-Open with Durable Buffer:** Failures in audit persistence must never discard historical event data; events are buffered in durable storage until downstream recovery.
