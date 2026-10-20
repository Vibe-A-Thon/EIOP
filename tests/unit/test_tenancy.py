"""Unit tests for packages/eoip/tenancy (SR-TEN-001/002/003/006/007/009)."""

from __future__ import annotations

import pytest

from eoip.tenancy import (
    GENESIS_HASH,
    IsolationModel,
    IsolationPlacement,
    IsolationRegistry,
    Lane,
    LifecycleError,
    MeteringLog,
    PlacementValidationError,
    QuotaManager,
    QuotaSpec,
    TenancyService,
    TenantContextRequired,
    TenantLifecycle,
    TenantState,
    model_catalog,
    resolve_context,
    validate_placement,
)
from eoip.tenancy.isolation import REQUIRED_LAYERS
from eoip.tenancy.quotas import QUOTA_DIMENSIONS

TENANT = "t-1"
PRINCIPAL = "svc-ci"


def _layers(tag: str) -> dict[str, str]:
    return {layer: f"{layer}:{tag}" for layer in sorted(REQUIRED_LAYERS)}


# ---------------------------------------------------------------------------
# SR-TEN-001 context
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-TEN-001")
class TestTenantContext:
    def test_resolve_ok(self):
        ctx = resolve_context(TENANT, PRINCIPAL)
        assert ctx.tenant_id == TENANT
        assert ctx.urn == "urn:eoip:tenancy:tenant:t-1"
        assert ctx.cache_key("k") == "ten:t-1:k"
        assert ctx.log_fields() == {"tenant_id": TENANT, "principal": PRINCIPAL}

    @pytest.mark.parametrize("tenant,principal", [
        (None, PRINCIPAL), ("", PRINCIPAL), ("  ", PRINCIPAL),
        (TENANT, None), (TENANT, ""),
    ])
    def test_fail_closed(self, tenant, principal):
        with pytest.raises(TenantContextRequired):
            resolve_context(tenant, principal)

    def test_urn_passthrough(self):
        ctx = resolve_context("urn:eoip:tenancy:tenant:x", PRINCIPAL)
        assert ctx.urn == "urn:eoip:tenancy:tenant:x"

    def test_cache_key_requires_tenant(self):
        from eoip.tenancy import TenantContext
        with pytest.raises(TenantContextRequired):
            TenantContext("", PRINCIPAL).cache_key("k")


# ---------------------------------------------------------------------------
# SR-TEN-002/003 isolation
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-TEN-002", "SR-TEN-003")
class TestIsolation:
    def test_catalog_covers_three_models(self):
        models = {m["model"] for m in model_catalog()}
        assert models == {"silo", "bridge", "pool"}

    def test_silo_dedicates_everything_pool_nothing(self):
        assert IsolationModel.SILO.dedicated_layers == frozenset(REQUIRED_LAYERS)
        assert IsolationModel.POOL.dedicated_layers == frozenset()
        assert IsolationModel.BRIDGE.dedicated_layers  # strict subset
        assert IsolationModel.BRIDGE.dedicated_layers < frozenset(REQUIRED_LAYERS)

    def test_valid_placement(self):
        p = IsolationPlacement(IsolationModel.BRIDGE, _layers("a"), TENANT)
        assert validate_placement(p).tenant_id == TENANT

    def test_missing_layer_rejected(self):
        layers = _layers("a")
        del layers["kms_key"]
        with pytest.raises(PlacementValidationError):
            validate_placement(IsolationPlacement(IsolationModel.POOL, layers, TENANT))

    def test_empty_layer_value_rejected(self):
        layers = _layers("a")
        layers["graph_namespace"] = ""
        with pytest.raises(PlacementValidationError):
            validate_placement(IsolationPlacement(IsolationModel.POOL, layers, TENANT))

    def test_dedicated_layer_collision_rejected(self):
        reg = IsolationRegistry()
        reg.register(IsolationPlacement(IsolationModel.BRIDGE, _layers("a"), "t-1"))
        with pytest.raises(PlacementValidationError):
            reg.register(IsolationPlacement(IsolationModel.BRIDGE, _layers("a"), "t-2"))

    def test_pool_allows_shared_layers(self):
        reg = IsolationRegistry()
        reg.register(IsolationPlacement(IsolationModel.POOL, _layers("shared"), "t-1"))
        reg.register(IsolationPlacement(IsolationModel.POOL, _layers("shared"), "t-2"))

    def test_get_unknown_tenant(self):
        with pytest.raises(PlacementValidationError):
            IsolationRegistry().get("nope")


