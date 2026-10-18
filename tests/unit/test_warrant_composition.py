from datetime import datetime, timezone
from uuid import uuid4

import pytest
from hypothesis import given, settings, strategies as st

from eoip.contracts.warrant import (
    Warrant,
    WarrantActionClass,
    WarrantAuthority,
    WarrantConsequence,
    WarrantGround,
    WarrantGroundKind,
    WarrantOperator,
    WarrantScope,
    WarrantStatus,
    WarrantSubject,
    WarrantSubjectKind,
    WarrantValidity,
)
from eoip.provenance.warrant_composition import (
    WarrantCompositionOperator,
    WarrantPrincipalAuthority,
    compose_warrant,
)
from eoip.provenance.warrant_order import minimum_warrant_status

NOW = datetime(2026, 10, 18, 12, tzinfo=timezone.utc)


def _warrant(
    *,
    status=WarrantStatus.OBSERVED,
    tenant_id="tenant-a",
    valid_from=datetime(2026, 10, 1, tzinfo=timezone.utc),
    valid_to=None,
    scopes=None,
    delegation_chain=None,
    confidence=0.9,
    kappa=0.0,
):
    return Warrant(
        warrant_id=uuid4(),
        tenant_id=tenant_id,
        subject=WarrantSubject(kind=WarrantSubjectKind.ASSERTION, ref="assertion-1"),
        grounds=[WarrantGround(kind=WarrantGroundKind.SOURCE_RECORD, id="source-1", version="v1")],
        status=status,
        confidence=confidence,
        validity=WarrantValidity(valid_from=valid_from, valid_to=valid_to, lease_ids=["lease-1"]),
        authority=WarrantAuthority(
            principal_id="principal-parent",
            scopes=scopes or [WarrantScope(action="read", resource_type="urn:Type", selector="*")],
            delegation_chain=delegation_chain or ["principal-parent"],
        ),
        consequence=WarrantConsequence(kappa=kappa, action_class=WarrantActionClass.READ_ONLY),
        operator=WarrantOperator.model_validate({
            "operator_id": "source-connector",
            "class": "OBSERVER",
            "version": "1",
        }),
        parents=[],
        created_at=NOW,
        schema_version="1.0",
    )


def _principal(scopes=None, *, tenant_id="tenant-a", has_subject_authority=False):
    return WarrantPrincipalAuthority(
        tenant_id=tenant_id,
        principal_id="principal-child",
        scopes=tuple(scopes or [WarrantScope(action="*", resource_type="*", selector="*")]),
        delegation_chain=("root",),
        has_subject_authority=has_subject_authority,
    )


@st.composite
def _composition_cases(draw):
    operator_class = draw(st.sampled_from(["OBSERVER", "COMPUTATION", "MODEL", "GENERATOR", "HUMAN"]))
    statuses = draw(st.lists(st.sampled_from(list(WarrantStatus)), max_size=4))
    actions = draw(st.lists(st.sampled_from(["*", "read", "write"]), min_size=len(statuses), max_size=len(statuses)))
    selectors = draw(
        st.lists(st.sampled_from(["*", "domain=payments", "region=west"]), min_size=len(statuses), max_size=len(statuses))
    )
    expiries = draw(
        st.lists(
            st.sampled_from([
                None,
                datetime(2026, 10, 20, tzinfo=timezone.utc),
                datetime(2026, 10, 21, tzinfo=timezone.utc),
            ]),
            min_size=len(statuses),
            max_size=len(statuses),
        )
    )
    principal_action = draw(st.sampled_from(["*", "read", "write"]))
    principal_selector = draw(st.sampled_from(["*", "domain=payments", "region=west"]))
    generator_status = draw(st.sampled_from(list(WarrantStatus)))
    return (
        operator_class,
        statuses,
        actions,
        selectors,
        expiries,
        principal_action,
        principal_selector,
        generator_status,
    )


@pytest.mark.req("REQ-WCA-001", "REQ-WCA-002", "REQ-WCA-003", "REQ-WCA-004")
def test_computation_takes_weakest_status_and_never_widens_scope_or_validity():
    observed = _warrant()
    predicted = _warrant(
        status=WarrantStatus.PREDICTED,
        valid_from=datetime(2026, 10, 5, tzinfo=timezone.utc),
        valid_to=datetime(2026, 10, 25, tzinfo=timezone.utc),
        scopes=[WarrantScope(action="read", resource_type="urn:SubType", selector="domain=payments")],
        delegation_chain=["root", "principal-parent"],
        confidence=0.7,
    )
    operator = WarrantCompositionOperator(
        operator_id="join",
        operator_class="COMPUTATION",
        version="1",
        approved=True,
    )
    principal = _principal([WarrantScope(action="*", resource_type="urn:Type", selector="*")])

    result = compose_warrant(
        operator,
        [observed, predicted],
        [],
        principal,
        subject=WarrantSubject(kind=WarrantSubjectKind.PROPOSITION, ref="claim-1"),
        now=NOW,
        is_subtype=lambda child, parent: child == "urn:SubType" and parent == "urn:Type",
    )

    assert result.status == WarrantStatus.PREDICTED
    assert result.confidence == 0.7
    assert result.validity.valid_from == datetime(2026, 10, 5, tzinfo=timezone.utc)
    assert result.validity.valid_to == datetime(2026, 10, 25, tzinfo=timezone.utc)
    assert result.validity.lease_ids == ["lease-1"]
    assert len(result.grounds) == 1
    assert [(scope.action, scope.resource_type, scope.selector) for scope in result.authority.scopes] == [
        ("read", "urn:SubType", "domain=payments")
    ]
    assert result.authority.delegation_chain == ["root", "principal-parent", "principal-child"]


