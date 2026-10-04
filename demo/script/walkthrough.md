# EOIP Demo Walkthrough — Meridian Financial Services

Step-by-step guide for presenting the EOIP platform using Meridian Financial Services demo data.
Estimated duration: 30 minutes for the full walkthrough, 15 minutes for the quick path.

**Organization:** Meridian Financial Services (MFS)
**Domains:** Payment Gateway Modernization (PAY) · Fraud Detection & AML (FRD)
**Graph Authority:** HugeGraph (local-first, no cloud dependency)

---

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

---

## Part 1: Health and Readiness (2 min)

### 1.1 Verify services

```powershell
curl http://localhost:8000/health/ready
```

Expected: `{"status": "ok", ...}` with HugeGraph, schema, and worker ready.

### 1.2 Check API docs

Open http://localhost:8000/docs — the full OpenAPI documentation is auto-generated, covering 40+ endpoints for search, traversal, analytics, ingestion, and administration.

---

## Part 2: Multi-Source Ingestion (5 min)

This section demonstrates EOIP ingesting data from 13 enterprise source systems into a unified knowledge graph.

### 2.1 Manual ingestion — Payment Gateway (PAY domain)

The `demo/demodata/manual/` folder contains offline fixture data for the Payment Gateway Modernization project:

| Source System | File | Key Records |
|---------------|------|-------------|
| Rally | `rally.json` | 3 Epics (EPC-101/102/103), 3 Features, 2 User Stories |
| Jira | `jira.json` | 18 issues: PAY-100 → PAY-321 (Features, Stories, Tasks) |
| GitLab | `gitlab.json` | 7 MRs (!301-!502), 7 pipelines (9001-9007) |
| ServiceNow | `servicenow.json` | 4 changes (CHG0090101-301), 2 incidents (INC0080101/102) |
| Confluence | `confluence.json` | 5 pages: architecture, PCI compliance, settlement, API ref, runbook |
| Figma | `figma.json` | 1 file, 3 pages, 4 components (Payment Portal) |
| qTest | `qtest.json` | 8 test cases (TC-PAY-001-008), 2 suites, 2 test runs |
| Kibana | `kibana.json` | 3 dashboards, 1 index pattern, 2 saved searches |
| Grafana | `grafana.json` | 2 dashboards, 2 alert rules, 2 datasources |
| Datadog | `datadog.json` | 2 dashboards, 4 monitors |
| API Portal | `api-portal.json` | 3 services, 11 endpoints |
| Code Graph | `code-graph.json` | 12 files, 20 symbols, 10 deps, 17 edges |
| Crawler | `crawler-sites.json` | 5 crawled pages from mfs.internal |

**Talking point:** Every source system produces events that are ingested through a connector, mapped to the EOIP schema, validated, and persisted to HugeGraph. No data transformations are lossy — the original payload is captured alongside the mapped entity.

```bash
TOKEN="<from deploy/.env>"

# Ingest Jira data (Payment Gateway)
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/admin/ingestion/json \
  -d @demo/demodata/manual/jira.json
```

### 2.2 Pipeline ingestion — Fraud Detection (FRD domain)

The `demo/demodata/pipelines/` folder contains data for the Fraud Detection & AML project:

| Key Difference | Manual (PAY) | Pipeline (FRD) |
|----------------|-------------|----------------|
| Jira keys | PAY-100 → PAY-321 | FRD-100 → FRD-321 |
| Rally epics | EPC-101/102/103 | EPC-201/202/203 |
| GitLab MRs | !301-!502 | !601-!802 |
| ServiceNow | CHG0090101-301 | CHG0090401-601 |
| Pipeline stages | N/A | 15-stage config in pipeline-config.json |

**Talking point:** Manual and pipeline ingestion produce identical graph structures — the difference is the trigger (human click vs. scheduled automation). The pipeline config defines stages: FETCH → MAP → VALIDATE → MUTATE → VERIFY → LINK → SNAPSHOT.

### 2.3 Run the automated demo

```powershell
# Full demo — both domains + all capabilities
.\demo\autodemo\run-demo.bat

# Manual only (PAY domain)
.\demo\autodemo\run-demo.bat manual

# Pipeline only (FRD domain)
.\demo\autodemo\run-demo.bat pipeline
```

---

## Part 3: Code-Graph Construction (3 min)

### 3.1 Four MFS code repositories

The `demo/demodata/code/` folder contains code-graph JSON for four projects:

