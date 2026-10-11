import pytest
from eoip.agents.mcp_pr_tools import (
    MCPPRToolHandler,
    PRFile,
    PRImpactCalculator,
    PullRequest,
    RiskLevel,
)
from eoip.agents.tools import build_graph_tool_registry
from eoip.contracts.tool import ToolRequest
from eoip.graph.memory import MemoryGraphStore


@pytest.mark.req("KGR-G-017")
def test_pr_impact_calculation_direct_and_transitive():
    store = MemoryGraphStore()

    # CodeSymbol representing a changed file
    s1 = store.upsert_vertex("CodeSymbol", {
        "canonical_id": "sym:payments/api.py",
        "name": "PaymentsAPI",
        "path": "src/payments/api.py",
    })
    # Dependent CodeSymbol
    s2 = store.upsert_vertex("CodeSymbol", {
        "canonical_id": "sym:orders/checkout.py",
        "name": "CheckoutService",
        "path": "src/orders/checkout.py",
    })
    # s2 DEPENDS_ON s1
    store.upsert_edge("DEPENDS_ON", s2["vid"], s1["vid"], {})

    calculator = PRImpactCalculator(store)
    pr = PullRequest(
        pr_id="pr-42",
        title="Refactor Payments API",
        author="alice",
        base_branch="main",
        head_branch="feature/payments-v2",
        repo_id="repo-checkout",
        files=[PRFile(path="src/payments/api.py", change_type="modified", additions=50, deletions=20)],
    )

    report = calculator.calculate(pr)
    assert report.pr_id == "pr-42"
    assert report.blast_radius >= 2
    impact_ids = {e.canonical_id for e in report.impacted_entities}
    assert "sym:payments/api.py" in impact_ids
    assert "sym:orders/checkout.py" in impact_ids


@pytest.mark.req("KGR-G-017")
def test_pr_risk_scoring_and_reviewer_suggestion():
    store = MemoryGraphStore()
    calc = PRImpactCalculator(store)

    small_pr = PullRequest(
        pr_id="pr-1",
        title="Fix typo",
        author="alice",
        base_branch="main",
        head_branch="patch-1",
        repo_id="repo-docs",
        files=[PRFile(path="README.md", change_type="modified", additions=1, deletions=1)],
    )
    small_report = calc.calculate(small_pr)
    assert small_report.risk_level in (RiskLevel.MINIMAL, RiskLevel.LOW)

    large_pr = PullRequest(
        pr_id="pr-2",
        title="Major refactor",
        author="alice",
        base_branch="main",
        head_branch="refactor",
        repo_id="repo-core",
        files=[
            PRFile(path=f"src/file_{i}.py", change_type="modified", additions=100, deletions=80)
            for i in range(15)
        ],
    )
    large_report = calc.calculate(large_pr)
    assert large_report.risk_score > small_report.risk_score


@pytest.mark.req("KGR-G-017")
def test_mcp_pr_tools_invocation_through_registry():
    store = MemoryGraphStore()
    registry = build_graph_tool_registry(store)

    assert registry.get("list_prs") is not None
    assert registry.get("get_pr_impact") is not None
    assert registry.get("triage_prs") is not None

    req = ToolRequest(
        tool_call_id="call-1",
        tool_name="get_pr_impact",
        arguments={
            "pr": {
                "pr_id": "pr-100",
                "title": "Update billing endpoint",
                "author": "bob",
                "repo_id": "repo-billing",
                "files": [{"path": "billing.py", "additions": 10, "deletions": 5}],
            }
        },
    )
    result = registry.invoke(req, allowed_tools={"get_pr_impact"}, remaining_seconds=10.0)
    assert result.status == "SUCCEEDED"
    assert result.result["pr_id"] == "pr-100"
    assert "risk_level" in result.result


@pytest.mark.req("KGR-G-017")
def test_triage_prs_ranking():
    store = MemoryGraphStore()
    handler = MCPPRToolHandler(store)

    prs = [
        {"pr_id": "pr-small", "files": [{"path": "a.txt", "additions": 2, "deletions": 1}]},
        {"pr_id": "pr-large", "files": [{"path": f"b_{i}.py", "additions": 50, "deletions": 30} for i in range(10)]},
    ]
    result, evidence = handler.triage_prs({"prs": prs})
    assert result["triage_count"] == 2
    assert result["ranked_prs"][0]["pr_id"] == "pr-large"  # Higher risk ranked first
