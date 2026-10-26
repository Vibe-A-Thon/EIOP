"""Link-prediction heuristics over an existing graph adjacency.

Deterministic structural scoring — common neighbors, Adamic-Adar, and
preferential attachment — over non-edge candidate pairs (second-hop pairs).
High-scoring pairs become ``PREDICTED_LINK`` proposals into the review
queue; nothing is written without validation (enrichment loop applies
approved additions only).
"""

from __future__ import annotations

from collections.abc import Mapping
from math import log

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import GraphDelta, ProposedEdge


class LinkPredictionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: str = Field(default="adamic_adar")  # common_neighbors | adamic_adar | preferential_attachment
    top_k: int = Field(default=500, ge=1)
    max_candidates_per_node: int = Field(default=500, ge=1)
    min_score: float = Field(default=0.0)


def _candidates(adj: Mapping[str, set[str]]) -> set[tuple[str, str]]:
    """Second-hop pairs that are not already edges."""
    out: set[tuple[str, str]] = set()
    for a in adj:
        for mid in adj[a]:
            for b in adj.get(mid, ()):
                if b == a or b in adj[a]:
                    continue
                out.add((a, b) if a < b else (b, a))
    return out


def score_pairs(
    adjacency: Mapping[str, set[str]] | Mapping[str, list[str]],
    config: LinkPredictionConfig | None = None,
) -> GraphDelta:
    """Score candidate pairs with the configured heuristic."""
    cfg = config or LinkPredictionConfig()
    adj = {k: set(v) for k, v in adjacency.items()}
    degrees = {n: len(v) for n, v in adj.items()}

    proposals: list[ProposedEdge] = []
    for a, b in sorted(_candidates(adj)):
        common = adj[a] & adj[b]
        if cfg.method == "common_neighbors":
            score = float(len(common))
        elif cfg.method == "adamic_adar":
            score = sum(1.0 / log(degrees[c] + 1) for c in common if degrees.get(c, 0) > 1)
        elif cfg.method == "preferential_attachment":
            score = float(degrees[a] * degrees[b])
        else:
            raise ValueError(f"Unknown link-prediction method: {cfg.method}")
        if score < cfg.min_score or score <= 0:
            continue
        proposals.append(
            ProposedEdge.make(
                "PREDICTED_LINK",
                a,
                b,
                score=score,
                method=f"link-prediction:{cfg.method}",
                common_neighbors=sorted(common),
            )
        )

    proposals.sort(key=lambda e: (-e.score, e.from_id, e.to_id))
    proposals = proposals[: cfg.top_k]
    return GraphDelta.make("link-prediction", repr((cfg.model_dump(), sorted(adj))), edges=proposals)
