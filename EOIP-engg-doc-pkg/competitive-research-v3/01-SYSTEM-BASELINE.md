# 01 — System Baseline (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 01-SYSTEM-BASELINE.md, part of the Master Prompt v3.0 deliverable package |
| Baseline date (UTC) | 2026-10-18 |
| Repository state | `F:\code\EIP\EIOP`, branch `dev_local`, HEAD `ad9937b`, working tree clean at the start of the run |
| Method | Static reading of code (`packages/eoip`, `apps/*`, `config/*`, `deploy/*`, `schemas/*`), the locked dependency set (`requirements.lock`), and a fresh local `pytest` run (see §2). Requirements Markdown is **never** used as proof of implementation. |
| Product name | KnowGridFlow / EOIP. The candidate rebrand "Semaplexvell" is **not used** in any artifact of this package until its spelling is confirmed (assumption A-01 in `22-OPEN-QUESTIONS-AND-ASSUMPTIONS.md`). |

## 1. Status vocabulary used in this package

| Status | Meaning in this package |
|---|---|
| **Implemented** | Production code exists on the runtime path, does real work (not a stub or a canned response), and is exercised by tests that passed in this run. It does **not** mean "verified against a live external backend" unless that is stated. |
| **Partial** | Code exists but covers only a subset of the capability, runs only against the in-memory store, is a contract or registry without enforcement, or depends on something not installed. The gap is named. |
| **Planned** | Specified in requirements or implementation plans; no runtime code found. |
| **Absent** | Neither code nor a plan was found. |
| **Unknown** | Could not be decided from the code inspected in this run. |

"Live-unverified" is added when the code talks to an external engine (HugeGraph, Neo4j, Neptune, Ollama…) and no live engine was running during this run.

## 2. Evidence produced in this run

| Evidence | Result |
|---|---|
| Python package size | 609 `.py` files under `packages/eoip` (107 sub-packages); 336 test files under `tests/` |
| API surface | FastAPI apps `apps/api/app.py` (1,702 lines), `apps/api/main.py` (1,716), `apps/api/extended.py` (1,519); MCP server `apps/mcp/main.py` (228 lines, 18 tools); worker `apps/worker/main.py` |
| Locked runtime dependencies | `requirements.lock` (43 lines): `fastapi 0.142.2`, `pydantic 2.13.5`, `httpx 0.28.1`, `mcp 1.30.0`, `pyyaml`… **No** `numpy`, `scipy`, `torch`, `rdflib`, `pyshacl`, `networkx` or vector-database client in the lock. |
| pytest, first attempt | Collection stopped: `tests/fuzz/test_property_fuzz.py` needs `hypothesis` (not installed). |
| pytest, second attempt | Collection stopped: 4 modules under `tests/neural/` need `numpy` (not installed) — `packages/eoip/neural/antistub.py:18` imports `numpy` at module import time, so `eoip.neural` cannot be imported in the locked environment. |
| pytest, third attempt (excluding `tests/fuzz`, `tests/neural`, `tests/runtime_hubble`, `tests/runtime_dlq`) | See §2.1. |
| Live backends | **Not running in this run.** No HugeGraph, Neo4j, Neptune, Fuseki, GraphDB, JanusGraph or Ollama endpoint was contacted. Every backend claim below is static-code evidence only. |

### 2.1 Test run result

Run on 2026-10-18 with `pytest tests -v --ignore=tests/runtime_hubble --ignore=tests/runtime_dlq --ignore=tests/fuzz --ignore=tests/neural` (3,929 tests collected):

| Observation | Detail |
|---|---|
| Completed before the hang | **696 passed, 2 failed** across the first 81 test files (≈18% of collected tests) |
| Failure 1 | `tests/semantic/test_shacl_differential.py::test_pyshacl_adapter_and_differential_oracle` — `ModuleNotFoundError: No module named 'pyshacl'`. The optional pySHACL adapter exists in code (`ontology/shacl_validator.py:788`) but pySHACL is not in the locked environment. |
| Failure 2 | One test in `tests/unit/test_authn.py` failed in the full run but **passed** when re-run in isolation — flaky (likely order- or time-dependent). Not investigated further. |
| Hang | `tests/unit/test_brain_and_living_system.py::test_brain_os_kernel` (7th test in that file) never returns; reproduced in isolation (killed after 240 s). The full suite therefore cannot complete in this environment. |
| Previous claim | `available-status.md` (2026-10-11) reports "2843 passed, 34 skipped, 0 failures". That result is **not reproduced** here: the current suite is larger (3,929 collected), needs `numpy`, `hypothesis` and `pyshacl` that are not installed, and hangs. |

