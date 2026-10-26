| Field | Value |
|---|---|
| Registry ID | T-C01-arcadedb |
| Tier | B (Apache-2.0 multi-model with Gremlin/Cypher/SQL; reuse candidate) |
| Versions examined | 26.10.2 (released 2026-10-15); default branch pushed 2026-10-25 |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V14 |

## 1. Identity, current status, tier, and sources
ArcadeDB is a JVM multi-model database (graph, document, key/value, search, time series, vector, geospatial), Apache-2.0, repo `ArcadeData/arcadedb` (~1.2k stars), very active: calendar-versioned releases (latest 26.10.2 on 2026-10-15; README examples reference 26.3.1 and 26.8.1) [CLAIM-arcade-01,02]. It descends from OrientDB code lineage (SQL dialect "derived from OrientDB") [CLAIM-arcade-01]. Owner: Arcade Data / ArcadeDB company (security contact support@arcadedb.com). See peers [C01-neo4j](C01-neo4j.md), [C01-arangodb](C01-arangodb.md), [C01-memgraph](C01-memgraph.md).

## 2. Primary problem, target workloads, example workflows
One engine for graph plus document plus vector plus search with several wire protocols, embeddable in a JVM or run as a server. Example: embed in a JVM service, ingest JSON documents as vertices, query via Cypher over Bolt with Neo4j drivers, and do vector search in the same store.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| Graph (LPG), documents, KV, time series, vector, geospatial | present | [CLAIM-arcade-01] |
| SQL (OrientDB-derived), openCypher, Gremlin (TinkerPop 3.7.x), GraphQL, MongoDB QL | present | openCypher completeness UNVERIFIED |
| Protocols: HTTP/JSON, Postgres wire, Bolt, Redis/Mongo subsets, gRPC modules | present/partial | Neo4j drivers tested |
| Embedded mode (JVM, Python bindings) | present | one-node friendly |
| HA: Raft-based replication, leader election | present | detail UNVERIFIED |
| Vector index in LSM, Studio vector search | present | algorithm not named in README |
| Built-in MCP server | present | agent tool interface (CAP-59) |
| Users, groups, API tokens | present | no ReBAC / source-ACL known |
| SPARQL / RDF / OWL / SHACL | absent | |
| Bitemporal / branching | absent | |

## 4. Architecture
```
 clients: HTTP | Bolt | PG wire | Gremlin | MCP
    -> query layer (SQL / Cypher / Gremlin / GraphQL parsers)
    -> engine (types: vertex/edge/document; LSM-tree indexes; transactions ACID)
    -> paginated file storage (WAL)   <-> Raft HA replication (server mode)
 embedded: same engine in-process (JVM)
```

## 5. Under-the-hood reconstruction
Records live in typed buckets with LSM-tree indexes (README mentions LSM vector-index rebuilds) [CLAIM-arcade-01]; adjacency is held as direct record pointers (index-free adjacency, HYPOTHESIS from OrientDB lineage). Multiple parsers compile into a shared execution layer; openCypher in recent versions runs a native planner (UNVERIFIED which). Concurrency: ACID transactions with WAL (README summary; MVCC detail UNVERIFIED). Replication: Raft cluster with snapshot install [CLAIM-arcade-01]. Security: user/group/token model, no row-level policy known.

## 6. Requirements inferred
JVM 17+ runtime (UNVERIFIED version); local disk with WAL; ports per protocol; optional 3-node cluster for HA.

## 7. Performance and resource model
No independent benchmark verified here; vendor claims not examined. JVM heap sizing governs cache; embedded mode avoids network cost. Failure modes: multi-model breadth means per-protocol feature unevenness (Redis/Mongo are subsets) [CLAIM-arcade-01].

## 8. Strengths
Permissive licence; many protocols mean EOIP can reuse existing Bolt/Cypher and Gremlin code paths; embedded one-node deploy fits "one-node first"; built-in vectors reduce BL-14 gap (pure-Python HNSW). Match: adapter reusing `graph/neo4j.py` patterns over Bolt/HTTP.

## 9. Limitations
| Class | Item |
|---|---|
| Maturity | small community (~1.2k stars) relative to Neo4j; calendar-version cadence with frequent releases |
| Semantics | no RDF/OWL/SHACL/reasoning |
| Friction | OrientDB-style SQL dialect is non-standard; openCypher coverage unverified |
| Security | no source-ACL/ReBAC; tenant isolation must be done above (BL-20) |
| Root cause | breadth-first multi-model scope (trade-off) |

