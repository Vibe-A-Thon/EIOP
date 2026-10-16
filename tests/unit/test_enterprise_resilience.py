"""Tests for enterprise resilience infrastructure: circuit breaker, rate limiter,
audit log, health probes, caching, and plugin system."""

from __future__ import annotations

import time

import pytest

from eoip.enterprise.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerRegistry,
    CircuitOpenError,
    CircuitState,
)
from eoip.enterprise.rate_limiter import RateLimiter
from eoip.enterprise.audit import AuditLog, AuditCategory, AuditSeverity
from eoip.enterprise.health import (
    HealthProbe,
    HealthStatus,
    ProbeType,
    ComponentHealth,
)
from eoip.enterprise.cache import IntelligentCache
from eoip.enterprise.plugin import (
    PluginRegistry,
    PluginMetadata,
    PluginCapability,
    PluginStatus,
)


# ---------------------------------------------------------------------------
# Circuit Breaker
# ---------------------------------------------------------------------------
@pytest.mark.enterprise
class TestCircuitBreaker:
    def test_starts_closed(self):
        cb = CircuitBreaker("test", failure_threshold=3, timeout_seconds=1.0)
        assert cb.state == CircuitState.CLOSED

    def test_opens_after_threshold(self):
        cb = CircuitBreaker("test", failure_threshold=2, timeout_seconds=60.0)
        for _ in range(2):
            with pytest.raises(ValueError):
                cb.call(lambda: (_ for _ in ()).throw(ValueError("boom")))
        assert cb.state == CircuitState.OPEN

    def test_rejects_when_open(self):
        cb = CircuitBreaker("test", failure_threshold=1, timeout_seconds=60.0)
        with pytest.raises(ValueError):
            cb.call(lambda: (_ for _ in ()).throw(ValueError("boom")))
        with pytest.raises(CircuitOpenError) as exc_info:
            cb.call(lambda: "ok")
        assert exc_info.value.retry_after > 0

    def test_closes_after_successful_half_open(self):
        cb = CircuitBreaker("test", failure_threshold=1, timeout_seconds=0.01, half_open_max=1)
        with pytest.raises(ValueError):
            cb.call(lambda: (_ for _ in ()).throw(ValueError("boom")))
        time.sleep(0.02)
        assert cb.state == CircuitState.HALF_OPEN
        result = cb.call(lambda: "recovered")
        assert result == "recovered"
        assert cb.state == CircuitState.CLOSED

    def test_metrics(self):
        cb = CircuitBreaker("metrics_test", failure_threshold=5)
        cb.call(lambda: "ok")
        m = cb.get_metrics()
        assert m.success_count == 1
        assert m.total_calls == 1
        assert m.state == CircuitState.CLOSED

    def test_reset(self):
        cb = CircuitBreaker("reset_test", failure_threshold=1, timeout_seconds=60.0)
        with pytest.raises(ValueError):
            cb.call(lambda: (_ for _ in ()).throw(ValueError("boom")))
        assert cb.state == CircuitState.OPEN
        cb.reset()
        assert cb.state == CircuitState.CLOSED

    def test_registry(self):
        reg = CircuitBreakerRegistry()
        cb1 = reg.get_or_create("svc_a")
        cb2 = reg.get_or_create("svc_a")
        assert cb1 is cb2
        assert len(reg.all_metrics()) == 1


# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------
@pytest.mark.enterprise
class TestRateLimiter:
    def test_allows_within_limit(self):
        rl = RateLimiter(max_requests=10, window_seconds=1.0, burst_size=5)
        result = rl.check("client_1")
        assert result.allowed is True
        assert result.remaining > 0

    def test_rejects_over_limit(self):
        rl = RateLimiter(max_requests=2, window_seconds=60.0, burst_size=0)
        rl.check("client_x")
        rl.check("client_x")
        result = rl.check("client_x")
        assert result.allowed is False
        assert result.retry_after is not None

    def test_status(self):
        rl = RateLimiter(max_requests=100, window_seconds=60.0, burst_size=20)
        rl.check("a")
        rl.check("b")
        status = rl.get_status()
        assert status["max_requests"] == 100
        assert status["active_clients"] == 2


# ---------------------------------------------------------------------------
# Audit Log
# ---------------------------------------------------------------------------
@pytest.mark.enterprise
class TestAuditLog:
    def test_record_and_query(self):
        log = AuditLog()
        event = log.record(
            category=AuditCategory.GRAPH_MUTATION,
            action="upsert_vertex",
            resource="vertex:svc:auth",
            actor="user@example.com",
        )
        assert event.event_id
        assert event.event_hash
        assert event.category == AuditCategory.GRAPH_MUTATION

        results = log.query(category=AuditCategory.GRAPH_MUTATION)
        assert len(results) == 1
        assert results[0].event_id == event.event_id

    def test_hash_chain_integrity(self):
        log = AuditLog()
        for i in range(5):
            log.record(AuditCategory.QUERY_EXECUTION, f"query_{i}", f"resource_{i}")
        valid, count = log.verify_chain()
        assert valid is True
        assert count == 5

    def test_stats(self):
        log = AuditLog()
        log.record(AuditCategory.GRAPH_MUTATION, "create", "v1")
        log.record(AuditCategory.QUERY_EXECUTION, "read", "v2")
        log.record(AuditCategory.GRAPH_MUTATION, "update", "v3")
        stats = log.get_stats()
        assert stats["total_events"] == 3
        assert stats["chain_valid"] is True
        assert stats["category_distribution"]["GRAPH_MUTATION"] == 2


