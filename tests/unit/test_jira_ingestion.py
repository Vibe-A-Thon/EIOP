import json
from pathlib import Path

import pytest

from eoip.connectors.jira_json import JiraJsonConnector
from eoip.contracts.source_event import SourceEvent
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService

pytestmark = pytest.mark.req("FR-CONN-002")


def _service(tmp_path) -> tuple[JiraIngestionService, MemoryGraphStore]:
    store = MemoryGraphStore()
    connector = JiraJsonConnector()
    capture = FileEventCapture(tmp_path / "raw")
    return JiraIngestionService(store, connector, capture, tmp_path / "dlq"), store


@pytest.mark.req("FR-INGEST-001")
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


def test_jira_import_accepts_configured_mapping_and_local_fixture(tmp_path) -> None:
    store = MemoryGraphStore()
    connector = JiraJsonConnector.from_yaml("config/mappings/jira-mvp.yaml")
    service = JiraIngestionService(store, connector, FileEventCapture(tmp_path / "raw"), tmp_path / "dlq")
    document = json.loads(
        Path("demo/demodata/core/jira/sample-jira.json").read_text(encoding="utf-8")
    )

    result = service.ingest(document)

    assert result["run_status"] == "SUCCEEDED"
    assert result["records_accepted"] == 2
    work_item = store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:EOIP-1")
    project = store.get_vertex_by_canonical_id("urn:eoip:work:project:jira:EOIP")
    person = store.get_vertex_by_canonical_id("urn:eoip:identity:person:email:engineer@example.invalid")
    assert work_item is not None
    assert work_item["properties"]["summary"] == "Trace a requirement to its implementation"
    assert work_item["properties"]["issue_type"] == "Story"
    assert work_item["properties"]["status"] == "In Progress"
    assert project is not None
    assert project["properties"]["name"] == "Enterprise Ontology Intelligence Platform"
    assert person is not None
    assert store.count_edges("ASSIGNED_TO") == 1


def test_jira_resume_replays_captured_events_without_regenerating_identity(tmp_path) -> None:
    service, store = _service(tmp_path)
    document = {"issues": [{"key": "EOIP-4", "fields": {"summary": "Resume import"}}]}

    first = service.ingest(document)
    captured_path = next((tmp_path / "raw" / "jira").glob("*.json"))
    captured = SourceEvent.model_validate(json.loads(captured_path.read_text(encoding="utf-8")))
    replay = service.ingest_events([captured])

    assert first["run_status"] == replay["run_status"] == "SUCCEEDED"
    assert first["records_accepted"] == replay["records_accepted"] == 1
    assert store.count_vertices("WorkItem") == 1
    assert store.count_vertices("Evidence") == 1
    assert len(list((tmp_path / "raw" / "jira").glob("*.json"))) == 1
    raw = json.loads(captured_path.read_text(encoding="utf-8"))
    assert raw["event_id"] == captured.event_id
    assert raw["payload_hash"] == captured.payload_hash


@pytest.mark.req("FR-CONN-007")
def test_jira_source_deletion_tombstones_without_hard_delete(tmp_path) -> None:
    service, store = _service(tmp_path)
    service.ingest({"issues": [{"key": "EOIP-7", "fields": {"summary": "Current issue"}}]})

    result = service.ingest(
        {"issues": [{"key": "EOIP-7", "deleted": True, "deleted_at": "2026-10-11T00:00:00Z"}]}
    )

    assert result["run_status"] == "SUCCEEDED"
    assert store.count_vertices("WorkItem") == 0
    hidden = store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:EOIP-7")
    assert hidden is not None
    assert hidden["properties"]["deleted_at"] == "2026-10-11T00:00:00Z"
    assert store.find_vertices("WorkItem", {"issue_key": "EOIP-7"}, include_deleted=True) == [hidden]
    assert len(list((tmp_path / "raw" / "jira").glob("*.json"))) == 2


@pytest.mark.req("FR-CONN-007")
def test_jira_source_reappearance_restores_current_view(tmp_path) -> None:
    service, store = _service(tmp_path)

    service.ingest({"issues": [{"key": "EOIP-8", "deleted": True}]})
    service.ingest({"issues": [{"key": "EOIP-8", "fields": {"summary": "Restored issue"}}]})

    restored = store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:EOIP-8")
    assert restored is not None
    assert restored["properties"]["summary"] == "Restored issue"
    assert "deleted_at" not in restored["properties"]
    assert store.find_vertices("WorkItem", {"issue_key": "EOIP-8"}) == [restored]


@pytest.mark.req("FR-INGEST-001")
def test_malformed_record_is_captured_and_quarantined_without_graph_mutation(tmp_path) -> None:
    service, store = _service(tmp_path)

    result = service.ingest({"issues": [{"fields": {"summary": "No key"}}]})

    assert result["run_status"] == "PARTIAL"
    assert result["records_rejected"] == 1
    assert store.count_vertices("WorkItem") == 0
    assert len(list((tmp_path / "raw" / "jira").glob("*.json"))) == 1
    assert len(list((tmp_path / "dlq").glob("*.json"))) == 1


def test_dlq_record_uses_the_unified_envelope(tmp_path) -> None:
    """FR-INGEST-005: every service writes the same DLQ envelope fields."""
    service, _store = _service(tmp_path)

    service.ingest({"issues": [{"fields": {"summary": "No key"}}]})

    records = list((tmp_path / "dlq").glob("*.json"))
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    for field in (
        "event_id",
        "source_system",
        "source_record_id",
        "payload_hash",
        "stage",
        "error_category",
        "error",
    ):
        assert field in record, f"DLQ record missing unified field: {field}"
    assert record["source_system"] == "jira"
    assert record["stage"] == "mapping"
    assert record["error_category"] == "mapping_error"
    assert record["replay_ref"]


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


def test_jira_ingestion_creates_belongs_to_domain_edges(tmp_path) -> None:
    """P1-17: Ingested entities are linked to their GraphDomain."""
    service, store = _service(tmp_path)
    document = {
        "issues": [
            {
                "key": "EOIP-10",
                "fields": {
                    "summary": "Domain test",
                    "project": {"key": "EOIP", "name": "EOIP"},
                    "assignee": {"accountId": "eng-1", "displayName": "Engineer"},
                },
            }
        ]
    }

    service.ingest(document)

    domain_edges = store.find_edges(label="BELONGS_TO_DOMAIN")
    assert len(domain_edges) >= 2
    domain_vids = {e["in_v"] for e in domain_edges}
    domain_labels = {store.get_vertex(vid)["label"] for vid in domain_vids}
    assert domain_labels == {"GraphDomain"}
