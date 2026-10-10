"""Comprehensive tests for enterprise features #9-#20."""

import time
import threading
import pytest

pytest_plugins = []

pytestmark = pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")


# ── Feature 9: Resilience ──────────────────────────────────────────────

class TestCircuitBreaker:
    def test_starts_closed(self):
        from eoip.resilience.circuit_breaker import CircuitBreaker, CircuitState
        cb = CircuitBreaker("test")
        assert cb.state == CircuitState.CLOSED

    def test_opens_after_failures(self):
        from eoip.resilience.circuit_breaker import (
            CircuitBreaker, CircuitBreakerConfig, CircuitState, CircuitOpenError,
        )
        cb = CircuitBreaker("test", CircuitBreakerConfig(failure_threshold=3))
        for _ in range(3):
            with pytest.raises(ValueError):
                cb.call(lambda: (_ for _ in ()).throw(ValueError("fail")))
        assert cb.state == CircuitState.OPEN
        with pytest.raises(CircuitOpenError):
            cb.call(lambda: None)

    def test_reset(self):
        from eoip.resilience.circuit_breaker import CircuitBreaker, CircuitState
        cb = CircuitBreaker("test")
        cb._state = CircuitState.OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_metrics(self):
        from eoip.resilience.circuit_breaker import CircuitBreaker
        cb = CircuitBreaker("test")
        cb.call(lambda: 42)
        m = cb.get_metrics()
        assert m["total_calls"] == 1
        assert m["name"] == "test"


class TestConnectionPool:
    def test_acquire_release(self):
        from eoip.resilience.connection_pool import ConnectionPool
        pool = ConnectionPool("test", factory=lambda: object())
        conn = pool.acquire()
        assert conn is not None
        pool.release(conn)
        m = pool.get_metrics()
        assert m.total_acquired == 1
        assert m.total_released == 1

    def test_acquire_timeout(self):
        from eoip.resilience.connection_pool import ConnectionPool, PoolConfig
        pool = ConnectionPool("test", factory=lambda: object(),
                              config=PoolConfig(max_size=1))
        c1 = pool.acquire()
        with pytest.raises((TimeoutError, RuntimeError)):
            pool.acquire(timeout=0.2)
        pool.release(c1)

    def test_close(self):
        from eoip.resilience.connection_pool import ConnectionPool
        pool = ConnectionPool("test", factory=lambda: object())
        pool.acquire()
        pool.close()
        assert pool._closed

    def test_health_check(self):
        from eoip.resilience.connection_pool import ConnectionPool
        pool = ConnectionPool("test", factory=lambda: object())
        pool.acquire()
        result = pool.health_check()
        assert "healthy" in result


class TestRateLimiter:
    def test_token_bucket_allows(self):
        from eoip.resilience.rate_limiter import RateLimiter, RateLimitConfig
        rl = RateLimiter("test", RateLimitConfig(burst_size=5))
        for _ in range(5):
            assert rl.allow() is True

    def test_token_bucket_rejects(self):
        from eoip.resilience.rate_limiter import RateLimiter, RateLimitConfig
        rl = RateLimiter("test", RateLimitConfig(burst_size=2, refill_rate=0.0))
        rl.allow()
        rl.allow()
        assert rl.allow() is False

    def test_acquire_raises(self):
        from eoip.resilience.rate_limiter import (
            RateLimiter, RateLimitConfig, RateLimitExceeded,
        )
        rl = RateLimiter("test", RateLimitConfig(burst_size=1, refill_rate=0.0))
        rl.acquire()
        with pytest.raises(RateLimitExceeded):
            rl.acquire()

    def test_sliding_window(self):
        from eoip.resilience.rate_limiter import (
            RateLimiter, RateLimitConfig, RateLimitStrategy,
        )
        rl = RateLimiter("test", RateLimitConfig(
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            max_requests=3, window_seconds=60.0,
        ))
        assert rl.allow()
        assert rl.allow()
        assert rl.allow()
        assert rl.allow() is False

    def test_metrics(self):
        from eoip.resilience.rate_limiter import RateLimiter
        rl = RateLimiter("test")
        rl.allow()
        m = rl.get_metrics()
        assert m["total_allowed"] >= 1