@pytest.mark.req("REQ-WCA-001", "REQ-WCA-002", "REQ-WCA-003")
def test_empty_computation_is_unknown_and_scope_intersection_cannot_widen():
    operator = WarrantCompositionOperator(
        operator_id="compute", operator_class="COMPUTATION", version="1", approved=True
    )
    subject = WarrantSubject(kind=WarrantSubjectKind.PROPOSITION, ref="claim-2")
    principal = _principal([WarrantScope(action="write", resource_type="urn:Type", selector="*")])
    input_warrant = _warrant(scopes=[WarrantScope(action="read", resource_type="urn:Type", selector="*")])

    denied = compose_warrant(
        operator,
        [input_warrant],
        [],
        principal,
        subject=subject,
        now=NOW,
    )
    assert denied.authority.scopes == []

    empty = compose_warrant(operator, [], [], _principal(), subject=subject, now=NOW)
    assert empty.status == WarrantStatus.UNKNOWN
    repeated = compose_warrant(operator, [], [], _principal(), subject=subject, now=NOW)
    assert repeated.warrant_id == empty.warrant_id


@pytest.mark.req("REQ-WCA-001", "REQ-OPR-004")
def test_observer_requires_qualification_and_human_requires_subject_authority():
    subject = WarrantSubject(kind=WarrantSubjectKind.ASSERTION, ref="assertion-2")
    observer = WarrantCompositionOperator(
        operator_id="connector", operator_class="OBSERVER", version="1", approved=True
    )
    with pytest.raises(PermissionError, match="not qualified"):
        compose_warrant(observer, [], [], _principal(), subject=subject, now=NOW)

    qualified = observer.model_copy(update={"observer_qualified": True})
    observer_receipt = WarrantGround(kind=WarrantGroundKind.TOOL_RECEIPT, id="receipt-1", version="v1")
    observed = compose_warrant(
        qualified,
        [],
        [observer_receipt],
        _principal(),
        subject=subject,
        now=NOW,
    )
    assert observed.status == WarrantStatus.OBSERVED
    assert observed.confidence == 1.0
    assert observer_receipt in observed.grounds

    human = WarrantCompositionOperator(
        operator_id="reviewer", operator_class="HUMAN", version="1", approved=True
    )
    with pytest.raises(PermissionError, match="lacks authority"):
        compose_warrant(human, [], [], _principal(), subject=subject, now=NOW)


@pytest.mark.req("REQ-WCA-001", "REQ-WAR-001", "REQ-WAR-002")
def test_model_requires_calibrated_confidence_and_uses_status_order():
    operator = WarrantCompositionOperator(
        operator_id="model", operator_class="MODEL", version="m1", approved=True
    )
    inputs = [_warrant(status=WarrantStatus.OBSERVED)]
    subject = WarrantSubject(kind=WarrantSubjectKind.PROPOSITION, ref="prediction-1")
    with pytest.raises(ValueError, match="calibrated"):
        compose_warrant(operator, inputs, [], _principal(), subject=subject, now=NOW, model_confidence=0.9)

    result = compose_warrant(
        operator,
        inputs,
        [],
        _principal(),
        subject=subject,
        now=NOW,
        model_confidence=0.9,
        model_confidence_calibrated=True,
    )
    assert result.status == WarrantStatus.PREDICTED
    assert result.confidence == 0.9


@pytest.mark.req("REQ-WCA-001", "REQ-WAR-011")
def test_generator_requires_matching_sasi_result_and_operator_must_be_approved():
    generator = WarrantCompositionOperator(
        operator_id="generator", operator_class="GENERATOR", version="g1", approved=True
    )
    subject = WarrantSubject(kind=WarrantSubjectKind.PROPOSITION, ref="claim-1")
    with pytest.raises(ValueError, match="SASI result"):
        compose_warrant(generator, [], [], _principal(), subject=subject, now=NOW)

    rejected_operator = generator.model_copy(update={"approved": False})
    with pytest.raises(PermissionError, match="not approved"):
        compose_warrant(rejected_operator, [], [], _principal(), subject=subject, now=NOW)

    sasi_ground = WarrantGround(kind=WarrantGroundKind.MODEL_RUN, id="sasi-run-1", version="1")
    sasi_result = _warrant(
        status=WarrantStatus.GENERATED,
        valid_to=datetime(2026, 10, 20, tzinfo=timezone.utc),
    ).model_copy(update={"subject": subject, "grounds": [sasi_ground]})
    composed = compose_warrant(
        generator,
        [],
        [],
        _principal(),
        subject=subject,
        now=NOW,
        generator_result=sasi_result,
    )
    assert composed.status == WarrantStatus.GENERATED
    assert composed.grounds == [sasi_ground]
    assert composed.validity.valid_to == datetime(2026, 10, 20, tzinfo=timezone.utc)
    assert composed.validity.lease_ids == ["lease-1"]


