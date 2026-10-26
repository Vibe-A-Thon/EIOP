# C13 — W3C PROV / PROV-O

| Field | Value |
|---|---|
| Registry ID | T-C13-prov-o |
| Tier | B (provenance model EOIP already emits from `mapping/executor.py`) |
| Versions examined | PROV-O W3C Recommendation, 30 April 2013 (PROV family: PROV-DM, -O, -N, -CONSTRAINTS, -XML, -AQ, -DICTIONARY) |
| Verified on | 2026-10-26 |
| Worker | V26 |

## 1. Identity, status, sources
PROV-O encodes PROV-DM in OWL 2; namespace `http://www.w3.org/ns/prov#`; editors Lebo, Sahoo, McGuinness [CLAIM-prov-01]. Standards-track Recommendation, stable since 2013, no successor verified (NOT PUBLICLY VERIFIED whether a W3C revision exists; confidence 0.6). W3C document licence (free to implement; no royalty-bearing patents verified — legal check not performed). Sources: W3C TR/prov-o; EOIP code.

## 2. Problem and workloads
Interchange of "who/what/when produced this data" across systems: Entity (thing), Activity (occurs over time), Agent (responsible party). Workflows: record that a graph node was derived from a source revision by a mapping run executed by a connector agent; audit "show me origin of this fact".

## 3. Feature inventory
| Term group | Contents | Status |
|---|---|---|
| Starting point | wasGeneratedBy, used, wasDerivedFrom, wasAttributedTo, wasAssociatedWith, actedOnBehalfOf, wasInformedBy, startedAtTime, endedAtTime [CLAIM-prov-01] | spec |
| Expanded | Collection, Bundle, Person, Organization, SoftwareAgent, Location; specializationOf, alternateOf, generatedAtTime, hadPrimarySource, wasRevisionOf, invalidatedAtTime [CLAIM-prov-01] | spec |
| Qualified | Influence classes (Usage, Generation, Association…) with qualifiedX properties [CLAIM-prov-01] | spec |
| Tooling (ProvToolbox, prov Python) | UNVERIFIED this session | — |
| Confidence, ACL, signatures | absent from model (use PROV extensions / Bundles) | absent |

## 4. Architecture
```
 Entity <-wasGeneratedBy- Activity -wasAssociatedWith-> Agent
   |  wasDerivedFrom          |used
   v                          v
 Entity(source revision)   Entity(input)
 (Bundle = named graph holding provenance about provenance)
```

## 5. Reconstruction
Pure vocabulary: triples with unqualified binary relations; qualified pattern reifies relation as Influence node to carry time/role/plan. Temporal terms are instants (xsd:dateTime) on Activity/Generation/Invalidation — not bitemporal intervals on the assertion. Bundles + named graphs give provenance-of-provenance. Hypothesis: one-node-per-claim PROV (Entity=claim, wasDerivedFrom=evidence span) maps cleanly to EOIP BL-39/BL-41 records. No storage, query or security semantics: inherits those of the host store.

## 6. Inferred requirements
Emit stable IRIs for activity/agent/entity; keep PROV triples out of the entity-permission path unless source ACL applies to them (BL-18 gap); include `invalidatedAtTime` for tombstones (BL-25).

## 7. Performance
Not applicable to a vocabulary; cost = triple count. Unqualified PROV adds ~3 triples per derived entity in EOIP executor (reasoned from code); qualified form multiplies this. No numbers claimed.

## 8. Strengths
Universally understood; query by SPARQL; extensible; fits ontology bridge strategy. Match: already done for mapping; exceed: extend to claims, inference rules, LLM calls (SoftwareAgent + model version).

## 9. Limitations
| Class | Item |
|---|---|
| Intentional | no confidence, no trust model, no access control |
| Semantic | instants not intervals; no bitemporal assertion semantics |
| Friction | verbose in LPG backends (HugeGraph/Neo4j): needs edge-property encoding, RDF-star-style loss |
| Hypothesis | qualified pattern blows up edge counts |

