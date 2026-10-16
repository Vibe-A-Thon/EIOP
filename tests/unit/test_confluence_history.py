import json

import httpx
import pytest
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.sync import SyncBatch
from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.source_sync import SourceSyncIngestionService


def version(number):
    return {
        "number": number, "when": f"2026-10-0{number}T02:00:00.123+02:00",
        "by": {"userKey": f"editor-{number}", "email": "not-projected@example.test"},
        "message": f"Revision {number}", "minorEdit": False,
    }


def client_for_history(response=None, number=3):
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path.endswith("/space"):
            return httpx.Response(200, json={"results": [{"key": "ENG", "name": "Engineering"}]})
        if request.url.path.endswith("/content/42"):
            if response:
                return response(request)
            n = int(request.url.params["version"])
            return httpx.Response(200, json={"id": "42", "version": version(n)})
        if "type = attachment" in request.url.params.get("cql", ""):
            return httpx.Response(200, json={"results": []})
        return httpx.Response(200, json={"results": [{
            "id": "42", "title": "Deploy", "space": {"key": "ENG"},
            "version": version(number) if number <= 3 else {"number": number},
            "body": {"storage": {"value": "<p>Deploy</p>"}},
            "_links": {"self": "https://untrusted.example/never-follow"},
        }]})

    return httpx.Client(transport=httpx.MockTransport(handler)), requests


@pytest.mark.req("G2-SRC-CONF-002", "G2-T0403")
def test_public_historical_content_is_captured_projected_and_replayed_offline(tmp_path):
    client, requests = client_for_history()
    with ConfluenceConnector("https://wiki.example/wiki", token="fixture", client=client) as connector:
        batch = connector.sync(correlation_id="history-correlation")
        page = next(e for e in batch.events if e.metadata["record_kind"] == "page")
        assert page.payload["version_history"] == {
            "complete": True, "results": [version(n) for n in (3, 2, 1)],
        }
        historical = [r for r in requests if r.url.path.endswith("/content/42")]
        assert [dict(r.url.params) for r in historical] == [
            {"status": "historical", "version": str(n), "expand": "version"} for n in (2, 1)
        ]
        assert all(r.url.host == "wiki.example" for r in requests)
        assert all(r.headers["x-correlation-id"] == "history-correlation" for r in requests)
        expected = {
            "schema_version": "1.0", "complete": True,
            "revisions": [{
                "number": n, "modified_at": f"2026-10-0{n}T00:00:00.123000Z",
                "editor": {"user_key": f"editor-{n}"}, "message": f"Revision {n}",
                "minor_edit": False,
                "source_ref": f"https://wiki.example/wiki/rest/api/content/42?status=historical&version={n}",
            } for n in (3, 2, 1)],
        }
        assert connector.map_event(page)["source_history"] == expected
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq"),
        )
        assert service.ingest(batch)["run_status"] == "SUCCEEDED"
        cid = f"urn:eoip:knowledge:document:{page.source_record_id}"
        document = store.get_vertex_by_canonical_id(cid)
        assert json.loads(document["properties"]["payload_json"])["source_history"] == expected
        raw_path = tmp_path / "raw" / "confluence" / f"{page.event_id}.json"
        captured = raw_path.read_bytes()
        request_count = len(requests)
        assert service.ingest(SyncBatch([page], page.captured_at))["run_status"] == "SUCCEEDED"
        assert len(requests) == request_count
        assert raw_path.read_bytes() == captured
        assert len(store.find_vertices(label="EntityRevision", filters={"subject_id": cid})) == 1


@pytest.mark.req("G2-SRC-CONF-002")
@pytest.mark.parametrize(("response", "category"), [
    (lambda r: httpx.Response(403), "authentication_failed"),
    (lambda r: httpx.Response(404), "remote_error"),
    (lambda r: httpx.Response(200, json={"id": "other", "version": version(2)}), "invalid_response"),
    (lambda r: httpx.Response(200, json={"id": "42", "version": version(3)}), "invalid_response"),
    (lambda r: httpx.Response(200, json={"id": "42", "version": []}), "invalid_response"),
])
def test_incomplete_or_mismatched_history_fails_acquisition(response, category):
    client, _requests = client_for_history(response)
    with ConfluenceConnector("https://wiki.example/wiki", token="fixture", client=client) as connector:
        with pytest.raises(ConnectorError) as error:
            connector.sync(correlation_id="history-refusal")
        assert error.value.category == category
        assert error.value.correlation_id == "history-refusal"


@pytest.mark.req("G2-SRC-CONF-002")
def test_history_limit_refuses_before_historical_requests():
    client, requests = client_for_history(number=1001)
    with (
        ConfluenceConnector("https://wiki.example/wiki", token="fixture", client=client) as connector,
        pytest.raises(ConnectorError),
    ):
        connector.sync()
    assert not any(r.url.path.endswith("/content/42") for r in requests)


@pytest.mark.req("G2-SRC-CONF-002")
@pytest.mark.parametrize("number", [True, 2.0])
def test_noninteger_current_version_refuses_before_historical_requests(number):
    client, requests = client_for_history(number=number)
    with (
        ConfluenceConnector("https://wiki.example/wiki", token="fixture", client=client) as connector,
        pytest.raises(ConnectorError),
    ):
        connector.sync()
    assert not any(r.url.path.endswith("/content/42") for r in requests)


@pytest.mark.req("G2-SRC-CONF-002")
def test_complete_history_must_agree_with_current_version_metadata():
    with ConfluenceConnector("https://wiki.example/wiki", token="fixture") as connector:
        payload = {
            "id": "42", "title": "Deploy", "space": {"key": "ENG"}, "version": version(2),
            "version_history": {"complete": True, "results": [version(2), version(1)]},
        }
        payload["version_history"]["results"][0]["message"] = "Different capture"
        event = connector.make_event("page", f"{connector.instance_id}:page:42", payload, 2)
        with pytest.raises(ValueError, match="current"):
            connector.map_event(event)


@pytest.mark.req("G2-SRC-CONF-002", "FR-CONN-006")
def test_old_captures_report_partial_history_and_invalid_complete_history_enters_dlq(tmp_path):
    with ConfluenceConnector("https://wiki.example/wiki", token="fixture") as connector:
        payload = {"id": "42", "title": "Deploy", "space": {"key": "ENG"}, "version": version(3)}
        event = connector.make_event("page", f"{connector.instance_id}:page:42", payload, 3)
        history = connector.map_event(event)["source_history"]
        assert history["complete"] is False
        assert [v["number"] for v in history["revisions"]] == [3]
        payload["version_history"] = {"complete": True, "results": [version(3), version(1)]}
        invalid = connector.make_event("page", event.source_record_id, payload, 3)
        store = MemoryGraphStore()
        service = SourceSyncIngestionService(
            store, connector, FileEventCapture(tmp_path / "raw"), str(tmp_path / "dlq"),
        )
        result = service.ingest(SyncBatch([invalid], invalid.captured_at))
        assert result["run_status"] == "PARTIAL" and result["records_rejected"] == 1
        assert store.count_vertices("Document") == 0
        assert len(list((tmp_path / "dlq").rglob("*.json"))) == 1
