"""TestCoverageAgent: identify work items lacking test coverage (FR-AGENT-003).

Scans WorkItem, Feature, and UserStory vertices for those that have no
incoming TESTS edges, reporting coverage gaps.
"""

from __future__ import annotations

from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.store import GraphStore

# Vertex labels that should have test coverage
_COVERABLE_LABELS = ["WorkItem", "Feature", "UserStory"]

# Edge labels indicating test coverage
_TEST_EDGE_LABELS = ["TESTS", "VALIDATES", "COVERS"]


class TestCoverageAgent:
    agent_id = "TestCoverage"
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
        labels_to_check = budgets.get("labels", _COVERABLE_LABELS)
        limit_per_label = min(budgets.get("limit", 500), 5000)

        tool_calls = [
            {"tool": "search", "input": {"labels": labels_to_check, "analysis": "test_coverage"}},
        ]

        total_checked = 0
        uncovered: list[dict] = []
        covered_count = 0
        label_stats: dict[str, dict] = {}

        for label in labels_to_check:
            vertices = store.find_vertices(label=label, limit=limit_per_label)
            label_total = len(vertices)
            label_uncovered = 0

            for v in vertices:
                total_checked += 1
                cid = v["properties"]["canonical_id"]

                # Check if any TESTS/VALIDATES/COVERS edge points TO this vertex
                has_test = False
                incoming = store.edges_to(v["vid"])
                for edge in incoming:
                    if edge["label"] in _TEST_EDGE_LABELS:
                        has_test = True
                        break

                if has_test:
                    covered_count += 1
                else:
                    label_uncovered += 1
                    uncovered.append({
                        "canonical_id": cid,
                        "label": label,
                        "name": v["properties"].get("name", v["properties"].get("title", cid)),
                    })

            label_stats[label] = {
                "total": label_total,
                "uncovered": label_uncovered,
                "covered": label_total - label_uncovered,
            }

        if total_checked == 0:
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary="No coverable entities found in the graph (no WorkItem, Feature, or UserStory vertices).",
                evidence_refs=[],
                tool_calls=tool_calls,
            )

        coverage_pct = (covered_count / total_checked * 100) if total_checked > 0 else 0.0
        evidence_refs = [u["canonical_id"] for u in uncovered]

        # Per-label breakdown
        label_breakdown = ", ".join(
            f"{label}: {stats['covered']}/{stats['total']} covered"
            for label, stats in sorted(label_stats.items())
            if stats["total"] > 0
        )

        summary = (
            f"Test coverage: {covered_count}/{total_checked} entities covered"
            f" ({coverage_pct:.1f}%). {len(uncovered)} gap(s) found."
        )
        if label_breakdown:
            summary += f" By type: {label_breakdown}."

        # List specific gaps (up to 10)
        if uncovered:
            gap_list = "; ".join(
                f"{u['canonical_id']} [{u['label']}]"
                for u in uncovered[:10]
            )
            summary += f" Uncovered: {gap_list}."
            if len(uncovered) > 10:
                summary += f" (and {len(uncovered) - 10} more)"

        warnings = None
        if coverage_pct < 50:
            warnings = [f"Test coverage is below 50% ({coverage_pct:.1f}%)"]

        return AgentResult(
            request_id=request.request_id,
            status="SUCCEEDED",
            summary=summary,
            evidence_refs=evidence_refs,
            tool_calls=tool_calls,
            warnings=warnings,
        )
