# Enterprise Ontology

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Define ontology vocabulary, namespaces, lifecycle and mappings

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Scope and design intent

The ontology is a controlled vocabulary, not simply a list of labels. Every entity type and relationship declares a definition, domain/range, required properties, cardinality expectations and lifecycle/version. The MVP implements only terms needed for the vertical slice while preserving namespaces for Organization, Work, Code, CI/CD, Operations, Knowledge and AI/Agent concepts.

EOIP forbids an undifferentiated `RELATED_TO` model for core facts. Relationships express semantics such as CONTAINS, IMPLEMENTS, MODIFIES, CALLS, IMPORTS, DEPENDS_ON, REFERENCES, DOCUMENTS and EVIDENCED_BY. Every inferred edge records confidence and evidence and is visually/semantically distinct from deterministic and human-confirmed facts.


## Applicable requirements

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-ONTO-001 | Enterprise ontology vocabulary | P1-MVP | MVP entities/edges reference ontology version and valid terms. |
| FR-ONTO-002 | Relationship semantics | P1-MVP | No MVP business relationship relies on untyped generic edge. |
| FR-GRAPH-010 | RDF/OWL interoperability | P2 | No documentation claims native SPARQL support. |

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
