# C14 Temporal (durable workflows) (Tier B)

| Field | Value |
|---|---|
| Registry ID | T-C14-temporal |
| Tier | B (durable workflow reference) |
| Versions examined | temporal server v1.32.1 (marked Latest, "08 Oct", year not shown on page; presumed 2026) |
| Verified on | 2026-10-26 (brief: 2026-10-18) |
| Worker | V27 |

## 1. Identity, current status, tier, and sources
Temporal Technologies; open-source durable-execution server (fork lineage of Uber Cadence, shown by the Uber 2020 copyright line) with SDKs. Licence MIT (Temporal Technologies 2025, Uber 2020) [CLAIM-temporal-02]. Active [CLAIM-temporal-01]. Temporal Cloud is a separate commercial service (not examined). Sources: GitHub releases, LICENSE, docs.temporal.io workflows, features index, self-hosted guide.

## 2. Problem, workloads, workflows
Long-running, failure-proof orchestration: code-defined workflows that survive crashes, with retries, timers, signals and schedules. EOIP workflow: "crawl source X incrementally every hour": a Schedule starts a workflow; an Activity fetches a page, emits `SourceEvent`s and records a cursor; the workflow continues-as-new per N pages; failure retries with backoff; replay re-drives from event history. Use for ontology release pipelines and DSAR erasure orchestration too.

## 3. Feature inventory
| Feature | Status | Claim |
|---|---|---|
| Workflows/Activities/Workers, timeouts, automatic retries | present | 03 |
| Child workflows, Nexus cross-namespace calls | present | 03 |
| Signals/updates (message passing), cancellation/termination with compensation | present | 03 |
| Schedules (cron-like), Activities as durable background jobs without a workflow | present | 03 |
| Observability: list workflows, metrics | present | 03 |
| Payload codecs / data encryption | present | 03, 05 |
| Workflow versioning/runtime safeguards | present | 03 |
| Visibility store (Elasticsearch listed) for search | present | 05 |
| Archival to blob storage; cross-cluster replication for DR | present | 05 |
| Source-ACL, graph semantics | absent (N/A) | n/a |
| DLQ | partial: failed/terminated workflows are queryable; replication DLQ exists for cluster replication (UNVERIFIED) | 05 |

## 4. Architecture
```
 SDK workers (user code: workflows+activities) <--long-poll task queues--> [Frontend] [History] [Matching] [Worker svc]
                                                                  |
                          Persistence: Cassandra | MySQL | PostgreSQL | SQLite(dev)    Visibility: SQL/Elasticsearch
 Dev: `temporal server start-dev` single binary, no external deps
```
Services and stores per self-hosted guide [CLAIM-temporal-05].

## 5. Under-the-hood reconstruction
Data model: Event History is an ordered log of everything that happened (timers, activity results, signals) and is the source of truth [CLAIM-temporal-04]. Recovery by *replay*: workflow code is re-executed from the start, with recorded events supplying results; activities are not re-run during replay [CLAIM-temporal-04]. Hence determinism constraints: no unrecorded clock, randomness, or network calls inside workflow code [CLAIM-temporal-04]. Sharded history service with per-workflow serialisation (hypothesis from general knowledge, 0.5). History size limits and continue-as-new: page did not cover; UNVERIFIED. At-least-once activity execution implies idempotent activities; the docs excerpt does not discuss idempotency keys explicitly [CLAIM-temporal-04]. Security: mTLS/auth in self-hosted guide index; namespaces for multi-tenancy [CLAIM-temporal-05].

## 6. Requirements inferred
FR: durable timers, retry policies, idempotent activities, workflow-id uniqueness (UNVERIFIED). NFR: persistence store with transactions; at least four server roles; workers need deterministic code discipline.

## 7. Performance and resource model
No numbers (NOT PUBLICLY VERIFIED here). Footprint: dev server is one binary; production needs PostgreSQL/MySQL/Cassandra plus optional Elasticsearch. Failure modes: non-determinism errors after code changes without versioning, history growth, persistence latency.

## 8. Strengths
Crash-proof orchestration with human-readable history; first-class retries, timers, schedules; SQL-only deployment possible; MIT. Match: EOIP's `DurableJobStore` already has lease, heartbeat, fencing token, checkpoint, outbox, governed DLQ and `replay_dlq` on SQLite, which covers job durability; what Temporal adds is multi-step workflow state and timers. Exceed: tenant-governed DLQ and signed receipts.

## 9. Limitations
Algorithmic: replay model forces deterministic code and versioning discipline. Operational: multi-service server and DB, Elasticsearch for advanced visibility. Friction: new programming model; Python SDK is a separate dependency (not examined). Heavy for one-node appliance.

