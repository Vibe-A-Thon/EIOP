"""
Graffin Autonomic Doctor Daemon & Graph Compaction (GRF-MNT-*, T-GRF-008..010).
Performs autonomous graph self-healing, dangling edge pruning, and query budget governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class GraphHealthAudit:
    total_vertices: int
    total_edges: int
    orphaned_vertices: List[str]
    dangling_edges: List[Dict[str, str]]
    duplicate_vertices: List[str]
    is_healthy: bool


class GraffinDoctorDaemon:
    """
    Self-healing daemon for graph maintenance and compaction.
    """

    def audit_graph(self, graph_dict: Dict[str, Any]) -> GraphHealthAudit:
        vertices = graph_dict.get("vertices", [])
        edges = graph_dict.get("edges", [])

        vertex_ids: Set[str] = set()
        duplicates: List[str] = []
        for v in vertices:
            v_id = v.get("id")
            if v_id in vertex_ids:
                duplicates.append(v_id)
            elif v_id:
                vertex_ids.add(v_id)

        dangling: List[Dict[str, str]] = []
        referenced_vertices: Set[str] = set()

        for e in edges:
            src = e.get("source_id")
            tgt = e.get("target_id")
            if src not in vertex_ids or tgt not in vertex_ids:
                dangling.append({"source": src, "target": tgt, "relation": e.get("relation", "")})
            if src:
                referenced_vertices.add(src)
            if tgt:
                referenced_vertices.add(tgt)

        orphans = [v_id for v_id in vertex_ids if v_id not in referenced_vertices]

        is_healthy = (len(dangling) == 0 and len(duplicates) == 0)
        return GraphHealthAudit(
            total_vertices=len(vertices),
            total_edges=len(edges),
            orphaned_vertices=orphans,
            dangling_edges=dangling,
            duplicate_vertices=duplicates,
            is_healthy=is_healthy,
        )

    def compact_graph(self, graph_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes duplicate vertices and prunes dangling edges.
        """
        vertices = graph_dict.get("vertices", [])
        edges = graph_dict.get("edges", [])

        seen_ids: Set[str] = set()
        clean_vertices = []
        for v in vertices:
            v_id = v.get("id")
            if v_id and v_id not in seen_ids:
                seen_ids.add(v_id)
                clean_vertices.append(v)

        clean_edges = []
        for e in edges:
            src = e.get("source_id")
            tgt = e.get("target_id")
            if src in seen_ids and tgt in seen_ids:
                clean_edges.append(e)

        return {
            **graph_dict,
            "vertices": clean_vertices,
            "edges": clean_edges,
            "vertices_count": len(clean_vertices),
            "edges_count": len(clean_edges),
        }
