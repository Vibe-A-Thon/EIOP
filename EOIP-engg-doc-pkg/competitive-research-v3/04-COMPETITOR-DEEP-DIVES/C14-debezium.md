# C14 Debezium (Tier B)

| Field | Value |
|---|---|
| Registry ID | T-C14-debezium |
| Tier | B (CDC reference; enabling technology, not a graph DB) |
| Versions examined | 3.7.0.Final (2026-09-29, "latest stable"); 3.6.3.Final (2026-09-18); 3.5.2.Final (2026-06-02) |
| Verified on | 2026-10-26 (brief said 2026-10-18; web evidence includes tags dated up to 2026-10-25, so the real access date is recorded) |
| Worker | V27 |

## 1. Identity, current status, tier, and sources
Debezium (debezium.io, Red Hat-sponsored community project) is a CDC platform that reads database transaction logs and emits row-level change events. Active: five 3.x minor lines released in 2026 [CLAIM-debezium-01]. Licence Apache-2.0 (LICENSE.txt) [CLAIM-debezium-02]. Three runtimes: Kafka Connect source connectors; Debezium Server (standalone, "without requiring Apache Kafka"); embedded Engine library; plus Debezium Platform (Kubernetes-managed pipelines) [CLAIM-debezium-03]. Sources: debezium.io/releases, GitHub tags, PostgreSQL connector reference, Debezium Server reference. Tier B: it is the reference design for BL-23/BL-24-style capture, but it is not a candidate EOIP dependency by default.

## 2. Problem, workloads, workflows
Low-latency, log-based capture of inserts/updates/deletes from operational databases without polling or dual writes. EOIP workflow: a customer's PostgreSQL/Oracle/SQL Server system of record changes; a Debezium connector emits events; an EOIP adapter converts each to a `SourceEvent` (BL-23) which goes through validation gate and replay/DLQ (BL-24) before any graph mutation. Also outbox-pattern capture for application-emitted events.

## 3. Feature inventory
| Feature | Status | Surface |
|---|---|---|
| Connectors (3.7): Cassandra 4/5, CockroachDB, Db2 (+IBM i), Informix, Ingres, MariaDB, MongoDB, MySQL, Oracle, PostgreSQL, Spanner, SQL Server, SQLite, TiDB, Vitess, YashanDB, plus JDBC and Milvus sinks [CLAIM-debezium-03] | present | Connect plugins |
| Initial snapshot modes (initial, always, initial_only, no_data, when_needed, configuration_based, custom) [CLAIM-debezium-04] | present | config |
| Incremental (chunked, watermark, resumable) snapshots via signal table or Kafka signal topic; stop-snapshot; per-table `additional-conditions` filter; read-only mode on PG13+ [CLAIM-debezium-04] | present | signalling |
| Transaction boundary events (BEGIN/END, txID:LSN) [CLAIM-debezium-04] | present | topic |
| Server sinks: Kafka, Pulsar, Kinesis, Pub/Sub, Event Hubs, NATS JetStream, RabbitMQ, Redis Stream, HTTP (JWT/OAuth/Standard Webhooks), Iceberg, JDBC, Milvus, Qdrant [CLAIM-debezium-05] | present | Server |
| Offset stores: file (default), memory, JDBC, Redis; schema history: Kafka, file, memory, Redis, Azure Blob etc. [CLAIM-debezium-05] | present | Server |
| DDL capture under logical decoding (PostgreSQL) | absent: logical decoding does not report DDL [CLAIM-debezium-04] | |
| Source ACL / row-security propagation | absent (inference) [CLAIM-debezium-07] | |
| UI | partial: Debezium Platform UI (not examined) | UNVERIFIED |

## 4. Architecture
```
 source DB --(WAL/binlog/redo, slot/LSN)--> [Connector task] --> [Converter] --> Kafka topic per table (+ .transaction topic)
                                                  |  offsets: Connect offsets topic | Server: file/JDBC/Redis
                                                  |  schema history topic/store
 Signal table / signal topic --> incremental snapshot chunks (watermarked, interleaved with stream)
 Debezium Server: same engine -> sink (NATS JetStream | HTTP | Kafka ...), no Kafka cluster
```

