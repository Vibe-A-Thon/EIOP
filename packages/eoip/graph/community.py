"""Community detection algorithms: label propagation and Louvain.

Pure-Python implementations operating on the GraphStore port.
No external graph-library dependencies.
"""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class CommunityResult:
    """Result of a community detection run."""

    communities: list[dict[str, Any]] = field(default_factory=list)
    modularity: float = 0.0
    algorithm: str = ""

    @property
    def community_count(self) -> int:
        return len(self.communities)

    def to_dict(self) -> dict[str, Any]:
        return {
            "communities": self.communities,
            "community_count": self.community_count,
            "modularity": self.modularity,
            "algorithm": self.algorithm,
        }


class CommunityDetectionEngine:
    """Community detection over an EOIP GraphStore."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_undirected_adjacency(self) -> tuple[dict[str, set[str]], int]:
        """Return (adjacency-by-canonical_id, total_edge_count).

        Each edge is counted once for the total but appears in both
        directions in the adjacency dict.
        """
        adj: dict[str, set[str]] = defaultdict(set)
        total_edges = 0

        vertices = self._store.find_vertices(limit=50_000)
        vid_to_cid: dict[str, str] = {}
        for v in vertices:
            cid = v["properties"]["canonical_id"]
            vid_to_cid[v["vid"]] = cid
            adj.setdefault(cid, set())

        for v in vertices:
            src_cid = vid_to_cid[v["vid"]]
            for edge in self._store.edges_from(v["vid"]):
                tgt_vid = edge["in_v"]
                tgt_cid = vid_to_cid.get(tgt_vid)
                if tgt_cid is None:
                    tgt = self._store.get_vertex(tgt_vid)
                    if tgt is None:
                        continue
                    tgt_cid = tgt["properties"]["canonical_id"]
                    vid_to_cid[tgt_vid] = tgt_cid
                if src_cid != tgt_cid:
                    adj[src_cid].add(tgt_cid)
                    adj[tgt_cid].add(src_cid)
                    total_edges += 1

        return adj, total_edges

    @staticmethod
    def _modularity(
        adj: dict[str, set[str]],
        labels: dict[str, int],
        total_edges: int,
    ) -> float:
        """Newman-Girvan modularity Q."""
        if total_edges == 0:
            return 0.0
        m2 = 2 * total_edges
        q = 0.0
        for node, neighbors in adj.items():
            ki = len(neighbors)
            for nbr in neighbors:
                if labels[node] == labels[nbr]:
                    kj = len(adj[nbr])
                    q += 1.0 - (ki * kj) / m2
        return q / m2

    @staticmethod
    def _labels_to_communities(labels: dict[str, int]) -> list[dict[str, Any]]:
        """Convert node->label mapping to community list."""
        groups: dict[int, list[str]] = defaultdict(list)
        for node, label in labels.items():
            groups[label].append(node)

        result = []
        for idx, (label_id, members) in enumerate(
            sorted(groups.items(), key=lambda kv: -len(kv[1]))
        ):
            result.append(
                {"id": idx, "members": sorted(members), "size": len(members)}
            )
        return result

    # ------------------------------------------------------------------
    # Algorithms
    # ------------------------------------------------------------------

    def label_propagation(self, max_iterations: int = 20) -> CommunityResult:
        """Asynchronous label propagation community detection.

        Each node starts with a unique label; on each iteration every node
        adopts the most frequent label among its neighbours (ties broken
        randomly). Converges when no label changes.
        """
        adj, total_edges = self._build_undirected_adjacency()
        nodes = list(adj.keys())
        if not nodes:
            return CommunityResult(communities=[], modularity=0.0, algorithm="label_propagation")

        labels: dict[str, int] = {node: i for i, node in enumerate(nodes)}

        for _ in range(max_iterations):
            changed = False
            order = list(nodes)
            random.shuffle(order)
            for node in order:
                neighbors = adj[node]
                if not neighbors:
                    continue
                freq: dict[int, int] = defaultdict(int)
                for nbr in neighbors:
                    freq[labels[nbr]] += 1
                max_count = max(freq.values())
                candidates = [lbl for lbl, cnt in freq.items() if cnt == max_count]
                chosen = random.choice(candidates)
                if labels[node] != chosen:
                    labels[node] = chosen
                    changed = True
            if not changed:
                break

        communities = self._labels_to_communities(labels)
        mod = self._modularity(adj, labels, total_edges)

        return CommunityResult(
            communities=communities,
            modularity=round(mod, 6),
            algorithm="label_propagation",
        )

    def leiden(self, resolution: float = 1.0, max_iterations: int = 10) -> CommunityResult:
        """Leiden algorithm: local moving + refinement + aggregation.

        Guarantees connected communities unlike Louvain.
        """
        adj, total_edges = self._build_undirected_adjacency()
        nodes = list(adj.keys())
        if not nodes:
            return CommunityResult(communities=[], modularity=0.0, algorithm="leiden")
        if total_edges == 0:
            communities = [{"id": i, "members": [n], "size": 1} for i, n in enumerate(nodes)]
            return CommunityResult(communities=communities, modularity=0.0, algorithm="leiden")

        m2 = 2.0 * total_edges
        node_comm: dict[str, int] = {n: i for i, n in enumerate(nodes)}
        node_degree: dict[str, int] = {n: len(adj[n]) for n in nodes}

        for _ in range(max_iterations):
            moved = False
            # Phase 1: local moving
            order = list(nodes)
            random.shuffle(order)
            for node in order:
                cur = node_comm[node]
                ki = node_degree[node]
                nbr_edges: dict[int, int] = defaultdict(int)
                for nbr in adj[node]:
                    nbr_edges[node_comm[nbr]] += 1
                own_edges = nbr_edges.get(cur, 0)
                comm_deg: dict[int, int] = defaultdict(int)
                for n in nodes:
                    comm_deg[node_comm[n]] += node_degree[n]
                sigma_own = comm_deg[cur] - ki
                best_delta, best_comm = 0.0, cur
                for c, ki_c in nbr_edges.items():
                    if c == cur:
                        continue
                    sigma_c = comm_deg[c]
                    delta = (ki_c - own_edges) / total_edges - resolution * ki * (sigma_c - sigma_own) / (m2 * total_edges)
                    if delta > best_delta:
                        best_delta = delta
                        best_comm = c
                if best_comm != cur:
                    node_comm[node] = best_comm
                    moved = True

            # Phase 2: refinement — split disconnected sub-communities
            comm_groups: dict[int, list[str]] = defaultdict(list)
            for n in nodes:
                comm_groups[node_comm[n]].append(n)
            remap: dict[str, int] = {}
            next_id = 0
            for members in comm_groups.values():
                visited: set[str] = set()
                for start in members:
                    if start in visited:
                        continue
                    component: list[str] = []
                    queue = [start]
                    visited.add(start)
                    while queue:
                        v = queue.pop()
                        component.append(v)
                        for nbr in adj.get(v, set()):
                            if nbr in visited or nbr not in set(members):
                                continue
                            visited.add(nbr)
                            queue.append(nbr)
                    for n in component:
                        remap[n] = next_id
                    next_id += 1
            node_comm = remap
            if not moved:
                break

        final_labels = node_comm
        communities = self._labels_to_communities(final_labels)
        mod = self._modularity(adj, final_labels, total_edges)
        return CommunityResult(communities=communities, modularity=round(mod, 6), algorithm="leiden")

    def louvain(self, resolution: float = 1.0) -> CommunityResult:
        """Simplified Louvain modularity optimisation (single pass).

        Greedily merges each node into the neighbouring community that
        yields the largest modularity gain. Runs until no beneficial
        move remains.
        """
        adj, total_edges = self._build_undirected_adjacency()
        nodes = list(adj.keys())
        if not nodes:
            return CommunityResult(communities=[], modularity=0.0, algorithm="louvain")

        if total_edges == 0:
            communities = [
                {"id": i, "members": [n], "size": 1} for i, n in enumerate(nodes)
            ]
            return CommunityResult(communities=communities, modularity=0.0, algorithm="louvain")

        m2 = 2.0 * total_edges

        # Each node starts in its own community
        node_comm: dict[str, int] = {node: i for i, node in enumerate(nodes)}
        comm_nodes: dict[int, set[str]] = {i: {node} for i, node in enumerate(nodes)}
        # Sum of degrees of nodes in each community
        comm_degree: dict[int, int] = {}
        node_degree: dict[str, int] = {}
        for node in nodes:
            deg = len(adj[node])
            node_degree[node] = deg
            comm_degree[node_comm[node]] = deg

        improved = True
        while improved:
            improved = False
            order = list(nodes)
            random.shuffle(order)
            for node in order:
                cur_comm = node_comm[node]
                ki = node_degree[node]

                # Count edges to each neighbouring community
                nbr_comm_edges: dict[int, int] = defaultdict(int)
                for nbr in adj[node]:
                    nbr_comm_edges[node_comm[nbr]] += 1

                # Remove node from its current community temporarily
                edges_to_own = nbr_comm_edges.get(cur_comm, 0)
                sigma_own = comm_degree[cur_comm] - ki

                best_delta = 0.0
                best_comm = cur_comm

                for c, ki_c in nbr_comm_edges.items():
                    if c == cur_comm:
                        continue
                    sigma_c = comm_degree[c]
                    # Delta Q for moving node into community c
                    delta = (ki_c - edges_to_own) / total_edges - resolution * ki * (sigma_c - sigma_own) / (m2 * total_edges)
                    if delta > best_delta:
                        best_delta = delta
                        best_comm = c

                if best_comm != cur_comm:
                    # Move node
                    comm_nodes[cur_comm].discard(node)
                    comm_degree[cur_comm] -= ki
                    if not comm_nodes[cur_comm]:
                        del comm_nodes[cur_comm]
                        del comm_degree[cur_comm]

                    node_comm[node] = best_comm
                    comm_nodes.setdefault(best_comm, set()).add(node)
                    comm_degree[best_comm] = comm_degree.get(best_comm, 0) + ki
                    improved = True

        # Relabel communities sequentially
        final_labels: dict[str, int] = {}
        comm_remap: dict[int, int] = {}
        next_id = 0
        for node in nodes:
            c = node_comm[node]
            if c not in comm_remap:
                comm_remap[c] = next_id
                next_id += 1
            final_labels[node] = comm_remap[c]

        communities = self._labels_to_communities(final_labels)
        mod = self._modularity(adj, final_labels, total_edges)

        return CommunityResult(
            communities=communities,
            modularity=round(mod, 6),
            algorithm="louvain",
        )

    def label_community(self, member_ids: list[str]) -> str:
        """Generate a human-readable label for a community.

        Uses the top-3 most common vertex labels and top-2 most common
        property values (name or display_name) to build a descriptive label.
        """
        label_counts: dict[str, int] = defaultdict(int)
        name_counts: dict[str, int] = defaultdict(int)
        for cid in member_ids:
            v = self._store.get_vertex_by_canonical_id(cid)
            if v is None:
                continue
            label_counts[v["label"]] += 1
            props = v.get("properties", v)
            name = props.get("name") or props.get("display_name") or ""
            if name:
                for part in name.replace("-", " ").replace("_", " ").split():
                    if len(part) > 2:
                        name_counts[part.lower()] += 1

        top_labels = sorted(label_counts.items(), key=lambda x: -x[1])[:3]
        top_names = sorted(name_counts.items(), key=lambda x: -x[1])[:2]

        label_str = ", ".join(l for l, _ in top_labels)
        name_str = ", ".join(n for n, _ in top_names)
        if name_str:
            return f"{label_str}: {name_str}"
        return label_str or "Unknown"

    def detect_with_labels(
        self, algorithm: str = "label_propagation", resolution: float = 1.0
    ) -> CommunityResult:
        """Run detection and auto-label each community."""
        if algorithm == "louvain":
            result = self.louvain(resolution=resolution)
        else:
            result = self.label_propagation()

        for comm in result.communities:
            comm["auto_label"] = self.label_community(comm["members"][:50])

        return result
