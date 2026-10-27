"""Feature Engineering engine — graph-aware feature extraction, versioned
feature store, and pipeline with dependency resolution."""

from __future__ import annotations

import hashlib
import math
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from collections.abc import Callable


class FeatureType(Enum):
    STRUCTURAL = "structural"
    TEMPORAL = "temporal"
    SEMANTIC = "semantic"
    TOPOLOGICAL = "topological"
    STATISTICAL = "statistical"
    DERIVED = "derived"


@dataclass
class FeatureDefinition:
    name: str
    feature_type: FeatureType
    extractor: Callable[[str, dict[str, Any], list[str]], float]
    depends_on: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class FeatureRecord:
    entity_id: str
    name: str
    value: float
    feature_type: FeatureType
    computed_at: float = field(default_factory=time.time)
    ttl_seconds: float = 3600.0

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.computed_at) > self.ttl_seconds


@dataclass
class FeatureSet:
    entity_id: str
    features: dict[str, float] = field(default_factory=dict)
    computed_at: float = field(default_factory=time.time)


class FeatureStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: dict[str, dict[str, FeatureRecord]] = defaultdict(dict)

    def put(self, record: FeatureRecord) -> None:
        with self._lock:
            self._store[record.entity_id][record.name] = record

    def put_batch(self, records: list[FeatureRecord]) -> None:
        with self._lock:
            for r in records:
                self._store[r.entity_id][r.name] = r

    def get(self, entity_id: str, name: str) -> FeatureRecord | None:
        with self._lock:
            record = self._store.get(entity_id, {}).get(name)
            if record and not record.is_expired:
                return record
            return None

    def get_vector(self, entity_id: str, feature_names: list[str] | None = None) -> list[float]:
        with self._lock:
            records = self._store.get(entity_id, {})
            if feature_names:
                return [records[n].value for n in feature_names if n in records and not records[n].is_expired]
            return [r.value for r in records.values() if not r.is_expired]

    def evict_expired(self) -> int:
        evicted = 0
        with self._lock:
            for entity_id in list(self._store.keys()):
                records = self._store[entity_id]
                expired = [n for n, r in records.items() if r.is_expired]
                for n in expired:
                    del records[n]
                    evicted += 1
        return evicted

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = sum(len(v) for v in self._store.values())
            return {"entities": len(self._store), "total_features": total}


