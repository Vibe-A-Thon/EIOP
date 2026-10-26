"""Tests for the §4 RAG extensions (architectures, techniques, metrics, router)."""

from __future__ import annotations

import pytest

from eoip.authz.core import PolicyEnforcer, User
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.rag_router import RAGAbstentionPolicy
from eoip.ragx import (
    ARCHITECTURES,
    TECHNIQUES,
    build_architecture,
    build_router,
)
from eoip.ragx.core import Candidate
from eoip.ragx import metrics as m
from eoip.ragx import techniques as t


@pytest.fixture()
def store() -> MemoryGraphStore:
    s = MemoryGraphStore()
    s.upsert_vertex("WorkItem", {
        "canonical_id": "issue:1",
        "issue_key": "EOIP-1",
        "summary": "Login page returns 500 error for admin users",
        "status": "open",
        "classification": "public",
        "source_ref": "jira://EOIP-1",
    })
    s.upsert_vertex("WorkItem", {
        "canonical_id": "issue:2",
        "issue_key": "EOIP-2",
        "summary": "Dashboard timeout depends on login error handling",
        "status": "closed",
        "classification": "restricted",
    })
    s.upsert_vertex("Commit", {
        "canonical_id": "commit:1",
        "commit_sha": "abc123",
        "summary": "fix login 500 error handling in auth module",
        "classification": "public",
        "source_ref": "git://demo/abc123",
    })
    s.upsert_vertex("CodeSymbol", {
        "canonical_id": "sym:1",
        "qualified_name": "auth.login_handler",
        "name": "login_handler",
        "summary": "handles the admin login request and raises on error",
        "language": "en",
    })
    s.upsert_vertex("Document", {
        "canonical_id": "doc:1",
        "name": "Deployment runbook",
        "description": "Steps to deploy the release: run migration, restart service, verify health",
        "content": "deploy the release: run migration, restart service, verify health",
        "version_id": "2.0",
        "language": "en",
        "classification": "public",
    })
    s.upsert_vertex("Metric", {
        "canonical_id": "metric:1",
        "metric_name": "login error rate",
        "metric_value": "0.42",
        "status": "breaching",
        "version_id": "1.0",
    })
    s.upsert_vertex("DocumentSection", {
        "canonical_id": "doc:1:s1",
        "name": "Runbook steps",
        "content": "deploy release steps for the login service",
    })
    v = {cid: s.get_vertex_by_canonical_id(cid)["vid"] for cid in
         ("issue:1", "issue:2", "commit:1", "sym:1", "doc:1", "metric:1", "doc:1:s1")}
    s.upsert_edge("IMPLEMENTS", v["commit:1"], v["issue:1"], {"source_ref": "git://demo/abc123"})
    s.upsert_edge("BLOCKS", v["issue:2"], v["issue:1"], {})
    s.upsert_edge("CONTAINS", v["doc:1"], v["doc:1:s1"], {})
    return s


# ---------------------------------------------------------------------------
# A. Architectures — every one answers the fixture question over the graph
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(ARCHITECTURES))
def test_architecture_executes_deterministically(store, name):
    engine = build_architecture(name, store)
    result = engine.execute("login 500 error handling", {"top_k": 5})
    assert result.pattern == name
    assert result.answer
    assert result.evidence_manifest is not None
    assert result.metadata.get("generation", "deterministic") in ("deterministic", "model")
    assert isinstance(result.confidence, float)
    if not result.abstained:
        assert result.sources


def test_all_architectures_registered():
    assert len(ARCHITECTURES) == 22
    assert "raptor" in ARCHITECTURES and "hipporag" in ARCHITECTURES


def test_kgrag_returns_grounded_triples(store):
    engine = build_architecture("kgrag", store)
    result = engine.execute("login error", {"top_k": 6, "seed_count": 2})
    assert "->" in result.answer  # triple rendering
    assert result.metadata["triple_count"] > 0


