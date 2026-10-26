"""Graph-build algorithm tests: each builder produces expected structures."""

import pytest
from eoip.graphbuild.cochange import CoChangeConfig, build_cochange_edges
from eoip.graphbuild.dependencies import InclusionDependencyConfig, discover_inclusion_dependencies
from eoip.graphbuild.enrichment import EnrichmentLoop
from eoip.graphbuild.hierarchy import HierarchyConfig, induce_hierarchy
from eoip.graphbuild.linking import Gazetteer, extract_mentions, extract_mentions_batch
from eoip.graphbuild.linkprediction import LinkPredictionConfig, score_pairs
from eoip.graphbuild.modes import plan_construction
from eoip.graphbuild.repair import repair_report
from eoip.graphbuild.rollup import build_hierarchical_rollup
from eoip.graphbuild.schema import induce_schema
from eoip.graphbuild.similarity import SimilarityConfig, build_similarity_graph
from eoip.ingest.profile import profile_records


# ------------------------------------------------------------------ schema
class TestSchemaInduction:
    def test_induces_root_and_nested_classes(self):
        records = [
            {"id": 1, "title": "A", "owner": {"name": "n1", "email": "n1@x.io"}},
            {"id": 2, "title": "B", "owner": {"name": "n2", "email": "n2@x.io"}},
        ]
        report = profile_records(records, dataset="tickets")
        schema = induce_schema(report)
        names = {c.name for c in schema.classes}
        assert "Tickets" in names
        assert "Owner" in names
        props = {(p.domain, p.name) for p in schema.properties}
        assert ("Tickets", "id") in props
        assert ("Owner", "email") in props
        id_prop = next(p for p in schema.properties if p.name == "id" and p.domain == "Tickets")
        assert id_prop.functional and id_prop.required
        email_prop = next(p for p in schema.properties if p.name == "email")
        assert "email" in email_prop.evidence["formats"]

    def test_deterministic(self):
        records = [{"a": i, "b": str(i)} for i in range(20)]
        s1 = induce_schema(profile_records(records, dataset="d"))
        s2 = induce_schema(profile_records(records, dataset="d"))
        assert s1.model_dump() == s2.model_dump()


# ------------------------------------------------------------------ modes
class TestConstructionModes:
    def test_modes_order_steps_and_reconcile(self):
        records = [{"id": i, "owner": {"name": f"n{i}"}} for i in range(5)]
        induced = induce_schema(profile_records(records, dataset="tickets"))
        for mode in ("ontology-first", "data-first", "hybrid"):
            plan = plan_construction(mode, "tickets", induced, ontology_classes=["Tickets"])
            assert plan.steps[0] in {"validate-ontology-manifest", "profile-dataset"}
            assert "validated-write" == plan.steps[-1]
        hybrid = plan_construction("hybrid", "tickets", induced, ontology_classes=["Tickets"])
        assert hybrid.reconciliation["Tickets"] == "match:existing"
        assert hybrid.reconciliation["Owner"] == "review:conflict"


# ------------------------------------------------------------------ cochange
class TestCoChange:
    def test_scores_pairwise_coupling(self):
        commits = [
            {"commit_id": "c1", "files": ["a.py", "b.py", "c.py"]},
            {"commit_id": "c2", "files": ["a.py", "b.py"]},
            {"commit_id": "c3", "files": ["a.py", "b.py"]},
            {"commit_id": "c4", "files": ["d.py"]},  # skipped: < min files
        ]
        delta = build_cochange_edges(commits, CoChangeConfig(min_support=2, min_confidence=0.5))
        edges = {(e.from_id, e.to_id): e for e in delta.edges}
        assert ("a.py", "b.py") in edges
        edge = edges[("a.py", "b.py")]
        assert edge.score == pytest.approx(1.0)
        assert edge.evidence["support"] == 3
        assert all(e.method == "co-change:pairwise" for e in delta.edges)

    def test_hook_can_filter(self):
        commits = [{"commit_id": "c1", "files": ["a", "b"]}, {"commit_id": "c2", "files": ["a", "b"]}]
        delta = build_cochange_edges(commits, hook=lambda e: None if e.from_id == "a" else e)
        assert all(e.from_id != "a" for e in delta.edges)


# ------------------------------------------------------------------ IND
class TestInclusionDependencies:
    def test_finds_containment(self):
        # Containment 0.9 with num_bands=32 (band width 2) makes a signature
        # band collision certain, so the exact verification step is exercised.
        columns = {
            "orders.customer_id": list(range(45)),
            "customers.id": list(range(50)),
            "unrelated.code": ["x", "y"],
        }
        delta = discover_inclusion_dependencies(
            columns, InclusionDependencyConfig(num_bands=32, min_containment=0.5)
        )
        edges = {(e.from_id, e.to_id) for e in delta.edges}
        assert ("orders.customer_id", "customers.id") in edges

    def test_exact_verify_removes_band_collisions(self):
        # Overlapping but non-contained values must not produce an edge.
        columns = {"a.v": list(range(100)) + ["zzz"], "b.v": list(range(100)) + ["yyy"]}
        delta = discover_inclusion_dependencies(columns)
        assert delta.edges == []


