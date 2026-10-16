"""Fresh HugeGraph demo, replay and logical recovery acceptance.

Run only in the disposable acceptance Compose project, never against the demo graph.
"""

import hashlib
import json
import os
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from eoip.contracts.source_event import SourceEventV2
from eoip.demo import load_demo
from eoip.graph.evolution import ChangeJournal, GraphEvolutionEngine
from eoip.graph.hugegraph import HugeGraphStore
from eoip.graph.memory import MemoryGraphStore, edge_key
from eoip.graph.traversal import GraphTraversal
from eoip.ingestion import pipeline
from eoip.ingestion.replay import logical_graph_output, logical_output_diff
from eoip.jobs import JobQueue, write_json
from eoip.provenance.lineage import LineageService
from eoip.snapshot import backup, restore
from eoip.validation.engine import ValidationEngine
from jsonschema import validate

from scripts.verify_restore import verify_restored_snapshot

ISSUE = "urn:eoip:work:item:jira:EOIP-1"
RECAPTURE_TIMESTAMPS = frozenset({"captured_at", "first_seen", "last_seen", "valid_from", "modified_at"})


def load_canonical_demo(store, data: Path, project_root: Path | None) -> tuple[dict, dict]:
    schema_root = Path(__file__).resolve().parents[1] / "schemas"
    schemas = {
        name: json.loads((schema_root / f"{name}.schema.json").read_text(encoding="utf-8"))
        for name in ("graph_mutation", "normalized_entity", "normalized_relationship")
    }
    counts = {"VERTEX": 0, "EDGE": 0}
    runs = set()
    consumer = pipeline.apply_graph_mutation

    def checked_consumer(graph, mutation):
        validate(mutation.model_dump(), schemas["graph_mutation"])
        kind = "normalized_entity" if mutation.target_kind == "VERTEX" else "normalized_relationship"
        validate(mutation.payload, schemas[kind])
        evidence_key = mutation.payload["properties"].get("evidence_key")
        if evidence_key:
            assert list((data / "raw").rglob(f"{evidence_key}.json")), "Mutation preceded evidence capture"
        result = consumer(graph, mutation)
        counts[mutation.target_kind] += 1
        runs.add(mutation.ingestion_run_id)
        return result

    with patch.object(pipeline, "apply_graph_mutation", side_effect=checked_consumer):
        result = load_demo(store, data, project_root)
    assert all(counts.values()), "Demo bypassed canonical mutation envelopes"
    assert runs, "Demo did not provide ingestion run context"
    return result, {"mutations": counts, "run_count": len(runs), "contracts_valid": True}


def verify_schema_preflight(store: HugeGraphStore) -> dict:
    kinds = tuple(store._schema_definitions())

    def schema_state():
        return {kind: store._request("GET", f"/schema/{kind}")[kind] for kind in kinds}

    def data_state():
        return {
            kind: {item["id"]: item for item in store._pages(kind)}
            for kind in ("vertices", "edges")
        }

    schema_before = schema_state()
    data_before = data_state()
    assert store.ensure_schema() == {"created": False, "initialized": True}
    proposals = [
        ("propertykeys", "data_type", "INT"),
        ("vertexlabels", "id_strategy", "AUTOMATIC"),
        ("edgelabels", "frequency", "SINGLE"),
        ("indexlabels", "index_type", "RANGE"),
    ]
    for kind, field, value in proposals:
        proposed = deepcopy(store._schema_definitions())
        proposed[kind][0][field] = value
        proposed["propertykeys"].append({
            "name": "acceptance_pending_property", "data_type": "TEXT", "cardinality": "SINGLE",
        })
        # Only the proposed manifest is substituted; all reads use the real populated server.
        with (
            patch.object(store, "_schema_definitions", return_value=proposed),
            patch.object(store, "_request", wraps=store._request) as requests,
        ):
            try:
                store.ensure_schema()
            except ValueError as exc:
                assert "Incompatible HugeGraph schema" in str(exc) and field in str(exc), str(exc)
            else:
                raise AssertionError(f"Incompatible {kind}/{field} proposal was accepted")
            assert len(requests.call_args_list) == 4
            assert all(call.args[0] == "GET" for call in requests.call_args_list)
        assert schema_state() == schema_before, f"Rejected {kind}/{field} changed schema"
        assert data_state() == data_before, f"Rejected {kind}/{field} changed data"
    return {
        "idempotent": True,
        "incompatible_proposals_rejected": len(proposals),
        "schema_and_data_unchanged": True,
        "no_schema_mutations": True,
    }


