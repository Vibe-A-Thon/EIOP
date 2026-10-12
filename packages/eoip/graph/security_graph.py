"""Security and supply-chain graph service (G2-GRAPH-SEC-001..003).

Provides blast-radius computation from package/CVE vulnerabilities to deployed
services and preserves scanner evidence and provenance.
"""

from __future__ import annotations

from typing import Any

from eoip.graph.store import GraphStore


def compute_vulnerability_blast_radius(
    store: GraphStore,
    root_cid: str,
    max_depth: int = 5,
) -> dict[str, Any]:
    """Computes blast radius from a CVE/vulnerability or Dependency to deployed services (G2-GRAPH-SEC-002).

    Preserves scanner/evidence provenance attached via EVIDENCED_BY edges (G2-GRAPH-SEC-003).
    """
    root = store.get_vertex_by_canonical_id(root_cid)
    if not root:
        raise ValueError(f"Entity not found: {root_cid}")

    # 1. Collect scanner / evidence provenance (G2-GRAPH-SEC-003)
    provenance_records = []
    evidence_edges = store.find_edges(out_v=root["vid"], limit=100)
    for e in evidence_edges:
        if e["label"] == "EVIDENCED_BY":
            ev = store.get_vertex(e["in_v"])
            if ev:
                provenance_records.append({
                    "evidence_id": ev["canonical_id"],
                    "source_system": ev["properties"].get("source_system", ""),
                    "source_ref": ev["properties"].get("source_ref", ""),
                    "method": ev["properties"].get("method", ""),
                    "observed_at": ev["properties"].get("observed_at", ""),
                })

    # 2. BFS traversal to find all impacted downstream services & deployments (G2-GRAPH-SEC-002)
    visited = {root["vid"]}
    queue = [(root, 0)]
    impacted_services: list[dict[str, Any]] = []
    impacted_deployments: list[dict[str, Any]] = []

    while queue:
        current, depth = queue.pop(0)
        if depth >= max_depth:
            continue

        # Look at both incoming and outgoing dependency edges
        edges = store.find_edges(in_v=current["vid"], limit=500)
        edges += store.find_edges(out_v=current["vid"], limit=500)

        for e in edges:
            peer_vid = e["out_v"] if e["in_v"] == current["vid"] else e["in_v"]
            if peer_vid in visited:
                continue
            visited.add(peer_vid)
            peer = store.get_vertex(peer_vid)
            if not peer:
                continue

            if peer["label"] in ("Service", "APIService"):
                impacted_services.append({
                    "canonical_id": peer["canonical_id"],
                    "label": peer["label"],
                    "name": peer["properties"].get("name", ""),
                    "distance": depth + 1,
                })
            elif peer["label"] == "Deployment":
                impacted_deployments.append({
                    "canonical_id": peer["canonical_id"],
                    "name": peer["properties"].get("name", ""),
                    "environment": peer["properties"].get("environment", ""),
                    "distance": depth + 1,
                })

            queue.append((peer, depth + 1))

    return {
        "root_entity": root_cid,
        "root_label": root["label"],
        "provenance": provenance_records,
        "has_provenance": len(provenance_records) > 0,
        "impacted_services": impacted_services,
        "impacted_deployments": impacted_deployments,
        "blast_radius_count": len(impacted_services) + len(impacted_deployments),
    }
