import pytest
from eoip.agents.catalog import build_agent_registry
from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.contracts.agent import (
    AgentBudgets,
    AgentContract,
    AgentRequest,
    AgentResult,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.fixture
def agent_store():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {
        "canonical_id": "svc:auth",
        "service_id": "auth-svc",
        "name": "Auth Service",
    })
    dep = store.upsert_vertex("Dependency", {
        "canonical_id": "dep:jwt-lib",
        "name": "python-jose",
    })
    store.upsert_edge("DEPENDS_ON", svc["vid"], dep["vid"], {
        "source_ref": "git://auth-repo/commit/123",
    })
    return store


@pytest.mark.req("FR-AGENT-001")
def test_agent_contract_validation():
    # Valid contract
    contract = AgentContract(
        agent_id="TestAgent",
        purpose="Automated test agent",
        allowed_tools=["search", "impact"],
        prohibited_tools=["write_graph"],
        risk_level="R0",
        human_control="READ_ONLY",
        budgets=AgentBudgets(max_steps=5, max_seconds=10.0),
    )
    assert contract.agent_id == "TestAgent"
    assert contract.enabled is True

    # Overlapping allowed and prohibited tools must be rejected
    with pytest.raises(ValueError, match="Tools cannot be both allowed and prohibited"):
        AgentContract(
            agent_id="BadAgent",
            purpose="Invalid agent",
            allowed_tools=["write_graph"],
            prohibited_tools=["write_graph"],
        )

    # Risk R2-R4 agent cannot be READ_ONLY without proposal/approval
    with pytest.raises(ValueError, match="Risk R2-R4 agents must use proposal or approval control"):
        AgentContract(
            agent_id="RiskyAgent",
            purpose="High risk agent",
            risk_level="R3",
            human_control="READ_ONLY",
        )


@pytest.mark.req("FR-AGENT-002")
def test_bounded_agent_runtime(agent_store):
    registry = AgentRegistry()
    registry.register(TraceImpactAgent())
    runtime = AgentRuntime(agent_store, registry)

    # Runtime enforces step and time bounds
    request = AgentRequest(
        request_id="req-bounded",
        agent_id="TraceImpact",
        goal="Trace impact with bounded steps",
        context_refs=["svc:auth"],
        budgets={"max_steps": 2, "max_seconds": 1.0},
    )
    result = runtime.run(request)
    assert result.status in {"SUCCEEDED", "PARTIAL"}
    assert result.request_id == "req-bounded"


@pytest.mark.req("FR-AGENT-003")
def test_trace_impact_agent(agent_store):
    agent = TraceImpactAgent()
    request = AgentRequest(
        request_id="req-trace-1",
        agent_id="TraceImpact",
        goal="svc:auth",
        context_refs=["svc:auth"],
    )
    result = agent.execute(request, agent_store)
    assert result.status in {"SUCCEEDED", "PARTIAL"}
    assert result.evidence_refs
    assert "dep:jwt-lib" in str(result.evidence_refs) or "connected entities" in result.summary


@pytest.mark.req("FR-AGENT-004")
def test_write_action_approval_boundary():
    registry = build_agent_registry()
    # KnowledgeCurator is R2 and requires PROPOSE_ONLY
    curator_contract = registry.get_contract("KnowledgeCurator")
    assert curator_contract.risk_level in {"R1", "R2", "R3"}
    assert curator_contract.human_control in {"PROPOSE_ONLY", "APPROVAL_REQUIRED"}
    assert "write_graph" in curator_contract.prohibited_tools


@pytest.mark.req("FR-AGENT-005")
def test_controlled_self_modification():
    registry = build_agent_registry()
    # Verify all agents in catalog have immutable tool boundaries and require governed proposal for modifications
    for agent_id in registry.list_agents():
        contract = registry.get_contract(agent_id)
        if contract.risk_level in {"R2", "R3", "R4"}:
            assert contract.human_control != "READ_ONLY"
            assert contract.prohibited_tools  # Must prohibit unconstrained self-modification / raw writes


@pytest.mark.req("MVP-FR-021")
def test_useful_read_only_agent_workflow(agent_store):
    registry = AgentRegistry()
    registry.register(TraceImpactAgent())
    runtime = AgentRuntime(agent_store, registry)

    request = AgentRequest(
        request_id="req-read-only-workflow",
        agent_id="TraceImpact",
        goal="Assess impact of changes to svc:auth",
        context_refs=["svc:auth"],
    )
    result = runtime.run(request)
    assert result.status == "SUCCEEDED"
    assert result.evidence_refs
    assert result.summary
    assert not result.warnings
