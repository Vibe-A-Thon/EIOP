import json

import pytest
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.servicenow import ServiceNowConnector
from eoip.connectors.sync import SyncBatch
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.replay import logical_graph_output, logical_output_diff
from eoip.ingestion.source_sync import SourceSyncIngestionService


@pytest.mark.req("FR-CONF-001", "FR-SNOW-001", "FR-CONN-006")
@pytest.mark.parametrize("source_system", ["confluence", "servicenow"])
def test_rest_refetch_preserves_capture_provenance_and_replay_freshness(tmp_path, source_system):
    connector = (
        ConfluenceConnector("https://confluence.example", token="fixture-only")
        if source_system == "confluence"
        else ServiceNowConnector("https://servicenow.example", token="fixture-only")
    )
    with connector:
        kind = "space" if source_system == "confluence" else "incident"
        payload = (
            {"key": "ENG", "name": "Engineering"}
            if kind == "space"
            else {
                "sys_id": "1", "number": "INC001", "short_description": "Fixture",
                "sys_updated_on": "2026-10-01 00:00:00",
            }
        )
        original = connector.make_event(kind, f"{connector.instance_id}:{kind}:1", payload, "1")
        original = original.model_copy(update={
            "captured_at": "2026-10-01T00:00:00Z", "event_time": "2026-10-01T00:00:00Z",
        })
        newer = original.model_copy(update={
            "captured_at": "2026-10-03T00:00:00Z", "event_time": "2026-10-03T00:00:00Z",
        })
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
        )
        assert service.ingest(SyncBatch([original], original.captured_at))["run_status"] == "SUCCEEDED"
        raw = tmp_path / "raw" / source_system / f"{original.event_id}.json"
        raw_bytes = raw.read_bytes()
        first = logical_graph_output(store)
        assert service.ingest(SyncBatch([newer], newer.captured_at))["run_status"] == "SUCCEEDED"
        latest = logical_graph_output(store)
        evidence = store.find_vertices(label="Evidence", filters={"evidence_key": original.event_id})[0]
        assert evidence["properties"]["captured_at"] == original.captured_at
        subject = next(v for v in store.find_vertices() if v["label"] in {"KnowledgeSpace", "WorkItem"})
        assert subject["properties"]["last_seen"] == newer.captured_at
        expected = json.loads(json.dumps(first))
        expected["vertices"][subject["canonical_id"]]["properties"]["last_seen"] = newer.captured_at
        assert logical_output_diff(expected, latest)["equivalent"]
        assert service.ingest(SyncBatch([original], newer.captured_at))["run_status"] == "SUCCEEDED"
        assert logical_output_diff(latest, logical_graph_output(store))["equivalent"]
        assert raw.read_bytes() == raw_bytes


@pytest.mark.req("FR-CONF-001")
def test_confluence_sync_ingestion_persists_documents_and_provenance_idempotently(tmp_path):
    connector = ConfluenceConnector("https://confluence.example/wiki", token="test-token")
    instance = connector.instance_id
    events = [
        connector.make_event(
            "space",
            f"{instance}:space:ENG",
            {"key": "ENG", "name": "Engineering", "description": "Engineering docs"},
            1,
        ),
        connector.make_event(
            "page",
            f"{instance}:page:42",
            {
                "id": "42",
                "title": "Release process",
                "space": {"key": "ENG"},
                "version": {"number": 7, "when": "2026-10-02T10:00:00Z"},
                "body": {"storage": {"value": "<p>Deploy safely</p>"}},
                "ancestors": [],
                "_links": {"webui": "/pages/42"},
            },
            7,
        ),
        connector.make_event(
            "attachment",
            f"{instance}:attachment:84",
            {
                "id": "84",
                "title": "diagram.png",
                "space": {"key": "ENG"},
                "container": {"id": "42"},
                "version": {"number": 2},
                "extensions": {"mediaType": "image/png", "fileSize": 1234},
            },
            2,
        ),
    ]
    batch = SyncBatch(events=events, next_checkpoint="2026-10-02T12:00:00Z")
    store = MemoryGraphStore()
    service = SourceSyncIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
    )
    replayed_events = [
        connector.make_event(
            event.metadata["record_kind"],
            event.source_record_id,
            event.payload,
            event.source_version,
        )
        for event in events
    ]

    first = service.ingest(batch)
    first_seen = store.get_vertex_by_canonical_id(
        f"urn:eoip:knowledge:document:{instance}:page:42"
    )["properties"]["first_seen"]
    second = service.ingest(SyncBatch(events=replayed_events, next_checkpoint=batch.next_checkpoint))

    assert first["run_status"] == second["run_status"] == "SUCCEEDED"
    assert store.count_vertices("KnowledgeSpace") == 1
    assert store.count_vertices("Document") == 2
    assert store.count_vertices("Evidence") == 3
    assert store.count_edges("EVIDENCED_BY") == 3
    assert store.count_edges("CONTAINS") == 3
    page = store.get_vertex_by_canonical_id(f"urn:eoip:knowledge:document:{instance}:page:42")
    attachment = store.get_vertex_by_canonical_id(
        f"urn:eoip:knowledge:document:{instance}:attachment:84"
    )
    assert page["properties"]["path"] == "https://confluence.example/wiki/pages/42"
    assert page["properties"]["first_seen"] == first_seen
    assert page["properties"]["description"] == "<p>Deploy safely</p>"
    assert attachment["properties"]["media_type"] == "image/png"
    assert attachment["properties"]["file_size"] == 1234
    assert len(list((tmp_path / "raw" / "confluence").glob("*.json"))) == 3


