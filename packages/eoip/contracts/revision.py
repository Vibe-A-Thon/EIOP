"""Canonical temporal revision contracts (G2-T0003, G2-EVOL-009)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RevisionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revision_id: str = Field(min_length=1, max_length=512)
    valid_from: str
    valid_to: str | None = None
    observed_at: str
    is_current: bool = True
    previous_revision: str | None = Field(default=None, max_length=512)
    source_version: str | None = Field(default=None, max_length=512)

    @model_validator(mode="after")
    def validate_validity_window(self) -> RevisionMetadata:
        if self.is_current and self.valid_to is not None:
            raise ValueError("a current revision cannot have valid_to")
        if not self.is_current and self.valid_to is None:
            raise ValueError("a historical revision requires valid_to")
        if self.previous_revision == self.revision_id:
            raise ValueError("previous_revision cannot refer to the same revision")
        return self


class GraphRevision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    canonical_id: str = Field(min_length=1, max_length=2048)
    entity_type: str = Field(min_length=1, max_length=128)
    revision: RevisionMetadata
    properties: dict[str, Any]
    source_event_id: str = Field(min_length=1, max_length=512)


class RelationshipRevision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    relationship_id: str = Field(min_length=1, max_length=2048)
    relationship_type: str = Field(min_length=1, max_length=128)
    from_id: str = Field(min_length=1, max_length=2048)
    to_id: str = Field(min_length=1, max_length=2048)
    revision: RevisionMetadata
    properties: dict[str, Any] = Field(default_factory=dict)
    evidence_refs: list[str] = Field(default_factory=list)
    source_event_id: str = Field(min_length=1, max_length=512)
