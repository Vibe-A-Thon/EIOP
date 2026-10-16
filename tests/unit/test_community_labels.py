"""Tests for community auto-labeling and detect_with_labels."""

from eoip.graph.community import CommunityDetectionEngine
from eoip.graph.memory import MemoryGraphStore


def _file_props(cid, name=None):
    props = {"canonical_id": cid, "repo_id": "repo-1", "path": f"src/{cid.split(':')[-1]}.py"}
    if name:
        props["name"] = name
    return props


def test_label_community_uses_vertex_labels():
    store = MemoryGraphStore()
    for i in range(5):
        store.upsert_vertex("File", _file_props(f"urn:f-{i}"))
    for i in range(3):
        store.upsert_vertex("Commit", {"canonical_id": f"urn:c-{i}", "commit_sha": f"sha{i}"})

    engine = CommunityDetectionEngine(store)
    members = [f"urn:f-{i}" for i in range(5)] + [f"urn:c-{i}" for i in range(3)]
    label = engine.label_community(members)
    assert "File" in label
    assert "Commit" in label


def test_label_community_includes_name_parts():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:auth-1", name="auth-service"))
    store.upsert_vertex("File", _file_props("urn:auth-2", name="auth-handler"))
    store.upsert_vertex("File", _file_props("urn:auth-3", name="auth-middleware"))

    engine = CommunityDetectionEngine(store)
    label = engine.label_community(["urn:auth-1", "urn:auth-2", "urn:auth-3"])
    assert "File" in label
    assert "auth" in label


def test_label_community_handles_missing_vertices():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:exists"))

    engine = CommunityDetectionEngine(store)
    label = engine.label_community(["urn:exists", "urn:gone-1", "urn:gone-2"])
    assert "File" in label


def test_label_community_returns_unknown_for_empty():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    label = engine.label_community([])
    assert label == "Unknown"


def test_label_community_all_missing_returns_unknown():
    store = MemoryGraphStore()
    engine = CommunityDetectionEngine(store)
    label = engine.label_community(["urn:nonexistent-1", "urn:nonexistent-2"])
    assert label == "Unknown"


def test_detect_with_labels_adds_auto_label():
    store = MemoryGraphStore()
    for i in range(4):
        store.upsert_vertex("File", _file_props(f"urn:a-{i}"))
    for i in range(4):
        for j in range(i + 1, 4):
            store.upsert_edge("DEPENDS_ON", f"urn:a-{i}", f"urn:a-{j}", {})

    engine = CommunityDetectionEngine(store)
    result = engine.detect_with_labels(algorithm="label_propagation")
    assert result.community_count >= 1
    for comm in result.communities:
        assert "auto_label" in comm
        assert isinstance(comm["auto_label"], str)
        assert len(comm["auto_label"]) > 0


def test_detect_with_labels_louvain():
    store = MemoryGraphStore()
    for i in range(4):
        store.upsert_vertex("File", _file_props(f"urn:lv-{i}"))
    for i in range(4):
        for j in range(i + 1, 4):
            store.upsert_edge("DEPENDS_ON", f"urn:lv-{i}", f"urn:lv-{j}", {})

    engine = CommunityDetectionEngine(store)
    result = engine.detect_with_labels(algorithm="louvain")
    assert result.community_count >= 1
    for comm in result.communities:
        assert "auto_label" in comm


def test_label_community_short_words_ignored():
    store = MemoryGraphStore()
    store.upsert_vertex("File", _file_props("urn:ab-1", name="a-b"))
    engine = CommunityDetectionEngine(store)
    label = engine.label_community(["urn:ab-1"])
    assert "File" in label
