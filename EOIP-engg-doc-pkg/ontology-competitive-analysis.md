# EOIP / KnowGridFlow — Ontology Platform Competitive Analysis & Inversion Blueprint

> **Classification**: Internal — Strategy & Engineering
> **Date**: 2026-10-16
> **Authors**: Enterprise Architecture / Principal KG Engineering
> **Companion artifacts**: `ontology-comparison-matrix.csv`, `ontology-analysis-dashboard.html`
> **Audience**: CTO, Architect, Lead Developer, Lead AI Engineer, Legal, Licensing

---

## 0. Executive Summary

### 0.1 The one-paragraph verdict

EOIP is **not** an inferior triplestore. It is a different species of system that has accidentally
grown a thin, non-standard semantic veneer. Measured against the W3C-native vendors
(GraphDB, Stardog, Jena, TopBraid), EOIP scores poorly on *standards compliance, formal
reasoning, and SPARQL* — and it will keep scoring poorly, because those are not the parts of
the problem EOIP actually solves. Measured against the same vendors on *enterprise source
coverage, ontology-as-code lifecycle, multi-format ingestion, and agentic grounding*, EOIP is
ahead of every tool in this study except Palantir Foundry — and ahead of Palantir on openness
and cost. **The strategy is therefore not "catch up on RDF." It is "become standards-compatible
at the boundary while widening the moat in the middle."**

### 0.2 The five findings that should change decisions

| # | Finding | Evidence | Consequence |
|---|---|---|---|
| **F1** | **EOIP cannot read any ontology produced by the outside world.** No `rdflib`, no `pySHACL`, no `owlready2` in the dependency tree. No Turtle / RDF-XML / N-Triples / OWL-XML parser exists. | `grep rdflib\|pyshacl\|owlready` across deps → zero hits | FIBO, gist, schema.org, SNOMED-CT, SKOS thesauri, and every customer's existing ontology are **unimportable**. This is the single largest commercial blocker. |
| **F2** | **The OWL reasoner is a demo, not a reasoner.** `OWLReasoner._bootstrap_core_axioms()` hardcodes `Microservice`, `Engineer`, `RelationalDatabase`. It does transitive subsumption + 2-step property chains only. No tableau, no consistency check, no unsatisfiable-class detection, no ABox realization. | `packages/eoip/ontology/rdf.py:598-700` | Any claim of "OWL reasoning" fails a technical buyer's first 10-minute probe. Reputational risk exceeds the functional gap. |
| **F3** | **SHACL output is SHACL-shaped, not SHACL.** `export_shacl_shapes()` emits `sh:NodeShape` / `sh:targetClass` correctly, but mixes in `eoip:allowedEndpointPairs` and `eoip:optionalProperty` and omits `sh:datatype`, `sh:nodeKind`, `sh:maxCount`, `sh:pattern`. A conformant SHACL processor would validate the document and find almost no constraints. | `packages/eoip/ontology/rdf.py:369-425` | Interop claims are not defensible. Fix is small (≈2 weeks) and high-leverage. |
| **F4** | **Ontology GitOps is genuinely best-in-class and nobody is marketing it.** 793 lines implementing branches, PRs with review gates, semantic diff, impact analysis, migration-script generation, rollback receipts, semver computation, and release packaging. | `packages/eoip/ontology/gitops.py` | **No competitor has this.** TopBraid EDG has workflow-with-approvals but not git semantics; TerminusDB has git semantics on *data* but not governed ontology change management; Protégé has revision history only. This is the headline differentiator. |
| **F5** | **Connector reach exceeds every ontology vendor in the study.** 38 connector modules + a 1,135-line universal `ConnectionFactory` with 8 application categories, plus a multi-format parser covering Office / media / engineering diagrams / archives. | `packages/eoip/connectors/` (38 files), `packages/eoip/fileparse/` | Ontology vendors assume data arrives. EOIP *goes and gets it.* Combined with F4, this is the defensible category position. |

### 0.3 Top 5 opportunities, ranked by (impact ÷ effort)

1. **ONT-001 — W3C serialization bridge** (`rdflib` adapter). Unlocks import of every external ontology. ~3 weeks. **Highest ROI in the entire backlog.**
2. **ONT-004 — Conformant SHACL via `pySHACL`.** Turns an interop liability into a checkbox. ~2 weeks.
3. **ONT-012 — Market the GitOps layer as "Ontology-as-Code".** Zero engineering. Pure positioning. Category-defining.
4. **ONT-002 — SPARQL 1.1 endpoint** (translate to the existing property-graph store). Enables BI tools, federation, and every RFP checklist. ~6 weeks.
5. **ONT-007 — Pluggable external reasoner** (HermiT/ELK via subprocess or a Jena/GraphDB sidecar) instead of growing the hand-rolled one. ~4 weeks, removes F2 permanently.

### 0.4 What to explicitly *not* build

| Don't build | Why | Do instead |
|---|---|---|
| A native RDF quad store | GraphDB/Jena/Virtuoso represent 15+ years of engineering. You will not beat them and the market does not reward a 12th triplestore. | Pluggable backend adapter (ONT-003) |
| A DL tableau reasoner | HermiT, ELK, Openllet are mature, free, and correct. Writing one is a PhD, not a sprint. | Shell out / sidecar (ONT-007) |
| A visual ontology editor to rival Protégé | 25 years of accumulated UX. | `studio.py` for *authoring the EOIP manifest only*; round-trip to Protégé via OWL export |
| Multilingual thesaurus management (VocBench/Graphite class) | Deep, niche, low overlap with your buyer | SKOS import/export only (`skos.py` already covers the model) |

---

## 1. Input Context — Measured Baseline

This section is **measured from the repository**, not asserted. Every claim has a file path.

### 1.1 Architecture & tech stack

| Layer | Implementation | Location | Scale |
|---|---|---|---|
| Language | Python 3.12+ (`from __future__ import annotations`, PEP 604 unions) | — | 587 `.py` files under `packages/` |
| API | FastAPI + Pydantic v2 | `packages/eoip/platform_router.py` | 133+ paths |
| Graph store | Pluggable: in-memory, HugeGraph, Neptune, Neo4j | `packages/eoip/graph/backends.py` | Property-graph (LPG) model |
| Graph model | Labeled Property Graph with manifest-governed vertex/edge labels | `packages/eoip/ontology/manifest.py` (505 LOC) | `VERTEX_LABELS`, `EDGE_LABELS` |
| Query | JQLite, JSONPath, Lucene, taxonomy DSL | `packages/eoip/qlang/` | **No SPARQL** |
| Semantic layer | Hand-rolled JSON-LD, pseudo-SHACL, toy OWL | `packages/eoip/ontology/` | 14 modules, ~3,400 LOC |
| Ingestion | 38 connectors + universal factory | `packages/eoip/connectors/` | 8 app categories |
| File parsing | Office, media, diagrams, archives, text | `packages/eoip/fileparse/` | 13 modules |
| Cognitive | Brain OS, 21 discipline engines, 14 control loops | `packages/eoip/brain/`, `intelligence_eng/` | — |

### 1.2 Ontology package inventory (the subject of this analysis)