## 10. Deployment, licensing, redistribution
Apache-2.0: redistribution-safe, patent grant. No community-vs-enterprise split stated in README (UNVERIFIED for hosted services). Runs as server, container, or embedded; no mandatory cloud; air-gap: yes (self-contained JVM). Legal review: low; verify third-party deps (TinkerPop Apache-2.0).

## 11. Competitive delta vs EOIP baseline
Adds a candidate default single-node backend with vectors (BL-14 partial), Cypher (BL-03 adapter reusable) and Gremlin (BL-02 reusable). Does not close BL-18 (ACL absent), BL-20 (tenancy partial), BL-29/30 (SHACL/OWL).

## 12. Strength cards and inversion cards
- STR-arcade-01 | ArcadeDB | Apache-2.0 embeddable multi-model with Bolt + Gremlin + vectors | CLAIM-arcade-01 | permissive one-node backend | integrate | `ArcadeDBGraphStore` over Bolt/HTTP | acceptance: conformance suite green, embedded mode air-gapped.
- STR-arcade-02 | ArcadeDB | built-in MCP server | CLAIM-arcade-01 | agent access | reject direct exposure (mutations must go via gateway) | wrap read-only | acceptance: MCP disabled by default and tenant-scoped.
- INV-arcade-01 | 26.10.2, ontology workloads | no RDF/SHACL | hypothesis: LPG-only engine (data model) | alternative: SHACL-style checks in EOIP mutation gateway (BL-28) portable across backends; worse when W3C interchange is needed | options: (a) pySHACL export (b) gateway constraint layer (c) typed-schema push-down | selected (b) | POC: constraint suite identical on ArcadeDB and Neo4j | defensibility: backend neutrality | decision: EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-04 embedded footprint | REUSE (candidate default backend) |
| CAP-53 vector search | EXPERIMENT |
| CAP-13/14 Gremlin/Cypher | INTEGRATE |
| CAP-59 MCP | REJECT as direct path; REFERENCE |
| CAP-09/10 RDFS/SHACL | REJECT (absent) |

## 14. Tests / PoC
Run `conformance.py`; ingest 10^7 edges; measure Bolt compatibility with the EOIP Neo4j adapter; verify WAL crash recovery and backup/restore (BL-50); test Raft failover.

## 15. Risks and open questions
Small vendor and bus factor; openCypher coverage and planner; vector-index algorithm and recall; JVM memory in constrained nodes.

## Appendix A. Research-dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D4 | 1-4 | covered |
| D5 storage | 5 | LSM + WAL (partly hypothesis) |
| D6 query | 3 | SQL/Cypher/Gremlin/GraphQL/Mongo |
| D7 reasoning | 9 | absent |
| D8 concurrency | 5 | ACID, Raft |
| D9 performance | 7 | no verified numbers |
| D10 versioning | 3 | absent |
| D11 security | 3,9 | users/groups/tokens |
| D12 ingestion | N/A | not examined |
| D13-D16 AI/vector | 3 | vectors + MCP |
| D17 ops | 14 | to test |
| D18 UX | 3 | Studio |
| D19-D20 licence/deploy | 10 | Apache-2.0 |
| D21 ecosystem | 9 | small |
| D22-D24 | 12,15 | covered |

## Appendix B. Capability mapping
| CAP-ID | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-01 | native | 01 | BL-01 | INTEGRATE | P1 |
| CAP-03 | native | 01 | BL-01 | REUSE | P2 |
| CAP-04 | native | 01 | BL-01 | REUSE | P1 |
| CAP-13/14 | partial/native | 01 | BL-09 partial | INTEGRATE | P2 |
| CAP-53 | native | 01 | BL-14 partial | EXPERIMENT | P2 |
| CAP-59 | native | 01 | BL-47 | REFERENCE | P3 |

## Appendix C. Evidence records
| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-arcade-01 | ArcadeDB README | Apache-2.0; models; languages; protocols; Raft HA; MCP server; vector | vendor docs | https://github.com/ArcadeData/arcadedb | accessed 2026-10-26 | 0.8 | none |
| CLAIM-arcade-02 | 26.10.2 | release 2026-10-15; push 2026-10-25; 1.2k stars | primary (API) | https://api.github.com/repos/arcadedata/arcadedb | 2026-10-26 | 0.85 | none |

## Appendix D. Assumptions
Adjacency/MVCC internals are OrientDB-lineage hypotheses; no benchmarks quoted.
