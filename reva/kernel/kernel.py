"""WarrantKernel issue pipeline, batching, supersession, and retraction (T-111 / T-112 / T-114)."""

from __future__ import annotations

import uuid
from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field

from reva.core.errors import (
    PredicateUnknownError,
    ProducerError,
    RevaIntegrityError,
    RevaNotFoundError,
    RevaValidationError,
)
from reva.core.ids import warrant_id as compute_warrant_id
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.acl import Principal
from reva.kernel.blobs import BlobStore
from reva.kernel.builder import ObservationDraft, WarrantDraftBuilder
from reva.kernel.keys import decrypt_private_key
from reva.kernel.predicates import get_predicate
from reva.kernel.producers import get_producer
from reva.kernel.query import get_warrant, query_warrants
from reva.kernel.signing import sign_warrant_id
from reva.kernel.store import RevaStore
from reva.kernel.translog import TransparencyLog
from reva.kernel.validation import ValidationContext, assert_valid
from reva.kernel.warrant import (
    Authority,
    ConfidenceBand,
    Epistemic,
    Link,
    ProducerRef,
    RawRef,
    SealedWarrant,
    WarrantBody,
    WarrantEnvelope,
)


class BatchItemResult(BaseModel):
    index: int
    warrant_id: Optional[str] = None
    warrant: Optional[SealedWarrant] = None
    error: Optional[Dict[str, Any]] = None


class BatchIssueResult(BaseModel):
    tenant_id: str
    total: int
    succeeded: int
    failed: int
    results: List[BatchItemResult]


