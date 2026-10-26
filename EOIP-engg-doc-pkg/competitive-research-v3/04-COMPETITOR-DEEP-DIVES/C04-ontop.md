# C04 — Ontop (virtual knowledge graphs / OBDA over relational databases)

| Field | Value |
|---|---|
| Registry ID | T-C04-ontop |
| Tier | A — leading OBDA / virtual-KG engine; Apache-2.0; seed inversion target (Master Prompt §10.5, "Ontop / OBDA: virtual graphs are read-mostly and mapping-heavy") |
| Versions examined | Ontop 5.5.0 (2026-02-14, tag `ontop-5.5.0`, latest found), 5.4.0 (2025-09-29), 5.3.1 (2025-09-29), 5.3.0 (2025-02-18), 5.2.0 (2024-08-16), 5.0.0 (2022-12-31) |
| Verified on | 2026-10-26 (actual access date; brief says 2026-10-18 — see Appendix D) |
| Worker | W12 (batch V02) |

## 1. Identity, current status, tier, and sources

**Identity.** Ontop is an open-source Virtual Knowledge Graph (VKG) system: it presents relational data as an RDF graph and answers SPARQL by translating it to SQL over the live sources using R2RML or Ontop's own mapping language plus an RDFS / OWL 2 QL ontology. It also has a `materialize` mode that dumps the same virtual graph to RDF files. [CLAIM-ontop-01] [CLAIM-ontop-05] Developed with the Free University of Bozen-Bolzano and the spin-off Ontopic s.r.l., with contributions from Birkbeck and Southeast University. [CLAIM-ontop-01]

**Licence.** Apache-2.0 for code (GitHub SPDX and README); documentation CC BY 4.0; contributor licence agreement files sit in the repo `documentation/` folder. [CLAIM-ontop-02]

**Status.** Active but slow cadence: 5.5.0 on 2026-02-14 is the latest tag; last push 2026-10-15; no release since (about 8 months). Releases: 5.0.0 Dec 2022, 5.1.0 Aug 2023, 5.2.0 Aug 2024, 5.3.0 Feb 2025, 5.4.0 Sep 2025, 5.5.0 Feb 2026. [CLAIM-ontop-02] [CLAIM-ontop-03] Commercial support is offered by Ontopic (Ontopic Studio / Ontopic Suite, built on Ontop; Docker-compose, Kubernetes, Windows desktop, AWS Marketplace). A LinkedIn post says Ontopic was acquired by Digital Science (metaphactory owner); no primary announcement found, so UNVERIFIED. [CLAIM-ontop-09]

**Traps.** "Ontop" is also the engine inside GraphDB's virtual repositories (Ontotext joined the project for GraphDB 9.5, 2020) — same code family, separate packaging; see `C02-ontotext-graphdb.md`. [CLAIM-ontop-10] Ontop does not implement RDF 1.2 / SPARQL 1.2 (RDF 1.1 data model); RDF-star appears only as a 2022 MSc thesis on the project site, not in release notes. [CLAIM-ontop-01] [CLAIM-ontop-03]

**Sources (10):** ontop-vkg.org guide, release notes, CLI page, support page; GitHub repository, releases API and tags; source at tag `ontop-5.5.0` (shallow clone: `core`, `engine`, `mapping`, `db`, `client`); GraphDB 9.5 press release; Ontopic site and docs; Ontop SWJ literature (not fetched).

## 2. Primary problem, target workloads, concrete example workflows

Give a semantic, ontology-level view over existing relational (and SQL-federated) sources without copying data, for ad-hoc and application SPARQL, data integration and consistent vocabularies. [CLAIM-ontop-01] Typical customers: public-sector and industry data catalogues over Postgres/Oracle/SQL Server/Snowflake/Databricks.

