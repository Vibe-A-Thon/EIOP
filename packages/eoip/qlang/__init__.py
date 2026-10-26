"""Query-language front-end registry (eoip.qlang).

Compiles external query languages to the shared ``QLangPlan`` IR
(``eoip.qlang.plans``), which lowers graph-shaped plans to the platform
``QueryPlan`` contract for policy-checked execution.

* Real deterministic parsers: JSONPath (RFC 9535 subset), jq-lite, XPath
  subset, Lucene syntax, KQL subset, PromQL, Datalog, SQL SELECT, GraphQL,
  Gremlin, openCypher, SPARQL SELECT.
* Declared-tier capability manifests (external gate, no fake parsers):
  GSQL, nGQL, TypeQL, AQL, PGQL, SQL/PGQ, DQL, SPARQL Update/Federated/
  star, GeoSPARQL, Gremlin DSL, SQL recursive CTEs, KQL-Kusto, ES DSL,
  Flux, MongoDB aggregation, SurrealQL, SQL++, XQuery, full jq, NL2* family
  (routed through eoip.suggest).
* ``eoip.qlang.taxonomy`` holds the §5.3 classification fix: RDF-family and
  metadata representation standards are Knowledge Representation, not query
  languages.
"""

from eoip.qlang.plans import (
    QLangNotMappableError,
    QLangParseError,
    QLangPlan,
)
from eoip.qlang.registry import (
    ExternalGateError,
    QLangManifest,
    RegisteredFrontEnd,
    RegistryTier,
    get,
    list_manifests,
    parse,
    parse_via_suggest,
    registry as get_registry,
)

__all__ = [
    "ExternalGateError",
    "QLangManifest",
    "QLangNotMappableError",
    "QLangParseError",
    "QLangPlan",
    "RegisteredFrontEnd",
    "RegistryTier",
    "get",
    "get_registry",
    "list_manifests",
    "parse",
    "parse_via_suggest",
]


def build_router(store=None):
    """Lazy re-export of the FastAPI router (fastapi imported inside)."""
    from eoip.qlang.router import build_router as _build

    return _build(store=store)
