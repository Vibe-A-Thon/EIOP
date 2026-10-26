# Cohort 16 — Ingestion, CDC and Streaming

| Field | Value |
|---|---|
| Cohort ID | 16-INGESTION-CDC-STREAMING |
| Workload class | Source capture, CDC, event transport, durable jobs and orchestration feeding EOIP's `SourceEvent` pipeline (CAP-26, CAP-27, CAP-36, CAP-04, CAP-05, CAP-46, CAP-50, CAP-77) |
| Members (deep dives) | [Debezium](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md), [Apache Kafka / Connect](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md), [NATS / JetStream](../04-COMPETITOR-DEEP-DIVES/C14-nats.md), [Airbyte](../04-COMPETITOR-DEEP-DIVES/C14-airbyte.md), [Temporal](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md) |
| Members (Tier C, V27) | [C14-tier-c-records-V27](../04-COMPETITOR-DEEP-DIVES/C14-tier-c-records-V27.md): Redpanda and Redpanda Connect, Flink / Flink CDC, NiFi, SeaTunnel, Dagster / Airflow / Prefect, dlt / Meltano / Hop |
| Reference columns | HugeGraph, Neo4j, Neptune: **not applicable** (graph stores, not ingestion engines; none of their deep dives is a CDC product). Shown only where a CAP touches the store |
| EOIP baseline | BL-17, BL-23, BL-24, BL-25, BL-52, BL-60 ([01-SYSTEM-BASELINE](../01-SYSTEM-BASELINE.md)); HEAD 896e06d per [01a](../01a-BASELINE-DELTA-HEAD.md): NB-06 (new connectors), NB-03 (ActionEngine), BL-18 (source ACL) |
| Additional HEAD evidence (not in 01a) | `packages/eoip/jobs.py` `DurableJobStore`, read for this cohort (see §1.3). Cited below as **JOBS-HEAD** |
| Pending research | none: all five C14 deep dives and V27 exist. Note the V27 Tier C file has one claim table per product (e.g. `redpanda-01..03`), not a deep dive |
| Date | 2026-10-26 |

## 1. Workload class and comparison basis

### 1.1 Workloads served
(a) Log-based CDC from customer operational databases (Postgres, Oracle, SQL Server) into `SourceEvent`s; (b) scheduled/incremental SaaS and API extraction (Jira, Salesforce class); (c) durable intra-platform job execution with retry, DLQ and replay; (d) optional scale-out event transport once a deployment outgrows one node; (e) multi-step workflow state (ontology releases, DSAR erasure, governed write-backs).

### 1.2 Why comparable, and who is excluded
The five deep-dive members are **not substitutes for each other**; they occupy different layers. Comparison is by the CAPs they would serve in EOIP, not by feature parity:

| Layer | Members | Role relative to EOIP |
|---|---|---|
| Capture | Debezium; Airbyte; (Tier C) SeaTunnel, dlt, Meltano, NiFi, Redpanda Connect | Produce records; EOIP adapter turns them into `SourceEvent` (BL-23: connectors never write the graph) |
| Transport | Kafka, NATS JetStream; (Tier C) Redpanda | Durable ordered log between capture and EOIP pipeline (BL-60 absent) |
| Durable execution | Temporal; (Tier C) Dagster/Airflow/Prefect, Flink | Job and workflow state (overlaps `DurableJobStore`) |

Excluded: graph databases and virtualisation engines (cohorts 01, 02); process-mining platforms. Flink, NiFi and the orchestrators are Tier C reference points only: records carry confidence 0.5-0.7 "general knowledge" content and are not used for hard comparisons below (V27 Tier C, `flink-01`, `nifi-01`, `orch-01..03`).

### 1.3 EOIP's own pipeline at HEAD (JOBS-HEAD, observed by code reading)
01a does not cover `packages/eoip/jobs.py` (598 lines). Reading it for this cohort: `DurableJobStore` is a SQLite store opened with `PRAGMA journal_mode = WAL` (`jobs.py:64`) with tables `jobs`, `job_outbox`, `governed_dlq`. It provides atomic claim or lease reclaim with an incremented **fencing token** (`claim_job`, :166), heartbeat (:231), checkpoint (:256), commit with **transactional outbox rows written in the same transaction** (`commit_job`, :279), failure handling that moves poison, non-idempotent or retry-exhausted jobs to a **governed DLQ** with secret redaction (`fail_job`, :334), cancel with fencing (:416), and `replay_dlq` requiring a replay authority and rejecting cross-tenant access (:443). `tests/integration/test_durable_jobs.py` has seven tests (claim race, lease expiry/fencing, outbox, redaction + DLQ, cancel fences worker, DLQ replay with audit authority, cross-tenant claim isolation); I did not run them. **Library-only caveat:** grep finds `DurableJobStore` referenced only by `jobs.py` and that test; nothing in `apps/` constructs it. There is also no outbox relay (only `list_outbox`, :529): nothing publishes the outbox rows. A separate `JobQueue` class (:537) is the file-backed legacy path. File-captured replay lives in `ingestion/replay.py` (FR-CONN-006) with dedupe by event id plus payload hash (BL-24).

