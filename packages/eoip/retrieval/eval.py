"""Deterministic RAG evaluation harness (FR-RAG-005).

Runs `eoip.retrieval.service.retrieve` over a set of golden cases and
computes quality metrics without any model: fact precision/recall against
expected canonical IDs, evidence coverage (share of retrieved relationship
contexts carrying citations), and groundedness (every non-summary context
has at least one citation). Cases pointing at nonexistent entities are
recorded as failed results instead of raising.
"""

from __future__ import annotations

import time

from eoip.retrieval.service import retrieve
from pydantic import BaseModel, Field


class EvalCase(BaseModel):
    id: str
    question: str
    canonical_id: str
    expected_facts: list[str] = Field(default_factory=list)
    expected_evidence_min: int = 1
    strategy: str | None = None


class EvalResult(BaseModel):
    case_id: str
    strategy_used: str
    facts_precision: float
    facts_recall: float
    evidence_coverage: float
    grounded: bool
    latency_ms: float
    passed: bool
    detail: str


def _fact_matches(expected: str, canonical_id: str) -> bool:
    expected = expected.casefold()
    actual = canonical_id.casefold()
    return expected in actual or actual in expected


def _score(result, case: EvalCase) -> tuple[float, float, float, bool, int, int]:
    facts = result.facts or []
    matched = sum(
        1
        for expected in case.expected_facts
        if any(_fact_matches(expected, f["canonical_id"]) for f in facts)
    )
    precision = matched / len(facts) if facts else 0.0
    recall = matched / len(case.expected_facts) if case.expected_facts else 1.0
    relationships = [c for c in result.contexts if c.kind == "relationship"]
    cited = sum(1 for c in relationships if c.citations)
    coverage = cited / len(relationships) if relationships else 1.0
    grounded = all(c.citations or c.kind == "summary" for c in result.contexts)
    return precision, recall, coverage, grounded, cited, matched


def run_eval(store, cases: list[EvalCase], *, synthesize: bool = False) -> list[EvalResult]:
    results: list[EvalResult] = []
    for case in cases:
        started = time.perf_counter()
        try:
            result = retrieve(store, case.canonical_id, case.question, synthesize=synthesize)
        except ValueError as exc:
            latency_ms = round((time.perf_counter() - started) * 1000, 3)
            results.append(
                EvalResult(
                    case_id=case.id,
                    strategy_used="none",
                    facts_precision=0.0,
                    facts_recall=0.0,
                    evidence_coverage=0.0,
                    grounded=False,
                    latency_ms=latency_ms,
                    passed=False,
                    detail=f"entity not found: {exc}",
                )
            )
            continue
        latency_ms = round((time.perf_counter() - started) * 1000, 3)
        precision, recall, coverage, grounded, cited, matched = _score(result, case)
        passed = recall == 1.0 and cited >= case.expected_evidence_min and grounded
        detail = (
            f"strategy={result.strategy}"
            + (f" (expected {case.strategy})" if case.strategy and case.strategy != result.strategy else "")
            + f"; matched {matched}/{len(case.expected_facts)} expected facts"
            f"; cited {cited} relationship context(s)"
        )
        results.append(
            EvalResult(
                case_id=case.id,
                strategy_used=result.strategy,
                facts_precision=round(precision, 4),
                facts_recall=round(recall, 4),
                evidence_coverage=round(coverage, 4),
                grounded=grounded,
                latency_ms=latency_ms,
                passed=passed,
                detail=detail,
            )
        )
    return results
