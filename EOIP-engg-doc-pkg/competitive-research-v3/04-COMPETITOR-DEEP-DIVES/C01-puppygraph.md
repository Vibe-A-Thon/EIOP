# C01 — PuppyGraph

| Field | Value |
|---|---|
| Registry ID | T-C01-puppygraph |
| Tier | B — zero-ETL graph query over SQL/lake data; OBDA-like competitor (see C04-ontop.md) |
| Versions examined | Developer and Enterprise editions per pricing page; no engine version number found; client repos updated 2026-10-18 (getting-started), 2026-10-13 (MCP server) |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V15 (W07 scope) |

## 1. Identity, current status, tier, and sources
PuppyGraph Inc. sells a graph query engine that exposes existing relational stores and lake tables as a property graph, queried with Gremlin and openCypher, with no data copy [CLAIM-puppygraph-01]. Editions: Developer (free, $0, single node, Docker, 2 concurrent data sources) and Enterprise (priced by server memory/CPU, 30-day trial, clustering, SSO, unlimited sources, AWS AMI) [CLAIM-puppygraph-02]. Engine source is not public: github.com/puppygraph contains only client/tooling repos under Apache-2.0 (Python client, MCP server, query tool, getting-started) [CLAIM-puppygraph-03]. Engine version/release cadence: NOT PUBLICLY VERIFIED. Licence of engine: proprietary EULA terms not read. Sources: pricing page, getting-started docs, GitHub org, vendor blogs.

## 2. Primary problem and workloads
Run multi-hop graph analytics on warehouse/lake/OLTP data without building a graph database or ETL; ~30 sources listed including PostgreSQL, MySQL, SQL Server, Snowflake, BigQuery, Databricks, Iceberg, Delta, Hudi, DuckDB, MongoDB, Trino [CLAIM-puppygraph-01]. EOIP workflows: graph view over a ServiceNow CMDB replica or lakehouse tables, queried by Cypher for impact analysis.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Gremlin and openCypher | Present |
| Schema mapping (JSON, Schema Builder UI, AI-assisted) | Present |
| Data sources (about 30) | Present; Developer limited to 2 |
| Row-level security walkthrough, Snowflake user impersonation, SSO (Keycloak) | Present; SSO Enterprise-only [CLAIM-puppygraph-02] |
| Clustering, monitoring (Prometheus, Datadog, health checks) | Enterprise |
| MCP server, Python client | Present (Apache-2.0 repos) |
| Writes / mutations to the graph | Absent for virtual graph (inference: read-only over sources; UNVERIFIED) |
| SPARQL, OWL/RDFS reasoning, SHACL | Absent (not found) |
| Vector / full-text | UNVERIFIED |
| Local graph storage ("Local Tables") | Present in docs navigation, details not read |

## 4. Architecture diagram
```
Gremlin/Cypher client -> PuppyGraph (graph schema mapping, planner)
   -> distributed columnar executor -> JDBC/connectors -> source tables (no copy)
   control: schema JSON, auth, cluster (Enterprise)
```

## 5. Under-the-hood reconstruction
Verified: user defines which columns are nodes/edges; engine connects to sources (BigQuery over JDBC), and the vendor describes a distributed columnar OLAP query engine with auto-sharding [CLAIM-puppygraph-04, vendor claim]. Translation internals and cost model: NOT PUBLICLY VERIFIED. Hypothesis (0.4): graph pattern compiled into joins pushed down to source engines or executed in its own vectorized engine, with edge tables as join paths. Compared with Ontop (C04): Ontop rewrites SPARQL to SQL with ontology-aware (TBox) rewriting and R2RML-style mappings; PuppyGraph maps to LPG with Gremlin/Cypher and has no found reasoning layer.

## 6. Requirements inferred
FR: declarative table->graph mapping; per-source credentials; multi-source graphs. NFR: query pushdown, source-side security honoured, read isolation from OLTP.

## 7. Performance and resource model
Vendor claim only: "10-hop queries in 2 seconds" on MotherDuck/DuckDB (blog, workload and hardware not stated) [CLAIM-puppygraph-04]; petabyte-scale claims on BigQuery are also vendor statements. No independent benchmark found. Failure modes: join explosion on deep traversals, source-load interference, data freshness equals source freshness.

## 8. Strengths
No-ETL graph over live data; wide source list; Cypher/Gremlin surface; free tier; row-level-security guidance. Match/exceed: EOIP can combine CML virtual mappings (BL-33, BL-51) with provenance and ACL enforcement that PuppyGraph lacks.

## 9. Limitations
Licensing: closed-source engine, free tier single node and 2 sources, SSO/cluster gated to paid edition (documented). Semantics: read-mostly virtual graph, no ontology/reasoning/provenance/versioning found. Operational: performance depends on source engines; cloud-warehouse dependence conflicts with air-gap unless sources are local (PostgreSQL, DuckDB, Iceberg on MinIO plausible). Dependence on JDBC credentials.

## 10. Deployment, licensing, viability
Docker self-hosted (Developer, on-prem) and AWS AMI/marketplaces (Enterprise). Air-gap: partial (Docker image local; licence enforcement/telemetry UNVERIFIED). Redistribution/OEM terms NOT PUBLICLY VERIFIED; closed engine means no white-label embedding without contract. Legal-review trigger: proprietary engine, edition feature gating, OEM terms.

