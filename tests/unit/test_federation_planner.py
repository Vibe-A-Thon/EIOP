"""Unit tests for the federated query planner (GAP-FABRIC-001..008)."""

from __future__ import annotations

import pytest

from eoip.federation import (
    FederatedQueryPlanner,
    HugeGraphLocalAdapter,
    InMemoryDemoAdapter,
    SourceCapability,
    SourceMode,
)

REQ = pytest.mark.req


def _cap(source_id, entity_types, mode=SourceMode.LIVE, push_filters=False,
         push_projection=False, freshness=None, authority=1.0, locality=1.0):
    return SourceCapability(
        source_id=source_id,
        entity_types=entity_types,
        pushdown_filters=push_filters,
        pushdown_projection=push_projection,
        mode=mode,
        freshness_seconds=freshness,
        authority=authority,
        locality=locality,
    )


CRM_ROWS = [
    {"canonical_id": "urn:eoip:crm:customer:1", "entity_type": "Customer",
     "name": "Acme", "region": "EMEA"},
    {"canonical_id": "urn:eoip:crm:customer:2", "entity_type": "Customer",
     "name": "Globex", "region": "APAC"},
]

JIRA_ROWS = [
    {"canonical_id": "urn:eoip:jira:issue:10", "entity_type": "Issue",
     "key": "PROJ-1", "status": "Open"},
    {"canonical_id": "urn:eoip:jira:issue:11", "entity_type": "Issue",
     "key": "PROJ-2", "status": "Done"},
]


def _planner() -> FederatedQueryPlanner:
    planner = FederatedQueryPlanner()
    planner.register(InMemoryDemoAdapter(
        _cap("crm", ["Customer"], push_filters=True, push_projection=True),
        CRM_ROWS,
    ))
    planner.register(InMemoryDemoAdapter(
        _cap("jira", ["Issue"], mode=SourceMode.MATERIALIZED,
             push_filters=True, freshness=30.0),
        JIRA_ROWS,
    ))
    return planner


@REQ("FABRIC-001")
def test_source_capability_registry():
    planner = _planner()
    caps = planner.sources()
    assert {c.source_id for c in caps} == {"crm", "jira"}
    crm = next(c for c in caps if c.source_id == "crm")
    assert crm.urn() == "urn:eoip:federation:source:crm"
    assert "Customer" in crm.entity_types


@REQ("FABRIC-002")
def test_fragment_planning_splits_per_source():
    planner = _planner()
    fragments = planner.plan_fragments(["Customer", "Issue"])
    assert len(fragments) == 2
    by_source = {f.source_id: f for f in fragments}
    assert by_source["crm"].entity_types == ["Customer"]
    assert by_source["jira"].entity_types == ["Issue"]


@REQ("FABRIC-003")
def test_cost_aware_routing_prefers_materialized():
    planner = _planner()
    fragments = planner.plan_fragments(["Customer", "Issue"])
    assert fragments[0].source_id == "jira"  # MATERIALIZED beats LIVE
    result = planner.execute(["Customer", "Issue"])
    order = [d["source_id"] for d in result["plan"]["fragments"]]
    assert order == ["jira", "crm"]
    costs = {d["source_id"]: d["cost"] for d in result["plan"]["fragments"]}
    assert costs["jira"] < costs["crm"]


@REQ("FABRIC-004")
def test_pushdown_filters_and_projection():
    planner = _planner()
    result = planner.execute(
        ["Customer"], filters={"region": "EMEA"}, projection=["canonical_id", "name"]
    )
    assert result["row_count"] == 1
    row = result["rows"][0]
    assert row["name"] == "Acme"
    assert set(row.keys()) == {"canonical_id", "name", "_provenance"}
    decision = result["plan"]["fragments"][0]
    assert decision["pushed_filters"] is True
    assert decision["pushed_projection"] is True


@REQ("FABRIC-004")
def test_no_pushdown_where_unsupported():
    planner = FederatedQueryPlanner()
    planner.register(InMemoryDemoAdapter(
        _cap("raw", ["Customer"]),  # no pushdown support
        CRM_ROWS,
    ))
    fragments = planner.plan_fragments(["Customer"], filters={"region": "EMEA"})
    assert fragments[0].filters == {}
    result = planner.execute(["Customer"], filters={"region": "EMEA"})
    assert result["row_count"] == 1  # local merge still applies the filter
    assert result["plan"]["fragments"][0]["pushed_filters"] is False


