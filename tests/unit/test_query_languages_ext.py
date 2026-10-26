"""Golden tests for the eoip.qlang query-language extensions (gap §5)."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eoip.contracts.query_plan import QueryPlan
from eoip.graph.memory import MemoryGraphStore
import eoip.qlang.registry as qlang_registry
from eoip.qlang import (
    ExternalGateError,
    QLangNotMappableError,
    datalog,
    graphql,
    gremlin,
    jqlite,
    jsonpath,
    kql,
    lucene,
    opencypher,
    promql,

    sparql,
    sql,
    xpath,
)
from eoip.qlang.plans import QLangPlan
from eoip.qlang.router import build_router
from eoip.qlang.taxonomy import (
    Classification,
    KNOWLEDGE_REPRESENTATION_STANDARDS,
    QUERY_LANGUAGE_IDS,
    assert_taxonomy_honesty,
    classification_of,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

PAYLOAD = {
    "store": {
        "book": [
            {"title": "A", "price": 5, "meta": {"isbn": "111"}},
            {"title": "B", "price": 12, "meta": {"isbn": "222"}},
            {"title": "C", "price": 20, "meta": {"isbn": "333"}},
        ],
        "bicycle": {"color": "red", "price": 19},
    }
}

DOCS = [
    {"title": "Graph Databases", "body": "nodes and edges", "year": 2020},
    {"title": "Search Engines", "body": "inverted index", "year": 2015},
    {"title": "Query Languages", "body": "parsing and planning", "year": 2023},
]

TABLES = {
    "incidents": [
        {"id": 1, "service": "api", "severity": "high"},
        {"id": 2, "service": "api", "severity": "low"},
        {"id": 3, "service": "web", "severity": "high"},
    ],
    "deployments": [
        {"id": 10, "env": "prod", "status": "ok"},
        {"id": 11, "env": "staging", "status": "failed"},
    ],
}

SERIES = [
    {
        "metric": "http_requests_total",
        "labels": {"service": "api", "code": "200"},
        "samples": [[100, 10.0], [160, 40.0], [220, 100.0]],
    },
    {
        "metric": "http_requests_total",
        "labels": {"service": "api", "code": "500"},
        "samples": [[100, 0.0], [160, 2.0], [220, 4.0]],
    },
    {
        "metric": "http_requests_total",
        "labels": {"service": "web", "code": "200"},
        "samples": [[100, 5.0], [160, 5.0]],
    },
]


@pytest.fixture()
def store() -> MemoryGraphStore:
    s = MemoryGraphStore()
    alice = s.upsert_vertex("Service", {"canonical_id": "urn:eoip:s:alice", "name": "Alice"})
    bob = s.upsert_vertex("Service", {"canonical_id": "urn:eoip:s:bob", "name": "Bob"})
    carol = s.upsert_vertex("Service", {"canonical_id": "urn:eoip:s:carol", "name": "Carol"})
    for out_v, in_v in [(alice, bob), (bob, carol)]:
        out_cid = out_v["properties"]["canonical_id"]
        in_cid = in_v["properties"]["canonical_id"]
        s.upsert_edge("DEPENDS_ON", out_cid, in_cid, {"canonical_id": f"urn:eoip:e:{out_cid[-1]}{in_cid[-1]}"})
    return s


# ---------------------------------------------------------------------------
# Golden queries: real parsers -> plan or result
# ---------------------------------------------------------------------------

def test_jsonpath_golden():
    plan = jsonpath.parse("$.store.book[*].title")
    assert plan.language == "jsonpath"
    assert jsonpath.evaluate(plan, PAYLOAD) == ["A", "B", "C"]
    assert jsonpath.parse_and_evaluate("$.store.bicycle.color", PAYLOAD) == ["red"]
    assert jsonpath.parse_and_evaluate("$..price", PAYLOAD) == [5, 12, 20, 19]
    assert jsonpath.parse_and_evaluate("$.store.book[1].title", PAYLOAD) == ["B"]
    assert jsonpath.parse_and_evaluate("$.store.book[0:2].price", PAYLOAD) == [5, 12]
    with pytest.raises(Exception):
        jsonpath.parse("store.book")


def test_jqlite_golden():
    assert jqlite.parse_and_evaluate(".store.book[] | select(.price > 10) | .title", PAYLOAD) == ["B", "C"]
    assert jqlite.parse_and_evaluate(".store.bicycle.color", PAYLOAD) == ["red"]
    assert jqlite.parse_and_evaluate(".", PAYLOAD) == [PAYLOAD]
    with pytest.raises(Exception):
        jqlite.parse("map(.title)")


def test_xpath_golden():
    assert xpath.parse_and_evaluate("/store/book/title", PAYLOAD) == ["A", "B", "C"]
    assert xpath.parse_and_evaluate("/store/bicycle/color", PAYLOAD) == ["red"]
    assert xpath.parse_and_evaluate("//color", PAYLOAD) == ["red"]
    with pytest.raises(Exception):
        xpath.parse("store/book")


def test_lucene_golden():
    assert len(lucene.parse_and_evaluate("title:databases", DOCS)) == 1
    assert len(lucene.parse_and_evaluate('"query languages"', DOCS, default_fields=["title"])) == 1
    assert len(lucene.parse_and_evaluate("year:[2016 TO 2024]", DOCS)) == 2
    assert len(lucene.parse_and_evaluate("year:2015 OR year:2023", DOCS)) == 2
    assert len(lucene.parse_and_evaluate("NOT year:2023", DOCS)) == 2
    assert len(lucene.parse_and_evaluate("year:2020 AND body:edges", DOCS)) == 1
    assert len(lucene.parse_and_evaluate("(year:2015 OR year:2020) AND NOT body:index", DOCS)) == 1
    with pytest.raises(Exception):
        lucene.parse("(year:2015 OR year:2020")  # unbalanced group


def test_kql_golden():
    assert len(kql.parse_and_evaluate("incidents | where severity == high", TABLES)) == 2
    assert len(kql.parse_and_evaluate("incidents | where severity != high", TABLES)) == 1
    result = kql.parse_and_evaluate("incidents | summarize count() by service", TABLES)
    assert {r["service"]: r["count"] for r in result} == {"api": 2, "web": 1}
    assert len(kql.parse_and_evaluate('search "api"', TABLES)) == 2
    assert len(kql.parse_and_evaluate("deployments | take 1", TABLES)) == 1
    with pytest.raises(Exception):
        kql.parse("incidents | sort by id")


def test_promql_golden():
    plan = promql.parse('http_requests_total{service="api", code="200"}')
    result = promql.evaluate(plan, SERIES)
    assert len(result) == 1 and result[0]["value"] == 100.0

    plan = promql.parse('sum(http_requests_total{service="api"}) by (code)')
    result = promql.evaluate(plan, SERIES)
    by_code = {r["labels"]["code"]: r["value"] for r in result}
    assert by_code == {"200": 100.0, "500": 4.0}

    rate = promql.parse('rate(http_requests_total{service="api", code="200"}[2m])')
    result = promql.evaluate(rate, SERIES)
    # samples within last 120s of t=220: t=160 -> 220, delta 60v / 60s
    assert result[0]["value"] == pytest.approx(1.0)

    rng = promql.evaluate_range(promql.parse("http_requests_total"), SERIES, 100, 220, 60)
    assert [r["t"] for r in rng] == [100, 160, 220]
    with pytest.raises(Exception):
        promql.parse("histogram_quantile(0.9, x)")


def test_datalog_golden():
    program = """
    parent(alice, bob).
    parent(bob, carol).
    ancestor(X, Y) :- parent(X, Y).
    ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
    """
    facts = datalog.parse_and_evaluate(program)
    assert ("alice", "carol") in facts["ancestor"]
    assert len(facts["ancestor"]) == 3

    cap_program = "edge(a, b). edge(b, c). reach(X, Y) :- edge(X, Y). reach(X, Y) :- reach(X, Z), edge(Z, Y)."
    facts = datalog.parse_and_evaluate(cap_program, iteration_cap=10)
    assert ("a", "c") in facts["reach"]


def test_sql_golden():
    assert sql.parse_and_evaluate("SELECT title FROM docs", {"docs": DOCS})[0] == {"title": "Graph Databases"}
    assert sql.parse_and_evaluate("SELECT * FROM docs WHERE year >= 2020", {"docs": DOCS})[1]["year"] == 2023
    assert sql.parse_and_evaluate("SELECT COUNT(*) FROM docs", {"docs": DOCS}) == [{"count": 3}]
    result = sql.parse_and_evaluate("SELECT service, COUNT(*) FROM incidents GROUP BY service", {"incidents": TABLES["incidents"]})
    assert {r["service"]: r["count"] for r in result} == {"api": 2, "web": 1}
    result = sql.parse_and_evaluate("SELECT title FROM docs ORDER BY title DESC LIMIT 2", {"docs": DOCS})
    assert [r["title"] for r in result] == ["Search Engines", "Query Languages"]
    result = sql.parse_and_evaluate("SELECT title FROM docs WHERE title LIKE '%Engines%'", {"docs": DOCS})
    assert len(result) == 1
    with pytest.raises(Exception):
        sql.parse("DELETE FROM docs")


def test_graphql_golden(store):
    query = "query { Service { name __typename depends_on { name } } }"
    plan = graphql.parse(query)
    assert plan.language == "graphql"
    result = graphql.execute(plan, store)
    people = result["data"]["Service"]
    assert {p["name"] for p in people} == {"Alice", "Bob", "Carol"}
    alice = next(p for p in people if p["name"] == "Alice")
    assert alice["depends_on"][0]["name"] == "Bob"
    with pytest.raises(Exception):
        graphql.parse("query { UnknownType { name } }")


def test_gremlin_golden(store):
    plan = gremlin.parse("g.V().hasLabel('Service').has('name','Alice').out('DEPENDS_ON').path()")
    result = gremlin.execute(plan, store)
    assert result["operation"] == "path"
    names = [n["name"] for n in result["result"][0]]
    assert names == ["Alice", "Bob"]

    count = gremlin.execute(gremlin.parse("g.V().hasLabel('Service').count()"), store)
    assert count["result"] == 3
    with pytest.raises(Exception):
        gremlin.parse("g.V().map{it.get()}")


def test_opencypher_golden(store):
    query = "MATCH (a:Service)-[r:DEPENDS_ON*1..2]->(b:Service) WHERE a.name = 'Alice' RETURN a.name, b.name"
    plan = opencypher.parse(query)
    assert plan.max_hops == 2
    result = opencypher.execute(plan, store)
    pairs = {(r["a.name"], r["b.name"]) for r in result["rows"]}
    assert ("Alice", "Bob") in pairs and ("Alice", "Carol") in pairs

    fixed = opencypher.parse("MATCH (a:Service)-[r:DEPENDS_ON]->(b:Service) RETURN b.name")
    result = opencypher.execute(fixed, store)
    assert len(result["rows"]) == 2
    with pytest.raises(Exception):
        opencypher.parse("MATCH (a) RETURN a")  # no bounds
    with pytest.raises(Exception):
        opencypher.parse("MATCH (a:Service)-[r:DEPENDS_ON*1..99]->(b:Service) RETURN b")


def test_sparql_golden(store):
    query = """
    PREFIX eoip: <urn:eoip:>
    SELECT ?s ?o WHERE {
        ?s DEPENDS_ON ?o .
        FILTER(?s = "urn:eoip:s:alice")
    }
    """
    plan = sparql.parse(query)
    result = sparql.execute(plan, store)
    assert result["rows"] == [{"s": "urn:eoip:s:alice", "o": "urn:eoip:s:bob"}]
    with pytest.raises(Exception):
        sparql.parse("SELECT * WHERE {}")


# ---------------------------------------------------------------------------
# QueryPlan IR lowering
# ---------------------------------------------------------------------------

def test_plan_lowers_to_query_plan(store):
    plan = gremlin.parse("g.V('urn:eoip:s:alice').hasLabel('Service').out('DEPENDS_ON')")
    assert plan.anchors == ["urn:eoip:s:alice"]
    qp = plan.to_query_plan()
    assert isinstance(qp, QueryPlan)
    assert qp.intent == "NEIGHBORHOOD"
    assert qp.relationship_allowlist == ["DEPENDS_ON"]

    path = opencypher.parse("MATCH (a:Service)-[r:DEPENDS_ON]->(b:Service) RETURN a, b")
    qp = path.to_query_plan()
    # Anchor-less traversal lowers honestly to a label-scoped SEARCH.
    assert qp.intent == "SEARCH"

    with pytest.raises(QLangNotMappableError):
        jsonpath.parse("$.a").to_query_plan()


# ---------------------------------------------------------------------------
# Registry tier honesty
# ---------------------------------------------------------------------------

def test_registry_real_entries_parse():
    for manifest in qlang_registry.list_manifests():
        if manifest.tier.value == "real":
            entry = qlang_registry.get(manifest.id)
            assert entry.parser is not None
            assert manifest.supports_parse is True


def test_registry_declared_tier_is_honest():
    declared = [m for m in qlang_registry.list_manifests() if m.tier.value == "declared"]
    assert declared, "declared tier must be populated"
    required = {
        "gsql", "ngql", "typeql", "aql", "pgql", "sqlpgq", "dql",
        "sparql_update", "sparql_federated", "sparql_star", "geosparql",
        "gremlin_dsl", "sql_recursive_cte", "kql_kusto", "es_dsl", "flux",
        "mongo_aggregation", "surrealql", "sqlpp", "xquery", "jq_full",
        "nl2cypher", "nl2sparql", "nl2gremlin", "nl2gql", "nl2graphql",
        "nl2kql", "nl2promql", "nl2logql", "nl2datalog", "nl2sql",
    }
    assert required <= {m.id for m in declared}
    for m in declared:
        assert m.supports_parse is False, f"{m.id} must not claim parsing"
        assert m.external_gate is True, f"{m.id} must be marked external gate"
        assert m.gate_reason, f"{m.id} needs an honest gate reason"
        entry = qlang_registry.get(m.id)
        assert entry.parser is None and entry.evaluator is None
        with pytest.raises(ExternalGateError):
            qlang_registry.parse(m.id, "anything")


def test_nl2_family_routes_to_suggest():
    for m in qlang_registry.list_manifests():
        if m.family == "NL2*":
            assert m.routes_to == "eoip.suggest"


# ---------------------------------------------------------------------------
# §5.3 taxonomy classification
# ---------------------------------------------------------------------------

def test_kr_standards_not_query_languages():
    assert assert_taxonomy_honesty() == []
    assert len(KNOWLEDGE_REPRESENTATION_STANDARDS) == 18
    for rec in KNOWLEDGE_REPRESENTATION_STANDARDS.values():
        assert rec.classification == Classification.KNOWLEDGE_REPRESENTATION
        assert rec.id not in QUERY_LANGUAGE_IDS

    expected = {
        "rdf", "rdfs", "owl", "skos", "shacl", "rdf_star", "json_ld", "turtle",
        "trig", "n_triples", "n_quads", "rdf_xml", "prov_o", "dc",
        "dublin_core_terms", "owl_time", "sosa", "ssn",
    }
    assert expected == set(KNOWLEDGE_REPRESENTATION_STANDARDS)
    assert classification_of("sparql") == Classification.QUERY_LANGUAGE
    assert classification_of("owl") == Classification.KNOWLEDGE_REPRESENTATION
    assert classification_of("unknown_xyz") is None


# ---------------------------------------------------------------------------
# HTTP router
# ---------------------------------------------------------------------------

def test_router_routes(store):
    app = FastAPI()
    app.include_router(build_router(store=store))
    client = TestClient(app)

    langs = client.get("/api/v1/qlang/languages")
    assert langs.status_code == 200
    ids = {m["id"] for m in langs.json()}
    assert {"jsonpath", "sparql", "graphql", "gsql", "nl2cypher"} <= ids

    detail = client.get("/api/v1/qlang/languages/gsql")
    assert detail.status_code == 200
    assert detail.json()["supports_parse"] is False

    assert client.get("/api/v1/qlang/languages/nope").status_code == 404

    plan = client.post("/api/v1/qlang/parse", json={"language": "jsonpath", "query": "$.a.b"})
    assert plan.status_code == 200
    assert plan.json()["language"] == "jsonpath"

    bad = client.post("/api/v1/qlang/parse", json={"language": "jsonpath", "query": "nope"})
    assert bad.status_code == 400

    gate = client.post("/api/v1/qlang/parse", json={"language": "gsql", "query": "SELECT 1"})
    assert gate.status_code == 422

    result = client.post(
        "/api/v1/qlang/execute",
        json={"language": "jq", "query": ".a[] | select(.x == 1)", "payload": {"a": [{"x": 1}, {"x": 2}]}},
    )
    assert result.status_code == 200
    assert result.json()["result"] == [{"x": 1}]

    graph = client.post(
        "/api/v1/qlang/execute",
        json={"language": "graphql", "query": "query { Service { name } }"},
    )
    assert graph.status_code == 200
    assert graph.json()["count"] == 3

    gate_exec = client.post("/api/v1/qlang/execute", json={"language": "typeql", "query": "match $x isa person;"})
    assert gate_exec.status_code == 422

    taxonomy = client.get("/api/v1/qlang/taxonomy")
    assert taxonomy.status_code == 200
    body = taxonomy.json()
    assert body["violations"] == []
    assert "owl" in body["knowledge_representation"]
