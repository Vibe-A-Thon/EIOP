"""Structural similarity algorithms for graph nodes.

Pure-Python implementations operating on the GraphStore port.
Provides Jaccard, Adamic-Adar, and common-neighbour similarity.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class SimilarityResult:
    """A single similarity score between two nodes."""

    canonical_id: str
    score: float
    common_neighbors: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "score": self.score,
            "common_neighbors": self.common_neighbors,
        }


class SimilarityEngine:
    """Structural node similarity over an EOIP GraphStore."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _neighbor_cids(self, vid: str) -> set[str]:
        """Return canonical_ids of all direct neighbours (both directions)."""
        cids: set[str] = set()
        for edge in self._store.edges_from(vid):
            tgt = self._store.get_vertex(edge["in_v"])
            if tgt is not None:
                cids.add(tgt["properties"]["canonical_id"])
        for edge in self._store.edges_to(vid):
            src = self._store.get_vertex(edge["out_v"])
            if src is not None:
                cids.add(src["properties"]["canonical_id"])
        return cids

    def _all_vertex_neighbors(self) -> dict[str, set[str]]:
        """Build a mapping from canonical_id to set of neighbour canonical_ids."""
        vertices = self._store.find_vertices(limit=50_000)
        vid_to_cid: dict[str, str] = {}
        for v in vertices:
            vid_to_cid[v["vid"]] = v["properties"]["canonical_id"]

        adj: dict[str, set[str]] = {cid: set() for cid in vid_to_cid.values()}
        for v in vertices:
            src_cid = vid_to_cid[v["vid"]]
            for edge in self._store.edges_from(v["vid"]):
                tgt_cid = vid_to_cid.get(edge["in_v"])
                if tgt_cid is not None and tgt_cid != src_cid:
                    adj[src_cid].add(tgt_cid)
                    adj[tgt_cid].add(src_cid)
        return adj

    # ------------------------------------------------------------------
    # Algorithms
    # ------------------------------------------------------------------

    def jaccard(self, canonical_id: str, limit: int = 10) -> list[SimilarityResult]:
        """Jaccard similarity: |intersection| / |union| of neighbour sets."""
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return []

        adj = self._all_vertex_neighbors()
        root_nbrs = adj.get(canonical_id, set())
        if not root_nbrs:
            return []

        scores: list[SimilarityResult] = []
        for other_cid, other_nbrs in adj.items():
            if other_cid == canonical_id or not other_nbrs:
                continue
            intersection = root_nbrs & other_nbrs
            union = root_nbrs | other_nbrs
            score = len(intersection) / len(union) if union else 0.0
            if score > 0.0:
                scores.append(
                    SimilarityResult(
                        canonical_id=other_cid,
                        score=round(score, 6),
                        common_neighbors=len(intersection),
                    )
                )

        scores.sort(key=lambda s: -s.score)
        return scores[:limit]

    def adamic_adar(self, canonical_id: str, limit: int = 10) -> list[SimilarityResult]:
        """Adamic-Adar index: sum of 1/log(degree) over common neighbours."""
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return []

        adj = self._all_vertex_neighbors()
        root_nbrs = adj.get(canonical_id, set())
        if not root_nbrs:
            return []

        scores: list[SimilarityResult] = []
        for other_cid, other_nbrs in adj.items():
            if other_cid == canonical_id or not other_nbrs:
                continue
            common = root_nbrs & other_nbrs
            if not common:
                continue
            aa_score = 0.0
            for cn in common:
                degree = len(adj.get(cn, set()))
                if degree > 1:
                    aa_score += 1.0 / math.log(degree)
            if aa_score > 0.0:
                scores.append(
                    SimilarityResult(
                        canonical_id=other_cid,
                        score=round(aa_score, 6),
                        common_neighbors=len(common),
                    )
                )

        scores.sort(key=lambda s: -s.score)
        return scores[:limit]

    def common_neighbors(self, canonical_id: str, limit: int = 10) -> list[SimilarityResult]:
        """Common-neighbour count as a similarity metric."""
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return []

        adj = self._all_vertex_neighbors()
        root_nbrs = adj.get(canonical_id, set())
        if not root_nbrs:
            return []

        scores: list[SimilarityResult] = []
        for other_cid, other_nbrs in adj.items():
            if other_cid == canonical_id or not other_nbrs:
                continue
            common = root_nbrs & other_nbrs
            if common:
                scores.append(
                    SimilarityResult(
                        canonical_id=other_cid,
                        score=float(len(common)),
                        common_neighbors=len(common),
                    )
                )

        scores.sort(key=lambda s: -s.score)
        return scores[:limit]

    def link_prediction(
        self,
        canonical_id: str,
        algorithm: str = "common_neighbors",
        limit: int = 10,
    ) -> list[dict]:
        """Predict missing edges from *canonical_id* using similarity scores.

        Returns dicts with source_id, target_id, score, and algorithm.
        Only non-adjacent pairs are returned.
        """
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return []

        adj = self._all_vertex_neighbors()
        root_nbrs = adj.get(canonical_id, set())

        predictions: list[dict] = []
        for other_cid, other_nbrs in adj.items():
            if other_cid == canonical_id or other_cid in root_nbrs:
                continue
            common = root_nbrs & other_nbrs
            if not common:
                continue

            if algorithm == "jaccard":
                union = root_nbrs | other_nbrs
                score = len(common) / len(union) if union else 0.0
            elif algorithm == "adamic_adar":
                score = 0.0
                for cn in common:
                    deg = len(adj.get(cn, set()))
                    if deg > 1:
                        score += 1.0 / math.log(deg)
            else:
                score = float(len(common))

            if score > 0.0:
                predictions.append({
                    "source_id": canonical_id,
                    "target_id": other_cid,
                    "score": round(score, 6),
                    "algorithm": algorithm,
                })

        predictions.sort(key=lambda p: -p["score"])
        return predictions[:limit]
