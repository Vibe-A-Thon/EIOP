"""Binary acquisition, capture-first graph ingestion, replay and authenticated APIs."""

from _principals import provision_api_token
import base64
import json

import pytest
from eoip.connectors.config import connector_from_registry
from eoip.connectors.files import FileParsingConnector, FileParsingScope, file_event
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.fileparse.contracts import ParseError, ParseOptions
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.files import FileIngestionService, run_registered_file_operation
from eoip.ingestion.replay import replay_captured_events
from eoip.retrieval.vectors import KeywordIndex, VectorIndex
from fastapi.testclient import TestClient


@pytest.mark.req("G2-EKAF-025")
def test_binary_connector_scope_and_limits(tmp_path):
    content = b"\xff\x00binary"
    (tmp_path / "actual.png").write_bytes(content)
    connector = FileParsingConnector("local-source", FileParsingScope(roots=[str(tmp_path)]))
    event = next(connector.baseline())
    assert base64.b64decode(event.payload["content"]) == content
    assert event.source_record_type == "binary_file"
    assert connector.fetch_record(str(tmp_path / "actual.png")).event_id == event.event_id
    (tmp_path / "second.txt").write_text("second", encoding="utf-8")
    connector = FileParsingConnector("local-source", FileParsingScope(roots=[str(tmp_path)], max_files=1))
    with pytest.raises(ParseError, match="max_files"):
        list(connector.baseline())
    connector = FileParsingConnector("local-source", FileParsingScope(
        roots=[str(tmp_path)], excluded_paths=[str(tmp_path / "actual.png")],
    ))
    assert len(list(connector.baseline())) == 1
    with pytest.raises(ParseError):
        connector.fetch_record(str(tmp_path / "actual.png"))


@pytest.mark.req("G2-SYNC-011")
def test_capture_graph_retrieval_and_idempotent_replay(tmp_path):
    store = MemoryGraphStore()
    service = FileIngestionService(store, tmp_path)
    event = file_event(b"Actual searchable provenance", "body.txt", "my-source")
    result = service.ingest_event(event)
    captured = tmp_path / "raw" / "documents" / f"{event.event_id}.json"
    assert captured.is_file()
    assert json.loads(captured.read_text())["payload"]["content"] == event.payload["content"]
    assert (tmp_path / "fileparse" / result["bundle_id"] / "parsed.json").is_file()
    assert store.count_vertices("Document") == 1
    assert store.count_vertices("DocumentSection") == 1
    assert len(store.find_edges(label="EVIDENCED_BY")) == 2
    keyword, vector = KeywordIndex(), VectorIndex()
    for vertex in store.find_vertices("DocumentSection"):
        keyword.add(vertex["canonical_id"], vertex["properties"]["content"])
        vector.add(vertex["canonical_id"], vertex["properties"]["content"])
    assert keyword.search("searchable")[0][0] == result["result"]["chunks"][0]["chunk_id"]
    assert vector.search("searchable")[0][0] == result["result"]["chunks"][0]["chunk_id"]
    replay = replay_captured_events(store, tmp_path, source_system="documents")
    assert replay["records_replayed"] == 1
    assert replay["logical_diff"]["equivalent"]
    assert store.count_vertices("Document") == 1


def test_dry_run_no_writes_and_failed_parse_is_captured_in_dlq(tmp_path):
    root = tmp_path / "data"
    store = MemoryGraphStore()
    service = FileIngestionService(store, root)
    assert service.ingest(b"actual", "body.txt", dry_run=True)["run_status"] == "DRY_RUN"
    assert not root.exists()
    assert store.count_vertices() == 0
    with pytest.raises(ParseError):
        service.ingest(b"not sqlite", "broken.db")
    assert len(list((root / "raw" / "documents").glob("*.json"))) == 1
    assert len(list((root / "dlq").glob("*.json"))) == 1
    assert store.count_vertices() == 0


def test_tampered_event_rejected(tmp_path):
    event = file_event(b"actual", "body.txt", "source")
    event.payload["content"] = base64.b64encode(b"tampered").decode()
    with pytest.raises(ParseError) as exc:
        FileIngestionService(MemoryGraphStore(), tmp_path).ingest_event(event)
    assert exc.value.code == "hash_mismatch"


def test_registered_documents_baseline_and_replay(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "body.txt").write_text("registered actual content", encoding="utf-8")
    entry = SourceRegistryEntry(
        source_id="files", source_type="documents", name="Documents",
        allowed_scopes=[str(source)], config={"scope": {"roots": [str(source)]}},
    )
    assert isinstance(connector_from_registry(entry), FileParsingConnector)
    store = MemoryGraphStore()
    root = tmp_path / "data"
    result = run_registered_file_operation(entry, {"operation": "BASELINE"}, store, str(root), "test")
    assert result["records_accepted"] == 1
    assert (root / "state" / "connectors" / "files.json").is_file()
    event_id = result["results"][0]["event_id"]
    result = run_registered_file_operation(
        entry, {"operation": "REPLAY", "event_ids": [event_id]}, store, str(root), "test",
    )
    assert result["records_accepted"] == 1
    assert store.count_vertices("Document") == 1


@pytest.fixture
def client(tmp_path, monkeypatch):
    from apps.api import main

    monkeypatch.setenv("EOIP_API_TOKEN", "file-parser-test-token-24-characters")
    provision_api_token(monkeypatch, "file-parser-test-token-24-characters")
    monkeypatch.setenv("EOIP_DATA_DIR", str(tmp_path))
    store = MemoryGraphStore()
    monkeypatch.setattr(store, "close", lambda: None, raising=False)
    monkeypatch.setattr(main, "create_store", lambda: store)
    with TestClient(main.create_app()) as client:
        yield client, store, tmp_path


