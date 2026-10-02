# Scope and Objectives

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define in-scope, out-of-scope and phase boundaries

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Phase 1 proves one end-to-end vertical slice rather than breadth. Jira JSON, local Git/GitLab-style metadata, Python/TypeScript code and linked documentation are sufficient to prove ingestion, canonicalization, code parsing, cross-domain linking, provenance, validation, query, GraphRAG, UI, VS Code, MCP, observability and recovery. Confluence, ServiceNow, sophisticated temporal reconstruction, many RAG variants, distributed HugeGraph and write-capable agents are deferred with interfaces prepared now.

The roadmap protects the vertical slice. P0 establishes contracts/schema/security foundations; P1 delivers the integrated MVP; P2 broadens connectors/ontology; P3 advances retrieval/RAG; P4 adds multi-agent patterns; P5 temporal/analytics; P6 human-control automation; P7 enterprise scale/hardening; P8+ controlled self-improvement only after governance exists.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CONN-002 | Jira JSON connector | P1-MVP | Repeat import is idempotent and creates expected graph. |
| FR-CONN-003 | Git repository connector | P1-MVP | Repository, branch and commit nodes plus modifications exist. |
| FR-CODE-002 | Python and TypeScript MVP parsing | P1-MVP | Demo repo symbols and imports/calls are queryable. |
| FR-RAG-004 | No mandatory vector DB in MVP | P1-MVP | MVP starts and demos without vector database. |
| FR-AGENT-003 | TraceImpact agent | P1-MVP | Same demo question works via UI/API/MCP context. |

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
