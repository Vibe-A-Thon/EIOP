# C02 Oxigraph

| Field | Value |
|---|---|
| Registry ID | T-C02-oxigraph |
| Tier | B (embeddable Rust SPARQL store; reuse candidate for optional RDF sidecar) |
| Versions examined | v0.5.13 (crates.io/docs.rs 2026-10-22); v0.5.12 (18 Oct), v0.5.11 (2 Sep), v0.5.10 (30 Aug) per GitHub releases (year inferred 2026) |
| Verified on | 2026-10-26 (brief 2026-10-18; v0.5.13 post-dates it) |
| Worker | V16 (registry W09) |

## 1. Identity, status, sources
Open-source "SPARQL database and RDF toolkit" in Rust (maintainer identity not verified in this run), repository `oxigraph/oxigraph` [CLAIM-oxigraph-01]. Dual licence Apache-2.0 OR MIT [CLAIM-oxigraph-01]. Fast cadence: four releases between 30 Aug and 22 Oct [CLAIM-oxigraph-02]. README itself says it is "in heavy development" and SPARQL evaluation "has not been optimized yet" (README text; release notes show ongoing optimiser work) [CLAIM-oxigraph-01,02]. Status: active, pre-1.0 (0.5.x). Cross-ref: `C02-apache-jena.md`, `C02-eclipse-rdf4j.md`, `C02-qlever.md`.

## 2. Problem and workloads
Small to medium RDF stores embedded in apps (Rust, Python `pyoxigraph`, JS/WASM), or run as a SPARQL 1.1 Protocol/Graph Store server [CLAIM-oxigraph-01]. Wikimedia's Wikidata evaluation discarded Oxigraph because it could not load Wikidata scale [CLAIM-oxigraph-05].

## 3. Feature inventory
| Feature | Status | CLAIM |
|---|---|---|
| SPARQL 1.1 Query, Update, Federated Query | present, "nearly fully conformant" | 01 |
| SPARQL 1.1 Protocol + Graph Store Protocol server (CLI) | present | 01 |
| RDF 1.2 / SPARQL 1.2 | preliminary; behind `rdf-12` Cargo feature; RDF/XML 1.2 draft since 0.5.4 | 01,02,03 |
| Parsers/serialisers (Turtle, TriG, N-Triples/Quads, RDF/XML, JSON-LD 1.1), canonicalisation | present | 01 |
| RocksDB persistence; in-memory mode (default for WASM) | present | 03,04 |
| Repeatable-read transactions, one read-write instance per data dir, backup via hard links | present | 06 |
| Python / JS bindings; standalone crates (oxrdf, spargebra, spareval) | present | 01 |
| OWL/RDFS reasoning, SHACL, full-text, GeoSPARQL, vector, auth, multi-tenancy, clustering | absent / not found | none |

## 4. Architecture
```
 CLI server (SPARQL Protocol/GSP) | Rust lib | pyoxigraph | WASM
        |
  spargebra (parse) -> algebra -> spareval (Volcano iterators, single-threaded per query)
        |
  Store: RocksDB (11 column families) or in-memory
     id2str + 9 quad indexes (spo,pos,osp ; spog,posg,ospg,gspo,gpos,gosp) + graphs
```

## 5. Reconstruction
Terms: type byte + <=32 bytes; strings <16 bytes inline, longer ones as 128-bit SipHash-2-4 with the string kept in `id2str`; IRIs stored as their hash; strings never garbage-collected [CLAIM-oxigraph-04]. Indexes: three for default graph, six for named graphs, big-endian keys for range scans (negative-number ordering flagged by the docs) [CLAIM-oxigraph-04]. Query: variables become integers, solutions arrays of encoded terms, Volcano iterators, loop vs hash join choice, greedy selectivity reordering, filter push-down; single-threaded evaluation per the wiki (may be dated) [CLAIM-oxigraph-04]; v0.5.13 improved join cost estimates and OPTIONAL planning [CLAIM-oxigraph-02]. Concurrency: repeatable-read isolation, one read-write handle per data dir; transactions buffer in memory so they are not for bulk loads; `bulk_loader` for large loads; `optimize()` can take hours on huge DBs [CLAIM-oxigraph-06]. Security/versioning/tenancy: none documented (named graphs only).