def demo_business_output(store) -> dict:
    projection = logical_graph_output(store)
    # Loading fixtures captures new observations; recovery comparisons below retain every property.
    for vertex in projection["vertices"].values():
        vertex["properties"] = {
            key: value for key, value in vertex["properties"].items() if key not in RECAPTURE_TIMESTAMPS
        }
    return projection


def verify_temporal_edge_upgrade(store, root: Path) -> dict:
    """Exercise old physical identities on the disposable acceptance server."""
    cid = {name: f"urn:eoip:acceptance:temporal:{name}" for name in ("a", "b", "c")}
    relationship = "urn:eoip:acceptance:temporal:dependency"
    assert all(store.get_vertex_by_canonical_id(value) is None for value in cid.values())

    def event(day, operation="UPSERT"):
        payload = {"id": relationship, "day": day}
        at = f"2026-10-{day:02d}T00:00:00Z"
        return SourceEventV2(
            event_id=f"acceptance-temporal-{day}", source_system="test",
            source_instance_id="acceptance", source_record_id=relationship,
            operation=operation, event_time=at, captured_at=at,
            content_hash=hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
            payload=payload if operation != "DELETE" else None,
        )

    fixture = MemoryGraphStore()
    for name, identity in cid.items():
        fixture.upsert_vertex("File", {"canonical_id": identity, "repo_id": "acceptance", "path": name})
    seeded = GraphEvolutionEngine(fixture, ChangeJournal(root / "seed.ndjson"))
    first = event(1)
    seeded.evolve_relationship(relationship, "DEPENDS_ON", cid["a"], cid["b"], {}, first)
    for vertex in fixture.find_vertices(limit=100):
        properties = {key: value for key, value in vertex["properties"].items() if key != "edge_key"}
        store.upsert_vertex(vertex["label"], properties)
    source = store.get_vertex_by_canonical_id(cid["a"])
    target = store.get_vertex_by_canonical_id(cid["b"])
    legacy_key = edge_key("DEPENDS_ON", cid["a"], cid["b"], relationship)
    old_properties = dict(fixture.find_edges()[0]["properties"])
    old_properties["edge_key"] = legacy_key
    store.upsert_edge("DEPENDS_ON", source["vid"], target["vid"], old_properties)
    engine = GraphEvolutionEngine(store, ChangeJournal(root / "evolution.ndjson"))

    def current_targets():
        return [
            edge["in_cid"] for edge in store.edges_from(source["vid"], labels=["DEPENDS_ON"])
        ]

    engine.evolve_relationship(relationship, "DEPENDS_ON", cid["a"], cid["c"], {}, event(2))
    assert current_targets() == [cid["c"]], "Legacy relationship remained current"
    expired = store.find_edge_by_key(legacy_key)
    assert expired["properties"]["is_current"] is False
    assert expired["properties"]["valid_to"] == event(2).event_time
    engine.evolve_relationship(relationship, "DEPENDS_ON", cid["a"], cid["c"], {}, event(3, "DELETE"))
    assert current_targets() == []
    engine.evolve_relationship(relationship, "DEPENDS_ON", cid["a"], cid["b"], {}, event(4))
    assert current_targets() == [cid["b"]]
    assert len(store.edges_from(source["vid"], labels=["DEPENDS_ON"], include_historical=True)) == 3
    assert not [
        item for item in engine.as_of("2026-10-03T12:00:00Z", limit=100_000)["relationships"]
        if item["relationship_id"] == relationship
    ]
    assert engine.evolve_relationship(
        relationship, "DEPENDS_ON", cid["a"], cid["b"], {}, first,
    )["status"] == "LATE_IGNORED"
    return {
        "legacy_edge_expired": True, "replacement_current_only": True,
        "deletion_barrier_preserved": True, "recreation_without_phantom_edge": True,
        "physical_history_edges": 3,
    }


def golden_queries(store, data: Path) -> dict:
    symbols = store.find_vertices(label="CodeSymbol", filters={"name": "compute_impact"})
    assert len(symbols) == 1, "Expected exactly one compute_impact symbol"
    path = GraphTraversal(
        store, allowed_edges=frozenset({"IMPLEMENTS", "MODIFIES", "DECLARES"})
    ).find_path(ISSUE, symbols[0]["canonical_id"])
    assert path, "Missing Jira-to-code path"
    assert {"IMPLEMENTS", "MODIFIES", "DECLARES"} <= {edge["label"] for edge in path["edges"]}
    for edge in path["edges"]:
        key = edge["properties"].get("evidence_key")
        assert key, "Golden path has no captured evidence"
        evidence = list((data / "raw").rglob(f"{key}.json"))
        assert len(evidence) == 1, f"Golden path evidence is missing or ambiguous: {key}"
        record = json.loads(evidence[0].read_text(encoding="utf-8"))
        assert record["event_id"] == key, "Golden path evidence identity differs"
    impact = GraphTraversal(store).impact(ISSUE, max_depth=4)
    assert len(impact["impacted"]) >= 4
    assert not impact["truncated"], "Demo impact exceeded the configured budget"
    lineage = LineageService(store).trace(ISSUE)
    assert lineage["sources"] and lineage["ingestion_runs"]
    assert not lineage["truncated"]
    return {
        "path": [vertex["canonical_id"] for vertex in path["vertices"]],
        "path_edges": [edge["label"] for edge in path["edges"]],
        "impact": sorted(item["vertex"]["canonical_id"] for item in impact["impacted"]),
        "lineage_sources": sorted(item["canonical_id"] for item in lineage["sources"]),
        "lineage_runs": sorted(item["canonical_id"] for item in lineage["ingestion_runs"]),
    }


