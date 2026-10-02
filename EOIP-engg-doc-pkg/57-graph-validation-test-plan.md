# Graph Validation Test Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define graph/ontology/provenance validation tests

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Tests are traceability assets. Unit/parser/connector/schema/integrity/ontology/identity/relationship/provenance/idempotency/recovery/query-limit/RAG/agent/MCP/UI/VS Code/security/Docker/backup/E2E/performance suites map to requirement IDs. A feature is done only when its requirement, implementation task, tests and acceptance evidence are linked.

Validation has pre-mutation hard invariants and post-ingestion soft-quality rules. Findings are first-class records with severity, affected fact, evidence, remediation and run ID. Quality metrics are derived from these facts so dashboards cannot invent “health” percentages.

The ontology is a controlled vocabulary, not simply a list of labels. Every entity type and relationship declares a definition, domain/range, required properties, cardinality expectations and lifecycle/version. The MVP implements only terms needed for the vertical slice while preserving namespaces for Organization, Work, Code, CI/CD, Operations, Knowledge and AI/Agent concepts.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-VALID-001 | Graph validation rules | P1-MVP | Admin UI shows real findings from demo data. |
| FR-VALID-002 | Validation gates | P1-MVP | Invalid endpoint edge cannot silently enter graph. |
| FR-VALID-003 | Graph quality metrics | P1-MVP | Dashboard values reconcile with fixture counts. |
| FR-PROV-001 | Evidence model | P1-MVP | MVP evidence coverage is 100% for cross-domain bridge edges. |

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
