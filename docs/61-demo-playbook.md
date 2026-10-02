# EOIP Demo Playbook

**Project:** Enterprise Ontology & Intelligence Platform  
**Version:** 0.1.0-architecture-baseline  
**Purpose:** Step-by-step clean-reset demo for the Phase 1 vertical slice

## Prerequisites

- Docker Desktop (or Docker Engine + Compose v2) with at least 8 GB RAM allocated
- PowerShell (Windows) or Bash (Linux/macOS)
- No internet connection required after initial image build

## 1. Clean environment start

```powershell
# From the repository root
.\scripts\docker.ps1 up
```

This will:
1. Generate credentials in `deploy/.env` if not present
2. Build application and web images
3. Start HugeGraph with RocksDB persistence
4. Initialize the graph schema (idempotent)
5. Start the API, worker, MCP, and web services
6. The worker automatically loads demo fixtures (Jira + Git + code)

Wait for all services to report healthy (approximately 60-90 seconds).

## 2. Verify readiness

```powershell
.\scripts\docker.ps1 status
```

All services should show `healthy`. The API documentation is at http://localhost:8000/docs.

## 3. Access the web application

Open http://localhost:8080 in a browser.

1. **Connect** using the `EOIP_API_TOKEN` from `deploy/.env`
2. The dashboard shows entity and relationship counts from HugeGraph
3. Search for `EOIP-1` to see the demo Jira work item

## 4. Demonstrate the evidence path

The golden demo path traces: **Jira Story -> Merge Request -> Commit -> Source File -> Function -> Dependency**

### 4a. Search and explore

1. Search `EOIP-1` — the work item appears in the graph visualization
2. Click the work item node to inspect its properties and source evidence
3. Click **Explore impact** to see all connected entities

### 4b. Trace a requirement to code

1. Search `compute_impact` — find the CodeSymbol
2. Use the **Trace** form: set source to `urn:eoip:work:item:jira:EOIP-1` and target to the symbol's canonical ID
3. The path shows IMPLEMENTS -> MODIFIES -> DECLARES edges with evidence

### 4c. Run TraceImpact agent

1. Select any entity and click **Run TraceImpact**
2. The agent returns a summary with evidence references and source citations
3. This uses deterministic graph traversal — no LLM required

### 4d. Administration

1. Switch to the **Administration** tab
2. View ingestion job history with status and record counts
3. Click **Run validation** to check graph integrity
4. The entity inventory shows counts by vertex label

## 5. API demonstration

```bash
# Health check
curl http://localhost:8000/health/ready

# Search (requires Bearer token)
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/search?q=EOIP-1"

# Path query
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/path \
  -d '{"source_id":"urn:eoip:work:item:jira:EOIP-1","target_id":"urn:eoip:code:symbol:demo:service.py:compute_impact"}'

# Impact analysis
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/impact \
  -d '{"canonical_id":"urn:eoip:work:item:jira:EOIP-1","max_depth":4}'

# TraceImpact agent
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/agents/trace-impact \
  -d '{"canonical_id":"urn:eoip:work:item:jira:EOIP-1"}'

# GraphRAG (deterministic fallback, no model required)
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/rag \
  -d '{"canonical_id":"urn:eoip:work:item:jira:EOIP-1","question":"What code implements this requirement?"}'

# Validation
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/admin/validation

# Ontology export (JSON-LD)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/ontology/export
```

## 6. MCP demonstration

The MCP server exposes read-only tools at http://localhost:8001/mcp, including:

- `search` — search entities by identifier or name
- `entity` — read entity with relationships
- `path` — find shortest path between entities
- `impact` — bounded impact analysis
- `lineage` — trace to source evidence
- `trace_impact` — run the TraceImpact agent
- `code_symbol` / `jira_issue` — look up code or Jira context
- `evidence` / `query` — retrieve evidence or execute a QueryPlan

No write tools are advertised.

## 7. VS Code extension

1. Install `apps/vscode-extension/dist/eoip-context-0.1.0.vsix`
2. Set the API token via the **EOIP: Set Token** command
3. Use **EOIP: Search** to find entities
4. Use **EOIP: Context**, **Impact**, **Path** commands on symbols
5. The extension remains functional (editing works) when EOIP is offline

## 8. Backup and restore

```powershell
# Create backup
.\scripts\docker.ps1 backup

# Run restore verification (separate HugeGraph instance)
.\scripts\docker.ps1 restore-test
```

The restore test:
1. Starts a clean HugeGraph instance
2. Restores the backup with checksum verification
3. Reruns golden path and impact queries
4. Verifies entity counts match

## 9. Run automated tests

```powershell
.\scripts\docker.ps1 test
```

This runs:
- Unit tests (pytest): contracts, connectors, parsers, graph, ingestion, query, validation, agents, provenance, identity, audit
- Contract tests: GraphStore protocol, QueryPlan validation
- Security tests: path traversal, redaction, policy enforcement, tool allowlists
- Integration tests: MCP transport
- E2E tests: full demo flow with backup/restore cycle
- Performance tests: entity lookup, path/impact query benchmarks
- Smoke tests: full-stack Docker verification including web and MCP
- UI tests (Playwright): login flow and admin panel

## 10. Clean reset

```powershell
.\scripts\docker.ps1 down
# Docker volumes are removed; next `up` starts fresh
```

## Golden expectations

After demo ingestion, the graph contains:
- At least 2 Jira work items (EOIP-1, EOIP-2) with project and person vertices
- Git repository with branches, commits, and file vertices
- Code symbols (functions) with DECLARES, CALLS, IMPORTS edges
- Cross-domain links: IMPLEMENTS (commit -> work item), MODIFIES (commit -> file)
- Evidence vertices linked via EVIDENCED_BY edges
- Ingestion run records linked via INGESTED_IN edges

The path from `EOIP-1` to `compute_impact` traverses:
`WorkItem -[IMPLEMENTS]- Commit -[MODIFIES]- File -[DECLARES]- CodeSymbol`
