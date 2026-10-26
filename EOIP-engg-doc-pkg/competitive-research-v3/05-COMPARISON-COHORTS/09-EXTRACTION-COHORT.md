# Cohort 09 — Unstructured Extraction and PII / Secret Detection

| Field | Value |
|---|---|
| Cohort ID | COH-09 |
| Workload class | Ingest-time conversion of documents and text into structured, span-anchored evidence, plus detection of personal data and secrets before data enters the graph or leaves through the egress gateway |
| Members (deep dives) | [Apache Tika](../04-COMPETITOR-DEEP-DIVES/C05-apache-tika.md), [Unstructured](../04-COMPETITOR-DEEP-DIVES/C05-unstructured.md), [Docling](../04-COMPETITOR-DEEP-DIVES/C05-docling.md), [spaCy](../04-COMPETITOR-DEEP-DIVES/C05-spacy.md), [GLiNER](../04-COMPETITOR-DEEP-DIVES/C05-gliner.md), [LLM schema extraction](../04-COMPETITOR-DEEP-DIVES/C05-llm-schema-extraction.md) (Neo4j LLM Graph Builder, LlamaIndex extractors, LangChain `LLMGraphTransformer`), [Presidio](../04-COMPETITOR-DEEP-DIVES/C05-presidio.md), [Secret scanners](../04-COMPETITOR-DEEP-DIVES/C05-secret-scanners.md) (gitleaks, Betterleaks, TruffleHog, detect-secrets) |
| Tier C records | [C05-tier-c-records-V17](../04-COMPETITOR-DEEP-DIVES/C05-tier-c-records-V17.md): Marker; REBEL and ReLiK; coreference, event and table tooling (all REFERENCE-ONLY) |
| Reference columns | HugeGraph, Neo4j, Neptune (extraction rows only; the engines themselves do no PII or secret detection) |
| EOIP status basis | `01-SYSTEM-BASELINE.md` (BL, ad9937b) superseded by `01a-BASELINE-DELTA-HEAD.md` (HEAD 896e06d). Where 01a is silent (it has no `fileparse` row), the HEAD source was read directly and is marked "source read" |
| Related BL | BL-23..26 (ingest), BL-41 (evidence), BL-45 (egress/DLP), BL-46 (privacy) |
| Journeys | J12 arbitrary-input onboarding, J16 air-gapped operation (no named journey for extraction; both constrain it) |
| Date | 2026-10-26 |

Count: 8 deep dives (counting the secret-scanner and LLM-extraction group records once each), 3 Tier C records.

## 1. Workload class and comparison basis

**Customer workloads.** (a) Turn PDFs, Office files, email and archives into text with page/offset anchors so that every extracted claim can cite a source span. (b) Propose entities and relations from text without sending client data to an external model. (c) Find PII and credentials in ingested content before indexing, and in outbound LLM payloads before egress.

**Why comparable.** Every member sits in the "parsing / normalization" or "evidence and provenance" stage of the canonical pipeline (Master Prompt §4.3 item 4). They are compared on what they emit (text, layout, spans, labels), how they behave on a CPU-only single node, whether they can run offline, and whether their code *and model weights* are redistributable in a white-label product.

**Sub-groups.** Parsers (Tika, Unstructured, Docling; Marker is Tier C). Entity extractors (spaCy, GLiNER, LLM extractors; REBEL/ReLiK Tier C). Sensitive-data detectors (Presidio, secret scanners). The sub-groups are complementary, not substitutes.

**Excluded.** OCR engines and vision-language models as standalone components (no deep dive), GraphRAG retrieval (cohort 06), and C19 scanners owned by another worker (C05-secret-scanners §1). Cloud-only extraction APIs are excluded under the no-mandatory-SaaS constraint.

**Evidence quality note.** Most C05 records were verified on 2026-10-26 from package metadata, READMEs and documentation; independent accuracy papers are cited from search summaries and marked "not re-read" in the deep dives (confidence 0.3 to 0.6). Accuracy conclusions below are therefore provisional.

