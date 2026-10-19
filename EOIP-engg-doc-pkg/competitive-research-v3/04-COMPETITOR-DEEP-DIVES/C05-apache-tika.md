# C05 — Apache Tika

| Field | Value |
|---|---|
| Registry ID | T-C05-apache-tika |
| Tier | B — document-parsing reuse candidate; adjacent enabling technology, not a competitor |
| Versions examined | Apache Tika 4.1.0 (announced 29 Sep 2026; Maven artefact directory dated 2026-09-26), 4.0.0 (21 Aug 2026), 3.3.3 support release (13 Oct 2026); `tika` Python client 3.3.2 (PyPI, 2026-08-01) |
| Verified on | 2026-10-18 |
| Worker | W14 |

## 1. Identity, current status, tier, and sources

Apache Tika is the Apache Software Foundation's content-detection and text/metadata-extraction toolkit (Java), licensed Apache-2.0 [CLAIM-apache-tika-01]. The current primary line is 4.x: 4.0.0 (first stable 4.x, 21 Aug 2026) and 4.1.0 (29 Sep 2026); 3.x remains a supported maintenance line (3.3.3, 13 Oct 2026, "a support release of the 3.x line, not the primary release") [CLAIM-apache-tika-02]. 1.x reached end of life on 30 Sep 2022 and 2.x is end of life [CLAIM-apache-tika-03]. 4.x requires Java 17; 3.x requires Java 11 [CLAIM-apache-tika-04]. The Maven `tika-core` metadata lists 4.1.0 as `latest`/`release` [CLAIM-apache-tika-05].

Name trap: the PyPI package `tika` (3.3.2) is a third-party Python client (tika-python, Chris Mattmann et al.), not an ASF release; it launches or calls a Tika server [CLAIM-apache-tika-06]. Status: **active**. Tier B because it is the most mature permissive multi-format parser and EOIP's own parser has no PDF path (see §11).

Sources: tika.apache.org (news, security page), Maven Central metadata, tika-python README, PyPI.

## 2. Primary problem, target workloads, concrete example workflows

Problem: turn arbitrary binary files (PDF, Office, OpenDocument, email, archives, images, ~1,000+ MIME types — vendor-stated breadth, not counted here) into text plus metadata through one detection + parser-dispatch API. Workloads: enterprise search indexing (Solr/Elasticsearch/OpenSearch pipelines historically), e-discovery, DLP pre-processing, RAG ingestion.

EOIP workflows:
- **SharePoint/file-share crawl → SourceEvent → parse.** A connector emits a SourceEvent with a blob reference; a parse worker sends the blob to a local `tika-server` (4.x, out-of-process), receives Markdown/XHTML + metadata, and stores a `ParsedDocument` with per-page sections.
- **Contract repository (J15).** Legacy `.doc`/`.pdf` contracts parsed to page-segmented text, then passed to NER/PII detection with page locators.

## 3. Feature inventory

| Area | Feature | Status | Evidence |
|---|---|---|---|
| Core | MIME detection + parser dispatch | present | CLAIM-apache-tika-01 |
| Core | Markdown default output (4.x) | present | CLAIM-apache-tika-07 |
| Isolation | Crash-isolated forked parsing via tika-pipes (server, app async/fork, gRPC) | present (4.x) | CLAIM-apache-tika-07 |
| API | tika-server REST; tika-grpc | present | CLAIM-apache-tika-07 |
| CLI | tika-app | present | CLAIM-apache-tika-07 |
| OCR | In-process Tesseract (4.0); engines chosen by name (4.1) | present | CLAIM-apache-tika-07, -08 |
| AI | Vision-language-model parsers (Claude, Gemini, OpenAI) | optional (cloud — must be disabled in EOIP) | CLAIM-apache-tika-07 |
| Ops | Named presets, Micrometer metrics, env interpolation in `tika-config.json` (4.1) | present | CLAIM-apache-tika-08 |
| Layout | Reading-order/table-structure ML (Docling-class) | absent (rule-based PDF text extraction; tables as text) | Reasoned inference — CLAIM-apache-tika-09 |
| Provenance | Character offsets back to source bytes | absent; page boundaries only for paged formats | CLAIM-apache-tika-09 |
| Python | tika-python client | third-party; downloads server jar from Apache by default | CLAIM-apache-tika-06 |
| Enterprise edition | — | none (single ASF edition) | CLAIM-apache-tika-01 |

