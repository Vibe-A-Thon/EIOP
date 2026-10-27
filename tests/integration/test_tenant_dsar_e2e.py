"""Tenant isolation + DSAR erasure end-to-end over the GraphStore port (CC3-011, SR-TEN-003, SR-PRV-002).

Proves, on the shared in-memory backend:

* two tenants populated through ``TenantScopedGraphStore`` (the port-boundary
  namespace enforcement layer in ``eoip.graph.tenant_store``) cannot read each
  other's vertices/edges — explicit foreign ids fail closed with
  ``ScopeViolationError`` and opaque-id probes are indistinguishable not-found;
* the authz barrier (``MultiTenantBarrierEnforcer``) and the tenancy layer
  handles (``TenantLayers`` search/vector surfaces) independently deny
  cross-tenant reach;
* a DSAR locate + ``ErasurePropagator`` run for one subject tombstones the
  graph entity and erases the derived search-index/vector/registry artifacts,
  leaving the other tenant's data untouched.
"""

from __future__ import annotations

import pytest
from eoip.authz.pdp import ScopeViolationError
from eoip.contracts.canonical import PrincipalType, TrustedScope
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.tenant_store import TenantScopedGraphStore
from eoip.privacy.dsar import ErasurePropagator, locate_subject
from eoip.tenancy.isolation import IsolationRegistry
from eoip.tenancy.isolation_hardened import MultiTenantBarrierEnforcer
from eoip.tenancy.layers import IsolationViolation, TenantLayers

MASTER_KEY = bytes(range(32))
TENANT_A = "tenant_a"
TENANT_B = "tenant_b"
SUBJECT_EMAIL = "alice@tenant-a.example"


@pytest.fixture
def layers(tmp_path):
    return TenantLayers(IsolationRegistry(), root=tmp_path, master_key=MASTER_KEY)


@pytest.fixture
def env(layers):
    """Two tenants sharing one MemoryGraphStore behind scoped port wrappers."""
    inner = MemoryGraphStore()
    store_a = TenantScopedGraphStore(inner, TENANT_A)
    store_b = TenantScopedGraphStore(inner, TENANT_B)
    handle_a = layers.ensure_tenant(TENANT_A)
    handle_b = layers.ensure_tenant(TENANT_B)

    person_a = store_a.upsert_vertex("Person", {
        "canonical_id": handle_a.graph_id("person-alice"),
        "display_name": "Alice A",
        "email": SUBJECT_EMAIL,
    })
    item_a = store_a.upsert_vertex("WorkItem", {
        "canonical_id": handle_a.graph_id("wi-1"),
        "issue_key": "A-1",
        "summary": "Tenant A work item",
    })
    store_a.upsert_edge("ASSIGNED_TO", item_a["vid"], person_a["vid"],
                        {"fact_key": "assign-a-1", "creation_status": "DETERMINISTIC"})
    handle_a.search_add(person_a["canonical_id"], "Alice A alice@tenant-a.example")
    handle_a.vector_upsert(person_a["canonical_id"], [1.0, 0.0],
                           {"display_name": "Alice A", "email": SUBJECT_EMAIL})

    person_b = store_b.upsert_vertex("Person", {
        "canonical_id": handle_b.graph_id("person-bob"),
        "display_name": "Bob B",
        "email": "bob@tenant-b.example",
    })
    store_b.upsert_vertex("WorkItem", {
        "canonical_id": handle_b.graph_id("wi-1"),
        "issue_key": "B-1",
        "summary": "Tenant B work item",
    })
    handle_b.search_add(person_b["canonical_id"], "Bob B bob@tenant-b.example")

    return {
        "inner": inner, "store_a": store_a, "store_b": store_b,
        "handle_a": handle_a, "handle_b": handle_b,
        "person_a": person_a, "item_a": item_a, "person_b": person_b,
    }


def _scope(tenant_id: str) -> TrustedScope:
    return TrustedScope(
        tenant_id=tenant_id,
        workspace_id=f"ws-{tenant_id}",
        principal_id=f"user-{tenant_id}",
        principal_type=PrincipalType.USER,
        roles=["analyst"],
        effective_acls=[f"tenant:{tenant_id}"],
        policy_epoch=1,
    )


