# C05 spaCy

| Field | Value |
|---|---|
| Registry ID | T-C05-spacy |
| Tier | B (local NLP pipeline reuse candidate) |
| Versions examined | spaCy 3.8.16 (PyPI; release date UNVERIFIED); pipelines `en_core_web_*` 3.8.x |
| Verified on | 2026-10-18 (re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
Explosion's industrial NLP library, MIT, Python `>=3.9,<3.15` [CLAIM-spacy-01]. Still releasing (3.8.16). Pipelines are separate packages (`[lang]_core_web_sm/md/lg/trf`) with their own versioning [CLAIM-spacy-02]. Pipeline licences vary by language: sampled releases show MIT for zh/uk/xx_ent_wiki but CC BY-SA 3.0 for `xx_sent_ud_sm`; English licence not confirmed here [CLAIM-spacy-03]. Related: REBEL ships a spaCy component (see tier-C file); GLiNER has a spaCy wrapper (not verified).

## 2. Primary problem, workloads, workflows
Tokenisation, tagging, dependency parse, NER, rule matching, text classification on CPU. EOIP use: replace/augment regex entity spotting in `nlp/pipeline.py` with statistical NER plus `EntityRuler` for ontology terms; feed Presidio as its NLP engine.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Statistical NER (OntoNotes labels) | present |
| `Matcher`, `PhraseMatcher`, `EntityRuler` rule engines | present (documented API; not re-fetched) |
| Span character offsets (`start_char`/`end_char`) | present (API knowledge, 0.8) |
| Transformer pipeline `trf` | optional (GPU preferred) |
| Custom training (`spacy train`, config system) | present |
| Coreference | experimental/external only |
| Relation extraction | absent in core (components via projects) |
| Server / UI | absent (library); CLI present |

## 4. Architecture
```
text -> tokenizer (rules) -> Doc
Doc -> tok2vec/transformer -> tagger -> parser -> ner -> (EntityRuler) -> Doc.ents
Doc.ents: label, start_char, end_char
packaging: pip wheel per pipeline; load from local path
```

## 5. Under-the-hood reconstruction
Doc/Span/Token objects over a shared vocab (Cython); pipeline components share `tok2vec` listeners; NER is a transition-based parser over spans (hypothesis from public design); `trf` uses a Hugging Face transformer. Stateless; thread-safe only per `Language` object with care. No security layer; untrusted-text DoS bounded by `nlp.max_length`.

## 6. Requirements inferred
FR: offsets stable across versions; label set mapped to EOIP ontology. NFR: wheels mirrored for air-gap; deterministic outputs given pinned model; CPU throughput budget per ingest node.

## 7. Performance and resource model
Vendor figures (OntoNotes 5.0 dev; 10k Reddit comments for speed): `en_core_web_lg` NER F 85.5, 10,014 words/s CPU; `en_core_web_trf` NER F 89.8, 684 words/s CPU, 3,768 GPU [CLAIM-spacy-04]. Domain shift is large: an independent PII benchmark (PIIBench) reports `en_core_web_lg` span F1 0.087 on PII-style text [CLAIM-spacy-05], so OntoNotes F is not a predictor of enterprise-text quality. Memory not measured.

## 8. Strengths
Mature, MIT, fast CPU path, rule+statistical hybrid with offsets, huge ecosystem, trainable on EOIP gold data. Match by adoption; exceed via ontology-bound EntityRuler generated from the graph.

## 9. Limitations
Verified: fixed label inventory (OntoNotes), not zero-shot; poor transfer to PII/enterprise entities [CLAIM-spacy-05]. Trade-off: `trf` accuracy costs ~15x throughput on CPU [CLAIM-spacy-04]. Licence: non-English pipelines vary; check per package. Friction: pipeline compatibility pinned to spaCy minor; no documented offline download procedure on the page read [CLAIM-spacy-02] (wheels/`pip --no-index` is the practical route; hypothesis).

## 10. Deployment, licensing, viability
Embedded library; fully air-gap viable via mirrored wheels. MIT code; pipeline licence per package (legal-review trigger only for CC BY-SA/NC pipelines).

## 11. Competitive delta
EOIP `nlp/pipeline.py` is pure Python, deterministic, no model downloads, `Entity(text,kind,start,end,confidence)` (BL-46 neighbourhood; BL-45 DLP is separate regex). spaCy adds statistical NER and dependency parse; EOIP's `Entity` contract already matches `Doc.ents`, so adoption is an adapter. EOIP lock has no ML libs (baseline section 2), so spaCy would be an optional extra.

## 12. Cards
STR-spacy-01 | spaCy | rules+statistics with char offsets | CLAIM-spacy-04 | cheap evidence spans | integrate | optional `SpacyExtractor` behind `Entity` contract | offsets round-trip 100% on 1k docs.
INV-spacy-01 | closed label set, domain shift (proven) | root: algorithm/data | alt: ontology-driven labels via zero-shot (GLiNER) with spaCy tokeniser; options: quick (EntityRuler from graph), native (hybrid ensemble), long-term (fine-tune on reviewed claims). Select quick + ensemble. Benchmark: F1 on 300 hand-labelled EOIP docs vs lg/trf. Defensible: gold set from review queue. EXPERIMENT.
Seed hypothesis (deterministic first, local models second): validated in direction.

## 13. Per-capability decisions
CAP-32 NER: INTEGRATE optional; rule matching: REUSE concepts, keep in-house default; CAP-28: DEFER; coreference/RE: REJECT as spaCy features (see other records).

## 14. Tests / PoC
Run `lg` and `trf` on 300 labelled docs (4 vCPU, offline wheels): per-type P/R/F, words/s, RSS; verify `text[start_char:end_char]==ent.text`. Accept: offsets exact; F1 reported with confidence interval.

## 15. Risks / open questions
English pipeline licence per package (re-read model cards); numpy/torch footprint in a locked install; maintenance continuity of Explosion.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | MIT, active |
| D2 | 2 | CPU NLP |
| D3 | 4 | pipeline |
| D4-D8 | N/A | in-process library |
| D9 | 2 | ingest-stage NLP |
| D10 | 3,12 | offsets |
| D11 | 9 | model-version pinning |
| D12 | 5,7 | NER models |
| D13-D16 | N/A | upstream |
| D17 | 3 | training config |
| D18 | 5 | max_length |
| D19 | N/A | library |
| D20 | 7 | vendor throughput |
| D21 | 10 | per-package licence |
| D22 | 10 | open formats |
| D23 | N/A | none |
| D24 | 7 | PII transfer evidence |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-32 | native (NER) | 04 | partial in-house (nlp/pipeline.py) | INTEGRATE | P2 |
| CAP-33 | partial | 05 | BL-46 | INTEGRATE via Presidio | P2 |
| CAP-50 | native | 01 | BL-45 | INTEGRATE | P2 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| spacy-01 | 3.8.16 | MIT; Python range | Officially documented | https://pypi.org/pypi/spacy/json | 2026-10-26 | 0.9 | none |
| spacy-02 | docs | pipeline packaging/versioning; no offline procedure shown | Officially documented | https://spacy.io/models | 10-26 | 0.8 | none |
| spacy-03 | spacy-models | licences vary (MIT; CC BY-SA 3.0 for xx_sent_ud_sm) | Officially documented | https://github.com/explosion/spacy-models/releases | 10-26 | 0.7 | English licence not seen |
| spacy-04 | lg/trf | NER F 85.5/89.8; words/s | Officially documented (vendor) | https://spacy.io/usage/facts-figures | 10-26 | 0.8 | different domain from EOIP |
| spacy-05 | PIIBench | spaCy lg span F1 0.0873 | Independent paper | https://arxiv.org/pdf/2604.15776 (via search summary) | 10-26 | 0.5 | not re-read |

## Appendix D. Assumptions
Span API and rule engines taken from known spaCy API, flagged where not re-fetched. Release date of 3.8.16 not obtained.
