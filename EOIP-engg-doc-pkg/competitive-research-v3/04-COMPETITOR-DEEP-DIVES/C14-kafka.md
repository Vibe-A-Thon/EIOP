# C14 Apache Kafka and Kafka Connect (Tier B)

| Field | Value |
|---|---|
| Registry ID | T-C14-kafka |
| Tier | B (event-bus option for BL-60) |
| Versions examined | 4.3.x (docs current; 4.3.2 tag 2026-10-20); 4.4.0 tag 2026-10-13 (docs not yet showing 4.4); 4.2.2 tag 2026-09-28 |
| Verified on | 2026-10-26 (brief: 2026-10-18; see Debezium note) |
| Worker | V27 |

## 1. Identity, current status, tier, and sources
Apache Kafka: ASF top-level project, distributed commit-log event streaming; Kafka Connect is the bundled integration framework. Licence Apache-2.0 (ASF standard; licence file not fetched this session, confidence 0.7) [CLAIM-kafka-04]. Kafka 4.0 removed ZooKeeper: "only supports KRaft mode"; 4.3 keeps this and ZooKeeper clusters must migrate first [CLAIM-kafka-02]. Brokers/Connect/tools need Java 17+, clients and Streams Java 11+ [CLAIM-kafka-02]. Active tags in Oct 2026 [CLAIM-kafka-01]. Sources: kafka.apache.org docs 4.3 (upgrade, Connect user guide), GitHub tags.

## 2. Problem, workloads, workflows
Durable, partitioned, replayable event log with consumer groups; Connect runs source/sink connectors with offset tracking. EOIP workflow: connectors publish `SourceEvent`s to `eoip.<tenant>.source` topics; an EOIP consumer applies them through the validation gate; poison events go to a DLQ topic. Relevant to BL-60 only when EOIP exceeds one node or a customer already runs Kafka.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| Partitioned replicated log, consumer groups, offsets, retention/compaction | present | documented concept; compaction advised for Connect topics [CLAIM-kafka-03] |
| KRaft controller quorum (no ZK) | present, only mode | [CLAIM-kafka-02] |
| Share groups ("Queues for Kafka", KIP-932): preview 4.1, production-ready 4.2 | present | [CLAIM-kafka-02] |
| Streams Rebalance Protocol production-ready core 4.2; bug fix in 4.2.1 | present | [CLAIM-kafka-02] |
| Connect REST API (port 8083): create/pause/resume/stop/restart, status, offsets view/reset/alter | present | [CLAIM-kafka-03] |
| Connect error handling: `errors.tolerance=none` default; `all` + `errors.deadletterqueue.topic.name` (+context headers); retry timeout | present (DLQ applies to sink connectors per KIP-298, reasoned 0.7) | [CLAIM-kafka-03] |
| Exactly-once source connectors (`exactly.once.source.support`), distributed mode only; connector-dependent | present | [CLAIM-kafka-03] |
| Transactions / idempotent producer / read_committed | present | consumer.isolation.level mentioned [CLAIM-kafka-03] |
| Tiered storage (KIP-1023 follow-up in 4.3) | present | [CLAIM-kafka-02] |
| ACLs per topic/principal; source-document ACL | topic ACLs present (not re-fetched); source ACL absent | inference [CLAIM-kafka-05] |
| Schema registry | not in Apache Kafka; separate (Confluent, not examined) | UNVERIFIED |

## 4. Architecture
```
 producers/Connect sources -> [Broker (KRaft combined or dedicated controllers)]
   topics -> partitions (leader+followers, ISR)  <- consumer groups (offsets in __consumer_offsets)
 Connect cluster (distributed): config.storage / offset.storage / status.storage topics
   workers rebalance tasks; REST :8083
```

## 5. Under-the-hood reconstruction
Log per partition: append-only segment files, sparse offset index, time index; replication leader->follower via ISR (hypothesis from general knowledge; not re-verified here). Metadata via KRaft Raft quorum replacing ZooKeeper [CLAIM-kafka-02]. Ordering guaranteed per partition only. Connect source offsets stored in `offset.storage.topic` (distributed) or local file (standalone), and the REST API can reset/alter them while stopped [CLAIM-kafka-03]. EOS source: connector offsets and records committed in one producer transaction (reasoned from docs, 0.7). Upgrade: rolling restart then `kafka-features.sh upgrade --release-version 4.3`; no metadata downgrade in 4.3.0 [CLAIM-kafka-02]. Security: SASL/TLS/ACLs (not re-fetched).

## 6. Requirements inferred
FR: ordered per-key delivery, consumer offset replay, DLQ, rate control via consumer pull/quotas (quota detail UNVERIFIED), backfill by offset reset. NFR: min 3 brokers for HA; JVM 17.

## 7. Performance and resource model
No benchmark gathered; vendor/community throughput figures not recorded (NOT PUBLICLY VERIFIED here). Footprint: a single KRaft combined-mode node is possible but production guidance prefers dedicated controllers (reasoned 0.6). JVM heap plus page cache; disk-bound. Failure modes: rebalance storms, under-replicated partitions, Connect task fail-fast.

## 8. Strengths
Mature replay (offset reset), consumer-group scaling, huge connector ecosystem via Connect, transactions, Apache-2.0 with ASF governance. EOIP match: BL-24 replay already exists in-process; exceeding Kafka means tenant-aware replay with ACL re-check at replay time.

