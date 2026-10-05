"""API tests for the extended capability routes in apps/api/extended.py.

Covers GAP-FABRIC (federation), GAP-TRUTH (claims/resolution), GAP-KP
(knowledge products), GAP-QI (explain/cost), GAP-SEARCH (facets),
GAP-GRAPHTEST (graph test framework), GAP-TAX (SKOS taxonomy),
GAP-RET (keyword retrieval), and GAP-TEMP (bitemporal slice).
"""

from eoip.graph.memory import MemoryGraphStore
from fastapi.testclient import TestClient

from apps.api.app import create_app

PLAN_BODY = {
    "intent": "SEARCH",
    "anchors": ["EOIP-1"],
    "max_depth": 3,
    "result_limit": 50,
    "timeout_ms": 5000,
    "evidence_mode": "SUMMARY",
}


def _claim(claim_id: str, value: str, authority: float = 0.9) -> dict:
    return {
        "claim_id": f"urn:eoip:truth:claim:{claim_id}",
        "subject_id": "urn:eoip:entity:svc",
        "predicate": "owner",
        "value": value,
        "source_id": "urn:eoip:source:demo",
        "source_authority": authority,
        "extraction_confidence": 0.9,
    }


def _client(store: MemoryGraphStore | None = None) -> TestClient:
    store = store or MemoryGraphStore()
    store.upsert_vertex(
        "WorkItem",
        {
            "canonical_id": "issue:EOIP-1",
            "issue_key": "EOIP-1",
            "summary": "Trace impact demo",
        },
    )
    return TestClient(create_app(store))


