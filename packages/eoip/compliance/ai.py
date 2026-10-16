"""AI governance records (SR-GOV-002).

Model cards, evaluation records, intended/prohibited use, human-oversight
configuration and the user-visible AI labeling flag. An AI-BOM (bill of
materials of models/components per feature) and the AI incident workflow are
ADR-gated: the record format here carries the fields they need, but the
incident workflow reuses the generic incident/RCA reporting path rather than
a dedicated state machine. Records persist to a JSON file store, matching
``eoip.agents.proposals.ProposalStore`` conventions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from eoip.compliance.pack import new_id

RiskLevel = Literal["minimal", "limited", "high", "unacceptable"]


class ModelCard(BaseModel):
    """Registered model card (SR-GOV-002)."""

    model_config = ConfigDict(extra="forbid")

    model_card_id: str
    name: str
    version: str
    provider: str = ""
    risk_classification: RiskLevel = "limited"
    intended_use: list[str] = Field(default_factory=list)
    prohibited_use: list[str] = Field(default_factory=list)
    training_data_summary: str = ""
    limitations: str = ""
    labeling_required: bool = True
    human_oversight_id: str | None = None
    created_at: str = ""


class EvaluationRecord(BaseModel):
    """Evaluation/benchmark result for a registered model (SR-GOV-002)."""

    model_config = ConfigDict(extra="forbid")

    evaluation_id: str
    model_card_id: str
    evaluated_at: str
    benchmark: str
    score: float
    threshold: float | None = None
    passed: bool = True
    notes: str = ""


class HumanOversightConfig(BaseModel):
    """Human-oversight configuration for AI-assisted outputs (SR-GOV-002)."""

    model_config = ConfigDict(extra="forbid")

    oversight_id: str
    name: str
    reviewer_role: str = "steward"
    require_approval_for: list[str] = Field(default_factory=lambda: ["mutation", "egress"])
    sampling_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    enabled: bool = True


class AIGovernanceStore:
    """JSON-file store for AI governance records (SR-GOV-002)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "ai-governance.json"
        self._model_cards: dict[str, ModelCard] = {}
        self._evaluations: dict[str, EvaluationRecord] = {}
        self._oversight: dict[str, HumanOversightConfig] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("model_cards", []):
            card = ModelCard(**item)
            self._model_cards[card.model_card_id] = card
        for item in data.get("evaluations", []):
            record = EvaluationRecord(**item)
            self._evaluations[record.evaluation_id] = record
        for item in data.get("oversight", []):
            config = HumanOversightConfig(**item)
            self._oversight[config.oversight_id] = config

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "model_cards": [c.model_dump() for c in self._model_cards.values()],
            "evaluations": [e.model_dump() for e in self._evaluations.values()],
            "oversight": [o.model_dump() for o in self._oversight.values()],
        }
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    # -- model cards ------------------------------------------------------
    def register_model_card(self, card: ModelCard) -> ModelCard:
        with self._lock:
            if card.model_card_id in self._model_cards:
                raise ValueError(f"Duplicate model card: {card.model_card_id}")
            self._model_cards[card.model_card_id] = card
            self._save()
        return card

    def get_model_card(self, model_card_id: str) -> ModelCard | None:
        return self._model_cards.get(model_card_id)

    def list_model_cards(self) -> list[ModelCard]:
        return list(self._model_cards.values())

    def new_model_card(
        self,
        name: str,
        version: str,
        *,
        risk_classification: RiskLevel = "limited",
        intended_use: list[str] | None = None,
        prohibited_use: list[str] | None = None,
        created_at: str = "",
    ) -> ModelCard:
        card = ModelCard(
            model_card_id=new_id("compliance", "model-card"),
            name=name,
            version=version,
            risk_classification=risk_classification,
            intended_use=intended_use or [],
            prohibited_use=prohibited_use or [],
            created_at=created_at,
        )
        return self.register_model_card(card)

    # -- evaluations ------------------------------------------------------
    def record_evaluation(self, record: EvaluationRecord) -> EvaluationRecord:
        with self._lock:
            if record.evaluation_id in self._evaluations:
                raise ValueError(f"Duplicate evaluation: {record.evaluation_id}")
            self._evaluations[record.evaluation_id] = record
            self._save()
        return record

    def list_evaluations(self, model_card_id: str | None = None) -> list[EvaluationRecord]:
        records = list(self._evaluations.values())
        if model_card_id:
            records = [r for r in records if r.model_card_id == model_card_id]
        return records

    # -- human oversight --------------------------------------------------
    def configure_oversight(self, config: HumanOversightConfig) -> HumanOversightConfig:
        with self._lock:
            self._oversight[config.oversight_id] = config
            self._save()
        return config

    def get_oversight(self, oversight_id: str) -> HumanOversightConfig | None:
        return self._oversight.get(oversight_id)

    # -- user-visible AI labeling ----------------------------------------
    def ai_label_for(self, model_card_id: str) -> dict:
        """User-visible AI labeling flag for outputs of a model (SR-GOV-002).

        Returns a ``{"ai_generated": bool, "label": str, "model_card_id": ...}``
        dict suitable for surfacing on any AI-assisted output.
        """
        card = self._model_cards.get(model_card_id)
        if card is None:
            return {"ai_generated": False, "label": "", "model_card_id": model_card_id}
        if not card.labeling_required:
            return {"ai_generated": True, "label": "", "model_card_id": model_card_id}
        return {
            "ai_generated": True,
            "label": f"AI-assisted ({card.name} v{card.version}, risk: {card.risk_classification})",
            "model_card_id": model_card_id,
        }