## 2. Capability comparison

Legend: native / partial / plugin / enterprise-only / absent / unknown. Cell evidence is a CLAIM-ID; "reasoned" marks claims the deep dive itself labels as inference (confidence stated). EOIP cells cite BL/NB at HEAD.

| CAP | Debezium | Kafka (+Connect) | NATS JetStream | Airbyte | Temporal | EOIP @HEAD |
|---|---|---|---|---|---|---|
| CAP-26 connectors and CDC | **native** log-based CDC for ~16 DBs ([CLAIM-debezium-03](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | plugin via Connect, ecosystem breadth not enumerated ([CLAIM-kafka-03](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | absent as a connector framework; Debezium Server can sink to it ([CLAIM-debezium-05](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | native for SaaS/DB catalogue, CDC for selected DBs unverified (reasoned, 0.4: [CLAIM-airbyte-06](../04-COMPETITOR-DEEP-DIVES/C14-airbyte.md)) | absent (activities are user code) | BL-23 Implemented; NB-06 client connectors, live-unverified; no log-based CDC connector found |
| CAP-27 idempotent log, replay, DLQ | partial: per-source order, offset resume; at-least-once only (reasoned 0.6: [CLAIM-debezium-07](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | native: offsets, reset; Connect DLQ via `errors.deadletterqueue.topic.name` ([CLAIM-kafka-03](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)); source-connector DLQ not built in (reasoned) | partial: replay by sequence/time, ack redelivery ([CLAIM-nats-03](../04-COMPETITOR-DEEP-DIVES/C14-nats.md)); no native DLQ ([CLAIM-nats-05](../04-COMPETITOR-DEEP-DIVES/C14-nats.md), 0.5) | partial: STATE checkpoint model (reasoned, [CLAIM-airbyte-06](../04-COMPETITOR-DEEP-DIVES/C14-airbyte.md)); DLQ absent (reasoned 0.4) | partial: event history replay ([CLAIM-temporal-04](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md)); replication DLQ unverified | BL-24 Implemented; JOBS-HEAD: leases, fencing, outbox, governed DLQ with authority-gated replay (library-only) |
| Exactly-once | absent: at-least-once (reasoned 0.6, [CLAIM-debezium-07](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | partial: EOS source connectors, distributed mode only, connector-dependent ([CLAIM-kafka-03](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | absent as guarantee; dedupe window pattern (0.5, [CLAIM-nats-05](../04-COMPETITOR-DEEP-DIVES/C14-nats.md)) | absent (at-least-once, reasoned) | partial: activities at-least-once, determinism for workflows ([CLAIM-temporal-04](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md)) | idempotent apply by event id + payload hash (BL-24); effectively-once, not transport EOS |
| CAP-36 event history | partial: envelope with LSN, txId ([CLAIM-debezium-04](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | native log retention/compaction ([CLAIM-kafka-03](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | native within stream limits ([CLAIM-nats-03](../04-COMPETITOR-DEEP-DIVES/C14-nats.md)) | absent | native event history ([CLAIM-temporal-04](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md)) | BL-25 tombstones; raw SourceEvent capture on disk; no unified history |
| CAP-46 source-ACL propagation | absent (reasoned/hypothesis, [CLAIM-debezium-07](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | absent; topic ACLs only (reasoned 0.5, [CLAIM-kafka-05](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | absent ([CLAIM-nats-05](../04-COMPETITOR-DEEP-DIVES/C14-nats.md)) | unknown ([CLAIM-airbyte-06](../04-COMPETITOR-DEEP-DIVES/C14-airbyte.md)) | absent (N/A) | BL-17 captures `PermissionMetadata`/`acl_hash`; BL-18 Partial (not applied on deployed retrieval paths, 01a) |
| CAP-47 tenant isolation of transport | n/a | partial: topic ACLs, topic-per-tenant limits unverified ([CLAIM-kafka-05](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | unknown: accounts model believed, unverified ([CLAIM-nats-06](../04-COMPETITOR-DEEP-DIVES/C14-nats.md), 0.3) | unknown | partial: namespaces ([CLAIM-temporal-05](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md)) | BL-20 Partial; JOBS-HEAD tenant-scoped claim and DLQ replay (tested); event topics tenant-scoped in `TenantLayers` |
| CAP-04 one-node footprint | native: Server mode, one JVM, file offsets ([CLAIM-debezium-05](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | partial: combined mode possible, prod guidance prefers dedicated controllers (reasoned 0.6, section 7) | native: single Go binary (reasoned; footprint not measured) | absent as design centre (container per sync, reasoned, unverified) | partial: dev server one binary; production needs SQL DB, multiple services ([CLAIM-temporal-05](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md)) | native: SQLite WAL, no external service (JOBS-HEAD) |
| CAP-05 scale-out | partial (via Connect/Kafka) | native ([CLAIM-kafka-02](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | native replication, Raft detail unverified ([CLAIM-nats-03](../04-COMPETITOR-DEEP-DIVES/C14-nats.md)) | unknown | native sharded services (reasoned 0.5) | BL-60 Absent; BL-52 in-process only |
| CAP-50 air-gap | native ([CLAIM-debezium-05](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | yes (section 10, reasoned) | yes (section 10, reasoned) | partial: images must be mirrored (unverified) | yes, self-hosted | yes by design (no required external service) |
| CAP-77 licence | Apache-2.0 ([CLAIM-debezium-02](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)) | Apache-2.0, licence file not fetched, 0.7 ([CLAIM-kafka-04](../04-COMPETITOR-DEEP-DIVES/C14-kafka.md)) | Apache-2.0 ([CLAIM-nats-02](../04-COMPETITOR-DEEP-DIVES/C14-nats.md)) | **ELv2 core, MIT protocol, contradictory docs** ([CLAIM-airbyte-02..05](../04-COMPETITOR-DEEP-DIVES/C14-airbyte.md)) | MIT ([CLAIM-temporal-02](../04-COMPETITOR-DEEP-DIVES/C14-temporal.md)) | BL-22 / NB-14 SBOM library-only |
| Graph-store reference (HugeGraph / Neo4j / Neptune) | n/a: none ships CDC from external DBs in the examined deep dives; Neptune/Neo4j stream features were not evidenced in cohort sources, so `unknown` | | | | | |

## 3. Operational and licensing comparison

| Dimension | Debezium | Kafka | NATS | Airbyte | Temporal | EOIP `DurableJobStore` |
|---|---|---|---|---|---|---|
| Latest examined | 3.7.0.Final, 2026-09-29 (CLAIM-debezium-01) | 4.3.2 tag 2026-10-20; 4.4.0 tag 2026-10-13, docs still 4.3 (CLAIM-kafka-01) | v2.15.1, 2026-10-09 (CLAIM-nats-01) | version **unverified** (CLAIM-airbyte-01, conf 0.2) | v1.32.1, "08 Oct", year not shown (CLAIM-temporal-01) | HEAD 896e06d |
| Runtime | JVM 17+ (Server 21+) | JVM 17+, KRaft only (CLAIM-kafka-02) | Go binary | Containers + platform workers | 4 services + SQL/Cassandra store (CLAIM-temporal-05) | Python + SQLite |
| One-node | feasible: one process | heavy vs SQLite (deep dive section 10) | single binary | not its design centre | dev server only | yes |
| Licence class | permissive | permissive | permissive | **source-available / mixed** | permissive (SDK licences unverified) | n/a |
| Redistribution / OEM trigger | none; Oracle/Db2/Informix JDBC driver licences UNVERIFIED | none (confirm licence file); exclude Confluent-licensed components (UNVERIFIED) | none; governance history UNVERIFIED (CLAIM-nats-06) | **ELv2 forbids hosted/managed-service exposure; white-label bundling is the risk case; legal review required** | none from server licence | n/a |
| Maintenance | active, five 3.x minors in 2026 | active | active | active (copyright 2026), cadence unknown | active | internal |

Tier C licence points (V27): Redpanda core is BSL 1.1 whose Additional Use Grant bars a "Streaming or Queueing Service", enterprise features are under a Redpanda Community License (`redpanda-01`, `redpanda-02`); Redpanda Connect has an Apache "free" bundle and a separate enterprise bundle with per-connector membership unverified (`redpanda-03`). Flink, NiFi, Airflow, SeaTunnel are Apache-2.0 by ASF standard but licence files were not fetched (confidence 0.7). Dagster, Prefect, dlt, Meltano licences were fetched: Apache-2.0 (Apache-2.0, MIT for Meltano) (`orch-01`, `orch-02`, `dlt-01`, `dlt-02`). These are legal-review triggers, not legal conclusions.

## 4. Performance evidence

None. All five deep dives record "no benchmark" ([CLAIM-debezium-04 section 7](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md), Kafka section 7, NATS section 7, Airbyte section 7, Temporal section 7). V27 Tier C gives no throughput figures. NATS "low memory" is a vendor-style claim not verified (NATS section 6). EOIP has no ingestion benchmark either (U-06 open, 01a). The only measurable statement is the Debezium incremental-snapshot default chunk of 1,024 rows ([CLAIM-debezium-04](../04-COMPETITOR-DEEP-DIVES/C14-debezium.md)), which is a setting, not a result. No winner can be declared on throughput, latency or footprint; the proposed POCs (Kafka card: 10k events/s on 4 vCPU; Temporal card: 1,000 crash injections) are the way to produce comparable evidence.

## 5. Findings

1. **The cohort is complementary, not competitive.** Capture (Debezium, Airbyte), transport (Kafka, NATS) and durable execution (Temporal) map to different CAPs; every deep-dive Appendix B maps them to different decisions (CAP-26, CAP-27, CAP-36). Falsifiable: a single product among the five covering CAP-26 + CAP-27 + one-node + permissive licence would contradict this; none does (matrix §2).
2. **No member propagates source ACLs.** Debezium, Kafka and NATS are absent or topic-level only; Airbyte and Temporal unknown or N/A (CLAIM-debezium-07, kafka-05, nats-05, airbyte-06). Caveat: the Debezium and Kafka entries are reasoned inference, not documentation reads (conf 0.5-0.6). EOIP already captures ACL metadata at ingest (BL-17), so ACL-carrying ingestion is differentiated if BL-18 is closed.
3. **Only Debezium has a documented consistent-backfill algorithm.** Watermarked, chunked incremental snapshot interleaved with the log, without locks (CLAIM-debezium-04). EOIP has replay of raw captured events but no equivalent live-source backfill-under-writes algorithm that I could find (BL-24, `ingestion/replay.py` covers file-captured sources only).
4. **EOIP's `DurableJobStore` matches or exceeds the examined brokers on governance semantics but not on distribution.** Tenant-gated, authority-gated DLQ replay with secret redaction (JOBS-HEAD) is not documented for Kafka DLQ topics, NATS, or Debezium (their deep dives record no tenant/authority-gated replay). It lacks multi-process fan-out, retention beyond SQLite, and any outbox relay. Falsifiable by running the `test_durable_jobs.py` suite and by a failed-relay test.
5. **`DurableJobStore` is not on any deployed path.** Only its own tests reference it (grep of `apps`, `packages`, `tests`). Any claim that EOIP "has a durable DLQ" must say library-only, consistent with 01a's library-only discipline.
6. **Airbyte is the only member whose licence blocks the obvious integration shape.** ELv2 core, MIT protocol, strategic connectors ELv2, with official docs and FAQ contradicting (CLAIM-airbyte-02..05); bundling in a white-label multi-tenant product is a legal trigger. The protocol alone is MIT (CLAIM-airbyte-03), so a protocol-compatible reader shim is not blocked on the evidence available.
7. **Debezium Server removes the Kafka dependency for CDC.** Sinks include NATS JetStream and HTTP with file offsets (CLAIM-debezium-05), so a one-node CDC path needs no Kafka and no Connect. Kafka's own deep dive rejects Connect as a connector host because Connect sinks would mutate the graph (Kafka section 13), a BL-23 conflict.
8. **Delivery is at-least-once everywhere in this cohort.** Every deep dive concludes consumers must dedupe (Debezium, NATS, Airbyte reasoned; Kafka EOS only for specific connectors). EOIP's event-id + payload-hash idempotency (BL-24) is therefore the correct place for exactly-once effects and should be treated as a parity requirement, not an optimisation.
9. **The Tier C permissive-licence connector long tail is unevaluated.** SeaTunnel 3.0.0 (dates differ by six days between sources, `seatunnel-01`), dlt, Meltano and Redpanda Connect free bundle are candidate sources, but all rest on general-knowledge descriptions (confidence 0.5-0.6) except licence and tag facts.
10. **Temporal addresses a gap EOIP has in NB-03.** `ActionEngine` keeps intents in an in-memory dict (01a NB-03), while Temporal's replayable event history is the reference design for persisted multi-step state (CLAIM-temporal-04). Whether EOIP needs Temporal itself or a journal on `DurableJobStore` is open (Temporal INV card selects the latter, unproven).

## 6. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-26 DB CDC | STR-debezium-01 (watermark backfill), STR-debezium-02 (Server to webhook) | INV-debezium-01 (no ACL propagation) | **INTEGRATE** Debezium Server as optional customer-run capture; **BUILD** the watermark-window pattern in EOIP crawl checkpoints | No log-based CDC connector exists; CDC change events cannot enter the `SourceEvent` pipeline with ACL and tenant metadata |
| CAP-26 connector breadth | STR-airbyte-01 (protocol-level contract) | INV-airbyte-01 (licence) | **EXPERIMENT** Airbyte-protocol reader shim for MIT/community connectors; **BUILD** licence gate over connector metadata; **REJECT** bundling Airbyte Core pending legal review; **EXPERIMENT** SeaTunnel / dlt / Meltano as permissive alternatives (V27) | No automated licence classification of third-party connectors (ties to CAP-77, CAP-79, NB-14) |
| CAP-27 replay / DLQ | STR-kafka-01 (offset replay) | INV-nats-01 (no governed DLQ), INV-kafka-01 (weight) | **REUSE** `DurableJobStore` as default; **BUILD** outbox relay and mount it in `apps`; **EXPERIMENT** bus port with NATS JetStream adapter | `DurableJobStore` is unmounted and has no relay publishing outbox rows; no ACL re-check at replay time |
| CAP-05 scale-out transport | STR-nats-01 | INV-kafka-01 | **DEFER** Kafka (adapter only on customer demand); **EXPERIMENT** NATS adapter behind a bus port. Mark Redpanda core **REJECT** for embedding (BSL, V27) | BL-60 external bus absent; available upstream, not integrated |
| CAP-46 ACL-aware ingestion | none (nobody does this) | INV-debezium-01, INV-kafka-01 | **BUILD** table-level ACL mapping to `SourceEvent.acl`, ACL-change events as first-class events, ACL re-check at DLQ replay | Source ACL is stored (BL-17) but not enforced end to end (BL-18); closing it is the moat for this cohort |
| CAP-36 / NB-03 state | STR-temporal-01 | INV-temporal-01 | **EXPERIMENT** step journal on SQLite for ActionEngine, DSAR and ontology releases; **DEFER** external Temporal as optional enterprise integration | `ActionEngine` intent state is non-durable |
| CAP-50 / CAP-04 | n/a | n/a | **REUSE**: SQLite default stays the one-node answer | Footprint claims for NATS/Kafka are unmeasured; run the 4 vCPU POC before any "lighter than Kafka" statement |

Backend neutrality: HugeGraph, Neo4j and Neptune are not ingestion engines; ingestion decisions here are store-agnostic because connectors never write the graph (BL-23).

## 7. Open questions

1. Does Airbyte's destination-only integration, run by the customer beside EOIP, count as "providing the software as a hosted service" under ELv2? (Airbyte section 15; legal review.)
2. What are Airbyte's current platform version, release cadence and ACL support? All three are UNVERIFIED (conf 0.2-0.4).
3. Which NATS JetStream facts hold: `Nats-Msg-Id` dedupe window, `max_deliver`, advisories, account isolation, Python client licence? Two documentation fetches failed (NATS Appendix D).
4. Is Kafka 4.4.0 GA? Tag exists 2026-10-13, docs show 4.3 (CLAIM-kafka-01).
5. Is `DurableJobStore` intended to be mounted (links to U-14 in 01a), and who relays `job_outbox`? Is per-key ordering guaranteed anywhere in it? (Not found in the code excerpts read.)
6. How should `tenant_id` travel over CDC: topic prefix versus message header (Debezium section 15)?
7. Do Oracle LogMiner/XStream and JDBC-driver licences create a redistribution trigger? (Debezium section 15, UNVERIFIED.)
8. Is Temporal server v1.32.1 dated 2026? The release page shows no year (CLAIM-temporal-01, conf 0.7).
9. Does a Redpanda Connect free-bundle component set (retries, DLQ-like routing) cover the sidecar role? Membership and depth unverified (`redpanda-03`).
