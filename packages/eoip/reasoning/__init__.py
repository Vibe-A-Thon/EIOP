"""§7 Reasoning & Orchestration infrastructure.

Submodules:

* :mod:`eoip.reasoning.strategies`  — §7 reasoning architectures registry.
* :mod:`eoip.reasoning.memory`      — §7 memory architectures.
* :mod:`eoip.reasoning.evaluation`  — §7 agent evaluation framework.
* :mod:`eoip.reasoning.agentops`    — §7 AgentOps (tracing, cost, SLA).
* :mod:`eoip.reasoning.router`      — ``build_router()`` HTTP surface.
"""

from eoip.reasoning.strategies import (
    ReasoningHooks,
    ReasoningProblem,
    ReasoningResult,
    ReasoningStep,
    StrategyRegistry,
    default_registry,
)
from eoip.reasoning.memory import (
    EpisodicMemory,
    HierarchicalMemory,
    ProceduralMemory,
    SemanticMemory,
    SharedMemory,
    TemporalMemory,
    WorkingMemory,
)
from eoip.reasoning.evaluation import (
    AdversarialTestSuite,
    BenchmarkRunner,
    BusinessOutcomeTracker,
    GoldenTask,
    Trajectory,
    TrajectoryScorer,
)
from eoip.reasoning.agentops import (
    CostLedger,
    DeploymentDescriptor,
    IncidentStore,
    RunTracer,
    SLAPolicy,
    SLATracker,
)

__all__ = [name for name in dir() if not name.startswith("_")]