class TestBulkhead:
    def test_execute(self):
        from eoip.resilience.bulkhead import Bulkhead
        bh = Bulkhead("test")
        result = bh.execute(lambda: 42)
        assert result == 42

    def test_full_rejects(self):
        from eoip.resilience.bulkhead import Bulkhead, BulkheadConfig, BulkheadFullError
        bh = Bulkhead("test", BulkheadConfig(max_concurrent=1, max_queue_size=0))
        event = threading.Event()

        def block():
            event.wait(timeout=2)

        t = threading.Thread(target=lambda: bh.execute(block), daemon=True)
        t.start()
        time.sleep(0.1)
        with pytest.raises(BulkheadFullError):
            bh.execute(lambda: None)
        event.set()
        t.join(timeout=1)

    def test_try_execute(self):
        from eoip.resilience.bulkhead import Bulkhead
        bh = Bulkhead("test")
        ok, result = bh.try_execute(lambda: 99)
        assert ok is True
        assert result == 99

    def test_metrics(self):
        from eoip.resilience.bulkhead import Bulkhead
        bh = Bulkhead("test")
        bh.execute(lambda: None)
        m = bh.get_metrics()
        assert m["total_completed"] == 1


# ── Feature 10: Batch & Streaming ──────────────────────────────────────

class TestBatchProcessor:
    def test_submit_and_complete(self):
        from eoip.ingestion.batch_streaming import BatchProcessor
        bp = BatchProcessor()
        records = [{"id": i} for i in range(10)]
        job = bp.submit("test-source", records)
        time.sleep(0.5)
        j = bp.get_job(job.job_id)
        assert j.processed_records == 10

    def test_cancel(self):
        from eoip.ingestion.batch_streaming import BatchProcessor, BatchConfig
        bp = BatchProcessor(config=BatchConfig(chunk_size=1))
        records = [{"id": i} for i in range(100)]
        job = bp.submit("test", records)
        bp.cancel(job.job_id)
        time.sleep(0.3)
        assert job.status.value in ("CANCELLED", "COMPLETED", "PARTIAL")

    def test_list_jobs(self):
        from eoip.ingestion.batch_streaming import BatchProcessor
        bp = BatchProcessor()
        bp.submit("src", [{"a": 1}])
        time.sleep(0.2)
        jobs = bp.list_jobs()
        assert len(jobs) >= 1


class TestStreamIngester:
    def test_create_and_ingest(self):
        from eoip.ingestion.batch_streaming import StreamIngester, StreamConfig, StreamMode
        flushed = []
        si = StreamIngester(
            config=StreamConfig(mode=StreamMode.RECORD_AT_A_TIME),
            flush_fn=lambda batch: flushed.extend(batch),
        )
        state = si.create_stream("test")
        si.start_stream(state.stream_id)
        si.ingest(state.stream_id, {"val": 1})
        si.stop_stream(state.stream_id)
        assert len(flushed) >= 1

    def test_backpressure(self):
        from eoip.ingestion.batch_streaming import StreamIngester, StreamConfig, StreamMode
        si = StreamIngester(config=StreamConfig(
            mode=StreamMode.RECORD_AT_A_TIME,
            max_buffer_size=5,
        ))
        state = si.create_stream("test")
        si.start_stream(state.stream_id)
        accepted = 0
        for i in range(10):
            if si.ingest(state.stream_id, {"i": i}):
                accepted += 1
        si.stop_stream(state.stream_id)
        assert accepted >= 1


# ── Feature 11: Snapshots ─────────────────────────────────────────────

class TestSnapshotManager:
    def test_create_snapshot(self):
        from eoip.graph.snapshots import SnapshotManager, SnapshotStatus
        sm = SnapshotManager()
        sm.set_current_data(entities={"e1": {"label": "Bug"}})
        snap = sm.create_snapshot("v1")
        assert snap.status == SnapshotStatus.READY
        assert snap.entity_count == 1

    def test_restore_snapshot(self):
        from eoip.graph.snapshots import SnapshotManager
        sm = SnapshotManager()
        sm.set_current_data(entities={"e1": {"label": "Bug"}})
        snap = sm.create_snapshot("v1")
        sm.set_current_data(entities={})
        rp = sm.restore_snapshot(snap.snapshot_id)
        assert rp.success
        assert rp.entities_restored == 1

    def test_compare_snapshots(self):
        from eoip.graph.snapshots import SnapshotManager
        sm = SnapshotManager()
        sm.set_current_data(entities={"e1": {"label": "A"}})
        s1 = sm.create_snapshot("v1")
        sm.set_current_data(entities={"e1": {"label": "A"}, "e2": {"label": "B"}})
        s2 = sm.create_snapshot("v2")
        diff = sm.compare_snapshots(s1.snapshot_id, s2.snapshot_id)
        assert "e2" in diff["added"]

    def test_delete_snapshot(self):
        from eoip.graph.snapshots import SnapshotManager
        sm = SnapshotManager()
        snap = sm.create_snapshot("v1")
        assert sm.delete_snapshot(snap.snapshot_id) is True
        assert sm.get_snapshot(snap.snapshot_id) is None


