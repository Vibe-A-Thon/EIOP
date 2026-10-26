# C17 — OpenAlex

| Field | Value |
|---|---|
| Registry ID | T-C17-openalex |
| Tier | B (open scholarly graph; candidate import source) |
| Versions examined | Rolling service, no semver (UNVERIFIED); quarterly free snapshot; docs at help.openalex.org (docs repo archived 2026-07-23) |
| Verified on | 2026-10-26 (brief said 2026-10-18; actual access date used) |
| Worker | V31 |

## 1. Identity, current status, tier, sources
OpenAlex is an open index of scholarly works, authors, sources, institutions, publishers, funders and topics run by OurResearch (nonprofit) [CLAIM-openalex-01]. Active; the old docs repo `ourresearch/openalex-docs` was archived 2026-07-23 and docs moved to help.openalex.org [CLAIM-openalex-02]. Data licence CC0 [CLAIM-openalex-03]. Tier B because it is the only realistic redistribution-safe literature graph to import.

## 2. Problem, workloads, workflows
Replace closed citation indexes. Workflows: (a) look up a DOI, get `referenced_works` and `cited_by_count`; (b) pull a topic slice via API filter; (c) load a snapshot into a store for local analytics; (d) disambiguate authors/institutions.

## 3. Feature inventory
| Feature | Status |
|---|---|
| Entity types: works, authors, sources, institutions, publishers, funders, topics (native IDs) | present [CLAIM-openalex-04] |
| REST API with free key ($1/day) | present [CLAIM-openalex-05] |
| Full snapshot, quarterly, free | present [CLAIM-openalex-02b] |
| Daily sync / changed-since filters | paid (Member+ $10k/yr, Partner) [CLAIM-openalex-05] |
| Curation (users fix errors) | present [CLAIM-openalex-04] |
| Claim-level provenance per field, contradiction/stance data | absent / UNKNOWN |
| Citation intent (supporting/contrasting) | absent (see scite, Semantic Scholar) |
| On-prem server product | absent (snapshot only) |

## 4. Architecture (public view)
```
 Crossref/PubMed/arXiv/ORCID/ROR... --> OpenAlex pipeline (closed) --> entity store
                                             |-> REST API (key, $ budget/day)
                                             |-> snapshot (JSONL per entity, quarterly free; daily paid)
 EOIP: snapshot/API -> SourceEvent -> validation gate -> GraphStore (connector never writes graph)
```

## 5. Under the hood
Pipeline internals NOT PUBLICLY VERIFIED beyond the entity taxonomy: native entities with minted IDs, vocabulary entities, component entities embedded in works (authorships, locations) [CLAIM-openalex-04]. Hypothesis: work-level records merge many upstream sources, so field-level origin is lost.

## 6. Requirements inferred
Import must be idempotent keyed on OpenAlex ID; store `retrieved_at`, snapshot date and licence; budget-aware rate limiting; mark values as third-party claims, never as ground truth.

## 7. Performance and resource model
No benchmark verified. Snapshot size UNVERIFIED (third-party blogs disagree: 324M vs 510.8M works, measured at different dates/filters) [CLAIM-openalex-06]; plan for hundreds of GB and filter by topic/year before loading. API cost is dollar-budgeted, not request-counted.

## 8. Strengths
CC0 means no redistribution constraint; stable IDs; citation edges plus topics give a ready literature graph; works offline from a snapshot (air-gap viable).

## 9. Limitations
| Class | Item |
|---|---|
| Intentional trade-off | Free tier limited to $1/day; freshness (daily sync) is paid [CLAIM-openalex-05] |
| Data quality | Algorithmic entity disambiguation can be wrong, hence curation [CLAIM-openalex-04] (hypothesis: author merges) |
| Semantics | No stance or claim data; citation = bare edge |
| Friction | Docs and pricing changed in 2026 (usage-based pricing); counts conflicting in third-party reports |

## 10. Deployment, licensing, viability
CC0 data; API terms separate (UNVERIFIED). Snapshot loadable in air-gapped one-node installs. No legal trigger on data; check API ToS only if used commercially.

## 11. Competitive delta vs baseline
EOIP has `ingestion/source_sync.py` and 30+ connectors (BL-23, BL-26) but no scholarly connector in the inspected baseline (UNKNOWN). Claims/contradictions exist (BL-39) and evidence manifests (BL-41), so imported citations fit as claims with source ref.

