# C04 — Zingg (ML entity resolution on Spark)

| Field | Value |
|---|---|
| Registry ID | T-C04-zingg |
| Tier | A — OSS ML entity resolution; REUSE/INTEGRATE candidate for the verified gap BL-36 (probabilistic ER absent); **AGPL-3.0 is a legal-review trigger** |
| Versions examined | Zingg Community 0.7.0 (GitHub release 2026-08-10, commit `21f54e9`), 0.6.0 (2026-04-28), 0.5.0 (2025-07-02), 0.4.0 (2024-01-01) |
| Verified on | 2026-10-26 (actual access date; brief says 2026-10-18 — see Appendix D) |
| Worker | W12 (batch V02) |

## 1. Identity, current status, tier, and sources

**Identity.** Zingg is an entity-resolution and master-data tool built by Zingg.AI (founder Sonal Goyal; repository `zinggAI/zingg`, created 2021-08-25). It runs on Apache Spark (Java/Scala core, Python API) and is distributed as **Zingg Community** (open source) and **Zingg Enterprise / Enterprise Lite** ("the suite of proprietary products licensed by Zingg"). [CLAIM-zingg-01] [CLAIM-zingg-06]

**Licence (verified).** The repository `LICENSE` is the GNU **Affero** General Public License v3 (SPDX AGPL-3.0); the GitHub API agrees. [CLAIM-zingg-01] Several features documented in the same docs tree are marked "Zingg Enterprise Feature" and are proprietary. [CLAIM-zingg-05]

**Status.** Active: last push 2026-10-19, not archived, about 1.26 k stars; releases roughly every 3–10 months (0.4.0 Jan 2024 → 0.5.0 Jul 2025 → 0.6.0 Apr 2026 → 0.7.0 Aug 2026). [CLAIM-zingg-02] 0.7.0 is a maintenance release: GraphFrames 0.10.0 → 0.11.0, Docker base `apache/spark:3.5.5-python3`, error-handling fixes, notebook reorganisation. 0.6.0 added Databricks Unity Catalog via `UCPipe`, Spark 3.5.5 and GraphFrames 0.10.0. [CLAIM-zingg-03]

**Traps.** "Zingg" also names unrelated projects; the registry means `zinggAI/zingg`. Documentation and some blog posts describe Enterprise features as if part of "Zingg"; the Community feature set is smaller (see §3). Cross-reference: `C04-splink.md` (permissive FS-based ER, primary REUSE) and `C04-senzing.md` (commercial real-time ER).

**Sources (12):** GitHub repo, LICENSE, releases API, README, `pom.xml`, source at tag `v0.7.0` (shallow clone); docs.zingg.ai pages (index, models, hardware sizing, telemetry, security, incremental, deterministic, explain, approval, reassign, verifyBlocking, scoring, link, match); zingg.ai edition comparison page.

## 2. Primary problem, target workloads, concrete example workflows

Deduplicate and link customer, patient, supplier, product or organisation records across silos at millions-of-records scale with minimal labelling. [CLAIM-zingg-04] Example EOIP workflow: export Workday, ServiceNow and Jira user tables to Parquet; configure fields (`fname`, `lname`, `email`, `dept`) with match types; run `findTrainingData` → `label` (≈ dozens of pairs) → `train` → `match`; ingest the `z_cluster`, `z_minScore`, `z_maxScore` output as `IdentityCandidate`s into the review queue (BL-35) instead of auto-merging. Second workflow: `link` phase to match a duplicate-free HR master against a duplicate-free CMDB owner list. [CLAIM-zingg-05]

## 3. Feature inventory

