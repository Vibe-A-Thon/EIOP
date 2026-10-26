# C19 — ReBAC engines: OpenFGA, SpiceDB, Permify (Zanzibar family)

| Field | Value |
|---|---|
| Registry ID | T-C19-rebac |
| Tier | B (permission-aware retrieval, BL-18 P0) |
| Versions examined | OpenFGA v1.22.0 (6 Oct), SpiceDB v1.57.0 (20 Oct), Permify v1.7.5 (9 Oct); years not shown on pages, 2026 inferred |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
| Member | Owner / governance | Licence | Status |
|---|---|---|---|
| OpenFGA | Originated at Auth0/Okta; **CNCF Incubating** (moved 2025-10-28; sandbox 2022) | Apache-2.0 | active, Go, 6.0k stars [CLAIM-rebac-02] |
| SpiceDB | AuthZed (company-led; `authzed/spicedb`) | Apache-2.0 | active, Go, 7.2k stars [CLAIM-rebac-03] |
| Permify | Permify, **acquired by FusionAuth (Nov 2025)** | **AGPL-3.0** (Community Edition) | active, last release 9 Oct [CLAIM-rebac-04] |
Reference: Google Zanzibar paper (USENIX ATC 2019) [CLAIM-rebac-01]. Permify's AGPL-3.0 is a legal-review trigger for embedding/redistribution; FusionAuth says it stays open source (secondary report, 0.5). Cedar/Cerbos are separate (C19-cedar-cerbos).

## 2. Problem and workflows
"Can subject S do P on object O?" over a relationship graph (folder->document, group->member, org->team). Workflow for EOIP: connector ingests source ACL (BL-17) -> writes tuples `document:42#viewer@group:finance#member` via a governed sync, never directly from the connector into the graph (BL-23 rule applies by analogy) -> retrieval asks the engine which candidate IDs the caller can see.

## 3. Feature inventory
| Capability | OpenFGA | SpiceDB | Permify |
|---|---|---|---|
| Check | present | present | present |
| Expand (userset tree) | present [CLAIM-rebac-05] | present | present (UNVERIFIED detail) |
| List objects / lookup resources | ListObjects: default deadline 3 s, max 1000 [CLAIM-rebac-05] | LookupResources: default limit 1000; lr3 and query-plan engine experimental [CLAIM-rebac-06] | lookup-entity API UNVERIFIED |
| List users / lookup subjects | ListUsers | LookupSubjects | UNVERIFIED |
| Consistency tokens | not documented on pages read (UNVERIFIED, 0.4) | **ZedToken** with 4 modes [CLAIM-rebac-07] | snap tokens UNVERIFIED |
| Watch / change stream | UNVERIFIED | present; defaults 1024-entry buffer, 1 s heartbeat [CLAIM-rebac-06] | UNVERIFIED |
| ABAC conditions | conditions (UNVERIFIED detail) | caveats (4096-byte context cap) | rules |
| Stores | in-memory (dev), PostgreSQL 14+, MySQL 8, SQLite (beta) | PostgreSQL, MySQL, CockroachDB, Spanner, memdb | NOT VERIFIED |

## 4. Architecture
```
Source ACL --sync--> [tuple writer] --> Datastore (PG/MySQL/...)  <== revision/timestamp per write
Retrieval --Check/Lookup(token)--> [authz server: schema + dispatcher + cache] --reads at snapshot--> Datastore
Watch stream --> optional denormalised index (Leopard-like) / search ACL fields
```

