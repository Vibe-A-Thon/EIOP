from eoip.ingestion.replay import logical_graph_output, logical_output_diff


def test_registered_v2_mapper_recovery_is_persistent_and_idempotent(live_replay, registered_capture):
    live = live_replay
    with registered_capture(recoverable=True) as (source_id, event):
        raw = live.root / "raw" / "confluence" / f"{event.event_id}.json"
        dlq = live.root / "dlq" / f"{event.event_id}.json"
        original = raw.read_bytes(), dlq.read_bytes()
        first = live.finish(live.submit(f"/api/v1/admin/dlq/{event.event_id}/replay"), "SUCCEEDED")
        assert first["result"]["records_accepted"] == 1
        cid = f"urn:eoip:knowledge:document:{event.source_record_id}"
        entity = live.store.get_vertex_by_canonical_id(cid)
        assert entity["properties"]["name"] == "Recovered registered page"
        assert entity["properties"]["registry_source_id"] == source_id
        evidence = live.store.find_vertices(label="Evidence", filters={"evidence_key": event.event_id})
        assert len(evidence) == 1
        assert any(edge["in_cid"] == evidence[0]["canonical_id"]
                   for edge in live.store.edges_from(entity["vid"], labels=["EVIDENCED_BY"]))
        before = logical_graph_output(live.store)
        second = live.finish(live.submit(f"/api/v1/sources/{source_id}/replay",
                                       {"event_ids": [event.event_id]}), "SUCCEEDED")
        assert second["result"]["records_accepted"] == 1
        assert logical_output_diff(before, logical_graph_output(live.store))["equivalent"]
        assert (raw.read_bytes(), dlq.read_bytes()) == original
        assert any(record["event_id"] == event.event_id for record in live.get("/api/v1/admin/dlq"))
        live.audit(first, "success")
        live.audit(second, "success")
