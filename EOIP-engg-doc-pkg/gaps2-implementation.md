# gaps2-implementation.md
## EOIP — Phase-by-Phase Implementation Plan for Enterprise Knowledge Acquisition, Graph Evolution & Next-Generation Intelligence

**Companion:** `gaps2-requirements.md`  
**Relationship:** Additive to the existing EOIP MVP implementation plan and `gaps-implementation.md`  
**Primary database:** Apache HugeGraph  
**Deployment:** Local/on-premises, Docker-first, no required cloud dependency  
**Strategy:** Build acquisition/synchronization foundations first; add new sources in waves; then add temporal intelligence and moonshot capabilities.

---

# 1. Implementation Objective

Implement the new `G2-*` requirements without fragmenting the existing EOIP architecture.

The implementation must preserve these invariants:

1. Connectors do not write HugeGraph directly.
2. All sources emit canonical `SourceEvent` records.
3. The common pipeline owns canonicalization, identity, relationship generation, validation, provenance and graph mutation.
4. Initial source connection establishes a baseline.
5. Normal operation processes deltas/events rather than rebuilding everything.
6. Historical relationships are expired/versioned, not silently erased.
7. Raw high-volume telemetry stays in source systems; EOIP stores semantic knowledge/evidence pointers.
8. AI inference is secondary to deterministic evidence.
9. New services are introduced only when load/operational requirements justify them.
10. Every phase leaves EOIP runnable and demonstratable.

---

# 2. Phase Overview

| Phase | Theme | Outcome |
|---|---|---|
| G2-P0 | Contract & architecture alignment | G2 additions fit current EOIP core |
| G2-P1 | EKAF core | Source registry + connector/crawler framework |
| G2-P2 | Baseline + incremental graph evolution | Safe continuous sync/versioning |
| G2-P3 | Source Wave 1 | Jira + Git/GitLab/GitHub + source + files |
| G2-P4 | Source Wave 2 | Confluence + ServiceNow + API portals |
| G2-P5 | Source Wave 3 | CI/CD + observability + runtime + SBOM |
| G2-P6 | Expanded semantic digital twin | New graph domains + intent-to-runtime |
| G2-P7 | Temporal/architecture/process intelligence | Time Machine + conformance + process mining |
| G2-P8 | Knowledge health & governed AI | immune system + ontology proposals + capsules |
| G2-P9 | Simulation & causal intelligence | counterfactual twin + causal hypotheses |
| G2-P10 | Diamond-standard UX & production hardening | lenses, playback, scale, operational maturity |

The sequence is dependency-oriented, not a rigid calendar. Individual source adapters can move earlier when a pilot customer requires them.

---

# 3. G2-P0 — Contract & Architecture Alignment

## Goal
Extend the existing EOIP architecture cleanly before implementing new crawlers.

## Requirements
- G2-ARCH-001..015
- G2-EKAF-003
- G2-EVOL-009
- G2-EVENT-001

## Tasks

### G2-T0001 — Audit current contracts
Inspect existing:
- SourceEvent
- NormalizedEntity
- NormalizedRelationship
- GraphMutation
- Evidence
- AuditEvent
- ontology/version metadata.

**Rule:** extend rather than duplicate.

**Acceptance:** document exact compatibility changes.

### G2-T0002 — SourceEvent v2
Add fields required for:
- operation,
- source version,
- event time,
- content hash,
- cursor,
- permission metadata,
- payload reference.

Provide v1→v2 compatibility adapter if existing code already uses v1.

### G2-T0003 — Canonical revision model
Add:
- revision ID,
- valid_from,
- valid_to,
- observed_at,
- is_current,
- previous_revision,
- source_version.

Decide whether revision data resides directly on entity/edge properties, revision vertices, or a hybrid based on HugeGraph query/update behavior. Document ADR.

### G2-T0004 — Source Registry schema
Implement contract and persistence model for source configurations excluding secret values.

### G2-T0005 — Capability interfaces
Define interfaces:

```python
class SourceConnector:
    def capabilities(self) -> SourceCapabilities: ...
    def discover(self, scope) -> DiscoveryResult: ...
    def baseline(self, checkpoint=None) -> Iterator[SourceEvent]: ...
    def poll_changes(self, checkpoint) -> Iterator[SourceEvent]: ...
    def handle_event(self, event) -> Iterator[SourceEvent]: ...
    def fetch_record(self, ref) -> SourceEvent: ...
    def health(self) -> ConnectorHealth: ...
```