Consequence for status labels: "Implemented" in §5 means code present and on the runtime path, with tests that either passed in this run or were not reached because of the hang. Rows whose tests sit after the hang carry the qualifier *tests not reached*.

## 3. Verified architecture (as found in code)

```
 Source systems (Jira, Confluence, GitLab, GitHub, ServiceNow, Datadog, Grafana, Kibana, OTel, CI/CD, SBOM, K8s, files, web, JSON)
        │  connectors/*.py  — emit SourceEvent v2 (contracts/source_event.py), never write the graph
        ▼
 Raw capture + SourceEvent log  ──► replay (ingestion/replay.py), DLQ (ingestion/dlq.py), webhook receipts (connectors/webhook.py)
        │
        ▼
 Normalisation / profiling (ingest/profile.py, ingestion/json_processor.py, mapping/cml.py → mapping/ir.py)
        │
        ▼
 Identity (identity/resolver.py — deterministic person identity; identity/candidates.py — review queue)
        │
        ▼
 Validation gate (validation/gate.py check_vertex/check_edge) ──► IngestionGraphStore (ingestion/pipeline.py:153)
        │
        ▼
 GraphStore protocol (graph/store.py:56) ── registry/factory (graph/backends.py:82, config/graph-store.yaml)
   ├─ HugeGraphStore  (graph/hugegraph.py:28, REST + /gremlin)          primary in config
   ├─ Neo4jGraphStore (graph/neo4j.py:31, HTTP /db/{db}/tx/commit Cypher)
   ├─ NeptuneGraphStore (graph/neptune.py:50, /openCypher, /gremlin, /sparql paths)
   ├─ JanusGraphStore (adapters/janusgraph.py:32, Gremlin Server HTTP)
   ├─ FusekiGraphStore / GraphDBGraphStore (graph/rdf_backend.py:25/216, SPARQL over HTTP)
   └─ MemoryGraphStore (graph/memory.py:26)  — used directly by 24 modules
        │
        ▼
 Query: QueryPlan v1 (contracts/query_plan.py:17) → policy → named bounded templates (query/executor.py:259)
        App-level DSLs (query/eql.py, query/languages.py, qlang/*), NL suggestions (suggest/*), NLQ (query/nlq.py)
 Retrieval: graph-first evidence retrieval (retrieval/service.py), BM25 + hashing vectors (retrieval/vectors.py),
        RRF fusion (search/hybrid_engine.py:150), optional Ollama / sentence-transformers embeddings (models/embeddings.py)
 AI boundary: egress gateway (egress/gateway.py:106, default sharing level S0 = none), deterministic/probabilistic
        boundary (ai/boundary.py, PROPOSED-until-promoted), truth/claims (truth/engine.py:26)
 Surfaces: FastAPI (apps/api), MCP (apps/mcp, 18 read-oriented tools), React 19 + Cytoscape/Sigma web app (apps/web),
        VS Code extension (apps/vscode-extension)
 Deployment: deploy/docker-compose.yml — eoip-api, eoip-worker, eoip-mcp, eoip-web, hugegraph/hugegraph:1.7.0,
        neo4j:5-community, ollama/ollama:0.12.3, prom/prometheus:v3.6.0, Hubble; Helm and Argo CD folders exist
```

## 4. Baseline fields (Master Prompt §4.2) — verified values

