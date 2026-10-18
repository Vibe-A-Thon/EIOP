"""Real HTTP admission and owner/scope isolation on persistent task memory."""

from eoip.agents.memory import MAX_TTL_SECONDS, FileMemoryStore


def test_task_memory_http_admission_and_scoped_deletion(live_replay):
    live = live_replay
    response = live.client.post("/api/v1/agents/TraceImpact/runs", json={"goal": "Check"})
    assert response.status_code == 200, response.text
    run_id = response.json()["run_id"]
    path = f"/api/v1/agents/runs/{run_id}/memory"
    store = FileMemoryStore(live.root)
    owner = live.get(f"/api/v1/agents/runs/{run_id}")["trace"]["actor_id"]
    try:
        assert live.client.get(path, headers={"Authorization": "Bearer invalid"}).status_code == 401
        persisted = live.get(path)
        assert persisted["ttl_seconds"] == MAX_TTL_SECONDS
        assert persisted["classification"] == "INTERNAL"
        assert store.get(run_id, scope="agent:TraceImpact", owner="foreign") is None
        assert not store.delete(run_id, scope="agent:Other", owner=owner)
        before = store.path.read_bytes()
        for ttl in (0, MAX_TTL_SECONDS + 1):
            refused = live.client.post("/api/v1/agents/TraceImpact/runs", json={
                "goal": "Check", "memory_ttl_seconds": ttl,
            })
            assert refused.status_code == 422, refused.text
        assert store.path.read_bytes() == before
        assert store.delete(run_id, scope="agent:TraceImpact", owner=owner)
        assert live.client.get(path).status_code == 404
        assert live.get(f"/api/v1/agents/runs/{run_id}")["trace"]["run_id"] == run_id
    finally:
        store.delete(run_id, scope="agent:TraceImpact", owner=owner)
