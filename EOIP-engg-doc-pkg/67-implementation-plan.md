# Master Implementation Plan

**Project:** Enterprise Ontology & Intelligence Platform (EOIP)  
**Baseline:** 0.1.0-architecture-baseline  
**Date:** 2026-10-01  
**Status:** Architecture baseline / engineering handoff  
**Purpose:** Phased work packages mapped to all requirements

> This document is normative for its scope. Where it conflicts with the master specification, the master non-negotiable constraints win. “MVP” means the Phase 1 integrated vertical slice, not a mock-up.

## Architecture decisions

1. **One physical HugeGraph graph in the MVP; multiple logical graph domains.** Jira, code, documentation, CI/CD, provenance, meta, identity and agent/action domains are separated by explicit labels/properties and meta-graph records. This preserves direct cross-domain Gremlin traversal and avoids an artificial cross-database join layer. Physical graph-space separation is a later scaling/isolation option, not an MVP assumption.
2. **HugeGraph is the only mandatory database.** Local files/volumes are used for immutable raw capture, DLQ, checkpoints, configuration, model artifacts and exports; they are not an alternative source-of-truth graph database.
3. **RocksDB standalone mode for the MVP.** It is appropriate for a single-node development/demo vertical slice. HStore/distributed topology is a Phase 7 decision based on measured capacity, HA and scale requirements.
4. **Modular monolith first.** A single Python codebase exposes API, worker and MCP entry points while maintaining strict package boundaries. Separate processes/containers may use the same image. Microservice extraction requires an independently deployable/scalable/security boundary and evidence that the split reduces risk/cost.
5. **No mandatory vector database in Phase 1.** Graph traversal, indexed identifiers, linked document sections and local lexical retrieval prove the platform. A local embedding provider is pluggable; a dedicated vector index becomes optional only after retrieval benchmarks show value.
6. **Deterministic parsing/linking before LLM inference.** Tree-sitter/AST, Git metadata, issue keys, commit SHAs, paths and configured identifiers are primary. Inferred relationships are explicitly marked, scored and evidence-backed.
7. **Safe query compilation.** Natural language produces a typed `QueryPlan`; it never produces directly executable unrestricted Gremlin. The query policy enforces depth/result/timeout/relationship bounds and read-only behavior.
8. **Read-only AI/MCP MVP.** The MVP agent and MCP surface only read/search/analyze. Source-system/code mutations are deferred until human-control and write-tool governance are implemented.
9. **Local model is optional to core graph utility.** The demo can show a local model, but search, path, impact, provenance and graph visualization continue to work when the model is stopped.
10. **No RBAC does not mean no security.** Phase 1 has environment/profile-aware authentication, network isolation, secret handling, audit, input/query/action policy and safe defaults. `/app` vs `/admin` is navigation, never an authorization boundary.


```text
eoip/
├─ apps/
│  ├─ api/                 # FastAPI composition root
│  ├─ worker/              # ingestion/parse job entry point
│  ├─ mcp/                 # MCP façade
│  ├─ web/                 # React/TypeScript SPA
│  └─ vscode-extension/    # VS Code extension
├─ packages/
│  ├─ contracts/           # Pydantic/versioned JSON contracts
│  ├─ connectors/          # SDK + jira/git/gitlab/file adapters
│  ├─ ingestion/           # capture/canonicalize/checkpoint/DLQ
│  ├─ ontology/            # ontology vocabulary + schema manifest
│  ├─ graph/               # HugeGraph client/schema/mutations
│  ├─ codegraph/           # parser plugins + symbol graph
│  ├─ identity/            # resolution policies
│  ├─ provenance/          # evidence/lineage
│  ├─ validation/          # rule engine + quality metrics
│  ├─ query/               # QueryPlan, policy, Gremlin templates
│  ├─ retrieval/           # RAG router/context builder
│  ├─ models/              # local model abstraction
│  ├─ agents/              # registry/runtime/TraceImpact agent
│  ├─ audit/               # audit event sink/redaction
│  └─ observability/       # logs/metrics/tracing helpers
├─ config/
│  ├─ ontology/
│  ├─ mappings/
│  ├─ query-policies/
│  └─ agents/
├─ deploy/
│  ├─ docker-compose.yml
│  ├─ docker-compose.observability.yml
│  └─ secrets.example/
├─ examples/
│  ├─ jira/
│  ├─ gitlab/
│  └─ demo-repo/
├─ tests/
│  ├─ unit/ contract/ integration/ e2e/ security/ performance/
├─ scripts/
│  ├─ bootstrap_schema.py
│  ├─ backup.py
│  ├─ restore.py
│  └─ demo_reset.py
└─ docs/
```
## Work packages

