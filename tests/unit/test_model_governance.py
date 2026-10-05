"""Tests for eoip.models.governance (§49, GAP-AGOV-012-adjacent)."""

from __future__ import annotations

import json

import pytest

from eoip.agents.evaluation import GoldenAgentCase
from eoip.models.governance import (
    EvaluationDataset,
    Feature,
    FeatureDisabled,
    FeatureDisabledReason,
    GovernancePolicy,
    HallucinationIncident,
    HallucinationIncidentLog,
    KillSwitch,
    ModelEntry,
    ModelHealth,
    ModelOutput,
    ModelRegistry,
    OutputClass,
    PromptTemplate,
    PromptTemplateRegistry,
    classify_model_output,
    hash_template,
)


def _entry(model_id: str = "llm-a", approved: bool = False) -> ModelEntry:
    return ModelEntry(
        model_id=model_id,
        version="1.0.0",
        provider="local",
        capabilities={"rag", "nlq"},
        approved=approved,
    )


class TestModelRegistry:
    def test_register_and_get(self):
        registry = ModelRegistry()
        registry.register(_entry())
        entry = registry.get("llm-a")
        assert entry is not None
        assert entry.urn == "urn:eoip:models:model:llm-a"

    def test_approved_list_add_check_remove(self):
        registry = ModelRegistry()
        registry.register(_entry())
        assert not registry.is_approved("llm-a")
        registry.approve("llm-a")
        assert registry.is_approved("llm-a")
        assert registry.approved_models() == ["llm-a"]
        registry.revoke("llm-a")
        assert not registry.is_approved("llm-a")
        assert registry.approved_models() == []

    def test_is_usable_requires_healthy(self):
        registry = ModelRegistry()
        registry.register(_entry(approved=True))
        assert not registry.is_usable("llm-a")  # unavailable by default
        registry.set_health("llm-a", ModelHealth.HEALTHY)
        assert registry.is_usable("llm-a")
        registry.set_health("llm-a", ModelHealth.DEGRADED)
        assert not registry.is_usable("llm-a")

    def test_remove(self):
        registry = ModelRegistry()
        registry.register(_entry())
        assert registry.remove("llm-a")
        assert not registry.remove("llm-a")
        assert registry.get("llm-a") is None

    def test_unknown_model_raises(self):
        registry = ModelRegistry()
        with pytest.raises(KeyError):
            registry.approve("nope")


class TestPromptTemplateRegistry:
    def test_register_computes_hash(self):
        registry = PromptTemplateRegistry()
        template = registry.register(PromptTemplate(
            name="summarize", version="1", template="Summarize {{text}}",
            variables=["text"],
        ))
        assert template.template_hash == hash_template("Summarize {{text}}")

    def test_new_version_deactivates_old(self):
        registry = PromptTemplateRegistry()
        registry.register(PromptTemplate(name="t", version="1", template="a"))
        registry.register(PromptTemplate(name="t", version="2", template="b"))
        assert registry.active_template("t").version == "2"
        assert not registry.get("t", "1").active

    def test_integrity_verification(self):
        registry = PromptTemplateRegistry()
        registry.register(PromptTemplate(name="t", version="1", template="a"))
        assert registry.verify_integrity("t", "1")
        template = registry.get("t", "1")
        template.template = "tampered"
        assert not registry.verify_integrity("t", "1")


class TestEvaluationDataset:
    def test_roundtrip_json(self, tmp_path):
        dataset = EvaluationDataset(
            dataset_id="golden-1",
            description="regression set",
            cases=[GoldenAgentCase(case_id="c1", agent_id="a1", goal="g")],
            minimum_pass_rate=0.75,
        )
        path = tmp_path / "dataset.json"
        dataset.to_json(path)
        loaded = EvaluationDataset.from_json(path)
        assert loaded.dataset_id == "golden-1"
        assert loaded.cases[0].case_id == "c1"
        assert loaded.minimum_pass_rate == 0.75
        assert loaded.urn == "urn:eoip:models:dataset:golden-1"

    def test_run_regression_uses_agents_evaluation(self, tmp_path):
        dataset = EvaluationDataset(
            dataset_id="d",
            cases=[GoldenAgentCase(case_id="c1", agent_id="a1", goal="g")],
            minimum_pass_rate=0.9,
        )
        calls = {}

        class FakeRuntime:
            def run(self, request):
                calls["request"] = request

                class Result:
                    status = "SUCCEEDED"
                    tool_calls = []
                    evidence_refs = ["urn:eoip:evidence:1"]

                return Result()

        report = dataset.run_regression(FakeRuntime())
        assert report.gate_passed
        assert calls["request"].dry_run is True


