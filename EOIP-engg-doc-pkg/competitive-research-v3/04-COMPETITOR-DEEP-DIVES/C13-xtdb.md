# C13 — XTDB

| Field | Value |
|---|---|
| Registry ID | T-C13-xtdb |
| Tier | B (bitemporal database reference) |
| Versions examined | v2.2.0 (21 Oct, 2026 inferred; GA, "Latest"); v2.1.1 (21 Oct); v2.1.0 (01 Dec 2025 inferred); 1.x on `1.x` branch |
| Verified on | 2026-10-26 |
| Worker | V26 |

## 1. Identity, status, sources
XTDB (JUXT / XTDB Ltd.), immutable SQL database with automatic bitemporality. 2.x is GA: v2.1.0 not marked pre-release, v2.2.0 is "Latest"; 2.2.0 requires rolling upgrades via 2.1.1 [CLAIM-xtdb-01]. `main` is 2.x; 1.x maintained on a branch. Licence: Mozilla Public License 2.0 "or any later version" (weak, file-level copyleft) [CLAIM-xtdb-02] — redistribution-safe if MPL file-level obligations met; legal-review flag (low). Sources: GitHub repo/releases, docs.xtdb.com.

## 2. Problem, workloads
Auditable, corrected-history business data; "as-of" reporting; regulated records; replacing hand-rolled valid/system-time columns. Example: insert price with valid-time range, later correct it; query as at 31 March of what was known on 15 April.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Automatic bitemporal columns on every table (four temporal columns) [CLAIM-xtdb-03] | present |
| SQL (SQL:2011-inspired) over Postgres wire protocol; XTQL | present [CLAIM-xtdb-02] |
| Columnar Arrow storage on object store; log as coordination point | present [CLAIM-xtdb-02,03] |
| Single writer leader per database; read-only followers [CLAIM-xtdb-01] | present (2.2) |
| External sources: Postgres logical replication, Kafka Connect, source SPI | present (2.2) |
| Arrow ADBC / Flight SQL | present (2.2) |
| Background GC, metrics/tracing, ingest-only node | present (2.2) |
| Graph traversal / Cypher / SPARQL | absent (relational; recursive SQL only — unverified depth) |
| Row/tenant ACL, RLS | NOT PUBLICLY VERIFIED; `CREATE USER` removed in 2.2 [CLAIM-xtdb-01] |

## 4. Architecture
```
 clients (pgwire / HTTP / ADBC)
        v
  node(s): SQL/XTQL planner -> tx processing (single leader per DB)
        |  tx log (e.g. Kafka / local)  --> Arrow/columnar blocks (flush 15 min if quiet)
        v
  object store (S3-like) : tables, indexes, metadata ; followers read-only
```

## 5. Reconstruction
Data model: documents/rows with `_id`, `_valid_from/_valid_to`, `_system_from/_system_to` maintained automatically [CLAIM-xtdb-03]. Writes append; updates close the prior version's system interval and insert new ones (inferred from "past versions retained"). Storage: columnar Arrow files in object storage, tx log as ordering authority; leader resolves transactions once and publishes results (2.2) [CLAIM-xtdb-01]. Queries default "now"; temporal qualifiers select as-at/range. 2.2 behaviour changes: snapshot fixed at first query, explicit SYSTEM_TIME must exceed latest tx [CLAIM-xtdb-01]. Indexing/planner internals: NOT PUBLICLY VERIFIED this session (source not read).

## 6. Inferred requirements
JVM 25 images; Kafka (or alternative log) topic per database incl. replica topic; object store; Postgres tooling compatibility; careful upgrade path.

## 7. Performance
No independent benchmarks gathered; vendor numbers not collected. Scaling hypothesis: reads scale via followers, writes bound by single leader per DB; history retained forever (cost on object storage). Failure modes: log loss, version skew (2.1.0 cannot read 2.2 tx format).

## 8. Strengths
Bitemporality without schema work; SQL familiarity; cheap history on object storage; Postgres ecosystem. Match: BL-37 semantics; exceed: engine-enforced non-overlap.

## 9. Limitations
| Class | Item |
|---|---|
| Verified trade-off | single writer per DB; breaking changes between minors (2.2 list) [CLAIM-xtdb-01] |
| Licensing | MPL-2.0 file-level copyleft |
| Friction | v1→v2 rewrite (different engine); no graph query language |
| Hypothesis | write-heavy streams limited by one leader; no native per-tenant ACL |

