# gaps2-requirements.md
## EOIP — Enterprise Knowledge Acquisition, Graph Evolution & Next-Generation Intelligence Requirements

**Project:** EOIP — Enterprise Ontology & Intelligence Platform  
**Document type:** Additive gap requirements / next-generation capability specification  
**Relationship:** Extends the existing EOIP engineering documentation package, `gaps-requirements.md`, and the current MVP/phase roadmap. It does not replace the existing requirements.  
**Primary deployment:** On-premises / self-hosted / air-gapped capable  
**Primary graph database:** Apache HugeGraph  
**Packaging:** Docker-first; Docker Compose for development/MVP; distributed deployment only when justified  
**Cloud dependency:** None required  
**AI stance:** Local-first, deterministic-first, evidence-backed  
**Status:** Engineering-ready requirement baseline for AI-assisted implementation

---

# 1. Purpose

EOIP already defines enterprise ontology, graph construction, canonical entities/relationships, provenance, temporal graph, GraphRAG, agents, MCP, web/admin experiences, VS Code integration, security, observability, testing and phased delivery.

This document adds the capabilities required to evolve EOIP into a continuously synchronized, time-aware, evidence-backed **enterprise digital knowledge twin**.

The major additions are:

1. A first-class **Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF)**.
2. Broad source harvesting across enterprise systems.
3. Baseline crawl + continuous incremental synchronization.
4. A **Graph Evolution Engine** that versions entities and relationships without losing history.
5. A local **Semantic Change Journal** and **Semantic Event Bus**.
6. API/contract, observability, runtime, security/supply-chain, test, decision, process and business-intent graph domains.
7. Runtime knowledge from Kibana, Datadog, Grafana and OpenTelemetry without copying all raw telemetry into HugeGraph.
8. Enterprise Time Machine.
9. Counterfactual / what-if enterprise twin.
10. Architecture conformance and semantic architecture compiler.
11. Knowledge health / “immune system”.
12. Ontology evolution proposals with human approval.
13. Causal-hypothesis intelligence.
14. Process mining.
15. Knowledge Capsules.
16. Native WHY / WHY NOT / WHAT IF / WHAT CHANGED query semantics.
17. Knowledge Debt and graph-native knowledge SLOs.
18. Intent-to-runtime traceability.
19. Next-generation GUI lenses, graph playback and semantic visualization.

The guiding goal is:

> EOIP must continuously learn the structure and evolution of an enterprise from configured/authorized sources while preserving provenance, history, trust and relationships.

---

# 2. Non-Negotiable Architectural Principles

## G2-ARCH-001 — One acquisition contract

Every source integration SHALL emit the same canonical `SourceEvent` family and SHALL NOT write HugeGraph directly.

## G2-ARCH-002 — API/event first

Source acquisition SHALL prefer:

1. webhook/event,
2. incremental/delta API,
3. REST/GraphQL/API,
4. repository protocol,
5. filesystem,
6. controlled web crawler,
7. browser automation only as a last resort.

## G2-ARCH-003 — Deterministic first

Deterministic source metadata, parser output, identifiers and explicit relationships SHALL take precedence over AI-inferred relationships.

## G2-ARCH-004 — Preserve source fidelity

Raw source payloads or evidence references SHALL be retained locally according to retention policy so graph facts can be replayed and audited.

## G2-ARCH-005 — HugeGraph is semantic operational truth

Apache HugeGraph SHALL remain the authoritative canonical graph store for operational enterprise knowledge.

## G2-ARCH-006 — No raw telemetry lake in HugeGraph

High-volume logs/metrics/traces SHALL NOT be copied wholesale into HugeGraph. EOIP SHALL store semantic summaries, topology, fingerprints, events, evidence pointers and bounded samples.

## G2-ARCH-007 — No destructive history overwrite

Changes SHALL close/expire old facts and create new revisions rather than silently destroying historical enterprise knowledge.

## G2-ARCH-008 — Current and historical views

Every time-varying domain SHALL support current-state and historical-state queries.

## G2-ARCH-009 — One semantic identity system

All connectors SHALL resolve into canonical IDs independent of source-internal database IDs.

## G2-ARCH-010 — Evidence is mandatory

Every externally sourced or inferred graph mutation SHALL carry provenance/evidence metadata.

## G2-ARCH-011 — AI is not the source of truth

The system SHALL remain useful with local models disabled.

## G2-ARCH-012 — Incremental by default after baseline

After a source baseline is established, normal synchronization SHALL process only new/changed/deleted source records plus periodic reconciliation.

## G2-ARCH-013 — Replayability

EOIP SHALL be able to rebuild derived graph state from captured events/mappings for supported domains.

## G2-ARCH-014 — Source permissions respected

Crawlers/connectors SHALL operate only against explicitly configured/authorized scopes and credentials.

## G2-ARCH-015 — Progressive complexity

MVP/team deployments SHALL remain lightweight. Brokers, separate search clusters, distributed graph components and additional stores SHALL be added only when workload evidence justifies them.

---

# 3. Enterprise Knowledge Acquisition & Synchronization Fabric (EKAF)

EKAF is the unified subsystem responsible for discovering, extracting, normalizing, synchronizing and reconciling enterprise knowledge.

## 3.1 Core components

- Source Registry
- Connector SDK
- Webhook/Event Gateway
- Poll Scheduler
- Repository Harvester
- Document Harvester
- API/Contract Harvester
- Telemetry Harvester
- Filesystem Harvester
- Controlled Web Crawler
- Crawl Frontier
- Checkpoint Manager
- Change Detector
- Content Fingerprinter
- Rate-Limit Manager
- Credential/Secret Resolver
- DLQ
- Replay Engine
- Reconciliation Engine
- Schema Drift Detector
- Connector Health Monitor
- Source Capability Registry
- Mapping Registry
- Source-to-Ontology Mapping Engine

## Requirements

### G2-EKAF-001 — Source Registry
Maintain a registry containing:
- source ID,
- source type,
- base endpoint,
- acquisition modes,
- credentials reference,
- allowed scopes,
- excluded scopes,
- polling frequency,
- webhook status,
- mapping version,
- parser version,
- checkpoint,
- last successful baseline,
- last incremental run,
- reconciliation schedule,
- health,
- freshness SLO.

### G2-EKAF-002 — Connector SDK
Provide a stable SDK with:
- `discover()`,
- `baseline()`,
- `poll_changes()`,
- `handle_event()`,
- `fetch_record()`,
- `fetch_children()`,
- `checkpoint()`,
- `health()`,
- `capabilities()`.