## 6. Requirements inferred
For an EOIP sidecar: named-graph-per-tenant mapping, external ACL gate in front of the SPARQL endpoint, query timeouts (not found in sources), snapshot/backup hooks (hard-link backup exists).

## 7. Performance and resource model
No benchmark run or cited. Wiki design suggests moderate throughput: single-threaded evaluation, hash-keyed IDs (low bytes per term, collisions deemed unlikely by author on a 2019 Wikidata dump [CLAIM-oxigraph-04]). Wikimedia: could not load Wikidata [CLAIM-oxigraph-05] (their scale: ~20B triples target). Failure modes: unbounded string growth, long `optimize()`, writer exclusivity.

## 8. Strengths
Permissive licence; tiny footprint; embeddable in Python (EOIP language) and WASM; clean standalone crates; transactional; active. Match for EOIP: use as optional RDF sidecar for SPARQL/RDF-star tests and JSON-LD/RDF round-trips; exceed by adding tenancy, ACL, and reasoning tiers around it.

## 9. Limitations
Algorithmic: no reasoning; limited planner (greedy); single-threaded queries (docs may lag). Operational: single read-write process, no clustering, no auth. Friction: pre-1.0 API churn (0.5.x dropped Python 3.8/3.13 free-threaded support, SPARQL Update ordering changed in 0.5.12 [CLAIM-oxigraph-02]). Outdated risk: wiki architecture page may not match current code. Licence: no flag.

## 10. Deployment, licensing
Single static binary, Docker, crate, PyPI, npm. Air-gap yes. Apache-2.0/MIT: permissive, OEM-safe; RocksDB (default feature) licence not re-verified in this run.

## 11. Delta vs baseline
BL-06 Fuseki/GraphDB adapters over HTTP could add Oxigraph as zero-JVM store; BL-29/BL-31: Oxigraph as independent oracle for JSON-LD/SPARQL behaviours; rdflib/pyshacl absent from lock (baseline §2) - pyoxigraph is a smaller dependency than rdflib but gives no SHACL.

## 12. Cards
STR-oxigraph-01 | Oxigraph | embeddable store with Python/WASM bindings and standalone parser/algebra crates | 01 | air-gapped, one-node-first RDF tier | integrate | `OxigraphGraphStore` adapter embedding pyoxigraph, one named graph per tenant, policy wrapper | test: BL-07 conformance + cross-tenant SPARQL `GRAPH ?g` probe returns nothing.
INV-oxigraph-01 | Oxigraph 0.5.13 | single-writer, no reasoning/ACL, pre-1.0 | root cause: maturity/architecture (proven for single-writer by docs [CLAIM-oxigraph-06]) | alternative: pair with EOIP policy layer and external rule tier; worse when concurrent multi-process writers needed | options: (a) embed as-is behind EOIP service (b) fork/patch (c) RDF4J/QLever for scale | select (a) EXPERIMENT | POC: 10M-triple load, mixed read/write for 1 h, record memory, p95 latency, restart time, on stated hardware | decision EXPERIMENT. Seed hypotheses §10.5 not targeted.

## 13. Capability decisions
CAP-02/04 RDF sidecar: INTEGRATE (EXPERIMENT). CAP-15 SPARQL: REUSE spargebra/spareval as parser/validator candidate (algebra-level update/SERVICE checks, cf. CRA-024). CAP-11 RDF-star/1.2: EXPERIMENT behind `rdf-12`. CAP-23 reasoning: REJECT here. CAP-74 backup: REUSE hard-link backup pattern.

## 14. Tests
PROPOSED: (1) RDF 1.2 syntax and eval tests (W3C suites) on a build with `rdf-12`; (2) SPARQL 1.1 W3C test-suite run; (3) 10M and 100M triple load and query timing; (4) crash-recovery; (5) tenant isolation via named graphs under adversarial SPARQL.

