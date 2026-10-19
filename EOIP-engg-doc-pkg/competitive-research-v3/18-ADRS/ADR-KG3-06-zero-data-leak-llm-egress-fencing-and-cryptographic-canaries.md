# ADR-KG3-06: Zero-Data-Leak LLM Egress Fencing and Cryptographic Canaries

| Field | Value |
|---|---|
| Status | **APPROVED** (Master Architecture Decision) |
| Deciders | Principal Architecture Review Board |
| Date | 2026-10-18 UTC |
| Relevant Capabilities | CAP-01 to CAP-80 |

---

## 1. Context & Problem Statement
Interacting with commercial LLMs risks exfiltrating proprietary code, connection strings, credentials, and PII.

## 2. Decision Outcome
Route all prompts through EgressSecurityGate; apply strict regex scrubbing and CodePseudonymizer; embed synthetic cryptographic canary tokens (egress_canary_...) and tripwire honeypots with an automated kill-switch.

## 3. Consequences & Trade-offs
### Positive Consequences:
- Enforces zero-data-leak compliance under REVA-SEC-013-STRICT.
- Fully aligns with KnowGridFlow non-negotiable constraints (air-gap capable, local-first, multi-tenant).

### Negative / Operational Consequences:
- Requires continuous conformance testing across HugeGraph, Neo4j, and Neptune.
- Initial engineering investment in AST compiler and derivation ACL tracking.

## 4. Reversibility
- **Reversibility Rating:** High. Decoupled behind the `GraphStore` protocol and standard OpenAPI contracts.
