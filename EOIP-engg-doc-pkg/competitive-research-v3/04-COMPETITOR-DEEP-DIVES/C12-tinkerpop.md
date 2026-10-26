# C12 — Apache TinkerPop / Gremlin

| Field | Value |
|---|---|
| Registry ID | T-C12-tinkerpop |
| Tier | A — Gremlin is EOIP's primary backend query language (HugeGraph, JanusGraph, Neptune adapters, BL-02/04/05). |
| Versions examined | **3.8.2** (announced 2026-09-01; Maven 2026-09-02; gremlinpython 3.8.2 on PyPI 2026-09-08); **3.7.7** (Maven 2026-09-02); 3.8.1 (2026-04-01); 3.8.0 (2025-11-12; Maven 2025-11-14); 3.7.6 (2026-04-01); 3.7.0 (2023-08-01); **4.0.0-beta.3** (Maven 2026-07-21; announcement and PyPI 2026-07-27); 4.0.0-beta.2 (Maven 2026-04-02); 4.0.0-beta.1. **No 4.0.0 GA exists on Maven Central** (checked 2026-10-26). |
| Verified on | 2026-10-18 (brief date); web sources actually fetched 2026-10-26 (session clock) |
| Worker | V08 (assigned as W25) |

## 1. Identity, current status, tier, and sources

| Item | Finding |
|---|---|
| What it is | Apache top-level project: the Gremlin traversal language (a functional, data-flow language for property graphs), the Structure API providers implement, the Gremlin machine (OLTP and OLAP), Gremlin Server, Gremlin Console, language variants (Java, Groovy, Python, .NET, JavaScript, Go) and the gremlin-language ANTLR grammar [CLAIM-tp-02]. |
| Licence | Apache-2.0 (PyPI `gremlinpython` 3.8.2: "Apache 2") [CLAIM-tp-07]. Permissive. |
| Latest stable | **3.8.2** (2026-09-01) and **3.7.7** (2026-09-02) both released: two maintained lines [CLAIM-tp-01][CLAIM-tp-02][CLAIM-tp-03]. |
| 4.0 status | **Beta.** 4.0.0-beta.1, -beta.2 (2026-04), -beta.3 (2026-07) published; Maven's `latest` metadata is `4.0.0-beta.3`; no GA date announced in the beta.3 notice [CLAIM-tp-01][CLAIM-tp-04]. |
| Runtime floor | 3.8.0: Java 11 minimum, Java 8 dropped; 3.8.2: experimental JDK 21 and 25, Groovy 4.0.32; 4.0 beta: Java 11 build no longer possible, Java 21/25 supported, Netty 4.2, Spark 4.1.x (upgrade notes) [CLAIM-tp-03][CLAIM-tp-05]. gremlinpython 3.8.2 needs Python >=3.10,<3.14 [CLAIM-tp-07]. |
| Provider adoption | "more than two dozen" systems claim support (project homepage; vendor-neutral claim, not audited) [CLAIM-tp-02]. Provider versions in EOIP's world: HugeGraph on TinkerPop 3.5.1; JanusGraph 1.1.0 on 3.7.3 (1.2.0 pre-release on 3.8.2); Neptune 1.5.0.0 on 3.8.0-3.8.1; Cosmos recommends 3.4.13 drivers (internal deep dives, secondary evidence) [CLAIM-tp-11]. |
| Name collision | None material. "Gremlin" the language is unrelated to the Gremlin chaos-engineering product. |
| Members | Gremlin language/grammar, Gremlin Server, Console, GLVs, TinkerGraph (reference in-memory graph), Hadoop-Gremlin / Spark-Gremlin (OLAP), Gremlin MCP server (added 3.8.0), Gremlint formatter. |

Sources: Maven Central metadata and file timestamps, project homepage, 3.8.2 reference documentation (Gremlin Server, HTTP, parameterised scripts, protecting script execution, transactions), upgrade documentation for 3.8.x and 4.0.0-beta.1..3, beta.3 announcement, PyPI. Cross-references: `C01-amazon-neptune.md`, `C01-azure-cosmos-db-gremlin.md`, `C01-apache-hugegraph.md`, `C01-janusgraph.md`. EOIP code: `packages/eoip/graph/hugegraph.py` and `packages/eoip/adapters/janusgraph.py` read directly.

## 2. Primary problem, target workloads, concrete example workflows

