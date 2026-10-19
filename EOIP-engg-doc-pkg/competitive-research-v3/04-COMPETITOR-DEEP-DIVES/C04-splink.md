# C04 — Splink (probabilistic record linkage, Ministry of Justice UK)

| Field | Value |
|---|---|
| Registry ID | T-C04-splink |
| Tier | A — OSS probabilistic record linkage; primary REUSE candidate for the verified EOIP gap BL-36 (probabilistic ER absent) |
| Versions examined | Splink **5.0.0** (PyPI upload 2026-09-28; GitHub release page dated "18 Sep") and maintained 4.x line **4.0.17** (2026-09-03). Source read at tag `v5.0.0`: `splink/internals/expectation_maximisation.py`, `comparison_level.py`, `blocking.py`, `estimate_u.py`, `predict.py`, `connected_components.py`, `clustering.py`, `database_api.py`. |
| Verified on | 2026-10-18 |
| Worker | W12 |

## 1. Identity, current status, tier, and sources

**Identity.** Splink is a Python library for probabilistic record linkage (deduplicating and linking records that have no shared reliable key). The UK Ministry of Justice (MoJ) Analytical Services develops it in the open at `github.com/moj-analytical-services/splink`, and it is distributed on PyPI as `splink` [CLAIM-splink-01][CLAIM-splink-02]. There is no name collision in this domain. The R package `irelink` is an independent third-party port that documents a mapping to Splink 5 functions; it is not Splink [CLAIM-splink-21].

**Status.** Active. 5.0.0 is the current major release. PyPI shows the upload on 2026-09-28. The GitHub release page shows "18 Sep", which is the PyPI date of `5.0.0.dev5`. PyPI is taken as authoritative [CLAIM-splink-02]. The 4.x line still gets maintenance releases (4.0.17 on 2026-09-03; 4.0.0 was 2024-07-24) [CLAIM-splink-03]. Pre-releases ran from 5.0.0.dev1 (2025-12-17) to dev5. Cadence: roughly monthly patch releases and a major release about every two years.

**Licence.** MIT, copyright 2020 Ministry of Justice [CLAIM-splink-01]. PyPI metadata also says MIT [CLAIM-splink-02].

**Governance.** Government-owned OSS with one dominant maintainer organisation. The MoJ Algorithmic Transparency Recording Standard (ATRS) record, dated 2025-10-06, documents production use [CLAIM-splink-16].

**Tier A reason.** Probabilistic ER is a verified EOIP gap: BL-36 is Absent, BL-34 covers deterministic person identity only, and BL-35 is a partial review queue. Splink is the leading permissively licensed, SQL-portable Fellegi–Sunter implementation.

**Sources (12):** licence file; PyPI history and 5.0.0 page; GitHub releases; v5.0.0 release notes; docs home; Fellegi–Sunter guide; training-rationale guide; term-frequency guide; source files at `v5.0.0`; MoJ ATRS record; `irelink` guide (third party). All accessed 2026-10-18.

## 2. Primary problem, target workloads, concrete example workflows

**Problem.** Link or deduplicate records about the same real-world entity when records contain typos, missing values or format differences and share no identifier. Splink does this without labelled training data [CLAIM-splink-05][CLAIM-splink-09].

**Workloads.** Batch deduplication and linkage of millions to hundreds of millions of rows in an analytical SQL engine, government statistical linkage, and master-person-index construction. MoJ runs it in both batch and real time: weekly refreshes of linked datasets, finding probation records for people arriving at court, a Core Person Record pilot (unique person ID) and a police-number lookup pilot [CLAIM-splink-16].

**Workflow (Splink 5, from docs and release notes):**
1. Register inputs as `SplinkDataFrame`s with a backend `db_api` (DuckDB, Spark, PostgreSQL or SQLite) [CLAIM-splink-15][CLAIM-splink-21].
2. Declare settings:
   - link type: dedupe / link_only / link_and_dedupe;
   - comparisons, each an ordered list of levels (exact, Jaro-Winkler ≥ 0.9, Levenshtein ≤ 2, else);
   - prediction blocking rules.
3. Train in three steps [CLAIM-splink-09]:
   - λ from deterministic rules plus a recall guess;
   - u from random pairs, capped by `max_pairs`;
   - m by EM over several blocking passes.
4. Predict: blocked pairs → comparison vectors γ → summed log2 Bayes factors plus TF adjustments → `match_weight` and `match_probability` [CLAIM-splink-08][CLAIM-splink-11].
5. Cluster: connected components at one or more thresholds [CLAIM-splink-13].
6. Explain and QA with waterfall charts, m/u charts and cluster studio [CLAIM-splink-17].
7. Score new records against an existing table with `predict_between` / `score_pair(s)`. `find_matches_to_new_records` was removed in 5.0 [CLAIM-splink-15].

