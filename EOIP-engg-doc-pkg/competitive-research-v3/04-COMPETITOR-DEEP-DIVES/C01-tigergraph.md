# C01 — TigerGraph

| Field | Value |
|---|---|
| Registry ID | T-C01-tigergraph |
| Tier | A (direct enterprise graph competitor: distributed analytics, GSQL, vector and GraphRAG positioning) |
| Versions examined | TigerGraph DB 4.2.5 LTS (2026-09-02); 4.2.x history 4.2.0 (2025-04-03 preview) to 4.2.5; 4.3.0-rc2 (2026-10-20, preview); GraphRAG repo v2.0.4 (2026-10-21); licence agreement updated 2026-03-05; Savanna pricing docs |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V01 |

## 1. Identity, current status, tier, and sources

TigerGraph Inc. sells a proprietary native parallel (MPP) graph database. Members: **TigerGraph DB** (self-managed, Enterprise and Community editions), **Savanna** (managed cloud; the former "TG Cloud Classic" was transitioned to it), GraphStudio / Insights (UI and BI add-ons), GSQL (query language), and **GraphRAG** (formerly CoPilot; GitHub `tigergraph/graphrag`) [CLAIM-tigergraph-01][CLAIM-tigergraph-09][CLAIM-tigergraph-10].

Status: **active**. 4.2 line: 4.2.0 preview 2025-04-03, 4.2.1 2025-09-05, 4.2.2 2025-09-30, 4.2.3 2026-06-05, 4.2.4 2026-07-20, 4.2.5 2026-09-02, all marked LTS from 4.2.1 on; 4.3.0-rc1 2026-07-08 and rc2 2026-10-20 are preview, no GA date [CLAIM-tigergraph-01][CLAIM-tigergraph-02]. Maturity: production (enterprise). Source code is **not public**; internals below rest on a 2019 vendor paper, vendor decks and docs, so many claims are NOT PUBLICLY VERIFIED.

Trap check (Master Prompt §5.8): "100x faster" and "108 TB" style claims are vendor or vendor-tuned results (section 7). Name note: CoPilot was renamed to GraphRAG in the repo; docs still use "CoPilot".

Sources (13): see Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

Deep-link analytics over large connected data: fraud/AML ring detection, supply-chain and customer-360, recommendation, with real-time ingestion and 3-10+ hop pattern queries expressed in GSQL [CLAIM-tigergraph-07]. Newer positioning: hybrid graph + vector search for GenAI (TigerVector) and GraphRAG Q&A [CLAIM-tigergraph-05][CLAIM-tigergraph-10].

EOIP-shaped workflows: (1) impact analysis "what depends on service account X" as a multi-hop accumulator query; (2) incident root-cause scoring over a digital-thread graph using GSQL accumulators; (3) vector-anchored retrieval then graph expansion for answer grounding.

## 3. Feature inventory

| Feature | Status | Notes |
|---|---|---|
| Property graph, schema-first (typed vertices/edges) | present | NULLABLE attributes arrive in 4.3 preview [CLAIM-tigergraph-02] |
| GSQL (procedural, accumulators, BSP semantics) | present | Proprietary dialect [CLAIM-tigergraph-07] |
| openCypher / GQL | partial | Pattern-matching portion of GQL and openCypher "within the same execution engine"; syntax V3; ad hoc interpreted queries; OPTIONAL MATCH etc. [CLAIM-tigergraph-06] |
| Gremlin / SPARQL / SQL-PGQ | not found in sources read | UNVERIFIED |
| Vector type (ANN, hybrid GSQL) | present from 4.2 | 4096 dims CE, 32768 EE [CLAIM-tigergraph-05] |
| Full-text | not examined | UNVERIFIED |
| Distributed cluster, HA, cross-region replication | enterprise | HA/region-aware are preview; CE single-server only [CLAIM-tigergraph-03][CLAIM-tigergraph-08] |
| Incremental backup, rolling upgrade (preview) | present | [CLAIM-tigergraph-12] |
| RBAC, SSO (SAML/OIDC/LDAP; Kerberos, mTLS in 4.3), row policies | enterprise/partial | CE exclusions not enumerated in sources read [CLAIM-tigergraph-08][CLAIM-tigergraph-02] |
| Loaders: files, Kafka, Iceberg (preview) | present | External Kafka connector 3.6-3.9.2 removed in 4.2.0 [CLAIM-tigergraph-12] |
| Graph algorithm library | present | not itemised here |
| GraphStudio / Insights UI | present | Insights billed as add-on in Savanna [CLAIM-tigergraph-09] |
| GraphRAG service | present, separate | AGPL-3.0 since v2.0.1; TigerGraph only [CLAIM-tigergraph-10] |
| Temporal / bitemporal, ontology/OWL, SHACL | absent in sources | |
| Query plan caching, profiler | present (4.2) | [CLAIM-tigergraph-12] |
| Managed cloud (Savanna), BYOC | present | usage-priced [CLAIM-tigergraph-09] |

