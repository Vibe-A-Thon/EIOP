"""Unit tests for the egress gateway (SR-LLM-010..020, SR-CON-010/011).

No real network calls: every test injects a stub transport.
"""

from __future__ import annotations

import time

import pytest

from eoip.egress import (
    ApprovalRequirement,
    BudgetExhausted,
    CanaryRegistry,
    ConsentRecord,
    DataFlowManifest,
    DlpScanner,
    EgressDenied,
    EgressGateway,
    EndpointConfig,
    PolicyEngine,
    PolicyRule,
    ServiceProviderManifest,
    SharingLevel,
    TokenVault,
    TransformError,
    aggregate,
    redact,
    schema_strip,
    synthetic,
    tokenize,
    transform,
)

CONSENT = dict(
    consent_id="urn:eoip:egress:consent:test1",
    endpoint_id="ext-eu",
    signer="admin@tenant.example",
    signed_at=0.0,
    dpa_ref="DPA-2026-17",
    residency_region="EU",
    scope="summarize D0/D1",
)


def make_gateway(*, rules=None, transport=None, audit=None, canaries=None):
    gw = EgressGateway(
        tenant_id="t1",
        policy=PolicyEngine(rules=rules),
        transport=transport or (lambda payload, endpoint: {"echo": payload}),
        audit=audit or (lambda event: None),
        canaries=canaries or CanaryRegistry(),
    )
    gw.register_endpoint(EndpointConfig(
        id="ext-eu", kind="chat", url_allowlist=["https://llm.example.eu"],
        region="EU", dpa_ref="DPA-2026-17",
    ))
    return gw


def enable(gw, admin="admin@tenant.example"):
    gw.enable_endpoint("ext-eu", admin=admin, consent=ConsentRecord(**CONSENT))


# ---------------------------------------------------------------------------
# SR-LLM-010/017 — disabled by default, admin enable with consent + audit
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-010", "SR-LLM-017")
class TestEnablement:
    def test_disabled_by_default_denies(self):
        gw = make_gateway()
        with pytest.raises(EgressDenied, match="disabled"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"])

    def test_enable_without_consent_rejected(self):
        gw = make_gateway()
        with pytest.raises(ValueError, match="consent"):
            gw.enable_endpoint("ext-eu", admin="a", consent=ConsentRecord(
                consent_id="c", endpoint_id="other", signer="s", signed_at=0.0))

    def test_enable_emits_audit(self):
        events = []
        gw = make_gateway(audit=events.append)
        enable(gw)
        assert events[0]["event"] == "egress.endpoint_enabled"
        assert events[0]["consent_id"] == CONSENT["consent_id"]
        assert events[0]["dpa_ref"] == "DPA-2026-17"
        assert events[0]["region"] == "EU"

    @pytest.mark.req("SR-LLM-017")
    def test_changed_contract_terms_require_reapproval_before_any_call(self):
        events = []
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S1)], audit=events.append)
        enable(gw)
        call = dict(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"], dry_run=True)
        gw.call(**call)
        assert gw.amend_consent("ext-eu", admin="a", residency_region="US") is True
        assert events[-1]["event"] == "egress.consent_changed_reapproval_required"
        assert events[-1]["changes"] == ["residency_region"]
        with pytest.raises(EgressDenied, match="disabled"):
            gw.call(**call)
        assert gw.amend_consent("ext-eu", admin="a", scope=CONSENT["scope"]) is False  # no change
        renewed = dict(CONSENT, consent_id="urn:eoip:egress:consent:test2", residency_region="US", signed_at=1.0)
        gw.enable_endpoint("ext-eu", admin="a", consent=ConsentRecord(**renewed))
        gw.call(**call)
        assert [c.consent_id for c in gw.consent_history["ext-eu"]] == [CONSENT["consent_id"], renewed["consent_id"]]
        assert "ext-eu" not in gw.reapproval_required

    def test_consent_dpa_mismatch_rejected(self):
        gw = make_gateway()
        bad = dict(CONSENT, dpa_ref="DPA-WRONG")
        with pytest.raises(ValueError, match="DPA"):
            gw.enable_endpoint("ext-eu", admin="a", consent=ConsentRecord(**bad))


# ---------------------------------------------------------------------------
# SR-LLM-011 — policy matrix: most-restrictive-wins, default deny
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-011")
class TestPolicy:
    def test_default_deny_s0(self):
        gw = make_gateway()
        enable(gw)
        with pytest.raises(EgressDenied, match="default deny"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D2"])

    def test_most_restrictive_wins(self):
        rules = [
            PolicyRule(rule_id="r1", classes=["D0"], tasks=["summarize"],
                       max_level=SharingLevel.S7),
            PolicyRule(rule_id="r2", max_level=SharingLevel.S1),
        ]
        gw = make_gateway(rules=rules)
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"note": "hello"}, user_id="u1", role="analyst",
                         data_classes=["D0"], dry_run=True)
        assert result["manifest"].level == 1  # S1 beats S7
        assert result["manifest"].matched_rule_ids == ["r1", "r2"]

    def test_d4_restricted_class_denied(self):
        rules = [PolicyRule(rule_id="r1", max_level=SharingLevel.S7)]
        gw = make_gateway(rules=rules)
        enable(gw)
        with pytest.raises(EgressDenied, match="default deny"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="admin", data_classes=["D4"])

    def test_sensitive_tags_cap_s1(self):
        rules = [PolicyRule(rule_id="r1", max_level=SharingLevel.S7)]
        gw = make_gateway(rules=rules)
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"ssn": "123-45-6789"}, user_id="u1",
                         role="admin", data_classes=["D2"], tags=["PII"],
                         dry_run=True)
        assert result["manifest"].level == 1

    def test_role_scoped_rule(self):
        rules = [PolicyRule(rule_id="r1", classes=["D3"], tasks=["report_narration"],
                            roles=["analyst"], max_level=SharingLevel.S4)]
        gw = make_gateway(rules=rules)
        enable(gw)
        ok = gw.call(endpoint_id="ext-eu", task="report_narration",
                     payload={"fact": "internal"}, user_id="u1", role="analyst",
                     data_classes=["D3"], dry_run=True)
        assert ok["manifest"].level == 4
        with pytest.raises(EgressDenied):
            gw.call(endpoint_id="ext-eu", task="report_narration",
                    payload={"fact": "internal"}, user_id="u1", role="viewer",
                    data_classes=["D3"])