### G2-T0006 — Traceability
Create G2 requirement-to-task/test mapping.

## Tests
- schema compatibility,
- serialization,
- source-event idempotency,
- revision metadata.

## Exit Criteria
No new source integration is allowed until common contracts and revision semantics are agreed.

---

# 4. G2-P1 — Enterprise Knowledge Acquisition Fabric Core

## Goal
Create one reusable acquisition/synchronization framework.

## Requirements
- G2-EKAF-001..030
- G2-SEC-CRAWL-001..012
- G2-OBS-001..002

## Workstream A — Source Registry

### G2-T0101
Backend CRUD/read operations for source configuration.

### G2-T0102
Secret references separate from config.

### G2-T0103
Source capability and compatibility metadata.

### G2-T0104
Admin Source Registry UI.

---

## Workstream B — Scheduler

### G2-T0110
Implement local job scheduler abstraction supporting:
- baseline,
- poll,
- reconcile,
- replay.

Do not add a distributed queue unless measurements require it.

### G2-T0111
Per-source concurrency/rate-limit configuration.

### G2-T0112
Pause/resume.

---

## Workstream C — Webhook Gateway

### G2-T0120
Authenticated/validated webhook endpoints by source type.

### G2-T0121
Deduplication key strategy.

### G2-T0122
Store event receipt before asynchronous processing when practical.

### G2-T0123
Return source-appropriate response quickly; downstream work should not block webhook delivery.

---

## Workstream D — Controlled Web Crawler

### G2-T0130
Crawl scope configuration:
- host allowlist,
- path allowlist/exclude,
- depth,
- page limit,
- MIME types,
- size limits.

### G2-T0131
Crawl frontier and canonical URL detection.

### G2-T0132
HTML extraction:
- title,
- headings,
- links,
- main text,
- metadata.

### G2-T0133
SSRF protection.

### G2-T0134
No arbitrary redirect escape from allowlist.

### G2-T0135
Content hashing/deduplication.

---

## Workstream E — DLQ / Replay

### G2-T0140
DLQ store.

### G2-T0141
Replay one/many.

### G2-T0142
Admin replay console.

---

## Workstream F — Discovery / Dry Run

### G2-T0150
Source discovery operation.

### G2-T0151
Preview estimated entity counts/types.

### G2-T0152
Mapping dry run produces canonical mutation preview.

### G2-T0153
Source onboarding wizard.

---

## Exit Criteria
A synthetic connector and generic web/file connector must both run through the same EKAF pipeline and produce equivalent SourceEvent semantics.

---

# 5. G2-P2 — Baseline, Incremental Sync & Graph Evolution

## Goal
Implement the core behavior the user requested: establish a baseline once, then add changes without breaking graph history.

## Requirements
- G2-SYNC-001..014
- G2-EVOL-001..016
- G2-JOURNAL-001..006
- G2-EVENT-001..007
- G2-REL-001..008

---

## Workstream A — Baseline Controller

### G2-T0201
Baseline run state machine:

`CREATED → DISCOVERING → FETCHING → MAPPING → VALIDATING → MUTATING → VERIFYING → COMPLETE/FAILED`

### G2-T0202
Store baseline manifest:
- source scope,
- versions,
- mapping/parser/ontology versions,
- counts,
- failures,
- checkpoint.

### G2-T0203
Baseline resume from safe checkpoint.

---

## Workstream B — Incremental Change Detector

### G2-T0210
Content hash comparison.

### G2-T0211
Source-version comparison.

### G2-T0212
Delta classifier:
- create,
- update,
- delete,
- relationship update,
- permission update.

### G2-T0213
Skip unchanged content before expensive parsing/model use.

---

## Workstream C — Graph Evolution Engine

### G2-T0220
Implement current/historical edge lifecycle.

### G2-T0221
On relationship replacement:
1. validate new assertion,
2. close old validity range,
3. create new revision,
4. link provenance,
5. emit change event.

### G2-T0222
Entity property revision policy.

