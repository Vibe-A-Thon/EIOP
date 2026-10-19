"""REVA error contract, hierarchy, and payload serialization (T-103 / REVA-WK-009 / §10.1)."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


class RevaError(Exception):
    """Base exception for all REVA domain and operational errors."""

    def __init__(
        self,
        code: str,
        category: str,
        message: str,
        *,
        retryable: bool = False,
        remediation_action: str = "Check inputs and retry",
        continuation: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.category = category
        self.message = message
        self.retryable = retryable
        self.remediation_action = remediation_action
        self.continuation = continuation
        self.details = details or {}

    def to_dict(self, correlation_id: Optional[str] = None) -> Dict[str, Any]:
        """Convert error to normative JSON payload matching §10.1."""
        return {
            "error": {
                "code": self.code,
                "category": self.category,
                "message": self.message,
                "retryable": self.retryable,
                "remediation": {
                    "action": self.remediation_action,
                    "continuation": self.continuation,
                },
                "details": {
                    "issues": self.details.get("issues", []),
                    "partial": self.details.get("partial"),
                    "limits": self.details.get("limits"),
                },
                "correlation_id": correlation_id or str(uuid.uuid4()),
            }
        }


# Concrete error classes per §10.1 catalogue
class SchemaUnknownFieldError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_SCHEMA_UNKNOWN_FIELD", "invalid_input", message, details=details)


class ValidationError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_VALIDATION", "invalid_input", message, details=details)


class CanonicalizationError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_CANONICALIZATION", "invalid_input", message, details=details)


class PredicateUnknownError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_PREDICATE_UNKNOWN", "invalid_input", message, details=details)


class ProducerError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_PRODUCER", "invalid_input", message, details=details)


class SignatureError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_SIGNATURE", "integrity", message, details=details)


class IntegrityError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_INTEGRITY", "integrity", message, details=details)


class NotFoundError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_NOT_FOUND", "not_found", message, details=details)


class ConflictError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_CONFLICT", "conflict", message, details=details)


class UnauthorizedError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_UNAUTHORIZED", "unauthorized", message, details=details)


class ForbiddenError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_FORBIDDEN", "forbidden", message, details=details)


class BudgetExceededError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_BUDGET_EXCEEDED", "resource_limit", message, details=details)


class ContinuationInvalidError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_CONTINUATION_INVALID", "invalid_input", message, details=details)


class ResourceLimitError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_RESOURCE_LIMIT", "resource_limit", message, details=details)


class DirtyTreeError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_DIRTY_TREE", "invalid_input", message, details=details)


class SandboxUnavailableError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_SANDBOX_UNAVAILABLE", "unavailable", message, details=details)


class TimeoutError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_TIMEOUT", "timeout", message, retryable=True, details=details)


class CancelledError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_CANCELLED", "cancelled", message, details=details)


class BackendCapabilityError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_BACKEND_CAPABILITY", "unavailable", message, details=details)


class EgressDeniedError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_EGRESS_DENIED", "forbidden", message, details=details)


class UnsupportedFormatError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_UNSUPPORTED_FORMAT", "invalid_input", message, details=details)


class MalformedInputError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_MALFORMED_INPUT", "invalid_input", message, details=details)


class InternalError(RevaError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("REVA_E_INTERNAL", "internal", message, details=details)


# Ergonomic aliases
RevaIntegrityError = IntegrityError
RevaNotFoundError = NotFoundError
RevaValidationError = ValidationError
RevaConflictError = ConflictError
RevaTimeoutError = TimeoutError
RevaUnauthorizedError = UnauthorizedError
RevaForbiddenError = ForbiddenError
RevaSignatureError = SignatureError
RevaDirtyTreeError = DirtyTreeError
RevaArtifactMalformedError = MalformedInputError
RevaResourceLimitError = ResourceLimitError
RevaSecurityError = ForbiddenError

