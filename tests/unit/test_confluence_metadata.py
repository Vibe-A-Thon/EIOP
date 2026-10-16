import json

import httpx
import pytest
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.sync import SyncBatch
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.replay import logical_graph_output, logical_output_diff
from eoip.ingestion.source_sync import SourceSyncIngestionService


def page_payload():
    return {
        "id": "42", "title": "Deploy", "space": {"key": "ENG"},
        "body": {"storage": {"value": "<h1>Deploy</h1>"}},
        "history": {
            "createdBy": {"type": "known", "userKey": "author-key", "username": "author",
                          "displayName": "Author", "email": "not-extracted@example.test"},
            "createdDate": "2026-10-01T02:00:00+02:00",
        },
        "version": {"number": 2, "when": "2026-10-02T00:00:00Z",
                    "by": {"type": "known", "userKey": "editor-key", "displayName": "Editor"}},
        "metadata": {"labels": {"results": [
            {"name": "runbook", "prefix": "global"},
            {"name": "deploy", "prefix": "global"},
            {"name": "runbook", "prefix": "global"},
        ]}},
    }


def expected_metadata():
    return {
        "schema_version": "1.0",
        "labels": [{"name": "deploy", "prefix": "global"}, {"name": "runbook", "prefix": "global"}],
        "author": {"type": "known", "user_key": "author-key", "username": "author",
                   "display_name": "Author"},
        "editor": {"type": "known", "user_key": "editor-key", "display_name": "Editor"},
        "created_at": "2026-10-01T00:00:00Z",
        "modified_at": "2026-10-02T00:00:00Z",
    }


@pytest.mark.req("G2-SRC-CONF-001", "FR-CONF-001")
def test_page_metadata_normalizes_labels_actors_and_source_timestamps():
    with ConfluenceConnector("https://wiki.example", token="fixture") as connector:
        event = connector.make_event("page", f"{connector.instance_id}:page:42", page_payload(), 2)
        assert connector.map_event(event)["source_metadata"] == expected_metadata()
        empty = connector.make_event("page", event.source_record_id, {
            "id": "42", "title": "Deploy", "space": {"key": "ENG"},
        }, 3)
        assert connector.map_event(empty)["source_metadata"] == {
            "schema_version": "1.0", "labels": [], "author": None, "editor": None,
            "created_at": None, "modified_at": None,
        }
        precise = page_payload()
        precise["version"]["when"] = "2026-10-02T02:00:00.123+02:00"
        precise_event = connector.make_event("page", event.source_record_id, precise, 2)
        assert connector.map_event(precise_event)["source_metadata"]["modified_at"] == "2026-10-02T00:00:00.123000Z"


@pytest.mark.req("G2-SRC-CONF-001")
@pytest.mark.parametrize(("field", "value"), [
    ("metadata", []),
    ("metadata", {"labels": []}),
    ("metadata", {"labels": {"results": {}}}),
    ("metadata", {"labels": {"results": [{"name": ""}]}}),
    ("metadata", {"labels": {"results": [{"name": "deploy", "prefix": 7}]}}),
    ("metadata", {"labels": {"results": [], "_links": {"next": "/unfetched"}}}),
    ("history", {"createdBy": []}),
    ("history", {"createdBy": {"userKey": 5}}),
    ("history", {"createdDate": "not-a-date"}),
    ("version", {"by": {"displayName": []}}),
    ("version", {"when": "not-a-date"}),
])
def test_invalid_page_metadata_is_captured_and_rejected_before_document_writes(tmp_path, field, value):
    with ConfluenceConnector("https://wiki.example", token="fixture") as connector:
        payload = {**page_payload(), field: value}
        event = connector.make_event("page", f"{connector.instance_id}:page:42", payload, 2)
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq"),
        )
        result = service.ingest(SyncBatch([event], event.captured_at))
        assert result["run_status"] == "PARTIAL" and result["records_rejected"] == 1
        assert store.count_vertices("Document") == store.count_vertices("Evidence") == 0
        assert (tmp_path / "raw" / "confluence" / f"{event.event_id}.json").exists()
        assert len(list((tmp_path / "dlq").rglob("*.json"))) == 1


