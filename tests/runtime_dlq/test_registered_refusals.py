import json
from uuid import uuid4

from eoip.jobs import write_json


def test_registered_v2_registry_refusals_enqueue_nothing(live_replay, registered_capture):
    live = live_replay
    with registered_capture() as (_source_id, event):
        dlq = live.root / "dlq" / f"{event.event_id}.json"
        original = dlq.read_bytes()
        record = json.loads(original)
        jobs = {path.name for path in (live.root / "jobs").glob("*.json")}
        vertices = live.store.count_vertices()
        wrong_id = f"wrong-{uuid4().hex}"
        response = live.client.post("/api/v1/sources", json={
            "source_id": wrong_id, "source_type": "servicenow",
            "name": "Wrong replay adapter", "base_url": "http://unreachable.invalid",
        })
        assert response.status_code == 201, response.text
        try:
            for registry_id in [f"missing-{uuid4().hex}", wrong_id]:
                record["registry_source_id"] = registry_id
                write_json(dlq, record)
                correlation = f"v2-refusal-{uuid4().hex}"
                response = live.client.post(f"/api/v1/admin/dlq/{event.event_id}/replay",
                                           headers={"X-Correlation-ID": correlation})
                assert response.status_code == 409, response.text
                assert any(item["correlation_id"] == correlation and item["outcome"] == "failure"
                           for item in live.get("/api/v1/admin/audit?limit=500"))
        finally:
            dlq.write_bytes(original)
            assert live.client.delete(f"/api/v1/sources/{wrong_id}").status_code == 204
        assert {path.name for path in (live.root / "jobs").glob("*.json")} == jobs
        assert live.store.count_vertices() == vertices