| Field | Provisional value in the prompt | Verified value | Status | Evidence |
|---|---|---|---|---|
| Graph backend(s) | Multi-backend; HugeGraph reference; Neo4j and Neptune required | A backend-abstraction layer **exists**: `GraphStore` protocol + registry/factory. Adapters for HugeGraph, Neo4j, Neptune, JanusGraph, Fuseki, GraphDB and an in-memory store. Config `primary: hugegraph`; env override `EOIP_GRAPH_BACKEND`. Compose runs HugeGraph 1.7.0 and Neo4j 5 Community. | Implemented (adapters) / live-unverified | `graph/store.py:56`, `graph/backends.py:82`, `config/graph-store.yaml`, `deploy/docker-compose.yml:31,47` |
| Authoritative backend today | Verify | HugeGraph (config primary, ADR-001/ADR-004 in `EOIP-engg-doc-pkg/64-decisions-and-adrs.md`). 24 modules bypass the protocol and import `MemoryGraphStore` directly, so those features are in-memory only. | Partial | `grep MemoryGraphStore` → 24 files; e.g. `ontology/shacl_validator.py`, `gnn/engine.py` |
| Vector store(s) | Multiple vector DBs required | **No external vector database is integrated.** In-process BM25 index, deterministic hashing embedder, a pure-Python HNSW index, optional Ollama and sentence-transformers embedding providers. ADR-005 says "no mandatory vector database in P1". | Partial | `retrieval/vectors.py:29,87`, `graph/vector_graph.py:78`, `models/embeddings.py:44,115` |
| Data model | LPG + ontology, meta-graph, higher layers | LPG with a fixed label manifest (`ontology/manifest.py` `VERTEX_LABELS`), canonical IDs, revision vertices (`EntityRevision`, `RelationshipRevision`), named-graph config, meta-graph modules (`graph/meta.py`, `graph_graph/`). | Implemented (LPG) / Partial (meta layers) | `ontology/manifest.py`, `contracts/revision.py:10`, `graph/named_graph.py` |
| Knowledge layers | Instance → meta → ontology → living brain → wisdom | Instance graph and revision history: code. Meta-graph and "brain": code exists (`graph/meta.py`, `brain/`), largely in-memory. Wisdom graph: requirements and plan only (`EOIP-engg-doc-pkg/wisdom-graph-requirements.md`, `…-implementation-plan.md`). | Partial / Planned (wisdom) | listed files |
| Reasoning | Unknown | A small in-house `OWLReasoner` (subclass, disjointness, property chains) and an in-house SHACL-subset validator over `MemoryGraphStore`, plus an optional pySHACL adapter whose dependency is not installed. No OWL 2 profile engine, no Datalog engine; `rdflib`/`pyshacl` absent from the lock. Rule catalog and "knowledge reasoning" modules are heuristic. | Partial | `ontology/rdf.py:598`, `ontology/shacl_validator.py:77`, `reasoning/knowledge_reasoning.py` |
| Query languages | Gremlin REST; Cypher, GQL, SPARQL, SQL, GraphQL required | Backend adapters speak Gremlin (HugeGraph, JanusGraph, Neptune), Cypher (Neo4j, Neptune openCypher) and SPARQL (Fuseki, GraphDB, Neptune). The **user-facing** query path is `QueryPlan` → named bounded templates executed through the `GraphStore` protocol — not a compiler to backend languages. A regex-based "universal transpiler" (GQL/Cypher/Gremlin/SPARQL subset) exists under `moonshot/`. App DSLs: EQL, EOQL, OSQL, SemanticQL, JSONPath subset, jq-lite, Lucene subset. No GraphQL, no SQL/PGQ execution. | Partial | `query/executor.py:259`, `contracts/query_plan.py:17`, `moonshot/universal_transpiler.py:26`, `qlang/plans.py:37` |
| Natural-language query | Deterministic + non-deterministic NL, suggestions before execution | Deterministic template/semantic parser tier and a ranked suggestion engine with an optional LLM-assist hook; NLQ response contract. | Implemented (deterministic tier) / Partial (LLM tier) | `suggest/parser.py`, `suggest/engine.py:36`, `query/nlq.py:32` |
| Backend stack | Python / FastAPI | Python 3.11.9, FastAPI 0.142.2, Pydantic 2, httpx. | Implemented | `requirements.lock`, `apps/api/*.py` |
| Frontend | React; redesign planned | React 19.1.1 + Vite 7, Cytoscape 3.30, Sigma 2.4 + Graphology 0.25; admin panels; Playwright + axe tests. Treated as non-binding (redesign planned). | Implemented | `apps/web/package.json`, `apps/web/src/` |
| Deployment | Docker / Compose; local-first | Compose with API, worker, MCP, web, HugeGraph, Neo4j, Ollama, Prometheus; acceptance, DLQ, HA, observability compose files; Helm and Argo CD folders. | Implemented (files) / live-unverified | `deploy/` |
| AI | Model abstraction, local default, MCP, GraphRAG, neuro-symbolic, GNN | Local model abstraction (Ollama in compose); egress gateway whose default sharing level is S0 (none); deterministic/probabilistic boundary with PROPOSED-until-promoted; MCP server; GraphRAG retrieval service. GNN engine is a pure-Python heuristic (node2vec-style walks, TransE-style scoring) over the in-memory store; the `neural` tier needs `numpy`, which is not installed. | Partial | `models/provider.py`, `egress/policy.py:13`, `ai/boundary.py:77,113,135`, `gnn/engine.py`, `neural/antistub.py:18` |
| Ingestion | Generic JSON with automatic entity/relationship detection; connectors | Streaming schema profiler with key detection and explicit relationship discovery (FK-like fields, arrays of IDs, parent pointers, URL references, polymorphic type+id); JSON processor; 30+ connectors emitting SourceEvent v2; replay; DLQ; webhook dedupe. Automatic **ontology proposal** from JSON is specified (`schemas/ontology_induction_result.schema.json`) with a moonshot module; governance path not end-to-end. | Implemented (profiling, connectors) / Partial (ontology proposal) | `ingest/profile.py`, `ingestion/json_processor.py`, `connectors/*.py`, `ingestion/replay.py:41` |
| Tenancy and packaging | White-label, multi-tenant | Tenant context propagation, isolation-model registry (SILO/BRIDGE/POOL) with a per-layer placement contract that **explicitly does not enforce physical isolation** ("External gate"), quotas, lifecycle, metering, branding themes, terminology maps, localisation packs, offline signed licence files. **The graph adapters contain no tenant handling** (0 occurrences of `tenant` in `hugegraph.py`, `neo4j.py`, `neptune.py`, `memory.py`, `store.py`). | Partial | `tenancy/isolation.py:1-20,30`, `tenancy/context.py:36`, `branding/theme.py`, `licensing/license_file.py` |

