# Functional Requirements

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Complete normative functional requirement catalog

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

### FR-CONN-001 — Connector SDK
**WHAT:** Provide a versioned connector interface for discover, extract, checkpoint, health and replay.  
**WHY:** New sources must not change graph-core logic.  
**HOW:** Each connector emits SourceEvent records and owns source-specific auth/pagination only.  
**DATA / INTERFACES:** ConnectorConfig, SourceEvent, Checkpoint  
**FAILURE:** Connector isolation; retryable failures checkpoint; poison records to DLQ.  
**TEST:** Contract tests against a fake source.  
**COMPLETE WHEN:** A new connector can be added without editing ingestion core.  
**TARGET PHASE:** P1-MVP

### FR-CONN-002 — Jira JSON connector
**WHAT:** Import configurable Jira JSON plus the synthetic MVP fixture.  
**WHY:** Jira is the primary work-management seed for traceability.  
**HOW:** Map source fields through configuration into canonical WorkItem/Project/Person entities.  
**DATA / INTERFACES:** JSON file, mapping YAML, SourceEvent  
**FAILURE:** Malformed records rejected individually with evidence; run continues.  
**TEST:** Fixture, malformed, duplicate, resume tests.  
**COMPLETE WHEN:** Repeat import is idempotent and creates expected graph.  
**TARGET PHASE:** P1-MVP

### FR-CONN-003 — Git repository connector
**WHAT:** Inspect local Git repositories without network access.  
**WHY:** The MVP must link work to commits and code.  
**HOW:** Read refs, commits, authors, changed paths and commit messages using local git.  
**DATA / INTERFACES:** Local repository path, git metadata  
**FAILURE:** Invalid repo/path traversal rejected; repository errors do not corrupt prior data.  
**TEST:** Temporary repository integration tests.  
**COMPLETE WHEN:** Repository, branch and commit nodes plus modifications exist.  
**TARGET PHASE:** P1-MVP

### FR-CONN-004 — GitLab metadata adapter
**WHAT:** Support GitLab-style MR/pipeline metadata from configurable API or local JSON fixture.  
**WHY:** The E2E story includes merge requests and pipelines.  
**HOW:** MVP supports fixture/offline mode; live on-prem GitLab adapter uses endpoint/token abstraction.  
**DATA / INTERFACES:** MR/pipeline JSON, endpoint config  
**FAILURE:** Rate limits/retries/checkpoints; no hard-coded credential.  
**TEST:** Mock API and fixture contract tests.  
**COMPLETE WHEN:** MR and pipeline records link to commits and work items.  
**TARGET PHASE:** P1-MVP

### FR-CONN-005 — Connector resiliency
**WHAT:** Implement pagination, retry/backoff, rate-limit handling, checkpointing and resume.  
**WHY:** Enterprise ingestion must survive partial failure.  
**HOW:** Persist checkpoint atomically in local state volume after committed graph batch.  
**DATA / INTERFACES:** Checkpoint JSON, job state  
**FAILURE:** Bounded retries then DLQ/failure state.  
**TEST:** Fault-injection restart tests.  
**COMPLETE WHEN:** Restart resumes without duplicate canonical nodes.  
**TARGET PHASE:** P1-MVP

### FR-CONN-006 — Dry run and replay
**WHAT:** Allow validation-only dry run and deterministic replay of captured source events.  
**WHY:** Safe mapping evolution and debugging need reproducibility.  
**HOW:** Dry run performs parse/map/validation without graph mutation; replay reads raw-capture events.  
**DATA / INTERFACES:** SourceEvent archive  
**FAILURE:** Invalid replay schema/version is quarantined.  
**TEST:** Golden-event replay tests.  
**COMPLETE WHEN:** Same input/version produces same canonical mutations.  
**TARGET PHASE:** P1-MVP

### FR-CONN-007 — Source deletion semantics
**WHAT:** Represent source disappearance/deletion without silent hard delete.  
**WHY:** Historical provenance must not be destroyed.  
**HOW:** Mark tombstone/deleted_at; hard delete is separate administrative operation.  
**DATA / INTERFACES:** Source version/tombstone  
**FAILURE:** Conflicting source state becomes validation finding.  
**TEST:** Deletion/reappearance tests.  
**COMPLETE WHEN:** Deleted source is queryable historically and excluded from current views.  
**TARGET PHASE:** P1-MVP

### FR-CONF-001 — Confluence connector
**WHAT:** Add on-prem Confluence connector through Connector SDK.  
**WHY:** Documentation traceability requires enterprise wiki ingestion.  
**HOW:** Deferred from MVP; support pages, spaces, attachments metadata and deltas.  
**DATA / INTERFACES:** Confluence API records  
**FAILURE:** Same connector failure model.  
**TEST:** Contract tests in P2.  
**COMPLETE WHEN:** Incremental sync and provenance pass.  
**TARGET PHASE:** P2

