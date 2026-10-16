import httpx
import pytest
from eoip.connectors.crawler import ControlledWebCrawler, CrawlScope


def make_crawler_client(handler):
    return httpx.Client(
        transport=httpx.MockTransport(handler),
        follow_redirects=False,
    )


@pytest.mark.req("G2-SRC-WEB-002")
def test_web_crawler_scope_and_allowlist_boundaries():
    scope = CrawlScope(
        start_urls=["https://docs.corp.internal/arch"],
        allowed_hosts=["docs.corp.internal"],
        include_paths=["/arch"],
        exclude_paths=["/arch/secret"],
    )
    # Outside allowed_hosts
    crawler = ControlledWebCrawler("web-1", scope, resolver=lambda _: ["93.184.216.34"])
    assert not crawler._is_in_scope("https://evil.external/arch")
    # Inside allowed_hosts and include_path
    assert crawler._is_in_scope("https://docs.corp.internal/arch/design")
    # In exclude_path
    assert not crawler._is_in_scope("https://docs.corp.internal/arch/secret/keys")


@pytest.mark.req("G2-SRC-WEB-003")
def test_web_crawler_html_structure_parsing():
    html_content = """<!DOCTYPE html>
    <html>
      <head><title>Architecture Overview</title></head>
      <body>
        <h1>Microservices Design</h1>
        <p>This document covers the core payment flow.</p>
        <a href="/arch/payments">Payments Service</a>
      </body>
    </html>"""

    def handler(request):
        return httpx.Response(200, text=html_content, headers={"content-type": "text/html"})

    scope = CrawlScope(
        start_urls=["https://docs.corp.internal/arch/overview"],
        allowed_hosts=["docs.corp.internal"],
        max_depth=0,
    )
    client = make_crawler_client(handler)
    crawler = ControlledWebCrawler(
        "web-doc",
        scope,
        resolver=lambda _: ["93.184.216.34"],
        client=client,
    )
    events = crawler.crawl()
    assert len(events) == 1
    event = events[0]
    assert event.payload["title"] == "Architecture Overview"
    assert "Microservices Design" in event.payload["headings"]
    assert "payment flow" in event.payload["text"]
    assert "https://docs.corp.internal/arch/payments" in event.payload["links"]


@pytest.mark.req("G2-SRC-WEB-004")
def test_web_crawler_politeness_delay_and_rate_limiting():
    sleep_calls = []
    current_time = [100.0]

    def fake_sleep(duration):
        sleep_calls.append(duration)
        current_time[0] += duration

    def fake_clock():
        return current_time[0]

    scope = CrawlScope(
        start_urls=["https://docs.corp.internal/arch/p1"],
        allowed_hosts=["docs.corp.internal"],
        politeness_delay_ms=500,
        rate_limit_per_minute=10,
    )
    crawler = ControlledWebCrawler(
        "web-throttled",
        scope,
        resolver=lambda _: ["93.184.216.34"],
        sleeper=fake_sleep,
        clock=fake_clock,
    )
    # Throttle first request
    crawler._throttle("https://docs.corp.internal/arch/p1")
    assert len(sleep_calls) == 0  # First request has no delay

    # Second request immediately afterwards to same host triggers politeness delay (500ms = 0.5s)
    crawler._throttle("https://docs.corp.internal/arch/p2")
    assert len(sleep_calls) == 1
    assert sleep_calls[0] == pytest.approx(0.5)


@pytest.mark.req("G2-SRC-WEB-005")
def test_web_crawler_content_hashing_and_event_version():
    def handler(request):
        return httpx.Response(200, text="<html><body>Static Content</body></html>", headers={"content-type": "text/html"})

    scope = CrawlScope(
        start_urls=["https://docs.corp.internal/arch/static"],
        allowed_hosts=["docs.corp.internal"],
        max_depth=0,
    )
    client = make_crawler_client(handler)
    crawler = ControlledWebCrawler(
        "web-hash",
        scope,
        resolver=lambda _: ["93.184.216.34"],
        client=client,
    )
    events = crawler.crawl()
    assert len(events) == 1
    event = events[0]
    assert event.source_system == "web"
    assert event.content_hash is not None
    assert event.source_version == event.content_hash
    assert event.operation == "UPSERT"
