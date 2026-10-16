# gaps-implementation.md
## Phase-by-Phase Implementation Plan for Competitive Gap Closure

**Date:** 2026-10-01  
**Companion document:** `gaps-requirements.md`  
**Primary database:** Apache HugeGraph  
**Deployment baseline:** Docker / Docker Compose; no required cloud services  
**Design rule:** Build the smallest complete vertical slice first, then add capability layers without re-platforming.

---

# 1. Implementation Strategy

The platform should not attempt to implement every competitive capability in the first release.

The recommended progression is:

**Foundation → Trust → Semantic Control → Engineering Intelligence → Retrieval/AI → Enterprise Governance → Scale → Ecosystem**

Every phase must leave the system deployable and demonstratable.

---

# 2. Phase Map

| Phase | Theme | Primary Outcome |
|---|---|---|
| 0 | Architecture & contracts | Stable foundations |
| 1 | Sellable vertical-slice MVP | Real end-to-end demo |
| 2 | Trustworthy ontology platform | Provenance, quality, ontology GitOps |
| 3 | Enterprise engineering intelligence | digital thread, code/runtime impact |
| 4 | Retrieval & GraphRAG intelligence | evidence-backed knowledge assistant |
| 5 | Federation & knowledge products | semantic fabric + catalog |
| 6 | Agentic knowledge operations | governed agents/MCP actions |
| 7 | Enterprise security & HA | production readiness |
| 8 | Advanced analytics & simulation | predictive/what-if intelligence |
| 9 | Ecosystem & domain packs | extensibility and market expansion |

---

# 3. Phase 0 — Architecture Foundation

## Goal
Prevent later architectural rewrites.

## Duration
Target 2–4 engineering weeks depending on existing code.

## Requirements
- GAP-CP-001..009
- GAP-HG-001
- GAP-PORT-001
- GAP-DBAGNOSTIC-001
- initial GAP-OBS-001..005
- initial GAP-AGOV-001..004

## Deliverables

### 3.1 Canonical Contracts
Create versioned Pydantic/JSON Schema contracts for:

- SourceRecord
- CanonicalEntity
- CanonicalRelationship
- SourceIdentity
- Evidence
- ProvenanceRecord
- GraphMutation
- GraphMutationResult
- ValidationFinding
- QueryRequest
- QueryPlan
- QueryResult
- RetrievalResult
- EvidenceManifest
- AgentAction
- AuditEvent

### 3.2 Core IDs
Define stable identity format:

`urn:org:<tenant/domain>:<entity-type>:<stable-id>`

Do not use database-internal IDs as external identity.

### 3.3 Service Boundaries

Start as a modular monorepo:

```text
/apps
  /web-user
  /web-admin
  /vscode-extension
/services
  /api
  /ingestion
  /ontology
  /query
  /retrieval
  /agents
/packages
  /contracts
  /hugegraph-client
  /ontology-core
  /provenance
  /validation
  /connector-sdk
  /agent-sdk
  /mcp-sdk
/deploy
  /docker
/tests
/docs
```

Do not split into many network microservices until operational need exists.

### 3.4 HugeGraph Repository Abstraction

Interfaces:
- EntityRepository
- RelationshipRepository
- TraversalRepository
- SchemaRepository
- MutationRepository
- GraphMetadataRepository

This keeps domain logic testable and reduces vendor coupling.

### 3.5 CI Baseline
- lint
- static typing
- unit tests
- dependency vulnerability scan
- SBOM
- container build
- Docker startup smoke test

## Exit Criteria
- clean checkout → one command → local stack runs.
- graph schema initializes idempotently.
- stable external IDs confirmed.
- schema/version metadata available.
- OpenAPI generated.
- tests run locally and in CI.

---

# 4. Phase 1 — Fully Functional Demonstrable MVP

## Goal
Create a real end-to-end product nucleus, not prototypes.

## Core Use Case
`Jira → Git/Code → Build/Deployment metadata → Documentation`

Then answer:
- “What code implements this requirement?”
- “What changes if this function is modified?”
- “Why does the system believe this relationship?”
- “Show the evidence.”

## Requirements
- baseline requirements from existing MVP
- GAP-SDT-001..004
- GAP-PROV-001..006
- GAP-HG-002..005
- GAP-QI-007
- GAP-KRAG-001, 002, 007, 009
- GAP-OBS-001..005
- GAP-OFFLINE-001

## Workstreams

