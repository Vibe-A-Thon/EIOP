"""Multi-Paradigm Semantic Query Decomposition, Synthesizer & Multi-Engine Dispatch Framework.

Unifies 5 cognitive query paradigms over live enterprise data:
1. Deterministic Kernel: Strict topological GraphStore traversal and schema filtering
2. Probabilistic Kernel: Term frequency & vector cosine similarity across entity properties
3. Heuristic Kernel: Weighted path search (A* / Dijkstra) over relationship trust and coupling weights
4. Stochastic Kernel: Monte Carlo path sampling over network topologies
5. Non-Deterministic Kernel: Sovereign Cognitive Narrator multi-perspective synthesis
"""

from __future__ import annotations

import heapq
import math
import random
import re
from dataclasses import dataclass, field
from typing import Any

from eoip.brain.cognitive_narrator import CognitiveNarrator
from eoip.graph.store import GraphStore


@dataclass
class KernelResult:
    paradigm: str
    execution_time_ms: float
    nodes_found: int
    edges_found: int
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class MultiParadigmResponse:
    query: str
    target_canonical_ids: list[str]
    deterministic_subgraph: dict[str, Any]
    probabilistic_matches: list[dict[str, Any]]
    heuristic_paths: list[dict[str, Any]]
    stochastic_metrics: dict[str, Any]
    cognitive_narration: dict[str, Any]
    kernel_breakdown: list[dict[str, Any]]


