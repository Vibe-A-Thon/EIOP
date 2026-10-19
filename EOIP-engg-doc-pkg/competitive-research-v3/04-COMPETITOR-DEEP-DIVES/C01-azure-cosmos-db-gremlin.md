# C01 — Azure Cosmos DB for Apache Gremlin

| Field | Value |
|---|---|
| Registry ID | T-C01-azure-cosmos-db-gremlin |
| Tier | B — a managed, Gremlin-compatible, cloud-only option, kept as a reference. It is not a required EOIP backend. |
| Versions examined | Managed service; no engine version is published. Recommended client drivers: TinkerPop **3.4.13**. The 3.5.x and 3.6.x drivers have known compatibility issues. Docs read: `gremlin/support` (updated_at 2026-04-27, ms.date 2021-07-06), `gremlin/overview` (ms.date 2025-07-22, updated_at 2026-04-27), `gremlin/partitioning`, `gremlin/limits`, `request-units` (updated_at 2026-07-21). |
| Verified on | 2026-10-18 |
| Worker | W03 |

## 1. Identity, current status, tier, and sources

**What it is.** Azure Cosmos DB for Apache Gremlin (formerly "Gremlin API") is one of Microsoft's multi-model "compatibility APIs" on top of Cosmos DB [CLAIM-azure-cosmos-db-gremlin-01]:
- vertices and edges are stored as JSON documents in a partitioned container;
- the API speaks the Gremlin wire protocol, with GraphSON v2 serialisation only;
- it is owned by Microsoft (Azure), proprietary, and runs only as a managed service.

**Status: active, but de-emphasised.**
- We found **no retirement, deprecation or feature-freeze announcement**. A Microsoft Q&A moderator (July 2025) said account-creation problems did "not necessarily mean" Microsoft is phasing the API out [CLAIM-azure-cosmos-db-gremlin-02].
- Every current Gremlin documentation page opens with a banner that steers readers elsewhere [CLAIM-azure-cosmos-db-gremlin-01]:
  - **high-scale** workloads → *Azure Cosmos DB for NoSQL*;
  - **OLAP graphs or "migrat[ing] an existing Apache Gremlin application"** → *Graph in Microsoft Fabric*.
- Other signals point the same way:
  - the compatibility page still recommends TinkerPop 3.4.13 drivers and cites TinkerPop 3.3.2 docs [CLAIM-azure-cosmos-db-gremlin-03];
  - the new cross-platform vNext emulator (GA 2026) supports the NoSQL API only [CLAIM-azure-cosmos-db-gremlin-09].
- We read this as **maintenance mode / strategic de-emphasis** (*reasoned inference*, confidence 0.6). It is **not** EOL.

**Successor in Microsoft's messaging.**
- Graph in Microsoft Fabric is GQL (ISO/IEC 39075), runs over OneLake, and uses Fabric capacity units [CLAIM-azure-cosmos-db-gremlin-08].
- The en-us overview (ms.date 2026-05-20) no longer shows a preview banner for graph itself. Earlier localised copies did say "public preview". GA status is therefore **UNVERIFIED** (confidence 0.5).
- Fabric Graph is analytics over lakehouse tables, not an OLTP Gremlin replacement. It is the subject of W17's Fabric research.

**Security event (resolved).** "CosmosEscape", reported by Wiz Research [CLAIM-azure-cosmos-db-gremlin-10]:
- *Flaw:* the Gremlin query sandbox compiled queries to .NET, and its restrictions missed .NET reflection. This allowed code execution on the shared gateway and exposure of a platform-wide key that worked across tenants and APIs.
- *Timeline:* reported 2025-11-20; the Gremlin entry point was blocked within 48 h; the permanent fix (key eliminated) was complete by July 2026; disclosed 2026-07-30.
- No evidence of exploitation beyond the researchers' own testing. No CVE was assigned.

**Sources (8).** Microsoft Learn ×6, Microsoft Q&A, Cloud Security Alliance research note. See Appendix C.

## 2. Primary problem, target workloads, concrete example workflows

**Microsoft's positioning** [CLAIM-azure-cosmos-db-gremlin-04]:
- a globally distributed, elastically scaled OLTP property graph;
- for social networks/Customer 360, recommendations, geospatial/logistics and IoT dependency graphs;
- automatic indexing of all properties and five tunable consistency levels.

**Example workflows** (Azure-resident customers):
- **W1 — Device dependency graph:** IoT devices are vertices partitioned by site; `out()` traversals stay inside a partition.
- **W2 — Customer 360:** person and account vertices, replicated to several regions for low-latency reads.