### G2-EKAF-003 — SourceEvent envelope
Every acquired unit SHALL be emitted as a versioned `SourceEvent` with:
- event_id,
- source_id,
- source_type,
- source_record_id,
- source_record_type,
- operation,
- event_time,
- observed_time,
- cursor/checkpoint,
- content_hash,
- source_version,
- payload/evidence reference,
- permissions metadata when applicable,
- correlation/run ID.

### G2-EKAF-004 — Baseline crawl
A source SHALL support an initial full authorized baseline extraction where technically possible.

### G2-EKAF-005 — Incremental sync
After baseline, EOIP SHALL ingest only:
- newly created records,
- changed records,
- deleted/archived records,
- relationship changes,
- permission changes where supported.

### G2-EKAF-006 — Webhook/event ingestion
Connectors that support events SHALL ingest them through a durable local event endpoint.

### G2-EKAF-007 — Poll fallback
Every event-driven connector SHOULD support incremental polling as reconciliation/fallback where the source permits it.

### G2-EKAF-008 — Reconciliation crawl
Periodic reconciliation SHALL compare source state/checksums/cursors with EOIP state and repair missed events.

### G2-EKAF-009 — Idempotency
Repeated delivery of the same source event SHALL NOT create duplicate canonical facts.

### G2-EKAF-010 — Ordering tolerance
Connectors SHALL tolerate delayed/out-of-order events using source versions/event timestamps where available.

### G2-EKAF-011 — Rate limiting
Connector framework SHALL support:
- source rate limits,
- adaptive backoff,
- retry-after,
- concurrency limits,
- per-source budgets.

### G2-EKAF-012 — Checkpointing
Checkpoints SHALL advance only after downstream graph mutation commits.

### G2-EKAF-013 — Replay
An operator SHALL be able to replay:
- one event,
- one record,
- one time window,
- one ingestion run,
- one source,
without requiring a full graph rebuild.

### G2-EKAF-014 — Dead-letter handling
Failed events SHALL enter a local DLQ with:
- failure category,
- source event,
- mapping/parser version,
- stack/correlation ID,
- retry state,
- remediation note.

### G2-EKAF-015 — Dry run
Every connector/mapping SHALL support a dry-run mode that produces proposed canonical mutations without modifying the graph.

### G2-EKAF-016 — Source deletion semantics
Deletion/archival SHALL expire current facts while retaining historical provenance.

### G2-EKAF-017 — Schema drift
EKAF SHALL detect source payload/schema changes and classify:
- additive,
- compatible,
- potentially breaking,
- breaking.

### G2-EKAF-018 — Mapping drift
A mapping version change SHALL be traceable and replayable.

### G2-EKAF-019 — Crawl boundaries
Controlled web crawling SHALL enforce:
- allowed hosts,
- allowed path prefixes,
- excluded path patterns,
- maximum depth,
- maximum pages,
- content type limits,
- size limits,
- concurrency,
- politeness/rate limits.

### G2-EKAF-020 — Authentication isolation
Secrets SHALL never be embedded in connector configuration artifacts.

### G2-EKAF-021 — Connector health
Expose:
- last success,
- last failure,
- lag,
- freshness,
- error rate,
- throughput,
- checkpoint,
- rate-limit status.

### G2-EKAF-022 — Source priority
When two sources assert conflicting facts, the acquisition layer SHALL preserve both claims and defer truth resolution to the trust layer.

### G2-EKAF-023 — Permission-aware metadata
Where supported, preserve source visibility/security metadata for future enforcement.

### G2-EKAF-024 — Content fingerprinting
Use stable hashing to skip unchanged content.

### G2-EKAF-025 — Attachment handling
Attachments SHALL be:
- classified,
- size-limited,
- hashed,
- safely parsed,
- linked to parent records,
- quarantined when unsafe/unparseable.

### G2-EKAF-026 — Incremental graph enrichment
A new source connection SHALL enrich existing canonical entities rather than create a disconnected duplicate domain.

### G2-EKAF-027 — Source capability introspection
Each connector SHALL report supported capabilities such as:
- baseline,
- delta,
- webhook,
- delete detection,
- version history,
- permissions,
- attachments,
- comments,
- relationships.

### G2-EKAF-028 — Connector compatibility matrix
Maintain tested source-product/API versions.

### G2-EKAF-029 — Offline source fixture mode
Every production connector SHALL have fixture/synthetic mode for local deterministic testing.

### G2-EKAF-030 — Source onboarding wizard
Admin GUI SHALL guide:
`connect → authenticate → scope → discover → preview → map → dry run → validate → baseline`.

---

# 4. Source-Specific Acquisition Requirements

# 4.1 Jira

## G2-SRC-JIRA-001
Capture projects, issue types, epics, stories, tasks, bugs, subtasks, sprints, statuses, labels, links, users, comments and changelog where authorized.

## G2-SRC-JIRA-002
Preserve issue key and immutable source ID separately.

## G2-SRC-JIRA-003
Map link types into explicit graph relationships.

## G2-SRC-JIRA-004
Incrementally process new/changed issues and changelog updates.

## G2-SRC-JIRA-005
Link Jira to commits/branches/MRs using deterministic references before semantic inference.

## G2-SRC-JIRA-006
Capture project/version/release relationships where available.

---

# 4.2 Confluence / Enterprise Wiki

## G2-SRC-CONF-001
Capture spaces, pages, page hierarchy, versions, labels, links, attachments, authors/editors and timestamps.

## G2-SRC-CONF-002
Preserve page revision history references.

## G2-SRC-CONF-003
Extract headings, anchors, internal links, external links, code snippets and structured tables where practical.

## G2-SRC-CONF-004
Create document-to-entity links for services, APIs, projects, requirements and code symbols where evidence exists.

## G2-SRC-CONF-005
Detect potentially stale documentation when referenced technical facts change.

---

# 4.3 ServiceNow Knowledge Base

## G2-SRC-SNKB-001
Capture KB articles, KBs/categories, article versions, ownership, state, validity and related records.

## G2-SRC-SNKB-002
Link KB articles to incidents, problems, services, CIs and change records when source relationships/evidence exist.

## G2-SRC-SNKB-003
Retain article revision lineage.

---

# 4.4 ServiceNow Incidents / Problems / Changes / CMDB

## G2-SRC-SNOW-001
Capture incident records and their affected services/CIs, assignment, severity, state, timestamps and linked records.

## G2-SRC-SNOW-002
Capture problem/RCA records and relationships to incidents and known errors.

## G2-SRC-SNOW-003
Capture change requests, approvals, windows, implementation/backout plans and affected CIs/services.

## G2-SRC-SNOW-004
Capture authorized CMDB CIs and relationships for topology enrichment.

## G2-SRC-SNOW-005
Preserve state transitions as temporal events rather than only current status.

## G2-SRC-SNOW-006
Link changes/deployments/incidents using explicit source relationships and bounded temporal correlation.

---

# 4.5 GitHub

