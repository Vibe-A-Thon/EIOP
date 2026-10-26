# C15 - Backstage, Port, Cortex (software catalogs / service-ownership graphs)

| Field | Value |
|---|---|
| Registry ID | T-C15-backstage |
| Tier | B - service/ownership graph patterns; one OSS reuse candidate (Backstage), two SaaS references |
| Versions examined | Backstage v1.56.2 (2026-10-22); Port Ocean framework Apache-2.0 (PyPI `port-ocean`, version not recorded); Cortex: no public version |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V29 |

## 1. Identity, status, tier, sources

| Product | Owner | Licence / class | Status | Claim |
|---|---|---|---|---|
| Backstage | Spotify origin; CNCF project (stage link says Incubation) | Apache-2.0, permissive | active, ~34.7k stars, pushed 2026-10-25 | [CLAIM-backstage-01] |
| Port | Port (commercial) | proprietary SaaS; Ocean integrations framework Apache-2.0 | active | [CLAIM-backstage-05] |
| Cortex | Cortex (commercial) | proprietary managed SaaS | active; pricing not published | [CLAIM-backstage-06] |

Only Backstage is deep-dived; Port and Cortex are covered where public evidence exists. Name collision: none material.

## 2. Problem and workloads

Single pane of ownership: who owns a service, what it depends on, which APIs it provides/consumes, whether it meets standards. Workflows: `catalog-info.yaml` in repo, auto-registration through templates, scorecards (Cortex), blueprint-driven self-service actions (Port). Answers EOIP reference questions "who owns / what depends on this" but not "who changed this class".

## 3. Feature inventory

| Feature | Backstage | Port | Cortex |
|---|---|---|---|
| Typed entity catalog (Component, API, System, Domain, Resource, User, Group, Location, Template) | present | blueprints (user-defined) | present (entity types) |
| Relations derived from spec (`ownedBy`, `dependsOn`, `providesApi`, `partOf`...) | present, read-only, derived | relations on blueprints | dependency/relationship map |
| Ingestion: YAML in Git, providers/processors, external sources | present | Ocean + 100+ integrations | 50+ integrations |
| Scorecards / standards checks | plugin | scorecards | core differentiator (CQL) |
| Self-service actions | Software Templates | actions | present |
| Self-hosted | yes | integrations only; single-tenant by sales | managed SaaS; on-prem unconfirmed |
| Plugin ecosystem | very large | limited | limited |
| Temporal/lineage history | absent | NOT PUBLICLY VERIFIED | NOT PUBLICLY VERIFIED |

## 4. Architecture

```
Backstage: frontend app (plugins) -> backend plugins (each own logical DB, Knex)
   catalog backend: providers -> processors -> entities+relations -> PostgreSQL
   search, TechDocs, Kubernetes, Templates as plugins
Port: SaaS tenant (blueprints/entities/relations) <- Ocean integrations (self-hostable, Helm/Docker)
```

## 5. Under-the-hood reconstruction

Backstage: entity = `apiVersion/kind/metadata/spec`; required spec fields per kind (Component: `type`, `lifecycle`, `owner`; API: also `definition`; Resource: `owner`,`type`); descriptor files must not contain relations, the catalog derives bidirectional pairs from spec fields [CLAIM-backstage-02]. Storage: each plugin has its own logical database through Knex; PostgreSQL preferred for production, SQLite for in-memory testing [CLAIM-backstage-03]. Processing loop (provider -> processor -> stitching), refresh cadence and permission framework: not read in this run, UNVERIFIED. Updates: owners change YAML via Git, catalog refreshes after a delay [CLAIM-backstage-04]. Port: blueprint/entity/relation/property model, entities populated continuously by integrations [CLAIM-backstage-05]. Cortex internals: NOT PUBLICLY VERIFIED beyond CQL scorecards [CLAIM-backstage-06].

## 6. Inferred requirements

Ownership as a first-class derived edge; descriptor-in-repo as source of truth; kind-specific required fields; unprocessed-entity surfacing for failures.

## 7. Performance and resource model

No benchmarks found. Backstage: Node service plus PostgreSQL; footprint scales with entity count and processing loop (hypothesis). Failure modes: catalog drift when YAML is stale, "Unprocessed Entities" for invalid descriptors [CLAIM-backstage-04].

## 8. Strengths

STR-backstage-01 descriptor-in-Git with derived relations. STR-backstage-02 small fixed ontology (kinds + relations) giving uniform ownership queries. STR-backstage-03 per-plugin DB isolation. STR-backstage-04 Apache-2.0, self-hosted, CNCF. STR-port-01 user-defined blueprints (schema-as-config).

## 9. Limitations

| Class | Finding |
|---|---|
| Algorithmic | catalog is entities+relations only; no code symbols, no multi-hop analytics (hypothesis from docs scope) |
| Operational | needs own Node app build and customisation; PostgreSQL |
| Friction | relies on teams maintaining YAML; Cortex CQL criticised as brittle (third-party) [CLAIM-backstage-06] |
| Licensing | Port/Cortex SaaS, not embeddable; Port self-host limited to integrations |
| Evidence | Port/Cortex pricing and deployment from third-party pages |

## 10. Deployment, licensing, viability

Backstage: self-hosted, air-gap viable (npm supply chain to mirror), Apache-2.0, OEM-friendly; plugin licences vary. Port: SaaS first; single-tenant by contract; violates "no mandatory cloud" as a dependency. Cortex: SaaS; reference only.

