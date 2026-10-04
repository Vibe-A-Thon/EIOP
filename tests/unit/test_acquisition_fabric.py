from __future__ import annotations

import hashlib
import hmac
import json
import time
from base64 import b64encode

import httpx
import pytest
from eoip.connectors.acquisition import AcquisitionPolicy, AcquisitionScheduler, BaselineController
from eoip.connectors.base import DiscoveryScope, SourceConnector
from eoip.connectors.crawler import ControlledWebCrawler, CrawlScope
from eoip.connectors.generic import LocalFileConnector, LocalFileScope, WebSourceConnector
from eoip.connectors.registry import SourceRegistry
from eoip.connectors.webhook import WebhookGateway
from eoip.contracts.source_registry import SourceRegistryEntry
from eoip.jobs import JobQueue


def _source(source_id: str = "confluence-prod") -> SourceRegistryEntry:
    return SourceRegistryEntry(
        source_id=source_id,
        source_type="confluence",
        name="Production Confluence",
        base_url="https://confluence.example.test",
        capabilities={"polling": True, "reconciliation": True, "replay": True},
        secret_refs={"token": "env://EOIP_CONFLUENCE_PROD_TOKEN"},
    )


@pytest.mark.req("G2-T0110", "G2-T0111", "G2-T0112")
def test_scheduler_admits_all_operation_types_and_enforces_controls(tmp_path) -> None:
    registry = SourceRegistry(tmp_path / "state" / "source-registry.json")
    registry.create(_source())
    queue = JobQueue(tmp_path)
    scheduler = AcquisitionScheduler(tmp_path, registry, queue)
    scheduler.set_policy(
        "confluence-prod", AcquisitionPolicy(max_concurrency=4, rate_limit_per_minute=4)
    )

    for operation, event_ids in [
        ("BASELINE", None),
        ("POLL", None),
        ("RECONCILE", None),
        ("REPLAY", ["a" * 64]),
    ]:
        result = scheduler.submit("confluence-prod", operation, event_ids=event_ids)
        job = queue.get(result["job_id"])
        assert job["payload"]["source_id"] == "confluence-prod"
        assert job["payload"]["operation"] == operation

    with pytest.raises(RuntimeError, match="concurrency"):
        scheduler.submit("confluence-prod", "POLL")
    scheduler.pause("confluence-prod")
    assert scheduler.policy("confluence-prod").paused is True
    with pytest.raises(RuntimeError, match="paused"):
        scheduler.submit("confluence-prod", "POLL")
    scheduler.resume("confluence-prod")
    assert scheduler.policy("confluence-prod").paused is False


@pytest.mark.req("G2-T0201", "G2-T0202", "G2-T0203")
def test_baseline_controller_persists_ordered_restart_manifest(tmp_path) -> None:
    path = tmp_path / "baseline.json"
    controller = BaselineController(path, "jira-prod", {"mapping_version": "jira/2.0"})
    for stage in ("DISCOVERING", "FETCHING", "MAPPING", "VALIDATING", "MUTATING", "VERIFYING"):
        controller.transition(stage)
    complete = controller.transition(
        "COMPLETE", checkpoint="cursor-1000", counts={"accepted": 1000}, failures=[]
    )

    resumed = BaselineController(path, "jira-prod").read()
    assert resumed == complete
    assert resumed["checkpoint"] == "cursor-1000"
    assert [item["stage"] for item in resumed["history"]] == list(BaselineController._ORDER)


