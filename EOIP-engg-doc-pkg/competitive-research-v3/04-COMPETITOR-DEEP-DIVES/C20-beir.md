# C20 BEIR (zero-shot information-retrieval benchmark)

| Field | Value |
|---|---|
| Registry ID | T-C20-beir |
| Tier | B (standard retrieval benchmark; basis for CAP-53/54/55 quality gates) |
| Versions examined | `beir` 2.2.0 (PyPI, 2025-06-04); paper arXiv:2104.08663 v4 (2021-10), NeurIPS 2021 Datasets and Benchmarks |
| Verified on | 2026-10-26 |
| Worker | V33 |

## 1. Identity, current status, tier, and sources
Heterogeneous benchmark of 18 public datasets (paper) for zero-shot evaluation of retrieval models; Python toolkit Apache-2.0 [CLAIM-beir-01, -02]. Authors Thakur, Reimers, Rucklé, Srivastava, Gurevych (UKP Lab). Last PyPI release June 2025; repo HEAD activity not dated. Status: maintenance (inferred).

## 2. Primary problem, target workloads, example workflows
Test whether a retriever generalises out-of-domain. Paper finding: BM25 is a robust baseline; re-ranking and late-interaction give best average zero-shot performance at high compute cost; dense/sparse are efficient but often underperform [CLAIM-beir-01]. EOIP workflow: run BM25 (BL-13) and the hashing/optional dense retriever (BL-14) on 3-4 small datasets (SciFact, NFCorpus, FiQA, ArguAna) to gate regressions.

## 3. Feature inventory
| Item | Status |
|---|---|
| Datasets | repo table lists 19; 15 downloadable (MSMARCO, TREC-COVID, NFCorpus, NQ, HotpotQA, FiQA, ArguAna, Touche-2020, CQADupStack, Quora, DBPedia, SCIDOCS, FEVER, Climate-FEVER, SciFact); 4 non-public (BioASQ, Signal-1M, TREC-NEWS, Robust04) [CLAIM-beir-02] |
| Metrics | NDCG@k, MAP@k, Recall@k, Precision@k, MRR (via custom evaluate) [CLAIM-beir-02] |
| Models | lexical (Elasticsearch/BM25), dense, sparse, late interaction, re-rankers (paper) |
| Graph, ACL, multi-hop, temporal, citations | absent (HotpotQA subset is only multi-hop piece) |

## 4. Architecture diagram
```
dataset (corpus.jsonl, queries.jsonl, qrels.tsv) -> retriever (any) -> ranked doc ids
-> pytrec_eval-style scoring (NDCG@10 headline) -> per-dataset table
```

## 5. Under-the-hood (metrics)
Qrels give graded relevance; NDCG@k = DCG@k / ideal DCG@k with log2 discount; Recall@k = relevant retrieved in top k / relevant total; MAP averages precision at each relevant hit; MRR = mean reciprocal rank of first relevant hit. NDCG@10 is the headline in the paper (reasoned from standard IR; paper tables not re-read). Qrels are incomplete (pooled), so unjudged hits count as non-relevant, penalising novel retrievers.

## 6. Requirements inferred
Offline dataset staging with checksums; fixed tokenisation/analyser documented; per-dataset report with confidence intervals; separate "graph-expanded" run against base run.

## 7. Performance model: what it can and cannot show
Shows first-stage and rerank retrieval quality on public text, and compute-quality trade-off. Cannot show: ACL-filtered retrieval, entity/graph retrieval, enterprise text (code, tickets), multi-hop quality, freshness, latency under concurrent tenants. Public-corpora overlap with model pretraining weakens "zero-shot".

## 8. Strengths and matching
Broad, cheap, widely reported, so numbers are comparable across systems on the same dataset/metric. Match by adding an EOIP BEIR job (CAP-78) for BM25 parity: EOIP BM25 NDCG@10 within 0.02 of Elasticsearch/Pyserini BM25 on the same dataset.

