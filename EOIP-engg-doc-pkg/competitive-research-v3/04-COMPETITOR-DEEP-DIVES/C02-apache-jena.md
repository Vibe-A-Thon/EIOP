# C02 — Apache Jena (TDB2, Fuseki, rule engines, SHACL)

| Field | Value |
|---|---|
| Registry ID | T-C02-apache-jena |
| Tier | A — Apache-2.0 reference RDF stack; EOIP has a `FusekiGraphStore` adapter; primary REUSE/oracle candidate for SPARQL, SHACL and rule reasoning |
| Versions examined | Jena 6.2.0 (Maven Central 2026-08-01; tag `jena-6.2.0`, build timestamp 2026-07-27, commit `d0676a2`), 6.1.0 (2026-05-12), 6.0.0 (ASF catalog 2026-01-27); 5.4.0 (2025-04, RDF 1.2 preview) |
| Verified on | 2026-10-26 (actual access date; brief says 2026-10-18 — see Appendix D) |
| Worker | W08 (batch V02) |

## 1. Identity, current status, tier, and sources

**Identity.** Apache Jena is an Apache Software Foundation top-level project (HP Labs origin 2000, ASF 2010, TLP April 2012) licensed Apache-2.0. [CLAIM-jena-02] Components: RDF API, ARQ (SPARQL), RDF I/O, Assembler, CLI tools, GeoSPARQL, Inference and Ontology APIs, Query Builder, RDF Connection, RDF Patch, SHACL, ShEx, TDB2, Text Search, and the Fuseki server. [CLAIM-jena-03]

**Version trap (brief said "latest 5.x").** The current line is **6.x**: 6.0.0 on 2026-01-27, 6.1.0 on 2026-05-12, 6.2.0 on 2026-08-01. The Jena 5.6.0 announcement pre-announced Jena 6 with minimum **Java 21**, Lucene 10, retirement of the Fuseki WAR/webapp, retirement of `jena-permissions`, and TDB1 deprecation (third-party mirror of the dev-list announcement; plan, not confirmed per release). [CLAIM-jena-01] Java 21 is confirmed twice: the download page ("Jena6 requires Java 21") and `<java.version>21` in the 6.2.0 `pom.xml`. [CLAIM-jena-01] Repository not archived; last push 2026-10-25. [CLAIM-jena-02]

**Other traps.** "Jena" vs the legacy HP Jena 2 and the many third-party "jena-*" Maven artefacts (SDB, LARQ tags are historic); Fuseki "1" is retired, `fuseki2` is the current code path. No separate commercial vendor; Fuseki is the server, TDB2 the store.

**Sources (10):** Jena download page, about page, Fuseki, TDB2, TDB2-admin, Inference and SHACL docs; GitHub repo API and tags; ASF release catalog; Maven Central listing; W3C RDF 1.2 / SPARQL 1.2 specs; source at tag `jena-6.2.0` (sparse clone).

## 2. Primary problem, target workloads, concrete example workflows

Open RDF/SPARQL toolkit and server for single-node triple stores up to hundreds of millions of triples, embedded reasoning, validation and linked-data publishing. [CLAIM-jena-05] Example EOIP workflow: run Fuseki 6.2 (Docker) with a TDB2 dataset and a `fuseki:shacl` endpoint; EOIP's mutation gateway posts a candidate batch to `/shacl`, receives a validation report, and only then commits. Example 2: use the CLI (`shacl validate`, `sparql`, `riot`) as a conformance oracle against EOIP's in-house SHACL subset and JSON-LD code (BL-29/31).

## 3. Feature inventory

| Feature | Status | CLAIM |
|---|---|---|
| SPARQL 1.1 Query/Update/Protocol, Graph Store Protocol | present | 04 |
| SPARQL 1.2 / RDF 1.2 triple terms | partial: experimental preview since 5.4.0; status in 6.x UNVERIFIED | 08 |
| TDB2 persistent transactional store | present (TDB1 deprecated per plan) | 05 |
| Fuseki server, Docker image, Shiro security, metrics, modules | present | 04 |
| Fuseki web UI | present (Vue 3.5 + Vite app `jena-fuseki-ui`); 5.4.0 notes UI did not yet render RDF 1.2 results | 04, 08 |
| Access control module `jena-fuseki-access` | present (graph-level data access control; depth UNVERIFIED) | 04 |
| RDFS reasoner (Full/Default/Simple) | present | 06 |
| OWL Full/Mini/Micro rule-based reasoners | present, incomplete by design | 06 |
| Generic rule engine: forward (RETE), backward (LP/tabling), hybrid | present | 06 |
| SHACL Core + SHACL-SPARQL constraints, SHACL compact syntax, SPARQL targets | present | 07 |
| SHACL-AF rules / node expressions | not stated in docs: UNVERIFIED | 07 |
| ShEx | present (module `jena-shex`) | 03 |
| GeoSPARQL Fuseki module | present | 04 |
| Text search (Lucene) | present | 03 |
| Complete OWL DL reasoning | absent ("use an external DL reasoner") | 06 |
| Clustering / sharding / HA | absent in core; RDF Patch for replication is a building block (depth UNVERIFIED) | 03, 05 |
| Commercial support | absent from the project (third parties exist; not researched) | — |
| Ontology governance, vector search, LLM features | absent | — |

