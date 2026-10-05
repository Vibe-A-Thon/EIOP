"""Tests for eoip.observability.metrics (GAP-OBS-003)."""

import pytest

pytestmark = pytest.mark.req("GAP-OBS-003")


@pytest.fixture
def registry():
    from eoip.observability.metrics import Registry

    return Registry()


def test_counter_increments(registry):
    counter = registry.counter("hits", "Total hits.", ("route",))
    counter.inc(route="/a")
    counter.inc(route="/a")
    counter.inc(route="/b")
    assert counter.get(route="/a") == 2
    assert counter.get(route="/b") == 1


def test_counter_rejects_negative(registry):
    counter = registry.counter("hits", "Total hits.")
    with pytest.raises(ValueError):
        counter.inc(-1)


def test_gauge_set_inc_dec(registry):
    gauge = registry.gauge("temperature", "Current temperature.")
    gauge.set(10)
    gauge.inc(5)
    gauge.dec(3)
    assert gauge.get() == 12


def test_histogram_buckets_and_sum(registry):
    histogram = registry.histogram("latency", "Latency.", buckets=(0.1, 0.5, 1.0))
    histogram.observe(0.05)
    histogram.observe(0.7)
    text = histogram.render()
    assert 'le="0.1"} 1' in text
    assert 'le="0.5"} 1' in text
    assert 'le="1"} 2' in text
    assert 'le="+Inf"} 2' in text
    assert "latency_sum 0.75" in text
    assert "latency_count 2" in text


def test_render_prometheus_format(registry):
    registry.counter("events", "Events.")
    registry.gauge("load", "Load.")
    text = registry.render()
    assert "# HELP events Events." in text
    assert "# TYPE events counter" in text
    assert "# TYPE load gauge" in text
    assert text.endswith("\n")


def test_register_duplicate_rejected(registry):
    registry.counter("dup", "First.")
    with pytest.raises(ValueError):
        registry.counter("dup", "Second.")


def test_record_request_creates_and_reuses_families(registry):
    from eoip.observability.metrics import record_request

    record_request(registry, method="GET", path="/x", status=200, duration_seconds=0.01)
    record_request(registry, method="GET", path="/x", status=200, duration_seconds=0.02)
    counter = registry.get("http_requests_total")
    assert counter.get(method="GET", path="/x", status="200") == 2
    histogram = registry.get("http_request_duration_seconds")
    assert histogram is not None


def test_timed_request_records_duration(registry):
    from eoip.observability.metrics import timed_request

    with timed_request(registry, method="POST", path="/y", status=201):
        pass
    counter = registry.get("http_requests_total")
    assert counter.get(method="POST", path="/y", status="201") == 1


def test_timed_request_marks_exception_as_500(registry):
    from eoip.observability.metrics import timed_request

    with pytest.raises(RuntimeError), timed_request(registry, method="GET", path="/z"):
        raise RuntimeError("boom")
    counter = registry.get("http_requests_total")
    assert counter.get(method="GET", path="/z", status="500") == 1


def test_label_escaping(registry):
    counter = registry.counter("quoted", "Help.", ("v",))
    counter.inc(v='a"b\\c\nd')
    assert 'v="a\\"b\\\\c\\nd"' in counter.render()