@pytest.mark.req("G2-T0120", "G2-T0121", "G2-T0122")
def test_webhook_gateway_authenticates_persists_and_deduplicates_before_processing(tmp_path) -> None:
    gateway = WebhookGateway(tmp_path)
    body = json.dumps({"event": "issue_updated", "id": "EOIP-1"}).encode()
    secret = "local-test-secret"
    signature = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

    first = gateway.receive(
        "jira-prod",
        body,
        signature=signature,
        secret=secret,
        delivery_id="delivery-1",
    )
    repeated = gateway.receive(
        "jira-prod",
        body,
        signature=signature,
        secret=secret,
        delivery_id="delivery-1",
    )

    assert first.duplicate is False
    assert repeated.duplicate is True
    persisted = json.loads(next((tmp_path / "receipts" / "jira-prod").glob("*.json")).read_text())
    assert persisted["payload"]["id"] == "EOIP-1"
    assert len(list((tmp_path / "receipts" / "jira-prod").glob("*.json"))) == 1

    with pytest.raises(PermissionError):
        gateway.receive("jira-prod", body, signature="sha256=" + "0" * 64, secret=secret)


@pytest.mark.req("G2-T0130", "G2-T0131", "G2-T0132", "G2-T0133", "G2-T0134", "G2-T0135")
def test_controlled_crawler_extracts_deduplicated_allowlisted_pages_and_blocks_redirect_escape() -> None:
    pages = {
        "/docs": '<html><head><title>EOIP Docs</title></head><body><h1>Guide</h1><a href="/docs/setup#top">Setup</a><a href="/private">Private</a></body></html>',
        "/docs/setup": "<html><body><h2>Setup</h2><p>Install locally.</p></body></html>",
    }

    def handler(request):
        if request.url.path == "/docs/escape":
            return httpx.Response(302, headers={"Location": "http://127.0.0.1/admin"})
        return httpx.Response(200, text=pages[request.url.path], headers={"Content-Type": "text/html"})

    scope = CrawlScope(
        start_urls=["https://docs.example.test/docs"],
        allowed_hosts=["docs.example.test"],
        include_paths=["/docs"],
        exclude_paths=["/docs/private"],
        max_depth=2,
        page_limit=10,
    )
    client = httpx.Client(transport=httpx.MockTransport(handler))
    crawler = ControlledWebCrawler(
        "docs-prod", scope, client=client, resolver=lambda _host: ["93.184.216.34"]
    )

    events = crawler.crawl()

    assert [event.source_record_id for event in events] == [
        "https://docs.example.test/docs",
        "https://docs.example.test/docs/setup",
    ]
    assert events[0].payload["title"] == "EOIP Docs"
    assert events[1].payload["headings"] == ["Setup"]
    assert events[0].content_hash == events[0].payload_hash

    escaping = ControlledWebCrawler(
        "docs-prod",
        scope.model_copy(update={"start_urls": ["https://docs.example.test/docs/escape"]}),
        client=client,
        resolver=lambda _host: ["93.184.216.34"],
    )
    with pytest.raises(ValueError, match="outside|non-public"):
        escaping.crawl()


@pytest.mark.req("G2-SEC-CRAWL-001", "G2-SEC-CRAWL-002")
def test_controlled_crawler_rejects_private_dns_resolution() -> None:
    scope = CrawlScope(
        start_urls=["https://docs.example.test/docs"],
        allowed_hosts=["docs.example.test"],
    )
    crawler = ControlledWebCrawler(
        "docs-prod",
        scope,
        client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(200))),
        resolver=lambda _host: ["127.0.0.1"],
    )
    with pytest.raises(ValueError, match="non-public"):
        crawler.crawl()


@pytest.mark.req("G2-SRC-WEB-002", "G2-SEC-CRAWL-002")
def test_controlled_crawler_can_authorize_private_intranet_targets_explicitly() -> None:
    scope = CrawlScope(
        start_urls=["https://docs.example.test/docs"],
        allowed_hosts=["docs.example.test"],
        allow_private_networks=True,
        max_depth=0,
    )
    crawler = ControlledWebCrawler(
        "docs-prod",
        scope,
        client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    200, text="<html><body>Internal docs</body></html>",
                    headers={"Content-Type": "text/html"},
                )
            )
        ),
        resolver=lambda _host: ["10.10.10.10"],
    )

    events = crawler.crawl()

    assert len(events) == 1
    assert events[0].source_record_id == "https://docs.example.test/docs"


