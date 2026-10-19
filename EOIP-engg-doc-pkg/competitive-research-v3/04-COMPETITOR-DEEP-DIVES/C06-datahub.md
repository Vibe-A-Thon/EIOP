| Field | Value |
|---|---|
| Registry ID | T-C06-datahub |
| Tier | B — OSS metadata graph; benchmark/reuse reference for EOIP catalog and lineage (CAP-40, CAP-42) |
| Versions examined | v1.7.0 (2026-08-04, stable); v1.7.0.1 (patch, date UNVERIFIED); v1.6.0.3 (2026-09-25, maintenance line); v1.8.0rc5 (2026-10-08, pre-release) |
| Verified on | 2026-10-18 |
| Worker | W15 |

# DataHub (datahub-project/datahub)

## 1. Identity, current status, tier, and sources

DataHub is an open-source metadata platform that started at LinkedIn. It is maintained at `github.com/datahub-project/datahub` with a commercial company behind it (formerly Acryl Data, now trading under the DataHub brand at datahub.com; the exact rebrand date was not verified) [CLAIM-datahub-01]. The core is licensed **Apache-2.0** [CLAIM-datahub-02]. The latest stable minor is **v1.7.0, released 2026-08-04**. A patch, v1.7.0.1, followed. A v1.6.0.x maintenance line is still patched (v1.6.0.3 on 2026-09-25), and **v1.8.0 is in release-candidate stage** (rc5 on 2026-10-08) [CLAIM-datahub-03][CLAIM-datahub-04]. The project is **active**. It releases a minor roughly every two months, with patch and RC tags in between. It is not archived.

Tier B: DataHub is the main open-source reference for a *metadata graph* (entities, aspects, typed relationships, change log). Its design patterns map directly onto EOIP CAP-42 (catalog and metadata management), CAP-40 (lineage), CAP-36 (event sourcing) and CAP-59 (MCP tools).

Sources: GitHub releases and tags; docs.datahub.com (architecture, components, metadata model, MCP/MCL, policies, graph-service migration, quickstart, releases, MCP feature guide, OpenLineage). All were accessed 2026-10-18 (Appendix C).

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** DataHub answers "what data exists, who owns it, where it came from and what breaks if it changes" across a modern data stack (warehouses, lakes, BI, orchestration, ML). It is **catalog search plus operational lineage**, not semantic inference.

- *Discovery:* a data analyst searches "revenue", filters by domain and tag, and opens a dataset page with schema, owners, glossary terms, usage statistics and documentation.
- *Impact analysis:* before dropping a column, an engineer opens column-level lineage downstream to dashboards and ML features [CLAIM-datahub-09].
- *Governance:* a steward applies glossary terms and a domain. Policies restrict who may edit tags or owners on assets in that domain [CLAIM-datahub-07].
- *Agent access:* an AI assistant calls the DataHub MCP server's `get_lineage` tool to explain downstream impact [CLAIM-datahub-10].

**Separation required by Master Prompt §6 C06:**

