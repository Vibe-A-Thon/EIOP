"""EOIP versioned data contracts (Pydantic models mirroring schemas/*.schema.json v1.0)."""

from eoip.contracts.agent import AgentRequest, AgentResult
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
from eoip.contracts.tool import ToolRequest, ToolResult

__all__ = [
    "AgentRequest",
    "AgentResult",
    "AuditEvent",
    "Evidence",
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
    "ToolRequest",
    "ToolResult",
    "upgrade_source_event",
]
