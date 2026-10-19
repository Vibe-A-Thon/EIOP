"""Grounded question answering with cryptographic warrant citations (T-801 / GA-001..005)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from reva.core.digest import sha256_canonical
from reva.kernel.authority import Authority, Epistemic
from reva.kernel.coverage import Coverage
from reva.kernel.warrant import SealedWarrant


@dataclass
class WarrantCitation:
    warrant_id: str
    predicate: str
    authority: str
    epistemic: str
    confidence_bp: int
    statement_snippet: str


@dataclass
class GroundedAnswer:
    answer_id: str
    question: str
    answer_text: str
    citations: List[WarrantCitation] = field(default_factory=list)
    epistemic_state: str = "observed"
    confidence_bp: int = 10000
    coverage: Coverage = field(default_factory=Coverage)
    contradictions_flag: bool = False


def answer_grounded_question(
    question: str,
    supporting_warrants: List[SealedWarrant],
    contradictions_present: bool = False,
) -> GroundedAnswer:
    """Compose fully warranted, cited answer derived from verified evidence."""
    citations: List[WarrantCitation] = []
    min_confidence = 10000

    for w in supporting_warrants:
        body = w.body
        snippet = str(body.statement)[:120]
        citations.append(
            WarrantCitation(
                warrant_id=w.warrant_id,
                predicate=body.predicate,
                authority=body.authority.value if hasattr(body.authority, "value") else str(body.authority),
                epistemic=body.epistemic_state.value if hasattr(body.epistemic_state, "value") else str(body.epistemic_state),
                confidence_bp=body.confidence.score_bp,
                statement_snippet=snippet,
            )
        )
        if body.confidence.score_bp < min_confidence:
            min_confidence = body.confidence.score_bp

    if not supporting_warrants:
        answer_text = "No verified warrants found covering the requested question."
        epistemic = "unknown"
        min_confidence = 0
        cov = Coverage(status="unknown", scope=question, reasons=[{"code": "NO_EVIDENCE", "message": "No warrants found"}])
    else:
        answer_text = f"Verified across {len(supporting_warrants)} evidentiary warrants."
        epistemic = "derived"
        cov = Coverage(status="complete", scope=question, examined_count=len(supporting_warrants))

    ans_id = "ans1_" + sha256_canonical({
        "citations": [c.warrant_id for c in citations],
        "question": question,
    })

    return GroundedAnswer(
        answer_id=ans_id,
        question=question,
        answer_text=answer_text,
        citations=citations,
        epistemic_state=epistemic,
        confidence_bp=min_confidence,
        coverage=cov,
        contradictions_flag=contradictions_present,
    )