| Feature | Community | Enterprise | CLAIM |
|---|---|---|---|
| Interactive active-learning labelling (`findTrainingData`, `label`, `updateLabel`) | present | present | 05 |
| Learned blocking model + learned similarity classifier (`train`) | present | present | 04 |
| `match` (dedupe), `link` (cross-dataset) | present | present | 05 |
| Pre-trained / example models (Febrl) | present | present | 04 |
| Custom blocking and similarity functions, stopwords, pass-through | present | present | 04 |
| Python API (community), Python Enterprise APIs (ZinggEC/ZinggES) | present / enterprise | | 05 |
| Incremental flow (`runIncremental`) with persistent ZINGG_ID, merge/unmerge on update | absent | enterprise-only | 05 |
| Deterministic matching in the same flow | absent | enterprise-only | 05 |
| `verifyBlocking`, `explainOutput` (pair-level evidence), `reassignZinggId`, model diff | absent | enterprise-only | 05 |
| Cluster approval workflow | "Coming Soon" | enterprise | 05 |
| Native Snowflake execution | absent | enterprise-only | 06 |
| Connectors: files, Parquet, JDBC (Postgres, MySQL), S3, Cassandra, MongoDB, Neo4j, BigQuery, Exasol, Databricks, Fabric | present (Spark pipes) | present | 06 |
| Web UI | absent (CLI + notebooks) | UNVERIFIED | 05 |
| Real-time/online matching | absent | "Batch, Real Time" listed in edition matrix, details UNVERIFIED | 06 |
| Survivorship / golden-record rules | not documented in pages read | UNVERIFIED | — |
| Merge/split history, tenant isolation, ACLs | absent | absent/UNVERIFIED | — |

## 4. Architecture diagram

```
 sources (CSV/Parquet/JDBC/S3/Mongo/Neo4j/BigQuery/Snowflake*)   *enterprise
        │  Zingg pipes (Spark DataFrame readers)
        ▼
 ┌────────── Spark driver + executors (local[*] or cluster) ───────────┐
 │ preprocess (stopwords, field types) ─ sampling                       │
 │ findTrainingData: active learning picks edge-case pairs ─► label CLI │
 │ train:  blocking tree (hash fns, Canopy/Tree) + LogisticRegression    │
 │         → model dir  zinggDir/modelId/{model,blocks,trainingData}    │
 │ match:  block → pair → features → classifier → edge list             │
 │         → GraphFrames connectedComponents → z_cluster, scores        │
 └──────────────────────────────────────────┬──────────────────────────┘
                                            ▼
                    output sink (same pipes); telemetry → Google Analytics (default on)
 Control: JSON/Python config, phases via zingg.sh; state = files in zinggDir
```

## 5. Under-the-hood reconstruction

Source read at tag `v0.7.0` (commit `21f54e9`); modules `common/core`, `spark/core`, `scala`, `python`.

**Data model.** Tabular records with a field-definition list: `fieldName`, `dataType`, `matchType` (e.g. `FUZZY`, `EXACT`, `NUMERIC`, `EMAIL`, `PINCODE`, `DONT_USE`, combinations comma-separated). Source codes for these live in `common/client/.../MatchTypes.java` and similarity functions under `common/core/.../similarity/function` (Jaro-Winkler, affine gap, Jaccard, bigram Jaccard, numbers Jaccard, email, pincode, product code, set membership). [CLAIM-zingg-04]

**Blocking (learned).** `common/core/.../block/Block.java`, `Tree.java`, `Canopy`: from labelled duplicate pairs and sampled data, Zingg greedily builds a **tree of hash functions** (library under `.../hash`: first/last N chars, last word, rounding, trim-last-digits, range, null checks) choosing at each node the function that best splits records while keeping known duplicates together, bounded by a maximum block size. This is the "auto-learned blocking model"; maintainers state typical comparisons are 0.05–1% of the possible pairs. [CLAIM-zingg-04] Pseudocode (reconstructed from names and docs, *hypothesis* on tie-breaking):

```
grow(node, records, dupes):
   best = argmax over (field, hashFn) of  elimination(records) subject to dupesKept(dupes) high
   if size(best.child) > maxSize: grow(child, ...)      # recurse on oversized leaves
```

