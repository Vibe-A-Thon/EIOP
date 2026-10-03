"""BlastRadiusAgent: compute blast radius for a given entity (FR-AGENT-003).

Uses the GraphMetricsEngine to determine how many entities would be
affected if a target entity changed, with depth breakdown and risk level.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.metrics import GraphMetricsEngine
from eoip.graph.store import GraphStore


class BlastRadiusAgent:
    agent_id = "BlastRadius"
    allowed_tools = frozenset({"search", "entity", "impact"})
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

        engine = GraphMetricsEngine(store)
        result = engine.blast_radius(canonical_id, max_depth=max_depth)

        if result.total_affected == 0 and result.risk == "NONE":
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Entity not found: {canonical_id}",
                evidence_refs=[],
                warnings=["The specified canonical_id does not exist in the graph"],
            )

        tool_calls = [
            {"tool": "impact", "input": {"canonical_id": canonical_id, "max_depth": max_depth}},
        ]

        depth_breakdown = ", ".join(
            f"depth {d}: {count}" for d, count in sorted(result.by_depth.items())
        )
        type_breakdown = ", ".join(
            f"{count} {label}" for label, count in sorted(result.by_type.items())
        )

        summary = (
            f"Blast radius for {canonical_id}: {result.total_affected} affected entities"
            f" within {max_depth} hops. Risk level: {result.risk}."
        )
        if depth_breakdown:
            summary += f" Depth breakdown: {depth_breakdown}."
        if type_breakdown:
            summary += f" By type: {type_breakdown}."

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=result.affected_ids,
            tool_calls=tool_calls,
        )
