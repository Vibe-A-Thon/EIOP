# ADR-KG3-08: Splink Probabilistic Entity Resolution Integration

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Deterministic person identity keys fail to resolve misspelled, incomplete, or cross-system duplicate business entities.

## 2. Decision Outcome
Integrate Splink's DuckDB-accelerated Fellegi-Sunter probabilistic matching model into the ingestion pipeline, routing ambiguous matches to the candidate review queue.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Provides scalable, explainable entity deduplication without expensive proprietary per-record licensing fees.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
