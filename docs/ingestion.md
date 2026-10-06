# EOIP Ingestion Pipeline

EOIP ingests from 24 source connectors via a capture-then-normalize-then-mutate pipeline with a dead-letter queue, incremental checkpoints, and a validated write boundary.

---

## Pipeline Stages

```
Source Connector
    ↓ SourceEventV2 (immutable envelope)
JSON Processor / Connector-specific normalizer
    ↓ NormalizedEntity + NormalizedRelationship
IngestionGraphStore (validation gate)
    ↓ Validated GraphMutation
GraphStore.upsert_vertex() / upsert_edge() / tombstone_vertex()
    ↓
GraphEvolutionEngine (EntityRevision / RelationshipRevision)
    ↓
SemanticPipeline (bridge_edges, search_index, analytics)
```

---

## Ingestion Services

All services in `packages/eoip/ingestion/`:

| File | Service | Source |
|------|---------|--------|
| `jira.py` | `JiraIngestionService` | Jira REST API or JSON fixture |
| `jira_rest.py` | REST client for live Jira | Jira |
| `gitlab.py` | `GitLabIngestionService` | GitLab REST API or JSON fixture |
| `gitlab_rest.py` | REST client for live GitLab | GitLab |
| `code.py` | `CodeIngestionService` | Local git repository tree |
| `code_graph_json.py` | `CodeGraphJsonProcessor` | Pre-extracted code-graph JSON |
| `github.py` | `GitHubIngestionService` | GitHub REST API |
| `files.py` | `FileIngestionService` | Binary/text file upload |
| `json_processor.py` | `JsonIngestionProcessor` | Generic JSON source connector |
| `source_sync.py` | `SourceSyncService` | Incremental sync orchestrator |
| `repository.py` | `IngestionRepository` | Run history and metadata |
| `dlq.py` | Dead-letter queue writer | All services |
| `replay.py` | `DLQReplayService` | Dead-letter queue |
| `semantic_pipeline.py` | `SemanticPipeline` | Post-ingestion enrichment |
| `pipeline.py` | `IngestionGraphStore` | Validated write boundary |

---

## Validated Write Boundary (`ingestion/pipeline.py`)

`IngestionGraphStore` wraps `GraphStore` and enforces:
- **Ontology conformance**: entity_type must be in `VERTEX_LABELS`
- **canonical_id consistency**: rejects canonical_id conflicts
- **graph_domain conformance**: domain must match ontology manifest
- **Property conformance**: required properties must be present
- **Edge endpoint existence**: relationship endpoints must exist in graph

Any violation raises `MutationBlocked` (never silently swallowed).

```python
store = IngestionGraphStore(graph_store)
store.write_entity(normalized_entity)      # → upsert_vertex
store.write_relationship(normalized_rel)   # → upsert_edge
```

---

## GraphEvolutionEngine

`packages/eoip/graph/evolution.py`

Tracks temporal writes. Every `upsert_vertex` creates an `EntityRevision`:
```
EntityRevision
  revision_id: str
  subject_id: canonical_id
  observed_at: datetime
  is_current: bool
  payload_json: str (snapshot of properties)
  previous_revision: str | None
```

Similarly `upsert_edge` creates `RelationshipRevision`.

A `GraphVersion` record marks each completed ingestion batch.

A `SemanticChange` event is emitted for changes detected as semantically significant (ADD, MODIFY, DELETE, SCHEMA_CHANGE). `SemanticChangeEvent.before_state` and `after_state` are excluded from the SHA-256 hash chain to prevent the chain from encoding volatile snapshot data.

---

## Dead-Letter Queue (`ingestion/dlq.py`)

Events that fail normalization or mutation land in the DLQ:

```
deploy/dlq/<source>/<timestamp>/<event_id>.json
```

DLQ record fields:
- `source`: connector name
- `event_id`: original event ID
- `error`: exception message
- `payload`: original raw payload
- `failed_at`: ISO timestamp

### DLQ Replay (`ingestion/replay.py`)

```python
replay_service = DLQReplayService(dlq_root, ingestion_service)
result = replay_service.replay(dlq_ref="dlq://jira/2026-10-01T10:00:00Z")
```

API: `POST /api/v1/admin/ingestion/replay`  
View queue: `GET /api/v1/ingestion/dlq`

---

## Checkpointing