## 9. Limitations
Algorithmic: per-partition ordering only; EOS is connector-dependent. Operational: JVM, 3-node HA, ops skill, Connect worker/topic sprawl; ZooKeeper migration burden for old clusters [CLAIM-kafka-02]. Developer friction: DLQ for source connectors not built in (reasoned), no native source-ACL, topic-per-tenant sprawl.

## 10. Deployment, licensing, viability
Apache-2.0 permissive; no legal trigger (confirm licence file). Air-gap yes. One-node: heavy relative to SQLite-backed `DurableJobStore`. As optional adapter behind an event-bus port: viable.

## 11. Delta vs baseline
BL-60 Absent at HEAD (01a confirms; string mentions only). BL-52 in-process streaming implemented. BL-24 implemented plus `packages/eoip/jobs.py` `DurableJobStore` (lease, fencing token, outbox, governed DLQ, `replay_dlq`) observed at HEAD in code, not in 01a. Kafka adds multi-process fan-out and long retention EOIP lacks; EOIP has tenant-governed DLQ that Kafka DLQ topics lack.

## 12. Cards
STR-kafka-01 | Kafka | offset-based replay/rewind per consumer group | CLAIM-kafka-03 | audit replay, reindex after ontology change | match | `replay(from_checkpoint)` already in `ingestion/replay.py`; add bus-port | test: replay 1M events, state identical hash.
INV-kafka-01 | Kafka 4.3 | too heavy for one-node/air-gap appliance (JVM + quorum) [hypothesis] | cause: deployment. A: optional Kafka adapter; B: bus port with SQLite/outbox default; C: tenant-aware log with ACL re-check. Select B. Worse when >1 node fan-out needed. POC: ingest 10k events/s on 4 vCPU, compare p99 vs Kafka single node. Decision EXPERIMENT (port defined; Kafka as one adapter). Defensibility: ACL-aware replay.

## 13. Decisions
CAP-26/27 external bus: DEFER (port + Kafka adapter when customer requires); Connect as connector host: REJECT (EOIP connectors never mutate graph; Connect sinks would); CAP-36: REUSE log concepts; CAP-50: Kafka viable but heavy.

## 14. Tests
Bus port contract tests; 3 failure injections (broker kill, consumer crash mid-batch, poison record). Acceptance: no loss, dedupe by event id, DLQ record carries tenant and reason. PROPOSED.

## 15. Risks / questions
4.4.0 tagged but docs show 4.3: confirm GA status. Topic-per-tenant limits unverified. Confluent-licensed components must be excluded (Confluent Community License, UNVERIFIED).

## Appendix A. Dimension coverage
| D | Sections | Summary |
|---|---|---|
| D1 | 1 | ASF, Apache-2.0 |
| D2 | 2 | event backbone |
| D3 | 4 | broker, Connect |
| D4-D7,D12-D14,D16,D19 | N/A | not graph/query/ML/UX |
| D8 | 5,7 | per-partition order, replication, EOS |
| D9 | 3,5 | connectors, offsets, DLQ |
| D10 | 9 | no source ACL |
| D11 | 5 | replay |
| D15,D17 | 3 | REST/CLI |
| D18 | 5 | SASL/TLS/ACL (not re-fetched) |
| D20 | 7 | no numbers |
| D21 | 10 | permissive |
| D22 | 13 | wire protocol widely emulated |
| D23 | N/A | none |
| D24 | App. C | docs |

## Appendix B. Capability mapping
| CAP | Kafka | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-26 | plugin (Connect) | 03 | BL-23 Impl | DEFER | P3 |
| CAP-27 | native | 03 | BL-24 Impl | REUSE patterns | P2 |
| CAP-36 | native | 03 | BL-52 Impl in-process | DEFER | P3 |
| CAP-46 | absent | 05 | BL-18 | BUILD | P1 |
| CAP-47 | partial (topic ACLs) | 05 | BL-20 Partial | BUILD | P1 |
| CAP-05 | native | 02 | BL-60 Absent | DEFER | P3 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| kafka-01 | 4.x tags | 4.3.2 (2026-10-20), 4.4.0 (10-13), 4.2.2 (09-28) | Officially documented | https://github.com/apache/kafka/tags | acc 2026-10-26 | 0.85 | docs site shows 4.3 current |
| kafka-02 | 4.3 | KRaft-only, Java 17/11, share groups prod 4.2, upgrade path | Officially documented | https://kafka.apache.org/43/getting-started/upgrade/ | acc 2026-10-26 | 0.85 | none |
| kafka-03 | 4.3 | Connect DLQ, EOS source, offsets, REST, distributed topics | Officially documented | https://kafka.apache.org/43/kafka-connect/user-guide/ | acc 2026-10-26 | 0.85 | none |
| kafka-04 | n/a | Apache-2.0 | Reasoned inference | ASF standard; licence file not fetched | acc 2026-10-26 | 0.7 | none |
| kafka-05 | n/a | no source-ACL concept; topic ACLs exist | Reasoned inference | n/a | n/a | 0.5 | n/a |

## Appendix D. Assumptions
Kafka is considered only as an optional adapter behind a bus port. Rate-limit/quota behaviour not verified in this session.
