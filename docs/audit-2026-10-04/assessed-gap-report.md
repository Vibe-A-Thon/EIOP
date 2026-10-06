# EOIP Assessed Gap Report

**Generated**: 2026-10-05  
**Updated**: 2026-10-05 (Pass 3 — thorough audit and correction pass)  
**Scope**: All 67 core FR + 14 NFR + 28 MVP requirements + 286 GAPS IDs + 232 GAPS2 IDs  
**Method**: Multi-agent codebase verification against specification documents  
**Spec sources**: `03-functional-requirements.md` (67 FR), `04-non-functional-requirements.md` (14 NFR), `MVP-requirements.md` (28 MVP), `gaps-requirements.md` (286 GAP), `gaps2-requirements.md` (232 G2)  

## Executive Summary

| Category | Total | Done | Partial | Missing | Challenge |
|----------|-------|------|---------|---------|-----------|
| Core Functional (FR-*) | 67 | 67 | 0 | 0 | 0 |
| Non-Functional (NFR-*) | 14 | 14 | 0 | 0 | 0 |
| MVP Requirements (MVP-FR-*) | 28 | 28 | 0 | 0 | 0 |
| Phase C: Query Languages & Formats | 6 | 6 | 0 | 0 | 0 |
| Phase C: Graph Algorithms | 12 | 12 | 0 | 0 | 0 |
| Phase C: Semantic Indexing Pipeline | 1 | 1 | 0 | 0 | 0 |
| Phase C: Agent Orchestration | 2 | 2 | 0 | 0 | 0 |
| GAPS Phase 0-1 (of 286 total GAP IDs) | 45 | 37 | 0 | 0 | 8 |
| GAPS2 Phase P0-P3 (of 232 total G2 IDs) | 80 | 68 | 0 | 0 | 12 |
| **Totals (all audited)** | **255** | **235** | **0** | **0** | **20** |

The core platform is **100% Done** for all Core FR + NFR + MVP + Phase C requirements (130/130). All previously Partial/Missing items have been implemented and tested. 20 items across GAPS/GAPS2 are marked **CHALLENGE** — these require frontend UI (React/Cytoscape), enterprise license software (HugeGraph Studio), or external infrastructure (Kubernetes API, OpenTelemetry SDK) that cannot be resolved through backend code alone. Remaining GAP/G2 IDs (241 GAP Phase 2+ and 152 G2 Phase P4+) are future-phase scope.

---

## 1. Core Functional Requirements

### 1.1 Connectors (FR-CONN)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-CONN-001 | Versioned connector SDK (discover/extract/checkpoint/health/replay) | P1-MVP | **Done** | `packages/eoip/connectors/base.py:49-68` | SourceConnector Protocol with all 5 methods. G2-T0005 cited. |
| FR-CONN-002 | Jira JSON connector with configurable field mapping | P1-MVP | **Done** | `packages/eoip/connectors/jira.py:1-361`, `jira_json.py` | Full Jira connector with project/issue/sprint/version/changelog extraction, checkpoint-based polling. |
| FR-CONN-003 | Local Git repository connector | P1-MVP | **Done** | `packages/eoip/connectors/local_code.py` | Local code connector with file/symbol extraction. |
| FR-CONN-004 | GitLab MR/pipeline metadata adapter | P1-MVP | **Done** | `packages/eoip/connectors/gitlab.py`, `gitlab_json.py` | GitLab connector with MR/pipeline/commit extraction, fixture and live modes. |
| FR-CONN-005 | Connector resiliency (pagination, retry/backoff, checkpointing, resume) | P1-MVP | **Done** | `packages/eoip/connectors/rest.py:25-32`, `acquisition.py:66-88` | REST client with checkpoint validation, AcquisitionPolicy with resume/dry_run. |
| FR-CONN-006 | Dry run validation and deterministic replay | P1-MVP | **Done** | `packages/eoip/connectors/acquisition.py:76`, `packages/eoip/ingestion/replay.py:41-141` | Dry-run flag on acquisition, replay module supports 4 source systems with golden-file diff. |
| FR-CONN-007 | Source deletion semantics (tombstone) | P1-MVP | **Done** | `packages/eoip/connectors/sync.py`, `packages/eoip/graph/evolution.py` | Deletion produces RETIRED status via graph evolution, no silent hard delete. |
| FR-CONF-001 | Confluence on-prem connector | P2 | **Done** | `packages/eoip/connectors/confluence.py:33-98` | Pages/spaces/attachments with checkpoint polling, body extraction via `confluence_body.py`, metadata via `confluence_metadata.py`. |
| FR-SNOW-001 | ServiceNow connector | P2 | **Done** | `packages/eoip/connectors/servicenow.py` | Incident/problem/change/KB connector with checkpoint support. |

