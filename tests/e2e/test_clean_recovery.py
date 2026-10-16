import json
import shutil
import subprocess
from pathlib import Path

import pytest
from eoip.graph.memory import MemoryGraphStore
from eoip.snapshot import backup, restore

from scripts.verify_clean_demo import verify_clean_demo, verify_temporal_edge_upgrade
from scripts.verify_restore import select_snapshot, verify_restored_snapshot


def test_clean_demo_replay_and_complete_recovery(tmp_path):
    project = tmp_path / "project"
    root = Path(__file__).resolve().parents[2]
    for directory in ("config/mappings", "demo/demodata/core/jira", "demo/demodata/core/gitlab", "demo/demodata/core/demo-repo"):
        shutil.copytree(root / directory, project / directory, ignore=shutil.ignore_patterns(".git"))
    repo = project / "demo" / "demodata" / "core" / "demo-repo"
    for command in (
        ["init", "-b", "main"],
        ["add", "."],
        ["-c", "user.name=EOIP Demo", "-c", "user.email=demo@example.invalid",
         "commit", "-m", "EOIP-1 implement impact calculation; EOIP-2 retain evidence"],
    ):
        subprocess.run(["git", "-C", str(repo), *command], check=True, capture_output=True)
    source, target = MemoryGraphStore(), MemoryGraphStore()
    result = verify_clean_demo(source, target, tmp_path, project_root=project)
    assert result["status"] == "PASS"
    assert result["replay_equivalent"]
    assert result["restored_raw_files"] > 0
    assert result["populated_target_rejected"]
    for ingestion in result["canonical_ingestion"].values():
        assert ingestion["contracts_valid"]
        assert ingestion["mutations"]["VERTEX"] > 0
        assert ingestion["mutations"]["EDGE"] > 0
        assert ingestion["run_count"] == 3


@pytest.mark.req("G2-T0220", "G2-T0221", "G2-T0223", "G2-T0225")
def test_disposable_temporal_upgrade_acceptance(tmp_path):
    result = verify_temporal_edge_upgrade(MemoryGraphStore(), tmp_path)
    assert result == {
        "legacy_edge_expired": True, "replacement_current_only": True,
        "deletion_barrier_preserved": True, "recreation_without_phantom_edge": True,
        "physical_history_edges": 3,
    }


@pytest.mark.parametrize("mutation", ["vertex", "edge", "raw", "extra_raw"])
def test_verifier_detects_loss_not_visible_in_graph_counts(tmp_path, mutation):
    source, target = MemoryGraphStore(), MemoryGraphStore()
    first = source.upsert_vertex("WorkItem", {"canonical_id": "issue:1", "name": "Original"})
    second = source.upsert_vertex("WorkItem", {"canonical_id": "issue:2"})
    source.upsert_edge("REFERENCES", first["vid"], second["vid"], {"confidence": 0.9})
    raw = tmp_path / "data" / "raw" / "jira" / "event.json"
    raw.parent.mkdir(parents=True)
    raw.write_text('{"event_id":"event"}', encoding="utf-8")
    snapshot = tmp_path / "snapshot.json"
    backup(source, tmp_path / "data", snapshot)
    restored = tmp_path / "restored"
    restore(target, restored, snapshot)
    verify_restored_snapshot(target, restored, snapshot)
    if mutation == "vertex":
        target.upsert_vertex("WorkItem", {"canonical_id": "issue:1", "name": "Changed"})
    elif mutation == "edge":
        vertices = {v["canonical_id"]: v["vid"] for v in target.find_vertices()}
        target.upsert_edge("REFERENCES", vertices["issue:1"], vertices["issue:2"], {"confidence": 0.1})
    elif mutation == "raw":
        (restored / "raw" / "jira" / "event.json").write_text('{"event_id":"changed"}', encoding="utf-8")
    else:
        (restored / "raw" / "jira" / "extra.json").write_text("{}", encoding="utf-8")
    assert target.count_vertices() == source.count_vertices()
    assert target.count_edges() == source.count_edges()
    with pytest.raises(AssertionError, match="differ"):
        verify_restored_snapshot(target, restored, snapshot)
    assert not (restored / "restore-verification.json").exists()


def test_snapshot_selection_is_explicit_and_missing_backup_is_actionable(tmp_path):
    with pytest.raises(FileNotFoundError, match="run the backup command first"):
        select_snapshot(None, tmp_path)
    older, newer = tmp_path / "20260101.json", tmp_path / "20260102.json"
    older.write_text(json.dumps({}), encoding="utf-8")
    newer.write_text(json.dumps({}), encoding="utf-8")
    assert select_snapshot(None, tmp_path) == newer
    assert select_snapshot(older, tmp_path) == older
    with pytest.raises(FileNotFoundError, match="Snapshot not found"):
        select_snapshot(tmp_path / "missing.json", tmp_path)
