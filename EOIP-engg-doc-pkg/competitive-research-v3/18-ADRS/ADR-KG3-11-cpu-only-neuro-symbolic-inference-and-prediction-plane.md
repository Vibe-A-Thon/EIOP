# ADR-KG3-11: CPU-Only Neuro-Symbolic Inference and Prediction Plane

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Graph Neural Networks often introduce CUDA GPU dependencies and black-box unexplainable predictions that contaminate ground truth.

## 2. Decision Outcome
Establish a strict CPU-only execution discipline (N0-N3 runtime tiers) using SimpleLearnedGNN; isolate all ML link predictions in a dedicated Prediction Plane (PROPOSED_UNTIL_VALIDATED) requiring human steward approval.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Prevents ungrounded hallucinated facts from corrupting the core knowledge graph.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