## 4. Architecture diagram

```
 Clients: SPARQL/HTTP | Graph Store | RDF Connection (Java) | CLI (riot, sparql, shacl, tdb2.*)
        │
 ┌──────▼────────────────────── Fuseki (jena-fuseki-main/core/server) ─────────────┐
 │ endpoint router: query | update | gsp-rw | shacl | patch | upload | stats        │
 │ Shiro auth ─ access module ─ modules (GeoSPARQL, custom) ─ Vue admin UI           │
 └──────┬───────────────────────────────────────────────────────────────────────────┘
        │ DatasetGraph API (transactions: begin/commit/abort)
 ┌──────▼─────────┐   ┌────────────────────┐   ┌──────────────────────┐
 │ ARQ: parse →    │   │ Inference layer    │   │ jena-shacl, jena-shex │
 │ algebra →       │   │ InfModel over Graph│   │ validation (in-proc)  │
 │ optimise → exec │   │ RETE / LP / hybrid │   └──────────────────────┘
 └──────┬─────────┘   └────────────────────┘
        ▼
 TDB2: node table (NodeId ↔ term), triple/quad tables on B+Trees,
       single-writer / multi-reader transactions, generations + compaction
 State: on-disk Data-NNNN directories; control plane = config.ttl assembler
```

## 5. Under-the-hood reconstruction

**Data model.** RDF dataset of named graphs; `DatasetGraph` abstraction; RDF 1.2 triple terms preview. Terms are mapped to `NodeId`s through a node table (`NodeTableNative`, caches, inline numeric values). [CLAIM-jena-05] (source `jena-tdb2/.../store/nodetable/`, tag `jena-6.2.0`)

**Storage.** TDB2 builds its triple/quad tables over B+Trees (`BPlusTreeFactory.createBPTree` in `TDB2StorageBuilder.java:281`) and a switchable generation design (`DatasetGraphSwitchable`) that lets compaction write a new `Data-NNNN` generation while readers continue; compaction is invoked with `DatabaseMgr.compact(...)` because databases "grow over time as updates occur". [CLAIM-jena-05] Exact index orderings (SPO/POS/OSP/GSPO…): not read at source level in this pass (UNVERIFIED).

**Transactions.** Transactional only (no autocommit); "writer pays" so readers do not; no transaction size limit (TDB1 had one); single-machine. The docs do not name MVCC; the behaviour is snapshot-style multi-reader/single-writer (*inference* from "writer pays" and the generation layout). [CLAIM-jena-05]

**Query pipeline.** ARQ: parser → algebra → optimiser (transformations, join reordering using a statistics-free heuristic by default, *hypothesis*) → streaming execution on `QueryIterator`s; source under `jena-arq/.../sparql/engine/main`. No cost-based WCOJ planner was verified.

**Reasoning (verified at source layout).** Under `jena-core/.../reasoner/rulesys`: `RETEEngine` (+`RETEConflictSet`, `RETEClauseFilter`) for forward chaining; `LPBRuleEngine`, `LPInterpreter` and tabling for backward chaining; hybrid = forward rules instantiate backward rules (data flows one way). Forward mode is incremental, only re-exploring consequences of changes; backward/hybrid discard tabled results on updates. [CLAIM-jena-06] Documented pathologies: loops possible, `remove`/`drop` primitives are non-monotonic, importing `owl.owl` or combining reasoners can cause "substantial slowdowns", OWL equality reasoning is the most expensive, RDFS figures are for in-memory models only. [CLAIM-jena-06] Rule pseudo-form:

```
[transitive: (?a ex:dependsOn ?b) (?b ex:dependsOn ?c) -> (?a ex:dependsOn ?c)]   # forward
[-> tabled]  (?x ex:impacts ?y) <- (?x ex:dependsOn ?y)                           # backward
```

