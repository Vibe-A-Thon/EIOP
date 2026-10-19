# C01 — Amazon Neptune (Neptune Database, Neptune Analytics, RDF/SPARQL mode)

| Field | Value |
|---|---|
| Registry ID | T-C01-amazon-neptune |
| Tier | A — a required supported backend of EOIP (Master Prompt §4.2, §4.3 item 3). This file also covers the C02 entry "Amazon Neptune (RDF mode)"; it is researched once here and cross-referenced. |
| Versions examined | **Neptune Database:** engine **1.5.0.0** (released 2026-10-13, the newest), **1.4.8.1** (2026-10-06) and 1.4.8.0 (2026-07-27). Query-language levels in 1.5.0.0: Gremlin 3.8.0–3.8.1, openCypher `Neptune-9.0.20190305-1.1`, SPARQL 1.1. **Neptune Analytics:** managed service with no public engine version (API `neptune-graph-2023-11-29`). **graph-notebook:** 5.3.0 (PyPI, 2026-08-04). **EOIP adapter:** `packages/eoip/graph/neptune.py` at HEAD `ad9937b`. |
| Verified on | 2026-10-18 |
| Worker | W03 |

---

## 1. Identity, current status, tier, and sources

**Identity.** Amazon Neptune is AWS's family of managed graph databases. The registry entry covers three things that are often confused:

1. **Neptune Database** — the transactional (OLTP) engine.
   - A cluster has one writer and up to 15 read replicas. All instances share one storage volume that spans three Availability Zones [CLAIM-amazon-neptune-26].
   - It serves Gremlin (Apache TinkerPop), openCypher (over HTTPS and Bolt) and SPARQL 1.1 [CLAIM-amazon-neptune-02][CLAIM-amazon-neptune-17].
   - A **Serverless** capacity mode (`db.serverless`) scales compute in Neptune Capacity Units [CLAIM-amazon-neptune-13].
2. **Neptune "RDF mode"** — not a separate product.
   - The same cluster can hold RDF quads, loaded from N-Triples, N-Quads, RDF/XML or Turtle and queried with SPARQL.
   - Property-graph data and RDF data can share a cluster, but **Gremlin and openCypher cannot query RDF data, and SPARQL cannot query property-graph data** [CLAIM-amazon-neptune-26][CLAIM-amazon-neptune-15].
   - This resolves the registry's double listing in C01 and C02: one engine with two isolated data models.
3. **Neptune Analytics** — a separate, in-memory analytics engine.
   - It has its own API (`neptune-graph`) and is queried with openCypher.
   - It offers 25+ built-in algorithms, called as `CALL neptune.algo.*`, and one HNSW vector index per graph.
   - It loads data from S3, from a Neptune Database cluster or from a snapshot [CLAIM-amazon-neptune-18][CLAIM-amazon-neptune-19][CLAIM-amazon-neptune-20].

**Owner.** Amazon Web Services.

**Status: active.**
- Engine 1.5.0.0 began general rollout on 2026-10-13.
- 1.4.x releases have published end-of-life dates between 2027-03-06 and 2027-10-27.
- The whole 1.2.x line reaches end of life on **2026-12-04** [CLAIM-amazon-neptune-01].
- AWS keeps minor versions available for at least 6 months and major versions for at least 12. At end of life, clusters are upgraded automatically during a maintenance window [CLAIM-amazon-neptune-27].
- Neptune Analytics was added to 14 more regions in January and February 2026 [CLAIM-amazon-neptune-35].

**Licence.** A proprietary managed service, governed by the AWS Customer Agreement and Service Terms. No engine binary is distributed. The client tooling is open source:
- graph-notebook is Apache-2.0 (5.3.0, 2026-08-04) [CLAIM-amazon-neptune-24];
- the drivers are Apache TinkerPop drivers (Apache-2.0) and the Neo4j Bolt drivers.

**Tier reason.** EOIP names Neptune as a required backend. In the baseline, the Neptune adapter is implemented but has never run against a live engine (BL-04), and IAM SigV4 support is an open question (U-03).

**Trap resolution (Master Prompt §5).**
- "Neptune RDF mode" in C02 is the same engine. It is cross-referenced, not duplicated.
- "Neptune Analytics supports Gremlin" is **false**: it supports openCypher only [CLAIM-amazon-neptune-18]. EOIP's own manifest makes this mistake [CLAIM-amazon-neptune-30].
- Neptune Analytics imports RDF as N-Triples and queries it with openCypher. Native SPARQL on Neptune Analytics is **NOT PUBLICLY VERIFIED** [CLAIM-amazon-neptune-21].
- "100,000 queries per second" and "tens of billions of relationships" are vendor claims [CLAIM-amazon-neptune-36].

**Sources.** 23 official AWS documentation pages, one LocalStack page, PyPI metadata, and EOIP code (Appendix C).

## 2. Primary problem, target workloads, concrete example workflows

Neptune is aimed at teams already on AWS who want a graph database without operating one.
- For Neptune Database, AWS lists social networking, fraud alerting, Customer 360, knowledge graphs, identity graphs and security graphs.
- For Neptune Analytics, it lists investigative, data-science and combined vector-and-graph (GraphRAG) workloads [CLAIM-amazon-neptune-36][CLAIM-amazon-neptune-18].

Example workflows relevant to EOIP customers:

- **W1 — Digital thread on AWS (J1).**
  - EOIP ingests Jira, GitLab and CI events and writes `WorkItem`, `Commit` and `Deployment` vertices and their edges into a Neptune cluster with openCypher `MERGE`.
  - Reads go to the reader endpoint. Those reads are snapshot-isolated and usually less than 100 ms behind the writer [CLAIM-amazon-neptune-10][CLAIM-amazon-neptune-12].
- **W2 — Keeping indexes fresh with Streams (J7).**
  - A worker polls `/propertygraph/stream` and updates EOIP's BM25 and vector indexes and its caches.
  - The change log is written in the same transaction as the change, is strictly ordered, has no duplicates and is complete [CLAIM-amazon-neptune-14].
- **W3 — Impact analytics (J9/J10).**
  - A nightly job copies the operational graph into Neptune Analytics.
  - It runs `neptune.algo.pageRank`, `wcc` or `louvain` together with a vector top-k search in one openCypher query.
  - It writes the scores back as *predictions* in EOIP's prediction plane (J8), not as facts [CLAIM-amazon-neptune-18][CLAIM-amazon-neptune-19].
- **W4 — Publishing the ontology (J4).**
  - EOIP exports a governed ontology and instance data as N-Quads into a named graph, so SPARQL clients can read them.
  - Note that Neptune's SPARQL default graph is the union of all named graphs [CLAIM-amazon-neptune-06].

**Local-first suitability: none.** Neptune exists only inside an AWS VPC (see §10).

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Query | Gremlin (TinkerPop 3.8.0–3.8.1 on 1.5.0.0): text queries over HTTPS and WebSocket, and GLV bytecode | present, with deviations | [CLAIM-amazon-neptune-02][CLAIM-amazon-neptune-03] |
| Query | openCypher (Cypher 9 baseline) over HTTPS `/openCypher` and over Bolt v1–4.0 (TCP only) | present, with deviations | [CLAIM-amazon-neptune-04][CLAIM-amazon-neptune-17] |
| Query | SPARQL 1.1 Query and Update; `SERVICE` federation | present | [CLAIM-amazon-neptune-06][CLAIM-amazon-neptune-12] |
| Query | Gremlin parameter bindings and script variables | **absent** (Neptune parses with the ANTLR grammar) | [CLAIM-amazon-neptune-03] |
| Query | openCypher `CALL … YIELD`, user-defined functions, `shortestPath()` (in Neptune Database) | **absent** | [CLAIM-amazon-neptune-04] |
| Query | Query hints (`USING`), explain and profile endpoints, slow-query log | present | [CLAIM-amazon-neptune-04][CLAIM-amazon-neptune-10] |
| Query | GQL (ISO/IEC 39075), SQL/PGQ, GraphQL | absent; GraphQL only through an AWS AppSync integration | [CLAIM-amazon-neptune-12] |
| Schema | Constraints beyond element-ID uniqueness | **absent** | [CLAIM-amazon-neptune-12] |
| Schema | User-defined secondary indexes | absent; three fixed quad indexes plus an optional OSGP index | [CLAIM-amazon-neptune-11] |
| Schema | Multiple labels per vertex (Gremlin `::`); multi-valued properties with set cardinality | present | [CLAIM-amazon-neptune-03] |
| Schema | Meta-properties; `null`, Map, UUID or List property values | **absent** | [CLAIM-amazon-neptune-03][CLAIM-amazon-neptune-05] |
| Reasoning | RDFS or OWL inference | absent; no reasoner is documented | [CLAIM-amazon-neptune-06] (none listed) |
| Storage | Volume up to 128 TiB; property value up to 55 MB | present | [CLAIM-amazon-neptune-08] |
| Scale | One writer plus 15 replicas; Global Database (cross-region copies) | present | [CLAIM-amazon-neptune-12][CLAIM-amazon-neptune-26] |
| Scale | Sharding, or more than one writer | **absent** — AWS says Neptune is "single-sharded by design" | [CLAIM-amazon-neptune-14] |
| Capacity | Serverless, 1.0–128 NCU (1 NCU ≈ 2 GiB) | present | [CLAIM-amazon-neptune-13] |
| Ingest | Bulk loader from S3: Gremlin CSV, openCypher CSV, N-Triples, N-Quads, RDF/XML, Turtle (gz or bz2); not ACID | present | [CLAIM-amazon-neptune-15] |
| Ingest | Fast offline bulk loader into an empty graph (new in 1.5.0.0) | present | [CLAIM-amazon-neptune-02] |
| Change data capture | Neptune Streams (retention 1–90 days) | optional (cluster parameter) | [CLAIM-amazon-neptune-14] |
| Search | Full-text search through Amazon OpenSearch (replicated from Streams) | optional; depends on another AWS service | [CLAIM-amazon-neptune-16] |
| Search | Native vector search in Neptune Database | absent; Neptune Analytics only | [CLAIM-amazon-neptune-19] |
| Analytics | Neptune Analytics algorithms: BFS, single-source shortest path (SSSP), top-k SSSP, egonet, degree, PageRank, closeness, eigenvector, Jaccard, overlap, common neighbours, weakly and strongly connected components (WCC/SCC), label propagation, Louvain, Leiden, vector distance and top-k, graph-schema procedures | present (separate service) | [CLAIM-amazon-neptune-18] |
| Machine learning | Neptune ML (GNN training through SageMaker) | optional, cloud-only | [CLAIM-amazon-neptune-26] |
| Security | IAM SigV4 authentication; per-action IAM for queries (`Read/Write/DeleteDataViaQuery`); KMS encryption at rest; TLS 1.2 | present | [CLAIM-amazon-neptune-07][CLAIM-amazon-neptune-09][CLAIM-amazon-neptune-08] |
| Security | Username/password login; access control on labels, properties or rows | **absent** | [CLAIM-amazon-neptune-08][CLAIM-amazon-neptune-12] |
| Tenancy | More than one database per cluster | **absent** — one graph per cluster | [CLAIM-amazon-neptune-12] |
| Operations | Snapshots, point-in-time restore (PITR), online index rebuild and storage breakdown (1.5.0.0), CloudWatch metrics | present | [CLAIM-amazon-neptune-02][CLAIM-amazon-neptune-14] |
| UI / IDE | graph-notebook (Jupyter magics and visualisation), Graph Explorer, third-party tools | present (open-source client) | [CLAIM-amazon-neptune-24][CLAIM-amazon-neptune-12] |
| SDK / CLI | AWS SDK clients `neptunedata` (Gremlin and openCypher, **no SPARQL**) and `neptune-graph` (Analytics); AWS CLI | present | [CLAIM-amazon-neptune-07][CLAIM-amazon-neptune-18] |
| Deployment | On-premises, air-gapped, self-hosted or embedded | **absent** | [CLAIM-amazon-neptune-08] |

