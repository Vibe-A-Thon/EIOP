# C20 GraphRAG-Bench (two distinct benchmarks share the name)

| Field | Value |
|---|---|
| Registry ID | T-C20-graphrag-bench |
| Tier | B (only purpose-built public benchmarks asking when graphs beat plain RAG; feeds J6) |
| Versions examined | (A) arXiv:2506.02404 v3 (2025-06-20); (B) arXiv:2506.05690 v3 (2026-02-22), repo GraphRAG-Bench/GraphRAG-Benchmark HEAD |
| Verified on | 2026-10-26 |
| Worker | V33 |

## 1. Identity, current status, tier, and sources
Disambiguation (required):
| Id | Title | Authors / affiliation | Venue | Licence |
|---|---|---|---|---|
| **GRB-A** | "GraphRAG-Bench: Challenging Domain-Specific Reasoning for Evaluating Graph RAG", arXiv:2506.02404 | Xiao, Dong, Zhou, Dong, Zhang, Yin, Sun, Huang (PolyU / Tencent Youtu per search summary) | arXiv preprint only, no venue on page [CLAIM-grb-01] | not verified |
| **GRB-B** | "When to use Graphs in RAG: A Comprehensive Analysis for Graph RAG", arXiv:2506.05690; repo README "Comprehensive Benchmark and Analysis" | Xiang, Wu, Zhang, Chen, Hong, Huang, Su | README says ICLR'26 acceptance; arXiv page lists no venue [CLAIM-grb-02, -03] | MIT (repo) [CLAIM-grb-03] |
Both appeared June 2025. GRB-B owns the GitHub org named GraphRAG-Bench; the registry most plausibly means GRB-B but both are examined. Whether GRB-A has its own repo or shares data with GRB-B: UNVERIFIED. Other uses of the name (leaderboards, vendor posts): not enumerated.

## 2. Primary problem, target workloads, example workflows
GRB-A: college-level multi-hop questions from twenty core textbooks across 16 disciplines; formats MCQ, true/false, multi-select, open-ended, fill-in-blank; some require math/programming; scores pipeline (construction, retrieval, generation) and reasoning coherence; nine GraphRAG methods tested [CLAIM-grb-01]. GRB-B: four task levels (fact retrieval, complex reasoning, contextual summarisation, creative generation) over Novel and Medical corpora; asks when GraphRAG underperforms vanilla RAG [CLAIM-grb-02, -03].

## 3. Feature inventory
| Item | GRB-A | GRB-B |
|---|---|---|
| Datasets | textbook-derived, size not stated on page (UNVERIFIED) | Novel, Medical on Hugging Face [CLAIM-grb-03] |
| Metrics | final answer plus reasoning coherence; named metrics UNVERIFIED | Accuracy, ROUGE-L (fact, reasoning); Accuracy, Coverage (summary); Accuracy, Factual Score, Coverage (creative) [CLAIM-grb-03] |
| Leaderboard | not verified | Novel and Medical leaderboards on project site [CLAIM-grb-03] |
| Pipeline-stage scoring | yes | yes |
| ACL/tenant/temporal | absent | absent |

## 4. Architecture diagram
```
corpus -> [GraphRAG method under test: graph build -> index -> retrieve -> generate]
questions (4 levels | 5 formats) -> answers -> metric scripts (LLM-judged parts) -> leaderboard
```

## 5. Under-the-hood (workload and scoring)
Workload design: GRB-B graded difficulty where fact retrieval favours chunk retrieval and higher levels test graph structure; GRB-A forces multi-hop domain reasoning. Scoring: ROUGE-L is lexical; Accuracy and Coverage/Factual Score for open tasks are LLM-judge based (hypothesis; judge model not verified). No formula for Coverage was read.

## 6. Requirements inferred
EOIP evaluation harness must accept a pluggable retriever, run vanilla-RAG vs graph-first A/B on identical corpora, and record judge model, seed, and cost.

## 7. Performance model: what it can and cannot show
Shows relative answer quality of graph vs chunk retrieval on public prose. Cannot show: ACL-filtered retrieval (J5), enterprise heterogeneity (code, tickets), local-model-only quality, latency or LLM token cost beyond what papers report, temporal truth. Quantitative results were not read; none are quoted here.

