from __future__ import annotations

import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.named_graph import (
    CrossTenantViolation,
    NamedGraphManager,
    NamedGraphStore,
    TenantConfig,
)

pytestmark = [pytest.mark.req("KGR-G-013", "SR-TEN-001")]


@pytest.fixture
def memory_store():
    return MemoryGraphStore()


@pytest.fixture
def tenant_alpha(memory_store):
    return NamedGraphStore(memory_store, TenantConfig(tenant_id="tenant-alpha", graph_name="g:tenant-alpha"))


@pytest.fixture
def tenant_beta(memory_store):
    return NamedGraphStore(memory_store, TenantConfig(tenant_id="tenant-beta", graph_name="g:tenant-beta"))


def test_named_graph_vertex_isolation(tenant_alpha, tenant_beta):
    # Upsert vertex with tenant-alpha
    v_alpha = tenant_alpha.upsert_vertex(
        "Project", {"canonical_id": "urn:project:1", "name": "Alpha Project"}
    )
    assert v_alpha["canonical_id"].startswith("g:tenant-alpha:")

    # Upsert vertex with tenant-beta with same local ID
    v_beta = tenant_beta.upsert_vertex(
        "Project", {"canonical_id": "urn:project:1", "name": "Beta Project"}
    )
    assert v_beta["canonical_id"].startswith("g:tenant-beta:")

    # Fetching from tenant_alpha returns Alpha Project
    fetched_alpha = tenant_alpha.get_vertex_by_canonical_id("urn:project:1")
    assert fetched_alpha is not None
    assert fetched_alpha["properties"]["name"] == "Alpha Project"

    # Fetching from tenant_beta returns Beta Project
    fetched_beta = tenant_beta.get_vertex_by_canonical_id("urn:project:1")
    assert fetched_beta is not None
    assert fetched_beta["properties"]["name"] == "Beta Project"


def test_cross_tenant_access_raises_violation(tenant_alpha, tenant_beta):
    # Alpha creates a vertex
    tenant_alpha.upsert_vertex(
        "Project", {"canonical_id": "urn:project:alpha", "name": "Secret Project"}
    )

    # Beta trying to directly access Alpha's namespaced canonical ID raises CrossTenantViolation
    with pytest.raises(CrossTenantViolation) as exc_info:
        tenant_beta.get_vertex_by_canonical_id("g:tenant-alpha:urn:project:alpha")
    assert "Cross-tenant violation" in str(exc_info.value)
    assert exc_info.value.source_tenant == "tenant-beta"
    assert exc_info.value.target_tenant == "tenant-alpha"


def test_named_graph_edge_isolation_and_find_edges(tenant_alpha, tenant_beta):
    # Alpha nodes
    p_alpha = tenant_alpha.upsert_vertex(
        "Project", {"canonical_id": "urn:project:alpha", "name": "Alpha Project"}
    )
    w_alpha = tenant_alpha.upsert_vertex(
        "WorkItem", {
            "canonical_id": "urn:item:alpha",
            "issue_key": "ALPHA-1",
            "summary": "Alpha item",
            "ingestion_run_id": "run-1",
        }
    )
    tenant_alpha.upsert_edge("CONTAINS", p_alpha["vid"], w_alpha["vid"], {"fact_key": "fk-a"})

    # Beta nodes
    p_beta = tenant_beta.upsert_vertex(
        "Project", {"canonical_id": "urn:project:beta", "name": "Beta Project"}
    )
    w_beta = tenant_beta.upsert_vertex(
        "WorkItem", {
            "canonical_id": "urn:item:beta",
            "issue_key": "BETA-1",
            "summary": "Beta item",
            "ingestion_run_id": "run-1",
        }
    )
    tenant_beta.upsert_edge("CONTAINS", p_beta["vid"], w_beta["vid"], {"fact_key": "fk-b"})

    # Alpha edges
    alpha_edges = tenant_alpha.find_edges(label="CONTAINS")
    assert len(alpha_edges) == 1
    assert "tenant-alpha" in alpha_edges[0]["out_cid"]

    # Beta edges
    beta_edges = tenant_beta.find_edges(label="CONTAINS")
    assert len(beta_edges) == 1
    assert "tenant-beta" in beta_edges[0]["out_cid"]

    # Cross-tenant edge traversal
    from_alpha = tenant_alpha.edges_from(p_alpha["vid"])
    assert len(from_alpha) == 1

    to_beta = tenant_beta.edges_to(w_beta["vid"])
    assert len(to_beta) == 1


def test_named_graph_find_vertex_by_property_and_count(tenant_alpha):
    tenant_alpha.upsert_vertex(
        "Project", {"canonical_id": "urn:project:p1", "name": "Project One"}
    )
    tenant_alpha.upsert_vertex(
        "Project", {"canonical_id": "urn:project:p2", "name": "Project Two"}
    )

    found = tenant_alpha.find_vertex_by_property("Project", "name", "Project One")
    assert len(found) == 1
    assert found[0]["properties"]["name"] == "Project One"

    assert tenant_alpha.count_vertices("Project") == 2


def test_named_graph_manager(memory_store):
    manager = NamedGraphManager(memory_store)
    cfg1 = TenantConfig(tenant_id="tenant-1", graph_name="g:tenant-1")
    t1 = manager.create_tenant(cfg1)
    assert manager.get_tenant("tenant-1") is t1
    assert manager.tenant_count == 1

    # Duplicate creation error
    with pytest.raises(ValueError, match="already exists"):
        manager.create_tenant(cfg1)

    # Removal
    assert manager.remove_tenant("tenant-1") is True
    assert manager.get_tenant("tenant-1") is None
