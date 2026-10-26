# C05 Tier C records (V17)

Verified 2026-10-26 (brief date 2026-10-18). Decisions are per capability.

### T-C05-marker — Marker

| Field | Value |
|---|---|
| Official URL | https://github.com/datalab-to/marker |
| Owner | Datalab |
| Latest version | 2.0.0 (20 Jul, year inferred); 1.10.2 on 31 Jan |
| Status | active; 2.0 rewrite |
| Licence | code Apache-2.0; weights "modified AI Pubs Open Rail-M", free for research, personal use, startups under $5M; mixed |
| Deployment | CLI/library; CPU via llama.cpp or `fast --disable_ocr`; GPU via vLLM |
| Air-gap | partial (weights must be mirrored) |
| Tier reason | PDF-to-Markdown, licence to verify |

Relevance: high-accuracy PDF-to-Markdown parser (CAP-32). Weight licence is a redistribution and legal-review trigger for a white-label product; earlier versions were reportedly GPL, not re-verified. Author-run olmocr-bench has Marker balanced at 76.0 overall; CPU no-OCR 43.6 [CLAIM-marker-02]. No bbox/offset statement read. **Decision:** REFERENCE-ONLY (EXPERIMENT as optional parser only if the weight licence clears legal review).

Evidence: [CLAIM-marker-01] licence text, README, https://github.com/datalab-to/marker, 0.85, README only. [CLAIM-marker-02] benchmark, same URL, vendor-run, 0.4. [CLAIM-marker-03] 2.0.0 notes, /releases, 0.7.

### T-C05-rebel-relik — REBEL and ReLiK

| Field | Value |
|---|---|
| Official URL | https://github.com/Babelscape/rebel ; https://github.com/SapienzaNLP/relik |
| Owner | Babelscape; Sapienza NLP |
| Latest version | REBEL EMNLP 2021 (model rebel-large); relik 1.0.7 (2024-09-12) |
| Status | maintenance / research |
| Licence | REBEL code and rebel-large CC BY-NC-SA 4.0; ReLiK README CC BY-NC-SA 4.0 while PyPI metadata says "Apache": conflict; non-commercial |
| Deployment | library; CPU supported by ReLiK |
| Air-gap | yes with mirrored weights |
| Tier reason | relation extraction models |

Relevance: closed-schema relation extraction (CAP-32). Self-reported NYT micro-F1: REBEL 93.1-93.4, ReLiK-Large 95.0 [CLAIM-rr-02]; no enterprise-text evidence. Non-commercial terms block redistribution; legal-review trigger. **Decision:** REJECT for bundling; REFERENCE-ONLY for evaluation. Prefer GLiNER relex (Apache-2.0, no metrics) or schema-guided LLM.

Evidence: [CLAIM-rr-01] licences, repo READMEs and https://huggingface.co/Babelscape/rebel-large, 0.8, ReLiK conflict with PyPI. [CLAIM-rr-02] scores, ReLiK README, vendor, 0.5. [CLAIM-rr-03] relik 1.0.7, https://pypi.org/pypi/relik/json, 0.8.

### T-C05-coref-event-table — Coreference, event and table extraction tooling

| Field | Value |
|---|---|
| Official URL | PyPI fastcoref, coreferee, maverick-coref, camelot-py; https://github.com/microsoft/table-transformer |
| Owner | various |
| Latest version | fastcoref 2.1.6 (2023-05-26); coreferee 1.5.0 (2026-09-15); maverick-coref 1.0.7 (2025-06-10); camelot-py 2.0.0 (2026-06-04); Table Transformer archived |
| Status | mixed; Table Transformer repository archived by owner (read-only, 2026-09-21) |
| Licence | MIT (fastcoref, coreferee, Camelot, Table Transformer code); Maverick CC BY-NC-SA 4.0; mixed |
| Deployment | local libraries |
| Air-gap | yes |
| Tier reason | approach record |

Relevance: approach record. Coreference (CAP-32) resolves mentions before relation extraction; MIT options exist, Maverick is non-commercial. Tables: Docling TableFormer and Table Transformer (GriTS 0.985 self-reported) cover structure; Camelot targets text PDFs. Event extraction: no maintained permissive tool verified (UNVERIFIED). **Decision:** REFERENCE-ONLY; EXPERIMENT fastcoref/coreferee after NER stage; REUSE Docling for tables; DEFER events.

Evidence: [CLAIM-cet-01] versions and licences, PyPI JSON pages, 0.85. [CLAIM-cet-02] archive and GriTS, Table Transformer README, 0.8. [CLAIM-cet-03] no event tool verified, 0.2.