## 4. Text-based architecture diagram

```
                         AWS account / Region (control plane = AWS APIs, IAM, KMS, CloudWatch)
 ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
 │  VPC (mandatory; no access from outside the VPC)                                             │
 │                                                                                              │
 │  Client (EOIP API/worker)                                                                    │
 │    │ HTTPS 8182  /gremlin  /openCypher  /sparql  /loader  /propertygraph/stream  /status      │
 │    │ WSS 8182 (Gremlin)   Bolt/TCP 8182 (openCypher)      ── SigV4 signed if IAM enabled ──  │
 │    ▼                                                                                         │
 │  Cluster endpoint ──► Writer instance (query engines: Gremlin [TinkerPop + native DFE],       │
 │  Reader endpoint ──►  Replica 1..15     openCypher [DFE], SPARQL; lock manager; buffer cache) │
 │  Custom endpoints     (snapshot-isolated reads; lag "usually <100 ms")                       │
 │                │                                                                             │
 │                ▼  (data plane: shared cluster volume, 3 AZs, <=128 TiB)                      │
 │  ┌───────────────────────────────────────────────────────────────────────┐                   │
 │  │ Dictionary (string <-> id)  Quad indexes SPOG | POGS | GPSO (+OSGP)   │                   │
 │  │ Predicate set index         Streams change log (same txn, 1-90 days)  │                   │
 │  └───────────────────────────────────────────────────────────────────────┘                   │
 │        ▲ bulk loader (assumes IAM role) <── S3 via VPC endpoint                              │
 │        └─ Streams poller ──► OpenSearch (full-text)   Neptune-to-Neptune replication          │
 └──────────────────────────────────────────────────────────────────────────────────────────────┘

 Neptune Analytics (separate service; endpoint <graph-id>.<region>.neptune-graph.amazonaws.com)
   in-memory graph (16..24,576 m-NCU, 0..2 replicas) <── import: S3 | Neptune DB cluster | snapshot
   openCypher + CALL neptune.algo.* + one HNSW vector index (non-atomic updates)
   private (VPC endpoint) or optional public connectivity; always IAM-authenticated
```

## 5. Under-the-hood reconstruction

AWS documents Neptune's storage model and locking in unusual detail, so this section goes further than is possible for most closed-source engines. Neptune's source code is not public, so no source paths can be cited. Anything not documented is marked *hypothesis*.

### 5.1 Data model

**One physical model: dictionary-encoded quads.** Every fact is a 4-tuple (S, P, O, G) of dictionary IDs [CLAIM-amazon-neptune-11][CLAIM-amazon-neptune-10].
- In RDF the positions are subject, predicate, object and graph.
- In the property graph they are used as follows:
  - a vertex label becomes `(v, ~label, Label, default)`;
  - a property becomes `(v, key, value, default)`;
  - an edge becomes `(out_v, edgeLabel, in_v, edge_id)`, with the edge ID in the G position;
  - edge properties are attached to the edge ID.

**Consequences.**
- Edge and vertex properties use the same machinery, and one cluster can hold both RDF and property-graph statements. The two are not interoperable at query time because they are encoded differently [CLAIM-amazon-neptune-26].
- The only constraint the engine enforces is that element IDs are unique. AWS recommends user-supplied string IDs as the way to get uniqueness, including composite keys [CLAIM-amazon-neptune-12].
- Properties hold **sets of values**:
  - Gremlin defaults to `set` cardinality;
  - arrays written through openCypher become multi-valued properties;
  - when a property has several values, openCypher returns one of them arbitrarily [CLAIM-amazon-neptune-03][CLAIM-amazon-neptune-04][CLAIM-amazon-neptune-05].
- `null`, maps, UUIDs, lists and meta-properties cannot be stored. Datetimes are converted to UTC and the original offset is lost [CLAIM-amazon-neptune-03][CLAIM-amazon-neptune-06].

### 5.2 Storage layout and indexing

**Indexes.**
- Neptune maintains three full statement indexes by default: **SPOG, POGS and GPSO**.
- Together with an index of distinct predicates, they cover all 16 combinations of bound and unbound positions.
- Access patterns that would need **OSGP** fall back to scanning POGS once per predicate — for example, "all incoming edges of a vertex" with no edge label given [CLAIM-amazon-neptune-11].
- OSGP can be switched on through Lab Mode, **but only on an empty cluster**. AWS documents the cost: inserts up to 23 % slower and storage up to 20 % larger [CLAIM-amazon-neptune-11].

**No user-defined indexes.** A property-equality lookup without a label (`MATCH (n {key:$v})`) becomes a POGS prefix scan on (P = key, O = value), so it is still indexed. The EOIP adapter's lookups on `eoip_vid` and `canonical_id` are therefore index-backed, not full scans (*reasoned inference* from the index table).

**Known weak spot.** Reverse traversals without an edge label (`in()`, `both()`, and `drop()` of vertices) are slow, especially in graphs with many distinct predicates [CLAIM-amazon-neptune-11].

**Shared storage volume.**
- The writer and replicas share one volume, so replicas do not replay writes.
- AWS states that the volume spans three Availability Zones and that losing two copies does not affect write availability [CLAIM-amazon-neptune-26].
- Nothing beyond those statements is public (*NOT PUBLICLY VERIFIED*). *Hypothesis:* a log-structured storage service with quorum replication, similar to Aurora's.

**Index growth.** 1.5.0.0 adds an online index rebuild that defragments index storage and reclaims space while the database keeps running [CLAIM-amazon-neptune-02]. This suggests index storage grows under heavy churn, as LSM or B-tree indexes with tombstones do. The actual structure is a *hypothesis*.

### 5.3 Query pipeline and planning

**Gremlin.**
- Text queries are parsed with TinkerPop's `gremlin-language` ANTLR grammar; no Groovy is executed.
  - This is why there are no variables, no bindings and no lambdas.
  - It also means a text query cannot inject arbitrary JVM code [CLAIM-amazon-neptune-03].
- Each step either runs natively or falls back to the TinkerPop reference implementation. Release 1.5.0.0 widens the set of steps the native "DFE" engine handles, following TinkerPop 3.8 semantics [CLAIM-amazon-neptune-02].
- Each traversal runs as its own transaction. Text submissions cannot call `tx.commit()` or `tx.rollback()`. Statements separated by `;` or a newline run together in one transaction [CLAIM-amazon-neptune-03].

**openCypher.**
- The baseline is Cypher 9.
- AWS documents these gaps [CLAIM-amazon-neptune-04]:
  - no `CALL` procedures in Neptune Database;
  - no user-defined functions;
  - no `shortestPath` or `allShortestPaths`;
  - no `UNION` in mutating queries;
  - only constant values in `SKIP` and `LIMIT`;
  - property filters on variable-length paths must be constants.
- Release 1.5.0.0 [CLAIM-amazon-neptune-34]:
  - adds native `all`, `any`, `none` and `single`, plus regex predicates on the DFE engine;
  - improves join ordering across `WITH` and `BIND` stages, which indicates a cost-based join-order optimiser shared by openCypher and SPARQL.

**SPARQL 1.1.**
- Runs over the same quad indexes.
- The default graph is the union of all named graphs.
- Numbers are limited to 64 bits.
- No entailment regime is documented [CLAIM-amazon-neptune-06].

*Reconstruction sketch (a hypothesis consistent with the documentation):*
```
parse(text) -> AST -> logical plan of quad patterns (S?,P?,O?,G?) + joins + filters
for each pattern: choose the index by bound prefix (SPOG|POGS|GPSO|OSGP|predicate-union)
join order: cost model over dictionary statistics + bindings produced by earlier stages (1.5.0.0)
execute: pipelined/vectorised operators (DFE), or TinkerPop fallback per step
```

### 5.4 Reasoning

None of the documentation we read mentions RDFS or OWL entailment or a rule engine. SPARQL evaluates over asserted triples only (an *absence inferred* from the compliance page, which lists no entailment regime [CLAIM-amazon-neptune-06]). EOIP's reasoning (BL-30) must therefore run outside Neptune: either materialise inferred facts in EOIP, or run a reasoner over exported RDF.

### 5.5 Concurrency and transactions

**Reads.**
- Read-only queries run under **snapshot isolation using MVCC** and take no locks.
- Replicas serve only these snapshot-isolated reads [CLAIM-amazon-neptune-10].

**Writes.**
- Mutation queries read at READ COMMITTED, strengthened against non-repeatable and phantom reads by **range (gap) locks** on whichever index the read used.
- A blocked writer waits up to **60 s** and is then rolled back.
- Deadlocks are resolved at once by aborting the transaction that made the fewest changes [CLAIM-amazon-neptune-10].

**False conflicts.**
- Gap locks cover more than the logical predicate, because neighbouring dictionary IDs collide.
- AWS states that "under a high load … 3–4 % of write queries fail because of false conflicts". Clients must retry these [CLAIM-amazon-neptune-10].
- A retry can itself hit a false conflict while the earlier attempt's rollback is still releasing its locks [CLAIM-amazon-neptune-10]. Clients should therefore retry with backoff and jitter.

**Weaker paths.**
- The bulk loader is **not ACID** [CLAIM-amazon-neptune-08].
- Neptune Analytics vector updates are **neither atomic nor isolated**: they become visible and durable immediately, even if the surrounding query later fails [CLAIM-amazon-neptune-19].

### 5.6 Partitioning and consistency

- Neptune Database is **single-sharded**: one writer per cluster. Reads scale out to up to 15 replicas, and Global Database adds copies in other regions [CLAIM-amazon-neptune-14][CLAIM-amazon-neptune-12].
- Writes are strongly consistent on the writer. Replicas are eventually consistent, "usually in less than 100 ms" [CLAIM-amazon-neptune-12].
- Write throughput is therefore limited to what one instance can do — on Serverless, up to 128 NCU (256 GB) [CLAIM-amazon-neptune-13].

### 5.7 Caching

- Each instance has a buffer cache.
- An optional lookup cache exists for provisioned instances but **does not work with Serverless** [CLAIM-amazon-neptune-13].
- When a Serverless instance scales down, cached data is evicted. AWS advises a higher minimum NCU for workloads that depend on the cache [CLAIM-amazon-neptune-13].
- Whether Neptune Database caches query results is *NOT PUBLICLY VERIFIED*.

### 5.8 Versioning and change history

- Neptune has no time-travel queries.
- Within the stream retention window (1–90 days), Streams keep an ordered, complete change log. AWS says this log can reconstruct the database state at any point *if the starting state is known* [CLAIM-amazon-neptune-14].
- Longer history requires snapshots or point-in-time restore, which restore a whole cluster rather than answering queries.
- EOIP's application-level bitemporal model (BL-37) therefore remains necessary on Neptune.

### 5.9 Security

