# C13 — Datomic

| Field | Value |
|---|---|
| Registry ID | T-C13-datomic |
| Tier | B (immutable fact store reference) |
| Versions examined | Datomic Pro 1.0.7745 (2026-10-16, release notes); search snippet earlier cited 1.0.7491 (2026-01-26) |
| Verified on | 2026-10-26 |
| Worker | V26 |

## 1. Identity, status, sources
Datomic: immutable, Datalog-queried database; developed by Cognitect, now Nubank. Active (release 2026-10-16) [CLAIM-datomic-01]. Licensing history: in April 2023 Nubank made Datomic free; Pro binaries are Apache-2.0 licensed at no cost with all features and unlimited peers/clients; Datomic Cloud made free June 2023; Datomic Local (embedded) is Apache-2.0 [CLAIM-datomic-02,03]. The product is NOT open source: source is closed, only binaries are Apache-2.0 [CLAIM-datomic-03]. Paid support remains. Sources: docs.datomic.com release notes; Datomic blog 2023; vendor FAQ.

## 2. Problem, workloads
Business systems needing full history, consistent reads, as-of audit, flexible schema; Clojure/JVM shops. Example: query account state as of tx 4567, diff against now.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Datom (E, A, V, Tx, Op); retractions are new datoms [CLAIM-datomic-04] | present |
| `as-of` view [CLAIM-datomic-04]; `since`, `history`, tx log | present (docs not fully fetched; conf 0.7) |
| Datalog query, pull API, rules | present (general knowledge; conf 0.7) |
| Indexes EAVT/AEVT/AVET/VAET | believed present; page did not list [CLAIM-datomic-04] |
| Valid-time (business time) | absent natively — modelled as ordinary attributes (reasoned) |
| Peers + transactor + pluggable storage (DDB, SQL, local) | present (general knowledge; conf 0.7) |
| Cloud (AWS-native) / Pro (on-prem or cloud) | present [CLAIM-datomic-02] |
| ACL / multi-tenancy | NOT PUBLICLY VERIFIED |

## 4. Architecture
```
 app peers (query engine in-process, caches segments)
     | reads segments           | txn requests
     v                          v
  storage service (object/SQL/KV)  <-- single transactor (serialised writes, tx log)
```

## 5. Reconstruction
Immutable value DB: the database is an ordered set of datoms; each transaction appends datoms with a monotonically increasing tx id; a retraction is `Op=false` datom; as-of filters `tx <= t` and drops retracted [CLAIM-datomic-04]. Hypothesis (general knowledge): covering indexes as persistent trees of segments, cached peer-side; single-writer transactor gives serialisable ACID with total tx order; reads scale horizontally with peers. Only one time axis (transaction); valid time must be app-modelled. Internals closed: NOT PUBLICLY VERIFIED beyond docs.

## 6. Inferred requirements
JVM; transactor process; storage backend; peer memory for working set; backup via storage-level.

## 7. Performance
No benchmarks gathered. Writes bound by one transactor (design trade-off, general knowledge). Working set must fit peer caches; failure mode: transactor failover window.

## 8. Strengths
Simple fact model, strong consistency, database-as-value (cheap time travel and "what-if" `with`). Match: BL-37 reads; exceed: derive speculative graph (`with`-style) for simulation.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | proprietary closed source; Apache-2.0 only on binaries [CLAIM-datomic-03]; no right to modify; vendor-controlled |
| Intentional | single transactor; unbounded-growth DB (excision needed for erasure) |
| Friction | Datalog/Clojure ecosystem; no graph query language; no bitemporality |
| Hypothesis | erasure ("excision") complicates DSAR |

## 10. Deployment/licensing
Binaries redistributable under Apache-2.0 per vendor release page; Datomic Local embeddable. Legal-review trigger: closed-source binary dependency, binary-only licence (no source), conflicting older Starter terms; confirm EULA scope for OEM white-label. Air-gap viable (Maven artifacts, local storage) — hypothesis.

