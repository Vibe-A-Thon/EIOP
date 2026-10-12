# Audit Coverage Ledger

**Repository:** `EIOP` | **Branch/commit:** `dev_local` / `350915b760bc2109352d9c59dc269460aa8227eb` | **Audit date:** 2026-10-13

## Scope And Method

This ledger is the proof-of-read inventory for `gaps-audit-cp.md` and `GUI-UIX-requirements.md`. The scanner opened every included first-party text/source/configuration file in binary, decoded it, counted every line, hashed the bytes and indexed IDs/routes/env references. Markdown was read line-by-line. Demo/example pieces and demo/sample data are listed but marked `EXCLUDED` from conclusions by user instruction. Generated runtime artifacts, lockfiles and binary office/checksum content are listed with reasons. `.audit-scratch/` is temporary audit machinery and is intentionally absent because it is deleted before delivery.

## Totals

| Measure | Total |
|---|---:|
| Repository files listed | 1,824 |
| Fully read/indexed files | 1,490 |
| Explicitly excluded files | 334 |
| Fully read lines | 334,170 |
| Markdown files listed | 219 |
| Markdown files fully read | 207 |
| Requirement records normalized | 2,603 |
| Normative candidate lines reviewed | 3,237 |
| REST integrations catalogued | 734 |
| WebSocket channels catalogued | 1 |
| Proposed missing GUI contracts | 20 |
| Environment/config symbols indexed | 138 |

## Directory Summary

| Top-level folder | Files | Fully read | Lines in fully read text |
|---|---:|---:|---:|
| `.` | 21 | 18 | 50,132 |
| `.github` | 2 | 2 | 138 |
| `.tmp` | 109 | 0 | 0 |
| `EOIP-engg-doc-pkg` | 226 | 221 | 54,201 |
| `apps` | 146 | 143 | 24,068 |
| `config` | 26 | 26 | 960 |
| `data` | 100 | 0 | 0 |
| `demo` | 114 | 0 | 0 |
| `deploy` | 35 | 35 | 3,037 |
| `docs` | 6 | 6 | 3,252 |
| `packages` | 583 | 583 | 132,929 |
| `schemas` | 45 | 45 | 2,551 |
| `scripts` | 103 | 103 | 7,230 |
| `secrets.example` | 2 | 2 | 38 |
| `tests` | 306 | 306 | 55,634 |

## Module, Framework And Entry-Point Map

| Module | Language/framework | Entry point / responsibility | Evidence |
|---|---|---|---|
| API | Python 3.11, FastAPI, Pydantic, Uvicorn | App factory, HTTP/WebSocket boundary and router assembly | `apps/api/main.py:1`; `apps/api/app.py:191` |
| Domain platform | Python packages | Graph, ontology, ingestion, query, RAG, agents, governance and enterprise services | `packages/eoip/__init__.py:1` |
| Worker | Python | Persistent acquisition/job execution sharing domain contracts | `deploy/docker-compose.yml:116` |
| MCP | Python FastMCP/httpx | Read-only facade over authenticated API | `apps/mcp/main.py:1` |
| Web | React/Vite JavaScript | Existing client inspected only for backend calls/security, not redesign input | `apps/web/package.json:1` |
| VS Code | JavaScript extension + MCP client | Editor integration | `apps/vscode-extension/extension.js:1` |
| Infrastructure | Docker Compose, Helm, PowerShell/shell | Local stack, optional services, deployment and operational wrappers | `deploy/docker-compose.yml:1`; `deploy/helm/eoip/Chart.yaml:1`; `scripts/container.ps1:1` |
| Tests | pytest, Playwright/Vitest-compatible web tooling | Unit, security, integration, runtime and E2E verification | `tests/conftest.py:1`; `apps/web/playwright.config.js:1` |

## Runtime Topology

| Runtime | Port/exposure | State/dependency | Audit note |
|---|---|---|---|
| `eoip-api` | loopback `${EOIP_API_PORT:-8000}:8000` | GraphStore, filesystem application data, optional local model | 734 live REST operations plus one WebSocket. |
| `eoip-worker` | internal | Shared graph/application volumes and connector endpoints | Background acquisition/jobs; durability varies by service. |
| `eoip-mcp` | loopback `${EOIP_MCP_PORT:-8001}:8001` | Calls API with bearer token | Read-only facade (`apps/mcp/main.py:1`). |
| `eoip-web` | loopback `${EOIP_WEB_PORT:-8080}:8080` | Static production bundle + API | Current design excluded from redesign input. |
| HugeGraph | internal | RocksDB volume; default graph backend | Canonical reference backend, not externally published by default. |
| Neo4j | optional profile/internal | Alternate graph volume | Adapter-supported, not the mandatory reference topology. |
| Hubble | loopback `${EOIP_HUBBLE_PORT:-8088}:8088` | HugeGraph administration | External/browser receipt not rerun. |
| Local model | internal/optional | Model volume | Real model availability and quality are deployment-dependent. |
| Prometheus | loopback `9090` in metrics profile | Metrics volume | No production observability receipt in this audit. |

Queues are implemented primarily through application job abstractions and persisted files rather than an independently catalogued broker. Graph backends include HugeGraph, Neo4j, Neptune and memory; vector/search/model adapters are configuration-selected. External dependencies include source-system APIs, optional external model endpoints and cloud graph services, all of which require deployment-specific credentials and egress policy.

## Environment And Feature Configuration

All 138 environment symbols found in source/config/docs are listed. Secret-like defaults are deliberately redacted; “no single literal default” means declarations disagree or defer to runtime and must be resolved before release.

