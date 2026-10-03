"""Phase 8 tests: what-if simulation — removal, isolation, component split + API."""

from eoip.graph.memory import MemoryGraphStore
from eoip.graph.whatif import WhatIfEngine


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_chain(store):
    """A -> B -> C -> D."""
    for cid in ["urn:a", "urn:b", "urn:c", "urn:d"]:
        store.upsert_vertex("File", _file_props(cid))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:b", "urn:c", {})
    store.upsert_edge("DEPENDS_ON", "urn:c", "urn:d", {})


def _build_hub(store):
    """Hub connected to 3 spokes with no inter-spoke edges."""
    store.upsert_vertex("File", _file_props("urn:hub"))
    for i in range(3):
        store.upsert_vertex("File", _file_props(f"urn:spoke-{i}"))
        store.upsert_edge("DEPENDS_ON", "urn:hub", f"urn:spoke-{i}", {})


# --- What-if removal ---

def test_remove_chain_middle():
    store = MemoryGraphStore()
    _build_chain(store)
    engine = WhatIfEngine(store)
    result = engine.simulate_removal("urn:b")
    assert result.action == "remove"
    assert result.broken_edges == 2
    assert result.affected_neighbors >= 2


def test_remove_hub_orphans_spokes():
    store = MemoryGraphStore()
    _build_hub(store)
    engine = WhatIfEngine(store)
    result = engine.simulate_removal("urn:hub")
    assert result.broken_edges == 3
    assert result.orphaned_entities == 3


def test_remove_nonexistent():
    store = MemoryGraphStore()
    engine = WhatIfEngine(store)
    result = engine.simulate_removal("urn:missing")
    assert result.broken_edges == 0
    assert result.affected_neighbors == 0


def test_remove_detects_component_split():
    store = MemoryGraphStore()
    _build_chain(store)
    engine = WhatIfEngine(store)
    result = engine.simulate_removal("urn:b")
    assert result.component_split is True


# --- What-if isolation ---

def test_isolate_hub():
    store = MemoryGraphStore()
    _build_hub(store)
    engine = WhatIfEngine(store)
    result = engine.simulate_isolation("urn:hub")
    assert result.action == "isolate"
    assert result.broken_edges == 3
    assert result.affected_neighbors == 3


def test_isolate_nonexistent():
    store = MemoryGraphStore()
    engine = WhatIfEngine(store)
    result = engine.simulate_isolation("urn:missing")
    assert result.broken_edges == 0


# --- API ---

def test_api_whatif_removal():
    from apps.api.app import create_app
    from fastapi.testclient import TestClient
    store = MemoryGraphStore()
    _build_hub(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/what-if", json={"canonical_id": "urn:hub", "action": "remove"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["broken_edges"] == 3


def test_api_whatif_isolate():
    from apps.api.app import create_app
    from fastapi.testclient import TestClient
    store = MemoryGraphStore()
    _build_hub(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/what-if", json={"canonical_id": "urn:hub", "action": "isolate"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["affected_neighbors"] == 3
