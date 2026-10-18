"""AI package — neuro-symbolic arbitration, dual-path semantics, and boundary governance."""

from eoip.ai.boundary import (
    ConstraintViolationError,
    DualPathOrchestrator,
    ProposalEvaluation,
    create_probabilistic_proposal,
    export_trig_quads,
    filter_asserted_only,
    validate_and_promote_proposal,
)
from eoip.ai.graphrag import (
    ContextManifest,
    EgressDLPFilter,
    EgressPolicyViolationError,
    GraphRAGPipeline,
    GroundedAnswer,
    ModelManifest,
    ModelUnqualifiedError,
    PromptInjectionFence,
)

__all__ = [
    "ConstraintViolationError",
    "DualPathOrchestrator",
    "ProposalEvaluation",
    "create_probabilistic_proposal",
    "export_trig_quads",
    "filter_asserted_only",
    "validate_and_promote_proposal",
    "ContextManifest",
    "EgressDLPFilter",
    "EgressPolicyViolationError",
    "GraphRAGPipeline",
    "GroundedAnswer",
    "ModelManifest",
    "ModelUnqualifiedError",
    "PromptInjectionFence",
]

