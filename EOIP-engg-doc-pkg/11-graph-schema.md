# HugeGraph Graph Schema

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define property, vertex, edge and index schema

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The ontology is a controlled vocabulary, not simply a list of labels. Every entity type and relationship declares a definition, domain/range, required properties, cardinality expectations and lifecycle/version. The MVP implements only terms needed for the vertical slice while preserving namespaces for Organization, Work, Code, CI/CD, Operations, Knowledge and AI/Agent concepts.

EOIP forbids an undifferentiated `RELATED_TO` model for core facts. Relationships express semantics such as CONTAINS, IMPLEMENTS, MODIFIES, CALLS, IMPORTS, DEPENDS_ON, REFERENCES, DOCUMENTS and EVIDENCED_BY. Every inferred edge records confidence and evidence and is visually/semantically distinct from deterministic and human-confirmed facts.

All externally ingested facts first become immutable `SourceEvent` envelopes with content hashes. Mappers generate versioned canonical entities and relationships. HugeGraph stores operational truth; local raw capture preserves source fidelity and replay. The canonical model is stable across connector implementations and includes source identity, provenance, creation status, confidence, temporal fields and version metadata.


## MVP HugeGraph schema

### Shared property keys
`canonical_id`, `source_system`, `source_id`, `source_uri`, `graph_domain`, `entity_type`, `name`, `display_name`, `content_hash`, `creation_status`, `confidence`, `first_seen`, `last_seen`, `created_at`, `modified_at`, `deleted_at`, `valid_from`, `valid_to`, `source_version`, `ingestion_run_id`, `ontology_version`, `schema_version`, `repo_id`, `path`, `qualified_name`, `symbol_kind`, `start_line`, `end_line`, `issue_key`, `commit_sha`, `evidence_key`, `description`, `doc_format`, `space_key`, `media_type`, `file_size`.

### MVP vertex labels
`DataSource`, `IngestionRun`, `GraphDomain`, `OntologyVersion`, `Evidence`, `ValidationRun`, `ValidationFinding`, `Project`, `WorkItem`, `Person`, `Repository`, `Branch`, `Commit`, `MergeRequest`, `PipelineRun`, `File`, `CodeSymbol`, `Dependency`, `Document`, `KnowledgeSpace`, `DocumentSection`, `AgentRun`.

`Document.description` stores extracted text for Confluence pages and ServiceNow knowledge articles. Attachment records remain metadata-only. Existing HugeGraph deployments append newly required property keys to existing vertex/edge labels during the idempotent schema bootstrap; the bootstrap does not drop labels or properties. This additive ontology vocabulary is versioned as ontology `0.2.0`; the snapshot envelope remains schema `1.0`.

### MVP edge labels
`CONTAINS`, `PARENT_OF`, `ASSIGNED_TO`, `AUTHORED_BY`, `HAS_BRANCH`, `HAS_COMMIT`, `HAS_MERGE_REQUEST`, `MODIFIES`, `DECLARES`, `CALLS`, `IMPORTS`, `DEPENDS_ON`, `IMPLEMENTS`, `REFERENCES`, `DOCUMENTS`, `EVIDENCED_BY`, `INGESTED_IN`, `BELONGS_TO_DOMAIN`, `VALIDATED_BY`, `PRODUCED_BY`.

### Index baseline
Create exact/secondary indexes for `canonical_id`, `(source_system,source_id)`, `issue_key`, `commit_sha`, `repo_id+path`, `qualified_name`, `graph_domain+entity_type` and selected timestamps used by operational queries. Do not add every property to an index. Query benchmarks decide additional indexes.

### Uniqueness and idempotency
The platform-level unique key is `canonical_id`. A canonical entity ID is derived from a versioned namespace and stable source/business identity. Edge identity is derived from edge semantic type + source/target canonical IDs + source fact identity. Schema bootstrap and mutation code must be idempotent even if HugeGraph's internal ID/index semantics change.

## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-003 | Schema bootstrap | P1-MVP | Fresh stack auto-initializes and second run is no-op. |
| FR-GRAPH-004 | Canonical identifiers | P1-MVP | Every canonical entity has unique stable canonical_id. |
| FR-GRAPH-008 | Index strategy | P1-MVP | Benchmark-critical lookup paths use planned indexes. |
| FR-ONTO-002 | Relationship semantics | P1-MVP | No MVP business relationship relies on untyped generic edge. |

## Engineering rules

- Configuration is versioned; secrets are references, never committed values.
- Every persistent fact carries canonical identity and provenance where applicable.
- Every failure path returns a stable error category, logs a correlation ID, and avoids partial silent success.
- MVP behavior must remain functional without an external network and, for graph features, without a local LLM.
- New implementation work must add/adjust automated tests and traceability entries.

## Validation / definition of done

- Normative interfaces are implemented and documented.
- Automated tests mapped to the listed requirement IDs pass.
- Error, security, logging and configuration paths are exercised.
- Acceptance evidence is reproducible from a clean documented environment.
- Deferred capabilities remain behind stable interfaces and are not represented as already implemented.
