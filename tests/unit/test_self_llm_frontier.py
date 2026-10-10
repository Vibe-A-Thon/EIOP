"""Tests for Enterprise Self-LLM Frontier Neural & GenAI Engine.

Validates:
1. Cognitive Tiers (Opus, Sonnet, Haiku, Reasoning-R1, Embedding-Multimodal)
2. Tensor Math (RoPE, RMSNorm, Softmax, Cosine Similarity, Top-K, Top-P, Min-P)
3. Tokenization & Matryoshka Dense Vector Embeddings
4. Deliberative Multi-Stage Chain-of-Thought Reasoning
5. Structured & Constrained JSON Schema Decoding
6. Streaming Generation with SSE Chunk Deltas
7. Explainable AI (XAI) Attribution, Counterfactuals & Uncertainty Quantification
8. Speculative Decoding Verification Loop
9. FastAPI Endpoints for LLM Generation, Streaming, Explainability & Embeddings
"""

import json
import pytest
from fastapi.testclient import TestClient

from apps.api.app import create_app
from eoip.graph.memory import MemoryGraphStore
from eoip.models.self_llm import (
    CognitiveTier,
    GenerationConfig,
    GenerationResult,
    SelfLLMEngine,
    TensorMath,
    TIER_PROFILES,
    get_self_llm_engine,
)


# ---------------------------------------------------------------------------
# 1. Test Cognitive Tiers and Profiles
# ---------------------------------------------------------------------------
def test_cognitive_tiers_and_profiles():
    assert len(CognitiveTier) == 5
    assert CognitiveTier.OPUS_FRONTIER.value == "OPUS_FRONTIER"
    assert CognitiveTier.SONNET_BALANCED.value == "SONNET_BALANCED"
    assert CognitiveTier.HAIKU_REALTIME.value == "HAIKU_REALTIME"
    assert CognitiveTier.REASONING_R1.value == "REASONING_R1"
    assert CognitiveTier.EMBEDDING_MULTIMODAL.value == "EMBEDDING_MULTIMODAL"

    for tier in CognitiveTier:
        profile = TIER_PROFILES[tier]
        assert profile.tier == tier
        assert profile.context_window > 0
        assert profile.hidden_dim > 0
        assert profile.num_heads > 0
        assert len(profile.name) > 0


# ---------------------------------------------------------------------------
# 2. Test Tensor Math & Transformer Primitives
# ---------------------------------------------------------------------------
def test_tensor_math_primitives():
    # Dot product & norm
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    assert TensorMath.dot_product(v1, v2) == 32.0
    assert TensorMath.vector_norm([3.0, 4.0]) == 5.0
    assert 0.95 < TensorMath.cosine_similarity(v1, v2) <= 1.0

    # RMSNorm
    normed = TensorMath.rms_norm([1.0, 2.0, 3.0, 4.0])
    assert len(normed) == 4
    assert pytest.approx(sum(x * x for x in normed) / len(normed), rel=1e-2) == 1.0

    # RoPE (Rotary Position Embeddings)
    rope_v = [1.0, 0.5, 0.8, 0.2]
    rot0 = TensorMath.apply_rope(rope_v, position=0)
    rot10 = TensorMath.apply_rope(rope_v, position=10)
    assert len(rot0) == len(rope_v)
    assert rot0[0] == pytest.approx(rope_v[0])  # cos(0)=1, sin(0)=0
    assert rot10 != rot0

    # Softmax
    probs = TensorMath.softmax([2.0, 1.0, 0.1], temperature=1.0)
    assert len(probs) == 3
    assert pytest.approx(sum(probs), rel=1e-5) == 1.0
    assert probs[0] > probs[1] > probs[2]

    # Sampling filters (Top-K, Top-P, Min-P)
    raw_probs = [0.6, 0.25, 0.1, 0.04, 0.01]
    filtered = TensorMath.apply_top_k_top_p_min_p(raw_probs, top_k=3, top_p=0.9, min_p=0.05)
    assert len(filtered) == 5
    assert pytest.approx(sum(filtered), rel=1e-5) == 1.0
    assert filtered[4] == 0.0  # pruned by min_p