**Similarity model.** `spark/core/.../model/SparkModel.java` builds a feature vector per pair (per-field similarity scores through `VectorAssembler`) and trains Spark ML **LogisticRegression** (`setMaxIter(100)`, cross-validated `regParam` grid 1e-4…1). The docs call the result a curve fit with an automatically chosen threshold, so scores below 0.5 can still be matches. [CLAIM-zingg-04]

**Clustering.** `common/core/.../util/GraphUtil.java` and `SparkGraphUtil.java` build a GraphFrame from accepted pair edges and call `connectedComponents()`. Transitive closure over pair decisions means one weak edge can chain two large clusters (a generic risk of connected-components ER; *inference*, see INV-zingg-03). [CLAIM-zingg-04]

**Active learning.** `findTrainingData` selects "edge cases" (uncertain pairs) and `label` collects yes / no / can't-say answers; the loop repeats; labels can be edited (`updateLabel`) and documented. Selection algorithm details: not read at source level (UNVERIFIED). [CLAIM-zingg-05]

**State and versioning.** All state is files under `zinggDir/modelId`: trained model, blocking tree, labelled pairs. Community `match` recomputes clusters over the full input; persistent identifiers, merge/unmerge and re-assignment need Enterprise (`runIncremental`, `reassignZinggId`). [CLAIM-zingg-05]

**Concurrency/partitioning.** Delegated to Spark (partitions, shuffles for blocking joins). No transactions. **Security.** No ACL or tenant concept; privacy statement: data stays in the deployment, but anonymous usage metrics (record count, field count, domain, user id, JDK/OS, execution time) go to Google Analytics unless `collectMetrics=false`. [CLAIM-zingg-09]

## 6. Functional and non-functional requirements inferred

| ID | Requirement an EOIP ER layer must satisfy to be comparable |
|---|---|
| FR-1 | Learn from ≤ 100 labelled pairs via an active-learning loop |
| FR-2 | Learn or derive blocking automatically with bounded comparisons |
| FR-3 | Output cluster id plus min/max pair scores; keep pair evidence |
| FR-4 | Stable persistent IDs and merge/unmerge on incremental data (Enterprise parity) |
| FR-5 | Deterministic + probabilistic in one flow |
| NFR-1 | Run on one node (Spark local mode documented for up to a few million records) [CLAIM-zingg-08] |
| NFR-2 | No mandatory network: telemetry off |
| NFR-3 | Redistribution-safe licence for any shipped component |

## 7. Performance and resource model

Maintainer-published sizing (not independent benchmarks): 120 k Febrl records ≈ 5 min on a 4-core, 10 GB local Spark; 5 M North Carolina voters ≈ 4 h on 4 cores/10 GB; 9 M records × 3 fields ≈ 45 min on AWS m5.24xlarge (96 cores, 384 GB); "80 M records, 8–10 fields, < 2 h" on a 1 + 8 node cluster is labelled user-reported and unoptimised. [CLAIM-zingg-08] CI workflows run Febrl120K and ncVoters5M performance tests, so numbers are re-measurable. Accuracy figures: none independently found (UNVERIFIED). Failure modes (docs): a poorly learned blocking model makes jobs slow or non-terminating (causes: skewed or unrepresentative training data, many null columns, too few labels); the guard tool `verifyBlocking` is Enterprise-only. [CLAIM-zingg-05] Memory: Spark heap; JVM start-up cost makes small batches inefficient. Java compile target is 11; Spark profiles 3.4.0 and 3.5.5, Scala 2.12. [CLAIM-zingg-03]

## 8. Strengths and use-case-specific advantages

| ID | Strength | Match or exceed |
|---|---|---|
| S1 | Few labels via active learning, aimed at non-statisticians | Match; exceed by feeding BL-35 reviewer decisions back as labels |
| S2 | Learned blocking at multi-million scale | Match pattern with profiler-driven blocking (BL-26 stats) |
| S3 | Spark scale-out to tens of millions | Do not rebuild; DuckDB first, Spark profile optional |
| S4 | Persistent ZINGG_ID, incremental merge/unmerge (Enterprise) | Exceed: EOIP identity ledger with bitemporal history (BL-37) |
| S5 | Pair-level explanation of clusters (Enterprise) | Match with open evidence records (BL-41) |
| S6 | Multi-language fields (Chinese, Thai, Japanese, Hindi per README) | Test with local-model embeddings later |

