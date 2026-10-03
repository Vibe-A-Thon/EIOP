import json

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.jobs import JobQueue
from eoip.snapshot import backup, digest, restore


def graph():
    store = MemoryGraphStore()
    issue = store.upsert_vertex(
        "WorkItem", {"canonical_id": "issue:1", "issue_key": "EOIP-1", "summary": "Trace"}
    )
    commit = store.upsert_vertex("Commit", {"canonical_id": "commit:1", "commit_sha": "abc"})
    store.upsert_edge(
        "IMPLEMENTS", commit["vid"], issue["vid"], {"source_ref": "git://demo/abc", "evidence_key": "event:1"}
    )
    return store


def test_snapshot_restores_graph_relationships_and_evidence(tmp_path):
    source = graph()
    raw = tmp_path / "raw/jira/event.json"
    raw.parent.mkdir(parents=True)
    raw.write_text('{"event_id": "event:1"}')
    backup(source, tmp_path, tmp_path / "snapshot.json")
    target = MemoryGraphStore()
    result = restore(target, tmp_path / "restored", tmp_path / "snapshot.json")
    assert result == {"vertices": 2, "edges": 1, "raw_files": 1}
    assert target.find_edges()[0]["properties"]["evidence_key"] == "event:1"
    assert json.loads((tmp_path / "restored/raw/jira/event.json").read_text())["event_id"] == "event:1"


def test_corrupted_snapshot_rejected_before_mutation(tmp_path):
    backup(graph(), tmp_path, tmp_path / "snapshot.json")
    archive = json.loads((tmp_path / "snapshot.json").read_text())
    archive["payload"]["vertices"][0]["properties"]["summary"] = "changed"
    (tmp_path / "snapshot.json").write_text(json.dumps(archive))
    target = MemoryGraphStore()
    with pytest.raises(ValueError, match="checksum"):
        restore(target, tmp_path, tmp_path / "snapshot.json")
    assert target.count_vertices() == 0


def test_restore_rejects_path_traversal_and_nonempty_graph(tmp_path):
    backup(graph(), tmp_path, tmp_path / "snapshot.json")
    with pytest.raises(ValueError, match="empty graph"):
        restore(graph(), tmp_path, tmp_path / "snapshot.json")
    archive = json.loads((tmp_path / "snapshot.json").read_text())
    archive["payload"]["raw_files"] = {"raw/../../escape.json": {}}
    archive["sha256"] = digest(archive["payload"])
    (tmp_path / "snapshot.json").write_text(json.dumps(archive))
    target = MemoryGraphStore()
    with pytest.raises(ValueError, match="evidence path"):
        restore(target, tmp_path, tmp_path / "snapshot.json")
    assert target.count_vertices() == 0


def test_queue_is_persistent_and_rejects_invalid_job_ids(tmp_path):
    job = JobQueue(tmp_path).submit("JIRA_JSON", {"document": {"issues": []}})
    fresh = JobQueue(tmp_path)
    assert fresh.get(job["job_id"])["payload"]["document"] == {"issues": []}
    assert fresh.list()[0]["status"] == "PENDING"
    assert "payload" not in fresh.list()[0]
    with pytest.raises(ValueError):
        fresh.get("../../outside")


@pytest.mark.req("G2-T0224", "G2-T0225", "NFR-REL-003")
def test_snapshot_preserves_tombstones_and_expired_relationships(tmp_path):
    source = graph()
    issue = source.get_vertex_by_canonical_id("issue:1")
    source.upsert_vertex("WorkItem", {
        **issue["properties"], "deleted_at": "2026-10-02T00:00:00Z",
    })
    edge = source.find_edges()[0]
    source.upsert_edge("IMPLEMENTS", edge["out_v"], edge["in_v"], {
        **edge["properties"], "is_current": False, "valid_to": "2026-10-02T00:00:00Z",
    })
    snapshot = tmp_path / "snapshot.json"
    result = backup(source, tmp_path / "source", snapshot)
    assert (result["vertices"], result["edges"]) == (2, 1)
    target = MemoryGraphStore()
    restore(target, tmp_path / "restored", snapshot)
    assert target.get_vertex_by_canonical_id("issue:1")["properties"]["deleted_at"]
    assert target.find_edges() == []
    assert target.find_edges(include_historical=True)[0]["properties"]["valid_to"] == "2026-10-02T00:00:00Z"


@pytest.mark.req("NFR-REL-003")
def test_restore_refuses_graph_containing_only_tombstones(tmp_path):
    snapshot = tmp_path / "snapshot.json"
    backup(graph(), tmp_path / "source", snapshot)
    target = MemoryGraphStore()
    target.upsert_vertex("WorkItem", {
        "canonical_id": "deleted:1", "issue_key": "EOIP-0", "summary": "Deleted",
        "deleted_at": "2026-10-02T00:00:00Z",
    })
    assert target.count_vertices() == 0
    with pytest.raises(ValueError, match="empty graph"):
        restore(target, tmp_path / "restored", snapshot)
    assert target.get_vertex_by_canonical_id("issue:1") is None
