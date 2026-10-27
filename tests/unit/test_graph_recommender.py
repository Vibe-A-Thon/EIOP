import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.recommend import GraphRecommender, Recommendation


@pytest.fixture
def graph():
    store = MemoryGraphStore()
    # Vertices
    s1 = store.upsert_vertex("Service", {"canonical_id": "svc:orders", "service_id": "orders", "name": "Orders Service"})
    s2 = store.upsert_vertex("Service", {"canonical_id": "svc:payments", "service_id": "payments", "name": "Payments Service"})
    d1 = store.upsert_vertex("Document", {"canonical_id": "doc:orders-runbook", "name": "Orders Runbook", "path": "/docs/orders.md"})
    d2 = store.upsert_vertex("Document", {"canonical_id": "doc:payments-spec", "name": "Payments Architecture", "path": "/docs/payments.md"})
    p1 = store.upsert_vertex("Person", {"canonical_id": "usr:alice", "display_name": "Alice Smith"})
    store.upsert_vertex("Person", {"canonical_id": "usr:bob", "display_name": "Bob Jones"})
    w1 = store.upsert_vertex("WorkItem", {"canonical_id": "task:101", "issue_key": "ORD-101", "summary": "Fix checkout bug"})
    store.upsert_vertex("Tag", {"canonical_id": "tag:checkout", "repo_id": "repo-1", "tag_name": "checkout"})

    # Edges
    store.upsert_edge("DOCUMENTS", d1["vid"], s1["vid"], {})
    store.upsert_edge("DOCUMENTS", d2["vid"], s2["vid"], {})
    store.upsert_edge("CALLS", s1["vid"], s2["vid"], {})
    store.upsert_edge("ASSIGNED_TO", w1["vid"], p1["vid"], {})
    store.upsert_edge("REFERENCES", d1["vid"], w1["vid"], {})

    return store


@pytest.mark.req("GAP-REC")
def test_recommend_documents(graph):
    rec = GraphRecommender(graph)
    # Directly linked is doc:orders-runbook, but include_linked=False excludes direct neighbors
    docs = rec.recommend_documents("svc:orders", include_linked=True)
    assert any(d.canonical_id == "doc:orders-runbook" for d in docs)
    # 2-hop document: svc:orders -> CALLS -> svc:payments <- DOCUMENTS <- doc:payments-spec
    docs_indirect = rec.recommend_documents("svc:orders", include_linked=False)
    assert any(d.canonical_id == "doc:payments-spec" for d in docs_indirect)


@pytest.mark.req("GAP-REC")
def test_recommend_experts(graph):
    rec = GraphRecommender(graph)
    # Path: svc:orders <- DOCUMENTS <- doc:orders-runbook -> REFERENCES -> task:101 -> ASSIGNED_TO -> usr:alice
    experts = rec.recommend_experts("svc:orders")
    assert len(experts) > 0
    top = experts[0]
    assert top.canonical_id == "usr:alice"
    assert top.distance is not None
    assert "usr:alice" in top.path


@pytest.mark.req("GAP-REC")
def test_recommend_components_and_all(graph):
    rec = GraphRecommender(graph)
    comps = rec.recommend_components("svc:orders", include_linked=True)
    assert any(c.canonical_id == "svc:payments" for c in comps)

    all_recs = rec.recommend_all("svc:orders")
    assert "documents" in all_recs
    assert "experts" in all_recs
    assert "components" in all_recs
    assert "concepts" in all_recs


@pytest.mark.req("GAP-REC")
def test_recommend_errors_and_boundaries(graph):
    rec = GraphRecommender(graph)
    with pytest.raises(KeyError):
        rec.recommend("nonexistent:id", "documents")
    with pytest.raises(ValueError):
        rec.recommend("svc:orders", "invalid_kind")
    with pytest.raises(ValueError):
        rec.recommend("svc:orders", "documents", limit=0)
    with pytest.raises(ValueError):
        GraphRecommender(graph, restart=1.5)