## 2. Capability comparison

Notation: `tika-` apache-tika, `unstr-`, `docl-`, `spacy-`, `gli-`, `llmx-`, `pres-`, `sec-`, `marker-`, `rr-` (REBEL/ReLiK), `cet-` (coref/event/table), `hg-` apache-hugegraph, `n4-` neo4j. `unknown` = not publicly verified.

| Capability | Tika | Unstructured | Docling | spaCy | GLiNER | LLM extractors | Presidio | Secret scanners | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|---|
| CAP-32 format breadth | native, widest, ASF single edition (tika-01, tika-07) | native, broadest with typed elements (unstr-04, unstr-05) | native: PDF, Office, images; feature list (docl-04) | absent (text in) | absent (text in) | absent (text/chunks in) | n/a | n/a | Implemented: text, Office, ODF, legacy via LibreOffice, images, archives, email, SQLite; **PDF only when `enable_pdf=True`, via pypdf** (source read: `fileparse/engine.py`, `contracts.py:37`) |
| Layout / tables | absent, no layout model (tika-09, reasoned) | partial in OSS; better table extraction is API-only (unstr-04) | native table structure model (docl-04, docl-09) | absent | absent | weak on tables/images (llmx-04) | n/a | n/a | absent (source read; no layout model) |
| OCR | in-process Tesseract in 4.0 (tika-07) | OSS hi_res path (unstr-07) | native OCR engines (docl-07) | absent | absent | absent | image redaction needs OCR (pres §10, hypothesis) | n/a | optional Tesseract, off by default (`ocr=False`, source read) |
| Closed-label NER | absent | OSS lacks NER enrichment (unstr-04) | absent | native, F 85.5 (lg) / 89.8 (trf) on OntoNotes (spacy-04) | native zero-shot (gli-01) | native | native via spaCy or others (pres-03) | n/a | Partial: deterministic regex/TF NER, `Entity(start,end)` (BL-46 area; `nlp/pipeline.py`) |
| Zero-shot / ontology-labelled NER | absent | absent | absent | absent (fixed inventory, spacy §9) | native, CPU/ONNX variants (gli-03) | native | plugin via GLiNER PII checkpoints (gli-10) | n/a | absent |
| Relation extraction | absent | absent | absent | absent in core | partial, `gliner-relex`, no metrics (gli-05) | native, schema-guided modes (llmx-04, llmx-05) | n/a | n/a | absent for text (BL-27 covers JSON ontology proposals only) |
| Evidence-span capture (CAP-38) | absent: no source offsets (tika-09) | partial: bbox, no character offsets (unstr-05) | native: bbox and page in `DoclingDocument` (docl-05) | native token/char offsets (`Doc.ents`, spacy §8) | partial: token-level spans in decoder, README shows no offsets (gli-03, gli-04) | partial: chunk-level only (llmx-04) | native result spans (pres-03) | partial: file/line of match (sec-01) | Implemented: `RagChunk.start_char/end_char` and `page_number` locator (source read: `fileparse/contracts.py:102,115`); BL-41 manifests |
| CAP-33 PII detection | absent | absent | absent | partial, poor transfer (spacy-05) | plugin (PII checkpoints, gli-10) | n/a | native recognisers, checksums, context scoring, anonymiser (pres-03, pres §8) | n/a | Implemented/Partial: 5 regex types, **no checksum, findings keep `raw_value`**; `privacy/classification.py` has a Luhn-shape rule (BL-46; source read: `privacy/scanner.py:38,75`) |
| CAP-33 secrets | absent | absent | absent | absent | absent | absent | absent | native: gitleaks rules, TruffleHog verification, detect-secrets baseline (sec-01, sec-03, sec-04) | Partial: egress DLP, about 9 regex classes plus entropy, at egress not ingest (BL-45; sec §11) |
| CAP-50 air-gap | partial: needs jar baked in, `TIKA_CLIENT_ONLY`, VLM parsers off (tika-06, tika-07) | viable once system packages and models mirrored; model fetch unverified (unstr §10) | native with prefetch and artifacts path (docl-06) | native with mirrored wheels (spacy §10) | viable with mirrored weights (gli §10) | only with local LLM and embeddings; default compose enables OpenAI and Diffbot (llmx-01) | native with mirrored spaCy models (pres §10) | gitleaks, detect-secrets yes; TruffleHog only with verification off (sec §10) | design goal; no executed offline run (BL-45) |
| CAP-51 egress | VLM parsers call cloud models (tika-07) | API-only features (unstr-04) | remote services gated (docl-06) | n/a | n/a | policy needed (llmx-01) | n/a | verification sends live credentials to third-party APIs (sec §9) | Implemented, strengthened: default S0, kill switch, response DLP scan (BL-45 HEAD) |
| CAP-78 evaluation harness | none | none | authors' benchmark (docl-07) | vendor figures (spacy-04) | none | tiny independent samples (llmx-06, llmx-07) | none vendor-side (pres-04) | independent SecretBench study (sec-05) | absent |

