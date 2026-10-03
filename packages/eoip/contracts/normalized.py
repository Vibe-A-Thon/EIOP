"""NormalizedEntity v1 and NormalizedRelationship v1.

Normative: schemas/normalized_entity.schema.json,
schemas/normalized_relationship.schema.json
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CreationStatus = Literal["DETERMINISTIC", "INFERRED", "AMBIGUOUS", "MANUAL", "HUMAN_CONFIRMED"]


class NormalizedEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    canonical_id: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    graph_domain: str = Field(min_length=1)
    source_refs: list[str]
    creation_status: CreationStatus | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0, strict=True)
    properties: dict


class NormalizedRelationship(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    relationship_id: str = Field(min_length=1)
    relationship_type: str = Field(min_length=1)
    from_id: str = Field(min_length=1)
    to_id: str = Field(min_length=1)
    evidence_refs: list[str]
    creation_status: CreationStatus
    confidence: float | None = Field(default=None, ge=0.0, le=1.0, strict=True)
    properties: dict | None = None
