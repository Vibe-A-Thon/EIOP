"""Impact Simulator and Blast-Radius Engine with Strict Output Category Separation (CRA-028.3, CRA-028.4, CRA-028.8, CRA-028.9, CRA-028.A).

Features:
- Explicit category separation (CRA-028.3):
  * OBSERVED: Direct relationships in active graph.
  * DETERMINISTIC_IMPACT: Exact BFS/Dijkstra dependency blast radius.
  * HEURISTIC_PATHS: Heuristic scores and severity paths, explicitly labelled HEURISTIC.
  * STOCHASTIC_ESTIMATE: Calibrated Monte Carlo / statistical propagation with seed and confidence bounds (never random-walk confusion).
  * LEARNED_ESTIMATE: Proposed neural/learned propagation (CRA-028.9) with dual-path status, never replacing deterministic order.
  * DOMAIN_SIMULATION: Counterfactual twin simulation with versioned model, assumptions, seed, and production-assertion fence (CRA-028.A).
- Blast-radius breakdown: Impacted services, teams, and business processes with explicit severity labels (CRA-028.8).
- Execution cancellation for expensive/long-running simulations (CRA-028.A).
"""

from __future__ import annotations

from collections import deque
import copy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
import json
import math
import random
from typing import Any, Callable, Optional
from uuid import uuid4

from eoip.graph.store import GraphStore
from eoip.temporal.deterministic_graph import DeterministicGraphAlgorithms, PathResult


class ImpactCategory(str, Enum):
    OBSERVED = "OBSERVED"
    DETERMINISTIC_IMPACT = "DETERMINISTIC_IMPACT"
    HEURISTIC_PATHS = "HEURISTIC_PATHS"
    STOCHASTIC_ESTIMATE = "STOCHASTIC_ESTIMATE"
    LEARNED_ESTIMATE = "LEARNED_ESTIMATE"
    DOMAIN_SIMULATION = "DOMAIN_SIMULATION"


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ProductionAssertionBlockedError(PermissionError):
    """Raised when simulated facts attempt to enter production knowledge without human review (CRA-028.A)."""


@dataclass
class ImpactedEntity:
    canonical_id: str
    entity_type: str
    name: str
    depth: int
    severity: SeverityLevel
    is_heuristic_score: bool = True
    score_confidence: float = 0.5
    path: list[str] = field(default_factory=list)


@dataclass
class DualPathImpactReport:
    """Combines deterministic blast radius and learned estimate (CRA-028.9, CRA-028.A)."""
    change_target: str
    deterministic_impacted_services: list[ImpactedEntity]
    deterministic_impacted_teams: list[str]
    deterministic_impacted_processes: list[str]
    learned_estimates: list[dict[str, Any]]
    agreement_status: str  # CORROBORATED, DISPUTED, UNCORROBORATED
    total_deterministic_count: int = 0
    total_learned_count: int = 0


@dataclass
class SimulationProtocol:
    model_version: str
    assumptions: list[str]
    input_parameters: dict[str, Any]
    seed: int
    uncertainty_distribution: str = "gaussian"
    trials: int = 100


@dataclass
class SimulationResult:
    simulation_id: str
    protocol: SimulationProtocol
    output_category: ImpactCategory
    mean_impact_count: float
    confidence_interval_95: tuple[float, float]
    impacted_nodes: list[str]
    executed_trials: int
    cancelled: bool = False
    is_asserted_production_fact: bool = False  # NEVER True without explicit human review fence


