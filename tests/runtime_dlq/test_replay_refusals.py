import json
from uuid import uuid4

import httpx
from eoip.connectors.jira_json import JiraJsonConnector
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService
from eoip.jobs import write_json


def test_replay_refusals_do_not_enqueue_jobs(live_replay):
    live = live_replay
    service = JiraIngestionService(
        live.store, JiraJsonConnector(), FileEventCapture(live.root / "raw"), live.root / "dlq",
    )
    result = service.ingest({"issues": [{"key": "DLQ-303", "fields": {}}]})
    event_id = result["rejected"][0]["event_id"]
    endpoint = f"/api/v1/admin/dlq/{event_id}/replay"
    jobs_before = {p.name for p in (live.root / "jobs").glob("*.json")}
    vertices_before = live.store.count_vertices()
    for headers in ({}, {"Authorization": "Bearer invalid-acceptance-token"}):
        response = httpx.post(str(live.client.base_url).rstrip("/") + endpoint, headers=headers, trust_env=False)
        assert response.status_code == 401
    assert live.client.post(f"/api/v1/admin/dlq/{'f' * 64}/replay").status_code == 404
    raw = live.root / "raw" / "jira" / f"{event_id}.json"
    saved = raw.with_suffix(".saved")
    raw.rename(saved)
    try:
        assert live.client.post(endpoint).status_code == 409
    finally:
        saved.rename(raw)
    dlq = live.root / "dlq" / f"{event_id}.json"
    original = dlq.read_bytes()
    record = json.loads(original)
    record["payload_hash"] = "0" * 64
    write_json(dlq, record)
    correlation = f"dlq-refusal-{uuid4().hex}"
    try:
        response = live.client.post(endpoint, headers={"X-Correlation-ID": correlation})
        assert response.status_code == 409
    finally:
        dlq.write_bytes(original)
    assert {p.name for p in (live.root / "jobs").glob("*.json")} == jobs_before
    assert live.store.count_vertices() == vertices_before
    audits = live.get("/api/v1/admin/audit?limit=500")
    assert any(r["correlation_id"] == correlation and r["outcome"] == "failure" for r in audits)
