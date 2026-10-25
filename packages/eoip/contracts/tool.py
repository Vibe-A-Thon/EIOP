"""Versioned tool contracts used by the governed agent runtime."""

from __future__ import annotations

from typing import Any, Literal

from eoip.contracts.agent import RiskLevel
from pydantic import BaseModel, Field, model_validator

ToolStatus = Literal["SUCCEEDED", "FAILED", "DENIED", "TIMEOUT"]


class ToolContract(BaseModel):
    schema_version: str = "2.0"
    name: str = Field(min_length=1)
    version: str = "1.0.0"
    description: str = Field(min_length=1)
    risk_level: RiskLevel = "R0"
    read_only: bool = True
    reversible: bool = True
    approval_required: bool = False
    timeout_seconds: float = Field(default=10.0, gt=0, le=120)
    input_schema: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_safety(self) -> ToolContract:
        if not self.read_only and self.risk_level in {"R2", "R3", "R4"}:
            self.approval_required = True
        return self


class ToolRequest(BaseModel):
    schema_version: str = "2.0"
    tool_call_id: str
    tool_name: str
    arguments: dict[str, Any]
    risk_level: RiskLevel | None = None
    actor_id: str | None = None
    tenant_id: str = Field(default="_platform", min_length=1)  # never blank (SR-TEN-001)
    run_id: str | None = None
    approval_id: str | None = None
    dry_run: bool = False


class ToolResult(BaseModel):
    schema_version: str = "2.0"
    tool_call_id: str
    status: ToolStatus
    result: object | None = None
    evidence_refs: list[str] | None = None
    error: dict[str, Any] | None = None
    duration_ms: int = Field(default=0, ge=0)
