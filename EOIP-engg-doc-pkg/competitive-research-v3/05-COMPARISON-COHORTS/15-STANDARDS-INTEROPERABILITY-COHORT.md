# Cohort 15 — Standards and Interoperability

| Field | Value |
|---|---|
| Cohort ID | 15-STANDARDS-INTEROPERABILITY |
| Workload class | Specifications EOIP must emit, accept, validate or bridge: RDF/OWL/SHACL/SPARQL on the semantic side; openCypher/GQL/SQL-PGQ/PG-Schema on the property-graph side; ODRL/DPV for policy interchange; conformance suites (CAP-02, 08, 09, 10, 11, 14, 15, 16, 20, 29, 45, 46) |
| Members (deep dives) | [RDF](../04-COMPETITOR-DEEP-DIVES/C18-rdf.md), [OWL 2](../04-COMPETITOR-DEEP-DIVES/C18-owl2.md), [SHACL](../04-COMPETITOR-DEEP-DIVES/C18-shacl.md), [SPARQL](../04-COMPETITOR-DEEP-DIVES/C18-sparql.md), [openCypher](../04-COMPETITOR-DEEP-DIVES/C18-opencypher.md), [GQL](../04-COMPETITOR-DEEP-DIVES/C18-gql.md), [SQL/PGQ](../04-COMPETITOR-DEEP-DIVES/C18-sql-pgq.md), [PG-Schema](../04-COMPETITOR-DEEP-DIVES/C18-pg-schema.md), [ODRL / DPV](../04-COMPETITOR-DEEP-DIVES/C18-odrl-dpv.md) (9 of 9 exist) |
| Members (Tier C) | [C18-tier-c-records-V32](../04-COMPETITOR-DEEP-DIVES/C18-tier-c-records-V32.md): SKOS, DCAT 3 / schema.org, GraphQL, GraphAr / GraphML / GEXF, CSV / Parquet / Arrow, OpenAPI / AsyncAPI, NGSI-LD, GeoSPARQL / OWL-Time, CloudEvents, W3C Verifiable Credentials (10 records). [C20-tier-c-records-V33](../04-COMPETITOR-DEEP-DIVES/C20-tier-c-records-V33.md): W3C SHACL / JSON-LD / OWL test suites, plus RDF benchmarks (LUBM, BSBM, WatDiv, gMark) |
| Reference columns | HugeGraph, Neo4j, Neptune (support for each standard, from their deep dives) |
| EOIP baseline | BL-06, BL-06a, BL-09, BL-28, BL-29, BL-30, BL-31, BL-33, BL-58, BL-59 plus NB-09 ([01](../01-SYSTEM-BASELINE.md), [01a](../01a-BASELINE-DELTA-HEAD.md); HEAD status used) |
| Pending research | none |
| Date | 2026-10-26 |

## 1. Workload class and comparison basis

**Workloads.** (a) Export ontologies and graph slices to a customer's RDF/SHACL toolchain; (b) accept SPARQL or Cypher/GQL from customer tools; (c) validate data against shapes or graph types; (d) push EOIP query plans to Neo4j, Neptune, HugeGraph, Fuseki or a SQL engine; (e) exchange policy and privacy metadata.

**Why comparable.** Specifications are not products, so the basis is not feature parity but **status, semantics and bridgeability**. They are comparable on three axes: governance status (what you may legitimately call "supported"), the data model each assumes (RDF open-world triples versus labelled property graph with edge identity versus relational view), and whether a public conformance suite exists. Capability cells say what the standard specifies, not what an engine ships.

**Excluded.** Engine products (cohorts 01, 02); orchestration contracts (MCP, cohort 09). Tier C records are listed for context but not scored where their record is a single paragraph.

**Rule applied.** Syntactic resemblance implies no compatibility. Every C18 deep dive repeats this warning for `(a)-[:R]->(b)` versus a triple; this cohort treats it as a test-case design rule.

## 2. Status labels (what "supports X" may mean)

Status as verified 2026-10-26. Where a status rests on one catalogue, that is stated.

