"""Real HTTP task memory expires without deleting its durable run trace."""

import time

from eoip.agents.memory import FileMemoryStore


def test_task_memory_http_persistence_expiry_and_trace_survival(live_replay):
    live = live_replay
    response = live.client.post("/api/v1/agents/TraceImpact/runs", json={
        "goal": "Check a nonexistent entity", "context_refs": ["urn:memory:absent"],
        "memory_ttl_seconds": 3,
    })
    assert response.status_code == 200, response.text
    run_id = response.json()["run_id"]
    path = f"/api/v1/agents/runs/{run_id}/memory"
    store = FileMemoryStore(live.root)
    try:
        assert live.client.get(path, headers={"Authorization": ""}).status_code == 401
        recovered = live.get(path)
        persisted = store.get(run_id, scope="agent:TraceImpact", owner="local-user")
        assert persisted.model_dump() == recovered
        assert recovered["ttl_seconds"] == 3
        assert recovered["content"]["status"] == response.json()["status"]
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            expired = live.client.get(path)
            if expired.status_code == 404:
                break
            assert expired.status_code == 200, expired.text
            time.sleep(0.2)
        else:
            raise AssertionError("Task memory remained readable beyond its TTL")
        assert store.get(run_id, scope="agent:TraceImpact", owner="local-user") is None
        assert live.get(f"/api/v1/agents/runs/{run_id}")["trace"]["run_id"] == run_id
        assert live.store.get_vertex_by_canonical_id(f"urn:eoip:agent:run:{run_id}") is not None
    finally:
        store.delete(run_id, scope="agent:TraceImpact", owner="local-user")