class TestCrossTenantGraphDenial:
    def test_foreign_canonical_id_read_fails_closed(self, env):
        with pytest.raises(ScopeViolationError):
            env["store_b"].get_vertex_by_canonical_id(env["person_a"]["canonical_id"])

    def test_opaque_vid_probe_is_indistinguishable_not_found(self, env):
        assert env["store_b"].get_vertex(env["person_a"]["vid"]) is None

    def test_property_scan_never_leaks_foreign_rows(self, env):
        hits = env["store_b"].find_vertex_by_property("Person", "email", SUBJECT_EMAIL)
        assert hits == []
        emails = {v["properties"].get("email") for v in env["store_b"].find_vertices(label="Person")}
        assert emails == {"bob@tenant-b.example"}

    def test_scans_are_tenant_bounded(self, env):
        assert env["store_a"].count_vertices() == 2
        assert env["store_b"].count_vertices() == 2
        assert env["inner"].count_vertices() == 4  # shared backend holds both, scoped views do not

    def test_cross_tenant_edge_write_rejected(self, env):
        with pytest.raises(ScopeViolationError):
            env["store_b"].upsert_edge(
                "ASSIGNED_TO", env["item_a"]["vid"], env["person_b"]["vid"],
                {"fact_key": "x-tenant", "creation_status": "DETERMINISTIC"},
            )

    def test_foreign_tombstone_fails_closed(self, env):
        with pytest.raises(ScopeViolationError):
            env["store_b"].tombstone_vertex(env["person_a"]["canonical_id"])

    def test_tenant_handle_cannot_clear_shared_store(self, env):
        with pytest.raises(ScopeViolationError):
            env["store_a"].clear()
        assert env["inner"].count_vertices() == 4

    def test_authz_barrier_denies_cross_tenant_target(self, env):
        enforcer = MultiTenantBarrierEnforcer()
        with pytest.raises(ScopeViolationError):
            enforcer.assert_same_tenant(
                _scope(TENANT_B), TENANT_A,
                entity_canonical_id=env["person_a"]["canonical_id"],
            )

    def test_tenancy_layer_search_and_vector_surfaces_isolated(self, env):
        handle_a, handle_b = env["handle_a"], env["handle_b"]
        assert env["person_a"]["canonical_id"] in handle_a.search_docs()
        assert env["person_a"]["canonical_id"] not in handle_b.search_docs()
        assert handle_a.search_index().keyword_search("alice")
        assert handle_b.search_index().keyword_search("alice") == []
        with pytest.raises(IsolationViolation):
            handle_b.vector_search([1.0, 0.0], collection=handle_a._p("vector_collection"))


class _SearchDocRegistry:
    """DerivedDataRegistry port over a tenant's search documents."""

    def __init__(self, handle):
        self._handle = handle

    def find_by_source(self, source_ref: str, tenant_id: str | None = None) -> list[dict]:
        return [
            {"ref": doc_id, "kind": "search_doc"}
            for doc_id, (text, _meta) in self._handle.search_docs().items()
            if source_ref in text
        ]


class _VectorRegistry:
    """DerivedDataRegistry port over a tenant's vector collection."""

    def __init__(self, handle):
        self._handle = handle

    def find_by_source(self, source_ref: str, tenant_id: str | None = None) -> list[dict]:
        return [
            {"ref": doc_id, "kind": "vector_index_entry"}
            for doc_id, (_vec, payload) in self._handle.vector_items().items()
            if source_ref in doc_id or source_ref in str(payload)
        ]


class TestDsarErasureEndToEnd:
    def test_locate_then_erase_removes_graph_and_derived_copies(self, env):
        store_a, handle_a = env["store_a"], env["handle_a"]
        cid = env["person_a"]["canonical_id"]

        report = locate_subject(
            SUBJECT_EMAIL,
            tenant_id=TENANT_A,
            graph_store=store_a,
            graph_labels=["Person"],
            derived_registries=[_SearchDocRegistry(handle_a), _VectorRegistry(handle_a)],
        )
        surfaces = report.surface_counts()
        assert surfaces.get("graph") == 1
        assert surfaces.get("derived") == 2  # search doc + vector entry

        propagator = ErasurePropagator(
            graph_store=store_a,
            derived_erasers={
                "search_doc": lambda ref, _tid: (handle_a.search_remove(ref), True)[1],
                "vector_index_entry": lambda ref, _tid: handle_a.vector_delete(ref),
            },
        )
        proof = propagator.erase(report)

        assert proof.tenant_id == TENANT_A
        assert proof.tombstoned_refs == [cid]
        assert sorted(proof.erased_derived_refs) == sorted([cid, cid]) or set(proof.erased_derived_refs) == {cid}
        assert proof.unerased_refs == []
        assert proof.digest and proof.id.endswith(proof.digest[:16])

        # graph store: erased subject absent from default scans, tombstone recorded
        assert store_a.find_vertex_by_property("Person", "email", SUBJECT_EMAIL) == []
        assert store_a.find_vertices(label="Person") == []
        tombstoned = store_a.get_vertex_by_canonical_id(cid)
        assert tombstoned["properties"]["deleted_at"]

        # search index + derived registries: subject is gone
        assert handle_a.search_index().keyword_search("alice") == []
        assert cid not in handle_a.search_docs()
        assert handle_a.vector_items() == {}

        # other tenant untouched
        assert env["store_b"].find_vertices(label="Person")
        assert env["handle_b"].search_index().keyword_search("bob")

    def test_dsar_locate_in_tenant_b_never_sees_tenant_a_subject(self, env):
        report = locate_subject(
            SUBJECT_EMAIL,
            tenant_id=TENANT_B,
            graph_store=env["store_b"],
            graph_labels=["Person"],
            derived_registries=[_SearchDocRegistry(env["handle_b"])],
        )
        assert report.hits == []
