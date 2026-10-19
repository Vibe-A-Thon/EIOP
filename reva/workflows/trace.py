"""Feature and impact trace analysis across graph vertices (T-701 / FT-001..006)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from reva.core.ids import trace_id as compute_trace_id
from reva.graph.port import GraphPort
from reva.kernel.coverage import Coverage, compose_coverage


@dataclass
class TraceHop:
    from_entity: str
    edge_label: str
    to_entity: str
    direction: str  # outgoing | incoming


@dataclass
class TraceResult:
    trace_id: str
    origin_entity: str
    direction: str
    max_depth: int
    visited_entities: List[str]
    hops: List[TraceHop]
    coverage: Coverage
    impacted_services: List[str] = field(default_factory=list)
    impacted_boundaries: List[str] = field(default_factory=list)
    recommended_test_ids: List[str] = field(default_factory=list)


def execute_feature_trace(
    graph: GraphPort,
    tenant_id: str,
    start_entity_id: str,
    direction: str = "outgoing",
    max_depth: int = 5,
) -> TraceResult:
    """Perform breadth-first graph traversal from starting entity within depth limit."""
    visited: Set[str] = {start_entity_id}
    queue: List[tuple[str, int]] = [(start_entity_id, 0)]
    hops: List[TraceHop] = []
    impacted_services: Set[str] = set()
    impacted_boundaries: Set[str] = set()

    while queue:
        curr, depth = queue.pop(0)
        if depth >= max_depth:
            continue

        page = graph.neighbours(
            tenant_id=tenant_id,
            ids=[curr],
            labels=None,
            direction=direction,
            valid_at=None,
            limit=50,
        )

        for edge in page.edges:
            target = edge.target_id if direction == "outgoing" else edge.source_id
            hops.append(
                TraceHop(
                    from_entity=edge.source_id,
                    edge_label=edge.label,
                    to_entity=edge.target_id,
                    direction=direction,
                )
            )
            if target not in visited:
                visited.add(target)
                queue.append((target, depth + 1))
                if "Service" in target or target.startswith("svc:"):
                    impacted_services.add(target)
                elif "Boundary" in target or target.startswith("bnd:"):
                    impacted_boundaries.add(target)

    coverage = Coverage(
        status="complete" if len(visited) < 1000 else "partial",
        scope=f"entity:{start_entity_id} depth:{max_depth}",
        examined_count=len(visited),
    )

    t_id = compute_trace_id({
        "direction": direction,
        "max_depth": max_depth,
        "origin_entity": start_entity_id,
        "tenant_id": tenant_id,
        "visited": sorted(list(visited)),
    })

    return TraceResult(
        trace_id=t_id,
        origin_entity=start_entity_id,
        direction=direction,
        max_depth=max_depth,
        visited_entities=sorted(list(visited)),
        hops=hops,
        coverage=coverage,
        impacted_services=sorted(list(impacted_services)),
        impacted_boundaries=sorted(list(impacted_boundaries)),
    )
