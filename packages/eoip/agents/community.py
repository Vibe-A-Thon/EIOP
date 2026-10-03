"""CommunityAnalysisAgent: detect communities in the knowledge graph (FR-AGENT-003).

Uses the CommunityDetectionEngine with label-propagation to find
clusters of tightly connected entities.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.community import CommunityDetectionEngine
from eoip.graph.store import GraphStore


class CommunityAnalysisAgent:
    agent_id = "CommunityAnalysis"
    allowed_tools = frozenset({"search", "entity"})
    max_steps = 10
    max_seconds = 60.0

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
        algorithm = budgets.get("algorithm", "label_propagation")
        max_iterations = min(budgets.get("max_iterations", 20), 50)

        engine = CommunityDetectionEngine(store)

        if algorithm == "louvain":
            resolution = budgets.get("resolution", 1.0)
            result = engine.louvain(resolution=resolution)
        else:
            result = engine.label_propagation(max_iterations=max_iterations)

        if not result.communities:
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary="No communities detected. The graph may be empty or fully disconnected.",
                evidence_refs=[],
                tool_calls=[{"tool": "search", "input": {"algorithm": algorithm}}],
            )

        tool_calls = [
            {"tool": "search", "input": {"algorithm": algorithm}},
        ]

        sizes = [c["size"] for c in result.communities]
        size_summary = ", ".join(
            f"community {c['id']}: {c['size']} members"
            for c in result.communities[:10]
        )

        summary = (
            f"Detected {len(result.communities)} communities using {result.algorithm}."
            f" Modularity: {result.modularity}."
            f" Sizes: min={min(sizes)}, max={max(sizes)}, avg={sum(sizes)/len(sizes):.1f}."
        )
        if size_summary:
            summary += f" Top communities: {size_summary}."

        # Collect member IDs from the largest communities as evidence
        evidence_refs = []
        for c in result.communities[:5]:
            evidence_refs.extend(c["members"][:10])

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=evidence_refs,
            tool_calls=tool_calls,
        )
