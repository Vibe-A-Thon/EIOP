"""Strict ASPEII action identity contracts and canonical digesting."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, Literal, NoReturn

import rfc8785
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ACTION_CANONICALIZATION_VERSION = "rfc8785-jcs-1"
ACTION_DOMAIN_SEPARATOR = b"EOIP-ASPEII-ACTION-v1\n"
MAX_JSON_DEPTH = 32
MAX_JSON_NODES = 10_000
MAX_SAFE_INTEGER = (2**53) - 1

ActionEffectClass = Literal[
    "READ_ONLY",
    "ADVISORY",
    "INTERNAL_WRITE",
    "EXTERNAL_WRITE",
    "IRREVERSIBLE",
]
ObligationDecision = Literal["PASS", "FAIL", "UNKNOWN"]
ApprovalChoice = Literal["APPROVE", "REJECT"]
ApprovalState = Literal["AVAILABLE", "CONSUMED", "REVOKED", "EXPIRED"]
EnforceabilityMode = Literal[
    "PRE_EXECUTION_GATE",
    "DELEGATED_GATE",
    "OBSERVE_ONLY",
    "RUNTIME_CONTROLLED",
]


class _FrozenDict(dict[str, Any]):
    def _deny_mutation(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise TypeError("Action intent mappings are immutable")

    __setitem__ = _deny_mutation
    __delitem__ = _deny_mutation
    clear = _deny_mutation
    pop = _deny_mutation
    popitem = _deny_mutation
    __ior__ = _deny_mutation

    def setdefault(self, key: str, default: Any = None, /) -> Any:
        self._deny_mutation(key, default)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self._deny_mutation(*args, **kwargs)


class _FrozenList(list):
    def _deny_mutation(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise TypeError("Action intent lists are immutable")

    __setitem__ = _deny_mutation
    __delitem__ = _deny_mutation
    __iadd__ = _deny_mutation
    __imul__ = _deny_mutation
    append = _deny_mutation
    clear = _deny_mutation
    extend = _deny_mutation
    insert = _deny_mutation
    pop = _deny_mutation
    remove = _deny_mutation
    reverse = _deny_mutation
    def sort(self, *, key: Callable[[Any], Any] | None = None, reverse: bool = False) -> None:
        self._deny_mutation(key=key, reverse=reverse)


class ActionReference(BaseModel):
    """Immutable, revision-bound reference used in a security decision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: str = Field(min_length=1, max_length=64)
    id: str = Field(min_length=1, max_length=512)
    revision: int = Field(ge=1)
    digest: str = Field(pattern=r"^[0-9a-f]{64}$")


def _validate_json_value(value: Any, *, path: str, depth: int, node_count: list[int]) -> None:
    node_count[0] += 1
    if node_count[0] > MAX_JSON_NODES:
        raise ValueError(f"JSON value at {path} exceeds the node limit")
    if depth > MAX_JSON_DEPTH:
        raise ValueError(f"JSON value at {path} exceeds the nesting limit")
    if value is None or isinstance(value, (bool, str)):
        if isinstance(value, str):
            try:
                value.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ValueError(f"String at {path} is not valid Unicode") from exc
        return
    if isinstance(value, int):
        if not -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER:
            raise ValueError(f"Integer at {path} is outside the RFC 8785 interoperable range")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"Non-finite number at {path} is not valid JSON")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_value(
                item, path=f"{path}[{index}]", depth=depth + 1, node_count=node_count
            )
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"Object key at {path} must be a string")
            try:
                key.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise ValueError(f"Object key at {path} is not valid Unicode") from exc
            _validate_json_value(
                item, path=f"{path}.{key}", depth=depth + 1, node_count=node_count
            )
        return
    raise ValueError(f"Value at {path} has unsupported JSON type {type(value).__name__}")