## 5. Under-the-hood reconstruction
Data model: envelope `{before, after, source{lsn, txId, ts}, op, ts_ms, transaction}` keyed by primary key. Offsets: the LSN (PostgreSQL) of last recorded event; on restart the connector resumes from it [CLAIM-debezium-04]. Ordering: preserved per source as written by Connect; per-key ordering follows from keyed partitioning (inference). Incremental snapshot algorithm (documented): split table into PK chunks (default 1024 rows), open/close watermarks in the log, drop chunk rows superseded by log events inside the window, so snapshot and stream interleave without locks [CLAIM-debezium-04]. Delivery semantics: at-least-once (consumers must dedupe on key+LSN) [CLAIM-debezium-07, reasoned inference, 0.6]. Security: relies on DB credentials and sink/transport TLS; no per-row ACL. Pseudocode for an EOIP-compatible adapter: `event -> SourceEvent(source_ref=f"{db}/{table}/{pk}", revision=lsn, op, payload_hash)`; dedupe key = (connector, lsn, pk) -> existing webhook-dedupe path (BL-24).

## 6. Requirements inferred
FR: log-position checkpoint; resumable backfill concurrent with streaming; delete events and tombstones; transaction grouping. NFR: source-DB privileges (replication role), WAL retention growth risk when a slot lags (reasoned inference, well-known operational hazard, not re-fetched), JVM 17+ (Server/Operator/Outbox 21+) [CLAIM-debezium-03].

## 7. Performance and resource model
No benchmark examined; NOT PUBLICLY VERIFIED for throughput. Footprint: a JVM per connector worker or a Debezium Server process; with file offset store and HTTP/NATS sink, no Kafka needed (single process). Failure modes: slot/WAL backlog, schema change mid-incremental-snapshot unsupported [CLAIM-debezium-04], snapshot duplicates in blocking snapshots.

## 8. Strengths
Best-in-class log-based CDC across many databases; resumable chunked backfills; transaction metadata; Server mode decouples from Kafka; Apache-2.0. Matching: EOIP can reuse the watermark-window algorithm for its own incremental crawls.

## 9. Limitations
Algorithmic: at-least-once only; DDL invisibility on PG logical decoding. Operational: JVM, replication-slot lag, DB privileges, per-connector snapshot locking behaviour (UNVERIFIED per connector). Developer friction: change events are table-shaped, not entity-shaped; mapping to ontology is entirely the consumer's work. No source-ACL concept.

## 10. Deployment, licensing, operational viability
Apache-2.0, redistribution-safe; no legal trigger. Air-gap: yes (Server + file offsets + NATS JetStream or HTTP sink, all local) [CLAIM-debezium-05]. One-node: feasible (one JVM). Connector JDBC drivers for Oracle/Db2/Informix carry their own licences (UNVERIFIED; legal review trigger limited to those drivers).

## 11. Competitive delta vs baseline
BL-23: EOIP has connectors that capture `SourceEvent`s but no log-based CDC connector (none verified); BL-24: EOIP has checkpoints/replay/DLQ at HEAD, now also `packages/eoip/jobs.py` `DurableJobStore` (SQLite WAL, lease + fencing token, outbox, governed DLQ) which 01a does not discuss; observed in code, not re-audited. BL-60: Debezium Server can feed NATS JetStream/HTTP without Kafka, so adopting it does not force an external bus. BL-52 unaffected.