# ---------------------------------------------------------------------------
# 3. Test Tokenization and Matryoshka Dense Embeddings
# ---------------------------------------------------------------------------
def test_tokenizer_and_embedding():
    engine = get_self_llm_engine()

    text = "Enterprise Knowledge Graph for Microservice Architecture"
    tokens = engine.tokenize(text)
    assert len(tokens) >= 5
    assert all(isinstance(t, int) for t in tokens)

    # Embedding with default dimension (1536)
    emb1536 = engine.embed(text, dimensions=1536)
    assert len(emb1536) == 1536
    norm = TensorMath.vector_norm(emb1536)
    assert pytest.approx(norm, rel=1e-3) == 1.0

    # Matryoshka adaptive dimension projection (512)
    emb512 = engine.embed(text, dimensions=512)
    assert len(emb512) == 512
    norm512 = TensorMath.vector_norm(emb512)
    assert pytest.approx(norm512, rel=1e-3) == 1.0


# ---------------------------------------------------------------------------
# 4. Test Opus Frontier Multi-Stage Deliberative Reasoning
# ---------------------------------------------------------------------------
def test_opus_frontier_generation():
    engine = get_self_llm_engine()

    prompt = "Design a resilient event-driven data pipeline across multiple regions."
    cfg = GenerationConfig(tier=CognitiveTier.OPUS_FRONTIER, enable_xai=True)
    res = engine.generate(prompt, config=cfg)

    assert isinstance(res, GenerationResult)
    assert res.tier == CognitiveTier.OPUS_FRONTIER
    assert "Opus" in res.model_name
    assert len(res.content) > 50
    assert len(res.reasoning_trace) >= 4
    assert any("Decomposing goal" in step for step in res.reasoning_trace)
    assert any("Self-Critique" in step for step in res.reasoning_trace)
    assert res.tokens_generated > 0
    assert res.latency_ms >= 0.0


# ---------------------------------------------------------------------------
# 5. Test Constrained & Structured JSON Decoding
# ---------------------------------------------------------------------------
def test_structured_json_decoding():
    engine = get_self_llm_engine()

    schema = {
        "type": "object",
        "properties": {
            "service_name": {"type": "string"},
            "replica_count": {"type": "integer"},
            "is_ha_enabled": {"type": "boolean"},
            "endpoints": {"type": "array"},
        },
        "required": ["service_name", "replica_count"],
    }

    cfg = GenerationConfig(
        tier=CognitiveTier.SONNET_BALANCED,
        json_schema=schema,
    )
    res = engine.generate("Generate service configuration", config=cfg)

    assert res.structured_json is not None
    assert "service_name" in res.structured_json
    assert "replica_count" in res.structured_json
    assert res.structured_json["replica_count"] == 100
    assert res.structured_json["is_ha_enabled"] is True
    assert isinstance(res.structured_json["endpoints"], list)


# ---------------------------------------------------------------------------
# 6. Test Progressive Token Delta Streaming
# ---------------------------------------------------------------------------
def test_streaming_generation():
    engine = get_self_llm_engine()

    cfg = GenerationConfig(tier=CognitiveTier.HAIKU_REALTIME)
    chunks = list(engine.generate_stream("Summarize system latency trends", config=cfg))

    assert len(chunks) >= 3
    assert chunks[0].index == 0
    assert chunks[-1].is_final is True
    assert len(chunks[-1].accumulated_content) > 0
    assert chunks[0].chunk_id == chunks[-1].chunk_id


# ---------------------------------------------------------------------------
# 7. Test XAI Explainability (Attribution, Citations & Counterfactuals)
# ---------------------------------------------------------------------------
def test_xai_explainability():
    engine = get_self_llm_engine()

    prompt = "Why does PaymentGateway depend on AuthorizationService?"
    cfg = GenerationConfig(tier=CognitiveTier.OPUS_FRONTIER, enable_xai=True)
    res = engine.generate(prompt, config=cfg)

    assert res.xai is not None
    assert len(res.xai.token_attributions) > 0
    assert any(attr.grounded_entity is not None for attr in res.xai.token_attributions)

    # Verify neuro-symbolic citations
    assert len(res.xai.neuro_symbolic_citations) > 0
    citation = res.xai.neuro_symbolic_citations[0]
    assert "claim" in citation
    assert "triple" in citation
    assert citation["confidence"] >= 0.80

    # Verify counterfactual reasoning
    assert len(res.xai.counterfactuals) > 0
    cf = res.xai.counterfactuals[0]
    assert len(cf.premise) > 0
    assert len(cf.alternative_hypothesis) > 0
    assert isinstance(cf.impact_delta, float)

    # Uncertainty calibration
    assert 0.0 <= res.xai.epistemic_uncertainty <= 1.0
    assert 0.0 <= res.xai.aleatoric_uncertainty <= 1.0
    assert res.xai.conformal_coverage_pct >= 90.0
    assert res.xai.honest_abstain is False


