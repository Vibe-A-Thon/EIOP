"""Expert finder and documentation freshness (GAP-REC-001, GAP-FRESH-001..005)."""

from datetime import UTC, datetime, timedelta

from eoip.graph.expertise import find_experts, freshness_report
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _iso(days_ago: float) -> str:
    return (
        datetime.now(UTC) - timedelta(days=days_ago)
    ).isoformat().replace("+00:00", "Z")


def _graph():
    store = MemoryGraphStore()
    store.ensure_schema({})
    person = store.upsert_vertex(
        "Person", {"canonical_id": "urn:person:murthy", "display_name": "Murthy Reddy"}
    )
    commit = store.upsert_vertex(
        "Commit",
        {
            "canonical_id": "urn:commit:1",
            "commit_sha": "abc123",
            "created_at": _iso(10),
        },
    )
    file_v = store.upsert_vertex(
        "File", {"canonical_id": "urn:file:svc", "repo_id": "demo", "path": "service.py"}
    )
    store.upsert_edge("AUTHORED_BY", commit["vid"], person["vid"], {"fact_key": "a:1"})
    store.upsert_edge("MODIFIES", commit["vid"], file_v["vid"], {"fact_key": "m:1"})
    return store


def test_expert_ranked_from_authorship_evidence():
    store = _graph()
    result = find_experts(store, "urn:file:svc")
    assert result["experts"][0]["person_cid"] == "urn:person:murthy"
    assert result["experts"][0]["score"] > 0
    assert result["experts"][0]["evidence"][0]["basis"] == "AUTHORED_BY"


def test_experts_unknown_component_raises():
    import pytest

    with pytest.raises(ValueError, match="not found"):
        find_experts(MemoryGraphStore(), "urn:missing")


def test_freshness_flags_stale_document():
    store = MemoryGraphStore()
    store.ensure_schema({})
    symbol = store.upsert_vertex(
        "CodeSymbol",
        {
            "canonical_id": "urn:symbol:1",
            "qualified_name": "demo.compute",
            "symbol_kind": "function",
            "modified_at": _iso(5),
        },
    )
    document = store.upsert_vertex(
        "Document",
        {
            "canonical_id": "urn:doc:1",
            "name": "Checkout runbook",
            "path": "docs/runbook.md",
            "last_seen": _iso(400),
        },
    )
    store.upsert_edge(
        "REFERENCES", document["vid"], symbol["vid"], {"fact_key": "r:1", "creation_status": "DETERMINISTIC"}
    )
    report = freshness_report(store, stale_days=90)
    assert report["stale_count"] == 1
    row = report["documents"][0]
    assert row["stale"] is True
    assert "human review" in row["recommendation"]


def test_experts_and_freshness_endpoints():
    store = _graph()
    store.upsert_vertex(
        "Document",
        {
            "canonical_id": "urn:doc:1",
            "name": "Doc",
            "path": "docs/d.md",
            "last_seen": _iso(1),
        },
    )
    client = TestClient(create_app(store))
    experts = client.get("/api/v1/experts/urn:file:svc")
    assert experts.status_code == 200
    assert experts.json()["experts"][0]["person_cid"] == "urn:person:murthy"
    assert client.get("/api/v1/experts/urn:missing").status_code == 404

    freshness = client.get("/api/v1/knowledge/freshness")
    assert freshness.status_code == 200
    assert freshness.json()["stale_count"] == 0

    cache_stats = client.get("/api/v1/query/cache/stats")
    assert cache_stats.status_code == 200
    assert cache_stats.json()["enabled"] is False
