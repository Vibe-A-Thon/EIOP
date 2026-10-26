# Chapter 2 — The Query & API Layer

This chapter is the complete reference for asking questions of the EOIP knowledge
graph through its HTTP API: the `QueryPlan` contract and the `/api/v1/query/*`
family, the EQL text language, the twelve real `qlang` language front-ends plus
the declared-tier capability manifests, the natural-language suggest engine,
faceted search, retrieval strategies, the bitemporal time-travel endpoints, and
the query caches.

Everything below was read directly from the source code. Where a feature is not
exercised at runtime by the wiring in `apps/api/`, that is stated explicitly.

Example values used throughout: tenant `t-001`, issue `EOIP-123`, service
`checkout`, base URL `http://localhost:8000`. Authenticated deployments expect a
bearer token: `-H "Authorization: Bearer $TOKEN"`.

## Index

1. [The QueryPlan IR and the policy gate](#1-the-queryplan-ir)
2. [POST /api/v1/query — execute a plan](#2-post-apiv1query)
3. [POST /api/v1/query/nl — natural language](#3-post-apiv1querynl)
4. [POST /api/v1/query/eql — the EQL text language](#4-post-apiv1queryeql)
5. [Query intelligence: explain, cost, history, slow](#5-query-intelligence)
6. [Saved query templates (CRUD + bind)](#6-saved-query-templates)
7. [POST /api/v1/query/language — EOQL / OSQL / Semantic](#7-post-apiv1querylanguage)
8. [The qlang registry: real vs declared tiers](#8-the-qlang-registry)
9. [qlang endpoints: languages, taxonomy, parse, execute](#9-qlang-endpoints)
10. [The 12 real language parsers with worked examples](#10-the-12-real-parsers)
11. [Declared-tier languages and capability manifests](#11-declared-tier-languages)
12. [Suggest engine: /api/v1/suggest](#12-suggest-engine)
13. [Faceted search: POST /api/v1/search/faceted](#13-faceted-search)
14. [Retrieval: keyword / vector / hybrid with trace](#14-retrieval-search)
15. [Bitemporal endpoints](#15-bitemporal-endpoints)
16. [Query caches: EOIP_QUERY_CACHE and EOIP_REDIS_URL](#16-query-caches)
17. [Quick error reference](#quick-error-reference)

---

## 1. The QueryPlan IR

**What it does.** `QueryPlan` (packages/eoip/contracts/query_plan.py) is the single
typed, policy-validated intermediate representation for graph queries. The design
rule, quoted verbatim from the module: *"Natural language NEVER produces executable
Gremlin; it produces a QueryPlan validated against schema + policy, then executed
via a named bounded template."* Every NL front-end, template, and DSL ultimately
lowers to this shape:

```json
{"intent": "IMPACT", "anchors": ["urn:eoip:ops:service:checkout"],
 "relationship_allowlist": ["DEPENDS_ON"], "max_depth": 3, "result_limit": 50,
 "timeout_ms": 5000, "evidence_mode": "FULL", "filters": {"label": "Service"}}
```

Field reference (all enforced by Pydantic):

| Field | Type | Bounds / values |
|---|---|---|
| `intent` | enum | `SEARCH`, `PATH`, `IMPACT`, `NEIGHBORHOOD`, `LINEAGE`, `TRACEABILITY` |
| `anchors` | `list[str]` | canonical IDs or (for `SEARCH`) free-text terms; at least 1 required |
| `relationship_allowlist` | `list[str] \| null` | edge labels from the ontology manifest |
| `max_depth` | int | 1–8 |
| `result_limit` | int | 1–500 |
| `timeout_ms` | int | 50–30000, default 5000 |
| `evidence_mode` | enum | `NONE`, `SUMMARY`, `FULL` |
| `filters` | dict \| null | e.g. `{"label": "WorkItem", "include_deleted": true}` |

**The policy gate** (packages/eoip/query/policy.py). Before execution,
`QueryPolicy.validate()` rejects plans with violations such as
`"Requested depth 9 exceeds policy maximum 8"` and
`"Unknown relationship types: ['FOO']"`. `DEFAULT_POLICY` allows all six intents,
`max_depth=8`, `max_results=500`, `max_timeout_ms=30000`, `read_only=True`.
After validation the plan is **clamped** to policy bounds.

**Execution templates** (packages/eoip/query/executor.py `_TEMPLATES`): each intent
maps to a bounded handler. `SEARCH` probes exact secondary indexes first
(`WorkItem.issue_key`, `Commit.commit_sha`, `CodeSymbol.qualified_name`), then does
a substring scan over searchable properties (`canonical_id`, `name`,
`display_name`, `summary`, `issue_key`, `path`, `qualified_name`, `commit_sha`).
`PATH` requires exactly 2 anchors. `LINEAGE` is restricted to `EVIDENCED_BY` /
`INGESTED_IN` edges; `TRACEABILITY` to `IMPLEMENTS` / `REFERENCES` / `DOCUMENTS`.
Execution runs in a worker thread under `plan.timeout_ms`; overrun raises
`QueryTimeout("Query exceeded <N>ms timeout")`.

---

## 2. POST /api/v1/query

**What it does.** Executes a `QueryPlan` directly against the graph
(apps/api/app.py `@app.post("/api/v1/query", response_model=GraphResult)`).

**Step by step.**

```bash
curl -s http://localhost:8000/api/v1/query -H 'Content-Type: application/json' -d '{
  "intent": "SEARCH", "anchors": ["EOIP-123"], "max_depth": 1, "result_limit": 25,
  "timeout_ms": 5000, "evidence_mode": "SUMMARY", "filters": {"label": "WorkItem"}}'
```

**Response/result.** A `GraphResult`:

```json
{"query_id": "7c9e…",
 "nodes": [{"id": "urn:eoip:work:workitem:EOIP-123", "label": "WorkItem",
            "domain": "WORK", "properties": {"issue_key": "EOIP-123", "name": "…"}}],
 "edges": [], "paths": [], "evidence": [], "partial": false}
```

`partial: true` means the result was truncated by `result_limit` or the
5000-vertex candidate-scan cap. Traversal intents also fill `paths` and
`meta.impact_rationale`.

**Errors and recovery.**
- `422 PolicyViolation` — message lists violations (depth over policy maximum,
  unknown relationship types, `PATH` without exactly 2 anchors, a SEARCH term
  shorter than 2 characters that is neither an issue key like `EOIP-123` nor a
  40-char commit SHA). Fix the plan and retry.
- `QueryTimeout` — raised internally when `timeout_ms` is exceeded; lower
  `max_depth` or narrow the allowlist.
- Pydantic `422` — out-of-bounds numbers (e.g. `result_limit: 1000`).

---

## 3. POST /api/v1/query/nl

**What it does.** Routes a plain-English question through `NLQProcessor`
(packages/eoip/query/nlq.py). It *never* converts text into raw query language;
it picks one of five engines: `query_plan` (NL → QueryPlan → policy-checked
execution), `eql` (deterministic count/label/domain facts), `operator` (WHY /
WHY NOT / WHAT CHANGED / CONTEXT), `search_fallback`, or `clarification`.

**Step by step.**

```bash
curl -s http://localhost:8000/api/v1/query/nl -H 'Content-Type: application/json' \
  -d '{"question": "what is impacted by the checkout service?"}'
```

**Response/result.** `NLQResponse`:

```json
{"question": "what is impacted by the checkout service?", "engine": "query_plan",
 "interpretation": {"plan": {"intent": "IMPACT", "anchors": ["…"]}, "clarification": null},
 "result": {"nodes": […], "edges": […], "partial": false},
 "answer": "Found 12 entities impacted by …", "confidence": 0.9,
 "highlights": ["urn:eoip:ops:service:checkout"],
 "followups": ["Ask for impact, traceability, lineage, or a path from one result."],
 "warnings": []}
```

**Errors and recovery.** If the question is ambiguous, `engine` is
`"clarification"`, `confidence` is `0.0`, and `answer` is the clarification
prompt — rephrase with a canonical ID or issue key (the processor recognises
`urn:eoip:…` IDs, `EOIP-123`-style keys, and 40-char SHAs). `422` if the
interpreted plan violates policy.

---

## 4. POST /api/v1/query/eql

**What it does.** Executes the EOIP Query Language, a structured text DSL
(packages/eoip/query/eql.py). Registered in apps/api/app.py as
`@app.post("/api/v1/query/eql")`; the body is a plain dict `{"query": "…"}`.

**Grammar (from the module docstring and `_HELP`):**

```
FIND <label> [WHERE <prop> <op> <value>] [LIMIT <n>]     op: = != > < >= <= CONTAINS LIKE
PATH <source_cid> TO <target_cid> [MAX_DEPTH <n>]
NEIGHBORS <cid> [DEPTH <n>] [LABEL <edge_label>]
IMPACT <cid> [DEPTH <n>]
WHY <cid>  |  WHY NOT <src> <tgt>  |  WHAT CHANGED <cid>  |  CONTEXT <cid>
EDGES FROM|TO <cid> [LABEL <edge_label>]
COUNT <label|VERTICES|EDGES>
DOMAINS | LABELS | VERTEX LABELS | EDGE LABELS | HELP
```

**Step by step.**

```bash
curl -s http://localhost:8000/api/v1/query/eql -H 'Content-Type: application/json' \
  -d '{"query": "FIND WorkItem WHERE issue_key = EOIP-123 LIMIT 10"}'
```

**Response/result.**

```json
{"query": "FIND", "label": "WorkItem", "results": [
  {"canonical_id": "urn:eoip:work:workitem:EOIP-123", "label": "WorkItem",
   "name": "…", "properties": {…}}], "total": 1}
```

`COUNT VERTICES` returns `{"query": "COUNT", "target": "VERTICES", "count": 1234}`;
`PATH` returns `{"found": true, "path": [{"canonical_id": …}], "length": 4}`.

**Errors and recovery.** Errors are **200 responses with an `error` key**, not
HTTP error codes: `{"error": "Unknown label: Foo", "available": […]}`,
`{"error": "Entity not found: <cid>"}`, `{"error": "Unrecognised query: …",
"help": "…"}`. Send `{"query": "HELP"}` for the full reference inline.

---

## 5. Query intelligence

Registered in apps/api/extended.py (`GAP-QI-001..008`), backed by
`QueryIntelligence` in packages/eoip/query/intelligence.py. All estimates are
deterministic heuristics over graph statistics — no LLM calls.

### POST /api/v1/query/explain

**What it does.** Explains a plan without executing it: steps, fanout, indexes,
traversal risks.

```bash
curl -s http://localhost:8000/api/v1/query/explain -H 'Content-Type: application/json' \
  -d '{"intent":"IMPACT","anchors":["urn:eoip:ops:service:checkout"],"max_depth":3,"result_limit":50,"timeout_ms":5000,"evidence_mode":"SUMMARY"}'
```

**Response.** `ExplainedQueryPlan`: `explain_id`
(`urn:eoip:query:explain:<uuid>`), echoed `plan`, `policy_violations`, `steps`
(each with `order`, `operation` such as `anchor_lookup`/`bfs_expand`,
`estimated_visited_vertices`, `fanout`, `indexes_used` such as
`primary.canonical_id`), `total_estimated_vertices`, `estimated_fanout`,
`indexes_used`, `estimated_cost`, and `traversal_risks` (strings like
`"No relationship allowlist: traversal crosses all edge labels"`,
`"Supernode risk: average degree 23.4 …"`, `"Traversal depth 8 is at the policy
maximum"`).

### POST /api/v1/query/cost

**What it does.** Heuristic cost score for a plan (same request body as explain).

**Response.** `CostEstimate`: `score` (0–1), `grade` (`LOW` < 0.35 ≤ `MODERATE` <
0.6 ≤ `HIGH` < 0.8 ≤ `SEVERE`), `breakdown` with weighted components
`depth` (0.35), `volume` (0.35), `scan` (0.15), `timeout` (0.15), and
`estimated_vertices`.

### GET /api/v1/query/history

**What it does.** Returns the in-memory ring buffer (capacity 1000) of executed
queries. Entries are recorded by `QueryIntelligence.execute` and also emitted to
the audit sink as `query.executed` events.

**Response.** `{"history": [{"history_id": "urn:eoip:query:history:<uuid>",
"query_id": …, "intent": "SEARCH", "anchors": ["EOIP-123"], "latency_ms": 12.4,
"result_nodes": 3, "result_edges": 0, "partial": false, "cost_score": 0.21,
"explain_id": "…"}]}`.

**Honest note:** history only fills when queries run through
`QueryIntelligence.execute`; the plain `POST /api/v1/query` route uses
`QueryExecutor` directly, so whether entries appear depends on deployment
wiring — not runtime-verified here.

### GET /api/v1/query/slow

**What it does.** Slow-query report. Query params: `threshold_ms` (default 1000,
≥ 0) and `top_n` (default 10, 1–100).

```bash
curl -s 'http://localhost:8000/api/v1/query/slow?threshold_ms=500&top_n=5'
```

**Response.** `{"threshold_ms": 500, "total_executed": 42, "slow_count": 2,
"top": [QueryHistoryEntry…], "suggestions": ["Query … (SEARCH, 812ms): add a
secondary index on the filtered property or narrow the label filter to skip the
candidate scan", …]}`. When nothing is slow, `suggestions` is
`["No slow queries above threshold"]`.

---

## 6. Saved query templates

**What it does.** Parameterized, policy-validated plan templates
(`GAP-QI-007/008`). Templates are in-memory per process (not persisted across
restarts).

### Create — POST /api/v1/query/templates (201)

```bash
curl -s -X POST http://localhost:8000/api/v1/query/templates -H 'Content-Type: application/json' -d '{
  "name": "service-impact", "description": "Blast radius for a service",
  "intent": "IMPACT", "anchor_params": ["service_cid"],
  "relationship_allowlist": ["DEPENDS_ON"], "max_depth": 3, "result_limit": 100,
  "timeout_ms": 5000, "evidence_mode": "SUMMARY", "created_by": "admin@t-001"}'
```

The save *fails* (`422`, `TemplateBindingError`) if a probe-bound plan violates
policy. **Response:** the `QueryTemplate` including its
`template_id: "urn:eoip:query:template:<uuid>"`.

### List / get / delete

- `GET /api/v1/query/templates` → `{"templates": […]}`
- `GET /api/v1/query/templates/{template_id}` → one template; `404` if unknown.
- `DELETE /api/v1/query/templates/{template_id}` → `{"template_id": …, "deleted": true}`; `404` if unknown.

### Bind — POST /api/v1/query/templates/{template_id}/bind

```bash
curl -s -X POST http://localhost:8000/api/v1/query/templates/urn:eoip:query:template:abc/bind \
  -H 'Content-Type: application/json' \
  -d '{"params": {"service_cid": "urn:eoip:ops:service:checkout"}}'
```

**Response.** The bound `QueryPlan` JSON, ready to POST to `/api/v1/query`.

**Errors and recovery** (all `422` unless noted):
- *Parameter mismatch*: every declared `anchor_params` name must be supplied, no
  extras — `"Parameter mismatch: missing=[…] extra=[…]"`.
- *Injection guard*: values containing `{`, `}`, `$` or `\` are rejected —
  `"Parameter 'service_cid' contains forbidden characters"`; empty and non-string
  values are rejected too.
- *`404`* on bind/get with an unknown template id.

---

## 7. POST /api/v1/query/language

**What it does.** Dispatches to the EOQL / OSQL / Semantic parsers in
packages/eoip/query/languages.py. Each produces a `QueryPlan`-based result —
never raw Gremlin.

```bash
curl -s http://localhost:8000/api/v1/query/language -H 'Content-Type: application/json' \
  -d '{"language": "eoql", "query": "SELECT name, issue_key FROM WorkItem WHERE status = Open LIMIT 10"}'
```

**Languages.** `eoql` (`SELECT <fields> FROM <entity_type> [WHERE …] [JOIN
<rel>] [LIMIT n]`, `TRAVERSE FROM <cid> [VIA <edges>] [DEPTH n]`, `AGGREGATE
<type> BY <field>`), `osql`, and `semantic` (see `parse_osql` /
`parse_semantic_query` in languages.py for their grammars).

**Errors.** `400 "Unknown language: x. Available: ['eoql', 'osql',
'semantic']"`; syntax problems return `{"error": "Invalid EOQL SELECT syntax",
"help": "…"}` in a 200.

---

## 8. The qlang registry

packages/eoip/qlang/registry.py holds two honestly-labelled tiers:

- **`real`** — a deterministic stdlib parser *and* evaluator implemented in this
  repo (`supports_parse=true`, `supports_execute=true`). Twelve of these:
  `jsonpath`, `jq`, `xpath`, `lucene`, `kql_kibana`, `promql`, `datalog`, `sql`,
  `graphql`, `gremlin`, `opencypher`, `sparql`.
- **`declared`** — a capability manifest only (`supports_parse=false`,
  `external_gate=true`, with a `gate_reason` naming the external system
  required). Calling parse/execute on one raises `ExternalGateError` → HTTP
  `422`. Never silently faked.

All real parsers compile to the shared IR `QLangPlan`
(packages/eoip/qlang/plans.py):

```json
{"language": "lucene", "intent": "FILTER", "operation": "…", "source": "<original text>",
 "projection": [], "filters": {}, "anchors": [], "edge_labels": [],
 "min_hops": 1, "max_hops": 1, "order_by": [], "group_by": [],
 "aggregates": {}, "limit": 50, "extra": {}}
```

`intent` is one of `SEARCH`, `PATH`, `NEIGHBORHOOD`, `IMPACT` (graph-shaped,
lowercable to the platform `QueryPlan` via `to_query_plan()`) or `PROJECT`,
`FILTER`, `AGGREGATE` (payload-shaped; `to_query_plan()` raises
`QLangNotMappableError` honestly).

---

## 9. qlang endpoints

Router: packages/eoip/qlang/router.py, prefix `/api/v1/qlang`, wired in
apps/api/extended.py via `build_qlang_router(store)`.

| Method & path | Purpose |
|---|---|
| `GET /api/v1/qlang/languages` | all capability manifests |
| `GET /api/v1/qlang/languages/{language_id}` | one manifest (`404` if unknown) |
| `GET /api/v1/qlang/taxonomy` | KR-vs-query-language classification (§5.3) |
| `POST /api/v1/qlang/parse` | body `{"language", "query"}` → `QLangPlan` |
| `POST /api/v1/qlang/execute` | body `{"language", "query", "payload"?}` → result |

**Parse example.**

```bash
curl -s -X POST http://localhost:8000/api/v1/qlang/parse \
  -H 'Content-Type: application/json' \
  -d '{"language": "jsonpath", "query": "$.services[0].name"}'
```

Parse failures return `400`; declared-tier ids return `422` with the gate reason.

**Execute example (payload language).**

```bash
curl -s -X POST http://localhost:8000/api/v1/qlang/execute \
  -H 'Content-Type: application/json' \
  -d '{"language": "jq", "query": ".services[] | select(.name == \"checkout\")",
       "payload": {"services": [{"name": "checkout", "tier": 1}, {"name": "billing", "tier": 2}]}}'
```

**Response shapes.** Payload languages return `{"result": …}`; `promql` returns
`{"result": …}`; `datalog` returns `{"facts": […]}`. Graph languages (`graphql`,
`gremlin`, `opencypher`, `sparql`) execute against the live GraphStore and return
their native result shape.

**Errors.**
- `404` — unknown language id (`/languages/{id}`); for parse/execute an unknown
  id surfaces as `400` from `get()`.
- `422` — declared-tier front-end asked to parse or execute; or a language with
  no registered evaluator.
- `503` — a graph language was executed without a wired GraphStore.

**Taxonomy.** `GET /api/v1/qlang/taxonomy` returns
`{"knowledge_representation": {rdf: {…}, rdfs, owl, skos, shacl, rdf_star,
json_ld, turtle, trig, n_triples, n_quads, rdf_xml, prov_o, dc,
dublin_core_terms, owl_time, sosa, ssn}, "query_languages": [sorted ids],
"violations": []}`. RDF-family standards are deliberately classified as
*Knowledge Representation*, not query languages; `violations` must be empty —
it is a live honesty check (`assert_taxonomy_honesty()`).

---

## 10. The 12 real parsers

Each entry quotes the implemented subset from the parser module docstring and
shows a `POST /api/v1/qlang/execute` body. "Payload" languages execute against
the `payload` fixture you supply; "Graph" languages execute against the
GraphStore. All examples return `{"result": …}` unless noted.

### JSONPath (`jsonpath`) — payload
RFC 9535 subset: `$`, `.child`, `['child']`, `[*]`, `[n]`, `[a:b]`, `..descend`.
```json
{"language":"jsonpath","query":"$.services[0].name","payload":{"services":[{"name":"checkout"}]}}
```

### jq-lite (`jq`) — payload
Pipes `a | b`, identity `.`, `.field`, `.[]`, `.name[0]`,
`select(.field == "v" | .field != v)`. Anything beyond the subset (`map`,
`reduce`, string interpolation) is rejected with `QLangParseError` — *"this is a
subset, not a fake full jq."*
```json
{"language":"jq","query":".services[] | select(.tier == 1)","payload":{"services":[…]}}
```

### XPath (`xpath`) — payload
`/a/b`, `//c`, predicates `[@attr='v']`, trailing `/text()`; payloads are nested
dicts, case-sensitive.
`{"language":"xpath","query":"//service[@name='checkout']/text()","payload":{…}}`

### Lucene (`lucene`) — payload
Bare terms, `"quoted phrases"`, `field:value`, boolean `AND`/`OR`/`NOT`
(uppercase), parenthesised groups, inclusive ranges `field:[a TO b]`. Default
operator OR; executes over a list-of-dicts fixture.
```json
{"language":"lucene","query":"status:open AND assignee:sindhuja","payload":[{"status":"open","assignee":"sindhuja","key":"EOIP-123"}]}
```

### KQL — Kibana subset (`kql_kibana`) — payload
`<source> [| where field == value]* [| summarize count() by field] [| take n]`;
sources are a bare table name or `search "<query>"` / `search field:value`;
fixtures are dicts of table-name → row-list.
```json
{"language":"kql_kibana","query":"issues | where status == \"open\" | summarize count() by assignee","payload":{"issues":[{"status":"open","assignee":"sindhuja"}]}}
```

### PromQL (`promql`) — payload
Instant + range queries: `metric{label="v", other!="x"}`,
`sum/avg/min/max/count(metric) by (label)`, `rate`/`increase[m]`. Series fixture:
`[{"metric": "…", "labels": {…}, "samples": [[t, v], …]}]`, timestamps in seconds.
```json
{"language":"promql","query":"sum(http_requests_total{service=\"checkout\"}) by (status)","payload":[{"metric":"http_requests_total","labels":{"service":"checkout","status":"200"},"samples":[[1700000000,42]]}]}
```

### Datalog (`datalog`) — payload
Facts `edge("a","b").` and rules `reachable(X,Y) :- edge(X,Z), reachable(Z,Y).`;
bottom-up semi-naive evaluation with an iteration cap (default 100) guaranteeing
termination. Variables start with an uppercase letter or `_`. Response:
`{"facts": […]}`.
```json
{"language":"datalog","query":"edge(\"checkout\", \"postgres\")."}
```

### SQL SELECT (`sql`) — payload
`SELECT col[, col | COUNT(*)] FROM table [WHERE col op value [AND …]] [GROUP BY
col] [ORDER BY col [ASC|DESC]] [LIMIT n]`; operators `= != > < >= <= LIKE`.
Fixture: `{"tables": {"name": [row, …]}}`.
```json
{"language":"sql","query":"SELECT assignee, COUNT(*) FROM issues WHERE status = 'open' GROUP BY assignee","payload":{"tables":{"issues":[{"assignee":"sindhuja","status":"open"}]}}}
```

### GraphQL (`graphql`) — graph
`query { Label { scalarField relatedField { field } } }` over the ontology
schema; root fields validated against `VERTEX_LABELS`, nested objects resolve via
matching edge labels; `__typename` and `__count` supported.
`{"language":"graphql","query":"{ WorkItem { name issue_key AUTHORED_BY { name } } }"}`

### Gremlin (`gremlin`) — graph
`g.V()` / `g.V(id)`, `hasLabel('L')`, `has('k','v')`, `out('E')` / `in('E')`,
`limit(n)`, `path()`, `count()`. Lambdas, variables, side-effects are rejected.
`{"language":"gremlin","query":"g.V().hasLabel('Service').has('name','checkout').out('DEPENDS_ON').limit(10)"}`

### openCypher (`opencypher`) — graph
`MATCH (a:Label)-[r:REL]->(b:Label)`, variable hops `[r:REL*1..3]` (capped,
default 8), `WHERE a.prop = 'v' AND b.other != 'w'`, `RETURN a, b | RETURN
a.prop`. At least one bound is required.
`{"language":"opencypher","query":"MATCH (a:Service)-[r:DEPENDS_ON*1..3]->(b) WHERE a.name = 'checkout' RETURN b.name"}`

### SPARQL SELECT (`sparql`) — graph
`PREFIX` declarations, triple patterns (`?s edgeLabel ?o .` or literal constant
predicates), `FILTER(?o = "value")` / `FILTER(?s != "value")`, `LIMIT n`.
Variables bind to vertex canonical IDs; predicates to edge labels.
`{"language":"sparql","query":"SELECT ?s ?o WHERE { ?s DEPENDS_ON ?o . } LIMIT 25"}`

---

## 11. Declared-tier languages

`GET /api/v1/qlang/languages` also returns declared-tier manifests. Example shape:

```json
{"id": "pgql", "name": "PGQL", "family": "Graph", "tier": "declared",
 "subset": "Oracle PGQL", "supports_parse": false, "supports_execute": false,
 "external_gate": true,
 "gate_reason": "Requires an Oracle graph database with PGQL support — external gate.",
 "routes_to": ""}
```

Declared ids include `gsql`, `ngql`, `typeql`, `aql`, `pgql`, `sqlpgq`, `dql`,
`sparql_update`, `sparql_federated`, `sparql_star`, `geosparql`, `gremlin_dsl`,
`sql_recursive_cte`, `kql_kusto`, `es_dsl`, `flux`, `mongo_aggregation`,
`surrealql`, `sqlpp`, `xquery`, `jq_full`, plus the `NL2*` family (`nl2cypher`,
`nl2sparql`, `nl2gremlin`, `nl2gql`, `nl2graphql`, `nl2kql`, `nl2promql`,
`nl2logql`, `nl2datalog`, `nl2sql`) whose `routes_to` is `eoip.suggest`.

**How to read a manifest:** `tier="real"` + `supports_parse=true` means you can
use `/parse` and `/execute` today. `tier="declared"` means the platform
advertises the capability honestly but does not implement it; `gate_reason`
names the external system you would need. Calling `/api/v1/qlang/parse` on one
returns `422` with the gate reason.

Separately, packages/eoip/qlang/manifest_registry.py + `manifests/*.yaml`
(`eql.yaml`, `eoql.yaml`, `osql.yaml`, `sql.yaml`, `cypher.yaml`, `graphql.yaml`,
`gremlin.yaml`, `sparql.yaml`) define per-dialect grammar manifests
(`supported_constructs`, `unsupported_constructs`, `capabilities` such as
`max_depth`/`default_limit`) used to reject unsupported constructs with
`UNSUPPORTED_CAPABILITY` (CRA-024.1). EQL's manifest, for example, supports
`FIND, NEIGHBORS, PATH, IMPACT, FILTER, DEPTH, LIMIT, LABEL` and rejects
`RECURSIVE_CYCLE, EVAL_CODE, DROP_SCHEMA`.

---

## 12. Suggest engine

**What it does.** Deterministic NL suggestion (packages/eoip/suggest/): parse a
question into ranked *candidate interpretations* — each a `QueryPlan` preview
plus UX metadata — without executing anything (SR-NLQ-002). An optional
LLM-assist hook exists but is an external gate; no model is invoked by default.

### POST /api/v1/suggest and POST /api/v1/suggest/interpret

Both routes call the same engine. Request body (`SuggestionRequest`,
`extra="forbid"`):

```bash
curl -s -X POST http://localhost:8000/api/v1/suggest/interpret -H 'Content-Type: application/json' -d '{
  "question": "what is impacted if checkout goes down?",
  "session_id": "sess-t-001-42", "user_id": "admin@t-001", "roles": ["viewer"], "limit": 5}'
```

**Response** (`SuggestionResponse`) — top level: `question`, `candidates`,
`llm_assist_used` (bool), and `parse` (`{"intent", "intent_scores",
"mentions"}`). Each candidate (`CandidateInterpretation`):

```json
{"candidate_id": "cand-1", "intent": "impact",
 "paraphrase": "Compute the blast radius if checkout fails",
 "plan_preview": {"intent": "IMPACT", "anchors": ["urn:eoip:ops:service:checkout"],
                  "max_depth": 5, "result_limit": 200, "timeout_ms": 5000, "evidence_mode": "FULL"},
 "result_shape": {"kind": "impacted_set", "columns": ["entity_id","name","depth","relationship","criticality"]},
 "entity_bindings": [{"mention": "checkout", "role": "subject",
   "resolved": {"entity_id": "urn:eoip:ops:service:checkout", "display_name": "checkout",
                "entity_type": "Service", "match_basis": "name", "match_score": 1.0},
   "alternatives": […], "ambiguous": false, "pinned": false}],
 "cost_tier": "heavy", "estimated_latency_ms": 3000, "confidence": 0.83,
 "data_coverage_note": "Dependency edges plus ownership and deployment links for 'checkout' across all ingested domains.",
 "permissions": {"permissions": ["graph:read"], "evaluated": true, "allowed": true, "note": "…"},
 "answer_mode": "deterministic", "source": "template"}
```

`plan_preview.anchors` contains the *resolved* entity IDs, not the raw mention.
Confidence is `0.35 + 0.45 * (top_intent_score / total)` plus a resolution
bonus/ambiguity penalty.

Ten intents are recognised (parser.py `_INTENT_PATTERNS`): `lookup`,
`traversal`, `impact`, `ownership`, `change-history`, `coverage`, `temporal`,
`aggregation`, `similarity`, `explain-why`. Cost tiers (`COST_TIERS`):
`fast` (≤200 ms, depth 1), `moderate` (800 ms, depth 3), `heavy` (3000 ms,
depth 5), `expensive` (10000 ms, depth 8). Answer modes: `deterministic`,
`narrated`, `exploratory`, `report`.

### Other suggest routes

- `POST /api/v1/suggest/pin` — body `{"session_id", "mention", "entity_id"}`
  pins one alternative for the session (SR-NLQ-003). `422` if the entity is not
  a current candidate for that mention.
- `DELETE /api/v1/suggest/pin?session_id=…&mention=…` → `{"removed": true|false}`.
- `GET /api/v1/suggest/intents` → `{"intents": […10…], "cost_tiers": […],
  "answer_modes": […], "deterministic_tier": true, "llm_assist": "external-gate
  optional hook"}`.

**Errors and recovery.** Unknown extra request fields → Pydantic `422`
(`extra="forbid"`). If no entity resolves, candidates still return but with
`resolved: null` and `alternatives` — pin one of the alternatives, or re-ask
with a canonical ID in quotes.

---

## 13. Faceted search

### POST /api/v1/search/faceted

**What it does.** Enterprise keyword search over graph entities with facet
aggregation (GAP-SEARCH-001/002), implemented by `FacetedSearch` in
packages/eoip/search/facets.py. Deterministic token matching over text fields
(`name`, `display_name`, `qualified_name`, `issue_key`, `mr_title`,
`commit_sha`, `path`, `service_id`, `repo_id`, `summary`, `description`,
`content`, `message`); no LLM or embeddings.

```bash
curl -s -X POST http://localhost:8000/api/v1/search/faceted -H 'Content-Type: application/json' -d '{
  "query": "checkout timeout", "entity_types": ["Service", "WorkItem"],
  "domains": ["OPS"], "trust_states": ["verified"],
  "freshness": ["fresh", "recent"], "limit": 25}'
```

Request fields: `query`, `entity_types`, `domains`, `owners`, `source_systems`,
`trust_states`, `projects`, `freshness` (all lists, default empty = no filter),
`limit` (1–500, default 25).

**Response** (`SearchResponse`) — `query`, `total` (hits before paging), `hits`,
`facets`:

```json
{"query": "checkout timeout", "total": 7,
 "hits": [{"canonical_id": "urn:eoip:ops:service:checkout", "label": "Service",
   "name": "checkout", "score": 4.5, "authority": "team-payments",
   "trust_state": "verified", "freshness": "fresh", "last_seen": "2026-10-01T09:12:00Z",
   "evidence": ["src://servicenow/cmdb/ci/checkout"],
   "matched_fields": ["name", "summary"], "matched_terms": ["checkout", "timeout"],
   "why": "Matched 'checkout' in name; 'timeout' in summary"}],
 "facets": {"entity_type": [{"value": "Service", "count": 3}, {"value": "WorkItem", "count": 4}],
   "domain": [{"value": "OPS", "count": 7}], "owner": [{"value": "team-payments", "count": 2}],
   "source_system": [{"value": "servicenow", "count": 3}],
   "trust_state": [{"value": "verified", "count": 5}],
   "freshness": [{"value": "fresh", "count": 4}],
   "project": [{"value": "checkout-platform", "count": 6}]}}
```

Facet buckets: `entity_type` = vertex label; `domain` = `graph_domain`;
`freshness` buckets are `fresh` (≤30 d), `recent` (≤90 d), `aging` (≤180 d),
`stale` (>180 d), `unknown`. Every hit preserves graph identity
(`canonical_id`) plus provenance pointers in `evidence`.

**Errors.** `422` for `limit` outside 1–500. An empty `query` with filters is
valid — it is a pure facet browse.

---

## 14. Retrieval search

### POST /api/v1/retrieval/search

**What it does.** Keyword / vector / hybrid retrieval with evidence-quality
re-ranking and a deterministic trace (GAP-RET-002/003/006), from
packages/eoip/retrieval/service.py. Tenant-bound callers search only their own
index layers (SR-TEN-003).

```bash
curl -s -X POST http://localhost:8000/api/v1/retrieval/search \
  -H 'Content-Type: application/json' -H "X-Tenant-Id: t-001" \
  -d '{"question": "checkout payment timeout incidents",
       "canonical_id": "urn:eoip:ops:service:checkout",
       "strategy": "hybrid", "top_k": 10}'
```

`strategy` must match `^(keyword|vector|hybrid)$` (or be omitted — then the
router picks `direct_graph` / `code_context` / `document_context` / `hybrid`
from question keywords and the seed's label). `top_k` 1–100, default 10.

**Response** (`RetrievalResult`):

```json
{"retrieval_id": "…", "strategy": "hybrid",
 "contexts": [{"kind": "entity", "ref": "urn:eoip:…", "text": "[Service] checkout", "citations": []}],
 "evidence_refs": ["src://…"], "metrics": {"entities": 6, "edges": 9, "generation": "deterministic"},
 "answer": "Ranked 6 graph entities for 'checkout payment timeout incidents' using strategy hybrid.",
 "warnings": [], "generation": "deterministic", "partial": false,
 "facts": [{"canonical_id": "…", "type": "Service", "name": "checkout"}],
 "graph": {"source": {…}, "impacted": […], "truncated": false},
 "trace": {"steps": [{"stage": "keyword", …}, {"stage": "vector", …}, {"stage": "graph", …}, {"stage": "ranked", …}]},
 "evidence_manifest": {…}, "citation_chains": [], "answer_citations": []}
```

The `trace` field (GAP-RET-006) records each stage (`keyword`, `vector`,
`graph`, `ranked`) with its candidate list — inspect it to understand *why* a
document ranked. Hybrid scoring fuses keyword hits, vector hits (local
`HashingEmbedder` — no external service), and graph proximity to the seed.

**Errors and recovery.**
- `422 "Entity not found"` — the seed `canonical_id` does not exist, or is
  outside the caller's tenant (out-of-tenant seeds deliberately look absent).
- `403` — tenant context required but missing/mismatched `X-Tenant-Id`.
- `422` — invalid `strategy` pattern or `top_k` out of range.
- No canonical ID with no strategy → `strategy: "none"`, empty result with
  `answer: "No canonical ID provided; retrieval disabled."` (a 200, not an
  error).

---

## 15. Bitemporal endpoints

**What it does.** Pure read-layer time travel over the revision journal
(`EntityRevision` / `RelationshipRevision` vertices), from
packages/eoip/graph/bitemporal.py. Two independent axes: **transaction time**
(`known_at` — "what did we know at S", filter `observed_at <= S`) and **valid
time** (`valid_at` — "what was true at V", window `valid_from <= V <
valid_to`). Router prefix `/api/v1/graph/bitemporal`, all POST; wired in
apps/api/app.py.

### POST /api/v1/graph/bitemporal/known-at, /valid-at, /slice, /topology

One curl pattern serves all four; only the path and coordinates change:

```bash
curl -s -X POST http://localhost:8000/api/v1/graph/bitemporal/slice \
  -H 'Content-Type: application/json' \
  -d '{"valid_at": "2026-08-15T12:00:00Z", "known_at": "2026-09-01T00:00:00Z"}'
```

- **known-at** `{"known_at": S}` — latest revision per subject recorded at or
  before S. Response `BitemporalSlice`: `{"coordinate": {…}, "entities":
  [RevisionRecord…], "relationships": […]}`; each `RevisionRecord` has
  `revision_id`, `subject_id`, `kind` (`ENTITY`/`RELATIONSHIP`), `observed_at`,
  `valid_from`, `valid_to`, `graph_version`, `is_delete`, `payload`.
- **valid-at** `{"valid_at": V}` — all revisions whose valid window covers V
  (open-ended when `valid_to` is unset).
- **slice** `{valid_at, known_at}` — valid at V *as known at* S; the true
  bitemporal coordinate, latest revision per subject.
- **topology** `{valid_at, known_at}` — reconstructed graph state
  `BitemporalTopology`: `{"coordinate": {…}, "entity_ids": ["urn:eoip:…", …],
  "edges": [{"relationship_id": …, "relationship_type": "DEPENDS_ON",
  "from_id": …, "to_id": …, "revision_id": …}], "entity_count": 120,
  "edge_count": 340}`. Deletes are honoured and dangling edges dropped.

### POST /api/v1/graph/bitemporal/diff

```bash
curl -s -X POST http://localhost:8000/api/v1/graph/bitemporal/diff \
  -H 'Content-Type: application/json' \
  -d '{"from_coordinate": {"known_at": "2026-08-01T00:00:00Z"},
       "to_coordinate":   {"known_at": "2026-09-01T00:00:00Z"}}'
```

**Response** (`BitemporalDiff`): `diff_id`
(`urn:eoip:bitemporal:diff:<24-hex>`), both coordinates, and `entities` /
`relationships` / `edges` as `{added, removed, changed}` lists plus a `summary`
(`entities_added`, `entities_removed`, `edges_changed`, …).

**Errors and recovery.** Coordinates use `extra="forbid"` — unknown fields →
`422`. Omitting both coordinates in `/diff` means "everything known so far"
(the engine uses a sentinel latest-knowledge read). Timestamps compare as ISO
strings; use zero-padded UTC ISO 8601 (`2026-09-01T00:00:00Z`) or comparisons
will be lexicographically wrong. An empty slice is a valid answer, not an
error — it means no revisions existed at that coordinate.

---

## 16. Query caches

### Semantic query cache — `EOIP_QUERY_CACHE`

packages/eoip/query/cache.py implements `SemanticQueryCache`: results are keyed
by the **normalized plan** (tenant id, intent, sorted anchors, depth, limit,
evidence mode, label filter, sorted allowlist) — never by raw prompt text — and
every entry stores the graph fingerprint (`sha256` of vertex/edge counts),
graph version, source-freshness stamps, touched entities, and a max staleness
(default 3600 s). A hit is served only when fingerprint, graph version,
freshness, and staleness all still hold; otherwise the entry is evicted and
counted. CDC events evict fine-grained entries via `invalidate_cdc()`. Capacity
256 entries; eviction drops the least-hit entry. AI responses live in a strictly
separate `AIResponseCache` keyed on prompt+model+temperature (GAP-CACHE-004).

The cache is **opt-in**: `cache_enabled()` is true only when `EOIP_QUERY_CACHE`
is `1`/`true`/`yes`.

```bash
EOIP_QUERY_CACHE=1 python -m apps.api   # or your normal startup
curl -s http://localhost:8000/api/v1/query/cache/stats
# {"enabled": true, "entries": 3, "misses": 5, "evictions": 1, "hits": 4}
```

**Honest note:** `GET /api/v1/query/cache/stats` (apps/api/app.py:1053) is the
only runtime surface; it lazily creates the cache on `app.state`. Whether query
execution actually consults the cache depends on wiring that is not visible in
`apps/api/app.py`'s `/api/v1/query` handler — treat end-to-end cache hits
through that endpoint as *not runtime-verified*.

### Distributed cache — `EOIP_REDIS_URL`

packages/eoip/query/distributed_cache.py provides `DistributedQueryCache`, a
drop-in Redis-backed variant with byte-identical key/fingerprint semantics.
Keys are `eoip:qcache:<plan-hash>` with a TTL (default 300 s); staleness is
still governed by the graph fingerprint, not the TTL. If the `redis` package is
missing, `EOIP_REDIS_URL` is unset, or the server is unreachable, it **degrades
transparently** to the in-memory `SemanticQueryCache` with a one-line warning —
no failure. `stats()` adds `backend` (`"redis"` or `"memory"`), `redis_hits`,
`redis_misses`.

```bash
export EOIP_REDIS_URL=redis://localhost:6379/0
pip install 'eoip[redis]'   # provides the redis client package
```

**Honest note:** `DistributedQueryCache` is referenced from
packages/eoip/ops/production.py and its own module; no route in `apps/api/`
exposes its stats directly — the Redis path is exercised through ops/production
wiring, which was not runtime-verified for this manual.

---

## Quick error reference

| HTTP | Where | Meaning | Fix |
|---|---|---|---|
| 400 | `/qlang/parse`, `/query/language` | unparseable query / unknown language | check `detail`; send `HELP` to EQL |
| 403 | `/retrieval/search` | tenant context required | send correct `X-Tenant-Id` |
| 404 | `/qlang/languages/{id}`, templates | unknown id | list first, use exact id |
| 422 | `/query`, templates bind, suggest, bitemporal | policy violation / bad params / extra fields | read `detail`, adjust plan or params |
| 503 | `/qlang/execute` (graph languages) | no GraphStore wired | start the full API app |
| 200 with `error` key | `/query/eql`, `/query/language` | DSL-level error | inspect `error`/`help` fields |
