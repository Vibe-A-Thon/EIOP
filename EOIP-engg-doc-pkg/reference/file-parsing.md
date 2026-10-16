# Actual file parsing and ingestion

The `eoip.fileparse` package decodes actual bytes rather than treating binary
files as UTF-8 or accepting pre-converted JSON as a substitute. It operates
locally; no document, image, email, or archive content is sent to a cloud service.

## Installation and format support

For host development, install the optional dependencies into the existing environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -e '.[fileparse]'
```

The application Dockerfile installs the pinned native dependencies from
`requirements-fileparse.lock` alongside the core runtime lock. These pins were
resolved and tested on Windows/Python 3.11; Linux image execution still needs
deployment verification. Existing images must be rebuilt to include them.

| Formats | Extraction |
| --- | --- |
| TXT, CSV, JSON | Strict text decoding; CSV headers/rows; structured JSON plus text |
| HTML, HTM, XHTML | Visible text and link metadata; scripts/styles excluded, links never fetched |
| XML | Structured tree and text using entity-safe XML parsing |
| RTF | Text using `striprtf` |
| DOCX | Paragraphs, tables, headers, footers, author metadata |
| XLSX | All worksheets and typed cells; formulas preserved as text, never executed |
| XLS | BIFF worksheet values using `xlrd`; formula results are cached values |
| PPTX | Slide text, tables, nested shapes, speaker notes |
| DB, SQLITE, SQLITE3 | SQLite 3 only, read-only snapshot; typed base64 BLOB values |
| JPG/JPEG, PNG, GIF, TIF/TIFF, BMP, WEBP | Decoded image dimensions/frame metadata; optional local OCR |
| EML | MIME headers/bodies and recursively parsed attachments |
| MSG | Outlook subject/body/metadata and binary attachments using `extract-msg` |
| ZIP, TAR, GZ, TGZ, 7Z | Bounded in-memory recursive decoding, without filesystem extraction |
| RAR | Stored members work natively; compressed members need a local backend |
| DOC, PPT, WPS, WPD | Local LibreOffice conversion to DOCX/PPTX, then native parsing |

Legacy conversion requires an installed `soffice` executable or an explicit
`libreoffice_path`. WPS refers to word-processing documents, not an arbitrary
Kingsoft format; WPS/WPD compatibility depends on LibreOffice's installed
import filters. Unsupported/encrypted/corrupt files fail explicitly.
MSG binary attachments are supported; embedded Outlook items must first be
exported as separate MSG files.

OCR requires an installed `tesseract` executable and local language data. Set
`ocr=true` and optionally `tesseract_path`/`ocr_language`. Without OCR, images
produce metadata and a warning, **not invented visual text or RAG chunks**.
No embedded Office images are OCRed automatically.

Compressed RAR decoding may require `unrar`, `unar`, or a supported `7z` backend
available to `rarfile`. External tools are not installed automatically. They run
locally with a timeout, without shell command interpolation. Treat untrusted
legacy files as potentially hostile: use a suitably isolated, least-privilege
runtime with network access restricted by the operator.

For SQLite, create a consistent backup/export of a live database before upload.
Local paths with a nonempty WAL sidecar are rejected rather than silently losing
uncheckpointed rows. Uploaded bytes cannot reveal absent WAL sidecars. Other
database engines and virtual tables require their own trusted export.

## CLI and Python

```powershell
.\.venv\Scripts\python.exe -m eoip.fileparse .\input.docx --output .\output-bundle --vectors
.\.venv\Scripts\python.exe -m eoip.fileparse .\image.png --output .\image-bundle --ocr --tesseract-path 'C:\Tools\Tesseract\tesseract.exe'
.\.venv\Scripts\python.exe -m eoip.fileparse --formats
```

The output must be a new directory; an existing bundle is never overwritten.
Exit codes are `0` for a successful conversion, `2` for a persisted partial/failed
container result, and `1` for a rejected input, missing tool, or write failure.
Use `--encoding` for explicitly non-UTF-8 text; UTF-8 and UTF-16 BOMs are recognized.

```python
from eoip.fileparse import FileParser, ParseOptions, export_bundle