@pytest.mark.req("G2-EKAF-019")
def test_controlled_crawler_enforces_rate_and_politeness_controls() -> None:
    pages = {
        "/docs": '<html><body><a href="/docs/setup">Setup</a></body></html>',
        "/docs/setup": "<html><body>Setup</body></html>",
    }
    requests = []

    def handler(request):
        requests.append(str(request.url))
        return httpx.Response(
            200,
            text=pages[request.url.path],
            headers={"Content-Type": "text/html"},
        )

    now = [100.0]
    sleeps: list[float] = []

    def sleeper(seconds: float) -> None:
        sleeps.append(seconds)
        now[0] += seconds

    scope = CrawlScope(
        start_urls=["https://docs.example.test/docs"],
        allowed_hosts=["docs.example.test"],
        include_paths=["/docs"],
        max_depth=1,
        page_limit=2,
        rate_limit_per_minute=1,
        politeness_delay_ms=500,
        max_concurrency=2,
    )
    crawler = ControlledWebCrawler(
        "docs-prod",
        scope,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        resolver=lambda _host: ["93.184.216.34"],
        sleeper=sleeper,
        clock=lambda: now[0],
    )

    events = crawler.crawl()

    assert len(events) == 2
    assert requests == [
        "https://docs.example.test/docs",
        "https://docs.example.test/docs/setup",
    ]
    assert sleeps and sleeps[0] == pytest.approx(60.0)
    assert events[0].metadata["rate_limit_per_minute"] == 1
    assert events[0].metadata["politeness_delay_ms"] == 500
    assert events[0].metadata["max_concurrency"] == 2

    polite_now = [200.0]
    polite_sleeps: list[float] = []

    def polite_sleep(seconds: float) -> None:
        polite_sleeps.append(seconds)
        polite_now[0] += seconds

    polite_crawler = ControlledWebCrawler(
        "docs-prod",
        scope.model_copy(update={"rate_limit_per_minute": 60}),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        resolver=lambda _host: ["93.184.216.34"],
        sleeper=polite_sleep,
        clock=lambda: polite_now[0],
    )

    polite_crawler.crawl()

    assert polite_sleeps[0] == pytest.approx(0.5)


@pytest.mark.req("G2-EKAF-001", "G2-T0340", "G2-T0341")
def test_generic_web_and_file_connectors_share_source_connector_semantics(tmp_path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("# Local guide\nEvidence first.", encoding="utf-8")
    file_connector = LocalFileConnector(
        "files-prod", LocalFileScope(roots=[str(docs)], suffixes=[".md"])
    )
    web_client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                text="<html><title>Guide</title><body>Evidence first.</body></html>",
                headers={"Content-Type": "text/html"},
            )
        )
    )
    web_connector = WebSourceConnector(
        "web-prod",
        ControlledWebCrawler(
            "web-prod",
            CrawlScope(
                start_urls=["https://docs.example.test/guide"],
                allowed_hosts=["docs.example.test"],
                max_depth=0,
            ),
            client=web_client,
            resolver=lambda _host: ["93.184.216.34"],
        ),
    )

    for connector in (file_connector, web_connector):
        assert isinstance(connector, SourceConnector)
        assert connector.discover(DiscoveryScope()).resources
        events = list(connector.baseline())
        assert len(events) == 1
        assert events[0].schema_version == "2.0"
        assert events[0].content_hash == events[0].payload_hash


