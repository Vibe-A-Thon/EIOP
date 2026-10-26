# C01 — Google Spanner Graph

| Field | Value |
|---|---|
| Registry ID | T-C01-spanner-graph |
| Tier | B — GQL in a distributed RDBMS; managed-cloud reference only |
| Versions examined | Managed service (no versions); release notes entries 2025-07-01 to 2026-09-11 |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V15 (W07 scope) |

## 1. Identity, current status, tier, and sources
Graph capability of Google Cloud Spanner: maps existing Spanner tables to property graphs via `CREATE PROPERTY GRAPH` and queries them with an "ISO GQL-compatible" interface; GQL and SQL interoperate on the same data [CLAIM-spanner-01]. Google's docs also state it adopts ISO GQL and SQL/PGQ (Italian-locale reference page) [CLAIM-spanner-02]. Available in Enterprise and Enterprise Plus editions, GoogleSQL dialect only (no PostgreSQL interface) [CLAIM-spanner-01]. Status: actively extended (see section 3). GA date for the original launch: NOT PUBLICLY VERIFIED here (only schemaless GA 2025-09-17 seen). Owner: Google. Proprietary managed service. Sources: Spanner Graph overview, openCypher comparison, release notes.

## 2. Primary problem and workloads
Graph queries (fraud, recommendation, supply chain, healthcare) over operational data with Spanner's consistency and scale, plus vector and full-text search for GraphRAG [CLAIM-spanner-01]. For EOIP: cloud reference for GQL semantics and SQL-plus-graph composition; not deployable on-prem.

## 3. Feature inventory
| Feature | Status |
|---|---|
| GQL queries; GRAPH clause naming target graph | Present |
| CREATE PROPERTY GRAPH over tables; graphs from SQL views (2026-01-05) | Present |
| Schemaless graph (GA 2025-09-17) | Present |
| Path search prefixes ANY, ANY SHORTEST (perf 2025-07-01), ANY CHEAPEST (2025-12-11), TRAIL mode | Present |
| Factorized execution hint `@{factorize_mode}` (2026-05-18) | Present |
| Built-in graph algorithms (centrality, clustering, similarity, paths) on dedicated compute | Present; algorithm functions Preview (2026-05-27) |
| Vector and full-text search combined with graph | Present (overview) |
| Spanner Studio visual graph schema (Preview, 2026-04-20); visualization expand/hide | Preview/Present |
| LangChain / Agent Platform GraphRAG integration | Present (overview) |
| openCypher | Absent natively; migration reference only; no predefined-schema semantics [CLAIM-spanner-02] |
| PostgreSQL dialect support | Absent |
| Self-hosted/air-gap | Absent (emulator support UNVERIFIED) |

## 4. Architecture diagram
```
Client -> Spanner frontend (GoogleSQL: SQL + GRAPH/GQL)
  -> query planner (graph pattern -> relational operators, factorized hint)
  -> distributed execution over splits (interleaved tables, Paxos groups, TrueTime)
  Algorithms: separate on-demand compute -> Cloud Storage / Spanner
```

## 5. Under-the-hood reconstruction
Verified: schema-declared property graph over table definitions; repeated edges allowed by default (TRAIL for openCypher-like uniqueness) [CLAIM-spanner-02]; factorized execution hint and path-search optimizations are documented in release notes [CLAIM-spanner-03]. Hypotheses (0.4): GQL pattern compiled to joins on Spanner tables and secondary indexes; interleaving gives locality for edge tables; external consistency inherited from Spanner core (general Spanner knowledge, not read this session).

## 6. Requirements inferred
Declarative graph over relational schema; dual GQL/SQL; explicit TRAIL/ANY semantics; schemaless option for evolving data.

## 7. Performance and resource model
No benchmark read; none quoted. Billing by Spanner compute capacity; algorithms on separate dedicated compute (cost model UNVERIFIED). Failure modes: unbounded path queries, cost of cheapest-path search.

## 8. Strengths
Closest cloud implementation of standard GQL + SQL composition; TRAIL/ANY/ANY CHEAPEST path semantics; graph from views; vector/FTS in one query. Match: adopt its path-mode vocabulary in EOIP QueryPlan (BL-08) semantics.

## 9. Limitations
Licensing: proprietary managed-only, no on-prem; lock-in to GoogleSQL; Enterprise edition cost; no PG dialect; algorithms still Preview. Semantic differences from openCypher require query rewriting (documented). Cloud egress violates EOIP default-local posture.

## 10. Deployment, licensing, viability
Managed Google Cloud only. Air-gap: no. EOIP constraint "no mandatory cloud" rules it out as bundled; usable as customer-chosen external source/target. Legal: commercial terms; no OEM path.