**Fit for EOIP-type workloads is poor:**
- digital-thread impact queries (J1/J9) are dominated by reverse (`in()`) traversals and deep paths;
- in Cosmos, `in()` is a cross-partition fan-out, and `repeat()` is capped at 32 iterations [CLAIM-azure-cosmos-db-gremlin-05][CLAIM-azure-cosmos-db-gremlin-06].

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Query | Gremlin text over WebSocket (`SubmitAsync`) | present | [CLAIM-azure-cosmos-db-gremlin-03] |
| Query | Gremlin bytecode / GLV fluent traversals | **absent** | [CLAIM-azure-cosmos-db-gremlin-03] |
| Query | `match()` step, lambdas, `property(set, …)` | **absent** | [CLAIM-azure-cosmos-db-gremlin-03] |
| Query | `executionProfile()` | present (Cosmos-specific) | [CLAIM-azure-cosmos-db-gremlin-03] |
| Query | openCypher / GQL / SPARQL on this API | absent | [CLAIM-azure-cosmos-db-gremlin-03] |
| Wire | GraphSON v2 only; no GraphSON v3, no GraphBinary | partial | [CLAIM-azure-cosmos-db-gremlin-03] |
| Drivers | TinkerPop 3.4.13 recommended; 3.5.x/3.6.x have "known compatibility issues" | partial | [CLAIM-azure-cosmos-db-gremlin-03] |
| Transactions | multi-statement transactions | **absent** (optimistic concurrency instead) | [CLAIM-azure-cosmos-db-gremlin-03] |
| Data | meta-properties, multi-properties (list cardinality), arrays | present | [CLAIM-azure-cosmos-db-gremlin-03] |
| Data | object (map) values, `null` | **absent** | [CLAIM-azure-cosmos-db-gremlin-03] |
| Index | automatic indexing of every property | present | [CLAIM-azure-cosmos-db-gremlin-03] |
| Index | index use after a mid-traversal `.V()` | **absent** (only the first `.V()` uses the index) | [CLAIM-azure-cosmos-db-gremlin-03] |
| Scale | partitioned containers (partition key required) | present | [CLAIM-azure-cosmos-db-gremlin-05] |
| Scale | global distribution; 5 consistency levels | present | [CLAIM-azure-cosmos-db-gremlin-04] |
| Analytics | graph OLAP | via the Spark connector, not in-engine | [CLAIM-azure-cosmos-db-gremlin-06] |
| Limits | 30 s traversal timeout; 32 `repeat()` iterations; 400 operator depth; 64 KB script; parallelism 32 partitions | present | [CLAIM-azure-cosmos-db-gremlin-06] |
| Cost | Request Units (provisioned / autoscale / serverless) | present | [CLAIM-azure-cosmos-db-gremlin-07] |
| Local dev | vNext emulator | absent for Gremlin (NoSQL only) | [CLAIM-azure-cosmos-db-gremlin-09] |
| Local dev | Windows emulator Gremlin endpoint | **UNVERIFIED** | Appendix D |
| Deployment | on-premises / air-gapped | **absent** | [CLAIM-azure-cosmos-db-gremlin-04] |

## 4. Text-based architecture diagram

```
 Client (Gremlin driver 3.4.x, GraphSON v2, text scripts)  ── key or resource token auth ──┐
                                                                                          ▼
 Azure region(s) ─ Cosmos DB account ─ Gremlin gateway (parses Gremlin, compiles to .NET; BFS execution)
                         │   (shared multi-tenant gateway tier — the CosmosEscape attack surface)
                         ▼
   Database ─ Graph container (partition key /pk; RU/s budget per container or per database)
     ├─ physical partition 1: vertex docs {id, label, _partition, properties{}}, outE{} (edges stored with source)
     ├─ physical partition 2 …     (hash of pk; edges carry target id + target pk)
     └─ automatic inverted index over all properties (schema-agnostic indexing)
   Replication: every region gets R RU/s; consistency strong | bounded staleness | session | consistent prefix | eventual
   OLAP: Spark connector (outside the engine)
```

## 5. Under-the-hood reconstruction

**Data model.**
- Vertices and edges are JSON documents [CLAIM-azure-cosmos-db-gremlin-05]:
  - a vertex holds `id`, `label`, the partition-key property and a `properties` bag of value arrays (multi-valued, with meta-properties);
  - adjacency (`outE` grouped by label) is stored with the **source** vertex.
- An edge records the target vertex's id **and partition key** [CLAIM-azure-cosmos-db-gremlin-05]. As a result:
  - `out()` is always a partition-scoped point lookup;
  - `in()` is a "blind" fan-out across partitions [CLAIM-azure-cosmos-db-gremlin-05].
- *Hypothesis:* a reverse traversal is a query on the indexed `inV` field of edge documents, run across all partitions and limited to 32 partitions per storage request.