| Workflow | Gremlin mechanism | EOIP relevance |
|---|---|---|
| Multi-hop impact traversal ("what is impacted if service account abc is deleted") | `g.V().has(...).repeat(out()).until(...).path()` | Customer question 1; typed `QueryPlan` templates (BL-08) must compile to this per backend |
| Idempotent upsert | `V().has(...).fold().coalesce(unfold(), addV(...))`; 3.6.2 added `mergeV/mergeE` | JanusGraph adapter uses the `coalesce` idiom; `mergeV` is the modern form (version gate) |
| Provider-neutral query | one language across HugeGraph / JanusGraph / Neptune / Cosmos | Backend neutrality; but dialect deviations are large (section 9) |
| OLAP analytics | `withComputer()` + VertexPrograms on Spark/Hadoop (PageRank, connected components) | CAP-62; spark-gremlin excluded from JDK 21/25 builds [CLAIM-tp-03] |
| LLM tooling | Gremlin MCP server (3.8.0, tools for schema discovery, formatting and executing traversals) | CAP-57/NL-query: a candidate for the "agent access" surface, read-only configuration required |
| Transactional write batches | `g.tx()` (embedded, thread-local) or remote tx (HTTP, 4.0) | Governed graph mutation needs atomic batches |

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Language | Gremlin traversal language, ~100 steps; `mergeV/E`, `elementMap`, `match()` (redesigned in 4.0 beta.3 with declarative subqueries e.g. TinkerGQL) | present | [CLAIM-tp-02][CLAIM-tp-04] |
| Grammar | `gremlin-language` ANTLR grammar; `GremlinLangScriptEngine` parses without Groovy | present (3.x optional); **default in 4.0** | [CLAIM-tp-06][CLAIM-tp-05] |
| Grammar changes | 3.8.0: `new` optional, `withoutStrategies()` in grammar, unquoted map keys matching keywords become strings; `none()` renamed `discard()`; `has(key, traversal)` removed; default date type `OffsetDateTime` | present, **breaking** | [CLAIM-tp-03] |
| Wire: transports | 3.x: WebSocket (bytecode or string scripts) and HTTP (string scripts, described as convenience/legacy); 4.0: HTTP, bytecode removed | present | [CLAIM-tp-06][CLAIM-tp-05] |
| Wire: serialisation | GraphBinary (recommended "always the best choice for drivers"), GraphSON 1/2/3 (+untyped); 4.0 beta.3 adds GraphBinary response streaming in all GLVs | present | [CLAIM-tp-06][CLAIM-tp-04] |
| Parameters | Groovy engine: `bindings` map (script caching, injection protection); 4.0: parameters are gremlin-lang literals, traversal objects rejected as parameters, nesting depth <= 32; GValue parameterisation in 3.8 | present | [CLAIM-tp-06][CLAIM-tp-05] |
| Transactions | embedded thread-local `tx()`; server sessionless = one request one tx with auto commit/rollback; sessions hold tx open; 4.0 beta: remote transactions over HTTP for all non-Java GLVs (`g.tx().begin()`, `client.transact()`, `executeInTx`) | present, provider dependent | [CLAIM-tp-06][CLAIM-tp-05] |
| Server security | SASL/Basic authentication, authorisation extension, Groovy sandbox *examples* (SimpleSandboxExtension, FileSandboxExtension); 3.7.7: Gryo disables Java serialisation, GraphSON 1.0 type allow-list, pre-auth request limits; 3.8.2: GraphSON custom `TraversalStrategy` only if registered; 4.0: Groovy disabled by default, ScriptEngine allow-list, declarative YAML | present | [CLAIM-tp-03][CLAIM-tp-05][CLAIM-tp-06] |
| Drivers | Java, Python, .NET, JavaScript, Go official; others community | present | [CLAIM-tp-02] |
| OLAP | Hadoop-Gremlin, Spark-Gremlin | present, aging (Spark 3.3 line, JDK 11/17 only in 3.8.2) | [CLAIM-tp-03] |
| UI | Gremlin Console (CLI), Gremlint; no GUI | partial | [CLAIM-tp-02] |
| Removed in 4.0 beta | bytecode, GLV translators, `sparql-gremlin` (TINKERPOP-3249), `neo4j-gremlin` (beta.2) | removal | [CLAIM-tp-05] |
| Schema, ontology, versioning, permissions per tenant | not part of TinkerPop; provider specific | absent | [CLAIM-tp-11] |

## 4. Text-based architecture diagram

```
 client apps / EOIP adapters
   │  (3.x) bytecode over WebSocket | gremlin-lang or Groovy string + bindings over WS/HTTP
   │  (4.0) gremlin-lang string + literal parameters over HTTP, GraphBinary streamed responses
   ▼
 ┌──────────────────────────── Gremlin Server (or provider's own endpoint) ───────────────────────────┐
 │ channelizer (WS / HTTP) ─► auth (SASL/Basic) ─► authorisation ext. ─► OpProcessor / HTTP handler │
 │            │                                                                                     │
 │   ScriptEngine: gremlin-groovy (full JVM, sandboxable, 3.x default)                              │
 │                 gremlin-lang (ANTLR grammar -> traversal, no JVM eval; 4.0 default)             │
 │            ▼                                                                                     │
 │   GraphTraversalSource g ─► TraversalStrategies (verification, optimisation, provider) ─► steps  │
 │            ▼                                                    ▲ transaction scope             │
 │   Structure API (Graph, Vertex, Edge, VertexProperty, Transaction)  sessionless: 1 req = 1 tx   │
 └───────────────┬───────────────────────────────────────────────────────────────────────────────┘
                 ▼
   provider storage (RocksDB/HugeGraph, Cassandra/HBase/Berkeley via JanusGraph, Neptune engine, Cosmos...)
   OLAP side channel: withComputer() -> Hadoop/Spark VertexPrograms (separate cluster)
```