**SHACL.** `jena-shacl` implements Core and SPARQL constraints plus compact syntax and SPARQL targets, exposed via CLI, API and the Fuseki `fuseki:shacl` operation (needs "new style" endpoint declarations; not installed by default). A `ValidationListener` hook exists. [CLAIM-jena-07]

**Security/caching/versioning.** Shiro-based authentication; access-control module; Fuseki exposes metrics/statistics; versioning of data is not native (RDF Patch is a change log format, depth UNVERIFIED); caches are node-table and block caches (sizes configurable, *hypothesis*).

## 6. Functional and non-functional requirements inferred

| ID | Requirement |
|---|---|
| FR-1 | Expose standard SPARQL 1.1 protocol so any client works; separate `/shacl` validation operation |
| FR-2 | Transactional batches of unbounded size on one node |
| FR-3 | Pluggable rule engines with explicit monotonic/non-monotonic caveats |
| FR-4 | Embeddable via modules; Docker image provided (`jena-fuseki-docker`) |
| NFR-1 | Java 21+; JVM heap sizing; SSD recommended for TDB2 |
| NFR-2 | Periodic compaction; backups via admin API |
| NFR-3 | Single-node scale ceiling: bulk upload "hundreds of millions of triples" (docs) [CLAIM-jena-05] |

## 7. Performance and resource model

Only vendor-neutral project statements exist: hundreds of millions of triples in a live Fuseki bulk upload (docs, no hardware stated); inference docs say OWL Full/Mini run about 3–4× slower than RDFS on pure RDFS data and RDFS numbers are in-memory only, DB-backed inference "would likely perform poorly without caching". [CLAIM-jena-05,06] No independent benchmark was collected (LUBM/BSBM/SP2Bench results exist in the literature; not retrieved). Failure modes: unbounded rule loops, large compaction I/O, full-generation disk use during compaction (*hypothesis*), JVM GC on large heaps.

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match/exceed |
|---|---|---|
| S1 | Apache-2.0, ASF governance, active (push 2026-10-25) | Reuse as network service or CLI oracle |
| S2 | Three rule engines incl. incremental RETE | Reuse for small per-tenant ontologies |
| S3 | SHACL Core+SPARQL in-process and as a Fuseki endpoint | Reuse as oracle; match in gateway |
| S4 | TDB2 transactions with no size limit, single-node simplicity | Fits one-node-first |
| S5 | Fuseki module system, Docker image, GeoSPARQL | Sidecar deployment |
| S6 | Early RDF 1.2 implementation | Track for standards gate |

## 9. Limitations with root causes

| Type | Limitation | Root cause |
|---|---|---|
| Intentional trade-off | OWL reasoners are sound-not-complete, instance-based, no `complementOf`/`oneOf` | Rule-based approximation of OWL Full |
| Algorithmic dead-end | Backward/hybrid tables flushed on update; equality reasoning expensive | Tabling without incremental maintenance |
| Operational | Single-node store, no sharding/HA in core; compaction needed | TDB2 design |
| Operational | JVM; Java 21 floor (a breaking change from 5.x) | Project policy |
| Friction | RDF 1.2 in flux, Fuseki UI lagged on 1.2 results | Spec still moving: SPARQL 1.2 Query is a Working Draft (2026-10-25) [CLAIM-jena-08] |
| Friction | Security via Shiro/access module; no tenant model | Not a goal |
| Hypothesis | Deleting/re-asserting facts under inference models forces recomputation | Per docs on tabling |
| Outdated | Jena 5.x docs/blogs describing WAR deployment | Retirement planned for 6 |

## 10. Deployment, licensing, redistribution, operational viability

Apache-2.0: embedding, OEM, SaaS and redistribution permitted subject to NOTICE/licence retention; no copyleft or patent exclusion beyond Apache's grant (not legal advice; standard class: **permissive**). Transitive dependency licences (Lucene, Shiro, Jetty) not audited here. Air-gapped: yes (no phone-home identified; telemetry absent in docs read). One-node: yes. EOIP's `rdf_backend.py` docstring says "GPL/AGPL servers never linked" — Jena/Fuseki is not GPL, so that caution does not apply here; running Fuseki as a sidecar container remains the lowest-coupling pattern for a Python product. Deployment: `jena-fuseki-docker`, `apache-jena-fuseki` distribution, or embedded Java (not applicable to Python).

## 11. Competitive delta against the EOIP verified baseline

