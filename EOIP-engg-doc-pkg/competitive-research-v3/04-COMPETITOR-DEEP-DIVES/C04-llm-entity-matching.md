# C04 — LLM-assisted entity matching (approach record)

| Field | Value |
|---|---|
| Registry ID | T-C04-llm-entity-matching |
| Tier | B — approach record (no single product) |
| Versions examined | Peeters, Steiner, Bizer, "Entity Matching using Large Language Models", arXiv 2310.11244 v1 2023-10-17 .. v4 2024-10-18; EDBT 2025 |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
An approach, not a product: use generative LLMs (hosted or local) as pairwise matchers, as match-rule generators, or as adjudicators of low-confidence pairs. Anchor study: Peeters and Bizer (later with Steiner), published at EDBT 2025; covers hosted and open-source LLMs run locally, zero-shot and with task data; finds no single best prompt, so prompts need per model and dataset tuning; also studies in-context demonstrations, generated matching rules and fine-tuning a hosted LLM [CLAIM-llmem-01]. Other lines (cited from memory, UNVERIFIED in this pass, conf 0.4): Narayan et al. foundation models for data wrangling (VLDB 2022), Jellyfish/Unicorn style tuned data-preparation models, and batch prompting for cost reduction. Maturity: research with fast-moving practice. Cross-refs: `C04-ditto.md` (fine-tuned PLM), `C04-splink.md`, `C04-zingg.md`.
Sources (3): arXiv abstract/versions page, EDBT venue listing, University of Mannheim repository entry.

## 2. Problem, workloads, workflows
Resolve ambiguous pairs that string/probabilistic scorers cannot (abbreviations, cross-language, product text). Workflows: (A) matcher for all candidate pairs (expensive); (B) **adjudicator** for the grey zone of a calibrated scorer; (C) rule synthesis: LLM drafts blocking/match rules which humans approve [CLAIM-llmem-01]; (D) explanation text for a reviewer.

## 3. Feature inventory (as an approach)
| Capability | Status |
|---|---|
| Zero-shot pair classification | present [CLAIM-llmem-01] |
| In-context demonstrations | present |
| Generated matching rules | present |
| Fine-tuning for matching | present (hosted); local fine-tune plausible |
| Local-model operation | present [CLAIM-llmem-01] |
| Calibrated probabilities | absent/partial (hypothesis: verbalised confidence is poorly calibrated) |
| Blocking | absent; needs upstream candidate generation |
| Determinism/auditability | partial (needs temperature 0, prompt+model version pinning) |

## 4. Architecture
```
candidates(blocked) -> calibrated scorer -> auto-accept | auto-reject
                                  \-> grey zone -> LLM adjudicator (local, egress-policy) -> verdict+rationale
                                                      \-> low confidence -> human review queue (BL-35)
audit: prompt hash, model id, input spans, verdict, reviewer override
```

## 5. Under-the-hood reconstruction
Serialise two records (attributes as `name: value` lines, truncated and PII-masked) into a prompt: "Do these refer to the same real-world entity? Answer Yes/No." Parse the first token; optionally compare logprobs of Yes/No for a score (hypothesis; needs local model/API with logprobs). Reduce cost by batch prompting several pairs per call and caching verdicts by canonical pair hash. Mitigations: self-consistency votes, position swap (A,B vs B,A), schema-agnostic serialisation. Security: prompt injection through record content (CAP-49) is a real threat because source data is untrusted: fence values, no tool access, constrained output grammar.

## 6. Requirements inferred
Deterministic invocation; per-tenant egress control (default-local model); evidence capture; cost budget per run; evaluation harness against labelled pairs; abstain option.

