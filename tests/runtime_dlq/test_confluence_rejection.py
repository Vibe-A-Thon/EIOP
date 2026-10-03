import json

import pytest
from eoip.contracts.source_event import SourceEventV2
from eoip.ingestion.replay import logical_graph_output, logical_output_diff


@pytest.mark.req("FR-CONF-001", "G2-T0402", "G2-T0112")
def test_confluence_fetched_rejection_preserves_capture_and_checkpoint(live_replay, confluence_source):
    live = live_replay
    with confluence_source(mode="rejected") as (source_id, upstream):
        baseline = live.finish(live.submit(f"/api/v1/sources/{source_id}/baseline", {}), "PARTIAL")
        result = baseline["result"]
        assert (result["records_seen"], result["records_accepted"], result["records_rejected"]) == (4, 3, 1)
        event_id = result["rejected"][0]["event_id"]
        raw = live.root / "raw" / "confluence" / f"{event_id}.json"
        dlq = live.root / "dlq" / f"{event_id}.json"
        original = raw.read_bytes(), dlq.read_bytes()
        event = SourceEventV2.model_validate_json(original[0])
        assert event.payload["id"] and "title" not in event.payload
        assert event.payload["metadata"]["labels"]["results"] == [
            {"name": "runbook", "prefix": "global"},
            {"name": "deploy", "prefix": "global"},
            {"name": "operations", "prefix": "team"},
        ]
        record = json.loads(original[1])
        assert record["registry_source_id"] == source_id and record["error_category"] == "mapping_error"
        assert record["correlation_id"] == baseline["correlation_id"]
        assert live.store.get_vertex_by_canonical_id(f"urn:eoip:knowledge:document:{event.source_record_id}") is None
        assert not (live.root / "state" / "connectors" / f"{source_id}.json").exists()
        before = logical_graph_output(live.store)
        replay = live.finish(live.submit(f"/api/v1/admin/dlq/{event_id}/replay"), "PARTIAL")
        assert (replay["result"]["records_accepted"], replay["result"]["records_rejected"]) == (0, 1)
        assert (raw.read_bytes(), dlq.read_bytes()) == original
        assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
        assert not (live.root / "state" / "connectors" / f"{source_id}.json").exists()
        requests = upstream.get("/requests").json()
        assert len(requests) == 17 and all(r["correlation_id"] == baseline["correlation_id"] for r in requests)
        live.audit(baseline, "partial")
        live.audit(replay, "partial")
