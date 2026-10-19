# ADR-KG3-02: Hybrid Tiered Reasoning Engine (HTRE)

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Stardog backward chaining suffers from query-time timeout variance, while GraphDB forward materialization causes 10x write amplification and slow retracts.

## 2. Decision Outcome
Forward-materialize static taxonomic closures (RDFS subClassOf, subPropertyOf, domain/range) into high-speed memory-mapped prefix trees at ingest; rewrite complex OWL 2 DL axioms and SHACL shapes at query time; maintain O(1) retraction via bitwise provenance vectors.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Guarantees predictable sub-10ms read latency for taxonomy while eliminating write amplification.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
