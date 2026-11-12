from pydantic import BaseModel, Field, model_validator
from typing import Optional

class TaskSubmitRequest(BaseModel):
    task_id: str = Field(..., description="Unique task identifier")
    prompt: str = Field(..., description="The user or agent prompt")
    priority: str = Field(default="standard", description="Execution priority")

    @model_validator(mode="before")
    @classmethod
    def reject_identity_spoofing(cls, data: dict):
        # Strict security invariant (ADR-001): Body cannot declare identity claims
        forbidden_keys = {"caller_type", "tenant_id", "user_id", "principal_id"}
        detected = forbidden_keys.intersection(data.keys())
        if detected:
            raise ValueError(f"Identity spoofing violation: Forbidden fields present in body: {detected}")
        return data

class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str
    derived_caller: str
    derived_tenant: str
