# ADR-KG3-09: Agent Memory as a Governed Epistemic Type

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-09 |
| Gap | GAP-34 (`07-GAP-REGISTER.md`, forced P0, High severity) |
| Capability | CAP-57 (Agent memory: write, expire, invalidate) |

## Context

`memory_eng/engine.py`, `reasoning/memory.py` and `agents/memory.py` implement agent memory with no ACL principal set, no tenant scope, no evidence pointer and no validity window on any memory record. This is not a unique EOIP defect — the same structural gap was found across every agent-memory competitor researched (C08-cognee, C08-mem0, C08-graphiti-zep, C08-letta all show the same absence) — but shared industry practice does not make it acceptable here, because Master Prompt §4.3 item 8 ("permissions survive everything... retrieval, summarization, traversal, caching, memory") names memory explicitly. The root cause is architectural: memory was built as a cache of conversation state, not as a governed knowledge type, so it never inherited the ACL/tenant/evidence model the rest of the graph has (BL-17, BL-19, BL-20). This card depends directly on GAP-07 (epistemic planes) landing first, because the fix treats memory records as first-class epistemic objects with the same observed/inferred/predicted distinction already being built for graph facts.

## Options considered

1. **Quick integration** — add ACL-principal, tenant-scope, evidence-pointer and validity-window fields to the existing memory schema, retrofitted onto today's record shape.
2. **Pragmatic native enhancement** — route memory writes through the same mutation gateway and promotion workflow as graph facts (propose-not-write), so a memory write is subject to the same epistemic-state and tenant-stamp gates as any other mutation; this directly echoes the risk Letta's own research names for autonomous "dreaming" subagents that write to long-term memory without review (C08-letta INV-letta-01).
3. **Long-term** — memory becomes a queryable view over the governed graph rather than a separate store, eliminating the schema-drift risk of maintaining two parallel models (graph facts and memory records) that are supposed to obey the same rules but are implemented twice.

## Options rejected and why

Treating option 1 as sufficient on its own is rejected: adding the fields without routing writes through the same gateway as graph facts (option 2) reproduces exactly the GAP-02/GAP-07 failure pattern — a mechanism that exists but is optional, bypassable by any memory-writing code path that does not call the new validation. The fields must be enforced at write time by the same gate, not merely available to a well-behaved caller.

## Decision

Adopt option 1 immediately as the schema change, paired with option 2 as the enforcement mechanism (not sequenced after it) — memory writes go through the existing mutation gateway so the ACL/tenant/evidence/validity fields are populated and checked the same way a graph-fact write is. Option 3 (memory as a view over the graph) is tracked as a research direction, contingent on GAP-07's epistemic-plane work maturing enough that treating memory as "just another plane" is actually simpler than maintaining a separate store.

## Consequences

**Positive:** closes a High-severity forced P0 (score 3.45). Extends the GAP-02/GAP-03 revocation guarantee (consistency tokens, BM-04/BM-05) to memory specifically — a revoked user's prior memory becomes inaccessible immediately rather than persisting as a stale, still-readable cache entry. No researched agent-memory competitor enforces ACL/tenant/evidence on memory; doing so correctly, with a passing benchmark, is named in the self-inversion card itself as "a genuine and currently unclaimed differentiator."

**Negative:** depends on GAP-02 and GAP-07 landing first (an explicit dependency in the card) — this is not independently shippable ahead of those two ADRs. Stale memories remain a named risk even after the fix (a memory record with an expired validity window that is not actively purged still occupies storage and must be handled by a retention policy, not just a flag).

## Reversibility

Medium. The schema addition (option 1) is additive and low-risk to add or remove. Routing memory writes through the shared mutation gateway (option 2) is a behavioural change to every agent that writes memory — reverting it after agents have come to depend on the gateway's validation (e.g., rejecting a write that lacks a tenant scope) would silently reopen the exact gap this ADR closes.
