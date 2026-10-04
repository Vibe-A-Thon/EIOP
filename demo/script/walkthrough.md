# EOIP Demo Walkthrough Script

Step-by-step guide for presenting the EOIP Phase 1 vertical slice.
Estimated duration: 20 minutes for the full walkthrough, 10 minutes for the quick path.

## Prerequisites

- Docker Desktop running with at least 8 GB RAM
- Repository cloned and images built
- No internet connection required after initial setup

## Quick Setup

```powershell
# From the repository root
.\scripts\docker.ps1 up
```

Wait for all services to report healthy (~60-90 seconds):

```powershell
.\scripts\docker.ps1 status
```

## Part 1: Health and Readiness (2 min)

### 1.1 Verify services

```powershell
curl http://localhost:8000/health/ready
```

Expected: `{"status": "ok", ...}` with HugeGraph, schema, and worker ready.

### 1.2 Check API docs

Open http://localhost:8000/docs — the full OpenAPI documentation is auto-generated.

## Part 2: The Golden Evidence Path (5 min)

This is the core demo: trace a business requirement through code to production.

### 2.1 Search for a work item

Open http://localhost:8080 in a browser.

1. Enter `EOIP-1` in the search bar
2. The work item "Trace a requirement to its implementation" appears
3. Click it to see properties and source evidence

**Talking point:** Every entity in the graph is linked to its source. The evidence is not metadata — it is the actual captured event.

### 2.2 Trace the path

```bash
TOKEN="<from deploy/.env>"

curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/path \
  -d '{"source_id":"urn:eoip:work:item:jira:EOIP-1","target_id":"urn:eoip:code:symbol:demo:service.py:compute_impact"}'
```

Expected path: `WorkItem → Commit → File → CodeSymbol`

Edge types traversed: `IMPLEMENTS → MODIFIES → DECLARES`

**Talking point:** This path is computed by bounded BFS over the live graph, not a pre-built index. Every edge has provenance.

### 2.3 Run impact analysis

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/impact \
  -d '{"canonical_id":"urn:eoip:work:item:jira:EOIP-1","max_depth":4}'
```

Shows all entities affected by changes to EOIP-1 with depth and risk classification.

## Part 3: AI-Assisted Analysis (3 min)

### 3.1 TraceImpact agent

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/agents/trace-impact \
  -d '{"canonical_id":"urn:eoip:work:item:jira:EOIP-1"}'
```

Returns a structured explanation with evidence references and confidence score.

**Talking point:** This agent uses deterministic graph traversal — no LLM required. It works offline.

### 3.2 GraphRAG retrieval

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/rag \
  -d '{"canonical_id":"urn:eoip:work:item:jira:EOIP-1","question":"What code implements this requirement?"}'
```

**Talking point:** When a local model is available, answers include synthesis. Without a model, you still get structured graph evidence with citations. No data ever leaves the network.

## Part 4: Enterprise Scenarios (5 min)

### 4.1 Check scenario readiness

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/demo/scenarios
```

All eight scenarios should report `ready: true`.

### 4.2 Intent to runtime (PAY-142)

Search `PAY-142` — trace from the checkout risk-control story through merge request, commit, source file, API contract, and deployment.

### 4.3 Incident root cause (INC0012042)

Search `INC0012042` — correlate the payment latency incident to alerts, the triggering deployment, and the approved remediation change.

### 4.4 API blast radius

Search `Checkout API` — run blast radius to see all downstream dependencies. Use what-if removal to assess architectural risk.

## Part 5: Administration (3 min)

### 5.1 Admin panel

Switch to the **Administration** tab at http://localhost:8080

1. **Overview** — entity and relationship counts from HugeGraph
2. **Ingestion** — job history with status and record counts
3. **Validation** — click "Run validation" to check graph integrity; view QualityRing
4. **Audit** — structured audit log with correlation IDs

### 5.2 Backup and restore

```powershell
.\scripts\docker.ps1 backup
.\scripts\docker.ps1 restore-test
```

**Talking point:** Backup produces a checksummed archive. Restore verification runs golden path queries against a clean instance.

## Part 6: Developer Integration (2 min)

### 6.1 MCP tools

The MCP server at `http://localhost:8001/mcp` exposes 17 read-only tools. No write operations are advertised.

### 6.2 VS Code extension

1. Install `apps/vscode-extension/dist/eoip-context-0.1.0.vsix`
2. Use **EOIP: Search** to find entities from the editor
3. Use **EOIP: Impact** on a selected symbol to see blast radius
4. The extension works in offline mode (editing continues when EOIP is down)

### 6.3 Prometheus metrics

```bash
curl http://localhost:8000/metrics
```

Shows request counts, operation durations, ingestion job transitions.

## Cleanup

```powershell
.\scripts\docker.ps1 down
```

## Quick Path (10 min version)

For a shorter demo, cover only:
1. Health check (30s)
2. Search EOIP-1 and trace the golden path (3 min)
3. TraceImpact agent (2 min)
4. Enterprise scenario PAY-142 (2 min)
5. Admin validation + backup (2 min)

## Honest Boundaries

- The graph and analytics are live behavior over persisted demo data
- Source exports are offline fixtures unless connector credentials are configured
- Model synthesis is optional; all golden paths work without a local model
- Container hardening, production performance, and G2 roadmap items are not demo claims