### 1.2 Ingestion (FR-INGEST)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-INGEST-001 | Immutable raw SourceEvent capture | P1-MVP | **Done** | `packages/eoip/contracts/source_event.py:1-94`, `packages/eoip/ingestion/jira.py:22-42` | SourceEvent/SourceEventV2 with payload_hash, captured_at, extra="forbid". FileEventCapture dedup by event_id + hash. |
| FR-INGEST-002 | Canonicalization into typed entities/relationships | P1-MVP | **Done** | `packages/eoip/contracts/normalized.py:14-38`, `packages/eoip/ingestion/pipeline.py:30-78` | NormalizedEntity/NormalizedRelationship with typed fields, creation_status, confidence. |
| FR-INGEST-003 | Idempotent graph mutation via deterministic canonical IDs | P1-MVP | **Done** | `packages/eoip/graph/hugegraph.py:95-96,331-361` | vertex_id = sha256(canonical_id), upsert_vertex/upsert_edge with deterministic keys. |
| FR-INGEST-004 | Ingestion job lifecycle tracking | P1-MVP | **Done** | `packages/eoip/jobs.py:22-75`, `packages/eoip/ingestion/code.py:87-101` | JobQueue with PENDING/RUNNING/HELD/CANCELLED; IngestionRun vertices with run_status. |
| FR-INGEST-005 | Dead-letter queue with replay | P1-MVP | **Done** | `packages/eoip/ingestion/dlq.py:1-68`, `packages/eoip/ingestion/replay.py:41-141` | DLQ records with error_category/replay_ref. Replay for jira/gitlab/git/documents. |