## 15. Risks, questions
Standards: RDF 1.2 Concepts is a Candidate Recommendation Snapshot (2026-04-07), SPARQL 1.2 only Working Drafts at last check, so support can change [CLAIM-oxigraph-07]. Exact single-threaded status; RocksDB build size; maintainer bus factor (UNVERIFIED).

## Appendix A. Dimensions
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | Apache/MIT, 0.5.13 |
| D2 | 2 | embedded RDF |
| D3 | 4 | crates + RocksDB |
| D4 | 5 | 11 CFs, hashed IDs |
| D5 | 3 | no SHACL/OWL |
| D6 | 5 | Volcano, greedy |
| D7 | N/A | none |
| D8 | 5,7 | repeatable read, 1 writer |
| D9 | 3 | SPARQL federation |
| D10-D12 | N/A | none |
| D13 | N/A | no FTS/vector |
| D14 | N/A | none |
| D15 | N/A | none |
| D16 | N/A | CLI/web minimal; unverified |
| D17 | 3 | bindings |
| D18 | 5 | none |
| D19 | 13 | named graphs only |
| D20 | 7 | no numbers |
| D21 | 10 | permissive |
| D22 | 3 | RDF formats |
| D23 | N/A | none |
| D24 | App C | README+docs |

## Appendix B. CAP mapping
| CAP | Oxigraph | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 01,04 | BL-06 | INTEGRATE | P2 |
| CAP-04 | native | 01 | BL-01 | INTEGRATE | P2 |
| CAP-11 | partial (1.2 flag) | 01,02 | absent | EXPERIMENT | P2 |
| CAP-15 | native | 01 | BL-06 | REUSE | P2 |
| CAP-21 | partial (SERVICE) | 01 | BL-51 | DEFER | P3 |
| CAP-74 | partial (backup) | 06 | BL-50 | REUSE pattern | P3 |

## Appendix C. Evidence
| CLAIM | version/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| oxigraph-01 | README | Apache-2.0 OR MIT; SPARQL Query/Update/Federated; "nearly fully conformant" 1.1; preliminary 1.2; RocksDB; Python/JS; Protocol + GSP server; "heavy development" | Officially documented | https://github.com/oxigraph/oxigraph | 2026-10-26 | 0.85 | none |
| oxigraph-02 | v0.5.10-0.5.13 | release notes: join estimates, OPTIONAL planning, update ordering change, Python support drops, RDF/XML 1.2 draft (0.5.4) | Officially documented | https://github.com/oxigraph/oxigraph/releases | 2026-10-26 | 0.8 | years not shown on page |
| oxigraph-03 | 0.5.13, 2026-10-22 | `rdf-12` feature enables RDF 1.2/SPARQL 1.2; `rocksdb` default | Officially documented | https://docs.rs/crate/oxigraph/latest | 2026-10-22 / 2026-10-26 | 0.85 | none |
| oxigraph-04 | wiki | 11 RocksDB tables, 3+6 indexes, 128-bit SipHash IDs, Volcano, single-threaded, greedy reorder | Officially documented | https://github.com/oxigraph/oxigraph/wiki/Architecture | 2026-10-26 | 0.7 | wiki may be dated |
| oxigraph-05 | Wikidata proposal | Oxigraph (and Jena) could not load Wikidata | Third-party report | https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update/Backend_Replacement | 2026-08-31 / 2026-10-26 | 0.6 | version tested unstated |
| oxigraph-06 | Store API | repeatable-read, one RW instance, in-memory tx buffer, bulk loader, optimize hours, hard-link backup | Officially documented | https://docs.rs/oxigraph/latest/oxigraph/store/struct.Store.html | 2026-10-26 | 0.85 | none |
| oxigraph-07 | W3C | RDF 1.2 Concepts CR Snapshot 2026-04-07; SPARQL 1.2 WDs to 2026-03-23 | Officially documented | https://www.w3.org/TR/rdf12-concepts/ | 2026-04-07 / 2026-10-26 | 0.8 | later status not checked |

## Appendix D. Assumptions
Release years inferred as 2026 from ordering and docs.rs date. Maintainer details not asserted.