## 5. Under-the-hood reconstruction (Zanzibar model)
- Data model: relation tuples `object#relation@user` or `@userset(object#relation)`; namespace configuration defines relations with **userset rewrites**: `computed_userset`, `tuple_to_userset` (parent folder), union/intersection/exclusion [CLAIM-rebac-01]. SpiceDB/OpenFGA express this in schema DSLs.
- **Check**: evaluates a userset expression by recursively dispatching sub-checks; results cached; delegated by consistent hashing so callers/callees share caches [CLAIM-rebac-01]. **Expand**: returns a userset tree (leaves = users/usersets; internal = union/intersect/exclude); Google clients use it to build ACL-aware search indexes [CLAIM-rebac-01]. **Read/Write/Watch**: tuple CRUD and ordered change stream.
- **Zookie / ZedToken**: opaque token encoding a global timestamp; a content write fetches a token via a content-change check, stored with the content; later checks pass it and are evaluated at a snapshot **at least as fresh**, solving the *new enemy problem* (revoked user seeing new content) [CLAIM-rebac-01, -07]. SpiceDB modes: `minimize_latency`, `at_least_as_fresh`, `at_exact_snapshot` (can fail "Snapshot Expired" after GC), `fully_consistent` (bypasses cache); default fully_consistent for writes/schema, minimize_latency otherwise [CLAIM-rebac-07].
- **Leopard** (Google): precomputed set index of (type, set id, element id) tuples for deeply nested groups, offline build plus incremental layer fed by Watch; one tuple change can yield tens of thousands of index events [CLAIM-rebac-01].
- Pre-filtering retrieval, two patterns: (a) **candidate check**: ANN/BM25 returns top-K*overfetch, `BulkCheck` filters, loop until K survivors (cost grows with deny ratio; leaks nothing); (b) **lookup**: `LookupResources`/`ListObjects` returns allowed IDs, pushed as an ID filter or intersected with candidates (breaks when allowed sets exceed the 1000-result defaults [CLAIM-rebac-05/06]; raise limits or stream). A third pattern, (c) denormalise principals into index documents via Watch (Onyx STR-onyx-01, OpenSearch DLS STR-opensearch-01), gives engine-enforced filtering at query time but inherits staleness: bound by recording the token used at index time (hypothesis).
- Caching/consistency: snapshot-timestamp quantised cache keys (1-10 s) in Zanzibar [CLAIM-rebac-01]. Security: tenant prefix on object ids or separate store per tenant (OpenFGA store concept; UNVERIFIED detail).

## 6. Requirements inferred
FR: deny-by-default, nesting, parent inheritance, revocation visible via token. NFR: low-ms Check, streaming lookup, token in cache keys, per-tenant keyspace.

## 7. Performance and resource model
Zanzibar (Google, Spanner, tens of datacentres): >2 trillion tuples (~100 TB), >10 M client QPS, Check "safe" p50/p95/p99/p99.9 about 3/11/20/93 ms, availability >99.999% over 3 years [CLAIM-rebac-01]. These are Google-scale and not transferable. Open-source engines: **no independent benchmark fetched; vendor figures not collected: UNVERIFIED**. Single-node footprint: Go binaries + PostgreSQL/SQLite; sizes NOT PUBLICLY VERIFIED here. Failure modes: deep recursion (SpiceDB max dispatch depth 50), 1000-limit truncation, snapshot expiry.

## 8. Strengths
Native inheritance/groups; consistency semantics prevent stale-grant leaks; reverse queries; Apache-2.0 engines; OpenFGA under CNCF.

## 9. Limitations
Algorithmic: lookups over huge allowed sets truncate or slow. Operational: second stateful service plus tuple sync; Materialize is managed [CLAIM-rebac-06]. Friction: modelling source ACLs (Confluence/Jira/SharePoint), sync lag. Licence: Permify AGPL-3.0; SpiceDB enterprise features UNVERIFIED.

## 10. Deployment and licensing
OpenFGA and SpiceDB: Apache-2.0, containers, air-gap viable, run on PG/SQLite-class stores (one-node friendly). Permify: AGPL-3.0, acquired by FusionAuth - REJECT as embedded dependency pending legal review. No mandatory cloud.

## 11. Delta vs EOIP baseline
BL-18 (source-ACL enforcement absent in baseline): in the working tree (HEAD 896e06d, later than baseline ad9937b) `retrieval/service.py:575` filters graph contexts through `DerivationACLEvaluator`, and `authz/pdp.py` has deny-by-default `can_read` over `acl_vector` tags, tenant check, and `PolicyEpochRegistry`. I did **not** audit whether lexical/vector candidate stages are ACL-filtered; treat BL-18 as **partial, re-audit required**. EOIP flat ACL tags have no group nesting/inheritance and no Expand. `policy_epoch` is a coarse per-tenant zookie analogue that fails closed (denies) when stale, instead of re-evaluating at a fresher snapshot. BL-20 tenancy remains contract-level. C09-mcp INV-mcp-02: single static bearer token means no principal reaches retrieval.

