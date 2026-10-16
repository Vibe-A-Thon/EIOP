"""Checksummed logical graph and raw-evidence export for small local deployments.

Stop the worker and avoid writes while creating a snapshot. This export is not
a replacement for native HugeGraph backups on large production graphs.
"""

import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from uuid import UUID

from eoip.contracts.source_event import utc_now_iso
from eoip.jobs import write_json
from eoip.ontology.manifest import (
    EDGE_LABELS,
    SCHEMA_VERSION,
    VERTEX_LABELS,
    edge_endpoints_valid,
)

JOB_STATUSES = {"PENDING", "RUNNING", "HELD", "SUCCEEDED", "PARTIAL", "FAILED", "CANCELLED"}
MAX_OPERATIONAL_FILES = 100_000
MAX_OPERATIONAL_BYTES = 64_000_000


def operational_path(name):
    if not isinstance(name, str):
        raise TypeError("Invalid snapshot operational path")
    relative = PurePosixPath(name)
    if (
        relative.is_absolute()
        or len(relative.parts) < 2
        or relative.as_posix() != name
        or PureWindowsPath(name).is_reserved()
        or any(part.endswith((".", " ")) for part in relative.parts)
        or any(part in {".", ".."} or ":" in part or "\\" in part for part in relative.parts)
        or relative.parts[0] not in {"state", "journal", "jobs", "receipts"}
        or name == "state/worker.json"
        or relative.suffix != (".ndjson" if relative.parts[0] == "journal" else ".json")
    ):
        raise ValueError("Invalid snapshot operational path")
    if relative.parts[0] == "jobs":
        if len(relative.parts) != 2:
            raise ValueError("Invalid snapshot operational job path")
        try:
            if str(UUID(relative.stem)) != relative.stem:
                raise ValueError("noncanonical job ID")
        except ValueError as exc:
            raise ValueError("Invalid snapshot operational job path") from exc
    if relative.parts[0] == "receipts" and (
        len(relative.parts) != 3
        or not relative.stem
        or len(relative.stem) != 64
        or any(character not in "0123456789abcdef" for character in relative.stem)
    ):
        raise ValueError("Invalid snapshot operational receipt path")
    return relative


def validate_operational_record(name, content):
    relative = operational_path(name)
    if not isinstance(content, str):
        raise TypeError("Invalid snapshot operational content")
    if relative.parts[0] == "journal":
        for line in content.splitlines():
            if line.strip() and not isinstance(json.loads(line), dict):
                raise ValueError("Invalid snapshot operational journal")
        return None
    record = json.loads(content)
    if relative.parts[0] == "receipts":
        receipt = record.get("receipt") if isinstance(record, dict) else None
        if (
            not isinstance(receipt, dict)
            or receipt.get("source_id") != relative.parts[1]
            or not isinstance(receipt.get("delivery_id"), str)
            or not isinstance(receipt.get("received_at"), str)
            or not isinstance(receipt.get("content_hash"), str)
            or len(receipt.get("content_hash", "")) != 64
            or not isinstance(receipt.get("payload_ref"), str)
            or not isinstance(record.get("payload"), dict)
            or not isinstance(record.get("metadata", {}), dict)
        ):
            raise ValueError("Invalid snapshot operational receipt")
        return record
    if relative.parts[0] == "jobs" and (
        not isinstance(record, dict)
        or record.get("job_id") != relative.stem
        or record.get("status") not in JOB_STATUSES
        or not isinstance(record.get("kind"), str)
        or not record["kind"]
        or not isinstance(record.get("created_at"), str)
        or "payload" not in record
        or (record.get("payload") is not None and not isinstance(record["payload"], dict))
        or not isinstance(record.get("correlation_id"), str)
        or (record.get("status") == "HELD" and not isinstance(record.get("recovery"), dict))
    ):
        raise ValueError("Invalid snapshot operational job")
    return record


def operational_files(root):
    records = {}
    total_bytes = 0
    for sub in ("state", "journal", "jobs", "receipts"):
        suffix = "*.ndjson" if sub == "journal" else "*.json"
        for path in (root / sub).rglob(suffix):
            name = path.relative_to(root).as_posix()
            if name == "state/worker.json":
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError("Invalid snapshot operational symlink")
            total_bytes += path.stat().st_size
            if len(records) >= MAX_OPERATIONAL_FILES or total_bytes > MAX_OPERATIONAL_BYTES:
                raise ValueError("Logical snapshot operational state exceeds export limits")
            content = path.read_bytes().decode("utf-8")
            validate_operational_record(name, content)
            records[name] = content
    return records