Reference columns (engines), extraction rows only:

| Capability | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|
| CAP-32 text to graph | partial: HugeGraph-LLM extracts a KG into a HugeGraph schema (hg-28, C01 dive §1) | partial: LLM Graph Builder, experimental Labs project, Neo4j-only (llmx-01) | unknown (no row in its deep dive) | absent for text (BL-27 covers JSON only) |
| CAP-33 PII / secrets | unknown | unknown | unknown | Partial (BL-45, BL-46) |

## 3. Operational and licensing comparison

Code licences are permissive for all members except TruffleHog. **Model weights are the redistribution risk** and are tracked separately.

| Member | Code licence | Weights / data licences | Redistribution / OEM trigger | One-node CPU footprint | Maintenance (verified 2026-10) |
|---|---|---|---|---|---|
| Tika | Apache-2.0, ASF (tika-01) | none bundled | none beyond NOTICE aggregation and SBOM scan | JVM 17 server, forked children; OCR dominates CPU (tika §7) | active; 4.1.0 on 2026-09-29, 3.x maintenance, 2.x EOL (tika-02, tika-03); CVE-2025-54988 XXE in PDF parser, affected 1.13 to 3.2.1 (tika-10) |
| Unstructured | Apache-2.0 (unstr-01) | hi_res models: fetch unverified | open-core split is capability, not licence (unstr §10) | heavy system dependencies (unstr-06) | very active, releases every few days (unstr-02) |
| Docling | MIT (docl-01) | Heron layout Apache-2.0 (docl-03); TableFormer, OCR engines, VLMs **unverified**; Granite-Docling card unreadable (docl §1) | **Legal review: yes** for any bundled image | CPU 3.1 s/page per authors (docl-07) | very active, releases every 1 to 2 days (docl-02); outputs change weekly |
| spaCy | MIT (spacy-01) | pipelines vary: MIT for several, CC BY-SA 3.0 for `xx_sent_ud_sm`, English not confirmed (spacy-03) | legal review only for CC BY-SA / NC pipelines | lg 10,014 words/s CPU; trf 684 words/s CPU (spacy-04) | active, 3.8.16 |
| GLiNER | Apache-2.0 (gli-02) | Apache-2.0 for large-v2.1, multi_pii-v1, bi-base-v2.0, relex-large-v1.0 (gli-08, gli-10); older `gliner_multi` reported CC-BY-NC-4.0 (gli-09, secondary) | **Legal review: yes**, per-checkpoint allowlist required | 459M parameters for large-v2.1 (gli-08); CPU latency unverified | 0.2.29 on 2026-09-08 (gli-02) |
| LLM extractors | Graph Builder Apache-2.0, LlamaIndex MIT, LangChain MIT (llmx-01..03) | depends on chosen LLM | per-model terms | needs local LLM; throughput unverified | Graph Builder Labs-grade; `langchain-experimental` "being sunset" (llmx-03) |
| Presidio | MIT (pres-01) | NER backend model licences | none beyond backend check | library or two containers; spaCy model download needed | active, 2.2.365; moved to community-governed `data-privacy-stack` (pres-01) |
| gitleaks | MIT | none | none | single static binary | feature complete, security patches only (sec-01) |
| Betterleaks | MIT | none | none | n/a | v2 unreleased (sec-02) |
| TruffleHog | **AGPL-3.0 since v3.0** (sec-03) | none | **Legal review: yes**; do not ship | n/a | very active, v3.99.7 |
| detect-secrets | Apache-2.0 | none | none | Python plugin set | stale: last release 2024-05-06 (sec-04) |
| Tier C | Marker Apache-2.0 code, modified Open RAIL-M weights (marker-01); REBEL/ReLiK CC BY-NC-SA 4.0 with a PyPI metadata conflict (rr-01); fastcoref/coreferee MIT, Maverick CC BY-NC-SA (cet-01) | | weights block bundling | | Table Transformer repository archived (cet-02) |