| Variable | Kind | Default/declaration | Evidence |
|---|---|---|---|
| `AWS_ACCESS_KEY` | `secret` | No single literal default found | `packages/eoip/egress/dlp.py:34` |
| `AWS_IAM` | `configuration` | "aws_iam" | `packages/eoip/systems/registry.py:55` |
| `AZURE_COSMOS_DB` | `configuration` | "AZURE_COSMOS_DB" | `packages/eoip/graph/database_adapters.py:69` |
| `EOIP_ACCEPTANCE_CONFLUENCE_URL` | `configuration` | No single literal default found | `deploy/docker-compose.dlq-acceptance.yml:98` |
| `EOIP_ACCEPTANCE_INVALID_TOKEN` | `secret` | [secret; no default reproduced] | `deploy/docker-compose.dlq-acceptance.yml:14` |
| `EOIP_ACCEPTANCE_REPORT` | `configuration` | No single literal default found | `deploy/docker-compose.acceptance.yml:30` |
| `EOIP_ACCEPTANCE_RUN` | `configuration` | $runId | `scripts/container.ps1:302` |
| `EOIP_ACCEPTANCE_SOURCE_TOKEN` | `secret` | [secret; no default reproduced] | `deploy/docker-compose.dlq-acceptance.yml:13` |
| `EOIP_ACCEPTANCE_SOURCE_URL` | `configuration` | No single literal default found | `deploy/docker-compose.acceptance.yml:28` |
| `EOIP_ACCEPTANCE_TARGET_URL` | `configuration` | No single literal default found | `deploy/docker-compose.acceptance.yml:29` |
| `EOIP_ADMIN_GREMLIN_ENABLED` | `feature/mode` | 1` | `EOIP-engg-doc-pkg/reference/api-reference.md:240` |
| `EOIP_API_PORT` | `configuration` | 8000 | `deploy/.env.example:16` |
| `EOIP_API_REPLICAS` | `configuration` | 2 | `packages/eoip/ops/production.py:81` |
| `EOIP_API_TOKEN` | `secret` | [secret value omitted] | `deploy/.env.example:3` |
| `EOIP_API_URL` | `configuration` | http://eoip-api:8000 | `apps/mcp/main.py:32` |
| `EOIP_AUDIT_GENESIS` | `configuration` | No single literal default found | `packages/eoip/enterprise/audit.py:81` |
| `EOIP_AUTHZ_TOKEN_SECRET` | `secret` | [secret value omitted] | `packages/eoip/authz/tokens.py:40` |
| `EOIP_AUTH_REQUIRED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:327` |
| `EOIP_BEHAVIORAL_GATE_BASE_REF` | `configuration` | No single literal default found | `packages/eoip/verification/behavioral_gate.py:852` |
| `EOIP_BEHAVIORAL_GATE_HEAD_REF` | `configuration` | HEAD | `packages/eoip/verification/behavioral_gate.py:853` |
| `EOIP_BEHAVIORAL_GATE_RISK` | `configuration` | No single literal default found | `packages/eoip/verification/behavioral_gate.py:855` |
| `EOIP_BENCHMARK_STORAGE_TYPE` | `configuration` | 'NVMe | `EOIP-engg-doc-pkg/reference/benchmarking.md:31` |
| `EOIP_BUILD_DIRTY` | `configuration` | No single literal default found | `scripts/benchmark.py:152` |
| `EOIP_BUILD_REVISION` | `configuration` | No single literal default found | `scripts/benchmark.py:151` |
| `EOIP_CACHE_BACKEND` | `configuration` | local | `packages/eoip/ops/production.py:24` |
| `EOIP_CACHE_MAX_ENTRIES` | `configuration` | 10000 | `packages/eoip/ops/production.py:27` |
| `EOIP_CACHE_TTL_SECONDS` | `configuration` | 300 | `packages/eoip/ops/production.py:26` |
| `EOIP_CB_FAILURE_THRESHOLD` | `configuration` | No single literal default found | `tests/unit/test_enterprise_infrastructure.py:107` |
| `EOIP_COMMAND_FAILED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:462` |
| `EOIP_COMPOSE_COMMAND` | `configuration` | 'podman-compose' | `scripts/container.ps1:11` |
| `EOIP_CONFIG_DIR` | `configuration` | /opt/eoip/config`, | `EOIP-engg-doc-pkg/reference/docker-local.md:636` |
| `EOIP_CONFLUENCE` | `configuration` | No single literal default found | `packages/eoip/connectors/config.py:26` |
| `EOIP_CONFLUENCE_PASSWORD` | `secret` | [secret; no default reproduced] | `deploy/.env.example:10` |
| `EOIP_CONFLUENCE_PROD_TOKEN` | `secret` | [secret; no default reproduced] | `tests/unit/test_acquisition_fabric.py:28` |
| `EOIP_CONFLUENCE_TOKEN` | `secret` | [secret; no default reproduced] | `deploy/.env.example:8` |
| `EOIP_CONFLUENCE_URL` | `configuration` | https://confluence.example | `deploy/.env.example:7` |
| `EOIP_CONFLUENCE_USERNAME` | `configuration` | No single literal default found | `deploy/.env.example:9` |
| `EOIP_CONTAINER_RUNTIME` | `configuration` | podman | `deploy/.env.example:2` |
| `EOIP_CONTEXT_FAILED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:137` |
| `EOIP_CORS_ORIGINS` | `configuration` | empty | `apps/api/app.py:219` |
| `EOIP_DATA_DIR` | `configuration` | 'C:\recovery-target\data' | `EOIP-engg-doc-pkg/reference/docker-local.md:619` |
| `EOIP_DATA_NS` | `configuration` | "urn:eoip:data:" | `packages/eoip/graph/format_converter.py:16` |
| `EOIP_DEBUG` | `configuration` | No single literal default found | `tests/unit/test_enterprise_infrastructure.py:106` |
| `EOIP_DEMO_API_URL` | `configuration` | No single literal default found | `apps/vscode-extension/demo/index.js:63` |
| `EOIP_DEMO_CONTEXT` | `configuration` | No single literal default found | `apps/vscode-extension/demo/index.js:65` |
| `EOIP_DEMO_DELAY_MS` | `configuration` | No single literal default found | `apps/vscode-extension/demo/index.js:67` |
| `EOIP_DEMO_MCP_URL` | `configuration` | No single literal default found | `apps/vscode-extension/demo/index.js:64` |
| `EOIP_DEMO_NO_PAUSE` | `configuration` | == | `apps/vscode-extension/demo/index.js:66` |
| `EOIP_DEMO_RECEIPT` | `configuration` | No single literal default found | `apps/vscode-extension/demo/index.js:62` |
| `EOIP_DEMO_TOKEN` | `secret` | [secret; no default reproduced] | `apps/vscode-extension/demo/index.js:61` |
| `EOIP_EMBEDDING_PROVIDER` | `configuration` | = | `packages/eoip/models/embeddings.py:165` |
| `EOIP_ENTITY_REQUIRED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:520` |
| `EOIP_ENV` | `configuration` | No single literal default found | `packages/eoip/ops/bundle.py:81` |
| `EOIP_ENVIRONMENT` | `configuration` | No single literal default found | `tests/unit/test_enterprise_infrastructure.py:105` |
| `EOIP_EXTENSION_RECEIPT` | `configuration` | No single literal default found | `apps/vscode-extension/test/runTest.js:27` |
| `EOIP_GITHUB_TOKEN` | `secret` | [secret; no default reproduced] | `EOIP-engg-doc-pkg/reference/connectors-github.md:57` |
| `EOIP_GITHUB_WEBHOOK_SECRET` | `secret` | [secret; no default reproduced] | `EOIP-engg-doc-pkg/reference/connectors-github.md:58` |
| `EOIP_GITLAB_TOKEN` | `secret` | [secret; no default reproduced] | `EOIP-engg-doc-pkg/reference/connectors-gitlab.md:67` |
| `EOIP_GITLAB_URL` | `configuration` | No single literal default found | `EOIP-engg-doc-pkg/reference/connectors.md:189` |
| `EOIP_GITLAB_WEBHOOK_SIGNING` | `configuration` | No single literal default found | `EOIP-engg-doc-pkg/reference/connectors-gitlab.md:68` |
| `EOIP_GOV_GROUNDEDNESS_THRESHOLD` | `configuration` | 0.8 | `apps/api/extended.py:184` |
| `EOIP_GOV_UNSAFE_ACTION_THRESHOLD` | `configuration` | 0.1 | `apps/api/extended.py:187` |
| `EOIP_GRAPH_` | `configuration` | No single literal default found | `EOIP-engg-doc-pkg/audits/audit-2026-10-06/assessed-gap-report.json:205` |
| `EOIP_GRAPH_BACKEND` | `configuration` | neptune\|hugegraph\|memory`. | `EOIP-engg-doc-pkg/06-architecture.md:278` |
| `EOIP_GRAPH_CLUSTER_MODE` | `feature/mode` | hugegraph-hstore | `packages/eoip/ops/production.py:84` |
| `EOIP_GRAPH_CONFIG` | `configuration` | No single literal default found | `packages/eoip/graph/backends.py:101` |
| `EOIP_GRAPH_DATABASE` | `configuration` | <logical-name> | `config/graph-store.yaml:9` |
| `EOIP_GRAPH_NODES` | `configuration` | 3 | `packages/eoip/ops/production.py:85` |
| `EOIP_GRAPH_PASSWORD` | `secret` | [secret; no default reproduced] | `EOIP-engg-doc-pkg/76-multi-backend.md:79` |
| `EOIP_GRAPH_URL` | `configuration` | <backend | `config/graph-store.yaml:8` |
| `EOIP_GRAPH_USER` | `configuration` | No single literal default found | `EOIP-engg-doc-pkg/76-multi-backend.md:78` |
| `EOIP_HTTP_` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:366` |
| `EOIP_HTTP_401` | `configuration` | No single literal default found | `apps/vscode-extension/test/suite/refusals.js:9` |
| `EOIP_HUBBLE_PORT` | `configuration` | 8088 | `deploy/.env.example:18` |
| `EOIP_HUGEGRAPH_` | `configuration` | No single literal default found | `EOIP-engg-doc-pkg/76-multi-backend.md:81` |
| `EOIP_HUGEGRAPH_GRAPH` | `configuration` | hugegraph | `packages/eoip/graph/backends.py:118` |
| `EOIP_HUGEGRAPH_PASSWORD` | `secret` | [secret value omitted] | `packages/eoip/graph/backends.py:120` |
| `EOIP_HUGEGRAPH_URL` | `configuration` | 'http://hugegraph-server:8080' | `EOIP-engg-doc-pkg/reference/benchmarking.md:39` |
| `EOIP_HUGEGRAPH_USER` | `configuration` | admin | `packages/eoip/graph/backends.py:119` |
| `EOIP_INSTALL_KEY` | `secret` | No single literal default found | `apps/api/extended.py:206` |
| `EOIP_INVALID_API_URL` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:334` |
| `EOIP_INVALID_MCP_ARGUMENTS` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:496` |
| `EOIP_INVALID_QUESTION` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:480` |
| `EOIP_INVALID_RESPONSE` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:361` |
| `EOIP_JIRA_TOKEN` | `secret` | [secret; no default reproduced] | `EOIP-engg-doc-pkg/reference/connectors.md:188` |
| `EOIP_JIRA_URL` | `configuration` | No single literal default found | `EOIP-engg-doc-pkg/reference/connectors.md:187` |
| `EOIP_JIRA_WEBHOOK_SECRET` | `secret` | [secret; no default reproduced] | `tests/unit/test_acquisition_fabric.py:388` |
| `EOIP_KILL_SWITCH` | `configuration` | empty | `apps/api/extended.py:191` |
| `EOIP_LEASE_PATH` | `configuration` | /leases/worker.lock`), | `EOIP-engg-doc-pkg/reference/deployment-ha.md:47` |
| `EOIP_LEASE_TTL_SECONDS` | `configuration` | 30 | `apps/worker/main.py:198` |
| `EOIP_LICENSE_KEY` | `secret` | No single literal default found | `packages/eoip/licensing/cli.py:7` |
| `EOIP_LICENSE_KEY_FILE` | `secret` | No single literal default found | `packages/eoip/licensing/license_file.py:17` |
| `EOIP_LICENSE_PATH` | `configuration` | empty | `apps/api/extended.py:245` |
| `EOIP_LICENSE_VENDOR_KEY` | `secret` | eoip-dev-vendor-key | `apps/api/extended.py:248` |
| `EOIP_LIVE_DLQ_ACCEPTANCE` | `configuration` | No single literal default found | `deploy/docker-compose.dlq-acceptance.yml:95` |
| `EOIP_LOAD_DEMO` | `configuration` | true | `deploy/.env.example:5` |
| `EOIP_MCP_PORT` | `configuration` | 8001 | `deploy/.env.example:17` |
| `EOIP_MCP_REPLICAS` | `configuration` | 2 | `packages/eoip/ops/production.py:83` |
| `EOIP_MISSING_VAR` | `configuration` | No single literal default found | `tests/unit/test_ops.py:57` |
| `EOIP_NAMESPACE` | `configuration` | "urn:eoip:ontology:" | `packages/eoip/ontology/rdf.py:17` |
| `EOIP_NEPTUNE_URL` | `configuration` | https://<endpoint>:8182` | `EOIP-engg-doc-pkg/76-multi-backend.md:102` |
| `EOIP_NO_ACTIVE_EDITOR` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:92` |
| `EOIP_NS` | `configuration` | "urn:eoip:ontology:" | `packages/eoip/graph/format_converter.py:15` |
| `EOIP_OFFLINE` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:312` |
| `EOIP_OLLAMA_EMBED_MODEL` | `feature/mode` | No single literal default found | `packages/eoip/models/embeddings.py:48` |
| `EOIP_OLLAMA_MODEL` | `feature/mode` | empty | `packages/eoip/models/provider.py:30` |
| `EOIP_OLLAMA_URL` | `configuration` | http://local-model:11434 | `packages/eoip/models/provider.py:31` |
| `EOIP_OTEL_ENDPOINT` | `configuration` | No single literal default found | `packages/eoip/observability/otel.py:4` |
| `EOIP_QA_COLLECTOR_OUT` | `configuration` | No single literal default found | `packages/eoip/qa/evidence.py:36` |
| `EOIP_QUERY_CACHE` | `configuration` | 1).""" | `apps/api/app.py:1036` |
| `EOIP_RAW_TELEMETRY_REFUSED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:697` |
| `EOIP_REDIS_URL` | `configuration` | empty | `packages/eoip/ops/production.py:25` |
| `EOIP_REGISTRY_PATH` | `configuration` | No single literal default found | `apps/api/extended.py:203` |
| `EOIP_REPOSITORY_ROOT_REQUIRED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:731` |
| `EOIP_RESPONSE_TOO_LARGE` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:353` |
| `EOIP_RUNTIME_API_URL` | `configuration` | http://localhost:8000 | `tests/runtime_hubble/conftest.py:44` |
| `EOIP_RUNTIME_HUBBLE` | `configuration` | 1`. | `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md:8178` |
| `EOIP_RUNTIME_HUBBLE_URL` | `configuration` | http://localhost:8088 | `tests/runtime_hubble/conftest.py:56` |
| `EOIP_RUNTIME_RUN_ID` | `configuration` | 'hubble-acceptance-20261005' | `EOIP-engg-doc-pkg/reference/hubble-runtime-validation.md:366` |
| `EOIP_SENTENCE_TRANSFORMER_MODEL` | `feature/mode` | all-MiniLM-L6-v2 | `packages/eoip/models/embeddings.py:119` |
| `EOIP_SERVICENOW` | `configuration` | No single literal default found | `packages/eoip/connectors/config.py:26` |
| `EOIP_SERVICENOW_PASSWORD` | `secret` | [secret; no default reproduced] | `deploy/.env.example:14` |
| `EOIP_SERVICENOW_TOKEN` | `secret` | [secret; no default reproduced] | `deploy/.env.example:12` |
| `EOIP_SERVICENOW_URL` | `configuration` | https://instance.service-now.example | `deploy/.env.example:11` |
| `EOIP_SERVICENOW_USERNAME` | `configuration` | No single literal default found | `deploy/.env.example:13` |
| `EOIP_SOURCE_NOT_FOUND` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:153` |
| `EOIP_SOURCE_OUTSIDE_REPOSITORY` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:158` |
| `EOIP_SOURCE_REQUIRED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:726` |
| `EOIP_SYMBOL_NOT_FOUND` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:109` |
| `EOIP_TARGET_REQUIRED` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:525` |
| `EOIP_TIMEOUT` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:381` |
| `EOIP_UNDEFINED` | `configuration` | No single literal default found | `tests/unit/test_ops.py:210` |
| `EOIP_UNSAFE_SOURCE_PATH` | `configuration` | No single literal default found | `apps/vscode-extension/extension.js:735` |
| `EOIP_WEB_PORT` | `configuration` | 8080 | `deploy/.env.example:15` |
| `EOIP_WORKER_REPLICAS` | `configuration` | 2 | `packages/eoip/ops/production.py:82` |
| `HUGEGRAPH_PASSWORD` | `secret` | [secret value omitted] | `deploy/.env.example:4` |
| `NEO4J_AUTH` | `configuration` | neo4j/eoip-local-password | `deploy/docker-compose.yml:49` |
| `REDIS_SEARCH` | `configuration` | "REDIS_SEARCH" | `packages/eoip/graph/database_adapters.py:84` |

## Structured Configuration Keys

The table flattens scalar/list defaults from operational files under `config/`, Helm values, `pyproject.toml` and `pyrightconfig.json`. Lists are summarized by length to avoid reproducing domain/example records; secret-like values are redacted. Runtime code defaults remain represented in the environment table above.

| Source | Key | Default/value |
|---|---|---|
| `config/agents/trace-impact.yaml:1` | `agent_id` | TraceImpact |
| `config/agents/trace-impact.yaml:2` | `description` | Deterministic read-only trace and impact analysis agent. Uses graph traversal to find connected enti... |
| `config/agents/trace-impact.yaml:6` | `allowed_tools` | [list:5] |
| `config/agents/trace-impact.yaml:14` | `budgets.max_steps` | 10 |
| `config/agents/trace-impact.yaml:15` | `budgets.max_seconds` | 30 |
| `config/agents/trace-impact.yaml:16` | `budgets.max_depth` | 8 |
| `config/agents/trace-impact.yaml:17` | `budgets.max_results` | 100 |
| `config/agents/trace-impact.yaml:19` | `read_only` | true |
| `config/benchmarks/mvp-v1.json:2` | `schema_version` | eoip-benchmark-manifest/v1 |
| `config/benchmarks/mvp-v1.json:3` | `manifest_id` | mvp-v1 |
| `config/benchmarks/mvp-v1.json:4` | `requirement` | NFR-PERF-001 |
| `config/benchmarks/mvp-v1.json:5` | `description` | EOIP MVP deterministic graph query benchmark |
| `config/benchmarks/mvp-v1.json:7` | `dataset.generator` | scripts.benchmark_data |
| `config/benchmarks/mvp-v1.json:8` | `dataset.seed` | 42 |
| `config/benchmarks/mvp-v1.json:10` | `dataset.profiles.smoke` | s |
| `config/benchmarks/mvp-v1.json:11` | `dataset.profiles.full` | baseline |
| `config/benchmarks/mvp-v1.json:15` | `reference_hardware.cpu_logical_cores_available_to_docker` | 8 |
| `config/benchmarks/mvp-v1.json:16` | `reference_hardware.memory_gib` | 32 |
| `config/benchmarks/mvp-v1.json:17` | `reference_hardware.storage` | local NVMe or SSD |
| `config/benchmarks/mvp-v1.json:19` | `bulk_batch_size` | 500 |
| `config/benchmarks/mvp-v1.json:22` | `runs.smoke.warmups` | 3 |
| `config/benchmarks/mvp-v1.json:23` | `runs.smoke.samples` | 20 |
| `config/benchmarks/mvp-v1.json:22` | `runs.full.warmups` | 10 |
| `config/benchmarks/mvp-v1.json:23` | `runs.full.samples` | 100 |
| `config/benchmarks/mvp-v1.json:30` | `workloads` | [list:5] |
| `config/domain-packs/bfsi/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/bfsi/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/bfsi/ontology.yaml:4` | `domains` | [list:2] |
| `config/domain-packs/bfsi/ontology.yaml:10` | `classes.Trade.description` | A financial trade or order executed on an instrument. |
| `config/domain-packs/bfsi/ontology.yaml:12` | `classes.Trade.properties.trade_id` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:13` | `classes.Trade.properties.instrument` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:14` | `classes.Trade.properties.notional` | DOUBLE |
| `config/domain-packs/bfsi/ontology.yaml:15` | `classes.Trade.properties.trade_date` | DATE |
| `config/domain-packs/bfsi/ontology.yaml:16` | `classes.Trade.properties.canonical_id` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:17` | `classes.Trade.properties.name` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:20` | `classes.Trade.relationships.SETTLES_INTO.out` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:21` | `classes.Trade.relationships.SETTLES_INTO.in` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:10` | `classes.Settlement.description` | A settlement instruction and its lifecycle state. |
| `config/domain-packs/bfsi/ontology.yaml:26` | `classes.Settlement.properties.settlement_id` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:27` | `classes.Settlement.properties.settlement_status` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:28` | `classes.Settlement.properties.settlement_date` | DATE |
| `config/domain-packs/bfsi/ontology.yaml:16` | `classes.Settlement.properties.canonical_id` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:17` | `classes.Settlement.properties.name` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:20` | `classes.Settlement.relationships.FUNDS.out` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:21` | `classes.Settlement.relationships.FUNDS.in` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:10` | `classes.Account.description` | A customer or ledger account under a business capability. |
| `config/domain-packs/bfsi/ontology.yaml:39` | `classes.Account.properties.account_number` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:40` | `classes.Account.properties.account_type` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:41` | `classes.Account.properties.currency` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:16` | `classes.Account.properties.canonical_id` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:17` | `classes.Account.properties.name` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:20` | `classes.Account.relationships.HELD_UNDER.out` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:21` | `classes.Account.relationships.HELD_UNDER.in` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:10` | `classes.Policy.description` | An insurance policy linked to knowledge documentation. |
| `config/domain-packs/bfsi/ontology.yaml:52` | `classes.Policy.properties.policy_number` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:53` | `classes.Policy.properties.policy_type` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:54` | `classes.Policy.properties.premium` | DOUBLE |
| `config/domain-packs/bfsi/ontology.yaml:16` | `classes.Policy.properties.canonical_id` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:17` | `classes.Policy.properties.name` | TEXT |
| `config/domain-packs/bfsi/ontology.yaml:20` | `classes.Policy.relationships.GOVERNED_BY.out` | [list:1] |
| `config/domain-packs/bfsi/ontology.yaml:21` | `classes.Policy.relationships.GOVERNED_BY.in` | [list:2] |
| `config/domain-packs/bfsi/ontology.yaml:62` | `validators` | [list:1] |
| `config/domain-packs/bfsi/pack.yaml:1` | `name` | bfsi |
| `config/domain-packs/bfsi/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/bfsi/pack.yaml:3` | `extends` | core |
| `config/domain-packs/bfsi/pack.yaml:4` | `description` | Banking, financial services and insurance pack: trade, account and policy concepts with regulatory r... |
| `config/domain-packs/compliance/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/compliance/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/compliance/ontology.yaml:4` | `domains` | [list:3] |
| `config/domain-packs/compliance/ontology.yaml:11` | `classes.Control.description` | A compliance control mapped to services and processes. |
| `config/domain-packs/compliance/ontology.yaml:13` | `classes.Control.properties.control_id` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:14` | `classes.Control.properties.framework` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:15` | `classes.Control.properties.control_status` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:16` | `classes.Control.properties.canonical_id` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:17` | `classes.Control.properties.name` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:20` | `classes.Control.relationships.MITIGATES.out` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:21` | `classes.Control.relationships.MITIGATES.in` | [list:2] |
| `config/domain-packs/compliance/ontology.yaml:20` | `classes.Control.relationships.APPLIES_TO.out` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:21` | `classes.Control.relationships.APPLIES_TO.in` | [list:2] |
| `config/domain-packs/compliance/ontology.yaml:11` | `classes.Policy.description` | Extends the shared policy term with attestation linkage. |
| `config/domain-packs/compliance/ontology.yaml:29` | `classes.Policy.properties.policy_id` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:30` | `classes.Policy.properties.effective_date` | DATE |
| `config/domain-packs/compliance/ontology.yaml:31` | `classes.Policy.properties.review_date` | DATE |
| `config/domain-packs/compliance/ontology.yaml:16` | `classes.Policy.properties.canonical_id` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:17` | `classes.Policy.properties.name` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:20` | `classes.Policy.relationships.MANDATES.out` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:21` | `classes.Policy.relationships.MANDATES.in` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:20` | `classes.Policy.relationships.ATTESTED_BY.out` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:21` | `classes.Policy.relationships.ATTESTED_BY.in` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:11` | `classes.Risk.description` | A registered risk with inherent and residual scoring. |
| `config/domain-packs/compliance/ontology.yaml:45` | `classes.Risk.properties.risk_id` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:46` | `classes.Risk.properties.inherent_score` | DOUBLE |
| `config/domain-packs/compliance/ontology.yaml:47` | `classes.Risk.properties.residual_score` | DOUBLE |
| `config/domain-packs/compliance/ontology.yaml:16` | `classes.Risk.properties.canonical_id` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:17` | `classes.Risk.properties.name` | TEXT |
| `config/domain-packs/compliance/ontology.yaml:20` | `classes.Risk.relationships.ACCEPTED_IN.out` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:21` | `classes.Risk.relationships.ACCEPTED_IN.in` | [list:1] |
| `config/domain-packs/compliance/ontology.yaml:55` | `validators` | [list:1] |
| `config/domain-packs/compliance/pack.yaml:1` | `name` | compliance |
| `config/domain-packs/compliance/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/compliance/pack.yaml:3` | `extends` | core |
| `config/domain-packs/compliance/pack.yaml:4` | `description` | Compliance pack: controls, policies, audit findings and evidence chains extending core META/DECISION... |
| `config/domain-packs/cybersecurity/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/cybersecurity/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/cybersecurity/ontology.yaml:4` | `domains` | [list:2] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Asset.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:11` | `classes.Asset.description` | A protected infrastructure, application, or data asset in the security topology. |
| `config/domain-packs/cybersecurity/ontology.yaml:13` | `classes.Asset.properties.canonical_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:14` | `classes.Asset.properties.name` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:15` | `classes.Asset.properties.ip_address` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:16` | `classes.Asset.properties.criticality` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:17` | `classes.Asset.properties.resilience` | DOUBLE |
| `config/domain-packs/cybersecurity/ontology.yaml:18` | `classes.Asset.properties.status` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Asset.relationships.AFFECTED_BY.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.Asset.relationships.AFFECTED_BY.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.Asset.relationships.AFFECTED_BY.in` | [list:2] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Vulnerability.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:11` | `classes.Vulnerability.description` | A disclosed vulnerability affecting dependencies or services. |
| `config/domain-packs/cybersecurity/ontology.yaml:29` | `classes.Vulnerability.properties.cve_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:30` | `classes.Vulnerability.properties.cvss_score` | DOUBLE |
| `config/domain-packs/cybersecurity/ontology.yaml:31` | `classes.Vulnerability.properties.exploit_available` | BOOLEAN |
| `config/domain-packs/cybersecurity/ontology.yaml:32` | `classes.Vulnerability.properties.remediation_status` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:13` | `classes.Vulnerability.properties.canonical_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:14` | `classes.Vulnerability.properties.name` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:35` | `classes.Vulnerability.properties.severity` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Vulnerability.relationships.AFFECTS.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.Vulnerability.relationships.AFFECTS.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.Vulnerability.relationships.AFFECTS.in` | [list:3] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Vulnerability.relationships.IMPACTS.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.Vulnerability.relationships.IMPACTS.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.Vulnerability.relationships.IMPACTS.in` | [list:4] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Vulnerability.relationships.FIXED_BY.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.Vulnerability.relationships.FIXED_BY.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.Vulnerability.relationships.FIXED_BY.in` | [list:2] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Threat.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:11` | `classes.Threat.description` | A threat actor or campaign observed against assets. |
| `config/domain-packs/cybersecurity/ontology.yaml:54` | `classes.Threat.properties.threat_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:55` | `classes.Threat.properties.threat_type` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:13` | `classes.Threat.properties.canonical_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:14` | `classes.Threat.properties.name` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Threat.relationships.EXPLOITS.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.Threat.relationships.EXPLOITS.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.Threat.relationships.EXPLOITS.in` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.Threat.relationships.TARGETS.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.Threat.relationships.TARGETS.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.Threat.relationships.TARGETS.in` | [list:2] |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.SecurityFinding.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:11` | `classes.SecurityFinding.description` | A scanner or pentest finding with remediation tracking. |
| `config/domain-packs/cybersecurity/ontology.yaml:72` | `classes.SecurityFinding.properties.finding_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:73` | `classes.SecurityFinding.properties.scanner` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:74` | `classes.SecurityFinding.properties.first_seen` | DATE |
| `config/domain-packs/cybersecurity/ontology.yaml:13` | `classes.SecurityFinding.properties.canonical_id` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:14` | `classes.SecurityFinding.properties.name` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:35` | `classes.SecurityFinding.properties.severity` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.SecurityFinding.relationships.REMEDIATED_BY.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `classes.SecurityFinding.relationships.REMEDIATED_BY.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `classes.SecurityFinding.relationships.REMEDIATED_BY.in` | [list:2] |
| `config/domain-packs/cybersecurity/ontology.yaml:11` | `classes.File.description` | Extends core File with secrets and IaC posture flags. |
| `config/domain-packs/cybersecurity/ontology.yaml:10` | `classes.File.extends_core` | true |
| `config/domain-packs/cybersecurity/ontology.yaml:88` | `classes.File.properties.contains_secrets` | [secret value omitted] |
| `config/domain-packs/cybersecurity/ontology.yaml:89` | `classes.File.properties.iac_kind` | TEXT |
| `config/domain-packs/cybersecurity/ontology.yaml:91` | `validators` | [list:2] |
| `config/domain-packs/cybersecurity/ontology.yaml:22` | `relationships.AFFECTS.out` | [list:1] |
| `config/domain-packs/cybersecurity/ontology.yaml:23` | `relationships.AFFECTS.in` | [list:3] |
| `config/domain-packs/cybersecurity/pack.yaml:1` | `name` | cybersecurity |
| `config/domain-packs/cybersecurity/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/cybersecurity/pack.yaml:3` | `extends` | core |
| `config/domain-packs/cybersecurity/pack.yaml:4` | `description` | Cybersecurity pack: vulnerabilities, threats, security findings and asset exposure extending core CO... |
| `config/domain-packs/data-governance/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/data-governance/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/data-governance/ontology.yaml:4` | `domains` | [list:2] |
| `config/domain-packs/data-governance/ontology.yaml:10` | `classes.Dataset.description` | A governed logical dataset registered in the catalog. |
| `config/domain-packs/data-governance/ontology.yaml:12` | `classes.Dataset.properties.dataset_id` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:13` | `classes.Dataset.properties.schema_ref` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:14` | `classes.Dataset.properties.freshness_slo` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:15` | `classes.Dataset.properties.canonical_id` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:16` | `classes.Dataset.properties.name` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:17` | `classes.Dataset.properties.owner` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:20` | `classes.Dataset.relationships.HAS_LINEAGE.out` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:21` | `classes.Dataset.relationships.HAS_LINEAGE.in` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:20` | `classes.Dataset.relationships.STORED_IN.out` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:21` | `classes.Dataset.relationships.STORED_IN.in` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:10` | `classes.DataProduct.description` | A consumable data product built from governed datasets. |
| `config/domain-packs/data-governance/ontology.yaml:29` | `classes.DataProduct.properties.product_id` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:30` | `classes.DataProduct.properties.sla_tier` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:15` | `classes.DataProduct.properties.canonical_id` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:16` | `classes.DataProduct.properties.name` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:17` | `classes.DataProduct.properties.owner` | TEXT |
| `config/domain-packs/data-governance/ontology.yaml:20` | `classes.DataProduct.relationships.BUILT_FROM.out` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:21` | `classes.DataProduct.relationships.BUILT_FROM.in` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:20` | `classes.DataProduct.relationships.SERVES.out` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:21` | `classes.DataProduct.relationships.SERVES.in` | [list:2] |
| `config/domain-packs/data-governance/ontology.yaml:10` | `classes.KnowledgeProduct.description` | Extends core KnowledgeProduct with governance quality scores. |
| `config/domain-packs/data-governance/ontology.yaml:44` | `classes.KnowledgeProduct.extends_core` | true |
| `config/domain-packs/data-governance/ontology.yaml:46` | `classes.KnowledgeProduct.properties.governance_score` | DOUBLE |
| `config/domain-packs/data-governance/ontology.yaml:47` | `classes.KnowledgeProduct.properties.certified` | BOOLEAN |
| `config/domain-packs/data-governance/ontology.yaml:20` | `classes.KnowledgeProduct.relationships.DERIVED_FROM.out` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:21` | `classes.KnowledgeProduct.relationships.DERIVED_FROM.in` | [list:1] |
| `config/domain-packs/data-governance/ontology.yaml:53` | `validators` | [list:2] |
| `config/domain-packs/data-governance/pack.yaml:1` | `name` | data-governance |
| `config/domain-packs/data-governance/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/data-governance/pack.yaml:3` | `extends` | core |
| `config/domain-packs/data-governance/pack.yaml:4` | `description` | Data governance pack: datasets, data products and lineage relationships extending core KNOWLEDGE/MET... |
| `config/domain-packs/healthcare/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/healthcare/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/healthcare/ontology.yaml:4` | `domains` | [list:3] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Encounter.description` | A clinical encounter (visit, admission, telehealth session) linking patients (pseudonymous by defaul... |
| `config/domain-packs/healthcare/ontology.yaml:15` | `classes.Encounter.properties.encounter_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:16` | `classes.Encounter.properties.encounter_type` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:17` | `classes.Encounter.properties.patient_ref` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:18` | `classes.Encounter.properties.started_at` | DATE |
| `config/domain-packs/healthcare/ontology.yaml:19` | `classes.Encounter.properties.ended_at` | DATE |
| `config/domain-packs/healthcare/ontology.yaml:20` | `classes.Encounter.properties.status` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Encounter.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Encounter.relationships.OCCURRED_AT.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Encounter.relationships.OCCURRED_AT.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Encounter.relationships.GENERATED.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Encounter.relationships.GENERATED.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Order.description` | A clinical or pharmacy order (medication, lab, imaging). |
| `config/domain-packs/healthcare/ontology.yaml:33` | `classes.Order.properties.order_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:34` | `classes.Order.properties.order_type` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:35` | `classes.Order.properties.ordered_at` | DATE |
| `config/domain-packs/healthcare/ontology.yaml:20` | `classes.Order.properties.status` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Order.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Order.relationships.PRESCRIBES.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Order.relationships.PRESCRIBES.in` | [list:2] |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Order.relationships.FULFILLED_BY.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Order.relationships.FULFILLED_BY.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Drug.description` | A medication or pharmaceutical product. |
| `config/domain-packs/healthcare/ontology.yaml:49` | `classes.Drug.properties.drug_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:50` | `classes.Drug.properties.drug_code` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:51` | `classes.Drug.properties.form` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:52` | `classes.Drug.properties.strength` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:53` | `classes.Drug.properties.manufacturer` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Drug.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Drug.relationships.AVAILABLE_AS.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Drug.relationships.AVAILABLE_AS.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Lot.description` | A manufactured/recalled batch of a drug or consumable. |
| `config/domain-packs/healthcare/ontology.yaml:63` | `classes.Lot.properties.lot_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:64` | `classes.Lot.properties.lot_number` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:65` | `classes.Lot.properties.expiry_date` | DATE |
| `config/domain-packs/healthcare/ontology.yaml:66` | `classes.Lot.properties.recall_status` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Lot.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Lot.relationships.RECALL_AFFECTS.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Lot.relationships.RECALL_AFFECTS.in` | [list:3] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Device.description` | A medical device or equipment unit tracked in operations. |
| `config/domain-packs/healthcare/ontology.yaml:76` | `classes.Device.properties.device_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:77` | `classes.Device.properties.device_type` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:78` | `classes.Device.properties.model` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:79` | `classes.Device.properties.serial_number` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Device.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Device.relationships.DEPLOYED_AT.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Device.relationships.DEPLOYED_AT.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Protocol.description` | A clinical protocol or care pathway governing encounters. |
| `config/domain-packs/healthcare/ontology.yaml:89` | `classes.Protocol.properties.protocol_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:90` | `classes.Protocol.properties.protocol_name` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:91` | `classes.Protocol.properties.version` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:20` | `classes.Protocol.properties.status` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Protocol.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Protocol.relationships.GOVERNS.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Protocol.relationships.GOVERNS.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Protocol.relationships.RUNS_AT.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Protocol.relationships.RUNS_AT.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:11` | `classes.Site.description` | A care site, clinic, hospital or trial site. |
| `config/domain-packs/healthcare/ontology.yaml:105` | `classes.Site.properties.site_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:106` | `classes.Site.properties.site_type` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:107` | `classes.Site.properties.region` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:108` | `classes.Site.properties.canonical_id` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:109` | `classes.Site.properties.name` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:21` | `classes.Site.properties.source_system` | TEXT |
| `config/domain-packs/healthcare/ontology.yaml:24` | `classes.Site.relationships.OPERATES_UNDER.out` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:25` | `classes.Site.relationships.OPERATES_UNDER.in` | [list:1] |
| `config/domain-packs/healthcare/ontology.yaml:116` | `validators` | [list:3] |
| `config/domain-packs/healthcare/pack.yaml:1` | `name` | healthcare |
| `config/domain-packs/healthcare/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/healthcare/pack.yaml:3` | `extends` | core |
| `config/domain-packs/healthcare/pack.yaml:4` | `description` | Healthcare and life sciences pack: Encounter, Order, Drug, Lot, Device, Protocol and Site concepts (... |
| `config/domain-packs/itsm/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/itsm/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/itsm/ontology.yaml:4` | `domains` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:9` | `classes.Incident.description` | Extends core Incident with ITIL problem linkage. |
| `config/domain-packs/itsm/ontology.yaml:10` | `classes.Incident.extends_core` | true |
| `config/domain-packs/itsm/ontology.yaml:12` | `classes.Incident.properties.problem_ref` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:13` | `classes.Incident.properties.major_incident` | BOOLEAN |
| `config/domain-packs/itsm/ontology.yaml:16` | `classes.Incident.relationships.ESCALATES_TO.out` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:17` | `classes.Incident.relationships.ESCALATES_TO.in` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:16` | `classes.Incident.relationships.LINKED_TO_PROBLEM.out` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:17` | `classes.Incident.relationships.LINKED_TO_PROBLEM.in` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:9` | `classes.Problem.description` | An ITIL problem record grouping related incidents. |
| `config/domain-packs/itsm/ontology.yaml:25` | `classes.Problem.properties.problem_id` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:26` | `classes.Problem.properties.root_cause` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:27` | `classes.Problem.properties.canonical_id` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:28` | `classes.Problem.properties.name` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:29` | `classes.Problem.properties.status` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:30` | `classes.Problem.properties.source_system` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:16` | `classes.Problem.relationships.CAUSED_BY.out` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:17` | `classes.Problem.relationships.CAUSED_BY.in` | [list:2] |
| `config/domain-packs/itsm/ontology.yaml:9` | `classes.ConfigurationItem.description` | A CMDB configuration item linked to services and incidents. |
| `config/domain-packs/itsm/ontology.yaml:39` | `classes.ConfigurationItem.properties.ci_id` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:40` | `classes.ConfigurationItem.properties.ci_class` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:41` | `classes.ConfigurationItem.properties.environment` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:27` | `classes.ConfigurationItem.properties.canonical_id` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:28` | `classes.ConfigurationItem.properties.name` | TEXT |
| `config/domain-packs/itsm/ontology.yaml:16` | `classes.ConfigurationItem.relationships.IMPACTS.out` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:17` | `classes.ConfigurationItem.relationships.IMPACTS.in` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:16` | `classes.ConfigurationItem.relationships.RUNS_ON.out` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:17` | `classes.ConfigurationItem.relationships.RUNS_ON.in` | [list:1] |
| `config/domain-packs/itsm/ontology.yaml:52` | `validators` | [list:2] |
| `config/domain-packs/itsm/pack.yaml:1` | `name` | itsm |
| `config/domain-packs/itsm/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/itsm/pack.yaml:3` | `extends` | core |
| `config/domain-packs/itsm/pack.yaml:4` | `description` | IT service management pack: extends OPS core concepts (Incident, ChangeRequest, ServiceRequest) with... |
| `config/domain-packs/manufacturing/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/manufacturing/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/manufacturing/ontology.yaml:4` | `domains` | [list:3] |
| `config/domain-packs/manufacturing/ontology.yaml:11` | `classes.Part.description` | A manufactured or purchased part/component. |
| `config/domain-packs/manufacturing/ontology.yaml:13` | `classes.Part.properties.part_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:14` | `classes.Part.properties.part_number` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:15` | `classes.Part.properties.material` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:16` | `classes.Part.properties.canonical_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:17` | `classes.Part.properties.name` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:18` | `classes.Part.properties.source_system` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.Part.relationships.USED_IN.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.Part.relationships.USED_IN.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.Part.relationships.SUPPLIED_BY.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.Part.relationships.SUPPLIED_BY.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:11` | `classes.BOM.description` | A bill of materials version listing component parts. |
| `config/domain-packs/manufacturing/ontology.yaml:30` | `classes.BOM.properties.bom_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:31` | `classes.BOM.properties.bom_revision` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:16` | `classes.BOM.properties.canonical_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:17` | `classes.BOM.properties.name` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:18` | `classes.BOM.properties.source_system` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.BOM.relationships.ASSEMBLED_AT.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.BOM.relationships.ASSEMBLED_AT.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:11` | `classes.Supplier.description` | An external supplier of parts or materials. |
| `config/domain-packs/manufacturing/ontology.yaml:43` | `classes.Supplier.properties.supplier_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:44` | `classes.Supplier.properties.supplier_tier` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:45` | `classes.Supplier.properties.region` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:16` | `classes.Supplier.properties.canonical_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:17` | `classes.Supplier.properties.name` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:18` | `classes.Supplier.properties.source_system` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.Supplier.relationships.SUPPLIES.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.Supplier.relationships.SUPPLIES.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:11` | `classes.Plant.description` | A manufacturing plant or production facility. |
| `config/domain-packs/manufacturing/ontology.yaml:57` | `classes.Plant.properties.plant_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:58` | `classes.Plant.properties.plant_code` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:45` | `classes.Plant.properties.region` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:16` | `classes.Plant.properties.canonical_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:17` | `classes.Plant.properties.name` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:18` | `classes.Plant.properties.source_system` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.Plant.relationships.FABRICATES.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.Plant.relationships.FABRICATES.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:11` | `classes.WorkOrder.description` | A production work order executed on a plant line. |
| `config/domain-packs/manufacturing/ontology.yaml:71` | `classes.WorkOrder.properties.work_order_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:72` | `classes.WorkOrder.properties.wo_status` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:73` | `classes.WorkOrder.properties.planned_start` | DATE |
| `config/domain-packs/manufacturing/ontology.yaml:74` | `classes.WorkOrder.properties.planned_end` | DATE |
| `config/domain-packs/manufacturing/ontology.yaml:75` | `classes.WorkOrder.properties.quantity` | INT |
| `config/domain-packs/manufacturing/ontology.yaml:18` | `classes.WorkOrder.properties.source_system` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.WorkOrder.relationships.EXECUTES.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.WorkOrder.relationships.EXECUTES.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.WorkOrder.relationships.RAISED.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.WorkOrder.relationships.RAISED.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:11` | `classes.QualityEvent.description` | A nonconformance, defect or quality inspection event. |
| `config/domain-packs/manufacturing/ontology.yaml:88` | `classes.QualityEvent.properties.quality_event_id` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:89` | `classes.QualityEvent.properties.defect_code` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:90` | `classes.QualityEvent.properties.severity` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:91` | `classes.QualityEvent.properties.event_timestamp` | DATE |
| `config/domain-packs/manufacturing/ontology.yaml:92` | `classes.QualityEvent.properties.status` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:18` | `classes.QualityEvent.properties.source_system` | TEXT |
| `config/domain-packs/manufacturing/ontology.yaml:21` | `classes.QualityEvent.relationships.NONCONFORMING_PART.out` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:22` | `classes.QualityEvent.relationships.NONCONFORMING_PART.in` | [list:1] |
| `config/domain-packs/manufacturing/ontology.yaml:99` | `validators` | [list:3] |
| `config/domain-packs/manufacturing/pack.yaml:1` | `name` | manufacturing |
| `config/domain-packs/manufacturing/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/manufacturing/pack.yaml:3` | `extends` | core |
| `config/domain-packs/manufacturing/pack.yaml:4` | `description` | Manufacturing and supply chain pack: Part, BOM, Supplier, Plant, WorkOrder and QualityEvent concepts... |
| `config/domain-packs/software-engineering/ontology.yaml:1` | `ontology_version` | 0.4.0 |
| `config/domain-packs/software-engineering/ontology.yaml:2` | `schema_version` | 1.2 |
| `config/domain-packs/software-engineering/ontology.yaml:4` | `domains` | [list:3] |
| `config/domain-packs/software-engineering/ontology.yaml:11` | `classes.WorkItem.description` | Extends core WorkItem with agile estimation fields. |
| `config/domain-packs/software-engineering/ontology.yaml:12` | `classes.WorkItem.extends_core` | true |
| `config/domain-packs/software-engineering/ontology.yaml:14` | `classes.WorkItem.properties.story_points` | INT |
| `config/domain-packs/software-engineering/ontology.yaml:15` | `classes.WorkItem.properties.epic_link` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:18` | `classes.WorkItem.relationships.ESTIMATED_FOR.out` | [list:1] |
| `config/domain-packs/software-engineering/ontology.yaml:19` | `classes.WorkItem.relationships.ESTIMATED_FOR.in` | [list:1] |
| `config/domain-packs/software-engineering/ontology.yaml:11` | `classes.CodeReview.description` | A code-review cycle on a repository change. |
| `config/domain-packs/software-engineering/ontology.yaml:24` | `classes.CodeReview.properties.review_id` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:25` | `classes.CodeReview.properties.review_state` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:26` | `classes.CodeReview.properties.reviewer_count` | INT |
| `config/domain-packs/software-engineering/ontology.yaml:27` | `classes.CodeReview.properties.canonical_id` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:28` | `classes.CodeReview.properties.source_system` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:18` | `classes.CodeReview.relationships.REVIEWS.out` | [list:1] |
| `config/domain-packs/software-engineering/ontology.yaml:19` | `classes.CodeReview.relationships.REVIEWS.in` | [list:2] |
| `config/domain-packs/software-engineering/ontology.yaml:18` | `classes.CodeReview.relationships.RAISED_AGAINST.out` | [list:1] |
| `config/domain-packs/software-engineering/ontology.yaml:19` | `classes.CodeReview.relationships.RAISED_AGAINST.in` | [list:2] |
| `config/domain-packs/software-engineering/ontology.yaml:11` | `classes.ReleaseTrain.description` | A grouped, versioned release cut across repositories. |
| `config/domain-packs/software-engineering/ontology.yaml:40` | `classes.ReleaseTrain.properties.train_name` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:41` | `classes.ReleaseTrain.properties.release_date` | DATE |
| `config/domain-packs/software-engineering/ontology.yaml:27` | `classes.ReleaseTrain.properties.canonical_id` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:43` | `classes.ReleaseTrain.properties.name` | TEXT |
| `config/domain-packs/software-engineering/ontology.yaml:18` | `classes.ReleaseTrain.relationships.CARRIES.out` | [list:1] |
| `config/domain-packs/software-engineering/ontology.yaml:19` | `classes.ReleaseTrain.relationships.CARRIES.in` | [list:2] |
| `config/domain-packs/software-engineering/ontology.yaml:49` | `validators` | [list:2] |
| `config/domain-packs/software-engineering/pack.yaml:1` | `name` | software-engineering |
| `config/domain-packs/software-engineering/pack.yaml:2` | `version` | 1.0.0 |
| `config/domain-packs/software-engineering/pack.yaml:3` | `extends` | core |
| `config/domain-packs/software-engineering/pack.yaml:4` | `description` | Software engineering pack: extends WORK/CODE/CICD core concepts with agile estimation, code-review a... |
| `config/graph-store.yaml:11` | `primary` | hugegraph |
| `config/graph-store.yaml:15` | `connections.hugegraph.type` | hugegraph |
| `config/graph-store.yaml:16` | `connections.hugegraph.url` | http://hugegraph-server:8080 |
| `config/graph-store.yaml:17` | `connections.hugegraph.graph` | hugegraph |
| `config/graph-store.yaml:18` | `connections.hugegraph.username` | admin |
| `config/graph-store.yaml:19` | `connections.hugegraph.password` | [secret value omitted] |
| `config/graph-store.yaml:15` | `connections.neptune.type` | neptune |
| `config/graph-store.yaml:16` | `connections.neptune.url` | https://your-neptune-endpoint:8182 |
| `config/graph-store.yaml:24` | `connections.neptune.database` | neptune |
| `config/graph-store.yaml:25` | `connections.neptune.open_cypher_path` | /openCypher |
| `config/graph-store.yaml:26` | `connections.neptune.sparql_path` | /sparql |
| `config/graph-store.yaml:27` | `connections.neptune.gremlin_path` | /gremlin |
| `config/graph-store.yaml:28` | `connections.neptune.verify_tls` | true |
| `config/graph-store.yaml:15` | `connections.neo4j.type` | neo4j |
| `config/graph-store.yaml:16` | `connections.neo4j.url` | http://neo4j:7474 |
| `config/graph-store.yaml:24` | `connections.neo4j.database` | neo4j |
| `config/graph-store.yaml:18` | `connections.neo4j.username` | neo4j |
| `config/graph-store.yaml:19` | `connections.neo4j.password` | [secret value omitted] |
| `config/graph-store.yaml:28` | `connections.neo4j.verify_tls` | true |
| `config/graph-store.yaml:15` | `connections.memory.type` | memory |
| `config/mappings/gitlab-mvp.yaml:1` | `version` | 1.0 |
| `config/mappings/gitlab-mvp.yaml:2` | `mapper_version` | gitlab-json/1.0 |
| `config/mappings/gitlab-mvp.yaml:3` | `issue_key_pattern` | [A-Z][A-Z0-9]+-\d+ |
| `config/mappings/jira-mvp.yaml:1` | `version` | 1.0 |
| `config/mappings/jira-mvp.yaml:2` | `mapper_version` | jira-json/1.0 |
| `config/mappings/jira-mvp.yaml:4` | `fields.issue_key` | key |
| `config/mappings/jira-mvp.yaml:5` | `fields.summary` | fields.summary |
| `config/mappings/jira-mvp.yaml:6` | `fields.description` | fields.description |
| `config/mappings/jira-mvp.yaml:7` | `fields.issue_type` | fields.issuetype.name |
| `config/mappings/jira-mvp.yaml:8` | `fields.status` | fields.status.name |
| `config/mappings/jira-mvp.yaml:9` | `fields.project_key` | fields.project.key |
| `config/mappings/jira-mvp.yaml:10` | `fields.project_name` | fields.project.name |
| `config/mappings/jira-mvp.yaml:11` | `fields.assignee_id` | fields.assignee.accountId |
| `config/mappings/jira-mvp.yaml:12` | `fields.assignee_name` | fields.assignee.displayName |
| `config/mappings/jira-mvp.yaml:13` | `fields.assignee_email` | fields.assignee.emailAddress |
| `config/mappings/jira-mvp.yaml:14` | `fields.parent_key` | fields.parent.key |
| `config/memory-policy.yaml:1` | `schema_version` | 1.0 |
| `config/memory-policy.yaml:2` | `ttl_seconds` | 2592000 |
| `config/memory-policy.yaml:3` | `max_records` | 1000 |
| `config/memory-policy.yaml:4` | `max_bytes` | 8388608 |
| `config/ontology/ontology-v0.2.0.yaml:1` | `ontology_version` | 0.2.0 |
| `config/ontology/ontology-v0.2.0.yaml:2` | `schema_version` | 1.0 |
| `config/ontology/ontology-v0.2.0.yaml:4` | `domains` | [list:7] |
| `config/ontology/ontology-v0.2.0.yaml:13` | `vertex_labels` | [list:22] |
| `config/ontology/ontology-v0.2.0.yaml:37` | `edge_labels` | [list:20] |
| `config/query-policies/default.yaml:1` | `policy_name` | default |
| `config/query-policies/default.yaml:2` | `description` | Default query policy for MVP. Enforces read-only queries with bounded depth, result limits, and time... |
| `config/query-policies/default.yaml:6` | `max_depth` | 8 |
| `config/query-policies/default.yaml:7` | `max_results` | 500 |
| `config/query-policies/default.yaml:8` | `max_timeout_ms` | 30000 |
| `config/query-policies/default.yaml:9` | `read_only` | true |
| `config/query-policies/default.yaml:11` | `allowed_intents` | [list:6] |
| `config/query-policies/default.yaml:19` | `blocked_edges` | [list:0] |
| `config/systems-registry.json:2` | `$schema` | urn:eoip:systems-registry:v1 |
| `config/systems-registry.json:3` | `version` | 1.0.0 |
| `config/systems-registry.json:4` | `description` | EOIP Unified Systems Registry — single configuration point for all connected enterprise systems. Eac... |
| `config/systems-registry.json:6` | `global_defaults.poll_interval_minutes` | 60 |
| `config/systems-registry.json:8` | `global_defaults.retry_policy.max_retries` | 3 |
| `config/systems-registry.json:9` | `global_defaults.retry_policy.backoff_seconds` | 30 |
| `config/systems-registry.json:10` | `global_defaults.retry_policy.backoff_multiplier` | 2.0 |
| `config/systems-registry.json:13` | `global_defaults.ingestion.batch_size` | 500 |
| `config/systems-registry.json:14` | `global_defaults.ingestion.dead_letter_queue_enabled` | true |
| `config/systems-registry.json:15` | `global_defaults.ingestion.schema_drift_detection` | true |
| `config/systems-registry.json:16` | `global_defaults.ingestion.auto_schema_induction` | true |
| `config/systems-registry.json:17` | `global_defaults.ingestion.auto_relationship_discovery` | true |
| `config/systems-registry.json:20` | `global_defaults.data_quality.deduplication_enabled` | true |
| `config/systems-registry.json:21` | `global_defaults.data_quality.identity_resolution` | true |
| `config/systems-registry.json:22` | `global_defaults.data_quality.provenance_tracking` | true |
| `config/systems-registry.json:25` | `global_defaults.security.encrypt_secrets_at_rest` | [secret value omitted] |
| `config/systems-registry.json:26` | `global_defaults.security.tls_required` | false |
| `config/systems-registry.json:27` | `global_defaults.security.audit_logging` | true |
| `config/systems-registry.json:30` | `systems` | [list:0] |
| `deploy/helm/eoip/values.yaml:5` | `image.registry` |  |
| `deploy/helm/eoip/values.yaml:6` | `image.repository` | eoip-app |
| `deploy/helm/eoip/values.yaml:7` | `image.tag` | local |
| `deploy/helm/eoip/values.yaml:8` | `image.pullPolicy` | IfNotPresent |
| `deploy/helm/eoip/values.yaml:10` | `imagePullSecrets` | [secret value omitted] |
| `deploy/helm/eoip/values.yaml:12` | `nameOverride` |  |
| `deploy/helm/eoip/values.yaml:13` | `fullnameOverride` |  |
| `deploy/helm/eoip/values.yaml:16` | `serviceAccount.create` | false |
| `deploy/helm/eoip/values.yaml:17` | `serviceAccount.name` |  |
| `deploy/helm/eoip/values.yaml:23` | `api.replicaCount` | 2 |
| `deploy/helm/eoip/values.yaml:24` | `api.port` | 8000 |
| `deploy/helm/eoip/values.yaml:1` | `api.resources.requests.cpu` | 250m |
| `deploy/helm/eoip/values.yaml:1` | `api.resources.requests.memory` | 512Mi |
| `deploy/helm/eoip/values.yaml:1` | `api.resources.limits.cpu` | 1 |
| `deploy/helm/eoip/values.yaml:1` | `api.resources.limits.memory` | 1Gi |
| `deploy/helm/eoip/values.yaml:30` | `api.tolerations` | [list:0] |
| `deploy/helm/eoip/values.yaml:34` | `api.podAntiAffinity.enabled` | true |
| `deploy/helm/eoip/values.yaml:35` | `api.podAntiAffinity.topologyKey` | kubernetes.io/hostname |
| `deploy/helm/eoip/values.yaml:34` | `mcp.enabled` | true |
| `deploy/helm/eoip/values.yaml:23` | `mcp.replicaCount` | 1 |
| `deploy/helm/eoip/values.yaml:24` | `mcp.port` | 8001 |
| `deploy/helm/eoip/values.yaml:1` | `mcp.resources.requests.cpu` | 100m |
| `deploy/helm/eoip/values.yaml:1` | `mcp.resources.requests.memory` | 256Mi |
| `deploy/helm/eoip/values.yaml:1` | `mcp.resources.limits.cpu` | 500m |
| `deploy/helm/eoip/values.yaml:1` | `mcp.resources.limits.memory` | 512Mi |
| `deploy/helm/eoip/values.yaml:34` | `mcp.podAntiAffinity.enabled` | false |
| `deploy/helm/eoip/values.yaml:35` | `mcp.podAntiAffinity.topologyKey` | kubernetes.io/hostname |
| `deploy/helm/eoip/values.yaml:34` | `worker.enabled` | true |
| `deploy/helm/eoip/values.yaml:23` | `worker.replicaCount` | 2 |
| `deploy/helm/eoip/values.yaml:54` | `worker.lease.path` | /data/leases/worker.lock |
| `deploy/helm/eoip/values.yaml:55` | `worker.lease.ttlSeconds` | 30 |
| `deploy/helm/eoip/values.yaml:1` | `worker.resources.requests.cpu` | 250m |
| `deploy/helm/eoip/values.yaml:1` | `worker.resources.requests.memory` | 512Mi |
| `deploy/helm/eoip/values.yaml:1` | `worker.resources.limits.cpu` | 1 |
| `deploy/helm/eoip/values.yaml:1` | `worker.resources.limits.memory` | 1Gi |
| `deploy/helm/eoip/values.yaml:34` | `worker.podAntiAffinity.enabled` | true |
| `deploy/helm/eoip/values.yaml:35` | `worker.podAntiAffinity.topologyKey` | kubernetes.io/hostname |
| `deploy/helm/eoip/values.yaml:34` | `persistence.enabled` | true |
| `deploy/helm/eoip/values.yaml:66` | `persistence.storageClass` |  |
| `deploy/helm/eoip/values.yaml:67` | `persistence.accessMode` | ReadWriteMany |
| `deploy/helm/eoip/values.yaml:68` | `persistence.size` | 10Gi |
| `deploy/helm/eoip/values.yaml:74` | `config.dataDir` | /data |
| `deploy/helm/eoip/values.yaml:75` | `config.loadDemo` | true |
| `deploy/helm/eoip/values.yaml:76` | `config.apiToken` | [secret value omitted] |
| `deploy/helm/eoip/values.yaml:77` | `config.existingSecret` | [secret value omitted] |
| `deploy/helm/eoip/values.yaml:78` | `config.extraEnv` | [list:0] |
| `deploy/helm/eoip/values.yaml:34` | `hugegraph.enabled` | true |
| `deploy/helm/eoip/values.yaml:87` | `hugegraph.url` | http://hugegraph-server:8080 |
| `deploy/helm/eoip/values.yaml:88` | `hugegraph.graph` | hugegraph |
| `deploy/helm/eoip/values.yaml:89` | `hugegraph.username` | admin |
| `deploy/helm/eoip/values.yaml:90` | `hugegraph.password` | [secret value omitted] |
| `deploy/helm/eoip/values.yaml:34` | `neptune.enabled` | false |
| `deploy/helm/eoip/values.yaml:87` | `neptune.url` | https://your-neptune-endpoint:8182 |
| `deploy/helm/eoip/values.yaml:97` | `neptune.database` | neptune |
| `deploy/helm/eoip/values.yaml:98` | `neptune.verifyTls` | true |
| `deploy/helm/eoip/values.yaml:34` | `ollama.enabled` | false |
| `deploy/helm/eoip/values.yaml:87` | `ollama.url` | http://ollama:11434 |
| `deploy/helm/eoip/values.yaml:104` | `ollama.model` |  |
| `deploy/helm/eoip/values.yaml:77` | `ollama.existingSecret` | [secret value omitted] |
| `deploy/helm/eoip/values.yaml:107` | `graphBackend` | hugegraph |
| `deploy/helm/eoip/values.yaml:34` | `redis.enabled` | false |
| `deploy/helm/eoip/values.yaml:87` | `redis.url` | redis://eoip-redis:6379/0 |
| `deploy/helm/eoip/values.yaml:4` | `redis.image` | redis:8.2-alpine |
| `deploy/helm/eoip/values.yaml:123` | `service.type` | ClusterIP |
| `deploy/helm/eoip/values.yaml:24` | `service.port` | 8000 |
| `deploy/helm/eoip/values.yaml:34` | `ingress.enabled` | false |
| `deploy/helm/eoip/values.yaml:128` | `ingress.className` | nginx |
| `deploy/helm/eoip/values.yaml:130` | `ingress.hosts` | [list:1] |
| `deploy/helm/eoip/values.yaml:135` | `ingress.tls` | [list:0] |
| `deploy/helm/eoip/values.yaml:34` | `hpa.enabled` | true |
| `deploy/helm/eoip/values.yaml:142` | `hpa.minReplicas` | 2 |
| `deploy/helm/eoip/values.yaml:143` | `hpa.maxReplicas` | 8 |
| `deploy/helm/eoip/values.yaml:144` | `hpa.targetCPUUtilizationPercentage` | 70 |
| `deploy/helm/eoip/values.yaml:145` | `hpa.targetMemoryUtilizationPercentage` | 80 |
| `deploy/helm/eoip/values.yaml:148` | `podSecurityContext.runAsNonRoot` | true |
| `deploy/helm/eoip/values.yaml:149` | `podSecurityContext.runAsUser` | 10001 |
| `deploy/helm/eoip/values.yaml:150` | `podSecurityContext.runAsGroup` | 10001 |
| `deploy/helm/eoip/values.yaml:151` | `podSecurityContext.fsGroup` | 10001 |
| `deploy/helm/eoip/values.yaml:154` | `securityContext.allowPrivilegeEscalation` | false |
| `deploy/helm/eoip/values.yaml:1` | `securityContext.capabilities.drop` | [list:1] |
| `pyproject.toml:2` | `build-system.requires` | [list:1] |
| `pyproject.toml:3` | `build-system.build-backend` | setuptools.build_meta |
| `pyproject.toml:6` | `project.name` | eoip |
| `pyproject.toml:7` | `project.version` | 1.0.0rc1 |
| `pyproject.toml:8` | `project.description` | Enterprise Ontology & Intelligence Platform (EOIP) — Phase 1 MVP vertical slice |
| `pyproject.toml:9` | `project.requires-python` | >=3.11 |
| `pyproject.toml:10` | `project.dependencies` | [list:9] |
| `pyproject.toml:23` | `project.scripts.eoip` | eoip.cli:main |
| `pyproject.toml:26` | `project.optional-dependencies.fileparse` | [list:10] |
| `pyproject.toml:38` | `project.optional-dependencies.codeparse` | [list:2] |
| `pyproject.toml:42` | `project.optional-dependencies.otel` | [list:3] |
| `pyproject.toml:47` | `project.optional-dependencies.k8s` | [list:1] |
| `pyproject.toml:50` | `project.optional-dependencies.redis` | [list:1] |
| `pyproject.toml:53` | `project.optional-dependencies.enterprise` | [list:5] |
| `pyproject.toml:60` | `project.optional-dependencies.dev` | [list:6] |
| `pyproject.toml:70` | `tool.setuptools.package-dir.` | packages |
| `pyproject.toml:73` | `tool.setuptools.packages.find.where` | [list:1] |
| `pyproject.toml:74` | `tool.setuptools.packages.find.include` | [list:1] |
| `pyproject.toml:77` | `tool.pytest.ini_options.pythonpath` | [list:2] |
| `pyproject.toml:78` | `tool.pytest.ini_options.asyncio_mode` | auto |
| `pyproject.toml:79` | `tool.pytest.ini_options.testpaths` | [list:1] |
| `pyproject.toml:80` | `tool.pytest.ini_options.addopts` | -q --strict-markers --tb=short |
| `pyproject.toml:81` | `tool.pytest.ini_options.markers` | [list:8] |
| `pyproject.toml:91` | `tool.pytest.ini_options.filterwarnings` | [list:1] |
| `pyproject.toml:96` | `tool.coverage.run.source` | [list:1] |
| `pyproject.toml:97` | `tool.coverage.run.omit` | [list:2] |
| `pyproject.toml:100` | `tool.coverage.report.show_missing` | true |
| `pyproject.toml:101` | `tool.coverage.report.fail_under` | 70 |
| `pyproject.toml:102` | `tool.coverage.report.exclude_lines` | [list:4] |
| `pyproject.toml:110` | `tool.mypy.python_version` | 3.11 |
| `pyproject.toml:111` | `tool.mypy.warn_return_any` | true |
| `pyproject.toml:112` | `tool.mypy.warn_unused_configs` | true |
| `pyproject.toml:113` | `tool.mypy.disallow_untyped_defs` | false |
| `pyproject.toml:114` | `tool.mypy.check_untyped_defs` | true |
| `pyproject.toml:115` | `tool.mypy.ignore_missing_imports` | true |
| `pyproject.toml:118` | `tool.ruff.line-length` | 110 |
| `pyproject.toml:119` | `tool.ruff.target-version` | py311 |
| `pyrightconfig.json:2` | `include` | [list:2] |
| `pyrightconfig.json:6` | `exclude` | [list:3] |
| `pyrightconfig.json:11` | `extraPaths` | [list:1] |
| `pyrightconfig.json:14` | `typeCheckingMode` | basic |

## Exclusion Policy

- `demo/**`, demo/sample data and example artifacts: user-directed exclusion from findings; inventoried below.
- Runtime outputs, caches, screenshots, coverage, generated audit JSON and compiled/binary artifacts: not source of product requirements; inventoried below.
- Lockfiles: byte-counted and dependency audit executed, but not line-by-line requirement sources.
- Binary Office/PDF/image/archive/checksum assets: metadata/inventory only because they are not safely decoded source text.
- Existing frontend source was read only for backend contract/security evidence and was not used as design input.

## File-By-File Ledger

| Path | Type | Lines | Read status | Requirement/integration IDs found | Reason/receipt |
|---|---|---:|---|---|---|
| `.containerignore` | `[none]` | 25 | `FULLY_READ` | - | Complete text read and indexed |
| `.dockerignore` | `[none]` | 25 | `FULLY_READ` | - | Complete text read and indexed |
| `.github/workflows/ci.yml` | `.yml` | 56 | `FULLY_READ` | - | Complete text read and indexed |
| `.github/workflows/validation-evidence.yml` | `.yml` | 82 | `FULLY_READ` | GAP-KGCI-001, KGR-G-011 | Complete text read and indexed |
| `.gitignore` | `[none]` | 92 | `FULLY_READ` | - | Complete text read and indexed |
| `.tmp/autodemo-full-check/raw/FRD/jira/02261e11c4f10170546a32a6ef3b2bad83e65ff1e12f57565f905731836645b7.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/06640d79f001fb80e86d7f7a40ae03b0c4daa2fdd97ff0b5b5ed108eb543f5f9.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/179d79ad5551c5216642b31bb8032729a55003e07a7e4a6c48a8b419e36c41d6.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/2d55a168adc84a5ac727d32eaadfc098acb4a8d17a80c47dbc5bfc2cb9ad7937.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/414ffac40e9e13fcfad3d0be00c61c9bda2fc829a5605a75b3cd65981deeddbc.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/4baeed26114d142528d6afc995817eb37e486534ce6af44f62932b14b6d05a25.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/661e3d8d600adede5ccfa78407b864be06dae17fd8488521d35b5766c14486dd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/6ba1088eecfd9dfb932022bf73365399686228aabfdb0aac2408d46401994d6f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/718cb98c4fee5665640d616e70681405fba01bf8e9618908301f5c438704d14c.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/7ea0cb949d27ef2d352e364f66d2c195fd26317dd4dd36485dfb3c6a0e729e78.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/92d9dabd023ddee01cf7040fafba6e3148c2142a1362571d2b595127c7be09cd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/9e9eac56afb6ebd5ee1983b83611d89e11cba6e0b56227bef5feeb98a22ee371.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/bfca43bdef9b6dfb6c6b94f2d5d523c9fbb721a3925dcdf5f441e979f0b80968.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/c74759deac0d93ca4da7abbadcb467cc50df14fbad16651db65a1aa71af51a97.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/c912e6a041240320fed38d70f4f067f4ad3b502d8e3443586dbab90d6c2ea8ef.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/e5870011f15fa3cfd8bc9887410bcf0d14966165ecb4dd05000214e85a7d5a7f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/edac9ed7d5f66d88d1b16394a1b19de5903e18b2d75a4d4a2ff9d08c78d88edd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/FRD/jira/f74da36d3e0dfec1fe1400506ba36f2516041cf2ad050beddeca0c2b33846dd4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/009eee60ad58a1c60749bb9e36ea7a09ad31f191bb45d9302b26c7e1558134b4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/0edca096be95696cce8457d102540f0e58b415c19cbcdb3f960b53fbd6600be6.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/25194f19a9882950e5dccee4bb06f660b3958c6d5bc47b3b2db9e2bf20a2b4db.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/2799468994d0add861a025dcb19118be001615d1ee247dabaf252b403be41c18.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/38b64383fc9dcf7b7348fb5577c6b4ba45b0698486040b5c4f00841979407a27.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/56e7665987a09fe955087076411a8d6fa65d26f67a83cde805907d159d4d4c7a.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/6e4407ec1725622b33c1004477d8d0c97b8c32930adc9ed1eaf9a2032b446b47.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/783d7e0c876aefd8d35998abbfd54566d0d315db9d1b62f11ce3957fcc720ddd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/8109d6ef8b6ce6324ed155a7d7e24c84c414b329a58181bb80e2062a8e5430b8.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/8e1293cbcdd2b6f296a4b6d9cd5c985ffef6eb55e05369f44ac442eac75e58f7.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/9151a32c8a04801fc5720a2ec79e7a379cf011e87c8ae1325f5bf55fec1678ac.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/b24233007cbb43d71da6e7b6c6d5915c2ffc2d7df48092863768e2002e52b022.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/bb00913ccac1a57f3cab104b2cd2151342e6b01df2d082a4d629e70c6f472aa0.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/bb607188b8bb5666a99e9ac012a3be686c9693173a8a15621efe096c3008c41f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/c7144120c8ef47ae47736ae51ea08cad421462a43fb150ef3e9121b4e68a247a.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/e72bbde4ea33d8c6ece8664469e69362ff57b29b6d37f6149dd432dd1ffadd55.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/f878ce0457f56f3f768dd208005b8d5aba43c3a0d9fe783f6fbbe16ccd3dfbab.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-full-check/raw/PAY/jira/fd8865bd39e669e7a62bda864a4abe5f06dab3079922395d7704ede34ce5caa4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/009eee60ad58a1c60749bb9e36ea7a09ad31f191bb45d9302b26c7e1558134b4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/0edca096be95696cce8457d102540f0e58b415c19cbcdb3f960b53fbd6600be6.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/25194f19a9882950e5dccee4bb06f660b3958c6d5bc47b3b2db9e2bf20a2b4db.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/2799468994d0add861a025dcb19118be001615d1ee247dabaf252b403be41c18.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/38b64383fc9dcf7b7348fb5577c6b4ba45b0698486040b5c4f00841979407a27.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/56e7665987a09fe955087076411a8d6fa65d26f67a83cde805907d159d4d4c7a.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/6e4407ec1725622b33c1004477d8d0c97b8c32930adc9ed1eaf9a2032b446b47.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/783d7e0c876aefd8d35998abbfd54566d0d315db9d1b62f11ce3957fcc720ddd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/8109d6ef8b6ce6324ed155a7d7e24c84c414b329a58181bb80e2062a8e5430b8.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/8e1293cbcdd2b6f296a4b6d9cd5c985ffef6eb55e05369f44ac442eac75e58f7.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/9151a32c8a04801fc5720a2ec79e7a379cf011e87c8ae1325f5bf55fec1678ac.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/b24233007cbb43d71da6e7b6c6d5915c2ffc2d7df48092863768e2002e52b022.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/bb00913ccac1a57f3cab104b2cd2151342e6b01df2d082a4d629e70c6f472aa0.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/bb607188b8bb5666a99e9ac012a3be686c9693173a8a15621efe096c3008c41f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/c7144120c8ef47ae47736ae51ea08cad421462a43fb150ef3e9121b4e68a247a.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/e72bbde4ea33d8c6ece8664469e69362ff57b29b6d37f6149dd432dd1ffadd55.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/f878ce0457f56f3f768dd208005b8d5aba43c3a0d9fe783f6fbbe16ccd3dfbab.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/raw/PAY/jira/fd8865bd39e669e7a62bda864a4abe5f06dab3079922395d7704ede34ce5caa4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/autodemo-launch-check-3c2f6eae2875405899d326dd6dfa8963/results.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/02261e11c4f10170546a32a6ef3b2bad83e65ff1e12f57565f905731836645b7.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/06640d79f001fb80e86d7f7a40ae03b0c4daa2fdd97ff0b5b5ed108eb543f5f9.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/179d79ad5551c5216642b31bb8032729a55003e07a7e4a6c48a8b419e36c41d6.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/2d55a168adc84a5ac727d32eaadfc098acb4a8d17a80c47dbc5bfc2cb9ad7937.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/414ffac40e9e13fcfad3d0be00c61c9bda2fc829a5605a75b3cd65981deeddbc.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/4baeed26114d142528d6afc995817eb37e486534ce6af44f62932b14b6d05a25.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/661e3d8d600adede5ccfa78407b864be06dae17fd8488521d35b5766c14486dd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/6ba1088eecfd9dfb932022bf73365399686228aabfdb0aac2408d46401994d6f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/718cb98c4fee5665640d616e70681405fba01bf8e9618908301f5c438704d14c.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/7ea0cb949d27ef2d352e364f66d2c195fd26317dd4dd36485dfb3c6a0e729e78.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/92d9dabd023ddee01cf7040fafba6e3148c2142a1362571d2b595127c7be09cd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/9e9eac56afb6ebd5ee1983b83611d89e11cba6e0b56227bef5feeb98a22ee371.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/bfca43bdef9b6dfb6c6b94f2d5d523c9fbb721a3925dcdf5f441e979f0b80968.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/c74759deac0d93ca4da7abbadcb467cc50df14fbad16651db65a1aa71af51a97.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/c912e6a041240320fed38d70f4f067f4ad3b502d8e3443586dbab90d6c2ea8ef.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/e5870011f15fa3cfd8bc9887410bcf0d14966165ecb4dd05000214e85a7d5a7f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/edac9ed7d5f66d88d1b16394a1b19de5903e18b2d75a4d4a2ff9d08c78d88edd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/FRD/jira/f74da36d3e0dfec1fe1400506ba36f2516041cf2ad050beddeca0c2b33846dd4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/009eee60ad58a1c60749bb9e36ea7a09ad31f191bb45d9302b26c7e1558134b4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/0edca096be95696cce8457d102540f0e58b415c19cbcdb3f960b53fbd6600be6.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/25194f19a9882950e5dccee4bb06f660b3958c6d5bc47b3b2db9e2bf20a2b4db.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/2799468994d0add861a025dcb19118be001615d1ee247dabaf252b403be41c18.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/38b64383fc9dcf7b7348fb5577c6b4ba45b0698486040b5c4f00841979407a27.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/56e7665987a09fe955087076411a8d6fa65d26f67a83cde805907d159d4d4c7a.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/6e4407ec1725622b33c1004477d8d0c97b8c32930adc9ed1eaf9a2032b446b47.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/783d7e0c876aefd8d35998abbfd54566d0d315db9d1b62f11ce3957fcc720ddd.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/8109d6ef8b6ce6324ed155a7d7e24c84c414b329a58181bb80e2062a8e5430b8.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/8e1293cbcdd2b6f296a4b6d9cd5c985ffef6eb55e05369f44ac442eac75e58f7.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/9151a32c8a04801fc5720a2ec79e7a379cf011e87c8ae1325f5bf55fec1678ac.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/b24233007cbb43d71da6e7b6c6d5915c2ffc2d7df48092863768e2002e52b022.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/bb00913ccac1a57f3cab104b2cd2151342e6b01df2d082a4d629e70c6f472aa0.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/bb607188b8bb5666a99e9ac012a3be686c9693173a8a15621efe096c3008c41f.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/c7144120c8ef47ae47736ae51ea08cad421462a43fb150ef3e9121b4e68a247a.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/e72bbde4ea33d8c6ece8664469e69362ff57b29b6d37f6149dd432dd1ffadd55.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/f878ce0457f56f3f768dd208005b8d5aba43c3a0d9fe783f6fbbe16ccd3dfbab.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/demo-guided-validation/raw/PAY/jira/fd8865bd39e669e7a62bda864a4abe5f06dab3079922395d7704ede34ce5caa4.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/full-pytest.xml` | `.xml` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/g2-coverage-audit.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/g2-test.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/g2-verify-current.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/gap-coverage-audit.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/gap-test.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/gap-verify-current.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/gen_sr_table.py` | `.py` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/generate_reconstruction_docs.py` | `.py` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/insert_pass9.py` | `.py` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/kgci/ontology-artifacts/ontology-0.4.0.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/kgci/report.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/presentation-build/package.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/spotcheck.py` | `.py` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/spotcheck2.py` | `.py` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/sr_ids.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/sr_table.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `.tmp/sr_texts.json` | `.json` | 0 | `EXCLUDED` | - | generated runtime, test, or prior audit artifact |
| `apps/api/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/api/app.py` | `.py` | 1684 | `FULLY_READ` | G2-P10, G2-P6, G2-P7, G2-P9, GAP-FRESH-001, GAP-REC-001 | Complete text read and indexed |
| `apps/api/extended.py` | `.py` | 1510 | `FULLY_READ` | GAP-DP-005, GAP-FABRIC-001, GAP-FABRIC-002, GAP-GITOPS-002, GAP-GOV-003, GAP-GRAPHTEST-001, GAP-GRAPHTEST-004, GAP-KGCI-... | Complete text read and indexed |
| `apps/api/main.py` | `.py` | 1514 | `FULLY_READ` | G2-CAP-001, GAP-ER-005, GAP-GITOPS-003 | Complete text read and indexed |
| `apps/mcp/main.py` | `.py` | 228 | `FULLY_READ` | FR-MCP-001, FR-MCP-002 | Complete text read and indexed |
| `apps/vscode-extension/.dockerignore` | `[none]` | 3 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/.vscodeignore` | `[none]` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/demo/index.js` | `.js` | 271 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/Dockerfile` | `[none]` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/extension.js` | `.js` | 792 | `FULLY_READ` | FR-VSCODE-001 | Complete text read and indexed |
| `apps/vscode-extension/mcp-client.js` | `.js` | 64 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/package-lock.json` | `.json` | 0 | `EXCLUDED` | - | generated dependency lockfile |
| `apps/vscode-extension/package.json` | `.json` | 131 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/README.md` | `.md` | 109 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/demo-driver.test.js` | `.js` | 53 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/mcp-client.test.js` | `.js` | 63 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/runTest.js` | `.js` | 62 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/suite/commands.js` | `.js` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/suite/index.js` | `.js` | 279 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/suite/refusals.js` | `.js` | 26 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/vscode-extension/test/suite/symbols.js` | `.js` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/.dockerignore` | `[none]` | 4 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/Containerfile` | `[none]` | 12 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/Dockerfile` | `[none]` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/Dockerfile.tests` | `.tests` | 0 | `EXCLUDED` | - | unsupported or binary file type |
| `apps/web/index.html` | `.html` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/nginx.conf` | `.conf` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/package-lock.json` | `.json` | 0 | `EXCLUDED` | - | generated dependency lockfile |
| `apps/web/package.json` | `.json` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/playwright.config.js` | `.js` | 20 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/admin/AdminDashboard.jsx` | `.jsx` | 148 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/admin/CheckpointAndRecoveryPanel.jsx` | `.jsx` | 185 | `FULLY_READ` | G2-ADMIN-004, G2-ADMIN-005 | Complete text read and indexed |
| `apps/web/src/admin/ConnectorSetupWizard.jsx` | `.jsx` | 185 | `FULLY_READ` | FR-ADMIN-001, G2-ADMIN-002 | Complete text read and indexed |
| `apps/web/src/admin/CrawlSafetyAndTelemetryPanel.jsx` | `.jsx` | 164 | `FULLY_READ` | CORE-104, G2-ADMIN-011, G2-ADMIN-012, G2-ADMIN-013 | Complete text read and indexed |
| `apps/web/src/admin/GraphTimelineAndJournalPanel.jsx` | `.jsx` | 186 | `FULLY_READ` | G2-ADMIN-008, G2-ADMIN-009, G2-ADMIN-010 | Complete text read and indexed |
| `apps/web/src/admin/index.jsx` | `.jsx` | 80 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, G2-ADMIN-001, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, G2-ADMIN... | Complete text read and indexed |
| `apps/web/src/admin/IngestionReconciliationPanel.jsx` | `.jsx` | 120 | `FULLY_READ` | FR-ADMIN-001, G2-ADMIN-003 | Complete text read and indexed |
| `apps/web/src/admin/KnowledgeGovernanceAndSLOPanel.jsx` | `.jsx` | 226 | `FULLY_READ` | FR-ADMIN-002, G2-ADMIN-014, G2-ADMIN-015, G2-ADMIN-016, G2-ADMIN-017 | Complete text read and indexed |
| `apps/web/src/admin/RbacPolicyEditor.jsx` | `.jsx` | 136 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/admin/SchemaDriftAndFreshnessPanel.jsx` | `.jsx` | 144 | `FULLY_READ` | G2-ADMIN-006, G2-ADMIN-007 | Complete text read and indexed |
| `apps/web/src/admin/SecurityGovernanceDashboard.jsx` | `.jsx` | 261 | `FULLY_READ` | GAP-SEC-008, GAP-SEC-009, GAP-SEC-012 | Complete text read and indexed |
| `apps/web/src/admin/UserManagement.jsx` | `.jsx` | 104 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/App.jsx` | `.jsx` | 1056 | `FULLY_READ` | FR-VALID-003, UI-01 | Complete text read and indexed |
| `apps/web/src/cognitive/cognitive.css` | `.css` | 493 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/CognitiveHub.jsx` | `.jsx` | 78 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/ContextSlicingStudio.jsx` | `.jsx` | 272 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/DisciplineMatrix.jsx` | `.jsx` | 324 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/McpAttestationStudio.jsx` | `.jsx` | 279 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/ReflectionSandboxStudio.jsx` | `.jsx` | 280 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/SentinelDistillationStudio.jsx` | `.jsx` | 260 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/cognitive/TokenEconomicsStudio.jsx` | `.jsx` | 209 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/components/ui/index.jsx` | `.jsx` | 347 | `FULLY_READ` | UI-001, UI-003 | Complete text read and indexed |
| `apps/web/src/components/ui/tokens.js` | `.js` | 84 | `FULLY_READ` | UI-001 | Complete text read and indexed |
| `apps/web/src/dashboards/CausalBlastRadiusDashboard.jsx` | `.jsx` | 228 | `FULLY_READ` | UI-01 | Complete text read and indexed |
| `apps/web/src/dashboards/ChangeLens.jsx` | `.jsx` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/DomainPackDashboard.jsx` | `.jsx` | 175 | `FULLY_READ` | UI-03 | Complete text read and indexed |
| `apps/web/src/dashboards/EngineDashboardsHub.jsx` | `.jsx` | 100 | `FULLY_READ` | UI-007, UI-008, UI-01, UI-02, UI-03, UI-04 | Complete text read and indexed |
| `apps/web/src/dashboards/MultiParadigmQueryDashboard.jsx` | `.jsx` | 162 | `FULLY_READ` | UI-02 | Complete text read and indexed |
| `apps/web/src/dashboards/ProcessLens.jsx` | `.jsx` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/ReleaseLens.jsx` | `.jsx` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/RuntimeLens.jsx` | `.jsx` | 32 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/SearchAnalyticsDashboard.jsx` | `.jsx` | 79 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/SimulationLens.jsx` | `.jsx` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/TimelineLens.jsx` | `.jsx` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/dashboards/XAIVerificationDashboard.jsx` | `.jsx` | 159 | `FULLY_READ` | UI-04 | Complete text read and indexed |
| `apps/web/src/GraphCanvas.jsx` | `.jsx` | 231 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/icons.jsx` | `.jsx` | 51 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/blast-radius.js` | `.js` | 42 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/centrality.js` | `.js` | 177 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/community.js` | `.js` | 82 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/edge-bundling.js` | `.js` | 147 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/graph-metrics.js` | `.js` | 4 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/link-prediction.js` | `.js` | 44 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/analysis/similarity.js` | `.js` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/AIExplorer.jsx` | `.jsx` | 129 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/AnnotationPanel.jsx` | `.jsx` | 25 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/CentralityRadar.jsx` | `.jsx` | 88 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/CodePanel.jsx` | `.jsx` | 57 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/ComboNode.jsx` | `.jsx` | 84 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/ContextMenu.jsx` | `.jsx` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/EdgeInspector.jsx` | `.jsx` | 75 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/EventFeed.jsx` | `.jsx` | 114 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/ExplorationHistory.jsx` | `.jsx` | 48 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/ExportMenu.jsx` | `.jsx` | 242 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/GeoMap.jsx` | `.jsx` | 84 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/GraphBookmarks.jsx` | `.jsx` | 77 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/GraphDiff.jsx` | `.jsx` | 127 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/GraphHealth.jsx` | `.jsx` | 138 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/GraphToolbar.jsx` | `.jsx` | 102 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/Minimap.jsx` | `.jsx` | 67 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/Playbooks.jsx` | `.jsx` | 131 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/PRDashboard.jsx` | `.jsx` | 78 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/QueryBuilder.jsx` | `.jsx` | 139 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/SimilarityPanel.jsx` | `.jsx` | 26 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/StyleRules.jsx` | `.jsx` | 101 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/SurprisePanel.jsx` | `.jsx` | 59 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/TableView.jsx` | `.jsx` | 119 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/TimelineScrubber.jsx` | `.jsx` | 86 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/VirtualEntityList.jsx` | `.jsx` | 85 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/components/VisualQueryBuilder.jsx` | `.jsx` | 63 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/enhancements.css` | `.css` | 105 | `FULLY_READ` | G2-UX-GRAPH-001, G2-UX-GRAPH-002 | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/GraphEnhancementToolbar.jsx` | `.jsx` | 86 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/GraphMinimap.jsx` | `.jsx` | 100 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/index.js` | `.js` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/LassoSelect.jsx` | `.jsx` | 159 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/layouts.js` | `.js` | 151 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/enhancements/theme.jsx` | `.jsx` | 50 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/export/GraphReport.js` | `.js` | 168 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/export/InteractiveExport.js` | `.js` | 137 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/ImpactGraph.jsx` | `.jsx` | 100 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/KnowledgeGraph.jsx` | `.jsx` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/MetadataGraph.jsx` | `.jsx` | 34 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/OntologyGraph.jsx` | `.jsx` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/ProvenanceGraph.jsx` | `.jsx` | 37 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/RelationshipGraph.jsx` | `.jsx` | 34 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/SimilarityGraph.jsx` | `.jsx` | 94 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/graphs/TemporalGraph.jsx` | `.jsx` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/hooks/useGraphEvents.js` | `.js` | 86 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/KGRExplorer.jsx` | `.jsx` | 986 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/renderers/CytoscapeRenderer.jsx` | `.jsx` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/renderers/LayoutWorker.js` | `.js` | 294 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/renderers/SigmaRenderer.jsx` | `.jsx` | 180 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/kgr/rendering/WebGLGraphRenderer.js` | `.js` | 53 | `FULLY_READ` | G2-UX-GRAPH-002 | Complete text read and indexed |
| `apps/web/src/kgr/workers/layoutWorker.js` | `.js` | 38 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/main.jsx` | `.jsx` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/studio/ConnectorBuilder.jsx` | `.jsx` | 169 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/studio/MappingDesigner.jsx` | `.jsx` | 229 | `FULLY_READ` | REQ-1 | Complete text read and indexed |
| `apps/web/src/studio/PipelineOrchestrator.jsx` | `.jsx` | 202 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/studio/QueryConsole.jsx` | `.jsx` | 115 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/studio/SchemaCanvas.jsx` | `.jsx` | 203 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/studio/studio-utils.js` | `.js` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/studio/studio.css` | `.css` | 331 | `FULLY_READ` | GAP-NOCODE-001, GAP-STUDIO-002 | Complete text read and indexed |
| `apps/web/src/studio/Studio.jsx` | `.jsx` | 46 | `FULLY_READ` | GAP-NOCODE-001, GAP-NOCODE-002, GAP-NOCODE-003, GAP-STUDIO-002, GAP-STUDIO-003 | Complete text read and indexed |
| `apps/web/src/studio/SystemRegistry.jsx` | `.jsx` | 316 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/src/style.css` | `.css` | 1264 | `FULLY_READ` | FR-QUERY-005, FR-VALID-003 | Complete text read and indexed |
| `apps/web/tests/admin-review.spec.js` | `.js` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/admin-source-registry.spec.js` | `.js` | 94 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/application.spec.js` | `.js` | 233 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/cognitive-engineering.spec.js` | `.js` | 103 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/enterprise-capabilities.spec.js` | `.js` | 47 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/error-recovery.spec.js` | `.js` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/guided-demo.spec.js` | `.js` | 133 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/hubble.spec.js` | `.js` | 174 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/tests/recovery-jobs.spec.js` | `.js` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/web/vite.config.js` | `.js` | 7 | `FULLY_READ` | - | Complete text read and indexed |
| `apps/worker/main.py` | `.py` | 344 | `FULLY_READ` | - | Complete text read and indexed |
| `audit-coverage-ledger.md` | `.md` | 2682 | `FULLY_READ` | - | current audit deliverable; generated and verified after source inventory |
| `available-status.md` | `.md` | 38 | `FULLY_READ` | BASE-01, BASE-02 | Complete text read and indexed |
| `config/agents/trace-impact.yaml` | `.yaml` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `config/architecture/default.rules` | `.rules` | 16 | `FULLY_READ` | - | Complete text read and indexed |
| `config/benchmarks/mvp-v1.json` | `.json` | 60 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `config/domain-packs/bfsi/ontology.yaml` | `.yaml` | 66 | `FULLY_READ` | GAP-DP-BFSI-001 | Complete text read and indexed |
| `config/domain-packs/bfsi/pack.yaml` | `.yaml` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `config/domain-packs/compliance/ontology.yaml` | `.yaml` | 59 | `FULLY_READ` | GAP-DP-COMP-001 | Complete text read and indexed |
| `config/domain-packs/compliance/pack.yaml` | `.yaml` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `config/domain-packs/cybersecurity/ontology.yaml` | `.yaml` | 104 | `FULLY_READ` | GAP-DP-CYBER-001, GAP-DP-CYBER-002 | Complete text read and indexed |
| `config/domain-packs/cybersecurity/pack.yaml` | `.yaml` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `config/domain-packs/data-governance/ontology.yaml` | `.yaml` | 61 | `FULLY_READ` | GAP-DP-DG-001, GAP-DP-DG-002 | Complete text read and indexed |
| `config/domain-packs/data-governance/pack.yaml` | `.yaml` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `config/domain-packs/healthcare/ontology.yaml` | `.yaml` | 128 | `FULLY_READ` | GAP-DP-HC-001, GAP-DP-HC-002, GAP-DP-HC-003 | Complete text read and indexed |
| `config/domain-packs/healthcare/pack.yaml` | `.yaml` | 8 | `FULLY_READ` | SR-COM-020 | Complete text read and indexed |
| `config/domain-packs/itsm/ontology.yaml` | `.yaml` | 60 | `FULLY_READ` | GAP-DP-ITSM-001, GAP-DP-ITSM-002 | Complete text read and indexed |
| `config/domain-packs/itsm/pack.yaml` | `.yaml` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `config/domain-packs/manufacturing/ontology.yaml` | `.yaml` | 111 | `FULLY_READ` | GAP-DP-MFG-001, GAP-DP-MFG-002, GAP-DP-MFG-003 | Complete text read and indexed |
| `config/domain-packs/manufacturing/pack.yaml` | `.yaml` | 7 | `FULLY_READ` | SR-COM-020 | Complete text read and indexed |
| `config/domain-packs/software-engineering/ontology.yaml` | `.yaml` | 57 | `FULLY_READ` | GAP-DP-SE-001, GAP-DP-SE-002 | Complete text read and indexed |
| `config/domain-packs/software-engineering/pack.yaml` | `.yaml` | 7 | `FULLY_READ` | - | Complete text read and indexed |
| `config/graph-store.yaml` | `.yaml` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `config/mappings/gitlab-mvp.yaml` | `.yaml` | 3 | `FULLY_READ` | - | Complete text read and indexed |
| `config/mappings/jira-mvp.yaml` | `.yaml` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `config/memory-policy.yaml` | `.yaml` | 4 | `FULLY_READ` | - | Complete text read and indexed |
| `config/ontology/ontology-v0.2.0.yaml` | `.yaml` | 57 | `FULLY_READ` | - | Complete text read and indexed |
| `config/query-policies/default.yaml` | `.yaml` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `config/systems-registry.json` | `.json` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `data/autodemo/raw/demo_enterprise/northstar-commerce-1.0.0.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/02261e11c4f10170546a32a6ef3b2bad83e65ff1e12f57565f905731836645b7.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/06640d79f001fb80e86d7f7a40ae03b0c4daa2fdd97ff0b5b5ed108eb543f5f9.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/079b9ff7b06bd0bed61747b26d3252355c4b335f54021c1e4d494ee83d8a455e.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/179d79ad5551c5216642b31bb8032729a55003e07a7e4a6c48a8b419e36c41d6.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/2d55a168adc84a5ac727d32eaadfc098acb4a8d17a80c47dbc5bfc2cb9ad7937.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/3dfc3521dad15faf22d5ff8f0948e12b1d46b34cad468973251f303d51e0cf5a.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/414ffac40e9e13fcfad3d0be00c61c9bda2fc829a5605a75b3cd65981deeddbc.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/4ae3465b3adff7febfe9f8dd31e2e516f94168a7093b22cf77313d6a2ce14cef.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/4baeed26114d142528d6afc995817eb37e486534ce6af44f62932b14b6d05a25.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/661e3d8d600adede5ccfa78407b864be06dae17fd8488521d35b5766c14486dd.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/6ba1088eecfd9dfb932022bf73365399686228aabfdb0aac2408d46401994d6f.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/718cb98c4fee5665640d616e70681405fba01bf8e9618908301f5c438704d14c.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/7ea0cb949d27ef2d352e364f66d2c195fd26317dd4dd36485dfb3c6a0e729e78.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/92d9dabd023ddee01cf7040fafba6e3148c2142a1362571d2b595127c7be09cd.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/9e9eac56afb6ebd5ee1983b83611d89e11cba6e0b56227bef5feeb98a22ee371.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/ac79e1025513d2e720433650614caba7f6978cf0dcc0c57388fbae31034c8ae0.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/bfca43bdef9b6dfb6c6b94f2d5d523c9fbb721a3925dcdf5f441e979f0b80968.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/c74759deac0d93ca4da7abbadcb467cc50df14fbad16651db65a1aa71af51a97.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/c912e6a041240320fed38d70f4f067f4ad3b502d8e3443586dbab90d6c2ea8ef.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/cdc0914666da0ca4c16532c8696d055f2ef13945e4c55c7a20fe688fb11245ff.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/e5870011f15fa3cfd8bc9887410bcf0d14966165ecb4dd05000214e85a7d5a7f.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/edac9ed7d5f66d88d1b16394a1b19de5903e18b2d75a4d4a2ff9d08c78d88edd.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/ee4cecea704609feb3c7782fc7a6274c149caa58ce9b4e733a66039446cb66ec.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/FRD/jira/f74da36d3e0dfec1fe1400506ba36f2516041cf2ad050beddeca0c2b33846dd4.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/007354d64f6fe8780a2dbb76ff8235f06ca6ceb18bc13b35827d90b3a149ef44.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/0b65ab083f2f4cd14677ae2ec28b74e1f6bef488c6fdeb372e02c5cbd419aef5.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/0f99e60284afa4534d8bfc569fed06d95b738f0e4b43ad14c3f6d39a141b305e.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/18d3a43856e0e8519964c28dea072a5a0399f4e13918d5a153e685bf0964cb73.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/192d40fe8ac0fb695fb9e7106714bd766a3eafc6f40d5c5e1a49c4d8a6b98830.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/1bfd3d84d968df19f5efdcd0086c1be21dc688a2b67141b1188ad0e786ad3948.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/1d4cf4b3a3488f916c258884c8feb9fc6da328719ee4b3d50360ed66c532c1d2.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/1db7358f1d8329778a4af5134e426d18870676409ca3c1534f54e5cb32030305.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/1df79bf940e2462f43fb8fab9fd2880992ac5d990b6a9e0107e9fda00b834a16.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/2a12e3f0626e2f9ba213e9f21a5bd9d7c880904932ee25868baee14d5725c5aa.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/33972a7c31d312de6bdb3a78cb44042ff668f3ce9f2b1b03e55b8ebc9cd3eac9.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/35c4352ac39bc982ca9a2e88e4e359d4cf2d8267a96916f86fceb18ee422a236.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/43a4df897c781fbc600c30ca3d459844d399cdb326d64031e97011723df81997.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/46adf5a80321660014aa682df3a7cc9e38f33c3a8cb9034b888d09b32cb74600.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/4729b6c87529c917f87a8d3fe284146658b31414e6e36f546d9afc69230197f4.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/4af7cd48b88bac2969514bde73d368090e59711030952e9cf2a422aefe44218c.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/4d80b797882c9987ddae4c4c989240544fae0c274c5e4f7bc1f782de9edfc1c8.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/4edbd6ed955d023d730ab00b237b776d676518eb0158f001520f7bf178af8f06.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/5400184b8e6a03a4fa164a82aa35a12eb51ac72c379007d4c490269b21530fd1.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/66822b4b11e1cdbc57bb179d832cc51b372ec41c0778d3ad4f226636415c3602.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/79f6db39bdb63623e80b564dca02b461810dc4ed93d7652168877027b65cc67f.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/7fafb6ea2f9aee0f00833fbba05b79dcb4859fe3835d0882f61179ded96ef101.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/82a3352e24169e7bf92346e20c69012515c30418b2e0f9b2383f318690b9079c.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/8aefc312ef35c8879bae56aa0b4145d3927de13463f6e5fcc86cbb041ac141db.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/8dcf0f23cbcc36cb66154972e5e860459a5f9f1acc7540239a13c9562f36631e.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/9cdd92fc95b63f690a447980ba543b35ce99ca09064696b7ddda768f7d5f8d71.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/9fddee510b647e30c7ab006a0fa6103b7bfd22cc0d14c9c3ef455cf904914cc6.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/a633643b87cddb04d3f38fc0e8c5874642ac973ed734a8e402a496b4466bbf5b.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/a69d66d447168421619d921137de5444d60b2085427bac51e55324c841504a93.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/a9909a41180693a890f6c06e73d71df9cc0d00190f2e66d5d5523d9872f9e377.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/b0c74dc2a5b108c58a4f7d9621c97cf06a0ef81797015174742285562cfa1eee.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/c995985f6714a532cde4a1b910b2b12115139cd0cb0d7ef301eff0d602a4f367.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/dc2a32988813c84c9ff13693125eba9af222a04fd0547c05afb550349be62eff.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/dfc587353f8b7837bfc24e244f0e07870767dddd96caef0f188baa76cc8149b6.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/e0ac176efdfee72d38629bbeb6f152cefe68429bd4769d1ede520160c7fe206c.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/e525f63295e92cb592c63ef299226c83a0fc01e909288ee0f130a76a740f0a27.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/e5439006df4a45dc262ffb29a76431ca641fff990d630238eb708db7dbc3c5a9.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/f1c27178e98cdb87f67c2cb891d3ed506afc303c1e43cfcffc62d7d31bb01db7.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/f476d3c69d35bb42a2325b90e325622b3523bb688397d7dbc8367525859b862d.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/f8c651ced54b77b2baa76da12ddeb917b36671520eb167328889cf1542ee36f8.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/git/fc5b28811e9274e09b0c9e306446f0c866a9bb1522d2c810e68c5653b3b8c287.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/jira/93beab733b1f92566e7e26e7f24f9b0289ed81982e0bbd39317d85811ea48fb2.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/jira/bafe019a7d47232f4a9f95b515c2fc3aaa6e6aa7a1b7dfc8ade68240071612bb.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/009eee60ad58a1c60749bb9e36ea7a09ad31f191bb45d9302b26c7e1558134b4.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/08de20bc21434d639ab06bd493d994782fb297872c6656561408612fdc976f64.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/0edca096be95696cce8457d102540f0e58b415c19cbcdb3f960b53fbd6600be6.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/25194f19a9882950e5dccee4bb06f660b3958c6d5bc47b3b2db9e2bf20a2b4db.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/2799468994d0add861a025dcb19118be001615d1ee247dabaf252b403be41c18.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/2a025f5ceeb0457547fa9183b4ce681f71b51ff035ce6193a96f369211cfe51d.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/2a1d30d06ec91c4bf7d8ec4684c1f6b5cf1f5975f401f4691c9608a43ca09977.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/38b64383fc9dcf7b7348fb5577c6b4ba45b0698486040b5c4f00841979407a27.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/4906d447e62ca59822763db818760a188b81a6dd57bca112ea0690fdc4fb48c8.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/56e7665987a09fe955087076411a8d6fa65d26f67a83cde805907d159d4d4c7a.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/58cef4de48cc448c4e4f1dbf664e859e59cae73e38d1b7f8a3c2b7e2e16b62d0.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/6e4407ec1725622b33c1004477d8d0c97b8c32930adc9ed1eaf9a2032b446b47.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/783d7e0c876aefd8d35998abbfd54566d0d315db9d1b62f11ce3957fcc720ddd.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/8109d6ef8b6ce6324ed155a7d7e24c84c414b329a58181bb80e2062a8e5430b8.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/8e1293cbcdd2b6f296a4b6d9cd5c985ffef6eb55e05369f44ac442eac75e58f7.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/9151a32c8a04801fc5720a2ec79e7a379cf011e87c8ae1325f5bf55fec1678ac.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/970110360a1552b6b6d3abc5cd6479f69057a06ba898f5a39426e9c083c783b0.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/99608931076e3f901a4d1c4ad671418d0537e0838b47aa89254bb4d4619e7038.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/9a51020a213f22fe26ecd3f5227507c7d7637023419bff7e2d3be2def9650039.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/b24233007cbb43d71da6e7b6c6d5915c2ffc2d7df48092863768e2002e52b022.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/b25bfb5d178c687afca8743791d0a77f8cb4378f7e9c3e2b6f25532149540310.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/bb00913ccac1a57f3cab104b2cd2151342e6b01df2d082a4d629e70c6f472aa0.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/bb607188b8bb5666a99e9ac012a3be686c9693173a8a15621efe096c3008c41f.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/c7144120c8ef47ae47736ae51ea08cad421462a43fb150ef3e9121b4e68a247a.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/e72bbde4ea33d8c6ece8664469e69362ff57b29b6d37f6149dd432dd1ffadd55.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/ec74c64168775a496bae83de1c3ee549820ddb4704855bdf5c065e1bfff5cc27.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/f878ce0457f56f3f768dd208005b8d5aba43c3a0d9fe783f6fbbe16ccd3dfbab.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/autodemo/raw/PAY/jira/fd8865bd39e669e7a62bda864a4abe5f06dab3079922395d7704ede34ce5caa4.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/manifest.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/ontology/enterprise-type-hierarchy.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/ontology/relationship-constraints.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `data/seed/default-taxonomy.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/__init__.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/__init__.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/admin_runner.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/administration-demo.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/application-demo.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/browser-demo.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/enterprise-journeys.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/generate_documents.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/launch-demo.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/results.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo-admin.bat` | `.bat` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo-hubble.bat` | `.bat` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo-hubble.ps1` | `.ps1` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo-manual.bat` | `.bat` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo-pipeline.bat` | `.bat` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo-vscode.bat` | `.bat` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/run-demo.bat` | `.bat` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/runner.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/runtime-validation-report.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/tests/enterprise-journeys.test.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/tests/evidence.test.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/tests/launchers.test.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/tests/options.test.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/autodemo/vscode-demo.js` | `.js` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/__init__.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/agents/agent-scenarios.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/code/mfs-common-libs.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/code/mfs-customer-portal.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/code/mfs-fraud-engine.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/code/mfs-payment-gateway.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/code/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/confluence/sample-confluence.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/demo-repo/client.ts` | `.ts` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/demo-repo/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/demo-repo/service.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/demo-repo/src/client.ts` | `.ts` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/demo-repo/src/service.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/eval/rag-golden.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/gitlab/merge-requests-pipelines.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/gitlab/sample-gitlab.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/jira/sample-jira.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/core/servicenow/sample-servicenow.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/crawler/api-portal-swagger.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/crawler/db-schemas.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/crawler/figma-designs.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/crawler/observability-portals.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/crawler/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/crawler/wiki-confluence.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/deployment-checklist-PAY.txt` | `.txt` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/FRD-Model-Performance-Metrics.csv` | `.csv` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Change-Calendar.xlsx` | `.xlsx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Fraud-Detection-ML-Architecture.docx` | `.docx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Incident-Postmortem-INC0080101.docx` | `.docx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Payment-Gateway-Architecture-v2.docx` | `.docx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Payment-Gateway-v2-Release-Review.pptx` | `.pptx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-PCI-DSS-Compliance-Report.docx` | `.docx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Platform-Overview-Q4-2026.pptx` | `.pptx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Service-Inventory.xlsx` | `.xlsx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/MFS-Test-Coverage-Matrix.xlsx` | `.xlsx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/PAY-Sprint14-Burndown.csv` | `.csv` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/runbook-fraud-engine-alerts.txt` | `.txt` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/documents/service-accounts-audit-Q3.txt` | `.txt` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/api/checkout-openapi.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/project-code/services/checkout/api.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/project-code/services/checkout/risk.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/project-code/tests/test_risk.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/scenario-pack.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/api-portal.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/confluence.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/figma.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/gitlab.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/jira.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/observability.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/qtest.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/source-fixtures/servicenow.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/wiki/checkout-latency-runbook.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/enterprise/wiki/checkout-risk-architecture.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/laya/laya-scenarios.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/api-portal.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/code-graph.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/confluence.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/crawler-sites.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/datadog.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/figma.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/gitlab.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/grafana.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/jira.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/kibana.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/qtest.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/rally.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/manual/servicenow.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/api-portal.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/code-graph.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/confluence.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/crawler-sites.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/datadog.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/figma.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/gitlab.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/grafana.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/jira.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/kibana.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/pipeline-config.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/qtest.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/rally.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/README.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/pipelines/servicenow.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/query/query-examples.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/demodata/rag/rag-demo-queries.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/script/presentation.html` | `.html` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/script/presentation.pptx` | `.pptx` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `demo/script/walkthrough.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded demo/example/data content |
| `deploy/.env.example` | `.example` | 20 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/argocd/application.yaml` | `.yaml` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/Containerfile` | `[none]` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/docker-compose.acceptance.yml` | `.yml` | 46 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/docker-compose.dlq-acceptance.yml` | `.yml` | 112 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/docker-compose.ha.yml` | `.yml` | 198 | `FULLY_READ` | GAP-HA-001, GAP-HG-006 | Complete text read and indexed |
| `deploy/docker-compose.observability.yml` | `.yml` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/docker-compose.yml` | `.yml` | 274 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/Dockerfile` | `[none]` | 29 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/environments/production/values.yaml` | `.yaml` | 40 | `FULLY_READ` | INFRA-003 | Complete text read and indexed |
| `deploy/environments/staging/values.yaml` | `.yaml` | 32 | `FULLY_READ` | INFRA-003 | Complete text read and indexed |
| `deploy/helm/eoip/Chart.yaml` | `.yaml` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/_helpers.tpl` | `.tpl` | 66 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/configmap.yaml` | `.yaml` | 28 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/deployment.yaml` | `.yaml` | 154 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/hpa.yaml` | `.yaml` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/ingress.yaml` | `.yaml` | 35 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/NOTES.txt` | `.txt` | 32 | `FULLY_READ` | GAP-PERF-001 | Complete text read and indexed |
| `deploy/helm/eoip/templates/pvc.yaml` | `.yaml` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/redis.yaml` | `.yaml` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/templates/service.yaml` | `.yaml` | 54 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/helm/eoip/values.yaml` | `.yaml` | 155 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/Containerfile` | `[none]` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/default-language.js` | `.js` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/Dockerfile` | `[none]` | 7 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/enterprise.css` | `.css` | 32 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/enterprise.html` | `.html` | 49 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/enterprise.js` | `.js` | 258 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/graph-idl.css` | `.css` | 321 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/graph-idl.html` | `.html` | 152 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/graph-idl.js` | `.js` | 647 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/hubble/hugegraph-hubble.properties` | `.properties` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/nginx/api-lb.conf` | `.conf` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `deploy/nginx/hugegraph-lb.conf` | `.conf` | 20 | `FULLY_READ` | GAP-HG-006 | Complete text read and indexed |
| `deploy/prometheus.yml` | `.yml` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `docs/api-reference.md` | `.md` | 17 | `FULLY_READ` | MVP-FR-024, NFR-OPS-001, NFR-OPS-002 | Complete text read and indexed |
| `docs/architecture-guide.md` | `.md` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `docs/audit-2026-10-06/assessed-gap-report.json` | `.json` | 2038 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `docs/audit-2026-10-06/assessed-gap-report.md` | `.md` | 1021 | `FULLY_READ` | AI-ACT-ART-13, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE... | Complete text read and indexed |
| `docs/getting-started.md` | `.md` | 46 | `FULLY_READ` | - | Complete text read and indexed |
| `docs/release-checklist.md` | `.md` | 103 | `FULLY_READ` | CG-GAP-008, MVP-FR-028, REL-01, REL-02, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-09, REL-10 (+9 more) | Complete text read and indexed |
| `EOIP-engg-doc-pkg/00-specification-audit-and-enhancements.md` | `.md` | 108 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/01-project-vision.md` | `.md` | 42 | `FULLY_READ` | FR-GRAPH-001, FR-GRAPH-006, FR-PROV-001, FR-QUERY-003, FR-RAG-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/02-scope-and-objectives.md` | `.md` | 42 | `FULLY_READ` | FR-AGENT-003, FR-CODE-002, FR-CONN-002, FR-CONN-003, FR-RAG-004 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/03-functional-requirements.md` | `.md` | 683 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/04-non-functional-requirements.md` | `.md` | 171 | `FULLY_READ` | NFR-MAINT-001, NFR-OPS-001, NFR-OPS-002, NFR-PERF-001, NFR-PRIV-001, NFR-REL-001, NFR-REL-002, NFR-SEC-001, NFR-SEC-002,... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/05-system-requirements.md` | `.md` | 42 | `FULLY_READ` | FR-GRAPH-001, NFR-OPS-001, NFR-REL-001, NFR-SEC-001, NFR-SEC-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/06-architecture.md` | `.md` | 333 | `FULLY_READ` | FR-AGENT-002, FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-006, FR-GRAPH-011, FR-QUERY-001, FR-RAG-003, GAP-FABRIC-001, GAP-OPS-... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/07-component-architecture.md` | `.md` | 72 | `FULLY_READ` | FR-AGENT-001, FR-CONN-001, FR-GRAPH-007, FR-INGEST-002, FR-MCP-001, FR-RAG-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/08-deployment-architecture.md` | `.md` | 79 | `FULLY_READ` | FR-GRAPH-001, NFR-OPS-001, NFR-SEC-001, NFR-SEC-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/09-data-architecture.md` | `.md` | 44 | `FULLY_READ` | FR-GRAPH-004, FR-INGEST-001, FR-INGEST-002, FR-PROV-001, NFR-PRIV-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/10-enterprise-ontology.md` | `.md` | 40 | `FULLY_READ` | FR-GRAPH-010, FR-ONTO-001, FR-ONTO-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/11-graph-schema.md` | `.md` | 62 | `FULLY_READ` | FR-GRAPH-003, FR-GRAPH-004, FR-GRAPH-008, FR-ONTO-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/12-meta-graph-design.md` | `.md` | 40 | `FULLY_READ` | FR-GRAPH-005, FR-INGEST-004, FR-VALID-003 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/13-relationship-model.md` | `.md` | 40 | `FULLY_READ` | FR-GRAPH-006, FR-ONTO-002, FR-PROV-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/14-temporal-graph.md` | `.md` | 39 | `FULLY_READ` | FR-GRAPH-009, FR-TEMP-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/15-provenance-lineage.md` | `.md` | 40 | `FULLY_READ` | FR-INGEST-001, FR-PROV-001, FR-PROV-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/16-identity-resolution.md` | `.md` | 39 | `FULLY_READ` | FR-ID-001, FR-ID-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/17-code-graph.md` | `.md` | 65 | `FULLY_READ` | CG-CODE-01, CG-CODE-02, FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/18-ingestion-architecture.md` | `.md` | 53 | `FULLY_READ` | FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/19-connector-framework.md` | `.md` | 41 | `FULLY_READ` | FR-CONN-001, FR-CONN-005, FR-CONN-006, FR-CONN-007 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/20-jira-connector-requirements.md` | `.md` | 39 | `FULLY_READ` | FR-CONN-002, FR-INGEST-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/21-confluence-connector-requirements.md` | `.md` | 38 | `FULLY_READ` | FR-CONF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/22-gitlab-connector-requirements.md` | `.md` | 40 | `FULLY_READ` | FR-CODE-003, FR-CONN-003, FR-CONN-004 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/23-servicenow-connector-requirements.md` | `.md` | 38 | `FULLY_READ` | FR-SNOW-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/24-file-web-connectors.md` | `.md` | 42 | `FULLY_READ` | FR-CONN-001, NFR-PRIV-001, NFR-SEC-003 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/25-query-engine-requirements.md` | `.md` | 57 | `FULLY_READ` | FR-QUERY-001, FR-QUERY-002, FR-QUERY-003, FR-QUERY-004, FR-QUERY-005, FR-QUERY-006, FR-QUERY-007, FR-QUERY-008, FR-QUERY... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/26-query-engine-implementation.md` | `.md` | 66 | `FULLY_READ` | FR-GRAPH-007, FR-QUERY-001, FR-QUERY-002, FR-QUERY-003 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/27-ontology-validation.md` | `.md` | 39 | `FULLY_READ` | FR-VALID-001, FR-VALID-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/28-graph-quality.md` | `.md` | 39 | `FULLY_READ` | FR-PROV-001, FR-VALID-003 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/29-rag-architecture.md` | `.md` | 58 | `FULLY_READ` | FR-RAG-001, FR-RAG-002, FR-RAG-003, FR-RAG-004, FR-RAG-005, FR-RAG-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/30-agent-architecture.md` | `.md` | 61 | `FULLY_READ` | FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/31-multi-agent-architecture.md` | `.md` | 40 | `FULLY_READ` | FR-AGENT-001, FR-AGENT-002, FR-AGENT-004 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/32-memory-engineering.md` | `.md` | 39 | `FULLY_READ` | FR-MEM-001, NFR-PRIV-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/33-context-engineering.md` | `.md` | 42 | `FULLY_READ` | FR-PROV-001, FR-QUERY-007, FR-RAG-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/34-loop-engineering.md` | `.md` | 38 | `FULLY_READ` | FR-AGENT-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/35-graph-engineering.md` | `.md` | 42 | `FULLY_READ` | FR-GRAPH-002, FR-GRAPH-006, FR-GRAPH-008 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/36-harness-engineering.md` | `.md` | 42 | `FULLY_READ` | FR-AGENT-001, FR-AGENT-002, NFR-OPS-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/37-graph-over-loop.md` | `.md` | 41 | `FULLY_READ` | FR-AGENT-002, FR-GRAPH-005 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/38-loop-over-graph.md` | `.md` | 40 | `FULLY_READ` | FR-AGENT-002, FR-QUERY-003, FR-QUERY-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/39-mcp-architecture.md` | `.md` | 40 | `FULLY_READ` | FR-AGENT-004, FR-MCP-001, FR-MCP-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/40-human-control-model.md` | `.md` | 39 | `FULLY_READ` | FR-AGENT-004, FR-AGENT-005 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/41-xai-explainability.md` | `.md` | 40 | `FULLY_READ` | FR-PROV-001, FR-QUERY-007, FR-RAG-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/42-web-user-ui-ux.md` | `.md` | 40 | `FULLY_READ` | FR-QUERY-004, FR-UI-001, FR-UI-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/43-admin-ui-ux.md` | `.md` | 43 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-INGEST-004, FR-VALID-003 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/44-vscode-extension.md` | `.md` | 42 | `FULLY_READ` | FR-CODE-005, FR-VSCODE-001, FR-VSCODE-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/45-api-specification.md` | `.md` | 43 | `FULLY_READ` | FR-AGENT-003, FR-INGEST-004, FR-QUERY-001, FR-QUERY-007 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/46-security-architecture.md` | `.md` | 56 | `FULLY_READ` | NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-SEC-006, NFR-SEC-007 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/47-threat-model.md` | `.md` | 49 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/48-data-privacy.md` | `.md` | 40 | `FULLY_READ` | NFR-PRIV-001, NFR-SEC-002, NFR-SEC-007 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/49-local-ai-model-strategy.md` | `.md` | 40 | `FULLY_READ` | FR-RAG-003, FR-RAG-004, NFR-SEC-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/50-observability.md` | `.md` | 38 | `FULLY_READ` | NFR-OPS-001, NFR-OPS-002, NFR-SEC-007 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/51-performance.md` | `.md` | 45 | `FULLY_READ` | FR-GRAPH-008, NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/52-scalability.md` | `.md` | 40 | `FULLY_READ` | FR-GRAPH-002, NFR-MAINT-001, NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/53-backup-restore.md` | `.md` | 38 | `FULLY_READ` | NFR-REL-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/54-devsecops.md` | `.md` | 40 | `FULLY_READ` | NFR-MAINT-001, NFR-SEC-002, NFR-SEC-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/55-testing-strategy.md` | `.md` | 110 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/56-rag-agent-evaluation.md` | `.md` | 42 | `FULLY_READ` | FR-AGENT-002, FR-AGENT-003, FR-RAG-005 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/57-graph-validation-test-plan.md` | `.md` | 43 | `FULLY_READ` | FR-PROV-001, FR-VALID-001, FR-VALID-002, FR-VALID-003 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/58-end-to-end-test-plan.md` | `.md` | 42 | `FULLY_READ` | FR-AGENT-003, FR-GRAPH-006, FR-MCP-001, FR-VSCODE-001, NFR-REL-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/59-docker-deployment.md` | `.md` | 64 | `FULLY_READ` | FR-GRAPH-001, NFR-OPS-001, NFR-SEC-001, NFR-SEC-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/60-operational-runbook.md` | `.md` | 41 | `FULLY_READ` | NFR-OPS-001, NFR-OPS-002, NFR-REL-001, NFR-REL-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/61-demo-playbook.md` | `.md` | 61 | `FULLY_READ` | FR-GRAPH-006, FR-MCP-001, FR-QUERY-002, FR-QUERY-003, FR-RAG-002, FR-VSCODE-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/62-risk-register.md` | `.md` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/63-assumptions.md` | `.md` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/64-decisions-and-adrs.md` | `.md` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/65-glossary.md` | `.md` | 50 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/66-phase-roadmap.md` | `.md` | 64 | `FULLY_READ` | FR-AGENT-005, FR-CONF-001, FR-GRAPH-010, FR-RAG-006, FR-SNOW-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/67-implementation-plan.md` | `.md` | 265 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/68-project-structure.md` | `.md` | 87 | `FULLY_READ` | FR-CONN-001, FR-QUERY-001, NFR-MAINT-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/69-dependency-license-sbom.md` | `.md` | 37 | `FULLY_READ` | NFR-MAINT-001, NFR-SEC-006 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/70-acceptance-criteria.md` | `.md` | 131 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/71-research-and-verification-basis.md` | `.md` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/72-requirement-traceability.md` | `.md` | 128 | `FULLY_READ` | AC-FR-ADMIN-001, AC-FR-ADMIN-002, AC-FR-AGENT-001, AC-FR-AGENT-002, AC-FR-AGENT-003, AC-FR-AGENT-004, AC-FR-AGENT-005, A... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/73-architecture-diagrams.md` | `.md` | 293 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/74-data-contracts.md` | `.md` | 209 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/75-self-review-and-gap-closure.md` | `.md` | 40 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/76-multi-backend.md` | `.md` | 179 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/agent_runbook.md` | `.md` | 83 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/Audit-GAPS-CG-dev.md` | `.md` | 142 | `FULLY_READ` | CG-DEV-2026-10-11, CG-GAP-001, CG-GAP-002, CG-GAP-003, CG-GAP-004, CG-GAP-005, CG-GAP-006, CG-GAP-007, CG-GAP-008, CG-GA... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/audit-2026-10-06/assessed-gap-report.json` | `.json` | 2038 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/audit-2026-10-06/assessed-gap-report.md` | `.md` | 1021 | `FULLY_READ` | AI-ACT-ART-13, FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/audit-2026-10-06/detailed-requirements-report.md` | `.md` | 57 | `FULLY_READ` | GAP-AGOV-001, GAP-AKO-001, GAP-ARCH-001, GAP-CHANGE-001, GAP-CONTRACT-001, GAP-CP-001, GAP-DBAGNOSTIC-001, GAP-EXPORT-00... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/audit-2026-10-06/phase-by-phase-implementation-approach.md` | `.md` | 51 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/benchmarks/2026-10-03-hugegraph-smoke-after-cache.json` | `.json` | 129 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/benchmarks/2026-10-03-hugegraph-smoke-bulk.json` | `.json` | 137 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/benchmarks/2026-10-03-hugegraph-smoke.json` | `.json` | 129 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/benchmarks/2026-10-03-memory-full.json` | `.json` | 129 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/benchmarks/2026-10-03-memory-smoke.json` | `.json` | 129 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/generated/current-gap-report.json` | `.json` | 1 | `FULLY_READ` | AC-04, AC-FR-ADMIN-001, AC-FR-ADMIN-002, AC-FR-AGENT-001, AC-FR-AGENT-002, AC-FR-AGENT-003, AC-FR-AGENT-004, AC-FR-AGENT... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/generated/current-gap-report.md` | `.md` | 1706 | `FULLY_READ` | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012 (+848 more) | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/generated/documentation-inventory.json` | `.json` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/generated/README.md` | `.md` | 27 | `FULLY_READ` | CG-GAP-009 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/historical/application-audit-2026-10-02.md` | `.md` | 76 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/historical/demo-readiness-audit-2026-10-03.md` | `.md` | 178 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/historical/eoip-development-audit-2026-10-03.md` | `.md` | 563 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/historical/gap-audit-2026-10-02.md` | `.md` | 637 | `FULLY_READ` | FR-AGENT-001, FR-CODE-003, FR-CONF-001, FR-CONN-001, FR-CONN-003, FR-CONN-006, FR-CONN-007, FR-GRAPH-002, FR-GRAPH-003, ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/historical/phase-completion-audit-2026-10-03.md` | `.md` | 400 | `FULLY_READ` | FR-CONF-001, FR-MEM-001, G2-P0, G2-P1, G2-P10, G2-P2, G2-P3, G2-P4, G2-P5, G2-P6, G2-P7, G2-P8 (+9 more) | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/consolidated-requirements.md` | `.md` | 8239 | `FULLY_READ` | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, AC-08, AC-09, AC-10, AC-11, AC-12 (+1230 more) | Complete text read and indexed |
| `EOIP-engg-doc-pkg/audits/reconstruction-audit-2026-10-07/mvp-phase-by-phase-implementation-plan.md` | `.md` | 332 | `FULLY_READ` | FR-GRAPH-003, FR-GRAPH-007, G2-ADMIN-001, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, G2-ADMIN... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/available-status.md` | `.md` | 38 | `FULLY_READ` | BASE-01, BASE-02 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/checklist.md` | `.md` | 112 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/context.md` | `.md` | 105 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/01-system-context.md` | `.md` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/02-container-architecture.md` | `.md` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/03-ingestion-pipeline.md` | `.md` | 10 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/04-enterprise-graph-architecture.md` | `.md` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/05-meta-graph.md` | `.md` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/06-code-graph.md` | `.md` | 12 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/07-cross-domain-relationship-graph.md` | `.md` | 15 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/08-query-execution.md` | `.md` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/09-graphrag.md` | `.md` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/10-agent-runtime.md` | `.md` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/11-multi-agent-orchestration.md` | `.md` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/12-mcp-architecture.md` | `.md` | 12 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/13-human-control-architecture.md` | `.md` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/14-web-ui-architecture.md` | `.md` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/15-vscode-architecture.md` | `.md` | 12 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/16-deployment.md` | `.md` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diagrams/17-mvp-e2e-flow.md` | `.md` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/diamond-moonshots-advanced.md` | `.md` | 685 | `FULLY_READ` | KGR-G-001, KGR-G-006, KGR-G-020, MS-1, MS-10, MS-11, MS-12, MS-13, MS-14, MS-15, MS-16, MS-17 (+22 more) | Complete text read and indexed |
| `EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md` | `.md` | 109 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/eoip-phase4-requirements.md` | `.md` | 1058 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, AI-001, AI-002, AI-003, AI-004, AI-005, AI-006, AI-007, COMPLY-001 (+37 more... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/eoip-phase4-tracker.html` | `.html` | 477 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, AI-001, AI-002, AI-003, AI-004, AI-005, AI-006, AI-007, COMPLY-001 (+37 more... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/examples/demo_code.py` | `.py` | 0 | `EXCLUDED` | - | user-excluded example content |
| `EOIP-engg-doc-pkg/examples/demo_documentation.md` | `.md` | 0 | `EXCLUDED` | - | user-excluded example content |
| `EOIP-engg-doc-pkg/examples/gitlab-synthetic.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded example content |
| `EOIP-engg-doc-pkg/examples/jira-synthetic.json` | `.json` | 0 | `EXCLUDED` | - | user-excluded example content |
| `EOIP-engg-doc-pkg/gaps-implementation.md` | `.md` | 1216 | `FULLY_READ` | GAP-AGOV-001, GAP-AKO-001, GAP-APP-001, GAP-ARCH-001, GAP-CACHE-001, GAP-CATALOG-001, GAP-CHANGE-001, GAP-CONTRACT-001, ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/gaps-requirements.md` | `.md` | 1401 | `FULLY_READ` | GAP-AGOV-001, GAP-AGOV-002, GAP-AGOV-003, GAP-AGOV-004, GAP-AGOV-005, GAP-AGOV-006, GAP-AGOV-007, GAP-AGOV-008, GAP-AGOV... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/gaps2-implementation.md` | `.md` | 1625 | `FULLY_READ` | G2-ADMIN-001, G2-ARCH-001, G2-ARCHC-001, G2-CAP-001, G2-CAUSE-001, G2-EKAF-001, G2-EKAF-003, G2-EVENT-001, G2-EVOL-001, ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/gaps2-requirements.md` | `.md` | 2059 | `FULLY_READ` | G2-ADMIN-001, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, G2-ADMIN-007, G2-ADMIN-008, G2-ADMIN... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/handoff_template.md` | `.md` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-agent-memory.md` | `.md` | 77 | `FULLY_READ` | FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-MEM-001, WP-AGENT-MEMORY-01, WP-AGENT-MEMORY-02... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-codegraph.md` | `.md` | 67 | `FULLY_READ` | FR-CODE-001, FR-CODE-002, FR-CODE-003, FR-CODE-004, FR-CODE-005, WP-CODEGRAPH-01, WP-CODEGRAPH-02, WP-CODEGRAPH-03, WP-C... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-connectors.md` | `.md` | 107 | `FULLY_READ` | FR-CONF-001, FR-CONN-001, FR-CONN-002, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-CONN-006, FR-CONN-007, FR-SNOW-001, WP-... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-experience.md` | `.md` | 77 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-UI-001, FR-UI-002, FR-VSCODE-001, FR-VSCODE-002, WP-EXPERIENCE-01, WP-EXPERIENCE-02, WP-E... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-foundation.md` | `.md` | 67 | `FULLY_READ` | FR-GRAPH-001, FR-GRAPH-002, FR-GRAPH-003, FR-GRAPH-004, NFR-MAINT-001, WP-FOUNDATION-01, WP-FOUNDATION-02, WP-FOUNDATION... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-ingestion.md` | `.md` | 67 | `FULLY_READ` | FR-INGEST-001, FR-INGEST-002, FR-INGEST-003, FR-INGEST-004, FR-INGEST-005, WP-INGESTION-01, WP-INGESTION-02, WP-INGESTIO... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-mcp.md` | `.md` | 37 | `FULLY_READ` | FR-MCP-001, FR-MCP-002, WP-MCP-01, WP-MCP-02 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-ontology-graph.md` | `.md` | 137 | `FULLY_READ` | FR-GRAPH-005, FR-GRAPH-006, FR-GRAPH-008, FR-GRAPH-009, FR-GRAPH-010, FR-ID-001, FR-ID-002, FR-ONTO-001, FR-ONTO-002, FR... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-query.md` | `.md` | 107 | `FULLY_READ` | FR-GRAPH-007, FR-QUERY-001, FR-QUERY-002, FR-QUERY-003, FR-QUERY-004, FR-QUERY-005, FR-QUERY-006, FR-QUERY-007, FR-QUERY... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-rag.md` | `.md` | 77 | `FULLY_READ` | FR-RAG-001, FR-RAG-002, FR-RAG-003, FR-RAG-004, FR-RAG-005, FR-RAG-006, WP-RAG-01, WP-RAG-02, WP-RAG-03, WP-RAG-04, WP-R... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-security-ops.md` | `.md` | 157 | `FULLY_READ` | NFR-MAINT-001, NFR-OPS-001, NFR-OPS-002, NFR-PERF-001, NFR-PRIV-001, NFR-REL-001, NFR-REL-002, NFR-SEC-001, NFR-SEC-002,... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/implementation/wp-validation.md` | `.md` | 47 | `FULLY_READ` | FR-VALID-001, FR-VALID-002, FR-VALID-003, WP-VALIDATION-01, WP-VALIDATION-02, WP-VALIDATION-03 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/instruction.md` | `.md` | 140 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/ip.md` | `.md` | 432 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/KGR-g-implementation-plan.md` | `.md` | 451 | `FULLY_READ` | KGR-G-001, KGR-G-002, KGR-G-003, KGR-G-004, KGR-G-005, KGR-G-006, KGR-G-007, KGR-G-008, KGR-G-009, KGR-G-010, KGR-G-011,... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/KGR-g-requirements.md` | `.md` | 948 | `FULLY_READ` | FR-01, FR-67, G2-P0-001, G2-P10-040, GAP-001, GAP-296, KGR-G-001, KGR-G-002, KGR-G-003, KGR-G-004, KGR-G-005, KGR-G-006 ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/KGR-implementation-plan.md` | `.md` | 2838 | `FULLY_READ` | FR-KGR-010, FR-KGR-011, FR-KGR-012, FR-KGR-013, FR-KGR-014, FR-KGR-015, FR-KGR-016 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/KGR-requirements.md` | `.md` | 1145 | `FULLY_READ` | AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, AC-08, AC-09, AC-10, AC-11, AC-12 (+71 more) | Complete text read and indexed |
| `EOIP-engg-doc-pkg/knowgridflow-product-architecture.md` | `.md` | 2010 | `FULLY_READ` | G2-P0, G2-P1, G2-P10, G2-P2, G2-P3, G2-P4, G2-P5, G2-P6, G2-P7, G2-P8, G2-P9 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/MANIFEST.sha256` | `.sha256` | 0 | `EXCLUDED` | - | binary office/checksum artifact; metadata inventoried, content not line-readable |
| `EOIP-engg-doc-pkg/memory.md` | `.md` | 326 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/MVP-implementation-plan.md` | `.md` | 590 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-003, FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CONN-002, FR-CONN-003, FR-CONN-004, ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/MVP-requirements.md` | `.md` | 275 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-003, FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CONN-002, FR-CONN-003, FR-CONN-004, ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/onboarding_checklist.md` | `.md` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/onboarding_prompts.md` | `.md` | 71 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/openapi/openapi-starter.json` | `.json` | 125 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/README.md` | `.md` | 89 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/adr-001-g2-contract-and-revision-model.md` | `.md` | 48 | `FULLY_READ` | G2-ARCH-001, G2-EKAF-003, G2-EVENT-001, G2-EVOL-009, G2-P2 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/agents.md` | `.md` | 214 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/api-reference.md` | `.md` | 293 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/benchmarking.md` | `.md` | 105 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/code-graph.md` | `.md` | 198 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/connectors-github.md` | `.md` | 85 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/connectors-gitlab.md` | `.md` | 109 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/connectors.md` | `.md` | 193 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/deep-agents-xai.md` | `.md` | 55 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/deployment-ha.md` | `.md` | 139 | `FULLY_READ` | GAP-HG-004, GAP-HG-006, GAP-HG-008, GAP-PERF-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/deployment-verification.md` | `.md` | 42 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/docker-local.md` | `.md` | 748 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/file-parsing.md` | `.md` | 195 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/g2-traceability.md` | `.md` | 78 | `FULLY_READ` | G2-ARCH-001, G2-EKAF-003, G2-EKAF-010, G2-EKAF-014, G2-EKAF-016, G2-EKAF-017, G2-EKAF-018, G2-EKAF-022, G2-EKAF-023, G2-... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/graph-algorithms.md` | `.md` | 210 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/hubble-local.md` | `.md` | 224 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/hubble-runtime-validation.md` | `.md` | 441 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/ingestion.md` | `.md` | 239 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/ontology.md` | `.md` | 249 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/query-engine.md` | `.md` | 220 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/rag.md` | `.md` | 196 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/reference/validation-evidence-phase1.md` | `.md` | 92 | `FULLY_READ` | MVP-FR-027 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles.md` | `.md` | 526 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/AIEngineer_tasks.md` | `.md` | 79 | `FULLY_READ` | AGENT-001, AGENT-002, AI-001, AI-002, AI-003, AI-005, AI-006, CORE-003, GRAPH-004, GRAPH-005, TASK-AIE-001, TASK-AIE-002... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/Architect_tasks.md` | `.md` | 105 | `FULLY_READ` | AGENT-003, AGENT-004, AI-006, CORE-001, CORE-002, CORE-003, CORE-004, GRAPH-001, GRAPH-005, INFRA-001, TASK-ARCH-001, TA... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/CEO_tasks.md` | `.md` | 125 | `FULLY_READ` | TASK-CEO-001, TASK-CEO-002, TASK-CEO-003, TASK-CEO-004, TASK-CEO-005, TASK-CEO-006, TASK-CEO-007, TASK-CEO-008, TASK-CEO... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/CTO_tasks.md` | `.md` | 144 | `FULLY_READ` | COMPLY-002, CORE-001, CORE-003, CORE-004, GRAPH-004, INFRA-001, INFRA-002, INFRA-003, INFRA-004, INFRA-006, INFRA-007, T... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/DeliveryManager_tasks.md` | `.md` | 118 | `FULLY_READ` | CORE-001, CORE-002, CORE-003, CORE-004, CORE-005, CORE-006, TASK-DM-001, TASK-DM-002, TASK-DM-003, TASK-DM-004, TASK-DM-... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/Developer_tasks.md` | `.md` | 102 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, CORE-001, CORE-002, CORE-003, CORE-004, CORE-005, CORE-006, GRAPH-001, GRAPH... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/LeadAIEngineer_tasks.md` | `.md` | 97 | `FULLY_READ` | AGENT-001, AGENT-002, AI-001, AI-003, AI-004, AI-005, AI-006, CORE-003, GRAPH-002, GRAPH-004, GRAPH-005, TASK-LAI-001 (+... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/LeadDeveloper_tasks.md` | `.md` | 97 | `FULLY_READ` | CORE-001, CORE-002, CORE-003, CORE-004, CORE-005, CORE-006, TASK-LD-001, TASK-LD-002, TASK-LD-003, TASK-LD-004, TASK-LD-... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/LegalCounsel_tasks.md` | `.md` | 101 | `FULLY_READ` | TASK-LEGAL-001, TASK-LEGAL-002, TASK-LEGAL-003, TASK-LEGAL-004, TASK-LEGAL-005, TASK-LEGAL-006, TASK-LEGAL-007, TASK-LEG... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/LicensingManager_tasks.md` | `.md` | 81 | `FULLY_READ` | CORE-001, TASK-LIC-001, TASK-LIC-002, TASK-LIC-003, TASK-LIC-004, TASK-LIC-005, TASK-LIC-006, TASK-LIC-007, TASK-LIC-008... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/MarketingExecutive_tasks.md` | `.md` | 71 | `FULLY_READ` | CORE-001, INFRA-006, TASK-MKE-001, TASK-MKE-002, TASK-MKE-003, TASK-MKE-004, TASK-MKE-005, TASK-MKE-006, TASK-MKE-007, T... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/MarketingManager_tasks.md` | `.md` | 100 | `FULLY_READ` | CORE-001, CORE-004, TASK-CEO-010, TASK-MKT-001, TASK-MKT-002, TASK-MKT-003, TASK-MKT-004, TASK-MKT-005, TASK-MKT-006, TA... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/QAEngineer_tasks.md` | `.md` | 74 | `FULLY_READ` | CORE-001, CORE-002, CORE-003, CORE-004, TASK-QA-001, TASK-QA-002, TASK-QA-003, TASK-QA-004, TASK-QA-005, TASK-QA-006, TA... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/QALead_tasks.md` | `.md` | 86 | `FULLY_READ` | TASK-QAL-001, TASK-QAL-002, TASK-QAL-003, TASK-QAL-004, TASK-QAL-005, TASK-QAL-006, TASK-QAL-007, TASK-QAL-008, TASK-QAL... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/roles_dashboard.html` | `.html` | 431 | `FULLY_READ` | COMPLY-001, COMPLY-002, CORE-001, CORE-002, CORE-003, CORE-004, CORE-005, CORE-006, GRAPH-005, INFRA-003, INFRA-004, INF... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/roles_index.md` | `.md` | 143 | `FULLY_READ` | INFRA-007, TEST-002, TEST-005, UI-002 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/roles/SecurityOfficer_tasks.md` | `.md` | 110 | `FULLY_READ` | COMPLY-001, COMPLY-002, COMPLY-003, CORE-001, CORE-002, INFRA-002, TASK-SEC-001, TASK-SEC-002, TASK-SEC-003, TASK-SEC-00... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/agent_request.schema.json` | `.json` | 53 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/agent_result.schema.json` | `.json` | 54 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/audit_event.schema.json` | `.json` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/evidence.schema.json` | `.json` | 47 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/graph_mutation.schema.json` | `.json` | 35 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/graph_result.schema.json` | `.json` | 35 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/memory_record.schema.json` | `.json` | 57 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/normalized_entity.schema.json` | `.json` | 48 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/normalized_relationship.schema.json` | `.json` | 52 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/query_plan.schema.json` | `.json` | 61 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/retrieval_result.schema.json` | `.json` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/source_event.schema.json` | `.json` | 46 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/tool_request.schema.json` | `.json` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/schemas/tool_result.schema.json` | `.json` | 32 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/source-master-prompt.txt` | `.txt` | 2374 | `FULLY_READ` | FR-AGENT-001, FR-CONN-001, FR-GRAPH-001, FR-MCP-001, FR-QUERY-001, FR-RAG-001, FR-UI-001, FR-VSCODE-001, MVP-FR-001, NFR... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/super-requirements.md` | `.md` | 1149 | `FULLY_READ` | FR-GRAPH-011, MVP-FR-001, MVP-FR-020, MVP-FR-028, NFR-MAINT-001, NFR-PERF-001, SR-AGT-001, SR-AGT-002, SR-AGT-003, SR-AG... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/requirements-map.md` | `.md` | 28 | `FULLY_READ` | MVP-FR-001, MVP-FR-027, MVP-FR-028, REQ-USER-IMPORT-001 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/ticket-20261004-001.md` | `.md` | 83 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/ticket-20261004-002.md` | `.md` | 61 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/ticket-20261004-003.md` | `.md` | 110 | `FULLY_READ` | MVP-FR-001, MVP-FR-028 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/ticket-20261004-004.md` | `.md` | 66 | `FULLY_READ` | MVP-FR-027 | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/ticket-20261004-005.md` | `.md` | 109 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/tickets/ticket-template.md` | `.md` | 38 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/todo-status.md` | `.md` | 25 | `FULLY_READ` | - | Complete text read and indexed |
| `EOIP-engg-doc-pkg/traceability/mvp-traceability.csv` | `.csv` | 29 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-003, FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CONN-002, FR-CONN-003, FR-CONN-004, ... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/traceability/requirements-traceability.csv` | `.csv` | 82 | `FULLY_READ` | AC-FR-ADMIN-001, AC-FR-ADMIN-002, AC-FR-AGENT-001, AC-FR-AGENT-002, AC-FR-AGENT-003, AC-FR-AGENT-004, AC-FR-AGENT-005, A... | Complete text read and indexed |
| `EOIP-engg-doc-pkg/traceability/requirements.json` | `.json` | 974 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, FR-CODE-001, FR-CODE-0... | Complete text read and indexed |
| `eoip-phase4-2-requirements.md` | `.md` | 2366 | `FULLY_READ` | AGENT-001, AGENT-001.1, AGENT-001.2, AGENT-001.3, AGENT-001.4, AGENT-001.5, AGENT-002, AGENT-002.1, AGENT-002.2, AGENT-0... | Complete text read and indexed |
| `eoip-phase4-2-tracker.html` | `.html` | 862 | `FULLY_READ` | AGENT-001, AGENT-001.1, AGENT-001.2, AGENT-001.3, AGENT-001.4, AGENT-001.5, AGENT-002, AGENT-002.1, AGENT-002.2, AGENT-0... | Complete text read and indexed |
| `gaps-audit-cp.md` | `.md` | 18505 | `FULLY_READ` | - | current audit deliverable; generated and verified after source inventory |
| `GUI-UIX-requirements.md` | `.md` | 1395 | `FULLY_READ` | - | current audit deliverable; generated and verified after source inventory |
| `kgf-completion-board.html` | `.html` | 612 | `FULLY_READ` | BASE-01, BASE-02, BASE-03, BASE-04, CG-CODE-01, CG-CODE-02, CG-DOC-01, CG-GAP-001, CG-GAP-002, CG-GAP-003, CG-GAP-004, C... | Complete text read and indexed |
| `KGF-MASTER-BACKLOG.md` | `.md` | 1334 | `FULLY_READ` | BASE-01, BASE-02, BASE-03, BASE-04, CG-CODE-01, CG-CODE-02, CG-DEV-2026-10-11, CG-DOC-01, CG-GAP-001, CG-GAP-002, CG-GAP... | Complete text read and indexed |
| `kgf-progress-2026-10-11.json.bak` | `.bak` | 0 | `EXCLUDED` | - | unsupported or binary file type |
| `kgf-progress-2026-10-12.json` | `.json` | 526 | `FULLY_READ` | BASE-01, BASE-02, BASE-03, BASE-04, CG-CODE-01, CG-CODE-02, CG-DOC-01, CG-GAP-001, CG-GAP-002, CG-GAP-003, CG-GAP-004, C... | Complete text read and indexed |
| `packages/eoip/__init__.py` | `.py` | 93 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/__main__.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/adapters/__init__.py` | `.py` | 23 | `FULLY_READ` | SR-GDB-002 | Complete text read and indexed |
| `packages/eoip/adapters/catalog.py` | `.py` | 130 | `FULLY_READ` | SR-GDB-002 | Complete text read and indexed |
| `packages/eoip/adapters/janusgraph.py` | `.py` | 405 | `FULLY_READ` | SR-GDB-003 | Complete text read and indexed |
| `packages/eoip/adapters/manifests.py` | `.py` | 677 | `FULLY_READ` | KGR-G-013, SR-GDB-002, SR-GDB-003, SR-GDB-004 | Complete text read and indexed |
| `packages/eoip/agentarch/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agentarch/base.py` | `.py` | 137 | `FULLY_READ` | GAP-ARCH-A-01 | Complete text read and indexed |
| `packages/eoip/agentarch/classical.py` | `.py` | 543 | `FULLY_READ` | GAP-ARCH-A-01, GAP-ARCH-A-02, GAP-ARCH-A-03, GAP-ARCH-A-04, GAP-ARCH-A-05, GAP-ARCH-A-06, GAP-ARCH-A-07, GAP-ARCH-A-08, ... | Complete text read and indexed |
| `packages/eoip/agentarch/enterprise.py` | `.py` | 654 | `FULLY_READ` | GAP-ARCH-C-01, GAP-ARCH-C-02, GAP-ARCH-C-03, GAP-ARCH-C-04, GAP-ARCH-C-05, GAP-ARCH-C-06, GAP-ARCH-C-07, GAP-ARCH-C-08, ... | Complete text read and indexed |
| `packages/eoip/agentarch/reasoning.py` | `.py` | 516 | `FULLY_READ` | GAP-ARCH-B-01, GAP-ARCH-B-02, GAP-ARCH-B-03, GAP-ARCH-B-04, GAP-ARCH-B-05, GAP-ARCH-B-06, GAP-ARCH-B-07, GAP-ARCH-B-08, ... | Complete text read and indexed |
| `packages/eoip/agents/__init__.py` | `.py` | 51 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/anomaly.py` | `.py` | 88 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/archetypes.py` | `.py` | 1415 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/blast_radius.py` | `.py` | 72 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/catalog.py` | `.py` | 95 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/community.py` | `.py` | 80 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/evaluation.py` | `.py` | 75 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/firewall.py` | `.py` | 124 | `FULLY_READ` | GAP-AGOV-006, GAP-AGOV-007, GAP-KFW-001, GAP-KFW-002, GAP-KFW-003, GAP-KFW-004, GAP-KFW-005, GAP-KFW-006, GAP-KFW-007, G... | Complete text read and indexed |
| `packages/eoip/agents/governed.py` | `.py` | 334 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/graph_analytics.py` | `.py` | 268 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/incident_correlation.py` | `.py` | 170 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/loops.py` | `.py` | 326 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/mcp_pr_tools.py` | `.py` | 411 | `FULLY_READ` | KGR-G-017 | Complete text read and indexed |
| `packages/eoip/agents/memory.py` | `.py` | 367 | `FULLY_READ` | KGR-G-014 | Complete text read and indexed |
| `packages/eoip/agents/mesh_supervisor.py` | `.py` | 165 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/message_bus.py` | `.py` | 271 | `FULLY_READ` | AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/orchestration.py` | `.py` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/proposals.py` | `.py` | 76 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/runtime.py` | `.py` | 602 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/semantic_index.py` | `.py` | 76 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/similarity.py` | `.py` | 89 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/test_coverage.py` | `.py` | 128 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/tools.py` | `.py` | 151 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/trace.py` | `.py` | 53 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/agents/trace_impact.py` | `.py` | 132 | `FULLY_READ` | FR-AGENT-003 | Complete text read and indexed |
| `packages/eoip/agents/uncertainty_protocol.py` | `.py` | 342 | `FULLY_READ` | KGR-G-019 | Complete text read and indexed |
| `packages/eoip/analytics/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/analytics/algorithms.py` | `.py` | 527 | `FULLY_READ` | KGR-G-004 | Complete text read and indexed |
| `packages/eoip/analytics/parallel_multihop.py` | `.py` | 393 | `FULLY_READ` | KGR-G-018 | Complete text read and indexed |
| `packages/eoip/analytics/service.py` | `.py` | 317 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/audit/__init__.py` | `.py` | 6 | `FULLY_READ` | NFR-OPS-001 | Complete text read and indexed |
| `packages/eoip/audit/redaction.py` | `.py` | 39 | `FULLY_READ` | NFR-OPS-001 | Complete text read and indexed |
| `packages/eoip/audit/sink.py` | `.py` | 130 | `FULLY_READ` | NFR-OPS-001, NFR-SEC-007 | Complete text read and indexed |
| `packages/eoip/audit/xai_ledger.py` | `.py` | 167 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/authn/__init__.py` | `.py` | 788 | `FULLY_READ` | GAP-SEC-001, GAP-SEC-002, GAP-SEC-003, GAP-SEC-004, NFR-OPS-001 | Complete text read and indexed |
| `packages/eoip/authn/oauth_sso.py` | `.py` | 276 | `FULLY_READ` | INFRA-002 | Complete text read and indexed |
| `packages/eoip/authz/__init__.py` | `.py` | 63 | `FULLY_READ` | GAP-SEC-001 | Complete text read and indexed |
| `packages/eoip/authz/core.py` | `.py` | 411 | `FULLY_READ` | GAP-SEC-001, GAP-SEC-002, GAP-SEC-003, GAP-SEC-004, GAP-SEC-005, GAP-SEC-006 | Complete text read and indexed |
| `packages/eoip/authz/security_router.py` | `.py` | 156 | `FULLY_READ` | GAP-SEC-008, GAP-SEC-009, GAP-SEC-010, GAP-SEC-011, GAP-SEC-012 | Complete text read and indexed |
| `packages/eoip/authz/tokens.py` | `.py` | 224 | `FULLY_READ` | GAP-SEC-007, GAP-SEC-008, GAP-SEC-009, GAP-SEC-010, GAP-SEC-011 | Complete text read and indexed |
| `packages/eoip/billing/metering.py` | `.py` | 88 | `FULLY_READ` | MS-27 | Complete text read and indexed |
| `packages/eoip/brain/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/adaptive_learning.py` | `.py` | 217 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/brain_os.py` | `.py` | 579 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/cognitive_narrator.py` | `.py` | 622 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/correlation_engine.py` | `.py` | 262 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/graph_intelligence.py` | `.py` | 583 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/learning_engine.py` | `.py` | 457 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/living_brain_algorithms.py` | `.py` | 358 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/nl_config.py` | `.py` | 284 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/predictive_analytics.py` | `.py` | 334 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/report_generator.py` | `.py` | 492 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/brain/router.py` | `.py` | 476 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/branding/__init__.py` | `.py` | 58 | `FULLY_READ` | SR-ONT-007, SR-WL-001 | Complete text read and indexed |
| `packages/eoip/branding/content.py` | `.py` | 82 | `FULLY_READ` | SR-WL-007 | Complete text read and indexed |
| `packages/eoip/branding/devendoring.py` | `.py` | 85 | `FULLY_READ` | SR-WL-004 | Complete text read and indexed |
| `packages/eoip/branding/localization.py` | `.py` | 88 | `FULLY_READ` | SR-WL-006 | Complete text read and indexed |
| `packages/eoip/branding/router.py` | `.py` | 68 | `FULLY_READ` | SR-ONT-007, SR-WL-001 | Complete text read and indexed |
| `packages/eoip/branding/terminology.py` | `.py` | 87 | `FULLY_READ` | SR-ONT-007, SR-WL-003 | Complete text read and indexed |
| `packages/eoip/branding/theme.py` | `.py` | 233 | `FULLY_READ` | SR-WL-001, SR-WL-003 | Complete text read and indexed |
| `packages/eoip/catalog/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/catalog/products.py` | `.py` | 319 | `FULLY_READ` | FR-GRAPH-001, GAP-KP-001, GAP-KP-002, GAP-KP-003, GAP-KP-004, GAP-KP-005 | Complete text read and indexed |
| `packages/eoip/causal/__init__.py` | `.py` | 19 | `FULLY_READ` | GRAPH-002 | Complete text read and indexed |
| `packages/eoip/causal/engine.py` | `.py` | 234 | `FULLY_READ` | GRAPH-002 | Complete text read and indexed |
| `packages/eoip/ci/__init__.py` | `.py` | 35 | `FULLY_READ` | GAP-KGCI-001 | Complete text read and indexed |
| `packages/eoip/ci/__main__.py` | `.py` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ci/pipeline.py` | `.py` | 559 | `FULLY_READ` | FR-VALID-003, GAP-KGCI-001, GAP-KGCI-002, GAP-KGCI-003, GAP-KGCI-004 | Complete text read and indexed |
| `packages/eoip/cli.py` | `.py` | 36 | `FULLY_READ` | KGR-G-012 | Complete text read and indexed |
| `packages/eoip/codegraph/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/codegraph/diff_hunk.py` | `.py` | 133 | `FULLY_READ` | FR-CODE-003 | Complete text read and indexed |
| `packages/eoip/codegraph/languages/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/codegraph/parser.py` | `.py` | 229 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/collaboration/__init__.py` | `.py` | 50 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/collaboration/activity.py` | `.py` | 162 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/collaboration/annotations.py` | `.py` | 254 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/collaboration/router.py` | `.py` | 412 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/collaboration/shared_queries.py` | `.py` | 236 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/collaboration/workspaces.py` | `.py` | 210 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/compliance/__init__.py` | `.py` | 72 | `FULLY_READ` | SR-GOV-001, SR-GOV-002, SR-GOV-003, SR-GOV-004, SR-GOV-005 | Complete text read and indexed |
| `packages/eoip/compliance/ai.py` | `.py` | 187 | `FULLY_READ` | SR-GOV-002 | Complete text read and indexed |
| `packages/eoip/compliance/change.py` | `.py` | 156 | `FULLY_READ` | SR-GOV-003 | Complete text read and indexed |
| `packages/eoip/compliance/constraints.py` | `.py` | 277 | `FULLY_READ` | COMPLY-001 | Complete text read and indexed |
| `packages/eoip/compliance/dashboard.py` | `.py` | 310 | `FULLY_READ` | COMPLY-003 | Complete text read and indexed |
| `packages/eoip/compliance/exceptions.py` | `.py` | 124 | `FULLY_READ` | SR-GOV-005 | Complete text read and indexed |
| `packages/eoip/compliance/extended_packs.py` | `.py` | 255 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/compliance/pack.py` | `.py` | 265 | `FULLY_READ` | SR-GOV-001 | Complete text read and indexed |
| `packages/eoip/compliance/packs.py` | `.py` | 286 | `FULLY_READ` | SR-GOV-001, SR-GOV-002, SR-GOV-004, SR-GOV-005 | Complete text read and indexed |
| `packages/eoip/compliance/roles.py` | `.py` | 102 | `FULLY_READ` | SR-GOV-003, SR-GOV-004 | Complete text read and indexed |
| `packages/eoip/compliance/router.py` | `.py` | 175 | `FULLY_READ` | SR-GOV-001, SR-GOV-002, SR-GOV-003, SR-GOV-004, SR-GOV-005 | Complete text read and indexed |
| `packages/eoip/config/__init__.py` | `.py` | 70 | `FULLY_READ` | SR-CFG-001, SR-CFG-003, SR-CFG-004, SR-CFG-005, SR-CFG-006 | Complete text read and indexed |
| `packages/eoip/config/_yaml.py` | `.py` | 43 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/config/ascode.py` | `.py` | 276 | `FULLY_READ` | SR-CFG-001, SR-CFG-002, SR-CFG-004 | Complete text read and indexed |
| `packages/eoip/config/layered.py` | `.py` | 705 | `FULLY_READ` | SR-CFG-001, SR-CFG-002, SR-CFG-003, SR-CFG-005, SR-CFG-006, SR-TEN-001 | Complete text read and indexed |
| `packages/eoip/config/router.py` | `.py` | 202 | `FULLY_READ` | SR-CFG-001, SR-CFG-002, SR-CFG-003, SR-CFG-004, SR-CFG-005, SR-CFG-006, SR-TEN-001 | Complete text read and indexed |
| `packages/eoip/connectors/__init__.py` | `.py` | 50 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/acquisition.py` | `.py` | 295 | `FULLY_READ` | G2-T0201 | Complete text read and indexed |
| `packages/eoip/connectors/api_portal.py` | `.py` | 163 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/base.py` | `.py` | 68 | `FULLY_READ` | FR-CONN-001, G2-T0005 | Complete text read and indexed |
| `packages/eoip/connectors/cicd.py` | `.py` | 214 | `FULLY_READ` | G2-SRC-CICD-001 | Complete text read and indexed |
| `packages/eoip/connectors/config.py` | `.py` | 185 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/conflicts.py` | `.py` | 86 | `FULLY_READ` | G2-EKAF-022 | Complete text read and indexed |
| `packages/eoip/connectors/confluence.py` | `.py` | 253 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/confluence_body.py` | `.py` | 169 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/confluence_metadata.py` | `.py` | 141 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/crawler.py` | `.py` | 258 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/datadog.py` | `.py` | 236 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/drift.py` | `.py` | 193 | `FULLY_READ` | G2-EKAF-017, G2-EKAF-018 | Complete text read and indexed |
| `packages/eoip/connectors/errors.py` | `.py` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/factory.py` | `.py` | 1135 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/figma.py` | `.py` | 211 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/files.py` | `.py` | 104 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/generic.py` | `.py` | 180 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/github.py` | `.py` | 353 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/gitlab.py` | `.py` | 572 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/gitlab_json.py` | `.py` | 103 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/grafana.py` | `.py` | 192 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/jira.py` | `.py` | 513 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/jira_json.py` | `.py` | 125 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/kibana.py` | `.py` | 124 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/kubernetes.py` | `.py` | 279 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/local_code.py` | `.py` | 58 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/otel.py` | `.py` | 182 | `FULLY_READ` | G2-SRC-OTEL-001 | Complete text read and indexed |
| `packages/eoip/connectors/qtest.py` | `.py` | 129 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/rally.py` | `.py` | 145 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/reconciliation.py` | `.py` | 81 | `FULLY_READ` | G2-T0250 | Complete text read and indexed |
| `packages/eoip/connectors/registry.py` | `.py` | 100 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/rest.py` | `.py` | 174 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/runtime_infra.py` | `.py` | 166 | `FULLY_READ` | G2-SRC-RUNTIME-001 | Complete text read and indexed |
| `packages/eoip/connectors/sbom.py` | `.py` | 214 | `FULLY_READ` | G2-SRC-SBOM-001 | Complete text read and indexed |
| `packages/eoip/connectors/servicenow.py` | `.py` | 140 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/sync.py` | `.py` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/connectors/webhook.py` | `.py` | 112 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/context/__init__.py` | `.py` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/context/engine.py` | `.py` | 189 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/context/graph_slicing.py` | `.py` | 222 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/contracts/__init__.py` | `.py` | 58 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/contracts/agent.py` | `.py` | 177 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/contracts/audit.py` | `.py` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/contracts/evidence.py` | `.py` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/contracts/graph_mutation.py` | `.py` | 26 | `FULLY_READ` | FR-INGEST-001 | Complete text read and indexed |
| `packages/eoip/contracts/graph_result.py` | `.py` | 53 | `FULLY_READ` | FR-QUERY-002, FR-QUERY-003, FR-QUERY-007 | Complete text read and indexed |
| `packages/eoip/contracts/memory.py` | `.py` | 23 | `FULLY_READ` | FR-MEM-001 | Complete text read and indexed |
| `packages/eoip/contracts/normalized.py` | `.py` | 38 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/contracts/query_plan.py` | `.py` | 25 | `FULLY_READ` | FR-QUERY-001, FR-QUERY-005, FR-QUERY-008 | Complete text read and indexed |
| `packages/eoip/contracts/retrieval.py` | `.py` | 30 | `FULLY_READ` | GAP-RET-006 | Complete text read and indexed |
| `packages/eoip/contracts/revision.py` | `.py` | 54 | `FULLY_READ` | G2-EVOL-009, G2-T0003 | Complete text read and indexed |
| `packages/eoip/contracts/source_event.py` | `.py` | 135 | `FULLY_READ` | FR-INGEST-001 | Complete text read and indexed |
| `packages/eoip/contracts/source_registry.py` | `.py` | 135 | `FULLY_READ` | G2-T0004, G2-T0005 | Complete text read and indexed |
| `packages/eoip/contracts/tool.py` | `.py` | 51 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/copilot/__init__.py` | `.py` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/copilot/engine.py` | `.py` | 510 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/cost_optimization/__init__.py` | `.py` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/cost_optimization/engine.py` | `.py` | 277 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/dashboards/__init__.py` | `.py` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/dashboards/builder.py` | `.py` | 279 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/demo.py` | `.py` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/demo_scenarios.py` | `.py` | 197 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/distillation/__init__.py` | `.py` | 19 | `FULLY_READ` | GRAPH-003 | Complete text read and indexed |
| `packages/eoip/distillation/engine.py` | `.py` | 246 | `FULLY_READ` | GRAPH-003 | Complete text read and indexed |
| `packages/eoip/edge/__init__.py` | `.py` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/edge/runtime.py` | `.py` | 384 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/egress/__init__.py` | `.py` | 80 | `FULLY_READ` | SR-CON-010, SR-LLM-010 | Complete text read and indexed |
| `packages/eoip/egress/dlp.py` | `.py` | 152 | `FULLY_READ` | SR-LLM-014 | Complete text read and indexed |
| `packages/eoip/egress/gateway.py` | `.py` | 346 | `FULLY_READ` | SR-LLM-010, SR-LLM-011, SR-LLM-012, SR-LLM-013, SR-LLM-014, SR-LLM-015, SR-LLM-016, SR-LLM-017, SR-LLM-018, SR-LLM-019, ... | Complete text read and indexed |
| `packages/eoip/egress/manifest.py` | `.py` | 104 | `FULLY_READ` | SR-LLM-013 | Complete text read and indexed |
| `packages/eoip/egress/policy.py` | `.py` | 192 | `FULLY_READ` | SR-LLM-011, SR-LLM-017 | Complete text read and indexed |
| `packages/eoip/egress/provider.py` | `.py` | 148 | `FULLY_READ` | SR-CON-010, SR-CON-011, SR-CON-012, SR-LLM-017 | Complete text read and indexed |
| `packages/eoip/egress/router.py` | `.py` | 217 | `FULLY_READ` | SR-CON-010, SR-CON-011, SR-LLM-010, SR-LLM-011, SR-LLM-012, SR-LLM-013, SR-LLM-016 | Complete text read and indexed |
| `packages/eoip/egress/transforms.py` | `.py` | 170 | `FULLY_READ` | SR-LLM-011, SR-LLM-012, SR-LLM-015 | Complete text read and indexed |
| `packages/eoip/egress/vault.py` | `.py` | 112 | `FULLY_READ` | SR-CON-012, SR-LLM-015 | Complete text read and indexed |
| `packages/eoip/embeddings/__init__.py` | `.py` | 25 | `FULLY_READ` | AI-006 | Complete text read and indexed |
| `packages/eoip/embeddings/engine.py` | `.py` | 259 | `FULLY_READ` | AI-006 | Complete text read and indexed |
| `packages/eoip/enterprise/__init__.py` | `.py` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/advanced_router.py` | `.py` | 174 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/audit.py` | `.py` | 192 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/cache.py` | `.py` | 280 | `FULLY_READ` | INFRA-001 | Complete text read and indexed |
| `packages/eoip/enterprise/circuit_breaker.py` | `.py` | 188 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/config.py` | `.py` | 131 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/container_runtime.py` | `.py` | 194 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/exceptions.py` | `.py` | 261 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/feature_flags.py` | `.py` | 151 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/health.py` | `.py` | 210 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/lifecycle.py` | `.py` | 170 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/logging.py` | `.py` | 72 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/middleware.py` | `.py` | 92 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/models.py` | `.py` | 309 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/observability.py` | `.py` | 124 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/plugin.py` | `.py` | 181 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/rate_limiter.py` | `.py` | 109 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/retry.py` | `.py` | 133 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/router.py` | `.py` | 725 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/enterprise/webhooks.py` | `.py` | 226 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/evaluation/__init__.py` | `.py` | 28 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/evaluation/distillation_sentinel.py` | `.py` | 165 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/evaluation/engine.py` | `.py` | 315 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/events/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/events/emitter.py` | `.py` | 93 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/exporters/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/exporters/obsidian_vault.py` | `.py` | 358 | `FULLY_READ` | KGR-G-003 | Complete text read and indexed |
| `packages/eoip/extraction/__init__.py` | `.py` | 37 | `FULLY_READ` | AGENT-002, AI-003 | Complete text read and indexed |
| `packages/eoip/extraction/engine.py` | `.py` | 333 | `FULLY_READ` | AGENT-002 | Complete text read and indexed |
| `packages/eoip/extraction/relation_extractor.py` | `.py` | 148 | `FULLY_READ` | AGENT-002, AI-003 | Complete text read and indexed |
| `packages/eoip/features/__init__.py` | `.py` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/features/engine.py` | `.py` | 253 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/federation/__init__.py` | `.py` | 57 | `FULLY_READ` | GAP-FABRIC-001, GRAPH-001 | Complete text read and indexed |
| `packages/eoip/federation/engine.py` | `.py` | 227 | `FULLY_READ` | GRAPH-001 | Complete text read and indexed |
| `packages/eoip/federation/planner.py` | `.py` | 1002 | `FULLY_READ` | GAP-FABRIC-001, GAP-FABRIC-002, GAP-FABRIC-003, GAP-FABRIC-004, GAP-FABRIC-005, GAP-FABRIC-006, GAP-FABRIC-007, GAP-FED-... | Complete text read and indexed |
| `packages/eoip/fileparse/__init__.py` | `.py` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/__main__.py` | `.py` | 52 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/api.py` | `.py` | 89 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/archives.py` | `.py` | 165 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/common.py` | `.py` | 105 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/contracts.py` | `.py` | 114 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/diagram_parser.py` | `.py` | 146 | `FULLY_READ` | MULTI-001 | Complete text read and indexed |
| `packages/eoip/fileparse/engine.py` | `.py` | 217 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/export.py` | `.py` | 97 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/media.py` | `.py` | 129 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/office.py` | `.py` | 131 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/text.py` | `.py` | 108 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/fileparse/tools.py` | `.py` | 72 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/future_scope.py` | `.py` | 861 | `FULLY_READ` | GAP-APP-001, GAP-APP-002, GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-005, GAP-CATALOG-001, GAP-CATALOG-002, GAP-CATALOG-003... | Complete text read and indexed |
| `packages/eoip/gaps/__init__.py` | `.py` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/gaps/coverage.py` | `.py` | 432 | `FULLY_READ` | GAP-CP-009, GAP-KGCI-001, GAP-KGCI-002, GAP-KGCI-003 | Complete text read and indexed |
| `packages/eoip/gaps/enterprise_completion.py` | `.py` | 483 | `FULLY_READ` | GAP-AGOV-001, GAP-AGOV-002, GAP-AGOV-003, GAP-AGOV-004, GAP-AGOV-005, GAP-AGOV-008, GAP-AGOV-009, GAP-AGOV-010, GAP-AGOV... | Complete text read and indexed |
| `packages/eoip/gaps/g2_architecture.py` | `.py` | 124 | `FULLY_READ` | G2-ARCH-001, G2-ARCH-002, G2-ARCH-003, G2-ARCH-004, G2-ARCH-005, G2-ARCH-006, G2-ARCH-007, G2-ARCH-008, G2-ARCH-009, G2-... | Complete text read and indexed |
| `packages/eoip/gaps/g2_observability.py` | `.py` | 127 | `FULLY_READ` | G2-GRAPH-OBS-002, G2-OBS-001, G2-OBS-002, G2-OBS-003, G2-OBS-004, G2-OBS-005, G2-OBS-006 | Complete text read and indexed |
| `packages/eoip/gaps/g2_readiness.py` | `.py` | 350 | `FULLY_READ` | G2-ADMIN-001, G2-ARCH-001, G2-ARCHC-001, G2-CAP-001, G2-CAUSE-001, G2-EKAF-001, G2-EVENT-001, G2-EVOL-001, G2-GRAPH-API-... | Complete text read and indexed |
| `packages/eoip/gnn/__init__.py` | `.py` | 23 | `FULLY_READ` | GRAPH-004 | Complete text read and indexed |
| `packages/eoip/gnn/engine.py` | `.py` | 300 | `FULLY_READ` | GRAPH-004 | Complete text read and indexed |
| `packages/eoip/graph/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/agent_router.py` | `.py` | 441 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/algorithms.py` | `.py` | 685 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/anomaly.py` | `.py` | 318 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/api_contracts.py` | `.py` | 182 | `FULLY_READ` | G2-GRAPH-API-001, G2-GRAPH-API-002, G2-GRAPH-API-003 | Complete text read and indexed |
| `packages/eoip/graph/backends.py` | `.py` | 309 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/benchmark.py` | `.py` | 237 | `FULLY_READ` | G2-PERF-002, GAP-HG-008, NFR-PERF-001 | Complete text read and indexed |
| `packages/eoip/graph/bitemporal.py` | `.py` | 388 | `FULLY_READ` | G2-P2, GAP-TEMP-001, GAP-TEMP-002, GAP-TEMP-003, GAP-TEMP-004, GAP-TEMP-005 | Complete text read and indexed |
| `packages/eoip/graph/business_intent.py` | `.py` | 282 | `FULLY_READ` | G2-GRAPH-BIZ-001, G2-I2R-004, G2-I2R-005, G2-T0620 | Complete text read and indexed |
| `packages/eoip/graph/capsules.py` | `.py` | 282 | `FULLY_READ` | G2-CAP-001, G2-CAP-005, G2-CAP-006 | Complete text read and indexed |
| `packages/eoip/graph/causal.py` | `.py` | 237 | `FULLY_READ` | G2-CAUSE-001, G2-T0920, G2-T0921, G2-T0923 | Complete text read and indexed |
| `packages/eoip/graph/community.py` | `.py` | 380 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/conformance.py` | `.py` | 267 | `FULLY_READ` | G2-ARCHC-001, G2-T0710 | Complete text read and indexed |
| `packages/eoip/graph/consumers.py` | `.py` | 131 | `FULLY_READ` | G2-T0242 | Complete text read and indexed |
| `packages/eoip/graph/database_adapters.py` | `.py` | 460 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/decisions.py` | `.py` | 173 | `FULLY_READ` | G2-GRAPH-DEC-001, G2-T0610 | Complete text read and indexed |
| `packages/eoip/graph/diff_engine.py` | `.py` | 217 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/documentation.py` | `.py` | 136 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/engineering.py` | `.py` | 404 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/evolution.py` | `.py` | 411 | `FULLY_READ` | G2-P2 | Complete text read and indexed |
| `packages/eoip/graph/expertise.py` | `.py` | 396 | `FULLY_READ` | GAP-FRESH-001, GAP-FRESH-002, GAP-FRESH-003, GAP-FRESH-004, GAP-FRESH-005, GAP-REC-001 | Complete text read and indexed |
| `packages/eoip/graph/format_converter.py` | `.py` | 418 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/hugegraph.py` | `.py` | 733 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/immune_system.py` | `.py` | 415 | `FULLY_READ` | G2-IMMUNE-001, G2-IMMUNE-002, G2-IMMUNE-003, G2-IMMUNE-004, G2-IMMUNE-005, G2-IMMUNE-006, G2-IMMUNE-007, G2-IMMUNE-008, ... | Complete text read and indexed |
| `packages/eoip/graph/knowledge_debt.py` | `.py` | 571 | `FULLY_READ` | G2-KD-001, G2-KD-003, G2-KD-004, G2-KD-005, G2-SLO-001 | Complete text read and indexed |
| `packages/eoip/graph/lens.py` | `.py` | 406 | `FULLY_READ` | G2-P10, G2-UX-LENS-001 | Complete text read and indexed |
| `packages/eoip/graph/materialized_views.py` | `.py` | 272 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/memory.py` | `.py` | 287 | `FULLY_READ` | FR-GRAPH-001 | Complete text read and indexed |
| `packages/eoip/graph/meta.py` | `.py` | 157 | `FULLY_READ` | FR-GRAPH-002, FR-GRAPH-005 | Complete text read and indexed |
| `packages/eoip/graph/metrics.py` | `.py` | 575 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/named_graph.py` | `.py` | 331 | `FULLY_READ` | KGR-G-013 | Complete text read and indexed |
| `packages/eoip/graph/neo4j.py` | `.py` | 392 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/neptune.py` | `.py` | 409 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/partitioning.py` | `.py` | 269 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/paths.py` | `.py` | 204 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/playback.py` | `.py` | 134 | `FULLY_READ` | G2-T1030, G2-T1032, G2-T1033 | Complete text read and indexed |
| `packages/eoip/graph/process_mining.py` | `.py` | 220 | `FULLY_READ` | G2-PM-001, G2-PM-002, G2-PM-003, G2-PM-004, G2-PM-005, G2-T0720, MS-16 | Complete text read and indexed |
| `packages/eoip/graph/query_operators.py` | `.py` | 430 | `FULLY_READ` | G2-QOP-001, G2-QOP-003, G2-QOP-005, G2-QOP-006, G2-QOP-007, G2-QOP-008, G2-QOP-009, G2-T0750 | Complete text read and indexed |
| `packages/eoip/graph/rag_router.py` | `.py` | 510 | `FULLY_READ` | GAP-KRAG-007, GAP-KRAG-008, GAP-KRAG-009 | Complete text read and indexed |
| `packages/eoip/graph/recommend.py` | `.py` | 171 | `FULLY_READ` | GAP-REC-001 | Complete text read and indexed |
| `packages/eoip/graph/rule_catalog.py` | `.py` | 67 | `FULLY_READ` | G2-ARCHC-002 | Complete text read and indexed |
| `packages/eoip/graph/runtime_topology.py` | `.py` | 96 | `FULLY_READ` | G2-GRAPH-RUNTIME-001, G2-GRAPH-RUNTIME-002, G2-GRAPH-RUNTIME-003 | Complete text read and indexed |
| `packages/eoip/graph/schema_migration.py` | `.py` | 256 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/security_graph.py` | `.py` | 91 | `FULLY_READ` | G2-GRAPH-SEC-001, G2-GRAPH-SEC-002, G2-GRAPH-SEC-003 | Complete text read and indexed |
| `packages/eoip/graph/similarity.py` | `.py` | 238 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/simulation.py` | `.py` | 481 | `FULLY_READ` | G2-SIM-001, G2-SIM-003, G2-SIM-004, G2-SIM-005, G2-SIM-006, G2-SIM-007, G2-T0901 | Complete text read and indexed |
| `packages/eoip/graph/snapshots.py` | `.py` | 206 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/store.py` | `.py` | 125 | `FULLY_READ` | NFR-MAINT-001 | Complete text read and indexed |
| `packages/eoip/graph/surprise.py` | `.py` | 180 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/test_intelligence.py` | `.py` | 131 | `FULLY_READ` | G2-T0601 | Complete text read and indexed |
| `packages/eoip/graph/traversal.py` | `.py` | 240 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph/twin.py` | `.py` | 260 | `FULLY_READ` | G2-T0630, G2-TWIN-001, G2-TWIN-003, G2-TWIN-004, MS-23 | Complete text read and indexed |
| `packages/eoip/graph/vector_graph.py` | `.py` | 423 | `FULLY_READ` | KGR-G-016 | Complete text read and indexed |
| `packages/eoip/graph/whatif.py` | `.py` | 320 | `FULLY_READ` | G2-T0910 | Complete text read and indexed |
| `packages/eoip/graph_graph/__init__.py` | `.py` | 19 | `FULLY_READ` | CORE-004 | Complete text read and indexed |
| `packages/eoip/graph_graph/engine.py` | `.py` | 299 | `FULLY_READ` | CORE-004 | Complete text read and indexed |
| `packages/eoip/graph_loop/__init__.py` | `.py` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graph_loop/engine.py` | `.py` | 184 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graphtest/__init__.py` | `.py` | 30 | `FULLY_READ` | GAP-GRAPHTEST-001 | Complete text read and indexed |
| `packages/eoip/graphtest/__main__.py` | `.py` | 30 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/graphtest/framework.py` | `.py` | 552 | `FULLY_READ` | GAP-GRAPHTEST-001, GAP-GRAPHTEST-002, GAP-GRAPHTEST-003, GAP-GRAPHTEST-004 | Complete text read and indexed |
| `packages/eoip/ha.py` | `.py` | 140 | `FULLY_READ` | GAP-HA-001 | Complete text read and indexed |
| `packages/eoip/harness/__init__.py` | `.py` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/harness/engine.py` | `.py` | 333 | `FULLY_READ` | AGENT-004 | Complete text read and indexed |
| `packages/eoip/health/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/health/aggregator.py` | `.py` | 232 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/identity/__init__.py` | `.py` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/identity/candidates.py` | `.py` | 124 | `FULLY_READ` | FR-ID-002, GAP-ER-001 | Complete text read and indexed |
| `packages/eoip/identity/resolver.py` | `.py` | 87 | `FULLY_READ` | FR-ID-001, FR-INGEST-002 | Complete text read and indexed |
| `packages/eoip/imports/__init__.py` | `.py` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/imports/engine.py` | `.py` | 402 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/incidents/__init__.py` | `.py` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/incidents/manager.py` | `.py` | 364 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingest/__init__.py` | `.py` | 6 | `FULLY_READ` | SR-ING-010 | Complete text read and indexed |
| `packages/eoip/ingest/incremental_crawler.py` | `.py` | 109 | `FULLY_READ` | G2-PERF-006, G2-PERF-007, G2-PERF-008 | Complete text read and indexed |
| `packages/eoip/ingest/profile.py` | `.py` | 1023 | `FULLY_READ` | SR-ING-010, SR-ING-012, SR-ING-013, SR-ING-014, SR-ING-016, SR-ING-020 | Complete text read and indexed |
| `packages/eoip/ingestion/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/batch_streaming.py` | `.py` | 291 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/code.py` | `.py` | 334 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/code_graph_json.py` | `.py` | 114 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/dlq.py` | `.py` | 84 | `FULLY_READ` | FR-INGEST-005 | Complete text read and indexed |
| `packages/eoip/ingestion/dlq_dashboard.py` | `.py` | 207 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/files.py` | `.py` | 197 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/github.py` | `.py` | 518 | `FULLY_READ` | G2-SRC-GH-001 | Complete text read and indexed |
| `packages/eoip/ingestion/gitlab.py` | `.py` | 255 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/gitlab_rest.py` | `.py` | 767 | `FULLY_READ` | G2-SRC-GL-001 | Complete text read and indexed |
| `packages/eoip/ingestion/incremental_indexer.py` | `.py` | 618 | `FULLY_READ` | KGR-G-012 | Complete text read and indexed |
| `packages/eoip/ingestion/jira.py` | `.py` | 307 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/jira_rest.py` | `.py` | 838 | `FULLY_READ` | G2-SRC-JIRA-001 | Complete text read and indexed |
| `packages/eoip/ingestion/json_processor.py` | `.py` | 321 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/multimodal_audio.py` | `.py` | 386 | `FULLY_READ` | KGR-G-002 | Complete text read and indexed |
| `packages/eoip/ingestion/pipeline.py` | `.py` | 230 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/polyglot_linker.py` | `.py` | 481 | `FULLY_READ` | KGR-G-001 | Complete text read and indexed |
| `packages/eoip/ingestion/replay.py` | `.py` | 216 | `FULLY_READ` | FR-CONN-006 | Complete text read and indexed |
| `packages/eoip/ingestion/repository.py` | `.py` | 446 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/semantic_pipeline.py` | `.py` | 285 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ingestion/source_sync.py` | `.py` | 611 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/integrations/__init__.py` | `.py` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/integrations/bus.py` | `.py` | 324 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/intelligence/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/intelligence/laya.py` | `.py` | 208 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/intelligence_eng/__init__.py` | `.py` | 50 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/intelligence_eng/engine.py` | `.py` | 1154 | `FULLY_READ` | CORE-005 | Complete text read and indexed |
| `packages/eoip/jobs.py` | `.py` | 75 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/licensing/__init__.py` | `.py` | 59 | `FULLY_READ` | SR-COM-001, SR-DEP-007, SR-TEN-009 | Complete text read and indexed |
| `packages/eoip/licensing/api.py` | `.py` | 94 | `FULLY_READ` | SR-DEP-007, SR-TEN-009 | Complete text read and indexed |
| `packages/eoip/licensing/cli.py` | `.py` | 78 | `FULLY_READ` | SR-DEP-007 | Complete text read and indexed |
| `packages/eoip/licensing/entitlements.py` | `.py` | 257 | `FULLY_READ` | SR-COM-001, SR-DEP-007 | Complete text read and indexed |
| `packages/eoip/licensing/license_file.py` | `.py` | 180 | `FULLY_READ` | SR-COM-001, SR-DEP-007 | Complete text read and indexed |
| `packages/eoip/licensing/meter.py` | `.py` | 156 | `FULLY_READ` | SR-DEP-007, SR-TEN-009 | Complete text read and indexed |
| `packages/eoip/loops/__init__.py` | `.py` | 93 | `FULLY_READ` | GAP-LOOP-001, GAP-LOOP-033 | Complete text read and indexed |
| `packages/eoip/loops/approval.py` | `.py` | 320 | `FULLY_READ` | GAP-LOOP-033, GAP-LOOP-034 | Complete text read and indexed |
| `packages/eoip/loops/core.py` | `.py` | 653 | `FULLY_READ` | FR-AGENT-002, GAP-LOOP-001, GAP-LOOP-006, GAP-LOOP-007 | Complete text read and indexed |
| `packages/eoip/loops/drivers.py` | `.py` | 261 | `FULLY_READ` | GAP-LOOP-010, GAP-LOOP-011, GAP-LOOP-012, GAP-LOOP-013, GAP-LOOP-014, GAP-LOOP-015, GAP-LOOP-016, GAP-LOOP-017, GAP-LOOP... | Complete text read and indexed |
| `packages/eoip/loops/router.py` | `.py` | 195 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/maintenance/__init__.py` | `.py` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/maintenance/autonomous.py` | `.py` | 339 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/marketplace/__init__.py` | `.py` | 86 | `FULLY_READ` | GAP-EXT-001, GAP-MKT-001 | Complete text read and indexed |
| `packages/eoip/marketplace/installer.py` | `.py` | 142 | `FULLY_READ` | GAP-MKT-004, GAP-MKT-005, GAP-MKT-006, GAP-MKT-007 | Complete text read and indexed |
| `packages/eoip/marketplace/manifest.py` | `.py` | 75 | `FULLY_READ` | GAP-MKT-001, GAP-MKT-002, GAP-MKT-004 | Complete text read and indexed |
| `packages/eoip/marketplace/packager.py` | `.py` | 277 | `FULLY_READ` | GAP-MKT-002, GAP-MKT-003, GAP-MKT-004, GAP-MKT-005, GAP-MKT-006 | Complete text read and indexed |
| `packages/eoip/marketplace/registry.py` | `.py` | 118 | `FULLY_READ` | GAP-MKT-006, GAP-MKT-008 | Complete text read and indexed |
| `packages/eoip/marketplace/sample.py` | `.py` | 33 | `FULLY_READ` | GAP-MKT-003 | Complete text read and indexed |
| `packages/eoip/marketplace/semver.py` | `.py` | 129 | `FULLY_READ` | GAP-MKT-004 | Complete text read and indexed |
| `packages/eoip/marketplace/signing.py` | `.py` | 76 | `FULLY_READ` | GAP-EXT-001, GAP-MKT-007, GAP-MKT-008 | Complete text read and indexed |
| `packages/eoip/memory_eng/__init__.py` | `.py` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/memory_eng/engine.py` | `.py` | 414 | `FULLY_READ` | MULTI-002 | Complete text read and indexed |
| `packages/eoip/mlops/__init__.py` | `.py` | 23 | `FULLY_READ` | AI-005 | Complete text read and indexed |
| `packages/eoip/mlops/experiment_tracker.py` | `.py` | 287 | `FULLY_READ` | AI-005 | Complete text read and indexed |
| `packages/eoip/model_management/__init__.py` | `.py` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/model_management/ai_ml_ops.py` | `.py` | 689 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/model_management/registry.py` | `.py` | 594 | `FULLY_READ` | AI-004 | Complete text read and indexed |
| `packages/eoip/models/__init__.py` | `.py` | 49 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/models/embeddings.py` | `.py` | 175 | `FULLY_READ` | GAP-SEARCH-001, H-02 | Complete text read and indexed |
| `packages/eoip/models/governance.py` | `.py` | 390 | `FULLY_READ` | GAP-AGOV-012 | Complete text read and indexed |
| `packages/eoip/models/provider.py` | `.py` | 91 | `FULLY_READ` | FR-RAG-002 | Complete text read and indexed |
| `packages/eoip/models/self_llm.py` | `.py` | 626 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/__init__.py` | `.py` | 36 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/bitemporal_state_machine.py` | `.py` | 360 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/causal_simulator.py` | `.py` | 186 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/collaborative_crdt.py` | `.py` | 217 | `FULLY_READ` | MS-12 | Complete text read and indexed |
| `packages/eoip/moonshot/compliance_twin.py` | `.py` | 272 | `FULLY_READ` | AI-ACT-ART-12, AI-ACT-ART-13, AI-ACT-ART-14, AI-ACT-ART-15 | Complete text read and indexed |
| `packages/eoip/moonshot/confidential_graph.py` | `.py` | 245 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/federated_graph.py` | `.py` | 116 | `FULLY_READ` | MS-18, NFR-SEC-001 | Complete text read and indexed |
| `packages/eoip/moonshot/generative_studio.py` | `.py` | 198 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/gfm_runtime.py` | `.py` | 116 | `FULLY_READ` | MS-29 | Complete text read and indexed |
| `packages/eoip/moonshot/health_dashboard.py` | `.py` | 110 | `FULLY_READ` | MS-24 | Complete text read and indexed |
| `packages/eoip/moonshot/live_causal_engine.py` | `.py` | 187 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/lom_finetune.py` | `.py` | 151 | `FULLY_READ` | MS-15 | Complete text read and indexed |
| `packages/eoip/moonshot/neuro_symbolic_memory.py` | `.py` | 176 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/ocel_fusion.py` | `.py` | 135 | `FULLY_READ` | MS-30 | Complete text read and indexed |
| `packages/eoip/moonshot/ontology_induction.py` | `.py` | 409 | `FULLY_READ` | KGR-G-015 | Complete text read and indexed |
| `packages/eoip/moonshot/quantum_optimizer.py` | `.py` | 197 | `FULLY_READ` | MS-22 | Complete text read and indexed |
| `packages/eoip/moonshot/router.py` | `.py` | 178 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/self_healing.py` | `.py` | 208 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/moonshot/sentinel.py` | `.py` | 133 | `FULLY_READ` | MS-21 | Complete text read and indexed |
| `packages/eoip/moonshot/spatial_lod_canvas.py` | `.py` | 121 | `FULLY_READ` | MS-6 | Complete text read and indexed |
| `packages/eoip/moonshot/streaming_agent_memory.py` | `.py` | 238 | `FULLY_READ` | KGR-G-014 | Complete text read and indexed |
| `packages/eoip/moonshot/universal_transpiler.py` | `.py` | 172 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/nlp/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/nlp/pipeline.py` | `.py` | 596 | `FULLY_READ` | AI-002 | Complete text read and indexed |
| `packages/eoip/notifications/__init__.py` | `.py` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/notifications/hub.py` | `.py` | 357 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/observability/__init__.py` | `.py` | 69 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/observability/logging.py` | `.py` | 158 | `FULLY_READ` | INFRA-004 | Complete text read and indexed |
| `packages/eoip/observability/metrics.py` | `.py` | 231 | `FULLY_READ` | GAP-OBS-003 | Complete text read and indexed |
| `packages/eoip/observability/otel.py` | `.py` | 108 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ontology/__init__.py` | `.py` | 21 | `FULLY_READ` | GRAPH-006 | Complete text read and indexed |
| `packages/eoip/ontology/domain_pack_manager.py` | `.py` | 323 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ontology/drift.py` | `.py` | 152 | `FULLY_READ` | G2-OEVO-001 | Complete text read and indexed |
| `packages/eoip/ontology/embedding_drift.py` | `.py` | 134 | `FULLY_READ` | GAP-DRIFT-005 | Complete text read and indexed |
| `packages/eoip/ontology/gitops.py` | `.py` | 793 | `FULLY_READ` | GAP-GITOPS-001, GAP-GITOPS-002, GAP-GITOPS-003, GAP-GITOPS-004, GAP-GITOPS-005, GAP-GITOPS-006, GAP-GITOPS-007, GAP-GITO... | Complete text read and indexed |
| `packages/eoip/ontology/gitops_router.py` | `.py` | 376 | `FULLY_READ` | GAP-GITOPS-002, GAP-GITOPS-003, GAP-GITOPS-004, GAP-GITOPS-005, GAP-GITOPS-006, GAP-GITOPS-007, GAP-GITOPS-008, GAP-MKT-... | Complete text read and indexed |
| `packages/eoip/ontology/industry_templates.py` | `.py` | 139 | `FULLY_READ` | GAP-MKT-003, GAP-MKT-006 | Complete text read and indexed |
| `packages/eoip/ontology/manifest.py` | `.py` | 505 | `FULLY_READ` | FR-GRAPH-008, FR-INGEST-003, FR-ONTO-001, FR-ONTO-002, FR-VALID-002, GAP-KP-001 | Complete text read and indexed |
| `packages/eoip/ontology/packs.py` | `.py` | 326 | `FULLY_READ` | GAP-DP-001, GAP-DP-002, GAP-DP-003, GAP-DP-004, GAP-DP-005 | Complete text read and indexed |
| `packages/eoip/ontology/rdf.py` | `.py` | 700 | `FULLY_READ` | GRAPH-006 | Complete text read and indexed |
| `packages/eoip/ontology/schema_gen.py` | `.py` | 127 | `FULLY_READ` | GAP-STUDIO-011 | Complete text read and indexed |
| `packages/eoip/ontology/shacl_validator.py` | `.py` | 194 | `FULLY_READ` | GRAPH-006 | Complete text read and indexed |
| `packages/eoip/ontology/skos.py` | `.py` | 450 | `FULLY_READ` | GAP-GOV-003, GAP-STUDIO-005, GAP-TAX-001 | Complete text read and indexed |
| `packages/eoip/ontology/stewardship.py` | `.py` | 151 | `FULLY_READ` | GAP-GITOPS-002, GAP-GITOPS-007 | Complete text read and indexed |
| `packages/eoip/ontology/studio.py` | `.py` | 177 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ops/__init__.py` | `.py` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ops/bundle.py` | `.py` | 105 | `FULLY_READ` | GAP-OPS-003 | Complete text read and indexed |
| `packages/eoip/ops/preflight.py` | `.py` | 150 | `FULLY_READ` | GAP-OPS-001 | Complete text read and indexed |
| `packages/eoip/ops/production.py` | `.py` | 132 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ops/upgrade.py` | `.py` | 138 | `FULLY_READ` | GAP-OPS-002 | Complete text read and indexed |
| `packages/eoip/platform_router.py` | `.py` | 2003 | `FULLY_READ` | CORE-001, CORE-006 | Complete text read and indexed |
| `packages/eoip/plugins/__init__.py` | `.py` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/plugins/loader.py` | `.py` | 101 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/plugins/runtime.py` | `.py` | 262 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/plugins/sdk.py` | `.py` | 173 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/privacy/__init__.py` | `.py` | 81 | `FULLY_READ` | SR-PRV-001, SR-PRV-006 | Complete text read and indexed |
| `packages/eoip/privacy/classification.py` | `.py` | 267 | `FULLY_READ` | SR-PRV-001 | Complete text read and indexed |
| `packages/eoip/privacy/consent.py` | `.py` | 105 | `FULLY_READ` | SR-PRV-004, SR-PRV-005 | Complete text read and indexed |
| `packages/eoip/privacy/dsar.py` | `.py` | 218 | `FULLY_READ` | SR-PRV-002, SR-PRV-003 | Complete text read and indexed |
| `packages/eoip/privacy/residency.py` | `.py` | 146 | `FULLY_READ` | SR-PRV-006 | Complete text read and indexed |
| `packages/eoip/privacy/retention.py` | `.py` | 143 | `FULLY_READ` | SR-PRV-003 | Complete text read and indexed |
| `packages/eoip/privacy/router.py` | `.py` | 127 | `FULLY_READ` | SR-PRV-001, SR-PRV-006 | Complete text read and indexed |
| `packages/eoip/privacy/scanner.py` | `.py` | 153 | `FULLY_READ` | COMPLY-002 | Complete text read and indexed |
| `packages/eoip/product/__init__.py` | `.py` | 15 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/product/intelligence.py` | `.py` | 478 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/prompts/__init__.py` | `.py` | 28 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/prompts/engine.py` | `.py` | 447 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/provenance/__init__.py` | `.py` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/provenance/evidence.py` | `.py` | 205 | `FULLY_READ` | FR-PROV-001, GAP-AI-001, GAP-GRAG-006, GAP-KRAG-007, GAP-PROV-001, GAP-PROV-002, GAP-PROV-003, GAP-PROV-004, GAP-PROV-00... | Complete text read and indexed |
| `packages/eoip/provenance/lineage.py` | `.py` | 59 | `FULLY_READ` | FR-PROV-002 | Complete text read and indexed |
| `packages/eoip/provenance/trust.py` | `.py` | 138 | `FULLY_READ` | GAP-RULE-002, GAP-TRUST-001, GAP-TRUST-002, GAP-TRUST-003, GAP-TRUST-004, GAP-TRUST-005 | Complete text read and indexed |
| `packages/eoip/qa/__init__.py` | `.py` | 46 | `FULLY_READ` | SR-QA-010, SR-QA-011, SR-QA-012, SR-QA-013, SR-QA-014 | Complete text read and indexed |
| `packages/eoip/qa/dashboard.py` | `.py` | 164 | `FULLY_READ` | SR-QA-010, SR-QA-011, SR-QA-012 | Complete text read and indexed |
| `packages/eoip/qa/evidence.py` | `.py` | 235 | `FULLY_READ` | SR-QA-010 | Complete text read and indexed |
| `packages/eoip/qa/introspection.py` | `.py` | 303 | `FULLY_READ` | SR-QA-013 | Complete text read and indexed |
| `packages/eoip/qa/mutation.py` | `.py` | 177 | `FULLY_READ` | SR-QA-011 | Complete text read and indexed |
| `packages/eoip/qa/policy.py` | `.py` | 162 | `FULLY_READ` | SR-QA-014 | Complete text read and indexed |
| `packages/eoip/qa/pytest_plugin.py` | `.py` | 65 | `FULLY_READ` | SR-QA-010 | Complete text read and indexed |
| `packages/eoip/qa/router.py` | `.py` | 136 | `FULLY_READ` | SR-QA-010, SR-QA-011, SR-QA-012, SR-QA-013, SR-QA-014 | Complete text read and indexed |
| `packages/eoip/qlang/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/qlang/jqlite.py` | `.py` | 133 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/qlang/jsonpath.py` | `.py` | 113 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/qlang/lucene.py` | `.py` | 212 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/qlang/plans.py` | `.py` | 86 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/qlang/taxonomy.py` | `.py` | 127 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/quality/__init__.py` | `.py` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/quality/engine.py` | `.py` | 373 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/quality/slo.py` | `.py` | 133 | `FULLY_READ` | G2-SLO-002, G2-SLO-003, G2-SLO-004, G2-SLO-005 | Complete text read and indexed |
| `packages/eoip/query/__init__.py` | `.py` | 16 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/cache.py` | `.py` | 292 | `FULLY_READ` | GAP-CACHE-001, GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-004, GAP-CACHE-005 | Complete text read and indexed |
| `packages/eoip/query/distributed_cache.py` | `.py` | 158 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/eql.py` | `.py` | 353 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/executor.py` | `.py` | 336 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/intelligence.py` | `.py` | 551 | `FULLY_READ` | GAP-QI-001, GAP-QI-002, GAP-QI-003, GAP-QI-004, GAP-QI-005, GAP-QI-006, GAP-QI-007, GAP-QI-008 | Complete text read and indexed |
| `packages/eoip/query/languages.py` | `.py` | 430 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/multi_paradigm_dispatcher.py` | `.py` | 377 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/nl.py` | `.py` | 284 | `FULLY_READ` | FR-QUERY-005 | Complete text read and indexed |
| `packages/eoip/query/nlq.py` | `.py` | 540 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/policy.py` | `.py` | 63 | `FULLY_READ` | FR-QUERY-006, FR-QUERY-008 | Complete text read and indexed |
| `packages/eoip/query/polyglot_engine.py` | `.py` | 566 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/query/unified.py` | `.py` | 550 | `FULLY_READ` | GAP-QUERY-001 | Complete text read and indexed |
| `packages/eoip/ragx/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ragx/architectures.py` | `.py` | 1142 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/ragx/core.py` | `.py` | 239 | `FULLY_READ` | GAP-KRAG-007 | Complete text read and indexed |
| `packages/eoip/reasoning/__init__.py` | `.py` | 46 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reasoning/agentops.py` | `.py` | 336 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reasoning/evaluation.py` | `.py` | 316 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reasoning/knowledge_reasoning.py` | `.py` | 395 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reasoning/memory.py` | `.py` | 424 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reasoning/router.py` | `.py` | 74 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reasoning/strategies.py` | `.py` | 717 | `FULLY_READ` | AI-007 | Complete text read and indexed |
| `packages/eoip/recovery/__init__.py` | `.py` | 25 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/recovery/backup_scheduler.py` | `.py` | 207 | `FULLY_READ` | INFRA-007 | Complete text read and indexed |
| `packages/eoip/recovery/wal.py` | `.py` | 404 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/recovery/webhook_reliability.py` | `.py` | 162 | `FULLY_READ` | G2-REL-002, G2-REL-003, G2-REL-004, G2-REL-005, G2-REL-008 | Complete text read and indexed |
| `packages/eoip/recovery_bundle.py` | `.py` | 382 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/reports/__init__.py` | `.py` | 41 | `FULLY_READ` | SR-NLQ-008 | Complete text read and indexed |
| `packages/eoip/reports/generator.py` | `.py` | 313 | `FULLY_READ` | SR-GOV-001, SR-GOV-003, SR-NLQ-008 | Complete text read and indexed |
| `packages/eoip/reports/router.py` | `.py` | 163 | `FULLY_READ` | SR-NLQ-008 | Complete text read and indexed |
| `packages/eoip/reports/schedule.py` | `.py` | 131 | `FULLY_READ` | SR-NLQ-008 | Complete text read and indexed |
| `packages/eoip/resilience/__init__.py` | `.py` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/resilience/bulkhead.py` | `.py` | 119 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/resilience/circuit_breaker.py` | `.py` | 127 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/resilience/connection_pool.py` | `.py` | 182 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/resilience/rate_limiter.py` | `.py` | 149 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/retrieval/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/retrieval/eval.py` | `.py` | 106 | `FULLY_READ` | FR-RAG-005 | Complete text read and indexed |
| `packages/eoip/retrieval/rag_suite.py` | `.py` | 1328 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/retrieval/service.py` | `.py` | 593 | `FULLY_READ` | FR-RAG-001, FR-RAG-002, FR-RAG-003, GAP-RET-002, GAP-RET-003, GAP-RET-006, GAP-SEARCH-001 | Complete text read and indexed |
| `packages/eoip/retrieval/strategy_registry.py` | `.py` | 220 | `FULLY_READ` | FR-RAG-006 | Complete text read and indexed |
| `packages/eoip/retrieval/temporal.py` | `.py` | 214 | `FULLY_READ` | GRAPH-005 | Complete text read and indexed |
| `packages/eoip/retrieval/vectors.py` | `.py` | 302 | `FULLY_READ` | GAP-RET-002, GAP-RET-006, GAP-SEARCH-001, GAP-SEARCH-002 | Complete text read and indexed |
| `packages/eoip/routing/__init__.py` | `.py` | 17 | `FULLY_READ` | CORE-003 | Complete text read and indexed |
| `packages/eoip/routing/engine.py` | `.py` | 266 | `FULLY_READ` | CORE-003 | Complete text read and indexed |
| `packages/eoip/runtime.py` | `.py` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/scheduling/__init__.py` | `.py` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/scheduling/executor.py` | `.py` | 404 | `FULLY_READ` | INFRA-005 | Complete text read and indexed |
| `packages/eoip/sdk/__init__.py` | `.py` | 29 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/sdk/gateway.py` | `.py` | 405 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/sdk/versioning.py` | `.py` | 168 | `FULLY_READ` | INFRA-006 | Complete text read and indexed |
| `packages/eoip/search/__init__.py` | `.py` | 53 | `FULLY_READ` | GAP-SEARCH-001, GAP-SEARCH-002 | Complete text read and indexed |
| `packages/eoip/search/analytics.py` | `.py` | 162 | `FULLY_READ` | UI-008 | Complete text read and indexed |
| `packages/eoip/search/facets.py` | `.py` | 348 | `FULLY_READ` | GAP-SEARCH-001, GAP-SEARCH-002 | Complete text read and indexed |
| `packages/eoip/search/hybrid_engine.py` | `.py` | 902 | `FULLY_READ` | H-02 | Complete text read and indexed |
| `packages/eoip/search/semantic.py` | `.py` | 336 | `FULLY_READ` | H-02 | Complete text read and indexed |
| `packages/eoip/security/__init__.py` | `.py` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/security/engine.py` | `.py` | 181 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/security/hardening.py` | `.py` | 137 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/security/reflection_sandbox.py` | `.py` | 265 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/snapshot.py` | `.py` | 258 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/specs/__init__.py` | `.py` | 30 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/specs/engine.py` | `.py` | 341 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/state/__init__.py` | `.py` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/state/engine.py` | `.py` | 169 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/streaming/__init__.py` | `.py` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/streaming/event_stream.py` | `.py` | 236 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/streaming/mutation_stream.py` | `.py` | 340 | `FULLY_READ` | KGR-G-020 | Complete text read and indexed |
| `packages/eoip/suggest/__init__.py` | `.py` | 35 | `FULLY_READ` | SR-NLQ-001 | Complete text read and indexed |
| `packages/eoip/suggest/engine.py` | `.py` | 274 | `FULLY_READ` | SR-NLQ-001, SR-NLQ-002, SR-NLQ-003 | Complete text read and indexed |
| `packages/eoip/suggest/models.py` | `.py` | 132 | `FULLY_READ` | SR-NLQ-002, SR-NLQ-003, SR-NLQ-004 | Complete text read and indexed |
| `packages/eoip/suggest/parser.py` | `.py` | 242 | `FULLY_READ` | SR-NLQ-001 | Complete text read and indexed |
| `packages/eoip/suggest/router.py` | `.py` | 49 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/__init__.py` | `.py` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/auto_onboard.py` | `.py` | 508 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/executor.py` | `.py` | 308 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/pipeline_factory.py` | `.py` | 342 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/registry.py` | `.py` | 432 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/router.py` | `.py` | 319 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/systems/schema_generator.py` | `.py` | 389 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/telemetry/adapter.py` | `.py` | 352 | `FULLY_READ` | AGENT-001, G2-TEL-002, G2-TEL-003, G2-TEL-004, G2-TEL-005, G2-TEL-006, G2-TEL-007, G2-TEL-008 | Complete text read and indexed |
| `packages/eoip/tenancy/__init__.py` | `.py` | 91 | `FULLY_READ` | SR-TEN-001, SR-TEN-002, SR-TEN-004, SR-TEN-005, SR-TEN-006, SR-TEN-007, SR-TEN-008, SR-TEN-009, SR-TEN-010 | Complete text read and indexed |
| `packages/eoip/tenancy/context.py` | `.py` | 101 | `FULLY_READ` | SR-TEN-001, SR-TEN-003 | Complete text read and indexed |
| `packages/eoip/tenancy/isolation.py` | `.py` | 155 | `FULLY_READ` | SR-TEN-002, SR-TEN-003, SR-TEN-005 | Complete text read and indexed |
| `packages/eoip/tenancy/lifecycle.py` | `.py` | 199 | `FULLY_READ` | SR-TEN-003, SR-TEN-005, SR-TEN-007 | Complete text read and indexed |
| `packages/eoip/tenancy/metering.py` | `.py` | 174 | `FULLY_READ` | SR-TEN-009 | Complete text read and indexed |
| `packages/eoip/tenancy/overrides.py` | `.py` | 189 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/tenancy/quotas.py` | `.py` | 240 | `FULLY_READ` | SR-TEN-006 | Complete text read and indexed |
| `packages/eoip/tenancy/router.py` | `.py` | 216 | `FULLY_READ` | SR-TEN-001, SR-TEN-002, SR-TEN-006, SR-TEN-007, SR-TEN-009 | Complete text read and indexed |
| `packages/eoip/tenancy/service.py` | `.py` | 41 | `FULLY_READ` | SR-TEN-001, SR-TEN-007, SR-TEN-009 | Complete text read and indexed |
| `packages/eoip/testing/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/testing/a11y_scanner.py` | `.py` | 136 | `FULLY_READ` | TEST-005 | Complete text read and indexed |
| `packages/eoip/testing/chaos.py` | `.py` | 220 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/testing/perf_regression.py` | `.py` | 134 | `FULLY_READ` | TEST-004 | Complete text read and indexed |
| `packages/eoip/token_budget/__init__.py` | `.py` | 19 | `FULLY_READ` | CORE-006 | Complete text read and indexed |
| `packages/eoip/token_budget/engine.py` | `.py` | 355 | `FULLY_READ` | CORE-006 | Complete text read and indexed |
| `packages/eoip/token_formats/__init__.py` | `.py` | 31 | `FULLY_READ` | CORE-001 | Complete text read and indexed |
| `packages/eoip/token_formats/engine.py` | `.py` | 810 | `FULLY_READ` | CORE-001 | Complete text read and indexed |
| `packages/eoip/tools_contract/__init__.py` | `.py` | 15 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/tools_contract/engine.py` | `.py` | 215 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/tools_contract/mcp_bridge.py` | `.py` | 237 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/truth/__init__.py` | `.py` | 12 | `FULLY_READ` | GAP-TRUTH-001 | Complete text read and indexed |
| `packages/eoip/truth/engine.py` | `.py` | 249 | `FULLY_READ` | GAP-TRUTH-001 | Complete text read and indexed |
| `packages/eoip/truth/models.py` | `.py` | 68 | `FULLY_READ` | GAP-TRUTH-001 | Complete text read and indexed |
| `packages/eoip/validation/__init__.py` | `.py` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/validation/engine.py` | `.py` | 281 | `FULLY_READ` | FR-VALID-001, FR-VALID-002 | Complete text read and indexed |
| `packages/eoip/validation/gate.py` | `.py` | 70 | `FULLY_READ` | FR-VALID-002, MVP-FR-012 | Complete text read and indexed |
| `packages/eoip/validation/quality.py` | `.py` | 135 | `FULLY_READ` | FR-VALID-002, FR-VALID-003 | Complete text read and indexed |
| `packages/eoip/validation/rules/__init__.py` | `.py` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/verification/__init__.py` | `.py` | 39 | `FULLY_READ` | CORE-002 | Complete text read and indexed |
| `packages/eoip/verification/behavioral_gate.py` | `.py` | 915 | `FULLY_READ` | KGR-G-011 | Complete text read and indexed |
| `packages/eoip/verification/engine.py` | `.py` | 465 | `FULLY_READ` | CORE-002 | Complete text read and indexed |
| `packages/eoip/verification/release_gate.py` | `.py` | 498 | `FULLY_READ` | CG-GAP-008, MVP-FR-028, REL-01, REL-02, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-09, REL-10 (+5 more) | Complete text read and indexed |
| `packages/eoip/workflows/__init__.py` | `.py` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/workflows/engine.py` | `.py` | 447 | `FULLY_READ` | - | Complete text read and indexed |
| `packages/eoip/xai/__init__.py` | `.py` | 27 | `FULLY_READ` | AI-001 | Complete text read and indexed |
| `packages/eoip/xai/engine.py` | `.py` | 432 | `FULLY_READ` | AI-001 | Complete text read and indexed |
| `pyproject.toml` | `.toml` | 119 | `FULLY_READ` | - | Complete text read and indexed |
| `pyrightconfig.json` | `.json` | 15 | `FULLY_READ` | - | Complete text read and indexed |
| `README.md` | `.md` | 205 | `FULLY_READ` | - | Complete text read and indexed |
| `requirements-fileparse.lock` | `.lock` | 0 | `EXCLUDED` | - | generated dependency lockfile |
| `requirements-registry.json` | `.json` | 17910 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, AI-001, AI-002, AI-003, AI-004, AI-005, AI-006, AI-007, BASE-01 (+923 more) | Complete text read and indexed |
| `requirements-test-map.json` | `.json` | 3396 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, AI-001, AI-002, AI-003, AI-004, AI-005, AI-006, AI-007, CG-GAP-008 (+888 mor... | Complete text read and indexed |
| `requirements.lock` | `.lock` | 0 | `EXCLUDED` | - | generated dependency lockfile |
| `schemas/_catalog.json` | `.json` | 517 | `FULLY_READ` | FR-AGT-001, FR-AGT-002, FR-API-001, FR-EVD-001, FR-GRH-002, FR-ING-001, FR-ING-003, FR-ING-004, FR-ING-008, FR-MEM-001, ... | Complete text read and indexed |
| `schemas/_common.schema.json` | `.json` | 119 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/agent_request.schema.json` | `.json` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/agent_result.schema.json` | `.json` | 76 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/api_contract.schema.json` | `.json` | 34 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/audit_event.schema.json` | `.json` | 54 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/behavioral_gate_verdict.schema.json` | `.json` | 85 | `FULLY_READ` | KGR-G-011 | Complete text read and indexed |
| `schemas/causal_hypothesis.schema.json` | `.json` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/crawl_scope.schema.json` | `.json` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/demo_scenario_pack.schema.json` | `.json` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/evidence.schema.json` | `.json` | 50 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/graph_diff.schema.json` | `.json` | 34 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/graph_mutation.schema.json` | `.json` | 35 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/graph_result.schema.json` | `.json` | 54 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/graph_revision.schema.json` | `.json` | 32 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/incremental_index_event.schema.json` | `.json` | 61 | `FULLY_READ` | KGR-G-012 | Complete text read and indexed |
| `schemas/knowledge_capsule.schema.json` | `.json` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/knowledge_debt_finding.schema.json` | `.json` | 20 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/knowledge_slo.schema.json` | `.json` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/memory_record.schema.json` | `.json` | 22 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/multihop_query.schema.json` | `.json` | 95 | `FULLY_READ` | KGR-G-018 | Complete text read and indexed |
| `schemas/mutation_stream_event.schema.json` | `.json` | 102 | `FULLY_READ` | KGR-G-020 | Complete text read and indexed |
| `schemas/named_graph_config.schema.json` | `.json` | 74 | `FULLY_READ` | KGR-G-013 | Complete text read and indexed |
| `schemas/normalized_entity.schema.json` | `.json` | 47 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/normalized_relationship.schema.json` | `.json` | 52 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/ontology_evolution_proposal.schema.json` | `.json` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/ontology_induction_result.schema.json` | `.json` | 115 | `FULLY_READ` | KGR-G-015 | Complete text read and indexed |
| `schemas/process_event.schema.json` | `.json` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/query_plan.schema.json` | `.json` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/reconciliation_run.schema.json` | `.json` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/relationship_revision.schema.json` | `.json` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/retrieval_result.schema.json` | `.json` | 44 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/semantic_change_event.schema.json` | `.json` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/simulation_spec.schema.json` | `.json` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/source_capabilities.schema.json` | `.json` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/source_checkpoint.schema.json` | `.json` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/source_event.schema.json` | `.json` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/source_event_v2.schema.json` | `.json` | 42 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/source_registry_entry.schema.json` | `.json` | 35 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/streaming_memory_event.schema.json` | `.json` | 83 | `FULLY_READ` | KGR-G-014 | Complete text read and indexed |
| `schemas/telemetry_evidence.schema.json` | `.json` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/tool_request.schema.json` | `.json` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/tool_result.schema.json` | `.json` | 17 | `FULLY_READ` | - | Complete text read and indexed |
| `schemas/uncertainty_envelope.schema.json` | `.json` | 129 | `FULLY_READ` | KGR-G-019 | Complete text read and indexed |
| `schemas/vector_search_request.schema.json` | `.json` | 86 | `FULLY_READ` | KGR-G-016 | Complete text read and indexed |
| `scripts/_all_phase6_tasks.py` | `.py` | 9 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_check_wp62.py` | `.py` | 23 | `FULLY_READ` | G2-IMMUNE-002, G2-IMMUNE-003, G2-IMMUNE-004, G2-IMMUNE-005, G2-IMMUNE-006, G2-IMMUNE-007, G2-IMMUNE-008, G2-IMMUNE-009, ... | Complete text read and indexed |
| `scripts/_check_wp71.py` | `.py` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_check_wp71_files.py` | `.py` | 5 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_check_wp72.py` | `.py` | 24 | `FULLY_READ` | G2-PERF-002, G2-PERF-003, G2-PERF-004, G2-PERF-005, G2-PERF-006, G2-PERF-007, G2-PERF-008, G2-REL-002, G2-REL-003, G2-RE... | Complete text read and indexed |
| `scripts/_find_lines.py` | `.py` | 6 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_find_moonshots.py` | `.py` | 8 | `FULLY_READ` | MS-15, MS-22 | Complete text read and indexed |
| `scripts/_find_sec_specs.py` | `.py` | 23 | `FULLY_READ` | GAP-SEC-008, GAP-SEC-009, GAP-SEC-010, GAP-SEC-011, GAP-SEC-012 | Complete text read and indexed |
| `scripts/_find_specs.py` | `.py` | 9 | `FULLY_READ` | G2-IMMUNE-002, G2-SIM-002, G2-TWIN-002 | Complete text read and indexed |
| `scripts/_find_vsc_specs.py` | `.py` | 25 | `FULLY_READ` | FR-VSCODE-001, FR-VSCODE-002, G2-VSC-002, G2-VSC-003, G2-VSC-004, G2-VSC-005, G2-VSC-006, G2-VSC-007, G2-VSC-008, MVP-FR... | Complete text read and indexed |
| `scripts/_inspect_gap_sec.py` | `.py` | 7 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_inspect_p6_registry.py` | `.py` | 7 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_inspect_phase6.py` | `.py` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_inspect_vsc_reqs.py` | `.py` | 13 | `FULLY_READ` | FR-VSCODE-001, FR-VSCODE-002, G2-VSC-002, G2-VSC-003, G2-VSC-004, G2-VSC-005, G2-VSC-006, G2-VSC-007, G2-VSC-008, MVP-FR... | Complete text read and indexed |
| `scripts/_mark_done.py` | `.py` | 98 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_mark_wp44_done.py` | `.py` | 49 | `FULLY_READ` | G2-CAP-002, G2-CAP-003, G2-CAP-004, G2-CAP-005, G2-CAP-006, G2-GRAPH-API-002, G2-GRAPH-API-003, G2-GRAPH-BIZ-002, G2-GRA... | Complete text read and indexed |
| `scripts/_mark_wp51_done.py` | `.py` | 40 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_mark_wp52_done.py` | `.py` | 108 | `FULLY_READ` | GAP-GITOPS-002, GAP-GITOPS-003, GAP-GITOPS-004, GAP-GITOPS-005, GAP-GITOPS-006, GAP-GITOPS-007, GAP-GITOPS-008, GAP-MKT-... | Complete text read and indexed |
| `scripts/_mark_wp53_done.py` | `.py` | 293 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-UI-001, FR-UI-002, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, ... | Complete text read and indexed |
| `scripts/_mark_wp54_and_wp55_done.py` | `.py` | 84 | `FULLY_READ` | FR-VSCODE-001, FR-VSCODE-002, G2-VSC-002, G2-VSC-003, G2-VSC-004, G2-VSC-005, G2-VSC-006, G2-VSC-007, G2-VSC-008, GAP-SE... | Complete text read and indexed |
| `scripts/_mark_wp61_done.py` | `.py` | 73 | `FULLY_READ` | G2-PM-002, G2-PM-003, G2-PM-004, G2-PM-005, MS-11, MS-12, MS-13, MS-16, MS-17, MS-25, MS-26, MS-27 (+2 more) | Complete text read and indexed |
| `scripts/_mark_wp62_done.py` | `.py` | 135 | `FULLY_READ` | G2-IMMUNE-002, G2-IMMUNE-003, G2-IMMUNE-004, G2-IMMUNE-005, G2-IMMUNE-006, G2-IMMUNE-007, G2-IMMUNE-008, G2-IMMUNE-009, ... | Complete text read and indexed |
| `scripts/_mark_wp71_done.py` | `.py` | 39 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_mark_wp72_done.py` | `.py` | 151 | `FULLY_READ` | G2-PERF-002, G2-PERF-003, G2-PERF-004, G2-PERF-005, G2-PERF-006, G2-PERF-007, G2-PERF-008, G2-REL-002, G2-REL-003, G2-RE... | Complete text read and indexed |
| `scripts/_mark_wp8_done.py` | `.py` | 79 | `FULLY_READ` | CG-GAP-008, MVP-FR-028, REL-01, REL-02, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-09, REL-10 (+5 more) | Complete text read and indexed |
| `scripts/_read_g2_ops.py` | `.py` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_read_gaps2.py` | `.py` | 19 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_read_moonshots_spec.py` | `.py` | 20 | `FULLY_READ` | MS-15, MS-18, MS-19, MS-21, MS-22, MS-23, MS-24, MS-29, MS-30 | Complete text read and indexed |
| `scripts/_show_unticked_p5.py` | `.py` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/_status_summary.py` | `.py` | 36 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/application_recovery_fixture.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/audit_phase3.py` | `.py` | 30 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/backup.py` | `.py` | 76 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_cache.py` | `.py` | 20 | `FULLY_READ` | GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-004, GAP-CACHE-005 | Complete text read and indexed |
| `scripts/batch_p4_fresh.py` | `.py` | 20 | `FULLY_READ` | GAP-FRESH-002, GAP-FRESH-003, GAP-FRESH-004, GAP-FRESH-005 | Complete text read and indexed |
| `scripts/batch_p4_gds.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_nlp.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_qi.py` | `.py` | 16 | `FULLY_READ` | GAP-QI-005, GAP-QI-006, GAP-QI-008 | Complete text read and indexed |
| `scripts/batch_p4_qop.py` | `.py` | 11 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_query.py` | `.py` | 2 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_rec.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_rule.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/batch_p4_truth.py` | `.py` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/benchmark.py` | `.py` | 537 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `scripts/benchmark_data.py` | `.py` | 300 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `scripts/bootstrap_schema.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/build_requirements_registry.py` | `.py` | 165 | `FULLY_READ` | BASE-01, BASE-02, BASE-04 | Complete text read and indexed |
| `scripts/check_backlog_phases.py` | `.py` | 27 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/check_markdown_links.py` | `.py` | 65 | `FULLY_READ` | CG-GAP-005, REL-13 | Complete text read and indexed |
| `scripts/check_p2_requirements.py` | `.py` | 40 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/check_phase2_diff.py` | `.py` | 12 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/check_product_gate.py` | `.py` | 20 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/check_wp53_registry.py` | `.py` | 20 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-UI-001, FR-UI-002, G2-UX-LENS-002, G2-UX-LENS-003, UI-01, UI-02, UI-03, UI-04 | Complete text read and indexed |
| `scripts/container.ps1` | `.ps1` | 364 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/container.sh` | `.sh` | 213 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/demo_reset.py` | `.py` | 90 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/detect_runtime.py` | `.py` | 55 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/docker.ps1` | `.ps1` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/documentation_audit.py` | `.py` | 317 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/gap_coverage.py` | `.py` | 84 | `FULLY_READ` | GAP-KGCI-001, GAP-KGCI-002, GAP-KGCI-003 | Complete text read and indexed |
| `scripts/inspect_all_p2_unticked.py` | `.py` | 14 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/inspect_progress.py` | `.py` | 8 | `FULLY_READ` | KGR-G-011 | Complete text read and indexed |
| `scripts/inspect_tested_p2.py` | `.py` | 9 | `FULLY_READ` | FR-CONF-001, FR-SNOW-001, G2-EKAF-003, G2-SEC-CRAWL-002, G2-SRC-CONF-002, G2-SRC-CONF-003, G2-SRC-CONF-004, G2-SRC-CONF-... | Complete text read and indexed |
| `scripts/inspect_wp21_reqs.py` | `.py` | 21 | `FULLY_READ` | G2-EKAF-003, G2-EKAF-010, G2-EKAF-014, G2-EKAF-016, G2-EKAF-023, G2-EKAF-024, G2-EKAF-025, G2-EKAF-026 | Complete text read and indexed |
| `scripts/inspect_wp21_tasks.py` | `.py` | 15 | `FULLY_READ` | CONN-01, CONN-02, CONN-03, FR-CONF-001, FR-SNOW-001, G2-EKAF-003, G2-EKAF-010, G2-EKAF-014, G2-EKAF-016, G2-EKAF-023, G2... | Complete text read and indexed |
| `scripts/inspect_wp32_backlog.py` | `.py` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/install_git_hooks.py` | `.py` | 31 | `FULLY_READ` | KGR-G-012 | Complete text read and indexed |
| `scripts/list_p4_unticked.py` | `.py` | 38 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/list_phase2_unticked.py` | `.py` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/list_phase3_unticked.py` | `.py` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/list_phase5.py` | `.py` | 20 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/load_demo_corpus.py` | `.py` | 142 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/ontology_diff.py` | `.py` | 21 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/parse_backlog.py` | `.py` | 33 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/patch_contracts_tags.py` | `.py` | 10 | `FULLY_READ` | FR-CONN-001, G2-EKAF-002, G2-T0005 | Complete text read and indexed |
| `scripts/rag_eval.py` | `.py` | 102 | `FULLY_READ` | FR-RAG-005 | Complete text read and indexed |
| `scripts/read_crawl_sec_specs.py` | `.py` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/read_g2_specs.py` | `.py` | 23 | `FULLY_READ` | G2-EKAF-003, G2-EKAF-010, G2-EKAF-014, G2-EKAF-016, G2-EKAF-023, G2-EKAF-024, G2-EKAF-025, G2-EKAF-026 | Complete text read and indexed |
| `scripts/read_wp22_specs.py` | `.py` | 20 | `FULLY_READ` | G2-EVENT-002, G2-EVENT-003, G2-EVENT-004, G2-EVENT-005, G2-EVENT-006, G2-EVENT-007, G2-SYNC-002, G2-SYNC-003, G2-SYNC-00... | Complete text read and indexed |
| `scripts/read_wp52.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/read_wp53.py` | `.py` | 8 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/replay.py` | `.py` | 47 | `FULLY_READ` | FR-CONN-006 | Complete text read and indexed |
| `scripts/restore.py` | `.py` | 72 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/scan_phase3_tests.py` | `.py` | 44 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/scan_phase4_tasks.py` | `.py` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/scan_unticked_tests.py` | `.py` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/scan_wp32.py` | `.py` | 13 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/setup_hubble.py` | `.py` | 89 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/smoke_test.py` | `.py` | 139 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/tick_phase0_phase1.py` | `.py` | 57 | `FULLY_READ` | BASE-01, BASE-02, BASE-03, BASE-04, CG-CODE-01, CG-CODE-02, CG-DOC-01, CG-GAP-001, CG-GAP-002, CG-GAP-003, CG-GAP-004, C... | Complete text read and indexed |
| `scripts/tick_phase2_batch1.py` | `.py` | 50 | `FULLY_READ` | FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CODE-005, FR-CONN-001, FR-CONN-003, FR-CONN-004, FR-CONN-005, FR-INGEST-002, F... | Complete text read and indexed |
| `scripts/update_phase2_wp23.py` | `.py` | 110 | `FULLY_READ` | CONN-01, CONN-02, CONN-03, FR-CONF-001, FR-SNOW-001, G2-SRC-API-002, G2-SRC-API-003, G2-SRC-API-004, G2-SRC-API-005, G2-... | Complete text read and indexed |
| `scripts/update_phase3_wp31.py` | `.py` | 142 | `FULLY_READ` | KGR-G-014, KGR-G-015, KGR-G-016, KGR-G-017, KGR-G-018, KGR-G-019, KGR-G-020 | Complete text read and indexed |
| `scripts/update_phase3_wp32_wp33.py` | `.py` | 324 | `FULLY_READ` | FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, G2-CAUSE-002, G2-CAUSE-003, G2-CAUSE-004, G2-CAUSE... | Complete text read and indexed |
| `scripts/update_wp21_registry.py` | `.py` | 87 | `FULLY_READ` | G2-EKAF-003, G2-EKAF-010, G2-EKAF-014, G2-EKAF-016, G2-EKAF-023, G2-EKAF-024, G2-EKAF-025, G2-EKAF-026 | Complete text read and indexed |
| `scripts/update_wp22_registry.py` | `.py` | 168 | `FULLY_READ` | G2-EVENT-002, G2-EVENT-003, G2-EVENT-004, G2-EVENT-005, G2-EVENT-006, G2-EVENT-007, G2-SYNC-002, G2-SYNC-003, G2-SYNC-00... | Complete text read and indexed |
| `scripts/validate_with_evidence.py` | `.py` | 239 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/verify_clean_demo.py` | `.py` | 292 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/verify_live_dlq.py` | `.py` | 88 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/verify_recovery_bundle.py` | `.py` | 105 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/verify_requirement_evidence.py` | `.py` | 327 | `FULLY_READ` | MVP-FR-001, MVP-FR-028 | Complete text read and indexed |
| `scripts/verify_restore.py` | `.py` | 132 | `FULLY_READ` | - | Complete text read and indexed |
| `scripts/verify_seeded_gate.py` | `.py` | 29 | `FULLY_READ` | - | Complete text read and indexed |
| `secrets.example/api-token.txt` | `.txt` | 1 | `FULLY_READ` | - | Complete text read and indexed |
| `secrets.example/README.md` | `.md` | 37 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/chaos/fault_injector.py` | `.py` | 86 | `FULLY_READ` | TEST-001 | Complete text read and indexed |
| `tests/conftest.py` | `.py` | 76 | `FULLY_READ` | BASE-02 | Complete text read and indexed |
| `tests/contract/__init__.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/contract/test_g2_contracts.py` | `.py` | 177 | `FULLY_READ` | FR-CONN-001, G2-EKAF-002, G2-EKAF-003, G2-EKAF-023, G2-REQ-34, G2-T0002, G2-T0003, G2-T0005 | Complete text read and indexed |
| `tests/contract/test_graph_store_contract.py` | `.py` | 65 | `FULLY_READ` | NFR-MAINT-001, TEST-1 | Complete text read and indexed |
| `tests/contract/test_query_plan_contract.py` | `.py` | 65 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/e2e/__init__.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/e2e/test_clean_recovery.py` | `.py` | 89 | `FULLY_READ` | G2-T0220, G2-T0221, G2-T0223, G2-T0225 | Complete text read and indexed |
| `tests/e2e/test_demo_corpus.py` | `.py` | 113 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/e2e/test_demo_flow.py` | `.py` | 143 | `FULLY_READ` | MVP-FR-028 | Complete text read and indexed |
| `tests/e2e/test_enterprise_demo_scenarios.py` | `.py` | 268 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/e2e/test_restart_safe.py` | `.py` | 142 | `FULLY_READ` | NFR-REL-001 | Complete text read and indexed |
| `tests/fuzz/test_property_fuzz.py` | `.py` | 124 | `FULLY_READ` | TEST-003 | Complete text read and indexed |
| `tests/integration/__init__.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/integration/test_mcp_transport.py` | `.py` | 82 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/load/k6_scenarios.js` | `.js` | 57 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/load/load_runner.py` | `.py` | 108 | `FULLY_READ` | TEST-002 | Complete text read and indexed |
| `tests/load/locustfile.py` | `.py` | 34 | `FULLY_READ` | TEST-002 | Complete text read and indexed |
| `tests/performance/__init__.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/performance/test_benchmark_publication.py` | `.py` | 166 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `tests/performance/test_benchmarks.py` | `.py` | 115 | `FULLY_READ` | NFR-PERF-001 | Complete text read and indexed |
| `tests/runtime_dlq/confluence_upstream.py` | `.py` | 148 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/conftest.py` | `.py` | 163 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/fixture_http.py` | `.py` | 18 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/servicenow_upstream.py` | `.py` | 79 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_confluence_acquisition.py` | `.py` | 155 | `FULLY_READ` | FR-CONF-001, G2-SRC-CONF-001, G2-SRC-CONF-002, G2-SRC-CONF-003, G2-SRC-CONF-004, G2-SRC-CONF-005, G2-T0401, G2-T0402, G2... | Complete text read and indexed |
| `tests/runtime_dlq/test_confluence_failures.py` | `.py` | 34 | `FULLY_READ` | FR-CONF-001, G2-T0401, G2-T0402 | Complete text read and indexed |
| `tests/runtime_dlq/test_confluence_rejection.py` | `.py` | 40 | `FULLY_READ` | FR-CONF-001, G2-T0112, G2-T0402 | Complete text read and indexed |
| `tests/runtime_dlq/test_memory_lifecycle.py` | `.py` | 38 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_memory_policy.py` | `.py` | 31 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_memory_privacy.py` | `.py` | 37 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_recovered_replay.py` | `.py` | 41 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_registered_recovery.py` | `.py` | 54 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_registered_refusals.py` | `.py` | 35 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_registered_rejection.py` | `.py` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_rejected_replay.py` | `.py` | 23 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_replay_refusals.py` | `.py` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_dlq/test_servicenow_acquisition.py` | `.py` | 57 | `FULLY_READ` | FR-SNOW-001, G2-T0110, G2-T0203 | Complete text read and indexed |
| `tests/runtime_dlq/test_servicenow_authentication.py` | `.py` | 26 | `FULLY_READ` | FR-SNOW-001 | Complete text read and indexed |
| `tests/runtime_dlq/test_servicenow_rejection.py` | `.py` | 66 | `FULLY_READ` | FR-SNOW-001, G2-T0112 | Complete text read and indexed |
| `tests/runtime_hubble/conftest.py` | `.py` | 88 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_hubble/test_01_manual.py` | `.py` | 24 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_hubble/test_02_pipeline.py` | `.py` | 45 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_hubble/test_03_persistence.py` | `.py` | 15 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_hubble/test_04_corpus.py` | `.py` | 40 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_hubble/test_05_enterprise.py` | `.py` | 57 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/runtime_hubble/test_07_code_graph.py` | `.py` | 43 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/security/__init__.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/security/test_container_hardening.py` | `.py` | 129 | `FULLY_READ` | NFR-SEC-006 | Complete text read and indexed |
| `tests/security/test_crawler_security.py` | `.py` | 184 | `FULLY_READ` | G2-SEC-CRAWL-002, G2-SEC-CRAWL-003, G2-SEC-CRAWL-004, G2-SEC-CRAWL-005, G2-SEC-CRAWL-006, G2-SEC-CRAWL-007, G2-SEC-CRAWL... | Complete text read and indexed |
| `tests/security/test_no_egress.py` | `.py` | 84 | `FULLY_READ` | NFR-SEC-001 | Complete text read and indexed |
| `tests/security/test_security_baseline.py` | `.py` | 113 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/security/test_verification_suite.py` | `.py` | 175 | `FULLY_READ` | FR-MCP-001, FR-MCP-002, MVP-FR-022, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-007 | Complete text read and indexed |
| `tests/unit/__init__.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_acquisition_fabric.py` | `.py` | 546 | `FULLY_READ` | FR-INGEST-004, G2-EKAF-001, G2-EKAF-004, G2-EKAF-005, G2-EKAF-006, G2-EKAF-007, G2-EKAF-008, G2-EKAF-009, G2-EKAF-011, G... | Complete text read and indexed |
| `tests/unit/test_acquisition_sync_semantics.py` | `.py` | 100 | `FULLY_READ` | G2-SYNC-010, G2-SYNC-013, G2-SYNC-014 | Complete text read and indexed |
| `tests/unit/test_admin_gremlin.py` | `.py` | 60 | `FULLY_READ` | FR-QUERY-008 | Complete text read and indexed |
| `tests/unit/test_admin_proposal_review.py` | `.py` | 122 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_advanced_enterprise_capabilities.py` | `.py` | 285 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_agent_analytics.py` | `.py` | 197 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_agent_memory.py` | `.py` | 411 | `FULLY_READ` | FR-MEM-001, NFR-PRIV-001 | Complete text read and indexed |
| `tests/unit/test_agent_runtime.py` | `.py` | 209 | `FULLY_READ` | TEST-1 | Complete text read and indexed |
| `tests/unit/test_agents_new.py` | `.py` | 144 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_aiml_ops.py` | `.py` | 230 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_all_15_engineering_disciplines.py` | `.py` | 435 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_api_portal_connector.py` | `.py` | 103 | `FULLY_READ` | G2-SRC-API-002, G2-SRC-API-003, G2-SRC-API-004, G2-SRC-API-005, G2-SRC-API-006 | Complete text read and indexed |
| `tests/unit/test_api_queries.py` | `.py` | 127 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_application_state_recovery.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_audit.py` | `.py` | 48 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_authn.py` | `.py` | 404 | `FULLY_READ` | GAP-SEC-001, GAP-SEC-003 | Complete text read and indexed |
| `tests/unit/test_authz.py` | `.py` | 310 | `FULLY_READ` | GAP-SEC-001, GAP-SEC-002, GAP-SEC-003, GAP-SEC-004, GAP-SEC-005, GAP-SEC-006, GAP-SEC-007, H-04 | Complete text read and indexed |
| `tests/unit/test_autodemo_runner.py` | `.py` | 216 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_behavioral_gate.py` | `.py` | 124 | `FULLY_READ` | KGR-G-011 | Complete text read and indexed |
| `tests/unit/test_bitemporal.py` | `.py` | 263 | `FULLY_READ` | GAP-TEMP-001, GAP-TEMP-002, GAP-TEMP-003, GAP-TEMP-004, GAP-TEMP-005 | Complete text read and indexed |
| `tests/unit/test_brain_and_living_system.py` | `.py` | 354 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_branding.py` | `.py` | 238 | `FULLY_READ` | SR-ONT-007, SR-WL-001, SR-WL-004 | Complete text read and indexed |
| `tests/unit/test_bulk_load.py` | `.py` | 158 | `FULLY_READ` | G2-EVOL-010, GAP-HG-004 | Complete text read and indexed |
| `tests/unit/test_cache_freshness_cdc.py` | `.py` | 119 | `FULLY_READ` | GAP-CACHE-002, GAP-CACHE-003, GAP-CACHE-004, GAP-CACHE-005 | Complete text read and indexed |
| `tests/unit/test_canonical_ingestion_boundary.py` | `.py` | 207 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_capsules.py` | `.py` | 142 | `FULLY_READ` | G2-CAP-001, G2-CAP-002, G2-CAP-003, G2-CAP-004, G2-CAP-005, G2-CAP-006 | Complete text read and indexed |
| `tests/unit/test_causal_reasoning.py` | `.py` | 104 | `FULLY_READ` | G2-CAUSE-002, G2-CAUSE-003, G2-CAUSE-004, G2-CAUSE-005, G2-CAUSE-006 | Complete text read and indexed |
| `tests/unit/test_change_journal_family.py` | `.py` | 152 | `FULLY_READ` | G2-JOURNAL-002, G2-JOURNAL-003, G2-JOURNAL-004, G2-JOURNAL-005, G2-JOURNAL-006 | Complete text read and indexed |
| `tests/unit/test_cicd_connector.py` | `.py` | 106 | `FULLY_READ` | G2-SRC-CICD-002, G2-SRC-CICD-003, G2-SRC-CICD-004 | Complete text read and indexed |
| `tests/unit/test_code_graph_json_ingestion.py` | `.py` | 131 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_code_ingestion.py` | `.py` | 57 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_code_parser.py` | `.py` | 48 | `FULLY_READ` | FR-CODE-001, FR-CODE-002, FR-CODE-004, FR-CODE-005, G2-SRC-CODE-002, G2-SRC-CODE-003, G2-SRC-CODE-004, G2-SRC-CODE-005 | Complete text read and indexed |
| `tests/unit/test_cognitive_narrator.py` | `.py` | 208 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_collaboration.py` | `.py` | 322 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_community_labels.py` | `.py` | 100 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_compliance_packs.py` | `.py` | 353 | `FULLY_READ` | SR-GOV-002, SR-GOV-003, SR-GOV-004, SR-GOV-005 | Complete text read and indexed |
| `tests/unit/test_confluence_body.py` | `.py` | 192 | `FULLY_READ` | FR-CONF-001, G2-ARCH-007, G2-SRC-CONF-003 | Complete text read and indexed |
| `tests/unit/test_confluence_history.py` | `.py` | 157 | `FULLY_READ` | FR-CONN-006, G2-SRC-CONF-002, G2-T0403 | Complete text read and indexed |
| `tests/unit/test_confluence_metadata.py` | `.py` | 196 | `FULLY_READ` | FR-CONF-001, FR-CONN-006, G2-ARCH-007, G2-SRC-CONF-001 | Complete text read and indexed |
| `tests/unit/test_confluence_upstream_fixture.py` | `.py` | 82 | `FULLY_READ` | FR-CONF-001 | Complete text read and indexed |
| `tests/unit/test_conformance.py` | `.py` | 195 | `FULLY_READ` | G2-ARCHC-002, G2-ARCHC-003, G2-ARCHC-004, G2-ARCHC-005, G2-ARCHC-006, G2-ARCHC-007, G2-ARCHC-008, G2-ARCHC-009 | Complete text read and indexed |
| `tests/unit/test_connection_factory.py` | `.py` | 308 | `FULLY_READ` | TASK-99 | Complete text read and indexed |
| `tests/unit/test_connectors_new.py` | `.py` | 158 | `FULLY_READ` | G2-SRC-DD-002, G2-SRC-DD-003, G2-SRC-DD-004, G2-SRC-GRAF-002, G2-SRC-GRAF-003, G2-SRC-KIB-002, G2-SRC-KIB-003, G2-SRC-KI... | Complete text read and indexed |
| `tests/unit/test_container_runtime.py` | `.py` | 136 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_container_smoke_manifest.py` | `.py` | 35 | `FULLY_READ` | H-06 | Complete text read and indexed |
| `tests/unit/test_contracts.py` | `.py` | 59 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_deep_agents.py` | `.py` | 247 | `FULLY_READ` | TEST-1 | Complete text read and indexed |
| `tests/unit/test_demo_reset.py` | `.py` | 80 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_deployment_api.py` | `.py` | 297 | `FULLY_READ` | H-07, H-08, NFR-SEC-005, TEST-DEL-1 | Complete text read and indexed |
| `tests/unit/test_deployment_artifacts.py` | `.py` | 37 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_deterministic_rule_engine.py` | `.py` | 129 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_diff_hunk.py` | `.py` | 148 | `FULLY_READ` | FR-CODE-003 | Complete text read and indexed |
| `tests/unit/test_dlq_source_admission.py` | `.py` | 67 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_document_references.py` | `.py` | 182 | `FULLY_READ` | FR-CONN-006, G2-SRC-CONF-004, G2-SRC-CONF-005, G2-T0225, G2-T0405 | Complete text read and indexed |
| `tests/unit/test_documentation_audit.py` | `.py` | 204 | `FULLY_READ` | FR-KGR-001, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-999 | Complete text read and indexed |
| `tests/unit/test_domain_packs.py` | `.py` | 185 | `FULLY_READ` | GAP-DP-001, GAP-DP-T-001 | Complete text read and indexed |
| `tests/unit/test_domain_packs_wave2.py` | `.py` | 94 | `FULLY_READ` | SR-COM-020, SR-COM-021 | Complete text read and indexed |
| `tests/unit/test_dual_semantic_model.py` | `.py` | 119 | `FULLY_READ` | FR-GRAPH-010, GAP-DUAL-001, GAP-DUAL-002 | Complete text read and indexed |
| `tests/unit/test_edge_dedup.py` | `.py` | 146 | `FULLY_READ` | FR-INGEST-003 | Complete text read and indexed |
| `tests/unit/test_egress_gateway.py` | `.py` | 560 | `FULLY_READ` | SR-CON-010, SR-LLM-010, SR-LLM-011, SR-LLM-012, SR-LLM-013, SR-LLM-014, SR-LLM-015, SR-LLM-016, SR-LLM-018 | Complete text read and indexed |
| `tests/unit/test_ekaf_conflicts.py` | `.py` | 64 | `FULLY_READ` | G2-EKAF-022 | Complete text read and indexed |
| `tests/unit/test_ekaf_drift.py` | `.py` | 111 | `FULLY_READ` | G2-EKAF-017, G2-EKAF-018 | Complete text read and indexed |
| `tests/unit/test_embeddings.py` | `.py` | 198 | `FULLY_READ` | GAP-SEARCH-001 | Complete text read and indexed |
| `tests/unit/test_engineering_disciplines.py` | `.py` | 560 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_engineering_platform_router.py` | `.py` | 113 | `FULLY_READ` | H-03 | Complete text read and indexed |
| `tests/unit/test_enterprise_advanced.py` | `.py` | 327 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_enterprise_features.py` | `.py` | 672 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_enterprise_gap_completion.py` | `.py` | 194 | `FULLY_READ` | GAP-AGOV-001, GAP-AGOV-002, GAP-AGOV-003, GAP-AGOV-004, GAP-AGOV-005, GAP-AGOV-008, GAP-AGOV-009, GAP-AGOV-010, GAP-AGOV... | Complete text read and indexed |
| `tests/unit/test_enterprise_infrastructure.py` | `.py` | 414 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_enterprise_readiness_wp51.py` | `.py` | 244 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_enterprise_resilience.py` | `.py` | 318 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_enterprise_security_wp55.py` | `.py` | 224 | `FULLY_READ` | GAP-SEC-008, GAP-SEC-009, GAP-SEC-010, GAP-SEC-011, GAP-SEC-012 | Complete text read and indexed |
| `tests/unit/test_eql.py` | `.py` | 230 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_evidence_addressable_rag.py` | `.py` | 111 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_expertise_freshness.py` | `.py` | 109 | `FULLY_READ` | GAP-FRESH-001, GAP-REC-001 | Complete text read and indexed |
| `tests/unit/test_extended_api_routes.py` | `.py` | 352 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_extended_api_routes_pass2.py` | `.py` | 323 | `FULLY_READ` | GAP-OBS-003, GAP-SEARCH-001 | Complete text read and indexed |
| `tests/unit/test_federation_planner.py` | `.py` | 383 | `FULLY_READ` | GAP-FABRIC-001, GAP-FABRIC-002, GAP-FABRIC-003, GAP-FABRIC-004, GAP-FABRIC-005, GAP-FABRIC-006, GAP-FABRIC-007, GAP-FABR... | Complete text read and indexed |
| `tests/unit/test_file_archives.py` | `.py` | 171 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_file_ingestion.py` | `.py` | 238 | `FULLY_READ` | G2-EKAF-025, G2-SYNC-011 | Complete text read and indexed |
| `tests/unit/test_file_parsers.py` | `.py` | 396 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_format_converter.py` | `.py` | 132 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_freshness_drift_audit.py` | `.py` | 115 | `FULLY_READ` | GAP-FRESH-002, GAP-FRESH-003, GAP-FRESH-004, GAP-FRESH-005 | Complete text read and indexed |
| `tests/unit/test_future_scope.py` | `.py` | 286 | `FULLY_READ` | GAP-CATALOG-005, GAP-FED-004 | Complete text read and indexed |
| `tests/unit/test_g2_domain_graphs.py` | `.py` | 365 | `FULLY_READ` | G2-GRAPH-API-002, G2-GRAPH-API-003, G2-GRAPH-BIZ-002, G2-GRAPH-BIZ-003, G2-GRAPH-DEC-002, G2-GRAPH-DEC-003, G2-GRAPH-OBS... | Complete text read and indexed |
| `tests/unit/test_g2_readiness.py` | `.py` | 101 | `FULLY_READ` | G2-ADMIN-001, G2-ADMIN-017, G2-ARCH-001, G2-ARCHC-001, G2-CAP-001, G2-CAUSE-001, G2-EKAF-001, G2-EVENT-001, G2-EVOL-001,... | Complete text read and indexed |
| `tests/unit/test_gap_coverage.py` | `.py` | 316 | `FULLY_READ` | G2-ARCH-001, G2-ARCH-002, G2-ARCH-003, G2-ARCH-004, G2-ARCH-005, G2-ARCH-006, G2-ARCH-008, G2-ARCH-009, G2-ARCH-010, G2-... | Complete text read and indexed |
| `tests/unit/test_gap_governance_controls.py` | `.py` | 203 | `FULLY_READ` | FR-PROV-001, GAP-AGOV-006, GAP-AGOV-007, GAP-AI-001, GAP-GRAG-006, GAP-KFW-001, GAP-KFW-002, GAP-KFW-003, GAP-KFW-004, G... | Complete text read and indexed |
| `tests/unit/test_gaps_implementations.py` | `.py` | 179 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_github_connector.py` | `.py` | 204 | `FULLY_READ` | FR-CONN-003, G2-SRC-GH-001, G2-SRC-GH-003, G2-SRC-GH-004 | Complete text read and indexed |
| `tests/unit/test_github_ingestion.py` | `.py` | 213 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_gitlab_connector.py` | `.py` | 264 | `FULLY_READ` | FR-CONN-004, G2-SRC-GL-001, G2-SRC-GL-003, G2-SRC-GL-004 | Complete text read and indexed |
| `tests/unit/test_gitlab_ingestion.py` | `.py` | 111 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_gitlab_rest_ingestion.py` | `.py` | 237 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_gitops_and_marketplace_wp52.py` | `.py` | 575 | `FULLY_READ` | GAP-GITOPS-002, GAP-GITOPS-003, GAP-GITOPS-004, GAP-GITOPS-005, GAP-GITOPS-006, GAP-GITOPS-007, GAP-GITOPS-008, GAP-MKT-... | Complete text read and indexed |
| `tests/unit/test_governed_agents.py` | `.py` | 137 | `FULLY_READ` | FR-AGENT-001, FR-AGENT-002, FR-AGENT-003, FR-AGENT-004, FR-AGENT-005, MVP-FR-021 | Complete text read and indexed |
| `tests/unit/test_graph_algorithms.py` | `.py` | 375 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_graph_analytics_service.py` | `.py` | 89 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_graph_backends.py` | `.py` | 272 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_graph_evolution.py` | `.py` | 279 | `FULLY_READ` | FR-GRAPH-009, G2-EKAF-010, G2-EKAF-016, G2-EKAF-024, G2-REL-005, G2-SYNC-004, G2-SYNC-006, G2-SYNC-007, G2-T0210, G2-T02... | Complete text read and indexed |
| `tests/unit/test_graph_evolution_family.py` | `.py` | 273 | `FULLY_READ` | G2-EVOL-002, G2-EVOL-003, G2-EVOL-004, G2-EVOL-005, G2-EVOL-006, G2-EVOL-007, G2-EVOL-008, G2-EVOL-009, G2-EVOL-010, G2-... | Complete text read and indexed |
| `tests/unit/test_graph_intelligence.py` | `.py` | 237 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_graph_recommender.py` | `.py` | 76 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_graph_traversal.py` | `.py` | 137 | `FULLY_READ` | FR-GRAPH-006, FR-QUERY-003 | Complete text read and indexed |
| `tests/unit/test_graphtest_framework.py` | `.py` | 260 | `FULLY_READ` | GAP-GRAPHTEST-001 | Complete text read and indexed |
| `tests/unit/test_ha_lease.py` | `.py` | 105 | `FULLY_READ` | GAP-HA-001 | Complete text read and indexed |
| `tests/unit/test_hubble_setup.py` | `.py` | 86 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_hybrid_search_engine.py` | `.py` | 347 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_i2r_intelligence.py` | `.py` | 101 | `FULLY_READ` | G2-I2R-002, G2-I2R-003, G2-I2R-004, G2-I2R-005 | Complete text read and indexed |
| `tests/unit/test_identity_candidates.py` | `.py` | 105 | `FULLY_READ` | FR-ID-002, GAP-ER-005 | Complete text read and indexed |
| `tests/unit/test_identity_ingestion.py` | `.py` | 109 | `FULLY_READ` | FR-ID-001 | Complete text read and indexed |
| `tests/unit/test_identity_resolver.py` | `.py` | 34 | `FULLY_READ` | FR-INGEST-002, G2-EKAF-026 | Complete text read and indexed |
| `tests/unit/test_incremental_indexer.py` | `.py` | 148 | `FULLY_READ` | KGR-G-012 | Complete text read and indexed |
| `tests/unit/test_ingestion_api.py` | `.py` | 187 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_jira_connector.py` | `.py` | 206 | `FULLY_READ` | CONN-03, G2-SRC-JIRA-002, G2-SRC-JIRA-003, G2-SRC-JIRA-004, G2-SRC-JIRA-005, G2-SRC-JIRA-006 | Complete text read and indexed |
| `tests/unit/test_jira_ingestion.py` | `.py` | 224 | `FULLY_READ` | FR-CONN-002, FR-CONN-007, FR-INGEST-001, FR-INGEST-005 | Complete text read and indexed |
| `tests/unit/test_json_processor.py` | `.py` | 234 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgci_pipeline.py` | `.py` | 279 | `FULLY_READ` | GAP-KGCI-001, GAP-KGCI-004 | Complete text read and indexed |
| `tests/unit/test_kgr_ai_intelligence.py` | `.py` | 306 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_anomaly.py` | `.py` | 95 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_centrality.py` | `.py` | 247 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_combo.py` | `.py` | 120 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_community.py` | `.py` | 151 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_community_labels.py` | `.py` | 89 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_competitive_parity.py` | `.py` | 163 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_diff.py` | `.py` | 94 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_endpoints.py` | `.py` | 117 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_events.py` | `.py` | 96 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_export.py` | `.py` | 129 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_filters.py` | `.py` | 129 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_metrics.py` | `.py` | 155 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_orphaned.py` | `.py` | 101 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_paths.py` | `.py` | 117 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_phase2.py` | `.py` | 144 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_pr_impact.py` | `.py` | 106 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_similarity.py` | `.py` | 143 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_structure.py` | `.py` | 149 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_surprise.py` | `.py` | 102 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_visual_intelligence.py` | `.py` | 281 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_kgr_whatif.py` | `.py` | 141 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_knowledge_debt.py` | `.py` | 286 | `FULLY_READ` | G2-KD-002, G2-KD-003, G2-KD-004, G2-KD-005, G2-KD-006, G2-P7 | Complete text read and indexed |
| `tests/unit/test_knowledge_products.py` | `.py` | 230 | `FULLY_READ` | GAP-KP-001, GAP-KP-002, GAP-KP-003, GAP-KP-004, GAP-KP-005 | Complete text read and indexed |
| `tests/unit/test_layered_config.py` | `.py` | 471 | `FULLY_READ` | H-05, SR-CFG-001, SR-CFG-002, SR-CFG-003, SR-CFG-004, SR-CFG-005, SR-CFG-006 | Complete text read and indexed |
| `tests/unit/test_learning_and_reports.py` | `.py` | 362 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_lens_playback.py` | `.py` | 391 | `FULLY_READ` | G2-P10 | Complete text read and indexed |
| `tests/unit/test_licensing.py` | `.py` | 336 | `FULLY_READ` | SR-COM-001, SR-DEP-007, SR-TEN-009 | Complete text read and indexed |
| `tests/unit/test_live_dlq_report.py` | `.py` | 86 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_local_nlp_pipeline.py` | `.py` | 100 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_loops_library.py` | `.py` | 427 | `FULLY_READ` | GAP-LOOP-001 | Complete text read and indexed |
| `tests/unit/test_manifest_integrity.py` | `.py` | 45 | `FULLY_READ` | FR-ONTO-001, FR-ONTO-002 | Complete text read and indexed |
| `tests/unit/test_marketplace.py` | `.py` | 273 | `FULLY_READ` | GAP-EXT-001, GAP-MKT-001 | Complete text read and indexed |
| `tests/unit/test_mcp_pr_tools.py` | `.py` | 124 | `FULLY_READ` | KGR-G-017 | Complete text read and indexed |
| `tests/unit/test_mcp_tools.py` | `.py` | 87 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_meta_graph.py` | `.py` | 192 | `FULLY_READ` | FR-GRAPH-002, FR-GRAPH-005 | Complete text read and indexed |
| `tests/unit/test_metrics.py` | `.py` | 99 | `FULLY_READ` | GAP-OBS-003 | Complete text read and indexed |
| `tests/unit/test_missing_tiers.py` | `.py` | 556 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_model_governance.py` | `.py` | 267 | `FULLY_READ` | GAP-AGOV-012 | Complete text read and indexed |
| `tests/unit/test_moonshots.py` | `.py` | 397 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_mutation_stream.py` | `.py` | 123 | `FULLY_READ` | KGR-G-020 | Complete text read and indexed |
| `tests/unit/test_named_graph_isolation.py` | `.py` | 98 | `FULLY_READ` | KGR-G-013 | Complete text read and indexed |
| `tests/unit/test_new_endpoints.py` | `.py` | 341 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_observability.py` | `.py` | 77 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_ontology_drift_review.py` | `.py` | 99 | `FULLY_READ` | G2-OEVO-001 | Complete text read and indexed |
| `tests/unit/test_ontology_evolution_family.py` | `.py` | 146 | `FULLY_READ` | G2-OEVO-002, G2-OEVO-003, G2-OEVO-004, G2-OEVO-005, G2-OEVO-006 | Complete text read and indexed |
| `tests/unit/test_ontology_gitops.py` | `.py` | 89 | `FULLY_READ` | GAP-GITOPS-001 | Complete text read and indexed |
| `tests/unit/test_ontology_induction.py` | `.py` | 139 | `FULLY_READ` | KGR-G-015 | Complete text read and indexed |
| `tests/unit/test_operational_recovery.py` | `.py` | 318 | `FULLY_READ` | G2-REL-007, G2-T0122, G2-T0123, NFR-REL-002, TEST-1 | Complete text read and indexed |
| `tests/unit/test_ops.py` | `.py` | 233 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_optional_integrations.py` | `.py` | 391 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_otel_connector.py` | `.py` | 78 | `FULLY_READ` | G2-SRC-OTEL-002, G2-SRC-OTEL-003, G2-SRC-OTEL-004, G2-SRC-OTEL-005 | Complete text read and indexed |
| `tests/unit/test_parallel_multihop.py` | `.py` | 112 | `FULLY_READ` | KGR-G-018 | Complete text read and indexed |
| `tests/unit/test_performance_reliability_and_operations_wp72.py` | `.py` | 518 | `FULLY_READ` | G2-PERF-002, G2-PERF-003, G2-PERF-004, G2-PERF-005, G2-PERF-006, G2-PERF-007, G2-PERF-008, G2-REL-002, G2-REL-003, G2-RE... | Complete text read and indexed |
| `tests/unit/test_phase2_api.py` | `.py` | 54 | `FULLY_READ` | G2-SYNC-009 | Complete text read and indexed |
| `tests/unit/test_phase2_connectors.py` | `.py` | 233 | `FULLY_READ` | CONN-01, FR-CONF-001, FR-CONN-005, FR-SNOW-001 | Complete text read and indexed |
| `tests/unit/test_phase2_hugegraph_schema.py` | `.py` | 393 | `FULLY_READ` | FR-GRAPH-003, FR-GRAPH-008, FR-INGEST-003, G2-SRC-CONF-004, H-01 | Complete text read and indexed |
| `tests/unit/test_phase2_ingestion.py` | `.py` | 353 | `FULLY_READ` | FR-CONF-001, FR-CONN-006, FR-SNOW-001, G2-EKAF-014 | Complete text read and indexed |
| `tests/unit/test_phase2_rdf_export.py` | `.py` | 137 | `FULLY_READ` | FR-GRAPH-010 | Complete text read and indexed |
| `tests/unit/test_phase4_accessibility.py` | `.py` | 65 | `FULLY_READ` | TEST-005, UI-001, UI-002, UI-003, UI-004, UI-005, UI-006, UI-007, UI-009 | Complete text read and indexed |
| `tests/unit/test_phase4_compliance_and_search.py` | `.py` | 108 | `FULLY_READ` | COMPLY-003, UI-008 | Complete text read and indexed |
| `tests/unit/test_phase4_core_engines.py` | `.py` | 397 | `FULLY_READ` | CORE-001, CORE-002, CORE-003, CORE-004, CORE-005, CORE-006 | Complete text read and indexed |
| `tests/unit/test_phase4_load.py` | `.py` | 54 | `FULLY_READ` | TEST-002 | Complete text read and indexed |
| `tests/unit/test_phase4_perf_regression.py` | `.py` | 66 | `FULLY_READ` | TEST-004 | Complete text read and indexed |
| `tests/unit/test_phase4_phase2_engines.py` | `.py` | 450 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, AI-003, GRAPH-001, GRAPH-002, GRAPH-003, GRAPH-004, GRAPH-005, GRAPH-006 | Complete text read and indexed |
| `tests/unit/test_phase4_phase3_engines.py` | `.py` | 386 | `FULLY_READ` | AI-001, AI-002, AI-004, AI-005, AI-006, AI-007 | Complete text read and indexed |
| `tests/unit/test_phase4_phase4_engines.py` | `.py` | 311 | `FULLY_READ` | INFRA-001, INFRA-002, INFRA-004, INFRA-005, INFRA-006, INFRA-007 | Complete text read and indexed |
| `tests/unit/test_phase4_phase6_7_engines.py` | `.py` | 225 | `FULLY_READ` | COMPLY-001, COMPLY-002, MULTI-001, MULTI-002, TEST-001 | Complete text read and indexed |
| `tests/unit/test_phase4_preflight.py` | `.py` | 65 | `FULLY_READ` | AGENT-001, AGENT-002, AGENT-003, AGENT-004, AI-001, AI-002, AI-003, AI-004, AI-005, AI-006, AI-007, COMPLY-001 (+39 more... | Complete text read and indexed |
| `tests/unit/test_pipeline.py` | `.py` | 131 | `FULLY_READ` | TEST-1 | Complete text read and indexed |
| `tests/unit/test_platform_and_ecosystem_moonshots_wp61.py` | `.py` | 357 | `FULLY_READ` | G2-PM-002, G2-PM-003, G2-PM-004, G2-PM-005, MS-11, MS-12, MS-13, MS-16, MS-17, MS-25, MS-26, MS-27 (+2 more) | Complete text read and indexed |
| `tests/unit/test_platform_modules.py` | `.py` | 652 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_privacy.py` | `.py` | 347 | `FULLY_READ` | SR-PRV-001, SR-PRV-006 | Complete text read and indexed |
| `tests/unit/test_process_mining.py` | `.py` | 156 | `FULLY_READ` | G2-P7 | Complete text read and indexed |
| `tests/unit/test_product_intelligence.py` | `.py` | 134 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_production_release_gate_wp8.py` | `.py` | 314 | `FULLY_READ` | CG-GAP-008, MVP-FR-028, REL-01, REL-02, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-09, REL-10 (+5 more) | Complete text read and indexed |
| `tests/unit/test_production_topology.py` | `.py` | 54 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_provenance.py` | `.py` | 46 | `FULLY_READ` | FR-PROV-002, TEST-1 | Complete text read and indexed |
| `tests/unit/test_qa_gate_integrity.py` | `.py` | 361 | `FULLY_READ` | SR-QA-010, SR-QA-011, SR-QA-012, SR-QA-013, SR-QA-014 | Complete text read and indexed |
| `tests/unit/test_quality.py` | `.py` | 100 | `FULLY_READ` | FR-VALID-003 | Complete text read and indexed |
| `tests/unit/test_query_budget.py` | `.py` | 41 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_query_cache.py` | `.py` | 74 | `FULLY_READ` | GAP-CACHE-001 | Complete text read and indexed |
| `tests/unit/test_query_executor.py` | `.py` | 146 | `FULLY_READ` | FR-QUERY-001, FR-QUERY-002, FR-QUERY-003, FR-QUERY-004, FR-QUERY-007, TEST-1 | Complete text read and indexed |
| `tests/unit/test_query_intelligence.py` | `.py` | 198 | `FULLY_READ` | FR-GRAPH-007, GAP-QI-001, GAP-QI-002, GAP-QI-003, GAP-QI-004, GAP-QI-007 | Complete text read and indexed |
| `tests/unit/test_query_intelligence_risks.py` | `.py` | 94 | `FULLY_READ` | GAP-QI-005, GAP-QI-006, GAP-QI-008 | Complete text read and indexed |
| `tests/unit/test_query_languages.py` | `.py` | 266 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_query_nl.py` | `.py` | 311 | `FULLY_READ` | FR-QUERY-005 | Complete text read and indexed |
| `tests/unit/test_query_operators.py` | `.py` | 185 | `FULLY_READ` | G2-P7 | Complete text read and indexed |
| `tests/unit/test_query_policy.py` | `.py` | 64 | `FULLY_READ` | FR-QUERY-006, FR-QUERY-008 | Complete text read and indexed |
| `tests/unit/test_question_operators_g2.py` | `.py` | 154 | `FULLY_READ` | G2-QOP-002, G2-QOP-003, G2-QOP-004, G2-QOP-005, G2-QOP-006, G2-QOP-007, G2-QOP-008, G2-QOP-009 | Complete text read and indexed |
| `tests/unit/test_rag_abstention.py` | `.py` | 145 | `FULLY_READ` | GAP-KRAG-007 | Complete text read and indexed |
| `tests/unit/test_recovery_bundle.py` | `.py` | 278 | `FULLY_READ` | G2-REL-007, NFR-REL-002 | Complete text read and indexed |
| `tests/unit/test_replay.py` | `.py` | 76 | `FULLY_READ` | FR-CONN-006 | Complete text read and indexed |
| `tests/unit/test_reports.py` | `.py` | 230 | `FULLY_READ` | SR-NLQ-008 | Complete text read and indexed |
| `tests/unit/test_repository_ingestion.py` | `.py` | 140 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_requirement_evidence.py` | `.py` | 153 | `FULLY_READ` | FR-CODE-001, FR-GRAPH-001, MVP-FR-001 | Complete text read and indexed |
| `tests/unit/test_retrieval.py` | `.py` | 85 | `FULLY_READ` | FR-RAG-001, FR-RAG-002, FR-RAG-003, FR-RAG-004, MVP-FR-020 | Complete text read and indexed |
| `tests/unit/test_retrieval_eval.py` | `.py` | 117 | `FULLY_READ` | FR-RAG-005 | Complete text read and indexed |
| `tests/unit/test_retrieval_vector.py` | `.py` | 191 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_runtime_connector.py` | `.py` | 62 | `FULLY_READ` | G2-SRC-RUNTIME-002, G2-SRC-RUNTIME-003 | Complete text read and indexed |
| `tests/unit/test_sbom_connector.py` | `.py` | 101 | `FULLY_READ` | G2-SRC-SBOM-002, G2-SRC-SBOM-003, G2-SRC-SBOM-004 | Complete text read and indexed |
| `tests/unit/test_scale_and_polish_wp71.py` | `.py` | 140 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_schema_profiler.py` | `.py` | 328 | `FULLY_READ` | SR-ING-010, SR-ING-012, SR-ING-013, SR-ING-016 | Complete text read and indexed |
| `tests/unit/test_search_facets.py` | `.py` | 197 | `FULLY_READ` | GAP-SEARCH-001, GAP-SEARCH-002 | Complete text read and indexed |
| `tests/unit/test_self_llm_frontier.py` | `.py` | 321 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_semantic_consumers_reconciliation.py` | `.py` | 141 | `FULLY_READ` | G2-EVENT-002, G2-EVENT-003, G2-EVENT-004, G2-EVENT-005, G2-EVENT-006, G2-EVENT-007, G2-SYNC-003, G2-SYNC-005, G2-SYNC-00... | Complete text read and indexed |
| `tests/unit/test_semantic_pipeline.py` | `.py` | 153 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_servicenow_connector.py` | `.py` | 144 | `FULLY_READ` | CONN-02, FR-SNOW-001, G2-SRC-SNKB-002, G2-SRC-SNKB-003, G2-SRC-SNOW-002, G2-SRC-SNOW-003, G2-SRC-SNOW-004, G2-SRC-SNOW-0... | Complete text read and indexed |
| `tests/unit/test_servicenow_upstream_fixture.py` | `.py` | 57 | `FULLY_READ` | FR-SNOW-001 | Complete text read and indexed |
| `tests/unit/test_simulation.py` | `.py` | 522 | `FULLY_READ` | G2-P9 | Complete text read and indexed |
| `tests/unit/test_skos_taxonomy.py` | `.py` | 234 | `FULLY_READ` | GAP-STUDIO-005, GAP-TAX-001 | Complete text read and indexed |
| `tests/unit/test_snapshots.py` | `.py` | 102 | `FULLY_READ` | G2-T0224, G2-T0225, NFR-REL-003 | Complete text read and indexed |
| `tests/unit/test_source_registry.py` | `.py` | 103 | `FULLY_READ` | G2-EKAF-001, G2-EKAF-021, G2-EKAF-028, G2-T0004, G2-T0101, G2-T0102 | Complete text read and indexed |
| `tests/unit/test_sr_wave_api_routes.py` | `.py` | 271 | `FULLY_READ` | SR-CFG-001, SR-COM-001, SR-CON-010, SR-DEP-007, SR-GOV-001, SR-ING-010, SR-LLM-010, SR-NLQ-002, SR-NLQ-008, SR-ONT-007, ... | Complete text read and indexed |
| `tests/unit/test_strategy_registry.py` | `.py` | 173 | `FULLY_READ` | FR-RAG-006 | Complete text read and indexed |
| `tests/unit/test_streaming_agent_memory.py` | `.py` | 133 | `FULLY_READ` | KGR-G-014 | Complete text read and indexed |
| `tests/unit/test_suggested_advanced_capabilities.py` | `.py` | 294 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_suggestion_engine.py` | `.py` | 165 | `FULLY_READ` | SR-NLQ-001, SR-NLQ-003 | Complete text read and indexed |
| `tests/unit/test_systems_registry.py` | `.py` | 466 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_temporal_model_family.py` | `.py` | 166 | `FULLY_READ` | G2-TIME-002, G2-TIME-003, G2-TIME-004, G2-TIME-005, G2-TIME-006, G2-TIME-007 | Complete text read and indexed |
| `tests/unit/test_tenancy.py` | `.py` | 428 | `FULLY_READ` | SR-TEN-001, SR-TEN-002, SR-TEN-006, SR-TEN-007, SR-TEN-009 | Complete text read and indexed |
| `tests/unit/test_trust_health_and_frontier_moonshots_wp62.py` | `.py` | 658 | `FULLY_READ` | G2-IMMUNE-002, G2-IMMUNE-003, G2-IMMUNE-004, G2-IMMUNE-005, G2-IMMUNE-006, G2-IMMUNE-007, G2-IMMUNE-008, G2-IMMUNE-009, ... | Complete text read and indexed |
| `tests/unit/test_truth_claims.py` | `.py` | 164 | `FULLY_READ` | GAP-TRUTH-001 | Complete text read and indexed |
| `tests/unit/test_truth_resolution.py` | `.py` | 192 | `FULLY_READ` | GAP-TRUTH-002, GAP-TRUTH-003, GAP-TRUTH-004, GAP-TRUTH-005, GAP-TRUTH-006, GAP-TRUTH-007, GAP-TRUTH-008, GAP-TRUTH-009, ... | Complete text read and indexed |
| `tests/unit/test_twin_domains.py` | `.py` | 420 | `FULLY_READ` | G2-P6 | Complete text read and indexed |
| `tests/unit/test_uncertainty_protocol.py` | `.py` | 77 | `FULLY_READ` | KGR-G-019 | Complete text read and indexed |
| `tests/unit/test_unified_query_api.py` | `.py` | 109 | `FULLY_READ` | - | Complete text read and indexed |
| `tests/unit/test_validation_engine.py` | `.py` | 224 | `FULLY_READ` | FR-VALID-001, FR-VALID-002, TEST-1 | Complete text read and indexed |
| `tests/unit/test_validation_source_binding.py` | `.py` | 279 | `FULLY_READ` | MVP-FR-027 | Complete text read and indexed |
| `tests/unit/test_vector_graph.py` | `.py` | 96 | `FULLY_READ` | KGR-G-016 | Complete text read and indexed |
| `tests/unit/test_vscode_extension_wp54.py` | `.py` | 155 | `FULLY_READ` | FR-VSCODE-001, FR-VSCODE-002, G2-VSC-002, G2-VSC-003, G2-VSC-004, G2-VSC-005, G2-VSC-006, G2-VSC-007, G2-VSC-008, MVP-FR... | Complete text read and indexed |
| `tests/unit/test_web_crawler_connector.py` | `.py` | 124 | `FULLY_READ` | G2-SRC-WEB-002, G2-SRC-WEB-003, G2-SRC-WEB-004, G2-SRC-WEB-005 | Complete text read and indexed |
| `tests/unit/test_web_ux_and_admin_wp53.py` | `.py` | 353 | `FULLY_READ` | FR-ADMIN-001, FR-ADMIN-002, FR-UI-001, FR-UI-002, G2-ADMIN-002, G2-ADMIN-003, G2-ADMIN-004, G2-ADMIN-005, G2-ADMIN-006, ... | Complete text read and indexed |
| `tests/unit/test_webhook_recovery.py` | `.py` | 0 | `FULLY_READ` | - | Complete text read and indexed |
| `todo-status.md` | `.md` | 25 | `FULLY_READ` | - | Complete text read and indexed |

## Requirement Extraction Notes

The scanner found 2,582 unique explicit IDs before removing scratch self-references; the normalized union with the registry plus separately identified atomic clauses is 2,603. Un-IDed normative candidate lines were reviewed as acceptance criteria, constraints, conflicts or explanatory context. The unnumbered Self-LLM completion claim was promoted to `DERIVED-LLM-SELF-001` because it is independently testable and materially diverges from implementation semantics. Repeated headings, WHY/rationale text and historical audit assertions were not minted as duplicate requirements. Original IDs remain in the master traceability matrix so every source citation can be followed.

## Integration Inventory Receipt

The live OpenAPI 3.1 document supplied 689 paths, 734 REST operations and 303 schemas. Source AST indexing found 744 HTTP route decorators; prefix composition and non-HTTP wiring explain count differences. One WebSocket route was separately traced at `apps/api/main.py:1489-1500`. Full operation-level details are embedded in `GUI-UIX-requirements.md` section 17.

## Quality Gate Receipt

- [x] Every in-scope Markdown file appears and was fully read; user-excluded demo/example Markdown is explicitly listed.
- [x] Every normalized explicit requirement has status, source, evidence/test field, root cause and remediation.
- [x] Historical labels and path existence were not accepted as implementation proof.
- [x] Every GUI screen references existing `INT-*` or flagged `BACKEND-MISSING-*` IDs.
- [x] Existing frontend design was excluded from the redesign input.
- [x] Every named frontend library has a version verified from current npm metadata on 2026-10-13.
- [x] Four theme modes, graph mechanics, all screen states, acceptance criteria and open questions are specified.
- [x] Fresh verification limitations and incomplete full-suite result are disclosed.
