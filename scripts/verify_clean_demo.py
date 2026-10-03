"""Fresh HugeGraph demo, replay and logical recovery acceptance.

Run only in the disposable acceptance Compose project, never against the demo graph.
"""

import json
import os
from pathlib import Path

from eoip.demo import load_demo
from eoip.graph.hugegraph import HugeGraphStore
from eoip.graph.traversal import GraphTraversal
from eoip.ingestion.replay import logical_graph_output, logical_output_diff
from eoip.jobs import write_json
from eoip.provenance.lineage import LineageService
from eoip.snapshot import backup, restore
from eoip.validation.engine import ValidationEngine

from scripts.verify_restore import verify_restored_snapshot

ISSUE = "urn:eoip:work:item:jira:EOIP-1"
RECAPTURE_TIMESTAMPS = frozenset({"captured_at", "first_seen", "last_seen", "valid_from", "modified_at"})


def demo_business_output(store) -> dict:
    projection = logical_graph_output(store)
    # Loading fixtures captures new observations; recovery comparisons below retain every property.
    for vertex in projection["vertices"].values():
        vertex["properties"] = {
            key: value for key, value in vertex["properties"].items() if key not in RECAPTURE_TIMESTAMPS
        }
    return projection


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
    initial = load_demo(source, original_data, project_root)
    assert initial["jira"]["run_status"] == "SUCCEEDED"
    assert initial["git"]["files"] and initial["git"]["symbols"]
    golden_queries(source, original_data)
    before = demo_business_output(source)
    replay = load_demo(source, original_data, project_root)
    assert replay["jira"]["run_status"] == "SUCCEEDED"
    diff = logical_output_diff(before, demo_business_output(source))
    assert diff["equivalent"], f"Replay changed logical business data: {diff}"
    golden = golden_queries(source, original_data)
    validation = ValidationEngine(source).run()
    errors = [finding for finding in validation["findings"] if finding["severity"] == "ERROR"]
    assert not errors, f"Fresh demo validation errors: {errors}"
    snapshot = root / "snapshot.json"
    exported = backup(source, original_data, snapshot)
    restored = restore(target, restored_data, snapshot)
    verify_restored_snapshot(target, restored_data, snapshot)
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