**EOIP workflows.**
- (a) Cross-source person identity: Jira users, GitHub accounts, Confluence authors, ServiceNow callers, HRIS and directory accounts, where email is missing or differs (J9, J2).
- (b) Vendor and organisation deduplication (J15).
- (c) System and application names across CMDB, repositories and catalogues ("payments-svc" vs "payment-service").

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Model | Fellegi–Sunter, log2 Bayes factors, prior λ | Present | [CLAIM-splink-08] |
| Model | Unsupervised training | Present | [CLAIM-splink-09] |
| Model | EM for m, random sampling for u | Present | [CLAIM-splink-10][CLAIM-splink-14] |
| Model | Term-frequency adjustment | Present | [CLAIM-splink-11] |
| Model | Active learning / labelling UI | Absent | [CLAIM-splink-18] |
| Comparisons | Exact, Jaro-Winkler, Levenshtein, dates, cosine (Spark cosine new in 5.0) | Present | [CLAIM-splink-15] |
| Blocking | Multi-rule duplicate-free union, exploding array rules | Present | [CLAIM-splink-12] |
| Blocking | Salting | Removed in 5.0 (chunking replaces it) | [CLAIM-splink-15] |
| Scale | Chunked prediction, pair-count estimation | Present (5.0) | [CLAIM-splink-15] |
| Backends | DuckDB (default), Spark, PostgreSQL, SQLite | Present | [CLAIM-splink-05][CLAIM-splink-23] |
| Backends | Athena | Removed in 5.0 | [CLAIM-splink-15][CLAIM-splink-23] |
| Clustering | SQL connected components, multi-threshold | Present | [CLAIM-splink-13] |
| Identity | Persistent IDs, merge/split history, survivorship | Absent | [CLAIM-splink-18] |
| Incremental | New-vs-existing scoring | Present (reworked API) | [CLAIM-splink-15] |
| Incremental | Incremental re-clustering | Absent | [CLAIM-splink-18] |
| Explainability | Waterfall, match-weight, m/u charts, cluster studio | Present | [CLAIM-splink-17] |
| Diagnostics | SQL profiling for DuckDB and Spark | Present (5.0) | [CLAIM-splink-24] |
| UI / API | Python library only; no server, REST or review UI | — | [CLAIM-splink-05] |
| Security / tenancy | N/A — inherited from the SQL engine | — | Reasoned inference |

## 4. Text-based architecture diagram

```
                     ┌──────────────── Python process (library) ────────────────────┐
 Settings JSON ─────►│ Linker                                                        │
 (comparisons,       │  training : λ (det. rules + recall) · estimate_u (random)     │
  levels, blocking,  │             EM loop over blocked pairs (m)                    │
  TF columns)        │  inference: predict / predict_between / score_pair(s)         │
                     │  clustering: connected components @ threshold(s)              │
                     │  charts   : waterfall, m/u, cluster studio (HTML)             │
                     │       │ SQL strings queued in a CTEPipeline                   │
                     │       ▼                                                       │
                     │  DatabaseAPI (abstract) ─ dialect subclasses                  │
                     └───────┬───────────────┬──────────────┬──────────────┬─────────┘
                             ▼               ▼              ▼              ▼
                       DuckDB (in-proc)    Spark       PostgreSQL       SQLite
 Data plane: inputs → __splink__df_concat_with_tf → blocked id pairs → γ vectors
             → predictions (match_weight, match_probability) → clusters
 Control plane: the caller (notebook / worker / orchestrator). State = SQL tables + model JSON.
```

## 5. Under-the-hood reconstruction

### 5.1 Data model
- **Inputs:** tables with a unique ID, plus `source_dataset` when linking. They are concatenated into `__splink__df_concat_with_tf`. In 5.0 term frequencies are joined at predict time [CLAIM-splink-15].
- **Comparison:** an ordered list of levels. Each level is a SQL boolean with `m_probability` and `u_probability`.
- **γ:** the index of the first level whose condition is true (−1 = null level) [CLAIM-splink-11].
- **Model:** saved as JSON (settings plus trained λ, m, u) [CLAIM-splink-15].

### 5.2 Scoring — verified [CLAIM-splink-08]
```
K_i = m_i/u_i ;  M = log2(λ/(1-λ)) + Σ_i log2 K_i (+ Σ TF adj) ;  Pr(match|γ) = 2^M/(1+2^M)
```
The docs state the conditional-independence assumption and note it is "rarely fully true" [CLAIM-splink-09].

### 5.3 Term-frequency adjustment — verified in source
Location: `comparison_level.py` lines 671–726 at `v5.0.0` [CLAIM-splink-11].
```
u_exact  = u of this comparison's exact-match level
tf       = greatest(coalesce(tf_l,tf_r), coalesce(tf_r,tf_l), tf_minimum_u_value)
M       += tf_adjustment_weight * (log2(u_exact) - log2(tf))   # 0 for null/else levels
```
- Effect: rare values get extra weight and common values ("Smith") lose weight.
- Fuzzy levels use the larger of the two term frequencies.
- EM does not estimate this term because it does not depend on m.

