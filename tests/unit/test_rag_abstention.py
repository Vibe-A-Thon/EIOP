"""GAP-KRAG-007/008/009 — GraphRAG abstention, calibrated confidence, evidence manifest."""

from datetime import UTC, datetime

import pytest

from eoip.graph.rag_router import (
    AbstentionThresholds,
    EvidenceManifest,
    RAGAbstentionPolicy,
    RAGResult,
    RAGRouter,
    RAG_PATTERNS,
)
from eoip.graph.memory import MemoryGraphStore

NOW = datetime(2026, 10, 4, tzinfo=UTC)


def make_store(n: int = 0, authority: float = 0.8, verified: bool = True) -> MemoryGraphStore:
    store = MemoryGraphStore()
    for i in range(n):
        props = {
            "canonical_id": f"urn:eoip:entity:test:{i + 1}",
            "name": f"entity {i + 1}",
            "confidence": authority,
        }
        if verified:
            props["trust_updated_at"] = NOW.isoformat()
        store.upsert_vertex("GenericEntity", props)
    return store


def result_with_sources(n: int, **metadata) -> RAGResult:
    return RAGResult(
        answer="answer",
        pattern="simple",
        confidence=0.6,
        sources=[f"urn:eoip:entity:test:{i + 1}" for i in range(n)],
        metadata=metadata,
    )


def policy(**overrides) -> RAGAbstentionPolicy:
    overrides.setdefault("now", NOW)
    return RAGAbstentionPolicy(AbstentionThresholds(**overrides))


def test_abstains_when_no_evidence():
    router = RAGRouter(make_store(), policy())
    out = router.route("unrelated query about nothing at all xyzzy")
    assert out["abstained"] is True
    assert "NO_RETRIEVED_EVIDENCE" in out["abstention_reasons"]
    assert out["confidence"] == 0.0
    assert out["missing_evidence"]


def test_abstains_when_low_authority_sources():
    store = make_store(n=3, authority=0.05)
    router = RAGRouter(store, policy(min_avg_authority=0.5, min_coverage=0.0))
    out = router.route("entity 1")
    assert out["abstained"] is True
    assert "LOW_SOURCE_AUTHORITY" in out["abstention_reasons"]


def test_abstains_when_entities_below_threshold():
    store = make_store(n=1)
    router = RAGRouter(store, policy(min_entities=3, min_coverage=0.0))
    out = router.route("entity 1")
    assert out["abstained"] is True
    assert "INSUFFICIENT_ENTITIES" in out["abstention_reasons"]


def test_abstains_when_paths_below_threshold():
    store = make_store(n=2)
    router = RAGRouter(store, policy(min_paths=2, min_coverage=0.0))
    out = router.route("entity 1")
    assert out["abstained"] is True
    assert "INSUFFICIENT_PATHS" in out["abstention_reasons"]


def test_answers_with_manifest_on_sufficient_evidence():
    store = make_store(n=5)
    router = RAGRouter(store, policy())
    out = router.route("entity 1")
    assert out["abstained"] is False
    assert out["confidence"] > 0.0
    manifest = out["evidence_manifest"]
    assert manifest is not None
    assert manifest["entity_count"] == 5
    assert len(manifest["items"]) == 5
    assert all(i["id"].startswith("urn:eoip:rag:evidence:") for i in manifest["items"])
    assert manifest["avg_authority"] == pytest.approx(0.8)
    assert manifest["avg_recency"] == pytest.approx(1.0)
    assert manifest["coverage"] == pytest.approx(1.0)


def test_confidence_monotonic_in_evidence_count():
    p = policy(target_evidence_items=10)
    store = MemoryGraphStore()
    scores = []
    for n in (1, 2, 4, 8, 16):
        confs = [p.calibrate_confidence(p.build_manifest(store, result_with_sources(k)))
                 for k in range(1, n + 1)]
        scores.append(confs[-1])
    assert scores == sorted(scores)
    assert len(set(scores)) == len(scores)  # strictly increasing


def test_confidence_ignores_model_self_confidence():
    p = policy()
    store = make_store(n=5)
    low = result_with_sources(5)
    low.confidence = 0.01
    high = result_with_sources(5)
    high.confidence = 0.99
    assert p.calibrate_confidence(p.build_manifest(store, low)) == \
        p.calibrate_confidence(p.build_manifest(store, high))


def test_stale_sources_reduce_confidence():
    store = make_store(n=4, verified=False)
    p = policy()
    manifest = p.build_manifest(store, result_with_sources(4))
    fresh = make_store(n=4, verified=True)
    fresh_manifest = p.build_manifest(fresh, result_with_sources(4))
    assert p.calibrate_confidence(manifest) < p.calibrate_confidence(fresh_manifest)


def test_all_seventeen_patterns_return_abstention_fields():
    store = make_store(n=6)
    router = RAGRouter(store, policy())
    for pattern in RAG_PATTERNS:
        out = router.route("entity 1 and entity 2 impact path?", pattern=pattern.name)
        assert "abstained" in out, pattern.name
        assert "evidence_manifest" in out, pattern.name
        assert "confidence" in out, pattern.name


def test_threshold_defaults_are_lenient_enough_for_normal_answers():
    store = make_store(n=5)
    router = RAGRouter(store)  # default policy
    out = router.route("entity 1")
    assert out["abstained"] is False
    assert out["evidence_manifest"]["entity_count"] == 5
