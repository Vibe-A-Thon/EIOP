"""Tests for packages/eoip/agentarch (GAP-ARCH).

Every architecture class must be instantiable and run a scripted task within
budgets; every orchestration pattern must coordinate 2-3 stub agents; the
A2A envelope must round-trip.
"""

from __future__ import annotations

from typing import Any

import pytest

from eoip.agentarch import A2ABus, A2AMessage, CapabilityCard, RuntimeRunner
from eoip.agentarch.org import PATTERNS, Coordinator, RuntimeRunner as OrgRunner
from eoip.contracts.agent import AgentRequest, AgentResult
from eoip.graph.memory import MemoryGraphStore


def _request(goal: str, **kwargs) -> AgentRequest:
    return AgentRequest(request_id="test-req-1", agent_id="urn:test", goal=goal,
                        actor_id="tester", **kwargs)


STORE = MemoryGraphStore()


# ---------------------------------------------------------------------------
# (A) classical types
# ---------------------------------------------------------------------------

from eoip.agentarch.classical import (  # noqa: E402
    BDIAgent, BayesianAgent, CausalReasoningAgent, DeliberativeAgent,
    EmbodiedAgent, HybridAgent, KnowledgeBasedAgent, LearningAgent,
    MPCAgent, MetaReasoningAgent, MultimodalAgent, NeuroSymbolicAgent,
    ProbabilisticAgent, RLAgent, ReactiveAgent, StatefulAgent,
    StatelessAgent, WorldModelAgent,
)

CLASSICAL = [
    LearningAgent(seed=1),
    KnowledgeBasedAgent(rules=[("r1", ["label"], "then-x")], seed=1),
    BDIAgent(desires=[("a", 0.5), ("b", 0.9)], seed=1),
    ReactiveAgent(rules=[("help", "assist")], seed=1),
    DeliberativeAgent(seed=1),
    HybridAgent(rules=[("help", "assist")], seed=1),
    StatefulAgent(seed=1),
    StatelessAgent(seed=1),
    ProbabilisticAgent(distribution={"go": 0.8, "stop": 0.2}, seed=3),
    BayesianAgent(priors={"h1": (2.0, 1.0), "h2": (1.0, 3.0)}, seed=1),
    RLAgent(actions=["left", "right"], seed=2),
    NeuroSymbolicAgent(rules=[("r", ["x"], "y")], perceive_hook=lambda g: ["cue"], seed=1),
    WorldModelAgent(transitions={("s0", "a"): "s1"}, actions=["a"], seed=1),
    CausalReasoningAgent(seed=1),
    MetaReasoningAgent(strategies={"s1": 0.4, "s2": 0.9}, seed=1),
    EmbodiedAgent(seed=1),
    MultimodalAgent(handlers={"text": lambda g: "ok"}, seed=1),
    MPCAgent(actions=["a", "b"], horizon=2, cost_fn=lambda seq: len([x for x in seq if x == "a"]), seed=1),
]


@pytest.mark.parametrize("agent", CLASSICAL, ids=lambda a: a.architecture)
def test_classical_runs_within_budget(agent):
    result = agent.execute(_request("help me analyse the graph"), STORE)
    assert result.status in {"SUCCEEDED", "PARTIAL", "FAILED"}
    assert result.summary
    assert agent._steps_used <= agent.max_steps


def test_learning_feedback_updates_policy():
    agent = LearningAgent(seed=1)
    agent.record_feedback(1.0, {"state": "s", "action": "a"})
    assert agent.policy["s"]["a"] > 0.5
    agent.act(_request("anything"), STORE)
    assert agent.feedback_count == 1


def test_bayesian_updates_belief():
    agent = BayesianAgent(seed=1)
    before = agent.beliefs["h1"][0]
    agent.update("h1", True)
    assert agent.beliefs["h1"][0] == before + 1


def test_rl_updates_q_table():
    agent = RLAgent(actions=["left", "right"], seed=1)
    agent.learn("s0", "right", 1.0, "s0")
    assert agent.q_table["s0"]["right"] > 0


def test_rl_deterministic_with_seed():
    a1 = RLAgent(seed=7).act(_request("learn"), STORE)
    a2 = RLAgent(seed=7).act(_request("learn"), STORE)
    assert a1["data"]["best_action"] == a2["data"]["best_action"]


def test_embodied_external_gate_manifest():
    agent = EmbodiedAgent(seed=1)
    outcome = agent.act(_request("move"), STORE)
    assert outcome["data"]["manifest"]["external_gate"] is True