| Standard | Status label | Evidence | Note |
|---|---|---|---|
| RDF 1.1 and syntaxes | **W3C Recommendation** | [CLAIM-rdf-01](../04-COMPETITOR-DEEP-DIVES/C18-rdf.md) | |
| RDF 1.2 Concepts / Semantics | **Candidate Recommendation** (Snapshot 2026-04-07) | CLAIM-rdf-01 | triple terms (object position only), `rdf:reifies`, base direction |
| RDF 1.2 Turtle, TriG, N-Triples, N-Quads, XML | **Working Draft** (2026-10-23/25) | CLAIM-rdf-02 | parsers may diverge until CR/Rec |
| JSON-LD 1.1 | **Recommendation**; 1.2 chartered Jan 2026-Jan 2028, no draft verified | CLAIM-rdf-03 | |
| RDF-star | **Community Group Final Report**, not a standard | CLAIM-rdf-04 | superseded by 1.2 triple terms |
| OWL 2 (Structural, Direct, RDF-Based, Profiles) | **Recommendation** (2012), unchanged | [CLAIM-owl2-01](../04-COMPETITOR-DEEP-DIVES/C18-owl2.md) | RDF 1.2 Schema is **WD** (CLAIM-owl2-02) |
| SHACL 1.0 (Core + SPARQL) | **Recommendation** (2017) | [CLAIM-shacl-02](../04-COMPETITOR-DEEP-DIVES/C18-shacl.md) | SHACL-JS, rules: Working Group Note |
| SHACL 1.2 | **Working Draft / FPWD family** | CLAIM-shacl-01 | splits SPARQL out of Core; adds `sh:entailment`, reifier annotations |
| SPARQL 1.1 | **Recommendation** (2013) | [CLAIM-sparql-01](../04-COMPETITOR-DEEP-DIVES/C18-sparql.md) | |
| SPARQL 1.2 | **Working Draft** (all parts) | CLAIM-sparql-01, -02 | `VERSION` directive, triple-term functions |
| openCypher | **De facto specification** with TCK; **not** ISO/W3C; repo "unsupported" by Neo4j | [CLAIM-ocy-01](../04-COMPETITOR-DEEP-DIVES/C18-opencypher.md), CLAIM-ocy-02 | project mission now "evolve toward GQL" |
| Neo4j Cypher 5 / Cypher 25 | **Vendor dialect** | CLAIM-ocy-03 (0.6, search snippet) | Neptune and Memgraph subsets are separate dialects (CLAIM-ocy-01 section 1) |
| GQL (ISO/IEC 39075) | **Published ISO standard**, 1st ed. 2024, paywalled; Cor 1:2026 on one catalogue (0.6) | [CLAIM-gql-01](../04-COMPETITOR-DEEP-DIVES/C18-gql.md), CLAIM-gql-02 | ISO page returned 403, not read directly |
| SQL/PGQ (ISO/IEC 9075-16:2023) | **Published ISO standard**, 269 pages; next-edition CD listed | [CLAIM-pgq-01](../04-COMPETITOR-DEEP-DIVES/C18-sql-pgq.md), CLAIM-pgq-02 | PostgreSQL 19 implementation: RC1, GA planned 2026-11-19, so **not GA at access** (CLAIM-pgq-03, 0.65) |
| PG-Schema | **Peer-reviewed research proposal** (SIGMOD 2023) | [CLAIM-pgs-01](../04-COMPETITOR-DEEP-DIVES/C18-pg-schema.md) | no tooling, suite or WG found (negative, unverified) |
| ODRL 2.2 | **Recommendation** (2018); successor WG only a **draft charter** (start 2027-01-01) | [CLAIM-odrl-01, -02](../04-COMPETITOR-DEEP-DIVES/C18-odrl-dpv.md) | no normative evaluation semantics |
| DPV 2.3 | **Community Group output**, not a standard; DPV-ODRL guide a draft CG report | CLAIM-dpv-01, -02 | licence not read |

Tier C labels from V32: SKOS Rec 2009 (CLAIM-skos-01), DCAT 3 Rec 2024 (CLAIM-dcat-01), VC Data Model 2.0 Rec 2025 (CLAIM-vc-01), GeoSPARQL 1.1 OGC standard (CLAIM-geo-01), OWL-Time latest = CR Draft 2022 (CLAIM-geo-02), GraphQL foundation spec edition Sept 2025 (CLAIM-gql-api-01, note: ID differs from C18 `gql-*` series), GraphAr Apache **Incubator** (CLAIM-gf-01), GraphML / GEXF de facto (CLAIM-gf-02), NGSI-LD ETSI V1.8.1 with 1.9 draft (CLAIM-ngsi-01, 0.6).