### 5.4 Training — verified
1. **λ.** Derived from deterministic rules plus a recall estimate. A wrong recall guess moves the prior only slightly (docs: a true −14 becomes −13.75 or −14.42) [CLAIM-splink-09].
2. **u.** Estimated from random pairs. `estimate_u.py` lines 301–327 size the sample [CLAIM-splink-14]:
   - dedupe: `rows = 0.5(√(8·max_pairs+1)+1)`;
   - link-only: `proportion = √(max_pairs/total_links)`;
   - counts are accumulated per chunk, with a minimum-count check.
3. **m.** Estimated by EM on pairs from a training blocking rule. Columns inside that rule cannot be estimated in the same pass, so the user runs several passes with different rules and the estimates are combined [CLAIM-splink-09].

EM is in `expectation_maximisation.py` [CLAIM-splink-10]:
```
if estimate_without_term_frequencies:
    P = SELECT γ1..γk, count(*) FROM comparison_vectors GROUP BY γ1..γk   # pattern counts
for i in 1..max_iterations:
    E: p = predict(pattern; λ, m, u)
    M: m[c,l] = Σ_{γc=l} p·cnt / Σ_l Σ p·cnt ;  u[c,l] = Σ_{γc=l}(1-p)·cnt / Σ_l Σ(1-p)·cnt
       keep training_fixed_probabilities; update λ
    break if max|Δθ| < em_convergence
```
- The pattern-count fast path makes each iteration O(distinct γ patterns), not O(pairs).
- 5.0 adds `max_pairs` to cap EM training input [CLAIM-splink-15].

### 5.5 Blocking — verified
- `block_using_rules_sqls` (`blocking.py` line 753) generates one SELECT per rule and joins them with UNION ALL [CLAIM-splink-12].
- Rule *n* sets `match_key = n` and adds `NOT coalesce((rule_j),false)` for every earlier rule *j*. The union is duplicate-free without a global DISTINCT (lines 124–221).
- `ExplodingBlockingRule` handles array columns: it explodes the arrays, materialises ID tables and de-duplicates (lines 333–600).
- With no rules, blocking falls back to `1=1`, which is a full Cartesian product.
- 5.0 adds hash-chunked pair generation and hash-based deterministic sampling [CLAIM-splink-15].

### 5.6 Clustering — verified
- `solve_connected_components` runs iterative SQL label propagation: each node takes the minimum representative among itself and its neighbours, repeated until nothing changes [CLAIM-splink-13].
- A source comment cites arXiv 1802.09478 as inspiration; the paper's method itself was not implemented because of UDF limits.
- Multi-threshold clustering reuses clusters that stay stable between thresholds (`_calculate_stable_clusters_at_new_threshold`).
- Cluster IDs are a function of the current run. They are **not persistent identities**, and Splink has no merge/split history, overrides or survivorship [CLAIM-splink-18].

### 5.7 Pipeline, concurrency, partitioning, caching, versioning, security
- **Pipeline:** each step queues SQL into a `CTEPipeline`, which `DatabaseAPI.sql_pipeline_to_splink_dataframe` materialises (`database_api.py` line 205). Dialect handling uses per-backend subclasses plus sqlglot [CLAIM-splink-19].
- **Transactions:** Splink has none of its own; it inherits the engine's. 5.0 makes SQLite chunk assignment stable across processes, which suggests multi-process runs [CLAIM-splink-15].
- **Partitioning:** Spark partitions, plus 5.0 chunking [CLAIM-splink-15].
- **Caching:** 5.0 removed the implicit cache in favour of explicit cache-table functions [CLAIM-splink-15].
- **Versioning:** the model JSON only; there is no decision lineage.
- **Security:** none at library level; data stays in the engine the caller configures. Telemetry is **NOT VERIFIED** [CLAIM-splink-20].

## 6. Functional and non-functional requirements inferred from verified behaviour

**Functional:**
- FR-1: explainable additive log-odds pair scoring [CLAIM-splink-08][CLAIM-splink-17].
- FR-2: label-free training [CLAIM-splink-09].
- FR-3: frequency-aware weighting [CLAIM-splink-11].
- FR-4: duplicate-free multi-rule blocking [CLAIM-splink-12].
- FR-5: threshold clustering and threshold comparison [CLAIM-splink-13].
- FR-6: online scoring of new records against an existing table [CLAIM-splink-15][CLAIM-splink-16].

**Non-functional:**
- NFR-1: the same model runs on a laptop (DuckDB) and on a cluster (Spark) [CLAIM-splink-05].
- NFR-2: memory is bounded by chunking [CLAIM-splink-15].
- NFR-3: the regulated-use pattern combines human review of borderline pairs with transparency documentation [CLAIM-splink-16].

## 7. Performance and resource model

| Claim | Type | Context | Confidence |
|---|---|---|---|
| "linking a million records on a laptop in approximately one minute" | Maintainer claim | Laptop and model unspecified | 0.3 [CLAIM-splink-06] |
| Spark "for 100+ million records" | Maintainer claim | Cluster unspecified | 0.3 [CLAIM-splink-06] |
| Homes England: ~30M addresses in under 5 h on Databricks | User report | Cluster size unknown | 0.4 [CLAIM-splink-07] |
| MoJ volumes: 19.6M / 2.9M / 2.2M / 2.4M / 20.9M / 17.7M records (pre-dedup), weekly | Government record | No hardware or latency given | 0.75 [CLAIM-splink-16] |