## 4. Architecture diagram

```
 clients: GraphStudio/Insights, REST (RESTPP), drivers, GSQL shell, GraphQL
        |  Nginx / auth (SSO, RBAC, row policy)
 +------v------------- TigerGraph cluster (shared-nothing) -----------+
 | RESTPP (API endpoints) -> GSQL compile/install (query -> C++ -> .so)|
 | per node: GSE (storage engine, vertex/edge segments, ID translation)|
 |           GPE (processing engine, parallel BSP execution)           |
 |           vector index (ANN) alongside vertex attrs                 |
 | Kafka-based change/WAL channel; admin (gadmin), CRR to DR region    |
 +--------------------------------------------------------------------+
   data plane: loaders (file/Kafka/Iceberg) -> partitions ; control plane: gadmin, GUI
 managed: Savanna (workspaces, compute/storage separation) ; AI: GraphRAG svc (python) -> LLM
```
Diagram synthesised from vendor sources; component names GSE/GPE appear in the vendor deck and third-party summaries; the Kafka WAL role and the compile-to-native-code step are hypotheses (H).

## 5. Under-the-hood reconstruction

**Data model.** Schema-first property graph; typed vertices and directed/undirected edges with attributes; multigraph support exists (docs list "Multi-graph", no detail read) [CLAIM-tigergraph-08]. External IDs are mapped to internal IDs by GSE [CLAIM-tigergraph-07].

**Storage layout and indexing.** Native graph store in custom C++ with disk persistence in GSE and in-memory computation in GPE (third-party summary of vendor docs). Physical layout (segment format, adjacency encoding, compression) is **NOT PUBLICLY VERIFIED**. Vector attributes have incremental ANN indexing with real-time updates; the TigerVector paper (SIGMOD 2025) describes the integration [CLAIM-tigergraph-05]. Secondary indexes on attributes: not examined.

**Query pipeline.** GSQL queries are installed (compiled) then run by GPE (H for the compile step); semantics are Bulk-Synchronous Processing: SELECT blocks over vertex sets with ACCUM (map) and POST-ACCUM (reduce) phases using accumulators for parallel aggregation [CLAIM-tigergraph-07]. 4.2 adds interpreted ad hoc queries and plan caching [CLAIM-tigergraph-12]; openCypher/GQL patterns are parsed into the same engine [CLAIM-tigergraph-06]. Cost-based optimisation details and join algorithms: NOT PUBLICLY VERIFIED.

**Reasoning.** None native (no OWL/Datalog). **Concurrency and transactions.** Docs list "transaction and ACID support" but the internals page was not retrievable; isolation level NOT PUBLICLY VERIFIED. **Partitioning.** Shared-nothing MPP with multiple partitions (dbdb summary); vertex-to-partition assignment and rebalancing scheme not public; repartition and expand/shrink operations are documented operationally [CLAIM-tigergraph-07][CLAIM-tigergraph-08]. **Consistency/replication.** HA cluster and cross-region replication (CRR) with failover commands; consistency model NOT PUBLICLY VERIFIED. **Caching.** Query plan cache. **Versioning.** Backup/incremental backup only; no graph history. **Security.** RBAC, row policies, SSO, audit log improvements, mTLS (4.3 preview) [CLAIM-tigergraph-02][CLAIM-tigergraph-08].