### WP-FOUNDATION
**Target phase(s):** P1-MVP  
**Requirements:** FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-004, NFR-MAINT-001  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-001 | HugeGraph authoritative store | P1-MVP | All demo graph paths survive service restart. |
| FR-GRAPH-002 | Logical graph domains | P1-MVP | Every business vertex/edge belongs to a valid domain. |
| FR-GRAPH-003 | Schema bootstrap | P1-MVP | Fresh stack auto-initializes and second run is no-op. |
| FR-GRAPH-004 | Canonical identifiers | P1-MVP | Every canonical entity has unique stable canonical_id. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |

### WP-CONNECTORS
**Target phase(s):** P1-MVP, P2  
**Requirements:** FR-CONN-001, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-CONN-006, FR-CONN-007, FR-CONF-001, FR-SNOW-001  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CONN-001 | Connector SDK | P1-MVP | A new connector can be added without editing ingestion core. |
| FR-CONN-002 | Jira JSON connector | P1-MVP | Repeat import is idempotent and creates expected graph. |
| FR-CONN-003 | Git repository connector | P1-MVP | Repository, branch and commit nodes plus modifications exist. |
| FR-CONN-004 | GitLab metadata adapter | P1-MVP | MR and pipeline records link to commits and work items. |
| FR-CONN-005 | Connector resiliency | P1-MVP | Restart resumes without duplicate canonical nodes. |
| FR-CONN-006 | Dry run and replay | P1-MVP | Same input/version produces same canonical mutations. |
| FR-CONN-007 | Source deletion semantics | P1-MVP | Deleted source is queryable historically and excluded from current views. |
| FR-CONF-001 | Confluence connector | P2 | Incremental sync and provenance pass. |
| FR-SNOW-001 | ServiceNow connector | P2 | Incremental sync and mappings pass. |

### WP-INGESTION
**Target phase(s):** P1-MVP  
**Requirements:** FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-INGEST-001 | Raw capture | P1-MVP | Every graph mutation references a captured event. |
| FR-INGEST-002 | Canonicalization | P1-MVP | Same source record maps deterministically for same mapper version. |
| FR-INGEST-003 | Idempotent mutation | P1-MVP | Second identical run does not increase logical entity/edge counts. |
| FR-INGEST-004 | Ingestion job lifecycle | P1-MVP | Admin UI reflects actual backend run state. |
| FR-INGEST-005 | Dead-letter processing | P1-MVP | Rejected records are inspectable and replayable. |

### WP-ONTOLOGY-GRAPH
**Target phase(s):** P1-MVP, P2  
**Requirements:** FR-GRAPH-005, FR-GRAPH-006, FR-GRAPH-008, FR-GRAPH-009, FR-GRAPH-010, FR-ONTO-001, FR-ONTO-002, FR-PROV-001, FR-PROV-002, FR-ID-001, FR-ID-002, FR-TEMP-001  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-GRAPH-005 | Meta graph | P1-MVP | Admin statistics are derived from graph/meta records. |
| FR-GRAPH-006 | Cross-domain bridge edges | P1-MVP | Jira→MR→Commit→File→Function→Dependency→Pipeline→Doc path is traversable. |
| FR-GRAPH-008 | Index strategy | P1-MVP | Benchmark-critical lookup paths use planned indexes. |
| FR-GRAPH-009 | Graph version journal | P1-MVP | Each changed fact can be attributed to a run/version. |
| FR-GRAPH-010 | RDF/OWL interoperability | P2 | No documentation claims native SPARQL support. |
| FR-ONTO-001 | Enterprise ontology vocabulary | P1-MVP | MVP entities/edges reference ontology version and valid terms. |
| FR-ONTO-002 | Relationship semantics | P1-MVP | No MVP business relationship relies on untyped generic edge. |
| FR-PROV-001 | Evidence model | P1-MVP | MVP evidence coverage is 100% for cross-domain bridge edges. |
| FR-PROV-002 | Provenance traversal | P1-MVP | User can trace demo answer to source fixture/commit metadata. |
| FR-ID-001 | Deterministic identity resolution | P1-MVP | Exact aliases merge predictably and retain source aliases. |
| FR-ID-002 | Ambiguous identity candidates | P1-MVP | No fuzzy-only match produces same canonical_id automatically. |
| FR-TEMP-001 | Bitemporal-ready fields | P1-MVP | MVP schema is ready for P5 without ID rewrite. |

