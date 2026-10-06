# EOIP System Architecture

Enterprise Ontology & Intelligence Platform — system architecture reference.

---

## Overview

EOIP is a **local-first, privacy-preserving knowledge graph platform** that ingests data from enterprise source systems (Jira, GitLab, GitHub, Confluence, ServiceNow, etc.), builds a unified property graph in Apache HugeGraph, and exposes that graph via a REST API, MCP interface, web UI, and VS Code extension — with GraphRAG, bounded agents, and 30+ graph algorithms.

```
Source Systems → Connectors → Ingestion Pipeline → Graph Store → Query/RAG/Agent Layer → UIs
```

---

## Component Map

### Backend Services (Docker)

| Service | Port | Responsibility |
|---------|------|---------------|
| `hugegraph-server` | Internal | HugeGraph 1.7.0 with RocksDB; authoritative graph store |
| `hubble` | 8088 | Hubble 1.7.0; schema browser, graph viz, Gremlin console |
| `hubble-init` | — | Idempotent connection registration (one-shot) |
| `schema-init` | — | One-time idempotent vertex/edge/index bootstrap |
| `eoip-api` | 8000 | FastAPI: query, RAG, agents, admin, metrics |
| `eoip-worker` | — | Single-worker durable filesystem queue; ingestion jobs |
| `eoip-web` | 8080 | React SPA (Nginx); same-origin proxy to API |
| `eoip-mcp` | 8001 | FastMCP; 17 read-only tools, TokenBoundary auth |

### Application Packages (`packages/eoip/`)

| Subpackage | Files | Purpose |
|------------|-------|---------|
| `connectors/` | 36 | 24 source connectors + SDK infrastructure |
| `graph/` | 40 | GraphStore protocol, HugeGraph adapter, algorithms, evolution, formats |
| `agents/` | 20 | 20 bounded agents with runtime + circuit breaker |
| `ingestion/` | 16 | Source-specific ingestion services, DLQ, replay |
| `ontology/` | 9 | Manifest, schema gen, SKOS, RDF, embedding drift |
| `query/` | 9 | QueryPlan executor, NLQ, EQL, query languages |
| `retrieval/` | 5 | RAG retrieval, strategy registry, eval |
| `codegraph/` | 3 | AST parser, diff hunk, language support |
| `contracts/` | 14 | Typed Pydantic contracts: events, entities, agents, tools |
| `provenance/` | 4 | Evidence model, lineage service |
| `identity/` | 3 | Deterministic identity resolution, candidate queue |
| `validation/` | — | Validation engine, gates, quality metrics |
| `audit/` | 3 | Audit sink, redaction |
| `models/` | 4 | LocalModelProvider (Ollama), graceful fallback |
| `fileparse/` | 12 | File format parsers (Office, text, media, PDF) |

---

## Data Flow

### 1. Source Ingestion Path

```
External System
      ↓
SourceConnector.discover() → DiscoveryResult
      ↓
SourceConnector.extract(checkpoint) → SourceEventV2 (immutable, payload_hash, captured_at)
      ↓
AcquisitionPolicy (dry_run, resume, checkpoint validation)
      ↓
Ingestion Service (jira.py, gitlab.py, code.py, etc.)
  → NormalizedEntity / NormalizedRelationship (typed, confidence, creation_status)
      ↓
IngestionGraphStore (validation boundary)
  → validate NormalizedEntity/NormalizedRelationship
      ↓
GraphStore.upsert_vertex() / upsert_edge()  OR  GraphEvolutionEngine.evolve_entity()
      ↓
HugeGraph (RocksDB) — canonical_id → SHA-256 vertex_id
      ↓
ChangeJournal (hash-chained NDJSON) → SemanticEventBus (pub/sub)
```

### 2. Query Path

```
HTTP POST /api/v1/query
      ↓
QueryPlan (intent, anchors, depth, timeout, evidence_mode)
      ↓
QueryPolicy.validate() (max_depth=8, max_results=500, timeout=30s)
      ↓
QueryExecutor.execute()
  ├─ SEARCH → scan by canonical_id / name / issue_key / path
  ├─ PATH → BFS / Yen's k-shortest paths
  ├─ IMPACT → blast-radius + rationale per entity
  ├─ NLQ → NL→QueryPlan (rule-based fast path + Ollama fallback)
  └─ EQL → EOIP Query Language parser
      ↓
GraphResult (nodes, edges, paths, evidence list, partial flag)
```

### 3. RAG Path

```
HTTP POST /api/v1/rag
      ↓
RAGRouter.select_strategy() (17 routing patterns)
      ↓
RetrievalStrategy (7 modes: GRAPH, KEYWORD, HYBRID, SEMANTIC, EVIDENCE, LINEAGE, AGENT)
      ↓
StrategyRegistry.execute_chain() (4 built-in strategies: GraphDepth, EvidenceWeight, DomainFocus, Freshness)
      ↓
LocalModelProvider.generate() (Ollama) OR structured fallback
      ↓
EvidenceManifest (stable URN citations: canonical_id + source_ref)
```

