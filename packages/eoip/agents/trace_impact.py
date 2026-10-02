"""TraceImpactAgent: deterministic read-only trace/impact analysis (FR-AGENT-003).

Uses allowlisted read tools (search, path, impact, lineage) to answer
trace and impact requests. Returns decision summary and evidence refs.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.store import GraphStore
from eoip.graph.traversal import GraphTraversal


class TraceImpactAgent:
    agent_id = "TraceImpact"
    allowed_tools = frozenset({"search", "entity", "path", "impact", "lineage"})
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
        canonical_id = request.context_refs[0] if request.context_refs else request.goal
        budgets = request.budgets or {}
        max_depth = min(budgets.get("max_depth", 4), 8)
        max_seconds = min(budgets.get("max_seconds", self.max_seconds), self.max_seconds)

        traversal = GraphTraversal(store, max_results=100, timeout_seconds=max_seconds)
        result = traversal.impact(canonical_id, max_depth=max_depth)

        if not result["source"]:
            if result["truncated"]:
                return AgentResult(
                    request_id=request.request_id,
                    status="PARTIAL",
                    summary="Traversal time budget expired before the source entity could be resolved.",
                    evidence_refs=[],
                    warnings=["Traversal stopped before source resolution"],
                )
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Entity not found: {canonical_id}",
                evidence_refs=[],
                warnings=["The specified canonical_id does not exist in the graph"],
            )

        impacted = result["impacted"]
        refs = sorted(
            {
                edge["properties"]["source_ref"]
                for item in impacted
                for edge in item["path"]["edges"]
                if edge["properties"].get("source_ref")
            }
        )

        tool_calls = [
            {"tool": "impact", "input": {"canonical_id": canonical_id, "max_depth": max_depth}},
        ]

        labels = {}
        for item in impacted:
            label = item["vertex"]["label"]
            labels[label] = labels.get(label, 0) + 1
        breakdown = ", ".join(f"{count} {label}" for label, count in sorted(labels.items()))

        summary = (
            f"Found {len(impacted)} connected entities within {max_depth} hops"
            f" of {canonical_id}."
        )
        if breakdown:
            summary += f" Breakdown: {breakdown}."
        if refs:
            summary += f" {len(refs)} source references found."

        return AgentResult(
            request_id=request.request_id,
            status="PARTIAL" if result["truncated"] else "SUCCEEDED",
            summary=summary,
            evidence_refs=refs,
            tool_calls=tool_calls,
            warnings=["Results truncated by traversal budget"] if result["truncated"] else None,
        )
