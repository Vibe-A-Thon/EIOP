"""Execution Plan Compiler and DAG Validator (PUR-APU-001, PUR-RUN-006).

Validates operator DAGs, performs deterministic topological sorting,
detects cycles, and calculates aggregate memory and deadline budgets.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple
from uuid import uuid4

from eoip.processing.catalog import get_operator_spec
from eoip.processing.contracts import ExecutionPlan, PlanNode


def compile_execution_plan(nodes: List[PlanNode]) -> ExecutionPlan:
    """Compile and validate an execution plan DAG."""
    if not nodes:
        raise ValueError("Execution plan cannot be empty")
    if len(nodes) > 32:
        raise ValueError(f"Plan exceeds maximum limit of 32 nodes, got {len(nodes)}")

    node_map: Dict[str, PlanNode] = {n.node_id: n for n in nodes}
    if len(node_map) != len(nodes):
        raise ValueError("Plan contains duplicate node IDs")

    # Validate operator IDs against catalog
    for n in nodes:
        spec = get_operator_spec(n.operator_id)
        if not spec:
            raise ValueError(f"Unregistered operator '{n.operator_id}' in node '{n.node_id}'")

    # Build dependency graph
    in_degree: Dict[str, int] = {n.node_id: 0 for n in nodes}
    adj: Dict[str, List[str]] = defaultdict(list)
    edge_count = 0

    for n in nodes:
        for port, src in n.inputs.items():
            if src in node_map:
                adj[src].append(n.node_id)
                in_degree[n.node_id] += 1
                edge_count += 1

    if edge_count > 64:
        raise ValueError(f"Plan exceeds maximum limit of 64 edges, got {edge_count}")

    # Kahn's algorithm with deterministic tie-breaking (sorted by node_id)
    queue = deque(sorted([nid for nid, deg in in_degree.items() if deg == 0]))
    topological_order: List[str] = []

    while queue:
        curr = queue.popleft()
        topological_order.append(curr)

        # Process successors in sorted order for determinism
        for neighbor in sorted(adj[curr]):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topological_order) != len(nodes):
        cycle_nodes = set(node_map.keys()) - set(topological_order)
        raise ValueError(f"Plan contains cyclic dependencies involving nodes: {sorted(cycle_nodes)}")

    # Aggregate budgets
    total_memory = max((n.budgets.memory_mib for n in nodes), default=512)
    total_duration = sum(n.budgets.deadline_seconds for n in nodes)

    plan = ExecutionPlan(
        plan_id=f"plan_{uuid4().hex[:12]}",
        nodes=nodes,
        topological_order=topological_order,
        estimated_memory_mib=total_memory,
        estimated_duration_seconds=total_duration,
        required_permissions=[],
        device_candidates=["cpu"],
    )
    plan.plan_digest = plan.compute_digest()
    return plan


compile_plan = compile_execution_plan

