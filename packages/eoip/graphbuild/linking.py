"""Mention / entity extraction from dictionaries and gazetteers.

Deterministic text annotation: a case-sensitive gazetteer plus a
case-insensitive dictionary are scanned with longest-match-first, emitting
``MENTIONS`` edge proposals (document → entity) with match evidence. No
required external NLP dependency; optional hook may post-filter matches and
its absence is a no-op.
"""

from __future__ import annotations

import re
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field

from eoip.graphbuild.models import GraphDelta, ProposedEdge

MatchHook = Callable[[ProposedEdge], ProposedEdge | None]

_TOKEN_BOUNDARY = re.compile(r"[A-Za-z0-9_]")


class ExtractionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text_id: str
    matches: list[ProposedEdge] = Field(default_factory=list)


class Gazetteer(BaseModel):
    """Dictionary + gazetteer model for mention extraction."""

    model_config = ConfigDict(extra="forbid")

    # canonical entity id -> surface forms (exact, case-sensitive gazetteer)
    entities: dict[str, list[str]] = Field(default_factory=dict)
    # normalized (casefold) alias -> canonical entity id (case-insensitive dict)
    aliases: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def from_entities(cls, entities: dict[str, list[str]], *, case_insensitive: bool = True) -> Gazetteer:
        aliases: dict[str, str] = {}
        for canonical, forms in entities.items():
            for form in forms:
                if case_insensitive:
                    aliases.setdefault(form.casefold(), canonical)
        return cls(entities=entities, aliases=aliases)

    def longest_match(self, text: str, start: int) -> tuple[str, str] | None:
        """Return (surface, canonical_id) of the longest match at ``start``."""
        tail = text[start:]
        best: tuple[str, str] | None = None
        for canonical, forms in self.entities.items():
            for form in forms:
                if tail.startswith(form) and (best is None or len(form) > len(best[0])):
                    best = (form, canonical)
        lowered = tail.casefold()
        for alias, canonical in self.aliases.items():
            if lowered.startswith(alias) and (best is None or len(alias) > len(best[0])):
                best = (tail[: len(alias)], canonical)
        return best


def _boundary_ok(text: str, start: int, end: int) -> bool:
    before = text[start - 1] if start > 0 else " "
    after = text[end] if end < len(text) else " "
    return not (_TOKEN_BOUNDARY.match(before) or _TOKEN_BOUNDARY.match(after))


def extract_mentions(
    text_id: str,
    text: str,
    gazetteer: Gazetteer,
    hook: MatchHook | None = None,
) -> ExtractionResult:
    """Longest-match-first mention extraction over ``text``.

    Matches must sit on token boundaries; overlapping matches resolve to the
    earliest-starting, longest surface. Emits one ``MENTIONS`` proposal per
    (entity, span).
    """
    matches: list[ProposedEdge] = []
    i = 0
    while i < len(text):
        hit = gazetteer.longest_match(text, i)
        if hit is None:
            i += 1
            continue
        surface, canonical = hit
        end = i + len(surface)
        if not _boundary_ok(text, i, end):
            i += 1
            continue
        edge = ProposedEdge.make(
            "MENTIONS",
            text_id,
            canonical,
            score=1.0,
            method="mention:dictionary+gazetteer",
            surface=surface,
            start=i,
            end=end,
        )
        if hook is not None:
            edge = hook(edge)
        if edge is not None:
            matches.append(edge)
        i = end
    return ExtractionResult(text_id=text_id, matches=matches)


def extract_mentions_batch(
    documents: dict[str, str],
    gazetteer: Gazetteer,
    hook: MatchHook | None = None,
) -> GraphDelta:
    """Run extraction over many documents; aggregate into one delta."""
    all_matches: list[ProposedEdge] = []
    for text_id in sorted(documents):
        all_matches.extend(extract_mentions(text_id, documents[text_id], gazetteer, hook).matches)
    return GraphDelta.make("mentions", repr(sorted(documents)), edges=all_matches)
