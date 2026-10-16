"""GraphAnalyticsAgent: runs graph algorithms as bounded agent workflows.

Supports all algorithms from the extended GraphAlgorithms module plus
the existing metrics/similarity/community engines. Can be triggered
individually or as part of a multi-agent swarm.
"""

from __future__ import annotations

from typing import Any

from eoip.contracts.agent import AgentRequest, AgentResult, ExplanationEnvelope
from eoip.graph.store import GraphStore


ALGORITHM_REGISTRY: dict[str, str] = {
    "ring_detection": "detect_rings",
    "intersection_detection": "detect_intersection",
    "weighted_shortest_path": "weighted_shortest_path",
    "single_source_weighted": "single_source_weighted_paths",
    "k_step_neighbors": "k_step_neighbors",
    "k_jump": "k_jump",
    "custom_path": "custom_path",
    "ray_detection": "ray_detection",
    "co_neighbors": "co_neighbors",
    "personal_rank": "personal_rank",
    "neighbor_rank": "neighbor_rank",
    "model_similarity": "model_similarity",
    "pagerank": "centrality_pagerank",
    "betweenness": "centrality_betweenness",
    "closeness": "centrality_closeness",
    "eigenvector": "centrality_eigenvector",
    "katz": "centrality_katz",
    "hits": "centrality_hits",
    "harmonic": "centrality_harmonic",
    "k_core": "k_core_decomposition",
    "community_detection": "community_detection",
    "all_shortest_paths": "all_shortest_paths",
    "k_shortest_paths": "k_shortest_paths",
    "jaccard_similarity": "jaccard_similarity",
    "adamic_adar": "adamic_adar",
    "common_neighbors": "common_neighbors_similarity",
    "link_prediction": "link_prediction",
    "blast_radius": "blast_radius",
    "anomaly_detection": "anomaly_detection",
}