**Cost model (reasoned inference from §5).** Total cost ≈ O(blocked pairs × comparisons) for γ + O(distinct patterns × iterations) for EM + O(edges × CC passes) for clustering.
- Blocking selectivity dominates. A permissive rule (gender, common surname) is quadratic within its blocks, which is why 5.0 added pair-count estimation and `max_pairs` [CLAIM-splink-15].
- CC needs a number of passes on the order of the graph diameter.

**Failure modes:**
- EM non-convergence on dirty data; the docs advise cleaning or fixing m by hand [CLAIM-splink-09].
- Giant clusters from transitive chaining (hypothesis, 0.5).
- Correlated fields over-counting evidence.
- A 4→5 Spark performance regression, fixed before release [CLAIM-splink-15].

No benchmark was executed here.

## 8. Strengths and use-case-specific advantages

1. **Explainable probabilistic scoring.** Additive per-comparison weights map one-to-one onto EOIP evidence records [CLAIM-splink-08][CLAIM-splink-17]. To exceed it, persist the weights as queryable, permission-aware evidence.
2. **Label-free start** [CLAIM-splink-09]. To exceed it, feed BL-35 reviewer decisions back as labels for calibration.
3. **Laptop-to-cluster portability.** DuckDB fits EOIP's one-node-first constraint [CLAIM-splink-05].
4. **TF adjustment** handles common versus rare names without hand-written rules [CLAIM-splink-11].
5. **Regulated production evidence** with human review [CLAIM-splink-16].
6. **MIT licence** [CLAIM-splink-01].

## 9. Limitations with root causes

| # | Limitation | Class | Root cause | Category |
|---|---|---|---|---|
| L1 | No persistent IDs, merge/split history or survivorship | Intentional scope | Clusters are recomputed per run [CLAIM-splink-13][CLAIM-splink-18] | Developer friction |
| L2 | No incremental clustering; `find_matches_to_new_records` removed | Verified API change | Batch-analytics design [CLAIM-splink-15] | Developer friction |
| L3 | Conditional independence assumption | Algorithmic | Naïve-Bayes structure; correlated fields double-count [CLAIM-splink-09] | Algorithmic dead-end (mitigated by merging correlated fields into one comparison) |
| L4 | Expert-tuned training (EM rules, λ rules, manual m fixes) | Verified (docs) | EM identifiability [CLAIM-splink-09] | User friction |
| L5 | Threshold + CC chaining | Hypothesis 0.5 | CC is transitive and ignores negative evidence | Algorithmic |
| L6 | Breaking major upgrade 4→5 (input API, cache, salting, Athena, DOB metric) | Verified | Redesign [CLAIM-splink-15] | Upgrade risk |
| L7 | Single dominant maintainer | Inference | Public-sector funding | Maturity |
| L8 | No clerical-review UI | Verified absence [CLAIM-splink-17] | Library scope | User friction |
| L9 | Python ≥ 3.10 in metadata vs "3.9+" in the description | Verified inconsistency [CLAIM-splink-04] | Metadata drift | Minor |

There are no licensing restrictions.

## 10. Deployment, licensing, redistribution, and operational viability under EOIP constraints

- **Licence:** MIT, so redistribution and white-labelling are safe as long as notices are kept. Legal-review trigger: **no**. Transitive dependencies (DuckDB, sqlglot, PyArrow) still go through the SBOM licence scan [CLAIM-splink-01].
- **Air-gap:** viable. Splink is pure Python with in-process DuckDB and needs no service. Telemetry is NOT VERIFIED; check it with egress blocked in POC-ER-01.
- **One-node first:** run on DuckDB inside the EOIP worker, using disk-backed DuckDB/Parquet intermediates [CLAIM-splink-15].
- **Footprint:** PyArrow is required; pandas, Altair and igraph are optional [CLAIM-splink-15][CLAIM-splink-22]. None of these is in EOIP's `requirements.lock`, so Splink would ship as an optional "ER extra". It needs no GPU. Wheel size is UNVERIFIED.
- **Backend neutrality:** Splink runs over staging tables built from SourceEvents and never queries HugeGraph, Neo4j or Neptune. Its behaviour is therefore identical whichever backend is configured (§4.3 item 3).
- **Tenancy:** one DuckDB file and one model per tenant. Term-frequency tables are derived from tenant data and must never be shared between tenants.
- **Pipeline fit:** the "entity identity and linking" stage, before governed mutation. Its outputs are proposals, not writes.

## 11. Competitive delta against the EOIP verified baseline