## 5. Under-the-hood reconstruction

Only items traced to documentation are facts; internals not read at source level are marked H.

| Aspect | Reconstruction |
|---|---|
| Data model | Property graph: Vertex, Edge, VertexProperty (properties on properties), labels; 4.0 beta.3 adds optional multi-labelled vertices [CLAIM-tp-04]. Provider decides ids, cardinality (list/set/single), schema. |
| Query model | A traversal is a chain of steps (map, flatMap, filter, sideEffect, branch) executed by the "Gremlin machine" via lazy, pull-based traversers with bulking (a traverser carries a bulk count) (H, standard TinkerPop design; `result bulking from server` appears in 4.0 beta.1 notes [CLAIM-tp-05]). |
| Pipeline | text -> (Groovy compile **or** ANTLR parse) -> `Traversal` -> `TraversalStrategies` (decoration, optimisation, provider, finalisation, verification; e.g. `StandardVerificationStrategy` rejects `inject()`/`cap()` inside `repeat()` since 3.8.0 [CLAIM-tp-03]) -> iteration. Providers insert their own strategies for index selection and push-down (e.g. JanusGraph, Neptune native engine with per-step fallback to the reference implementation [internal CLAIM-tp-11]). |
| Caching | Gremlin Server caches compiled **scripts keyed on a hash of the exact script string**; `g.V(1)` and `g.V(2)` compile twice, `g.V(x)` with a binding once. The reference server does not cache parameterised queries beyond that: "will not see any performance improvements" with gremlin-lang parameterisation; providers may [CLAIM-tp-06]. |
| Transactions | Embedded graphs: `AbstractThreadLocalTransaction`; a tx starts implicitly on first read/write, `commit()`/`rollback()` explicit. Remote: sessionless auto-commit on success, rollback on failure, **one traversal = one transaction**; sessions keep a tx open until closed. Multi-traversal atomic batches were not possible remotely in 3.x without sessions; 4.0 adds HTTP remote tx with begin/commit/rollback and closure-managed blocks, and a safer default close [CLAIM-tp-05][CLAIM-tp-06]. The underlying isolation level is **the provider's**, not TinkerPop's. |
| Concurrency / partitioning | None in TinkerPop; provider concern. OLAP is a bulk-synchronous VertexProgram over Spark (H). |
| Versioning | TinkerPop semver with semantic changes inside minor lines (3.8.0 is breaking); GLV and server must be matched. Providers advertise their TinkerPop level. Conformance via the Gherkin feature suite (new Gherkin tags for property value types in 3.8.1 [CLAIM-tp-03]). |
| Security | Groovy: "Scripts have access to the full power of their language and the JVM"; docs say TinkerPop "does not offer an end-to-end out-of-the-box solution to perfectly protect against bad actors", sandboxes are examples; authorisation for scripts is "hardly feasible" because scripts get full environment access [CLAIM-tp-06]. gremlin-lang spares that class of problem. 4.0 flips defaults: gremlin-lang default, Groovy off, allow-listed engines [CLAIM-tp-05]. |
| Provider contract | Implement Structure API + optional strategies + `Graph.Features`; the Gherkin suite states what is supported. Cosmos and Neptune are *remote Gremlin providers* with no embedded `Graph` access (so no `Graph` transaction configuration) [CLAIM-tp-06]. |

**Re-implementation blueprint (for an EOIP gremlin-lang emitter, H):** compile `QueryPlan` templates (BL-08) to canonical gremlin-lang strings by a typed builder (no string concatenation of untrusted values); pass untrusted values only as parameters/literals; select a per-backend dialect profile (bindings yes/no, lambdas yes/no, cardinality default, id type, TinkerPop level); run the Gremlin conformance subset per backend (BL-07).

## 6. Functional and non-functional requirements inferred

| ID | Requirement for EOIP's Gremlin adapters |
|---|---|
| FR-1 | Never concatenate untrusted data into a script. Values via bindings (Groovy) or typed literals (gremlin-lang). Identifiers (labels, keys) only from validated ontology lists or an allow-list regex. |
| FR-2 | Adapter declares a dialect profile: engine (groovy/lang), bindings supported, lambdas supported, TinkerPop level, id type, default cardinality, transaction mode. |
| FR-3 | No lambdas or Groovy closures in production templates (non-portable to Neptune, Cosmos, gremlin-lang). |
| FR-4 | Atomic mutation batches use remote tx / sessions only where the backend supports them; else idempotent `mergeV/E` with replay (connectors never mutate the graph directly). |
| FR-5 | Raw-Gremlin endpoints are administrator-only and run read-only with time and result limits. |
| NFR-1 | Pin TinkerPop level per backend; run an upgrade regression suite before moving (3.8.0 changes may be silent). |
| NFR-2 | Air-gap: Maven/PyPI mirrors; Gremlin Server Docker image mirrored. |