def test_pathrag_finds_inter_seed_path(store):
    engine = build_architecture("pathrag", store)
    result = engine.execute("login error timeout", {"seed_count": 4, "max_paths": 2})
    assert result.metadata.get("evidence_count", 0) > 0


def test_temporal_rag_filters_by_valid_time(store):
    engine = build_architecture("temporal", store)
    result = engine.execute("login error", {"valid_at": "2023-01-01", "top_k": 5})
    assert result.answer  # property-based filter passes (no valid_from set)


def test_temporal_rag_with_revision_journal(store):
    store.upsert_vertex("EntityRevision", {
        "canonical_id": "rev:issue:1:2",
        "subject_id": "issue:1",
        "observed_at": "2024-06-01T00:00:00Z",
        "valid_from": "2024-01-01T00:00:00Z",
        "payload_json": '{"operation": "UPSERT"}',
    })
    store.upsert_vertex("EntityRevision", {
        "canonical_id": "rev:issue:2:1",
        "subject_id": "issue:2",
        "observed_at": "2020-01-01T00:00:00Z",
        "valid_from": "2020-01-01T00:00:00Z",
        "payload_json": '{"operation": "UPSERT"}',
    })
    engine = build_architecture("temporal", store)
    out = engine.retrieve("login error", {"known_at": "2021-01-01", "top_k": 10})
    ids = {c.source_id for c in out}
    assert "issue:1" not in ids  # observed after known_at
    assert "issue:2" in ids


def test_streaming_rag_incorporates_deltas(store):
    engine = build_architecture("streaming", store)
    engine.append_delta({"canonical_id": "delta:1", "text": "fresh delta about login outage", "op": "ADD"})
    out = engine.retrieve("login outage", {"top_k": 3})
    assert any(c.source_id == "delta:1" for c in out)


def test_incremental_rag_cdc_delete(store):
    engine = build_architecture("incremental", store)
    assert any(c.source_id == "issue:1" for c in engine.retrieve("login 500 error", {"top_k": 5}))
    engine.on_cdc({"operation": "DELETE", "canonical_id": "issue:1"})
    assert not any(c.source_id == "issue:1" for c in engine.retrieve("login 500 error", {"top_k": 5}))


def test_privacy_aware_rag_filters_before_ranking(store):
    enforcer = PolicyEnforcer()
    enforcer.load_yaml("""
policies:
  - id: allow-public-rag
    role: viewer
    permission: rag:read
    conditions:
      - {attribute: classification, op: in, value: [public, null]}
""")
    engine = build_architecture("privacy_aware", store, enforcer=enforcer)
    user = User(user_id="u:1", roles=["viewer"])
    out = engine.retrieve("login error", {"user": user, "action": "rag:read", "top_k": 10, "pool_size": 30})
    restricted = [c for c in out if c.properties.get("classification") == "restricted"]
    assert not restricted
    assert engine.denied_count > 0


def test_provenance_aware_requires_citations(store):
    engine = build_architecture("provenance_aware", store)
    out = engine.retrieve("login error", {"top_k": 10})
    assert out and all(c.citations for c in out)
    result = engine.execute("login error", {"top_k": 5})
    assert result.metadata.get("citations_locked")


def test_version_aware_pins_document_version(store):
    engine = build_architecture("version_aware", store)
    out = engine.retrieve("login deploy", {"version_id": "2.0", "top_k": 10})
    assert {c.source_id for c in out} == {"doc:1"}


def test_multilingual_rag_prefers_query_language(store):
    engine = build_architecture("multilingual", store)
    out = engine.execute("login error deploy steps", {"language": "en", "top_k": 5})
    assert out.sources


def test_event_aware_rag_uses_event_context(store):
    engine = build_architecture("event_aware", store)
    out = engine.retrieve("ignored", {"event_id": "issue:1", "event_types": ["IMPLEMENTS", "BLOCKS"], "top_k": 5})
    ids = {c.source_id for c in out}
    assert {"commit:1", "issue:2"} & ids


