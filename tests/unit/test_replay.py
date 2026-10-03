from eoip.codegraph.parser import CodeParser
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.connectors.local_code import LocalCodeConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.code import CodeIngestionService
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.ingestion.replay import (
    logical_graph_output,
    logical_output_diff,
    replay_captured_events,
)

from apps.worker.main import execute_job


def _captured_jira_graph(tmp_path):
    store = MemoryGraphStore()
    service = JiraIngestionService(
        store,
        JiraJsonConnector(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    service.ingest(
        {
            "issues": [
                {
                    "key": "EOIP-REPLAY-1",
                    "fields": {
                        "summary": "Replay captured source event",
                        "project": {"key": "EOIP", "name": "EOIP"},
                    },
                }
            ]
        }
    )
    event_id = next((tmp_path / "raw" / "jira").glob("*.json")).stem
    return store, event_id


def test_replay_preserves_captured_identity_and_is_logically_equivalent(tmp_path):
    store, event_id = _captured_jira_graph(tmp_path)
    expected = logical_graph_output(store)

    result = replay_captured_events(
        store,
        tmp_path,
        source_system="jira",
        event_ids=[event_id],
    )

    assert result["records_replayed"] == 1
    assert result["logical_diff"]["equivalent"] is True, result["logical_diff"]
    assert logical_graph_output(store) == expected
    evidence = store.get_vertex_by_canonical_id(
        f"urn:eoip:evidence:source-event:jira:{event_id}"
    )
    assert evidence["properties"]["evidence_key"] == event_id


def test_worker_executes_replay_job_kind(tmp_path):
    store, event_id = _captured_jira_graph(tmp_path)

    result = execute_job(
        store,
        tmp_path,
        {
            "kind": "REPLAY",
            "correlation_id": "replay-correlation",
            "payload": {
                "source_system": "jira",
                "event_ids": [event_id],
                "dry_run": False,
            },
        },
    )

    assert result["run_status"] == "SUCCEEDED"
    assert result["records_replayed"] == 1
    assert result["logical_diff"]["equivalent"] is True


def test_replay_rejects_missing_selected_event(tmp_path):
    store, _event_id = _captured_jira_graph(tmp_path)

    try:
        replay_captured_events(
            store,
            tmp_path,
            source_system="jira",
            event_ids=["0" * 64],
        )
    except ValueError as exc:
        assert "captured events not found" in str(exc)
    else:
        raise AssertionError("missing replay event must be rejected")


def test_logical_output_diff_reports_golden_drift():
    expected = {"vertices": {"urn:test:1": {"label": "Project"}}, "edges": {}}
    actual = {
        "vertices": {
            "urn:test:1": {"label": "Repository"},
            "urn:test:2": {"label": "Project"},
        },
        "edges": {},
    }

    diff = logical_output_diff(expected, actual)

    assert diff == {
        "vertices": {
            "added": ["urn:test:2"],
            "removed": [],
            "changed": ["urn:test:1"],
        },
        "edges": {"added": [], "removed": [], "changed": []},
        "equivalent": False,
    }


def test_captured_code_event_replays_without_source_tree(tmp_path):
    source_root = tmp_path / "repository"
    source_root.mkdir()
    (source_root / "service.py").write_text(
        "def execute():\n    return 'ok'\n",
        encoding="utf-8",
    )
    store = MemoryGraphStore()
    service = CodeIngestionService(
        store,
        LocalCodeConnector(),
        CodeParser(),
        FileEventCapture(tmp_path / "raw"),
        tmp_path / "dlq",
    )
    service.ingest(source_root, "platform")
    event_id = next((tmp_path / "raw" / "git").glob("*.json")).stem
    expected = logical_graph_output(store)
    (source_root / "service.py").unlink()

    result = replay_captured_events(
        store,
        tmp_path,
        source_system="git",
        event_ids=[event_id],
    )

    assert result["records_replayed"] == 1
    assert result["logical_diff"]["equivalent"] is True, result["logical_diff"]
    assert logical_graph_output(store) == expected
