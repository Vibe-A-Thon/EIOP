# ADR-KG3-01: Source-ACL Enforcement as a Mandatory Pipeline Stage

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic — see `10-TARGET-REFERENCE-ARCHITECTURE.md` header note on required overwrite) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-01 |
| Gap | GAP-02 (`07-GAP-REGISTER.md`, forced P0, Critical severity) |
| Capability | CAP-46 (ReBAC / source-ACL enforcement in retrieval and answers) |

## Context

`07-GAP-REGISTER.md` GAP-02 and `01a-BASELINE-DELTA-HEAD.md` BL-18 establish, by code reading, that source-ACL enforcement exists as a library call but is not applied on any deployed path. `authz/pdp.py` (`can_read`, tenant/policy-epoch/classification/ACL-intersection, deny-by-default) and `authz/derivation_acl.py` (`filter_graph_contexts`, derivation-aware ACL composition for inferred facts — this is the existing INV-01/NB-17 mechanism) are real and tested. But `retrieval/service.py` calls this filter only inside the graph-traversal branch of `retrieve(...)`, and only when a `scope` argument is supplied. No deployed caller supplies it: `apps/api/extended.py:906-913` passes tenant-ownership `allow` but not `scope`; `apps/api/main.py:1770` (`/api/v1/rag`) passes neither; `agents/governed.py:250` passes neither; the MCP surface forwards to REST and inherits the gap. The keyword, vector and hybrid retrieval branches filter candidates by tenant ownership only — never by source ACL or classification. This means two users with different source permissions asking the same question through any shipped surface get answers filtered by tenant, not by what they are each individually permitted to see — a direct violation of Master Prompt §4.3 item 8 ("permissions survive everything") and of acceptance journey J5.

## Options considered

1. **Quick integration** — make the existing `scope`/ACL filter a mandatory, non-optional parameter of `retrieve()`, closing the one known branch.
2. **Pragmatic native enhancement** — propagate ACL principals through every candidate-generation stage (keyword, vector, hybrid, graph), not just the graph branch, plus a delivery-time re-check and a consistency token keyed to the tenant's policy epoch so a permission revocation invalidates previously computed results without a full re-index.
3. **Long-term differentiated architecture** — ACL-embedded indexes, following the pattern already proven by Onyx (per-chunk ACL principal strings filtered at query time, STR-onyx-01) and OpenSearch document-level security (STR-opensearch-01), with Zanzibar-style consistency tokens (STR-rebac-01) as the revocation mechanism, so the ACL check is a property of the index itself rather than a post-hoc filter.

## Options rejected and why

Option 1 alone is rejected as the final design (though it is the correct first step) because it leaves the keyword/vector/hybrid stages — which are the default path for most queries — filtering by tenant only. A user who loses access to a specific Confluence space but keeps tenant membership would still see that space's content through keyword or vector search. Doing only option 1 would pass a graph-only test of J5 while failing it on every other retrieval mode, which is not a defensible claim.

## Decision

Adopt option 2 immediately as the shipped architecture, with option 3 (ACL-embedded VectorPort adapters per STR-onyx-01/STR-opensearch-01/STR-pgvector-01) as the target once CAP-53's VectorPort exists (GAP-46; these two gaps share infrastructure). Concretely: every fact, chunk and edge carries a resolved ACL-principal set at write time (extending the `PermissionMetadata`/`acl_hash` already captured at ingest, BL-17); every retrieval stage — not only the graph branch — pre-filters candidates by the caller's resolved principal set before ranking; a final check runs at delivery time as a defence-in-depth measure; a consistency token tied to the tenant's policy epoch is checked on every read so a revocation is honored without waiting for a background re-index or cache expiry (STR-rebac-01, "exceed" target, not merely "match").

## Consequences

**Positive:** closes the platform's most severe forced-P0 gap (GAP-02, Critical, score 3.55, the top-priority forced item after the licence/vault/model/MCP quartet). Makes J5 (permission-aware GraphRAG) actually testable rather than selectively testable. Gives the platform a defensible, benchmarked claim ("zero leaked facts under BM-04") that the cohort research (`12-SECURITY-POLICY-COHORT.md`) found most competitors do not test or document at all.

**Negative:** every retrieval stage must be touched, not just one function signature — this is L-effort (per CAP-46's effort estimate), not a one-line fix. ACL pre-filtering at the candidate-generation stage, before ranking, risks reducing recall if the filter is applied too aggressively (e.g. filtering before expansion rather than after) — BM-04 must measure this trade-off, not assume it away.

## Reversibility

High at the interface level (AuthzPort is additive to existing call sites) but the propagation into every retrieval stage is not something to half-revert once the consistency-token scheme is live, since rolling back would silently reopen the leak it closed. Any rollback must be accompanied by re-running BM-04 to confirm the regression is intentional and documented, not accidental.
