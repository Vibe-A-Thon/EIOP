import json

import pytest
from eoip.contracts.source_event import SourceEventV2
from eoip.ingestion.replay import logical_graph_output, logical_output_diff


@pytest.mark.req("FR-SNOW-001", "G2-T0110", "G2-T0203")
def test_servicenow_http_baseline_incremental_and_replay(live_replay, servicenow_source):
    live = live_replay
    with servicenow_source() as (source_id, upstream):
        baseline = live.finish(live.submit(f"/api/v1/sources/{source_id}/baseline", {}), "SUCCEEDED")
        result = baseline["result"]
        assert (result["records_seen"], result["records_accepted"], result["records_rejected"]) == (5, 5, 0)
        requests = upstream.get("/requests").json()
        assert len(requests) == 9
        assert all(r["authorized"] and r["correlation_id"] == baseline["correlation_id"] for r in requests)
        for table in ("incident", "problem", "change_request", "kb_knowledge"):
            offsets = [int(r["params"]["sysparm_offset"][0]) for r in requests if r["table"] == table]
            assert offsets == ([0, 1, 2] if table == "incident" else [0, 1])
        events = []
        for path in (live.root / "raw" / "servicenow").glob("*.json"):
            event = SourceEventV2.model_validate_json(path.read_text(encoding="utf-8"))
            if event.payload["sys_id"].startswith(source_id.removeprefix("servicenow-")):
                events.append(event)
        assert len(events) == 5
        for event in events:
            kind = event.metadata["record_kind"]
            prefix = "urn:eoip:knowledge:document" if kind == "knowledge" else "urn:eoip:work:item"
            entity = live.store.get_vertex_by_canonical_id(f"{prefix}:servicenow:{event.source_record_id}")
            assert entity["label"] == ("Document" if kind == "knowledge" else "WorkItem")
            assert entity["properties"]["registry_source_id"] == source_id
            evidence = live.store.find_vertices(label="Evidence", filters={"evidence_key": event.event_id})
            assert len(evidence) == 1
            assert any(e["in_cid"] == evidence[0]["canonical_id"]
                       for e in live.store.edges_from(entity["vid"], labels=["EVIDENCED_BY"]))
        checkpoint_path = live.root / "state" / "connectors" / f"{source_id}.json"
        state = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        assert state["baseline_complete"] and state["checkpoint"] == result["next_checkpoint"]
        before = logical_graph_output(live.store)
        incremental = live.finish(live.submit(f"/api/v1/sources/{source_id}/sync", {}), "SUCCEEDED")
        assert incremental["result"]["records_seen"] == 0
        poll_requests = upstream.get("/requests").json()[9:]
        assert len(poll_requests) == 4
        assert all("sys_updated_on>=" in r["params"]["sysparm_query"][0] for r in poll_requests)
        assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
        checkpoint_bytes = checkpoint_path.read_bytes()
        raw = live.root / "raw" / "servicenow" / f"{events[0].event_id}.json"
        raw_bytes = raw.read_bytes()
        replay = live.finish(live.submit(f"/api/v1/sources/{source_id}/replay",
                                        {"event_ids": [events[0].event_id]}), "SUCCEEDED")
        assert replay["result"]["records_accepted"] == 1
        assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
        assert checkpoint_path.read_bytes() == checkpoint_bytes and raw.read_bytes() == raw_bytes
        assert len(upstream.get("/requests").json()) == 13
        for job in (baseline, incremental, replay):
            live.audit(job, "success")