- **Network:** reachable only inside a VPC, and only over TLS 1.2 [CLAIM-amazon-neptune-08].
- **Authentication:** with IAM enabled, every HTTP request must carry an AWS SigV4 signature for service name `neptune-db`. Bolt carries a signed header bundle in the basic-auth credentials field. Signatures expire after about 5 minutes [CLAIM-amazon-neptune-07][CLAIM-amazon-neptune-17].
- **No passwords:** "Amazon Neptune does not support user name/password–based access control" [CLAIM-amazon-neptune-08].
- **Authorization:**
  - permissions are granted per cluster and per query action (`Read/Write/DeleteDataViaQuery`), refined by IAM condition keys and tags;
  - Neptune works out every action a query *could* perform before running it — for example, every openCypher `SET` needs Delete permission [CLAIM-amazon-neptune-09];
  - there is no access control on labels, properties or rows. AWS says finer control "can be implemented at the application layer" [CLAIM-amazon-neptune-12].
- **Tenancy:** one graph per cluster. Multi-tenancy means either one cluster per tenant (silo) or a `tenantId` property enforced by the application (pool) [CLAIM-amazon-neptune-12][CLAIM-amazon-neptune-32].

### 5.10 EOIP adapter, as observed in code — resolves U-03

`packages/eoip/graph/neptune.py` (409 lines) [CLAIM-amazon-neptune-29].

**Authentication (lines 58–79): there is no SigV4 signing.**
- The client is created as `httpx.Client(..., auth=(username, password) if username or password else None, trust_env=False)`. That is HTTP Basic authentication, or nothing.
- Nowhere in `packages/eoip` is there a `botocore` import, a `SigV4Auth` call, an `x-amz-*` header or an AWS credential provider. The only "SigV4" strings are descriptive labels in `graph/database_adapters.py:126,153`.
- The factory (`graph/backends.py:212-224`) passes only `username`, `password` and `verify_tls`. The config file (`config/graph-store.yaml:21-28`) and the Helm values have no region, role or credential fields.
- **Effect:**
  - against a cluster with IAM authentication enabled, every request fails;
  - against a cluster without IAM, the Basic credentials are simply ignored, because Neptune has no password authentication [CLAIM-amazon-neptune-08]. Security then rests entirely on the VPC and its security groups.
- **U-03 is resolved: SigV4 support is Absent.**

**Protocol.**
- The adapter uses openCypher over HTTPS form posts: `query`, plus `parameters` as a JSON string.
- SPARQL is a pass-through that posts `query=` only. SPARQL Update, which needs `update=`, is not supported.
- Gremlin is a JSON pass-through that rejects bindings. Rejecting bindings is correct for Neptune.

**Identity.**
- Vertices are written with `MERGE (n:Label {canonical_id:$cid}) SET n += $props`, and get a property `eoip_vid = "eoip-" + sha256(canonical_id)`.
- The adapter does **not** set Neptune's own `~id`. Neptune therefore generates UUIDs, and EOIP identity depends on a property.
- Element-ID uniqueness — the only uniqueness guarantee Neptune has [CLAIM-amazon-neptune-12] — goes unused.

**Edges.**
- `upsert_edge` makes **three round trips**: two `get_vertex` calls and one `MERGE`.
- `edges_from` and `edges_to` fetch `limit` edges and only *then* filter by label in Python. When a vertex has more than `limit` edges, label-filtered neighbourhoods are silently truncated. This defect applies whatever the backend.

**Bulk load.** Rows are upserted one by one, about N + 3M requests for N vertices and M edges. Neither the Neptune S3 bulk loader nor the 1.5.0.0 offline loader is used.

**Neptune features the adapter does not use:**
- IAM / SigV4;
- routing reads to the reader endpoint (there is one URL);
- retrying on `ConcurrentModificationException` or other false conflicts;
- Streams;
- the bulk loader;
- Bolt;
- explain and profile;
- query-timeout hints (there is only a client-side time budget);
- Neptune Analytics — only a manifest entry exists, and it wrongly says Gremlin [CLAIM-amazon-neptune-30];
- full-text search;
- Neptune ML;
- tenant handling (consistent with BL-20).

**Misleading capability report.**
- `capabilities()` advertises `models: ["property_graph","rdf"]` and exports that include `shacl`, `gql` and `pgql`.
- Neptune executes none of those three, and the adapter has no path for writing RDF.
- Because Neptune keeps RDF and property-graph data apart, EOIP's property-graph writes are invisible to `execute_sparql`.
- Separately, `graph/database_adapters.py:323` sends Neptune queries through a regex Cypher-to-Gremlin translator, although Neptune runs openCypher natively [CLAIM-amazon-neptune-31].

## 6. Functional and non-functional requirements inferred from verified behaviour

| ID | Requirement for EOIP's Neptune support | Derived from |
|---|---|---|
| FR-NEP-01 | Sign every HTTPS, WebSocket and Bolt request with SigV4 — service `neptune-db`, or `neptune-graph` for Neptune Analytics — using the standard AWS credential chain, including STS session tokens and their refresh | [CLAIM-amazon-neptune-07][CLAIM-amazon-neptune-17] |
| FR-NEP-02 | Use a deterministic `~id` = f(tenant, canonical_id), so the engine's only uniqueness guarantee also enforces EOIP identity | [CLAIM-amazon-neptune-12][CLAIM-amazon-neptune-03] |
| FR-NEP-03 | Encode property values for Neptune: omit `null`; store maps as JSON strings or flatten them; store lists as JSON strings or as sets, under a declared contract; store datetimes in UTC, with the offset in a separate field when it matters | [CLAIM-amazon-neptune-03][CLAIM-amazon-neptune-05][CLAIM-amazon-neptune-06] |
| FR-NEP-04 | Retry mutations on concurrent-modification errors and lock-wait timeouts, with bounded exponential backoff and jitter; use only idempotent `MERGE` statements | [CLAIM-amazon-neptune-10] |
| FR-NEP-05 | Send reads that must see the caller's own writes to the writer endpoint; other reads may use the reader endpoint | [CLAIM-amazon-neptune-10][CLAIM-amazon-neptune-12] |
| FR-NEP-06 | Isolate tenants either with one cluster per tenant (silo) or with a tenant predicate that EOIP's query gateway injects into every query (pool); never rely on callers to add it | [CLAIM-amazon-neptune-12] |
| FR-NEP-07 | Report the real dialect gaps in capability negotiation: no `CALL` in Neptune Database, no `shortestPath`, no bindings, RDF isolated from property-graph data | [CLAIM-amazon-neptune-04][CLAIM-amazon-neptune-26] |
| NFR-NEP-01 | Never make Neptune a mandatory dependency; air-gapped installs must not need it | §4.3-1, [CLAIM-amazon-neptune-08] |
| NFR-NEP-02 | Run the parity test suite against an engine version still inside its support window (1.3.x or later until 2027-03) | [CLAIM-amazon-neptune-01] |
| NFR-NEP-03 | Keep each HTTP request below 150 MB, and size batches accordingly | [CLAIM-amazon-neptune-08] |

## 7. Performance and resource model

**No independent benchmark found.** In this pass we found no third-party benchmark of Neptune Database or Neptune Analytics that states its hardware and dataset. As far as we checked, LDBC lists no audited Neptune result (**UNVERIFIED**; not searched exhaustively).

**Vendor claims (not usable for comparison).**
- Neptune Database can "scale to 100,000 queries per second".
- Neptune Analytics handles "tens of billions of relationships" and "thousands of analytic queries per second".
- None of these states a workload or hardware [CLAIM-amazon-neptune-36].

**Documented resource figures.**

| Item | Value | Evidence |
|---|---|---|
| Serverless capacity | 1 NCU = 2 GiB plus vCPU; 1.0–128 NCU (256 GB) | [CLAIM-amazon-neptune-13] |
| Neptune Analytics capacity | 16–24,576 m-NCU, where 1 m-NCU = 1 GB; 0–2 replicas, each billed again | [CLAIM-amazon-neptune-20][CLAIM-amazon-neptune-23] |
| Storage volume | up to 128 TiB | [CLAIM-amazon-neptune-08] |
| Cost of the OSGP index | storage +20 %, insert rate −23 % | [CLAIM-amazon-neptune-11] |
| Cost of Streams | slightly slower writes, plus I/O and storage charges | [CLAIM-amazon-neptune-14] |
| False write conflicts | 3–4 % of writes under high load | [CLAIM-amazon-neptune-10] |
| Lock wait before rollback | 60 s | [CLAIM-amazon-neptune-10] |
| Connection limits | 32,768 WebSockets on large instances; 1,000 Bolt connections | [CLAIM-amazon-neptune-28][CLAIM-amazon-neptune-17] |

**Cost examples (us-east-1, from the pricing page) [CLAIM-amazon-neptune-23].**
- db.r5.large instance: $0.348 per hour.
- Standard storage: $0.10 per GB-month, plus I/O at $0.20 per million requests.
- I/O-Optimized storage: $0.225 per GB-month, with no I/O charge.
- Neptune Analytics: the page's example of $7.68 per hour for 256 GB implies about $0.03 per m-NCU-hour. The page does not state that rate (*reasoned inference*). On that basis the smallest graph (16 m-NCU) costs roughly $0.48 per hour, about $350 per month, before replicas.

**EOIP adapter cost model (reasoned from the code).**
- One vertex upsert takes 1 request; one edge upsert takes 3.
- `bulk_load` of N vertices and M edges therefore takes N + 3M requests, all made one after another.
- With an in-VPC round trip of *r* ms, the total time is about (N + 3M) × r.
- Example: 1 M vertices and 3 M edges need about 10 M requests — about 2.8 hours at 1 ms per request and 28 hours at 10 ms, before any lock waits.
- AWS's documented path for volumes like this is the S3 loader [CLAIM-amazon-neptune-15].

**Failure modes.**
- Rollbacks after lock waits when many writes hit the same vertex. Hub ("supernode") vertices concentrate gap locks on one subject prefix (*hypothesis* drawn from the locking documentation).
- A cold cache after a Serverless instance scales down.
- Replica lag during write bursts when readers have a low minimum NCU [CLAIM-amazon-neptune-13].
- Stream reads competing with queries for the same resources [CLAIM-amazon-neptune-14].
- SigV4 signatures expiring in long-lived Bolt connection pools [CLAIM-amazon-neptune-17].

## 8. Strengths and use-case-specific advantages — and how each could be matched or exceeded

1. **Three query languages and two data models in one managed engine** [CLAIM-amazon-neptune-02][CLAIM-amazon-neptune-26].
   - *Match:* EOIP already speaks all three through its adapters (BL-04, BL-06).
   - *Exceed:* a typed, backend-neutral QueryPlan compiled for each dialect (CAP-20). Neptune cannot offer this itself, because its property-graph and RDF data cannot see each other.
2. **Durability with no operations work.** Storage across three Availability Zones, 15 replicas, point-in-time restore and Global Database [CLAIM-amazon-neptune-26][CLAIM-amazon-neptune-12].
   - *Integrate:* for AWS customers, EOIP should hand high availability and disaster recovery to Neptune rather than duplicate them.
3. **An ordered, complete, transactional change log (Streams)** [CLAIM-amazon-neptune-14].
   - *Match / exceed:* EOIP's SourceEvent log and mutation stream (BL-23, BL-52) are backend-neutral.
   - Streams can still serve as an *external consistency check*, and can tell EOIP to refresh its indexes when another writer has touched the cluster.
4. **Algorithms plus vector top-k inside one openCypher statement (Neptune Analytics)** [CLAIM-amazon-neptune-18][CLAIM-amazon-neptune-19].
   - *Integrate* as an optional analytics target alongside EOIP's in-process algorithms (BL-43).
   - *Exceed* by storing the results in EOIP's prediction plane (J8) with provenance.
