# ADR-KG3-10: Sigma.js WebGL Visualization Consolidation and Cytoscape Deprecation

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Maintaining competing graph visualization runtimes (Cytoscape + Sigma) inflates bundle size and fragments UI behavior.

## 2. Decision Outcome
Consolidate strictly on Sigma.js + Graphology as the sole primary WebGL graph renderer (Rule R13); provide synchronized WCAG 2.2 AA accessible table and tree views upon WebGL context loss.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Achieves smooth 60 FPS rendering on 100,000+ nodes while meeting enterprise accessibility standards.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