# ── Feature 12: DLQ Dashboard ─────────────────────────────────────────

class TestDLQDashboard:
    def test_add_and_list(self):
        from eoip.ingestion.dlq_dashboard import DLQDashboard
        dlq = DLQDashboard()
        dlq.add_entry("jira", "pipe-1", {"key": "PROJ-1"}, "Timeout")
        entries = dlq.list_entries()
        assert len(entries) == 1

    def test_replay(self):
        from eoip.ingestion.dlq_dashboard import DLQDashboard, DLQEntryStatus
        dlq = DLQDashboard(replay_fn=lambda rec: True)
        entry = dlq.add_entry("jira", "p1", {"k": "v"}, "err")
        assert dlq.replay_entry(entry.entry_id) is True
        assert entry.status == DLQEntryStatus.REPLAYED

    def test_replay_batch(self):
        from eoip.ingestion.dlq_dashboard import DLQDashboard
        dlq = DLQDashboard(replay_fn=lambda rec: True)
        dlq.add_entry("s1", "p1", {}, "e1")
        dlq.add_entry("s1", "p1", {}, "e2")
        result = dlq.replay_batch(source="s1")
        assert result["succeeded"] == 2

    def test_stats(self):
        from eoip.ingestion.dlq_dashboard import DLQDashboard
        dlq = DLQDashboard()
        dlq.add_entry("jira", "p1", {}, "err", error_type="timeout")
        stats = dlq.get_stats()
        assert stats.total_entries == 1
        assert stats.by_error_type["timeout"] == 1

    def test_discard(self):
        from eoip.ingestion.dlq_dashboard import DLQDashboard, DLQEntryStatus
        dlq = DLQDashboard()
        entry = dlq.add_entry("s1", "p1", {}, "e")
        dlq.discard_entry(entry.entry_id)
        assert entry.status == DLQEntryStatus.DISCARDED


# ── Feature 13: Health Aggregator ──────────────────────────────────────

class TestHealthAggregator:
    def test_register_and_run(self):
        from eoip.health.aggregator import HealthAggregator, HealthCheck, HealthStatus
        ha = HealthAggregator()
        ha.register_check(HealthCheck(
            name="jira", target="jira-1",
            check_fn=lambda: {"status": "HEALTHY", "message": "OK"},
        ))
        result = ha.run_check("jira-1")
        assert result.status == HealthStatus.HEALTHY

    def test_aggregate_status(self):
        from eoip.health.aggregator import HealthAggregator, HealthCheck
        ha = HealthAggregator()
        ha.register_check(HealthCheck(
            name="a", target="a",
            check_fn=lambda: {"status": "HEALTHY"},
        ))
        ha.run_all_checks()
        agg = ha.get_aggregate_status()
        assert agg["overall_status"] == "HEALTHY"

    def test_sla_tracking(self):
        from eoip.health.aggregator import HealthAggregator, SLATarget, SLAMetric
        ha = HealthAggregator()
        ha.add_sla_target(SLATarget(
            name="uptime", metric=SLAMetric.UPTIME,
            target_value=0.99, warning_threshold=0.95, current_value=1.0,
        ))
        report = ha.get_sla_report()
        assert report[0]["met"] is True

    def test_uptime_computation(self):
        from eoip.health.aggregator import HealthAggregator, HealthCheck
        ha = HealthAggregator()
        ha.register_check(HealthCheck(
            name="x", target="x",
            check_fn=lambda: {"status": "HEALTHY"},
        ))
        ha.run_check("x")
        ha.run_check("x")
        assert ha.compute_uptime("x") == 1.0


# ── Feature 14: Schema Migration ──────────────────────────────────────

