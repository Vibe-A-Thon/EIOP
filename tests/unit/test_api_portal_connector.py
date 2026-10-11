import httpx
import pytest
from eoip.connectors.api_portal import APIPortalConnector
from eoip.connectors.errors import ConnectorError


def make_portal_client(handler):
    return httpx.Client(
        base_url="https://portal.internal",
        transport=httpx.MockTransport(handler),
    )


def mock_portal_responses(request):
    path = request.url.path
    if path == "/api/v1/services":
        page = int(request.url.params.get("page", 1))
        if page == 1:
            return httpx.Response(200, json={
                "services": [
                    {
                        "id": "svc-payments",
                        "name": "Payments API",
                        "version": "v2.1",
                        "swagger_url": "https://portal.internal/specs/payments.json",
                        "updated_at": "2026-10-01T12:00:00Z"
                    }
                ],
                "total": 1,
            })
        return httpx.Response(200, json={"services": [], "total": 1})
    if path == "/api/v1/services/svc-payments/endpoints":
        return httpx.Response(200, json={
            "endpoints": [
                {
                    "id": "ep-charge",
                    "path": "/v2/charge",
                    "method": "POST",
                    "version": "v2.1",
                    "swagger_url": "https://portal.internal/specs/payments.json#/paths/~1charge",
                    "updated_at": "2026-10-01T12:00:00Z"
                }
            ]
        })
    return httpx.Response(404, json={"error": "not found"})


@pytest.mark.req("G2-SRC-API-002")
def test_api_portal_service_catalog_discovery():
    client = make_portal_client(mock_portal_responses)
    connector = APIPortalConnector("https://portal.internal", token="mock-token", client=client, page_size=10)
    batch = connector.sync(watermark="2026-10-02T00:00:00Z")
    service_events = [e for e in batch.events if e.metadata["record_kind"] == "service"]
    assert len(service_events) == 1
    assert "svc-payments" in service_events[0].source_record_id
    assert service_events[0].payload["name"] == "Payments API"


@pytest.mark.req("G2-SRC-API-003")
def test_api_portal_endpoint_extraction_and_mapping():
    client = make_portal_client(mock_portal_responses)
    connector = APIPortalConnector("https://portal.internal", token="mock-token", client=client)
    batch = connector.sync(watermark="2026-10-02T00:00:00Z")
    ep_events = [e for e in batch.events if e.metadata["record_kind"] == "endpoint"]
    assert len(ep_events) == 1
    assert "ep-charge" in ep_events[0].source_record_id
    mapped = connector.map_event(ep_events[0])
    assert mapped["kind"] == "endpoint"
    assert mapped["service_id"] == "svc-payments"
    assert mapped["api_name"] == "/v2/charge"


@pytest.mark.req("G2-SRC-API-004")
def test_api_portal_swagger_openapi_url_metadata():
    client = make_portal_client(mock_portal_responses)
    connector = APIPortalConnector("https://portal.internal", token="mock-token", client=client)
    batch = connector.sync(watermark="2026-10-02T00:00:00Z")
    service_event = next(e for e in batch.events if e.metadata["record_kind"] == "service")
    mapped = connector.map_event(service_event)
    assert mapped["swagger_url"] == "https://portal.internal/specs/payments.json"
    assert mapped["api_version"] == "v2.1"


@pytest.mark.req("G2-SRC-API-005")
def test_api_portal_checkpoint_and_watermark_sync():
    client = make_portal_client(mock_portal_responses)
    connector = APIPortalConnector("https://portal.internal", token="mock-token", client=client)
    batch = connector.sync(checkpoint="2026-10-01T00:00:00Z", watermark="2026-10-02T12:00:00Z")
    assert batch.next_checkpoint == "2026-10-02T12:00:00Z"
    assert len(batch.events) == 2  # 1 service + 1 endpoint


@pytest.mark.req("G2-SRC-API-006")
def test_api_portal_schema_drift_and_error_handling():
    def handler(request):
        # Service missing 'id' or 'service_id' triggers schema_drift
        return httpx.Response(200, json={"services": [{"name": "Missing ID Service"}], "total": 1})

    client = make_portal_client(handler)
    connector = APIPortalConnector("https://portal.internal", token="mock-token", client=client)
    with pytest.raises(ConnectorError) as exc_info:
        connector.sync(watermark="2026-10-02T00:00:00Z")
    assert exc_info.value.category == "schema_drift"
