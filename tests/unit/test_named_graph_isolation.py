from __future__ import annotations

import time

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.named_graph import CrossTenantViolation, NamedGraphManager, TenantConfig
from eoip.tenancy.service import TenancyService


def _symbol(store, canonical_id: str, name: str):
    return store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": canonical_id,
            "qualified_name": name,
            "symbol_kind": "function",
            "name": name,
            "path": f"{name}.py",
        },
    )


@pytest.mark.req("KGR-G-013")
def test_named_graph_vertices_are_invisible_across_tenants() -> None:
    manager = NamedGraphManager(MemoryGraphStore())
    tenant_a = manager.create_tenant(TenantConfig("tenant-a", "g:tenant-a"))
    tenant_b = manager.create_tenant(TenantConfig("tenant-b", "g:tenant-b"))

    _symbol(tenant_a, "symbol:shared-name", "handler")
    _symbol(tenant_b, "symbol:shared-name", "handler")

    assert tenant_a.count_vertices("CodeSymbol") == 1
    assert tenant_b.count_vertices("CodeSymbol") == 1
    assert tenant_a.get_vertex_by_canonical_id("symbol:shared-name")["canonical_id"].startswith("g:tenant-a:")
    assert tenant_b.get_vertex_by_canonical_id("symbol:shared-name")["canonical_id"].startswith("g:tenant-b:")
    with pytest.raises(CrossTenantViolation):
        tenant_a.get_vertex_by_canonical_id("g:tenant-b:symbol:shared-name")


@pytest.mark.req("KGR-G-013")
def test_named_graph_blocks_adversarial_cross_namespace_edges() -> None:
    manager = NamedGraphManager(MemoryGraphStore())
    tenant_a = manager.create_tenant(TenantConfig("tenant-a", "g:tenant-a"))
    tenant_b = manager.create_tenant(TenantConfig("tenant-b", "g:tenant-b"))
    a_symbol = _symbol(tenant_a, "symbol:a", "a")
    b_symbol = _symbol(tenant_b, "symbol:b", "b")

    with pytest.raises(CrossTenantViolation):
        tenant_a.upsert_edge("CALLS", a_symbol["canonical_id"], b_symbol["canonical_id"], {"fact_key": "attack"})

    assert manager.isolation_guard.violation_count == 1
    assert tenant_a.count_edges("CALLS") == 0
    assert tenant_b.count_edges("CALLS") == 0


@pytest.mark.req("KGR-G-013")
def test_named_graph_edges_and_counts_are_tenant_scoped() -> None:
    manager = NamedGraphManager(MemoryGraphStore())
    tenant_a = manager.create_tenant(TenantConfig("tenant-a", "g:tenant-a"))
    tenant_b = manager.create_tenant(TenantConfig("tenant-b", "g:tenant-b"))
    caller = _symbol(tenant_a, "symbol:caller", "caller")
    callee = _symbol(tenant_a, "symbol:callee", "callee")
    _symbol(tenant_b, "symbol:other", "other")

    tenant_a.upsert_edge("CALLS", caller["canonical_id"], callee["canonical_id"], {"fact_key": "tenant-a-call"})

    assert tenant_a.count_edges("CALLS") == 1
    assert tenant_b.count_edges("CALLS") == 0
    assert tenant_a.edges_from(caller["canonical_id"], labels=["CALLS"])[0]["in_cid"].startswith("g:tenant-a:")


@pytest.mark.req("KGR-G-013")
def test_named_graph_creation_deletion_latency_and_thousand_tenant_support() -> None:
    manager = NamedGraphManager(MemoryGraphStore())
    started = time.perf_counter()
    tenant = manager.create_tenant(TenantConfig("tenant-0000", "g:tenant-0000"))
    assert tenant.tenant_id == "tenant-0000"
    assert (time.perf_counter() - started) * 1000 < 50
    started = time.perf_counter()
    assert manager.remove_tenant("tenant-0000")
    assert (time.perf_counter() - started) * 1000 < 50

    for index in range(1000):
        manager.create_tenant(TenantConfig(f"tenant-{index:04d}", f"g:tenant-{index:04d}"))

    assert manager.tenant_count == 1000


@pytest.mark.req("KGR-G-013")
def test_tenancy_service_wires_named_graphs_to_tenant_facade() -> None:
    service = TenancyService(MemoryGraphStore())

    graph = service.named_graph_for("tenant-a")
    _symbol(graph, "symbol:a", "a")

    assert service.named_graph_for("tenant-a").count_vertices("CodeSymbol") == 1
    assert service.named_graph_for("tenant-b").count_vertices("CodeSymbol") == 0