## G2-SRC-GH-001
Capture repositories, organizations, branches, tags, commits, pull requests, issues, releases, workflows/actions metadata and repository ownership metadata where authorized.

## G2-SRC-GH-002
Support event-driven updates plus reconciliation.

## G2-SRC-GH-003
Map PR/commit/change-set relationships to code symbols after parsing.

## G2-SRC-GH-004
Capture repository documentation and GitHub Pages sources when configured.

---

# 4.6 GitLab

## G2-SRC-GL-001
Capture groups/projects, repositories, branches, tags, commits, merge requests, issues/work items, pipelines, jobs, artifacts metadata, releases and wiki/pages metadata where authorized.

## G2-SRC-GL-002
Consume webhook events where configured.

## G2-SRC-GL-003
Link MR → commit → file → symbol → pipeline → deployment metadata.

## G2-SRC-GL-004
Support GitLab Pages / “prod pages” content as a documentation source when configured.

---

# 4.7 Local Git / Source Code

## G2-SRC-CODE-001
Parse configured repositories using deterministic language parsers.

## G2-SRC-CODE-002
Create repository/directory/file/module/class/interface/function/method/import/call/dependency nodes and relationships where statically resolvable.

## G2-SRC-CODE-003
Record source ranges for symbol traceability.

## G2-SRC-CODE-004
Do not state dynamically unresolved calls as deterministic facts.

## G2-SRC-CODE-005
Process only changed files/symbols after initial baseline where parser support permits.

---

# 4.8 API Portals / Contracts

## G2-SRC-API-001
Ingest OpenAPI/Swagger specifications.

## G2-SRC-API-002
Support AsyncAPI, GraphQL schemas, protobuf descriptors, JSON Schema and Postman collections where practical.

## G2-SRC-API-003
Build:
`Application → API → Endpoint/Operation → Request/Response Schema → Data Entity → Consumer`.

## G2-SRC-API-004
Version API contracts.

## G2-SRC-API-005
Detect breaking API changes.

## G2-SRC-API-006
Link APIs to code symbols, services, docs, consumers, tests and incidents when evidence exists.

---

# 4.9 Kibana / Elastic Observability

## G2-SRC-KIB-001
Capture configured dashboard/saved-object/data-view metadata through supported APIs/export mechanisms where authorized.

## G2-SRC-KIB-002
Capture alert/rule metadata where available and configured.

## G2-SRC-KIB-003
Do not ingest full raw log history into HugeGraph.

## G2-SRC-KIB-004
Create semantic objects:
- LogPattern,
- ErrorSignature,
- SavedQuery,
- Dashboard,
- Panel,
- AlertDefinition,
- EvidenceWindow.

## G2-SRC-KIB-005
Retain source query/time-range pointers for reproducibility.

---

# 4.10 Datadog

## G2-SRC-DD-001
Capture configured services, service dependencies, dashboards, monitors, SLO metadata, APM/service catalog metadata and bounded log/trace evidence where authorized.

## G2-SRC-DD-002
Create runtime dependency edges from supported service/APM topology.

## G2-SRC-DD-003
Link monitors/alerts to services, deployments and incidents where evidence allows.

## G2-SRC-DD-004
Do not copy unbounded raw telemetry into HugeGraph.

---

# 4.11 Grafana

## G2-SRC-GRAF-001
Capture dashboards, folders, panels, alerting metadata and configured datasource/query references through supported APIs/export formats.

## G2-SRC-GRAF-002
Build:
`Dashboard → Panel → Query → Metric/DataSource → Service/Component`.

## G2-SRC-GRAF-003
Preserve dashboard version/revision metadata where available.

---

# 4.12 OpenTelemetry

## G2-SRC-OTEL-001
Support OTLP-compatible semantic ingestion or an adapter for normalized traces/metrics/log metadata.

## G2-SRC-OTEL-002
Map resource/service attributes into canonical Service, Instance, Environment and Deployment entities.

## G2-SRC-OTEL-003
Derive bounded runtime call relationships from traces.

## G2-SRC-OTEL-004
Store trace exemplars/evidence references rather than all spans unless explicitly configured for a small environment.

## G2-SRC-OTEL-005
Use telemetry windows and confidence for runtime relationships.

---

# 4.13 CI/CD

## G2-SRC-CICD-001
Capture pipeline, run, job, test, artifact, release and deployment metadata from configured systems.

## G2-SRC-CICD-002
Link:
`Commit → Build → Artifact → Deployment → Environment`.

## G2-SRC-CICD-003
Capture failure/success state transitions.

## G2-SRC-CICD-004
Preserve artifact checksums/identifiers where available.

---

# 4.14 Docker / Kubernetes / Runtime Infrastructure

## G2-SRC-RUNTIME-001
Capture images, containers/workloads, namespaces, deployments, services, config references and environment metadata where authorized.

## G2-SRC-RUNTIME-002
Link image digest to build/artifact/commit where possible.

## G2-SRC-RUNTIME-003
Maintain current and historical workload/service topology.

---

# 4.15 SBOM / SCA / Vulnerability

## G2-SRC-SBOM-001
Ingest SPDX/CycloneDX or equivalent supported SBOM formats.

## G2-SRC-SBOM-002
Build:
`Repository/Artifact → Package → Version → Dependency`.

## G2-SRC-SBOM-003
Link vulnerabilities/CVEs to affected package versions when data is provided by configured scanners/feeds.

## G2-SRC-SBOM-004
Support query:
“Which production services contain package/version X?”

---

# 4.16 Generic Files / Intranet / Web

## G2-SRC-WEB-001
Support Markdown, text, HTML, JSON, YAML, XML, PDF and configured office/document formats when a safe parser exists.

## G2-SRC-WEB-002
Implement controlled internal web crawling with explicit allowlists and bounds.

## G2-SRC-WEB-003
Detect duplicate content by hash/canonical URL.

## G2-SRC-WEB-004
Retain link graph and document hierarchy.

## G2-SRC-WEB-005
Never follow unconfigured external domains automatically.

---

# 5. Baseline, Incremental Synchronization & Reconciliation

## G2-SYNC-001 — Baseline state
Every source SHALL have a recorded baseline completion marker.

## G2-SYNC-002 — Baseline snapshot
Baseline SHALL record:
- source scope,
- source version/cursor,
- started/finished times,
- counts,
- failures,
- mapping/parser versions,
- graph mutation counts.

## G2-SYNC-003 — Delta processing
Only changed records SHALL be reprocessed after baseline unless reconciliation requests otherwise.

## G2-SYNC-004 — Delete/retire
Source deletion SHALL expire current graph assertions; historical revisions remain queryable.

## G2-SYNC-005 — Missed-event recovery
Reconciliation SHALL repair missed webhooks/events.