| Module | LOC | What it genuinely does | Standards-grade? |
|---|---:|---|---|
| `gitops.py` | 793 | Branch, commit, PR, review, merge, semantic diff, impact analysis, migration generation, rollback, semver, release packaging | **Exceeds market** (no standard exists) |
| `manifest.py` | 505 | Vertex/edge label registry, endpoint validity, domain mapping | Proprietary (fine) |
| `rdf.py` | 700 | JSON-LD export/import, property-graph round-trip, SHACL-shaped export, `OWLReasoner` | **No** — see F1/F2/F3 |
| `skos.py` | 450 | Concept, ConceptScheme, Collection, mappings, integrity issues, label conflicts | Model is faithful; **no SKOS RDF I/O** |
| `gitops_router.py` | 376 | 20+ FastAPI endpoints over the GitOps workflow | Good |
| `packs.py` | 326 | Domain pack load/validate/conflict detection | Proprietary (good pattern) |
| `domain_pack_manager.py` | 323 | Pack lifecycle | Proprietary |
| `shacl_validator.py` | 194 | Custom `SHACLValidator` with severity/violation/report types | **No** — not SHACL Core |
| `studio.py` | 177 | Visual project model (classes, relations, properties) | Early |
| `drift.py` | 152 | Ontology drift detection + evolution proposals | **Differentiator** |
| `stewardship.py` | 151 | Governance states, branches, steward assignment | Good |
| `industry_templates.py` | 139 | Prebuilt industry ontology templates | Good |
| `embedding_drift.py` | 134 | Cosine drift over label-grouped vectors | **Differentiator** |
| `schema_gen.py` | 127 | JSON Schema / OpenAPI / form-spec generation from ontology | **Differentiator** |

### 1.3 Declared constraints (assumed — confirm before sign-off)

| Constraint | Assumed value | Confirm with |
|---|---|---|
| Target scale | 100M nodes / ~500M triple-equivalents, 20k classes, 150k axioms | CTO (TASK-CTO-002) |
| Latency | p95 < 20ms simple lookup; < 1s multi-hop | Architect (TASK-ARCH-015) |
| Deployment | Kubernetes, multi-region, air-gap capable | TASK-CTO-004 |
| Licensing | **Must avoid GPL/AGPL contamination in the distributed core** | Legal (TASK-LEGAL-004) |
| Team | 1 Tech Lead, small dev team + AI coding agents | TASK-DM-013 |
| Horizon | 3 quarters to standards parity | TASK-DM-001 |

> ⚠ **Licensing flag for Legal**: Protégé is BSD but **WebProtégé is AGPL**. Neo4j Community is **GPLv3**. Virtuoso OSE is **GPLv2**. `rdflib` and `pySHACL` are BSD/Apache — safe. HermiT is LGPL; ELK is Apache 2.0 — **prefer ELK**. See §8.

---

## 2. Scoring Rubric

Scores are 1–5 against the 22 dimensions requested. Scoring is **relative to enterprise
production readiness**, not academic completeness.

| Score | Meaning |
|---|---|
| 5 | Best-in-class; defines the state of the art |
| 4 | Production-grade, complete, minor gaps |
| 3 | Usable, meaningful gaps, workarounds required |
| 2 | Partial / demo-grade; fails under enterprise load or scrutiny |
| 1 | Absent or non-functional |

### 2.1 EOIP self-assessment (honest baseline)

| # | Dimension | Score | Rationale |
|---|---|:---:|---|
| 1 | Core Functionality | **4** | Full ontology lifecycle incl. packs, templates, stewardship. Missing: external import. |
| 2 | Architecture & Internals | **4** | Clean modular engines, singleton pattern, pluggable graph backends. Import chain slow (60–120s collection). |
| 3 | Data Model & Expressivity | **2** | LPG + manifest. No RDF model, no OWL profiles, no conformant SHACL, no SPARQL. |
| 4 | Reasoning & Inference | **2** | Transitive subsumption + 2-step chains, hardcoded axioms. No DL. |
| 5 | Interoperability & Standards | **2** | JSON-LD export only, non-round-trippable with standard tools. |
| 6 | Performance & Scalability | **3** | Pluggable to Neptune/Neo4j/HugeGraph, but in-memory default; no published benchmarks. |
| 7 | Extensibility | **5** | Domain packs, plugin system, connector factory, 21 discipline engines. |
| 8 | Security & Governance | **4** | RBAC, audit, provenance, tenancy, compliance modules all present. |
| 9 | Usability & Tooling | **3** | 90+ React components, studio early-stage, no Protégé-class editor. |
| 10 | Deployment & Ops | **3** | K8s-ready; DR/multi-region designed not proven. |
| 11 | Licensing & Cost | **5** | Own IP, no vendor royalties, 4-tier licensing already modeled. |
| 12 | Known Limitations | **2** | F1–F3 above are material. |
| 13 | Ecosystem & Community | **1** | Pre-launch. No community, no third-party integrations. |
| 14 | Migration Effort (into EOIP) | **1** | **Cannot ingest external ontologies at all.** Worst score in the study. |
| 15 | Differentiators | **5** | GitOps ontology, drift detection, 38 connectors, agentic grounding, schema-gen. |
| 16 | Observability | **4** | Prometheus/OTel present; alerting rules absent. |
| 17 | CI/CD & Testing | **3** | 239 test files; slow collection; some pre-existing failures. |
| 18 | Backup & DR | **3** | WAL exists; no automated DR drills. |
| 19 | Legal/IP Risk | **3** | Patents unfiled (TASK-LEGAL-001); dependency audit pending. |
| 20 | Accessibility & i18n | **2** | 146 ARIA attributes, **zero i18n**. |
| 21 | Support & SLAs | **1** | None defined. |
| 22 | KPIs | **2** | Targets drafted, not instrumented. |
| | **Weighted mean** | **≈2.9** | Strong extremes: 5s and 1s, few 3s. |

**Read the shape, not the mean.** EOIP's profile is bimodal — world-class at 7/11/15, bottom-of-market at 13/14/21. That is the profile of a *pre-launch platform with a real moat*, not a weak product.

---

## 3. Category Analysis & Reconstruction

### 3.1 Category 1 — Authoring & Conceptual Modeling

| Tool | License | Core(1) | Expressivity(3) | Reasoning(4) | Interop(5) | Usability(9) | Ecosystem(13) | Threat to EOIP |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Protégé 5.6 / WebProtégé** | BSD / **AGPL** | 5 | 5 | 5 | 5 | 4 | 5 | **Low** — different job |
| TopBraid Composer | Commercial | 4 | 5 | 4 | 5 | 4 | 3 | Low |
| OntoStudio | Commercial | 3 | 4 | 4 | 3 | 3 | 1 | None (declining) |
| Fluent Editor (CNL) | Commercial | 3 | 4 | 4 | 3 | 4 | 1 | **Idea worth stealing** |
| Ontosphere | Open Source | 3 | 4 | 3 | 4 | 4 | 2 | **MCP hook worth stealing** |
| Graphologi | Commercial | 4 | 4 | 3 | 4 | 5 | 2 | Low |
| Chowlk / OnToology | Open Source | 3 | 3 | 2 | 4 | 3 | 2 | **Overlaps GitOps — study closely** |

**Architecture reconstruction — Protégé.** Java/OSGi plugin host over the **OWL API** object model.
The OWL API is the real asset: a complete in-memory axiom model with visitor-based traversal, plus
pluggable `OWLReasoner` implementations (HermiT tableau, ELK for EL++, FaCT++, Openllet).
Classification runs the reasoner over the TBox, caches a `Node<OWLClass>` subsumption hierarchy,
and surfaces unsatisfiable classes as subclasses of `owl:Nothing`. WebProtégé replaces the local
file with an event-sourced change log (`OWLOntologyChange` records) over MongoDB, giving revision
diffs and threaded review.