### FR-SNOW-001 — ServiceNow connector
**WHAT:** Add on-prem ServiceNow incident/problem/change/KB connector.  
**WHY:** Operations traceability needs service-management data.  
**HOW:** Deferred from MVP behind Connector SDK.  
**DATA / INTERFACES:** ServiceNow table API  
**FAILURE:** Rate limits and schema drift isolated.  
**TEST:** Contract tests in P2.  
**COMPLETE WHEN:** Incremental sync and mappings pass.  
**TARGET PHASE:** P2

### FR-INGEST-001 — Raw capture
**WHAT:** Persist immutable local SourceEvent envelopes before normalization.  
**WHY:** Replay, provenance and audit require source fidelity.  
**HOW:** Write newline-delimited JSON by source/run/date with hashes and restrictive permissions.  
**DATA / INTERFACES:** SourceEvent v1  
**FAILURE:** Disk-full fails job before graph mutation of uncaptured record.  
**TEST:** Hash/replay/restart tests.  
**COMPLETE WHEN:** Every graph mutation references a captured event.  
**TARGET PHASE:** P1-MVP

### FR-INGEST-002 — Canonicalization
**WHAT:** Normalize source events into typed canonical entities/relationships.  
**WHY:** Cross-source graph logic requires stable contracts.  
**HOW:** Pure/config-driven mappers emit versioned NormalizedEntity/Relationship records.  
**DATA / INTERFACES:** Canonical JSON contracts  
**FAILURE:** Mapper errors are per-record findings/DLQ.  
**TEST:** Golden mapping tests.  
**COMPLETE WHEN:** Same source record maps deterministically for same mapper version.  
**TARGET PHASE:** P1-MVP

### FR-INGEST-003 — Idempotent mutation
**WHAT:** Use deterministic canonical IDs and mutation upserts.  
**WHY:** Repeated sync must not duplicate graph facts.  
**HOW:** Canonical IDs hash namespace/type/source identity; edges use deterministic semantic key.  
**DATA / INTERFACES:** GraphMutation v1  
**FAILURE:** Conflict surfaces validation finding; no blind merge.  
**TEST:** Double-ingest E2E.  
**COMPLETE WHEN:** Second identical run does not increase logical entity/edge counts.  
**TARGET PHASE:** P1-MVP

### FR-INGEST-004 — Ingestion job lifecycle
**WHAT:** Track queued/running/succeeded/partial/failed/cancelled states.  
**WHY:** Admin UI and recovery need truthful state.  
**HOW:** Each run records counts, checkpoint, timings, versions and errors in meta graph and local logs.  
**DATA / INTERFACES:** IngestionRun  
**FAILURE:** Worker crash leaves resumable state.  
**TEST:** State-transition tests.  
**COMPLETE WHEN:** Admin UI reflects actual backend run state.  
**TARGET PHASE:** P1-MVP

