"""Pydantic response models for enterprise API endpoints.

Typed response models enable OpenAPI schema generation, client codegen,
and compile-time validation of API contracts.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ── Common ────────────────────────────────────────────────────────────────

class ErrorDetail(BaseModel):
    code: str = Field(description="Machine-readable error code (e.g. EOIP-RES-001)")
    message: str = Field(description="Human-readable error description")
    category: str = Field(description="Error category")
    severity: str = Field(description="Operational severity: LOW, MEDIUM, HIGH, CRITICAL")


class ErrorResponse(BaseModel):
    error: ErrorDetail
    correlation_id: str | None = None


class OperationResult(BaseModel):
    success: bool
    message: str = ""


# ── Resilience ────────────────────────────────────────────────────────────

class CircuitBreakerStatus(BaseModel):
    name: str
    state: str = Field(description="CLOSED, OPEN, or HALF_OPEN")
    failure_count: int
    total_calls: int
    total_failures: int
    total_opens: int
    total_resets: int


class PoolMetricsResponse(BaseModel):
    pool_size: int
    active: int
    idle: int
    waiting: int
    total_acquired: int
    total_released: int
    total_created: int
    total_destroyed: int
    total_timeouts: int
    total_health_failures: int


class RateLimiterStatus(BaseModel):
    name: str
    strategy: str
    total_allowed: int
    total_rejected: int
    remaining: int
    rejection_rate: float


class BulkheadStatus(BaseModel):
    name: str
    active: int
    queued: int
    max_concurrent: int
    max_queue_size: int
    total_accepted: int
    total_rejected: int
    total_completed: int
    total_timeouts: int
    utilization: float


# ── Snapshots ─────────────────────────────────────────────────────────────

class SnapshotResponse(BaseModel):
    snapshot_id: str
    name: str
    snapshot_type: str
    status: str
    created_at: str
    entity_count: int
    edge_count: int
    size_bytes: int
    checksum: str
    parent_snapshot_id: str | None = None
    tags: dict[str, str] = Field(default_factory=dict)


class SnapshotListResponse(BaseModel):
    snapshots: list[SnapshotResponse]
    total: int = 0


class RestorePointResponse(BaseModel):
    restore_id: str
    snapshot_id: str
    started_at: str
    completed_at: str | None = None
    entities_restored: int
    edges_restored: int
    success: bool


# ── DLQ ───────────────────────────────────────────────────────────────────

class DLQEntryResponse(BaseModel):
    entry_id: str
    source: str
    error_type: str
    error_message: str
    status: str
    created_at: str
    retry_count: int = 0


class DLQStatsResponse(BaseModel):
    total: int
    pending: int
    replayed: int
    discarded: int
    expired: int
    by_source: dict[str, int] = Field(default_factory=dict)
    by_error_type: dict[str, int] = Field(default_factory=dict)


class DLQReplayResponse(BaseModel):
    replayed: int
    failed: int
    total_attempted: int


# ── Health ────────────────────────────────────────────────────────────────

class HealthCheckResult(BaseModel):
    name: str
    status: str
    latency_ms: float
    last_checked: str
    consecutive_failures: int = 0
    message: str = ""


class AggregateHealthResponse(BaseModel):
    overall_status: str = Field(description="HEALTHY, DEGRADED, or UNHEALTHY")
    checks: dict[str, HealthCheckResult] = Field(default_factory=dict)
    uptime_percent: float = 0.0
    checked_at: str = ""


class SLAReportResponse(BaseModel):
    sla_targets: list[dict[str, Any]] = Field(default_factory=list)


# ── Migrations ────────────────────────────────────────────────────────────

class MigrationResponse(BaseModel):
    migration_id: str
    version: str
    name: str
    status: str
    applied_at: str | None = None
    description: str = ""


class MigrationListResponse(BaseModel):
    migrations: list[dict[str, Any]]
    current_version: str | None = None


class MigrationApplyResponse(BaseModel):
    applied: bool
    version: str | None = None


# ── Chaos ─────────────────────────────────────────────────────────────────

class ExperimentResponse(BaseModel):
    experiment_id: str
    name: str
    hypothesis: str
    status: str
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    result: str | None = None


class ExperimentListResponse(BaseModel):
    experiments: list[dict[str, Any]]
    total: int = 0


# ── Diff ──────────────────────────────────────────────────────────────────

class ChangeRecord(BaseModel):
    change_id: str
    entity_id: str
    change_type: str
    timestamp: str
    impact: str = "UNKNOWN"


class DiffChangesResponse(BaseModel):
    changes: list[dict[str, Any]]
    total: int = 0


class EntityTimelineResponse(BaseModel):
    entity_id: str
    total_modifications: int
    first_seen: str | None = None
    last_modified: str | None = None
    changes: list[dict[str, Any]] = Field(default_factory=list)


# ── Learning ──────────────────────────────────────────────────────────────

class FeedbackResponse(BaseModel):
    feedback_id: str
    feedback_type: str
    domain: str
    created_at: str
    rule_derived: bool = False


class LearningRulesResponse(BaseModel):
    rules: list[dict[str, Any]]
    total: int = 0


class LearningStatsResponse(BaseModel):
    total_feedback: int
    rules_active: int
    accuracy: float = 0.0
    by_domain: dict[str, int] = Field(default_factory=dict)


# ── Correlation ───────────────────────────────────────────────────────────

class CorrelationEventResponse(BaseModel):
    events: list[dict[str, Any]]
    total: int = 0


class RootCauseAnalysisResponse(BaseModel):
    event_id: str
    root_cause: dict[str, Any] | None = None
    correlated_events: list[dict[str, Any]] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    confidence: float = 0.0


# ── NL Config ─────────────────────────────────────────────────────────────

class NLConfigExecuteResponse(BaseModel):
    intent: str
    confidence: float
    parameters: dict[str, Any] = Field(default_factory=dict)
    executed: bool = False
    result: dict[str, Any] | None = None
    dry_run: bool = False


class NLSuggestionsResponse(BaseModel):
    suggestions: list[str]


# ── Analytics ─────────────────────────────────────────────────────────────

class TrendResponse(BaseModel):
    metric: str
    direction: str
    slope: float
    data_points: int
    coefficient_of_variation: float = 0.0
    confidence: float = 0.0


class AnomalyResponse(BaseModel):
    anomalies: list[dict[str, Any]]
    total: int = 0


class ForecastResponse(BaseModel):
    metric: str
    method: str
    horizon: int
    predictions: list[float]
    confidence_interval: dict[str, Any] = Field(default_factory=dict)


class GrowthReportResponse(BaseModel):
    metric: str
    current_value: float
    growth_rate: float
    projected_30d: float | None = None
    projected_90d: float | None = None
    days_to_threshold: int | None = None


class MetricsListResponse(BaseModel):
    metrics: dict[str, Any]