EOIP-relevant workflows: (1) A ServiceNow CMDB replica in Postgres exposed as a VKG with the EOIP ontology; the NL-suggestion layer (BL-11) emits a SPARQL query and the user sees live rows. (2) Nightly `ontop materialize --separate-files` per class into RDF files that an EOIP connector ingests as SourceEvents, so the authoritative graph stays governed (constraint 4 in Master Prompt §4.3). (3) `ontop bootstrap` proposes an ontology and mappings from a database schema, feeding BL-27 ontology proposals. [CLAIM-ontop-05]

## 3. Feature inventory

| Feature | Status | CLAIM |
|---|---|---|
| SPARQL 1.1 query (most of it) + GeoSPARQL functions; SPARQL endpoint; predefined-query endpoint (beta) | present | 01 |
| SPARQL Update / writes through the VKG | not documented in pages read: UNVERIFIED (design is read-only) | 01 |
| R2RML and Ontop native `.obda` mappings; converters `to-obda`, `to-r2rml`, `pretty-r2rml` | present | 05 |
| SPARQL rules extending the VKG; `FROM` / `FROM NAMED` (5.0) | present | 03 |
| Lenses (virtual views incl. flatten and union lenses, beta) | present, renamed from "views" in 5.0 | 03 |
| OWL 2 QL / RDFS reasoning by rewriting + mapping saturation | present | 01, 06 |
| `rdfs:subClassOf*` property path (5.4) | present | 03 |
| `materialize` to RDF/XML, Turtle, N-Triples, N-Quads, TriG, JSON-LD; streaming, gzip/zip, per-class files | present | 05 |
| `bootstrap` ontology + mapping from DB schema; `extract-db-metadata`; `validate` | present | 05 |
| Protégé plugin (mapping editor + SPARQL tester) | present (bundles embed JRE 11) | 01, 03 |
| Databases: PostgreSQL, MySQL/MariaDB, Oracle, SQL Server, DB2, H2, DuckDB, Snowflake, Databricks/Spark SQL, BigQuery, Athena, Redshift, Trino/Presto, Dremio, Denodo, Teiid, TDEngine, MS Access | present at differing maturity (dialect providers visible in `db/rdb`) | 01, 03, 06 |
| DynamoDB via CData | beta | 03 |
| User/HTTP-header info for SQL functions and query logs (5.2.0) | present | 03 |
| Authorization / row-level security / ACL | absent (delegated to the DB account) | — |
| Mapping versioning, diff, review workflow | absent in OSS (Ontopic Studio: UNVERIFIED) | — |
| Vector search, LLM features, graph algorithms | absent | — |
| Property-graph (Cypher/Gremlin) interface | absent | — |
| Result/plan caching | partial: query cache class `GuiceBasedQueryCache` exists; semantics UNVERIFIED | 06 |

## 4. Architecture diagram

```
 SPARQL client / Protégé / CLI `ontop query`            mapping files (R2RML | .obda | lenses)
        │                                                 ontology (OWL 2 QL / RDFS)
        ▼                                                 DB metadata (JDBC or JSON export)
 ┌──────────────────────── Ontop engine (JVM, Java 11+) ───────────────────────────┐
 │ LOAD TIME:  parse mappings ─► apply lenses ─► T-mapping saturation (ontology     │
 │             hierarchy compiled into mappings) ─► mapping optimisation (constraints)│
 │ QUERY TIME: SPARQL (RDF4J 5.1.4 parser) ─► internal IQ ─► [existential rewriting │
 │             TreeWitnessRewriter] ─► unfolding (Basic / TwoPhase) ─► IQ optimiser │
 │             (joins, left joins, unions, filters, flatten, aggregation)            │
 │             ─► native SQL per dialect ─► JDBC ─► RDF term construction             │
 └──────────────┬────────────────────────────────────────────────┬─────────────────┘
                ▼ read path (virtual)                              ▼ batch path
        relational sources (live, DB creds)               `materialize` ► RDF files
 Control plane: config properties, mapping files.  State: none persistent (stateless).
```

## 5. Under-the-hood reconstruction

