# C04 — OpenRefine and Wikidata reconciliation

| Field | Value |
|---|---|
| Registry ID | T-C04-openrefine |
| Tier | B — data cleaning/reconciliation reference |
| Versions examined | OpenRefine **3.10.1** (release 2026-03-04; 3.10.0 on 2026-02-27); commits through 2026-10-23; Reconciliation Service API **v0.2** (W3C Entity Reconciliation CG Final Report, 2023-04-10) |
| Verified on | 2026-10-18 |
| Worker | V12 |

## 1. Identity, current status, tier, and sources
OpenRefine is a desktop-served (local web UI) data cleaning and transformation tool, originally Google Refine (copyright "2010, Google Inc." and OpenRefine contributors) [CLAIM-or-01]. Licence BSD 3-clause style (text includes redistribution conditions and "Neither the name" clause) [CLAIM-or-01]. Status: **active**, commits within days of verification [CLAIM-or-02]. Reconciliation means matching cell values to entities in an external service that implements the Reconciliation Service API; Wikidata is built in [CLAIM-or-03]. The API spec is a W3C Community Group report, not a W3C Standard [CLAIM-or-04]. Cross-ref: `C04-senzing.md`, `C04-splink.md` for full ER.
Sources (5): repo LICENSE and Atom feeds; OpenRefine manual "Reconciling"; W3C CG report v0.2; CG list announcement.

## 2. Problem, workloads, workflows
Interactive cleanup of messy tabular data (clustering of near-duplicate strings, transformations in GREL/Python/Jython-class expressions, faceting) and linking cells to canonical IDs. Workflow: import CSV -> cluster/edit -> reconcile column against Wikidata or a custom service -> review candidates by score -> bulk-accept best matches -> export or push to Wikibase [CLAIM-or-03]. Scale: a single-user, in-memory tool (hypothesis; typical limit is project size in RAM).

## 3. Feature inventory
| Feature | Status |
|---|---|
| Faceting, clustering of variants, transform expressions | present |
| Reconciliation with scores, property-assisted disambiguation | present [CLAIM-or-03] |
| Auto-match vs candidate review (dark/light blue) | present [CLAIM-or-03] |
| Use values as identifiers (skip lookup) | present |
| Local services from CSV (reconcile-csv, csv-reconcile) | present (third-party) [CLAIM-or-03] |
| Create-new-item drafts for Wikibase upload | partial; few services support it [CLAIM-or-03] |
| Reconciliation API v0.2: authentication, type hierarchies, per-feature candidate scores, property-only reconciliation | present in spec [CLAIM-or-04] |
| Multi-user, tenancy, RBAC, server mode | absent (single-user; hypothesis conf 0.7) |
| Operation history as JSON recipe | present (hypothesis from OpenRefine docs, conf 0.7) |

## 4. Architecture
```
Browser UI <--HTTP--> local Jetty server (Java) : project store on disk, in-memory grid
column cell values --HTTP/JSON (Reconciliation API)--> reconciliation service (Wikidata, custom)
   <-- candidates{id,name,score,types,match} ; user accepts/auto-accepts --> cell linked to id
```

## 5. Under-the-hood reconstruction
Spec level (documented): client POSTs batches of queries (`query` text, optional `type`, `properties`, `limit`) and receives ranked candidates with `id`, `name`, `score`, `match` flag, types; v0.2 adds features per candidate [CLAIM-or-04]. Scores are service-specific, so thresholds are not portable [CLAIM-or-03]. Hypotheses (conf 0.5): project stored as a serialized grid + change history; cluster methods include key-collision (fingerprint) and nearest-neighbour (distance) families. No concurrency, partitioning or security model beyond local use.

## 6. Requirements inferred
Candidate scoring with property evidence; human-in-the-loop acceptance thresholds; replayable operation history; pluggable reconciliation endpoints with auth.

## 7. Performance and resource model
No numbers verified. Wikidata reconciliation depends on a public hosted endpoint (network; not available air-gapped). Local CSV-backed services are the offline path [CLAIM-or-03]. Failure modes: ambiguous names, rate limits, differing score scales, large projects in RAM.

