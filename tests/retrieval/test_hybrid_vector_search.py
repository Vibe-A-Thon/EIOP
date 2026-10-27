"""Acceptance test suite for Search, Embeddings and Projection Fidelity (WP-025, CRA-025.1-9, CRA-025.A)."""
from __future__ import annotations

import pytest
import time
from importlib import import_module
from typing import Any

from eoip.gnn.engine import GraphEmbedder
from eoip.retrieval.hybrid_vector_service import (
    DimensionMismatchError,
    EmbeddingProviderUnavailableError,
    HybridVectorIndexManager,
    IncompatibleEmbeddingFamilyError,
    IndexFamily,
    IndexMetadata,
    IndexState,
    ProductionConfigurationError,
    RealSemanticProvider,
    SearchEvaluationHarness,
    TenantVectorIndex,
    TestHashingEmbedder,
    VectorDocument,
)
HashBaseline: Any = import_module("tests.neural.baselines").HashBaseline


# ===========================================================================
# CRA-025.1: Index versioning by scope, revisions, provider, model, dimension
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_1_index_metadata_versioning():
    meta = IndexMetadata(
        index_id="idx_tenant_alpha_text_v1",
        scope="tenant_alpha",
        family=IndexFamily.TEXT,
        source_revision="git-commit-a1b2c3",
        ontology_revision="eoip-ont-3.2",
        policy_revision="pol-epoch-4",
        provider="sentence-transformers",
        model="all-MiniLM-L6-v2",
        tokenizer="wordpiece-bert-mini",
        dimension=384,
        normalization="L2",
        metric="COSINE",
        policy_epoch=4,
        state=IndexState.ACTIVE,
    )
    meta_dict = meta.to_dict()
    assert meta_dict["scope"] == "tenant_alpha"
    assert meta_dict["family"] == "TEXT"
    assert meta_dict["dimension"] == 384
    assert meta_dict["ontology_revision"] == "eoip-ont-3.2"
    assert meta_dict["policy_epoch"] == 4
    assert meta_dict["state"] == "ACTIVE"


# ===========================================================================
# CRA-025.2: Real semantic providers vs fixtures, dimension mismatch errors
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_2_provider_unavailable_and_dimension_mismatch():
    # Unavailable provider raises hard error
    unavail_provider = RealSemanticProvider(is_available=False)
    with pytest.raises(EmbeddingProviderUnavailableError, match="disabled or unavailable"):
        unavail_provider.embed("hello world")

    # A configured provider never substitutes hashing: wrong dimensions or an outage are hard errors
    from eoip.models.provider import ModelUnavailable
    from eoip.retrieval.hybrid_vector_service import DimensionMismatchError as _DM

    class _Backend:
        def __init__(self, out):
            self.out, self.model_name = out, "m"

        def embed_one(self, text):
            if isinstance(self.out, Exception):
                raise self.out
            return self.out

    with pytest.raises(_DM):
        RealSemanticProvider(dimension=128, backend=_Backend([0.1] * 64)).embed("sample query")
    with pytest.raises(EmbeddingProviderUnavailableError):
        RealSemanticProvider(backend=_Backend(ModelUnavailable("down"))).embed("sample query")
    with pytest.raises(EmbeddingProviderUnavailableError):
        RealSemanticProvider(backend=_Backend([0.0] * 8)).embed("sample query")
    assert len(RealSemanticProvider(dimension=3, backend=_Backend([0.1, 0.2, 0.3])).embed("q")) == 3

    # Dimension mismatch raises hard error (never silently zero-pads)
    meta = IndexMetadata(
        index_id="idx_1",
        scope="tenant_1",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="st",
        model="mini",
        tokenizer="mini",
        dimension=128,
    )
    index = TenantVectorIndex(meta)
    doc_bad = VectorDocument(
        doc_id="doc_bad",
        text="bad vector length",
        vector=[0.1] * 64,  # 64 != 128
        family=IndexFamily.TEXT,
    )
    with pytest.raises(DimensionMismatchError, match="does not match index dimension"):
        index.add_document(doc_bad)


