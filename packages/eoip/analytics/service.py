"""GAP-GDS: Local graph analytics service.

A pluggable analytics API over the GraphStore.  Algorithms are registered in
an :class:`AlgorithmRegistry` (built-ins plus user plugins) and executed via
:class:`GraphAnalyticsService`, which projects the store into an adjacency
map once per call and returns uniform, JSON-serialisable results.

Everything runs locally (pure Python, no external graph engine).
"""

from __future__ import annotations

import heapq
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Protocol
from collections.abc import Callable

from eoip.analytics.algorithms import (
    AdjacencyBuilder,
    BetweennessCentrality,
    ClosenessCentrality,
    DegreeCentrality,
    LeidenCommunityDetection,
    PageRank,
)
from eoip.graph.store import GraphStore

Adjacency = dict[str, dict[str, float]]


class UnknownAlgorithm(KeyError):
    """Raised when an algorithm name is not registered."""


@dataclass
class AnalyticsResult:
    algorithm: str
    category: str
    values: Any
    node_count: int = 0
    edge_count: int = 0
    duration_ms: float = 0.0
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "category": self.category,
            "values": self.values,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "duration_ms": round(self.duration_ms, 3),
            "parameters": self.parameters,
        }


class AnalyticsAlgorithm(Protocol):
    name: str
    category: str
    directed: bool

    def run(self, adj: Adjacency, **params: Any) -> Any: ...


@dataclass
class FunctionAlgorithm:
    """Adapter that registers a plain function as an algorithm plugin."""

    name: str
    category: str
    fn: Callable[..., Any]
    directed: bool = False
    description: str = ""

    def run(self, adj: Adjacency, **params: Any) -> Any:
        return self.fn(adj, **params)


# --------------------------------------------------------------------------
# Built-in algorithms (operate on a symmetric/directed adjacency map)
# --------------------------------------------------------------------------
def connected_components(adj: Adjacency) -> dict[str, int]:
    comp: dict[str, int] = {}
    cid = 0
    for start in sorted(adj):
        if start in comp:
            continue
        comp[start] = cid
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for w in adj.get(v, {}):
                if w not in comp:
                    comp[w] = cid
                    queue.append(w)
        cid += 1
    return comp