## 9. Limitations with root causes

| Type | Limitation | Root cause |
|---|---|---|
| Licensing | AGPL-3.0 core; production-grade incremental, explain, deterministic, approval gated to proprietary Enterprise | Open-core split [CLAIM-zingg-01,06] |
| Algorithmic | Connected components can over-merge; threshold chosen automatically; LR on per-field similarity ignores field correlation | Design (inference) |
| Algorithmic | Blocking learned once; drift or skew silently degrades runtime | Learned hash tree |
| Operational | Spark/JVM footprint even for 100 k records; Java 11 build, Spark 3.4/3.5 pins; Scala 2.12 | Platform choice |
| Operational | Default telemetry to Google Analytics | Product analytics [CLAIM-zingg-09] |
| Friction | Community has no persistent IDs; reruns recluster everything; no UI; approval "coming soon" | Feature gating |
| Friction | Field-type model is flat/tabular: no graph-relational evidence (shared neighbours) | Data model |
| Unknown | Accuracy vs Splink/Senzing on identical data; labelled-pair requirements | No independent benchmark found |

## 10. Deployment, licensing, redistribution, operational viability

Run modes: Docker image (`zingg/zingg`), local Spark, Spark clusters, Databricks, Fabric, AWS/Azure; Snowflake native is Enterprise. One-node: yes in Spark local mode (docs suggest it for up to a few million records). Air-gap: viable (CPU-only, no model downloads in the core flow; no pretrained neural embedding in Community) **provided telemetry is disabled and dependencies are mirrored**. [CLAIM-zingg-08,09]

**Legal-review triggers (record, no conclusions):** (1) AGPL-3.0 on the Community code, models and example assets in the repo; AGPL §13 network-use clause and "combined work" questions arise if EOIP ships Zingg inside its image, links its jars, or modifies it and exposes it as a service. (2) Enterprise is proprietary with its own terms, pricing not published in pages read. (3) Redistribution of trained models derived from customer data under AGPL tooling is unclear. (4) Third-party licences (Spark, GraphFrames, Hadoop) not audited here. Safest architectural posture for EOIP: customer-installed, process-isolated batch job invoked via CLI with file/Parquet hand-off, never linked, never vendored — the same posture `rdf_backend.py` documents for GPL/AGPL RDF servers. Whether process isolation is sufficient for a white-label product is a question for counsel.

## 11. Competitive delta against the EOIP verified baseline

| Area | EOIP | Zingg | Delta |
|---|---|---|---|
| BL-34 deterministic identity | Person identity only, email key (`identity/resolver.py:49`) | Probabilistic any-entity; deterministic only in Enterprise | EOIP's deterministic first pass is a valid complement |
| BL-35 review queue | Partial: candidate with `match_basis`, `confidence`, PENDING/CONFIRMED/REJECTED (`identity/candidates.py:26`) | Community: none; approval "coming soon" | EOIP ahead on governance semantics |
| BL-36 probabilistic ER | Absent | Learned blocking + LR + clustering | Largest delta |
| BL-26 profiler | Implemented key detection, stats | Manual field config | EOIP can auto-propose blocking fields |
| BL-37 bitemporal, BL-41 evidence | Implemented | Enterprise ID reassignment only | EOIP ahead if wired to ER |
| BL-18/20 ACL, tenancy | Absent / contract | none | Both lack; ER across tenants would leak |
| Language/runtime | Python 3.11 locked, no numpy | JVM + Spark | Heavy dependency for one-node Python product |

[CLAIM-zingg-10] records the baseline dependency facts used. Compared with Splink (`C04-splink.md`): Splink is permissive, SQL-portable, additive explainable weights, no active learning; Zingg is AGPL, Spark-bound, has active learning and learned blocking. Compared with Senzing (`C04-senzing.md`): real-time and principle-based, commercial.

