"""Enterprise exception hierarchy with error codes and structured diagnostics.

Every enterprise error carries a machine-readable code, HTTP status mapping,
and optional diagnostic context so API consumers can programmatically handle
failures without parsing message strings.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class ErrorSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ErrorCategory(str, Enum):
    VALIDATION = "VALIDATION"
    AUTHORIZATION = "AUTHORIZATION"
    RESOURCE = "RESOURCE"
    RESILIENCE = "RESILIENCE"
    CONFIGURATION = "CONFIGURATION"
    INGESTION = "INGESTION"
    GRAPH = "GRAPH"
    INTELLIGENCE = "INTELLIGENCE"
    INFRASTRUCTURE = "INFRASTRUCTURE"


class EnterpriseError(Exception):
    """Base exception for all enterprise features.

    Attributes:
        error_code: Machine-readable error identifier (e.g. ``EOIP-RES-001``).
        http_status: Suggested HTTP response code.
        severity: Operational severity for alerting/logging.
        category: High-level error family.
        context: Arbitrary diagnostic payload (never sent to end-users in production).
    """

    error_code: str = "EOIP-ENT-000"
    http_status: int = 500
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.INFRASTRUCTURE

    def __init__(self, message: str, *,
                 context: dict[str, Any] | None = None,
                 cause: Exception | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.__cause__ = cause

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
        }


# ── Resilience Errors ────────────────────────────────────────────────────

class ResilienceError(EnterpriseError):
    error_code = "EOIP-RES-000"
    category = ErrorCategory.RESILIENCE


class CircuitOpenError(ResilienceError):
    error_code = "EOIP-RES-001"
    http_status = 503
    severity = ErrorSeverity.HIGH


class RateLimitExceeded(ResilienceError):
    error_code = "EOIP-RES-002"
    http_status = 429
    severity = ErrorSeverity.MEDIUM


class BulkheadFullError(ResilienceError):
    error_code = "EOIP-RES-003"
    http_status = 503
    severity = ErrorSeverity.HIGH


class BulkheadTimeoutError(ResilienceError):
    error_code = "EOIP-RES-004"
    http_status = 504
    severity = ErrorSeverity.HIGH


class ConnectionPoolExhausted(ResilienceError):
    error_code = "EOIP-RES-005"
    http_status = 503
    severity = ErrorSeverity.HIGH


class ConnectionPoolTimeout(ResilienceError):
    error_code = "EOIP-RES-006"
    http_status = 504
    severity = ErrorSeverity.HIGH


# ── Validation Errors ─────────────────────────────────────────────────────

class ValidationError(EnterpriseError):
    error_code = "EOIP-VAL-001"
    http_status = 422
    category = ErrorCategory.VALIDATION
    severity = ErrorSeverity.LOW


class InvalidConfigurationError(EnterpriseError):
    error_code = "EOIP-CFG-001"
    http_status = 400
    category = ErrorCategory.CONFIGURATION
    severity = ErrorSeverity.MEDIUM


# ── Resource Errors ───────────────────────────────────────────────────────

class ResourceNotFoundError(EnterpriseError):
    error_code = "EOIP-RES-010"
    http_status = 404
    category = ErrorCategory.RESOURCE
    severity = ErrorSeverity.LOW


class ResourceConflictError(EnterpriseError):
    error_code = "EOIP-RES-011"
    http_status = 409
    category = ErrorCategory.RESOURCE
    severity = ErrorSeverity.MEDIUM


class ResourceExhaustedError(EnterpriseError):
    error_code = "EOIP-RES-012"
    http_status = 503
    category = ErrorCategory.RESOURCE
    severity = ErrorSeverity.HIGH


# ── Ingestion Errors ──────────────────────────────────────────────────────

class IngestionError(EnterpriseError):
    error_code = "EOIP-ING-001"
    http_status = 500
    category = ErrorCategory.INGESTION
    severity = ErrorSeverity.MEDIUM


class BatchProcessingError(IngestionError):
    error_code = "EOIP-ING-002"


class StreamIngestionError(IngestionError):
    error_code = "EOIP-ING-003"


class DLQOverflowError(IngestionError):
    error_code = "EOIP-ING-004"
    http_status = 507
    severity = ErrorSeverity.HIGH


# ── Graph Errors ──────────────────────────────────────────────────────────

class GraphError(EnterpriseError):
    error_code = "EOIP-GRF-000"
    category = ErrorCategory.GRAPH


class SnapshotError(GraphError):
    error_code = "EOIP-GRF-001"


class SnapshotNotFoundError(SnapshotError):
    error_code = "EOIP-GRF-002"
    http_status = 404
    severity = ErrorSeverity.LOW


class SnapshotRestoreError(SnapshotError):
    error_code = "EOIP-GRF-003"
    severity = ErrorSeverity.HIGH


class MigrationError(GraphError):
    error_code = "EOIP-GRF-010"


class MigrationConflictError(MigrationError):
    error_code = "EOIP-GRF-011"
    http_status = 409
    severity = ErrorSeverity.HIGH


class DiffError(GraphError):
    error_code = "EOIP-GRF-020"


# ── Intelligence Errors ───────────────────────────────────────────────────

class IntelligenceError(EnterpriseError):
    error_code = "EOIP-INT-000"
    category = ErrorCategory.INTELLIGENCE


class LearningError(IntelligenceError):
    error_code = "EOIP-INT-001"


class CorrelationError(IntelligenceError):
    error_code = "EOIP-INT-002"


class PredictionError(IntelligenceError):
    error_code = "EOIP-INT-003"


class NLConfigParseError(IntelligenceError):
    error_code = "EOIP-INT-004"
    http_status = 422
    severity = ErrorSeverity.LOW


# ── Testing Errors ────────────────────────────────────────────────────────

class ChaosError(EnterpriseError):
    error_code = "EOIP-TST-001"
    category = ErrorCategory.INFRASTRUCTURE


class ExperimentNotFoundError(ChaosError):
    error_code = "EOIP-TST-002"
    http_status = 404
    severity = ErrorSeverity.LOW


class ExperimentAlreadyRunningError(ChaosError):
    error_code = "EOIP-TST-003"
    http_status = 409
    severity = ErrorSeverity.MEDIUM


# ── Health Errors ─────────────────────────────────────────────────────────

class HealthCheckError(EnterpriseError):
    error_code = "EOIP-HLT-001"
    category = ErrorCategory.INFRASTRUCTURE
    severity = ErrorSeverity.HIGH


class SLAViolationError(HealthCheckError):
    error_code = "EOIP-HLT-002"
    severity = ErrorSeverity.CRITICAL
