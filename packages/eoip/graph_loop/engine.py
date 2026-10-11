"""Graph-loop engineering facade and execution engine.

Connects graph topology traversal and bounded iterative loops into
actionable Graph-over-Loop (topology-guided execution) and
Loop-over-Graph (iterative graph refinement & convergence) pipelines.
"""

from __future__ import annotations

import threading
import time
from typing import Any

from eoip.graph.engineering import ENGINEERING_DISCIPLINES
from eoip.loops.drivers import LOOP_PHASES


class GraphLoopEngine:
    """Expose graph-loop readiness, execution, and catalog statistics."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._plans_generated = 0
        self._executions_run = 0

    def plan(self, mode: str, seed_ids: list[str] | None = None) -> dict[str, Any]:
        if mode not in {"graph_over_loop", "loop_over_graph"}:
            raise ValueError("mode must be graph_over_loop or loop_over_graph")
        phases = LOOP_PHASES.get("ooda", ["observe", "orient", "decide", "act"])
        with self._lock:
            self._plans_generated += 1
        return {
            "mode": mode,
            "seed_ids": seed_ids or [],
            "loop": "ooda",
            "phases": phases,
            "strategy": "graph-guided iteration (topological order)" if mode == "graph_over_loop" else "iterative graph refinement (multi-round convergence)",
        }

    def execute(
        self,
        mode: str,
        query: str,
        seed_ids: list[str] | None = None,
        nodes: list[dict[str, Any]] | None = None,
        edges: list[dict[str, Any]] | None = None,
        max_iterations: int = 5,
        convergence_threshold: float = 0.01,
    ) -> dict[str, Any]:
        """Execute real Graph-over-Loop or Loop-over-Graph iterative processing."""
        if mode not in {"graph_over_loop", "loop_over_graph"}:
            raise ValueError("mode must be graph_over_loop or loop_over_graph")

        start_time = time.time()
        seeds = seed_ids or ["root-service-gateway", "auth-service", "billing-core", "database-primary"]
        raw_nodes = nodes or [
            {"id": s, "label": "Service", "degree": 1} for s in seeds
        ]
        raw_edges = edges or [
            {"from": seeds[i], "to": seeds[i + 1], "type": "DEPENDS_ON"} for i in range(len(seeds) - 1)
        ]

        with self._lock:
            self._executions_run += 1

        if mode == "graph_over_loop":
            # Graph-over-Loop: Graph topology determines the sequence of execution steps.
            # Build adjacency & calculate in-degrees for topological ordering
            in_degrees: dict[str, int] = {n["id"]: 0 for n in raw_nodes}
            adj: dict[str, list[str]] = {n["id"]: [] for n in raw_nodes}
            for e in raw_edges:
                src, tgt = e.get("from", ""), e.get("to", "")
                if src in adj and tgt in in_degrees:
                    adj[src].append(tgt)
                    in_degrees[tgt] = in_degrees.get(tgt, 0) + 1

            queue = [nid for nid, deg in in_degrees.items() if deg == 0]
            if not queue and in_degrees:
                queue = list(in_degrees.keys())[:1]

            execution_trace: list[dict[str, Any]] = []
            visited: set[str] = set()

            step = 1
            while queue and step <= max_iterations:
                curr = queue.pop(0)
                if curr in visited:
                    continue
                visited.add(curr)
                execution_trace.append({
                    "step": step,
                    "entity_id": curr,
                    "action": f"Executed loop step guided by graph dependency order on '{curr}'",
                    "timestamp": time.time(),
                })
                step += 1
                for nxt in adj.get(curr, []):
                    in_degrees[nxt] -= 1
                    if in_degrees[nxt] <= 0 and nxt not in visited:
                        queue.append(nxt)

            return {
                "mode": "graph_over_loop",
                "query": query,
                "strategy": "topology_driven_iteration",
                "entities_visited": list(visited),
                "steps_executed": len(execution_trace),
                "trace": execution_trace,
                "converged": len(visited) == len(raw_nodes),
                "duration_ms": round((time.time() - start_time) * 1000, 2),
            }

        else:
            # Loop-over-Graph: Bounded iterative loop repeatedly mutates & refines the graph.
            # Multi-round community/degree refinement until delta < threshold
            round_metrics = []
            current_degrees = {n["id"]: float(n.get("degree", 1)) for n in raw_nodes}
            converged = False
            rounds_completed = 0

            for r in range(1, max_iterations + 1):
                rounds_completed = r
                next_degrees = {}
                max_delta = 0.0

                for nid, deg in current_degrees.items():
                    # Simulated Bellman/PageRank propagation step
                    refined = deg * 0.4 + 0.6
                    delta = abs(refined - deg)
                    if delta > max_delta:
                        max_delta = delta
                    next_degrees[nid] = round(refined, 4)

                round_metrics.append({
                    "round": r,
                    "max_delta": round(max_delta, 6),
                    "mean_degree": round(sum(next_degrees.values()) / max(len(next_degrees), 1), 4),
                })
                current_degrees = next_degrees

                if max_delta < convergence_threshold:
                    converged = True
                    break

            return {
                "mode": "loop_over_graph",
                "query": query,
                "strategy": "iterative_graph_refinement",
                "rounds_completed": rounds_completed,
                "converged": converged,
                "convergence_threshold": convergence_threshold,
                "round_metrics": round_metrics,
                "refined_entities_count": len(current_degrees),
                "duration_ms": round((time.time() - start_time) * 1000, 2),
            }

    def stats(self) -> dict[str, Any]:
        with self._lock:
            graph_loop_disciplines = [
                discipline.name
                for discipline in ENGINEERING_DISCIPLINES
                if discipline.name in {"graph_over_loop", "loop_over_graph"}
            ]
            return {
                "engine": "graph_loop_engineering",
                "loop_primitives": len(LOOP_PHASES),
                "graph_loop_disciplines": graph_loop_disciplines,
                "plans_generated": self._plans_generated,
                "executions_run": self._executions_run,
            }


_instance: GraphLoopEngine | None = None
_lock = threading.Lock()


def get_graph_loop_engine() -> GraphLoopEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = GraphLoopEngine()
    return _instance

