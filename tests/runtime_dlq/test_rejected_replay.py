def test_worker_rejection_and_replay_remain_partial(live_replay):
    live = live_replay
    submitted = live.submit(
        "/api/v1/admin/ingestion/jira",
        {"document": {"issues": [{"key": "DLQ-101", "fields": {}}]}},
    )
    job = live.finish(submitted, "PARTIAL")
    assert job["result"]["records_rejected"] == 1
    assert job["result"]["records_accepted"] == 0
    event_id = job["result"]["rejected"][0]["event_id"]
    record = next(r for r in live.get("/api/v1/admin/dlq") if r["event_id"] == event_id)
    assert record["stage"] == "mapping" and record["error_category"] == "mapping_error"
    assert record["run_id"] == job["result"]["run_id"]
    raw = live.root / "raw" / "jira" / f"{event_id}.json"
    captured = raw.read_bytes()
    replay = live.finish(live.submit(f"/api/v1/admin/dlq/{event_id}/replay"), "PARTIAL")
    assert replay["result"]["records_replayed"] == 0
    assert replay["result"]["logical_diff"]["equivalent"]
    assert raw.read_bytes() == captured
    assert live.store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:DLQ-101") is None
    assert any(r["event_id"] == event_id for r in live.get("/api/v1/admin/dlq"))
    live.audit(job, "partial")
    live.audit(replay, "partial")
