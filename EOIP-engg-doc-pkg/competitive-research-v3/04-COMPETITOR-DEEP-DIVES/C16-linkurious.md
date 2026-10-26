| Field | Value |
|---|---|
| Registry ID | T-C16-linkurious |
| Tier | B (investigation product + SDK) |
| Versions examined | Ogma 6.1.0 (docs nav; Ogma 6.0 announced 2026-02-24); Linkurious Enterprise manual 4.3.14 (latest release date UNVERIFIED; 4.1 was April 2025) |
| Verified on | 2026-10-26 |
| Worker | V30 |

## 1. Identity and status
Linkurious SAS: **Linkurious Enterprise** (complete investigation platform) embeds **Ogma** (commercial JS graph-viz library) [CLAIM-lk-01]. Both active. Compare separately: Ogma = rendering library; Enterprise = visual-intelligence product.

## 2. Problem and workflows
Financial-crime/AML, cyber, supply-chain analysts explore graph databases visually: search, expand, alerts, case reports, collaboration. Enterprise adds server (logic layer) between UI and database.

## 3. Features
| Feature | Ogma | Enterprise |
|---|---|---|
| WebGL-first renderer; Canvas/SVG supported (docs) | present [CLAIM-lk-02] | via Ogma |
| Layouts incl. GPU layout (5.0), grouping, clustering | present | present |
| Annotations (6.0 rewritten: comments, polygons, undo) | present | present |
| Time/attribute filters, maps, export (PNG/SVG/PDF/Excel) | present | present |
| Connectors: Neo4j, Neptune, JanusGraph, Oracle SQL/PGQ plugin | present | Neo4j, Neptune, Memgraph, Spanner Graph, BigQuery, Cosmos DB [CLAIM-lk-03] |
| RBAC by group, property-key access rights, SSO (LDAP, AD, Azure AD, OIDC, SAML2) | n/a | present [CLAIM-lk-03] |
| Alerts, case management | n/a | present |
| Docker/air-gap | n/a | on-prem + cluster mode documented; Docker/air-gap not stated |
| Accessibility | UNVERIFIED | UNVERIFIED |

## 4. Architecture
```
Browser (Ogma view) <-> Linkurious server (logic layer: auth, RBAC, query rewrite,
   alerts, cache, cluster mode) <-> graph DB(s)
Ogma standalone: app code <-> own API <-> DB
```
## 5. Reconstruction
The manual states access policies are enforced in the **server-side logic layer** with user groups and property-key rights (so filtering precedes the client) [CLAIM-lk-03]; a connector abstraction maps product features to Cypher/Gremlin/SQL graph dialects (hypothesis from the connector list). Ogma internals closed.

## 6. Requirements inferred
Server-mediated queries; property-level ACL; alerting over graph patterns; reproducible case reports.

## 7. Performance
Vendor claims (Ogma): "25,000 nodes in less than 1 second", "tens of thousands of nodes almost instantly even on a 5-year-old GPU"; older page: ~10,000 nodes in one second, "up to 40x faster than other solutions"; no benchmark details, hardware or dataset [CLAIM-lk-02]. Vendor advises server-side algorithms for weak clients. Independent: none.

## 8. Strengths
Product-level proof that a server logic layer with property-key ACL makes visual exploration safe; alerts; broad DB connectors. STR-lk-01: server-enforced property-level access. STR-lk-02: annotation/undo in the canvas.

## 9. Limitations
Commercial, licence terms not public ("commercial JavaScript library", trial) [CLAIM-lk-02]; Enterprise is server product, not an embeddable OSS component; Memgraph/Neo4j/Neptune coverage but not HugeGraph (not stated). Hypothesis: copies of subgraph in the browser remain exposed.

## 10. Deployment and licensing
Enterprise on-prem; air-gap not stated (NOT PUBLICLY VERIFIED). Ogma OEM/redistribution terms NOT PUBLICLY VERIFIED. Legal-review trigger: yes.

## 11. Delta vs baseline
BL-54 UI has no server-side logic layer for graph-visual queries beyond EOIP's API; EOIP's ACL model (derivation-aware, per ADRs) is stricter than property-key rights in principle, but unproven in UI.

## 12. Cards
STR-lk-01/02 above. INV-lk-01 | target Linkurious Enterprise 4.x; limitation: closed server product with vendor-specific alert model; cause: governance/licensing; alternatives: (a) integrate as external viewer on Neo4j backend, (b) native investigation workspace + alerts via EOIP events (BL-52), (c) permission-correct aggregated exploration; selected (b); POC: AML-style 100k edge graph, 3 analyst roles, zero leaked properties in HAR; decision EXPERIMENT.

## 13. Decisions
CAP-71 BUILD (reference its workflow); Ogma CAP-70 REJECT dependency; Enterprise INTEGRATE only as customer-chosen external viewer; CAP-45 REUSE concept.

## 14. Tests
Trial Enterprise on Neo4j sample: check HAR for filtered properties; time Ogma 25k render on mid GPU; evaluate alert latency.

## 15. Risks
Terms unknown; vendor acquisition/roadmap; parity chase.

## Appendix A
| Dim | Sec | Summary |
|---|---|---|
| D1-D3 | 1-3 | library vs product |
| D4,D5 | 4,5 | logic layer |
| D6 | N/A | uses external DB |
| D7,D8 | 7 | vendor claims |
| D10 | 5,8 | RBAC |
| D11,D12 | 10 | unknown terms |
| D13,D21 | 3 | connectors |
| D14 | 3 | a11y unknown |
| D15-D17 | N/A | not examined |
| D18-D24 | 9,15 | see |

## Appendix B
| CAP | Tech | CLAIM | Baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-71 | native | 03 | BL-54 | BUILD | P1 |
| CAP-45 | enterprise-only | 03 | BL-19 partial; BL-18 absent at baseline | REUSE concept | P2 |
| CAP-70 | native (Ogma) | 02 | BL-54 | REJECT | P3 |

## Appendix C
| CLAIM | prod/ver/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-lk-01 | Ogma 6.1.0; Ent. 4.3.14 | versions, Ogma inside Enterprise | verified | doc.linkurious.com; linkurious.com/blog | 2026-02-24 / 10-26 | 0.75 | Ent. latest unknown |
| CLAIM-lk-02 | Ogma pages | WebGL-first, node-count claims, commercial | vendor | linkurious.com/ogma; doc.linkurious.com/ogma | / 10-26 | 0.6 | two pages differ on counts and on Canvas/SVG |
| CLAIM-lk-03 | Ent. 4.3.14 | RBAC, SSO, connectors, on-prem | vendor docs | doc.linkurious.com/admin-manual | / 10-26 | 0.8 | none |

## Appendix D
Release date of 4.3.14 not established. BL-18 (source ACL in retrieval) absent at baseline snapshot; later commits (e.g. df724e4) may have changed this.