def shortest_path(adj: Adjacency, *, source: str, target: str) -> dict[str, Any]:
    """Dijkstra over non-negative edge weights."""
    if source not in adj or target not in adj:
        return {"found": False, "path": [], "distance": None}
    dist = {source: 0.0}
    prev: dict[str, str] = {}
    heap: list[tuple[float, str]] = [(0.0, source)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist.get(v, float("inf")):
            continue
        if v == target:
            break
        for w, weight in adj.get(v, {}).items():
            if weight < 0:
                raise ValueError("negative edge weights are not supported")
            nd = d + weight
            if nd < dist.get(w, float("inf")):
                dist[w] = nd
                prev[w] = v
                heapq.heappush(heap, (nd, w))
    if target not in dist:
        return {"found": False, "path": [], "distance": None}
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()
    return {"found": True, "path": path, "distance": dist[target]}


def triangle_count(adj: Adjacency) -> dict[str, int]:
    nbrs = {v: set(n) - {v} for v, n in adj.items()}
    return {
        v: sum(1 for a in n for b in n if a < b and b in nbrs.get(a, ()))
        for v, n in nbrs.items()
    }


def clustering_coefficient(adj: Adjacency) -> dict[str, float]:
    tri = triangle_count(adj)
    out: dict[str, float] = {}
    for v, n in adj.items():
        k = len(set(n) - {v})
        out[v] = round(2.0 * tri[v] / (k * (k - 1)), 8) if k > 1 else 0.0
    return out


def k_core(adj: Adjacency) -> dict[str, int]:
    """Core number of every node (Batagelj-Zaversnik peeling)."""
    nbrs = {v: set(n) - {v} for v, n in adj.items()}
    degree = {v: len(n) for v, n in nbrs.items()}
    core: dict[str, int] = {}
    remaining = set(nbrs)
    k = 0
    while remaining:
        v = min(remaining, key=lambda x: (degree[x], x))
        k = max(k, degree[v])
        core[v] = k
        remaining.discard(v)
        for w in nbrs[v]:
            if w in remaining:
                degree[w] -= 1
    return core


def label_propagation(adj: Adjacency, *, max_iterations: int = 50) -> dict[str, int]:
    """Deterministic label propagation (ties broken by smallest label)."""
    nodes = sorted(adj)
    label = {v: i for i, v in enumerate(nodes)}
    for _ in range(max_iterations):
        changed = False
        for v in nodes:
            counts: dict[int, float] = defaultdict(float)
            for w, weight in adj.get(v, {}).items():
                if w != v:
                    counts[label[w]] += weight
            if not counts:
                continue
            best = min(counts, key=lambda lbl: (-counts[lbl], lbl))
            if best != label[v]:
                label[v] = best
                changed = True
        if not changed:
            break
    remap = {old: new for new, old in enumerate(sorted(set(label.values())))}
    return {v: remap[lbl] for v, lbl in label.items()}


def jaccard_similarity(adj: Adjacency, *, node: str, top_k: int = 10) -> list[dict[str, Any]]:
    if node not in adj:
        return []
    base = set(adj[node]) - {node}
    scored = []
    for other, n in adj.items():
        if other == node:
            continue
        other_set = set(n) - {other}
        union = base | other_set
        if not union:
            continue
        score = len(base & other_set) / len(union)
        if score > 0:
            scored.append({"node": other, "score": round(score, 8)})
    scored.sort(key=lambda r: (-r["score"], r["node"]))
    return scored[:top_k]


def _scores(result: Any) -> dict[str, float]:
    return dict(result.scores)


class AlgorithmRegistry:
    """Thread-safe registry of analytics algorithms (built-in + plugins)."""

    def __init__(self, *, with_builtins: bool = True) -> None:
        self._algos: dict[str, AnalyticsAlgorithm] = {}
        self._lock = threading.RLock()
        if with_builtins:
            self._register_builtins()

    def register(self, algo: AnalyticsAlgorithm, *, replace: bool = False) -> None:
        with self._lock:
            if algo.name in self._algos and not replace:
                raise ValueError(f"algorithm already registered: {algo.name}")
            self._algos[algo.name] = algo

    def register_function(
        self,
        name: str,
        fn: Callable[..., Any],
        *,
        category: str = "custom",
        directed: bool = False,
        replace: bool = False,
    ) -> None:
        self.register(FunctionAlgorithm(name, category, fn, directed), replace=replace)

    def unregister(self, name: str) -> bool:
        with self._lock:
            return self._algos.pop(name, None) is not None

    def get(self, name: str) -> AnalyticsAlgorithm:
        with self._lock:
            try:
                return self._algos[name]
            except KeyError as exc:
                raise UnknownAlgorithm(name) from exc

    def catalog(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {"name": a.name, "category": a.category, "directed": a.directed}
                for a in sorted(self._algos.values(), key=lambda a: (a.category, a.name))
            ]

    def _register_builtins(self) -> None:
        pr, bc, cc = PageRank(), BetweennessCentrality(), ClosenessCentrality()
        dc, leiden = DegreeCentrality(), LeidenCommunityDetection()
        builtins: list[FunctionAlgorithm] = [
            FunctionAlgorithm("pagerank", "centrality",
                              lambda a, **p: _scores(pr.compute(a, **p)), directed=True),
            FunctionAlgorithm("betweenness", "centrality",
                              lambda a, **p: _scores(bc.compute(a, **p))),
            FunctionAlgorithm("closeness", "centrality",
                              lambda a, **p: _scores(cc.compute(a, **p))),
            FunctionAlgorithm("degree", "centrality",
                              lambda a, **p: _scores(dc.compute(a, **p))),
            FunctionAlgorithm("leiden", "community",
                              lambda a, **p: dict(leiden.compute(a, **p).communities)),
            FunctionAlgorithm("label_propagation", "community", label_propagation),
            FunctionAlgorithm("connected_components", "structure", connected_components),
            FunctionAlgorithm("k_core", "structure", k_core),
            FunctionAlgorithm("triangle_count", "structure", triangle_count),
            FunctionAlgorithm("clustering_coefficient", "structure", clustering_coefficient),
            FunctionAlgorithm("shortest_path", "path", shortest_path, directed=True),
            FunctionAlgorithm("jaccard_similarity", "similarity", jaccard_similarity),
        ]
        for algo in builtins:
            self.register(algo)


class GraphAnalyticsService:
    """Runs registered algorithms against a GraphStore projection."""

    def __init__(self, store: GraphStore, registry: AlgorithmRegistry | None = None) -> None:
        self.store = store
        self.registry = registry or AlgorithmRegistry()

    def catalog(self) -> list[dict[str, Any]]:
        return self.registry.catalog()

    def run(
        self,
        name: str,
        *,
        edge_labels: list[str] | None = None,
        **params: Any,
    ) -> AnalyticsResult:
        algo = self.registry.get(name)
        started = time.monotonic()
        adj, edge_count = AdjacencyBuilder.build_from_store(
            self.store, directed=algo.directed, edge_labels=edge_labels,
        )
        values = algo.run(adj, **params)
        return AnalyticsResult(
            algorithm=algo.name,
            category=algo.category,
            values=values,
            node_count=len(adj),
            edge_count=edge_count,
            duration_ms=(time.monotonic() - started) * 1000,
            parameters={"edge_labels": edge_labels, **params},
        )

    def run_many(self, names: list[str], **kwargs: Any) -> dict[str, AnalyticsResult]:
        return {n: self.run(n, **kwargs) for n in names}