class TestSchemaMigration:
    def test_create_and_apply(self):
        from eoip.graph.schema_migration import SchemaMigrationManager
        sm = SchemaMigrationManager()
        m = sm.create_migration("1.0.0", "add-bug-type", up_steps=[
            {"action": "ADD_VERTEX_TYPE", "target": "Bug", "params": {"properties": ["summary"]}}
        ])
        assert sm.apply_migration(m.migration_id) is True
        assert sm.get_current_version() == "1.0.0"
        state = sm.get_schema_state()
        assert "Bug" in state["vertex_types"]

    def test_rollback(self):
        from eoip.graph.schema_migration import SchemaMigrationManager
        sm = SchemaMigrationManager()
        m = sm.create_migration("1.0.0", "add-bug", up_steps=[
            {"action": "ADD_VERTEX_TYPE", "target": "Bug", "params": {}}
        ], down_steps=[
            {"action": "REMOVE_VERTEX_TYPE", "target": "Bug", "params": {}}
        ])
        sm.apply_migration(m.migration_id)
        assert sm.rollback_migration(m.migration_id) is True
        assert sm.get_current_version() == "0.0.0"

    def test_apply_all_pending(self):
        from eoip.graph.schema_migration import SchemaMigrationManager
        sm = SchemaMigrationManager()
        sm.create_migration("1.0.0", "m1", up_steps=[
            {"action": "ADD_VERTEX_TYPE", "target": "A", "params": {}}
        ])
        sm.create_migration("2.0.0", "m2", up_steps=[
            {"action": "ADD_VERTEX_TYPE", "target": "B", "params": {}}
        ])
        result = sm.apply_all_pending()
        assert len(result["applied"]) == 2
        assert sm.get_current_version() == "2.0.0"

    def test_list_migrations(self):
        from eoip.graph.schema_migration import SchemaMigrationManager
        sm = SchemaMigrationManager()
        sm.create_migration("1.0.0", "m1", up_steps=[
            {"action": "ADD_PROPERTY", "target": "name", "params": {"type": "string"}}
        ])
        migs = sm.list_migrations()
        assert len(migs) == 1


# ── Feature 15: Chaos Testing ─────────────────────────────────────────

class TestChaosEngine:
    def test_create_experiment(self):
        from eoip.testing.chaos import ChaosEngine
        ce = ChaosEngine()
        exp = ce.create_experiment("test", "System stays healthy under latency", faults=[
            {"fault_type": "LATENCY", "target": "db", "latency_ms": 100}
        ])
        assert exp.name == "test"

    def test_run_experiment(self):
        from eoip.testing.chaos import ChaosEngine
        ce = ChaosEngine(steady_state_fn=lambda: {"status": "ok"})
        exp = ce.create_experiment("t", "h", faults=[
            {"fault_type": "LATENCY", "target": "x", "latency_ms": 1}
        ])
        result = ce.run_experiment(exp.experiment_id)
        assert result.verdict in ("PASSED", "HYPOTHESIS_DISPROVED")

    def test_fault_injector(self):
        from eoip.testing.chaos import FaultInjector, FaultConfig, FaultType, ChaosError
        fi = FaultInjector()
        fid = fi.activate(FaultConfig(
            fault_type=FaultType.ERROR, target="api",
            error_message="injected",
        ))
        with pytest.raises(ChaosError):
            fi.intercept("api", lambda: None)
        fi.deactivate(fid)
        assert fi.intercept("api", lambda: 42) == 42

    def test_list_experiments(self):
        from eoip.testing.chaos import ChaosEngine
        ce = ChaosEngine()
        ce.create_experiment("e1", "h1", faults=[])
        assert len(ce.list_experiments()) == 1


# ── Feature 16: Graph Diff ────────────────────────────────────────────

