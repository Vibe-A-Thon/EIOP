"""Phase 12 graph surprise detection tests."""

from unittest.mock import patch

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.surprise import SurpriseDetector
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _props(cid: str, name: str | None = None) -> dict:
    return {"canonical_id": cid, "name": name or cid.rsplit(":", 1)[-1]}


def _build_surprise_graph(store: MemoryGraphStore) -> None:
    for label, cid in [
        ("Service", "urn:svc:checkout"),
        ("Service", "urn:svc:payment"),
        ("WorkItem", "urn:story:pay-142"),
        ("Commit", "urn:commit:a1"),
        ("Document", "urn:doc:runbook"),
        ("File", "urn:file:checkout"),
        ("CodeSymbol", "urn:symbol:checkout.handler"),
        ("CodeSymbol", "urn:symbol:payment.client"),
    ]:
        store.upsert_vertex(label, _props(cid))

    store.upsert_edge("DEPENDS_ON", "urn:svc:checkout", "urn:svc:payment", {})
    store.upsert_edge("IMPLEMENTS", "urn:commit:a1", "urn:story:pay-142", {})
    store.upsert_edge("MODIFIES", "urn:commit:a1", "urn:file:checkout", {})
    store.upsert_edge("REFERENCES", "urn:story:pay-142", "urn:file:checkout", {})
    store.upsert_edge("DECLARES", "urn:file:checkout", "urn:symbol:checkout.handler", {})
    store.upsert_edge("CALLS", "urn:symbol:checkout.handler", "urn:symbol:payment.client", {})
    store.upsert_edge("DOCUMENTS", "urn:doc:runbook", "urn:svc:checkout", {})
    store.upsert_edge("DOCUMENTS", "urn:doc:runbook", "urn:svc:payment", {})
    store.upsert_edge("REFERENCES", "urn:doc:runbook", "urn:story:pay-142", {})
    store.upsert_edge("DEPENDS_ON", "urn:file:checkout", "urn:svc:checkout", {})
    store.upsert_edge("DEPENDS_ON", "urn:symbol:payment.client", "urn:svc:payment", {})


def test_surprising_edges_prioritizes_cross_domain_bridges():
    store = MemoryGraphStore()
    _build_surprise_graph(store)

    results = SurpriseDetector(store).surprising_edges(limit=10)

    assert results
    assert all(result.kind == "surprising_edge" for result in results)
    assert any(result.source_label != result.target_label for result in results)
    assert results == sorted(results, key=lambda result: (-result.score, result.source_id or "", result.target_id or ""))


def test_unexpected_absences_find_high_similarity_missing_edges():
    store = MemoryGraphStore()
    _build_surprise_graph(store)

    results = SurpriseDetector(store).unexpected_absences(limit=10)
    pairs = {(result.source_id, result.target_id) for result in results}

    assert results
    assert ("urn:story:pay-142", "urn:svc:checkout") in pairs or (
        "urn:svc:checkout",
        "urn:story:pay-142",
    ) in pairs
    assert all(result.kind == "unexpected_absence" for result in results)


def test_surprise_summary_has_counts_and_serializable_results():
    store = MemoryGraphStore()
    _build_surprise_graph(store)

    summary = SurpriseDetector(store).summary(limit=5)

    assert set(summary) == {"surprising_edges", "unexpected_absences", "counts"}
    assert summary["counts"]["surprising_edges"] == len(summary["surprising_edges"])
    assert summary["counts"]["unexpected_absences"] == len(summary["unexpected_absences"])
    assert "score" in summary["surprising_edges"][0]


def test_api_graph_surprises_returns_ranked_sections():
    store = MemoryGraphStore()
    _build_surprise_graph(store)
    client = TestClient(create_app(store))

    response = client.post("/api/v1/graph/surprises", json={"limit": 5})

    assert response.status_code == 200
    body = response.json()
    assert body["counts"]["surprising_edges"] <= 5
    assert body["surprising_edges"]
    assert body["unexpected_absences"]


def test_unexpected_absences_do_not_rescan_entire_graph_for_each_source():
    store = MemoryGraphStore()
    _build_surprise_graph(store)
    vertex_count = len(store.find_vertices(limit=100))
    with patch.object(store, "edges_from", wraps=store.edges_from) as edge_reads:
        results = SurpriseDetector(store).unexpected_absences(limit=10)
    assert results
    assert edge_reads.call_count <= 2 * vertex_count
