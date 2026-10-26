# C13 — OpenLineage and Marquez

| Field | Value |
|---|---|
| Registry ID | T-C13-openlineage-marquez |
| Tier | B (lineage standard + reference server; EOIP emits internal lineage and has a mapper, not an exporter) |
| Versions examined | OpenLineage 1.54.0 (13 Oct; year not shown on page, 2026 inferred); Marquez 0.50.0 (release page, 24 Oct, 2024 inferred), main branch commits to 2026-04-12 |
| Verified on | 2026-10-26 (brief says 10-18; actual access date used) |
| Worker | V26 |

## 1. Identity, current status, tier, sources
OpenLineage = open standard (JSON-Schema spec + client libraries + integrations: Spark, Airflow, dbt, Flink…) for run/job/dataset lineage events [CLAIM-ol-01]. Marquez = reference metadata/lineage server (Java, PostgreSQL, web UI), Apache-2.0, LF AI & Data graduated, README says "under active development" [CLAIM-ol-02]. Marquez cadence: last tagged release visible is 0.50.0; main shows a 0.51.1 prepare-release commit (2025-03-27) then only UI/doc/query-fix commits through 2026-04-12 — effectively maintenance [CLAIM-ol-03]. OpenLineage spec licence not re-fetched this session (believed Apache-2.0, confidence 0.6). Sources: openlineage.io docs, GitHub OpenLineage/OpenLineage and MarquezProject/marquez.

## 2. Problem, workloads, workflows
Cross-tool operational lineage for data pipelines: "which job run produced this dataset, from what inputs, with what schema/quality?" Workflows: Airflow task emits START/COMPLETE with input/output datasets; Marquez stores and renders the graph; impact analysis for column/dataset change. Not entity-level knowledge lineage.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Object model Job / Run (client-generated runId, UUIDv7 recommended) / Dataset [CLAIM-ol-04] | present |
| RunEvent, JobEvent, DatasetEvent [CLAIM-ol-04] | present |
| Standard facets: run (nominalTime, parent, errorMessage, sql), job (sourceCodeLocation, sourceCode), dataset (schema, dataSource, lifecycleStateChange, version), input (dataQualityMetrics/Assertions), output (outputStatistics) [CLAIM-ol-04] | present |
| Custom facets with `{prefix}{Name}{Entity}Facet`, immutable `_schemaURL` [CLAIM-ol-05] | present |
| Column-level lineage facet | UNVERIFIED this session (believed present) |
| HTTP/Kafka/file transports, Spark/Airflow/dbt integrations | present (docs; not re-verified per integration) |
| Marquez REST API, lineage graph UI, OpenSearch search | present (reasoned from README; conf 0.6) |
| Auth, tenancy, per-row ACL in Marquez | NOT PUBLICLY VERIFIED / believed absent |

## 4. Architecture
```
 producers (Spark/Airflow/dbt/EOIP exporter)
   | OpenLineage RunEvent JSON (HTTP POST /api/v1/lineage)
   v
 Marquez API (Java) --> PostgreSQL (jobs, runs, datasets, versions, facets JSONB)
        |--> OpenSearch (optional search)     --> React UI (lineage DAG)
```

## 5. Under-the-hood reconstruction
Event-in, append-and-version model: each event carries `eventType`, `eventTime`, `run{runId,facets}`, `job{namespace,name,facets}`, `inputs[]/outputs[]`, `producer`, `schemaURL`. Server upserts job/dataset, creates immutable dataset/job *versions* on schema/source change, links runs to versions; lineage = bounded traversal over run-input/output edges in Postgres (hypothesis: recursive CTE/graph walk; code not inspected). Facet replacement: same-named facet fully replaces earlier instance [CLAIM-ol-05]. Concurrency: events may arrive out of order; spec requires idempotent upsert by runId (reasoned). Security: none in spec; deployment-level.

## 6. Inferred requirements
FR: emit RunEvent per ingestion/mapping run with input = SourceEvent datasets, output = graph partitions; stable job names; immutable facet schema URLs. NFR: event idempotency, no PII in facets (egress/DLP), optional (off by default, air-gap safe: file/HTTP-to-local transport).

## 7. Performance and resource model
No benchmarks gathered; NOT PUBLICLY VERIFIED. Cost drivers: event volume × facets JSONB size; Postgres graph traversal depth. Failure mode: lineage gaps from missed events.

## 8. Strengths
Vendor-neutral, extensible facets, broad integrations; small footprint (Postgres). Match: EOIP exporter. Exceed: entity/claim-level and ACL-aware lineage.

## 9. Limitations
| Class | Item |
|---|---|
| Intentional trade-off | Dataset/job granularity; no entity/claim semantics |
| Maturity | Marquez maintenance-mode cadence [CLAIM-ol-03] |
| Friction | Producer-side instrumentation needed; no authz model in spec |
| Hypothesis | Postgres traversal degrades on very deep/wide lineage |

## 10. Deployment, licensing
Apache-2.0 (Marquez verified; spec believed same). Self-hosted Docker/K8s, Postgres required; no cloud dependency; air-gap viable. No legal trigger identified; confirm spec licence.

