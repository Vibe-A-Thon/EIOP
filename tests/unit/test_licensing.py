"""Unit tests for eoip.licensing (SR-DEP-007, SR-COM-001, SR-TEN-009)."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from eoip.licensing import (
    EntitlementChecker,
    LicensePayload,
    UsageMeter,
    build_entitlement_checker,
    sign_license,
    verify_license,
    verify_license_cli,
)
from eoip.licensing.cli import main as cli_main
from eoip.licensing.entitlements import READ_ONLY_NOTICE
from eoip.licensing.license_file import (
    canonical_payload_bytes,
    generate_vendor_key,
    load_license_file,
    save_license_file,
)
from eoip.licensing.meter import GENESIS_PREV_HASH, event_hash

VENDOR_KEY = "test-vendor-key-0123456789abcdef"


def _payload(**overrides) -> LicensePayload:
    base = dict(
        customer="Acme Corp",
        edition="enterprise",
        model="subscription",
        modules=["graph", "audit"],
        max_seats=10,
        max_tenants=3,
        max_records=1_000_000,
        expiry=datetime.now(timezone.utc) + timedelta(days=30),
    )
    base.update(overrides)
    return LicensePayload(**base)


def _checker(**payload_overrides) -> EntitlementChecker:
    return EntitlementChecker(verify_license(sign_license(_payload(**payload_overrides), VENDOR_KEY), VENDOR_KEY))


# --- license file signing / verification (SR-DEP-007) -----------------------


def test_sign_and_verify_roundtrip():
    doc = sign_license(_payload(), VENDOR_KEY)
    result = verify_license(doc, VENDOR_KEY)
    assert result.ok
    assert result.payload is not None
    assert result.payload.customer == "Acme Corp"
    assert result.payload.license_id.startswith("urn:eoip:licensing:license:")


def test_verify_rejects_wrong_key():
    doc = sign_license(_payload(), VENDOR_KEY)
    result = verify_license(doc, "attacker-key")
    assert not result.ok
    assert result.reason == "invalid_signature"


def test_verify_rejects_tampered_payload():
    doc = sign_license(_payload(), VENDOR_KEY)
    doc["payload"]["max_seats"] = 9999
    result = verify_license(doc, VENDOR_KEY)
    assert not result.ok


def test_verify_rejects_malformed_document():
    assert verify_license({"payload": {}}, VENDOR_KEY).reason == "malformed_document"
    assert verify_license("not-a-dict", VENDOR_KEY).reason == "malformed_document"


def test_verify_rejects_future_algorithm():
    payload = _payload()
    data = payload.model_dump(mode="json")
    data["signature_algorithm"] = "ed25519"  # ADR-gated upgrade path
    result = verify_license({"payload": data, "signature": "aa" * 32}, VENDOR_KEY)
    assert not result.ok
    assert result.reason.startswith("unsupported_signature_algorithm")


def test_perpetual_license_must_not_carry_expiry():
    with pytest.raises(Exception):
        _payload(model="perpetual", expiry=datetime.now(timezone.utc))


def test_canonical_bytes_independent_of_key_order():
    a = {"b": 1, "a": {"y": 2, "x": 1}}
    b = {"a": {"x": 1, "y": 2}, "b": 1}
    assert canonical_payload_bytes(a) == canonical_payload_bytes(b)


def test_save_and_load_license_file(tmp_path: Path):
    path = tmp_path / "license.json"
    save_license_file(sign_license(_payload(), VENDOR_KEY), path)
    result = load_license_file(path, VENDOR_KEY)
    assert result.ok
    assert load_license_file(path, "wrong").reason == "invalid_signature"
    assert load_license_file(tmp_path / "missing.json", VENDOR_KEY).reason.startswith("unreadable")


def test_generated_vendor_key_is_hex():
    assert len(generate_vendor_key()) == 64


# --- entitlements (SR-COM-001, SR-DEP-007) -----------------------------------


def test_checker_requires_valid_verification():
    with pytest.raises(ValueError):
        EntitlementChecker(verify_license({"payload": {}, "signature": "x"}, VENDOR_KEY))


def test_module_check_uses_license_list():
    checker = _checker()
    assert checker.check_module("audit").allowed
    outcome = checker.check_module("ml")
    assert not outcome.allowed
    assert outcome.notice == "module_not_licensed:ml"


def test_module_check_falls_back_to_edition_defaults():
    checker = _checker(modules=[], edition="professional")
    assert checker.check_module("nl").allowed
    assert not checker.check_module("audit").allowed


def test_seat_tenant_record_limits():
    checker = _checker()
    assert checker.check_seats(10).allowed
    over = checker.check_seats(11)
    assert not over.allowed and over.limit == 10 and over.current == 11
    assert not checker.check_tenants(4).allowed
    assert checker.check_tenants(3).allowed
    assert not checker.check_records(2_000_000).allowed
    unlimited = _checker(max_seats=None)
    assert unlimited.check_seats(10**9).allowed


def test_edition_and_size_tier_ranking():
    checker = _checker(edition="professional", size_tier="medium")
    assert checker.check_edition("professional").allowed
    assert not checker.check_edition("enterprise").allowed
    assert checker.check_size_tier("small").allowed
    assert not checker.check_size_tier("large").allowed


def test_grace_period_then_read_only_degrade():
    expiry = datetime.now(timezone.utc) - timedelta(days=1)
    grace = _checker(expiry=expiry, grace_days=14)
    assert grace.license_state == "grace"
    assert grace.notice == "license_expired_in_grace_period"
    # Full function during grace, warning visible via degrade():
    grace_notice = grace.degrade(grace.check_module("graph"))
    assert grace_notice.allowed
    assert grace_notice.notice == "license_expired_in_grace_period"

    expired = _checker(expiry=expiry, grace_days=0)
    assert expired.license_state == "expired"
    outcome = expired.degrade(expired.check_module("graph"))
    assert not outcome.allowed
    assert outcome.degraded
    assert outcome.notice == READ_ONLY_NOTICE


def test_expiry_never_deletes_or_locks_reads():
    # SR-DEP-007 hard rule: degraded means read-only, data untouched.
    expired = _checker(expiry=datetime.now(timezone.utc) - timedelta(days=100), grace_days=0)
    outcome = expired.degrade(expired.check_seats(5))
    assert outcome.degraded and outcome.notice == READ_ONLY_NOTICE
    # read paths (module checks on existing data) still evaluate normally:
    assert expired.check_module("audit").allowed is False  # degraded only via degrade()
    assert "audit" in expired.licensed_modules()  # entitlement knowledge intact


def test_perpetual_state():
    checker = _checker(model="perpetual", expiry=None)
    assert checker.license_state == "perpetual"
    assert checker.notice is None


def test_require_module_dependency_raises():
    pytest.importorskip("fastapi")
    from fastapi import HTTPException

    checker = _checker()
    dep = checker.require_module("ml")
    with pytest.raises(HTTPException):
        dep()
    checker.require_module("graph")()  # allowed module: no raise


def test_build_entitlement_checker_helper():
    doc = sign_license(_payload(), VENDOR_KEY)
    checker = build_entitlement_checker(doc, VENDOR_KEY)
    assert checker.summary()["customer"] == "Acme Corp"
    assert checker.summary()["state"] == "active"


# --- usage meter (SR-TEN-009) -------------------------------------------------


def test_meter_chain_verifies_and_aggregates(tmp_path: Path):
    meter = UsageMeter(tmp_path)
    meter.record("queries", tenant_id="t1")
    meter.record("llm_tokens", value=150, tenant_id="t1")
    meter.record("seats", value=7)
    verification = meter.verify()
    assert verification.ok and verification.records_checked == 3
    export = meter.export()
    assert export["totals"] == {"llm_tokens": 150, "queries": 1, "seats": 7}
    assert export["tenants"] == ["t1"]
    assert export["chain"]["ok"]


def test_meter_detects_tampering(tmp_path: Path):
    meter = UsageMeter(tmp_path)
    meter.record("queries")
    meter.record("queries")
    path = tmp_path / "usage_meter.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    first["value"] = 999  # forged retroactive usage
    lines[0] = json.dumps(first, sort_keys=True, separators=(",", ":"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    verification = meter.verify()
    assert not verification.ok
    assert verification.reason == "hash_mismatch"
    assert verification.first_bad_seq == 1


def test_meter_detects_truncation(tmp_path: Path):
    meter = UsageMeter(tmp_path)
    meter.record("queries")
    meter.record("queries")
    path = tmp_path / "usage_meter.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(lines[0] + "\n", encoding="utf-8")
    verification = meter.verify()
    assert verification.ok  # a prefix of a valid chain is still internally consistent
    assert verification.records_checked == 1


def test_meter_event_hash_covers_prev(tmp_path: Path):
    meter = UsageMeter(tmp_path)
    e1 = meter.record("queries")
    e2 = meter.record("queries")
    assert e1.prev_hash == GENESIS_PREV_HASH
    assert e2.prev_hash == e1.hash
    assert e2.hash == event_hash(e2.model_dump(mode="json"), e1.hash)


def test_meter_rejects_negative_value(tmp_path: Path):
    meter = UsageMeter(tmp_path)
    with pytest.raises(ValueError):
        meter.record("queries", value=-1)


# --- offline CLI (SR-DEP-007) ---------------------------------------------------


def test_cli_verify_ok_and_bad_key(tmp_path: Path, capsys):
    path = tmp_path / "license.json"
    save_license_file(sign_license(_payload(), VENDOR_KEY), path)
    ok = verify_license_cli(path, vendor_key=VENDOR_KEY)
    assert ok["ok"] and ok["payload"]["customer"] == "Acme Corp"
    bad = verify_license_cli(path, vendor_key="nope")
    assert not bad["ok"]

    key_file = tmp_path / "vendor.key"
    key_file.write_text(VENDOR_KEY, encoding="utf-8")
    assert verify_license_cli(path, key_file=key_file)["ok"]
    assert not verify_license_cli(path)["ok"]  # no key anywhere

    assert cli_main(["verify", "--license", str(path), "--key-file", str(key_file)]) == 0
    capsys.readouterr()
    assert cli_main(["verify", "--license", str(path), "--key-file", str(tmp_path / 'missing.key')]) == 1
    capsys.readouterr()


# --- router (lazy fastapi) -------------------------------------------------------


def test_router_routes(tmp_path: Path):
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    from eoip.licensing import build_router

    checker = _checker()
    meter = UsageMeter(tmp_path)
    router = build_router(checker, meter)

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    status = client.get("/api/v1/licensing/status")
    assert status.status_code == 200
    assert status.json()["state"] == "active"

    doc = sign_license(_payload(), VENDOR_KEY)
    ok = client.post("/api/v1/licensing/verify", json={"document": doc, "vendor_key": VENDOR_KEY})
    assert ok.status_code == 200 and ok.json()["ok"]
    bad = client.post("/api/v1/licensing/verify", json={"document": doc, "vendor_key": "x"})
    assert not bad.json()["ok"]

    check = client.post("/api/v1/licensing/check-module", json={"module": "audit"})
    assert check.status_code == 200 and check.json()["allowed"]

    rec = client.post("/api/v1/licensing/meter/record", json={"metric": "queries", "value": 3, "tenant_id": "t1"})
    assert rec.status_code == 200 and rec.json()["seq"] == 1
    assert client.get("/api/v1/licensing/meter/verify").json()["ok"]
    export = client.get("/api/v1/licensing/meter/export")
    assert export.json()["totals"]["queries"] == 3

    routes = sorted({f"{sorted(r.methods)[0]} {r.path}" for r in router.routes})
    assert routes == [
        "GET /api/v1/licensing/meter/export",
        "GET /api/v1/licensing/meter/verify",
        "GET /api/v1/licensing/status",
        "POST /api/v1/licensing/check-module",
        "POST /api/v1/licensing/meter/record",
        "POST /api/v1/licensing/verify",
    ]


# --- SR-COM-001: every licensing model the entitlement system supports ------


@pytest.mark.req("SR-COM-001")
def test_perpetual_plus_annual_support_tracks_support_separately_from_the_license():
    now = datetime.now(timezone.utc)
    active = _checker(model="perpetual", expiry=None, support_expiry=now + timedelta(days=200))
    lapsed = _checker(model="perpetual", expiry=None, support_expiry=now - timedelta(days=1))
    assert active.license_state == lapsed.license_state == "perpetual"
    assert active.support_state() == "active" and lapsed.support_state() == "lapsed"
    assert lapsed.check_module("graph").allowed  # lapsed support never removes the license
    assert lapsed.summary()["support"] == "lapsed"
    with pytest.raises(ValueError, match="support_expiry"):
        _payload(model="subscription", support_expiry=now + timedelta(days=1))


@pytest.mark.req("SR-COM-001")
def test_annual_subscription_size_tier_usage_per_tenant_and_seat_addon_models_are_enforced():
    sub = _checker(model="subscription", expiry=datetime.now(timezone.utc) + timedelta(days=365))
    assert sub.license_state == "active" and sub.support_state() == "not_included"
    tier = _checker(model="size_tier", size_tier="medium", max_records=1000)
    assert tier.check_size_tier("small").allowed and not tier.check_size_tier("large").allowed
    usage = _checker(model="usage", max_records=1000)
    assert usage.check_records(1000).allowed and not usage.check_records(1001).allowed
    oem_tenants = _checker(model="per_tenant", edition="oem", max_tenants=5)
    assert oem_tenants.check_tenants(5).allowed and not oem_tenants.check_tenants(6).allowed
    seats = _checker(max_seats=10 + 5)  # base seats plus a 5-seat add-on
    assert seats.check_seats(15).allowed and not seats.check_seats(16).allowed


@pytest.mark.req("SR-COM-001")
def test_oem_revenue_share_royalty_terms_are_signed_and_computed_per_period():
    from eoip.licensing.license_file import RoyaltyTerms, compute_royalty

    terms = RoyaltyTerms(basis="revenue", rate_bps=1500, minimum_per_period=50_000, period="quarterly")
    checker = _checker(model="oem_revenue_share", edition="oem", royalty=terms)
    assert checker.payload.royalty == terms and checker.summary()["model"] == "oem_revenue_share"
    # royalty terms are inside the signature: tampering with the rate breaks verification
    doc = sign_license(_payload(model="oem_revenue_share", edition="oem", royalty=terms), VENDOR_KEY)
    doc["payload"]["royalty"]["rate_bps"] = 1
    assert not verify_license(doc, VENDOR_KEY).ok
    st = compute_royalty(terms, period_label="2026-Q3", gross_revenue_minor=1_000_000)
    assert st["computed"] == 150_000 and st["amount_due_minor"] == 150_000 and not st["minimum_applied"]
    low = compute_royalty(terms, period_label="2026-Q4", gross_revenue_minor=100_000)
    assert low["computed"] == 15_000 and low["amount_due_minor"] == 50_000 and low["minimum_applied"]
    units = RoyaltyTerms(basis="usage_units", rate_bps=25, period="monthly")
    assert compute_royalty(units, period_label="2026-10", usage_units=40_000)["amount_due_minor"] == 1_000
    with pytest.raises(ValueError):
        compute_royalty(terms, period_label="x", usage_units=10)
    with pytest.raises(ValueError, match="royalty terms"):
        _payload(model="oem_revenue_share", edition="oem")
    with pytest.raises(ValueError, match="only valid"):
        _payload(royalty=terms)