Source at tag `ontop-5.5.0` (modules `core/{model,obda,optimization,kg-query}`, `mapping/{core,sql,owlapi}`, `db/rdb`, `engine/{reformulation,system}`, `client/{cli,endpoint}`); `jdk.version` = 11, RDF4J 5.1.4, OWLAPI 5.5.1 in the root `pom.xml`. [CLAIM-ontop-04]

**Data model.** Virtual RDF 1.1 graph defined by mapping assertions `SQL source query → RDF template`. R2RML triples-maps are converted to an internal mapping form; lenses define virtual relations over base tables (flatten for arrays/JSON, union). Subject IRIs are built from templates over key columns, which lets the unfolder join on keys and drop self-joins. [CLAIM-ontop-05]

**Load-time compilation (mapping saturation).** `TMappingSaturatorImpl` (`mapping/core/.../transformer/impl`) takes the OWL 2 QL class/property hierarchy and extends mapping assertions so that a query for a superclass is answered by the union of its sub-class mappings — the classic *T-mapping* technique (name-level inference; the source shows the component and its tests `TMappingUOBMShortTest`, `TMappingDisablingTest`; the technique description is from OBDA literature, *inference*). It can be disabled by configuration. Existential axioms that cannot be pushed into mappings are handled at query time by `TreeWitnessRewriter` (445 lines, `engine/reformulation/.../rewriting/impl`) via `ExistentialQueryRewriter`. [CLAIM-ontop-06]

**Query pipeline.**

```
q   = parse(SPARQL)                       # RDF4J
iq  = toIQ(q)                             # intermediate query tree
iq' = rewriteExistentials(iq, ontology)   # TreeWitnessRewriter; identity when no existential axioms
iq''= unfold(iq', saturatedMappings)      # Basic or TwoPhaseQueryUnfolder (5.4 added the two-phase unfolder)
iq3 = optimise(iq'', dbConstraints)       # core/optimization: self-join elimination, left-join, union/binding lifting, filter lifting...
sql = serialise(iq3, dialect)             # db/rdb dialect providers; CTEs supported since 5.5
rows→ RDF terms (datatype casts, IRI templates), stream to client
```

**Constraints exploitation.** Unique/primary/foreign keys from JDBC metadata (or `extract-db-metadata` JSON, or declared on lenses) drive join simplification; 5.3.0 added "unique constraint inference and strict dependents" optimisations. [CLAIM-ontop-03] Cost-based planning is **not** done by Ontop: it emits SQL and relies on the source DBMS optimiser (*inference from architecture*, no statistics component seen).

**Materialisation.** `DefaultOntopRDFMaterializer` iterates mapping assertions (per class/property with `--separate-files`), streams SQL results, supports compression since 5.2.0. [CLAIM-ontop-05]

**Concurrency/transactions.** Read-only queries on JDBC connections; isolation and freshness are whatever the source DBMS provides; there is no write path, snapshot pinning, or consistent multi-source read. **Security.** Authentication to sources via JDBC credentials in properties; since 5.2.0 user info from HTTP headers reaches SQL functions and logs — a hook for audit and policy, not an ACL model. [CLAIM-ontop-03] **Versioning.** Mapping files are text and git-friendly; Ontop itself has no version model.

## 6. Functional and non-functional requirements inferred

| ID | Requirement for an EOIP virtual/hybrid source layer |
|---|---|
| FR-1 | Declarative mappings (R2RML-compatible) with validation before activation |
| FR-2 | SPARQL → SQL translation with sound handling of NULL, bag/set semantics, datatypes |
| FR-3 | Ontology-aware answering for subclass/subproperty by mapping saturation |
| FR-4 | Materialisation of the same mappings to events (not direct graph writes) |
| FR-5 | Per-request identity propagated to the source (permissions survive) |
| NFR-1 | Java 11+ JVM sidecar; JDBC drivers supplied by operator |
| NFR-2 | Freshness stated per source (live vs snapshot); partial-source degradation |
| NFR-3 | Latency governed by source DB indexes; no hidden full scans |