| BL | EOIP | Splink | Delta |
|---|---|---|---|
| BL-34 deterministic identity | Implemented, person only, email key (`identity/resolver.py:49`) | Rules only as λ/blocking inputs | Keep BL-34 as the high-precision first pass; Splink adds the fuzzy second pass |
| BL-35 review queue | Partial: `IdentityCandidate` with `match_basis`, `confidence`, PENDING/CONFIRMED/REJECTED (`identity/candidates.py:26`) | None | EOIP is ahead on review semantics; Splink fills `confidence` with calibrated probability and explanation |
| BL-36 probabilistic ER | Absent | Full FS/EM/TF/blocking/CC [CLAIM-splink-08..13] | Largest delta; REUSE closes it |
| BL-37/38 revisions, bitemporal | Implemented | None | EOIP can version identity decisions |
| BL-39/40 claims, epistemic separation | Implemented (contract) | None | Matches stored as PROPOSED claims |
| BL-41 evidence manifests | Implemented | Per-pair terms available | Persist waterfall terms in manifests |

## 12. Strength-adoption cards and Con-to-Pro inversion cards

### Strength-adoption cards

| STR-ID | Competitor | Strength | Evidence | Value to EOIP customers | Decision | Design approach | Acceptance test |
|---|---|---|---|---|---|---|---|
| STR-splink-01 | Splink | Unsupervised FS with additive explainable weights | CLAIM-splink-08, -09, -17 | Fuzzy cross-source identity without labelling projects; reviewers see why | integrate (REUSE) | `eoip.identity.prob` adapter builds settings from the ontology's identity profile per entity type, runs on DuckDB staging and emits `IdentityCandidate`s with per-comparison weights | POC-ER-01: pairwise F1 ≥ 0.90; every candidate's terms sum to its match weight ±1e-6 |
| STR-splink-02 | Splink | TF adjustment | CLAIM-splink-11 | Fewer over-merges on common names | integrate | TF on name and email local part, computed per tenant | Ablation: fewer false merges on the common-surname subset, recall drop ≤ 2 pp |
| STR-splink-03 | Splink | Same model on DuckDB and Spark | CLAIM-splink-05 | Grows without a model rewrite | match | DuckDB by default; Spark profile documented only | Identical scores (±1e-9) on a 100k sample on both engines |
| STR-splink-04 | Splink | Duplicate-free multi-rule blocking | CLAIM-splink-12 | Bounded compute at high recall | match | Plus automatic rule suggestion from BL-26 profiler cardinality/null stats | Pairs ≤ 0.5 % of n² with blocking recall ≥ 0.98 |
| STR-splink-05 | Splink | Regulated production use with transparency records | CLAIM-splink-16 | Buyer trust; documentation template | match | Auto-generated ER model card per tenant model (settings, data window, thresholds, review rates) | Model card produced for every trained model and approved via the J4 workflow |

### Con-to-Pro inversion cards

**INV-splink-01 — Clusters without memory (no persistent identity, merge/split history or survivorship)**
- *Target:* Splink 5.0.0 under continuous enterprise ingest that needs stable IDs across daily runs.
- *Limitation:* cluster IDs are recomputed per run. There is no persistent-ID, unmerge or survivorship API, and `find_matches_to_new_records` was removed [CLAIM-splink-13][CLAIM-splink-15][CLAIM-splink-18].
- *Root cause:* scope/coupling. Splink is a batch analytical library (**proven**).
- *Mitigation and when it is worse:* an identity ledger treats Splink output as evidence edges and keeps canonical IDs with explicit merge/split events. That gives stable vertex keys, which J7 requires. It is worse for one-off statistical linkage, where the extra machinery is not needed.
- *Options:*
  1. Nightly Splink run, mapping new clusters to old canonical IDs by maximum overlap.
  2. **Identity ledger:** canonical-ID table, append-only `IdentityDecision` events (MERGE / SPLIT / ASSERT_SAME / ASSERT_DIFFERENT), and per-component incremental re-clustering with `predict_between`.
  3. Bitemporal identity graph (BL-37), with human assertions as must-link/cannot-link constraints.
- *Selected:* option 2, designed to grow into option 3.
```
on records R:
  det  = deterministic_keys(R)                         # BL-34 first pass
  cand = splink.predict_between(R, canonical_members)  # weighted pairs
  for component C touched by det ∪ cand (≥ review_threshold):
      cons = human ASSERT_SAME / ASSERT_DIFFERENT in C
      prop = constrained_cluster(C, edges, cons)       # CC with cannot-link cuts
      emit IdentityDecision(PROPOSED, diff(prop, current(C)), evidence=weights)
      auto-apply iff all edges ≥ auto_threshold and no constraint touched
  canonical IDs stable unless an approved MERGE/SPLIT; retired IDs become aliases
```
- *POC-ER-02:* 30 daily increments on a 1M base (5 % new, 2 % updated, 0.5 % deleted) with injected corrections. Success criteria:
  - ≥ 99.5 % of IDs unchanged where there is no new evidence;
  - every change traceable to an event;
  - an incremental run takes ≤ 10 % of a full rerun on one 8-core node.
- *Dependencies and compatibility:* BL-35 gains `decision_type` and edge-evidence references. Existing `urn:eoip:identity:person:email:*` IDs stay canonical.
- *Failure cases:* a merge must not merge ACLs. Facts keep their per-member source ACLs, which depends on BL-18. Cross-tenant merges are impossible because runs are per tenant, but cross-permission-domain merges inside one tenant need field-level ACL retention.
- *Defensibility:* the ledger is coupled to EOIP's bitemporal, evidence and review planes.
- *Decision:* **ADOPT**.

