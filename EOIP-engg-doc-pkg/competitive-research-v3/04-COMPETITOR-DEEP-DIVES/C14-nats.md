# C14 NATS and JetStream (Tier B)

| Field | Value |
|---|---|
| Registry ID | T-C14-nats |
| Tier | B (lightweight bus option for BL-60) |
| Versions examined | nats-server v2.15.1 (marked Latest; asset timestamps 2026-10-09) |
| Verified on | 2026-10-26 (brief: 2026-10-18) |
| Worker | V27 |

## 1. Identity, current status, tier, and sources
NATS is a Go messaging server; Core NATS is at-most-once pub/sub, JetStream is the built-in persistence layer [CLAIM-nats-03]. nats-server latest v2.15.1, 2026-10-09 [CLAIM-nats-01]. Licence of nats-server LICENSE: Apache-2.0 [CLAIM-nats-02]. Stewardship (Synadia / CNCF) not verified in this session: UNVERIFIED, confidence 0.3 [CLAIM-nats-06]. Sources: GitHub releases, LICENSE, docs.nats.io JetStream and consumers pages.

## 2. Problem, workloads, workflows
Small-footprint messaging with request/reply, subjects, streams, KV and object store. EOIP workflow: single static binary, JetStream stream `SOURCE_EVENTS` with subjects `src.<tenant>.>`; pull consumers drive the ingestion pipeline; Debezium Server can sink directly to NATS JetStream [CLAIM-debezium-05].

## 3. Feature inventory
| Feature | Status | Claim |
|---|---|---|
| Streams (memory/disk, limits- or ack-driven retention, server sequence numbers) | present | 03 |
| Consumers (server-side position, independent, explicit ack, redelivery on ack timeout) | present | 03 |
| Start positions: beginning, latest, sequence, time | present | 03 |
| Pull consumer batch/expires, MaxAckPending default 1000 | present | 04 |
| KV store, Object store (chunked) | present | 03 |
| Replication per stream | present (Raft detail not verified) | 03 |
| Dedupe via `Nats-Msg-Id` window; max_deliver; backoff; delivery-exceeded advisories | believed present, NOT verified this session | 05 (0.5) |
| Per-subject auth, accounts for multi-tenancy | believed present (accounts model), UNVERIFIED | 06 |
| Source-ACL propagation | absent | 05 |
| Native DLQ | absent as a primitive; built from advisories + a dead stream (reasoned) | 05 |

## 4. Architecture
```
 publishers --subject--> [nats-server] -- JetStream: stream (file/mem) --> consumer(s) (pull, ack)
 cluster: Raft-replicated streams across servers; accounts isolate subject spaces (UNVERIFIED)
 KV / Object store = streams with conventions
```

## 5. Under-the-hood reconstruction
Data model: subjects (dotted hierarchies) mapped to streams; each stored message gets a monotonically increasing stream sequence [CLAIM-nats-03]. Consumer = durable cursor + ack state; unacked messages are redelivered after the ack wait [CLAIM-nats-03]. Pull consumers: client requests a batch with `expires`; 408/404 status for empty fetch [CLAIM-nats-04], which is the natural backpressure and rate-limit mechanism (consumer paced, MaxAckPending bounds in-flight). Exactly-once pattern (hypothesis from general knowledge, 0.5): publisher sets `Nats-Msg-Id` for dedupe inside a server window, consumer double-acks, and EOIP's own idempotency key resolves residual duplicates, as with its webhook dedupe (BL-24). Ordering: per stream sequence; with filtered consumers, per-subject order preserved (reasoned). Security: account/permission model, TLS (not verified).

## 6. Requirements inferred
FR: subject-per-tenant namespacing; replay from sequence/time; ack-based redelivery; bounded in-flight. NFR: single static binary, low memory (vendor claim, not verified), file store durability.

## 7. Performance and resource model
No numbers collected; NOT PUBLICLY VERIFIED. Footprint small by design (Go single process) per general knowledge; one-node viable; clustering requires odd-sized Raft group (reasoned). Failure modes: consumer lag, stream limits discarding old messages (retention misconfiguration silently loses replay history).

## 8. Strengths
Smallest viable external bus; replay by sequence/time; KV and object store reduce extra components; Apache-2.0. EOIP matching: the existing SQLite outbox (`jobs.py`) covers one-node; NATS is the natural scale-out step and Debezium Server has a JetStream sink.

## 9. Limitations
Algorithmic: at-least-once; exactly-once is a pattern, not a guarantee (reasoned). Operational: retention limits lose history; no built-in DLQ. User friction: smaller connector ecosystem than Kafka Connect (no Connect equivalent verified). Licensing: governance history UNVERIFIED (legal review not triggered by licence text, which is Apache-2.0).