def test_multimodal_unregistered_modality_is_gate():
    agent = MultimodalAgent(handlers={"text": lambda g: "ok"}, seed=1)
    outcome = agent.act(_request("describe", metadata={"modalities": ["text", "audio"]}), STORE)
    assert outcome["data"]["routed"]["text"]["status"] == "SUCCEEDED"
    assert outcome["data"]["routed"]["audio"]["status"] == "EXTERNAL_GATE"


# ---------------------------------------------------------------------------
# (B) advanced reasoning
# ---------------------------------------------------------------------------

from eoip.agentarch.reasoning import (  # noqa: E402
    ArbitrationAgent, CounterfactualAgent, DebateAgent, FormalReasoningAgent,
    GraphOfThoughtAgent, HypothesisTestingAgent, MCTSAgent,
    PlanAndExecuteAgent, ReActAgent, ReplanningAgent, ReflexionAgent,
    SearchBasedAgent, SimulationAgent, TreeOfThoughtAgent, VerificationAgent,
)

REASONING = [
    ReActAgent(seed=1, max_iterations=2),
    PlanAndExecuteAgent(seed=1),
    TreeOfThoughtAgent(branch_factor=2, depth=2, seed=1),
    GraphOfThoughtAgent(seed=1),
    SearchBasedAgent(seed=1),
    MCTSAgent(simulations=4, rollout_depth=2, seed=5),
    ReplanningAgent(seed=1),
    ReflexionAgent(criteria=["x", "y"], seed=1),
    HypothesisTestingAgent(hypotheses=["h-alpha", "h-beta"], seed=1),
    SimulationAgent(seed=1),
    CounterfactualAgent(options=["a", "b"], seed=1),
    DebateAgent(rounds=2, seed=1),
    ArbitrationAgent(seed=1),
    VerificationAgent(seed=1),
    FormalReasoningAgent(invariants=[("nonempty", "count(*) >= 0")], seed=1),
]


@pytest.mark.parametrize("agent", REASONING, ids=lambda a: a.architecture)
def test_reasoning_runs_within_budget(agent):
    result = agent.execute(
        _request("analyse quality; find errors; help", context_refs=["urn:alpha", "urn:beta"]), STORE)
    assert result.status in {"SUCCEEDED", "PARTIAL"}
    assert agent._steps_used <= agent.max_steps


def test_mcts_deterministic():
    a = MCTSAgent(simulations=6, seed=11)
    b = MCTSAgent(simulations=6, seed=11)
    ra = a.act(_request("plan"), STORE)
    rb = b.act(_request("plan"), STORE)
    assert ra["data"]["mean_value"] == rb["data"]["mean_value"]


def test_formal_reasoning_detects_violation():
    agent = FormalReasoningAgent(invariants=[("too-big", "count(*) > 1000000")], seed=1)
    outcome = agent.act(_request("check"), STORE)
    assert outcome["status"] == "PARTIAL"
    assert outcome["warnings"] == ["too-big"]


def test_reflexion_memory_grows():
    agent = ReflexionAgent(seed=1)
    agent.act(_request("one"), STORE)
    agent.act(_request("two"), STORE)
    assert len(agent.feedback_memory) == 2


# ---------------------------------------------------------------------------
# (C) enterprise operational classes
# ---------------------------------------------------------------------------

from eoip.agentarch.enterprise import (  # noqa: E402
    AuditAgent, BenchmarkingAgent, CodeEngineeringAgent, ConnectorAgent,
    ContextManagementAgent, CostOptimizationAgent, CrawlerAgent,
    DebuggingAgent, DeploymentAgent, DiscoveryAgent, DocumentationAgent,
    EntityResolutionAgent, EvaluatorAgent, EvidenceProvenanceAgent,
    GraphValidationAgent, HumanEscalationAgent, IngestionAgent,
    KGBuilderAgent, MemoryManagementAgent, ModelSelectionAgent,
    OntologyAgent, PolicyEnforcementAgent, QueryTranslationAgent,
    RecoveryAgent, RiskAssessmentAgent, SecurityMonitoringAgent,
    TestingAgent as TestingOpsAgent,
)

ENTERPRISE = [
    DiscoveryAgent(), ConnectorAgent(), CrawlerAgent(), IngestionAgent(),
    EntityResolutionAgent(), KGBuilderAgent(), GraphValidationAgent(),
    OntologyAgent(), QueryTranslationAgent(), EvidenceProvenanceAgent(),
    MemoryManagementAgent(), ContextManagementAgent(), ModelSelectionAgent(),
    CostOptimizationAgent(), SecurityMonitoringAgent(),
    PolicyEnforcementAgent(), RiskAssessmentAgent(), AuditAgent(),
    HumanEscalationAgent(), RecoveryAgent(), BenchmarkingAgent(),
    EvaluatorAgent(), CodeEngineeringAgent(), TestingOpsAgent(), DebuggingAgent(),
    DeploymentAgent(), DocumentationAgent(),
]