## 7. Performance and resource model
No numbers asserted. Cost = (#grey-zone pairs) x (tokens per pair) x model throughput; a 7-8B local model on CPU is slow, GPU strongly preferred (hypothesis). Failure modes: hallucinated rationales, order bias, injection, drift when the model is swapped, run-to-run nondeterminism.

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-llmem-01 | Little or no task training data; robust to unseen entities vs fine-tuned PLMs [CLAIM-llmem-01] | EXPERIMENT adjudicator on grey zone only |
| STR-llmem-02 | Natural-language rationale for reviewers | surface as non-authoritative note with evidence spans |
| STR-llmem-03 | Rule generation for human-approved matching rules | EXPERIMENT; rules stored in versioned mapping repo |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | Prompt sensitivity per model/dataset [CLAIM-llmem-01]; poor calibration (hypothesis) |
| Operational | Latency and GPU cost; model-version drift |
| Developer friction | prompt and evaluation engineering; reproducibility |
| Security | injection through data fields |
INV-llmem-01: *Target* LLM pairwise matching. *Limitation:* unaudited, unreproducible merges. *Root cause* semantics/governance (proven for nondeterminism, hypothesis for calibration). *Options:* (a) call local LLM in a script; (b) adjudicator service with pinned model, cache, deterministic decoding, structured verdict, advisory-only status; (c) distil adjudicator verdicts (after review) into a small cheap classifier. *Selected:* (b), then (c). Pattern: LLM verdict is an `INFERRED` claim, never an automatic merge; merges need score >= threshold or human approval. *POC:* WDC and ER-Magellan; success = grey-zone F1 gain >= 5 points over scorer alone with <= 2 s/pair on target hardware and 100% of verdicts reproducible at temperature 0. *Defensibility:* governance integration, not model access. *Decision:* EXPERIMENT. No seed hypothesis targets this approach.

## 10. Deployment, licensing, viability
Fits EOIP only with a local model (air-gap) and egress policy; model licences vary (flag per-model; legal review for Llama-community-style terms, record only). No code to redistribute.

## 11. Competitive delta vs EOIP baseline
BL-36 absent; BL-35 partial review queue; BL-27 has a `LocalOllamaProvider` (`moonshot/ontology_induction.py`), so a local-LLM harness exists to reuse for a pair adjudicator. No LLM ER code verified in baseline.

## 12. Cards
STR-llmem-01..03; INV-llmem-01.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Grey-zone adjudication (CAP-31) | EXPERIMENT |
| Rule generation | EXPERIMENT |
| LLM as primary matcher | REJECT |
| Verdict cache + audit | BUILD |

## 14. Tests and acceptance
Offline benchmark with position-swap and injection-seeded records; acceptance: reproducible, injection-resistant, measurable lift on the grey zone, reviewer agreement study.

## 15. Risks and open questions
Calibration, cost on large grey zones, model licences, whether batch prompting harms accuracy; later literature not surveyed.

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | approach, research-grade |
| D2 | 2 | grey-zone adjudication |
| D3 | 4 | service pattern |
| D4–D8 | N/A | no storage |
| D9 | N/A | |
| D10 | 2,5,9 | core: match decisions, rationale, evidence |
| D11 | N/A | |
| D12 | 5 | LLM inference |
| D13 | 5 | prompt fencing |
| D14 | N/A | |
| D15 | 4 | human review |
| D16 | N/A | |
| D17 | N/A | |
| D18 | 5,9 | injection, egress |
| D19 | 6 | per-tenant egress |
| D20 | 7 | no numbers |
| D21 | 10 | model licences |
| D22 | N/A | |
| D23 | N/A | not searched |
| D24 | 1 | one anchor paper verified at abstract level |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | partial (adjudication) | llmem-01 | BL-36 absent | EXPERIMENT | P2 |
| CAP-51 | plugin | llmem-01 | egress policy per constraints | REUSE | P1 |
| CAP-49 | absent | llmem-02 | n/a | BUILD | P1 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-llmem-01 | arXiv 2310.11244 v4 / EDBT 2025 | LLMs as EM matchers, hosted and local, zero-shot and with data; no single best prompt; demonstrations, generated rules, fine-tuning studied | Third-party report (paper abstract via search) | https://arxiv.org/abs/2310.11244v4 | 2023-10-17 (v1), 2024-10-18 (v4) / 2026-10-18 | 0.8 | numbers not read |
| CLAIM-llmem-02 | n/a | prompt injection through data fields applies to LLM matchers | Reasoned inference | n/a | 2026-10-18 | 0.6 | none |

## Appendix D — Assumptions
Numeric results not verified; mitigations in section 5 are design hypotheses.
