"""Temporal & Hybrid Retrieval Engineering (GRAPH-005).

Maintains temporal validity windows for dynamic facts:
- TemporalIndex: validity windows (valid_from, valid_to) per knowledge graph fact
- AsOfQuery: point-in-time point retrieval ("as of timestamp T")
- TemporalRangeQuery: interval-bounded query retrieval
- Temporal evolution timeline tracking
- Integration with hybrid search engine and state time-travel
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from eoip.search.hybrid_engine import get_hybrid_search_engine

logger = logging.getLogger("eoip.retrieval.temporal")


@dataclass
class TemporalFact:
    """Knowledge fact with temporal observation validity window."""

    fact_id: str
    subject: str
    predicate: str
    object_value: Any
    valid_from: float
    valid_to: float | None = None  # None indicates actively valid into future
    confidence: float = 1.0
    recorded_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_valid_at(self, timestamp: float) -> bool:
        if timestamp < self.valid_from:
            return False
        if self.valid_to is not None and timestamp > self.valid_to:
            return False
        return True

    def overlaps_window(self, start: float, end: float) -> bool:
        to_time = self.valid_to if self.valid_to is not None else float("inf")
        return max(self.valid_from, start) <= min(to_time, end)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AsOfQuery:
    """Point-in-time retrieval query specification."""

    as_of_time: float
    subject: str | None = None
    predicate: str | None = None
    min_confidence: float = 0.5


@dataclass
class TemporalRangeQuery:
    """Range-bounded retrieval query specification."""

    start_time: float
    end_time: float
    subject: str | None = None
    predicate: str | None = None


class TemporalIndex:
    """In-memory indexing for temporal facts with fast window matching."""

    def __init__(self) -> None:
        self._facts: dict[str, TemporalFact] = {}
        self._by_subject: dict[str, list[str]] = {}
        self._by_predicate: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    def add_fact(self, fact: TemporalFact) -> None:
        with self._lock:
            # If previous active fact for exact (subject, predicate) exists without valid_to, expire it
            for f_id in self._by_subject.get(fact.subject.lower(), []):
                old = self._facts[f_id]
                if old.predicate.lower() == fact.predicate.lower() and old.valid_to is None:
                    if old.valid_from <= fact.valid_from:
                        old.valid_to = fact.valid_from

            self._facts[fact.fact_id] = fact
            s_key = fact.subject.lower()
            p_key = fact.predicate.lower()
            self._by_subject.setdefault(s_key, []).append(fact.fact_id)
            self._by_predicate.setdefault(p_key, []).append(fact.fact_id)

    def query_as_of(self, query: AsOfQuery) -> list[TemporalFact]:
        """Return facts that were valid at query.as_of_time."""
        with self._lock:
            candidates = self._filter_candidate_ids(query.subject, query.predicate)
            results: list[TemporalFact] = []

            for fid in candidates:
                fact = self._facts[fid]
                if fact.confidence >= query.min_confidence and fact.is_valid_at(query.as_of_time):
                    results.append(fact)

            results.sort(key=lambda f: f.valid_from)
            return results

    def query_range(self, query: TemporalRangeQuery) -> list[TemporalFact]:
        """Return facts whose validity window overlaps [start_time, end_time]."""
        with self._lock:
            candidates = self._filter_candidate_ids(query.subject, query.predicate)
            results: list[TemporalFact] = []

            for fid in candidates:
                fact = self._facts[fid]
                if fact.overlaps_window(query.start_time, query.end_time):
                    results.append(fact)

            results.sort(key=lambda f: f.valid_from)
            return results

    def query_timeline(self, subject: str, predicate: str | None = None) -> list[TemporalFact]:
        """Retrieve chronological history of values for an entity."""
        with self._lock:
            candidates = self._filter_candidate_ids(subject, predicate)
            facts = [self._facts[fid] for fid in candidates]
            facts.sort(key=lambda f: f.valid_from)
            return facts

    def _filter_candidate_ids(self, subject: str | None, predicate: str | None) -> list[str]:
        if subject and predicate:
            s_set = set(self._by_subject.get(subject.lower(), []))
            p_set = set(self._by_predicate.get(predicate.lower(), []))
            return list(s_set.intersection(p_set))
        if subject:
            return list(self._by_subject.get(subject.lower(), []))
        if predicate:
            return list(self._by_predicate.get(predicate.lower(), []))
        return list(self._facts.keys())


class TemporalHybridRetrievalEngine:
    """Combines Temporal validity indexes with semantic and keyword search."""

    _instance: TemporalHybridRetrievalEngine | None = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.temporal_index = TemporalIndex()
        self.hybrid_engine = get_hybrid_search_engine()

    @classmethod
    def get_instance(cls) -> TemporalHybridRetrievalEngine:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def record_fact(
        self,
        fact_id: str,
        subject: str,
        predicate: str,
        object_value: Any,
        valid_from: float,
        valid_to: float | None = None,
        confidence: float = 1.0,
    ) -> TemporalFact:
        fact = TemporalFact(
            fact_id=fact_id,
            subject=subject,
            predicate=predicate,
            object_value=object_value,
            valid_from=valid_from,
            valid_to=valid_to,
            confidence=confidence,
        )
        self.temporal_index.add_fact(fact)
        return fact

    def retrieve_as_of(
        self,
        query_text: str,
        as_of_timestamp: float,
        subject: str | None = None,
    ) -> dict[str, Any]:
        """Hybrid retrieval conditioned on point-in-time validity."""
        as_of_q = AsOfQuery(as_of_time=as_of_timestamp, subject=subject)
        temporal_facts = self.temporal_index.query_as_of(as_of_q)

        # Query hybrid search
        hybrid_res = self.hybrid_engine.search(query_text, top_k=5)

        return {
            "query": query_text,
            "as_of_time": as_of_timestamp,
            "temporal_facts": [f.to_dict() for f in temporal_facts],
            "temporal_fact_count": len(temporal_facts),
            "hybrid_search_hits": hybrid_res.get("hits", []),
        }

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "temporal_hybrid_retrieval",
            "indexed_facts": len(self.temporal_index._facts),
        }


def get_temporal_retrieval_engine() -> TemporalHybridRetrievalEngine:
    return TemporalHybridRetrievalEngine.get_instance()
