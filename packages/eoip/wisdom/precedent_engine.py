"""Precedent matching and graph search engine for Wisdom Graph (WG-WP-06..10)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from eoip.wisdom.decision_trace import DecisionTrace


@dataclass
class PrecedentMatch:
    trace: DecisionTrace
    similarity_score: float
    matched_tags: List[str]
    relevance_rationale: str


class PrecedentEngine:
    """Indexes decision traces and performs precedent retrieval."""

    def __init__(self) -> None:
        self._traces: Dict[str, DecisionTrace] = {}
        self._tag_index: Dict[str, Set[str]] = {}  # tag -> set of trace_ids

    def index_trace(self, trace: DecisionTrace) -> None:
        self._traces[trace.trace_id] = trace
        for tag in trace.context_tags:
            tag_lower = tag.lower().strip()
            self._tag_index.setdefault(tag_lower, set()).add(trace.trace_id)

    def get_trace(self, trace_id: str) -> Optional[DecisionTrace]:
        return self._traces.get(trace_id)

    def find_precedents(
        self,
        query_situation: str,
        context_tags: Optional[List[str]] = None,
        tenant_id: str = "acme-demo",
        min_similarity: float = 0.2,
        limit: int = 5,
    ) -> List[PrecedentMatch]:
        query_tokens = set(re.findall(r"\w+", query_situation.lower()))
        query_tags = set(t.lower().strip() for t in (context_tags or []))

        matches: List[PrecedentMatch] = []

        for trace in self._traces.values():
            if trace.tenant_id != tenant_id:
                continue

            # Tag similarity (Jaccard)
            trace_tags = set(t.lower().strip() for t in trace.context_tags)
            common_tags = query_tags.intersection(trace_tags)
            tag_score = len(common_tags) / max(1, len(query_tags.union(trace_tags))) if (query_tags or trace_tags) else 0.0

            # Text token overlap
            trace_tokens = set(re.findall(r"\w+", trace.situation.lower()))
            common_tokens = query_tokens.intersection(trace_tokens)
            token_score = len(common_tokens) / max(1, len(query_tokens.union(trace_tokens))) if (query_tokens or trace_tokens) else 0.0

            # Combined score (weighted 50% tags, 50% text)
            combined_score = (0.5 * tag_score) + (0.5 * token_score)

            if combined_score >= min_similarity:
                rationale = (
                    f"Matched {len(common_tags)} context tags ({', '.join(sorted(common_tags))}) "
                    f"and {len(common_tokens)} situational keywords."
                )
                matches.append(
                    PrecedentMatch(
                        trace=trace,
                        similarity_score=round(combined_score, 4),
                        matched_tags=sorted(list(common_tags)),
                        relevance_rationale=rationale,
                    )
                )

        matches.sort(key=lambda m: m.similarity_score, reverse=True)
        return matches[:limit]