### G2-T0223
Historical state query API.

### G2-T0224
Graph diff algorithm.

### G2-T0225
Late event conflict resolution.

---

## Workstream D — Semantic Change Journal

### G2-T0230
Append local change record after graph mutation.

### G2-T0231
Expose journal API/UI.

### G2-T0232
Implement replay cursor.

---

## Workstream E — Semantic Event Bus

### G2-T0240
Start with process-local durable-aware pub/sub abstraction.

### G2-T0241
Publish event only after mutation commit.

### G2-T0242
Implement first consumers:
- quality recalculation,
- semantic cache invalidation,
- admin timeline.

### G2-T0243
Broker adapter interface for future scale.

---

## Workstream F — Reconciliation

### G2-T0250
Source-specific reconciliation interface.

### G2-T0251
Compare IDs/hash/version/cursor with current state.

### G2-T0252
Repair missed changes.

### G2-T0253
Reconciliation report.

---

## Critical Tests

1. Baseline 1,000 records.
2. Re-run baseline: no duplicates.
3. Change one source record.
4. Incremental sync mutates only affected canonical facts.
5. Delete source relationship.
6. Old relationship visible historically but not current.
7. Duplicate webhook safe.
8. Event delivered late after newer event does not corrupt state.
9. Crash before checkpoint and restart.
10. Reconciliation repairs intentionally dropped event.

## Exit Criteria
The baseline→delta lifecycle is reliable before additional enterprise connectors are scaled out.

---

# 6. G2-P3 — Source Wave 1: Jira, Git, GitLab, GitHub, Code, Files

## Goal
Apply EKAF to high-value engineering systems.

## Requirements
- G2-SRC-JIRA-001..006
- G2-SRC-GL-001..004
- G2-SRC-GH-001..004
- G2-SRC-CODE-001..005
- G2-SRC-WEB-001..005

---

## 6.1 Jira

### G2-T0301
Upgrade existing Jira adapter to:
- baseline,
- delta,
- optional webhook,
- changelog.

### G2-T0302
Build temporal status/assignment/ownership relationships.

### G2-T0303
Issue-link normalization.

### G2-T0304
Jira compatibility fixtures.

---

## 6.2 GitLab

### G2-T0310
Project/group discovery.

### G2-T0311
Webhook adapter.

### G2-T0312
MR/pipeline/job/release mapping.

### G2-T0313
Pages/wiki/documentation ingestion when enabled.

---

## 6.3 GitHub

### G2-T0320
GitHub source adapter.

### G2-T0321
Webhook adapter.

### G2-T0322
PR/actions/release graph mappings.

### G2-T0323
Pages/docs support if configured.

---

## 6.4 Code Incremental Parsing

### G2-T0330
Determine changed files from commits.

### G2-T0331
Reparse only changed files.

### G2-T0332
Expire/rebuild impacted static call/import edges.

### G2-T0333
Preserve symbol history by revision/commit.

---

## 6.5 Generic file/web

### G2-T0340
Local file crawler.

### G2-T0341
Controlled HTTP crawler.

### G2-T0342
Document parser isolation and size limits.

---

## Demo
1. Connect Jira + GitLab/GitHub/local repo.
2. Baseline.
3. Create/change a work item and commit fixture.
4. Incremental update.
5. Display graph timeline and evidence.

---

# 7. G2-P4 — Source Wave 2: Confluence, ServiceNow & API Portals

## Goal
Expand from engineering code graph into enterprise knowledge/ITSM/contracts.

## Requirements
- G2-SRC-CONF-001..005
- G2-SRC-SNKB-001..003
- G2-SRC-SNOW-001..006
- G2-SRC-API-001..006
- G2-GRAPH-API-001..003

---

## 7.1 Confluence

### G2-T0401
Space/page discovery.

### G2-T0402
Page baseline/incremental sync.

### G2-T0403
Version and page hierarchy mapping.

### G2-T0404
Attachment extraction.

### G2-T0405
Document-to-service/API/code semantic link candidates.

---

## 7.2 ServiceNow

Implement as separate logical source modules on common client/auth infrastructure.

### G2-T0410 — KB
KB/article/category/version.

### G2-T0411 — Incident
Incident/assignment/affected CI/service.