**What EOIP should take.** Not the editor — the **axiom model and the reasoner interface**. EOIP's
`OWLReasoner` should become a *port*, with adapters to ELK (Apache 2.0) and the hand-rolled fallback.
Protégé is also the right **round-trip target**: if EOIP exports valid OWL, every ontologist on earth
can open it. That is worth more than any editor EOIP could build.

**Cons to invert.**
- *Protégé is single-user desktop-first; WebProtégé is AGPL and heavy.* → EOIP offers **governed multi-user ontology change as a service** with git semantics and no AGPL.
- *No connection to live enterprise data.* Protégé models the world in the abstract. → EOIP **induces** the ontology from 38 connected systems (`moonshot/ontology_induction.py` already exists).
- *Chowlk/OnToology stop at linting + docs on commit.* → EOIP's `gitops.py` already does impact analysis, migration generation, and rollback — a superset. **Publish a comparison table.**

---

### 3.2 Category 2 — Governance, Taxonomy & Vocabulary

| Tool | License | Governance(8) | Workflow | Taxonomy depth | Interop(5) | Threat |
|---|---|:---:|:---:|:---:|:---:|---|
| **TopBraid EDG** | Commercial | 5 | 5 | 4 | 5 | **High — closest competitor** |
| VocBench 3 | Open Source | 4 | 4 | 5 | 5 | Low |
| PoolParty (Graphwise) | Commercial | 4 | 4 | 5 | 4 | **Medium-High** |
| Progress Semaphore | Commercial | 4 | 3 | 4 | 3 | Medium |
| Synaptica Graphite | Commercial | 3 | 3 | 5 | 4 | Low |
| SciBite CenTree/TERMite | Commercial | 4 | 3 | 5 (life-sci) | 4 | Low (vertical) |
| Data Harmony | Commercial | 3 | 3 | 4 | 3 | Low |
| Semantic Arts **gist** | CC-BY (ontology) | — | — | — | 5 | **Adopt, don't compete** |
| Reltio Ontology Builder | Commercial | 4 | 3 | 2 | 3 | Low |

**Architecture reconstruction — TopBraid EDG.** The design thesis is *SHACL as the universal
metamodel*. Everything — data models, taxonomies, reference data, glossaries — is a SHACL shape
graph stored in a Jena-backed quad store. Because shapes are data, EDG derives UI forms, validation,
and **auto-generated GraphQL APIs** from the same shape definitions. Workflow is a state machine
over named graphs: each change set is an isolated graph, merged to production on approval, with
impact analysis computed by SPARQL over the diff.

**This is the single most strategically important system in the study**, because EOIP has
independently reinvented two-thirds of it — and gone further on version control.

| Capability | TopBraid EDG | EOIP today | Verdict |
|---|---|---|---|
| Shape-driven UI/API generation | ✅ GraphQL from SHACL | ✅ `schema_gen.py` → JSON Schema + OpenAPI + form spec | **Parity** |
| Change workflow with approval gates | ✅ State machine | ✅ `OntologyGitOpsWorkflow` + `PullRequestStatus` | **EOIP ahead** (git semantics) |
| Impact analysis | ✅ SPARQL over diff | ✅ `run_ontology_impact_analysis` | Parity |
| Rollback | ⚠️ Restore prior graph | ✅ `RollbackReceipt` + `OntologyVersionStore` | **EOIP ahead** (auditable receipts) |
| Semantic versioning | ❌ Manual | ✅ `compute_next_semver(diff)` | **EOIP uniquely ahead** |
| Migration script generation | ❌ | ✅ `generate_ontology_migration_script` | **EOIP uniquely ahead** |
| Standards substrate | ✅ Full SHACL/SPARQL/RDF | ❌ Proprietary manifest | **EDG far ahead** |
| Enterprise source connectors | ⚠️ Limited | ✅ 38 + factory | **EOIP far ahead** |

**The inversion is already 70% built.** Close the standards gap (ONT-001/004) and EOIP is
strictly superior to EDG for a modern buyer, at a fraction of the price.

**gist — adopt it.** Semantic Arts' `gist` is a ~200-concept minimalist upper ontology under a
permissive license. It solves the "what are the root classes" problem that every enterprise
ontology project burns a quarter on. **Recommendation: ship `gist` as a first-class domain pack
(`ONT-010`) once ONT-001 lands.** Costs ~1 week; instantly credible with semantic-web buyers.

---

### 3.3 Category 3 — Triplestores & Reasoning Engines

| Tool | License | Expressivity(3) | Reasoning(4) | Perf(6) | Scale ceiling | Deploy(10) | Cost(11) |
|---|---|:---:|:---:|:---:|---|:---:|:---:|
| **GraphDB** (Graphwise) | Commercial / free CE | 5 | 4 (fwd-chaining, OWL2 RL/QL) | 4 | ~10–50B triples | 4 | 3 |
| **Stardog 12.x** | Commercial | 5 | **5** (query-time OWL2 SL + SWRL + proof trees) | 4 | ~10B+ | 4 | 2 |
| AllegroGraph | Commercial | 5 | 5 (Prolog + vectors) | 4 | FedShard clusters | 3 | 2 |
| **Apache Jena** (TDB2/Fuseki) | **Apache 2.0** | 5 | 3 (rule engine) | 3 | ~1B practical | 4 | **5** |
| Virtuoso | **GPLv2** / Commercial | 5 | 3 | 5 | 10B+ | 3 | 4 |
| **Eclipse RDF4J** | **EPL/BSD** | 5 | 3 | 3 | ~500M | 4 | **5** |
| Amazon Neptune | Commercial | 4 | 2 (weak inference) | 4 | 64TB/cluster | 5 | 3 |
| MarkLogic (Progress) | Commercial | 4 | 3 | 4 | PB-scale docs | 3 | 1 |
| TerminusDB 12.x | Apache 2.0* | 3 | 2 | 3 | ~100M | 4 | 5 |
| Neo4j + n10s | **GPLv3** CE | 3 | 2 | 4 | 10B+ nodes | 4 | 3 |

*TerminusDB licensing is reported inconsistently across sources — **Legal must verify before any dependency.**

**Reasoning strategy — the key architectural fork.**

```
                    ┌─────────────────────────────┐
  Forward-chaining  │  Materialize at WRITE time   │  GraphDB, Jena rules
  (materialization) │  + fast deterministic reads  │
                    │  − slow writes, storage bloat│
                    │  − full recompute on TBox Δ  │
                    └─────────────────────────────┘
                    ┌─────────────────────────────┐
  Backward-chaining │  Rewrite at QUERY time       │  Stardog, Ontop
  (query rewriting) │  + instant TBox changes      │
                    │  + no storage cost           │
                    │  − per-query latency cost    │
                    └─────────────────────────────┘
```

**EOIP's position is accidentally correct.** `OWLReasoner.infer_triples()` is forward-chaining, but
`is_subclass_of()` is backward-chaining — a **hybrid**. Formalize this as a deliberate design
(`ONT-008`): materialize cheap, stable inferences (transitivity, inverse, symmetric) at write;
evaluate expensive or volatile ones (property chains over large fan-out, cross-pack rules) at query.
This is defensible IP and a real talking point — *and it maps cleanly onto the existing
`graph_graph/` layer-over-layer engine.*