## 4. Text-based architecture diagram

```
 EOIP parse worker (Python)                 Tika sidecar (JVM 17, local container)
 ┌───────────────────────────┐   HTTP/gRPC  ┌───────────────────────────────────────┐
 │ SourceEvent(blob_ref,acl) │ ───────────► │ tika-server  (control plane: presets, │
 │ size/time budgets         │              │   config.json, Micrometer metrics)    │
 │ ParsedDocument builder    │ ◄─────────── │ tika-pipes dispatcher                 │
 └───────────────────────────┘ Markdown/    │   └─ forked parser JVMs (data plane)  │
              │                 XHTML+meta  │       Detector → Parser (PDFBox, POI, │
              ▼                             │       mail, archive) → SAX → Markdown │
   PII/secret scan → NER/RE → claims        │       optional Tesseract OCR          │
                                            │  [VLM parsers: DISABLED by policy]    │
                                            └───────────────────────────────────────┘
 State: stateless per request; no Tika-side persistence. Network egress: none if VLM parsers off.
```

## 5. Under-the-hood reconstruction

- **Data model.** A detected MIME type, a `Metadata` multimap (Dublin Core/XMP-like keys) and a stream of SAX XHTML events; 4.x serialises to Markdown by default [CLAIM-apache-tika-07]. Embedded documents (attachments, archive members) are recursed as child documents.
- **Pipeline.** `Detector` (magic bytes + filename + container inspection) → `CompositeParser` dispatch → format parser → `ContentHandler`. 4.x moves the parser into forked processes (tika-pipes) so a hostile or pathological file kills only a child [CLAIM-apache-tika-07].
- **Storage/indexing, reasoning, transactions, partitioning, versioning.** N/A — stateless transformer.
- **Caching.** None internal (hypothesis: callers cache by content hash; EOIP already hashes content in `fileparse`).
- **Security.** Parser attack surface is the main risk: CVE-2025-54988 "XXE when parsing XFA via the PDFParser" affected 1.13–3.2.1 [CLAIM-apache-tika-10]. Forked isolation in 4.x limits blast radius but not XXE-style data exfiltration; the sidecar should run with no network and read-only filesystem.
- **Evidence spans (hypothesis, consistent with documented output).** Offsets are only meaningful relative to Tika's emitted text, not to source bytes; EOIP must treat Tika output as the canonical "extracted text" and anchor spans to it (as `fileparse/contracts.py` already does: "offsets refer to extracted section text").

## 6. Functional and non-functional requirements inferred

FR: parse PDF/legacy Office/email/archives into text + metadata; recurse embedded files; OCR images. NFR: crash isolation per document; bounded time/memory per parse; no runtime network; deterministic output per Tika version (parser version must be recorded in provenance — EOIP `ParsedDocument.parser_version` already exists).

## 7. Performance and resource model

