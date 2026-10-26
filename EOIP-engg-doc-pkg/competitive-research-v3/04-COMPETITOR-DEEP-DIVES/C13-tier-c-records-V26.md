# C13 — Tier C records (V26)

Access date 2026-10-26. GitHub pages show day/month only; years inferred and marked.

### T-C13-fluree — Fluree

| Field | Value |
|---|---|
| Official URL | https://github.com/fluree/db |
| Owner | Fluree PBC |
| Latest version + date | v4.2.4 (14 Oct, 2026 per asset timestamps); v5.0.0-alpha.1 pre-release same day |
| Status | active (12,556 commits on main) |
| Licence + class | Business Source License 1.1, converts to Apache-2.0 at Change Date (see LICENSE) — source-available; hosted-offering restriction; legal-review trigger |
| Deployment | self-hosted binary/packages; air-gap viable (hypothesis) |
| Tier reason | ledger graph DB; credible counterexample to app-layer history |

Temporal, verifiable graph database with git-like branching and merging; RDF, SPARQL, JSON-LD, openCypher; integrated vector/text/geo search [CLAIM-fluree-01]. Relevant as a database-native bitemporal-ish graph with branching, closest to what EOIP builds in the application layer (CAP-34, CAP-35, CAP-02, CAP-15, CAP-14). BSL bars offering Fluree as a hosted DB, which matters for white-label SaaS; internals and claims not verified.
**Decision:** REFERENCE-ONLY — study branch/merge semantics; no dependency (BSL review).

| ID | Claim | Class | Source | Dates | Conf |
|---|---|---|---|---|---|
| CLAIM-fluree-01 | BSL 1.1; temporal, branching, SPARQL/openCypher; release v4.2.4 | Officially documented | https://github.com/fluree/db (+/releases) | 2026-10-26 | 0.8 (exact Change Date unread) |

### T-C13-lakefs — lakeFS

| Field | Value |
|---|---|
| Official URL | https://github.com/treeverse/lakeFS |
| Owner | Treeverse |
| Latest version + date | v1.88.0 (01 Oct; year not shown, 2026 inferred) |
| Status | active |
| Licence + class | BUSL-1.1; free for unmodified internal production use; each version becomes Apache-2.0 four years after release — source-available; legal-review trigger |
| Deployment | self-hosted over S3/Azure/GCS-compatible object store; air-gap viable with S3-compatible local store (hypothesis) |
| Tier reason | Git-for-object-store data versioning |

Branches and commits over data lake objects without copying, time travel, rollback, hooks gating publish [CLAIM-lakefs-01]. Relevant to versioning bulk source captures and evidence blobs, not graph semantics (CAP-35, CAP-74). BUSL redistribution constraints are a trigger for white-label bundling.
**Decision:** REFERENCE-ONLY — hook-gated publish pattern informs the validation gate; not bundled.

| ID | Claim | Class | Source | Dates | Conf |
|---|---|---|---|---|---|
| CLAIM-lakefs-01 | BUSL-1.1, 4-year Apache conversion, S3-compatible, branching/hooks; v1.88.0 | Officially documented | https://github.com/treeverse/lakeFS (+/releases) | 2026-10-26 | 0.8 |

### T-C13-table-time-travel — Apache Iceberg / Delta Lake time travel

| Field | Value |
|---|---|
| Official URL | https://iceberg.apache.org ; https://github.com/delta-io/delta |
| Owner | Apache Software Foundation (Iceberg); Delta Lake project under Linux Foundation |
| Latest version + date | Iceberg Java 1.12.0 (date unverified); Delta Lake 4.4.1 (05 Oct, year inferred 2026) |
| Status | active |
| Licence + class | Iceberg Apache-2.0 (ASF); Delta licence not shown in fetched page (believed Apache-2.0, conf 0.6) — permissive |
| Deployment | library/table formats on object store; air-gap viable |
| Tier reason | snapshot semantics reference |

Both keep immutable table snapshots / transaction logs enabling query-as-of-snapshot or version, rollback; Iceberg adds branching and tagging (docs navigation lists "Branching and Tagging") [CLAIM-ttt-01]. Relevant as design pattern for BL-38 snapshots and retention (snapshot expiry vs audit), CAP-34, CAP-35, CAP-74. Only transaction-time semantics, no valid time.
**Decision:** REFERENCE-ONLY — snapshot manifest and expiry design; possible Parquet export format (EXPERIMENT later).

| ID | Claim | Class | Source | Dates | Conf |
|---|---|---|---|---|---|
| CLAIM-ttt-01 | Iceberg 1.12.0 "Latest" with Branching and Tagging concept page; Delta 4.4.1 latest | Officially documented | https://iceberg.apache.org/releases/ ; https://github.com/delta-io/delta/releases | 2026-10-26 | 0.7; time-travel syntax not read |

### T-C13-spline — Spline

| Field | Value |
|---|---|
| Official URL | https://github.com/AbsaOSS/spline |
| Owner | ABSA OSS |
| Latest version + date | tag release/1.0.0-RC3 (2026-06-02); 0.8.6 (2025-11-18) |
| Status | active, pre-1.0 RC |
| Licence + class | Apache-2.0 — permissive |
| Deployment | Spark agent + server (self-hosted); air-gap viable (hypothesis) |
| Tier reason | Spark lineage capture |

Open-source lineage tracking for Apache Spark and similar frameworks with visualisation; Java 21 related [CLAIM-spline-01]. Relevant only as an upstream OpenLineage-adjacent producer pattern (CAP-40); EOIP has no Spark dependency. OpenLineage's Spark integration overlaps.
**Decision:** REFERENCE-ONLY.

| ID | Claim | Class | Source | Dates | Conf |
|---|---|---|---|---|---|
| CLAIM-spline-01 | Apache-2.0; lineage for Spark; tags through 1.0.0-RC3 | Officially documented | https://github.com/AbsaOSS/spline (+/tags) | 2026-10-26 | 0.85 |

### T-C13-aeong — AeonG-style temporal graph research

| Field | Value |
|---|---|
| Official URL | https://arxiv.org/abs/2304.12212 ; https://github.com/hououou/AeonG |
| Owner | Renmin Univ. of China with Waterloo, UNSW authors |
| Latest version + date | PVLDB vol. 17 no. 6 pp. 1515–1527 (2024); arXiv extended v2 |
| Status | research prototype |
| Licence + class | repository licence not shown on page: UNVERIFIED; code extends Memgraph (BSL-family licence of Memgraph not checked) — legal-review trigger |
| Deployment | research build; not for production |
| Tier reason | temporal property-graph storage research |

Built-in temporal support on a graph DB: hybrid storage (current store + historical store), native temporal query engine, anchor-based version retrieval; authors report up to 5.73x lower storage, 2.57x lower temporal latency, 9.74% overhead (vendor-of-paper claims, workload and hardware not extracted) [CLAIM-aeong-01]. Directly relevant to the design of efficient history in BL-37 (separate current vs historical layout, anchors) and CAP-65 temporal analytics.
**Decision:** REFERENCE-ONLY — adopt the current/historical split and anchor idea in an EXPERIMENT for bitemporal indexing; no code reuse before licence check.

| ID | Claim | Class | Source | Dates | Conf |
|---|---|---|---|---|---|
| CLAIM-aeong-01 | VLDB 2024; hybrid storage, anchor-based retrieval, reported speed/storage gains | Third-party report (paper abstract via search) | https://arxiv.org/pdf/2304.12212 | 2024 / 2026-10-26 | 0.7; full paper unread |