@pytest.mark.parametrize("agent", ENTERPRISE, ids=lambda a: a.capability)
def test_enterprise_contract_and_run(agent):
    contract = agent.contract()
    assert contract["inputs"] and contract["outputs"]
    result = agent.execute(
        _request("help analyse service errors", metadata={"claims": []}), STORE)
    assert result.status in {"SUCCEEDED", "PARTIAL", "DENIED"}
    assert result.summary


def test_policy_enforcement_denies():
    agent = PolicyEnforcementAgent(policies=[("deny", "drop"), ("allow", "")])
    result = agent.execute(_request("please drop the table"), STORE)
    assert result.status == "DENIED"


def test_security_monitoring_flags_credential():
    agent = SecurityMonitoringAgent()
    result = agent.execute(_request("leaked password in logs"), STORE)
    assert result.status == "PARTIAL"
    assert "password" in result.warnings


def test_query_translation_eoql():
    agent = QueryTranslationAgent()
    result = agent.execute(_request("SELECT name FROM Entity LIMIT 3"), STORE)
    assert result.status == "SUCCEEDED"
    assert result.data["plan"]


def test_model_selection_uses_registry():
    from eoip.models.governance import ModelEntry, ModelHealth, ModelRegistry

    registry = ModelRegistry()
    registry.register(ModelEntry(model_id="m-fast", provider="local",
                                 version="1.0.0", health=ModelHealth.HEALTHY))
    agent = ModelSelectionAgent(model_registry=registry)
    result = agent.execute(_request("summarize"), STORE)
    assert result.data["model_id"] == "m-fast"


# ---------------------------------------------------------------------------
# (D) org patterns with stub runner
# ---------------------------------------------------------------------------

