from fastapi import FastAPI, Header, HTTPException, Depends
from models import TaskSubmitRequest, TaskSubmitResponse
from typing import Optional

app = FastAPI(title="Task Gateway - EEEMIAD Reference")

def authenticate_bearer_token(authorization: Optional[str] = Header(None)) -> dict:
    # Fail-Closed security invariant (Rule R7 & ADR-001)
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Bearer header")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Bearer token format")
    
    token = parts[1]
    # In production this verifies the JWT signature against the identity provider public key
    if token == "valid-user-token":
        return {"principal_id": "usr-42", "tenant_id": "tnt-prod", "role": "member"}
    elif token == "valid-admin-token":
        return {"principal_id": "usr-admin", "tenant_id": "tnt-prod", "role": "admin"}
    else:
        raise HTTPException(status_code=401, detail="Cryptographically invalid or expired token")

@app.get("/v1/health")
def health_check():
    return {"status": "healthy", "service": "task-gateway"}

@app.post("/v1/tasks", response_model=TaskSubmitResponse)
def submit_task(
    payload: TaskSubmitRequest,
    caller_claims: dict = Depends(authenticate_bearer_token)
):
    # Derived identity: Claims originate strictly from the token, not the body (ADR-001 D2)
    return TaskSubmitResponse(
        task_id=payload.task_id,
        status="admitted",
        derived_caller=caller_claims["principal_id"],
        derived_tenant=caller_claims["tenant_id"]
    )
