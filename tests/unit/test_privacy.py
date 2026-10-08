"""Unit tests for privacy controls (SR-PRV-001..004, SR-PRV-006)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from eoip.privacy import (
    ClassificationEngine,
    ConsentRecord,
    ConsentRegistry,
    DataClass,
    DetectorKind,
    DetectorRule,
    ErasurePropagator,
    ExpiryAction,
    Purpose,
    RegionSet,
    ResidencyAspect,
    ResidencyPolicy,
    ResidencyValidator,
    RetainableRecord,
    RetentionEngine,
    RetentionPolicy,
    SensitivityLabel,
    locate_subject,
    propagate_labels,
    shannon_entropy,
)
from eoip.privacy.router import build_router
from pydantic import ValidationError

# ---------------------------------------------------------- classification ---

def test_classify_builtin_rules():
    engine = ClassificationEngine()
    result = engine.classify(
        {"user": {"email": "jane@example.com", "ssn": "123-45-6789"}},
        source_ref="src-1",
        tenant_id="t-1",
    )
    labels = {l.value for l in result.labels}
    assert {"PII"} <= labels
    paths = {f.field_path for f in result.fields}
    assert "user.email" in paths and "user.ssn" in paths


def test_classify_secret_and_phi_and_pci():
    engine = ClassificationEngine()
    result = engine.classify(
        {
            "config": "api_key: 'sk-live-abcdef1234567890'",
            "note": "patient diagnosis recorded",
            "card": "4111 1111 1111 1111",
        }
    )
    labels = {l.value for l in result.labels}
    assert "SECRET" in labels and "PHI" in labels and "PCI" in labels


def test_classify_entropy_detector():
    engine = ClassificationEngine()
    result = engine.classify({"token": "aB3xK9mQ2vL8pR4nT7wZ5cF"})
    assert SensitivityLabel.SECRET in result.labels


def test_customer_extensible_rule():
    engine = ClassificationEngine()
    engine.register(
        DetectorRule(
            name="codename",
            kind=DetectorKind.DICTIONARY,
            labels=[SensitivityLabel.EXPORT_CONTROLLED],
            terms=["project falcon"],
        )
    )
    result = engine.classify({"doc": "this covers project falcon"})
    assert SensitivityLabel.EXPORT_CONTROLLED in result.labels
    assert "codename" in result.fields[0].matched_by


def test_invalid_rule_rejected():
    with pytest.raises(ValidationError):
        DetectorRule(name="bad", kind=DetectorKind.PATTERN, labels=[SensitivityLabel.PII])
    with pytest.raises(ValueError):
        DetectorRule(name="badre", kind=DetectorKind.PATTERN, labels=[SensitivityLabel.PII], pattern="([").compile()


def test_labels_propagate_to_derived():
    engine = ClassificationEngine()
    result = engine.classify({"email": "a@b.co"}, source_ref="src-1")
    derived = propagate_labels(result, [{"ref": "emb-1", "kind": "embedding"}, {"ref": "doc-1", "sensitivity_labels": ["IP"]}])
    assert derived[0]["sensitivity_labels"] == ["PII"]
    assert derived[1]["sensitivity_labels"] == ["IP", "PII"]


def test_shannon_entropy():
    assert shannon_entropy("aaaaaaaa") == 0.0
    assert shannon_entropy("abcd") == pytest.approx(2.0)


# ------------------------------------------------------------------ dsar ---

class _FakeGraphStore:
    def __init__(self, vertices):
        self._vertices = vertices

    def find_vertex_by_property(self, label, key, value, limit=10, include_deleted=False):
        return [v for v in self._vertices if v["label"] == label and v["properties"].get(key) == value][:limit]

    def tombstone_vertex(self, canonical_id):
        return any(v["canonical_id"] == canonical_id for v in self._vertices)


class _FakeCaptures:
    def __init__(self, rows):
        self._rows = rows

    def find_by_subject(self, subject_id, tenant_id=None):
        return [r for r in self._rows if r.get("subject_id") == subject_id]


class _FakeDerived:
    def __init__(self, rows):
        self._rows = rows

    def find_by_source(self, source_ref, tenant_id=None):
        return [r for r in self._rows if r.get("source_ref") == source_ref]


def test_locate_subject_all_surfaces():
    store = _FakeGraphStore(
        [{"vid": "v1", "canonical_id": "urn:eoip:graph:entity:e1", "label": "Entity", "properties": {"email": "jane@example.com", "sensitivity_labels": ["PII"]}}]
    )
    captures = _FakeCaptures([{"ref": "cap-1", "kind": "ticket", "subject_id": "jane@example.com", "sensitivity_labels": ["PII"]}])
    derived = _FakeDerived([{"ref": "emb-1", "kind": "embedding", "source_ref": "jane@example.com"}])
    report = locate_subject(
        "jane@example.com",
        graph_store=store,
        raw_captures=captures,
        derived_registries=[derived],
    )
    surfaces = {h.surface for h in report.hits}
    assert surfaces == {"graph", "raw_capture", "derived"}
    assert "backups" in report.unsearched_surfaces
    assert report.surface_counts()["graph"] == 1


def test_erasure_propagation_with_proof():
    store = _FakeGraphStore(
        [{"vid": "v1", "canonical_id": "urn:eoip:graph:entity:e1", "label": "Entity", "properties": {"subject_id": "s-1"}}]
    )
    erased_refs: list[str] = []
    derived = _FakeDerived([{"ref": "emb-1", "kind": "embedding", "source_ref": "s-1"}])
    erasers = {"embedding": lambda ref, tenant: erased_refs.append(ref) or True}
    report = locate_subject("s-1", graph_store=store, derived_registries=[derived])
    proof = ErasurePropagator(graph_store=store, derived_erasers=erasers).erase(report)
    assert proof.tombstoned_refs == ["urn:eoip:graph:entity:e1"]
    assert proof.erased_derived_refs == ["emb-1"]
    assert proof.digest


def test_erasure_marks_unerasable():
    store = _FakeGraphStore([])
    derived = _FakeDerived([{"ref": "sum-1", "kind": "summary", "source_ref": "s-1"}])
    report = locate_subject("s-1", graph_store=store, derived_registries=[derived])
    proof = ErasurePropagator(graph_store=store).erase(report)
    assert proof.unerased_refs == ["sum-1"]


# -------------------------------------------------------------- retention ---

def _policy(**over):
    base = {
        "id": "urn:eoip:privacy:retention:default-raw",
        "data_class": DataClass.RAW_CAPTURE,
        "retain_days": 30,
    }
    base.update(over)
    return RetentionPolicy(**base)


def test_retention_specificity():
    engine = RetentionEngine([_policy()])
    engine.register(_policy(id="urn:eoip:privacy:retention:t1-raw", tenant_id="t-1", retain_days=7))
    old = (datetime.now(UTC) - timedelta(days=10)).isoformat()
    record = RetainableRecord(ref="r-1", data_class=DataClass.RAW_CAPTURE, tenant_id="t-1", ingested_at=old)
    decision = engine.decide(record)
    assert decision.expired and decision.policy_id == "urn:eoip:privacy:retention:t1-raw"


def test_retention_within_window_and_no_policy():
    engine = RetentionEngine([_policy()])
    recent = datetime.now(UTC).isoformat()
    ok = engine.decide(RetainableRecord(ref="r-1", data_class=DataClass.RAW_CAPTURE, ingested_at=recent))
    assert not ok.expired
    none = engine.decide(RetainableRecord(ref="r-2", data_class=DataClass.AUDIT, ingested_at=recent))
    assert none.policy_id == ""


def test_retention_legal_hold_suspends_expiry():
    engine = RetentionEngine([_policy(legal_hold=True)])
    old = (datetime.now(UTC) - timedelta(days=400)).isoformat()
    decision = engine.decide(RetainableRecord(ref="r-1", data_class=DataClass.RAW_CAPTURE, ingested_at=old))
    assert not decision.expired and "legal hold" in decision.reason


def test_retention_expiry_executor():
    engine = RetentionEngine([_policy(action=ExpiryAction.ANONYMIZE)])
    old = (datetime.now(UTC) - timedelta(days=60)).isoformat()
    executed: list[str] = []
    engine.run_expiry(
        [RetainableRecord(ref="r-1", data_class=DataClass.RAW_CAPTURE, ingested_at=old)],
        executor={"anonymize": lambda r: executed.append(r.ref)},
    )
    assert executed == ["r-1"]


def test_retention_urn_validation():
    with pytest.raises(ValidationError):
        _policy(id="retention-1")


# ---------------------------------------------------------------- consent ---

def _registry_with_purpose(**purpose_over):
    registry = ConsentRegistry()
    base = {"id": "urn:eoip:privacy:purpose:analytics", "code": "analytics"}
    base.update(purpose_over)
    registry.register_purpose(Purpose(**base))
    return registry


def _consent(granted, **over):
    base = {
        "id": "urn:eoip:privacy:consent:c-1",
        "tenant_id": "t-1",
        "subject_id": "sub-1",
        "purpose_code": "analytics",
        "granted": granted,
    }
    base.update(over)
    return ConsentRecord(**base)


def test_consent_grant_revoke_and_expiry():
    registry = _registry_with_purpose()
    assert not registry.allowed("sub-1", "analytics")
    registry.record(_consent(True))
    assert registry.allowed("sub-1", "analytics")
    registry.record(_consent(False))
    assert not registry.allowed("sub-1", "analytics")


def test_consent_expiration():
    registry = _registry_with_purpose()
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    registry.record(_consent(True, expires_at=past))
    assert not registry.allowed("sub-1", "analytics")


def test_purpose_without_consent_requirement():
    registry = _registry_with_purpose(requires_consent=False)
    assert registry.allowed("sub-1", "analytics")
    with pytest.raises(KeyError):
        registry.record(_consent(True, purpose_code="unknown"))


# -------------------------------------------------------------- residency ---

def _residency(**over):
    base = {
        "id": "urn:eoip:privacy:residency:t-1",
        "tenant_id": "t-1",
        "storage": RegionSet(allowed=["eu-west-1"]),
        "processing": RegionSet(allowed=["eu"]),
        "model_endpoints": RegionSet(allowed=["us"]),
    }
    base.update(over)
    return ResidencyPolicy(**base)


def test_residency_prefix_matching():
    policy = _residency()
    assert policy.allows(ResidencyAspect.STORAGE, "eu-west-1")
    assert not policy.allows(ResidencyAspect.STORAGE, "us-east-1")
    assert policy.allows(ResidencyAspect.PROCESSING, "eu-central-1")
    assert policy.allows(ResidencyAspect.MODEL_ENDPOINTS, "us-east-1")


def test_residency_deny_overlap_rejected():
    with pytest.raises(ValidationError):
        _residency(deny_regions=["eu-west-1"])


def test_residency_validator():
    validator = ResidencyValidator()
    validator.register(_residency())
    ok = validator.validate("t-1", {ResidencyAspect.STORAGE: "eu-west-1"})
    assert ok.valid
    bad = validator.validate("t-1", {ResidencyAspect.STORAGE: "ap-south-1", ResidencyAspect.PROCESSING: "eu-central-1"})
    assert not bad.valid and len(bad.violations) == 1 and bad.violations[0].aspect == ResidencyAspect.STORAGE


# --------------------------------------------------------------- router ---

def test_privacy_router_routes():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    store = _FakeGraphStore(
        [{"vid": "v1", "canonical_id": "urn:eoip:graph:entity:e1", "label": "Entity", "properties": {"email": "j@x.co"}}]
    )
    consent = _registry_with_purpose()
    consent.record(_consent(True))
    retention = RetentionEngine([_policy()])
    residency = ResidencyValidator()
    residency.register(_residency())

    app = FastAPI()
    app.include_router(
        build_router(consent=consent, retention=retention, residency=residency, graph_store=store, graph_labels=["Entity"])
    )
    client = TestClient(app)

    resp = client.post("/api/v1/privacy/classify", json={"payload": {"email": "j@x.co"}})
    assert resp.status_code == 200
    assert "PII" in resp.json()["labels"]

    resp = client.post("/api/v1/privacy/dsar/locate", json={"subject_id": "j@x.co"})
    assert resp.status_code == 200
    assert any(h["surface"] == "graph" for h in resp.json()["hits"])

    resp = client.get("/api/v1/privacy/consents/allowed", params={"subject_id": "sub-1", "purpose": "analytics", "tenant_id": "t-1"})
    assert resp.json()["allowed"] is True

    resp = client.post(
        "/api/v1/privacy/retention/evaluate",
        json={"records": [{"ref": "r-1", "data_class": "raw_capture", "ingested_at": "2020-01-01T00:00:00+00:00"}]},
    )
    assert resp.json()["decisions"][0]["expired"] is True

    resp = client.post(
        "/api/v1/privacy/residency/validate",
        json={"tenant_id": "t-1", "placements": {"storage": "eu-west-1"}},
    )
    assert resp.json()["valid"] is True