### G2-T0412 — Problem
Problem/RCA/incident relationships.

### G2-T0413 — Change
Change/approval/window/CI/service.

### G2-T0414 — CMDB
Authorized CI topology.

### G2-T0415
Temporal state transitions.

### G2-T0416
Reconciliation tests for state changes.

---

## 7.3 API Portal / Contracts

### G2-T0420
OpenAPI parser.

### G2-T0421
GraphQL schema parser.

### G2-T0422
AsyncAPI parser.

### G2-T0423
protobuf/JSON Schema adapters.

### G2-T0424
API compatibility diff.

### G2-T0425
Link endpoint to code symbol using route/framework extraction.

### G2-T0426
Link consumers from code/dependency/static configuration where deterministic.

---

## Exit Criteria
EOIP can traverse:
`Requirement → Code → API → Documentation → Change/Incident`.

---

# 8. G2-P5 — Source Wave 3: CI/CD, Observability, Runtime, SBOM

## Goal
Connect implementation knowledge to actual runtime and operational evidence.

## Requirements
- G2-SRC-CICD-001..004
- G2-SRC-KIB-001..005
- G2-SRC-DD-001..004
- G2-SRC-GRAF-001..003
- G2-SRC-OTEL-001..005
- G2-SRC-RUNTIME-001..003
- G2-SRC-SBOM-001..004
- G2-GRAPH-OBS-001..003
- G2-GRAPH-RUNTIME-001..003
- G2-GRAPH-SEC-001..003
- G2-TEL-001..008

---

## 8.1 CI/CD

### G2-T0501
Connector adapter interface for pipeline systems.

### G2-T0502
Map commit→build→artifact→deployment.

### G2-T0503
Link tests/results.

### G2-T0504
Deployment state transitions.

---

## 8.2 Kibana

### G2-T0510
Saved object/dashboard/data view metadata adapter.

### G2-T0511
Configured bounded query evidence fetch.

### G2-T0512
Log fingerprint/error signature extraction.

### G2-T0513
Never bulk-copy log index.

---

## 8.3 Datadog

### G2-T0520
Service/catalog/APM topology adapter.

### G2-T0521
Dashboard/monitor/SLO metadata.

### G2-T0522
Bounded evidence sampling.

### G2-T0523
Runtime dependency confidence/time-window logic.

---

## 8.4 Grafana

### G2-T0530
Dashboard/panel/folder metadata.

### G2-T0531
Datasource/query reference extraction.

### G2-T0532
Panel→metric→service mappings.

---

## 8.5 OpenTelemetry

### G2-T0540
OTLP/normalized telemetry adapter.

### G2-T0541
Resource→Service/Environment mapping.

### G2-T0542
Trace-derived service call graph.

### G2-T0543
Exemplar retention.

---

## 8.6 Runtime

### G2-T0550
Docker/Kubernetes metadata adapters as configured.

### G2-T0551
Image digest→artifact→commit linkage.

---

## 8.7 SBOM

### G2-T0560
CycloneDX parser.

### G2-T0561
SPDX parser.

### G2-T0562
Package dependency graph.

### G2-T0563
Vulnerability relationship adapter from configured scanner input.

---

## Critical Guardrail
Benchmark semantic aggregation before increasing telemetry scope. HugeGraph remains a knowledge graph, not raw log/metric storage.

---

# 9. G2-P6 — Expanded Semantic Digital Twin

## Goal
Connect new sources into coherent enterprise graph domains.

## Requirements
- G2-GRAPH-API-*
- G2-GRAPH-OBS-*
- G2-GRAPH-RUNTIME-*
- G2-GRAPH-SEC-*
- G2-GRAPH-TEST-*
- G2-GRAPH-DEC-*
- G2-GRAPH-PROC-*
- G2-GRAPH-BIZ-*
- G2-TWIN-001..005
- G2-I2R-001..005

---

## Workstream A — Test Intelligence

### G2-T0601
Map tests to code symbols through framework/static/coverage evidence.

### G2-T0602
Map test runs to builds/releases.

### G2-T0603
Change-based test selection API.

---

## Workstream B — Decision Graph

### G2-T0610
ADR/document decision extractor (deterministic structure first).

### G2-T0611
Decision/rationale/alternative model.

