"""Cited-span claim support (CRA-026.7/.8).

Every answer sentence must be backed by a span of the evidence it cites. Support is lexical and strict:
the sentence's content words must be covered by one evidence sentence (>= ``threshold``), every number in
the claim must appear in that span, and a negation in the claim must also appear in the span. Sentences
that fail are removed from the answer and reported as unsupported claims. This is a conservative check
(it under-accepts paraphrase); it never accepts a claim with no overlapping cited evidence.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

_STOP = frozenset(["a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "can", "could", "did", "do", "does", "for", "from", "had", "has", "have", "how", "if", "in", "into", "is", "it", "its", "may", "might", "no", "nor", "not", "of", "on", "or", "our", "should", "so", "such", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "to", "too", "under", "up", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would", "you", "your", "also", "very", "just", "only", "about", "above", "after", "again", "against", "all", "any", "because", "before", "being", "below", "between", "both", "during", "each", "few", "further", "here", "more", "most", "other", "over", "own", "same", "some", "through", "until"])
_NEG = frozenset({"not", "no", "never", "none", "cannot", "without", "nor"})
_CITE = re.compile(r"\[([^\[\]]{1,200})\]")
_SENT = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")
_NUM = re.compile(r"\d+(?:[.,:]\d+)*")


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9_\-]*", text.lower())


def content_tokens(text: str) -> set[str]:
    return {w for w in _words(_CITE.sub(" ", text)) if len(w) > 2 and w not in _STOP and not _NUM.fullmatch(w)}


def numbers(text: str) -> set[str]:
    return set(_NUM.findall(_CITE.sub(" ", text)))


def sentences(text: str) -> list[tuple[str, int, int]]:
    out = []
    for m in _SENT.finditer(text):
        s = m.group(0)
        lead = len(s) - len(s.lstrip())
        stripped = s.strip()
        if stripped:
            out.append((stripped, m.start() + lead, m.start() + lead + len(stripped)))
    return out


def cited_ids(sentence: str) -> list[str]:
    ids: list[str] = []
    for group in _CITE.findall(sentence):
        ids += [x.strip() for x in group.split(",") if x.strip()]
    return ids


@dataclass
class ClaimSupport:
    sentence: str
    supported: bool
    score: float
    assertion_id: str | None = None
    span: dict[str, Any] | None = None
    reason: str = ""
    cited: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _item_text(item: dict) -> str:
    return str(item.get("snippet", item.get("text", "")))


def best_span(claim: str, item: dict) -> tuple[float, tuple[str, int, int] | None]:
    want = content_tokens(claim)
    best: tuple[float, tuple[str, int, int] | None] = (0.0, None)
    if not want:
        return best
    text = _item_text(item)
    sents = sentences(text)
    # single sentences, and adjacent pairs (a claim may join a sentence and its follow-up, e.g. "It ...")
    windows = sents + [(text[a[1]:b[2]], a[1], b[2]) for a, b in zip(sents, sents[1:])]
    for span in windows:
        score = len(want & content_tokens(span[0])) / len(want)
        if score > best[0] or (score == best[0] and best[1] is not None and len(span[0]) < len(best[1][0])):
            best = (score, span)
    return best


def check_claim(claim: str, evidence: list[dict], *, threshold: float = 0.6) -> ClaimSupport:
    cited = cited_ids(claim)
    by_id = {str(e.get("assertion_id")): e for e in evidence}
    if cited and not any(c in by_id for c in cited):
        return ClaimSupport(claim, False, 0.0, reason="cites evidence that was not in the context", cited=cited)
    pool = [by_id[c] for c in cited if c in by_id] or evidence  # uncited: must still be backed by some evidence
    if not content_tokens(claim):
        return ClaimSupport(claim, False, 0.0, reason="no checkable content", cited=cited)
    scored = []
    for item in pool:
        score, span = best_span(claim, item)
        if span is not None:
            scored.append((score, item, span))
    if not scored:
        return ClaimSupport(claim, False, 0.0, reason="no overlapping evidence span", cited=cited)
    score, item, (text, start, end) = max(scored, key=lambda x: x[0])
    span = {"text": text, "start": start, "end": end}
    aid = str(item.get("assertion_id"))
    missing_nums = numbers(claim) - numbers(text)
    if missing_nums:
        return ClaimSupport(claim, False, round(score, 3), aid, span, f"numbers not in evidence: {sorted(missing_nums)}", cited)
    if (set(_words(claim)) & _NEG) and not (set(_words(text)) & _NEG):
        return ClaimSupport(claim, False, round(score, 3), aid, span, "negation not supported by evidence", cited)
    if score < threshold:
        return ClaimSupport(claim, False, round(score, 3), aid, span, f"coverage {score:.2f} < {threshold}", cited)
    return ClaimSupport(claim, True, round(score, 3), aid, span, "", cited)


def extractive_sentences(question: str, evidence: list[dict]) -> list[ClaimSupport]:
    """One cited evidence sentence per accepted item: the span most relevant to the question."""
    q = content_tokens(question)
    out = []
    for item in evidence:
        spans = sentences(_item_text(item))
        if not spans:
            continue
        text, start, end = max(spans, key=lambda s: (len(q & content_tokens(s[0])), -s[1]))
        aid = str(item.get("assertion_id"))
        out.append(ClaimSupport(f"{text.rstrip('.')}. [{aid}]", True, 1.0, aid,
                                {"text": text, "start": start, "end": end}, "verbatim evidence span", [aid]))
    return out
