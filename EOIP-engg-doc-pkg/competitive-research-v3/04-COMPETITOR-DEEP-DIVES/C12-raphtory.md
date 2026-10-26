# C12 — Raphtory

| Field | Value |
|---|---|
| Registry ID | T-C12-raphtory |
| Tier | B (temporal graph analytics; licence to verify) |
| Versions examined | raphtory 0.18.5 (PyPI 2026-06-23); 0.17.0 (2026-03-11); repo branch `db_v4` |
| Verified on | 2026-10-26 |
| Worker | V25 |

## 1. Identity, status, sources
Raphtory: "scalable graph analytics database powered by a multithreaded, vectorized temporal engine, written in Rust", in-memory with Python API, by the Pometry-associated team [CLAIM-raphtory-01]. **Licence: GPL-3.0** (repo sidebar and README) [CLAIM-raphtory-01] — the PyPI metadata carries no licence field. README refers to a commercial "subscription model" for out-of-memory scaling (terms not public) [CLAIM-raphtory-01]. Paper arXiv:2306.16309 (v2 2024-01-03) [CLAIM-raphtory-03]. Active (649 stars, 2,351 commits on db_v4). Pre-1.0.

## 2. Problem and workloads
Temporal networks: edges/nodes with time-stamped updates; windows, views at time t, rolling analyses, temporal motifs, risk scoring. Workflow: `g.add_edge(ts, src, dst, properties)`, `g.window(t1,t2)`, run algorithms, serve via GraphQL.

## 3. Feature inventory
| Area | Status |
|---|---|
| Temporal event model, windows/views, as-of | present (CAP-34, CAP-65) |
| Algorithms: PageRank, temporal motifs; "bounty board of desired algorithms" | present partially; full list UNVERIFIED (docs URL 404) |
| Centrality/community/shortest paths | partial/UNVERIFIED |
| Subgraph matching | UNVERIFIED |
| GraphQL server | present [CLAIM-raphtory-03] |
| Out-of-memory storage | commercial subscription (enterprise-only, unverified terms) |
| Anomaly detection | "automatic risk detection" marketing only, UNVERIFIED |
| Auth/tenancy | UNVERIFIED |

## 4. Architecture
```
Python / GraphQL / Rust API -> Rust temporal engine (in-memory, sharded, multithreaded)
   ingest: add_edge(timestamp,...) -> time-indexed adjacency; views = lazy time windows
```
Single process; sharding is intra-process.

## 5. Reconstruction
Hypothesis (0.4): each node/edge stores a sorted history of (time, event/property) entries; windows are filters over histories, avoiding materialisation; algorithms run vertex-centrically on lazy views. Not verified against source in this pass. The paper abstract confirms Rust core, Python interface, GraphQL server, ingestion from various sources [CLAIM-raphtory-03].

## 6. Requirements inferred
Event-time ingest; window/view algebra; property history; extensible algorithms; embeddable and serveable.

## 7. Performance and resource model
No benchmark figures in abstract [CLAIM-raphtory-03]; none retrieved independently: UNVERIFIED. Footprint: PyPI linux x86_64 wheels for 0.17.0 are ~93 MB (cp311), versus ~31 MB for 0.16.5 [CLAIM-raphtory-02]. The 0.18.5 PyPI release lists only two macOS wheels (~97-102 MB) in the JSON file list, no Linux/Windows files — so Linux installs of 0.18.5 may require source build or the last Linux release (0.17.0) [CLAIM-raphtory-02] (as seen via the API; may change). Memory bound by RAM.

## 8. Strengths
Only verified temporal-native analytics engine in C12; Rust performance; GraphQL; maps directly to CAP-65 and bitemporal-adjacent needs.

## 9. Limitations
| Class | Item |
|---|---|
| Licensing | GPL-3.0 core; commercial split for scale |
| Operational | in-memory; 3x wheel growth to ~93 MB; Linux wheel gap in 0.18.5 |
| Maturity | pre-1.0; docs URL for v0.16 algorithms 404; single-valid-time model, not bitemporal (hypothesis) |

