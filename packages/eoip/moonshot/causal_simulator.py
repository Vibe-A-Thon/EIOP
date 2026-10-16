"""Moonshot 3: Causal Graph Neural Simulator & Counterfactual Blast-Radius Engine.

Provides deep graph neural message-passing simulation of systemic cascading failures,
tipping points, resilience modeling, and counterfactual what-if intervention probes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CausalNode:
    node_id: str
    node_type: str
    resilience: float = 1.0  # 0.0 (fragile) to 1.0 (hardened)
    failure_probability: float = 0.0
    criticality: float = 1.0


@dataclass
class CausalEdge:
    from_node: str
    to_node: str
    coupling_strength: float = 0.8  # transmission factor 0.0 - 1.0
    propagation_delay_ms: float = 10.0


@dataclass
class CascadeStep:
    step: int
    newly_impacted_nodes: list[str]
    cumulative_failures: dict[str, float]
    step_loss: float


@dataclass
class CascadeResult:
    initial_shock: dict[str, float]
    total_steps: int
    final_failure_probabilities: dict[str, float]
    collapsed_nodes: list[str]
    systemic_loss_score: float
    tipping_point_node: str | None
    timeline: list[CascadeStep]


class CausalGraphSimulator:
    """Physics-style message passing simulation engine for systemic failure propagation."""

    def __init__(self) -> None:
        self.nodes: dict[str, CausalNode] = {}
        self.edges: list[CausalEdge] = []
        # Adjacency: from_node -> list of CausalEdge
        self._adj_out: dict[str, list[CausalEdge]] = {}

    def add_node(self, node_id: str, node_type: str, resilience: float = 1.0, criticality: float = 1.0) -> None:
        self.nodes[node_id] = CausalNode(
            node_id=node_id,
            node_type=node_type,
            resilience=max(0.01, min(1.0, resilience)),
            criticality=criticality,
        )
        if node_id not in self._adj_out:
            self._adj_out[node_id] = []

    def add_edge(self, from_node: str, to_node: str, coupling_strength: float = 0.8, delay_ms: float = 10.0) -> None:
        if from_node not in self.nodes or to_node not in self.nodes:
            raise KeyError("Both from_node and to_node must exist before adding an edge")
        edge = CausalEdge(from_node=from_node, to_node=to_node, coupling_strength=coupling_strength, propagation_delay_ms=delay_ms)
        self.edges.append(edge)
        self._adj_out[from_node].append(edge)

    def simulate_cascade(
        self,
        shock_nodes: dict[str, float],  # node_id -> initial shock magnitude (0.0 to 1.0)
        max_steps: int = 10,
        dampening_factor: float = 0.85,
        failure_threshold: float = 0.5,
    ) -> CascadeResult:
        """Run message-passing simulation to propagate failure shocks through graph dependencies."""
        current_probs: dict[str, float] = {nid: 0.0 for nid in self.nodes}
        for nid, shock in shock_nodes.items():
            if nid in current_probs:
                current_probs[nid] = min(1.0, shock)

        timeline: list[CascadeStep] = []
        collapsed_set: set[str] = {nid for nid, p in current_probs.items() if p >= failure_threshold}
        tipping_point: str | None = None
        max_single_step_spread = 0

        for step in range(1, max_steps + 1):
            next_probs = dict(current_probs)
            newly_impacted: list[str] = []

            # GNN-style message passing: each node aggregates shock from its predecessors
            incoming_messages: dict[str, float] = {nid: 0.0 for nid in self.nodes}

            for from_nid, edges in self._adj_out.items():
                p_from = current_probs[from_nid]
                if p_from <= 0.05:
                    continue
                for edge in edges:
                    to_nid = edge.to_node
                    # Transmitted shock modulated by coupling and target resilience
                    to_resilience = self.nodes[to_nid].resilience
                    transmitted = p_from * edge.coupling_strength * (1.0 - to_resilience * 0.7) * dampening_factor
                    incoming_messages[to_nid] = max(incoming_messages[to_nid], transmitted)

            # Update probabilities
            for nid, msg in incoming_messages.items():
                if msg > 0:
                    combined = 1.0 - (1.0 - next_probs[nid]) * (1.0 - msg)
                    if combined > next_probs[nid] + 0.01:
                        next_probs[nid] = min(1.0, combined)
                        if next_probs[nid] >= failure_threshold and nid not in collapsed_set:
                            collapsed_set.add(nid)
                            newly_impacted.append(nid)

            # Step loss calculation weighted by node criticality
            step_loss = sum(next_probs[nid] * self.nodes[nid].criticality for nid in self.nodes)

            timeline.append(
                CascadeStep(
                    step=step,
                    newly_impacted_nodes=newly_impacted,
                    cumulative_failures=dict(next_probs),
                    step_loss=step_loss,
                )
            )

            if len(newly_impacted) > max_single_step_spread:
                max_single_step_spread = len(newly_impacted)
                tipping_point = newly_impacted[0] if newly_impacted else None

            current_probs = next_probs
            if not newly_impacted and step > 1:
                break  # System reached equilibrium

        final_loss = sum(current_probs[nid] * self.nodes[nid].criticality for nid in self.nodes)

        return CascadeResult(
            initial_shock=shock_nodes,
            total_steps=len(timeline),
            final_failure_probabilities=current_probs,
            collapsed_nodes=sorted(list(collapsed_set)),
            systemic_loss_score=round(final_loss, 3),
            tipping_point_node=tipping_point,
            timeline=timeline,
        )

    def counterfactual_probe(
        self,
        baseline_shock: dict[str, float],
        interventions: dict[str, float],  # node_id -> new resilience
    ) -> dict[str, Any]:
        """Compare baseline cascading failure against hypothetical resilience interventions."""
        baseline_res = self.simulate_cascade(baseline_shock)

        # Apply intervention
        original_resiliences = {nid: self.nodes[nid].resilience for nid in interventions if nid in self.nodes}
        for nid, new_res in interventions.items():
            if nid in self.nodes:
                self.nodes[nid].resilience = new_res

        try:
            mitigated_res = self.simulate_cascade(baseline_shock)
        finally:
            # Restore original
            for nid, orig in original_resiliences.items():
                self.nodes[nid].resilience = orig

        loss_reduction = baseline_res.systemic_loss_score - mitigated_res.systemic_loss_score
        collapsed_reduction = len(baseline_res.collapsed_nodes) - len(mitigated_res.collapsed_nodes)

        return {
            "baseline_loss": baseline_res.systemic_loss_score,
            "mitigated_loss": mitigated_res.systemic_loss_score,
            "loss_reduction": round(loss_reduction, 3),
            "collapsed_nodes_avoided": collapsed_reduction,
            "baseline_collapsed": baseline_res.collapsed_nodes,
            "mitigated_collapsed": mitigated_res.collapsed_nodes,
            "effective_roi": round((loss_reduction / max(1.0, baseline_res.systemic_loss_score)) * 100, 2),
        }
