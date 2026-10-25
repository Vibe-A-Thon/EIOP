"""Runtime per-layer tenant isolation (SR-TEN-003): every layer, cross-tenant access refused."""

from __future__ import annotations

import logging

import pytest

from eoip.authz.pdp import ScopeViolationError
from eoip.tenancy.isolation import REQUIRED_LAYERS, IsolationModel, IsolationPlacement, IsolationRegistry
from eoip.tenancy.layers import IsolationViolation, TenantLayers

pytestmark = pytest.mark.req("SR-TEN-003")


def placement(tenant, model, shared=False):
    tag = "pool" if shared else tenant
    return IsolationPlacement(model=model, tenant_id=tenant, layers={l: f"{l}-{tag}" for l in REQUIRED_LAYERS})


@pytest.fixture
def layers(tmp_path):
    reg = IsolationRegistry()
    reg.register(placement("acme", IsolationModel.SILO))
    reg.register(placement("bolt", IsolationModel.BRIDGE))
    reg.register(placement("cara", IsolationModel.POOL, shared=True))
    reg.register(placement("dyna", IsolationModel.POOL, shared=True))  # shares every placement value
    tl = TenantLayers(reg, root=tmp_path, master_key=b"m" * 32)
    return tl, {t: tl.for_tenant(t) for t in ("acme", "bolt", "cara", "dyna")}


PAIRS = [("acme", "bolt"), ("cara", "dyna")]  # dedicated vs dedicated, pool tenants sharing values


def test_graph_ids_are_tenant_namespaced_and_foreign_ids_rejected(layers):
    _, h = layers
    assert h["acme"].graph_id("svc-1") == "urn:eoip:acme:svc-1"
    with pytest.raises(ScopeViolationError):
        h["bolt"].graph_id("urn:eoip:acme:svc-1")


@pytest.mark.parametrize("a, b", PAIRS)
def test_vector_collections(layers, a, b):
    _, h = layers
    h[a].vector_upsert("d1", [1.0, 0.0])
    assert h[a].vector_search([1.0, 0.0]) == ["d1"]
    assert h[b].vector_search([1.0, 0.0]) == []
    with pytest.raises(IsolationViolation):
        h[b].vector_search([1.0, 0.0], collection=h[a]._p("vector_collection"))


@pytest.mark.parametrize("a, b", PAIRS)
def test_search_indexes(layers, a, b):
    _, h = layers
    h[a].search_index().add("e1", "payment outage in billing")
    assert [e for e, _ in h[a].search_index().keyword_search("billing")] == ["e1"]
    assert h[b].search_index().keyword_search("billing") == []


@pytest.mark.parametrize("a, b", PAIRS)
def test_relational_schema_and_no_attach(layers, a, b):
    _, h = layers
    h[a].sql("CREATE TABLE incidents (id TEXT)")
    h[a].sql("INSERT INTO incidents VALUES ('i1')")
    assert h[a].sql("SELECT id FROM incidents") == [("i1",)]
    with pytest.raises(Exception, match="no such table"):
        h[b].sql("SELECT id FROM incidents")
    with pytest.raises(IsolationViolation):
        h[b].sql("ATTACH DATABASE ':memory:' AS other")


@pytest.mark.parametrize("a, b", PAIRS)
def test_object_prefix(layers, a, b):
    _, h = layers
    h[a].put_object("reports/r1.json", b"{}")
    assert h[a].get_object("reports/r1.json") == b"{}"
    with pytest.raises(FileNotFoundError):
        h[b].get_object("reports/r1.json")
    with pytest.raises(IsolationViolation):
        h[b].get_object(f"../{h[a]._p('object_prefix')}/reports/r1.json")


@pytest.mark.parametrize("a, b", PAIRS)
def test_event_topics(layers, a, b):
    _, h = layers
    got_a, got_b = [], []
    h[a].subscribe(got_a.append)
    h[b].subscribe(got_b.append)
    h[a].publish({"type": "changed"})
    assert len(got_a) == 1 and got_b == []
    with pytest.raises(IsolationViolation):
        h[b].subscribe(got_b.append, topic=h[a]._p("event_topic"))
    with pytest.raises(IsolationViolation):
        h[b].publish({"type": "spoof"}, topic=h[a]._p("event_topic"))


