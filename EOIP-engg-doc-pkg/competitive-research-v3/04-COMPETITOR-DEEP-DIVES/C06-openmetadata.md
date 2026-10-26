| Field | Value |
|---|---|
| Registry ID | T-C06-openmetadata |
| Tier | B - OSS catalog; closest self-hostable peer to DataHub (CAP-42, CAP-40) |
| Versions examined | 2.0.6-release (2026-10-21, latest); 2.0.5 (10-08); 2.0.4 (10-06); 2.0.3 (09-30). Year inferred from page context; day/month only displayed |
| Verified on | 2026-10-26 |
| Worker | V18 |

# OpenMetadata

## 1. Identity, current status, tier, and sources
Open-source metadata platform, repo `open-metadata/OpenMetadata`, Apache-2.0, about 15.6k stars [CLAIM-om-01]. Commercial company: Collate, which sells managed enterprise features (AI agents, automation, enterprise MCP workflows) [CLAIM-om-01]. Status: active, very frequent patch releases (four in 3 weeks) [CLAIM-om-02]. Compared with DataHub, see `C06-datahub.md` (Apache-2.0 metadata graph with Kafka-based log); not duplicated here. Sources: GitHub, docs.open-metadata.org (Appendix C).

## 2. Primary problem, workloads, workflows
| Concern | Position |
|---|---|
| Catalog search | Core: Elasticsearch/OpenSearch index [CLAIM-om-03] |
| Operational lineage | Core: auto-extraction, OpenLineage events, column-level, manual edits [CLAIM-om-04] |
| Semantic inference | Absent as a reasoner; RDF/OWL/SHACL/JSON-LD named as supported standards (depth UNVERIFIED) [CLAIM-om-01] |
| Knowledge intelligence | Vendor framing: "metadata graph", governed memory, semantic search, MCP at `/mcp` [CLAIM-om-01] |

Workflows: ingest Snowflake metadata and query-log lineage; steward sets owner (a Group) and policy; engineer inspects column lineage before change; agent calls MCP.

## 3. Feature inventory
| Area | Feature | Status |
|---|---|---|
| Model | JSON-Schema entity definitions generating Java/Python/TypeScript | present [CLAIM-om-03] |
| Storage | MySQL (docs) / PostgreSQL; ES/OpenSearch | present [CLAIM-om-03][CLAIM-om-05] |
| Versioning | per-entity versions (0.1 minor, 1.0 major), change events | present [CLAIM-om-03] |
| Connectors | 130+ | present [CLAIM-om-01] |
| Lineage | table + column, OpenLineage ingest, cross-DB | present [CLAIM-om-04] |
| AuthZ | roles, policies, RBAC+ABAC conditions, `isOwner()` | present [CLAIM-om-06] |
| MCP / SDKs | MCP, Python, TS, Java AI SDKs | present [CLAIM-om-01] |
| Enterprise-only | AI Studio, agents, managed ops (Collate) | enterprise-only [CLAIM-om-01] |

## 4. Architecture diagram
```
connectors -> Ingestion Framework (Python) -> REST API (Java, Jetty)
   Entity Resource -> Entity Repository -> MySQL/Postgres: <entity>_entity JSON, entity_relationship, change_event
                                        -> Elasticsearch/OpenSearch (search)
   UI (TypeScript) | MCP /mcp | events
```

## 5. Under-the-hood reconstruction
Entities are JSON documents in one table per type; relationships are rows in `entity_relationship` (the graph is relational, not a graph database); each write that changes an entity creates a version and a `change_event`; `POST` runs Prepare (validate, compute FQN) then Store; `PUT` restricts changeable fields [CLAIM-om-03]. Search is a separate index fed from the entity store (hypothesis on sync mechanism). Policy evaluation maps each API call to (resource type, operation) and evaluates rule conditions [CLAIM-om-06]. Blueprint: schema-first JSON-Schema codegen + relational triple table (from, to, relation) + event table + search projection. This is easily reproducible on EOIP's GraphStore protocol. Concurrency, partitioning and caching: NOT PUBLICLY VERIFIED.

## 6. Requirements inferred
FR: schema-first model, FQN-based identity, versioned entities, lineage ingest incl. OpenLineage, policy engine with ownership conditions. NFR: modest footprint (below), upgrade safety (data-integrity migrations appear in 2.0.3 notes) [CLAIM-om-02].

## 7. Performance and resource model
Vendor sizing for one replica: server 4 vCPU/16 GiB/100 GiB; database 4 vCPU/16 GiB; Elasticsearch 2 vCPU/8 GiB/100 GiB [CLAIM-om-05]. This is a sizing guide, not a benchmark; no throughput numbers found. Relational edge table implies deep-traversal cost grows with joins (hypothesis).

## 8. Strengths
| Strength | Match/exceed |
|---|---|
| Small stack (RDBMS + search), no Kafka/graph DB needed | match: one-node-first fits EOIP |
| Policy conditions with ownership | exceed: add per-fact source ACL (BL-17/18) |
| Apache-2.0 | REUSE patterns freely; legal check for code |
| OpenLineage ingest | integrate |

## 9. Limitations
Verified defects: 2.0.x ingestion regressions required a restore release; 2.0.3 fixed a certificate-verification bypass and a SQL injection [CLAIM-om-02]. Policy granularity: grants at service level reach all assets under it; per-asset grants not confirmed [CLAIM-om-06]. Intentional trade-off: relational graph. Hypothesis: no reasoning. Root causes: algorithmic (join-based traversal), user friction (connector churn).

