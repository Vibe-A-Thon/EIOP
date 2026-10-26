# 15 — Validation & Benchmark Plan (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 15-VALIDATION-BENCHMARK-PLAN.md |
| Status | **PROPOSED SPECIFICATION — nothing in this document has been executed.** Every BM-ID below is a benchmark *design*, not a result. Per Master Prompt §12/§15, any test not actually run is marked PROPOSED, never PASSED, and this research programme ran none of them. |
| Scope | BM-01 .. BM-22, mapped exactly to the GAP/CAP associations already fixed in `07-GAP-REGISTER.md` §1. No BM-ID is renumbered or invented here. |
| Inputs | `KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md` §12 (benchmark protocol), §14 (J1-J16), §15 (prohibited shortcuts); `07-GAP-REGISTER.md`; `08-STRENGTH-ADOPTION-REGISTER.md`; `09-CON-TO-PRO-INVERSION-REGISTER.md` §3; `01-SYSTEM-BASELINE.md` / `01a-BASELINE-DELTA-HEAD.md`; `02-TECHNOLOGY-REGISTRY.md` §3 and `04-COMPETITOR-DEEP-DIVES/C20-*.md` |
| Prior placeholder notice | A pass on 2026-10-19 wrote an earlier version of this file with specific pass/fail numbers presented as results (e.g. "p50 < 8ms, p95 < 25ms", ">= 55 FPS"). That version is superseded in full by this one. Nothing was measured on either date. Where a number appears below it is a **target threshold to test against**, not a result. |

---

## 1. Reproducibility rules (apply to every benchmark in this plan, no exceptions)

Master Prompt §12 requires that a benchmark state, every time, without exception: hardware, workload generator, dataset licence, query mix, warm-up, cache state, repetitions, variance, configuration, and versions. This plan adds the following standing rules, which bind every BM-ID below:

1. **Hardware must be stated per run, not assumed from a reference profile.** The reference profile below is the *target* configuration for the harness's first execution (GAP-43, INV-SELF-07); it is not evidence that any run happened on it.
   - **Reference node (target, unexecuted):** 16 vCPU (AMD EPYC class or equivalent), 64 GB RAM, NVMe SSD, no GPU (CPU-first policy per ADR-H15/H16/H17, `01-SYSTEM-BASELINE.md` U-11). Any GPU-accelerated run must say so explicitly and must not be compared to the CPU-only number without saying so.
