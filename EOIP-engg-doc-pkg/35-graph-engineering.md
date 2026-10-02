# Graph Engineering

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define semantic graph construction and query discipline

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Loop engineering designs bounded iterative execution; graph engineering designs semantic state and traversals; harness engineering supplies deterministic wrappers, tools, policies, observability and evaluation; context engineering constructs minimal evidence packages; memory engineering governs persistence. Graph-over-loop records loop state/outcomes as graph facts; loop-over-graph iteratively traverses/evaluates graph neighborhoods under explicit termination conditions.

The ontology is a controlled vocabulary, not simply a list of labels. Every entity type and relationship declares a definition, domain/range, required properties, cardinality expectations and lifecycle/version. The MVP implements only terms needed for the vertical slice while preserving namespaces for Organization, Work, Code, CI/CD, Operations, Knowledge and AI/Agent concepts.

The application exposes domain query services rather than database access. Exact identifier search anchors graph operations. Natural-language interpretation produces a typed QueryPlan, validated against ontology/schema and policy, then executes a named bounded Gremlin template. Depth, edge classes, result size and timeout are explicit inputs with hard maximums.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-002 | Logical graph domains | P1-MVP | Every business vertex/edge belongs to a valid domain. |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable. |
| FR-GRAPH-008 | Index strategy | P1-MVP | Benchmark-critical lookup paths use planned indexes. |

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
