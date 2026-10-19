# ADR-KG3-03: Derivation-Aware Access Control List Composition

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Triplestores and vector stores treat graph edges and embeddings as globally readable once materialized, leaking restricted facts to unauthorized users.

## 2. Decision Outcome
Every inferred edge and vector chunk cryptographically inherits the intersection of all supporting premise ACLs; enforce a monotonic policy epoch counter that invalidates dependent derived facts in O(1) upon permission revocation.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Eliminates permission leakage through logical deduction and vector search (GAP-01 / INV-01).
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
