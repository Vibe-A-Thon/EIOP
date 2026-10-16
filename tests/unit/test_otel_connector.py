import pytest
import eoip.connectors.otel as otel_module
from eoip.connectors.otel import OpenTelemetryConnector


@pytest.mark.req("G2-SRC-OTEL-002")
def test_otel_trace_span_extraction():
    connector = OpenTelemetryConnector(source_id="otel-prod")
    spans = [
        {
            "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
            "span_id": "00f067aa0ba902b7",
            "name": "HTTP GET /checkout",
            "service_name": "checkoutservice",
            "start_time": "2026-10-01T12:00:00Z",
            "end_time": "2026-10-01T12:00:00.250Z",
            "status": "OK",
            "attributes": {"http.status_code": 200, "service.name": "checkoutservice"},
        }
    ]
    events = connector.extract(spans=spans)
    assert len(events) == 1
    event = events[0]
    assert event.metadata["record_kind"] == "span"
    assert "4bf92f3577b34da6a3ce929d0e0e4736" in event.source_record_id
    assert event.payload["name"] == "HTTP GET /checkout"
    assert event.payload["service_name"] == "checkoutservice"


@pytest.mark.req("G2-SRC-OTEL-003")
def test_otel_metric_descriptor_and_datapoint_ingestion():
    connector = OpenTelemetryConnector(source_id="otel-prod")
    metrics = [
        {
            "name": "http_requests_total",
            "type": "counter",
            "value": 1420,
            "unit": "requests",
            "timestamp": "2026-10-01T12:05:00Z",
            "attributes": {"handler": "checkout", "code": "200"},
        }
    ]
    events = connector.extract(metrics=metrics)
    assert len(events) == 1
    event = events[0]
    assert event.metadata["record_kind"] == "metric"
    assert "http_requests_total" in event.source_record_id
    assert event.payload["value"] == 1420
    assert event.payload["unit"] == "requests"


@pytest.mark.req("G2-SRC-OTEL-004")
def test_otel_graceful_handling_when_sdk_missing(monkeypatch):
    monkeypatch.setattr(otel_module, "_OTEL_AVAILABLE", False)
    connector = OpenTelemetryConnector(source_id="otel-missing")

    health = connector.health()
    assert health.status == "UNAVAILABLE"
    assert "not installed" in health.detail

    with pytest.raises(ImportError, match="opentelemetry-sdk is required"):
        connector.extract(spans=[{"span_id": "1"}])


@pytest.mark.req("G2-SRC-OTEL-005")
def test_otel_checkpoint_and_healthy_status():
    connector = OpenTelemetryConnector(source_id="otel-cluster", endpoint="http://otel-collector:4317")
    assert connector.checkpoint() is None

    health = connector.health()
    assert health.status == "HEALTHY"
    assert "available" in health.detail.lower()

    discovery = connector.discover()
    assert discovery.source_id == "otel-cluster"
    res_ids = [r.resource_id for r in discovery.resources]
    assert "traces" in res_ids
    assert "metrics" in res_ids
