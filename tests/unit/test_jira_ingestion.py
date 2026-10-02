import json

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService


def _service(tmp_path) -> tuple[JiraIngestionService, MemoryGraphStore]:
    store = MemoryGraphStore()
    connector = JiraJsonConnector()
    capture = FileEventCapture(tmp_path / "raw")
    return JiraIngestionService(store, connector, capture, tmp_path / "dlq"), store


def test_jira_import_captures_evidence_and_is_idempotent(tmp_path) -> None:
    service, store = _service(tmp_path)
    document = {
        "issues": [
            {
                "key": "EOIP-1",
                "fields": {
                    "summary": "Trace a requirement",
                    "project": {"key": "EOIP", "name": "EOIP"},
                    "assignee": {"accountId": "engineer-1", "displayName": "Demo Engineer"},
                },
            }
        ]
    }

    first = service.ingest(document)
    second = service.ingest(document)

    assert first["records_accepted"] == second["records_accepted"] == 1
    assert store.count_vertices("WorkItem") == 1
    assert store.count_vertices("Evidence") == 1
    assert store.count_edges("CONTAINS") == 1
    assert store.count_edges("EVIDENCED_BY") == 3
    assert store.count_vertices("Person") == 1
    assert store.count_edges("ASSIGNED_TO") == 1
    project = store.get_vertex_by_canonical_id("urn:eoip:work:project:jira:EOIP")
    run = store.get_vertex_by_canonical_id(f"urn:eoip:meta:ingestion-run:{first['run_id']}")
    assert project is not None and run is not None
    assert any(edge["in_v"] == run["vid"] for edge in store.edges_from(project["vid"], ["INGESTED_IN"]))
    assert store.edges_from(project["vid"], ["EVIDENCED_BY"])
    raw_files = list((tmp_path / "raw" / "jira").glob("*.json"))
    assert len(raw_files) == 1
    assert json.loads(raw_files[0].read_text(encoding="utf-8"))["payload_hash"]


def test_malformed_record_is_captured_and_quarantined_without_graph_mutation(tmp_path) -> None:
    service, store = _service(tmp_path)

    result = service.ingest({"issues": [{"fields": {"summary": "No key"}}]})

    assert result["run_status"] == "PARTIAL"
    assert result["records_rejected"] == 1
    assert store.count_vertices("WorkItem") == 0
    assert len(list((tmp_path / "raw" / "jira").glob("*.json"))) == 1
    assert len(list((tmp_path / "dlq").glob("*.json"))) == 1


def test_dry_run_validates_without_capture_or_graph_writes(tmp_path) -> None:
    service, store = _service(tmp_path)
    document = {"issues": [{"key": "EOIP-3", "fields": {"summary": "Dry run"}}]}

    result = service.ingest(document, dry_run=True)

    assert result["run_status"] == "DRY_RUN"
    assert result["records_accepted"] == 1
    assert store.count_vertices() == 0
    assert not (tmp_path / "raw").exists()


def test_jira_parent_relationship_is_created_even_when_parent_record_follows_child(tmp_path) -> None:
    service, store = _service(tmp_path)
    document = {
        "issues": [
            {"key": "EOIP-2", "fields": {"summary": "Child", "parent": {"key": "EOIP-1"}}},
            {"key": "EOIP-1", "fields": {"summary": "Parent"}},
        ]
    }

    result = service.ingest(document)

    assert result["records_accepted"] == 2
    parent = store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:EOIP-1")
    child = store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:EOIP-2")
    edge = store.find_edges(label="PARENT_OF")[0]
    assert edge["out_v"] == parent["vid"]
    assert edge["in_v"] == child["vid"]