## 8. Strengths and matching
Explicit graded tasks; open data (GRB-B); both argue GraphRAG is not always better, supporting EOIP's "deterministic first" stance (J6). Match: run GRB-B Novel/Medical against BL-16 retrieval and against BM25 baseline.

## 9. Limitations
Intentional: public prose domains. Verified: no peer-reviewed venue visible for GRB-A; GRB-B venue claim from README only. Hypotheses: LLM-judge variance and judge contamination; textbook corpora likely in model pretraining. User/dev friction: GraphRAG methods tested need external LLM APIs by default (UNVERIFIED; air-gap needs local model swap).

## 10. Deployment, licensing, redistribution
GRB-B repo MIT; dataset licence on Hugging Face not verified (legal-review trigger: textbook-derived GRB-A text, novel text in GRB-B may be copyrighted; UNVERIFIED). No result-publication restrictions found. Air-gap: yes if datasets and a local judge are pre-staged.

## 11. Competitive delta against baseline
BL-16 "no benchmark vs strong plain RAG found"; BL-14 hashing embedder default. Delta: EOIP has no published comparison; this benchmark is the cheapest first one.

## 12. Cards
STR-grb-01 | GRB-B | graph-vs-vanilla A/B across four task levels | grb-02,-03 | evidence for when to route to graph | integrate | adopt task levels as J6 routing labels | EOIP graph-first >= BM25 on levels 2-3 and not worse by >2 points on level 1.
INV-grb-01 | GRB-A/B | lexical/LLM-judged scores ignore citation faithfulness and ACL (hypothesis; semantics) | add cited-span support check (see CRA-026 claim-support in repo history) and ACL canary | EXPERIMENT | falsifiable: judged accuracy vs citation precision correlation on 200 items.

## 13. Per-capability decisions
CAP-56 GraphRAG eval: INTEGRATE GRB-B data. CAP-60 grounded answers: EXPERIMENT (add citation scoring). CAP-55 hybrid: REFERENCE. Leaderboard submission: DEFER.

## 14. Tests and acceptance
Run GRB-B Novel+Medical with local 7-14B model on reference node; report per-level accuracy for BM25, hashing-vector, EOIP graph-first; fix judge model and log it; repeat 3 seeds.

## 15. Risks and open questions
Name collision causes mis-citation; data contamination; unknown GRB-A question counts and licence; leaderboard rules unseen.

## Appendix A. Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | two papers, MIT repo for B |
| D2 | 2 | prose-QA GraphRAG |
| D13 | 2,7,8 | primary dimension |
| D24 | 5,7,9 | judge and contamination caveats |
| D20 | 7 | no verified cost numbers |
| D3-D12,D14-D19,D21-D23 | N/A | evaluation dataset, no engine |

## Appendix B. Capability mapping
| CAP | Tech | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-56 | native (eval) | grb-02 | BL-16 | INTEGRATE | P1 |
| CAP-55 | partial | grb-03 | BL-13/14 | REFERENCE | P2 |
| CAP-60 | absent | grb-03 | BL-16 | EXPERIMENT | P1 |
| CAP-78 | native | grb-03 | U-06 | INTEGRATE | P1 |

## Appendix C. Evidence records
| ID | Product/ver/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| grb-01 | GRB-A v3 2025-06-20 | 16 disciplines, 20 textbooks, 5 question formats, 9 methods, preprint | Official (arXiv) | https://arxiv.org/abs/2506.02404 | 2025-06 / 2026-10-26 | 0.85 | none |
| grb-02 | GRB-B v3 2026-02-22 | four task levels; GraphRAG often underperforms vanilla RAG per prior studies | Official (arXiv) | https://arxiv.org/abs/2506.05690 | 2026-02 / 2026-10-26 | 0.85 | none |
| grb-03 | GRB-B repo | MIT; Novel/Medical; metrics per task; ICLR'26 per README; 514 stars | Official | https://github.com/GraphRAG-Bench/GraphRAG-Benchmark | n/a / 2026-10-26 | 0.75 | arXiv lists no venue |

## Appendix D. Assumptions
Registry name resolved to both; results not read so no scores quoted.
