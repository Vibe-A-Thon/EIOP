"""Agent registry and runtime (FR-AGENT-003).

Read-only agents use allowlisted tools within execution budgets.
"""

from eoip.agents.anomaly import AnomalyDetectionAgent
from eoip.agents.blast_radius import BlastRadiusAgent
from eoip.agents.catalog import build_agent_registry
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
from eoip.agents.runtime import AgentRegistry, AgentRuntime
from eoip.agents.similarity import SimilarityAgent
from eoip.agents.test_coverage import TestCoverageAgent
from eoip.agents.trace_impact import TraceImpactAgent

__all__ = [
    "AgentRegistry",
    "AgentRuntime",
    "AnomalyDetectionAgent",
    "ArchitectureConformanceAgent",
    "BlastRadiusAgent",
    "ChangeImpactAgent",
    "CommunityAnalysisAgent",
    "ConnectorDiagnosisAgent",
    "DataQualityAgent",
    "DocumentationFreshnessAgent",
    "EvidenceVerificationAgent",
    "GraphInvestigatorAgent",
    "IncidentCorrelationAgent",
    "IncidentInvestigationAgent",
    "KnowledgeCuratorAgent",
    "OntologyReviewAgent",
    "QueryOptimizationAgent",
    "SimilarityAgent",
    "TestCoverageAgent",
    "TraceImpactAgent",
    "build_agent_registry",
]
