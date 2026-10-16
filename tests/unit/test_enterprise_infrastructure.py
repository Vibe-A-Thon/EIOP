"""Enterprise infrastructure tests — exceptions, config, logging, observability, middleware, models.

Tests the enterprise foundation layer that all features build on:
error hierarchy, configuration management, structured logging,
metrics collection, and API middleware.
"""

import pytest

pytestmark = [
    pytest.mark.enterprise,
    pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning"),
]


# ── Exception Hierarchy ───────────────────────────────────────────────────

class TestExceptionHierarchy:
    def test_all_enterprise_errors_inherit_base(self):
        from eoip.enterprise.exceptions import (
            CircuitOpenError, RateLimitExceeded, BulkheadFullError,
            SnapshotNotFoundError, MigrationError, ChaosError,
            LearningError, CorrelationError, NLConfigParseError,
            HealthCheckError, SLAViolationError,
            ResourceNotFoundError, ResourceConflictError,
            BatchProcessingError, StreamIngestionError,
            ValidationError, InvalidConfigurationError,
            EnterpriseError,
        )
        subclasses = [
            CircuitOpenError, RateLimitExceeded, BulkheadFullError,
            SnapshotNotFoundError, MigrationError, ChaosError,
            LearningError, CorrelationError, NLConfigParseError,
            HealthCheckError, SLAViolationError,
            ResourceNotFoundError, ResourceConflictError,
            BatchProcessingError, StreamIngestionError,
            ValidationError, InvalidConfigurationError,
        ]
        for cls in subclasses:
            assert issubclass(cls, EnterpriseError), f"{cls.__name__} must inherit EnterpriseError"

    def test_error_codes_are_unique(self):
        from eoip.enterprise import exceptions
        import inspect
        codes = {}
        for name, cls in inspect.getmembers(exceptions, inspect.isclass):
            if hasattr(cls, 'error_code') and cls is not exceptions.EnterpriseError:
                code = cls.error_code
                assert code not in codes or codes[code] is cls, (
                    f"Duplicate error code {code}: {codes.get(code, '')} and {name}"
                )
                codes[code] = cls
        assert len(codes) >= 15

    def test_error_to_dict(self):
        from eoip.enterprise.exceptions import CircuitOpenError
        err = CircuitOpenError("test msg", context={"circuit": "main"})
        d = err.to_dict()
        assert d["error_code"] == "EOIP-RES-001"
        assert d["message"] == "test msg"
        assert d["category"] == "RESILIENCE"
        assert d["severity"] == "HIGH"

    def test_error_preserves_cause(self):
        from eoip.enterprise.exceptions import SnapshotNotFoundError
        cause = ValueError("original")
        err = SnapshotNotFoundError("not found", cause=cause)
        assert err.__cause__ is cause

    def test_error_context_dict(self):
        from eoip.enterprise.exceptions import ResourceNotFoundError
        err = ResourceNotFoundError("missing", context={"id": "abc"})
        assert err.context == {"id": "abc"}

    def test_http_status_codes(self):
        from eoip.enterprise.exceptions import (
            CircuitOpenError, RateLimitExceeded, BulkheadTimeoutError,
            ResourceNotFoundError, ResourceConflictError,
            ValidationError, NLConfigParseError,
        )
        assert CircuitOpenError("x").http_status == 503
        assert RateLimitExceeded("x").http_status == 429
        assert BulkheadTimeoutError("x").http_status == 504
        assert ResourceNotFoundError("x").http_status == 404
        assert ResourceConflictError("x").http_status == 409
        assert ValidationError("x").http_status == 422
        assert NLConfigParseError("x").http_status == 422


# ── Configuration ─────────────────────────────────────────────────────────