| Repository | Files | Symbols | Dependencies | Edges |
|------------|-------|---------|--------------|-------|
| mfs-payment-gateway | 13 | 33 | 11 | 69 |
| mfs-fraud-engine | 13 | 29 | 11 | 70 |
| mfs-common-libs | 8 | 24 | 6 | 44 |
| mfs-customer-portal | 12 | 24 | 8 | 61 |
| **Total** | **46** | **110** | **36** | **244** |

**Talking point:** Code-graph construction parses source files to extract symbols (classes, functions, methods), file structure, and dependency relationships. These are linked to Jira stories, GitLab MRs, and test cases to form a complete traceability chain.

### 3.2 Explore code dependencies

```bash
# Search for the TokenizationService class
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/search?q=TokenizationService"

# Blast radius — what depends on TokenizationService?
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/graph/blast-radius \
  -d '{"canonical_id":"urn:eoip:code:symbol:mfs-payment-gateway:tokenization.service:TokenizationService"}'
```

---

## Part 4: Crawler Data Processing (2 min)

### 4.1 Five portal types crawled

The `demo/demodata/crawler/` folder contains mock crawl results from MFS internal portals:

| Source | File | Pages | Content |
|--------|------|-------|---------|
| Confluence Wiki | `wiki-confluence.json` | 9 | Architecture docs, runbooks, onboarding |
| API Portal | `api-portal-swagger.json` | 6 | Swagger specs, endpoint reference |
| DB Schemas | `db-schemas.json` | 4 | mfs_payments_db, mfs_fraud_db, mfs_audit_db |
| Figma Designs | `figma-designs.json` | 3 | Payment Portal, Fraud Dashboard, Component Library |
| Observability | `observability-portals.json` | 7 | Grafana, Datadog, Kibana, Fortuna, status pages |

**Talking point:** The Controlled Web Crawler operates within policy-defined boundaries — allowed hosts, rate limits, depth limits. It produces SourceEvents with full provenance (URL, content hash, timestamp, link structure) that feed into the knowledge graph.

---

## Part 5: The Golden Evidence Path (5 min)

This is the core demo: trace a business requirement through code to production.

### 5.1 Search for a work item

Open http://localhost:8080 in a browser.

1. Enter `PAY-101` in the search bar
2. The work item "Implement payment tokenization service" appears
3. Click it to see properties and source evidence

**Talking point:** Every entity in the graph is linked to its source. The evidence is not metadata — it is the actual captured event with a payload hash.

### 5.2 Trace the full path

```bash
# Rally Epic → Jira Feature → Story → MR → Commit → File → CodeSymbol
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/traceability \
  -d '{"source":"urn:eoip:work:epic:rally:EPC-101"}'
```

Expected chain: `Epic (EPC-101) → Feature (PAY-100) → Story (PAY-101) → MR (!301) → Pipeline (9001) → Deployment → Pod`

### 5.3 Path from story to code

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/path \
  -d '{"source_id":"urn:eoip:work:item:jira:PAY-101","target_id":"urn:eoip:code:symbol:mfs-payment-gateway:tokenization.service:tokenize_card"}'
```

Expected path: `WorkItem → MergeRequest → Commit → File → CodeSymbol`

### 5.4 Impact analysis

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/impact \
  -d '{"canonical_id":"urn:eoip:code:symbol:mfs-payment-gateway:tokenization.service:tokenize_card","max_depth":3}'
```

Shows all entities affected by changes to `tokenize_card()` — files, dependent symbols, work items, test cases.

### 5.5 Incident root cause (INC0080101)

```bash
# Search for the payment timeout incident
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/v1/search?q=INC0080101"

# Explore its neighborhood
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/neighborhood \
  -d '{"anchor":"urn:eoip:ops:incident:INC0080101","max_depth":2}'
```

Expected: Incident → mfs-payment-gateway → CHG0090101 → Pipeline 9001 → MR !301 → PAY-101

**Talking point:** The same graph that traces requirements forward also traces incidents backward — no separate CMDB integration needed.

---

## Part 6: AI-Assisted Analysis (5 min)

### VS Code live segment (included in full auto-demo)

Watch the separate isolated EOIP 0.1.0 development-host window. First the NLQ
command asks for the live intent-to-runtime anchor's impact (Northstar PAY-142)
and shows the resolved plan and live graph
answer. Then the MCP command displays server/protocol metadata, discovered
tools, search results and lineage. These are real authenticated calls to the
local deployed services, not the console's in-memory graph.