## 7. Performance and resource model

No benchmark numbers were collected; none are claimed.

| Topic | Verified | Unknown / hypothesis |
|---|---|---|
| Script compile cost | "Compilation of a script should be considered expensive"; more parameters means more expensive compile; caching keyed on exact string [CLAIM-tp-06] | magnitude per request (needs EOIP measurement) |
| gremlin-lang parse | Documented as an alternative that avoids Groovy compile; reference server has no query cache [CLAIM-tp-06] | latency vs Groovy+cache |
| Java runtime | Java 11-25 supported by line; spark-gremlin limited | JVM RSS for a one-node Gremlin Server beside a store |
| Traversal cost | Provider-dependent; `repeat()` and unindexed `has()` can scan (H); Cosmos caps `repeat()` at 32 iterations (internal) [CLAIM-tp-11] | |
| Failure modes | `while(true){}` script exhausts the thread pool (documented); timeouts; supernode fan-out; silent semantic changes across minor versions | |

## 8. Strengths and use-case-specific advantages

| Strength | Why it matters | Match / exceed |
|---|---|---|
| Apache-2.0 and a very wide provider set | Only query language already spoken by all three EOIP reference backends (HugeGraph, JanusGraph, Neptune) | Reuse |
| Real grammar (gremlin-language, ANTLR) | Safe parse path; usable for validation, linting, translation and canonical form | Reuse for parsing and linting |
| Parameterisation and canonical-string wire in 4.0 | Injection-resistant design pushed into the protocol; human-readable logs | Adopt the pattern now |
| Conformance suite (Gherkin) | A ready-made basis for BL-07 backend conformance tests | Reuse |
| Remote transactions arriving over HTTP in 4.0 | Atomic multi-step mutations | Experiment |
| Mature OLAP path | CAP-62 beyond OLTP | Defer |
| MCP server | Agent access without writing our own server | Experiment |

## 9. Limitations with root causes

| Class | Limitation | Type | Evidence |
|---|---|---|---|
| User/developer friction | **Provider conformance is uneven**: HugeGraph built on 3.5.1; JanusGraph 1.1.0 on 3.7.3 (1.2.0 pre-release on 3.8.2, "breaking semantics"); Neptune 3.8.0-3.8.1 with ANTLR parsing, **no bindings**, set cardinality default, no lambdas; Cosmos GraphSON v2 only, drivers 3.4.13, **no bytecode, no `match()`, no lambdas**, `repeat()` capped at 32 | verified in sibling deep dives (secondary evidence) | [CLAIM-tp-11] |
| User/developer friction | TinkerPop minor releases break semantics (3.8.0 removals/renames; Neptune warns changes "may not surface as errors") | verified | [CLAIM-tp-03][CLAIM-tp-11] |
| User/developer friction | 4.0 is a large transport/API break (bytecode and translators removed, WebSocket-to-HTTP, traversals no longer passable as parameters) and not GA | verified | [CLAIM-tp-05][CLAIM-tp-01] |
| Operational | JVM-only server; OLAP stack pinned to old Spark (3.3) and JDK 11/17 in 3.8.2 | verified | [CLAIM-tp-03] |
| Security (intentional trade-off) | Groovy engine means remote code execution by design; sandbox is only an example; script authorisation infeasible | vendor-stated | [CLAIM-tp-06] |
| Security (real-world) | Cosmos DB's Gremlin sandbox escape ("CosmosEscape") shows the class of risk in a Gremlin sandbox implemented by a provider | third-party report in sibling dive | [CLAIM-tp-11] |
| Algorithmic | Traversal-based pattern matching has no cost-based join planning in the reference implementation (H); providers differ | hypothesis | n/a |
| Operational | HTTP endpoint is "convenience and legacy" in 3.x; recommended path is bytecode over WebSocket, which Neptune/Cosmos/HugeGraph do not all support | verified/mixed | [CLAIM-tp-06][CLAIM-tp-11] |
| Licensing | none (Apache-2.0); provider licences differ | n/a | [CLAIM-tp-07] |

## 10. Deployment, licensing, redistribution, and operational viability

| Item | Assessment |
|---|---|
| Deployment | Library/driver inside EOIP; optional Gremlin Server in Docker (official image on Docker Hub per beta.3 notice) [CLAIM-tp-04]. |
| Air-gap | yes (all artefacts mirrorable from Maven/PyPI/npm). |
| Licence | Apache-2.0; **no legal-review trigger** for TinkerPop itself. Per-provider licences are tracked in their own entries. |
| One-node first | Gremlin Server on JVM next to a store is feasible; JVM memory cost not measured. |
| Multi-tenant | TinkerPop has none. Tenant isolation must be enforced by the adapter (graph/partition per tenant or mandatory `tenant_id` filter strategy) and tested; a `TraversalStrategy`-based mandatory filter is a design option (H). |
| Version policy | Today pin 3.7.x or 3.8.x clients per backend; track 4.0 GA before adopting; do not adopt a beta in distributed bundles. |