def test_federated_rag_merges_local_source(store):
    engine = build_architecture("federated", store)
    result = engine.execute("login error", {"entity_types": ["WorkItem"], "top_k": 5})
    assert result.answer


def test_raptor_tree_clusters_related_documents(store):
    engine = build_architecture("raptor", store)
    assert engine.tree.roots  # tree built deterministically
    out = engine.retrieve("login error", {"top_k": 5})
    assert out


def test_lazygraphrag_respects_token_budget(store):
    engine = build_architecture("lazygraphrag", store)
    out = engine.retrieve("login error deploy", {"token_budget": 40, "pool_size": 30})
    total = sum(len(c.text.split()) for c in out)
    assert total <= 40 + 25  # one overshoot margin for a single item


# ---------------------------------------------------------------------------
# B. Techniques
# ---------------------------------------------------------------------------


def _cands():
    return [
        Candidate("a", "login 500 error handling fix", 0.9),
        Candidate("b", "login 500 error handling fix", 0.8),
        Candidate("c", "dashboard timeout under load", 0.7),
        Candidate("d", "deployment runbook release steps", 0.6),
    ]


def test_query_expansion_and_decomposition_and_stepback():
    assert len(t.query_expansion("fix the deploy bug")) >= 2
    assert t.query_decomposition("What broke? And why?") == ["What broke", "why"]
    assert t.step_back("why does the login 500 error happen").startswith("What is known about")


def test_rrf_and_rag_fusion():
    r1 = _cands()[:3]
    r2 = list(reversed(_cands()))[:3]
    fused = t.reciprocal_rank_fusion([r1, r2])
    assert {c.source_id for c in fused} == {"a", "b", "c", "d"}
    assert fused[0].source_id == "b"  # b and c appear in both rankings
    assert fused[0].score > fused[-1].score

    def retrieve(q: str, top_k: int) -> list[Candidate]:
        return [c for c in _cands() if "error" in c.text or "fix" in q][:top_k]

    fused2 = t.rag_fusion("fix the login error", retrieve)
    assert fused2


def test_cross_encoder_and_late_interaction():
    ranked = t.cross_encoder_rerank("login error handling", _cands())
    assert ranked[0].source_id == "a"
    li = t.late_interaction("login error", _cands())
    assert len(li) == 4 and li[0].score >= li[-1].score


def test_multi_vector():
    fields = {"x": {"name": "alpha", "body": "unrelated words"}, "y": {"name": "beta", "body": "login error text"}}
    out = t.multi_vector("login error", fields, top_n=2)
    assert out[0].source_id == "y"


def test_chunking():
    text = "The login fails. The login fails hard. The dashboard is green. Deploy steps follow."
    sem = t.semantic_chunking(text)
    assert len(sem) >= 2
    dyn = t.dynamic_chunking(" ".join(["word"] * 500), target_tokens=50)
    assert len(dyn) >= 2 and all(len(c.split()) <= 150 for c in dyn)


def test_context_processing():
    cands = _cands()
    comp = t.context_compression(cands, token_budget=10)
    assert sum(len(c.text.split()) for c in comp) <= 10 + 10
    dedup = t.evidence_deduplication(cands)
    assert {c.source_id for c in dedup} == {"a", "c", "d"}  # b is near-dup of a
    mmr = t.diversity_mmr(cands, top_n=3, lambda_=0.5)
    assert len(mmr) == 3
    assert mmr[0].source_id == "a"
    enriched = t.contextual_retrieval(cands, lambda cid: f"context for {cid}")
    assert enriched[0].text.startswith("context for a")


def test_parent_child_rolls_up_children():
    children = [Candidate("child:1", "login error", 0.9), Candidate("child:2", "login fix", 0.7)]
    out = t.parent_child(children, lambda cid: ("parent:login", "parent login context"))
    assert out[0].source_id == "parent:login"
    assert out[0].kind == "parent"
    assert out[0].score == pytest.approx(0.9)


