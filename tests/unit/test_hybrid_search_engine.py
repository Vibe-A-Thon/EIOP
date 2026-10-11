"""Tests for the unified hybrid search engine — all 7 search modalities."""

from __future__ import annotations

import unittest


class TestKeywordSearchAdapter(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import KeywordSearchAdapter
        self.kw = KeywordSearchAdapter()
        self.kw.index("e1", "kubernetes container orchestration platform", entity_type="Service")
        self.kw.index("e2", "docker container runtime engine", entity_type="Service")
        self.kw.index("e3", "financial reporting quarterly dashboard", entity_type="Report")

    def test_keyword_search_returns_matches(self):
        results = self.kw.search("container")
        self.assertGreater(len(results), 0)
        ids = [r.entity_id for r in results]
        self.assertIn("e1", ids)
        self.assertIn("e2", ids)

    def test_keyword_no_match(self):
        results = self.kw.search("zzzznotexist")
        self.assertEqual(len(results), 0)

    def test_keyword_modality_label(self):
        results = self.kw.search("kubernetes")
        self.assertEqual(results[0].modality.value, "KEYWORD")


class TestVectorSearchAdapter(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import VectorSearchAdapter
        self.vec = VectorSearchAdapter(dim=128)
        self.vec.index("e1", "machine learning neural network", entity_type="Concept")
        self.vec.index("e2", "deep learning artificial intelligence", entity_type="Concept")
        self.vec.index("e3", "database query optimization", entity_type="Concept")

    def test_vector_search(self):
        results = self.vec.search("neural network learning")
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].modality.value, "VECTOR")

    def test_vector_count(self):
        self.assertEqual(self.vec.count(), 3)


class TestContextualSearchAdapter(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import (
            ContextualSearchAdapter, SearchCandidate, SearchModality, UserContext,
        )
        self.ctx_adapter = ContextualSearchAdapter()
        self.SearchCandidate = SearchCandidate
        self.SearchModality = SearchModality
        self.UserContext = UserContext
        self.ctx_adapter.register_user(UserContext(
            user_id="alice",
            role="engineer",
            team="platform",
            recent_entities=["e1"],
            preferred_types=["Service"],
            expertise_domains=["kubernetes"],
            search_history=["deploy container", "service mesh"],
        ))

    def test_contextual_boost_recent(self):
        base = [
            self.SearchCandidate(entity_id="e1", score=0.5,
                                 modality=self.SearchModality.KEYWORD,
                                 text="kubernetes service", entity_type="Service"),
            self.SearchCandidate(entity_id="e2", score=0.6,
                                 modality=self.SearchModality.KEYWORD,
                                 text="database backup", entity_type="Database"),
        ]
        boosted = self.ctx_adapter.boost(base, "alice")
        e1_score = next(c.score for c in boosted if c.entity_id == "e1")
        self.assertGreater(e1_score, 0.5)

    def test_contextual_preferred_type_boost(self):
        base = [
            self.SearchCandidate(entity_id="e3", score=0.4,
                                 modality=self.SearchModality.KEYWORD,
                                 text="auth gateway", entity_type="Service"),
        ]
        boosted = self.ctx_adapter.boost(base, "alice")
        self.assertGreater(boosted[0].score, 0.4)

    def test_contextual_no_user_passthrough(self):
        base = [
            self.SearchCandidate(entity_id="e1", score=0.5,
                                 modality=self.SearchModality.KEYWORD,
                                 text="test", entity_type="X"),
        ]
        result = self.ctx_adapter.boost(base, "unknown_user")
        self.assertEqual(result[0].score, 0.5)


class TestMultimodalSearchAdapter(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import MultimodalSearchAdapter, MultimodalInput
        self.mm = MultimodalSearchAdapter(dim=128)
        self.MultimodalInput = MultimodalInput
        self.mm.index("e1", text="architecture diagram of microservices", entity_type="Diagram")
        self.mm.index("e2", text="team standup meeting recording", entity_type="Audio",
                      audio_text="standup meeting sprint retrospective")

    def test_text_query(self):
        query = self.MultimodalInput(text="architecture diagram of microservices")
        results = self.mm.search(query)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0].entity_id, "e1")

    def test_audio_query(self):
        query = self.MultimodalInput(audio_transcript="standup sprint meeting")
        results = self.mm.search(query)
        self.assertGreater(len(results), 0)

    def test_multimodal_label(self):
        query = self.MultimodalInput(text="diagram")
        results = self.mm.search(query)
        if results:
            self.assertEqual(results[0].modality.value, "MULTIMODAL")


