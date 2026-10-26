| Field | Value |
|---|---|
| Registry ID | T-C01-typedb |
| Tier | B (strong typing and inference reference for the typed mutation-gateway inversion) |
| Versions examined | TypeDB CE 3.14.1 (released 2026-10-22); 3.0 launch post dated 2025-02-11 |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V14 |

## 1. Identity, current status, tier, and sources
TypeDB (company TypeDB Ltd, formerly Vaticle) is a strongly typed database with the TypeQL query language. The 3.x line is a ground-up Rust rewrite replacing the Java 2.x codebase [CLAIM-typedb-02,03]. Community Edition source is at `typedb/typedb`, licence MPL-2.0 (weak copyleft, file-level), ~4.5k stars, latest release 3.14.1 on 2026-10-22, pushed 2026-10-24 [CLAIM-typedb-01]. Date conflict: the vendor launch post dates 3.0 to 2025-02-11 whereas Wikipedia lists 3.0.0 on 2024-12-20 (likely an earlier tag); treat 3.0 GA as early 2025 [CLAIM-typedb-03]. Commercial: TypeDB Cloud (DBaaS) and TypeDB Enterprise (self-hosted cloud edition) [CLAIM-typedb-02]. The 3.x line does not read as a continuation of 2.x on-disk data: migration path UNVERIFIED. Peers: [C01-neo4j](C01-neo4j.md) (seed inversion row), [C01-janusgraph](C01-janusgraph.md).

## 2. Primary problem, target workloads, example workflows
Model complex, polymorphic domains where structure matters (life sciences, security, enterprise knowledge). Schema defines entities, relations (role-based, n-ary) and attributes with inheritance and interfaces; data insertion is validated against it [CLAIM-typedb-02]. Example: `insert $p isa employee, has name "A"; $r (manager: $m, report: $p) isa management;` is rejected if types or roles are wrong.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| Strong static typing, inheritance, interfaces | present | [CLAIM-typedb-02] |
| n-ary relations with roles, relations as first-class | present | hyperedge-like (CAP-11) |
| Constraints: cardinality, value range, value enumeration | present in 3.0 | [CLAIM-typedb-03] |
| TypeQL functions (reusable subqueries) | present; replace 2.x rules | [CLAIM-typedb-03] |
| Query pipelines (read/write/transform in one query) | present | [CLAIM-typedb-03] |
| Rule-based inference (2.x rules) | removed/replaced by functions | removal detail UNVERIFIED |
| OWL/RDF/SPARQL, SHACL | absent | |
| Drivers: gRPC-based (Rust, Python, Java, others) | present; list UNVERIFIED | |
| HA/clustering | Enterprise only (UNVERIFIED) | CE single node |
| Bitemporal/branching | absent | |

## 4. Architecture
```
 driver (gRPC) -> server: TypeQL parse -> type-check against schema
     -> pipeline planner (match/insert/delete/update/reduce + functions)
     -> executor -> MVCC-style transactions -> RocksDB storage
 schema (types, roles, constraints, functions) stored in the database
```

## 5. Under-the-hood reconstruction
The README names Rust, RocksDB and gRPC as core technologies [CLAIM-typedb-02]. A query is type-checked against the schema (type inference over polymorphic variables) before execution; writes are validated for type, role and constraint conformance, which is exactly the property EOIP wants in its mutation gateway (BL-28 only checks labels/required properties). Functions compile into the same pipeline as recursive/sub-queries (3.0 positions them as the replacement for rules) [CLAIM-typedb-03]. Transaction isolation level and storage key layout: UNVERIFIED. Security: users/roles in the server; no row-level or tenant isolation primitive verified.

## 6. Requirements inferred
Schema-first data entry; mutation API that rejects ill-typed writes with machine-readable errors; reusable named read-functions; schema versioning/migration.

## 7. Performance and resource model
The vendor states performance improved "at all levels" and a smaller memory footprint but gives no figures; benchmarks are promised, none verified here [CLAIM-typedb-03]. Uncertainty: type inference cost on deep hierarchies; function recursion cost.

## 8. Strengths
Type-checked reads and writes at the database; expressive n-ary modelling; query pipelines reduce round trips; Rust footprint. Exceed approach: EOIP enforces equivalent constraints backend-neutrally in the gateway.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | MPL-2.0 CE (file-level copyleft: modifications to MPL files must be shared); clustering/Enterprise proprietary (UNVERIFIED) |
| Intentional trade-off | strict schema-first slows exploratory ingest |
| Friction | TypeQL is proprietary (no GQL/Cypher/SPARQL), 2.x to 3.x breaking language change; rules replaced |
| Operational | single-node CE; no verified HA in CE |
| Root cause | custom type-theoretic data model (data model/semantics) |