| Concern | DataHub position |
|---|---|
| Catalog search | Core feature. Elasticsearch/OpenSearch index. |
| Semantic inference | Absent. Glossary terms and term relationships exist, but there is no reasoning engine. |
| Operational lineage | Core feature. Dataset, job and column lineage come from SQL parsing, connectors and OpenLineage. |
| Knowledge intelligence | Partial. AI documentation and MCP are offered, with more in the commercial Cloud product (details NOT PUBLICLY VERIFIED). |

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Model | Schema-first PDL entity/aspect model, URNs, `@Relationship` edges | present | CLAIM-datahub-05 |
| Model | Versioned aspects (version 0 = latest), timeseries aspects | present | CLAIM-datahub-05 |
| Model | Metric and semantic-model entities, logical model editing (v1.7.0) | present | CLAIM-datahub-04 |
| Write path | MetadataChangeProposal → GMS → DB → MetadataChangeLog on Kafka | present | CLAIM-datahub-06 |
| Write path | CDC mode (MCLs generated from DB change events, commit order) | optional | CLAIM-datahub-06 |
| Storage | MySQL (relational primary), Elasticsearch, Kafka | present | CLAIM-datahub-08 |
| Graph index | Elasticsearch (default) or Neo4j | optional | CLAIM-datahub-11 |
| API | REST (Rest.li), GraphQL, Kafka Avro, Python/Java SDKs | present | CLAIM-datahub-08, -12 |
| Lineage | Table/column lineage from SQL parsing; OpenLineage REST endpoint; Spark listener | present | CLAIM-datahub-09 |
| Lineage | Data products in the lineage graph (v1.7.0) | present | CLAIM-datahub-04 |
| AuthZ | Platform and metadata policies; actor/resource/privilege; domain/tag/term/container filters | present | CLAIM-datahub-07 |
| AuthZ | Sub-resource `privilegeConstraints` | partial (experimental, API-only) | CLAIM-datahub-07 |
| AuthZ | Search-result filtering / Search Access Controls | enterprise-only (DataHub Cloud) | CLAIM-datahub-07 |
| AuthZ | Inheritance of *source-system* data ACLs onto metadata | absent / unknown | none found; reasoned (CLAIM-datahub-14) |
| AI | MCP server with lineage, search and entity tools | present | CLAIM-datahub-10 |
| Semantics | OWL/RDFS reasoning, SHACL | absent | reasoned from the docs inventory |
| Tenancy | Multi-tenant isolation inside one deployment | absent (one deployment per organisation) / unknown | CLAIM-datahub-14 |
| UI | React web app: search, entity pages, lineage visualisation | present | CLAIM-datahub-08 |

## 4. Text-based architecture diagram

```
 Sources (Snowflake, BigQuery, dbt, Airflow 3+, Spark, Looker, Kafka ...)
   |  pull: Python ingestion framework (recipes)      push: SDK / REST / Kafka / OpenLineage REST
   v                                                    v
 +------------------------ Metadata Change Proposal (MCP, Avro) -------------------------+
 |  Kafka topic MetadataChangeProposal_v1  -->  GMS (Spring/Rest.li, metadata service)  |
 |                                               | validate against PDL aspect schema    |
 |                                               v                                       |
 |                    MySQL/Postgres: versioned aspect rows (urn, aspect, version)       |  <- system of record
 |                                               | after commit (or via CDC)             |
 |                                               v                                       |
 |  Kafka MetadataChangeLog_Versioned_v1 (7d) / _Timeseries_v1 (90d)  (prev + new value) |
 +-----------------------------------------------+---------------------------------------+
                                                 v  MCL processor(s)
             +----------------------+------------------------+--------------------+
             v                      v                        v                    v
   Search index (ES/OS)    Graph index (ES or Neo4j)   Timeseries index (ES)   Actions/webhooks
             +--------------+-------+------------------------+
                            v
              GraphQL API  <-- React UI, MCP server, SDKs
 Control plane: policies (cached; ~120 s propagation), auth (OIDC/JAAS), ingestion scheduler
```

## 5. Under-the-hood reconstruction

**Data model.** Each entity is identified by a URN serialised from its key aspect (`urn:li:corpuser:johnsmith`). Its state is a set of independently writable aspects, each validated against one PDL schema. A relationship is a foreign-key field inside an aspect annotated `@Relationship`, so edges are *derived from aspect content*: the graph index is a projection, not the source of truth [CLAIM-datahub-05].

**Storage layout.** The relational store holds one row per (urn, aspect, version). Version 0 is the latest, and older versions are kept when fields change. Timeseries aspects (profiles, usage) are **not** stored in the relational store. They live in the search index and on Kafka, and the docs warn that this makes disaster recovery harder [CLAIM-datahub-05].