Use `node .\demo\autodemo\vscode-demo.js` to replay only this segment once the
services and a ready intent-to-runtime scenario are available. Inspect the generated live-demo receipt.
The window closes after three steps; each result pauses for 2.5 seconds.
This demonstrates the updated source plugin, not installation of the old VSIX
or model inference. See [prerequisites and boundaries](../autodemo/README.md).

### 6.1 RAG pattern routing (17 patterns)

EOIP routes queries to the optimal RAG pattern based on intent classification:

```bash
# Simple RAG — entity lookup
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/rag \
  -d '{"question":"What is PAY-101?"}'

# Multi-hop RAG — infrastructure to business impact
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/rag \
  -d '{"question":"Which Rally epic is affected if pghost-prod-01.mfs.internal goes down?"}'

# Branched RAG — comparative analysis
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/rag \
  -d '{"question":"Compare the test coverage of Payment Gateway vs Fraud Engine"}'
```

**Talking point:** All 17 RAG patterns (simple, advanced, graph, hybrid, corrective, self, adaptive, agentic, modular, HyDE, conversational, multi-step, multi-hop, branched, multimodal, speculative, RAG-of-RAGs) use the graph as their primary context source. No vector database required — the graph IS the retrieval engine.

### 6.2 Agent dispatch (41 agent types, 9 categories)

```bash
# Compliance agent — PCI DSS verification
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/agents/compliance \
  -d '{"question":"Verify that all cardholder data handling meets PCI DSS encryption and key management requirements"}'

# Blast radius agent — dependency impact
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/agents/blast-radius \
  -d '{"question":"What is the blast radius of upgrading sqlalchemy in mfs-common-libs?"}'
```

Agent categories: Tool-Using · Deliberative · Enterprise · Orchestration · Autonomous · Reactive · Meta-Cognitive · Collaboration · Hybrid

### 6.3 LAYA — Local AI Yield Augmentation (8 capabilities)

```bash
# Incident summary
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/laya \
  -d '{"question":"Summarize the payment timeout spike incident (INC0080101) and its resolution","capability":"incident_summary","context_entities":["urn:eoip:ops:incident:INC0080101"]}'

# Release readiness
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/laya \
  -d '{"question":"Is the Payment Gateway V2 release ready for production?","capability":"release_readiness"}'
```

LAYA capabilities: incident_summary · decision_explanation · release_readiness · runbook_generation · change_risk · entity_explanation · gap_analysis · trend_summary

**Talking point:** LAYA uses a local LLM when available, otherwise falls back to structured graph analysis with deterministic summaries. No data leaves the network.

---

## Part 7: Query Capabilities (3 min)

### 7.1 Twelve query types

| Type | Example | MFS Data |
|------|---------|----------|
| Search | `PAY-101` | Find tokenization story |
| Path | PAY-101 → tokenize_card | Story to code function |
| Impact | tokenize_card blast radius | All dependents |
| Natural Language | "How is HSM key rotation implemented?" | NL → path query |
| Neighborhood | INC0080101 neighbors | Incident context |
| Traceability | EPC-101 full chain | Epic to production |
| Lineage | Payment Gateway API provenance | api-portal, swagger, gitlab |
| EQL | `FIND WorkItem WHERE status = 'In Progress'` | Structured query |
| Cross-Domain | qTest cases covering fraud API | test × api × code |
| Temporal | Changes between Sep 15 – Oct 1 | MRs, deploys, incidents |
| Blast Radius | What breaks if we change X? | Graph-driven |
| What-If | Remove AuthClient from common-libs | Speculative analysis |

### 7.2 Cross-domain query demo

```bash
# Which test cases in qTest cover the fraud scoring API endpoints?
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/v1/query/nl \
  -d '{"query":"Which test cases in qTest cover the fraud scoring API endpoints?"}'
```

---

## Part 8: Administration (3 min)

### 8.1 Admin panel

Switch to the **Administration** tab at http://localhost:8080

1. **Overview** — entity and relationship counts from HugeGraph
2. **Ingestion** — job history with status and record counts for all 13 source systems
3. **Validation** — click "Run validation" to check graph integrity; view QualityRing
4. **Audit** — structured audit log with correlation IDs

### 8.2 Graph statistics

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/graph/statistics
```

Shows vertex counts by label, edge counts by type, and graph-wide metrics.

### 8.3 Backup and restore

```powershell
.\scripts\docker.ps1 backup
.\scripts\docker.ps1 restore-test
```

**Talking point:** Backup produces a checksummed archive. Restore verification runs golden path queries against a clean instance.

---

## Part 9: Developer Integration (2 min)

### 9.1 MCP tools

The MCP server at `http://localhost:8001/mcp` exposes 17 read-only tools. No write operations are advertised.

