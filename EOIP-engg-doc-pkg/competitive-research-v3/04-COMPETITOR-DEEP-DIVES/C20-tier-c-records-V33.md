# C20 Tier C records (batch V33)

Verified 2026-10-26. Each record is capped at 250 words. Legend: BM-xx = benchmark IDs in 15-VALIDATION-BENCHMARK-PLAN.md; J = journeys.

### T-C20-memory-benchmarks — LoCoMo and LongMemEval
| Field | Value |
|---|---|
| URLs | https://github.com/snap-research/locomo ; https://github.com/xiaowu0162/LongMemEval |
| Owner | Snap Research / UNC (LoCoMo, ACL 2024, arXiv:2402.17753); Wu et al. (LongMemEval, ICLR 2025) |
| Version, status | no tagged releases; LoCoMo public file locomo10.json (10 conversations); LongMemEval 500 questions per variant (S, M, oracle) |
| Licence | LongMemEval MIT; LoCoMo LICENSE.txt present, type not read (UNVERIFIED) |
| Air-gap | yes data; LongMemEval auto-eval defaults to gpt-4o judge (needs swap to local) |
Relevance: evaluate agent memory write/expire/recall (CAP-57), J5 memory invalidation, J6 abstention (LongMemEval has 30 abstention items). Cannot test ACL revocation, tenant isolation (J13) or deletion. **LoCoMo is contested**: a vendor audit (Penfield) claims 6.4% of 1,540 questions have score-corrupting answer-key errors and a judge accepting up to 63% of deliberately wrong answers; Zep reported the adversarial category lacks ground truth and disputed Mem0's published comparison. Neither audit is independent or peer-reviewed; treat as unresolved [CLAIM-mem-03].
**Decision:** EXPERIMENT (LongMemEval primary; LoCoMo reference-only with caveat).
Claims: mem-01 LoCoMo 10 conv public, 50 in v1 paper, ACL 2024 (GitHub, 0.8). mem-02 LongMemEval MIT, 500 items per file, ICLR 2025, gpt-4o autoeval (GitHub, 0.8). mem-03 audit controversy (dev.to Penfield post; blog.getzep.com), third-party/vendor claims, 0.4, contra: no LoCoMo-author response found.

### T-C20-rdf-benchmarks — LUBM, BSBM, WatDiv, gMark
| Field | Value |
|---|---|
| URLs | swat.cse.lehigh.edu/projects/lubm ; BSBM (Univ. Mannheim, page unreachable by TLS error); dsg.uwaterloo.ca/watdiv ; github.com/gbagan/gmark |
| Versions | LUBM UBA 1.7 / UBT 1.1 (no date); WatDiv v0.6 (ISWC 2014); gMark no release; BSBM UNVERIFIED |
| Licence | LUBM: none stated; WatDiv: free use if citing the paper, "as is"; gMark MIT; BSBM UNVERIFIED |
| Air-gap | yes |
Relevance: SPARQL/OWL store load and query for GraphDB/Fuseki adapters (CAP-02, CAP-15, CAP-23); LUBM has 14 SPARQL 1.0 queries over one university ontology and tests OWL-lite-style reasoning; WatDiv stresses diverse query shapes; gMark generates graph plus query workloads from schemas (usable for synthetic enterprise schemas, CAP-78). All dated, SPARQL 1.0 era; not a substitute for SNB; publication terms unclear for LUBM/WatDiv beyond citation.
**Decision:** REFERENCE-ONLY (LUBM for reasoner smoke test; gMark EXPERIMENT for schema-driven workloads).
Claims: rdf-01 LUBM contents (lehigh page, 0.8). rdf-02 WatDiv v0.6 cite-to-use (UW page, 0.8). rdf-03 gMark MIT (GitHub, 0.7).

