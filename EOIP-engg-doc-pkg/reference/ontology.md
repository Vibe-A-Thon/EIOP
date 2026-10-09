# EOIP Ontology

EOIP uses a controlled vocabulary (not a configurable ontology) defining all vertex labels, edge labels, property keys, and graph domains.

**Ontology version**: 0.4.0  
**Schema version**: 1.2  
**Source**: `packages/eoip/ontology/manifest.py`

---

## Graph Domains (14)

One physical HugeGraph instance, 14 logical domains:

| Domain | Scope |
|--------|-------|
| META | Ingestion runs, ontology versions, evidence, validation |
| WORK | Projects, work items, sprints, versions, epics, features |
| CODE | Repositories, files, symbols, commits, services, APIs |
| CICD | Merge requests, pipeline runs, jobs, releases, deployments |
| KNOWLEDGE | Documents, knowledge spaces, KB articles, knowledge products |
| IDENTITY | Persons, organizations |
| AGENT | Agent runs |
| OPS | Incidents, change requests, dashboards, monitors, alerts, metrics |
| TEST | Test cases, suites, cycles, runs |
| DESIGN | Figma design files, pages, components |
| INTEGRATION | Generic entities from JSON ingestion pipelines |
| DECISION | Decisions, alternatives, outcomes |
| PROCESS | Process models, process steps, process events |
| BUSINESS | Objectives, capabilities, value streams |

---

## Vertex Labels (50+)

### META Domain
| Label | Required Properties |
|-------|-------------------|
| `DataSource` | canonical_id, name, source_system |
| `IngestionRun` | canonical_id, run_status, run_kind |
| `GraphDomain` | canonical_id, name |
| `OntologyVersion` | canonical_id, ontology_version |
| `Evidence` | canonical_id, source_system, source_ref, method |
| `ValidationRun` | canonical_id, run_status |
| `ValidationFinding` | canonical_id, severity, rule_id |
| `EntityRevision` | canonical_id, revision_id, subject_id, observed_at, is_current, payload_json, source_event_id |
| `RelationshipRevision` | canonical_id, revision_id, relationship_id, relationship_type, from_id, to_id, observed_at, is_current |
| `GraphVersion` | canonical_id, graph_version, created_at |
| `SemanticChange` | canonical_id, graph_version, change_kind, observed_at, payload_json |

### WORK Domain
| Label | Required Properties |
|-------|-------------------|
| `Project` | canonical_id, name |
| `WorkItem` | canonical_id, issue_key, summary |
| `IssueType` | canonical_id, issue_type_id, name |
| `Status` | canonical_id, status_id, name |
| `Version` | canonical_id, version_id, name |
| `Sprint` | canonical_id, sprint_id, name |
| `Comment` | canonical_id, comment_id, content |
| `WorkItemChange` | canonical_id, change_id, field_name |
| `Epic` | canonical_id, name (Rally) |
| `Feature` | canonical_id, name (Rally) |
| `UserStory` | canonical_id, name (Rally) |
| `Requirement` | canonical_id, name |

### CODE Domain
| Label | Required Properties |
|-------|-------------------|
| `Repository` | canonical_id, repo_id, name |
| `Branch` | canonical_id, branch_name |
| `Commit` | canonical_id, commit_sha |
| `File` | canonical_id, repo_id, path |
| `CodeSymbol` | canonical_id, qualified_name, symbol_kind |
| `Dependency` | canonical_id, name |
| `Service` | canonical_id, service_id, name |
| `Tag` | canonical_id, repo_id, tag_name |
| `APIService` | canonical_id, api_name |
| `APIEndpoint` | canonical_id, api_name, api_method, api_path |
| `APIConnection` | canonical_id, upstream_service, downstream_service |

### CICD Domain
| Label | Required Properties |
|-------|-------------------|
| `MergeRequest` | canonical_id, mr_iid, mr_title |
| `PipelineRun` | canonical_id, name |
| `Job` | canonical_id, job_id, name |
| `Release` | canonical_id, name, tag_name |
| `Artifact` | canonical_id, name |
| `Deployment` | canonical_id, name |
| `BuildRecord` | canonical_id, name |

### OPS Domain
| Label | Required Properties |
|-------|-------------------|
| `Incident` | canonical_id, incident_number, summary |
| `ChangeRequest` | canonical_id, name, change_type |
| `ServiceRequest` | canonical_id, name |
| `Dashboard` | canonical_id, name, dashboard_type |
| `MonitorRule` | canonical_id, name, monitor_type |
| `AlertEvent` | canonical_id, name |
| `Metric` | canonical_id, name |
| `LogAggregate` | canonical_id, log_source |

### Other Domains (TEST, DESIGN, KNOWLEDGE, IDENTITY, etc.)
See `manifest.py` `VERTEX_LABELS` for full list.

---

## Edge Labels (30+)

`packages/eoip/ontology/manifest.py` — `EDGE_LABELS`

