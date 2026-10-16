"""Contract tests: GraphStore protocol compliance (NFR-MAINT-001).

Both MemoryGraphStore and HugeGraphStore must satisfy the GraphStore protocol.
"""

from eoip.graph.memory import MemoryGraphStore


def test_memory_store_vertex_lifecycle():
    store = MemoryGraphStore()
    vertex = store.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test"})
    assert vertex["canonical_id"] == "urn:test:item:1"
    assert vertex["label"] == "WorkItem"

    found = store.get_vertex_by_canonical_id("urn:test:item:1")
    assert found is not None
    assert found["canonical_id"] == vertex["canonical_id"]

    updated = store.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Updated"})
    assert updated["vid"] == vertex["vid"]
    assert updated["properties"]["summary"] == "Updated"

    assert store.count_vertices("WorkItem") == 1
    assert store.count_vertices() >= 1


def test_memory_store_edge_lifecycle():
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("Project", {"canonical_id": "urn:test:project:1", "name": "P1"})
    v2 = store.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test"})

    edge = store.upsert_edge("CONTAINS", v1["vid"], v2["vid"], {"fact_key": "test-edge", "creation_status": "DETERMINISTIC"})
    assert edge["label"] == "CONTAINS"
    assert edge["out_v"] == v1["vid"]
    assert edge["in_v"] == v2["vid"]

    outgoing = store.edges_from(v1["vid"])
    assert len(outgoing) == 1
    assert outgoing[0]["eid"] == edge["eid"]

    incoming = store.edges_to(v2["vid"])
    assert len(incoming) == 1
    assert incoming[0]["eid"] == edge["eid"]


def test_memory_store_tombstone():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:test:item:tomb", "issue_key": "T-1", "summary": "To delete"})
    assert store.tombstone_vertex("urn:test:item:tomb")
    v = store.get_vertex_by_canonical_id("urn:test:item:tomb")
    assert v["properties"].get("deleted_at") is not None


def test_memory_store_clear():
    store = MemoryGraphStore()
    store.upsert_vertex("Project", {"canonical_id": "urn:test:clear:1", "name": "Clear"})
    assert store.count_vertices() > 0
    store.clear()
    assert store.count_vertices() == 0
    assert store.count_edges() == 0


def test_memory_store_health():
    store = MemoryGraphStore()
    assert store.health()