## G2-SYNC-006 — Duplicate-event handling
Duplicate events SHALL be safe.

## G2-SYNC-007 — Late event handling
Late events SHALL not incorrectly overwrite newer source versions.

## G2-SYNC-008 — Dependency-aware update
When source A changes, only dependent derived relationships/retrieval indexes/summaries SHALL be invalidated/recomputed.

## G2-SYNC-009 — Consistency watermark
Expose source consistency/freshness watermarks.

## G2-SYNC-010 — Full rebuild is exceptional
Full rebuild SHALL be an explicit maintenance action, not normal sync behavior.

## G2-SYNC-011 — Rebuild equivalence test
For supported deterministic domains, replay/rebuild output SHALL be logically equivalent to incrementally maintained graph state.

## G2-SYNC-012 — Connector pause/resume
Operators SHALL pause a source without losing checkpoint.

## G2-SYNC-013 — Backfill
A newly added mapping/entity type SHALL support bounded historical backfill without re-ingesting unrelated data.

## G2-SYNC-014 — Selective rescan
Support rescan by:
- entity type,
- path,
- repository,
- project,
- time range,
- source ID.

---

# 6. Graph Evolution Engine

The Graph Evolution Engine converts source changes into safe temporal graph mutations.

## G2-EVOL-001
Every mutable canonical entity SHALL support revision metadata.

## G2-EVOL-002
Every mutable relationship SHALL support validity interval:
- `valid_from`,
- `valid_to`.

## G2-EVOL-003
Store observation/system time separately from business/event-valid time where meaningful.

## G2-EVOL-004
A relationship removal SHALL expire the previous assertion rather than erase history.

## G2-EVOL-005
A relationship update SHALL be represented as a new revision/assertion.

## G2-EVOL-006
Current views SHALL exclude expired facts unless explicitly requested.

## G2-EVOL-007
Historical queries SHALL reconstruct state at time T.

## G2-EVOL-008
Provide graph diff:
- added entities,
- changed entities,
- removed/retired entities,
- added edges,
- expired edges,
- changed properties,
- trust changes.

## G2-EVOL-009
Every graph mutation SHALL reference:
- SourceEvent,
- ingestion run,
- mapping/parser version,
- ontology version.

## G2-EVOL-010
Graph mutation batches SHALL be atomic at an appropriate bounded unit.

## G2-EVOL-011
Failed mutation batch SHALL not advance source checkpoint.

## G2-EVOL-012
Relationship preservation SHALL mean “preserve history,” not “keep stale edges active.”

## G2-EVOL-013
Support previous-revision links or revision identifiers.

## G2-EVOL-014
Support tombstone/retired status for source objects no longer current.

## G2-EVOL-015
Provide rollback/replay strategy for mapping defects.

## G2-EVOL-016
Schema/ontology migration SHALL explicitly declare whether existing facts require:
- no migration,
- lazy migration,
- online backfill,
- offline migration,
- source replay.

---

# 7. Semantic Change Journal

## G2-JOURNAL-001
Maintain an append-oriented local change journal for source and graph changes.

## G2-JOURNAL-002
Record:
- event ID,
- source,
- canonical entity,
- before hash,
- after hash,
- mutation type,
- changed fields/edges,
- timestamps,
- causal source event,
- graph version.

## G2-JOURNAL-003
Support query by:
- source,
- entity,
- time,
- release,
- ingestion run.

## G2-JOURNAL-004
Journal SHALL support replay into derived indexes/services.

## G2-JOURNAL-005
Journal retention SHALL be configurable.

## G2-JOURNAL-006
Journal data SHALL be included in audit/incident troubleshooting.

---

# 8. Semantic Event Bus

A local semantic event layer SHALL notify internal consumers of graph changes.

## Event types

- `ENTITY_CREATED`
- `ENTITY_CHANGED`
- `ENTITY_RETIRED`
- `RELATION_CREATED`
- `RELATION_CHANGED`
- `RELATION_EXPIRED`
- `ONTOLOGY_CHANGED`
- `IDENTITY_MERGED`
- `IDENTITY_SPLIT`
- `QUALITY_DEGRADED`
- `QUALITY_RECOVERED`
- `SOURCE_STALE`
- `SOURCE_RECOVERED`
- `TRUST_CHANGED`
- `GRAPH_VERSION_PUBLISHED`

## Requirements

### G2-EVENT-001
Events SHALL have stable versioned schemas.

### G2-EVENT-002
Events SHALL be emitted only after durable graph mutation state is known.

### G2-EVENT-003
Consumers SHALL be idempotent.

### G2-EVENT-004
Support local in-process implementation initially; broker abstraction MAY be added later.

### G2-EVENT-005
Consumers may include:
- search index,
- vector index,
- GraphRAG community summaries,
- semantic cache,
- dashboards,
- quality metrics,
- agents,
- alerts.

### G2-EVENT-006
Consumer failures SHALL not corrupt authoritative graph state.

### G2-EVENT-007
Support replay from journal/checkpoint.

---

# 9. Additional Graph Domains

# 9.1 API & Contract Graph

## G2-GRAPH-API-001
Model APIs, versions, endpoints/operations, schemas, owners, providers, consumers and compatibility.

## G2-GRAPH-API-002
Link contracts to:
- source symbols,
- services,
- docs,
- tests,
- deployments,
- consumers.

## G2-GRAPH-API-003
Track breaking/non-breaking contract changes.

---

# 9.2 Observability Graph

## G2-GRAPH-OBS-001
Model:
- Dashboard,
- Panel,
- Metric,
- LogPattern,
- ErrorSignature,
- Monitor,
- Alert,
- TraceEvidence,
- SLO,
- Service.

## G2-GRAPH-OBS-002
Link runtime evidence to deployments/incidents/services.

## G2-GRAPH-OBS-003
Relationships SHALL have bounded observation windows and evidence.

---

# 9.3 Runtime Topology Graph

## G2-GRAPH-RUNTIME-001
Represent implemented runtime topology independently from intended architecture.

## G2-GRAPH-RUNTIME-002
Support temporal service-to-service relationships.

## G2-GRAPH-RUNTIME-003
Compare runtime relationships with static code dependencies.

---

# 9.4 Security & Supply-Chain Graph

## G2-GRAPH-SEC-001
Represent package/version/dependency/SBOM/vulnerability/artifact/service relationships.

## G2-GRAPH-SEC-002
Support blast radius from package/CVE to deployed services.

## G2-GRAPH-SEC-003
Preserve scanner/evidence provenance.

---

# 9.5 Test Intelligence Graph

## G2-GRAPH-TEST-001
Represent:
`Requirement → Code Symbol → Test → TestRun → Build → Release`.

## G2-GRAPH-TEST-002
Support change-based test impact analysis.

