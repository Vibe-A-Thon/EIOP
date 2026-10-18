"""Contracts and data models for Governed Actions & Two-Phase Write-Back (CRA-027)."""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.intelligence_eng.engine import AutonomyLevel


class ActionState(str, Enum):
    """ActionIntent lifecycle states (CRA-027.6)."""

    PROPOSED = "PROPOSED"
    STAGED = "STAGED"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATED = "COMPENSATED"
    UNKNOWN_OUTCOME = "UNKNOWN_OUTCOME"


class RiskClass(str, Enum):
    """Action risk classification."""

    READ_ONLY = "READ_ONLY"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL_DESTRUCTIVE = "CRITICAL_DESTRUCTIVE"


class ActionError(Exception):
    """Base error for action operations."""

    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


class WriteBackDisabledError(ActionError):
    pass


class ApprovalExpiredError(ActionError):
    pass


class InvalidApprovalError(ActionError):
    pass


class IntentDigestMismatchError(ActionError):
    pass


class IdempotencyViolationError(ActionError):
    pass


class ReadBackVerificationError(ActionError):
    pass


class ActionType(BaseModel):
    """SHACL Action Shape declaration (OntologyAction, ONT-009, CRA-027.7)."""

    model_config = ConfigDict(frozen=True)

    type_id: str
    name: str
    description: str = ""
    target_connector: str  # e.g., "jira", "servicenow", "github", "sql"
    argument_schema: dict[str, Any] = Field(default_factory=dict)
    preconditions: list[str] = Field(default_factory=list)
    declared_effects: list[str] = Field(default_factory=list)  # Classes/properties mutated
    risk_class: RiskClass = RiskClass.LOW
    required_autonomy_level: AutonomyLevel = AutonomyLevel.HITL
    compensation_action_id: str | None = None
    read_back_query: str | None = None
    is_destructive: bool = False


class ActionIntent(BaseModel):
    """Security-bearing ActionIntent specification (CRA-027.3, CRA-027.6, ASPEII)."""

    model_config = ConfigDict(extra="ignore")

    intent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_type_id: str
    target_instance: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    principal: str
    scope: dict[str, Any] = Field(default_factory=dict)  # tenant_id, workspace_id, roles
    idempotency_key: str  # Mandatory 16-128 chars (CRA-027.8)
    state: ActionState = ActionState.PROPOSED
    policy_revision: str = "v1.0"
    base_revision: str = "v1.0"
    created_at: float = Field(default_factory=time.time)
    deadline: float | None = None
    dry_run: bool = False
    details: dict[str, Any] = Field(default_factory=dict)

    def canonical_digest(self) -> str:
        """Computes SHA-256 over UTF-8 RFC 8785 canonical JSON with domain separator."""
        canonical_projection = {
            "action_type_id": self.action_type_id,
            "target_instance": self.target_instance,
            "arguments": self.arguments,
            "principal": self.principal,
            "scope": self.scope,
            "idempotency_key": self.idempotency_key,
            "policy_revision": self.policy_revision,
            "base_revision": self.base_revision,
        }
        # Deterministic sorting and compact separators matching RFC 8785 JSON canonicalization
        payload = json.dumps(canonical_projection, sort_keys=True, separators=(",", ":"))
        full_bytes = f"EOIP-ASPEII-ACTION-v1\n{payload}".encode("utf-8")
        return hashlib.sha256(full_bytes).hexdigest()


class ApprovalGrant(BaseModel):
    """Approval bound to exact intent digest, principal, nonce, and expiry (CRA-027.3, CRA-027.8)."""

    model_config = ConfigDict(frozen=True)

    grant_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    intent_id: str
    intent_digest: str
    approver: str
    approver_autonomy: AutonomyLevel = AutonomyLevel.HITL
    nonce: str
    created_at: float = Field(default_factory=time.time)
    expires_at: float = Field(default_factory=lambda: time.time() + 300.0)  # 5 min default
    signature: str = ""

    def is_expired(self, current_time: float | None = None) -> bool:
        t = current_time if current_time is not None else time.time()
        return t > self.expires_at


class ExecutionJournalEntry(BaseModel):
    """Tamper-evident audit and state transition journal record (CRA-027.4)."""

    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    intent_id: str
    timestamp: float = Field(default_factory=time.time)
    state: ActionState
    details: dict[str, Any] = Field(default_factory=dict)
    read_back_verified: bool = False
    error: str | None = None
