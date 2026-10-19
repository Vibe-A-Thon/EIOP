"""Fluent builder for warrant observation drafts (T-118 / REVA-WK-013 / REVA-WK-014)."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

from reva.core.ids import artifact_id as compute_artifact_id
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.authority import Authority, ConfidenceBand, CoverageStatus, Depth, Epistemic
from reva.kernel.coverage import Coverage
from reva.kernel.warrant import (
    ArchiveMemberLocation,
    ArtifactRangeLocation,
    ArtifactSubject,
    Confidence,
    Environment,
    GraphEntitySubject,
    GraphLocation,
    Limitation,
    Link,
    Location,
    LogLocation,
    NoneSubject,
    ProducerRef,
    RecordFieldLocation,
    RuntimeInstanceSubject,
    RuntimeLocation,
    SourceRecordSubject,
    SourceSpanLocation,
    Subject,
    UrlLocation,
    ValidTime,
    WarrantAcl,
    WarrantClassification,
)


class ObservationDraft(BaseModel):
    """Normalized pre-warrant draft observation before signing and sealing."""

    predicate: str
    operation: str
    producer: ProducerRef
    subject: Subject
    locations: List[Location] = Field(default_factory=list)
    authority: Authority = Authority.SHIPPED_ARTIFACT
    epistemic_state: Epistemic = Epistemic.OBSERVED
    confidence: Confidence
    coverage: Optional[Coverage] = None
    limitations: List[Limitation] = Field(default_factory=list)
    links: List[Link] = Field(default_factory=list)
    environment: Optional[Environment] = None
    observed_at: str
    valid_time: ValidTime
    parameters: Dict[str, Any] = Field(default_factory=dict)
    statement: Dict[str, Any] = Field(default_factory=dict)
    classification: WarrantClassification = Field(default_factory=WarrantClassification)
    acl: WarrantAcl = Field(default_factory=WarrantAcl)


class WarrantDraftBuilder:
    """Fluent API for constructing valid ObservationDraft instances."""

    def __init__(self, predicate: str, operation: str) -> None:
        self._predicate = predicate
        self._operation = operation
        self._producer: Optional[ProducerRef] = None
        self._subject: Optional[Subject] = None
        self._locations: List[Location] = []
        self._authority: Authority = Authority.SHIPPED_ARTIFACT
        self._epistemic_state: Epistemic = Epistemic.OBSERVED

        self._confidence: Optional[Confidence] = None
        self._coverage: Optional[Coverage] = None
        self._limitations: List[Limitation] = []
        self._links: List[Link] = []
        self._environment: Optional[Environment] = None
        now_ts = format_ts(utc_now_ms())
        self._observed_at: str = now_ts
        self._valid_time: ValidTime = ValidTime.model_validate({"from": now_ts})
        self._parameters: Dict[str, Any] = {}
        self._statement: Dict[str, Any] = {}
        self._classification = WarrantClassification()
        self._acl = WarrantAcl()

    # Producer
    def producer(
        self,
        producer_id: str,
        name: str,
        version: str,
        producer_type: str = "tool",
        key_id: str = "key1_dummy",
        build_digest: Optional[str] = None,
    ) -> WarrantDraftBuilder:
        self._producer = ProducerRef(
            producer_id=producer_id,
            producer_type=producer_type,
            name=name,
            version=version,
            key_id=key_id,
            build_digest=build_digest,
        )
        return self

    # Subjects
    def about_artifact(
        self,
        sha256: str,
        size_bytes: int = 0,
        media_type: str = "application/octet-stream",
        format: str = "raw",
        artifact_id: Optional[str] = None,
    ) -> WarrantDraftBuilder:
        aid = artifact_id or compute_artifact_id(sha256)
        self._subject = ArtifactSubject(
            artifact_id=aid,
            sha256=sha256,
            size_bytes=size_bytes,
            media_type=media_type,
            format=format,
        )
        return self

    def about_source_record(
        self,
        system_type: str,
        system_instance_id: str,
        record_type: str,
        record_key: str,
        record_version: str = "1",
    ) -> WarrantDraftBuilder:
        self._subject = SourceRecordSubject(
            system_type=system_type,
            system_instance_id=system_instance_id,
            record_type=record_type,
            record_key=record_key,
            record_version=record_version,
        )
        return self

    def about_graph_entity(self, entity_id: str, entity_type: str, version_id: Optional[str] = None) -> WarrantDraftBuilder:
        self._subject = GraphEntitySubject(
            entity_id=entity_id,
            entity_type=entity_type,
            version_id=version_id,
        )
        return self

    def about_runtime_instance(self, environment_id: str, instance_key: str, capture_id: str) -> WarrantDraftBuilder:
        self._subject = RuntimeInstanceSubject(
            environment_id=environment_id,
            instance_key=instance_key,
            capture_id=capture_id,
        )
        return self

    def about_nothing(self, reason: str = "global_observation") -> WarrantDraftBuilder:
        self._subject = NoneSubject(reason=reason)
        return self

    # Locations
    def at_source_span(self, repo_id: str, commit: str, path: str, start_line: int, end_line: int, start_col: int = 0, end_col: int = 0) -> WarrantDraftBuilder:
        self._locations.append(SourceSpanLocation(repo_id=repo_id, commit=commit, path=path, start_line=start_line, end_line=end_line, start_col=start_col, end_col=end_col))
        return self

    def at_record_field(self, system_instance_id: str, record_key: str, json_pointer: str) -> WarrantDraftBuilder:
        self._locations.append(RecordFieldLocation(system_instance_id=system_instance_id, record_key=record_key, json_pointer=json_pointer))
        return self

    def at_url(self, url: str, method: Optional[str] = None) -> WarrantDraftBuilder:
        self._locations.append(UrlLocation(url=url, method=method))
        return self

    # Epistemic and Authority
    def authority(self, auth: Authority) -> WarrantDraftBuilder:
        self._authority = auth
        return self

    def observed(self) -> WarrantDraftBuilder:
        self._epistemic_state = Epistemic.OBSERVED
        return self

    def derived(self) -> WarrantDraftBuilder:
        self._epistemic_state = Epistemic.DERIVED
        return self

    def inferred(self) -> WarrantDraftBuilder:
        self._epistemic_state = Epistemic.INFERRED
        return self

    def unknown(self, reason: str) -> WarrantDraftBuilder:
        self._epistemic_state = Epistemic.UNKNOWN
        self._limitations.append(Limitation(code="EPISTEMIC_UNKNOWN", message=reason))
        return self

    # Confidence
    def confidence(self, band: ConfidenceBand, score_bp: int) -> WarrantDraftBuilder:
        self._confidence = Confidence(band=band, score_bp=score_bp)
        return self

    # Coverage
    def with_coverage(
        self,
        status: CoverageStatus = CoverageStatus.COMPLETE,
        depth: Depth = Depth.STATIC,
        examined_count: Optional[int] = None,
        omitted_count: Optional[int] = None,
        truncated: bool = False,
    ) -> WarrantDraftBuilder:

        self._coverage = Coverage(
            status=status,
            depth=depth,
            examined_count=examined_count,
            omitted_count=omitted_count,
            truncated=truncated,
        )
        return self

    # Limitations
    def limitation(self, code: str, message: str) -> WarrantDraftBuilder:
        self._limitations.append(Limitation(code=code, message=message))
        return self

    # Links
    def link(self, rel: str, to_warrant_id: str) -> WarrantDraftBuilder:
        self._links.append(Link(rel=rel, warrant_id=to_warrant_id))
        return self

    def derived_from(self, parent_warrant_id: str) -> WarrantDraftBuilder:
        return self.link("derived_from", parent_warrant_id)

    # Valid times
    def valid(self, from_ts: str, to_ts: Optional[str] = None) -> WarrantDraftBuilder:
        data: Dict[str, Any] = {"from": from_ts}
        if to_ts is not None:
            data["to"] = to_ts
        self._valid_time = ValidTime.model_validate(data)
        return self

    # Environment
    def environment(self, env: Environment) -> WarrantDraftBuilder:
        self._environment = env
        return self

    # Parameters & Statement
    def params(self, p: Dict[str, Any]) -> WarrantDraftBuilder:
        self._parameters.update(p)
        return self

    def statement(self, s: Dict[str, Any]) -> WarrantDraftBuilder:
        self._statement.update(s)
        return self

    # Classification & ACL
    def classification(self, level: Literal["public", "internal", "confidential", "restricted"] = "internal", pii: bool = False, tags: Optional[List[str]] = None) -> WarrantDraftBuilder:
        self._classification = WarrantClassification(level=level, pii=pii, tags=tags or [])
        return self

    def acl(self, required_tokens: Optional[List[str]] = None, allow: Optional[List[str]] = None, deny: Optional[List[str]] = None) -> WarrantDraftBuilder:
        self._acl = WarrantAcl(
            source_acl_refs=required_tokens or [],
            allow=allow or [],
            deny=deny or [],
        )
        return self

    def build(self) -> ObservationDraft:
        """Validate presence of required draft components and return ObservationDraft."""
        if not self._producer:
            raise ValueError("WarrantDraftBuilder requires a producer")
        if not self._subject:
            raise ValueError("WarrantDraftBuilder requires a subject")
        if not self._confidence:
            raise ValueError("WarrantDraftBuilder requires confidence")

        return ObservationDraft(
            predicate=self._predicate,
            operation=self._operation,
            producer=self._producer,
            subject=self._subject,
            locations=self._locations,
            authority=self._authority,
            epistemic_state=self._epistemic_state,
            confidence=self._confidence,
            coverage=self._coverage,
            limitations=self._limitations,
            links=self._links,
            environment=self._environment,
            observed_at=self._observed_at,
            valid_time=self._valid_time,
            parameters=self._parameters,
            statement=self._statement,
            classification=self._classification,
            acl=self._acl,
        )

