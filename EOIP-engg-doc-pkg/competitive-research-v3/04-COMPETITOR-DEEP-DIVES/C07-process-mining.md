| Field | Value |
|---|---|
| Registry ID | T-C07-process-mining |
| Tier | B (grouped: Celonis, PM4Py, OCEL 2.0; event-graph patterns for CAP-80) |
| Versions examined | OCEL 2.0 specification (2023-10-16); PM4Py PyPI 2.7.23.11 (release date UNVERIFIED; requires Python >= 3.11); Celonis platform (SaaS, unversioned) |
| Verified on | 2026-10-26 (brief date 2026-10-18; actual access date used) |
| Worker | V19 |

## 1. Identity, current status, tier, sources
Three members. **OCEL 2.0** (Object-Centric Event Log): open standard from the Chair of Process and Data Science, RWTH Aachen (copyright 2024-2026); spec dated 2023-10-16; three exchange formats: relational SQLite, XML, JSON; adds object-to-object relations, qualified relations to events, and object attribute changes over time; designed backward-compatible with OCEL 1.0 [CLAIM-pm-01,02]. **PM4Py**: Python process-mining library, managed by PIS - Process Intelligence Solutions (Fraunhofer FIT spin-off); repo github.com/process-intelligence-solutions/pm4py; **licence AGPL-3.0 (PyPI: AGPL-3.0-or-later) with a separate commercial licence** - network-copyleft, hard EOIP constraint, legal-review trigger [pm-03,04]. OCEL support in PM4Py not confirmed on the page read (an `ocel` extra exists) [pm-03]. **Celonis**: proprietary SaaS process-intelligence platform; "Objects and Events" object-centric data model and Object-Centric Process Mining (OCPM); PQL (Process Query Language, 150+ operators per a 2022 chapter) [pm-05,06]. Related: C07-servicenow-kg, C07-palantir-foundry.

## 2. Problem and workloads
Reconstruct how work actually flows from event logs (ERP, ticketing), find bottlenecks, conformance deviations, rework. Case-centric logs force one case ID; object-centric logs let order, delivery, invoice objects share events, avoiding convergence/divergence distortions. Example: Order-to-Cash order branches into deliveries and invoices [pm-06]. EOIP relevance: CAP-80, journey J3 (incident <-> deployments correlation via event windows) and J15 (policy/contract/team impact in non-IT orgs).

## 3. Feature inventory
| Feature | OCEL 2.0 | PM4Py | Celonis |
|---|---|---|---|
| Object-centric event model | spec | listed `ocel` extra (details unverified) | Objects and Events (docs) |
| Discovery, conformance, performance | n/a | present (library scope; specifics unverified here) | present (marketing) |
| Query language | none | Python API | PQL (native OCPM support) |
| Exchange formats SQLite/XML/JSON | yes | partly unverified | unverified |
| Prebuilt connectors/quickstarts | n/a | no | yes (prebuilt object/event types via quickstarts) |
| Self-host / air-gap | n/a (format) | yes (pip) | no (SaaS) |
| AI/agents | n/a | n/a | marketed "process-intelligent AI" (unverified) |

## 4. Architecture diagram
```
Source systems -> extraction -> event table(s) + object table(s) + E2O + O2O relations
   OCEL 2.0 file (SQLite | XML | JSON)  <-> PM4Py (discover/conform/perf) 
   Celonis: Objects&Events data model -> PQL -> analyses/agents (SaaS)
EOIP projection: SourceEvent -> Event node -[involves(qualifier)]-> Object node ; Object -[rel]-> Object
```

## 5. Under-the-hood reconstruction
OCEL 2.0 relational schema (from spec): event, object, event-object (qualified), object-object (qualified), object-attribute-change tables - effectively a bipartite temporal graph [pm-01,02]. This maps 1:1 onto a property graph: Event and Object nodes, qualified E2O edges, O2O edges, attribute changes as dated property revisions - compatible with EOIP bitemporal reads (BL-37). Celonis internals (storage, PQL execution) NOT PUBLICLY VERIFIED beyond: foreign-key relationships drive implicit joins, case-centric single-perspective snowflake vs object-centric many-perspective model [pm-05,06]. PM4Py algorithm internals: not examined; discovery algorithms are published research (reuse ideas, not code, due to AGPL).

## 6. Inferred requirements
Ordered event timestamps with qualified object links; object lifecycle attribute history; extraction of event logs from SourceEvents; perspective switching without remodelling (object-centric); conformance checking against a reference process.

## 7. Performance and resource model
No benchmarks examined. Process mining cost scales with events x object relations; object-centric flattening can blow up row counts (hypothesis). Failure modes: missing timestamps, clock skew, partial logs.

## 8. Strengths
OCEL 2.0 gives a vendor-neutral, graph-shaped interchange. PM4Py is the reference research implementation. Celonis shows commercial value of object-centric views. Match: EOIP ingests OCEL as a CML mapping; exceed by joining process graph to ontology, ACLs and evidence.

## 9. Limitations
Licensing: PM4Py AGPL (strong legal flag; EOIP may only run it as a separate, unmodified, user-installed tool or reimplement algorithms from papers); Celonis proprietary. Intentional: analytics rather than a persistent KG; process graph usually rebuilt. Friction: log-extraction effort. Hypothesis: low-quality timestamps degrade results. No complaint data gathered.

## 10. Deployment/licensing/viability
OCEL 2.0: open format (spec licence not retrieved; RWTH copyright) - safe to implement. PM4Py: self-hosted, air-gap OK technically, AGPL network-copyleft. Celonis: SaaS only, no OEM. Legal review triggers: AGPL, commercial dual licence.