def _degree_centrality(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    return float(len(neighbors))

def _in_degree(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    return float(props.get("in_degree", len(neighbors) // 2))

def _out_degree(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    return float(props.get("out_degree", len(neighbors) - len(neighbors) // 2))

def _clustering_coefficient(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    n = len(neighbors)
    if n < 2:
        return 0.0
    possible = n * (n - 1) / 2
    actual = float(props.get("neighbor_edges", 0))
    return actual / possible if possible > 0 else 0.0

def _pagerank(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    d = 0.85
    n = max(len(neighbors), 1)
    return (1 - d) + d * (1.0 / n)

def _entity_age_days(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    created = props.get("created_at", time.time())
    return (time.time() - created) / 86400.0

def _update_recency(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    updated = props.get("updated_at", time.time())
    return 1.0 / (1.0 + (time.time() - updated) / 86400.0)

def _text_richness(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    text = str(props.get("text", ""))
    return min(1.0, len(text.split()) / 100.0)

def _property_completeness(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    if not props:
        return 0.0
    filled = sum(1 for v in props.values() if v is not None and v != "")
    return filled / len(props)

def _text_embedding(entity_id: str, props: dict[str, Any], neighbors: list[str]) -> float:
    text = str(props.get("text", entity_id))
    h = hashlib.sha256(text.encode()).hexdigest()
    vals = [int(h[i:i+4], 16) / 65535.0 for i in range(0, 64, 4)]
    return sum(vals) / len(vals)


BUILTIN_EXTRACTORS: list[FeatureDefinition] = [
    FeatureDefinition("degree_centrality", FeatureType.STRUCTURAL, _degree_centrality),
    FeatureDefinition("in_degree", FeatureType.STRUCTURAL, _in_degree),
    FeatureDefinition("out_degree", FeatureType.STRUCTURAL, _out_degree),
    FeatureDefinition("clustering_coefficient", FeatureType.TOPOLOGICAL, _clustering_coefficient),
    FeatureDefinition("pagerank", FeatureType.TOPOLOGICAL, _pagerank),
    FeatureDefinition("entity_age_days", FeatureType.TEMPORAL, _entity_age_days),
    FeatureDefinition("update_recency", FeatureType.TEMPORAL, _update_recency),
    FeatureDefinition("text_richness", FeatureType.SEMANTIC, _text_richness),
    FeatureDefinition("property_completeness", FeatureType.STATISTICAL, _property_completeness),
    FeatureDefinition("text_embedding", FeatureType.SEMANTIC, _text_embedding),
]


class FeaturePipeline:
    def __init__(self, definitions: list[FeatureDefinition] | None = None) -> None:
        self._definitions = {d.name: d for d in (definitions or BUILTIN_EXTRACTORS)}

    def _topological_sort(self) -> list[str]:
        visited: set[str] = set()
        ordered: list[str] = []
        def visit(name: str) -> None:
            if name in visited:
                return
            visited.add(name)
            defn = self._definitions.get(name)
            if defn:
                for dep in defn.depends_on:
                    visit(dep)
            ordered.append(name)
        for name in self._definitions:
            visit(name)
        return ordered

    def compute_for_entity(self, entity_id: str, properties: dict[str, Any],
                           neighbors: list[str]) -> dict[str, float]:
        order = self._topological_sort()
        results: dict[str, float] = {}
        for name in order:
            defn = self._definitions.get(name)
            if defn:
                results[name] = defn.extractor(entity_id, properties, neighbors)
        return results

    def compute_batch(self, entities: list[tuple[str, dict[str, Any], list[str]]]) -> dict[str, dict[str, float]]:
        return {eid: self.compute_for_entity(eid, props, nbrs)
                for eid, props, nbrs in entities}


class FeatureEngine:
    """Top-level Feature Engineering orchestrator."""

    def __init__(self) -> None:
        self._store = FeatureStore()
        self._pipeline = FeaturePipeline()

    @property
    def store(self) -> FeatureStore:
        return self._store

    @property
    def pipeline(self) -> FeaturePipeline:
        return self._pipeline

    def extract(self, entity_id: str, properties: dict[str, Any],
                neighbors: list[str] | None = None) -> dict[str, float]:
        results = self._pipeline.compute_for_entity(entity_id, properties, neighbors or [])
        records = [
            FeatureRecord(entity_id, name, value, FeatureType.STRUCTURAL)
            for name, value in results.items()
        ]
        self._store.put_batch(records)
        return results

    def extract_batch(self, entities: list[tuple[str, dict[str, Any], list[str]]]) -> dict[str, dict[str, float]]:
        all_results = self._pipeline.compute_batch(entities)
        for eid, features in all_results.items():
            records = [FeatureRecord(eid, n, v, FeatureType.STRUCTURAL) for n, v in features.items()]
            self._store.put_batch(records)
        return all_results

    def create_feature_set(self, entity_id: str) -> FeatureSet:
        vector = self._store.get_vector(entity_id)
        return FeatureSet(entity_id=entity_id, features={f"f{i}": v for i, v in enumerate(vector)})

    def get_feature_vector(self, entity_id: str, feature_names: list[str] | None = None) -> list[float]:
        return self._store.get_vector(entity_id, feature_names)

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "feature_engineering",
            "store": self._store.stats(),
            "extractors": len(BUILTIN_EXTRACTORS),
        }


_instance: FeatureEngine | None = None
_lock = threading.Lock()


def get_feature_engine() -> FeatureEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = FeatureEngine()
    return _instance
