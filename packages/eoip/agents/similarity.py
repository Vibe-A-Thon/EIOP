"""SimilarityAgent: find structurally similar nodes (FR-AGENT-003).

Takes a canonical_id from context_refs and finds nodes with the most
similar neighbourhood structure using Jaccard similarity.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.similarity import SimilarityEngine
from eoip.graph.store import GraphStore


class SimilarityAgent:
    agent_id = "Similarity"
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
        canonical_id = request.context_refs[0] if request.context_refs else request.goal
        budgets = request.budgets or {}
        limit = min(budgets.get("limit", 10), 50)
        algorithm = budgets.get("algorithm", "jaccard")

        engine = SimilarityEngine(store)

        if algorithm == "adamic_adar":
            results = engine.adamic_adar(canonical_id, limit=limit)
        elif algorithm == "common_neighbors":
            results = engine.common_neighbors(canonical_id, limit=limit)
        else:
            results = engine.jaccard(canonical_id, limit=limit)

        tool_calls = [
            {"tool": "entity", "input": {"canonical_id": canonical_id}},
            {"tool": "search", "input": {"algorithm": algorithm, "limit": limit}},
        ]

        if not results:
            # Check if the entity exists at all
            v = store.get_vertex_by_canonical_id(canonical_id)
            if v is None:
                return AgentResult(
                    request_id=request.request_id,
                    status="FAILED",
                    summary=f"Entity not found: {canonical_id}",
                    evidence_refs=[],
                    tool_calls=tool_calls,
                    warnings=["The specified canonical_id does not exist in the graph"],
                )
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary=f"No structurally similar nodes found for {canonical_id}.",
                evidence_refs=[],
                tool_calls=tool_calls,
            )

        evidence_refs = [r.canonical_id for r in results]

        entries = []
        for r in results:
            entries.append(
                f"{r.canonical_id} (score={r.score}, "
                f"common_neighbors={r.common_neighbors})"
            )

        summary = (
            f"Top {len(results)} nodes similar to {canonical_id}"
            f" by {algorithm}: " + "; ".join(entries) + "."
        )

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=evidence_refs,
            tool_calls=tool_calls,
        )