All connectors return a `checkpoint` dict — serializable resume state. Between runs, checkpoints are stored in `deploy/checkpoints/<source_id>.json`.

On restart, `SourceSyncService` loads the checkpoint and resumes from the last known position (e.g., updated_after, page cursor, commit SHA).

---

## Jira Ingestion (`ingestion/jira.py`)

### Fixture Mode (JSON)
```python
service = JiraIngestionService(store, connector=JiraJsonConnector("demo/demodata/jira.json"))
result = service.ingest()
```

### Live Mode
Uses `jira_rest.py` to poll Jira API with `updated_after` checkpoint.

Normalizes: Project, WorkItem, Person, Sprint, Version, Comment, WorkItemChange, IssueType, Status.

Cross-references: `ASSIGNED_TO`, `REPORTED_BY`, `CONTAINS`, `REFERENCES`, `LINKED_TO`.

---

## GitLab Ingestion (`ingestion/gitlab.py`)

Normalizes: Repository, MergeRequest, Commit, PipelineRun, Job, Branch, Tag, Release.

Cross-references: `INTRODUCES`, `IMPLEMENTS`, `TRIGGERS`, `IN_BRANCH`.

---

## Code Ingestion (`ingestion/code.py`)

`CodeIngestionService` flow:

1. `LocalCodeConnector.events(root, repo_id)` — walks file tree, yields `SourceEvent` per file
2. `CodeParser.parse(repo_id, path, source)` — AST parse to extract CodeSymbol list
3. For each symbol: `IngestionGraphStore.write_entity(CodeSymbol)`
4. Creates `DEFINES` edges (File → CodeSymbol), `CALLS` edges (symbol → symbol)
5. Creates `CommitSymbolLink` for symbols modified in a commit
6. DLQ write on any parse failure

---

## Code Graph JSON Ingestion (`ingestion/code_graph_json.py`)

`CodeGraphJsonProcessor` ingests pre-extracted code-graph JSON (from static analysis tools):

Expected JSON format:
```json
{
  "files": [{"path": "src/PaymentController.py", "language": "python"}],
  "symbols": [{"qualified_name": "PaymentController.process", "kind": "method", "file": "...", "start_line": 12, "end_line": 45}],
  "edges": [{"from": "...", "to": "...", "type": "CALLS"}]
}
```

API: `POST /api/v1/admin/ingestion/code-graph-json`

---

## Semantic Pipeline (`ingestion/semantic_pipeline.py`)

Runs post-ingestion enrichment in 6 stages:

| Stage | Description |
|-------|-------------|
| `bridge_edges` | Creates cross-domain bridge edges (WorkItem ↔ Commit ↔ CodeSymbol) |
| `metadata_enrichment` | Enriches entities with computed properties (depth, centrality hints) |
| `search_index` | Builds `InMemorySearchIndex` from all graph entities |
| `analytics` | Runs lightweight centrality pass |
| `validation` | Runs `OntologyDriftChecker` and `ValidationGate` |
| `event_publish` | Publishes `SemanticChange` events for downstream consumers |

Triggered automatically after bulk ingestion. Can be triggered manually:

```
POST /api/v1/admin/semantic-pipeline
{"stages": ["bridge_edges", "search_index"]}
```

Agent: `SemanticIndexAgent` can run individual stages with scope filtering.

---

## Ingestion Run Tracking

Every ingestion run creates an `IngestionRun` vertex:

```
IngestionRun:
  run_status: PENDING | RUNNING | DONE | FAILED
  run_kind: FULL | INCREMENTAL | REPLAY
  source_system: jira | gitlab | git | ...
  records_accepted: int
  records_rejected: int
  started_at: datetime
  finished_at: datetime
```

API: `GET /api/v1/ingestion/runs`

---

## File Ingestion (`ingestion/files.py`)

`FileIngestionService` processes uploaded files via the fileparse engine:

| Format | Parser |
|--------|--------|
| `.pdf` | `fileparse/pdf.py` |
| `.docx` | `fileparse/docx.py` |
| `.xlsx` | `fileparse/xlsx.py` |
| `.pptx` | `fileparse/pptx.py` |
| `.txt`, `.md` | `fileparse/text.py` |
| `.csv` | `fileparse/csv.py` |

Creates: `Document` vertex + `DocumentSection` vertices + `PART_OF` edges.

API: `POST /api/v1/upload`
