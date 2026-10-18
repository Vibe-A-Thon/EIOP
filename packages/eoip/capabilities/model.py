"""Capability models and exceptions conforming to CRA-001 and section 6."""
from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional
from pydantic import BaseModel, Field

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class CapabilityState(str, Enum):
    SUPPORTED_QUALIFIED = "SUPPORTED_QUALIFIED"
    SUPPORTED_UNQUALIFIED = "SUPPORTED_UNQUALIFIED"
    DISABLED = "DISABLED"
    UNAVAILABLE = "UNAVAILABLE"
    UNLICENSED = "UNLICENSED"
    UNSUPPORTED = "UNSUPPORTED"

class CapabilityEntry(BaseModel):
    capability_id: str
    provider_id: str
    provider_version: str
    profile: str = "P0"
    state: CapabilityState
    last_probe_at: Optional[datetime] = None
    receipt_ref: Optional[str] = None
    qualifying_clauses: list[str] = Field(default_factory=list)
    unsupported_constructs: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)

class CapabilityError(Exception):
    def __init__(self, code: str, message: str, status_code: int, details: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }

class UnsupportedCapabilityError(CapabilityError):
    """HTTP 422: capability or construct is unsupported."""
    def __init__(self, capability_id: str, construct: Optional[str] = None):
        msg = f"Capability '{capability_id}' does not support construct '{construct}'" if construct else f"Capability '{capability_id}' is unsupported"
        super().__init__(
            code="UNSUPPORTED_CAPABILITY",
            message=msg,
            status_code=422,
            details={"capability_id": capability_id, "unsupported_construct": construct},
        )

class CapabilityUnavailableError(CapabilityError):
    """HTTP 503: configured capability is temporarily unavailable."""
    def __init__(self, capability_id: str, reason: str = "Provider health probe failed or tier missing"):
        super().__init__(
            code="CAPABILITY_UNAVAILABLE",
            message=f"Capability '{capability_id}' is unavailable: {reason}",
            status_code=503,
            details={"capability_id": capability_id, "reason": reason},
        )

class CapabilityNotEntitledError(CapabilityError):
    """HTTP 403: tenant/principal not licensed for capability."""
    def __init__(self, capability_id: str):
        super().__init__(
            code="CAPABILITY_NOT_ENTITLED",
            message=f"Capability '{capability_id}' is unlicensed for current scope",
            status_code=403,
            details={"capability_id": capability_id},
        )

class CapabilityDisabledError(CapabilityError):
    """HTTP 409: capability disabled by configuration."""
    def __init__(self, capability_id: str):
        super().__init__(
            code="CAPABILITY_DISABLED",
            message=f"Capability '{capability_id}' is disabled by configuration",
            status_code=409,
            details={"capability_id": capability_id},
        )