## 10. Deployment, licensing, viability
Self-host via Docker/Helm/bare metal [CLAIM-om-05]; Apache-2.0; air-gap viable (connectors to local sources; no cloud required, confidence 0.7). Enterprise features under Collate; community-vs-enterprise split is a legal-review trigger.

## 11. Competitive delta
EOIP lacks a catalog UI/model (no BL for it); has GraphStore (BL-01) that could host OM-style entities; has ACL capture but no enforcement (BL-17/18); OpenLineage ingest not found in baseline.

## 12. Cards
STR-om-01 | OpenMetadata | schema-first entity codegen + change events | CLAIM-om-03 | consistent API/SDK/UI | match | JSON Schema in contracts/, generate TS types | schema change breaks no consumer in CI.
INV-om-01 | OM 2.0.x | relational edge table and regressions | root cause: storage/maturity (proven regressions, hypothesis on joins) | options: integrate as source / native catalog view on GraphStore / lineage as first-class graph | selected: native view + OpenLineage ingest | benchmark: 5-hop impact query on 1M-edge lineage vs OM | defensibility: ACL-aware lineage | decision: EXPERIMENT. Seed hypothesis on catalogs lacking evidence spans: partly supported.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-40 lineage ingest (OpenLineage) | INTEGRATE |
| CAP-42 catalog | INTEGRATE OM as source; BUILD thin native |
| Policy model | EXPERIMENT |
| Collate features | REJECT |

## 14. Tests and acceptance
Ingest an OpenLineage fixture and an OM export; 5-hop impact query p95 target set from OM baseline run; verify per-asset ACL denial and audit.

## 15. Risks and open questions
Postgres parity and version minima (table empty in captured docs); exact enterprise/OSS feature line.

## Appendix A - Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, active |
| D2 | 2 | catalog+lineage |
| D3 | 4 | 3 blocks |
| D4 | 5 | JSON rows + edge table |
| D5 | 5 | JSON Schema |
| D6 | N/A | REST, no graph query |
| D7 | 2 | none |
| D8 | 7 | sizing only |
| D9 | 3 | 130+ connectors |
| D10 | N/A | FQN identity only |
| D11 | 5 | entity versions |
| D12 | N/A | out of scope |
| D13 | 2,3 | MCP |
| D14 | N/A | unverified |
| D15 | 3 | stewardship, policies |
| D16 | 3 | UI, not run |
| D17 | 3 | SDKs |
| D18 | 3,9 | RBAC/ABAC; CVE-class fixes |
| D19 | N/A | not documented |
| D20 | 7 | sizing |
| D21 | 10 | Collate split |
| D22 | 8 | OpenLineage, JSON-LD |
| D23 | N/A | not assessed |
| D24 | 9 | docs + releases |

## Appendix B - Capability mapping
| CAP | OM | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-40 | native | 04 | BL-41 partial | INTEGRATE | P1 |
| CAP-42 | native | 03 | none | BUILD thin | P1 |
| CAP-26 | native | 01 | BL-23 | INTEGRATE | P2 |
| CAP-59 MCP | native | 01 | BL-47 | REUSE own | P3 |

## Appendix C - Evidence records
| CLAIM | product/date | claim | class | source | access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-om-01 | repo README | Apache-2.0; ~15.6k stars; 130+ connectors; MCP `/mcp`; Collate commercial; standards JSON Schema, RDF/OWL, SHACL, JSON-LD | Officially documented | github.com/open-metadata/OpenMetadata | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-om-02 | 2.0.3-2.0.6 | 2.0.6 latest (21 Oct); 2.0.5 restores metadata hit by 2.0 regressions; 2.0.3 security fixes | Officially documented | github.com/open-metadata/OpenMetadata/releases | 2026-10 / 2026-10-26 | 0.8 year inferred | none |
| CLAIM-om-03 | docs latest | API/UI/Ingestion; MySQL entity store with per-entity JSON tables, `entity_relationship`, `change_event`; ES search; versioning | Officially documented | docs.open-metadata.org/latest/main-concepts/high-level-design | n/a / 2026-10-26 | 0.85 | page omits Postgres/OpenSearch |
| CLAIM-om-04 | docs latest | Lineage auto-extract, OpenLineage ingest, column-level, cross-DB | Officially documented | docs.open-metadata.org/latest/how-to-guides/data-lineage | n/a / 2026-10-26 | 0.8 | extraction method unstated |
| CLAIM-om-05 | docs | Postgres or MySQL; ES/OpenSearch; sizing; Helm/bare metal | Officially documented | docs.open-metadata.org/latest/deployment/production-ready-requirements | n/a / 2026-10-26 | 0.7 | doc has conflicting DB storage numbers |
| CLAIM-om-06 | docs | Policies evaluate caller, resource, operation; RBAC+ABAC; Group ownership; service-level grants cascade | Officially documented | docs.open-metadata.org/latest/how-to-guides/admin-guide/roles-policies | n/a / 2026-10-26 | 0.8 | per-asset grants unconfirmed |

## Appendix D - Assumptions
Release year 2026 inferred. Elasticsearch sync mechanism and Airflow role not verified.
