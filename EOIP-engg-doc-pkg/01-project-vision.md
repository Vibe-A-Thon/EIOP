# Project Vision

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define the product outcome and architectural north star

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

EOIP turns fragmented enterprise work, code, delivery and knowledge artifacts into a provenance-preserving operational knowledge graph. Its first measurable outcome is answering “what implements this requirement?”, “what changes if this symbol changes?”, and “why do we believe this relationship?” from persisted evidence. The platform is intentionally useful without generative AI; AI adds query interpretation, summarization and agent orchestration rather than replacing deterministic graph engineering.

Phase 1 proves one end-to-end vertical slice rather than breadth. Jira JSON, local Git/GitLab-style metadata, Python/TypeScript code and linked documentation are sufficient to prove ingestion, canonicalization, code parsing, cross-domain linking, provenance, validation, query, GraphRAG, UI, VS Code, MCP, observability and recovery. Confluence, ServiceNow, sophisticated temporal reconstruction, many RAG variants, distributed HugeGraph and write-capable agents are deferred with interfaces prepared now.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-001 | HugeGraph authoritative store | P1-MVP | All demo graph paths survive service restart. |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable. |
| FR-PROV-001 | Evidence model | P1-MVP | MVP evidence coverage is 100% for cross-domain bridge edges. |
| FR-QUERY-003 | Impact analysis | P1-MVP | Demo function change returns expected dependents with paths. |
| FR-RAG-002 | GraphRAG evidence retrieval | P1-MVP | Demo GraphRAG answer cites graph/source references. |

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
