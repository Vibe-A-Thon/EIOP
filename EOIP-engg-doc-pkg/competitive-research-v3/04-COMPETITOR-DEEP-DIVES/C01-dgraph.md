# C01 — Dgraph

| Field | Value |
|---|---|
| Registry ID | T-C01-dgraph |
| Tier | B — GraphQL-native distributed graph; ownership changed twice; licence picture inconsistent |
| Versions examined | v25.5.1 (2026-10-22, latest), v25.5.0 (2026-10-13), v25.4.1 (2026-08-24), v25.4.0 (2026-07-30) |
| Verified on | 2026-10-26 (actual access date; brief says 2026-10-18) |
| Worker | V15 (W07 scope) |

## 1. Identity, current status, tier, and sources
Dgraph (github.com/dgraph-io/dgraph, Go). Owners: Dgraph Labs, then Hypermode (acquired 2024), then Istari Digital (announced 2025-10-23, terms undisclosed; Istari says it will keep supporting the open-source community) [CLAIM-dgraph-01]. Status: active; releases roughly every 2-8 weeks, last push 2026-10-23, Apache-2.0 per GitHub SPDX, 21.8k stars [CLAIM-dgraph-02]. Release authors are a small group (matthewmcneely, shiva-istari) -> small-team bus factor (inference). Licence conflict: v25 preview notes say the full codebase is Apache-2.0; official licence pages (v24.1, v25.x) still say enterprise features are proprietary under the Dgraph Community License with a 30-day trial [CLAIM-dgraph-03]. Unresolved here: LICENSE file text not read. Sources: GitHub repo/releases/API, Istari press release, Dgraph licence docs, Hypermode v25 preview.

## 2. Primary problem, target workloads, example workflows
Horizontally scalable graph store with a native GraphQL API plus DQL, for app backends and AI-native relationship workloads [CLAIM-dgraph-01]. EOIP-relevant: (a) a GraphQL-served "service catalogue" graph for UI clients; (b) predicate-sharded storage for a single large tenant. Poor fit as a governed multi-source KG core (no ontology/SHACL layer found).

## 3. Feature inventory
| Feature | Status |
|---|---|
| GraphQL API generated from schema | Present (documented, README) |
| DQL (own query language), RDF import | Present |
| Namespaces (multi-tenancy), MCP server, v2 APIs | Present in v25 preview (docs) [CLAIM-dgraph-03] |
| ACL / native authn-authz | "Upcoming preview" in v25 notes; formerly enterprise |
| Backups, encryption at rest, audit | Historically enterprise-only; current gating UNVERIFIED |
| Vector search | UNVERIFIED this session |
| Cypher / Gremlin / SPARQL / GQL | Absent (not found) |
| UI (Ratel), CLI, Go/Java/JS/Python clients | Present / partial (clients maintained by team per README) |

## 4. Architecture diagram
```
Client -> Alpha (GraphQL/DQL/gRPC) --Raft group(s)--> Badger KV (predicate shards)
              ^                                      
Zero (cluster membership, shard assignment, timestamps, txn oracle)
```

## 5. Under-the-hood reconstruction
Hypotheses from prior knowledge, NOT verified this session (confidence 0.5): data stored as RDF-like triples sharded by predicate (whole predicate lives in one group); posting lists in Badger (LSM); Zero hands out start/commit timestamps (snapshot isolation, MVCC); Raft per Alpha group; multi-hop queries fan out per predicate across groups. Verified: v25.4.0 notes show Zero admin endpoints were unauthenticated until a `--security` superflag was added [CLAIM-dgraph-04]; v25.4.0-preview1 ships a "mutation pipeline" flag (documented in release notes).

## 6. Requirements inferred
FR: schema-first typing, GraphQL generation, namespaces. NFR: horizontal scale, ACID per cluster, secure-by-default admin plane (the v25.4 fix implies it was not).

## 7. Performance and resource model
No independent benchmark read; none quoted. Predicate sharding implies hot-predicate and cross-group join cost (hypothesis). Failure modes: Zero as control-plane dependency.

## 8. Strengths
Schema-to-GraphQL generation; unrestricted multi-instance clustering if Apache-2.0 holds; active CVE/dependency patching in 2026 [CLAIM-dgraph-05]. Match via a thin GraphQL facade over BL-01 (BL-58 absent).

## 9. Limitations
Verified: unauthenticated Zero admin endpoints until v25.4.0 [CLAIM-dgraph-04]. Licensing: Apache-2.0 vs Community-License inconsistency; two ownership changes in two years [CLAIM-dgraph-01, -03]. Algorithmic: custom DQL, no standards query language (inference). Friction: GraphQL-first model is awkward for ontology-rich KGs.

## 10. Deployment, licensing, viability
Self-hosted binary/Docker/Kubernetes; air-gap viable. Legal-review trigger: confirm whether enterprise code ships in the Apache build, and Istari's intentions. Not a candidate to bundle until resolved.