def _validate_json_object(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Action arguments and expected state must be JSON objects")
    _validate_json_value(value, path="$", depth=0, node_count=[0])
    return value


def _freeze_json(value: Any) -> Any:
    if isinstance(value, dict):
        return _FrozenDict({key: _freeze_json(item) for key, item in value.items()})
    if isinstance(value, list):
        return _FrozenList(_freeze_json(item) for item in value)
    return value


def _normalize_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Action timestamps must include a timezone")
    return value.astimezone(timezone.utc)


class ASPEIIActionIntent(BaseModel):
    """Immutable, fully resolved action projection used for checking/approval."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["aspeii-action/1"] = "aspeii-action/1"
    canonicalization_version: Literal["rfc8785-jcs-1"] = ACTION_CANONICALIZATION_VERSION
    action_id: str = Field(min_length=1, max_length=128)
    revision: int = Field(ge=1)
    tenant_id: str = Field(min_length=1, max_length=256)
    workspace_id: str = Field(min_length=1, max_length=256)
    principal_id: str = Field(min_length=1, max_length=512)
    intent_ref: ActionReference
    task_ref: ActionReference
    grant_ref: ActionReference
    tool_ref: ActionReference
    adapter_ref: ActionReference
    resource_ref: ActionReference
    policy_ref: ActionReference
    destination: str = Field(min_length=1, max_length=2048)
    account_id: str = Field(min_length=1, max_length=512)
    effect_class: ActionEffectClass
    arguments: dict[str, Any] = Field(max_length=256)
    expected_state: dict[str, Any] = Field(default_factory=dict, max_length=256)
    obligation_refs: list[ActionReference] = Field(min_length=1, max_length=256)
    evidence_refs: list[ActionReference] = Field(default_factory=list, max_length=512)
    scope: list[str] = Field(min_length=1, max_length=256)
    deadline: datetime
    created_at: datetime
    created_by: str = Field(min_length=1, max_length=512)
    logical_idempotency_key: str = Field(min_length=16, max_length=128)

    @field_validator("arguments", "expected_state", mode="before")
    @classmethod
    def validate_json_objects(cls, value: Any) -> dict[str, Any]:
        return _validate_json_object(value)

    @field_validator("deadline", "created_at")
    @classmethod
    def normalize_timestamps(cls, value: datetime) -> datetime:
        return _normalize_utc(value)

    @field_validator("scope")
    @classmethod
    def validate_scope(cls, value: list[str]) -> list[str]:
        if any(not item or len(item) > 512 for item in value):
            raise ValueError("Action scopes must be nonempty strings of at most 512 characters")
        if len(value) != len(set(value)):
            raise ValueError("Action scopes must not contain duplicates")
        return sorted(value)

    @field_validator("obligation_refs", "evidence_refs")
    @classmethod
    def validate_reference_sets(cls, value: list[ActionReference]) -> list[ActionReference]:
        identities = [(item.kind, item.id, item.revision, item.digest) for item in value]
        if len(identities) != len(set(identities)):
            raise ValueError("Action reference sets must not contain duplicates")
        return sorted(value, key=lambda item: (item.kind, item.id, item.revision, item.digest))

    @model_validator(mode="after")
    def validate_action(self) -> ASPEIIActionIntent:
        if self.created_by != self.principal_id:
            raise ValueError("created_by must match the resolved principal_id")
        if self.deadline <= self.created_at:
            raise ValueError("Action deadline must be later than created_at")
        object.__setattr__(self, "arguments", _freeze_json(self.arguments))
        object.__setattr__(self, "expected_state", _freeze_json(self.expected_state))
        object.__setattr__(self, "obligation_refs", _FrozenList(self.obligation_refs))
        object.__setattr__(self, "evidence_refs", _FrozenList(self.evidence_refs))
        object.__setattr__(self, "scope", _FrozenList(self.scope))
        return self


class ASPEIIObligationResult(BaseModel):
    """One independently evaluated, versioned admission obligation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    obligation_ref: ActionReference
    verifier_ref: ActionReference
    decision: ObligationDecision
    reason_code: str = Field(min_length=1, max_length=128)
    evidence_refs: list[ActionReference] = Field(default_factory=list, max_length=256)
    evaluated_at: datetime

    @field_validator("evaluated_at")
    @classmethod
    def normalize_evaluated_at(cls, value: datetime) -> datetime:
        return _normalize_utc(value)

    @field_validator("evidence_refs")
    @classmethod
    def freeze_evidence_refs(cls, value: list[ActionReference]) -> list[ActionReference]:
        return _FrozenList(value)


class ASPEIIActionCertificatePayload(BaseModel):
    """Successful admission payload awaiting a configured trusted signer."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["aspeii-action-certificate/1"] = "aspeii-action-certificate/1"
    certificate_id: str = Field(min_length=1, max_length=128)
    action_ref: ActionReference
    action_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    canonicalization_version: Literal["rfc8785-jcs-1"]
    verifier_ref: ActionReference
    required_obligation_refs: list[ActionReference] = Field(min_length=1, max_length=256)
    obligation_results: list[ASPEIIObligationResult] = Field(min_length=1, max_length=256)
    authorization_decision: Literal["ALLOW"]
    enforceability_mode: EnforceabilityMode
    approval_refs: list[ActionReference] = Field(default_factory=list, max_length=32)
    issued_at: datetime
    expires_at: datetime
    key_id: str = Field(min_length=1, max_length=256)

    @field_validator("issued_at", "expires_at")
    @classmethod
    def normalize_certificate_times(cls, value: datetime) -> datetime:
        return _normalize_utc(value)

    @field_validator("required_obligation_refs", "obligation_results", "approval_refs")
    @classmethod
    def freeze_certificate_lists(cls, value: list[Any]) -> list[Any]:
        return _FrozenList(value)

    @model_validator(mode="after")
    def validate_certificate(self) -> ASPEIIActionCertificatePayload:
        if self.expires_at <= self.issued_at:
            raise ValueError("Certificate expiry must be later than issue time")
        if self.action_ref.digest != self.action_digest:
            raise ValueError("Certificate action reference must bind the canonical action digest")
        if any(result.decision != "PASS" for result in self.obligation_results):
            raise ValueError("A certificate cannot contain failed or unknown obligations")
        required_keys = [
            (item.kind, item.id, item.revision, item.digest)
            for item in self.required_obligation_refs
        ]
        result_keys = [
            (
                result.obligation_ref.kind,
                result.obligation_ref.id,
                result.obligation_ref.revision,
                result.obligation_ref.digest,
            )
            for result in self.obligation_results
        ]
        if len(required_keys) != len(set(required_keys)) or len(result_keys) != len(set(result_keys)):
            raise ValueError("Certificate obligation references must be unique")
        if set(result_keys) != set(required_keys):
            raise ValueError("Certificate must contain exactly one result for every required obligation")
        return self


class ASPEIIActionCertificate(ASPEIIActionCertificatePayload):
    """Admission payload plus a cryptographic signature from a configured key."""

    signature: str = Field(min_length=1, max_length=128)


class ASPEIIApprovalDecision(BaseModel):
    """Immutable reviewer decision bound to one action digest and policy revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["aspeii-approval/1"] = "aspeii-approval/1"
    approval_id: str = Field(min_length=1, max_length=128)
    tenant_id: str = Field(min_length=1, max_length=256)
    action_ref: ActionReference
    action_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    requester_principal_id: str = Field(min_length=1, max_length=512)
    reviewer_principal_id: str = Field(min_length=1, max_length=512)
    decision: ApprovalChoice
    rationale: str = Field(min_length=1, max_length=4096)
    policy_ref: ActionReference
    separation_of_duties_passed: bool
    decided_at: datetime
    expires_at: datetime
    state: ApprovalState = "AVAILABLE"
    consumed_at: datetime | None = None
    revocation_ref: ActionReference | None = None

    @field_validator("decided_at", "expires_at", "consumed_at")
    @classmethod
    def normalize_decision_times(cls, value: datetime | None) -> datetime | None:
        return None if value is None else _normalize_utc(value)

    @model_validator(mode="after")
    def validate_decision(self) -> ASPEIIApprovalDecision:
        if self.expires_at <= self.decided_at:
            raise ValueError("Approval expiry must be later than decision time")
        if self.action_ref.digest != self.action_digest:
            raise ValueError("Approval action reference must bind the canonical action digest")
        if self.decision == "APPROVE":
            if self.requester_principal_id == self.reviewer_principal_id:
                raise ValueError("An approver cannot approve their own action")
            if not self.separation_of_duties_passed:
                raise ValueError("Approval requires a passing separation-of-duties check")
        if self.state == "CONSUMED" and self.consumed_at is None:
            raise ValueError("Consumed approval state requires consumed_at")
        if self.state != "CONSUMED" and self.consumed_at is not None:
            raise ValueError("Only consumed approval state may have consumed_at")
        if self.state == "REVOKED" and self.revocation_ref is None:
            raise ValueError("Revoked approval state requires a revocation reference")
        if self.consumed_at is not None and self.consumed_at < self.decided_at:
            raise ValueError("Approval cannot be consumed before it was decided")
        return self


def canonical_action_bytes(action: ASPEIIActionIntent) -> bytes:
    """Return the domain-separated RFC 8785 preimage for a resolved action."""

    if not isinstance(action, ASPEIIActionIntent):
        raise TypeError("canonical_action_bytes requires an ASPEIIActionIntent")
    projection = action.model_dump(mode="json")
    try:
        return ACTION_DOMAIN_SEPARATOR + rfc8785.dumps(projection)
    except (rfc8785.CanonicalizationError, ValueError, TypeError) as exc:
        raise ValueError("Action intent cannot be serialized as RFC 8785 JSON") from exc


def canonical_action_digest(action: ASPEIIActionIntent) -> str:
    """SHA-256 of the versioned, domain-separated canonical action bytes."""

    return hashlib.sha256(canonical_action_bytes(action)).hexdigest()