def test_openapi_resolves_all_extended_request_models() -> None:
    client = _client()
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    for route, model in [
        ("/api/v1/algorithms/run", "AlgorithmRequest"),
        ("/api/v1/query/language", "QueryLanguageRequest"),
        ("/api/v1/admin/semantic-pipeline", "SemanticPipelineRequest"),
        ("/api/v1/agents/analytics", "AgentAnalyticsRequest"),
        ("/api/v1/agents/semantic-index", "AgentAnalyticsRequest"),
    ]:
        body = schema["paths"][route]["post"]["requestBody"]
        assert body["content"]["application/json"]["schema"]["$ref"].endswith(f"/{model}")
    response = client.post("/api/v1/query/language", json={
        "language": "eoql", "query": "SELECT * FROM WorkItem LIMIT 1",
    })
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_federation_sources_and_query() -> None:
    client = _client()
    sources = client.get("/api/v1/federation/sources")
    assert sources.status_code == 200
    ids = {s["source_id"] for s in sources.json()["sources"]}
    assert {"demo-memory", "hugegraph-local"} <= ids

    response = client.post(
        "/api/v1/federation/query",
        json={"entity_types": ["WorkItem"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["row_count"] >= 1
    assert body["plan"]["fragments"]
    assert any(f["status"] == "executed" for f in body["plan"]["fragments"])


def test_truth_claim_resolve_explain_and_assertion() -> None:
    client = _client()
    assert client.post("/api/v1/truth/claims", json=_claim("1", "team-a")).status_code == 201
    assert client.post("/api/v1/truth/claims", json=_claim("2", "team-b", 0.4)).status_code == 201

    contradictions = client.get("/api/v1/truth/contradictions")
    assert contradictions.status_code == 200
    assert len(contradictions.json()["contradictions"]) == 1

    resolve = client.post(
        "/api/v1/truth/resolve",
        json={
            "subject_id": "urn:eoip:entity:svc",
            "predicate": "owner",
            "policy": "highest-authority",
        },
    )
    assert resolve.status_code == 200
    assert resolve.json()["chosen_claim_id"].endswith("1")

    assertion = client.get("/api/v1/truth/assertions/urn:eoip:entity:svc/owner")
    assert assertion.status_code == 200
    assert assertion.json()["value"] == "team-a"

    explain = client.get("/api/v1/truth/explain/urn:eoip:entity:svc/owner")
    assert explain.status_code == 200
    assert "highest authority" in explain.json()["explanation"]

    missing = client.get("/api/v1/truth/assertions/urn:eoip:entity:none/owner")
    assert missing.status_code == 404

    export = client.get("/api/v1/truth/export")
    assert export.status_code == 200
    assert "claims" in export.json()


def test_truth_resolve_without_conflict_is_422() -> None:
    client = _client()
    response = client.post(
        "/api/v1/truth/resolve",
        json={"subject_id": "urn:eoip:entity:none", "predicate": "owner"},
    )
    assert response.status_code == 422


def test_knowledge_product_create_transition_lineage() -> None:
    client = _client()
    created = client.post(
        "/api/v1/catalog/products",
        json={
            "name": "Impact Graph",
            "owner": "platform-team",
            "domain": "engineering",
            "source_graphs": ["graph:demo"],
            "consumers": ["dashboard:impact"],
        },
    )
    assert created.status_code == 201
    product_id = created.json()["product_id"]
    assert created.json()["state"] == "Draft"

    listing = client.get("/api/v1/catalog/products")
    assert listing.status_code == 200
    assert any(p["product_id"] == product_id for p in listing.json()["products"])

    illegal = client.post(
        f"/api/v1/catalog/products/{product_id}/transition",
        json={"to_state": "Certified"},
    )
    assert illegal.status_code == 422

    transitioned = client.post(
        f"/api/v1/catalog/products/{product_id}/transition",
        json={"to_state": "Experimental"},
    )
    assert transitioned.status_code == 200
    assert transitioned.json()["state"] == "Experimental"

    lineage = client.get(f"/api/v1/catalog/products/{product_id}/lineage")
    assert lineage.status_code == 200
    assert lineage.json()["source_graphs"][0]["source_graph"] == "graph:demo"
    assert lineage.json()["consumers"][0]["consumer"] == "dashboard:impact"

    exported = client.get(f"/api/v1/catalog/products/{product_id}/export")
    assert exported.status_code == 200
    assert exported.json()["name"] == "Impact Graph"

    missing = client.get("/api/v1/catalog/products/urn:eoip:catalog:knowledge-product:nope")
    assert missing.status_code == 404


def test_query_explain_cost_and_templates() -> None:
    client = _client()
    explain = client.post("/api/v1/query/explain", json=PLAN_BODY)
    assert explain.status_code == 200
    assert explain.json()["steps"]
    assert explain.json()["indexes_used"]

    cost = client.post("/api/v1/query/cost", json=PLAN_BODY)
    assert cost.status_code == 200
    assert 0.0 <= cost.json()["score"] <= 1.0

    history = client.get("/api/v1/query/history")
    assert history.status_code == 200
    assert history.json()["history"] == []

    slow = client.get("/api/v1/query/slow", params={"threshold_ms": 10, "top_n": 5})
    assert slow.status_code == 200
    assert slow.json()["suggestions"]

    saved = client.post(
        "/api/v1/query/templates",
        json={"name": "by-key", "intent": "SEARCH", "anchor_params": ["key"]},
    )
    assert saved.status_code == 201
    template_id = saved.json()["template_id"]

    listed = client.get("/api/v1/query/templates")
    assert any(t["template_id"] == template_id for t in listed.json()["templates"])

    bound = client.post(
        f"/api/v1/query/templates/{template_id}/bind",
        json={"params": {"key": "EOIP-1"}},
    )
    assert bound.status_code == 200
    assert bound.json()["anchors"] == ["EOIP-1"]

    bad_bind = client.post(
        f"/api/v1/query/templates/{template_id}/bind",
        json={"params": {}},
    )
    assert bad_bind.status_code == 422

    deleted = client.delete(f"/api/v1/query/templates/{template_id}")
    assert deleted.status_code == 200


def test_faceted_search_preserves_identity() -> None:
    client = _client()
    response = client.post("/api/v1/search/faceted", json={"query": "EOIP"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["hits"][0]["canonical_id"] == "issue:EOIP-1"
    assert body["facets"]["entity_type"][0]["value"] == "WorkItem"


def test_graph_tests_run_returns_report_even_when_failing() -> None:
    client = _client()
    suite = {
        "id": "suite-1",
        "name": "Demo suite",
        "assertions": [
            {"id": "a1", "type": "no_orphan", "label": "WorkItem"},
            {"id": "a2", "type": "no_orphan", "label": "NoSuchLabel"},
        ],
    }
    response = client.post("/api/v1/graph-tests/run", json=suite)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["conformant"] is False
    assert body["passed"] == 1

    invalid = client.post("/api/v1/graph-tests/run", json={"unknown": True})
    assert invalid.status_code == 422


def test_skos_scheme_concept_mapping_validate_and_export() -> None:
    client = _client()
    scheme = client.post("/api/v1/taxonomy/schemes", json={"title": "Domains"})
    assert scheme.status_code == 201
    scheme_id = scheme.json()["scheme_id"]

    duplicate = client.post(
        "/api/v1/taxonomy/schemes",
        json={"title": "Dup", "scheme_id": scheme_id},
    )
    assert duplicate.status_code == 409

    concept = client.post(
        "/api/v1/taxonomy/concepts",
        json={"scheme_id": scheme_id, "pref_label": "Alpha"},
    )
    assert concept.status_code == 201
    concept_id = concept.json()["concept_id"]

    unknown_scheme = client.post(
        "/api/v1/taxonomy/concepts",
        json={"scheme_id": "missing", "pref_label": "X"},
    )
    assert unknown_scheme.status_code == 404

    concept_b = client.post(
        "/api/v1/taxonomy/concepts",
        json={"scheme_id": scheme_id, "pref_label": "Beta"},
    )
    mapping = client.post(
        "/api/v1/taxonomy/mappings",
        json={
            "source_id": concept_id,
            "target_id": concept_b.json()["concept_id"],
            "kind": "relatedMatch",
        },
    )
    assert mapping.status_code == 201
    assert len(client.get("/api/v1/taxonomy/mappings").json()["mappings"]) == 1

    concepts = client.get("/api/v1/taxonomy/concepts", params={"scheme": scheme_id})
    assert len(concepts.json()["concepts"]) == 2

    validate = client.get("/api/v1/taxonomy/validate")
    assert validate.status_code == 200
    assert validate.json()["label_conflicts"] == []

    exported = client.get("/api/v1/taxonomy/export.rdf")
    assert exported.status_code == 200
    assert exported.headers["content-type"].startswith("application/ld+json")
    assert exported.json()["@context"]["skos"]


def test_retrieval_keyword_search_returns_trace() -> None:
    client = _client()
    response = client.post(
        "/api/v1/retrieval/search",
        json={"question": "EOIP", "strategy": "keyword", "top_k": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["strategy"] == "keyword"
    assert body["trace"]
    assert body["evidence_refs"] == ["issue:EOIP-1"]


def test_bitemporal_slice_endpoint_is_available() -> None:
    client = _client()
    response = client.post("/api/v1/graph/bitemporal/slice", json={})
    assert response.status_code == 200
    assert response.json()["coordinate"]["valid_at"] in (None, "")
    assert response.json()["coordinate"]["known_at"] in (None, "")


def test_rag_query_response_includes_abstention_fields() -> None:
    client = _client()
    response = client.post("/api/v1/rag/query", json={"query": "what is EOIP-1?"})
    assert response.status_code == 200
    assert "abstained" in response.json()
    assert "evidence_manifest" in response.json()