**INV-splink-02 — Independence assumption and expert-tuned training**
- *Target:* Splink 5.0.0 on heterogeneous sources with correlated attributes.
- *Limitation:* FS independence, expert-chosen training rules and manual m-fixing [CLAIM-splink-09].
- *Root cause:* algorithm, namely naïve-Bayes structure and EM identifiability (**proven** by the docs).
- *Mitigation and when it is worse:* calibrate with BL-35 reviewer labels (active learning). This adds nothing at cold start with no reviewers; FS stays the default then.
- *Options:*
  1. Generate EM training rules automatically from profiler statistics.
  2. Active learning: sample near the threshold and in uncertain γ patterns, re-estimate m with u fixed, and fit isotonic calibration.
  3. FS weights as features in a monotonic supervised model that keeps additive explanations.
- *Selected:* options 1 + 2. API: `ActiveLearner.next_batch(k)`; `Calibrator.fit(labels)`, versioned with the model.
- *POC-ER-03:* 0 / 200 / 500 / 1,000 labels. Success: Brier score improves ≥ 20 % at 500 labels, and F1 is not worse at 0 labels.
- *Failure cases:* labels are tenant data and stay per tenant; reviewer bias.
- *Defensibility:* labels compound per customer.
- *Decision:* **EXPERIMENT**.

**INV-splink-03 — Tabular-only evidence vs graph-relational identity signals**
- *Limitation:* only SQL backends and tabular comparisons are supported [CLAIM-splink-05]. Relational signals such as shared manager, co-commit or same repository are not native.
- *Root cause:* data model (**proven**).
- *Options:*
  1. Attributes only.
  2. Materialise graph features (Jaccard of linked repositories or projects, from BL-43) for blocked pairs as extra comparison columns.
  3. Collective ER that uses already-resolved neighbours.
- *Selected:* option 2 = EXPERIMENT; option 3 = DEFER. It is worse when features are expensive; blocking bounds that cost.
- *POC:* add one relational comparison to POC-ER-01. Success: ≥ 2 pp F1 gain on the developer subset with no extra pairs.
- *Decision:* **EXPERIMENT**.

**Seed hypothesis (§10.5):** none targets Splink.

## 13. Per-capability decisions

| Capability | Decision | Reason |
|---|---|---|
| CAP-31 probabilistic scoring (FS/EM/TF/blocking/clustering) | **REUSE** Splink after POC-ER-01 | MIT, mature, explainable, one-node DuckDB |
| CAP-31 persistent IDs, merge/split, survivorship | **BUILD** (identity ledger) | Absent in Splink and the other OSS reviewed; must integrate with EOIP revisions |
| CAP-30 deterministic keys | **BUILD** (extend BL-34 beyond persons) | Highest-precision first pass |
| CAP-24 match explanation | **BUILD** on Splink's terms | Persist as evidence |
| CAP-43 epistemic separation for matches | **BUILD** | PROPOSED until auto-threshold or approval |
| CAP-78 ER evaluation harness | **BUILD** | Synthetic plus public ER sets (W32 to confirm licences) |
| CAP-05 Spark scale-out ER | **DEFER** | Only when one node is exceeded |
| Active learning | **EXPERIMENT** | INV-splink-02 |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (all PROPOSED)

- **POC-ER-01 — Splink on one node.**
  - *Data:* synthetic enterprise identities (Jira/GitHub/HRIS/AD with typos, missing email, nicknames, transliteration) at 100k and 1M records, plus one public ER set whose licence allows publishing results.
  - *Setup:* Splink 5.0.0 on DuckDB, 8 vCPU / 32 GB, egress blocked.
  - *Metrics:* pairwise P/R/F1, B³ F1, blocking recall, pair count, wall time, peak RSS.
  - *Accept:* F1 ≥ 0.90 at 1M; ≤ 30 min; RSS ≤ 16 GB; zero outbound connections.
- **POC-ER-02 / POC-ER-03:** see INV-splink-01 and INV-splink-02.
- **T-ER-ACL:** a merged entity built from records with different ACLs; a user cleared for only one source must not see the other source's attributes (J5, depends on BL-18).
- **T-ER-TENANT:** no shared TF tables, models or DuckDB files across tenants (J13).
- **T-ER-REPLAY:** replaying the same SourceEvents produces identical canonical IDs and decisions (J7).

## 15. Risks, trade-offs, and open research questions

- **Upgrade risk** (4→5 broke APIs) [CLAIM-splink-15]: pin the major version and wrap Splink behind an EOIP adapter.
- **Maintainer concentration:** MIT permits a fork if needed.
- **Over-merge harm:** a false merge on permissioned data is worse than a missed match. Defaults should favour precision, with a high auto-merge threshold.
- **Open questions:**
  - Telemetry?
  - `predict_between` single-record latency against 1M canonical records on DuckDB?
  - Best constrained clustering method (CC with cannot-link vs correlation clustering)?
  - Can per-tenant TF tables be maintained incrementally?

