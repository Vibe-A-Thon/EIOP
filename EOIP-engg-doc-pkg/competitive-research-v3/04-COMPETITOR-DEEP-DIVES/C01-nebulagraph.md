| Field | Value |
|---|---|
| Registry ID | T-C01-nebulagraph |
| Tier | B (distributed LPG reference; one-node-first and openCypher-subset angles) |
| Versions examined | v3.8.0 (tag/release 2024-05-17); default branch active, last push 2026-09-08 |
| Verified on | 2026-10-26 (brief says 2026-10-18; actual access date used) |
| Worker | V14 |

## 1. Identity, current status, tier, and sources
NebulaGraph is a distributed, Raft-replicated native property graph database from Vesoft Inc., Apache-2.0 on GitHub (`vesoft-inc/nebula`, ~12.4k stars) [CLAIM-nebula-01]. Latest tagged release is v3.8.0 (2024-05-17); no newer release is visible 17 months later although the default branch was pushed 2026-09-08, so cadence has slowed (maintenance-active, not fast-moving) [CLAIM-nebula-02]. A managed offering exists on AWS; whether a proprietary enterprise edition exists is NOT PUBLICLY VERIFIED from sources read. Tier B: reference for distributed LPG; peers already deep-dived: [C01-janusgraph](C01-janusgraph.md), [C01-tigergraph](C01-tigergraph.md), [C01-apache-hugegraph](C01-apache-hugegraph.md). Sources: GitHub README/tags/API, 3.8.0 architecture docs [CLAIM-nebula-03].

## 2. Primary problem, target workloads, example workflows
Billion-scale graphs needing horizontal scale-out with strong consistency and low-latency multi-hop reads (fraud, recommendation, knowledge graphs). Example: a KG of 10^9 edges sharded across storaged nodes; graphd runs a 3-hop expansion in parallel. For EOIP: not a single-node-first fit; relevant as an optional backend for very large tenants.

## 3. Feature inventory
| Feature | Status | Note |
|---|---|---|
| Native LPG, tagged vertices/edge types, typed schema | present | schema-first (tags/edge types); statements via nGQL |
| nGQL + openCypher-compatible subset | present/partial | README says "OpenCypher-compatible"; coverage level UNVERIFIED [CLAIM-nebula-01] |
| GQL (ISO 39075) | unknown | not claimed in sources read |
| Gremlin | absent | not offered natively (UNVERIFIED) |
| Raft replication, partitioned storage, storage/compute separation | present | [CLAIM-nebula-03] |
| RBAC | present | metad-managed users/privileges [CLAIM-nebula-03] |
| Operator/Kubernetes | present | Nebula Operator (third-party page) |
| Vector / full-text | unknown/partial | full-text via external Elasticsearch listener (UNVERIFIED) |
| Bitemporal/branching | absent | |

## 4. Architecture
```
 clients(nGQL/openCypher) -> graphd (stateless query: parse, plan, execute)
        graphd -> metad  (schema, users, partition map; Raft group)
        graphd -> storaged (partitions; each part = Raft group; RocksDB KV)
 control plane: metad       data plane: storaged (vertex/edge as KV pairs)
```

## 5. Under-the-hood reconstruction
Vertices and edges are stored as key-value pairs in RocksDB (default engine); partitions with the same ID across hosts form a Raft group for replication [CLAIM-nebula-03]. graphd is stateless, reads metadata from metad and pushes scans down to storaged. Edges are stored by source (out-edge) and mirrored for in-edges (HYPOTHESIS from the dual-edge design; verify in code `src/storage`). Transactions: per-partition Raft; cross-partition atomicity for edge pairs is via a TOSS mechanism (UNVERIFIED). Security is RBAC in metad; no row/label-level ACL known. Versioning: none native.

## 6. Requirements inferred
Schema-first typing; Raft-quorum writes; metad availability for DDL; minimum cluster of 3 for HA.

## 7. Performance and resource model
No benchmark verified here; vendor LDBC-SNB claims exist but were not read (UNVERIFIED). Expected scaling: reads scale with storaged nodes; fixed overhead of three services makes it heavy for one-node deployments. Failure modes: metad quorum loss blocks DDL; leader election pauses on partition loss.

## 8. Strengths
Distributed scale-out with strong consistency; permissive licence; storage/compute separation. Match approach: EOIP can offer Nebula as a scale-out adapter behind `GraphStore` rather than build sharding.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | none for core (Apache-2.0); enterprise features UNVERIFIED |
| Operational | three-service cluster; one-node deployment is oversized; release gap since 2024-05 |
| User friction | nGQL is non-standard; openCypher subset only; no Gremlin/SPARQL |
| Semantics | no RDF/OWL, no inference, no bitemporal |
| Root cause | KV-over-RocksDB design optimised for traversal, not axioms (hypothesis) |