**Storage and indexing.**
- Cosmos DB's write-optimised, schema-agnostic inverted index covers every property by default. The documentation cites the VLDB 2015 paper on schema-agnostic indexing [CLAIM-azure-cosmos-db-gremlin-03].
- Only the first `.V()` of a traversal is resolved through the index [CLAIM-azure-cosmos-db-gremlin-03].

**Query pipeline.**
- Text Gremlin → gateway → executed **breadth-first** rather than TinkerPop's depth-first. Microsoft says this suits scale-out [CLAIM-azure-cosmos-db-gremlin-03].
- The gateway compiles queries into .NET code — a fact disclosed by the CosmosEscape research [CLAIM-azure-cosmos-db-gremlin-10].
- There is no bytecode path and no cost-based optimiser documentation (*NOT PUBLICLY VERIFIED*).

**Reasoning.** None.

**Concurrency.**
- No transactions. The documentation recommends session consistency ("read your own writes") plus optimistic concurrency [CLAIM-azure-cosmos-db-gremlin-03].
- *Hypothesis:* ETag-based document replacement.

**Partitioning and consistency.**
- Partitioning applies when a container exceeds 20 GB or 10,000 RU/s [CLAIM-azure-cosmos-db-gremlin-05].
- A partition key is required with 3.x+ drivers; `/id` and `/label` cannot be the partition key [CLAIM-azure-cosmos-db-gremlin-05].
- Five consistency levels are available. Strong and bounded staleness cost about 2× the read RUs [CLAIM-azure-cosmos-db-gremlin-07].

**Caching.** NOT PUBLICLY VERIFIED.

**Versioning.** The engine offers no graph history. The Cosmos change feed exists at the platform level, but whether Gremlin exposes it is **UNVERIFIED**.

**Security.**
- Account keys and resource tokens (at most 100 unique tokens per hour per region) [CLAIM-azure-cosmos-db-gremlin-06].
- Encryption at rest and in transit, and role-based access control, are stated in the overview [CLAIM-azure-cosmos-db-gremlin-04].
- Whether Microsoft Entra ID data-plane RBAC applies to the Gremlin API is **UNVERIFIED**.
- The gateway is shared by many tenants (see CosmosEscape) [CLAIM-azure-cosmos-db-gremlin-10].

**EOIP code.**
- EOIP has **no Cosmos adapter**.
- `graph/database_adapters.py:69,154` only lists `AZURE_COSMOS_DB` with a protocol label.
- `translate_query` routes it to a regex Cypher→Gremlin translator (`database_adapters.py:323`), which would produce Gremlin scripts. Nothing guarantees that Cosmos's step subset or its 3.4-era drivers accept them [CLAIM-azure-cosmos-db-gremlin-11].

## 6. Functional and non-functional requirements inferred from verified behaviour

| ID | Requirement if EOIP ever supported Cosmos Gremlin | Evidence |
|---|---|---|
| FR-CGR-01 | Text-only Gremlin generation, GraphSON v2 parsing, a 3.4-compatible client | [CLAIM-azure-cosmos-db-gremlin-03] |
| FR-CGR-02 | Every vertex carries a tenant-aware partition key, and every lookup passes `(pk, id)` | [CLAIM-azure-cosmos-db-gremlin-05] |
| FR-CGR-03 | Materialise reverse edges, or keep a reverse index in EOIP, so that impact (`in()`) queries stay inside a partition | [CLAIM-azure-cosmos-db-gremlin-05] |
| FR-CGR-04 | Make multi-element writes idempotent and compensating (no transactions) | [CLAIM-azure-cosmos-db-gremlin-03] |
| FR-CGR-05 | Break multi-hop queries deeper than 32 hops, or longer than 30 s, into EOIP-side iteration | [CLAIM-azure-cosmos-db-gremlin-06] |
| NFR-CGR-01 | Never required; cloud-only, so excluded from air-gapped profiles | §4.3-1 |
| NFR-CGR-02 | A per-query RU budget enforced by EOIP, with 429 throttling handled by backoff | [CLAIM-azure-cosmos-db-gremlin-06][CLAIM-azure-cosmos-db-gremlin-07] |

## 7. Performance and resource model

- **No independent benchmark found.**
- **Cost model:** RU-based [CLAIM-azure-cosmos-db-gremlin-07]:
  - 1 RU ≈ a point read of a 1 KB item;
  - writes cost more as item size and the number of indexed properties grow;
  - query cost depends on predicates and result size;
  - strong or bounded-staleness reads cost about 2×;
  - provisioned RU/s are charged in **every** region (total = R × N).