**Cons to invert.**
- *Triplestores cannot represent two distinct relationships of the same type between the same pair of nodes* without reification bloat (the standard RDF criticism). → **EOIP is natively LPG: edges have identity and properties for free.** Market this as "no reification tax."
- *SPARQL reasoning offers no termination guarantee.* → EOIP's `token_budget/` and control-loop architecture can impose **hard query budgets with graceful degradation** — a guarantee no triplestore offers.
- *Triplestores are weak at traversal* (conceded even by Ontotext). → EOIP is traversal-native (`graph/paths.py`, `algorithms.py`, `community.py`).
- *Every triplestore makes you bring your own data.* → EOIP mines it.

**Backend recommendation (`ONT-003`).** Do not build a store. Extend `graph/backends.py` with an
**RDF backend port** targeting Jena Fuseki (Apache 2.0, zero license risk) as the reference
implementation and GraphDB as the certified commercial option. Customers who already own GraphDB
or Stardog can then point EOIP at it — turning competitors into **distribution channels**.

---

### 3.4 Category 4 — OBDA, Virtualization & Semantic Fabrics

| Tool | License | Virtualization | Mapping std | Perf(6) | Threat |
|---|---|:---:|---|:---:|---|
| **Ontop** | Apache 2.0 | 5 | R2RML / RML | 4 | **Low — adopt the technique** |
| Timbr.ai | Commercial | 4 | SQL views over OWL | 4 | Medium |
| Anzo / AnzoGraph (**Altair**) | Commercial | 5 | Proprietary + RDF | 5 (MPP) | Medium |
| Morph-KGC | Apache 2.0 | — (materializing) | R2RML/RML-star | 4 | Low |
| RMLStreamer / SDM-RDFizer | Open Source | — (streaming) | RML | 4 | **Adopt the pattern** |
| Karma | Open Source | 3 | R2RML + ML | 2 | **Steal the ML mapping idea** |

**Architecture reconstruction — Ontop.** The canonical OBDA pipeline:
1. **Unfold** — rewrite the SPARQL query against R2RML mappings into a relational algebra tree.
2. **Optimize semantically** — use the OWL 2 QL TBox to prune provably-empty branches and collapse
   subsumption into unions; the QL profile is chosen precisely because it is *first-order rewritable*.
3. **Emit native SQL** — push the whole thing to the source DB, which does the work.

No data moves. The TBox is a *query optimizer input*, not a materialization target.

**Why this matters enormously to EOIP.** The user's requirement — "connect to Jira, Confluence,
ServiceNow, Snowflake, GitLab, Splunk… either they push or we crawl" — is **exactly the OBDA
problem**, generalized from SQL to REST. EOIP's `connectors/factory.py` is the transport. What is
missing is the **declarative mapping layer** between a connector's native payload and the ontology.

> **ONT-005 — Connector Mapping Language (CML).** An RML-inspired, YAML-authored declarative mapping
> from connector payload (JSON/XML/CSV/row) → ontology classes, properties, and relations. Today the
> mapping is implicit in each of 38 hand-written connectors; that does not scale to "any enterprise
> system." CML makes a new source a *config file*, not a Python module. **This is the highest-value
> architectural idea in this entire document after ONT-001.**

Sketch:

```yaml
# mappings/jira.cml.yaml
source: jira
version: 1
subject_map:
  template: "eoip:entity/Issue/{key}"
  class: Issue
property_maps:
  - path: $.fields.summary      → title          { datatype: string, required: true }
  - path: $.fields.created      → createdAt      { datatype: dateTime }
  - path: $.fields.status.name  → status         { datatype: string, vocab: skos:IssueStatus }
relation_maps:
  - path: $.fields.assignee.accountId
    predicate: ASSIGNED_TO
    object_template: "eoip:entity/Person/{value}"
    object_class: Person
  - path: $.fields.issuelinks[*].outwardIssue.key
    predicate: DEPENDS_ON
    object_template: "eoip:entity/Issue/{value}"
provenance:
  emit: true          # W3C PROV-O wasDerivedFrom / wasGeneratedBy
  confidence: 1.0
governance:
  classification: internal
  pii_fields: [$.fields.assignee.emailAddress]
```

**Cons to invert.**
- *Ontop requires OWL 2 QL — the weakest profile — and a relational source.* → EOIP's CML targets
  **any connector**, with a hybrid materialize/virtualize decision per source.
- *Karma's ML mapping suggestions never productized.* → EOIP has an AI layer (`extraction/`, `nlp/`,
  `moonshot/ontology_induction.py`). **Auto-suggest CML mappings from sampled payloads** (`ONT-006`).
  This is a genuinely novel, patentable capability.

---

### 3.5 Category 5 — Operational Ontologies & Action Platforms

| Tool | License | Actions/write-back | Agent grounding | Openness | Cost | Threat |
|---|---|:---:|:---:|:---:|:---:|---|
| **Palantir Foundry / AIP** | Commercial | 5 | 5 | **1** | **1** | **HIGHEST — the real competitor** |
| Microsoft Fabric semantic layer | Commercial | 3 | 4 | 2 | 3 | High (bundling) |
| Oracle AI Data Platform | Commercial | 3 | 3 | 2 | 2 | Medium |
| Cosmo Tech | Commercial | 4 (simulation) | 2 | 1 | 2 | Low (vertical) |
| Cinchapi Concourse | Commercial/open-core | 3 | 2 | 3 | 3 | Low |
| Essential Cloud | Commercial | 2 | 1 | 3 | 4 | Low |

**Architecture reconstruction — Palantir Ontology.** Three coupled layers:
1. **Semantic layer** — Object Types, Link Types, Properties. Deliberately *not* RDF; a typed
   object-relational model backed by versioned datasets in Foundry's pipeline system.
2. **Kinetic layer** — **Actions**: typed, parameterized, permissioned functions that write back to
   source systems (ERP/CRM) and mutate object state transactionally. *This is the part competitors miss.*
3. **Dynamic layer** — AIP binds LLM agents to the ontology, so an agent can only perceive what the
   ontology exposes and only act through governed Actions. The ontology **is the agent's safety boundary**.

**This is the architecture EOIP is converging on.** EOIP already has: `agents/` (35 types),
`loops/` (14 control loops), `harness/`, `verification/`, `tools_contract/`, `authz/`, and now
`intelligence_eng/` as meta-orchestrator. **What EOIP lacks is the Action abstraction** — the typed,
governed, auditable write-back primitive.

> **ONT-009 — Governed Action Layer.** Define `OntologyAction`: a typed, permissioned,
> ontology-bound operation with declared preconditions (SHACL), effects (which classes/properties
> mutate), a target connector for write-back, an approval policy keyed to the existing `AutonomyLevel`
> enum, and an immutable audit receipt. This closes the gap to Palantir on the only axis where
> Palantir is genuinely ahead — **and EOIP's 14-level autonomy ladder is a finer-grained safety
> model than anything in AIP.**

**Cons to invert — the Palantir displacement thesis.** Third-party analyses consistently cite four
weaknesses. Each maps to an EOIP design response:

| Palantir con (per third-party analysis) | EOIP inversion | Implementation |
|---|---|---|
| **Proprietary, closed; data and models hard to migrate out** | Open formats end to end: ontology exports as valid OWL/SHACL, graph as JSON-LD/RDF, mappings as portable CML | ONT-001, ONT-004, ONT-005 |
| **TCO reported 3–8× build alternatives; per-seat costs cited in the $100k–$300k range for heavy users** | Self-hostable, 4-tier licensing already modeled, no per-seat cliff; publish a TCO calculator | TASK-LIC-009, TASK-LIC-010 |
| **Months-to-a-year implementations; heavy forward-deployed engineering; manual relationship modeling** | **Ontology induction from connected systems** — mine first, curate second | `moonshot/ontology_induction.py` + ONT-006 |
| **Agent Studio described as basic vs. other agent frameworks** | 35 agent types, 14 control loops, 9 reasoning strategies, verification engine, 64 RAG modes | Already shipped |

