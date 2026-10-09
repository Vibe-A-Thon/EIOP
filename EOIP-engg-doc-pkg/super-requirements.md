# SUPER-REQUIREMENTS — Commercial, White-Label, Local-First Enterprise Ontology & Intelligence Platform ("Living Organizational Brain")

| Field | Value |
| --- | --- |
| Document type | Master product requirements baseline (supersedes the "Enhanced Unified Super-Prompt" and builds on `consolidated-requirements.md` for the EOIP / KnowGridFlow codebase) |
| Generated | 2026-10-08 |
| Audience | Product owner, architects, engineering teams, coding/AI agents, security & compliance reviewers, sales engineering |
| Status | Baseline v1.0 — requirements are normative; "Proposal" marks anything that needs an owner decision or benchmark before commitment |
| Working product name | "the Platform" (white-label placeholder; EOIP / KnowGridFlow is the engineering lineage) |

---

## 0. How to Read and Use This Document

**Normative language.** MUST / MUST NOT = release-blocking for the stated priority. SHOULD = expected unless an ADR records why not. MAY = optional.

**Priorities.** `P0` = required for the first commercial GA. `P1` = within two releases after GA. `P2` = planned, not committed. `P3` = horizon / research.

**Requirement IDs.** `SR-<AREA>-<nnn>`. Areas: VIS, CON, ARC, GDB, VDB, QRY, ING, ONT, RAG, NLQ, LLM, AGT, TEN, WL, CFG, EXT, UX, SEC, PRV, GOV, NFR, OPS, DEP, QA, COM. Each `SR-` ID MUST be traced to at least one behavioral test (see §17.3) before it may be called "Done".

**Evidence tiers (inherited lesson).** The prior audit found that "Done" counts produced by an ID-string-matching gate were not behavioral proof (113 of 296 gap IDs were satisfied only by docstring name-dropping). Therefore in this baseline: `Done` = behavior verified by an executable acceptance test that fails when the behavior is broken; `Exists` = code present, not behaviorally verified; `External gate` = needs customer infrastructure, real tenants, hardware, or independent review.

**What changed versus the source files.** The Super-Prompt fixed HugeGraph as the only mandatory store, "NO CLOUD SERVICES", and "no RBAC in MVP". The new commercial brief requires many graph/vector backends, optional cloud enablement, white-label multi-tenancy, and configurable external-LLM sharing. §2 resolves every conflict explicitly.

---

## 1. Enhanced Mission Brief (the enhanced prompt, in normative form)

**Mission.** Build and sell a **fully customizable, white-label, multi-tenant, local-first Enterprise Ontology & Intelligence Platform** that:

1. **Ingests** data from any system (JSON as the canonical interchange, plus CSV/XML/Parquet/Avro/Office/PDF/logs/DB/CDC/API/streams/RDF).
2. **Understands** the data: profiles it, detects entities, keys, hierarchies and relationships, resolves identities, aligns it to an ontology, and **constructs** instance graphs, meta-graphs, relationship graphs, provenance/lineage graphs, temporal graphs and similarity graphs — optimized so storage and retrieval are fast.
3. **Stores** it in the customer's choice of graph database(s), vector store(s), search index and relational/object stores, behind adapters — default stack fully self-contained and on-premises.
4. **Answers** questions in natural language — deterministic ("who changed class X in API Y?") and exploratory/non-deterministic ("where should I troubleshoot incident INC-123?") — with evidence, explanations, ranked hypotheses, suggested queries the user can pick and fire, and long-form reports at LLM-grade depth.
5. **Acts** as a living organizational brain: continuously synchronizing, detecting change and drift, scoring freshness, alerting, simulating "what-if", and exposing governed tools to AI agents (MCP/API).
6. **Protects** the customer: no enterprise data leaves the customer boundary unless the customer explicitly enables an external endpoint and configures **which data types, at which sharing level, to which endpoint, for which tasks, for which users**.
7. **Sells** to nearly any organization (IT and non-IT): white-labelable, multi-tenant, modular SKUs, industry packs, partner/OEM program, offline licensing.

**Design stance.** (a) *Deterministic first, LLM optional* — every core function works with no LLM; LLMs augment, never gate. (b) *Evidence or it didn't happen* — every answer, edge and claim carries provenance, method and confidence. (c) *Everything is configuration* — behavior is policy-as-data, layered per edition/partner/tenant/workspace/user. (d) *Adapters everywhere* — graph DB, vector DB, query language, model, IdP, storage, bus are all ports with swappable adapters.

### 1.1 Personas

| Persona | Primary jobs | Typical questions |
| --- | --- | --- |
| Executive / Business leader | Risk, cost, capability overview | "Which business capabilities depend on the legacy billing system?" |
| Enterprise / solution architect | Impact, dependency, target-state | "What breaks if we retire service S?" |
| Engineer / SRE / DevOps | Change, incident, ownership | "Which class caused this incident?" |
| Security & compliance officer | Access, data flow, evidence | "Which systems hold PII and who can reach them?" |
| Data steward / ontologist | Model quality, vocabulary | "Which fields lack a mapped concept?" |
| Analyst / operations manager | Insight, reporting | "Summarize supplier risk by region" |
| Auditor | Traceability, immutable evidence | "Show lineage of this reported figure" |
| Tenant administrator | Users, connectors, policies, branding | "Disable external LLM for the finance workspace" |
| Platform operator / partner / reseller | Fleet, licensing, white-label | "Provision a branded tenant for customer X" |
| Integrator / developer | Connectors, plugins, API | "Add a connector for system Z" |
| AI agent (machine principal) | Governed tool use | MCP/API calls under least privilege |

### 1.2 Question taxonomy the NL layer MUST classify and serve

Lookup · traversal · shortest/all paths · impact / blast radius · root-cause · ownership / expertise · change history ("who changed") · coverage / gap · comparison · temporal / as-of · what-if / simulation · aggregation / analytics · similarity / recommendation · policy / compliance check · summarization / report · explain-why.

### 1.3 Canonical question patterns (from the brief) and required behavior

| # | Question | Required graph pattern and reasoning | Required output |
| --- | --- | --- | --- |
| Q1 | "What systems are impacted if I change / update / delete service account `abc`?" | Resolve `ServiceAccount` (alias-aware) → forward dependency traversal over credential, identity, secret, role, job, pipeline, API and deployment edges. Operation-aware: delete, rotate, permission-change and rename activate different edge sets. Direct vs transitive, environment- and criticality-weighted. | Ranked blast-radius list with path evidence per item, owners to notify, inferred-vs-asserted edge flags, coverage warning for non-ingested sources, rollout/test suggestions |
| Q2 | "Who made changes to class `X` in API `Y`?" | Class → File → Commit / MergeRequest → Person, window-aware, identity-resolved aliases, linked stories | Timeline, top contributors, reviewers, linked tickets, current owner |
| Q3 | "What systems must change to implement feature `F`?" | Feature/Epic text → semantic + graph-neighborhood match to components; co-change coupling from history; consumers of touched contracts (APIs, schemas, topics, jobs) | Proposed change-set with confidence per component, consumers, schemas, infra, docs, tests, owners, risks |
| Q4 | "What must I test when rule `R` is added / updated / deleted?" | Rule → consumers → `TESTS`/coverage edges → historical failure correlation | Prioritized test list with justification, untested-consumer gaps |
| Q5 | "For incident `INC-n`: what is impacted, where do I troubleshoot, which class caused it?" | Incident → affected service → time-window correlation with deploys, config changes, alerts, logs, traces → topology neighbors → stack-trace-to-symbol → last-modified commit/author; similar past incidents and resolutions | Ranked root-cause hypotheses with evidence, next diagnostic steps, runbooks, impacted-service list |

The same engine MUST serve non-IT equivalents (see §19: drug-recall lot tracing, supplier-nonconformance impact, contract-clause exposure, regulation-to-control mapping, outage-to-customer impact, curriculum prerequisite chains).

---

## 2. Reconciliation of Source Documents (binding decisions)

| # | Conflict in the sources | Resolution adopted in this baseline |
| --- | --- | --- |
| C1 | "HugeGraph is the only mandatory DB" (Super-Prompt; docs 07/08) vs multi-backend (consolidated doc: `06-architecture`, `76-multi-backend`, `FR-GRAPH-011/012`) | **Multi-backend wins.** Apache HugeGraph is the *default bundled* backend for local/on-prem profiles; all graph access goes through the Graph Store Port (§5). Backends are certified by tier. |
| C2 | "NO CLOUD SERVICES" vs "cloud enablement on client request" | **Cloud-free by default, cloud-capable by configuration.** Default profiles DP-0/DP-1 require zero cloud services and enforce it at the network layer. Cloud services are enabled per capability through declared-data-flow plugins (§3.3). |
| C3 | "No RBAC in MVP; URL separation is not authorization" vs multi-tenant commercial sale | **RBAC/ABAC/ReBAC and tenant isolation are P0 for commercial GA.** A demo build may run single-user, but every API, query, job and agent call MUST carry a principal and tenant context from day one (no retrofits). URL separation remains explicitly *not* an authorization boundary. |
| C4 | "External LLMs disabled" vs configurable sharing | Disabled by default (Level L0). Enabling requires an explicit, audited, per-tenant policy (§10). |
| C5 | "Vector DB not mandatory" vs "support various vector DBs" | Embedded vector index ships by default; external vector stores are adapters (§5.4). A deployment with no vector store MUST still work (graph + full-text retrieval). |
| C6 | "Gremlin as primary query language" vs "multiple graph and data query languages" | Introduce a backend-neutral **QueryPlan IR**; Gremlin, openCypher, GQL, SPARQL, SQL/PGQ, etc. are *front-ends and back-ends* of the IR (§6). Gremlin remains the reference traversal dialect for HugeGraph. |
| C7 | JSON as the ingestion format | JSON stays the **canonical interchange and raw-capture format**; non-JSON sources are normalized to JSON envelopes by connectors/parsers (§7). |
| C8 | Normative schema (doc 11) vs as-built schema (doc 06: 74 vertex / 68 edge labels) | As-built `06` is the baseline; the commercial ontology is *layered*: core upper ontology + industry packs + tenant extensions (§8). |
| C9 | Audit "100% Done" vs verified reality | Adopt the evidence tiers in §0. Inherit the 16 open external gates (Appendix C) as GA release gates. |
| C10 | Vocabulary drift (`IngestionRun` PENDING/RUNNING/DONE vs SUCCEEDED/PARTIAL/HELD; `GraphRevision` vs `EntityRevision`; DLQ path drift; MCP tool-count drift) | Standardize by ADR before GA: run states = `PENDING, RUNNING, SUCCEEDED, PARTIAL, HELD, FAILED, CANCELLED`; revision concept = `EntityRevision`; generated inventories (tool counts, routes) MUST be produced from code, never hand-written. |

---

## 3. Principles, Constraints and Deployment Profiles

### 3.1 Non-negotiable principles

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-CON-001 | **Self-contained:** the default distribution MUST run with zero external network dependencies (no SaaS, no cloud API, no phone-home, no CDN assets, no package fetch at runtime). | P0 |
| SR-CON-002 | **Local-first:** all processing, storage, indexing, embedding, inference and UI serving happen inside the customer-controlled boundary by default; the system MUST function fully offline. | P0 |
| SR-CON-003 | **No egress by default:** outbound traffic MUST be denied by default via network policy and application-level egress gateway; any permitted egress is allowlisted, logged and attributable. | P0 |
| SR-CON-004 | **Everything configurable, safely:** every behavior in this document that says "configurable" MUST be a typed, versioned, validated, auditable setting with a safe default (§12.3). | P0 |
| SR-CON-005 | **LLM-optional:** ingestion, graph construction, validation, deterministic query, impact analysis, lineage and reporting MUST work with no LLM present. | P0 |
| SR-CON-006 | **Evidence-first:** every returned fact carries source, method (asserted/derived/inferred/curated), confidence, freshness and policy-filter notice. | P0 |
| SR-CON-007 | **Clean-room and license-clean:** study external products and papers for ideas only; produce an independent implementation, SBOM and license report per release. | P0 |
| SR-CON-008 | **Adapters over lock-in:** no component outside an adapter may import a vendor-specific graph, vector, model, bus or storage SDK. Enforced by architecture tests. | P0 |
| SR-CON-009 | **Vendor-neutral data ownership:** customers can export all data, ontology, config and audit trails in open formats at any time (§7.9). | P0 |

### 3.2 Deployment profiles (each MUST be a first-class, tested configuration)

| Profile | Description | Cloud services | External LLM | Pri |
| --- | --- | --- | --- | --- |
| DP-0 Demo / single node | Compose, embedded stores, sample data | None | None | P0 |
| DP-1 Air-gapped on-prem | Offline signed bundles, enforced no-egress, offline license and updates | None | None | P0 |
| DP-2 On-prem connected | On-prem plus egress gateway with allowlist | Optional, per plugin | Optional (policy) | P0 |
| DP-3 Hybrid | Selected components in customer cloud account/VPC (e.g., object store, managed graph) | Declared, per capability | Optional | P1 |
| DP-4 Cloud-native single tenant | Kubernetes in customer cloud; managed-service adapters (graph, search, object, KMS, IdP) | Yes, customer-owned | Optional | P1 |
| DP-5 Partner/vendor-hosted multi-tenant | Managed service with strict tenant isolation | Yes | Optional | P2 |
| DP-6 Edge / federated | Site nodes (factory, hospital, branch) sync graph deltas or summaries to a hub; operate disconnected | Optional | Optional | P2 |

### 3.3 Cloud and cloud-service enablement model

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-CON-010 | Cloud capabilities MUST be delivered as **Service Provider plugins** (e.g., object storage, managed graph DB, managed search, KMS/HSM, IdP, queue, LLM endpoint, monitoring sink) selectable per capability, per tenant. | P0 |
| SR-CON-011 | Every plugin MUST ship a **Data-Flow Manifest** declaring data classes sent/received, destinations, regions, retention and whether data can leave the tenant boundary. Installation MUST display it and require admin approval; the egress gateway enforces it at runtime. | P0 |
| SR-CON-012 | Provide reference adapters for the three hyperscalers' object storage, KMS, identity federation and managed graph/search where available (e.g., Amazon Neptune/OpenSearch/S3/KMS, Azure Blob/Key Vault/Entra ID/Cosmos Gremlin, GCP GCS/KMS/Cloud Identity). | P1 |
| SR-CON-013 | Provide infrastructure-as-code modules (Terraform/OpenTofu, Helm) for DP-3/DP-4 with security-hardened defaults, private networking, and no public endpoints by default. | P1 |
| SR-CON-014 | A tenant MUST be able to switch a capability between local and cloud providers via migration tooling (e.g., local object store → cloud bucket) with verification and rollback. | P2 |

---

## 4. Reference Architecture

### 4.1 Logical layers