@pytest.mark.req("G2-T0110")
def test_source_operation_api_queues_registry_scoped_job(monkeypatch, tmp_path) -> None:
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    from apps.api import main as api_main

    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    client = TestClient(api_main.create_app())
    headers = {"Authorization": "Bearer " + "x" * 32}
    created = client.post("/api/v1/sources", json=_source().model_dump(mode="json"), headers=headers)
    assert created.status_code == 201
    policy = client.put(
        "/api/v1/sources/confluence-prod/schedule",
        json={"max_concurrency": 4, "rate_limit_per_minute": 60, "paused": False},
        headers=headers,
    )
    assert policy.status_code == 200

    response = client.post(
        "/api/v1/sources/confluence-prod/baseline",
        json={"dry_run": True},
        headers=headers,
    )
    assert response.status_code == 202
    job = JobQueue(tmp_path).get(response.json()["job_id"])
    assert job["kind"] == "SOURCE_OPERATION"
    assert job["payload"] == {
        "source_id": "confluence-prod",
        "operation": "BASELINE",
        "checkpoint": None,
        "event_ids": [],
        "dry_run": True,
    }

    dry_run = client.post(
        "/api/v1/sources/confluence-prod/dry-run",
        json={},
        headers=headers,
    )
    assert dry_run.status_code == 202
    dry_run_job = JobQueue(tmp_path).get(dry_run.json()["job_id"])
    assert dry_run_job["payload"]["operation"] == "BASELINE"
    assert dry_run_job["payload"]["dry_run"] is True

    checkpoint = client.get("/api/v1/sources/confluence-prod/checkpoint", headers=headers)
    assert checkpoint.status_code == 200
    assert checkpoint.json()["source_id"] == "confluence-prod"


@pytest.mark.req("G2-T0120", "G2-T0121", "G2-T0123")
def test_webhook_api_uses_source_hmac_and_queues_only_new_delivery(monkeypatch, tmp_path) -> None:
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    from apps.api import main as api_main

    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    monkeypatch.setenv("EOIP_JIRA_WEBHOOK_SECRET", "webhook-test-secret")
    client = TestClient(api_main.create_app())
    auth = {"Authorization": "Bearer " + "x" * 32}
    source = SourceRegistryEntry(
        source_id="jira-webhook",
        source_type="jira",
        name="Jira Webhooks",
        base_url="https://jira.example.test",
        capabilities={"webhooks": True},
        secret_refs={"webhook_hmac": "env://EOIP_JIRA_WEBHOOK_SECRET"},
    )
    assert client.post("/api/v1/sources", json=source.model_dump(mode="json"), headers=auth).status_code == 201
    body = json.dumps(
        {"issue": {"key": "EOIP-1", "fields": {"summary": "Webhook issue"}}}
    ).encode()
    signature = "sha256=" + hmac.new(b"webhook-test-secret", body, hashlib.sha256).hexdigest()
    headers = {"X-EOIP-Signature": signature, "X-EOIP-Delivery": "delivery-9"}

    first = client.post("/api/v1/sources/jira-webhook/webhooks", content=body, headers=headers)
    duplicate = client.post("/api/v1/sources/jira-webhook/webhooks", content=body, headers=headers)
    denied = client.post(
        "/api/v1/sources/jira-webhook/webhooks",
        content=body,
        headers={"X-EOIP-Signature": "sha256=" + "0" * 64},
    )

    assert first.status_code == duplicate.status_code == 202
    assert first.json()["job_id"]
    assert duplicate.json()["duplicate"] is True
    assert "job_id" not in duplicate.json()
    assert denied.status_code == 401
    assert len(JobQueue(tmp_path).list()) == 1


@pytest.mark.req("G2-SRC-GH-002")
def test_webhook_api_accepts_native_github_signature_delivery_and_event_headers(
    monkeypatch, tmp_path
) -> None:
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    from apps.api import main as api_main

    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    monkeypatch.setenv("EOIP_GITHUB_WEBHOOK_SECRET", "github-secret")
    client = TestClient(api_main.create_app())
    auth = {"Authorization": "Bearer " + "x" * 32}
    source = SourceRegistryEntry(
        source_id="github-prod",
        source_type="github",
        name="GitHub",
        base_url="https://api.github.com",
        capabilities={"webhooks": True},
        config={"repositories": ["acme/app"]},
        secret_refs={
            "token": "env://EOIP_GITHUB_TOKEN",
            "webhook_hmac": "env://EOIP_GITHUB_WEBHOOK_SECRET",
        },
    )
    assert client.post("/api/v1/sources", json=source.model_dump(mode="json"), headers=auth).status_code == 201
    body = json.dumps(
        {
            "action": "opened",
            "repository": {"full_name": "acme/app"},
            "pull_request": {"id": 7, "number": 7, "title": "Feature"},
        }
    ).encode()
    signature = "sha256=" + hmac.new(b"github-secret", body, hashlib.sha256).hexdigest()

    response = client.post(
        "/api/v1/sources/github-prod/webhooks",
        content=body,
        headers={
            "X-Hub-Signature-256": signature,
            "X-GitHub-Delivery": "delivery-gh-1",
            "X-GitHub-Event": "pull_request",
        },
    )

    assert response.status_code == 202
    receipt = json.loads(next((tmp_path / "receipts" / "github-prod").glob("*.json")).read_text())
    assert receipt["metadata"]["event_name"] == "pull_request"


