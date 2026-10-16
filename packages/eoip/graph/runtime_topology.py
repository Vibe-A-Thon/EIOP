"""Runtime topology graph service (G2-GRAPH-RUNTIME-001..003).

Models temporal service-to-service runtime interactions and compares runtime
topology with static code dependencies to detect shadow or dormant relationships.
"""

from __future__ import annotations

from typing import Any

from eoip.graph.store import GraphStore


def record_temporal_service_call(
    store: GraphStore,
    caller_cid: str,
    callee_cid: str,
    observed_at: str,
    *,
    call_count: int = 1,
    latency_ms: float = 0.0,
) -> dict[str, Any]:
    """Records a temporal runtime service-to-service relationship (G2-GRAPH-RUNTIME-002)."""
    caller = store.get_vertex_by_canonical_id(caller_cid)
    callee = store.get_vertex_by_canonical_id(callee_cid)
    if not caller or not callee:
        raise ValueError(f"Service not found: {caller_cid} -> {callee_cid}")

    fact_key = f"temporal_call:{caller_cid}:{callee_cid}:{observed_at}"
    edge = store.upsert_edge(
        "DEPENDS_ON",
        caller["vid"],
        callee["vid"],
        {
            "fact_key": fact_key,
            "observed_at": observed_at,
            "creation_status": "DETERMINISTIC",
            "source_ref": f"telemetry:{observed_at}",
        },
    )
    return {
        "edge_id": edge["eid"],
        "caller": caller_cid,
        "callee": callee_cid,
        "observed_at": observed_at,
    }


def compare_runtime_vs_static_dependencies(store: GraphStore) -> dict[str, Any]:
    """Compares runtime relationships with static code dependencies (G2-GRAPH-RUNTIME-003).

    Returns:
    - matched_dependencies: present both at runtime and statically
    - shadow_runtime_dependencies: observed at runtime but undeclared in static dependencies
    - dormant_static_dependencies: declared statically but not observed at runtime
    - conformance_score: matched / total
    """
    runtime_pairs: set[tuple[str, str]] = set()
    static_pairs: set[tuple[str, str]] = set()

    services = store.find_vertices(label="Service", limit=5000)
    services += store.find_vertices(label="APIService", limit=5000)
    service_by_vid = {s["vid"]: s["canonical_id"] for s in services}

    # Find edges between services
    for s in services:
        out_edges = store.find_edges(out_v=s["vid"], limit=500)
        for e in out_edges:
            if e["in_v"] in service_by_vid:
                target_cid = service_by_vid[e["in_v"]]
                pair = (s["canonical_id"], target_cid)
                if e["properties"].get("observed_at"):
                    runtime_pairs.add(pair)
                else:
                    static_pairs.add(pair)

    matched = sorted(runtime_pairs & static_pairs)
    shadow_runtime = sorted(runtime_pairs - static_pairs)
    dormant_static = sorted(static_pairs - runtime_pairs)

    total_pairs = len(runtime_pairs | static_pairs)
    conformance = len(matched) / max(total_pairs, 1)

    return {
        "matched_dependencies": [{"caller": p[0], "callee": p[1]} for p in matched],
        "shadow_runtime_dependencies": [{"caller": p[0], "callee": p[1]} for p in shadow_runtime],
        "dormant_static_dependencies": [{"caller": p[0], "callee": p[1]} for p in dormant_static],
        "counts": {
            "runtime_total": len(runtime_pairs),
            "static_total": len(static_pairs),
            "matched": len(matched),
            "shadow": len(shadow_runtime),
            "dormant": len(dormant_static),
        },
        "conformance_score": round(conformance, 3),
    }