### G2-T0612
Link decisions to architecture/code.

---

## Workstream C — Business Intent

### G2-T0620
Business Objective/Capability ontology module.

### G2-T0621
Mapping configuration from enterprise source records.

### G2-T0622
Reverse runtime→capability traversal.

---

## Workstream D — Digital Twin View

### G2-T0630
Meta-query that classifies facts:
- intended,
- implemented,
- observed,
- inferred.

### G2-T0631
Digital-thread coverage metrics.

### G2-T0632
Missing-link detector.

---

## Exit Criteria
Demonstrate:
`Business Capability → Requirement → Decision → Code → API → Test → Build → Deployment → Runtime → Incident`.

---

# 10. G2-P7 — Temporal, Architecture & Process Intelligence

## Goal
Turn the graph from a current-state knowledge base into a time-aware engineering intelligence system.

## Requirements
- G2-TIME-001..007
- G2-ARCHC-001..009
- G2-PM-001..005
- G2-KD-001..006
- G2-SLO-001..005
- G2-QOP-001..009

---

## 10.1 Enterprise Time Machine

### G2-T0701
As-of graph query service.

### G2-T0702
T1↔T2 semantic diff service.

### G2-T0703
Release snapshot markers.

### G2-T0704
Timeline Lens.

### G2-T0705
Historical Evidence Lens.

---

## 10.2 Architecture Conformance

### G2-T0710
Architecture rule DSL/schema.

### G2-T0711
Compiler to graph-query/validation plan.

### G2-T0712
Intended/implemented/runtime comparison engine.

### G2-T0713
Web finding UI.

### G2-T0714
VS Code findings.

### G2-T0715
CI exit-code/report mode.

---

## 10.3 Process Mining

### G2-T0720
Normalize event-log/case data.

### G2-T0721
Discover observed process paths.

### G2-T0722
Compare to designed flow.

### G2-T0723
Deviation/bottleneck report.

---

## 10.4 Knowledge Debt

### G2-T0730
Knowledge Debt Finding model.

### G2-T0731
Rule pack.

### G2-T0732
Trend aggregation.

### G2-T0733
Knowledge Health Lens.

---

## 10.5 Knowledge SLO

### G2-T0740
SLO DSL/config.

### G2-T0741
Scheduled/event-driven evaluator.

### G2-T0742
Breach findings.

### G2-T0743
Admin SLO dashboard.

---

## 10.6 Native Query Operators

### G2-T0750
Structured `WHY`.

### G2-T0751
Structured `WHY NOT`.

### G2-T0752
Structured `WHAT CHANGED`.

### G2-T0753
`WHEN/WHO/WHERE/HOW`.

`WHAT IF` becomes full implementation in G2-P9.

---

# 11. G2-P8 — Knowledge Health & Governed AI

## Goal
Add proactive maintenance and safer AI consumption without allowing uncontrolled graph/ontology mutation.

## Requirements
- G2-IMMUNE-001..013
- G2-OEVO-001..006
- G2-CAP-001..006

---

## 11.1 Knowledge Immune System

### G2-T0801
Rule-driven knowledge anomaly detectors.

### G2-T0802
Statistical anomaly detectors only after sufficient baseline history.

### G2-T0803
Quarantine/review queue integration.

### G2-T0804
Repair recommendation model.

### G2-T0805
No automatic trusted-fact rewrite.

---

## 11.2 Ontology Evolution Proposals

### G2-T0810
Cluster recurring unmapped entity/relation patterns.

### G2-T0811
Generate candidate ontology proposal.

### G2-T0812
Run impact/backfill simulation.

### G2-T0813
Human review UI.

### G2-T0814
Accepted proposal → Ontology GitOps branch/PR artifact.

---

## 11.3 Knowledge Capsules

### G2-T0820
Capsule manifest.

### G2-T0821
Bounded traversal builder.

### G2-T0822
Trust/security filtering.

### G2-T0823
Evidence bundling.

### G2-T0824
Agent/RAG context adapter.

---

## Exit Criteria
An AI agent can receive a reproducible bounded service/incident/release capsule instead of unrestricted enterprise context.

---

# 12. G2-P9 — Counterfactual Twin & Causal Intelligence