class ImpactSimulator:
    """Computes deterministic and dual-path blast radius and governed simulations (CRA-028.3, 028.4, 028.8, 028.9)."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._algorithms = DeterministicGraphAlgorithms(store)

    def compute_blast_radius(
        self,
        target_canonical_id: str,
        max_depth: int = 5,
        learned_propagator: Optional[Callable[[str, int], list[dict[str, Any]]]] = None,
    ) -> DualPathImpactReport:
        """Compute blast radius with explicit separation between deterministic impact and learned estimates (CRA-028.8, CRA-028.9, CRA-028.A)."""
        # 1. Deterministic BFS / reachability
        reachable_cids = self._algorithms.bfs_reachable(target_canonical_id, max_depth=max_depth)

        impacted_services: list[ImpactedEntity] = []
        impacted_teams: set[str] = set()
        impacted_processes: set[str] = set()

        for cid in reachable_cids:
            vertex = self._store.get_vertex_by_canonical_id(cid)
            if not vertex:
                continue
            v_props = vertex.get("properties", {})
            v_label = vertex.get("label", "Entity")

            # Dijkstra shortest path to get exact distance and hop evidence
            path_res = self._algorithms.dijkstra_shortest_path(target_canonical_id, cid)
            depth = path_res.hop_count if path_res else 1
            hops = path_res.hops if path_res else [target_canonical_id, cid]

            # Severity calculation (labelled HEURISTIC unless formal domain model exists - CRA-028.8)
            severity = SeverityLevel.LOW
            if depth == 1:
                severity = SeverityLevel.CRITICAL
            elif depth == 2:
                severity = SeverityLevel.HIGH
            elif depth <= 4:
                severity = SeverityLevel.MEDIUM

            name = v_props.get("name") or v_props.get("display_name") or cid
            entity = ImpactedEntity(
                canonical_id=cid,
                entity_type=v_label,
                name=name,
                depth=depth,
                severity=severity,
                is_heuristic_score=True,  # CRA-028.8: explicitly labelled heuristic
                score_confidence=max(0.2, 1.0 - (depth * 0.15)),
                path=hops,
            )

            if v_label in ("Service", "APIService", "Database", "Repository"):
                impacted_services.append(entity)
            if v_label in ("Person", "Organization") or "owner" in v_props or "team" in v_props:
                team_name = v_props.get("owner") or v_props.get("team") or name
                impacted_teams.add(team_name)
            if v_label in ("ProcessFlow", "ProcessStep", "WorkItem", "BusinessObjective", "BusinessCapability"):
                impacted_processes.add(name)

        # 2. Learned impact propagation (CRA-028.9)
        learned_candidates = []
        if learned_propagator:
            raw_learned = learned_propagator(target_canonical_id, max_depth)
            for item in raw_learned:
                cid = item.get("canonical_id")
                # Labelled as PROPOSED and UNCORROBORATED if not present in deterministic set (CRA-028.A)
                is_corroborated = cid in reachable_cids
                status = "CORROBORATED" if is_corroborated else "UNCORROBORATED"
                learned_candidates.append({
                    "canonical_id": cid,
                    "score": item.get("score", 0.5),
                    "knowledge_state": "PROPOSED",
                    "dual_path_status": status,
                    "producer_class": "PROBABILISTIC",
                })

        # Dual-path agreement status
        deterministic_set = set(reachable_cids)
        learned_set = {item["canonical_id"] for item in learned_candidates}

        if not learned_candidates:
            agreement = "DETERMINISTIC_ONLY"
        elif deterministic_set == learned_set:
            agreement = "CORROBORATED"
        elif deterministic_set.issubset(learned_set):
            agreement = "UNCORROBORATED_EXTENSIONS"
        else:
            agreement = "DISPUTED"

        return DualPathImpactReport(
            change_target=target_canonical_id,
            deterministic_impacted_services=impacted_services,
            deterministic_impacted_teams=sorted(impacted_teams),
            deterministic_impacted_processes=sorted(impacted_processes),
            learned_estimates=learned_candidates,
            agreement_status=agreement,
            total_deterministic_count=len(reachable_cids),
            total_learned_count=len(learned_candidates),
        )

    def run_stochastic_simulation(
        self,
        start_id: str,
        protocol: SimulationProtocol,
        cancellation_check: Optional[Callable[[], bool]] = None,
    ) -> SimulationResult:
        """Run a calibrated Monte Carlo simulation with repeatable seed and uncertainty protocol (CRA-028.4, CRA-028.A)."""
        rng = random.Random(protocol.seed)
        trial_counts: list[int] = []
        collected_impacted: set[str] = set()

        adj, _ = self._algorithms._build_adj_list()

        for t in range(protocol.trials):
            if cancellation_check and cancellation_check():
                # Expensive simulation cancelled gracefully (CRA-028.A)
                return SimulationResult(
                    simulation_id=f"sim-cancelled-{uuid4().hex[:8]}",
                    protocol=protocol,
                    output_category=ImpactCategory.STOCHASTIC_ESTIMATE,
                    mean_impact_count=float(sum(trial_counts) / len(trial_counts)) if trial_counts else 0.0,
                    confidence_interval_95=(0.0, 0.0),
                    impacted_nodes=sorted(collected_impacted),
                    executed_trials=t,
                    cancelled=True,
                    is_asserted_production_fact=False,
                )

            # Failure cascade trial
            visited: set[str] = {start_id}
            queue = deque([start_id])

            while queue:
                curr = queue.popleft()
                for edge in adj.get(curr, []):
                    nbr = edge["target"]
                    weight = edge.get("weight", 0.5)
                    # Use calibrated failure distribution with parameter noise
                    prob = min(0.95, max(0.05, weight + rng.gauss(0, 0.05)))
                    if nbr not in visited and rng.random() < prob:
                        visited.add(nbr)
                        collected_impacted.add(nbr)
                        queue.append(nbr)

            trial_counts.append(len(visited) - 1)

        mean_val = float(sum(trial_counts) / len(trial_counts))
        variance = sum((x - mean_val) ** 2 for x in trial_counts) / max(1, len(trial_counts) - 1)
        std_err = math.sqrt(variance) / math.sqrt(len(trial_counts))
        ci_95 = (round(mean_val - 1.96 * std_err, 2), round(mean_val + 1.96 * std_err, 2))

        return SimulationResult(
            simulation_id=f"sim-res-{uuid4().hex[:8]}",
            protocol=protocol,
            output_category=ImpactCategory.STOCHASTIC_ESTIMATE,
            mean_impact_count=round(mean_val, 2),
            confidence_interval_95=ci_95,
            impacted_nodes=sorted(collected_impacted),
            executed_trials=protocol.trials,
            cancelled=False,
            is_asserted_production_fact=False,  # Never enters production without review (CRA-028.A)
        )

    def assert_simulation_fact_to_production(
        self,
        simulation_result: SimulationResult,
        fact: dict[str, Any],
        human_approver: Optional[str] = None,
    ) -> None:
        """Production Assertion Fence (CRA-028.A).

        Ensures simulated facts cannot enter asserted production knowledge without explicit human review.
        """
        if not human_approver:
            raise ProductionAssertionBlockedError(
                f"Simulated fact for simulation '{simulation_result.simulation_id}' cannot enter "
                "asserted production knowledge without human review (CRA-028.A)"
            )
        # With human approver, fact can be recorded as human-reviewed assertion
        simulation_result.is_asserted_production_fact = True
