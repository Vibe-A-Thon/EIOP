# EOIP — Enterprise Ontology & Intelligence Platform

EOIP is a local-first enterprise knowledge graph platform that ingests from 24 source connectors (Jira, GitLab, GitHub, Confluence, ServiceNow, and more), links cross-domain facts into a typed property graph, and answers questions about your codebase, work items, incidents, people, and deployments through a GraphRAG retrieval system and 20 bounded agents.

**Key capabilities:**
- 24 source connectors with checkpoint-based incremental sync
- Multi-backend graph store: Apache HugeGraph (default), Amazon Neptune, or in-memory — via `config/graph-store.yaml`
- 14 graph domains, 50+ vertex types, 30+ edge types
- 6 query languages: EQL, NLQ, EOQL, OSQL, Semantic QL, raw Gremlin (admin)
- 30+ graph algorithms: centrality, community, paths, similarity, blast radius, cycle detection
- Federated query planner with cost-aware routing, filter/projection pushdown, and per-row provenance
- GraphRAG with 7 retrieval strategies, stable evidence citations, no mandatory vector DB
- 20 bounded read-only agents with circuit breaker and budget enforcement
- 12 export formats: RDF, OWL, JSON-LD 1.1, Cypher, Gremlin, SPARQL, SHACL, GQL, and more
- MCP server with 17 read-only tools for VS Code / IDE integration
- Full test suite: 1,897 passed, 24 skipped, 0 failures (1,921 total test cases)

## Quick Start

From the repository root, with Docker Desktop running in Linux-container mode:

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

## Documentation

| Guide | Description |
|-------|-------------|
| [Architecture](eoip-engg-doc-pkg/06-architecture.md) | System overview, Docker services, data flows, storage, security |
| [API Reference](docs/api-reference.md) | All REST endpoints with request/response examples |
| [Connectors](docs/connectors.md) | All 24 source connectors with configuration |
| [Agents](docs/agents.md) | Agent framework, 20 agents, tool access policy |
| [RAG](docs/rag.md) | GraphRAG retrieval system, 7 strategies, evidence citations |
| [Query Engine](docs/query-engine.md) | 6 query languages, QueryPlan executor, safety policy |
| [Graph Algorithms](docs/graph-algorithms.md) | 30+ algorithms: centrality, community, paths, similarity |
| [Ontology](docs/ontology.md) | Vocabulary, vertex/edge labels, schema generation, SKOS |
| [Ingestion](docs/ingestion.md) | Ingestion pipeline, DLQ, checkpointing, semantic pipeline |
| [Code Graph](docs/code-graph.md) | Code parser, symbol extraction, CommitSymbolLink, diff hunks |
| [Multi-Backend](eoip-engg-doc-pkg/76-multi-backend.md) | HugeGraph, Neptune, memory backends — config and factory |
| [File Parsing](docs/file-parsing.md) | .docx, .xlsx, .pptx, .pdf, .csv, .txt ingestion |
| [Docker Local](docs/docker-local.md) | Full Docker runbook, backup/restore, VS Code extension |
| [Deep Agents & XAI](docs/deep-agents-xai.md) | Agent contracts, orchestration, approval workflows |
| [Benchmarking](docs/benchmarking.md) | Performance benchmarks |
| [Audit Report](docs/audit-2026-10-06/assessed-gap-report.md) | Pass 5 — comprehensive completion audit (2026-10-06) |

## On-prem source connectors

Actual local binary/text files can be converted into JSON, citation-aware RAG
chunks, graph records, and keyword/vector artifacts using the `documents`
connector or authenticated raw-file upload API. See
[file parsing and ingestion](docs/file-parsing.md) for formats, local tool
prerequisites, CLI/API examples, and explicit support limitations.

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

See the [Deep Agents and XAI guide](docs/deep-agents-xai.md) for governed agent contracts,
bounded orchestration, evidence-linked explanations, and approval-only change proposals.