| Area | EOIP | Jena | Delta |
|---|---|---|---|
| BL-06 Fuseki adapter | **Stub**: dict cache; HTTP only for ASK health probe; `query_url/update_url/data_url` unused (`graph/rdf_backend.py:25-214`, esp. `:40-42,49-56,72-83,189-210`) [CLAIM-jena-09] | Real SPARQL/GSP server | Adapter has no live path |
| SPARQL handler | Returns synthetic bindings, backend untouched (`query/sparql_protocol.py:124-152`) [CLAIM-jena-09] | Real engine | Must be replaced before any SPARQL claim |
| BL-29 SHACL | in-house subset; pySHACL absent (test fails) | Core + SPARQL, W3C test coverage claimed by project (not verified here) | Use Jena as differential oracle |
| BL-30 OWL | subclass/disjoint/chain (`ontology/rdf.py:598`) | RDFS + OWL Mini/Micro/Full rules + custom | Moderate deficit; INTEGRATE |
| BL-31 JSON-LD/RDF I/O | Implemented in-house | `riot` reference parser | Use `riot` as conformance oracle |
| BL-37 bitemporal | Implemented | none native | EOIP ahead |
| BL-18/20 ACL, tenancy | Absent / contract only | Access module, Shiro | Not a solution to per-fact source ACL |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

| STR-ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-jena-01 | Jena | Apache-2.0 Fuseki+TDB2 as default RDF backend | 02,04,05 | Redistribution-safe RDF option | integrate | Compose service `fuseki:6.2`, adapter speaks SPARQL 1.1 + GSP with auth | Round-trip 10 k entities survive restart; conformance suite green |
| STR-jena-02 | Jena | Validation endpoint `/shacl` | 07 | Gateway-level shape checks | integrate/reuse | POST candidate batch to `fuseki:shacl`; map report to PROPOSED/REJECTED | Differential test vs in-house validator: 0 disagreements on W3C Core cases |
| STR-jena-03 | Jena | Incremental RETE forward rules | 06 | Small-ontology inference without a new engine | experiment | Per-tenant InfModel in sidecar for ontologies < 100 k triples | Insert/delete latency vs full recompute ≥ 5× faster on 1 % change |
| STR-jena-04 | Jena | Unlimited-size transactions with compaction | 05 | Safe bulk loads | match | Backend-agnostic batch contract: one atomic revision per batch | 1 M-triple batch abort leaves no partial state |
| STR-jena-05 | Jena | `riot`/`shacl` CLI as oracle | 03,07 | Standards gate for BL-29/31 | reuse | CI job runs CLIs on fixtures | W3C SHACL + RDF test pass rates published |

**INV-jena-01 — Reasoning is in-memory and non-incremental for backward chaining.** Target: Jena 6.2, generic rule reasoner, hybrid mode [CLAIM-jena-06]. Limitation: tabled results discarded on update; DB-backed models slow; OWL equality costly. Root cause: algorithm/coupling (*proven* by documentation). Alternative: externalise rules to a Datalog engine with semi-naïve incremental maintenance and support counts, writing results as `inferred` facts with evidence (worse when rule sets need OWL DL expressivity or non-stratified negation). Options: (1) quick — run Jena rules per tenant on small ontologies; (2) native — Datalog packs over the mutation gateway; (3) long-term — tiered materialise/rewrite. Selected: (2) via C02 Soufflé/Nemo research. POC: 500 k-edge graph, 10 rules, 1 % change batch; metric incremental update ≥ 5× faster than Jena hybrid re-inference; baseline Jena InfModel on same data and a 16 GB heap. Dependencies: epistemic plane BL-40. Failure case: derived facts leak across tenants (separate ledgers). Defensibility: explanation traces plus tenant-scoped ledger. Decision: **EXPERIMENT**.

**INV-jena-02 — Single-node store, no tenant model.** Root cause: storage design (*proven*). Option (1) one Fuseki dataset per tenant (quick); (2) tenant-scoped named-graph policy in the adapter plus access module; (3) per-tenant physical stores behind one gateway. Risk of (1): cross-dataset federation cost. POC: 50 tenants × 1 M triples, check leakage with J13-style probes, RSS per idle dataset. Decision: **EXPERIMENT**.

**INV-jena-03 — Spec churn (RDF/SPARQL 1.2).** Root cause: maturity/standards (*proven*: Concepts is a Candidate Recommendation Snapshot dated 2026-04-07; SPARQL 1.2 Query a Working Draft of 2026-10-25). Option: version-pin and keep EOIP's RDF-star-like needs in its own claim layer (BL-39) rather than triple terms until Recommendation. Decision: **DEFER**.

