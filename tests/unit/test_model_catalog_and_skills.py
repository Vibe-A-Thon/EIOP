"""Model registry with signed offline bundles (SR-LLM-003) and prompt/skill registry (SR-LLM-006)."""

from __future__ import annotations

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from eoip.models.catalog import (
    ApprovalStatus,
    BundleRejected,
    LicenseTerms,
    ModelCatalog,
    ModelRecord,
    build_bundle,
)
from eoip.models.skills import RegressionCase, RegressionFailed, SensitivePromptContent, SkillRegistry

MODEL = {"model_id": "qwen-small-q4", "source": "hf://example/qwen-small", "weights_file": "model.gguf",
         "license": {"license_id": "custom-open-weight", "commercial_use": True, "commercial_redistribution": False,
                     "restrictions": ["no redistribution of weights"]},
         "intended_tasks": ["classification", "extraction"], "hardware_profile": "cpu-small",
         "eval_scores": {"intent_f1": 0.91, "extraction_em": 0.84}}


@pytest.fixture
def bundle(tmp_path):
    key = Ed25519PrivateKey.generate()
    (tmp_path / "model.gguf").write_bytes(b"\x00weights" * 100)
    (tmp_path / "tokenizer.json").write_text("{}")
    build_bundle(tmp_path, model=MODEL, private_key=key, publisher="eoip-models")
    return tmp_path, key


@pytest.mark.req("SR-LLM-003")
class TestModelCatalog:
    def test_signed_offline_bundle_imports_with_full_metadata_pending_approval(self, bundle):
        d, key = bundle
        cat = ModelCatalog(trusted_publishers={"eoip-models": key.public_key()}, min_eval_score=0.8)
        rec = cat.import_bundle(d)
        assert rec.source == MODEL["source"] and len(rec.sha256) == 64
        assert rec.license.commercial_redistribution is False and rec.license.restrictions
        assert rec.intended_tasks == ("classification", "extraction") and rec.hardware_profile == "cpu-small"
        assert rec.eval_scores["intent_f1"] == 0.91 and rec.approval is ApprovalStatus.PENDING
        assert cat.approved_for("classification") == []

    def test_tampered_untrusted_or_badly_signed_bundles_are_rejected(self, bundle, tmp_path_factory):
        d, key = bundle
        with pytest.raises(BundleRejected, match="not trusted"):
            ModelCatalog().import_bundle(d)
        other = Ed25519PrivateKey.generate().public_key()
        with pytest.raises(BundleRejected, match="signature"):
            ModelCatalog(trusted_publishers={"eoip-models": other}).import_bundle(d)
        cat = ModelCatalog(trusted_publishers={"eoip-models": key.public_key()})
        (d / "model.gguf").write_bytes(b"tampered")
        with pytest.raises(BundleRejected, match="hash mismatch"):
            cat.import_bundle(d)
        (d / "model.gguf").unlink()
        with pytest.raises(BundleRejected, match="file list"):
            cat.import_bundle(d)

    def test_approval_requires_eval_scores_and_a_license_that_permits_the_use(self, bundle):
        d, key = bundle
        cat = ModelCatalog(trusted_publishers={"eoip-models": key.public_key()}, min_eval_score=0.8)
        rec = cat.import_bundle(d)
        with pytest.raises(PermissionError, match="redistribution"):
            cat.approve(rec.model_id, approver="ml-lead", use="redistribution")
        cat.approve(rec.model_id, approver="ml-lead", use="commercial")
        assert [r.model_id for r in cat.approved_for("classification")] == ["qwen-small-q4"]
        low = cat.register(ModelRecord(model_id="weak", source="local", sha256="a" * 64,
                                       license=LicenseTerms("apache-2.0", True, True), intended_tasks=("synthesis",),
                                       hardware_profile="single-gpu", eval_scores={"qa": 0.5}))
        with pytest.raises(PermissionError, match="below"):
            cat.approve(low.model_id, approver="ml-lead")
        with pytest.raises(ValueError, match="sha256"):
            cat.register(ModelRecord(model_id="x", source="s", sha256="short", license=LicenseTerms("mit", True, True),
                                     intended_tasks=(), hardware_profile="cpu-small"))


SCHEMA = {"type": "object", "properties": {"label": {"type": "string"}}}


def _suite():
    return [RegressionCase({"text": "printer broken"}, lambda out: "printer broken" in out),
            RegressionCase({"text": "add dark mode"}, lambda out: "Classify" in out)]


@pytest.mark.req("SR-LLM-006")
class TestSkillRegistry:
    def test_versioned_prompt_schema_and_few_shot_with_regression_gate(self):
        reg = SkillRegistry()
        v1 = reg.add("triage", "Classify: {{text}}", SCHEMA, [("app crashes", '{"label":"bug"}')])
        assert reg.promote(v1, _suite()) == 1.0
        out = reg.render("triage", {"text": "printer broken"}, tenant_id="t1")
        assert out.startswith("Input: app crashes") and out.endswith("Classify: printer broken")
        v2 = reg.add("triage", "Label it: {{text}}", SCHEMA)  # regresses the 'Classify' case
        with pytest.raises(RegressionFailed):
            reg.promote(v2, _suite())
        assert reg.resolve("triage", tenant_id="t1").version == 1
        with pytest.raises(RegressionFailed, match="required"):
            reg.promote(v2, [])
        assert v1.fingerprint != v2.fingerprint and v1.output_schema == SCHEMA

    def test_ab_split_is_deterministic_and_tenant_overrides_win(self):
        reg = SkillRegistry()
        reg.promote(reg.add("triage", "Classify: {{text}}", SCHEMA), _suite())
        reg.add("triage", "Classify carefully: {{text}}", SCHEMA)
        reg.start_ab("triage", 1, 2, 0.5)
        picks = {reg.resolve("triage", tenant_id="t1", request_id=f"r{i}").version for i in range(40)}
        assert picks == {1, 2}
        assert reg.resolve("triage", tenant_id="t1", request_id="r7").version == reg.resolve(
            "triage", tenant_id="t1", request_id="r7").version
        assert reg.ab_result("triage")["winner"] is None  # no samples yet
        for _ in range(20):
            reg.record_outcome("triage", 1, 0.7)
            reg.record_outcome("triage", 2, 0.9)
        assert reg.ab_result("triage")["winner"] == 2
        ov = reg.add("triage", "Classify (acme rules): {{text}}", SCHEMA, tenant_id="acme")
        reg.promote(ov, _suite())
        assert reg.render("triage", {"text": "x"}, tenant_id="acme").startswith("Classify (acme rules)")
        assert reg.resolve("triage", tenant_id="other", request_id="r1").tenant_id is None

    def test_rendered_prompt_never_carries_raw_sensitive_data_unless_policy_allows(self):
        reg = SkillRegistry(raw_sensitive_allowed={"hr"})
        reg.promote(reg.add("triage", "Classify: {{text}}", SCHEMA), _suite())
        with pytest.raises(SensitivePromptContent, match="EMAIL"):
            reg.render("triage", {"text": "from jane@corp.example"}, tenant_id="t1")
        assert "jane@corp.example" in reg.render("triage", {"text": "from jane@corp.example"}, tenant_id="hr")
