# C01 — GraphScope / GraphScope Flex

| Field | Value |
|---|---|
| Registry ID | T-C01-graphscope |
| Tier | B — modular graph computing stack (cross-ref C12 TinkerPop, C11 PyG); LDBC SNB audited |
| Versions examined | GitHub "latest" release v0.31.0 (2025-01-27); FDR used Flex 0.31.3 (2025-04-21); repo push 2026-09-23 |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V15 (W07 scope) |

## 1. Identity, current status, tier, and sources
Alibaba open-source "one-stop" graph system: GRAPE (analytics), GIE (interactive queries; GAIA/Hiactor, GOpt optimizer), Graph-Learn (GNN), Vineyard (in-memory data exchange); Flex = modular "LEGO-like" redesign (SIGMOD 2024 industry track) with products Interactive (single-node OLTP-style), Groot (distributed store), gsctl CLI, Portal web UI [CLAIM-graphscope-01, -02]. Licence Apache-2.0 [CLAIM-graphscope-01]. Status: repo pushed 2026-09-23 but the last GitHub-tagged release is 2025-01-27 (about 21 months); the project blog in 2026 focuses on a new embedded engine "NeuG" (open-sourced 2026-02-11, v0.1.3 2026-07-02), site still titled GraphScope [CLAIM-graphscope-04]. Whether NeuG replaces Flex is not stated (inference only). Sources: repo, releases, LDBC FDR, graphscope.io docs/blog.

## 2. Primary problem and workloads
Large-graph analytics, interactive Cypher/Gremlin queries, GNN training in one Python-driven stack; Flex lets users assemble only needed components. EOIP-relevant: LDBC-audited single-node Cypher engine as a possible analytical sidecar; GOpt as optimizer reference (CAP-18).

## 3. Feature inventory
| Feature | Status |
|---|---|
| Cypher (ad-hoc since v0.29.0; OPTIONAL MATCH, UNWIND, TRAIL), Gremlin | Present [CLAIM-graphscope-02] |
| GQL | Partial/frontend claimed in slides only (UNVERIFIED) |
| Stored procedures (C++), ad-hoc queries | Present |
| NL-to-Cypher via OpenAI-compatible API | Present (v0.25.0 notes) |
| Portal web UI (modeling, import, query), gsctl, Java/Python SDKs | Present (v0.28-0.30) |
| Bulk load (incl. ODPS) | Present |
| Distributed Groot store, secondary read-only instances | Present |
| Auth/RBAC, tenancy, encryption | UNVERIFIED / not found |
| Vector search | Not found |
| SPARQL, SQL/PGQ, ontology | Absent |

## 4. Architecture diagram
```
Client (Python/gsctl/Portal) -> Coordinator
   Interactive (Flex): Cypher -> GOpt compile -> C++ stored proc -> embedded graph store
   Groot (distributed): GIE frontend -> compute workers <-> RocksDB-style stores + Kafka-style log (hypothesis)
   GRAPE analytics <-> Vineyard shared memory <-> Graph-Learn
```

## 5. Under-the-hood reconstruction
Verified: declarative Cypher is compiled at runtime by an in-house compiler; ACID tests for serializable isolation were audited for the Interactive run [CLAIM-graphscope-03]; GOpt integrated v0.28.0; RelGo ports GOpt into DuckDB (blog, SIGMOD 2025). Hypotheses (0.4): CSR-style in-memory storage, MVCC with single-writer batching in Interactive; Groot is a log-based distributed store. Concurrency/partitioning in Groot not verified.

## 6. Requirements inferred
Compile-to-native query path, schema-first typing, composable deployment (Docker/K8s), declarative benchmark conformance (LDBC).

## 7. Performance and resource model
Vendor claims, audited by LDBC: Flex Interactive on SF30/100/300, single instance, Cypher, FDR 2025-04-21 [CLAIM-graphscope-03]; blog says ">80,000 QPS" while docs cite 33,180.87 ops/s — unreconciled; hardware/dataset detail not read, so no numbers adopted. Failure mode: stored-procedure compile latency for new queries (inference).

## 8. Strengths
LDBC-audited performance; GOpt optimizer; modular packaging; Apache-2.0. Match optimizer ideas via cost-based plan hints in BL-08 executor; benchmark with LDBC.

## 9. Limitations
Release cadence stalled on GitHub since Jan 2025 (verified); strategy shift toward NeuG ambiguous; heavy C++/K8s stack; Chinese-ecosystem docs/ODPS bias; no ontology, RDF, governance, tenancy found; 426 open issues (repo page).

## 10. Deployment, licensing, viability
Apache-2.0, self-hosted Docker/K8s/pip, air-gap viable. No copyleft found; third-party libraries differ (README). Redistribution fine subject to dependency audit. Embedded NeuG licence not read.

## 11. Competitive delta vs baseline
BL-01 (GraphStore protocol) lacks any Cypher-compiled analytical engine; BL-43 algorithms are in-process Python, GRAPE offers distributed equivalents; BL-59 absent. EOIP does not need a new store.