### FR-INGEST-005 — Dead-letter processing
**WHAT:** Store rejected events locally with reason/evidence and replay controls.  
**WHY:** Bad records must not block whole imports.  
**HOW:** DLQ files contain event hash, stage, error code, safe message, run ID.  
**DATA / INTERFACES:** DLQ envelope  
**FAILURE:** Secrets/PII are not duplicated beyond allowed capture.  
**TEST:** Malformed fixtures.  
**COMPLETE WHEN:** Rejected records are inspectable and replayable.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-001 — HugeGraph authoritative store
**WHAT:** Use Apache HugeGraph as the authoritative property graph and ontology operational store.  
**WHY:** This is a non-negotiable platform constraint.  
**HOW:** All user-visible entity/relationship truth is resolved from HugeGraph; raw files are evidence, not alternative truth DB.  
**DATA / INTERFACES:** HugeGraph schema/Gremlin  
**FAILURE:** Graph unavailable returns degraded/readiness failure; no shadow DB fallback.  
**TEST:** Startup and persistence tests.  
**COMPLETE WHEN:** All demo graph paths survive service restart.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-002 — Logical graph domains
**WHAT:** Represent Jira, Code, Docs, CI, Provenance, Meta and other domains explicitly within the graph.  
**WHY:** Avoid one undifferentiated graph while preserving native cross-domain traversal.  
**HOW:** MVP uses one physical graph with graph_domain property and domain meta nodes; later physical isolation only by measured need.  
**DATA / INTERFACES:** graph_domain, GraphDomain node  
**FAILURE:** Unknown domain is rejected by schema policy.  
**TEST:** Domain integrity tests.  
**COMPLETE WHEN:** Every business vertex/edge belongs to a valid domain.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-003 — Schema bootstrap
**WHAT:** Initialize property keys, vertex labels, edge labels and indexes idempotently.  
**WHY:** `docker compose up` must create a usable environment.  
**HOW:** Schema bootstrap compares expected schema version before applying additive changes.  
**DATA / INTERFACES:** Schema manifest  
**FAILURE:** Incompatible migration fails startup of app mutation path but preserves DB.  
**TEST:** Fresh/repeat/incompatible schema tests.  
**COMPLETE WHEN:** Fresh stack auto-initializes and second run is no-op.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-004 — Canonical identifiers
**WHAT:** Define deterministic IDs independent of HugeGraph internal IDs where possible.  
**WHY:** Traceability and replay cannot depend on unstable database identifiers.  
**HOW:** canonical_id is the platform identity; source aliases map to it; ambiguous identities stay separate.  
**DATA / INTERFACES:** canonical_id/source_id/source_system  
**FAILURE:** Collision is a blocking validation error.  
**TEST:** Collision/idempotency tests.  
**COMPLETE WHEN:** Every canonical entity has unique stable canonical_id.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-005 — Meta graph
**WHAT:** Model datasets, sources, graph domains, schema/ontology versions, ingestion runs, quality and lineage metadata.  
**WHY:** The query router and admin UI need graph self-description.  
**HOW:** Meta nodes are queryable and link to domain data via INGESTED_IN/BELONGS_TO_DOMAIN/EVIDENCED_BY.  
**DATA / INTERFACES:** Meta entities/edges  
**FAILURE:** Stale meta state is validation finding.  
**TEST:** Meta traversal tests.  
**COMPLETE WHEN:** Admin statistics are derived from graph/meta records.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-006 — Cross-domain bridge edges
**WHAT:** Create explicit, evidence-backed edges between work, code, CI and documents.  
**WHY:** The value proposition is end-to-end enterprise traceability.  
**HOW:** Link deterministic identifiers first (issue keys, commit SHA, paths); inferred links are labeled and scored.  
**DATA / INTERFACES:** IMPLEMENTS, MODIFIES, REFERENCES, DOCUMENTS, PRODUCED_BY  
**FAILURE:** Low-confidence inference never becomes deterministic truth.  
**TEST:** Synthetic E2E path assertions.  
**COMPLETE WHEN:** Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-007 — Gremlin repository
**WHAT:** Centralize parameterized/bounded Gremlin templates.  
**WHY:** Unrestricted model-generated graph queries are unsafe.  
**HOW:** Only named templates and validated QueryPlans reach the graph client in MVP.  
**DATA / INTERFACES:** QueryPlan v1  
**FAILURE:** Unknown template or over-limit request rejected.  
**TEST:** Policy and traversal-bound tests.  
**COMPLETE WHEN:** No UI/agent endpoint can execute arbitrary mutation Gremlin.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-008 — Index strategy
**WHAT:** Create indexes only for measured access patterns.  
**WHY:** Over-indexing increases write/storage cost.  
**HOW:** MVP indexes canonical/source IDs, issue keys, commit SHA, qualified symbol name, path/domain/type and selected timestamps.  
**DATA / INTERFACES:** HugeGraph IndexLabels  
**FAILURE:** Index bootstrap mismatch blocks incompatible mutation.  
**TEST:** Query-plan benchmark tests.  
**COMPLETE WHEN:** Benchmark-critical lookup paths use planned indexes.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-009 — Graph version journal
**WHAT:** Record mutation run, schema/ontology version, first/last seen and validity metadata.  
**WHY:** Reproducibility needs temporal/version context.  
**HOW:** MVP stores revisions/change journal metadata; full snapshots/diffs are P5.  
**DATA / INTERFACES:** revision fields, IngestionRun  
**FAILURE:** Missing version metadata is validation error.  
**TEST:** Replay/version tests.  
**COMPLETE WHEN:** Each changed fact can be attributed to a run/version.  
**TARGET PHASE:** P1-MVP

### FR-GRAPH-010 — RDF/OWL interoperability
**WHAT:** Export platform ontology/data through explicit adapters rather than claiming native RDF/SPARQL.  
**WHY:** Interoperability is useful but HugeGraph is a property graph.  
**HOW:** P2 export maps canonical vocabulary to RDF/OWL; SPARQL, if added, targets an adapter, not raw HugeGraph.  
**DATA / INTERFACES:** RDF/OWL mapping  
**FAILURE:** Unsupported construct reports mapping loss.  
**TEST:** Round-trip fixtures where possible.  
**COMPLETE WHEN:** No documentation claims native SPARQL support.  
**TARGET PHASE:** P2

### FR-ONTO-001 — Enterprise ontology vocabulary
**WHAT:** Version organization, work, code, CI/CD, operations, knowledge and AI/agent concepts.  
**WHY:** Cross-source semantics require a controlled vocabulary.  
**HOW:** Terms have URI/name, definition, domain/range, cardinality and lifecycle status.  
**DATA / INTERFACES:** Ontology manifest  
**FAILURE:** Unknown/deprecated term creates validation error/warning.  
**TEST:** Ontology conformance tests.  
**COMPLETE WHEN:** MVP entities/edges reference ontology version and valid terms.  
**TARGET PHASE:** P1-MVP

