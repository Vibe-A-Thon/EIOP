"""Search Analytics & Relevance Tuning Engine (UI-008).

Provides:
- Search event logging with query performance & user engagement metrics
- Analytics aggregation: top queries, zero-result rates, click-through rate (CTR)
- Dynamic relevance tuning: synonym dictionaries, query term boost/bury rules, and stopword filters
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any

logger = logging.getLogger("eoip.search.analytics")


@dataclass
class SearchEvent:
    event_id: str
    query: str
    dialect: str
    latency_ms: float
    result_count: int
    clicked_entity_id: str | None = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SearchMetricsSummary:
    total_searches: int
    zero_result_searches: int
    zero_result_rate: float
    avg_latency_ms: float
    click_through_rate: float
    top_queries: list[tuple[str, int]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_searches": self.total_searches,
            "zero_result_searches": self.zero_result_searches,
            "zero_result_rate": round(self.zero_result_rate, 4),
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "click_through_rate": round(self.click_through_rate, 4),
            "top_queries": self.top_queries,
        }


class SearchAnalyticsEngine:
    """Enterprise search event aggregator and relevance optimizer."""

    def __init__(self) -> None:
        self._events: list[SearchEvent] = []
        self._synonyms: dict[str, set[str]] = {}
        self._boosts: dict[str, float] = {}  # term -> boost multiplier (e.g. 1.5, 0.5)
        self._stopwords: set[str] = {"a", "an", "the", "in", "on", "at", "for", "to"}
        self._lock = threading.Lock()

    def log_search(
        self,
        query: str,
        dialect: str = "TEXT",
        latency_ms: float = 10.0,
        result_count: int = 5,
        clicked_entity_id: str | None = None,
    ) -> SearchEvent:
        import uuid
        event = SearchEvent(
            event_id=f"SE-{uuid.uuid4().hex[:8]}",
            query=query.strip(),
            dialect=dialect,
            latency_ms=latency_ms,
            result_count=result_count,
            clicked_entity_id=clicked_entity_id,
        )
        with self._lock:
            self._events.append(event)
        return event

    def record_click(self, event_id: str, entity_id: str) -> bool:
        with self._lock:
            for ev in self._events:
                if ev.event_id == event_id:
                    ev.clicked_entity_id = entity_id
                    return True
        return False

    def compute_summary(self) -> SearchMetricsSummary:
        with self._lock:
            events = list(self._events)

        if not events:
            return SearchMetricsSummary(0, 0, 0.0, 0.0, 0.0, [])

        total = len(events)
        zero_res = sum(1 for e in events if e.result_count == 0)
        clicked = sum(1 for e in events if e.clicked_entity_id is not None)
        tot_latency = sum(e.latency_ms for e in events)

        # Query frequency
        counts: dict[str, int] = {}
        for e in events:
            q = e.query.lower()
            counts[q] = counts.get(q, 0) + 1
        sorted_queries = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return SearchMetricsSummary(
            total_searches=total,
            zero_result_searches=zero_res,
            zero_result_rate=zero_res / total if total > 0 else 0.0,
            avg_latency_ms=tot_latency / total if total > 0 else 0.0,
            click_through_rate=clicked / total if total > 0 else 0.0,
            top_queries=sorted_queries,
        )

    def add_synonym(self, term: str, synonym: str) -> None:
        with self._lock:
            t = term.lower().strip()
            s = synonym.lower().strip()
            self._synonyms.setdefault(t, set()).add(s)
            self._synonyms.setdefault(s, set()).add(t)

    def set_term_boost(self, term: str, boost_factor: float) -> None:
        with self._lock:
            self._boosts[term.lower().strip()] = max(0.1, boost_factor)

    def apply_relevance_tuning(self, tokens: list[str]) -> list[tuple[str, float]]:
        """Filters stopwords, expands synonyms, applies term boost weights."""
        with self._lock:
            stopwords = set(self._stopwords)
            boosts = dict(self._boosts)
            synonyms = {k: set(v) for k, v in self._synonyms.items()}

        results: list[tuple[str, float]] = []
        for tok in tokens:
            t = tok.lower().strip()
            if t in stopwords:
                continue
            weight = boosts.get(t, 1.0)
            results.append((t, weight))
            if t in synonyms:
                for syn in synonyms[t]:
                    results.append((syn, weight * 0.85))
        return results


_search_analytics_singleton: SearchAnalyticsEngine | None = None
_search_analytics_lock = threading.Lock()


def get_search_analytics_engine() -> SearchAnalyticsEngine:
    global _search_analytics_singleton
    if _search_analytics_singleton is None:
        with _search_analytics_lock:
            if _search_analytics_singleton is None:
                _search_analytics_singleton = SearchAnalyticsEngine()
    return _search_analytics_singleton
