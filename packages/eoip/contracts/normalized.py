"""NormalizedEntity v1 and NormalizedRelationship v1.

Normative: EOIP-engg-doc-pkg/schemas/normalized_entity.schema.json,
EOIP-engg-doc-pkg/schemas/normalized_relationship.schema.json
"""

from typing import Literal

from pydantic import BaseModel, Field

CreationStatus = Literal["DETERMINISTIC", "INFERRED", "AMBIGUOUS", "MANUAL", "HUMAN_CONFIRMED"]


class NormalizedEntity(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    canonical_id: str
    entity_type: str
    graph_domain: str
    source_refs: list[str]
    creation_status: CreationStatus | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    properties: dict


class NormalizedRelationship(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    relationship_id: str
    relationship_type: str
    from_id: str
    to_id: str
    evidence_refs: list[str]
    creation_status: CreationStatus
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    properties: dict | None = None
