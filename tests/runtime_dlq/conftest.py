"""Opt-in API/worker tests; never connect to the primary demo."""

import json
import os
import time
from contextlib import contextmanager
from uuid import uuid4

import httpx
import pytest
from eoip.connectors.confluence import ConfluenceConnector
from eoip.connectors.sync import SyncBatch
from eoip.ingestion.jira import FileEventCapture
from eoip.ingestion.source_sync import SourceSyncIngestionService
from eoip.runtime import api_token, create_store, data_root


class LiveReplay:
    def __init__(self, client, store, root):
        self.client, self.store, self.root = client, store, root

    def get(self, path):
        response = self.client.get(path)
        response.raise_for_status()
        return response.json()

    def submit(self, path, document=None):
        correlation = f"dlq-acceptance-{uuid4().hex}"
        response = self.client.post(path, json=document, headers={"X-Correlation-ID": correlation})
        assert response.status_code == 202, response.text
        assert response.headers["X-Correlation-ID"] == correlation
        job = response.json()
        assert job["correlation_id"] == correlation
        return job

    def finish(self, submitted, expected):
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            job = self.get(f"/api/v1/admin/jobs/{submitted['job_id']}")
            if job["status"] in {"SUCCEEDED", "PARTIAL", "FAILED", "CANCELLED"}:
                assert job["status"] == expected, job
                persisted = json.loads(
                    (self.root / "jobs" / f"{job['job_id']}.json").read_text(encoding="utf-8")
                )
                assert persisted.get("result") == job.get("result")
                assert persisted["correlation_id"] == submitted["correlation_id"]
                return job
            time.sleep(0.5)
        raise AssertionError(f"Worker did not finish {submitted['job_id']}")

    def audit(self, job, outcome):
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            records = self.get("/api/v1/admin/audit?limit=500")
            matching = [r for r in records if r.get("job_id") == job["job_id"] and r["actor"] == "worker"]
            if matching:
                assert matching[-1]["correlation_id"] == job["correlation_id"]
                assert matching[-1]["outcome"] == outcome
                assert any(r["actor"] != "worker" and r["correlation_id"] == job["correlation_id"] for r in records)
                return
            time.sleep(0.2)
        raise AssertionError("Worker completion audit was not persisted")


@pytest.fixture(scope="session")
def live_replay():
    if os.getenv("EOIP_LIVE_DLQ_ACCEPTANCE") != "1":
        pytest.skip("Run scripts/container.ps1 dlq-acceptance for isolated live infrastructure")
    assert os.environ["EOIP_API_URL"] == "http://dlq-api:8000"
    assert os.environ["EOIP_HUGEGRAPH_URL"] == "http://dlq-graph:8080"
    assert os.environ["EOIP_LOAD_DEMO"] == "false"
    store = create_store()
    try:
        with httpx.Client(
            base_url=os.environ["EOIP_API_URL"],
            headers={"Authorization": f"Bearer {api_token()}"},
            timeout=30, trust_env=False,
        ) as client:
            response = client.get("/health/ready")
            assert response.status_code == 200 and response.json()["status"] == "ready"
            yield LiveReplay(client, store, data_root())
    finally:
        store.close()


class ObsoleteConfluenceMapper(ConfluenceConnector):
    def map_event(self, event):
        raise ValueError("obsolete mapper cannot read page title")


@contextmanager
def registered_http_source(live, source_type, upstream_url, mode, token_ref):
    run_id = uuid4().hex
    source_id = f"{source_type}-{run_id}"
    base_url = f"{upstream_url}/{run_id}/{mode}"
    response = live.client.post("/api/v1/sources", json={
        "source_id": source_id, "source_type": source_type,
        "name": "HTTP acquisition acceptance", "base_url": base_url,
        "capabilities": {"polling": True},
        "config": {"page_size": 1}, "secret_refs": {"token": token_ref},
    })
    assert response.status_code == 201, response.text
    try:
        with httpx.Client(base_url=base_url, timeout=15, trust_env=False) as upstream:
            yield source_id, upstream
    finally:
        response = live.client.delete(f"/api/v1/sources/{source_id}")
        assert response.status_code == 204, response.text


@pytest.fixture
def servicenow_source(live_replay):
    def register(*, mode="valid", token_ref="env://EOIP_ACCEPTANCE_SOURCE_TOKEN"):
        url = os.environ["EOIP_ACCEPTANCE_SOURCE_URL"]
        assert url == "http://dlq-upstream:8090"
        return registered_http_source(live_replay, "servicenow", url, mode, token_ref)
    return register


@pytest.fixture
def confluence_source(live_replay):
    def register(*, mode="valid", token_ref="env://EOIP_ACCEPTANCE_SOURCE_TOKEN"):
        url = os.environ["EOIP_ACCEPTANCE_CONFLUENCE_URL"]
        assert url == "http://dlq-confluence:8091"
        return registered_http_source(live_replay, "confluence", url, mode, token_ref)
    return register


@pytest.fixture
def registered_capture(live_replay):
    @contextmanager
    def seed(*, recoverable=False):
        live = live_replay
        source_id = f"confluence-{uuid4().hex}"
        response = live.client.post("/api/v1/sources", json={
            "source_id": source_id, "source_type": "confluence", "name": "Replay acceptance",
            "base_url": "http://unreachable.invalid", "secret_refs": {"token": "env://EOIP_API_TOKEN"},
        })
        assert response.status_code == 201, response.text
        assert live.get(f"/api/v1/sources/{source_id}")["source_id"] == source_id
        connector_class = ObsoleteConfluenceMapper if recoverable else ConfluenceConnector
        connector = connector_class("http://unreachable.invalid", token="acceptance-only")
        try:
            payload = {"id": uuid4().hex, "space": {"key": "ACCEPTANCE"},
                       "body": {"storage": {"value": "<p>Replay evidence</p>"}}}
            if recoverable:
                payload["title"] = "Recovered registered page"
            event = connector.make_event("page", f"{source_id}:page:{payload['id']}", payload, 1)
            # Registry ID deliberately differs from adapter instance hash.
            assert event.source_instance_id != source_id
            service = SourceSyncIngestionService(
                live.store, connector, FileEventCapture(live.root / "raw"),
                str(live.root / "dlq"), registry_source_id=source_id,
            )
            result = service.ingest(SyncBatch(events=[event], next_checkpoint=""))
            assert result["run_status"] == "PARTIAL" and result["records_rejected"] == 1
            yield source_id, event
        finally:
            connector.close()
            response = live.client.delete(f"/api/v1/sources/{source_id}")
            assert response.status_code == 204, response.text

    return seed