### 4.1 HugeGraph
- Docker image.
- schema loader.
- property keys.
- vertex labels.
- edge labels.
- indexes.
- health check.
- backup command.
- restore command.

### 4.2 Jira Connector
- JSON file import first.
- optional API ingestion.
- checkpoint.
- normalized events.
- idempotent upsert.

### 4.3 Git/Code Connector
- repository metadata.
- commits.
- branches.
- changed files.
- Tree-sitter symbols.
- imports/calls where reliable.

### 4.4 Cross-Link Engine
Deterministic rules before AI:
- Jira key in branch.
- Jira key in commit.
- Jira key in MR.
- code ownership.
- repository/project mappings.

LLM/entity inference is optional and marked `INFERRED`.

### 4.5 Provenance
Every mutation stores:
- source,
- source ID,
- ingestion run,
- parser/mapping version,
- timestamp,
- confidence,
- evidence pointer.

### 4.6 Query API
Minimum:
- entity lookup,
- neighbors,
- path,
- issue-to-code,
- code-to-issue,
- impact analysis,
- provenance.

### 4.7 User Web
- universal search.
- graph explorer.
- entity panel.
- evidence panel.
- impact analysis page.

### 4.8 Admin Web
- connector run.
- ingest status.
- graph stats.
- validation.
- backup/restore status.

### 4.9 VS Code
- current file/symbol lookup.
- Jira links.
- related commits.
- impact query.
- evidence view.

### 4.10 GraphRAG
- local embeddings/local model.
- retrieval from real graph.
- answer requires Evidence Manifest.
- abstain when evidence below threshold.

### 4.11 MCP
Read-only first:
- search_entity
- get_entity
- get_neighbors
- find_path
- impact_analysis
- get_evidence

## Tests
- duplicate ingestion.
- connector replay.
- expected graph path.
- invalid path.
- source deletion.
- parser error.
- backup/restore.
- GraphRAG groundedness.
- VS Code → API integration.
- no external egress.

## Demo Exit Criteria
A clean system can ingest sample data and reproduce the full Jira→code path without hardcoded graph results.

---

# 5. Phase 2 — Trustworthy Ontology & Semantic Governance

## Goal
Move from “connected graph” to “governed enterprise ontology.”

## Requirements
- GAP-GITOPS-001..008
- GAP-CONTRACT-001..006
- GAP-KQ-001..006
- GAP-TRUTH-001..010
- GAP-TRUST-001..005
- GAP-STUDIO-001..011
- GAP-TAX-001
- GAP-GOV-001..003

## 5.1 Ontology-as-Code
Create canonical YAML/Turtle/JSON-LD representation.

Example:
```yaml
class: Service
version: 1.2.0
properties:
  - name: criticality
    type: enum
relationships:
  - name: DEPENDS_ON
    target: Service
constraints:
  - rule: owner_required
```

Compiler outputs:
- HugeGraph schema migration.
- semantic/RDF representation.
- validation rules.
- documentation.
- optional UI forms.

## 5.2 Semantic Diff Engine
Implement AST-like comparison rather than text diff.

Classify:
- non-breaking additive,
- potentially breaking,
- breaking,
- migration-required.

## 5.3 Ontology CI
Pipeline:
1. syntax validation,
2. semantic validation,
3. compatibility,
4. sample-data validation,
5. graph invariant tests,
6. migration simulation,
7. quality regression,
8. publish artifact.

## 5.4 Ontology Studio
React UI:
- graph model canvas,
- hierarchy panel,
- class/property editor,
- constraints,
- source mapping,
- diff,
- review.

## 5.5 Claim/Truth Model
Introduce:
- Claim
- Evidence
- CanonicalAssertion
- ResolutionDecision

Do not force contradictory sources into one value.

## 5.6 Trust Zones
Separate labels/metadata for:
Raw → Parsed → Inferred → Reviewed → Trusted → Certified.

## Exit Criteria
- ontology branch can be modified, diffed, validated and released.
- breaking change is detected before deployment.
- graph quality dashboard is operational.
- a conflicting fact can be inspected and adjudicated.

---

# 6. Phase 3 — Enterprise Engineering Intelligence

## Goal
Create a differentiation moat around engineering digital thread and change intelligence.

## Requirements
- GAP-SDT-005..008
- GAP-ARCH-001..006
- GAP-CHANGE-001..006
- GAP-FRESH-001..005
- semantic release diff requirements
- expert/ownership features where appropriate