# ---------------------------------------------------------------------------
# SR-LLM-011/015 — transforms
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-011", "SR-LLM-015")
class TestTransforms:
    payload = {"name": "Alice", "age": 34,
               "notes": ["call Alice", "review"], "meta": {"dept": "eng"}}

    def test_s0_raises(self):
        with pytest.raises(TransformError):
            transform(self.payload, SharingLevel.S0)

    def test_s1_schema_strip(self):
        out = schema_strip(self.payload)
        assert set(out) == set(self.payload)
        assert all(set(v) == {"type"} for v in out.values())
        assert "Alice" not in str(out)

    def test_s2_aggregate_small_cell_suppression(self):
        out = aggregate({"items": ["a", "a", "b", "c", "d", "e"], "n": 3}, k=2)
        assert out["items"]["count"] == 6
        assert out["items"]["suppressed_cells"] == 4  # "a" count 2 >= k, others suppressed
        assert out["n"] == {"type": "number", "count": 1}

    def test_s3_synthetic_shape(self):
        out = synthetic(self.payload)
        assert isinstance(out["name"], str) and out["name"].startswith("syn_")
        assert isinstance(out["age"], int)
        assert isinstance(out["notes"], list) and len(out["notes"]) == 2
        assert isinstance(out["meta"], dict) and "dept" in out["meta"]
        assert "Alice" not in str(out)

    def test_s4_tokenize_reversible(self):
        vault = TokenVault("t", b"secret")
        out = tokenize(self.payload, vault)
        assert out["name"] != "Alice" and out["name"].startswith("tok_")
        assert vault.detokenize(out["name"]) == "Alice"
        assert vault.detokenize(out["meta"]["dept"]) == "eng"

    def test_s5_redact(self):
        out = redact({"text": "email alice@example.com or call 555-123-4567",
                      "secret": "password=hunter2"})
        assert "[EMAIL]" in out["text"] and "[PHONE]" in out["text"]
        assert "hunter2" not in out["secret"]

    def test_s6_s7_passthrough(self):
        assert transform(self.payload, SharingLevel.S6) is self.payload
        assert transform(self.payload, SharingLevel.S7) is self.payload