class MultiParadigmQueryDispatcher:
    """Dispatches queries across 5 heterogeneous execution kernels over live enterprise graph data."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store
        self.narrator = CognitiveNarrator(store=store)

    def execute(
        self,
        query: str,
        seed_canonical_ids: list[str] | None = None,
        max_depth: int = 2,
        monte_carlo_samples: int = 50,
    ) -> MultiParadigmResponse:
        """Executes all 5 query paradigms against the live graph store and fuses the results."""
        import time

        seeds = list(seed_canonical_ids or [])
        kernels: list[KernelResult] = []

        # ---------------------------------------------------------
        # 1. Deterministic Kernel: topological search & entity retrieval
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        det_nodes: dict[str, dict[str, Any]] = {}
        det_edges: list[dict[str, Any]] = []

        # If no seeds provided, search vertices matching query tokens
        if not seeds:
            tokens = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 2]
            all_verts = self.store.find_vertices(limit=200)
            for v in all_verts:
                props_str = " ".join(str(val).lower() for val in v.get("properties", {}).values())
                cid = v.get("canonical_id", "")
                if any(t in props_str or t in cid.lower() for t in tokens):
                    seeds.append(cid)
                    if len(seeds) >= 5:
                        break

        # Expand deterministic graph from seeds
        queue: list[tuple[str, int]] = [(cid, 0) for cid in seeds]
        visited_cids: set[str] = set()

        while queue:
            cid, depth = queue.pop(0)
            if cid in visited_cids:
                continue
            visited_cids.add(cid)

            vertex = self.store.get_vertex_by_canonical_id(cid)
            if not vertex:
                continue
            det_nodes[cid] = vertex

            if depth < max_depth:
                out_edges = self.store.edges_from(vertex["vid"], limit=50)
                for edge in out_edges:
                    det_edges.append(edge)
                    tgt = edge.get("in_cid")
                    if tgt and tgt not in visited_cids:
                        queue.append((tgt, depth + 1))

                in_edges = self.store.edges_to(vertex["vid"], limit=50)
                for edge in in_edges:
                    det_edges.append(edge)
                    src = edge.get("out_cid")
                    if src and src not in visited_cids:
                        queue.append((src, depth + 1))

        t_det = (time.perf_counter() - t0) * 1000.0
        kernels.append(
            KernelResult(
                paradigm="DETERMINISTIC",
                execution_time_ms=round(t_det, 2),
                nodes_found=len(det_nodes),
                edges_found=len(det_edges),
                data={"seed_count": len(seeds)},
            )
        )

        # ---------------------------------------------------------
        # 2. Probabilistic Kernel: Cosine similarity over property terms
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        query_terms = re.findall(r"\w+", query.lower())
        query_vec: dict[str, float] = {}
        for q in query_terms:
            query_vec[q] = query_vec.get(q, 0.0) + 1.0

        q_norm = math.sqrt(sum(v * v for v in query_vec.values())) or 1.0

        prob_matches: list[dict[str, Any]] = []
        for cid, node in det_nodes.items():
            props = node.get("properties", {})
            doc_text = " ".join(f"{k} {v}" for k, v in props.items()).lower()
            doc_terms = re.findall(r"\w+", doc_text)
            doc_vec: dict[str, float] = {}
            for d in doc_terms:
                doc_vec[d] = doc_vec.get(d, 0.0) + 1.0
            d_norm = math.sqrt(sum(v * v for v in doc_vec.values())) or 1.0

            # Cosine dot product
            dot = sum(query_vec.get(term, 0.0) * doc_vec.get(term, 0.0) for term in query_vec)
            cosine = dot / (q_norm * d_norm) if (q_norm * d_norm) > 0 else 0.0

            if cosine > 0.0 or cid in seeds:
                prob_matches.append(
                    {
                        "canonical_id": cid,
                        "label": node.get("label"),
                        "similarity_score": round(max(0.05, cosine), 4),
                        "matched_terms": [t for t in query_terms if t in doc_vec],
                    }
                )

        prob_matches.sort(key=lambda m: m["similarity_score"], reverse=True)
        t_prob = (time.perf_counter() - t0) * 1000.0
        kernels.append(
            KernelResult(
                paradigm="PROBABILISTIC",
                execution_time_ms=round(t_prob, 2),
                nodes_found=len(prob_matches),
                edges_found=0,
                data={"top_similarity": prob_matches[0]["similarity_score"] if prob_matches else 0.0},
            )
        )

        # ---------------------------------------------------------
        # 3. Heuristic Kernel: Weighted A* / Dijkstra path exploration
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        heuristic_paths: list[dict[str, Any]] = []
        relationship_weights: dict[str, float] = {
            "DEPENDS_ON": 1.0,
            "CALLS": 1.2,
            "RUNS_ON": 1.1,
            "HOSTED_ON": 1.1,
            "COMMUNICATES_WITH": 1.5,
            "IMPACTS": 1.0,
            "CONTAINS": 1.8,
            "OWNS": 2.0,
            "RELATED_TO": 2.5,
        }

        # Build adjacency graph from deterministic edges
        adj: dict[str, list[tuple[str, str, float]]] = {}
        for e in det_edges:
            src, tgt, lbl = e.get("out_cid"), e.get("in_cid"), e.get("label", "RELATED_TO")
            if src and tgt:
                w = relationship_weights.get(lbl.upper(), 2.0)
                adj.setdefault(src, []).append((tgt, lbl, w))
                adj.setdefault(tgt, []).append((src, lbl, w))  # Undirected traversal for discovery

        if len(seeds) >= 2:
            src_cid, dst_cid = seeds[0], seeds[1]
            dist: dict[str, float] = {src_cid: 0.0}
            prev: dict[str, tuple[str, str]] = {}
            heap = [(0.0, src_cid)]

            while heap:
                d, curr = heapq.heappop(heap)
                if curr == dst_cid:
                    break
                if d > dist.get(curr, float("inf")):
                    continue
                for neighbor, lbl, weight in adj.get(curr, []):
                    new_dist = d + weight
                    if new_dist < dist.get(neighbor, float("inf")):
                        dist[neighbor] = new_dist
                        prev[neighbor] = (curr, lbl)
                        heapq.heappush(heap, (new_dist, neighbor))

            if dst_cid in dist:
                path_nodes: list[str] = []
                path_edges: list[str] = []
                curr = dst_cid
                while curr in prev:
                    p_node, p_lbl = prev[curr]
                    path_nodes.insert(0, curr)
                    path_edges.insert(0, p_lbl)
                    curr = p_node
                path_nodes.insert(0, src_cid)
                heuristic_paths.append(
                    {
                        "from": src_cid,
                        "to": dst_cid,
                        "total_cost": round(dist[dst_cid], 2),
                        "hop_count": len(path_edges),
                        "nodes": path_nodes,
                        "relationships": path_edges,
                    }
                )
        elif seeds and len(det_nodes) > 1:
            # Find closest 3 nodes from first seed
            src_cid = seeds[0]
            dist = {src_cid: 0.0}
            heap = [(0.0, src_cid)]
            while heap:
                d, curr = heapq.heappop(heap)
                if d > dist.get(curr, float("inf")):
                    continue
                for neighbor, lbl, weight in adj.get(curr, []):
                    new_dist = d + weight
                    if new_dist < dist.get(neighbor, float("inf")):
                        dist[neighbor] = new_dist
                        heapq.heappush(heap, (new_dist, neighbor))
            for target_cid, cost in sorted(dist.items(), key=lambda x: x[1])[1:4]:
                heuristic_paths.append(
                    {
                        "from": src_cid,
                        "to": target_cid,
                        "total_cost": round(cost, 2),
                        "hop_count": 1 if cost <= 2.5 else 2,
                        "nodes": [src_cid, target_cid],
                        "relationships": ["TRAVERSED"],
                    }
                )

        t_heur = (time.perf_counter() - t0) * 1000.0
        kernels.append(
            KernelResult(
                paradigm="HEURISTIC",
                execution_time_ms=round(t_heur, 2),
                nodes_found=len(heuristic_paths),
                edges_found=sum(p["hop_count"] for p in heuristic_paths),
                data={"paths_discovered": len(heuristic_paths)},
            )
        )

        # ---------------------------------------------------------
        # 4. Stochastic Kernel: Monte Carlo Path Reliability Sampling
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        stochastic_metrics: dict[str, Any] = {}
        if adj and seeds:
            start_node = seeds[0]
            reach_counts: dict[str, int] = {}
            for _ in range(monte_carlo_samples):
                curr = start_node
                steps = 0
                while steps < 4:
                    neighbors = adj.get(curr, [])
                    if not neighbors:
                        break
                    # Probabilistic walk weighted inversely by edge cost
                    weights = [1.0 / max(0.1, n[2]) for n in neighbors]
                    total_w = sum(weights)
                    probs = [w / total_w for w in weights]
                    r = random.random()
                    cumulative = 0.0
                    chosen = neighbors[-1][0]
                    for idx, p in enumerate(probs):
                        cumulative += p
                        if r <= cumulative:
                            chosen = neighbors[idx][0]
                            break
                    curr = chosen
                    reach_counts[curr] = reach_counts.get(curr, 0) + 1
                    steps += 1

            stochastic_metrics = {
                "monte_carlo_trials": monte_carlo_samples,
                "node_reachability_frequencies": {
                    k: round(v / (monte_carlo_samples * 4), 4)
                    for k, v in sorted(reach_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                },
                "network_entropy": round(
                    -sum((v / sum(reach_counts.values())) * math.log(v / sum(reach_counts.values())) for v in reach_counts.values())
                    if reach_counts
                    else 0.0,
                    3,
                ),
            }

        t_stoch = (time.perf_counter() - t0) * 1000.0
        kernels.append(
            KernelResult(
                paradigm="STOCHASTIC",
                execution_time_ms=round(t_stoch, 2),
                nodes_found=len(stochastic_metrics.get("node_reachability_frequencies", {})),
                edges_found=0,
                data=stochastic_metrics,
            )
        )

        # ---------------------------------------------------------
        # 5. Non-Deterministic Kernel: Sovereign Cognitive Narrator
        # ---------------------------------------------------------
        t0 = time.perf_counter()
        narration = self.narrator.synthesize_narrative_answer(
            question=query,
            target_canonical_ids=seeds,
        )
        t_non_det = (time.perf_counter() - t0) * 1000.0
        kernels.append(
            KernelResult(
                paradigm="NON_DETERMINISTIC",
                execution_time_ms=round(t_non_det, 2),
                nodes_found=len(narration.get("deterministic_evidence", {}).get("vertices", [])),
                edges_found=len(narration.get("deterministic_evidence", {}).get("edges", [])),
                data={"approaches_used": list(narration.get("multi_approach_narration", {}).keys())},
            )
        )

        top_probabilistic_matches = prob_matches[:10]

        return MultiParadigmResponse(
            query=query,
            target_canonical_ids=seeds,
            deterministic_subgraph={
                "nodes": [
                    {"id": v["canonical_id"], "label": v["label"], "properties": v["properties"]}
                    for v in det_nodes.values()
                ],
                "edges": det_edges,
                "total_nodes": len(det_nodes),
                "total_edges": len(det_edges),
            },
            probabilistic_matches=top_probabilistic_matches,
            heuristic_paths=heuristic_paths,
            stochastic_metrics=stochastic_metrics,
            cognitive_narration=narration,
            kernel_breakdown=[
                {
                    "paradigm": k.paradigm,
                    "latency_ms": k.execution_time_ms,
                    "nodes_found": k.nodes_found,
                    "edges_found": k.edges_found,
                    "metrics": k.data,
                }
                for k in kernels
            ],
        )
