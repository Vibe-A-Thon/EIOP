| Field | Value |
|---|---|
| Registry ID | T-C07-azure-digital-twins |
| Tier | B (twin graph + modelling language) |
| Versions examined | Azure Digital Twins service (docs page updated 2026-08-11); DTDL v2 / v3 (ADT) and v4 (IoT Operations) |
| Verified on | 2026-10-26 (brief date 2026-10-18; actual access date used) |
| Worker | V19 |

## 1. Identity, current status, tier, sources
Microsoft Azure PaaS for twin graphs of environments, modelled in DTDL (Digital Twins Definition Language). **Status check:** no retirement or deprecation announcement for the service or for DTDL was found; search surfaced only older retirements (2018 service, preview control-plane API versions) [CLAIM-adt-03]. The Learn overview was updated 2026-08-11 and still lists 3D Scenes Studio as *preview* [adt-01]. Microsoft separately offers **digital twin builder (preview) in Microsoft Fabric Real-Time Intelligence**, explicitly described as different from ADT; any ADT-to-Fabric migration plan: NOT PUBLICLY VERIFIED [adt-04]. Name collisions: IoT Hub device twins; Eclipse Ditto (Tier C record). DTDL repo (Azure/opendigitaltwins-dtdl): licences "CC-BY-4.0, MIT"; v4 is highest listed; v3 supported in ADT and IoT Plug and Play; v2 in ADT, IoT Central, IoT PnP; "based on W3C standards such as JSON-LD and RDF" [adt-02]. Proprietary service; open modelling language.

## 2. Problem and workloads
Digital twins of buildings, factories, energy networks; IoT-driven state; topology queries; 3D views. Workflow: upload DTDL models -> create twins and relationships -> ingest via IoT Hub/REST -> event routes to Functions/Event Hubs -> query graph or ADX history [adt-01]. EOIP relevance: modelling language and event-route patterns for asset/physical-operations tenants; mostly adjacent.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| DTDL models: properties, telemetry, commands, relationships, components | present | adt-01,02 |
| Twin graph, relationship properties | present | adt-01 |
| Query API with property, relationship, model conditions | present | adt-01 |
| Event routes (Event Hubs, Event Grid, Service Bus) | present | adt-01 |
| Data history to Azure Data Explorer | present | adt-01 |
| Explorer UI; 3D Scenes Studio | present; 3D is preview | adt-01 |
| Industry ontologies (DTDL-based) | present | adt-01 |
| Reasoning / OWL / SHACL | absent (not documented) | |
| Self-hosted / air-gap | absent | |
| Bitemporal, branching | absent (history via ADX only) | |

## 4. Architecture diagram
```
IoT Hub / REST / Logic Apps -> [ADT instance: model repo (DTDL) | twin graph | event router]
   -> query API  -> clients, Explorer, 3D Scenes
   -> event routes -> Event Hubs/Grid/Service Bus -> Functions, ADX data history
control plane: Azure RM; data plane: REST/SDK
```
Verified at box level; internals hypothetical.

## 5. Under-the-hood reconstruction
Verified: DTDL JSON-LD-based models define types; twins instantiate models; model validation on twin create/patch is implied by the documented model-type contract (inferred). Storage engine, indexing, query planner, consistency, and partitioning: NOT PUBLICLY VERIFIED beyond published service limits (not read). For EOIP: DTDL maps to ontology classes (Interface -> class, Property -> datatype property, Relationship -> object property with properties, Component -> composition); an importer can use JSON-LD parsing and EOIP's JSON-LD round-trip with loss accounting (BL-31). DTDL v3 adds features over v2 (not enumerated here: UNVERIFIED).

## 6. Inferred requirements
Strong typing at write; relationship properties; event emission on change; time-series history sidecar; model versioning (DTDL versioned `@id`s).

## 7. Performance and resource model
Service limits exist (documented separately; not read) - no numbers asserted. Consumption pricing unverified. Failure modes: cloud-region dependency; preview features lack SLA.

## 8. Strengths
Typed modelling language with component composition; event-routed twin updates; industry ontologies. Match: import DTDL into EOIP ontology (BL-32 gitops); exceed with SHACL validation (BL-29), bitemporal reads (BL-37) and branching diff (BL-38).

## 9. Limitations
Intentional: IoT/physical-asset focus, Azure-only. Licensing: service proprietary; DTDL open (CC-BY-4.0/MIT) - lowest-risk reuse. Maturity risk: 3D preview; Fabric twin builder overlap suggests strategy uncertainty (hypothesis, not evidence of retirement). No user-complaint data gathered.

## 10. Deployment/licensing/viability
Managed Azure only; no air-gap. Legal trigger: none for DTDL spec use (permissive per repo licence line), review service terms. DTDL import is air-gap safe.

