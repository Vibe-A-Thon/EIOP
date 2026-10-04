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
4. Traversal enforces a cooperative deadline and applies the remaining time to graph-store requests; expiration returns a partial result. Network timeout semantics and scheduler latency mean an in-flight request is not forcibly interrupted at an exact wall-clock instant.

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

## Enterprise sales scenarios

The default demo job also loads the validated Northstar Commerce scenario pack at `demo/demodata/enterprise/scenario-pack.json`. This is an executable corpus, not UI-only sample text. The live catalog endpoint reports readiness from persisted graph entities:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/demo/scenarios
```

All eight scenarios should report `ready: true` before a customer session.

| Scenario | Start with | Demonstrate |
|---|---|---|
| Intent to runtime | Search `PAY-142` | Trace to commit `c0ffee142`, `risk.py`, `authorize_order`, API contract, tests, pipeline and deployment. |
| Incident root cause | Search `INC0012042` | Correlate alert, log signature and dashboard to deployment `2026.10.1` and emergency change `CHG0031088`. |
| API blast radius | Search `Checkout API` | Explore downstream Risk and Payments APIs; run blast radius, centrality and what-if removal. |
| Release governance | Search `2026.10.1` | Follow release to pipeline, jobs, artifact, test run and production deployment with evidence. |
| Test intelligence | Search `Checkout regression` | Prove TC-884 covers PAY-142, `authorize_order`, and `POST /orders`; show TC-901 resilience coverage. |
| Design to delivery | Search `Northstar Checkout Experience` | Connect the Figma page/component to FTR-42 and US-142. |
| Knowledge provenance | Search `KB00192` | Retrieve the trusted runbook, architecture decision, API and monitor; open evidence/lineage. |
| Graph analytics | Search `Checkout API` in KGR | Run communities, similarity, anomaly detection, link prediction and graph-health/what-if views. |

### Suggested 20-minute pitch

1. Open the scenario catalog endpoint and show all eight green readiness results.
2. Use `PAY-142` for the two-minute intent-to-code trace, including relationship evidence.
3. Pivot to `INC0012042` for the operations story and show the triggering deployment.
4. Open KGR on `Checkout API`; show blast radius and what-if removal to explain architectural risk.
5. Finish with `KB00192` in GraphRAG and emphasize source-linked answers, local deployment, and deterministic fallback.

### Presenter API notes

- Use `/api/v1/path` for the governed PAY-142 intent-to-runtime trace. For the
  broader incident, release, test and design stories use
  `/api/v1/graph/shortest-paths`; that analytics route traverses every current
  relationship type, while the governed path query intentionally applies a
  semantic relationship allowlist.
- Allow up to 30 seconds for the first validation or what-if request after a
  container rebuild. On the verified 2026-10-04 development graph, validation
  completed in 6.3 seconds and Checkout API removal what-if in 15.45 seconds.
- Treat `/api/v1/demo/scenarios` readiness as an entity-availability check, then
  execute at least one path/analytic per story. Readiness alone is not proof that
  every query mode traverses the same relationship vocabulary.

### Honest live-demo boundary

The graph and analytics are live application behavior over persisted demo data. The source exports are offline fixtures unless organization-specific connector URLs and credentials have been configured. Optional model synthesis is not required for any golden path. Native disaster recovery, full-scale production performance, and the remaining G2 P6-P10 roadmap items are not represented by this pack as completed capabilities.