# ---------------------------------------------------------------------------
# SR-LLM-012 — dry-run preview
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-012")
class TestDryRun:
    def test_dry_run_returns_exact_payload_no_transport(self):
        sent = []
        gw = make_gateway(
            rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S4)],
            transport=lambda p, e: sent.append(p) or {"ok": True},
        )
        enable(gw)
        payload = {"name": "Alice"}
        result = gw.call(endpoint_id="ext-eu", task="summarize", payload=payload,
                         user_id="u1", role="analyst", data_classes=["D2"],
                         dry_run=True)
        assert sent == []  # transport never invoked
        assert result["dry_run"] is True
        assert result["manifest"].dry_run is True
        assert result["payload"] != payload          # tokenized
        assert result["payload"]["name"].startswith("tok_")
        assert gw.vault.detokenize(result["payload"]["name"]) == "Alice"

    def test_s6_requires_approval(self):
        rules = [PolicyRule(rule_id="r1", classes=["D2"],
                            approval=ApprovalRequirement.PER_REQUEST,
                            max_level=SharingLevel.S6)]
        gw = make_gateway(rules=rules)
        enable(gw)
        with pytest.raises(EgressDenied, match="approval"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D2"])
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"a": "x"}, user_id="u1", role="analyst",
                         data_classes=["D2"], approval_id="apr-1", dry_run=True)
        assert result["manifest"].approval_id == "apr-1"
        assert result["payload"] == {"a": "x"}  # exact preview


# ---------------------------------------------------------------------------
# SR-LLM-013 — immutable manifests + report
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-013")
class TestManifest:
    @pytest.mark.req("SR-LLM-013")
    def test_manifest_records_endpoint_fields_and_vault_tokens_at_s4(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S4)])
        enable(gw)
        m = gw.call(endpoint_id="ext-eu", task="summarize", payload={"customer": "Jane Doe", "note": "hi"},
                    user_id="u1", role="analyst", data_classes=["D2"])["manifest"]
        assert m.level == 4 and m.endpoint_id == "ext-eu" and m.endpoint_region == "EU"
        assert m.fields == ["customer", "note"]
        assert len(m.tokens) == 2 and all(t.startswith("tok_") for t in m.tokens)
        assert "Jane Doe" not in str(m.tokens)

    @pytest.mark.req("SR-LLM-013")
    def test_recorded_manifest_is_immutable(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize", payload={"doc": "public"},
                         user_id="u1", role="analyst", data_classes=["D0"])
        m = result["manifest"]
        assert m is gw.manifests[-1]
        with pytest.raises(Exception):
            m.bytes_out = 0
        with pytest.raises(Exception):
            m.denied = True
        with pytest.raises(TypeError):
            m.fields.append("smuggled")
        with pytest.raises(TypeError):
            m.data_classes[0] = "D9"
        assert m.fields == ["doc"] and m.data_classes == ["D0"]
        with pytest.raises(EgressDenied):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"doc": "x"}, user_id="u1",
                    role="analyst", data_classes=["D0"], region="US")
        denied = gw.manifests[-1]
        assert denied.denied and "region" in denied.denial_reason
        with pytest.raises(Exception):
            denied.denied = False

    def test_manifest_fields_and_report(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"doc": "public report"}, user_id="u1",
                         role="analyst", data_classes=["D0"])
        m = result["manifest"]
        assert m.manifest_id.startswith("urn:eoip:egress:manifest:")
        assert m.user_id == "u1" and m.endpoint_region == "EU"
        assert m.data_classes == ["D0"] and m.level == 7
        assert m.bytes_out > 0 and m.bytes_in > 0
        assert len(m.response_hash) == 64
        report = gw.report()
        assert report["manifest_count"] == 1
        assert report["by_endpoint"] == {"ext-eu": 1}
        assert report["by_data_class"] == {"D0": 1}

    def test_denied_calls_recorded_not_in_report(self):
        gw = make_gateway()
        enable(gw)
        with pytest.raises(EgressDenied):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D2"])
        assert len(gw.manifests) == 1 and gw.manifests[0].denied
        assert gw.report()["manifest_count"] == 0


