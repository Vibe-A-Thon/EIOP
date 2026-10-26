"""§7 Reasoning & Orchestration infrastructure.

Submodules:

* :mod:`eoip.reasoning.strategies`  — §7 reasoning architectures registry.
* :mod:`eoip.reasoning.memory`      — §7 memory architectures.
* :mod:`eoip.reasoning.evaluation`  — §7 agent evaluation framework.
* :mod:`eoip.reasoning.agentops`    — §7 AgentOps (tracing, cost, SLA).
* :mod:`eoip.reasoning.router`      — ``build_router()`` HTTP surface.
"""

from eoip.reasoning.agentops import (
    CostLedger,
    DeploymentDescriptor,
    IncidentRecord,
    IncidentStore,
    RunTrace,
    RunTracer,
    SLAPolicy,
    SLATracker,
    validate_deployment,
)
from eoip.reasoning.evaluation import (
    AdversarialSuiteReport,
    AdversarialTestSuite,
    BenchmarkReport,
    BenchmarkRunner,
    BusinessOutcomeMetrics,
    BusinessOutcomeTracker,
    GoldenTask,
    Trajectory,
    TrajectoryScorer,
    TrajectoryScores,
    score_step_efficiency,
    score_tool_use,
)
from eoip.reasoning.memory import (
    EpisodicMemory,
    HierarchicalMemory,
    ProceduralMemory,
    SemanticMemory,
    SharedMemory,
    TemporalMemory,
    WorkingMemory,
    estimate_tokens,
)
from eoip.reasoning.strategies import (
    ReasoningHooks,
    ReasoningProblem,
    ReasoningResult,
    ReasoningStep,
    StrategyRegistry,
    default_registry,
)

__all__ = [
    "AdversarialSuiteReport",
    "AdversarialTestSuite",
    "BenchmarkReport",
    "BenchmarkRunner",
    "BusinessOutcomeMetrics",
    "BusinessOutcomeTracker",
    "CostLedger",
    "DeploymentDescriptor",
    "EpisodicMemory",
    "GoldenTask",
    "HierarchicalMemory",
    "IncidentRecord",
    "IncidentStore",
    "ProceduralMemory",
    "ReasoningHooks",
    "ReasoningProblem",
    "ReasoningResult",
    "ReasoningStep",
    "RunTrace",
    "RunTracer",
    "SLAPolicy",
    "SLATracker",
    "SemanticMemory",
    "SharedMemory",
    "StrategyRegistry",
    "TemporalMemory",
    "Trajectory",
    "TrajectoryScorer",
    "TrajectoryScores",
    "WorkingMemory",
    "default_registry",
    "estimate_tokens",
    "score_step_efficiency",
    "score_tool_use",
    "validate_deployment",
]
