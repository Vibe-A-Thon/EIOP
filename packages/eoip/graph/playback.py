"""Graph playback — temporal event stream for incident/release analysis (G2-T1030..1033).

Builds a chronological event stream for a selected entity (incident, release,
deployment) by traversing the graph for temporally-ordered connected events.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from eoip.graph.store import GraphStore

TEMPORAL_FIELDS = ("created_at", "modified_at", "started_at", "finished_at",
                   "resolved_at", "closed_at", "event_timestamp", "observed_at")

PLAYBACK_EDGE_LABELS = (
    "TRIGGERED_BY", "RESOLVES", "CORRELATES_WITH", "IMPLEMENTS",
    "MODIFIES", "HAS_CHANGE", "DEPLOYS", "PRODUCED_BY", "CONTAINS",
    "TESTS", "EVIDENCED_BY",
)


def _extract_timestamp(props: dict) -> str:
    for f in TEMPORAL_FIELDS:
        val = props.get(f)
        if val:
            return str(val)
    return ""


def build_event_stream(
    store: GraphStore,
    root_cid: str,
    max_depth: int = 3,
    max_events: int = 200,
) -> dict[str, Any]:
    """Build a chronological event stream radiating from a root entity."""
    root = store.get_vertex_by_canonical_id(root_cid)
    if not root:
        return {"root": root_cid, "events": [], "error": "Entity not found"}

    events: list[dict[str, Any]] = []
    visited: set[str] = set()
    queue: list[tuple[str, int]] = [(root["vid"], 0)]
    visited.add(root["vid"])

    while queue and len(events) < max_events:
        vid, depth = queue.pop(0)
        vertex = store.get_vertex(vid)
        if not vertex:
            continue

        ts = _extract_timestamp(vertex["properties"])
        events.append({
            "canonical_id": vertex["canonical_id"],
            "label": vertex["label"],
            "name": vertex["properties"].get("name", vertex["properties"].get("summary", "")),
            "timestamp": ts,
            "depth": depth,
            "properties": {k: v for k, v in vertex["properties"].items()
                          if k in ("status", "severity", "priority", "message", "commit_sha",
                                   "field_name", "from_value", "to_value", "incident_number",
                                   "creation_status", "source_system")},
        })

        if depth < max_depth:
            for e in store.edges_from(vid, limit=50):
                if e["label"] in PLAYBACK_EDGE_LABELS and e["in_v"] not in visited:
                    visited.add(e["in_v"])
                    queue.append((e["in_v"], depth + 1))
            for e in store.edges_to(vid, limit=50):
                if e["label"] in PLAYBACK_EDGE_LABELS and e["out_v"] not in visited:
                    visited.add(e["out_v"])
                    queue.append((e["out_v"], depth + 1))

    events.sort(key=lambda ev: ev.get("timestamp", ""))

    return {
        "root": root_cid,
        "root_label": root["label"],
        "events": events,
        "total_events": len(events),
    }


def build_evidence_panel(store: GraphStore, entity_cid: str) -> dict[str, Any]:
    """Build a source-evidence side panel for an entity (G2-T1032)."""
    entity = store.get_vertex_by_canonical_id(entity_cid)
    if not entity:
        return {"entity": entity_cid, "evidence": [], "error": "Entity not found"}

    evidence: list[dict[str, Any]] = []
    out_edges = store.find_edges(out_v=entity["vid"], label="EVIDENCED_BY", limit=100)
    for e in out_edges:
        ev = store.get_vertex(e["in_v"])
        if ev:
            evidence.append({
                "evidence_id": ev["canonical_id"],
                "source_system": ev["properties"].get("source_system", ""),
                "source_ref": ev["properties"].get("source_ref", ""),
                "method": ev["properties"].get("method", ""),
                "confidence": ev["properties"].get("confidence"),
                "captured_at": ev["properties"].get("captured_at", ""),
            })

    ingestion_edges = store.find_edges(out_v=entity["vid"], label="INGESTED_IN", limit=10)
    ingestion_runs: list[dict[str, Any]] = []
    for e in ingestion_edges:
        run = store.get_vertex(e["in_v"])
        if run:
            ingestion_runs.append({
                "run_id": run["canonical_id"],
                "status": run["properties"].get("run_status", ""),
                "started_at": run["properties"].get("started_at", ""),
            })

    return {
        "entity": entity_cid,
        "label": entity["label"],
        "evidence": evidence,
        "ingestion_runs": ingestion_runs,
        "creation_status": entity["properties"].get("creation_status", ""),
    }


def export_timeline(store: GraphStore, root_cid: str, format: str = "json") -> dict[str, Any]:
    """Export an evidence timeline for a root entity (G2-T1033)."""
    stream = build_event_stream(store, root_cid)
    if format == "csv":
        lines = ["timestamp,canonical_id,label,name,depth"]
        for ev in stream["events"]:
            lines.append(f"{ev['timestamp']},{ev['canonical_id']},{ev['label']},{ev.get('name','')},{ev['depth']}")
        return {"format": "csv", "content": "\n".join(lines), "total_events": stream["total_events"]}
    return {"format": "json", **stream}
