"""QLang front-end registry — capability manifests per query language.

Two tiers, honestly declared:

* ``REAL`` — deterministic stdlib parser + executor implemented in this
  package (``supports_parse=True``).
* ``DECLARED`` — capability manifest only (``supports_parse=False``). These
  carry an ``external_gate`` marker naming the external system/SDK that a
  real implementation would require. Declared-tier entries NEVER claim
  parsing; calling ``parse`` on one raises ``ExternalGateError``.

The NL2* family routes through the existing ``eoip.suggest`` engine where
applicable (schema-grounded generation with graceful fallback when no LLM
hook is configured).
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel, Field

from eoip.qlang import (
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
from eoip.qlang.plans import QLangParseError, QLangPlan


class RegistryTier(str, Enum):
    REAL = "real"
    DECLARED = "declared"


class ExternalGateError(QLangParseError):
    """Raised when a declared-tier (external gate) front-end is asked to parse."""


class QLangManifest(BaseModel):
    """Capability manifest for one query-language front-end."""

    id: str
    name: str
    family: str
    tier: RegistryTier
    subset: str = Field(default="", description="honest description of what is implemented")
    supports_parse: bool
    supports_execute: bool
    external_gate: bool = Field(default=False, description="requires an external system/SDK")
    gate_reason: str = Field(default="", description="why this is an external gate")
    routes_to: str = Field(default="", description="existing engine the family routes through")


ParserFn = Callable[[str], QLangPlan]


class RegisteredFrontEnd(BaseModel):
    manifest: QLangManifest
    parser: ParserFn | None = None
    evaluator: Callable[..., Any] | None = None
    model_config = {"arbitrary_types_allowed": True}


def _real(
    manifest: QLangManifest,
    parser: ParserFn,
    evaluator: Callable[..., Any] | None = None,
) -> RegisteredFrontEnd:
    return RegisteredFrontEnd(
        manifest=manifest,
        parser=parser,
        evaluator=evaluator,
    )


def _declared(
    language_id: str,
    name: str,
    family: str,
    subset: str,
    gate_reason: str,
    routes_to: str = "",
) -> RegisteredFrontEnd:
    return RegisteredFrontEnd(
        manifest=QLangManifest(
            id=language_id,
            name=name,
            family=family,
            tier=RegistryTier.DECLARED,
            subset=subset,
            supports_parse=False,
            supports_execute=False,
            external_gate=True,
            gate_reason=gate_reason,
            routes_to=routes_to,
        ),
        parser=None,
        evaluator=None,
    )


def _build_registry() -> dict[str, RegisteredFrontEnd]:
    reg: dict[str, RegisteredFrontEnd] = {}

    real_entries = [
        _real(
            QLangManifest(
                id="jsonpath", name="JSONPath", family="Payload",
                tier=RegistryTier.REAL, subset="RFC 9535 subset: $, .child, ['child'], [*], [n], [a:b], ..descend",
                supports_parse=True, supports_execute=True,
            ),
            jsonpath.parse, jsonpath.evaluate,
        ),
        _real(
            QLangManifest(
                id="jq", name="jq-lite", family="Payload",
                tier=RegistryTier.REAL, subset="Pipes, '.', .field, .[], select(.f == v)",
                supports_parse=True, supports_execute=True,
            ),
            jqlite.parse, jqlite.evaluate,
        ),
        _real(
            QLangManifest(
                id="xpath", name="XPath", family="Payload",
                tier=RegistryTier.REAL, subset="/a/b, //c, [@attr='v'] predicates, text() projection",
                supports_parse=True, supports_execute=True,
            ),
            xpath.parse, xpath.evaluate,
        ),
        _real(
            QLangManifest(
                id="lucene", name="Lucene query syntax", family="Search",
                tier=RegistryTier.REAL, subset="Terms, \"phrases\", field:value, AND/OR/NOT, [a TO b] ranges",
                supports_parse=True, supports_execute=True,
            ),
            lucene.parse, lucene.evaluate,
        ),
        _real(
            QLangManifest(
                id="kql_kibana", name="KQL (Kibana subset)", family="Search",
                tier=RegistryTier.REAL, subset="source | where | summarize count() by | take",
                supports_parse=True, supports_execute=True,
            ),
            kql.parse, kql.evaluate,
        ),
        _real(
            QLangManifest(
                id="promql", name="PromQL", family="Observability",
                tier=RegistryTier.REAL, subset="Instant + range queries, selectors {k=\"v\"}, sum/avg/min/max/count by (...), rate/increase[m]",
                supports_parse=True, supports_execute=True,
            ),
            promql.parse, promql.evaluate,
        ),
        _real(
            QLangManifest(
                id="datalog", name="Datalog", family="Logic",
                tier=RegistryTier.REAL, subset="Facts + rules, bottom-up semi-naive evaluation with iteration cap",
                supports_parse=True, supports_execute=True,
            ),
            datalog.parse, datalog.evaluate,
        ),
        _real(
            QLangManifest(
                id="sql", name="SQL SELECT", family="Relational",
                tier=RegistryTier.REAL, subset="SELECT cols/COUNT(*) FROM t WHERE GROUP BY ORDER BY LIMIT",
                supports_parse=True, supports_execute=True,
            ),
            sql.parse, sql.evaluate,
        ),
        _real(
            QLangManifest(
                id="graphql", name="GraphQL", family="Graph",
                tier=RegistryTier.REAL, subset="Typed selection over ontology schema, nested edge expansion, __typename",
                supports_parse=True, supports_execute=True,
            ),
            graphql.parse, graphql.execute,
        ),
        _real(
            QLangManifest(
                id="gremlin", name="Gremlin traversal", family="Graph",
                tier=RegistryTier.REAL, subset="g.V/hasLabel/has/out/in/limit/path/count",
                supports_parse=True, supports_execute=True,
            ),
            gremlin.parse, gremlin.execute,
        ),
        _real(
            QLangManifest(
                id="opencypher", name="openCypher", family="Graph",
                tier=RegistryTier.REAL, subset="MATCH (a:L)-[r:R*min..max]->(b:L) WHERE =/!= RETURN",
                supports_parse=True, supports_execute=True,
            ),
            opencypher.parse, opencypher.execute,
        ),
        _real(
            QLangManifest(
                id="sparql", name="SPARQL SELECT", family="Semantic",
                tier=RegistryTier.REAL, subset="PREFIX + triple patterns + FILTER(=,!=); serialization reuse via eoip.graph.format_converter",
                supports_parse=True, supports_execute=True,
            ),
            sparql.parse, sparql.execute,
        ),
    ]
    for entry in real_entries:
        reg[entry.manifest.id] = entry

    declared_entries = [
        _declared("gsql", "GSQL", "Graph", "TigerGraph GSQL",
                  "Requires a TigerGraph database and its GSQL SDK — external gate.", ""),
        _declared("ngql", "nGQL", "Graph", "NebulaGraph nGQL",
                  "Requires a NebulaGraph deployment and its client SDK — external gate.", ""),
        _declared("typeql", "TypeQL", "Graph", "TypeDB TypeQL",
                  "Requires a TypeDB server and typedb-client — external gate.", ""),
        _declared("aql", "AQL", "Graph", "ArangoDB AQL",
                  "Requires an ArangoDB instance and python-arango — external gate.", ""),
        _declared("pgql", "PGQL", "Graph", "Oracle PGQL",
                  "Requires an Oracle graph database with PGQL support — external gate.", ""),
        _declared("sqlpgq", "SQL/PGQ", "Graph", "ISO/IEC 39075 SQL/PGQ GRAPH_TABLE",
                  "Requires a SQL/PGQ-capable database (Oracle 23c+) — external gate.", ""),
        _declared("dql", "DQL", "Graph", "Dgraph DQL/GraphQL+-",
                  "Requires a Dgraph cluster and pydgraph — external gate.", ""),
        _declared("sparql_update", "SPARQL Update", "Semantic", "SPARQL 1.1 Update",
                  "Write path requires a real triple-store transaction manager — external gate.", ""),
        _declared("sparql_federated", "SPARQL Federated", "Semantic", "SERVICE <endpoint> federation",
                  "Requires live remote SPARQL endpoints and federated query planning — external gate.", ""),
        _declared("sparql_star", "SPARQL-star", "Semantic", "Quoted triples <<s p o>>",
                  "Requires an RDF-star triple store — external gate.", ""),
        _declared("geosparql", "GeoSPARQL", "Semantic", "Geospatial SPARQL functions",
                  "Requires a geospatial triple store (e.g. GraphDB/Strabon) — external gate.", ""),
        _declared("gremlin_dsl", "Gremlin DSL", "Graph", "Vendor Gremlin DSLs (e.g. Neptune ML)",
                  "Requires vendor-specific Gremlin bytecode extensions — external gate.", ""),
        _declared("sql_recursive_cte", "SQL recursive CTEs", "Relational", "WITH RECURSIVE",
                  "Recursive execution requires a real SQL engine; fixpoint recursion over fixtures is not faithful — external gate.", ""),
        _declared("kql_kusto", "KQL (Kusto)", "Search", "Azure Data Explorer Kusto",
                  "Requires an Azure Data Explorer cluster or kusto emulator — external gate.", ""),
        _declared("es_dsl", "Elasticsearch Query DSL", "Search", "Elastic JSON query DSL",
                  "Requires an Elasticsearch/OpenSearch cluster — external gate.", ""),
        _declared("flux", "Flux", "Observability", "InfluxDB Flux",
                  "Requires an InfluxDB 2.x instance — external gate.", ""),
        _declared("mongo_aggregation", "MongoDB aggregation", "Document", "Aggregation pipeline",
                  "Requires a MongoDB instance and pymongo — external gate.", ""),
        _declared("surrealql", "SurrealQL", "Document", "SurrealDB SurrealQL",
                  "Requires a SurrealDB instance and surrealdb client — external gate.", ""),
        _declared("sqlpp", "SQL++ (N1QL)", "Document", "Couchbase SQL++",
                  "Requires a Couchbase cluster — external gate.", ""),
        _declared("xquery", "XQuery", "Payload", "XQuery 3.1",
                  "Full XQuery requires a W3C XQuery engine (e.g. BaseX/eXist) — external gate.", ""),
        _declared("jq_full", "jq (full)", "Payload", "Full jq language",
                  "Full jq semantics require the libjq engine binding — external gate; use jq-lite subset meanwhile.", ""),
    ]

    nl2_targets = "NL2Cypher/SPARQL/Gremlin/GQL/GraphQL/KQL/PromQL/LogQL/Datalog + schema-grounded generation, validation/repair, cost estimation"
    nl2_members = [
        ("nl2cypher", "NL2Cypher"), ("nl2sparql", "NL2SPARQL"), ("nl2gremlin", "NL2Gremlin"),
        ("nl2gql", "NL2GQL"), ("nl2graphql", "NL2GraphQL"), ("nl2kql", "NL2KQL"),
        ("nl2promql", "NL2PromQL"), ("nl2logql", "NL2LogQL"), ("nl2datalog", "NL2Datalog"),
        ("nl2sql", "NL2SQL"),
    ]
    for language_id, name in nl2_members:
        declared_entries.append(
            _declared(
                language_id, name, "NL2*", nl2_targets,
                "High-fidelity natural-language-to-query generation is non-deterministic and "
                "requires an LLM hook; deterministic scaffolding routes through eoip.suggest — "
                "external gate when a generation/repair/cost model is required.",
                routes_to="eoip.suggest",
            )
        )

    for entry in declared_entries:
        reg[entry.manifest.id] = entry
    return reg


_REGISTRY: dict[str, RegisteredFrontEnd] | None = None


def registry() -> dict[str, RegisteredFrontEnd]:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = _build_registry()
    return _REGISTRY


def list_manifests() -> list[QLangManifest]:
    return [entry.manifest for entry in registry().values()]


def get(language_id: str) -> RegisteredFrontEnd:
    entry = registry().get(language_id)
    if entry is None:
        raise QLangParseError(
            f"Unknown qlang front-end: {language_id!r}. Known: {sorted(registry())}"
        )
    return entry


def parse(language_id: str, query: str) -> QLangPlan:
    """Parse ``query`` with the registered front-end, or raise honestly."""
    entry = get(language_id)
    if entry.parser is None:
        raise ExternalGateError(
            f"{entry.manifest.name} is a declared-tier capability manifest "
            f"(external gate): {entry.manifest.gate_reason}"
        )
    return entry.parser(query)


def parse_via_suggest(engine: Any, question: str, *, target: str = "cypher") -> dict[str, Any]:
    """Route an NL2* question through the existing eoip.suggest engine.

    Deterministic-first: returns structured suggestions from the store with
    graceful degradation when no LLM hook is configured. Never fabricates a
    query the engine did not produce.
    """
    from eoip.suggest.models import SuggestionRequest

    request = SuggestionRequest(question=question, limit=10)
    response = engine.suggest(request)
    return {
        "engine": "eoip.suggest",
        "target": target,
        "suggestions": [c.model_dump() for c in response.candidates],
        "llm_assist_used": response.llm_assist_used,
        "note": "NL2* deterministic scaffolding; generative/repair/cost model is an external gate.",
    }