Reimplementation blueprint (equivalent behaviour, not copying): BSP superstep engine over partitioned adjacency arrays; vertex-set algebra (`SELECT t FROM s:src -(E)-> t:tgt ACCUM ...`) with commutative accumulators merged per partition then globally; ANN index co-located with vertex segments and updated through the same write path. EOIP value: accumulator-style aggregation as a typed query-plan operator (BL-08) executable in Python on small graphs and pushable to Gremlin/Cypher backends (H).

## 6. Functional and non-functional requirements inferred

FR: deep-hop analytics with accumulators; schema-first typed graph; ANN + graph hybrid; Cypher/GQL pattern subset; HA and DR; SSO/RBAC/row policy; incremental load. NFR: MPP scale-out; query deployment/installation step; licence-key-enforced limits; Linux-only self-managed server (Docker, bare metal, Kubernetes) [CLAIM-tigergraph-08].

## 7. Performance and resource model

Vendor/third-party claims only. (a) UC Merced / arXiv:1907.07405 (2019): LDBC SNB comparison with "active involvement of the vendors in tuning"; TigerGraph "two or more orders of magnitude" faster than Neo4j on some interactive-complex and BI queries; Neo4j completed 12 of 25 BI queries within five hours. This is academic but vendor-tuned and 2019-vintage [CLAIM-tigergraph-11]. (b) TigerGraph says it passed LDBC SNB 1 TB auditing; its later larger runs (e.g. 108 TB on SF30k with modified queries and fewer substitution parameters) are labelled unaudited [CLAIM-tigergraph-11]. (c) Marketing load rate of 50-150 GB/hour per machine is self-reported (third-party relay, no hardware context). No independent v4.2 benchmark found. Scaling behaviour: scale-up and scale-out claimed in the 2019 paper's benchmark; failure modes unknown. **Licence clause:** the Community licence forbids running or publishing benchmarks, so EOIP cannot publish CE comparisons [CLAIM-tigergraph-04].

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match or exceed |
|---|---|---|
| STR-tigergraph-01 | Accumulator-based deep-hop analytics (BSP) | Typed accumulator operator in QueryPlan, pushdown where backend supports |
| STR-tigergraph-02 | Hybrid vector + graph in one query language | Hybrid plan operator over pluggable vector engine; add ACL pre-filter |
| STR-tigergraph-03 | Operational completeness: incremental backup, CRR, rolling upgrade, audit log, row policy | Match basics on EOIP (BL-50, BL-49, BL-19) |
| STR-tigergraph-04 | Query language bridging: GSQL with openCypher/GQL patterns in one engine | Pattern: compile standard patterns into typed plans (BL-09 production path) |

Strength cards: STR-tigergraph-01 | TigerGraph | accumulator analytics | [CLAIM-tigergraph-07] | impact analysis/root-cause scoring in one pass | match | add `aggregate` operator with commutative-monoid contract and bounded depth | accumulated count of reachable systems equals brute-force on 1M-edge graph, within time budget. STR-tigergraph-02 | TigerGraph | hybrid | [CLAIM-tigergraph-05] | GraphRAG anchoring | match | vector candidates restricted to ACL-visible ids before expansion | zero ACL violations in canary test; recall vs plain hybrid RAG baseline (Master Prompt §5.3).

## 9. Limitations with root causes

| Class | Item | Type | Evidence |
|---|---|---|---|
| Licensing | CE: internal use, revocable, no support, no third-party use, no derivative/redistribution, no benchmark publication, 300 GB combined, no mixing with supported software | licensing | [CLAIM-tigergraph-03][CLAIM-tigergraph-04] |
| Licensing | GraphRAG repo moved Apache-2.0 to AGPL-3.0 at v2.0.1 (2026-07-22); only hybrid search officially supported, rest as-is/SoW | licensing | [CLAIM-tigergraph-10] |
| Algorithmic | GSQL is a proprietary dialect; Cypher/GQL only patterns | trade-off | [CLAIM-tigergraph-06] |
| Operational | Linux server stack, schema-first; HA features partly preview | verified | [CLAIM-tigergraph-08][CLAIM-tigergraph-12] |
| Operational | Savanna usage pricing with HA multiplier 2.8x/1.95x | vendor price | [CLAIM-tigergraph-09] |
| Friction | Closed source: no verifiable internals; no public optimiser/isolation spec | NOT PUBLICLY VERIFIED | n/a |
| Outdated | 2019 benchmark and unaudited large runs reused in marketing | vendor claim | [CLAIM-tigergraph-11] |
| Hypothesis | Strict schema-first conflicts with EOIP schema-flexible ingest | (H) | [CLAIM-tigergraph-02] NULLABLE support only in 4.3 preview |