## 10. Deployment, licensing, redistribution
CE can be self-hosted, air-gap viable. MPL-2.0 permits linking and bundling unmodified binaries; legal review trigger for any fork or modified MPL files and for Enterprise terms. Not a drop-in `GraphStore` backend (no LPG query language); better as a design reference or a typed side-store.

## 11. Competitive delta vs EOIP baseline
BL-28 validation gate is label/required-property level; BL-29 SHACL is partial; BL-10 in-house DSLs. TypeDB shows role-typed relations, cardinality and value constraints plus named functions; the EOIP gateway lacks cardinality, value-range and role-type constraints. Seed hypothesis (Neo4j row "typed property graph with SHACL/TypeQL-style constraints in mutation gateway"): validated as a design direction; TypeDB itself rejected as a backend.

## 12. Strength cards and inversion cards
- STR-typedb-01 | TypeDB | write-time type, role and cardinality validation | CLAIM-typedb-02,03 | no graph decay | match/exceed | extend `validation/gate.py` with a constraint model (cardinality, range, enum, role types) compiled from ontology | acceptance: 100% of ill-typed writes in a corpus rejected on Neo4j and HugeGraph with the same error codes.
- STR-typedb-02 | TypeDB | named reusable functions | CLAIM-typedb-03 | governed inference/queries | match | versioned, registered read-only query-plan fragments in BL-08 | acceptance: function inlined into typed plan with budget check.
- INV-typedb-01 | CE 3.14.1, enterprise KG | proprietary language and single-vendor storage | root cause data model/licensing (proven by design) | alternative: typed constraints enforced above any backend; worse when constraints must be enforced against writes bypassing the gateway | options: (a) wrap TypeDB as backend (b) gateway constraint layer (c) own typed-schema compiler to SHACL + backend constraints | selected (b) then (c) | POC: 200-case constraint corpus; success = identical accept/reject on 3 backends; baseline BL-28 | failure case: out-of-band writes | defensibility: backend neutrality | decision: ADOPT (design), REJECT (backend).

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-08 schema/typing/constraint enforcement | BUILD (inspired by TypeQL) |
| CAP-11 n-ary relations | EXPERIMENT (relation-as-node pattern) |
| CAP-22 rules vs functions | EXPERIMENT |
| CAP-01 as backend | REJECT |
| CAP-20 portable IR | REFERENCE-ONLY |

## 14. Tests / PoC
Model the EOIP core ontology in TypeQL 3.x; run the 200-case constraint corpus; port the same constraints to gateway; measure write latency overhead.

## 15. Risks and open questions
Date and migration ambiguity between 2.x and 3.x; which features are Enterprise-only; MPL scope; TypeQL stability across 3.x minors.

## Appendix A. Research-dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D4 | 1-4 | covered |
| D5 storage | 5 | RocksDB (README) |
| D6 query | 3,5 | TypeQL pipelines |
| D7 reasoning | 3 | functions replace rules |
| D8 concurrency | 5 | UNVERIFIED |
| D9 performance | 7 | no numbers |
| D10 versioning | 3 | absent |
| D11 security | 5 | basic |
| D12 ingestion | N/A | not examined |
| D13-D16 AI | N/A | not examined |
| D17 ops | 9 | single-node CE |
| D18 UX | N/A | Studio not examined |
| D19-D20 | 10 | MPL-2.0 |
| D21 ecosystem | 1 | |
| D22-D24 | 12,15 | covered |

## Appendix B. Capability mapping
| CAP-ID | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-08 | native | 02,03 | BL-28 partial | BUILD | P1 |
| CAP-11 | native | 02 | BL-01 (LPG) | EXPERIMENT | P3 |
| CAP-22 | native (functions) | 03 | BL-30 partial | EXPERIMENT | P2 |
| CAP-37 | unknown | - | BL-32 partial | DEFER | P3 |
| CAP-77 | MPL-2.0 | 01 | BL-22 | REFERENCE | P2 |

## Appendix C. Evidence records
| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-typedb-01 | 3.14.1 | MPL-2.0; release 2026-10-22; 4.5k stars | primary (API) | https://api.github.com/repos/typedb/typedb | 2026-10-26 | 0.85 | none |
| CLAIM-typedb-02 | README | Rust/RocksDB/gRPC; types, interfaces; Cloud/Enterprise/CE; TypeQL functions | vendor docs | https://github.com/typedb/typedb | 2026-10-26 | 0.8 | none |
| CLAIM-typedb-03 | 3.0 | Rust rewrite; functions replace rules; constraints; pipelines; no figures | vendor blog | https://typedb.com/blog/typedb-3-0-is-now-live | 2025-02-11 / 2026-10-26 | 0.75 | Wikipedia dates 3.0.0 to 2024-12-20 |

## Appendix D. Assumptions
Enterprise-only features and 2.x migration unknown; transaction semantics not verified.