Representative edges:

| Edge | From → To | Meaning |
|------|-----------|---------|
| `ASSIGNED_TO` | WorkItem → Person | Assignee |
| `REPORTED_BY` | WorkItem → Person | Reporter |
| `CONTAINS` | Project → WorkItem | Issue belongs to project |
| `IMPLEMENTS` | Commit → WorkItem | Commit addresses issue |
| `INTRODUCES` | Commit → File | File was added/modified |
| `DEFINES` | File → CodeSymbol | Symbol declared in file |
| `CALLS` | CodeSymbol → CodeSymbol | Function calls |
| `IMPORTS` | File → Dependency | Package import |
| `REFERENCES` | WorkItem → WorkItem | Cross-issue link |
| `TRIGGERS` | PipelineRun → Job | Pipeline stage |
| `DOCUMENTS` | Document → Service | Documentation target |
| `OBSERVED_IN` | Evidence → Entity | Evidence links to entity |
| `REVISED_TO` | EntityRevision → EntityRevision | Version chain |
| `HAS_DOMAIN` | GraphDomain → Entity | Domain membership |
| `DEPLOYS` | Deployment → Service | Deployment target |
| `EXPOSES` | Service → APIEndpoint | Published endpoint |
| `COVERS` | TestCase → CodeSymbol | Test coverage |
| `DEPENDS_ON` | Service → Service | Runtime dependency |
| `CORRELATES_WITH` | Incident → WorkItem | Incident-to-issue link |

---

## Canonical ID Format

All entities use a URI-like canonical ID:

```
urn:<source_system>:<domain_key>/<entity_key>
```

Examples:
- `urn:jira:PAY-123`
- `urn:gitlab:!456`
- `urn:git:abc123def456`
- `urn:service:payment-gateway`
- `urn:codesymbol:payment-gateway/PaymentController/processPayment`

Canonical IDs are stable across graph rebuilds and are the citation key in all RAG evidence.

---

## Schema Generation (`packages/eoip/ontology/schema_gen.py`)

Generates schema artifacts from the ontology manifest:

```python
from eoip.ontology.schema_gen import SchemaGenerator

gen = SchemaGenerator()
json_schema = gen.generate_json_schema("WorkItem")
openapi_schema = gen.generate_openapi("WorkItem")
form_spec = gen.generate_form_spec("WorkItem")
```

API: `POST /api/v1/ontology/schema/generate`

---

## SKOS Export (`packages/eoip/ontology/skos.py`)

Generates SKOS concept scheme from the ontology vocabulary:

- Each vertex label becomes a `skos:Concept`
- Domain membership via `skos:inScheme`
- Relationships via `skos:related`

API: `GET /api/v1/ontology/export?format=skos`

---

## RDF / JSON-LD Export (`packages/eoip/ontology/rdf.py`)

`packages/eoip/ontology/rdf.py` generates:
- JSON-LD 1.1 with `@context` embedding all property keys
- RDF Turtle with OWL class assertions
- RDFS with domain/range declarations

API: `GET /api/v1/ontology/export` (default: JSON-LD 1.1)

---

## Ontology Packs (`packages/eoip/ontology/packs.py`)

Ontology packs are domain-scoped subsets of the ontology for publishing or federation:

```python
pack = OntologyPack.from_domain("CODE")
# Includes: Repository, File, CodeSymbol, Commit, Dependency, Service, ...
```

---

## Embedding Drift Detection (`packages/eoip/ontology/embedding_drift.py`)

Monitors structural drift in graph embedding space:

- Computes embedding centroid per domain
- Detects entities that drift outside ±2σ of their domain centroid
- Raises `EmbeddingDriftWarning` for significant drift events

Triggered automatically after bulk ingestion runs.

---

## Ontology Drift (`packages/eoip/ontology/drift.py`)

`OntologyDriftChecker` runs post-ingestion:
- Verifies all new vertices/edges conform to `VERTEX_LABELS` / `EDGE_LABELS`
- Detects properties added outside the manifest
- Emits `SchemaViolation` findings to `ValidationRun`

---

## GitOps Integration (`packages/eoip/ontology/gitops.py`)

Manages ontology versioning via git:
- Tracks `ONTOLOGY_VERSION` and `SCHEMA_VERSION` changes in git history
- Generates a migration summary when the ontology version increments
- Used by CI/CD to gate deployments when schema is incompatible

---

## HugeGraph Schema Bootstrap

On first start, `packages/eoip/graph/hugegraph.py` creates the HugeGraph schema:

1. Create all property keys (TEXT, INT, LONG, DOUBLE, BOOLEAN, DATE types)
2. Create all vertex labels with required and optional property lists
3. Create all edge labels with domain and range constraints
4. Create indexes (secondary + composite) for search performance

If HugeGraph is unavailable, the system falls back to `MemoryGraphStore` (in-memory dict-based store) for local dev.
