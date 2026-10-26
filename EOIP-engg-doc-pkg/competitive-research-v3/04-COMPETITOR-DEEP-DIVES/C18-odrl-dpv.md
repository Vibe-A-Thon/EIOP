# C18-odrl-dpv — ODRL (usage policies) and DPV (Data Privacy Vocabulary)

| Field | Value |
|---|---|
| Registry ID | T-C18-odrl-dpv |
| Tier | B (policy/privacy vocabularies; BL-45, BL-46, BL-17) |
| Versions examined | ODRL Information Model 2.2 (W3C Rec, 2018-02-15); ODRL Vocabulary & Expression 2.2 (Rec); DPV v2.3 (GitHub "Latest", 28 Feb, year 2026 per secondary source); DPV v2.2 (23 Sep) and 2.2.1 hotfix (03 Nov) [years not shown on page]; DPV v2.0 paper (arXiv 2404.13426) |
| Verified on | 2026-10-26 |
| Worker | V32 |

## 1. Identity, current status, tier, and sources
**ODRL 2.2 = W3C Recommendation (2018)**; the Permissions & Obligations Expression WG ended; the model page offers errata only. A **W3C Workshop on the Future of ODRL (London, 20–21 July 2026)** led to a *draft* charter for a "Digital Policy Working Group" (start 2027-01-01, end 2028-12-31; chairs placeholders; planned five normative specs, ODRL 3.0 direction). No ODRL 2.3 or published successor Working Draft found [CLAIM-odrl-01, -02]. **DPV = W3C Data Privacy Vocabularies and Controls Community Group (DPVCG) output, i.e. NOT a W3C standard**; v2.3 is listed "Latest" on GitHub, preceded by v2.2 and v2.2.1; the DPV-ODRL guide is a *Draft Community Group Report* [CLAIM-dpv-01, -02]. DPV licence not read (CC-BY 4.0 per prior knowledge, conf 0.5).

## 2. Primary problem, workloads, workflows
ODRL: machine-readable permissions, prohibitions, duties, with constraints. DPV: taxonomy of processing, purposes, legal bases, data categories, TOMs, risks (GDPR-oriented, with AI and sector extensions). Workflows: attach an ODRL policy to a dataset; annotate processing records with DPV purpose and legal basis; DSAR classification (BL-46).

## 3. Feature inventory
| Feature | Status |
|---|---|
| ODRL Policy/Offer/Agreement, Permission/Prohibition/Duty, constraints, assigner/assignee | Rec 2.2 |
| ODRL Profiles mechanism | Rec 2.2 |
| ODRL formal semantics / evaluation engine | NOT in Rec (CG material only; UNVERIFIED) |
| DPV core + extensions (personal-data, risk, tech, AI, justifications, locations, sectors, legal) | CG v2.x |
| DPV-with-ODRL guide | draft CG report |
| Enforcement | absent in both (vocabulary only) |

## 4. Architecture (specification structure, conformance classes)
```
ODRL: Information Model -> Vocabulary & Expression (JSON-LD, RDF) -> Profiles
DPV : core + extension modules (RDF/OWL/SKOS) -> guides (e.g. DPV-ODRL)
Neither defines an enforcement point, evaluator or decision API.
```

## 5. Under-the-hood (formal semantics, complexity, what an implementation must do)
ODRL 2.2 is an RDF vocabulary with an information model; **no normative evaluation semantics**: conflict resolution, `odrl:conflict` strategies, constraint operators over time/location/purpose and "refinements" are left to implementers, which is why research and the 2026 workshop push for formalisation. An implementation must: choose a decision procedure (deny-overrides vs permit-overrides), define attribute mapping (what is `odrl:purpose`, `odrl:spatial`), enforce duties asynchronously, and keep policy provenance. DPV terms are SKOS/OWL concepts with subclass hierarchies; reasoning is subsumption only. Both are **open-world RDF vocabularies**: a policy that does not mention an action is not a prohibition; default-deny must be an explicit implementation rule — the opposite of EOIP's deny-by-default stance if left implicit.

## 6. Functional and non-functional requirements inferred
FR: store policies as versioned graph objects (audit, CAP-48); map ODRL/DPV concepts to authz attributes (CAP-45); record legal basis per processing; retention duties. NFR: policy decisions must be deterministic and logged; vocabulary version pinned per tenant.

## 7. Performance and resource model
Not applicable to vocabularies; decision latency depends on the chosen evaluator. No numbers.

## 8. Strengths and use-case advantages
Common vocabulary for privacy and usage-control interchange; DPV gives regulator-recognised terms (GDPR-oriented; EU AI Act extensions claimed by DPVCG, not verified). Match by mapping EOIP privacy modules (BL-46) to DPV IRIs for exports.

## 9. Limitations with root causes
| Class | Items |
|---|---|
| Algorithmic | no evaluation semantics; conflict handling undefined |
| Operational | ODRL 2.2 from 2018; successor WG not yet chartered (draft charter only); DPV is CG output with frequent releases |
| Friction | ODRL lacks legal-compliance concepts — DPV bridges but guide is draft; ABAC engines (Cedar/OPA/OpenFGA) are separate |

