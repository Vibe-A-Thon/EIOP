"""Production agent catalog and validated contracts."""

from __future__ import annotations

from eoip.agents.anomaly import AnomalyDetectionAgent
from eoip.agents.blast_radius import BlastRadiusAgent
from eoip.agents.community import CommunityAnalysisAgent
from eoip.agents.governed import (
    ArchitectureConformanceAgent,
    ChangeImpactAgent,
    ConnectorDiagnosisAgent,
    DataQualityAgent,
    DocumentationFreshnessAgent,
    EvidenceVerificationAgent,
    GraphInvestigatorAgent,
    IncidentInvestigationAgent,
    KnowledgeCuratorAgent,
    OntologyReviewAgent,
    QueryOptimizationAgent,
)
from eoip.agents.incident_correlation import IncidentCorrelationAgent
from eoip.agents.runtime import AgentRegistry
from eoip.agents.similarity import SimilarityAgent
from eoip.agents.test_coverage import TestCoverageAgent
from eoip.agents.trace_impact import TraceImpactAgent
from eoip.contracts.agent import AgentBudgets, AgentContract


def _contract(
    agent,
    purpose: str,
    *,
    agent_type: str = "TASK",
    risk_level: str = "R0",
    human_control: str = "READ_ONLY",
    model_policy: str = "deterministic",
) -> AgentContract:
    return AgentContract(
        agent_id=agent.agent_id,
        version="1.0.0",
        agent_type=agent_type,
        purpose=purpose,
        capabilities=[agent.agent_id],
        allowed_tools=sorted(agent.allowed_tools),
        prohibited_tools=["write_graph", "delete_graph", "deploy", "send_message"],
        model_policy=model_policy,
        risk_level=risk_level,
        human_control=human_control,
        budgets=AgentBudgets(max_steps=agent.max_steps, max_seconds=agent.max_seconds),
    )


def build_agent_registry(trace_impact_config: dict | None = None) -> AgentRegistry:
    registry = AgentRegistry()
    entries = [
        (TraceImpactAgent(trace_impact_config), "Trace entity impact with bounded evidence paths", "GOAL_BASED"),
        (ChangeImpactAgent(), "Assess the blast radius of a proposed or observed change", "GOAL_BASED"),
        (IncidentInvestigationAgent(), "Correlate incidents with changes, deployments, and evidence", "MODEL_BASED"),
        (IncidentCorrelationAgent(), "Find incident correlation chains", "MODEL_BASED"),
        (DataQualityAgent(), "Measure identity, completeness, and provenance quality", "VALIDATOR"),
        (OntologyReviewAgent(), "Review graph facts against the governed ontology", "REVIEWER"),
        (ConnectorDiagnosisAgent(), "Diagnose connector and ingestion run failures", "MODEL_BASED"),
        (DocumentationFreshnessAgent(), "Detect stale or disconnected documentation", "VALIDATOR"),
        (EvidenceVerificationAgent(), "Verify claims have source-backed evidence", "VALIDATOR"),
        (
            GraphInvestigatorAgent(),
            "Answer graph questions with optional grounded local-model synthesis",
            "RAG",
        ),
        (ArchitectureConformanceAgent(), "Check dependencies against architecture governance", "REVIEWER"),
        (QueryOptimizationAgent(), "Recommend bounded query focus from graph cardinality", "UTILITY_BASED"),
        (AnomalyDetectionAgent(), "Detect structural graph anomalies", "MODEL_BASED"),
        (BlastRadiusAgent(), "Rank the downstream blast radius of an entity", "GOAL_BASED"),
        (CommunityAnalysisAgent(), "Identify graph communities and boundaries", "MODEL_BASED"),
        (SimilarityAgent(), "Find structurally similar knowledge entities", "MODEL_BASED"),
        (TestCoverageAgent(), "Find requirements and work items without test coverage", "VALIDATOR"),
    ]
    for agent, purpose, agent_type in entries:
        registry.register(agent, _contract(
            agent,
            purpose,
            agent_type=agent_type,
            model_policy="optional_local_grounded" if agent.agent_id == "GraphInvestigator" else "deterministic",
        ))

    curator = KnowledgeCuratorAgent()
    registry.register(curator, _contract(
        curator,
        "Propose evidence-backed knowledge remediation for human approval",
        agent_type="WRITING",
        risk_level="R2",
        human_control="PROPOSE_ONLY",
    ))
    return registry
