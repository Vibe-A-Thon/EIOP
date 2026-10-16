"""Optional integration modules behave without their extras installed.

G2-SRC-OTEL-LIB, G2-SRC-K8S, G2-SCALE-CACHE: each module must import cleanly
and degrade gracefully when opentelemetry / kubernetes / redis are absent, and
must exercise its real code paths against monkeypatched fake modules.
"""

from __future__ import annotations

import importlib.util
import sys
import types

import pytest
from eoip.connectors.base import DiscoveryScope
from eoip.graph.memory import MemoryGraphStore
from eoip.query.cache import SemanticQueryCache

HAS_OTEL = importlib.util.find_spec("opentelemetry") is not None
HAS_K8S = importlib.util.find_spec("kubernetes") is not None
HAS_REDIS_PKG = importlib.util.find_spec("redis") is not None


def _store():
    store = MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem", {"canonical_id": "w:1", "issue_key": "EOIP-1", "summary": "One"}
    )
    return store


def _plan():
    return {
        "intent": "SEARCH",
        "anchors": ["EOIP-1"],
        "max_depth": 1,
        "result_limit": 25,
        "evidence_mode": "NONE",
    }


# ---------------------------------------------------------------------------
# G2-SRC-OTEL-LIB
# ---------------------------------------------------------------------------


def test_otel_setup_noop_without_package(monkeypatch, caplog):
    pytest.importorskip("fastapi")  # only needed for the instrumented path
    if HAS_OTEL:
        # Force the ImportError path regardless of the environment.
        for name in list(sys.modules):
            if name.startswith("opentelemetry"):
                monkeypatch.delitem(sys.modules, name)
        monkeypatch.setitem(sys.modules, "opentelemetry", None)
    from eoip.observability import otel

    monkeypatch.setattr(otel, "_warned", False)
    warnings_seen: list[str] = []
    monkeypatch.setattr(
        otel.logger, "warning", lambda message, *a, **k: warnings_seen.append(message)
    )
    assert otel.setup_tracing(object(), "eoip-test") is False
    assert any("OpenTelemetry not installed" in message for message in warnings_seen)
    # Documented no-op: tracer factory still returns something usable.
    assert otel.get_tracer("x") is not None


def _fake_otel_modules(monkeypatch):
    def module(name, **attrs):
        mod = types.ModuleType(name)
        for key, value in attrs.items():
            setattr(mod, key, value)
        monkeypatch.setitem(sys.modules, name, mod)
        return mod

    recorded = {"provider": None, "instrumented": [], "middleware": [], "exporter_endpoint": None}

    class FakeTracerProvider:
        def __init__(self):
            self.processors = []
            recorded["provider"] = self

        def add_span_processor(self, processor):
            self.processors.append(processor)

    class FakeBatchSpanProcessor:
        def __init__(self, exporter):
            self.exporter = exporter

    class FakeOTLPSpanExporter:
        def __init__(self, endpoint=None):
            recorded["exporter_endpoint"] = endpoint

    class FakeFastAPIInstrumentor:
        @staticmethod
        def instrument_app(app):
            recorded["instrumented"].append(app)

    class FakeSpan:
        def is_recording(self):
            return True

        def set_attribute(self, key, value):
            recorded.setdefault("attributes", []).append((key, value))

    fake_trace = module(
        "opentelemetry.trace",
        set_tracer_provider=lambda provider: recorded.setdefault("provider_set", provider),
        get_tracer_provider=lambda: recorded["provider"],
        get_current_span=lambda: FakeSpan(),
        get_tracer=lambda name: ("tracer", name),
    )
    module("opentelemetry", trace=fake_trace)
    sdk_trace = module("opentelemetry.sdk.trace", TracerProvider=FakeTracerProvider)
    module("opentelemetry.sdk", trace=sdk_trace)
    module(
        "opentelemetry.sdk.trace.export",
        BatchSpanProcessor=FakeBatchSpanProcessor,
        SimpleSpanProcessor=FakeBatchSpanProcessor,
    )
    module(
        "opentelemetry.exporter.otlp.proto.http.trace_exporter",
        OTLPSpanExporter=FakeOTLPSpanExporter,
    )
    module(
        "opentelemetry.instrumentation.fastapi",
        FastAPIInstrumentor=FakeFastAPIInstrumentor,
    )
    return recorded


class _FakeApp:
    def __init__(self):
        self.middlewares = []

    def middleware(self, kind):
        def register(fn):
            self.middlewares.append((kind, fn))
            return fn

        return register


