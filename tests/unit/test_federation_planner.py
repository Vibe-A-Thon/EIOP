"""Unit tests for the federated query planner (GAP-FABRIC-001..008)."""

from __future__ import annotations

import pytest
from eoip.federation import (
    FederatedQueryPlanner,
    FileSourceAdapter,
    HugeGraphLocalAdapter,
    InMemoryRowAdapter,
    JdbcSourceAdapter,
    SourceCapability,
    SourceMode,
    SourcePolicy,
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
    planner.register(InMemoryRowAdapter(
        _cap("crm", ["Customer"], push_filters=True, push_projection=True),
        CRM_ROWS,
    ))
    planner.register(InMemoryRowAdapter(
        _cap("jira", ["Issue"], mode=SourceMode.MATERIALIZED,
             push_filters=True, freshness=30.0),
        JIRA_ROWS,
    ))
    return planner


@REQ("GAP-FABRIC-002")
def test_source_capability_registry():
    planner = _planner()
    caps = planner.sources()
    assert {c.source_id for c in caps} == {"crm", "jira"}
    crm = next(c for c in caps if c.source_id == "crm")
    assert crm.urn() == "urn:eoip:federation:source:crm"
    assert "Customer" in crm.entity_types


@REQ("GAP-FABRIC-002")
def test_fragment_planning_splits_per_source():
    planner = _planner()
    fragments = planner.plan_fragments(["Customer", "Issue"])
    assert len(fragments) == 2
    by_source = {f.source_id: f for f in fragments}
    assert by_source["crm"].entity_types == ["Customer"]
    assert by_source["jira"].entity_types == ["Issue"]


@REQ("GAP-FABRIC-003")
def test_cost_aware_routing_prefers_materialized():
    planner = _planner()
    fragments = planner.plan_fragments(["Customer", "Issue"])
    assert fragments[0].source_id == "jira"  # MATERIALIZED beats LIVE
    result = planner.execute(["Customer", "Issue"])
    order = [d["source_id"] for d in result["plan"]["fragments"]]
    assert order == ["jira", "crm"]
    costs = {d["source_id"]: d["cost"] for d in result["plan"]["fragments"]}
    assert costs["jira"] < costs["crm"]


@REQ("GAP-FABRIC-004")
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


@REQ("GAP-FABRIC-004")
def test_no_pushdown_where_unsupported():
    planner = FederatedQueryPlanner()
    planner.register(InMemoryRowAdapter(
        _cap("raw", ["Customer"]),  # no pushdown support
        CRM_ROWS,
    ))
    fragments = planner.plan_fragments(["Customer"], filters={"region": "EMEA"})
    assert fragments[0].filters == {}
    result = planner.execute(["Customer"], filters={"region": "EMEA"})
    assert result["row_count"] == 1  # local merge still applies the filter
    assert result["plan"]["fragments"][0]["pushed_filters"] is False


@REQ("GAP-FABRIC-005")
def test_merge_attaches_row_provenance():
    planner = _planner()
    result = planner.execute(["Customer", "Issue"])
    assert result["row_count"] == 4
    for row in result["rows"]:
        prov = row["_provenance"]
        assert len(prov["sources"]) == 1
        assert prov["source_urns"][0].startswith("urn:eoip:federation:source:")


@REQ("GAP-FABRIC-005")
def test_merge_fills_missing_fields_across_sources():
    planner = FederatedQueryPlanner()
    planner.register(InMemoryRowAdapter(
        _cap("a", ["Customer"]),
        [{"canonical_id": "c1", "entity_type": "Customer", "name": "Acme"}],
    ))
    planner.register(InMemoryRowAdapter(
        _cap("b", ["Customer"]),
        [{"canonical_id": "c1", "entity_type": "Customer", "region": "EMEA"}],
    ))
    result = planner.execute(["Customer"], merge_key="canonical_id")
    assert result["row_count"] == 1
    row = result["rows"][0]
    assert row["name"] == "Acme"
    assert row["region"] == "EMEA"
    assert sorted(row["_provenance"]["sources"]) == ["a", "b"]


@REQ("GAP-FABRIC-006")
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


@REQ("GAP-FABRIC-007")
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


@REQ("GAP-FABRIC-007")
def test_duplicate_coverage_secondary_source():
    planner = FederatedQueryPlanner()
    planner.register(InMemoryRowAdapter(
        _cap("primary", ["Customer"], mode=SourceMode.MATERIALIZED, authority=1.0),
        CRM_ROWS,
    ))
    planner.register(InMemoryRowAdapter(
        _cap("secondary", ["Customer"], mode=SourceMode.LIVE, authority=0.3),
        CRM_ROWS,
    ))
    fragments = planner.plan_fragments(["Customer"])
    assert fragments[0].source_id == "primary"
    assert fragments[1].source_id == "secondary"
    assert "secondary/duplicate coverage" in fragments[1].reason


@REQ("GAP-FABRIC-001")
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


@REQ("GAP-FED")
@REQ("GAP-FED-001")
@REQ("GAP-FED-004")
def test_file_and_jdbc_adapters_query_external_sources_without_hugegraph(tmp_path):
    file_path = tmp_path / "services.json"
    file_path.write_text(
        """{"rows":[{"canonical_id":"svc:1","entity_type":"Service","name":"Billing","tier":"gold"}]}""",
        encoding="utf-8",
    )
    db_path = tmp_path / "issues.db"
    import sqlite3

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TABLE issues (canonical_id TEXT, entity_type TEXT, issue_key TEXT, status TEXT)"
        )
        conn.execute(
            "INSERT INTO issues VALUES ('wi:1', 'WorkItem', 'PAY-1', 'Open')"
        )

    planner = FederatedQueryPlanner()
    planner.register(
        FileSourceAdapter(
            _cap("file-services", ["Service"], mode=SourceMode.VIRTUAL, push_filters=True),
            file_path,
        )
    )
    planner.register(
        JdbcSourceAdapter(
            _cap("jdbc-issues", ["WorkItem"], mode=SourceMode.VIRTUAL, push_filters=True),
            db_path,
            "issues",
        )
    )

    result = planner.execute(["Service", "WorkItem"])

    assert result["row_count"] == 2
    adapter_kinds = {
        detail["adapter_kind"]
        for row in result["rows"]
        for detail in row["_provenance"]["source_details"]
    }
    assert adapter_kinds == {"file", "jdbc"}


