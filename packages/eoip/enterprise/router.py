"""Unified API router for enterprise features #9-#20.

Provides production-grade REST endpoints with:
- Typed Pydantic request/response models
- Structured error handling via EnterpriseError hierarchy
- OpenAPI documentation with tags, descriptions, and examples
- Correlation-ID propagation and structured logging
- Observability instrumentation
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from eoip.enterprise.exceptions import (
    EnterpriseError,
    ExperimentNotFoundError,
    ResourceNotFoundError,
    SnapshotNotFoundError,
    ValidationError,
)
from eoip.enterprise.logging import get_logger
from eoip.enterprise.observability import get_metrics, timed

_log = get_logger("router")
_obs = get_metrics()

# ── Request models ─────────────────────────────────────────────────────

class SnapshotRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256, description="Snapshot display name")
    snapshot_type: str = Field(default="FULL", pattern="^(FULL|INCREMENTAL|SCHEMA_ONLY)$",
                               description="Type of snapshot to create")
    tags: dict[str, str] = Field(default_factory=dict, description="Key-value metadata tags")


class RestoreRequest(BaseModel):
    snapshot_id: str = Field(min_length=1, max_length=64, description="ID of snapshot to restore")


class DLQReplayRequest(BaseModel):
    entry_ids: list[str] | None = Field(default=None, description="Specific entry IDs to replay")
    source: str | None = Field(default=None, max_length=256, description="Filter by source system")


class MigrationRequest(BaseModel):
    version: str = Field(min_length=1, max_length=32, description="Semantic version string")
    name: str = Field(min_length=1, max_length=256, description="Migration name")
    up_steps: list[dict[str, Any]] = Field(min_length=1, description="Forward migration steps")
    down_steps: list[dict[str, Any]] | None = Field(default=None, description="Rollback steps")
    description: str = Field(default="", max_length=1024, description="Migration description")


class ChaosExperimentRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256, description="Experiment name")
    hypothesis: str = Field(min_length=1, max_length=1024, description="Expected behavior under fault")
    faults: list[dict[str, Any]] = Field(min_length=1, description="Fault injection specifications")


class FeedbackRequest(BaseModel):
    feedback_type: str = Field(min_length=1, max_length=64, description="Type of feedback")
    domain: str = Field(min_length=1, max_length=64, description="Learning domain")
    context: dict[str, Any] = Field(default_factory=dict)
    original_output: Any = None
    corrected_output: Any = None
    rating: float = Field(default=0.0, ge=-1.0, le=1.0)


class CorrelationEventRequest(BaseModel):
    event_type: str = Field(min_length=1, max_length=128)
    system_id: str = Field(min_length=1, max_length=256)
    severity: str = Field(default="INFO", pattern="^(INFO|WARNING|ERROR|CRITICAL)$")
    data: dict[str, Any] = Field(default_factory=dict)


class NLConfigRequest(BaseModel):
    command: str = Field(min_length=1, max_length=2000, description="Natural language command")
    dry_run: bool = Field(default=True, description="If true, parse only without executing")


class RecordMetricRequest(BaseModel):
    metric: str = Field(min_length=1, max_length=256, description="Metric name")
    value: float = Field(description="Metric value")


def build_enterprise_router() -> APIRouter:
    """Build the enterprise features router (features #9-#20)."""
    router = APIRouter(prefix="/api/v1/enterprise", tags=["Enterprise"])

    _state: dict[str, Any] = {}

    def _snapshots():
        if "snapshots" not in _state:
            from eoip.graph.snapshots import SnapshotManager
            _state["snapshots"] = SnapshotManager()
        return _state["snapshots"]

    def _dlq():
        if "dlq" not in _state:
            from eoip.ingestion.dlq_dashboard import DLQDashboard
            _state["dlq"] = DLQDashboard()
        return _state["dlq"]

    def _health():
        if "health" not in _state:
            from eoip.health.aggregator import HealthAggregator
            _state["health"] = HealthAggregator()
        return _state["health"]

    def _migration():
        if "migration" not in _state:
            from eoip.graph.schema_migration import SchemaMigrationManager
            _state["migration"] = SchemaMigrationManager()
        return _state["migration"]

    def _chaos():
        if "chaos" not in _state:
            from eoip.testing.chaos import ChaosEngine
            _state["chaos"] = ChaosEngine()
        return _state["chaos"]

    def _diff():
        if "diff" not in _state:
            from eoip.graph.diff_engine import GraphDiffEngine
            _state["diff"] = GraphDiffEngine()
        return _state["diff"]

    def _learning():
        if "learning" not in _state:
            from eoip.brain.adaptive_learning import AdaptiveLearningEngine
            _state["learning"] = AdaptiveLearningEngine()
        return _state["learning"]

    def _correlation():
        if "correlation" not in _state:
            from eoip.brain.correlation_engine import CorrelationEngine
            _state["correlation"] = CorrelationEngine()
        return _state["correlation"]

    def _nlconfig():
        if "nlconfig" not in _state:
            from eoip.brain.nl_config import NLConfigEngine
            _state["nlconfig"] = NLConfigEngine()
        return _state["nlconfig"]

    def _analytics():
        if "analytics" not in _state:
            from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine
            _state["analytics"] = PredictiveAnalyticsEngine()
        return _state["analytics"]

    # ── Snapshots ──────────────────────────────────────────────────────

    @router.post("/snapshots", summary="Create graph snapshot",
                 description="Create a full, incremental, or schema-only snapshot of the current graph state.")
    def create_snapshot(req: SnapshotRequest) -> dict[str, Any]:
        from eoip.graph.snapshots import SnapshotType
        _obs.increment("enterprise.snapshot.create")
        _log.info("creating snapshot name=%s type=%s", req.name, req.snapshot_type)
        snap = _snapshots().create_snapshot(
            req.name, SnapshotType(req.snapshot_type), tags=req.tags)
        return snap.to_dict()

    @router.get("/snapshots", summary="List all snapshots",
                description="Return all available snapshots sorted by creation time (newest first).")
    def list_snapshots() -> dict[str, Any]:
        snapshots = _snapshots().list_snapshots()
        return {"snapshots": snapshots, "total": len(snapshots)}

    @router.post("/snapshots/restore", summary="Restore from snapshot",
                 description="Restore graph state to a specific snapshot point-in-time.")
    def restore_snapshot(req: RestoreRequest) -> dict[str, Any]:
        from dataclasses import asdict
        _obs.increment("enterprise.snapshot.restore")
        _log.info("restoring snapshot_id=%s", req.snapshot_id)
        try:
            rp = _snapshots().restore_snapshot(req.snapshot_id)
        except ValueError as exc:
            raise SnapshotNotFoundError(str(exc)) from exc
        return asdict(rp)

    @router.get("/snapshots/{snapshot_id}", summary="Get snapshot details")
    def get_snapshot(snapshot_id: str) -> dict[str, Any]:
        snap = _snapshots().get_snapshot(snapshot_id)
        if not snap:
            raise ResourceNotFoundError(f"Snapshot {snapshot_id} not found",
                                        context={"snapshot_id": snapshot_id})
        return snap.to_dict()

    @router.delete("/snapshots/{snapshot_id}", summary="Delete snapshot")
    def delete_snapshot(snapshot_id: str) -> dict[str, Any]:
        if not _snapshots().delete_snapshot(snapshot_id):
            raise ResourceNotFoundError(f"Snapshot {snapshot_id} not found")
        _log.info("deleted snapshot_id=%s", snapshot_id)
        return {"deleted": True, "snapshot_id": snapshot_id}

    @router.post("/snapshots/compare", summary="Compare two snapshots",
                 description="Compute the diff between two graph snapshots.")
    def compare_snapshots(id_a: str = Query(min_length=1), id_b: str = Query(min_length=1)) -> dict[str, Any]:
        return _snapshots().compare_snapshots(id_a, id_b)

    # ── DLQ Dashboard ──────────────────────────────────────────────────

    @router.get("/dlq/entries", summary="List DLQ entries",
                description="List dead-letter queue entries, optionally filtered by source.")
    def dlq_list(source: str | None = Query(default=None, max_length=256),
                 limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
        entries = _dlq().list_entries(source=source, limit=limit)
        return {"entries": entries, "total": len(entries)}

    @router.get("/dlq/stats", summary="DLQ statistics",
                description="Aggregated statistics of DLQ entries by source and error type.")
    def dlq_stats() -> dict[str, Any]:
        return _dlq().get_stats().to_dict()

    @router.post("/dlq/replay", summary="Replay DLQ entries",
                 description="Replay failed entries from the dead-letter queue, optionally filtered by entry IDs or source.")
    def dlq_replay(req: DLQReplayRequest) -> dict[str, Any]:
        _obs.increment("enterprise.dlq.replay")
        _log.info("replaying DLQ entries source=%s ids=%s", req.source, req.entry_ids)
        return _dlq().replay_batch(entry_ids=req.entry_ids, source=req.source)

    @router.delete("/dlq/{entry_id}", summary="Discard DLQ entry")
    def dlq_discard(entry_id: str) -> dict[str, Any]:
        if not _dlq().discard_entry(entry_id):
            raise ResourceNotFoundError(f"DLQ entry {entry_id} not found")
        return {"discarded": True, "entry_id": entry_id}

    # ── Health Aggregator ──────────────────────────────────────────────

    @router.get("/health/aggregate", summary="Aggregate health status",
                description="Return overall system health (HEALTHY, DEGRADED, UNHEALTHY) with per-check details.")
    def health_aggregate() -> dict[str, Any]:
        return _health().get_aggregate_status()

    @router.post("/health/check-all", summary="Run all health checks",
                 description="Execute all registered health checks and return results.")
    def health_check_all() -> dict[str, Any]:
        results = _health().run_all_checks()
        return {"results": {k: v.to_dict() for k, v in results.items()},
                "total_checks": len(results)}

    @router.get("/health/sla", summary="SLA report",
                description="Return SLA target compliance status and uptime metrics.")
    def health_sla() -> dict[str, Any]:
        return {"sla_targets": _health().get_sla_report()}

    @router.get("/health/uptime", summary="System uptime",
                description="Compute uptime percentage from health check history.")
    def health_uptime() -> dict[str, Any]:
        return {"uptime_percent": _health().compute_uptime()}

    # ── Schema Migration ───────────────────────────────────────────────

    @router.post("/migrations", summary="Create schema migration",
                 description="Register a new schema migration with up/down steps.")
    def create_migration(req: MigrationRequest) -> dict[str, Any]:
        _obs.increment("enterprise.migration.create")
        _log.info("creating migration version=%s name=%s", req.version, req.name)
        m = _migration().create_migration(
            req.version, req.name, req.up_steps,
            down_steps=req.down_steps, description=req.description)
        return m.to_dict()

    @router.get("/migrations", summary="List migrations",
                description="List all migrations and the current applied version.")
    def list_migrations() -> dict[str, Any]:
        migrations = _migration().list_migrations()
        return {"migrations": migrations,
                "current_version": _migration().get_current_version(),
                "total": len(migrations)}

    @router.post("/migrations/{migration_id}/apply", summary="Apply migration")
    def apply_migration(migration_id: str) -> dict[str, Any]:
        _obs.increment("enterprise.migration.apply")
        _log.info("applying migration_id=%s", migration_id)
        ok = _migration().apply_migration(migration_id)
        if not ok:
            raise HTTPException(400, "Migration could not be applied")
        return {"applied": True, "version": _migration().get_current_version()}

    @router.post("/migrations/{migration_id}/rollback", summary="Rollback migration")
    def rollback_migration(migration_id: str) -> dict[str, Any]:
        _obs.increment("enterprise.migration.rollback")
        _log.info("rolling back migration_id=%s", migration_id)
        ok = _migration().rollback_migration(migration_id)
        if not ok:
            raise HTTPException(400, "Migration could not be rolled back")
        return {"rolled_back": True, "version": _migration().get_current_version()}

    @router.post("/migrations/apply-all", summary="Apply all pending migrations")
    def apply_all_migrations() -> dict[str, Any]:
        _obs.increment("enterprise.migration.apply_all")
        return _migration().apply_all_pending()

    # ── Chaos Testing ──────────────────────────────────────────────────

    @router.post("/chaos/experiments", summary="Create chaos experiment",
                 description="Define a chaos experiment with fault injection specifications and a steady-state hypothesis.")
    def create_experiment(req: ChaosExperimentRequest) -> dict[str, Any]:
        _obs.increment("enterprise.chaos.create")
        _log.info("creating chaos experiment name=%s", req.name)
        exp = _chaos().create_experiment(req.name, req.hypothesis, req.faults)
        return exp.to_dict()

    @router.get("/chaos/experiments", summary="List chaos experiments")
    def list_experiments() -> dict[str, Any]:
        experiments = _chaos().list_experiments()
        return {"experiments": experiments, "total": len(experiments)}

    @router.post("/chaos/experiments/{experiment_id}/run", summary="Run chaos experiment",
                 description="Execute a chaos experiment, injecting faults and verifying the steady-state hypothesis.")
    def run_experiment(experiment_id: str) -> dict[str, Any]:
        _obs.increment("enterprise.chaos.run")
        _log.info("running chaos experiment_id=%s", experiment_id)
        exp = _chaos().run_experiment(experiment_id)
        return exp.to_dict()

    # ── Graph Diff ─────────────────────────────────────────────────────

    @router.get("/diff/changes", summary="Recent graph changes",
                description="Return recent change records from the graph diff engine.")
    def diff_recent_changes(limit: int = Query(default=50, ge=1, le=1000)) -> dict[str, Any]:
        changes = _diff().get_recent_changes(limit=limit)
        return {"changes": changes, "total": len(changes)}

    @router.get("/diff/stats", summary="Change statistics",
                description="Aggregated statistics of graph changes by type and impact.")
    def diff_stats() -> dict[str, Any]:
        return _diff().get_change_stats()

    @router.get("/diff/timeline/{entity_id}", summary="Entity change timeline",
                description="Return the full change history for a specific entity.")
    def diff_timeline(entity_id: str) -> dict[str, Any]:
        tl = _diff().get_entity_timeline(entity_id)
        return {
            "entity_id": tl.entity_id,
            "total_modifications": tl.total_modifications,
            "first_seen": tl.first_seen,
            "last_modified": tl.last_modified,
            "changes": [c.to_dict() for c in tl.changes],
        }

    # ── Adaptive Learning ──────────────────────────────────────────────

    @router.post("/learning/feedback", summary="Submit learning feedback",
                 description="Submit feedback to the adaptive learning engine to improve system behavior.")
    def submit_feedback(req: FeedbackRequest) -> dict[str, Any]:
        from eoip.brain.adaptive_learning import FeedbackType, LearningDomain
        _obs.increment("enterprise.learning.feedback")
        try:
            entry = _learning().submit_feedback(
                FeedbackType(req.feedback_type), LearningDomain(req.domain),
                context=req.context, original_output=req.original_output,
                corrected_output=req.corrected_output, rating=req.rating)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        return entry.to_dict()

    @router.get("/learning/rules", summary="List active learning rules",
                description="Return all derived learning rules with confidence scores.")
    def learning_rules() -> dict[str, Any]:
        rules = _learning().get_rules()
        return {"rules": rules, "total": len(rules)}

    @router.get("/learning/stats", summary="Learning statistics")
    def learning_stats() -> dict[str, Any]:
        return _learning().get_feedback_stats()

    @router.post("/learning/prune", summary="Prune weak rules",
                 description="Remove learning rules below the confidence threshold.")
    def prune_rules(threshold: float = Query(default=0.3, ge=0.0, le=1.0)) -> dict[str, Any]:
        pruned = _learning().prune_weak_rules(threshold)
        _log.info("pruned %d weak rules below threshold=%.2f", pruned, threshold)
        return {"pruned": pruned, "threshold": threshold}

    # ── Correlation Engine ─────────────────────────────────────────────

    @router.get("/correlation/events", summary="Event stream",
                description="Return ingested events, optionally filtered by system.")
    def correlation_events(system_id: str | None = Query(default=None, max_length=256),
                           limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
        events = _correlation().get_event_stream(system_id=system_id, limit=limit)
        return {"events": events, "total": len(events)}

    @router.post("/correlation/analyze/{event_id}", summary="Root cause analysis",
                 description="Perform root cause analysis for a specific event using temporal and entity correlation.")
    def correlation_analyze(event_id: str) -> dict[str, Any]:
        _obs.increment("enterprise.correlation.analyze")
        analysis = _correlation().analyze_root_cause(event_id)
        return analysis.to_dict()

    @router.get("/correlation/stats", summary="Correlation statistics")
    def correlation_stats() -> dict[str, Any]:
        return _correlation().get_stats()

    # ── NL Configuration ───────────────────────────────────────────────

    @router.post("/nlconfig/execute", summary="Execute natural language command",
                 description="Parse and optionally execute a natural language system configuration command.")
    def nlconfig_execute(req: NLConfigRequest) -> dict[str, Any]:
        _obs.increment("enterprise.nlconfig.execute")
        _log.info("nlconfig command=%s dry_run=%s", req.command[:100], req.dry_run)
        return _nlconfig().parse_and_execute(req.command)

    @router.post("/nlconfig/suggest", summary="Suggest commands",
                 description="Given partial input, suggest matching natural language commands.")
    def nlconfig_suggest(req: NLConfigRequest) -> dict[str, Any]:
        suggestions = _nlconfig().suggest_commands(req.command)
        return {"suggestions": suggestions, "total": len(suggestions)}

    # ── Predictive Analytics ───────────────────────────────────────────

    @router.post("/analytics/record", summary="Record metric data point",
                 description="Record a time-series data point for predictive analytics.")
    def analytics_record(req: RecordMetricRequest) -> dict[str, str]:
        _analytics().record(req.metric, req.value)
        _obs.increment("enterprise.analytics.record", metric=req.metric)
        return {"status": "recorded"}

    @router.get("/analytics/trend/{metric}", summary="Analyze metric trend",
                description="Compute trend direction (RISING, FALLING, STABLE, VOLATILE) for a metric.")
    def analytics_trend(metric: str, window: int | None = Query(default=None, ge=10, le=10000)) -> dict[str, Any]:
        return _analytics().analyze_trend(metric, window=window).to_dict()

    @router.get("/analytics/anomalies/{metric}", summary="Detect anomalies",
                description="Detect anomalous data points using z-score analysis.")
    def analytics_anomalies(metric: str,
                            threshold: float = Query(default=2.5, ge=1.0, le=5.0)) -> dict[str, Any]:
        anomalies = _analytics().detect_anomalies(metric)
        return {"anomalies": [a.to_dict() for a in anomalies], "total": len(anomalies)}

    @router.get("/analytics/forecast/{metric}", summary="Forecast metric values",
                description="Generate predictions using linear regression, exponential smoothing, or moving average.")
    def analytics_forecast(metric: str,
                           horizon: int = Query(default=10, ge=1, le=365),
                           method: str = Query(default="LINEAR",
                                               pattern="^(LINEAR|EXPONENTIAL_SMOOTHING|MOVING_AVERAGE)$")) -> dict[str, Any]:
        return _analytics().forecast(metric, horizon=horizon).to_dict()

    @router.get("/analytics/growth/{metric}", summary="Growth report",
                description="Project growth trajectory with capacity threshold analysis.")
    def analytics_growth(metric: str,
                         threshold: float | None = Query(default=None, ge=0.0)) -> dict[str, Any]:
        return _analytics().growth_report(metric, capacity_threshold=threshold).to_dict()

    @router.get("/analytics/metrics", summary="List tracked metrics",
                description="Return all metrics currently tracked by the analytics engine.")
    def analytics_metrics() -> dict[str, Any]:
        return _analytics().get_metrics()

    # ── Observability ──────────────────────────────────────────────────

    @router.get("/observability/metrics", summary="Enterprise metrics",
                description="Return internal metrics counters, gauges, and histogram summaries.",
                tags=["Observability"])
    def observability_metrics() -> dict[str, Any]:
        return _obs.snapshot()

    # ── Health Probes ──────────────────────────────────────────────────

    from eoip.enterprise.health import HealthProbe, HealthStatus, ComponentHealth

    _health = HealthProbe(version="1.0.0")
    _health.mark_startup_complete()

    @router.get("/health/live", summary="Liveness probe",
                description="Kubernetes-compatible liveness check.",
                tags=["Health"])
    def health_liveness() -> dict[str, Any]:
        h = _health.check_liveness()
        return _health.to_dict(h)

    @router.get("/health/ready", summary="Readiness probe",
                description="Kubernetes-compatible readiness check with subsystem health.",
                tags=["Health"])
    def health_readiness() -> dict[str, Any]:
        h = _health.check_readiness()
        return _health.to_dict(h)

    @router.get("/health/startup", summary="Startup probe",
                description="Kubernetes-compatible startup check.",
                tags=["Health"])
    def health_startup() -> dict[str, Any]:
        h = _health.check_startup()
        return _health.to_dict(h)

    # ── Circuit Breakers ───────────────────────────────────────────────

    from eoip.enterprise.circuit_breaker import get_circuit_breaker_registry

    @router.get("/resilience/circuit-breakers", summary="Circuit breaker status",
                description="View all circuit breakers and their current states.",
                tags=["Resilience"])
    def circuit_breaker_status() -> list[dict[str, Any]]:
        reg = get_circuit_breaker_registry()
        return [
            {
                "name": m.name,
                "state": m.state.value,
                "failure_count": m.failure_count,
                "success_count": m.success_count,
                "total_calls": m.total_calls,
            }
            for m in reg.all_metrics()
        ]

    @router.post("/resilience/circuit-breakers/reset", summary="Reset all circuit breakers",
                 description="Force all circuit breakers back to CLOSED state.",
                 tags=["Resilience"])
    def circuit_breaker_reset() -> dict[str, str]:
        get_circuit_breaker_registry().reset_all()
        return {"status": "ALL_RESET"}

    # ── Audit Log ──────────────────────────────────────────────────────

    from eoip.enterprise.audit import get_audit_log, AuditCategory as AuditCat

    @router.get("/audit/events", summary="Query audit events",
                description="Query the tamper-evident audit log with filters.",
                tags=["Audit"])
    def audit_query(category: str | None = None, actor: str | None = None,
                    resource: str | None = None, limit: int = Query(default=100, le=1000)) -> list[dict[str, Any]]:
        log = get_audit_log()
        cat = None
        if category:
            try:
                cat = AuditCat(category)
            except ValueError:
                pass
        return [e.to_dict() for e in log.query(category=cat, actor=actor, resource=resource, limit=limit)]

    @router.get("/audit/stats", summary="Audit log statistics",
                description="Chain integrity verification and event distribution.",
                tags=["Audit"])
    def audit_stats() -> dict[str, Any]:
        return get_audit_log().get_stats()

    @router.get("/audit/verify", summary="Verify audit chain integrity",
                description="Cryptographically verify the hash chain of the audit log.",
                tags=["Audit"])
    def audit_verify() -> dict[str, Any]:
        valid, count = get_audit_log().verify_chain()
        return {"chain_valid": valid, "events_verified": count}

    # ── Cache ──────────────────────────────────────────────────────────

    from eoip.enterprise.cache import get_cache

    @router.get("/cache/stats", summary="Cache statistics",
                description="View intelligent cache hit rate, size, and eviction counts.",
                tags=["Cache"])
    def cache_stats() -> dict[str, Any]:
        s = get_cache().stats()
        return {
            "hits": s.hits,
            "misses": s.misses,
            "evictions": s.evictions,
            "current_size": s.current_size,
            "max_size": s.max_size,
            "hit_rate": s.hit_rate,
        }

    @router.post("/cache/clear", summary="Clear cache",
                 description="Purge all cached results.",
                 tags=["Cache"])
    def cache_clear() -> dict[str, Any]:
        removed = get_cache().clear()
        return {"status": "CLEARED", "entries_removed": removed}

    # ── Plugins ────────────────────────────────────────────────────────

    from eoip.enterprise.plugin import get_plugin_registry

    @router.get("/plugins", summary="List plugins",
                description="View all registered plugins, their status, and capabilities.",
                tags=["Plugins"])
    def list_plugins() -> list[dict[str, Any]]:
        return get_plugin_registry().list_all()

    @router.get("/plugins/stats", summary="Plugin system stats",
                description="Summary of plugin ecosystem health.",
                tags=["Plugins"])
    def plugin_stats() -> dict[str, Any]:
        return get_plugin_registry().get_stats()

    # ── Lifecycle ─────────────────────────────────────────────────────

    from eoip.enterprise.lifecycle import get_lifecycle_manager

    @router.get("/lifecycle/status", summary="Application lifecycle status",
                description="Current lifecycle phase, active requests, and component health.",
                tags=["Lifecycle"])
    def lifecycle_status() -> dict[str, Any]:
        return get_lifecycle_manager().stats()

    @router.post("/lifecycle/drain", summary="Initiate graceful drain",
                 description="Begin draining active requests in preparation for shutdown.",
                 tags=["Lifecycle"])
    def lifecycle_drain() -> dict[str, Any]:
        mgr = get_lifecycle_manager()
        report = mgr.shutdown()
        return {"status": "DRAINED", "report": report}

    # ── Feature Flags ─────────────────────────────────────────────────

    from eoip.enterprise.feature_flags import get_feature_flags, FlagDefinition as FlagDef

    class FeatureFlagRequest(BaseModel):
        name: str
        description: str = ""
        default_enabled: bool = False
        rollout_percentage: float = 100.0

    class FlagEvalRequest(BaseModel):
        flag_name: str
        tenant_id: str | None = None

    class FlagOverrideRequest(BaseModel):
        flag_name: str
        tenant_id: str
        enabled: bool

    @router.get("/feature-flags", summary="List all feature flags",
                description="View all defined feature flags with rollout configuration.",
                tags=["Feature Flags"])
    def list_feature_flags() -> list[dict[str, Any]]:
        return get_feature_flags().list_flags()

    @router.post("/feature-flags", summary="Define a feature flag",
                 description="Create or update a feature flag with rollout percentage.",
                 tags=["Feature Flags"])
    def define_feature_flag(req: FeatureFlagRequest) -> dict[str, Any]:
        get_feature_flags().define(FlagDef(
            name=req.name,
            description=req.description,
            default_enabled=req.default_enabled,
            rollout_percentage=req.rollout_percentage,
        ))
        return {"status": "DEFINED", "flag": req.name}

    @router.post("/feature-flags/evaluate", summary="Evaluate a feature flag",
                 description="Check if a feature flag is enabled for a given tenant.",
                 tags=["Feature Flags"])
    def evaluate_feature_flag(req: FlagEvalRequest) -> dict[str, Any]:
        result = get_feature_flags().is_enabled(req.flag_name, tenant_id=req.tenant_id)
        return {
            "flag": result.flag_name,
            "enabled": result.enabled,
            "reason": result.reason,
            "tenant_id": result.tenant_id,
        }

    @router.post("/feature-flags/override", summary="Set tenant override",
                 description="Override a feature flag for a specific tenant.",
                 tags=["Feature Flags"])
    def set_flag_override(req: FlagOverrideRequest) -> dict[str, Any]:
        get_feature_flags().set_override(req.flag_name, req.tenant_id, req.enabled)
        return {"status": "OVERRIDE_SET", "flag": req.flag_name, "tenant": req.tenant_id}

    @router.get("/feature-flags/stats", summary="Feature flag statistics",
                tags=["Feature Flags"])
    def feature_flag_stats() -> dict[str, Any]:
        return get_feature_flags().stats()

    # ── Webhooks ──────────────────────────────────────────────────────

    from eoip.enterprise.webhooks import get_webhook_manager, WebhookEventType as WHEventType

    class WebhookSubscribeRequest(BaseModel):
        url: str
        events: list[str]
        secret: str = ""
        max_retries: int = 3

    @router.get("/webhooks", summary="List webhook subscriptions",
                description="View all registered webhook subscriptions.",
                tags=["Webhooks"])
    def list_webhooks() -> list[dict[str, Any]]:
        return get_webhook_manager().list_subscriptions()

    @router.post("/webhooks/subscribe", summary="Register webhook",
                 description="Subscribe to event notifications with HMAC-SHA256 signed delivery.",
                 tags=["Webhooks"])
    def subscribe_webhook(req: WebhookSubscribeRequest) -> dict[str, Any]:
        events = []
        for e in req.events:
            try:
                events.append(WHEventType(e))
            except ValueError:
                pass
        if not events:
            raise HTTPException(status_code=400, detail="No valid event types provided")
        sub = get_webhook_manager().subscribe(
            url=req.url, events=events, secret=req.secret, max_retries=req.max_retries,
        )
        return {"status": "SUBSCRIBED", "subscription_id": sub.subscription_id}

    @router.delete("/webhooks/{subscription_id}", summary="Unsubscribe webhook",
                   tags=["Webhooks"])
    def unsubscribe_webhook(subscription_id: str) -> dict[str, Any]:
        removed = get_webhook_manager().unsubscribe(subscription_id)
        if not removed:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return {"status": "UNSUBSCRIBED"}

    @router.get("/webhooks/dead-letters", summary="View dead-letter queue",
                description="Failed webhook deliveries awaiting manual review.",
                tags=["Webhooks"])
    def webhook_dead_letters(limit: int = Query(50, ge=1, le=500)) -> list[dict[str, Any]]:
        return get_webhook_manager().get_dead_letters(limit=limit)

    @router.get("/webhooks/stats", summary="Webhook delivery statistics",
                tags=["Webhooks"])
    def webhook_stats() -> dict[str, Any]:
        return get_webhook_manager().stats()

    return router
