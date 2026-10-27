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

## SP2Bench (CRA-024 A.2)

`tests/query/test_sp2bench_live.py` runs SP2Bench Q1–Q12c (Schmidt et al., ICDE 2009). The queries and documents come from the official SP2Bench generator, as published in RDFLib/rdflib-benchmark at commit `456f7b1c`. `scripts/fetch_sp2bench.sh` fetches them, verifying the git objects and the sha256 values in `scripts/sp2bench.sha256`. The benchmark runs through `SparqlProtocolHandler` on live Fuseki and GraphDB Free in the `sparql-fuseki` CI job.

* **Correctness** (16,040 triples): every query is answered through the endpoint and compared, as a multiset of rows, with rdflib's independent evaluation of the same query over the same document. Blank nodes match any blank node. A page truncated at 10,000 rows must be a sub-multiset of the reference. Result: 17/17 queries match on both engines.
* **Latency** (1,024,112 triples): each query runs through the endpoint under the 30 s deadline and the 10,000-row page. The engine's full evaluation, `COUNT(*)` over the query sent straight to the engine, is timed separately. Where both engines finish, they must agree on the full result size.
* **Never hang**: an over-budget query must be cancelled by the engine at the deadline and answered with a 504. The test also runs a probe at a 5 s deadline.

Local results, using the same images as CI. Endpoint time is to the first page; full time is the complete evaluation.

| Query | Fuseki 5.1.0 endpoint / full | GraphDB 10.7.6 endpoint / full |
|---|---|---|
| Q1, Q3a–c, Q8–Q11, Q12a–c | < 1 s / < 1 s | < 1 s / < 1 s |
| Q2 | 2.7 s / 1.6 s | 0.6 s / 0.3 s |
| Q4 | **> 30 s (504)** / > 30 s | 0.1 s / 14.1 s |
| Q5a | **> 30 s (504)** / > 30 s | **> 30 s (504)** / > 30 s |
| Q5b | 0.3 s / 0.6 s | 0.3 s / 0.5 s |
| Q6 | 0.9 s / 4.2 s | **> 30 s (504)** / > 30 s |
| Q7 | **> 30 s (504)** / > 30 s | 1.0 s / 1.1 s |

CRA-024 A.2 ("none exceeding 30 s") is **not met**: 3 queries on Fuseki and 2 on GraphDB exceed the budget. They are recorded as known gaps in `tests/query/sp2bench_known_gaps.json` under decision D-CRA-024-07 and are never counted as passing. A gap that starts passing fails the test until the entry is removed. The federated Jira + Snowflake clause has not been run yet: Snowflake is a paid system, so it needs a mock and remains pending live validation.

SP2Bench found three defects in the EOIP layer, all fixed and covered offline by `tests/query/test_sparql_deadline_fixes.py`:

* EOIP sent Fuseki's `timeout` in milliseconds, but Fuseki reads it as seconds. Over-budget queries kept running on the server for hours after the client gave up; they are now cancelled at the deadline.
* GraphDB answers an expired query with HTTP 200 and partial rows, flagged only in `X-GraphDB-Warning`. EOIP returned those partial rows as the answer. They are now reported as a 504.
* GraphDB 10.7 sometimes fails an interrupted query with a 500 (NullPointerException) at the deadline. EOIP now treats a 500 at the deadline as a cancellation and keeps it a backend error otherwise.

## SPARQL 1.1 Protocol endpoint (CRA-024.7; D-CRA-024-02, D-CRA-024-04)

`GET|POST /api/v1/sparql` (`packages/eoip/query/sparql_router.py`) is a read-only SPARQL 1.1 Protocol
query service:

* `GET ?query=`, `POST application/x-www-form-urlencoded`, `POST application/sparql-query`; protocol
  dataset parameters `default-graph-uri` / `named-graph-uri` are forwarded to the engine.
* Results: SPARQL JSON, XML, CSV, TSV by `Accept` (q-values honoured; none / `*/*` gives JSON; 406 when
  nothing acceptable; CSV/TSV are not offered for ASK).
* Read-only: updates (GET `update=`, form `update=`, `application/sparql-update`) are 400; methods other than
  GET/POST are 405 (`Allow: GET, POST`); other media types 415; two `query` parameters or non-UTF-8 input 400.
* Auth: no anonymous access (the API middleware answers 401 without a login session or API token); the
  route checks the `route_policy` read tier for GET and POST (viewer and above; deny by default).
* Tenancy: the engine dataset is `EOIP_SPARQL_ENDPOINT` with `{tenant}` replaced by the verified principal's
  tenant (platform superadmins without a tenant get `default`); request headers/parameters never choose it.
  `EOIP_SPARQL_BACKEND` = `fuseki` | `graphdb`; `EOIP_SPARQL_USER` / `EOIP_SPARQL_PASSWORD`. Unconfigured: 503.

W3C protocol suite (`sparql11/protocol/manifest.ttl`, 34 tests, `tests/query/test_w3c_sparql11_protocol.py`,
run through the real app with a viewer session token):

| Engine | Pass | Rejected by design | Fail |
|---|---|---|---|
| Fuseki 5.1.0 | 25 | 9 | 0 |
| GraphDB Free 10.7.6 | 25 | 9 | 0 |

Rejected by design (verified on the response): 7 update tests (endpoint is read-only, 400) and the
CONSTRUCT / DESCRIBE content-type tests (graph results are outside the supported subset, 422). Note that the
`bad_update_*` tests pass because every update is refused before parsing; they are not evidence of update
handling.

### SP2Bench over-budget investigation (2026-10-27)

Tried on the local engines with the 1.02M-triple document; none brought a listed query under 30 s, so all
five stay open gaps (details in `tests/query/sp2bench_known_gaps.json`, `investigation_2026_10_27`):
Fuseki TDB2 with the fixed optimizer, and TDB2 with `tdb2.tdbstats` statistics (Q4/Q5a/Q7 still cancelled at
30.0 s); a Q5a FILTER-to-join rewrite was rejected as not semantics-preserving (value equality vs term
identity); the endpoint already streams only the first 10,000-row page. The 30 s target is unchanged.

## Federated Jira x Snowflake query (CRA-024 A.2) - pending live validation

`packages/eoip/federation/jira_snowflake.py`: Jira issues ingested via `JiraConnector` become `WorkItem`
nodes; `query_work_items_with_snowflake` filters them in the graph and joins them with a Snowflake table
through the OBDA engine (filter and projection pushed down as bound SQL), under the 30 s deadline (TIMEOUT,
no partial rows, past it). `tests/query/test_federated_jira_snowflake.py` checks it against an independent
oracle with 3,000 paged Jira issues (REST contract mock) and ~4,500 invoices (fakesnow). No customer Jira
site or Snowflake account has been used: the result is **pending live validation**.