@pytest.mark.req("FR-SNOW-001")
def test_servicenow_sync_ingestion_maps_work_items_and_links_run_evidence(tmp_path):
    connector = ServiceNowConnector(
        "https://servicenow.example",
        token="test-token",
        tables={"incident": "incident"},
    )
    event = connector.make_event(
        "incident",
        f"{connector.instance_id}:incident:sys-id-1",
        {
            "sys_id": "sys-id-1",
            "number": "INC001234",
            "short_description": "Authentication outage",
            "description": "Login requests fail",
            "state": "2",
            "sys_updated_on": "2026-10-02 10:00:00",
        },
        "2026-10-02 10:00:00",
    )
    batch = SyncBatch(events=[event], next_checkpoint="2026-10-02T12:00:00Z")
    store = MemoryGraphStore()
    service = SourceSyncIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
    )

    first = service.ingest(batch)
    second = service.ingest(batch)

    assert first["run_status"] == second["run_status"] == "SUCCEEDED"
    assert store.count_vertices("WorkItem") == 1
    assert store.count_vertices("Evidence") == 1
    assert store.count_edges("EVIDENCED_BY") == 1
    item = store.get_vertex_by_canonical_id(
        f"urn:eoip:work:item:servicenow:{event.source_record_id}"
    )
    assert item["properties"]["issue_key"] == "INC001234"
    assert item["properties"]["summary"] == "Authentication outage"
    assert item["properties"]["issue_type"] == "incident"
    runs = store.edges_from(item["vid"], labels=["INGESTED_IN"])
    assert len(runs) == 2
    raw_event = json.loads(
        next((tmp_path / "raw" / "servicenow").glob("*.json")).read_text(encoding="utf-8")
    )
    assert raw_event["payload_hash"] == event.payload_hash


@pytest.mark.req("FR-SNOW-001")
def test_servicenow_knowledge_records_are_persisted_as_documents(tmp_path):
    connector = ServiceNowConnector(
        "https://servicenow.example",
        token="test-token",
        tables={"knowledge": "kb_knowledge"},
    )
    event = connector.make_event(
        "knowledge",
        f"{connector.instance_id}:kb_knowledge:article-1",
        {
            "sys_id": "article-1",
            "number": "KB001",
            "short_description": "Reset account credentials",
            "description": "Follow the approved account recovery steps.",
            "sys_updated_on": "2026-10-02 10:00:00",
        },
        "2026-10-02 10:00:00",
    )
    store = MemoryGraphStore()
    service = SourceSyncIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
    )

    result = service.ingest(SyncBatch(events=[event], next_checkpoint="2026-10-02T12:00:00Z"))

    assert result["run_status"] == "SUCCEEDED"
    assert store.count_vertices("WorkItem") == 0
    assert store.count_vertices("Document") == 1
    document = store.get_vertex_by_canonical_id(
        f"urn:eoip:knowledge:document:servicenow:{event.source_record_id}"
    )
    assert document["properties"]["name"] == "Reset account credentials"
    assert document["properties"]["description"] == "Follow the approved account recovery steps."