## 10. Deployment, licensing
GPL-3.0 = strong copyleft, legal-review trigger (embedding, redistribution in wheels/containers). Community-vs-enterprise split: out-of-memory in paid tier. Air-gap: wheels install offline when available. CPU only.

## 11. Delta vs baseline
BL-43 has no temporal analytics; temporal semantics elsewhere in EOIP (event sourcing, as-of) belong to other baseline items I did not re-audit. Raphtory shows temporal windows as first-class analytics views over a time-indexed adjacency.

## 12. Cards
`STR-raphtory-01 | Raphtory | window/view algebra for temporal graph analytics | CLAIM-01,03 | "what did the graph look like / how did centrality change" | exceed | EOIP native windowed snapshot over event log, permissive code | windowed PageRank on 10^6 events matches Raphtory output; clean-room`
INV-raphtory-01 — target 0.18.5. Limitation: GPL + in-memory + paid scale tier. Root cause: licensing/storage (proven for licence; hypothesis for architecture). Options: (a) exclude, (b) native windowed algorithms over EOIP event log, (c) process-isolated optional adapter after legal review. Selected (b). POC: 10^6-event log, 10 windows, PageRank per window, time and RSS recorded. Failure: windows must respect tenant/ACL filters. Decision: EXPERIMENT. No seed hypothesis targets Raphtory.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-65 temporal analytics concept | BUILD natively (clean-room) |
| Raphtory as dependency | REJECT (GPL-3.0; legal review) |
| Raphtory as external benchmark | REFERENCE-ONLY |

## 14. Tests
Off-product comparison harness; licence scan; acceptance: windowed results equal Raphtory on public dataset.

## 15. Risks
Licence ambiguity of the commercial tier; source not inspected; benchmark and algorithm list unknown; GPL contamination if read-and-copied.

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1 | 1,10 | GPL-3.0, active |
| D2 | 2 | temporal nets |
| D3 | 4 | Rust engine |
| D4 | 5 | hypothesis |
| D5 | N/A | |
| D6 | N/A | |
| D7 | N/A | |
| D8 | 7 | in-memory |
| D9 | 3 | ingest from sources |
| D10 | N/A | |
| D11 | 3,5 | windows, as-of |
| D12 | 3 | partial |
| D13 | N/A | |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | Python, GraphQL |
| D18 | UNVERIFIED | |
| D19 | UNVERIFIED | |
| D20 | 7 | wheel sizes only |
| D21 | 1,10 | open core split |
| D22 | N/A | |
| D23 | N/A | none found |
| D24 | 7 | weak |

## Appendix B
| CAP | Raphtory | Claim | EOIP | Decision | Prio |
|---|---|---|---|---|---|
| CAP-65 | native | 01,03 | BL-43 (no temporal) | BUILD | P1 |
| CAP-34 | partial | 01 | not re-audited | BUILD | P2 |
| CAP-77 | GPL / enterprise tier | 01 | — | REJECT dep | P1 |

## Appendix C
| ID | Product | Claim | Class | Source | Dates / conf | Contradiction |
|---|---|---|---|---|---|---|
| CLAIM-raphtory-01 | repo db_v4 | GPL-3.0; Rust; in-memory; subscription for OOM | Officially documented | https://github.com/Raphtory/Raphtory | acc 2026-10-26; 0.8 | |
| CLAIM-raphtory-02 | 0.16.5-0.18.5 | wheel sizes/platforms | Officially documented | https://pypi.org/pypi/raphtory/json | 2026-06-23 / acc 2026-10-26; 0.85 | file list may be incomplete |
| CLAIM-raphtory-03 | paper v2 2024-01-03 | Rust core, GraphQL, no figures | Officially documented | https://arxiv.org/abs/2306.16309 | acc 2026-10-26; 0.9 | |

## Appendix D
Source not read; algorithm list unavailable; PyPI listing for 0.18.5 may be a transient artefact.