**INV-SELF-RDF-01** (see GraphDB deep dive): EOIP's Fuseki adapter is a cache; **ADOPT** a real SPARQL client first with Jena Fuseki as the reference target.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-02 RDF storage | INTEGRATE (Fuseki/TDB2 sidecar) | Apache-2.0 |
| CAP-15 SPARQL | INTEGRATE | Real client required |
| CAP-10 SHACL | REUSE (Jena `shacl` CLI/endpoint, pySHACL for Python path) | Oracle role |
| CAP-23 OWL profile reasoning | INTEGRATE for small ontologies; EXPERIMENT elsewhere | Jena rules not complete OWL |
| CAP-22 incremental rules | EXPERIMENT | INV-jena-01 |
| CAP-24 explanation | BUILD | Jena offers derivation logs (`getDerivation`, depth UNVERIFIED) |
| CAP-47 tenancy | EXPERIMENT | INV-jena-02 |
| CAP-11 RDF 1.2 triple terms | DEFER | Spec in flux |
| CAP-05 scale-out | REJECT for Jena | Use other backends |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

PROPOSED: (1) Compose `fuseki:6.2.0` + TDB2; adapter upsert/find/tombstone round trip across restart (fails today). (2) W3C SPARQL 1.1 and SHACL Core suite run against Fuseki through the EOIP adapter; record pass rates. (3) Differential SHACL test of `ontology/shacl_validator.py` vs `shacl validate`. (4) Compaction under write load: p95 query latency and disk high-water mark. (5) Tenant isolation probe with two datasets and Shiro roles. (6) Java 21 base image in air-gapped build. Acceptance: tests 1–2 green and BL-06 restated before any "RDF backend certified" claim.

## 15. Risks, trade-offs, and open research questions

Risks: JVM sidecar adds heap and ops cost to a one-node Python product; Java 21 floor; RDF 1.2 migration; rule engine pathologies; dependency licence audit. Open: exact TDB2 index set and statistics-driven optimisation; Jena 6.x RDF 1.2 completeness; derivation-explanation API depth; independent LUBM/BSBM numbers at 6.2; Fuseki UI 6.x changes beyond Vue/Vite; RDF Patch as an event-sourcing feed for BL-24.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | ASF, Apache-2.0, 6.2.0 |
| D2 | 2 | Single-node RDF toolkit |
| D3 | 4 | Fuseki / ARQ / TDB2 / inference |
| D4 | 5 | B+Tree tables, node table; index order UNVERIFIED |
| D5 | 3, 5 | RDFS, OWL rules, SHACL, ShEx, RDF 1.2 preview |
| D6 | 5 | ARQ algebra; cost model not verified |
| D7 | 5, 12 | RETE, LP, hybrid |
| D8 | 5, 7 | Single-writer, no HA |
| D9 | 3 | Upload, RDF Connection; no OBDA |
| D10 | N/A | No ER |
| D11 | N/A | No native history |
| D12 | N/A | None |
| D13 | N/A | No retrieval/LLM features |
| D14 | N/A | Query Builder only |
| D15 | N/A | Not an authoring tool |
| D16 | 3 | Fuseki Vue UI |
| D17 | 3, 14 | CLI, modules, Docker |
| D18 | 5, 9 | Shiro, access module |
| D19 | 12 | Dataset-per-tenant option |
| D20 | 7 | Docs-only |
| D21 | 10 | Apache-2.0, no vendor |
| D22 | 11 | Standards-based I/O |
| D23 | N/A | None examined |
| D24 | App C | Docs + source tag |

## Appendix B — Capability mapping

