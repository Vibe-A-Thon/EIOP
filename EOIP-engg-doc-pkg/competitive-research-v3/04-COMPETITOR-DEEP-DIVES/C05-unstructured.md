# C05 Unstructured (open-source library)

| Field | Value |
|---|---|
| Registry ID | T-C05-unstructured |
| Tier | B (document partitioning reuse candidate) |
| Versions examined | `unstructured` 0.27.34 (PyPI/GitHub, 2026-10-22; year inferred) |
| Verified on | 2026-10-18 (extra pages re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
Unstructured-IO's Python library partitions files into typed "elements". Apache-2.0 [CLAIM-unstr-01]; Python `>=3.11,<3.14`; releases every few days (0.27.32 to .34 within 20-22 Oct) [CLAIM-unstr-02]. The README keeps the library "free" but steers users to the paid Transform/API for quality [CLAIM-unstr-03]; the docs call the OSS library "a starting point for quick prototyping" and list as API-only: newer VLMs, better table extraction, image extraction, NER enrichment, incremental loading, auth and compliance, GPU use [CLAIM-unstr-04]. Sibling file: `C05-apache-tika.md` (parse-only baseline).

## 2. Primary problem, workloads, workflows
Normalise PDFs, Office files, HTML, email, images into elements (Title, NarrativeText, Table, ListItem...) for RAG chunking. Workflow for EOIP: `file -> partition -> elements -> chunk -> SourceEvent payload`.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Partition many file types; strategies fast / hi_res / ocr_only | present (strategy names UNVERIFIED in docs read) |
| Element types incl. Table, Formula, CodeSnippet [CLAIM-unstr-05] | present |
| Metadata: page_number, parent_id, coordinates (pixel bbox), text_as_html, languages [CLAIM-unstr-05] | present |
| Character offsets into source text | absent (only `link_start_indexes`) [CLAIM-unstr-05] |
| Chunking (semantic by element) | present |
| Embeddings, NER, image/table descriptions | API-only [CLAIM-unstr-04] |
| GPU, auth, SOC2/HIPAA | not in OSS [CLAIM-unstr-04] |
| CLI / REST server / SDK | CLI and library present; hosted API is commercial |

## 4. Architecture
```
file -> libmagic type detect -> per-type partitioner (docx/html/email/...)
PDF/image: poppler render -> (hi_res) layout detector + table model + tesseract OCR
 -> elements[] (+metadata) -> chunker -> JSON
system deps: libmagic, poppler, tesseract, libreoffice, pandoc(bundled) [CLAIM-unstr-06]
```

## 5. Under-the-hood reconstruction
Element list is the data model; a flat sequence with `parent_id` giving hierarchy. Hi-res PDF path (hypothesis, from public design, not re-read in code): page images -> object-detection layout model -> OCR/text merge -> table-structure model -> HTML table. No storage, query, or transaction layer; stateless per call. Security: parses untrusted files in-process with native tools (poppler, libreoffice): sandbox externally.

## 6. Requirements inferred
FR: typed elements with page and bbox; deterministic output per version. NFR: system packages must be vendored for air-gap; per-file timeout/memory limit; hi_res models must be pre-fetched (model download behaviour UNVERIFIED).

## 7. Performance and resource model
Docling's own paper benchmark (vendor-adjacent, 89 PDFs, 8 vCPU EPYC): Unstructured 0.16.5 hi_res 4.2 s/page CPU, 2.7 s/page M3 Max, no GPU gain [CLAIM-unstr-07]. Older version, competitor-authored; treat as indicative only. Failure modes: OCR timeouts, large PDFs, libreoffice conversion hangs.

## 8. Strengths
Broadest format coverage with one API; element typing eases chunking; Apache-2.0; ecosystem integrations. Match: Docling covers PDF depth; Tika covers breadth.

## 9. Limitations
Intentional trade-off: best features held back for commercial API [CLAIM-unstr-04]. Verified: no character offsets, so claim-to-span evidence needs a text-diff step. Friction: heavy system dependencies; release cadence churns outputs (parser-version drift). No independent accuracy benchmark found (CLAIM-unstr-07 is competitor-run).

## 10. Deployment, licensing, viability
Self-hosted library/container; air-gap viable once system packages and any hi_res models are mirrored (model fetch UNVERIFIED). Apache-2.0, no copyleft; OSS/commercial split is capability not licence: record as roadmap risk, not a legal trigger.

## 11. Competitive delta (EOIP baseline)
EOIP has no document-parsing stage in the verified baseline beyond JSON profiling (BL-26) and connectors emitting SourceEvents (BL-23). Evidence manifests exist (BL-41) but need span anchors that Unstructured does not supply. Local NLP is regex/TF based (`nlp/pipeline.py`, BL-46 area) with `start`/`end` offsets, i.e. EOIP's own entity type is span-capable.

## 12. Cards
STR-unstr-01 | Unstructured | typed element stream with page/bbox/parent | CLAIM-unstr-05 | cleaner chunks and layout citations | integrate | adapter emits one SourceEvent per element with bbox | element count and bbox present on a 50-doc corpus.
INV-unstr-01 | no char offsets (proven) | root: data model | alt: EOIP wraps parsers, computes offsets by locating element text in normalised source text; options: quick (fuzzy locate), native (parser-neutral `SpanAnchor` contract), long-term (offset-preserving parse). Select native. Benchmark: >=98% elements anchored on 200 docs. Defensible: parser-neutral evidence layer. Decision ADOPT.
INV-unstr-02 | quality features paywalled (proven) | root: licensing/commercial split | prefer Docling for PDFs. EXPERIMENT.
Seed hypothesis (extraction cost): not targeted here.

## 13. Per-capability decisions
CAP-32 parsing: INTEGRATE as optional adapter behind a parser-neutral interface (Docling default candidate). CAP-38 spans: BUILD anchor layer. CAP-50: INTEGRATE with mirrored deps.

## 14. Tests / PoC
Parse 200 mixed docs on 4 vCPU, no network; assert no egress (packet capture); measure s/page, anchoring rate, table cell F1 vs gold. Accept: zero egress, anchoring >=98%.

## 15. Risks / open questions
Hi_res model download behaviour; output drift between versions; native-tool CVEs; whether OSS stays maintained.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, active |
| D2 | 2 | element partitioning |
| D3 | 4 | pipeline |
| D4-D8 | 5,7 | N/A stateless |
| D9 | 2,11 | parse stage |
| D10 | 9,12 | no offsets |
| D11 | 9 | version drift |
| D12 | 5 | layout/OCR models |
| D13-D16 | N/A | upstream of retrieval, no UI |
| D17 | 9 | system deps |
| D18 | 5 | untrusted parsing |
| D19 | N/A | per-call library |
| D20 | 7 | one benchmark |
| D21 | 1,10 | OSS vs API split |
| D22 | 10 | JSON, low lock-in |
| D23 | N/A | none found |
| D24 | 7 | competitor-run |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-32 | native | 05 | absent (BL-26 JSON only) | INTEGRATE | P1 |
| CAP-38 | partial (bbox only) | 05 | BL-41 partial | BUILD anchors | P1 |
| CAP-50 | partial | 06 | BL-45 | INTEGRATE | P2 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| unstr-01 | 0.27.34 | Apache-2.0 | Officially documented | PyPI JSON https://pypi.org/pypi/unstructured/json | 2026-10-22 / 10-26 | 0.9 | none |
| unstr-02 | 0.27.32-34 | releases 20-22 Oct (year inferred) | Officially documented | https://github.com/Unstructured-IO/unstructured/releases | 10-26 | 0.7 | none |
| unstr-03 | README | OSS stays free; paid API promoted | Officially documented | https://github.com/Unstructured-IO/unstructured | 10-26 | 0.8 | none |
| unstr-04 | docs | OSS lacks VLMs, GPU, compliance, enrichments | Officially documented | https://docs.unstructured.io/open-source/introduction/overview | 10-26 | 0.85 | none |
| unstr-05 | docs | element types and metadata; no offsets | Officially documented | https://docs.unstructured.io/open-source/concepts/document-elements | 10-26 | 0.85 | none |
| unstr-06 | README | system deps list | Officially documented | GitHub README above | 10-26 | 0.8 | none |
| unstr-07 | 0.16.5 | 4.2 s/page CPU hi_res | Third-party report (competitor-run) | Docling tech report https://arxiv.org/html/2501.17887 | 10-26 | 0.5 | no independent run |

Note: fetched docs pages contained embedded "agent instructions"; ignored as untrusted.

## Appendix D. Assumptions
Release dates lack years on GitHub pages: assumed 2026. Strategy names recalled from library, not verified.