## 10. Deployment/licensing
Self-host JVM + object store + log; runs in containers; embeddable in-process (JDK) — air-gap viable with MinIO/local FS (hypothesis). Not a `GraphStore` backend; best as optional history/audit store.

## 11. Delta vs baseline
BL-37 provides valid + transaction time over any GraphStore at app layer, which XTDB provides in-engine with SQL:2011 semantics. EOIP lacks: engine-enforced temporal integrity, temporal SQL, cheap long-term history storage. XTDB lacks: graph traversal, ontology, ACL (BL-18/19/20 matter more). Inconclusive on speed.

## 12. Cards
STR-xtdb-01 | XTDB 2.2 | automatic bitemporality | CLAIM-xtdb-03 | corrected-history answers with no custom columns | match | HistoryStore SPI; XTDB adapter as oracle/optional backend | randomized history agrees with BL-37 `slice()`.
STR-xtdb-02 | XTDB 2.2 | history on object storage + Postgres wire | CLAIM-xtdb-02 | cheap BI access via Metabase/Grafana | integrate | read-only history export to XTDB | Metabase query over audit history.
INV-xtdb-01 | XTDB 2.2, writes | single leader per DB; relational-only | root cause: algorithm/data model (proven for leader, CLAIM-xtdb-01) | EOIP shards per tenant, history per tenant DB; graph stays in GraphStore | options: oracle only / optional adapter / native temporal indexes | choose oracle then adapter | POC: 100k events replayed into XTDB vs BL-37, metric: identical as-of results, ingest rate vs baseline | deps: JDK25, log | defensibility: backend-neutral graph + temporal | EXPERIMENT. Seed §10.5: none target XTDB.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-34 as-of semantics | EXPERIMENT (oracle), P2 |
| CAP-36 history store | INTEGRATE optional adapter, P3 |
| CAP-01 as graph backend | REJECT |
| CAP-74 PITR | REFERENCE |

## 14. Tests
Oracle equivalence on property-test histories; 2.1.1→2.2 upgrade drill; air-gap start with local object store; MPL file-level audit of any redistributed XTDB jar.

## 15. Risks / open questions
MPL obligations if embedded; breaking-change cadence; ACL model; planner internals unread; exact 2.1.0/2.2.0 years inferred.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | MPL-2.0, GA 2.x |
| D2 | 2 | audit/time |
| D3 | 4 | log + leader + object store |
| D4 | 5 | Arrow columnar |
| D5 | 3 | relational, no constraints verified |
| D6 | 3 | SQL/XTQL; planner UNVERIFIED |
| D7 | N/A | none |
| D8 | 5,9 | single leader |
| D9 | 3 | Postgres/Kafka sources |
| D10 | 11 | none |
| D11 | 3,5 | bitemporal core |
| D12–D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | pgwire, ADBC |
| D18 | 3 | UNVERIFIED |
| D19 | 9 | none verified |
| D20 | 7 | no numbers |
| D21 | 10 | MPL |
| D22 | 11 | SQL export |
| D23 | N/A | |
| D24 | App C | docs-level |

## Appendix B — Capability mapping
| CAP | Native | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-34 | native | xtdb-03 | BL-37 Implemented | EXPERIMENT | P2 |
| CAP-36 | native | xtdb-03 | BL-37/24 | INTEGRATE | P3 |
| CAP-16 | native SQL | xtdb-02 | BL-59 Absent | REFERENCE | P3 |
| CAP-74 | partial | xtdb-02 | BL-50 | REFERENCE | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| xtdb-01 | 2.2.0 | GA; single writer; rolling upgrade via 2.1.1; breaking list | Officially documented | https://github.com/xtdb/xtdb/releases/tag/v2.2.0 | 21 Oct (year inferred) / 2026-10-26 | 0.85 | none |
| xtdb-02 | repo main | MPL-2.0+; SQL + XTQL; Arrow columnar on object storage | Officially documented | https://github.com/xtdb/xtdb | 2026-10-26 | 0.9 | none |
| xtdb-03 | docs | four temporal columns; valid + system time; SQL:2011 inspired | Officially documented | https://docs.xtdb.com/intro/what-is-xtdb.html | 2026-10-26 | 0.85 | none |

## Appendix D — Assumptions
Release years inferred from page footer; internals beyond docs are hypotheses.
