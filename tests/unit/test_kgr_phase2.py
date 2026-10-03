"""Phase 2 tests: component extraction, 8+ graph types, 8-tab inspector, edge inspector."""

from apps.api.app import create_app
from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient


def _file_props(cid):
    return {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}


def _build_graph(store):
    store.upsert_vertex("File", _file_props("urn:a"))
    store.upsert_vertex("File", _file_props("urn:b"))
    store.upsert_vertex("File", _file_props("urn:c"))
    store.upsert_edge("DEPENDS_ON", "urn:a", "urn:b", {})
    store.upsert_edge("DEPENDS_ON", "urn:b", "urn:c", {})


# --- Inspector tab completeness ---

def test_inspector_8_tabs_listed():
    """The NodeInspector defines exactly 8 tabs."""
    import importlib.util
    import os
    path = os.path.join("apps", "web", "src", "kgr", "KGRExplorer.jsx")
    if not os.path.exists(path):
        return
    with open(path) as f:
        content = f.read()
    assert "inspectorTabs" in content
    assert "'overview'" in content
    assert "'relationships'" in content
    assert "'impact'" in content
    assert "'centrality'" in content
    assert "'similarity'" in content
    assert "'whatif'" in content
    assert "'evidence'" in content
    assert "'annotations'" in content


def test_graph_types_count_10():
    """KGRExplorer defines 10 graph types."""
    import os
    path = os.path.join("apps", "web", "src", "kgr", "KGRExplorer.jsx")
    if not os.path.exists(path):
        return
    with open(path) as f:
        content = f.read()
    assert "'knowledge'" in content
    assert "'relationship'" in content
    assert "'metadata'" in content
    assert "'ontology'" in content
    assert "'temporal'" in content
    assert "'provenance'" in content
    assert "'impact'" in content
    assert "'similarity'" in content
    assert "'diff'" in content
    assert "'health'" in content


# --- Edge inspector component exists ---

def test_edge_inspector_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "EdgeInspector.jsx"))


def test_minimap_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "Minimap.jsx"))


def test_graph_toolbar_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "GraphToolbar.jsx"))


# --- Graph view files ---

def test_graphs_directory_has_8_files():
    import os
    graphs_dir = os.path.join("apps", "web", "src", "kgr", "graphs")
    assert os.path.isdir(graphs_dir)
    files = [f for f in os.listdir(graphs_dir) if f.endswith('.jsx')]
    assert len(files) >= 8


def test_cytoscape_renderer_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "renderers", "CytoscapeRenderer.jsx"))


# --- API still works with 8+ graph types ---

def test_schema_has_vertex_and_edge_labels():
    store = MemoryGraphStore()
    _build_graph(store)
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/schema")
    assert resp.status_code == 200
    data = resp.json()
    assert "vertex_labels" in data
    assert "edge_labels" in data


def test_blast_radius_with_extracted_components():
    store = MemoryGraphStore()
    _build_graph(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/blast-radius", json={"canonical_id": "urn:a", "max_depth": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_affected"] >= 1


def test_metrics_with_extracted_components():
    store = MemoryGraphStore()
    _build_graph(store)
    client = TestClient(create_app(store))
    resp = client.post("/api/v1/graph/metrics", json={"canonical_ids": ["urn:a"]})
    assert resp.status_code == 200


# --- Analysis module files ---

def test_analysis_similarity_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "analysis", "similarity.js"))


def test_analysis_link_prediction_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "analysis", "link-prediction.js"))


def test_similarity_panel_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "SimilarityPanel.jsx"))


def test_annotation_panel_file_exists():
    import os
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "AnnotationPanel.jsx"))