Root causes: proprietary closed engine (governance/licensing); schema-first design (UX/deployment).

## 10. Deployment, licensing, redistribution, operational viability

Editions and terms (record, no legal conclusions): **Enterprise** under commercial licence (agreement updated 2026-03-05); **Enterprise Evaluation**; **Community Edition** (from 4.2): up to 300 GB combined graph+vector (4.2.0 initially 200 GB graph + 100 GB vector), single server, community-only support; licence grants internal use only, revocable at TigerGraph's discretion, forbids providing it to or using it on behalf of third parties, reproduction/distribution/derivatives, benchmark publication, and forbids use "in connection with" supported TigerGraph software [CLAIM-tigergraph-03][CLAIM-tigergraph-04]. **Savanna**: managed cloud, compute+storage billing, BYOC licence fee [CLAIM-tigergraph-09].

EOIP verdict inputs: CE cannot be bundled, resold or run for customers by a white-label vendor (third-party use and redistribution barred) => **legal-review trigger, likely blocker**; Enterprise OEM terms NOT PUBLICLY VERIFIED. Air-gap: self-managed server runs on-prem on Linux (Docker/bare metal/K8s), offline licence-key handling NOT PUBLICLY VERIFIED; Savanna is cloud-only and excluded. GraphRAG with Ollama local models is possible but AGPL-3.0 [CLAIM-tigergraph-10]. One-node: CE and EE both run single server; distributed is EE. Backend neutrality: would be an optional customer-licensed backend.

## 11. Competitive delta against the EOIP baseline

| Area | TigerGraph | EOIP baseline | Delta |
|---|---|---|---|
| Backend | proprietary MPP | BL-01..05 no TigerGraph adapter | adapter would use REST/GSQL; no OSS test target |
| Deep-hop analytics | native BSP engine | BL-43 pure Python, scale unmeasured (U-06) | large performance gap likely at scale; EOIP traverses in Python (BL-01) |
| Query | GSQL + Cypher/GQL patterns | BL-08/BL-10/BL-59 | EOIP has no GQL execution; TigerGraph covers a subset |
| Vector | native ANN | BL-14 Partial | gap on large corpora |
| GraphRAG | service (AGPL) | BL-16 deterministic | no benchmark either side |
| Security | RBAC, row policy, audit | BL-18 Absent, BL-19 Implemented | TigerGraph row policies = a pattern for fact-level ACL |
| Tenancy | multigraph (detail unread) | BL-20 Partial | UNVERIFIED |
| Ops | incremental backup, CRR | BL-50 scripts | match basics |
| Temporal/epistemic | none | BL-37, BL-40 Implemented | EOIP differentiator |

## 12. Strength-adoption and inversion cards

**INV-tigergraph-01** — Target TigerGraph DB 4.2.5 CE, white-label deployment. Limitation: CE licence bars third-party use, distribution, benchmark publication [CLAIM-tigergraph-04]. Root cause: licensing (proven). Alternative: EOIP keeps TigerGraph as customer-supplied backend only, never a bundled dependency, with its own analytics operators; worse when a customer demands TigerGraph-scale MPP. Options: (1) quick: adapter plus customer's own Enterprise licence; (2) native: accumulator operator on existing backends; (3) long-term: optional MPP engine (HugeGraph-Computer/Vermeer, see HugeGraph file) behind the same operator. Selected: (2) then (3). Sketch: `AggregatePlan{frontier, edge_types, depth_cap, monoid}` executed backend-natively when supported, else BSP in Python with spill. POC: 10M-edge synthetic dependency graph, 4-hop impact count; success within 3x of GSQL on the same hardware (needs customer licence for comparison and must not publish CE results). Failure case: unbounded depth on supernodes; apply bounds from BL-08. Defensibility: typed plans plus ACL-aware aggregation, not engine speed. Decision: EXPERIMENT.