def auth():
    return {"Authorization": "Bearer file-parser-test-token-24-characters", "Content-Type": "application/octet-stream"}


def test_authenticated_parse_upload_and_persisted_download(client):
    client, store, root = client
    url = "/api/v1/admin/ingestion/files/parse?filename=actual.txt"
    assert client.post(url, content=b"actual").status_code == 401
    response = client.post(url, headers=auth(), content=b"Actual API content")
    assert response.status_code == 200, response.text
    result = response.json()
    bundle_id = result["bundle_id"]
    download = client.get(
        f"/api/v1/admin/ingestion/files/bundles/{bundle_id}/chunks.jsonl", headers=auth(),
    )
    assert download.status_code == 200
    assert json.loads(download.text)["text"] == "Actual API content"
    assert (root / "fileparse" / bundle_id / "manifest.json").is_file()
    assert store.count_vertices() == 0
    assert client.get(
        f"/api/v1/admin/ingestion/files/bundles/{bundle_id}/secrets.txt", headers=auth(),
    ).status_code == 404


def test_api_ingestion_and_error_contracts(client):
    client, store, _ = client
    base = "/api/v1/admin/ingestion/files"
    response = client.post(base + "?filename=actual.csv", headers=auth(), content=b"name\nactual\n")
    assert response.status_code == 200, response.text
    assert store.count_vertices("Document") == 1
    assert client.post(base + "?filename=actual.txt", headers=auth(), json={}).status_code == 200
    headers = {"Authorization": auth()["Authorization"], "Content-Type": "application/json"}
    assert client.post(base + "?filename=actual.txt", headers=headers, json={}).status_code == 415
    assert client.post(base + "?filename=bad.json", headers=auth(), content=b"{").status_code == 422
    assert client.post(base + "?filename=../bad.txt", headers=auth(), content=b"bad").status_code == 422


def test_api_upload_stream_limit_and_missing_tool(client, monkeypatch):
    from eoip.fileparse import api, tools

    client, _, _ = client
    monkeypatch.setattr(api, "ParseOptions", lambda **options: ParseOptions(max_file_bytes=3, **options))
    base = "/api/v1/admin/ingestion/files/parse"
    assert client.post(base + "?filename=actual.txt", headers=auth(), content=b"four").status_code == 413
    monkeypatch.setattr(tools.shutil, "which", lambda _: None)
    response = client.post(base + "?filename=actual.doc", headers=auth(), content=b"bin")
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "tool_unavailable"


def test_registered_batch_continues_after_parse_failure_without_advancing_checkpoint(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a-bad.json").write_bytes(b"{")
    (source / "b-good.txt").write_text("good", encoding="utf-8")
    entry = SourceRegistryEntry(
        source_id="files", source_type="documents", name="Documents",
        allowed_scopes=[str(source)], config={"scope": {"roots": [str(source)]}},
    )
    root = tmp_path / "data"
    store = MemoryGraphStore()
    result = run_registered_file_operation(entry, {"operation": "BASELINE"}, store, str(root), "test")
    assert result["run_status"] == "PARTIAL"
    assert result["records_accepted"] == result["records_rejected"] == 1
    assert store.count_vertices("Document") == 1
    assert len(list((root / "raw" / "documents").glob("*.json"))) == 2
    assert not (root / "state" / "connectors" / "files.json").exists()


def test_worker_dispatch_and_selected_replay_stay_within_source(tmp_path):
    from eoip.connectors.registry import SourceRegistry

    from apps.worker.main import execute_job

    source = tmp_path / "source"
    source.mkdir()
    for name in ("one", "two"):
        (source / f"{name}.txt").write_text(name, encoding="utf-8")
    entry = SourceRegistryEntry(
        source_id="files", source_type="documents", name="Documents",
        allowed_scopes=[str(source)], config={"scope": {"roots": [str(source)]}},
    )
    root = tmp_path / "data"
    SourceRegistry(root / "state" / "source-registry.json").create(entry)
    store = MemoryGraphStore()
    job = {"kind": "SOURCE_OPERATION", "correlation_id": "test",
           "payload": {"source_id": "files", "operation": "BASELINE"}}
    baseline = execute_job(store, root, job)
    assert baseline["records_accepted"] == 2
    checkpoint = (root / "state" / "connectors" / "files.json").read_bytes()
    selected = baseline["results"][0]["event_id"]
    result = run_registered_file_operation(
        entry, {"operation": "REPLAY", "event_ids": [selected]}, store, str(root), "test",
    )
    assert result["records_seen"] == 1
    assert (root / "state" / "connectors" / "files.json").read_bytes() == checkpoint
    foreign = file_event(b"foreign", "foreign.txt", "another-source")
    FileIngestionService(store, root).ingest_event(foreign)
    for event_ids in ([], ["../escape"], [foreign.event_id], ["0" * 64]):
        with pytest.raises(ValueError):
            run_registered_file_operation(
                entry, {"operation": "REPLAY", "event_ids": event_ids}, store, str(root), "test",
            )


def test_registered_source_root_allowlist_is_enforced(tmp_path):
    from eoip.connectors.errors import ConnectorError

    allowed = tmp_path / "allowed"
    outside = tmp_path / "outside"
    allowed.mkdir()
    outside.mkdir()
    entry = SourceRegistryEntry(
        source_id="files", source_type="documents", name="Documents",
        allowed_scopes=[str(allowed)], config={"scope": {"roots": [str(outside)]}},
    )
    with pytest.raises(ConnectorError):
        connector_from_registry(entry)
