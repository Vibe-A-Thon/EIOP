# EIOP

Enterprise Ontology & Intelligence Platform. The implementation lives at the
repository root; the requirements and architecture handoff are in
`EOIP-engg-doc-pkg/`.

Start the local Docker deployment from this directory: From the repository root, with Docker Desktop running in Linux-container mode:

```powershell
.\scripts\docker.ps1 up
.\scripts\docker.ps1 test
```
The startup script finds Docker Desktop even when its CLI is missing from PATH,
generates local credentials, builds the services, and waits for readiness.
No host Python or Node installation is required.


Open [the explorer](http://localhost:8080/app) or
[administration](http://localhost:8080/admin). Enter `EOIP_API_TOKEN` from the
generated, Git-ignored `deploy/.env`. API documentation is at
[localhost:8000/docs](http://localhost:8000/docs).

The explorer uses an on-demand Cytoscape.js canvas with Search, Graph, Impact,
Evidence, and Architecture lenses, typed legends, bounded expansion,
relationship/trust filters, highlighted paths, exported local context, and
responsive inspection panels. Administration includes live source/job,
validation/quality, ontology, model/backup health, audit, and dead-letter
views; operational values are always read from the API. The API supports
QueryPlan execution (`POST /api/v1/query`), provenance lineage
(`POST /api/v1/lineage`), GraphRAG retrieval (`POST /api/v1/rag`), and
ingestion/validation run history (`GET /api/v1/ingestion/runs`,
`GET /api/v1/validation/runs`).

The demo worker loads Jira fixtures, a real Git repository, Python/TypeScript
symbols, documentation, merge-request metadata, and pipeline metadata.

## On-prem source connectors

The worker supports incremental Confluence Data Center and ServiceNow Table API
jobs. Before starting it, configure each source in the worker environment using
either a bearer token or a username/password pair:

| Source | URL | Bearer token | Basic-auth pair |
|---|---|---|---|
| Confluence | `EOIP_CONFLUENCE_URL` | `EOIP_CONFLUENCE_TOKEN` | `EOIP_CONFLUENCE_USERNAME`, `EOIP_CONFLUENCE_PASSWORD` |
| ServiceNow | `EOIP_SERVICENOW_URL` | `EOIP_SERVICENOW_TOKEN` | `EOIP_SERVICENOW_USERNAME`, `EOIP_SERVICENOW_PASSWORD` |

Set credentials only through the worker's secret/environment configuration.
The API request and durable job payload contain sync options only, never source
credentials. Submit an authenticated job to
`POST /api/v1/admin/ingestion/confluence` or
`POST /api/v1/admin/ingestion/servicenow` with an optional ISO-8601 `checkpoint`,
optional ISO-8601 `watermark`, and `dry_run` boolean. If no checkpoint is
supplied, the worker resumes from `state/connectors/{source}.json`. It advances
that checkpoint only after a fully successful, non-dry-run ingestion; partial
mapping results are captured to raw storage and DLQ, then replay from the old
checkpoint. Confluence pages/spaces and ServiceNow knowledge articles are
persisted with source-event evidence and containment lineage; page/article
text is stored in the document description. Confluence attachment binaries are
not downloaded by this connector.

## RDF/OWL interoperability

The authenticated `GET /api/v1/ontology/export` endpoint returns a JSON-LD 1.1
document containing the EOIP ontology vocabulary and graph data. It exports
vertices as OWL individuals and labels as ontology classes, while edges are
represented both as direct relation triples and as reified assertions to retain
edge properties. The optional `limit` query parameter bounds vertices and edges
independently (default 5000, maximum 10000); inspect `export.partial`,
`export.truncated_vertices`, `export.truncated_edges`, and `export.mapping_losses`
before treating an export as complete. This is an export adapter: HugeGraph does
not provide native RDF or SPARQL support.

See [the Docker runbook](docs/docker-local.md) for Full instructions and current scope, services, tests,
backup/restore, the VS Code extension, optional profiles, and implementation limits.