| CAP-ID | Technology | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-02 | native | 05 | BL-06 stub | INTEGRATE | P1 |
| CAP-10 | native | 07 | BL-29 Partial | REUSE | P1 |
| CAP-15 | native | 04 | BL-06/09 | INTEGRATE | P1 |
| CAP-22 | partial (forward RETE incremental) | 06 | Absent | EXPERIMENT | P2 |
| CAP-23 | partial (incomplete OWL) | 06 | BL-30 Partial | INTEGRATE | P2 |
| CAP-04 | native (embedded/single node) | 05 | — | INTEGRATE | P2 |
| CAP-11 | partial (RDF 1.2 preview) | 08 | BL-31 | DEFER | P3 |
| CAP-45 | partial (Shiro/access module) | 04 | BL-19 | REUSE | P3 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class. | Source | Pub./access | Confidence | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-jena-01 | Jena 6.0.0–6.2.0 | 6.0.0 archived 2026-01-27; 6.1.0 2026-05-12; 6.2.0 2026-08-01; Java 21 required; Jena 6 plan included Fuseki WAR and jena-permissions retirement | Officially documented / Third-party report for plan | jena.apache.org/download; release-catalog.apache.org/jena/6.0.0; mvnrepository.com jena versions; `pom.xml` `java.version=21` at tag jena-6.2.0; Jena 5.6.0 announcement mirror (eclipse.org lyo-dev list) | 2026 / 2026-10-26 | 0.85 versions, 0.5 plan items | catalog "not yet reviewed by Jena" |
| CLAIM-jena-02 | repo | Apache-2.0 (SPDX), not archived, last push 2026-10-25; ASF TLP April 2012 | Officially documented | github.com/apache/jena (API); jena.apache.org/about_jena/about.html | 2026-10-25 / 2026-10-26 | 0.9 | none |
| CLAIM-jena-03 | docs | Component list incl. SHACL, ShEx, TDB2, GeoSPARQL, Text Search | Officially documented | jena.apache.org docs menu | 2026 / 2026-10-26 | 0.85 | none |
| CLAIM-jena-04 | Fuseki 6.2 | SPARQL 1.1 protocols + GSP, TDB integration, Shiro, Docker, modules; source modules core/ui/access/main/mod-geosparql/server/docker; UI package uses Vue 3.5, Vite | Observed in source code + Officially documented | jena.apache.org/documentation/fuseki2/; `jena-fuseki2/pom.xml` and `jena-fuseki-ui/package.json` @jena-6.2.0 | 2026 / 2026-10-26 | 0.85 | none |
| CLAIM-jena-05 | TDB2 | Transactional only, writer pays, no txn size limit, not TDB1-compatible, compaction via `DatabaseMgr.compact`, B+Tree in `TDB2StorageBuilder.java:281`, hundreds of millions of triples bulk | Officially documented + Observed in source code | jena.apache.org/documentation/tdb2/ and tdb2_admin.html; source @jena-6.2.0 | 2026 / 2026-10-26 | 0.8 | docs do not name MVCC |
| CLAIM-jena-06 | Inference docs | RDFS reasoner; OWL Full/Mini/Micro incomplete; generic rule reasoner forward RETE incremental / backward tabled / hybrid default; limitations and slowdowns; DB-backed untested | Officially documented | jena.apache.org/documentation/inference/ ; source `reasoner/rulesys` @jena-6.2.0 | 2026 / 2026-10-26 | 0.85 | docs may predate 6.x |
| CLAIM-jena-07 | jena-shacl | Core + SPARQL constraints, compact syntax, SPARQL targets, `fuseki:shacl`, ValidationListener | Officially documented | jena.apache.org/documentation/shacl/ | 2026 / 2026-10-26 | 0.85 | SHACL-AF not mentioned |
| CLAIM-jena-08 | RDF/SPARQL 1.2 | Jena 5.4.0 experimental RDF 1.2 preview (triple terms, `rdf:reifies`, text direction) and Fuseki UI result rendering not yet; RDF 1.2 Concepts = Candidate Recommendation Snapshot 2026-04-07; SPARQL 1.2 Query = Working Draft 2026-10-25 | Third-party report + Officially documented | 5.4.0 announcement mirror (eclipse.org lyo-dev); w3.org/TR/rdf12-concepts, /sparql12-query | 2025-04, 2026 / 2026-10-26 | 0.7 / 0.9 | 6.x status unknown |
| CLAIM-jena-09 | EOIP dev_local | Fuseki adapter is a dict cache; SPARQL handler returns synthetic bindings | Observed in source code | `graph/rdf_backend.py`, `query/sparql_protocol.py` | working tree / 2026-10-26 | 0.95 | BL-06 wording |

## Appendix D — Assumptions

1. Access date 2026-10-26 (pages carry dates later than the brief's 2026-10-18).
2. User's "latest 5.x" corrected to 6.2.0 because 6.x exists.
3. Release dates for 6.x come from Maven Central / ASF catalog; no release-announcement pages were retrievable.
4. SHACL-AF, derivation-API depth, TDB2 index ordering and RDF 1.2 completeness in 6.x are UNVERIFIED.
5. Jena is treated as Apache-2.0 service reachable over HTTP; Java embedding is irrelevant to the Python core.