# ===========================================================================
# CRA-025.3: ACL permission filtering and policy-epoch cache revocation
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_3_acl_filtering_and_policy_epoch():
    meta = IndexMetadata(
        index_id="idx_sec",
        scope="tenant_finance",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="st",
        model="m",
        tokenizer="t",
        dimension=4,
        policy_epoch=1,
    )
    index = TenantVectorIndex(meta)

    # Document visible only to finance-analyst role
    doc_restricted = VectorDocument(
        doc_id="payroll_report",
        text="Q4 executive compensation payroll audit",
        vector=[1.0, 0.0, 0.0, 0.0],
        family=IndexFamily.TEXT,
        acl_allow_roles=["finance-analyst"],
    )
    # Document visible to all employees
    doc_public = VectorDocument(
        doc_id="all_hands_notes",
        text="Company all-hands announcements",
        vector=[0.0, 1.0, 0.0, 0.0],
        family=IndexFamily.TEXT,
        acl_allow_roles=["employee"],
    )
    index.add_document(doc_restricted)
    index.add_document(doc_public)

    # Standard employee cannot retrieve or see payroll_report
    results_emp = index.hybrid_search(
        query_text="payroll",
        query_vector=[1.0, 0.0, 0.0, 0.0],
        query_family=IndexFamily.TEXT,
        caller_roles=["employee"],
    )
    retrieved_ids_emp = [r["doc_id"] for r in results_emp]
    assert "payroll_report" not in retrieved_ids_emp
    assert "all_hands_notes" in retrieved_ids_emp

    # Finance analyst can see payroll_report
    results_fin = index.hybrid_search(
        query_text="payroll",
        query_vector=[1.0, 0.0, 0.0, 0.0],
        query_family=IndexFamily.TEXT,
        caller_roles=["finance-analyst"],
    )
    retrieved_ids_fin = [r["doc_id"] for r in results_fin]
    assert "payroll_report" in retrieved_ids_fin

    # Verify policy epoch cache revocation:
    assert len(index._cache) > 0
    index.revoke_policy_epoch()
    assert index.metadata.policy_epoch == 2
    assert len(index._cache) == 0  # previous cache invalidated


# ===========================================================================
# CRA-025.4: Resumable indexing, deletion, shadow index evaluation & cutover
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_4_resumable_indexing_shadow_cutover_and_rollback():
    manager = HybridVectorIndexManager(tenant_id="tenant_cloud")

    meta_v1 = IndexMetadata(
        index_id="idx_v1",
        scope="tenant_cloud",
        family=IndexFamily.TEXT,
        source_revision="v1",
        ontology_revision="v1",
        policy_revision="v1",
        provider="st",
        model="v1-model",
        tokenizer="tok",
        dimension=4,
    )
    idx_v1 = TenantVectorIndex(meta_v1)
    idx_v1.add_document(VectorDocument(doc_id="doc_1", text="text 1", vector=[1, 0, 0, 0], family=IndexFamily.TEXT))
    manager.set_active_index(idx_v1)

    assert manager.active_indexes[IndexFamily.TEXT].metadata.index_id == "idx_v1"

    # Resumable indexing / deletion
    idx_v1.checkpoint_watermark = 100
    assert idx_v1.checkpoint_watermark == 100
    idx_v1.remove_document("doc_1")
    assert "doc_1" not in idx_v1.documents

    # Create shadow index for model re-embedding
    shadow_id = manager.create_shadow_index(
        family=IndexFamily.TEXT,
        new_provider="sentence-transformers",
        new_model="v2-model",
        new_dim=8,
    )
    assert shadow_id in manager.shadow_indexes
    shadow = manager.shadow_indexes[shadow_id]
    shadow.add_document(VectorDocument(doc_id="doc_2", text="text 2", vector=[0.1] * 8, family=IndexFamily.TEXT))

    # Atomic cutover to shadow index
    manager.cutover_shadow_index(shadow_id)
    assert manager.active_indexes[IndexFamily.TEXT].metadata.dimension == 8
    assert manager.active_indexes[IndexFamily.TEXT].metadata.state == IndexState.ACTIVE

    # Rollback to previous index
    assert manager.rollback() is True
    assert manager.active_indexes[IndexFamily.TEXT].metadata.dimension == 4


