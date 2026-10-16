"""Graph-aware recommendation engine (GAP-REC-001).

Recommends documents, experts, components and related concepts for any
entity using personalised PageRank (random walk with restart) over the live
graph. Walks are restricted to the supplied seed, so scores reflect real graph
proximity and hub-dampening; every recommendation carries an explanation path
found by BFS over the same graph.

No data is fabricated: results derive only from the store passed in.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any

DOCUMENT_LABELS = frozenset({"Document", "DocumentSection", "KBArticle"})
EXPERT_LABELS = frozenset({"Person"})
COMPONENT_LABELS = frozenset({
    "Service", "APIService", "APIEndpoint", "DesignComponent", "Repository", "Database",
})
CONCEPT_LABELS = frozenset({
    "Tag", "Feature", "BusinessCapability", "BusinessObjective", "Requirement",
    "KnowledgeProduct", "Epic",
})

KINDS: dict[str, frozenset[str]] = {
    "documents": DOCUMENT_LABELS,
    "experts": EXPERT_LABELS,
    "components": COMPONENT_LABELS,
    "concepts": CONCEPT_LABELS,
}


@dataclass
class Recommendation:
    canonical_id: str
    label: str
    name: str
    score: float
    distance: int | None
    path: list[str] = field(default_factory=list)  # alternating cid / edge-label hops
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "label": self.label,
            "name": self.name,
            "score": round(self.score, 6),
            "distance": self.distance,
            "path": self.path,
            "reason": self.reason,
        }


def _display(rec: dict) -> str:
    p = rec["properties"]
    for k in ("display_name", "name", "title", "summary", "tag_name", "issue_key"):
        if p.get(k):
            return str(p[k])
    return rec["canonical_id"]


class GraphRecommender:
    def __init__(self, store: Any, *, restart: float = 0.15, iterations: int = 40,
                 max_hops: int = 4) -> None:
        if not 0 < restart < 1:
            raise ValueError("restart must be in (0, 1)")
        self.store = store
        self.restart = restart
        self.iterations = iterations
        self.max_hops = max_hops

    # -- graph snapshot -----------------------------------------------------
    def _snapshot(self):
        verts = {v["vid"]: v for v in self.store.find_vertices(limit=1_000_000)}
        adj: dict[str, list[tuple[str, str]]] = {vid: [] for vid in verts}
        for e in self.store.find_edges(limit=1_000_000):
            a, b = e["out_v"], e["in_v"]
            if a in verts and b in verts and a != b:
                adj[a].append((b, f"{e['label']}"))
                adj[b].append((a, f"~{e['label']}"))
        return verts, adj

    def _rwr(self, adj: dict[str, list[tuple[str, str]]], seed: str) -> dict[str, float]:
        rank = {seed: 1.0}
        for _ in range(self.iterations):
            nxt: dict[str, float] = {seed: self.restart}
            for node, mass in rank.items():
                nbrs = adj.get(node, [])
                if not nbrs:
                    nxt[seed] = nxt.get(seed, 0.0) + (1 - self.restart) * mass
                    continue
                share = (1 - self.restart) * mass / len(nbrs)
                for nb, _ in nbrs:
                    nxt[nb] = nxt.get(nb, 0.0) + share
            rank = nxt
        return rank

    def _bfs_paths(self, verts, adj, seed: str) -> dict[str, tuple[int, list[str]]]:
        found: dict[str, tuple[int, list[str]]] = {seed: (0, [verts[seed]["canonical_id"]])}
        q = deque([seed])
        while q:
            cur = q.popleft()
            depth, path = found[cur]
            if depth >= self.max_hops:
                continue
            for nb, lab in sorted(adj[cur], key=lambda x: (x[0], x[1])):
                if nb not in found:
                    found[nb] = (depth + 1, path + [lab, verts[nb]["canonical_id"]])
                    q.append(nb)
        return found

    # -- core -----------------------------------------------------------------
    def recommend(self, canonical_id: str, kind: str, *, limit: int = 10,
                  include_linked: bool = False, min_score: float = 0.0) -> list[Recommendation]:
        if kind not in KINDS:
            raise ValueError(f"unknown recommendation kind {kind!r}; expected {sorted(KINDS)}")
        return self.recommend_labels(canonical_id, KINDS[kind], limit=limit,
                                     include_linked=include_linked, min_score=min_score)

    def recommend_labels(self, canonical_id: str, labels: frozenset[str] | set[str], *,
                         limit: int = 10, include_linked: bool = False,
                         min_score: float = 0.0) -> list[Recommendation]:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        seed_rec = self.store.get_vertex_by_canonical_id(canonical_id)
        if seed_rec is None:
            raise KeyError(f"unknown entity: {canonical_id}")
        verts, adj = self._snapshot()
        seed = seed_rec["vid"]
        rank = self._rwr(adj, seed)
        paths = self._bfs_paths(verts, adj, seed)
        linked = {nb for nb, _ in adj[seed]}
        out: list[Recommendation] = []
        for vid, score in rank.items():
            rec = verts.get(vid)
            if rec is None or vid == seed or rec["label"] not in labels:
                continue
            if rec["properties"].get("deleted_at"):
                continue
            if vid in linked and not include_linked:
                continue
            if score <= min_score:
                continue
            depth, path = paths.get(vid, (None, []))
            out.append(Recommendation(
                canonical_id=rec["canonical_id"], label=rec["label"], name=_display(rec),
                score=score, distance=depth, path=path,
                reason=(f"{depth}-hop graph proximity via {' '.join(path[1::2]) or 'n/a'}"
                        if depth else "reachable by random walk"),
            ))
        out.sort(key=lambda r: (-r.score, r.canonical_id))
        return out[:limit]

    # -- typed convenience API -------------------------------------------------
    def recommend_documents(self, cid: str, **kw: Any) -> list[Recommendation]:
        return self.recommend(cid, "documents", **kw)

    def recommend_experts(self, cid: str, **kw: Any) -> list[Recommendation]:
        return self.recommend(cid, "experts", **kw)

    def recommend_components(self, cid: str, **kw: Any) -> list[Recommendation]:
        return self.recommend(cid, "components", **kw)

    def recommend_concepts(self, cid: str, **kw: Any) -> list[Recommendation]:
        return self.recommend(cid, "concepts", **kw)

    def recommend_all(self, cid: str, *, limit: int = 5) -> dict[str, list[dict]]:
        return {k: [r.to_dict() for r in self.recommend(cid, k, limit=limit)] for k in KINDS}