## G2-GRAPH-TEST-003
Track test coverage relationship confidence/source.

---

# 9.6 Decision Graph

## G2-GRAPH-DEC-001
Represent:
- Decision,
- Alternative,
- Constraint,
- Rationale,
- Evidence,
- Approver,
- Affected Architecture,
- Implementation,
- Outcome.

## G2-GRAPH-DEC-002
Link ADRs/design decisions to code/architecture/releases.

## G2-GRAPH-DEC-003
Support “Why was this architecture chosen?” queries.

---

# 9.7 Process Graph

## G2-GRAPH-PROC-001
Derive process events from Jira/ServiceNow/CI/CD where configured.

## G2-GRAPH-PROC-002
Represent designed and observed process flows separately.

## G2-GRAPH-PROC-003
Identify skipped steps, loops, bottlenecks and deviations.

---

# 9.8 Business Intent / Capability Graph

## G2-GRAPH-BIZ-001
Represent:
- BusinessObjective,
- BusinessCapability,
- Requirement,
- Product,
- Application,
- Service,
- Owner.

## G2-GRAPH-BIZ-002
Link business intent through technical implementation and runtime.

## G2-GRAPH-BIZ-003
Support reverse query:
“Which business capabilities are affected if Service X fails?”

---

# 10. Live Enterprise Digital Knowledge Twin

## G2-TWIN-001
EOIP SHALL present the enterprise as a continuously synchronized semantic twin.

## G2-TWIN-002
The twin SHALL include:
- business intent,
- requirements,
- architecture,
- code,
- APIs,
- tests,
- CI/CD,
- deployments,
- runtime,
- telemetry semantics,
- incidents,
- knowledge/docs,
- people/ownership,
- decisions.

## G2-TWIN-003
The twin SHALL expose current state and historical revisions.

## G2-TWIN-004
Every derived twin relationship SHALL be evidence-addressable.

## G2-TWIN-005
The twin SHALL distinguish:
- intended,
- implemented,
- observed runtime,
- inferred.

---

# 11. Enterprise Time Machine

## G2-TIME-001
GUI SHALL provide a temporal state selector for supported domains.

## G2-TIME-002
Support “state as of T”.

## G2-TIME-003
Support compare T1 vs T2.

## G2-TIME-004
Highlight semantic additions/removals/changes.

## G2-TIME-005
Support release-based snapshots.

## G2-TIME-006
Time travel SHALL include ontology/schema version context.

## G2-TIME-007
Evidence viewed in historical mode SHALL reflect what was known/valid for that time.

---

# 12. Counterfactual Enterprise Twin / What-If Simulation

## G2-SIM-001
Create a logical simulation workspace from a selected graph version.

## G2-SIM-002
Apply hypothetical mutations without touching authoritative graph.

## G2-SIM-003
Supported mutations SHOULD include:
- remove API,
- upgrade dependency,
- change service dependency,
- split/merge service,
- transfer ownership,
- change ontology rule,
- retire component.

## G2-SIM-004
Run:
- blast radius,
- architecture conformance,
- quality validation,
- test impact,
- policy checks.

## G2-SIM-005
Compare simulated state to baseline.

## G2-SIM-006
Simulation output SHALL show evidence, assumptions and uncertainty.

## G2-SIM-007
A simulation SHALL be reproducible by:
- base graph version,
- mutation set,
- rules/version.

---

# 13. Architecture Conformance & Semantic Architecture Compiler

## G2-ARCHC-001
Maintain separate views for:
- intended architecture,
- implemented/static architecture,
- observed runtime architecture.

## G2-ARCHC-002
Define architecture policy DSL or declarative rules.

## G2-ARCHC-003
Rule examples:
- UI MUST_NOT_ACCESS database directly.
- Domain A MUST_NOT_DEPEND_ON Domain B.
- Critical API MUST have owner and tests.
- Regulated data MUST_NOT cross boundary X.

## G2-ARCHC-004
Compile rules into bounded graph validations.

## G2-ARCHC-005
Report exact violating graph path.

## G2-ARCHC-006
Map violations to source files/symbols/commits where possible.

## G2-ARCHC-007
Expose violations in Web UI and VS Code.

## G2-ARCHC-008
Support CI gate mode.

## G2-ARCHC-009
Track architecture debt trend.

---

# 14. Causal Intelligence

Causality SHALL be handled conservatively.

## G2-CAUSE-001
Represent correlation separately from causal hypotheses.

## G2-CAUSE-002
Relationship classes:
- `CORRELATED_WITH`
- `POSSIBLY_CAUSED`
- `EVIDENCE_SUPPORTS_CAUSE`
- `HUMAN_CONFIRMED_CAUSE`

## G2-CAUSE-003
AI SHALL NOT silently promote correlation into confirmed causality.

## G2-CAUSE-004
Causal hypotheses SHALL include:
- evidence,
- time ordering,
- alternative explanations,
- confidence,
- review status.

## G2-CAUSE-005
Use deployment/telemetry/incident relationships to propose bounded hypotheses.

## G2-CAUSE-006
Human confirmation/rejection SHALL be preserved.

---

# 15. Enterprise Knowledge Immune System

This subsystem continuously evaluates knowledge health and proposes remediation.

## G2-IMMUNE-001
Detect orphan nodes.

## G2-IMMUNE-002
Detect missing mandatory relationships.

## G2-IMMUNE-003
Detect contradictory claims.

## G2-IMMUNE-004
Detect stale documentation.

## G2-IMMUNE-005
Detect source/schema/mapping drift.

## G2-IMMUNE-006
Detect unexpected architecture edges.

## G2-IMMUNE-007
Detect missing ownership.

## G2-IMMUNE-008
Detect broken provenance/evidence references.

## G2-IMMUNE-009
Detect suspicious/low-confidence AI-inferred relationships.

## G2-IMMUNE-010
Detect graph poisoning patterns/untrusted source anomalies.

## G2-IMMUNE-011
Recommend repair, quarantine, re-ingestion or human review.

## G2-IMMUNE-012
Trusted knowledge SHALL NOT be silently rewritten by the immune system.

## G2-IMMUNE-013
Every recommendation SHALL explain why it was generated.

---

# 16. Controlled Ontology Evolution

## G2-OEVO-001
Detect recurring unmapped entity/relationship patterns.

## G2-OEVO-002
Propose new class/property/relationship definitions.

## G2-OEVO-003
Proposals SHALL include:
- evidence count,
- examples,
- candidate parent/class,
- proposed constraints,
- impact analysis,
- migration/backfill requirement.

## G2-OEVO-004
Ontology changes require configured human review/approval.

## G2-OEVO-005
Approved ontology changes SHALL enter existing Ontology GitOps workflow.