## 10. Deployment, licensing, redistribution
Apache-2.0 core is redistribution-safe; patent grant included. Docker/Compose/Kubernetes supported (operator). Air-gap: yes (self-hosted, no phone-home known; UNVERIFIED). Legal review: confirm no proprietary enterprise-only modules required for RBAC/audit.

## 11. Competitive delta vs EOIP baseline
EOIP has no Nebula adapter (BL-01 lists HugeGraph, Neo4j, Neptune, Janus; BL-02..05) and conformance is live-unverified (BL-07). Nebula would add scale-out but not tenancy (BL-20 partial) or ACL enforcement (BL-18 absent).

## 12. Strength cards and inversion cards
- STR-nebula-01 | NebulaGraph | Raft-partitioned scale-out under Apache-2.0 | CLAIM-nebula-01,03 | large-tenant option | integrate | adapter via nGQL/openCypher over HTTP/bolt-like client | acceptance: `graph/conformance.py` suite passes on 3-node cluster.
- INV-nebula-01 | v3.8.0, small-tenant one-node | three services too heavy | hypothesis: cluster-first design (deployment) | alternative: keep embedded/LPG default and add Nebula only for scale tier; worse when tenant graph >single-node RAM | options: (a) document-only (b) adapter (c) shard-aware GraphStore router | selected: (b) | POC: conformance + 10^8-edge load on 3 nodes, success = p95 3-hop < agreed SLO, baseline Neo4j CE | security failure: tenant label filters must be injected by adapter | defensibility: backend neutrality | decision: DEFER.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-05 scale-out | INTEGRATE (optional adapter) |
| CAP-14 openCypher | EXPERIMENT (subset test) |
| CAP-47 tenant isolation | REJECT as a backend responsibility; stays in EOIP |
| CAP-35 branching | REJECT (absent) |

## 14. Tests / PoC
Run `conformance.py` against a 3-node docker-compose; verify nGQL tombstones (BL-25); load test; kill a storaged and measure recovery.

## 15. Risks and open questions
Release stall since 2024-05; enterprise split unknown; openCypher coverage unknown; whether GQL support arrives.

## Appendix A. Research-dimension coverage
| Dimension | Sections | Summary |
|---|---|---|
| D1-D4 identity, workload, features, architecture | 1-4 | covered |
| D5 data model/storage | 5 | LPG over RocksDB KV |
| D6 query | 3,5 | nGQL + openCypher subset |
| D7 reasoning | 9 | absent |
| D8 concurrency/consistency | 5 | Raft per partition |
| D9 scale/performance | 7 | no verified numbers |
| D10 versioning/temporal | 3 | absent |
| D11 security/tenancy | 5,11 | RBAC only |
| D12 ingestion | N/A | not verified (importer tools exist, UNVERIFIED) |
| D13-D16 AI/vector/GraphRAG | 3 | unknown; Nebula store integrations exist in LlamaIndex (see V10 fragment) |
| D17 ops/backup | 7 | UNVERIFIED |
| D18 UX | N/A | Studio/Explorer not examined |
| D19-D20 licence/deploy | 10 | Apache-2.0 |
| D21 ecosystem | 1 | community channels |
| D22-D24 cost, risk, roadmap | 12,15 | covered |

## Appendix B. Capability mapping
| CAP-ID | This tech | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-01 | native | 03 | BL-01 implemented | INTEGRATE | P2 |
| CAP-05 | native | 03 | BL-01 (single backend) | INTEGRATE | P2 |
| CAP-14 | partial | 01 | BL-59 absent | EXPERIMENT | P3 |
| CAP-45 | native (RBAC) | 03 | BL-19 implemented | REJECT | P3 |
| CAP-77 | native (Apache-2.0) | 01 | BL-22 | REUSE | P2 |

## Appendix C. Evidence records
| CLAIM-ID | Product/version/date | Claim | Class | Source | Dates | Confidence | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-nebula-01 | NebulaGraph, README 2026-10-26 | Apache-2.0; symmetric distribution; Raft; openCypher-compatible; RBAC; free as SaaS backend | vendor docs | GitHub vesoft-inc/nebula, https://github.com/vesoft-inc/nebula | accessed 2026-10-26 | 0.8 | none |
| CLAIM-nebula-02 | v3.8.0 | latest release 2024-05-17; push 2026-09-08; ~12.4k stars | primary (API) | https://api.github.com/repos/vesoft-inc/nebula | 2026-10-26 | 0.85 | tags list may omit unreleased builds |
| CLAIM-nebula-03 | 3.8.0 docs | metad/graphd/storaged; RocksDB default; Raft per partition | primary docs | https://docs.nebula-graph.io/3.8.0/1.introduction/3.nebula-graph-architecture/1.architecture-overview | 2026-10-26 | 0.7 (via search snippet) | none |

## Appendix D. Assumptions
Hypotheses flagged inline; enterprise-edition status assumed UNVERIFIED; deeper source-path citations deferred for Tier B.
