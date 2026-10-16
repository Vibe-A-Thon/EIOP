"""GraphResult v1 — shared query response envelope.

Normative: EOIP-engg-doc-pkg/schemas/graph_result.schema.json
Consumed identically by UI, GraphRAG, MCP and Agent (FR-QUERY-007).
"""

from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str  # canonical_id
    label: str  # vertex label / entity_type
    domain: str | None = None
    properties: dict = {}


class GraphEdge(BaseModel):
    id: str  # relationship_id / edge key
    type: str  # edge label
    from_id: str
    to_id: str
    creation_status: str | None = None
    properties: dict = {}


class GraphPath(BaseModel):
    """Ordered vertex/edge sequence (FR-QUERY-002)."""

    path_id: str
    node_ids: list[str]
    edge_ids: list[str]


class GraphResult(BaseModel):
    query_id: str
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    paths: list[GraphPath] = []
    evidence: list[dict] = []
    partial: bool
    warnings: list[str] = []


class TraversalGraphResult(GraphResult):
    """GraphResult plus executor-computed traversal metadata.

    `meta.impact_rationale` maps each impacted canonical_id to a deterministic
    'why included' string (FR-QUERY-003). Extension only: every GraphResult v1
    field is preserved and `meta` is optional, so this remains wire-compatible
    with the published graph_result.schema.json envelope.
    """

    meta: dict | None = None
