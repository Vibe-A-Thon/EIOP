# C01 — Neo4j (Community, Enterprise, Infinigraph, GDS, Bloom, NeoDash, Aura, NVL)

| Field | Value |
|---|---|
| Registry ID | T-C01-neo4j |
| Tier | A. Neo4j is a required EOIP backend (adapter `packages/eoip/graph/neo4j.py`, BL-03) and the market-reference labelled property graph (LPG). |
| Versions examined | Neo4j **2026.09.0** (release notes 21 Sep 2026; tag 16 Sep 2026). **5.26.32 LTS** (tag 8 Oct 2026; this is what EOIP's `neo4j:5-community` resolves to). GDS 2026.09.0. Bloom 2.36.0 (bundled) and 2.37.0. APOC 2026.09.0. n10s 2025.06.1. NVL `@neo4j-nvl/base` 2.0.0 (15 Sep 2026). Python driver 6.4.1 (15 Oct 2026). Enterprise Studio (24 Jun 2026). |
| Verified on | 2026-10-18 |
| Worker | W02 |

**Cross-references:**
- Neo4j GraphRAG Python package: `C08-neo4j-graphrag.md` (W19).
- NVL as a library: Tier C `T-C16-neo4j-nvl` (W29).
- GDS as an algorithm or ML library: W33 (C12) and W24 (C11).

---

## 1. Identity, current status, tier, and sources

**Owner and status.**
- Owner: Neo4j, Inc. The code is "developed and owned by Neo4j Sweden AB" [CLAIM-neo4j-04]. Site: https://neo4j.com. Source: https://github.com/neo4j/neo4j.
- **Active.** Monthly calendar-versioned releases (CalVer) since 2025.01. **Each CalVer minor is supported only until the next one ships** [CLAIM-neo4j-02].
- **5.26 is the long-term support (LTS) line, supported to 6 Jun 2028** [CLAIM-neo4j-02][CLAIM-neo4j-03].
- The next LTS ("2026.LTS") is planned for Nov 2026. It is the last version that can read the high_limit and standard store formats [CLAIM-neo4j-18][CLAIM-neo4j-19].
- No 2026.10 release existed on the access date [CLAIM-neo4j-01].

**Traps resolved.**
- `5-community` means the LTS line, not the current release.
- GDS switched from 2.x to CalVer at 2026.03 (2.27 shipped with Neo4j 2026.02) [CLAIM-neo4j-25].
- Bloom still uses semantic versions [CLAIM-neo4j-26].
- **NeoDash Labs is unmaintained; dashboards are now commercial** [CLAIM-neo4j-27].

| Member | Licence / terms | Status |
|---|---|---|
| Community Edition (CE): single instance | GPLv3. A signed commercial agreement supersedes it [CLAIM-neo4j-04]. | active |
| Enterprise Edition (EE): CE plus closed modules | Commercial (Software Agreement, evaluation agreement) [CLAIM-neo4j-04][CLAIM-neo4j-05] | active |
| Infinigraph: EE plus sharded property databases (2025.12) and GDS | Separate subscription; not on Aura [CLAIM-neo4j-06] | active |
| GDS | OpenGDS sources are GPLv3. Neo4j's build adds closed code. EE needs a licence file [CLAIM-neo4j-24][CLAIM-neo4j-25]. | active |
| Bloom | Server plugin needs an activation key; the hosted web app is EE-only [CLAIM-neo4j-26] | active |
| NeoDash Labs | Apache-2.0; "no longer maintained" [CLAIM-neo4j-27] | unmaintained |
| NeoDash commercial / Dashboards | Part of an Enterprise agreement [CLAIM-neo4j-27] | active |
| Enterprise Studio (Query, Bloom, Dashboards; air-gap; SSO) | Commercial [CLAIM-neo4j-28] | active |
| Aura (reference only) | SaaS with published prices [CLAIM-neo4j-29] | cloud-only |
| NVL | "SEE LICENSE IN 'LICENSE.txt'"; reported as Neo4j-only [CLAIM-neo4j-33] | needs legal review |
| n10s (RDF/OWL/SHACL) | Apache-2.0; Labs, "not part of Neo4j's supported product lineup" [CLAIM-neo4j-31] | last release 2025.06.1 |
| APOC Core | Apache-2.0 [CLAIM-neo4j-34] | bundled |

**Sources (Appendix C).** 17 sources, all accessed 2026-10-18:
- release notes
- endoflife.date
- GitHub tags and licences
- Operations Manual
- Cypher Manual
- HTTP and Query API manuals
- GDS documentation and README
- Bloom, NeoDash and Enterprise Studio pages
- pricing page
- n10s documentation
- npm and PyPI

## 2. Primary problem, target workloads, concrete example workflows

Neo4j is a native transactional LPG database. Its core value is relationship traversal written in Cypher (now Cypher 25, aligned with GQL), plus in-database analytics (GDS), vector and full-text search, and visual tools.

- **Positioning:** CE is for "learning, do-it-yourself projects, and small workgroups"; EE is for production [CLAIM-neo4j-05].
- **Segments:** fraud, identity, IT dependency and CMDB graphs, supply chain, knowledge graphs and GraphRAG.

**EOIP journeys:**
- **J9 blast radius.** One variable-length Cypher pattern of up to 6 hops, planned by Neo4j's optimiser. EOIP today runs a Python breadth-first search (BL-01).
- **J1 change impact.** Path queries plus GDS centrality.
- **J5 permissions.** EE privileges hide restricted data [CLAIM-neo4j-14]. This is defence in depth only; it does not replace BL-18.
- **J13 tenancy.** One database per tenant works on EE only; CE has "exactly one standard database" [CLAIM-neo4j-13].
- **J14 portability.** Neo4j is the reference for Cypher and GQL.

## 3. Feature inventory

Legend:
- **P**: both CE and EE
- **EE**: Enterprise only
- **INF**: Infinigraph only
- **OPT**: separate plugin
- **LABS**: unsupported Labs project
- **A**: absent
- **DEP**: deprecated

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Storage | Aligned format (2^35 nodes and 2^35 relationships) | P (CE default) | [CLAIM-neo4j-18] |
| Storage | Block format (128-byte blocks, 2^48 nodes); native `VECTOR` type | EE (default since 5.22) | [CLAIM-neo4j-18][CLAIM-neo4j-09] |
| Storage | Standard and high_limit formats | DEP 5.23; removed after the Nov-2026 LTS | [CLAIM-neo4j-18] |
| Storage | Sharded property databases | INF | [CLAIM-neo4j-06] |
| Query | Cypher 5 (frozen) and Cypher 25; cost-based optimiser; EXPLAIN/PROFILE; slotted runtime | P | [CLAIM-neo4j-05][CLAIM-neo4j-07] |
| Query | GQL (ISO/IEC 39075:2024) | Partial: "majority of mandatory features"; 5 areas missing | [CLAIM-neo4j-08] |
| Query | Pipelined and parallel runtimes; composite databases | EE | [CLAIM-neo4j-05] |
| Query | `SEARCH`: vector (2026.01) and full-text (2026.09) | P (Cypher 25) | [CLAIM-neo4j-09][CLAIM-neo4j-10] |
| Index | Range, text, point, composite and full-text (Lucene) | P | [CLAIM-neo4j-05] |
| Index | Vector index (HNSW, ≤4096 dimensions, cosine/euclidean, scalar/binary quantisation, filter properties) | P (CE: list properties) | [CLAIM-neo4j-09] |
| Schema | Uniqueness constraints | P | [CLAIM-neo4j-22] |
| Schema | Existence, type and key constraints; GRAPH TYPE (GA 2026.06, Cypher 25, open semantics) | EE | [CLAIM-neo4j-22][CLAIM-neo4j-23] |
| Semantics | RDF import/export, OWL/SKOS import, SHACL, query-time hierarchy inference | LABS (n10s) | [CLAIM-neo4j-31][CLAIM-neo4j-32] |
| Semantics | Native OWL, RDFS or Datalog reasoner | A | [CLAIM-neo4j-05][CLAIM-neo4j-32] |
| Transactions | ACID, read committed, deadlock detection | P | [CLAIM-neo4j-20] |
| Transactions | CDC | EE | [CLAIM-neo4j-05] |
| Security | Authentication | P | [CLAIM-neo4j-05] |
| Security | RBAC; label, type, property and value privileges; LDAP; Kerberos | EE | [CLAIM-neo4j-14][CLAIM-neo4j-15] |
| Tenancy | Multiple databases and aliases | EE | [CLAIM-neo4j-13] |
| HA | Autonomous clustering (Raft; ≤11 primaries; ≤20 secondaries) | EE | [CLAIM-neo4j-16] |
| Ops | Offline dump and load | P | [CLAIM-neo4j-05] |
| Ops | Online and differential backup; point-in-time recovery; Prometheus; Ops Manager | EE | [CLAIM-neo4j-17][CLAIM-neo4j-05] |
| Ops | Usage report, on by default | P; can be disabled | [CLAIM-neo4j-30] |
| API | Bolt and drivers (.NET, Go, Java, JavaScript, Python) | P | [CLAIM-neo4j-34] |
| API | HTTP transactional API `/db/{db}/tx[/commit]` | **DEP 5.26**; not on Aura | [CLAIM-neo4j-11] |
| API | Query API `/db/{db}/query/v2` | P since 5.19; on by default since 5.25 | [CLAIM-neo4j-12] |
| AI | GenAI plugin | P | [CLAIM-neo4j-19] |
| Analytics | GDS CE (all algorithms, 4 cores, 3 models) / GDS EE (Arrow, model persistence, optimised graph) | OPT / EE licence | [CLAIM-neo4j-24] |
| UI | Browser (P). Bloom and Dashboards (commercial). NeoDash Labs (unmaintained). | mixed | [CLAIM-neo4j-26][CLAIM-neo4j-27][CLAIM-neo4j-28] |

## 4. Text-based architecture diagram

```
 CONTROL PLANE                                  DATA PLANE
 system DB: users/roles/privileges/topology/    Clients: Bolt :7687 | Query API (+legacy HTTP) :7474/7473
   aliases/graph types (Raft-replicated)        Browser | Bloom | Dashboards | cypher-shell
 Usage report → Neo4j / 24h (default ON) ─X         │ auth: native | LDAP/SSO [EE]
 Ops Manager / Fleet Mgmt [EE]                      ▼
 Cluster [EE]: servers PRIMARY|SECONDARY|NONE   Cypher parse → AST → semantic (CYPHER 5|25) → cost-based
   per DB ≤11 primaries (Raft, 1 writer),         plan → runtime slotted [CE] | pipelined/parallel [EE]
   ≤20 async secondaries, bookmarks               → privilege filter [EE] → kernel (heap tx state, locks)
 Infinigraph [INF]: graph shard (topology,          ▼
   Raft) + N hashed property shards             Store/DB: aligned [CE/EE] | block [EE]; page cache;
 Plugins in-JVM: APOC, GDS (heap catalog),        GBPTree + Lucene FT/HNSW; WAL → backup/PITR [EE] | dump
   GenAI, n10s (Labs), Bloom plugin
 EOIP: GraphStore → httpx → POST /db/neo4j/tx/commit (deprecated); 1 stmt/request; 1 DB; no tenant
```

## 5. Under-the-hood reconstruction

**Evidence base:**
- CE source is public at tag `2026.09.0`. Modules include `community/record-storage-engine`, `kernel`, `cypher`, `native-index`, `lucene-index`, `lock`, `wal`, `bolt`, `server`, `fabric` and `genai-plugin` [CLAIM-neo4j-42].
- **Block format, clustering, RBAC and the parallel runtime are closed source.** Statements about them below are documented behaviour or marked as hypotheses.
- This is a blueprint of behaviour, not a recommendation to copy GPL code.

| Layer | Verified behaviour | EOIP blueprint |
|---|---|---|
| Data model | Nodes have 0..n labels and properties. A relationship has one type, a direction and properties. One graph per database [CLAIM-neo4j-14]. No hyperedges or reification. GQL baseline is GG01, "open graph type" [CLAIM-neo4j-08]. | Model claims as nodes. Put `edge_key`, validity and provenance on relationships. |
| Storage | Aligned format uses "linked, list-like structures"; per-field layout is a *hypothesis* from public design history. Block format (EE): 128 B = 2×64 B records (labels and properties; relationships), fitting about 10 labels, 6–7 properties and 5 relationships. Overflow goes to dynamic stores (8,192 B and 2,047 B). Values over ~31 B go to a big-values store. Dense nodes use a tree sorted by type and direction [CLAIM-neo4j-18]. | Same principle as HugeGraph's RocksDB adjacency co-location: fewer pages per hop. Do not build a store. |
| Indexes | GBPTree for range, point, text and token. Lucene for full-text and HNSW (m 1–512, default 16; ef_construction 1–3200, default 100). One vector index per label and property pair. **Changes in the same transaction are not visible to the index** [CLAIM-neo4j-09]. | `VectorIndexPort` flags `{in_tx_visibility, filter_props, max_dims, quantisation}`. Neo4j: `CREATE VECTOR INDEX … WITH [tenant, acl_hash]` + `SEARCH`. |
| Query | Cost-based optimiser and 3 runtimes [CLAIM-neo4j-05]. Version chosen per query or database. New features go only to Cypher 25; Cypher 5 will be retired [CLAIM-neo4j-07]. Peer-reviewed formal semantics [CLAIM-neo4j-43]. Missing GQL: §7.1–7.3 sessions, §8.1–8.4 transactions, §11.1 graph expressions, §17.1 schema reference, §21.3 tokens [CLAIM-neo4j-08]. | Compile `QueryPlan` to Cypher 25 when supported (sketch below). |
| Reasoning | None native. (a) GRAPH TYPE label implication `(c:Crew => :Person)`, enforced on write (EE) [CLAIM-neo4j-23]. (b) n10s query-time `nodesLabelled`, `hasLabel`, `nodesInCategory`, `inCategory`, `getRels` over subClassOf and subPropertyOf hierarchies; no materialisation [CLAIM-neo4j-32]. (c) n10s SHACL in batch, node-set or trigger mode, covering "a significant portion … but not all" [CLAIM-neo4j-31]. | Reasoning lives in the EOIP layer with provenance. Push only enforceable rules down. |
| Transactions | Read committed. Lost updates possible. DeadlockDetected means the client retries. MERGE "takes locks out of order" [CLAIM-neo4j-20]. Transaction state lives in heap. Default limit 1000 concurrent transactions. Timeout defaults to 0, meaning off [CLAIM-neo4j-21]. | Back every MERGE key with a constraint. Batch with UNWIND. Retry. Enforce budgets on the server. |
| Partitioning | EE: one Raft group per database, async secondaries, bookmarks [CLAIM-neo4j-16]. A transaction cannot span databases [CLAIM-neo4j-13]. Infinigraph shards properties, not topology [CLAIM-neo4j-06]. | One database per tenant on EE; pooled tenants on CE. |
| Caching | Off-heap page cache, fully reserved since 2026.09 [CLAIM-neo4j-19]. GDS graphs live in heap [CLAIM-neo4j-24]. | Size page cache, heap and GDS together. |
| Versioning | No native as-of queries. History exists only through WAL-based PITR (`--restore-until` timestamp or txId) and CDC, both EE [CLAIM-neo4j-17]. | EOIP keeps bitemporality (BL-37). |
| Security | Database ACCESS, then TRAVERSE, READ and MATCH privileges by label, type and property. Access needs GRANT with no DENY; restricted reads are invisible [CLAIM-neo4j-14]. **Value-based rules: one property per rule, "significant performance overhead", and DENY "fails open"** [CLAIM-neo4j-15]. | Label-based ACL partitions as defence in depth. |

**Pushdown sketch** (EOIP pseudocode). The hop bound is a validated integer literal, because Cypher does not accept a parameter there:
```
if caps.pushdown("var_length_path"):
  run(f"CYPHER 25 MATCH p=(s:EOIPEntity {{canonical_id:$k}})-[:USES|DEPLOYS*1..{h}]->(x) "
      "WHERE all(n IN nodes(p) WHERE n.tenant=$t AND n.acl_hash IN $acl) RETURN p LIMIT $lim",
      params, max_execution_time=plan.budget)
else: python_bfs(store.neighbours, plan)          # BL-01
```

## 6. Functional and non-functional requirements inferred from verified behaviour

| ID | Requirement | Evidence |
|---|---|---|
| FR-N1 | The adapter uses a supported API (Query API or Bolt) and runs on both 5.26 LTS and the current CalVer release | [CLAIM-neo4j-11][CLAIM-neo4j-12] |
| FR-N2 | Capability discovery reports the edition and gates multi-database, constraints, GRAPH TYPE, RBAC and backup features | [CLAIM-neo4j-05][CLAIM-neo4j-23] |
| FR-N3 | Writes are batched with UNWIND; every MERGE key is constraint-backed | [CLAIM-neo4j-20][CLAIM-neo4j-22] |
| FR-N4 | `edge_key` lookups are typed and indexed | [CLAIM-neo4j-37] |
| FR-N5 | The portable schema compiles to GRAPH TYPE or constraints; the EOIP gate stays authoritative | [CLAIM-neo4j-23] |
| FR-N6 | Vector search never assumes in-transaction freshness; tenant and ACL are filter properties | [CLAIM-neo4j-09] |
| NFR-N1 | The air-gap profile sets `dbms.usage_report.enabled=false` and has no Aura dependency | [CLAIM-neo4j-30] |
| NFR-N2 | Production pins the LTS line | [CLAIM-neo4j-02] |
| NFR-N3 | Time budgets are enforced by the server (`maxExecutionTime` or the transaction timeout) | [CLAIM-neo4j-12][CLAIM-neo4j-21] |

## 7. Performance and resource model

**Benchmarks.**
- None run in this programme.
- **No independent, audited benchmark (for example LDBC) of Neo4j 2026.x was found.**
- Vendor claim: rescored binary quantisation gives "about a 5X reduction in latency and 5X increase in query throughput". No dataset or hardware is given: **Unverified** [CLAIM-neo4j-10].
- The README's "orders of magnitude" over relational databases is unverified marketing.

**Resource model (documented behaviour):**
- Memory is page cache (off-heap) plus heap. Heap holds transaction state, queries and GDS projections [CLAIM-neo4j-21][CLAIM-neo4j-24].
- Large transactions must be split [CLAIM-neo4j-21].
- **GDS CE is capped at 4 cores** [CLAIM-neo4j-24].
- Block format reduces page reads; dense-node trees mitigate supernodes [CLAIM-neo4j-18].
- There is one writer per database; more primaries mean more Raft round trips [CLAIM-neo4j-16].
- Reads scale to 20 secondaries.
- More than ~34 billion nodes requires block format (EE) [CLAIM-neo4j-18].

**Failure modes:**
- MERGE deadlocks [CLAIM-neo4j-20]
- overhead from value-based access rules [CLAIM-neo4j-15]
- vector index not seeing changes within the writing transaction [CLAIM-neo4j-09]
- the 2026.08.0 query regression, since patched [CLAIM-neo4j-01]

**EOIP adapter cost (observed in code):**
- **3 HTTP calls per edge.**
- One request per entity in `bulk_load`; `batch_size` is unused.
- Full relationship scan in `find_edge_by_key`.
- So throughput is roughly bounded by 3 × round-trip time per edge (inference, not measured) [CLAIM-neo4j-37][CLAIM-neo4j-38].

## 8. Strengths and use-case-specific advantages

| # | Strength | How EOIP matches or exceeds it |
|---|---|---|
| S1 | Cypher 25/GQL with a cost-based optimiser and PROFILE [CLAIM-neo4j-05][CLAIM-neo4j-07] | Push `QueryPlan` down; exceed it with ACL and tenant predicates on every backend |
| S2 | Vector, full-text and graph in one query [CLAIM-neo4j-09][CLAIM-neo4j-10] | Neo4j implementation of the retrieval port; RRF (BL-15) elsewhere |
| S3 | GRAPH TYPE enforced schema [CLAIM-neo4j-23] | Compile EOIP's manifest to it |
| S4 | GDS library [CLAIM-neo4j-24] | Optional pushdown; BL-43 as fallback |
| S5 | EE fine-grained security [CLAIM-neo4j-14][CLAIM-neo4j-15] | Defence in depth beneath EOIP's ACL filter |
| S6 | Clustering, differential backup, PITR [CLAIM-neo4j-16][CLAIM-neo4j-17] | Orchestrate through BL-50 |
| S7 | One database per tenant [CLAIM-neo4j-13] | Adapter routes tenants to databases |
| S8 | Air-gappable Enterprise Studio [CLAIM-neo4j-28] | Customer-licensed only; never bundled |

## 9. Limitations with root causes

| Type | Limitation | Root cause | Evidence |
|---|---|---|---|
| Trade-off (verified) | No native reasoning; n10s inference is query-time and Labs-only | Algorithm (LPG built for traversal) | [CLAIM-neo4j-32] |
| Trade-off (verified) | GRAPH TYPE is open, so data outside it is unconstrained; no open-world axioms | Semantics | [CLAIM-neo4j-23] |
| Licensing | **CE has no RBAC, multi-database, clustering, online backup, existence/type/key constraints or GRAPH TYPE** | Community/enterprise split | [CLAIM-neo4j-05][CLAIM-neo4j-22] |
| Licensing | CE is GPLv3; Bloom, GDS EE and Dashboards are commercial; NVL is reportedly Neo4j-only | Licensing | [CLAIM-neo4j-04][CLAIM-neo4j-26][CLAIM-neo4j-33] |
| Verified | Value-based ACL: one property per rule, overhead, fails open | Runtime filtering | [CLAIM-neo4j-15] |
| Verified | GQL incomplete | Maturity | [CLAIM-neo4j-08] |
| Verified | **The HTTP API EOIP uses is deprecated** | Coupling (EOIP side) | [CLAIM-neo4j-11] |
| Verified | Query API explicit transactions only on Aura or a single instance | Deployment | [CLAIM-neo4j-12] |
| Verified | Vector index not visible within the transaction; one index per label/property pair | Storage (Lucene) | [CLAIM-neo4j-09] |
| Verified | Read committed: lost updates and MERGE deadlocks | Concurrency | [CLAIM-neo4j-20] |
| Operational | Monthly support windows; offline format migrations that change IDs | Operational overhead | [CLAIM-neo4j-02][CLAIM-neo4j-18] |
| Operational | Usage report on by default, sends server IP | Egress | [CLAIM-neo4j-30] |
| User-reported | Aura Dashboards are missing NeoDash features (2025) | UX | [CLAIM-neo4j-27] |
| Hypothesis | GDS and APOC run in the database JVM, so analytics can starve OLTP | Coupling | [CLAIM-neo4j-24] |

**Root causes grouped:**
- **Algorithmic dead-ends:** no entailment layer; per-row value-based ACL evaluation; supernodes handled only by dense-node trees.
- **Operational and hardware overhead:** heap pressure; offline migrations; monthly upgrade cadence.
- **User and developer friction:** schema enforcement gated to EE; Cypher 5 to 25 migration; commercial UI stack; unsupported RDF bridge.

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

| Constraint | Assessment |
|---|---|
| Air-gap | **Yes, self-hosted CE or EE,** with `dbms.usage_report.enabled=false` [CLAIM-neo4j-30]. Enterprise Studio works air-gapped [CLAIM-neo4j-28]. Aura and its console must never be mandatory. |
| One node first | CE or EE single instance works; GDS CE is limited to 4 cores [CLAIM-neo4j-24]. |
| Neutrality | Neo4j sits behind `GraphStore`; Neo4j-specific features are capability flags only. |
| Redistribution | **CE is GPLv3** [CLAIM-neo4j-04]. Bundling it in a white-label appliance creates GPL distribution duties. Network use through Apache-2.0 drivers [CLAIM-neo4j-34] is the lower-risk pattern. EE needs a commercial agreement; OEM terms exist but are not public. **Legal-review trigger.** |
| Tenancy | CE: EOIP predicate isolation. EE: one database per tenant. |
| Cost | EE, Infinigraph and GDS EE are priced through sales. Aura costs $0.09/GB/hour (Professional) and $0.20/GB/hour (Business Critical) [CLAIM-neo4j-29]. |

**Packaging:** customer-supplied Neo4j. EOIP ships only the client, with no Neo4j binaries, Bloom or NVL.

## 11. Competitive delta against the EOIP verified baseline

| Topic | Neo4j | EOIP | Delta |
|---|---|---|---|
| Transport | Query API and Bolt | BL-03 uses the deprecated `/tx/commit`, one statement per call [CLAIM-neo4j-36] | **EOIP deficit (P1)** |
| Writes | UNWIND, constraint-backed MERGE | Row-by-row; 3 calls per edge; no relationship index [CLAIM-neo4j-37][CLAIM-neo4j-38] | Performance gap |
| Correctness | — | **`edges_from`/`edges_to` filter labels after LIMIT** [CLAIM-neo4j-39]; `labels(n)[-1]` relies on an undocumented label order (hypothesis) [CLAIM-neo4j-41] | EOIP bugs (P1) |
| Pushdown | Native paths and optimiser | BL-08 templates in Python; BL-09 regex transpiler | Missing |
| Schema | GRAPH TYPE and constraints (EE) | BL-28 gate; BL-29 partial SHACL | Combine both |
| Reasoning | None | BL-30 partial OWL | EOIP ahead on paper; neither side has conformance proof |
| Temporal | None | BL-37 bitemporal | EOIP ahead |
| ACL and tenancy | EE RBAC and multi-database | **BL-18 absent; BL-20 contract only; adapter has no tenant handling** [CLAIM-neo4j-36] | EOIP P0 gap |
| Vector / analytics / backup | HNSW / GDS / PITR | BL-14 / BL-43 / BL-50 | Available upstream, not integrated |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Strength | Evidence | Value | Decision | Design | Acceptance test (PROPOSED) |
|---|---|---|---|---|---|---|
| STR-neo4j-01 | Native multi-hop Cypher | CLAIM-neo4j-05, -07, -43 | Fast J1, J9, J10 | match | `QueryPlan` → Cypher 25 compiler with injected ACL and tenant predicates | Same results as Python on 1M edges; p95 ≥5× faster |
| STR-neo4j-02 | In-graph hybrid retrieval | CLAIM-neo4j-09, -10 | One-round-trip GraphRAG | integrate | `VectorIndexPort` for Neo4j with `tenant` and `acl_hash` filters | recall@10 ≥0.95 of exact search; 0 cross-tenant hits |
| STR-neo4j-03 | GRAPH TYPE | CLAIM-neo4j-23 | No schema drift on EE | integrate | Manifest → GRAPH TYPE; constraints on CE | Violations rejected by both EOIP and Neo4j |
| STR-neo4j-04 | GDS | CLAIM-neo4j-24 | Analytics at scale | integrate (optional) | Algorithm port writing to the prediction plane | Matches BL-43 on a small graph; 10M edges within budget |
| STR-neo4j-05 | EE fine-grained security | CLAIM-neo4j-14, -15 | Defence in depth | integrate | ACL partitions mapped to labels and roles | J5 passes with the database alone and with EOIP added |
| STR-neo4j-06 | Differential backup and PITR | CLAIM-neo4j-17 | RPO and RTO | integrate | BL-50 calls `neo4j-admin` backup and restore | Restore to a transaction ID; empty BL-38 diff |
| STR-neo4j-07 | One database per tenant | CLAIM-neo4j-13 | Physical isolation | integrate | Tenant → database map | J13: zero leaks |

### Inversion cards

**INV-neo4j-01: seed hypothesis §10.5, "weak formal semantics / no native reasoning / schema decay".**
- **Scope:** 5.26 CE and 2026.09 EE, governed knowledge graphs.
- **Verdict: PARTIALLY VALIDATED.**
  - Validated: no native reasoning [CLAIM-neo4j-32] and no data axioms; GRAPH TYPE is open [CLAIM-neo4j-23].
  - Rejected: "weak formal semantics" as stated. Cypher has peer-reviewed semantics and is moving toward GQL [CLAIM-neo4j-43][CLAIM-neo4j-08]. The weakness is data semantics, not query semantics.
  - Rejected for EE 2026.06+: "schema decay", because GRAPH TYPE enforces implication, types, keys and endpoints.
  - Validated for CE, which has uniqueness constraints only [CLAIM-neo4j-22].
- **Root cause:** semantics and licensing (proven).
- **Alternative:** a shape contract enforced in EOIP's gateway works on any backend. It is worse against writers that bypass EOIP, which only native enforcement catches.
- **Options:**
  1. n10s SHACL. Rejected: Labs, and no 2026.x release.
  2. **Selected:** gateway contract *plus* compilation to GRAPH TYPE or constraints.
  3. Long term: EOIP rule materialisation (RL/Datalog fragment) that writes inferred edges with `creation_status=INFERRED` and the rule version.
- **Sketch:**
```
shape = Manifest.compile(); gate.enforce(shape)                     # all backends (BL-28)
if caps.edition=="EE" and caps.version>="2026.06":
    run("CYPHER 25 ALTER CURRENT GRAPH TYPE SET {"+to_graph_type(shape)+"}")
else: run_all(to_uniqueness_constraints(shape))
```
- **POC:** 50 shapes and 10k writes, 5% of them violating, sent via (a) EOIP, (b) EOIP plus GRAPH TYPE, (c) direct Cypher. Success: 100% rejected in (a) and (b), and in-scope violations rejected in (c) on EE. Write overhead under 10%.
- **Risks:** mismatched open semantics; legacy data that violates the type blocks migration; rollback needs `DROP`.
- **Defensibility:** the same contract governs HugeGraph and Neptune.
- **Decision: ADOPT.**

**INV-neo4j-02: the CE/EE split blocks tenancy and governance on CE.**
- **Limitation:** CE has one database, no RBAC, no online backup and no clustering [CLAIM-neo4j-05][CLAIM-neo4j-13]. Root cause: licensing (proven).
- **Alternative:** EOIP-layer isolation works on CE. It is worse than one database per tenant for noisy neighbours and tenant deletion.
- **Options:**
  1. Require EE.
  2. **Selected:** adapter `TenantPlacement` with `DB_PER_TENANT` (EE) and `POOLED_LABEL` (CE). In pooled mode the adapter injects mandatory `n.tenant=$t` and `:T_<id>` predicates and rejects any statement without the guard.
  3. Per-tenant instances (SILO).
- **POC:** J13 with 2 tenants × 100k entities on CE, with fuzzed queries. Success: zero cross-tenant rows.
- **Defensibility:** uniform tenancy across backends and editions.
- **Decision: ADOPT.**

**INV-neo4j-03: database-level ACLs are costly and fail open.**
- **Limitation:** value rules allow one property, add overhead and fail open [CLAIM-neo4j-15]. They cannot express varied per-source ACLs. Root cause: per-row evaluation at runtime (proven).
- **Alternative:** precomputed `acl_hash` partitions (BL-17) filtered through an indexed `IN $acl`. Worse when ACLs churn, because data must be re-labelled.
- **Options:**
  1. Post-filtering. This leaks counts.
  2. **Selected:** indexed pre-filter in Cypher and in vector `SEARCH`, with EE roles as defence in depth.
  3. ReBAC service (OpenFGA or SpiceDB, W34).
- **POC:** J5 with 2 principals, 10k documents and a revocation. Success: no inaccessible fact in results, embeddings or caches 60 s after revocation; p95 overhead under 15%.
- **Decision: ADOPT.** This closes BL-18 (P0).

**INV-neo4j-04: vector index freshness and filter semantics.**
- **Limitation:** writes are not visible within the transaction, and only one index per pair is allowed [CLAIM-neo4j-09]. Whether filters apply before or after the search is undocumented. Root cause: Lucene segments (proven for freshness; filter behaviour is a hypothesis).
- **Options:**
  1. Accept eventual freshness.
  2. **Selected:** filter properties plus oversampling plus filter-recall verification.
  3. External vector database through the BL-14 port (W23).
- **POC:** 1M 768-dimension vectors at 1% filter selectivity. Success: filtered recall@10 ≥0.9.
- **Decision: EXPERIMENT.**

**INV-neo4j-05: licence and redistribution exposure.**
- **Limitation:** GPLv3 CE; commercial Bloom, GDS EE and Dashboards; restricted NVL [CLAIM-neo4j-04][CLAIM-neo4j-33]. Root cause: licensing (proven).
- **Options:**
  1. Bundle CE (needs legal review).
  2. **Selected:** customer-supplied Neo4j; EOIP ships only Apache-2.0 drivers; EOIP's Cytoscape/Sigma UI does not depend on NVL.
  3. OEM agreement.
- **Downside:** no batteries-included appliance.
- **Test:** an SBOM scan finds no Neo4j server or NVL artefacts in EOIP images.
- **Decision: ADOPT** (legal-review trigger).

**INV-neo4j-06: EOIP adapter self-inversion** (propose an aggregate INV-SELF ID).
- **Limitation:** deprecated API, 3 calls per edge, no batching, full relationship scan, filtering after LIMIT, no tenant [CLAIM-neo4j-36]–[CLAIM-neo4j-39]. Root cause: coupling and maturity (proven from code).
- **Options:**
  1. Switch the endpoint to `/db/{db}/query/v2` with `maxExecutionTime` [CLAIM-neo4j-12].
  2. **Selected:**
     - Query API as the zero-dependency default, with an optional Bolt extra (Apache-2.0 driver).
     - UNWIND batches of 500.
     - A relationship index `FOR ()-[r:<T>]-() ON (r.edge_key)` per type.
     - Typed lookups.
     - Label filtering inside Cypher.
     - Tenant injection (INV-02).
  3. Cypher compiler (STR-01).
- **POC:** BM-01 on 5.26.32 CE and 2026.09.0 EE (evaluation). Success: 100% conformance; 100k vertices and 300k edges load ≥20× faster.
- **Compatibility:** HTTP mode stays behind a flag until Neo4j removes it.
- **Decision: ADOPT.**

## 13. Per-capability decisions

| Capability | Decision | Rationale |
|---|---|---|
| Neo4j backend (CAP-01) | INTEGRATE | Required; stays behind `GraphStore` |
| Cypher/GQL pushdown (CAP-14, 19) | BUILD the compiler; INTEGRATE Neo4j execution | STR-01 |
| Schema enforcement (CAP-08) | BUILD the portable contract; INTEGRATE GRAPH TYPE | INV-01 |
| OWL/RDFS reasoning (CAP-22, 23) | REJECT n10s; BUILD/REUSE in EOIP (C02/C03 workers) | Labs-only, query-time |
| SHACL (CAP-10) | REJECT n10s as the engine; REUSE standard tooling (W11) | Partial and unsupported |
| Vector and hybrid (CAP-53, 55) | INTEGRATE (optional) | STR-02 |
| Algorithms (CAP-62, 64) | INTEGRATE GDS (optional; customer licence for >4 cores) | STR-04 |
| Tenancy (CAP-47) | BUILD placement modes | INV-02 |
| ACL (CAP-45, 46) | BUILD in EOIP; INTEGRATE EE RBAC as defence in depth | INV-03 |
| Backup and HA (CAP-74, 76) | INTEGRATE native tools | STR-06 |
| Temporal (CAP-34, 36) | Keep the EOIP build (BL-37) | Neo4j has nothing native |
| Visualisation (CAP-70, 71) | REJECT embedding Bloom or NVL; use as UX reference | Licensing |
| Bulk load (CAP-06) | BUILD UNWIND; EXPERIMENT with `neo4j-admin import` | Throughput |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All tests below are PROPOSED; none has been run.

| Test | Setup | Pass condition |
|---|---|---|
| T1 Conformance (BM-01) | 5.26.32 CE, 2026.09.0 CE and EE | 100% pass; edition flags reported correctly |
| T2 API migration | Query API and Bolt modes | Results match HTTP mode; no deprecation notices |
| T3 Bulk load | 100k vertices + 300k edges; 8 vCPU / 32 GB | ≥20× faster than today; rerun creates no duplicates |
| T4 Concurrency | 16 writers on overlapping keys | 0 duplicate `canonical_id` or `edge_key`; deadlocks retried |
| T5 Schema | GRAPH TYPE (EE) and constraints (CE) | Violations rejected |
| T6 Tenancy (J13) | Pooled CE and one database per tenant (EE) | 0 leaks in rows, vectors and logs |
| T7 ACL (J5) | Revocation | No stale access after 60 s |
| T8 Air-gap (J16) | No network; usage report off | Full flow works; 0 outbound packets |
| T9 Portability (J14) | HugeGraph, Neo4j, Neptune | Parity-gap report produced |
| T10 `edges_from` | More edges than `limit`, mixed labels | Complete filtered set returned |

## 15. Risks, trade-offs, and open research questions

**Risks:**
- **R1: the HTTP API could be removed, breaking BL-03.** No removal date is published.
- R2: CalVer churn versus pinning the LTS, which lacks GRAPH TYPE (needs 2026.06+).
- R3: EE-gated features depend on what the customer has licensed.
- R4: GPL and NVL exposure if bundled.
- R5: usage report egress.

**Open questions:**
- Q1: are vector filters applied before or after the search?
- Q2: is `labels()` order stable?
- Q3: what is in the next LTS, and when is the HTTP API removed?
- Q4: what write overhead does GRAPH TYPE add?
- Q5: are there independent LDBC results for 2026.x?
- Q6: does n10s work with 2026.x?

---

## Appendix A — Research-dimension coverage

| Dim | Section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity | §1 | CalVer; 5.26 LTS to 2028-06-06; GPLv3 or commercial |
| D2 Problem | §2 | OLTP LPG plus analytics |
| D3 Architecture | §4, §5 | system-DB control plane, Raft, plugins in the JVM |
| D4 Storage | §5 | aligned linked records; block format (EE); GBPTree; Lucene |
| D5 Schema | §3, §5, INV-01 | uniqueness (CE); existence/type/key and GRAPH TYPE (EE); open semantics |
| D6 Query | §5 | Cypher 5/25, partial GQL, cost-based optimiser, `SEARCH` |
| D7 Reasoning | §5, INV-01 | none native; n10s query-time |
| D8 Transactions | §5, §7 | read committed, Raft, Infinigraph |
| D9 Ingestion | §3, §7 | CDC (EE), admin import, UNWIND |
| D10 Identity and evidence | §5 | no entity resolution or provenance model; EOIP builds it |
| D11 Time | §5 | PITR and CDC only |
| D12 Algorithms and ML | §3, STR-04 | GDS CE/EE |
| D13 Retrieval | §3, STR-02 | HNSW, full-text, `SEARCH`; GraphRAG covered by W19 |
| D14 NL query | — | N/A here; Text2Cypher covered by W19/W32 |
| D15 Governance | INV-01 | GRAPH TYPE lifecycle; no review workflow |
| D16 Human experience | §1, §3 | Browser, Bloom, Dashboards, Studio |
| D17 Developer experience | §3 | drivers, APOC, hot plugin reload |
| D18 Security | §5, INV-03 | EE RBAC; DENY fails open |
| D19 Tenancy | INV-02 | one database per tenant on EE only |
| D20 Economics | §7, §10 | no independent benchmarks; Aura prices |
| D21 Commercial | §10 | community/enterprise split; OEM terms not public |
| D22 Interoperability | §5, §13 | RDF via n10s (Labs); partial GQL |
| D23 IP | — | Not assessed: no patent search in this run |
| D24 Research quality | App. C | official docs dominate; no reproducible benchmarks |

## Appendix B — Capability mapping

| CAP | Neo4j | Evidence | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-01 | native | -18 | BL-03 Implemented, not run live | INTEGRATE | P1 |
| CAP-05 | enterprise-only | -16, -06 | n/a | INTEGRATE (customer EE) | P3 |
| CAP-06 | native | -38 | BL-03 row-by-row | BUILD batching | P1 |
| CAP-08 | partial (CE) / enterprise-only (GRAPH TYPE) | -22, -23 | BL-28 Implemented | BUILD + INTEGRATE | P1 |
| CAP-09/10 | plugin (Labs) | -31 | BL-30/29 Partial | REJECT n10s | P1 |
| CAP-14 | native (partial GQL) | -07, -08 | BL-09 Partial | BUILD compiler | P1 |
| CAP-18/19 | native | -05 | BL-08 emulated | INTEGRATE pushdown | P1 |
| CAP-22 | absent | -32 | BL-30 Partial | BUILD | P2 |
| CAP-34 | absent | -17 | BL-37 Implemented | keep BUILD | P1 |
| CAP-45 | enterprise-only | -14 | BL-19 Implemented | INTEGRATE | P2 |
| CAP-46 | enterprise-only, partial | -15 | BL-18 Absent | BUILD | P0 |
| CAP-47 | enterprise-only | -13 | BL-20 Partial | BUILD | P0 |
| CAP-50 | native | -30 | compose | INTEGRATE config | P0 |
| CAP-53/54 | native | -09, -10 | BL-14 Partial / BL-13 | INTEGRATE optional | P2 |
| CAP-62 | plugin | -24 | BL-43 | INTEGRATE optional | P2 |
| CAP-70 | commercial | -26, -33 | BL-54 | REJECT embedding | P3 |
| CAP-74/76 | enterprise-only | -16, -17 | BL-50 | INTEGRATE | P2 |
| CAP-77 | mixed | -29 | n/a | legal review | P1 |

## Appendix C — Evidence records

All records were accessed on 2026-10-18. "OD" means Officially documented.

| CLAIM | Product / version | Exact claim | Class | Source | Published | Conf. | Contra |
|---|---|---|---|---|---|---|---|
| neo4j-01 | 2026.09.0 | Latest release, 21 Sep 2026; a 2026.08.0 bug broke some queries (patched) | OD | https://neo4j.com/release-notes/database/neo4j-2026-09/ | 2026-09-21 | 0.85 | page meta says 09-23 |
| neo4j-02 | all | CalVer since 2025.01; minors supported until the next release; 5.26 LTS to 2028-06-06; 5.26.32 on 2026-10-08 | Third-party | https://endoflife.date/neo4j | rolling | 0.7 | one source says Nov 2028 |
| neo4j-03 | tags | 2026.09.0 (09-16), 5.26.32 (10-08) | Source repo | https://github.com/neo4j/neo4j/tags | 2026-10-08 | 0.9 | — |
| neo4j-04 | CE/EE | "licensed under the GNU GENERAL PUBLIC LICENSE Version 3", superseded by a commercial agreement; EE "closed-source components … requires a commercial license" | Source code | https://github.com/neo4j/neo4j (LICENSE.txt, README) | current | 0.95 | — |
| neo4j-05 | 2026.09 | Edition table: EE-only = block format, CDC, pipelined/parallel runtimes, GDS EE, Bloom, existence/type/key constraints, RBAC, sub-graph and property ACL, LDAP, online backup, multi-database, clustering, composite databases, Prometheus. CE = vector indexes and uniqueness constraints. | OD | https://neo4j.com/docs/operations-manual/current/introduction/ | current | 0.9 | — |
| neo4j-06 | 2025.12+ | Graph shard plus hashed property shards; "requires an Infinigraph subscription"; not on Aura | OD | …/operations-manual/current/scalability/sharded-property-databases/overview/ | current | 0.85 | — |
| neo4j-07 | 2025.06+ | Cypher 25 arrived in 2025.06; Cypher 5 frozen; new features only in 25; conf default CYPHER_25 from 2026.02 | OD | https://neo4j.com/docs/cypher-manual/current/queries/select-version/ | current | 0.9 | — |
| neo4j-08 | Cypher 25 | "supports the majority of mandatory GQL features"; unsupported: §7.1–7.3, §8.1–8.4, §11.1, §17.1, §21.3 | OD | …/cypher-manual/current/appendix/gql-conformance/ (+ /unsupported-mandatory/) | current | 0.85 | — |
| neo4j-09 | 2026.x | Lucene HNSW; 1–4096 dimensions; cosine/euclidean; none/scalar/binary quantisation; filter properties (2026.01); `SEARCH` preferred, procedures deprecated 2026.04; CE list properties, VECTOR needs block format; transaction changes not visible; one index per pair | OD | …/cypher-manual/current/indexes/semantic-indexes/vector-indexes/ | current | 0.8 | quantisation-default wording inconsistent |
| neo4j-10 | 2026.09 | Full-text `SEARCH`; "about a 5X reduction in latency and 5X increase in query throughput" | Vendor claim, Unverified | release notes (as -01) | 2026-09-21 | 0.3 for figure | — |
| neo4j-11 | 5.26+ | "The transactional HTTP API is deprecated and replaced by the Query API"; "Not available on Aura" | OD | https://neo4j.com/docs/http-api/current/ (+ /transactions/) | current | 0.9 | — |
| neo4j-12 | 5.19+ | Introduced 5.19, on by default from 5.25; `POST /db/<db>/query/v2`; explicit transactions "only available on Aura and on single-instance self-managed servers"; `maxExecutionTime` since 2026.04 | OD | https://neo4j.com/docs/query-api/current/ (+ /query/, /transactions/) | current | 0.85 | rollback path shown inconsistently |
| neo4j-13 | current | CE has "exactly one standard database"; EE "any number"; no cross-database transactions | OD | …/operations-manual/current/database-administration/ | current | 0.9 | — |
| neo4j-14 | EE | GRANT with no DENY required; restricted reads invisible; one graph per database | OD | …/authentication-authorization/manage-privileges/ | current | 0.85 | — |
| neo4j-15 | EE | One property per rule; "significant performance overhead"; DENY "fails open"; not on sharded databases | OD | …/authentication-authorization/property-based-access-control/ | current | 0.9 | — |
| neo4j-16 | EE | One writer; ≤11 primaries, ≤20 secondaries; Raft; bookmarks | OD | …/operations-manual/current/clustering/introduction/ | current | 0.85 | — |
| neo4j-17 | EE | `--restore-until` timestamp or txId; differential chains; restore is EE | OD | …/backup-restore/restore-backup/ | current | 0.9 | — |
| neo4j-18 | current | Block format is the EE default since 5.22 (2^48); aligned is CE (2^35); 128 B = 2×64 B; standard/high_limit deprecated; final LTS Nov 2026 | OD | …/database-internals/store-formats/ | current | 0.85 | — |
| neo4j-19 | 2026.09 | Bundles GDS 2026.09.0, Bloom 2.36.0, APOC, GenAI plugin; `dbms.reloadProcedures()`; page-cache fix; high_limit fails after the next LTS | OD | release notes (as -01) | 2026-09-21 | 0.85 | — |
| neo4j-20 | current | Read committed; lost updates; DeadlockDetected; MERGE locks out of order | OD | …/database-internals/concurrent-data-access/ | current | 0.85 | — |
| neo4j-21 | current | Transaction changes kept in memory; 1000 concurrent; timeout default 0 | OD | …/database-internals/transaction-management/ | current | 0.85 | — |
| neo4j-22 | current | Uniqueness is in CE; existence, type and key constraints are EE | OD | https://neo4j.com/docs/cypher-manual/current/schema/constraints/ | current | 0.85 | — |
| neo4j-23 | 2026.02/.06 | GRAPH TYPE introduced 2026.02, GA 2026.06, EE, Cypher 25 only; open; implication, types, NOT NULL, keys, endpoints | OD | …/cypher-manual/current/schema/graph-types/ ; https://neo4j.com/blog/developer/graph-type-schema-enforcement-made-easy-preview/ | 2026-03-03 | 0.85 | — |
| neo4j-24 | GDS | CE: all algorithms, 4 cores, 3 models. EE: licence file, Arrow, model persistence, optimised graph, cluster writes | OD | https://neo4j.com/docs/graph-data-science/current/introduction/ | current | 0.9 | — |
| neo4j-25 | GDS | OpenGDS GPLv3; distributed build has closed sources; CalVer from 2026.03 | Source repo | https://github.com/neo4j/graph-data-science (README, LICENSE.txt) | current | 0.9 | — |
| neo4j-26 | Bloom | Plugin activation key required; hosted app is EE; semver; Desktop governed by its own licence | OD | https://neo4j.com/docs/bloom-user-guide/current/bloom-installation/installation-activation/ (+ deployment modes) | current | 0.8 | free Desktop use in 2026 unconfirmed |
| neo4j-27 | NeoDash | Labs "no longer maintained", Apache-2.0; staff (Aug 2025): archived read-only; commercial version under Enterprise agreement; Aura Dashboards gaps | OD + third-party | https://github.com/neo4j-labs/neodash ; https://community.neo4j.com/t/75091 ; https://neo4j.com/docs/neodash-commercial/current/ | 2025-08-12 | 0.75 | — |
| neo4j-28 | Studio | Announced 2026-06-24; Query, Bloom, Dashboards; "can be deployed in airgapped environments"; SSO | OD (vendor blog) | https://neo4j.com/blog/graph-database/enterprise-studio/ | 2026-06-24 | 0.75 | price not public |
| neo4j-29 | Aura/self-managed | Professional $0.09/GB/h; Business Critical $0.20/GB/h; RBAC from Business Critical up; CE has no HA, hot backup, RBAC or multi-database | OD | https://neo4j.com/pricing/ | current | 0.8 | prices change |
| neo4j-30 | CE/EE | Usage reported every 24 h, including server IP; `dbms.usage_report.enabled=false` disables | OD | https://neo4j.com/docs/usage-data | current | 0.85 | — |
| neo4j-31 | n10s 2025.06.1 | "experimental Neo4j Labs project … not part of Neo4j's supported product lineup"; Apache-2.0; SHACL "significant portion … but not all"; trigger mode via APOC | Source repo (docs) | https://github.com/neo4j-labs/neosemantics (branch 2025.06, docs/…/validation.adoc) | 2025 | 0.85 | release year inferred |
| neo4j-32 | n10s | Inference "on the fly" via `n10s.inference.*` over subClassOf/subPropertyOf | Source repo (docs) | neosemantics inference.adoc (branch 2025.06) | 2025 | 0.85 | — |
| neo4j-33 | NVL 2.0.0 | npm licence "SEE LICENSE IN 'LICENSE.txt'", published 2026-09-15; third party says "for use with Neo4j products only" | Registry + third-party | https://registry.npmjs.org/@neo4j-nvl/base ; https://tessl.io/registry/skills/github/neo4j-contrib/neo4j-skills/neo4j-nvl-skill | 2026-09-15 | 0.5 | W29 to confirm |
| neo4j-34 | drivers/APOC | Python driver 6.4.1 (2026-10-15) Apache-2.0 AND Python-2.0; APOC Apache-2.0 | Registry/repo | https://pypi.org/project/neo4j/ ; https://github.com/neo4j/apoc | 2026-10-15 | 0.9 | — |
| neo4j-35 | Desktop | Developer offerings "generally provided for free and internal, non-production use" | OD | https://neo4j.com/licensing/ | current | 0.7 | — |
| neo4j-36 | EOIP adapter | `/db/{database}/tx/commit`; one statement per request; row format; default database `neo4j`; no tenant; compose `neo4j:5-community` | Source code | `packages/eoip/graph/neo4j.py:51,69-81`; `deploy/docker-compose.yml:48` | HEAD ad9937b | 0.95 | — |
| neo4j-37 | EOIP adapter | `MATCH ()-[r {edge_key:$k}]->()` is untyped; `ensure_schema` creates only a node constraint and index, so this is a full relationship scan | Source code + inference | `neo4j.py:128-131, 286-289` | HEAD | 0.8 | — |
| neo4j-38 | EOIP adapter | `bulk_load` writes one entity per call; `batch_size` only reported; `upsert_edge` makes 3 requests | Source code | `neo4j.py:241-279, 347-381` | HEAD | 0.9 | — |
| neo4j-39 | EOIP adapter | `edges_from`/`edges_to` filter labels in Python after LIMIT | Source code | `neo4j.py:318-336` | HEAD | 0.9 | — |
| neo4j-40 | 5.26 | `5-community` runs 5.26 LTS, where the HTTP API is deprecated but present | Inference | -02 + -11 | — | 0.6 | — |
| neo4j-41 | EOIP adapter | `labels(n)[-1]` assumes a label order; no documented guarantee found | Inference (hypothesis) | `neo4j.py:172,185,193,229` | HEAD | 0.4 | untested |
| neo4j-42 | 2026.09.0 | `community/` contains record-storage-engine, cypher, kernel, lucene-index, native-index, lock, wal, bolt, server, fabric, genai-plugin | Source repo | https://github.com/neo4j/neo4j/tree/2026.09.0/community | 2026-09-16 | 0.9 | — |
| neo4j-43 | Cypher | Formal semantics: Francis et al., "Cypher: An Evolving Query Language for Property Graphs", SIGMOD 2018, doi:10.1145/3183713.3190657 | Peer-reviewed | ACM SIGMOD 2018 | 2018 | 0.85 | covers Cypher 9, not 25 |

## Appendix D — Assumptions

1. "Latest" means the latest generally available release on 2026-10-18 (2026.09.0); 2026.10 is presumed unpublished.
2. `neo4j:5-community` resolves to the latest 5.26.x; the image digest was not pulled.
3. Bloom and NeoDash commercial terms are summarised from documentation, not from contracts. No legal conclusions are drawn.
4. The NVL licence is deferred to W29 (low confidence).
5. Adapter line numbers refer to HEAD `ad9937b`.
6. The GitHub API was rate-limited, so github.com pages and raw files were used instead.
7. No patent search was done (D23).