5. **Query permissions decided before execution** [CLAIM-amazon-neptune-09].
   - *Integrate:* give EOIP's read-only agent role only `ReadDataViaQuery`. Neptune then blocks agent writes even if EOIP has a bug — defence in depth for read-only agents (§4.3-8).
6. **Bulk loading from S3, including a new offline fast path** [CLAIM-amazon-neptune-15][CLAIM-amazon-neptune-02].
   - *Integrate* behind EOIP's governed mutation path: EOIP writes validated CSV files, and Neptune loads them.

## 9. Limitations with root causes

**Documented gaps and defects**
- No `CALL` procedures, user-defined functions or `shortestPath` in Neptune Database openCypher [CLAIM-amazon-neptune-04].
- No Gremlin bindings [CLAIM-amazon-neptune-03].
- The bulk loader is not ACID [CLAIM-amazon-neptune-08].
- Neptune Analytics vector updates are not atomic [CLAIM-amazon-neptune-19].
- openCypher returns an arbitrary value when a property has several [CLAIM-amazon-neptune-04].
- The `boto3` `neptunedata` client cannot send SPARQL [CLAIM-amazon-neptune-07].

**Intentional trade-offs**
- One writer and no sharding [CLAIM-amazon-neptune-14].
- Three default indexes; OSGP only on an empty cluster [CLAIM-amazon-neptune-11].
- Datetimes converted to UTC [CLAIM-amazon-neptune-06].
- Gap locks that cause false conflicts [CLAIM-amazon-neptune-10].

**Licensing and commercial restrictions**
- A proprietary service. It cannot be embedded in, redistributed with or OEM-shipped inside EOIP; it runs only in the customer's own AWS account.
- Benchmark publication is governed by AWS's terms. Whether a "DeWitt clause" applies is **UNVERIFIED**; legal review is recommended.

**User-reported complaints (third-party, not independently verified)**
- Neo4j Bolt drivers failed to re-authenticate with IAM once a signature expired, until driver-side token managers appeared. AWS itself documents this and cites the Neo4j driver issues [CLAIM-amazon-neptune-17].
- LocalStack users report serializer incompatibilities between Gremlin driver versions [CLAIM-amazon-neptune-25].

**Outdated claims to avoid**
- "Neptune openCypher has no date/time arithmetic" — no longer true on 1.3.2.0+ with lab mode, or on Neptune Analytics [CLAIM-amazon-neptune-04].
- "Neptune has no Bolt support" — false since the 1.2.x releases [CLAIM-amazon-neptune-17].
- "Neptune Analytics supports Gremlin" — false [CLAIM-amazon-neptune-18].

**Root causes**
- *Algorithmic dead ends:*
  - reverse traversal without edge labels needs the non-default OSGP index [CLAIM-amazon-neptune-11];
  - the granularity of gap locks makes false conflicts unavoidable under contention [CLAIM-amazon-neptune-10];
  - there is no reasoning engine, so RDFS/OWL inferences must be materialised outside Neptune [CLAIM-amazon-neptune-06].
- *Operational and hardware overhead:*
  - VPC-only access means developers need a bastion host or VPN [CLAIM-amazon-neptune-08];
  - Neptune Analytics starts at 16 m-NCU [CLAIM-amazon-neptune-20];
  - Serverless evicts its cache when it scales down [CLAIM-amazon-neptune-13];
  - the bulk loader needs S3, an IAM role and an S3 VPC endpoint [CLAIM-amazon-neptune-15].
- *User and developer friction:*
  - there is no local engine; LocalStack's emulation is paid ("Ultimate" plan), Gremlin-centric and keeps no data between runs [CLAIM-amazon-neptune-25];
  - SigV4 signing is needed everywhere, including token refresh on Bolt [CLAIM-amazon-neptune-17];
  - dialect deviations [CLAIM-amazon-neptune-03][CLAIM-amazon-neptune-04];
  - coarse IAM makes application-level access control unavoidable [CLAIM-amazon-neptune-12].

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint (§4.3) | Assessment |
|---|---|
| 1 Air-gap / local-first | **Fails.** Neptune is cloud-only, reachable only inside a VPC, and depends on the AWS control plane [CLAIM-amazon-neptune-08]. It is acceptable only as an *optional backend that a customer requests*. It must never be part of the default install or the default test path. AWS GovCloud and China regions exist [CLAIM-amazon-neptune-33]; that helps regulated customers but is still not air-gapped. |
| 2 LLM egress | Does not apply to Neptune Database. Bedrock-based GraphRAG on Neptune Analytics (mentioned in AWS announcements [CLAIM-amazon-neptune-35]) would be an external LLM path and must stay behind EOIP's egress gateway (BL-45). |
| 3 Backend neutrality | Neptune stays a supported backend. Its native features — Streams, the loader, Neptune Analytics — are *available upstream but not integrated*. They must be optional adapters, never required by core features. |
| 4 Canonical pipeline | Compatible. EOIP stays the only writer and Neptune is a projection target. Other writers to the same cluster would bypass governance; Streams can detect them (STR-amazon-neptune-03). |
| 8 Permissions survive | Neptune offers only coarse IAM [CLAIM-amazon-neptune-09][CLAIM-amazon-neptune-12]. Per-fact ACL filtering (BL-18, P0) must be enforced in EOIP, before and after each query. |
| 9 Tenant isolation | One graph per cluster [CLAIM-amazon-neptune-12]. Silo = one cluster per tenant (Serverless makes this affordable at small scale). Pool = a tenant predicate injected by EOIP. The adapters contain no tenant handling today (BL-20). |
| 10 One-node first | Does not apply (managed service). The smallest footprint is one Serverless instance at 1.0 NCU, or a db.t4g.medium. Development needs an AWS account. |
| 12 Redistribution | The service itself raises no redistribution question, because it runs in the customer's own AWS account. Client libraries are Apache-2.0 (TinkerPop, graph-notebook) plus the Neo4j drivers, whose licences are researched in T-C01-neo4j. **Legal-review trigger: no** for client code. **Commercial review: yes** for any EOIP offering that resells Neptune capacity (AWS Service Terms). |

**Local substitutes for development and testing.** There is no official local version of Neptune. The options are:

1. **Apache TinkerPop Gremlin Server with TinkerGraph 3.8.x** (Apache-2.0).
   - Closest to Neptune 1.5.0.0's Gremlin semantics (TinkerPop 3.8.0–3.8.1).
   - Differences: TinkerGraph keeps insertion order and supports List cardinality, bindings and Groovy scripts; Neptune supports none of these.
   - Configure the server to use the `gremlin-lang` grammar, and run a "Neptune strict" linter over all queries.
2. **openCypher.** No open-source engine reproduces Neptune's dialect exactly.
   - Neo4j Community can run the common Cypher 9 subset; it is GPL-3.0, which is a legal-review trigger for redistribution.
   - Memgraph and FalkorDB can also run that subset.
   - Any of them needs a Neptune-dialect linter in front: no `CALL`, no `shortestPath`, constant variable-length-path filters, scalar properties only.
3. **SPARQL.** Apache Jena Fuseki or Oxigraph, configured to treat the default graph as the union of named graphs, as Neptune does [CLAIM-amazon-neptune-06]. EOIP already has a Fuseki adapter (BL-06).
4. **LocalStack's Neptune emulation** [CLAIM-amazon-neptune-25].
   - Commercial "Ultimate" plan, based on Gremlin Server 3.7.2, enforces IAM for Gremlin, keeps no data between runs.
   - Useful for SigV4 tests. Not redistributable, and irrelevant to air-gapped installs.
5. **Final check against the real service.** A short-lived Serverless cluster (minimum 1.0 NCU) in CI runs the J14 parity suite. Run it only when a customer contract requires Neptune.

## 11. Competitive delta against the EOIP verified baseline

| Capability | Neptune | EOIP baseline | Delta |
|---|---|---|---|
| Backend adapter | managed engine | BL-04: implemented, never tested live | **EOIP gap:** no SigV4, so the adapter cannot connect to IAM-enabled clusters [CLAIM-amazon-neptune-29]. U-03 resolved as Absent. |
| Identity enforcement | element-ID uniqueness only | BL-30/34: deterministic IDs in the application, but the adapter stores them as a property, not as `~id` | EOIP should map canonical IDs onto `~id` (INV-amazon-neptune-03) |
| Schema constraints | none | BL-28: validation gate | EOIP ahead; keep enforcing in the gateway |
| Reasoning | none | BL-30: partial, in-house | EOIP ahead in scope; neither is standards-grade |
| Temporal data | none (only the Streams window) | BL-37: application-level bitemporal model | EOIP ahead |
| Change data capture | Streams, native | BL-52: in-process stream | Neptune ahead on durability; integrate |
| Bulk load | S3 loader and offline loader | BL-01: `bulk_load` upserts row by row on Neptune | Neptune ahead; integrate (cloud-only) |
| Graph algorithms | Neptune Analytics (25+) | BL-43: pure Python, in-process | Neptune ahead at scale; optional pushdown |
| Vector search | Neptune Analytics only | BL-14: partial | Parity unclear; DEFER |
| Authentication | IAM SigV4, per-action query permissions | BL-19: RBAC/ABAC on the API | Complementary; EOIP must sign its requests |
| Source-ACL filtering | none | BL-18: **Absent** | Both absent → P0 build in EOIP |
| Tenancy | one cluster per tenant, or enforced by the application | BL-20: contract only | Both rely on the application in pool mode |
| Query portability | three dialects, isolated data models | BL-08/09: QueryPlan plus a partial transpiler | EOIP's model is the right direction but needs per-dialect profiles |
| Description of Neptune Analytics | openCypher | `adapters/manifests.py:428-435` says "Gremlin (serverless analytics)" | **Defect in EOIP's manifest** [CLAIM-amazon-neptune-30] |
| Air-gapped operation | impossible | CAP-50: design goal | Structural EOIP advantage |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | competitor | strength | evidence | value to EOIP customers | match / exceed / integrate / reject | design approach | acceptance test |
|---|---|---|---|---|---|---|---|
| STR-amazon-neptune-01 | Amazon Neptune | Gremlin, openCypher and SPARQL in one managed engine | [CLAIM-amazon-neptune-02][CLAIM-amazon-neptune-26] | AWS customers keep their existing graph tooling | exceed | Compile QueryPlans into per-dialect templates with a *Neptune dialect profile* (no bindings, no `CALL`, scalar properties). Project EOIP data to RDF through EOIP's mapping layer (BL-33) so SPARQL can see it — something Neptune's data-model isolation otherwise prevents. | T-NEP-02: 30 core QueryPlans return identical results on HugeGraph, Neo4j and Neptune (openCypher), and the same projection is visible through SPARQL on Neptune's RDF side |
| STR-amazon-neptune-02 | Amazon Neptune | Managed high availability and disaster recovery: storage across three Availability Zones, 15 replicas, point-in-time restore, Global Database | [CLAIM-amazon-neptune-26][CLAIM-amazon-neptune-12] | No graph operations team needed | integrate | When the backend is Neptune, EOIP relies on Neptune snapshots; `scripts/backup.py` records snapshot ARNs in EOIP's evidence log instead of dumping data | T-NEP-10: restore a snapshot to a new cluster; EOIP's conformance and revision-history checks pass |
| STR-amazon-neptune-03 | Amazon Neptune | Ordered, complete, transactional change log (Streams) | [CLAIM-amazon-neptune-14] | Fresh indexes and caches; detection of writes that bypass EOIP | integrate | Optional `NeptuneStreamWatcher` worker compares each stream record's `edge_key` or `canonical_id` with EOIP's mutation log. Writes EOIP does not know about raise a governance alert; known writes trigger re-indexing. | T-NEP-07: after 10k mutations, indexes are fresh within 5 s at p95; a write made outside EOIP is flagged every time |
| STR-amazon-neptune-04 | Amazon Neptune | Algorithms and vector top-k inside one openCypher query (Neptune Analytics) | [CLAIM-amazon-neptune-18][CLAIM-amazon-neptune-19] | Graph analytics at scales EOIP's Python algorithms (BL-43) cannot reach | integrate (optional, P2) | An `AnalyticsBackend` protocol: copy the graph, run the algorithm, write results to the prediction plane with the algorithm's version and parameters | T-NEP-11: PageRank and Louvain on a 1 M-edge copy match EOIP's in-process results (rank correlation ≥ 0.99; NMI ≥ 0.9), and no result lands in the fact plane |
| STR-amazon-neptune-05 | Amazon Neptune | Query permissions decided by IAM before execution | [CLAIM-amazon-neptune-09] | Read-only agents cannot write, even if EOIP has a bug | integrate | A separate IAM role for each class of EOIP principal; MCP and agent traffic is signed with a role that has only `ReadDataViaQuery` | T-NEP-12: Neptune rejects a mutation sent with the agent role (403-class error) |
| STR-amazon-neptune-06 | Amazon Neptune | S3 bulk loader and offline fast loader | [CLAIM-amazon-neptune-15][CLAIM-amazon-neptune-02] | Initial loads take hours instead of days | integrate | EOIP writes each validated batch as Neptune CSV into the customer's S3 bucket and starts a loader job; EOIP records the job ID, row counts and errors as evidence | T-NEP-09: loading 1 M vertices and 3 M edges is at least 10× faster than row upserts, with identical counts and no validation-gate violations |

