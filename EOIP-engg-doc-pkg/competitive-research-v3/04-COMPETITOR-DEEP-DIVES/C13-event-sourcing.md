# C13 — Event sourcing, CQRS and bitemporal modelling (pattern record)

| Field | Value |
|---|---|
| Registry ID | T-C13-event-sourcing |
| Tier | B (pattern reference for living-graph mechanics; no single product) |
| Versions examined | Fowler "Bitemporal History" (7 Apr 2021); SQL:2011 temporal (XTDB docs reference); EOIP HEAD temporal/replay code |
| Verified on | 2026-10-26 |
| Worker | V26 |

## 1. Identity, status, sources
Not a product: a family of patterns. Event sourcing (ES) = persist state changes as an append-only event log, derive current state by fold; CQRS = separate write model from read models/projections; bitemporal = two time axes, "actual history" (valid time) and "record history" (transaction time) [CLAIM-es-01]. Standards anchor: SQL:2011 period/system-versioned tables (cited by XTDB as its inspiration) [CLAIM-es-02]. Licensing: none (ideas). Implementations referenced: XTDB, Datomic, Dolt, TerminusDB (C01-terminusdb.md), Graphiti/Zep (C08-graphiti-zep.md). Sources: martinfowler.com article; XTDB docs; EOIP code.

## 2. Problem and workloads
Audit, replay, rebuild projections after logic bug, answer "what did we believe on date X?", late-arriving corrections, regulatory reconstruction, graph "drift" tracking. Example: a customer address is corrected retroactively; system must show both the corrected truth and what reports said last quarter.

## 3. Feature inventory (pattern components)
| Component | Role | Pitfall |
|---|---|---|
| Append-only event log | source of truth | schema evolution of events |
| Projections / read models | graph, search, vector indexes | rebuild time, eventual consistency |
| Snapshots | bound replay cost | stale snapshot after code change |
| Idempotency keys, ordering per aggregate | exactly-once effect | cross-aggregate ordering |
| Valid/transaction time columns | bitemporal reads | correction semantics, interval overlap |
| Upcasting / event versioning | evolve events | long tail of old versions |
| Tombstone + crypto-shredding | GDPR erasure in immutable log | conflicts with immutability |

## 4. Architecture
```
 command -> validate (gate) -> EVENT LOG (append-only, tx_time stamped)
                                   |-> projector -> graph store (current + history)
                                   |-> projector -> search/vector index
                                   '-> snapshot store
 query: as-of(valid_at, known_at) -> reads projection or replays slice
```

## 5. Reconstruction
Bitemporal record = (subject, payload, valid_from, valid_to, tx_from, tx_to?). Fowler's formulation: record history is append-only; corrections add entries and never overwrite [CLAIM-es-01]. Two query shapes: "known_at T" (filter by tx time then pick latest per subject) and "valid_at V". EOIP implements exactly this: `BitemporalQueryEngine.known_at/valid_at/slice/topology/diff` selecting `RevisionRecord` (observed_at, valid_from, valid_to, is_delete) over any `GraphStore` and taking the latest per subject [CLAIM-es-03]. Differences from DB-native: no transactional guarantee that valid-time intervals are non-overlapping; scan-based `_select` (hypothesis: O(n) over revisions, not indexed — code not profiled). Erasure vs immutability: tombstones (BL-25) plus DSAR (BL-46).

## 6. Inferred requirements
Event contract versioning; deterministic replay (same input, same graph hash); per-tenant partitioning of log; projection rebuild tests; erasure path; tx-time server-assigned only.

## 7. Performance model
Write: O(1) append. Read-as-of: O(history) unless indexed per subject/time; snapshots bound replay. Rebuild cost linear in log length. No numbers claimed. Failure modes: projection drift, poison events (BL-24 DLQ), unbounded log growth (needs compaction/archival).

## 8. Strengths
Total audit; time travel; recomputation after bug fix; decoupled read models (fits multi-backend neutrality: log is backend-neutral). Match: already; exceed: deterministic replay hash + ACL-aware as-of (HEAD `temporal/authorized_as_of.py`).

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | read-your-writes, cross-aggregate transactions awkward |
| Operational | log growth, snapshot/projection rebuild windows |
| Friction | event schema evolution, developer mental model; "ES everywhere" anti-pattern |
| Legal | erasure vs immutability |
| Hypothesis | application-layer revisions miss DB-level atomicity of valid/tx time |

## 10. Deployment/licensing
Pattern: no licence. Fully air-gap viable. Any store can host the log (Postgres, files, Kafka); EOIP has `execution/eventstore.py` plus WAL/backup (BL-50).

