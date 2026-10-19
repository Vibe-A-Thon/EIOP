# ADR-KG3-09: Two-Phase Transactional Operational Action Write-Backs

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Enterprise knowledge graphs are traditionally passive and read-only, unable to execute governed write-backs to source systems.

## 2. Decision Outcome
Adopt Palantir-inspired operational actions declared as SHACL-constrained shapes; execute via a two-phase transactional outbox with dry-run simulation, approval gates, and source read-back verification.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Enables safe, reversible operational workflows directly from the knowledge workbench.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