**Usage rule for EOIP claims:** "RDF 1.2", "SPARQL 1.2" and "SHACL 1.2" may be described only as *draft-tracking experiments*; "GQL" as *ISO standard, EOIP emits no GQL*; "PG-Schema" as *research input*, not a standard.

## 3. Capability comparison

### 3.1 What each standard specifies

Cell values: **native** (in the normative text), **partial**, **absent** (specification does not cover it), **unknown**.

| CAP | RDF | OWL 2 | SHACL | SPARQL | openCypher | GQL | SQL/PGQ | PG-Schema | ODRL/DPV |
|---|---|---|---|---|---|---|---|---|---|
| CAP-02 RDF storage model | native (rdf-01) | native on RDF (owl2-01) | native (shapes are RDF; shacl-01) | native (sparql-01) | absent | absent | absent | absent | native (vocabularies; odrl-01) |
| CAP-08 schema / constraints | absent | absent (infers, not rejects) | native for RDF; Core Rec (shacl-02) | absent | absent (vendor DDL; ocy-01) | partial: limited graph types in 1st ed. (gql-03) | partial: relational DDL under the graph view (pgq-03) | native in proposal (pgs-01) | absent |
| CAP-09 ontology RDFS/OWL | RDFS via Schema (WD in 1.2; owl2-02) | native (owl2-01) | absent | partial via entailment regimes (sparql-01) | absent (no entailment; ocy-01) | absent (no entailment; gql-01) | absent | absent | partial: DPV concept hierarchies, subsumption only (dpv-01) |
| CAP-10 shape validation | absent | absent | native (shacl-01/02) | partial via SHACL-SPARQL | absent | absent | absent | native in proposal (pgs-01) | absent |
| CAP-11 edge properties / reification | partial: reifier + triple terms in 1.2 CR (rdf-01) | absent | partial: reifier annotations in 1.2 WD (shacl-03) | partial: 1.2 WD annotation syntax (rdf-05, sparql-04) | native (relationship properties; ocy-01) | native (edge identity, parallel edges; gql-01) | partial: edge-table columns only (pgq-03) | native in proposal (edge types; pgs-01) | absent |
| CAP-14 Cypher / GQL | absent | absent | absent | absent | native de facto | native ISO | partial: shared pattern language (0.7, from prior knowledge; gql-01 section 3) | absent | absent |
| CAP-15 SPARQL | absent | absent | partial | native 1.1 Rec; 1.2 WD | absent | absent | absent | absent | absent |
| CAP-16 SQL / PGQ | absent | absent | absent | absent | absent | absent | native (pgq-01) | absent | absent |
| CAP-19 paths | partial: none | absent | absent | partial: property paths return endpoints, no path objects (sparql-04) | native (variable-length; ocy-01) | native: WALK/TRAIL/ACYCLIC/SIMPLE and shortest selectors (0.7; gql-01) | partial: lacks variable-length in the PG19 first implementation (pgq-03) | absent | absent |
| CAP-23 OWL profile reasoning | absent | native EL/QL/RL/DL; complexity per profile (owl2-03) | absent (`sh:entailment` in WD only) | partial: entailment regimes optional | absent | absent | absent | absent | absent |
| CAP-45/46 policy / ACL | absent | absent | absent | absent | absent | absent | partial: via RLS in PostgreSQL (pgq-03, inference) | absent | partial: vocabulary only, **no enforcement** (odrl-01, dpv-01) |

### 3.2 Reference engines and EOIP