class TestGraphDiffEngine:
    def test_diff_added_entities(self):
        from eoip.graph.diff_engine import GraphDiffEngine
        gd = GraphDiffEngine()
        state_a = {"entities": {"e1": {"label": "Bug"}}, "edges": []}
        state_b = {"entities": {"e1": {"label": "Bug"}, "e2": {"label": "Task"}}, "edges": []}
        result = gd.diff(state_a, state_b)
        assert result.summary.get("ENTITY_ADDED", 0) == 1

    def test_diff_removed_entities(self):
        from eoip.graph.diff_engine import GraphDiffEngine
        gd = GraphDiffEngine()
        state_a = {"entities": {"e1": {}, "e2": {}}, "edges": []}
        state_b = {"entities": {"e1": {}}, "edges": []}
        result = gd.diff(state_a, state_b)
        assert result.summary.get("ENTITY_REMOVED", 0) == 1

    def test_diff_property_change(self):
        from eoip.graph.diff_engine import GraphDiffEngine
        gd = GraphDiffEngine()
        state_a = {"entities": {"e1": {"properties": {"status": "open"}}}, "edges": []}
        state_b = {"entities": {"e1": {"properties": {"status": "closed"}}}, "edges": []}
        result = gd.diff(state_a, state_b)
        assert result.summary.get("PROPERTY_CHANGED", 0) >= 1

    def test_record_and_timeline(self):
        from eoip.graph.diff_engine import GraphDiffEngine, ChangeType
        gd = GraphDiffEngine()
        gd.record_change(ChangeType.ENTITY_ADDED, "e1", entity_label="Bug")
        gd.record_change(ChangeType.PROPERTY_CHANGED, "e1", property_name="status")
        tl = gd.get_entity_timeline("e1")
        assert tl.total_modifications == 2

    def test_change_stats(self):
        from eoip.graph.diff_engine import GraphDiffEngine, ChangeType
        gd = GraphDiffEngine()
        gd.record_change(ChangeType.ENTITY_ADDED, "e1")
        stats = gd.get_change_stats()
        assert stats["total_changes"] == 1


# ── Feature 17: Adaptive Learning ─────────────────────────────────────

class TestAdaptiveLearning:
    def test_submit_feedback(self):
        from eoip.brain.adaptive_learning import (
            AdaptiveLearningEngine, FeedbackType, LearningDomain,
        )
        engine = AdaptiveLearningEngine()
        entry = engine.submit_feedback(
            FeedbackType.CORRECTION, LearningDomain.SCHEMA_MAPPING,
            context={"source": "jira", "field": "assignee"},
            original_output="Person", corrected_output="User",
        )
        assert entry.feedback_type == FeedbackType.CORRECTION

    def test_rule_derivation(self):
        from eoip.brain.adaptive_learning import (
            AdaptiveLearningEngine, FeedbackType, LearningDomain,
        )
        engine = AdaptiveLearningEngine()
        ctx = {"source": "jira", "field": "assignee"}
        for _ in range(5):
            engine.submit_feedback(
                FeedbackType.CORRECTION, LearningDomain.SCHEMA_MAPPING,
                context=ctx, original_output="Person", corrected_output="User",
            )
        rules = engine.get_rules(LearningDomain.SCHEMA_MAPPING)
        assert len(rules) >= 1

    def test_apply_rules(self):
        from eoip.brain.adaptive_learning import (
            AdaptiveLearningEngine, FeedbackType, LearningDomain,
        )
        engine = AdaptiveLearningEngine()
        ctx = {"source": "jira", "field": "assignee"}
        for _ in range(5):
            engine.submit_feedback(
                FeedbackType.CORRECTION, LearningDomain.SCHEMA_MAPPING,
                context=ctx, corrected_output="User",
            )
        result = engine.apply_rules(LearningDomain.SCHEMA_MAPPING, ctx, "Person")
        assert result == "User"

    def test_stats(self):
        from eoip.brain.adaptive_learning import (
            AdaptiveLearningEngine, FeedbackType, LearningDomain,
        )
        engine = AdaptiveLearningEngine()
        engine.submit_feedback(FeedbackType.APPROVAL, LearningDomain.CLASSIFICATION)
        stats = engine.get_feedback_stats()
        assert stats["total_feedback"] == 1


# ── Feature 18: Correlation Engine ────────────────────────────────────

class TestCorrelationEngine:
    def test_ingest_event(self):
        from eoip.brain.correlation_engine import CorrelationEngine, EventSeverity
        ce = CorrelationEngine()
        event = ce.ingest_event("jira", "sync_failed", EventSeverity.ERROR)
        assert event.system_id == "jira"

    def test_temporal_correlation(self):
        from eoip.brain.correlation_engine import CorrelationEngine, EventSeverity
        ce = CorrelationEngine(temporal_window_seconds=60)
        e1 = ce.ingest_event("jira", "sync_failed", EventSeverity.ERROR)
        ce.ingest_event("github", "webhook_timeout", EventSeverity.WARNING)
        corr = ce.correlate_temporal(e1.event_id)
        assert len(corr.events) >= 2

    def test_entity_correlation(self):
        from eoip.brain.correlation_engine import CorrelationEngine
        ce = CorrelationEngine()
        ce.ingest_event("jira", "updated", entity_id="PROJ-123")
        ce.ingest_event("github", "pr_merged", entity_id="PROJ-123")
        corr = ce.correlate_by_entity("PROJ-123")
        assert len(corr.systems) == 2

    def test_root_cause_analysis(self):
        from eoip.brain.correlation_engine import CorrelationEngine, EventSeverity
        ce = CorrelationEngine()
        e1 = ce.ingest_event("db", "connection_pool_exhausted", EventSeverity.CRITICAL)
        ce.ingest_event("jira", "sync_timeout", EventSeverity.ERROR)
        analysis = ce.analyze_root_cause(e1.event_id)
        assert len(analysis.affected_systems) >= 1
        assert len(analysis.recommendations) > 0

    def test_stats(self):
        from eoip.brain.correlation_engine import CorrelationEngine
        ce = CorrelationEngine()
        ce.ingest_event("a", "x")
        stats = ce.get_stats()
        assert stats["total_events"] == 1


