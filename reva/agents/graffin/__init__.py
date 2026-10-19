"""
Living AI Agent Worker 'Graffin' (GRF-REQ-*, GRF-PLAN-v1).
Autonomous, self-healing, epistemically-grounded knowledge curation agent.
"""

from reva.agents.graffin.constitution import ConstitutionVerifier, ConstitutionTamperedError
from reva.agents.graffin.kill_switch import KillSwitchController
from reva.agents.graffin.autonomy import AutonomyStateMachine, AutonomyLevel, ConsequenceBudget, RiskTier
from reva.agents.graffin.evaluators import CalibrationJudge, RegressionSentinel
from reva.agents.graffin.doctor import GraffinDoctorDaemon, GraphHealthAudit
from reva.agents.graffin.curator import GraffinCurator, KnowledgeGapItem, QuarantinedContradiction
from reva.agents.graffin.worker import GraffinLifecycleWorker, CurationCycleReport

__all__ = [
    "ConstitutionVerifier",
    "ConstitutionTamperedError",
    "KillSwitchController",
    "AutonomyStateMachine",
    "AutonomyLevel",
    "ConsequenceBudget",
    "RiskTier",
    "CalibrationJudge",
    "RegressionSentinel",
    "GraffinDoctorDaemon",
    "GraphHealthAudit",
    "GraffinCurator",
    "KnowledgeGapItem",
    "QuarantinedContradiction",
    "GraffinLifecycleWorker",
    "CurationCycleReport",
]