class GraphAnalyticsAgent:
    agent_id = "GraphAnalytics"
    allowed_tools = frozenset({"search", "entity", "analytics"})
    max_steps = 15
    max_seconds = 60.0

    def __init__(self, config: dict | None = None) -> None:
        if config:
            budgets = config.get("budgets", {})
            self.max_steps = budgets.get("max_steps", self.max_steps)
            self.max_seconds = budgets.get("max_seconds", self.max_seconds)

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        algorithm = request.goal.strip().lower().replace(" ", "_").replace("-", "_")

        if algorithm == "all" or algorithm == "swarm":
            return self._run_swarm(request, store)

        if algorithm not in ALGORITHM_REGISTRY:
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Unknown algorithm: {algorithm}. Available: {sorted(ALGORITHM_REGISTRY.keys())}",
                evidence_refs=[],
            )

        method_name = ALGORITHM_REGISTRY[algorithm]
        params = self._extract_params(request)

        try:
            result_data = self._dispatch(store, method_name, params)
        except Exception as exc:
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Algorithm {algorithm} failed: {exc}",
                evidence_refs=[],
            )

        envelope = ExplanationEnvelope(
            decision_summary=f"Algorithm {algorithm} completed successfully",
            observed_facts=[f"Ran algorithm: {algorithm}"],
            inferred_findings=[f"Result type: {type(result_data).__name__}"],
            evidence_refs=[f"algorithm:{algorithm}"],
            confidence=1.0,
        )

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=f"Algorithm {algorithm} completed successfully",
            evidence_refs=[f"algorithm:{algorithm}"],
            explanation=envelope,
            data=self._serialize(result_data),
        )

    def _run_swarm(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        cid = request.context_refs[0] if request.context_refs else None
        results: dict[str, Any] = {}
        failed: list[str] = []

        swarm_algorithms = [
            "ring_detection", "k_core", "community_detection",
            "anomaly_detection", "blast_radius",
        ]
        if cid:
            swarm_algorithms.extend([
                "k_step_neighbors", "personal_rank", "neighbor_rank",
                "jaccard_similarity",
            ])

        params = self._extract_params(request)
        if cid:
            params.setdefault("canonical_id", cid)
            params.setdefault("source_id", cid)
            params.setdefault("start_id", cid)

        for algo in swarm_algorithms:
            method_name = ALGORITHM_REGISTRY.get(algo)
            if not method_name:
                continue
            try:
                result_data = self._dispatch(store, method_name, params)
                results[algo] = self._serialize(result_data)
            except Exception as exc:
                failed.append(f"{algo}: {exc}")

        envelope = ExplanationEnvelope(
            decision_summary=f"Swarm completed: {len(results)} succeeded, {len(failed)} failed",
            observed_facts=[f"Swarm executed {len(results)} algorithms"],
            inferred_findings=[f"Failed: {len(failed)}"] if failed else [],
            evidence_refs=[f"algorithm:{a}" for a in results],
            confidence=1.0 if not failed else 0.8,
        )

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED" if not failed else "PARTIAL",
            summary=f"Swarm completed: {len(results)} succeeded, {len(failed)} failed",
            evidence_refs=[f"swarm:{request.request_id}"],
            explanation=envelope,
            data={"results": results, "failed": failed},
        )

    def _extract_params(self, request: AgentRequest) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if request.context_refs:
            if len(request.context_refs) >= 1:
                params["canonical_id"] = request.context_refs[0]
                params["source_id"] = request.context_refs[0]
                params["start_id"] = request.context_refs[0]
                params["root_a"] = request.context_refs[0]
            if len(request.context_refs) >= 2:
                params["target_id"] = request.context_refs[1]
                params["root_b"] = request.context_refs[1]

        budgets = request.budgets or {}
        params["max_depth"] = budgets.get("max_depth", 4)
        params["limit"] = budgets.get("max_results", 20)
        params["k"] = budgets.get("k", 5)
        return params

    def _dispatch(self, store: GraphStore, method_name: str, params: dict[str, Any]) -> Any:
        from eoip.graph.algorithms import GraphAlgorithms
        from eoip.graph.community import CommunityDetectionEngine
        from eoip.graph.metrics import GraphMetricsEngine
        from eoip.graph.paths import GraphPathFinder
        from eoip.graph.similarity import SimilarityEngine

        algo = GraphAlgorithms(store)
        metrics = GraphMetricsEngine(store)
        sim = SimilarityEngine(store)
        paths = GraphPathFinder(store)
        community = CommunityDetectionEngine(store)

        dispatch_map: dict[str, Any] = {
            "detect_rings": lambda: algo.detect_rings(
                max_length=params.get("max_depth", 10), limit=params.get("limit", 20)),
            "detect_intersection": lambda: algo.detect_intersection(
                params["root_a"], params["root_b"], max_depth=params.get("max_depth", 4)),
            "weighted_shortest_path": lambda: algo.weighted_shortest_path(
                params["source_id"], params["target_id"]),
            "single_source_weighted_paths": lambda: algo.single_source_weighted_paths(
                params["source_id"], limit=params.get("limit", 100)),
            "k_step_neighbors": lambda: algo.k_step_neighbors(
                params["canonical_id"], k=params.get("k", 3), limit=params.get("limit", 500)),
            "k_jump": lambda: algo.k_jump(
                params["start_id"], k=params.get("k", 5), walks=params.get("limit", 10)),
            "custom_path": lambda: algo.custom_path(
                params["source_id"], params["target_id"],
                max_depth=params.get("max_depth", 6), max_paths=params.get("limit", 5)),
            "ray_detection": lambda: algo.ray_detection(
                params["source_id"], direction=params.get("direction", "outgoing"),
                max_depth=params.get("max_depth", 10)),
            "co_neighbors": lambda: algo.co_neighbors(
                params["source_id"], params["target_id"]),
            "personal_rank": lambda: algo.personal_rank(
                params["source_id"], limit=params.get("limit", 20)),
            "neighbor_rank": lambda: algo.neighbor_rank(
                params["source_id"], limit=params.get("limit", 20)),
            "model_similarity": lambda: algo.model_similarity(
                params.get("nodes_a", [params.get("source_id", "")]),
                params.get("nodes_b", [params.get("target_id", "")])),
            "centrality_pagerank": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["pagerank"]),
            "centrality_betweenness": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["betweenness"]),
            "centrality_closeness": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["closeness"]),
            "centrality_eigenvector": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["eigenvector"]),
            "centrality_katz": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["katz"]),
            "centrality_hits": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["hits"]),
            "centrality_harmonic": lambda: metrics.full_centrality(
                [params["canonical_id"]], ["harmonic"]),
            "k_core_decomposition": lambda: metrics.k_core_decomposition(),
            "community_detection": lambda: community.label_propagation(),
            "all_shortest_paths": lambda: paths.all_shortest_paths(
                params["source_id"], params["target_id"],
                max_paths=params.get("limit", 5)),
            "k_shortest_paths": lambda: paths.k_shortest_paths(
                params["source_id"], params["target_id"],
                k=params.get("k", 5)),
            "jaccard_similarity": lambda: sim.jaccard(
                params["canonical_id"], limit=params.get("limit", 10)),
            "adamic_adar": lambda: sim.adamic_adar(
                params["canonical_id"], limit=params.get("limit", 10)),
            "common_neighbors_similarity": lambda: sim.common_neighbors(
                params["canonical_id"], limit=params.get("limit", 10)),
            "link_prediction": lambda: sim.link_prediction(
                params["canonical_id"], limit=params.get("limit", 10)),
            "blast_radius": lambda: metrics.blast_radius(
                params["canonical_id"], max_depth=params.get("max_depth", 4)),
            "anomaly_detection": lambda: self._run_anomaly(store),
        }

        fn = dispatch_map.get(method_name)
        if fn is None:
            raise ValueError(f"No dispatch for: {method_name}")
        return fn()

    def _run_anomaly(self, store: GraphStore) -> Any:
        from eoip.graph.anomaly import AnomalyDetector
        detector = AnomalyDetector(store)
        return detector.degree_zscore_outliers()

    def _serialize(self, data: Any) -> Any:
        if data is None:
            return None
        if isinstance(data, (str, int, float, bool)):
            return data
        if isinstance(data, dict):
            return {str(k): self._serialize(v) for k, v in data.items()}
        if isinstance(data, (list, tuple)):
            return [self._serialize(item) for item in data]
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return str(data)
