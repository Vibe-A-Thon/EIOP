# C05 Microsoft Presidio (now Data Privacy Stack Presidio)

| Field | Value |
|---|---|
| Registry ID | T-C05-presidio |
| Tier | B (PII detection reuse candidate, BL-46) |
| Versions examined | presidio-analyzer 2.2.365 (2026-10-25; year inferred) |
| Verified on | 2026-10-18 (re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
Presidio detects and anonymises PII in text, images and structured data. Rename/ownership trap resolved: the repo moved from `microsoft/presidio` to the independent, community-governed `data-privacy-stack/presidio`; MIT continues; Docker images moved from `mcr.microsoft.com/presidio-*` to `ghcr.io/data-privacy-stack/presidio-*`, old MCR tags no longer updated [CLAIM-pres-01]. Release 2.2.365 (25 Oct, year inferred) follows 2.2.364 (22 Jul) and 2.2.363 (28 Jun) [CLAIM-pres-02]. PyPI licence MIT, Python `>=3.10,<3.15` [CLAIM-pres-02]. Transition date not stated on the page read.

## 2. Primary problem, workloads, workflows
Find and redact/tokenise PII before storage, indexing or LLM egress. EOIP flow: SourceEvent text -> Analyzer -> findings with offsets -> classification label on evidence and DLP at egress; Anonymizer for DSAR/redaction exports.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Regex PatternRecognizer with context words, validate/invalidate hooks | present [CLAIM-pres-03] |
| Checksum validators for national IDs (e.g. PESEL, ABN, HETU) | present, being extended each release [CLAIM-pres-02] |
| NER via spaCy, Stanza, Hugging Face NlpEngine | present [CLAIM-pres-03] |
| Result fields entity_type, score, start, end | present [CLAIM-pres-03] |
| Custom recognizers (Flair, SpanMarker samples; GLiNER as recognizer: possible, not verified) | present |
| Anonymizer operators, batch deanonymise, image redactor, structured data | present [CLAIM-pres-02][CLAIM-pres-04] |
| Evaluation tooling | present (link only) [CLAIM-pres-03] |
| REST services (analyzer, anonymizer), Docker | present |
| Offline operation | stated by docs index [CLAIM-pres-04]; model download step not verified |
| Guaranteed accuracy | explicitly not guaranteed [CLAIM-pres-04] |

## 4. Architecture
```
text -> NlpEngine (spaCy etc.: tokens, lemmas, NER)
 -> recognizers[] (pattern | checksum | NER-mapped | custom)
 -> ContextAwareEnhancer (lemma context words boost score)
 -> overlap/duplicate resolution -> RecognizerResult[start,end,score]
 -> Anonymizer operators (replace|mask|hash|encrypt|custom)
```

## 5. Under-the-hood reconstruction
Recognizer registry per language; each returns scored spans; enhancer adds to score when context lemmas appear nearby (default lemma match, multi-word context needs a custom enhancer) [CLAIM-pres-03]. Conflict resolution keeps highest score/longest span (hypothesis from design; release notes mention a REMOVE_INTERSECTIONS fix) [CLAIM-pres-02]. Stateless. Recent notes: quadratic-time duplicate checks removed, tokenizer-based chunking for NER recognizers [CLAIM-pres-02].

## 6. Requirements inferred
FR: span offsets, per-entity thresholds, language-specific recognisers, reversible tokens only through EOIP vault. NFR: no network at inference; deterministic given pinned spaCy model; findings never persist raw values.

## 7. Performance and resource model
No vendor accuracy or throughput promise [CLAIM-pres-04]. Independent: PIIBench reports Presidio span F1 0.1385 (spaCy lg 0.0873) on a 1,398-record subset, all systems low [CLAIM-pres-05]; an out-of-distribution robustness paper finds Presidio shows the smallest generalisation gap, recall 1.000 on SSN and IP, precision stable, recall drops elsewhere [CLAIM-pres-06]; a self-reported leaderboard has Presidio last of five, micro-F1 0.195, recall 0.07 on high-sensitivity types [CLAIM-pres-07]. Interpretation: structured identifiers good, free-text names/addresses weak; evidence is mixed and dataset-dependent. Latency and memory: NOT PUBLICLY VERIFIED here.

## 8. Strengths
Mature recogniser library with checksums, context scoring, 30+ locale additions per quarter, anonymiser operators, MIT. Match by adopting; exceed by adding tenant-defined recognisers and ontology-aware sensitivity.

## 9. Limitations
Verified: accuracy not guaranteed [CLAIM-pres-04]; weak on unstructured names in independent tests [CLAIM-pres-05,07]. Governance change: new volunteer-run organisation (continuity risk, hypothesis). Friction: default NER needs a spaCy model download (air-gap staging). Quality dependent on the chosen NER backend.

## 10. Deployment, licensing, viability
Python library or two Docker services; air-gap viable with mirrored spaCy models and images. MIT; no copyleft. Image redaction needs OCR (Tesseract) as optional dependency (hypothesis). No legal trigger beyond model-licence checks for NER backends.

## 11. Competitive delta
EOIP `privacy/scanner.py` (BL-46): 5 regex types (email, phone, SSN, card, IP), no checksum (Luhn absent), property-level scan over `MemoryGraphStore`, findings keep `raw_value`. `egress/dlp.py` (BL-45): regex+entropy+dictionary, stdlib only. Presidio gives ~dozens of validated recognisers, context scoring and NER, with offsets that fit EVIDENCE spans; EOIP's scanner does not operate on text with offsets nor on non-memory backends. Retaining `raw_value` in findings is a privacy defect to fix regardless.

## 12. Cards
STR-pres-01 | Presidio | checksum+context recognisers with offsets | CLAIM-pres-02,03 | fewer false positives on IDs | integrate | `PresidioDetector` implements EOIP `PIIDetector` protocol, replaces regex list, keeps BL-45 as fast gate | card/SSN precision >=0.98 on 1k synthetic records.
INV-pres-01 | weak free-text NER recall (proven by CLAIM-pres-05,07) | root: algorithm | options: quick (Presidio+spaCy lg), native (add GLiNER PII checkpoint and ontology dictionaries as recognisers), long-term (tenant-trained detector from review labels). Select native. Benchmark: per-type recall on 500 EOIP-style docs; success: recall >=0.8 names at precision >=0.8 (target, untested). Defensible: tenant dictionaries + labels. Decision EXPERIMENT.
INV-pres-02 | governance migration (proven) | root: maturity | pin versions, vendor-mirror. ADOPT.

## 13. Per-capability decisions
CAP-33 PII detection: REUSE (INTEGRATE as optional extra; keep in-house regex as zero-dependency fallback). Anonymiser: REUSE operators but keep EOIP vault for reversible tokens (BL-45). Image redaction: DEFER. CAP-50: INTEGRATE.

## 14. Tests / PoC
Synthetic + hand-labelled corpus (names, emails, IDs, addresses, secrets), 4 vCPU offline: per-entity P/R/F vs `scanner.py`, offsets exact, docs/s, RSS; run with and without spaCy model. Accept: zero egress; Presidio >= in-house on every type; offsets round-trip.

## 15. Risks / open questions
False sense of security (no guarantee); locale coverage; spaCy model licences; post-transition maintenance; findings must not store raw text.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | MIT, moved org |
| D2 | 2 | PII ingest/egress |
| D3 | 4 | recognisers + NLP |
| D4-D8 | N/A | stateless |
| D9 | 2,11 | ingest gate |
| D10 | 3,11 | spans, PII handling |
| D11 | N/A | none |
| D12 | 5 | NER, context |
| D13 | N/A | upstream |
| D14-D16 | N/A | none |
| D17 | 3 | custom recognisers |
| D18 | 11,15 | raw_value defect |
| D19 | 12 | tenant dictionaries |
| D20 | 7 | no numbers |
| D21 | 10 | MIT |
| D22 | 10 | open |
| D23 | N/A | none |
| D24 | 7 | mixed evidence |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-33 | native | 02,03 | BL-46 partial, BL-45 | REUSE | P1 |
| CAP-38 | partial (spans) | 03 | BL-41 | INTEGRATE | P2 |
| CAP-51 | partial | 04 | BL-45 | INTEGRATE | P2 |
| CAP-50 | native | 04 | BL-45 | INTEGRATE | P2 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| pres-01 | repo | moved to data-privacy-stack; MIT; images moved | Officially documented | https://github.com/data-privacy-stack/presidio/blob/main/docs/project_transition.md | 2026-10-26 | 0.85 | none |
| pres-02 | 2.2.363-365 | release content, MIT, Python range | Officially documented | https://github.com/microsoft/presidio/releases ; https://pypi.org/pypi/presidio-analyzer/json | 10-26 | 0.8 | year inferred |
| pres-03 | analyzer docs | recognizers, result fields, enhancer, NLP engines | Officially documented | https://presidio.dataprivacystack.org/analyzer/ | 10-26 | 0.9 | none |
| pres-04 | docs index | offline, image/structured, not guaranteed | Officially documented | https://microsoft.github.io/presidio/ (redirect notice summary) | 10-26 | 0.6 | summary only |
| pres-05 | PIIBench | Presidio F1 0.1385; spaCy 0.0873 | Independent paper | https://arxiv.org/pdf/2604.15776 | 10-26 | 0.5 | not re-read |
| pres-06 | OOD paper | smallest gap; SSN/IP recall 1.0 | Independent paper | https://arxiv.org/pdf/2609.03464 | 10-26 | 0.5 | not re-read |
| pres-07 | leaderboard | micro-F1 0.195 | Third-party report | https://benchmarklist.com/benchmarks/redact/ | 10-26 | 0.3 | self-reported |

## Appendix D. Assumptions
Years inferred 2026. EOIP baseline details of `scanner.py` read from source lines 55-62 this run (regex list, no Luhn).
