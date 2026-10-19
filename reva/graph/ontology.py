"""Normative graph ontology, vertex/edge labels, and property schemas (T-119 / §6.10 / C-03 / C-04)."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Set
from pydantic import BaseModel, Field


class VertexLabel(str, Enum):
    REPOSITORY = "Repository"
    COMMIT = "Commit"
    ARTIFACT = "Artifact"
    SOURCE_FILE = "SourceFile"
    MODULE = "Module"
    FUNCTION = "Function"
    CLASS = "Class"
    API_ENDPOINT = "ApiEndpoint"
    DATABASE_SCHEMA = "DatabaseSchema"
    DATABASE_TABLE = "DatabaseTable"
    SERVICE_INSTANCE = "ServiceInstance"
    OBLIGATION = "Obligation"
    VERIFIER = "Verifier"
    WARRANT = "Warrant"
    ENTITY = "Entity"


class EdgeLabel(str, Enum):
    CONTAINS = "CONTAINS"
    DEPENDS_ON = "DEPENDS_ON"
    DEFINES = "DEFINES"
    CALLS = "CALLS"
    EXPOSES = "EXPOSES"
    READS_FROM = "READS_FROM"
    WRITES_TO = "WRITES_TO"
    ATTESTED_BY = "ATTESTED_BY"
    SUPERSEDES = "SUPERSEDES"
    DERIVED_FROM = "DERIVED_FROM"
    IMPLEMENTS = "IMPLEMENTS"


class GraphVertex(BaseModel):
    id: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    label: str
    from_id: str
    to_id: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphMutation(BaseModel):
    action: str = "upsert"  # upsert | delete
    vertices: List[GraphVertex] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)
