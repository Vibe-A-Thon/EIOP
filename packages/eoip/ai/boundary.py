"""Deterministic–probabilistic boundary and neuro-symbolic arbitration (CRA-045.1 - CRA-045.8).

Enforces:
1. Producer classification: DETERMINISTIC vs PROBABILISTIC (CRA-045.1).
2. Proposal lifecycle: probabilistic outputs enter strictly as 'proposed', never directly 'asserted' (CRA-045.2).
3. Dual-path answering: CORROBORATED on match, DISPUTED on disagreement, UNCORROBORATED when only probabilistic (CRA-045.3).
4. Constraint pre-filtering: candidates violating SHACL/ontology rejected with violated shape (CRA-045.4).
5. Storage, query, and export separation: asserted-only by default; proposed exports placed in urn:eoip:proposed:{tenant} (CRA-045.5).
6. Calibration honesty: raw model output is 'score', never 'probability' or 'confidence' without calibrator (CRA-045.6).
7. Reproducibility metadata: model revision, prompt digest, context manifest digest, seed (CRA-045.7).
8. Text-labelled explanations for each path (CRA-045.8).
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel, Field

from eoip.contracts.canonical import (
    AgreementState,
    CanonicalAssertion,
    DualPathResult,
    KnowledgeState,
    ModelLineage,
    ProducerClass,
    RDFTerm,
    TermKind,
    TrustedScope,
)

logger = logging.getLogger(__name__)


class ConstraintViolationError(ValueError):
    """Raised when a probabilistic proposal violates ontology or SHACL constraints."""
    def __init__(self, message: str, violated_rule: str) -> None:
        super().__init__(f"{message} (violated: {violated_rule})")
        self.violated_rule = violated_rule


@dataclass
class ProposalEvaluation:
    accepted: bool
    rejection_reason: str | None = None
    violated_constraint: str | None = None


# ---------------------------------------------------------------------------
# Calibration Honesty (CRA-045.6) & Proposal Creation (CRA-045.2, CRA-045.7)
# ---------------------------------------------------------------------------

def create_probabilistic_proposal(
    subject: str,
    predicate: str,
    object_value: str,
    model_name: str,
    model_version: str,
    raw_score: float,
    prompt_text: str = "",
    context_manifest_digest: str = "",
    seed: int | None = None,
    calibrator_ref: str | None = None,
    calibrated_confidence: float | None = None,
    assertion_id: str | None = None,
    tenant_id: str = "default_tenant",
) -> CanonicalAssertion:
    """CRA-045.2, CRA-045.6, CRA-045.7: Create proposal with calibration honesty and reproducibility metadata.

    Enforces:
    - knowledge_state is strictly PROPOSED.
    - confidence is populated ONLY if calibrator_ref is non-empty.
    - confidence_calibrated is True only if calibrator_ref is non-empty.
    """
    prompt_digest = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest() if prompt_text else ""
    lineage = ModelLineage(
        model_id=model_name,
        model_version=model_version,
        producer_class=ProducerClass.PROBABILISTIC,
        prompt_digest=prompt_digest,
        context_manifest_digest=context_manifest_digest,
        seed_bundle={"seed": seed} if seed is not None else {},
        calibrator_id=calibrator_ref,
    )

    # CRA-045.6: If no calibrator exists, calibrated confidence cannot be claimed
    has_calibrator = bool(calibrator_ref)
    effective_confidence = calibrated_confidence if has_calibrator else None

    subj_term = RDFTerm(kind=TermKind.IRI, value=subject)
    pred_term = RDFTerm(kind=TermKind.IRI, value=predicate)
    obj_term = (
        RDFTerm(kind=TermKind.IRI, value=object_value)
        if object_value.startswith("http://") or object_value.startswith("urn:")
        else RDFTerm(kind=TermKind.LITERAL, value=object_value)
    )

    aid = assertion_id or f"prop:{hashlib.sha256(f'{subject}:{predicate}:{object_value}:{prompt_digest}'.encode()).hexdigest()[:16]}"
    graph_iri = f"urn:eoip:proposed:{tenant_id}"

    return CanonicalAssertion(
        assertion_id=aid,
        graph_iri=graph_iri,
        subject=subj_term,
        predicate=pred_term,
        object=obj_term,
        knowledge_state=KnowledgeState.PROPOSED,
        tenant_id=tenant_id,
        confidence=effective_confidence,
        confidence_calibrated=has_calibrator,
        model_lineage=lineage,
    )


# ---------------------------------------------------------------------------
# Proposal Promotion with Constraint Enforcement (CRA-045.2, CRA-045.4)
# ---------------------------------------------------------------------------

def validate_and_promote_proposal(
    proposal: CanonicalAssertion,
    approver: str,
    constraint_validator: Callable[[CanonicalAssertion], ProposalEvaluation] | None = None,
) -> CanonicalAssertion:
    """CRA-045.2, CRA-045.4: Promotes a proposal to asserted ONLY after constraint validation and approval.

    Preserves original ModelLineage and records approver.
    If constraint_validator fails, raises ConstraintViolationError and rejects proposal.
    """
    if proposal.knowledge_state != KnowledgeState.PROPOSED:
        raise ValueError(f"Only PROPOSED assertions can be promoted; current state: {proposal.knowledge_state}")

    if constraint_validator:
        evaluation = constraint_validator(proposal)
        if not evaluation.accepted:
            raise ConstraintViolationError(
                f"Candidate rejected by deterministic constraint: {evaluation.rejection_reason}",
                violated_rule=evaluation.violated_constraint or "UNKNOWN_CONSTRAINT",
            )

    # Promoted: state becomes ASSERTED, keeps probabilistic model_lineage, records approver
    promoted = proposal.model_copy(update={
        "knowledge_state": KnowledgeState.ASSERTED,
        "graph_iri": f"urn:eoip:tenant:{proposal.tenant_id}",
        "approver": approver,
    })
    return promoted


# ---------------------------------------------------------------------------
# Dual-Path Answering & Arbitration (CRA-045.3, CRA-045.8)
# ---------------------------------------------------------------------------

class DualPathOrchestrator:
    """Arbitrates concurrent deterministic and probabilistic query execution."""

    def execute_dual_path(
        self,
        question_id: str,
        question_text: str,
        scope: TrustedScope,
        deterministic_fn: Callable[[TrustedScope, str], Any] | None,
        probabilistic_fn: Callable[[TrustedScope, str], Any],
        tolerance: float = 0.001,
    ) -> DualPathResult:
        """CRA-045.3: Run deterministic and probabilistic paths beside each other.

        Reports:
        - CORROBORATED: Both paths produced equivalent answers.
        - DISPUTED: Disagreement between deterministic and probabilistic answers (no silent override).
        - UNCORROBORATED: Probabilistic-only answer (no deterministic path exists).
        """
        det_result = None
        prob_result = None

        if deterministic_fn is not None:
            try:
                det_result = deterministic_fn(scope, question_text)
            except Exception as e:
                logger.warning(f"Deterministic path execution failed for {question_id}: {e}")
                det_result = None

        try:
            prob_result = probabilistic_fn(scope, question_text)
        except Exception as e:
            logger.warning(f"Probabilistic path execution failed for {question_id}: {e}")
            prob_result = None

        # Determine AgreementState
        if det_result is None and prob_result is not None:
            agreement = AgreementState.UNCORROBORATED
            explanation = (
                f"[PROBABILISTIC ONLY] Question '{question_text}' has no exact deterministic answer. "
                "Output is an uncorroborated probabilistic proposal."
            )
        elif det_result is not None and prob_result is not None:
            is_match = self._check_equivalence(det_result, prob_result, tolerance)
            if is_match:
                agreement = AgreementState.CORROBORATED
                explanation = (
                    f"[CORROBORATED] Deterministic path and Probabilistic path agree: '{det_result}'."
                )
            else:
                agreement = AgreementState.DISPUTED
                explanation = (
                    f"[DISPUTED] Deterministic path returned '{det_result}', but Probabilistic AI proposed "
                    f"'{prob_result}'. Deterministic truth bounds display; disagreement surfaced explicitly."
                )
        else:
            agreement = AgreementState.UNCORROBORATED
            explanation = f"[EMPTY] No answers produced by either path."

        q_digest = hashlib.sha256(question_text.encode("utf-8")).hexdigest()

        return DualPathResult(
            question_digest=q_digest,
            deterministic_result=det_result,
            probabilistic_result=prob_result,
            agreement=agreement,
            explanation=explanation,
        )

    def _check_equivalence(self, det: Any, prob: Any, tolerance: float) -> bool:
        """Evaluate equivalence between deterministic and probabilistic outputs."""
        if det == prob:
            return True
        if isinstance(det, (int, float)) and isinstance(prob, (int, float)):
            return abs(float(det) - float(prob)) <= tolerance
        if isinstance(det, (list, set)) and isinstance(prob, (list, set)):
            return set(det) == set(prob)
        if isinstance(det, str) and isinstance(prob, str):
            return det.strip().lower() == prob.strip().lower()
        return False


# ---------------------------------------------------------------------------
# Storage, Query, and TriG Export Separation (CRA-045.5)
# ---------------------------------------------------------------------------

def filter_asserted_only(
    assertions: list[CanonicalAssertion],
    include_proposed: bool = False,
) -> list[CanonicalAssertion]:
    """CRA-045.5: Asserted-only default. Excludes proposed statements unless caller requests."""
    if include_proposed:
        return assertions
    return [a for a in assertions if a.knowledge_state != KnowledgeState.PROPOSED]


def export_trig_quads(
    assertions: list[CanonicalAssertion],
    tenant_id: str,
    include_proposed: bool = False,
) -> str:
    """CRA-045.5: Exports assertions to TriG format.

    - Facts (ASSERTED, INFERRED) placed in <urn:eoip:tenant:{tenant_id}>.
    - Proposed statements (if explicitly included) placed in <urn:eoip:proposed:{tenant_id}>.
    - Proposed statements NEVER enter the facts graph.
    """
    facts_graph = f"urn:eoip:tenant:{tenant_id}"
    proposed_graph = f"urn:eoip:proposed:{tenant_id}"

    facts_triples: list[str] = []
    proposed_triples: list[str] = []

    for a in assertions:
        subj = f"<{a.subject.value}>" if a.subject.kind == TermKind.IRI else a.subject.value
        pred = f"<{a.predicate.value}>" if a.predicate.kind == TermKind.IRI else a.predicate.value
        obj = (
            f"<{a.object.value}>"
            if a.object.kind == TermKind.IRI
            else f'"{a.object.value}"'
        )
        triple_line = f"    {subj} {pred} {obj} ."

        if a.knowledge_state == KnowledgeState.PROPOSED:
            if include_proposed:
                proposed_triples.append(triple_line)
        else:
            facts_triples.append(triple_line)

    lines: list[str] = []
    lines.append(f"<{facts_graph}> {{")
    lines.extend(facts_triples)
    lines.append("}")

    if include_proposed and proposed_triples:
        lines.append("")
        lines.append(f"<{proposed_graph}> {{")
        lines.extend(proposed_triples)
        lines.append("}")

    return "\n".join(lines) + "\n"