class TestGraphSearchAdapter(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import GraphSearchAdapter
        self.graph = GraphSearchAdapter()
        self.graph.add_entity("svc-auth", text="Authentication Service", entity_type="Service")
        self.graph.add_entity("svc-user", text="User Service", entity_type="Service")
        self.graph.add_entity("db-users", text="Users Database", entity_type="Database")
        self.graph.add_entity("team-plat", text="Platform Team", entity_type="Team")
        self.graph.add_edge("svc-auth", "svc-user", "DEPENDS_ON")
        self.graph.add_edge("svc-user", "db-users", "USES")
        self.graph.add_edge("team-plat", "svc-auth", "OWNS")

    def test_single_hop(self):
        results = self.graph.search(["svc-auth"], max_hops=1)
        ids = [r.entity_id for r in results]
        self.assertIn("svc-user", ids)

    def test_multi_hop(self):
        results = self.graph.search(["svc-auth"], max_hops=2)
        ids = [r.entity_id for r in results]
        self.assertIn("db-users", ids)

    def test_no_self_in_results(self):
        results = self.graph.search(["svc-auth"], max_hops=2)
        ids = [r.entity_id for r in results]
        self.assertNotIn("svc-auth", ids)

    def test_graph_modality(self):
        results = self.graph.search(["svc-auth"], max_hops=1)
        self.assertEqual(results[0].modality.value, "GRAPH")


class TestStructuredSearchAdapter(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import StructuredSearchAdapter
        self.struct = StructuredSearchAdapter()
        self.struct.index("e1", {"name": "auth-svc", "type": "Service", "status": "healthy", "cpu": 45})
        self.struct.index("e2", {"name": "billing-svc", "type": "Service", "status": "degraded", "cpu": 90})
        self.struct.index("e3", {"name": "users-db", "type": "Database", "status": "healthy", "cpu": 20})

    def test_exact_match(self):
        results = self.struct.search({"type": "Service"})
        self.assertEqual(len(results), 2)

    def test_multi_field_filter(self):
        results = self.struct.search({"type": "Service", "status": "healthy"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_id, "e1")

    def test_comparison_operator(self):
        results = self.struct.search({"cpu": {"op": "gt", "value": 50}})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].entity_id, "e2")

    def test_contains_operator(self):
        results = self.struct.search({"name": {"op": "contains", "value": "svc"}})
        self.assertEqual(len(results), 2)

    def test_structured_modality(self):
        results = self.struct.search({"type": "Database"})
        self.assertEqual(results[0].modality.value, "STRUCTURED")


class TestReciprocalRankFusion(unittest.TestCase):
    def test_rrf_merges_rankings(self):
        from eoip.search.hybrid_engine import SearchCandidate, SearchModality, reciprocal_rank_fusion
        list1 = [
            SearchCandidate("e1", 0.9, SearchModality.KEYWORD),
            SearchCandidate("e2", 0.7, SearchModality.KEYWORD),
        ]
        list2 = [
            SearchCandidate("e2", 0.95, SearchModality.VECTOR),
            SearchCandidate("e1", 0.6, SearchModality.VECTOR),
        ]
        scores = reciprocal_rank_fusion([list1, list2])
        self.assertIn("e1", scores)
        self.assertIn("e2", scores)

    def test_rrf_weighted(self):
        from eoip.search.hybrid_engine import SearchCandidate, SearchModality, reciprocal_rank_fusion
        list1 = [SearchCandidate("e1", 0.9, SearchModality.KEYWORD)]
        list2 = [SearchCandidate("e2", 0.9, SearchModality.VECTOR)]
        scores = reciprocal_rank_fusion(
            [list1, list2],
            modality_weights={"KEYWORD": 1.0, "VECTOR": 2.0},
        )
        self.assertGreater(scores["e2"], scores["e1"])


class TestHybridSearchEngine(unittest.TestCase):
    def setUp(self):
        from eoip.search.hybrid_engine import HybridSearchEngine, UserContext
        self.engine = HybridSearchEngine(vector_dim=128)
        self.UserContext = UserContext

        self.engine.index_entity("svc-auth", "Authentication service handles login and JWT tokens",
                                 entity_type="Service", fields={"status": "healthy", "team": "platform"})
        self.engine.index_entity("svc-billing", "Billing service processes payments and invoices",
                                 entity_type="Service", fields={"status": "degraded", "team": "finance"})
        self.engine.index_entity("svc-search", "Search service provides full text search capabilities",
                                 entity_type="Service", fields={"status": "healthy", "team": "platform"})
        self.engine.index_entity("db-users", "PostgreSQL database storing user accounts and profiles",
                                 entity_type="Database", fields={"status": "healthy", "team": "platform"})
        self.engine.index_entity("doc-api", "API documentation for the platform services",
                                 entity_type="Document", fields={"status": "active", "team": "docs"})

        self.engine.add_edge("svc-auth", "db-users", "USES")
        self.engine.add_edge("svc-auth", "svc-billing", "CALLS")
        self.engine.add_edge("svc-search", "db-users", "QUERIES")

    def test_basic_search(self):
        results = self.engine.search("authentication login")
        self.assertGreater(len(results), 0)
        ids = [r.entity_id for r in results]
        self.assertIn("svc-auth", ids)

    def test_search_returns_unified_results(self):
        results = self.engine.search("service")
        self.assertGreater(len(results), 0)
        r = results[0]
        self.assertTrue(len(r.modalities_matched) > 0)
        self.assertGreater(r.final_score, 0)

    def test_search_with_structured_filters(self):
        from eoip.search.hybrid_engine import SearchModality
        results = self.engine.search(
            "service",
            modalities=[SearchModality.STRUCTURED],
            structured_filters={"team": "platform"},
        )
        for r in results:
            self.assertIn("STRUCTURED", r.modalities_matched)

    def test_search_with_graph_seeds(self):
        from eoip.search.hybrid_engine import SearchModality
        results = self.engine.search(
            "database",
            graph_seeds=["svc-auth"],
            modalities=[SearchModality.GRAPH],
        )
        ids = [r.entity_id for r in results]
        self.assertIn("db-users", ids)

    def test_search_with_user_context(self):
        from eoip.search.hybrid_engine import SearchModality
        self.engine.contextual.register_user(self.UserContext(
            user_id="alice",
            recent_entities=["svc-auth"],
            preferred_types=["Service"],
            expertise_domains=["authentication"],
        ))
        results = self.engine.search(
            "service",
            user_context=self.UserContext(user_id="alice"),
        )
        self.assertGreater(len(results), 0)
        ctx_results = [r for r in results if "CONTEXTUAL" in r.modalities_matched]
        self.assertGreater(len(ctx_results), 0)

    def test_plan_search(self):
        plan = self.engine.plan_search("test query")
        self.assertIn("KEYWORD", [m.value for m in plan.active_modalities])
        self.assertIn("VECTOR", [m.value for m in plan.active_modalities])
        self.assertIn("HYBRID", [m.value for m in plan.active_modalities])

    def test_plan_with_filters_adds_structured(self):
        plan = self.engine.plan_search(
            "test", structured_filters={"status": "healthy"},
        )
        modalities = [m.value for m in plan.active_modalities]
        self.assertIn("STRUCTURED", modalities)

    def test_plan_with_seeds_adds_graph(self):
        plan = self.engine.plan_search(
            "test", graph_seeds=["svc-auth"],
        )
        modalities = [m.value for m in plan.active_modalities]
        self.assertIn("GRAPH", modalities)

    def test_metrics_logged(self):
        self.engine.search("authentication")
        metrics = self.engine.get_metrics()
        self.assertEqual(len(metrics), 1)
        self.assertIn("candidates_per_modality", metrics[0])

    def test_stats(self):
        stats = self.engine.stats()
        self.assertEqual(stats["keyword_index_size"], 5)
        self.assertEqual(stats["vector_index_size"], 5)
        self.assertGreater(stats["graph_entity_count"], 0)

    def test_modality_weights_configurable(self):
        self.engine.set_modality_weights({"KEYWORD": 2.0})
        self.assertEqual(self.engine._modality_weights["KEYWORD"], 2.0)

    def test_empty_query_returns_empty(self):
        results = self.engine.search("")
        self.assertEqual(len(results), 0)

    def test_remove_entity(self):
        self.engine.index_entity("temp", "temporary entity")
        self.engine.remove_entity("temp")
        results = self.engine.search("temporary entity")
        ids = [r.entity_id for r in results]
        self.assertNotIn("temp", ids)


class TestHybridSearchOpenAPI(unittest.TestCase):
    def test_openapi_resolves(self):
        from eoip.platform_router import build_platform_router
        from fastapi import FastAPI
        app = FastAPI()
        app.include_router(build_platform_router())
        schema = app.openapi()
        paths = list(schema["paths"].keys())
        search_paths = [p for p in paths if "/search/" in p]
        self.assertGreater(len(search_paths), 0)


if __name__ == "__main__":
    unittest.main()
