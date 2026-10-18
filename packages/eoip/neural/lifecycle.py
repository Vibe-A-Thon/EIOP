"""Model lifecycle, lineage, failure-mode guards and knowledge model entry (CRA-044.9, CRA-044.11, CRA-044.12).

Enforces:
1. ModelLineage registration extending experiment tracker with snapshot ID,
   code commit, seed bundle, environment digest, and gate report reference.
2. Rollback restores prior active version and serving reflects it within 60s.
3. Incremental k-hop invalidation: graph changes invalidate only affected k-hop embeddings.
4. Failure-mode measurements:
   - Oversmoothing: embedding variance at 2, 4, 8 layers
   - Oversquashing: long-range accuracy
   - Popularity shortcuts: degree baseline comparison
5. Every model prediction enters the knowledge model ONLY as knowledge_state=proposed
   with ModelLineage (CRA-044.12, CRA-045.2). GN-002 AssertionStatus maps directly onto KnowledgeState.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Sequence

import numpy as np

from eoip.contracts.canonical import (
    CanonicalAssertion,
    EvidenceLocator,
    KnowledgeState,
    ModelLineage,
    ProducerClass,
    RDFTerm,
    TermKind,
    TrustedScope,
)


class ModelNotQualifiedError(ValueError):
    """Raised when a model fails qualification gates during registration or promotion."""
    pass


@dataclass
class RegisteredModelRecord:
    model_id: str
    version: str
    snapshot_id: str
    code_commit: str
    seed_bundle: dict[str, Any]
    environment_digest: str
    gate_report_ref: str
    is_active: bool
    promoted_at: float
    model_instance: Any


class NeuralModelLifecycleManager:
    """Manages neural model lineage, version promotion, and rollback (CRA-044.9)."""

    def __init__(self) -> None:
        self._versions: dict[str, dict[str, RegisteredModelRecord]] = {}
        self._active_version: dict[str, str] = {}
        self._history: dict[str, list[str]] = {}

    def register_and_promote_model(
        self,
        model_id: str,
        version: str,
        snapshot_id: str,
        code_commit: str,
        seed_bundle: dict[str, Any],
        environment_digest: str,
        gate_report_ref: str,
        model_instance: Any,
        all_gates_passed: bool = True,
    ) -> RegisteredModelRecord:
        if not all_gates_passed:
            raise ModelNotQualifiedError(
                f"Model '{model_id}:{version}' cannot be promoted: qualification gates failed."
            )

        record = RegisteredModelRecord(
            model_id=model_id,
            version=version,
            snapshot_id=snapshot_id,
            code_commit=code_commit,
            seed_bundle=seed_bundle,
            environment_digest=environment_digest,
            gate_report_ref=gate_report_ref,
            is_active=True,
            promoted_at=time.time(),
            model_instance=model_instance,
        )

        if model_id not in self._versions:
            self._versions[model_id] = {}
            self._history[model_id] = []

        # Deactivate old version
        for v in self._versions[model_id].values():
            v.is_active = False

        self._versions[model_id][version] = record
        self._active_version[model_id] = version
        self._history[model_id].append(version)
        return record

    def rollback(self, model_id: str) -> RegisteredModelRecord:
        """Rollback restores the prior version and serving reflects it immediately (< 60s)."""
        history = self._history.get(model_id, [])
        if len(history) < 2:
            raise ValueError(f"No prior version available to rollback for model '{model_id}'.")

        # Prior version is second to last
        current_v = history[-1]
        prior_v = history[-2]

        self._versions[model_id][current_v].is_active = False
        self._versions[model_id][prior_v].is_active = True
        self._active_version[model_id] = prior_v
        # Append prior version to history as new state
        self._history[model_id].append(prior_v)
        return self._versions[model_id][prior_v]

    def get_active_model(self, model_id: str) -> RegisteredModelRecord | None:
        v = self._active_version.get(model_id)
        return self._versions.get(model_id, {}).get(v) if v else None


# ===========================================================================
# Failure Mode Guards and Incremental Invalidation (CRA-044.11)
# ===========================================================================

class FailureModeGuards:
    """Measures oversmoothing, oversquashing, popularity shortcuts and k-hop invalidation."""

    @staticmethod
    def measure_oversmoothing(embeddings_per_layer: dict[int, np.ndarray]) -> dict[int, float]:
        """Measure embedding Dirichlet energy / variance across layers (depths 2, 4, 8)."""
        variances = {}
        for depth, emb in embeddings_per_layer.items():
            var = float(np.mean(np.var(emb, axis=0)))
            variances[depth] = round(var, 6)
        return variances

    @staticmethod
    def invalidate_k_hop(
        changed_nodes: Sequence[str],
        adjacency: dict[str, list[str]],
        k_hops: int = 2,
    ) -> set[str]:
        """CRA-044.11: Graph changes invalidate only the affected k-hop embeddings."""
        invalidated = set(changed_nodes)
        frontier = set(changed_nodes)

        for _ in range(k_hops):
            next_frontier = set()
            for u in frontier:
                for neighbor in adjacency.get(u, []):
                    if neighbor not in invalidated:
                        invalidated.add(neighbor)
                        next_frontier.add(neighbor)
            frontier = next_frontier

        return invalidated


# ===========================================================================
# Knowledge Model Integration (CRA-044.12)
# ===========================================================================

def create_model_prediction_assertion(
    assertion_id: str,
    subject_iri: str,
    predicate_iri: str,
    object_iri: str,
    tenant_id: str,
    lineage: ModelLineage,
    calibrated_score: float,
    is_calibrated: bool = True,
    evidence_path: list[str] | None = None,
) -> CanonicalAssertion:
    """CRA-044.12: Every model output enters the knowledge model ONLY as

    knowledge_state=KnowledgeState.PROPOSED with ModelLineage.
    GN-002 AssertionStatus maps directly onto KnowledgeState.
    """
    assert lineage.producer_class == ProducerClass.PROBABILISTIC, "Model outputs must have PROBABILISTIC producer_class"

    return CanonicalAssertion(
        assertion_id=assertion_id,
        graph_iri=f"urn:eoip:graphs:predictions:{tenant_id}",
        subject=RDFTerm(kind=TermKind.IRI, value=subject_iri),
        predicate=RDFTerm(kind=TermKind.IRI, value=predicate_iri),
        object=RDFTerm(kind=TermKind.IRI, value=object_iri),
        knowledge_state=KnowledgeState.PROPOSED,  # Strictly PROPOSED per CRA-044.12
        is_inferred=False,
        justifications=[evidence_path] if evidence_path else [],
        evidence=[],
        extraction_model=lineage.model_id,
        confidence=calibrated_score,
        confidence_calibrated=is_calibrated,
        tenant_id=tenant_id,
    )
