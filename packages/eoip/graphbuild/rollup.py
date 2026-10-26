"""Hierarchical community rollup above a flat Leiden partition.

``eoip.graph.community.CommunityDetectionEngine.leiden`` produces a flat
partition; this module rolls it into a summary hierarchy by repeatedly
coarsening the quotient graph (deterministic label propagation in pure
Python): each level clusters the previous level's communities, so original
entities get nested summary nodes. Levels stop at one community or
``max_levels``.

Level 0 is the *base partition* (typically Leiden output). When no base
partition is supplied, connected components are used as level 0.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import _urn


class RollupLevel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level: int
    communities: list[dict[str, Any]] = Field(default_factory=list)
    """Each community: {community_id, members, size}."""


class HierarchicalRollup(BaseModel):
    """Multi-level community summary."""

    model_config = ConfigDict(extra="forbid")

    rollup_id: str
    levels: list[RollupLevel] = Field(default_factory=list)
    entity_to_leaf: dict[str, str] = Field(default_factory=dict)
    """Entity id -> its level-0 (base partition) community id."""

    @property
    def depth(self) -> int:
        return len(self.levels)


def _label_propagation(adj: dict[str, set[str]], max_iterations: int = 20) -> dict[str, int]:
    labels = {node: idx for idx, node in enumerate(sorted(adj))}
    for _ in range(max_iterations):
        changed = False
        for node in sorted(adj):
            neighbors = adj[node] - {node}
            if not neighbors:
                continue
            counts: dict[int, int] = {}
            for other in neighbors:
                counts[labels[other]] = counts.get(labels[other], 0) + 1
            best = max(sorted(counts), key=lambda lb: counts[lb])
            if best != labels[node]:
                labels[node] = best
                changed = True
        if not changed:
            break
    return labels


def _connected_components(adj: dict[str, set[str]]) -> dict[str, int]:
    labels: dict[str, int] = {}
    component = 0
    for start in sorted(adj):
        if start in labels:
            continue
        stack = [start]
        labels[start] = component
        while stack:
            for other in adj[stack.pop()]:
                if other not in labels:
                    labels[other] = component
                    stack.append(other)
        component += 1
    return labels


def build_hierarchical_rollup(
    adjacency: Mapping[str, set[str]] | Mapping[str, list[str]],
    *,
    base_partition: Mapping[str, str] | None = None,
    max_levels: int = 4,
) -> HierarchicalRollup:
    """Roll an entity adjacency + flat partition into nested summaries.

    ``adjacency`` maps entity id -> neighbor ids (treated as undirected).
    ``base_partition`` maps entity id -> its Leiden community id; when absent,
    connected components become the level-0 partition. Deeper levels are
    addressable through ``levels[i].communities[*].members``.
    """
    # Symmetrize.
    current_adj: dict[str, set[str]] = {str(k): set() for k in adjacency}
    for k, v in adjacency.items():
        for n in v:
            current_adj[str(k)].add(str(n))
            current_adj.setdefault(str(n), set()).add(str(k))

    if base_partition is not None:
        base_labels = {str(k): str(v) for k, v in base_partition.items()}
    else:
        base_labels = {node: str(label) for node, label in _connected_components(current_adj).items()}
    # Isolated entities missing from the adjacency map still appear via base_partition.
    for node in base_labels:
        current_adj.setdefault(node, set())

    levels: list[RollupLevel] = []
    entity_to_leaf = dict(sorted(base_labels.items()))
    level = 0
    current_labels = base_labels

    while current_adj and level < max_levels:
        # Group current nodes by their current label.
        groups: dict[str, list[str]] = {}
        for node in sorted(current_adj):
            groups.setdefault(current_labels.get(node, node), []).append(node)

        communities = []
        for idx, label in enumerate(sorted(groups)):
            members = sorted(groups[label])
            communities.append(
                {
                    "community_id": _urn("community", f"L{level}:{label}"),
                    "members": members,
                    "size": len(members),
                }
            )
        current_to_cid = {node: c["community_id"] for c in communities for node in c["members"]}
        if level == 0:
            entity_to_leaf = dict(sorted(current_to_cid.items()))
        levels.append(RollupLevel(level=level, communities=communities))
        if len(communities) <= 1:
            break

        # Coarsen: quotient graph over community ids; label propagation decides
        # which communities merge at the next level.
        quotient: dict[str, set[str]] = {}
        for node, neighbors in current_adj.items():
            cid = current_to_cid[node]
            bucket = quotient.setdefault(cid, set())
            for other in neighbors:
                other_cid = current_to_cid.get(other)
                if other_cid and other_cid != cid:
                    bucket.add(other_cid)
        merged = _label_propagation({cid: set(neigh) | {cid} for cid, neigh in quotient.items()})
        current_labels = {cid: str(merged[cid]) for cid in quotient}
        current_adj = quotient
        level += 1

    return HierarchicalRollup(
        rollup_id=_urn("rollup", repr(sorted(entity_to_leaf.items()))),
        levels=levels,
        entity_to_leaf=entity_to_leaf,
    )