## 11. Competitive delta vs baseline
BL-51 federation planner (partial) and BL-33 CML->IR mapping cover similar intent but run no distributed pushdown engine. BL-59: no SQL/PGQ; PuppyGraph does not fill it. BL-18: PuppyGraph's source-side RLS pattern is a model for ACL pushdown. BL-06: RDF-store adapters; Ontop is the open alternative.

## 12. Strength and inversion cards
STR-puppygraph-01 | PuppyGraph | zero-copy graph view over SQL/lake data | CLAIM-puppygraph-01 | live CMDB/lakehouse graph without second store | match | CML virtual-graph mode compiling QueryPlan to SQL pushdown with tenant+ACL predicates | results equal materialized graph on 1M-row test; no ACL leak.
STR-puppygraph-02 | PuppyGraph | source-side row-level security and impersonation | CLAIM-puppygraph-02 | BL-18 closure | match | pass caller identity to source | denied rows absent in all paths.
INV-puppygraph-01 | PuppyGraph Enterprise/Developer | closed engine and edition gating vs OEM/white-label | licensing, proven | alternative: Ontop (Apache-2.0) or own CML pushdown (worse: no Cypher, smaller scope) | options: (1) integrate PuppyGraph as optional customer-licensed source, (2) wrap Ontop for SPARQL virtual, (3) native CML pushdown to SQL | select (3) with (1) optional | POC: 5 multi-hop queries vs materialized baseline, success = identical rows, p95 within 3x | defensibility: provenance+ACL on virtual reads | decision EXPERIMENT. Seed hypothesis (Ontop/OBDA "virtual graphs are read-mostly and mapping-heavy") partially validated here: PuppyGraph is also read-only/mapping-driven (inference).

## 13. Per-capability decisions
CAP-21 virtualisation: BUILD native pushdown, INTEGRATE PuppyGraph/Ontop optionally. CAP-14 Cypher: INTEGRATE. CAP-46 ACL pushdown: BUILD. CAP-77: REJECT bundling.

## 14. Tests and acceptance
Run Developer image offline over PostgreSQL; map 3 tables; compare Cypher results with materialized Neo4j-like load; measure freshness lag, source load, RLS behaviour; confirm no outbound traffic.

## 15. Risks and open questions
Engine licence/EULA, telemetry, OEM; translation behaviour on deep paths; version cadence; write-back.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Closed engine, editions |
| D2 | 2 | Zero-ETL graph |
| D3 | 4 | Hypothesis |
| D4 | 5 | No own storage (verified claim) |
| D5 | 3 | Schema mapping |
| D6 | 5 | Unverified translation |
| D7 | N/A | None found |
| D8 | N/A | Source-dependent |
| D9 | 2, 3 | 30 sources, pushdown |
| D10 | N/A | None |
| D11 | N/A | Not found |
| D12 | N/A | Not read |
| D13 | 3 | MCP server |
| D14 | 3 | AI-assisted schema only |
| D15 | N/A | None |
| D16 | 3 | Explorer |
| D17 | 3 | Python, MCP |
| D18 | 3 | RLS, SSO |
| D19 | N/A | Not found |
| D20 | 7 | Vendor claims |
| D21 | 10 | Editions |
| D22 | 5, 11 | Ontop contrast |
| D23 | N/A | Not researched |
| D24 | App. C | Conf per claim |

## Appendix B — Capability mapping
| CAP | PuppyGraph | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-21 | native | -01 | BL-51 partial | BUILD / INTEGRATE | P1 |
| CAP-14 | native | -01 | BL-09 | INTEGRATE | P2 |
| CAP-46 | partial | -02 | BL-18 absent | BUILD | P0 |
| CAP-13 | native | -01 | BL-09 | DEFER | P3 |
| CAP-59 | partial | -03 | BL-47 | REFERENCE | P3 |

## Appendix C — Evidence records
| CLAIM-ID | Product/date | Claim | Class | Source | Access | Conf | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-puppygraph-01 | current | Zero-ETL graph query on relational/lake sources via Gremlin and openCypher; ~30 sources | Officially documented | docs.puppygraph.com/getting-started/ ; puppygraph.com | 2026-10-26 | 0.8 | none |
| CLAIM-puppygraph-02 | pricing page | Developer $0 single node, 2 sources, no SSO; Enterprise priced by memory/CPU, 30-day trial, clustering, SSO, AMI, monitoring | Officially documented | puppygraph.com/pricing | 2026-10-26 | 0.85 | PricingSaaS says undisclosed |
| CLAIM-puppygraph-03 | GitHub org | Public repos are client/tooling (Apache-2.0); engine not public | Observed (listing) | github.com/puppygraph | 2026-10-26 | 0.7 | none |
| CLAIM-puppygraph-04 | MotherDuck blog | Distributed columnar engine, auto-sharding, "10 hops in 2 seconds" | Third-party/vendor claim | motherduck.com/blog/duckdb-puppygraph-graph-model-on-motherduck/ | 2026-10-26 | 0.4 | no independent benchmark |

## Appendix D — Assumptions
Engine closed-source inferred from absence of engine repo. Read-only behaviour inferred, not verified.