## 11. Competitive delta
EOIP has wisdom graph PLANNED (BL-56), event log and replay (BL-24), temporal graph (BL-37/38), graph algorithms (BL-43), no process-mining or OCEL support (CAP-80 absent in baseline). Opportunity: event graph from Jira/Git/CI SourceEvents for J3.

## 12. Cards
STR-pm-01 | OCEL 2.0 | Open object-centric, graph-shaped event interchange | pm-01,02 | value: process intelligence without vendor lock-in | integrate | OCEL SQLite/JSON importer-exporter via CML; Event/Object nodes | test: import OCEL 2.0 sample logs, export, structural equality.
STR-pm-02 | Celonis | Perspective switching on one object-centric model | pm-05,06 | value: J15 cross-domain views | exceed | query templates over event graph | test: three perspectives answered from one graph.
INV-pm-01 | PM4Py | AGPL blocks embedding | pm-03,04 | root cause: licensing, proven | alt: clean-room algorithms from papers or process boundary; worse for effort | options: (1) optional external tool, (2) native directly-follows/conformance, (3) event-graph analytics on backend | selected 1 then 2 | POC: compare DFG output vs PM4Py on public logs, equality of edge counts | defensibility: integrated ACL+provenance | decision EXPERIMENT. Seed hypotheses in §10.5: none targeting this entry identified.

## 13. Per-capability decisions
CAP-80: EXPERIMENT (OCEL importer + event-graph projection). CAP-36 event sourcing: REUSE existing replay (BL-24). CAP-65 temporal analytics: BUILD simple DFG on backend. PM4Py: REFERENCE-ONLY/INTEGRATE as external process pending legal review; Celonis: REJECT as dependency.

## 14. Tests/POC
OCEL 2.0 sample log import; SourceEvent -> OCEL export from Jira JSON connector (BL-23); DFG cross-check; J3 query: deployments within a window before incident, labelled correlation not causation.

## 15. Risks and open questions
PM4Py release date and OCEL 2.0 coverage; spec licence text; Celonis OCDM schema (docs gated behind login); event-log quality.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | AGPL; spec 2023 |
| D2 | 2 | process analytics |
| D3 | 4 | pipeline |
| D4 | 5 | relational OCEL tables |
| D5 | 5 | qualified relations |
| D6 | 3 | PQL; Python |
| D7 | N/A | conformance noted only |
| D8 | N/A | not examined |
| D9 | 6 | log extraction |
| D10 | N/A | |
| D11 | 5 | attribute change history |
| D12 | 3 | process discovery only |
| D13 | N/A | |
| D14 | N/A | |
| D15 | N/A | |
| D16 | N/A | |
| D17 | 3 | PM4Py API |
| D18 | N/A | |
| D19 | N/A | |
| D20 | 7 | no figures |
| D21 | 9,10 | AGPL/commercial; SaaS |
| D22 | 1,12 | open format |
| D23 | N/A | not examined |
| D24 | 1 | docs partly gated |

## Appendix B — Capability mapping
| CAP | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-80 | native (all) | pm-01,05 | BL-56 Planned | EXPERIMENT | P2 |
| CAP-36 | partial | pm-01 | BL-24 | REUSE | P2 |
| CAP-65 | partial | pm-06 | BL-37 | BUILD | P3 |
| CAP-77 | n/a | pm-03 | - | flag AGPL | P1 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| pm-01 | OCEL 2.0 / 2023-10-16 | Spec dated Oct 16 2023; SQLite, XML, JSON formats; object changes and qualified relations | Officially documented | OCEL 2.0 Specification, https://arxiv.org/pdf/2403.01975 | 2023-10 / 2026-10-26 | 0.75 | |
| pm-02 | ocel-standard.org | RWTH Chair of Process and Data Science copyright 2024-2026; format for object-centric logs | Officially documented | https://www.ocel-standard.org/ | 2026 / 2026-10-26 | 0.7 | spec licence not stated |
| pm-03 | PM4Py repo | AGPL-3.0, commercial licence available; managed by PIS (Fraunhofer FIT spin-off); `ocel` extra | Officially documented | https://github.com/process-intelligence-solutions/pm4py | n/d / 2026-10-26 | 0.8 | releases section empty; OCEL 2.0 support unconfirmed |
| pm-04 | PM4Py on PyPI | version 2.7.23.11, AGPL-3.0-or-later, Python >= 3.11 | Officially documented | https://pypi.org/pypi/pm4py/json | n/d / 2026-10-26 | 0.6 | upload date not read; version string odd, recheck |
| pm-05 | Celonis docs | Objects and Events is OCPM base; case-centric vs object-centric models; PQL native OCPM | Officially documented (search summary; docs gated) | https://docs.celonis.com/en/object-centric-process-mining.html ; https://docs.celonis.com/en/data-model-design.html | n/d / 2026-10-26 | 0.55 | login redirect on direct fetch |
| pm-06 | PQL | 150+ operators, FK-based implicit joins | Peer-reviewed chapter | https://www.springerprofessional.de/en/celonis-pql-a-query-language-for-process-mining/20342470 | 2022 / 2026-10-26 | 0.5 | |

## Appendix D — Assumptions
Grouped record covers the three named members only; no other tools (ProM, Disco) assessed. PM4Py GitHub org is process-intelligence-solutions (older fraunhofer-fit repo assumed superseded - UNVERIFIED).
