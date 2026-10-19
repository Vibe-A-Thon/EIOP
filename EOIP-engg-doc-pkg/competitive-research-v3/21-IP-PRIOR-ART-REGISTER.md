# 21 — Intellectual Property & Prior-Art Register (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 21-IP-PRIOR-ART-REGISTER.md |
| Scope | Candidate Novel Inventions, Prior Art Mapping & Freedom-to-Operate Flags |
| Legal Disclaimer | Technical analysis only; not formal legal opinion. Items flagged for IP counsel review. |
| Verification Cutoff | 2026-10-18 UTC |

---

## 1. Candidate Novel Inventions & Patentability Analysis

### Invention 1: Derivation-Aware Access Control List Composition in Graph Traversals
- **Novelty:** Traditional knowledge graphs treat materialized edges as globally readable or apply post-filtering on query results. The invention mathematically calculates the intersected union of all premise ACLs at materialization and binds them to a monotonic policy epoch counter.
- **Related Prior Art:**
  - US Patent 9,646,168 (Palantir Technologies): "Dynamic access control in object-centric data environments".
  - US Patent 10,817,597 (Microsoft): "Graph-based access control evaluation".
- **Differentiator / FTO:** Palantir's patent focuses on object-centric relational views; our mechanism operates on arbitrary multi-hop recursive deductive proofs and vector embeddings across heterogeneous graph backends.
- **Recommendation:** Flag for defensive patent filing.

### Invention 2: Hybrid Tiered Reasoning with Provenance Vector Single-Premise Retraction
- **Novelty:** Solves the classic dilemma between GraphDB's total forward chaining (slow write) and Stardog's backward chaining (slow read). Encodes dependency chains as compact bitwise provenance vectors enabling $O(1)$ retraction when premises are deleted.
- **Related Prior Art:**
  - Academic Datalog provenance semirings (Green et al., 2007).
  - RDFox Datalog materialization patents (Oxford University).
- **Differentiator / FTO:** Fully published in academic literature; free of patent barriers. Safe to build and open-source under Apache-2.0.

### Invention 3: Zero-Data-Leak Cryptographic Tripwire Canaries for LLM Egress Fencing
- **Novelty:** Embeds pseudorandom deterministic canaries into code embeddings and prompt contexts with an automated honeypot monitor that trips an instant kill-switch upon unauthorized exfiltration.
- **Recommendation:** Defensive publication / Trade secret.
