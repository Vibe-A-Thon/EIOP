from http.server import ThreadingHTTPServer
from threading import Thread
from uuid import uuid4

import pytest
from eoip.connectors.jira import ConnectorError
from eoip.connectors.servicenow import ServiceNowConnector

from tests.runtime_dlq.servicenow_upstream import TableAPIHandler


@pytest.fixture
def upstream_url(monkeypatch):
    monkeypatch.setenv("EOIP_ACCEPTANCE_SOURCE_TOKEN", "fixture-only-valid")
    monkeypatch.setattr(TableAPIHandler, "requests", {})
    server = ThreadingHTTPServer(("127.0.0.1", 0), TableAPIHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/{uuid4().hex}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
        assert not thread.is_alive()


@pytest.mark.req("FR-SNOW-001")
def test_fixture_paginates_and_filters_incremental_queries(upstream_url):
    with ServiceNowConnector(upstream_url + "/valid", token="fixture-only-valid", page_size=1) as connector:
        batch = connector.sync(watermark="2026-10-03T00:00:00Z", correlation_id="fixture-check")
        assert len(batch.events) == 5
        assert {connector.map_event(event)["kind"] for event in batch.events} == {
            "incident", "problem", "change", "knowledge",
        }
        assert len(next(iter(TableAPIHandler.requests.values()))) == 9
        assert all(request["correlation_id"] == "fixture-check"
                   for request in next(iter(TableAPIHandler.requests.values())))
        assert connector.sync(checkpoint=batch.next_checkpoint, watermark="2026-10-03T01:00:00Z").events == []


def test_fixture_returns_genuine_mapping_rejection(upstream_url):
    with ServiceNowConnector(upstream_url + "/rejected", token="fixture-only-valid", page_size=1) as connector:
        batch = connector.sync(watermark="2026-10-03T00:00:00Z")
        invalid = [event for event in batch.events if "number" not in event.payload]
        assert len(invalid) == 1 and invalid[0].payload["sys_id"]
        with pytest.raises(ValueError, match="requires number"):
            connector.map_event(invalid[0])


def test_fixture_refuses_wrong_upstream_token(upstream_url):
    with ServiceNowConnector(upstream_url + "/valid", token="fixture-only-invalid") as connector:
        with pytest.raises(ConnectorError) as exc:
            connector.sync(correlation_id="fixture-denied")
        assert exc.value.category == "authentication_failed"
        assert len(next(iter(TableAPIHandler.requests.values()))) == 1
        assert next(iter(TableAPIHandler.requests.values()))[0]["correlation_id"] == "fixture-denied"