| Standard | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|
| RDF / SPARQL 1.1 | absent: no SPARQL / RDF / SHACL / OWL / GQL / SQL-PGQ module in 1.7.0 tree (reasoned 0.7; C01-apache-hugegraph.md section 3 standards row) | plugin: n10s is Labs, "not part of Neo4j's supported product lineup", Apache-2.0 ([CLAIM-neo4j-31](../04-COMPETITOR-DEEP-DIVES/C01-neo4j.md)) | native: SPARQL 1.1 Query and Update, `SERVICE`; no entailment regime listed; RDF isolated from property-graph data ([CLAIM-amazon-neptune-06](../04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md), -26) | BL-06 Implemented (Fuseki/GraphDB over SPARQL 1.1, live tests skipped without env); BL-06a library-only, not mounted (01a) |
| openCypher / Cypher | partial (CAP-14, CLAIM-11/-12 in C01-apache-hugegraph.md) | native Cypher 5 and Cypher 25 ([CLAIM-neo4j-07](../04-COMPETITOR-DEEP-DIVES/C01-neo4j.md)) | native with deviations: Cypher 9 baseline, no `shortestPath`, no `CALL..YIELD`, no UDF ([CLAIM-amazon-neptune-04](../04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md)) | BL-03/04 HTTP adapters; BL-09 `ast_compiler` emits text, nothing executes it on Neo4j (01a) |
| Gremlin | native (CLAIM-06, -21) | absent | native with deviations (CLAIM-amazon-neptune-03) | BL-02/04/05 adapters; live-unverified |
| GQL / SQL-PGQ | absent (same row as above) | partial GQL: "majority of mandatory features", five areas missing ([CLAIM-neo4j-08](../04-COMPETITOR-DEEP-DIVES/C01-neo4j.md)) | absent: no GQL, SQL/PGQ ([CLAIM-amazon-neptune-12](../04-COMPETITOR-DEEP-DIVES/C01-amazon-neptune.md)) | BL-59 Partial, library-only; emits no GQL / `GRAPH_TABLE` |
| Schema / constraints | native strict schema (CLAIM-13) | partial (CE); GRAPH TYPE enterprise-only, open semantics ([CLAIM-neo4j-22, -23](../04-COMPETITOR-DEEP-DIVES/C01-neo4j.md)) | absent beyond ID uniqueness (CLAIM-amazon-neptune-12) | BL-28 label / required-property gate; BL-29 Partial |
| SHACL / OWL | absent (reasoned) | plugin n10s: SHACL covers "a significant portion but not all" (CLAIM-neo4j-32) | absent: no reasoner documented (CLAIM-amazon-neptune-06) | BL-29 Partial (pySHACL differential test passes at HEAD); BL-30 Partial with canned Openllet/HermiT/Jena adapters (01a, do not cite as capability) |
| JSON-LD / mapping | n/a | n/a | n/a | BL-31 Implemented with loss accounting; BL-33 Implemented, R2RML partial, not conformance-tested (NB-09) |

## 4. Semantics differences and bridging loss

This is the core of the cohort. Each row is a property of the specifications, taken from the C18 deep dives; none is measured on EOIP.

| Dimension | RDF / OWL / SHACL / SPARQL | openCypher / GQL / PG-Schema | SQL/PGQ | Loss when bridging |
|---|---|---|---|---|
| Identity | IRIs; merge by union; blank nodes existential (rdf-01) | node and edge identity, parallel edges allowed (gql-01, ocy-01) | primary key of base table (pgq-03) | LPG parallel edges collapse to one triple unless an edge IRI is minted; blank-node scope has no LPG form |
| World assumption | open, monotonic, no unique-name (owl2-03) | closed when a type is declared; `null` 3VL (ocy-01) | closed relational (pgq-03) | OWL `domain/range` becomes a rejection or nothing in LPG; existential restrictions have no LPG form (owl2 section 11) |
| Edge properties | reifier or triple term in 1.2 CR; 3-4x triples when reified (rdf section 9) | native on relationship | edge-table columns | RDF-star-looking syntax is not edge-property semantics (rdf section 11) |
| Absence | unbound variable in OPTIONAL | `null` | SQL NULL | SPARQL unbound is not an LPG null (sparql section 11) |
| Path semantics | property paths return endpoints; `*`/`+` use distinct-endpoint semantics (sparql-04) | trail / acyclic / simple; NP-hard in general (ocy, gql) | recursive CTE / operator | GQL path modes have no SPARQL equivalent (gql section 11) |
| Multiplicity | set semantics for graphs; **bag** semantics for solutions | bags | bags | no guarantee that Cypher and SPARQL translations of one plan return equal answers (sparql section 11) |
| Typing | classes with inference; `rdf:type` | labels (sets), no hierarchy | table / label expressions | multi-label to multi-type loses hierarchy (gql section 11) |
| Constraints | SHACL: closed-world check on a given graph, no entailment unless materialised (shacl section 5) | PG-Schema / GQL graph type: constrain and reject | DDL | SHACL validates the *projection*, not LPG-native edge identity (shacl section 11); ontology to PG-Schema loses OWL restrictions and disjointness inference (pg-schema section 11) |
| Policy | ODRL: open-world, no default-deny, no evaluation semantics (odrl section 5) | EOIP authz: deny-by-default | RLS | ODRL import loses duties, `odrl:conflict` and refinements; export needs explicit prohibitions to preserve deny-by-default (odrl section 11) |

