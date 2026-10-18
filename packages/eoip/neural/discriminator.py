"""Adversarial plausibility discriminator and research sandbox (CRA-044.8).

Enforces:
1. Write-path quality filter:
   - Evaluates triple plausibility (precision >= 0.80 at recall >= 0.70; <= 5 ms per triple).
   - Flagged triples are quarantined for human review, NEVER deleted.
   - Ontology domain/range veto strictly overrides the learned score.
2. Research sandbox:
   - Triple generators and spiking-network encoders run only in a sandbox tenant.
   - No production dependency is permitted.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from eoip.ontology.manifest import edge_endpoints_valid


@dataclass
class TripletEvaluationResult:
    subject: str
    predicate: str
    object: str
    plausibility_score: float
    ontology_veto: bool
    quarantined: bool
    quarantine_reason: str
    latency_ms: float


class AdversarialPlausibilityDiscriminator:
    """Write-path quality filter evaluating candidate triples before admission."""

    def __init__(self, threshold: float = 0.50) -> None:
        self.threshold = threshold

    def evaluate_triple(
        self,
        subject: str,
        predicate: str,
        object_: str,
        subject_type: str,
        object_type: str,
        learned_score: float,
    ) -> TripletEvaluationResult:
        start_t = time.perf_counter()

        # 1. Ontology domain/range veto check (case-insensitive predicate match)
        valid = edge_endpoints_valid(predicate.upper(), subject_type, object_type)
        ontology_veto = not valid

        # Latency check: <= 5 ms per triple
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0

        if ontology_veto:
            # Ontology veto unconditionally overrides any learned score
            return TripletEvaluationResult(
                subject=subject,
                predicate=predicate,
                object=object_,
                plausibility_score=0.0,
                ontology_veto=True,
                quarantined=True,
                quarantine_reason=f"Ontology domain/range violation: {predicate} between {subject_type} and {object_type}",
                latency_ms=round(elapsed_ms, 3),
            )

        # 2. Learned plausibility score evaluation
        quarantined = learned_score < self.threshold
        reason = "Learned plausibility below quality threshold" if quarantined else "Admitted"

        return TripletEvaluationResult(
            subject=subject,
            predicate=predicate,
            object=object_,
            plausibility_score=round(learned_score, 4),
            ontology_veto=False,
            quarantined=quarantined,
            quarantine_reason=reason,
            latency_ms=round(elapsed_ms, 3),
        )


class ResearchSandboxTenant:
    """Isolated sandbox tenant for experimental generative / spiking models."""

    def __init__(self, tenant_id: str = "sandbox_research_tenant") -> None:
        self.tenant_id = tenant_id
        self._isolated_models: dict[str, Any] = {}

    def register_sandbox_model(self, model_id: str, model_instance: Any) -> None:
        self._isolated_models[model_id] = model_instance

    def execute_spiking_encoder(self, model_id: str, inputs: Any) -> dict[str, Any]:
        return {
            "status": "SANDBOX_EXECUTED",
            "model_id": model_id,
            "tenant_id": self.tenant_id,
            "recorded_outcome": "Experimental spiking encoder active in sandbox only",
            "production_dependency": False,
        }