## 11. Competitive delta against the EOIP verified baseline

| EOIP item | Delta |
|---|---|
| BL-02 HugeGraph adapter (REST `/gremlin`) | `execute_gremlin` posts `{"gremlin", "bindings", "language": "gremlin-groovy", "aliases"}` (`hugegraph.py:545-566`). Parameterisation: **good** for values; but the only production template uses a Groovy closure (`.filter { v -> filter_values.every {...} }`, lines 525-526) which locks it to the Groovy engine, will not run on gremlin-lang or Neptune, and would be unsafe if ever fed unvalidated text. Label is validated against `VERTEX_LABELS` and also bound (lines 515, 530) [CLAIM-tp-10]. |
| BL-05 JanusGraph adapter | Values are bound (`cid`, `val`, `vid`, `p_<key>`), numbers via `int()`. **Identifier handling is weaker**: labels and keys use `json.dumps` into double-quoted Groovy strings, and the property key `k` is interpolated *bare* as a variable name in `upsert_vertex` (line 192) and `upsert_edge` (line 276): `p_{k}`. A key that is not a valid identifier fails to compile; a hostile key could inject script text if keys originate from ingested JSON (not verified where keys are validated upstream). `json.dumps` does not escape `$`, so `${...}` inside a Groovy double-quoted string is a GString hazard. `_gremlin_string()` (line 99) is defined but not called. The sibling `C01-janusgraph.md` raised the same GString finding [CLAIM-tp-10][CLAIM-tp-11]. |
| BL-04 Neptune adapter | Neptune rejects bindings (sibling dive), so the bindings-based pattern in BL-02/05 cannot be reused; Neptune needs literals built by a safe emitter [CLAIM-tp-11]. |
| BL-08 typed bounded query plan | Strong: users never submit Gremlin; templates are named and bounded. This is the right place to hold the injection defence. |
| BL-09 portable IR compiled to Gremlin (regex subset, not on the production path) | A grammar-based emitter/parser (gremlin-language) is the missing piece; regex translation is fragile. |
| BL-07 conformance suite (not run against live engines) | TinkerPop's Gherkin feature suite is a ready source of provider-level tests. |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-tinkerpop-01** | TinkerPop | Canonical gremlin-lang with parameters as the wire format (4.0) | [CLAIM-tp-05] | Injection-resistant, loggable, auditable queries | match | `GremlinEmitter` producing canonical gremlin-lang strings from typed `QueryPlan` nodes; parameters as typed literals | Fuzz 10k hostile labels/keys/values: zero executed side effects; every emitted string re-parses with the ANTLR grammar.

**STR-tinkerpop-02** | TinkerPop | Gherkin conformance suite | [CLAIM-tp-03] | Evidence-based backend capability matrix instead of claims | integrate | Run feature subsets per backend; store results in the dialect profile | Matrix published per backend and version; regression on upgrade.

**STR-tinkerpop-03** | TinkerPop | Server "secure by default" posture in 4.0 (Groovy off, engine allow-list) | [CLAIM-tp-05] | Safer self-hosted Gremlin Server | match | Deployment profile: gremlin-lang only; reject `gremlin-groovy` | Config test: Groovy request returns an error.

**INV-tinkerpop-01 — String-built Gremlin in adapters**
- Target: EOIP adapters over TinkerPop 3.7/3.8, Groovy script engine.
- Limitation: identifiers are concatenated into script text (JanusGraph `p_{k}`, `json.dumps` labels with `$` hazard); the Groovy engine has full JVM access [CLAIM-tp-06][CLAIM-tp-10].
- Root cause: *semantics / coupling*, **proven** by code inspection; exploitability *hypothesis* (depends on where keys originate).
- Alternative design: typed emitter with identifier allow-list plus bound values; gremlin-lang engine (no Groovy). Worse when the backend only accepts Groovy (HugeGraph on 3.5.1).
- Options: (1) quick: `re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}")` validation of keys/labels and use bound names `p0..pn` instead of `p_<key>`; (2) pragmatic: shared `GremlinEmitter` used by all Gremlin adapters, `$`-escaping for Groovy strings, dialect profile; (3) long-term: gremlin-lang everywhere plus 4.0 HTTP when GA and provider support exists.
- Selected: 1 now, 2 next. Sketch: `props -> [(name_i, key_k)]; script uses .property("<key-literal-from-allowlist>", p{i}); bindings = {f"p{i}": value}`.
- Benchmark: property-based fuzz of keys/labels including `${`, quotes, newlines, `);`, unicode; success = 0 injected statements, 100% either rejected or stored verbatim; baseline = current adapter behaviour reproduced against a TinkerGraph Gremlin Server in Docker.
- Dependencies: ontology/key validation upstream; backward compat: keys with illegal characters need a mapping table (stored name vs property key); security failure: allow-list too narrow drops legitimate keys, so log and quarantine.
- Defensibility: low as a technique, high as assurance evidence for enterprise buyers.
- Decision: **ADOPT**.