## 11. Delta vs EOIP baseline
Present: BL-37 revisions + bitemporal reads (application layer; HEAD adds `temporal/authorized_as_of.py`, `deterministic_graph.py`); BL-38 diff/snapshots/playback; BL-24 replay/DLQ/checkpoints; BL-52 mutation stream. Gaps: no single canonical command/event log feeding all projections (log scattered: SourceEvent, WAL, eventstore) — UNVERIFIED unification; no verified temporal indexes; BL-18 ACL absent in retrieval though as-of is authorised at HEAD (UNVERIFIED end-to-end); CAP-37 schema evolution partial (BL-32).

## 12. Cards
STR-event-sourcing-01 | pattern | replayable, rebuildable projections | CLAIM-es-01, es-03 | backend-neutral rebuild of graph/search/vector after bug or backend switch | match | single `MutationEvent` log with versioned schema, projector per backend | rebuild graph from log yields identical canonical hash on two backends.
STR-event-sourcing-02 | pattern/XTDB | bitemporal corrections without data loss | CLAIM-es-01,es-02 | regulator-grade "as known on" answers | exceed | add per-subject temporal index and non-overlap validator | 1M-revision as-of query p95 within budget (to set).
INV-event-sourcing-01 | pattern vs DB-native | app-layer temporal logic reimplements what XTDB/Datomic enforce in engine | root cause: coupling (hypothesis) | keep app layer for backend neutrality; add invariants test + indexes | options: (a) integrate XTDB as history store, (b) harden native (indexes, constraints), (c) pluggable HistoryStore SPI with XTDB reference adapter | choose (b) then (c) | property tests: non-overlap, idempotent replay, equality vs XTDB oracle on random histories; baseline = current scan | deps BL-01 | defensibility: works on HugeGraph/Neo4j/Neptune where none has bitemporality | ADOPT. Seed §10.5 "graph drift via bitemporal event sourcing": supported as direction, NOT validated by measurement here.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-36 event sourcing/history | BUILD (consolidate log), P1 |
| CAP-34 bitemporal/as-of | BUILD harden + EXPERIMENT XTDB oracle, P1 |
| CAP-35 branch/diff/merge | REUSE existing BL-38; see Dolt/TerminusDB |
| CAP-37 schema evolution | BUILD (event upcasters), P2 |
| CAP-27 replay | REUSE BL-24 |

## 14. Tests/POC
Replay determinism; temporal property tests vs XTDB oracle; erasure-through-log test; as-of ACL test; projection-drift detector.

## 15. Risks / open questions
Is there a canonical log today? Do temporal reads scale? How to reconcile crypto-shredding with replay hash? Does HEAD `authorized_as_of` cover retrieval paths?

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | pattern, no owner |
| D2 | 2 | audit/time-travel |
| D3 | 4 | log→projections |
| D4 | 5 | N/A (host-defined) |
| D5 | 3 | event versioning |
| D6 | N/A | host |
| D7 | N/A | none |
| D8 | 9 | ordering, consistency |
| D9 | 3,11 | replay, idempotency |
| D10 | 5 | evidence via events |
| D11 | 5,11 | core topic |
| D12–D14 | N/A | out of scope |
| D15 | 11 | schema evolution |
| D16 | 11 | time-machine UX (CAP-73) |
| D17 | 12 | upcasters, tests |
| D18 | 9 | erasure, ACL |
| D19 | 6 | per-tenant log |
| D20 | 7 | growth/rebuild |
| D21 | 10 | none |
| D22 | 10 | log neutral |
| D23 | N/A | not assessed |
| D24 | App C | |

## Appendix B — Capability mapping
| CAP | Native | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-36 | pattern | es-01 | BL-37,BL-24 Implemented | BUILD | P1 |
| CAP-34 | pattern | es-01,es-03 | BL-37 Implemented | BUILD | P1 |
| CAP-27 | pattern | es-03 | BL-24 | REUSE | P2 |
| CAP-37 | pattern | es-01 | BL-32 Partial | BUILD | P2 |
| CAP-73 | n/a | — | BL-38 | DEFER | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| es-01 | Fowler 2021 | actual vs record history; record history append-only | Third-party report (authoritative) | https://martinfowler.com/articles/bitemporal-history.html | 2021-04-07 / 2026-10-26 | 0.9 | none |
| es-02 | XTDB docs | temporal model inspired by SQL:2011 | Officially documented | https://docs.xtdb.com/intro/what-is-xtdb.html | 2026-10-26 | 0.85 | none |
| es-03 | EOIP HEAD | BitemporalQueryEngine known_at/valid_at/slice/topology/diff over RevisionRecord | Observed in source code | packages/eoip/graph/bitemporal.py:42-271 | 2026-10-26 | 0.9 | not profiled |

## Appendix D — Assumptions
Pattern treated as a single record; "O(n) scan" is hypothesis; CQRS literature not separately fetched (general knowledge, conf 0.6).
