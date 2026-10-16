import json


def test_registered_v2_invalid_replay_remains_partial(live_replay, registered_capture):
    live = live_replay
    with registered_capture() as (source_id, event):
        raw = live.root / "raw" / "confluence" / f"{event.event_id}.json"
        dlq = live.root / "dlq" / f"{event.event_id}.json"
        original = raw.read_bytes(), dlq.read_bytes()
        assert json.loads(original[0])["schema_version"] == "2.0"
        assert json.loads(original[1])["registry_source_id"] == source_id
        job = live.finish(live.submit(f"/api/v1/admin/dlq/{event.event_id}/replay"), "PARTIAL")
        persisted = json.loads((live.root / "jobs" / f"{job['job_id']}.json").read_text())
        assert persisted["kind"] == "SOURCE_OPERATION"
        assert persisted["payload"]["source_id"] == source_id
        assert persisted["payload"]["operation"] == "REPLAY"
        assert job["result"]["records_accepted"] == 0
        assert job["result"]["records_rejected"] == 1
        assert live.store.get_vertex_by_canonical_id(
            f"urn:eoip:knowledge:document:{event.source_record_id}"
        ) is None
        assert (raw.read_bytes(), dlq.read_bytes()) == original
        live.audit(job, "partial")