## 7. Performance and resource model

No independent benchmark was retrieved in this pass (published OBDA benchmarks such as NPD and BSBM exist in the Ontop papers; not fetched, UNVERIFIED). Project statements: queries become "highly optimised SQL" (qualitative). Scaling follows the source DBMS: Ontop is stateless, so memory is dominated by mapping size, ontology classification and result streaming; large unions caused by T-mapping saturation (hierarchy depth × mapping count) and many left joins are the known cost drivers (*hypothesis*, supported by the dedicated unfolder and optimiser work in 5.2.0–5.4.0 release notes). `--no-streaming` materialisation holds all SQL results in memory and is discouraged. [CLAIM-ontop-05] Failure modes: unbounded property paths, non-indexed join keys, dialect function gaps, JDBC driver quirks (release notes list many per-database fixes). [CLAIM-ontop-03]

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match or exceed |
|---|---|---|
| S1 | Zero-copy semantic access, always fresh | Integrate Ontop; exceed with governance and ACLs |
| S2 | Mature SPARQL→SQL optimiser exploiting constraints | Reuse, do not rebuild |
| S3 | R2RML standard mappings + converters + Protégé editor | Reuse; export EOIP CML to R2RML |
| S4 | Broad SQL dialect coverage (Snowflake, Databricks, DuckDB, Trino…) | Reuse |
| S5 | `bootstrap` from schema | Match with BL-26 profiler; compare output |
| S6 | Materialisation of the same mappings (hybrid in one tool) | Wrap as a governed batch source |
| S7 | Apache-2.0, redistributable | Fits white-label |

## 9. Limitations with root causes

| Type | Limitation | Root cause |
|---|---|---|
| Intentional trade-off | Read-only virtual graph; traversal cost = SQL join cost | Query rewriting over relational sources [CLAIM-ontop-01,06] |
| Algorithmic dead-end | Deep multi-hop and transitive queries become large SQL unions/self-joins; `rdfs:subClassOf*` supported only recently (5.4) | Relational execution of graph patterns |
| Operational | JVM + JDBC drivers; per-DB dialect fixes every release | Platform; heterogeneity [CLAIM-ontop-03] |
| User friction | Mappings are required and hand-authored; ontology must be OWL 2 QL | Method; bootstrap gives only a starting point |
| Semantics | RDF 1.1 only; no RDF-star/1.2; no property-graph view | Data model [CLAIM-ontop-01] |
| Security | No ACL model; permissions = DB account unless per-user credentials | Not a goal |
| Governance | No mapping diff/versioning/review in OSS | Not a goal |
| Maturity/ownership | Release cadence ~6 months; Ontopic commercial packaging; ownership change unverified | Vendor structure |

## 10. Deployment, licensing, redistribution, operational viability

Apache-2.0: embedding, OEM and redistribution permitted with notices (class: **permissive**; no legal conclusion). Distribution forms: CLI zip, Docker image `ontop/ontop` (ARM64 since 5.0), endpoint, Protégé bundles. Third-party JDBC drivers (Oracle, DB2, SQL Server) have their own licences and are supplied by the user (not bundled: UNVERIFIED; `licenses/` folder exists). Air-gap: yes (no cloud dependency identified); one-node: yes (stateless JVM). Commercial: Ontopic Suite/Studio under separate terms, not researched. Legal-review triggers: CLA obligations on contributions; dependency licences (RDF4J, OWLAPI); any bundled JDBC drivers.

## 11. Competitive delta against the EOIP verified baseline