### FR-ONTO-002 — Relationship semantics
**WHAT:** Distinguish containment, identity, dependency, implementation, authorship, provenance, temporal and cross-domain semantics.  
**WHY:** Generic RELATED_TO edges destroy explainability.  
**HOW:** Every edge label has explicit domain/range, direction, inverse semantics where relevant and evidence policy.  
**DATA / INTERFACES:** Edge manifest  
**FAILURE:** Invalid endpoints rejected or quarantined.  
**TEST:** Edge domain/range tests.  
**COMPLETE WHEN:** No MVP business relationship relies on untyped generic edge.  
**TARGET PHASE:** P1-MVP

### FR-PROV-001 — Evidence model
**WHAT:** Attach source reference, event hash, extraction time, mapper/parser version, confidence and creation status.  
**WHY:** Answers and inferred links must be defensible.  
**HOW:** Evidence nodes/records link to entities and relationships; DETERMINISTIC/INFERRED/HUMAN_CONFIRMED status is mandatory.  
**DATA / INTERFACES:** Evidence v1  
**FAILURE:** Missing evidence makes inferred fact invalid.  
**TEST:** Provenance coverage tests.  
**COMPLETE WHEN:** MVP evidence coverage is 100% for cross-domain bridge edges.  
**TARGET PHASE:** P1-MVP

### FR-PROV-002 — Provenance traversal
**WHAT:** Support reverse traversal from graph fact to source event and ingestion run.  
**WHY:** Audit/debugging needs chain of custody.  
**HOW:** API exposes evidence references and lineage path.  
**DATA / INTERFACES:** Evidence, SourceEvent, IngestionRun  
**FAILURE:** Missing source artifact is reported, not hidden.  
**TEST:** Lineage API E2E.  
**COMPLETE WHEN:** User can trace demo answer to source fixture/commit metadata.  
**TARGET PHASE:** P1-MVP

### FR-ID-001 — Deterministic identity resolution
**WHAT:** Resolve exact emails, canonical source IDs and configured aliases before fuzzy methods.  
**WHY:** Avoid accidental person/service merging.  
**HOW:** Generate candidate set and auto-merge only deterministic rules.  
**DATA / INTERFACES:** IdentityCandidate  
**FAILURE:** Conflict preserved as separate nodes.  
**TEST:** Alias/conflict tests.  
**COMPLETE WHEN:** Exact aliases merge predictably and retain source aliases.  
**TARGET PHASE:** P1-MVP

### FR-ID-002 — Ambiguous identity candidates
**WHAT:** Never silently merge low-confidence fuzzy matches.  
**WHY:** False identity merges contaminate the enterprise graph.  
**HOW:** Store candidate relationship/confidence for review; human-confirmed merge is future UI.  
**DATA / INTERFACES:** IdentityCandidate  
**FAILURE:** Ambiguous candidates remain separate.  
**TEST:** Fuzzy boundary tests.  
**COMPLETE WHEN:** No fuzzy-only match produces same canonical_id automatically.  
**TARGET PHASE:** P1-MVP

### FR-TEMP-001 — Bitemporal-ready fields
**WHAT:** Store created/modified/deleted, first/last seen, valid_from/valid_to and source_version where available.  
**WHY:** Enterprise topology changes over time.  
**HOW:** MVP writes fields and current-state queries; historical reconstruction/diff is P5.  
**DATA / INTERFACES:** temporal properties  
**FAILURE:** Invalid intervals generate validation findings.  
**TEST:** Temporal validation tests.  
**COMPLETE WHEN:** MVP schema is ready for P5 without ID rewrite.  
**TARGET PHASE:** P1-MVP

### FR-CODE-001 — Deterministic code parser
**WHAT:** Parse source using Tree-sitter/language-specific AST tooling, never LLM as primary parser.  
**WHY:** Code relationships must be reproducible.  
**HOW:** Parser plugins emit File and CodeSymbol records with ranges, qualified names and structural relationships.  
**DATA / INTERFACES:** Repository checkout, parser contracts  
**FAILURE:** Parse errors become file-level findings and do not abort repository.  
**TEST:** Golden parser fixtures.  
**COMPLETE WHEN:** Supported files yield stable symbol graph and exact source ranges.  
**TARGET PHASE:** P1-MVP

### FR-CODE-002 — Python and TypeScript MVP parsing
**WHAT:** Support Python and TypeScript/JavaScript in Phase 1.  
**WHY:** Two common languages prove parser extensibility without over-scoping.  
**HOW:** Tree-sitter grammars/plugins extract modules/classes/functions/methods/imports/calls where statically resolvable.  
**DATA / INTERFACES:** Source files  
**FAILURE:** Unsupported syntax is partial with confidence/status.  
**TEST:** Language-specific fixtures.  
**COMPLETE WHEN:** Demo repo symbols and imports/calls are queryable.  
**TARGET PHASE:** P1-MVP