### T-C20-ogb — Open Graph Benchmark
| Field | Value |
|---|---|
| URL | https://ogb.stanford.edu/ ; https://pypi.org/project/ogb/ |
| Owner | Stanford SNAP group |
| Version | ogb 1.3.6 (2023-04-07); no newer release seen (maintenance) |
| Licence | package MIT; dataset licences not stated (UNVERIFIED, per-dataset review) |
| Air-gap | yes after download |
Relevance: standard node/link/graph property prediction (ogbn, ogbl, ogbg) and Large-Scale Challenge (MAG240M, WikiKG90Mv2, PCQM4Mv2) with fixed splits, evaluators and leaderboards. Use for CAP-63/64 (embeddings, link prediction) to confirm that a prediction plane (J8) reproduces known numbers; no enterprise, temporal or ACL aspect. Package pins old PyTorch/Python (3.6+, torch 1.6+), friction.
**Decision:** REFERENCE-ONLY (EXPERIMENT only if EOIP ships GNN link prediction).
Claims: ogb-01 v1.3.6 2023-04-07 MIT (PyPI, 0.9). ogb-02 task families (docs, 0.85).

### T-C20-multihop-qa — HotpotQA, 2WikiMultiHopQA, MuSiQue, MultiHop-RAG, CRAG, STaRK, KILT
| Set | Licence | Notes |
|---|---|---|
| HotpotQA | CC BY-SA 4.0 | distractor and fullwiki; EM/F1 on answer, supporting facts, joint |
| 2WikiMultiHopQA | Apache-2.0 repo (COLING 2020) | reasoning-step evidence |
| MuSiQue | CC BY 4.0 (TACL 2022) | composed single-hop questions |
| MultiHop-RAG | ODC-BY; 2,556 queries; COLM 2024 | 2-4 evidence docs, news |
| CRAG (Meta) | CC BY-NC 4.0 | non-commercial: legal-review trigger; 5 domains, 8 categories |
| STaRK | MIT; NeurIPS 2024 D&B | semi-structured KB retrieval (Amazon, MAG, PrimeKG) |
| KILT | MIT; repo archived 2023-10-31 | test answers hidden, EvalAI submission |
Relevance: BM-05 (HotpotQA, 2Wiki, MuSiQue named in the plan) and J6 plain-RAG vs graph A/B (CAP-56, CAP-55). STaRK is closest to KG-plus-text retrieval. Wikipedia-based sets overlap pretraining; none tests ACL, citations or abstention beyond CRAG-style categories. CRAG and CC BY-SA terms restrict redistribution inside a product; use download-only in CI.
**Decision:** INTEGRATE HotpotQA/2Wiki/MuSiQue/STaRK for BM-05; MultiHop-RAG EXPERIMENT; CRAG REFERENCE-ONLY; KILT REFERENCE-ONLY.
Claims: mh-01..mh-07, one per row, from the respective GitHub/site pages (0.75-0.85); dataset sizes mostly not on pages (UNVERIFIED).

### T-C20-mteb — MTEB (and MMTEB)
| Field | Value |
|---|---|
| URL | https://github.com/embeddings-benchmark/mteb |
| Owner | embeddings-benchmark community; leaderboard on Hugging Face |
| Version | no release shown on page (UNVERIFIED); "MTEB(eng, v2)" and MMTEB referenced |
| Licence | Apache-2.0 code; per-dataset licences not covered |
| Air-gap | yes after caching models/datasets |
Relevance: choose the default local embedding model (CAP-53, CAP-61) and replace the BL-14 hashing embedder with evidence; filter by size for CPU-only nodes. Leaderboard scores are self-reported/contamination-prone (hypothesis); English/multilingual generic text, not enterprise code or tickets; complements BEIR.
**Decision:** INTEGRATE (task-level runs on a 5-task subset for candidate local models).
Claims: mteb-01 Apache-2.0, v2 and MMTEB references, HF leaderboard (GitHub, 0.75).

### T-C20-rag-evaluators — ARES and TruLens
| Field | Value |
|---|---|
| URLs | https://github.com/stanford-futuredata/ARES ; https://github.com/truera/trulens |
| Versions | ARES v0.5.7 (pip ares-ai); TruLens no release listed on page |
| Licence | ARES Apache-2.0; TruLens MIT |
| Status | ARES 740 stars, 420 commits; TruLens 3.6k stars; maintenance not stated for either |
Relevance: ARES trains small judge classifiers for context relevance, faithfulness, answer relevance and uses prediction-powered inference for confidence intervals; this suits calibrating a local judge (CAP-60, CAP-78) but needs labelled data. TruLens provides OpenTelemetry-native tracing and the RAG triad (groundedness, context relevance, answer relevance); README cites groundedness F1 0.81 on LLM-AggreFact (vendor claim). Complements RAGAS (C20-ragas.md); OTel fits EOIP observability (BL-49).
**Decision:** ARES EXPERIMENT (judge calibration); TruLens REFERENCE-ONLY (OTel span conventions).
Claims: ev-01 ARES Apache-2.0, v0.5.7, PPI (GitHub, 0.8). ev-02 TruLens MIT, OTel-native, 3.6k stars (GitHub, 0.8).

