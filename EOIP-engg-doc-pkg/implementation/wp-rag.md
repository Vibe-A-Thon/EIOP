# WP-RAG Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Engineering plan for WP-RAG

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-RAG-001 | Retrieval router | P1-MVP | Known MVP questions route without external service. |
| FR-RAG-002 | GraphRAG evidence retrieval | P1-MVP | Demo GraphRAG answer cites graph/source references. |
| FR-RAG-003 | Local model abstraction | P1-MVP | Core search/path/impact remains usable with model service stopped. |
| FR-RAG-004 | No mandatory vector DB in MVP | P1-MVP | MVP starts and demos without vector database. |
| FR-RAG-005 | RAG evaluation harness | P1-MVP | Baseline report is reproducible locally. |
| FR-RAG-006 | Adaptive RAG strategy framework | P3 | P3 can add strategy plugin without changing callers. |

## Implementation sequence

### WP-RAG-01 — Retrieval router
**Objective:** Choose direct graph, linked documents, code context, graph+text hybrid or no retrieval.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** RetrievalRequest  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unknown intent chooses conservative graph/search path.  
**Tests:** Router table tests.  
**Acceptance:** Known MVP questions route without external service.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-001`.
### WP-RAG-02 — GraphRAG evidence retrieval
**Objective:** Retrieve entities, relationships, paths, neighborhoods, provenance and linked documents.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** GraphResult/Evidence  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Insufficient evidence yields explicit insufficiency, not invention.  
**Tests:** Golden question/evidence tests.  
**Acceptance:** Demo GraphRAG answer cites graph/source references.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-002`.
### WP-RAG-03 — Local model abstraction
**Objective:** Provide model interface for chat/generation and optional embeddings with all external providers disabled in MVP.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** ModelRequest/Response  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Model-down degrades to graph results and deterministic summaries.  
**Tests:** No-egress/model-down tests.  
**Acceptance:** Core search/path/impact remains usable with model service stopped.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-003`.
### WP-RAG-04 — No mandatory vector DB in MVP
**Objective:** Do not require a second database for semantic retrieval in Phase 1.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** DocumentSection  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Semantic-only request reports reduced capability if embeddings disabled.  
**Tests:** Model-off tests.  
**Acceptance:** MVP starts and demos without vector database.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-004`.
### WP-RAG-05 — RAG evaluation harness
**Objective:** Measure retrieval precision/recall, context relevance, evidence coverage, groundedness, answer correctness, latency and token usage.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** EvalCase/EvalResult  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Failed generation does not erase retrieval metrics.  
**Tests:** Automated evaluation tests.  
**Acceptance:** Baseline report is reproducible locally.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-005`.
### WP-RAG-06 — Adaptive RAG strategy framework
**Objective:** Expose strategy interface for simple/graph/hybrid/corrective/self/adaptive/agentic/multi-hop variants without instantiating all.  
**Dependencies:** canonical contracts, configuration, common logging/audit, and any prerequisite requirement documented in the master plan.  
**Interfaces/data:** RAGStrategy  
**Steps:** (1) write/validate contract or schema; (2) implement domain logic behind a port; (3) integrate with application composition root; (4) instrument logs/metrics; (5) add fixtures and tests; (6) update traceability/documentation.  
**Failure handling:** Unsupported strategy rejected cleanly.  
**Tests:** Strategy contract tests.  
**Acceptance:** P3 can add strategy plugin without changing callers.  
**Expected output:** reviewed code/configuration/tests plus reproducible acceptance evidence tagged `FR-RAG-006`.