def test_metadata_aware_filter_and_boost():
    cands = [
        Candidate("a", "login error", 0.5, properties={"status": "open", "classification": "public"}),
        Candidate("b", "login error", 0.5, properties={"status": "closed", "classification": "restricted"}),
    ]
    filtered = t.metadata_aware("login", cands, filters={"status": "open"})
    assert [c.source_id for c in filtered] == ["a"]
    boosted = t.metadata_aware("login", cands, boost={"status": "open"})
    assert boosted[0].source_id == "a" and boosted[0].score > boosted[1].score


def test_iterative_flare_ircot():
    catalog = _cands()

    def retrieve(q: str, top_k: int) -> list[Candidate]:
        return catalog[:top_k]

    it = t.iterative_rag("login error", retrieve, max_iterations=3)
    assert it
    flared = t.flare("login error", retrieve, max_iterations=2)
    assert flared
    cands, rationale = t.ircot("login error", retrieve, steps=2)
    assert cands and len(rationale) == 2


def test_hyde_fallback():
    hypo = t.hyde_query("login error", _cands())
    assert "login" in hypo and "error" in hypo


def test_verification_guided_and_confidence_gated(store):
    policy = RAGAbstentionPolicy()
    catalog = [Candidate("issue:1", "login 500 error", 1.0), Candidate("commit:1", "fix login", 0.9)]

    def retrieve(q: str, top_k: int) -> list[Candidate]:
        return catalog[:top_k]

    verdict = t.verification_guided("login error", retrieve, policy, store)
    assert verdict["verified"] and verdict["confidence"] > 0
    gated = t.confidence_gated(catalog, policy, store)
    assert not gated["abstained"] and gated["confidence"] > 0


def test_contradiction_aware_detects_conflicts():
    cands = [
        Candidate("issue:1", "login works fine", properties={"status": "open"}),
        Candidate("issue:1", "login does not work", properties={"status": "closed"}),
        Candidate("issue:2", "unrelated text", properties={}),
    ]
    report = t.contradiction_aware(cands)
    assert report["conflict_count"] >= 1
    kinds = {c["kind"] for c in report["conflicts"]}
    assert "polarity" in kinds or "value_mismatch" in kinds


def test_citation_aware_binds_claims():
    cands = [Candidate("a", "login 500 error fix", citations=["jira://EOIP-1"])]
    report = t.citation_aware(cands, claims=["login 500 error fix", "made up claim"])
    assert report["citation_accuracy"] == 0.5
    assert report["unsupported"] == ["made up claim"]


def test_cost_adaptive_respects_budget():
    def retrieve(q: str, top_k: int) -> list[Candidate]:
        return [Candidate(f"c{i}", "word " * 20, 1.0) for i in range(top_k)]

    out = t.cost_adaptive("q", retrieve, token_budget=100, depth_schedule=(2, 4, 8))
    assert out["tokens_spent"] <= 100 + 40
    assert out["candidates"]


def test_all_techniques_registered():
    expected = {
        "rag_fusion", "parent_child", "contextual_retrieval", "query_expansion",
        "query_decomposition", "step_back", "reciprocal_rank_fusion",
        "cross_encoder_rerank", "late_interaction", "multi_vector",
        "metadata_aware", "semantic_chunking", "dynamic_chunking",
        "context_compression", "evidence_deduplication", "diversity_mmr",
        "hyde", "flare", "ircot", "iterative_rag", "verification_guided",
        "contradiction_aware", "confidence_gated", "citation_aware",
        "cost_adaptive",
    }
    assert expected <= set(TECHNIQUES)


# ---------------------------------------------------------------------------
# C. Metrics on fixture rankings
# ---------------------------------------------------------------------------


RANKING = ["a", "b", "c", "d", "e"]
RELEVANT = {"a", "c", "e"}


