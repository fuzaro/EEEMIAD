# ADR-001: Task Admission Gateway and Hop-by-Hop Identity Derivation

```yaml
status: ACCEPTED
date: 2026-09-28
deciders: [deciding role, platform lead]
hierarchy_layer: ADR
governs: [spec/task-gateway.md]
justified_by: [plan/framework-principles.md §Principle 1, §Principle 2]
replaces: []
eee_phase: 4
```

---

## 1. Problem Context and Empirical Evidence
- **Empirical Origin:** Incident in which a caller supplied `caller_type="internal"` in the request body and bypassed the risk classifier and tenant quota checks (the classic "plausible answer" instance: the gate validated a subject chosen by the caller).
- **Observed Symptom:** Security admission was evaluating user-controlled attributes instead of cryptographically proven identity claims.
- **Affected Principles:** Principle 1 (Least Privilege), Principle 2 (Fail-Closed).

---

## 2. Architectural Decisions
- **D1 (Bearer Token Requirement):** All tasks submitted to `POST /v1/tasks` must carry an `Authorization: Bearer <token>` header.
- **D2 (Token-Derived Identity):** The orchestrator derives `caller_id` and `tenant_id` strictly from token claims; request body fields claiming identity are rejected with HTTP 422.
- **D3 (Fail-Closed Degradation):** Missing or invalid tokens result in immediate `HTTP 401 Unauthorized` without entering task orchestration.

---

## 3. Alternatives Considered

| Alternative | Pros | Cons | Ruling |
|---|---|---|:---:|
| **Option A (Body-Declared Caller):** Accept `caller_type` in JSON body with shared HMAC secret. | Trivial implementation. | Vulnerable to impersonation; violates zero-trust perimeter. | **REJECTED** |
| **Option B (Bearer JWT Extraction - Selected):** Derive identity strictly from Bearer token claims via gateway middleware. | Strict hop-by-hop non-repudiation; audit-ready. | Requires JWT parser on ingress. | **ACCEPTED** |

---

## 4. Accepted Consequences
- **Positive:** Closes the body-declared identity spoofing vector; every task submission carries a non-repudiable audit trail.
- **Negative:** External client scripts must authenticate and obtain a valid session token before dispatching tasks.