## Appendix A — Research-dimension coverage

| Dimension | Section(s) | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | 1 | MoJ, MIT, 5.0.0 (2026-09-28), 4.0.17 maintained |
| D2 Problem and workloads | 2 | Batch/real-time probabilistic linkage |
| D3 Architecture | 4, 5.7 | Library → DatabaseAPI → SQL engines |
| D4 Storage and indexing | 5.1, 5.7 | No own storage; engine tables |
| D5 Schema and semantics | 5.1 | Comparisons/levels; no ontology |
| D6 Query pipeline | 5.5, 5.7 | CTE pipeline, blocking unions, chunking, profiling |
| D7 Reasoning | 5.2–5.4 | Probabilistic (FS/EM); no logic reasoning |
| D8 Transactions and scale | 5.7, 7 | Inherited; chunking; Spark |
| D9 Ingestion and federation | 2, 10 | Registered tables only |
| D10 Identity and evidence | 5, 11, 12 | Core; no merge/split/survivorship |
| D11 Time and evolution | 9, 12 | No temporal identity; ledger proposed |
| D12 Graph algorithms and ML | 5.6, 12 | CC; EM; relational features proposed |
| D13 Retrieval and agents | N/A | Not retrieval; feeds identity |
| D14 NL querying | N/A | None |
| D15 Governance | 12, 14 | Model JSON; model card proposed |
| D16 Human experience | 3, 9 | Charts; no review UI |
| D17 Developer experience | 1, 9, 15 | Python API; breaking 5.0 |
| D18 Trust and security | 5.7, 10 | Inherited; telemetry unverified; ACL-merge risk |
| D19 Multi-tenancy / white-label | 10 | Per-tenant runs; MIT |
| D20 Economics | 7 | Claims only |
| D21 Commercial / licensing | 10 | Free, MIT |
| D22 Interoperability / lock-in | 4, 10 | SQL engines, JSON model; low lock-in |
| D23 IP and prior art | 5 | FS (1969) and EM are public prior art; no patent search done |
| D24 Research quality | 7, App. C | Source-verified algorithms; performance unverified |

## Appendix B — Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-31 | native (scoring, clustering); absent (merge/split, survivorship) | CLAIM-splink-08..13, -18 | BL-36 Absent; BL-35 Partial | REUSE + BUILD ledger | P1 |
| CAP-30 | partial | CLAIM-splink-09 | BL-34 Implemented (person) | BUILD | P1 |
| CAP-24 | native (pair waterfall) | CLAIM-splink-17 | BL-48 Partial | BUILD on Splink terms | P2 |
| CAP-43 | absent | CLAIM-splink-18 | BL-40 Implemented (contract) | BUILD | P1 |
| CAP-04 | native (DuckDB) | CLAIM-splink-05 | — | REUSE | P1 |
| CAP-05 | native (Spark) | CLAIM-splink-05 | — | DEFER | P3 |
| CAP-50 | native offline (telemetry unverified) | CLAIM-splink-20 | — | REUSE after egress test | P1 |
| CAP-77 | MIT | CLAIM-splink-01 | BL-22 | REUSE | P2 |
| CAP-78 | partial | CLAIM-splink-17 | — | BUILD | P1 |

## Appendix C — Evidence records