## 12. Strength-adoption cards and Con-to-Pro inversion cards

| STR-ID | Competitor | Strength | Evidence | Value | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-zingg-01 | Zingg | Frugal active-learning labelling | 05 | ER without a data-science team | match / exceed | Uncertainty sampling over candidate pairs presented in the BL-35 queue; reviewer verdicts become labels | F1 ≥ baseline with ≤ 50 labels on Febrl120k |
| STR-zingg-02 | Zingg | Learned blocking | 04 | Bounded comparisons | match | Derive blocking keys from labelled dupes + profiler stats; report pairs/n² | Pairs ≤ 1 % of n², blocking recall ≥ 0.98 |
| STR-zingg-03 | Zingg | Stable cluster ID with merge/unmerge (Enterprise) | 05 | Downstream stability | exceed | Identity ledger with bitemporal assignments; reassign preserves IDs | Re-run after model change keeps ≥ 95 % of IDs |
| STR-zingg-04 | Zingg | Pair-level explanation | 05 | Review trust | match | Store pair scores and feature contributions as evidence | Every cluster edge has a retrievable explanation |
| STR-zingg-05 | Zingg | Deterministic + probabilistic single flow | 05 | Precision on strong identifiers | match | BL-34 first pass, probabilistic second pass | No regression on exact-key matches |

**INV-zingg-01 — Open-core split and AGPL core.** Target: Zingg 0.7.0 Community. Limitation: incremental, explain, deterministic, approval, verifyBlocking are Enterprise [CLAIM-zingg-05]. Root cause: licensing (*proven*). Alternative: build the incremental ledger and explanation in EOIP around a permissive scorer (Splink, MIT per C04-splink) — worse if Zingg's learned-blocking accuracy proves materially better. Options: (1) quick: process-isolated Zingg batch job behind legal approval; (2) native: scorer-agnostic `eoip.identity.prob` port (Splink default, Zingg optional) plus ledger; (3) long-term: own active-learning module. Select (2). Sketch: `IdentityScorer.score(batch)->edges[{a,b,p,evidence}]`; ledger `cluster(id, members, valid_from, tx_from, decision)`. POC: same data through Zingg 0.7.0, Splink and BL-34; metrics pairwise precision/recall/F1, cluster purity, runtime, RAM on 8 cores/16 GB; baseline BL-34 (email only). Dependencies: BL-35, BL-37; failure case: cross-tenant block keys. Defensibility: ledger + governance are the moat, scorer is swappable. Decision: **ADOPT** (port) / **EXPERIMENT** (Zingg adapter).

**INV-zingg-02 — Spark footprint on a one-node product.** Root cause: deployment/coupling (*proven* by §5, §7). Alternative: DuckDB/Arrow in-process blocking and scoring; worse above ~10 M records. Options: (1) Spark local mode in a sidecar; (2) native DuckDB path; (3) optional Spark profile for large tenants. Select (2). POC: 1 M records, wall-clock and peak RSS vs Zingg local[8] (baseline from [CLAIM-zingg-08]). Decision: **EXPERIMENT**.

**INV-zingg-03 — Silent blocking drift and chaining.** Root cause: algorithm (learned blocking tree *proven*; chaining *hypothesis*). Alternative: surface block-size histograms and cluster-diameter checks in the open layer; require review for clusters with a bridge edge below threshold. POC: inject 1 % noisy bridge records into Febrl120k; metric false-merge rate with and without bridge guard. Decision: **ADOPT** (guardrail cheap).

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-31 probabilistic ER | REUSE Splink first; INTEGRATE Zingg optionally (process-isolated, legal gate) | INV-zingg-01 |
| CAP-31 merge/split + survivorship | BUILD | Not in Community |
| CAP-30 deterministic keys | BUILD (extend BL-34) | Needed before probabilistic pass |
| Active learning for labelling | EXPERIMENT | STR-zingg-01 |
| Learned blocking | EXPERIMENT (pattern) | STR-zingg-02 |
| Pair-level explanation | BUILD | CAP-24/38 |
| Spark runtime | DEFER | INV-zingg-02 |
| Enterprise edition | REJECT as dependency | Proprietary, undisclosed terms |
| CAP-50 air-gap | n/a | Telemetry off required |