## 6.1 Deep Code Graph
Add:
- symbol references,
- callers/callees,
- inheritance,
- interface implementation,
- API endpoints,
- data models,
- config dependencies,
- tests,
- package dependency graph.

Prioritize languages used by pilot customers.

## 6.2 CI/CD Graph
Connect:
- commit,
- build,
- test,
- artifact,
- pipeline,
- deployment,
- environment.

## 6.3 Runtime/ITSM Graph
Connect:
- service,
- incident,
- problem,
- change,
- alert,
- owner,
- runbook.

## 6.4 Architecture Conformance DSL
Example:
```text
RULE UI_NO_DIRECT_DB
FROM Component(type="ui")
MUST_NOT_REACH Component(type="database")
EXCEPT_VIA Service(type="api")
```

Compiler:
DSL → graph traversal → findings.

## 6.5 Pre-Merge Impact
Webhook/local command:
- inspect changed symbols,
- map to graph,
- traverse dependencies,
- identify tests/services/docs/owners,
- return evidence.

## 6.6 Documentation Freshness
Compare graph/code facts with docs.
Create review recommendation, never silently rewrite authoritative docs.

## Exit Criteria
Demonstrate:
`PR diff → impacted functions → services → tests → Jira → owners → runtime history → docs`

---

# 7. Phase 4 — Unified Retrieval & Evidence-Backed GraphRAG

## Goal
Make AI a trustworthy consumer of the ontology rather than an alternate source of truth.

## Requirements
- GAP-RET-001..006
- GAP-SEARCH-001..002
- GAP-KRAG-001..010
- GAP-GRAG-001..006
- GAP-CACHE-001..005
- GAP-QI-001..008

## 7.1 Retrieval Router

Inputs:
- intent,
- entities,
- requested freshness,
- scope,
- security context,
- latency budget.

Routes:
- direct Gremlin,
- full-text,
- vector,
- hybrid,
- code-symbol,
- temporal,
- provenance.

## 7.2 Full Text
Use local OpenSearch only if operationally justified.
For smaller deployments, use a lighter local index.

Create a SearchIndex interface so implementation is replaceable.

## 7.3 Vector
Local embeddings.
Store vector references to canonical entity IDs.
Do not create an untraceable second knowledge store.

## 7.4 GraphRAG Evaluation Harness
Dataset:
- factual one-hop,
- multi-hop,
- global/theme,
- temporal,
- contradictory,
- insufficient evidence,
- code impact.

Compare:
1. no RAG,
2. vector RAG,
3. direct graph,
4. graph+text hybrid,
5. community GraphRAG.

Metrics:
- answer correctness,
- evidence precision,
- evidence recall,
- groundedness,
- abstention correctness,
- latency,
- compute.

## 7.5 Community Summaries
Implement incrementally:
graph CDC → affected community → regenerate only affected summaries.

## Exit Criteria
Every generated answer has machine-readable evidence and can be replayed against a graph version.

---

# 8. Phase 5 — Federation, Catalog & Knowledge Products

## Goal
Support heterogeneous enterprises without copying everything into one physical store.

## Requirements
- GAP-FED-001..004
- GAP-FABRIC-001..008
- GAP-CATALOG-001..005
- GAP-KP-001..005
- GAP-LAYER-001..002
- GAP-LIN-001..005
- GAP-DATAOPS-001

## 8.1 Federation Architecture

Create:
- Source Capability Registry.
- Query Fragment Planner.
- Connector Query Adapter.
- Cache.
- Provenance merger.

Execution plan example:
```text
HugeGraph: find services owned by Team X
PostgreSQL adapter: fetch current SLA
ServiceNow adapter: fetch open P1 incidents
merge locally
attach provenance
```

## 8.2 Materialization Policy
Per entity/domain:
- LIVE
- CACHE_TTL
- MATERIALIZED
- HYBRID

## 8.3 Knowledge Catalog
Index:
- datasets,
- graphs,
- ontology versions,
- source systems,
- mappings,
- agents,
- queries,
- dashboards,
- knowledge products.

## 8.4 Knowledge Products
Provide templates:
- Engineering Digital Thread
- Change Risk
- Service 360
- Incident 360
- Application 360
- Audit Evidence Pack

## Exit Criteria
One query can combine materialized graph knowledge and at least one live external source with provenance.

---

# 9. Phase 6 — Governed Agentic Knowledge Operations

## Goal
Allow agents to perform bounded, auditable knowledge work.