**INV-tigergraph-02** — Target GraphRAG v2.0.4. Limitation: single-database lock-in (TigerGraph only), AGPL since v2.0.1, only hybrid search supported [CLAIM-tigergraph-10]. Root cause: licensing + coupling (proven). Alternative: EOIP's backend-neutral retrieval service (BL-16) with local models; worse where TigerGraph is already deployed. Options: (1) integrate unmodified as a separate network service (AGPL review); (2) native retrieval pipeline with benchmark vs BM25/dense/hybrid; (3) differentiated: ACL-aware, evidence-span GraphRAG with abstention. Selected: (2). POC: GraphRAG-Bench-style multi-hop set versus EOIP BL-16 and plain hybrid RAG; metric answer-F1 and citation precision; baselines measured locally. Decision: EXPERIMENT; REJECT embedding AGPL code.

**INV-tigergraph-03** — Target schema-first model. Limitation (hypothesis): rigid schema vs EOIP automatic schema inference from arbitrary JSON (BL-26). Root cause: data model (hypothesis; NULLABLE attributes only in preview 4.3). Alternative: EOIP infers a schema then applies it as a backend DDL migration with review. Decision: DEFER; test needs a live instance. Seed hypotheses in Master Prompt §10.5: none targets TigerGraph; "fixed vendor query languages via typed query plans plus adapters" is supported by GSQL's proprietary dialect.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-01/CAP-05 as backend | EXPERIMENT (customer-supplied adapter only) | licence blocks bundling |
| CAP-13/CAP-14 GSQL/openCypher | INTEGRATE Cypher subset if adapter built; REJECT GSQL as EOIP language | |
| CAP-18 optimisation/PROFILE | REFERENCE-ONLY | internals closed |
| CAP-19 multi-hop | BUILD accumulator operator | STR-01 |
| CAP-46 row-policy ACL | BUILD (EOIP) with TigerGraph row policy as pattern | BL-18 P0 |
| CAP-53 vector | INTEGRATE existing engines (C10 files); REJECT TigerGraph dependency | |
| CAP-56 GraphRAG | EXPERIMENT as baseline; REJECT embedding (AGPL, single DB) | |
| CAP-62 algorithms | REUSE OSS libraries (C12) | |
| CAP-74/CAP-76 incremental backup, CRR | BUILD basics via backend-neutral scripts | |
| CAP-77 licensing/TCO | legal review | |

## 14. Tests, POC, acceptance

1. Legal gate: obtain Enterprise OEM terms or declare "customer-supplied only"; acceptance, written decision.
2. Adapter conformance (needs customer or evaluation licence): run `graph/conformance.py` against TigerGraph via REST; acceptance, all required operations or documented gaps.
3. Accumulator POC (INV-01) on licensed instance, results kept private if under CE.
4. GraphRAG baseline experiment (INV-02) with local Ollama model; measure vs plain hybrid.
5. ACL canary through hybrid vector+graph query: zero leakage.

## 15. Risks, trade-offs, open research questions

