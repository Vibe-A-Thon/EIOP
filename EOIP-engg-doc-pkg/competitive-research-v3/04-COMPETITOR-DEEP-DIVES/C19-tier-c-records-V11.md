# C19 — Tier C records (worker V11)

### T-C19-auth-aware-search — Authorization-aware search (pattern: pre-filter vs post-filter vs ACL-embedded index)

| Field | Value |
|---|---|
| Official URL | none (pattern); anchors: Zanzibar paper https://www.usenix.org/system/files/atc19-pang.pdf ; OpenSearch DLS (C10-opensearch STR-opensearch-01); Onyx (C07-onyx STR-onyx-01) |
| Owner | n/a (pattern) |
| Latest version + date | n/a; reference implementations tracked in C19-rebac, C19-opa, C19-cedar-cerbos |
| Status | established pattern; Zanzibar (2019) describes Expand-built ACL-aware search indexes |
| Licence + class | n/a |
| Deployment modes | library/design pattern inside retrieval |
| Air-gap viable | yes |
| Tier reason | pattern record (registry seed), but it is the design decision behind BL-18 (P0) |

**Relevance.** Three architectures for enforcing source ACLs in retrieval:

| Pattern | How | Pros | Cons / failure modes | Examples |
|---|---|---|---|---|
| Post-filter | retrieve top-K, check each hit with PDP, drop denied | simplest; always fresh if checked live; no index changes | recall collapse when deny ratio is high (K survivors < K); existence/count leaks via aggregates, timing, facets; wasted compute | Check loop in ReBAC engines (C19-rebac) |
| Pre-filter | policy/engine produces allowed IDs or a condition tree; applied inside ANN/BM25/graph query | correct top-K, no recall loss, leaks nothing when applied inside engine | allowed-ID lists truncate (OpenFGA ListObjects 1000 default; SpiceDB LookupResources 1000), plan operators must map to the store; two systems to keep consistent | OPA partial evaluation to SQL conditions (C19-opa), Cerbos PlanResources adapters incl. LangChain/ChromaDB (C19-cedar-cerbos) |
| ACL-embedded index | principal/group strings stored on each chunk and enforced by the engine (filter or document-level security) | engine-enforced, fast, covers aggregates; zero extra runtime hop | staleness when ACLs change (needs re-index or token), group expansion at index time explodes (Zanzibar Leopard analogue: one tuple change yields tens of thousands of index events), per-principal fields grow | Onyx per-chunk ACL principal strings; OpenSearch DLS (verify aggregation behaviour) |

Recommendation for EOIP (inference): hybrid. Index `acl_principals` (tenant-prefixed, unknown ACL = private) on every chunk/fact for engine-enforced coarse filtering, and verify survivors with the native PDP/ReBAC check at answer time with a revision token so revocations beat index staleness. Graph expansion must apply the check per hop (EOIP already has `DerivationACLEvaluator` for graph contexts) and the MCP layer must carry a per-user principal (INV-mcp-02). Touches CAP-46, CAP-47, CAP-53, CAP-54, CAP-55, CAP-56, CAP-59. Baseline: BL-18 (retrieval ACL; partial/re-audit at HEAD 896e06d: graph-context filtering present, lexical/vector stage unconfirmed), BL-17 (ACL captured at ingest), BL-20.

**Decision.** BUILD (ACL-embedded filter plus native recheck) with INTEGRATE of a ReBAC engine for group/inheritance resolution; EXPERIMENT on policy-compiled pre-filters.

**Evidence.**

| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-aas-01 | Zanzibar 2019 | Expand output is used by clients to build ACL-aware search indexes; Leopard denormalises nested sets; one tuple change can yield tens of thousands of index events | Peer-reviewed paper | https://www.usenix.org/system/files/atc19-pang.pdf | 2019 / 2026-10-26 | 0.9 | none |
| CLAIM-aas-02 | OpenFGA / SpiceDB | list/lookup defaults cap at 1000 results (OpenFGA deadline 3 s) | Officially documented | https://openfga.dev/docs/interacting/relationship-queries ; https://authzed.com/docs/spicedb/concepts/commands | n/a / 2026-10-26 | 0.85 | limits configurable |
| CLAIM-aas-03 | OPA / Cerbos | policy partial evaluation / PlanResources yields condition trees for DB or retriever filters | Officially documented | https://www.openpolicyagent.org/docs/filtering/partial-evaluation ; https://docs.cerbos.dev/cerbos/latest/api/index.html | n/a / 2026-10-26 | 0.8 | ES/OpenSearch target unconfirmed |
| CLAIM-aas-04 | Onyx / OpenSearch | per-chunk ACL strings; document-level security | Reasoned from sibling deep dives | C07-onyx.md STR-onyx-01 ; C10-opensearch.md STR-opensearch-01 | 2026-10 / 2026-10-26 | 0.7 | not re-verified by V11 |
| CLAIM-aas-05 | pattern comparison | trade-off table and hybrid recommendation | Reasoned inference | n/a | 2026-10-26 | 0.5 | needs POC (J5) |