@pytest.mark.req("G2-SRC-CONF-001", "G2-ARCH-007", "FR-CONN-006")
def test_metadata_persists_in_revisions_clears_on_update_and_is_replay_stable(tmp_path):
    with ConfluenceConnector("https://wiki.example", token="fixture") as connector:
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq"),
        )
        original = connector.make_event("page", f"{connector.instance_id}:page:42", page_payload(), 2)
        original = original.model_copy(update={"event_time": "2026-10-02T00:00:00Z"})
        assert service.ingest(SyncBatch([original], original.captured_at))["run_status"] == "SUCCEEDED"
        cid = f"urn:eoip:knowledge:document:{original.source_record_id}"
        page = store.get_vertex_by_canonical_id(cid)
        assert json.loads(page["properties"]["payload_json"])["source_metadata"] == expected_metadata()
        raw_path = tmp_path / "raw" / "confluence" / f"{original.event_id}.json"
        raw = raw_path.read_bytes()
        before = logical_graph_output(store)
        assert service.ingest(SyncBatch([original], original.captured_at))["run_status"] == "SUCCEEDED"
        assert logical_output_diff(before, logical_graph_output(store))["equivalent"]
        assert raw_path.read_bytes() == raw
        updated = connector.make_event("page", original.source_record_id, {
            "id": "42", "title": "Deploy", "space": {"key": "ENG"},
            "body": {"storage": {"value": "<h1>Deploy</h1>"}},
            "version": {"number": 3, "when": "2026-10-03T00:00:00Z"},
        }, 3).model_copy(update={"event_time": "2026-10-03T00:00:00Z"})
        assert service.ingest(SyncBatch([updated], updated.captured_at))["run_status"] == "SUCCEEDED"
        latest = store.get_vertex_by_canonical_id(cid)["properties"]["payload_json"]
        assert json.loads(latest)["source_metadata"]["labels"] == []
        assert json.loads(latest)["source_metadata"]["author"] is None
        old = next(r for r in store.find_vertices(label="EntityRevision", filters={"subject_id": cid})
                   if not r["properties"]["is_current"])
        state = json.loads(old["properties"]["payload_json"])
        assert json.loads(state["properties"]["payload_json"])["source_metadata"] == expected_metadata()
        assert service.ingest(SyncBatch([original], updated.captured_at))["run_status"] == "SUCCEEDED"
        assert store.get_vertex_by_canonical_id(cid)["properties"]["payload_json"] == latest


def label_client(label_response):
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path == "/rest/api/space":
            return httpx.Response(200, json={"results": [{"key": "ENG", "name": "Engineering"}]})
        if request.url.path.endswith("/label"):
            return label_response(request)
        if request.url.path.endswith("/content/42"):
            return httpx.Response(200, json={"id": "42", "version": {"number": 1}})
        if "type = attachment" in request.url.params["cql"]:
            return httpx.Response(200, json={"results": []})
        payload = page_payload()
        payload["metadata"]["labels"] = {
            "results": [{"name": "partial", "prefix": "global"}],
            "_links": {"next": "https://untrusted.example/never-follow"},
        }
        return httpx.Response(200, json={"results": [payload]})

    return httpx.Client(base_url="https://wiki.example", transport=httpx.MockTransport(handler)), requests


@pytest.mark.req("G2-SRC-CONF-001", "FR-CONF-001")
def test_acquisition_completes_truncated_labels_without_following_remote_links():
    def labels(request):
        start = int(request.url.params["start"])
        result = [{"name": f"label-{start}", "prefix": "global"}] if start < 2 else []
        return httpx.Response(200, json={
            "results": result, "_links": {"next": "/next"} if start == 0 else {},
        })

    client, requests = label_client(labels)
    with ConfluenceConnector("https://wiki.example", token="fixture", client=client, page_size=2) as connector:
        batch = connector.sync(watermark="2026-10-03T00:00:00Z", correlation_id="metadata-acquisition")
        page = next(e for e in batch.events if e.metadata["record_kind"] == "page")
        assert connector.map_event(page)["source_metadata"]["labels"] == [
            {"name": "label-0", "prefix": "global"}, {"name": "label-1", "prefix": "global"},
        ]
        assert "history" in next(r.url.params["expand"] for r in requests if "/search" in r.url.path)
        label_requests = [r for r in requests if r.url.path.endswith("/label")]
        assert [r.url.path for r in label_requests] == ["/rest/api/content/42/label"] * 2
        assert [r.url.params["start"] for r in label_requests] == ["0", "1"]
        assert all(r.url.host == "wiki.example" for r in requests)
        assert all(r.headers["X-Correlation-ID"] == "metadata-acquisition" for r in requests)


@pytest.mark.parametrize("mode", ["invalid-shape", "empty-next", "repeated-page", "authentication", "label-limit"])
def test_label_acquisition_fails_explicitly_instead_of_emitting_partial_page(mode):
    def labels(_request):
        if mode == "authentication":
            return httpx.Response(401, json={})
        if mode == "invalid-shape":
            return httpx.Response(200, json={"results": {}})
        if mode == "label-limit":
            return httpx.Response(200, json={"results": [
                {"name": f"label-{i}", "prefix": "global"} for i in range(10_001)
            ]})
        return httpx.Response(200, json={
            "results": [] if mode == "empty-next" else [{"name": "repeat", "prefix": "global"}],
            "_links": {"next": "/more"},
        })

    client, _requests = label_client(labels)
    with ConfluenceConnector("https://wiki.example", token="fixture", client=client, page_size=2) as connector:
        with pytest.raises(ConnectorError) as error:
            connector.sync(watermark="2026-10-03T00:00:00Z", correlation_id="metadata-failure")
        assert error.value.category == ("authentication_failed" if mode == "authentication" else "invalid_response")
        assert error.value.correlation_id == "metadata-failure"
