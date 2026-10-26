"""HTTP surface for agent architectures (wired by apps/api; not here).

Routes under ``/api/v1/agentarch``:

* ``GET  /api/v1/agentarch/catalog``        — architecture class inventory
* ``POST /api/v1/agentarch/run``            — run one architecture class
* ``POST /api/v1/agentarch/coordinate``     — run an orchestration pattern
* ``POST /api/v1/agentarch/a2a/send``       — A2A envelope round-trip
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from eoip.agentarch.a2a import A2ABus, A2AMessage, CapabilityCard, new_traceparent
from eoip.agentarch.base import URN_PREFIX
from eoip.agentarch.org import PATTERNS, RuntimeRunner
from eoip.agents.runtime import AgentRegistry, AgentRuntime


def architecture_catalog() -> dict[str, list[str]]:
    from eoip.agentarch.classical import (
        BDIAgent, BayesianAgent, CausalReasoningAgent, DeliberativeAgent,
        EmbodiedAgent, HybridAgent, KnowledgeBasedAgent, LearningAgent,
        MPCAgent, MetaReasoningAgent, MultimodalAgent, NeuroSymbolicAgent,
        ProbabilisticAgent, RLAgent, ReactiveAgent, StatefulAgent,
        StatelessAgent, WorldModelAgent,
    )
    from eoip.agentarch.enterprise import (
        AuditAgent, BenchmarkingAgent, CodeEngineeringAgent, ConnectorAgent,
        ContextManagementAgent, CostOptimizationAgent, CrawlerAgent,
        DebuggingAgent, DeploymentAgent, DiscoveryAgent, DocumentationAgent,
        EntityResolutionAgent, EvaluatorAgent, EvidenceProvenanceAgent,
        GraphValidationAgent, HumanEscalationAgent, IngestionAgent,
        KGBuilderAgent, MemoryManagementAgent, ModelSelectionAgent,
        OntologyAgent, PolicyEnforcementAgent, QueryTranslationAgent,
        RecoveryAgent, RiskAssessmentAgent, SecurityMonitoringAgent,
        TestingAgent,
    )
    from eoip.agentarch.reasoning import (
        ArbitrationAgent, CounterfactualAgent, DebateAgent,
        FormalReasoningAgent, GraphOfThoughtAgent, HypothesisTestingAgent,
        MCTSAgent, PlanAndExecuteAgent, ReActAgent, ReplanningAgent,
        ReflexionAgent, SearchBasedAgent, SimulationAgent,
        TreeOfThoughtAgent, VerificationAgent,
    )

    classical = [cls.architecture for cls in (
        LearningAgent, KnowledgeBasedAgent, BDIAgent, ReactiveAgent,
        DeliberativeAgent, HybridAgent, StatefulAgent, StatelessAgent,
        ProbabilisticAgent, BayesianAgent, RLAgent, NeuroSymbolicAgent,
        WorldModelAgent, CausalReasoningAgent, MetaReasoningAgent,
        EmbodiedAgent, MultimodalAgent, MPCAgent,
    )]
    reasoning = [cls.architecture for cls in (
        ReActAgent, PlanAndExecuteAgent, TreeOfThoughtAgent,
        GraphOfThoughtAgent, SearchBasedAgent, MCTSAgent, ReplanningAgent,
        ReflexionAgent, HypothesisTestingAgent, SimulationAgent,
        CounterfactualAgent, DebateAgent, ArbitrationAgent,
        VerificationAgent, FormalReasoningAgent,
    )]
    enterprise = [cls.capability for cls in (
        DiscoveryAgent, ConnectorAgent, CrawlerAgent, IngestionAgent,
        EntityResolutionAgent, KGBuilderAgent, GraphValidationAgent,
        OntologyAgent, QueryTranslationAgent, EvidenceProvenanceAgent,
        MemoryManagementAgent, ContextManagementAgent, ModelSelectionAgent,
        CostOptimizationAgent, SecurityMonitoringAgent,
        PolicyEnforcementAgent, RiskAssessmentAgent, AuditAgent,
        HumanEscalationAgent, RecoveryAgent, BenchmarkingAgent,
        EvaluatorAgent, CodeEngineeringAgent, TestingAgent, DebuggingAgent,
        DeploymentAgent, DocumentationAgent,
    )]
    return {"classical": classical, "reasoning": reasoning,
            "enterprise": enterprise, "patterns": sorted(PATTERNS)}


def _default_runtime(store) -> AgentRuntime:
    registry = AgentRegistry()
    from eoip.agentarch.classical import ReactiveAgent
    from eoip.agentarch.reasoning import ReActAgent
    from eoip.agentarch.enterprise import DiscoveryAgent, OntologyAgent

    for agent in (
        ReactiveAgent(f"{URN_PREFIX}:reactive"),
        ReActAgent(f"{URN_PREFIX}:react"),
        DiscoveryAgent(f"{URN_PREFIX}:discovery"),
        OntologyAgent(f"{URN_PREFIX}:ontology"),
    ):
        registry.register(agent)
    return AgentRuntime(store, registry)


class ArchRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    actor_id: str = "api"
    metadata: dict[str, Any] = Field(default_factory=dict)


class CoordinateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pattern: str = Field(min_length=1)
    participants: list[str] = Field(min_length=1, max_length=12)
    goal: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


def build_router(store, runtime: AgentRuntime | None = None):
    """Construct the FastAPI router (lazy import, apps/api calls this)."""
    from fastapi import APIRouter, HTTPException

    router = APIRouter(prefix="/api/v1/agentarch", tags=["agentarch"])
    rt = runtime or _default_runtime(store)
    runner = RuntimeRunner(rt, actor_id="agentarch-api")
    bus = A2ABus(runner)
    for agent_id in rt.registry.list_agents():
        card = rt.registry.get_contract(agent_id)
        if card is not None:
            bus.register(CapabilityCard(
                agent_id=agent_id, capabilities=list(card.capabilities),
                budgets=card.budgets.model_dump(),
            ))

    @router.get("/catalog")
    def catalog() -> dict[str, Any]:
        return architecture_catalog()

    @router.post("/run")
    def run_arch(body: ArchRunRequest) -> dict[str, Any]:
        from eoip.contracts.agent import AgentRequest

        result = rt.run(AgentRequest(
            request_id=f"api:agentarch:{body.agent_id}",
            agent_id=body.agent_id, goal=body.goal, actor_id=body.actor_id,
            correlation_id=f"api:agentarch", metadata=body.metadata,
        ))
        return result.model_dump()

    @router.post("/coordinate")
    def coordinate(body: CoordinateRequest) -> dict[str, Any]:
        pattern = PATTERNS.get(body.pattern)
        if pattern is None:
            raise HTTPException(status_code=404, detail=f"Unknown pattern: {body.pattern}")
        coordinator = pattern(body.participants, runner)
        return coordinator.coordinate(body.goal, metadata=body.metadata)

    @router.post("/a2a/send")
    def a2a_send(message: A2AMessage) -> dict[str, Any]:
        try:
            reply = bus.send(message)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        return reply.model_dump()

    @router.get("/a2a/capabilities/{agent_id}")
    def a2a_capabilities(agent_id: str) -> dict[str, Any]:
        card = bus.capabilities(agent_id)
        if card is None:
            raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_id}")
        return card.model_dump()

    return router


__all__ = ["build_router", "architecture_catalog"]
