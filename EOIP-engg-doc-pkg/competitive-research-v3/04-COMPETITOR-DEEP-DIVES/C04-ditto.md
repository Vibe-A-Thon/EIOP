# C04 — Ditto (deep entity matching, Megagon Labs)

| Field | Value |
|---|---|
| Registry ID | T-C04-ditto |
| Tier | B — transformer matching reference |
| Versions examined | `megagonlabs/ditto` master, no tagged releases; last commit 2021-09-24 |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
Ditto fine-tunes pre-trained language models for entity matching as sequence-pair classification (VLDB 2021 paper "Deep Entity Matching with Pre-Trained Language Models", Li et al.; paper not opened here, title from memory, conf 0.6). Repo `github.com/megagonlabs/ditto`, Apache-2.0, 29 commits, 321 stars, no releases [CLAIM-ditto-01][CLAIM-ditto-02]. Status: **research artefact, effectively unmaintained** since 2021-09-24 (not archived). Pinned stack is Python 3.7.7, PyTorch 1.9, Transformers 4.9.2, NVIDIA Apex for fp16 [CLAIM-ditto-01]. Cross-refs: `C04-splink.md`, `C04-zingg.md`, `C04-llm-entity-matching.md`.
Sources (3): repo page, LICENSE, commits Atom feed.

## 2. Primary problem, target workloads, example workflows
Classify candidate pairs as match/non-match with far fewer labels than classical deep matchers. Workflow: serialise each record as `COL name VAL x COL ...`; fine-tune `distilbert` (also bert, albert) on labelled pairs; optional MixDA augmentation, domain-knowledge span tagging, TF-IDF summarisation; evaluate on ER-Magellan (13 datasets: Structured, Dirty, Textual) and WDC product matching (small to xlarge) [CLAIM-ditto-01]. No blocking is included (assumed external; hypothesis conf 0.6).

## 3. Feature inventory
| Feature | Status |
|---|---|
| PLM fine-tuned pair classifier | present |
| MixDA augmentation (del, swap, drop_col, append_col, all) | present |
| Domain knowledge injection (general, product) | present |
| Summarisation of long fields | present |
| Blocking, clustering, merge/split, survivorship | absent |
| Serving API, model registry | absent |
| Explanations | absent (attention-only, hypothesis) |
| Reported F1 in README | absent [CLAIM-ditto-01] |

## 4. Architecture
```
labelled pairs --> serialise(COL/VAL) --> [DA, DK, summarise] --> PLM fine-tune (GPU)
candidate pairs (from external blocker) --> serialise --> PLM --> P(match)
```

## 5. Under-the-hood reconstruction
Input `[CLS] serialise(a) [SEP] serialise(b) [SEP]`; linear head on `[CLS]`; cross-entropy; MixDA interpolates the representation of original and augmented sequences (per README operators list). Infer: no state besides checkpoint. No concurrency/security concerns (offline script). Hypothesis: inference cost = O(#candidate pairs) forward passes, so external blocking is mandatory.

## 6. Requirements inferred
GPU for training (flags `--use_gpu`, `--fp16`; VRAM not stated); labelled training set; deterministic serialisation; blocking upstream.

## 7. Performance and resource model
No numbers in the README. Training needs NVIDIA GPU and Apex for fp16; inference is a transformer forward per pair (CPU possible but slow; hypothesis). Failure modes: domain shift, unseen entity types, label scarcity, stale pinned dependencies preventing install on current Python/CUDA.

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-ditto-01 | Learns semantic similarity beyond string distance (e.g., abbreviations, product text) | EXPERIMENT as optional second-stage reranker on review-queue pairs |
| STR-ditto-02 | Data augmentation to cut label needs | adopt augmentation idea for synthetic training pairs |
| STR-ditto-03 | Public benchmark suites referenced (ER-Magellan, WDC) | use for 15-VALIDATION plan |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | Pairwise only; no transitive closure or cluster consistency; no calibrated uncertainty |
| Operational | GPU, old pinned stack, no releases (verified) |
| Developer friction | script-style, not a package |
| User-reported | not collected |
INV-ditto-01: *Target* Ditto master. *Limitation:* unmaintained research code with GPU dependency blocks one-node CPU-first and air-gap deployment. *Root cause* maturity/deployment (proven). *Options:* (a) run reference code in a pinned container for benchmark only; (b) reimplement a small cross-encoder reranker with ONNX/CPU inference using HF checkpoints; (c) use local LLM judge (see llm-entity-matching). *Selected:* (b) behind an optional "pair scorer" interface, never the primary matcher. *POC:* ER-Magellan Structured+Dirty, success = F1 within 3 points of Ditto reference with CPU p95 < 200 ms per pair batch of 32 (target, not measured). *Decision:* EXPERIMENT. Seed hypotheses: none target Ditto.

## 10. Deployment, licensing, viability
Apache-2.0; offline-capable after downloading base model weights (weight licences are separate and must be checked per model; legal-review item for weights, not code). GPU strongly preferred. Not one-node-first friendly.

## 11. Competitive delta vs EOIP baseline
BL-36 absent; BL-35 review queue partial. Ditto provides a learned pair scorer EOIP lacks, but should only be a pluggable reranker beneath a calibrated matcher (Splink/Zingg) with human review.

## 12. Cards
STR-ditto-01..03; INV-ditto-01.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Learned pair reranker (CAP-31) | EXPERIMENT |
| Fine-tuning infrastructure | DEFER |
| Reference code reuse | REJECT (stale stack) |
| Benchmarks | REUSE |

## 14. Tests and acceptance
Reproduce on ER-Magellan 3 datasets in container; compare to Splink-only and to Splink+reranker for F1 and reviewer-queue size.

## 15. Risks and open questions
Weights licence; domain shift on enterprise data; reproducing published F1 (not stated in repo).

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, stale |
| D2 | 2 | pair classification |
| D3 | 4 | script pipeline |
| D4–D8 | N/A | no storage/query/reasoning |
| D9 | N/A | |
| D10 | 2,5 | match probability only |
| D11 | N/A | |
| D12 | 5 | PLM fine-tuning |
| D13–D14 | N/A | |
| D15–D16 | N/A | |
| D17 | 3 | scripts |
| D18–D19 | N/A | |
| D20 | 7 | GPU; no numbers |
| D21 | 10 | Apache-2.0 |
| D22 | N/A | |
| D23 | N/A | not searched |
| D24 | 1 | README only; paper unopened |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | partial (pair scoring only) | ditto-01 | BL-36 absent | EXPERIMENT | P2 |
| CAP-61 | partial | ditto-01 | n/a | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-ditto-01 | master | models bert/distilbert/albert; MixDA ops; DK; summarisation; ER-Magellan and WDC; GPU/Apex; pinned versions; no F1 in README; no releases | Officially documented | https://github.com/megagonlabs/ditto | n/a / 2026-10-18 | 0.85 | none |
| CLAIM-ditto-02 | master | Apache-2.0; last commit 2021-09-24 | Officially documented | LICENSE; https://github.com/megagonlabs/ditto/commits.atom | 2026-10-18 | 0.9 | none |

## Appendix D — Assumptions
Paper claims not opened; blocking assumed external; inference cost reasoning is inference.
