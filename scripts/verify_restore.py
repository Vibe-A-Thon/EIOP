"""Verify a real HugeGraph restore in an isolated, disposable container."""

import argparse
import json
from pathlib import Path

from eoip.graph.traversal import GraphTraversal
from eoip.runtime import create_store, data_root
from eoip.snapshot import backup, digest, restore


def graph_records(payload):
    vertices = {vertex["vid"]: vertex["canonical_id"] for vertex in payload["vertices"]}
    return {
        "vertices": sorted(
            json.dumps({"label": vertex["label"], "properties": vertex["properties"]}, sort_keys=True)
            for vertex in payload["vertices"]
        ),
        "edges": sorted(
            json.dumps(
                {
                    "label": edge["label"],
                    "out": vertices[edge["out_v"]],
                    "in": vertices[edge["in_v"]],
                    "properties": edge["properties"],
                },
                sort_keys=True,
            )
            for edge in payload["edges"]
        ),
    }


def verify_restored_snapshot(store, data: Path, source: Path) -> None:
    archive = json.loads(source.read_text(encoding="utf-8"))
    payload = archive["payload"]
    assert archive["sha256"] == digest(payload), "Snapshot checksum mismatch"
    assert store.count_vertices() == len(payload["vertices"])
    assert store.count_edges() == len(payload["edges"])
    comparison = data / "restore-verification.json"
    try:
        backup(store, data, comparison)
        actual = json.loads(comparison.read_text(encoding="utf-8"))["payload"]
        assert graph_records(actual) == graph_records(payload), "Restored graph properties differ"
        assert actual["raw_files"] == payload["raw_files"], "Restored raw/DLQ evidence differs"
    finally:
        comparison.unlink(missing_ok=True)


def select_snapshot(source: Path | None, backup_dir: Path) -> Path:
    if source is not None:
        if not source.is_file():
            raise FileNotFoundError(f"Snapshot not found: {source}")
        return source
    candidates = list(backup_dir.glob("*.json"))
    if not candidates:
        raise FileNotFoundError(f"No snapshots in {backup_dir}; run the backup command first")
    return max(candidates, key=lambda path: path.name)


def main():
    parser = argparse.ArgumentParser(description="Verify an isolated HugeGraph logical restore")
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    source = select_snapshot(args.source, Path("/source/backups"))
    store = create_store()
    try:
        result = restore(store, data_root(), source)
        verify_restored_snapshot(store, data_root(), source)
        symbols = store.find_vertices(label="CodeSymbol", filters={"name": "compute_impact"})
        assert symbols
        path = GraphTraversal(
            store, allowed_edges=frozenset({"IMPLEMENTS", "MODIFIES", "DECLARES"})
        ).find_path("urn:eoip:work:item:jira:EOIP-1", symbols[0]["canonical_id"])
        assert path and {edge["label"] for edge in path["edges"]}.issuperset(
            {"IMPLEMENTS", "MODIFIES", "DECLARES"}
        )
        assert all(edge["properties"].get("evidence_key") for edge in path["edges"])
        print(f"PASS: isolated HugeGraph restore: {result}; all graph properties, evidence and golden path preserved")
    finally:
        store.close()


if __name__ == "__main__":
    main()