# ------------------------------------------------------------------ mentions
class TestMentions:
    def test_longest_match_and_boundaries(self):
        gazetteer = Gazetteer.from_entities(
            {"urn:ent:neo4j": ["Neo4j", "Neo4j AuraDB"], "urn:ent:graph": ["graph"]}
        )
        result = extract_mentions("doc:1", "We use Neo4j AuraDB and a graph store.", gazetteer)
        surfaces = [(m.evidence["surface"], m.to_id) for m in result.matches]
        assert ("Neo4j AuraDB", "urn:ent:neo4j") in surfaces
        # "graph store" -> "graph" matches on boundary; no partial-token matches
        assert any(s == "graph" for s, _ in surfaces)
        assert not any("Neo4j AuraDBs" in s for s, _ in surfaces)

    def test_no_substring_match_inside_words(self):
        gazetteer = Gazetteer.from_entities({"urn:ent:go": ["Go"]})
        assert extract_mentions("d", "Golang is not Go.", gazetteer).matches[0].evidence["start"] == 14

    def test_batch_delta(self):
        gazetteer = Gazetteer.from_entities({"urn:e:1": ["Acme"]})
        delta = extract_mentions_batch({"d1": "Acme", "d2": "nothing"}, gazetteer)
        assert len(delta.edges) == 1
        assert delta.edges[0].label == "MENTIONS"


# ------------------------------------------------------------------ hierarchy
class TestHierarchy:
    @staticmethod
    def _records() -> list[dict]:
        return [
            {"id": "n1", "parent_id": "n0", "name": "Alpha", "path": "root/n0/n1"},
            {"id": "n2", "parent_id": "n0", "name": "Beta", "path": "root/n0/n2"},
            {"id": "n0", "parent_id": "", "name": "Rootish", "path": "root/n0"},
        ]

    def test_parent_pointer(self):
        delta = induce_hierarchy(self._records(), HierarchyConfig(method="parent_pointer"))
        edges = {(e.from_id, e.to_id) for e in delta.edges}
        assert edges == {("n1", "n0"), ("n2", "n0")}

    def test_path_string(self):
        delta = induce_hierarchy(self._records(), HierarchyConfig(method="path_string", path_field="path", delimiter="/"))
        edges = {(e.from_id, e.to_id) for e in delta.edges}
        assert edges == {("n1", "n0"), ("n2", "n0")}

    def test_lexical_clustering(self):
        records = [{"id": "a", "name": "Auth Login"}, {"id": "b", "name": "Auth Logout"}, {"id": "c", "name": "Billing"}]
        delta = induce_hierarchy(records, HierarchyConfig(method="lexical_clustering"))
        parents = {(e.from_id, e.to_id) for e in delta.edges}
        assert ("a", "synthetic:Auth") in parents
        assert ("b", "synthetic:Auth") in parents
        assert not any(e.from_id == "c" for e in delta.edges)


# ------------------------------------------------------------------ rollup
class TestRollup:
    def test_multi_level_rollup(self):
        # Two triangles joined by one bridge: with the flat Leiden partition as
        # level 0 there are two communities; quotient coarsening merges them.
        adj = {
            "a": {"b", "c"}, "b": {"a", "c"}, "c": {"a", "b"},
            "x": {"y", "z", "b"}, "y": {"x", "z"}, "z": {"x", "y"},
        }
        base_partition = {"a": "C1", "b": "C1", "c": "C1", "x": "C2", "y": "C2", "z": "C2"}
        rollup = build_hierarchical_rollup(adj, base_partition=base_partition, max_levels=4)
        assert len(rollup.levels[0].communities) == 2
        assert set(rollup.entity_to_leaf) == set(adj)
        assert set(rollup.entity_to_leaf.values()) == {
            c["community_id"] for c in rollup.levels[0].communities
        }
        level1 = rollup.levels[1]
        assert len(level1.communities) == 1
        assert set(level1.communities[0]["members"]) == {
            c["community_id"] for c in rollup.levels[0].communities
        }

    def test_base_partition_defaults_to_components(self):
        rollup = build_hierarchical_rollup({"solo": set()})
        assert rollup.entity_to_leaf["solo"].startswith("urn:eoip:graphbuild:community:")


