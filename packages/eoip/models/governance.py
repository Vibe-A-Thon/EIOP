"""Responsible AI / model governance (§49, GAP-AGOV-012-adjacent).

Deterministic-first governance layer covering:

- ModelRegistry: approved-model list with add/remove/check (§49.2,
  GAP-AGOV-012-adjacent).
- PromptTemplateRegistry: versioned prompt templates with content hashes
  (§49.3).
- EvaluationDataset + regression runner hooks reusing the golden-case
  conventions from eoip.agents.evaluation (§49.4).
- GovernancePolicy: groundedness and unsafe-action thresholds with
  evaluate(response) -> pass/fail (§49.5).
- KillSwitch: global + per-feature (rag, agents, nlq) AI kill switch;
  disabled features refuse with a structured reason (§49.6).
- classify_model_output: grounded / uncertain / unsupported stub based on
  evidence manifest coverage (§49.7).
- HallucinationIncidentLog: append-only JSONL incident log with secret
  redaction via eoip.audit.redaction (§49.8).

No external dependencies beyond stdlib + pydantic.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from pathlib import Path
from typing import Any
from collections.abc import Iterable

from pydantic import BaseModel, Field

from eoip.agents.evaluation import GoldenAgentCase
from eoip.audit.redaction import redact_secrets

MODELS_AREA = "models"


def _model_urn(model_id: str) -> str:
    return f"urn:eoip:{MODELS_AREA}:model:{model_id}"


# -- model registry (§49.2, GAP-AGOV-012-adjacent) ---------------------------


class ModelHealth(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class ModelEntry(BaseModel):
    """A registered model version with capabilities and approval state."""

    model_id: str
    version: str
    provider: str
    capabilities: set[str] = Field(default_factory=set)
    health: ModelHealth = ModelHealth.UNAVAILABLE
    approved: bool = False

    @property
    def urn(self) -> str:
        return _model_urn(self.model_id)


class ModelRegistry:
    """Registry of models with an approved-model list.

    Approvals are explicit: a model is usable only when registered,
    approved, and healthy. GAP-AGOV-012-adjacent.
    """

    def __init__(self) -> None:
        self._models: dict[str, ModelEntry] = {}

    def register(self, entry: ModelEntry) -> None:
        self._models[entry.model_id] = entry

    def get(self, model_id: str) -> ModelEntry | None:
        return self._models.get(model_id)

    def remove(self, model_id: str) -> bool:
        return self._models.pop(model_id, None) is not None

    def set_health(self, model_id: str, health: ModelHealth) -> None:
        entry = self._require(model_id)
        entry.health = health

    def approve(self, model_id: str) -> None:
        self._require(model_id).approved = True

    def revoke(self, model_id: str) -> None:
        self._require(model_id).approved = False

    def is_approved(self, model_id: str) -> bool:
        entry = self._models.get(model_id)
        return bool(entry and entry.approved)

    def is_usable(self, model_id: str) -> bool:
        entry = self._models.get(model_id)
        return bool(entry and entry.approved and entry.health == ModelHealth.HEALTHY)

    def approved_models(self) -> list[str]:
        return sorted(mid for mid, e in self._models.items() if e.approved)

    def list_models(self) -> list[ModelEntry]:
        return [self._models[k] for k in sorted(self._models)]

    def _require(self, model_id: str) -> ModelEntry:
        entry = self._models.get(model_id)
        if entry is None:
            raise KeyError(f"unknown model: {model_id}")
        return entry


# -- prompt template registry (§49.3) ----------------------------------------


class PromptTemplate(BaseModel):
    name: str
    version: str
    template: str
    variables: list[str] = Field(default_factory=list)
    template_hash: str = ""
    active: bool = True


def hash_template(template: str) -> str:
    return hashlib.sha256(template.encode("utf-8")).hexdigest()


class PromptTemplateRegistry:
    """Versioned registry of prompt templates with content hashes."""

    def __init__(self) -> None:
        self._templates: dict[tuple[str, str], PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> PromptTemplate:
        template.template_hash = hash_template(template.template)
        key = (template.name, template.version)
        # Registering a new version deactivates prior versions.
        if key not in self._templates:
            for (name, _), existing in self._templates.items():
                if name == template.name:
                    existing.active = False
        self._templates[key] = template
        return template

    def get(self, name: str, version: str | None = None) -> PromptTemplate | None:
        if version is not None:
            return self._templates.get((name, version))
        versions = [t for (n, _), t in self._templates.items() if n == name]
        versions.sort(key=lambda t: t.version)
        return versions[-1] if versions else None

    def active_template(self, name: str) -> PromptTemplate | None:
        for (n, _), t in self._templates.items():
            if n == name and t.active:
                return t
        return None

    def verify_integrity(self, name: str, version: str) -> bool:
        template = self._templates.get((name, version))
        return bool(template and template.template_hash == hash_template(template.template))

    def list_templates(self, name: str | None = None) -> list[PromptTemplate]:
        items = [
            t for (n, _), t in sorted(self._templates.items())
            if name is None or n == name
        ]
        return items


# -- evaluation dataset + regression hooks (§49.4) ----------------------------


class EvaluationDataset(BaseModel):
    """Golden-case regression dataset reusing agents/evaluation conventions."""

    dataset_id: str
    description: str = ""
    cases: list[GoldenAgentCase] = Field(default_factory=list)
    minimum_pass_rate: float = 0.9

    @property
    def urn(self) -> str:
        return f"urn:eoip:{MODELS_AREA}:dataset:{self.dataset_id}"

    @classmethod
    def from_json(cls, path: str | Path) -> EvaluationDataset:
        return cls.model_validate(json.loads(Path(path).read_text("utf-8")))

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(self.model_dump_json(indent=2), "utf-8")

    def run_regression(self, runtime: Any) -> Any:
        """Run golden cases through eoip.agents.evaluation.evaluate_agents."""
        from eoip.agents.evaluation import evaluate_agents

        return evaluate_agents(runtime, self.cases, minimum_pass_rate=self.minimum_pass_rate)


# -- governance policy thresholds (§49.5) -------------------------------------


class ModelOutput(BaseModel):
    """A scored model response assessed against governance thresholds."""

    response_id: str
    model_id: str
    text: str
    groundedness_score: float = 0.0  # 0..1 fraction of claims backed by evidence
    unsafe_action_score: float = 0.0  # 0..1 risk of unsafe action
    evidence_refs: list[str] = Field(default_factory=list)


class PolicyVerdict(BaseModel):
    passed: bool
    reasons: list[str] = Field(default_factory=list)


class GovernancePolicy(BaseModel):
    """Groundedness + unsafe-action thresholds (§49.5)."""

    groundedness_threshold: float = 0.8
    unsafe_action_threshold: float = 0.1

    def evaluate(self, response: ModelOutput) -> PolicyVerdict:
        reasons: list[str] = []
        if response.groundedness_score < self.groundedness_threshold:
            reasons.append(
                f"groundedness {response.groundedness_score:.3f} below "
                f"threshold {self.groundedness_threshold:.3f}"
            )
        if response.unsafe_action_score > self.unsafe_action_threshold:
            reasons.append(
                f"unsafe_action {response.unsafe_action_score:.3f} above "
                f"threshold {self.unsafe_action_threshold:.3f}"
            )
        return PolicyVerdict(passed=not reasons, reasons=reasons)


# -- AI kill switch (§49.6) ----------------------------------------------------


class Feature(StrEnum):
    RAG = "rag"
    AGENTS = "agents"
    NLQ = "nlq"


class FeatureDisabledReason(BaseModel):
    """Structured refusal reason returned/raised when a feature is disabled."""

    feature: str
    enabled: bool = False
    reason: str


class FeatureDisabled(Exception):
    def __init__(self, refusal: FeatureDisabledReason) -> None:
        super().__init__(refusal.reason)
        self.refusal = refusal


class KillSwitch:
    """Global + per-feature AI kill switch (§49.6).

    A global disable overrides every feature. Individual features can be
    disabled without affecting the others.
    """

    def __init__(self) -> None:
        self._global_enabled = True
        self._features: dict[str, bool] = {f.value: True for f in Feature}
        self._feature_reasons: dict[str, str] = {}
        self._reason = ""

    def disable_all(self, reason: str = "global kill switch engaged") -> None:
        self._global_enabled = False
        self._reason = reason

    def enable_all(self) -> None:
        self._global_enabled = True
        self._reason = ""

    def disable(self, feature: Feature | str, reason: str = "") -> None:
        self._features[str(feature)] = False
        if reason:
            self._feature_reasons[str(feature)] = reason

    def enable(self, feature: Feature | str) -> None:
        self._features[str(feature)] = True
        self._feature_reasons.pop(str(feature), None)

    def is_enabled(self, feature: Feature | str) -> bool:
        return self._global_enabled and self._features.get(str(feature), False)

    def check(self, feature: Feature | str) -> None:
        """Raise FeatureDisabled with a structured reason if disabled."""
        feature = str(feature)
        if self.is_enabled(feature):
            return
        if not self._global_enabled:
            reason = self._reason or "global kill switch engaged"
            raise FeatureDisabled(FeatureDisabledReason(
                feature=feature, reason=f"global kill switch: {reason}"
            ))
        raise FeatureDisabled(FeatureDisabledReason(
            feature=feature,
            reason=self._feature_reasons.get(feature, f"feature '{feature}' is disabled"),
        ))


# -- model-output classification (§49.7) --------------------------------------


class OutputClass(StrEnum):
    GROUNDED = "grounded"
    UNCERTAIN = "uncertain"
    UNSUPPORTED = "unsupported"


def classify_model_output(
    output: ModelOutput,
    evidence_manifest: Iterable[str],
    *,
    uncertain_floor: float = 0.5,
) -> OutputClass:
    """Classify model output by evidence manifest coverage (§49.7).

    Deterministic stub: groundedness_score >= 0.9 and full evidence coverage
    -> grounded; score below uncertain_floor -> unsupported; otherwise
    uncertain. Coverage requires every evidence_ref to appear in the
    manifest.
    """
    manifest = set(evidence_manifest)
    coverage = (
        len([r for r in output.evidence_refs if r in manifest]) / len(output.evidence_refs)
        if output.evidence_refs
        else 0.0
    )
    if output.groundedness_score >= 0.9 and coverage >= 1.0 and output.evidence_refs:
        return OutputClass.GROUNDED
    if output.groundedness_score < uncertain_floor or coverage == 0.0:
        return OutputClass.UNSUPPORTED
    return OutputClass.UNCERTAIN


# -- hallucination incident log (§49.8) ----------------------------------------


class HallucinationIncident(BaseModel):
    incident_id: str
    model_id: str
    response_id: str
    classification: OutputClass
    summary: str
    evidence_refs: list[str] = Field(default_factory=list)


class HallucinationIncidentLog:
    """Append-only JSONL log of hallucination incidents with secret redaction."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    def record(self, incident: HallucinationIncident, extra: dict | None = None) -> None:
        record = incident.model_dump(mode="json")
        if extra:
            record["extra"] = extra
        redacted = redact_secrets(record)
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(redacted, sort_keys=True) + "\n")

    def read_all(self) -> list[dict]:
        if not self._path.exists():
            return []
        incidents = []
        with self._path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    incidents.append(json.loads(line))
        return incidents