**INV-tinkerpop-02 — Dialect drift between providers**
- Evidence: HugeGraph 3.5.1, JanusGraph 3.7.3/3.8.2, Neptune 3.8.x without bindings, Cosmos 3.4.13 without bytecode [CLAIM-tp-11].
- Root cause: *semantics / maturity*, proven.
- Alternative: capability-negotiated dialect profiles + a single typed IR; keep openCypher as Neptune's main path (Neptune dive). Worse for tiny single-backend deployments where the extra layer is overhead.
- Options: (1) per-adapter hand-written templates plus tests; (2) shared emitter with profiles and Gherkin-derived tests; (3) full IR compiled to Gremlin/Cypher/GQL/SPARQL (BL-09 extended).
- Selected: 2. POC: run the same 20 templates against TinkerGraph, HugeGraph, JanusGraph and Neptune (or its local substitute); success = identical result sets on the shared fixture or an explicitly declared deviation.
- Defensibility: medium-high (conformance data per backend and version). Decision: **ADOPT**.

**INV-tinkerpop-03 — Groovy closure in HugeGraph template**
- Evidence: `hugegraph.py:525-526` closure; forced `language: gremlin-groovy` (line 551) [CLAIM-tp-10].
- Root cause: *coupling*, proven.
- Alternative: express filters with `has(key, value)` steps per validated key. Worse if filter keys are open-ended and must be validated first.
- Options: (1) loop of `.has()` with validated keys and bound values; (2) emitter; (3) push search to a text index.
- Selected: 1. POC: equal results for 1,000 random filters on a fixture; no `{` closure in emitted text.
- Decision: **ADOPT**.

Seed hypotheses: #1 (multi-backend abstraction with portable IR compiled to Gremlin) - validated as needed but not yet delivered (BL-09 not on the production path); the provider-deviation evidence says a dialect profile is mandatory.

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| CAP-13 Gremlin as a backend language | INTEGRATE (TinkerPop drivers, Apache-2.0) | Native to HugeGraph, JanusGraph, Neptune. |
| Gremlin emitter / query construction | BUILD (small, typed) | No injection-safe EOIP path today. |
| gremlin-language parser | REUSE (linting, validation) | Apache-2.0 grammar. |
| Gherkin conformance suite | REUSE for BL-07 | |
| Groovy script engine in EOIP deployments | REJECT as a default | Full JVM code execution. |
| Raw user Gremlin | DEFER; admin-only and read-only | |
| Remote transactions (4.0) | EXPERIMENT after GA | Beta only. |
| TinkerPop 4.0 adoption | DEFER until GA and provider support | |
| Gremlin MCP server | EXPERIMENT (read-only profile) | |
| OLAP via Spark-Gremlin | DEFER | Old Spark/JDK constraints; prefer HugeGraph-Computer or in-process algorithms (CAP-62 handled elsewhere). |
| CAP-14/15 other languages | N/A here | Cypher/SPARQL entries. |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

| ID | Test | Acceptance |
|---|---|---|
| T-TP-01 | Fuzz hostile identifiers and values against JanusGraph and HugeGraph adapters on Dockerised servers (3.7.x) | 0 injected side effects; reject-or-store-verbatim |
| T-TP-02 | Static check: no f-string/concatenation puts non-allow-listed data into a script (lint rule in CI) | CI gate green |
| T-TP-03 | Dialect profile matrix: run 20 core templates on TinkerGraph 3.7.7, 3.8.2, HugeGraph, JanusGraph, Neptune | identical results or declared deviations |
| T-TP-04 | Upgrade regression: 3.7.7 -> 3.8.2 on JanusGraph fixture | semantic diffs listed (cardinality, `elementMap`, dates) |
| T-TP-05 | Gremlin Server with gremlin-lang only: Groovy request rejected | error returned |
| T-TP-06 | Tenant isolation: tenant A traversal cannot return tenant B vertices (mandatory filter) | 0 leaks in 10k randomised queries |
| T-TP-07 | Transaction: batch of N writes with injected failure at k | all-or-nothing on tx-capable backend; idempotent replay on others |

## 15. Risks, trade-offs, and open research questions

| Risk / question | Note |
|---|---|
| 4.0 timing | Beta only; no GA date; early adoption would break providers. |
| Provider lag | HugeGraph on 3.5.1 will not follow 3.8 or 4.0 soon (no evidence of plans; UNVERIFIED). |
| Silent semantics | Upgrades may change results without errors. |
| Groovy dependence | Some providers (HugeGraph) require Groovy scripts; sandbox quality there is NOT PUBLICLY VERIFIED in this run. |
| Open | Where do JanusGraph property keys originate and are they validated before reaching the adapter? |
| Open | Does HugeGraph's `/gremlin` honour bindings with gremlin-lang? (code forces groovy). |
| Open | Are Neptune and Cosmos adapters able to share an emitter given no bindings in Neptune? |
| Open | Value of a TraversalStrategy-based tenant filter vs adapter-level filtering. |