| Area | EOIP | Ontop | Delta |
|---|---|---|---|
| BL-33 mapping language | CML → engine-neutral IR → LPG/RDF + PROV-O; not R2RML-conformant | R2RML + `.obda`, converters | Parity via R2RML export/import; EOIP lacks conformance |
| `mapping/r2rml.py` (162 lines) | Adapter with loss report; unsupported constructs tracked | Full R2RML | Partial |
| BL-51 federation / virtual planner | `federation/planner.py`, `federation/obda.py` (226 lines) = freshness, pushdown fragments, partial-source degradation as contracts; `mapping/virtualization.py:59-74` `rewrite_point_query` builds `SELECT … WHERE id = '{entity_id}'` by string interpolation and `execute_point_query_mock` runs against a Python dict; the docstring claims "SQL pushdown < 50 ms" for a mock. [CLAIM-ontop-07] | Real SPARQL→SQL unfolder/optimiser | EOIP has no real OBDA engine; the point-query path is injectable if ever wired to SQL |
| BL-26 profiler / BL-27 ontology proposal | Implemented / Partial | `bootstrap` | Compare outputs; complementary |
| BL-23 connectors never mutate graph | Implemented | `materialize` emits files | Fit: wrap as SourceEvent source |
| BL-18/20 ACL, tenancy | Absent / contract | DB-account only | Both need work; per-user DB credentials are the clean lever |
| BL-37 bitemporal | Implemented | none | EOIP ahead |
| BL-08 typed bounded queries | Implemented | SPARQL free-form | Keep typed plans as the front door; compile selected plans to SPARQL for Ontop |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

| STR-ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-ontop-01 | Ontop | Virtual KG, zero copy, live | 01 | Fresh answers for volatile sources (CMDB, tickets) | integrate | Ontop sidecar behind an adapter, read-only role per tenant | SPARQL answer equals SQL ground truth on 20 queries; no rows copied |
| STR-ontop-02 | Ontop | Mapping saturation for class hierarchies | 06 | Ontology-aware answers without reasoner | reuse | Ship EOIP ontology as OWL 2 QL profile subset; lint against QL | Subclass query returns union of sub-class sources |
| STR-ontop-03 | Ontop | R2RML + converters | 05 | Standard mapping interchange | match | CML ⇄ R2RML round trip with loss report (extends `mapping/r2rml.py`) | W3C R2RML test cases pass rate published |
| STR-ontop-04 | Ontop | Materialise from same mappings | 05 | One mapping, two execution modes | integrate | Materialised output enters as versioned SourceEvents | Idempotent replay yields identical graph hash |
| STR-ontop-05 | Ontop | Constraint-driven SQL simplification | 03,06 | Fast point/join queries | reuse | Feed FK/unique metadata from BL-26 profile to lenses | Self-join count in generated SQL = 0 on key joins |
| STR-ontop-06 | Ontop | Dialect breadth | 01,06 | Warehouse reach | reuse | Support matrix per tenant source | Query passes on Postgres, Snowflake, DuckDB fixtures |

**INV-ontop-01 — Seed hypothesis: virtual graphs are read-mostly and mapping-heavy; invert with hybrid virtualise/materialise and mapping versioning.** Target: Ontop 5.5.0, virtual repository over relational sources. **Verdict on the §10.5 hypothesis: PARTLY VALIDATED, PARTLY ALREADY SATISFIED UPSTREAM.** *Validated:* read-only (no write path documented), mapping authoring is mandatory and manual (`bootstrap` is only a starting point), graph traversal is paid at SQL-join cost, and there is no mapping versioning or governance [CLAIM-ontop-01,05,06]. *Rejected as stated:* the "hybrid" is not novel — Ontop already executes the **same mappings** in virtual and materialised modes, with streaming and per-class output [CLAIM-ontop-05]. The missing piece is a **policy layer**: which predicates to virtualise vs materialise, freshness SLAs, invalidation, and ACLs. Root cause: semantics/coupling (*proven*: relational rewriting; *hypothesis*: union blow-up as dominant cost). Why the alternative helps: materialising hot, traversal-heavy subgraphs into the governed graph removes SQL-join cost and gives bitemporal history and provenance; it is worse when sources change faster than ingestion can follow, when data sovereignty forbids copies, or for rarely-queried long tails. Options: (1) quick — Ontop sidecar for exploration + nightly `materialize` as a connector; (2) native — hybrid planner choosing per-predicate mode from query log statistics and source freshness metadata, with mapping files versioned in `ontology/gitops.py`; (3) long-term — incremental view maintenance from CDC (Debezium) into the graph with virtual fallback. Select (2). Sketch:

```
mode(pred) = MATERIALISE if hops(pred) >= 3 and p95_sql_ms(pred) > T and change_rate(pred) <= R
           else VIRTUAL
mapping_version(pred) -> git sha;  materialised edges carry mapping_version + source_snapshot
```

POC: one Postgres CMDB replica (≈ 1 M CIs, 5 M relations), 30 impact-analysis queries (1–6 hops); metric p95 latency and result-equality vs SQL ground truth for VIRTUAL, MATERIALISED and HYBRID; baseline Ontop virtual 5.5.0 with default T-mappings on 8 cores/16 GB. Falsifier: hybrid does not beat pure virtual by ≥ 3× on ≥ 3-hop queries. Dependencies: connectors (BL-23), replay (BL-24), tombstones (BL-25). Failure cases: stale materialised edges after source deletes (needs tombstone via snapshot diff), mapping change invalidating history (store `mapping_version`), tenant leakage via shared Ontop instance (one VKG instance or credentials per tenant). Defensibility: governance (versioned mappings, provenance, freshness policy, ACL) persists even if Ontop adds a similar toggle. Decision: **EXPERIMENT**.

**INV-ontop-02 — No permission model.** Root cause: governance (*proven*). Option: per-tenant, per-role DB principals; row-level security in the source; user identity passed through 5.2.0 header hook for audit; gateway rejects queries touching unmapped predicates. POC: two users with different RLS see disjoint rows through the same SPARQL endpoint; zero leakage in 1,000 randomised queries. Decision: **EXPERIMENT** (P0 prerequisite to exposing any VKG).

**INV-ontop-03 — RDF 1.1 / OWL 2 QL expressivity ceiling.** Root cause: semantics/algorithm (*proven*: QL profile). Option: keep richer reasoning (RL rules, SHACL) in the governed graph for materialised portions; document QL lint. Decision: **ADOPT** (documentation + lint).

**INV-ontop-04 — Dialect and driver churn.** Root cause: maturity/operations (*proven* by per-release DB fixes). Option: certified source matrix (Postgres, MySQL, SQL Server, Oracle, Snowflake, DuckDB), contract tests per release. Decision: **ADOPT**.

**INV-SELF-OBDA-01 — EOIP virtualisation is a mock with an injectable SQL builder.** Root cause: maturity (*proven*, `mapping/virtualization.py:59-80`). Option: drop string interpolation, use parameterised queries, mark module as simulation, or replace with Ontop adapter. Decision: **ADOPT** (security P1).

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-21 federation/virtualisation (OBDA) | INTEGRATE Ontop | Sidecar; do not write own unfolder |
| CAP-29 declarative mapping R2RML | INTEGRATE / REUSE | Export-import with CML |
| CAP-15 SPARQL over sources | INTEGRATE | Read-only |
| CAP-23 OWL profile (QL) | REUSE via Ontop for virtual path | |
| CAP-26 connectors | INTEGRATE `materialize` as batch adapter | Events, not direct writes |
| CAP-28 schema inference | EXPERIMENT (`bootstrap` vs BL-26) | |
| Hybrid virtual/materialise policy | BUILD | INV-ontop-01 |
| Mapping versioning/diff | BUILD | CAP-37, `gitops.py` |
| CAP-46 ACL on virtual reads | BUILD | INV-ontop-02 |
| CAP-20 portable query IR | EXPERIMENT (QueryPlan → SPARQL for Ontop) | |
| RDF 1.2 / RDF-star | DEFER | Not supported |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All PROPOSED. T1: Docker `ontop/ontop:5.5.0` + Postgres fixture; 20 SPARQL queries vs SQL ground truth. T2: W3C R2RML test-case suite through Ontop and through `mapping/r2rml.py`; publish pass rates. T3: `materialize --separate-files` → connector → graph; replay idempotency and tombstone-on-delete. T4: hybrid POC from INV-ontop-01. T5: RLS leakage probe (INV-ontop-02). T6: generated-SQL review for self-joins and union size at hierarchy depth 1/3/6 (T-mapping blow-up). T7: air-gap run with no network. T8: fuzz `rewrite_point_query` for SQL injection before any wiring. Acceptance: T1/T5 green; no cross-tenant rows; materialised-vs-virtual answer equality.

