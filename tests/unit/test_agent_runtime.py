"""Tests for the agent registry, runtime, and TraceImpactAgent."""

import pytest
from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.agents.tools import ToolRegistry
from eoip.contracts.tool import ToolContract, ToolRequest
from eoip.graph.memory import MemoryGraphStore


def _loaded_store():
    store = MemoryGraphStore()
    wi = store.upsert_vertex("WorkItem", {
        "canonical_id": "urn:test:item:1", "issue_key": "TEST-1", "summary": "Test",
    })
    commit = store.upsert_vertex("Commit", {
        "canonical_id": "urn:test:commit:abc", "commit_sha": "abc123",
    })
    store.upsert_edge("IMPLEMENTS", commit["vid"], wi["vid"], {
        "fact_key": "test-impl", "creation_status": "DETERMINISTIC",
        "source_ref": "git://abc123", "evidence_key": "ev1",
    })
    return store


def test_trace_impact_agent_succeeds():
    store = _loaded_store()
    registry = AgentRegistry()
    registry.register(TraceImpactAgent())
    runtime = AgentRuntime(store, registry)

    request = AgentRequest(
        request_id="req-1", agent_id="TraceImpact",
        goal="Trace impact of TEST-1",
        context_refs=["urn:test:item:1"],
        budgets={"max_depth": 4},
    )
    result = runtime.run(request)
    assert result.status in {"SUCCEEDED", "PARTIAL"}
    assert "connected entities" in result.summary
    assert result.evidence_refs


def test_agent_not_found_returns_denied():
    store = MemoryGraphStore()
    registry = AgentRegistry()
    runtime = AgentRuntime(store, registry)
    request = AgentRequest(
        request_id="req-2", agent_id="NonExistent",
        goal="Test", context_refs=["x"],
    )
    result = runtime.run(request)
    assert result.status == "DENIED"


def test_runtime_clamps_and_forwards_agent_time_budget():
    received_budgets = {}

    class BudgetProbeAgent:
        agent_id = "BudgetProbe"
        allowed_tools = frozenset({"impact"})
        max_steps = 3
        max_seconds = 5.0

        def execute(self, request, store):
            received_budgets.update(request.budgets)
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary="Budget received",
                evidence_refs=[],
            )

    registry = AgentRegistry()
    registry.register(BudgetProbeAgent())
    runtime = AgentRuntime(MemoryGraphStore(), registry)
    request = AgentRequest(
        request_id="req-budget",
        agent_id="BudgetProbe",
        goal="Check budget propagation",
        budgets={"max_seconds": 0.25, "max_steps": 2},
    )

    result = runtime.run(request)

    assert result.status == "SUCCEEDED"
    assert received_budgets["max_seconds"] == 0.25
    assert received_budgets["max_steps"] == 2


def test_run_persistence_failure_is_reported(monkeypatch):
    class FailingPersistenceStore(MemoryGraphStore):
        def upsert_vertex(self, label, properties):
            if label == "AgentRun":
                raise OSError("storage unavailable")
            return super().upsert_vertex(label, properties)

    class SuccessfulAgent:
        agent_id = "SuccessfulAgent"
        allowed_tools = frozenset({"impact"})
        max_steps = 1
        max_seconds = 5.0

        def execute(self, request, store):
            return AgentResult(
                request_id=request.request_id,
                status="SUCCEEDED",
                summary="Completed",
                evidence_refs=[],
            )

    registry = AgentRegistry()
    registry.register(SuccessfulAgent())
    runtime = AgentRuntime(FailingPersistenceStore(), registry)
    log_events = []
    monkeypatch.setattr(
        "eoip.agents.runtime.log.error",
        lambda message, **kwargs: log_events.append(message),
    )
    request = AgentRequest(
        request_id="req-persist",
        agent_id="SuccessfulAgent",
        goal="Run with failing audit persistence",
    )

    result = runtime.run(request)

    assert result.status == "PARTIAL"
    assert "Agent run could not be persisted" in result.warnings
    assert "agent.run.persist_failed" in log_events


def test_failed_agent_execution_is_persisted():
    class FailingAgent:
        agent_id = "FailingAgent"
        allowed_tools = frozenset({"impact"})
        max_steps = 1
        max_seconds = 5.0

        def execute(self, request, store):
            raise ValueError("execution failed")

    store = MemoryGraphStore()
    registry = AgentRegistry()
    registry.register(FailingAgent())
    runtime = AgentRuntime(store, registry)
    request = AgentRequest(
        request_id="req-failed",
        agent_id="FailingAgent",
        goal="Persist an execution failure",
    )

    result = runtime.run(request)
    run = store.get_vertex_by_canonical_id("urn:eoip:agent:run:req-failed")

    assert result.status == "FAILED"
    assert run["properties"]["run_status"] == "FAILED"


def test_trace_impact_agent_entity_not_found():
    store = MemoryGraphStore()
    registry = AgentRegistry()
    registry.register(TraceImpactAgent())
    runtime = AgentRuntime(store, registry)

    request = AgentRequest(
        request_id="req-3", agent_id="TraceImpact",
        goal="Trace missing", context_refs=["urn:missing"],
    )
    result = runtime.run(request)
    assert result.status == "FAILED"
    assert "not found" in result.summary.lower()


def test_trace_impact_reports_partial_when_budget_expires_before_source(monkeypatch):
    class ExpiredTraversal:
        def __init__(self, store, *, max_results, timeout_seconds):
            assert timeout_seconds == 0.1

        def impact(self, canonical_id, *, max_depth):
            return {"source": None, "impacted": [], "truncated": True}

    monkeypatch.setattr("eoip.agents.trace_impact.GraphTraversal", ExpiredTraversal)
    agent = TraceImpactAgent()
    request = AgentRequest(
        request_id="req-expired",
        agent_id="TraceImpact",
        goal="Trace impact",
        context_refs=["urn:test:item:1"],
        budgets={"max_seconds": 0.1},
    )

    result = agent.execute(request, MemoryGraphStore())

    assert result.status == "PARTIAL"
    assert result.evidence_refs == []
    assert result.warnings


def test_registry_rejects_write_tools():
    class WriteAgent:
        agent_id = "Writer"
        allowed_tools = frozenset({"search", "write_vertex"})
        max_steps = 1
        max_seconds = 5.0
        def execute(self, request, store): pass

    registry = AgentRegistry()
    with pytest.raises(ValueError):
        registry.register(WriteAgent())


def test_approval_required_tool_rejects_unresolved_approval_id():
    calls = []
    tools = ToolRegistry()
    tools.register(
        ToolContract(
            name="dangerous_write",
            description="A consequential write tool",
            risk_level="R2",
            read_only=False,
        ),
        lambda arguments: (calls.append(arguments) or {"changed": True}, []),
    )

    result = tools.invoke(
        ToolRequest(
            tool_call_id="call-1",
            tool_name="dangerous_write",
            arguments={"target": "resource-1"},
            actor_id="agent-1",
            approval_id="fabricated-approval-id",
        ),
        allowed_tools={"dangerous_write"},
        remaining_seconds=1,
    )

    assert result.status == "DENIED"
    assert result.error == {"code": "APPROVAL_NOT_VERIFIED"}
    assert calls == []
