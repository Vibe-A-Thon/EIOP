"""Tests for the agent registry, runtime, and TraceImpactAgent."""

import pytest
from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.contracts.agent import AgentRequest
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