| CLAIM-ID | Product / version / date | Exact claim | Classification | Source | Pub. / access | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-splink-01 | Splink master | MIT, © 2020 Ministry of Justice | Observed in source code | LICENSE https://raw.githubusercontent.com/moj-analytical-services/splink/master/LICENSE | 2020 / 2026-10-18 | 0.95 | None |
| CLAIM-splink-02 | 5.0.0 | PyPI upload 2026-09-28; dev1 2025-12-17…dev5 2026-09-18; MIT | Officially documented | https://pypi.org/project/splink/#history ; https://pypi.org/project/splink/5.0.0/ | 2026-09-28 / 2026-10-18 | 0.9 | GitHub release page "18 Sep" https://github.com/moj-analytical-services/splink/releases/tag/v5.0.0 |
| CLAIM-splink-03 | 4.0.x | 4.0.17 2026-09-03; 4.0.0 2024-07-24 | Officially documented | PyPI history | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-04 | 5.0.0 | requires Python >=3.10,<4; description says 3.9+ | Officially documented | PyPI 5.0.0 | / 2026-10-18 | 0.85 | Internal inconsistency |
| CLAIM-splink-05 | 5 docs | Backends DuckDB (default), Spark, SQLite, PostgreSQL; unsupervised; Python library | Officially documented | https://moj-analytical-services.github.io/splink/index.html | / 2026-10-18 | 0.85 | None |
| CLAIM-splink-06 | 5 docs | "a million records on a laptop in approximately one minute"; Spark "100+ million records" | Unverified | docs home | / 2026-10-18 | 0.3 no workload/hardware | None |
| CLAIM-splink-07 | 5 docs | Homes England ~30M records <5 h on Databricks | Third-party report | docs home | / 2026-10-18 | 0.4 | None |
| CLAIM-splink-08 | docs | K=m/u; M=log2(λ/(1−λ))+Σlog2(m/u); Pr=2^M/(1+2^M) | Officially documented | https://moj-analytical-services.github.io/splink/topic_guides/theory/fellegi_sunter.html | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-09 | docs | λ via rules+recall; u via random sampling; m via EM on blocked pairs; blocked columns not estimable in that pass; independence "rarely fully true"; manual m fix | Officially documented | https://moj-analytical-services.github.io/splink/topic_guides/training/training_rationale.html | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-10 | v5.0.0 | EM E/M steps, pattern-count fast path, convergence test | Observed in source code | `splink/internals/expectation_maximisation.py` L28–312 @v5.0.0 | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-11 | v5.0.0 | TF adj = w·(log2 u_exact − log2 greatest(tf_l,tf_r,tf_min)); not EM-estimated; fuzzy uses larger TF | Observed in source code; Officially documented | `comparison_level.py` L671–726 @v5.0.0; https://moj-analytical-services.github.io/splink/topic_guides/comparisons/term-frequency.html | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-12 | v5.0.0 | UNION ALL of rules, each excluding preceding rules; match_key; exploding rules | Observed in source code | `blocking.py` L108–221, 333–600, 753–836 @v5.0.0 | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-13 | v5.0.0 | Iterative SQL connected components (cites arXiv 1802.09478); multi-threshold stable clusters | Observed in source code | `connected_components.py`; `clustering.py` L44–347 @v5.0.0 | / 2026-10-18 | 0.9 | None |
| CLAIM-splink-14 | v5.0.0 | u sample sizing formulas; chunked accumulation | Observed in source code | `estimate_u.py` L99–330 @v5.0.0 | / 2026-10-18 | 0.85 | None |
| CLAIM-splink-15 | 5.0.0 | Removes implicit cache, salting, Athena, `find_matches_to_new_records`; adds chunking, `predict_between`/`predict_within`/`score_pair(s)`, TF join at predict, EM `max_pairs`, hash sampling, Spark cosine, PyArrow required, pandas optional, SplinkDataFrame-only registration, DOB → Levenshtein, Spark regression fix | Officially documented (PR titles) | https://github.com/moj-analytical-services/splink/releases/tag/v5.0.0 | 2026-09 / 2026-10-18 | 0.8 | None |
| CLAIM-splink-16 | MoJ record 2025-10-06 | Batch and real-time linkage across justice datasets; listed volumes; weekly JustLink; human review of some matches; trained staff merge/unmerge; clerical-label evaluation | Officially documented | https://www.gov.uk/algorithmic-transparency-records/moj-splink-master-record | 2025-10-06 / 2026-10-18 | 0.8 | None |
| CLAIM-splink-17 | 5 docs | Waterfall, match-weight, m/u charts; cluster studio | Officially documented | docs home | / 2026-10-18 | 0.8 | None |
| CLAIM-splink-18 | 5.0.0 | No persistent IDs, survivorship, incremental re-clustering, active-learning UI | Reasoned inference (absence) | sources of -05, -13, -15 | / 2026-10-18 | 0.55 | None found |
| CLAIM-splink-19 | 4.0.13 | sqlglot used for SQL parsing | Officially documented | https://github.com/moj-analytical-services/splink/releases | / 2026-10-18 | 0.7 | None |
| CLAIM-splink-20 | — | Telemetry behaviour | Unverified | — | / 2026-10-18 | 0.2 | — |
| CLAIM-splink-21 | irelink | Maps Splink 5 `predict_between`, `score_pair(s)`; `db_api.register()` before `Linker` | Third-party report | https://cran.r-universe.dev/irelink/doc/from_splink.html | / 2026-10-18 | 0.5 | None |
| CLAIM-splink-22 | 5.0.0 | Altair, igraph optional; Jinja, jsonschema removed | Officially documented | v5.0.0 notes | / 2026-10-18 | 0.8 | None |
| CLAIM-splink-23 | v5.0.0 | `postgres/database_api.py`, `duckdb/database_api.py` present; `athena/database_api.py` 404 | Observed in source code | raw.githubusercontent.com @v5.0.0 | / 2026-10-18 | 0.85 | None |
| CLAIM-splink-24 | 5.0.0 | SQL profiling (`DuckDBAPIWithProfiling`) | Officially documented | v5.0.0 notes (#3021) | / 2026-10-18 | 0.8 | None |

## Appendix D — Assumptions

1. The registry entry means `moj-analytical-services/splink`.
2. The PyPI date (2026-09-28) is the 5.0.0 release date; GitHub's "18 Sep" is recorded as contradictory.
3. Year-less GitHub dates were placed in 2026 by matching PyPI.
4. No performance figure was reproduced.
5. Per-tenant DuckDB execution in the EOIP worker is a design proposal.
6. Uncommitted working-tree files in the EOIP repository, which are outside the HEAD `ad9937b` baseline, were not evaluated.