2. **Workload generator and dataset must be named with a version, a checksum of the generated/staged data, and a licence.** "Synthetic data" without a generator version is not reproducible and is not accepted evidence.
3. **Query mix must be published as an explicit list of query shapes** (single-hop, deep multi-hop, recursive, subgraph match, ontology validation, temporal as-of, full-text/vector/hybrid, narrative evidence, NL-to-query — per Master Prompt §12), with the count of each shape in the run, not just a label like "mixed workload".
4. **Warm-up and cache state must be stated and held constant across compared runs.** A cold-cache number and a warm-cache number are different measurements and must never be shown as one line.
5. **Repetitions and variance:** minimum 3 repetitions per condition; report median and p95 plus the spread (min-max or stdev); a single run is not a benchmark result.
6. **Configuration and versions:** backend version, adapter commit hash, EOIP commit hash, dependency lock file hash, and any feature flags in effect must be recorded alongside every number.
7. **No universal "fastest" claim.** Every comparative claim is scoped to the exact backend version, data tier, and query shape tested; a win on BM-01 Tier 1 is not evidence for BM-02 Tier 3.
8. **Regression thresholds and rollback conditions are defined per benchmark** (see each BM-ID's "Regression / rollback rule" below) so that a CI gate has an unambiguous action, not a number to eyeball.
9. **Every result line in every future run of this plan carries a status tag**: PROPOSED (specified, not run — the status of everything in this document), RUN-LOCAL (executed on a non-reference machine, caveated), or RUN-REFERENCE (executed on the stated reference node). PASSED/FAILED is only ever written next to a RUN-* tag, never next to PROPOSED.
10. **No competitor number is reused as EOIP's own number.** Where a competitor's publicly reported figure is cited (e.g. TigerGraph's 2019 LDBC run, Mem0's LoCoMo figures), it is cited as *their* claim with its confidence rating from the relevant deep dive, never blended into an EOIP result row.

---

## 2. Benchmark suite (BM-01 .. BM-22)

Each entry: purpose (GAP/CAP it validates, exactly as fixed in `07-GAP-REGISTER.md`), data tier, workload/query mix, backends in scope, measures (Master Prompt §12 categories: systems / retrieval+answers / ML / UX), dataset and licence, pass/fail threshold (as a target, PROPOSED), regression/rollback rule.

### BM-01 — Backend conformance
- **Purpose:** CAP-01,13,14,18-20; GAP-01 (adapter defects unproven live), GAP-04 (query IR not on production path), GAP-05 (string-built Gremlin), GAP-06 (no path-mode/push-down), GAP-19 (licence gate), GAP-43 (no harness).
- **Data tier:** Tier 1 (100k nodes / 500k edges) for functional conformance; Tier 2 (1M / 10M) for the same suite under load.
- **Workload/query mix:** an identical CRUD + neighbourhood + bulk-load + tombstone script (the `GraphStore` protocol surface, `graph/store.py:56`) replayed against every adapter, plus the three named defects from INV-SELF-05: (a) a property-key round-trip test (write then read by non-canonical key) targeting the JanusGraph `p_`-prefix mismatch; (b) a label-filter-with-LIMIT test targeting the Neptune silent-truncation risk; (c) a Groovy-closure-dependent query against a gremlin-lang-only endpoint for the HugeGraph adapter.
- **Backends in scope:** HugeGraph, Neo4j, Neptune, JanusGraph, Fuseki, GraphDB, MemoryGraphStore (as a control, not a production target).
- **Measures:** systems — correctness (identical result sets within documented semantic differences), p50/p95/p99 latency, throughput, failure recovery.
- **Dataset/licence:** synthetic fixture generated in-repo (no external licence); optionally LDBC SNB SF1 (Apache-2.0, `04-COMPETITOR-DEEP-DIVES/C20-ldbc.md`) for a cross-backend parity check once a conformance harness exists.
- **Pass/fail threshold (target):** zero result-set mismatches across backends for identical logical queries, after documented semantic differences are excluded; the three named defects must each have a passing regression test before the suite is considered green.
- **Regression/rollback rule:** any backend adapter that newly fails a previously-passing conformance case blocks release of that adapter; roll back to the last green adapter commit.

### BM-02 — Scale and sizing
- **Purpose:** CAP-01-07,...,62,70; GAP-01, GAP-06 (multi-hop push-down), GAP-23 (canned OWL reasoners), GAP-24 (SPARQL not mounted), GAP-30 (sizing profiles unmeasured), GAP-31 (bulk-load throughput), GAP-32 (no supernode controls), GAP-37 (pure-Python algorithms), GAP-41 (large-graph rendering, cross-referenced to BM-13).
- **Data tier:** all three — Tier 1, Tier 2, Tier 3 (10M+ nodes / 100M edges) — this is the only BM-ID that must run the full tier ladder, per A-10 (`22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md`: ~10M nodes/~50M edges per tenant is the one-node sizing target).
- **Workload/query mix:** 2-hop and 4-hop neighbourhood traversals, bulk load at sustained rate, supernode (hot high-degree vertex) traversal, pure-Python algorithm runs (`graph/algorithms.py`, `graph/community.py`, `graph/paths.py`, `graph/anomaly.py` — BL-43) at each tier to find the point where in-process Python traversal misses a usable latency budget (GAP-06's hypothesis).
- **Backends in scope:** HugeGraph (primary), Neo4j, Neptune, JanusGraph; GraphBLAS/rustworkx/networkx-class engines as REFERENCE comparators only (per C12 cards), never as EOIP's own number.
- **Measures:** systems — ingest events/s, p50/p95/p99 latency, throughput, CPU/RAM/disk, storage amplification, operator effort.
- **Dataset/licence:** LDBC SNB generator (Apache-2.0) SF1/SF10/SF100 scaled to approximate the three tiers; synthetic enterprise digital-thread generator (in-repo, no external licence) for Tier-specific code/ops data.
- **Pass/fail threshold (target):** document the actual p50/p95/p99 curve and the tier at which it breaks a stated SLO (no SLO number is asserted here until measured); supernode test must show bounded memory growth, not an OOM.
- **Regression/rollback rule:** a release that regresses p95 by more than 20% at the same tier and query shape, with no documented cause, blocks release; rollback to the last release meeting the recorded baseline curve.

### BM-03 — Ingest / CDC chaos
- **Purpose:** CAP-04-06,25-27,32,34-41; GAP-12 (no typed constraint layer at the mutation gateway), GAP-15 (claims/contradictions in-memory only), GAP-16 (bitemporal reads unindexed), GAP-17 (ontology/data branches not persisted on Git), GAP-26 (connector breadth and permission-sync), GAP-29 (no OpenLineage interoperability), GAP-30, GAP-31.
- **Data tier:** Tier 1 for correctness; Tier 2 for throughput-under-chaos.
- **Workload/query mix:** duplicate events, out-of-order events, deletions, connector outage and resume, partial failure mid-batch, replay from checkpoint, corrupt-checkpoint recovery, source-schema changes mid-stream, permission revocation mid-stream.
- **Backends in scope:** primary backend only (HugeGraph) plus the ingestion pipeline (`ingestion/pipeline.py`, `ingestion/replay.py`, `ingestion/dlq.py`, `connectors/webhook.py`) — this BM-ID is about the pipeline, not backend parity.
- **Measures:** systems — ingest events/s under chaos, indexing lag, failure recovery time, no duplicate identities, no orphaned critical links, recoverable checkpoints (J7 acceptance criteria, Master Prompt §14).
- **Dataset/licence:** synthetic SourceEvent v2 stream generator (in-repo); no external dataset licence.
- **Pass/fail threshold (target):** zero duplicate identities and zero orphaned critical links after any chaos scenario; checkpoint recovery resumes within one replay cycle with no manual intervention.
- **Regression/rollback rule:** any chaos scenario that newly produces a duplicate identity or an orphaned link blocks release; this is treated as a correctness defect, not a performance regression, and gets the same severity as a P0 gap.

### BM-04 — ACL/tenant leakage — retrieval
- **Purpose:** CAP-30-33,38,44-47,53,55-57; GAP-02 (source-ACL not enforced on deployed paths — INV-SELF-01), GAP-10 (PII detection narrow), GAP-13 (ER limited to persons), GAP-28 (no evidence-span anchors), GAP-33 (GraphRAG not benchmarked, summaries not ACL-scoped), GAP-34 (agent memory lacks ACL — INV-SELF-09).
- **Data tier:** Tier 1, with two synthetic users of disjoint permissions over the same corpus (the exact construction specified in `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-01's falsifiable benchmark and realised as POC-02 below).
- **Workload/query mix:** identical question asked by both users across keyword, vector, hybrid and graph-traversal retrieval modes, through `/api/v1/rag`, `/api/v1/retrieval`, `agents/governed.py`, and the MCP surface — the four call sites `01a-BASELINE-DELTA-HEAD.md` BL-18/U-04 names as not passing `scope` today.
- **Backends in scope:** MemoryGraphStore for the first pass (fastest to wire the ACL check into); HugeGraph for the second pass once ACL propagation reaches the adapter layer.
- **Measures:** retrieval/answers — permission-leakage rate (target zero), citation and span accuracy, abstention behaviour when a fact is inaccessible.
- **Dataset/licence:** synthetic fact set with ACL principals (in-repo; see POC-02); no external dataset needed for the core leakage test. GraphRAG-vs-plain-RAG quality overlay (if run) may draw on GRB-B (MIT, `04-COMPETITOR-DEEP-DIVES/C20-graphrag-bench.md`) or BEIR (Apache-2.0 code, per-dataset licence, `04-COMPETITOR-DEEP-DIVES/C20-beir.md`) — see §4 on the LoCoMo caveat for why memory-specific claims need a different corpus.
- **Pass/fail threshold (target):** zero leaked facts in the answer, in citations, in the retrieval cache, or in agent memory, across all four call sites and all three retrieval modes; the derivation-ACL overhead (BM-04's own latency sub-measure) must stay under a documented percentage of unauthenticated traversal time, to be set once a first run exists (never asserted unmeasured, per rule 7 above).
- **Regression/rollback rule:** any leaked fact in any mode is a release blocker, full stop — there is no acceptable non-zero leakage rate; roll back to the last commit with a passing BM-04 run.

### BM-05 — ACL/tenant leakage — cross-tenant adversarial
- **Purpose:** CAP-45-47,53,55-57; GAP-02, GAP-03 (tenant isolation not enforced in graph adapters — INV-SELF-02), GAP-33, GAP-34.
- **Data tier:** Tier 1 for the adversarial probe set; Tier 2 to confirm the same probes hold under load with "noisy neighbor" tenants active.
- **Workload/query mix:** two tenants with adversarial cross-tenant query attempts (crafted traversal starting points that try to pivot from an owned node into another tenant's subgraph; crafted MCP/API calls supplying another tenant's IDs; cache-timing probes).
- **Backends in scope:** HugeGraph, Neo4j, Neptune — explicitly the three backends `01a-BASELINE-DELTA-HEAD.md` BL-20 confirms have zero tenant-handling code at the adapter level, so this is the benchmark that must catch what the embedded-layer isolation (`tenancy/layers.py`) does not reach.
- **Measures:** retrieval/answers — cross-tenant leakage (target zero) across data, index, cache, log, and agent memory (J13 acceptance criteria, Master Prompt §14).
- **Dataset/licence:** synthetic two-tenant fixture (in-repo).
- **Pass/fail threshold (target):** zero cross-tenant leakage across all five surfaces named above, for every isolation placement model (SILO/BRIDGE/POOL, `tenancy/isolation.py`).
- **Regression/rollback rule:** same as BM-04 — any leak is a release blocker; additionally, any backend whose native isolation primitive (graph space / multi-db / cluster) is not yet wired must be explicitly marked unsupported for POOL/BRIDGE deployment rather than silently passing SILO-only coverage.

### BM-06 — Retrieval/answer quality incl. GraphRAG-vs-plain-RAG
- **Purpose:** CAP-09,13,19-24,30-32,38,43,46,47,53-56,58-60; GAP-04 (query IR not on production path), GAP-06, GAP-09 (MCP single bearer token), GAP-13, GAP-22 (no incremental rule materialisation), GAP-23, GAP-25 (virtualisation SQL by f-string), GAP-28, GAP-33, GAP-35 (NL-query tier emits raw queries), GAP-46 (no persistent vector/full-text engine).
- **Data tier:** Tier 1 for the core A/B; Tier 2 to check that graph-first retrieval's relative advantage (or lack of one) holds as the corpus grows.
- **Workload/query mix:** identical question set run against (a) BM25 alone, (b) hashing-vector alone, (c) hybrid RRF, (d) graph-first `GraphRAGPipeline` (`ai/graphrag.py`, BL-16) — the deterministic-first, AI-second ordering required by J6 (Master Prompt §14).
- **Backends in scope:** MemoryGraphStore and HugeGraph; the retrieval service, not the graph backend, is under test.
- **Measures:** retrieval/answers — recall/precision/nDCG/MRR, faithfulness, answer correctness, citation and span accuracy, abstention behaviour, contradiction handling, token use, cost per correct answer.
- **Dataset/licence:** GRB-B Novel and Medical corpora (MIT repo, dataset licence on Hugging Face unread — legal-review trigger) for the graph-vs-vanilla task-level A/B; BEIR SciFact/NFCorpus/FiQA/ArguAna (Apache-2.0 code; per-dataset licence, download-only, not bundled) for a BM25 regression gate; HotpotQA (CC BY-SA 4.0, share-alike — legal-review trigger) and MuSiQue (CC BY 4.0) for multi-hop; **CRAG is explicitly excluded from this benchmark's default corpus** because it is CC BY-NC 4.0 (non-commercial) and EOIP has not obtained a commercial-use clearance — see §4 and §5.
- **Pass/fail threshold (target):** graph-first retrieval must not score worse than BM25 by more than a documented margin on fact-retrieval-level tasks, and must score better on multi-hop/complex-reasoning-level tasks, per the GRB-B task-level routing EOIP intends to use for J6 (`09-CON-TO-PRO-INVERSION-REGISTER.md` is silent on an exact number here; one is set only after a first run).
- **Regression/rollback rule:** a release that moves graph-first accuracy below the BM25 floor on any task level, with no corresponding fix to the regression's root cause, blocks promotion of that release as "graph-first enabled by default" for the affected task level.

### BM-07 — Query safety / NL-to-query execution accuracy
- **Purpose:** CAP-13,14,18-20,46,47,56-58; GAP-04, GAP-05 (string-built Gremlin, regex-only injection defences — INV-SELF-08), GAP-06, GAP-33, GAP-34, GAP-35.
- **Data tier:** Tier 1.
- **Workload/query mix:** CypherBench-style execution-accuracy set (Execution Accuracy, Provenance Subgraph Jaccard Similarity, Executable%) adapted to EOIP's own ontology and `QueryPlan`; a mutation/injection corpus (crafted property keys/labels designed to break out of the two string-built Gremlin call sites named in INV-SELF-08: `adapters/janusgraph.py:192,276`, `graph/hugegraph.py:525-551`); a cross-tenant canary set reused from BM-05.
- **Backends in scope:** JanusGraph and HugeGraph (the two adapters with the named string-building defect); Neo4j as a parameterised-query control.
- **Measures:** retrieval/answers — text-to-query execution accuracy; systems — zero successful injections (a correctness/security measure, not a performance one).
- **Dataset/licence:** CypherBench (Apache-2.0 repo; hardware note — needs 64 GB RAM for the 7-graph test split, 128 GB for all 11, `04-COMPETITOR-DEEP-DIVES/C20-text2cypher-bench.md`) for the external calibration set; an EOIP-ontology set of about 200 questions with gold `QueryPlan`s (in-repo) for the primary measurement, because CypherBench's Wikidata schema does not exercise EOIP's own query surface.
- **Pass/fail threshold (target):** zero successful injections from the mutation corpus (this is a hard zero, not a percentage); execution accuracy and PSJS reported per model/config with no absolute number asserted before a first run; top-3 NL-query-suggestion accuracy (J11) at least matching the deterministic-tier baseline.
- **Regression/rollback rule:** any successful injection blocks release unconditionally; an execution-accuracy regression beyond a documented band on the EOIP-ontology set triggers a review of the NL-to-query tier before the next release.

### BM-08 — Standards conformance (SHACL/W3C suites, OWL, RDF round-trip)
- **Purpose:** CAP-01,02,08-11,13-15,22,23,27-29,41,43,46; GAP-01, GAP-05, GAP-11 (SHACL conformance unproven), GAP-12, GAP-14, GAP-22, GAP-23 (OWL adapters return canned results), GAP-24 (SPARQL endpoint not mounted), GAP-27 (mapping not RML-conformant).
- **Data tier:** Tier 1 (W3C test suites are fixed-size by design, not scaled).
- **Workload/query mix:** the full W3C SHACL Core test suite against both the in-house validator (`ontology/shacl_validator.py`) and the `PySHACLAdapter` (pyshacl 0.40.1, now installed in the test environment per `01a-BASELINE-DELTA-HEAD.md` BL-29, not yet in the runtime image); the W3C JSON-LD test suite against `ontology/rdf.py`'s round-trip code; an RML test-case run (`04-COMPETITOR-DEEP-DIVES/C04-rml-tools.md` INV-rml-01) against the CML-to-IR mapping layer; a canned-result probe against each of the Openllet/HermiT/Jena reasoning adapters (`ontology/reasoning/adapters.py`) that must demonstrably fail on an unsatisfiable-class fixture, proving they are not wired to a real reasoner (BL-30).
- **Backends in scope:** n/a (semantic-web layer runs over RDF serialisations, not a graph backend); Fuseki/GraphDB (`graph/rdf_backend.py`) as the round-trip target once `query/sparql_protocol.py` is mounted (currently it is not — BL-06a).
- **Measures:** systems — conformance pass rate against the published test suite (a correctness measure); UX is not applicable here.
- **Dataset/licence:** W3C SHACL and JSON-LD test suites (W3C document licence, free to use for conformance testing); RML test cases (per `C04-rml-tools.md`, licence per source repo).
- **Pass/fail threshold (target):** 100% pass on W3C SHACL Core and JSON-LD conformance test cases that the in-house engine claims to support (unsupported constructs must be rejected with `UnsupportedConstraintError`, not silently skipped — this is already the design per BL-29, and this benchmark verifies it); the three canned-result reasoning adapters must be relabelled Absent/Research in every public claim until they call a real reasoner.
- **Regression/rollback rule:** any new SHACL/JSON-LD conformance failure on a previously-passing test case blocks release; any claim that cites OWL reasoning as "Implemented" while BM-08's canned-result probe still passes trivially is itself a documentation defect to fix before release, independent of code.

### BM-09 — Entity resolution precision/recall
- **Purpose:** CAP-28-31,41,47; GAP-13 (identity limited to persons; "Splink" engine is an unintegrated reimplementation), GAP-14 (ontology proposal not wired into governance), GAP-27 (mapping not RML-conformant).
- **Data tier:** Tier 1, scaled to the record counts in the chosen public ER benchmark.
- **Workload/query mix:** labelled-pair precision/recall evaluation against `identity/resolver.py` (person-only deterministic resolver) and `er/splink_engine.py` (the in-house Fellegi-Sunter reimplementation that does not call Splink, per BL-36); a blocking-quality check (block-size histogram, cluster-diameter) per the self-inversion-adjacent INV-zingg-03 pattern; a merge/split reversibility check against `identity/merger.py`'s ledger.
- **Backends in scope:** n/a (identity layer runs over the store protocol; MemoryGraphStore is sufficient).
- **Measures:** ML — precision/recall/F1 against a labelled gold set, calibration of the fixed m/u priors versus an EM-trained baseline (the gap BL-36 names explicitly), reproducibility across repeated runs.
- **Dataset/licence:** a public ER benchmark with a permissive licence (e.g., a standard deduplication benchmark set — exact set to be chosen at harness-build time and recorded with its licence before use; none is bundled by default).
- **Pass/fail threshold (target):** precision/recall reported against the gold set with no number asserted here before a first run; the review workflow for merge decisions above a cost threshold (GAP-13's "merge errors are costly" note) must trigger in 100% of high-impact cases in the test set.
- **Regression/rollback rule:** a drop in precision below the recorded baseline on the gold set, without a corresponding threshold-tuning changelog entry, blocks release of the identity layer.

### BM-10 — Schema-inference / ontology-proposal quality
- **Purpose:** CAP-20,26-28,41; GAP-14 (ontology proposal from arbitrary JSON not wired into governance), GAP-26 (connector breadth and permission sync).
- **Data tier:** Tier 1.
- **Workload/query mix:** arbitrary-JSON onboarding scenario (J12, Master Prompt §14): unknown JSON export fed to `ingest/profile.py` and `moonshot/ontology_induction.py`; measure whether the proposed ontology extension reaches a human review step and whether approval results in governed ingestion with provenance, end to end — the exact path GAP-14 says is not yet wired.
- **Backends in scope:** n/a (ingestion/governance layer).
- **Measures:** systems — entity/relationship detection precision/recall against a hand-labelled JSON fixture; UX — reviewer steps to approve/reject a proposal (onboarding friction, Master Prompt §12 UX category).
- **Dataset/licence:** synthetic JSON fixtures covering FK-like fields, arrays of IDs, parent pointers, URL references, polymorphic type+id (the shapes `ingest/profile.py` already claims to detect) — in-repo, no external licence.
- **Pass/fail threshold (target):** every proposed entity/relationship reaches the governance review queue (`ontology/governance.py` `GovernedPullRequest`) with evidence attached; zero silent auto-promotion of a proposal to a schema change without steward approval.
- **Regression/rollback rule:** any path that writes a schema change without passing through `GovernedPullRequest` is a P0 regression and blocks release.

### BM-11 — Temporal/bitemporal/contradiction correctness
- **Purpose:** CAP-08,09,19,20,22-25,32,34,38,39,41,71-73; GAP-06, GAP-12, GAP-15 (claims/contradictions in-memory only), GAP-16 (bitemporal reads unindexed and untested against an oracle), GAP-23.
- **Data tier:** Tier 1 for correctness against an oracle; Tier 2 for bitemporal read latency.
- **Workload/query mix:** as-of queries against `contracts/revision.py` and `graph/bitemporal.py` compared to a hand-built oracle (independently computed expected state at each (valid-time, transaction-time) pair); two-source-disagreement scenario (J2, Master Prompt §14: Confluence and ServiceNow disagree about the owning team) verifying both claims, validity time, evidence, and the resolution decision are preserved, never silently overwritten; a contradiction-detection probe against `truth/engine.py`'s in-memory `TruthStore`.
- **Backends in scope:** n/a for the temporal model itself (application layer); HugeGraph for the storage substrate.
- **Measures:** systems — graph completeness and consistency against the oracle, contradiction handling; retrieval/answers — citation and span accuracy when an as-of query is used as retrieval evidence.
- **Dataset/licence:** synthetic revision-history fixture with a hand-computed oracle (in-repo).
- **Pass/fail threshold (target):** 100% agreement with the oracle on as-of reconstruction for every tested (valid-time, transaction-time) pair; J2's "never overwrite history silently" criterion holds with zero violations in the test set.
- **Regression/rollback rule:** any as-of query that disagrees with the oracle, or any case where a second claim overwrites rather than coexists with a first, blocks release.

### BM-12 — Code-intelligence / digital-thread journeys (J1, J9, J10)
- **Purpose:** CAP-17-20,66-69; GAP-06, GAP-39 (code graph syntactic, 2 languages, no compiler-grade symbols), GAP-40 (digital-thread journeys untested end to end).
- **Data tier:** Tier 2 (a realistic multi-service codebase plus its Jira/PR/CI/incident history).
- **Workload/query mix:** J1 (Jira Story -> PR -> commit -> function -> downstream service/API -> build -> deployment -> docs -> related incidents, with version-specific affected assets, source spans, permissions, confidence, explanation; reindexing a changed commit must not break unchanged relationships); J9 (service-account blast radius across identity directory, code, CI/CD, infra config, runbooks); J10 (rule-change test scope: which systems/code paths/tests/owners are affected).
- **Backends in scope:** primary backend (HugeGraph) with the code graph (`codegraph/parser.py`, Python and TypeScript only per BL-42 — SCIP/LSIF absent).
- **Measures:** systems — reindex correctness (no broken unchanged relationships); retrieval/answers — evidence completeness and confidence calibration for blast-radius answers; UX — investigation steps to reach a correct answer.
- **Dataset/licence:** a synthetic but realistic enterprise digital-thread fixture (in-repo generator: Jira -> Git PR -> commit -> Python/TypeScript AST -> service trace); no external dataset licence needed, since BL-42 covers only Python/TypeScript today.
- **Pass/fail threshold (target):** J1/J9/J10 all return a materially correct answer set (manually verified against the fixture's known-correct graph) with evidence spans and confidence on every edge; reindexing a single changed commit leaves all other relationships byte-identical.
- **Regression/rollback rule:** any journey that returns an incomplete or incorrect blast-radius answer on the fixture, or any reindex that mutates an unrelated relationship, blocks release of the code-intelligence layer.

### BM-13 — Large-graph rendering
- **Purpose:** CAP-20,70,71; GAP-41 (large-graph rendering unmeasured).
- **Data tier:** Tier 2 and Tier 3 node counts rendered client-side (not the same as backend scale — this measures the web UI, `apps/web/src/*`, Cytoscape 3.30 / Sigma 2.4).
- **Workload/query mix:** pan/zoom/filter interaction on a 100k-node, then a 1M-node, permission-filtered subgraph view.
- **Backends in scope:** n/a (client rendering).
- **Measures:** UX — rendering frame rate (Master Prompt §12 UX category), usability under permission-filtered views (server-side aggregation per `09-CON-TO-PRO-INVERSION-REGISTER.md` Gephi seed-hypothesis finding: "poor at very large" is unproven and must be measured, not assumed).
- **Dataset/licence:** synthetic graph fixture (in-repo).
- **Pass/fail threshold (target):** a documented, measured frame-rate curve at each node count, with the point at which interaction becomes unusable identified before any UI library decision is made (per the inversion register's explicit caution: "do not churn libraries before measurement").
- **Regression/rollback rule:** a frame-rate regression at a previously-acceptable node count, with no corresponding feature justification, blocks release of the affected UI change.

### BM-14 — Local model serving / MCP latency
- **Purpose:** CAP-46,59-61; GAP-09 (MCP single shared bearer token — INV-SELF-04), GAP-36 (Ollama pinned old, root, unauthenticated — INV-SELF-10).
- **Data tier:** Tier 1 (latency benchmark, not a graph-scale benchmark).
- **Workload/query mix:** local-model inference latency (Ollama/llama.cpp class) under a realistic GraphRAG synthesis prompt load; MCP tool-call round-trip latency through the 18 tools in `apps/mcp/main.py`; a CVE/vulnerability scan of the pinned model-runtime image (the INV-SELF-10 benchmark: "zero known-exploitable CVEs at release time, re-checked on every release").
- **Backends in scope:** n/a (model-serving layer).
- **Measures:** systems — p50/p95/p99 latency, local inference throughput; retrieval/answers — cost per correct answer (token use); security — CVE count on the pinned image (zero target).
- **Dataset/licence:** synthetic prompt set representative of GraphRAG synthesis calls (in-repo).
- **Pass/fail threshold (target):** zero known-exploitable CVEs on the pinned model-runtime image; MCP tool-call latency documented with no asserted SLO before a first run.
- **Regression/rollback rule:** a newly-disclosed exploitable CVE on the pinned image blocks release until the pin is updated; this is a standing CI gate, not a one-time check, per INV-SELF-10.

### BM-15 — Epistemic-plane and ML-prediction integrity
- **Purpose:** CAP-10,20,28,41-43,47,62-64; GAP-07 (epistemic planes not enforced store-wide — INV-SELF-06), GAP-17, GAP-37 (algorithms pure Python, no fast-engine port), GAP-38 (neural tier not executable, torch absent).
- **Data tier:** Tier 1.
- **Workload/query mix:** INV-SELF-06's own falsifiable benchmark — attempt to write an "approved" fact through every ingestion path without going through promotion; all attempts must fail; separately, a probe that every link-prediction/anomaly output from `gnn/engine.py` lands only in the prediction plane (J8, Master Prompt §14: predictions without fact contamination) and never auto-promotes to a fact without human approval.
- **Backends in scope:** n/a (epistemic-boundary and prediction-plane logic sits above the store).
- **Measures:** systems — write-path correctness (a security/governance measure, not performance); ML — leakage-safe evaluation is deferred to BM-21 for the GNN-specific case; here the measure is binary (contaminated vs not).
- **Dataset/licence:** synthetic ingestion-path fixture (in-repo).
- **Pass/fail threshold (target):** zero successful "approved" writes that bypass promotion, across every ingestion path tested; zero predictions that land in the fact plane without a recorded human-approval event.
- **Regression/rollback rule:** any bypass is a P0 release blocker, same severity class as GAP-07's forced-P0 status.

### BM-16 — Backup/restore/DR drills
- **Purpose:** CAP-74-76; GAP-42 (restore drills not run).
- **Data tier:** Tier 2 and Tier 3 (restore time is the measure of interest, and it scales with data volume).
- **Workload/query mix:** full backup, then restore to a clean environment, then point-in-time restore (PITR) to a timestamp mid-way through a recorded ingestion stream, verifying no data loss beyond the documented RPO.
- **Backends in scope:** HugeGraph (primary); `scripts/backup.py`, `scripts/restore.py`, `recovery/wal.py` (BL-50, currently "Implemented (scripts) / live-unverified").
- **Measures:** systems — recovery duration, restore reliability (does the restored graph match the pre-backup graph exactly, modulo the intended PITR cutoff).
- **Dataset/licence:** the Tier 2/Tier 3 synthetic fixtures from BM-02 (in-repo).
- **Pass/fail threshold (target):** restored graph is byte-for-byte equivalent (modulo timestamps) to the source at the PITR cutoff; restore duration documented with no asserted target before a first run.
- **Regression/rollback rule:** any restore that loses data inside the documented RPO window blocks release of the backup/restore tooling; this is the first time this suite has ever run (per the brief's explicit instruction to note that no restore drill has completed), so the first green run becomes the baseline, not a comparison point.

### BM-17 — Ontology governance workflow
- **Purpose:** CAP-08,10-12,20,25,34-37,39-41,70-72; GAP-11, GAP-12, GAP-15, GAP-16, GAP-17 (ontology/data branches not persisted on Git, governance mostly unmounted), GAP-18 (no dry-run migration with rollback), GAP-29, GAP-41.
- **Data tier:** Tier 1.
- **Workload/query mix:** J4 (Master Prompt §14: model a new relation; dry-run migration and SHACL validation; show semantic diff and impacted queries; approve; release; roll back safely) run end to end against `ontology/gitops.py`, `ontology/governance.py`, `migration/protocol.py`.
- **Backends in scope:** n/a (governance layer); HugeGraph as the target of the eventual migration.
- **Measures:** systems — migration correctness (semantic-equivalence "golden queries" stage per `01a-BASELINE-DELTA-HEAD.md` NB-09); UX — steward task completion time for a governed ontology change.
- **Dataset/licence:** synthetic ontology-change fixture (in-repo).
- **Pass/fail threshold (target):** the full J4 sequence (dry-run -> diff -> approve -> release -> rollback) completes with a correct rollback that restores pre-change state exactly.
- **Regression/rollback rule:** any migration that cannot be dry-run or cannot be rolled back safely is a release blocker for that migration path.

### BM-18 — Security/injection/audit/supply-chain
- **Purpose:** CAP-13,20,44,46-51,53,57-59,79; GAP-02, GAP-03, GAP-05 (INV-SELF-08's own benchmark), GAP-08 (egress vault cipher — INV-SELF-03's own benchmark), GAP-09 (INV-SELF-04's own benchmark), GAP-20 (audit trail not tamper-evident), GAP-21, GAP-34, GAP-35.
- **Data tier:** Tier 1.
- **Workload/query mix:** the injection corpus from INV-SELF-08 (malicious property keys/labels against every adapter); the cryptographic review checklist plus known-plaintext-recovery test from INV-SELF-03 (must fail against the replacement AEAD cipher); the malicious tool-poisoning and confused-deputy test suite from INV-SELF-04 (every MCP tool call must be attributable to a real end-user principal and ACL-checked); an audit-log tamper-evidence probe (hash-chain verification, GAP-20, currently unverified per the gap register).
- **Backends in scope:** JanusGraph, HugeGraph (injection corpus); n/a for the egress vault and MCP tests.
- **Measures:** systems/security — zero successful injections, zero successful known-plaintext recovery against the AEAD cipher, 100% MCP tool-call attribution, tamper-evidence verified on every audit-log entry.
- **Dataset/licence:** in-repo fixtures; reference the OWASP Top 10 for LLM Applications (2025 edition, licence UNVERIFIED — do not copy text verbatim, `04-COMPETITOR-DEEP-DIVES/C19-llm-threat-guidance.md`) and MITRE ATLAS technique IDs for test-case tagging only, not for reused text.
- **Pass/fail threshold (target):** every sub-test above at zero (hard zero, not a percentage).
- **Regression/rollback rule:** any single failure in this suite blocks release; this suite sits directly underneath `16-SECURITY-PRIVACY-THREAT-MODEL.md` and should be read alongside it.

### BM-19 — Air-gap install drill
- **Purpose:** CAP-02-04,13,48-50,79; GAP-05, GAP-20, GAP-21 (air-gapped install unverified; Neptune cannot be air-gapped), GAP-24, GAP-30.
- **Data tier:** Tier 1 (the drill is about install mechanics, not data scale).
- **Workload/query mix:** transfer a pre-built offline bundle to a network-isolated host, load container images, stage local model weights, boot via compose, run a self-test suite with zero outbound network calls observed (verified by a packet-capture or egress-proxy check, not by trusting the installer's own claim).
- **Backends in scope:** HugeGraph, Neo4j (both air-gappable); Neptune explicitly excluded and documented as excluded (A-08, `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md`: "Neptune is treated as a required supported backend even though it cannot run air-gapped").
- **Measures:** systems — install success, zero outbound network calls observed during the self-test, operator effort (time to first governed query).
- **Dataset/licence:** the offline bundle itself (EOIP's own images and models — licence of any bundled model weight must be checked against the allow-list before staging, per GAP-19/BM-20).
- **Pass/fail threshold (target):** zero outbound network calls during the entire drill; self-test suite passes with no manual patching.
- **Regression/rollback rule:** any outbound network call detected during an air-gap drill is a release blocker for the "air-gapped" claim specifically (the product may still ship for connected deployments, but the air-gap claim is withdrawn until fixed).

### BM-20 — Licence CI gate / white-label packaging
- **Purpose:** CAP-28,43,50-52,75-79; GAP-08, GAP-19 (no licence allow-list in CI — INV-SELF-11's own benchmark), GAP-21, GAP-43, GAP-44 (no SBOM/signing pipeline; scanners unpinned).
- **Data tier:** n/a (this is a build/CI benchmark, not a data-scale one).
- **Workload/query mix:** INV-SELF-11's own benchmark — introduce a dependency with a known-blocked licence (e.g. a package declaring AGPL-3.0) on a test branch; the CI gate must fail the build; separately, a supply-chain drill per `04-COMPETITOR-DEEP-DIVES/C19-supply-chain.md`: SBOM completeness diff against `requirements.lock`, offline signature verification of a signed artefact, a tamper test (modify a signed image and confirm `cosign verify` rejects it), and a pinned-SHA lint on CI workflow files (the control that would have caught the March 2026 Trivy supply-chain compromise described in C19-supply-chain, where `trivy-action` tags were force-pushed and `setup-trivy`/Trivy v0.69.4 were backdoored for roughly 12 hours).
- **Backends in scope:** n/a.
- **Measures:** systems/security — build fails on a blocked licence (binary pass/fail); SBOM completeness; signature verification success; tamper detection.
- **Dataset/licence:** n/a (CI fixtures only); the allow-list itself is derived from `02-TECHNOLOGY-REGISTRY.md` §3's legal-review triggers.
- **Pass/fail threshold (target):** the CI gate fails 100% of the time when a blocked-licence dependency is introduced; SBOM lists all `requirements.lock` entries with no omissions; a tampered image fails `cosign verify` offline.
- **Regression/rollback rule:** any silent pass of a blocked-licence dependency, or any successful verification of a tampered artefact, is a P0 release blocker (GAP-19 is forced-P0 per the gap register's own rule for licensing gates).

### BM-21 — Temporal graph learning / GNN leakage-safe eval
- **Purpose:** CAP-34,43,63-65; GAP-38 (neural tier not executable, torch absent; no calibration).
- **Data tier:** Tier 1 (the numerics-only path, `neural/*` with numpy, is testable today; the torch-dependent encoders in `neural/encoders.py` are not executable in any shipped environment per `01a-BASELINE-DELTA-HEAD.md` BL-44, and this benchmark cannot run until torch is added to a lock file — U-13).
- **Workload/query mix:** leakage-safe temporal train/test splits (no future edge visible to the training split); link-prediction/anomaly task against `gnn/engine.py`'s pure-Python heuristics as the only currently-runnable baseline; a non-graph and rule-only baseline comparison (Master Prompt §12 ML measure: "non-graph and rule-only baselines" is mandatory before any graph-learning claim).
- **Backends in scope:** n/a (in-process).
- **Measures:** ML — AUROC/AUPRC/F1 against the rule-only baseline, calibration, drift, explanation quality, reproducibility.
- **Dataset/licence:** a public temporal-graph benchmark with a permissive licence, to be chosen and recorded at harness-build time; no dataset is bundled by default.
- **Pass/fail threshold (target):** the pure-Python heuristic engine must beat the rule-only baseline before any "learned" claim is made in marketing or product docs; once torch is added, `neural/encoders.py`'s R-GCN/GraphSAGE/R-GAT/HGT/GraphGPS/ChebNet models must each individually beat both the rule-only baseline and the pure-Python heuristic before being called "Implemented".
- **Regression/rollback rule:** any claim of a working GNN capability that has not passed this benchmark against a rule-only baseline is a documentation defect to correct immediately, independent of a code change.

### BM-22 — Wisdom/process-intelligence + evaluation-harness meta-test
- **Purpose:** CAP-38,78-80; GAP-43 (no unified evaluation harness with regression gates — INV-SELF-07's own benchmark), GAP-44, GAP-45 (wisdom/decision layer library-only; no process-event import).
- **Data tier:** n/a for the meta-test (it tests the harness, not a data tier); Tier 1 for the wisdom-layer functional test.
- **Workload/query mix:** INV-SELF-07's own benchmark — "does every BM-ID in this document execute and gate a release" — i.e., BM-22 is partly a test of this very plan's own machinery, run as a CI meta-check once the harness exists; separately, a functional probe of `wisdom/decision_trace.py`, `wisdom/precedent_engine.py`, `wisdom/outcome_tracker.py`, `wisdom/counsel.py` (library-only per `01a-BASELINE-DELTA-HEAD.md` BL-56) to confirm decision traces persist and are queryable once mounted.
- **Backends in scope:** n/a.
- **Measures:** systems — harness coverage (fraction of BM-01..BM-21 that the harness can actually execute unattended, which today is zero); UX — none specific.
- **Dataset/licence:** n/a.
- **Pass/fail threshold (target):** the harness executes BM-01 through BM-21 unattended and produces a pass/fail/PROPOSED report for each, with no manual step; the wisdom layer persists a decision trace that survives a restart.
- **Regression/rollback rule:** since the harness itself does not exist yet (GAP-43 is the precondition for every other benchmark's own automation), BM-22's first green run is the baseline for "the plan works," and every subsequent release must keep that coverage fraction from regressing.

---

## 3. Chaos/stress matrix

Master Prompt §12 names ten chaos/stress dimensions. This matrix maps each to the BM-IDs that exercise it; a dimension with only one BM-ID is under-tested and should get a dedicated case before it is considered covered.

| Chaos dimension | BM-IDs that exercise it |
|---|---|
| Degree skew (hot supernodes) | BM-02, BM-13 |
| Bursty CDC | BM-03 |
| Clock skew | BM-03, BM-11 |
| Duplicate/out-of-order events | BM-03 |
| Partial failure (mid-batch, mid-write) | BM-03, BM-16 |
| Replay | BM-03, BM-16 |
| Corrupt checkpoints | BM-03, BM-16 |
| Source-schema changes mid-stream | BM-03, BM-10 |
| Permission revocation | BM-03, BM-04, BM-05 |
| Offline restarts | BM-16, BM-19 |
| Noisy tenants (added dimension, not in the original ten but required for BM-05's "noisy neighbor" case) | BM-02, BM-05 |

No chaos scenario is currently run (per the status line at the top of this document); this matrix is the design for the harness that GAP-43/BM-22 must build.

---

## 4. LoCoMo and memory-benchmark contested evidence

LoCoMo-style agent-memory benchmarks are **contested evidence** and must not be used alone to validate any BM-06/BM-07 memory-specific claim. The GraphRAG/memory cohort finding (`05-COMPARISON-COHORTS/06-GRAPHRAG-MEMORY-COHORT.md`) records three vendors reporting internally contradictory numbers on the same benchmark under different configurations (Zep 75.14, Mem0 92.5, Letta 74.0, all self-reported), and a third-party audit (Penfield Labs, cited at confidence 0.3, secondary source, `04-COMPETITOR-DEEP-DIVES/C08-graphiti-zep.md` CLAIM-graphiti-zep-22) found 99 score-corrupting errors in 1,540 LoCoMo questions and an LLM judge that accepted 62.81% of deliberately wrong answers. This is not a case of "one vendor is right" — it is evidence that the LoCoMo answer key and judge methodology are themselves unreliable as currently published.

Consequence for this plan: BM-06 and BM-07's memory-adjacent claims (agent memory ACL/evidence, per GAP-34/INV-SELF-09) must be validated with **task-completion and citation-accuracy measures** instead — i.e., does the memory record support the exact claim it is cited for, with a deterministic span check (the same claim-support mechanism EOIP already has in `ai/claim_support.py`, commit c264c07), not an LLM-judge accuracy percentage on a contested answer key. `04-COMPETITOR-DEEP-DIVES/C20-tier-c-records-V33.md` records the decision as "EXPERIMENT LongMemEval for CAP-57; LoCoMo reference-only, contested" — LongMemEval (MIT licence) is the preferred external memory benchmark where one is needed at all, and even then only paired with the deterministic claim-support check, never as the sole measure.

---

## 5. Benchmark-publication constraints

Three licence terms researched in this programme restrict how EOIP may publish comparative benchmark numbers. This plan complies with all three as follows:

1. **TigerGraph Community Edition licence** forbids benchmark publication outright (`04-COMPETITOR-DEEP-DIVES/C01-tigergraph.md` CLAIM-tigergraph-04: "no benchmark publication" as a Community Edition term, updated 2026-03-05, confidence 0.8 — summary via fetch tool, not full text read). **Compliance:** EOIP does not run or publish any benchmark naming TigerGraph Community Edition performance figures; if an Enterprise-licensed TigerGraph comparison is ever wanted, it requires separate legal clearance of the Enterprise OEM terms (currently unverified) before any number is published.
2. **RDFox evaluation licence** requires prior approval before publishing benchmarks (`04-COMPETITOR-DEEP-DIVES/C02-rdfox.md` CLAIM-rdfox-04: "evaluation only; no commercial use/distribution; benchmark publication needs approval"). **Compliance:** this plan does not publish any RDFox performance number; if RDFox is ever benchmarked internally for evaluation purposes under that licence, the result stays internal (not published, not quoted in sales/marketing material) unless Oxford Semantic Technologies approves publication in writing.
3. **LDBC's "LDBC Benchmark Results" trademark rule** (`04-COMPETITOR-DEEP-DIVES/C20-ldbc.md` §10): only an LDBC-approved-auditor-reviewed run may be called an "LDBC Benchmark Result"; any other report of SNB/FinBench/Graphalytics/SPB-based numbers that uses that phrase infringes the trademark. Unaudited results are permitted if clearly labelled unofficial. **Compliance:** every number this plan produces using the LDBC generator/driver (BM-01, BM-02) is labelled **"not LDBC Benchmark Results"** in any report or artefact, per the Fair Use Policy's own suggested disclaimer; EOIP does not commission an LDBC audit in this programme and makes no audited-result claim.

All three constraints are **legal-review triggers**, not resolved legal conclusions (per A-11, `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md`: "legal conclusions on licences are out of scope"). Before any benchmark number touching TigerGraph, RDFox, or LDBC-sourced tooling is published externally (sales deck, blog, docs site), legal review must confirm the specific licence text in force at that time, since `C01-tigergraph.md` and `C02-rdfox.md` both flag their cited clauses as summaries, not full-text reads.

Separately, the dataset-licence legal-review triggers flagged in §2 above (CRAG CC BY-NC 4.0 excluded from BM-06's default corpus; HotpotQA CC BY-SA 4.0 share-alike; GRB-B's underlying Novel/Medical dataset licences on Hugging Face unverified) all require the same legal clearance before any of those corpora are redistributed inside an EOIP product image. This plan's default posture is **download-only, staged in CI, never bundled**, for every dataset carrying a restrictive licence.
