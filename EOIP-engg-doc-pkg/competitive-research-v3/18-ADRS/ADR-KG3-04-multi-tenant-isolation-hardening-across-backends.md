# ADR-KG3-04: Multi-Tenant Isolation Hardening Across Backends

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Shared backend adapters contain zero tenant scoping parameters, relying on application-layer filtering labeled 'External gate'.

## 2. Decision Outcome
Enforce mandatory tenant ID prefixing on all entity keys, vertices, edge labels, vector segments, and caches, backed by SILO, BRIDGE, and POOL placement profiles.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Guarantees 0.00% cross-tenant data, cache, and log leakage in compliance with non-negotiable Rule R6.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