def restored_operational_files(payload, snapshot_sha256, restored_at):
    restored = {}
    records = payload.get("operational_files", {})
    if not isinstance(records, dict) or len(records) > MAX_OPERATIONAL_FILES:
        raise ValueError("Invalid snapshot operational files")
    total_bytes = 0
    for name, content in records.items():
        record = validate_operational_record(name, content)
        total_bytes += len(content.encode("utf-8"))
        if total_bytes > MAX_OPERATIONAL_BYTES:
            raise ValueError("Logical snapshot operational state exceeds export limits")
        if name.startswith("jobs/") and record["status"] in {"PENDING", "RUNNING"}:
            record["recovery"] = {
                "original_status": record["status"],
                "snapshot_sha256": snapshot_sha256,
                "restored_at": restored_at,
            }
            record["status"] = "HELD"
            content = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        restored[name] = content
    return restored


def digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def backup(store, data_dir, destination):
    if hasattr(store, "_pages"):
        vertices = [store._vertex(raw) for raw in store._pages("vertices")]
        edges = [store._edge(raw) for raw in store._pages("edges")]
    else:
        vertices = store.find_vertices(limit=1_000_001, include_deleted=True)
        edges = store.find_edges(limit=1_000_001, include_historical=True)
        if len(vertices) > 1_000_000 or len(edges) > 1_000_000:
            raise ValueError("Logical snapshot exceeds 1000000 records; use a paginated store export")
    root = Path(data_dir)
    raw = {
        path.relative_to(root).as_posix(): json.loads(path.read_text(encoding="utf-8"))
        for sub in ("raw", "dlq")
        for path in (root / sub).rglob("*.json")
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now_iso(),
        "vertices": vertices,
        "edges": edges,
        "raw_files": raw,
        "operational_files": operational_files(root),
    }
    write_json(Path(destination), {"sha256": digest(payload), "payload": payload})
    return {
        "file": str(destination),
        "vertices": len(vertices),
        "edges": len(edges),
        "sha256": digest(payload),
    }


def validate_restore(store, data_dir, source):
    """Validate logical recovery without modifying the graph or data destinations."""
    archive = json.loads(Path(source).read_text(encoding="utf-8"))
    payload = archive["payload"]
    if archive.get("sha256") != digest(payload) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Snapshot checksum or schema version mismatch")
    vertices = {v["vid"]: v for v in payload["vertices"]}
    if len(vertices) != len(payload["vertices"]):
        raise ValueError("Invalid snapshot duplicate vertex IDs")
    canonical_ids = set()
    for vertex in vertices.values():
        if (
            vertex["label"] not in VERTEX_LABELS
            or not isinstance(vertex["properties"], dict)
            or not isinstance(vertex["canonical_id"], str) or not vertex["canonical_id"]
            or vertex["canonical_id"] != vertex["properties"].get("canonical_id")
            or vertex["canonical_id"] in canonical_ids
        ):
            raise ValueError("Invalid snapshot vertex")
        canonical_ids.add(vertex["canonical_id"])
    for edge in payload["edges"]:
        if (
            edge["label"] not in EDGE_LABELS
            or not isinstance(edge["properties"], dict)
            or edge["out_v"] not in vertices
            or edge["in_v"] not in vertices
            or not edge_endpoints_valid(
                edge["label"], vertices[edge["out_v"]]["label"], vertices[edge["in_v"]]["label"]
            )
        ):
            raise ValueError("Invalid snapshot edge")
    root = Path(data_dir).resolve()
    operational = restored_operational_files(payload, archive["sha256"], utc_now_iso())
    for name in operational:
        if not (root / name).resolve().is_relative_to(root):
            raise ValueError("Invalid snapshot operational path")
    for name in payload.get("raw_files", {}):
        relative = PurePosixPath(name)
        destination = (root / name).resolve()
        if (
            relative.is_absolute()
            or not relative.parts
            or relative.parts[0] not in {"raw", "dlq"}
            or not destination.is_relative_to(root)
        ):
            raise ValueError("Invalid snapshot evidence path")
    if store.find_vertices(limit=1, include_deleted=True) or store.find_edges(
        limit=1, include_historical=True
    ):
        raise ValueError("Restore requires an empty graph; use a separate Compose project")
    if any(
        path.is_file()
        for sub in ("raw", "dlq", "state", "journal", "jobs")
        for path in (root / sub).rglob("*")
        if path != root / "state" / "worker.json"
    ):
        raise ValueError("Restore requires empty application data; use a separate Compose project")
    return payload, vertices, root, operational


def restore(store, data_dir, source):
    payload, vertices, root, operational = validate_restore(store, data_dir, source)
    store.ensure_schema({})
    ids = {}
    for old_id, vertex in vertices.items():
        ids[old_id] = store.upsert_vertex(vertex["label"], vertex["properties"])["vid"]
    for edge in payload["edges"]:
        store.upsert_edge(edge["label"], ids[edge["out_v"]], ids[edge["in_v"]], edge["properties"])
    for name, record in payload.get("raw_files", {}).items():
        write_json(root / name, record)
    for name, content in operational.items():
        destination = root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content.encode("utf-8"))
    return {
        "vertices": len(vertices),
        "edges": len(payload["edges"]),
        "raw_files": len(payload.get("raw_files", {})),
    }