## 11. Delta vs baseline
EOIP BL-37 gives two time axes at app layer; Datomic gives one built-in axis plus immutable-DB semantics. EOIP BL-25 tombstones vs Datomic retractions are comparable; DSAR (BL-46) harder in Datomic. No ACL advantage. Datomic is a model to emulate, not a candidate backend (CAP-01 REJECT).

## 12. Cards
STR-datomic-01 | Datomic | database as immutable value; `as-of`/`with` | CLAIM-datomic-04 | what-if simulation and consistent snapshots (CAP-65, simulation) | exceed | `GraphView(snapshot_id)` read-only handle and speculative overlay (HEAD `temporal/deterministic_graph.py` is a start) | overlay query never mutates store; snapshot hash stable.
STR-datomic-02 | Datomic | free binaries since 2023 | CLAIM-datomic-02,03 | cost-free audit store option | integrate | optional external store, not bundled | licence review sign-off.
INV-datomic-01 | Datomic | closed source, single transactor, excision | root cause: licensing/architecture (proven: not open source CLAIM-datomic-03) | keep temporal logic in open code; use open adapters | options: ignore / reference model / adapter | choose reference model | POC none; decision doc only | defensibility: open ontology/evidence formats | REJECT as dependency. Seed §10.5: none target this.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-34 as-of | REFERENCE (BL-37 suffices) |
| CAP-36 history | REFERENCE |
| Immutable-DB-value / what-if | EXPERIMENT |
| Datomic as backend | REJECT |

## 14. Tests
Snapshot-handle immutability test; speculative-overlay isolation test; licence file check if ever bundled.

## 15. Risks / open questions
Exact EULA wording for OEM; two version numbers seen (1.0.7491 vs 1.0.7745) — newest from docs page; internals unverifiable.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | Nubank; free Apache binaries |
| D2 | 2 | audit business data |
| D3 | 4 | peer/transactor/storage |
| D4 | 5 | datoms, covering indexes (believed) |
| D5 | 3 | attribute schema |
| D6 | 3 | Datalog |
| D7 | N/A | rules only |
| D8 | 5,7 | single transactor |
| D9 | N/A | |
| D10 | N/A | |
| D11 | 5 | tx time only |
| D12–D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | Clojure/Java |
| D18 | 3 | UNVERIFIED |
| D19 | N/A | |
| D20 | 7 | none |
| D21 | 1,10 | closed, free |
| D22 | 11 | lock-in via Datalog |
| D23 | N/A | |
| D24 | App C | |

## Appendix B — Capability mapping
| CAP | Native | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-34 | partial (tx time) | datomic-04 | BL-37 | REFERENCE | P3 |
| CAP-36 | native | datomic-04 | BL-37 | REFERENCE | P3 |
| CAP-65 | partial | datomic-04 | BL-43 | EXPERIMENT | P3 |
| CAP-77 | n/a | datomic-02 | — | REFERENCE | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| datomic-01 | Pro 1.0.7745 | latest Pro release; Pro binaries Apache-2.0, no cost, all features | Officially documented | https://docs.datomic.com/releases-pro.html | 2026-10-16 / 2026-10-26 | 0.85 | search snippet cited 1.0.7491 |
| datomic-02 | 2023 | all editions free; Cloud free June 2023 | Officially documented | https://blog.datomic.com/2023/04/datomic-is-free.html | 2023-04 / 2026-10-26 | 0.8 (from search result summary) | none |
| datomic-03 | FAQ/Wikipedia | not open source; Apache-2.0 for binaries; Local Apache-2.0 | Third-party report | https://en.wikipedia.org/wiki/Datomic | 2026-10-26 | 0.7 | none |
| datomic-04 | docs | datom 5-tuple, retraction as datom, as-of semantics | Officially documented | https://docs.datomic.com/whatis/data-model.html | 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions
Architecture of peers/transactor from general knowledge not fetched; licence conclusions are facts only, no legal view.