## 4. Performance and accuracy evidence

No comparable end-to-end evidence exists. All entries are attributed; none were reproduced.

| Source | Figure | Workload / hardware | Class |
|---|---|---|---|
| Docling authors (docl-07) | 3.1 s/page x86 CPU, 1.27 s M3 Max, 0.49 s L4 GPU | 89 PDFs, 8 vCPU EPYC 7R13, 32 GB; Docling 2.5.2 with EasyOCR | authors' benchmark |
| Docling report on Unstructured (unstr-07) | 4.2 s/page CPU hi_res, no GPU gain | same set, Unstructured 0.16.5 | competitor-run, old version |
| Marker maintainers (docl-08) | Docling GPU 50.3 overall vs Marker balanced 76.0 on olmocr-bench | B200 host | competitor-run; conflicts in framing with docl-07 |
| GROBID paper (docl-09) | Docling table TEDS 0.858 vs 0.715 | PubTables | independent, not re-read |
| spaCy (spacy-04) | NER F 85.5 lg, 89.8 trf; 10,014 and 684 words/s CPU | OntoNotes dev; 10k Reddit comments | vendor |
| PIIBench (spacy-05, pres-05, gli-07) | spaCy lg span F1 0.087; Presidio 0.139; all systems low | 1,398-record subset | independent paper, not re-read |
| Self-reported leaderboard (gli-06, pres-07) | GLiNER micro-F1 0.32; Presidio 0.195 (last of five) | 1,000 records | self-reported, 0.3 |
| OOD robustness paper (pres-06) | Presidio smallest generalisation gap; SSN and IP recall 1.0 | not re-read | independent |
| SecretBench study (sec-05) | gitleaks recall 88%, precision 46%; TruffleHog recall 52% | 2023-era versions | independent |
| LLM extraction studies (llmx-06, llmx-07) | precision below recall; node conflation | 3 abstracts | independent, tiny sample |
| EOIP | none for parsing, NER, PII or secrets | n/a | not measured |

Derived arithmetic, not a measured result: at Docling's authors' 3.1 s/page on 8 vCPU, a 100,000-page corpus needs about 86 hours on one such node, which is why throughput must be measured on EOIP's target hardware (POC proposals in each deep dive §14, PROPOSED).

Reading across: independent PII benchmarks show low F1 for every system on enterprise-style text, and the numbers come from different datasets. Presidio's strength is structured identifiers (checksums, SSN/IP); free-text names and addresses are weak for all (pres §7).

## 5. Findings

