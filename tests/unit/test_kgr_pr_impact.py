"""Phase 10 tests: PR/change impact dashboard, conflict detection, file viewer."""

import os

from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app


def _build_pr_graph(store):
    pr1_commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:commit:pr1-a", "commit_sha": "aaa",
        "merge_request_id": "101", "pr_title": "Add auth", "pr_author": "alice",
    })
    pr1_file = store.upsert_vertex("File", {
        "canonical_id": "urn:file:auth", "repo_id": "r1", "path": "src/auth.py",
        "merge_request_id": "101",
    })
    pr2_commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:commit:pr2-a", "commit_sha": "bbb",
        "merge_request_id": "102", "pr_title": "Fix auth", "pr_author": "bob",
    })
    pr2_file = store.upsert_vertex("File", {
        "canonical_id": "urn:file:auth-fix", "repo_id": "r1", "path": "src/auth_fix.py",
        "merge_request_id": "102",
    })
    store.upsert_edge("MODIFIES", pr1_commit["vid"], pr1_file["vid"], {})
    store.upsert_edge("MODIFIES", pr2_commit["vid"], pr2_file["vid"], {})
    store.upsert_edge("DEPENDS_ON", pr2_file["vid"], pr1_file["vid"], {})
    return store


# --- PR Impact API ---

def test_pr_impact_endpoint():
    store = _build_pr_graph(store=MemoryGraphStore())
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/pr-impact")
    assert resp.status_code == 200
    data = resp.json()
    assert "pull_requests" in data
    assert "conflicts" in data
    assert isinstance(data["pull_requests"], list)
    assert isinstance(data["conflicts"], list)


def test_pr_impact_lists_prs():
    store = _build_pr_graph(store=MemoryGraphStore())
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/pr-impact")
    data = resp.json()
    mr_ids = [pr["mr_id"] for pr in data["pull_requests"]]
    assert "101" in mr_ids or "102" in mr_ids


def test_pr_impact_empty_graph():
    store = MemoryGraphStore()
    client = TestClient(create_app(store))
    resp = client.get("/api/v1/graph/pr-impact")
    assert resp.status_code == 200
    assert resp.json()["pull_requests"] == []


# --- File viewer API ---

def test_file_viewer_endpoint(tmp_path, monkeypatch):
    (tmp_path / "sample.txt").write_text("hello\nworld\n", encoding="utf-8")
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    client = TestClient(create_app(MemoryGraphStore()))
    resp = client.get("/api/v1/files/sample.txt")
    assert resp.status_code == 200
    data = resp.json()
    assert "content" in data
    assert "lines" in data
    assert data["lines"] > 0


def test_file_viewer_not_found():
    client = TestClient(create_app(MemoryGraphStore()))
    resp = client.get("/api/v1/files/nonexistent/path.py")
    assert resp.status_code == 404


def test_file_viewer_blocks_path_traversal():
    client = TestClient(create_app(MemoryGraphStore()))
    resp = client.get("/api/v1/files/foo/../../etc/passwd")
    assert resp.status_code in (400, 404)


# --- Frontend components exist ---

def test_pr_dashboard_jsx_exists():
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "PRDashboard.jsx"))


def test_code_panel_jsx_exists():
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "CodePanel.jsx"))


def test_query_builder_jsx_exists():
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "QueryBuilder.jsx"))


def test_geo_map_jsx_exists():
    assert os.path.exists(os.path.join("apps", "web", "src", "kgr", "components", "GeoMap.jsx"))