class TestEnterpriseConfig:
    def test_default_config_values(self):
        from eoip.enterprise.config import EnterpriseConfig
        cfg = EnterpriseConfig()
        assert cfg.environment == "production"
        assert cfg.debug is False
        assert cfg.resilience.circuit_breaker_failure_threshold == 5
        assert cfg.resilience.pool_max_size == 10
        assert cfg.ingestion.batch_chunk_size == 500
        assert cfg.intelligence.learning_min_samples == 3
        assert cfg.chaos.enabled is False

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("EOIP_ENVIRONMENT", "staging")
        monkeypatch.setenv("EOIP_DEBUG", "true")
        monkeypatch.setenv("EOIP_CB_FAILURE_THRESHOLD", "10")
        from eoip.enterprise.config import EnterpriseConfig, ResilienceConfig, reset_enterprise_config
        reset_enterprise_config()
        cfg = EnterpriseConfig(
            environment="staging",
            debug=True,
            resilience=ResilienceConfig(circuit_breaker_failure_threshold=10),
        )
        assert cfg.environment == "staging"
        assert cfg.debug is True
        assert cfg.resilience.circuit_breaker_failure_threshold == 10

    def test_config_is_frozen(self):
        from eoip.enterprise.config import EnterpriseConfig
        cfg = EnterpriseConfig()
        with pytest.raises(AttributeError):
            cfg.environment = "test"

    def test_get_enterprise_config_singleton(self):
        from eoip.enterprise.config import get_enterprise_config, reset_enterprise_config
        reset_enterprise_config()
        c1 = get_enterprise_config()
        c2 = get_enterprise_config()
        assert c1 is c2

    def test_reset_clears_singleton(self):
        from eoip.enterprise.config import get_enterprise_config, reset_enterprise_config
        c1 = get_enterprise_config()
        reset_enterprise_config()
        c2 = get_enterprise_config()
        assert c1 is not c2

    def test_chaos_allowed_environments(self):
        from eoip.enterprise.config import ChaosConfig
        cc = ChaosConfig()
        assert "production" not in cc.allowed_environments
        assert "staging" in cc.allowed_environments


# ── Logging ───────────────────────────────────────────────────────────────

class TestEnterpriseLogging:
    def test_get_logger_returns_child(self):
        from eoip.enterprise.logging import get_logger, ENTERPRISE_LOGGER_NAME
        log = get_logger("test_module")
        assert log.name == f"{ENTERPRISE_LOGGER_NAME}.test_module"

    def test_correlation_id_propagation(self):
        from eoip.enterprise.logging import set_correlation_id, get_correlation_id
        set_correlation_id("test-123")
        assert get_correlation_id() == "test-123"
        set_correlation_id("")

    def test_log_filter_adds_context(self):
        import logging
        from eoip.enterprise.logging import get_logger, set_correlation_id, set_tenant_id
        set_correlation_id("cid-abc")
        set_tenant_id("tenant-xyz")
        log = get_logger("filter_test")
        record = log.makeRecord(log.name, logging.INFO, "", 0, "test", (), None)
        for f in log.filters:
            f.filter(record)
        assert record.correlation_id == "cid-abc"
        assert record.tenant_id == "tenant-xyz"
        set_correlation_id("")
        set_tenant_id("")


# ── Observability ─────────────────────────────────────────────────────────