# ---------------------------------------------------------------------------
# Health Probes
# ---------------------------------------------------------------------------
@pytest.mark.enterprise
class TestHealthProbe:
    def test_healthy_system(self):
        probe = HealthProbe(version="1.0.0")
        probe.register("test_component", lambda: ComponentHealth(
            name="test_component", status=HealthStatus.HEALTHY, latency_ms=1.0,
        ))
        probe.mark_startup_complete()
        health = probe.check_liveness()
        assert health.status == HealthStatus.HEALTHY
        assert len(health.components) == 1

    def test_unhealthy_critical_component(self):
        probe = HealthProbe()
        probe.register("critical_db", lambda: ComponentHealth(
            name="critical_db", status=HealthStatus.UNHEALTHY, latency_ms=0.0,
            details={"error": "Connection refused"},
        ), critical=True)
        health = probe.check_readiness()
        assert health.status == HealthStatus.UNHEALTHY

    def test_degraded_non_critical(self):
        probe = HealthProbe()
        probe.register("optional_svc", lambda: ComponentHealth(
            name="optional_svc", status=HealthStatus.DEGRADED, latency_ms=0.0,
        ), critical=False)
        health = probe.check_readiness()
        assert health.status == HealthStatus.DEGRADED

    def test_startup_not_complete(self):
        probe = HealthProbe()
        health = probe.check_startup()
        assert health.status == HealthStatus.UNHEALTHY

    def test_to_dict(self):
        probe = HealthProbe(version="2.0.0")
        probe.mark_startup_complete()
        health = probe.check_liveness()
        d = probe.to_dict(health)
        assert d["version"] == "2.0.0"
        assert d["status"] == "HEALTHY"


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
@pytest.mark.enterprise
class TestIntelligentCache:
    def test_put_and_get(self):
        cache = IntelligentCache(max_size=10, default_ttl=60.0)
        cache.put("k1", {"result": "data"})
        assert cache.get("k1") == {"result": "data"}

    def test_ttl_expiry(self):
        cache = IntelligentCache(max_size=10, default_ttl=0.01)
        cache.put("k1", "value")
        time.sleep(0.02)
        assert cache.get("k1") is None

    def test_lru_eviction(self):
        cache = IntelligentCache(max_size=2, default_ttl=60.0)
        cache.put("k1", "v1")
        cache.put("k2", "v2")
        cache.put("k3", "v3")
        assert cache.get("k1") is None
        assert cache.get("k2") == "v2"
        assert cache.get("k3") == "v3"

    def test_fingerprint(self):
        fp1 = IntelligentCache.fingerprint("  Hello World  ", approach="HYBRID")
        fp2 = IntelligentCache.fingerprint("hello world", approach="HYBRID")
        assert fp1 == fp2

    def test_stats(self):
        cache = IntelligentCache(max_size=10)
        cache.put("k1", "v1")
        cache.get("k1")
        cache.get("k1")
        cache.get("miss")
        stats = cache.stats()
        assert stats.hits == 2
        assert stats.misses == 1
        assert stats.hit_rate > 0.5

    def test_invalidate_pattern(self):
        cache = IntelligentCache()
        cache.put("report:a", "r1")
        cache.put("report:b", "r2")
        cache.put("query:c", "q1")
        removed = cache.invalidate_pattern("report:")
        assert removed == 2
        assert cache.get("query:c") == "q1"


# ---------------------------------------------------------------------------
# Plugin System
# ---------------------------------------------------------------------------
@pytest.mark.enterprise
class TestPluginRegistry:
    def test_register_and_list(self):
        reg = PluginRegistry()
        reg.register(PluginMetadata(
            name="neo4j-connector",
            version="1.0.0",
            author="EOIP",
            description="Neo4j graph backend plugin",
            capabilities=[PluginCapability.GRAPH_BACKEND],
        ))
        plugins = reg.list_all()
        assert len(plugins) == 1
        assert plugins[0]["name"] == "neo4j-connector"
        assert plugins[0]["status"] == "REGISTERED"

    def test_load_plugin(self):
        reg = PluginRegistry()
        reg.register(PluginMetadata(
            name="test-plugin",
            version="0.1.0",
            author="test",
            description="Test",
            capabilities=[PluginCapability.CUSTOM],
        ))
        assert reg.load("test-plugin") is True
        record = reg.get("test-plugin")
        assert record.status == PluginStatus.LOADED

    def test_find_by_capability(self):
        reg = PluginRegistry()
        reg.register(PluginMetadata(
            name="rag-ext", version="1.0.0", author="t", description="d",
            capabilities=[PluginCapability.RAG_STRATEGY],
        ))
        reg.load("rag-ext")
        found = reg.find_by_capability(PluginCapability.RAG_STRATEGY)
        assert len(found) == 1

    def test_dependency_check(self):
        reg = PluginRegistry()
        reg.register(PluginMetadata(
            name="child", version="1.0.0", author="t", description="d",
            capabilities=[PluginCapability.CUSTOM],
            dependencies=["parent"],
        ))
        assert reg.load("child") is False
        record = reg.get("child")
        assert record.status == PluginStatus.ERROR

    def test_stats(self):
        reg = PluginRegistry()
        reg.register(PluginMetadata(
            name="p1", version="1.0.0", author="t", description="d",
            capabilities=[PluginCapability.GRAPH_BACKEND, PluginCapability.CUSTOM],
        ))
        reg.load("p1")
        stats = reg.get_stats()
        assert stats["total_plugins"] == 1
        assert "GRAPH_BACKEND" in stats["capabilities_available"]