**Write pipeline (event-sourced projection).**
```
on MCP(urn, aspect, value):
    schema.validate(aspect, value)                      # PDL
    prev = db.latest(urn, aspect)
    if value != prev: db.insert_version(urn, aspect, value)   # transactional
    kafka.emit(MCL{urn, aspect, new=value, previous=prev, systemMetadata})
on MCL:
    search_index.upsert(urn, aspect)                    # async by default
    graph_index.diff_edges(prev.relationships, new.relationships)
```
The previous value is carried in the MCL so that index processors can compute edge diffs [CLAIM-datahub-06]. In CDC mode the MCL order matches the database commit order [CLAIM-datahub-06].

**Query and lineage.** Lineage traversal is served by the graph index (Elasticsearch by default, Neo4j optional), with search through Elasticsearch [CLAIM-datahub-11]. *Hypothesis:* multi-hop lineage on the Elasticsearch graph backend is iterative per-hop lookups rather than a native traversal engine. That would explain why Neo4j is offered for heavier graph use. Not verified at code level in this run.

**Reasoning.** None. Glossary-term relationships are stored, not inferred.

**Concurrency and consistency.** The relational write is the commit point. Indices are eventually consistent: Elasticsearch writes are asynchronous by default [CLAIM-datahub-06].

**Versioning.** Aspect version history and the MCL stream exist. There is no branch/merge and no valid-time model (transaction-time-like history only).

**Security.** Grant-only, first-match-wins policies over actors, privileges and resource filters [CLAIM-datahub-07]. Policies govern *metadata* actions, not the underlying data rows. v1.7.0.1 removed a hardcoded system client secret default [CLAIM-datahub-04], which shows that secure defaults have historically lagged.

## 6. Functional and non-functional requirements inferred

- FR: every metadata write is a typed, schema-validated aspect proposal. Edges are derived from aspect fields.
- FR: lineage at dataset, job, column and data-product granularity, with OpenLineage intake.
- FR: policies scoped by domain, container, tag and glossary term, inherited recursively for domains and containers.
- NFR: indices can be rebuilt from the system of record (the RestoreIndices job) [CLAIM-datahub-11].
- NFR: single-host quickstart tested on 2 CPU / 8 GB RAM / 2 GB swap [CLAIM-datahub-13]. Production uses Kubernetes and Helm.

## 7. Performance and resource model

- Vendor claim: "Proven to 10M+ assets and O(1B) relationships" in production [CLAIM-datahub-12]. No hardware, workload or latency figures are given. Treat as **Unverified**.
- Footprint: at least three stateful services (relational DB, Elasticsearch/OpenSearch, Kafka), plus optional Neo4j, GMS, frontend and consumers. The quickstart needs about 8 GB RAM; out-of-memory kills (exit 137) are a known failure mode with less [CLAIM-datahub-13].
- Failure modes: index lag behind the DB (asynchronous); timeseries aspects lost if Elasticsearch and Kafka are lost (90-day retention is the replay window) [CLAIM-datahub-05][CLAIM-datahub-06]; policy changes take about 120 s to propagate [CLAIM-datahub-07].
- No independent benchmark was found. Proposed: BM-C06-01 (§14).

## 8. Strengths and how to match or exceed them

1. **Event-sourced metadata change log with previous and new value.** EOIP's SourceEvent v2 + replay (BL-23, BL-24) is similar at ingest but has no external bus (BL-60). Match by emitting a graph *mutation log* with before and after images from the mutation gateway. Exceed with bitemporal validity (BL-37), which DataHub lacks.
2. **Schema-first aspect model.** Aspects are small, independently writable units, so connectors and humans can own different aspects of one entity without clobbering each other. EOIP's `catalog/layered_metadata.py` (base, edit and merged layers) follows the same idea. Match with per-aspect ownership and precedence.
3. **Pluggable graph index (Elasticsearch or Neo4j).** This shows the pattern "system of record + rebuildable graph projection", which matches EOIP's backend neutrality (BL-01).
4. **Broad connector ecosystem and OpenLineage intake.** INTEGRATE rather than rebuild: ingest DataHub as a source of data-asset metadata (EOIP already has projection code in `catalog/projections.py`).

