# C20 RAGAS (RAG evaluation framework)

| Field | Value |
|---|---|
| Registry ID | T-C20-ragas |
| Tier | B (de facto RAG metric library; candidate evaluator in EOIP CI) |
| Versions examined | ragas 0.4.3 on PyPI (2026-01-13); repo now at vibrantlabsai/ragas (HEAD 2026-10-26); paper arXiv:2309.15217 v2 (2025-04-28) |
| Verified on | 2026-10-26 |
| Worker | V33 |

## 1. Identity, current status, tier, and sources
Python evaluation framework for RAG and LLM apps; Apache-2.0 [CLAIM-ragas-01]. Repo observed under `vibrantlabsai/ragas` (earlier `explodinggradients/ragas`; ownership change reasoned from redirect, UNVERIFIED). 16.2k stars, 385 open issues, 251 open PRs [CLAIM-ragas-02]. Paper by Es, James, Espinosa-Anke, Schockaert: reference-free RAG evaluation, arXiv only [CLAIM-ragas-03]. Latest PyPI release is nine months old at access date; repo activity not dated on page.

## 2. Primary problem, target workloads, example workflows
Score a RAG pipeline without human labels: retrieval quality, faithfulness of answer to retrieved context, answer relevance; also synthetic test-set generation and agent/tool metrics [CLAIM-ragas-01, -04]. Workflow: collect (question, contexts, answer, optional reference) rows, run metrics with a judge LLM, aggregate per release.

## 3. Feature inventory
| Family | Metrics (docs) | Needs LLM |
|---|---|---|
| RAG | Context Precision, Context Recall, Context Entities Recall, Noise Sensitivity, Response Relevancy, Faithfulness, multimodal variants | mostly yes (inferred) |
| Nvidia | Answer Accuracy, Context Relevance, Response Groundedness | yes (inferred) |
| Agents/tools | Topic Adherence, Tool Call Accuracy, Tool Call F1, Agent Goal Accuracy | partly |
| NL comparison | Factual Correctness, Semantic Similarity, BLEU, CHRF, ROUGE, Exact Match, String Presence | non-LLM for lexical ones |
| SQL | Execution-based Datacompy, SQL Query Equivalence | mixed |
| General | Aspect Critic, rubrics scoring | yes |
Source [CLAIM-ragas-04]. Per-metric LLM/embedding dependency not stated on the index page.

## 4. Architecture diagram
```
dataset rows -> Metric (prompt templates) -> judge LLM (pluggable) [+ embeddings]
           -> per-row score -> aggregate -> (optional) tracing/app integration
```

## 5. Under-the-hood (metric definitions)
Documented at the paper level: faithfulness = fraction of answer statements supported by context (statement decomposition then verification); answer relevance via LLM-generated questions compared to the original by embedding similarity; context relevance via extracted sentences (hypothesis from the paper's design; exact current formulas not re-read; verify against docs before relying). Scores are LLM outputs, therefore stochastic and judge-model dependent.

## 6. Requirements inferred
Local judge model support (Ollama-compatible) is mandatory for air-gap; pinned prompts; seeds and judge identity recorded per run; metric adapters over EOIP RetrievalResult (answer_citations).

## 7. Performance and resource model: what it can and cannot show
Shows relative faithfulness/relevance trends on a fixed set with a fixed judge. Cannot show absolute correctness, ACL safety, leakage, or tenant isolation; scores shift when the judge changes. Cost scales with rows x LLM calls per metric (several per row; exact counts not verified). Failure modes: judge hallucination, parse failures, rate limits.

## 8. Strengths and matching
Wide metric catalogue, reference-free options, active community. EOIP can reuse metric definitions but EOIP already has a deterministic cited-span claim-support check (commit c264c07 per repo log), which is stronger for auditability; combine both.

## 9. Limitations
Hypothesis/verified split: verified high issue/PR backlog [CLAIM-ragas-02]; hypotheses: LLM-judge bias, weak reproducibility across judge versions; defaults pull OpenAI-style providers (UNVERIFIED for 0.4.3). Dev friction: rapid API changes between 0.x versions (UNVERIFIED).

## 10. Deployment, licensing, redistribution
Apache-2.0, pip install, embeddable as dev dependency [CLAIM-ragas-01]; no benchmark-publication clause; legal-review trigger: none. Air-gap: partial-to-yes with local judge; telemetry/usage tracking behaviour UNVERIFIED (check before offline use).

## 11. Competitive delta against baseline
BL-16 (graph-first retrieval) has no LLM-judge metric suite; EOIP has deterministic support check only. Delta: RAGAS adds breadth, EOIP adds determinism.

## 12. Cards
STR-ragas-01 | broad reference-free metric catalogue | ragas-04 | fast J6 A/B scoring | integrate | wrap as optional evaluator plugin, local judge | scores reproducible within +/-0.03 over 3 runs on fixed judge.
INV-ragas-01 | judge-dependence (hypothesis, semantics) | EOIP pairs LLM metrics with deterministic claim-support and citation precision; worse when answers are abstractive paraphrases that span-matching misses. Options: (1) use as-is, (2) dual-score (selected), (3) calibrated local judge with human-labelled set. POC: 100 human-labelled answers; success: judge-vs-human kappa >= 0.6. Decision EXPERIMENT.

## 13. Per-capability decisions
CAP-78 harness: INTEGRATE (optional). CAP-60 grounded answers metric: REUSE metric definitions. CAP-58 SQL/query equivalence metrics: EXPERIMENT for text-to-Cypher (see C08-text-to-query). Test-set generation: EXPERIMENT.

## 14. Tests and acceptance
Run Faithfulness, Context Precision/Recall, Response Relevancy on 200-item EOIP set with local judge, no network (verify with egress block); variance check; compare to deterministic support check agreement.

## 15. Risks and open questions
Ownership/rename churn; telemetry; judge drift; metric formula versions; whether 0.4.x requires cloud providers by default.

## Appendix A. Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, 0.4.3 |
| D2 | 2 | RAG/agent eval |
| D13,D14 | 3,13 | metrics incl. SQL |
| D17 | 3,6 | Python lib |
| D18 | 10 | telemetry unverified |
| D24 | 5,7,9 | judge variance |
| D3-D12,D15,D16,D19-D23 | N/A | evaluator, not engine |

## Appendix B. Capability mapping
| CAP | Tech | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-78 | native | ragas-01 | U-06 | INTEGRATE | P1 |
| CAP-60 | native | ragas-04 | BL-16 | REUSE | P1 |
| CAP-58 | partial | ragas-04 | - | EXPERIMENT | P2 |

## Appendix C. Evidence records
| ID | Product/ver/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| ragas-01 | 0.4.3, 2026-01-13 | Apache-2.0, Python >=3.9, evaluation framework | Official | https://pypi.org/project/ragas/ | 2026-01 / 2026-10-26 | 0.9 | none |
| ragas-02 | repo | 16.2k stars, 385 issues, 251 PRs, vibrantlabsai org | Official | https://github.com/explodinggradients/ragas (redirect) | n/a / 2026-10-26 | 0.7 | rename unverified |
| ragas-03 | paper v2 | reference-free RAG evaluation | Official | https://arxiv.org/abs/2309.15217 | 2023-09/2025-04 / 2026-10-26 | 0.9 | none |
| ragas-04 | docs | metric families listed | Official | https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/ | n/a / 2026-10-26 | 0.85 | LLM dependency per metric not stated |

## Appendix D. Assumptions
Metric formulas taken from paper design, flagged hypothesis; release cadence inferred from one PyPI date.
