import httpx
import pytest
from eoip.connectors.config import connector_from_environment
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.errors import ConnectorError
from eoip.connectors.servicenow import ServiceNowConnector


def make_client(handler):
    return httpx.Client(
        base_url="https://eoip-test.local",
        transport=httpx.MockTransport(handler),
    )


@pytest.mark.req("FR-CONF-001")
def test_confluence_sync_emits_spaces_pages_and_attachment_metadata_incrementally():
    requests = []
    responses = {
        "/rest/api/space": {
            "results": [{"key": "ENG", "name": "Engineering", "description": "Docs"}],
            "size": 1,
        },
        "/rest/api/content/search": {
            "results": [
                {
                    "id": "42",
                    "type": "page",
                    "title": "Release process",
                    "space": {"key": "ENG"},
                    "version": {"number": 7, "when": "2026-10-02T10:00:00.000Z"},
                    "body": {"storage": {"value": "<p>Deploy safely</p>"}},
                    "_links": {"webui": "/pages/42"},
                }
            ],
            "size": 1,
        },
    }

    def handler(request):
        requests.append(request)
        if request.url.path.endswith("/content/42"):
            return httpx.Response(200, json={
                "id": "42", "version": {"number": int(request.url.params["version"])},
            })
        if request.url.path.endswith("/rest/api/content/search"):
            query = request.url.params["cql"]
            if "type = attachment" in query:
                return httpx.Response(
                    200,
                    json={
                        "results": [
                            {
                                "id": "84",
                                "type": "attachment",
                                "title": "diagram.png",
                                "space": {"key": "ENG"},
                                "container": {"id": "42"},
                                "version": {"number": 2},
                                "extensions": {"mediaType": "image/png", "fileSize": 1234},
                            }
                        ],
                        "size": 1,
                    },
                )
        return httpx.Response(200, json=responses[request.url.path])

    client = make_client(handler)
    connector = ConfluenceConnector("https://eoip-test.local", token="test-token", client=client)

    batch = connector.sync(checkpoint="2026-10-01T00:00:00Z", watermark="2026-10-02T12:00:00Z")

    assert [event.metadata["record_kind"] for event in batch.events] == [
        "space",
        "page",
        "attachment",
    ]
    mapped = [connector.map_event(event) for event in batch.events]
    assert mapped[0] == {"kind": "space", "space_key": "ENG", "name": "Engineering", "description": "Docs"}
    assert mapped[1]["content_id"] == "42"
    assert mapped[1]["body"] == "<p>Deploy safely</p>"
    assert mapped[2]["page_id"] == "42"
    assert mapped[2]["media_type"] == "image/png"
    assert batch.next_checkpoint == "2026-10-02T12:00:00Z"
    assert all(request.headers["authorization"] == "Bearer test-token" for request in requests)
    page_query = next(
        request.url.params["cql"]
        for request in requests
        if request.url.path.endswith("/content/search")
        and "type = page" in request.url.params["cql"]
    )
    assert 'lastModified >= "2026-09-30 23:58"' in page_query
    assert 'lastModified <= "2026-10-02 12:00"' in page_query


@pytest.mark.req("FR-CONF-001")
def test_confluence_pagination_and_event_identity_are_stable():
    pages = []

    def handler(request):
        if request.url.path.endswith("/rest/api/space"):
            spaces = [{"key": "OPS", "name": "Operations"}] if int(request.url.params["start"]) == 0 else []
            return httpx.Response(200, json={"results": spaces, "size": len(spaces)})
        if request.url.params.get("cql", "").find("type = page") >= 0:
            start = int(request.url.params["start"])
            pages.append(start)
            result = (
                [{"id": "1", "type": "page", "title": "One", "space": {"key": "OPS"}, "version": {"number": 1}}]
                if start == 0
                else [{"id": "2", "type": "page", "title": "Two", "space": {"key": "OPS"}, "version": {"number": 1}}]
                if start == 1
                else []
            )
            return httpx.Response(200, json={"results": result, "size": len(result)})
        return httpx.Response(200, json={"results": [], "size": 0})

    client = make_client(handler)
    connector = ConfluenceConnector(
        "https://eoip-test.local",
        token="test-token",
        client=client,
        page_size=1,
    )
    first = connector.sync(watermark="2026-10-02T12:00:00Z")
    second = connector.sync(watermark="2026-10-02T12:00:00Z")

    assert pages[:3] == [0, 1, 2]
    page_events = [event for event in first.events if event.metadata["record_kind"] == "page"]
    repeated_events = [event for event in second.events if event.metadata["record_kind"] == "page"]
    assert len(page_events) == 2
    assert [event.event_id for event in page_events] == [event.event_id for event in repeated_events]