## 12. Cards
STR-debezium-01 | Debezium | watermark-based incremental snapshot interleaved with the log | CLAIM-debezium-04 | consistent backfill without source locks | match | implement watermark-window dedupe in EOIP crawl checkpoint | test: update rows during backfill, final state equals source, zero lost updates.
STR-debezium-02 | Debezium | Server mode with pluggable sink/offset store | CLAIM-debezium-05 | no-Kafka one-node CDC | integrate | run Server to HTTP sink hitting EOIP webhook endpoint | test: kill -9 Server, restart, no gaps, duplicates absorbed by webhook dedupe.
INV-debezium-01 | Debezium 3.7 | no source-ACL propagation; row-level security not carried [CLAIM-debezium-07, hypothesis] | cause: semantics/governance (hypothesis). Option A: connector config maps table-level ACL to `SourceEvent.acl`; B: native ACL join from source RLS policy tables; C: ACL-change events as first-class SourceEvents. Select A+B for DB sources. Mitigation worse when source ACL is application-level. POC: 3-user table with RLS, assert retrieval filters. Defensibility: ACL-aware CDC mapping. Decision EXPERIMENT. Seed hypotheses in Master Prompt 10.5: none target Debezium.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-26 DB CDC connector | INTEGRATE (optional, Debezium Server -> EOIP webhook/NATS); never as graph writer |
| CAP-27 replay/DLQ | REJECT as dependency; EOIP native is adequate |
| CAP-36 event history | REUSE envelope concepts |
| Incremental backfill algorithm | BUILD (watermark pattern) |

## 14. Tests/POC
PG container + Debezium Server file offsets -> HTTP sink -> EOIP webhook; check dedupe, crash resume, backfill under writes, delete -> tombstone (BL-25). Acceptance: zero lost, no direct graph mutation. PROPOSED.

## 15. Risks / open questions
WAL growth on lagging slot; Oracle licensing of LogMiner/XStream (UNVERIFIED); how to carry tenant_id (topic prefix vs header); schema-history store for Server in air-gap (file is available).

## Appendix A. Dimension coverage
| Dimension | Covered in | Summary |
|---|---|---|
| D1-D3 | 1,3,4,10 | Active, Apache-2.0, Connect/Server/Engine |
| D8-D11 | 5,7 | at-least-once, per-source order, snapshots, offsets, replay |
| D18,D20,D21,D22 | 5,7,10 | DB creds/TLS, no numbers, permissive, portable envelope |
| D4-D7,D12-D17,D19,D23 | N/A | enabling technology; no storage, query, reasoning, ML, UX, tenancy or patents identified |
| D24 | App. C | official docs, partially read |

## Appendix B. Capability mapping
| CAP | Native? | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-26 | native | 03 | BL-23 Implemented (no log CDC) | INTEGRATE | P2 |
| CAP-27 | partial | 04,05 | BL-24 Implemented | REUSE patterns | P3 |
| CAP-36 | partial | 04 | BL-25 | REUSE | P3 |
| CAP-46 | absent | 07 | BL-18 Absent/partial | BUILD mapping | P1 |
| CAP-50 | native | 05 | n/a | INTEGRATE | P2 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| debezium-01 | 3.7.0.Final 2026-09-29 | latest tags 3.7.0, 3.6.3, 3.6.2, 3.6.1, 3.6.0 | Officially documented | GitHub tags https://github.com/debezium/debezium/tags | acc 2026-10-26 | 0.9 | GitHub Releases page empty |
| debezium-02 | main | LICENSE.txt is Apache-2.0 | Observed (licence file) | https://raw.githubusercontent.com/debezium/debezium/main/LICENSE.txt | acc 2026-10-26 | 0.9 | none |
| debezium-03 | 3.7 | connector list; Java 17+/21+; Kafka Connect 3.1+; Server/Platform/Engine | Officially documented | https://debezium.io/releases/ | acc 2026-10-26 | 0.85 | page orders some dates oddly |
| debezium-04 | PG connector stable | snapshot modes, incremental snapshots, LSN offsets, ordering, txn metadata, no DDL | Officially documented | https://debezium.io/documentation/reference/stable/connectors/postgresql.html | acc 2026-10-26 | 0.85 | read only first 100k chars |
| debezium-05 | Server stable | sinks, offset and schema-history stores | Officially documented | https://debezium.io/documentation/reference/stable/operations/debezium-server.html | acc 2026-10-26 | 0.85 | licence not on page |
| debezium-06 | n/a | reserved: not used | n/a | n/a | n/a | n/a | n/a |
| debezium-07 | n/a | at-least-once delivery; no ACL propagation; WAL lag hazard | Reasoned inference | n/a | n/a | 0.6 | not re-fetched |

## Appendix D. Assumptions
Brief date 2026-10-18 superseded by actual access 2026-10-26. Adapter would be written by EOIP; Debezium is never a graph writer.