## Requirements
- GAP-AKO-001..010
- GAP-AGOV-001..012
- GAP-KFW-001..008
- agent evaluation requirements

## 9.1 Agent Runtime
State machine:
`Receive → Context → Plan → Validate → Execute → Observe → Verify → Finish`

Hard controls:
- max steps,
- max tool calls,
- timeout,
- budget,
- cancellation,
- circuit breaker.

## 9.2 Tool Risk Classes
- R0: read-only lookup
- R1: expensive read
- R2: reversible write
- R3: external/change action
- R4: destructive/high-risk

Human approval by policy.

## 9.3 Initial Agents
1. Data Quality Agent
2. Ontology Review Agent
3. Change Impact Agent
4. Incident Investigation Agent
5. Connector Diagnosis Agent

Avoid autonomous self-modifying agents in production.

## 9.4 Knowledge Firewall
Run before:
- model context assembly,
- MCP execution,
- agent tool action,
- external export.

## 9.5 Evaluation
Each agent must pass:
- golden tasks,
- tool selection accuracy,
- invalid action rate,
- evidence coverage,
- hallucination rate,
- timeout/recovery.

## Exit Criteria
Agent actions are replayable and every tool action is attributable to user, agent, policy and evidence.

---

# 10. Phase 7 — Enterprise Security, HA & Operational Maturity

## Goal
Move from pilot-ready to enterprise production-ready.

## Requirements
- GAP-SEC-* security roadmap
- GAP-HA-001
- GAP-LITE-001..002
- production HugeGraph distributed requirements
- full backup/restore and DR

## 10.1 Identity
Add:
- local admin bootstrap,
- OIDC,
- SAML,
- LDAP/AD.

## 10.2 Authorization
Add:
- RBAC,
- ABAC,
- domain policy,
- graph/property filters when required.

Source permission synchronization should be configurable.

## 10.3 HugeGraph Distributed
Validate current HugeGraph distributed architecture and chosen storage backend before production.

Implement:
- cluster topology,
- rolling restart procedure,
- capacity plan,
- backup,
- restore,
- failure testing.

## 10.4 HA Application Layer
- multiple API replicas,
- stateless UI,
- worker failover,
- durable job state,
- distributed locks only where required.

## 10.5 DR
Document:
- RPO,
- RTO,
- backup schedule,
- restore drill,
- disaster recovery test.

## 10.6 Enterprise Operations
- preflight CLI,
- support bundle,
- configuration export,
- diagnostic snapshot,
- upgrade checker,
- migration preview,
- rollback.

## Exit Criteria
Pass production-readiness review and recovery exercise.

---

# 11. Phase 8 — Advanced Analytics, Simulation & Predictive Intelligence

## Goal
Move beyond “what is connected?” to “what may happen?”

## Requirements
- GAP-GDS-001..002
- graph simulation requirements
- calibrated change risk

## 11.1 Analytics
Implement local graph algorithms:
- PageRank,
- betweenness,
- degree centrality,
- connected components,
- community detection,
- similarity,
- shortest path.

## 11.2 Risk Model
Inputs:
- dependency depth,
- service criticality,
- recent change,
- incident history,
- test coverage,
- ownership stability,
- graph centrality.

Output:
Risk factors + evidence, not unexplained score.

## 11.3 What-If Sandbox
Clone logical snapshot metadata.
Apply hypothetical mutation set.
Run:
- validation,
- architecture conformance,
- blast radius,
- quality impact.

## 11.4 Calibration
Compare predicted impact to real outcomes.
Track false positives/negatives.

## Exit Criteria
A change simulation can be reproduced from a graph version + mutation set.

---

# 12. Phase 9 — Ecosystem, Extensions & Domain Packs

## Goal
Turn platform into extensible product ecosystem.

## Requirements
- GAP-MKT-001..008
- GAP-APP-001..002
- GAP-TEMPLATE-001
- GAP-EXT-001
- Domain Packs

## 12.1 SDKs
Publish stable SDK contracts:
- connector,
- parser,
- extractor,
- resolver,
- ontology,
- retriever,
- agent,
- MCP,
- validation,
- UI widget.

## 12.2 Package Manifest
Example:
```yaml
name: bfsi-core
version: 1.0.0
platform: ">=3.0"
provides:
  ontologies:
    - customer
    - account
    - payment
  validators:
    - pii-boundary
dependencies:
  - enterprise-core >=2.4
```

## 12.3 Signing
Later:
- package signatures,
- trusted publisher,
- checksum verification.

