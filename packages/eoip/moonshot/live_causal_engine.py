"""Live Causal Graph Neural Simulator & Counterfactual Blast-Radius Engine.

Bridges the physical CausalGraphSimulator with the live GraphStore:
- Extracts live subgraphs, causal dependencies, and operational couplings.
- Computes degree-based and attribute-based node criticalities.
- Simulates cascading shocks on actual enterprise entities.
- Calculates topological blast-radius, critical tipping-point nodes, and counterfactual interventions.
"""

from __future__ import annotations

from typing import Any

from eoip.graph.store import GraphStore
from eoip.moonshot.causal_simulator import CascadeResult, CausalGraphSimulator


class LiveCausalGraphEngine:
    """Executes causal propagation and counterfactual blast-radius analysis over live graph entities."""

    def __init__(self, store: GraphStore) -> None:
        self.store = store

    def build_causal_subgraph(
        self,
        seed_canonical_ids: list[str],
        max_depth: int = 3,
        max_nodes: int = 150,
    ) -> CausalGraphSimulator:
        """Extracts an interconnected causal dependency subgraph from the live GraphStore."""
        simulator = CausalGraphSimulator()
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(cid, 0) for cid in seed_canonical_ids]

        # Criticality mapping based on entity attributes
        criticality_weights: dict[str, float] = {
            "CRITICAL": 3.0,
            "HIGH": 2.0,
            "MEDIUM": 1.2,
            "LOW": 0.8,
        }

        # Coupling strength based on relationship types
        relationship_couplings: dict[str, float] = {
            "DEPENDS_ON": 0.95,
            "CALLS": 0.85,
            "RUNS_ON": 0.90,
            "HOSTED_ON": 0.90,
            "COMMUNICATES_WITH": 0.75,
            "IMPACTS": 0.90,
            "CONTAINS": 0.80,
            "OWNS": 0.60,
            "AFFECTS": 0.85,
        }

        # Step 1: Collect nodes and outgoing/incoming edges up to max_depth
        while queue and len(visited) < max_nodes:
            current_id, depth = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            vertex = self.store.get_vertex_by_canonical_id(current_id)
            if not vertex:
                continue

            v_props = vertex.get("properties", {})
            v_type = vertex.get("label", "Unknown")
            raw_crit = str(v_props.get("criticality", v_props.get("priority", "MEDIUM"))).upper()
            crit_val = criticality_weights.get(raw_crit, 1.0)
            resilience_val = float(v_props.get("resilience", 0.6))
            resilience_val = max(0.05, min(0.95, resilience_val))

            simulator.add_node(
                node_id=current_id,
                node_type=v_type,
                resilience=resilience_val,
                criticality=crit_val,
            )

            if depth < max_depth:
                # Outgoing edges
                outgoing = self.store.edges_from(vertex["vid"], limit=100)
                for edge in outgoing:
                    target_cid = edge.get("in_cid")
                    if target_cid and target_cid not in visited:
                        queue.append((target_cid, depth + 1))

                # Incoming edges
                incoming = self.store.edges_to(vertex["vid"], limit=100)
                for edge in incoming:
                    source_cid = edge.get("out_cid")
                    if source_cid and source_cid not in visited:
                        queue.append((source_cid, depth + 1))

        # Step 2: Populate causal edges between all discovered visited nodes
        for node_id in visited:
            vertex = self.store.get_vertex_by_canonical_id(node_id)
            if not vertex:
                continue
            outgoing = self.store.edges_from(vertex["vid"], limit=100)
            for edge in outgoing:
                target_cid = edge.get("in_cid")
                if target_cid and target_cid in simulator.nodes:
                    edge_type = edge.get("label", "DEPENDS_ON").upper()
                    coupling = relationship_couplings.get(edge_type, 0.70)
                    try:
                        simulator.add_edge(from_node=node_id, to_node=target_cid, coupling_strength=coupling)
                    except KeyError:
                        pass

        return simulator

    def compute_blast_radius(
        self,
        shock_entities: dict[str, float],
        max_depth: int = 3,
        failure_threshold: float = 0.5,
        dampening_factor: float = 0.85,
    ) -> dict[str, Any]:
        """Calculates live topological blast radius and cascading failure timeline."""
        seed_ids = list(shock_entities.keys())
        simulator = self.build_causal_subgraph(seed_ids, max_depth=max_depth)

        if not simulator.nodes:
            return {
                "shock_entities": shock_entities,
                "total_nodes_evaluated": 0,
                "collapsed_nodes": [],
                "systemic_loss_score": 0.0,
                "tipping_point_node": None,
                "blast_radius_depth": 0,
                "impact_breakdown": {},
            }

        result: CascadeResult = simulator.simulate_cascade(
            shock_nodes=shock_entities,
            max_steps=10,
            dampening_factor=dampening_factor,
            failure_threshold=failure_threshold,
        )

        impact_breakdown: dict[str, dict[str, Any]] = {}
        for nid, prob in result.final_failure_probabilities.items():
            if prob > 0.05:
                node = simulator.nodes.get(nid)
                impact_breakdown[nid] = {
                    "failure_probability": round(prob, 4),
                    "node_type": node.node_type if node else "Unknown",
                    "criticality": node.criticality if node else 1.0,
                    "status": "COLLAPSED" if prob >= failure_threshold else "DEGRADED",
                }

        return {
            "shock_entities": shock_entities,
            "total_nodes_evaluated": len(simulator.nodes),
            "total_edges_evaluated": len(simulator.edges),
            "total_steps": result.total_steps,
            "collapsed_nodes": result.collapsed_nodes,
            "systemic_loss_score": result.systemic_loss_score,
            "tipping_point_node": result.tipping_point_node,
            "blast_radius_depth": len(result.timeline),
            "impact_breakdown": impact_breakdown,
        }

    def evaluate_counterfactual(
        self,
        shock_entities: dict[str, float],
        interventions: dict[str, float],  # entity_cid -> new resilience
        max_depth: int = 3,
    ) -> dict[str, Any]:
        """Evaluates what-if resilience interventions on live graph topology."""
        seed_ids = list(set(shock_entities.keys()) | set(interventions.keys()))
        simulator = self.build_causal_subgraph(seed_ids, max_depth=max_depth)

        if not simulator.nodes:
            return {
                "error": "No nodes found in subgraph for specified entities",
                "baseline_loss": 0.0,
                "mitigated_loss": 0.0,
                "loss_reduction": 0.0,
            }

        probe_result = simulator.counterfactual_probe(shock_entities, interventions)
        probe_result["shock_entities"] = shock_entities
        probe_result["interventions_applied"] = interventions
        return probe_result
