"""Deterministic captured-event replay (FR-CONN-006)."""

import pytest
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.replay import replay_captured_events


def _ingest_jira(tmp_path, document):
    store = MemoryGraphStore()
    service = JiraIngestionService(
        store,
        JiraJsonConnector.from_yaml("config/mappings/jira-mvp.yaml"),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    result = service.ingest(document)
    return store, service, result


def test_replay_is_idempotent_and_preserves_counts(tmp_path):
    document = {
        "issues": [
            {"key": "EOIP-7", "fields": {"summary": "Replay me", "project": {"key": "EOIP"}}},
        ]
    }
    store, _service, first = _ingest_jira(tmp_path, document)
    assert first["records_accepted"] == 1
    before = store.count_vertices()

    replay = replay_captured_events(store, tmp_path, source_system="jira")

    assert replay["records_replayed"] == 1
    assert replay["run_status"] == "SUCCEEDED"
    # Logical entities are unchanged; only a new IngestionRun records the replay.
    assert store.count_vertices() - before == 1
    assert store.count_vertices("IngestionRun") == 2
    assert store.count_vertices("WorkItem") == 1


def test_replay_dry_run_writes_nothing(tmp_path):
    document = {"issues": [{"key": "EOIP-8", "fields": {"summary": "Dry"}}]}
    store, _service, _ = _ingest_jira(tmp_path, document)
    before = store.count_vertices()

    replay = replay_captured_events(store, tmp_path, source_system="jira", dry_run=True)

    assert replay["run_status"] == "DRY_RUN"
    assert store.count_vertices() == before


def test_replay_with_unknown_event_id_fails_explicitly(tmp_path):
    document = {"issues": [{"key": "EOIP-9", "fields": {"summary": "One"}}]}
    store, _service, _ = _ingest_jira(tmp_path, document)

    with pytest.raises(ValueError, match="not found"):
        replay_captured_events(
            store, tmp_path, source_system="jira", event_ids=["f" * 64]
        )


def test_replay_unsupported_source_fails_explicitly(tmp_path):
    store = MemoryGraphStore()
    with pytest.raises(ValueError, match="not supported"):
        replay_captured_events(store, tmp_path, source_system="confluence")


def test_replay_empty_source_is_a_noop_success(tmp_path):
    store = MemoryGraphStore()
    (tmp_path / "raw" / "jira").mkdir(parents=True)

    replay = replay_captured_events(store, tmp_path, source_system="jira")

    assert replay["records_seen"] == 0
    assert replay["run_status"] == "SUCCEEDED"
