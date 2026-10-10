"""Unified API router for enterprise features #9-#20."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


# ── Request models ─────────────────────────────────────────────────────

class SnapshotRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    snapshot_type: str = "FULL"
    tags: dict[str, str] = Field(default_factory=dict)

class RestoreRequest(BaseModel):
    snapshot_id: str = Field(min_length=1)

class DLQReplayRequest(BaseModel):
    entry_ids: list[str] | None = None
    source: str | None = None

class MigrationRequest(BaseModel):
    version: str = Field(min_length=1)
    name: str = Field(min_length=1)
    up_steps: list[dict[str, Any]]
    down_steps: list[dict[str, Any]] | None = None
    description: str = ""

class ChaosExperimentRequest(BaseModel):
    name: str = Field(min_length=1)
    hypothesis: str = Field(min_length=1)
    faults: list[dict[str, Any]]

class FeedbackRequest(BaseModel):
    feedback_type: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)
    original_output: Any = None
    corrected_output: Any = None
    rating: float = 0.0

class NLConfigRequest(BaseModel):
    command: str = Field(min_length=1)

class RecordMetricRequest(BaseModel):
    metric: str = Field(min_length=1)
    value: float


def build_enterprise_router() -> APIRouter:
    """Build the enterprise features router (features #9-#20)."""
    router = APIRouter(prefix="/api/v1/enterprise", tags=["enterprise"])

    # Lazy singletons
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

    @router.post("/snapshots")
    def create_snapshot(req: SnapshotRequest) -> dict[str, Any]:
        from eoip.graph.snapshots import SnapshotType
        snap = _snapshots().create_snapshot(
            req.name, SnapshotType(req.snapshot_type), tags=req.tags)
        return snap.to_dict()

    @router.get("/snapshots")
    def list_snapshots() -> dict[str, Any]:
        return {"snapshots": _snapshots().list_snapshots()}

    @router.post("/snapshots/restore")
    def restore_snapshot(req: RestoreRequest) -> dict[str, Any]:
        from dataclasses import asdict
        rp = _snapshots().restore_snapshot(req.snapshot_id)
        return asdict(rp)

    # ── DLQ Dashboard ──────────────────────────────────────────────────

    @router.get("/dlq/entries")
    def dlq_list(source: str | None = None, limit: int = 50) -> dict[str, Any]:
        return {"entries": _dlq().list_entries(source=source, limit=limit)}

    @router.get("/dlq/stats")
    def dlq_stats() -> dict[str, Any]:
        return _dlq().get_stats().to_dict()

    @router.post("/dlq/replay")
    def dlq_replay(req: DLQReplayRequest) -> dict[str, Any]:
        return _dlq().replay_batch(entry_ids=req.entry_ids, source=req.source)

    # ── Health Aggregator ──────────────────────────────────────────────

    @router.get("/health/aggregate")
    def health_aggregate() -> dict[str, Any]:
        return _health().get_aggregate_status()

    @router.post("/health/check-all")
    def health_check_all() -> dict[str, Any]:
        results = _health().run_all_checks()
        return {"results": {k: v.to_dict() for k, v in results.items()}}

    @router.get("/health/sla")
    def health_sla() -> dict[str, Any]:
        return {"sla_targets": _health().get_sla_report()}

    # ── Schema Migration ───────────────────────────────────────────────

    @router.post("/migrations")
    def create_migration(req: MigrationRequest) -> dict[str, Any]:
        m = _migration().create_migration(
            req.version, req.name, req.up_steps,
            down_steps=req.down_steps, description=req.description)
        return m.to_dict()

    @router.get("/migrations")
    def list_migrations() -> dict[str, Any]:
        return {"migrations": _migration().list_migrations(),
                "current_version": _migration().get_current_version()}

    @router.post("/migrations/{migration_id}/apply")
    def apply_migration(migration_id: str) -> dict[str, Any]:
        ok = _migration().apply_migration(migration_id)
        if not ok:
            raise HTTPException(400, "Migration could not be applied")
        return {"applied": True, "version": _migration().get_current_version()}

    @router.post("/migrations/{migration_id}/rollback")
    def rollback_migration(migration_id: str) -> dict[str, Any]:
        ok = _migration().rollback_migration(migration_id)
        if not ok:
            raise HTTPException(400, "Migration could not be rolled back")
        return {"rolled_back": True, "version": _migration().get_current_version()}

    @router.post("/migrations/apply-all")
    def apply_all_migrations() -> dict[str, Any]:
        return _migration().apply_all_pending()

    # ── Chaos Testing ──────────────────────────────────────────────────

    @router.post("/chaos/experiments")
    def create_experiment(req: ChaosExperimentRequest) -> dict[str, Any]:
        exp = _chaos().create_experiment(req.name, req.hypothesis, req.faults)
        return exp.to_dict()

    @router.get("/chaos/experiments")
    def list_experiments() -> dict[str, Any]:
        return {"experiments": _chaos().list_experiments()}

    @router.post("/chaos/experiments/{experiment_id}/run")
    def run_experiment(experiment_id: str) -> dict[str, Any]:
        exp = _chaos().run_experiment(experiment_id)
        return exp.to_dict()

    # ── Graph Diff ─────────────────────────────────────────────────────

    @router.get("/diff/changes")
    def diff_recent_changes(limit: int = 50) -> dict[str, Any]:
        return {"changes": _diff().get_recent_changes(limit=limit)}

    @router.get("/diff/stats")
    def diff_stats() -> dict[str, Any]:
        return _diff().get_change_stats()

    @router.get("/diff/timeline/{entity_id}")
    def diff_timeline(entity_id: str) -> dict[str, Any]:
        from dataclasses import asdict
        tl = _diff().get_entity_timeline(entity_id)
        return {
            "entity_id": tl.entity_id,
            "total_modifications": tl.total_modifications,
            "first_seen": tl.first_seen,
            "last_modified": tl.last_modified,
            "changes": [c.to_dict() for c in tl.changes],
        }

    # ── Adaptive Learning ──────────────────────────────────────────────

    @router.post("/learning/feedback")
    def submit_feedback(req: FeedbackRequest) -> dict[str, Any]:
        from eoip.brain.adaptive_learning import FeedbackType, LearningDomain
        entry = _learning().submit_feedback(
            FeedbackType(req.feedback_type), LearningDomain(req.domain),
            context=req.context, original_output=req.original_output,
            corrected_output=req.corrected_output, rating=req.rating)
        return entry.to_dict()

    @router.get("/learning/rules")
    def learning_rules() -> dict[str, Any]:
        return {"rules": _learning().get_rules()}

    @router.get("/learning/stats")
    def learning_stats() -> dict[str, Any]:
        return _learning().get_feedback_stats()

    # ── Correlation Engine ─────────────────────────────────────────────

    @router.get("/correlation/events")
    def correlation_events(system_id: str | None = None, limit: int = 50) -> dict[str, Any]:
        return {"events": _correlation().get_event_stream(system_id=system_id, limit=limit)}

    @router.post("/correlation/analyze/{event_id}")
    def correlation_analyze(event_id: str) -> dict[str, Any]:
        analysis = _correlation().analyze_root_cause(event_id)
        return analysis.to_dict()

    @router.get("/correlation/stats")
    def correlation_stats() -> dict[str, Any]:
        return _correlation().get_stats()

    # ── NL Configuration ───────────────────────────────────────────────

    @router.post("/nlconfig/execute")
    def nlconfig_execute(req: NLConfigRequest) -> dict[str, Any]:
        return _nlconfig().parse_and_execute(req.command)

    @router.post("/nlconfig/suggest")
    def nlconfig_suggest(req: NLConfigRequest) -> dict[str, Any]:
        return {"suggestions": _nlconfig().suggest_commands(req.command)}

    # ── Predictive Analytics ───────────────────────────────────────────

    @router.post("/analytics/record")
    def analytics_record(req: RecordMetricRequest) -> dict[str, str]:
        _analytics().record(req.metric, req.value)
        return {"status": "recorded"}

    @router.get("/analytics/trend/{metric}")
    def analytics_trend(metric: str, window: int | None = None) -> dict[str, Any]:
        return _analytics().analyze_trend(metric, window=window).to_dict()

    @router.get("/analytics/anomalies/{metric}")
    def analytics_anomalies(metric: str) -> dict[str, Any]:
        return {"anomalies": [a.to_dict() for a in _analytics().detect_anomalies(metric)]}

    @router.get("/analytics/forecast/{metric}")
    def analytics_forecast(metric: str, horizon: int = 10) -> dict[str, Any]:
        return _analytics().forecast(metric, horizon=horizon).to_dict()

    @router.get("/analytics/growth/{metric}")
    def analytics_growth(metric: str, threshold: float | None = None) -> dict[str, Any]:
        return _analytics().growth_report(metric, capacity_threshold=threshold).to_dict()

    @router.get("/analytics/metrics")
    def analytics_metrics() -> dict[str, Any]:
        return _analytics().get_metrics()

    return router