# ---------------------------------------------------------------------------
# SR-LLM-014 — DLP + canaries
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-014")
class TestDlpCanaries:
    def test_dlp_scan_detects_pii_and_secrets(self):
        scanner = DlpScanner(dictionary_terms=["ACME-INTERNAL"])
        findings = scanner.scan_text("contact alice@example.com key=abcdef")
        detectors = {f.detector for f in findings}
        assert "EMAIL" in detectors and "SECRET_ASSIGNMENT" in detectors
        assert scanner.scan_text("ACME-INTERNAL")[0].detector == "DICTIONARY"

    def test_high_entropy_detected(self):
        scanner = DlpScanner()
        findings = scanner.scan_text("value aB3xk9mp2vl8nq4wr7zt5yu1cd6fg0hjZZ9 here")
        assert any(f.detector == "HIGH_ENTROPY" for f in findings)

    def test_canary_blocks_egress_below_level(self):
        canaries = CanaryRegistry()
        canary = canaries.plant("CANARY-TOKEN-XYZ-12345")
        rules = [PolicyRule(rule_id="r1", max_level=SharingLevel.S7)]
        gw = make_gateway(rules=rules, canaries=canaries)
        enable(gw)
        with pytest.raises(EgressDenied, match="canary"):
            gw.call(endpoint_id="ext-eu", task="summarize",
                    payload={"note": "contains CANARY-TOKEN-XYZ-12345"},
                    user_id="u1", role="analyst", data_classes=["D0"])
        assert gw.manifests[-1].canary_blocked

    def test_canary_allowed_at_sufficient_level(self):
        canaries = CanaryRegistry()
        canaries.plant("CANARY-OK", min_level=5)
        rules = [PolicyRule(rule_id="r1", max_level=SharingLevel.S7)]
        gw = make_gateway(rules=rules, canaries=canaries)
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"note": "CANARY-OK"}, user_id="u1",
                         role="analyst", data_classes=["D0"], dry_run=True)
        assert result["manifest"].level == 7  # no block at S7 >= min_level 5

    def test_dlp_findings_recorded_on_manifest(self):
        rules = [PolicyRule(rule_id="r1", max_level=SharingLevel.S7)]
        gw = make_gateway(rules=rules)
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"text": "reach me at alice@example.com"},
                         user_id="u1", role="analyst", data_classes=["D0"],
                         dry_run=True)
        assert "EMAIL" in result["manifest"].dlp_findings


# ---------------------------------------------------------------------------
# SR-LLM-016 — kill switch + budgets + anomaly
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-016")
class TestKillSwitchBudgets:
    @pytest.mark.req("SR-LLM-016")
    def test_platform_kill_switch_stops_every_tenant_gateway(self):
        from eoip.egress import PlatformKillSwitch
        switch = PlatformKillSwitch()
        gws = []
        for tenant in ("t1", "t2"):
            gw = EgressGateway(tenant_id=tenant, policy=PolicyEngine(rules=[
                PolicyRule(rule_id="r1", max_level=SharingLevel.S7)]),
                transport=lambda payload, endpoint: {"echo": payload}, platform_kill_switch=switch)
            gw.register_endpoint(EndpointConfig(id="ext-eu", kind="chat", url_allowlist=["https://llm.example.eu"],
                                                region="EU", dpa_ref="DPA-2026-17"))
            enable(gw)
            gws.append(gw)
        switch.engage(admin="secops", reason="vendor incident")
        for gw in gws:
            with pytest.raises(EgressDenied, match="platform kill switch"):
                gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                        user_id="u1", role="analyst", data_classes=["D0"])
            assert gw.manifests[-1].denied
        with pytest.raises(ValueError):
            switch.release(admin="")
        switch.release(admin="secops")
        assert gws[0].call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                           user_id="u1", role="analyst", data_classes=["D0"])["response"]

    def test_default_gateways_share_the_platform_switch(self):
        from eoip.egress import PLATFORM_KILL_SWITCH
        assert make_gateway().platform_kill_switch is PLATFORM_KILL_SWITCH

    def test_global_kill_switch(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        enable(gw)
        gw.kill(admin="secops", reason="incident")
        with pytest.raises(EgressDenied, match="kill switch"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"])

    def test_per_endpoint_kill(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        enable(gw)
        gw.kill_endpoint("ext-eu", admin="secops")
        with pytest.raises(EgressDenied, match="endpoint kill"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"])

    def test_rate_budget(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        gw.rate_limit_per_window = 1
        enable(gw)
        gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                user_id="u1", role="analyst", data_classes=["D0"])
        with pytest.raises(BudgetExhausted):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"])

    def test_cost_budget(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        gw.cost_budget = 1.0
        enable(gw)
        gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                user_id="u1", role="analyst", data_classes=["D0"],
                estimated_cost=0.8)
        with pytest.raises(BudgetExhausted):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"],
                    estimated_cost=0.5)

    def test_anomaly_threshold_audits_and_blocks(self):
        events = []
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)],
                          audit=events.append)
        gw.anomaly_bytes_threshold = 10
        enable(gw)
        with pytest.raises(BudgetExhausted, match="anomaly"):
            gw.call(endpoint_id="ext-eu", task="summarize",
                    payload={"big": "x" * 100}, user_id="u1", role="analyst",
                    data_classes=["D0"])
        assert any(e.get("event") == "egress.anomaly" for e in events)


