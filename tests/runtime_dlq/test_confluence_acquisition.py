import json

import pytest
from eoip.contracts.source_event import SourceEventV2
from eoip.ingestion.replay import logical_graph_output, logical_output_diff


@pytest.mark.req("FR-CONF-001", "G2-T0401", "G2-T0402", "G2-T0403", "G2-T0404", "G2-SRC-CONF-003", "G2-SRC-CONF-001")
def test_confluence_http_baseline_hierarchy_incremental_and_replay(live_replay, confluence_source):
    live = live_replay
    with confluence_source() as (source_id, upstream):
        run_id = source_id.removeprefix("confluence-")
        baseline = live.finish(live.submit(f"/api/v1/sources/{source_id}/baseline", {}), "SUCCEEDED")
        result = baseline["result"]
        assert (result["records_seen"], result["records_accepted"], result["records_rejected"]) == (4, 4, 0)
        requests = upstream.get("/requests").json()
        assert len(requests) == 15
        assert all(r["authorized"] and r["correlation_id"] == baseline["correlation_id"] for r in requests)
        for kind, expected in (("space", [0, 1]), ("page", [0, 1, 2]), ("attachment", [0, 1])):
            offsets = [int(r["params"]["start"][0]) for r in requests
                       if (r["path"].endswith("/space") if kind == "space"
                           else f"type = {kind}" in r["params"].get("cql", [""])[0])]
            assert offsets == expected
        for index in range(2):
            assert [int(r["params"]["start"][0]) for r in requests
                    if r["path"].endswith(f"/{run_id}-page-{index}/label")] == [0, 1, 2, 3]
        events = []
        for path in (live.root / "raw" / "confluence").glob("*.json"):
            event = SourceEventV2.model_validate_json(path.read_text(encoding="utf-8"))
            if event.payload.get("space", {}).get("key") == f"SPACE-{run_id}" or (
                event.metadata["record_kind"] == "space"
                and event.payload["key"] == f"SPACE-{run_id}"
            ):
                events.append(event)
        assert len(events) == 4
        nodes = {}
        for event in events:
            kind = event.metadata["record_kind"]
            prefix = "urn:eoip:knowledge:space" if kind == "space" else "urn:eoip:knowledge:document"
            node = live.store.get_vertex_by_canonical_id(f"{prefix}:{event.source_record_id}")
            assert node["label"] == ("KnowledgeSpace" if kind == "space" else "Document")
            assert node["properties"]["registry_source_id"] == source_id
            evidence = live.store.find_vertices(label="Evidence", filters={"evidence_key": event.event_id})
            assert len(evidence) == 1 and evidence[0]["properties"]["content_hash"] == event.content_hash
            if kind == "page":
                structure = json.loads(node["properties"]["payload_json"])
                index = event.payload["id"].rsplit("-", 1)[-1]
                assert structure["headings"] == [
                    {"level": 2, "text": f"Fixture page {index}", "anchor": f"fixture-{index}"}
                ]
                assert structure["anchors"] == [f"fixture-{index}", "checks"]
                assert [link["kind"] for link in structure["links"]] == ["anchor", "external", "page"]
                assert structure["code_snippets"] == [{"language": "python", "text": 'print("ready")'}]
                assert structure["tables"][0]["rows"] == [
                    [{"text": "State", "header": True, "rowspan": 1, "colspan": 1}],
                    [{"text": "Ready", "header": False, "rowspan": 1, "colspan": 1}],
                ]
                assert node["properties"]["description"] == event.payload["body"]["storage"]["value"]
                assert evidence[0]["properties"]["parser_version"] == structure["parser_version"]
                assert structure["source_metadata"] == {
                    "schema_version": "1.0",
                    "labels": [
                        {"name": "deploy", "prefix": "global"},
                        {"name": "runbook", "prefix": "global"},
                        {"name": "operations", "prefix": "team"},
                    ],
                    "author": {"type": "known", "user_key": "author-key",
                               "username": "fixture-author", "display_name": "Fixture Author"},
                    "editor": {"type": "known", "user_key": "editor-key", "display_name": "Fixture Editor"},
                    "created_at": "2026-09-30T00:00:00Z",
                    "modified_at": "2026-10-01T00:00:00Z",
                }
            assert any(e["in_cid"] == evidence[0]["canonical_id"]
                       for e in live.store.edges_from(node["vid"], labels=["EVIDENCED_BY"]))
            nodes[event.source_record_id] = node
        space = next(node for node in nodes.values() if node["label"] == "KnowledgeSpace")
        documents = [node for node in nodes.values() if node["label"] == "Document"]
        assert {e["in_cid"] for e in live.store.edges_from(space["vid"], labels=["CONTAINS"])} == {
            node["canonical_id"] for node in documents
        }
        parent = next(node for key, node in nodes.items() if key.endswith(f":page:{run_id}-page-0"))
        child_ids = {node["canonical_id"] for node in documents if node != parent}
        assert {e["in_cid"] for e in live.store.edges_from(parent["vid"], labels=["CONTAINS"])} == child_ids
        checkpoint = live.root / "state" / "connectors" / f"{source_id}.json"
        state = json.loads(checkpoint.read_text(encoding="utf-8"))
        assert state["baseline_complete"] and state["checkpoint"] == result["next_checkpoint"]
        manifest_path = live.root / "state" / "baselines" / source_id / f"{baseline['correlation_id']}.json"
        assert json.loads(manifest_path.read_text(encoding="utf-8"))["stage"] == "COMPLETE"
        original_raw = {e.event_id: (live.root / "raw" / "confluence" / f"{e.event_id}.json").read_bytes()
                        for e in events}
        before = logical_graph_output(live.store)
        incremental = live.finish(live.submit(f"/api/v1/sources/{source_id}/sync", {}), "SUCCEEDED")
        assert incremental["result"]["records_seen"] == 1  # Space metadata is refreshed on every sync.
        assert incremental["result"]["records_accepted"] == 1
        poll_requests = upstream.get("/requests").json()[15:]
        assert len(poll_requests) == 4
        assert all("lastModified >=" in r["params"]["cql"][0] for r in poll_requests if "cql" in r["params"])
        assert all(r["correlation_id"] == incremental["correlation_id"] for r in poll_requests)
        latest = logical_graph_output(live.store)
        expected = json.loads(json.dumps(before))
        observed_at = latest["vertices"][space["canonical_id"]]["properties"]["last_seen"]
        assert observed_at > space["properties"]["last_seen"]
        expected["vertices"][space["canonical_id"]]["properties"]["last_seen"] = observed_at
        assert logical_output_diff(expected, latest)["equivalent"]
        checkpoint_bytes = checkpoint.read_bytes()
        replay = live.finish(live.submit(f"/api/v1/sources/{source_id}/replay",
                                        {"event_ids": [e.event_id for e in events]}), "SUCCEEDED")
        assert replay["result"]["records_accepted"] == 4
        assert logical_output_diff(latest, logical_graph_output(live.store))["equivalent"]
        assert checkpoint.read_bytes() == checkpoint_bytes
        assert all((live.root / "raw" / "confluence" / f"{event_id}.json").read_bytes() == raw
                   for event_id, raw in original_raw.items())
        assert len(upstream.get("/requests").json()) == 19
        for job in (baseline, incremental, replay):
            live.audit(job, "success")