1. **Span capture is where parsers differ most, and EOIP already has the anchor model.** Tika emits no offsets (tika-09), Unstructured gives bbox but no character offsets (unstr-05), Docling gives page and bbox (docl-05), spaCy and Presidio give character spans (spacy §8, pres-03). EOIP's `RagChunk` carries `start_char`, `end_char` and a page locator (source read). Two anchor kinds are needed (character range and page+bbox). Falsified if an adopted parser's output cannot be mapped to either anchor.
2. **The Tika, Unstructured and Docling dives describe EOIP's parsing gap in terms that no longer match HEAD.** `fileparse` now lists PDF through `pypdf`, off by default (`enable_pdf=False`), and `pypdf` is in no lock file found. Tika's dive observed no `.pdf` at ad9937b; Unstructured and Docling dives state there is no document parser beyond JSON profiling. Both claims conflict with the source and with each other. Status at HEAD: PDF text only, opt-in, no layout, no tables.
3. **Weights, not code, decide redistributability.** Marker's weights use a modified Open RAIL-M licence (marker-01), REBEL and ReLiK are CC BY-NC-SA (rr-01), the older GLiNER multi checkpoint is reported CC-BY-NC (gli-09), some spaCy pipelines are CC BY-SA (spacy-03) and Docling's non-layout weights are unverified (docl §1). A per-model licence allowlist in the SBOM gate is required before bundling anything.
4. **Offline is a configuration trap in four members.** tika-python downloads the server jar at runtime (tika-06), Tika 4.0 adds cloud VLM parsers (tika-07), Docling fetches weights from Hugging Face unless prefetched (docl-06), Graph Builder's default compose enables OpenAI and Diffbot (llmx-01), and TruffleHog verification calls live APIs (sec §9). Each is avoidable; none is tested in EOIP (no executed J16).
5. **Independent PII accuracy is poor for all tools, so no vendor claim can be relied on.** spaCy 0.087 and Presidio 0.139 span F1 (spacy-05, pres-05), both from an unread paper. EOIP should adopt Presidio for structured identifiers but must build its own labelled evaluation before claiming free-text PII coverage (CAP-78).
6. **EOIP's PII scanner has a defect independent of competitors.** Findings keep `raw_value` (source read: `privacy/scanner.py:38`), the scanner has no checksum validation, and it scans property values in the in-memory store rather than text with offsets (pres §11). Presidio or an in-house port of checksums fixes validation; dropping `raw_value` is a privacy fix regardless.
7. **Secret detection at ingest does not exist in EOIP.** DLP runs at egress (BL-45) and no ingest gate quarantines credentials (sec §11). gitleaks supplies a ready MIT rule corpus, but it is feature-frozen with 46% precision in a 2023 study (sec-01, sec-05); TruffleHog is AGPL and its verification conflicts with default S0 egress (sec-03).
8. **Open-core and stale maintenance bound the safe set.** Unstructured withholds VLMs, GPU use and better tables from OSS (unstr-04), detect-secrets has had no release since 2024-05 (sec-04), LangChain's graph transformer is being sunset (llmx-03). Docling (MIT, daily releases), spaCy, GLiNER and Presidio are the active permissive choices, and daily release cadence is itself a reproducibility burden (docl §9).
9. **LLM extraction is the least validated option.** Independent studies are three-abstract samples with precision below recall (llmx-06, llmx-07), and none tests local models. It must produce PROPOSED claims only (BL-39/40), never graph writes.
10. **Neither HugeGraph, Neo4j nor Neptune supplies extraction or PII detection as a supported engine feature.** HugeGraph-LLM extracts to HugeGraph only (hg-28) and Neo4j's builder is a Neo4j-only Labs project (llmx-01), so extraction must stay backend-neutral in EOIP's pipeline.