### Inversion cards

**INV-amazon-neptune-01 — The engine is cloud-only and reachable only inside a VPC**
- **Target:** Neptune Database 1.5.0.0 and Neptune Analytics; every workload.
- **Limitation:** Neptune runs only inside an AWS VPC. There is no on-premises or air-gapped option, and development needs an AWS account or a paid emulator [CLAIM-amazon-neptune-08][CLAIM-amazon-neptune-25].
- **Root cause:** deployment model (proven).
- **Why an alternative mitigates it:** EOIP's backend-neutral `GraphStore` lets the same governed pipeline run on HugeGraph or Neo4j on a single node. Neptune becomes one deployment profile, not the architecture.
- **When the alternative is worse:** AWS-native customers would lose managed high availability if pushed onto self-hosted engines.
- **Options:**
  - (a) Quick: keep Neptune opt-in and document that it is excluded from J16.
  - (b) Pragmatic: a "Neptune dialect profile" whose parity suite runs offline on TinkerGraph 3.8 and Fuseki, behind a strict linter.
  - (c) Long term: a backend capability matrix generated from conformance runs and published with each release.
- **Selected:** (b) and (c).
- **Design sketch:**
  ```
  profile neptune-1.5:
    gremlin: grammar=gremlin-lang, bindings=false, cardinality=set, ids=string
    cypher:  call=false, shortestPath=false, vlp_prop_filter=constant, props=scalar
    sparql:  default_graph=union
  CI: lint(queries, profile) -> run(suite, tinkergraph-3.8 | fuseki) -> [nightly, optional] run(suite, neptune-serverless)
  ```
- **Falsifiable POC (T-NEP-08):** the parity suite on the local substitutes predicts at least 95 % of Neptune's pass/fail outcomes. Each live run costs at most 1 NCU-hour.
- **Dependencies and security:** AWS credentials live only in CI secrets; no customer data enters CI.
- **Defensibility:** air-gap support is structural. A cloud vendor cannot copy it without shipping its engine on-premises.
- **Decision: ADOPT.**
- **Seed hypotheses:** none of the rows in Master Prompt §10.5 targets Neptune. The additional direction "replace fixed vendor query languages with typed query plans plus adapters" is **validated** by this card and by INV-amazon-neptune-04.

**INV-amazon-neptune-02 — Coarse authorization and one graph per cluster**
- **Target:** Neptune Database; multi-tenant, permission-sensitive retrieval (J5, J13).
- **Limitation:** IAM covers only the cluster and the read, write and delete actions. There is no label, property or row security, and a cluster holds one graph [CLAIM-amazon-neptune-09][CLAIM-amazon-neptune-12].
- **Root cause:** governance and data model (proven).
- **Why an alternative mitigates it:** a policy-enforcing query gateway in EOIP adds tenant and ACL predicates to every compiled plan and filters the results afterwards. In silo mode, each tenant gets its own cluster.
- **When the alternative is worse:** injected predicates make queries more expensive, and EOIP becomes the only guard if raw endpoint access leaks. Silo mode multiplies fixed costs.
- **Options:**
  - (a) Silo only: one cluster per tenant, using Serverless.
  - (b) Pool: gateway-injected `tenant_id` and `acl_hash` predicates, plus a separate IAM role per EOIP service.
  - (c) Long term: tenant-scoped `~id` namespaces, per-tenant IAM tag conditions and EOIP relationship-based access control (CAP-46).
- **Selected:** (b) by default; (a) for regulated tenants.
- **Sketch:**
  ```
  compile(plan, ctx) = plan.with(where=[n.tenant_id = ctx.tenant, n.acl_hash IN ctx.acl_set])
  post_filter(rows, ctx.principal)
  ```
- **POC (T-NEP-05, J13):** two tenants and 10k adversarial queries. Success: zero rows from another tenant, and at most 15 % extra latency at p95.
- **Failure cases:** a raw Gremlin pass-through skips injection, so `execute_gremlin` and `execute_opencypher` must be restricted to administrators.
- **Defensibility:** ACL-aware retrieval on every backend is EOIP's product promise. Neptune's design leaves that work to applications.
- **Decision: ADOPT.**

**INV-amazon-neptune-03 — No constraints other than element-ID uniqueness**
- **Target:** Neptune Database; idempotent ingest (J7).
- **Limitation:** Neptune cannot declare `canonical_id` unique [CLAIM-amazon-neptune-12]. EOIP's `MERGE … {canonical_id}` relies on Neptune's range locks to stay safe under concurrent writes [CLAIM-amazon-neptune-10].
- **Root cause:** data model (proven).
- **Alternative:** set `~id = "eoip:" + sha256(tenant || canonical_id)` and create vertices with `MERGE (n {`~id`: $id})`; Neptune supports custom IDs in `MERGE` [CLAIM-amazon-neptune-04]. The engine's ID uniqueness then enforces EOIP identity, and lookups become direct reads on the SPOG index.
- **When worse:** merging or splitting identities (BL-35) would require changing keys. Use a stable surrogate ID plus an alias edge instead of changing `~id`.
- **Options:**
  - (a) Keep the property.
  - (b) Use `~id` for new deployments, with a migration tool.
  - (c) Make hash IDs the primary key on every backend.
- **Selected:** (b), then (c).
- **POC (T-NEP-04):** 32 concurrent writers each perform 50k overlapping upserts. Success: zero duplicate canonical IDs, and requests per edge upsert drop from 3 to 1.
- **Migration:** during a transition window the adapter reads both `eoip_vid` and `~id`, which keeps it backward compatible.
- **Decision: ADOPT.**

**INV-amazon-neptune-04 — Dialect deviations break naive portability**
- **Target:** Gremlin 3.8 and openCypher on 1.5.0.0.
- **Limitation:**
  - Gremlin: no bindings or variables, set cardinality by default, no Map, List or null values [CLAIM-amazon-neptune-03];
  - openCypher: no `CALL`, no `shortestPath`, no mutating `UNION`, and an arbitrary choice when a property has several values [CLAIM-amazon-neptune-04][CLAIM-amazon-neptune-05];
  - the TinkerPop 3.8 upgrade in 1.5.0.0 can *silently* change the results of existing queries [CLAIM-amazon-neptune-02].
- **Root cause:** semantics and maturity (proven).
- **Alternative:** EOIP compiles typed plans for each backend profile and owns the encoder for property values.
- **When worse:** hand-tuned native queries can beat generated ones.
- **Options:**
  - (a) Document the gaps.
  - (b) A profile-aware compiler, a value encoder and a regression suite run before each engine upgrade.
  - (c) A formal intermediate representation with declared semantics (CAP-20).
- **Selected:** (b).
- **POC (T-NEP-06):** round-trip every EOIP property type (str, int, float, bool, datetime with offset, list, dict, None) through the encoder on all backends — the values must come back identical. Also compare 30 plans on 1.4.8.1 against 1.5.0.0 — there must be no unexplained differences.
- **Decision: ADOPT.**

**INV-amazon-neptune-05 — False write conflicts and 60-second lock waits under contention**
- **Target:** Neptune mutations; ingest bursts that hit hub vertices such as services and service accounts (J9).
- **Limitation:** under high load, gap locks make 3–4 % of writes fail with false conflicts, and a blocked writer waits up to 60 s [CLAIM-amazon-neptune-10].
- **Root cause:** algorithm — the granularity of the locks (proven).
- **Alternative:** EOIP's ingest worker groups batches by subject vertex, serialises writes to each hub vertex, and retries idempotent statements with jittered backoff. The EOIP adapter currently does none of this [CLAIM-amazon-neptune-29].
- **When worse:** serialising writes per hub limits throughput for a single very hot vertex.
- **Options:**
  - (a) A retry wrapper.
  - (b) Retries plus batches grouped by subject vertex.
  - (c) A write-combining queue that merges property updates per vertex before committing.
- **Selected:** (b).
- **POC (T-NEP-03):** 16 writers send 100k upserts concentrated on 50 hub vertices. Success: every write eventually succeeds, the retry rate is recorded, and p99 latency is at most twice the uncontended baseline.
- **Decision: ADOPT.**

**INV-amazon-neptune-06 — Neptune Analytics allows one vector index per graph, fixed at creation, with non-atomic updates**
- **Target:** Neptune Analytics; GraphRAG retrieval (CAP-53/56).
- **Limitation:** exactly one vector index, whose dimension is fixed when the graph is created. Updates are neither atomic nor isolated, and vectors cannot be imported from Neptune Database or from snapshots [CLAIM-amazon-neptune-19].
- **Root cause:** storage design (proven).
- **Alternative:** EOIP keeps embeddings in its own vector layer, versioned by model, so several models and dimensions can coexist per tenant. Neptune Analytics, if used at all, is an accelerator that can be rebuilt.
- **When worse:** a separate vector store is one more system to keep consistent.
- **Options:**
  - (a) Ignore Neptune Analytics vectors.
  - (b) Treat them as a derived cache rebuilt from EOIP.
  - (c) An EOIP-native hybrid index.
- **Selected:** (a) now; (b) as an experiment.
- **POC:** on the same embeddings, Neptune Analytics top-k reaches recall@10 of at least 0.95 against EOIP's HNSW index; the rebuild time is recorded.
- **Decision: DEFER.**

**INV-SELF-W03-01 (EOIP self-inversion; to be renumbered centrally) — The Neptune adapter cannot authenticate to IAM-enabled clusters**
- **Target:** `packages/eoip/graph/neptune.py` at HEAD `ad9937b`.
- **Limitation:** the adapter uses Basic authentication only, with no SigV4 [CLAIM-amazon-neptune-29]. Neptune ignores passwords [CLAIM-amazon-neptune-08], so the adapter either fails (IAM on) or runs unauthenticated inside the VPC (IAM off).
- **Root cause:** maturity (proven in code).
- **Options:**
  - (a) An optional `botocore` dependency providing a `SigV4Auth`-based `httpx.Auth` subclass that signs the method, path, query string and body hash, for service `neptune-db` and a configured region.
  - (b) Additionally cover Bolt (a signed token manager) and Neptune Analytics (`neptune-graph`).
  - (c) A pluggable credential-provider interface shared with other cloud backends.