## 10. Deployment, licensing, viability
MIT permissive; no legal trigger from server licence; SDK licences not examined (UNVERIFIED). Air-gap yes (self-hosted; SQLite dev only, not production). One-node: dev server only; production single-node Postgres-backed possible but not verified.

## 11. Delta vs baseline
BL-24: replay/DLQ/checkpoints Implemented; `packages/eoip/jobs.py` (598 lines; observed at HEAD, not covered in 01a) provides a SQLite durable queue with leases, fencing tokens, heartbeats, checkpoint, commit, fail/retry, transactional outbox, governed DLQ and `replay_dlq`, plus `JobQueue`. NB-03 ActionEngine implements two-phase write-back in-memory (no persistence), where Temporal-style durable state would add value. BL-23 unaffected. BL-60 unaffected.

## 12. Cards
STR-temporal-01 | Temporal | event-history replay for crash recovery of multi-step flows | CLAIM-temporal-04 | resumable ontology releases, DSAR, ActionEngine | match | persist `ActionEngine` intents and step results as an append-only history in SQLite; resume by re-driving from history | test: kill mid-flow at each step, restart, final state identical, side effects exactly once via idempotency key.
INV-temporal-01 | Temporal | deterministic-code requirement and multi-service footprint [CLAIM-temporal-04,05; root cause: coupling/deployment, proven] | A: integrate Temporal for customers who run it; B: extend `DurableJobStore` with step journal and timers; C: declarative workflow definitions (data, not code) replayed deterministically. Select B. Worse for very long, complex human-in-loop flows. POC: 10-step flow, 1,000 crash injections. Decision EXPERIMENT. Seed hypotheses 10.5: none target Temporal.

## 13. Decisions
CAP-27 durable job/replay: REUSE existing `DurableJobStore`; step journal/timers: BUILD (EXPERIMENT); external Temporal: DEFER/INTEGRATE optional for enterprise customers; CAP-36 history concept: REUSE.

## 14. Tests
Crash-injection harness on journal; worker fencing test (expired lease cannot commit, already in `FencedWorkerError`); schedule drift test. Acceptance: no double side effects, DLQ record per exhausted retry. PROPOSED.

## 15. Risks / questions
Version-date year not shown; history size limits unverified; Python SDK licence unverified; Temporal Cloud-only features unknown.

## Appendix A. Dimension coverage
| D | Sections | Summary |
|---|---|---|
| D1 | 1 | MIT |
| D2 | 2 | durable orchestration |
| D3 | 4 | 4 services + stores |
| D4-D7,D12-D14,D16 | N/A | not graph |
| D8 | 5,7 | persistence-backed, replay |
| D9 | 3 | retries, schedules |
| D10 | 9 | none |
| D11 | 5 | event history |
| D15,D17 | 3 | SDKs |
| D18 | 5 | mTLS, codecs |
| D19 | 5 | namespaces |
| D20 | 7 | none |
| D21 | 10 | MIT |
| D22 | N/A | code-defined |
| D23 | N/A | none |
| D24 | App. C | partial |

## Appendix B. Capability mapping
| CAP | Temporal | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-27 | partial | 03,04 | BL-24 Impl | REUSE own | P2 |
| CAP-36 | native | 04 | BL-25 | REUSE concept | P2 |
| CAP-47 | partial | 05 | BL-20 Partial | EXPERIMENT | P3 |
| CAP-75 | partial | 03 | n/a | REUSE | P3 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| temporal-01 | v1.32.1 | latest release, "08 Oct" | Officially documented | https://github.com/temporalio/temporal/releases | acc 2026-10-26 | 0.7 | year not shown |
| temporal-02 | main | MIT, Temporal 2025 and Uber 2020 | Observed (licence file) | https://raw.githubusercontent.com/temporalio/temporal/main/LICENSE | acc 2026-10-26 | 0.9 | none |
| temporal-03 | docs | feature list | Officially documented | https://docs.temporal.io/evaluate/development-production-features/ | acc 2026-10-26 | 0.85 | none |
| temporal-04 | docs | event history, replay, determinism | Officially documented | https://docs.temporal.io/workflows | acc 2026-10-26 | 0.85 | none |
| temporal-05 | docs | persistence stores, services, namespaces, dev server | Officially documented | https://docs.temporal.io/self-hosted-guide | acc 2026-10-26 | 0.85 | none |

## Appendix D. Assumptions
Temporal server licence is MIT; SDK repos assumed MIT but unverified. `jobs.py` read at HEAD only superficially (headers, method names).