## 11. Delta vs EOIP baseline
EOIP has BL-41 (`provenance/lineage.py` traversal over EVIDENCED_BY/INGESTED_IN, evidence manifests) and BL-33 PROV-O triples; `future_scope.py:622` contains a mapper `to_openlineage` (GAP-LIN-001..005) — scaffold, no evidence of production emission. EOIP lineage is entity-level and tenant-aware in intent; absent: standards-conformant OpenLineage emission, catalog interop (CAP-40). EOIP lead: entity/claim granularity (BL-39, BL-41); OpenLineage lead: ecosystem.

## 12. Cards
STR-openlineage-01 | OpenLineage | open event spec with facets | CLAIM-ol-04,05 | lets customers' Airflow/Spark/dbt lineage flow into the brain and EOIP runs flow into their catalogs | integrate | opt-in `OpenLineageExporter` mapping IngestionRun→Run, SourceEvent set→inputs | JSON validates against pinned spec schema; Marquez ingests it.
STR-openlineage-02 | OpenLineage | immutable versioned facet schemas | CLAIM-ol-05 | forward-compatible custom facets | match | `eoip_*` facets (tenant-hash, evidence count) with SHA-pinned URLs | schema URL resolves offline.
INV-openlineage-01 | OpenLineage/Marquez, 1.54/0.50, pipeline lineage | dataset-level granularity only; no claim/ACL semantics | root cause: semantics (proven by object model) | EOIP entity-level lineage plus ACL filter on lineage reads; worse where only pipeline view needed | options: (a) exporter only, (b) ingest OL events as Run/Dataset nodes tagged observed, (c) unified lineage+claim graph | choose (a) then (b) | POC: replay a Spark OL event stream, verify joins to entities; metric: 100% events mapped, 0 cross-tenant leaks | deps: BL-18 ACL gap, BL-20 | defensibility: claim-level lineage with permissions | EXPERIMENT. Seed hypotheses (§10.5): none target this technology.
INV-openlineage-02 | Marquez | slowed maintenance, no authz | root cause: maturity (proven by commit history) | do not make Marquez a hard dependency; keep it a sink | options: use as test sink / own minimal store / none | choose test sink only | POC: 10k events ingest to local Marquez | DEFER (as product dependency).

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-40 OpenLineage emission | INTEGRATE (exporter, P1) |
| CAP-40 Marquez server | REFERENCE/EXPERIMENT as optional sink |
| CAP-38 facet design for evidence | REUSE pattern |
| CAP-42 catalog | DEFER |

## 14. Tests/POC
Export schema validation against pinned OpenLineage JSON schema; Marquez round-trip; DLP test (no PII in facets); idempotent re-emit after replay (BL-24).

## 15. Risks / open questions
Spec licence confirm; Marquez future; column-level facet verification; whether lineage events leak tenant names; mapping of replay re-runs to new runIds.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | active spec; Marquez maintenance |
| D2 | 2 | pipeline lineage |
| D3 | 4 | event producer→API→Postgres |
| D4 | 5 | Postgres relational; N/A graph |
| D5 | 3 | JSON-Schema facets |
| D6 | N/A | no graph query language verified |
| D7 | N/A | none |
| D8 | 5 | idempotent upsert (reasoned) |
| D9 | 2,5 | event ingest |
| D10 | 11 | dataset-level only |
| D11 | 5 | run/version history |
| D12–D14 | N/A | out of scope |
| D15 | 3 | facet governance via spec PRs |
| D16 | 3 | lineage UI |
| D17 | 3,12 | clients, custom facets |
| D18 | 3,9 | no authz verified |
| D19 | 9 | namespaces only; not tenancy |
| D20 | 7 | no benchmarks |
| D21 | 10 | Apache-2.0 |
| D22 | 11 | JSON events; PROV mapping possible |
| D23 | N/A | none identified |
| D24 | App C | docs-level evidence |

## Appendix B — Capability mapping
| CAP | Native? | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-40 | native | ol-04 | BL-41 partial vs standard | INTEGRATE | P1 |
| CAP-38 | partial | ol-05 | BL-41,BL-33 | REUSE | P2 |
| CAP-42 | Marquez partial | ol-02 | none | DEFER | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| ol-01 | OL 1.54.0 | latest release 1.54.0, 13 Oct | Officially documented | github.com/OpenLineage/OpenLineage/releases | n/a / 2026-10-26 | 0.8; year inferred | none |
| ol-02 | Marquez | Apache-2.0, LF AI & Data graduated, active badge | Officially documented | github.com/MarquezProject/marquez | 2026-10-26 | 0.8 | ol-03 |
| ol-03 | Marquez | latest release 0.50.0; main commits Mar 2025 then Mar–Apr 2026 UI/doc/fix | Officially documented | github.com/MarquezProject/marquez/commits/main | 2026-10-26 | 0.7 | README "active" |
| ol-04 | OL 1.54.0 | Job/Run/Dataset model, 3 event types, listed facets | Officially documented | openlineage.io/docs/spec/object-model | 2026-10-26 | 0.9 | none |
| ol-05 | OL 1.54.0 | custom facet naming, immutable `_schemaURL`, replacement semantics | Officially documented | openlineage.io/docs/spec/facets/ | 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions
Access date 2026-10-26; GitHub years inferred from footer/context; Marquez internals from README-level knowledge, unverified in code.