@REQ("GAP-FED")
@REQ("GAP-FED-002")
@REQ("GAP-FABRIC-005")
@REQ("GAP-FABRIC-006")
def test_cache_mode_serves_fresh_cached_rows_when_source_goes_offline():
    adapter = InMemoryRowAdapter(
        _cap(
            "cached",
            ["Customer"],
            mode=SourceMode.CACHE,
            push_filters=True,
            freshness=120.0,
        ),
        CRM_ROWS,
    )
    planner = FederatedQueryPlanner()
    planner.register(adapter)

    first = planner.execute(["Customer"], filters={"region": "EMEA"})
    adapter.set_healthy(False)
    second = planner.execute(["Customer"], filters={"region": "EMEA"})

    assert first["plan"]["fragments"][0]["cache_hit"] is False
    assert second["degraded"] is False
    assert second["plan"]["fragments"][0]["cache_hit"] is True
    assert second["rows"][0]["_freshness"]["ttl_seconds"] == 120.0


@REQ("GAP-FED")
@REQ("GAP-FED-002")
def test_entity_mode_policy_splits_virtual_cache_and_materialized_fragments():
    planner = FederatedQueryPlanner()
    planner.register(
        InMemoryRowAdapter(
            SourceCapability(
                source_id="mixed-policy",
                entity_types=["Customer", "Issue"],
                entity_modes={
                    "Customer": SourceMode.VIRTUAL,
                    "Issue": SourceMode.MATERIALIZE,
                },
            ),
            [*CRM_ROWS, *JIRA_ROWS],
        )
    )

    fragments = planner.plan_fragments(["Customer", "Issue"])

    assert [fragment.access_mode for fragment in fragments] == [
        SourceMode.VIRTUAL,
        SourceMode.MATERIALIZE,
    ]


@REQ("GAP-FED")
@REQ("GAP-FED-003")
def test_explainable_plan_distinguishes_hugegraph_and_live_sources():
    planner = FederatedQueryPlanner()
    planner.register(
        InMemoryRowAdapter(
            _cap("external-rest-like", ["Customer"], mode=SourceMode.VIRTUAL),
            CRM_ROWS,
        )
    )

    result = planner.execute(["Customer"])

    decision = result["plan"]["fragments"][0]
    provenance = result["rows"][0]["_provenance"]["source_details"][0]
    assert decision["mode"] == "VIRTUAL"
    assert decision["adapter_kind"] == "generic"
    assert provenance["mode"] == "VIRTUAL"


@REQ("GAP-FABRIC-008")
def test_source_policy_enforces_role_purpose_filters_and_field_denial():
    planner = FederatedQueryPlanner()
    planner.register(
        InMemoryRowAdapter(
            SourceCapability(
                source_id="restricted",
                entity_types=["Customer"],
                pushdown_filters=True,
                mode=SourceMode.VIRTUAL,
                policy=SourcePolicy(
                    allowed_roles=["analyst"],
                    required_purpose="support",
                    required_filters={"region": "EMEA"},
                    denied_fields=["internal_note"],
                    max_rows=1,
                ),
            ),
            [
                {**CRM_ROWS[0], "internal_note": "restricted"},
                {**CRM_ROWS[1], "internal_note": "restricted"},
            ],
        )
    )

    denied = planner.execute(
        ["Customer"],
        filters={"region": "EMEA"},
        policy_context={"roles": ["viewer"], "purpose": "support"},
    )
    allowed = planner.execute(
        ["Customer"],
        filters={"region": "EMEA"},
        policy_context={"roles": ["analyst"], "purpose": "support"},
    )

    assert denied["row_count"] == 0
    assert denied["plan"]["policy_denied_sources"] == ["restricted"]
    assert allowed["row_count"] == 1
    assert "internal_note" not in allowed["rows"][0]