## 8. Strengths
| ID | Strength | Match/exceed |
|---|---|---|
| STR-or-01 | Open, W3C-CG reconciliation protocol with scores, types, properties | INTEGRATE: expose an EOIP reconciliation endpoint (tenant ACL aware) and consume the protocol for external authority files |
| STR-or-02 | Reviewer UX: facets by score, bulk accept, "also use details from other columns" | BUILD equivalent in identity review queue (BL-35) |
| STR-or-03 | Replayable cleaning history | match via CML transform steps with provenance |
| STR-or-04 | Mature, BSD, offline desktop | REFERENCE; users can pre-clean before onboarding |

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | Reconciliation is candidate lookup, not clustering ER; score scales not comparable |
| Operational | Single user, in-memory; Wikidata path needs internet |
| Developer friction | Not an embeddable service; API v0.2 pending REST redesign with breaking changes [CLAIM-or-04] |
| Licensing | BSD, none |
INV-or-01: *Target* OpenRefine 3.10.1. *Limitation:* cleaning/reconciliation actions are not auditable into a governed graph. *Root cause* governance (proven: standalone project files). *Options:* (a) document OpenRefine as a pre-processing step; (b) reconciliation endpoint on EOIP so OpenRefine can link to the enterprise graph; (c) in-platform cleaning workspace emitting claims with provenance. *Selected:* (b) first. *POC:* OpenRefine reconciles a CSV against an EOIP service on 1k rows; success = results include ACL filtering (unauthorised entities never returned), p95 < 500 ms per batch of 10 queries (target). *Decision:* EXPERIMENT. No seed hypothesis targets OpenRefine.

## 10. Deployment, licensing, viability
Local Java app/desktop installers, BSD, air-gap viable except Wikidata. Wikidata data itself is CC0 (from memory, conf 0.7; verify before redistribution). No legal trigger found.

## 11. Competitive delta vs EOIP baseline
No reconciliation API or interactive cleaning surface in baseline (BL-34 deterministic person identity; BL-35 partial review queue). OpenRefine contributes protocol and UX patterns, not engine.

## 12. Cards
STR-or-01..04; INV-or-01.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Reconciliation API server (CAP-31, CAP-59-adjacent) | BUILD |
| External authority lookup (CAP-42) | INTEGRATE |
| Interactive cleaning UI (CAP-71) | DEFER |
| Embedding OpenRefine | REJECT |

## 14. Tests and acceptance
Conformance test of EOIP endpoint against the v0.2 spec test bench (if available; UNVERIFIED); OpenRefine round-trip; ACL-leak test.

## 15. Risks and open questions
Spec v0.2 to REST redesign churn; score semantics; whether Wikidata dependency violates air-gap defaults (yes unless mirrored).

## Appendix A — Research-dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | BSD, active |
| D2 | 2 | cleaning + reconciliation |
| D3 | 4 | local server + remote services |
| D4–D8 | N/A | no graph storage/query |
| D9 | 2 | file import |
| D10 | 2,5 | candidate scores, no merge model |
| D11 | N/A | |
| D12 | N/A | |
| D13–D14 | N/A | |
| D15 | 3,8 | review UX |
| D16 | 3 | web UI |
| D17 | 5 | HTTP API |
| D18–D19 | 3 | none (single-user) |
| D20 | 7 | no numbers |
| D21 | 10 | BSD |
| D22 | 5 | open protocol |
| D23 | N/A | |
| D24 | 1 | manual and spec read |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-31 | partial (candidate matching) | or-03 | BL-36 absent | BUILD endpoint | P2 |
| CAP-42 | partial | or-04 | n/a | INTEGRATE | P3 |
| CAP-71 | partial | or-03 | n/a | DEFER | P3 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-or-01 | master | BSD-style licence; copyright Google 2010 and OpenRefine contributors | Officially documented | https://github.com/OpenRefine/OpenRefine/blob/master/LICENSE.txt | 2026-10-18 | 0.9 | none |
| CLAIM-or-02 | 3.10.1 | release 2026-03-04; commits 2026-10-23 | Officially documented | https://github.com/OpenRefine/OpenRefine/releases.atom | 2026-10-18 | 0.95 | none |
| CLAIM-or-03 | 3.10 | reconciliation workflow, scores, properties, auto-match, local services, create-new-item | Officially documented | https://openrefine.org/docs/manual/reconciling | 2026-10-18 | 0.85 | none |
| CLAIM-or-04 | Reconciliation API v0.2 | CG Final report 2023-04-10; editors; not a W3C Standard; adds auth, type hierarchies, per-feature scores, property-only; REST redesign planned | Officially documented | https://w3c.github.io/cg-reports/reconciliation/CG-FINAL-specs-0.2-20230410/ | 2023-04-10 / 2026-10-18 | 0.85 | none |

## Appendix D — Assumptions
Internals (clustering, history format) from general knowledge; Wikidata endpoint specifics not verified (search found nothing specific).