## 9. Limitations
Verified: four datasets not distributable [CLAIM-beir-02]; repo features text and table disagree (17 vs 19 datasets). Intentional trade-off: English-centric, document-level retrieval. Hypotheses: annotation-pool bias; saturation by 2026 embedding models (see MTEB record). Friction: dataset sizes (MSMARCO, NQ, FEVER large).

## 10. Deployment, licensing, redistribution, publication
Code Apache-2.0 [CLAIM-beir-02]. Datasets keep original licences; maintainers say it is the user's responsibility to establish permission and cite owners [CLAIM-beir-02]. Per-dataset licences not individually verified here (legal-review trigger: yes for any redistribution inside EOIP images; keep datasets out of the product, download in CI only). No result-publication restrictions found. Air-gap: yes after staging.

## 11. Competitive delta against baseline
BL-13 BM25 and BL-14 hashing embedder have no recorded retrieval-quality figure (U-06). Delta: absent baseline measurements.

## 12. Cards
STR-beir-01 | comparable, multi-domain retrieval scoring | beir-01 | quick regression gate | integrate | CI job on 3 small datasets | NDCG@10 within 0.02 of reference BM25.
INV-beir-01 | no graph/ACL/multi-hop signal (semantics, proven by dataset list) | complement with GRB-B and multihop-qa sets plus EOIP ACL canary corpus; worse where only chunk retrieval matters. Options: (1) BEIR only, (2) BEIR + HotpotQA/MuSiQue + ACL canaries (selected), (3) EOIP-native enterprise retrieval benchmark. POC success: graph-first not worse than BM25 on BEIR subset by more than 0.02 and better on multi-hop. Decision ADOPT (2).

## 13. Per-capability decisions
CAP-54 full-text: INTEGRATE as regression gate. CAP-53 vector: INTEGRATE. CAP-55 hybrid fusion: EXPERIMENT (BEIR with RRF). Leaderboard publication: DEFER.

## 14. Tests and acceptance
Stage SciFact, NFCorpus, FiQA, ArguAna offline; run EOIP BM25, hashing vector, optional sentence-transformer, hybrid RRF; report NDCG@10 and Recall@100 with commit hash; no network egress during run.

## 15. Risks and open questions
Per-dataset licences; whether pip package pulls network at import; saturation; relevance of NDCG@10 gains to J5/J6.

## Appendix A. Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, 2.2.0 |
| D2 | 2 | zero-shot IR |
| D13 | 2,7 | retrieval metrics |
| D20 | 7 | compute-quality trade-off only qualitative |
| D24 | 5,7,9 | pooling bias, overlap |
| D3-D12,D14-D19,D21-D23 | N/A | dataset/toolkit |

## Appendix B. Capability mapping
| CAP | Tech | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-54 | native (eval) | beir-02 | BL-13 | INTEGRATE | P1 |
| CAP-53 | native (eval) | beir-02 | BL-14 | INTEGRATE | P1 |
| CAP-55 | partial | beir-01 | - | EXPERIMENT | P2 |
| CAP-78 | native | beir-02 | U-06 | INTEGRATE | P1 |

## Appendix C. Evidence records
| ID | Product/ver/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| beir-01 | paper v4 | 18 datasets, 10 systems; BM25 robust; rerank best but costly | Official | https://arxiv.org/abs/2104.08663 | 2021-10 / 2026-10-26 | 0.9 | none |
| beir-02 | repo + PyPI 2.2.0 | Apache-2.0; 19-row dataset table, 15 public; metrics; dataset-permission disclaimer | Official | https://github.com/beir-cellar/beir ; https://pypi.org/project/beir/ | 2025-06 / 2026-10-26 | 0.8 | 17 vs 19 dataset count |

## Appendix D. Assumptions
Metric formulas are standard IR definitions, not re-read from the paper.
