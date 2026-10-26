| Field | Value |
|---|---|
| Registry ID | T-C06-apache-atlas |
| Tier | B - OSS lineage catalog; Hadoop-era reference and Purview ancestor (CAP-40, CAP-42) |
| Versions examined | 2.5.0 (2026-04-30); 2.4.0 (2025-01-02 per ASF release catalog; 2025-01-04 per board minutes) |
| Verified on | 2026-10-26 |
| Worker | V18 |

# Apache Atlas

## 1. Identity, current status, tier, and sources
**Name collision resolved:** this is Apache Atlas, the Apache Software Foundation metadata and governance framework (`apache/atlas`), not Atlan, Atlas (MongoDB cloud) or other Atlas products. Licence Apache-2.0, about 2.2k stars, no archive notice, active pull requests [CLAIM-atlas-01]. Latest release 2.5.0 on 2026-04-30; 2.4.0 on 2025-01 [CLAIM-atlas-02]. Cadence: slow (about 15 months between minors). Status: maintenance-to-active. It is Hadoop-centric ("across the Hadoop platform and beyond") [CLAIM-atlas-01]. Downstream: Cloudera embeds it (CDP 7.3.2 moves Atlas 2.1.0 to 2.4.0) [CLAIM-atlas-02]; Microsoft Purview Data Map exposes Atlas-compatible APIs [CLAIM-atlas-03]; the Atlan SDK credits Atlas code [see C06-atlan]. Tier B because it shapes the typedef/lineage model most catalogs copy.

## 2. Primary problem, workloads, workflows
| Concern | Position |
|---|---|
| Catalog search | Core (search API; index backend per deployment) |
| Operational lineage | Core: hooks for Hive, Impala, Spark etc. publish lineage via Kafka (background knowledge, see D) |
| Semantic inference | Absent; classification propagation is rule-based |
| Knowledge intelligence | Absent |

Workflow: a Hive hook publishes a CTAS as Process entity linking input and output tables; a classification `PII` on a column propagates downstream; Ranger policies use tags.

## 3. Feature inventory
| Area | Feature | Status |
|---|---|---|
| Type system | Typedefs for entities, classifications, relationships, business metadata | present (background) |
| Graph engine | JanusGraph | present (background; not re-verified) |
| Search | Solr / Elasticsearch | present (background) |
| Notifications | Kafka | present (background) |
| Lineage | Process-based, column-level for supported hooks | present (background) |
| Classification propagation | via lineage | present (background) |
| Authorization | simple authorizer, Ranger | present (background) |
| UI, REST | yes | present |
| Fixes in 2.5.0 | async import speed, array business-attribute delete, Impala INSERT OVERWRITE hook, search API | [CLAIM-atlas-02] |

## 4. Architecture diagram
```
hooks (Hive/Spark/Impala/Kafka) -> Kafka -> Atlas server (REST, type system)
   -> JanusGraph (HBase/Cassandra/BerkeleyDB) + Solr/ES index
   -> UI | REST | Ranger tag policies
```
Component list is from prior project knowledge; the project site pages fetched in this run listed only topic keywords (JanusGraph, HBase, Solr, Kafka, lineage, classification propagation) [CLAIM-atlas-04].

## 5. Under-the-hood reconstruction
Verified only at keyword level [CLAIM-atlas-04]. From background (confidence 0.5): entities are JanusGraph vertices with a GUID; relationships are edges; the typedef registry drives schema; classification propagation traverses lineage edges and stamps propagated tags; soft delete leaves vertices that need purging (Cloudera added auto-purge in 7.3.2) [CLAIM-atlas-02]. Blueprint: typed property graph + Process nodes + propagation walker + tag-based policy. EOIP already has such a graph protocol (BL-01), so Atlas adds the typedef/propagation design only.

## 6. Requirements inferred
Hook-based lineage capture, typedef extensibility, tag propagation, tag-driven authorization, purge of soft deletes.

## 7. Performance and resource model
No benchmark found. JanusGraph plus HBase plus Solr plus Kafka is a heavy footprint (background); EOIP already lists JanusGraph as an adapter (BL-05).

## 8. Strengths
| Strength | Match/exceed |
|---|---|
| Ecosystem standard; Atlas-compatible APIs in Purview | integrate: an Atlas REST read adapter |
| Tag propagation + Ranger | match concept |
| Apache-2.0 | REUSE ideas freely |