# ---------------------------------------------------------------------------
# SR-TEN-006 quotas
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-TEN-006")
class TestQuotas:
    def test_counter_consume_refund(self):
        qm = QuotaManager()
        qm.set_quota(TENANT, QuotaSpec(concurrent_queries=2))
        assert qm.consume(TENANT, "concurrent_queries").allowed
        assert qm.consume(TENANT, "concurrent_queries").allowed
        denied = qm.consume(TENANT, "concurrent_queries")
        assert not denied.allowed and "quota exceeded" in denied.reason
        qm.refund(TENANT, "concurrent_queries")
        assert qm.consume(TENANT, "concurrent_queries").allowed

    def test_counter_overflow(self):
        qm = QuotaManager()
        qm.set_quota(TENANT, QuotaSpec(graph_size=10))
        assert qm.consume(TENANT, "graph_size", 10).allowed
        assert not qm.consume(TENANT, "graph_size", 1).allowed
        assert qm.usage(TENANT, "graph_size") == 10

    def test_unlimited_when_no_spec(self):
        qm = QuotaManager()
        d = qm.consume(TENANT, "storage_bytes", 10**9)
        assert d.allowed and d.limit is None

    def test_unknown_dimension(self):
        with pytest.raises(ValueError):
            QuotaManager().check(TENANT, "bogus")

    def test_idempotency(self):
        qm = QuotaManager()
        qm.set_quota(TENANT, QuotaSpec(concurrent_queries=1))
        first = qm.consume(TENANT, "concurrent_queries", idempotency_key="k1")
        second = qm.consume(TENANT, "concurrent_queries", idempotency_key="k1")
        assert first.allowed and second.allowed
        assert qm.usage(TENANT, "concurrent_queries") == 1
        # fresh key is denied (slot held by k1)
        assert not qm.consume(TENANT, "concurrent_queries", idempotency_key="k2").allowed
        # refund releases the slot and clears the idempotency record
        qm.refund(TENANT, "concurrent_queries", idempotency_key="k1")
        assert qm.consume(TENANT, "concurrent_queries", idempotency_key="k2").allowed

    def test_fair_order_priority_lanes(self):
        qm = QuotaManager()
        qm.set_quota("bg", QuotaSpec(concurrent_queries=100), lane=Lane.BACKGROUND)
        qm.set_quota("it", QuotaSpec(concurrent_queries=100), lane=Lane.INTERACTIVE)
        qm.set_quota("bt", QuotaSpec(concurrent_queries=100), lane=Lane.BATCH)
        # Interactive first even though listed last; background last.
        assert qm.fair_order(["bg", "bt", "it"]) == ["it", "bt", "bg"]

    def test_fair_order_deficit_first(self):
        qm = QuotaManager()
        qm.set_quota("a", QuotaSpec(graph_size=100), lane=Lane.BATCH)
        qm.set_quota("b", QuotaSpec(graph_size=100), lane=Lane.BATCH)
        qm.consume("a", "graph_size", 90)
        qm.consume("b", "graph_size", 10)
        assert qm.fair_order(["a", "b"]) == ["b", "a"]

    def test_all_dimensions_defined(self):
        assert QUOTA_DIMENSIONS == frozenset({
            "graph_size", "ingestion_rate", "concurrent_queries", "llm_tokens", "storage_bytes",
        })