## 10. Deployment/licensing
Spec only; zero runtime dependency; air-gap trivial. W3C licence — record, no legal conclusion.

## 11. Delta vs baseline
`mapping/executor.py` lines ~10–13 and 140–160 emit wasDerivedFrom (source resource revision), wasGeneratedBy (mapping-run activity), wasAttributedTo (connector agent) when `emit_prov_o` is set (BL-33). Only unqualified, three predicates; no `used`, `startedAtTime`, `wasInformedBy`, `invalidatedAtTime`; no PROV for claims/inference/LLM (BL-39, BL-41 use native EVIDENCED_BY/INGESTED_IN edges). Not emitted as Bundle; not tenant-scoped by construction (BL-20 Partial).

## 12. Cards
STR-prov-o-01 | PROV-O | interoperable provenance vocabulary | CLAIM-prov-01 | auditors and catalog tools read EOIP provenance without custom parsers | match | extend executor to `used`, `startedAtTime/endedAtTime`, Bundle per run | SHACL shape check + SPARQL "origin of X" returns source revision.
STR-prov-o-02 | PROV-O | qualified influence pattern | CLAIM-prov-01 | role/plan/time per derivation | exceed | qualified form only for claim-level records | round-trip losslessness test.
INV-prov-o-01 | PROV-O 2013 | no assertion-time semantics | root cause: semantics (proven: instants only) | pair PROV with BL-37 revision coordinates; PROV answers "how", bitemporal answers "when known/valid" | options: (a) annotate with `eoip:validFrom/knownAt`, (b) PROV-STAR, (c) native claim-provenance model projected to PROV on export | choose (c) | POC: export 1k claims, import into rdflib, compare coverage; metric: 100% evidence spans reachable | deps BL-31 loss accounting | defensibility: ACL-aware provenance projection | ADOPT. Seed hypotheses §10.5: none target this technology.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-38 provenance export | REUSE (extend existing) |
| CAP-38 internal claim model | keep native (BUILD done, BL-39/41) |
| CAP-40 lineage mapping | INTEGRATE with OpenLineage exporter |
| CAP-34 temporal in PROV | REJECT (use BL-37) |

## 14. Tests
Golden-file Turtle for a mapping run; SHACL validation of PROV shapes; tenant-leak test on provenance triples; LPG round-trip loss accounting.

## 15. Risks / open questions
Triple growth; ACL on provenance; whether to emit Bundles; PROV revision status unverified.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | W3C Rec 2013 |
| D2 | 2 | provenance interchange |
| D3–D4 | N/A | vocabulary only |
| D5 | 3,5 | OWL2 classes/properties |
| D6–D8 | N/A | host-store dependent |
| D9 | 11 | emitted at mapping time |
| D10 | 5,11 | evidence/attribution |
| D11 | 9 | instants only |
| D12–D14 | N/A | none |
| D15 | 3 | bundles |
| D16 | N/A | none |
| D17 | 12 | libraries unverified |
| D18 | 9 | no ACL |
| D19 | 11 | none |
| D20 | 7 | triple count |
| D21 | 10 | W3C licence |
| D22 | 9 | LPG loss |
| D23 | N/A | none identified |
| D24 | App C | primary spec |

## Appendix B — Capability mapping
| CAP | Native | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-38 | native vocab | prov-01 | BL-33,BL-41 | REUSE | P1 |
| CAP-40 | partial | prov-01 | BL-41 | INTEGRATE | P2 |
| CAP-09 | native OWL2 | prov-01 | BL-30 | REUSE | P3 |

## Appendix C — Evidence
| ID | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| prov-01 | PROV-O Rec 2013-04-30 | classes, term groups, namespace as listed | Officially documented | https://www.w3.org/TR/prov-o/ | 2013-04-30 / 2026-10-26 | 0.9 | none |
| prov-02 | EOIP HEAD | executor emits three PROV predicates when `emit_prov_o` | Observed in source code | packages/eoip/mapping/executor.py:140-160 | 2026-10-26 | 0.9 | none |

## Appendix D — Assumptions
No newer W3C PROV revision assumed; tooling not evaluated.