@pytest.mark.req("G2-SRC-GL-002")
def test_webhook_api_accepts_gitlab_standard_signature_and_rejects_stale_delivery(
    monkeypatch, tmp_path
) -> None:
    from eoip.graph.memory import MemoryGraphStore
    from fastapi.testclient import TestClient

    from apps.api import main as api_main

    monkeypatch.setattr(api_main, "api_token", lambda: "x" * 32)
    monkeypatch.setattr(api_main, "create_store", MemoryGraphStore)
    monkeypatch.setattr(api_main, "data_root", lambda: tmp_path)
    raw_key = b"gitlab-signing-key"
    signing_token = "whsec_" + b64encode(raw_key).decode()
    monkeypatch.setenv("EOIP_GITLAB_WEBHOOK_SIGNING", signing_token)
    client = TestClient(api_main.create_app())
    auth = {"Authorization": "Bearer " + "x" * 32}
    source = SourceRegistryEntry(
        source_id="gitlab-prod",
        source_type="gitlab",
        name="GitLab",
        base_url="https://gitlab.example/api/v4",
        capabilities={"webhooks": True},
        config={"projects": ["acme/app"]},
        secret_refs={
            "token": "env://EOIP_GITLAB_TOKEN",
            "webhook_signing": "env://EOIP_GITLAB_WEBHOOK_SIGNING",
        },
    )
    assert client.post("/api/v1/sources", json=source.model_dump(mode="json"), headers=auth).status_code == 201
    body = json.dumps(
        {
            "object_kind": "merge_request",
            "project": {"path_with_namespace": "acme/app"},
            "object_attributes": {"id": 7, "iid": 7, "title": "Feature"},
        }
    ).encode()
    delivery_id = "delivery-gl-1"
    timestamp = str(int(time.time()))
    message = delivery_id.encode() + b"." + timestamp.encode() + b"." + body
    signature = "v1," + b64encode(hmac.new(raw_key, message, hashlib.sha256).digest()).decode()
    headers = {
        "webhook-id": delivery_id,
        "webhook-timestamp": timestamp,
        "webhook-signature": signature,
        "X-Gitlab-Event": "Merge Request Hook",
    }

    response = client.post(
        "/api/v1/sources/gitlab-prod/webhooks",
        content=body,
        headers=headers,
    )
    stale_timestamp = str(int(timestamp) - 1000)
    stale_message = delivery_id.encode() + b"." + stale_timestamp.encode() + b"." + body
    stale_signature = "v1," + b64encode(
        hmac.new(raw_key, stale_message, hashlib.sha256).digest()
    ).decode()
    stale = client.post(
        "/api/v1/sources/gitlab-prod/webhooks",
        content=body,
        headers={
            **headers,
            "webhook-id": "delivery-gl-stale",
            "webhook-timestamp": stale_timestamp,
            "webhook-signature": stale_signature,
        },
    )

    assert response.status_code == 202
    assert stale.status_code == 401
    receipt = json.loads(next((tmp_path / "receipts" / "gitlab-prod").glob("*.json")).read_text())
    assert receipt["metadata"]["event_name"] == "Merge Request Hook"