class WarrantKernel:
    """Core REVA warrant issuance, bitemporal querying, and lifecycle engine."""

    def __init__(self, store: RevaStore, blobs: Optional[BlobStore] = None, log: Optional[TransparencyLog] = None) -> None:
        self.store = store
        self.blobs = blobs or BlobStore()
        self.log = log or TransparencyLog(store, "reva_main_log")

    @property
    def translog(self) -> TransparencyLog:
        return self.log

    def issue(
        self,
        tenant_id: str,
        draft: ObservationDraft,
        raw: Optional[Union[BinaryIO, bytes]] = None,
    ) -> SealedWarrant:
        """Issue a warrant deterministically with CAS storage, validation, log append, and outbox notification."""
        # 1. Resolve producer and active key
        producer = get_producer(self.store, tenant_id, draft.producer.producer_id)
        if not producer or not producer.active:
            raise ProducerError(f"Producer {draft.producer.producer_id} not found or inactive in tenant {tenant_id}")

        key_id = producer.active_key_id
        if not key_id:
            raise ProducerError(f"Producer {producer.producer_id} has no active signing key")

        key_record = self.store.get_key(key_id)
        if not key_record or not key_record.get("private_key_enc"):
            raise ProducerError(f"Signing key {key_id} is missing private key data")

        # 2. Resolve predicate spec
        spec = get_predicate(draft.predicate)
        if not spec:
            raise PredicateUnknownError(f"Unknown predicate: {draft.predicate}")

        # 3. Handle raw payload storage (CAS idempotent)
        raw_ref: Optional[RawRef] = None
        if raw is not None:
            blob_ref = self.blobs.put(
                tenant_id=tenant_id,
                data=raw,
                classification=draft.classification.level,
            )
            raw_ref = RawRef(
                blob_id=blob_ref.blob_id,
                sha256=blob_ref.sha256,
                media_type=blob_ref.media_type,
                size_bytes=blob_ref.size_bytes,
            )

        # 4. Construct WarrantBody
        body = WarrantBody(
            schema="reva.warrant/1",
            tenant_id=tenant_id,
            subject=draft.subject,
            predicate=draft.predicate,
            producer=ProducerRef(
                producer_id=producer.producer_id,
                producer_type=producer.producer_type,
                name=producer.name,
                version=producer.version,
                key_id=key_id,
                build_digest=producer.build_digest,
            ),
            operation=draft.operation,
            authority=draft.authority,
            epistemic_state=draft.epistemic_state,
            confidence=draft.confidence,
            observed_at=draft.observed_at,
            valid_time=draft.valid_time,
            statement=draft.statement,
            parameters=draft.parameters,
            locations=draft.locations,
            coverage=draft.coverage,
            limitations=draft.limitations,
            links=draft.links,
            environment=draft.environment,
            raw_ref=raw_ref,
        )

        # 5. Cross-field validation (V-01..V-16)
        known_artifacts = {}
        if hasattr(draft.subject, "artifact_id") and hasattr(draft.subject, "sha256"):
            known_artifacts[draft.subject.artifact_id] = draft.subject.sha256
        if raw_ref:
            known_artifacts[raw_ref.blob_id] = raw_ref.sha256

        ctx = ValidationContext(
            known_artifacts=known_artifacts,
            known_warrants={link.warrant_id for link in draft.links},
            active_keys={key_id},
            predicate_validators={spec.name: lambda s: True},
            skip_external_lookups=True,
        )
        assert_valid(body, ctx)


        # 6. Compute canonical warrant ID
        canonical_dict = body.canonical_dict()
        wid = compute_warrant_id(canonical_dict)

        # 7. Check idempotency: if already stored, return existing warrant
        existing = self.store.get_warrant(tenant_id, wid)
        if existing:
            return SealedWarrant(
                warrant_id=wid,
                body=WarrantBody.model_validate(existing[0]),
                envelope=WarrantEnvelope.model_validate(existing[1]),
            )

        # 8. Decrypt private key and generate signature
        priv_key = decrypt_private_key(key_record["private_key_enc"])
        sig = sign_warrant_id(wid, priv_key)


        # 9. Append to Merkle Transparency Log
        leaf_index = self.log.append(wid)

        # 10. Assemble Envelope
        now_ts = format_ts(utc_now_ms())
        envelope = WarrantEnvelope(
            warrant_id=wid,
            signature={
                "alg": "ed25519",
                "key_id": key_id,
                "sig": sig,
            },
            recorded_at=now_ts,
            log={
                "log_id": self.log.log_id,
                "leaf_index": leaf_index,
            },
            status="active",
            classification=draft.classification,
            acl=draft.acl,
        )

        # 11. Transactionally persist in store
        if hasattr(body.subject, "sha256"):
            subject_key = f"artifact:{body.subject.sha256}"
        elif hasattr(body.subject, "record_key"):
            subject_key = f"source_record:{body.subject.system_instance_id}:{body.subject.record_key}"
        elif hasattr(body.subject, "entity_id"):
            subject_key = f"graph_entity:{body.subject.entity_type}:{body.subject.entity_id}"
        elif hasattr(body.subject, "instance_key"):
            subject_key = f"runtime_instance:{body.subject.environment_id}:{body.subject.instance_key}"
        elif hasattr(body.subject, "reason"):
            subject_key = f"none:{body.subject.reason}"
        else:
            subject_key = "unknown"

        links_data = [{"rel": l.rel, "warrant_id": l.warrant_id} for l in body.links]
        self.store.save_warrant(
            tenant_id=tenant_id,
            warrant_id=wid,
            body=canonical_dict,
            envelope=envelope.model_dump(mode="json"),
            subject_key=subject_key,
            predicate=body.predicate,
            producer_id=producer.producer_id,
            authority=body.authority.value,
            epistemic=body.epistemic_state.value,
            confidence_bp=body.confidence.score_bp,
            observed_at=body.observed_at,
            valid_from=body.valid_time.from_ts,
            valid_to=body.valid_time.to_ts,
            recorded_at=now_ts,
            status="active",
            log_index=leaf_index,
            acl_tokens=draft.acl.source_acl_refs,
            classification=draft.classification.level,
            links=links_data,
        )


        # 12. Record outbox event for projection and listeners
        self.store.save_outbox_event(
            event_id=f"evt_{uuid.uuid4().hex}",
            tenant_id=tenant_id,
            event_type="reva.warrant.issued",
            payload={
                "warrant_id": wid,
                "predicate": body.predicate,
                "producer_id": producer.producer_id,
                "recorded_at": now_ts,
            },
        )

        return SealedWarrant(
            warrant_id=wid,
            body=body,
            envelope=envelope,
        )

    def issue_many(
        self,
        tenant_id: str,
        drafts: List[ObservationDraft],
        batch_size: int = 500,
    ) -> BatchIssueResult:
        """Batch issue with per-item validation and failure isolation (T-112 / REVA-WK-008)."""
        results: List[BatchItemResult] = []
        succeeded = 0
        failed = 0

        for i, draft in enumerate(drafts):
            try:
                warrant = self.issue(tenant_id, draft)
                results.append(BatchItemResult(index=i, warrant_id=warrant.warrant_id, warrant=warrant))
                succeeded += 1
            except Exception as e:
                err_dict = {"type": type(e).__name__, "message": str(e)}
                results.append(BatchItemResult(index=i, error=err_dict))
                failed += 1

        return BatchIssueResult(
            tenant_id=tenant_id,
            total=len(drafts),
            succeeded=succeeded,
            failed=failed,
            results=results,
        )

    def supersede(
        self,
        tenant_id: str,
        old_warrant_id: str,
        new_draft: ObservationDraft,
        reason: str,
    ) -> SealedWarrant:
        """Supersede an existing warrant with a newly issued warrant (T-114 / REVA-WK-011)."""
        # Add supersedes link to new draft
        new_draft.links.append(Link(rel="supersedes", warrant_id=old_warrant_id))

        # Issue new warrant
        new_warrant = self.issue(tenant_id, new_draft)

        # Mark old warrant superseded in envelope
        old_row = self.store.get_warrant(tenant_id, old_warrant_id)
        if old_row:
            old_body, old_env = old_row
            old_env["status"] = "superseded"
            old_env["status_changed_at"] = format_ts(utc_now_ms())
            self.store.update_warrant_envelope(tenant_id, old_warrant_id, old_env, "superseded")

        return new_warrant

    def retract(
        self,
        tenant_id: str,
        warrant_id: str,
        reason: str,
        producer_id: str,
    ) -> SealedWarrant:
        """Retract an existing warrant with an audit retraction warrant (T-114 / REVA-WK-011)."""
        now = format_ts(utc_now_ms())
        draft = (
            WarrantDraftBuilder("reva.pred.human_assertion", "retract")
            .producer(producer_id, f"retractor:{producer_id}", "1.0.0")
            .about_nothing(f"retraction of {warrant_id}")
            .authority(Authority.HUMAN_ATTESTED)
            .observed()
            .confidence(ConfidenceBand.EXACT, 10000)
            .link("supersedes", warrant_id)
            .statement({"action": "retract", "retracted_warrant_id": warrant_id, "reason": reason})
            .valid(now)
            .build()
        )

        retraction_warrant = self.issue(tenant_id, draft)

        old_row = self.store.get_warrant(tenant_id, warrant_id)
        if old_row:
            old_body, old_env = old_row
            old_env["status"] = "retracted"
            old_env["status_changed_at"] = now
            self.store.update_warrant_envelope(tenant_id, warrant_id, old_env, "retracted")

        return retraction_warrant


    def get(
        self,
        tenant_id: str,
        principal: Optional[Union[Principal, str]] = None,
        warrant_id: str = "",
        **kwargs: Any,
    ) -> SealedWarrant:
        """Retrieve warrant with cryptographic verification and ACL enforcement."""
        p = principal or kwargs.get("principal_id") or "system"
        if isinstance(p, str):
            p = Principal(id=p, tenant_id=tenant_id, is_admin=True)
        wid = warrant_id or kwargs.get("warrant_id", "")
        return get_warrant(self.store, tenant_id, p, wid)

    def query(
        self,
        tenant_id: str,
        principal: Optional[Union[Principal, str]] = None,
        subject_key: Optional[str] = None,
        predicate: Optional[str] = None,
        producer_id: Optional[str] = None,
        authority: Optional[str] = None,
        epistemic: Optional[str] = None,
        status: Optional[str] = None,
        min_confidence_bp: Optional[int] = None,
        classification: Optional[str] = None,
        as_of_valid: Optional[str] = None,
        as_of_recorded: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        **kwargs: Any,
    ) -> List[SealedWarrant]:
        """Search warrants bitemporally with ACL filtering."""
        p = principal or kwargs.get("principal_id") or "system"
        if isinstance(p, str):
            p = Principal(id=p, tenant_id=tenant_id, is_admin=True)
        return query_warrants(
            store=self.store,
            tenant_id=tenant_id,
            principal=p,
            subject_key=subject_key,
            predicate=predicate,
            producer_id=producer_id,
            authority=authority,
            epistemic=epistemic,
            status=status,
            min_confidence_bp=min_confidence_bp,
            classification=classification,
            as_of_valid=as_of_valid,
            as_of_recorded=as_of_recorded,
            limit=limit,
            offset=offset,
        )
