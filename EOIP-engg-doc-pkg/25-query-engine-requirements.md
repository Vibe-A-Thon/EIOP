# Query Engine Requirements

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define safe structured/NL graph queries

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The application exposes domain query services rather than database access. Exact identifier search anchors graph operations. Natural-language interpretation produces a typed QueryPlan, validated against ontology/schema and policy, then executes a named bounded Gremlin template. Depth, edge classes, result size and timeout are explicit inputs with hard maximums.

Security is designed for a local trusted-network MVP without pretending that trusted means safe. The system minimizes exposed ports, runs components least-privileged, protects secrets, validates inputs, prevents prompt/tool injection from bypassing policies, denies outbound enterprise-data egress and records auditable actions.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | All NL and structured requests compile to validated QueryPlan. |
| FR-QUERY-002 | Path query | P1-MVP | Demo Jira-to-function path returns expected ordered edges. |
| FR-QUERY-003 | Impact analysis | P1-MVP | Demo function change returns expected dependents with paths. |
| FR-QUERY-004 | Entity search | P1-MVP | Demo Jira issue, commit and symbol are discoverable. |
| FR-QUERY-005 | Natural-language query interpretation | P1-MVP | Prompt injection cannot bypass QueryPlan policy. |
| FR-QUERY-006 | Query safety policy | P1-MVP | All exposed query endpoints pass policy conformance suite. |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | GraphRAG/UI/MCP consume same evidence format. |
| FR-QUERY-008 | Raw Gremlin admin boundary | P1-MVP | No public OpenAPI/MCP tool accepts free-form Gremlin in MVP. |
| FR-QUERY-009 | Natural-language query processor | P1-MVP | NLQ routes graph facts, query operators, QueryPlan execution and safe search fallback while returning answer text, confidence, highlights and follow-ups. |

## Natural-language query processor

The NLQ processor SHALL be the single public natural-language query layer for graph exploration. It SHALL route a question to the narrowest safe engine that can answer it:

1. graph fact/EQL routes for counts, domains, labels and relationship labels;
2. structured query operators for WHY, WHY NOT, WHAT CHANGED and contextual who/when/where/how questions;
3. natural-language-to-QueryPlan interpretation for search, path, impact, neighborhood, lineage and traceability;
4. graph-domain search fallback only when a question is clearly about known graph concepts but lacks a canonical anchor.

Every route SHALL preserve the QueryPlan safety boundary for graph traversal, SHALL avoid natural-language-to-Gremlin generation, and SHALL return a user-facing answer with machine-readable result data, confidence, highlights, warnings and suggested follow-up queries.

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