## 9. Limitations with root causes

| Type | Limitation | Root cause | Class |
|---|---|---|---|
| Intentional trade-off | No reasoning, constraints or ontology semantics beyond the glossary | Catalog scope | algorithmic scope (design) |
| Verified (docs) | Policies are grant-only first-match. Search filtering is Cloud-only. Sub-resource constraints are experimental [CLAIM-datahub-07] | Policies attach to metadata entities, not data-level ACLs | user/developer friction; licensing split |
| Verified (docs) | Timeseries aspects only in Elasticsearch and Kafka, so disaster recovery is harder [CLAIM-datahub-05] | Storage optimisation | operational overhead |
| Verified (docs) | Several stateful services; 8 GB minimum for quickstart [CLAIM-datahub-13] | Kafka + Elasticsearch + RDBMS architecture | operational and hardware overhead |
| Verified (release notes) | Breaking upgrades (Airflow 3+ required, classifier removed) [CLAIM-datahub-04] | Fast release cadence | developer friction |
| Hypothesis | Deep lineage traversal on the Elasticsearch graph backend degrades for very large fan-out | Per-hop index lookups | algorithmic |
| Hypothesis | No tenant isolation inside a deployment | One organisation per deployment | deployment |

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

Apache-2.0 core: redistribution, embedding and OEM use are permitted subject to NOTICE and attribution. There is no copyleft trigger for the core [CLAIM-datahub-02]. Community-versus-enterprise split: DataHub Cloud adds features such as search access controls [CLAIM-datahub-07]. **Legal-review trigger: false for the OSS core**, but check bundled dependencies before redistribution. Neo4j Community is GPLv3 if the optional Neo4j graph backend is chosen, and Elasticsearch's licence terms differ from OpenSearch's. DataHub can be self-hosted with Docker or Helm and runs air-gapped once images are mirrored (no mandatory cloud call was found; *reasoned*). Fit as an EOIP dependency: **INTEGRATE as a source and target catalog**, not as EOIP's internal store. Embedding it would add Kafka, Elasticsearch and an RDBMS to the one-node footprint, and it lacks source-ACL semantics.

## 11. Competitive delta against the EOIP verified baseline

| Topic | DataHub | EOIP baseline |
|---|---|---|
| Metadata model | PDL aspects, URNs, derived edges [CLAIM-datahub-05] | Fixed LPG label manifest; canonical IDs; revisions (BL-01, BL-37) |
| Change log | Kafka MCL with before/after [CLAIM-datahub-06] | SourceEvent log + replay + DLQ (BL-23, BL-24); no external bus (BL-60) |
| Lineage | Column-level from SQL parsing, OpenLineage [CLAIM-datahub-09] | Evidence lineage (BL-41); regex-based SQL lineage parser that emits UNCERTAIN for dynamic SQL, plus an OpenLineage mapping (`catalog/lineage_parser.py`, `future_scope.py:622`) [CLAIM-datahub-15] — Partial, not in the baseline inventory |
| Permissions | Metadata policies [CLAIM-datahub-07] | API RBAC/ABAC (BL-19); **source-ACL enforcement Absent (BL-18)** |
| Temporal | Transaction-time aspect versions | Bitemporal (BL-37), diff and playback (BL-38) — EOIP ahead |
| Truth | None | Claims and contradictions (BL-39), epistemic separation (BL-40) — EOIP ahead |
| MCP | Lineage/search tools [CLAIM-datahub-10] | 18 read-oriented tools (BL-47) — parity |
| Ecosystem | Large connector catalogue (vendor; count not verified) | 30+ IT-centric connectors (BL-23) — DataHub ahead for data-stack sources |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-datahub-01** | DataHub | Event-sourced metadata change log with previous and new value, consumed by rebuildable indices | CLAIM-datahub-06, -11 | Customers can rebuild search, graph and vector indices from one log after corruption or a backend switch, and get audit and replay | match | Mutation gateway emits `GraphMutationLogged{before, after, actor, evidence, tenant}` to a pluggable log (file/SQLite on one node; Kafka/NATS later). Every index (BM25, vector, backend graph) is a checkpointed consumer. | Delete all derived indices and rebuild from the log; query results identical on a 1M-edge fixture; rebuild time recorded.