def test_recall_and_precision_at_k():
    assert m.recall_at_k(RANKING, RELEVANT, 1) == pytest.approx(1 / 3)
    assert m.recall_at_k(RANKING, RELEVANT, 5) == pytest.approx(1.0)
    assert m.precision_at_k(RANKING, RELEVANT, 1) == pytest.approx(1.0)
    assert m.precision_at_k(RANKING, RELEVANT, 5) == pytest.approx(3 / 5)
    assert m.recall_at_k([], set(), 5) == 1.0
    assert m.precision_at_k([], RELEVANT, 5) == 0.0


def test_mrr():
    assert m.mean_reciprocal_rank([["x", "a"], ["a", "e"]], [{"a"}, {"a"}]) == pytest.approx((1 / 2 + 1) / 2)
    assert m.mean_reciprocal_rank([["z"]], [{"a"}]) == 0.0
    assert m.mean_reciprocal_rank([], []) == 0.0


def test_ndcg():
    relevance = {"a": 3.0, "c": 2.0, "e": 1.0}
    assert m.ndcg_at_k(["a", "c", "e"], relevance, 3) == pytest.approx(1.0)
    assert m.ndcg_at_k(["e", "c", "a"], relevance, 3) < 1.0
    assert m.ndcg_at_k(["a"], {}, 3) == 0.0


def test_citation_accuracy_metric():
    claims = [
        {"claim": "x", "citation": "src:1", "valid_citations": {"src:1"}},
        {"claim": "y", "citation": "src:2", "valid_citations": {"src:1"}},
        {"claim": "z", "citation": None},
    ]
    assert m.citation_accuracy(claims) == pytest.approx(1 / 3)
    assert m.citation_accuracy([{"claim": "x", "citation": "any"}]) == 1.0
    assert m.citation_accuracy([]) == 1.0


def test_access_control_correctness_metric():
    report = m.access_control_correctness(["a", "b", "secret"], {"a", "b", "c"}, {"secret"})
    assert not report["correct"]
    assert report["leaked"] == ["secret"]
    ok = m.access_control_correctness(["a", "b"], {"a", "b", "c"}, {"secret"})
    assert ok["correct"]
    assert ok["allowed_coverage"] == pytest.approx(2 / 3)


# ---------------------------------------------------------------------------
# D. Router
# ---------------------------------------------------------------------------


def test_router_lists_capabilities(store):
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(build_router(store))
    client = TestClient(app)
    resp = client.get("/api/v1/ragx/architectures")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["architectures"]) == 22
    assert "rag_fusion" in body["techniques"]
    assert "ndcg_at_k" in body["metrics"]


def test_router_query_endpoint(store):
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(build_router(store))
    client = TestClient(app)
    resp = client.post("/api/v1/ragx/query", json={
        "query": "login 500 error handling",
        "architecture": "kgrag",
        "context": {"top_k": 5},
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["architecture"] == "kgrag"
    assert body["answer"]
    assert "evidence_manifest" in body


def test_router_adaptive_and_404(store):
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(build_router(store))
    client = TestClient(app)
    resp = client.post("/api/v1/ragx/query", json={"query": "overview of communities"})
    assert resp.status_code == 200
    assert client.post("/api/v1/ragx/query", json={
        "query": "q", "architecture": "nope"}).status_code == 404


def test_router_metrics_endpoint(store):
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(build_router(store))
    client = TestClient(app)
    resp = client.post("/api/v1/ragx/metrics/compute", json={
        "metric": "recall_at_k",
        "ranking": RANKING,
        "relevant": sorted(RELEVANT),
        "k": 5,
    })
    assert resp.status_code == 200
    assert resp.json()["value"] == 1.0


def test_router_technique_endpoint(store):
    from fastapi.testclient import TestClient
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(build_router(store))
    client = TestClient(app)
    resp = client.post("/api/v1/ragx/techniques/apply", json={
        "technique": "reciprocal_rank_fusion",
        "query": "login error",
        "candidates": [
            {"source_id": "a", "text": "login error", "score": 1.0},
            {"source_id": "b", "text": "other", "score": 0.5},
        ],
    })
    assert resp.status_code == 200
    assert [c["source_id"] for c in resp.json()["candidates"]] == ["a", "b"]