@pytest.mark.req("FR-SNOW-001")
def test_servicenow_sync_paginates_supported_tables_and_maps_records():
    requests = []
    rows = {
        "incident": [{"sys_id": "i-1", "number": "INC001", "short_description": "Login failure"}],
        "problem": [{"sys_id": "p-1", "number": "PRB001", "short_description": "Auth outage"}],
        "change_request": [{"sys_id": "c-1", "number": "CHG001", "short_description": "Rotate key"}],
        "kb_knowledge": [{"sys_id": "k-1", "number": "KB001", "short_description": "Reset password"}],
    }

    def handler(request):
        requests.append(request)
        table = request.url.path.rsplit("/", 1)[-1]
        start = int(request.url.params["sysparm_offset"])
        return httpx.Response(
            200,
            json={"result": rows[table][start : start + int(request.url.params["sysparm_limit"])]},
        )

    client = make_client(handler)
    connector = ServiceNowConnector(
        "https://eoip-test.local",
        token="test-token",
        client=client,
        page_size=1,
    )

    batch = connector.sync(checkpoint="2026-10-01 00:00:00", watermark="2026-10-02 12:00:00")

    assert [event.metadata["record_kind"] for event in batch.events] == [
        "incident",
        "problem",
        "change",
        "knowledge",
    ]
    assert connector.map_event(batch.events[0]) == {
        "kind": "incident",
        "record_id": "i-1",
        "number": "INC001",
        "short_description": "Login failure",
        "description": None,
        "state": None,
        "updated_at": None,
    }
    assert batch.next_checkpoint == "2026-10-02T12:00:00Z"
    assert all(request.headers["authorization"] == "Bearer test-token" for request in requests)
    assert all("sys_updated_on>=2026-10-01 00:00:00" in request.url.params["sysparm_query"] for request in requests)
    assert all("sys_updated_on<=2026-10-02 12:00:00" in request.url.params["sysparm_query"] for request in requests)


@pytest.mark.req("FR-SNOW-001")
def test_servicenow_rejects_schema_drift_without_dropping_raw_record():
    client = make_client(
        lambda request: httpx.Response(
            200,
            json={"result": [{"number": "INC001", "short_description": "Missing sys_id"}]},
        )
    )
    connector = ServiceNowConnector(
        "https://eoip-test.local",
        token="test-token",
        client=client,
        tables={"incident": "incident"},
    )
    with pytest.raises(ConnectorError) as exc_info:
        connector.sync(watermark="2026-10-02 12:00:00")
    assert exc_info.value.category == "schema_drift"
    assert exc_info.value.source_system == "servicenow"


@pytest.mark.req("FR-CONN-005")
def test_connector_errors_use_stable_categories_without_exposing_credentials():
    client = make_client(lambda request: httpx.Response(429, json={"error": "too many requests"}))
    connector = ServiceNowConnector(
        "https://eoip-test.local",
        token="never-log-this-secret",
        client=client,
        tables={"incident": "incident"},
    )

    with pytest.raises(ConnectorError) as exc_info:
        connector.sync(correlation_id="corr-1", watermark="2026-10-02 12:00:00")

    assert exc_info.value.category == "rate_limited"
    assert exc_info.value.correlation_id == "corr-1"
    assert "never-log-this-secret" not in str(exc_info.value)


@pytest.mark.req("FR-CONF-001")
def test_environment_configuration_rejects_missing_auth_without_echoing_secrets():
    with pytest.raises(ConnectorError) as exc_info:
        connector_from_environment(
            "confluence",
            correlation_id="corr-config",
            environ={"EOIP_CONFLUENCE_URL": "https://eoip-test.local"},
        )

    assert exc_info.value.category == "configuration_error"
    assert exc_info.value.correlation_id == "corr-config"
    assert "configuration_error" in str(exc_info.value)
