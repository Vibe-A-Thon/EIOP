"""Graph-loop engineering facade.

This module connects the graph discipline router and the loop primitive catalog
into one stats/reporting surface for Graph-over-Loop and Loop-over-Graph use.
"""

from __future__ import annotations

import threading
from typing import Any

from eoip.graph.engineering import ENGINEERING_DISCIPLINES
from eoip.loops.drivers import LOOP_PHASES


class GraphLoopEngine:
    """Expose graph-loop readiness and catalog statistics."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._plans_generated = 0

    def plan(self, mode: str, seed_ids: list[str] | None = None) -> dict[str, Any]:
        if mode not in {"graph_over_loop", "loop_over_graph"}:
            raise ValueError("mode must be graph_over_loop or loop_over_graph")
        phases = LOOP_PHASES.get("ooda", [])
        with self._lock:
            self._plans_generated += 1
        return {
            "mode": mode,
            "seed_ids": seed_ids or [],
            "loop": "ooda",
            "phases": phases,
            "strategy": "graph-guided iteration" if mode == "graph_over_loop" else "iterative graph refinement",
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