- **Selected:** (a) now, (b) next.
- **Sketch:**
  ```python
  class SigV4HttpxAuth(httpx.Auth):
      requires_request_body = True
      def __init__(self, session, region, service="neptune-db"): ...
      def auth_flow(self, request):
          creds = self.session.get_credentials().get_frozen_credentials()  # refresh-aware
          aws_req = AWSRequest(method=request.method, url=str(request.url),
                               data=request.content, headers={"host": request.url.host})
          SigV4Auth(creds, self.service, self.region).add_auth(aws_req)
          request.headers.update(dict(aws_req.headers)); yield request
  ```
  `botocore` is Apache-2.0. Ship it as an *optional extra* (`eoip[aws]`) so air-gapped installs do not carry it.
- **POC (T-NEP-01):** a unit test against SigV4 test vectors using `httpx.MockTransport`, plus a live `RETURN 1` call to an IAM-enabled 1.5.0.0 Serverless cluster that returns 200.
- **Security:** no static keys in configuration — use the default credential chain (instance profile, IRSA, SSO) — and never log signed headers.
- **Defensibility:** not a differentiator; it is the minimum needed before EOIP can claim Neptune support.
- **Decision: ADOPT (P0 for any Neptune customer).**

## 13. Per-capability decisions

| CAP | Decision | Rationale |
|---|---|---|
| CAP-44 authentication (SigV4 for Neptune) | **BUILD** (in the adapter, as an optional extra) | Required to connect at all [CLAIM-amazon-neptune-07][CLAIM-amazon-neptune-29] |
| CAP-13 Gremlin, CAP-14 openCypher, CAP-15 SPARQL on Neptune | **INTEGRATE** | Native to the backend; keep openCypher as the main property-graph path |
| CAP-20 portable query IR (dialect profiles) | **BUILD** | Neptune's deviations prove the need [CLAIM-amazon-neptune-03][CLAIM-amazon-neptune-04] |
| CAP-30 deterministic identity keys (`~id`) | **BUILD** | INV-amazon-neptune-03 |
| CAP-08 constraints | **BUILD** in EOIP's gateway (Neptune has none) | [CLAIM-amazon-neptune-12] |
| CAP-06 bulk load | **INTEGRATE** the S3 loader (opt-in) | [CLAIM-amazon-neptune-15] |
| CAP-26/27 change data capture and event log | **INTEGRATE** Streams as an optional freshness and governance watcher; EOIP's log stays authoritative | [CLAIM-amazon-neptune-14] |
| CAP-62 algorithm library | **DEFER → INTEGRATE** Neptune Analytics as an optional pushdown (P2) | [CLAIM-amazon-neptune-18] |
| CAP-53 vector search | **DEFER** (Neptune Analytics vectors) | INV-amazon-neptune-06 |
| CAP-54 full-text search | **DEFER** (the OpenSearch coupling works only on AWS) | [CLAIM-amazon-neptune-16] |
| CAP-46 source-ACL enforcement | **BUILD** in EOIP (Neptune provides none) | [CLAIM-amazon-neptune-12] |
| CAP-47 tenant isolation | **BUILD** (pool injection) and **INTEGRATE** (silo clusters) | INV-amazon-neptune-02 |
| CAP-45 RBAC on the engine side | **INTEGRATE** per-action IAM roles for each class of EOIP principal | [CLAIM-amazon-neptune-09] |
| CAP-02 RDF storage on Neptune | **INTEGRATE** (P2) through EOIP's RDF projection into named graphs | [CLAIM-amazon-neptune-06] |
| CAP-22/23 reasoning on Neptune | **REJECT** waiting for it upstream; materialise inferences in EOIP | [CLAIM-amazon-neptune-06] |
| CAP-34/36 temporal data and history | **BUILD** (keep the application-level bitemporal model; Streams retention is too short) | [CLAIM-amazon-neptune-14] |
| CAP-74/76 backup, high availability, disaster recovery | **INTEGRATE** (delegate to Neptune) | [CLAIM-amazon-neptune-26] |
| CAP-75 observability | **INTEGRATE** the slow-query log and CloudWatch metrics into EOIP dashboards (P3) | [CLAIM-amazon-neptune-10] |
| CAP-18 explain and profile | **INTEGRATE** (diagnostics only, P3) | [CLAIM-amazon-neptune-04] |
| CAP-64 GNN (Neptune ML) | **REJECT** as a dependency (SageMaker, cloud-only); EOIP's ML tiers stay local | [CLAIM-amazon-neptune-26] |
| CAP-50 air-gapped operation | **REJECT** Neptune for air-gapped profiles, and document this | [CLAIM-amazon-neptune-08] |
| CAP-78 benchmark harness | **BUILD** the parity suite with local substitutes plus an optional live Neptune run | INV-amazon-neptune-01 |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All tests are PROPOSED; none has been run.

| Test | Setup | Acceptance |
|---|---|---|
| T-NEP-01 SigV4 | `httpx.MockTransport` capturing headers, with botocore SigV4 test vectors; then a live IAM-enabled 1.5.0.0 Serverless cluster (1.0–2.5 NCU) | Authorization header has the form `AWS4-HMAC-SHA256 Credential=…/neptune-db/aws4_request`; live `RETURN 1` returns 200; an expired STS token is refreshed without failures over 2 hours |
| T-NEP-02 Parity (J14) | Same ontology, a 10k-vertex synthetic digital thread, 30 QueryPlans on HugeGraph 1.7.0, Neo4j 5 and Neptune 1.5.0.0 | Identical result sets, or documented parity gaps with reasons |
| T-NEP-03 Contention | 16 writers, 100k upserts on 50 hub vertices | Every write eventually succeeds; no duplicates; p99 at most 2× baseline |
| T-NEP-04 Identity | 32 writers × 50k overlapping upserts using the `~id` scheme | Zero duplicate canonical IDs; one request per edge upsert |
| T-NEP-05 Tenancy (J13) | Two tenants in pool mode; 10k adversarial queries, including attempts to use raw pass-throughs | Zero rows from another tenant; raw endpoints refused to non-administrators |
| T-NEP-06 Value encoding | Every Python property type, including datetimes with time zones, lists, dicts and None | Lossless round trip through the encoder on every backend |
| T-NEP-07 Streams watcher | Streams enabled; 10k mutations plus one write made outside EOIP | Index freshness p95 ≤ 5 s; the outside write is flagged |
| T-NEP-08 Fidelity of local substitutes | Parity suite on TinkerGraph 3.8 and Fuseki compared with live Neptune | Pass/fail outcomes agree at least 95 % of the time |
| T-NEP-09 Bulk load | 1 M vertices and 3 M edges via the S3 loader vs row upserts | At least 10× faster; identical counts; loader errors recorded as evidence |
| T-NEP-10 Restore | Restore a snapshot into a new cluster | Conformance and revision-history checks pass |
| T-NEP-11 Analytics pushdown | 1 M-edge copy in Neptune Analytics (16 m-NCU) | PageRank Spearman correlation ≥ 0.99 against EOIP's in-process results; results stored only in the prediction plane |
| T-NEP-12 Agent role | MCP agent signed with a read-only role | Neptune rejects mutations |
| T-NEP-13 Adapter truncation regression | A vertex with 600 edges, 10 of them labelled X; call `edges_from(vid, ["X"], limit=500)` | All 10 returned (fails today, because the label filter runs after `LIMIT`) |

## 15. Risks, trade-offs, and open research questions

**Risks**
- *Silent changes in query semantics.* The 1.5.0.0 release notes warn that TinkerPop 3.8 changes "may not surface as errors" [CLAIM-amazon-neptune-02]. Mitigation: pin the engine version for each customer and run T-NEP-02 before every upgrade.
- *1.2.x reaches end of life on 2026-12-04* [CLAIM-amazon-neptune-01]. Any customer pilot on 1.2.x must upgrade within weeks.
- *Unexpected costs:*
  - Neptune Analytics starts at 16 m-NCU — about $350 per month before replicas, by inference [CLAIM-amazon-neptune-23];
  - Streams add I/O charges;
  - I/O-heavy workloads on Standard storage pay per request.
- *Overstated capabilities.* EOIP's manifest and adapter currently overstate Neptune support: Neptune Analytics listed with "Gremlin", and the adapter claiming RDF, SHACL and GQL exports [CLAIM-amazon-neptune-29][CLAIM-amazon-neptune-30]. This damages credibility in customer due diligence.

**Trade-offs**
- openCypher over HTTP vs Gremlin vs Bolt. HTTP is stateless and easy to sign. Bolt allows explicit multi-statement transactions but needs token refresh [CLAIM-amazon-neptune-17].
- Silo vs pool tenancy: cost against isolation.

**Open questions**
- Does Neptune Analytics support SPARQL? **NOT PUBLICLY VERIFIED**; only openCypher over N-Triples was found.
- Do the AWS Service Terms restrict publishing Neptune benchmark results? **UNVERIFIED**; a legal question.
- How does the native DFE engine compare with the TinkerPop fallback, step by step, for EOIP's query shapes? Measure with explain.
- Does `SET n += $map` behave the same on 1.5.0.0 when the parameter map contains list values? Covered by T-NEP-06.
- Do official AWS MCP servers for Neptune exist? Not researched here; cross-reference W22.

---