Risks: licence (CE barred for OEM), closed internals prevent verification, AGPL GraphRAG, 4.3 preview changes (Kafka connector removal precedent). Open: Enterprise OEM and air-gap licence mechanics; exact CE feature exclusions; isolation level and consistency; multigraph tenancy isolation; Gremlin/SPARQL support; 4.3 GA date; full-text; real independent benchmark post-2022.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Proprietary, editions, active, LTS cadence |
| D2 | 2 | Deep-link analytics, GenAI |
| D3 | 4 | GSE/GPE/RESTPP, cluster |
| D4 | 5 | Layout NOT PUBLICLY VERIFIED; ANN vectors |
| D5 | 3,5 | Schema-first, multigraph; no ontology |
| D6 | 5 | GSQL BSP, Cypher/GQL patterns, plan cache; optimiser unknown |
| D7 | N/A | No reasoning engine |
| D8 | 5,7 | MPP shared-nothing, HA, CRR; ACID listed, details unverified |
| D9 | 3 | File/Kafka/Iceberg loaders; CDC output |
| D10 | N/A | No ER/evidence features |
| D11 | 5 | Backups only |
| D12 | 3 | Algorithm library; no ML detail read |
| D13 | 3,8 | Vector, GraphRAG |
| D14 | 3 | GraphRAG NL Q&A; accuracy not evaluated |
| D15 | N/A | Not examined |
| D16 | 3 | GraphStudio/Insights; not examined |
| D17 | 3 | GSQL, REST, drivers |
| D18 | 5,10 | RBAC, row policy, SSO, mTLS |
| D19 | 11 | Multigraph; detail unread |
| D20 | 7 | Vendor numbers only |
| D21 | 10 | Tiered licences, Savanna pricing |
| D22 | 9,11 | Proprietary GSQL; Cypher subset |
| D23 | N/A | No patent search done |
| D24 | App. C | Mixed official/vendor |

## Appendix B — Capability mapping

| CAP-ID | TigerGraph | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-tigergraph-07 | BL-01 | EXPERIMENT | P3 |
| CAP-05 | enterprise-only | CLAIM-tigergraph-08 | BL-02 | REUSE HugeGraph | P2 |
| CAP-08 | native (schema-first) | CLAIM-tigergraph-02 | BL-28 | REUSE EOIP | P2 |
| CAP-13 | absent/unknown | CLAIM-tigergraph-06 | BL-05 | n/a | P3 |
| CAP-14 | partial | CLAIM-tigergraph-06 | BL-03/BL-59 | INTEGRATE | P2 |
| CAP-18 | native (profiler) | CLAIM-tigergraph-12 | BL-08 | REFERENCE-ONLY | P3 |
| CAP-19 | native | CLAIM-tigergraph-07 | BL-43 | BUILD | P1 |
| CAP-45 | enterprise-only | CLAIM-tigergraph-08 | BL-19 | REUSE EOIP | P2 |
| CAP-46 | enterprise (row policy) | CLAIM-tigergraph-08 | BL-18 Absent | BUILD | P0 |
| CAP-47 | unknown | CLAIM-tigergraph-08 | BL-20 | EXPERIMENT | P1 |
| CAP-50 | partial | CLAIM-tigergraph-09 | BL-45 | legal review | P1 |
| CAP-52 | proprietary | CLAIM-tigergraph-04 | BL-21 | REJECT bundling | P1 |
| CAP-53 | native | CLAIM-tigergraph-05 | BL-14 | INTEGRATE alternatives | P2 |
| CAP-56 | plugin (AGPL) | CLAIM-tigergraph-10 | BL-16 | EXPERIMENT | P2 |
| CAP-62 | native | CLAIM-tigergraph-07 | BL-43 | REUSE OSS | P3 |
| CAP-74 | native | CLAIM-tigergraph-12 | BL-50 | BUILD | P2 |
| CAP-76 | enterprise | CLAIM-tigergraph-08 | BL-50 | DEFER | P3 |
| CAP-77 | proprietary | CLAIM-tigergraph-04 | n/a | legal | P1 |

