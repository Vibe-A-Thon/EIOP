"""Typed records matching the canonical IP Warrant 1.0 JSON Schema."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WarrantStatus(str, Enum):
    OBSERVED = "OBSERVED"
    ATTESTED = "ATTESTED"
    PREDICTED = "PREDICTED"
    GENERATED = "GENERATED"
    HEARSAY = "HEARSAY"
    UNKNOWN = "UNKNOWN"


class WarrantSubjectKind(str, Enum):
    PROPOSITION = "proposition"
    ASSERTION = "assertion"
    ACTION = "action"
    ANSWER = "answer"


class WarrantGroundKind(str, Enum):
    GRAPH_NODE = "graph_node"
    GRAPH_EDGE = "graph_edge"
    GRAPH_PROPERTY = "graph_property"
    SOURCE_RECORD = "source_record"
    DOC_SPAN = "doc_span"
    TOOL_RECEIPT = "tool_receipt"
    ATTESTATION = "attestation"
    MODEL_RUN = "model_run"
    RULE = "rule"


class WarrantActionClass(str, Enum):
    READ_ONLY = "READ_ONLY"
    ADVISORY = "ADVISORY"
    INTERNAL_WRITE = "INTERNAL_WRITE"
    EXTERNAL_WRITE = "EXTERNAL_WRITE"
    IRREVERSIBLE = "IRREVERSIBLE"


class WarrantOperatorClass(str, Enum):
    OBSERVER = "OBSERVER"
    COMPUTATION = "COMPUTATION"
    MODEL = "MODEL"
    GENERATOR = "GENERATOR"
    HUMAN = "HUMAN"


class _SchemaModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class WarrantSubject(_SchemaModel):
    kind: WarrantSubjectKind
    ref: str
    text: str | None = Field(default=None, max_length=4000)
    hash: str | None = None


class WarrantGroundSpan(_SchemaModel):
    start: int | None = None
    end: int | None = None


class WarrantGround(_SchemaModel):
    kind: WarrantGroundKind
    id: str
    version: str | None = None
    span: WarrantGroundSpan | None = None
    hash: str | None = None


class WarrantValidity(_SchemaModel):
    valid_from: datetime
    valid_to: datetime | None = None
    lease_ids: list[str] = Field(default_factory=list)

    @field_validator("valid_from", "valid_to")
    @classmethod
    def require_aware_times(cls, value: datetime | None) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("Warrant validity timestamps must include a timezone")
        return value


class WarrantScope(_SchemaModel):
    action: str
    resource_type: str
    selector: str


class WarrantAuthority(_SchemaModel):
    principal_id: str
    scopes: list[WarrantScope]
    delegation_chain: list[str]


class WarrantConsequence(_SchemaModel):
    kappa: float = Field(ge=0)
    impact_run_id: str | None = None
    action_class: WarrantActionClass | None = None


class WarrantOperator(_SchemaModel):
    operator_id: str
    class_: WarrantOperatorClass = Field(alias="class")
    version: str


class Warrant(_SchemaModel):
    warrant_id: UUID
    tenant_id: str
    subject: WarrantSubject
    grounds: list[WarrantGround]
    status: WarrantStatus
    validity: WarrantValidity
    authority: WarrantAuthority
    consequence: WarrantConsequence
    operator: WarrantOperator
    parents: list[UUID]
    created_at: datetime
    schema_version: Literal["1.0"]
    confidence: float | None = Field(default=None, ge=0, le=1)
    signature: str | None = None

    @field_validator("created_at")
    @classmethod
    def require_aware_creation_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Warrant created_at must include a timezone")
        return value

    def to_schema_dict(self) -> dict[str, Any]:
        """Serialize by aliases and omit absent optional properties per schema."""

        return self.model_dump(mode="json", by_alias=True, exclude_none=True)