> **Positioning line for Marketing (TASK-MKT-002):** *"The operational ontology, without the
> lock-in."* Every artifact EOIP produces — ontology, graph, mappings, actions — is an open,
> portable, standards-based file. That is a claim Palantir structurally cannot make, and it is only
> true once ONT-001 and ONT-004 land. **Do not make the claim before then.**

---

### 3.6 Category 6 — Metadata Catalogs & Context Layers

| Tool | License | Lineage | Glossary | Graph-native | MCP/agent | Threat |
|---|---|:---:|:---:|:---:|:---:|---|
| OpenMetadata | Apache 2.0 | 4 | 4 | 3 | ✅ MCP | **Medium — study the MCP server** |
| data.world | Commercial | 4 | 5 | **5** (RDF-native) | 3 | Medium |
| Collibra | Commercial | 5 | 5 | 2 | 2 | Low (different buyer) |
| Alation | Commercial | 4 | 4 | 2 | 3 | Low |
| OvalEdge | Commercial | 3 | 4 | 3 | 3 | Low |
| DataHub | Apache 2.0 | 4 | 3 | 4 | 2 | Medium |
| Apache Atlas | Apache 2.0 | 4 | 3 | 3 | 1 | Low (Hadoop-era) |

**The convergence to watch.** Catalogs are growing ontologies; ontology tools are growing catalogs;
both are growing MCP servers to feed agents. EOIP sits in the middle and should claim the junction.

> **ONT-011 — MCP Server for the Enterprise Ontology.** Expose the ontology, graph, and governed
> Actions over Model Context Protocol so *any* agent framework (Claude, LangGraph, internal copilots)
> can ground on EOIP. OpenMetadata and Ontosphere both ship this; it is becoming table stakes.
> EOIP already has `tools_contract/` and `sdk/` — this is wiring, not invention. **~2 weeks.**

**Cons to invert.** Catalogs describe data but cannot reason over it; ontology tools reason but
cannot see the enterprise. → EOIP does both, and adds drift detection (`drift.py`,
`embedding_drift.py`) that neither category has: **the ontology notices when reality diverges from it.**

---

### 3.7 Category 7 — Ontology CI/CD & Validation

| Tool | License | Role | EOIP equivalent | Gap |
|---|---|---|---|---|
| **ROBOT** | BSD | CLI build/reason/release pipeline | `gitops.py:main()` CLI | Needs OWL ops (ONT-001) |
| **pySHACL** | Apache 2.0 | Reference Python SHACL validator | `shacl_validator.py` (custom) | **Replace/wrap — ONT-004** |
| TopBraid SHACL API | Apache 2.0 | JVM SHACL | n/a | Not needed (Python stack) |
| **OOPS!** | Open Source | Pitfall/antipattern scanner | ❌ **none** | **ONT-013 — build it** |
| Widoco / LODE | Apache/MIT | HTML ontology docs | `ontology/documentation`? partial | ONT-014 |

> **ONT-013 — Ontology Pitfall Scanner.** OOPS! detects ~40 modeling antipatterns (missing
> domain/range, circular hierarchies, equivalent-class loops, unconnected elements, naming
> inconsistency). EOIP has `drift.py` and `packs.py` conflict detection but no pitfall linting.
> This is a **contained, high-signal addition** that strengthens the Ontology-as-Code story and
> plugs directly into `gitops.py` PR validation as a quality gate.

**This category is where EOIP's moat already lives.** ROBOT + pySHACL + OOPS! + Widoco are four
separate CLI tools a team must assemble and maintain. **EOIP's `gitops.py` is the integrated
product those four tools imply but never became.** Say so, loudly.

---

### 3.8 Category 8 — Semantic Enrichment, NLP & Ontology Learning

| Tool | License | Extraction | Linking | Learning | EOIP overlap |
|---|---|:---:|:---:|:---:|---|
| Mondeca | Commercial | 4 | 4 | 3 | `extraction/` |
| Diffbot | Commercial | 5 (web) | 5 | 4 | Low (web-focused) |
| **DeepOnto** | Apache 2.0 | — | 4 | **5** (BERT alignment, subsumption prediction) | **Adopt** |
| spaCy / Textacy | MIT | 4 | 4 | — | `nlp/` |

**DeepOnto is the one to adopt.** Transformer-based ontology *alignment* (matching two ontologies'
classes) and *subsumption prediction* directly serve two EOIP needs: merging domain packs without
conflicts, and inducing hierarchy from mined entities. `ONT-015`.

**EOIP's unfair advantage here.** These tools enrich from *text*. EOIP's `fileparse/` handles
**engineering diagrams, images, video, Office, email, archives** — and `connectors/` pulls from
38 live systems with structure already attached. The extraction surface is an order of magnitude
wider than any tool in this category.

---

## 4. Gap Analysis & Prioritized Backlog

IDs continue the existing Phase-4 convention. Each is written for direct AI-agent execution.

### Tier 0 — Credibility blockers (Q1, must ship together)

#### ONT-001 — W3C Serialization Bridge
- **Priority** P0 · **Complexity** M · **Depends** none
- **Path** `packages/eoip/ontology/serialization.py` (new)
- **Do**: add `rdflib>=7.0` (BSD). Implement `RDFSerializer` / `RDFDeserializer` supporting Turtle,
  RDF/XML, N-Triples, N-Quads, JSON-LD, TriG. Map LPG ↔ RDF via a documented, lossless-where-possible
  scheme; reify edge properties only when the edge carries properties (avoid the reification tax
  on the common case). Reuse `rdf.py:jsonld_to_property_graph` as the internal pivot.
- **Accept**:
  - [ ] Round-trip `gist`, `schema.org`, FOAF, Dublin Core, and a 10k-triple SKOS thesaurus
  - [ ] Round-trip fidelity ≥ 99% on node/edge/property counts; losses enumerated in a report
  - [ ] `POST /ontology/import` accepts all six formats; `GET /ontology/export?format=turtle` emits valid output
  - [ ] Output validates in Protégé 5.6 without error
  - [ ] Property-name collisions and datatype coercion covered by unit tests

#### ONT-004 — Conformant SHACL
- **Priority** P0 · **Complexity** S · **Depends** ONT-001
- **Path** `packages/eoip/ontology/shacl_validator.py` (rewrite), `rdf.py:export_shacl_shapes` (fix)
- **Do**: add `pyshacl` (Apache 2.0). Emit real SHACL — `sh:datatype`, `sh:nodeKind`, `sh:minCount`,
  `sh:maxCount`, `sh:pattern`, `sh:class`, `sh:in`. Move `allowedEndpointPairs` to conformant
  `sh:targetObjectsOf` + `sh:class` constraints. Keep the existing `SHACLValidationReport` as the
  public API; delegate execution to pySHACL so callers are unaffected.
- **Accept**:
  - [ ] Exported shapes pass the W3C SHACL test suite parser
  - [ ] Validation report matches pySHACL's `sh:ValidationReport` structure
  - [ ] A deliberately invalid graph produces violations identical to reference pySHACL output
  - [ ] Existing `/ontology/validate` callers unchanged (contract test)