- **Graph-specific cost drivers:**
  - every `in()` traversal is a fan-out;
  - automatic indexing of all properties raises write RUs unless the indexing policy is trimmed;
  - large vertices with embedded `outE` arrays (supernodes) grow the document and raise its read and write RU (*hypothesis*: follows from adjacency stored with the source document).
- **Hard limits** [CLAIM-azure-cosmos-db-gremlin-06]: 30 s timeout, 32 repeat iterations, 400 operator depth, 1 h idle WebSocket timeout. Exceeding them returns 429 or cancels the traversal.
- **Failure modes:** throttling (429) under RU exhaustion; hot partitions from a skewed partition key; truncated deep traversals.

## 8. Strengths and use-case-specific advantages — and how each could be matched or exceeded

1. **Partition-aware adjacency** [CLAIM-azure-cosmos-db-gremlin-05]. Outgoing edges sit in the source vertex's partition and carry the target's partition key, so `out()` never scans blindly.
   - *Match:* EOIP's HugeGraph and JanusGraph deployments can co-locate data the same way.
   - *Exceed:* store edges in both directions so impact queries stay local.
2. **Indexing of every property with zero configuration** [CLAIM-azure-cosmos-db-gremlin-03]. Ad-hoc filters work without index design.
   - *Match:* in EOIP's index advisor — but at a write cost.
3. **Global distribution with five consistency levels** [CLAIM-azure-cosmos-db-gremlin-04].
   - Not a one-node-first concern for EOIP; *reject* as a goal and keep as a reference.
4. **A predictable cost currency (RU, with a charge header per request)** [CLAIM-azure-cosmos-db-gremlin-07].
   - *Exceed:* EOIP could report an engine-neutral "query cost units" figure per QueryPlan for metering (BL-22).

## 9. Limitations with root causes

**Verified gaps**
- no bytecode, no GraphSON v3/GraphBinary, no `match()`, no lambdas, no set cardinality, no transactions, no map values or `null`;
- indexes used only by the first `.V()`;
- drivers stuck at 3.4.13 [CLAIM-azure-cosmos-db-gremlin-03].

**Intentional trade-offs**
- breadth-first execution;
- the 30 s / 32-hop limits for OLTP protection [CLAIM-azure-cosmos-db-gremlin-03][CLAIM-azure-cosmos-db-gremlin-06];
- adjacency stored only with the source vertex [CLAIM-azure-cosmos-db-gremlin-05].

**Strategic signals.** Documentation banners steer new and migrating Gremlin users to NoSQL or Fabric Graph [CLAIM-azure-cosmos-db-gremlin-01]. The emulator roadmap excludes Gremlin [CLAIM-azure-cosmos-db-gremlin-09].

**Security incident.** CosmosEscape: a sandbox escape in the Gremlin gateway that led to a cross-tenant key exposure. Fixed [CLAIM-azure-cosmos-db-gremlin-10].

**Root causes**
- *Algorithmic dead-ends:*
  - reverse traversal cost — the data model is source-partitioned (proven);
  - bounded traversal depth (proven).
- *Operational overhead:* RU tuning, partition-key design, and per-region RU multiplication [CLAIM-azure-cosmos-db-gremlin-07].
- *Developer friction:* old TinkerPop drivers, a text-only API, a Cosmos-specific JSON result shape that differs from standard GraphSON [CLAIM-azure-cosmos-db-gremlin-03], and no local emulator on the current toolchain [CLAIM-azure-cosmos-db-gremlin-09].

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Air-gap / local-first (§4.3-1) | **Fails.** Azure-only. No supported local Gremlin emulator on the vNext toolchain [CLAIM-azure-cosmos-db-gremlin-09]. |
| Backend neutrality (§4.3-3) | Cosmos is not a named required backend. Adding it would cost a 3.4-era dialect profile plus a reverse-edge emulation layer. |
| Permissions / tenancy (§4.3-8/9) | Account keys or resource tokens only. No per-vertex ACLs; EOIP would have to enforce everything. Tenant-per-container or partition-key-prefix designs are possible. The shared gateway tier had a cross-tenant flaw (fixed) [CLAIM-azure-cosmos-db-gremlin-10]. |
| One-node first (§4.3-10) | N/A (managed). |
| Licensing / redistribution (§4.3-12) | A proprietary Azure service in the customer's own subscription. Client drivers are Apache TinkerPop (Apache-2.0). **No legal-review trigger** for client code. Commercial review is needed only for resale. |
| Maintenance risk | Medium–high. No EOL announcement, but clear de-emphasis signals (§1). |

## 11. Competitive delta against the EOIP verified baseline