---

## Appendix A — Research-dimension coverage

| Dimension | Section(s) | Summary |
|---|---|---|
| D1 Identity and maturity | 1 | Apache-2.0; 3.8.2 and 3.7.7 current; 4.0 beta.3 |
| D2 Problem and workloads | 2 | Provider-neutral traversal and OLAP |
| D3 Architecture | 4, 5 | Server, script engines, strategies, providers |
| D4 Storage/indexing | N/A | Provider concern (sections 5, 9) |
| D5 Schema/semantics | 3, 5 | Property graph; multi-label in 4.0 beta |
| D6 Query pipeline | 5 | Parse/compile -> strategies -> traversers |
| D7 Reasoning | N/A | None native |
| D8 Transactions/scale | 5, 7 | Thread-local; remote one-request-one-tx; 4.0 HTTP tx |
| D9 Ingestion | N/A | Not provided; `io()` step and loaders are provider-side |
| D10 Identity/evidence | N/A | None |
| D11 Time | 3 | Dates default to `OffsetDateTime`; no bitemporality |
| D12 Graph algorithms/ML | 2, 3 | OLAP VertexPrograms; no ML |
| D13 Retrieval/agents | 2, 13 | MCP server |
| D14 NL querying | 2, 11 | Text-to-Gremlin lives elsewhere; safe emitter needed |
| D15 Governance | N/A | None |
| D16 Human experience | 3 | Console, Gremlint |
| D17 Developer experience | 3, 9 | Strong GLVs; breaking minors |
| D18 Trust/security | 5, 9, 11, 12 | Groovy RCE trade-off, injection, 3.7.7/3.8.2 hardening |
| D19 Multi-tenancy | 10 | None native |
| D20 Empirical economics | 7 | No numbers; compile-cost guidance only |
| D21 Commercial/licensing | 10 | Apache-2.0 |
| D22 Interoperability/lock-in | 8, 9 | Common language but provider deviations |
| D23 IP/prior art | N/A | Not examined; NOT PUBLICLY VERIFIED |
| D24 Evaluation harness | 8, 14 | Gherkin feature suite |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-13 Gremlin | native | [CLAIM-tp-02] | BL-02/04/05 Implemented/live-unverified | INTEGRATE | P0 |
| CAP-18 optimisation/EXPLAIN | partial (`explain()`, strategies; provider-dependent) | [CLAIM-tp-02] | Unknown | DEFER | P3 |
| CAP-62 algorithm library | partial (OLAP VertexPrograms) | [CLAIM-tp-03] | BL-44 Partial | DEFER | P3 |
| CAP-45 RBAC/ABAC | partial (server authorisation extension) | [CLAIM-tp-05][CLAIM-tp-06] | Implemented elsewhere | REUSE patterns only | P2 |
| CAP-47 tenant isolation | absent | [CLAIM-tp-06] | Implemented in EOIP (adapter-level) | BUILD/keep | P0 |
| CAP-57 agent access / MCP | partial (Gremlin MCP) | [CLAIM-tp-03] | Planned | EXPERIMENT | P2 |
| CAP-78 conformance harness | native (Gherkin) | [CLAIM-tp-03] | BL-07 Partial | REUSE | P1 |
| CAP-79 supply chain | n/a | [CLAIM-tp-07] | | INTEGRATE (mirror, pin) | P2 |
| CAP-76 HA/DR | absent (provider) | [CLAIM-tp-11] | | N/A | P3 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Claim | Classification | Source + URL | Pub / access date | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-tp-01 | gremlin-core on Maven Central | Versions 3.7.0-3.7.7, 3.8.0-3.8.2, 4.0.0-beta.1/2/3; `latest` = 4.0.0-beta.3; 4.0.0 absent; file timestamps 3.7.7 and 3.8.2 = 2026-09-02, 3.8.1 and 3.7.6 = 2026-04-01, 3.8.0 = 2025-11-14, 3.7.0 = 2023-08-01, 4.0.0-beta.2 = 2026-04-02, beta.3 = 2026-07-21 | Reproduced (HTTP) | https://repo1.maven.org/maven2/org/apache/tinkerpop/gremlin-core/maven-metadata.xml | 2026-10-26 | 0.9 (Last-Modified is upload time; may differ from announce date) | announced dates differ by 1-6 days |
| CLAIM-tp-02 | Project homepage | 3.8.2 released 1 Sept 2026; TinkerPop is an OLTP/OLAP framework; supported by more than two dozen databases; official drivers Java, Groovy, Python, .NET, Node | Officially documented | https://tinkerpop.apache.org/ | 2026-10-26 | 0.9 | none |
| CLAIM-tp-03 | Upgrade docs 3.8.x/3.7.x | 3.8.2: JDK 21/25 experimental, Groovy 4.0.32, spark-gremlin excluded from JDK 21/25, GraphSON custom strategy registration; 3.8.1: Gremlint via MCP, Gherkin tags; 3.8.0 (2025-11-12): Java 11 minimum, removals (`has(key, traversal)`, `store()`, `P.getOriginalValue()`), `none()` -> `discard()`, grammar changes, `OffsetDateTime` default, MCP server; 3.7.7 headings: Gryo Java serialisation off, GraphSON 1.0 allow-list, pre-auth limits | Officially documented | https://tinkerpop.apache.org/docs/current/upgrade/ | 2026-09 / 2026-10-26 | 0.85 (3.7.x bodies not read) | none |
| CLAIM-tp-04 | 4.0.0-beta.3 announcement | Redesigned `match()` (TinkerGQL), dynamic-argument overhaul, optional multi-label vertices, HTTP migration continues with transactions API and GraphBinary streaming in all GLVs; artefacts incl. Docker images; no GA timeline | Officially documented | https://groups.google.com/g/gremlin-users/c/3oNpgOGbWKw | 2026-07-27 / 2026-10-26 | 0.85 (summarised by a tool) | none |
| CLAIM-tp-05 | Upgrade docs 4.0.0-beta.1-3 | gremlin-lang replaces Groovy as default ScriptEngine; Groovy disabled by default; engines allow-listed in YAML; bytecode removed, GLVs emit canonical gremlin-lang strings, translators removed; traversals rejected as parameters (anti-injection), nesting depth 32; remote transactions over HTTP in all non-Java GLVs; sparql-gremlin and neo4j-gremlin removed; Java 11 no longer buildable | Officially documented | https://tinkerpop.apache.org/docs/4.0.0-beta.3/upgrade/ | 2026-07 / 2026-10-26 | 0.9 | beta: may change before GA |
| CLAIM-tp-06 | Reference docs 3.8.2 | Server transports (WS bytecode/string, HTTP string-only "convenience and legacy"); GraphBinary preferred; "imperative to use script parameterization. Period." for Groovy engine; GremlinLangScriptEngine spares those concerns; script cache keyed by exact string; GValue parameters protect against "gremlin-injection"; Groovy sandbox only examples, no end-to-end protection; script authorisation "hardly feasible"; transaction semantics (sessionless auto commit/rollback, sessions, one traversal = one tx remotely) | Officially documented | https://tinkerpop.apache.org/docs/3.8.2/reference/ | 2026-09 / 2026-10-26 | 0.9 | none |
| CLAIM-tp-07 | gremlinpython 3.8.2 | Apache 2; Python >=3.10,<3.14; 3.8.2 and 3.7.7 uploaded 2026-09-08; 4.0.0b3 2026-07-27 | Officially documented (registry API) | https://pypi.org/pypi/gremlinpython/json | 2026-10-26 | 0.9 | none |
| CLAIM-tp-10 | EOIP code | `hugegraph.py:545-566` posts bindings with `language=gremlin-groovy`; closure at 525-526; label validated and bound; `janusgraph.py:192,276` bare `p_{k}` identifiers, `json.dumps` labels/keys, `_gremlin_string` unused | Observed in source code | `packages/eoip/graph/hugegraph.py`, `packages/eoip/adapters/janusgraph.py` | repo state 2026-10-26 | 0.9 (callers upstream not traced; only one `execute_gremlin` caller found) | none |
| CLAIM-tp-11 | Provider dialects | HugeGraph on TinkerPop 3.5.1; JanusGraph 1.1.0 = 3.7.3, 1.2.0 pre-release = 3.8.2; Neptune 1.5.0.0 = 3.8.0-3.8.1, ANTLR parser, no bindings; Cosmos: GraphSON v2 only, 3.4.13 drivers recommended, no bytecode/`match()`/lambdas, `repeat()` cap 32, CosmosEscape sandbox flaw | Third-party/internal reports (secondary; not re-verified) | `C01-apache-hugegraph.md`, `C01-janusgraph.md`, `C01-amazon-neptune.md`, `C01-azure-cosmos-db-gremlin.md` in this folder | 2026-10-18 | 0.7 | primary vendor docs not re-fetched here |

## Appendix D — Assumptions

- Brief date 2026-10-18 recorded as verification date; fetches used the session clock 2026-10-26.
- Release dates for Maven artefacts come from HTTP Last-Modified; docs-announced dates are preferred where both exist (3.8.0: 2025-11-12, 3.8.2: 2026-09-01).
- TinkerPop internals (traverser bulking, strategy ordering) are stated from public design, not source reading; marked H.
- HugeGraph's Groovy sandbox and Cosmos/Neptune provider behaviour rely on the sibling deep dives (secondary evidence, confidence 0.7).
- Source of JanusGraph property keys was not traced; exploitability of `p_{k}` is a hypothesis.
- No benchmark was run.