No independent throughput benchmark of Tika 4.x was found; **NOT PUBLICLY VERIFIED**. Resource model (reasoned inference): a JVM 17 server process plus forked child JVMs; memory scales with largest document and concurrency; OCR dominates CPU when enabled. Failure modes: pathological PDFs (timeouts), zip bombs (must keep EOIP's nested-container budgets), OCR latency. POC must measure p50/p95 seconds/page on a CPU-only node (§14).

## 8. Strengths and use-case-specific advantages

1. Breadth and maturity across legacy formats with one permissive dependency [CLAIM-apache-tika-01] — **match by integrating** as an optional sidecar.
2. Crash-isolated parsing in 4.x [CLAIM-apache-tika-07] — **exceed**: EOIP adds per-tenant quotas and DLQ on parse failure (BL-24).
3. ASF governance, no community/enterprise split [CLAIM-apache-tika-01].

## 9. Limitations with root causes

- **Algorithmic dead-end (intentional trade-off):** rule-based PDF text extraction without layout models — weaker reading order and table structure than Docling/Marker [CLAIM-apache-tika-09, hypothesis supported by Docling's comparative framing].
- **Operational overhead:** JVM 17 sidecar in a Python stack [CLAIM-apache-tika-04].
- **Developer friction / air-gap trap (verified):** tika-python by default checks the Tika version and pulls the latest server jar from Apache at runtime; offline use requires `TIKA_SERVER_JAR=file:///…` or `TIKA_CLIENT_ONLY` [CLAIM-apache-tika-06].
- **Egress trap (verified feature):** 4.0 added cloud VLM parsers [CLAIM-apache-tika-07] — must be excluded from the EOIP image.
- **Security defect (verified):** CVE-2025-54988 [CLAIM-apache-tika-10].

## 10. Deployment, licensing, redistribution, operational viability

Apache-2.0, ASF — redistribution-safe with NOTICE handling; no legal-review trigger beyond dependency NOTICE aggregation (bundled parser libraries are ASF-vetted; still run an SBOM licence scan). Deployment: container sidecar (`tika-server`), CPU-only, air-gap viable if (a) the jar is baked into the image, (b) VLM parsers are not configured, (c) the Python client runs in `TIKA_CLIENT_ONLY` mode.

## 11. Competitive delta against the EOIP verified baseline

- EOIP `fileparse` supports text, HTML/XML, RTF, DOCX/XLSX/XLS/PPTX, legacy Office via LibreOffice, images via Tesseract, archives, email and SQLite — **but no `.pdf`** in `SUPPORTED_EXTENSIONS` (`packages/eoip/fileparse/engine.py:31-37`, observed 2026-10-18). PDF is the dominant enterprise document format, so this is a material ingest gap under CAP-32 (relates to BL-23/BL-26 ingest pipeline; no BL-ID covers file parsing explicitly).
- EOIP already has what Tika lacks: chunk-level `start_char/end_char` provenance (`fileparse/contracts.py` `RagChunk`), nested-container budgets, content hashing.
- Delta: Tika fills breadth (PDF, legacy, odd formats); Docling (see C05-docling) fills layout-quality PDF. Neither replaces EOIP's provenance contract.

## 12. Strength-adoption cards and Con-to-Pro inversion cards

**STR-apache-tika-01** | Apache Tika | breadth of format coverage with crash-isolated parsing | CLAIM-apache-tika-01, -07 | customers ingest file shares with decades of legacy formats | integrate | optional `tika` parse backend behind `fileparse` dispatch: formats EOIP lacks (PDF fallback, ODF, odd MIME) route to a local tika-server; output normalised into `ParsedDocument` with `parser_version="tika-4.1.0"` | 500-file mixed corpus parses with 0 worker crashes, all failures go to DLQ with reason, no outbound network observed.

**INV-apache-tika-01 — "Text without anchors."**
- Target: Tika 4.1.0, PDF/Office parsing for evidence-backed KG extraction.
- Limitation: output text carries page/metadata boundaries but no stable offsets back to source bytes or layout boxes [CLAIM-apache-tika-09].
- Root cause: *storage/data model* — SAX text stream designed for search indexing (proven by output model; hypothesis on intent).
- Alternative design: canonical extracted-text artefact, content-addressed and versioned, with every downstream span anchored to (document hash, parser version, section index, char range). Worse when: parser upgrades change text, invalidating spans — needs re-anchoring.
- Options: (1) quick — call Tika, store its text as the canonical artefact; (2) pragmatic — section-per-page normalisation plus span anchors in EOIP `Section.locator` (`{"page": n}`); (3) long-term — multi-parser "evidence text" layer where Docling (bbox+charspan) is preferred for PDFs and Tika for breadth, with a span-migration routine across parser versions.
- Selected: (2) now, (3) when Docling lands. Sketch: `Anchor = {doc_sha256, parser:"tika@4.1.0", section:int, start:int, end:int, page:int?}`; on reparse, `migrate(anchor, old_text, new_text)` via diff alignment; unresolved anchors flagged, claims demoted to UNCORROBORATED.
- Benchmark: 200 PDFs; extract claims, upgrade parser, re-anchor; success ≥ 98 % anchors resolved exactly, 0 silent mismatches; cost baseline = CPU minutes per 1,000 pages.
- Failure cases: OCR non-determinism; ACL must travel with the artefact (BL-17); tenant-scoped storage of extracted text.
- Defensibility: the value is EOIP's evidence chain (BL-41) — copying Tika gives text, not auditable claims.
- Decision: **ADOPT** (option 2), **EXPERIMENT** (option 3).

## 13. Per-capability decisions

| Capability | Decision | Note |
|---|---|---|
| CAP-32 multi-format parsing breadth | INTEGRATE (optional sidecar) | Apache-2.0, CPU-only |
| CAP-32 high-fidelity PDF layout/tables | REJECT Tika for this; see Docling | |
| CAP-38 evidence spans | BUILD (EOIP anchor layer) | Tika provides no source offsets |
| CAP-50 air-gap | BUILD guardrail | bake jar; `TIKA_CLIENT_ONLY`; VLM parsers off |
| CAP-79 supply chain | BUILD | SBOM + CVE watch (CVE-2025-54988 class) |

## 14. Concrete tests, proof-of-concept, and acceptance conditions (PROPOSED)

- T1 air-gap: run tika-server 4.1.0 container with `--network none` equivalent; parse corpus; assert zero egress attempts.
- T2 robustness: corpus with zip bombs, malformed PDFs, XFA forms; assert no worker crash, DLQ entries, XXE canary not resolved.
- T3 quality: PDF text vs Docling on 100 PDFs (reading order, table cells) — decides routing policy.
- T4 throughput: seconds/page p50/p95 on 8-core CPU, OCR on/off.

## 15. Risks, trade-offs, and open research questions

Risks: JVM footprint on one-node installs; parser CVEs; accidental enabling of cloud VLM parsers. Open: Tika 4.x Markdown fidelity for tables vs Docling; whether tika-pipes per-request fork overhead is acceptable for many small files; planned change of default unpack format in 4.2.0 [CLAIM-apache-tika-07].

## Appendix A. Research-dimension coverage

| Dimension | Covered in | Summary or N/A reason |
|---|---|---|
| D1 Identity and maturity | §1 | ASF, 4.1.0, active, Apache-2.0 |
| D2 Problem and workloads | §2 | multi-format text extraction |
| D3 Architecture | §4 | server + forked pipes |
| D4 Storage and indexing | §5 | N/A — stateless |
| D5 Schema and semantics | §5 | metadata multimap only |
| D6 Query pipeline | — | N/A — no query engine |
| D7 Reasoning | — | N/A |
| D8 Transactions and scale | §7 | process-level concurrency only |
| D9 Ingestion and federation | §2, §11 | parse stage of ingest |
| D10 Identity and evidence | §9, §12 | no source offsets — INV-01 |
| D11 Time and evolution | §12 | parser-version drift |
| D12 Algorithms and ML | §3 | OCR only |
| D13 Retrieval and agents | — | N/A (upstream of retrieval) |
| D14 NL querying | — | N/A |
| D15 Governance | — | N/A |
| D16 Human experience | — | N/A (no UI) |
| D17 Developer experience | §9 | Python client air-gap trap |
| D18 Trust and security | §5, §9 | CVE-2025-54988, isolation |
| D19 Multi-tenancy | §12 | EOIP must scope artefacts per tenant |
| D20 Economics | §7 | not publicly benchmarked |
| D21 Commercial/licensing | §10 | Apache-2.0, no split |
| D22 Interop and lock-in | §10 | low lock-in |
| D23 IP and prior art | — | none flagged |
| D24 Research quality | §7 | no independent benchmark found |

## Appendix B. Capability mapping

| CAP-ID | This technology | Evidence | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-32 | native (parsing) | CLAIM-apache-tika-01, -07 | fileparse: no PDF (observed); BL-23 Implemented | INTEGRATE | P1 |
| CAP-38 | absent (source offsets) | CLAIM-apache-tika-09 | BL-41 Implemented | BUILD | P1 |
| CAP-50 | partial (needs config) | CLAIM-apache-tika-06, -07 | Partial | BUILD guardrail | P1 |
| CAP-79 | n/a | CLAIM-apache-tika-10 | Unknown | BUILD | P2 |

## Appendix C. Evidence records

| CLAIM-ID | product / version / date | exact claim | classification | source | pub / access | confidence | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-apache-tika-01 | Apache Tika | ASF project, Apache-2.0, single edition | Officially documented | Apache Tika home https://tika.apache.org/ ; PyPI/Maven licence fields | — / 2026-10-18 | 0.9 | none |
| CLAIM-apache-tika-02 | 4.1.0 / 4.0.0 / 3.3.3 | 4.1.0 released 29 Sep 2026 (current); 4.0.0 21 Aug 2026; 3.3.3 13 Oct 2026 is "a support release of the 3.x line" | Officially documented | Tika news https://tika.apache.org/ | 2026-10-13 / 2026-10-18 | 0.85 | Maven dirs dated 2026-09-26 (4.1.0) and 2026-08-18 (4.0.0) — artefact upload precedes announcement |
| CLAIM-apache-tika-03 | 1.x, 2.x | 1.x EOL 30 Sep 2022; 2.x and Java 8 support EOL | Officially documented | https://tika.apache.org/ | — / 2026-10-18 | 0.85 | none |
| CLAIM-apache-tika-04 | 4.x / 3.x | 4.0.x "requires Java 17"; 3.x "requires Java 11" | Officially documented | https://tika.apache.org/ | — / 2026-10-18 | 0.85 | none |
| CLAIM-apache-tika-05 | tika-core | Maven metadata latest=release=4.1.0, lastUpdated 20261013 | Officially documented | https://repo1.maven.org/maven2/org/apache/tika/tika-core/maven-metadata.xml | 2026-10-13 / 2026-10-18 | 0.9 | none |
| CLAIM-apache-tika-06 | tika-python 3.3.2 | "Without this set, the default is to check the tika version and pull latest every time from Apache"; offline requires TIKA_SERVER_JAR file URL; TIKA_CLIENT_ONLY mode | Officially documented (client README) | tika-python README https://github.com/chrismattmann/tika-python | — / 2026-10-18 | 0.85 | none |
| CLAIM-apache-tika-07 | 4.0.0 | default output Markdown; "moves parsing into crash-isolated forked processes"; server/app/grpc parse out-of-process via tika-pipes; "adds vision-language-model parsers (Claude, Gemini, OpenAI) and in-process Tesseract OCR"; plan to change default unpack format in 4.2.0 | Officially documented | https://tika.apache.org/ (4.0.0 news) | 2026-08-21 / 2026-10-18 | 0.85 | none |
| CLAIM-apache-tika-08 | 4.1.0 | OCR/enrichment engines chosen by name; server named presets, Micrometer metrics, env interpolation in tika-config.json | Officially documented | https://tika.apache.org/ | 2026-09-29 / 2026-10-18 | 0.85 | none |
| CLAIM-apache-tika-09 | 4.x | No layout-model reading order/table structure and no source-byte offsets in output | Reasoned inference | from documented output model (CLAIM-07) and absence in release notes | — / 2026-10-18 | 0.5 — absence not exhaustively checked | none found |
| CLAIM-apache-tika-10 | ≤3.2.1 | CVE-2025-54988 "XXE when parsing XFA via the PDFParser", affected 1.13–3.2.1 | Officially documented | Tika security page https://tika.apache.org/security.html | 2025 / 2026-10-18 | 0.85 | fixed version not stated on page |

## Appendix D. Assumptions

- A1: "Apache Tika" in the registry means the ASF Java project; the Python client is recorded as a member, not the subject.
- A2: Announcement dates on tika.apache.org are taken as release dates; Maven upload dates recorded as contradictory evidence.
- A3: The `fileparse` PDF gap was observed by direct file read on 2026-10-18 (not in `01-SYSTEM-BASELINE.md`); coordinator may wish to add a BL-ID for file parsing.