# ---------------------------------------------------------------------------
# SR-LLM-015 — response re-identification
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-015")
class TestVault:
    def test_response_tokens_reidentified(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S4)])
        enable(gw)
        gw.call(endpoint_id="ext-eu", task="summarize", payload={"name": "Alice"},
                user_id="u1", role="analyst", data_classes=["D2"], dry_run=True)
        token = gw.vault.export_index()["tokens"][0]["token"]
        result = gw.call(endpoint_id="ext-eu", task="summarize",
                         payload={"name": "Alice"}, user_id="u1", role="analyst",
                         data_classes=["D2"])
        # stub transport echoes tokens; display path re-identifies them
        assert result["response"]["echo"]["name"] == "Alice"
        assert token not in str(result["response"])

    @pytest.mark.req("SR-LLM-015")
    def test_model_response_is_scanned_and_redacted_before_display(self):
        events = []
        leaked = "contact leak@other.example, ssn 123-45-6789"

        def transport(payload, endpoint):
            return {"echo": payload, "text": leaked}

        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S4)], transport=transport,
                          audit=events.append)
        enable(gw)
        result = gw.call(endpoint_id="ext-eu", task="summarize", payload={"name": "Alice"},
                         user_id="u1", role="analyst", data_classes=["D2"])
        assert result["response"]["echo"]["name"] == "Alice"  # vault tokens are not treated as leaks
        assert "leak@other.example" not in str(result["response"])
        assert "123-45-6789" not in str(result["response"])
        assert "[REDACTED:EMAIL]" in result["response"]["text"]
        assert result["response_findings"] == ["EMAIL", "SSN"]
        assert any(e["event"] == "egress.response_redacted" for e in events)

    @pytest.mark.req("SR-LLM-015")
    def test_vault_keys_and_tokens_are_per_tenant(self):
        from eoip.egress.vault import TokenVault

        a, b = TokenVault("tenant-a", secret=b"same-local-secret"), TokenVault("tenant-b", secret=b"same-local-secret")
        assert a._key != b._key  # PBKDF2 salted with the tenant id
        token = a.tokenize("Alice", field="name")
        assert a.detokenize(token) == "Alice"
        assert b.reidentify_text(f"hello {token}") == f"hello {token}"  # other tenant cannot re-identify
        assert "Alice" not in str(a.export_index())  # plaintext never leaves the vault


# ---------------------------------------------------------------------------
# SR-LLM-018/019/020 — kinds, fallback notice, region pinning
# ---------------------------------------------------------------------------

