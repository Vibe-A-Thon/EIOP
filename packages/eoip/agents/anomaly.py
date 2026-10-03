"""AnomalyDetectionAgent: find structurally anomalous nodes (FR-AGENT-003).

Scans the graph for nodes with unusual degree (z-score above threshold)
and optionally detects dense subgraphs.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.anomaly import AnomalyDetector
from eoip.graph.store import GraphStore


class AnomalyDetectionAgent:
    agent_id = "AnomalyDetection"
    allowed_tools = frozenset({"search", "entity"})
    max_steps = 10
    max_seconds = 30.0

    def __init__(self, config: dict | None = None) -> None:
        if config:
            budgets = config.get("budgets", {})
            self.max_steps = budgets.get("max_steps", self.max_steps)
            self.max_seconds = budgets.get("max_seconds", self.max_seconds)
            tools = config.get("allowed_tools")
            if tools:
                self.allowed_tools = frozenset(tools)

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult:
        budgets = request.budgets or {}
        threshold = budgets.get("zscore_threshold", 2.0)
        include_dense = budgets.get("include_dense_subgraphs", False)

        detector = AnomalyDetector(store)
        outliers = detector.degree_zscore_outliers(threshold=threshold)

        tool_calls = [
            {"tool": "search", "input": {"analysis": "degree_zscore", "threshold": threshold}},
        ]

        dense_results = []
        if include_dense:
            dense_results = detector.dense_subgraph_detection()
            tool_calls.append(
                {"tool": "search", "input": {"analysis": "dense_subgraph"}}
            )

        if not outliers and not dense_results:
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary=f"No anomalies detected with z-score threshold {threshold}.",
                evidence_refs=[],
                tool_calls=tool_calls,
            )

        evidence_refs = [o.canonical_id for o in outliers]

        outlier_details = []
        for o in outliers[:10]:
            outlier_details.append(
                f"{o.canonical_id} (degree={o.details['degree']}, "
                f"z={o.details['z_score']}, label={o.details['label']})"
            )

        summary = f"Found {len(outliers)} degree outlier(s) with z-score > {threshold}."
        if outlier_details:
            summary += " Top outliers: " + "; ".join(outlier_details) + "."

        if dense_results:
            summary += (
                f" Also found {len(dense_results)} dense subgraph(s)."
            )
            for dr in dense_results[:3]:
                summary += (
                    f" Cluster around {dr.canonical_id}:"
                    f" {dr.details['cluster_size']} nodes,"
                    f" density={dr.details['local_density']}."
                )
            evidence_refs.extend(dr.canonical_id for dr in dense_results)

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=evidence_refs,
            tool_calls=tool_calls,
        )
