from eoip.connectors.jira_json import JiraJsonConnector
from eoip.ingestion.jira import FileEventCapture, JiraIngestionService


def test_mapper_recovery_replays_immutable_capture_idempotently(live_replay):
    live = live_replay
    # An obsolete mapper rejects valid input; the independent worker uses the current mapper.
    service = JiraIngestionService(
        live.store, JiraJsonConnector({"summary": "fields.obsolete_summary"}),
        FileEventCapture(live.root / "raw"), live.root / "dlq",
    )
    rejected = service.ingest(
        {"issues": [{"key": "DLQ-202", "fields": {"summary": "Recovered via replay"}}]}
    )
    assert rejected["run_status"] == "PARTIAL"
    event_id = rejected["rejected"][0]["event_id"]
    raw = live.root / "raw" / "jira" / f"{event_id}.json"
    dlq = live.root / "dlq" / f"{event_id}.json"
    raw_before, dlq_before = raw.read_bytes(), dlq.read_bytes()
    assert any(r["event_id"] == event_id for r in live.get("/api/v1/admin/dlq"))
    first = live.finish(live.submit(f"/api/v1/admin/dlq/{event_id}/replay"), "SUCCEEDED")
    assert first["result"]["records_replayed"] == 1
    entity = live.store.get_vertex_by_canonical_id("urn:eoip:work:item:jira:DLQ-202")
    assert entity["properties"]["summary"] == "Recovered via replay"
    evidence = live.store.find_vertices(label="Evidence", filters={"evidence_key": event_id})
    assert len(evidence) == 1
    assert any(
        edge["in_cid"] == evidence[0]["canonical_id"]
        for edge in live.store.edges_from(entity["vid"], labels=["EVIDENCED_BY"])
    )
    labels_before = live.get("/api/v1/admin/stats")["labels"]
    second = live.finish(live.submit(f"/api/v1/admin/dlq/{event_id}/replay"), "SUCCEEDED")
    assert second["result"]["records_replayed"] == 1
    assert second["result"]["logical_diff"]["equivalent"]
    labels_after = live.get("/api/v1/admin/stats")["labels"]
    assert {
        key: value for key, value in labels_before.items() if key != "IngestionRun"
    } == {key: value for key, value in labels_after.items() if key != "IngestionRun"}
    assert raw.read_bytes() == raw_before and dlq.read_bytes() == dlq_before
    live.audit(first, "success")
    live.audit(second, "success")
