from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _vertex(store: MemoryGraphStore, label: str, canonical_id: str, **properties: str) -> dict:
    return store.upsert_vertex(label, {"canonical_id": canonical_id, "name": canonical_id, **properties})


def _demo_store() -> MemoryGraphStore:
    store = MemoryGraphStore()
    issue = _vertex(store, "WorkItem", "issue:EOIP-1", issue_key="EOIP-1", summary="Trace impact")
    commit = _vertex(store, "Commit", "commit:abc123", commit_sha="abc123")
    file = _vertex(store, "File", "file:src/service.py", path="src/service.py")
    symbol = _vertex(store, "CodeSymbol", "symbol:src/service.py:run", qualified_name="service.run")
    evidence = _vertex(
        store,
        "Evidence",
        "evidence:commit:abc123",
        source_system="git",
        source_ref="git://demo/commit/abc123",
        method="SOURCE_EVENT",
        evidence_key="evidence:commit:abc123",
    )
    run = _vertex(
        store,
        "IngestionRun",
        "run:git:abc123",
        run_kind="GIT",
        run_status="SUCCEEDED",
    )
    store.upsert_edge("IMPLEMENTS", commit["vid"], issue["vid"], {"evidence_key": "evidence:commit:abc123"})
    store.upsert_edge("MODIFIES", commit["vid"], file["vid"], {})
    store.upsert_edge("DECLARES", file["vid"], symbol["vid"], {})
    store.upsert_edge("EVIDENCED_BY", symbol["vid"], evidence["vid"], {"source_ref": "git://demo/commit/abc123"})
    store.upsert_edge("INGESTED_IN", symbol["vid"], run["vid"], {"ingestion_run_id": "abc123"})
    return store


def test_search_path_and_impact_use_graph_store_data() -> None:
    client = TestClient(create_app(_demo_store()))

    search = client.get("/api/v1/search", params={"q": "EOIP-1"})
    path = client.post(
        "/api/v1/path",
        json={"source_id": "issue:EOIP-1", "target_id": "symbol:src/service.py:run"},
    )
    impact = client.post("/api/v1/impact", json={"canonical_id": "issue:EOIP-1", "max_depth": 3})
    lineage = client.post(
        "/api/v1/lineage",
        json={"canonical_id": "symbol:src/service.py:run"},
    )

    assert search.status_code == 200
    assert search.json()["nodes"][0]["id"] == "issue:EOIP-1"
    assert path.status_code == 200
    assert [edge["type"] for edge in path.json()["edges"]] == ["IMPLEMENTS", "MODIFIES", "DECLARES"]
    assert path.json()["evidence"][0]["evidence_key"] == "evidence:commit:abc123"
    assert impact.status_code == 200
    assert len(impact.json()["paths"]) == 3
    assert lineage.status_code == 200
    assert {node["label"] for node in lineage.json()["nodes"]} == {"CodeSymbol", "Evidence", "IngestionRun"}
    assert {edge["type"] for edge in lineage.json()["edges"]} == {"EVIDENCED_BY", "INGESTED_IN"}
    assert {item["source_ref"] for item in lineage.json()["evidence"]} == {"git://demo/commit/abc123"}


def test_query_api_sets_correlation_id_and_rejects_excessive_limits() -> None:
    client = TestClient(create_app(_demo_store()))

    health = client.get("/health/live", headers={"X-Correlation-ID": "trace-123"})
    invalid = client.post(
        "/api/v1/path",
        json={"source_id": "a", "target_id": "b", "max_depth": 9},
    )
    unknown = client.post("/api/v1/lineage", json={"canonical_id": "unknown:entity"})

    assert health.headers["x-correlation-id"] == "trace-123"
    assert invalid.status_code == 422
    assert unknown.status_code == 404


def test_neighborhood_and_traceability_endpoints() -> None:
    client = TestClient(create_app(_demo_store()))

    neighborhood = client.post(
        "/api/v1/neighborhood",
        json={"canonical_id": "commit:abc123"},
    )
    traceability = client.post(
        "/api/v1/traceability",
        json={"canonical_id": "commit:abc123"},
    )

    assert neighborhood.status_code == 200
    node_ids = {n["id"] for n in neighborhood.json()["nodes"]}
    assert "commit:abc123" in node_ids

    assert traceability.status_code == 200
    edge_types = {e["type"] for e in traceability.json()["edges"]}
    assert not edge_types or edge_types <= {"IMPLEMENTS", "REFERENCES", "DOCUMENTS"}


def test_neighborhood_returns_404_for_unknown_entity() -> None:
    client = TestClient(create_app(_demo_store()))
    r = client.post("/api/v1/neighborhood", json={"canonical_id": "unknown:x"})
    assert r.status_code == 404


def test_traceability_returns_404_for_unknown_entity() -> None:
    client = TestClient(create_app(_demo_store()))
    r = client.post("/api/v1/traceability", json={"canonical_id": "unknown:x"})
    assert r.status_code == 404