#### ONT-007 — Pluggable Reasoner Port
- **Priority** P0 · **Complexity** M · **Depends** ONT-001
- **Path** `packages/eoip/ontology/reasoning/` (new package)
- **Do**: define `ReasonerPort` protocol (`classify`, `is_consistent`, `unsatisfiable_classes`,
  `realize`, `explain`). Adapters: `ELKAdapter` (Apache 2.0, EL++ — **default**, license-safe),
  `NativeAdapter` (wrap existing `OWLReasoner` for offline/air-gap), `FusekiAdapter` (rules).
  **Delete the hardcoded `_bootstrap_core_axioms()` demo axioms** — load axioms from the manifest
  and installed domain packs instead.
- **Accept**:
  - [ ] Classifies a 20k-class ontology in < 60s
  - [ ] Detects unsatisfiable classes on a known-inconsistent fixture
  - [ ] No hardcoded domain axioms remain anywhere in `ontology/`
  - [ ] Air-gap mode works with `NativeAdapter` and degrades explicitly, not silently

### Tier 1 — Strategic differentiators (Q1–Q2)

| ID | Title | P | Cx | Why it matters |
|---|---|:--:|:--:|---|
| **ONT-005** | **Connector Mapping Language (CML)** | P0 | L | Makes "connect to any enterprise system" true as *config*, not code. Highest architectural leverage. |
| **ONT-006** | AI-suggested CML mappings from sampled payloads | P1 | M | Novel, patentable; kills Palantir's implementation-time advantage |
| **ONT-009** | Governed Action Layer (write-back) | P0 | L | Only axis where Palantir is genuinely ahead |
| **ONT-002** | SPARQL 1.1 endpoint over LPG store | P1 | L | RFP checkbox; unlocks BI tools + federation |
| **ONT-003** | RDF backend port (Jena Fuseki ref, GraphDB certified) | P1 | M | Turns competitors into distribution channels |
| **ONT-008** | Formalize hybrid materialize/virtualize reasoning | P1 | M | Defensible IP; already half-built |
| **ONT-011** | MCP server for ontology + Actions | P1 | S | Becoming table stakes; ~2 weeks |
| **ONT-013** | Ontology pitfall scanner (OOPS!-class) | P1 | M | Completes Ontology-as-Code story; PR quality gate |

### Tier 2 — Completeness (Q2–Q3)

| ID | Title | P | Cx |
|---|---|:--:|:--:|
| ONT-010 | Ship `gist` + FIBO + schema.org as domain packs | P1 | S |
| ONT-012 | Position & document "Ontology-as-Code" (no code) | P0 | XS |
| ONT-014 | Widoco-class HTML ontology documentation generator | P2 | M |
| ONT-015 | DeepOnto-based ontology alignment for pack merging | P2 | L |
| ONT-016 | SKOS RDF import/export (wire `skos.py` to ONT-001) | P1 | S |
| ONT-017 | R2RML/RML import → CML translation (migration path) | P2 | M |
| ONT-018 | PROV-O provenance emission on every mined triple | P1 | M |
| ONT-019 | OWL export round-trip certification vs Protégé (CI gate) | P1 | S |
| ONT-020 | Ontology benchmark harness (LUBM, BSBM, SP2Bench) | P1 | M |

---

## 5. Cons-to-Pros Inversion Blueprint

The consolidated inversion table. Each row: a competitor weakness → the EOIP design that converts
it into an advantage → where it lands.

| # | Competitor con | Who | EOIP inversion | Requirement |
|---|---|---|---|---|
| I1 | RDF cannot give identity to parallel same-type relationships; reification bloat | All triplestores | Native LPG — edges have identity + properties with zero overhead. "No reification tax." | Existing; **market it** |
| I2 | SPARQL reasoning has no termination guarantee | Triplestores | Hard token/time budgets with graceful degradation via `token_budget/` + control loops | ONT-002 + existing |
| I3 | Triplestores are weak at traversal | Conceded by Ontotext | Traversal-native: `paths.py`, `algorithms.py`, `community.py`, `process_mining.py` | Existing |
| I4 | Forward-chaining stalls on TBox change (full recompute) | GraphDB | Hybrid: materialize stable inferences, rewrite volatile ones at query time | ONT-008 |
| I5 | Query-time reasoning costs per-query latency | Stardog, Ontop | Same hybrid, decided per-rule by cost model | ONT-008 |
| I6 | Ontology tools assume the data has already arrived | Protégé, TopBraid, VocBench | 38 connectors + universal factory + crawler; the ontology comes to the data | Existing; **market it** |
| I7 | OBDA limited to OWL 2 QL over relational sources | Ontop | CML maps *any* connector payload; per-source materialize/virtualize choice | ONT-005 |
| I8 | New source = new hand-written integration | Everyone | New source = a YAML file | ONT-005 |
| I9 | ML-assisted mapping never productized | Karma | AI-suggested mappings from sampled payloads | ONT-006 |
| I10 | Proprietary formats; migration out is hard | Palantir, Reltio, Collibra | Every artifact exports to an open standard | ONT-001, ONT-004 |
| I11 | High TCO; per-seat pricing cliffs | Palantir, MarkLogic | Self-hostable, 4-tier, published TCO calculator | TASK-LIC-009/010 |
| I12 | Months-to-a-year implementation; manual relationship modeling | Palantir | Ontology induction mines the model, humans curate it | ONT-006 + `ontology_induction.py` |
| I13 | Agent tooling described as basic | Palantir AIP | 35 agents, 14 control loops, 9 reasoning strategies, verification engine | Existing |
| I14 | Ontology CI/CD requires assembling 4+ separate CLI tools | ROBOT+pySHACL+OOPS!+Widoco | One integrated governed workflow | Existing + ONT-013/014 |
| I15 | Change workflow without version-control semantics | TopBraid EDG | Branch/PR/merge/semver/rollback-receipt | **Existing — unique** |
| I16 | No migration scripts generated on schema change | All | `generate_ontology_migration_script` | **Existing — unique** |
| I17 | Ontology silently drifts from reality | All | `drift.py` + `embedding_drift.py` detect and propose evolution | **Existing — unique** |
| I18 | Catalogs describe but cannot reason | Collibra, Alation, Atlas | Catalog + ontology + reasoner + agents in one system | Existing + ONT-007 |
| I19 | WebProtégé is AGPL; Neo4j CE is GPLv3; Virtuoso is GPLv2 | — | Permissive-only dependency policy; ELK over HermiT; Fuseki over Neo4j as reference | TASK-LEGAL-004, ONT-003 |
| I20 | Life-science / publishing verticals locked to specialist tools | SciBite, Data Harmony | Domain packs + industry templates make verticals a config artifact | Existing + ONT-010 |

**Inversions already won (ship marketing, not code): I1, I3, I6, I13, I15, I16, I17.**
Seven of twenty. That is the story Marketing should be telling while engineering closes the rest.

---

## 6. Design Recommendations

### 6.1 Target module layout