### FR-CODE-003 — Commit-to-symbol linking
**WHAT:** Relate commits to files and affected symbols using changed ranges/versions where available.  
**WHY:** Requirements must trace below file level.  
**HOW:** MVP maps changed files deterministically and intersects diff hunks with symbol ranges when possible.  
**DATA / INTERFACES:** Git diff metadata, symbols  
**FAILURE:** Ambiguous deleted/renamed symbols produce evidence-backed partial link.  
**TEST:** Rename/diff tests.  
**COMPLETE WHEN:** Demo commit connects to relevant function(s).  
**TARGET PHASE:** P1-MVP

### FR-CODE-004 — Call/import/dependency edges
**WHAT:** Represent calls, imports and package/module dependencies with provenance.  
**WHY:** Impact analysis needs dependency structure.  
**HOW:** Static extractor emits typed edges and marks unresolved/external targets explicitly.  
**DATA / INTERFACES:** AST, manifests  
**FAILURE:** Dynamic calls are not fabricated.  
**TEST:** Static-call fixtures.  
**COMPLETE WHEN:** Blast radius traverses only validated edge classes.  
**TARGET PHASE:** P1-MVP

### FR-CODE-005 — Source navigation
**WHAT:** Preserve repo, revision, path and line/column ranges.  
**WHY:** VS Code must open exact context.  
**HOW:** API returns workspace-relative path plus range and commit/revision evidence.  
**DATA / INTERFACES:** CodeSymbol  
**FAILURE:** Missing local checkout returns context without unsafe file access.  
**TEST:** Navigation contract tests.  
**COMPLETE WHEN:** Extension opens demo symbol at correct range.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-001 — Structured QueryPlan
**WHAT:** Represent user/agent query intent as a typed plan before Gremlin.  
**WHY:** Separates interpretation from execution and enables policy.  
**HOW:** QueryPlan contains intent, anchors, relationship allowlist, depth, filters, limits and evidence mode.  
**DATA / INTERFACES:** QueryPlan v1  
**FAILURE:** Invalid/oversized plans rejected before graph call.  
**TEST:** Schema/property-based tests.  
**COMPLETE WHEN:** All NL and structured requests compile to validated QueryPlan.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-002 — Path query
**WHAT:** Find bounded paths between known entities.  
**WHY:** Core traceability questions are path questions.  
**HOW:** Use template with max depth, relationship allowlist, timeout and result cap.  
**DATA / INTERFACES:** Entity IDs, QueryPlan  
**FAILURE:** No path returns empty evidence-backed result; timeout is explicit.  
**TEST:** Known/unknown/over-depth tests.  
**COMPLETE WHEN:** Demo Jira-to-function path returns expected ordered edges.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-003 — Impact analysis
**WHAT:** Compute directional bounded blast radius using configured impact edge semantics.  
**WHY:** Users need change consequences, not generic neighborhoods.  
**HOW:** Traverse allowlisted dependency/call/implementation edges, dedupe, rank by path length/evidence and report why each node is included.  
**DATA / INTERFACES:** Anchor entity, impact policy  
**FAILURE:** Cycles bounded; partial results marked on timeout.  
**TEST:** Cyclic graph and golden blast-radius tests.  
**COMPLETE WHEN:** Demo function change returns expected dependents with paths.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-004 — Entity search
**WHAT:** Search by canonical/source IDs, issue key, commit SHA, symbol/path and names.  
**WHY:** Users need reliable anchors before traversal.  
**HOW:** Exact/indexed identifiers first; bounded text/name match second.  
**DATA / INTERFACES:** SearchRequest  
**FAILURE:** Broad queries require minimum term and result cap.  
**TEST:** Search relevance/limit tests.  
**COMPLETE WHEN:** Demo Jira issue, commit and symbol are discoverable.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-005 — Natural-language query interpretation
**WHAT:** Interpret supported NL intents locally and safely.  
**WHY:** Natural interaction improves usability without sacrificing graph safety.  
**HOW:** Rule/regex fast path handles canonical questions; local LLM may produce QueryPlan JSON only, never executable Gremlin.  
**DATA / INTERFACES:** NL text, schema snapshot  
**FAILURE:** Model failure falls back to deterministic intents or requests structured refinement.  
**TEST:** Adversarial prompt/query tests.  
**COMPLETE WHEN:** Prompt injection cannot bypass QueryPlan policy.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-006 — Query safety policy
**WHAT:** Enforce traversal depth, result count, timeout, relationship/property allowlists and read-only mode.  
**WHY:** Graph queries can be computationally expensive or destructive.  
**HOW:** Policy validates plans and server-side execution wrapper cancels/limits work where supported.  
**DATA / INTERFACES:** QueryPolicy  
**FAILURE:** Violation returns stable error code and audit event.  
**TEST:** Boundary/fuzz tests.  
**COMPLETE WHEN:** All exposed query endpoints pass policy conformance suite.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-007 — Query evidence envelope
**WHAT:** Every derived result can include paths, fact IDs and evidence references.  
**WHY:** Explainability requires more than answer text.  
**HOW:** API returns answer-independent GraphResult/Evidence objects.  
**DATA / INTERFACES:** GraphResult v1  
**FAILURE:** Missing evidence is visible in result quality.  
**TEST:** Evidence completeness tests.  
**COMPLETE WHEN:** GraphRAG/UI/MCP consume same evidence format.  
**TARGET PHASE:** P1-MVP