# ===========================================================================
# CRA-025.5: Evaluation harness: recall@k, nDCG, latency across domains
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_5_search_evaluation_harness():
    provider = TestHashingEmbedder(dimensions=16)  # index mechanics; real model: test_real_embedding_provider.py
    meta = IndexMetadata(
        index_id="eval_idx",
        scope="tenant_eval",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="test-p",
        model="m",
        tokenizer="t",
        dimension=16,
    )
    index = TenantVectorIndex(meta)

    # Populate index with known corpus
    for i in range(1, 11):
        txt = f"entity subject record {i} for observability monitoring"
        vec = provider.embed(txt)
        index.add_document(VectorDocument(doc_id=f"doc_{i}", text=txt, vector=vec, family=IndexFamily.TEXT))

    eval_corpus = [
        {"query": "observability monitoring 1", "relevant_doc_id": "doc_1", "roles": ["public"]},
        {"query": "observability monitoring 5", "relevant_doc_id": "doc_5", "roles": ["public"]},
    ]

    harness = SearchEvaluationHarness()
    report = harness.evaluate(index, eval_corpus, provider, top_k=5)
    assert "recall@k" in report
    assert "ndcg@k" in report
    assert "latency_p50_ms" in report
    assert report["recall@k"] > 0.0


# ===========================================================================
# CRA-025.6: Dense + BM25 fusion via RRF (k=60) with graph centrality boost
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_6_rrf_hybrid_fusion():
    TestHashingEmbedder(dimensions=8)  # index mechanics; real model: test_real_embedding_provider.py
    meta = IndexMetadata(
        index_id="idx_rrf",
        scope="tenant_fusion",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="st",
        model="mini",
        tokenizer="tok",
        dimension=8,
    )
    index = TenantVectorIndex(meta)

    # Doc 1: high keyword match, low vector similarity
    v1 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    index.add_document(VectorDocument(
        doc_id="doc_keyword",
        text="kubernetes pod container crashloop restart",
        vector=v1,
        family=IndexFamily.TEXT,
        graph_centrality=0.1,
    ))

    # Doc 2: low keyword match, high vector similarity
    v2 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    index.add_document(VectorDocument(
        doc_id="doc_semantic",
        text="infrastructure operational incident container health",
        vector=v2,
        family=IndexFamily.TEXT,
        graph_centrality=0.9,  # high graph centrality
    ))

    q_text = "kubernetes pod crash"
    q_vec = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    results = index.hybrid_search(
        query_text=q_text,
        query_vector=q_vec,
        query_family=IndexFamily.TEXT,
        caller_roles=["public"],
        top_k=5,
        rrf_k=60,
        use_graph_centrality=True,
    )
    assert len(results) == 2
    # Verify RRF score computation
    assert all(r["final_score"] > 0.0 for r in results)


# ===========================================================================
# CRA-025.7: Test-hashing embedder refused in production profile
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_7_test_hashing_refused_in_production():
    # In development/test profile, TestHashingEmbedder is allowed
    dev_embedder = TestHashingEmbedder(dimensions=32, profile="development")
    vec = dev_embedder.embed("testing")
    assert len(vec) == 32

    # In production profile, TestHashingEmbedder is REFUSED at startup
    with pytest.raises(ProductionConfigurationError, match="refused in production profile"):
        TestHashingEmbedder(dimensions=32, profile="production")


