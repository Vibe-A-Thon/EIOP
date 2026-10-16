"""Tests for enterprise lifecycle, feature flags, retry, and webhooks."""

from __future__ import annotations

import time
import pytest

from eoip.enterprise.lifecycle import (
    LifecycleManager,
    LifecycleComponent,
    LifecyclePhase,
)
from eoip.enterprise.feature_flags import (
    FeatureFlagRegistry,
    FlagDefinition,
)
from eoip.enterprise.retry import (
    RetryPolicy,
    RetryableOperation,
    RetryExhausted,
    retry_sync,
    compute_delay,
)
from eoip.enterprise.webhooks import (
    WebhookManager,
    WebhookEventType,
)


# ── Lifecycle Manager ─────────────────────────────────────────────────


class TestLifecycleManager:
    def test_phases_progress_correctly(self):
        mgr = LifecycleManager()
        assert mgr.phase == LifecyclePhase.INITIALIZING

        started = []
        stopped = []
        mgr.register(LifecycleComponent(
            name="db", priority=10,
            startup=lambda: started.append("db"),
            shutdown=lambda: stopped.append("db"),
        ))
        mgr.register(LifecycleComponent(
            name="cache", priority=20,
            startup=lambda: started.append("cache"),
            shutdown=lambda: stopped.append("cache"),
        ))

        mgr.start()
        assert mgr.phase == LifecyclePhase.RUNNING
        assert started == ["db", "cache"]

        report = mgr.shutdown()
        assert mgr.phase == LifecyclePhase.TERMINATED
        assert stopped == ["cache", "db"]
        assert report["drain_completed"] is True

    def test_request_tracking(self):
        mgr = LifecycleManager()
        mgr.start()
        assert mgr.request_enter() is True
        assert mgr.active_requests == 1
        mgr.request_exit()
        assert mgr.active_requests == 0

    def test_rejects_during_shutdown(self):
        mgr = LifecycleManager()
        mgr.start()
        mgr.shutdown()
        assert mgr.request_enter() is False

    def test_is_accepting(self):
        mgr = LifecycleManager()
        assert mgr.is_accepting is False
        mgr.start()
        assert mgr.is_accepting is True

    def test_stats(self):
        mgr = LifecycleManager()
        mgr.register(LifecycleComponent(name="svc"))
        s = mgr.stats()
        assert s["phase"] == "INITIALIZING"
        assert s["components"] == 1

    def test_phase_callbacks(self):
        mgr = LifecycleManager()
        phases_seen = []
        mgr.on_phase(LifecyclePhase.RUNNING, lambda: phases_seen.append("RUNNING"))
        mgr.on_phase(LifecyclePhase.TERMINATED, lambda: phases_seen.append("TERMINATED"))
        mgr.start()
        mgr.shutdown()
        assert "RUNNING" in phases_seen
        assert "TERMINATED" in phases_seen


# ── Feature Flags ─────────────────────────────────────────────────────


class TestFeatureFlags:
    def test_define_and_evaluate(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(name="dark_mode", description="UI dark mode", default_enabled=True))
        result = reg.is_enabled("dark_mode")
        assert result.enabled is True
        assert result.reason == "DEFAULT"

    def test_undefined_flag(self):
        reg = FeatureFlagRegistry()
        result = reg.is_enabled("nonexistent")
        assert result.enabled is False
        assert result.reason == "FLAG_NOT_DEFINED"

    def test_tenant_override(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(name="beta_ui", description="Beta UI", default_enabled=False))
        reg.set_override("beta_ui", "tenant_123", True)
        result = reg.is_enabled("beta_ui", tenant_id="tenant_123")
        assert result.enabled is True
        assert result.reason == "TENANT_OVERRIDE"

    def test_blocked_tenant(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(
            name="feature_x", description="X", default_enabled=True,
            blocked_tenants={"banned_tenant"},
        ))
        result = reg.is_enabled("feature_x", tenant_id="banned_tenant")
        assert result.enabled is False
        assert result.reason == "TENANT_BLOCKED"

    def test_rollout_percentage(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(
            name="gradual_rollout", description="50% rollout",
            default_enabled=True, rollout_percentage=50.0,
        ))
        results = [reg.is_enabled("gradual_rollout", tenant_id=f"t{i}") for i in range(100)]
        enabled_count = sum(1 for r in results if r.enabled)
        assert 20 < enabled_count < 80

    def test_clear_override(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(name="f1", description="", default_enabled=False))
        reg.set_override("f1", "t1", True)
        reg.clear_override("f1", "t1")
        result = reg.is_enabled("f1", tenant_id="t1")
        assert result.enabled is False

    def test_list_and_stats(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(name="a", description="Alpha", default_enabled=True))
        reg.define(FlagDefinition(name="b", description="Beta", default_enabled=False))
        flags = reg.list_flags()
        assert len(flags) == 2
        stats = reg.stats()
        assert stats["total_flags"] == 2
        assert stats["enabled_by_default"] == 1

    def test_allowed_tenants(self):
        reg = FeatureFlagRegistry()
        reg.define(FlagDefinition(
            name="exclusive", description="", default_enabled=True,
            allowed_tenants={"vip_tenant"},
        ))
        result = reg.is_enabled("exclusive", tenant_id="other")
        assert result.enabled is False
        assert result.reason == "TENANT_NOT_ALLOWED"
        result = reg.is_enabled("exclusive", tenant_id="vip_tenant")
        assert result.enabled is True


# ── Retry ─────────────────────────────────────────────────────────────


