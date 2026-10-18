"""Deterministic Warrant A1 composition over registered operator metadata."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Callable, Sequence
from datetime import datetime, timezone
from typing import Literal
from uuid import NAMESPACE_URL, uuid5

import rfc8785
from pydantic import BaseModel, ConfigDict, Field

from eoip.contracts.warrant import (
    Warrant,
    WarrantActionClass,
    WarrantAuthority,
    WarrantConsequence,
    WarrantGround,
    WarrantOperator,
    WarrantScope,
    WarrantStatus,
    WarrantSubject,
    WarrantValidity,
)
from eoip.provenance.warrant_order import (
    DEFAULT_WARRANT_STATUS_ORDER,
    minimum_warrant_status,
    validate_warrant_status_order,
)

OperatorClass = Literal["OBSERVER", "COMPUTATION", "MODEL", "GENERATOR", "HUMAN"]


class WarrantCompositionOperator(BaseModel):
    """Resolved, approved operator contract required by the pure composer."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    operator_id: str = Field(min_length=1)
    operator_class: OperatorClass
    version: str = Field(min_length=1)
    approved: bool
    observer_qualified: bool = False
    receipt_grounds: tuple[WarrantGround, ...] = ()


class WarrantPrincipalAuthority(BaseModel):
    """Authenticated principal authority supplied by a trusted caller."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: str = Field(min_length=1)
    principal_id: str = Field(min_length=1)
    scopes: tuple[WarrantScope, ...] = ()
    delegation_chain: tuple[str, ...] = ()
    has_subject_authority: bool = False


def _scope_intersection(
    left: WarrantScope,
    right: WarrantScope,
    *,
    is_subtype: Callable[[str, str], bool],
) -> WarrantScope | None:
    if left.action == right.action:
        action = left.action
    elif left.action == "*":
        action = right.action
    elif right.action == "*":
        action = left.action
    else:
        return None

    if left.resource_type == right.resource_type:
        resource_type = left.resource_type
    elif is_subtype(left.resource_type, right.resource_type):
        resource_type = left.resource_type
    elif is_subtype(right.resource_type, left.resource_type):
        resource_type = right.resource_type
    else:
        return None

    selectors = sorted({item for item in (left.selector, right.selector) if item != "*"})
    selector = "*" if not selectors else selectors[0] if len(selectors) == 1 else " AND ".join(
        f"({item})" for item in selectors
    )
    return WarrantScope(action=action, resource_type=resource_type, selector=selector)


def _intersect_scope_sets(
    current: Sequence[WarrantScope],
    other: Sequence[WarrantScope],
    *,
    is_subtype: Callable[[str, str], bool],
) -> list[WarrantScope]:
    intersections = {
        (scope.action, scope.resource_type, scope.selector): scope
        for left in current
        for right in other
        if (scope := _scope_intersection(left, right, is_subtype=is_subtype)) is not None
    }
    return [intersections[key] for key in sorted(intersections)]


def _deduplicate_grounds(grounds: Sequence[WarrantGround]) -> list[WarrantGround]:
    unique: dict[tuple[str, str, str | None], WarrantGround] = {}
    for ground in grounds:
        key = (ground.kind.value, ground.id, ground.version)
        prior = unique.get(key)
        if prior is not None and prior.model_dump(mode="json", exclude_none=True) != ground.model_dump(
            mode="json", exclude_none=True
        ):
            raise ValueError(f"Conflicting warrant grounds share identity {key!r}")
        unique[key] = ground
    return [unique[key] for key in sorted(unique)]


def compose_warrant(
    operator: WarrantCompositionOperator,
    inputs: Sequence[Warrant],
    receipt_grounds: Sequence[WarrantGround],
    principal: WarrantPrincipalAuthority,
    *,
    subject: WarrantSubject,
    now: datetime,
    status_order: Sequence[str | WarrantStatus] = DEFAULT_WARRANT_STATUS_ORDER,
    is_subtype: Callable[[str, str], bool] | None = None,
    model_confidence: float | None = None,
    model_confidence_calibrated: bool = False,
    generator_result: Warrant | None = None,
    action_class: WarrantActionClass | None = None,
    action_kappa: float | None = None,
    impact_run_id: str | None = None,
) -> Warrant:
    """Compose one immutable warrant according to IP requirements A1.

    Operator lookup, principal authentication, action impact computation, and
    generator SASI evaluation belong to trusted callers. The caller must pass
    their resolved results; this function performs no I/O.
    """

    if not operator.approved:
        raise PermissionError("Operator registration is not approved")
    if any(item.tenant_id != principal.tenant_id for item in inputs):
        raise ValueError("Warrant inputs must belong to the principal tenant")
    order = validate_warrant_status_order(status_order)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Warrant composition time must include a timezone")
    now = now.astimezone(timezone.utc)
    subtype = is_subtype or (lambda child, parent: child == parent)

    input_statuses = [item.status for item in inputs]
    input_grounds = [ground for item in inputs for ground in item.grounds]
    grounds = _deduplicate_grounds([*receipt_grounds, *operator.receipt_grounds, *input_grounds])
    validity_inputs = list(inputs)

    if operator.operator_class == "OBSERVER":
        if not operator.observer_qualified:
            raise PermissionError("OBSERVER operator is not qualified against a system of record")
        if not receipt_grounds and not operator.receipt_grounds:
            raise ValueError("OBSERVER composition requires an operator receipt ground")
        status = WarrantStatus.OBSERVED
        confidence = 1.0
    elif operator.operator_class == "HUMAN":
        if not principal.has_subject_authority:
            raise PermissionError("Human operator lacks authority over the warrant subject")
        status = WarrantStatus.ATTESTED
        confidence = 1.0
    elif operator.operator_class == "COMPUTATION":
        status = minimum_warrant_status(input_statuses, order=order)
        input_confidences = [item.confidence for item in inputs]
        confidence = (
            min(value for value in input_confidences if value is not None)
            if input_confidences and all(value is not None for value in input_confidences)
            else None
        )
    elif operator.operator_class == "MODEL":
        if not model_confidence_calibrated or model_confidence is None:
            raise ValueError("MODEL composition requires a calibrated model confidence")
        if not 0.0 <= model_confidence <= 1.0:
            raise ValueError("Calibrated model confidence must be in [0, 1]")
        status = minimum_warrant_status([*input_statuses, WarrantStatus.PREDICTED], order=order)
        confidence = model_confidence
    else:
        if generator_result is None:
            raise ValueError("GENERATOR composition requires a per-proposition SASI result")
        if generator_result.tenant_id != principal.tenant_id:
            raise ValueError("SASI result must belong to the principal tenant")
        if generator_result.subject.ref != subject.ref or generator_result.subject.kind != subject.kind:
            raise ValueError("SASI result subject does not match the composed proposition")
        grounds = _deduplicate_grounds([*grounds, *generator_result.grounds])
        validity_inputs.append(generator_result)
        status = generator_result.status
        confidence = generator_result.confidence

    valid_from_candidates = [item.validity.valid_from for item in validity_inputs]
    if operator.operator_class in {"OBSERVER", "HUMAN"} or not valid_from_candidates:
        valid_from_candidates.append(now)
    valid_from = max(valid_from_candidates).astimezone(timezone.utc)
    finite_valid_to = [item.validity.valid_to for item in validity_inputs if item.validity.valid_to is not None]
    valid_to = min(finite_valid_to).astimezone(timezone.utc) if finite_valid_to else None
    lease_ids = sorted({lease_id for item in validity_inputs for lease_id in item.validity.lease_ids})

    scopes = list(principal.scopes)
    for item in inputs:
        scopes = _intersect_scope_sets(
            scopes, item.authority.scopes, is_subtype=subtype
        )

    longest_chain = max(
        (item.authority.delegation_chain for item in inputs),
        key=len,
        default=(),
    )
    delegation_chain = list(longest_chain)
    if not delegation_chain or delegation_chain[-1] != principal.principal_id:
        delegation_chain.append(principal.principal_id)

    if subject.kind == "action":
        if action_class is None or action_kappa is None or not math.isfinite(action_kappa) or action_kappa < 0:
            raise ValueError("Action warrant composition requires action class and computed kappa")
        kappa = action_kappa
    else:
        action_class = None
        kappa = max((item.consequence.kappa for item in inputs), default=0.0)

    provisional = {
        "tenant_id": principal.tenant_id,
        "subject": subject.model_dump(mode="json", exclude_none=True),
        "grounds": [item.model_dump(mode="json", exclude_none=True) for item in grounds],
        "status": status.value,
        "confidence": confidence,
        "validity": WarrantValidity(
            valid_from=valid_from,
            valid_to=valid_to,
            lease_ids=lease_ids,
        ).model_dump(mode="json", exclude_none=True),
        "authority": WarrantAuthority(
            principal_id=principal.principal_id,
            scopes=scopes,
            delegation_chain=delegation_chain,
        ).model_dump(mode="json", exclude_none=True),
        "consequence": WarrantConsequence(
            kappa=kappa,
            impact_run_id=impact_run_id or (
                max(inputs, key=lambda item: item.consequence.kappa).consequence.impact_run_id
                if inputs
                else None
            ),
            action_class=action_class,
        ).model_dump(mode="json", exclude_none=True),
        "operator": WarrantOperator.model_validate({
            "operator_id": operator.operator_id,
            "class": operator.operator_class,
            "version": operator.version,
        }).model_dump(mode="json", by_alias=True, exclude_none=True),
        "parents": [str(item.warrant_id) for item in inputs],
        "created_at": now.isoformat().replace("+00:00", "Z"),
        "schema_version": "1.0",
    }
    identity_digest = hashlib.sha256(rfc8785.dumps(provisional)).hexdigest()
    warrant_id = uuid5(NAMESPACE_URL, f"EOIP-WARRANT-v1:{identity_digest}")
    provisional["warrant_id"] = str(warrant_id)
    return Warrant.model_validate(provisional)