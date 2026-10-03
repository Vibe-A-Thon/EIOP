"""IncidentCorrelationAgent: trace incident cause chains (FR-AGENT-003).

Takes an incident canonical_id and traces TRIGGERED_BY, RESOLVES, and
related edges to find correlated commits, deployments, and change requests.
"""

from __future__ import annotations

from collections import deque

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.store import GraphStore

# Edge labels relevant to incident correlation
_CORRELATION_EDGES = frozenset({
    "TRIGGERED_BY",
    "RESOLVES",
    "CAUSED_BY",
    "CORRELATES_WITH",
    "PRODUCED_BY",
    "MODIFIES",
    "DEPLOYED_BY",
    "REFERENCES",
})

# Vertex labels that represent correlated entities
_CORRELATED_TYPES = frozenset({
    "Commit",
    "Deployment",
    "ChangeRequest",
    "MergeRequest",
    "Incident",
    "Alert",
    "Pipeline",
    "Release",
})


class IncidentCorrelationAgent:
    agent_id = "IncidentCorrelation"
    allowed_tools = frozenset({"search", "entity", "path", "lineage"})
    max_steps = 15
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

        root = store.get_vertex_by_canonical_id(canonical_id)
        if root is None:
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Incident entity not found: {canonical_id}",
                evidence_refs=[],
                warnings=["The specified canonical_id does not exist in the graph"],
            )

        tool_calls = [
            {"tool": "entity", "input": {"canonical_id": canonical_id}},
            {"tool": "lineage", "input": {"canonical_id": canonical_id, "max_depth": max_depth}},
        ]

        # BFS traversal following correlation edges
        visited: set[str] = {root["vid"]}
        queue: deque[tuple[str, int, list[str]]] = deque([(root["vid"], 0, [])])
        correlations: list[dict] = []

        while queue:
            vid, depth, chain = queue.popleft()
            if depth >= max_depth:
                continue

            # Check outgoing edges
            for edge in store.edges_from(vid):
                if edge["label"] not in _CORRELATION_EDGES:
                    continue
                tgt_vid = edge["in_v"]
                if tgt_vid in visited:
                    continue
                visited.add(tgt_vid)
                target = store.get_vertex(tgt_vid)
                if target is None:
                    continue
                new_chain = chain + [f"--({edge['label']})-->"]
                tgt_cid = target["properties"]["canonical_id"]
                correlations.append({
                    "canonical_id": tgt_cid,
                    "label": target["label"],
                    "edge_label": edge["label"],
                    "depth": depth + 1,
                    "chain": new_chain + [tgt_cid],
                })
                queue.append((tgt_vid, depth + 1, new_chain + [tgt_cid]))

            # Check incoming edges
            for edge in store.edges_to(vid):
                if edge["label"] not in _CORRELATION_EDGES:
                    continue
                src_vid = edge["out_v"]
                if src_vid in visited:
                    continue
                visited.add(src_vid)
                source = store.get_vertex(src_vid)
                if source is None:
                    continue
                new_chain = chain + [f"<--({edge['label']})--"]
                src_cid = source["properties"]["canonical_id"]
                correlations.append({
                    "canonical_id": src_cid,
                    "label": source["label"],
                    "edge_label": edge["label"],
                    "depth": depth + 1,
                    "chain": new_chain + [src_cid],
                })
                queue.append((src_vid, depth + 1, new_chain + [src_cid]))

        if not correlations:
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary=(
                    f"No correlated entities found for incident {canonical_id}"
                    f" within {max_depth} hops."
                ),
                evidence_refs=[],
                tool_calls=tool_calls,
            )

        evidence_refs = [c["canonical_id"] for c in correlations]

        # Group by type
        by_type: dict[str, list[str]] = {}
        for c in correlations:
            by_type.setdefault(c["label"], []).append(c["canonical_id"])

        type_summary = ", ".join(
            f"{len(ids)} {label}(s)" for label, ids in sorted(by_type.items())
        )

        # Build chain descriptions for top correlations
        chain_details = []
        for c in correlations[:5]:
            chain_str = " ".join(c["chain"])
            chain_details.append(f"{c['canonical_id']} [{c['label']}] at depth {c['depth']}: {chain_str}")

        summary = (
            f"Incident {canonical_id} correlates with {len(correlations)} entities"
            f" within {max_depth} hops. By type: {type_summary}."
        )
        if chain_details:
            summary += " Correlation chains: " + "; ".join(chain_details) + "."

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=evidence_refs,
            tool_calls=tool_calls,
        )
