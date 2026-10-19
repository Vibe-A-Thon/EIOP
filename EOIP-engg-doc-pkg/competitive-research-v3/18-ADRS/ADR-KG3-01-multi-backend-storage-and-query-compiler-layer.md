# ADR-KG3-01: Multi-Backend Storage and Query Compiler Layer

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Supporting multiple heterogeneous graph backends (HugeGraph, Neo4j, Neptune) without vendor lock-in or client-side traversal loops.

## 2. Decision Outcome
Adopt a two-tier abstraction: a capability-negotiating GraphStore protocol for basic mutations/lookups, and a typed QueryPlan AST compiler translating high-level traversals into native Gremlin bytecode, Cypher 25, and SPARQL 1.1.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Enables 100% backend portability while preserving native database query optimizers.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
