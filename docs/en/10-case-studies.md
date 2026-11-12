# 10. Real-World Case Studies from SolarSystems
## Empirical Evidence, Critical Incidents, and Methodological Resolutions

---

### 1. Case 1: The 12-Day RBAC Blackout and Flip Composition (§5.4)

#### Context and Incident
In August 2026, the platform underwent an operational flip to enforce strict authorization: `PLUTO_ACCESS_ADMISSION_MODE=enforce`.
Immediately following deployment, the hourly scheduled batch executor (`solar-decision-table`) collapsed silently. For **11 consecutive days**, all executions aborted with HTTP 403, masked by the Nomad scheduler as status `dead`.
- **Measured Impact:** ~2,800 lost task executions; task throughput in `sun.executions` plummeted from ~252/day to **precisely zero**.

#### Root Cause
Three security flips were deployed in the same operational window:
1. Audit chain lock: `MOON_AUDIT_CHAIN_LOCK=true`.
2. Model token enforcement: `NEPTUNE_TOKEN_REQUIRED=true`.
3. Strict admission mode: `PLUTO_ACCESS_ADMISSION_MODE=enforce`.

Each flip had been independently validated by its author. However, the internal client in Saturn, when querying account administrators to run batch jobs, omitted the `Authorization` header.
> **The failure broke the question, not the answer.** No isolated unit test caught the defect because none tested the **composed product end-to-end**.

#### EEEMIAD Resolution
1. **Immediate Shadow Fallback:** The admission flag was reverted to `shadow` mode on 2026-08-18 (`commit a671908`).
2. **Pre-Flight Form 1 Institution (§5.4):** Mandatory inclusion of the **Flip Composition Clause**:
   *"What OTHER gates were flipped in this window? Was the COMPOSED PRODUCT exercised end-to-end with verified command and output?"*
3. **Conforming Re-provisioning:** Elimination of the static admin token and granting of proper OpenFGA tuples to the operational machine principal (`pri_platform_ops`).

---

### 2. Case 2: The Moon Orphan Audit Route and M11 Failure Modes

#### Context and Incident
On 2026-08-03, routine telemetry sweeps revealed that a primary audit insertion endpoint in Moon was silently returning HTTP 422.
- **Measured Impact:** Loss of ~370 live audit records over an 8-hour window.

#### Root Cause
A decorator order defect in the FastAPI controller bound an input sanitization helper in place of the database persistence handler.
The service exhibited **accidental Fail-Closed behavior on audit storage**: the request failed, the task completed anyway, and physical reality records were erased.

#### EEEMIAD Resolution (Rule R7)
1. **Application of Rule R7:**  
   *"Fail-Closed protects authorization decisions; Fail-Open protects historical evidence."*
2. **Append-Only Buffer:** Decoupling audit logging into a transactional NATS JetStream queue backed by 64-bit advisory locks in PostgreSQL.
3. **Negative Control Suite:** Adding corrupted payload tests verifying that telemetry alerts trigger without aborting audit durability.

---

### 3. Case 3: Ingress Caller-Type Spoofing and the C6 Vulnerability (ADR-042)

#### Context and Incident
A task submitted to the external ingress gateway (Venus) could bypass tenant quotas and safety classification if the JSON request body contained:
```json
{
  "caller_type": "internal",
  "priority": "system"
}
```

#### Root Cause
The master orchestrator read caller identity and authority **from the request body**, assuming that only internal services could hit the `/v1/tasks` route.
This represents a classic **Plausible Answer defect (Instance #1)**: the security gate functioned, but evaluated a subject supplied by the caller.

#### EEEMIAD Resolution
1. **ADR-042 Ratification:** Penned by the Reflective Agent with phased shadow-to-enforce progression.
2. **Hop-by-Hop Derived Identity:** Reading caller roles from request bodies was banned. Identity is **strictly derived from Vault Transit signed JWT session tokens**.
3. **Live Adversarial Assertion:** Reproduction tests confirmed that forged payloads now reliably receive `HTTP 403 blocked_by_classifier`.
