# C01 — Kùzu and successors/forks (LadybugDB, RyuGraph, Bighorn)

| Field | Value |
|---|---|
| Registry ID | T-C01-kuzu |
| Tier | B — embedded columnar / CSR / worst-case-optimal-join architecture reference; upstream archived 2025 (Master Prompt §5.1) |
| Versions examined | Kùzu v0.11.3 (GitHub release 2025-10-10, final release; repository archived 2025-10-10). Design per CIDR 2023 paper / technical report. LadybugDB v0.21.2 (GitHub release "01 Oct", asset timestamps 2026). RyuGraph crate 25.9.2 (Dec 2025 per lib.rs; repository tag not visible). Bighorn branch 0.11 (no release visible). |
| Verified on | 2026-10-18 |
| Worker | W06 |

## 1. Identity, current status, tier, and sources

**Identity.** Kùzu (repository `github.com/kuzudb/kuzu`, owner Kùzu Inc., originating in Semih Salihoğlu's group at the University of Waterloo) is an embeddable, disk-based property-graph DBMS queried with Cypher [CLAIM-kuzu-05][CLAIM-kuzu-06].

**Status — resolves trap §5.1.** The official repository "was archived by the owner on Oct 10, 2025. It is now read-only" [CLAIM-kuzu-01]. The last release is **v0.11.3, published 2025-10-10** [CLAIM-kuzu-02]. The README carries a notice that the project is being archived and that Kùzu "is working on something new"; existing releases keep working, and extension users are pointed to v0.11.3 or a self-hosted extension server [CLAIM-kuzu-04]. On the access date the documentation host `docs.kuzudb.com` did not resolve (DNS ENOTFOUND) in our fetch [CLAIM-kuzu-10]. Third-party reports say Apple acqui-hired the Kùzu team, citing a European Commission filing. We did not find the primary filing, so this stays a third-party report [CLAIM-kuzu-11]. **Kùzu is treated as archived and not advancing.** The earlier unverified market-position phrase from prior internal material is not repeated.

**Licence.** MIT [CLAIM-kuzu-03].

**Successors / forks (pinned):**

| Fork | Repository / owner | Licence | Evidence of activity (2026-10-18) | Assessment |
|---|---|---|---|---|
| LadybugDB | `github.com/LadybugDB/ladybug`, "LadybugDB Developers"; led by Arun Sharma per a third-party report | MIT | README: "formerly known as Kuzu"; 6,697 commits, 1.9k stars, 104 open issues; releases v0.21.0–v0.21.2 dated 29 Sep–01 Oct (2026) [CLAIM-kuzu-12][CLAIM-kuzu-13] | The only fork with verified recent releases. Third-party coverage calls it the definitive fork and lists new features (multiple labels per node, attaching external databases, subgraphs) [CLAIM-kuzu-18] |
| RyuGraph | `github.com/predictable-labs/ryugraph`, Predictable Labs, Inc. | MIT | 5,339 commits; no release tag on the repo page; Rust crate releases up to 25.9.2 (Dec 2025) [CLAIM-kuzu-15] | Maintained by a company that used Kùzu internally; 2026 activity **UNVERIFIED** |
| Bighorn | `github.com/Kineviz/bighorn`, Kineviz | MIT | 5,219 commits on branch 0.11; no releases; a third-party editor's note calls it unmaintained [CLAIM-kuzu-14] | Treat as dormant |
| Vela Partners fork | not pinned | unknown | A vendor blog claims concurrent writes and "374x faster than Neo4j", with no workload or hardware published [CLAIM-kuzu-16] | Unverified marketing; not used |

The registry entry "Kùzu and successors/forks" is read as Kùzu v0.11.3 (the architecture reference) plus LadybugDB as the only currently viable continuation.

**Tier B reason.** Architecture reference for embedded columnar storage, CSR join indices, factorised processing and worst-case-optimal (WCO) joins. Not a supported EOIP backend.

## 2. Primary problem, target workloads, concrete example workflows

Kùzu targeted *in-process* graph analytics. It is a library linked into a Python/C++/Node/Java/Rust/Wasm application, with no server, for graphs too large to handle comfortably in an in-memory library such as NetworkX, and for queries with many-to-many joins (multi-hop, cyclic patterns) [CLAIM-kuzu-05][CLAIM-kuzu-06]. The paper names graph-ML pipelines (feature loading for PyG/DGL) as a motivating case [CLAIM-kuzu-06].

Example workflows relevant to EOIP:
- **Local blast-radius analytics (J9):** export an EOIP tenant snapshot as node/edge tables, load it into an embedded engine, and run 3–5-hop `MATCH` queries from a service account to deployments and runbooks.
- **Cyclic-pattern detection:** dependency cycles (service A → B → C → A) or triangle patterns in code/CI graphs. The WCO intersection operator is designed for these [CLAIM-kuzu-07].
- **GNN feature extraction (BL-44):** columnar scans of node properties for an N1 neural tier.

## 3. Feature inventory

| Area | Feature | Status (v0.11.3 unless noted) | Evidence |
|---|---|---|---|
| Data model | Property graph with typed node/rel tables (schema-first DDL) | present | CLAIM-kuzu-06 |
| Query | Cypher | present (dialect; no published TCK result found) | CLAIM-kuzu-05 |
| Query | GQL / SQL/PGQ / Gremlin / SPARQL | absent | CLAIM-kuzu-05 (not listed) |
| Storage | Columnar disk-based storage, CSR adjacency/join indices | present | CLAIM-kuzu-05, -06 |
| Execution | Vectorised, factorised processor; WCO multiway joins | present (design as in the paper) | CLAIM-kuzu-06, -07 |
| Search | Full-text index, vector index | present (extensions) | CLAIM-kuzu-05 |
| Transactions | Serializable ACID; single writer plus concurrent readers | present (paper); later MVCC changes UNVERIFIED | CLAIM-kuzu-08 |
| APIs | Python, C++, Node, Java, Rust, Wasm bindings | present | CLAIM-kuzu-05 |
| Server / cluster / HA | — | absent (embedded library) | CLAIM-kuzu-05 |
| AuthN/AuthZ, multi-tenancy | — | absent (process-level only) | reasoned inference from the embedded design |
| UI | Kùzu Explorer | unknown in 2026 (docs host down) | CLAIM-kuzu-10 |
| Extensions | Downloaded from an extension server | present; after the archive, requires self-hosting | CLAIM-kuzu-04 |
| Maintenance | Security fixes, platform builds | **absent since 2025-10-10** | CLAIM-kuzu-01 |

## 4. Text-based architecture diagram

```
 Host application process (Python / C++ / Node / Java / Rust / Wasm)
 +--------------------------------------------------------------------+
 |  Binding API --> Connection --> Cypher parser --> binder (catalog)  |
 |                                   |                                 |
 |                                   v                                 |
 |                logical plan --> DP join optimiser (filter push-down)|
 |                                   v                                 |
 |     physical plan: scans, S-Join / ASP-Join (accumulate,            |
 |     semijoin filter via sideways information passing, probe),       |
 |     multiway WCO ASP-Join (adjacency-list intersection)             |
 |                                   |  factorised vector groups       |
 |                                   v                                 |
 |  Buffer manager (fixed 4 KB pages, GClock eviction)                 |
 |        |                     |                        |             |
 |  node column files    fwd/bwd CSR adjacency     parallel CSR edge   |
 |  + PK hash index      (dst IDs [+labels])       property columns    |
 |        |                                                            |
 |  WAL (atomicity/durability) -- one write txn || many read txns      |
 +--------------------------------------------------------------------+
   one database directory on local disk; no network plane
```

The control plane and data plane are both inside the host process. There is no server, replication or tenant boundary [CLAIM-kuzu-06][CLAIM-kuzu-08].

## 5. Under-the-hood reconstruction

**Data model.** Typed node tables with a primary key, and typed rel tables between node tables. The paper also mentions an extra semi-structured column for arbitrary properties (as of the paper) [CLAIM-kuzu-06].

**Storage layout and indexing.** This is the published design. Whether v0.11.3 still matches it in every detail is a *hypothesis* [CLAIM-kuzu-06].
- Structured node properties are kept in plain column files (one column per property), addressed by dense internal node offsets.
- Edges are **double-indexed** in forward and backward CSR adjacency lists that hold destination node IDs. Labels are omitted when DDL fixes the destination label.
- Edge properties are kept in "parallel" CSR structures, also double-indexed. Any node's edges *and* their properties can then be scanned sequentially in both directions, at a storage and update cost the authors acknowledge.
- Each node table has a default hash index on its primary key.
- All structures are read through a buffer manager with 4 KB pages and GClock eviction.

**Query pipeline.** Parser → binder (types from the catalog) → logical plan → dynamic-programming join optimiser with filter push-down → physical operators [CLAIM-kuzu-09]. Intermediate results are *factorised vector groups*. A group is either flat (one current tuple) or unflat (a vector of values), so a 2-hop result `a × {b} × {c}` is represented without materialising the Cartesian product [CLAIM-kuzu-06].

**Joins** [CLAIM-kuzu-07]:
- **ASP-Join** (accumulate–semijoin–probe) runs in three pipelines. Pipeline 1 accumulates probe-side factorised tuples into a factorised table and builds a semijoin filter. Pipeline 2 builds the hash table, scanning only the build-side values that pass the filter (sideways information passing). Pipeline 3 re-scans the accumulated tuples and probes.
- **Multiway WCO ASP-Join** extends ASP-Join with Generic-Join-style extension: it intersects several adjacency lists of bound vertices to compute the extension variable (for example, triangles).

Pseudocode of the WCO extension step, reconstructed from the paper's description:

```
for each prefix tuple (a, b) in accumulated FT:          # bound vars
    L1 = fwd_adj[Trn][b]        # sorted dst IDs
    L2 = bwd_adj[DD][a]
    for c in intersect_sorted(L1, L2):                  # extension var
        emit factorised (a, b, c)
```

**Reasoning.** None (no rules, no ontology layer).

**Concurrency and transactions.** A WAL provides atomicity and durability. Transactions are serializable because only one write transaction runs at a time, alongside many readers. Multi-writer MVCC was "on the roadmap" in 2023 [CLAIM-kuzu-08]. Whether 0.11.x changed this is **UNVERIFIED** (docs unreachable).

**Partitioning, consistency and caching.** Single node, one database directory; the buffer pool is the only cache. **Versioning:** none beyond the WAL, and no time travel. **Security:** relies on OS file permissions; no users or roles (reasoned inference).

## 6. Functional and non-functional requirements inferred

- FR: schema-first typed node/rel tables; Cypher reads and writes; bulk `COPY` from files; FTS and vector extensions.
- NFR: embedding with no operations work; sequential scans for multi-hop; robustness on many-to-many joins; single-writer serializability; no network exposure.
- Implied for any EOIP use: the embedded engine must be a **derived, rebuildable projection** and never the authoritative store, because it lacks tenancy, ACLs, replication and, now, maintenance.

## 7. Performance and resource model

No benchmark was run in this programme. The paper reports that ASP-Join-based plans "can broadly outperform" factorised and flat plans in the authors' evaluation [CLAIM-kuzu-07]. That evaluation's hardware and dataset are in the paper and apply only to the 2023 code. Third-party fork marketing ("374x faster than Neo4j") publishes no workload or hardware and is treated as **Unverified** [CLAIM-kuzu-16].

Expected scaling (reasoned): double-indexed CSR roughly doubles edge storage compared with single-direction lists. Updates cost more than in LSM/KV layouts because CSR regions must be rewritten or overflowed.

Failure modes:
- contention on the single writer under concurrent ingest;
- buffer-pool thrashing when the working set is much larger than RAM;
- unpatched CVEs in an archived codebase.

## 8. Strengths — and how to match or exceed

1. **Sequential multi-hop scans from CSR plus columnar layout** [CLAIM-kuzu-06]. EOIP can match this by building an in-memory CSR *projection* of a tenant subgraph for algorithms (BL-43), instead of per-edge dictionary lookups in Python.
2. **WCO intersection for cyclic patterns** [CLAIM-kuzu-07]. EOIP can match this for named bounded templates that detect cycles (dependency loops, approval-bypass triangles), using sorted-list intersection over the projection.
3. **Factorised intermediate results** [CLAIM-kuzu-06] reduce memory blow-up on fan-out queries. EOIP can adopt a compact "grouped neighbours" result shape in QueryPlan responses.
4. **Embedding with no operations work, under a permissive licence** [CLAIM-kuzu-03]. This fits one-node first. EOIP can only get this through a maintained fork (LadybugDB) or its own projection code.

## 9. Limitations with root causes

| Type | Limitation | Root cause class | Evidence |
|---|---|---|---|
| Verified defect / status | Upstream archived, no fixes after 2025-10-10; docs host unreachable | Governance/maturity — **proven** | CLAIM-kuzu-01, -10 |
| Intentional trade-off | One writer at a time | Concurrency design — proven as of the paper | CLAIM-kuzu-08 |
| Intentional trade-off | Double-indexed CSR raises storage and update cost | Storage — proven (the authors state it) | CLAIM-kuzu-06 |
| Licensing | None (MIT); governance risk in the successors | — | CLAIM-kuzu-03 |
| Operational | Since the archive, extensions need a self-hosted extension server (affects air-gap) | Deployment — proven | CLAIM-kuzu-04 |
| Hypothesis | No tenant or ACL model; embedding it in a multi-tenant server needs one DB file per tenant | Architecture — hypothesis | reasoned |

Root causes by group:
- *Algorithmic dead-ends:* none; the join design is sound.
- *Operational and hardware overhead:* CSR update amplification and the single writer.
- *User and developer friction:* abandonment, fork fragmentation, and Cypher-dialect drift between forks.

## 10. Deployment, licensing, redistribution, operational viability

MIT allows OEM embedding and white-label redistribution, provided the notice is kept [CLAIM-kuzu-03]. The licence raises no legal-review trigger. The trigger is **operational**: embedding archived C++ code in a sold product means EOIP would own security patching. Air-gap: the core library works offline; extensions only with a self-hosted extension server [CLAIM-kuzu-04]. LadybugDB is also MIT [CLAIM-kuzu-12].

## 11. Competitive delta against the EOIP baseline

- EOIP runs traversal and algorithms in Python through the `GraphStore` CRUD/neighbourhood protocol, with no pushdown (BL-01, BL-43). Kùzu's design shows what a columnar CSR engine gains for multi-hop and cyclic queries.
- EOIP has no embedded analytical engine and no WCO joins (CAP-18 absent).
- EOIP is ahead on governance: validation gate (BL-28), revisions and bitemporal reads (BL-37), claims (BL-39), egress (BL-45). None of these exist in Kùzu.
- EOIP's backend neutrality (BL-01) protects against exactly the failure Kùzu showed: the vendor abandoning the engine.

## 12. Strength-adoption and inversion cards

**STR-kuzu-01** | Kùzu | CSR plus columnar storage for sequential multi-hop scans | CLAIM-kuzu-05, -06 | faster J1/J9 impact queries on one node | match | build an in-process, read-only CSR snapshot ("analytic projection") per tenant from the authoritative backend; rebuild it on the revision watermark | 3-hop blast-radius query on a synthetic 1M-edge tenant: projection result set identical to the `GraphStore` BFS, with p95 latency at least 5× lower (target, PROPOSED).

**STR-kuzu-02** | Kùzu | WCO multiway intersection for cyclic patterns | CLAIM-kuzu-07 | detect dependency cycles and control-bypass triangles | match | sorted adjacency arrays plus a k-way intersection operator inside named templates | triangle and 4-cycle counts equal to brute force on an LDBC-style synthetic graph; runtime grows sub-quadratically with skew (PROPOSED).

**STR-kuzu-03** | Kùzu / LadybugDB | embeddable engine with no operations work, MIT | CLAIM-kuzu-03, -12 | optional local analytics without a second server | integrate (experimental) | optional `analytics` module that loads Parquet exports into LadybugDB | installs and runs offline with no network and a bundled extension set (PROPOSED).

**INV-kuzu-01 — abrupt abandonment of a single-vendor embedded engine.**
- **Target/version/workload:** Kùzu v0.11.3, any embedded deployment.
- **Limitation:** archived with no successor guarantee [CLAIM-kuzu-01][CLAIM-kuzu-04].
- **Root cause:** governance/maturity (a single corporate owner) — **proven**.
- **Why an alternative mitigates it:** EOIP treats every engine as a replaceable adapter behind `GraphStore`. Authoritative state lives in a supported backend, and the SourceEvent log (BL-23/24) can rebuild any projection. This is worse when projection rebuild time exceeds the RTO for large tenants.
- **Options:**
  1. Quick: pin v0.11.3 in a sidecar.
  2. Pragmatic: an engine-agnostic "analytic projection" contract with two implementations, LadybugDB and an in-house numpy CSR.
  3. Long-term: an EOIP-owned projection format (Arrow/Parquet node/edge tables plus a revision watermark) that any embedded engine can read (LadybugDB, DuckDB+DuckPGQ).
- **Selected:** option 2, moving to option 3. Sketch:
  ```
  interface AnalyticProjection:
      build(tenant, watermark, label_filter) -> ProjectionHandle
      run(template_id, params, principal) -> Rows   # ACL-filtered before return
      drop(handle)
  ```
- **Benchmark/POC:** rebuild the projection of a 10M-edge tenant from a Parquet export on a 16-core/64 GB node. Success means rebuild time and query parity are recorded for both implementations, and the implementation can be swapped with no API change.
- **Dependencies, security and failure cases:** projections inherit the tenant boundary (one file per tenant). An ACL post-filter is mandatory, since BL-18 is a P0 gap. Failure case: a stale projection serving revoked data, prevented by enforcing the watermark and invalidating on revocation.
- **Defensibility:** the value is the contract plus the provenance and ACL wrapping, not the engine. A competitor that copies an engine does not get the governed rebuild path.
- **Decision:** **ADOPT** (contract), **EXPERIMENT** (LadybugDB implementation).

**INV-kuzu-02 — a single-writer embedded engine cannot serve concurrent multi-tenant writes.**
- **Limitation:** one write transaction at a time [CLAIM-kuzu-08].
- **Root cause:** concurrency design — proven as of the paper; a hypothesis for 0.11.
- **Inversion:** EOIP already funnels every write through one governed mutation path (BL-28, BL-23). A single-writer projection fed by that path is therefore a *fit*, not a defect. This is worse when interactive what-if writes are needed on the projection.
- **Options:**
  1. A read-only projection.
  2. Per-tenant projection files with an append-only apply loop.
  3. Incremental CSR delta segments merged in the background.
- **Selected:** option 2.
- **POC:** apply 100k revision events per minute to a per-tenant projection while serving reads. Success means no reader is blocked for more than 100 ms (target, PROPOSED).
- **Decision:** **EXPERIMENT**.

Seed hypotheses (§10.5): none targets Kùzu directly.

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-04 embedded/single-node analytics engine | EXPERIMENT | LadybugDB as an optional sidecar; never authoritative |
| CAP-18 WCO joins / factorised execution | BUILD (pattern) | in-house CSR projection plus intersection for named templates |
| CAP-62 graph algorithm library over CSR | BUILD | move BL-43 algorithms onto a CSR projection |
| CAP-01 as an EOIP backend adapter | REJECT (Kùzu) / DEFER (LadybugDB) | Kùzu is archived; fork governance is young |
| CAP-53 vector index via Kùzu | REJECT | follow the CAP-53 decision from the C10 cohort |

## 14. Concrete tests, POC, acceptance conditions (all PROPOSED)

1. **POC-kuzu-A:** export a synthetic 1M- and 10M-edge tenant from `MemoryGraphStore` to Parquet, load it into LadybugDB v0.21.x, and run 10 J1/J9 templates. Accept if the results equal the Python BFS reference and the install works offline with bundled extensions.
2. **POC-kuzu-B:** an in-house numpy CSR projection (requires adding numpy; see BL-57) for the same templates. Accept if it stays within 2× of LadybugDB latency, which would make the dependency unnecessary.
3. **Licence and supply-chain check:** produce an SBOM of the LadybugDB wheels and confirm MIT terms for all bundled third-party code.

## 15. Risks, trade-offs, open questions

- Fork fragmentation: Cypher dialects and file formats may diverge between LadybugDB, RyuGraph and Bighorn.
- Open questions:
  - Did Kùzu 0.11 add multi-writer MVCC? (docs offline)
  - Is LadybugDB's file format compatible with Kùzu 0.11.3?
  - What is LadybugDB's governance (foundation, CLA)?
  - Is the Apple acquisition documented in a primary filing?
- Trade-off: a projection adds a staleness window, and ACLs must be enforced in EOIP, not in the engine.

## Appendix A — Research-dimension coverage

| Dimension | Covered in section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | archived 2025-10-10, MIT, forks pinned |
| D2 Problem and workloads | 2 | embedded graph analytics |
| D3 Architecture decomposition | 4 | single-process library |
| D4 Storage primitives and indexing | 5 | columnar plus double-indexed CSR, PK hash index |
| D5 Schema and semantic expressivity | 3, 5 | typed node/rel tables; no ontology |
| D6 Query pipeline and optimisation | 5 | DP optimiser, ASP-Join, WCO |
| D7 Reasoning and inference | 5 | N/A — none |
| D8 Transactions, concurrency, scale | 5, 7 | WAL, single writer, single node |
| D9 Ingestion and federation | 3 | bulk COPY; no CDC or federation |
| D10 Identity and evidence | 11 | N/A — no provenance features |
| D11 Time and evolution | 5 | none; no time travel |
| D12 Graph algorithms and ML | 2, 8 | GNN feature pipelines as motivation |
| D13 Retrieval and agent integration | 3 | FTS and vector extensions |
| D14 Natural-language querying | — | N/A — none native |
| D15 Governance and authoring | 11 | N/A |
| D16 Human experience | 3 | Explorer status unknown |
| D17 Developer experience | 3 | many bindings |
| D18 Trust and security | 5, 9 | OS-level only; unpatched since the archive |
| D19 Multi-tenancy and white-label | 9 | none; one file per tenant (hypothesis) |
| D20 Empirical economics | 7 | qualitative only; nothing was run |
| D21 Commercial and licensing | 10 | MIT, no commercial edition |
| D22 Interoperability and lock-in | 12 | Parquet/CSV in; risk of fork divergence |
| D23 IP and prior art | 5 | factorisation and WCO are published academic methods (paper); no patent search done |
| D24 Research quality | 7, 15 | paper is from 2023; docs offline; fork data partly third-party |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-01 | native | CLAIM-kuzu-06 | BL-01/BL-02 Implemented | REJECT as backend | P3 |
| CAP-04 | native | CLAIM-kuzu-05 | BL-01 MemoryGraphStore (Partial) | EXPERIMENT (LadybugDB) | P2 |
| CAP-14 | native (dialect) | CLAIM-kuzu-05 | BL-03 via Neo4j; BL-59 Absent | REJECT (reference only) | P3 |
| CAP-18 | native | CLAIM-kuzu-07, -09 | Absent | BUILD (pattern) | P2 |
| CAP-19 | native | CLAIM-kuzu-06 | BL-43 Implemented (Python) | BUILD (CSR projection) | P2 |
| CAP-53 | plugin | CLAIM-kuzu-05 | BL-14 Partial | REJECT here | P3 |
| CAP-62 | partial | CLAIM-kuzu-06 | BL-43 Implemented | BUILD | P2 |
| CAP-77 | MIT, no support | CLAIM-kuzu-01, -03 | BL-22 Implemented | REJECT (unsupported dependency) | P3 |

## Appendix C — Evidence records

| CLAIM-ID | product / version / date | exact claim | classification | source title + URL | publication / access date | confidence + rationale | contradictory evidence |
|---|---|---|---|---|---|---|---|
| CLAIM-kuzu-01 | Kùzu repo, 2025-10-10 | "This repository was archived by the owner on Oct 10, 2025. It is now read-only." | Officially documented | GitHub kuzudb/kuzu — https://github.com/kuzudb/kuzu | 2025-10-10 / 2026-10-18 | 0.95: GitHub banner plus API `archived: true`, last push 2025-10-10T15:34Z | none |
| CLAIM-kuzu-02 | Kùzu v0.11.3 | latest and final release v0.11.3 published 2025-10-10 (previous: v0.11.2, 2025-08-21) | Officially documented | GitHub releases API — https://api.github.com/repos/kuzudb/kuzu/releases | 2025-10-10 / 2026-10-18 | 0.9: API output | none |
| CLAIM-kuzu-03 | Kùzu | Licence: MIT | Officially documented | GitHub repo licence — https://github.com/kuzudb/kuzu | — / 2026-10-18 | 0.95: SPDX ID via API | none |
| CLAIM-kuzu-04 | Kùzu README | Project being archived; "working on something new"; extension users should use v0.11.3 or self-host an extension server | Officially documented | README — https://github.com/kuzudb/kuzu | 2025-10 / 2026-10-18 | 0.85: README text via fetch | none |
| CLAIM-kuzu-05 | Kùzu README | columnar disk-based storage; columnar sparse row-based (CSR) adjacency list/join indices; vectorised and factorised processor; FTS and vector index; serializable ACID; Cypher; Wasm | Officially documented | README — https://github.com/kuzudb/kuzu | — / 2026-10-18 | 0.85 | README does not name WCO explicitly (the paper does) |
| CLAIM-kuzu-06 | Kùzu (CIDR 2023 TR) | node properties in column files; edges double-indexed in CSR; edge properties in parallel CSR; PK hash index; buffer manager with 4 KB pages, GClock | Officially documented (peer-reviewed paper) | Feng, Jin, Chen, Liu, Salihoğlu, "KÙZU Graph Database Management System", CIDR 2023 — https://vldb.org/cidrdb/2023/kuzu-graph-database-management-system.html ; TR https://cs.uwaterloo.ca/~ssalihog/papers/kuzu-tr.pdf | 2023-01 / 2026-10-18 | 0.85 for the 2023 design; may differ in 0.11 | none found |
| CLAIM-kuzu-07 | Kùzu (CIDR 2023) | ASP-Join (accumulate-semijoin-probe, 3 pipelines, sideways information passing) is the core join; the multiway WCO join extends ASP-Join by intersecting adjacency lists | Officially documented (paper) | same as CLAIM-kuzu-06 | 2023 / 2026-10-18 | 0.85 | none |
| CLAIM-kuzu-08 | Kùzu (CIDR 2023) | WAL; serializable by allowing one writer concurrent with multiple readers; multi-writer MVCC on the roadmap | Officially documented (paper) | same as CLAIM-kuzu-06 | 2023 / 2026-10-18 | 0.8 (state in 2023) | later versions UNVERIFIED |
| CLAIM-kuzu-09 | Kùzu (CIDR 2023) | parser → binder → logical plan → DP join optimiser with filter push-down → physical plan | Officially documented (paper) | same | 2023 / 2026-10-18 | 0.8 | none |
| CLAIM-kuzu-10 | docs.kuzudb.com | documentation host did not resolve (getaddrinfo ENOTFOUND) | Reproduced by our experiment (single fetch) | https://docs.kuzudb.com/concurrency/ | — / 2026-10-18 | 0.6: could be transient | none |
| CLAIM-kuzu-11 | Kùzu Inc. | Apple acqui-hired the team, reportedly confirmed by an EC filing about 4 months after the archive | Third-party report | gdotv, "Kuzu's Legacy and the New Wave of Embedded Graph Databases" — https://gdotv.com/blog/kuzu-legacy-embedded-graph-database-landscape/ | 2026-05-28 / 2026-10-18 | 0.45: primary filing not located | none |
| CLAIM-kuzu-12 | LadybugDB | repo LadybugDB/ladybug, MIT, "formerly known as Kuzu", 6,697 commits, 1.9k stars; releases v0.21.2 (01 Oct), v0.21.1 (30 Sep), v0.21.0 (29 Sep) | Officially documented | https://github.com/LadybugDB/ladybug ; https://github.com/LadybugDB/ladybug/releases | 2026 / 2026-10-18 | 0.75: year inferred from asset timestamps | none |
| CLAIM-kuzu-13 | LadybugDB | created and announced by Arun Sharma as a community fork intended as a 1:1 Kùzu replacement; later called the "definitive fork", with 20+ releases and 80+ contributors | Third-party report | gdotv, The Weekly Edge, 24 Oct 2025 — https://gdotv.com/blog/weekly-edge-kuzu-forks-duckdb-graph-cypher-24-october-2025/ | 2025-10-24 (with a later editor's note) / 2026-10-18 | 0.55 | ArcadeDB (a competitor) calls the forks unfunded experiments — CLAIM-kuzu-17 |
| CLAIM-kuzu-14 | Bighorn | Kineviz/bighorn, MIT, no releases; described as unmaintained | Third-party report plus repo page | https://github.com/Kineviz/bighorn ; gdotv (as CLAIM-kuzu-13) | — / 2026-10-18 | 0.5 | none |
| CLAIM-kuzu-15 | RyuGraph | predictable-labs/ryugraph, MIT, maintained by Predictable Labs Inc.; crate releases up to 25.9.2 (Dec 2025) | Officially documented (repo) plus package index | https://github.com/predictable-labs/ryugraph ; https://lib.rs/crates/ryugraph | 2025-12 / 2026-10-18 | 0.6: 2026 activity unverified | none |
| CLAIM-kuzu-16 | Vela Partners fork | "374x faster than Neo4j", concurrent writes | Unverified (vendor blog, no workload or hardware) | https://vela.partners/blog/kuzudb-ai-agent-memory-graph-database | — / 2026-10-18 | 0.2: marketing | none |
| CLAIM-kuzu-17 | ArcadeDB on the forks | forks are "early-stage experiments with no funding, no core team, and no roadmap" | Third-party report (competitor marketing) | https://arcadedb.com/blog/from-kuzudb-to-arcadedb-migration-guide/ | — / 2026-10-18 | 0.25: biased source | contradicted by the activity in CLAIM-kuzu-12 |
| CLAIM-kuzu-18 | LadybugDB | new features: multiple labels per node, attaching external databases, subgraph support | Third-party report | gdotv (as CLAIM-kuzu-11) | 2026-05-28 / 2026-10-18 | 0.5 | none |

## Appendix D — Assumptions

- A-kuzu-1: "Kùzu and successors/forks" means Kùzu v0.11.3 plus its forks. LadybugDB is evaluated as the live continuation, and no separate ADD entry is proposed.
- A-kuzu-2: The 2023 paper design is assumed to be broadly representative of v0.11.3 storage. Differences are flagged as hypotheses.
- A-kuzu-3: The 2026 year for the LadybugDB releases is inferred from asset timestamps on the releases page.
- A-kuzu-4: Performance targets in §12 and §14 are acceptance thresholds we set, not measured results.