**STR-datahub-02** | DataHub | Aspect-granular ownership of entity state (connectors and humans write different aspects) | CLAIM-datahub-05 | Human curation survives connector re-syncs | match (EOIP partial in `catalog/layered_metadata.py`) | Promote base/edit/merged layers into a general aspect-precedence contract on every vertex type | Re-run a connector after a human edit: the edit persists, and source drift raises a conflict record (J2).

**STR-datahub-03** | DataHub | OpenLineage intake and column-level lineage | CLAIM-datahub-09 | Data-platform customers already emit OpenLineage | integrate | OpenLineage HTTP receiver → SourceEvent v2 → mapping → governed mutation (connectors never write the graph) | Replay the OpenLineage spec examples; column edges match the expected set; duplicate events are idempotent (J7).

**INV-datahub-01 — Metadata permissions are not source-data permissions**
- Target: DataHub v1.7.0 OSS. Workload: permission-aware discovery and agent answers.
- Limitation (evidence): grant-only, first-match policies on metadata actions. Search-result filtering requires DataHub Cloud. Sub-resource constraints are experimental [CLAIM-datahub-07]. No documented import of source-system ACLs as visibility constraints [CLAIM-datahub-14].
- Root cause: governance (*proven* from the docs), because policies attach to catalog entities and roles. Data model (*hypothesis*): visibility is not a property carried on every edge and aspect.
- Why an alternative mitigates it: carrying `acl_hash`/principal sets from source capture (BL-17) through to every retrievable unit lets search, lineage, GraphRAG and MCP filter consistently. *Worse when* source ACLs are unavailable or extremely high-cardinality: ACL expansion costs time, and the index grows.
- Options: (1) Quick: post-filter results by calling source systems at query time. (2) Pragmatic: principal-set tags on vertices and edges plus filter pushdown in the QueryPlan executor and retrieval. (3) Long-term: a ReBAC graph (Zanzibar-style) co-indexed with knowledge, with revocation propagated to caches and agent memory.
- Selected: (2) now, designed toward (3).
  ```
  principals = authz.expand(user)                        # user, groups, roles, tenant
  results = executor.run(plan, visibility=lambda e: e.acl & principals)
  answer  = synthesise(results)   # only visible evidence; abstain if insufficient
  ```
- Benchmark/POC: J5 with two users and a 100k-asset fixture, 10% restricted. Success means zero restricted items in search, lineage, answers and MCP, with p95 overhead ≤ 20% versus unfiltered. Baseline cost: one node, 16 GB RAM.
- Dependencies and failure cases: this fixes EOIP **BL-18 (Absent, P0)**. Failure cases: stale ACL caches after revocation; lineage that reveals the existence of hidden assets (needs "redacted node" semantics); principal namespaces that must be per tenant (J13).
- Defensibility: permission-correct answers across *all* surfaces (search, graph, GraphRAG, agents) need end-to-end design. A catalog that copies only search filtering still leaks through lineage and agents.
- Decision: **ADOPT** (P0). This is the same gap as the EOIP self-inversion for BL-18.