# ── Feature 19: NL Configuration ──────────────────────────────────────

class TestNLConfigEngine:
    def test_parse_register(self):
        from eoip.brain.nl_config import NLConfigEngine, IntentType
        nl = NLConfigEngine()
        cmd = nl.parse("register a new jira system")
        assert cmd.intent == IntentType.REGISTER_SYSTEM
        assert cmd.entities.get("system_type") == "jira"

    def test_parse_schedule(self):
        from eoip.brain.nl_config import NLConfigEngine, IntentType
        nl = NLConfigEngine()
        cmd = nl.parse("schedule sync every 30 minutes")
        assert cmd.intent == IntentType.SET_SCHEDULE
        assert cmd.parameters.get("interval") == 30

    def test_parse_enable(self):
        from eoip.brain.nl_config import NLConfigEngine, IntentType
        nl = NLConfigEngine()
        cmd = nl.parse("enable real-time streaming")
        assert cmd.intent == IntentType.ENABLE_FEATURE

    def test_parse_status(self):
        from eoip.brain.nl_config import NLConfigEngine, IntentType
        nl = NLConfigEngine()
        cmd = nl.parse("show status of github")
        assert cmd.intent == IntentType.QUERY_STATUS

    def test_execute_dry_run(self):
        from eoip.brain.nl_config import NLConfigEngine
        nl = NLConfigEngine()
        result = nl.parse_and_execute("register a jira system")
        assert result["result"]["dry_run"] is True

    def test_suggest_commands(self):
        from eoip.brain.nl_config import NLConfigEngine
        nl = NLConfigEngine()
        suggestions = nl.suggest_commands("register")
        assert len(suggestions) >= 1


# ── Feature 20: Predictive Analytics ──────────────────────────────────

class TestPredictiveAnalytics:
    def test_record_and_trend(self):
        from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine, TrendDirection
        pa = PredictiveAnalyticsEngine()
        for i in range(20):
            pa.record("entity_count", 100 + i * 5)
        trend = pa.analyze_trend("entity_count")
        assert trend.direction == TrendDirection.RISING
        assert trend.slope > 0

    def test_anomaly_detection(self):
        from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine
        pa = PredictiveAnalyticsEngine()
        for _ in range(50):
            pa.record("latency", 100)
        pa.record("latency", 500)
        anomalies = pa.detect_anomalies("latency")
        assert len(anomalies) >= 1
        assert anomalies[-1].value == 500

    def test_forecast(self):
        from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine, ForecastMethod
        pa = PredictiveAnalyticsEngine()
        for i in range(30):
            pa.record("count", 10 + i)
        fc = pa.forecast("count", horizon=5, method=ForecastMethod.LINEAR)
        assert len(fc.predictions) == 5
        assert fc.predictions[0]["value"] > 30

    def test_growth_report(self):
        from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine
        pa = PredictiveAnalyticsEngine()
        for i in range(20):
            pa.record("nodes", 1000 + i * 50)
        report = pa.growth_report("nodes", capacity_threshold=5000)
        assert report.growth_rate > 0
        assert report.projected_value_30d > report.current_value

    def test_metrics(self):
        from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine
        pa = PredictiveAnalyticsEngine()
        pa.record("x", 1)
        m = pa.get_metrics()
        assert m["tracked_metrics"] == 1

    def test_stable_trend(self):
        from eoip.brain.predictive_analytics import PredictiveAnalyticsEngine, TrendDirection
        pa = PredictiveAnalyticsEngine()
        for _ in range(20):
            pa.record("flat", 100)
        trend = pa.analyze_trend("flat")
        assert trend.direction == TrendDirection.STABLE