## Goal
Support safe “what if?” reasoning and evidence-grounded causal hypotheses.

## Requirements
- G2-SIM-001..007
- G2-CAUSE-001..006
- G2-QOP-003

---

## 12.1 Simulation Workspace

### G2-T0901
Create immutable base graph-version reference.

### G2-T0902
Overlay hypothetical mutation set.

### G2-T0903
Simulation query layer combines base + overlay.

### G2-T0904
Run impact/conformance/quality/test analyses.

### G2-T0905
Simulation comparison UI.

### G2-T0906
Persist reproducible simulation manifest.

---

## 12.2 What-If Operator

### G2-T0910
Translate structured/natural-language intent into proposed mutation plan.

### G2-T0911
Require user confirmation of parsed scenario before costly execution.

### G2-T0912
Return affected entities by category and graph path.

---

## 12.3 Causal Hypothesis Engine

### G2-T0920
Generate correlation candidates from temporal graph.

### G2-T0921
Check prerequisite evidence/time order.

### G2-T0922
Represent alternatives.

### G2-T0923
Never emit `HUMAN_CONFIRMED_CAUSE` automatically.

### G2-T0924
Reviewer UI.

---

## Validation
Use synthetic incident scenarios with known causal ground truth before any production claims.

---

# 13. G2-P10 — Diamond-Standard UX & Production Hardening

## Goal
Make the expanded platform understandable and usable without graph expertise.

## Requirements
- G2-UX-LENS-001..003
- G2-UX-GRAPH-001..016
- G2-UX-PLAY-001..005
- G2-ADMIN-001..017
- G2-VSC-001..008
- performance/reliability hardening

---

## 13.1 Lens Framework

Implement a shared context state:

```ts
type KnowledgeContext = {
  rootEntities: string[];
  graphVersion?: string;
  asOf?: string;
  domains: string[];
  trustThreshold?: string;
  filters: Record<string, unknown>;
};
```

Switching lenses reuses this context.

---

## 13.2 Required Lens Delivery Order

1. Search
2. Graph
3. Evidence
4. Impact
5. Timeline
6. Change
7. Architecture
8. Runtime
9. Requirement
10. Trust
11. Security
12. Release
13. Process
14. Knowledge Health
15. Simulation
16. Agent
17. Decision
18. API
19. Test
20. Ontology

---

## 13.3 Graph Canvas

Use level-of-detail rendering:
- compact clusters at zoomed-out state,
- expand neighbors on demand,
- cap visible nodes,
- server-side path/neighborhood queries.

Never attempt to render a large enterprise graph at once.

---

## 13.4 Graph Playback

### G2-T1030
Temporal event stream for selected incident/release.

### G2-T1031
Playback UI.

### G2-T1032
Source-evidence side panel.

### G2-T1033
Export evidence timeline.

---

## 13.5 Production Hardening

### G2-T1040
Load tests for connector waves.

### G2-T1041
Historical query benchmark.

### G2-T1042
Graph diff benchmark.

### G2-T1043
Reconciliation chaos/failure testing.

### G2-T1044
Long-running source sync test.

### G2-T1045
Upgrade/migration test across graph revisions.

### G2-T1046
Backup/restore with checkpoints/journal.

---

# 14. Cross-Phase Source Adapter Template

Every new source adapter should include:

```text
/connectors/<source>/
  client.py
  auth.py
  capabilities.py
  discovery.py
  baseline.py
  delta.py
  webhook.py
  mapping.py
  fixtures/
  tests/
  README.md
```

Only files relevant to source capability need exist; do not create meaningless stubs.

---

# 15. Connector Implementation Checklist

For every source:

- [ ] supported product/API versions documented
- [ ] authentication mode documented
- [ ] minimum permissions documented
- [ ] source scopes configurable
- [ ] discovery implemented
- [ ] baseline implemented
- [ ] incremental sync implemented or limitation documented
- [ ] delete semantics implemented
- [ ] webhook implemented if supported/needed
- [ ] polling fallback
- [ ] reconciliation
- [ ] pagination
- [ ] rate limiting
- [ ] retries/backoff
- [ ] content hashing
- [ ] checkpointing
- [ ] dry run
- [ ] replay
- [ ] DLQ
- [ ] schema drift
- [ ] mapping version
- [ ] tests
- [ ] telemetry
- [ ] security review
- [ ] fixtures
- [ ] operator docs

