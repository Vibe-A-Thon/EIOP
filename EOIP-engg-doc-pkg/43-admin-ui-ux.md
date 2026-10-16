# Admin UI/UX

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define engineering/admin operations UI

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The admin experience shows actual ingestion jobs, checkpoints, DLQ counts, graph/schema versions, validation findings, quality metrics, backup state and local model health. It uses the same authentication profile as the application in MVP; `/admin` route separation is never described as authorization.

The runbook assumes a restricted local environment: stage images/models, provision secrets, start Compose, verify readiness/schema, load demo or enterprise mappings, monitor job and graph quality, run smoke queries, back up before destructive maintenance, and capture diagnostics with correlation IDs. Recovery instructions favor replay/idempotency over manual graph surgery.

Validation has pre-mutation hard invariants and post-ingestion soft-quality rules. Findings are first-class records with severity, affected fact, evidence, remediation and run ID. Quality metrics are derived from these facts so dashboards cannot invent “health” percentages.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-ADMIN-001 | Admin ingestion UI | P1-MVP | Run state reconciles with backend/meta graph. |
| FR-ADMIN-002 | Admin graph quality UI | P1-MVP | No dashboard KPI is hardcoded. |
| FR-INGEST-004 | Ingestion job lifecycle | P1-MVP | Admin UI reflects actual backend run state. |
| FR-VALID-003 | Graph quality metrics | P1-MVP | Dashboard values reconcile with fixture counts. |

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
