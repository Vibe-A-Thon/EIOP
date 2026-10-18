"""EOIP versioned data contracts and governed agent execution models."""

from eoip.contracts.agent import (
    AgentBudgets,
    AgentContract,
    AgentExecutionTrace,
    AgentRequest,
    AgentResult,
    ChangeProposal,
    ExplanationEnvelope,
)
from eoip.contracts.audit import AuditEvent
from eoip.contracts.evidence import Evidence
from eoip.contracts.graph_mutation import GraphMutation
from eoip.contracts.graph_result import GraphEdge, GraphNode, GraphPath, GraphResult
from eoip.contracts.memory import MemoryRecord
from eoip.contracts.normalized import NormalizedEntity, NormalizedRelationship
from eoip.contracts.query_plan import QueryPlan
from eoip.contracts.retrieval import RetrievalResult
from eoip.contracts.revision import GraphRevision, RelationshipRevision, RevisionMetadata
from eoip.contracts.source_event import PermissionMetadata, SourceEvent, SourceEventV2, upgrade_source_event
from eoip.contracts.source_registry import SourceCapabilities, SourceCheckpoint, SourceRegistryEntry
from eoip.contracts.tool import ToolContract, ToolRequest, ToolResult
from eoip.contracts.canonical import (
    PrincipalType,
    TrustedScope,
    TermKind,
    RDFTerm,
    EvidenceLocator,
    KnowledgeState,
    CanonicalAssertion,
    ActionStatus,
    ActionIntent,
    ProducerClass,
    ModelLineage,
    AgreementState,
    DualPathResult,
    ContextManifest,
)

__all__ = [
    "AgentBudgets",
    "AgentContract",
    "AgentExecutionTrace",
    "AgentRequest",
    "AgentResult",
    "AuditEvent",
    "ChangeProposal",
    "Evidence",
    "ExplanationEnvelope",
    "GraphEdge",
    "GraphMutation",
    "GraphNode",
    "GraphPath",
    "GraphResult",
    "GraphRevision",
    "MemoryRecord",
    "NormalizedEntity",
    "NormalizedRelationship",
    "PermissionMetadata",
    "QueryPlan",
    "RelationshipRevision",
    "RetrievalResult",
    "RevisionMetadata",
    "SourceCapabilities",
    "SourceCheckpoint",
    "SourceEvent",
    "SourceEventV2",
    "SourceRegistryEntry",
    "ToolContract",
    "ToolRequest",
    "ToolResult",
    "upgrade_source_event",
]
