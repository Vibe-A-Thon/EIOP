"""Graph metrics engine: centrality, blast radius, and what-if analysis."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from eoip.graph.store import GraphStore


class BlastRadiusResult:
    __slots__ = ("target_id", "total_affected", "by_depth", "by_type", "risk", "affected_ids")

    def __init__(self, target_id: str, total_affected: int, by_depth: dict[int, int],
                 by_type: dict[str, int], risk: str, affected_ids: list[str]):
        self.target_id = target_id
        self.total_affected = total_affected
        self.by_depth = by_depth
        self.by_type = by_type
        self.risk = risk
        self.affected_ids = affected_ids

    def to_dict(self) -> dict:
        return {
            "target_id": self.target_id,
            "total_affected": self.total_affected,
            "by_depth": self.by_depth,
            "by_type": self.by_type,
            "risk": self.risk,
            "affected_ids": self.affected_ids,
        }


class CentralityMetrics:
    __slots__ = ("canonical_id", "degree", "in_degree", "out_degree",
                 "betweenness", "closeness", "page_rank")

    def __init__(self, canonical_id: str, degree: int = 0, in_degree: int = 0,
                 out_degree: int = 0, betweenness: float = 0.0,
                 closeness: float = 0.0, page_rank: float = 0.0):
        self.canonical_id = canonical_id
        self.degree = degree
        self.in_degree = in_degree
        self.out_degree = out_degree
        self.betweenness = betweenness
        self.closeness = closeness
        self.page_rank = page_rank

    def to_dict(self) -> dict:
        return {
            "canonical_id": self.canonical_id,
            "degree": self.degree,
            "in_degree": self.in_degree,
            "out_degree": self.out_degree,
            "betweenness": round(self.betweenness, 6),
            "closeness": round(self.closeness, 6),
            "page_rank": round(self.page_rank, 6),
        }


class GraphMetricsEngine:
    def __init__(self, store: GraphStore):
        self._store = store

    def _build_adjacency(self, node_ids: set[str] | None = None) -> tuple[
        dict[str, list[str]], dict[str, list[str]], dict[str, dict]
    ]:
        out_adj: dict[str, list[str]] = defaultdict(list)
        in_adj: dict[str, list[str]] = defaultdict(list)
        node_map: dict[str, dict] = {}

        vertices = self._store.find_vertices(limit=50000) if node_ids is None else []
        if node_ids is not None:
            for cid in node_ids:
                v = self._store.get_vertex_by_canonical_id(cid)
                if v:
                    vertices.append(v)

        for v in vertices:
            cid = v["properties"]["canonical_id"]
            node_map[cid] = v
            for edge in self._store.edges_from(v["vid"]):
                target = self._store.get_vertex(edge["in_v"])
                if target:
                    tcid = target["properties"]["canonical_id"]
                    out_adj[cid].append(tcid)
                    in_adj[tcid].append(cid)

        return out_adj, in_adj, node_map

    def blast_radius(self, canonical_id: str, max_depth: int = 4) -> BlastRadiusResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return BlastRadiusResult(canonical_id, 0, {}, {}, "NONE", [])

        visited: set[int] = {root["vid"]}
        queue: deque[tuple[int, int]] = deque([(root["vid"], 0)])
        by_depth: dict[int, int] = defaultdict(int)
        by_type: dict[str, int] = defaultdict(int)
        affected_ids: list[str] = []

        while queue:
            vid, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for edge in self._store.edges_from(vid):
                tvid = edge["in_v"]
                if tvid not in visited:
                    visited.add(tvid)
                    target = self._store.get_vertex(tvid)
                    if target:
                        d = depth + 1
                        by_depth[d] = by_depth.get(d, 0) + 1
                        by_type[target["label"]] = by_type.get(target["label"], 0) + 1
                        affected_ids.append(target["properties"]["canonical_id"])
                        queue.append((tvid, d))

        total = len(affected_ids)
        total_graph = self._store.count_vertices()
        pct = (total / max(total_graph, 1)) * 100
        risk = "HIGH" if pct > 20 else "MEDIUM" if pct > 5 else "LOW"

        return BlastRadiusResult(canonical_id, total, dict(by_depth), dict(by_type), risk, affected_ids)

    def reverse_impact(self, canonical_id: str, max_depth: int = 4) -> BlastRadiusResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return BlastRadiusResult(canonical_id, 0, {}, {}, "NONE", [])

        visited: set[int] = {root["vid"]}
        queue: deque[tuple[int, int]] = deque([(root["vid"], 0)])
        by_depth: dict[int, int] = defaultdict(int)
        by_type: dict[str, int] = defaultdict(int)
        affected_ids: list[str] = []

        while queue:
            vid, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for edge in self._store.edges_to(vid):
                svid = edge["out_v"]
                if svid not in visited:
                    visited.add(svid)
                    source = self._store.get_vertex(svid)
                    if source:
                        d = depth + 1
                        by_depth[d] = by_depth.get(d, 0) + 1
                        by_type[source["label"]] = by_type.get(source["label"], 0) + 1
                        affected_ids.append(source["properties"]["canonical_id"])
                        queue.append((svid, d))

        total = len(affected_ids)
        total_graph = self._store.count_vertices()
        pct = (total / max(total_graph, 1)) * 100
        risk = "HIGH" if pct > 20 else "MEDIUM" if pct > 5 else "LOW"

        return BlastRadiusResult(canonical_id, total, dict(by_depth), dict(by_type), risk, affected_ids)

    def centrality(self, canonical_ids: list[str]) -> dict[str, CentralityMetrics]:
        results: dict[str, CentralityMetrics] = {}
        for cid in canonical_ids:
            v = self._store.get_vertex_by_canonical_id(cid)
            if v is None:
                continue
            out_edges = self._store.edges_from(v["vid"])
            in_edges = self._store.edges_to(v["vid"])
            results[cid] = CentralityMetrics(
                canonical_id=cid,
                degree=len(out_edges) + len(in_edges),
                in_degree=len(in_edges),
                out_degree=len(out_edges),
            )
        return results

    def graph_statistics(self) -> dict[str, Any]:
        from eoip.ontology.manifest import VERTEX_LABELS, EDGE_LABELS
        vertex_count = self._store.count_vertices()
        edge_count = self._store.count_edges()
        max_possible_edges = vertex_count * (vertex_count - 1) if vertex_count > 1 else 1
        density = edge_count / max_possible_edges if max_possible_edges > 0 else 0.0

        return {
            "vertex_count": vertex_count,
            "edge_count": edge_count,
            "density": round(density, 6),
            "vertex_label_count": len(VERTEX_LABELS),
            "edge_label_count": len(EDGE_LABELS),
        }

    def graph_schema(self) -> dict[str, Any]:
        from eoip.ontology.manifest import (
            VERTEX_LABELS, EDGE_LABELS, PROPERTY_KEYS,
            INDEXES, ONTOLOGY_VERSION, SCHEMA_VERSION, DOMAINS,
        )
        vertex_schemas = {}
        for label, (domain, required, optional) in VERTEX_LABELS.items():
            vertex_schemas[label] = {
                "domain": domain,
                "required_properties": required,
                "optional_properties": optional,
                "instance_count": self._store.count_vertices(label),
            }

        edge_schemas = {}
        for label, (out_labels, in_labels, props) in EDGE_LABELS.items():
            edge_schemas[label] = {
                "source_labels": out_labels,
                "target_labels": in_labels,
                "properties": props,
            }

        index_info = []
        for idx in INDEXES:
            index_info.append({
                "name": idx["name"],
                "type": idx["type"],
                "label": idx.get("label"),
                "fields": idx["fields"],
            })

        return {
            "ontology_version": ONTOLOGY_VERSION,
            "schema_version": SCHEMA_VERSION,
            "domains": DOMAINS,
            "vertex_labels": vertex_schemas,
            "edge_labels": edge_schemas,
            "property_keys": PROPERTY_KEYS,
            "indexes": index_info,
        }