class TestGatewayBehavior:
    @pytest.mark.req("SR-LLM-019")
    def test_fallback_notice_on_denial(self):
        gw = make_gateway()
        enable(gw)
        with pytest.raises(EgressDenied) as exc_info:
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D2"])
        assert "local model" in exc_info.value.fallback_notice

    @pytest.mark.req("SR-LLM-020")
    def test_region_pin_violation_denied(self):
        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S7)])
        enable(gw)
        with pytest.raises(EgressDenied, match="jurisdiction"):
            gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                    user_id="u1", role="analyst", data_classes=["D0"], region="US")
        ok = gw.call(endpoint_id="ext-eu", task="summarize", payload={"a": "x"},
                     user_id="u1", role="analyst", data_classes=["D0"], region="EU",
                     dry_run=True)
        assert ok["manifest"].level == 7

    @pytest.mark.req("SR-LLM-018")
    def test_endpoint_kinds_cover_all_egress(self):
        # SR-LLM-018: embeddings/OCR/speech/rerank/telemetry ride the same path
        rules = [PolicyRule(rule_id="r1", max_level=SharingLevel.S1)]
        for kind in ("chat", "embed", "ocr", "speech", "rerank", "telemetry"):
            gw = make_gateway(rules=rules)
            gw.register_endpoint(EndpointConfig(id=f"ep-{kind}", kind=kind, region="EU"))
            gw.enable_endpoint(f"ep-{kind}", admin="a", consent=ConsentRecord(
                consent_id="c", endpoint_id=f"ep-{kind}", signer="s",
                signed_at=0.0))
            result = gw.call(endpoint_id=f"ep-{kind}", task=kind,
                             payload={"vec": [1.0, 2.0]}, user_id="u1",
                             role="analyst", data_classes=["D1"], dry_run=True)
            assert result["manifest"].level == 1

    @pytest.mark.req("SR-LLM-010")
    def test_unknown_endpoint_raises(self):
        gw = make_gateway()
        with pytest.raises(KeyError):
            gw.call(endpoint_id="nope", task="x", payload={}, user_id="u",
                    role="r", data_classes=["D0"])


# ---------------------------------------------------------------------------
# SR-CON-010/011 — Service Provider plugins + Data-Flow manifest
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-CON-010", "SR-CON-011")
class TestProviderPlugins:
    def _manifest(self, crosses=True):
        return ServiceProviderManifest(
            id="urn:eoip:egress:provider:acme-llm",
            name="acme-llm", capability="llm_endpoint", provider="Acme",
            data_flow=DataFlowManifest(
                data_classes_sent=["D1", "D2"], data_classes_received=["D1"],
                tags=[], destinations=["https://llm.acme.example"],
                regions=["EU"], retention="zero_retention",
                crosses_boundary=crosses,
            ),
        )

    def test_manifest_validation(self):
        with pytest.raises(ValueError, match="capability"):
            self._manifest().model_copy(update={"capability": "bogus"}).model_validate(
                self._manifest().model_copy(update={"capability": "bogus"}).model_dump())
        with pytest.raises(ValueError, match="data classes"):
            DataFlowManifest(data_classes_sent=["D9"])

    def test_install_requires_consent_for_boundary_crossing(self):
        gw = make_gateway()
        gw.plugin_registry.submit(self._manifest(crosses=True))
        with pytest.raises(ValueError, match="consent"):
            gw.plugin_registry.install(
                "urn:eoip:egress:provider:acme-llm", approved_by="admin")
        record = gw.plugin_registry.install(
            "urn:eoip:egress:provider:acme-llm", approved_by="admin",
            consent_ref="DPA-2026-17 / admin@tenant.example / 2026-10-08")
        assert record.acknowledged_data_flow
        assert gw.plugin_registry.is_installed("urn:eoip:egress:provider:acme-llm")

    def test_non_crossing_plugin_installs_without_consent(self):
        gw = make_gateway()
        gw.plugin_registry.submit(self._manifest(crosses=False))
        record = gw.plugin_registry.install(
            "urn:eoip:egress:provider:acme-llm", approved_by="admin")
        assert record.approved_by == "admin"

    def test_data_flow_declaration_fields(self):
        m = self._manifest()
        df = m.data_flow
        assert df.data_classes_sent == ["D1", "D2"]
        assert df.regions == ["EU"]
        assert df.retention == "zero_retention"
        assert df.crosses_boundary is True