class StubRunner:
    """Deterministic stub: echoes the goal, succeeds unless 'fail' present."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def run(self, agent_id: str, goal: str, *, metadata: dict | None = None) -> AgentResult:
        self.calls.append((agent_id, goal))
        failed = "fail" in goal
        return AgentResult(
            request_id=f"stub:{len(self.calls)}",
            status="FAILED" if failed else "SUCCEEDED",
            summary=f"stub:{agent_id}:{abs(hash(goal)) % 7}",
            evidence_refs=[],
            warnings=["injected failure"] if failed else [],
        )


PARTICIPANT_SETS = [
    ["urn:agents:a", "urn:agents:b"],
    ["urn:agents:a", "urn:agents:b", "urn:agents:c"],
]


@pytest.mark.parametrize("pattern_name", sorted(PATTERNS))
@pytest.mark.parametrize("participants", PARTICIPANT_SETS)
def test_pattern_coordinates_stub_agents(pattern_name, participants):
    runner = StubRunner()
    coordinator: Coordinator = PATTERNS[pattern_name](participants, runner, max_steps=8)
    outcome = coordinator.coordinate("analyse; report; confirm")
    assert outcome["pattern"] == pattern_name
    assert runner.calls, f"{pattern_name} never invoked participants"
    assert all(agent_id in participants for agent_id, _ in runner.calls)


def test_federated_policy_boundary():
    runner = StubRunner()
    coordinator = PATTERNS["federated"](
        ["urn:agents:a", "urn:agents:b"], runner,
        policy_tiers={"urn:agents:a": 0, "urn:agents:b": 2})
    outcome = coordinator.coordinate("task", metadata={"policy_tier": 1})
    assert outcome["denied_by_policy"] == ["urn:agents:b"]
    assert all(aid == "urn:agents:a" for aid, _ in runner.calls)


def test_market_picks_lowest_bid():
    runner = StubRunner()
    coordinator = PATTERNS["market-based"](
        ["urn:agents:a", "urn:agents:b"], runner, bid_hook=lambda aid: 0.1 if aid.endswith("b") else 9.9)
    outcome = coordinator.coordinate("task")
    assert outcome["winner"] == "urn:agents:b"
    assert len(runner.calls) == 1


# ---------------------------------------------------------------------------
# governed runtime integration
# ---------------------------------------------------------------------------

def test_agents_run_through_governed_runtime():
    from eoip.agents.runtime import AgentRegistry, AgentRuntime

    from eoip.agentarch.classical import ReactiveAgent
    from eoip.agentarch.reasoning import FormalReasoningAgent

    registry = AgentRegistry()
    registry.register(ReactiveAgent("urn:arch:test:reactive", rules=[("help", "assist")]))
    registry.register(FormalReasoningAgent("urn:arch:test:formal",
                                           invariants=[("ok", "count(*) >= 0")]))
    runtime = AgentRuntime(MemoryGraphStore(), registry)
    result = runtime.run(AgentRequest(
        request_id="arch-rt-1", agent_id="urn:arch:test:reactive",
        goal="help me", actor_id="tester"))
    assert result.status == "SUCCEEDED"
    trace = runtime.trace_store.get("arch-rt-1")
    assert trace is not None and trace.final_status == "SUCCEEDED"


def test_runtime_runner_for_org_patterns():
    from eoip.agents.runtime import AgentRegistry, AgentRuntime

    from eoip.agentarch.classical import ReactiveAgent

    registry = AgentRegistry()
    registry.register(ReactiveAgent("urn:arch:worker:1", rules=[("x", "y")]))
    registry.register(ReactiveAgent("urn:arch:worker:2", rules=[("x", "y")]))
    runtime = AgentRuntime(MemoryGraphStore(), registry)
    runner = OrgRunner(runtime, actor_id="coord-test")
    coordinator = PATTERNS["pipeline"](["urn:arch:worker:1", "urn:arch:worker:2"], runner)
    outcome = coordinator.coordinate("x task")
    assert outcome["status"] == "SUCCEEDED"


# ---------------------------------------------------------------------------
# (E) A2A layer
# ---------------------------------------------------------------------------

def test_a2a_envelope_round_trip():
    runner = StubRunner()
    bus = A2ABus(runner)
    bus.register(CapabilityCard(agent_id="urn:agents:a", capabilities=["analyse"]))
    bus.register(CapabilityCard(agent_id="urn:agents:b", capabilities=["report"]))

    message = A2AMessage(
        sender_id="urn:agents:a", recipient_id="urn:agents:b",
        message_type="TASK", content={"goal": "report on findings"},
        traceparent="00-" + "ab" * 16 + "-" + "cd" * 8 + "-01",
    )
    reply = bus.send(message)
    assert reply.message_type == "RESPONSE"
    assert reply.sender_id == "urn:agents:b"
    assert reply.causation_id == message.message_id
    assert reply.traceparent.split("-")[1] == message.traceparent.split("-")[1]
    assert "task_id" in reply.content


def test_a2a_capability_discovery_and_cancel():
    runner = StubRunner()
    bus = A2ABus(runner)
    bus.register(CapabilityCard(agent_id="urn:agents:a", capabilities=["analyse", "report"]))
    assert bus.find_agents("analyse") == ["urn:agents:a"]
    query = A2AMessage(sender_id="urn:agents:x", recipient_id="urn:agents:a",
                       message_type="CAPABILITY_QUERY", content={},
                       traceparent="00-" + "ef" * 16 + "-" + "01" * 8 + "-01")
    reply = bus.send(query)
    assert reply.content["card"]["agent_id"] == "urn:agents:a"

    cancel = A2AMessage(sender_id="urn:agents:x", recipient_id="urn:agents:a",
                        message_type="CANCEL", content={"task_id": "urn:eoip:a2a:task:t1"},
                        traceparent=query.traceparent)
    cancel_reply = bus.send(cancel)
    assert cancel_reply.content["cancelled"] is True
    assert "urn:eoip:a2a:task:t1" in bus._cancelled


def test_a2a_recursion_budget():
    runner = StubRunner()
    bus = A2ABus(runner, max_recursion=1)
    bus.register(CapabilityCard(agent_id="urn:agents:a", capabilities=["x"]))
    with pytest.raises(ValueError):
        bus.delegate("urn:agents:a", "goal", traceparent="00-" + "00" * 16 + "-" + "11" * 8 + "-01",
                     recursion_depth=2)


def test_a2a_unknown_recipient():
    bus = A2ABus(StubRunner())
    with pytest.raises(ValueError):
        bus.send(A2AMessage(sender_id="a", recipient_id="ghost", content={},
                            traceparent="00-" + "00" * 16 + "-" + "11" * 8 + "-01"))


# ---------------------------------------------------------------------------
# router
# ---------------------------------------------------------------------------

def test_router_catalog_and_routes():
    from eoip.agentarch.router import build_router

    router = build_router(MemoryGraphStore())
    routes = {(r.path, tuple(sorted(r.methods))) for r in router.routes}
    paths = {p for p, _ in routes}
    assert "/api/v1/agentarch/catalog" in paths
    assert "/api/v1/agentarch/run" in paths
    assert "/api/v1/agentarch/coordinate" in paths
    assert "/api/v1/agentarch/a2a/send" in paths
    assert any("/a2a/capabilities/" in p for p in paths)
