import json
from uuid import uuid4

import httpx
import pytest
from eoip.ingestion.replay import logical_graph_output, logical_output_diff


@pytest.mark.req("FR-SNOW-001", "G2-T0112")
def test_servicenow_fetched_rejection_and_admission_controls(live_replay, servicenow_source):
    live = live_replay
    with servicenow_source(mode="rejected") as (source_id, upstream):
        baseline = live.finish(live.submit(f"/api/v1/sources/{source_id}/baseline", {}), "PARTIAL")
        result = baseline["result"]
        assert (result["records_seen"], result["records_accepted"], result["records_rejected"]) == (5, 4, 1)
        event_id = result["rejected"][0]["event_id"]
        raw = live.root / "raw" / "servicenow" / f"{event_id}.json"
        dlq = live.root / "dlq" / f"{event_id}.json"
        original = raw.read_bytes(), dlq.read_bytes()
        record = json.loads(original[1])
        assert record["registry_source_id"] == source_id and record["error_category"] == "mapping_error"
        assert not (live.root / "state" / "connectors" / f"{source_id}.json").exists()
        endpoint = f"/api/v1/admin/dlq/{event_id}/replay"
        before = logical_graph_output(live.store)
        jobs = {p.name for p in (live.root / "jobs").glob("*.json")}
        correlations = []

        def refuse(status):
            correlation = f"sn-refusal-{uuid4().hex}"
            response = live.client.post(endpoint, headers={"X-Correlation-ID": correlation})
            assert response.status_code == status, response.text
            correlations.append((correlation, "denied" if status == 422 else "failure"))
            assert {p.name for p in (live.root / "jobs").glob("*.json")} == jobs
            assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]

        for headers in ({}, {"Authorization": "Bearer invalid-fixture-token"}):
            response = httpx.post(str(live.client.base_url).rstrip("/") + endpoint,
                                  headers=headers, trust_env=False)
            assert response.status_code == 401
        assert live.client.post(f"/api/v1/sources/{source_id}/pause").status_code == 200
        refuse(409)
        assert live.client.post(f"/api/v1/sources/{source_id}/resume").status_code == 200
        assert live.client.patch(f"/api/v1/sources/{source_id}", json={"enabled": False}).status_code == 200
        refuse(409)
        assert live.client.patch(f"/api/v1/sources/{source_id}", json={
            "enabled": True, "capabilities": {"replay": False},
        }).status_code == 200
        refuse(422)
        assert live.client.patch(f"/api/v1/sources/{source_id}", json={"capabilities": {"replay": True}}).status_code == 200
        assert live.client.put(f"/api/v1/sources/{source_id}/schedule", json={
            "max_concurrency": 1, "rate_limit_per_minute": 1,
        }).status_code == 200
        refuse(409)
        assert live.client.put(f"/api/v1/sources/{source_id}/schedule", json={
            "max_concurrency": 1, "rate_limit_per_minute": 120,
        }).status_code == 200
        replay = live.finish(live.submit(endpoint), "PARTIAL")
        assert replay["result"]["records_accepted"] == 0 and replay["result"]["records_rejected"] == 1
        assert (raw.read_bytes(), dlq.read_bytes()) == original
        assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
        assert len(upstream.get("/requests").json()) == 9
        audits = live.get("/api/v1/admin/audit?limit=500")
        assert all(any(a["correlation_id"] == c and a["outcome"] == outcome for a in audits)
                   for c, outcome in correlations)
        live.audit(baseline, "partial")
        live.audit(replay, "partial")
