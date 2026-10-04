# EOIP Automated Demo — Meridian Financial Services

Runs the full EOIP demo walkthrough non-interactively against an in-memory graph store.
Loads data from 13 source systems across two domains (Payment Gateway and Fraud Detection),
constructs code graphs, processes crawler data, and validates all platform capabilities.

## Usage

```powershell
# Full demo — both domains + all capabilities
.\demo\autodemo\run-demo.bat

# Or run directly with Python
.\.venv\Scripts\python.exe -m demo.autodemo.runner --verbose

# Manual ingestion only (Payment Gateway / PAY domain)
.\demo\autodemo\run-demo.bat manual

# Pipeline ingestion only (Fraud Detection / FRD domain)
.\demo\autodemo\run-demo.bat pipeline

# Save results to JSON
.\.venv\Scripts\python.exe -m demo.autodemo.runner --output demo/autodemo/results.json
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
