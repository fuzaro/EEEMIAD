# Specification: Task Ingress Gateway
## Service: Task Ingress & Admission Control

```yaml
service_name: task-gateway
version: 1.0.0
status: Active
governing_adr: adr/ADR-001-task-admission-gateway.md
```

---

## 1. Endpoints

### 1.1 Submit Task
- **Path:** `POST /v1/tasks`
- **Headers:** `Authorization: Bearer <token>` (Required)
- **Request Body (JSON):**
  ```json
  {
    "task_id": "tsk-12345",
    "prompt": "Summarize the findings report",
    "priority": "standard"
  }
  ```
  *(Note: Any body containing `caller_type`, `tenant_id`, or `user_id` will be rejected with HTTP 422).*
- **Responses:**
  - `200 OK`: Task successfully admitted and queued.
  - `401 Unauthorized`: Token missing or invalid.
  - `422 Unprocessable Entity`: Body contains forbidden identity spoofing fields.

### 1.2 Health Probe
- **Path:** `GET /v1/health`
- **Responses:**
  - `200 OK`: `{ "status": "healthy", "service": "task-gateway" }`

---

## 2. M11 Failure Mode Matrix

| Endpoint | Error Condition | Failure Class | Degradation Posture | Expected Response |
|---|---|---|---|:---:|
| `POST /v1/tasks` | Missing Authorization Header | Hard Failure | **Fail-Closed** | `401 Unauthorized` |
| `POST /v1/tasks` | Forged identity in body | Hard Failure | **Fail-Closed** | `422 Unprocessable Entity` |
| `POST /v1/tasks` | Internal downstream timeout | Transient Failure | **Fail-Closed** | `503 Service Unavailable` |