## 11. Competitive delta vs baseline
BL-58 (GraphQL API absent): Dgraph shows schema-derived GraphQL. BL-01/BL-05: Dgraph not a GraphStore backend today; BL-20 tenancy: namespaces comparable in intent. BL-59: no SQL/PGQ, no gain.

## 12. Strength and inversion cards
STR-dgraph-01 | Dgraph | schema-derived GraphQL API | CLAIM-dgraph-01 | typed API for front-ends | match | generate GraphQL from the ontology registry, tenant-scoped | introspection round-trip test.
INV-dgraph-01 | target Dgraph v25.x; any workload | ownership churn plus ambiguous licence is a procurement risk | CLAIM-dgraph-01/-03 | licensing/governance, proven | alternative: treat engines as replaceable adapters behind BL-01 (worse when adapter semantic loss is high) | options: (1) skip, (2) experimental adapter, (3) conformance-gated adapter | select (1)/(2) | POC: pass `graph/conformance.py` on 3-node cluster, success = 100% core ops | migration: export RDF | defensibility: backend neutrality persists | decision DEFER. Seed hypotheses in Master Prompt §10.5 for Dgraph: none found.

## 13. Per-capability decisions
CAP-17 GraphQL API: EXPERIMENT (own facade, not Dgraph). CAP-05 scale-out: DEFER. CAP-47 tenancy: REFERENCE only. Backend adapter: DEFER pending licence clarification.

## 14. Tests and acceptance
Read LICENSE at pinned tag; diff enterprise-code paths; run conformance suite; check Zero endpoint auth under default config.

## 15. Risks and open questions
Is ACL now free? Vector support level? Istari roadmap? Maintainer depth?

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Identity, ownership, licence |
| D2 | 2 | GraphQL-native workloads |
| D3 | 4 | Alpha/Zero |
| D4 | 5 | Hypothesis: Badger, predicate shards |
| D5 | 3 | Schema-first; no ontology |
| D6 | 3, 9 | DQL/GraphQL; planner N/A unverified |
| D7 | N/A | No reasoning found |
| D8 | 5 | Hypothesis: Raft, Zero oracle |
| D9 | 3 | RDF import; connectors N/A |
| D10 | N/A | None found |
| D11 | N/A | None found |
| D12 | N/A | None found |
| D13 | 3 | MCP server (preview) |
| D14 | N/A | Not found |
| D15 | N/A | Not found |
| D16 | 3 | Ratel UI |
| D17 | 3 | Clients |
| D18 | 9 | Zero admin auth fix |
| D19 | 3 | Namespaces |
| D20 | 7 | No numbers |
| D21 | 10 | Licence ambiguity |
| D22 | 11 | RDF in; no standard QL |
| D23 | N/A | Not researched |
| D24 | App. C | Confidence per claim |

## Appendix B — Capability mapping
| CAP | Dgraph | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-17 | native | -01 | BL-58 absent | EXPERIMENT | P2 |
| CAP-47 | partial (namespaces) | -03 | BL-20 partial | REFERENCE | P3 |
| CAP-05 | native | -01 | BL-01 | DEFER | P3 |
| CAP-45 | partial/unknown | -03 | BL-19 | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM-ID | Product/date | Claim | Class | Source | Access | Conf | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-dgraph-01 | 2025-10-23 | Istari Digital acquired Dgraph from Hypermode (which bought Dgraph Labs in 2024); will support OSS community; terms undisclosed | Third-party report/press release | istaridigital.com/resources/istari-acquires-dgraph ; fenwick.com | 2026-10-26 | 0.8 | none |
| CLAIM-dgraph-02 | v25.5.1, 2026-10-22 | Latest release; Apache-2.0; 21.8k stars; push 2026-10-23 | Officially documented | github.com/dgraph-io/dgraph (+API) | 2026-10-26 | 0.9 | none |
| CLAIM-dgraph-03 | v25 / v24.1 docs | v25 preview: whole codebase Apache-2.0, namespaces/MCP; licence docs: enterprise features under Dgraph Community License, 30-day trial | Officially documented (via search snippet + fetch) | docs.hypermode.com/dgraph/v25-preview ; docs.dgraph.io/installation/configuration/license | 2026-10-26 | 0.6 | the two sources conflict |
| CLAIM-dgraph-04 | v25.4.0 | Zero admin endpoints previously unauthenticated; `--security` superflag added | Officially documented | GitHub releases | 2026-10-26 | 0.7 | none |
| CLAIM-dgraph-05 | v25.5.1 | Release clears CVE-scan findings, Go update | Officially documented | GitHub releases | 2026-10-26 | 0.7 | none |

## Appendix D — Assumptions
Release page dates read as 2026 (API confirmed 2026-10-22/10-13). Architecture in section 5 is prior knowledge, flagged. GitHub API rate limit prevented commit-level checks.