**EOIP specific.** BL-06 states the LPG-shaped `GraphStore` over SPARQL cannot express RDF-only constructs and "semantic loss of LPG to RDF mapping still unmeasured" (01a). That claim is not tested anywhere in the evidence reviewed; this cohort cannot say how much is lost, only which classes of construct are lost by specification.

## 5. Conformance suites

| Standard | Public suite | Evidence | EOIP status |
|---|---|---|---|
| SHACL 1.0 | W3C data-shapes suite, 121 validation tests, EARL results, `sht:partial` (V33 record `shacl-02`, 0.85) | V33 | **Not run** (U-07 in 01a: pyshacl differential test passes locally, W3C suite not run); in-house validator rejects unsupported components |
| OWL 2 | W3C OWL 2 conformance (profile identification, entailment, consistency; V33 `owl-01`, 0.85) | V33 | not run; BL-30 reasoner adapters partly canned |
| JSON-LD | `w3c/json-ld-api` tests (date and licence not read; V33) | V33 | BL-31 round-trip uses rdflib as oracle (`test_rdf_fidelity.py` passes, 01a); W3C suite not run |
| RDF / SPARQL | `w3c/rdf-tests` jointly managed by CG and WG ([CLAIM-rdf-06](../04-COMPETITOR-DEEP-DIVES/C18-rdf.md)) | C18 | independent result corpus on rdflib and CI Fuseki job (commit 099eb38); W3C test manifests not stated as run |
| openCypher | TCK (Cucumber features, `/tck`; Maven listing 2024.2, last July 2025, snippet 0.5; CLAIM-ocy-01, -04) | C18 | not run; no engine executes `ast_compiler` output (01a) |
| GQL | **no public conformance suite verified** (gql section 3) | C18 | n/a |
| SQL/PGQ | **no public suite verified** (pgq section 3) | C18 | n/a |
| PG-Schema | **none found** (pgs section 3) | C18 | n/a |
| ODRL / DPV | none verified (odrl section 3: "no normative evaluation semantics") | C18 | n/a |
| RDF/OWL performance | LUBM (14 SPARQL 1.0 queries), WatDiv v0.6, gMark MIT; BSBM page unreachable (V33; `rdf-01..03` in V33) | V33 | not run; V33 labels them REFERENCE-ONLY |

Evidence note: V33 reuses claim IDs `shacl-01`, `shacl-02`, `rdf-01..03` for different facts than the C18 deep dives (`CLAIM-shacl-01` is the SHACL 1.2 family; V33 `shacl-01` is the 2017 Rec and suite URL; `CLAIM-rdf-01` is RDF 1.2 CR while V33 `rdf-01` is LUBM). Cite with the file name to avoid ambiguity.

## 6. Operational and licensing view

| Item | Finding | Evidence |
|---|---|---|
| Specification access | GQL and SQL/PGQ are **paywalled**; W3C specs royalty-free per policy (not re-read) | gql-01, pgq-01; owl2 / rdf section 10 |
| Patents | ISO declarations for GQL / PGQ not checked; PG-Schema authors from Neo4j, AWS, Google, no claim verified | gql section 10, pgs section 10 (legal-review triggers, no conclusion) |
| Reasoners | HermiT LGPL, Openllet/Pellet-family AGPL or commercial, ELK Apache-2.0: prior knowledge, 0.6, **verify**; AGPL is a hard exclusion for EOIP | owl2 section 9 |
| Libraries | rdflib BSD-3 (0.6 from rdf/sparql deep dives; BSD in 01a U-12), pySHACL Apache-2.0 (0.6), Jena Apache-2.0 | rdf/shacl section 10 |
| Neo4j | Community GPLv3 / Enterprise commercial: prior knowledge in the openCypher deep dive; GRAPH TYPE and existence / type / key constraints are enterprise-only | ocy section 10; CLAIM-neo4j-22, -23 |
| Air-gap | all specifications usable offline; JSON-LD remote contexts break air-gap (SSRF risk) unless bundled; VC verification may need network for DID and status lists | rdf section 7/10; V32 `vc-01` record |

