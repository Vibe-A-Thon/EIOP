# ADR-KG3-02: Tenant Isolation as a Protocol-Level Guarantee

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-26 |
| Supersedes | The 2026-10-19 placeholder of this file (same path, different topic) |
| Based on | `09-CON-TO-PRO-INVERSION-REGISTER.md` INV-SELF-02 |
| Gap | GAP-03 (`07-GAP-REGISTER.md`, forced P0, Critical severity) |
| Capability | CAP-47 (Multi-tenant isolation) |

## Context

GAP-03 and BL-20 (`01a-BASELINE-DELTA-HEAD.md`) establish that `tenancy/layers.py` and `tenancy/isolation_hardened.py` genuinely isolate embedded vector indexes, search indexes, SQLite schemas, object prefixes, event topics, secrets, per-tenant AES-256-GCM data keys, caches, logs and backups — this is real, tested work, not a placeholder. The API layer wraps non-system-tenant graph access in a `NamedGraphStore` wrapper (`apps/api/main.py:680`). But `tenancy/isolation.py` defines tenant placement (SILO/BRIDGE/POOL) as a *contract*, explicitly documented as an "external gate" — and a grep for `tenant` across `graph/hugegraph.py`, `graph/neo4j.py`, `graph/neptune.py`, `graph/memory.py`, `graph/store.py`, `graph/rdf_backend.py` and `adapters/janusgraph.py` returns zero matches. No graph adapter has ever read a tenant context. A platform administrator without a tenant context gets global scope by default (`apps/api/extended.py:899-904`). This satisfies J13 (multi-tenant isolation) only for the embedded layers EOIP controls directly, not for the graph backends that hold the actual knowledge graph — the asset J13 cares most about.

## Options considered

1. **Quick integration** — add a tenant-id property and predicate to every query path, enforced at the `GraphStore` protocol boundary, for POOL and BRIDGE placement models (where tenants share infrastructure).
2. **Pragmatic native enhancement** — use each backend's own native isolation primitive, chosen per the existing `IsolationPlacement` contract: HugeGraph graph spaces (distributed deployments), Neo4j multi-database (Community or Enterprise), Neptune cluster-per-tenant (since Neptune has no sub-cluster multi-tenancy primitive).
3. **Long-term** — a tenant-aware `GraphStore` protocol that refuses any call without a resolved tenant context, backend-neutral, so "tenant-unaware" becomes structurally impossible rather than merely undocumented.

## Options rejected and why

A universal fix applied identically regardless of isolation model is rejected: for a SILO deployment (dedicated stack per tenant, which several customers will choose for compliance reasons) the operational convention of separate deployments is already sufficient isolation, and adding a data-plane tenant check on top is redundant overhead with no correctness benefit — the isolation boundary is the deployment itself. The fix must be conditional on the isolation model actually chosen, not a blanket requirement.

## Decision

Adopt option 2 immediately for POOL/BRIDGE deployments — per-backend native isolation units selected by the existing `IsolationPlacement` contract — with option 3 (a tenant-aware protocol that refuses unscoped calls) as the long-term target that closes the gap by construction rather than by adapter-by-adapter discipline. Option 1's universal predicate approach is folded into option 3 rather than shipped as a separate interim step, because a predicate bolted onto today's protocol without the refusal semantics of option 3 would be exactly the kind of "available if called" mechanism that GAP-02's sibling gap already shows is unreliable in practice.

## Consequences

**Positive:** closes a Critical-severity forced P0 (score 3.5). Gives EOIP a backend-neutral tenant-isolation claim, provable by the same BM-05 benchmark across HugeGraph, Neo4j and Neptune — something no single-backend competitor researched (FalkorDB's graph-per-tenant key, STR-falkordb-02; Weaviate's shard-per-tenant lifecycle, STR-weaviate-01; Amazon AGE's equivalent) can make across engines it does not itself support.

**Negative:** per-backend work is not uniform — HugeGraph graph spaces exist today but are not wired to tenant context; Neo4j Community lacks true multi-database isolation (an Enterprise-only feature in some versions, requiring licence verification before relying on it); Neptune's cluster-per-tenant unit is the costliest to operate at small tenant counts. "Noisy neighbour" and misconfiguration are named risks in the capability matrix (CAP-47) that BM-05 must specifically probe, not just adversarial query attempts.

## Reversibility

Medium. The `IsolationPlacement` contract already exists and is additive to adopt; what is costly to reverse is any customer deployment that has already been provisioned under one backend's native isolation unit (e.g., migrating a POOL deployment that used HugeGraph graph spaces to a per-cluster Neptune model requires a data migration, not a config change).
