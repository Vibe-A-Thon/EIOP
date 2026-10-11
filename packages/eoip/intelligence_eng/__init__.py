"""Intelligence Engineering — System-Level Autonomy.

The holistic discipline that designs and orchestrates the entire cognitive
stack: combining prompt layers, dynamic context engineering, memory
architectures, tool-use loops, multi-agent orchestration, and all 15+
engineering disciplines into a unified autonomous pipeline.

This is the meta-orchestrator — given a task, it decides which disciplines
to activate, at what autonomy level, in what order, and how to fuse their
outputs into a coherent cognitive response.
"""

from eoip.intelligence_eng.engine import (
    AutonomyLevel,
    CapabilityManifest,
    CognitivePlan,
    CognitivePlanStep,
    DisciplineActivation,
    IntelligenceEngine,
    TaskAnalysis,
    TaskComplexity,
    get_intelligence_engine,
)

__all__ = [
    "AutonomyLevel",
    "CapabilityManifest",
    "CognitivePlan",
    "CognitivePlanStep",
    "DisciplineActivation",
    "IntelligenceEngine",
    "TaskAnalysis",
    "TaskComplexity",
    "get_intelligence_engine",
]