## 7. Performance evidence

None attributable. The C18 deep dives explicitly record "not specified by the standard / no numbers claimed" for RDF, OWL, SHACL, SPARQL, openCypher, GQL and SQL/PGQ. The only complexity facts are theoretical: OWL 2 EL PTIME-complete, QL NLogSpace taxonomic with AC0 data, RL PTIME consistency (CLAIM-owl2-03, Recommendation text); DL N2EXPTIME combined (0.7, literature, not re-fetched). SPARQL PSPACE-complete combined (0.7, literature). Trail / simple-path semantics are NP-hard in general (GQL and openCypher deep dives). PostgreSQL 19 implements `GRAPH_TABLE` as a join rewriter, "not a graph storage engine" (CLAIM-pgq-03, 0.65), so relational optimiser behaviour governs depth. No engine-level comparison exists in these sources; the LDBC and V33 benchmark records are the route to produce one.

## 8. Findings

1. **Only four of the nine members are final standards today for the semantic side**: RDF 1.1, OWL 2, SHACL 1.0, SPARQL 1.1. RDF 1.2 is CR; its syntaxes, SPARQL 1.2 and SHACL 1.2 are drafts (CLAIM-rdf-01/02, sparql-01, shacl-01). Falsifiable by any later W3C publication.
2. **The property-graph side has two ISO standards but no public conformance suites**, while openCypher has a TCK but no standard status (CLAIM-gql-01, pgq-01, ocy-01; "NOT PUBLICLY VERIFIED"). "GQL-compatible" and "SQL/PGQ-compatible" are therefore unverifiable claims for any vendor, including EOIP.
3. **PG-Schema is not a standard** and has no tooling or suite found (CLAIM-pgs-01); it should be an input to EOIP's graph-type IR, not a compliance target.
4. **No evidence supports a lossless bridge between RDF and LPG.** Every C18 deep dive lists constructs with no counterpart (parallel edges, blank-node scope, path modes, OWL restrictions). Falsifiable by a round-trip experiment that measures zero loss on a defined corpus; none exists in the evidence.
5. **EOIP's strongest standards asset is its loss-accounted JSON-LD and its SPARQL execution layer**, not a SPARQL endpoint: BL-31 Implemented; BL-06a with algebra-walk rejection of updates, `SERVICE` and unbounded paths is described as stronger than raw endpoint exposure (sparql section 11, 01a), but it is not mounted on any route.
6. **EOIP has no GQL or SQL/PGQ emitter**, and `ast_compiler` targets Cypher, Gremlin and SPARQL only (BL-59, 01a). Among reference engines Neo4j has partial GQL (CLAIM-neo4j-08), Neptune none (CLAIM-amazon-neptune-12), HugeGraph none (reasoned). A GQL emitter would therefore have no verified production target today other than Neo4j partial.
7. **SHACL conformance can be claimed only after the W3C suite runs.** The suite exists with 121 tests (V33 `shacl-02`); EOIP has run none (U-07). Until then public wording must say "SHACL Core subset, differential-tested against pySHACL".
8. **ODRL and DPV are vocabularies, not enforcement.** ODRL 2.2 has no normative evaluation semantics, no successor WG is chartered, and DPV is not a standard (CLAIM-odrl-02, dpv-01). They can label exports (CAP-33 mapping to DPV) but cannot replace EOIP's source-ACL enforcement, itself still Partial (BL-18).
9. **SQL/PGQ is unusual among members in being a view over relational tables**, which is attractive for one-node PostgreSQL substrates and RLS (pgq section 8), but PG19 was not GA at access and lacks variable-length paths (CLAIM-pgq-03).
10. **Evidence conflict worth resolving:** the C18 openCypher deep dive says Neo4j 2026.02 made Cypher 25 default for new organisations (CLAIM-ocy-03, 0.6, snippet only); the Neo4j deep dive records GRAPH TYPE GA in 2026.06 and Cypher 5 "frozen" (CLAIM-neo4j-07). The two are not contradictory but the 2026.02 page was never fetched.