# ---------------------------------------------------------------------------
# 8. Test Speculative Decoding Acceleration
# ---------------------------------------------------------------------------
def test_speculative_decoding():
    engine = get_self_llm_engine()

    prompt = "Analyze database deadlock prevention algorithms."
    cfg = GenerationConfig(tier=CognitiveTier.OPUS_FRONTIER)
    res = engine.generate(prompt, config=cfg)

    assert res.speculative_accepted_tokens > 0


# ---------------------------------------------------------------------------
# 9. Test Self-LLM FastAPI REST Endpoints via TestClient
# ---------------------------------------------------------------------------
def test_self_llm_fastapi_endpoints():
    store = MemoryGraphStore()
    app = create_app(store)
    client = TestClient(app)

    # 1. GET /api/v1/brain/llm/models
    res = client.get("/api/v1/brain/llm/models")
    assert res.status_code == 200
    models = res.json()
    assert len(models) == 5
    tier_names = {m["tier"] for m in models}
    assert "OPUS_FRONTIER" in tier_names
    assert "SONNET_BALANCED" in tier_names

    # 2. POST /api/v1/brain/llm/generate
    res = client.post(
        "/api/v1/brain/llm/generate",
        json={
            "prompt": "Synthesize microservice architecture requirements",
            "tier": "OPUS_FRONTIER",
            "enable_xai": True,
        },
    )
    assert res.status_code == 200
    gen = res.json()
    assert gen["tier"] == "OPUS_FRONTIER"
    assert len(gen["content"]) > 0
    assert len(gen["reasoning_trace"]) >= 1
    assert gen["xai"] is not None
    assert len(gen["xai"]["token_attributions"]) > 0

    # 3. POST /api/v1/brain/llm/stream
    res = client.post(
        "/api/v1/brain/llm/stream",
        json={
            "prompt": "Fast stream response",
            "tier": "HAIKU_REALTIME",
        },
    )
    assert res.status_code == 200
    chunks = res.json()
    assert len(chunks) >= 1
    assert "delta" in chunks[0]
    assert chunks[-1]["is_final"] is True

    # 4. POST /api/v1/brain/llm/explain
    res = client.post(
        "/api/v1/brain/llm/explain",
        json={
            "prompt": "Explain database bottleneck causes",
            "tier": "OPUS_FRONTIER",
        },
    )
    assert res.status_code == 200
    exp = res.json()
    assert "xai" in exp
    assert len(exp["xai"]["counterfactuals"]) > 0

    # 5. POST /api/v1/brain/llm/tokenize
    res = client.post(
        "/api/v1/brain/llm/tokenize",
        json={"text": "Enterprise Ontology Intelligence"},
    )
    assert res.status_code == 200
    tok = res.json()
    assert tok["token_count"] >= 3

    # 6. POST /api/v1/brain/llm/embed
    res = client.post(
        "/api/v1/brain/llm/embed",
        json={"text": "Semantic Graph Vectors", "dimensions": 512},
    )
    assert res.status_code == 200
    emb = res.json()
    assert emb["dimensions"] == 512
    assert len(emb["embedding"]) == 512

    # 7. POST /api/v1/brain/ask with Tier & XAI
    res = client.post(
        "/api/v1/brain/ask",
        json={
            "query": "Evaluate reliability metrics for payment gateway",
            "tier": "OPUS_FRONTIER",
        },
    )
    assert res.status_code == 200
    ans = res.json()
    assert ans["cognitive_tier"] == "OPUS_FRONTIER"
    assert ans["xai"] is not None
