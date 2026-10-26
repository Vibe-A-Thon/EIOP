# C05 Docling

| Field | Value |
|---|---|
| Registry ID | T-C05-docling |
| Tier | B (layout-aware parsing reuse candidate) |
| Versions examined | docling 2.142.1 (2026-10-23; year inferred) |
| Verified on | 2026-10-18 (re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
Docling: document converter started at IBM Research Zurich, hosted by LF AI & Data, repo `docling-project/docling`, MIT code [CLAIM-docl-01]. Releases every 1-2 days in Oct (2.141.0 on 20 Oct, 2.142.0 on 22 Oct, 2.142.1 on 23 Oct) [CLAIM-docl-02]. Default layout model "Heron" (RT-DETR v2, 42.9M params) is Apache-2.0 [CLAIM-docl-03]. Other model weights (TableFormer, OCR engines, VLMs such as Granite-Docling, Nemotron-Parse) have their own licences: UNVERIFIED here (Granite-Docling card returned 401).

## 2. Primary problem, workloads, workflows
Convert PDF, Office, HTML, images, audio, email etc. to a lossless `DoclingDocument` and Markdown/JSON for RAG and KG ingest. EOIP flow: `file -> docling convert -> DoclingDocument items (text, table, picture, bbox, page) -> SourceEvent`.

## 3. Feature inventory
| Feature | Status |
|---|---|
| PDF layout, reading order, table structure, code, formulas, image classification | present [CLAIM-docl-04] |
| Many non-PDF formats (DOCX, PPTX, XLSX, HTML, EPUB, ODF, email, LaTeX, audio) | present |
| Provenance: page numbers and bboxes per item | present [CLAIM-docl-05] |
| Character offsets into source | absent in what was read (UNVERIFIED for text-layer PDFs) |
| OCR (EasyOCR default, Tesseract, RapidOCR, others) | optional |
| VLM pipelines | optional, new models added each release [CLAIM-docl-02] |
| Remote services | off unless `enable_remote_services=True` [CLAIM-docl-06] |
| CLI, Python SDK, `docling-serve` REST, MCP server, LangChain/LlamaIndex/Haystack | present |

## 4. Architecture
```
input -> format backend (pdf text-layer parser | docx/xlsx/html parsers)
PDF -> page images -> layout detector (Heron) -> [OCR if needed]
    -> TableFormer -> assemble reading order -> DoclingDocument
DoclingDocument -> export Markdown / HTML / DocTags / lossless JSON
models cache: ~/.cache/docling/models or --artifacts-path [CLAIM-docl-06]
```

## 5. Under-the-hood reconstruction
Data model: `DoclingDocument` (package `docling-core`) holds typed items with provenance (page, bbox) [CLAIM-docl-05]. Pipeline: standard staged pipeline of specialised models (layout detector derived from RT-DETR retrained on DocLayNet and other data; TableFormer for table structure) plus optional OCR [CLAIM-docl-07]. Recent releases harden against untrusted input (decompressed-size limits for DOCX/XLSX/EPUB, bounded VLM output) [CLAIM-docl-02]. No persistence or query layer. Security boundary is the host process.

## 6. Requirements inferred
FR: convert with bbox provenance; offline model prefetch. NFR: pre-staged weights; pinned versions; per-document resource caps.

## 7. Performance and resource model
Authors' benchmark (89 PDFs; 8 vCPU EPYC 7R13, 32 GB; M3 Max; L4 GPU), Docling 2.5.2 with EasyOCR: 3.1 s/page x86 CPU, 1.27 s M3 Max, 0.49 s L4 [CLAIM-docl-07]. Memory not reported. Competitor-run comparison by Marker's maintainers (olmocr-bench, B200 host): docling (GPU) overall 50.3, digital-only 64.0, 2.1 pages/s versus Marker balanced 76.0 [CLAIM-docl-08]; both are interested parties. Independent: a GROBID paper reports Docling TEDS 0.858 on PubTables vs 0.715 for GROBID+PP [CLAIM-docl-09]. No independent head-to-head across parsers found.

## 8. Strengths
Best-documented offline story of the group; MIT; explicit bbox provenance; table structure model; fast release cadence; neutral foundation hosting. Match: use as default PDF parser. Exceed: add a parser-neutral span anchor.

## 9. Limitations
Verified: output and model set change weekly (reproducibility burden). Trade-off: weights fetched from Hugging Face on first run unless prefetched [CLAIM-docl-06]. Model licences heterogeneous (legal-review trigger for any bundled weights). Vendor-run benchmarks disagree (CLAIM-docl-07 vs 08). Hypothesis: CPU-only throughput of VLM pipelines is poor; not measured.

## 10. Deployment, licensing, viability
Self-host library/container; air-gap viable with prefetch and artifacts path [CLAIM-docl-06]. Code MIT; Heron Apache-2.0; other weights UNVERIFIED, so redistribution of a bundled image requires checking each model card (legal-review trigger: mixed model licences, no conclusion).

## 11. Competitive delta
No document parser in EOIP baseline (BL-26 covers JSON only; BL-23 connectors emit SourceEvents). BL-41 evidence manifests could carry `{page, bbox}`; EOIP `nlp/pipeline.py` `Entity.start/end` are text offsets, not bbox: two anchor kinds are needed.

## 12. Cards
STR-docl-01 | Docling | bbox+page provenance on every item | CLAIM-docl-05 | page-level citations in answers | integrate | store `SpanAnchor{page,bbox,text_hash}` in evidence | 95% of table cells anchored on 100 PDFs.
STR-docl-02 | Docling | explicit offline switch and remote-service gate | CLAIM-docl-06 | air-gap default | match | EOIP egress gateway wraps parser config | packet capture shows zero egress.
INV-docl-01 | weekly drift and mixed weights (proven) | root: maturity/licensing | options: pin+mirror; native conformance corpus per parser version; long-term parser-neutral golden set. Select pin+golden set. Benchmark: output diff <2% on golden set across minor upgrades. Defensible: tenant-specific golden sets. EXPERIMENT.
Seed hypotheses: none targeted.

## 13. Per-capability decisions
CAP-32 PDF/Office parsing: INTEGRATE (default candidate). CAP-38 bbox provenance: REUSE format, BUILD anchor contract. CAP-50: INTEGRATE with prefetch. VLM pipelines: DEFER.

## 14. Tests / PoC
200-doc corpus (scanned + digital + tables) on 4 vCPU, no network: s/page, table TEDS vs gold, anchoring rate, RSS peak; repeat on two docling versions for drift. Accept: zero egress, TEDS within 5 points of vendor claim, drift <2%.

## 15. Risks / open questions
Per-model licences; torch dependency size on a one-node install; VLM CPU cost; independent accuracy evidence.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | MIT, LF AI&Data, active |
| D2 | 2 | RAG ingest |
| D3 | 4,5 | staged models |
| D4-D8 | N/A | stateless library |
| D9 | 2,11 | parse stage |
| D10 | 3,12 | bbox yes, offsets unknown |
| D11 | 9 | drift |
| D12 | 5 | layout, TableFormer, OCR |
| D13-D16 | N/A | upstream |
| D17 | 3 | SDK, CLI, serve, MCP |
| D18 | 5 | hardening |
| D19 | N/A | library |
| D20 | 7 | vendor-run numbers |
| D21 | 10 | OSS only |
| D22 | 3 | open JSON |
| D23 | N/A | none |
| D24 | 7 | conflicting benchmarks |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-32 | native | 04 | absent | INTEGRATE | P1 |
| CAP-38 | partial | 05 | BL-41 partial | REUSE+BUILD | P1 |
| CAP-50 | native | 06 | BL-45 | INTEGRATE | P1 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| docl-01 | 2.142.1 | MIT; LF AI&Data; IBM origin | Officially documented | https://docling-project.github.io/docling/ ; PyPI JSON | 2026-10-26 | 0.9 | none |
| docl-02 | 2.141-2.142.1 | release dates and hardening notes | Officially documented | https://github.com/docling-project/docling/releases | 10-26 | 0.8 | year inferred |
| docl-03 | Heron | Apache-2.0, RT-DETRv2, 42.9M | Officially documented | https://huggingface.co/docling-project/docling-layout-heron | 10-26 | 0.9 | none |
| docl-04 | 2.142 | feature list | Officially documented | docs index above | 10-26 | 0.85 | none |
| docl-05 | tech report | DoclingDocument stores bbox, page | Officially documented | https://arxiv.org/html/2501.17887 | 10-26 | 0.85 | none |
| docl-06 | docs | prefetch, artifacts path, remote-services gate | Officially documented | https://docling-project.github.io/docling/usage/advanced_options/ | 10-26 | 0.9 | none |
| docl-07 | 2.5.2 | 3.1/1.27/0.49 s per page | Third-party report (authors) | arXiv 2501.17887 | 10-26 | 0.6 | CLAIM-docl-08 |
| docl-08 | docling GPU | olmocr-bench 50.3 | Third-party report (competitor) | https://github.com/datalab-to/marker | 10-26 | 0.4 | CLAIM-docl-07 |
| docl-09 | PubTables | TEDS 0.858 | Independent paper | https://arxiv.org/pdf/2609.26381 (via search) | 10-26 | 0.5 | not re-read |

## Appendix D. Assumptions
Years inferred as 2026 for GitHub dates. Non-Heron model licences left UNVERIFIED rather than assumed.