## 11. Delta vs EOIP

| Area | Catalog tools | EOIP |
|---|---|---|
| Ownership edges | first-class `ownedBy` | graph can model; no dedicated catalog connector row in baseline (Absent as product feature) |
| Source | Git YAML, integrations | BL-23 connectors incl. GitHub/GitLab/Kubernetes |
| Code depth | none | BL-42 symbols |
| Lineage/time | none | BL-41, BL-37 |
| Permissions | Backstage permission plugin (UNVERIFIED) | BL-18 Partial |

## 12. Cards

| ID | Card |
|---|---|
| STR-backstage-01 | [CLAIM-backstage-02,04] derived relations from declared specs; value: ownership/dependency edges; **integrate**: Backstage connector ingesting `catalog-info.yaml` and catalog API as SourceEvents; test: fixture catalog yields `ownedBy` edges with Git revision evidence |
| STR-backstage-02 | [CLAIM-backstage-02] small uniform kinds; **match** as ontology package "service-catalog" in C03 terms |
| INV-backstage-01 | Target Backstage 1.56.2. Limitation: catalog has no code-level or temporal layer [CLAIM-backstage-02]; cause semantics (hypothesis). Options: (a) ingest catalog only; (b) join catalog to code graph and incidents; (c) bitemporal ownership history. Selected (b) then (c). Benchmark: answer "who owns the service of class X" with 100% on fixture; ownership history as-of query. Defensibility: cross-source join. EXPERIMENT. |
| INV-backstage-02 | Port/Cortex SaaS-only core blocks air-gap [CLAIM-backstage-05,06]; licensing. Decision REJECT as dependency. No 10.5 seed applies. |

## 13. Decisions

CAP-42 catalog: INTEGRATE (Backstage as source system). CAP-69: BUILD (ownership join). CAP-17-style scorecards: EXPERIMENT (as EOIP validation rules). Port: REFERENCE-ONLY (Ocean connector pattern; Apache-2.0 REUSE patterns only). Cortex: REFERENCE-ONLY.

## 14. Tests/POC

Spin Backstage with PostgreSQL in Docker, export catalog entities via API, ingest. Acceptance: re-run yields zero delta; deleted entity produces tombstone (BL-25); entity ACL from group membership carried as `PermissionMetadata`.

## 15. Risks

Descriptor staleness yields false ownership; Backstage version churn; Port/Cortex terms may change. Open: Backstage permission framework mapping to BL-17; catalog scale limits.

## Appendix A - Dimensions

| Dim | Sec | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0 / SaaS |
| D2 | 2 | ownership graph |
| D3 | 4 | plugin backends |
| D4 | 5 | PostgreSQL per plugin |
| D5 | 5 | kinds + derived relations |
| D6 | N/A | catalog API |
| D7 | N/A | none |
| D8 | 5 | N/A |
| D9 | 3,5 | Git YAML, providers |
| D10 | 5 | owner field |
| D11 | 3 | none |
| D12 | N/A | none |
| D13 | N/A | none |
| D14 | N/A | none |
| D15 | 3 | scorecards |
| D16 | 3 | portal UI |
| D17 | 3 | plugins |
| D18 | 5 | permissions UNVERIFIED |
| D19 | 9 | single-org |
| D20 | 7 | none found |
| D21 | 1,10 | free vs SaaS |
| D22 | 11 | YAML export |
| D23 | N/A | none |
| D24 | 5 | doc pages only |

## Appendix B - Capabilities

| CAP | Tech | Claim | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-42 | native | 02 | BL-23 | INTEGRATE | P2 |
| CAP-26 | native | 04 | BL-23 | INTEGRATE | P2 |
| CAP-69 | partial | 02 | BL-41/42 | BUILD | P1 |
| CAP-47 | unknown | 03 | BL-20 | REFERENCE | P3 |

## Appendix C - Evidence

| ID | Product/date | Claim | Class | Source | Dates/conf | Contra |
|---|---|---|---|---|---|---|
| CLAIM-backstage-01 | v1.56.2 | Apache-2.0, 2026-10-22, 34.7k stars | Officially documented | https://github.com/backstage/backstage | 2026-10-26, 0.85 | none |
| CLAIM-backstage-02 | descriptor docs | kinds, required fields, derived relations | Officially documented | https://backstage.io/docs/features/software-catalog/descriptor-format | 0.85 | docs inconsistent on Template owner |
| CLAIM-backstage-03 | architecture docs | per-plugin DB, PostgreSQL | Officially documented | https://backstage.io/docs/overview/architecture-overview | 0.85 | MySQL reported to work |
| CLAIM-backstage-04 | catalog docs | Git workflow, unprocessed entities | Officially documented | https://backstage.io/docs/features/software-catalog/ | 0.8 | none |
| CLAIM-backstage-05 | Port docs, PyPI | blueprints, SaaS, Ocean Apache-2.0 | Officially documented | https://docs.port.io/build-your-software-catalog/ ; https://pypi.org/project/port-ocean | 0.65 | search summary |
| CLAIM-backstage-06 | Cortex | SaaS, CQL, unpublished pricing | Third-party report | https://cortex.io/compare/cortex-vs-port ; https://rywalker.com/research/cortex | 0.4 | vendor lists on-prem row |

## Appendix D - Assumptions

Backstage processing loop and permission framework assumed to exist as widely known but not verified here.