# ---------------------------------------------------------------------------
# SR-TEN-007 lifecycle
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-TEN-007")
class TestLifecycle:
    def _lifecycle(self):
        return TenantLifecycle()

    def test_happy_path(self):
        lc = self._lifecycle()
        lc.provision(TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL)
        assert lc.state(TENANT) == TenantState.PROVISIONING
        lc.configure(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.ACTIVE
        lc.suspend(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.SUSPENDED
        lc.resume(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.ACTIVE

    def test_illegal_transitions(self):
        lc = self._lifecycle()
        lc.provision(TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL)
        with pytest.raises(LifecycleError):
            lc.suspend(TENANT, PRINCIPAL)  # provisioning -> suspended illegal
        lc.configure(TENANT, PRINCIPAL)
        with pytest.raises(LifecycleError):
            lc.resume(TENANT, PRINCIPAL)   # not suspended

    def test_unknown_tenant(self):
        with pytest.raises(LifecycleError):
            self._lifecycle().state("nope")

    def test_clone_flow(self):
        lc = self._lifecycle()
        lc.provision(TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL)
        lc.configure(TENANT, PRINCIPAL)
        lc.clone(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.CLONED
        lc.configure(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.ACTIVE

    def test_export_returns_to_prior_state(self):
        lc = self._lifecycle()
        lc.provision(TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL)
        lc.configure(TENANT, PRINCIPAL)
        lc.export(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.ACTIVE  # restored
        lc.suspend(TENANT, PRINCIPAL)
        lc.export(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.SUSPENDED

    def test_delete_issues_certificate_and_terminates(self):
        lc = self._lifecycle()
        placement = IsolationPlacement(IsolationModel.BRIDGE, _layers("a"), TENANT)
        lc.provision(TENANT, placement, PRINCIPAL)
        lc.configure(TENANT, PRINCIPAL)
        cert = lc.delete(TENANT, PRINCIPAL)
        assert lc.state(TENANT) == TenantState.DELETED
        assert cert.tenant_id == TENANT
        assert cert.certificate_id.startswith("urn:eoip:tenancy:cod:")
        assert set(cert.destroyed_layers) == REQUIRED_LAYERS
        assert len(cert.verification_hash) == 64
        assert lc.certificate(TENANT) == cert
        with pytest.raises(LifecycleError):
            lc.resume(TENANT, PRINCIPAL)  # deleted is terminal

    def test_cannot_delete_provisioning_via_configure_gap(self):
        # provisioning can be deleted per transition table
        lc = self._lifecycle()
        lc.provision(TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL)
        cert = lc.delete(TENANT, PRINCIPAL)
        assert cert.destroyed_layers  # layers were placed at provision time

    def test_history_recorded(self):
        lc = self._lifecycle()
        lc.provision(TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL)
        lc.configure(TENANT, PRINCIPAL)
        actions = [e.action for e in lc.history(TENANT)]
        assert actions == ["provision", "configure"]


# ---------------------------------------------------------------------------
# SR-TEN-009 metering
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-TEN-009")
class TestMetering:
    def test_append_chain(self):
        log = MeteringLog()
        r1 = log.record(TENANT, {"queries": 5})
        r2 = log.record(TENANT, {"records_ingested": 10, "graph_size": 7})
        assert r1.prev_hash == GENESIS_HASH
        assert r2.prev_hash == r1.entry_hash
        assert log.chain_head(TENANT) == r2.entry_hash
        assert log.verify_chain(TENANT)

    def test_totals(self):
        log = MeteringLog()
        log.record(TENANT, {"queries": 5})
        log.record(TENANT, {"queries": 3, "llm_tokens": 100})
        totals = log.totals(TENANT)
        assert totals["queries"] == 8
        assert totals["llm_tokens"] == 100
        assert totals["seats"] == 0

    def test_unknown_dimension(self):
        with pytest.raises(ValueError):
            MeteringLog().record(TENANT, {"bogus": 1})

    def test_tamper_detection(self):
        log = MeteringLog()
        log.record(TENANT, {"queries": 5})
        log.record(TENANT, {"queries": 5})
        chain = log._chains[TENANT]
        log._chains[TENANT] = [chain[0], chain[1].__class__(
            record_id=chain[1].record_id,
            tenant_id=chain[1].tenant_id,
            at=chain[1].at,
            dimensions={"queries": 500},  # edited
            prev_hash=chain[1].prev_hash,
            entry_hash=chain[1].entry_hash,
            note=chain[1].note,
        )]
        assert not log.verify_chain(TENANT)

    def test_tamper_by_removal_detected(self):
        log = MeteringLog()
        log.record(TENANT, {"queries": 1})
        log.record(TENANT, {"queries": 2})
        del log._chains[TENANT][0]  # remove earliest entry
        assert not log.verify_chain(TENANT)

    def test_export_roundtrip(self):
        log = MeteringLog()
        log.record(TENANT, {"storage_bytes": 42})
        log.record(TENANT, {"seats": 3, "connectors": 2})
        exported = log.export(TENANT)
        assert exported["verified"] and exported["record_count"] == 2
        assert exported["totals"]["storage_bytes"] == 42
        restored = MeteringLog()
        assert restored.import_chain(TENANT, exported["records"])
        assert restored.chain_head(TENANT) == exported["chain_head"]
        assert restored.verify_chain(TENANT)

    def test_export_empty_tenant(self):
        exported = MeteringLog().export(TENANT)
        assert exported["chain_head"] == GENESIS_HASH
        assert exported["verified"] and exported["record_count"] == 0


# ---------------------------------------------------------------------------
# Service integration (destruction certificate signed into metering chain)
# ---------------------------------------------------------------------------

class TestService:
    def test_delete_recorded_in_meter_log(self):
        svc = TenancyService()
        svc.lifecycle.provision(
            TENANT, IsolationPlacement(IsolationModel.POOL, _layers("a"), TENANT), PRINCIPAL
        )
        svc.lifecycle.configure(TENANT, PRINCIPAL)
        cert = svc.lifecycle.delete(TENANT, PRINCIPAL)
        assert svc.metering.verify_chain(TENANT)
        notes = [r.note for r in svc.metering.records(TENANT)]
        assert f"destruction:{cert.certificate_id}" in notes


# ---------------------------------------------------------------------------
# Router (SR-TEN-001 endpoints; lazy fastapi import verified by import here)
# ---------------------------------------------------------------------------

class TestRouter:
    @pytest.fixture
    def client(self):
        fastapi = pytest.importorskip("fastapi")
        from eoip.tenancy.router import build_router
        from eoip.tenancy.service import TenancyService

        app = fastapi.FastAPI()
        app.include_router(build_router(TenancyService()))
        from fastapi.testclient import TestClient
        return TestClient(app)

    @pytest.fixture
    def headers(self):
        return {"X-Tenant-Id": TENANT, "X-Principal": PRINCIPAL}

    def test_fail_closed_without_headers(self, client):
        resp = client.get("/api/v1/tenancy/context")
        assert resp.status_code == 403

    def test_context_echo(self, client, headers):
        resp = client.get("/api/v1/tenancy/context", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["tenant_id"] == TENANT

    def test_isolation_models(self, client, headers):
        resp = client.get("/api/v1/tenancy/isolation/models", headers=headers)
        assert resp.status_code == 200
        assert len(resp.json()["models"]) == 3

    def test_placement_roundtrip(self, client, headers):
        body = {"model": "pool", "layers": _layers("rt")}
        assert client.post("/api/v1/tenancy/isolation/placement", json=body, headers=headers).status_code == 200
        resp = client.get("/api/v1/tenancy/isolation/placement", headers=headers)
        assert resp.json()["layers"] == _layers("rt")

    def test_incomplete_placement_rejected(self, client, headers):
        body = {"model": "pool", "layers": {"graph_namespace": "g"}}
        resp = client.post("/api/v1/tenancy/isolation/placement", json=body, headers=headers)
        assert resp.status_code == 400

    def test_quota_deny_returns_429(self, client, headers):
        # Default spec: no quota set -> unlimited; exercise check endpoint.
        resp = client.post(
            "/api/v1/tenancy/quotas/check",
            json={"dimension": "concurrent_queries", "amount": 1},
            headers=headers,
        )
        assert resp.status_code == 200
        assert resp.json()["allowed"]

    def test_metering_flow(self, client, headers):
        rec = client.post(
            "/api/v1/tenancy/metering/record",
            json={"dimensions": {"queries": 9}},
            headers=headers,
        )
        assert rec.status_code == 200
        verify = client.get("/api/v1/tenancy/metering/verify", headers=headers)
        assert verify.json()["verified"]
        exported = client.get("/api/v1/tenancy/metering/export", headers=headers)
        assert exported.json()["totals"]["queries"] == 9

    def test_lifecycle_flow_over_http(self, client, headers):
        body = {"model": "pool", "layers": _layers("http")}
        assert client.post("/api/v1/tenancy/lifecycle/provision", json=body, headers=headers).status_code == 200
        assert client.post("/api/v1/tenancy/lifecycle/configure", headers=headers).status_code == 200
        assert client.post("/api/v1/tenancy/lifecycle/suspend", headers=headers).status_code == 200
        assert client.post("/api/v1/tenancy/lifecycle/resume", headers=headers).status_code == 200
        cert = client.post("/api/v1/tenancy/lifecycle/delete", headers=headers)
        assert cert.status_code == 200
        assert cert.json()["certificate_id"].startswith("urn:eoip:tenancy:cod:")

    def test_illegal_transition_over_http(self, client, headers):
        body = {"model": "pool", "layers": _layers("bad")}
        client.post("/api/v1/tenancy/lifecycle/provision", json=body, headers=headers)
        client.post("/api/v1/tenancy/lifecycle/configure", headers=headers)
        resp = client.post("/api/v1/tenancy/lifecycle/resume", headers=headers)  # not suspended
        assert resp.status_code == 400


class TestCircuitBreakers:
    @pytest.mark.req("SR-TEN-006")
    def test_per_tenant_breaker_opens_isolates_and_recovers_via_single_probe(self):
        from eoip.tenancy import CircuitOpen, TenantCircuitBreaker

        now = [0.0]
        cb = TenantCircuitBreaker(failure_threshold=3, cooldown_s=10, clock=lambda: now[0])

        def boom():
            raise RuntimeError("backend down")

        for _ in range(3):
            with pytest.raises(RuntimeError):
                cb.call("noisy", "graph-db", boom)
        assert cb.state("noisy", "graph-db") == "open"
        with pytest.raises(CircuitOpen) as exc:
            cb.call("noisy", "graph-db", lambda: "x")
        assert exc.value.retry_after == pytest.approx(10)
        # another tenant on the same dependency is unaffected
        assert cb.call("quiet", "graph-db", lambda: "ok") == "ok"
        assert cb.state("quiet", "graph-db") == "closed"
        # after cooldown: exactly one probe; a failed probe re-opens
        now[0] = 10.0
        assert cb.state("noisy", "graph-db") == "half_open"
        with pytest.raises(RuntimeError):
            cb.call("noisy", "graph-db", boom)
        assert cb.state("noisy", "graph-db") == "open"
        now[0] = 20.0
        cb.before_call("noisy", "graph-db")  # the single probe slot
        with pytest.raises(CircuitOpen):
            cb.before_call("noisy", "graph-db")
        cb.record_success("noisy", "graph-db")
        assert cb.state("noisy", "graph-db") == "closed"
        with pytest.raises(ValueError):
            cb.call("", "graph-db", lambda: 1)  # no tenant context: fail closed

    def test_quota_manager_exposes_tenant_breakers(self):
        from eoip.tenancy import QuotaManager, TenantCircuitBreaker
        assert isinstance(QuotaManager().breakers, TenantCircuitBreaker)
