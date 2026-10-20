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


def _cross_repo_store():
    store = MemoryGraphStore()
    core = store.upsert_vertex("CodeSymbol", {"canonical_id": "sym:repo-core:api", "name": "CoreAPI",
                                              "path": "src/api.py", "repo_id": "repo-core"})
    client = store.upsert_vertex("CodeSymbol", {"canonical_id": "sym:repo-client:sdk", "name": "ClientSDK",
                                                "path": "sdk/client.py", "repo_id": "repo-client"})
    app = store.upsert_vertex("CodeSymbol", {"canonical_id": "sym:repo-app:checkout", "name": "Checkout",
                                             "path": "app/checkout.py", "repo_id": "repo-app"})
    # same path, unrelated repository: must not be treated as the changed file
    store.upsert_vertex("CodeSymbol", {"canonical_id": "sym:repo-other:api", "name": "OtherAPI",
                                       "path": "src/api.py", "repo_id": "repo-other"})
    store.upsert_edge("DEPENDS_ON", client["vid"], core["vid"], {})
    store.upsert_edge("DEPENDS_ON", app["vid"], client["vid"], {})
    return store


def _core_pr():
    return PullRequest(pr_id="pr-7", title="Change core API", author="alice", base_branch="main",
                       head_branch="feat", repo_id="repo-core",
                       files=[PRFile(path="src/api.py", change_type="modified", additions=40, deletions=10)])


@pytest.mark.req("KGR-G-017")
def test_blast_radius_spans_three_connected_repositories_and_ignores_same_path_elsewhere():
    report = PRImpactCalculator(_cross_repo_store()).calculate(_core_pr())
    ids = [e.canonical_id for e in report.impacted_entities]
    assert ids == ["sym:repo-core:api", "sym:repo-client:sdk", "sym:repo-app:checkout"]
    assert report.repos_affected == ["repo-app", "repo-client", "repo-core"]
    assert "sym:repo-other:api" not in ids


@pytest.mark.req("KGR-G-017")
def test_risk_score_and_report_are_deterministic_for_identical_diffs():
    store = _cross_repo_store()
    first = PRImpactCalculator(store).calculate(_core_pr())
    second = PRImpactCalculator(store).calculate(_core_pr())
    assert first.risk_score == second.risk_score and first.risk_level == second.risk_level
    assert [e.canonical_id for e in first.impacted_entities] == [e.canonical_id for e in second.impacted_entities]
    assert first.summary == second.summary


@pytest.mark.req("KGR-G-017")
def test_pr_tool_definitions_are_mcp_tools_with_valid_json_schema_input():
    import jsonschema

    registry = build_graph_tool_registry(MemoryGraphStore())
    for name in ("list_prs", "get_pr_impact", "triage_prs"):
        tool = registry.get(name)
        schema = tool.input_schema
        jsonschema.Draft202012Validator.check_schema(schema)  # MCP inputSchema is JSON Schema
        assert schema["type"] == "object" and tool.name == name and tool.description
    bad = registry.invoke(ToolRequest(tool_call_id="c", tool_name="get_pr_impact", arguments={"pr": {"title": "x"}}),
                          allowed_tools={"get_pr_impact"}, remaining_seconds=5)
    assert bad.status == "FAILED" and bad.error["code"] == "INVALID_ARGUMENTS"
