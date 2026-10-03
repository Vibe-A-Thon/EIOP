from http.server import ThreadingHTTPServer
from threading import Thread
from uuid import uuid4

import pytest
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.errors import ConnectorError

from tests.runtime_dlq.confluence_upstream import ConfluenceAPIHandler


@pytest.fixture
def confluence_url(monkeypatch):
    monkeypatch.setenv("EOIP_ACCEPTANCE_SOURCE_TOKEN", "fixture-only-valid")
    monkeypatch.setattr(ConfluenceAPIHandler, "requests", {})
    server = ThreadingHTTPServer(("127.0.0.1", 0), ConfluenceAPIHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/{uuid4().hex}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
        assert not thread.is_alive()


@pytest.mark.req("FR-CONF-001")
def test_confluence_fixture_pagination_and_incremental_overlap(confluence_url):
    with ConfluenceConnector(confluence_url + "/valid", token="fixture-only-valid", page_size=1) as connector:
        baseline = connector.sync(watermark="2026-10-01T00:00:00Z", correlation_id="fixture-baseline")
        assert [connector.map_event(e)["kind"] for e in baseline.events] == [
            "space", "page", "page", "attachment",
        ]
        requests = next(iter(ConfluenceAPIHandler.requests.values()))
        assert len(requests) == 15
        for event in baseline.events:
            if event.metadata["record_kind"] == "page":
                metadata = connector.map_event(event)["source_metadata"]
                assert metadata["labels"] == [
                    {"name": "deploy", "prefix": "global"},
                    {"name": "runbook", "prefix": "global"},
                    {"name": "operations", "prefix": "team"},
                ]
                assert metadata["author"]["user_key"] == "author-key"
                assert metadata["editor"]["user_key"] == "editor-key"
        assert all(r["authorized"] and r["correlation_id"] == "fixture-baseline" for r in requests)
        overlap = connector.sync(checkpoint=baseline.next_checkpoint, watermark="2026-10-01T00:01:00Z")
        assert [e.event_id for e in overlap.events] == [e.event_id for e in baseline.events]
        incremental = connector.sync(checkpoint="2026-10-03T00:00:00Z", watermark="2026-10-03T01:00:00Z")
        assert [e.metadata["record_kind"] for e in incremental.events] == ["space"]
        assert connector.sync(watermark="2026-09-30T23:59:00Z").events[0].metadata["record_kind"] == "space"
        assert len(connector.sync(watermark="2026-09-30T23:59:00Z").events) == 1


def test_confluence_fixture_mapping_rejection(confluence_url):
    with ConfluenceConnector(confluence_url + "/rejected", token="fixture-only-valid", page_size=1) as connector:
        batch = connector.sync(watermark="2026-10-03T00:00:00Z")
        invalid = [e for e in batch.events if e.metadata["record_kind"] == "page" and "title" not in e.payload]
        assert len(invalid) == 1 and invalid[0].payload["id"]
        with pytest.raises(ValueError, match="page title"):
            connector.map_event(invalid[0])


@pytest.mark.parametrize(("mode", "token", "category"), [
    ("valid", "fixture-only-invalid", "authentication_failed"),
    ("schema-drift", "fixture-only-valid", "schema_drift"),
    ("invalid-response", "fixture-only-valid", "invalid_response"),
    ("label-invalid", "fixture-only-valid", "invalid_response"),
])
def test_confluence_fixture_categorizes_acquisition_failures(confluence_url, mode, token, category):
    with ConfluenceConnector(f"{confluence_url}/{mode}", token=token, page_size=1) as connector:
        with pytest.raises(ConnectorError) as exc:
            connector.sync(correlation_id="fixture-failure")
        assert exc.value.category == category and exc.value.correlation_id == "fixture-failure"
        assert all(r["correlation_id"] == "fixture-failure"
                   for r in next(iter(ConfluenceAPIHandler.requests.values())))