```
 EXPERIENCE   Web app | Admin/Tenant/Partner consoles | VS Code & JetBrains | CLI | Chat/ChatOps | MCP clients | REST/GraphQL/gRPC SDKs
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 EDGE/PEP     API gateway • AuthN • Tenant resolution • AuthZ policy enforcement point • rate/quota • egress gateway
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 INTELLIGENCE NL interface • Intent & suggestion engine • QueryPlan compiler/optimizer • Retrieval router • GraphRAG
              Reasoning/inference • Agent runtime & orchestrator • Report generator • Simulation / what-if
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 KNOWLEDGE    Ontology service • Graph service (Graph Store Port) • Vector/Search service • Identity resolution
              Provenance & lineage • Temporal versioning • Quality & validation • Catalog/glossary • Policy/classification
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 INGESTION    Connector runtime • Raw landing (immutable) • Pipeline orchestrator • Parsers/extractors • Schema inference
              Relationship discovery • Mapping engine • CDC/stream processors • DLQ/replay
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 MODEL LAYER  Model abstraction • Local runtimes • Embedding service • Egress-gated external endpoints • Prompt/eval registry
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 STORAGE      Graph backends | Vector stores | Full-text | Relational metadata/config | Object/raw | Cache | Event log | Secrets/KMS
 ───────────────────────────────────────────────────────────────────────────────────────────────────────────────
 PLATFORM     Tenancy • Config • Licensing/entitlements • Plugin runtime • Scheduler • Observability • Backup • Update/offline bundles
 CROSS-CUTTING Security • Privacy • Governance • Audit • Compliance evidence
```

### 4.2 Architectural requirements

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ARC-001 | **Modular monolith first, service-extractable:** modules communicate through typed interfaces/events and MUST be separable into independently scalable services without code rewrite (preserves the prior `NFR-MAINT-001` boundary). | P0 |
| SR-ARC-002 | **Ports-and-adapters:** Graph Store, Vector Store, Search, Object Store, Relational Store, Event Bus, Model Provider, Identity Provider, Secret/KMS, Scheduler and Notification are ports with versioned contracts and a conformance test kit. | P0 |
| SR-ARC-003 | **Event backbone:** an append-only event log (pluggable: embedded log for DP-0; NATS JetStream/Kafka-class for clustered) carries ingestion, mutation, policy and audit events; consumers are idempotent (outbox pattern). | P0 |
| SR-ARC-004 | **Single canonical contract per concept:** one versioned schema registry for entities, edges, events, QueryPlan, agent contract, config and plugin manifest; all APIs and UIs derive from it (generated, not hand-copied). | P0 |
| SR-ARC-005 | **Distributed by design:** stateless API/query/worker tiers scale horizontally; stateful tiers (graph, vector, search, relational, object, log) support replication and partitioning per backend capability. | P0 |
| SR-ARC-006 | **Consistency model documented and tested:** strong consistency within a graph partition for writes and read-your-writes for the writer; eventual consistency for derived indexes (vector, search, materialized views) with measurable lag SLOs and a staleness indicator surfaced to users. | P0 |
| SR-ARC-007 | **Exactly-once effects** via idempotency keys, deterministic IDs and replay-safe mutations; at-least-once delivery acceptable at transport level. | P0 |
| SR-ARC-008 | **Hybrid logical clocks / bitemporal fields** on all mutations (valid time, transaction time) so federated and replayed data order deterministically. | P1 |
| SR-ARC-009 | **Federation:** queries MAY span multiple graph backends and multiple sites (hub-and-spoke or mesh) with partial-result semantics, per-site policy enforcement and no raw-data movement unless permitted. | P2 |
| SR-ARC-010 | **Sandboxed extension runtime:** plugins execute in isolated containers or WASM sandboxes with declared capabilities, CPU/memory/egress limits and signed manifests (§12.5). | P0 |
| SR-ARC-011 | **Architecture fitness tests** in CI: forbidden imports, layering rules, adapter-only vendor SDK usage, no hand-maintained inventories, no cross-tenant code paths without tenant context. | P0 |
| SR-ARC-012 | **Mandatory ADR process:** every decision that changes a port, a default component or a supported-backend tier needs an ADR with alternatives, license review and benchmark evidence. | P0 |

---

## 5. Storage Layer: Graph, Vector, Search, Relational, Object, Bus

### 5.1 Graph Store Port and certification tiers

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-GDB-001 | All graph access MUST go through the **Graph Store Port** exposing: schema ops, bulk load, transactional upsert (idempotent by canonical ID), traversal, path, neighborhood, aggregation, full-scan with cursor, index management, snapshot/export, health and statistics. | P0 |
| SR-GDB-002 | Each adapter MUST publish a **Capability Manifest** (example in §5.6). The planner uses it to choose pushdown vs in-engine execution and to refuse or degrade unsupported plans *explicitly* (never silently). | P0 |
| SR-GDB-003 | A **backend-neutral conformance suite** (contract tests + golden queries + performance probes + failure injection) MUST gate every adapter. Backend-specific behavior (e.g., HugeGraph 1.7 not honoring UNIQUE edge indexes, requiring SECONDARY + sort-key emulation) is recorded in the manifest, not scattered in code. | P0 |
| SR-GDB-004 | **Certification tiers:** Tier A *Certified* (full conformance, benchmarked, HA validated, supported under SLA); Tier B *Compatible* (documented capability gaps); Tier C *Community/Experimental*. Marketing MUST NOT claim support beyond the tier. | P0 |
| SR-GDB-005 | **Polyglot persistence:** each logical graph domain (e.g., org, code, incident, lineage, meta) MAY bind to a different backend and tier (hot/warm/cold); cross-domain **bridge edges** are resolved by the federation layer. | P1 |
| SR-GDB-006 | **Online migration** between backends (export → verify counts/checksums/golden queries → dual-write or cutover → rollback) MUST be supported for Tier A pairs. | P1 |
| SR-GDB-007 | **Virtual/zero-ETL graph mode:** optionally expose existing relational/lakehouse data as a graph view through declarative mappings (OBDA/virtual-graph style) without copying data. | P2 |
| SR-GDB-008 | **Multi-model graph support:** property graph (LPG) and RDF are both first-class; RDF-star/reification patterns and LPG↔RDF round-trip mappings MUST be defined and tested. | P1 |
| SR-GDB-009 | **Graph versioning:** every mutation produces an `EntityRevision`; point-in-time ("as-of") reads and diffs between revisions MUST be supported (full snapshot/diff at P1). | P1 |
| SR-GDB-010 | **Embedded engine option** for DP-0/edge nodes with no server process, and an in-memory engine for tests only (selection is explicit configuration, never a silent fallback). | P0 |

### 5.2 Supported-backend matrix (initial tiering — Proposal; verify license and current maintenance at selection time)

| Backend / family | Native query surface | Runs local | Cloud-managed | Initial tier | Notes |
| --- | --- | --- | --- | --- | --- |
| Apache HugeGraph (1.7.x; top-level Apache project since Jan 2026; distributed PD/Store mode exists) | Gremlin (primary) | Yes | No | A (default bundled) | Single-node and distributed shapes MUST both be validated; the repo notes PD/Store sharding is not yet validated |
| Neo4j | Cypher; GQL-aligned | Yes | Yes (Aura) | A | Edition and license determine bundling; bring-your-own mode |
| Amazon Neptune | openCypher, Gremlin, SPARQL | No | Yes only | A (DP-3/4) | Implemented in baseline (openCypher) |
| JanusGraph (Cassandra/ScyllaDB/HBase + search backend) | Gremlin | Yes | Via hosted storage | B | Scale-out friendly; operationally heavy |
| TigerGraph | GSQL, openCypher subset | Yes | Yes | B | Commercial; deep-link analytics |
| Memgraph | Cypher | Yes | Yes | B | In-memory, streaming-friendly |
| Apache AGE (PostgreSQL extension) | openCypher in SQL | Yes | Via Postgres hosts | B | Attractive for Postgres-standardized shops |
| Embedded columnar graph engines (Kuzu lineage / community forks; verify maintenance status) | Cypher | Embedded | No | B/C | Candidate for DP-0 and edge |
| FalkorDB, NebulaGraph, ArangoDB, Dgraph, others | Cypher/nGQL/AQL/DQL | Yes | Varies | C | Community adapters via SDK |
| Azure Cosmos DB (Gremlin API) | Gremlin | No | Yes only | B (DP-4) | |
| SQL/PGQ-capable relational engines (e.g., Oracle Database 23ai; others as they ship ISO/IEC 9075-16 support) | SQL/PGQ | Yes | Yes | B/P2 | Enterprise standardization path |
| RDF triple stores: Apache Jena/Fuseki, Eclipse RDF4J, Oxigraph, Ontotext GraphDB, Stardog, Virtuoso, AllegroGraph | SPARQL 1.1 (+RDF-star where available) | Yes | Some | A for one OSS store, others B | Needed for OWL/SHACL-centric customers |
| Virtual graph engines over SQL/lakehouse (e.g., PuppyGraph-style, Ontop-style OBDA) | openCypher/Gremlin/SPARQL | Yes | Some | P2 | Zero-ETL mode (SR-GDB-007) |

### 5.3 Relational, object, bus, cache, workflow

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-GDB-011 | **Relational metadata/config store:** PostgreSQL as the clustered default, SQLite for single-node DP-0; ports allow customer-standard engines (SQL Server, Oracle, MySQL/MariaDB) at P2. | P0 |
| SR-GDB-012 | **Object/raw store:** filesystem (DP-0), S3-compatible (clustered), and cloud blob adapters. Raw captures are immutable, content-addressed (SHA-256), encrypted, and retention-managed. | P0 |
| SR-GDB-013 | **Event bus adapters:** embedded log, NATS JetStream-class, Kafka/Redpanda-class, RabbitMQ, cloud queues. | P0/P1 |
| SR-GDB-014 | **Cache:** in-process plus a Redis-protocol-compatible adapter; every cache key MUST include tenant, policy-version and graph-revision. | P0 |
| SR-GDB-015 | **Durable workflow engine** built in (retry, timers, human-approval steps, sagas); optional adapters for Temporal/Airflow/Dagster/Prefect-class orchestrators. | P1 |
| SR-GDB-016 | **Component license matrix:** every bundled and optional component is classified (permissive / weak copyleft / strong copyleft or network-copyleft / source-available / commercial). Anything other than permissive MUST NOT be bundled without legal sign-off and MUST be offered as bring-your-own where needed. | P0 |

### 5.4 Vector, hybrid and full-text retrieval stores

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-VDB-001 | **Vector Store Port:** upsert/delete by ID with metadata, filtered kNN, hybrid (dense + sparse/BM25), namespace-per-tenant, snapshot/restore, index rebuild, embedding-model version tracking. | P0 |
| SR-VDB-002 | **Adapters:** embedded (FAISS/hnswlib/USearch/LanceDB-class), PostgreSQL pgvector, Qdrant, Milvus, Weaviate, Chroma, OpenSearch/Elasticsearch k-NN, Redis-compatible vector, Vespa, graph-native vector indexes (e.g., Neo4j), plus cloud-managed (Pinecone, Azure AI Search, Vertex AI Vector Search, Atlas Vector Search) under DP-3/4 only. | P0 (embedded, pgvector) / P1 (rest) |
| SR-VDB-003 | **Index strategies configurable:** HNSW, IVF-PQ, DiskANN-class disk indexes, scalar/product/binary quantization, filtered-search strategies, per-collection recall/latency targets. | P1 |
| SR-VDB-004 | **Multi-vector and multimodal:** text, code, table, image, audio-transcript, and node/graph embeddings; late-interaction (ColBERT-style) and sparse-learned (SPLADE-style) as optional retrievers. | P2 |
| SR-VDB-005 | **Embedding governance:** embeddings are derived data; they inherit the classification and access policy of their source, are deleted when the source is erased (§14.3), and are re-generated on model change with versioned side-by-side indexes and cut-over. | P0 |
| SR-VDB-006 | **Full-text/search port:** BM25 keyword, phrase, fuzzy, facets, highlighting, multilingual analyzers; adapters for embedded engine (Tantivy/SQLite-FTS class), PostgreSQL FTS, OpenSearch/Elasticsearch class. | P0 |
| SR-VDB-007 | A deployment with **no vector store** MUST still pass the core NL acceptance suite using graph + full-text retrieval (degraded semantic recall is acceptable and MUST be signalled). | P0 |

### 5.5 Sizing tiers (Proposal — targets to validate by benchmark; do not publish as claims until measured)

| Tier | Graph size (vertices + edges) | Topology | Notes |
| --- | --- | --- | --- |
| S | ≤ 50 M | single node | DP-0/DP-1 small orgs, departmental |
| M | ≤ 2 B | 3–9 node cluster | typical enterprise |
| L | ≤ 20 B | sharded, multi-cluster | large enterprise / managed multi-tenant |
| XL | > 20 B | federated multi-cluster | global orgs; hot/cold tiering mandatory |

### 5.6 Sample Graph Store Capability Manifest (illustrative)

```yaml
adapter: hugegraph
adapter_version: 1.0.0
backend_version_range: ">=1.7.0 <2.0.0"
tier: A
languages: { gremlin: native, opencypher: translated, gql: translated, sparql: unsupported }
capabilities:
  transactions: { multi_statement: true, isolation: read_committed }
  unique_edge_index: emulated        # SECONDARY index + sort key (documented backend limitation)
  bulk_load: { formats: [json, csv], max_batch: 50000 }
  as_of_reads: emulated_via_revisions
  vector_index: false                # routed to Vector Store Port
  distributed: { sharding: pd_store, validated_profiles: [single_node] }
limits: { max_traversal_depth: 12, default_timeout_ms: 20000 }
pushdown: [path, neighborhood, filter, aggregate_count, topk]
```

---

## 6. Query and Language Layer

### 6.1 Canonical QueryPlan IR

All user-facing and machine-facing queries compile to a **QueryPlan IR** (structured, validated, versioned), which is then lowered to the selected backend dialect. This is how multiple graph languages, data languages and natural language coexist without N×M translators.

```json
{
  "plan_version": "2",
  "intent": "impact_analysis",
  "tenant": "t-001", "principal": "u-123", "as_of": null,
  "anchor": { "type": "ServiceAccount", "match": { "name": "abc" }, "resolve": "alias_aware" },
  "operation": "delete",
  "traversal": {
    "direction": "out",
    "edge_classes": ["USES_CREDENTIAL", "AUTHENTICATES_AS", "RUNS_AS", "REFERENCES_SECRET", "DEPLOYED_BY"],
    "max_depth": 6, "min_confidence": 0.6, "include_inferred": true
  },
  "rank": { "by": ["criticality", "path_confidence", "environment"] },
  "limits": { "timeout_ms": 15000, "max_results": 500, "max_expansions": 200000 },
  "output": { "shape": "blast_radius", "evidence": "paths", "explain": true }
}
```

### 6.2 Language support

