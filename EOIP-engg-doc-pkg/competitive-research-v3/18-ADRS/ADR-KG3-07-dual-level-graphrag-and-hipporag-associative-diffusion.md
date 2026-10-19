# ADR-KG3-07: Dual-Level GraphRAG and HippoRAG Associative Diffusion

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Plain vector RAG fails on multi-hop questions, while Microsoft GraphRAG requires exorbitant offline LLM clustering costs.

## 2. Decision Outcome
Combine LightRAG dual-level routing (low-level entity + high-level theme) with HippoRAG Personalized PageRank (PPR) diffusion over knowledge graphs.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Delivers multi-hop associative retrieval with 85% lower token cost and sub-second retrieval latency.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