### WP-CODEGRAPH
**Target phase(s):** P1-MVP  
**Requirements:** FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-CODE-001 | Deterministic code parser | P1-MVP | Supported files yield stable symbol graph and exact source ranges. |
| FR-CODE-002 | Python and TypeScript MVP parsing | P1-MVP | Demo repo symbols and imports/calls are queryable. |
| FR-CODE-003 | Commit-to-symbol linking | P1-MVP | Demo commit connects to relevant function(s). |
| FR-CODE-004 | Call/import/dependency edges | P1-MVP | Blast radius traverses only validated edge classes. |
| FR-CODE-005 | Source navigation | P1-MVP | Extension opens demo symbol at correct range. |

### WP-QUERY
**Target phase(s):** P1-MVP  
**Requirements:** FR-QUERY-001, FR-QUERY-002, FR-QUERY-003, FR-QUERY-004, FR-QUERY-005, FR-QUERY-006, FR-QUERY-007, FR-QUERY-008, FR-GRAPH-007  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-QUERY-001 | Structured QueryPlan | P1-MVP | All NL and structured requests compile to validated QueryPlan. |
| FR-QUERY-002 | Path query | P1-MVP | Demo Jira-to-function path returns expected ordered edges. |
| FR-QUERY-003 | Impact analysis | P1-MVP | Demo function change returns expected dependents with paths. |
| FR-QUERY-004 | Entity search | P1-MVP | Demo Jira issue, commit and symbol are discoverable. |
| FR-QUERY-005 | Natural-language query interpretation | P1-MVP | Prompt injection cannot bypass QueryPlan policy. |
| FR-QUERY-006 | Query safety policy | P1-MVP | All exposed query endpoints pass policy conformance suite. |
| FR-QUERY-007 | Query evidence envelope | P1-MVP | GraphRAG/UI/MCP consume same evidence format. |
| FR-QUERY-008 | Raw Gremlin admin boundary | P1-MVP | No public OpenAPI/MCP tool accepts free-form Gremlin in MVP. |
| FR-GRAPH-007 | Gremlin repository | P1-MVP | No UI/agent endpoint can execute arbitrary mutation Gremlin. |

### WP-VALIDATION
**Target phase(s):** P1-MVP  
**Requirements:** FR-VALID-001, FR-VALID-002, FR-VALID-003  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-VALID-001 | Graph validation rules | P1-MVP | Admin UI shows real findings from demo data. |
| FR-VALID-002 | Validation gates | P1-MVP | Invalid endpoint edge cannot silently enter graph. |
| FR-VALID-003 | Graph quality metrics | P1-MVP | Dashboard values reconcile with fixture counts. |

### WP-RAG
**Target phase(s):** P1-MVP, P3  
**Requirements:** FR-RAG-001, FR-RAG-002, FR-RAG-003, FR-RAG-004, FR-RAG-005, FR-RAG-006  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-RAG-001 | Retrieval router | P1-MVP | Known MVP questions route without external service. |
| FR-RAG-002 | GraphRAG evidence retrieval | P1-MVP | Demo GraphRAG answer cites graph/source references. |
| FR-RAG-003 | Local model abstraction | P1-MVP | Core search/path/impact remains usable with model service stopped. |
| FR-RAG-004 | No mandatory vector DB in MVP | P1-MVP | MVP starts and demos without vector database. |
| FR-RAG-005 | RAG evaluation harness | P1-MVP | Baseline report is reproducible locally. |
| FR-RAG-006 | Adaptive RAG strategy framework | P3 | P3 can add strategy plugin without changing callers. |

### WP-AGENT-MEMORY
**Target phase(s):** P1-MVP, P8+  
**Requirements:** FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-MEM-001  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-AGENT-001 | Agent contract | P1-MVP | Every enabled agent has a validated contract. |
| FR-AGENT-002 | Bounded agent runtime | P1-MVP | Agent cannot exceed configured execution envelope. |
| FR-AGENT-003 | TraceImpact agent | P1-MVP | Same demo question works via UI/API/MCP context. |
| FR-AGENT-004 | Write/action approval boundary | P1-MVP | No MVP agent can mutate source systems or code. |
| FR-AGENT-005 | Controlled self-modification | P8+ | No production self-modification path exists before P8+. |
| FR-MEM-001 | Scoped memory records | P1-MVP | No uncontrolled accumulation in MVP. |

