import json

import pytest
from eoip.ingestion.replay import logical_graph_output, logical_output_diff


@pytest.mark.req("FR-SNOW-001")
def test_servicenow_upstream_authentication_failure_is_persistent(live_replay, servicenow_source):
    live = live_replay
    with servicenow_source(token_ref="env://EOIP_ACCEPTANCE_INVALID_TOKEN") as (source_id, upstream):
        before = logical_graph_output(live.store)
        raw_before = {p.name for p in (live.root / "raw" / "servicenow").glob("*.json")}
        failed = live.finish(live.submit(f"/api/v1/sources/{source_id}/baseline", {}), "FAILED")
        assert failed["error"] == "authentication_failed"
        assert failed["attempts"] == 1
        requests = upstream.get("/requests").json()
        assert len(requests) == 1 and not requests[0]["authorized"]
        assert requests[0]["correlation_id"] == failed["correlation_id"]
        assert {p.name for p in (live.root / "raw" / "servicenow").glob("*.json")} == raw_before
        assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
        assert not (live.root / "state" / "connectors" / f"{source_id}.json").exists()
        manifests = list((live.root / "state" / "baselines" / source_id).glob("*.json"))
        assert len(manifests) == 1
        manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
        assert manifest["stage"] == "FAILED" and manifest["failures"]
        live.audit(failed, "failed")