### FR-QUERY-008 — Raw Gremlin admin boundary
**WHAT:** Do not expose unrestricted Gremlin to user app, agent or MCP.  
**WHY:** Prevents arbitrary traversal/mutation and injection.  
**HOW:** Developer-only local diagnostic path is disabled by default and never used by normal flows.  
**DATA / INTERFACES:** Admin configuration  
**FAILURE:** Disabled path returns 404/403-like policy response.  
**TEST:** Endpoint exposure tests.  
**COMPLETE WHEN:** No public OpenAPI/MCP tool accepts free-form Gremlin in MVP.  
**TARGET PHASE:** P1-MVP

### FR-VALID-001 — Graph validation rules
**WHAT:** Execute rule packs for orphan, endpoint/domain-range, duplicate, provenance, mandatory edge, type and dangling reference checks.  
**WHY:** Graph correctness must be measurable.  
**HOW:** Rules produce ValidationFinding with rule, severity, entity/edge refs, evidence and remediation.  
**DATA / INTERFACES:** ValidationRun/Finding  
**FAILURE:** Rule failure isolated and reported.  
**TEST:** Seeded-invalid-graph tests.  
**COMPLETE WHEN:** Admin UI shows real findings from demo data.  
**TARGET PHASE:** P1-MVP

### FR-VALID-002 — Validation gates
**WHAT:** Block or quarantine mutations that violate hard invariants; soft rules run post-ingestion.  
**WHY:** Not all quality defects have equal risk.  
**HOW:** ERROR invariants prevent commit; WARN/INFO findings persist.  
**DATA / INTERFACES:** Rule policy  
**FAILURE:** Partial batches are rolled back or safely marked by mutation strategy.  
**TEST:** Hard/soft rule tests.  
**COMPLETE WHEN:** Invalid endpoint edge cannot silently enter graph.  
**TARGET PHASE:** P1-MVP

### FR-VALID-003 — Graph quality metrics
**WHAT:** Compute completeness, freshness, orphan rate, duplicate rate, provenance/evidence coverage and schema compliance.  
**WHY:** Admin users need trendable graph health.  
**HOW:** Metrics derive from validation and graph stats; MVP computes per run/domain.  
**DATA / INTERFACES:** QualitySnapshot  
**FAILURE:** Unknown denominator reported as N/A, not false zero/100%.  
**TEST:** Metric fixture tests.  
**COMPLETE WHEN:** Dashboard values reconcile with fixture counts.  
**TARGET PHASE:** P1-MVP

### FR-RAG-001 — Retrieval router
**WHAT:** Choose direct graph, linked documents, code context, graph+text hybrid or no retrieval.  
**WHY:** Avoid unnecessary LLM/vector infrastructure and token use.  
**HOW:** Deterministic intent rules first; pluggable local classifier later.  
**DATA / INTERFACES:** RetrievalRequest  
**FAILURE:** Unknown intent chooses conservative graph/search path.  
**TEST:** Router table tests.  
**COMPLETE WHEN:** Known MVP questions route without external service.  
**TARGET PHASE:** P1-MVP

### FR-RAG-002 — GraphRAG evidence retrieval
**WHAT:** Retrieve entities, relationships, paths, neighborhoods, provenance and linked documents.  
**WHY:** Answers must be grounded in authoritative graph context.  
**HOW:** Convert bounded GraphResult into context blocks with stable citations.  
**DATA / INTERFACES:** GraphResult/Evidence  
**FAILURE:** Insufficient evidence yields explicit insufficiency, not invention.  
**TEST:** Golden question/evidence tests.  
**COMPLETE WHEN:** Demo GraphRAG answer cites graph/source references.  
**TARGET PHASE:** P1-MVP

### FR-RAG-003 — Local model abstraction
**WHAT:** Provide model interface for chat/generation and optional embeddings with all external providers disabled in MVP.  
**WHY:** Local-first is non-negotiable and future providers must not leak enterprise data.  
**HOW:** Configuration supports a local OpenAI-compatible/Ollama-style adapter; external adapter code is disabled by policy.  
**DATA / INTERFACES:** ModelRequest/Response  
**FAILURE:** Model-down degrades to graph results and deterministic summaries.  
**TEST:** No-egress/model-down tests.  
**COMPLETE WHEN:** Core search/path/impact remains usable with model service stopped.  
**TARGET PHASE:** P1-MVP