def verify_clean_demo(source, target, root: Path, *, project_root: Path | None = None) -> dict:
    for store in (source, target):
        assert store.count_vertices() == store.count_edges() == 0, "Acceptance requires empty graphs"
    source.ensure_schema({})
    original_data, restored_data = root / "original", root / "restored"
    initial, initial_contracts = load_canonical_demo(source, original_data, project_root)
    assert initial["jira"]["run_status"] == "SUCCEEDED"
    assert initial["git"]["files"] and initial["git"]["symbols"]
    golden_queries(source, original_data)
    before = demo_business_output(source)
    replay, replay_contracts = load_canonical_demo(source, original_data, project_root)
    assert replay["jira"]["run_status"] == "SUCCEEDED"
    diff = logical_output_diff(before, demo_business_output(source))
    assert diff["equivalent"], f"Replay changed logical business data: {diff}"
    golden = golden_queries(source, original_data)
    validation = ValidationEngine(source).run()
    errors = [finding for finding in validation["findings"] if finding["severity"] == "ERROR"]
    assert not errors, f"Fresh demo validation errors: {errors}"
    write_json(original_data / "state" / "connectors" / "acceptance.json",
               {"cursor": "acceptance-checkpoint", "baseline_complete": True})
    write_json(original_data / "state" / "worker.json", {"status": "running"})
    pending = JobQueue(original_data).submit("DEMO")
    snapshot = root / "snapshot.json"
    exported = backup(source, original_data, snapshot)
    restored = restore(target, restored_data, snapshot)
    verify_restored_snapshot(target, restored_data, snapshot)
    assert JobQueue(restored_data).get(pending["job_id"])["status"] == "HELD"
    assert not (restored_data / "state" / "worker.json").exists()
    assert golden_queries(target, restored_data) == golden, "Recovery changed golden query results"
    try:
        restore(target, restored_data, snapshot)
    except ValueError as exc:
        assert "empty graph" in str(exc)
    else:
        raise AssertionError("A populated restore target was accepted")
    verify_restored_snapshot(target, restored_data, snapshot)
    return {
        "status": "PASS",
        "vertices": exported["vertices"],
        "edges": exported["edges"],
        "restored_raw_files": restored["raw_files"],
        "replay_equivalent": diff["equivalent"],
        "replay_excluded_observation_timestamps": sorted(RECAPTURE_TIMESTAMPS),
        "validation_errors": len(errors),
        "golden": golden,
        "snapshot_sha256": exported["sha256"],
        "populated_target_rejected": True,
        "operational_recovery": {"checkpoint_preserved": True, "active_job_held": True,
                                 "stale_worker_heartbeat_excluded": True},
        "canonical_ingestion": {"initial": initial_contracts, "replay": replay_contracts},
    }


def main():
    source_url = os.environ["EOIP_ACCEPTANCE_SOURCE_URL"]
    target_url = os.environ["EOIP_ACCEPTANCE_TARGET_URL"]
    if source_url == target_url:
        raise ValueError("Acceptance source and target must be separate disposable graph servers")
    report = Path(os.environ["EOIP_ACCEPTANCE_REPORT"])
    password = os.environ["EOIP_HUGEGRAPH_PASSWORD"]
    source = HugeGraphStore(source_url, password=password)
    target = HugeGraphStore(target_url, password=password)
    try:
        result = verify_clean_demo(source, target, Path("/tmp/acceptance"))
        result["schema_preflight"] = verify_schema_preflight(source)
        result["temporal_edge_upgrade"] = verify_temporal_edge_upgrade(source, Path("/tmp/temporal"))
        write_json(report, result)
        print(json.dumps(result, indent=2))
    except Exception as exc:
        write_json(report, {"status": "FAIL", "reason_code": type(exc).__name__})
        raise
    finally:
        source.close()
        target.close()


if __name__ == "__main__":
    main()