## 5. Capability inventory with status (BL-IDs are referenced by the capability matrix)

| BL-ID | Capability | Status | Evidence | Note |
|---|---|---|---|---|
| BL-01 | Backend-neutral `GraphStore` protocol and factory | Implemented | `graph/store.py:56`, `graph/backends.py:82` | Protocol is CRUD + neighbourhood + bulk load + tombstone; no query-language pushdown in the protocol |
| BL-02 | HugeGraph adapter | Implemented / live-unverified | `graph/hugegraph.py:28` (733 lines, REST + `/gremlin`) | runtime tests under `tests/runtime_hubble` not run here |
| BL-03 | Neo4j adapter | Implemented / live-unverified | `graph/neo4j.py:31` (HTTP transactional Cypher) | |
| BL-04 | Neptune adapter | Implemented / live-unverified | `graph/neptune.py:50` (openCypher/Gremlin/SPARQL paths) | IAM SigV4 signing not verified |
| BL-05 | JanusGraph adapter | Implemented / live-unverified | `adapters/janusgraph.py:32` | |
| BL-06 | RDF store adapters (Fuseki, GraphDB) | Partial / live-unverified | `graph/rdf_backend.py:25,216` | LPG-shaped API over SPARQL; semantic loss not measured |
| BL-07 | Backend conformance suite | Partial | `graph/conformance.py` | conformance against live engines not run |
| BL-08 | Typed bounded query plan + policy | Implemented | `contracts/query_plan.py:17`, `query/executor.py:259`, `query/policy.py` | intent → template; no compiled backend query |
| BL-09 | Portable query IR compiled to Gremlin/Cypher/SPARQL | Partial | `moonshot/universal_transpiler.py:26` | regex subset; not on the production path |
| BL-10 | Application query DSLs (EQL, qlang front-ends) | Implemented | `query/eql.py`, `qlang/plans.py:37` | in-house languages; lock-in risk for users (see self-inversion cards) |
| BL-11 | NL suggestion engine (deterministic tier) | Implemented | `suggest/parser.py`, `suggest/engine.py` | |
| BL-12 | NL → query with LLM | Partial | `suggest/engine.py:36` (`LLMAssistHook`) | optional hook |
| BL-13 | Keyword (BM25-style) search | Implemented | `retrieval/vectors.py:29` | in-process, not persistent |
| BL-14 | Dense vector search | Partial | `retrieval/vectors.py:87`, `graph/vector_graph.py:78` | hashing embedder default; pure-Python HNSW; no external vector DB |
| BL-15 | Hybrid fusion (RRF) | Implemented | `search/hybrid_engine.py:150` | |
| BL-16 | Graph-first evidence retrieval / GraphRAG | Implemented (deterministic) | `retrieval/service.py` | no benchmark vs strong plain RAG found |
| BL-17 | Source permission metadata captured at ingest | Implemented | `contracts/source_event.py:42,50,74` (`PermissionMetadata`, `acl_hash`) | |
| BL-18 | Source-ACL enforcement in retrieval and answers | **Absent** in `retrieval/service.py`, `query/policy.py`, `query/executor.py` | grep for acl/permission/principal/visibility found nothing in those files | RBAC/ABAC exists for API actions (`authz/core.py`), not for per-fact source ACL filtering — P0 gap |
| BL-19 | RBAC/ABAC on API actions; HMAC tokens; OIDC/SAML | Implemented / Partial (SSO live-unverified) | `authz/core.py:92`, `authz/tokens.py`, `authn/oauth_sso.py:29` | |
| BL-20 | Tenant context and isolation contract | Partial | `tenancy/context.py:36`, `tenancy/isolation.py:30` | physical isolation "External gate"; adapters not tenant-aware |
| BL-21 | White-label branding, terminology, localisation | Implemented | `branding/theme.py`, `branding/terminology.py`, `branding/localization.py` | de-vendoring checklist marked partial in its own docstring |
| BL-22 | Offline licensing and metering | Implemented | `licensing/license_file.py`, `licensing/meter.py`, `tenancy/metering.py` | |
| BL-23 | SourceEvent capture, connectors never write the graph | Implemented | `connectors/base.py`, `connectors/jira_json.py` docstring, `ingestion/source_sync.py` | |
| BL-24 | Replay, DLQ, webhook dedupe, checkpoints | Implemented | `ingestion/replay.py:41`, `ingestion/dlq.py`, `connectors/webhook.py:18`, `schemas/source_checkpoint.schema.json` | live DLQ tests not run |
| BL-25 | Tombstones / deletes | Implemented | `graph/store.py` `tombstone_vertex`, 18 files reference tombstones | edge tombstone semantics per backend unverified |
| BL-26 | Schema profiling, key detection, relationship discovery from arbitrary JSON | Implemented | `ingest/profile.py` (1,023 lines) | |
| BL-27 | Ontology proposal from JSON with review and promotion | Partial | `schemas/ontology_induction_result.schema.json`, `moonshot/ontology_induction.py` | governance flow not end-to-end |
| BL-28 | Validation gate on the mutation path | Implemented | `validation/gate.py:28,50`, `ingestion/pipeline.py:153` | label/required-property checks; not SHACL |
| BL-29 | SHACL validation | Partial | `ontology/shacl_validator.py:77` (in-house subset), `ontology/shacl_validator.py:788` (optional pySHACL adapter), `ontology/rdf.py` `validate_shacl` | in-house subset over the in-memory store; pySHACL adapter present but pySHACL not installed, so its differential test fails; W3C SHACL Core conformance not tested |
| BL-30 | OWL reasoning | Partial | `ontology/rdf.py:598` | subclass/disjoint/property-chain only |
| BL-31 | JSON-LD export/import with loss accounting | Implemented | `ontology/rdf.py:77,254,337,529` | round-trip validator exists |
| BL-32 | Ontology-as-code, semantic change records, stewardship | Partial | `ontology/gitops.py:31`, `ontology/stewardship.py`, `scripts/ontology_diff.py` | no CI SHACL suite against W3C tests |
| BL-33 | Mapping language (CML) → engine-neutral IR → LPG/RDF + PROV-O | Implemented | `mapping/cml.py`, `mapping/ir.py`, `mapping/executor.py:28` | not R2RML/RML-conformant |
| BL-34 | Deterministic identity resolution | Implemented (person identity) | `identity/resolver.py:49` | only person identity; no blocking, no probabilistic ER |
| BL-35 | Identity candidate review queue (merge/split review) | Partial | `identity/candidates.py:26` | |
| BL-36 | Probabilistic entity resolution | Absent | — | candidate REUSE: Splink / Zingg (see deep dives) |
| BL-37 | Revisions and bitemporal reads (valid time + transaction time) | Implemented | `contracts/revision.py:10`, `graph/bitemporal.py` | application-layer temporal model |
| BL-38 | Graph diff, snapshots, playback | Implemented | `graph/diff_engine.py:17`, `graph/snapshots.py`, `graph/playback.py` | |
| BL-39 | Claims, contradictions, resolution decisions | Implemented | `truth/engine.py:26,66,91,158` | in-memory `TruthStore` |
| BL-40 | Epistemic separation (PROPOSED-until-validated; CORROBORATED/DISPUTED/UNCORROBORATED) | Implemented (contract) / Partial (store-wide) | `ai/boundary.py:6,77,113,135` | not yet a storage-level plane on every backend |
| BL-41 | Evidence manifests and lineage | Implemented | `provenance/evidence.py:31`, `provenance/lineage.py` | |
| BL-42 | Code graph (Python/TypeScript symbols, diff hunks, incremental re-index) | Implemented (2 languages) / Partial (polyglot) | `codegraph/parser.py:45`, `codegraph/diff_hunk.py`, `ingestion/incremental_indexer.py:30`, `ingestion/polyglot_linker.py` | Tree-sitter referenced in 2 files; SCIP/LSIF absent |
| BL-43 | Graph algorithms (paths, centrality, community, similarity, anomaly) | Implemented (in-process) | `graph/algorithms.py`, `graph/community.py:18`, `graph/paths.py`, `graph/anomaly.py` | pure Python; scale untested |
| BL-44 | GNN / link prediction | Partial | `gnn/engine.py` | pure-Python heuristics; `neural/*` cannot import without numpy |
| BL-45 | Egress gateway, DLP, tokenisation vault, per-call manifest | Implemented | `egress/gateway.py:106`, `egress/dlp.py`, `egress/vault.py`, `egress/manifest.py` | default S0 |
| BL-46 | PII detection and privacy (classification, DSAR, retention, residency) | Implemented / Partial (by docstring) | `privacy/*.py` | DSAR, consent, residency marked partial in their own docstrings |
| BL-47 | MCP server (read-oriented tools; QueryPlan tool) | Implemented | `apps/mcp/main.py` (18 tools incl. `query(plan)`, `run_agent`) | write tools absent by design (ADR-007) |
| BL-48 | Agent runtime, governed tools, XAI | Partial | `agents/`, `contracts/agent.py`, `contracts/tool.py`, `xai/engine.py` | |
| BL-49 | Observability: Prometheus text metrics, JSON logs, optional OTel | Implemented / Partial | `observability/metrics.py`, `observability/logging.py`, `observability/otel.py:25` | |
| BL-50 | Backup/restore, WAL | Implemented (scripts) / live-unverified | `scripts/backup.py`, `scripts/restore.py`, `recovery/wal.py:20` | |
| BL-51 | Federation / virtual sources planner | Partial | `federation/planner.py:35` | |
| BL-52 | Real-time mutation streaming and webhooks | Implemented (in-process) | `streaming/mutation_stream.py:25`, `events/emitter.py` | no external bus (Kafka/NATS absent) |
| BL-53 | Collaboration (annotations, workspaces, shared queries) | Implemented | `collaboration/*.py` | no real-time co-editing / CRDT |
| BL-54 | Web UI: graph canvas, admin, studio | Implemented | `apps/web/src/*` | redesign planned; large-graph performance unmeasured |
| BL-55 | VS Code extension | Implemented (files) | `apps/vscode-extension/` | not exercised in this run |
| BL-56 | Wisdom graph (decisions, rationale, outcomes, lessons) | Planned | `EOIP-engg-doc-pkg/wisdom-graph-requirements.md` | `graph/decisions.py` exists as a precursor (Unknown depth) |
| BL-57 | Numerical/neural stack N0–N3 (CPU-only policy) | Planned / Partial | `neural/runtime.py:11`; ADR-H15/H16/H17 in `docs/decisions/` | numpy not in the lock |
| BL-58 | GraphQL API | Absent | — | |
| BL-59 | SQL/PGQ or GQL execution | Absent (transpiler subset only) | `moonshot/universal_transpiler.py` | |
| BL-60 | External event bus (Kafka/NATS/Redpanda) | Absent | only string references in 4 files | in-process streaming only |