class TestGovernancePolicy:
    def test_passes_within_thresholds(self):
        policy = GovernancePolicy(groundedness_threshold=0.8, unsafe_action_threshold=0.1)
        verdict = policy.evaluate(ModelOutput(
            response_id="r1", model_id="m", text="t",
            groundedness_score=0.9, unsafe_action_score=0.05,
        ))
        assert verdict.passed
        assert verdict.reasons == []

    def test_fails_low_groundedness(self):
        policy = GovernancePolicy(groundedness_threshold=0.8)
        verdict = policy.evaluate(ModelOutput(
            response_id="r1", model_id="m", text="t", groundedness_score=0.5,
        ))
        assert not verdict.passed
        assert any("groundedness" in r for r in verdict.reasons)

    def test_fails_unsafe_action(self):
        policy = GovernancePolicy(unsafe_action_threshold=0.1)
        verdict = policy.evaluate(ModelOutput(
            response_id="r1", model_id="m", text="t", unsafe_action_score=0.5,
        ))
        assert not verdict.passed
        assert any("unsafe_action" in r for r in verdict.reasons)


class TestKillSwitch:
    def test_enabled_by_default(self):
        switch = KillSwitch()
        for feature in Feature:
            assert switch.is_enabled(feature)
            switch.check(feature)  # no raise

    def test_disable_feature_with_structured_reason(self):
        switch = KillSwitch()
        switch.disable(Feature.RAG, reason="hallucination spike")
        assert not switch.is_enabled(Feature.RAG)
        assert switch.is_enabled(Feature.NLQ)
        with pytest.raises(FeatureDisabled) as exc_info:
            switch.check(Feature.RAG)
        refusal: FeatureDisabledReason = exc_info.value.refusal
        assert refusal.feature == "rag"
        assert not refusal.enabled
        assert "hallucination spike" in refusal.reason

    def test_global_disable_overrides_features(self):
        switch = KillSwitch()
        switch.disable_all(reason="operator override")
        for feature in Feature:
            assert not switch.is_enabled(feature)
            with pytest.raises(FeatureDisabled) as exc_info:
                switch.check(feature)
            assert "global kill switch" in exc_info.value.refusal.reason
            assert "operator override" in exc_info.value.refusal.reason
        switch.enable_all()
        assert switch.is_enabled(Feature.RAG)

    def test_reenable_feature(self):
        switch = KillSwitch()
        switch.disable("nlq")
        switch.enable("nlq")
        assert switch.is_enabled("nlq")


class TestClassifyModelOutput:
    def _output(self, score: float, refs: list[str]) -> ModelOutput:
        return ModelOutput(
            response_id="r", model_id="m", text="t",
            groundedness_score=score, evidence_refs=refs,
        )

    def test_grounded(self):
        assert classify_model_output(
            self._output(0.95, ["e1", "e2"]), ["e1", "e2"],
        ) == OutputClass.GROUNDED

    def test_uncertain(self):
        assert classify_model_output(
            self._output(0.7, ["e1"]), ["e1"],
        ) == OutputClass.UNCERTAIN

    def test_unsupported(self):
        assert classify_model_output(
            self._output(0.3, ["e1"]), ["e1"],
        ) == OutputClass.UNSUPPORTED
        assert classify_model_output(
            self._output(0.95, ["e1"]), ["other"],
        ) == OutputClass.UNSUPPORTED

    def test_no_evidence_is_unsupported(self):
        assert classify_model_output(
            self._output(0.95, []), ["e1"],
        ) == OutputClass.UNSUPPORTED


class TestHallucinationIncidentLog:
    def test_append_only_and_redaction(self, tmp_path):
        log = HallucinationIncidentLog(tmp_path / "incidents.jsonl")
        incident = HallucinationIncident(
            incident_id="i1", model_id="m", response_id="r",
            classification=OutputClass.UNSUPPORTED, summary="leak",
            evidence_refs=["e1"],
        )
        log.record(incident, extra={"token": "secret-value", "note": "password=hunter2"})
        log.record(incident, extra={"note": "clean"})

        records = log.read_all()
        assert len(records) == 2
        assert records[0]["extra"]["token"] == "***REDACTED***"
        assert "***REDACTED***" in records[0]["extra"]["note"]
        assert records[1]["extra"]["note"] == "clean"

        # append-only: file holds exactly two lines
        lines = (tmp_path / "incidents.jsonl").read_text("utf-8").strip().splitlines()
        assert len(lines) == 2
        json.loads(lines[0])

    def test_read_missing_file(self, tmp_path):
        log = HallucinationIncidentLog(tmp_path / "nope.jsonl")
        assert log.read_all() == []