## 12. Strength and inversion cards
STR-graphscope-01 | GraphScope | GOpt cost-based cross-engine optimizer | CLAIM-graphscope-02 | faster multi-hop J-queries | exceed | rule/cost pass on BL-08 plans | LDBC-style multi-hop set, p95 vs baseline.
STR-graphscope-02 | GraphScope Flex | audited serializable Cypher engine | CLAIM-graphscope-03 | credible benchmark | integrate (optional) | read-replica sidecar | FDR-style audit rerun.
INV-graphscope-01 | GraphScope Flex v0.31.x | no tagged release since 2025-01 while a new engine is promoted | maturity/governance, proven for cadence, hypothesis for cause | pinning an adapter to repo `main` is risky; alternative: integrate only via Cypher/Bolt-like protocol, worse if semantics diverge | options: skip / conformance adapter / own CSR engine | choose skip, watch NeuG | POC: BL-07 suite on Interactive, 100% core ops | defensibility: backend neutrality | decision DEFER. Seed hypotheses: none.

## 13. Per-capability decisions
CAP-18 optimizer: REUSE ideas (papers). CAP-14 Cypher: INTEGRATE only if conformance passes (DEFER). CAP-62 algorithms: EXPERIMENT GRAPE. CAP-63/64: DEFER.

## 14. Tests and acceptance
Run Interactive in Docker offline; load 1M-edge tenant graph; run BL-07 conformance; measure ad-hoc Cypher compile latency.

## 15. Risks and open questions
Flex vs NeuG future? Tenant isolation? Memory per million edges? Licence of NeuG?

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1, 10 | Alibaba, Apache-2.0, stalled tags |
| D2 | 2 | Analytics+interactive+GNN |
| D3 | 4 | Coordinator/Interactive/Groot |
| D4 | 5 | Hypothesis CSR |
| D5 | 3 | Schema-first; no ontology |
| D6 | 5 | GOpt, runtime compile |
| D7 | N/A | None |
| D8 | 5, 7 | Serializable audited |
| D9 | 3 | Bulk load only |
| D10 | N/A | None |
| D11 | N/A | None found |
| D12 | 3 | GRAPE, Graph-Learn |
| D13 | 3 | NL-to-Cypher only |
| D14 | 3 | OpenAI-compatible NL2Cypher |
| D15 | N/A | None |
| D16 | 3 | Portal |
| D17 | 3 | SDKs, gsctl |
| D18 | 9 | Not found |
| D19 | N/A | Not found |
| D20 | 7 | Unreconciled vendor numbers |
| D21 | 10 | Apache-2.0 |
| D22 | 11 | Cypher/Gremlin |
| D23 | N/A | Not researched |
| D24 | App. C | Confidence per claim |

## Appendix B — Capability mapping
| CAP | GraphScope | Claim | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-14 | native | -02 | BL-08/09 | DEFER | P3 |
| CAP-18 | native | -02 | BL-08 | REUSE ideas | P2 |
| CAP-62 | native | -01 | BL-43 | EXPERIMENT | P3 |
| CAP-64 | native | -01 | BL-44 | DEFER | P3 |
| CAP-05 | native (Groot) | -02 | BL-01 | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM-ID | Product/date | Claim | Class | Source | Access | Conf | Contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-graphscope-01 | repo | Apache-2.0; components GRAPE/MaxGraph/Graph-Learn/Vineyard; Flex described as modular successor; 3.6k stars | Officially documented | github.com/alibaba/GraphScope | 2026-10-26 | 0.85 | none |
| CLAIM-graphscope-02 | v0.25-0.31 | Release notes: Interactive, GOpt (0.28), ad-hoc Cypher (0.29), Portal, gsctl, Groot Cypher/Gremlin HTTP (0.30-0.31), NL2Cypher (0.25) | Officially documented | github.com/alibaba/GraphScope/releases | 2026-10-26 | 0.8 | none |
| CLAIM-graphscope-03 | Flex 0.31.3, 2025-04-21 | LDBC SNB Interactive FDR on SF30/100/300, single instance, declarative Cypher, serializable ACID tests audited | Independent benchmark (audited) | ldbcouncil.org LDBC_SNB_I_20250421_SF30-100-300_graphscope.pdf | 2026-10-26 | 0.8 | blog 80k QPS vs docs 33,180.87 ops/s |
| CLAIM-graphscope-04 | latest release 2025-01-27; blog 2026 | Latest GitHub release v0.31.0 on 2025-01-27 (API); push 2026-09-23; 2026 blog dominated by NeuG (embedded graph DB, open-sourced 2026-02-11) | Officially documented | GitHub API; graphscope.io/blog | 2026-10-26 | 0.8 | relation to Flex not stated |

## Appendix D — Assumptions
Tags after v0.31.0 may exist (FDR cites 0.31.3); only GitHub "latest release" and blog were checked. Storage internals are hypotheses.