class TestRetry:
    def test_succeeds_first_try(self):
        result, outcome = retry_sync(lambda: 42)
        assert result == 42
        assert outcome.success is True
        assert outcome.attempts == 1

    def test_retries_on_failure(self):
        call_count = 0

        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "ok"

        policy = RetryPolicy(max_attempts=5, base_delay=0.01, jitter=False)
        result, outcome = retry_sync(flaky, policy=policy)
        assert result == "ok"
        assert outcome.attempts == 3

    def test_exhausted_raises(self):
        policy = RetryPolicy(max_attempts=2, base_delay=0.01, jitter=False)
        with pytest.raises(RetryExhausted) as exc_info:
            retry_sync(lambda: 1 / 0, policy=policy)
        assert exc_info.value.outcome.attempts == 2
        assert exc_info.value.outcome.success is False

    def test_retryable_exceptions_filter(self):
        policy = RetryPolicy(
            max_attempts=3, base_delay=0.01, jitter=False,
            retryable_exceptions=(ValueError,),
        )
        with pytest.raises(ZeroDivisionError):
            retry_sync(lambda: 1 / 0, policy=policy)

    def test_compute_delay_with_cap(self):
        policy = RetryPolicy(base_delay=1.0, max_delay=5.0, exponential_base=2.0, jitter=False)
        assert compute_delay(0, policy) == 1.0
        assert compute_delay(1, policy) == 2.0
        assert compute_delay(2, policy) == 4.0
        assert compute_delay(3, policy) == 5.0

    def test_retryable_operation_stats(self):
        counter = {"n": 0}

        def sometimes_fail():
            counter["n"] += 1
            if counter["n"] % 2 == 1:
                raise ValueError("odd")
            return counter["n"]

        op = RetryableOperation(sometimes_fail, RetryPolicy(max_attempts=3, base_delay=0.01, jitter=False))
        result = op.execute()
        assert result == 2
        stats = op.stats()
        assert stats["total_calls"] == 1
        assert stats["total_retries"] == 1


# ── Webhooks ──────────────────────────────────────────────────────────


class TestWebhookManager:
    def test_subscribe_and_list(self):
        mgr = WebhookManager()
        sub = mgr.subscribe(
            url="https://example.com/hook",
            events=[WebhookEventType.GRAPH_MUTATION],
        )
        assert sub.subscription_id
        subs = mgr.list_subscriptions()
        assert len(subs) == 1
        assert subs[0]["url"] == "https://example.com/hook"

    def test_unsubscribe(self):
        mgr = WebhookManager()
        sub = mgr.subscribe(url="https://example.com/hook", events=[WebhookEventType.GRAPH_MUTATION])
        assert mgr.unsubscribe(sub.subscription_id) is True
        assert mgr.unsubscribe("nonexistent") is False
        assert len(mgr.list_subscriptions()) == 0

    def test_dispatch_delivers(self):
        delivered = []

        def mock_deliver(url, headers, body):
            delivered.append({"url": url, "body": body})
            return 200

        mgr = WebhookManager(delivery_fn=mock_deliver)
        mgr.subscribe(url="https://example.com/hook", events=[WebhookEventType.ENTITY_CREATED])
        count = mgr.dispatch(WebhookEventType.ENTITY_CREATED, {"entity_id": "E1"})
        assert count == 1
        assert len(delivered) == 1

    def test_dispatch_skips_non_matching(self):
        mgr = WebhookManager()
        mgr.subscribe(url="https://example.com/hook", events=[WebhookEventType.GRAPH_MUTATION])
        count = mgr.dispatch(WebhookEventType.HEALTH_DEGRADED, {"node": "N1"})
        assert count == 0

    def test_failed_delivery_goes_to_dead_letter(self):
        def fail_deliver(url, headers, body):
            raise ConnectionError("refused")

        mgr = WebhookManager(delivery_fn=fail_deliver)
        mgr.subscribe(
            url="https://example.com/hook",
            events=[WebhookEventType.AUDIT_ALERT],
            max_retries=1,
        )
        count = mgr.dispatch(WebhookEventType.AUDIT_ALERT, {"alert": "test"})
        assert count == 0
        dead = mgr.get_dead_letters()
        assert len(dead) == 1

    def test_hmac_signature(self):
        captured_headers: dict[str, str] = {}

        def capture_deliver(url, headers, body):
            captured_headers.update(headers)
            return 200

        mgr = WebhookManager(delivery_fn=capture_deliver)
        mgr.subscribe(
            url="https://example.com/hook",
            events=[WebhookEventType.SCHEMA_CHANGED],
            secret="my-secret",
        )
        mgr.dispatch(WebhookEventType.SCHEMA_CHANGED, {"schema": "v2"})
        assert "X-Webhook-Signature" in captured_headers
        assert captured_headers["X-Webhook-Signature"].startswith("sha256=")

    def test_stats(self):
        mgr = WebhookManager()
        mgr.subscribe(url="https://example.com/hook", events=[WebhookEventType.GRAPH_MUTATION])
        mgr.dispatch(WebhookEventType.GRAPH_MUTATION, {"action": "create"})
        stats = mgr.stats()
        assert stats["subscriptions"] == 1
        assert stats["total_dispatched"] == 1
        assert stats["total_delivered"] == 1

    def test_multiple_subscribers(self):
        delivered = []
        mgr = WebhookManager(delivery_fn=lambda u, h, b: (delivered.append(u), 200)[1])
        mgr.subscribe(url="https://a.com/hook", events=[WebhookEventType.GRAPH_QUERY])
        mgr.subscribe(url="https://b.com/hook", events=[WebhookEventType.GRAPH_QUERY])
        count = mgr.dispatch(WebhookEventType.GRAPH_QUERY, {"query": "test"})
        assert count == 2
        assert len(delivered) == 2
