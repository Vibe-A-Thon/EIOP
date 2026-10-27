"""Verify a real HugeGraph restore in an isolated, disposable container."""

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from eoip.graph.traversal import GraphTraversal
from eoip.recovery_bundle import CHUNK, restore_bundle
from eoip.runtime import create_store, data_root
from eoip.snapshot import backup, digest, restore, restored_operational_files


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
    comparison = data / "restore-verification.json"
    try:
        backup(store, data, comparison)
        actual = json.loads(comparison.read_text(encoding="utf-8"))["payload"]
        assert graph_records(actual) == graph_records(payload), "Restored graph properties differ"
        assert actual["raw_files"] == payload["raw_files"], "Restored raw/DLQ evidence differs"
        operational = actual.get("operational_files", {})
        active_names = [
            name for name, content in payload.get("operational_files", {}).items()
            if name.startswith("jobs/") and json.loads(content)["status"] in {"PENDING", "RUNNING"}
        ]
        held = [json.loads(operational[name]) for name in active_names if name in operational]
        restored_at = held[0]["recovery"]["restored_at"] if held else ""
        expected = restored_operational_files(payload, archive["sha256"], restored_at)
        assert operational == expected, "Restored operational state differs"
    finally:
        comparison.unlink(missing_ok=True)


def select_snapshot(source: Path | None, backup_dir: Path) -> Path:
    if source is not None:
        if not source.is_file():
            raise FileNotFoundError(f"Snapshot not found: {source}")
        return source
    candidates = [*backup_dir.glob("*.json"), *backup_dir.glob("*.zip")]
    if not candidates:
        raise FileNotFoundError(f"No snapshots in {backup_dir}; run the backup command first")
    return max(candidates, key=lambda path: path.name)


def verify_restored_bundle(store, data, source, *, config_dir, model_dir):
    with zipfile.ZipFile(source) as archive:
        manifest = json.loads(archive.read("bundle.json"))
        with tempfile.TemporaryDirectory(prefix="eoip-recovery-verification-") as temporary:
            snapshot = Path(temporary) / "snapshot.json"
            snapshot.write_bytes(archive.read("snapshot.json"))
            verify_restored_snapshot(store, data, snapshot)
        for name, record in manifest["files"].items():
            if name == "snapshot.json":
                continue
            group, *parts = Path(name).parts
            root = Path(config_dir if group == "config" else model_dir)
            path = root.joinpath(*parts)
            assert path.stat().st_size == record["size"], "Restored asset size differs"
            hasher = hashlib.sha256()
            with path.open("rb") as handle:
                while chunk := handle.read(CHUNK):
                    hasher.update(chunk)
            assert hasher.hexdigest() == record["sha256"], "Restored asset bytes differ"
        for group, root in (("config", Path(config_dir)), ("models", Path(model_dir))):
            actual = {f"{group}/{path.relative_to(root).as_posix()}"
                      for path in root.rglob("*") if path.is_file()}
            expected = {name for name in manifest["files"] if name.startswith(f"{group}/")}
            assert actual == expected, "Restored asset inventory differs"


def main():
    parser = argparse.ArgumentParser(description="Verify an isolated HugeGraph logical restore")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--config-dir", type=Path, default=Path(tempfile.gettempdir()) / "restore-config")
    parser.add_argument("--model-dir", type=Path, default=Path(tempfile.gettempdir()) / "restore-models")
    args = parser.parse_args()
    source = select_snapshot(args.source, Path("/source/backups"))
    store = create_store()
    try:
        if source.suffix.lower() == ".zip" or zipfile.is_zipfile(source):
            result = restore_bundle(
                store, data_root(), source, config_dir=args.config_dir, model_dir=args.model_dir,
            )
            verify_restored_bundle(
                store, data_root(), source, config_dir=args.config_dir, model_dir=args.model_dir,
            )
        else:
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