class TestMetricsCollector:
    def test_counter_increment(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        m.increment("requests")
        m.increment("requests", 5)
        assert m.get_counter("requests") == 6

    def test_gauge_set(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        m.gauge_set("connections", 42.0)
        assert m.get_gauge("connections") == 42.0

    def test_histogram_summary(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        for v in [10, 20, 30, 40, 50]:
            m.observe("latency", float(v))
        summary = m.get_histogram_summary("latency")
        assert summary["count"] == 5
        assert summary["min"] == 10.0
        assert summary["max"] == 50.0
        assert summary["avg"] == 30.0

    def test_histogram_empty(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        summary = m.get_histogram_summary("nonexistent")
        assert summary["count"] == 0

    def test_labeled_metrics(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        m.increment("requests", method="GET")
        m.increment("requests", method="POST")
        assert m.get_counter("requests", method="GET") == 1
        assert m.get_counter("requests", method="POST") == 1

    def test_snapshot(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        m.increment("c")
        m.gauge_set("g", 1.0)
        m.observe("h", 2.0)
        snap = m.snapshot()
        assert "c" in snap["counters"]
        assert "g" in snap["gauges"]
        assert "h" in snap["histograms"]

    def test_reset(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        m.increment("c")
        m.reset()
        assert m.get_counter("c") == 0

    def test_timed_decorator(self):
        from eoip.enterprise.observability import MetricsCollector, timed
        import eoip.enterprise.observability as obs
        original = obs._metrics
        m = MetricsCollector()
        obs._metrics = m

        @timed("test_op")
        def my_func():
            return 42

        result = my_func()
        assert result == 42
        assert m.get_counter("test_op.success") == 1
        summary = m.get_histogram_summary("test_op.duration_ms")
        assert summary["count"] == 1
        obs._metrics = original

    def test_timed_decorator_on_error(self):
        from eoip.enterprise.observability import MetricsCollector, timed
        import eoip.enterprise.observability as obs
        original = obs._metrics
        m = MetricsCollector()
        obs._metrics = m

        @timed("fail_op")
        def failing():
            raise ValueError("boom")

        with pytest.raises(ValueError):
            failing()
        assert m.get_counter("fail_op.error") == 1
        obs._metrics = original

    def test_histogram_eviction(self):
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        for i in range(12000):
            m.observe("big", float(i))
        summary = m.get_histogram_summary("big")
        assert summary["count"] <= 10000

    def test_thread_safety(self):
        import threading
        from eoip.enterprise.observability import MetricsCollector
        m = MetricsCollector()
        errors = []

        def worker():
            try:
                for _ in range(100):
                    m.increment("threaded")
                    m.observe("threaded_hist", 1.0)
                    m.gauge_set("threaded_gauge", 1.0)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert not errors
        assert m.get_counter("threaded") == 1000


# ── Response Models ───────────────────────────────────────────────────────

class TestResponseModels:
    def test_error_response_serialization(self):
        from eoip.enterprise.models import ErrorResponse, ErrorDetail
        resp = ErrorResponse(
            error=ErrorDetail(code="EOIP-RES-001", message="test",
                              category="RESILIENCE", severity="HIGH"),
            correlation_id="abc-123",
        )
        d = resp.model_dump()
        assert d["error"]["code"] == "EOIP-RES-001"
        assert d["correlation_id"] == "abc-123"

    def test_snapshot_response(self):
        from eoip.enterprise.models import SnapshotResponse
        snap = SnapshotResponse(
            snapshot_id="abc", name="test", snapshot_type="FULL",
            status="READY", created_at="2025-01-01", entity_count=100,
            edge_count=50, size_bytes=1024, checksum="abc123",
        )
        assert snap.snapshot_id == "abc"

    def test_dlq_stats_response(self):
        from eoip.enterprise.models import DLQStatsResponse
        stats = DLQStatsResponse(total=100, pending=50, replayed=30,
                                  discarded=15, expired=5)
        d = stats.model_dump()
        assert d["total"] == 100

    def test_operation_result(self):
        from eoip.enterprise.models import OperationResult
        r = OperationResult(success=True, message="done")
        assert r.success is True


# ── Middleware ─────────────────────────────────────────────────────────────

class TestMiddleware:
    def test_build_error_response(self):
        from eoip.enterprise.middleware import build_error_response
        from eoip.enterprise.exceptions import RateLimitExceeded
        err = RateLimitExceeded("too fast")
        resp = build_error_response(err, correlation_id="cid-123")
        assert resp.status_code == 429
        import json
        body = json.loads(resp.body)
        assert body["error"]["code"] == "EOIP-RES-002"
        assert body["correlation_id"] == "cid-123"

    def test_error_response_without_correlation(self):
        from eoip.enterprise.middleware import build_error_response
        from eoip.enterprise.exceptions import ResourceNotFoundError
        err = ResourceNotFoundError("not found")
        resp = build_error_response(err)
        assert resp.status_code == 404
        import json
        body = json.loads(resp.body)
        assert "correlation_id" not in body


# ── Enterprise Router ─────────────────────────────────────────────────────

class TestEnterpriseRouter:
    def test_router_has_routes(self):
        from eoip.enterprise.router import build_enterprise_router
        r = build_enterprise_router()
        assert len(r.routes) >= 35

    def test_router_prefix(self):
        from eoip.enterprise.router import build_enterprise_router
        r = build_enterprise_router()
        assert r.prefix == "/api/v1/enterprise"

    def test_request_validation_snapshot(self):
        from eoip.enterprise.router import SnapshotRequest
        req = SnapshotRequest(name="test")
        assert req.snapshot_type == "FULL"

    def test_request_validation_snapshot_invalid_type(self):
        from eoip.enterprise.router import SnapshotRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            SnapshotRequest(name="test", snapshot_type="INVALID")

    def test_request_validation_feedback_rating_bounds(self):
        from eoip.enterprise.router import FeedbackRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            FeedbackRequest(feedback_type="CORRECTION", domain="QUERY",
                            rating=5.0)

    def test_request_validation_metric_empty_name(self):
        from eoip.enterprise.router import RecordMetricRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            RecordMetricRequest(metric="", value=1.0)

    def test_request_validation_migration_min_steps(self):
        from eoip.enterprise.router import MigrationRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            MigrationRequest(version="1.0", name="test", up_steps=[])

    def test_request_validation_chaos_empty_faults(self):
        from eoip.enterprise.router import ChaosExperimentRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            ChaosExperimentRequest(name="exp", hypothesis="test", faults=[])

    def test_nlconfig_request_max_length(self):
        from eoip.enterprise.router import NLConfigRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            NLConfigRequest(command="x" * 2001)