# ------------------------------------------------------------------ similarity
class TestSimilarity:
    def test_knn_cosine(self):
        embeddings = {
            "a": [1.0, 0.0],
            "b": [0.99, 0.01],
            "c": [0.0, 1.0],
            "d": [1.0, 0.0],
        }
        delta = build_similarity_graph(embeddings, SimilarityConfig(k=1, min_similarity=0.9))
        edges = {(e.from_id, e.to_id) for e in delta.edges}
        assert ("a", "b") in edges or ("b", "a") in edges
        assert all(e.label == "SIMILAR_TO" for e in delta.edges)

    def test_mutual_only(self):
        embeddings = {"a": [1, 0], "b": [1, 0.01], "c": [0, 1]}
        delta = build_similarity_graph(embeddings, SimilarityConfig(k=2, min_similarity=0.5, include_mutual_only=True))
        # a<->b is mutual nearest; c is not mutual with a or b.
        assert {(e.from_id, e.to_id) for e in delta.edges} == {("a", "b")}


# ------------------------------------------------------------------ link prediction
class TestLinkPrediction:
    @staticmethod
    def _adj() -> dict[str, set[str]]:
        return {
            "a": {"b", "c"},
            "b": {"a", "c", "d"},
            "c": {"a", "b"},
            "d": {"b", "e"},
            "e": {"d"},
        }

    def test_common_neighbors(self):
        delta = score_pairs(self._adj(), LinkPredictionConfig(method="common_neighbors"))
        best = delta.edges[0]
        # a-c is already an edge; top candidate should be a-d or c-d (1 common neighbor: b)
        assert best.score == 1.0
        assert best.label == "PREDICTED_LINK"
        assert {best.from_id, best.to_id} in [{"a", "d"}, {"c", "d"}]

    def test_adamic_adar_orders_by_rarity(self):
        delta = score_pairs(self._adj(), LinkPredictionConfig(method="adamic_adar"))
        assert delta.edges[0].score > 0
        assert all(e.evidence["common_neighbors"] for e in delta.edges)

    def test_preferential_attachment(self):
        delta = score_pairs(self._adj(), LinkPredictionConfig(method="preferential_attachment"))
        top = delta.edges[0]
        degrees = {"a": 2, "b": 3, "c": 2, "d": 2, "e": 1}
        expected = max(
            degrees[a] * degrees[b]
            for a, b in [(e.from_id, e.to_id) for e in delta.edges]
        )
        assert top.score == expected


# ------------------------------------------------------------------ repair
class TestRepair:
    def test_detects_and_clusters_dangling(self):
        vertices = {"v1", "v2"}
        edges = [
            {"edge_id": "e1", "label": "R", "out_cid": "v1", "in_cid": "v2"},
            {"edge_id": "e2", "label": "R", "out_cid": "v1", "in_cid": "v9"},
            {"edge_id": "e3", "label": "R", "out_cid": "v9", "in_cid": "v8"},
            {"edge_id": "e4", "label": "R", "out_cid": "v7", "in_cid": "v2"},
        ]
        report = repair_report(vertices, edges)
        assert report.dangling_count == 3
        # e2+e3 form one orphan component {v1-side? no: endpoints v1,v9,v8}
        assert ["v1", "v8", "v9"] in report.orphan_clusters
        assert ["v2", "v7"] in report.orphan_clusters


# ------------------------------------------------------------------ enrichment
class TestEnrichment:
    def test_validated_only_application(self):
        loop = EnrichmentLoop(min_score=0.5)
        loop.add_vertex("a")
        loop.add_vertex("b")
        loop.add_vertex("c")
        commits = [
            {"commit_id": "c1", "files": ["a", "b"]},
            {"commit_id": "c2", "files": ["a", "b"]},
            {"commit_id": "c3", "files": ["a", "c"]},
        ]
        delta = build_cochange_edges(commits, CoChangeConfig(min_support=2, min_confidence=0.5))
        stats = loop.submit(delta)
        assert stats["applied"] >= 1
        snapshot = loop.snapshot()
        assert snapshot["review_queue"] == len(delta.edges)
        # duplicate submission is rejected
        stats2 = loop.submit(delta)
        assert stats2["applied"] == 0

    def test_custom_validator(self):
        loop = EnrichmentLoop(validator=lambda e: False)
        delta = build_cochange_edges(
            [{"commit_id": "c1", "files": ["a", "b"]}, {"commit_id": "c2", "files": ["a", "b"]}]
        )
        stats = loop.submit(delta)
        assert stats == {"applied": 0, "rejected": len(delta.edges)}
        reasons = {item.reason for item in loop.review_queue()}
        assert reasons == {"validator-rejected"}


# ------------------------------------------------------------------ router smoke
class TestRouter:
    def test_routes_exist(self):
        from eoip.graphbuild.router import build_adapters_router, build_graphbuild_router

        gb = build_graphbuild_router()
        paths = {r.path for r in gb.routes}
        assert "/api/v1/graphbuild/cochange" in paths
        assert "/api/v1/graphbuild/repair" in paths
        ad = build_adapters_router()
        ad_paths = {r.path for r in ad.routes}
        assert "/api/v1/adapters" in ad_paths
        assert "/api/v1/adapters/{backend}" in ad_paths