### FR-RAG-004 — No mandatory vector DB in MVP
**WHAT:** Do not require a second database for semantic retrieval in Phase 1.  
**WHY:** Infrastructure must stay minimal.  
**HOW:** Use graph, metadata, document sections and local lexical retrieval; optional embeddings may be evaluated in-process/file-indexed.  
**DATA / INTERFACES:** DocumentSection  
**FAILURE:** Semantic-only request reports reduced capability if embeddings disabled.  
**TEST:** Model-off tests.  
**COMPLETE WHEN:** MVP starts and demos without vector database.  
**TARGET PHASE:** P1-MVP

### FR-RAG-005 — RAG evaluation harness
**WHAT:** Measure retrieval precision/recall, context relevance, evidence coverage, groundedness, answer correctness, latency and token usage.  
**WHY:** RAG quality must be testable.  
**HOW:** Golden QA dataset includes expected entities/paths/evidence.  
**DATA / INTERFACES:** EvalCase/EvalResult  
**FAILURE:** Failed generation does not erase retrieval metrics.  
**TEST:** Automated evaluation tests.  
**COMPLETE WHEN:** Baseline report is reproducible locally.  
**TARGET PHASE:** P1-MVP

### FR-RAG-006 — Adaptive RAG strategy framework
**WHAT:** Expose strategy interface for simple/graph/hybrid/corrective/self/adaptive/agentic/multi-hop variants without instantiating all.  
**WHY:** Future expansion should not rewrite retrieval.  
**HOW:** Strategy selected by router and capability/config; Phase 3 adds advanced variants based on evaluation.  
**DATA / INTERFACES:** RAGStrategy  
**FAILURE:** Unsupported strategy rejected cleanly.  
**TEST:** Strategy contract tests.  
**COMPLETE WHEN:** P3 can add strategy plugin without changing callers.  
**TARGET PHASE:** P3

### FR-AGENT-001 — Agent contract
**WHAT:** Define ID/type/purpose/input/output/capabilities/tools/model/memory/policies/time/budget/retry/failure/evidence/audit fields.  
**WHY:** Agents require enforceable runtime contracts.  
**HOW:** Registry loads versioned YAML/JSON definitions and validates before execution.  
**DATA / INTERFACES:** AgentContract  
**FAILURE:** Invalid contract cannot register.  
**TEST:** Schema tests.  
**COMPLETE WHEN:** Every enabled agent has a validated contract.  
**TARGET PHASE:** P1-MVP

### FR-AGENT-002 — Bounded agent runtime
**WHAT:** Enforce maximum steps/retries/recursion/time/model/tool budgets and circuit breaker.  
**WHY:** Prevents unbounded loops and resource use.  
**HOW:** Runtime state machine records route/context/plan/tool/observation/evaluation/result/audit.  
**DATA / INTERFACES:** AgentRun  
**FAILURE:** Budget exhaustion terminates with partial evidence.  
**TEST:** Loop/budget tests.  
**COMPLETE WHEN:** Agent cannot exceed configured execution envelope.  
**TARGET PHASE:** P1-MVP

### FR-AGENT-003 — TraceImpact agent
**WHAT:** Provide one useful read-only MVP workflow that answers requirement/code trace and impact questions.  
**WHY:** MVP requires a real agent without unsafe write autonomy.  
**HOW:** Agent composes search/path/impact/retrieval tools and returns evidence summary.  
**DATA / INTERFACES:** AgentRequest/AgentResult  
**FAILURE:** Tool/model failures are surfaced with partial structured result.  
**TEST:** Golden E2E agent tests.  
**COMPLETE WHEN:** Same demo question works via UI/API/MCP context.  
**TARGET PHASE:** P1-MVP

### FR-AGENT-004 — Write/action approval boundary
**WHAT:** Separate read tools from write/destructive tools and require explicit confirmation for future write actions.  
**WHY:** Agent autonomy must not bypass human control.  
**HOW:** MVP registers read tools only; future action registry includes risk/reversibility/approval policy.  
**DATA / INTERFACES:** ToolContract  
**FAILURE:** Unapproved write invocation denied/audited.  
**TEST:** Negative policy tests.  
**COMPLETE WHEN:** No MVP agent can mutate source systems or code.  
**TARGET PHASE:** P1-MVP

### FR-AGENT-005 — Controlled self-modification
**WHAT:** Self-learning/evolving/writing capabilities remain disabled until governance, sandboxing, tests and approval exist.  
**WHY:** Autonomous self-change is high risk.  
**HOW:** Architecture reserves versioned proposal/sandbox interfaces only; implementation is P8+.  
**DATA / INTERFACES:** ChangeProposal  
**FAILURE:** Any runtime self-edit request denied in earlier phases.  
**TEST:** Policy tests.  
**COMPLETE WHEN:** No production self-modification path exists before P8+.  
**TARGET PHASE:** P8+