@pytest.mark.req("FR-CONF-001")
def test_confluence_mapping_rejection_is_captured_and_does_not_advance_batch(tmp_path):
    connector = ConfluenceConnector("https://confluence.example", token="test-token")
    event = connector.make_event(
        "page",
        f"{connector.instance_id}:page:bad",
        {"id": "bad", "space": {"key": "ENG"}},
        1,
    )
    store = MemoryGraphStore()
    service = SourceSyncIngestionService(
        store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq")
    )

    result = service.ingest(SyncBatch(events=[event], next_checkpoint="2026-10-02T12:00:00Z"))

    assert result["run_status"] == "PARTIAL"
    assert result["records_rejected"] == 1
    assert result["rejected"][0]["error_category"] == "mapping_error"
    assert store.count_vertices("Document") == 0
    assert len(list((tmp_path / "raw" / "confluence").glob("*.json"))) == 1
    dlq_record = json.loads(next((tmp_path / "dlq").glob("*.json")).read_text(encoding="utf-8"))
    assert dlq_record["error_category"] == "mapping_error"
    assert dlq_record["correlation_id"] == result["correlation_id"]


@pytest.mark.req("FR-SNOW-001")
def test_source_sync_checkpoint_is_saved_only_after_successful_non_dry_run(
    monkeypatch, tmp_path
):
    from eoip.ingestion.source_sync import run_configured_source_sync

    connector = ServiceNowConnector(
        "https://servicenow.example",
        token="test-token",
        tables={"incident": "incident"},
    )
    instance = connector.instance_id
    rejected_event = connector.make_event(
        "incident",
        f"{instance}:incident:missing-number",
        {"sys_id": "missing-number", "short_description": "Incomplete record"},
        "2026-10-02 10:00:00",
    )
    batches = [
        SyncBatch(events=[], next_checkpoint="2026-10-02T00:00:00Z"),
        SyncBatch(events=[rejected_event], next_checkpoint="2026-10-02T12:00:00Z"),
        SyncBatch(events=[], next_checkpoint="2026-10-03T00:00:00Z"),
    ]
    captured_checkpoints = []

    def sync(**kwargs):
        captured_checkpoints.append(kwargs["checkpoint"])
        return batches.pop(0)

    monkeypatch.setattr(connector, "sync", sync)
    monkeypatch.setattr(
        "eoip.connectors.config.connector_from_environment",
        lambda *_args, **_kwargs: connector,
    )
    store = MemoryGraphStore()
    checkpoint_path = tmp_path / "state" / "connectors" / "servicenow.json"
    checkpoint_path.parent.mkdir(parents=True)
    checkpoint_path.write_text(
        json.dumps({"checkpoint": "2026-10-01T00:00:00Z"}), encoding="utf-8"
    )

    dry_result = run_configured_source_sync(
        "servicenow", {"dry_run": True}, store, str(tmp_path), "correlation-dry"
    )
    assert dry_result["run_status"] == "DRY_RUN"
    assert json.loads(checkpoint_path.read_text(encoding="utf-8"))["checkpoint"] == (
        "2026-10-01T00:00:00Z"
    )

    partial_result = run_configured_source_sync(
        "servicenow", {}, store, str(tmp_path), "correlation-partial"
    )
    assert partial_result["run_status"] == "PARTIAL"
    assert json.loads(checkpoint_path.read_text(encoding="utf-8"))["checkpoint"] == (
        "2026-10-01T00:00:00Z"
    )

    result = run_configured_source_sync(
        "servicenow", {}, store, str(tmp_path), "correlation-success"
    )

    assert result["run_status"] == "SUCCEEDED"
    assert captured_checkpoints == ["2026-10-01T00:00:00Z"] * 3
    assert json.loads(checkpoint_path.read_text(encoding="utf-8"))["checkpoint"] == (
        "2026-10-03T00:00:00Z"
    )