## Appendix C — Evidence records (access 2026-10-26)

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-tigergraph-01 | DB 4.2.0-4.2.5 | Release dates and LTS flags (4.2.5 2026-09-02, 4.2.4 2026-07-20, 4.2.3 2026-06-05, 4.2.2 2025-09-30, 4.2.1 2025-09-05, 4.2.0 2025-04-03) | Officially documented | TigerGraph DB 4.2 Release Notes, tigergraph.com/docs/tigergraph-server/4.2/release-notes/ | 10-26 | 0.9 | sources differ on alpha date 2025-03-04 vs SIGMOD Dec 2024 integration |
| CLAIM-tigergraph-02 | 4.3.0-rc2 | rc1 2026-07-08, rc2 2026-10-20 preview; mTLS, Kerberos, NULLABLE, Iceberg preview, audit log, CRR commands | Officially documented | 4.3 Release Notes, tigergraph.com/docs/tigergraph-server/4.3/release-notes/ | 10-26 | 0.85 | none |
| CLAIM-tigergraph-03 | CE 4.2.x | CE single server; 200 GB graph + 100 GB vector at 4.2.0, 300 GB combined from 4.2.1; community-only support | Officially documented | 4.2 release notes (as above) | 10-26 | 0.85 | Atlan states 16 CPU cap: UNVERIFIED |
| CLAIM-tigergraph-04 | licence, updated 2026-03-05 | CE: internal use, revocable, no support/updates, no third-party use, no distribution/derivatives, no benchmark publication, 300 GB combined, no mixing with supported software | Officially documented | TigerGraph License Agreement, tigergraph.com/license-agreement/ | 2026-03-05 / 10-26 | 0.8 (summary via fetch tool, not full text read) | none |
| CLAIM-tigergraph-05 | 4.2 | VECTOR attribute, ANN with incremental index, hybrid GSQL, 4096 dims CE / 32768 EE; TigerVector (SIGMOD 2025) | Officially documented + paper | GSQL vector reference docs.tigergraph.com/gsql-ref/4.2/vector ; SIGMOD25_TigerVector.pdf | 2025 / 10-26 | 0.8 | none |
| CLAIM-tigergraph-06 | 4.2 | openCypher and GQL pattern matching in same execution engine; syntax V3; interpreted queries | Officially documented | Query Language Reference, tigergraph.com/docs/gsql-ref/4.2/intro/ ; 4.2 release notes | 10-26 | 0.8 | no conformance claim |
| CLAIM-tigergraph-07 | architecture | Native MPP; GSE/GPE; BSP/accumulator GSQL; ID translation; partition scheme not public | Third-party report + paper | arXiv:1901.08248 "TigerGraph: A Native MPP Graph Database"; dbdb.io; TigerGraph deep-dive deck info.tigergraph.com | 2019 / 10-26 | 0.6 | 2019-vintage; current internals unverified |
| CLAIM-tigergraph-08 | 4.2 docs | Docker, bare metal, K8s, cloud images; HA/region-aware (preview), CRR, repartition; RBAC, SSO, LDAP, row policies; Kafka loading; multigraph link | Officially documented | TigerGraph 4.2 intro, tigergraph.com/docs/tigergraph-server/4.2/intro/ | 10-26 | 0.8 | none |
| CLAIM-tigergraph-09 | Savanna | Usage-priced compute/storage, HA multipliers, BYOC licence fee; Classic customers transitioned | Officially documented | Savanna pricing docs, tigergraph.com/docs/savanna/main/overview/pricing | 10-26 | 0.7 | search results gave $45/GB-month and hourly rates inconsistently: UNVERIFIED |
| CLAIM-tigergraph-10 | graphrag v2.0.4 | AGPL-3.0 since v2.0.1 (2026-07-22), Apache-2.0 before; TigerGraph only; Ollama among providers; hybrid search officially supported; v2.0.4 2026-10-21 | Officially documented | github.com/tigergraph/graphrag | 10-26 | 0.85 | README lists provider sets inconsistently |
| CLAIM-tigergraph-11 | benchmarks | 100x claim from vendor-tuned UC Merced LDBC study; 1 TB LDBC audit; larger runs unaudited with modified queries | Independent benchmark (vendor-tuned) + vendor report | arXiv:1907.07405; tigergraph.com/benchmark | 2019, 2022 / 10-26 | 0.7 | none |
| CLAIM-tigergraph-12 | 4.2 | Incremental backup, rolling upgrade (preview), plan caching, profiler; Kafka connector removed; breaking changes | Officially documented | 4.2 release notes | 10-26 | 0.85 | none |

## Appendix D — Assumptions

A1: Internal architecture pages were unreachable; architecture from the 2019 paper, vendor deck and docs, flagged as such. A2: "Enterprise Free"-style edition names not found; only Community, Enterprise, Evaluation. A3: Licence terms are from a summarised fetch of the agreement; the full text must go to legal. A4: GSQL install-time compilation is a hypothesis. A5: Access date 2026-10-26.
