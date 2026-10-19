# Connectors and Source Acquisition

Connectors translate source-specific protocols/records into contracts consumed by ingestion services. A connector module, catalog entry or synthetic fixture does not establish live vendor qualification.

## Follow a Source

Inspect `registry.py` for source registration, `config.py` for configured connector construction, `errors.py` for classified failures and the source-specific connector. Then follow the matching service in `packages/eoip/ingestion/` and dispatch in `apps/worker/main.py`. Registration, discovery, extraction, normalization and execution are different responsibilities.

JSON demo connectors and REST/webhook connectors have different contracts. A batch ingestion demo does not prove authenticated incremental polling. Use [connector qualification](../../../docs/connectors/qualification.md) and its vendor-specific companion docs for the intended capability matrix.

## Adding or Changing a Connector

1. Define supported source/version, credential method, scopes, allowed hosts, pagination and rate limits.
2. Preserve source IDs, cursor/version semantics, deletion handling and raw-event provenance.
3. Validate schema/normalization and enforce tenant/source boundaries before graph effects.
4. Classify timeout, authentication, rate-limit and remote errors without leaking tokens or payload secrets.
5. Wire the actual registry/API/worker path; do not stop at a connector class.
6. Test retries, duplicates, partial pages, webhook verification, interruption and reconciliation.
7. Qualify an authorized live sandbox separately and document unavailable operations honestly.

Do not place credentials in job/source payloads. Verify secret-reference resolution and deployment injection rather than assuming a reference field implements a vault. Treat crawled pages and tool descriptions as untrusted content. Use [operations](../../../docs/operations-runbook.md) before replaying DLQ or resetting cursors.