## 10. Deployment, licensing, redistribution, viability
Vocabularies are data files; air-gap: yes. W3C Rec patent policy for ODRL; DPV CG licence (CC-BY 4.0, unverified) allows redistribution with attribution — legal-review trigger only to confirm. No enforcement software included.

## 11. Competitive delta against EOIP baseline
BL-17 captures source `PermissionMetadata` and `acl_hash`; BL-18 source-ACL enforcement in retrieval is **absent**; BL-19 RBAC/ABAC on API actions; BL-45 egress policy; BL-46 privacy classification/DSAR/retention. EOIP has no ODRL import/export or DPV tagging. **Semantics**: ODRL/DPV are RDF vocabularies; EOIP authz is closed-world deny-by-default. An ODRL policy converted to EOIP ABAC loses duties, `odrl:conflict`, and refinements; an EOIP ACL exported as ODRL needs explicit prohibitions to preserve default-deny. Shared words ("permission") do not imply equivalent semantics.

## 12. Strength-adoption and inversion cards
STR-odrl-01 | DPV | regulator-aligned privacy taxonomy | CLAIM-dpv-01 | DSAR/RoPA interoperability | integrate | map `privacy/*` categories and purposes to DPV IRIs; version-pin | export validates against DPV vocabulary files; every purpose resolves to a DPV term or flagged custom.
INV-odrl-01 | ODRL | vocabulary without evaluation semantics | CLAIM-odrl-01,02 | semantics: proven | options: quick = import as metadata only; native = EOIP policy IR with explicit ODRL mapping and documented loss; long-term = adopt ODRL 3.0 if chartered | POC: 30 ODRL examples converted and evaluated by authz core, 100% decisions logged, losses listed | EXPERIMENT. Seed hypotheses: none targeted.

## 13. Per-capability decisions
CAP-45 EXPERIMENT (ODRL import into ABAC IR); CAP-46 BUILD (ACL enforcement, independent of ODRL); CAP-33 INTEGRATE (DPV categories); CAP-42 REFERENCE.

## 14. Concrete tests and acceptance
No ODRL conformance suite verified (W3C Rec had implementation experience only; UNVERIFIED). DPV: SHACL/OWL files in repo can validate exports (repository contents not enumerated). Acceptance: differential evaluation corpus built by us. **PROPOSED, not run.**

## 15. Risks and open questions
Digital Policy WG outcome (draft charter, may not pass); DPV release churn; DPV 2.3 year of release inferred; mapping of EU AI Act terms unverified.

## Appendix A — Dimension coverage
| Dim | § | Summary |
|---|---|---|
| D1 | 1 | Rec vs CG |
| D2 | 2 | policy, privacy |
| D3 | 4 | modules |
| D4 | N/A | data files |
| D5 | 3 | SKOS/OWL concepts |
| D6-D7 | 5 | no evaluation |
| D8-D9 | N/A | out of scope |
| D10 | 6 | provenance of policy |
| D11 | N/A | none |
| D12-D14 | N/A | out of scope |
| D15 | 12 | review |
| D16-D17 | N/A | none |
| D18 | 5,11 | default-deny |
| D19 | 6 | per-tenant pin |
| D20 | N/A | no cost |
| D21 | 10 | licence |
| D22 | 11 | loss |
| D23 | N/A | not assessed |
| D24 | App C | W3C + GitHub |

## Appendix B — Capability mapping
| CAP | Tech | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-45 | partial (vocab) | odrl-01 | BL-19 | EXPERIMENT | P2 |
| CAP-46 | absent | — | BL-18 absent | BUILD | P0 |
| CAP-33 | partial (DPV) | dpv-01 | BL-46 | INTEGRATE | P2 |

## Appendix C — Evidence records
| CLAIM | Product/date | Claim | Class | Source | Dates | Conf | Contra |
|---|---|---|---|---|---|---|---|
| odrl-01 | ODRL Information Model 2.2 | W3C Rec 2018-02-15 | Officially documented | https://www.w3.org/TR/odrl-model/ | 2018-02-15 / 2026-10-26 | 0.9 | none |
| odrl-02 | ODRL CG 2026 | Workshop 2026-07-20/21; draft Digital Policy WG charter 2027-01-01 to 2028-12-31; no ODRL 2.3 found | Officially documented (draft) | https://w3c.github.io/odrl/w3c-wg-draft-charter-2026/dpwg-draft-charter.html ; https://www.w3.org/2026/ODRLWS/report.html | 2026-09 / 2026-10-26 | 0.75 | charter may have changed |
| dpv-01 | DPV releases | v2.3 Latest (28 Feb), v2.2.1 (03 Nov), v2.2 (23 Sep); years not shown | Officially documented | https://github.com/w3c/dpv/releases | 2026-10-26 | 0.7 | year 2026 for 2.3 from Dublin Core page |
| dpv-02 | DPV-ODRL guide | draft CG report | Officially documented | https://w3id.org/dpv/guides/dpv-odrl | 2026-10-26 | 0.75 | none |

## Appendix D — Assumptions
DPV licence and ODRL lack of evaluation semantics (from Rec structure and workshop framing) inferred. No ODRL test suite search beyond one query.
