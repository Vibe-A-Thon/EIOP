# EOIP Competitive Research and Architecture Analysis

Research date: 2026-10-16, Asia/Calcutta. Baseline revision: `ccf9e2891070b9b10eb05791ef8cf4cd1ca08731`.

Companion execution specification: [CRAr.md](CRAr.md). Machine-readable comparison: [competitive-research-matrix.csv](competitive-research-matrix.csv).

### Navigation

- [Executive decision](#1-executive-decision)
- [Scope and evidence](#2-scope-intake-and-evidence-contract)
- [EOIP baseline and observed gaps](#3-eoip-baseline-and-concrete-gaps)
- [Selected product profiles](#4-recommended-product-profiles)
- [Scoring and matrices](#5-rubric-and-comparison-matrices)
- [All tool dossiers and inversions](#6-tool-dossiers-and-limitation-inversions)
- [Prioritized backlog](#7-prioritized-gap-backlog-and-inversion-traceability)
- [Architecture](#8-recommended-architecture-and-module-boundaries)
- [Connection factory](#9-universal-connection-factory-and-enterprise-source-coverage)
- [Formats and knowledge construction](#10-multiformat-acquisition-and-knowledge-construction)
- [Contracts, algorithms, API and UX](#11-concrete-designs-and-algorithms)
- [Migration](#12-migration-and-integration-plan)
- [Security and licensing](#13-security-legal-and-compliance-assessment)
- [Benchmark and QA](#14-benchmark-and-qa-plan)
- [Observability and recovery](#15-observability-delivery-and-recovery)
- [Playbooks and support](#16-operational-playbooks-and-support)
- [Roadmap and costs](#17-roadmap-capacity-and-cost-model)
- [Deliverable acceptance](#18-ecosystem-and-deliverable-acceptance)
- [Reproduction and remaining research](#19-reproduction-standards-and-remaining-research)

## 1. Executive Decision

Build a governed enterprise knowledge platform, not a new implementation of every competing database, editor and machine-learning library. Preserve EOIP's Python/FastAPI and React foundations. Reuse qualified semantic engines behind explicit interfaces; make connectors, parsers, stores, reasoners, model providers, workflows and presentation modules independently replaceable. Keep original EOIP code proprietary, with independently licensed dependencies and deployment-specific notices.

The product must support both deterministic semantics and probabilistic assistance. An embedding similarity, language-model answer, extracted diagram edge or suggested identity match is a proposal, not a logical entailment or an authorized write. Separate asserted, inferred, proposed, rejected and historical knowledge, and bind every result to source revisions and access policy.

### Top Five Opportunities

1. **Permission-preserving enterprise acquisition:** carry source ACLs, deletion, identity and revisions through crawl, extraction, graph, index, answer and export. Connector count alone is not the differentiator.
2. **Semantic correctness with inspectable limits:** publish exactly which RDF, OWL, SHACL and query profiles each configured engine supports. Reject unsupported constructs rather than issuing an apparently successful partial result.
3. **A portable operational ontology:** combine standards-based definitions and evidence with governed actions, dry-runs, approvals, idempotency, compensation and source-system read-back.
4. **A customizable but certifiable platform:** versioned plugin contracts, typed configuration, sandboxing, capability discovery, portable data, accessible generated forms and reproducible plugin qualification.
5. **A trustworthy living knowledge system:** incremental changes, provenance, temporal views, calibrated extraction, drift review and revocation propagation, backed by restart, migration and failure evidence.

These are design opportunities, not claims that all competitors lack these features or that EOIP already delivers them. Do not advertise competitive superiority without a comparable, licensed, reproducible evaluation.

## 2. Scope, Intake and Evidence Contract

### 2.1 Attachment Coverage

The complete 612-line UTF-8 attachment was read in numbered ranges 1-180, 181-360, 361-510 and 511-612, including the repeated instructions and landscape matrix. Attachment SHA-256: `16b46f814235cf0bf873512a8440830b258494b9a72972d346441bb401c23875`.

| Attachment lines | Obligation | Treatment in this package |
|---|---|---|
| 1-23, 125-145 | Roles, system baseline, scale, constraints, people and exclusions | Sections 1-4; explicit planning defaults and unresolved procurement decisions |
| 24-49, 146-171 | All 22 evaluation dimensions | Section 5 and the 55-row CSV; unverified dimensions remain ND |
| 52-92, 174-214 | Sixteen deliverables and acceptance | Sections 6-19 and deliverable closure table |
| 96-120, 219-540, 546-606 | All eight categories and named landscape entries | C01-C54; paired tools are distinguished within their dossier |
| 123 | Every named enterprise source, push/pull and file/media formats | Sections 9-10 and CRA-004..015 |
| 129 | Additional OWL API example | Supplemental C55, not silently omitted |
| 608 | Deterministic plus probabilistic architecture | Sections 8, 11 and CRA-016..028 |
| 611-612 | Two named Markdown files; no file-reference-only completion | This file and CRAr.md; evidence gates CRA-037 |

The later, broader eight-category inventory takes precedence over the earlier six-category summary. None of the 54 landscape rows is excluded. PoolParty/Graphwise are product aliases/transitions, not independent competitors. Foundry/AIP and SciBite are suites, not a single engine. OWL API is a library, not a database.

The owner subsequently delegated architecture choices and requested complete modularity and extensibility without a preferred competitor. Accordingly, the defaults below are explicit engineering decisions, not invented statements about existing infrastructure, staff, budget or customer contracts.

### 2.2 What This Research Does and Does Not Establish

This is public-documentation architectural reconstruction and selected local-code inspection, not proprietary-source reverse engineering or a hands-on qualification of 55 products. Vendor descriptions establish documented behavior, not independently measured performance. No competitor binaries were installed, private APIs accessed, license restrictions bypassed, customer data uploaded or competitor benchmark executed.

Evidence labels:

- **DOC:** identifiable official documentation, maintainer repository or normative standard was inspected.
- **LOCAL:** a specific local implementation was inspected; this does not certify the whole feature.
- **PROBE:** the stated bounded local behavior was executed and its output observed.
- **INFERENCE:** architectural consequence or suitability judgment derived from evidence; not a vendor admission.
- **ND:** not determined from adequate evidence, not a zero score or proof of absence.
- **PROPOSED:** a target, design, command or future acceptance requirement, not implemented behavior.

All public links were consulted on the research date unless explicitly described as a follow-up lead. Moving documentation and default branches are not immutable release evidence. Exact package versions, image digests, commercial editions, support terms and licensed evaluation rights must be pinned before procurement or a benchmark. A legacy page is labelled as such; it is not evidence of a current release.

Full source-level algorithms for closed-source products, patent freedom-to-operate, current negotiated prices, vendor SLAs, accessibility conformance and equal-hardware performance remain unqualified. These are work items, not facts to fill in with guesses. No weighted league table is calculated from incomparable categories and missing values.

## 3. EOIP Baseline and Concrete Gaps

### 3.1 Inspected Technology

| Layer | Current evidence | Conservative assessment |
|---|---|---|
| API/runtime | `pyproject.toml`: Python >=3.11, FastAPI, Pydantic, httpx, Uvicorn, MCP | Existing application stack; dependency ranges are not locked installed versions |
| Graph abstraction | `packages/eoip/graph/store.py`, `backends.py`; HugeGraph, Neo4j, Neptune and memory factories | Reuse the adapter boundary; capability strings do not establish backend conformance |
| Ontology | Manifest, RDF/JSON-LD mapping, custom reasoner, custom shape validator, SKOS and GitOps modules | Useful controlled-vocabulary foundations; not demonstrated generic OWL DL or complete SHACL |
| Acquisition | `connectors/base.py`, registry, `factory.py`, vendor adapters, webhooks/crawlers | Factory exists; generic REST fallback is not proof of arbitrary-system connectivity |
| Files | `fileparse/engine.py`, text/office/archive/email/image adapters and budgets | Real local parsing paths exist; tool-dependent formats and all-media qualification remain partial |
| Retrieval/models | Hashing vector index plus optional Ollama and sentence-transformer providers | Do not call hashing fallback a qualified semantic embedding model |
| Queries | EQL, EOQL, OSQL and other dispatchers | Several parsers implement restricted grammars; names do not prove SPARQL/Cypher/SQL equivalence |
| Frontend | React/Vite, graph renderers, shared transport/shell and legacy modules | Prior [GUI audit](GUI-UIX-audit-2026-10-16.md) remains partial; its test receipts are historical |
| Operations/security | Existing tenancy, policy, jobs, reports, egress, observability and verification modules | Reuse and audit; no new whole-system production qualification was performed here |
| Licensing | `LicenseRef-EOIP-Proprietary`, [LICENSING.md](LICENSING.md) | Owned code remains commercial; upstream software, models, datasets and content retain separate terms |

The architecture guide contains broad intelligence and distributed-runtime claims. They were treated as statements to verify, not proof that model inference, HA, causal validity or standards compliance is complete. This task did not re-audit every repository file or rerun the complete application test suite.

### 3.2 Observed Findings

| Gap | Observation and evidence | Impact | Required closure |
|---|---|---|---|
| G01 | LOCAL/PROBE: `SHACLShape` declares `min_counts`/`max_counts`, but `SHACLValidator.validate` does not enforce them | Invalid data can receive `conforms=true` | CRA-020; independent SHACL oracle, cardinality and transactional tests |
| G02 | LOCAL/PROBE: `_check_datatype` returns true for an unrecognized datatype | Unsupported constraints silently pass | CRA-020; fail closed with unsupported-feature status |
| G03 | LOCAL/PROBE: `OWLReasoner.is_subclass_of('urn:example:A','urn:example:a')` returns true through lowercasing | Case-distinct identifiers are conflated | CRA-016/019; exact RDF-term identity and profile-correct engine |
| G04 | LOCAL: reasoner bootstraps example class axioms and executes limited property chains | A custom helper is labelled more broadly than established formal coverage | CRA-019; advertised profile plus independent entailment/retraction corpus |
| G05 | LOCAL: JSON-LD import recognizes an EOIP-specific compact representation and manifest | General JSON-LD processing is not established by this importer | CRA-016/017; standards parser and explicit mapping-loss report |
| G06 | LOCAL: backend exports/query language capability lists include labels across adapters | Text declarations can overstate actual executable semantics | CRA-001/024; executable capability registry and unsupported responses |
| G07 | LOCAL: connector specialization errors are broadly caught and fall back to generic REST | Authentication/configuration defects may become misleading fallback behavior | CRA-004; explicit fallback policy, safe errors, capability downgrade |
| G08 | LOCAL: unknown applications default to `api/entities`; generic Agile profiles include tool-specific assumptions | Registration is not live integration certification | CRA-005..009; exact API versions, scopes, pagination, ACLs and fixtures |
| G09 | LOCAL: local parser catalog does not itself establish video extraction or scanned-diagram understanding | Format presence can be confused with useful semantic extraction | CRA-012..015; capability-by-task and dependency readiness |
| G10 | LOCAL: diagram parser maps unmatched relations to CALLS and vertices to Service | Original diagram semantics can be replaced without an explicit loss decision | CRA-015/017; retain raw syntax and uncertainty, block silent remapping |
| G11 | LOCAL: separate multimodal `_chunk_text` sets `start=end-overlap` without an end-of-input exit | For long input and positive overlap, termination appears unsafe; not executed here to avoid a hang | CRA-012/014; bounded worker reproduction and progress invariant |
| G12 | LOCAL: default vectors are deterministic hashing; optional providers exist | Model quality and production indexing must not be inferred from vector-shaped values | CRA-025/026; provider identity, index isolation and real retrieval evaluation |
| G13 | LOCAL: limited EOQL grammar and traversal-label handling | A SQL-like interface is not a full SQL/federated query implementation | CRA-024; grammar manifest, plan truth and differential queries |
| G14 | LOCAL: stochastic dispatcher uses random walks and heuristic hop summaries | Frequency is not calibrated failure probability or a causal proof | CRA-028; seeded reproducibility and explicitly modelled assumptions |
| G15 | Historical GUI audit: many screens, source contracts and tenant lifecycle remain partial | Rich UI cannot stand in for complete user journeys | CRA-030/037; current real-service workflow and accessibility evidence |
| G16 | Broad governance/jobs/recovery modules exist but were not fully qualified in this task | Persistence, revocation and restore claims remain open | CRA-003/031..033/040; restart and adversarial proof |
| G17 | Licensing guide identifies unresolved component and distribution questions | Commercial first-party licensing does not clear dependencies | CRA-035; exact shipped SBOM, obligations and counsel approval |
| G18 | Target scale, measured workload and actual staffing were not supplied | Numeric performance, cost and delivery claims would otherwise be invented | CRA-001/036; adopt explicit profiles, measure, revise estimates |

The executable probe used `PYTHONPATH=.;packages`, in-memory objects and no external service. It returned `conforms=true`, zero violations, `unknown_datatype_accepted=true` and `case_distinct_iri_subclass=true`. The first attempt without the repository Python path failed to import the module; that failed attempt is not application behavior. Reproduction is in section 19. These findings concern the inspected classes, not every validation path in EOIP.

## 4. Recommended Product Profiles

These are selected development targets, not current capacity claims or purchased infrastructure. All are configurable through versioned profiles; changes trigger affected qualification again.

| Profile | Dataset and users | Reference topology | Initial qualification targets |
|---|---|---|---|
| P0 developer | 1M asserted triples, 1k classes, 10k axioms; 5 concurrent users | 8 logical CPU, 32 GiB RAM; local durable store; memory only for named test harnesses | Point read p95 <=250 ms; bounded 1-hop page <=750 ms; no HA/SLA claim |
| P1 enterprise | 50M asserted triples, 10k classes, 75k axioms; 100 concurrent users; 20 source instances | Separate API/workers/control database/object store; qualified graph/search/vector deployment; start with 3 x 16-vCPU/128-GiB data nodes | Point read p95 <=250 ms; bounded graph page <=1 s; approved query suite p95 <=3 s; accepted-to-searchable p95 <=60 s |
| P2 scale qualification | 500M asserted triples, 20k classes, 150k axioms; 500 concurrent users; skewed ACLs and 100 source instances | Start with 3 x 32-vCPU/256-GiB data nodes plus measured API/workers and index resources; resize from evidence | Point read p95 <=500 ms; bounded graph page <=2 s; approved query suite p95 <=10 s; no universal sub-20-ms promise |

For every profile, count inferred triples, named graphs, raw bytes, vector bytes, replicas, index amplification, retained revisions and hot/cold residency separately. Hardware is a starting experiment, not a guarantee that a chosen engine fits. A 500M-triple target does not mean a browser renders 500M nodes. Browser scenes are bounded and use aggregation/LOD; full-data analysis runs on servers.

Default online request deadline: 30 s; longer work is a cancellable durable job. Default source acquisition concurrency: 2 per source, bounded by the vendor's limits and configurable budgets. Proposed availability objective for qualified P1 service: 99.9% monthly; RPO <=15 min and RTO <=4 h for the declared failure model. None is an executed SLA. See section 16 for exact measurement semantics.

Default deployment modes: managed SaaS, customer-operated containers/Kubernetes, and disconnected installation where dependencies and feature entitlements permit. No mandatory cloud or mandatory external LLM. Choose a maintainable modular application plus isolated workers first; split services only for actual trust, resource or scaling boundaries.

## 5. Rubric and Comparison Matrices

### 5.1 Scoring Rules

Numbers are analyst judgments about **documented suitability for the stated role**, not measured product quality. 1 = documented narrow/basic scope, 2 = limited role coverage, 3 = useful role coverage with important integration work, 4 = broad role-specific capability, 5 = unusually comprehensive documented coverage for that role. A library can score 4 in its role without being a complete enterprise platform. Cross-category total rankings are invalid.

ND means a necessary input or adequate primary evidence is missing. It must not be replaced with 1, 3, a blank numeric zero or a fabricated average. No dimension receives 5 merely because marketing says enterprise, scalable or AI-native. Matrix scores are DOC-based, medium-confidence suitability assessments unless the dossier explicitly marks lower confidence. They are never benchmark, compliance or legal grades.

| Dimension | Meaning | Numeric-score rationale and what would change it |
|---|---|---|
| D01 | Core functionality | Author/editor/store/catalog/mapping function documented in the dossier; lifecycle breadth raises coverage |
| D02 | Architecture/internals | Publicly described boundaries and component responsibilities; unknown proprietary internals remain ND |
| D03 | Model/expressivity | Exact documented RDF/OWL/SKOS/SHACL or non-W3C model; no equivalence assumed |
| D04 | Reasoning/inference | Declared execution/profile; OWL serializer, traversal or LLM alone is not a reasoner |
| D05 | Interoperability | Documented APIs, standards and portable mappings; exact-version round trips still needed |
| D06 | Performance/scale | ND until comparable measured workloads; vendor measurements remain attributed claims |
| D07 | Extensibility | Documented plugin/library/mapping/API extension mechanism, not hypothetical source modification |
| D08 | Security/governance | ND until edition-specific policy, attack and lifecycle evidence is evaluated |
| D09 | Usability/tooling | ND until task-based user and accessibility evaluation; screenshots/docs alone insufficient |
| D10 | Deployment/ops | ND until a specific install/upgrade/operation profile is qualified |
| D11 | Licensing/cost | ND until exact artifacts, integration model, quote and TCO inputs are approved |
| D12 | Limitations/known issues | ND as a single grade; each identified limitation is individually recorded and inverted |
| D13 | Ecosystem/community | ND until comparable maintainership, support and adoption measures are defined |
| D14 | Migration effort | ND until source edition, dataset, mapping loss and rollback exercise are known |
| D15 | Differentiators | Distinctive documented mechanism, not novelty/patent freedom or superiority |
| D16 | Observability | ND until actual telemetry, privacy and operational workflows are exercised |
| D17 | CI/CD/testing | ND until runnable release pipeline and reproducibility are reviewed |
| D18 | Backup/DR | ND until timed restore/consistency and failure evidence exists |
| D19 | Legal/IP risk | ND until appropriate legal and exact-component review; permissive is not risk-free |
| D20 | Accessibility/localization | ND until current edition conformance plus manual AT and locale tests |
| D21 | Support/SLA | ND until an applicable support contract and escalation exercise |
| D22 | KPI success | ND until defined role-specific tasks and independent measurement |

The compact Markdown table below shows the seven provisionally scored dimensions. The CSV retains all 22 dimensions for every row, a common rationale reference, the tool's evidence URL and inversion ID. The other fifteen dimensions are explicitly ND in every row. This deliberately incomplete scoring is preferable to invented certainty; CRA-001/036/037/038 define how to replace ND with qualified results.

### 5.2 Documented-Scope Matrix

| ID | Tool family | D01 | D02 | D03 | D04 | D05 | D07 | D15 | Inversion |
|---|---|---|---|---|---|---|---|---|---|
| C01 | Protege / WebProtege | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-01 |
| C02 | TopBraid Composer | 4 | 3 | 4 | 3 | 4 | 3 | 3 | INV-02 |
| C03 | OntoStudio / OntoStudio X | 3 | 3 | 3 | 3 | 3 | 3 | 4 | INV-03 |
| C04 | Fluent Editor | 3 | ND | 4 | 3 | 3 | 3 | 4 | INV-04 |
| C05 | Ontosphere | 3 | 4 | 4 | 4 | 4 | 4 | 4 | INV-05 |
| C06 | Graphologi | 4 | ND | 4 | ND | 3 | 3 | 3 | INV-06 |
| C07 | Chowlk / OnToology | 3 | 3 | 4 | ND | 4 | 3 | 4 | INV-07 |
| C08 | TopBraid EDG | 4 | 3 | 4 | 3 | 4 | 4 | 4 | INV-08 |
| C09 | VocBench 3 | 4 | 4 | 4 | ND | 4 | 4 | 4 | INV-09 |
| C10 | PoolParty / Graphwise | 4 | 3 | 4 | 3 | 4 | 4 | 4 | INV-10 |
| C11 | Progress Semaphore | 4 | 4 | 3 | 3 | 3 | 4 | 4 | INV-11 |
| C12 | Synaptica Graphite | 4 | 3 | 4 | ND | 4 | 3 | 4 | INV-12 |
| C13 | SciBite CENtree / TERMite | 4 | 3 | 4 | ND | 3 | 3 | 4 | INV-13 |
| C14 | Data Harmony | 3 | 3 | 3 | ND | 3 | 3 | 3 | INV-14 |
| C15 | Semantic Arts / gist | 3 | 4 | 4 | ND | 4 | 4 | 4 | INV-15 |
| C16 | Reltio Ontology Builder | 3 | 3 | 3 | ND | 3 | ND | 4 | INV-16 |
| C17 | GraphDB | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-17 |
| C18 | Stardog / Studio | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-18 |
| C19 | AllegroGraph | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-19 |
| C20 | Apache Jena / TDB2 / Fuseki | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-20 |
| C21 | Virtuoso | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-21 |
| C22 | Eclipse RDF4J | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-22 |
| C23 | Amazon Neptune | 4 | 3 | 4 | ND | 4 | 3 | 4 | INV-23 |
| C24 | MarkLogic | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-24 |
| C25 | TerminusDB | 4 | 4 | 3 | 3 | 3 | 4 | 4 | INV-25 |
| C26 | Neo4j / n10s | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-26 |
| C27 | Ontop | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-27 |
| C28 | Timbr | 4 | 4 | 3 | 3 | 4 | 4 | 4 | INV-28 |
| C29 | Anzo / AnzoGraph | 4 | 4 | 4 | ND | 4 | 3 | 4 | INV-29 |
| C30 | Morph-KGC | 4 | 4 | 4 | ND | 4 | 4 | 4 | INV-30 |
| C31 | RMLStreamer / SDM-RDFizer | 4 | 4 | 4 | ND | 4 | 4 | 4 | INV-31 |
| C32 | Karma | 3 | 4 | 4 | ND | 4 | 3 | 4 | INV-32 |
| C33 | Palantir Foundry / AIP | 4 | 3 | 3 | ND | 3 | 4 | 4 | INV-33 |
| C34 | Microsoft Fabric / IQ | 4 | 3 | 3 | ND | 3 | 3 | 4 | INV-34 |
| C35 | Oracle graph / AI Data Platform | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-35 |
| C36 | Cosmo Tech | 3 | 3 | 3 | ND | 3 | 3 | 4 | INV-36 |
| C37 | Cinchapi Concourse | 4 | 4 | 3 | ND | 3 | 4 | 4 | INV-37 |
| C38 | Essential Cloud | 4 | 3 | 3 | ND | 3 | 3 | 4 | INV-38 |
| C39 | OpenMetadata | 4 | 4 | 3 | ND | 4 | 4 | 4 | INV-39 |
| C40 | data.world | 4 | 3 | 4 | ND | 4 | 3 | 4 | INV-40 |
| C41 | Collibra | 4 | 3 | 3 | ND | 4 | 4 | 4 | INV-41 |
| C42 | Alation | 4 | 3 | 3 | ND | 4 | 4 | 4 | INV-42 |
| C43 | OvalEdge | 4 | 4 | 3 | ND | 3 | 3 | 4 | INV-43 |
| C44 | DataHub | 4 | 4 | 3 | ND | 4 | 4 | 4 | INV-44 |
| C45 | Apache Atlas | 4 | 4 | 3 | ND | 4 | 4 | 4 | INV-45 |
| C46 | ROBOT | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-46 |
| C47 | pySHACL | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-47 |
| C48 | TopBraid SHACL API | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-48 |
| C49 | OOPS! | 3 | 3 | 3 | ND | 3 | ND | 4 | INV-49 |
| C50 | WIDOCO / LODE | 4 | 4 | 4 | ND | 4 | 3 | 4 | INV-50 |
| C51 | Mondeca suite / CAM | 4 | 3 | 4 | 3 | 4 | 4 | 4 | INV-51 |
| C52 | Diffbot | 4 | 3 | 3 | ND | 3 | 3 | 4 | INV-52 |
| C53 | DeepOnto | 4 | 4 | 4 | 4 | 4 | 4 | 4 | INV-53 |
| C54 | spaCy / textacy | 4 | 4 | 2 | ND | 3 | 4 | 4 | INV-54 |
| C55 | OWL API | 4 | 4 | 4 | 3 | 4 | 4 | 4 | INV-55 |

For D01/D02/D03/D04/D05/D07/D15 respectively, each dossier's capability, reconstruction, semantics, inference, interface, extension and differentiator statements are the rationale. A suite row describes the cited combination, not every edition or every constituent library. ND within the seven scored columns denotes an additional evidence gap. Scores should be revised, not merely copied, after a pinned-edition evaluation.

## 6. Tool Dossiers and Limitation Inversions

Each numbered dossier is a standalone executive/technical briefing. Markdown has no fixed printed page size; no claim of a typeset one-page layout is made. The following contain documented strengths, architectural reconstruction, limits, interfaces/deployment, and a specific inversion. Undocumented internals are left unknown. The INV IDs are the complete set of limitations asserted by this report; each is traced to executable requirements in section 7 and CRAr.md.

### Category 1: Authoring and Conceptual Modelling

#### C01. Protege and WebProtege

**DOC/decision:** Protege is the desktop authoring reference to interoperate with, while WebProtege supplies collaborative editing, revision history, discussions and permissions. The inspected WebProtege repository explicitly describes migration toward finer-grained services; do not combine its classic deployment architecture with next-generation components as one release. Its inspected license is BSD-style, not the attachment's blanket AGPL assertion. [WebProtege repository](https://github.com/protegeproject/webprotege), [license](https://github.com/protegeproject/webprotege/blob/master/license.txt).

**Reconstruction:** ontology document -> OWL API object model -> editor changes -> chosen reasoner -> classified hierarchy/explanations; collaboration adds project permissions, change history and notifications. This is not an enterprise acquisition pipeline or operational graph backend. Desktop plugins and external reasoners require separate artifact/license review. [Desktop releases](https://github.com/protegeproject/protege/releases).

**INV-01, INFERENCE:** expert axiom editing does not by itself solve enterprise onboarding and source lifecycle. EOIP should offer simple business forms and expert axiom mode over the same versioned model, loss-aware export and reviewable diffs. Qualify a Protege -> EOIP -> Protege cycle with blank nodes, imports, annotations and logical equivalence, not a successful file download. Maps to CRA-016/018/019/022/030.

#### C02. TopBraid Composer

**DOC/decision:** Composer documents SHACL/SPIN rule execution in a local modelling environment. Study the author/query/validate workflow; do not choose it as the enterprise runtime by name. Its older documentation is not evidence that all current EDG capabilities exist in Composer. [Composer rules](https://topbraidcomposer.org/html/Define_rules.htm).

**Reconstruction:** model files and imported vocabularies -> visual/expert editor -> query/rule execution -> model and derived artifacts. EDG's later Active Data Shapes tooling is a related but distinct development model. [TopQuadrant product-direction discussion](https://www.topquadrant.com/blog/q-a-part-2-from-the-webinar-whats-new-in-topbraid-edg-7-1).

**INV-02, INFERENCE:** coupling local authoring to a particular distribution creates qualification and handoff work. Build portable ontology packages containing source, imports lock, shapes, transformations, metadata and acceptance results; run identical validation in local, CI and server contexts. Require engine/version disclosure and no silent SPIN-to-SHACL conversion. Exact current Composer release, support lifecycle and OEM terms require vendor confirmation. Maps to CRA-018/020/022/035/039.

#### C03. OntoStudio and OntoStudio X

**DOC/decision:** distinguish historical OntoStudio from current OntoStudio X. The current vendor describes spreadsheet-native ObjectLogic authoring with OntoBroker and Java/Python bridges, multi-server workbooks and macro-free XLSX files. Do not repeat the attachment's Eclipse description as the current architecture. [OntoStudio X](https://semafora-systems.com/technology/ontostudio-x/).

**Reconstruction:** workbook functions and named ontology references -> bridges -> one or more OntoBroker servers -> rules/query results returned to dynamic arrays. ObjectLogic and OWL are not interchangeable syntax with identical semantics; transformations need a feature-loss ledger. [OntoBroker help](https://www.semafora-systems.com/ontobroker-help).

**INV-03, INFERENCE:** expert or spreadsheet-specific rule workflows can make semantics difficult to inspect outside the originating tool. EOIP should store a typed rule AST, source language, profile and dependency graph, provide tabular editing as a projection, and reject unsupported translations. Verify round-trip and explanation identity across interfaces. Product compatibility, current license and unsupported construct behavior remain qualification work. Maps to CRA-017/019/022/024/030.

#### C04. Fluent Editor

**DOC/decision:** controlled English and a predictive editor are useful business-authoring patterns. The vendor lists OWL/SWRL interfaces, plugins and a SWRL debugger; free-use categories do not establish unrestricted commercial redistribution rights. [Fluent Editor](https://www.cognitum.eu/semantics/FluentEditor/).

**Reconstruction:** restricted grammar and vocabulary -> parse into formal statements -> reason/materialize -> inspect rules and entities. Unlike an unconstrained LLM, controlled language can have explicitly bounded meaning. Full proprietary parser internals are not public evidence here.

**INV-04, INFERENCE:** controlled English can limit languages and expressivity, while free text can introduce ambiguity. Offer a schema-aware sentence builder with displayed formal translation, ambiguity diagnostics, multilingual labels and an explicit approval step. Expert editing must preserve constructs the sentence builder cannot represent. Acceptance includes round-trip meaning, ambiguous input rejection and no LLM-generated axiom directly reaching production. Exact supported grammar, release and deployment terms remain ND. Maps to CRA-019/021/022/026/030.

#### C05. Ontosphere

**DOC/decision:** the inspected project describes a browser-side RDF store, Reactodia canvas, workers, reasoning integrations and an MCP surface. Current README describes Konclude-based DL functionality, so the supplied simple OWL-RL description is not a safe release-level summary. [Ontosphere source and architecture](https://github.com/ThHanke/ontosphere).

**Reconstruction:** RDF store is authoritative; the visual canvas mirrors selected nodes, and tool calls mutate data then refresh presentation. Browser execution, worker boundaries and inference visualization are useful reference patterns. Apache-licensed application source does not automatically clear every bundled reasoner or WASM dependency.

**INV-05, INFERENCE:** client-local models and powerful tool mutation surfaces need enterprise authorization, persistence, quotas and origin controls when adopted into a server-backed product. EOIP should retain responsive local previews but route committed mutations through server policy and revision checks. Test MCP denial, stale revision, browser restart, large-model cancellation and accessible graph alternatives. Do not copy an agent relay into production without a separate threat model. Maps to CRA-002/003/019/027/030/035/039.

#### C06. Graphologi

**DOC/decision:** the official guide describes SKOS/SKOS-XL taxonomies, ontology-driven enrichment and templates using SHACL where possible. Reuse the idea of constrained task forms and a clear concept/label distinction. Do not infer a full OWL reasoner from template validation. [Graphologi guide](https://graphologi.com/docs/).

**Reconstruction:** vocabulary/model -> template constraints -> editing interface -> relationship exploration -> published data. Backend storage topology, engine implementation, complete API surface and exact service guarantees were not established by that guide.

**INV-06, INFERENCE:** a simplified template UI may not expose every underlying ontology construct. EOIP should disclose supported editing coverage, preserve uneditable statements and provide accessible table/tree/expert modes over the same revisions. Compare controlled business tasks and loss-aware RDF/SKOS import/export before drawing usability conclusions. Qualification requires actual API and current commercial edition access; the attachment's ownership and SharePoint assertions are not assumed. Maps to CRA-018/020/021/030/034.

#### C07. Chowlk and OnToology

**DOC/decision:** Chowlk converts diagrams.net conceptualizations following its notation into OWL/Turtle; it exposes an upload API and Apache-2.0 source. This does not mean arbitrary engineering images or generic UML preserve formal semantics. [Chowlk](https://github.com/oeg-upm/Chowlk).

**Reconstruction:** diagram XML -> notation recognition -> ontology constructs -> serialization. OnToology is listed in the attachment as a separate ontology repository automation workflow, not the converter itself. The attempted canonical repository URL was unavailable and its project site timed out during this review; exact current supported hosting, permissions, release and license require verification before integrating it. The family scores apply to documented Chowlk coverage, not verified OnToology internals. [OnToology project site, unavailable during review](http://ontoology.linkeddata.es/).

**INV-07, INFERENCE:** visual conversion and hosted automation can lose semantics or require sensitive repository/ontology access. EOIP should use notation-specific adapters, offline CI runners, explicit conversion diagnostics and minimum repository permissions. Compare emitted axioms with a golden ontology and deliberately invalid diagrams. Keep hosted submission opt-in. Maps to CRA-015/017/022/035/037.

### Category 2: Governance, Taxonomy and Vocabulary

#### C08. TopBraid EDG

**DOC/decision:** EDG is a SHACL-centred governance platform with standards-based representations. Active Data Shapes generates scripting interfaces from shapes and supplies graph access; this does not prove the attachment's unspecified microservices topology. [EDG introduction, 8.3 baseline](https://docs.topquadrant.com/8.3/introduction/index.html), [ADS architecture](https://www.topquadrant.com/blog/q-a-part-2-from-the-webinar-whats-new-in-topbraid-edg-7-1).

**Reconstruction:** governed asset collections and models -> forms/constraints/scripts -> permissions/workflow -> publication and APIs. Treat newer EDG 9.1 release notes as a separate version signal, not proof that 8.3 installation commands apply unchanged. [9.1 notes](https://www.topquadrant.com/release-note/9-1).

**INV-08, INFERENCE:** model-generated execution surfaces can increase coupling and privilege if scripts share service authority. EOIP should derive forms/contracts from versioned shapes but isolate code execution, bind approvals to exact revisions and retain portable packages. Test that validation and authorization cannot be bypassed through generated endpoints. Commercial license, extension support and schema-migration compatibility need pinned-edition evaluation. Maps to CRA-002/018/020/022/030/039.

#### C09. VocBench 3

**DOC/decision:** VocBench supports collaborative OWL, SKOS/SKOS-XL and OntoLex-Lemon work. Semantic Turkey is built on RDF4J, CODA, OSGi and Spring; the attachment's Jena-backed assertion is corrected. [VocBench documentation](https://vocbench.uniroma2.it/doc/), [Semantic Turkey](https://semanticturkey.uniroma2.it/).

**Reconstruction:** web vocabulary editor -> Semantic Turkey services -> RDF repositories; changes and workflows operate on structured concepts and lexical resources. Preserve the difference between concept identifiers, language-tagged labels and lexical entries. Do not infer linguistic quality or current accessibility from format support.

**INV-09, INFERENCE:** a strong vocabulary workbench does not itself define EOIP's source ingestion and operational actions. Build vocabulary stewardship as an independent bounded module, integrated by stable IDs and events. Prove multilingual import/export, polyhierarchy, concurrent edits, term deprecation and dependent-index updates. Exact build artifacts and module licenses must be reviewed individually; no suite-wide license guess is made. Maps to CRA-018/021/022/025/030.

#### C10. PoolParty / Graphwise

**DOC/decision:** the current transition guide maps PoolParty components into Graph Modeling, Semantic Analytics, GraphRAG and Graph Automation. Do not score a renamed component twice or assume all bundle entitlements. [Transition guide](https://help.graphwise.ai/en/graphwise-documentation/graphwise-sub-components-at-a-glance/poolparty-semantic-suite-to-graphwise-platform-transition-guide.html).

**Reconstruction:** managed taxonomy/ontology -> extraction/enrichment -> retrieval or application pipeline. The inspected GraphRAG integration uses modelling-project identity and separately managed credentials. GraphDB is a related store component with its own documentation and qualification, not synonymous with taxonomy management. [Graph Modeling integration](https://help.graphwise.ai/gwp26-1/en/graphrag/graphrag-configuration-guide/graphwise-graph-modeling-integration.html).

**INV-10, INFERENCE:** bundle transitions and cross-component compatibility can complicate modular upgrades. EOIP needs a compatibility manifest, semantic API versions, portable packages, independently deployed providers and regression-tested migrations. Qualify terminology updates through retrieval/answers and rollback. No assumption that Graphwise lacks these controls is made. Maps to CRA-002/021/025/026/035/039.

#### C11. Progress Semaphore

**DOC/decision:** Semaphore's classification architecture is unusually explicit: knowledge model management -> publisher -> rulebases -> classification/language service, with document analysis and precision/recall tooling. [How classification works](https://docs.progress.com/bundle/semaphore-5-how-classification-works/page/topics/classification/welcome.html).

**Reconstruction:** curated terms and templates compile to weighted classification rules, which emit structured topic scores. Scores are not automatically probabilities; evaluate against a labelled corpus. This is content intelligence rather than proof of arbitrary OWL DL reasoning. Deployment, scale and redaction claims require exact licensed modules.

**INV-11, INFERENCE:** rulebase freshness and domain drift can affect extraction quality. EOIP should version classification rules with vocabularies, run shadow evaluations before release, preserve source spans and confidence, and require steward approval for expansion. Demonstrate precision/recall by domain/language and rule rollback without losing provenance. Do not repeat the attachment's petabyte-throughput claim as a measured fact. Maps to CRA-021/022/026/036/040.

#### C12. Synaptica Graphite

**DOC/decision:** Graphite documents RDF concept modelling, taxonomy workflows, scheme versioning/forking, archive/restore, audit APIs and Confluence/SharePoint-related integrations. Its strengths are stewardship and publication, not evidence of a particular hidden storage implementation. [Graphite capabilities](https://synaptica.com/synaptica-graphite/).

**Reconstruction:** schemes/concepts/predicates -> graphical authoring and rule checks -> editorial state -> scheduled publication/integration. Publication and restoration are distinct from database DR; neither implies a measured RPO/RTO.

**INV-12, INFERENCE:** controlled vocabulary publication can drift from consuming indexes and sources. EOIP should provide versioned publication receipts, consumer acknowledgements, compatibility checks and replayable change events. Demonstrate failed-consumer retry, old-version reads, term retirement and rollback with permissions preserved. Commercial terms and current operational internals remain edition-specific evaluation work. Maps to CRA-021/022/025/031/033.

#### C13. SciBite CENtree and TERMite

**DOC/decision:** separate CENtree's ontology management from TERMite's terminology recognition. The vendor describes a terminology -> recognition -> harmonization workflow, with domain-specific vocabulary assets. [Ontology-management use case](https://scibite.com/wp-content/uploads/2024/10/SciBite-Use-Case_Democratised-Ontology-Management_UC016v2.pdf), [CENtree 3.0 datasheet](https://scibite.com/wp-content/uploads/2025/03/Datasheet-SciBite-CENtree-3.0_v4_20250305.pdf).

**Reconstruction:** terminology repository/API -> vocabulary build -> document recognition -> stable concept annotations -> search/registration. A life-sciences domain asset can carry licensing restrictions separate from application code. The 2025 roadmap is historical intent, not acceptance of every announced release.

**INV-13, INFERENCE:** specialist terminology investment does not transfer automatically to engineering domains. EOIP should package domain vocabularies, extractors, evaluation corpora and license metadata independently. Prove abbreviation disambiguation, unseen terms, corpus drift and multilingual quality on enterprise examples. No SNOMED/MedDRA redistribution is presumed. Maps to CRA-021/023/026/035/036.

#### C14. Data Harmony

**DOC/decision:** the vendor's suite links thesaurus management with machine-assisted indexing. This is a useful architecture for reviewed content classification, not a generic knowledge-store substitute. [Data Harmony products](https://www.accessinn.com/data-harmony-products/).

**Reconstruction:** controlled terms and editorial relationships -> indexing configuration -> document tagging -> reviewed metadata delivery. Exact ranking algorithms, current internals, API versions and formal reasoning coverage are not established here.

**INV-14, INFERENCE:** highly tuned indexing rules can become opaque or expensive to maintain across domains. EOIP should expose versioned classifier configurations, explanation traces, evaluation reports and accepted/rejected term suggestions. Keep curated labels separate from machine proposals and support portable SKOS exports with a loss report. Acceptance requires labelled-document evaluation and a reproducible vocabulary upgrade, not a list of taxonomy features. Maps to CRA-021/022/026/034/036.

#### C15. Semantic Arts and gist

**DOC/decision:** Semantic Arts is a consultancy/tooling practice; gist is an upper enterprise ontology, not a database or full platform. The inspected page identifies gist 14.1.0, April 2026, under CC BY 4.0 and supplies migration guidance. [gist](https://www.semanticarts.com/gist/).

**Reconstruction:** reusable domain-independent concepts -> enterprise-specific extensions -> mappings from source schemas -> reasoning and applications supplied by other engines. Source and migration files are available in the maintainer repository. [gist source](https://github.com/semanticarts/gist).

**INV-15, INFERENCE:** upper-ontology adoption can be misread as a complete domain model and can introduce breaking conceptual migrations. EOIP should permit upper ontologies as optional pinned dependencies, preserve their namespaces, track attribution and version migration impact. Compare competency questions before/after upgrades; never redefine upstream terms inside an upstream namespace. Commercial consulting and separately licensed tools are not covered merely by gist's license. Maps to CRA-018/021/022/034/035.

#### C16. Reltio Ontology Builder

**DOC/decision:** Reltio describes an agentic schema-to-Reltio-canonical-model experience, with industry models, mapping review and downloadable artifacts. It explicitly tells users to validate generated artifacts before tenant configuration and to avoid sensitive schemas without authorization. Do not infer universal W3C export or a general-purpose DL engine. [Reltio documentation](https://docs.reltio.com/en/objectives/model-data/reltio-ontology-builder).

**Reconstruction:** sanitized source schema -> model analysis and LLM-assisted candidates -> diagram/list review -> canonical mappings and download. Internal models and prompts remain proprietary/unknown.

**INV-16, INFERENCE:** a target-specific mapping assistant can create destination dependence and false confidence in generated mappings. EOIP should maintain a destination-neutral mapping IR, show source/target constraints, preserve unresolved constructs and require a dry-run plus review before publication. Prove rejected suggestions never mutate live schemas and that a portable mapping can execute against two qualified backends. Maps to CRA-017/022/024/026/034.

### Category 3: Databases and Reasoning Engines

#### C17. GraphDB

**DOC/decision:** the inspected reasoning guide describes compiled rule sets and repeated forward-chaining materialization. It also documents an OWL2-QL non-conformance, so even a broad inference summary must be checked against the detailed release notes. [Reasoning, 11.3](https://graphdb.ontotext.com/documentation/11.3/reasoning.html), [inference, 11.4](https://graphdb.ontotext.com/documentation/11.4/inference.html).

**Reconstruction:** asserted triples plus selected rules -> compiled rule engine -> inferred closure -> indexed query, with ruleset operations and retraction handling. These versions are reviewed documentation baselines, not a declaration of the latest available release.

**INV-17, INFERENCE:** materialization trades extra write/storage work for query convenience; removal and provenance are important correctness costs. EOIP should support explicit inference modes, separate asserted/inferred graphs, track derivation dependencies and measure amplification/retraction. Test a multiply-supported inference after deleting one versus every supporting assertion. Do not infer EOIP capacity from vendor scale claims. Maps to CRA-019/020/024/036.

#### C18. Stardog and Studio

**DOC/decision:** Stardog documents on-demand reasoning via query rewriting, an internal Datalog representation and alternative reasoner configuration. This is more precise than labelling all reasoning simply backward chaining. [Inference engine](https://docs.stardog.com/inference-engine/).

**Reconstruction:** query + schema -> internal rules/rewrite -> optimized expanded plan -> query results. Virtualization adds remote-source translation and pushdown; exact source and edition support requires separate tests. Query hints can alter reasoning scope and plan behavior. [Query hints](https://docs.stardog.com/query-stardog/query-hints).

**INV-18, INFERENCE:** query rewriting can expand plans and remote work; materialization has different costs. EOIP should expose reasoning/profile/source plans, deadlines, cost guards and semantic diagnostics rather than hiding rewrite cost. Qualify representative queries with reasoning on/off and stale mappings, preserving intended answers. No unsupported GraphQL/openCypher/SWRL equivalence is inferred from the attachment. Maps to CRA-019/024/029/036.

#### C19. AllegroGraph

**DOC/decision:** AllegroGraph documents RDF/SPARQL, Prolog, geospatial functions, FedShard and AI integrations. The inspected documentation index identifies 9.0.3; a FedShard definition example is versioned 9.0.2. Do not mix them into one unpinned configuration. [Documentation](https://agraph.franz.com/agraph/support/documentation/), [FedShard definitions](https://examples.franz.com/agraph/support/documentation/fedshard-def.html).

**Reconstruction:** repositories distributed by configured keys -> shard/federated execution -> optional knowledge-base repositories and replicas. Querying, Prolog rules and vector retrieval are different execution mechanisms requiring separate authorization and semantic tests.

**INV-19, INFERENCE:** sharding key choice can make cross-partition traversals and policy enforcement expensive. EOIP should declare partition affinity, profile remote joins, budget graph expansion and preserve derivation/ACL labels across partitions. Prove a two-tenant join cannot expose hidden intermediate facts. Exact optimizer internals, HA guarantees and cost remain vendor-evaluation items. Maps to CRA-003/019/024/025/036.

#### C20. Apache Jena, TDB2 and Fuseki

**DOC/decision:** Jena supplies RDF APIs, TDB2 persistent storage and Fuseki SPARQL protocol services. TDB2 is a single-machine store; using Fuseki does not turn it into a distributed database. TDB1/TDB2 storage compatibility is not assumed. [TDB2](https://jena.apache.org/documentation/tdb2/index.html), [Fuseki](https://jena.apache.org/documentation/fuseki2/).

**Reconstruction:** parsers/model APIs -> transactional dataset -> indexes/query algebra; inference can be layered into configured datasets. The documented Fuseki Main graph ACL mechanism has read-only dataset limitations. [Data access control](https://jena.apache.org/documentation/fuseki2/fuseki-data-access-control).

**INV-20, DOC/INFERENCE:** embedded framework flexibility leaves integration, write authorization, backup and multi-node design to the product team. EOIP should isolate the semantic engine, enforce policy on every mutation and qualify backup/restore under concurrent traffic. Use it as a candidate semantic service, not an automatic choice for the 500M profile. Maps to CRA-003/016/019/020/033/036.

#### C21. OpenLink Virtuoso

**DOC/decision:** Virtuoso documents combined relational/RDF capabilities and open-source versus commercial licensing/feature distinctions. Commercial distribution and OEM use must be reviewed against the exact edition, not the word open-source. [Product and licensing FAQ](https://virtuoso.openlinksw.com/index/).

**Reconstruction:** RDF quads and relational access -> hybrid optimizer/indexes -> SQL/SPARQL interfaces; distributed designs introduce communication and data placement costs. This reconstruction derives from OpenLink's architecture paper, not inspected current source internals. [Web-scale RDF paper](https://virtuoso.openlinksw.com/whitepapers/Web-Scale%20RDF.pdf).

**INV-21, INFERENCE:** edition-gated federation/HA and mixed query semantics create portability and procurement risk. EOIP should declare minimum backend capabilities and offer alternatives without pretending every adapter supports the same features. Perform round-trip, isolation and failover tests for each paid/open edition separately. A network boundary is not automatic GPL clearance. Maps to CRA-002/017/024/035/036.

#### C22. Eclipse RDF4J

**DOC/decision:** RDF4J's SHACL engine analyses transaction changes and validates during commit, with dependency-aware data retrieval and documented feature/transaction restrictions. Its guide explicitly discloses incomplete features and validation-report limitations. [SHACL engine](https://rdf4j.org/documentation/programming/shacl/).

**Reconstruction:** Repository API -> Sail layers -> storage/inference/SHACL; writes produce validation plans, read affected data and commit or reject. Shapes changes may require substantial revalidation. Treat its extension predicates separately from W3C profiles.

**INV-22, DOC/INFERENCE:** incremental validation still needs correct affected-node analysis and serializable outcomes. EOIP should choose qualified validators, expose truncation and unsupported features, and test concurrent writes that are individually valid but jointly violate constraints. Benchmark both local changes and shape migrations. Do not claim standalone validation automatically enforces mutation-time atomicity. Maps to CRA-019/020/022/031/036.

#### C23. Amazon Neptune

**DOC/decision:** Neptune documents managed graph services supporting property-graph and RDF interfaces. Supporting both models does not establish an automatic lossless mapping or a single universal query language over both datasets. Pin the actual Neptune product and engine version; database and analytics offerings have different interfaces. [Neptune overview](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html).

**Reconstruction:** API clients and AWS authorization -> selected graph interface -> managed storage/compute. Managed backups, high availability and region features must be qualified against the chosen configuration rather than copied from generic cloud descriptions. EOIP's existing Neptune adapter uses openCypher for GraphStore operations; listing SPARQL is not proof of equivalent RDF application behavior.

**INV-23, INFERENCE:** provider-specific operational/security contracts limit portability. EOIP should isolate cloud adapters, implement request signing where required, disclose model coverage and preserve export/restore paths for customer installations. Test actual authorization failures, network outages, cancellation and recovery. Maps to CRA-002/003/017/024/033/035.

#### C24. Progress MarkLogic

**DOC/decision:** MarkLogic's semantics guide describes dictionary-encoded triple values/data and indexing of valid triple elements in documents. This is a document-plus-semantics architecture, not interchangeable with every triplestore. [Semantics guide, historical baseline](https://docs.marklogic.com/guide/semantics.pdf).

**Reconstruction:** JSON/XML documents and extracted triples -> document/index structures -> search/SPARQL/application APIs. Security depends on document/triple interactions; older element-level-security documentation explicitly has semantics restrictions. A historical restriction requires current-version verification, not a claim that it necessarily persists. [Security interaction, version 9](https://docs.marklogic.com/9.0/guide/security/element).

**INV-24, INFERENCE:** combining document, field and triple policies can yield unexpected visibility. EOIP should test the effective policy of every derived fact and support label composition rather than flattening access control at ingestion. Prove restricted source spans cannot leak through triples, search counts or answers. Maps to CRA-003/010/029/040.

#### C25. TerminusDB

**DOC/decision:** current documentation describes schema-enforced JSON documents over immutable delta layers, version control, WOQL/GraphQL/HTTP APIs and stewardship by DFRNT. Do not equate its closed-world document model with unrestricted OWL DL or generic SPARQL. [Architecture](https://docs.terminusdb.org/docs/terminusdb-explanation/), [query interfaces](https://docs.terminusdb.org/docs/querying-terminusdb/).

**Reconstruction:** schema-aware write -> immutable commit/delta -> branch history -> query resolution across layers; rollup controls layer overhead. History is not an off-site backup, and branch reset does not undo an external action.

**INV-25, INFERENCE:** version-rich data models still need explicit retention, deletion and merge-conflict policy. EOIP should version ontology and graph views independently, record structured conflicts and preserve legally required deletion across retained derivatives. Qualify branch merge, divergent schema and recovery with policy changes. Do not copy claimed memory-per-triple results into EOIP sizing. Maps to CRA-018/022/028/033/040.

#### C26. Neo4j and Neosemantics (n10s)

**DOC/decision:** distinguish the database, n10s extension and each one's licensing/version. n10s documents RDF import/export, ontology-related operations and SHACL validation for property graphs. It is not evidence that Neo4j becomes a fully equivalent RDF/OWL store. [n10s guide, 4.0 baseline](https://neo4j.com/labs/neosemantics/4.0/), [maintainer repository](https://github.com/neo4j-labs/neosemantics).

**Reconstruction:** RDF terms and configured mapping rules -> labels/relationships/properties -> Cypher queries and validation -> RDF serialization. Namespace configuration, multivalues, datatypes, blank nodes and parallel edges need mapping-specific tests.

**INV-26, INFERENCE:** RDF-to-LPG transformations can change identity and expressivity. EOIP should retain canonical RDF terms and relationship assertion IDs, emit loss diagnostics, and allow a semantic store plus read-optimized property projection when needed. Prove two identical-endpoint edges retain distinct provenance through export/import. Maps to CRA-016/017/020/024/034.

### Category 4: OBDA, Virtualization and Mapping

#### C27. Ontop

**DOC/decision:** Ontop exposes relational data as virtual RDF graphs, translating SPARQL using R2RML mappings and lightweight ontologies into source SQL. This is a strong candidate OBDA integration, not a replacement for source ACLs or CDC. [Ontop source](https://github.com/ontop/ontop).

**Reconstruction:** ontology + mappings + database metadata -> intermediate/reformulated query -> SQL optimization/pushdown -> source execution -> RDF bindings. The CLI documentation explicitly warns that `ontop query` includes setup work and is unsuitable for production benchmarking; use a warmed endpoint. [CLI guidance](https://ontop-vkg.org/guide/cli).

**INV-27, DOC/INFERENCE:** query cost and availability inherit source constraints and mapping semantics. EOIP should expose source plans, credential delegation, row limits and partial-source errors. Compare virtual answers with a materialized reference under nulls, joins and source schema drift. Do not label every supported mapping profile full OWL reasoning. Maps to CRA-017/019/024/036.

#### C28. Timbr

**DOC/decision:** Timbr describes SQL-native ontologies as a virtual semantic layer, mapping business concepts and relationships to existing data; it also documents caching/materialization options. No-copy virtualization does not mean no metadata/cache retention or no source cost. [Introduction](https://docs.timbr.ai/doc/docs/getting-started/intro-timbr/).

**Reconstruction:** concept/property/relationship definitions -> mappings/views -> semantic SQL -> source pushdown and results. Its modelling guide distinguishes intrinsic, exhaustive, dereferenced, view and graph schemas; some functionality has separate entitlement. [Modelling](https://timbr.ai/doc/docs/getting-started/timbrmodeling/).

**INV-28, INFERENCE:** SQL familiarity can hide semantic rewriting and target-specific model behavior. EOIP should offer a typed query builder and optional SQL-facing adapter with visible plans, supported grammar and exportable mappings. Test real null/cardinality/recursive semantics and policy preservation rather than accepting a SQL-looking string. Maps to CRA-017/024/029/030/035.

#### C29. Anzo and AnzoGraph

**DOC/decision:** the inspected deployment guide describes AnzoGraph MPP execution, subject-based distribution, in-memory analytics and a leader endpoint. Anzo the platform and AnzoGraph the query engine need separate version and deployment qualification. [Anzo 5.4 deployment guide](https://docs.cambridgesemantics.com/anzo/v5.4/userdoc/pdf/Anzo-v54-Deployment-Guide.pdf).

**Reconstruction:** source mappings and graph data -> distributed slices -> parallel query operations -> merged results. Memory residency and network exchange are central sizing dimensions. The historical guide is not an independently verified current architecture or evidence that every workload virtualizes data.

**INV-29, INFERENCE:** an in-memory analytic model can require substantial RAM and careful skew management. EOIP should bound jobs, estimate graph/index amplification and support hot/cold projections without pretending disk-backed and memory-resident stores have identical performance. Test subject skew, cross-partition joins, OOM handling and restart. Maps to CRA-002/024/031/036.

#### C30. Morph-KGC

**DOC/decision:** Morph-KGC constructs RDF with R2RML/RML and mapping partitions. The implementation distinguishes CLI/library multiprocessing and output-specific memory behavior. It is materialization, not transparent virtual access. [Architecture](https://morph-kgc.readthedocs.io/en/stable/), [current configuration](https://morph-kgc.readthedocs.io/en/latest/documentation/).

**Reconstruction:** mappings -> logical-source reads and partition plan -> term generation/joins -> RDF output. Python integration fits EOIP, but function execution and remote sources still require sandboxing and egress control.

**INV-30, DOC/INFERENCE:** large in-memory outputs and platform-specific parallelism affect operability. EOIP should use bounded external workers, chunked N-Quads manifests, resumable checkpoints and explicit UDF policies. Benchmark source joins, duplicate rates and peak RSS; verify identical terms against an independent mapper. Windows development results must not be extrapolated to Linux multi-process throughput. Maps to CRA-002/017/031/036.

#### C31. RMLStreamer and SDM-RDFizer

**DOC/decision:** these are different engines. RMLStreamer provides streaming RML execution with Flink-related infrastructure; SDM-RDFizer documents optimized mapping plans/operators and batch construction. They must not share an assumed exactly-once guarantee or benchmark result. [RMLStreamer](https://github.com/RMLio/RMLStreamer), [SDM-RDFizer](https://github.com/SDM-TIB/SDM-RDFizer).

**Reconstruction:** both evaluate mappings over sources, but stream windows, joins, checkpoints and sink transactions differ from batch plan execution. Throughput numbers from the maintainer's datasets are not EOIP performance evidence.

**INV-31, INFERENCE:** source checkpoint success and graph publication can diverge after a crash. EOIP should use stable event IDs, idempotent writes and a publication/checkpoint transaction protocol, explicitly describing at-least-once delivery. Test duplicate/reordered updates, deletes, sink failure and replay, including stream/batch equivalence. Each component and dependency needs its own license review. Maps to CRA-010/017/031/036.

#### C32. Karma

**DOC/decision:** Web-Karma is a source-to-ontology integration reference, but its owner archived the repository on 2025-04-16. Its Apache-2.0 source does not supply ongoing maintenance or a support SLA. [Archived maintainer repository](https://github.com/usc-isi-i2/Web-Karma).

**Reconstruction:** source worksheets -> semantic typing/alignment interaction -> mapping model -> generated RDF/integration outputs. Study the assisted mapping workflow independently of an obsolete runtime dependency stack.

**INV-32, DOC/INFERENCE:** adopting an archived application creates maintenance and security ownership. EOIP should reuse the workflow concept, retain an engine-neutral mapping IR and certify actively maintained execution adapters. Test user correction, ambiguous semantic typing, mappings with joins and deterministic re-execution. Do not automatically embed the archived web server because a demo starts. Maps to CRA-017/022/030/034/035.

### Category 5: Operational Ontologies, Digital Twins and AI

#### C33. Palantir Foundry and AIP

**DOC/decision:** the Ontology combines business object/link models with operational interfaces and actions. Permissions distinguish ontology resources from objects and links. This is a useful benchmark for operational workflows, not proof of W3C formal semantics or a public implementation of proprietary internals. [Ontology overview](https://www.palantir.com/docs/foundry/ontology/overview), [object permissioning](https://www.palantir.com/docs/foundry/object-permissioning/overview).

**Reconstruction:** backing data -> ontology objects and links -> applications/functions/actions -> governed operational interaction. AIP integration does not make an LLM a deterministic reasoner. Exact indexing algorithms, storage internals and negotiated economics remain unknown here.

**INV-33, INFERENCE:** operational models and action integrations can be difficult to port if semantics and execution contracts are inseparable. EOIP should define portable object/action manifests with explicit preconditions, policy checks, signed approvals, idempotency and read-back. Prove an approved action cannot be replayed with changed parameters and that a failed source write is not reported as success. Maps to CRA-018/024/027/034/039.

#### C34. Microsoft Fabric, Semantic Models and Fabric IQ

**DOC/decision:** distinguish Power BI semantic models, OneLake, Fabric IQ ontology/graph preview and Microsoft 365 Copilot integration. They are related products, not one universally available W3C ontology runtime. Current ontology-agent documentation lists preview limits, single-ontology conversations and no built-in rollback of applied ontology changes. [Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview), [ontology agent](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-use-ontology-agent).

**Reconstruction:** source-bound business model -> optional materialized graph -> query/agent/application surfaces. The graph projection guide excludes some sources/types and configurations; do not assume every semantic model can become the same graph. [Projection limits](https://learn.microsoft.com/en-us/fabric/iq/ontology/how-to-use-ontology-graph).

**INV-34, DOC/INFERENCE:** preview boundaries and in-place changes create compatibility/rollback risk. EOIP should version capabilities by service/region, preserve an exportable prior revision and block unsupported projections without coercing away meaning. Qualify types, inheritance, permission delegation and rollback. Local/no-egress operation must remain independent of Fabric services. Maps to CRA-002/017/022/024/026/034.

#### C35. Oracle AI Data Platform and Oracle Graph

**DOC/decision:** the attachment bundles distinct Oracle offerings. Evaluate Oracle database RDF Graph, property graphs/PGQL/SQL interfaces, Graph Studio and AI-platform services separately. The RDF guide explicitly describes conversion from RDF to property graphs, not identity of both models. [Oracle database 26 RDF guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/rdfrm/graph-developers-guide-rdf-graph.pdf).

**Reconstruction:** database-managed graph/relational data -> indexed semantic or property-graph operations -> analytic/UI integrations. Mapping into a property graph can change identifiers, literal representation and available inference. The attachment's trillions-of-triples claim is not an executed benchmark.

**INV-35, INFERENCE:** enterprise database coupling and separately licensed features can reduce deployment flexibility. EOIP should support Oracle through versioned adapters and source mappings without making it mandatory, and record exact capability/edition dependencies. Test cross-model conversion, source policy, query semantics and export. No Oracle AI Data Platform entitlement is inferred from database ownership. Maps to CRA-002/017/024/034/035/036.

#### C36. Cosmo Tech

**DOC/decision:** Cosmo Tech provides simulation-oriented digital-twin workflows. Its public BuildMyApp documentation exposes workspace/API concepts; this does not disclose the complete solver internals or establish a general OWL reasoner. [Workspace/API baseline, 5.0.0](https://cosmo-tech.github.io/BuildMyApp/5.0.0/tutorials/api/workspace/).

**Reconstruction:** model/data -> workspace/scenario configuration -> runner execution -> results and comparison. Treat relationships in a simulation model separately from empirical causal identification. Cloud integrations and simulator packages need independent licensing and availability checks.

**INV-36, INFERENCE:** a graph-shaped scenario does not establish causal correctness or operational safety. EOIP should require model assumptions, versioned inputs, seeds, uncertainty and validation against known scenarios; display simulated outputs separately from observed facts. Test repeated seeded execution, cancellation, parameter sensitivity and prohibited action boundaries. Do not market existing heuristic blast-radius functions as calibrated simulation. Maps to CRA-027/028/031/036.

#### C37. Cinchapi Concourse

**DOC/decision:** the maintainer guide describes a temporal document/record graph with transactions, search, CCL and time-travel APIs, and identifies Apache-2.0 licensing. It is unrelated to the Concourse CI project; similarly named search results were excluded. [Concourse guide](https://docs.cinchapi.com/concourse/), [graph operations](https://docs.cinchapi.com/concourse/graph/).

**Reconstruction:** dynamically typed record fields and links -> transactional update/history -> current or historical query/navigation. Its query language is not SPARQL or OWL. Exact current cluster semantics and binary versions remain evaluation work.

**INV-37, INFERENCE:** flexible temporal records still require enterprise identity, schema and retention policy. EOIP should keep stable canonical identifiers and distinguish valid time from transaction time, making corrections and retractions explicit. Test historical links after identity merges, concurrent edits, clock skew and authorized deletion. Do not equate time travel with a complete bitemporal or compliant retention design. Maps to CRA-016/023/028/033/040.

#### C38. Essential Cloud

**DOC/decision:** Essential is an enterprise-architecture platform with a meta-model spanning business, applications, information and technology. It is a model/workflow reference for impact analysis rather than a general ontology engine. [Ontology-based enterprise architecture](https://enterprise-architecture.org/ontology-enterprise-architecture/), [meta-model](https://www2.enterprise-architecture.org/meta_model.php).

**Reconstruction:** architecture concepts/relationships -> populated repository -> published views and dependency analysis. Open-source Essential and commercial Cloud are different distribution/support arrangements. A familiar EA diagram does not prove automated freshness of source evidence.

**INV-38, INFERENCE:** manually populated architecture views risk stale dependencies. EOIP should combine curated intent with observed runtime/source facts, surface conflict and freshness, and retain who approved an override. Qualify source change -> architecture impact -> reviewed decision without silently replacing curated knowledge. Measure stewardship work and stale facts, not only diagram density. Maps to CRA-010/022/028/029/030.

### Category 6: Catalogs, Context and Data Intelligence

#### C39. OpenMetadata

**DOC/decision:** OpenMetadata documents schema-first contracts, REST, a metadata store and search index, plus an MCP surface. A metadata graph does not imply an RDF triplestore. The inspected 1.11 architecture describes MySQL and Elasticsearch; snapshot documentation is not a current production dependency lock. [Architecture](https://docs.open-metadata.org/v1.11.x/developers/architecture), [MCP](https://docs.open-metadata.org/v1.12.x/how-to-guides/mcp).

**Reconstruction:** common schema -> generated server/ingestion/UI models -> metadata writes/events -> entity store and search projections. This is a strong pattern for EOIP's cross-language contract generation.

**INV-39, INFERENCE:** multiple projections can disagree after failed indexing or permission change. EOIP should track source revision, projection watermark and policy epoch, support replay and show stale/unavailable states. Test that an ACL change removes a result from API, UI, vector search and MCP before declaring revocation complete. Maps to CRA-001/003/025/029/031/039.

#### C40. data.world

**DOC/decision:** data.world documents a knowledge-graph-backed catalog with base, edit and merged layers. User overrides can supersede later imported changes; this is a substantive model policy to assess. Current documentation identifies data.world from ServiceNow. [Catalog layers](https://docs.data.world/en/168180-understanding-the-catalog-graph.html), [current introduction](https://docs.data.world/en/312653-an-introduction-to-data-catalog.html).

**Reconstruction:** collector/configuration graph + explicit edit graph -> merged current graph -> discovery and query. UI presentation and raw source state are therefore intentionally different layers, not accidental duplication.

**INV-40, DOC/INFERENCE:** persistent overrides can conceal evolving source truth if conflict is not explicit. EOIP should retain observed/asserted/curated layers with precedence rules, conflict indicators and steward review, never silently flattening disagreements. Test a source rename after a human override, subsequent retirement and exact restoration. SaaS residency and export rights require contract evaluation. Maps to CRA-010/022/028/029/034.

#### C41. Collibra

**DOC/decision:** Collibra documents an operating model of communities, domains, asset/relation/attribute types and statuses, plus REST, GraphQL and workflow APIs. This is governance infrastructure, not evidence of unrestricted OWL semantics. [Operating model](https://productresources.collibra.com/docs/collibra/latest/Content/to_operating-model.htm), [APIs](https://developer.collibra.com/api).

**Reconstruction:** typed governance assets -> responsibilities/permissions -> forms/workflows -> publication/integration. Public and internal APIs are explicitly distinguished. Workflow scripts execute with material platform coupling; the vendor warns against heavy workflow processing.

**INV-41, DOC/INFERENCE:** governance customizations can become long-running privileged scripts. EOIP should separate declarative approval workflows from isolated compute jobs, expose a stable public extension API and version migrations. Prove bounded execution, denial, cancellation and workflow recovery after restart. Do not depend on private endpoints because they appear in browser traffic. Maps to CRA-002/022/027/031/039.

#### C42. Alation

**DOC/decision:** Alation's Open Connector Framework distinguishes metadata extraction, profiling, query-log ingestion and lineage. Lineage can be derived from parsed statements and view definitions. These are separate permissions and schedules. [OCF source types](https://docs.alation.com/en/latest/sources/CatalogSources/CatalogSourceTypes.html), [lineage](https://docs.alation.com/en/latest/sources/WorkwithCatalogData/TableLineage.html).

**Reconstruction:** source credentials and capabilities -> metadata/query logs -> parsed usage/lineage -> catalog search and curation. A connector's ability to connect does not mean it can safely retrieve all query history.

**INV-42, INFERENCE:** query logs and sampled data can expose literals and sensitive business activity. EOIP should default to metadata-only discovery, request profiling/log scopes separately, redact sensitive fields before indexing and record provenance. Test incomplete SQL dialects, dynamic statements and unsupported lineage as uncertainty, not invented edges. Maps to CRA-004/009/024/029/040.

#### C43. OvalEdge

**DOC/decision:** OvalEdge describes crawler, profiler and lineage operations, connector administration and an n-tier deployment supporting multiple pods. Its connector guide distinguishes source permissions, policy synchronization and metadata storage. A context-graph product description does not itself prove an RDF/OWL engine. [Architecture](https://support.ovaledge.com/reference-architecture-overview), [connectors](https://support.ovaledge.com/ovaledgeconnectors).

**Reconstruction:** scheduled source jobs -> metadata repository/profiling/lineage -> governed discovery and interfaces. Source-as-master versus catalog-as-master permission behavior is a significant operational distinction.

**INV-43, INFERENCE:** permission synchronization can accidentally become an authoritative write-back. EOIP should default to source-authoritative, read-only permissions and require explicit approved provisioning actions for any policy write. Test loss of source scope, stale ACL snapshots, partial crawl and rollback of a failed provisioning action. Maps to CRA-003/004/009/027/029/040.

#### C44. DataHub

**DOC/decision:** DataHub documents schema-first metadata, REST/GraphQL, Kafka-based changes and metadata services. Its architecture page's scale numbers remain vendor/maintainer claims, not a benchmark run here. Core and Cloud must be evaluated separately. [Architecture](https://docs.datahub.com/docs/architecture/architecture).

**Reconstruction:** typed metadata aspects/proposals -> metadata service and event stream -> search/graph projections -> APIs/UI and automation. This supports decoupled ingestion and ownership, with eventual-consistency costs.

**INV-44, INFERENCE:** distributed projections need replay, schema evolution and event-lag visibility. EOIP should publish an event compatibility contract, per-projection checkpoints, idempotent consumers and repair jobs. Prove restart/replay does not duplicate facts and policy changes propagate even during backlog. Choose a durable event system from actual workload evidence rather than requiring Kafka everywhere. Maps to CRA-002/010/029/031/032/039.

#### C45. Apache Atlas

**DOC/decision:** the inspected architecture describes a type system, graph engine using JanusGraph, REST and Kafka integration. This historical 2.0 baseline should not determine contemporary dependency versions. Atlas is metadata governance, not automatically master-data management or OWL reasoning. [Architecture](https://atlas.apache.org/2.0.0/Architecture.html).

**Reconstruction:** source hooks -> notifications -> typed entities/classifications -> graph persistence/indexing -> discovery and downstream governance integration. Classification propagation requires its own policy semantics.

**INV-45, INFERENCE:** ecosystem-specific hooks and several stateful infrastructure dependencies increase operational and integration work. EOIP should make acquisition protocols pluggable, separate catalog models from storage technology, and offer small versus scaled deployment profiles. Prove ordered classification/deletion propagation, complete export and timed restore across all projections. Maps to CRA-002/009/029/031/033/035.

### Category 7: Ontology-as-Code, Validation and Documentation

#### C46. ROBOT

**DOC/decision:** ROBOT provides composable ontology operations and reasoner integrations. Its reason command distinguishes logical validation, classification and different reasoners; report runs quality queries and can fail on severity. A successful subset/profile run does not establish complete ontology correctness. [Reason](https://robot.obolibrary.org/reason.html), [report](https://robot.obolibrary.org/report).

**Reconstruction:** versioned ontology/import closure -> CLI operations -> reasoner/report -> release artifacts. Report documentation describes memory limitations, disk-backed options and result truncation; preserve those limits in receipts. ROBOT's BSD license does not clear bundled reasoners and vocabularies.

**INV-46, DOC/INFERENCE:** CI can become falsely green if errors are configured away or reports are truncated. EOIP should make release policy explicit, bind artifacts to inputs and prohibit success when required checks were skipped, unsupported or incomplete. Test timeout, missing import, incoherence and intentionally failing quality rules. Maps to CRA-018/019/022/035/037.

#### C47. pySHACL

**DOC/decision:** pySHACL is an Apache-2.0 Python SHACL validator using RDFLib and optional reasoning/features. It exposes distinct conformant, nonconformant, runtime-error and not-implemented exit outcomes. Do not collapse every nonzero outcome into ordinary invalid data. [Maintainer documentation](https://github.com/RDFLib/pySHACL).

**Reconstruction:** data graph + shapes + optional ontology/feature configuration -> validation -> structured report and status. It fits an initial EOIP validation worker, subject to exact dependency pins and resource/security qualification. SHACL-JS and advanced rules are not enabled by default merely to satisfy a broad feature label.

**INV-47, DOC/INFERENCE:** general validation can consume unbounded CPU/memory or trigger unsafe imports/functions. EOIP should isolate workers, restrict remote retrieval, bound reports and distinguish unsupported, cancelled and timed-out jobs. Compare supported Core constraints with an independent implementation; verify failed validation cannot publish. Maps to CRA-002/020/031/035/037.

#### C48. TopBraid SHACL API

**DOC/decision:** the inspected Apache-2.0 Jena-based library supports Core/SPARQL validation and advanced rules. Its README distinguishes former compact-syntax/JavaScript coverage by version. It is not the commercial EDG product. [SHACL API](https://github.com/TopQuadrant/shacl).

**Reconstruction:** Jena models -> shapes engine -> validation report/rule results; command or service wrappers supply lifecycle and authorization. Exact version compatibility with Jena and extensions must be pinned.

**INV-48, DOC/INFERENCE:** engine-specific extensions and version changes can undermine portable validation. EOIP should expose a standards profile plus optional extension namespace, reject unsupported constraints and compare pySHACL/Jena-based results on the supported intersection. Report intentional differences and engine bugs rather than averaging conflicting answers. Maps to CRA-002/019/020/022/037.

#### C49. OOPS!

**DOC/decision:** OOPS! offers ontology pitfall analysis through a documented XML POST service and a Docker deployment option. Its pitfall catalogue and implemented checks are not identical sets. Hosted evaluation can involve retention of submitted ontologies; the UI includes a copy-retention choice. [Service](https://oops.linkeddata.es/webservice.html), [deployment/UI](https://oops.linkeddata.es/).

**Reconstruction:** submitted ontology/URI -> implemented pitfall checks -> issue report. Pitfall warnings do not replace OWL consistency or SHACL instance validation. Current image contents, license and maintenance need artifact review before embedding.

**INV-49, DOC/INFERENCE:** online linting introduces egress and service-dependency risks. EOIP should offer offline lint rules and explicit opt-in external analysis with redaction, retention and version controls. Preserve unsupported checks as NOT_RUN; never infer a clean model from an empty or failed remote response. Maps to CRA-020/022/026/035/037/040.

#### C50. WIDOCO and LODE

**DOC/decision:** WIDOCO generates ontology documentation with ontology metadata, cross references and integrated components. Legacy LODE announces an August 2026 move to OpenCitations, and the inspected legacy repository identifies ISC, not the supplied blanket MIT label. New and bundled copies require separate license checks. [WIDOCO](https://github.com/dgarijo/Widoco), [legacy transition notice](https://github.com/essepuntato/LODE), [current LODE](https://github.com/opencitations/lode).

**Reconstruction:** pinned ontology/imports -> extraction/rendering/templates -> navigable HTML and metadata. Documentation generation can have remote integrations; a locally started generator does not guarantee offline operation.

**INV-50, DOC/INFERENCE:** generated HTML may become stale or include unsafe authored markup. EOIP should generate docs from signed release manifests, sanitize labels/descriptions, record engine versions and serve strict content policies. Test hostile annotations, broken references, no-network execution and build/release hash match. Maps to CRA-018/022/030/035/039.

### Category 8: Enrichment, NLP and Ontology Learning

#### C51. Mondeca suite and CAM

**DOC/decision:** the current vendor describes ITM, Content Auto-Tagging Manager and Knowledge Browser as separate modules. CAM integrates linguistic/ML services, semantic lookup/scoring and reviewable content tagging, including multiple media types. These are documented capabilities, not demonstrated EOIP adapters. [Suite](https://mondeca.com/software/), [CAM](https://mondeca.com/products-cam/).

**Reconstruction:** vocabulary/model + pipeline configuration -> analysis/enrichment -> reviewed annotations -> search/publication. Provider-composed pipelines require individual data-processing and model-policy review; multilingual content support is not the same as complete accessible localization.

**INV-51, INFERENCE:** enrichment orchestration can obscure which model, rule or source produced a tag. EOIP should attach evidence spans, model/rule versions, licensing, calibrated confidence and reviewer decisions to every generated assertion. Test pipeline substitution, partial provider failure and strict no-egress modes without fabricated tags. Maps to CRA-014/021/026/030/040.

#### C52. Diffbot

**DOC/decision:** Diffbot exposes extraction and NLP APIs for entities/facts and an external knowledge graph. Current NLP documentation explicitly says Open Facts is disabled and describes differing language/size limits. Do not repeat the attachment's unconstrained extraction description as current capability. [Natural Language API](https://www.diffbot.com/docs/natural-language/).

**Reconstruction:** URL or text -> extraction/classification/linking -> structured results, sometimes enriched with external-KG facts. External facts must remain distinguishable from facts present in the submitted document; retrieval is not evidence that a source asserted them.

**INV-52, DOC/INFERENCE:** external enrichment can introduce egress, licensing, provenance and correctness ambiguity. EOIP should separate source extraction from external enrichment, keep source spans and data rights, and permit local replacement. Test restricted documents never leave the boundary and external facts cannot inherit the source's authority. Honor API payload/rate limits and expose disabled features. Maps to CRA-010/014/023/026/035/040.

#### C53. DeepOnto

**DOC/decision:** DeepOnto combines Python deep-learning workflows with OWL API through a JVM bridge, plus ontology processing, reasoning and alignment. BERTMap's pipeline supplies a reference for model-assisted alignment with candidate evaluation. [Architecture](https://krr-oxford.github.io/DeepOnto/), [alignment](https://krr-oxford.github.io/DeepOnto/bertmap/).

**Reconstruction:** source/target ontology annotations -> candidate text/corpora -> learned similarity/alignment -> reasoning/repair/evaluation. An ML match is not an entailed equivalence; adding equivalence can make an ontology incoherent. Exact model/dependency/compute requirements vary.

**INV-53, INFERENCE:** confident-looking neural alignment can amplify wrong identity or schema links. EOIP should record candidate evidence, evaluate calibration, require high-impact review and run consistency checks before publication. Prove rejected/removed matches retract dependent inferences and indexes. Use isolated JVM/model workers rather than blocking API threads. Maps to CRA-019/022/023/026/036.

#### C54. spaCy and textacy

**DOC/decision:** spaCy's EntityLinker needs a knowledge base, candidate generation and a trained disambiguation model; NER alone is not canonical entity linking. textacy adds text-processing utilities on spaCy, not a ready-made enterprise identity system. [EntityLinker](https://spacy.io/api/entitylinker/), [textacy README](https://github.com/chartbeat-labs/textacy/blob/main/README.md).

**Reconstruction:** parsed text -> mentions -> KB candidates -> context-based selection -> IDs and evidence offsets. Separately evaluate model, vocabulary and training-data terms. A code library's license does not confer rights in every downloadable model/corpus.

**INV-54, INFERENCE:** generic models and abbreviation ambiguity can mislink enterprise terms. EOIP should provide tenant-scoped candidate indexes, NIL/no-match output, curator feedback and domain/language evaluation. Never merge enterprise identities solely because two mentions share a label. Pin spaCy/textacy compatibility and maintain an alternative if dependencies age. Maps to CRA-021/023/026/035/036.

### Supplemental Library

#### C55. OWL API

**DOC/decision:** OWL API is a Java ontology object model and tooling interface, used by editors and reasoner integrations. It is not by itself a complete DL reasoner or graph database. Its repository includes historical dual-license changes; the exact chosen distribution and dependencies must be reviewed. [OWL API source](https://github.com/owlcs/owlapi).

**Reconstruction:** parser -> OWL structural objects/ontology manager -> transformations/profile checks -> pluggable reasoner interface -> serialization. Correct handling of imports, anonymous individuals and annotations matters more than a generic `owl_supported=true` flag.

**INV-55, INFERENCE:** embedding a mutable ontology manager and reasoner in an API process can couple memory and lifecycle. EOIP should use a versioned semantic-worker protocol with exact imports, deadlines, resource limits and typed results. Evaluate ELK, HermiT, FaCT++ or alternatives only against their supported profiles and exact licenses; the names mentioned in the attachment are not automatic approved dependencies. Maps to CRA-002/016/018/019/035.

### 6.1 Version and Investigation Register

| Family | Reviewed baseline | What must be pinned before execution |
|---|---|---|
| Protege/WebProtege | Desktop release listing; classic web 4.0.2 listing plus next-gen transition README | Desktop/plugin/reasoner versions; classic versus next-gen deployment |
| TopBraid | Composer legacy docs; EDG 8.3 concepts and 9.1 release note | Exact current commercial product/edition; ADS/SHACL/Jena versions |
| OntoStudio | Current X page plus legacy OntoBroker help | X build, bridge/server compatibility; do not reuse legacy install instructions |
| Graphwise | 2026 transition guide and GraphRAG 1.2.0 integration documentation | Per-component version, migration map and entitlement |
| GraphDB | Reasoning 11.3 / inference 11.4 documentation | Current tested edition/version/ruleset and known conformance differences |
| AllegroGraph | 9.0.3 index / 9.0.2 FedShard definition | Matching engine/config/client versions |
| n10s | Version 4.0 guide plus maintainer source | Actual Neo4j/n10s pairing and database edition |
| Anzo | Historical 5.4 deployment guide | Current Anzo/AnzoGraph distribution, support and architecture |
| OpenMetadata/DataHub | 1.11/1.12 documentation; DataHub architecture page version 1.7.0 | Stable edition, image digests, schema/connector versions |
| Oracle | Database 26 RDF guide | Specific database and AI/graph services; entitlements |
| Fabric | Current service documentation, with ontology preview distinguished | Tenant/region/service rollout, preview restrictions and API contract |
| Cosmo Tech | BuildMyApp 5.0.0 documentation | Compatible API, simulation packages and deployment |
| gist | Current page identifies 14.1.0 | Ontology artifact hash, import closure and attribution |
| Karma | Repository archived 2025-04-16 | Maintained replacement/fork decision before runtime adoption |
| LODE | Legacy notice dated 2026-08-04; current OpenCitations repository | Exact new distribution, WIDOCO-bundled copy and licenses |
| All others | Official living docs/repositories linked above; not installed here | Exact release/commit, artifact checksum, source/license snapshot and lifecycle |

Do not infer a latest version from an unversioned URL or a search crawl date. The register deliberately leaves unverified releases unresolved.

## 7. Prioritized Gap Backlog and Inversion Traceability

Priority P0 protects correctness, tenant data and recoverability; P1 completes valuable journeys; P2 adds advanced capability after foundations. Each item requires the named CRA acceptance clauses, not just file existence.

| Backlog | Priority | Scope and acceptance summary | Inversions addressed | Requirements |
|---|---|---|---|---|
| B01 | P0 | Versioned contracts, decision records, truthful capability discovery and qualified plugin execution | 05,08,10,21,23,29,39,44,45,55 | CRA-001/002/039 |
| B02 | P0 | Identity/workspace/source ACL policy enforced across data, derivations, indexes, jobs and exports | 05,19,20,24,39,43 | CRA-003/010/040 |
| B03 | P0 | Existing connection factory audited; explicit fallbacks, vendor auth, sandboxed push/pull, conformance suite | 07,27,31,42,43,45 | CRA-004..011 |
| B04 | P0 | Bounded safe parsers and dependency readiness; no silent data loss or unbounded chunk loop | 07,30,49,51,52 | CRA-012..015 |
| B05 | P0 | Standards-based RDF term fidelity and explicit LPG mapping losses | 01,03,16,23,26,35,55 | CRA-016/017 |
| B06 | P0 | Real profile-qualified reasoning and constraint enforcement, including unsupported/error states | 01,04,17,18,20,22,46,47,48,55 | CRA-019/020 |
| B07 | P1 | Durable ontology registry, governed changes, term stewardship and migration | 02,06,08,09,10,12,13,14,15,16,25,32,34,46,49,50 | CRA-018/021/022/034 |
| B08 | P1 | Identity resolution with evidence, reversible merge/split and inferred-dependency repair | 13,25,37,52,53,54 | CRA-023/028/040 |
| B09 | P1 | Scoped bounded query/federation with visible plans and qualified dialects | 03,18,19,21,23,27,28,29,35 | CRA-024 |
| B10 | P1 | Real versioned retrieval and evidence-bound AI with no hidden provider fallback | 04,10,11,14,16,39,51,52,53,54 | CRA-025/026 |
| B11 | P1 | Governed operational actions and honest temporal/simulation capabilities | 33,36,37,38,41,43 | CRA-027/028 |
| B12 | P1 | Catalog/context/lineage with observed versus curated precedence and freshness | 18,24,28,38,39,40,42,43,44,45 | CRA-029 |
| B13 | P1 | Complete accessible modular UI flows and customization across supported profiles | 01,03,06,09,16,28,32,38,50,51 | CRA-030 |
| B14 | P0 | Durable jobs, replay/outbox, truthful telemetry and tested restore | 12,20,23,25,29,30,31,36,39,41,44,45 | CRA-031..033 |
| B15 | P0 | Commercial distribution, SBOM, signed packages, no unlawful dependency relabelling | 02,05,13,15,21,32,35,46,49,50,54,55 | CRA-035 |
| B16 | P0 | Independent correctness/performance/security qualification and content-bound receipts | 01..55, especially 17,22,27,46,47,48 | CRA-036/037 |
| B17 | P1 | Honest support/service commitments, SDK/developer ecosystem and operator handoff | 02,10,23,35,41,44,45,50 | CRA-038/039 |

Every INV-01..55 maps to at least one backlog row and requirement. This does not claim every possible competitor defect was discovered. Newly observed limitations must receive new evidence and traceability, not be backfilled as facts.

## 8. Recommended Architecture and Module Boundaries

### 8.1 Current-to-Target Architecture

Current inspected shape:

```text
React GUI / VS Code / API clients
               |
       Composed FastAPI application
               |
   GraphStore + ontology + query + acquisition + jobs + AI modules
               |
   HugeGraph / Neo4j / Neptune adapters or explicit memory harness
               |
   Ancillary state and optional model/provider/index integrations
```

Target design, PROPOSED:

```text
Enterprise systems ---- push/webhooks ----+---- bounded poll/crawl agents
                                         |
                             Policy-aware acquisition gateway
                                         |
                        Raw object vault + source event journal
                                         |
                      Isolated parser/extractor/mapping workers
                                         |
                         Staged assertions + evidence + ACLs
                                         |
                Validation / reasoning / identity review / approval
                                         |
                            Authorized publication boundary
                                         |
      +----------------------+-----------+----------------------+
      |                      |                                  |
 Canonical graph       Ontology/revision registry          Control database
      |                      |                                  |
      +------- durable outbox and scoped projection workers -----+
                             |
           Search + vector + catalog + analytics projections
                             |
           Query/retrieval/context/answer and governed-action APIs
                             |
               Accessible modular GUI / SDK / MCP adapters

Cross-cutting: trusted principal, policy epochs, secrets/egress, audit,
resource budgets, telemetry, recovery, licensing and feature entitlements.
```

Do not replace existing working modules wholesale. First measure their contracts and introduce compatibility adapters. Prefer one canonical owner for each state type. Derived indexes are rebuildable projections; they do not become alternative authorities for asserted facts or permissions.

### 8.2 Interfaces and State Ownership

| Boundary | Owns | Must not own |
|---|---|---|
| Connector factory | Provider registration/config validation/capability selection | A claim that every registered source is certified |
| Acquisition worker | Vendor cursor/lease and received source events | Final ontology publication or broad service-account authority |
| Raw vault | Immutable revision bytes, checksums, access metadata, retention | Publicly guessable download URLs |
| Parser/extractor | Bounded extraction results, source locators and warnings | Automatic acceptance of model-generated claims |
| Semantic worker | Pinned parsing/reasoning/validation runs and artifacts | Tenant routing from untrusted request text |
| Registry/governance | Ontology releases, imports, review and publication manifests | Mutable unversioned global model singleton |
| Canonical graph | Authorized accepted assertions and stable identities | A hidden vector fallback presented as a fact |
| Query/retrieval | Typed plan, filtered results and evidence selection | Remote unrestricted execution of user strings |
| Action executor | Specific authorized side effects and compensation journal | General purpose privileged code execution |
| GUI | Task state, accessible views and authorized drafts | Independent truth, capability or authorization decisions |

### 8.3 Engine Selection Strategy

Initial candidates, not procurement approvals: a pySHACL-based bounded worker for supported validation; OWL API plus a profile-appropriate reasoner for formal ontology checks; Jena/Fuseki or RDF4J as a semantic-store candidate; Ontop for qualified relational OBDA; existing GraphStore adapters for operational projections; Morph-KGC or another measured mapper for batch RDF. Evaluate alternatives against the same corpus before selection.

Use independent adapters for logical classification, instance validation, graph storage, vector search and LLM generation. No hand-written claim of complete OWL DL/SPARQL/SHACL implementation. Engine absence yields UNAVAILABLE, not an empty result or fabricated successful fallback. Reasoners and copied ontology assets need separate license review even when the facade library is permissive.

## 9. Universal Connection Factory and Enterprise Source Coverage

Universal means **an open contract for adding systems**, not prebuilt support for every undocumented API. A connector declares discovery, baseline, polling, webhook, CDC, delete, ACL, attachment, lineage, write-back and resume independently. Each capability has supported versions, scopes, limits, a qualification receipt and a truthful unavailable reason.

| Source family | Required integration work | Critical qualification |
|---|---|---|
| Jira | Cloud/Data Center identity, project/issue/link/comment/attachment acquisition | Pagination, custom fields, deletes and issue/project permissions |
| Wiki / Confluence | Generic wiki adapter plus Confluence-specific page/space/version/attachment support | Restricted pages, inherited restrictions, macro/body fidelity and deleted versions |
| Rally | Workspace/project-scoped artifacts and relationships | Scope hierarchy, throttling and revision checkpoints |
| ServiceNow | Table/CMDB/incident/change/knowledge profiles | ACL-aware reads, reference expansion, domain separation and approved writes |
| Snowflake | Metadata, lineage/query-history where granted, optional sampled or virtualized data | Role/warehouse scopes, masking/row policies, costs and SQL dialect |
| GitLab / GitHub | Repositories, commits, merge/pull requests, issues, CI artifacts and code references | Installation/project scopes, rename/delete, branch changes, private assets and rate limits |
| qTest | Projects/tests/runs/results/defects | API edition, project ACLs and incremental results |
| API Portal | Configured provider profile, OpenAPI/documentation/version acquisition | Product identity is required; do not invent a standard vendor API |
| Artifactory | Repository/artifact/build metadata and permitted content | Repository ACL, checksum identity and signed artifact provenance |
| Splunk | Search/knowledge/configuration/log profiles | Search budgets, sensitive events and least-privilege tokens |
| Slack | Enterprise-approved conversations/messages/files/events | Channel membership, private-message prohibition by default, edits/deletes and retention |
| Kibana / Elasticsearch | Saved objects, dashboards and separately authorized index access | Spaces versus index permissions; Kibana API is not Elasticsearch data authority |
| Fortuna | Explicit identification and discovery workshop | Ambiguous product/internal system: custom adapter until contract supplied |
| Grafana (attachment: graffana) | Dashboards/data-source metadata and optional approved query results | Organization/folder/data-source permissions and no credential extraction |
| Documentum | Repository objects, versions, renditions, relationships and metadata | ACL/inheritance, retention/legal hold, checkout/version and licensed API |
| Other systems | REST/OpenAPI, GraphQL, SOAP, JDBC/ODBC, SFTP/object store, file, event/CDC plugin families | Per-protocol security plus provider-specific mapping; no fake certification |

Prefer APIs and source-native event/CDC mechanisms over scraping when equivalent permitted access exists. Crawling is authorized, bounded and allowlisted, with attachment processing isolated. Store operational cursors separately from credentials; secrets are references, never ordinary configuration values or browser storage.

The specific vendor documentation for all connector API versions was not individually researched in this competitive desk review. CRA-005..009 require that research and licensed sandbox qualification before implementing or advertising each adapter. Existing adapter names are discovery leads, not proof of completion.

## 10. Multiformat Acquisition and Knowledge Construction

Required source-to-knowledge sequence:

```text
Accept -> quarantine/scan -> identify actual format -> bounded decode
-> source-located sections/frames/transcripts -> extract candidates
-> normalize/map -> resolve candidates -> validate -> review -> publish
-> update graph/meta-graph/search/vector projections -> acknowledge cursor
```

| Input | Minimum meaningful result | Must not be called complete |
|---|---|---|
| TXT/JSON/CSV | Encoding/schema-aware structure, rows/fields and source locations | Decoding bytes without field meaning |
| HTML/XML | Sanitized structure, safe parser, explicit remote-resource policy | Rendering scripts or resolving arbitrary external entities |
| DOCX/PPTX/XLSX | Paragraphs/slides/sheets/tables, stable locators, formulas separate from cached values | File extension recognition alone |
| DOC/PPT/XLS/RTF | Qualified local converter/parser and explicit fidelity diagnostics | Assuming legacy conversion is lossless |
| EML/email/MSG | Message identity, headers, body parts and nested attachment provenance | Treating mailbox access or one MIME part as the complete message |
| Image/scanned document | Metadata plus optional OCR with coordinates/confidence | Metadata-only output labelled visual understanding |
| Video/audio | Authorized decode, timestamps, transcript, frame/scene sampling and explicit multimodal capability | A filename or unsupported media type yielding success |
| Engineering diagram | Notation-aware parsing or reviewed visual extraction, components/ports/links with uncertainty | Mapping every box to Service and every arrow to CALLS |
| Archives | Global depth/member/expanded-byte/time budgets and safe names | Per-member bounds that allow total expansion to exceed limits |

Images/video do not automatically yield correct engineering topology. A model suggestion remains a candidate with region/time evidence and steward review. Preserve raw bytes and extraction versions so corrections can rebuild all derivatives. PDF and audio support are sensible additional plugin requirements, not inferred native coverage of the existing parser catalog.

Build distinct but linked graphs: source/resource graph, accepted domain graph, schema/meta-graph, provenance/derivation graph, lineage graph, policy/security graph, event/temporal graph and optional vector-similarity projection. A meta-graph cannot be just the same data graph relabelled; its objects are models, types, predicates, mappings, profiles and versions.

## 11. Concrete Designs and Algorithms

### 11.1 Example Canonical Records

These are proposed contracts to reconcile with existing Pydantic source-event/normalized/evidence/revision models, not duplicate classes to create blindly.

```json
{
  "contract_version": "1.0",
  "event_id": "source-instance:opaque-vendor-event-id",
  "operation": "upsert",
  "source_instance_id": "jira-eu-01",
  "resource_id": "opaque-vendor-resource-id",
  "source_revision": "opaque-vendor-revision",
  "observed_at": "2026-10-16T00:00:00Z",
  "content_sha256": "64-lowercase-hex-characters",
  "acl_revision": "opaque-acl-version",
  "payload_ref": "authorized-object-reference",
  "parser_profile": "text-office-v1",
  "correlation_id": "request-or-job-id"
}
```

Tenant/workspace context must be established by trusted server authorization. External payload fields are validated and cannot select another tenant's storage. Event IDs need a source-defined uniqueness strategy; content hash alone cannot represent ACL-only changes or deletion.

```json
{
  "assertion_id": "urn:eoip:assertion:opaque-id",
  "subject": {"kind": "iri", "value": "urn:example:service:A"},
  "predicate": {"kind": "iri", "value": "urn:example:dependsOn"},
  "object": {"kind": "iri", "value": "urn:example:service:B"},
  "knowledge_state": "proposed",
  "source_revision": "r17",
  "evidence_locator": {"document_id": "d1", "page": 2, "start": 42, "end": 87},
  "extraction": {"provider": "configured-provider", "model_revision": "pinned-revision", "score": 0.83},
  "ontology_revision": "o9",
  "policy_epoch": "p12",
  "derivation_id": null
}
```

Scores are not probabilities unless calibrated against a documented corpus. Policy labels, valid/transaction time, language/datatype, graph identity and deletion metadata are additional required schema fields defined in CRAr.md.

### 11.2 Safe Incremental Publication

```text
receive(source_event, trusted_scope)
  verify signature or authenticated source and authorized scope
  deduplicate by source instance + event ID + contract semantics
  acquire lease and check expected cursor/revision
  persist raw event and payload reference durably
  parse/extract with budgets in an isolated worker
  stage candidates with source ACL and evidence
  validate syntax, model profile, shapes and identity changes
  if unsupported/error/cancelled/timeout: do not publish; retain explicit result
  bind review/approval to candidate, ontology and policy revisions
  publish canonical mutation + outbox atomically where supported
  otherwise use a durable intent, idempotent sinks and reconciliation protocol
  acknowledge source cursor only after declared durability boundary
  project updates idempotently; expose lag and incomplete projections
```

No distributed exactly-once claim is made. A connector can provide at-least-once delivery with effectively-once published effects under tested idempotency. Multi-store failure requires repair, not a hidden successful response.

### 11.3 Reasoning and Authorization

```text
classify(pinned_ontology, requested_profile, resource_budget)
  load only approved, hash-pinned import closure
  check profile and fail on unsupported constructs
  run selected qualified engine in isolated worker
  retain consistency/incoherence/entailment results and explanations
  write derived facts to a separate revisioned graph
  attach supporting assertions and source-policy dependencies
  invalidate/recompute when a support, ontology or ACL changes
```

An entailment using restricted evidence can leak that evidence. Default derived access requires access to all supporting facts used by the explanation; any authorized declassification is a separate audited policy. Multiple derivations and alternate permitted proofs must be represented explicitly. Global reasoning and per-user filtering are not automatically safe together.

### 11.4 Proposed API Fragment

This OpenAPI 3.1 fragment is a design, not a currently implemented endpoint. Reconcile with composed OpenAPI and existing route ownership before adding it.

```yaml
openapi: 3.1.0
info: {title: EOIP Semantic Jobs - proposed, version: 1.0.0}
paths:
  /api/v1/semantic/validations:
    post:
      operationId: submitSemanticValidation
      security: [{bearerAuth: []}]
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema: {type: string, minLength: 1, maxLength: 128}
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              required: [dataset_revision, ontology_revision, shapes_revision, profile]
              properties:
                dataset_revision: {type: string, minLength: 1}
                ontology_revision: {type: string, minLength: 1}
                shapes_revision: {type: string, minLength: 1}
                profile: {enum: [shacl-core-2017]}
      responses:
        '202':
          description: Authorized durable job accepted; not a validation pass
          content:
            application/json:
              schema:
                type: object
                required: [job_id, status_url]
                properties:
                  job_id: {type: string}
                  status_url: {type: string}
        '403': {description: Scope or capability denied}
        '409': {description: Revision or idempotency payload conflict}
        '422': {description: Invalid request or unsupported declared profile}
        '503': {description: Required validator unavailable}
components:
  securitySchemes:
    bearerAuth: {type: http, scheme: bearer}
```

Bearer authentication in the fragment is an interface example, not a replacement for production session/IdP design. Every status/download/cancel URL requires the same trusted scope and authorization. Error payloads need stable codes, field pointers and correlation without secrets.

### 11.5 Task-Oriented UI Wireframes

```text
Sources | Ontologies | Knowledge | Ask | Work | Administration

Source detail
  Name / scope / provider version / capability status / last observation
  Tabs: Overview | Resources | Mapping | Runs | Permissions | Settings
  Primary workflow: Discover -> Select -> Map -> Dry-run -> Review -> Publish
  Inspector: source preview / ACL / evidence / warnings / revision diff

Ontology release
  Version / profile / imports / state / reviewer / validation observation
  Tabs: Concepts | Axioms | Shapes | Mappings | Changes | Publication
  Views: accessible table / tree / bounded graph / expert text
  Review: precise added/removed statements, affected sources and decisions

Answer
  Question / permitted scope / freshness / provider / execution status
  Answer clauses -> evidence spans -> source revision and access decision
  Separate panels: grounded facts / inferred facts / uncertain suggestions
  Cancel / save / authorized export; no invented progress or citations
```

Use the existing design system, semantic colors and Lucide icon registry. Preserve familiar navigation and compact operational layouts. Motion is bounded, interruptible and disabled under reduced-motion preferences. No decorative redesign substitutes for backend state and complete error/loading/empty/partial/denied behavior.

## 12. Migration and Integration Plan

1. **Discover:** pin source product/edition/build, supported export/API contracts, graph/ontology license, entity counts, imports, ACLs, retention and external actions. Obtain a read-only licensed export, not undocumented scraping.
2. **Preserve:** retain raw files, checksums, source IDs, namespaces, literals/languages/datatypes, named graphs, assertions, revisions, annotations and ownership. Generate an immutable extraction manifest.
3. **Map:** create a versioned mapping IR, explicit identity policy and feature-loss ledger. OWL equivalence is not label equality; SKOS related/broader/exactMatch are not interchangeable; an LPG edge with attributes needs an assertion identity.
4. **Stage:** load into a scoped staging dataset with no live action privileges. Validate with independent parsers, selected reasoners/shapes and domain competency questions. Report unsupported features, inaccessible records and truncation separately.
5. **Compare:** compare canonicalized RDF datasets and semantics, not lexical blank-node labels or output row order. Compare business query results and permissions; record intentional projection losses.
6. **Catch up:** replay source changes from an established watermark; handle ACL-only updates and tombstones. Shadow reads without writes. Do not dual-write operational systems until deduplication/compensation is proven.
7. **Cut over:** approve a manifest binding source watermark, mapping, target revision, validation and policy. Switch routing atomically with a rollback window and observable consumer lag.
8. **Rollback:** revert read routing to the source snapshot or prior target revision, restore compatible projections, revoke new actions, replay required source deltas and verify business invariants. Never call a graph reset an undo of external writes.
9. **Retire:** only after accepted counts/queries/ACLs and restore rehearsal, retire the old path according to retention/contracts. Purge test extracts and secrets.

Proposed migration script suite, **not implemented in this task**: export manifest, convert with declared profile, validate, compare, replay, cutover and rollback commands. Their CLI names must be designed in CRA-034; do not invent executable `eoip migrate-*` commands in documentation before they exist. See section 19 for real commands that can currently be run.

## 13. Security, Legal and Compliance Assessment

### Threat Model

| Threat | Required design | Acceptance attack |
|---|---|---|
| Tenant/source ACL leak | Trusted scope, deny-by-default, source-authoritative access and scoped projections | Two tenants with colliding IDs; hidden intermediate traversal; aggregate/count leak |
| SSRF and crawl escape | Egress allowlist, scheme/port restrictions, DNS/redirect checks, metadata/private-range rules | Redirect/DNS rebinding, IPv6, proxy, embedded URL and cross-origin auth |
| Malicious file/plugin/ontology | Quarantine, safe parsers, limits, isolated workers, pinned imports | Zip/XML bombs, macros, path traversal, hostile JS/rules/imports |
| Prompt injection | Source text is untrusted data; tools use independent server policy | Document asks assistant to export restricted content or execute an action |
| Action replay/confused deputy | Exact parameter/revision approval, delegated scope, expiry and nonce/idempotency | Alter target or parameters after approval; replay or revoke before execution |
| Derived-fact disclosure | Derivation ACL composition and policy-epoch invalidation | Remove one support permission and probe answers/indexes/exports |
| Tampered update/supply chain | Signed plugin/package manifests, SBOM and provenance | Modified image/plugin/config, dependency confusion, stale signature |
| Silent data loss | Checksums, loss ledger, explicit partial states and reconciliation | Unsupported type, dropped mapping, failed projection or stale cursor |
| Retention/deletion failure | Derivative inventory and deletion workflow including indexes/caches/backups | Delete a subject and check every derived store under hold/retention policy |

### Licensing and IP Boundaries

EOIP's first-party commercial direction remains unchanged. Reusing standards and permissive libraries does not require relicensing owned EOIP code under Apache. Apache-licensed dependencies retain their conditions and notices; do not remove upstream rights. [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).

Review each exact application/library/plugin/reasoner/model/dataset/font/container component and how it is linked, modified, delivered or hosted. GPL/AGPL/LGPL obligations depend on the component and actual integration/distribution; a process or service boundary is not a blanket exemption. Commercial tools usually require explicit OEM/embedding/redistribution rights. Publicly readable source is not sufficient permission to copy it. No patent freedom-to-operate or jurisdiction-specific legal opinion is provided here.

Important corrections: classic WebProtege's inspected license is BSD-style; gist is CC BY 4.0 ontology content; legacy LODE identifies ISC and has a successor; TopBraid SHACL API's open-source code is distinct from EDG; Neo4j/n10s and their editions require separate checks. Models, scientific vocabularies and source-system content have independent rights. Maintain the existing licensing release checklist, including its unresolved `extract-msg` issue, rather than silently approving it.

Use a clean-room feature analysis: record public facts and independent designs, preserve provenance, do not copy proprietary code/UI assets, and do not claim ownership of competitor ontologies. Standards compatibility must be measured against the exact standard/version, not implied by brand names.

## 14. Benchmark and QA Plan

No comparative benchmark was executed. Numbers below are qualification targets and workload designs, not results.

### Datasets and Workloads

| Dataset | Purpose | Required reproducibility metadata |
|---|---|---|
| Small authored enterprise ontology | Known entailments, inconsistency and competency questions | Reviewed gold answers; no synthetic evidence treated as customer data |
| W3C RDF/SPARQL/SHACL and OWL profile tests | Syntax/semantics and supported feature conformance | Exact suite revision, license, expected outcomes and exclusions |
| LUBM/BSBM or qualified equivalent | Structured query/reasoning comparison | Exact generator/version/license, seeds, scale and inference mode |
| WatDiv or qualified diverse graph workload | Query selectivity, path/shape diversity | Generator artifacts, skew and query mix |
| Synthetic enterprise source/ACL corpus | Jira/wiki/code/incident/document joins and revocation | Per-source fixtures, tenant collisions, expected ACLs and delete truth |
| Mapping corpus | CSV/SQL/JSON/XML, nulls, joins and duplicate rates | Mapping revision, source dump, expected RDF and loss ledger |
| Labelled multimodal corpus | OCR, entity linking, diagram topology and facts | Licensed inputs, human annotation protocol and domain/language splits |

Benchmark names are candidate datasets, not downloaded/approved assets. Verify their licenses and releases before acquisition. Keep customer corpora inside authorized boundaries.

Measure p50/p95/p99, throughput, successful/failed/cancelled counts, timeouts, CPU, peak RSS, disk/GPU bytes, index/inference amplification, projection lag, source cost, cache state and restore time. Report both latency and correctness; fast wrong answers fail. Include cold/warm phases, concurrency ramps, skew, updates/deletes, stale mappings, source throttling and crash/restart. Do not benchmark Ontop by repeatedly invoking its setup-heavy query CLI.

Protocol: pin hardware/OS/runtime/engine/config/dataset; verify expected answers; warm according to the published procedure; run at least three repeated measured trials with a fixed workload and seeded generation; retain every trial and failure; report variability and enough observations for quantiles. Competitive comparisons require equivalent semantics, authorization, replication, durability and paid features, with vendor benchmark/publication terms reviewed.

### Selected Initial Quality Gates

These are explicit engineering targets selected under the owner's delegated design authority, not observed product accuracy. Store them in replaceable task/domain/language manifests; tightening or relaxing a gate requires a recorded review, not an agent silently changing expected results.

| Task | Initial gate on the approved held-out corpus | Important boundary |
|---|---|---|
| Supported structured-diagram and RDF term round trip | 100% expected term/edge/axiom fidelity for the declared supported subset | Unsupported constructs are a separate failing/loss outcome, never omitted from the denominator |
| Reviewed entity/fact linking | Precision >=0.99 and recall >=0.80 on the configured domain | High-impact automatic merges remain disabled; confidence calibration and NIL behavior also tested |
| Grounded answer clauses | Evidence precision >=0.98; evidence coverage >=0.95; unanswerable-case abstention >=0.95 | Any observed unauthorized disclosure fails the safety gate irrespective of accuracy |
| Clean printed OCR | Character error rate <=0.05 on the declared language/document stratum | Handwriting, degraded scans and new scripts require separate profiles |
| Clean-speech transcription | Word error rate <=0.15 on the declared language/acoustic stratum | Noisy/multispeaker/technical speech requires separate evaluation, not assumed parity |
| Visual diagram candidate extraction | Relation precision >=0.95 and recall >=0.85 | Human review required before semantic publication |

Start with at least 200 independently annotated items per enabled AI task, including at least 50 items in each release-critical domain/language stratum; enlarge when strata or statistical uncertainty require it. Include negative/unanswerable/adversarial cases, two-reviewer adjudication for disagreements and uncertainty intervals. Point estimates on one corpus do not establish a universal quality guarantee. A task that fails the selected gate stays unqualified or is explicitly restricted; it is not replaced with fake provider output.

### QA Layers

Unit tests cover syntax, schemas, profile selection, budgets and reducers. Property/fuzz tests cover term round trips, Unicode, blank nodes, hostile formats and connector cursors. Differential tests compare independent semantic engines on a declared intersection. Integration tests use real stores, IdP and licensed vendor sandboxes. Workflow tests use the browser against real APIs with persistence/read-back; mocks are a separate category. Chaos tests interrupt writes, publication, projection and restore. Manual reviews qualify keyboard/assistive technology, usability, security and legal obligations.

Every release gate needs raw results plus environment/source/artifact identity. A test that is skipped, xfailed, mocked at the integration boundary, stale, nondeterministic without recorded seed, or run against another backend cannot qualify the corresponding requirement. Code files, screenshots, registry markers and test names alone are never completion evidence.

## 15. Observability, Delivery and Recovery

Use OpenTelemetry/structured logs/Prometheus-compatible metrics through existing EOIP adapters. Correlate source event -> job -> parser -> semantic run -> publication -> projection -> query/action. Record IDs and hashes, not tokens, raw sensitive content or unredacted prompts. Bound metric cardinality; tenant/source detail belongs in access-controlled logs/traces, not unlimited metric labels.

Required dashboards: acquisition freshness and denied scopes; parser failures/budgets; validation unsupported/timeouts; ontology release health; inference amplification/retraction; job queue/lease age; projection policy/revision lag; model cost/quality; query latency/errors; action pending/compensation; backup/restore observations. Unknown/stale telemetry is not a healthy zero.

CI stages: static checks -> contracts -> unit/fuzz -> independent semantics -> real-backend integration -> security/tenancy -> real browser/accessibility -> migration/restore -> workload/performance -> signed artifact/SBOM/notices -> source-bound evidence verification. Build once and promote the exact digest. Qualify both installed and SaaS profiles; neither one substitutes for the other.

Backup includes canonical graph, control database, ontology packages/import locks, raw references, secrets/KMS recovery procedure, event/outbox state and projection rebuild watermarks. Backups must be encrypted, access controlled, retention-aware and periodically restored into a clean environment. Restore is accepted only after data/query/ACL/revision consistency and measured recovery targets, not after a successful archive command.

## 16. Operational Playbooks and Support

| Incident | First containment | Recovery and proof |
|---|---|---|
| Cross-tenant or source-ACL leak | Disable affected reads/actions, preserve restricted audit and revoke sessions/keys as appropriate | Repair policy/projection, rotate compromised material, demonstrate adversarial non-disclosure before reopening |
| Source credential compromise | Pause source, revoke credential, block egress and affected actions | Replace least-privilege secret, reconcile source ACL/content changes, resume from verified checkpoint |
| Poisoned ontology/model proposal | Freeze publication/affected derived graphs and model runs | Restore approved revision, retract/rebuild dependent facts, rerun gold corpus and review impact |
| Parser exploit or decompression spike | Quarantine payload, terminate worker and isolate plugin | Reproduce safely in sandbox, patch, reprocess unaffected items and retain explicit failed status |
| Query overload/OOM | Enforce budgets/cancel, shed load without bypassing authorization | Identify plan/skew, tune or partition from measurements, repeat workload and error checks |
| Stuck/duplicate jobs | Pause claims, inspect leases and publication IDs | Reconcile durable intent/outbox, replay idempotently, prove one published effect and correct cursor |
| Index/policy lag | Deny unsafe stale results; expose affected projection status | Rebuild from authoritative data/policy epoch, compare counts and ACL corpus before serving |
| Regional/store loss | Fence writes, declare recovery profile and select verified backup/watermark | Restore all authoritative state, rebuild projections, measure RPO/RTO and business invariants |
| Failed upgrade | Stop rollout and preserve compatible prior routing | Restore tested snapshot/config plus forward events, verify schema/API/policy compatibility |

Scaling playbook: observe bottleneck -> confirm correctness/lag -> select scale lever -> capacity/load test -> staged rollout -> rollback on invariant or SLO breach. Upgrade playbook: signed manifest -> compatibility/dry-run -> backup/restore rehearsal -> canary -> monitored promotion -> retained rollback. No production action should be performed merely because this document contains a playbook.

Proposed support tiers: developer/community documentation and best-effort support without SLA; standard business-hours support with agreed response targets; enterprise 24x7 critical-incident escalation only when staffing and contracts support it. Suggested initial response objectives are P1 1 hour, P2 4 business hours, P3 2 business days, subject to a signed service schedule; response is not resolution.

Proposed availability metric: successful eligible requests / all eligible requests over the calendar month, with explicit endpoint set, location, maintenance/exclusion policy and independent observations. A 99.9% engineering objective is not an automatic contract promise. Customer-installed support must define responsibility for infrastructure, connectivity, upgrades and recovery. Service credits, liability, governing law and data-processing terms require counsel and commercial approval.

## 17. Roadmap, Capacity and Cost Model

Recommended sequence has dependency gates, not a promised calendar. Estimates are initial planning ranges for the complete programme, not a price quote or measured team velocity. AI agents accelerate some coding; they do not remove architecture, security, domain stewardship, vendor access or manual qualification work.

| Stage | Work | Initial person-week allocation | Exit gate |
|---|---|---|---|
| M0 | Decisions, current capability inventory and release ledger | 8 | Approved profiles/contracts and reproducible baseline |
| M1 | Principal/policy, module/plugin boundaries and durable control plane | 24 | Real two-tenant isolation and worker recovery |
| M2 | Source/event factory and initial certified connectors | 40 | Push/pull/ACL/delete/replay journey |
| M3 | All named source families and protocol SDK certification | 60 | Every declared named source has qualification or explicit blocked state |
| M4 | Safe multimodal/diagram ingestion | 45 | Licensed corpus, source evidence and bounded failure |
| M5 | RDF/mapping/reasoning/validation engines | 40 | Independent semantic correctness and transactional publication |
| M6 | Ontology/vocabulary lifecycle, identity and migration | 50 | Approved version release and reversible identity changes |
| M7 | Query/OBDA/catalog/context projections | 35 | Correct scoped queries and freshness/rebuild proof |
| M8 | Real retrieval/AI/actions/simulation boundaries | 40 | Evidence/egress/action/uncertainty acceptance |
| M9 | Complete modular accessible GUI and customization | 30 | Real end-to-end user tasks and manual AT |
| M10 | Performance, HA/restore, supply chain and both deployment modes | 35 | P1 then P2 qualification against built artifacts |
| M11 | Independent acceptance, support and rollout | 25 | All required clauses accepted; no critical open defects |

Baseline sum: 432 person-weeks; planning uncertainty range 350-700 until M0/M2 recalibrate. This is an analyst estimate, not evidence of actual staffing or an approved spend. With 8 staffed FTE at 70% delivery availability, the range is approximately 63-125 working weeks before critical-path/vendor constraints; do not interpret this as a guaranteed delivery date. A solo engineer must narrow the release scope or accept a much longer horizon while keeping deferred items open.

Cost formula, not a filled quotation:

```text
engineering = sum(person_weeks_by_role * loaded_weekly_rate_by_role)
runtime = compute_hours * measured_hourly_cost
        + retained_GiB_months * storage_rate
        + requests_or_tokens_or_GPU_hours * provider_rate
        + backup + network + observability + commercial_engine/support
programme_total = engineering + runtime + security/legal/accessibility reviews
                + licensed datasets/vendor sandboxes + contingency
```

Keep currency, location, staffing rates, provider quotes, customer environments and contingency as named configurable inputs. Sensitivity cases must vary staff availability, data volume, retention, model usage, inference amplification and source-specific complexity. Do not claim a dollar budget without those inputs.

Risk register: unsupported standards/profile scope; source API/ACL ambiguity; Fortuna/API Portal identity unknown; semantic-to-LPG loss; licensing/OEM terms; vendor test access; inconsistent multi-store publication; cross-tenant inference leakage; deletion versus immutable history; archive/media exploits; model quality/egress; graph/browser scale; actual team capacity. Assign owners and mitigations through CRA-001 rather than hiding risks as assumptions.

## 18. Ecosystem and Deliverable Acceptance

Publish versioned Python/TypeScript SDKs from the actual contract, connector/parser/reasoner plugin templates, conformance fixtures, compatibility tables, migration guides and examples using synthetic or licensed data. Separate stable public APIs from internal endpoints. Support contract deprecation windows and signed marketplace/plugin packages; do not allow arbitrary uploaded Python/JavaScript to execute in the main process.

Community strategy: publish safe interoperability specifications and selected SDK/examples where ownership permits; maintain a security disclosure channel, issue templates, reproducible bug bundles and contribution terms. A proprietary core can coexist with open interface tooling under explicitly chosen separate terms. Do not publish customer ontologies, internal prompts, access policies or licensed corpus data for community growth.

| Requested deliverable | Location | Sign-off condition / current limitation |
|---|---|---|
| 1. Executive summaries and verdict | Sections 1 and C01-C55 | Public desk briefs supplied; hands-on product validation remains open |
| 2. Technical dossier | Sections 6, 8, 11 | Architecture reconstruction supplied; closed-source internals explicitly unknown |
| 3. Markdown and CSV matrix | Section 5 and CSV | All 22 dimensions represented; ND values are unresolved, not completed scoring |
| 4. Gap backlog | Sections 3/7; CRAr.md | Each gap has implementation and behavioral closure criteria |
| 5. Designs/API/schema/UX | Sections 8-11; CRAr.md | Proposed designs; API fragments are not deployed routes |
| 6. Migration/integration | Section 12; CRA-034 | Strategy supplied; migration CLI and rollback exercise remain development |
| 7. Security/legal/compliance | Section 13 | Threats and review gates supplied; not legal/compliance certification |
| 8. Performance plan | Sections 4/14; CRA-036 | Workloads/targets defined; no benchmark results invented |
| 9. Observability/ops | Sections 15-16 | Required telemetry/runbooks defined; operational exercises pending |
| 10. QA plan | Section 14; CRA-037 | Independent and real-integration evidence required |
| 11. Roadmap/cost | Section 17 | Initial capacity estimate and parametric cost; rates/staff/vendor inputs unresolved |
| 12. Playbooks | Section 16 | Draft procedures supplied; operator rehearsal required |
| 13. Support/SLA | Section 16; CRA-038 | Proposed targets only; staffing/legal execution not assumed |
| 14. Ecosystem strategy | This section; CRA-039 | SDK/plugin and contribution strategy defined, not launched |
| 15. Cons-to-pros | INV-01..55 and section 7 | Every limitation asserted here mapped; hypotheses labelled |
| 16. Appendices/reproduction | Section 19 and source links | Input coverage and commands supplied; external product evaluation remains open |

## 19. Reproduction, Standards and Remaining Research

### Real Local Probe

Run from the repository root in PowerShell. This reproduces the inspected defect; it is not a desired passing acceptance test and performs no external writes.

```powershell
$env:PYTHONPATH='.;packages'
python -c "from types import SimpleNamespace; from eoip.ontology.shacl_validator import SHACLValidator, SHACLShape; from eoip.ontology.rdf import OWLReasoner; v=SHACLValidator(); v.shapes={}; v.register_shape(SHACLShape(shape_id='count',target_class='Service',min_counts={'name':2},max_counts={'tag':1})); s=SimpleNamespace(find_vertices=lambda:[{'label':'Service','canonical_id':'urn:test:a','properties':{'name':'only-one','tag':['a','b']}}]); print(v.validate(s).to_dict()); print(v._check_datatype('text','unsupported_type')); print(OWLReasoner().is_subclass_of('urn:example:A','urn:example:a'))"
```

Observed: zero violations/conforms true; unknown datatype true; case-distinct subclass true. After proper remediation, invalid cardinalities must be rejected, unsupported datatypes must be explicit errors, and the distinct identifiers must not be equated without an axiom. Test each separately to avoid a false pass caused by another failure.

### Example External Qualification Commands

These are **not run here**, require approved pinned tools and input files, and must run with network restrictions. They show the command shape, not an existing EOIP harness.

```powershell
pyshacl -s shapes.ttl -f turtle data.ttl
robot reason --reasoner ELK --input ontology.owl --output reasoned.owl
robot report --input ontology.owl --output report.tsv
```

Expected outcomes depend on the fixture and profile: pySHACL distinguishes conformant/nonconformant/runtime/unsupported outcomes; ROBOT must fail on intended incoherence or release-blocking reports. Pin the reasoner and check its license. Never treat command exit zero without artifact/coverage inspection as full acceptance.

### Small Independent Semantic Fixture

The following are source examples to materialize as separate reviewed fixture files during CRA-016/019/020 implementation. They were not submitted to an external engine in this task. They do not substitute for W3C suites or a realistic enterprise ontology.

`ontology.ttl`:

```turtle
@prefix ex: <urn:example:> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:Ontology a owl:Ontology .
ex:Service a owl:Class .
ex:Database a owl:Class ; rdfs:subClassOf ex:Service .
ex:Person a owl:Class ; owl:disjointWith ex:Service .
ex:name a owl:DatatypeProperty ; rdfs:range xsd:string .
ex:dependsOn a owl:ObjectProperty, owl:TransitiveProperty .
```

`data.ttl`:

```turtle
@prefix ex: <urn:example:> .
ex:Orders a ex:Service ; ex:name "Orders" ; ex:dependsOn ex:Ledger .
ex:Ledger a ex:Database ; ex:name "Ledger" ; ex:dependsOn ex:Cache .
ex:Cache a ex:Service ; ex:name "Cache" .
```

`shapes.ttl`:

```turtle
@prefix ex: <urn:example:> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:ServiceShape a sh:NodeShape ;
  sh:targetClass ex:Service ;
  sh:property [ sh:path ex:name ; sh:datatype xsd:string ;
                sh:minCount 1 ; sh:maxCount 1 ] .
```

Expected under the declared RDFS/transitivity reasoning profile: `ex:Ledger a ex:Service` and `ex:Orders ex:dependsOn ex:Cache`. The data conform to the shape. Independently add a second distinct name to Orders: maxCount must fail. Remove its name: minCount must fail. Add `ex:Orders a ex:Person`: the OWL ontology/data combination becomes inconsistent under the declared disjointness semantics, which is a separate test from shape validation. `urn:example:A` and `urn:example:a` must retain distinct RDF term identity; OWL's lack of a unique-name assumption does not license silently lowercasing or asserting equality. [RDF concepts](https://www.w3.org/TR/rdf11-concepts/), [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/).

### Normative and Primary References

The selected baseline is RDF 1.1/JSON-LD 1.1/SPARQL 1.1/OWL 2/SHACL 2017 for interoperability. Newer standards/drafts or vendor extensions require an explicit profile/version decision, not an implicit upgrade. OWL reasoning and SHACL validation are different semantics and must have separate results. [OWL 2 profiles](https://www.w3.org/TR/owl2-profiles/), [SHACL](https://www.w3.org/TR/shacl/), [SPARQL 1.1 family](https://www.w3.org/TR/sparql11-overview/).

Each tool dossier links its supporting maintainer/vendor sources. Additional required research before procurement/release: exact artifact/license snapshots; current release support/lifecycle; per-edition security/DR/accessibility; real benchmark permission and results; API/version/scopes for every connector; model/dataset terms; vendor quote/contract; operator and domain-steward review. Unavailable pages and contradictory documentation remain unresolved evidence gaps, not negative findings about a product.

Completion statement: the research and proposed engineering requirements are delivered as planning artifacts. The product is not declared complete, fully standards-conformant, universally connected, legally cleared or production-qualified by this document.

### Document Validation Performed

Validated 55 unique dossier/matrix IDs, all 22 CSV dimension columns, numeric-or-ND score values, 40 requirement sections and 210 numbered acceptance clauses. Local document links, requirement references and balanced fenced blocks passed structural checks. The three JSON examples and one OpenAPI YAML fragment parsed successfully; this is serialization validation, not complete OpenAPI semantic validation or endpoint execution. The roadmap allocation independently sums to 432 person-weeks.

The three Turtle examples were identified but not parser/reasoner-qualified: RDFLib is not installed in the inspected Python environment. No dependency was installed merely to make a research document appear verified. The semantic example outcomes remain specified expectations, with independent engine execution required by CRAr.md. The targeted local validator/reasoner defect probe did execute as described above. No application files were changed or whole-application regression/competitor benchmark claimed in this documentation task.
