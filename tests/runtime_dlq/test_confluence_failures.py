import json

import pytest
from eoip.ingestion.replay import logical_graph_output, logical_output_diff


@pytest.mark.req("FR-CONF-001", "G2-T0401", "G2-T0402")
def test_confluence_upstream_failures_are_persistent_and_nonmutating(live_replay, confluence_source):
    live = live_replay
    for mode, token_ref, category, request_count in (
        ("valid", "env://EOIP_ACCEPTANCE_INVALID_TOKEN", "authentication_failed", 1),
        ("schema-drift", "env://EOIP_ACCEPTANCE_SOURCE_TOKEN", "schema_drift", 2),
        ("invalid-response", "env://EOIP_ACCEPTANCE_SOURCE_TOKEN", "invalid_response", 1),
        ("label-invalid", "env://EOIP_ACCEPTANCE_SOURCE_TOKEN", "invalid_response", 3),
    ):
        with confluence_source(mode=mode, token_ref=token_ref) as (source_id, upstream):
            before = logical_graph_output(live.store)
            raw_before = {p.name for p in (live.root / "raw" / "confluence").glob("*.json")}
            dlq_before = {p.name for p in (live.root / "dlq").glob("*.json")}
            failed = live.finish(live.submit(f"/api/v1/sources/{source_id}/baseline", {}), "FAILED")
            assert failed["error"] == category and failed["attempts"] == 1
            requests = upstream.get("/requests").json()
            assert len(requests) == request_count
            assert all(r["correlation_id"] == failed["correlation_id"] for r in requests)
            assert all(r["authorized"] == (category != "authentication_failed") for r in requests)
            assert {p.name for p in (live.root / "raw" / "confluence").glob("*.json")} == raw_before
            assert {p.name for p in (live.root / "dlq").glob("*.json")} == dlq_before
            assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
            assert not (live.root / "state" / "connectors" / f"{source_id}.json").exists()
            manifests = list((live.root / "state" / "baselines" / source_id).glob("*.json"))
            assert len(manifests) == 1
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
            assert manifest["stage"] == "FAILED" and manifest["failures"]
            live.audit(failed, "failed")