## 10. Deployment, licensing, viability
Apache-2.0; redistributable; air-gap yes; one-node yes (single binary). Embedding in-process is possible in Go only; for Python EOIP it is a sidecar.

## 11. Delta vs baseline
BL-60 Absent, BL-52 in-process only; BL-24 implemented, and HEAD `packages/eoip/jobs.py` already provides lease, fencing, outbox, DLQ on SQLite. NATS adds cross-process pub/sub the SQLite store lacks; it does not add DLQ governance or ACL.

## 12. Cards
STR-nats-01 | NATS | tiny single-binary durable bus with replay by seq/time | CLAIM-nats-03 | one-node to multi-node growth path | integrate | `EventBusPort` with NATS JetStream adapter, subjects `eoip.<tenant>.*` | test: publish 100k, kill server, restart, consumers resume from ack floor, zero loss.
INV-nats-01 | NATS 2.15 | no native DLQ/ACL-aware replay [CLAIM-nats-05, hypothesis] | cause: semantics. A: advisory-to-stream DLQ script; B: EOIP governed DLQ (`governed_dlq`) fed from max-deliver advisories; C: unified DLQ across SQLite and NATS. Select B. Worse if broker alone is expected to hold governance. POC: poison message exhausts redeliveries, lands in governed_dlq with tenant and reason, replay re-checks ACL. Decision EXPERIMENT.

## 13. Decisions
CAP-27: INTEGRATE (optional JetStream adapter, keep SQLite default); CAP-04 footprint: REUSE concept; CAP-47 tenant subjects: EXPERIMENT; KV/object store: REJECT (graph backends hold state).

## 14. Tests
Adapter contract tests shared with SQLite store; chaos: kill -9 during ack; duplicate publish with same msg-id; stream limit hit. Acceptance: no loss, idempotent apply, tenant isolation of subjects. PROPOSED.

## 15. Risks / questions
Verify dedupe window, max_deliver, advisory subjects, account isolation, licence/governance current state, Python client (nats.py) licence. Retention-vs-replay window sizing.

## Appendix A. Dimension coverage
| D | Sections | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0, governance UNVERIFIED |
| D2 | 2 | lightweight bus |
| D3 | 4 | server, streams, consumers |
| D4-D7,D12-D14,D16,D19 | N/A | not graph/query |
| D8 | 5 | seq ordering, replication |
| D9 | 3,5 | pull pacing, replay |
| D10 | 9 | no ACL |
| D11 | 5 | replay by time |
| D15,D17 | 3 | N/A detail |
| D18 | 3 | UNVERIFIED |
| D20 | 7 | no numbers |
| D21 | 10 | permissive |
| D22 | 13 | proprietary protocol, simple |
| D23 | N/A | none |
| D24 | App. C | partial pages |

## Appendix B. Capability mapping
| CAP | NATS | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-27 | partial | 03,05 | BL-24 Impl | INTEGRATE | P2 |
| CAP-04 | native | 07 | BL-60 Absent | EXPERIMENT | P2 |
| CAP-05 | native | 03 | BL-60 Absent | DEFER | P3 |
| CAP-47 | partial | 06 | BL-20 Partial | EXPERIMENT | P2 |
| CAP-50 | native | 02 | n/a | INTEGRATE | P2 |

## Appendix C. Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| nats-01 | v2.15.1 | latest release, 2026-10-09 per asset timestamps | Officially documented | https://github.com/nats-io/nats-server/releases | acc 2026-10-26 | 0.8 | page truncated at 100k chars |
| nats-02 | main | LICENSE is Apache-2.0 | Observed (licence file) | https://raw.githubusercontent.com/nats-io/nats-server/main/LICENSE | acc 2026-10-26 | 0.9 | none |
| nats-03 | docs | streams, consumers, at-least-once, start positions, KV, object store | Officially documented | https://docs.nats.io/nats-concepts/jetstream | acc 2026-10-26 | 0.85 | page omits dedupe/DLQ |
| nats-04 | docs | pull consumer, MaxAckPending 1000, 408/404 | Officially documented | https://docs.nats.io/nats-concepts/jetstream/consumers | acc 2026-10-26 | 0.8 | none |
| nats-05 | n/a | Nats-Msg-Id dedupe, max_deliver, advisories; no native DLQ | Reasoned inference | pages did not cover | n/a | 0.5 | unverified |
| nats-06 | n/a | accounts isolation, governance history | Unverified | n/a | n/a | 0.3 | n/a |

## Appendix D. Assumptions
Items marked 0.5 or less come from general knowledge and need a follow-up fetch of the JetStream model/reference pages (two fetches failed to return them).