## Appendix A — Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | Active AWS service; engine 1.5.0.0 (2026-10-13); end-of-life policy; proprietary |
| D2 Problem and workloads | 2 | OLTP graph, analytics and RDF; not local-first |
| D3 Architecture decomposition | 4, 5.10 | Writer and replicas over a shared volume in three Availability Zones; separate Analytics service; endpoints |
| D4 Storage primitives and indexing | 5.1, 5.2 | Quad model; SPOG/POGS/GPSO indexes (plus optional OSGP); dictionary encoding |
| D5 Schema and semantic expressivity | 3, 5.1 | Schema-free; only ID uniqueness; multiple labels; set-valued properties; no meta-properties |
| D6 Query pipeline and optimisation | 5.3 | ANTLR-parsed Gremlin; DFE engine; join-order improvements; explain |
| D7 Reasoning and inference | 5.4 | None documented |
| D8 Transactions, concurrency, scale | 5.5, 5.6, 7 | MVCC snapshot reads; range locks; 60 s lock waits; one writer; 15 replicas |
| D9 Ingestion and federation | 3, 8 | S3 loader, offline loader, SPARQL `SERVICE` |
| D10 Identity and evidence | 5.10, INV-03 | Only ID uniqueness; EOIP must own identity and evidence |
| D11 Time and evolution | 5.8 | No time travel; Streams retain 1–90 days; snapshots and point-in-time restore |
| D12 Graph algorithms and ML | 3, 8 | Neptune Analytics algorithms; Neptune ML (SageMaker) |
| D13 Retrieval and agent integration | 3, 10, INV-06 | Neptune Analytics vector index; Bedrock GraphRAG mentioned in AWS announcements; no ACL-aware retrieval |
| D14 Natural-language querying | 10 | No native natural-language-to-query in Neptune found; Bedrock-based features sit outside the engine. N/A for the engine. |
| D15 Governance and authoring | 9, 13 | No schema or governance tooling; EOIP's gateway is required |
| D16 Human experience | 3 | graph-notebook, Graph Explorer, partner visualisation tools |
| D17 Developer experience | 9, 10 | SDKs; SigV4 friction; no local engine; LocalStack emulation (paid) |
| D18 Trust and security | 5.9, INV-02 | IAM SigV4; per-action query permissions; VPC; KMS; no password authentication |
| D19 Multi-tenancy and white-label | 5.9, INV-02 | One graph per cluster; silo or pool. White-label N/A (Neptune is a backend). |
| D20 Empirical economics | 7 | Pricing examples; NCU and m-NCU model; no independent benchmarks |
| D21 Commercial and licensing | 1, 10 | Proprietary service; usage-based billing; no OEM option |
| D22 Interoperability and lock-in | 3, 9, 11 | Standard languages with deviations; RDF isolated from property-graph data; neptune-export; lock-in through IAM, Streams and the Analytics APIs |
| D23 IP and prior art | 15 | No patents researched. Beyond general prior art on locking and indexing (recorded only), N/A for EOIP's planned inventions. |
| D24 Research quality | Appendix C | Mostly official documentation (confidence 0.8–0.9); vendor performance claims ≤ 0.3; adapter observed in code |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence CLAIM-ID | EOIP baseline (BL-ID + status) | Decision for EOIP | Priority |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-amazon-neptune-11 | BL-04 Implemented / never tested live | INTEGRATE | P1 |
| CAP-02 | native (isolated from property-graph data) | CLAIM-amazon-neptune-06, -26 | BL-06 Partial | INTEGRATE | P2 |
| CAP-04 | absent (managed only) | CLAIM-amazon-neptune-08 | — | REJECT (for one-node installs) | P3 |
| CAP-05 | partial (read replicas, no sharding) | CLAIM-amazon-neptune-14 | — | INTEGRATE | P2 |
| CAP-06 | native (S3 loader) | CLAIM-amazon-neptune-15 | BL-01 row upserts | INTEGRATE | P2 |
| CAP-07 | partial (optional OSGP; gap-lock contention) | CLAIM-amazon-neptune-11, -10 | — | BUILD (batching) | P2 |
| CAP-08 | absent (ID uniqueness only) | CLAIM-amazon-neptune-12 | BL-28 Implemented | BUILD | P1 |
| CAP-13 | native (with deviations) | CLAIM-amazon-neptune-03 | BL-04 | INTEGRATE | P1 |
| CAP-14 | native (with deviations) | CLAIM-amazon-neptune-04 | BL-04 | INTEGRATE | P1 |
| CAP-15 | native | CLAIM-amazon-neptune-06 | BL-04/06 | INTEGRATE | P2 |
| CAP-18 | partial (explain, query hints) | CLAIM-amazon-neptune-04, -34 | — | INTEGRATE | P3 |
| CAP-20 | absent | CLAIM-amazon-neptune-26 | BL-09 Partial | BUILD | P1 |
| CAP-21 | partial (SPARQL `SERVICE` only) | CLAIM-amazon-neptune-12 | BL-51 Partial | DEFER | P3 |
| CAP-22/23 | absent | CLAIM-amazon-neptune-06 | BL-30 Partial | REJECT waiting for upstream | P3 |
| CAP-26 | native (Streams) | CLAIM-amazon-neptune-14 | BL-52 Implemented (in-process) | INTEGRATE | P2 |
| CAP-30 | partial (ID uniqueness can be used) | CLAIM-amazon-neptune-12 | BL-34 Implemented | BUILD | P1 |
| CAP-34/36 | absent | CLAIM-amazon-neptune-14 | BL-37 Implemented | BUILD (keep) | P1 |
| CAP-44 | native (IAM SigV4) | CLAIM-amazon-neptune-07 | BL-04 — SigV4 Absent | BUILD | **P0** (for Neptune) |
| CAP-45 | partial (per-action permissions) | CLAIM-amazon-neptune-09 | BL-19 | INTEGRATE | P2 |
| CAP-46 | absent | CLAIM-amazon-neptune-12 | BL-18 Absent | BUILD | **P0** |
| CAP-47 | partial (one cluster per tenant) | CLAIM-amazon-neptune-12, -32 | BL-20 Partial | BUILD + INTEGRATE | **P0** |
| CAP-50 | absent | CLAIM-amazon-neptune-08 | design goal | REJECT Neptune for air-gapped installs | P0 (documentation) |
| CAP-53 | Neptune Analytics only | CLAIM-amazon-neptune-19 | BL-14 Partial | DEFER | P3 |
| CAP-54 | plugin (OpenSearch) | CLAIM-amazon-neptune-16 | BL-13 | DEFER | P3 |
| CAP-62 | Neptune Analytics only | CLAIM-amazon-neptune-18 | BL-43 Implemented | INTEGRATE (optional) | P2 |
| CAP-64 | plugin (Neptune ML / SageMaker) | CLAIM-amazon-neptune-26 | BL-44 Partial | REJECT as a dependency | P3 |
| CAP-74/76 | native | CLAIM-amazon-neptune-26 | BL-50 | INTEGRATE | P2 |
| CAP-75 | native (CloudWatch, slow-query log) | CLAIM-amazon-neptune-10 | BL-49 | INTEGRATE | P3 |
| CAP-77 | proprietary usage-based pricing | CLAIM-amazon-neptune-23 | BL-22 | — (recorded) | P3 |
| CAP-78 | — | — | BL-07 Partial | BUILD | P1 |

## Appendix C — Evidence records

All sources were accessed on 2026-10-18. "Publication date" is the date shown on the page; "n/d" means none is shown (AWS documentation pages carry no date).

| CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication / access | confidence + rationale | contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-amazon-neptune-01 | Neptune DB engines | 1.5.0.0 active, released 2026-10-13; 1.4.8.1 released 2026-10-06; 1.4.8.0 released 2026-07-27 (EOL 2027-10-27); 1.2.x EOL 2026-12-04; 1.3.0.0–1.4.6.1 EOL 2027-03-06 | Officially documented | Engine releases for Amazon Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases.html | n/d / 2026-10-18 | 0.9 — official table | none |
| CLAIM-amazon-neptune-02 | 1.5.0.0 | Gremlin on TinkerPop 3.8.x (earliest 3.8.0, latest 3.8.1); openCypher `Neptune-9.0.20190305-1.1`; SPARQL 1.1; fast offline bulk loader; online index rebuild; semantic step changes "may not surface as errors"; MERGE now rejects null values | Officially documented | Amazon Neptune Engine version 1.5.0.0 — https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases-1.5.0.0.html | 2026-10-13 / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-03 | Neptune Gremlin | ANTLR grammar: no variables, parameterization or bindings; no Groovy; String IDs only; no meta-properties; no null, Map or UUID values; set cardinality by default, List unsupported; no lambdas; `io()` read-only; sessions limited to 10 min; no `tx.commit` in text submissions; multiple labels with `::` | Officially documented | Gremlin standards compliance in Amazon Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-gremlin-differences.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-04 | Neptune openCypher | Based on Cypher 9; no `shortestPath`/`allShortestPaths`, `MANDATORY MATCH`, `CALL…YIELD` or UDFs; mutating `UNION` unsupported; non-constant `SKIP`/`LIMIT` unsupported; variable-length-path property filters must be constants; custom IDs allowed in `MATCH`/`CREATE`/`MERGE`; IDs are strings; a multi-valued property returns an arbitrary value; extended datetime support on 1.3.2.0+ (lab mode) and in Neptune Analytics | Officially documented | openCypher specification compliance in Amazon Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/feature-opencypher-compliance.html | n/d / 2026-10-18 | 0.9 | 1.5.0.0 adds all/any/none/single (CLAIM-34) |
| CLAIM-amazon-neptune-05 | Neptune openCypher data model | Arrays loaded into Neptune become multi-valued properties; AWS advises against inserting array values; `SET` accepts only simple literals | Officially documented (read through a search summary) | openCypher data model — https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-opencypher-data-model.html ; exceptions page — https://docs.amazonaws.cn/en_us/neptune/latest/userguide/access-graph-opencypher-exceptions.html | n/d / 2026-10-18 | 0.65 — pages not fetched in full | none |
| CLAIM-amazon-neptune-06 | Neptune SPARQL | SPARQL 1.1 Query and Update; default graph = union of all named graphs; fallback named graph `http://aws.amazon.com/neptune/vocab/v01/DefaultNamedGraph`; dateTime stored in UTC (offset lost); numbers limited to 64 bits; no entailment regime listed | Officially documented | SPARQL standards compliance in Amazon Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/feature-sparql-compliance.html | n/d / 2026-10-18 | 0.85; the absence of reasoning is inferred from its omission (0.6) | none |
| CLAIM-amazon-neptune-07 | Neptune IAM | With IAM database authentication enabled, every HTTP request must be SigV4-signed; service name `neptune-db`; the boto3 `neptunedata` client signs Gremlin and openCypher but does not support SPARQL | Officially documented | Connecting … using IAM authentication — https://docs.aws.amazon.com/neptune/latest/userguide/iam-auth-connecting.html ; … with Python — https://docs.aws.amazon.com/neptune/latest/userguide/iam-auth-connecting-python.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-08 | Neptune limits | VPC-only, no access from outside the VPC; TLS 1.2 only; HTTP payload up to 150 MB; property up to 55 MB; volume up to 128 TiB; "does not support user name/password–based access control"; loader not ACID; at most 64 queued load jobs | Officially documented | Amazon Neptune Limits — https://docs.aws.amazon.com/neptune/latest/userguide/limits.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-09 | Neptune IAM data access | Actions ReadDataViaQuery, WriteDataViaQuery and DeleteDataViaQuery; the required set is computed from every action a query could perform; openCypher `SET` always needs Delete | Officially documented | Creating custom IAM policy statements to access data — https://docs.aws.amazon.com/neptune/latest/userguide/iam-data-access-policies.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-10 | Neptune transactions | Read-only queries: snapshot isolation via MVCC; mutations: READ COMMITTED plus range/gap locks on SPOG, POGS and GPSO; lock waits up to 60 s; deadlocks rolled back immediately; 3–4 % false conflicts under high load; lock-wait counters from 1.4.5.0 | Officially documented | Transaction Isolation Levels in Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/transactions-neptune.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-11 | Neptune indexing | Default indexes SPOG, POGS and GPSO; OSGP only through Lab Mode on an empty cluster; inserts up to 23 % slower and storage up to 20 % larger with OSGP; label-less `in()`/`both()` inefficient without OSGP | Officially documented | How Statements Are Indexed in Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/feature-overview-storage-indexing.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-12 | Neptune compared with Neo4j | One graph per cluster (multi-tenancy through separate clusters or a tenantId property); only ID uniqueness as a constraint; no custom procedures or APOC; no native geospatial support; finer access control left to the application; SPARQL `SERVICE` federation; one writer plus 15 replicas, replicas eventually consistent, usually < 100 ms behind; GraphQL through AppSync | Officially documented | Neptune compatibility with Neo4j — https://docs.aws.amazon.com/neptune/latest/userguide/migration-compatibility.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-13 | Neptune Serverless | 1 NCU = 2 GiB RAM plus vCPU; minimum 1.0 and maximum 128 NCU (256 GB); the maximum setting must be at least 2.5 NCU; engine 1.2.0.1 or later; lookup cache not supported; only compute scales | Officially documented | Amazon Neptune Serverless — https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless.html ; Capacity scaling — https://docs.aws.amazon.com/neptune/latest/userguide/neptune-serverless-capacity-scaling.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-14 | Neptune Streams | Change log written synchronously in the same transaction; strictly ordered, no duplicates, complete; 7-day retention by default, configurable to 1–90 days from 1.2.0.0; "Neptune is single-sharded by design"; no Lambda trigger; slightly slower writes | Officially documented | Capturing graph changes in real time using Neptune streams — https://docs.aws.amazon.com/neptune/latest/userguide/streams.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-15 | Neptune loader | Loads from S3 using an IAM role and an S3 VPC endpoint; formats csv (Gremlin), opencypher, ntriples, nquads, rdfxml and turtle; gzip and bzip2 compression | Officially documented | Using the Amazon Neptune bulk loader — https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load.html ; Load Data Formats — https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-16 | Neptune full-text search | Full-text search for Gremlin and SPARQL through the Amazon OpenSearch integration; blank nodes are not replicated | Officially documented | Full text search in Amazon Neptune using Amazon OpenSearch Service — https://docs.aws.amazon.com/neptune/latest/userguide/full-text-search.html | n/d / 2026-10-18 | 0.85 | none |
| CLAIM-amazon-neptune-17 | Neptune Bolt | Bolt through Neo4j drivers, TCP only, Bolt versions 1–4.0, at most 1,000 connections; IAM through signed headers sent as JSON in the basic-auth credentials; SigV4 signatures expire after about 5 min; known driver re-authentication issues | Officially documented | Using the Bolt protocol to make openCypher queries to Neptune — https://docs.aws.amazon.com/neptune/latest/userguide/access-graph-opencypher-bolt.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-18 | Neptune Analytics | In-memory analytics engine; openCypher; loads from S3 or Neptune Database; more than 25 algorithms (BFS, SSSP, Top-K SSSP, ST-SSSP, EgoNet, Degree, PageRank, Closeness, Eigenvector, Common/Total Neighbors, Jaccard, Overlap, WCC, SCC, Label Propagation, Louvain, Leiden, vector Distance/Top-K, schema procedures) through `CALL neptune.algo.*`; signing service `neptune-graph` | Officially documented | What is Neptune Analytics — https://docs.aws.amazon.com/neptune-analytics/latest/userguide/what-is-neptune-analytics.html ; Algorithms — https://docs.aws.amazon.com/neptune-analytics/latest/userguide/algorithms.html | n/d / 2026-10-18 | 0.9 | EOIP manifest claims Gremlin (CLAIM-30) |
| CLAIM-amazon-neptune-19 | Neptune Analytics vector search | One vector index per graph, created with the graph, dimension 1–65,535; HNSW; vector updates neither atomic nor isolated; vectors cannot be loaded from Neptune Database or a snapshot | Officially documented | Vector indexing in Neptune Analytics — https://docs.aws.amazon.com/neptune-analytics/latest/userguide/vector-index.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-20 | Neptune Analytics CreateGraph | provisionedMemory 16–24,576 m-NCU; publicConnectivity optional, and "All access to graphs is IAM authenticated"; replicaCount 0–2 (default 1); KMS key | Officially documented | CreateGraph API — https://docs.aws.amazon.com/neptune-analytics/latest/apiref/API_CreateGraph.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-21 | Neptune Analytics RDF | Imports N-Triples; openCypher over RDF (announced 2024-08); blank nodes converted to IRIs; no SPARQL endpoint found | Officially documented (absence of SPARQL: Unverified) | Using RDF data — https://docs.aws.amazon.com/neptune-analytics/latest/userguide/using-rdf-data.html ; What's New 2024-08 — https://aws.amazon.com/about-aws/whats-new/2024/08/amazon-neptune-analytics-opencypher-queries-graphs/ | 2024-08-13 / 2026-10-18 | 0.85 (absence of SPARQL: 0.3) | none |
| CLAIM-amazon-neptune-22 | Neptune Analytics loading | Bulk import only into an empty graph (CreateGraphUsingImportTask / StartImportTask); incremental batch loading with `neptune.load()`; loading the same edge file twice duplicates edges | Officially documented | Loading data into a Neptune Analytics graph — https://docs.aws.amazon.com/neptune-analytics/latest/userguide/loading-data.html | n/d / 2026-10-18 | 0.85 | none |
| CLAIM-amazon-neptune-23 | Pricing | Example: db.r5.large $0.348/h (us-east-1); storage $0.10/GB-month; I/O $0.20 per million; I/O-Optimized storage $0.225/GB-month; Neptune Analytics m-NCU = 1 GB for one hour, with an example of $7.68/h for 256 GB; a paused graph costs 10 %; 30-day free trial | Officially documented (per-m-NCU rate inferred) | Amazon Neptune pricing — https://aws.amazon.com/neptune/pricing/ | n/d / 2026-10-18 | 0.75 — regional examples; m-NCU rate inferred | none |
| CLAIM-amazon-neptune-24 | graph-notebook 5.3.0 | Latest PyPI release 5.3.0, uploaded 2026-08-04; Apache License 2.0 | Officially documented (package registry) | PyPI graph-notebook — https://pypi.org/project/graph-notebook/ | 2026-08-04 / 2026-10-18 | 0.85 | GitHub API not reachable (rate limit) |
| CLAIM-amazon-neptune-25 | LocalStack Neptune | Available from the "Ultimate" plan; based on Gremlin Server 3.7.2; IAM enforcement for Gremlin; no persistence; serializer issues; SPARQL and openCypher not described | Third-party report (the emulator vendor's documentation) | LocalStack Neptune — https://docs.localstack.cloud/aws/services/neptune/ | n/d / 2026-10-18 | 0.7 | none |
| CLAIM-amazon-neptune-26 | Neptune FAQ | A cluster can store both property-graph and RDF data, but property-graph queries cannot run over RDF data and vice versa; one writer plus up to 15 replicas; the volume spans three Availability Zones and survives the loss of two copies; Global Database; Neptune ML through SageMaker | Officially documented | Amazon Neptune FAQs — https://aws.amazon.com/neptune/faqs/ | n/d / 2026-10-18 | 0.85 | none |
| CLAIM-amazon-neptune-27 | Neptune end-of-life policy | Minor versions available for at least 6 months, major versions for at least 12; 3 months' notice; automatic upgrade at end of life | Officially documented | Engine releases (end-of-life planning) — https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-28 | Neptune WebSocket | Up to 32,768 concurrent WebSockets on large and serverless instances; idle timeout 20–25 min; WebSockets using IAM closed after about 10 days | Officially documented | Amazon Neptune Limits — https://docs.aws.amazon.com/neptune/latest/userguide/limits.html | n/d / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-29 | EOIP `graph/neptune.py` at ad9937b | httpx Basic auth or none (lines 72–79); no SigV4 or botocore anywhere in `packages/eoip`; `~id` not used; `upsert_edge` takes 3 requests; `edges_from`/`edges_to` filter labels after `LIMIT`; `bulk_load` upserts row by row; no retries; `capabilities()` claims rdf, shacl, gql and pgql exports; the factory passes only username, password and verify_tls (`graph/backends.py:212-224`) | Observed in source code | `packages/eoip/graph/neptune.py`, `packages/eoip/graph/backends.py`, `config/graph-store.yaml` | 2026-10-18 / 2026-10-18 | 0.95 — read directly | none |
| CLAIM-amazon-neptune-30 | EOIP `adapters/manifests.py:428-435` | The Neptune Analytics manifest lists native surfaces "openCypher" and "Gremlin (serverless analytics)", with adapter_status "manifest-only" | Observed in source code | `packages/eoip/adapters/manifests.py` | 2026-10-18 / 2026-10-18 | 0.95 | contradicts CLAIM-18 |
| CLAIM-amazon-neptune-31 | EOIP `graph/database_adapters.py:323` | `translate_query` sends AMAZON_NEPTUNE (and AZURE_COSMOS_DB) queries through a regex Cypher-to-Gremlin translator | Observed in source code | `packages/eoip/graph/database_adapters.py` | 2026-10-18 / 2026-10-18 | 0.95 | Neptune supports openCypher natively (CLAIM-04) |
| CLAIM-amazon-neptune-32 | Neptune multi-tenancy guidance | AWS describes silo (one cluster per tenant), pool (logical partitioning) and hybrid models; Orca Security's pool model uses Gremlin PartitionStrategy | Officially documented (summary only) | Multi-tenancy guidance for ISVs running Amazon Neptune databases — https://docs.aws.amazon.com/prescriptive-guidance/latest/multi-tenancy-amazon-neptune/introduction.html ; AWS Database Blog — https://aws.amazon.com/blogs/database/build-multi-tenant-architectures-on-amazon-neptune | 2024-08 / 2026-10-18 | 0.55 — pages not opened in full | none |
| CLAIM-amazon-neptune-33 | Neptune regions | Available in 32 regions, including GovCloud (US-West and US-East) and China (Beijing and Ningxia) | Officially documented | Amazon Neptune Limits — https://docs.aws.amazon.com/neptune/latest/userguide/limits.html | n/d / 2026-10-18 | 0.85 | none |
| CLAIM-amazon-neptune-34 | 1.5.0.0 | Native `all()`, `any()`, `none()` and `single()`; regex predicates on DFE; better join ordering across `WITH`/`BIND` stages for openCypher and SPARQL; more Gremlin steps on DFE | Officially documented | Engine version 1.5.0.0 — https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases-1.5.0.0.html | 2026-10-13 / 2026-10-18 | 0.9 | none |
| CLAIM-amazon-neptune-35 | Neptune Analytics regions | Seven regions added on 2026-01-22 and seven more on 2026-02-09; the announcements' boilerplate mentions managed GraphRAG with Bedrock Knowledge Bases and an integration with the Strands Agents SDK | Officially documented (announcement) | What's New — https://aws.amazon.com/about-aws/whats-new/2026/01/amazon-neptune-analytics-generally-available-additional-regions ; https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-neptune-analytics-in-seven-additional-regions | 2026-01 and 2026-02 / 2026-10-18 | 0.7 — read through a search summary | none |
| CLAIM-amazon-neptune-36 | Vendor performance claims | Neptune Database can "scale to 100,000 queries per second"; Neptune Analytics handles "tens of billions of relationships" and "thousands of analytic queries per second"; no workload or hardware stated | Unverified (vendor claim) | When to use Neptune Analytics and when to use Neptune Database — https://docs.aws.amazon.com/neptune-analytics/latest/userguide/neptune-analytics-vs-neptune-database.html | n/d / 2026-10-18 | 0.3 — marketing figures without methodology | none found |

## Appendix D — Assumptions

1. "Amazon Neptune (RDF/SPARQL mode)" in C02 means the same Neptune Database engine. It gets no separate registry entry; W09 should cross-reference this file.
2. EOIP's Neptune support targets engines 1.4.8.x and 1.5.0.0. 1.5.0.0 takes several days to reach every region, so some customers may briefly see 1.4.8.1 as the newest version.
3. The Neptune Analytics price per m-NCU-hour is inferred from the pricing page's example ($7.68 per hour for 256 GB). Prices differ by region.
4. Statements about Neptune's storage internals beyond the documentation (for example, that the volume is log-structured like Aurora's) are hypotheses and are labelled as such.
5. The adapter assessment reflects HEAD `ad9937b` plus the uncommitted working tree on 2026-10-18. `graph/neptune.py` is not among the modified files, so it is assumed identical to HEAD.
6. No AWS account was used and no live Neptune test was run. Every test in §14 is PROPOSED.
7. Neo4j driver licensing is not re-researched here; see T-C01-neo4j by W02.