### WP-MCP
**Target phase(s):** P1-MVP  
**Requirements:** FR-MCP-001, FR-MCP-002  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-MCP-001 | MCP read server | P1-MVP | MCP returns same graph evidence as REST for demo case. |
| FR-MCP-002 | MCP action separation | P1-MVP | MVP MCP surface is read-only. |

### WP-EXPERIENCE
**Target phase(s):** P1-MVP  
**Requirements:** FR-UI-001, FR-UI-002, FR-ADMIN-001, FR-ADMIN-002, FR-VSCODE-001, FR-VSCODE-002  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| FR-UI-001 | User web application | P1-MVP | Demo flow works from persisted data. |
| FR-UI-002 | Graph explorer | P1-MVP | Demo path is highlighted with evidence access. |
| FR-ADMIN-001 | Admin ingestion UI | P1-MVP | Run state reconciles with backend/meta graph. |
| FR-ADMIN-002 | Admin graph quality UI | P1-MVP | No dashboard KPI is hardcoded. |
| FR-VSCODE-001 | VS Code context extension | P1-MVP | Opening demo function retrieves correct graph context. |
| FR-VSCODE-002 | VS Code trace/impact commands | P1-MVP | Demo command returns Jira→code path and impact. |

### WP-SECURITY-OPS
**Target phase(s):** P1-MVP  
**Requirements:** NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-SEC-006, NFR-SEC-007, NFR-REL-001, NFR-REL-002, NFR-OPS-001, NFR-OPS-002, NFR-PERF-001, NFR-MAINT-001, NFR-PRIV-001  
**Build rule:** Implement contracts/tests first, then adapters/domain logic, then API/UI exposure. Every package must use canonical contracts and the common audit/observability layer.

| ID | Requirement | Phase | Completion signal |
|---|---|---|---|
| NFR-SEC-001 | No outbound enterprise-data egress | P1-MVP | Demo succeeds with external network disabled. |
| NFR-SEC-002 | Secret isolation | P1-MVP | Repository and logs contain no test secret plaintext. |
| NFR-SEC-003 | Input/file safety | P1-MVP | Security suite rejects malicious fixtures. |
| NFR-SEC-004 | Prompt/tool injection defenses | P1-MVP | Known injection cases remain read-only/bounded. |
| NFR-SEC-005 | Authentication without MVP RBAC | P1-MVP | /admin route presence is never claimed as authorization boundary. |
| NFR-SEC-006 | Container hardening | P1-MVP | HugeGraph/model not exposed externally by default. |
| NFR-SEC-007 | Audit events | P1-MVP | Sensitive operation has traceable audit ID. |
| NFR-REL-001 | Restart-safe processing | P1-MVP | No duplicates or silent skipped records after restart. |
| NFR-REL-002 | Backup and restore | P1-MVP | Restored demo reproduces expected counts/path queries. |
| NFR-OPS-001 | Structured logging and health | P1-MVP | Failure can be followed by correlation ID. |
| NFR-OPS-002 | Local metrics | P1-MVP | Key MVP metrics are machine-readable. |
| NFR-PERF-001 | Benchmark-defined objectives | P1-MVP | Published numbers identify dataset/hardware/version. |
| NFR-MAINT-001 | Modular monolith boundary | P1-MVP | Core can later split without changing external contracts. |
| NFR-PRIV-001 | Data minimization and classification | P1-MVP | Audit/log exports contain no prohibited content. |


## Sequencing rules

1. Schema/contracts/security profile precede all connectors.
2. Raw capture/canonicalization precede graph mutation.
3. Jira and code subgraphs must pass validation independently before cross-domain linking.
4. QueryPlan/policy precede NL/RAG/agent/MCP exposure.
5. Evidence retrieval precedes answer generation.
6. Web, VS Code and MCP reuse the same application services rather than reimplementing graph logic.
7. Backup/restore is completed before MVP release, not as a post-demo operation.
8. Advanced phases may add components only behind existing versioned ports or by an explicit ADR/migration plan.

## Requirement implementation template

Every engineering ticket derived from this plan must contain: objective; mapped requirement IDs; dependencies; modules/files; versioned interfaces; ordered implementation steps; unit/contract/integration/security tests; acceptance evidence; expected artifacts; rollback/failure handling; observability; and documentation impact.
