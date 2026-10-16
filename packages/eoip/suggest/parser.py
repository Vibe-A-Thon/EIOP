"""Deterministic template/semantic-parser tier for the §1.2 question taxonomy.

Maps natural-language questions to candidate ``QueryPlan`` shapes *without an
LLM* (SR-NLQ-001). Ten intents are recognized: lookup, traversal, impact,
ownership, change-history, coverage, temporal, aggregation, similarity and
explain-why. An optional LLM-assist hook (External gate) may add candidates
for open-ended phrasing, but the deterministic tier never depends on it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from eoip.contracts.query_plan import EvidenceMode, QueryIntent, QueryPlan
from eoip.suggest.models import COST_TIERS, AnswerMode

IntentName = Literal[
    "lookup", "traversal", "impact", "ownership", "change-history",
    "coverage", "temporal", "aggregation", "similarity", "explain-why",
]

# Keyword evidence per intent. Score = sum of matched pattern weights; the
# highest-scoring intent wins. Deterministic and order-independent.
_INTENT_PATTERNS: dict[str, list[tuple[str, float]]] = {
    "lookup": [
        (r"\bwhat is\b", 1.0), (r"\bwho is\b", 1.0), (r"\bfind\b", 0.8),
        (r"\bshow me\b", 0.8), (r"\bdetails?\b", 0.6), (r"\blookup\b", 1.5),
        (r"\bget\b", 0.5), (r"\bdescribe\b", 0.9),
    ],
    "traversal": [
        (r"\bdepends? on\b", 1.5), (r"\bupstream\b", 1.2), (r"\bdownstream\b", 1.2),
        (r"\bconnected to\b", 1.0), (r"\brelated to\b", 1.0), (r"\bneighbors?\b", 1.2),
        (r"\bpath (from|to|between)\b", 1.5), (r"\bhops?\b", 0.8), (r"\btraverse\b", 1.5),
    ],
    "impact": [
        (r"\bimpact\b", 1.5), (r"\bblast radius\b", 2.0), (r"\baffect(?:ed|s)?\b", 1.2),
        (r"\bif .{1,40} (goes? down|fails?)\b", 1.5), (r"\bwhat breaks\b", 1.5),
        (r"\brisk of\b", 1.0), (r"\bripple\b", 1.0), (r"\bconsequence", 1.0),
    ],
    "ownership": [
        (r"\bwho owns\b", 2.0), (r"\bowner(s|ship)?\b", 1.5), (r"\bresponsible for\b", 1.5),
        (r"\bteam\b.{0,30}\b(of|for)\b", 0.8), (r"\bcontact for\b", 1.2),
        (r"\baccountable\b", 1.2), (r"\bescalat", 0.8),
    ],
    "change-history": [
        (r"\bchange[sd]?\b", 1.2), (r"\bhistory\b", 1.2), (r"\brecent (changes|updates|edits)\b", 1.5),
        (r"\bwho (changed|modified|updated)\b", 1.5), (r"\bwhen was\b", 1.0),
        (r"\brevision", 1.0), (r"\baudit (trail|log)\b", 1.2), (r"\bcommit", 0.6),
    ],
    "coverage": [
        (r"\bcoverage\b", 2.0), (r"\bwhat (do we know|is tracked|sources)\b", 1.2),
        (r"\bingested\b", 1.0), (r"\bmissing\b", 0.8), (r"\bgaps?\b", 1.0),
        (r"\bmonitored\b", 0.8), (r"\bnot .{0,20}(ingested|tracked|covered)\b", 1.2),
    ],
    "temporal": [
        (r"\bas of\b", 1.5), (r"\bat that time\b", 1.5), (r"\blast (week|month|quarter|year)\b", 1.2),
        (r"\bbetween\b", 1.0), (r"\bwhen\b", 0.8), (r"\b(before|after)\b", 0.8),
        (r"\bpoint[- ]in[- ]time\b", 1.8), (r"\bback then\b", 1.5), (r"\bon (\d{4}-\d{2}-\d{2})\b", 1.8),
    ],
    "aggregation": [
        (r"\bhow many\b", 1.8), (r"\bcount\b", 1.5), (r"\baverage\b", 1.2),
        (r"\bsum\b", 1.0), (r"\bmost\b", 1.0), (r"\btop \d+\b", 1.5),
        (r"\bper (team|domain|system)\b", 1.2), (r"\bgroup(ed)? by\b", 1.5),
        (r"\bdistribution\b", 1.0), (r"\bstatistics?\b", 1.0),
    ],
    "similarity": [
        (r"\bsimilar to\b", 2.0), (r"\blike this\b", 1.2), (r"\banalogous\b", 1.5),
        (r"\bcompare\b", 1.2), (r"\bclosest\b", 1.2), (r"\bduplicates?\b", 1.2),
        (r"\bcousins?\b", 1.0), (r"\bresembl", 1.2),
    ],
    "explain-why": [
        (r"\bwhy\b", 1.8), (r"\breason\b", 1.2), (r"\broot cause\b", 1.5),
        (r"\bexplain\b", 1.5), (r"\bwhat caused\b", 1.5), (r"\bbecause\b", 1.0),
        (r"\bjustify\b", 1.0), (r"\brationale\b", 1.2),
    ],
}

# QueryPlan shape per intent (SR-NLQ-001: templates emit QueryPlan IR).
_PLAN_SHAPES: dict[str, dict] = {
    "lookup": {"intent": "SEARCH", "max_depth": 1, "result_limit": 50, "timeout_ms": 500, "evidence_mode": "SUMMARY"},
    "traversal": {"intent": "PATH", "max_depth": 4, "result_limit": 100, "timeout_ms": 2000, "evidence_mode": "SUMMARY"},
    "impact": {"intent": "IMPACT", "max_depth": 5, "result_limit": 200, "timeout_ms": 5000, "evidence_mode": "FULL"},
    "ownership": {"intent": "NEIGHBORHOOD", "max_depth": 2, "result_limit": 50, "timeout_ms": 1000, "evidence_mode": "SUMMARY"},
    "change-history": {"intent": "LINEAGE", "max_depth": 3, "result_limit": 100, "timeout_ms": 2000, "evidence_mode": "FULL"},
    "coverage": {"intent": "SEARCH", "max_depth": 1, "result_limit": 500, "timeout_ms": 5000, "evidence_mode": "SUMMARY"},
    "temporal": {"intent": "LINEAGE", "max_depth": 3, "result_limit": 100, "timeout_ms": 2000, "evidence_mode": "FULL"},
    "aggregation": {"intent": "SEARCH", "max_depth": 1, "result_limit": 500, "timeout_ms": 2000, "evidence_mode": "NONE"},
    "similarity": {"intent": "SEARCH", "max_depth": 2, "result_limit": 100, "timeout_ms": 5000, "evidence_mode": "SUMMARY"},
    "explain-why": {"intent": "TRACEABILITY", "max_depth": 4, "result_limit": 100, "timeout_ms": 5000, "evidence_mode": "FULL"},
}

_INTENT_TIER: dict[str, str] = {
    "lookup": "fast", "traversal": "moderate", "impact": "heavy", "ownership": "fast",
    "change-history": "moderate", "coverage": "expensive", "temporal": "moderate",
    "aggregation": "expensive", "similarity": "expensive", "explain-why": "heavy",
}

_RESULT_SHAPES: dict[str, dict] = {
    "lookup": {"kind": "entity_list", "columns": ["entity_id", "type", "name", "source_system"]},
    "traversal": {"kind": "path_set", "columns": ["path", "hops", "via"]},
    "impact": {"kind": "impacted_set", "columns": ["entity_id", "name", "depth", "relationship", "criticality"]},
    "ownership": {"kind": "entity_list", "columns": ["entity_id", "name", "owner", "team", "contact"]},
    "change-history": {"kind": "timeline", "columns": ["revision_id", "changed_at", "changed_by", "change_type"]},
    "coverage": {"kind": "coverage_matrix", "columns": ["source_system", "domain", "entity_count", "last_seen"]},
    "temporal": {"kind": "timeline", "columns": ["entity_id", "state_at", "valid_at"]},
    "aggregation": {"kind": "aggregate_table", "columns": ["group_key", "metric", "value"]},
    "similarity": {"kind": "ranked_entity_list", "columns": ["entity_id", "name", "similarity_score"]},
    "explain-why": {"kind": "evidence_trail", "columns": ["premise", "path", "confidence"]},
}

_QUOTED_RE = re.compile(r"[\"'‘“](.+?)[\"'’”]")


@dataclass(frozen=True)
class ParsedQuestion:
    """Deterministic parse of the question text."""

    question: str
    normalized: str
    intent_scores: dict[str, float]
    intent: str | None
    mentions: tuple[str, ...]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().casefold())


def score_intents(normalized: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for intent, patterns in _INTENT_PATTERNS.items():
        total = 0.0
        for pattern, weight in patterns:
            if re.search(pattern, normalized):
                total += weight
        if total > 0:
            scores[intent] = round(total, 3)
    return scores


def extract_mentions(normalized: str) -> tuple[str, ...]:
    """Entity mentions: quoted spans first, then known suffix tokens.

    Quoted spans are exact; unquoted mentions are trimmed of leading stopwords.
    """
    raw = normalized.strip().rstrip("?").strip()
    quoted = [m.group(1).strip() for m in _QUOTED_RE.finditer(raw)]
    if quoted:
        return tuple(dict.fromkeys(quoted))
    # Strip leading interrogative/verb phrases to leave a candidate tail.
    tail = re.split(
        r"^(?:please\s+)?(?:can you\s+|could you\s+)?(?:what is|who is|who owns|"
        r"show me|find|get|list|describe|explain|why is|why did|tell me about)\s+",
        raw, maxsplit=1,
    )
    candidate = tail[-1].strip() if len(tail) > 1 else ""
    candidate = re.sub(
        r"\b(the|a|an|of|for|in|on|at|to|from|my|our|me|any|all|all of)\b", " ", candidate
    )
    candidate = re.sub(r"\s+", " ", candidate).strip()
    if not candidate:
        return ()
    # Keep the longest noun-ish span (up to 6 words).
    words = candidate.split()[:6]
    return (" ".join(words),)


def parse_question(question: str) -> ParsedQuestion:
    normalized = _normalize(question)
    scores = score_intents(normalized)
    intent = max(scores, key=scores.get) if scores else None
    return ParsedQuestion(
        question=question,
        normalized=normalized,
        intent_scores=scores,
        intent=intent,
        mentions=extract_mentions(normalized),
    )


def plan_for_intent(intent: str, anchors: list[str]) -> QueryIntent | None:
    shape = _PLAN_SHAPES.get(intent)
    if shape is None:
        return None
    return QueryPlan(
        intent=shape["intent"],  # type: ignore[arg-type]
        anchors=list(anchors),
        max_depth=shape["max_depth"],
        result_limit=shape["result_limit"],
        timeout_ms=shape["timeout_ms"],
        evidence_mode=shape["evidence_mode"],  # type: ignore[arg-type]
    )


def cost_tier_for_intent(intent: str) -> str:
    return _INTENT_TIER.get(intent, "moderate")


def result_shape_for_intent(intent: str) -> dict:
    return dict(_RESULT_SHAPES.get(intent, _RESULT_SHAPES["lookup"]))


def paraphrase(intent: str, mention: str | None, question: str) -> str:
    templates = {
        "lookup": f"Look up details for {mention}" if mention else "Look up the referenced entity",
        "traversal": f"Show the dependency path around {mention}" if mention else "Show dependency paths for the referenced entity",
        "impact": f"Compute the blast radius if {mention} fails" if mention else "Compute the blast radius of the referenced entity",
        "ownership": f"Find who owns {mention}" if mention else "Find the owner of the referenced entity",
        "change-history": f"List recent changes to {mention}" if mention else "List recent changes to the referenced entity",
        "coverage": f"Show what data we have on {mention}" if mention else "Show data coverage and ingestion status",
        "temporal": f"Show the state of {mention} at the requested time" if mention else "Show the state of the referenced entity at the requested time",
        "aggregation": f"Aggregate counts and metrics for {mention}" if mention else "Aggregate counts and metrics over the matching entities",
        "similarity": f"Find entities similar to {mention}" if mention else "Find entities similar to the referenced entity",
        "explain-why": f"Explain why, with the evidence trail, for: {question.strip('?')}",
    }
    return templates.get(intent, question.strip("?"))


def coverage_note(intent: str, mention: str | None, domains: list[str]) -> str:
    domain_txt = ", ".join(domains) if domains else "all ingested domains"
    base = {
        "lookup": "Entity properties and source aliases",
        "traversal": "Relationship edges across ingested source systems",
        "impact": "Dependency edges plus ownership and deployment links",
        "ownership": "Ownership/team edges and identity-resolved persons",
        "change-history": "Revision and audit-event history (bitemporal record)",
        "coverage": "Source registry and ingestion coverage index",
        "temporal": "Bitemporal revision timeline (valid + transaction time)",
        "aggregation": "Entity counts grouped over the graph store",
        "similarity": "Entity features and relationship neighborhoods",
        "explain-why": "Paths, rules and provenance edges with evidence",
    }.get(intent, "Graph store entities and edges")
    scope = f" for '{mention}'" if mention else ""
    return f"{base}{scope} across {domain_txt}."


def default_answer_mode(intent: str) -> AnswerMode:
    from eoip.suggest.models import choose_answer_mode

    return choose_answer_mode(intent)