## 9. Limitations
Verified: soft-delete buildup needed auto-purge downstream [CLAIM-atlas-02]; slow release cadence. Hypothesis: heavyweight stack, Hadoop-era connector set. Root causes: operational overhead (4 services), user friction (UI age), algorithmic (graph store scaling on HBase).

## 10. Deployment, licensing, viability
Apache-2.0; air-gap viable (self-hosted, no cloud); one-node first is hard because of the multi-service stack. No community-vs-enterprise split at ASF; vendor distributions (Cloudera) add features.

## 11. Competitive delta
EOIP's JanusGraph adapter (BL-05) could run an Atlas-like typedef layer; EOIP lacks hook-based lineage capture (BL-23 covers connectors only) and lineage propagation rules.

## 12. Cards
STR-atlas-01 | Atlas | classification propagation along lineage | CLAIM-atlas-04 | sensitivity inheritance | match | propagation walker emitting PROPOSED tags | 3-hop propagation + deletion test.
INV-atlas-01 | Atlas 2.4/2.5 | soft-delete accumulation and heavy stack | root cause: storage/deployment (proven for delete, hypothesis for stack) | options: integrate Atlas read adapter / native tombstone purge policy / lineage with TTL | selected: native tombstone policy (BL-25 exists) | benchmark: graph size after 1M create/delete cycles | defensibility: audit-preserving purge | decision: ADOPT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-40 lineage model | REUSE design (Process node) |
| CAP-42 catalog | INTEGRATE Atlas as source (REST) |
| Atlas runtime as dependency | REJECT (heavy) |

## 14. Tests and acceptance
Import a recorded Atlas entity JSON export; map to GraphStore; propagate a tag three hops; confirm tombstone purge keeps audit trail.

## 15. Risks and open questions
Architecture details unverified this run; exact 2.5.0 release notes not read; activity of committers.

## Appendix A - Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, 2.5.0 |
| D2 | 2 | lineage catalog |
| D3 | 4 | background |
| D4 | 5 | JanusGraph (background) |
| D5 | 3 | typedefs |
| D6 | N/A | REST/DSL, unverified |
| D7 | 2 | rule-based |
| D8 | 7 | N/A |
| D9 | 2 | hooks via Kafka |
| D10 | N/A | GUID identity |
| D11 | 9 | soft delete only |
| D12 | N/A | out of scope |
| D13 | N/A | none |
| D14 | N/A | none |
| D15 | 3 | classifications |
| D16 | 3 | UI exists |
| D17 | 3 | REST |
| D18 | 3 | Ranger |
| D19 | N/A | none |
| D20 | 7 | N/A |
| D21 | 10 | ASF |
| D22 | 8 | Purview compat |
| D23 | N/A | not assessed |
| D24 | 5 | site pages thin |

## Appendix B - Capability mapping
| CAP | Atlas | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-40 | native | 04 | BL-41 partial | REUSE design | P1 |
| CAP-42 | native | 01 | none | INTEGRATE | P2 |

## Appendix C - Evidence records
| CLAIM | product/date | claim | class | source | access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-atlas-01 | repo | Apache-2.0; ~2.2k stars; not archived; "metadata management and governance across the Hadoop platform and beyond" | Officially documented | github.com/apache/atlas | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-atlas-02 | 2.5.0 / 2.4.0 | 2.5.0 released 2026-04-30; 2.4.0 2025-01-02/04; Cloudera 7.3.2 moves 2.1.0 to 2.4.0 and adds auto-purge | Officially documented (ASF) / third-party | release-catalog.apache.org/atlas/2.5.0/index.html; whimsy board minutes Atlas; docs.cloudera.com CDP 7.3.2 notes | 2026-10-26 | 0.8 | 2.4.0 date differs by 2 days |
| CLAIM-atlas-03 | Purview | Data Map exposes Apache Atlas-compatible APIs | Officially documented | learn.microsoft.com/purview/data-map; docs.azure.cn purview pricing | 2026-10-26 | 0.7 | none |
| CLAIM-atlas-04 | atlas.apache.org | Site lists type system, JanusGraph, HBase, Solr, Kafka, lineage, classification propagation | Officially documented (keywords only) | atlas.apache.org | 2026-10-26 | 0.5 | no detail pages reachable |

## Appendix D - Assumptions
Architecture beyond keywords relies on prior knowledge (confidence 0.5); marked as such. Hook list not verified.
