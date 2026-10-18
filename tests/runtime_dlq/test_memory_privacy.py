"""Real HTTP memory excludes raw task text and fails closed on corrupt storage."""

import json
from uuid import uuid4

from eoip.agents.memory import FileMemoryStore


def test_task_memory_http_minimization_and_corruption_refusal(live_replay):
    live = live_replay
    marker = f"private-body-{uuid4().hex}"
    response = live.client.post("/api/v1/agents/TraceImpact/runs", json={
        "goal": marker, "context_refs": ["urn:memory:absent"],
    })
    assert response.status_code == 200, response.text
    run_id = response.json()["run_id"]
    path = f"/api/v1/agents/runs/{run_id}/memory"
    store = FileMemoryStore(live.root)
    owner = live.get(f"/api/v1/agents/runs/{run_id}")["trace"]["actor_id"]
    original = store.path.read_bytes()
    try:
        assert live.client.get(path, headers={"Authorization": ""}).status_code == 401
        memory = live.get(path)
        assert marker not in original.decode("utf-8")
        assert set(memory["content"]) == {"status", "evidence_count"}
        assert memory["provenance_refs"] == [f"urn:eoip:agent:run:{run_id}"]
        payload = json.loads(original)
        item = next(item for item in payload["records"] if item["memory_id"] == run_id)
        item["content"]["prompt"] = marker
        store.path.write_text(json.dumps(payload), encoding="utf-8")
        refused = live.client.get(path)
        assert refused.status_code == 503, refused.text
        assert refused.json()["detail"] == "Task memory storage is unavailable"
    finally:
        store.path.write_bytes(original)
        store.delete(run_id, scope="agent:TraceImpact", owner=owner)
    assert live.client.get(path).status_code == 404
    assert live.get(f"/api/v1/agents/runs/{run_id}")["trace"]["run_id"] == run_id