### FR-MEM-001 — Scoped memory records
**WHAT:** Model working/task/conversation/semantic/episodic/procedural memory with scope/source/TTL/provenance/confidence/classification/deletion policy.  
**WHY:** Agent memory must be governable.  
**HOW:** MVP persists only task/audit evidence needed for TraceImpact; broad long-term memory is later.  
**DATA / INTERFACES:** MemoryRecord  
**FAILURE:** Expired/forbidden memory excluded.  
**TEST:** TTL/scope tests.  
**COMPLETE WHEN:** No uncontrolled accumulation in MVP.  
**TARGET PHASE:** P1-MVP

### FR-MCP-001 — MCP read server
**WHAT:** Expose search_entity/get_entity/neighbors/path/query/impact/code/jira/document/lineage/evidence as local MCP tools/resources.  
**WHY:** Developer and agent clients need standard context access.  
**HOW:** Thin adapter calls same application services and policy layer as REST.  
**DATA / INTERFACES:** MCP tool schemas  
**FAILURE:** Backend/policy errors map to structured MCP errors.  
**TEST:** MCP contract/E2E tests.  
**COMPLETE WHEN:** MCP returns same graph evidence as REST for demo case.  
**TARGET PHASE:** P1-MVP

### FR-MCP-002 — MCP action separation
**WHAT:** Keep write/action tools in separate registry and disabled in MVP.  
**WHY:** Protocol access must not expand authority.  
**HOW:** Action tools require explicit config, risk policy and confirmation in later phases.  
**DATA / INTERFACES:** ToolRegistry  
**FAILURE:** Disabled writes are not advertised.  
**TEST:** Capability-list tests.  
**COMPLETE WHEN:** MVP MCP surface is read-only.  
**TARGET PHASE:** P1-MVP

### FR-UI-001 — User web application
**WHAT:** Provide search/NL query, graph visualization, details/evidence, path and impact views backed by real APIs.  
**WHY:** MVP must demonstrate value interactively.  
**HOW:** React/TypeScript app uses /api/v1; no hardcoded domain responses.  
**DATA / INTERFACES:** REST/SSE  
**FAILURE:** API failure shows explicit degraded/error state.  
**TEST:** Component + Playwright E2E.  
**COMPLETE WHEN:** Demo flow works from persisted data.  
**TARGET PHASE:** P1-MVP

### FR-UI-002 — Graph explorer
**WHAT:** Visualize typed nodes/edges with filters, expansion, path highlighting and provenance.  
**WHY:** Users need interpretable graph navigation.  
**HOW:** Cytoscape.js loaded locally; server returns bounded subgraphs.  
**DATA / INTERFACES:** GraphResult  
**FAILURE:** Large result prompts/refuses expansion beyond cap.  
**TEST:** Visual E2E + API bounds.  
**COMPLETE WHEN:** Demo path is highlighted with evidence access.  
**TARGET PHASE:** P1-MVP

### FR-ADMIN-001 — Admin ingestion UI
**WHAT:** Show connectors, runs, status, counts, errors, replay/dry-run controls.  
**WHY:** Operations must reflect real system state.  
**HOW:** Admin routes call ingestion APIs; URL separation is not authorization.  
**DATA / INTERFACES:** IngestionRun  
**FAILURE:** Actions validate local auth/confirmation.  
**TEST:** Admin E2E.  
**COMPLETE WHEN:** Run state reconciles with backend/meta graph.  
**TARGET PHASE:** P1-MVP

### FR-ADMIN-002 — Admin graph quality UI
**WHAT:** Show graph stats, validation findings, quality metrics, schema/ontology versions and backup state.  
**WHY:** Demonstrates maintainability and trust.  
**HOW:** All values queried from APIs/meta graph.  
**DATA / INTERFACES:** QualitySnapshot  
**FAILURE:** Missing metric displayed as unavailable.  
**TEST:** Fixture reconciliation tests.  
**COMPLETE WHEN:** No dashboard KPI is hardcoded.  
**TARGET PHASE:** P1-MVP

### FR-VSCODE-001 — VS Code context extension
**WHAT:** Provide sidebar/webview showing current file/symbol, Jira, commits, dependencies, docs and provenance.  
**WHY:** Developer workflow is a required product surface.  
**HOW:** Extension resolves local workspace path/symbol and calls platform API over configured local endpoint.  
**DATA / INTERFACES:** Extension API contract  
**FAILURE:** Unavailable platform shows offline state; no source modification.  
**TEST:** Extension host tests.  
**COMPLETE WHEN:** Opening demo function retrieves correct graph context.  
**TARGET PHASE:** P1-MVP

### FR-VSCODE-002 — VS Code trace/impact commands
**WHAT:** Commands answer why code exists and what change may affect.  
**WHY:** Makes enterprise graph actionable in editor.  
**HOW:** Commands invoke path/impact services and render evidence.  
**DATA / INTERFACES:** Query API  
**FAILURE:** No unrestricted Gremlin/tool execution.  
**TEST:** Command E2E.  
**COMPLETE WHEN:** Demo command returns Jira→code path and impact.  
**TARGET PHASE:** P1-MVP