```
packages/eoip/ontology/
├── serialization.py          # ONT-001  rdflib bridge: TTL/RDFXML/NT/NQ/JSON-LD/TriG
├── reasoning/                # ONT-007  reasoner port + adapters
│   ├── port.py               #          ReasonerPort protocol
│   ├── elk_adapter.py        #          Apache 2.0 — default
│   ├── native_adapter.py     #          wraps existing OWLReasoner (air-gap)
│   └── hybrid.py             # ONT-008  materialize/virtualize cost model
├── mapping/                  # ONT-005  Connector Mapping Language
│   ├── language.py           #          CML schema + parser
│   ├── executor.py           #          payload → triples
│   ├── suggest.py            # ONT-006  AI-suggested mappings
│   └── r2rml_import.py       # ONT-017  migration from R2RML/RML
├── actions/                  # ONT-009  governed write-back
│   ├── model.py              #          OntologyAction, preconditions, effects
│   ├── executor.py           #          autonomy-gated execution + audit receipt
│   └── registry.py
├── lint/                     # ONT-013  pitfall scanner
├── sparql/                   # ONT-002  SPARQL 1.1 → LPG translation
├── mcp_server.py             # ONT-011
├── shacl_validator.py        # ONT-004  rewritten over pySHACL
├── gitops.py                 #          ← the moat. Do not destabilize.
└── (existing modules unchanged)
```

**Non-negotiable constraint:** `gitops.py`, `manifest.py`, and `packs.py` are the moat and the
stable core. New work attaches to them through ports; it does not refactor them. Any PR touching
`gitops.py` requires Lead Developer review (TASK-LD-013).

### 6.2 API surface (additions)

```
POST   /ontology/import              {format, content}      → import report
GET    /ontology/export?format=      turtle|rdfxml|nt|jsonld|trig
POST   /ontology/validate/shacl      {graph?, shapes?}      → sh:ValidationReport
POST   /ontology/reason/classify     {}                     → class hierarchy + unsatisfiable
POST   /ontology/reason/explain      {axiom}                → proof tree
POST   /sparql                       {query}                → SPARQL JSON results
GET    /sparql                       ?query=                → (W3C protocol compliance)
POST   /ontology/mapping             {cml}                  → validation + dry-run triples
POST   /ontology/mapping/suggest     {source, samples}      → suggested CML
GET    /ontology/mapping/{source}
POST   /ontology/actions/{id}/invoke {params}               → receipt (autonomy-gated)
GET    /ontology/actions                                    → registry
POST   /ontology/lint                {}                     → pitfall findings
GET    /ontology/docs                                       → generated HTML spec
```

Follow the existing conventions: Pydantic request models at **module level** (required for
FastAPI OpenAPI schema resolution — this bit the team on the intelligence endpoints), thread-safe
singleton accessors, and a `stats()` method on every engine wired into `brain_os.py` telemetry.

### 6.3 LPG ↔ RDF mapping scheme (ONT-001 core decision)

| LPG construct | RDF representation | Notes |
|---|---|---|
| Vertex | IRI `eoip:entity/{Label}/{id}` | `rdf:type eoip:class/{Label}` |
| Vertex property | Literal via `eoip:property/{name}` | datatype from manifest |
| Edge **without** properties | Direct triple `(s, eoip:relation/{label}, o)` | **no reification — the common case** |
| Edge **with** properties | RDF-star `<<s p o>>` when target supports it; else named-graph reification | Degrade explicitly, record in report |
| Named graph / tenant | `TriG` graph IRI `eoip:tenant/{id}` | preserves multi-tenancy on export |
| Provenance | PROV-O on the edge/graph | ONT-018 |

The "no reification for simple edges" rule is what makes EOIP's export *cleaner* than a naive
LPG→RDF dump, and it is the technical substance behind inversion I1. Document it.

---

## 7. Benchmark Plan

| Benchmark | Dataset | Measures | Target |
|---|---|---|---|
| **LUBM** | 1k–10k universities (~130M triples) | Load time, query latency Q1–Q14, inference completeness | Load ≥ 50k triples/s; Q1–Q14 p95 < 500ms |
| **BSBM** | 100M triples | Mixed read/write business intelligence | ≥ 1,000 QMpH |
| **SP2Bench** | 50M triples | SPARQL operator coverage & optimizer quality | No query > 30s |
| **SHACL throughput** | 10M nodes, 500 shapes | Validation rate | ≥ 20k nodes/s |
| **Classification** | 20k classes / 150k axioms (GALEN, GO) | Reasoner wall time | < 60s (ELK) |
| **Round-trip fidelity** | gist, FIBO, schema.org, SNOMED subset | Node/edge/property loss | ≥ 99%, losses enumerated |
| **CML throughput** | 1M Jira issues | Payload → triples rate | ≥ 10k records/s |

Reproducibility: commit generator commands, fixed seeds, and expected-output hashes under
`tests/benchmarks/ontology/`. Wire a regression gate into CI (TASK-QAL-010) that fails the build on
> 10% latency regression.

---

## 8. Security, Legal & Licensing Assessment

### 8.1 Dependency licensing decision table

| Dependency | License | Verdict | Rationale |
|---|---|---|---|
| `rdflib` | BSD-3 | ✅ **Adopt** | Permissive; the de facto Python RDF library |
| `pySHACL` | Apache 2.0 | ✅ **Adopt** | Reference implementation |
| **ELK** reasoner | Apache 2.0 | ✅ **Adopt as default** | Permissive; EL++ covers most enterprise ontologies |
| HermiT | LGPL | ⚠️ **Optional plugin only** | Full OWL 2 DL but copyleft — never bundle in core |
| Openllet | Apache 2.0 | ✅ Alternative to HermiT | More expressive than ELK, permissive |
| Apache Jena / Fuseki | Apache 2.0 | ✅ **Reference RDF backend** | Zero license risk |
| Eclipse RDF4J | EPL 2.0 / BSD | ✅ Acceptable | Weak copyleft, file-level |
| **Neo4j Community** | **GPLv3** | ⛔ **Do not bundle** | Connector over the wire only; never link |
| **Virtuoso OSE** | **GPLv2** | ⛔ **Do not bundle** | Same |
| **WebProtégé** | **AGPL** | ⛔ **Never integrate** | AGPL network clause is fatal to SaaS |
| TerminusDB | **Disputed (Apache vs GPLv3)** | ⛔ **Blocked pending Legal** | Sources conflict — verify before any use |
| `gist` ontology | CC-BY | ✅ Adopt with attribution | Attribution notice required in docs |
| FIBO | MIT | ✅ Adopt | — |
| SNOMED-CT | **Affiliate licence required** | ⚠️ Customer-provided only | Never redistribute |

**Action for Legal (extends TASK-LEGAL-004/006):** the GPL contamination risk is concentrated in
exactly three places — Neo4j, Virtuoso, WebProtégé. All three are reachable only over a network
boundary in the current design. **Codify "network boundary only, never link" as policy** and add a
CI license-scan gate that fails on any GPL/AGPL entering the dependency graph.

### 8.2 Threat model additions (extends TASK-SEC-001)

| Threat | Vector | Mitigation |
|---|---|---|
| **XXE via RDF/XML import** | Malicious external entity in uploaded ontology | Disable entity resolution in the parser; `rdflib` with `resolve_entities=False`; size caps |
| **Billion-laughs / entity expansion** | Nested entity bomb | Hard expansion limits; parse timeout |
| **SPARQL injection** | Untrusted string into query | Parameterized query construction only; never string-concatenate |
| **SPARQL DoS** | Unbounded `OPTIONAL`/property-path query | Query cost estimator + hard timeout + result caps (reuses `token_budget/`) |
| **Reasoner DoS** | Adversarial ontology with exponential classification | Classification timeout; pre-flight axiom-count check; ELK profile restriction |
| **CML mapping as code execution** | Template injection in subject/object templates | Templates are a restricted grammar, **never `eval`**; whitelist functions |
| **Action write-back abuse** | Agent triggers destructive ERP write | Autonomy-gated (HCTL for destructive), precondition SHACL, approval receipt, idempotency key |
| **PII leakage via ontology export** | Exported graph contains classified fields | Classification-aware export filter honoring `governance.classification` in CML |
| **Cross-tenant leakage on export** | Named-graph boundary dropped | TriG export preserves tenant graph IRIs; contract test |

