"""Normative warrant models and serialization (T-104 / REVA-WK-003 / §6.3–§6.6)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator

from reva.core.ids import is_valid_id, normalize_set, warrant_id
from reva.core.time import parse_ts
from reva.kernel.authority import Authority, ConfidenceBand, Epistemic
from reva.kernel.coverage import Coverage


# --- Subjects (§6.4.1) ---
class ArtifactSubject(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["artifact"] = "artifact"
    artifact_id: str
    sha256: str
    size_bytes: int = Field(ge=0)
    media_type: str
    format: str


class SourceRecordSubject(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["source_record"] = "source_record"
    system_type: str
    system_instance_id: str
    record_type: str
    record_key: str
    record_version: str


class GraphEntitySubject(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["graph_entity"] = "graph_entity"
    entity_id: str
    entity_type: str
    version_id: Optional[str] = None


class RuntimeInstanceSubject(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["runtime_instance"] = "runtime_instance"
    environment_id: str
    instance_key: str
    capture_id: str


class NoneSubject(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["none"] = "none"
    reason: str


Subject = Union[
    ArtifactSubject,
    SourceRecordSubject,
    GraphEntitySubject,
    RuntimeInstanceSubject,
    NoneSubject,
]


# --- Locations (§6.4.2) ---
class ArtifactRangeLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["artifact_range"] = "artifact_range"
    artifact_id: str
    offset: int = Field(ge=0)
    length: int = Field(ge=0)


class ArchiveMemberLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["archive_member"] = "archive_member"
    artifact_id: str
    member_path: str
    member_sha256: str


class SourceSpanLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["source_span"] = "source_span"
    repo_id: str
    commit: str
    path: str
    start_line: int = Field(ge=1)
    start_col: int = Field(ge=0)
    end_line: int = Field(ge=1)
    end_col: int = Field(ge=0)


class RecordFieldLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["record_field"] = "record_field"
    system_instance_id: str
    record_key: str
    json_pointer: str


class UrlLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["url"] = "url"
    url: str
    method: Optional[str] = None


class RuntimeLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["runtime"] = "runtime"
    environment_id: str
    service: str
    instance: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    at: str


class LogLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["log"] = "log"
    stream: str
    cursor: str
    at: str


class GraphLocation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    kind: Literal["graph"] = "graph"
    entity_id: str


Location = Union[
    ArtifactRangeLocation,
    ArchiveMemberLocation,
    SourceSpanLocation,
    RecordFieldLocation,
    UrlLocation,
    RuntimeLocation,
    LogLocation,
    GraphLocation,
]


# --- Sub-components ---
class Confidence(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=False, frozen=True)
    band: ConfidenceBand
    score_bp: int = Field(ge=0, le=10000)
    calibration_ref: Optional[str] = None


class ProducerRef(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    producer_id: str
    producer_type: str
    name: str
    version: str
    build_digest: Optional[str] = None
    key_id: str


class Limitation(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    code: str
    message: str


class Link(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    rel: str
    warrant_id: str


class Environment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    environment_id: str
    platform: str
    arch: str
    runtime: str
    isolation: Literal["none", "process", "container", "vm"]


class ValidTime(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    from_ts: str = Field(alias="from")
    to_ts: Optional[str] = Field(default=None, alias="to")

    @field_validator("from_ts", "to_ts")
    @classmethod
    def validate_ts(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            parse_ts(v)
        return v


class RawRef(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    blob_id: str
    sha256: str
    size_bytes: int = Field(ge=0)
    media_type: str


# --- Warrant Body & Envelope ---
class WarrantBody(BaseModel):
    """The immutable, hashed and signed payload of a warrant (§6.3.1)."""

    model_config = ConfigDict(extra="forbid", strict=False, frozen=True, populate_by_name=True)


    schema_name: Literal["reva.warrant/1"] = Field(default="reva.warrant/1", alias="schema")
    tenant_id: str
    subject: Subject
    producer: ProducerRef
    operation: str
    predicate: str
    parameters: Dict[str, Any]
    statement: Dict[str, Any]
    raw_ref: Optional[RawRef] = None
    authority: Authority
    epistemic_state: Epistemic
    confidence: Confidence
    coverage: Optional[Coverage] = None
    locations: List[Location] = Field(default_factory=list)
    limitations: List[Limitation] = Field(default_factory=list)
    environment: Optional[Environment] = None
    observed_at: str
    valid_time: ValidTime
    links: List[Link] = Field(default_factory=list)

    @field_validator("observed_at")
    @classmethod
    def validate_observed_at(cls, v: str) -> str:
        parse_ts(v)
        return v

    @field_validator("locations", "limitations", "links", mode="after")
    @classmethod
    def normalize_sorted_sets(cls, v: List[Any]) -> List[Any]:
        return normalize_set(v)

    def canonical_dict(self) -> Dict[str, Any]:
        """Return clean dict suitable for JCS hashing and signing."""
        return self.model_dump(by_alias=True, mode="json", exclude_none=False)

    def compute_id(self) -> str:
        """Derive normative warrant_id wr1_<sha256>."""
        return warrant_id(self.canonical_dict())


class WarrantSignature(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    alg: Literal["ed25519"] = "ed25519"
    key_id: str
    sig: str


class WarrantLogRef(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    log_id: str
    leaf_index: int = Field(ge=0)


class WarrantAcl(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    source_acl_refs: List[str] = Field(default_factory=list)
    allow: List[str] = Field(default_factory=list)
    deny: List[str] = Field(default_factory=list)


class WarrantClassification(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    level: Literal["public", "internal", "confidential", "restricted"] = "internal"
    pii: bool = False
    tags: List[str] = Field(default_factory=list)


class WarrantRetention(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    policy_id: str = "default"
    expires_at: Optional[str] = None
    legal_hold: bool = False


class WarrantDisplay(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    subject_label: str
    local_path: Optional[str] = None
    url: Optional[str] = None


class WarrantEnvelope(BaseModel):
    """The administrative, mutable metadata wrapping a warrant body (§6.3.2)."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    warrant_id: str
    signature: WarrantSignature
    recorded_at: str
    log: WarrantLogRef
    acl: WarrantAcl = Field(default_factory=WarrantAcl)
    classification: WarrantClassification = Field(default_factory=WarrantClassification)
    retention: WarrantRetention = Field(default_factory=WarrantRetention)
    display: Optional[WarrantDisplay] = None
    status: Literal["active", "superseded", "retracted"] = "active"
    status_changed_at: Optional[str] = None



class SealedWarrant(BaseModel):
    """The full sealed warrant combining body and envelope."""

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    warrant_id: str
    body: WarrantBody
    envelope: WarrantEnvelope