Seed hypotheses (§10.5): none targets DataHub directly. The "typed constraints in our mutation gateway" direction (Neo4j seed) applies by analogy: DataHub validates aspect *shape* (PDL), not semantic constraints. EOIP should keep semantic validation in its gateway (BL-28).

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-42 catalog and metadata management | INTEGRATE (DataHub as source/target) + BUILD the aspect-precedence contract | Do not embed DataHub as EOIP's internal store |
| CAP-40 lineage | INTEGRATE OpenLineage intake; BUILD a replacement for the regex SQL lineage parser using a maintained SQL parser library (licence check) | Benchmark against DataHub column lineage |
| CAP-36 event sourcing | BUILD (match STR-datahub-01) | |
| CAP-46 source-ACL enforcement | BUILD (INV-datahub-01) | P0 |
| CAP-59 MCP tools | BUILD (match): add a `get_lineage`-style tool | |
| CAP-17 GraphQL | DEFER | DataHub proves value for UI aggregation; EOIP BL-58 Absent |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

- **POC-DH-1 (federation):** ingest a DataHub v1.7.0 instance through its GraphQL/REST API into EOIP SourceEvents. Accept when datasets, schema fields, owners, glossary terms and lineage edges round-trip with stable IDs, and deletes in DataHub produce tombstones (BL-25).
- **BM-C06-01 (lineage depth):** 10k datasets and 200k column edges. Compare EOIP's 5-hop downstream impact query (HugeGraph backend versus in-process) with DataHub (Elasticsearch graph and Neo4j graph). Report p50/p95 latency and correctness against a gold set.
- **T-DH-ACL:** the J5 permission test in INV-datahub-01.
- **T-DH-REBUILD:** the STR-datahub-01 acceptance test.

## 15. Risks, trade-offs, and open research questions

- Risk: copying the Kafka + Elasticsearch + RDBMS stack would break the one-node-first rule. Use a pluggable log instead.
- Open: Neo4j versus Elasticsearch graph-index lineage performance (no public benchmark found).
- Open: which DataHub Cloud features are missing from OSS beyond search access control (NOT PUBLICLY VERIFIED).
- Open: the release date of v1.7.0.1 and the v1.8.0 GA date.

## Appendix A. Research-dimension coverage

| Dimension | Covered in | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Apache-2.0, active, v1.7.0 (2026-08-04), v1.8 RC |
| D2 Problem and workloads | 2 | Data-stack discovery, lineage, governance |
| D3 Architecture | 4, 5 | GMS, Kafka MCP/MCL, RDBMS, ES/OS, graph index |
| D4 Storage and indexing | 5 | Versioned aspect rows; ES search; ES or Neo4j graph |
| D5 Schema and semantics | 3, 5 | PDL schema-first; no OWL/SHACL |
| D6 Query pipeline | 5 | GraphQL/REST; search plus graph index; no user query language |
| D7 Reasoning | 5 | None |
| D8 Transactions and scale | 5, 7 | DB commit, async indices; vendor 10M+ assets claim |
| D9 Ingestion and federation | 2, 3 | Pull recipes, push SDK/Kafka, OpenLineage |
| D10 Identity and evidence | 5 | URN keys; no ER; no evidence spans |
| D11 Time and evolution | 5 | Aspect versions; MCL; no valid time |
| D12 Graph algorithms and ML | — | N/A: not offered in OSS beyond lineage traversal |
| D13 Retrieval and agents | 3 | MCP server with lineage tools |
| D14 NL querying | — | N/A for OSS core (Cloud AI features NOT PUBLICLY VERIFIED) |
| D15 Governance and authoring | 3, 5 | Glossary, domains, policies; no ontology workflow |
| D16 Human experience | 3 | React UI, lineage visualisation |
| D17 Developer experience | 3 | SDKs, GraphQL, ingestion framework |
| D18 Trust and security | 5, 9 | Policies; secure-default fix in v1.7.0.1 |
| D19 Multi-tenancy | 3, 9 | No intra-deployment tenancy (hypothesis) |
| D20 Economics | 7 | 2 CPU / 8 GB quickstart; multiple stateful services |
| D21 Commercial | 10 | OSS plus DataHub Cloud |
| D22 Interoperability | 8, 14 | OpenLineage, APIs; EOIP projection code exists |
| D23 IP and prior art | 15 | No patents reviewed; Apache-2.0 includes a patent grant |
| D24 Research quality | App. C | Official docs plus release pages; no independent benchmarks |