@pytest.mark.req("REQ-WCA-001", "REQ-PLT-001")
def test_composition_rejects_cross_tenant_inputs():
    operator = WarrantCompositionOperator(
        operator_id="compute", operator_class="COMPUTATION", version="1", approved=True
    )
    with pytest.raises(ValueError, match="principal tenant"):
        compose_warrant(
            operator,
            [_warrant(tenant_id="tenant-b")],
            [],
            _principal(tenant_id="tenant-a"),
            subject=WarrantSubject(kind=WarrantSubjectKind.PROPOSITION, ref="claim-1"),
            now=NOW,
        )


@pytest.mark.req("REQ-WCA-001", "REQ-BRB-001")
def test_action_warrant_requires_trusted_action_class_and_kappa():
    operator = WarrantCompositionOperator(
        operator_id="compute", operator_class="COMPUTATION", version="1", approved=True
    )
    with pytest.raises(ValueError, match="computed kappa"):
        compose_warrant(
            operator,
            [],
            [],
            _principal(),
            subject=WarrantSubject(kind=WarrantSubjectKind.ACTION, ref="action-1"),
            now=NOW,
        )
    with pytest.raises(ValueError, match="computed kappa"):
        compose_warrant(
            operator,
            [],
            [],
            _principal(),
            subject=WarrantSubject(kind=WarrantSubjectKind.ACTION, ref="action-1"),
            now=NOW,
            action_class=WarrantActionClass.INTERNAL_WRITE,
            action_kappa=float("inf"),
            impact_run_id="impact-1",
        )

    action_warrant = compose_warrant(
        operator,
        [],
        [],
        _principal(),
        subject=WarrantSubject(kind=WarrantSubjectKind.ACTION, ref="action-1"),
        now=NOW,
        action_class=WarrantActionClass.INTERNAL_WRITE,
        action_kappa=4.5,
        impact_run_id="impact-1",
    )
    assert action_warrant.consequence.kappa == 4.5
    assert action_warrant.consequence.impact_run_id == "impact-1"


@pytest.mark.req("REQ-WCA-002", "REQ-WCA-003", "REQ-WCA-004")
@settings(max_examples=10_000, deadline=None, derandomize=True)
@given(case=_composition_cases())
def test_a1_status_authority_and_validity_properties(case):
    (
        operator_class,
        statuses,
        actions,
        selectors,
        expiries,
        principal_action,
        principal_selector,
        generator_status,
    ) = case
    input_scopes = [
        WarrantScope(action=action, resource_type="urn:Type", selector=selector)
        for action, selector in zip(actions, selectors)
    ]
    inputs = [
        _warrant(status=status, scopes=[scope], valid_to=expiry)
        for status, scope, expiry in zip(statuses, input_scopes, expiries)
    ]
    principal_scope = WarrantScope(
        action=principal_action,
        resource_type="urn:Type",
        selector=principal_selector,
    )
    operator = WarrantCompositionOperator(
        operator_id="property-operator",
        operator_class=operator_class,
        version="1",
        approved=True,
        observer_qualified=True,
        receipt_grounds=(WarrantGround(kind=WarrantGroundKind.TOOL_RECEIPT, id="property-receipt"),),
    )
    principal = _principal([principal_scope], has_subject_authority=True)
    subject = WarrantSubject(kind=WarrantSubjectKind.PROPOSITION, ref="property-claim")
    generator_result = None
    if operator_class == "GENERATOR":
        generator_result = _warrant(status=generator_status).model_copy(update={"subject": subject})

    result = compose_warrant(
        operator,
        inputs,
        [],
        principal,
        subject=subject,
        now=NOW,
        model_confidence=0.75,
        model_confidence_calibrated=True,
        generator_result=generator_result,
    )

    if operator_class == "OBSERVER":
        expected_status = WarrantStatus.OBSERVED
    elif operator_class == "HUMAN":
        expected_status = WarrantStatus.ATTESTED
    elif operator_class == "COMPUTATION":
        expected_status = minimum_warrant_status(statuses)
    elif operator_class == "MODEL":
        expected_status = minimum_warrant_status([*statuses, WarrantStatus.PREDICTED])
    else:
        expected_status = generator_status
    assert result.status == expected_status

    for output_scope in result.authority.scopes:
        for source_scope in [principal_scope, *input_scopes]:
            assert source_scope.action == "*" or output_scope.action == source_scope.action
            assert output_scope.resource_type == source_scope.resource_type
            assert source_scope.selector == "*" or source_scope.selector in output_scope.selector

    validity_inputs = [*inputs, *([generator_result] if generator_result is not None else [])]
    finite_expiries = [item.validity.valid_to for item in validity_inputs if item.validity.valid_to is not None]
    if finite_expiries:
        assert result.validity.valid_to is not None
        assert result.validity.valid_to <= min(finite_expiries)