### 9.2 VS Code extension

1. Install `apps/vscode-extension/dist/eoip-context-0.1.0.vsix`
2. Use **EOIP: Search** to find entities from the editor
3. Use **EOIP: Impact** on a selected symbol to see blast radius
4. The extension works in offline mode (editing continues when EOIP is down)

### 9.3 Prometheus metrics

```bash
curl http://localhost:8000/metrics
```

Shows request counts, operation durations, ingestion job transitions.

---

## Cleanup

```powershell
.\scripts\docker.ps1 down
```

---

## Quick Path (15 min version)

For a shorter demo, cover only:
1. Health check (30s)
2. Multi-source ingestion overview — show the 13 source files (2 min)
3. Run `run-demo.bat` to show automated validation (2 min)
4. Search PAY-101, trace the golden evidence path EPC-101 → code (4 min)
5. Incident root cause INC0080101 (2 min)
6. RAG pattern demo — simple + multi-hop (2 min)
7. LAYA release readiness check (1 min)
8. Admin panel overview (1 min)

---

## Key Entity Reference

### Payment Gateway (Manual Folder — PAY Domain)

| Entity | ID | Description |
|--------|-----|-------------|
| Rally Epic | EPC-101 | Payment Gateway Modernization |
| Rally Epic | EPC-102 | PCI DSS Compliance Hardening |
| Rally Epic | EPC-103 | Settlement Engine Rewrite |
| Jira Feature | PAY-100 | Payment Tokenization |
| Jira Feature | PAY-200 | PCI DSS Compliance |
| Jira Feature | PAY-300 | Settlement Processing |
| Jira Story | PAY-101 | Implement payment tokenization service |
| Jira Story | PAY-201 | Encrypt cardholder data at rest |
| Jira Story | PAY-301 | Settlement batch engine |
| GitLab MR | !301 | Tokenization service implementation |
| ServiceNow | CHG0090101 | Payment Gateway tokenization deployment |
| Incident | INC0080101 | Payment timeout spike — gateway p99 > 2s |
| qTest | TC-PAY-001-008 | Payment Gateway test cases |

### Fraud Detection (Pipeline Folder — FRD Domain)

| Entity | ID | Description |
|--------|-----|-------------|
| Rally Epic | EPC-201 | Fraud Detection Engine Overhaul |
| Rally Epic | EPC-202 | AML Regulatory Compliance |
| Rally Epic | EPC-203 | Transaction Monitoring Platform |
| Jira Feature | FRD-100 | Fraud Scoring Model V2 |
| Jira Feature | FRD-200 | AML/KYC Compliance |
| Jira Feature | FRD-300 | Real-Time Transaction Monitor |
| GitLab MR | !601 | Fraud scoring model v2 |
| ServiceNow | CHG0090401 | Fraud scoring model v2 deployment |
| Incident | INC0080201 | False positive spike in fraud scoring |
| qTest | TC-FRD-001-008 | Fraud Detection test cases |

### People

| Name | Role | Domain |
|------|------|--------|
| Sarah Chen | Lead Architect | Payment Gateway |
| Marcus Johnson | Senior Developer | Payment Gateway |
| Priya Sharma | DevOps Engineer | Both |
| James Wilson | QA Lead | Both |
| David Kim | Security Engineer | PCI DSS |
| Elena Rodriguez | Tech Lead | Fraud Detection |
| Raj Patel | ML Engineer | Fraud Detection |
| Lisa Park | Compliance Analyst | AML |

### Infrastructure

| Component | Details |
|-----------|---------|
| DB Servers | pghost-prod-01/02.mfs.internal |
| Databases | mfs_payments_db, mfs_fraud_db, mfs_audit_db |
| OpenShift | pods: payment-gateway-prod-1/2/3, fraud-engine-prod-1/2 |
| Service Accounts | svc-payment-gateway, svc-fraud-engine, svc-settlement-batch |
| Kafka | topics: payment.transactions, fraud.alerts, settlement.batches |

---

## Honest Boundaries

- The graph and analytics are live behavior over persisted demo data
- Source exports are offline fixtures unless connector credentials are configured
- Model synthesis is optional; all golden paths work without a local model
- LAYA falls back to structured graph summaries when no local LLM is available
- Container hardening, production performance, and G2 roadmap items are not demo claims
- The 13 source system connectors each have their own JSON format validated by the platform
