# C14 Tier C records (V27)

Verified 2026-10-26. Context: EOIP baseline BL-23 (SourceEvent capture, connectors never mutate the graph), BL-24 (replay/DLQ/dedupe/checkpoints; HEAD adds `packages/eoip/jobs.py` DurableJobStore), BL-52 (in-process streaming), BL-60 (no external bus).

### T-C14-redpanda — Redpanda and Redpanda Connect (Benthos)
| Field | Value |
|---|---|
| Official URL | https://github.com/redpanda-data/redpanda ; https://github.com/redpanda-data/connect |
| Owner | Redpanda Data, Inc. |
| Latest | Redpanda v26.2.2 (2026-08-19), v26.1.17 (2026-08-19); Connect v4.115.1 (2026-10-23) |
| Status | active |
| Licence | Redpanda core: Business Source License 1.1 (Additional Use Grant bars a "Streaming or Queueing Service"; Change Date 4 years per version, Change License Apache-2.0); Enterprise features: Redpanda Community License (fees, no streaming service, usage data sharing, patent termination). Connect: "Apache V2" free bundle and separate "Enterprise" bundle. Class: source-available (core), mixed (Connect) |
| Deployment | self-hosted, docker, k8s, managed cloud |
| Air-gap | partial (enterprise licence keys, usage-data clause unverified for offline) |
| Tier reason | Kafka-compatible |

Kafka-API-compatible C++ broker with no JVM/ZooKeeper; Connect is the former Benthos stream processor (single static binary; Go plugin API under `redpanda-data/benthos/v4`; cgo components such as zmq4 off by default, `x_benthos_extra` tag) [CLAIM-redpanda-01..03]. For EOIP the Connect free bundle is an attractive lightweight source-to-webhook/NATS pipeline tool with retries and DLQ-like routing (feature depth not verified). Core BSL and RCL are legal-review triggers (redistribution as embedded product vs "streaming service" clause). CAPs: 26, 27, 04, 77.
**Decision:** EXPERIMENT Connect free (Apache) bundle as optional ingestion sidecar; REJECT embedding Redpanda core; DEFER broker.
| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| redpanda-01 | BSL 1.1 parameters as above | Officially documented | https://raw.githubusercontent.com/redpanda-data/redpanda/dev/licenses/bsl.md (acc 2026-10-26) | 0.85 |
| redpanda-02 | RCL terms (2(d), 4, 5, 6, 14) | Officially documented | https://raw.githubusercontent.com/redpanda-data/connect/main/licenses/rcl.md | 0.8 |
| redpanda-03 | Connect free (Apache V2) vs enterprise bundle; tags v4.115.1 | Officially documented | https://github.com/redpanda-data/connect (+tags) | 0.7; per-connector bundle membership unverified |

### T-C14-flink — Apache Flink
| Field | Value |
|---|---|
| Official URL | https://flink.apache.org |
| Owner | Apache Software Foundation |
| Latest | Flink 2.3.0 (2026-06-25); Flink CDC 3.7.0 (date not shown; works with Flink 1.20.x/2.2.x) |
| Status | active |
| Licence | Apache-2.0 (ASF standard; file not fetched, 0.7); permissive |
| Deployment | self-hosted, k8s, standalone |
| Air-gap | yes |
| Tier reason | Stream processing |

Distributed stateful stream processor with checkpointing and exactly-once state semantics (general knowledge, 0.6); Flink CDC embeds Debezium-style log capture. Relevant only for very high-volume windowed enrichment; JVM cluster is far outside one-node-first. Overlaps BL-52 only conceptually. CAPs: 26, 27, 05, 22 (incremental).
**Decision:** DEFER; REFERENCE-ONLY for checkpoint-barrier design.
| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| flink-01 | 2.3.0 on 2026-06-25; CDC 3.7.0 | Officially documented | https://flink.apache.org/downloads/ (acc 2026-10-26) | 0.8 |

### T-C14-nifi — Apache NiFi
| Field | Value |
|---|---|
| Official URL | https://nifi.apache.org |
| Owner | Apache Software Foundation |
| Latest | 2.12.0 (2026-09-13) |
| Status | active |
| Licence | Apache-2.0 (ASF standard, not file-verified, 0.7); permissive |
| Deployment | self-hosted, docker, k8s |
| Air-gap | yes |
| Tier reason | Flow-based ingestion |

Visual dataflow engine with provenance, back-pressure, prioritised queues and many processors (general knowledge, 0.6). Strong for file/SFTP/legacy ingestion with per-record provenance; JVM and UI-centric configuration conflict with GitOps-as-code and one-node footprint. Could run as customer-side collector posting to EOIP webhooks. CAPs: 26, 27, 40.
**Decision:** INTEGRATE optionally (customer-run, webhook sink); REFERENCE-ONLY for provenance UX.
| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| nifi-01 | 2.12.0 on 2026-09-13 | Officially documented | https://nifi.apache.org/download/ | 0.8 |

