"""Graph metrics engine: centrality, blast radius, and what-if analysis."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from eoip.graph.store import GraphStore


class AffectedItem:
    __slots__ = ("canonical_id", "edge_classes", "evidence_count", "label", "path_depth")

    def __init__(self, canonical_id: str, label: str, path_depth: int,
                 edge_classes: list[str], evidence_count: int = 0):
        self.canonical_id = canonical_id
        self.label = label
        self.path_depth = path_depth
        self.edge_classes = edge_classes
        self.evidence_count = evidence_count

    def to_dict(self) -> dict:
        return {
            "canonical_id": self.canonical_id,
            "label": self.label,
            "path_depth": self.path_depth,
            "edge_classes": self.edge_classes,
            "evidence_count": self.evidence_count,
            "why_included": (
                f"Reached at depth {self.path_depth} via {', '.join(self.edge_classes)}"
                + (f"; {self.evidence_count} evidence link(s)" if self.evidence_count else "")
            ),
        }


class BlastRadiusResult:
    __slots__ = ("affected_details", "affected_ids", "by_depth", "by_type", "risk", "target_id", "total_affected")

    def __init__(self, target_id: str, total_affected: int, by_depth: dict[int, int],
                 by_type: dict[str, int], risk: str, affected_ids: list[str],
                 affected_details: list[AffectedItem] | None = None):
        self.target_id = target_id
        self.total_affected = total_affected
        self.by_depth = by_depth
        self.by_type = by_type
        self.risk = risk
        self.affected_ids = affected_ids
        self.affected_details = affected_details or []

    def to_dict(self) -> dict:
        return {
            "target_id": self.target_id,
            "total_affected": self.total_affected,
            "by_depth": self.by_depth,
            "by_type": self.by_type,
            "risk": self.risk,
            "affected_ids": self.affected_ids,
            "affected_details": [item.to_dict() for item in self.affected_details],
        }


class CentralityMetrics:
    __slots__ = (
        "betweenness",
        "canonical_id",
        "closeness",
        "degree",
        "eigenvector",
        "harmonic",
        "hits_authority",
        "hits_hub",
        "in_degree",
        "katz",
        "out_degree",
        "page_rank",
    )

    def __init__(self, canonical_id: str, degree: int = 0, in_degree: int = 0,
                 out_degree: int = 0, betweenness: float = 0.0,
                 closeness: float = 0.0, page_rank: float = 0.0,
                 eigenvector: float = 0.0, katz: float = 0.0,
                 hits_hub: float = 0.0, hits_authority: float = 0.0,
                 harmonic: float = 0.0):
        self.canonical_id = canonical_id
        self.degree = degree
        self.in_degree = in_degree
        self.out_degree = out_degree
        self.betweenness = betweenness
        self.closeness = closeness
        self.page_rank = page_rank
        self.eigenvector = eigenvector
        self.katz = katz
        self.hits_hub = hits_hub
        self.hits_authority = hits_authority
        self.harmonic = harmonic

    def to_dict(self) -> dict:
        return {
            "canonical_id": self.canonical_id,
            "degree": self.degree,
            "in_degree": self.in_degree,
            "out_degree": self.out_degree,
            "betweenness": round(self.betweenness, 6),
            "closeness": round(self.closeness, 6),
            "page_rank": round(self.page_rank, 6),
            "eigenvector": round(self.eigenvector, 6),
            "katz": round(self.katz, 6),
            "hits_hub": round(self.hits_hub, 6),
            "hits_authority": round(self.hits_authority, 6),
            "harmonic": round(self.harmonic, 6),
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

    def _evidence_count(self, vid: int) -> int:
        return sum(1 for e in self._store.edges_from(vid) if e["label"] == "EVIDENCED_BY")

    def blast_radius(self, canonical_id: str, max_depth: int = 4) -> BlastRadiusResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return BlastRadiusResult(canonical_id, 0, {}, {}, "NONE", [])

        visited: set[int] = {root["vid"]}
        queue: deque[tuple[int, int, list[str]]] = deque([(root["vid"], 0, [])])
        by_depth: dict[int, int] = defaultdict(int)
        by_type: dict[str, int] = defaultdict(int)
        affected_ids: list[str] = []
        affected_details: list[AffectedItem] = []

        while queue:
            vid, depth, edge_trail = queue.popleft()
            if depth >= max_depth:
                continue
            for edge in self._store.edges_from(vid):
                tvid = edge["in_v"]
                if tvid not in visited:
                    visited.add(tvid)
                    target = self._store.get_vertex(tvid)
                    if target:
                        d = depth + 1
                        trail = edge_trail + [edge["label"]]
                        by_depth[d] = by_depth.get(d, 0) + 1
                        by_type[target["label"]] = by_type.get(target["label"], 0) + 1
                        cid = target["properties"]["canonical_id"]
                        affected_ids.append(cid)
                        affected_details.append(AffectedItem(
                            canonical_id=cid,
                            label=target["label"],
                            path_depth=d,
                            edge_classes=list(dict.fromkeys(trail)),
                            evidence_count=self._evidence_count(tvid),
                        ))
                        queue.append((tvid, d, trail))

        total = len(affected_ids)
        total_graph = self._store.count_vertices()
        pct = (total / max(total_graph, 1)) * 100
        risk = "HIGH" if pct > 20 else "MEDIUM" if pct > 5 else "LOW"

        affected_details.sort(key=lambda i: (i.path_depth, -i.evidence_count))
        return BlastRadiusResult(canonical_id, total, dict(by_depth), dict(by_type), risk, affected_ids, affected_details)

    def reverse_impact(self, canonical_id: str, max_depth: int = 4) -> BlastRadiusResult:
        root = self._store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return BlastRadiusResult(canonical_id, 0, {}, {}, "NONE", [])

        visited: set[int] = {root["vid"]}
        queue: deque[tuple[int, int, list[str]]] = deque([(root["vid"], 0, [])])
        by_depth: dict[int, int] = defaultdict(int)
        by_type: dict[str, int] = defaultdict(int)
        affected_ids: list[str] = []
        affected_details: list[AffectedItem] = []

        while queue:
            vid, depth, edge_trail = queue.popleft()
            if depth >= max_depth:
                continue
            for edge in self._store.edges_to(vid):
                svid = edge["out_v"]
                if svid not in visited:
                    visited.add(svid)
                    source = self._store.get_vertex(svid)
                    if source:
                        d = depth + 1
                        trail = edge_trail + [edge["label"]]
                        by_depth[d] = by_depth.get(d, 0) + 1
                        by_type[source["label"]] = by_type.get(source["label"], 0) + 1
                        cid = source["properties"]["canonical_id"]
                        affected_ids.append(cid)
                        affected_details.append(AffectedItem(
                            canonical_id=cid,
                            label=source["label"],
                            path_depth=d,
                            edge_classes=list(dict.fromkeys(trail)),
                            evidence_count=self._evidence_count(svid),
                        ))
                        queue.append((svid, d, trail))

        total = len(affected_ids)
        total_graph = self._store.count_vertices()
        pct = (total / max(total_graph, 1)) * 100
        risk = "HIGH" if pct > 20 else "MEDIUM" if pct > 5 else "LOW"

        affected_details.sort(key=lambda i: (i.path_depth, -i.evidence_count))
        return BlastRadiusResult(canonical_id, total, dict(by_depth), dict(by_type), risk, affected_ids, affected_details)

    def full_centrality(self, canonical_ids: list[str], algorithms: list[str]) -> dict[str, CentralityMetrics]:
        results = self.centrality(canonical_ids)
        need_adj = {"betweenness", "closeness", "pagerank", "eigenvector", "katz", "hits", "harmonic"}
        if need_adj & set(algorithms):
            out_adj, in_adj, _node_map = self._build_adjacency(set(canonical_ids))
            all_nodes = set(out_adj.keys()) | set(in_adj.keys())
            if "betweenness" in algorithms:
                for cid, val in self._betweenness(out_adj, all_nodes).items():
                    if cid in results:
                        results[cid].betweenness = val
            if "closeness" in algorithms:
                for cid, val in self._closeness(out_adj, all_nodes).items():
                    if cid in results:
                        results[cid].closeness = val
            if "pagerank" in algorithms:
                for cid, val in self._pagerank(out_adj, in_adj, all_nodes).items():
                    if cid in results:
                        results[cid].page_rank = val
            if "eigenvector" in algorithms:
                for cid, val in self._eigenvector(out_adj, in_adj, all_nodes).items():
                    if cid in results:
                        results[cid].eigenvector = val
            if "katz" in algorithms:
                for cid, val in self._katz(out_adj, in_adj, all_nodes).items():
                    if cid in results:
                        results[cid].katz = val
            if "hits" in algorithms:
                for cid, (h, a) in self._hits(out_adj, in_adj, all_nodes).items():
                    if cid in results:
                        results[cid].hits_hub = h
                        results[cid].hits_authority = a
            if "harmonic" in algorithms:
                for cid, val in self._harmonic(out_adj, all_nodes).items():
                    if cid in results:
                        results[cid].harmonic = val
        return results

    def _betweenness(self, adj: dict[str, list[str]], nodes: set[str]) -> dict[str, float]:
        cb: dict[str, float] = {n: 0.0 for n in nodes}
        for s in nodes:
            stack: list[str] = []
            pred: dict[str, list[str]] = {n: [] for n in nodes}
            sigma: dict[str, int] = {n: 0 for n in nodes}
            sigma[s] = 1
            dist: dict[str, int] = {n: -1 for n in nodes}
            dist[s] = 0
            queue: list[str] = [s]
            qi = 0
            while qi < len(queue):
                v = queue[qi]; qi += 1
                stack.append(v)
                for w in adj.get(v, []):
                    if w not in dist or dist[w] < 0:
                        dist[w] = dist[v] + 1
                        queue.append(w)
                    if dist.get(w, -1) == dist[v] + 1:
                        sigma[w] = sigma.get(w, 0) + sigma[v]
                        pred[w].append(v)
            delta: dict[str, float] = {n: 0.0 for n in nodes}
            while stack:
                w = stack.pop()
                for v in pred.get(w, []):
                    delta[v] += (sigma.get(v, 1) / max(sigma.get(w, 1), 1)) * (1 + delta.get(w, 0))
                if w != s:
                    cb[w] = cb.get(w, 0) + delta.get(w, 0)
        n = len(nodes)
        norm = max((n - 1) * (n - 2), 1)
        return {k: v / norm for k, v in cb.items()}

    def _closeness(self, adj: dict[str, list[str]], nodes: set[str]) -> dict[str, float]:
        result: dict[str, float] = {}
        for s in nodes:
            dist: dict[str, int] = {s: 0}
            queue: list[str] = [s]
            qi = 0
            while qi < len(queue):
                v = queue[qi]; qi += 1
                for w in adj.get(v, []):
                    if w not in dist:
                        dist[w] = dist[v] + 1
                        queue.append(w)
            total_dist = sum(dist.values())
            reachable = len(dist) - 1
            result[s] = reachable / max(total_dist, 1) if reachable > 0 else 0.0
        return result

    def _pagerank(
        self,
        out_adj: dict[str, list[str]],
        in_adj: dict[str, list[str]],
        nodes: set[str],
        damping: float = 0.85,
        iterations: int = 20,
    ) -> dict[str, float]:
        """PageRank over the undirected dependency view used by KGR centrality."""
        n = len(nodes)
        if n == 0:
            return {}
        neighbors = {
            node: set(out_adj.get(node, [])) | set(in_adj.get(node, []))
            for node in nodes
        }
        pr: dict[str, float] = {node: 1.0 / n for node in nodes}
        for _ in range(iterations):
            dangling = sum(pr[node] for node in nodes if not neighbors[node])
            new_pr: dict[str, float] = {}
            for node in nodes:
                rank = (1 - damping) / n + damping * dangling / n
                for other in neighbors[node]:
                    rank += damping * pr[other] / len(neighbors[other])
                new_pr[node] = rank
            pr = new_pr
        return pr

    def _eigenvector(self, out_adj: dict[str, list[str]], in_adj: dict[str, list[str]],
                     nodes: set[str], iterations: int = 50) -> dict[str, float]:
        """Power iteration for eigenvector centrality on undirected view."""
        if not nodes:
            return {}
        x = {n: 1.0 / len(nodes) for n in nodes}
        for _ in range(iterations):
            x_new: dict[str, float] = {n: 0.0 for n in nodes}
            for n in nodes:
                for nbr in out_adj.get(n, []):
                    if nbr in x_new:
                        x_new[nbr] += x[n]
                for nbr in in_adj.get(n, []):
                    if nbr in x_new:
                        x_new[nbr] += x[n]
            norm = max(sum(v * v for v in x_new.values()) ** 0.5, 1e-12)
            x = {n: v / norm for n, v in x_new.items()}
        return x

    def _katz(self, out_adj: dict[str, list[str]], in_adj: dict[str, list[str]],
              nodes: set[str], alpha: float = 0.1, beta: float = 1.0,
              iterations: int = 50) -> dict[str, float]:
        """Katz centrality approximated via power iteration."""
        if not nodes:
            return {}
        x = {n: beta for n in nodes}
        for _ in range(iterations):
            x_new: dict[str, float] = {n: beta for n in nodes}
            for n in nodes:
                for nbr in out_adj.get(n, []):
                    if nbr in x_new:
                        x_new[nbr] += alpha * x[n]
                for nbr in in_adj.get(n, []):
                    if nbr in x_new:
                        x_new[nbr] += alpha * x[n]
            norm = max(sum(v * v for v in x_new.values()) ** 0.5, 1e-12)
            x = {n: v / norm for n, v in x_new.items()}
        return x

    def _hits(self, out_adj: dict[str, list[str]], in_adj: dict[str, list[str]],
              nodes: set[str], iterations: int = 20) -> dict[str, tuple[float, float]]:
        """HITS hub and authority scores."""
        if not nodes:
            return {}
        hub = {n: 1.0 for n in nodes}
        auth = {n: 1.0 for n in nodes}
        for _ in range(iterations):
            new_auth: dict[str, float] = {n: 0.0 for n in nodes}
            for n in nodes:
                for src in in_adj.get(n, []):
                    if src in hub:
                        new_auth[n] += hub[src]
            norm_a = max(sum(v * v for v in new_auth.values()) ** 0.5, 1e-12)
            auth = {n: v / norm_a for n, v in new_auth.items()}
            new_hub: dict[str, float] = {n: 0.0 for n in nodes}
            for n in nodes:
                for tgt in out_adj.get(n, []):
                    if tgt in auth:
                        new_hub[n] += auth[tgt]
            norm_h = max(sum(v * v for v in new_hub.values()) ** 0.5, 1e-12)
            hub = {n: v / norm_h for n, v in new_hub.items()}
        return {n: (hub[n], auth[n]) for n in nodes}

    def _harmonic(self, adj: dict[str, list[str]], nodes: set[str]) -> dict[str, float]:
        """Harmonic centrality: sum of inverse shortest-path distances."""
        result: dict[str, float] = {}
        n = len(nodes)
        for s in nodes:
            dist: dict[str, int] = {s: 0}
            queue: list[str] = [s]
            qi = 0
            while qi < len(queue):
                v = queue[qi]; qi += 1
                for w in adj.get(v, []):
                    if w not in dist:
                        dist[w] = dist[v] + 1
                        queue.append(w)
            total = sum(1.0 / d for d in dist.values() if d > 0)
            result[s] = total / max(n - 1, 1) if n > 1 else 0.0
        return result

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
        from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS
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

    def k_core_decomposition(self) -> dict[int, list[str]]:
        """Find k-core subgraphs. Returns {k: [canonical_ids]}."""
        out_adj, in_adj, node_map = self._build_adjacency()
        all_nodes = set(out_adj.keys()) | set(in_adj.keys()) | set(node_map.keys())
        if not all_nodes:
            return {}
        degree: dict[str, int] = {}
        for n in all_nodes:
            degree[n] = len(set(out_adj.get(n, [])) | set(in_adj.get(n, [])))
        removed: set[str] = set()
        core_number: dict[str, int] = {}
        max_deg = max(degree.values()) if degree else 0
        for k in range(max_deg + 1):
            changed = True
            while changed:
                changed = False
                for n in list(all_nodes - removed):
                    live_neighbors = (set(out_adj.get(n, [])) | set(in_adj.get(n, []))) - removed
                    if len(live_neighbors) < k:
                        removed.add(n)
                        core_number[n] = max(k - 1, 0)
                        changed = True
        for n in all_nodes - removed:
            core_number[n] = max_deg
        result: dict[int, list[str]] = {}
        for node, k in core_number.items():
            if k not in result:
                result[k] = []
            result[k].append(node)
        return result

    def connected_components(self) -> list[list[str]]:
        """BFS component detection on undirected view. Returns list of components."""
        out_adj, in_adj, node_map = self._build_adjacency()
        all_nodes = set(out_adj.keys()) | set(in_adj.keys()) | set(node_map.keys())
        if not all_nodes:
            return []
        visited: set[str] = set()
        components: list[list[str]] = []
        for start in all_nodes:
            if start in visited:
                continue
            component: list[str] = []
            queue = deque([start])
            visited.add(start)
            while queue:
                node = queue.popleft()
                component.append(node)
                for nbr in set(out_adj.get(node, [])) | set(in_adj.get(node, [])):
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
            components.append(component)
        components.sort(key=len, reverse=True)
        return components

    def degree_distribution(self) -> dict[int, int]:
        """Histogram of degree values. Returns {degree: count}."""
        out_adj, in_adj, node_map = self._build_adjacency()
        all_nodes = set(out_adj.keys()) | set(in_adj.keys()) | set(node_map.keys())
        if not all_nodes:
            return {}
        dist: dict[int, int] = {}
        for n in all_nodes:
            deg = len(set(out_adj.get(n, [])) | set(in_adj.get(n, [])))
            dist[deg] = dist.get(deg, 0) + 1
        return dict(sorted(dist.items()))

    def graph_schema(self) -> dict[str, Any]:
        from eoip.ontology.manifest import (
            DOMAINS,
            EDGE_LABELS,
            INDEXES,
            ONTOLOGY_VERSION,
            PROPERTY_KEYS,
            SCHEMA_VERSION,
            VERTEX_LABELS,
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