## 12. Cards
**STR-rebac-01** | SpiceDB/Zanzibar | consistency token (ZedToken) | CLAIM-01,07 | no stale-grant leaks after revocation | match | carry a per-tenant revision token on retrieval requests, cache keys include it | revoke then query: 0 forbidden hits.
**STR-rebac-02** | OpenFGA/SpiceDB | reverse lookup for pre-filtering | CLAIM-05,06 | permission-aware retrieval | integrate | pattern (a) default, (b) when allowed set <1000 | J5 leakage test, differential vs full check.
**STR-rebac-03** | Zanzibar | Expand/Leopard flattened sets | CLAIM-01 | nested groups at scale | experiment | flatten groups into index principals via Watch | index and Check agree on 10k docs.
**INV-rebac-01** (lookup truncation, proven by defaults) | Options: raise limits/stream; check-filter loop; Watch-fed principal index (selected: loop plus index hybrid). Benchmark: 100k docs, 10% visible, p95 added latency <=50 ms vs unfiltered (target hypothesis). Decision EXPERIMENT. Failure case: truncated lookup silently hides allowed docs; must report it.
**INV-rebac-02** (second stateful service vs one-node-first, deployment) | option: embedded native tuple store with same port, engine optional. Decision EXPERIMENT.
**INV-rebac-03** (Permify AGPL, licensing) | REJECT embedding; REFERENCE only.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-46 source-ACL/ReBAC engine | INTEGRATE OpenFGA or SpiceDB behind an `AuthzPort` (both Apache-2.0); EXPERIMENT which |
| Consistency token | BUILD in native pdp (generalise `policy_epoch`) |
| Native tuple model for one-node | EXPERIMENT |
| Permify | REJECT (AGPL) |

## 14. Tests
J5 (1,000 mixed-ACL docs: 0 forbidden results across search, GraphRAG, summaries, cache); revocation race with token; nesting depth 10; truncation reporting; air-gapped one node.

## 15. Risks
Source-ACL mapping errors and sync lag; token plumbing through caches; engine lock-in; benchmark gap.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1,D21 | 1,10 | owners, licences, AGPL flag |
| D2-D3 | 2,4 | permission-aware retrieval, server+datastore |
| D4-D8 | 5,7 | tuples, rewrites, Check/Lookup, snapshots, Leopard |
| D9-D10,D13 | 2,5,11 | ACL sync, pre-filter patterns |
| D18-D19 | 5,11 | auth, tenancy |
| D20,D24 | 7,C | Google-only figures; no OSS benchmark |
| D22 | 8 | schema DSL lock-in |
| Others | N/A | not applicable |

## Appendix B — Capabilities
| CAP | Native? | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-46 | native | 01,05,06 | BL-18 partial/re-audit | INTEGRATE | P0 |
| CAP-47 | partial | 05 | BL-20 Partial | EXPERIMENT | P0 |
| CAP-45 | partial | 06 | BL-19 | REUSE | P2 |
| CAP-53/55 | via filtering | - | BL-14,15 | INTEGRATE | P0 |

## Appendix C — Evidence
| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-rebac-01 | Zanzibar 2019 | zookies, Expand, Watch, Leopard, >2T tuples, >10M QPS, Check p50/95/99/99.9 ~3/11/20/93 ms, >99.999% | Peer-reviewed paper (read locally) | https://www.usenix.org/system/files/atc19-pang.pdf | 2019 / 2026-10-26 | 0.95 | Google-only scale |
| CLAIM-rebac-02 | OpenFGA | Apache-2.0, Go, datastores memory/PG14+/MySQL8/SQLite beta, CNCF incubating 2025-10-28 | Officially documented | https://github.com/openfga/openfga ; https://openfga.dev/project | 2025-10-28 / 2026-10-26 | 0.85 | sandbox date differs by source |
| CLAIM-rebac-03 | SpiceDB v1.57.0 | Apache-2.0; PG/MySQL/Cockroach/Spanner | Officially documented | https://github.com/authzed/spicedb | 20 Oct / 2026-10-26 | 0.85 | none |
| CLAIM-rebac-04 | Permify v1.7.5 | AGPL-3.0; acquired by FusionAuth Nov 2025 | Officially documented + secondary | https://github.com/Permify/permify ; https://permify.notion.site/Permify-Joins-FusionAuth-Community-FAQ-2b123f742ce58048aa72e107dad176b3 | 2025-11 / 2026-10-26 | 0.8 | none |
| CLAIM-rebac-05 | OpenFGA | Check, Expand, ListObjects (3 s, 1000), ListUsers, Read | Officially documented | https://openfga.dev/docs/interacting/relationship-queries | n/a / 2026-10-26 | 0.9 | consistency not stated there |
| CLAIM-rebac-06 | SpiceDB | LookupResources limit 1000, lr3 experimental, Watch defaults, dispatch depth 50, Materialize managed | Officially documented | https://authzed.com/docs/spicedb/concepts/commands | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-rebac-07 | SpiceDB | ZedToken modes and new-enemy problem | Officially documented | https://authzed.com/docs/spicedb/concepts/consistency | n/a / 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions
Release years inferred as 2026. OpenFGA/Permify consistency tokens, Permify lookup APIs, and OSS latency left UNVERIFIED rather than guessed. EOIP code read at working-tree HEAD, not baseline commit.
