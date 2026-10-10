"""
Enterprise Ontology & Intelligence Platform (EOIP / KnowGridFlow).

Top-level enterprise interface providing cognitive architectures, multi-loop
orchestration, polyglot query transpilation, 55-database integration, and
living brain algorithms.
"""

__version__ = "1.0.0-rc.1"

from eoip.brain.brain_os import BrainOSKernel
from eoip.brain.living_brain_algorithms import LivingBrainEngine, LivingBrainAlgorithms
from eoip.agents.loops import (
    LoopType,
    HumanControlPattern,
    AutonomousExecutionLoop,
    ExecutionLimits,
    LoopExecutionRecord,
    EnterpriseLoopManager,
)
from eoip.agents.archetypes import AgentFactory, BaseAgent, A2AProtocolBroker
from eoip.retrieval.rag_suite import EnterpriseRAGSuite, RAGMode, RAGResult
from eoip.query.polyglot_engine import (
    PolyglotQueryEngine,
    QueryDialect,
    TranspiledPlan,
    QueryExecutionResult,
)
from eoip.graph.database_adapters import (
    DatabaseAdapterRegistry,
    BaseDatabaseAdapter,
    DatabaseType,
)
from eoip.models.self_llm import (
    SelfLLMEngine,
    CognitiveTier,
    GenerationConfig,
    GenerationResult,
    XAIExplanation,
    get_self_llm_engine,
)
from eoip.brain.learning_engine import CognitiveLearningEngine, LearningParadigm
from eoip.brain.report_generator import DetailedReportGenerator, QueryApproach, BrainReport
from eoip.brain.cognitive_narrator import (
    CognitiveNarrator,
    CognitiveNarration,
    EnhancedQuery,
    ComplementaryQuestion,
)


__all__ = [
    "__version__",
    "BrainOSKernel",
    "LivingBrainEngine",
    "LivingBrainAlgorithms",
    "LoopType",
    "HumanControlPattern",
    "AutonomousExecutionLoop",
    "ExecutionLimits",
    "LoopExecutionRecord",
    "EnterpriseLoopManager",
    "AgentFactory",
    "BaseAgent",
    "A2AProtocolBroker",
    "EnterpriseRAGSuite",
    "RAGMode",
    "RAGResult",
    "PolyglotQueryEngine",
    "QueryDialect",
    "TranspiledPlan",
    "QueryExecutionResult",
    "DatabaseAdapterRegistry",
    "BaseDatabaseAdapter",
    "DatabaseType",
    "SelfLLMEngine",
    "CognitiveTier",
    "GenerationConfig",
    "GenerationResult",
    "XAIExplanation",
    "get_self_llm_engine",
    "CognitiveLearningEngine",
    "LearningParadigm",
    "DetailedReportGenerator",
    "QueryApproach",
    "BrainReport",
    "CognitiveNarrator",
    "CognitiveNarration",
    "EnhancedQuery",
    "ComplementaryQuestion",
]


