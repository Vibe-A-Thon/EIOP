"""Phase 4 tests: 10-dimensional filter state management and filter-related API behaviour."""

from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_diverse_graph(store):
    store.upsert_vertex("File", _file_props("urn:f1"))
    store.upsert_vertex("File", _file_props("urn:f2"))
    store.upsert_vertex("WorkItem", {"canonical_id": "urn:w1", "issue_key": "PROJ-1"})
    store.upsert_vertex("Commit", {"canonical_id": "urn:c1", "commit_sha": "abc123"})
    store.upsert_edge("DEPENDS_ON", "urn:f1", "urn:f2", {})
    store.upsert_edge("IMPLEMENTS", "urn:c1", "urn:w1", {})
    store.upsert_edge("MODIFIES", "urn:c1", "urn:f1", {})


# --- Filter dimensions in KGRExplorer ---

def test_default_filters_has_10_dimensions():
    """defaultFilters object should have 10 filter dimensions."""
    import os
    path = os.path.join("apps", "web", "src", "kgr", "KGRExplorer.jsx")
    if not os.path.exists(path):
        return
    with open(path) as f:
        content = f.read()
    assert "domain:" in content
    assert "label:" in content
    assert "edgeType:" in content
    assert "trust:" in content
    assert "evidence:" in content
    assert "source:" in content
    assert "minDegree:" in content
    assert "searchText:" in content
    assert "temporal:" in content
    assert "community:" in content


def test_filter_chips_include_temporal():
    import os
    path = os.path.join("apps", "web", "src", "kgr", "KGRExplorer.jsx")
    if not os.path.exists(path):
        return
    with open(path) as f:
        content = f.read()
    assert "filters.temporal" in content


def test_filter_chips_include_community():
    import os
    path = os.path.join("apps", "web", "src", "kgr", "KGRExplorer.jsx")
    if not os.path.exists(path):
        return
    with open(path) as f:
        content = f.read()
    assert "filters.community" in content


# --- API endpoints support filtering data ---

def test_schema_provides_filter_metadata():
    store = MemoryGraphStore()
    _build_diverse_graph(store)
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/schema")
    assert resp.status_code == 200
    data = resp.json()
    assert "vertex_labels" in data
    assert len(data["vertex_labels"]) >= 2


def test_statistics_provides_counts():
    store = MemoryGraphStore()
    _build_diverse_graph(store)
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/statistics")
    assert resp.status_code == 200
    data = resp.json()
    assert data["vertex_count"] >= 3
    assert data["edge_count"] >= 2


def test_cluster_provides_community_data():
    store = MemoryGraphStore()
    _build_diverse_graph(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/cluster", json={"algorithm": "label_propagation"})
    assert resp.status_code == 200
    data = resp.json()
    assert "communities" in data
    assert "modularity" in data


# --- Keyboard nav presence ---

def test_keyboard_shortcuts_defined():
    import os
    path = os.path.join("apps", "web", "src", "kgr", "KGRExplorer.jsx")
    if not os.path.exists(path):
        return
    with open(path) as f:
        content = f.read()
    assert "Escape" in content
    assert "handleUndo" in content
    assert "handleRedo" in content
    assert "setShowFilters" in content


# --- Context menu presence ---

def test_context_menu_component_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "ContextMenu.jsx"))


def test_exploration_history_component_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "ExplorationHistory.jsx"))


def test_bookmarks_component_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "GraphBookmarks.jsx"))