### T-C14-seatunnel — Apache SeaTunnel
| Field | Value |
|---|---|
| Official URL | https://seatunnel.apache.org |
| Owner | Apache Software Foundation |
| Latest | GitHub tags: v3.0.0 (2026-09-23); download page lists v3.0.0 dated 2026-09-29; prior 2.3.13 (2026-02-18) |
| Status | active; date discrepancy of 6 days between sources, a web search summary found no 3.0.0 announcement |
| Licence | Apache-2.0 (ASF standard, not file-verified, 0.7); permissive |
| Deployment | self-hosted, Zeta engine, can use Flink/Spark |
| Air-gap | yes |
| Tier reason | Data integration |

Batch and CDC data-integration engine with its own Zeta engine and many connectors (general knowledge, 0.5). Overlaps Airbyte/Debezium with a fully Apache-licensed catalogue, which makes it the lowest-licence-risk connector-breadth option; maturity of 3.0.0 unverified. CAPs: 26, 6.
**Decision:** EXPERIMENT as permissive connector source for SourceEvent sinks.
| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| seatunnel-01 | v3.0.0 2026-09-23 (tags) / 2026-09-29 (download page) | Officially documented | https://github.com/apache/seatunnel/tags ; https://seatunnel.apache.org/download | 0.6 |

### T-C14-orchestrators — Dagster, Airflow, Prefect
| Field | Value |
|---|---|
| Official URL | https://dagster.io ; https://airflow.apache.org ; https://www.prefect.io |
| Owner | Dagster Labs ; ASF ; Prefect Technologies |
| Latest | Dagster 1.13.26 (2026-10-09); Airflow 3.3.2 (2026-09-17); Prefect 3.9.0 (2026-10-21) |
| Status | active (all) |
| Licence | Dagster Apache-2.0 (LICENSE fetched); Prefect Apache-2.0 (fetched); Airflow Apache-2.0 (ASF, not file-verified); permissive. Managed offerings (Dagster+, Prefect Cloud, Astronomer) are commercial and not examined |
| Deployment | self-hosted, docker, k8s, managed cloud |
| Air-gap | yes (self-hosted, Python packages mirrored) |
| Tier reason | Batch orchestration |

Python schedulers/DAG runners with retries, backfills and sensors (Dagster adds asset-oriented lineage; general knowledge, 0.6). They orchestrate crawls, not capture events; EOIP already has scheduling and `DurableJobStore`. Customers with an existing Airflow could call EOIP APIs. Heavy metadata DB and webserver for one-node. CAPs: 26, 27, 40 (Dagster asset lineage), 75.
**Decision:** REFERENCE-ONLY (Dagster asset-lineage model, backfill partitions); INTEGRATE as customer-side caller only.
| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| orch-01 | Dagster Apache-2.0, 1.13.26 | Observed licence + tags | https://raw.githubusercontent.com/dagster-io/dagster/master/LICENSE ; https://github.com/dagster-io/dagster/tags | 0.9 |
| orch-02 | Prefect Apache-2.0, 3.9.0 | Observed licence + tags | https://raw.githubusercontent.com/PrefectHQ/prefect/main/LICENSE ; https://github.com/PrefectHQ/prefect/tags | 0.9 |
| orch-03 | Airflow 3.3.2 (2026-09-17) | Officially documented | https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html | 0.75 |

### T-C14-dlt-meltano — dlt, Meltano/Singer, Apache Hop
| Field | Value |
|---|---|
| Official URL | https://github.com/dlt-hub/dlt ; https://github.com/meltano/meltano ; https://hop.apache.org |
| Owner | dltHub (ScaleVector copyright) ; Arch Data, Inc. ; ASF |
| Latest | dlt 1.31.0 (2026-10-07); Meltano v4.4.1 (2026-10-07); Hop 2.19.0-rc1 (2026-08-12 tag; release candidate only seen) |
| Status | active |
| Licence | dlt Apache-2.0 (fetched); Meltano MIT (fetched); Hop Apache-2.0 (ASF, not file-verified); Singer spec/taps: licences vary per tap, UNVERIFIED. Permissive for the three tools |
| Deployment | embedded Python library (dlt), CLI (Meltano), desktop/server (Hop) |
| Air-gap | yes |
| Tier reason | ELT tooling |

dlt is an embeddable Python pipeline library (schema inference, incremental state, load packages; general knowledge, 0.5) and the closest fit for in-process, one-node connector authoring that emits `SourceEvent`s; Meltano wraps Singer taps/targets (huge long-tail catalogue with per-tap licence variance, so a licence gate is needed); Hop is a Java visual ETL (Kettle lineage). CAPs: 26, 28, 04.
**Decision:** EXPERIMENT dlt as connector-authoring option and its incremental-state pattern; REUSE Singer message shape only after licence check; REFERENCE-ONLY Hop.
| ID | Claim | Class | Source | Conf |
|---|---|---|---|---|
| dlt-01 | dlt Apache-2.0, 1.31.0 | Observed licence + tags | https://raw.githubusercontent.com/dlt-hub/dlt/devel/LICENSE.txt ; https://github.com/dlt-hub/dlt/tags | 0.9 |
| dlt-02 | Meltano MIT, v4.4.1 | Observed licence + tags | https://raw.githubusercontent.com/meltano/meltano/main/LICENSE ; https://github.com/meltano/meltano/tags | 0.9 |
| dlt-03 | Hop tags 2.19.0-rc1 newest | Officially documented | https://github.com/apache/hop/tags | 0.6; GA release not seen |
