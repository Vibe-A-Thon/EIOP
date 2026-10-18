"""Stable connector errors shared by remote source adapters.

Implements error contracts required by CRA-004.2, CRA-004.3, CRA-004.8, and CRA-004.A.
"""

from __future__ import annotations
from typing import Any, Dict, Optional


class ConnectorError(RuntimeError):
    """Base error for connector operations."""

    def __init__(
        self,
        source_system: str,
        category: str,
        correlation_id: str = "default-corr-id",
        code: str = "CONNECTOR_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.source_system = source_system
        self.category = category
        self.correlation_id = correlation_id
        self.code = code
        self.details = details or {}
        super().__init__(f"{source_system} connector {category} (code={code}, correlation_id={correlation_id})")


class ConnectorAuthFailedError(ConnectorError):
    """Raised when authentication credentials or token are invalid or rejected (CRA-004.A)."""

    def __init__(self, source_system: str, correlation_id: str = "default-corr-id", details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            source_system=source_system,
            category="authentication_failure",
            correlation_id=correlation_id,
            code="CONNECTOR_AUTH_FAILED",
            details=details,
        )


class ConnectorVersionUnsupportedError(ConnectorError):
    """Raised when the remote product version is incompatible or unsupported (CRA-004.A)."""

    def __init__(
        self,
        source_system: str,
        version: str,
        supported_versions: list[str],
        correlation_id: str = "default-corr-id",
    ) -> None:
        details = {"version": version, "supported_versions": supported_versions}
        super().__init__(
            source_system=source_system,
            category="unsupported_version",
            correlation_id=correlation_id,
            code="CONNECTOR_VERSION_UNSUPPORTED",
            details=details,
        )


class UnsupportedCapabilityError(ConnectorError):
    """Raised when an operation requires an undeclared capability (CRA-004.A, CRA-004.1)."""

    def __init__(
        self,
        source_system: str,
        capability: str,
        correlation_id: str = "default-corr-id",
    ) -> None:
        details = {"capability": capability}
        super().__init__(
            source_system=source_system,
            category="unsupported_capability",
            correlation_id=correlation_id,
            code="UNSUPPORTED_CAPABILITY",
            details=details,
        )


class ConnectorSpecializationFailedError(ConnectorError):
    """Raised when specialized connector instantiation fails (G07 closure, CRA-004.A)."""

    def __init__(
        self,
        source_system: str,
        reason: str,
        correlation_id: str = "default-corr-id",
    ) -> None:
        details = {"reason": reason}
        super().__init__(
            source_system=source_system,
            category="specialization_failure",
            correlation_id=correlation_id,
            code="CONNECTOR_SPECIALIZATION_FAILED",
            details=details,
        )


class UnsupportedProtocolError(ConnectorError):
    """Raised when an unsupported protocol is requested (CRA-004.3)."""

    def __init__(
        self,
        source_system: str,
        protocol: str,
        correlation_id: str = "default-corr-id",
    ) -> None:
        details = {"protocol": protocol}
        super().__init__(
            source_system=source_system,
            category="unsupported_protocol",
            correlation_id=correlation_id,
            code="UNSUPPORTED_PROTOCOL",
            details=details,
        )


class RateLimitExceededError(ConnectorError):
    """Raised when source request rate limit is exceeded (CRA-004.8)."""

    def __init__(
        self,
        source_system: str,
        retry_after: float,
        correlation_id: str = "default-corr-id",
    ) -> None:
        details = {"retry_after": retry_after}
        super().__init__(
            source_system=source_system,
            category="rate_limit_exceeded",
            correlation_id=correlation_id,
            code="RATE_LIMIT_EXCEEDED",
            details=details,
        )