---

# 16. Graph Evolution Mutation Algorithm

Pseudo-flow:

```text
receive SourceEvent
    ↓
validate event
    ↓
lookup current source/canonical revision
    ↓
if same content/version:
    ACK / no-op
else:
    map proposed canonical facts
    ↓
identity resolution
    ↓
validate proposed mutation
    ↓
compute graph semantic diff
    ↓
begin bounded mutation unit
    ↓
expire superseded assertions
create/update new assertions
attach provenance/evidence
update meta/version
    ↓
commit
    ↓
append change journal
    ↓
publish semantic events
    ↓
advance checkpoint
```

If mutation fails before commit:
- no checkpoint advance,
- no success event,
- source event remains retryable.

---

# 17. Historical Relationship Strategy

Example:

```text
Service-A --DEPENDS_ON--> Service-B
valid_from: 2026-05-01
valid_to:   2026-09-30
is_current: false

Service-A --DEPENDS_ON--> Service-C
valid_from: 2026-10-01
valid_to:   null
is_current: true
```

Current traversal returns C.  
Historical traversal for July returns B.

This behavior must be covered by integration tests.

---

# 18. Telemetry Aggregation Strategy

## Logs
Store:
- fingerprint,
- normalized error signature,
- count/window,
- first/last seen,
- service,
- deployment,
- bounded exemplars,
- source query/ref.

## Metrics
Store:
- metric definition,
- dashboard/panel use,
- service association,
- SLO/monitor relationship,
- exceptional summarized windows only when needed.

## Traces
Store:
- service dependency edge,
- observation window,
- request count/sample count,
- latency summary if useful,
- trace exemplar IDs.

The raw observability system remains authoritative for detailed telemetry.

---

# 19. Versioning Strategy

Maintain separate versions:

- source connector version,
- source record version,
- parser version,
- mapping version,
- ontology version,
- schema version,
- graph logical version,
- retrieval index version,
- GraphRAG summary version.

Do not collapse these into one version number.

---

# 20. Recommended Persistence Additions

Keep HugeGraph authoritative.

Use local filesystem/object-style volumes for:
- raw capture,
- DLQ,
- large attachments,
- replay fixtures,
- backups,
- evidence manifests.

Use relational/embedded metadata storage only if existing architecture already needs it; do not introduce one solely for convenience without an ADR.

Semantic event bus starts as an abstraction over local process/durable journal. Introduce Kafka/NATS/Redpanda-like infrastructure only after measured throughput/consumer needs justify it and only if on-prem deployment remains supported.

---

# 21. UI Delivery Principle

Every advanced GUI capability must be backed by a real query/service.

Bad:
- hardcoded timeline,
- fake graph playback,
- mock simulation.

Required:
`UI → API → query/service → HugeGraph/source evidence`.

---

# 22. AI Use by Phase

## P0–P5
AI optional. Focus deterministic extraction/sync.

## P6–P7
AI may assist:
- semantic mapping suggestions,
- documentation links,
- natural-language query planning.

## P8
AI may propose:
- ontology evolution,
- knowledge repair,
- capsule summaries.

## P9
AI may help interpret simulation/causal evidence but cannot invent graph state.

All AI outputs remain evidence constrained.

---

# 23. Test Matrix

| Capability | Unit | Contract | Integration | E2E | Security | Performance |
|---|---:|---:|---:|---:|---:|---:|
| Connector SDK | ✓ | ✓ | ✓ |  | ✓ |  |
| Jira/Git | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Confluence/SNOW | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Observability | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Graph Evolution | ✓ |  | ✓ | ✓ |  | ✓ |
| Change Journal | ✓ |  | ✓ | ✓ | ✓ | ✓ |
| Event Bus | ✓ | ✓ | ✓ | ✓ |  | ✓ |
| Time Machine | ✓ |  | ✓ | ✓ |  | ✓ |
| Architecture Conformance | ✓ | ✓ | ✓ | ✓ |  | ✓ |
| Knowledge Immune | ✓ |  | ✓ | ✓ | ✓ |  |
| Simulation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| GUI Lenses | ✓ |  | ✓ | ✓ | ✓ | ✓ |