## 11. Competitive delta
EOIP: CML mapping (BL-33), ontology as code (BL-32), no DTDL import, no physical-asset connectors. Relationship properties exist in LPG backends (BL-01..05). No gap on core graph.

## 12. Cards
STR-adt-01 | ADT/DTDL | Open typed modelling language for assets with composition and relationships | adt-02 | value: interoperability with Azure IoT estates | integrate | DTDL v2/v3 -> ontology importer with loss report | test: import Microsoft public DTDL building ontology, round-trip, zero silent loss.
INV-adt-01 | ADT | Azure-only, preview components, no reasoning | adt-01,04 | root cause: deployment/maturity, proven for preview label | alt: local twin graph on EOIP backends; worse for huge IoT telemetry | options: (1) DTDL importer, (2) twin-instance sync via SourceEvents, (3) native twin projection with time-series sidecar | selected 1 | POC above | defensibility: air-gap + reasoning | decision EXPERIMENT. No §10.5 seed targets this.

## 13. Per-capability decisions
CAP-08 typing: REUSE DTDL as import schema. CAP-37 evolution: REFERENCE DTDL versioning. CAP-69 digital thread: DEFER. CAP-52: n/a. ADT service: REJECT as dependency; Eclipse Ditto: see Tier C.

## 14. Tests/POC
DTDL importer test on published ontologies; validate generated SHACL shapes; confirm no retirement notice via Azure Updates before any commitment.

## 15. Risks and open questions
ADT vs Fabric twin builder trajectory; DTDL v4 scope; service limits; whether DTDL stays Microsoft-governed.

## Appendix A — Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | no retirement found |
| D2 | 2 | IoT twins |
| D3 | 4 | managed PaaS |
| D4 | 5 | not public |
| D5 | 3,5 | DTDL typing |
| D6 | 3 | query API |
| D7 | 3 | none |
| D8 | 7 | limits not read |
| D9 | 2,3 | IoT Hub, REST, routes |
| D10 | N/A | not examined |
| D11 | 3 | ADX history |
| D12 | N/A | |
| D13 | N/A | |
| D14 | N/A | |
| D15 | 5 | DTDL versions |
| D16 | 3 | Explorer, 3D |
| D17 | 3 | REST/SDKs |
| D18 | N/A | Azure RBAC, not read |
| D19 | N/A | |
| D20 | 7 | no numbers |
| D21 | 9,10 | proprietary service |
| D22 | 5,10 | JSON-LD basis |
| D23 | N/A | |
| D24 | 1 | official docs + repo |

## Appendix B — Capability mapping
| CAP | Technology | CLAIM | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-08 | native | adt-01,02 | BL-28 | REUSE | P2 |
| CAP-11 | native | adt-01 | BL-01 | REFERENCE | P3 |
| CAP-37 | partial | adt-02 | BL-32 | REFERENCE | P3 |
| CAP-36 | partial (ADX) | adt-01 | BL-37 | DEFER | P3 |
| CAP-50 | absent | adt-01 | yes | EOIP advantage | P1 |

## Appendix C — Evidence records
| CLAIM | product/version/date | claim | class | source | pub/access | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| adt-01 | ADT overview, updated 2026-08-11 | PaaS twin graphs, DTDL v3 link, query API, event routes, ADX data history, 3D Scenes Studio preview | Officially documented | https://learn.microsoft.com/en-us/azure/digital-twins/overview | 2026-08-11 / 2026-10-26 | 0.85 | |
| adt-02 | DTDL repo | v3 in ADT, v4 highest listed (IoT Operations), CC-BY-4.0 + MIT, JSON-LD/RDF based | Officially documented | https://github.com/Azure/opendigitaltwins-dtdl | n/d / 2026-10-26 | 0.75 | no release dates visible |
| adt-03 | ADT retirements | only legacy 2018 service and 2023 preview API retirements found; none for current service | Reasoned inference (absence) | https://github.com/microsoft/azure-digital-twins-java/blob/master/README.md ; https://azure.microsoft.com/en-us/updates/azure-digital-twins-controlplane-preview-api-retirement-20210631 | 2020-23 / 2026-10-26 | 0.5 | Azure Updates feed not fully searched |
| adt-04 | Fabric digital twin builder (preview) | distinct from ADT; low-code ontology; announced Build 2025 | Officially documented | https://learn.microsoft.com/en-us/fabric/real-time-intelligence/digital-twin-builder/overview | 2025 / 2026-10-26 | 0.6 | current preview state unchecked |

## Appendix D — Assumptions
"Azure Digital Twins and DTDL" = the current (2020+) service. Cross-ref C07-microsoft-graph-copilot-fabric (Fabric twin builder overlap).
