# Context Engineering

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define evidence-first context construction

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

Loop engineering designs bounded iterative execution; graph engineering designs semantic state and traversals; harness engineering supplies deterministic wrappers, tools, policies, observability and evaluation; context engineering constructs minimal evidence packages; memory engineering governs persistence. Graph-over-loop records loop state/outcomes as graph facts; loop-over-graph iteratively traverses/evaluates graph neighborhoods under explicit termination conditions.

RAG is a retrieval framework, not a synonym for vector search. The MVP retrieval router chooses direct graph, linked code/doc context or graph+text hybrid based on intent. A local model may synthesize an answer, but the evidence package is independently returned. Advanced CRAG/Self-RAG/Adaptive/Agentic/Multi-hop strategies are plugins evaluated in P3.

Explainability is evidence-centric. The platform exposes source facts, graph paths, retrieval context, rule decisions, tool invocations, confidence/uncertainty and concise decision summaries. It neither requests nor stores hidden model chain-of-thought.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-RAG-002 | GraphRAG evidence retrieval | P1-MVP | Demo GraphRAG answer cites graph/source references. |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | GraphRAG/UI/MCP consume same evidence format. |
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
