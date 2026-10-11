import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.vector_graph import (
    HNSWConfig,
    HNSWIndex,
    UnifiedVectorGraphPlanner,
    VectorEntry,
)


@pytest.mark.req("KGR-G-016")
def test_hnsw_index_insert_and_search():
    index = HNSWIndex(HNSWConfig(max_connections=8, ef_construction=50, ef_search=20))
    # Insert 4 3-dimensional vectors
    v1 = VectorEntry(canonical_id="doc:payments", vector=(1.0, 0.0, 0.0), metadata={"domain": "payments"})
    v2 = VectorEntry(canonical_id="doc:billing", vector=(0.9, 0.1, 0.0), metadata={"domain": "billing"})
    v3 = VectorEntry(canonical_id="doc:auth", vector=(0.0, 1.0, 0.0), metadata={"domain": "auth"})
    v4 = VectorEntry(canonical_id="doc:identity", vector=(0.1, 0.9, 0.0), metadata={"domain": "identity"})

    for v in [v1, v2, v3, v4]:
        index.insert(v)

    assert index.size == 4
    # Query vector close to payments/billing
    results = index.search((0.95, 0.05, 0.0), k=2)
    assert len(results) == 2
    top_id, top_score = results[0]
    assert top_id in {"doc:payments", "doc:billing"}
    assert top_score > 0.9


@pytest.mark.req("KGR-G-016")
def test_hnsw_index_removal():
    index = HNSWIndex()
    v1 = VectorEntry(canonical_id="node:1", vector=(1.0, 0.0))
    v2 = VectorEntry(canonical_id="node:2", vector=(0.0, 1.0))
    index.insert(v1)
    index.insert(v2)
    assert index.size == 2

    assert index.remove("node:1") is True
    assert index.size == 1
    assert index.get("node:1") is None
    assert index.remove("nonexistent") is False


@pytest.mark.req("KGR-G-016")
def test_unified_vector_then_traverse_colocated():
    store = MemoryGraphStore()
    index = HNSWIndex()

    # Create vertices in graph store
    s1 = store.upsert_vertex("Service", {"canonical_id": "svc:checkout", "name": "Checkout"})
    s2 = store.upsert_vertex("Service", {"canonical_id": "svc:payment", "name": "Payment Gateway"})
    s3 = store.upsert_vertex("Service", {"canonical_id": "svc:notify", "name": "Notification"})

    # Add edges: checkout -> payment -> notify
    store.upsert_edge("CALLS", s1["vid"], s2["vid"], {})
    store.upsert_edge("CALLS", s2["vid"], s3["vid"], {})

    # Index vector representations
    index.insert(VectorEntry("svc:checkout", (0.9, 0.1, 0.0)))
    index.insert(VectorEntry("svc:payment", (0.8, 0.2, 0.0)))
    index.insert(VectorEntry("svc:notify", (0.1, 0.9, 0.0)))

    planner = UnifiedVectorGraphPlanner(store, index)

    # Vector-then-traverse: find nearest vector to checkout, traverse 2 hops
    results = planner.vector_then_traverse((0.95, 0.05, 0.0), top_k=1, max_hops=2)
    assert len(results) == 1
    assert results[0].canonical_id == "svc:checkout"
    ctx = results[0].graph_context
    assert ctx is not None
    neighbor_ids = {n["id"] for n in ctx["neighbors"]}
    assert "svc:payment" in neighbor_ids


@pytest.mark.req("KGR-G-016")
def test_unified_graph_then_vector_colocated():
    store = MemoryGraphStore()
    index = HNSWIndex()

    s1 = store.upsert_vertex("Service", {"canonical_id": "svc:core", "name": "Core"})
    s2 = store.upsert_vertex("Service", {"canonical_id": "svc:auth", "name": "Auth"})
    s3 = store.upsert_vertex("Service", {"canonical_id": "svc:billing", "name": "Billing"})
    store.upsert_edge("CALLS", s1["vid"], s2["vid"], {})
    store.upsert_edge("CALLS", s1["vid"], s3["vid"], {})

    index.insert(VectorEntry("svc:auth", (0.0, 1.0)))
    index.insert(VectorEntry("svc:billing", (1.0, 0.0)))

    planner = UnifiedVectorGraphPlanner(store, index)
    # Start at svc:core, find called services, rank by vector similarity to billing
    results = planner.graph_then_vector("svc:core", (0.95, 0.05), top_k=2)
    assert len(results) >= 1
    assert results[0].canonical_id == "svc:billing"