### 4. Agent Path

```
HTTP POST /api/v1/agents/{type}
      ↓
AgentRuntime (budget clamping, circuit breaker, step/tool/recursion limits)
      ↓
Agent.run() (READ_TOOLS frozenset only — no write tools)
      ↓
Tool calls: graph query, RAG, validation, metrics, algorithms
      ↓
ExplanationEnvelope (evidence_refs, calibrated confidence, rationale)
```

---

## Graph Schema

### Authoritative Domains (14)

`CODE`, `WORK`, `CICD`, `KNOWLEDGE`, `PEOPLE`, `INFRASTRUCTURE`, `SECURITY`, `COMPLIANCE`, `CATALOG`, `QUALITY`, `TEMPORAL`, `PROVENANCE`, `META`, `TRUST`

### Core Vertex Labels (40+)

Work: `WorkItem`, `Sprint`, `Epic`, `Project`  
Code: `Repository`, `File`, `CodeSymbol`, `Commit`, `MergeRequest`, `Pipeline`  
People: `Person`, `Team`, `Organisation`  
Knowledge: `Document`, `DocumentSection`, `KnowledgeArticle`  
Infrastructure: `Service`, `Endpoint`, `Container`, `Deployment`  
Provenance: `Evidence`, `DataSource`, `IngestionRun`  
Meta: `GraphDomain`, `OntologyVersion`, `ValidationRun`, `Finding`  

### Core Edge Labels (30+)

`IMPLEMENTS`, `REFERENCES`, `DOCUMENTS`, `PRODUCED_BY`, `TRACES_TO`, `BELONGS_TO_DOMAIN`,  
`ASSIGNED_TO`, `CONTAINS`, `DECLARES`, `CALLS`, `IMPORTS`, `DEPENDS_ON`,  
`COMMITTED_TO`, `MERGED_VIA`, `DEPLOYED_BY`, `EVIDENCE_FOR`, `AUTHORED_BY`

### Index Strategy (12+ indexes)

- `UNIQUE` on `canonical_id` for all vertex types
- Composite on `(domain, label)` for domain scans
- Single-column on `created_at`, `updated_at` for temporal access
- Full-text on `name`, `description` for search

---

## Security Architecture

| Layer | Implementation |
|-------|---------------|
| Authentication | Single-user EOIP_API_TOKEN; non-loopback requires token |
| Data egress | No outbound calls — Ollama only; `tests/security/test_no_egress.py` |
| Secret isolation | `audit/redaction.py` scrubs secrets from audit records + repr() |
| Input safety | Path validation, size limits, traversal rejection in fileparse + connectors |
| Injection defense | Template injection prevention (forbids `{}$\` in params); retrieved content as data |
| Container | Non-root user, read-only filesystem, dropped capabilities |
| Audit | Persistent audit sink for auth/ingestion/query/agent/admin/backup events |

---

## Observability

| Concern | Implementation |
|---------|---------------|
| Metrics | Prometheus-format `GET /metrics` — counters (requests, operations, failures), histograms (duration, job_duration) |
| Logging | `packages/eoip/observability.py` — JsonLogFormatter, correlation ID middleware |
| Health | `/health/live`, `/health/ready` endpoints |
| Tracing | Correlation IDs propagated through all request-scoped operations |
| Audit | `packages/eoip/audit/sink.py` — persistent audit event sink |

---

## Storage

| Data | Location | Format |
|------|---------|--------|
| Graph vertices/edges | HugeGraph + RocksDB (Docker volume) | Property graph |
| Raw source events | Worker filesystem (Docker volume) | SourceEventV2 NDJSON |
| Dead-letter queue | Worker filesystem | DLQ NDJSON |
| Job records | Worker filesystem | JobQueue NDJSON |
| Change journal | Worker filesystem | Hash-chained NDJSON |
| Snapshots | Worker filesystem | Checksummed archive |
| Connector state | `state/connectors/{source}.json` | Checkpoint JSON |
| Corpus/documents | Worker filesystem | Document + chunk records |

---

## Deployment

Local Docker deployment via `.\scripts\docker.ps1 up`. See [docker-local.md](docker-local.md) for full instructions.

All ports bind to `127.0.0.1` — not exposed to the network. This is a local development model.

For details on backup/restore, demo data loading, optional Hubble setup, and VS Code extension, see:
- [docker-local.md](docker-local.md) — Docker deployment and services
- [hubble-local.md](hubble-local.md) — HugeGraph Hubble browser setup
- [deployment-verification.md](deployment-verification.md) — Deployment verification steps
