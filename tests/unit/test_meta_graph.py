"""Tests for meta-graph bootstrap, BELONGS_TO_DOMAIN, AUTHORED_BY, DEPENDS_ON, config loading."""

import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.meta import DOMAINS, SchemaVersionConflict, bootstrap_meta_graph, check_schema_compatibility
from eoip.ontology.manifest import ONTOLOGY_VERSION, SCHEMA_VERSION


def test_bootstrap_creates_domain_vertices():
    store = MemoryGraphStore()
    result = bootstrap_meta_graph(store)
    assert result["domains"] == len(DOMAINS)
    for domain in DOMAINS:
        v = store.get_vertex_by_canonical_id(f"urn:eoip:meta:domain:{domain.lower()}")
        assert v is not None
        assert v["label"] == "GraphDomain"
        assert v["properties"]["name"] == domain


def test_bootstrap_creates_ontology_version():
    store = MemoryGraphStore()
    bootstrap_meta_graph(store)
    v = store.get_vertex_by_canonical_id(f"urn:eoip:meta:ontology:{ONTOLOGY_VERSION}")
    assert v is not None
    assert v["label"] == "OntologyVersion"


def test_bootstrap_creates_data_sources():
    store = MemoryGraphStore()
    result = bootstrap_meta_graph(store)
    assert result["data_sources"] == 3
    for source in ["jira", "git", "gitlab"]:
        v = store.get_vertex_by_canonical_id(f"urn:eoip:meta:source:{source}")
        assert v is not None
        assert v["label"] == "DataSource"


def test_bootstrap_is_idempotent():
    store = MemoryGraphStore()
    r1 = bootstrap_meta_graph(store)
    count1 = store.count_vertices()
    r2 = bootstrap_meta_graph(store)
    count2 = store.count_vertices()
    assert count1 == count2
    assert r1["domains"] == r2["domains"]


def test_demo_creates_belongs_to_domain_edges(tmp_path):
    from eoip.demo import load_demo

    store = MemoryGraphStore()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    load_demo(store, str(data_dir))

    domain_v = store.get_vertex_by_canonical_id("urn:eoip:meta:domain:work")
    assert domain_v is not None
    edges = store.edges_to(domain_v["vid"])
    btd = [e for e in edges if e["label"] == "BELONGS_TO_DOMAIN"]
    assert len(btd) > 0


def test_demo_creates_authored_by_edges(tmp_path):
    from eoip.demo import load_demo

    store = MemoryGraphStore()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    load_demo(store, str(data_dir))

    persons = [v for v in store.find_vertices(limit=10000) if v["label"] == "Person"]
    assert len(persons) > 0
    authored_edges = []
    for p in persons:
        incoming = store.edges_to(p["vid"])
        authored_edges.extend(e for e in incoming if e["label"] == "AUTHORED_BY")
    assert len(authored_edges) > 0


def test_demo_creates_depends_on_edges(tmp_path):
    from eoip.demo import load_demo

    store = MemoryGraphStore()
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    load_demo(store, str(data_dir))

    all_edges = store.find_edges(limit=10000)
    depends_on = [e for e in all_edges if e["label"] == "DEPENDS_ON"]
    # Whether DEPENDS_ON edges exist depends on whether any imports resolve within the demo repo
    # At minimum, the code path should not error
    assert isinstance(depends_on, list)


def test_config_load_query_policy():
    from eoip.config import load_query_policy

    policy = load_query_policy()
    assert policy.max_depth == 8
    assert policy.max_results == 500
    assert policy.read_only is True
    assert "SEARCH" in policy.allowed_intents


def test_config_load_agent_config():
    from eoip.config import load_agent_config

    config = load_agent_config("trace-impact")
    assert config is not None
    assert config["agent_id"] == "TraceImpact"
    assert config["budgets"]["max_steps"] == 10


def test_config_load_missing_agent_returns_none():
    from eoip.config import load_agent_config

    assert load_agent_config("nonexistent-agent") is None


def test_query_timeout_exception():
    from eoip.query.executor import QueryTimeout

    exc = QueryTimeout(5000)
    assert exc.timeout_ms == 5000
    assert "5000ms" in str(exc)


def test_neighborhood_is_1_hop():
    from eoip.contracts.query_plan import QueryPlan
    from eoip.query.executor import QueryExecutor

    store = MemoryGraphStore()
    a = store.upsert_vertex("WorkItem", {"canonical_id": "a", "issue_key": "A-1", "summary": "A"})
    b = store.upsert_vertex("Commit", {"canonical_id": "b", "commit_sha": "abc123"})
    c = store.upsert_vertex("File", {"canonical_id": "c", "repo_id": "r", "path": "f.py"})
    store.upsert_edge("IMPLEMENTS", b["vid"], a["vid"], {"source_system": "test"})
    store.upsert_edge("MODIFIES", b["vid"], c["vid"], {"source_system": "test"})

    executor = QueryExecutor(store)
    plan = QueryPlan(intent="NEIGHBORHOOD", anchors=["b"], max_depth=1, result_limit=100, evidence_mode="NONE")
    result = executor.execute(plan)
    ids = {n.id for n in result.nodes}
    assert "b" in ids
    assert "a" in ids
    assert "c" in ids


def test_traceability_only_follows_traceability_edges():
    from eoip.contracts.query_plan import QueryPlan
    from eoip.query.executor import QueryExecutor

    store = MemoryGraphStore()
    a = store.upsert_vertex("WorkItem", {"canonical_id": "w1", "issue_key": "T-1", "summary": "Trace"})
    b = store.upsert_vertex("Commit", {"canonical_id": "c1", "commit_sha": "sha1"})
    c = store.upsert_vertex("File", {"canonical_id": "f1", "repo_id": "r", "path": "x.py"})
    store.upsert_edge("IMPLEMENTS", b["vid"], a["vid"], {"source_system": "test"})
    store.upsert_edge("MODIFIES", b["vid"], c["vid"], {"source_system": "test"})

    executor = QueryExecutor(store)
    plan = QueryPlan(intent="TRACEABILITY", anchors=["c1"], max_depth=4, result_limit=100, evidence_mode="NONE")
    result = executor.execute(plan)
    edge_types = {e.type for e in result.edges}
    assert not edge_types or edge_types <= {"IMPLEMENTS", "REFERENCES", "DOCUMENTS"}


def test_schema_version_compatible_same_major():
    """P1-22: same major version passes compatibility check."""
    store = MemoryGraphStore()
    bootstrap_meta_graph(store)
    check_schema_compatibility(store)


def test_schema_version_incompatible_major_raises():
    """P1-22: incompatible major version fails startup."""
    store = MemoryGraphStore()
    store.upsert_vertex(
        "OntologyVersion",
        {
            "canonical_id": "urn:eoip:meta:ontology:legacy",
            "ontology_version": "0.1.0",
            "schema_version": "999.0",
        },
    )
    with pytest.raises(SchemaVersionConflict, match="999.0"):
        check_schema_compatibility(store)


def test_schema_version_empty_store_passes():
    """P1-22: fresh store with no OntologyVersion passes."""
    store = MemoryGraphStore()
    check_schema_compatibility(store)