def test_otel_setup_with_fake_sdk(monkeypatch):
    from eoip.observability import otel

    recorded = _fake_otel_modules(monkeypatch)
    app = _FakeApp()
    monkeypatch.setenv("EOIP_OTEL_ENDPOINT", "http://collector:4318/v1/traces")
    assert otel.setup_tracing(app, "eoip-test") is True
    assert recorded["instrumented"] == [app]
    assert recorded["exporter_endpoint"] == "http://collector:4318/v1/traces"
    assert len(recorded["provider"].processors) == 1
    # Correlation-id enrichment middleware is registered.
    assert len(app.middlewares) == 1

    # The middleware copies X-Correlation-ID onto the active span.
    import asyncio

    kind, middleware = app.middlewares[0]
    assert kind == "http"

    class _Req:
        headers = types.MappingProxyType({"x-correlation-id": "corr-123"})

    async def _run():
        return await middleware(_Req(), lambda r: asyncio.sleep(0, result="ok"))

    assert asyncio.run(_run()) == "ok"
    assert ("eoip.correlation_id", "corr-123") in recorded["attributes"]


# ---------------------------------------------------------------------------
# G2-SRC-K8S
# ---------------------------------------------------------------------------


def _obj(name, namespace=None, uid=None, **extra):
    return types.SimpleNamespace(
        metadata=types.SimpleNamespace(name=name, namespace=namespace, uid=uid),
        **extra,
    )


class _FakeCoreV1:
    def __init__(self):
        self.pods = [_obj("pod-a", "ns1", "u1", status=types.SimpleNamespace(phase="Running"))]
        self.services = [_obj("svc-a", "ns1", "u2")]
        self.namespaces = [_obj("ns1", uid="u3")]

    def list_namespace(self):
        return types.SimpleNamespace(items=self.namespaces)

    def list_namespaced_pod(self, namespace):
        return types.SimpleNamespace(items=[p for p in self.pods if p.metadata.namespace == namespace])

    def list_namespaced_service(self, namespace):
        return types.SimpleNamespace(items=[s for s in self.services if s.metadata.namespace == namespace])

    def read_namespaced_pod(self, name, namespace):
        return self.list_namespaced_pod(namespace).items[0]

    def read_namespaced_service(self, name, namespace):
        return self.list_namespaced_service(namespace).items[0]

    def read_namespace(self, name):
        return self.namespaces[0]


class _FakeAppsV1:
    def __init__(self):
        self.deployments = [_obj("dep-a", "ns1", "u4", spec=types.SimpleNamespace(replicas=2))]

    def list_namespaced_deployment(self, namespace):
        return types.SimpleNamespace(
            items=[d for d in self.deployments if d.metadata.namespace == namespace]
        )

    def read_namespaced_deployment(self, name, namespace):
        return self.list_namespaced_deployment(namespace).items[0]


@pytest.mark.skipif(HAS_K8S, reason="forces absence of kubernetes")
def test_kubernetes_missing_package_error():
    from eoip.connectors.kubernetes import (
        KubernetesConnector,
        KubernetesDependencyMissingError,
        _load_kubernetes,
    )

    with pytest.raises(KubernetesDependencyMissingError, match="eoip\\[k8s\\]"):
        _load_kubernetes()
    connector = KubernetesConnector()
    with pytest.raises(KubernetesDependencyMissingError):
        connector._core()


def test_kubernetes_connector_protocol_with_fake_client():
    from eoip.connectors.kubernetes import KubernetesConnector

    core = _FakeCoreV1()
    apps = _FakeAppsV1()
    client = types.SimpleNamespace(
        **{name: getattr(core, name) for name in dir(core) if not name.startswith("_")}
    )
    client.list_namespaced_deployment = apps.list_namespaced_deployment
    client.read_namespaced_deployment = apps.read_namespaced_deployment
    connector = KubernetesConnector(source_id="k8s-test", client=client)

    caps = connector.capabilities()
    assert caps.baseline and caps.polling and caps.discovery

    result = connector.discover(DiscoveryScope())
    types_found = {r.resource_type for r in result.resources}
    assert {"namespace", "pod", "deployment", "service"} <= types_found
    assert result.source_id == "k8s-test"
    assert not result.warnings
    namespace_entries = [r for r in result.resources if r.resource_type == "namespace"]
    assert namespace_entries[0].estimated_records == 1

    events = list(connector.baseline())
    assert len(events) == len(result.resources)
    first = events[0]
    assert first.source_system == "kubernetes"
    assert first.source_instance_id == "k8s-test"
    assert first.payload and first.content_hash

    # Second baseline yields identical content hashes (deterministic mapping).
    again = list(connector.baseline())
    assert {e.content_hash for e in again} == {e.content_hash for e in events}

    fetched = connector.fetch_record("pod/ns1/pod-a")
    assert fetched.source_record_type == "pod"
    with pytest.raises(LookupError):
        connector.fetch_record("bogus")

    handled = list(connector.handle_event({"ref": "service/ns1/svc-a"}))
    assert len(handled) == 1

    health = connector.health()
    assert health.status == "HEALTHY"
    assert health.latency_ms is not None

    replayed = list(connector.replay(events[:1]))
    assert replayed == events[:1]