## Appendix B. Capability mapping

| CAP-ID | DataHub | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-42 | native | CLAIM-datahub-05, -08 | `catalog/*` Partial (not baselined); BL-41 Implemented | INTEGRATE + BUILD | P1 |
| CAP-40 | native | CLAIM-datahub-09 | BL-41 Implemented (evidence lineage); SQL lineage Partial | INTEGRATE + BUILD | P1 |
| CAP-36 | native (transaction-time) | CLAIM-datahub-06 | BL-37 Implemented, BL-60 Absent | BUILD | P1 |
| CAP-45 | native (metadata actions) | CLAIM-datahub-07 | BL-19 Implemented | BUILD (match) | P2 |
| CAP-46 | enterprise-only/absent | CLAIM-datahub-07 | BL-18 Absent | BUILD | P0 |
| CAP-59 | native | CLAIM-datahub-10 | BL-47 Implemented | BUILD (match) | P2 |
| CAP-17 | native | CLAIM-datahub-08 | BL-58 Absent | DEFER | P3 |
| CAP-26 | native | CLAIM-datahub-09 | BL-23 Implemented | INTEGRATE | P2 |
| CAP-47 | absent (hypothesis) | CLAIM-datahub-14 | BL-20 Partial | BUILD (EOIP's own) | P0 |

## Appendix C. Evidence records

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source | Pub / access | Confidence | Contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-datahub-01 | DataHub company | The commercial company, formerly Acryl Data, now publishes under the datahub.com brand | Third-party report | Search results incl. datahub.com post "A Control Plane for Data, and a New Era for Acryl" https://datahub.com/?p=2753 | n.d. / 2026-10-18 | 0.5 — rebrand text not read | none |
| CLAIM-datahub-02 | DataHub master | Licence is Apache License 2.0 | Observed in source code (LICENSE) | https://raw.githubusercontent.com/datahub-project/datahub/master/LICENSE | — / 2026-10-18 | 0.95 | none |
| CLAIM-datahub-03 | v1.8.0rc5, v1.6.0.3 | v1.8.0rc5 pre-release 2026-10-08; v1.6.0.3 2026-09-25 | Officially documented | GitHub tags https://github.com/datahub-project/datahub/tags | 2026-10-08 / 2026-10-18 | 0.85 | none |
| CLAIM-datahub-04 | v1.7.0 / v1.7.0.1 | v1.7.0 released 2026-08-04; adds metric and semantic-model entities and data products in lineage; drops Airflow 2; v1.7.0.1 tightens authorisation and removes the hardcoded system client secret default | Officially documented | DataHub Releases https://docs.datahub.com/docs/releases ; mirror https://newreleases.io/project/github/datahub-project/datahub/release/v1.7.0.1 | 2026-08 / 2026-10-18 | 0.75 — release table read via search summary | v1.7.0.1 date not confirmed |
| CLAIM-datahub-05 | docs current | Schema-first PDL; entity is the primary node, identified by a URN; aspects are the smallest atomic unit of write; relationships via `@Relationship` foreign keys; versioned aspects (version 0 latest); timeseries aspects not stored in the relational store, which complicates DR | Officially documented | Metadata model https://docs.datahub.com/docs/metadata-modeling/metadata-model | — / 2026-10-18 | 0.85 | none |
| CLAIM-datahub-06 | docs current | MCPs go to MetadataChangeProposal_v1 and are ingested asynchronously; GMS emits MCLs after the DB write; the MCL carries the previous value; versioned MCL topic has 7-day and timeseries topic 90-day retention; CDC mode keeps commit order; ES writes are async | Officially documented | MCP/MCL https://docs.datahub.com/docs/advanced/mcp-mcl | — / 2026-10-18 | 0.85 | none |
| CLAIM-datahub-07 | docs current | Platform vs metadata policies; grant-only first-match; filters by type, URN, tag, domain, container, term; privilegeConstraints experimental and API-only; search access controls require DataHub Cloud; ~120 s propagation | Officially documented | Policies https://docs.datahub.com/docs/authorization/policies | — / 2026-10-18 | 0.85 | none |
| CLAIM-datahub-08 | docs current | Metadata store is a Spring Java service with Rest.li endpoints using MySQL, Elasticsearch and Kafka; GraphQL API; React UI | Officially documented | Components https://docs.datahub.com/docs/components | — / 2026-10-18 | 0.8 | Postgres/OpenSearch support exists per other docs (not re-verified) |
| CLAIM-datahub-09 | v1.3+ docs | REST endpoint accepts OpenLineage events; Spark listener with column-level lineage; column lineage from SQL parsing | Officially documented | https://archive.docs.datahub.com/docs/1.3.0/lineage/openlineage ; https://solutions.datahub.com/lp/enterprise-data-lineage-software | — / 2026-10-18 | 0.75 | none |
| CLAIM-datahub-10 | docs current | MCP server exposes tools incl. `get_lineage` for datasets, columns, dashboards | Officially documented | https://docs.datahub.com/docs/features/feature-guides/mcp | — / 2026-10-18 | 0.75 | none |
| CLAIM-datahub-11 | docs current | Graph service supports Elasticsearch or Neo4j; ES recommended for lighter deployments; RestoreIndices rebuilds the graph index | Officially documented | https://docs.datahub.com/docs/how/migrating-graph-service-implementation | — / 2026-10-18 | 0.8 | none |
| CLAIM-datahub-12 | docs current | "Proven to 10M+ assets and O(1B) relationships" | Unverified (vendor claim, no workload/hardware) | Architecture https://docs.datahub.com/docs/architecture/architecture | — / 2026-10-18 | 0.3 | none |
| CLAIM-datahub-13 | quickstart | Tested config 2 CPUs, 8 GB RAM, 2 GB swap | Officially documented | https://datahubproject.io/docs/quickstart | — / 2026-10-18 | 0.75 | A DataHub support article recommends 4 CPU / 8 GB / 20 GB disk |
| CLAIM-datahub-14 | v1.7.0 | No documented intra-deployment tenant isolation and no import of source-system data ACLs | Reasoned inference (absent from the docs read) | Docs listed above | — / 2026-10-18 | 0.4 | DataHub Cloud may differ |
| CLAIM-datahub-15 | EOIP HEAD ad9937b | EOIP has `catalog/lineage_parser.py` (regex SQL lineage; UNCERTAIN for dynamic SQL), `catalog/projections.py` (to_openmetadata, to_datahub, to_apache_atlas) and an OpenLineage mapping in `future_scope.py:622` | Observed in source code | `packages/eoip/catalog/*.py`, `packages/eoip/future_scope.py` | — / 2026-10-18 | 0.85 — static read; tests exist (`tests/semantic/test_catalog_lineage_context.py`) but were not run by W15 | Not in the 01-SYSTEM-BASELINE inventory |

## Appendix D. Assumptions

1. "DataHub" means the LinkedIn-origin `datahub-project/datahub` project, not unrelated products with the same name (e.g. Raynet DataHub, Skycatch DataHub).
2. The latest *stable* release is v1.7.0/v1.7.0.1. v1.6.0.3 is a maintenance backport, and v1.8.0 is RC only.
3. DataHub Cloud internals are described only where the OSS docs say a feature is Cloud-only.
4. EOIP status for the `catalog/` module comes from W15's static read, not from the coordinator baseline.