## 6. What the baseline means for the competitive programme

1. **Backend neutrality is real at the adapter level but shallow at the query level.** Portability today means "every backend implements the same CRUD/neighbourhood protocol, and traversal happens in Python". That is safe and portable, but it gives up each engine's optimiser for deep multi-hop and analytics. The competitor research has to judge which capabilities should be pushed down (backend-native) and which stay emulated.
2. **The largest P0 risk is permissions and tenancy, not features.** Permission metadata is captured, but nothing filters retrieval or answers by source ACL (BL-18), and tenant isolation is a contract only (BL-20). Per Master Prompt §4.3 items 8 and 9 these are P0 defects whatever any competitor does.
3. **Semantic-web capabilities are in-house subsets.** SHACL, OWL and RDF are implemented without the standard engines. Interoperability claims must be tested against W3C test suites before they are made (Standards gate).
4. **Many "intelligence" modules run only against the in-memory store** (24 modules). Their behaviour on HugeGraph, Neo4j or Neptune at realistic sizes is unknown.
5. **The ML stack is not installed.** Neural/GNN claims are design intent until N0/N1 are installed and the anti-stub probes pass (Graph-Neurons programme).

## BASELINE_UNCERTAINTIES

| U-ID | Uncertainty | Why it matters | How to resolve |
|---|---|---|---|
| U-01 | Live behaviour of the HugeGraph, Neo4j, Neptune, JanusGraph, Fuseki and GraphDB adapters was not exercised | All backend-parity claims are static | Run `tests/runtime_hubble` and the conformance suite against each engine (`15-VALIDATION-BENCHMARK-PLAN.md` BM-01) |
| U-02 | Whether the 24 modules that import `MemoryGraphStore` directly have backend-backed equivalents | Determines which features exist in production deployments | Trace each import; record Implemented/Partial per backend |
| U-03 | Neptune IAM (SigV4) authentication support | Neptune with IAM auth enabled rejects unsigned calls | Inspect `graph/neptune.py` auth path; live test |
| U-04 | Whether any code path enforces source ACLs outside the files searched | BL-18 is marked Absent from a targeted search | Full-repo audit of retrieval/answer paths; permission-leakage test J5 |
| U-05 | Physical tenant isolation on any backend | Cross-tenant leakage is P0 | Implement and test J13 |
| U-06 | Scale and latency of in-process algorithms, HNSW and BM25 | No benchmarks run | BM-02..BM-06 |
| U-07 | W3C conformance of the in-house SHACL and JSON-LD code | Standards gate | Run the W3C SHACL and JSON-LD test suites |
| U-08 | Depth of `graph/decisions.py`, `brain/`, `moonshot/` modules | Some may be prototypes | Code review per module |
| U-09 | Whether the web UI handles 100k+ node views | Visualisation competitiveness | BM-UX-01 |
| U-10 | Product name "Semaplexvell" spelling | Branding in artifacts | Product owner confirmation |
| U-11 | GPU availability at customer sites (H-17, open) | ML sizing | Interim CPU-only policy (ADR-H15/H16/H17) |
| U-12 | Legal positions on any licence | Licensing gate only flags triggers | Legal review of flagged items in `02-TECHNOLOGY-REGISTRY.md` |