## G2-OEVO-006
Rejected suggestions SHALL remain available as training/evaluation feedback without becoming facts.

---

# 17. Process Mining

## G2-PM-001
Create case/event sequences from configured Jira/ServiceNow/CI/CD event data.

## G2-PM-002
Compare designed workflow with observed workflow.

## G2-PM-003
Detect:
- skipped steps,
- rework loops,
- bottlenecks,
- long waits,
- exception paths,
- emergency changes.

## G2-PM-004
Link process deviations to incidents/outcomes where evidence exists.

## G2-PM-005
Support drill-down from process path to source events.

---

# 18. Knowledge Capsules

A Knowledge Capsule is a bounded portable graph context for a task/person/agent.

## G2-CAP-001
Capsule definition SHALL specify:
- root entities,
- traversal rules,
- max depth,
- domains,
- time window,
- trust threshold,
- evidence inclusion,
- security policy.

## G2-CAP-002
Capsules SHALL be reproducible against a graph version.

## G2-CAP-003
Capsules SHALL reduce unnecessary context exposure to AI agents.

## G2-CAP-004
Capsules SHALL include manifest and evidence references.

## G2-CAP-005
Example capsules:
- release,
- incident,
- service,
- application,
- change request,
- architecture review,
- audit evidence.

## G2-CAP-006
Capsules MAY be exportable in an approved local package format.

---

# 19. Native Semantic Query Operators

These SHALL be explicit query intents, not prompt-only behavior.

## G2-QOP-001 — WHY
Explain why entities/results/relationships are connected.

## G2-QOP-002 — WHY NOT
Explain why a candidate/result was excluded or not connected.

## G2-QOP-003 — WHAT IF
Execute counterfactual simulation where supported.

## G2-QOP-004 — WHAT CHANGED
Produce semantic diff between versions/times/releases.

## G2-QOP-005 — WHEN
Determine first/last/valid observation of a relationship/fact.

## G2-QOP-006 — WHO
Resolve ownership/contribution/review responsibility with evidence.

## G2-QOP-007 — WHERE
Locate requirement/code/runtime/document representation.

## G2-QOP-008 — HOW
Explain a trace/path/process from one state/entity to another.

## G2-QOP-009
All native operators SHALL expose structured result + evidence, not just natural-language prose.

---

# 20. Intent-to-Runtime Traceability

## G2-I2R-001
Support the chain:
`Business Objective → Capability → Requirement → Decision → Jira → Code → API → Test → Build → Deployment → Runtime → Telemetry → Incident/Outcome`.

## G2-I2R-002
Support reverse traversal.

## G2-I2R-003
Compute coverage for missing links.

## G2-I2R-004
Flag critical production assets without business/requirement ownership.

## G2-I2R-005
Flag business-critical requirements without runtime traceability.

---

# 21. Knowledge Debt

## G2-KD-001
Represent Knowledge Debt Finding as a first-class record.

## G2-KD-002
Categories:
- unowned component,
- undocumented API,
- unlinked requirement,
- unlinked implementation,
- stale document,
- unresolved identity,
- broken provenance,
- low-confidence critical inference,
- missing test,
- missing architecture mapping,
- unknown production owner,
- stale runbook.

## G2-KD-003
Compute debt by:
- project,
- team,
- service,
- application,
- domain,
- release.

## G2-KD-004
Avoid one opaque debt score; expose contributing dimensions.

## G2-KD-005
Support debt trend over time.

## G2-KD-006
Link every finding to remediation action/evidence.

---

# 22. Knowledge Reliability SLOs

## G2-SLO-001
Allow SLOs such as:
- percentage of production services with owner,
- percentage of requirements linked to implementation,
- percentage of deployments linked to commits,
- percentage of critical APIs documented,
- provenance coverage,
- maximum ownership staleness,
- maximum connector lag.

## G2-SLO-002
SLOs SHALL be configurable by domain.

## G2-SLO-003
SLO breach SHALL create a quality finding.

## G2-SLO-004
Dashboards SHALL show objective, current value, trend and breached assets.

## G2-SLO-005
SLO evaluation SHALL be reproducible against a graph version.

---

# 23. Next-Generation GUI / Application Requirements

EOIP SHALL not expose only a generic “dots and lines” graph.

## 23.1 Lens framework

### G2-UX-LENS-001
Implement a pluggable lens framework where all lenses operate on the same graph/query services.

### Required lenses

- Search Lens
- Graph Lens
- Timeline Lens
- Change Lens
- Impact Lens
- Architecture Lens
- Runtime Lens
- Requirement Lens
- Evidence Lens
- Trust Lens
- Ontology Lens
- Decision Lens
- Security/Supply-Chain Lens
- Release Lens
- Simulation Lens
- Agent Lens
- Knowledge Health Lens
- Process Lens
- API Lens
- Test Lens

### G2-UX-LENS-002
Lens state SHALL preserve current scope/entity/time/filter context when switching.

### G2-UX-LENS-003
Lenses SHALL support shareable/exportable local query definitions where permitted.

---

# 24. Advanced Graph Canvas

## G2-UX-GRAPH-001
Semantic zoom.

## G2-UX-GRAPH-002
Clustering/grouping.

## G2-UX-GRAPH-003
Graph folding/collapse.

## G2-UX-GRAPH-004
Progressive expansion rather than rendering huge neighborhoods.

## G2-UX-GRAPH-005
Time slider.

## G2-UX-GRAPH-006
Current/historical toggle.

## G2-UX-GRAPH-007
Relationship/trust/source filters.

## G2-UX-GRAPH-008
Edge confidence/evidence indicators.

## G2-UX-GRAPH-009
Path storytelling mode.

## G2-UX-GRAPH-010
Architecture boundary overlays.

## G2-UX-GRAPH-011
Runtime topology overlay.

## G2-UX-GRAPH-012
Release comparison overlay.

## G2-UX-GRAPH-013
Blast-radius highlighting.

## G2-UX-GRAPH-014
Click relationship → “Why does this edge exist?”

## G2-UX-GRAPH-015
Click node → “Where did this entity come from?”

## G2-UX-GRAPH-016
Click path → evidence bundle for path.

---

# 25. Graph Playback

## G2-UX-PLAY-001
Replay selected incident/release/change as temporal graph events.

## G2-UX-PLAY-002
Playback SHALL synchronize:
- deployment,
- topology,
- alerts,
- error signatures,
- incidents,
- rollback/recovery.

## G2-UX-PLAY-003
Allow pause/step/scrub.

## G2-UX-PLAY-004
Every playback event SHALL link to source evidence.

## G2-UX-PLAY-005
Support export of an incident timeline evidence package.

---

# 26. Admin / Engineering GUI Additions

## G2-ADMIN-001
Source Registry management.

## G2-ADMIN-002
Connector setup wizard.