## 14. Concrete tests, proof-of-concept, and acceptance conditions

All PROPOSED. T1: run Zingg 0.7.0 Docker on `examples/febrl120k`, record F1 against ground truth, runtime and RAM on the target one-node box. T2: ablate labels (20/50/100) for the active-learning curve. T3: compare with Splink and BL-34 on a synthetic enterprise people set (Jira/ServiceNow/Workday-style, with tenant tags). T4: confirm no outbound traffic with `collectMetrics=false` (packet capture). T5: blocking guard test (INV-zingg-03). T6: AGPL review package: file inventory of what would ship, for counsel. Acceptance for adopting any ER engine: pairwise F1 ≥ 0.90 at ≤ 1 % pair budget, explanation per edge, zero cross-tenant pairs, reviewer verdicts persisted.

## 15. Risks, trade-offs, and open research questions

Risks: AGPL contamination arguments; Enterprise gating of the features EOIP needs most; maintainer-run benchmarks; JVM/Spark ops cost; over-merging in connected components; pretrained model provenance. Open: algorithm used to select active-learning pairs; accuracy on enterprise-identity data; whether a Python-callable API avoids Spark for small data; Enterprise pricing and OEM terms; dataset licences for Febrl and NC Voters examples.

---

## Appendix A — Research-dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | AGPL-3.0, Zingg.AI, 0.7.0 |
| D2 | 2 | Customer/patient/supplier ER |
| D3 | 4 | Spark pipeline, pipes |
| D4 | 5 | Files in zinggDir; no index store |
| D5 | N/A | No schema semantics beyond field types |
| D6 | N/A | Not a query engine |
| D7 | N/A | No reasoning |
| D8 | 5, 7 | Spark partitions; no transactions |
| D9 | 3 | Pipes/connectors, incremental (EE) |
| D10 | 3, 5, 9 | Core topic: blocking, scoring, clusters |
| D11 | 3, 9 | Persistent IDs only in EE |
| D12 | 5 | Logistic regression; no GNN |
| D13 | N/A | No retrieval |
| D14 | N/A | None |
| D15 | 3 | Labelling CLI, approval planned |
| D16 | 3 | No UI |
| D17 | 3 | Python API, config JSON |
| D18 | 5, 9 | Telemetry, no ACL |
| D19 | 11 | No tenancy |
| D20 | 7 | Maintainer numbers |
| D21 | 1, 10 | Open-core |
| D22 | 3 | Parquet/JDBC; no RDF |
| D23 | N/A | No patent search |
| D24 | App C | Source at tag plus docs |

## Appendix B — Capability mapping

| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | native (scoring, clustering); EE for IDs | 04,05 | BL-36 Absent, BL-35 Partial | REUSE/INTEGRATE | P1 |
| CAP-30 | enterprise-only | 05 | BL-34 Implemented (person) | BUILD | P1 |
| CAP-28 | absent | — | BL-26 | n/a | — |
| CAP-24 | enterprise-only | 05 | partial | BUILD | P2 |
| CAP-38 | enterprise-only (pair evidence) | 05 | BL-41 | BUILD | P2 |
| CAP-50 | partial (telemetry default on) | 09 | — | INTEGRATE with flag | P1 |
| CAP-77 | AGPL/EE | 01,06 | BL-22 | DEFER to legal | P1 |

## Appendix C — Evidence records

