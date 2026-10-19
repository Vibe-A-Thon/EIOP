"""Unit tests for cross-field warrant validation rules V-01..V-16 (T-105 / OBL-REVA-WK-004-01)."""

import pytest
from reva.core.errors import ValidationError
from reva.kernel.authority import Authority, ConfidenceBand, CoverageStatus, Epistemic
from reva.kernel.coverage import Coverage, CoverageReason
from reva.kernel.validation import ValidationContext, assert_valid, validate_warrant_body
from reva.kernel.warrant import (
    ArtifactSubject,
    Confidence,
    Limitation,
    Link,
    ProducerRef,
    RuntimeLocation,
    UrlLocation,
    ValidTime,
    WarrantBody,
)

pytestmark = pytest.mark.reva_depth("unit")


def make_valid_body(**overrides) -> WarrantBody:
    base = {
        "tenant_id": "tenant-test",
        "subject": ArtifactSubject(
            artifact_id="art1_" + "a" * 64,
            sha256="a" * 64,
            size_bytes=1024,
            media_type="application/java-archive",
            format="jar",
        ),
        "producer": ProducerRef(
            producer_id="prd1_" + "p" * 64,
            producer_type="extractor",
            name="test-producer",
            version="1.0.0",
            build_digest=None,
            key_id="key1_" + "k" * 64,
        ),
        "operation": "test.op",
        "predicate": "reva.pred.built_from_commit",
        "parameters": {"param": "val"},
        "statement": {"commit": "c" * 40},
        "raw_ref": None,
        "authority": Authority.SHIPPED_ARTIFACT,
        "epistemic_state": Epistemic.OBSERVED,
        "confidence": Confidence(band=ConfidenceBand.HIGH, score_bp=9000),
        "coverage": None,
        "locations": [],
        "limitations": [],
        "environment": None,
        "observed_at": "2026-10-18T10:00:00.000Z",
        "valid_time": ValidTime(**{"from": "2026-10-18T10:00:00.000Z", "to": None}),
        "links": [],
    }
    base.update(overrides)
    return WarrantBody(**base)


@pytest.mark.reva_obligation("OBL-REVA-WK-004-01")
@pytest.mark.reva_case("positive")
def test_valid_warrant_passes():
    body = make_valid_body()
    assert len(validate_warrant_body(body)) == 0
    assert_valid(body)


@pytest.mark.reva_obligation("OBL-REVA-WK-004-01")
@pytest.mark.reva_case("negative")
def test_rule_v01_violation():
    # model_inferred requires epistemic_state inferred
    body = make_valid_body(
        authority=Authority.MODEL_INFERRED,
        epistemic_state=Epistemic.OBSERVED,
    )
    v = validate_warrant_body(body)
    assert any(x.rule_id == "V-01" for x in v)


@pytest.mark.reva_obligation("OBL-REVA-WK-004-01")
@pytest.mark.reva_case("negative")
def test_rule_v04_violation():
    # exact band requires score_bp 10000
    body = make_valid_body(
        confidence=Confidence(band=ConfidenceBand.EXACT, score_bp=9999),
    )
    v = validate_warrant_body(body)
    assert any(x.rule_id == "V-04" for x in v)


@pytest.mark.reva_obligation("OBL-REVA-WK-004-01")
@pytest.mark.reva_case("negative")
def test_rule_v10_violation():
    # static authority cannot have runtime location
    body = make_valid_body(
        authority=Authority.SOURCE_CODE_STATIC,
        locations=[
            RuntimeLocation(
                environment_id="env-prod",
                service="svc-api",
                at="2026-10-18T10:00:00.000Z",
            )
        ],
    )
    v = validate_warrant_body(body)
    assert any(x.rule_id == "V-10" for x in v)


@pytest.mark.reva_obligation("OBL-REVA-WK-004-01")
@pytest.mark.reva_case("negative")
def test_rule_v13_violation():
    # valid_time.to must be >= valid_time.from
    body = make_valid_body(
        valid_time=ValidTime(**{"from": "2026-10-18T12:00:00.000Z", "to": "2026-10-18T10:00:00.000Z"}),
    )
    v = validate_warrant_body(body)
    assert any(x.rule_id == "V-13" for x in v)
