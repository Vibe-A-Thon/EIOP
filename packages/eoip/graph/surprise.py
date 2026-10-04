"""Surprising connection detection for EOIP graphs.

The detector ranks edges and absences that deserve human attention because
they bridge otherwise separate neighborhoods or connect different domains.
It is deliberately read-only and bounded so it can back demo/UI exploration
without becoming a graph mutation path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from eoip.graph.similarity import SimilarityEngine
from eoip.graph.store import Edge, GraphStore, Vertex


@dataclass(frozen=True)
class SurpriseResult:
    kind: str
    score: float
    explanation: str
    source_id: str | None = None
    target_id: str | None = None
    edge_id: str | None = None
    edge_label: str | None = None
    source_label: str | None = None
    target_label: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "score": round(self.score, 6),
            "explanation": self.explanation,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_id": self.edge_id,
            "edge_label": self.edge_label,
            "source_label": self.source_label,
            "target_label": self.target_label,
        }


class SurpriseDetector:
    """Ranks structurally unexpected edges and missing relationships."""

    def __init__(self, store: GraphStore, *, scan_limit: int = 50_000) -> None:
        self._store = store
        self._scan_limit = scan_limit

    def _vertices(self) -> list[Vertex]:
        return self._store.find_vertices(limit=self._scan_limit)

    def _vertex_maps(self) -> tuple[dict[str, Vertex], dict[str, str]]:
        vertices = self._vertices()
        by_vid = {v["vid"]: v for v in vertices}
        cid_to_vid = {v["properties"]["canonical_id"]: v["vid"] for v in vertices}
        return by_vid, cid_to_vid

    def _adjacency(self, by_vid: dict[str, Vertex]) -> dict[str, set[str]]:
        adjacency: dict[str, set[str]] = {v["properties"]["canonical_id"]: set() for v in by_vid.values()}
        for vertex in by_vid.values():
            source_cid = vertex["properties"]["canonical_id"]
            for edge in self._store.edges_from(vertex["vid"], limit=500):
                target = by_vid.get(edge["in_v"])
                if target is None:
                    continue
                target_cid = target["properties"]["canonical_id"]
                if target_cid == source_cid:
                    continue
                adjacency[source_cid].add(target_cid)
                adjacency[target_cid].add(source_cid)
        return adjacency

    def surprising_edges(self, limit: int = 20) -> list[SurpriseResult]:
        by_vid, _ = self._vertex_maps()
        adjacency = self._adjacency(by_vid)
        scored: list[SurpriseResult] = []
        seen: set[str] = set()

        for edge in self._store.find_edges(limit=self._scan_limit):
            edge_id = edge.get("eid") or edge.get("id")
            if edge_id in seen:
                continue
            seen.add(edge_id)
            source = by_vid.get(edge["out_v"])
            target = by_vid.get(edge["in_v"])
            if source is None or target is None:
                continue
            scored.append(self._score_edge(edge, source, target, adjacency))

        scored.sort(key=lambda result: (-result.score, result.source_id or "", result.target_id or ""))
        return scored[:limit]

    def _score_edge(
        self,
        edge: Edge,
        source: Vertex,
        target: Vertex,
        adjacency: dict[str, set[str]],
    ) -> SurpriseResult:
        source_cid = source["properties"]["canonical_id"]
        target_cid = target["properties"]["canonical_id"]
        source_neighbors = set(adjacency.get(source_cid, set())) - {target_cid}
        target_neighbors = set(adjacency.get(target_cid, set())) - {source_cid}
        union = source_neighbors | target_neighbors
        intersection = source_neighbors & target_neighbors
        jaccard = len(intersection) / len(union) if union else 0.0
        cross_domain = source["label"] != target["label"]
        source_degree = len(adjacency.get(source_cid, set()))
        target_degree = len(adjacency.get(target_cid, set()))
        bridge_factor = 1.0 / (jaccard + 0.05)
        domain_bonus = 1.75 if cross_domain else 1.0
        degree_bonus = min(2.0, 1.0 + ((source_degree + target_degree) / 20.0))
        evidence_bonus = 0.85 if edge.get("properties", {}).get("creation_status") == "INFERRED" else 1.0
        score = bridge_factor * domain_bonus * degree_bonus * evidence_bonus
        reason_bits = [
            f"{edge['label']} connects {source['label']} to {target['label']}",
            f"neighborhood_overlap={jaccard:.2f}",
        ]
        if cross_domain:
            reason_bits.append("cross-domain bridge")
        return SurpriseResult(
            kind="surprising_edge",
            score=score,
            explanation="; ".join(reason_bits),
            source_id=source_cid,
            target_id=target_cid,
            edge_id=edge.get("eid"),
            edge_label=edge["label"],
            source_label=source["label"],
            target_label=target["label"],
        )

    def unexpected_absences(self, limit: int = 20) -> list[SurpriseResult]:
        """Rank high-similarity pairs that do not currently have an edge."""
        similarity = SimilarityEngine(self._store)
        by_vid, _ = self._vertex_maps()
        adjacency = self._adjacency(by_vid)
        labels_by_cid = {v["properties"]["canonical_id"]: v["label"] for v in by_vid.values()}
        results: list[SurpriseResult] = []
        seen_pairs: set[tuple[str, str]] = set()

        for source_id in sorted(adjacency):
            for prediction in similarity.link_prediction(source_id, algorithm="common_neighbors", limit=limit):
                target_id = prediction["target_id"]
                pair = tuple(sorted((source_id, target_id)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                score = float(prediction["score"])
                if score <= 0:
                    continue
                results.append(
                    SurpriseResult(
                        kind="unexpected_absence",
                        score=score,
                        explanation=f"{source_id} and {target_id} share {int(score)} neighbor(s) but have no direct edge",
                        source_id=source_id,
                        target_id=target_id,
                        source_label=labels_by_cid.get(source_id),
                        target_label=labels_by_cid.get(target_id),
                    )
                )

        results.sort(key=lambda result: (-result.score, result.source_id or "", result.target_id or ""))
        return results[:limit]

    def summary(self, limit: int = 20) -> dict[str, Any]:
        surprising_edges = self.surprising_edges(limit=limit)
        unexpected_absences = self.unexpected_absences(limit=limit)
        return {
            "surprising_edges": [result.to_dict() for result in surprising_edges],
            "unexpected_absences": [result.to_dict() for result in unexpected_absences],
            "counts": {
                "surprising_edges": len(surprising_edges),
                "unexpected_absences": len(unexpected_absences),
            },
        }
