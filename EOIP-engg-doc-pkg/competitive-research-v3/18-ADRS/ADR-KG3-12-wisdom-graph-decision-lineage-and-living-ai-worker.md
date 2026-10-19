# ADR-KG3-12: Wisdom Graph Decision Lineage and Living AI Worker

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Enterprises lose institutional rationale and repeat architectural mistakes because decision history is disconnected from code and data.

## 2. Decision Outcome
Mine Architecture Decision Records (ADRs) and git commit histories into Plane GW; deploy the Living AI Agent Graffin with 10 constitutional guardrails, a 4-channel kill switch, and an autonomous self-healing loop.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Transforms static documentation into an active, self-auditing organization brain.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
