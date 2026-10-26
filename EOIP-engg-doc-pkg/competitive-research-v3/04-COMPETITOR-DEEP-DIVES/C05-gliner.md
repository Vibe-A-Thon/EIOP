# C05 GLiNER

| Field | Value |
|---|---|
| Registry ID | T-C05-gliner |
| Tier | B (zero-shot local NER) |
| Versions examined | `gliner` 0.2.29 (PyPI, 2026-09-08); checkpoints gliner_large-v2.1, gliner_multi_pii-v1, knowledgator gliner-bi-base-v2.0 and gliner-relex-large-v1.0 |
| Verified on | 2026-10-18 (re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
Zero-shot NER with a bidirectional encoder (paper arXiv 2311.08526, labelled work in progress, v1 only on the page read) [CLAIM-gli-01]. Library by urchade, Apache-2.0, 0.2.29 uploaded 2026-09-08 [CLAIM-gli-02]. Ecosystem: GLiNER.cpp, gline-rs, GLiNER2 (multi-task NER/classification/extraction), GLiClass, GLinker, multi-task paper 2406.12925 [CLAIM-gli-03]. Checkpoint licences vary per model card (see 10). Registry means the urchade/GLiNER project and its community checkpoints.

## 2. Primary problem, workloads, workflows
Extract arbitrary entity types named at inference time without training, on CPU. EOIP use: label set = ontology classes (`Person`, `Service`, `Incident`...) to propose PROPOSED entities (BL-40) from text; PII spotting as an extra recogniser inside Presidio.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Zero-shot entity types as free text labels | present |
| Uni-encoder, bi-encoder, decoder, streaming-span variants | present as separate checkpoints [CLAIM-gli-03] |
| Joint relation extraction (gliner-relex) | optional, model card gives thresholds, no metrics [CLAIM-gli-05] |
| PII checkpoints (gliner_multi_pii-v1, stream-pii) | present |
| CPU, INT8, ONNX export, torch.compile | present per README [CLAIM-gli-03] |
| Character offsets in public output | UNVERIFIED: decoder emits token-level start/end [CLAIM-gli-04]; README example prints only text and label |
| Server / UI | absent |

## 4. Architecture
```
text -> word splitter -> [labels ; words] -> encoder (DeBERTa-class)
 -> span representations x label embeddings -> sigmoid scores
 -> greedy decode (token start/end) -> entities
```

## 5. Under-the-hood reconstruction
Decoder builds `Span(start, end, entity_type, score)` where start/end are token positions (inclusive) [CLAIM-gli-04]; span score is sigmoid probability (span mode) or min of inside/start/end probabilities (token mode). Mapping to character offsets requires the splitter's token-to-char map: whether the public `predict_entities` returns it was not confirmed (POC item). Bi-encoder variants precompute label embeddings (hypothesis: enables many labels cheaply). No state, storage or security layer; model weights are untrusted pickles/safetensors, so pin hashes.

## 6. Requirements inferred
FR: label set per tenant ontology; threshold per entity type; exact char offsets. NFR: INT8/ONNX CPU path; checkpoint licence recorded per deployment; no network at load.

## 7. Performance and resource model
No benchmark table read: model cards show benchmark images only and gliner-relex reports no metrics [CLAIM-gli-05]. Paper abstract claims it outperforms ChatGPT and fine-tuned LLMs zero-shot [CLAIM-gli-01]. Independent: a 1,000-record self-reported leaderboard gives GLiNER partial micro-F1 0.32 vs Presidio 0.195 [CLAIM-gli-06]; PIIBench reports low F1 for all systems on narrow-domain-trained models [CLAIM-gli-07]. `gliner_large-v2.1` is 459M parameters [CLAIM-gli-08]. Latency and memory on CPU: NOT PUBLICLY VERIFIED.

## 8. Strengths
Zero-shot ontology-labelled NER, CPU-friendly, small versus LLMs, Apache-2.0 library and v2.1 checkpoints. Exceed by binding labels to the live ontology and logging threshold per type.

## 9. Limitations
Verified: README does not show offsets [CLAIM-gli-03]. Licence: older `gliner_multi` family is reported CC-BY-NC-4.0 by secondary sources (v2.1 and PII model Apache-2.0) [CLAIM-gli-09]. Trade-off: recall/precision depend on label wording and threshold (hypothesis; common observation, not measured). Long text needs chunking (~384-token window, from library knowledge, UNVERIFIED). No relation or coreference in base models.

## 10. Deployment, licensing, viability
Embedded Python; air-gap viable with mirrored weights. Library Apache-2.0. Per-checkpoint licences: Apache-2.0 for gliner_large-v2.1, gliner_multi_pii-v1, gliner-bi-base-v2.0 and gliner-relex-large-v1.0 (model cards read) [CLAIM-gli-08][CLAIM-gli-10]; bi-base card lists upstream encoders whose licences were not checked. Legal-review trigger: non-commercial checkpoints in the family; require per-checkpoint licence allowlist.

## 11. Competitive delta
EOIP `nlp/pipeline.py` is deterministic and model-free with `start/end` (BL-46 area); no zero-shot capability. GLiNER fills "local models second" of the seed hypothesis (Master Prompt row on Graphiti). Outputs must enter as PROPOSED claims with evidence (BL-39/40/41).

## 12. Cards
STR-gli-01 | GLiNER | ontology-labelled zero-shot NER on CPU | CLAIM-gli-01,08 | no LLM cost for entity proposal | integrate | adapter turns ontology class names into labels | F1 >= regex+spaCy on 300 docs.
INV-gli-01 | offsets unverified, token-level spans (proven for decoder) | root: data model | options: quick (re-locate text in source), native (wrap with char map), long-term (contribute upstream). Select native char-map wrapper; falsify with exact round-trip on 1k docs. Defensible: evidence-anchor contract. ADOPT.
INV-gli-02 | checkpoint licence heterogeneity (proven) | root: licensing | allowlist enforced at load. ADOPT.

## 13. Per-capability decisions
CAP-32 NER: EXPERIMENT -> INTEGRATE optional (P2). CAP-33: INTEGRATE inside Presidio. CAP-38 spans: BUILD wrapper. Relation extraction via gliner-relex: EXPERIMENT (no metrics).

## 14. Tests / PoC
300 EOIP-style docs, gold labels, 4 vCPU offline: P/R/F per type at thresholds 0.3-0.7; compare regex, spaCy lg, GLiNER large-v2.1, multi_pii; verify offsets; INT8 vs FP32 delta. Accept: offsets exact, per-type recall reported, licence allowlist test passes.

## 15. Risks / open questions
Offset API; label-wording sensitivity; hallucinated entities with no source anchor; model supply chain; independent F1 on enterprise text.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0 lib, active |
| D2 | 2 | zero-shot NER |
| D3 | 4 | encoder |
| D4-D8 | N/A | stateless |
| D9 | 2 | ingest-stage |
| D10 | 5,9,12 | offsets unverified |
| D11 | N/A | none |
| D12 | 5,7 | span scoring |
| D13-D16 | N/A | upstream |
| D17 | 3 | ONNX etc. |
| D18 | 5 | weights supply chain |
| D19 | N/A | library |
| D20 | 7 | no numbers |
| D21 | 10 | checkpoint licences |
| D22 | 10 | HF weights |
| D23 | N/A | none |
| D24 | 7 | thin evidence |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-32 | native NER, partial RE | 03,05 | partial in-house | EXPERIMENT | P2 |
| CAP-33 | plugin (PII checkpoints) | 03 | BL-46 | INTEGRATE | P2 |
| CAP-38 | partial | 04 | BL-41 | BUILD wrapper | P1 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| gli-01 | paper v1 | outperforms ChatGPT zero-shot | Third-party report (authors) | https://arxiv.org/abs/2311.08526 | 2026-10-26 | 0.5 | numbers not read |
| gli-02 | 0.2.29 | Apache-2.0, uploaded 2026-09-08 | Officially documented | https://pypi.org/pypi/gliner/json | 10-26 | 0.9 | none |
| gli-03 | README | variants, CPU/ONNX/INT8, no offsets shown | Officially documented | https://github.com/urchade/GLiNER | 10-26 | 0.8 | none |
| gli-04 | main | decoder spans are token-level | Observed in source | https://raw.githubusercontent.com/urchade/GLiNER/main/gliner/decoding/decoder.py | 10-26 | 0.7 | public wrapper unread |
| gli-05 | relex-large-v1.0 | joint RE, thresholds, no metrics, Apache-2.0 | Officially documented | https://huggingface.co/knowledgator/gliner-relex-large-v1.0 | 10-26 | 0.85 | none |
| gli-06 | leaderboard | GLiNER 0.32 vs Presidio 0.195 | Third-party report | https://benchmarklist.com/models/gliner/ (via search) | 10-26 | 0.3 | self-reported |
| gli-07 | PIIBench | all systems low F1 | Independent paper | https://arxiv.org/pdf/2604.15776 | 10-26 | 0.5 | not re-read |
| gli-08 | large-v2.1 | Apache-2.0; 459M params | Officially documented | https://huggingface.co/urchade/gliner_large-v2.1 | 10-26 | 0.9 | none |
| gli-09 | gliner_multi | CC-BY-NC-4.0 (secondary) | Third-party report | https://superlinked.com/glossary/what-is-gliner (via search) | 10-26 | 0.5 | model card unread |
| gli-10 | multi_pii-v1, bi-base-v2.0 | Apache-2.0 | Officially documented | https://huggingface.co/urchade/gliner_multi_pii-v1 ; https://huggingface.co/knowledgator/gliner-bi-base-v2.0 | 10-26 | 0.9 | none |

## Appendix D. Assumptions
Treated offsets as unverified rather than assuming char-level. "Other GLiNER forks" disambiguation is a caution, not an enumerated finding.