## 15. Risks, trade-offs, and open research questions

Risks: virtual reads put load on operational databases; permissions at the source are the only barrier; JVM sidecar for a Python core; slowing release cadence and unclear Ontopic ownership; users expect writes. Open: SPARQL Update support; exact published benchmark numbers for 5.x; whether Ontopic Studio adds mapping versioning/ACL; Snowflake and Databricks maturity versus Postgres; T-mapping size at EOIP ontology scale; best IR for QueryPlan → SPARQL compilation.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Apache-2.0, 5.5.0, Ontopic |
| D2 | 2 | VKG over SQL |
| D3 | 4 | Engine, CLI, endpoint, Protégé |
| D4 | 5 | No storage; source DB |
| D5 | 3, 5 | RDFS, OWL 2 QL, R2RML |
| D6 | 5 | SPARQL→IQ→SQL; no own CBO |
| D7 | 5 | Rewriting + T-mappings (backward/compile-time) |
| D8 | 5 | Stateless; source isolation |
| D9 | 3, 5 | Core topic: OBDA, materialise |
| D10 | N/A | No ER |
| D11 | 5, 9 | No history; mapping git only |
| D12 | N/A | None |
| D13 | N/A | No retrieval; SPARQL only |
| D14 | 11 | Target for NL→SPARQL, not native |
| D15 | 3 | Protégé mapping editor; no governance |
| D16 | 3 | Protégé, endpoint UI |
| D17 | 3, 5 | CLI, Docker, converters |
| D18 | 5, 12 | JDBC creds, header hook, no ACL |
| D19 | 12 | Per-tenant instance/credential option |
| D20 | 7 | No numbers verified |
| D21 | 1, 10 | OSS + Ontopic commercial |
| D22 | 3 | R2RML, RDF export; no LPG |
| D23 | N/A | Not examined |
| D24 | App C | Source tag + docs |

## Appendix B — Capability mapping

| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-21 | native | 01,06 | BL-51 Partial (contracts/mock) | INTEGRATE | P1 |
| CAP-29 | native | 05 | BL-33 Implemented (not R2RML) | INTEGRATE | P1 |
| CAP-15 | native (read) | 01 | BL-06/09 stub | INTEGRATE | P2 |
| CAP-23 | partial (OWL 2 QL) | 06 | BL-30 Partial | REUSE | P2 |
| CAP-26 | partial (`materialize` batch) | 05 | BL-23 | INTEGRATE | P2 |
| CAP-28 | partial (`bootstrap`) | 05 | BL-26 Implemented | EXPERIMENT | P3 |
| CAP-37 | absent | — | BL-32 Partial | BUILD | P2 |
| CAP-46 | absent | — | BL-18 Absent | BUILD | P0 |
| CAP-50 | native | 02 | — | INTEGRATE | P2 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class. | Source | Pub./access | Confidence | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-ontop-01 | 5.5.0 | VKG over relational DBs; SPARQL→SQL via R2RML/Ontop mappings; RDF 1.1, RDFS, OWL 2 QL; most of SPARQL 1.1 + GeoSPARQL; lenses; materialise; Protégé plugin; Apache-2.0, docs CC BY 4.0 | Officially documented | ontop-vkg.org/guide/ | 2026-02 / 2026-10-26 | 0.9 | none |
| CLAIM-ontop-02 | repo | Apache-2.0 SPDX; not archived; last push 2026-10-15; README: current 5.5.0, released 14/02/2026; tags 5.4.0, 5.5.0 | Officially documented | github.com/ontop/ontop (API, README) | 2026-10 / 2026-10-26 | 0.9 | none |
| CLAIM-ontop-03 | 5.0.0–5.5.0 | Release content: 5.0 Java 11+, SPARQL rules, Snowflake/MariaDB, lenses rename; 5.2 compression, header user info; 5.3 RDF4J 5.1.0, constraint inference; 5.4 `rdfs:subClassOf*`, two-phase unfolder, TDEngine; 5.5 CTEs, files as relation names, DuckDB 1.4 | Officially documented | ontop-vkg.org/guide/releases.html | 2026-02 / 2026-10-26 | 0.9 | none |
| CLAIM-ontop-04 | 5.5.0 | `jdk.version` 11; RDF4J 5.1.4; OWLAPI 5.5.1; module layout | Observed in source code | `pom.xml` @ontop-5.5.0 | 2026-02 / 2026-10-26 | 0.9 | 5.0 notes say "Java 11 or newer" (consistent) |
| CLAIM-ontop-05 | 5.5.0 | CLI: `bootstrap`, `endpoint`, `extract-db-metadata`, `materialize`, `query`, `validate`, `mapping`; materialise formats rdfxml/turtle/ntriples/nquads/trig/jsonld, streaming default, `--separate-files`, compression | Officially documented | ontop-vkg.org/guide/cli.html; `client/cli/.../Ontop*.java` | 2026 / 2026-10-26 | 0.9 | none |
| CLAIM-ontop-06 | 5.5.0 | Components: `TMappingSaturatorImpl`, `TreeWitnessRewriter`, `ExistentialQueryRewriter`, `BasicQueryUnfolder`, `TwoPhaseQueryUnfolder`, `core/optimization` optimisers, `db/rdb` dialect providers (Athena, BigQuery, DB2, DuckDB, H2, MySQL, Oracle, PostgreSQL, SQLServer, SparkSQL, TDEngine, Teiid, Trino, Dremio, Denodo, UCanAccess), `DefaultOntopRDFMaterializer` | Observed in source code | source tree @ontop-5.5.0 | 2026-02 / 2026-10-26 | 0.85 (existence read; algorithm semantics inferred) | none |
| CLAIM-ontop-07 | EOIP dev_local | `rewrite_point_query` interpolates `entity_id` into SQL; `execute_point_query_mock` uses a dict; `federation/obda.py` is contracts | Observed in source code | `packages/eoip/mapping/virtualization.py:59-80`, `federation/obda.py` | working tree / 2026-10-26 | 0.95 | none |
| CLAIM-ontop-08 | Ontopic | Ontopic offers commercial support; Studio/Suite built on Ontop; deployment options | Third-party report (vendor site) | ontopic.ai, docs.ontopic.ai, ontop-vkg.org/community/support.html | 2026 / 2026-10-26 | 0.7 | pricing unknown |
| CLAIM-ontop-09 | Ontopic | Acquired by Digital Science (metaphactory integration) | Unverified | LinkedIn post (via search) | n/d / 2026-10-26 | 0.25 | no primary |
| CLAIM-ontop-10 | GraphDB 9.5 | Ontotext joined Ontop; all editions offer Ontop-based virtual repositories | Third-party report | PR Newswire GraphDB 9.5, Dec 2020 | 2020-12 / 2026-10-26 | 0.6 | not re-checked for 11.x |

## Appendix D — Assumptions

1. Access date 2026-10-26 (not the brief's 2026-10-18).
2. "Latest" = highest tag/release found (5.5.0); no 5.6 or 6.0 tag exists on 2026-10-26.
3. SPARQL Update, result caching semantics, measured performance and Ontopic terms were not verified.
4. T-mapping behaviour is inferred from source file names, tests and OBDA literature, not from line-level code reading.
5. The seed hypothesis verdict (partly validated) rests on documentation plus source layout; the POC in INV-ontop-01 is the falsification test.