@pytest.mark.parametrize("a, b", PAIRS)
def test_secrets(layers, a, b):
    _, h = layers
    h[a].put_secret("db-password", "s3cr3t-value")
    assert h[a].get_secret("db-password") == "s3cr3t-value"
    with pytest.raises(KeyError):
        h[b].get_secret("db-password")
    with pytest.raises(IsolationViolation):
        h[b].get_secret(f"../{h[a]._p('secrets_path')}/db-password")


@pytest.mark.parametrize("a, b", PAIRS)
def test_kms_keys(layers, a, b):
    _, h = layers
    blob = h[a].encrypt(b"payload")
    assert h[a].decrypt(blob) == b"payload"
    with pytest.raises(IsolationViolation):
        h[b].decrypt(blob)


@pytest.mark.parametrize("a, b", PAIRS)
def test_caches(layers, a, b):
    _, h = layers
    h[a].cache_set("q:1", "answer")
    assert h[a].cache_get("q:1") == "answer" and h[b].cache_get("q:1") is None
    h[b].cache_set("q:1", "other")
    assert h[b].cache_clear() == 1 and h[a].cache_get("q:1") == "answer"


@pytest.mark.parametrize("a, b", PAIRS)
def test_logs(layers, a, b):
    tl, h = layers
    logger = logging.getLogger(f"eoip.test.layers.{a}")
    logger.propagate = False
    logger.addHandler(tl.log_handler())
    logger.warning("tenant event", extra={"tenant_id": a})
    assert [r["message"] for r in h[a].read_logs()] == ["tenant event"]
    assert h[b].read_logs() == []
    with pytest.raises(IsolationViolation):
        h[b].read_logs(stream=h[a]._p("log_stream"))


@pytest.mark.parametrize("a, b", PAIRS)
def test_backups(layers, a, b):
    _, h = layers
    path = h[a].backup("nightly", {"vertices": 3})
    assert h[a].restore(path) == {"vertices": 3}
    with pytest.raises(IsolationViolation):
        h[b].restore(path)


@pytest.mark.parametrize("a, b", PAIRS)
def test_exports(layers, a, b):
    _, h = layers
    h[a].write_export("graph.ttl", b"@prefix x: <y> .")
    assert h[a].list_exports() == ["graph.ttl"] and h[b].list_exports() == []
    with pytest.raises(FileNotFoundError):
        h[b].read_export("graph.ttl")
    with pytest.raises(IsolationViolation):
        h[b].read_export("../graph.ttl")


def test_semantic_query_cache_is_namespaced_per_tenant():
    from eoip.query.cache import SemanticQueryCache

    class _Store:
        def count_vertices(self):
            return 3

        def count_edges(self):
            return 2

    cache, store = SemanticQueryCache(), _Store()
    plan = {"intent": "owners", "anchors": ["svc"], "tenant_id": "acme"}
    cache.put(plan, store, {"rows": ["acme-secret"]})
    assert cache.get(plan, store) == {"rows": ["acme-secret"]}
    assert cache.get({**plan, "tenant_id": "bolt"}, store) is None
    assert cache.get({k: v for k, v in plan.items() if k != "tenant_id"}, store) is None


def test_master_key_is_resolved_lazily_and_validated(tmp_path):
    from eoip.tenancy.layers import load_or_create_master_key

    reg = IsolationRegistry()
    reg.register(placement("acme", IsolationModel.SILO))
    calls = []
    key_file = tmp_path / "state" / "tenant-master.key"

    def source():
        calls.append(1)
        return load_or_create_master_key(key_file)

    tl = TenantLayers(reg, root=tmp_path / "t", master_key=source)
    assert calls == [] and not key_file.exists()  # app start-up writes nothing (restore needs empty data)
    h = tl.for_tenant("acme")
    assert h.decrypt(h.encrypt(b"x")) == b"x" and calls == [1] and key_file.stat().st_size == 32
    with pytest.raises(ValueError):
        TenantLayers(reg, root=tmp_path, master_key=lambda: b"short").for_tenant("acme").encrypt(b"x")
