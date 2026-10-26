"""Similarity graph construction: kNN edges from an embedding index.

Deterministic cosine-similarity kNN over an in-memory embedding index
(``{entity_id: [float, ...]}``); outputs ``SIMILAR_TO`` edge proposals with
the cosine score. Works against any vector backend the caller already has —
the vector databases themselves are External-gate adapters (§6.5 manifests),
so this builder never speaks to them directly.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import GraphDelta, ProposedEdge


class SimilarityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    k: int = Field(default=5, ge=1)
    min_similarity: float = Field(default=0.5, ge=-1.0, le=1.0)
    include_mutual_only: bool = False


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if not na or not nb:
        return 0.0
    return dot / (na * nb)


def build_similarity_graph(
    embeddings: Mapping[str, list[float]],
    config: SimilarityConfig | None = None,
) -> GraphDelta:
    """Build a kNN similarity graph over an embedding index.

    Ties break on neighbor id for determinism. With ``include_mutual_only``,
    only reciprocal nearest-neighbor pairs are emitted (precision mode).
    """
    cfg = config or SimilarityConfig()
    ids = sorted(embeddings)
    vectors = {i: list(embeddings[i]) for i in ids}

    neighbors: dict[str, list[tuple[str, float]]] = {}
    for i in ids:
        scored = sorted(
            ((j, _cosine(vectors[i], vectors[j])) for j in ids if j != i),
            key=lambda item: (-item[1], item[0]),
        )
        neighbors[i] = [(j, s) for j, s in scored[: cfg.k] if s >= cfg.min_similarity]

    edges: list[ProposedEdge] = []
    for i in ids:
        for j, score in neighbors[i]:
            if cfg.include_mutual_only and i not in {n for n, _ in neighbors.get(j, [])}:
                continue
            if cfg.include_mutual_only and i > j:
                continue  # one proposal per mutual pair
            edges.append(
                ProposedEdge.make(
                    "SIMILAR_TO",
                    i,
                    j,
                    score=score,
                    method="similarity:knn-cosine",
                    k=cfg.k,
                )
            )

    edges.sort(key=lambda e: (e.from_id, -e.score, e.to_id))
    return GraphDelta.make("similarity", repr(sorted(ids)), edges=edges)