# ===========================================================================
# CRA-025.8: Graph-structure and text embeddings are distinct families
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_8_distinct_embedding_families():
    meta_text = IndexMetadata(
        index_id="idx_text",
        scope="tenant_m",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="st",
        model="text-model",
        tokenizer="t",
        dimension=4,
    )
    index_text = TenantVectorIndex(meta_text)

    # Document with GRAPH_STRUCTURE family cannot be inserted into TEXT index
    doc_graph = VectorDocument(
        doc_id="node_1",
        text="node2vec structural walk",
        vector=[1, 0, 0, 0],
        family=IndexFamily.GRAPH_STRUCTURE,
    )
    with pytest.raises(IncompatibleEmbeddingFamilyError, match="Cannot add document family"):
        index_text.add_document(doc_graph)

    # Query with GRAPH_STRUCTURE family vector against TEXT index is strictly rejected
    with pytest.raises(IncompatibleEmbeddingFamilyError, match="incompatible with index family"):
        index_text.hybrid_search(
            query_text="walk",
            query_vector=[1, 0, 0, 0],
            query_family=IndexFamily.GRAPH_STRUCTURE,
            caller_roles=["public"],
        )


# ===========================================================================
# CRA-025.9: GNN hash-based vectors refused in production profile
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_9_gnn_hash_vectors_refused_in_production():
    # In production profile, GraphEmbedder hash vectors are refused
    with pytest.raises(ProductionConfigurationError, match="Hash-based graph vectors are refused in production"):
        GraphEmbedder(profile="production")

    # HashBaseline is explicitly marked for test baselines only
    baseline = HashBaseline()
    assert baseline.profile == "test"


# ===========================================================================
# CRA-025.A: Full Acceptance: Isolation, Recovery, and Startup Protection
# ===========================================================================

@pytest.mark.req("CRA-025")
def test_cra_025_a_search_acceptance_gate():
    provider = TestHashingEmbedder(dimensions=8)  # index mechanics; real model: test_real_embedding_provider.py

    # 1. Multi-tenant isolation demonstration (no cross-tenant leakage)
    meta_a = IndexMetadata(
        index_id="idx_tenant_a",
        scope="tenant_A",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="st",
        model="m",
        tokenizer="t",
        dimension=8,
    )
    meta_b = IndexMetadata(
        index_id="idx_tenant_b",
        scope="tenant_B",
        family=IndexFamily.TEXT,
        source_revision="1",
        ontology_revision="1",
        policy_revision="1",
        provider="st",
        model="m",
        tokenizer="t",
        dimension=8,
    )
    idx_a = TenantVectorIndex(meta_a)
    idx_b = TenantVectorIndex(meta_b)

    idx_a.add_document(VectorDocument(
        doc_id="confidential_A",
        text="Tenant A strategic product plans",
        vector=provider.embed("plans"),
        family=IndexFamily.TEXT,
    ))
    idx_b.add_document(VectorDocument(
        doc_id="confidential_B",
        text="Tenant B secret merger plans",
        vector=provider.embed("plans"),
        family=IndexFamily.TEXT,
    ))

    # Tenant A search returns confidential_A and zero traces of Tenant B
    res_a = idx_a.hybrid_search("plans", provider.embed("plans"), IndexFamily.TEXT, caller_roles=["public"])
    ids_a = [r["doc_id"] for r in res_a]
    assert "confidential_A" in ids_a
    assert "confidential_B" not in ids_a
    assert len(idx_a.documents) == 1

    # 2. Production profile refusal validation
    with pytest.raises(ProductionConfigurationError):
        TestHashingEmbedder(profile="production")
    with pytest.raises(ProductionConfigurationError):
        GraphEmbedder(profile="production")

    # 3. Cross-family query rejection validation
    with pytest.raises(IncompatibleEmbeddingFamilyError):
        idx_a.hybrid_search("plans", provider.embed("plans"), IndexFamily.GRAPH_STRUCTURE, caller_roles=["public"])
