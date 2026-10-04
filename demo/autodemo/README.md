# EOIP Automated Demo — Meridian Financial Services

The batch launcher starts the Docker Desktop services, waits for health checks, opens the
interactive EOIP web UI, then runs automated validation in a console against an in-memory
graph store. The automated validation loads demo data from 13 source systems across two
domains, constructs code graphs, processes crawler data, and checks platform capabilities.

## Usage

```powershell
# Full demo — both domains + all capabilities
.\demo\autodemo\run-demo.bat

# Run just the automated validation directly with Python (without starting Docker)
.\.venv\Scripts\python.exe -m demo.autodemo.runner --verbose

# Manual ingestion only (Payment Gateway / PAY domain)
.\demo\autodemo\run-demo.bat manual

# Pipeline ingestion only (Fraud Detection / FRD domain)
.\demo\autodemo\run-demo.bat pipeline

# Save results to JSON
.\.venv\Scripts\python.exe -m demo.autodemo.runner --output demo/autodemo/results.json

# Run without writing captures into the default data/autodemo directory
.\demo\autodemo\run-demo.bat manual --quiet --data-dir .tmp\demo-run
```

## What it tests

### Phase 1 — Initialize
1. Graph store initialization with meta-graph bootstrap

### Phase 2 — Multi-Source Ingestion
2. Manual folder ingestion: 13 source files (Rally, Jira, GitLab, ServiceNow, Confluence, Figma, qTest, Kibana, Grafana, Datadog, API Portal, Code Graph, Crawler)
3. Pipeline folder ingestion: same 13 sources for the FRD domain
4. Jira deep ingestion into graph store (PAY and FRD domains)

### Phase 3 — Code Graph
5. Code-graph JSON loading for 4 projects (mfs-payment-gateway, mfs-fraud-engine, mfs-common-libs, mfs-customer-portal)

### Phase 4 — Crawler
6. Crawler data loading from 5 portal types (Wiki, API Portal, DB Schemas, Figma, Observability)

### Phase 5 — Graph Verification
7. Vertex and edge count verification
8. Vertex label diversity check
9. Impact analysis from PAY-* work items

### Phase 6 — RAG Routing
10. RAG pattern routing across 17 patterns (simple, advanced, graph, hybrid, etc.)

### Phase 7 — Agent Dispatch
11. Agent dispatch across 9 categories (tool-using, deliberative, enterprise, etc.)

### Phase 8 — LAYA Analysis
12. LAYA capability enumeration (8 capabilities)
13. LAYA analysis execution (incident summary, release readiness, etc.)

### Phase 9 — Query Examples
14. Query type coverage (12 types: search, path, impact, NL, neighborhood, traceability, etc.)

### Phase 10 — Validation & Quality
15. Graph validation (zero errors expected)
16. Quality metrics (evidence coverage, orphan rate)

### Phase 11 — Graph Before/After
17. Graph growth comparison (vertices and edges added during ingestion)
18. Cross-domain link creation

## Exit codes

- `0` — all steps passed
- `1` — one or more steps failed

## VS Code NLQ and MCP (full mode)

Full mode now runs a separate, visible VS Code window after successful console
checks. The user-approved isolated profile does not modify your regular VS Code
settings, SecretStorage or installed extensions. It loads the **updated 0.1.0
source extension** from this checkout, not the previously packaged/installed VSIX.
Repackaging/installing that VSIX is a separate action.

The window shows JSON results for:
1. **EOIP: Natural Language Query**: impact of the ready live intent-to-runtime
   scenario anchor (currently Northstar PAY-142), including interpreted plan
   and nonempty live graph results.
2. **EOIP: Read-only MCP Tool**: actual JSON-RPC initialization, initialized
   notification, tool discovery and search call.
3. MCP lineage for the search result, with graph/provenance output.

Each result stays visible for 2.5 seconds. This is command/editor automation
inside the real VS Code host, not mouse-click simulation. It uses the existing
API on port 8000 and stateless JSON Streamable HTTP MCP on port 8001; no model
inference or graph writes are performed by this phase. The host closes after the
sequence, and a unique `test-results/vscode-live-demo-*.json` receipt records the
steps and live/fixture boundaries. Failures produce a nonzero launcher exit;
there is no fixture fallback.

Prerequisites: Node.js, existing extension `node_modules`, cached VS Code 1.96.4
at `apps/vscode-extension/.vscode-test/vscode-win32-x64-archive-1.96.4/Code.exe`,
running authenticated API/MCP, and a ready intent-to-runtime demo scenario. The demo does not
download VS Code or install extensions. It passes the token privately to the
isolated host, which stores it in that profile's SecretStorage; the profile is
removed afterward. The launcher reads `EOIP_API_TOKEN` from the process
environment or `deploy/.env` without printing it.

```powershell
# No Docker, secrets, ingestion, desktop window or captures:
.\demo\autodemo\run-demo.bat --mode full --dry-run

# Only the live VS Code portion; does not rebuild/start Docker:
node .\demo\autodemo\vscode-demo.js
```

The console portion remains in-memory fixture validation. Live extension success
does not certify every enterprise scenario, the installed VSIX, manual prompts,
local-model inference or independent QA.