| Category | Language / standard | Role in the Platform | Pri |
| --- | --- | --- | --- |
| Property-graph | **Gremlin** (Apache TinkerPop) | Reference traversal dialect; back-end for HugeGraph/Janus/Neptune/Cosmos | P0 |
| Property-graph | **openCypher** | Front-end and back-end (Neo4j, Neptune, Memgraph, AGE, embedded engines) | P0 |
| Property-graph | **GQL — ISO/IEC 39075:2024** | Standards-based front-end and target as backends adopt it | P1 |
| Property-graph in SQL | **SQL/PGQ — ISO/IEC 9075-16:2023** | Relational-engine graph queries; BI integration path | P1 |
| Vendor graph | GSQL (TigerGraph), PGQL (Oracle), AQL (ArangoDB), nGQL (NebulaGraph), DQL (Dgraph) | Adapter-specific back-ends only | P2 |
| RDF | **SPARQL 1.1** (+ RDF-star/SPARQL-star, and 1.2 as it stabilizes) | RDF back-ends; federated SPARQL endpoints | P0 |
| Graph API | **GraphQL** | Public API surface and schema auto-generated from the ontology (not a storage query language) | P0 |
| Relational | **SQL** (ANSI + dialect options) | Metadata, analytics, JDBC/ODBC read-only SQL view over the graph for BI tools | P0 |
| JSON | **JSONPath (RFC 9535)**, JMESPath, jq-style filters | Query raw captures and node payloads | P0 |
| XML | XPath/XQuery | XML source payloads | P2 |
| Rules/logic | Datalog-style rules, SWRL/N3-style rules, SHACL-SPARQL rules | Inference and derived edges (§8.4) | P1 |
| Search | Lucene-style query syntax; vector kNN with filters | Retrieval | P0 |
| Native | **EOQL** (platform's declarative query language) | Compiles to QueryPlan IR; the stable, backend-neutral language for saved queries and APIs | P0 |
| Not query languages (clarified) | **SHACL** (validation), **SKOS** (vocabulary), **OWL/RDFS** (ontology) | Handled in §8; do not conflate with query languages | — |

### 6.3 Query-engine requirements

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-QRY-001 | The compiler MUST accept EOQL, Gremlin, openCypher, GQL (subset first), SPARQL, SQL (analytics) and NL-produced plans, validate them against the ontology and the caller's policy, and lower them per the Capability Manifest. | P0 |
| SR-QRY-002 | **Never execute raw model- or user-generated graph queries** without schema-aware validation, policy rewrite, depth/timeout/expansion/cost limits and expensive-pattern detection. Raw dialect access is an admin-gated, audited feature. | P0 |
| SR-QRY-003 | **Query Explain:** every query returns (on request) the plan, chosen backend(s), pushdowns, estimated vs actual cost, and the generated dialect text. | P0 |
| SR-QRY-004 | **Dialect round-trip tests:** a golden corpus (≥ 500 queries per Tier A backend, growing) MUST prove IR → dialect semantic equivalence by result comparison on shared fixtures. | P0 |
| SR-QRY-005 | **Parameterization everywhere;** string-built queries are forbidden (injection defense). | P0 |
| SR-QRY-006 | **Saved queries, query libraries, templates and versioned "question catalog"** per tenant/workspace, shareable and permission-aware. | P0 |
| SR-QRY-007 | **Result envelope:** rows/graph/table/report + evidence IDs + method flags + freshness (as-of, lag) + coverage notes + policy filters applied. | P0 |
| SR-QRY-008 | **Graph algorithm library** callable from plans (≥ 60 algorithms by P1): shortest/k-shortest/all-simple paths, reachability, SCC/WCC, topological order and cycle detection, dominators/critical path, PageRank/personalized PageRank, betweenness/closeness/degree/eigenvector centrality, community detection (Leiden/Louvain/label propagation), triangle/clustering/k-core, similarity (Jaccard/cosine/Adamic-Adar), node embeddings (node2vec/GraphSAGE-class), link prediction, motif matching, temporal paths, flow/cut, subgraph isomorphism/pattern matching. Each declares complexity and sampling/approximation modes. | P0 (core 30) / P1 |
| SR-QRY-009 | **Incremental / precomputed accelerators:** transitive-closure or reachability indexes for impact queries, materialized views per persona, summary edges, and top-k caches, all invalidated by graph-revision events. | P1 |
| SR-QRY-010 | **Federated query** across backends and sites with per-source policy enforcement and partial results. | P2 |
| SR-QRY-011 | **Time travel:** `AS OF`, `BETWEEN`, `DIFF` over revisions for every query class where backends or the revision store allow. | P1 |
| SR-QRY-012 | **Multilingual query front-ends** (NL, EOQL) with locale-aware date/number handling. | P1 |

---

## 7. Ingestion, Transformation and Automatic Graph Construction

### 7.1 Connector and format coverage

| Domain | Representative sources (each is a connector or a mapping pack) |
| --- | --- |
| Engineering | Git, GitLab, GitHub, Bitbucket, Azure DevOps, Jira, Confluence, Jenkins/CI, Artifactory/registries, SonarQube-class, SBOM (CycloneDX/SPDX), IaC (Terraform, Kubernetes, Helm, Ansible), API specs (OpenAPI, AsyncAPI, protobuf, GraphQL SDL) |
| IT operations | ServiceNow, BMC, PagerDuty/Opsgenie, Splunk, Datadog, Kibana/Elastic, Prometheus, Grafana, OpenTelemetry traces, CMDB/CSDM |
| Cloud & infra | AWS/Azure/GCP inventories, Kubernetes, VMware, network/firewall configs, DNS/CDN |
| Identity & security | AD/Entra, Okta, LDAP, IAM policies, Vault/KMS, SIEM, vulnerability and CSPM scanners, STIX/TAXII |
| Data platform | JDBC/ODBC DBs, warehouses, lakehouse (Iceberg/Delta/Hudi), Kafka, dbt, Airflow, OpenLineage, data catalogs (DataHub, OpenMetadata, Atlas, Collibra-class) |
| Documents & knowledge | SharePoint, Documentum, Drive/Box, file shares, email, wiki, PDF/Office/CSV/XML/Markdown, images (OCR), audio/video transcripts, architecture diagrams |
| Business applications | SAP, Oracle, Salesforce, Workday, Dynamics, Zendesk, HubSpot, ERP/CRM/HRIS/PLM/MES exports |
| Industry standards | HL7/FHIR, DICOM metadata, X12/EDIFACT, ISO 20022/SWIFT, FIX, ACORD, GS1, OPC UA, MQTT, IEC 61850/CIM, ISA-95, TM Forum |
| Generic | REST, GraphQL, SOAP, webhooks, SFTP, S3-compatible, file drop, OData; JSON, NDJSON, CSV/TSV, XML, YAML, Parquet, Avro, Excel, RDF (Turtle, N-Quads, JSON-LD) |

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-001 | **Connector SDK** (Python and TypeScript at P0; Go/Java at P1) with a stable contract: `discover`, `authenticate`, `fetch(cursor)`, `schema`, `health`, `metrics`, `capabilities`, `deletion_semantics`; connectors run sandboxed with declared scopes. | P0 |
| SR-ING-002 | Resiliency: pagination, rate-limit adaptation, retry with jitter, circuit breaker, checkpoint/cursor, partial-failure isolation, DLQ, replay, dry-run, backfill and incremental sync. | P0 |
| SR-ING-003 | **Change capture:** polling, webhooks, CDC (log-based where the source supports it), file watchers, stream consumers; deletes handled by tombstones with configurable semantics (soft delete, retire edge, hard delete on policy). | P0 |
| SR-ING-004 | **Credential isolation:** connector secrets live only in the secret store, scoped per tenant/connector, rotated, never logged, never visible to plugins other than the owning connector. | P0 |
| SR-ING-005 | **Connector marketplace-ready packaging:** signed manifest, version, compatibility range, data-flow manifest, test fixtures, health contract. | P1 |
| SR-ING-006 | **Streaming and batch share one pipeline:** the same stages and mapping specs serve both; back-pressure and priority lanes per tenant. | P0 |
| SR-ING-007 | **Large-JSON handling:** streaming parse (never load whole file), gz/zstd/archive support, malformed-record quarantine with line/offset pointers, numeric precision and Unicode/timezone normalization, binary blob offload. | P0 |

### 7.2 Pipeline stages (extends the 13-step source pipeline)

| # | Stage | Output |
| --- | --- | --- |
| 1 | Source & auth | scoped session |
| 2 | Fetch / stream | raw payload batches |
| 3 | **Raw capture** (immutable, content-addressed) | `raw_id`, hash, encrypted blob |
| 4 | **Classification & policy tagging** (PII/PHI/PCI/IP/secret; tenant data class) — *before* anything is indexed or embedded | sensitivity labels, handling policy |
| 5 | Canonicalization | normalized JSON envelope |
| 6 | **Profiling & schema inference** | field profiles, type/cardinality/key candidates |
| 7 | Parsing & extraction (documents, code ASTs, logs, tables) | structured fragments |
| 8 | **Entity detection** | candidate entities |
| 9 | **Key & relationship discovery** | candidate edges with method and confidence |
| 10 | **Identity resolution** | clusters, `identity_candidates`, crosswalks |
| 11 | **Ontology mapping** | typed vertices/edges (ontology version pinned) |
| 12 | Validation (SHACL-class + rules + severities) | validation report; hard-invalid → quarantine |
| 13 | **Graph mutation** (idempotent, transactional, revisioned) | `EntityRevision`s |
| 14 | **Derived structures** | meta-graph, materialized views, closures, communities, embeddings, search index |
| 15 | Quality, lineage, events | completeness/freshness/confidence metrics, OpenLineage events, notifications |

Provenance persisted for **every** vertex/edge/property: `source_system`, `source_id`, `raw_id`, `ingestion_run_id`, `connector_version`, `mapping_version`, `ontology_version`, `method` (asserted / derived / inferred / curated), `confidence`, `evidence[]`, `valid_from/valid_to`, `recorded_at`, `classification`, `tenant_id`.

### 7.3 Automatic detection of entities and relationships from JSON

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-010 | The **Schema Profiler** MUST infer types, nullability, cardinality, uniqueness, enumerations, formats (email, UUID, URL, IP/CIDR, ISO date/time, currency, phone, IBAN, ARN/URN, git SHA, ticket keys like `ABC-123`, file paths), nesting shape, and drift across versions of a payload. | P0 |
| SR-ING-011 | **Entity detection:** record types from top-level arrays/envelopes/discriminator fields; nested objects classified as *embedded value*, *child entity*, or *reference* using a scored heuristic (key presence, size, reuse across parents, naming, user override). | P0 |
| SR-ING-012 | **Key detection:** natural/surrogate key candidates; composite keys; stability scoring across runs; canonical ID minting strategy per type (deterministic, namespaced, collision-safe). | P0 |
| SR-ING-013 | **Relationship discovery — explicit:** foreign-key-like fields, `$ref`/JSON Pointer, URLs to known entities, `*_id`/`parent`/`owner` conventions, join-table detection (junction → edge with properties), polymorphic `type`+`id` pairs, array-of-IDs, hierarchy via parent pointers or path strings. | P0 |
| SR-ING-014 | **Relationship discovery — statistical:** inclusion-dependency and value-overlap discovery across datasets (MinHash/LSH containment for scale), name and embedding-based schema matching, co-occurrence, temporal proximity, co-change coupling, mention extraction in text (entity linking). | P0 (value overlap) / P1 |
| SR-ING-015 | **Relationship discovery — operational:** service-call edges from traces/logs, config references (env var → secret → account), IaC dependency edges, build/runtime dependencies from SBOM and lockfiles, code call/import graphs (tree-sitter and SCIP/LSIF-class indexers), SQL lineage parsing, access-log derived usage edges. | P0 (engineering set) / P1 |
| SR-ING-016 | **Edge classes and honesty:** every edge is `ASSERTED` (source says so), `DERIVED` (deterministic rule), `INFERRED` (statistical/ML/LLM), or `CURATED` (human-approved), with confidence and method. Inferred edges are excluded from "authoritative" answers unless the query opts in. *(Analogous to Graphify's EXTRACTED / INFERRED / AMBIGUOUS confidence tags, extended with CURATED and DERIVED.)* | P0 |
| SR-ING-017 | **Ontology induction:** propose classes, properties, relation types and hierarchies from data; present for steward approval in the Mapping Studio; support *ontology-first*, *data-first* and *hybrid* modes. | P1 |
| SR-ING-018 | **Link prediction / graph completion** (heuristic and learned, e.g., translational and GNN-class models) proposes missing edges into a review queue; auto-assertion only above a tenant-configured threshold. | P2 |
| SR-ING-019 | **Mapping DSL:** declarative, versioned, diff-able mappings (YAML/JSON) with RML/R2RML and JSON-LD `@context` import/export; generated by inference, editable by humans, testable on samples. | P0 |
| SR-ING-020 | **Schema drift handling:** new/changed/removed fields trigger drift events, auto-compatible mapping updates when safe, and steward review when not; mappings are pinned per run for reproducibility. | P0 |

**Sample inferred mapping (illustrative):**

```yaml
mapping: incidents-v3
source: { system: servicenow, dataset: incident, format: json }
entities:
  - type: Incident
    id: { from: "$.number", namespace: "snow:incident" }
    props: { summary: "$.short_description", priority: "$.priority", opened_at: { path: "$.opened_at", type: datetime } }
  - type: Person
    id: { from: "$.assigned_to.email", normalize: lowercase, namespace: "person" }
    resolve: { strategy: identity_resolution, keys: [email, employee_id] }
relationships:
  - { edge: ASSIGNED_TO, from: Incident, to: Person, class: ASSERTED }
  - { edge: AFFECTS, from: Incident, to: Service, via: "$.cmdb_ci.value", class: ASSERTED }
  - { edge: MENTIONS_CLASS, from: Incident, to: Class, via: { text_extract: "$.description", linker: symbol_linker }, class: INFERRED, min_confidence: 0.7 }
policy: { classification_from: [ "$.caller_id.email" ], retain_days: 1095 }
```

### 7.4 Identity resolution and entity resolution

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-030 | Deterministic rules first (exact keys, normalized emails/IDs), then probabilistic (blocking via sorted-neighborhood/canopy/LSH; pairwise similarity with string/phonetic/numeric/date/embedding features; Fellegi–Sunter-class scoring and/or trained classifiers). | P0 |
| SR-ING-031 | **Collective resolution** using graph context (shared neighbors, co-authorship, same repo/team) and transitive clustering with constraints; **survivorship rules** produce golden records with per-attribute source precedence. | P1 |
| SR-ING-032 | Every merge is **explainable, reversible (unmerge), audited**; three bands (auto-merge / human review / reject) with tenant-set thresholds and an active-learning review queue. | P0 |
| SR-ING-033 | **Cross-source ID crosswalk** persisted as first-class graph structure (`SAME_AS` with confidence and evidence) so aliases resolve at query time. | P0 |

### 7.5 Graph construction: the derived graph family

The Platform MUST construct and maintain, per tenant and per ontology version, these graph structures (each queryable, each with its own freshness SLO):

| Graph | Contents | Purpose |
| --- | --- | --- |
| Instance graph | Entities and typed relationships | Core knowledge |
| **Meta-graph (schema graph)** | Types, relation types, cardinalities, statistics, field-to-concept mappings, per-domain and per-backend placement | Query planning, discovery, NL grounding, "what do we know about?" |
| **Relationship graph** | Collapsed/summarized inter-entity-type and inter-domain relations with weights | Fast multi-hop search, domain overview |
| Provenance & lineage graph | Raw captures → transformations → entities; data and code lineage | Trust, audit, erasure propagation |
| Source graph | Systems, datasets, fields, connectors, runs | Coverage and drift awareness |
| Temporal graph | Revisions, validity intervals, events | As-of queries, change history |
| Similarity graph | kNN edges from embeddings and structural similarity | Recommendation, dedupe, discovery |
| Community / hierarchy graph | Leiden/Louvain communities, hierarchical summaries with LLM-free labels first | Global questions, GraphRAG-style summarization |
| Policy graph | Classification, ownership, ACL and retention propagation | Authorization and DLP at query time |
| Usage graph | Query patterns, hot paths, answer feedback | Adaptive indexing, suggestion ranking |
| Reified/n-ary relations | Statement nodes for relations with attributes, time, evidence | Rich facts; RDF-star mapping |
| Hypergraph / causal-dependency views | Multi-party events (incidents, changes, transactions) | Root-cause and what-if |

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-040 | Derived graphs are computed **incrementally** from mutation events; full rebuild MUST be possible and verified equivalent to the incremental result. | P0 |
| SR-ING-041 | **Graphify-class artifacts:** auto-generate portable `graph.json`, interactive HTML, and a markdown/wiki report per graph or subgraph; support export to Obsidian/Markdown vaults; support post-commit/post-merge hooks and PR-impact triage (rank open change requests by graph impact; flag overlapping-community conflicts). | P1 |
| SR-ING-042 | **Traversal-first retrieval** (no embeddings required) is the baseline retrieval mode; embeddings enhance recall but are never prerequisite (consistent with SR-CON-005). | P0 |
| SR-ING-043 | **Pre-aggregation:** per-type degree/centrality, per-edge-class reachability, and domain-to-domain bridge statistics are maintained to answer overview and impact questions within latency targets. | P1 |

### 7.6 Quality, validation, observability of ingestion

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-050 | Validation rules with severities (`INFO/WARN/ERROR/BLOCKER`), remediation suggestions, quarantine with replay, and a data-quality scorecard (completeness, freshness, uniqueness, consistency, confidence distribution) per source and per domain. | P0 |
| SR-ING-051 | **Freshness SLOs** per connector with alerting and a user-visible "knowledge age" on every answer. | P0 |
| SR-ING-052 | **Idempotency tests:** re-running an ingestion produces zero net graph change; interrupted runs resume without duplicates (restart-safe). | P0 |
| SR-ING-053 | **Reconciliation reports** (source counts vs graph counts, orphan edges, dangling references) on schedule. | P0 |

### 7.7 Ingestion performance targets (Proposal; baseline numbers come from the source Super-Prompt and MUST be re-measured per profile)

| Metric | S | M | L |
| --- | --- | --- | --- |
| Batch ingest of JSON issue-type records | ≥ 10 k records/min per worker | ≥ 100 k/min cluster | ≥ 1 M/min cluster |
| Bulk load into graph | ≥ 1 M vertices/hour (source baseline) per node | ≥ 50 M/hour cluster | ≥ 500 M/hour cluster |
| Freshness for webhook/CDC sources | ≤ 60 s p95 | ≤ 30 s p95 | ≤ 30 s p95 |
| Derived-structure lag | ≤ 5 min p95 | ≤ 5 min p95 | ≤ 15 min p95 |

### 7.8 Ingestion security

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-060 | **Hostile-input posture:** parsers sandboxed; zip-bomb/path-traversal/XXE/deserialization defenses; file-type verification; size/time limits. | P0 |
| SR-ING-061 | **Indirect prompt injection defense:** ingested text is data, never instructions; extracted passages are fenced, scanned and flagged before any LLM sees them. | P0 |

### 7.9 Export and interoperability

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ING-070 | Export formats: JSON/NDJSON, CSV, Parquet, GraphML, GEXF, GraphSON, openCypher bulk CSV, RDF (Turtle, N-Quads, JSON-LD, RDF-star), DOT/Mermaid, Markdown vault, interactive HTML; full-tenant export bundle (data + ontology + mappings + config + audit). | P0 |
| SR-ING-071 | BI/analytics access: read-only JDBC/ODBC SQL views, OData, GraphQL, Arrow Flight-class bulk endpoint, notebook (Jupyter) client libraries. | P1 |

---

## 8. Ontology, Semantics and Reasoning

### 8.1 Layered ontology model

| Layer | Content | Owner |
| --- | --- | --- |
| L0 Upper/core | Entity, Event, Agent, Artifact, Location, Time, Document, Policy, Evidence, Provenance (aligned to PROV-O) | Vendor |
| L1 Domain core | Organization, Person, Team, System, Service, API, Code, Change, Incident, Risk, Control, Asset, Contract, Process | Vendor |
| L2 Industry packs | Finance, Healthcare, Manufacturing, Retail, Energy, Telecom, Government, Education, Legal, Insurance, Logistics (§19) | Vendor/partner |
| L3 Tenant extensions | Custom classes, properties, vocabularies, rules | Customer |
| L4 Workspace views | Per-team aliases, labels, saved facets | Team |

### 8.2 Requirements

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ONT-001 | **Ontology service** stores ontologies as versioned artifacts (semantic versioning, diff, migration plans, deprecation lifecycle). Every graph element pins `ontology_version`. | P0 |
| SR-ONT-002 | **Import/export:** OWL 2 (RDF/XML, Turtle, Manchester), RDFS, SKOS, JSON Schema, JSON-LD contexts, LinkML-style schemas, Protégé project interop, CSV glossaries; export of the active ontology to OWL and SHACL shapes. | P0 |
| SR-ONT-003 | **Ontology Studio** (UI): visual class/property editor, relationship canvas, constraint editor, glossary/taxonomy manager, mapping designer, diff/merge, impact preview ("what existing data breaks if I change this?"), review-and-approve workflow with roles. | P0 |
| SR-ONT-004 | **Constraint validation** via SHACL-class shapes plus native rules; severity-based gates in ingestion; constraint violations visible as a graph-quality dashboard. | P0 |
| SR-ONT-005 | **Business glossary and taxonomy** (SKOS-compatible): terms, synonyms, multilingual labels, definitions, owners, approved-status; terms link to ontology concepts and to physical fields; NL layer uses the glossary for grounding. | P0 |
| SR-ONT-006 | **Ontology alignment/matching:** lexical, structural, embedding-assisted mapping between a customer's vocabulary and an industry standard, with confidence and steward review. | P1 |
| SR-ONT-007 | **Tenant-renamable terminology (white-label semantics):** a tenant may rename "Service" → "Application", "Incident" → "Case", etc., without changing the underlying canonical type. | P0 |
| SR-ONT-008 | **Ontology-driven generation:** GraphQL schema, REST resources, form UIs, validation, and docs generated from the ontology. | P1 |
| SR-ONT-009 | **Governed evolution:** proposals, review, approval, scheduled rollout, backward-compat checks, automatic data migration jobs, rollback. | P0 |
| SR-ONT-010 | **Catalog interoperability:** import/sync with data catalogs and glossaries (DataHub, OpenMetadata, Atlas, Collibra-class), CMDBs, enterprise-architecture repositories (ArchiMate/TOGAF models), and API registries. | P1 |

### 8.3 Standards and vocabularies the packs SHOULD align to (verify current versions when implementing)

| Area | Standards / vocabularies |
| --- | --- |
| General | RDF/RDFS/OWL 2, SKOS, SHACL, PROV-O (provenance), DCAT (catalogs), ODRL (policy), W3C Organization, FOAF, schema.org, Dublin Core, SOSA/SSN (sensors), GeoSPARQL |
| Engineering/IT | OpenTelemetry semantic conventions, CycloneDX/SPDX, OpenAPI/AsyncAPI, ITIL/CSDM-style service models, ArchiMate, STIX/ATT&CK |
| Finance/insurance | FIBO, ISO 20022, ACORD |
| Healthcare/life sciences | HL7 FHIR, SNOMED CT, ICD, LOINC, RxNorm (licensing of terminologies MUST be checked per jurisdiction) |
| Manufacturing/energy | ISA-95, OPC UA information models, IEC CIM (61970/61968), GS1 |
| Telecom | TM Forum SID |
| Government/legal | Legislation/legal XML models (e.g., Akoma Ntoso, ELI), OCDS (procurement) |

### 8.4 Reasoning and inference

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-ONT-020 | **Inference tiers:** (a) graph-native derivations (transitive, inverse, symmetric, property chains), (b) rule-based (Datalog/SWRL-class) materialization with provenance, (c) OWL-RL/EL profile reasoning where RDF back-ends support it, (d) probabilistic/ML inference proposals. Every inferred fact is labeled `DERIVED` or `INFERRED` and explainable ("why is this true?" returns the rule and premises). | P1 |
| SR-ONT-021 | **Truth maintenance:** retraction of premises retracts conclusions; contradictions are surfaced as validation findings, never silently resolved. | P1 |
| SR-ONT-022 | **Temporal and defeasible semantics** for roles/ownership that change over time (valid-time intervals on edges). | P1 |

### 8.5 Prior art to study (ideas only; clean-room), and what the Platform must exceed

| Category | Examples to benchmark / interoperate with |
| --- | --- |
| Code/knowledge-graph builders | **Graphify** (GitHub; AI-assistant-driven; typed edges with confidence tags; Leiden communities; post-commit rebuild; PR-impact triage; MCP/assistant integrations — *verify its repository, release and license state before reusing any code*), other code-graph and codemap tools |
| Ontology tooling | Protégé, TopBraid-class suites, PoolParty-class taxonomy tools, Ontotext GraphDB, Stardog, Neo4j with RDF/n10s-class plugins, Apache Jena/RDF4J, Ontop, pySHACL, owlready2-class libraries |
| Enterprise ontology/operational platforms | Palantir-Foundry-style operational ontologies, Microsoft Fabric/Purview-class semantic and catalog layers, data catalogs and lineage (DataHub, OpenMetadata, Atlas, Collibra, Atlan), developer portals (Backstage-class) |
| GraphRAG / agent memory | Microsoft GraphRAG, LightRAG-class, LlamaIndex property-graph indexes, Neo4j GraphRAG tooling, temporal knowledge-graph memory systems (e.g., Graphiti-class), Cognee-class pipelines |
| Graph engines & benchmarks | LDBC SNB / BI workloads, LUBM/BSBM-style RDF benchmarks |

**Where the Platform must exceed them:** multi-source enterprise scope, governed multi-tenancy, bitemporal truth, honest confidence/provenance on every edge, policy-aware answers, backend portability, local-first/air-gapped operation, and non-IT industry packs.

---

## 9. Retrieval, GraphRAG and the Natural-Language Interface

### 9.1 Retrieval Router (extends the source decision table)

| Query class | Graph traversal | Full-text | Vector | Community summaries | LLM needed | Notes |
| --- | :-: | :-: | :-: | :-: | :-: | --- |
| Entity lookup / alias resolution | Yes | Yes | Fuzzy only | No | No | Deterministic; alias crosswalk first |
| Traceability, path, impact, ownership, change history | **Yes** | Optional | No | No | Narration only | Provenance mandatory; inferred edges opt-in |
| Root cause / troubleshooting | Yes | Yes (logs, KB) | Yes (similar incidents) | No | Optional | Hypothesis ranking with evidence |
| Code symbol / semantic code search | Yes (AST/call graph) | Yes | Yes (code embeddings) | No | No | Exact first, fuzzy second |
| Document question answering | Context only | Yes | Yes | No | Yes | Cite passages; verify against graph facts |
| Multi-hop reasoning | Yes | Yes | Yes | Optional | Yes | Hybrid; step decomposition |
| Global / corpus-level ("what are the main risk themes?") | Yes | No | Optional | **Yes** | Yes | Map-reduce over hierarchical community summaries |
| Temporal / as-of / diff | Yes (revisions) | Optional | No | No | No | Revision store |
| Aggregation / analytics | Yes or SQL | No | No | No | No | Compute, don't generate |
| What-if simulation | Yes (overlay graph) | No | No | No | Narration only | Copy-on-write overlay; never mutates truth |
| Policy / compliance check | Yes + rules | Yes | Optional | No | Optional | Control-to-evidence mapping |
| Quick facts with a deterministic answer | Yes | Optional | No | No | **No** | Skip the LLM entirely |

### 9.2 Retrieval and RAG requirements

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-RAG-001 | **Router** chooses strategy per query class with a logged rationale; operators can override per tenant/workspace; unknown classes degrade to hybrid retrieval with a visible notice. | P0 |
| SR-RAG-002 | **GraphRAG patterns:** local (entity-neighborhood + attached documents), global (community-summary map-reduce), path-based, subgraph-as-context, and temporal. | P0 (local) / P1 |
| SR-RAG-003 | **Hybrid retrieval:** BM25 + dense (+ optional sparse-learned) with reciprocal-rank fusion, cross-encoder reranking (local models), metadata/policy filtering *before* ranking. | P0 |
| SR-RAG-004 | **Advanced strategies as plugins:** HyDE, query decomposition, step-back, RAG-Fusion, parent-child chunking, sentence-window, self-RAG/corrective-RAG, agentic RAG loops, long-context packing with budget manager. | P1 |
| SR-RAG-005 | **Graph-aware chunking:** chunk boundaries follow document structure and link to graph entities; every chunk carries `raw_id`, section path, classification, ontology links. | P0 |
| SR-RAG-006 | **Corrective verification:** before returning any LLM-generated assertion, verify entity/relationship claims against deterministic graph facts; unverifiable claims are removed or labeled. | P0 |
| SR-RAG-007 | **Context budget manager:** token-aware assembly, deduplication, evidence prioritization, and per-model context-window adaptation. | P0 |
| SR-RAG-008 | **Model-down fallback:** if no model is reachable, return deterministic results, retrieved evidence and templated narration with clear labeling (inherited `MVP-FR-020`). | P0 |
| SR-RAG-009 | **Caching:** semantic and exact caches keyed by tenant, policy version, graph revision and model version; invalidated by revision events. | P1 |
| SR-RAG-010 | **RAG evaluation harness** built in: retrieval precision/recall@k, MRR/nDCG, groundedness/faithfulness, citation precision, answer relevance, hallucination rate, latency, token cost; regression gates in CI. | P0 |

### 9.3 Natural-language interface (NL → question understanding → query → answer)

**Pipeline:** sanitize → language detect → intent classify → **entity linking/grounding** (glossary, aliases, meta-graph) → ambiguity detection → **clarify/suggest** → plan generation → validation → policy rewrite → execute → evidence assembly → answer synthesis → verification → follow-ups.

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-NLQ-001 | **Template/semantic-parser tier first:** common intents (§1.2) compile deterministically without an LLM; an LLM-assisted tier handles open-ended phrasing using constrained decoding against the ontology schema; both emit QueryPlan IR. | P0 |
| SR-NLQ-002 | **Intelligent suggestion engine (core differentiator):** when a question is ambiguous, under-specified, too broad, or maps to multiple plans, the system MUST present a ranked set of **candidate questions/queries** each with: plain-language paraphrase, the exact QueryPlan/dialect preview, expected result shape, entity bindings (with alternatives), estimated cost/latency, confidence, data-coverage note, and a permission check. The user selects and **fires** one (or edits first). | P0 |
| SR-NLQ-003 | **Entity disambiguation UX:** "service account `abc`" resolving to several entities (dev/prod, duplicates across systems) shows candidates with context and lets the user pin one for the session. | P0 |
| SR-NLQ-004 | **Answer modes:** (1) *Deterministic* — computed from the graph, exact, no LLM; (2) *Narrated* — deterministic facts + LLM wording; (3) *Exploratory investigation* — multi-step agent with visible plan and evidence trail; (4) *Report* — long-form, multi-section, charts/tables/citations, exportable. The UI states which mode produced the answer. | P0 |
| SR-NLQ-005 | **Depth bar ("no shortness"):** answers MUST include, as relevant: direct answer, supporting evidence and paths, assumptions, confidence and uncertainty, alternatives considered, recommended next actions, coverage gaps ("sources not ingested that could change this"), and suggested follow-up questions. Minimum answer-quality gates are enforced by the evaluation suite (SR-NLQ-010). | P0 |
| SR-NLQ-006 | **Explainability (XAI):** "why?" on any result returns the paths/rules/premises; counterfactuals ("what would change the answer?"); confidence decomposition (edge confidence, source freshness, coverage). Do not depend on exposing hidden model chain-of-thought. | P0 |
| SR-NLQ-007 | **Conversation context:** follow-ups, pronoun/ellipsis resolution, session and saved-investigation memory, pinned entities, branching ("explore alternative"), shareable investigation links respecting each viewer's permissions. | P0 |
| SR-NLQ-008 | **Reports:** templates (impact assessment, incident RCA, change-risk review, compliance evidence, executive brief), scheduled/recurring, parameterized, multi-format export (HTML, PDF, DOCX, PPTX, Markdown, JSON), evidence appendix with provenance, approval workflow, white-label styling. | P0 (HTML/MD/PDF) / P1 |
| SR-NLQ-009 | **Languages:** English at P0; multilingual NL (major European, Indic and East-Asian languages) via local multilingual models at P1, with glossary-term translation. | P1 |
| SR-NLQ-010 | **NL evaluation suite:** golden question sets per intent and per industry pack; metrics — intent accuracy, entity-link accuracy, plan validity rate, **execution accuracy** (result-set equality), groundedness, hallucination rate, refusal correctness, clarification precision, latency, tokens. Proposal gates: ≥ 95 % execution accuracy on Tier-1 deterministic intents; ≥ 0.95 groundedness on narrated answers; 0 policy-violating results in the adversarial set. | P0 |
| SR-NLQ-011 | **Safety:** refuse or constrain questions the user is not entitled to; never reveal existence of hidden entities ("redaction notice" lists the *fact* that filters applied, not the content). | P0 |
| SR-NLQ-012 | **Feedback loop:** thumbs/corrections/"this edge is wrong" feed a curation queue that improves mappings, aliases, intent templates and ranking, with steward approval. | P1 |
| SR-NLQ-013 | **Voice and chat surfaces:** same pipeline via chat apps (Teams/Slack-class), IDE chat, CLI, and optional speech I/O. | P2 |
| SR-NLQ-014 | **What-if simulation:** sandboxed copy-on-write overlay graph where users propose changes (delete service, rotate account, add dependency) and see propagated impact before acting; overlay never alters production truth. | P1 |
| SR-NLQ-015 | **Proactive suggestions:** based on role, current entity and usage graph, the UI proposes "questions you might ask next" (e.g., owners to notify, tests to run). | P1 |

---

## 10. Model Abstraction Layer and External-LLM Data-Sharing Control

### 10.1 Model abstraction

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-LLM-001 | **Model Provider Port** for chat/completion, structured output (grammar/JSON-schema constrained), tool calling, embeddings, reranking, vision/OCR, speech; capability negotiation (context length, modalities, tools, determinism). | P0 |
| SR-LLM-002 | **Local/self-hosted by default.** Adapters for local runtimes (vLLM-, SGLang-, llama.cpp-, Ollama-, TGI-, ONNX Runtime-, OpenVINO-, TensorRT-LLM-class). **No external provider adapter is active until explicitly enabled by an authorized tenant administrator** (§10.2). | P0 |
| SR-LLM-003 | **Model registry:** per model — source, hash, license terms (open-weight licenses differ and some restrict commercial redistribution), intended tasks, hardware profile, evaluation scores, approval status; offline model bundles with signature verification. | P0 |
| SR-LLM-004 | **Task-based routing:** small/fast models for classification, extraction and routing; larger models for synthesis; fallbacks and circuit breakers; per-tenant model allowlists. | P0 |
| SR-LLM-005 | **Hardware reference configurations** (CPU-only small model; single-GPU; multi-GPU; air-gapped appliance) with sizing guidance, quantization options, throughput/latency benchmarks per release. | P0 |
| SR-LLM-006 | **Prompt/skill registry:** versioned prompts, schemas, few-shot sets; A/B and regression-evaluated; tenant overrides; prompt content never contains raw sensitive data unless policy allows. | P0 |
| SR-LLM-007 | **Embedding service** with model versioning, batch/online modes, multilingual and code models, and re-embedding jobs (SR-VDB-005). | P0 |
| SR-LLM-008 | **LLM observability:** per-call latency, tokens, cost, cache hits, refusals, guardrail triggers, quality scores — local telemetry only unless the tenant exports it. | P0 |
| SR-LLM-009 | **Guardrails:** input/output scanners (PII, secrets, injection patterns), tool allowlists, output schema validation, jailbreak/prompt-injection test corpus in CI (aligned with the OWASP LLM Top-10 categories). | P0 |

### 10.2 External-endpoint enablement and data-sharing policy

External LLM/embedding/OCR endpoints (any hosted provider, including hyperscaler-hosted models) are **opt-in**, **policy-gated**, and **observable**.

**Dimension A — data classes** (what the data is): `D0 public` · `D1 metadata/schema/ontology labels` · `D2 internal business facts` · `D3 confidential` · `D4 restricted` (PII, PHI, PCI, credentials/secrets, privileged legal, export-controlled, classified). Orthogonal tags: `PII, PHI, PCI, SECRET, SOURCE_CODE, IP, LEGAL_PRIVILEGED, EXPORT_CONTROLLED, EMPLOYEE, CUSTOMER, FINANCIAL, GEO`.

**Dimension B — sharing levels** (what form leaves):

| Level | Name | What may leave the boundary |
| --- | --- | --- |
| S0 | **None** (default) | Nothing; local models only |
| S1 | Schema-only | Ontology/type names and field names, no values |
| S2 | Aggregates | Counts/statistics with small-cell suppression (k-anonymity threshold; differential privacy optional at P2) |
| S3 | Synthetic | Generated look-alike data preserving shape, never derived 1:1 from real records |
| S4 | Tokenized / pseudonymized | Values replaced by reversible tokens; token vault stays local; model sees tokens only |
| S5 | Redacted excerpts | DLP-masked minimal passages |
| S6 | Minimized full context with **per-request human approval** | Exactly the previewed payload |
| S7 | Full | Only for data the tenant designates as shareable (e.g., D0) |

**Policy matrix:** `(data class/tags) × (task type) × (endpoint) × (user role) × (region/jurisdiction) → max sharing level + approval requirement + retention assertion`. Most-restrictive-wins across layers (platform → partner → tenant → workspace → user).

```yaml
llm_egress:
  default_level: S0
  endpoints:
    - id: ext-gpt-eu
      type: external
      url_allowlist: ["https://llm.example-provider.eu"]
      region: EU
      tls: { mtls: true, pin_sha256: "..." }
      contract_attestations: { zero_retention: true, no_training: true, dpa_ref: "DPA-2026-17" }
      enabled: false                  # nothing leaves until an admin flips this, with audit + approval
  policy:
    - match: { class: [D0, D1], tasks: [summarize, classify] }
      max_level: S7
    - match: { tags: [PII, PHI, PCI, SECRET, SOURCE_CODE] }
      max_level: S1
    - match: { class: D3, tasks: [report_narration], roles: [analyst] }
      max_level: S4
      approval: none
    - match: { class: D4 }
      max_level: S0
  on_denied: fallback_to_local
```

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-LLM-010 | **Egress Gateway** is the *only* path to any external model; enforced by network policy so bypass is technically impossible. | P0 |
| SR-LLM-011 | **Policy engine** evaluates every outbound call against the matrix, transforms the payload to the permitted level (schema-strip, aggregate, synthesize, tokenize, redact), and blocks on failure. Default is S0 for all tenants. | P0 |
| SR-LLM-012 | **Dry-run preview:** administrators and (for S6) requesters see the *exact* payload that would be sent before approval. | P0 |
| SR-LLM-013 | **Per-call Egress Manifest** (immutable): who, what data classes, which level, which fields/tokens, endpoint, region, byte counts, approval id, response hash. A "what left the building" report is exportable for auditors. | P0 |
| SR-LLM-014 | **DLP and canary testing:** outbound payloads are scanned (PII/secret/PHI patterns, entropy, customer-defined dictionaries); CI plants canary values in test tenants and fails the build if any canary appears in outbound traffic below the allowed level. | P0 |
| SR-LLM-015 | **Reversible tokenization vault** (local, per-tenant keys) re-identifies model responses locally; responses are also scanned before display. | P0 |
| SR-LLM-016 | **Kill switch and budgets:** global/tenant/endpoint disable, rate and cost budgets, anomaly alerts on egress volume. | P0 |
| SR-LLM-017 | **Consent and contract records:** enabling an endpoint records the signer, date, DPA reference, data-residency region and scope; changes require re-approval. | P0 |
| SR-LLM-018 | **Same policy applies to embeddings, OCR, speech, reranking and telemetry** — not only chat models. | P0 |
| SR-LLM-019 | **Local fallback:** on denial or outage, tasks fall back to local models or deterministic modes with a visible notice. | P0 |
| SR-LLM-020 | **Region and sovereignty pinning:** endpoints and processing regions are constrained per tenant/jurisdiction. | P1 |

---

## 11. Agents, Automation and the "Living Brain"

### 11.1 Agent framework

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-AGT-001 | **Agent contract** (JSON schema): identity, purpose, allowed tools, input/output schemas, budgets (steps, tokens, time, expansions), risk class, approval mode, memory scope, evaluation hooks. Agents are data, versioned and reviewable. | P0 |
| SR-AGT-002 | **Bounded runtime:** tool allowlist, budget enforcement, circuit breaker, loop/stall detection, deterministic replay from traces. | P0 |
| SR-AGT-003 | **Autonomy modes:** HITL (human approves each action), HOTL (human monitors, can intervene), HIC (human in command; autonomy scoped by policy). Mode is a policy per agent × action risk class × tenant. | P0 |
| SR-AGT-004 | **Read/write separation:** default agents are read-only; any write/action tool requires an explicit approval boundary, audit and (where configured) dual control. | P0 |
| SR-AGT-005 | **MCP servers:** a read-only MCP server exposing graph, query, evidence and lineage tools; a separately governed action server; inventories generated from code; per-tenant auth and rate limits. | P0 |
| SR-AGT-006 | **Memory:** scoped (turn/session/user/workspace/tenant), policy-governed, expiring, inspectable and erasable; no cross-tenant memory. | P0 |
| SR-AGT-007 | **Agent registry & marketplace:** discover, install, evaluate and certify agents; signed packages; capability declarations. | P1 |
| SR-AGT-008 | **Multi-agent orchestration:** planner/critic/worker patterns, event-driven coordination, shared evidence blackboard, XAI trace per run. | P1 |
| SR-AGT-009 | **Controlled self-improvement is OFF by default;** proposals (prompt, mapping, ontology, rule changes) are generated as reviewable change requests, never self-applied. | P0 |
| SR-AGT-010 | **Specialist agent catalog** (starting set inherited from the codebase, plus new): DataQuality, OntologyReview, ConnectorDiagnosis, DocumentationFreshness, EvidenceVerification, ArchitectureConformance, QueryOptimization, GraphInvestigator, KnowledgeCurator, ChangeImpact, IncidentInvestigation; new: ComplianceMapper, ImpactSimulator, ExpertFinder, KnowledgeDebt, ReportWriter, OntologyInduction, ThreatPathAnalyst. | P1 |
| SR-AGT-011 | **RPA/workflow hooks:** approved agent outputs may trigger tickets, PR comments, notifications or runbook steps through connectors, always with human approval unless policy allows. | P1 |

### 11.2 Living-brain capabilities

| ID | Capability | Pri |
| --- | --- | --- |
| SR-AGT-020 | **Continuous sync and change detection:** the brain updates on source change; users can **watch** an entity, pattern or question and get alerts when answers change ("continuous queries"). | P1 |
| SR-AGT-021 | **Drift and conformance detection:** docs vs code, architecture vs deployment, ontology vs data, policy vs access, declared vs observed dependencies. | P1 |
| SR-AGT-022 | **Freshness and knowledge-decay scoring:** per node/edge/source; stale knowledge is visibly flagged and down-ranked. | P0 |
| SR-AGT-023 | **Knowledge-debt and bus-factor analysis:** single-owner components, orphaned systems, undocumented critical dependencies. | P1 |
| SR-AGT-024 | **Expert finder and routing:** who knows/owns/changed what, with identity-resolved evidence; "who should I ask?". | P1 |
| SR-AGT-025 | **Risk scoring:** change risk = blast radius × fragility × test coverage × recent-incident correlation; surfaced in PR/change-request bots. | P1 |
| SR-AGT-026 | **Anomaly detection** on graph structure, ingestion patterns and access behavior. | P2 |
| SR-AGT-027 | **Digest and briefing:** scheduled personalized briefings (what changed, what's at risk, open items) per role. | P1 |
| SR-AGT-028 | **Onboarding and tours:** auto-generated "map of this domain" guides for newcomers from the graph. | P2 |
| SR-AGT-029 | **Digital-twin mode:** model processes/assets/organizations as simulatable graphs for scenario planning (links to SR-NLQ-014). | P3 |

---

## 12. Multi-Tenancy, White-Label, Configuration and Extensibility

### 12.1 Tenancy model

Hierarchy: **Platform operator → Partner/Reseller → Tenant (organization) → Business unit → Workspace → User/Agent.**

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-TEN-001 | **Tenant context is mandatory** in every API, query, job, event, cache key, log line, metric label, agent call and plugin invocation; code paths without tenant context fail closed. | P0 |
| SR-TEN-002 | **Three isolation models**, selectable per tenant/edition: *Silo* (dedicated stack), *Bridge* (shared compute, dedicated data stores/namespaces), *Pool* (shared everything, logical isolation). | P0 (Silo, Bridge) / P1 (Pool) |
| SR-TEN-003 | Isolation is enforced at **every layer:** graph (database/graph-space/namespace per tenant), vector (collection), search (index), relational (schema + row-level security), object (bucket/prefix), event topics, secrets, KMS keys, caches, logs, backups, exports. | P0 |
| SR-TEN-004 | **Automated cross-tenant penetration suite** (every endpoint, job type and plugin hook attempts cross-tenant reads/writes/side-channels) MUST pass in CI and before each release. | P0 |
| SR-TEN-005 | **Per-tenant keys** (envelope encryption; BYOK and hold-your-own-key options), **crypto-shredding** on tenant deletion. | P0 |
| SR-TEN-006 | **Noisy-neighbor control:** quotas (graph size, ingestion rate, concurrent queries, LLM tokens, storage), fair scheduling, priority lanes, per-tenant rate limits and circuit breakers. | P0 |
| SR-TEN-007 | **Tenant lifecycle:** provision (API + console + IaC), configure, suspend, resume, clone (staging), migrate (cluster/region), export, delete (verified, certificate of destruction). | P0 |
| SR-TEN-008 | **Per-tenant everything:** ontology extensions, connectors, mappings, model allowlist, egress policy, retention, region, SSO, branding, SLA tier, feature entitlements. | P0 |
| SR-TEN-009 | **Metering and entitlements:** local, tamper-evident usage meters (records ingested, graph size, queries, LLM tokens, storage, seats, connectors) with export for billing; entitlements enforce edition/module limits; offline-capable. | P0 |
| SR-TEN-010 | **Cross-tenant sharing (opt-in):** controlled sharing of ontologies, mappings, templates and anonymized benchmarks; never raw data; always explicit and auditable. | P2 |

### 12.2 White-label / OEM

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-WL-001 | **Brand tokens:** logo(s), favicon, app name, colors, typography, spacing, icon sets, node/edge visual styles per ontology type, light/dark themes — all via theme packages, no code change. | P0 |
| SR-WL-002 | **Domain and identity:** custom domains/CNAMEs, tenant-supplied TLS certs, branded login/SSO pages, branded transactional email, branded PDF/DOCX/PPTX/HTML reports. | P0 |
| SR-WL-003 | **Terminology and persona white-labelling:** tenant renames concepts (SR-ONT-007) and names/styles the AI assistant (name, tone, avatar, greeting) without altering safety behavior. | P0 |
| SR-WL-004 | **De-vendoring:** vendor identifiers removable from UI, docs, CLI binary names, container/image names, package names, API hostnames, error pages and installers; "powered by" is a licensed toggle. | P0 |
| SR-WL-005 | **OEM rebuild pipeline:** partners can produce rebranded, re-signed bundles/appliance images from a documented pipeline; partner-owned update channel and docs portal. | P1 |
| SR-WL-006 | **Localization packs:** UI strings, date/number formats, RTL, glossary translation; partner-supplied language packs. | P0 |
| SR-WL-007 | **Custom legal and onboarding content:** terms, privacy notices, welcome tours, help links. | P0 |
| SR-WL-008 | **Partner console:** create/branding/configure tenants, view fleet health and usage, apply partner policy floors, issue licenses, manage support entitlements. | P1 |
| SR-WL-009 | **Embeddable components:** iframe/web-component widgets (NL console, graph viewer, impact panel) with token-based auth for embedding in customer or partner portals. | P1 |

### 12.3 Configuration framework ("everything customizable", safely)

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-CFG-001 | **Layered configuration:** product default → edition → partner → tenant → business unit → workspace → user. Each setting is typed (JSON Schema), documented, validated, versioned and audited. | P0 |
| SR-CFG-002 | **Floors and ceilings:** upper layers may set security/compliance *floors* and *ceilings* lower layers cannot loosen (e.g., tenant cannot enable external LLMs beyond partner-allowed levels). Most-restrictive-wins for security settings. | P0 |
| SR-CFG-003 | **Effective-config explain:** "why does this setting have this value?" shows the layer chain and last change. | P0 |
| SR-CFG-004 | **Config as code:** export/import (YAML/JSON), GitOps promotion dev → stage → prod, diff, dry-run, rollback, change approval workflow. | P0 |
| SR-CFG-005 | **Feature flags and entitlements** distinct from configuration; flags never bypass policy. | P0 |
| SR-CFG-006 | **Hot reload** for non-structural settings; structural changes (backend bindings, ontology major versions) go through migration plans. | P1 |

**Configuration domain catalog (each MUST be configurable):**

| Domain | Examples |
| --- | --- |
| Branding & UX | themes, navigation, home dashboards, default views, widgets, node/edge styling, report templates |
| Terminology & ontology | renamed concepts, extensions, glossaries, validation rules, mapping templates |
| Connectors & pipelines | sources, schedules, windows, rate limits, retention of raw, DLQ policy, mapping versions |
| Storage bindings | graph/vector/search/relational/object/bus providers, per-domain placement, tiering |
| Query & NL | enabled languages, default dialects, intents and templates, suggestion behavior, answer depth/tone, languages, cost limits |
| Models & egress | models, routing, hardware profile, sharing levels, endpoints, approvals, budgets |
| Agents | enablement, tools, autonomy modes, budgets, approval chains, memory scopes |
| Security | SSO/MFA, session policy, IP allowlists, roles/attributes, key management, break-glass |
| Privacy & governance | classification rules, retention, legal hold, residency, DSAR workflow, SoD, approval workflows |
| Compliance | packs enabled, control mappings, evidence schedules |
| Reliability & performance | quotas, timeouts, caching, HA/DR profile, backup schedule |
| Observability | sinks, sampling, alert rules, log levels |
| Licensing | editions, modules, seats, size tier |

### 12.4 APIs and SDKs

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-EXT-001 | **Headless first:** every UI capability is available through public, versioned APIs — REST (OpenAPI 3.1), GraphQL (ontology-generated), gRPC (high-volume), WebSocket/SSE (streaming answers, subscriptions), webhooks, MCP, CLI. | P0 |
| SR-EXT-002 | API standards: semantic versioning, ≥ 12-month deprecation window, idempotency keys, cursor pagination, async job pattern, consistent error model, rate-limit headers, generated reference and SDKs. | P0 |
| SR-EXT-003 | **Admin APIs** cover tenants, users, config, branding, licenses, connectors, policies — enabling partner automation. | P0 |
| SR-EXT-004 | Official SDKs: Python, TypeScript at P0; Java/Kotlin, Go, .NET at P1; Jupyter/notebook integrations. | P0/P1 |
| SR-EXT-005 | **Integration surface:** Slack/Teams-class ChatOps, ITSM (ServiceNow/Jira), CI/CD bots (PR impact comments, merge-risk gates), SIEM, email, calendar, BI tools (SR-ING-071), IDE extensions (VS Code at P0; JetBrains at P1). | P1 |

### 12.5 Plugin and extension runtime

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-EXT-010 | **Extension points:** connectors, parsers/extractors, relationship-discovery methods, identity-resolution matchers, graph algorithms, store adapters, query-dialect adapters, model providers, agents/skills, UI pages/widgets, report templates, validation/policy/ontology packs, notification channels, auth providers, export formats. | P0 (core 8) / P1 |
| SR-EXT-011 | **Isolation:** each plugin runs in a container or WASM sandbox with declared capabilities (network, filesystem, secrets, graph read/write scopes), CPU/memory/time limits, health checks and no ambient authority. | P0 |
| SR-EXT-012 | **Signed, versioned packages** with manifest, compatibility range, Data-Flow Manifest, SBOM and test fixtures; trust levels (first-party / certified partner / community / private). | P0 |
| SR-EXT-013 | **Plugin test kit** and scaffolding CLI; contract tests mandatory for marketplace listing. | P1 |
| SR-EXT-014 | **Marketplace** (online catalog for connected profiles; **offline catalog bundles** for air-gapped): ratings, security scan results, certification badges, revenue-share support. | P1 |
| SR-EXT-015 | **Low-code Studio:** visual pipeline, mapping, rule, agent and report builders that emit the same versioned artifacts as code. | P1 |

---

## 13. User Experience

### 13.1 Applications (modular, individually licensable, one design system)

NL Console & Explorer · Ontology Studio · Mapping & Pipeline Studio · Connector Manager · Query Workbench (multi-language editor with autocomplete, explain, profiling) · Impact & Lineage · Report Studio · Governance & Quality Console · Agent Studio · Dashboard Builder · Admin & Tenant Console · Partner/Operator Console · IDE extensions and CLI.

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-UX-001 | **No mock UI:** every screen reads live APIs; hardcoded demo data is allowed only in an explicit, labeled Demo Mode. UI acceptance tests assert real backend calls. | P0 |
| SR-UX-002 | **Graph visualization at scale:** WebGL rendering, level-of-detail and semantic zoom, bounded subgraph fetch, clustering/community collapse, multiple layouts (force, hierarchical, radial, geo), 2D/3D, minimap, path highlighting, blast-radius overlay; interactive at ≥ 50 k visible elements with LOD, ≥ 5 k fully detailed. | P0 |
| SR-UX-003 | **Alternate views:** table, matrix (dependency/DSM), tree/hierarchy, Sankey/flow, timeline/scrubber (temporal), geo-map, diff view between revisions. | P1 |
| SR-UX-004 | **Honest visual encoding:** edge style encodes class and confidence (asserted/derived/inferred/curated); freshness shading; provenance drawer ("show evidence") one click from any element or answer sentence. | P0 |
| SR-UX-005 | **NL console:** suggestion cards (SR-NLQ-002), query preview (EOQL + dialect), evidence panel, mode badge (deterministic/narrated/exploratory/report), follow-up chips, investigation canvas that pins entities, paths and findings. | P0 |
| SR-UX-006 | **Persona-based homes** and role-aware navigation (executive, architect, engineer, steward, auditor, admin), fully configurable. | P1 |
| SR-UX-007 | **Collaboration:** comments, annotations, @mentions, shared investigations/views, review of proposed ontology/mapping changes, activity feed. | P1 |
| SR-UX-008 | **Accessibility:** WCAG 2.2 AA, keyboard-first, screen-reader semantics for graph (alt text paths, tabular fallback), reduced-motion, color-blind-safe palettes. | P0 |
| SR-UX-009 | **Responsive and mobile read:** tablet/phone views for answers, alerts and approvals. | P1 |
| SR-UX-010 | **Onboarding:** guided setup wizard (connect → profile → map → validate → ask), sample-data sandbox, in-product help, "what can I ask?" explorer driven by the meta-graph. | P0 |
| SR-UX-011 | **Destructive-action safety:** confirmations with impact preview, undo where possible, dual control for configured classes. | P0 |
| SR-UX-012 | **Performance budget:** initial load ≤ 3 s on reference hardware over LAN; interactions ≤ 200 ms for local operations. | P1 |

---

## 14. Security, Privacy, Compliance and Governance

### 14.1 Identity, access and policy

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-SEC-001 | **Authentication:** OIDC, SAML 2.0, LDAP/AD, SCIM 2.0 provisioning, local break-glass accounts, MFA (TOTP, WebAuthn/FIDO2), scoped API keys, OAuth2 client credentials, mTLS service identities, short-lived tokens, session controls. | P0 |
| SR-SEC-002 | **Authorization:** RBAC + ABAC + relationship-based (Zanzibar-style) checks + classification-based mandatory access; evaluated by a policy engine (policy-as-code, OPA/Cedar-class) with a test and **"what can this user see?" simulation** tool. | P0 |
| SR-SEC-003 | **Element-level security:** policies apply to vertices, edges, properties and derived structures (embeddings, summaries, communities, caches); query-time policy rewriting and result filtering; field masking; purpose-based and time-bound (JIT) access; segregation of duties. | P0 |
| SR-SEC-004 | **Permission-aware ingestion and retrieval:** where the source provides ACLs/permissions, the connector ingests and maps them so answers include only what the asking user could access in the source system; unmapped ACLs default to deny. This MUST also govern RAG context assembly and community summaries (summaries of restricted content are themselves restricted). | P0 |
| SR-SEC-005 | **Access governance:** access reviews/certification campaigns, privileged-access workflows, break-glass with mandatory post-hoc review. | P1 |
| SR-SEC-006 | **Agent identities** are first-class principals with least-privilege roles and budgets; agents never inherit a human's full rights implicitly. | P0 |

### 14.2 Platform and supply-chain security

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-SEC-010 | **Encryption:** TLS 1.3 externally, mTLS internally; at-rest encryption for all stores; field-level encryption for sensitive properties; KMS/HSM integration (PKCS#11, KMIP, cloud KMS adapters); rotation; optional FIPS 140-validated crypto modules. | P0 |
| SR-SEC-011 | **Secrets:** mounted files/secret store only; no secrets in environment variables, images, logs, graph or embeddings; automated secret scanning on ingested content with quarantine. | P0 |
| SR-SEC-012 | **Audit:** immutable, hash-chained, signed, exportable (WORM option, SIEM formats); covers authN/Z decisions, config, data access (detail configurable), policy decisions, egress manifests, admin and agent actions; retention configurable. | P0 |
| SR-SEC-013 | **Hardening:** non-root containers, read-only root FS, dropped capabilities, seccomp/AppArmor profiles, minimal signed base images, network segmentation, CIS-aligned benchmarks. | P0 |
| SR-SEC-014 | **Supply chain:** SBOM (CycloneDX/SPDX) per image and release, VEX, signed images/artifacts (Sigstore/cosign-class), SLSA-aligned provenance, pinned and reproducible builds, license scanning, dependency review. | P0 |
| SR-SEC-015 | **Secure SDLC:** threat models (STRIDE + LLM-specific + multi-tenant), SAST/DAST/SCA/fuzzing in CI, annual independent penetration test, vulnerability disclosure program, patch SLAs, security advisories channel. | P0 |
| SR-SEC-016 | **Web and API defenses:** CSP, CSRF/XSS protections, SSRF guards for connectors and model endpoints, input validation, request size/time limits, DoS and abuse controls. | P0 |
| SR-SEC-017 | **LLM-specific security:** prompt-injection and data-exfiltration test corpus, output filtering, tool-permission enforcement, context isolation per tenant/user (aligned with OWASP LLM Top-10 categories). | P0 |

### 14.3 Privacy engineering

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-PRV-001 | **Classification engine** at ingest (patterns, dictionaries, NER, ML; customer-extensible) labels PII/PHI/PCI/secrets/IP/legal-privileged/export-controlled; labels propagate to derived data. | P0 |
| SR-PRV-002 | **Data-subject requests:** locate a subject across graph, raw captures, vector/search indexes, caches, derived graphs, exports and backups (flagged); execute access/export, rectification and **erasure with propagation** (including embeddings and summaries) and produce proof. | P0 |
| SR-PRV-003 | **Retention and legal hold** per class/tenant/source; automated expiry with crypto-shred option. | P0 |
| SR-PRV-004 | **Purpose and consent tracking** where applicable; purpose limitation enforced in policy. | P1 |
| SR-PRV-005 | **Compliance from the graph:** auto-generate records of processing, data maps, data-flow diagrams, system-to-data-class inventories, cross-border transfer views and DPIA starter reports from the graph itself. | P1 |
| SR-PRV-006 | **Residency enforcement:** region pinning for storage, processing and model endpoints; cross-border transfer controls. | P0 |
| SR-PRV-007 | **Pseudonymization/anonymization services** (tokenization, k-anonymity checks, optional differential-privacy aggregates). | P1 |

### 14.4 Compliance and AI governance (the product supports customer compliance; vendor certifications are separate programs — do not claim any certification until attested)

| Area | Frameworks to map (control mapping, evidence collectors, policy and report templates as "Compliance Packs") |
| --- | --- |
| Privacy | GDPR/UK GDPR, CCPA/CPRA, India DPDP Act 2023, LGPD, PIPEDA |
| Security | SOC 2, ISO/IEC 27001/27017/27018/27701, NIST CSF, NIST SP 800-53/800-171, CMMC, FedRAMP-aligned controls, NIS2, DORA |
| Industry | HIPAA/HITECH, PCI DSS, SOX, GxP and 21 CFR Part 11, FERPA, CJIS, BCBS 239, NERC CIP |
| Trade | Export-control classification of the product (including cryptography), ITAR/EAR handling guidance for customers |
| AI | ISO/IEC 42001, NIST AI RMF, EU AI Act (risk classification, transparency, logging, human oversight) |

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-GOV-001 | **Compliance Pack format:** control catalog, mapping to platform capabilities, automated evidence queries over the graph/audit, report templates, gap analysis. | P1 |
| SR-GOV-002 | **AI governance:** model cards, AI-BOM, evaluation records, intended-use and prohibited-use settings, human-oversight configuration, user-visible AI labeling, AI incident workflow. | P0 |
| SR-GOV-003 | **Change governance:** ontology, mapping, policy, model and agent changes use proposal → review → approval → rollout with audit and rollback. | P0 |
| SR-GOV-004 | **Roles:** data owners, stewards, custodians, ontology curators, security admins, auditors (read-only, tamper-evident views). | P0 |
| SR-GOV-005 | **Policy exceptions** are time-boxed, approved, visible and auto-expiring. | P1 |

---

## 15. Non-Functional Requirements: Performance, Scale, Reliability, Operations

### 15.1 Service-level objectives (Proposal — every number is a target to be validated on reference hardware and published only after measurement)

| Metric | S | M | L |
| --- | --- | --- | --- |
| Point lookup / alias resolution p95 | ≤ 100 ms | ≤ 100 ms | ≤ 150 ms |
| 3-hop traversal p95 (typical dataset; source baseline ≤ 2 s) | ≤ 2 s | ≤ 2 s | ≤ 3 s |
| Bounded impact analysis (≤ 6 hops, ≤ 500 results) p95 | ≤ 3 s (≤ 1 s with accelerators) | ≤ 5 s (≤ 1.5 s) | ≤ 8 s (≤ 2 s) |
| Deterministic NL intent end-to-end p95 (no clarification) | ≤ 4 s | ≤ 4 s | ≤ 6 s |
| Narrated answer, first token (GPU reference config) | ≤ 3 s | ≤ 3 s | ≤ 4 s |
| Report generation (10-section) | ≤ 3 min | ≤ 5 min | ≤ 10 min |
| API availability (HA edition) | 99.5 % | 99.9 % | 99.95 % |
| Backup RPO / restore RTO | 24 h / 8 h | ≤ 15 min / ≤ 2 h | ≤ 5 min / ≤ 1 h |
| Cross-site DR (optional) RPO / RTO | — | ≤ 15 min / ≤ 4 h | ≤ 5 min / ≤ 2 h |

### 15.2 Scalability and reliability requirements

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-NFR-001 | **Horizontal scale** for API, query, ingestion workers, agent runners, embedding and model-serving tiers; autoscaling policies (K8s) and manual sizing for appliances. | P0 |
| SR-NFR-002 | **Data scaling patterns:** graph partitioning/sharding per backend capability, read replicas, tenant-based partitioning, hot/warm/cold tiering, archive to object storage with rehydration, vector index sharding, search index lifecycle management. | P1 |
| SR-NFR-003 | **Query protection:** admission control, per-tenant concurrency, cost-based throttling, kill-runaway-query, result streaming and spill, plan caching. | P0 |
| SR-NFR-004 | **Graceful degradation matrix** (documented and tested): vector down → text/graph retrieval; model down → deterministic + evidence (SR-RAG-008); search down → graph-only; bus lag → stale-flag; one backend down → federated partial results with notice. | P0 |
| SR-NFR-005 | **Backup/restore:** native backend backups and logical checksummed archives; consistent multi-store snapshots (graph + vector + search + relational + object + event log) with crash-atomic recovery; point-in-time recovery via event log + revisions; restore drills automated with golden-query verification. | P0 |
| SR-NFR-006 | **Upgrades:** rolling and blue/green for clustered; offline signed upgrade bundles for air-gapped; versioned idempotent schema/ontology migrations; tested downgrade/rollback; compatibility matrix; LTS and stable channels (LTS ≥ 24 months). | P0 |
| SR-NFR-007 | **Chaos and soak testing:** node/zone failure, partition, slow disk, clock skew, backend restart mid-ingest; 7-day soak per release. | P1 |
| SR-NFR-008 | **Capacity planning tools:** sizing calculator and in-product forecasts (graph growth, index size, GPU needs) with reference architectures per tier. | P1 |

### 15.3 Observability and supportability

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-OPS-001 | **OpenTelemetry** metrics, logs and traces end-to-end (ingestion → mutation → query → answer); local sinks (Prometheus/Grafana/Loki/Tempo-class) bundled; customer sinks pluggable. Structured JSON logs with correlation IDs, no secrets, no raw sensitive values. | P0 |
| SR-OPS-002 | **Health and readiness** endpoints per service; dependency health roll-up; SLO dashboards and alert rules shipped as code. | P0 |
| SR-OPS-003 | **Support bundle:** one command/UI action produces a redacted diagnostic archive; customer reviews before sharing. | P0 |
| SR-OPS-004 | **Telemetry to vendor is OFF by default;** optional, opt-in, content-free usage statistics with a visible schema. | P0 |
| SR-OPS-005 | **Runbooks** for connector failure, DLQ drain, graph restore, schema/ontology migration rollback, model outage, egress incident, tenant isolation incident, key rotation, DR failover. | P0 |
| SR-OPS-006 | **Cost/FinOps views** for cloud profiles (storage, compute, LLM tokens) and capacity views for on-prem. | P2 |

---

## 16. Deployment, Packaging and Delivery

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-DEP-001 | **Docker Compose** distribution for DP-0 with healthy-start verification and one-command clean-reset demo including backup/restore (inherited `MVP-FR-028`). | P0 |
| SR-DEP-002 | **Helm charts/operators** for Kubernetes (HA, autoscaling, network policies, pod security, PDBs) for DP-1…DP-4. | P1 |
| SR-DEP-003 | **Offline delivery:** signed OCI image archives, model bundles, ontology/industry packs, connector catalog, docs, license file, checksum manifest; verified by an installer **preflight checker** (OS, kernel, CPU/GPU, storage, ports, time sync, certificates). | P0 |
| SR-DEP-004 | **Appliance image** (hardware + software; CPU and GPU variants) with hardened OS, first-boot wizard, lifecycle updates. | P2 |
| SR-DEP-005 | **Native packages** (RPM/DEB) and VM images for customers without containers. | P2 |
| SR-DEP-006 | **Supported-platform matrix** (OS, kernel, Kubernetes, container runtime, browsers, GPUs) maintained and tested per release. | P0 |
| SR-DEP-007 | **Offline licensing:** signed license files encoding edition, modules, size tier, tenants, seats, expiry; grace periods; **no license check may ever delete or lock customer data** (read-only degrade only); usage export for manual reporting. | P0 |
| SR-DEP-008 | **Edge/federation package** for DP-6: small footprint, offline-first, delta/summary sync with conflict policies and bandwidth limits. | P2 |
| SR-DEP-009 | **Reference architectures and hardening guides** per profile and tier, including network diagrams for air-gapped and connected variants. | P0 |

---

## 17. Quality, Evaluation and Release Gates

### 17.1 Test strategy

| Layer | Requirement |
| --- | --- |
| Unit / property-based | Connectors, parsers, identity resolution, mapping, policy, QueryPlan compiler |
| Contract | Every port (graph, vector, search, object, bus, model, IdP) and every plugin type |
| Conformance | Per-adapter suites with golden queries and failure injection |
| Dialect equivalence | IR → dialect result equivalence on shared fixtures (SR-QRY-004) |
| Integration / E2E | Ingestion → graph → query → NL → report on synthetic industry datasets; UI E2E (Playwright-class) against live APIs |
| NL & RAG evaluation | Golden sets per intent and industry; adversarial and injection sets (SR-NLQ-010, SR-RAG-010) |
| Security | SAST/DAST/SCA, fuzzing, secret scanning, **tenant-isolation suite**, **egress canary suite**, pen tests |
| Performance & scale | Ingestion, traversal, impact, NL latency, GPU throughput; **LDBC SNB/BI-style** graph benchmarks and RDF benchmarks (LUBM/BSBM-style) for relevant backends; soak and chaos |
| Operations | Backup/restore drills, upgrade/downgrade, DR failover, offline-bundle install on a clean machine |
| Accessibility & i18n | Automated and manual WCAG checks; RTL and locale tests |

### 17.2 Synthetic data

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-QA-001 | Provide **synthetic dataset generators** per industry pack (referentially consistent, with planted ground-truth relationships, duplicates, drift, PII canaries and adversarial prompt-injection documents). No real customer data in test assets. | P0 |
| SR-QA-002 | Each generator exposes scale knobs (S/M/L/XL) and ground-truth answers for the golden question sets. | P0 |

### 17.3 Traceability and gate integrity (lesson from the prior audit)

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-QA-010 | Every `SR-` requirement maps to ≥ 1 executable acceptance test; the mapping is stored as structured data (test-ID → requirement-ID), **and references in comments or docstrings never count as evidence.** | P0 |
| SR-QA-011 | A requirement is `Done` only if its mapped tests pass **and** a mutation/negative check proves the test fails when the behavior is broken (sampled per release). | P0 |
| SR-QA-012 | Status dashboards MUST report three numbers separately: *tests passing*, *requirements with behavioral evidence*, *requirements with external-gate evidence*; a single "% complete" is prohibited. | P0 |
| SR-QA-013 | Generated inventories (API routes, tools, labels, algorithms, commands) come from code introspection; hand-written counts fail the docs build. | P0 |
| SR-QA-014 | Linters/type-checkers/security scanners run at zero-error policy on main (the prior baseline carried 165 lint errors, mostly mechanical). | P0 |

### 17.4 GA release gates (all MUST pass)

1. All P0 requirements `Done` with behavioral evidence, or an approved, time-boxed exception recorded as an ADR.
2. Inherited open external gates (Appendix C) closed or explicitly de-scoped by the product owner.
3. Tenant-isolation, egress-canary, prompt-injection and permission-leak suites green.
4. SBOM, license report, vulnerability scan, signed artifacts, reproducible-build check.
5. Backup/restore and upgrade/rollback drills passed on Tier A backends.
6. Performance report against §15.1 on published reference hardware.
7. Independent security review and penetration test completed; findings triaged.
8. Documentation, runbooks and compliance packs complete for the release.

---

## 18. Commercialization

### 18.1 Editions and modular SKUs

| Edition | Intended buyer | Notes |
| --- | --- | --- |
| Community / Evaluation | Developers, PoC | Limited size and connectors, no white-label, time-boxed commercial evaluation license |
| Professional | Departments, SMEs | Single tenant, core packs |
| Enterprise (on-prem) | Large organizations | HA, SSO/SCIM, compliance packs, support SLAs |
| Appliance | Regulated / air-gapped | Hardware + software + lifecycle service |
| Partner / OEM (white-label, multi-tenant) | Integrators, ISVs, resellers | Partner console, rebuild pipeline, tenant metering |
| Managed (partner- or vendor-hosted) | Customers who want a service | DP-5 |

**Modular packs (individually licensable, one ecosystem):** Core Graph & Ingestion · NL & GraphRAG · Ontology Studio · Agents & MCP · Governance & Compliance · Multi-Tenant & White-Label · Connector Packs (by domain) · Industry Packs · Advanced Analytics/Graph ML · Edge & Federation.

### 18.2 Requirements

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-COM-001 | **Licensing models** supported by the entitlement system: perpetual + annual support, annual subscription, size-tier/usage-based, per-tenant (OEM/managed), seat-based add-ons, revenue-share/royalty for OEM. | P0 |
| SR-COM-002 | **PoC kit:** 30-day evaluation license, per-industry demo datasets, scripted demo flows, sizing tool, ROI calculator, 10-question "prove it on your data" workshop template. | P0 |
| SR-COM-003 | **Legal and procurement kit:** EULA, MSA, DPA, SLA, OEM and partner agreements, BAA template, security questionnaire answers (SIG/CAIQ-style), SBOM and third-party notices, export-control classification, accessibility conformance report. | P0 |
| SR-COM-004 | **Support:** Standard / Priority / Enterprise / Mission-critical tiers with response targets, escalation paths, named technical account managers, support-bundle workflow. | P0 |
| SR-COM-005 | **Services:** onboarding, connector development, ontology engineering, NL tuning, training, compliance-pack onboarding, managed operations. | P0 |
| SR-COM-006 | **Partner program:** certification tracks (implementer, connector developer, ontology engineer), partner portal, deal registration, co-marketing assets. | P1 |
| SR-COM-007 | **Documentation set:** admin, user, API/SDK, connector developer, ontology guide, security whitepaper, architecture, reference deployments, runbooks, compliance mappings, release notes, upgrade guides, training curriculum. | P0 |
| SR-COM-008 | **Sales artifacts:** datasheets per module and industry, battlecards, demo environments, reference architectures, case-study templates. | P1 |
| SR-COM-009 | **Lifecycle policy:** versioning, LTS, end-of-support, security-patch commitments published. | P0 |
| SR-COM-010 | **Strategy decisions to record as ADRs:** open-core vs source-available vs closed; trademark and white-label rights; third-party component redistribution rights; IP assignment for plugins and marketplace content. | P0 |

---

## 19. Industry Packs (starter ontology + connectors + sample questions + compliance mappings)

| Industry | Core entities | Typical sources | Sample questions the pack MUST answer | Key obligations |
| --- | --- | --- | --- | --- |
| Software & IT operations (baseline) | Service, API, Repo, Commit, Change, Incident, Account, Environment | Git, Jira, ServiceNow, APM/logs, IaC | Q1–Q5 in §1.3 | SOC 2, ISO 27001 |
| Banking & financial services | Customer, Account, Product, Trade, Counterparty, Control, Report, Regulation | Core banking, trade systems, GRC, data lineage | "Which regulatory reports change if source field F changes?" "Which controls cover process P?" | BCBS 239, SOX, DORA, PCI DSS |
| Insurance | Policy, Claim, Coverage, Peril, Broker, Reinsurer | Policy admin, claims, geospatial | "Which policies are exposed to flood zone Z?" | Solvency-style reporting, ACORD |
| Healthcare & life sciences | Encounter, Order, Protocol, Drug, Lot, Device, Trial, Site (patients pseudonymous by default) | EHR/FHIR, LIMS, QMS, supply | "Which sites/protocols/products are affected by recalled lot L?" "Which datasets feed submission S?" | HIPAA, GxP, 21 CFR Part 11 |
| Manufacturing & supply chain | Part, BOM, Supplier, Plant, Line, Work order, Quality event | ERP, MES, PLM, QMS | "Which finished goods are affected if supplier S's part P is nonconforming?" | ISA-95, ISO 9001/IATF |
| Retail & consumer goods | SKU, Store, Supplier, Promotion, Order | ERP, POS, WMS | "Which stores and SKUs are exposed to this supplier outage?" | Product-safety, privacy |
| Energy & utilities | Asset, Substation, Feeder, Outage, Work order, Meter | SCADA/historian, GIS, EAM | "Which critical facilities lose supply if feeder F trips?" | NERC CIP, safety |
| Telecom | Cell site, Network element, Service, Customer, SLA, Ticket | OSS/BSS, inventory, NMS | "Which enterprise customers and SLAs are hit if element E fails?" | TM Forum SID, lawful-intercept controls |
| Government & public sector | Regulation, Agency, Program, Case, Asset, Procurement | Legacy systems, registries, document stores | "Which programs and systems are affected by amendment A to regulation R?" | Sovereignty, FedRAMP-style, records law |
| Legal & compliance | Contract, Clause, Party, Obligation, Matter, Regulation | CLM, DMS, email | "Which contracts contain clause C and renew within 90 days?" | Privilege handling, retention |
| Education | Course, Prerequisite, Outcome, Credential, Cohort (pseudonymous) | SIS, LMS, curriculum repos | "What changes if course C is retired?" | FERPA-style privacy |
| Logistics & transportation | Shipment, Route, Hub, Carrier, Asset, Customs event | TMS, WMS, telematics | "Which shipments are impacted by this port closure?" | Customs, trade controls |
| Cybersecurity & GRC | Asset, Vulnerability, Control, Threat, Identity, Attack path | Scanners, SIEM, CSPM, IAM, CMDB | "Which attack paths reach the crown-jewel database?" | NIST, ISO 27001, NIS2 |
| HR & workforce | Role, Skill, Team, Certification, Position (privacy-sensitive) | HRIS, LMS | "Which critical projects depend on a single holder of skill S?" | Employee-privacy law, works-council rules |

| ID | Requirement | Pri |
| --- | --- | --- |
| SR-COM-020 | Pack SDK and signed distribution format: ontology layer, mapping templates, connector bundles, validation/policy rules, glossary, sample dataset generator, golden questions, report templates, compliance pack references. | P0 |
| SR-COM-021 | Ship the Software/IT pack and **two non-IT packs** at GA to prove horizontal applicability; remaining packs on the roadmap (§20). | P0 |

---

## 20. Phased Roadmap

**Baseline B0 (as built, per the consolidated audit — treat as "Exists" until re-verified under §17.3):** Docker-local HugeGraph stack; Jira/Git/GitLab/Confluence/ServiceNow connectors (fixture-verified; live tenants are external gates); ingestion pipeline with DLQ/replay; ontology and 74/68 vertex/edge labels; provenance; identity resolution; meta-graph and bridge edges; QueryPlan, path/impact/entity search and NL interpretation; retrieval router and GraphRAG with local model abstraction; bounded agents and 11 specialist agents; MCP (18 tools); web, admin and VS Code surfaces; 29-entry algorithm registry; multi-backend registry (HugeGraph, Neptune, Neo4j, memory); marketplace/packager modules; roughly 1.9 k passing tests.

| Release | Window | Theme | Key scope | Exit criteria |
| --- | --- | --- | --- | --- |
| R1 | 0–4 mo | **Commercial foundation** | Real authN/Z (RBAC+ABAC) and tenant context end-to-end; tenant-isolation suite; layered config + floors/ceilings; offline licensing/entitlements; Egress Gateway + sharing levels S0–S7 + canary suite; model registry + hardware profiles; SBOM/signing/license matrix; vocabulary ADRs (C10); gate-integrity fixes (SR-QA-010…014); DP-0/DP-1 offline bundle; close external gates 1(single-node part), 2, 5, 8, 9, 14 | GA release gates 1, 3, 4 pass for R1 scope |
| R2 | 4–9 mo | **Breadth and intelligence** | Graph Store Port v2 + conformance kit; Tier A: HugeGraph, Neo4j, Neptune; vector adapters (embedded, pgvector, Qdrant, Milvus, Weaviate); QueryPlan IR with Gremlin/openCypher/SPARQL/EOQL; schema profiler and relationship discovery v2; edge classes; Ontology Studio; suggestion engine and entity disambiguation; report studio; white-label theming v1; Helm charts; permission-aware ingestion | Dialect-equivalence and NL evaluation gates met on synthetic packs |
| R3 | 9–15 mo | **Scale and enterprise** | Validated HA/sharded profiles; pool/bridge/silo tenancy GA; federation basics; GQL and SQL/PGQ front-ends; temporal/as-of queries; what-if overlay; privacy engine (DSAR, erasure propagation); compliance packs (GDPR, SOC 2, HIPAA, DPDP first); marketplace v1; Software/IT + 2 non-IT packs | Performance report on L tier; independent pen test; GA gates all pass |
| R4 | 15–24 mo | **Ecosystem** | Partner/OEM console and rebuild pipeline; appliance; edge/federation; 10+ industry packs; graph ML (embeddings, link prediction); certification program; multilingual NL | Partner pilot customers live |
| R5 | 24 mo+ | **Horizon** | Digital-twin mode; virtual/zero-ETL graph; autonomous curation with approvals; cross-tenant benchmark sharing | Research-gated |

*Mapping to the source roadmap:* the Super-Prompt's MVP/Phase 1–3 timeline assumed a greenfield build; because B0 exists, R1–R4 re-sequence the remaining commercial work and fold in the new multi-backend, white-label and external-LLM-policy requirements.

---

## 21. Risks and Open Decisions

### 21.1 Risk register

| ID | Risk | Mitigation |
| --- | --- | --- |
| RK-01 | "Support every backend/language" spreads the team thin | Tiered certification; IR-based compiler; conformance kit; publish support matrix honestly |
| RK-02 | License contamination (copyleft, network-copyleft, source-available, commercial-only components bundled in a sold product) | License matrix (SR-GDB-016), bring-your-own mode, legal gate in CI, clean-room rule |
| RK-03 | NL answer quality below customer expectation; hallucination erodes trust | Deterministic-first, evidence envelopes, corrective verification, evaluation gates, suggestion engine to avoid wrong queries |
| RK-04 | Permission leakage through RAG, summaries, caches or embeddings | SR-SEC-003/004, derived-data classification, leak test suite, per-user filter before ranking |
| RK-05 | Impact queries slow on dense graphs | Accelerators (SR-QRY-009), bounded traversal, pre-aggregation, tiered storage |
| RK-06 | Local-LLM hardware cost/availability blocks air-gapped customers | Small-model-first design, deterministic modes, hardware profiles, appliance SKU |
| RK-07 | White-label/OEM support burden | Partner certification, rebuild pipeline automation, support entitlements, partner-owned L1 |
| RK-08 | Compliance over-claiming | Separate "supports" from "certified"; legal review of all claims |
| RK-09 | Dialect/semantic divergence between backends | Golden-query equivalence, capability manifests, explicit degradation |
| RK-10 | Inference noise pollutes the graph | Edge classes, thresholds, review queues, exclusion of inferred edges from authoritative answers by default |
| RK-11 | Status/audit gaming recurs | SR-QA-010…013 |
| RK-12 | Indirect prompt injection from ingested documents | SR-ING-061, SR-SEC-017, fenced context, tool allowlists |
| RK-13 | Multi-tenant isolation defect | Fail-closed tenant context, isolation suite, silo option, per-tenant keys |
| RK-14 | Ontology sprawl and inconsistent extensions | Governance workflow, alignment tools, deprecation policy, quality dashboards |
| RK-15 | Upstream project changes (relicensing, abandonment, e.g., an embedded engine's maintenance status) | Adapter isolation, exit paths, migration tooling (SR-GDB-006) |
| RK-16 | Customer data heterogeneity exceeds auto-discovery | Human-in-the-loop Mapping Studio, steward queues, confidence reporting |

### 21.2 Decisions required from the product owner (record each as an ADR)

1. Product name, trademark and white-label rights model; open-core vs source-available vs closed.
2. Tier A backend set for GA (proposal: HugeGraph, Neo4j, Neptune; one RDF store).
3. Default tenancy model for the Managed edition (pool vs bridge).
4. Default embedded vector index and default local model family, each after license review.
5. Positioning of EOQL relative to GQL (long-term: EOQL as a GQL superset/facade?).
6. When to begin vendor attestations (SOC 2 Type II, ISO 27001) and which industry packs to certify first.
7. Which two non-IT packs ship at GA.
8. Hardware reference configurations to publish.
9. Pricing structure and metering definitions.
10. Whether DP-5 (hosted multi-tenant) is in scope for the first two years.

---

## Appendix A — Glossary

**Blast radius:** set of entities affected by a change, with paths. **Bridge edge:** cross-domain relationship. **Edge class:** ASSERTED / DERIVED / INFERRED / CURATED. **EOQL:** the platform's native declarative query language. **Egress Gateway:** sole outbound path for external model calls. **GraphRAG:** retrieval-augmented generation using graph structure. **Meta-graph:** graph describing the schema, sources and statistics of the instance graph. **Overlay graph:** copy-on-write sandbox for what-if analysis. **QueryPlan IR:** backend-neutral intermediate query representation. **Sharing level:** form in which data may leave the boundary (S0–S7). **Tenant:** an isolated customer organization.

## Appendix B — Traceability to the consolidated source requirement families

| Source family (consolidated-requirements.md) | Where carried forward |
| --- | --- |
| FR-CONN / FR-CONF / FR-SNOW (connectors, resiliency, replay, deletion) | §7.1, SR-ING-001…007 |
| FR-INGEST (raw capture, canonicalization, idempotency, lifecycle, DLQ) | §7.2, SR-ING-052 |
| FR-GRAPH (store, domains, schema, IDs, meta-graph, bridges, Gremlin repo, indexes, journal, RDF/OWL, multi-backend) | §5, §7.5, SR-GDB-001…010 |
| FR-ONTO / FR-PROV / FR-ID / FR-TEMP | §8, §7.2–7.4, SR-GDB-009 |
| FR-CODE (parser, Python/TS, commit-symbol, call/import edges) | SR-ING-015, §19 Software/IT pack |
| FR-QUERY / FR-VALID | §6, SR-ING-050 |
| FR-RAG (router, GraphRAG, local models, no mandatory vector DB, eval, adaptive) | §9.2, SR-VDB-007, SR-LLM |
| FR-AGENT / FR-MEM / FR-MCP | §11 |
| FR-UI / FR-ADMIN / FR-VSCODE | §13, SR-EXT-005 |
| NFR-SEC / NFR-PRIV | §14 |
| NFR-REL / NFR-OPS / NFR-PERF / NFR-MAINT | §15, §17 |
| MVP-FR-001…028 | Baseline B0 (§20); re-verified under §17.3 |
| Honest residual gaps RG-01…04 | RK-01, RK-09, §17.4, Appendix C |

## Appendix C — Inherited open external gates (union; each remains a GA gate unless de-scoped)

1. Live multi-node HA / Kubernetes / graph-cluster certification (HugeGraph PD/Store sharding is documented as not validated). 2. Live-tenant connector verification (Jira, Confluence, ServiceNow, GitHub, GitLab). 3. Confluence attachment bytes and historical bodies. 4. Inferred semantic-matching acceptance. 5. Native HugeGraph/RocksDB backup and crash-atomic multi-store recovery. 6. Webhook receipt rebasing. 7. Memory/audit/trace-history recovery. 8. Production-scale, hardware-backed benchmark of the full NFR-PERF-001 profile. 9. Release SBOM / license / no-egress evidence package. 10. Installed-VSIX and visual acceptance of the VS Code extension. 11. Remote CI observation, publication and independent QA review. 12. User-import scope decision (referenced spec found not to exist). 13. Live-stack verification for the demo ticket. 14. Linux-image verification of native file-parsing dependencies. 15. Operational coverage beyond the 66 of 271 operations rehearsed. 16. MVP evidence-annotation coverage (3/28 — an annotation metric, not completion).

## Appendix D — Research agenda for the engineering/research agent (each item yields an ADR or design note; items marked ◆ were not independently verified while drafting this baseline)

| # | Topic | Deliverable |
| --- | --- | --- |
| 1 | Graphify ◆ — repository activity, license, architecture, extraction/community/impact features | Adopt/avoid list; clean-room design note |
| 2 | Graph DB landscape ◆ — current versions, licenses, distributed shapes, GQL/PGQ progress for each Tier A/B candidate | Support matrix v1 with evidence |
| 3 | GQL (ISO/IEC 39075:2024) and SQL/PGQ (ISO/IEC 9075-16:2023) adoption status in engines ◆ | Dialect roadmap |
| 4 | Query-language translation theory and practice (Cypher↔Gremlin↔SPARQL semantic gaps) | IR specification + known-gap catalog |
| 5 | Relationship discovery from JSON: inclusion-dependency, schema-matching and LSH methods at scale | Algorithm selection + benchmark |
| 6 | Entity resolution at scale (blocking, Fellegi–Sunter, collective ER, active learning) | ER design + evaluation on synthetic ground truth |
| 7 | Ontology induction and alignment (LLM-free first, local-LLM assisted) | Mapping Studio design |
| 8 | GraphRAG variants and temporal knowledge-graph memory ◆ (current literature and OSS) | Strategy plugin catalog + evaluation results |
| 9 | Text-to-graph-query accuracy methods (schema linking, constrained decoding, repair loops) | NL parser design + benchmark |
| 10 | Permission-aware retrieval and ACL propagation for RAG | Leak-proof retrieval design |
| 11 | Local model landscape ◆ — quality/size/license for chat, embedding, reranker, OCR, multilingual | Model registry seed + hardware profiles |
| 12 | Vector DB comparison ◆ — filtered ANN, hybrid, multi-tenancy, license, operational cost | Adapter priority and defaults |
| 13 | Differential privacy / k-anonymity for S2 aggregates and synthetic data (S3) | Egress transformations spec |
| 14 | Multi-tenant graph isolation patterns per backend | Isolation matrix per adapter |
| 15 | Offline licensing and tamper-evident metering | Design + threat model |
| 16 | Federation/CRDT-style sync for edge graphs | Conflict-policy design |
| 17 | Compliance-pack content (GDPR, SOC 2, HIPAA, DPDP, DORA, EU AI Act) with legal review | Pack v1 |
| 18 | Industry ontology licensing (e.g., clinical terminologies) and redistribution rights | Pack content policy |
| 19 | Graph visualization at scale (WebGL, LOD, layout) | UX prototype + performance data |
| 20 | Export-control classification and encryption export obligations | Legal memo |

## Appendix E — Assumptions and limits of this baseline

- This document was derived from the two attached files plus published-standards knowledge; vendor-specific facts (versions, licenses, maintenance status, hosted-service availability) change quickly and are flagged "verify" where they matter. A quick check during drafting indicates Apache HugeGraph 1.7.0 (released Nov 2025) is the current stable release line and the project became a top-level Apache project in Jan 2026, with a distributed PD/Store mode; the Graphify project is an actively developed, fast-growing open-source tool for turning code, documents and media into queryable knowledge graphs. Neither was examined at source-code level.
- All numeric targets (sizes, latencies, availability, accuracy gates) are **proposals**, not measurements.
- The consolidated file's own audit caveats are preserved: its "Done" statuses reflect a code-evidence policy and a string-match gate, not independent behavioral verification; its open gates remain open.
- Nothing here constitutes legal advice; compliance mappings, export classification and license determinations require qualified review.
