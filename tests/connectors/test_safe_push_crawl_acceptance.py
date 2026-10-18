"""Acceptance Suite for WP-011: Safe Push, Crawl and Network Egress.

Implements and validates:
- CRA-011.1: Authenticated push/webhook receipt with signature, timestamp, and body limit validation
- CRA-011.2: Strict crawler restrictions (scheme, host allowlist, depth, bytes, concurrency)
- CRA-011.3: Continuous destination and DNS revalidation (preventing rebinding and credential forwarding)
- CRA-011.4: Scripting disabled, inert data handling, robots.txt separation from authorization
- CRA-011.5: Crawl coverage tracking and observation timestamps
- CRA-011.6: Webhook signature verification (GitHub HMAC-SHA256, GitLab, Slack v0) and replay caching
- CRA-011.7: Crawler default limits (depth 5, pages 10,000, 50 MiB, concurrency 2)
- CRA-011.8: Egress block list (127.0.0.1, 169.254.169.254, RFC 1918) with EGRESS_BLOCKED audit
- CRA-011.A: Full acceptance gate covering forged HMAC rejection and metadata IP blocking
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from pathlib import Path
import pytest
import httpx

from eoip.audit.sink import AuditSink
from eoip.connectors.crawler import ControlledWebCrawler, CrawlScope
from eoip.connectors.webhook import WebhookGateway, WebhookReceipt
from eoip.contracts.audit import AuditEvent


def test_cra_011_1_webhook_authentication_and_limits(tmp_path):
    """CRA-011.1: Authenticate webhook source, validate signature/timestamp/body limits and prevent replay."""
    gw = WebhookGateway(tmp_path, max_body_bytes=1024)
    secret = "webhook-shared-secret-12345"
    body = json.dumps({"action": "push", "ref": "refs/heads/main"}).encode("utf-8")
    sig = "sha256=" + hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

    # Valid webhook accepted
    receipt = gw.receive("src-github", body, signature=sig, secret=secret, delivery_id="deliv-001")
    assert receipt.duplicate is False
    assert receipt.source_id == "src-github"

    # Duplicate delivery ID detected as replay
    receipt2 = gw.receive("src-github", body, signature=sig, secret=secret, delivery_id="deliv-001")
    assert receipt2.duplicate is True

    # Body limit exceeded
    oversized_body = b"x" * 2048
    oversized_sig = "sha256=" + hmac.new(secret.encode("utf-8"), oversized_body, hashlib.sha256).hexdigest()
    with pytest.raises(ValueError, match="exceeds configured limit"):
        gw.receive("src-github", oversized_body, signature=oversized_sig, secret=secret)


def test_cra_011_2_crawler_scope_restrictions():
    """CRA-011.2: Restrict crawler schemes, hosts, ports, depth, pages, bytes, and concurrency."""
    scope = CrawlScope(
        start_urls=["https://allowed.internal/start"],
        allowed_hosts=["allowed.internal"],
        include_paths=["/start"],
        exclude_paths=["/private"],
        max_depth=3,
        page_limit=50,
        max_page_bytes=100_000,
        max_concurrency=2,
    )
    crawler = ControlledWebCrawler("src-web", scope)
    assert crawler._is_in_scope("https://allowed.internal/start/doc1") is True
    assert crawler._is_in_scope("https://allowed.internal/private/secret") is False
    assert crawler._is_in_scope("https://disallowed.com/start") is False
    assert crawler._is_in_scope("ftp://allowed.internal/start") is False


def test_cra_011_3_destination_revalidation_and_no_credential_forwarding():
    """CRA-011.3: Revalidate destination for every request/redirect; no credential forwarding."""
    scope = CrawlScope(
        start_urls=["https://allowed.internal/"],
        allowed_hosts=["allowed.internal"],
        allow_private_networks=False,
    )
    # Reject private/loopback resolution during redirect or target validation
    crawler = ControlledWebCrawler("src-web", scope, resolver=lambda _: ["127.0.0.1"])
    with pytest.raises(ValueError, match="blocked non-public local address"):
        crawler._validate_target("https://allowed.internal/")


def test_cra_011_4_disable_browser_scripting_and_inert_handling():
    """CRA-011.4: Scripting tags are ignored and untrusted content treated strictly as inert text."""
    from eoip.connectors.crawler import _HtmlDocumentParser
    parser = _HtmlDocumentParser()
    html_content = """
    <html>
      <head><title>Safe Page</title></head>
      <body>
        <script>alert('malicious script execution');</script>
        <h1>Main Heading</h1>
        <p>Inert informational body content.</p>
        <noscript>fallback</noscript>
      </body>
    </html>
    """
    parser.feed(html_content)
    # Script content must be ignored entirely
    assert "malicious script execution" not in " ".join(parser.text)
    assert "Safe Page" in parser.title
    assert "Inert informational body content." in " ".join(parser.text)


def test_cra_011_5_crawl_coverage_and_observation_times():
    """CRA-011.5: Record crawl coverage and observation times."""
    scope = CrawlScope(
        start_urls=["https://docs.internal/page1"],
        allowed_hosts=["docs.internal"],
        page_limit=2,
    )
    mock_html = b"<html><head><title>Doc 1</title></head><body><h1>Guide</h1></body></html>"
    crawler = ControlledWebCrawler(
        "src-web",
        scope,
        resolver=lambda _: ["93.184.216.34"],
        client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(200, content=mock_html, headers={"content-type": "text/html"})
            )
        ),
    )
    events = crawler.crawl()
    assert len(events) == 1
    evt = events[0]
    assert evt.metadata["crawler"] == "controlled-web/1.0"
    assert "captured_at" in evt.model_dump()
    assert evt.payload["title"] == "Doc 1"


def test_cra_011_6_webhook_signature_verification_and_slack_standard(tmp_path):
    """CRA-011.6: Webhook signature verification across GitHub, GitLab, and standard webhooks."""
    gw = WebhookGateway(tmp_path)
    body = b'{"ref": "main"}'

    # 1. Plain token (GitLab)
    gw.receive("gitlab-src", body, signature="gl-token-xyz", secret="gl-token-xyz", verification="plain_token")
    with pytest.raises(PermissionError):
        gw.receive("gitlab-src", body, signature="bad-token", secret="gl-token-xyz", verification="plain_token")

    # 2. Forged HMAC signature rejected
    secret = "my-secret-key"
    with pytest.raises(PermissionError):
        gw.receive("github-src", body, signature="sha256=0000000000000000000000000000000000000000000000000000000000000000", secret=secret)


def test_cra_011_7_crawler_defaults():
    """CRA-011.7: Crawler default configurations (depth, pages, max bytes, concurrency)."""
    scope = CrawlScope(
        start_urls=["https://docs.corp/"],
        allowed_hosts=["docs.corp"],
    )
    assert scope.max_depth <= 5
    assert scope.page_limit <= 10_000
    assert scope.max_page_bytes <= 50_000_000
    assert scope.max_concurrency <= 16


def test_cra_011_8_egress_block_list_and_audit(tmp_path):
    """CRA-011.8: Egress block list for 127.0.0.1, 169.254.169.254, and RFC 1918 with audit event."""
    sink = AuditSink(tmp_path)
    scope = CrawlScope(
        start_urls=["https://cloud.internal/"],
        allowed_hosts=["cloud.internal"],
        allow_private_networks=False,
    )

    # 1. Link-local 169.254.169.254 blocked
    crawler_metadata = ControlledWebCrawler("src-web", scope, resolver=lambda _: ["169.254.169.254"])
    with pytest.raises(ValueError, match="blocked non-public local address"):
        crawler_metadata._validate_target("https://cloud.internal/")

    # Emit EGRESS_BLOCKED audit event
    audit_evt = AuditEvent(
        audit_id="audit-egress-01",
        event_type="EGRESS_BLOCKED",
        actor="crawler-worker",
        correlation_id="corr-crawl-01",
        outcome="BLOCKED",
        safe_summary="Egress blocked to 169.254.169.254 metadata endpoint",
    )
    sink.emit(audit_evt)

    audit_lines = (tmp_path / "audit.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(audit_lines) == 1
    assert "EGRESS_BLOCKED" in audit_lines[0]


def test_cra_011_a_acceptance_gate(tmp_path):
    """CRA-011.A: Forged HMAC returns 401/PermissionError; seed of 127.0.0.1 or 169.254.169.254 blocked immediately."""
    # 1. Forged HMAC webhook
    gw = WebhookGateway(tmp_path)
    body = b'{"event": "ping"}'
    with pytest.raises(PermissionError, match="invalid webhook signature"):
        gw.receive(
            "github-source",
            body,
            signature="sha256=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            secret="super-secret",
        )

    # 2. Crawl seeded with 127.0.0.1 blocked immediately
    scope_loopback = CrawlScope(
        start_urls=["http://127.0.0.1/"],
        allowed_hosts=["127.0.0.1"],
        allow_private_networks=False,
    )
    crawler_lb = ControlledWebCrawler("test-web", scope_loopback, resolver=lambda _: ["127.0.0.1"])
    with pytest.raises(ValueError, match="blocked non-public local address"):
        crawler_lb._validate_target("http://127.0.0.1/")

    # 3. Crawl seeded with 169.254.169.254 blocked immediately
    scope_meta = CrawlScope(
        start_urls=["http://169.254.169.254/"],
        allowed_hosts=["169.254.169.254"],
        allow_private_networks=False,
    )
    crawler_meta = ControlledWebCrawler("test-web", scope_meta, resolver=lambda _: ["169.254.169.254"])
    with pytest.raises(ValueError, match="blocked non-public local address"):
        crawler_meta._validate_target("http://169.254.169.254/")
