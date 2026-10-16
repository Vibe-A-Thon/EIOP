import httpx
import pytest
from eoip.connectors.errors import ConnectorError
from eoip.connectors.servicenow import ServiceNowConnector


def make_mock_client(handler):
    return httpx.Client(
        base_url="https://snow.internal",
        transport=httpx.MockTransport(handler),
    )


@pytest.mark.req("CONN-02", "FR-SNOW-001")
def test_servicenow_offline_fixtures():
    def handler(request):
        return httpx.Response(200, json={"result": [{"sys_id": "s1", "number": "INC100"}]})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client, page_size=10)
    batch = connector.sync(watermark="2026-10-10 12:00:00")
    assert len(batch.events) >= 1
    assert batch.next_checkpoint == "2026-10-10T12:00:00Z"


@pytest.mark.req("G2-SRC-SNOW-002")
def test_servicenow_incident_extraction():
    records = [{"sys_id": "inc-01", "number": "INC0001", "short_description": "Network latency", "state": "2"}]
    def handler(request):
        if "incident" in request.url.path:
            return httpx.Response(200, json={"result": records})
        return httpx.Response(200, json={"result": []})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client, tables={"incident": "incident"})
    batch = connector.sync(watermark="2026-10-10 12:00:00")
    assert len(batch.events) == 1
    mapped = connector.map_event(batch.events[0])
    assert mapped["kind"] == "incident"
    assert mapped["record_id"] == "inc-01"
    assert mapped["number"] == "INC0001"
    assert mapped["short_description"] == "Network latency"


@pytest.mark.req("G2-SRC-SNOW-003")
def test_servicenow_problem_extraction():
    records = [{"sys_id": "prb-01", "number": "PRB0001", "short_description": "Root cause outage"}]
    def handler(request):
        if "problem" in request.url.path:
            return httpx.Response(200, json={"result": records})
        return httpx.Response(200, json={"result": []})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client, tables={"problem": "problem"})
    batch = connector.sync(watermark="2026-10-10 12:00:00")
    assert len(batch.events) == 1
    mapped = connector.map_event(batch.events[0])
    assert mapped["kind"] == "problem"
    assert mapped["record_id"] == "prb-01"
    assert mapped["short_description"] == "Root cause outage"


@pytest.mark.req("G2-SRC-SNOW-004")
def test_servicenow_change_request_extraction():
    records = [{"sys_id": "chg-01", "number": "CHG0001", "short_description": "Database migration", "state": "approved"}]
    def handler(request):
        if "change_request" in request.url.path:
            return httpx.Response(200, json={"result": records})
        return httpx.Response(200, json={"result": []})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client, tables={"change": "change_request"})
    batch = connector.sync(watermark="2026-10-10 12:00:00")
    assert len(batch.events) == 1
    mapped = connector.map_event(batch.events[0])
    assert mapped["kind"] == "change"
    assert mapped["record_id"] == "chg-01"
    assert mapped["number"] == "CHG0001"


@pytest.mark.req("G2-SRC-SNOW-005")
def test_servicenow_pagination_and_watermarks():
    incident_offsets = []
    def handler(request):
        offset = int(request.url.params["sysparm_offset"])
        if "incident" in request.url.path:
            incident_offsets.append(offset)
            if offset == 0:
                return httpx.Response(200, json={"result": [{"sys_id": "i1", "number": "INC1"}]})
        return httpx.Response(200, json={"result": []})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client, page_size=1)
    batch = connector.sync(checkpoint="2026-10-01 00:00:00", watermark="2026-10-02 00:00:00")
    assert incident_offsets == [0, 1]
    assert batch.next_checkpoint == "2026-10-02T00:00:00Z"


@pytest.mark.req("G2-SRC-SNOW-006")
def test_servicenow_schema_drift():
    def handler(request):
        return httpx.Response(200, json={"result": [{"short_description": "Missing sys_id"}]})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client)
    with pytest.raises(ConnectorError) as exc_info:
        connector.sync(watermark="2026-10-02 00:00:00")
    assert exc_info.value.category == "schema_drift"


@pytest.mark.req("G2-SRC-SNKB-002")
def test_servicenow_kb_article_extraction():
    records = [{"sys_id": "kb-01", "number": "KB0001", "short_description": "How to rotate certs", "text": "Step 1..."}]
    def handler(request):
        if "kb_knowledge" in request.url.path:
            return httpx.Response(200, json={"result": records})
        return httpx.Response(200, json={"result": []})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client)
    batch = connector.sync(watermark="2026-10-10 12:00:00")
    assert len(batch.events) == 1
    mapped = connector.map_event(batch.events[0])
    assert mapped["kind"] == "knowledge"
    assert mapped["record_id"] == "kb-01"
    assert mapped["short_description"] == "How to rotate certs"


@pytest.mark.req("G2-SRC-SNKB-003")
def test_servicenow_kb_metadata_and_version():
    records = [{"sys_id": "kb-02", "number": "KB0002", "short_description": "FAQ", "sys_updated_on": "2026-10-05 10:00:00"}]
    def handler(request):
        if "kb_knowledge" in request.url.path:
            return httpx.Response(200, json={"result": records})
        return httpx.Response(200, json={"result": []})

    client = make_mock_client(handler)
    connector = ServiceNowConnector("https://snow.internal", token="mock-token", client=client, page_size=10)
    batch = connector.sync(watermark="2026-10-10 12:00:00")
    assert len(batch.events) == 1
    event = batch.events[0]
    assert event.source_record_id.endswith(":kb-02")
    assert event.source_version == "2026-10-05 10:00:00"
    assert event.metadata["record_kind"] == "knowledge"
