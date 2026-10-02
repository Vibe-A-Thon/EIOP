"""Checksummed logical graph and raw-evidence export for small local deployments.

Stop the worker and avoid writes while creating a snapshot. This export is not
a replacement for native HugeGraph backups on large production graphs.
"""

import hashlib
import json
from pathlib import Path, PurePosixPath

from eoip.contracts.source_event import utc_now_iso
from eoip.jobs import write_json
from eoip.ontology.manifest import (
    EDGE_LABELS,
    SCHEMA_VERSION,
    VERTEX_LABELS,
    edge_endpoints_valid,
)


def digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def backup(store, data_dir, destination):
    if hasattr(store, "_pages"):
        vertices = [store._vertex(raw) for raw in store._pages("vertices")]
        edges = [store._edge(raw) for raw in store._pages("edges")]
    else:
        vertices = store.find_vertices(limit=1_000_000)
        edges = store.find_edges(limit=1_000_000)
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
    }
    write_json(Path(destination), {"sha256": digest(payload), "payload": payload})
    return {
        "file": str(destination),
        "vertices": len(vertices),
        "edges": len(edges),
        "sha256": digest(payload),
    }


def restore(store, data_dir, source):
    archive = json.loads(Path(source).read_text(encoding="utf-8"))
    payload = archive["payload"]
    if archive.get("sha256") != digest(payload) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Snapshot checksum or schema version mismatch")
    vertices = {v["vid"]: v for v in payload["vertices"]}
    for vertex in vertices.values():
        if vertex["label"] not in VERTEX_LABELS or vertex["canonical_id"] != vertex["properties"].get(
            "canonical_id"
        ):
            raise ValueError("Invalid snapshot vertex")
    for edge in payload["edges"]:
        if (
            edge["label"] not in EDGE_LABELS
            or edge["out_v"] not in vertices
            or edge["in_v"] not in vertices
            or not edge_endpoints_valid(
                edge["label"], vertices[edge["out_v"]]["label"], vertices[edge["in_v"]]["label"]
            )
        ):
            raise ValueError("Invalid snapshot edge")
    root = Path(data_dir).resolve()
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
    if store.count_vertices() or store.count_edges():
        raise ValueError("Restore requires an empty graph; use a separate Compose project")
    store.ensure_schema({})
    ids = {}
    for old_id, vertex in vertices.items():
        ids[old_id] = store.upsert_vertex(vertex["label"], vertex["properties"])["vid"]
    for edge in payload["edges"]:
        store.upsert_edge(edge["label"], ids[edge["out_v"]], ids[edge["in_v"]], edge["properties"])
    for name, record in payload.get("raw_files", {}).items():
        write_json(root / name, record)
    return {
        "vertices": len(vertices),
        "edges": len(payload["edges"]),
        "raw_files": len(payload.get("raw_files", {})),
    }