## G2-ADMIN-003
Baseline/incremental/reconciliation status.

## G2-ADMIN-004
Checkpoint viewer.

## G2-ADMIN-005
DLQ/replay console.

## G2-ADMIN-006
Schema/mapping drift console.

## G2-ADMIN-007
Source freshness/lag dashboard.

## G2-ADMIN-008
Graph version timeline.

## G2-ADMIN-009
Semantic Change Journal viewer.

## G2-ADMIN-010
Semantic event consumer health.

## G2-ADMIN-011
Source-to-ontology mapping preview.

## G2-ADMIN-012
Crawl-scope safety preview.

## G2-ADMIN-013
Telemetry semantic extraction controls.

## G2-ADMIN-014
Knowledge SLO management.

## G2-ADMIN-015
Knowledge Debt dashboard.

## G2-ADMIN-016
Ontology evolution proposal review.

## G2-ADMIN-017
Simulation workspace manager.

---

# 27. VS Code Additions

## G2-VSC-001
Display API contract relationships for current symbol.

## G2-VSC-002
Display runtime services/deployments connected to current code.

## G2-VSC-003
Display architecture conformance findings inline/panel.

## G2-VSC-004
Display impacted tests for current change.

## G2-VSC-005
Display relevant incidents/error signatures.

## G2-VSC-006
Display decision/ADR rationale.

## G2-VSC-007
Support `WHY`, `WHAT CHANGED`, `IMPACT`, `WHERE USED` quick actions.

## G2-VSC-008
Never require unrestricted raw telemetry access in editor.

---

# 28. Telemetry Semantics and Storage Rules

## G2-TEL-001
HugeGraph SHALL store semantic telemetry objects, not unlimited raw measurements.

## G2-TEL-002
Every telemetry-derived relationship SHALL have observation window.

## G2-TEL-003
Every telemetry-derived relationship SHALL include source/evidence reference.

## G2-TEL-004
Use aggregation/fingerprints for repeated log patterns.

## G2-TEL-005
Preserve bounded exemplar IDs/trace IDs where permitted.

## G2-TEL-006
Support configurable retention for derived telemetry facts.

## G2-TEL-007
A runtime edge SHALL expire when no longer observed under configured policy.

## G2-TEL-008
Do not confuse “not observed” with “does not exist”; confidence/coverage SHALL be explicit.

---

# 29. Security Requirements for Acquisition/Crawling

## G2-SEC-CRAWL-001
SSRF protection for crawlers/connectors.

## G2-SEC-CRAWL-002
Strict target allowlist.

## G2-SEC-CRAWL-003
No automatic Internet traversal.

## G2-SEC-CRAWL-004
Secret/credential redaction in logs.

## G2-SEC-CRAWL-005
TLS validation configurable but secure by default.

## G2-SEC-CRAWL-006
Untrusted document parsing SHALL be sandboxed/isolated where practical.

## G2-SEC-CRAWL-007
Content-size/decompression limits.

## G2-SEC-CRAWL-008
Archive/bomb protection.

## G2-SEC-CRAWL-009
Prompt-injection content SHALL be tagged as data, not instructions to agents.

## G2-SEC-CRAWL-010
Crawler actions SHALL be read-only unless a separate explicitly approved action connector exists.

## G2-SEC-CRAWL-011
Source credentials SHALL use minimum required permissions.

## G2-SEC-CRAWL-012
All outbound source access SHALL be auditable.

---

# 30. Observability Requirements

## G2-OBS-001
Trace source fetch → SourceEvent → mapping → graph mutation.

## G2-OBS-002
Expose per-source:
- fetch latency,
- records/sec,
- errors,
- lag,
- retries,
- DLQ count.

## G2-OBS-003
Expose graph evolution metrics:
- added/changed/expired facts,
- mutation latency,
- validation failures.

## G2-OBS-004
Expose semantic event bus consumer lag.

## G2-OBS-005
Expose graph version publication time.

## G2-OBS-006
Expose knowledge SLO evaluation latency.

---

# 31. Performance & Scale Requirements

Performance claims SHALL be benchmark-based.

## G2-PERF-001
Baseline ingestion throughput SHALL be measured per source type.

## G2-PERF-002
Incremental update latency SHALL be measured separately.

## G2-PERF-003
Graph mutation throughput SHALL be benchmarked.

## G2-PERF-004
Historical-state reconstruction latency SHALL be benchmarked.

## G2-PERF-005
Graph diff latency SHALL be benchmarked.

## G2-PERF-006
Crawler concurrency SHALL be source-configurable.

## G2-PERF-007
High-volume telemetry adapters SHALL aggregate before graph write.

## G2-PERF-008
Incremental processing SHALL avoid global recomputation.

---

# 32. Reliability & Recovery

## G2-REL-001
Connector workers SHALL restart from committed checkpoint.

## G2-REL-002
Webhook delivery SHALL be deduplicated.

## G2-REL-003
Missed webhook recovery SHALL be tested.

## G2-REL-004
Reconciliation SHALL be safe to rerun.

## G2-REL-005
Event/journal corruption detection SHALL be implemented.

## G2-REL-006
Backup SHALL include graph state plus metadata required for synchronization continuity.

## G2-REL-007
Restore SHALL preserve/restore connector checkpoints consistently.

## G2-REL-008
A restore procedure SHALL document whether events after backup must be replayed.

---

# 33. AI Agent Development Rules

An AI coding agent implementing these requirements SHALL:

1. Read existing EOIP contracts before creating new contracts.
2. Extend existing `SourceEvent`, canonical entity/relationship and provenance patterns rather than fork them.
3. Never write source-specific logic into HugeGraph mutation core.
4. Never allow a connector to directly mutate HugeGraph.
5. Implement deterministic behavior before LLM inference.
6. Mark inferred relationships explicitly.
7. Add stable requirement IDs to code/tests/docs.
8. Implement migration strategy for schema changes.
9. Use feature flags for incomplete future capabilities.
10. Never claim a source capability is implemented until integration tests exist.
11. Use synthetic/fixture data if real credentials/data are unavailable.
12. Never fabricate successful integration with an unavailable system.
13. Add error categories, logging, metrics and audit for each new connector.
14. Keep cloud services optional/non-required.
15. Keep external LLM egress disabled by default.
16. Preserve backward compatibility with existing MVP interfaces unless a documented migration is approved.
17. Add tests for duplicate, delete, late-event, replay and restart behavior.
18. Include acceptance evidence.

---

# 34. Required Data Contracts

Add or extend schemas for:

- `source_registry_entry.schema.json`
- `source_capabilities.schema.json`
- `source_event_v2.schema.json`
- `source_checkpoint.schema.json`
- `crawl_scope.schema.json`
- `reconciliation_run.schema.json`
- `semantic_change_event.schema.json`
- `graph_revision.schema.json`
- `relationship_revision.schema.json`
- `graph_diff.schema.json`
- `telemetry_evidence.schema.json`
- `api_contract.schema.json`
- `knowledge_capsule.schema.json`
- `simulation_spec.schema.json`
- `knowledge_debt_finding.schema.json`
- `knowledge_slo.schema.json`
- `ontology_evolution_proposal.schema.json`
- `causal_hypothesis.schema.json`
- `process_event.schema.json`

All contracts SHALL be versioned.

---

# 35. Required APIs / Service Operations

Minimum additions:

- `POST /api/v1/sources`
- `GET /api/v1/sources`
- `POST /api/v1/sources/{id}/discover`
- `POST /api/v1/sources/{id}/dry-run`
- `POST /api/v1/sources/{id}/baseline`
- `POST /api/v1/sources/{id}/sync`
- `POST /api/v1/sources/{id}/reconcile`
- `GET /api/v1/sources/{id}/checkpoint`
- `GET /api/v1/ingestion/dlq`
- `POST /api/v1/ingestion/replay`
- `GET /api/v1/graph/versions`
- `GET /api/v1/graph/diff`
- `GET /api/v1/graph/as-of`
- `GET /api/v1/change-journal`
- `GET /api/v1/knowledge-debt`
- `GET /api/v1/knowledge-slos`
- `POST /api/v1/simulations`
- `GET /api/v1/simulations/{id}`
- `POST /api/v1/capsules`
- `GET /api/v1/capsules/{id}`
- `POST /api/v1/query/why`
- `POST /api/v1/query/why-not`
- `POST /api/v1/query/what-changed`
- `POST /api/v1/query/what-if`

Write/action endpoints remain policy controlled.

---

# 36. Testing Requirements

## Connector contract tests
Every connector must pass:
- baseline,
- incremental update,
- duplicate event,
- delete,
- rate-limit,
- auth failure,
- pagination,
- checkpoint resume,
- malformed payload,
- schema drift,
- dry run,
- replay.

## Graph evolution tests
- edge expiry,
- entity revision,
- late update,
- historical reconstruction,
- graph diff,
- rollback/replay.

## Telemetry tests
- bounded ingestion,
- aggregation,
- source reference,
- runtime edge expiration,
- no uncontrolled raw telemetry copy.

## UI tests
- source onboarding,
- timeline,
- lens switch,
- graph evidence,
- playback,
- simulation.

## Security tests
- SSRF,
- path escape,
- malicious URL,
- decompression bomb,
- oversized document,
- prompt injection in source content,
- credential leak prevention.

---

# 37. Acceptance Scenarios

## Scenario A — Baseline and incremental Jira/Git
1. Baseline Jira and repository.
2. Build Jira/Code graph.
3. Add one new Jira change and one commit.
4. Incremental sync.
5. Verify only changed facts mutate.
6. Verify previous graph history remains accessible.

## Scenario B — ServiceNow incident
1. Ingest incident and affected service.
2. Link recent deployment.
3. Link commit/code.
4. Display evidence chain.

## Scenario C — Observability
1. Ingest configured Datadog/Grafana/Kibana metadata fixture.
2. Build dashboard/monitor/service relationships.
3. Derive bounded runtime relationship.
4. Verify raw telemetry is not bulk-stored in HugeGraph.

## Scenario D — Time Machine
1. Create two relationship revisions.
2. Query state before and after change.
3. Compare graph diff.

## Scenario E — Simulation
1. Select API.
2. Simulate removal.
3. Produce affected consumers/tests/services/docs.
4. Verify authoritative graph is unchanged.

## Scenario F — Architecture conformance
1. Define forbidden dependency rule.
2. Ingest violating code path.
3. Detect violation.
4. Show exact source path and evidence.

## Scenario G — Knowledge Immune System
1. Introduce orphan/unowned/stale sample facts.
2. Detect findings.
3. Produce recommended remediation.
4. Verify no trusted graph mutation occurs automatically.

---

# 38. Phase Priority

## P0 — Must build early
- EKAF core
- Source Registry
- Connector SDK expansion
- baseline/incremental/reconciliation
- Graph Evolution Engine
- Semantic Change Journal
- event abstraction
- Jira/Git/GitLab/source code/file support
- versioned current/historical relationship semantics

## P1 — High-value enterprise expansion
- Confluence
- ServiceNow KB/incident/problem/change/CMDB
- GitHub
- API portal/contracts
- CI/CD graph
- Runtime/observability metadata
- OpenTelemetry adapter
- knowledge SLOs
- knowledge debt

## P2 — Differentiating intelligence
- Time Machine
- intended/implemented/runtime architecture comparison
- architecture compiler/conformance
- process mining
- Knowledge Capsules
- native semantic query operators
- intent-to-runtime traceability

## P3 — Moonshot/advanced
- Counterfactual twin
- causal hypotheses
- knowledge immune system
- controlled ontology evolution proposals
- graph playback
- richer simulation/calibration

---

# 39. Definition of Done

A requirement is not complete until:

- code exists,
- interface/contract is versioned,
- migration impact is handled,
- unit tests pass,
- integration tests pass,
- error paths are tested,
- logging/metrics exist,
- security implications are documented,
- requirement ID is in traceability,
- operator/user docs exist,
- acceptance scenario is reproducible,
- no mock/hardcoded output is presented as a working integration.

---

# 40. North-Star Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                  EXPERIENCE & APPLICATIONS                   │
│ Web | Admin | VS Code | API | MCP | Domain Applications    │
├──────────────────────────────────────────────────────────────┤
│                        INTELLIGENCE                          │
│ Search | Impact | Time | Simulation | GraphRAG | Agents    │
├──────────────────────────────────────────────────────────────┤
│                     TRUST & GOVERNANCE                       │
│ Evidence | Provenance | Quality | SLO | History | Policy   │
├──────────────────────────────────────────────────────────────┤
│                   ENTERPRISE KNOWLEDGE GRAPH                 │
│         Apache HugeGraph + Meta + Temporal/Revisions         │
├──────────────────────────────────────────────────────────────┤
│                    SEMANTIC CONTROL PLANE                    │
│ Ontology | Identity | Rules | Contracts | Mappings         │
├──────────────────────────────────────────────────────────────┤
│          KNOWLEDGE ACQUISITION & SYNCHRONIZATION FABRIC      │
│ APIs | Webhooks | Crawlers | Git | Telemetry | Reconcile   │
└──────────────────────────────────────────────────────────────┘
```

EOIP's target end state is a **continuously synchronized, time-aware, evidence-backed digital knowledge twin of the enterprise** that can be queried, compared, simulated and safely consumed by humans and AI systems.