| CLAIM-ID | Product/version/date | Exact claim | Class. | Source | Pub./access | Confidence | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-zingg-01 | Zingg main | LICENSE is GNU AGPL v3; GitHub SPDX AGPL-3.0 | Observed in source code | github.com/zinggAI/zingg `LICENSE`; GitHub API | 2026-10 / 2026-10-26 | 0.95 | none |
| CLAIM-zingg-02 | repo | Created 2021-08-25; pushed 2026-10-19; not archived; releases v0.7.0 2026-08-10, v0.6.0 2026-04-28, v0.5.0 2025-07-02, v0.4.0 2024-01-01 | Officially documented | GitHub API/releases | 2026-10 / 2026-10-26 | 0.9 | none |
| CLAIM-zingg-03 | 0.6.0, 0.7.0 | 0.7.0: GraphFrames 0.11.0, Spark 3.5.5 Docker base; 0.6.0: Unity Catalog `UCPipe`, Spark 3.5.5; `pom.xml` Spark profiles 3.4.0/3.5.5, Scala 2.12, Java source/target 11 | Officially documented + Observed in source code | GitHub release notes; `pom.xml` @v0.7.0 | 2025-04, 2026-08 / 2026-10-26 | 0.9 | none |
| CLAIM-zingg-04 | 0.7.0 | Learned blocking tree (`Block.java`, `Tree.java`, hash fns), LogisticRegression similarity (`SparkModel.java`, maxIter 100, regParam grid), GraphFrames `connectedComponents` (`GraphUtil.java`); maintainers say comparisons are 0.05–1 % of pairs | Observed in source code + Officially documented | source @v0.7.0; docs.zingg.ai/latest/zmodels | 2026 / 2026-10-26 | 0.85 (0.05–1 % is a maintainer claim, Unverified) | none |
| CLAIM-zingg-05 | docs v0.7 | Phases and features; Enterprise-only: runIncremental, deterministic matching, verifyBlocking, explainOutput, reassignZinggId, approval ("Coming Soon"); community `link` and `match`; poorly learnt blocking can stall jobs | Officially documented | docs.zingg.ai/latest/stepbystep/* and explainoutput | 2026 / 2026-10-26 | 0.85 | none |
| CLAIM-zingg-06 | editions | Enterprise is a suite of proprietary products; Community / Enterprise Lite / Enterprise matrix; Snowflake native run is Enterprise | Officially documented | zingg.ai compare-versions page; docs install pages | 2026 / 2026-10-26 | 0.7 (matrix columns garbled in extraction) | none |
| CLAIM-zingg-07 | docs | Connectors and platforms (Databricks, Fabric, Snowflake, JDBC, S3, Cassandra, MongoDB, Neo4j, BigQuery, Exasol, Parquet) | Officially documented | docs.zingg.ai/latest/llms.txt index | 2026 / 2026-10-26 | 0.85 | none |
| CLAIM-zingg-08 | docs | Sizing: 120 k in 5 min, 5 M in ~4 h (4 cores/10 GB); 9 M in 45 min (m5.24xlarge); 80 M < 2 h user-reported; single machine OK for a few million | Third-party report (maintainer docs) | docs.zingg.ai/latest/stepbystep/hardwaresizing | 2026 / 2026-10-26 | 0.5 | no independent run |
| CLAIM-zingg-09 | docs | `collectMetrics` default true, writes usage metrics to Google Analytics; no input data captured (maintainer statement) | Officially documented | docs.zingg.ai telemetry and security pages | 2026 / 2026-10-26 | 0.85 | no traffic capture done |
| CLAIM-zingg-10 | EOIP dev_local | Baseline: BL-34 person-only email key, BL-35 partial, BL-36 absent; lock has no numpy | Observed in source code | `01-SYSTEM-BASELINE.md` §5 BL-34..36; `identity/resolver.py:49` | 2026-10-18 / 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions

1. Access date 2026-10-26 (not the brief's 2026-10-18).
2. The edition matrix on zingg.ai was read as: Community = batch probabilistic; Enterprise Lite/Enterprise add incremental, deterministic, explainability; feature-level doc footnotes were preferred over the garbled matrix.
3. Active-learning selection strategy, accuracy and survivorship behaviour were not verified at source level.
4. No licence conclusions are drawn; all AGPL and Enterprise-terms items are flagged for counsel.
5. Spark, GraphFrames and Hadoop dependency licences were not checked.