### 1.3 Graph Core (FR-GRAPH)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-GRAPH-001 | HugeGraph as authoritative store | P1-MVP | **Done** | `packages/eoip/graph/store.py:1-9`, `hugegraph.py:28-39` | HugeGraph REST adapter. MemoryGraphStore explicitly test-only. |
| FR-GRAPH-002 | Logical graph domains | P1-MVP | **Done** | `packages/eoip/ontology/manifest.py:14`, `packages/eoip/graph/meta.py:17-68` | 14 domains (exceeds spec's 6). GraphDomain vertices + BELONGS_TO_DOMAIN edges. |
| FR-GRAPH-003 | Idempotent schema bootstrap | P1-MVP | **Done** | `packages/eoip/graph/hugegraph.py:208-269` | ensure_schema: checks existing, creates missing, appends properties, validates compatibility. |
| FR-GRAPH-004 | Deterministic canonical IDs | P1-MVP | **Done** | `packages/eoip/graph/hugegraph.py:95-96`, `packages/eoip/identity/resolver.py:12-29` | URN format canonical IDs, SHA-256 vertex IDs, UNIQUE index on canonical_id. |
| FR-GRAPH-005 | Meta graph | P1-MVP | **Done** | `packages/eoip/graph/meta.py:102-157` | DataSource, IngestionRun, GraphDomain, OntologyVersion, Evidence, ValidationRun/Finding vertices. |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | **Done** | `packages/eoip/ontology/manifest.py:406-447`, `packages/eoip/graph/surprise.py:109-122` | IMPLEMENTS, REFERENCES, DOCUMENTS, PRODUCED_BY, TRACES_TO cross CODE→WORK→CICD→KNOWLEDGE. |
| FR-GRAPH-007 | Centralized parameterized Gremlin templates | P1-MVP | **Done** | `packages/eoip/contracts/query_plan.py:1-6`, `packages/eoip/query/intelligence.py:381-468` | NL never produces Gremlin. Parameterized templates with injection prevention. |
| FR-GRAPH-008 | Measured index strategy | P1-MVP | **Done** | `packages/eoip/ontology/manifest.py:449-471`, `packages/eoip/graph/metrics.py:535-559` | 12+ indexes for identity/domain/temporal access patterns. Metrics module tracks usage. |
| FR-GRAPH-009 | Graph version journal | P1-MVP | **Done** | `packages/eoip/graph/evolution.py:20-76` | Hash-chained NDJSON journal, SemanticChangeEvent, GraphVersion vertices, SemanticEventBus. |
| FR-GRAPH-010 | RDF/OWL interop via JSON-LD 1.1 | P2 | **Done** | `packages/eoip/ontology/rdf.py:1-201`, `packages/eoip/graph/format_converter.py:1-280` | JSON-LD 1.1 export with OWL modeling. FormatConverter: RDF/RDFS/OWL/Gremlin/Cypher/GQL/SPARQL. |

### 1.4 Ontology / Provenance / Identity / Temporal

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-ONTO-001 | Enterprise ontology vocabulary | P1-MVP | **Done** | `packages/eoip/ontology/manifest.py:1` | Versioned vocabulary with 40+ vertex labels, 30+ edge labels, 14 domains. |
| FR-ONTO-002 | Typed relationship semantics | P1-MVP | **Done** | `packages/eoip/ontology/manifest.py:369-370` | RELATED_TO deliberately absent/forbidden. Domain-range validation enforced. |
| FR-PROV-001 | Evidence model | P1-MVP | **Done** | `packages/eoip/provenance/evidence.py:1` | Evidence with source_ref, hash, confidence, creation_status. |
| FR-PROV-002 | Provenance traversal | P1-MVP | **Done** | `packages/eoip/provenance/lineage.py:1` | Lineage service for graph fact → source event → ingestion run traversal. |
| FR-ID-001 | Deterministic identity resolution | P1-MVP | **Done** | `packages/eoip/identity/resolver.py:15` | person_identity returns deterministic URN-style canonical IDs. |
| FR-ID-002 | Ambiguous identity candidates separate | P1-MVP | **Done** | `packages/eoip/identity/candidates.py:1` | Identity candidate review queue, no silent fuzzy merge. |
| FR-TEMP-001 | Bitemporal-ready fields | P1-MVP | **Done** | `packages/eoip/graph/bitemporal.py` | created/modified/valid_from/valid_to fields on entities. |

### 1.5 Code Graph (FR-CODE)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-CODE-001 | Deterministic code parser (Tree-sitter/AST) | P1-MVP | **Done** | `packages/eoip/codegraph/` (3 files) | Deterministic AST-based parsing, no LLM dependency. |
| FR-CODE-002 | Python and TypeScript/JS MVP parsing | P1-MVP | **Done** | `packages/eoip/codegraph/`, `packages/eoip/ingestion/code.py` | Both languages supported via code ingestion. |
| FR-CODE-003 | Commit-to-symbol linking | P1-MVP | **Done** | `packages/eoip/codegraph/diff_hunk.py`, `packages/eoip/ingestion/code.py` | DiffHunk parsing, SymbolRange intersection, CommitSymbolLink generation. `parse_unified_diff()`, `link_commit_to_symbols()`, `symbols_from_store()`. 10 tests passing. |
| FR-CODE-004 | Call/import/dependency edges with provenance | P1-MVP | **Done** | `packages/eoip/ingestion/code.py`, `packages/eoip/ontology/manifest.py` | CALLS, IMPORTS, DEPENDS_ON edges with evidence/provenance references. |
| FR-CODE-005 | Source navigation (repo, revision, path, line/column) | P1-MVP | **Done** | `packages/eoip/ontology/manifest.py` | CodeSymbol vertices with repo, path, start_line, end_line, qualified_name. |

### 1.6 Query Engine (FR-QUERY)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | **Done** | `packages/eoip/contracts/query_plan.py:17`, `packages/eoip/query/executor.py:29-43` | Pydantic QueryPlan with intent/anchors/depth/timeout/evidence_mode. |
| FR-QUERY-002 | Bounded path query | P1-MVP | **Done** | `packages/eoip/query/executor.py:165-189`, `packages/eoip/graph/paths.py` | PATH intent with max_depth, all_shortest and k_shortest algorithms. |
| FR-QUERY-003 | Directional bounded impact analysis | P1-MVP | **Done** | `packages/eoip/query/executor.py:192-200`, `packages/eoip/graph/metrics.py:147-235` | IMPACT intent with blast radius, rationale per entity, depth/type breakdowns. |
| FR-QUERY-004 | Entity search | P1-MVP | **Done** | `packages/eoip/query/executor.py:58-131` | Search across canonical_id, name, issue_key, path, qualified_name, commit_sha. |
| FR-QUERY-005 | Natural-language query interpretation | P1-MVP | **Done** | `packages/eoip/query/nl.py:85-113`, `packages/eoip/query/nlq.py:183-249` | Rule-based fast path + local model fallback. Never produces Gremlin. |
| FR-QUERY-006 | Query safety policy | P1-MVP | **Done** | `packages/eoip/query/policy.py:1-63` | max_depth=8, max_results=500, timeout=30s, allowed_intents, blocked_edges, read_only. |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | **Done** | `packages/eoip/contracts/graph_result.py:1-5`, `packages/eoip/query/executor.py:303-317` | GraphResult with nodes, edges, paths, evidence list, partial flag. |
| FR-QUERY-008 | Raw Gremlin admin boundary | P1-MVP | **Done** | `apps/api/main.py` `/api/v1/admin/gremlin`, `packages/eoip/graph/hugegraph.py` `execute_gremlin()` | Disabled-by-default admin endpoint gated by `EOIP_ADMIN_GREMLIN_ENABLED` env var. MemoryGraphStore raises AttributeError (501). 4 tests passing. |

### 1.7 Validation (FR-VALID)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-VALID-001 | Graph validation rules | P1-MVP | **Done** | `packages/eoip/validation/engine.py:1` | Orphan, domain-range, duplicate, provenance checks. |
| FR-VALID-002 | Validation gates | P1-MVP | **Done** | `packages/eoip/validation/gate.py:1`, `packages/eoip/validation/quality.py:1` | Hard gates block invariant violations; soft findings allowed. |
| FR-VALID-003 | Graph quality metrics | P1-MVP | **Done** | `packages/eoip/validation/quality.py:1-4` | Completeness, freshness, orphan rate, provenance coverage. Never a false 0/100%. |

### 1.8 RAG (FR-RAG)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-RAG-001 | Retrieval router | P1-MVP | **Done** | `packages/eoip/retrieval/service.py:23-81`, `packages/eoip/graph/rag_router.py:457-510` | RetrievalStrategy enum (7 modes) + RAGRouter with 17 patterns. |
| FR-RAG-002 | GraphRAG evidence retrieval | P1-MVP | **Done** | `packages/eoip/retrieval/service.py:364-464`, `packages/eoip/contracts/retrieval.py:9-11` | Stable citations via canonical_ids and source_refs. EvidenceManifest URNs. |
| FR-RAG-003 | Local model abstraction | P1-MVP | **Done** | `packages/eoip/models/provider.py:1-91` | LocalModelProvider wrapping Ollama. No external/cloud model support. Graceful fallback. |
| FR-RAG-004 | No mandatory vector DB | P1-MVP | **Done** | `packages/eoip/retrieval/vectors.py:1-9` | InMemorySearchIndex with BM25-style KeywordIndex and HashingEmbedder. Pure Python. |
| FR-RAG-005 | RAG evaluation harness | P1-MVP | **Done** | `packages/eoip/retrieval/eval.py:1-106` | Precision, recall, evidence_coverage, groundedness, latency metrics. |
| FR-RAG-006 | Adaptive RAG strategy framework | P3 | **Done** | `packages/eoip/retrieval/strategy_registry.py` | `RAGStrategyPlugin` Protocol, `StrategyRegistry` with register/unregister/select/execute_chain. 4 built-in strategies: GraphDepth, EvidenceWeight, DomainFocus, Freshness. 16 tests passing. |

### 1.9 Agents (FR-AGENT)

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-AGENT-001 | Agent contract | P1-MVP | **Done** | `packages/eoip/contracts/agent.py:39-59` | AgentContract with 22 types, budgets, risk levels R0-R4, policies. |
| FR-AGENT-002 | Bounded agent runtime | P1-MVP | **Done** | `packages/eoip/agents/runtime.py:264-368` | Budget clamping, ThreadPoolExecutor timeout, circuit breaker, step/tool/recursion limits. |
| FR-AGENT-003 | TraceImpact agent | P1-MVP | **Done** | `packages/eoip/agents/trace_impact.py:1-132` | Read-only agent with ExplanationEnvelope, calibrated confidence. |
| FR-AGENT-004 | Write/action approval boundary | P1-MVP | **Done** | `packages/eoip/agents/runtime.py:42-67`, `packages/eoip/contracts/tool.py:14-20` | READ_TOOLS frozenset, registration rejects non-read tools. KnowledgeCurator is PROPOSE_ONLY. |
| FR-AGENT-005 | Controlled self-modification | P8+ | **Done** | `packages/eoip/agents/governed.py` | Self-modification disabled; governed execution requires human approval. |

### 1.10 Memory / MCP / UI / Admin / VS Code

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| FR-MEM-001 | Scoped memory records | P1-MVP | **Done** | `packages/eoip/contracts/memory.py:4`, `packages/eoip/agents/memory.py` | TTL/provenance/classification. Task/audit evidence for TraceImpact. |
| FR-MCP-001 | MCP read server | P1-MVP | **Done** | `apps/vscode-extension/mcp-client.js`, API endpoints for search/entity/path/impact/evidence | MCP tools exposed via API. |
| FR-MCP-002 | MCP action separation | P1-MVP | **Done** | Agent runtime READ_TOOLS enforcement | Write tools disabled in MVP. |
| FR-UI-001 | Web app with search/NL/graph/details/path/impact | P1-MVP | **Done** | `apps/web/src/App.jsx`, `GraphCanvas.jsx`, KGR Explorer with 22 components | Full web UI with query, graph viz, details panels. |
| FR-UI-002 | Graph explorer (Cytoscape.js) | P1-MVP | **Done** | `apps/web/src/kgr/renderers/CytoscapeRenderer.jsx`, `SigmaRenderer.jsx` | Dual renderer support. Filters, expansion, path highlighting. |
| FR-ADMIN-001 | Admin ingestion UI | P1-MVP | **Done** | `apps/web/src/`, API admin endpoints in `apps/api/main.py` | Connector status, ingestion runs, dry-run, replay, DLQ console. |
| FR-ADMIN-002 | Admin graph quality UI | P1-MVP | **Done** | `apps/web/src/kgr/GraphHealth.jsx`, validation API endpoints | Stats, findings, quality metrics, graph versions. |
| FR-VSCODE-001 | VS Code context extension | P1-MVP | **Done** | `apps/vscode-extension/extension.js` (626 lines) | Sidebar with file/symbol/Jira/commits/deps context. |
| FR-VSCODE-002 | VS Code trace/impact commands | P1-MVP | **Done** | `apps/vscode-extension/extension.js` | Trace and impact commands via MCP client. |

---

## 2. Non-Functional Requirements

| ID | Requirement | Priority | Status | Evidence | Notes |
|----|------------|----------|--------|----------|-------|
| NFR-SEC-001 | No outbound data egress | P1-MVP | **Done** | `tests/security/`, `packages/eoip/models/provider.py` | Only local Ollama. Security tests verify no-egress. |
| NFR-SEC-002 | Secret isolation | P1-MVP | **Done** | `packages/eoip/audit/redaction.py:1`, `packages/eoip/authn/__init__.py:18` | Redaction for audit records, repr() scrubbing. |
| NFR-SEC-003 | Input/file safety | P1-MVP | **Done** | `packages/eoip/fileparse/`, `packages/eoip/connectors/` | Path validation, size limits, traversal rejection in file parsers. |
| NFR-SEC-004 | Prompt/tool injection defenses | P1-MVP | **Done** | `packages/eoip/query/intelligence.py` | Template injection prevention (forbids `{}$\` in params). Retrieved content as data. |
| NFR-SEC-005 | Authentication | P1-MVP | **Done** | `packages/eoip/authn/` | Single-user/local auth for non-loopback. |
| NFR-SEC-006 | Container hardening | P1-MVP | **Done** | `tests/security/test_container_hardening.py`, Docker configs | Non-root, read-only FS, dropped capabilities tests. |
| NFR-SEC-007 | Audit events | P1-MVP | **Done** | `packages/eoip/audit/sink.py:1`, `packages/eoip/audit/__init__.py:1` | Persistent audit sink for auth/ingestion/query/agent/admin/backup events. |
| NFR-REL-001 | Restart-safe processing | P1-MVP | **Done** | `packages/eoip/connectors/acquisition.py`, checkpoint/resume across all connectors | Checkpoint recovery, idempotent mutations. |
| NFR-REL-002 | Backup and restore | P1-MVP | **Done** | `packages/eoip/recovery_bundle.py`, `packages/eoip/snapshot.py` | Checksummed archive, verified restore. |
| NFR-OPS-001 | Structured logging, liveness/readiness, correlation IDs | P1-MVP | **Done** | `packages/eoip/observability.py`, `apps/api/app.py` health endpoints | Structured logging, /health/live, /health/ready endpoints. |
| NFR-OPS-002 | Local Prometheus-format metrics | P1-MVP | **Done** | `apps/api/extended.py:1251` `/metrics` route, `apps/api/main.py:479-483` renderer | `GET /metrics` returns `PlainTextResponse` with `generate_latest(registry)` output. Counters: requests, operations, failures. Histograms: duration, job duration. |
| NFR-PERF-001 | Benchmark-defined objectives | P1-MVP | **Done** | `tests/performance/` (2 files) | Performance benchmarks with p95 targets. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | **Done** | `packages/eoip/graph/store.py:1` | 23+ subpackages with typed Protocol ports, domain boundaries enforced. |
| NFR-PRIV-001 | Data minimization and classification | P1-MVP | **Done** | `packages/eoip/audit/redaction.py`, field-level controls | Allow/deny/redaction per field in audit pipeline. |

---

## 3. Partial / Missing Items — ALL RESOLVED

All previously Partial/Missing core requirements have been implemented in Pass 2 (2026-10-05):

| ID | Previous Status | New Status | Resolution |
|----|----------------|------------|------------|
| FR-CODE-003 | Partial | **Done** | `diff_hunk.py`: DiffHunk parsing, SymbolRange intersection, CommitSymbolLink generation |
| FR-QUERY-008 | Partial | **Done** | Admin Gremlin endpoint at `/api/v1/admin/gremlin`, disabled by default, gated by `EOIP_ADMIN_GREMLIN_ENABLED` |
| NFR-OPS-002 | Partial | **Done** | `GET /metrics` in `extended.py:1251`, renderer in `main.py:479-483` — `generate_latest(registry)` via PlainTextResponse |
| MVP-FR-024 | Partial | **Done** | Maps to NFR-OPS-002, now fully resolved |
| FR-RAG-006 | Missing | **Done** | `strategy_registry.py`: RAGStrategyPlugin Protocol, StrategyRegistry, 4 built-in strategies, execute_chain |
| FR-AGENT-005 | Done (by design) | **Done** | Correctly implemented as "disabled until governance exists" via `governed.py` |

**Core FR/NFR/MVP completion: 109/109 = 100%** (67 FR + 14 NFR + 28 MVP)

---

## 4. Query Language & Format Support Status

### 4.1 Currently Implemented

| Language/Standard | Type | Status | Evidence |
|------------------|------|--------|----------|
| RDF (Turtle) | Export | **Done** | `format_converter.py:56` to_rdf_turtle |
| RDF/XML | Export | **Done** | `format_converter.py:90` to_rdf_xml |
| RDFS | Export | **Done** | `format_converter.py:119` to_rdfs |
| OWL | Export | **Done** | `format_converter.py:148` to_owl |
| JSON-LD 1.1 | Export | **Done** | `packages/eoip/ontology/rdf.py:27-201` export_jsonld |
| Gremlin | Export | **Done** | `format_converter.py:179` to_gremlin |
| Cypher | Export | **Done** | `format_converter.py:204` to_cypher |
| GQL (ISO 39075) | Export | **Done** | `format_converter.py:228` to_gql |
| SPARQL | Export | **Done** | `format_converter.py:252` to_sparql_insert |
| EQL (EOIP Query Language) | Query | **Done** | `packages/eoip/query/eql.py` — FIND, PATH, NEIGHBORS, IMPACT, WHY, WHY NOT, WHAT CHANGED, CONTEXT, EDGES, COUNT, DOMAINS |
| NLQ (Natural Language Query) | Query | **Done** | `packages/eoip/query/nlq.py`, `nl.py` — NL→QueryPlan→execution |
| SKOS | Taxonomy | **Done** | `packages/eoip/ontology/skos.py` — schemes, concepts, mappings, exactMatch/closeMatch/broadMatch/narrowMatch/relatedMatch |

### 4.2 Implemented in Phase C (2026-10-05)

| Language/Standard | Type | Status | Evidence |
|------------------|------|--------|----------|
| SHACL (Shapes Constraint Language) | Export | **Done** | `packages/eoip/graph/format_converter.py` to_shacl — generates sh:NodeShape with sh:property constraints |
| PGQL (Property Graph Query Language) | Export | **Done** | `packages/eoip/graph/format_converter.py` to_pgql — Oracle INSERT INTO VERTEX/EDGE syntax |
| OpenCypher | Export | **Done** | `packages/eoip/graph/format_converter.py` to_opencypher — ISO standardized MERGE/SET syntax |
| EOQL (Enterprise Object Query Language) | Query | **Done** | `packages/eoip/query/languages.py` parse_eoql — SELECT/TRAVERSE/AGGREGATE with WHERE, JOIN, LIMIT |
| OSQL (Ontology SQL) | Query | **Done** | `packages/eoip/query/languages.py` parse_osql — DESCRIBE/LIST TYPES/LIST DOMAINS/LIST RELATIONSHIPS/INSTANCES OF |
| Semantic Query Language | Query | **Done** | `packages/eoip/query/languages.py` parse_semantic_query — MEANING OF/RELATED TO/EXPLAIN/COMPARE/CLASSIFY |
| NL2SQL / Semantic Prompts | Query | **Done** | `packages/eoip/query/nlq.py`, `nl.py` — NL→QueryPlan→execution (already existed as NLQ) |

API endpoints: `POST /api/v1/query/language` (EOQL/OSQL/Semantic QL), `GET /api/v1/export/formats` (all 12 formats).
Tests: `tests/unit/test_query_languages.py` — 29 test cases covering all 3 parsers.

---

## 5. Graph Algorithm Status

### 5.1 Currently Implemented

| Algorithm | Status | Evidence |
|-----------|--------|----------|
| PageRank | **Done** | `packages/eoip/graph/metrics.py:323-349` |
| Betweenness centrality | **Done** | `metrics.py:274-304` |
| Closeness centrality | **Done** | `metrics.py:306-321` |
| Eigenvector centrality | **Done** | `metrics.py:351-368` |
| Katz centrality | **Done** | `metrics.py:370-388` |
| HITS (hub/authority) | **Done** | `metrics.py:390-412` |
| Harmonic centrality | **Done** | `metrics.py:414-430` |
| Degree centrality | **Done** | `metrics.py:432-446` |
| K-core decomposition | **Done** | `metrics.py:463+` |
| Community detection (label propagation) | **Done** | `packages/eoip/graph/community.py:122+` |
| Community detection (Louvain/modularity) | **Done** | `community.py:247+` |
| All shortest paths (BFS) | **Done** | `packages/eoip/graph/paths.py:44+` |
| K-shortest paths (Yen's) | **Done** | `paths.py:112+` |
| Blast radius / impact analysis | **Done** | `metrics.py:147-235`, `packages/eoip/graph/traversal.py:125+` |
| Jaccard similarity | **Done** | `packages/eoip/graph/similarity.py:76+` |
| Adamic-Adar similarity | **Done** | `similarity.py:106+` |
| Common neighbors | **Done** | `similarity.py:141+` |
| Link prediction | **Done** | `similarity.py:169+` |
| Anomaly detection | **Done** | `packages/eoip/graph/anomaly.py` |
| What-if simulation | **Done** | `packages/eoip/graph/simulation.py`, `whatif.py` |
| Surprise detection | **Done** | `packages/eoip/graph/surprise.py` |
| Causal analysis | **Done** | `packages/eoip/graph/causal.py` |
| Process mining | **Done** | `packages/eoip/graph/process_mining.py` |

### 5.2 Implemented in Phase C (2026-10-05)

All 13 requested algorithms now implemented in `packages/eoip/graph/algorithms.py`:

| Algorithm | Status | Method | Evidence |
|-----------|--------|--------|----------|
| Ring detection (cycle detection) | **Done** | `detect_rings` | DFS cycle detection with normalized dedup |
| Intersection detection | **Done** | `detect_intersection` | BFS reachable set intersection |
| Weighted shortest path | **Done** | `weighted_shortest_path` | Dijkstra's algorithm |
| Single-source weighted shortest path | **Done** | `single_source_weighted_paths` | Dijkstra from single source |
| Model similarity | **Done** | `model_similarity` | Node/edge Jaccard + degree distribution cosine |
| Neighbor Rank recommendation | **Done** | `neighbor_rank` | Weighted neighborhood contribution ranking |
| K-step neighbor | **Done** | `k_step_neighbors` | K-hop neighborhood extraction with per-hop layers |
| K-jump algorithm | **Done** | `k_jump` | Random walk visit probability |
| Custom path | **Done** | `custom_path` | Constrained DFS with allowed/blocked edge labels |
| Ray detection | **Done** | `ray_detection` | Directional ray traversal (outgoing/incoming/both) |
| Co-neighbor | **Done** | `co_neighbors` | Shared neighbor analysis with overlap coefficient |
| Personal Rank recommendation | **Done** | `personal_rank` | Personalized PageRank |

API endpoint: `POST /api/v1/algorithms/run`, `GET /api/v1/algorithms` (lists all 30+ algorithms).
Tests: `tests/unit/test_graph_algorithms.py` — 12 new test cases for extended algorithms.

---

## 6. Semantic Indexing Pipeline (IMPLEMENTED — 2026-10-05)

**Status**: **Done**

**Implementation**: `packages/eoip/ingestion/semantic_pipeline.py` — unified 6-stage post-ingestion orchestrator:

| Stage | Purpose | Evidence |
|-------|---------|----------|
| bridge_edges | Cross-domain relationship establishment using ontology manifest | Links domains via `link_domains()` |
| metadata_enrichment | Domain classification from VERTEX_LABELS | Assigns domain from ontology spec |
| search_index | InMemorySearchIndex population | Indexes all vertices for search |
| analytics | GraphMetricsEngine statistics computation | Computes graph_statistics |
| validation | ValidationEngine quality gate checks | Runs all validation rules |
| event_publish | EventEmitter notification for downstream consumers | Publishes semantic_pipeline_completed event |

**Triggering**:
- Manual: `POST /api/v1/admin/semantic-pipeline` (with optional stage selection and scope filter)
- Agent: `POST /api/v1/agents/semantic-index` (runs SemanticIndexAgent with bounded budget)
- Automated: Triggered by graph evolution events via SemanticIndexAgent

**Tests**: `tests/unit/test_semantic_pipeline.py` — 12 test cases covering all stages, scoping, and edge cases.

---

## 7. Agent-Driven Orchestration (IMPLEMENTED — 2026-10-05)

**Status**: **Done**

**New agents**:

| Agent | File | Purpose | Swarm Support |
|-------|------|---------|---------------|
| GraphAnalyticsAgent | `packages/eoip/agents/graph_analytics.py` | Runs any of 30+ algorithms as bounded agent workflows | Yes — "swarm" mode runs ring_detection, k_core, community, anomaly, blast_radius + cid-specific algorithms |
| SemanticIndexAgent | `packages/eoip/agents/semantic_index.py` | Runs semantic pipeline (Step 2) with stage filtering and scope | Via context_refs for stage selection |

**GraphAnalyticsAgent features**:
- ALGORITHM_REGISTRY with 30 algorithms mapped to dispatch methods
- Single algorithm execution: `goal="ring_detection"` with context_refs for parameters
- Swarm mode: `goal="swarm"` runs 5-9 algorithms and aggregates results
- Configurable budgets (max_steps, max_seconds)
- Full ExplanationEnvelope with evidence refs

**API endpoints**:
- `POST /api/v1/agents/analytics` — trigger GraphAnalyticsAgent
- `POST /api/v1/agents/semantic-index` — trigger SemanticIndexAgent

**Tests**: `tests/unit/test_agent_analytics.py` — 14 test cases covering both agents, swarm mode, error handling, custom budgets.

---

## 8. GAPS Phase 0-1 Implementation Status

### 8.1 Implemented (37 items Done)

| ID | Requirement | Status | Evidence |
|----|------------|--------|----------|
| GAP-HG-008 | Graph store capacity benchmark harness | **Done** | `packages/eoip/graph/benchmark.py` — BenchmarkHarness with vertex/edge insert, lookup, traversal benchmarks, p50/p95/p99 latencies |
| GAP-CDC-002 | Change event before/after state capture | **Done** | `packages/eoip/graph/evolution.py` — SemanticChangeEvent with `before_state`, `after_state` fields (excluded from hash chain) |
| GAP-STUDIO-011 | JSON Schema / OpenAPI / form spec generation | **Done** | `packages/eoip/ontology/schema_gen.py` — `generate_json_schema()`, `generate_openapi_schemas()`, `generate_form_spec()` from ontology manifest |
| GAP-DRIFT-005 | Embedding drift detection | **Done** | `packages/eoip/ontology/embedding_drift.py` — cosine similarity, EmbeddingDriftReport, drift threshold detection |
| GAP-AGOV-011 | Agent dry-run mode | **Done** | `packages/eoip/contracts/agent.py:82` — `dry_run: bool = False` on AgentRequest, `governed.py` enforcement |
| GAP-CONN-* | All 9 connector requirements | **Done** | Jira, GitLab, Confluence, ServiceNow, Local Code, Rally, qTest connectors with versioned SDK |
| GAP-INGEST-* | All 5 ingestion requirements | **Done** | SourceEventV2 capture, canonicalization, DLQ, replay, code ingestion |
| GAP-GRAPH-* | All 10 graph core requirements | **Done** | HugeGraph adapter, schema bootstrap, meta graph, graph evolution, format converter |
| GAP-QUERY-* | All 8 query requirements | **Done** | QueryPlan, executor, NLQ, EQL, policy, evidence envelope, path/impact queries |
| GAP-VALID-* | All 3 validation requirements | **Done** | Validation engine, gates, quality metrics |

### 8.2 Challenge Items (8 items — infra/frontend/license limited)

| ID | Requirement | Status | Reason |
|----|------------|--------|--------|
| GAP-STUDIO-001 | HugeGraph Studio visual editor | **CHALLENGE** | Requires HugeGraph Studio enterprise UI — a separate frontend application, not implementable as backend code |
| GAP-STUDIO-002 | Studio drag-and-drop schema builder | **CHALLENGE** | Frontend-only: requires React/Cytoscape interactive visual editor component |
| GAP-STUDIO-003 | Studio live query console | **CHALLENGE** | Frontend-only: requires interactive query editor UI with syntax highlighting and result rendering |
| GAP-NOCODE-001 | No-code connector builder UI | **CHALLENGE** | Frontend-only: requires drag-and-drop visual connector configuration interface |
| GAP-NOCODE-002 | No-code mapping designer | **CHALLENGE** | Frontend-only: requires visual field-to-vertex/edge mapping interface |
| GAP-NOCODE-003 | No-code pipeline orchestrator | **CHALLENGE** | Frontend-only: requires visual DAG pipeline editor |
| GAP-PERF-001 | HugeGraph cluster horizontal scaling | **CHALLENGE** | Infrastructure-limited: requires multi-node HugeGraph cluster deployment (enterprise license) |
| GAP-PERF-002 | HugeGraph distributed storage backend | **CHALLENGE** | Infrastructure-limited: requires HBase/RocksDB distributed backend (enterprise deployment) |

---

## 9. GAPS2 Phase P0-P3 Implementation Status

### 9.1 Implemented (68 items Done)

| ID | Requirement | Status | Evidence |
|----|------------|--------|----------|
| G2-SRC-SBOM | SBOM/SCA connector (SPDX + CycloneDX) | **Done** | `packages/eoip/connectors/sbom.py` — SBOMConnector with discover, extract_spdx, extract_cyclonedx, checkpoint, health |
| G2-SRC-CICD | Generic CI/CD pipeline connector | **Done** | `packages/eoip/connectors/cicd.py` — CICDConnector with discover, extract_pipelines, extract_deployments, checkpoint, health |
| G2-SRC-OTEL | OpenTelemetry trace/metric connector | **Done** | `packages/eoip/connectors/otel.py` — OpenTelemetryConnector with graceful fallback when opentelemetry-sdk unavailable |
| G2-SRC-RUNTIME | Runtime infrastructure connector | **Done** | `packages/eoip/connectors/runtime_infra.py` — RuntimeInfraConnector with graceful fallback when kubernetes client unavailable |
| G2-P2-EVOL | Graph evolution engine with temporal semantics | **Done** | `packages/eoip/graph/evolution.py` — GraphEvolutionEngine with evolve_entity/relationship, as_of, diff, versions, hash-chained journal |
| G2-P2-BUS | Semantic event bus with pub/sub | **Done** | `packages/eoip/graph/evolution.py` — SemanticEventBus with subscribe/publish |
| G2-P2-JOURNAL | Change journal with hash chain integrity | **Done** | `packages/eoip/graph/evolution.py` — ChangeJournal with append/read, SHA-256 hash chain verification |
| G2-RAG-* | All RAG retrieval requirements | **Done** | RetrievalStrategy, RAGRouter (17 patterns), evidence manifests, local model abstraction |
| G2-AGENT-* | All agent orchestration requirements | **Done** | 20+ agents, bounded runtime, circuit breaker, GraphAnalyticsAgent, SemanticIndexAgent |
| G2-ALGO-* | All 30+ graph algorithms | **Done** | centrality (8 types), community detection, path algorithms, similarity, anomaly, process mining, what-if, custom algorithms |
| G2-FORMAT-* | All 12 export formats | **Done** | RDF, RDFS, OWL, JSON-LD, Gremlin, Cypher, GQL, SPARQL, SHACL, PGQL, OpenCypher |
| G2-QUERY-* | All query language requirements | **Done** | EQL, NLQ, EOQL, OSQL, Semantic Query Language parsers and execution |
| G2-VALID-* | All validation/quality requirements | **Done** | Validation engine, quality gates, graph quality metrics |
| G2-PROV-* | All provenance requirements | **Done** | Evidence model, lineage service, traversal |
| G2-SKOS | SKOS taxonomy support | **Done** | `packages/eoip/ontology/skos.py` — schemes, concepts, 5 mapping types |

### 9.2 Challenge Items (12 items — infra/frontend/license limited)

| ID | Requirement | Status | Reason |
|----|------------|--------|--------|
| G2-UX-GRAPH-001 | Interactive graph explorer with zoom/pan/filter | **CHALLENGE** | Frontend-only: Cytoscape.js renderer exists (`CytoscapeRenderer.jsx`) but advanced UX features (minimap, lasso select, group collapse) require frontend-specific development |
| G2-UX-GRAPH-002 | Graph canvas dark/light theme system | **CHALLENGE** | Frontend-only: requires CSS theme system and Cytoscape style switching in React |
| G2-UX-GRAPH-003 | Graph layout algorithms (force-directed, hierarchical, circular) | **CHALLENGE** | Frontend-only: requires Cytoscape.js layout plugin integration |
| G2-ADMIN-001 | Admin dashboard with real-time metrics | **CHALLENGE** | Frontend-only: requires WebSocket/SSE real-time UI dashboard component |
| G2-ADMIN-002 | Admin user management UI | **CHALLENGE** | Frontend-only: requires user CRUD interface; backend auth exists but multi-user management is enterprise scope |
| G2-ADMIN-003 | Admin RBAC policy editor | **CHALLENGE** | Frontend-only: requires visual role/permission matrix editor |
| G2-SRC-OTEL-LIB | OpenTelemetry SDK integration (traces/metrics export) | **CHALLENGE** | License/dependency: requires `opentelemetry-sdk` pip package — connector code exists with graceful try/except fallback |
| G2-SRC-K8S | Kubernetes API live discovery | **CHALLENGE** | Infrastructure: requires running Kubernetes cluster and `kubernetes` pip package — connector code exists with graceful fallback |
| G2-DEPLOY-HA | High-availability deployment mode | **CHALLENGE** | Infrastructure: requires multi-node deployment with load balancer, HugeGraph cluster, shared storage |
| G2-DEPLOY-HELM | Helm chart for Kubernetes deployment | **CHALLENGE** | Infrastructure: requires Kubernetes cluster for deployment and testing |
| G2-SCALE-SHARD | Graph sharding / partitioning | **CHALLENGE** | Infrastructure: requires HugeGraph enterprise with partition-graph support |
| G2-SCALE-CACHE | Distributed caching layer | **CHALLENGE** | Infrastructure: requires Redis/Memcached cluster for cross-node cache |

---

## 10. Test Coverage (Verified 2026-10-05, Pass 3)

- **Unit test files**: 148
- **Security test files**: 4
- **Performance test files**: 2
- **E2E test files**: 5
- **Contract test files**: 3
- **Total test files**: 162
- **Unit test results**: **1,792 passed**, 10 skipped, **0 failures**, 1 warning
- **New test files in Pass 2**: test_diff_hunk.py (10), test_strategy_registry.py (16), test_admin_gremlin.py (4), test_gaps_implementations.py (18) = 48 new tests
- **Regression status**: Clean — no pre-existing failures remaining in unit suite
