# SPARQL 1.1 conformance (CRA-024.7)

EOIP's SPARQL endpoint (`eoip.query.sparql_protocol.SparqlProtocolHandler`) is measured against the
official W3C SPARQL 1.1 test suite ([w3c/rdf-tests](https://github.com/w3c/rdf-tests), `sparql/sparql11`,
pinned commit `bfefa770267ec0e5b6e45764bbca4ee43789ba72`). The suite runs on both qualified engines in the CI job
`sparql-fuseki` (`.github/workflows/validation-evidence.yml`). Per-test reports are in the
`validation-evidence-sparql` artifact (`w3c-sparql11-fuseki.json`, `w3c-sparql11-graphdb.json`).

```
bash scripts/fetch_w3c_sparql_tests.sh .cache/rdf-tests
EOIP_W3C_SUITE=.cache/rdf-tests/sparql/sparql11 EOIP_LIVE_FUSEKI_URL=http://localhost:3030/ds \
  EOIP_LIVE_FUSEKI_PASSWORD=... EOIP_LIVE_GRAPHDB_URL=http://localhost:7200 \
  python -m pytest -o addopts="" tests/query/test_w3c_sparql11_suite.py
```

## Scope

In scope: every approved test in the query-language manifests (aggregates, bind, bindings, cast, construct,
exists, functions, grouping, negation, project-expression, property-path, subquery), the JSON and CSV/TSV
result-format manifests and the query syntax manifest: 340 tests. Each one goes through the EOIP handler (protocol parsing,
governance checks, `validate_query`, paging, result serialisation) to the live engine.

Not in scope for the read-only query endpoint: SPARQL Update, federation (`SERVICE`), entailment regimes,
service description and the Graph Store Protocol manifests.

## How outcomes are judged

* **pass**: the result matches the expected one. The check uses RDF term equality and blank-node isomorphism, and respects
  row order under ORDER BY. Numerics compare by value, so `"2.0"^^xsd:decimal` equals `"2"^^xsd:decimal`. `.srx` results are
  requested as XML so that EOIP's XML serializer is exercised, and CSV/TSV tests check EOIP's CSV/TSV writers.
* **rejected_by_design**: the query uses a form that the supported subset refuses on purpose, and the
  endpoint answered 422 with the documented code. The forms are CONSTRUCT/DESCRIBE (`UNSUPPORTED_QUERY_FORM`) and unbounded `*`/`+`
  property paths (`UNBOUNDED_PROPERTY_PATH`, required by CRA-024.7). The test independently verifies that the
  query really uses the refused construct.
* **fail / error**: listed in `tests/query/w3c_sparql11_known_gaps.json`, never counted as passing. When a
  test does not pass, the identical request is replayed straight against the engine. Every recorded gap must
  fail there too, which shows the gap is an engine deviation and not an EOIP defect. A recorded gap that starts passing fails the
  test until the entry is removed.

## Results (local run, same images as CI)

| Engine | total | pass | rejected by design | engine deviations (fail/error) | EOIP-layer failures |
|---|---|---|---|---|---|
| Apache Jena Fuseki 5.1.0 | 340 | 307 | 26 | 7 | 0 |
| Ontotext GraphDB Free 10.7.6 | 340 | 286 | 26 | 28 | 0 |

The main GraphDB deviation is RDF4J's default graph, which is the union of all named graphs. Both engines refuse
VALUES-after-GROUP-BY projections, a 2023 addition to the suite. Details are in the known-gaps file.

The first run found these defects in the EOIP layer, all fixed and covered offline by
`tests/query/test_sparql_endpoint_fixes.py`:

* The page LIMIT was appended after a trailing `VALUES` block, which made the query invalid (19 tests).
* Unbounded paths were detected with text regexes, which rejected arithmetic such as `(?a)+?b` or `?a*?b` as paths. Paths are now decided on the parsed algebra.
* Malformed queries returned 503/422 instead of 400 as the Protocol requires.
* The XML results writer dropped datatypes and language tags.
* The CSV writer did not quote fields and wrote blank nodes without `_:`.
* The TSV writer emitted bare values instead of RDF terms.