## 9. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-02 / BL-06 | STR-rdf (standard-compliant I/O via rdflib/Jena; no own triplestore) | semantic loss unmeasured | **INTEGRATE** (REUSE of rdflib/Fuseki/GraphDB); **EXPERIMENT** loss-measurement harness | LPG-over-RDF contract has no measured loss budget; RDF 1.2 triple terms unsupported (BL-33) |
| CAP-15 / BL-06a | STR-sparql (algebra-level validation) | EOIP ahead on policy-checked execution | **REUSE** engines; **BUILD** mount with tenant / ACL predicates | `SparqlProtocolHandler` not mounted (01a) |
| CAP-20 / BL-09 | typed IR with documented loss per dialect | Neptune deviations (no `CALL`, no `shortestPath`) prove dialect profiles are needed (CLAIM-amazon-neptune-04) | **BUILD** | No equivalence testing between Cypher and SPARQL outputs of the same plan |
| CAP-14 GQL | emitter when two backends support it | none | **DEFER** emitter; **INTEGRATE** Cypher dialects now | Only Neo4j partial GQL (CLAIM-neo4j-08) |
| CAP-16 SQL/PGQ | `GRAPH_TABLE` emitter | PG19 not GA | **EXPERIMENT** after GA, with PostgreSQL RLS for CAP-47 | BL-01 `GraphStore` has no SQL backend; BL-59 no `GRAPH_TABLE` |
| CAP-10 / BL-29 | run W3C SHACL suite in CI; publish EARL report | in-house validator tenant-safe core | **INTEGRATE** pySHACL as oracle + **BUILD** in-house core (as in deep dive) | W3C suite not run; pySHACL not in runtime image |
| CAP-23 / BL-30 | declared profile (EL / RL) with explanation | Openllet / HermiT / Jena adapters are canned | **INTEGRATE** ELK optional (licence gated); **REJECT** AGPL reasoners | No OWL profile engine executes (01a); mark as "available upstream, not integrated" |
| CAP-08 | graph-type IR aligned with GQL / PG-Schema | Neptune has no constraints; Neo4j GRAPH TYPE enterprise-only, open | **BUILD** own IR; compile to Neo4j GRAPH TYPE and SHACL | No LPG schema language with edge-endpoint typing (BL-28) |
| CAP-11 | RDF 1.2 triple terms behind a flag | RDF-star is not a standard | **EXPERIMENT** | no RDF 1.2 support; do not claim |
| CAP-45/46 / BL-18 | ODRL import to ABAC IR, DPV tags on export | ODRL has no enforcement | **EXPERIMENT** import; **BUILD** ACL enforcement independent of ODRL | source ACL not enforced end to end (BL-18) |
| Tier C | SKOS REUSE, DCAT 3 REUSE, GraphML / GEXF REUSE, Arrow / Parquet REUSE, CloudEvents REUSE, VC EXPERIMENT, GraphQL EXPERIMENT (BL-58 library-only), OWL-Time EXPERIMENT, GraphAr / GeoSPARQL / NGSI-LD REFERENCE-ONLY (V32 per-record decisions) | | per V32 | |

## 10. Open questions

1. How much does the BL-06 LPG-to-RDF mapping lose on a defined corpus (parallel edges, language tags, named graphs)? Needs a harness before any "lossless" wording.
2. Which reasoner licences are final? HermiT, Openllet and ELK terms are 0.6 prior knowledge (OWL 2 section 9).
3. Is the ISO GQL Cor 1:2026 real? One catalogue only (CLAIM-gql-02, 0.6). Is a GQL conformance programme planned?
4. When does PostgreSQL 19 reach GA (planned 2026-11-19) and does a later release add variable-length paths?
5. Does the W3C SHACL suite pass on the EOIP in-house validator and on `PySHACLAdapter`; what are `sht:partial` outcomes?
6. Will the draft Digital Policy WG charter (start 2027-01-01) produce evaluation semantics for ODRL?
7. ODRL / DPV, DPV licence and openCypher TCK cadence need confirmation (all unread or snippet-based).
8. What is the DPV 2.3 date? The GitHub page shows no year (CLAIM-dpv-01, 0.7).
