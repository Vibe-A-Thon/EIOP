# EOIP API Reference

REST API served by `eoip-api` on port 8000. Full OpenAPI docs at `http://localhost:8000/docs`.

All endpoints (except `/health/*` and `/metrics`) require `Authorization: Bearer <EOIP_API_TOKEN>`.

---

## Query Endpoints

### `POST /api/v1/query`
Execute a structured QueryPlan.

```json
{
  "intent": "SEARCH|PATH|IMPACT|NLQ|EQL|NEIGHBORS",
  "anchors": [{"canonical_id": "urn:jira:PAY-123"}],
  "depth": 3,
  "timeout": 30,
  "evidence_mode": "FULL|SUMMARY|NONE"
}
```

Returns `GraphResult` with nodes, edges, paths, evidence list, partial flag.

### `POST /api/v1/query/language`
Execute EOQL, OSQL, or Semantic Query Language.

```json
{"language": "EOQL", "query": "SELECT WorkItem WHERE status = 'Open'"}
```

### `POST /api/v1/path`
Find paths between two entities.

```json
{"source": "urn:commit:abc123", "target": "urn:jira:PAY-100", "max_depth": 5}
```

### `POST /api/v1/impact`
Blast-radius impact analysis from an anchor entity.

```json
{"canonical_id": "urn:service:payment-gateway", "direction": "DOWNSTREAM", "max_depth": 4}
```

### `POST /api/v1/search`
Entity search by name, canonical_id, path, or issue_key.

```json
{"query": "PaymentController", "labels": ["CodeSymbol", "WorkItem"], "limit": 20}
```

### `POST /api/v1/nlq`
Natural language query → QueryPlan → execution.

```json
{"text": "What changed in the payment module last week?", "context_entities": []}
```

---

## RAG & Retrieval

### `POST /api/v1/rag`
GraphRAG retrieval with evidence citations.

```json
{
  "question": "Why did the payment gateway break in sprint 14?",
  "strategy": "HYBRID",
  "max_results": 10
}
```

Returns answer with `EvidenceManifest` (stable URN citations).

### `GET /api/v1/export/formats`
List all 12 supported export formats.

### `GET /api/v1/ontology/export`
Export the full ontology as JSON-LD 1.1 (OWL individuals + class assertions).

```
GET /api/v1/ontology/export?limit=5000
```

---

## Graph Algorithms

### `POST /api/v1/algorithms/run`
Execute any of the 30+ graph algorithms.

```json
{
  "algorithm": "pagerank|betweenness|community_detection|blast_radius|detect_rings|...",
  "parameters": {"start_vertex": "urn:service:auth", "max_depth": 3}
}
```

### `GET /api/v1/algorithms`
List all available algorithms with parameter schemas.

---

## Agent Endpoints

### `POST /api/v1/agents/query`
Run TraceImpactAgent on a natural-language question.

```json
{"question": "What services would break if auth-service is removed?", "budget": {"max_steps": 10}}
```

### `POST /api/v1/agents/analytics`
Run GraphAnalyticsAgent (single algorithm or swarm mode).

```json
{"goal": "ring_detection", "context_refs": ["urn:domain:CODE"]}
```

Swarm mode:
```json
{"goal": "swarm"}
```

### `POST /api/v1/agents/semantic-index`
Run SemanticIndexAgent to rebuild semantic indexing pipeline.

```json
{"stages": ["bridge_edges", "search_index"], "scope": "CODE"}
```

---

## Ingestion & Admin

### `POST /api/v1/admin/ingestion/jira`
Submit a Jira ingestion job.

```json
{"source_id": "jira-prod", "checkpoint": "2026-09-01T00:00:00Z", "dry_run": false}
```

### `POST /api/v1/admin/ingestion/confluence`
Submit a Confluence ingestion job.

```json
{"checkpoint": "2026-09-01T00:00:00Z", "dry_run": false}
```

### `POST /api/v1/admin/ingestion/servicenow`
Submit a ServiceNow ingestion job.

### `POST /api/v1/admin/ingestion/git`
Submit a Git repository ingestion job.

```json
{"repo_path": "/mnt/repos/payment-gateway", "dry_run": false}
```

### `POST /api/v1/admin/semantic-pipeline`
Manually trigger the semantic indexing pipeline.

```json
{"stages": ["bridge_edges", "metadata_enrichment", "search_index"], "scope": null}
```

### `GET /api/v1/ingestion/runs`
List ingestion run history (latest first).

### `GET /api/v1/ingestion/dlq`
View dead-letter queue entries.

### `POST /api/v1/admin/ingestion/replay`
Replay a dead-letter queue entry.

```json
{"dlq_ref": "dlq://jira/2026-10-01T10:00:00Z"}
```

---

## Validation & Quality

### `POST /api/v1/validation/run`
Trigger graph validation (all rules).

Returns `ValidationRun` with FindingList (hard violations + soft findings).

### `GET /api/v1/validation/runs`
List validation run history.

### `GET /api/v1/quality`
Current graph quality metrics (completeness, freshness, orphan rate, provenance coverage).

---

## Schema & Ontology

### `GET /api/v1/ontology/schema`
Full ontology schema (vertex/edge labels, properties, indexes, domains).

### `POST /api/v1/ontology/schema/generate`
Generate JSON Schema / OpenAPI / form spec from ontology.

```json
{"format": "json_schema|openapi|form_spec", "label": "WorkItem"}
```

### `GET /api/v1/ontology/domains`
List all 14 graph domains with vertex/edge label membership.

---

## Lineage & Provenance

### `POST /api/v1/lineage`
Trace a graph fact back to its source event and ingestion run.

```json
{"canonical_id": "urn:jira:PAY-123", "depth": 3}
```

### `POST /api/v1/evidence`
Retrieve evidence manifest for a set of canonical IDs.

```json
{"canonical_ids": ["urn:jira:PAY-123", "urn:commit:abc123"]}
```

---

## Admin Gremlin (Restricted)

### `POST /api/v1/admin/gremlin`
Execute raw Gremlin query. **Disabled by default.**

Enable by setting `EOIP_ADMIN_GREMLIN_ENABLED=1` in environment.

```json
{"query": "g.V().limit(10)", "parameters": {}}
```

Returns 501 if disabled or if using MemoryGraphStore.

---

## Observability

### `GET /metrics`
Prometheus-format metrics.

Counters: `eoip_requests_total`, `eoip_operations_total`, `eoip_failures_total`  
Histograms: `eoip_request_duration_seconds`, `eoip_job_duration_seconds`

### `GET /health/live`
Liveness probe — returns 200 when process is alive.

### `GET /health/ready`
Readiness probe — returns 200 when graph store and dependencies are ready.

---

## Upload & File Ingestion

### `POST /api/v1/upload`
Upload a binary/text file for document ingestion.

```
Content-Type: multipart/form-data
file: <binary>
```

Returns Document canonical_id.

### `GET /api/v1/code/export`
Export code graph as JSON for a repository.

```
GET /api/v1/code/export?repo=urn:repo:payment-gateway
```

---

## VS Code / MCP Surfaces

The MCP server at `http://localhost:8001/mcp` exposes 17 read-only tools:

`search_entities`, `get_entity`, `get_neighbors`, `find_path`, `impact_analysis`, `trace_lineage`, `get_evidence`, `list_domains`, `get_code_symbol`, `get_file_symbols`, `list_commits`, `get_merge_request`, `get_dependencies`, `query_graph`, `get_quality`, `get_ingestion_status`, `list_sources`

All tools are read-only. No mutation tools are exposed via MCP.