# ---------------------------------------------------------------------------
# Router smoke test (lazy FastAPI import)
# ---------------------------------------------------------------------------

@pytest.mark.req("SR-LLM-010")
class TestRouter:
    def test_build_router_routes(self):
        fastapi = pytest.importorskip("fastapi")
        from eoip.egress.router import build_router

        gw = make_gateway()
        router = build_router(gw)
        paths = sorted({r.path for r in router.routes})
        assert paths == [
            "/api/v1/egress/call",
            "/api/v1/egress/endpoints",
            "/api/v1/egress/endpoints/{endpoint_id}/consent",
            "/api/v1/egress/endpoints/{endpoint_id}/consent/amend",
            "/api/v1/egress/endpoints/{endpoint_id}/disable",
            "/api/v1/egress/endpoints/{endpoint_id}/enable",
            "/api/v1/egress/kill",
            "/api/v1/egress/manifests",
            "/api/v1/egress/plugins",
            "/api/v1/egress/plugins/install",
            "/api/v1/egress/plugins/submit",
            "/api/v1/egress/policy/rules",
            "/api/v1/egress/report",
        ]

    def test_end_to_end_via_testclient(self):
        pytest.importorskip("fastapi")
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from eoip.egress.router import build_router

        gw = make_gateway(rules=[PolicyRule(rule_id="r1", max_level=SharingLevel.S1)])
        app = FastAPI()
        app.include_router(build_router(gw))
        client = TestClient(app)

        rules = client.get("/api/v1/egress/policy/rules").json()
        assert rules["default_level"] == 0

        denied = client.post("/api/v1/egress/call", json={
            "endpoint_id": "ext-eu", "task": "summarize",
            "payload": {"a": "b"}, "user_id": "u1", "role": "analyst",
            "data_classes": ["D2"],
        })
        assert denied.status_code == 403
        assert "local model" in denied.json()["detail"]["fallback_notice"]

        client.post("/api/v1/egress/endpoints/ext-eu/enable", json={
            "endpoint_id": "ext-eu", "admin": "a", "signer": "s",
            "dpa_ref": "DPA-2026-17", "residency_region": "EU", "scope": "x",
        })
        ok = client.post("/api/v1/egress/call", json={
            "endpoint_id": "ext-eu", "task": "summarize",
            "payload": {"a": "b"}, "user_id": "u1", "role": "analyst",
            "data_classes": ["D2"], "dry_run": True,
        })
        assert ok.status_code == 200
        assert ok.json()["payload"] == {"a": {"type": "string"}}

    @pytest.mark.req("SR-LLM-017")
    def test_consent_record_routes_show_signer_terms_history_and_reapproval(self):
        pytest.importorskip("fastapi")
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from eoip.egress.router import build_router

        gw = make_gateway()
        app = FastAPI()
        app.include_router(build_router(gw))
        client = TestClient(app)
        assert client.get("/api/v1/egress/endpoints/nope/consent").status_code == 404
        assert client.get("/api/v1/egress/endpoints/ext-eu/consent").json()["current"] is None
        assert client.post("/api/v1/egress/endpoints/ext-eu/consent/amend",
                           json={"admin": "a", "scope": "y"}).status_code == 409
        client.post("/api/v1/egress/endpoints/ext-eu/enable", json={
            "endpoint_id": "ext-eu", "admin": "a", "signer": "dpo@tenant.example",
            "dpa_ref": "DPA-2026-17", "residency_region": "EU", "scope": "x",
        })
        rec = client.get("/api/v1/egress/endpoints/ext-eu/consent").json()
        assert rec["current"]["signer"] == "dpo@tenant.example" and rec["current"]["signed_at"] > 0
        assert (rec["current"]["dpa_ref"], rec["current"]["residency_region"], rec["current"]["scope"]) == (
            "DPA-2026-17", "EU", "x")
        amended = client.post("/api/v1/egress/endpoints/ext-eu/consent/amend", json={"admin": "a", "scope": "y"})
        assert amended.json() == {"endpoint_id": "ext-eu", "reapproval_required": True}
        rec = client.get("/api/v1/egress/endpoints/ext-eu/consent").json()
        assert rec["reapproval_required"] is True and len(rec["history"]) == 1