@REQ("FABRIC-005")
def test_merge_attaches_row_provenance():
    planner = _planner()
    result = planner.execute(["Customer", "Issue"])
    assert result["row_count"] == 4
    for row in result["rows"]:
        prov = row["_provenance"]
        assert len(prov["sources"]) == 1
        assert prov["source_urns"][0].startswith("urn:eoip:federation:source:")


@REQ("FABRIC-005")
def test_merge_fills_missing_fields_across_sources():
    planner = FederatedQueryPlanner()
    planner.register(InMemoryDemoAdapter(
        _cap("a", ["Customer"]),
        [{"canonical_id": "c1", "entity_type": "Customer", "name": "Acme"}],
    ))
    planner.register(InMemoryDemoAdapter(
        _cap("b", ["Customer"]),
        [{"canonical_id": "c1", "entity_type": "Customer", "region": "EMEA"}],
    ))
    result = planner.execute(["Customer"], merge_key="canonical_id")
    assert result["row_count"] == 1
    row = result["rows"][0]
    assert row["name"] == "Acme"
    assert row["region"] == "EMEA"
    assert sorted(row["_provenance"]["sources"]) == ["a", "b"]


@REQ("FABRIC-006")
def test_offline_degradation_continues():
    planner = _planner()
    crm_adapter = planner._adapters["crm"]
    crm_adapter.set_healthy(False)
    result = planner.execute(["Customer", "Issue"])
    assert result["degraded"] is True
    assert result["plan"]["degraded_sources"] == ["crm"]
    statuses = {d["source_id"]: d["status"] for d in result["plan"]["fragments"]}
    assert statuses["crm"] == "degraded"
    assert statuses["jira"] == "executed"
    # Available source still returned rows.
    assert result["row_count"] == 2


@REQ("FABRIC-007")
def test_explainable_routing_plan():
    planner = _planner()
    result = planner.execute(["Customer"], filters={"region": "APAC"},
                             projection=["canonical_id"])
    plan = result["plan"]
    assert "total_cost" in plan
    frag = plan["fragments"][0]
    for key in ("fragment_id", "source_id", "mode", "cost", "reason",
                "status", "pushed_filters", "pushed_projection",
                "row_count", "elapsed_ms"):
        assert key in frag
    assert frag["status"] == "executed"
    assert "filters pushed down" in frag["reason"]


@REQ("FABRIC-008")
def test_duplicate_coverage_secondary_source():
    planner = FederatedQueryPlanner()
    planner.register(InMemoryDemoAdapter(
        _cap("primary", ["Customer"], mode=SourceMode.MATERIALIZED, authority=1.0),
        CRM_ROWS,
    ))
    planner.register(InMemoryDemoAdapter(
        _cap("secondary", ["Customer"], mode=SourceMode.LIVE, authority=0.3),
        CRM_ROWS,
    ))
    fragments = planner.plan_fragments(["Customer"])
    assert fragments[0].source_id == "primary"
    assert fragments[1].source_id == "secondary"
    assert "secondary/duplicate coverage" in fragments[1].reason


@REQ("FABRIC-001")
def test_hugegraph_local_adapter_over_graph_store():
    from eoip.graph.memory import MemoryGraphStore

    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:hg:service:1",
                                    "name": "Acme"})
    store.upsert_vertex("Service", {"canonical_id": "urn:eoip:hg:service:2",
                                    "name": "Globex"})

    planner = FederatedQueryPlanner()
    planner.register(HugeGraphLocalAdapter(
        _cap("hugegraph-local", ["Service"]), store
    ))
    result = planner.execute(["Service"])
    assert result["row_count"] == 2
    names = {r["name"] for r in result["rows"]}
    assert names == {"Acme", "Globex"}
    prov = result["rows"][0]["_provenance"]
    assert prov["source_urns"] == ["urn:eoip:federation:source:hugegraph-local"]