## 12.4 App Builder
Compose:
- saved query,
- graph panel,
- table,
- timeline,
- KPI,
- evidence viewer.

All definitions exportable as code/config.

---

# 13. Cross-Phase Architecture Components

## Always Present
1. Canonical Contracts
2. HugeGraph Access Layer
3. Ontology Registry
4. Provenance Service
5. Validation Service
6. Query Planner
7. Audit
8. Telemetry
9. Configuration
10. Version Registry

No phase may bypass these foundations.

---

# 14. Data Migration Strategy

Every graph-schema change must define one of:

- `NO_MIGRATION`
- `LAZY_MIGRATION`
- `ONLINE_BACKFILL`
- `OFFLINE_MIGRATION`
- `REBUILD_FROM_SOURCE`

Migration record:
- source schema version,
- target schema version,
- affected labels,
- estimated mutations,
- reversible?,
- rollback,
- validation.

---

# 15. Testing Evolution by Phase

## Phase 1
Unit + integration + E2E.

## Phase 2
Semantic compatibility + migration + truth/conflict.

## Phase 3
Code-graph accuracy + architecture rules + blast radius.

## Phase 4
Retrieval and AI evaluation.

## Phase 5
Federation consistency and source outage tests.

## Phase 6
Agent safety and prompt/tool injection.

## Phase 7
chaos/failure/recovery/security/performance.

## Phase 8
simulation correctness and predictive calibration.

## Phase 9
SDK compatibility and extension isolation.

---

# 16. Recommended Release Gates

A release cannot progress if any critical gate fails.

### Gate A — Data
- no critical schema violations,
- provenance coverage above configured threshold.

### Gate B — Graph
- no forbidden relationship classes,
- graph invariant tests pass.

### Gate C — Security
- no critical dependency vulnerability,
- no secret leakage,
- egress policy verified.

### Gate D — AI
- groundedness threshold met,
- forbidden-action rate = 0 on safety suite.

### Gate E — Operations
- backup/restore tested for release candidate,
- upgrade migration tested.

---

# 17. Performance Engineering

Create benchmark generators at multiple sizes:

### S
100K vertices / 500K edges

### M
1M vertices / 10M edges

### L
10M vertices / 100M edges

### XL
Defined after production hardware and HugeGraph distributed validation.

Measure:
- ingest throughput,
- upsert latency,
- point lookup,
- 2-hop,
- 5-hop bounded traversal,
- shortest path,
- impact query,
- search,
- hybrid retrieval,
- validation,
- concurrent reads/writes.

Never extrapolate marketing numbers from a different graph engine.

---

# 18. Technology Decisions

## Keep
- Python/FastAPI
- TypeScript/React
- VS Code extension API
- Apache HugeGraph
- Gremlin
- Tree-sitter
- Docker
- local models
- MCP
- OpenAPI
- Mermaid docs

## Add Carefully
- OpenSearch: only when search scale justifies.
- Redis: only when cache/job coordination justifies.
- local object/file store: only when artifact volume justifies.
- message broker: only when ingestion/CDC throughput requires.

Avoid infrastructure by habit.

---

# 19. Implementation Ordering Inside Each Phase

Use this pattern:

1. Contract
2. Storage model
3. Domain service
4. API
5. telemetry
6. tests
7. CLI
8. UI
9. docs
10. acceptance demo

Do not build UI before the domain contract and backend path exist.

---

# 20. Definition of Done for Every Gap Requirement

A GAP requirement is done only if:

- code exists,
- typed interface exists,
- tests exist,
- error handling exists,
- telemetry exists,
- security impact documented,
- migration impact documented,
- user/admin documentation exists,
- requirement ID appears in traceability matrix,
- acceptance criterion demonstrated.

---

# 21. Suggested Milestone Sequence

## M0 — Foundation
Contracts + HugeGraph abstraction + Docker + CI.

## M1 — Connected Graph MVP
Jira + Git + code + graph + query.

## M2 — Evidence
Provenance + evidence + validation.

## M3 — UX
User/Admin/VS Code.

## M4 — Semantic Governance
Ontology Studio + GitOps + quality.

## M5 — Engineering Intelligence
Deep code + CI/CD + ITSM + architecture rules.

## M6 — Trusted AI
Retrieval router + GraphRAG + evidence.

## M7 — Federation
Catalog + live sources + knowledge products.

## M8 — Governed Agents
Agent runtime + MCP governance + firewall.