## 6. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-32 parsing (PDF layout, tables) | STR-docling (bbox, table model) | INV-unstructured (open-core withholding), INV-tika (no layout) | **INTEGRATE** Docling as optional adapter behind a parser-neutral interface; **INTEGRATE** Tika as optional breadth sidecar; **REUSE** Unstructured only as adapter | "PDF is opt-in, text-only, via a dependency not in the locks; no layout or tables." |
| CAP-38 span anchors | STR-docling provenance, STR-presidio spans | tika-09, unstr-05 | **BUILD** parser-neutral anchor contract (char range and page+bbox) mapped into BL-41 manifests | "No contract normalises parser output to evidence anchors." |
| CAP-32 NER | STR-spacy (CPU speed), STR-gliner (zero-shot) | spacy-05 poor transfer | **EXPERIMENT** GLiNER with a checkpoint licence allowlist; **INTEGRATE** spaCy as optional extra; keep in-house NER as dependency-free fallback | "NER is deterministic regex only; no zero-shot capability." |
| CAP-32 relations / LLM extraction | STR-llmx (schema-constrained, chunk provenance) | INV-llmx (no spans, no review state, Neo4j-only builder) | **EXPERIMENT** policy-gated local LLM extraction; **REJECT** Graph Builder and `LLMGraphTransformer` as dependencies; PROPOSED claims only | "No text-to-triple path." |
| CAP-33 PII | STR-presidio (recognisers, checksums, context) | pres-05, pres-07 (free-text weakness) | **REUSE** Presidio as optional extra; keep regex scanner as fallback; **BUILD** raw-value removal and Luhn/IBAN checksums; **BUILD** evaluation set | "Findings retain raw values; no checksum; not text-offset based." |
| CAP-33 secrets | STR-gitleaks (rule corpus), STR-detect-secrets (baseline workflow) | sec-05 precision, sec §9 | **BUILD** ingest-time quarantine gate; **REUSE** gitleaks rules; **EXPERIMENT** Betterleaks after stable v2; **REJECT** TruffleHog bundling | "Secrets are checked at egress only." |
| CAP-50 / CAP-51 | Docling prefetch, Tika offline settings | tika-06, tika-07, llmx-01 | **BUILD** egress-blocked CI job per adapter; **BUILD** SBOM check of model licences | "No executed offline test for any extraction adapter." |
| CAP-78 evaluation | Magellan-style public sets, SecretBench | independent evidence thin | **BUILD** harness (PII, NER, secrets, span accuracy); mark all runs PROPOSED until executed | "No accuracy measurement exists." |
| Tier C (Marker, REBEL/ReLiK, coref) | n/a | weight licences | **REFERENCE-ONLY**; Marker **EXPERIMENT** only if weight licence clears legal review | |

Backend neutrality: extraction outputs are SourceEvents and evidence records upstream of the `GraphStore` protocol, so none of this depends on HugeGraph, Neo4j or Neptune. Backend-supplied extraction (HugeGraph-LLM, Neo4j Graph Builder) is "available upstream / not integrated" and is deliberately not adopted.

## 7. Open questions

1. What is the English spaCy pipeline licence, and the licences of Docling TableFormer, OCR engines and Granite-Docling (spacy-03, docl §1)?
2. Does GLiNER emit character offsets in its public API, and what are its CPU latency and memory (gli-03, gli-04, gli §7)?
3. Should `pypdf` be added to the lock and `enable_pdf` default flipped, and how does that interact with the zip-bomb and nested-container budgets (tika §9)?
4. Are the independent PIIBench and SecretBench numbers reproducible (pres-05, sec-05; both "not re-read")?
5. Is `raw_value` retention in `privacy/scanner.py` intentional for DSAR, or a defect (pres §11)? 01a lists BL-46 as strengthened without noting it.
6. Evidence conflicts: Tika dive (PDF absent), Unstructured and Docling dives (no parser) versus HEAD source (PDF opt-in); Docling's own benchmark versus Marker's (docl-07 vs docl-08); Tika 4.1.0 dates differ between announcement and Maven upload (tika-02). Only the first changes a status.
7. Can Betterleaks reach a stable v2, and will gitleaks accept the maintainer move (sec-01, sec-02)?