def test_kubernetes_namespace_scoping():
    from eoip.connectors.kubernetes import KubernetesConnector

    core = _FakeCoreV1()
    connector = KubernetesConnector(client=core, namespaces=["ns1"])
    result = connector.discover(DiscoveryScope(exclude=["ns1"]))
    assert result.resources == []
    result = connector.discover(DiscoveryScope(include=["ns1"]))
    assert any(r.resource_type == "pod" for r in result.resources)


# ---------------------------------------------------------------------------
# G2-SCALE-CACHE
# ---------------------------------------------------------------------------


class _FakeRedis:
    def __init__(self):
        self.data = {}
        self.fail = False

    def get(self, key):
        if self.fail:
            raise ConnectionError("boom")
        return self.data.get(key)

    def setex(self, key, ttl, value):
        if self.fail:
            raise ConnectionError("boom")
        self.data[key] = value

    def delete(self, key):
        self.data.pop(key, None)

    def scan_iter(self, pattern):
        return [k for k in self.data if k.startswith(pattern.rstrip("*"))]


def test_distributed_cache_semantics_match_in_memory():
    from eoip.query.distributed_cache import DistributedQueryCache

    store = _store()
    distributed = DistributedQueryCache(client=_FakeRedis())
    local = SemanticQueryCache()
    assert distributed.plan_key(_plan()) == local.plan_key(_plan())
    assert distributed.fingerprint(store) == local.fingerprint(store)

    assert distributed.get(_plan(), store) is None
    distributed.put(_plan(), store, {"nodes": [1]})
    assert distributed.get(_plan(), store) == {"nodes": [1]}
    assert distributed.stats()["redis_hits"] == 1

    store.upsert_vertex("WorkItem", {"canonical_id": "w:2", "issue_key": "EOIP-2", "summary": "Two"})
    assert distributed.get(_plan(), store) is None  # fingerprint change evicts


def test_distributed_cache_shared_across_instances():
    from eoip.query.distributed_cache import DistributedQueryCache

    shared = _FakeRedis()
    store = _store()
    first = DistributedQueryCache(client=shared)
    second = DistributedQueryCache(client=shared)
    first.put(_plan(), store, "shared-result")
    assert second.get(_plan(), store) == "shared-result"
    assert second.backend == "redis"


def test_distributed_cache_clear():
    from eoip.query.distributed_cache import DistributedQueryCache

    store = _store()
    cache = DistributedQueryCache(client=_FakeRedis())
    cache.put(_plan(), store, "x")
    cache.clear()
    assert cache.get(_plan(), store) is None


def test_distributed_cache_falls_back_when_unavailable(monkeypatch):
    if HAS_REDIS_PKG:
        pytest.skip("forces absence of redis")

    from eoip.query.distributed_cache import DistributedQueryCache

    monkeypatch.setenv("EOIP_REDIS_URL", "redis://localhost:6379/0")
    cache = DistributedQueryCache()  # package missing -> in-memory backend
    assert cache.backend == "memory"
    store = _store()
    cache.put(_plan(), store, "local")
    assert cache.get(_plan(), store) == "local"
    assert cache.stats()["backend"] == "memory"


def test_distributed_cache_degrades_on_runtime_errors():
    from eoip.query.distributed_cache import DistributedQueryCache

    store = _store()
    fake = _FakeRedis()
    cache = DistributedQueryCache(client=fake)

    fake.fail = True
    cache.put(_plan(), store, "v")  # error -> memory fallback stores locally
    assert cache.backend == "memory"
    assert cache.get(_plan(), store) == "v"
