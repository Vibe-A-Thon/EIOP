"""Canonical Cross-Module Contracts conforming to requirements section 6."""
from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class PrincipalType(str, Enum):
    USER = "user"
    SERVICE_ACCOUNT = "service_account"
    AGENT = "agent"

class TrustedScope(BaseModel):
    tenant_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    principal_id: str = Field(min_length=1)
    principal_type: PrincipalType
    roles: list[str] = Field(default_factory=list)
    effective_acls: list[str] = Field(default_factory=list)
    policy_epoch: int = Field(default=1, ge=1)
    delegation_chain: list[str] = Field(default_factory=list)
    autonomy_level: Optional[str] = None
    expires_at: datetime = Field(default_factory=_utcnow)

class TermKind(str, Enum):
    IRI = "iri"
    BLANK_NODE = "blank_node"
    LITERAL = "literal"
    TRIPLE = "triple"

class RDFTerm(BaseModel):
    kind: TermKind
    value: str  # exact lexical form; never case-folded (CRA-016.2)
    datatype: Optional[str] = None
    language: Optional[str] = None

class EvidenceLocator(BaseModel):
    document_id: str
    source_system: str
    source_revision: str
    page_number: Optional[int] = None
    slide_number: Optional[int] = None
    sheet_name: Optional[str] = None
    cell: Optional[str] = None
    paragraph_index: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    bounding_box: Optional[list[float]] = None  # [ymin, xmin, ymax, xmax] in 0..1
    media_start_ms: Optional[int] = None
    media_end_ms: Optional[int] = None

class KnowledgeState(str, Enum):
    ASSERTED = "asserted"
    INFERRED = "inferred"
    PROPOSED = "proposed"
    REJECTED = "rejected"
    HISTORICAL = "historical"

class CanonicalAssertion(BaseModel):
    assertion_id: str
    graph_iri: str
    subject: RDFTerm
    predicate: RDFTerm
    object: RDFTerm
    knowledge_state: KnowledgeState = KnowledgeState.ASSERTED
    is_inferred: bool = False
    justifications: list[list[str]] = Field(default_factory=list)
    evidence: list[EvidenceLocator] = Field(default_factory=list)
    extraction_model: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    confidence_calibrated: bool = False
    tenant_id: str
    source_acl_vector: list[str] = Field(default_factory=list)
    security_classification: str = "INTERNAL"
    policy_epoch: int = 1
    source_revision: Optional[str] = None
    ontology_revision: Optional[str] = None
    mapping_revision: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    tx_from: datetime = Field(default_factory=_utcnow)
    tx_to: Optional[datetime] = None
    approver: Optional[str] = None
    model_lineage: Optional[ModelLineage] = None

class ActionStatus(str, Enum):
    PROPOSED = "proposed"
    STAGED = "staged"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"
    UNKNOWN_OUTCOME = "unknown_outcome"

class ActionIntent(BaseModel):
    action_id: str
    action_shape_iri: str
    target_system_id: str
    idempotency_key: str = Field(min_length=16, max_length=128)
    parameters: dict[str, Any]
    parameters_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    base_revisions: dict[str, str] = Field(default_factory=dict)
    status: ActionStatus = ActionStatus.PROPOSED
    requested_by: str
    approved_by: Optional[str] = None
    approval_signature: Optional[str] = None
    approval_nonce: Optional[str] = None
    approval_expires_at: Optional[datetime] = None
    dry_run: bool = False
    read_back_query: Optional[str] = None
    compensation_action_id: Optional[str] = None
    tenant_id: str

class ProducerClass(str, Enum):
    DETERMINISTIC = "deterministic"
    PROBABILISTIC = "probabilistic"

class ModelLineage(BaseModel):
    model_id: str
    model_version: str
    producer_class: ProducerClass = ProducerClass.PROBABILISTIC
    trained_at: datetime = Field(default_factory=_utcnow)
    graph_snapshot_id: Optional[str] = None
    code_commit: str = "baseline"
    seed_bundle: dict[str, Any] = Field(default_factory=dict)
    environment_digest: str = "default_env"
    calibrator_id: Optional[str] = None
    gate_report_ref: Optional[str] = None
    prompt_digest: Optional[str] = None
    context_manifest_digest: Optional[str] = None

class AgreementState(str, Enum):
    CORROBORATED = "CORROBORATED"
    DISPUTED = "DISPUTED"
    UNCORROBORATED = "UNCORROBORATED"

class DualPathResult(BaseModel):
    question_digest: str
    deterministic_result: Optional[Any] = None
    probabilistic_result: Optional[Any] = None
    agreement: AgreementState
    deterministic_evidence: list[str] = Field(default_factory=list)
    probabilistic_evidence: list[str] = Field(default_factory=list)
    dispute_details: dict[str, Any] = Field(default_factory=dict)
    explanation: Optional[str] = None

class ContextManifest(BaseModel):
    model_revision: str
    tokenizer: str
    max_input_tokens: int
    max_output_tokens: int
    ordered_evidence: list[dict[str, Any]] = Field(default_factory=list)
    template_revision: str
    retrieval_parameters: dict[str, Any] = Field(default_factory=dict)
    reduction_applied: bool = False
    omitted_count: int = 0
    digest: str
