"""Tests for Dual-Level GraphRAG & HippoRAG Diffusion (WP-KG3-07, GAP-05, STR-11, CAP-56, CRA-026.1)."""

import pytest
from eoip.rag.dual_level_diffusion import (
    DualLevelGraphRAGPipeline,
    DualLevelRouter,
    HippoRAGPPRDiffusion,
    QueryIntent,
)


def test_dual_level_router_classification():
    """Validates accurate classification of local vs global vs hybrid query intents."""
    # Local queries
    assert DualLevelRouter.classify("What databases does billing-service connect to?") == QueryIntent.LOCAL
    assert DualLevelRouter.classify("Who is the maintainer of ServiceA?") == QueryIntent.LOCAL

    # Global queries
    assert DualLevelRouter.classify("What are the systemic risks across all architecture components?") == QueryIntent.GLOBAL
    assert DualLevelRouter.classify("Summarize the common patterns and failure themes across the entire organization") == QueryIntent.GLOBAL

    # Hybrid queries
    assert DualLevelRouter.classify("Across all payment services, what are the common risks in BillingService-v2?") == QueryIntent.HYBRID


def test_hipporag_ppr_diffusion_convergence():
    """Validates Personalized PageRank continuous diffusion from seed nodes."""
    nodes = [
        {"canonical_id": f"node_{i}", "label": "Service", "properties": {"name": f"Service-{i}"}}
        for i in range(10)
    ]
    # Chain topology: 0 -> 1 -> 2 -> 3 ...
    edges = [
        {"out_cid": f"node_{i}", "in_cid": f"node_{i+1}", "label": "CALLS"}
        for i in range(9)
    ]

    ppr = HippoRAGPPRDiffusion(alpha=0.85, max_iter=30)
    scores = ppr.diffuse(nodes, edges, seed_cids=["node_0"], top_k=5)

    assert len(scores) == 5
    # Seed node and its immediate neighbors must be top ranked
    ranked_nodes = list(scores.keys())
    assert "node_0" in ranked_nodes[:2]
    assert "node_1" in ranked_nodes[:2]
    assert scores["node_1"] > scores["node_4"]


def test_token_reduction_exit_gate():
    """CRA-026.1 & WP-KG3-07: Validates that HippoRAG PPR diffusion achieves >= 80% token reduction."""
    # Create realistic synthetic enterprise graph of 60 nodes and 90 edges
    nodes = []
    for i in range(60):
        nodes.append({
            "canonical_id": f"urn:eoip:service:svc_{i}",
            "label": "Service",
            "properties": {
                "name": f"EnterpriseService_{i}",
                "description": f"Handles high-throughput mission-critical business transactions for department {i % 5}.",
                "version": "v2.4.1",
                "tier": "TIER_1" if i % 3 == 0 else "TIER_2",
            },
        })

    edges = []
    for i in range(59):
        edges.append({
            "out_cid": f"urn:eoip:service:svc_{i}",
            "in_cid": f"urn:eoip:service:svc_{i+1}",
            "label": "DEPENDS_ON",
        })
        if i % 3 == 0 and i + 5 < 60:
            edges.append({
                "out_cid": f"urn:eoip:service:svc_{i}",
                "in_cid": f"urn:eoip:service:svc_{i+5}",
                "label": "REPLICATES_TO",
            })

    pipeline = DualLevelGraphRAGPipeline()

    # Local query targeting svc_0
    result = pipeline.execute_rag(
        query="What components are impacted by EnterpriseService_0?",
        nodes=nodes,
        edges=edges,
        seed_cids=["urn:eoip:service:svc_0"],
        top_k=5,
    )

    assert result.query_intent == QueryIntent.LOCAL
    assert len(result.selected_nodes) == 5
    # Exit gate check: must achieve >= 80% token reduction!
    assert result.token_reduction_pct >= 80.0
    print(f"Token reduction achieved: {result.token_reduction_pct}% (Raw: {result.raw_token_count_estimate}, Diffused: {result.diffused_token_count_estimate})")


def test_global_query_community_summarization():
    """Validates global community detection and thematic summarization (resolving GAP-05)."""
    # Create two disjoint clusters of services
    cluster_a = [
        {"canonical_id": f"auth_{i}", "label": "SecurityModule", "properties": {"name": f"Auth_{i}"}}
        for i in range(5)
    ]
    edges_a = [
        {"out_cid": f"auth_{i}", "in_cid": f"auth_{i+1}", "label": "AUTHENTICATES"}
        for i in range(4)
    ]

    cluster_b = [
        {"canonical_id": f"pay_{i}", "label": "PaymentGateway", "properties": {"name": f"Payment_{i}"}}
        for i in range(5)
    ]
    edges_b = [
        {"out_cid": f"pay_{i}", "in_cid": f"pay_{i+1}", "label": "TRANSFERS"}
        for i in range(4)
    ]

    nodes = cluster_a + cluster_b
    edges = edges_a + edges_b

    pipeline = DualLevelGraphRAGPipeline()
    result = pipeline.execute_rag(
        query="What are the common systemic themes across the entire organization?",
        nodes=nodes,
        edges=edges,
    )

    assert result.query_intent == QueryIntent.GLOBAL
    assert len(result.community_summaries) == 2
    themes = {theme for comm in result.community_summaries for theme in comm.key_themes}
    assert "SecurityModule" in themes
    assert "PaymentGateway" in themes
