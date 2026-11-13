import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_probe():
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_submit_task_success_with_valid_bearer():
    headers = {"Authorization": "Bearer valid-user-token"}
    payload = {
        "task_id": "tsk-001",
        "prompt": "Analyze code architecture",
        "priority": "standard"
    }
    resp = client.post("/v1/tasks", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "admitted"
    # Proves identity is derived from token (ADR-001 D2)
    assert data["derived_caller"] == "usr-42"
    assert data["derived_tenant"] == "tnt-prod"

# Negative Controls & Disagreeable Pairs (Rule R2 & Fail-Closed M11)
def test_submit_task_missing_auth_header_fails_closed_401():
    payload = {"task_id": "tsk-002", "prompt": "Unauthenticated task"}
    resp = client.post("/v1/tasks", json=payload)
    assert resp.status_code == 401
    assert "Missing Authorization" in resp.json()["detail"]

def test_submit_task_invalid_bearer_token_fails_401():
    headers = {"Authorization": "Bearer forged-or-expired-token"}
    payload = {"task_id": "tsk-003", "prompt": "Attack task"}
    resp = client.post("/v1/tasks", json=payload, headers=headers)
    assert resp.status_code == 401
    assert "invalid or expired" in resp.json()["detail"]

def test_submit_task_body_spoofing_attempt_rejected_422():
    # Attempting to inject identity claims into the body (identity-spoofing reproduction)
    headers = {"Authorization": "Bearer valid-user-token"}
    payload = {
        "task_id": "tsk-004",
        "prompt": "Privilege escalation attempt",
        "caller_type": "internal",
        "tenant_id": "tnt-master-admin"
    }
    resp = client.post("/v1/tasks", json=payload, headers=headers)
    # Must fail with validation error, refusing to allow body spoofing
    assert resp.status_code == 422