### T-C20-code-benchmarks — SWE-bench, RepoBench, CrossCodeEval, CodeSearchNet
| Set | Licence | Notes |
|---|---|---|
| SWE-bench | MIT | Docker harness, Verified = 500 tasks; needs x86_64, 120 GB, 16 GB RAM; Multimodal v2 480 tasks (2026-09-01) |
| RepoBench | CC-BY-4.0 data; ICLR 2024; v1.1 2024-02-05 | cross_file_first/random, in_file; EM, ES, CodeBLEU |
| CrossCodeEval | Apache-2.0; NeurIPS 2023 | cross-file completion, tree-sitter metrics |
| CodeSearchNet | MIT code; repo archived 2023-04-11; per-project data licences | NDCG; 6 languages; 99 annotated queries |
Relevance: J1 and J10 code-graph quality (CAP-66, CAP-67, CAP-69): RepoBench/CrossCodeEval measure whether cross-file context retrieval helps, CodeSearchNet measures code retrieval, SWE-bench measures issue resolution by an agent (end-to-end, heavy). None measures call-graph precision or change-impact recall directly; EOIP needs its own labelled impact set. Source-project licences inside the datasets need review.
**Decision:** EXPERIMENT (RepoBench, CrossCodeEval as retrieval probes); SWE-bench REFERENCE-ONLY; CodeSearchNet REFERENCE-ONLY.
Claims: code-01..04 from GitHub pages (0.8).

### T-C20-oaei-er-datasets — OAEI and standard entity-resolution datasets
| Field | Value |
|---|---|
| URL | https://oaei.ontologymatching.org/ |
| Owner | OAEI organisers; campaign OAEI-2026 at ISWC ontology matching workshop (Bari) |
| Version | annual campaigns; tracks, MELT/SEALS tooling not confirmed on page (UNVERIFIED) |
| Licence | data-use document linked, terms not read (UNVERIFIED) |
Relevance: ontology alignment (CAP-09, CAP-12) and ER (CAP-31, J2, J12). "Standard ER datasets" (e.g. Magellan/DeepMatcher/Walmart-Amazon type sets) were not individually verified and are not endorsed here; gate any use on a licence check. Public sets lack survivorship, merge/split history and PII constraints (Senzing C04 covers product side).
**Decision:** EXPERIMENT (OAEI anatomy/conference-style tracks for ontology matching tests).
Claims: oaei-01 OAEI-2026 campaign listed (site, 0.7).

### T-C20-shacl-test-suites — W3C SHACL, JSON-LD and OWL test suites (ADD)
| Field | Value |
|---|---|
| URLs | https://w3c.github.io/data-shapes/data-shapes-test-suite/ ; https://github.com/w3c/json-ld-api ; https://www.w3.org/TR/owl2-test/ |
| Status | SHACL Recommendation 2017-07-20; OWL 2 conformance REC 2012-12-11; JSON-LD tests under `tests/` (date and licence not read) |
| Licence | SHACL suite no licence stated; OWL: W3C document rules, test-case licence unspecified; JSON-LD LICENSE.md not read |
Relevance: BL-29 notes the in-house SHACL subset runs against no W3C test suite and BL-32 no CI SHACL suite. The SHACL suite has 121 validation tests per its implementation report, EARL result files, `sht:partial` for conformance-only results. OWL 2 tests cover profile identification, entailment, consistency. Direct conformance proof for CAP-10, CAP-09, CAP-23 and for export interchange; JSON-LD tests for CAP-29/22-style interchange. Gap: reports are public claims, so EOIP must label partial support honestly.
**Decision:** INTEGRATE (run SHACL suite in CI, publish EARL report); OWL/JSON-LD EXPERIMENT. Registry action ADD.
Claims: shacl-01 REC 2017-07-20 and suite URL (W3C, 0.9). shacl-02 121 tests, EARL/partial (suite page, 0.85). owl-01 REC 2012-12-11 test types (W3C, 0.85).