## M9 — Enterprise
SSO/RBAC/HA/DR/hardening.

## M10 — Analytics/Ecosystem
Simulation + SDK + domain packs.

---

# 22. Commercial Pilot Readiness

Before the first paid pilot, complete at minimum:

- Phase 1 fully.
- Critical subset of Phase 2:
  - provenance,
  - evidence,
  - ontology versioning,
  - quality dashboard.
- Critical subset of Phase 3:
  - impact analysis,
  - requirement-to-code traceability.
- Basic local GraphRAG from Phase 4.
- deployment/backup/restore.
- offline installation.
- license/SBOM/security documentation.

Do not wait for every advanced agent/RAG pattern.

---

# 23. Enterprise GA Readiness

Before broad enterprise sale, complete:

- Phase 2.
- Phase 3.
- Phase 4 core.
- Phase 7 security/operations.
- validated scale benchmark.
- upgrade/rollback.
- support/diagnostics.
- documentation.
- compatibility matrix.
- penetration/security testing.

Federation, advanced agents and simulation can remain licensed/additional modules if desired.

---

# 24. “Competitor Con → Our Pro” Mapping

| Observed trade-off | Product response |
|---|---|
| Cloud-only managed graph | Offline/on-prem first |
| Property graph with semantics as extension | Native semantic control plane + property graph runtime |
| RDF platform weak in code intelligence | Deep AST/code/runtime digital thread |
| Heavy production footprint | Progressive laptop → server → distributed profiles |
| Add-on fragmentation | Coherent core + optional advanced modules |
| AI answers without durable evidence | Mandatory Evidence Manifest |
| Ontology changes outside DevOps | Ontology GitOps + CI |
| Data catalog detached from source execution | Catalog linked to live graph paths |
| GraphRAG indexing expense | deterministic-first + incremental graph/community updates |
| Agent autonomy risk | bounded tools, trust zones, human policies |
| Proprietary lock-in | canonical IDs + RDF/JSON-LD/GraphML/JSON export |
| Stale graph | CDC + freshness SLO + incremental ingestion |
| Opaque data-quality score | multidimensional quality SLOs |
| Hard-to-explain inference | claim/evidence/truth-resolution model |
| Generic graph visualization | task-specific business/developer/architecture experiences |

---

# 25. Delivery Backlog Structure

Epic groups:

- EPIC-FOUNDATION
- EPIC-CONNECTORS
- EPIC-HUGEGRAPH
- EPIC-ONTOLOGY
- EPIC-PROVENANCE
- EPIC-QUALITY
- EPIC-CODEGRAPH
- EPIC-DIGITALTHREAD
- EPIC-QUERY
- EPIC-SEARCH
- EPIC-RAG
- EPIC-AGENTS
- EPIC-MCP
- EPIC-WEB
- EPIC-VSCODE
- EPIC-FEDERATION
- EPIC-CATALOG
- EPIC-SECURITY
- EPIC-OBSERVABILITY
- EPIC-HA
- EPIC-SDK
- EPIC-DOMAINPACKS

Every ticket should include the originating `GAP-*` requirement.

---

# 26. Recommended First 90-Day Build Focus

This is intentionally narrower than the complete roadmap.

### Days 1–30
- canonical contracts,
- HugeGraph,
- Jira,
- Git/code parser,
- provenance,
- basic graph query.

### Days 31–60
- cross-linking,
- impact analysis,
- user/admin UI,
- VS Code,
- validation,
- backup/restore.

### Days 61–90
- evidence service,
- ontology versioning,
- graph quality,
- local GraphRAG,
- MCP read tools,
- end-to-end pilot demo.

At Day 90, evaluate actual pilot feedback before accelerating advanced agents.

---

# 27. Architecture Rule

The product should have **one semantic truth architecture**, not separate mini-products for graph, RAG, agents and UI.

All layers must converge on:

`Canonical Identity + Ontology + Provenance + Evidence + Policy + Version`

That is the architectural invariant that keeps the platform coherent as it grows.

---

# 28. Final Implementation Principle

Do not attempt to beat competitors by implementing all their features at once.

Beat the trade-offs by sequencing:

1. **trustworthy graph**, then
2. **semantic governance**, then
3. **engineering intelligence**, then
4. **evidence-backed AI**, then
5. **enterprise operations**, then
6. **ecosystem scale**.

This creates a product that can be sold earlier while preserving a path toward the broader platform vision.