---

# 24. Phase Exit Gates

## Gate 0 — Contract Integrity
No duplicate competing SourceEvent/canonical model.

## Gate 1 — Acquisition Integrity
At least one API connector and one crawler/file source work through EKAF.

## Gate 2 — Incremental Integrity
Baseline + update + delete + replay + reconciliation pass.

## Gate 3 — Engineering Sources
Jira/Git/code graph is continuously synchronized.

## Gate 4 — Enterprise Sources
Confluence/ServiceNow/API contract paths work.

## Gate 5 — Runtime Knowledge
Observability/runtime data is semantically linked without raw telemetry explosion.

## Gate 6 — Digital Twin
Intent-to-runtime path works.

## Gate 7 — Temporal Intelligence
As-of/diff/architecture/process queries work.

## Gate 8 — Knowledge Health
Findings/proposals are evidence-backed and non-destructive.

## Gate 9 — Simulation
Counterfactual run is isolated/reproducible.

## Gate 10 — UX/Operations
Advanced lenses are production-backed and operationally supportable.

---

# 25. Commercial Pilot Subset

A customer pilot does not require completion through P10.

Recommended pilot minimum:

- G2-P0
- G2-P1
- G2-P2
- G2-P3
- selected G2-P4 connectors relevant to customer
- one observability source from G2-P5
- basic Time Machine
- basic Knowledge SLO
- current Web/Admin/VS Code experience

Pilot demo:

```text
Jira requirement
 → commit
 → code symbol
 → API
 → build/deployment
 → runtime service
 → incident/dashboard
 → documentation/owner
```

Then:
- update one source,
- show incremental graph evolution,
- compare historical state,
- show evidence.

---

# 26. First Recommended Implementation Sprint Sequence

## Sprint/Iteration 1
Source Registry + SourceEvent v2 + capability contracts.

## Sprint/Iteration 2
Baseline controller + checkpoints + dry run.

## Sprint/Iteration 3
Graph revision/edge expiry + historical query.

## Sprint/Iteration 4
Change Journal + local semantic events.

## Sprint/Iteration 5
Upgrade Jira/Git/GitLab to EKAF.

## Sprint/Iteration 6
Reconciliation + late/duplicate event tests.

## Sprint/Iteration 7
GitHub + controlled crawler.

## Sprint/Iteration 8
Confluence.

## Sprint/Iteration 9
ServiceNow KB/Incident/Change.

## Sprint/Iteration 10
API contracts.

After this point, select observability connectors based on actual pilot priorities.

---

# 27. AI Coding Agent Work Protocol

For each task, the implementation agent SHALL output/update:

1. requirement IDs,
2. design/ADR if architecture changes,
3. files changed,
4. contracts changed,
5. migration impact,
6. implementation,
7. unit tests,
8. integration tests,
9. failure handling,
10. telemetry,
11. security notes,
12. traceability,
13. demo/acceptance evidence.

The agent SHALL stop and report a blocker instead of fabricating source behavior when:
- API documentation/fixture is unavailable,
- credentials are unavailable,
- source version is unsupported,
- an assumption would change canonical semantics.

---

# 28. Definition of Done

A phase is complete only when:

- all mandatory requirements are implemented or explicitly deferred,
- schema migrations are versioned,
- baseline and incremental behavior is demonstrated,
- current/historical semantics are correct,
- source failures are recoverable,
- tests pass from clean checkout,
- Docker startup is reproducible,
- no mandatory cloud dependency exists,
- no uncontrolled external data egress exists,
- docs/traceability are current,
- UI demonstrates real backend state.

---

# 29. Final Build Order Principle

Do **not** begin with the moonshot GUI or autonomous agents.

Build in this order:

```text
Acquire reliably
    ↓
Synchronize incrementally
    ↓
Version safely
    ↓
Establish provenance
    ↓
Build cross-domain graphs
    ↓
Expose historical/intelligence queries
    ↓
Add proactive knowledge health
    ↓
Add controlled AI
    ↓
Add simulation
    ↓
Polish next-generation experiences
```

This order turns EOIP into a trustworthy live enterprise knowledge twin rather than a visually impressive but unreliable graph demo.