### 8.3 Patent candidates (feeds TASK-LEGAL-001)

Five of these are, on their face, novel over the prior art surveyed here. **File provisionals
before any public disclosure, conference talk, or docs-site publication:**

1. **Semver-computed ontology versioning from semantic diff** (`compute_next_semver`) — no competitor does this.
2. **Automated migration-script generation from ontology diff** — no competitor does this.
3. **Hybrid per-rule materialize/virtualize reasoning with a cost model** (ONT-008).
4. **AI-suggested declarative source-to-ontology mappings from sampled payloads** (ONT-006).
5. **Combined structural + embedding drift detection driving automated ontology evolution proposals** (`drift.py` + `embedding_drift.py`).

---

## 9. Roadmap

### Q1 — Credibility (standards parity)
`ONT-001` → `ONT-004` → `ONT-007` → `ONT-016` → `ONT-019` → `ONT-012`
**Exit criteria:** EOIP imports and re-exports `gist`, FIBO, and schema.org losslessly; exported
shapes pass the W3C SHACL suite; no hardcoded axioms remain; a technical buyer's 10-minute probe
passes. **This quarter removes findings F1, F2, F3.**

### Q2 — Differentiation (the moat, widened)
`ONT-005` → `ONT-006` → `ONT-009` → `ONT-011` → `ONT-013` → `ONT-010`
**Exit criteria:** a new enterprise source is onboarded by writing one YAML file; agents act on the
enterprise through governed, audited Actions; MCP server live.

### Q3 — Scale & completeness
`ONT-002` → `ONT-003` → `ONT-008` → `ONT-018` → `ONT-020` → `ONT-014` → `ONT-015` → `ONT-017`
**Exit criteria:** SPARQL endpoint passes W3C protocol tests; LUBM-10k benchmarked and published;
EOIP runs against a customer's existing GraphDB.

### Risk register (ontology-specific; feeds TASK-DM-010)

| # | Risk | Sev | Mitigation |
|---|---|---|---|
| OR1 | LPG↔RDF round-trip is lossy in edge cases; interop claims overstated | High | ONT-019 CI certification gate; publish the loss report honestly |
| OR2 | SPARQL-over-LPG translation underperforms native triplestores | High | Set expectations: SPARQL is for *interop*, not hot paths; ONT-003 offers a native backend |
| OR3 | GPL contamination enters via a transitive dependency | High | CI license scan; permissive-only policy |
| OR4 | ONT-005 CML scope creeps into a general ETL language | Med | Hard scope: payload→ontology mapping only. No transformations beyond a whitelisted function set |
| OR5 | Reasoner performance collapses on customer ontologies | Med | ELK/EL++ default + pre-flight profile check + explicit degradation message |
| OR6 | Marketing claims standards compliance before Q1 ships | **High** | **Gate all standards messaging on ONT-019 passing.** Legal + Marketing sign-off |
| OR7 | `gitops.py` destabilized by adjacent work | Med | Ports-only policy; Lead Dev review on every touch |

---

## 10. Appendices

### A. Evidence index (repository)

| Claim | Path |
|---|---|
| Toy OWL reasoner, hardcoded axioms | `packages/eoip/ontology/rdf.py:598-700` |
| Non-conformant SHACL export | `packages/eoip/ontology/rdf.py:369-425` |
| Custom SHACL validator | `packages/eoip/ontology/shacl_validator.py:77-193` |
| Ontology GitOps workflow | `packages/eoip/ontology/gitops.py:220-383` |
| Semver from semantic diff | `packages/eoip/ontology/gitops.py:733` |
| Migration-script generation | `packages/eoip/ontology/gitops.py:545` |
| Rollback receipts | `packages/eoip/ontology/gitops.py:613-733` |
| Drift detection | `packages/eoip/ontology/drift.py:56` |
| Embedding drift | `packages/eoip/ontology/embedding_drift.py:78` |
| Schema generation | `packages/eoip/ontology/schema_gen.py:33-96` |
| Universal connection factory | `packages/eoip/connectors/factory.py` (1,135 LOC) |
| Graph backend ports | `packages/eoip/graph/backends.py:189-245` |
| Query dialects (no SPARQL) | `packages/eoip/qlang/` |

### B. External sources

- [Semantic Web Company and Ontotext merge to create Graphwise](https://graphwise.ai/blog/graphwise-merger-swc-ontotext) — Oct 2024; GraphDB and PoolParty brands retained
- [Graphwise FAQ](https://graphwise.ai/faq/) — brand transition plan
- [Altair acquires Cambridge Semantics](https://bigdatawire.com/2024/04/19/altair-bolsters-analytics-offering-with-cambridge-semantics-buy) — Apr 2024; Anzo folding into Altair RapidMiner
- [Stardog reasoning overview](https://atlan.com/know/ai-agent/knowledge-graph/what-is-stardog/) — query-time OWL 2 (QL/RL/EL unioned as SL) + SWRL (third-party source)
- [TerminusDB](https://en.wikipedia.org/wiki/TerminusDB) — v12.x active 2026; **license reported inconsistently**
- [Neo4j: RDF vs property graphs](https://neo4j.com/blog/knowledge-graph/rdf-vs-property-graphs-knowledge-graphs/) — relationship-identity and termination criticisms (vendor source)
- [Ontotext: triplestores as operational graph databases](https://www.ontotext.com/blog/triplestores-are-proven-as-operational-graph-databases/) — concedes weak out-of-box traversal (vendor source)
- [TigerGraph: RDF vs property graph](https://www.tigergraph.com/blog/rdf-vs-property-graph-choosing-the-right-foundation-for-knowledge-graphs/) — join-overhead argument (vendor source)
- [Property Graph vs RDF Triple Store (PLOS ONE)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4684231/) — peer-reviewed; portability argument favors RDF (2015, dated)
- [Gremlinator: SPARQL over property graphs](https://arxiv.org/pdf/1801.09556) — translation precedent relevant to ONT-002
- [Expressive Reasoning Graph Store](https://arxiv.org/pdf/2209.05828) — unified RDF + property-graph framework
- [Palantir AIP/Foundry negotiation white paper](https://redresscompliance.com/palantir-aip-foundry-negotiation.html) — TCO and per-seat cost claims (**vendor of negotiation services — self-interested**)
- [Palantir analysis 2026](https://blog.pebblous.ai/project/BizReport/palantir-analysis-2026/en/) — FY2025 revenue $4.46B

> **Evidence caveat.** Most competitive claims in Categories 3 and 5 come from vendor blogs or
> consultancies with commercial interests. Scores marked from these sources are **indicative, not
> audited**. Before any of this reaches a customer-facing battlecard (TASK-MKT-003), the
> performance and cost figures must be independently verified or dropped.

### C. Open questions for sign-off

1. Confirm target scale (§1.3) — drives ONT-003 backend choice and all of §7.
2. Air-gap requirement: does any customer forbid the ELK JVM sidecar? (Drives `NativeAdapter` priority.)
3. Is write-back (ONT-009) in scope for v1, or read-only until SOC 2 lands? **Security Officer decision.**
4. Legal: resolve the TerminusDB license question, then permanently remove or admit it.
5. Does Marketing accept gating all standards messaging on ONT-019? (Risk OR6.)

---

*End of document.*