| Capability | Cosmos Gremlin | EOIP baseline | Delta |
|---|---|---|---|
| Adapter | — | none; protocol label only (`database_adapters.py:154`) | No support today. Recommend keeping it that way (DEFER) |
| Gremlin portability | 3.4-era text subset | BL-05 JanusGraph and BL-02 HugeGraph Gremlin | EOIP's Gremlin generation would need a third dialect profile |
| Transactions | none | BL-01 protocol assumes per-call atomic upserts | Compatible only with idempotent single-element writes |
| Reverse traversal (J1/J9) | fan-out, ≤32 hops | BL-43 Python traversal | EOIP's application-layer traversal would hide the cost but multiply RUs |
| Temporal / provenance | none | BL-37/41 implemented | EOIP ahead |
| ACL / tenancy | key-level | BL-18 absent, BL-20 partial | both need EOIP-side enforcement (P0 regardless) |
| Air-gap | impossible | design goal | EOIP structural advantage |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

| STR-ID | competitor | strength | evidence | value to EOIP customers | match/exceed/integrate/reject | design approach | acceptance test |
|---|---|---|---|---|---|---|---|
| STR-azure-cosmos-db-gremlin-01 | Azure Cosmos DB for Apache Gremlin | Partition-aware adjacency (edges store the target's id and partition key) | [CLAIM-azure-cosmos-db-gremlin-05] | Bounded traversal cost at scale | exceed | EOIP partitioning advice for distributed backends: tenant + domain partition key; edges stored **both** ways (forward with the source, reverse index with the target) | T-CGR-02: a 3-hop impact query touches ≤3 partitions at p95 on a sharded backend |
| STR-azure-cosmos-db-gremlin-02 | Azure Cosmos DB for Apache Gremlin | Per-request cost currency (RU charge header) | [CLAIM-azure-cosmos-db-gremlin-07] | Predictable metering for white-label tenants | exceed | Engine-neutral cost units per QueryPlan in EOIP metering (BL-22) | Cost units within ±20 % of measured CPU-ms across backends for 30 plans |

**INV-azure-cosmos-db-gremlin-01 — Reverse traversals are cross-partition fan-outs, capped at 32 hops and 30 s**
- **Target:** Cosmos Gremlin (current service); impact and blast-radius analysis (J1, J9, J10).
- **Limitation:** `in()` "will always be an expensive fan-out query"; `repeat()` is limited to 32 iterations; traversals time out at 30 s [CLAIM-azure-cosmos-db-gremlin-05][CLAIM-azure-cosmos-db-gremlin-06].
- **Root cause:** data model — adjacency is stored with the source only (proven).
- **Why an alternative mitigates it:** EOIP maintains both directions and computes bounded impact closures incrementally at ingest.
- **When the alternative is worse:** write amplification is about 2× per edge, and storage grows.
- **Options:**
  - (a) Quick: do not support Cosmos.
  - (b) Pragmatic: an EOIP reverse-edge materialiser for any source-partitioned backend.
  - (c) Long-term: an incremental "impact index" (precomputed k-hop dependents per asset, invalidated by mutation events).
- **Selected:** (a) for Cosmos; (c) as an EOIP-wide EXPERIMENT for J9/J10 latency on every backend.
- **Sketch:**
  ```
  on edge_upsert(a -DEPENDS_ON-> b): impact_index[b] |= {a} ∪ impact_index[a] (bounded k)
  on tombstone(edge): recompute affected keys
  ```
- **POC:** on a 1 M-edge synthetic digital thread, the service-account blast-radius query (J9) reaches p95 ≤200 ms with the impact index vs live traversal, with identical result sets.
- **Security:** the impact index must be ACL-filtered at read time, never precomputed per principal.
- **Defensibility:** incremental, permission-aware impact answers are customer-visible value that does not depend on any engine.
- **Decision:** **EXPERIMENT** (EOIP-wide); **REJECT** Cosmos as a backend for this workload.

**INV-azure-cosmos-db-gremlin-02 — Shared multi-tenant gateway: a cross-tenant platform risk**
- **Target:** the Cosmos DB platform (all APIs); the incident lasted from 2025-11 to 2026-07.
- **Limitation:** a Gremlin sandbox escape exposed a platform-wide key [CLAIM-azure-cosmos-db-gremlin-10].
- **Root cause:** coupling and deployment — query compilation inside a shared gateway (proven by the third-party report; details at confidence 0.6).
- **Why an alternative mitigates it:** EOIP's self-hosted, per-customer deployment removes the cross-customer blast radius. EOIP must still apply the same lesson internally: never compile user-influenced queries into host-language code.
  - The Neptune ANTLR approach [cross-ref CLAIM-amazon-neptune-03] and EOIP's typed QueryPlan templates (BL-08) are the safer pattern.
- **When worse:** self-hosting moves patching responsibility to the customer.
- **Options:**
  - (a) Record it as competitive evidence for regulated buyers.
  - (b) Add a "no dynamic code from queries" rule to EOIP's threat model and a fuzz test for query front-ends (EQL, qlang).
  - (c) Run query front-ends in a separate low-privilege process per tenant.
- **Selected:** (a) + (b).
- **POC:** grammar-based fuzzing of EOIP's query parsers for 24 h, with no execution outside the template set.
- **Decision:** **ADOPT** (b).

## 13. Per-capability decisions

| CAP | Decision | Note |
|---|---|---|
| CAP-13 Gremlin (Cosmos dialect) | **DEFER** | Add only on a contract requirement; it would need a 3.4-era text-only profile |
| CAP-05 distributed scale-out | **REJECT** (as an EOIP dependency) | Reference pattern only |
| CAP-19 multi-hop / reverse traversal | **EXPERIMENT** (EOIP impact index) | INV-azure-cosmos-db-gremlin-01 |
| CAP-49 query-injection defence | **BUILD** (threat-model rule + fuzzing) | INV-azure-cosmos-db-gremlin-02 |
| CAP-77 licensing / TCO metering | **EXPERIMENT** (engine-neutral cost units) | STR-azure-cosmos-db-gremlin-02 |
| CAP-50 air-gapped operation | **REJECT** Cosmos in air-gapped profiles | [CLAIM-azure-cosmos-db-gremlin-09] |
| CAP-20 portable IR | **BUILD** (independent of Cosmos); Cosmos shows why dialect profiles are needed | [CLAIM-azure-cosmos-db-gremlin-03] |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (PROPOSED; none run)

| Test | Setup | Acceptance |
|---|---|---|
| T-CGR-01 Dialect probe (only if a customer requires it) | Run EOIP's 30 Gremlin core plans as text against a Cosmos Gremlin account (serverless) using driver 3.4.13 | Pass rate recorded; every failure mapped to a documented gap |
| T-CGR-02 Partition locality (backend-agnostic) | Sharded backend; 3-hop forward and reverse impact queries | ≤3 partitions touched at p95 with bidirectional edges |
| T-CGR-03 Impact-index POC | 1 M edges, J9 query | p95 ≤200 ms; identical results to live traversal; ACL filter applied |
| T-CGR-04 Query-parser fuzzing | 24 h grammar fuzzing of EQL/qlang | No crash escapes; no code execution outside templates |
| T-CGR-05 Translator safety | `database_adapters.translate_query` for `AZURE_COSMOS_DB` | Either removed, or marked "unsupported" in capability negotiation |

## 15. Risks, trade-offs, and open research questions

- **Risks:**
  - investing in a Cosmos adapter while Microsoft steers Gremlin users elsewhere (§1);
  - EOIP's `database_adapters.py` advertises Cosmos protocol support that does not exist [CLAIM-azure-cosmos-db-gremlin-11].
- **Trade-offs:** bidirectional edges (local reverse traversal) vs write amplification.
- **Open questions:**
  - Will Microsoft announce a retirement date? (Watch Azure Updates.)
  - Does the Windows emulator still expose a Gremlin endpoint? (UNVERIFIED.)
  - Is Entra ID data-plane RBAC available for the Gremlin API? (UNVERIFIED.)
  - Is Fabric Graph generally available, and does it offer a Gremlin migration path? (Cross-reference W17.)

---

## Appendix A — Research-dimension coverage

| Dimension | Covered in | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Active, de-emphasised; no EOL found; proprietary |
| D2 Problem and workloads | 2 | OLTP graph; poor fit for reverse-traversal-heavy impact analysis |
| D3 Architecture | 4 | Gateway over partitioned JSON containers |
| D4 Storage and indexing | 5 | JSON documents; adjacency with the source; automatic inverted index |
| D5 Schema expressivity | 3, 5 | Schema-free; meta-properties and multi-properties; no maps or null |
| D6 Query pipeline | 5 | Text Gremlin, BFS, compiled to .NET; first-`.V()` index use |
| D7 Reasoning | 5 | None |
| D8 Transactions and scale | 5, 7 | No transactions; partitioned; 5 consistency levels |
| D9 Ingestion and federation | 3 | Gremlin writes; Spark connector; bulk tooling not researched (N/A at Tier B) |
| D10 Identity and evidence | 5 | id + partition-key uniqueness only |
| D11 Time and evolution | 5 | No graph history; change-feed exposure for Gremlin UNVERIFIED |
| D12 Algorithms and ML | 3 | OLAP via Spark only |
| D13 Retrieval and agents | — | No vector or GraphRAG features on the Gremlin API found; N/A |
| D14 NL querying | — | None in this API; Fabric Graph NL2GQL is a separate product (W17) |
| D15 Governance | — | None in-engine; N/A |
| D16 Human experience | 3 | Data Explorer (portal); no emulator UI for Gremlin |
| D17 Developer experience | 9 | Old drivers, text-only, GraphSON v2 |
| D18 Trust and security | 5, INV-02 | Keys and resource tokens; CosmosEscape |
| D19 Multi-tenancy | 10 | Container or partition-key designs; app-enforced |
| D20 Economics | 7 | RU model; per-region multiplication |
| D21 Commercial | 10 | Proprietary Azure service |
| D22 Interoperability / lock-in | 9, 11 | Non-standard result JSON; 3.4 dialect; migration path steered to Fabric |
| D23 IP and prior art | — | Schema-agnostic indexing paper (VLDB 2015) is published prior art; no FTO concern for EOIP identified |
| D24 Research quality | App. C | Official docs (0.8–0.9); status inference 0.6; security incident third-party 0.6–0.7 |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-01 | native (document-backed) | CLAIM-azure-cosmos-db-gremlin-05 | BL-01 Implemented | REJECT as backend | P3 |
| CAP-05 | native | CLAIM-azure-cosmos-db-gremlin-05 | — | REJECT (reference) | P3 |
| CAP-13 | partial (3.4-era text subset) | CLAIM-azure-cosmos-db-gremlin-03 | BL-02/05 | DEFER | P3 |
| CAP-19 | partial (≤32 hops; `in()` fan-out) | CLAIM-azure-cosmos-db-gremlin-06 | BL-43 | EXPERIMENT (impact index) | P2 |
| CAP-20 | absent | CLAIM-azure-cosmos-db-gremlin-03 | BL-09 Partial | BUILD | P1 |
| CAP-45 | partial (keys, resource tokens) | CLAIM-azure-cosmos-db-gremlin-06 | BL-19 | — | P3 |
| CAP-47 | partial (container / partition) | CLAIM-azure-cosmos-db-gremlin-05 | BL-20 Partial | BUILD in EOIP | P0 |
| CAP-49 | — (incident) | CLAIM-azure-cosmos-db-gremlin-10 | BL-08 | BUILD (fuzzing) | P1 |
| CAP-50 | absent | CLAIM-azure-cosmos-db-gremlin-09 | goal | REJECT | P0 (doc) |
| CAP-77 | RU pricing | CLAIM-azure-cosmos-db-gremlin-07 | BL-22 | EXPERIMENT | P3 |

## Appendix C — Evidence records

| CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication / access | confidence + rationale | contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-azure-cosmos-db-gremlin-01 | Cosmos Gremlin docs, 2026 | Banner on Gremlin pages: high-scale → "Consider Azure Cosmos DB for NoSQL"; OLAP graph or "migrate an existing Apache Gremlin application" → "Consider Graph in Microsoft Fabric" | Officially documented | Introduction/Overview — https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/overview (same banner on /support, /partitioning, /limits) | updated 2026-04-27 / 2026-10-18 | 0.9 — present verbatim | no deprecation notice found |
| CLAIM-azure-cosmos-db-gremlin-02 | Cosmos Gremlin, 2025-07 | Microsoft moderator: account-creation failure "does not necessarily mean" Microsoft is phasing out the Gremlin API | Third-party report (vendor forum) | Is Cosmos Db Gremlin API deprecated? — https://learn.microsoft.com/en-us/answers/questions/3145158/is-cosmos-db-gremlin-api-deprecated | 2025-07 / 2026-10-18 | 0.5 — read via search summary; forum post | none |
| CLAIM-azure-cosmos-db-gremlin-03 | Cosmos Gremlin support page | Recommended drivers 3.4.13; 3.5.x/3.6.x "known compatibility issues"; GraphSON v2 only; no bytecode, `match()`, lambdas, set cardinality, object properties, null; no transactions (use session consistency + optimistic concurrency); BFS execution; automatic indexing of all properties; only the first `.V()` uses the index; meta-properties and multi-properties supported | Officially documented | Azure Cosmos DB for Gremlin support and compatibility with TinkerPop features — https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/support | ms.date 2021-07-06, updated 2026-04-27 / 2026-10-18 | 0.85 — official, but content dated | none |
| CLAIM-azure-cosmos-db-gremlin-04 | Cosmos Gremlin overview | Fully managed; elastic scale "billions of vertices and edges"; global distribution; automatic indexing; five consistency levels; encryption and RBAC; use cases social/recommendation/geospatial/IoT | Officially documented (scale figure = vendor claim) | Overview — https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/overview | ms.date 2025-07-22 / 2026-10-18 | 0.8 (scale claim 0.3) | none |
| CLAIM-azure-cosmos-db-gremlin-05 | Cosmos Gremlin partitioning | Vertices and edges are JSON docs; vertices need a partition key; edges stored with the source vertex and holding the target id + pk; `in()` "will always be an expensive fan-out query"; `/id` and `/label` cannot be pk; partitioning when >20 GB or >10,000 RU/s | Officially documented | Data partitioning in Azure Cosmos DB for Gremlin — https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/partitioning | ms.date 2019-06-24, updated 2026-04-27 / 2026-10-18 | 0.85 | none |
| CLAIM-azure-cosmos-db-gremlin-06 | Cosmos Gremlin limits | Script 64 KB; operator depth 400; parallelism 32 partitions; repeat limit 32; traversal timeout 30 s; idle connection 1 h; 100 resource tokens per hour; throttling 429 | Officially documented | Limits of Azure Cosmos DB for Gremlin — https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/limits | ms.date 2019-10-04, updated 2026-04-27 / 2026-10-18 | 0.85 | none |
| CLAIM-azure-cosmos-db-gremlin-07 | Cosmos DB RU model | 1 RU ≈ point read of 1 KB; provisioned, serverless, autoscale modes; costs grow with item size, indexed properties, query complexity; strong/bounded staleness ≈2× read RUs; RUs provisioned in every region (R × N) | Officially documented | Request Units — https://learn.microsoft.com/en-us/azure/cosmos-db/request-units | ms.date 2025-09-03, updated 2026-07-21 / 2026-10-18 | 0.9 | none |
| CLAIM-azure-cosmos-db-gremlin-08 | Graph in Microsoft Fabric | LPG over OneLake, GQL (ISO/IEC 39075), NL2GQL; billed in Fabric CUs (10 CU-seconds per uptime second; ≥100 GB storage); en-us page shows no preview banner for graph itself | Officially documented (GA status inferred) | What is graph in Microsoft Fabric? — https://learn.microsoft.com/en-us/fabric/graph/overview | ms.date 2026-05-20 / 2026-10-18 | 0.5 for GA status; 0.85 for features | localised copies say "public preview" |
| CLAIM-azure-cosmos-db-gremlin-09 | Cosmos DB emulators | Linux vNext emulator (GA 2026) supports only the API for NoSQL; the emulator is not for production | Officially documented | Linux-based emulator — https://learn.microsoft.com/en-us/azure/cosmos-db/emulator-linux ; Emulator — https://learn.microsoft.com/en-us/azure/cosmos-db/emulator | updated 2026-09-01 / 2026-10-18 | 0.75 — vNext scope via search summary | Windows emulator Gremlin support UNVERIFIED |
| CLAIM-azure-cosmos-db-gremlin-10 | Cosmos DB, 2025-11 to 2026-07 | "CosmosEscape": Gremlin queries compiled to .NET; reflection bypass → code execution on shared gateway → platform-wide key across tenants/APIs; reported 2025-11-20, entry point blocked within 48 h, permanent fix by July 2026, disclosed 2026-07-30; no evidence of exploitation; no CVE | Third-party report | CSA Research Note: Azure Cosmos DB CosmosEscape — https://labs.cloudsecurityalliance.org/research/csa-research-note-azure-cosmos-db-cosmosescape-20260801-csa/ ; The Hacker News — https://thehackernews.com/2026/07/azure-cosmos-db-flaw-exposed-platform.html | 2026-08-01 / 2026-10-18 | 0.65 — secondary analysis of Wiz research; Microsoft advisory not read | none |
| CLAIM-azure-cosmos-db-gremlin-11 | EOIP @ ad9937b | No Cosmos adapter; `DatabaseType.AZURE_COSMOS_DB` with protocol label "Azure Cosmos DB Gremlin API" (`graph/database_adapters.py:69,154`); `translate_query` routes it to the regex Cypher→Gremlin translator (`:323`) | Observed in source code | `packages/eoip/graph/database_adapters.py` | 2026-10-18 / 2026-10-18 | 0.95 | none |

## Appendix D — Assumptions

1. "Azure Cosmos DB Gremlin API" in the Master Prompt is the product now called Azure Cosmos DB for Apache Gremlin. There is no name collision.
2. "De-emphasised" is our inference from documentation banners, the age of the driver guidance and the emulator scope. Microsoft has not said it.
3. Whether the Windows local emulator still exposes a Gremlin endpoint was not verified; it is recorded as UNVERIFIED.
4. CosmosEscape details come from third-party write-ups of Wiz's research. Microsoft's own advisory was not read.
5. No Azure account was used; every test is PROPOSED.
