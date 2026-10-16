# Provenance and Lineage

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define evidence chain of custody

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Provenance is part of every mutation, not a separate report. Cross-domain links have evidence references to raw events, commits/diffs, parser output or mapping rules, plus ingestion/parser/ontology versions. API, UI, RAG and MCP return the same evidence identifiers so an answer can be audited independent of the LLM.

All externally ingested facts first become immutable `SourceEvent` envelopes with content hashes. Mappers generate versioned canonical entities and relationships. HugeGraph stores operational truth; local raw capture preserves source fidelity and replay. The canonical model is stable across connector implementations and includes source identity, provenance, creation status, confidence, temporal fields and version metadata.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-PROV-001 | Evidence model | P1-MVP | MVP evidence coverage is 100% for cross-domain bridge edges. |
| FR-PROV-002 | Provenance traversal | P1-MVP | User can trace demo answer to source fixture/commit metadata. |
| FR-INGEST-001 | Raw capture | P1-MVP | Every graph mutation references a captured event. |

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
