# ADR-KG3-05: GitOps Ontology-as-Code Lifecycle and Schema Studio

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Traditional ontology tools (Protégé, TopBraid) are desktop-bound JVM apps or heavy monolithic enterprise appliances.

## 2. Decision Outcome
Define ontologies as versioned code artifacts (LinkML YAML / W3C Turtle) in git; automate CI SHACL validation tests; provide a calm browser-based collaborative Schema Studio writing to the same declarative source.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Provides continuous integration, semantic diff, and safe rollback for enterprise ontologies.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