## 12. Cards
STR-openalex-01 | OpenAlex | CC0 open citation graph | CLAIM-03,04 | free research-domain content for customers | integrate | snapshot connector emitting SourceEvent v2, topic-filtered | idempotent re-import yields zero graph diffs.
INV-openalex-01 | target OpenAlex snapshot | no field-level provenance; root cause: data/semantics (hypothesis) | alternative: wrap each imported fact as a Claim with `source=openalex:<id>@<snapshot date>` (EOIP truth/evidence); worse if upstream conflicts are needed. Options: quick = store raw JSON on vertex; native = claim per field; long = multi-source reconcile with Crossref. Select native. POC: import 100k works, compare 1,000 DOIs against Crossref, metric disagreement rate. Defensibility: provenance plus governance. Decision EXPERIMENT. No seed hypothesis targets it.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| Literature graph import (CAP-26) | INTEGRATE (connector) |
| Citation provenance (CAP-38) | BUILD on EOIP claims |
| Semantic/vector search over abstracts (CAP-53) | DEFER |
| Paid daily sync | DEFER |

## 14. Tests / acceptance
Load a 100k-work topic slice offline; verify idempotency, licence stamp, ACL default public; query citation path of length 3; measure memory per 1M edges on in-process store.

## 15. Risks and open questions
Snapshot scale vs in-memory baseline (BL-43, U-06); API ToS for OEM use; whether abstracts are redistributable per-work (inverted-index form, UNVERIFIED).

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | owner, CC0, active |
| D2 | 2 | literature workflows |
| D3 | 4 | API plus snapshot |
| D4–D8 | N/A | closed internals, not verified |
| D9 | 4,6 | snapshot/API ingest |
| D10 | 5,12 | no field provenance |
| D11 | 3 | snapshots dated; no history API UNKNOWN |
| D12–D14 | N/A | not offered |
| D15 | 3 | curation |
| D16–D17 | 3 | API/CLI/agent access (help center) |
| D18–D19 | N/A | public data |
| D20 | 7 | cost model |
| D21 | 10 | pricing tiers |
| D22 | 6 | JSON entities, IDs |
| D23 | N/A | none found |
| D24 | 9 | counts conflict |

## Appendix B — Capability mapping
| CAP | OpenAlex | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-26 | native (API/snapshot) | 02,05 | BL-23 Implemented | INTEGRATE | P2 |
| CAP-38 | partial | 04 | BL-41 Implemented | BUILD | P2 |
| CAP-50 | snapshot works offline | 02b | n/a | REUSE | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Access | Conf | Contra |
|---|---|---|---|---|---|---|---|
| openalex-01 | OpenAlex 2026 | index of world's research | Official docs | https://help.openalex.org/ | 2026-10-26 | 0.8 | none |
| openalex-02 | 2026-07-23 | docs repo archived, docs moved | Official repo | https://github.com/ourresearch/openalex-docs | 2026-10-26 | 0.7 | none |
| openalex-02b | 2026 | free snapshot updated quarterly (search summary of official docs; not directly fetched) | Official docs via summary | https://docs.openalex.org/ | 2026-10-26 | 0.5 | none |
| openalex-03 | 2026 | data released under CC0 | Official docs | https://help.openalex.org/access/pricing | 2026-10-26 | 0.9 | none |
| openalex-04 | 2026 | native/vocabulary/component entity kinds; curatable | Official docs | https://help.openalex.org/data/ | 2026-10-26 | 0.85 | none |
| openalex-05 | 2026 | free $1/day key; Member $5k, Member+ $10k (daily sync), Partner $20k+ | Official docs | https://help.openalex.org/access/pricing | 2026-10-26 | 0.85 | blogs cite $0.10/day no-key |
| openalex-06 | 2026 | work counts 323,964,135 (9 Aug) vs 510.8M (29 Jun) | Third-party | https://jwatte.com/blog/openalex-open-index-of-research/ | 2026-10-26 | 0.3 | mutually conflicting |

## Appendix D — Assumptions
Access date 2026-10-26. Snapshot format (JSONL) assumed from prior knowledge, UNVERIFIED this run. Walden/topic versions not verified.