parser = FileParser(ParseOptions(chunk_chars=1200, chunk_overlap=150))
result = parser.parse_path(r"C:\Data\input.xlsx", source_id="documents-team")
manifest = export_bundle(result, r"C:\Data\new-bundle", vectors=True)
```

## Artifact contract

Each bundle is staged and renamed into place only after all files are written:

- `parsed.json`: versioned result, parsed documents, chunks, warnings/errors and status.
- `documents/<identity-hash>.json`: one structured document, including tables/data.
- `chunks.jsonl`: chunk text, document/source identity, hash, exact section offsets,
  locators and citation URLs.
- `graph.json`: `Document`/`DocumentSection` entities and `CONTAINS` relationships.
- `keyword.jsonl`: token data keyed by chunk identity with citations.
- `vectors.jsonl` (optional): normalized 256-dimensional local lexical hashing
  vectors, model identifier and citations.
- `manifest.json`: format/parser version, counts/status/errors and file SHA-256
  digests (the manifest itself is not included in its checksum map).

Vectors reuse the application's `HashingEmbedder`. They are **not trained semantic
embeddings**. These artifacts are inputs for local RAG, graph, and search consumers;
they do not automatically provision a remote vector database.

Document identities include source instance, URI and content hash. Chunk
identities also include parser version, section, offsets and content. Changed
files produce new immutable identities; this connector does not delete previous
versions or declare one version current. Nested URIs include archive/attachment
paths, and citations address exact offsets in extracted section text, not binary
byte offsets or physical page coordinates.

## Authenticated raw upload API

Send actual file bytes as `application/octet-stream`, **not multipart or JSON**:

```powershell
curl.exe -H "Authorization: Bearer $env:EOIP_API_TOKEN" `
  -H "Content-Type: application/octet-stream" `
  --data-binary '@input.docx' `
  'http://localhost:8000/api/v1/admin/ingestion/files/parse?filename=input.docx'
```

- `GET /api/v1/connectors/files/formats`: supported adapters and default limits.
- `POST /api/v1/admin/ingestion/files/parse?filename=...&source_id=...&ocr=false`:
  parse/persist artifacts without graph mutation.
- `POST /api/v1/admin/ingestion/files?filename=...&source_id=...&ocr=false&dry_run=false`:
  capture raw bytes, persist artifacts, and write through validated graph ingestion.
- `GET /api/v1/admin/ingestion/files/bundles/{bundle_id}/{artifact}`:
  authenticated download of an allowlisted top-level artifact.

The host's existing authentication/audit boundary applies. HTTP `415` means
wrong upload content type, `413` an exceeded limit, `422` invalid/unsupported
input, and `503` a missing dependency or local executable. Recoverable container
failures return an explicit result status/error list; inspect it even on HTTP 200.
Dry-run ingestion parses but writes no raw capture, bundle, DLQ, or graph mutation.

Ingestion captures immutable base64 `documents/binary_file` SourceEvent V2
envelopes under `<data>/raw/documents` before parsing. Rejected parses go to the
existing DLQ. Graph entities have source-event `EVIDENCED_BY` and `INGESTED_IN`
edges. Graph failures are reported; the already-persisted bundle remains, and
graph writes do not claim transactional rollback. The normal deployed GraphStore
is used; `MemoryGraphStore` is only the test harness.

## Registered sources and replay

Register a `documents` source through the existing source registry API:

```json
{
  "source_id": "team-files",
  "source_type": "documents",
  "name": "Team files",
  "allowed_scopes": ["C:\\Data\\team"],
  "capabilities": {"polling": true, "reconciliation": false},
  "config": {
    "scope": {
      "roots": ["C:\\Data\\team"],
      "excluded_paths": ["C:\\Data\\team\\private"],
      "max_files": 10000,
      "max_file_bytes": 20000000
    },
    "parse_options": {"ocr": false}
  }
}
```

Roots must stay within `allowed_scopes`; `excluded_scopes` are merged with explicit
excluded paths. Container workers need mounted paths accessible inside their
container, not Windows host paths. Scope suffixes default to all supported formats.

The worker dispatches `BASELINE`, `POLL`, and `REPLAY`. Polling currently rescans
the scope (not an incremental filesystem watcher); immutable source capture and
canonical graph upserts deduplicate unchanged content. Baseline/poll checkpoints
advance only on fully successful non-dry runs. Individual parse failures are
captured/reported while later files continue. Replay requires explicit captured
SHA-256 `event_ids`, verifies source identity, and does not advance acquisition
checkpoints. Deletion reconciliation, permission-event acquisition and webhooks
are not advertised or implemented.

## Limits and failures

Default parser limits: 20 MB input, 100 MB cumulative expanded bytes, 500 nested
inputs, depth 3, 10,000 rows/sections, 5,000,000 extracted text characters,
25,000,000 image pixels, and a 60-second external-tool timeout. Office uncompressed
data contributes to expansion limits. Rows, sections and text budgets are shared
across nested inputs; the root itself counts toward the nested-input budget.
CSV also respects Python's local CSV field-size limit. Configure stricter limits
through `ParseOptions`/registered `parse_options`; the HTTP API uses defaults.

Absolute/traversal paths, duplicate members, links/devices and encrypted archives
are rejected. Resource and unsafe-path errors fail the whole parse; unsupported
or corrupt individual members can produce `PARTIAL` (usable content plus explicit
errors) or `FAILED` (no usable content). Earlier descendants of a failed nested
member are removed, so exports never retain orphan containment references.

Tests generate original real Office, BIFF XLS, Outlook MSG, stored RAR, 7z, image,
SQLite, MIME and text fixtures. LibreOffice/OCR success and process failures are
tested with mocked local executables; live external conversion, OCR, compressed
RAR and Linux image/HugeGraph execution need environment-specific verification.