## 11. Competitive delta vs baseline
BL-59 (GQL/SQL-PGQ absent): Spanner shows required semantics. BL-09 IR has no TRAIL/ANY modes. BL-14 vector is pure-Python HNSW; Spanner integrates vector with graph in one engine. BL-58 N/A.

## 12. Strength and inversion cards
STR-spanner-graph-01 | Spanner Graph | explicit path-search modes (ANY, SHORTEST, CHEAPEST, TRAIL) | CLAIM-spanner-02, -03 | deterministic impact queries (J1) | match | add path_mode to QueryPlan with bounded depth | same query yields same set on two backends.
STR-spanner-graph-02 | Spanner Graph | graph defined as a view over existing tables | CLAIM-spanner-01, -03 | zero-copy graph views | match | CML->virtual graph definition | row parity vs materialized graph.
INV-spanner-graph-01 | Spanner Graph, managed | cloud-only proprietary service | licensing/deployment, proven | alternative: standard GQL/PGQ subset on local engines (worse: lose Spanner scale) | options: skip / dialect emitter / own path-mode IR | select own path-mode IR | POC: path-mode corpus on 2 local engines | defensibility: air-gap | decision ADOPT (pattern only). Seed hypotheses: none apply.

## 13. Per-capability decisions
CAP-14/16 GQL: EXPERIMENT (emit GQL-style subset). CAP-19 path modes: BUILD. CAP-62: REUSE vocabulary. Backend: REJECT.

## 14. Tests and acceptance
Build a path-semantics conformance corpus from Google's openCypher comparison page; run on rdflib/Neo4j/DuckPGQ; document divergences.

## 15. Risks and open questions
ISO GQL compliance level beyond "compatible"; GA history; emulator availability; pricing.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Google, proprietary, editions |
| D2 | 2 | Operational graph + SQL |
| D3 | 4 | Hypothesis from Spanner |
| D4 | 5 | Table-mapped |
| D5 | 3 | Schema and schemaless |
| D6 | 5 | Factorized hint |
| D7 | N/A | None |
| D8 | 5 | Inherited Spanner |
| D9 | N/A | Tables native |
| D10 | N/A | None |
| D11 | N/A | Not found |
| D12 | 3 | Algorithms (Preview) |
| D13 | 3 | GraphRAG, vector |
| D14 | N/A | Not verified |
| D15 | N/A | None |
| D16 | 3 | Studio, viz |
| D17 | 3 | LangChain |
| D18 | N/A | IAM not read |
| D19 | N/A | Not read |
| D20 | 7 | No numbers |
| D21 | 10 | Editions |
| D22 | 9 | openCypher differences |
| D23 | N/A | Not researched |
| D24 | App. C | Conf per claim |

## Appendix B — Capability mapping
| CAP | Spanner Graph | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-14 | native (GQL) | -01 | BL-08/09 | EXPERIMENT | P2 |
| CAP-16 | native | -02 | BL-59 absent | EXPERIMENT | P1 |
| CAP-19 | native | -03 | BL-09 | BUILD | P2 |
| CAP-53 | native | -01 | BL-14 | REFERENCE | P3 |
| CAP-62 | partial (Preview) | -03 | BL-43 | REFERENCE | P3 |

## Appendix C — Evidence records
| CLAIM-ID | Product/date | Claim | Class | Source | Access | Conf | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-spanner-01 | current | ISO GQL-compatible interface; tables mapped via declarative schema; GQL+SQL interop; vector/FTS; algorithms on dedicated compute; Enterprise/Enterprise Plus; GoogleSQL only | Officially documented | docs.cloud.google.com/spanner/docs/graph/overview | 2026-10-26 | 0.85 | none |
| CLAIM-spanner-02 | current | Adopts ISO GQL and SQL/PGQ; requires CREATE PROPERTY GRAPH; repeated edges by default, TRAIL for uniqueness; differs from openCypher | Officially documented | cloud.google.com/spanner/docs/graph/opencypher-reference (locale variants) | 2026-10-26 | 0.7 | overview says "compatible", not "compliant" |
| CLAIM-spanner-03 | notes 2025-07 to 2026-09 | Schemaless GA 2025-09-17; ANY CHEAPEST 2025-12-11; graphs from views 2026-01-05; factorize hint 2026-05-18; algorithms Preview 2026-05-27 | Officially documented | docs.cloud.google.com/spanner/docs/release-notes (first 100k chars only) | 2026-10-26 | 0.7 | page partly read |

## Appendix D — Assumptions
"GQL support level" = documented as compatible/adopting, no conformance certificate found. Release-note page read partially.
