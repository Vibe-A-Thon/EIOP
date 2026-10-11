# Northstar enterprise demo pack

This directory is the executable, synthetic sales-demo corpus loaded by the normal EOIP `DEMO` worker job. It contains no real customer data or credentials.

## How this maps to implemented EOIP features

The pack drives the current enterprise demo surfaces: authenticated scenario
readiness APIs, graph explorer lenses, Hubble visualization, GraphRAG evidence
flows, impact/lineage/neighborhood/traceability calls, governance views,
decision/process/business capability entities, code/CI/test/design/ops
relationships, and persisted knowledge products. Loading is validated against
the runtime ontology and graph mutation boundary, captures the source pack
before writing, and remains idempotent.

## What is included

- `scenario-pack.json` version 1.1.0 is the canonical graph seed: 11 stories, 70 entities, and 114 relationships across BUSINESS, DECISION, PROCESS, WORK, CODE, CICD, TEST, DESIGN, OPS, KNOWLEDGE, IDENTITY, and META.
- `source-fixtures/` contains representative Jira, GitLab, Confluence, ServiceNow, observability, qTest, Figma, and API-portal exports for connector demonstrations.
- `project-code/` provides a small risk-aware checkout implementation and tests.
- `api/checkout-openapi.json` provides the API contract linked from the graph.
- `wiki/` provides the architecture page and operational runbook represented by knowledge entities.

The loader validates `scenario-pack.json` against `schemas/demo_scenario_pack.schema.json`, then validates every graph label, property, endpoint, and scenario reference against the runtime ontology. It captures the source pack before writing, uses the canonical normalized mutation boundary, adds ingestion and domain links, and is idempotent.

The enrichment adds conversion/latency objectives, business capabilities,
accepted/rejected alternatives, a superseded decision, an outcome, ordered
incident-response steps and an approval-delay exception. All KPIs, timings and
outcomes are explicitly synthetic. Test-case creation now precedes its execution.
Business captions are persisted as `display_name`; canonical and physical IDs
are unchanged. The original seed's 92 relationship fact keys remain compatible
with 1.0.0, so enrichment does not duplicate those facts. New facts have explicit
stable keys. Ingestion runs and changed source-document versions are retained
as provenance, not overwritten or deleted.

## Guided Hubble demonstration

Run `scripts\docker.ps1 demo-data`, then open
**http://localhost:8088/enterprise.html**, or double-click
`demo\autodemo\run-demo-hubble.bat` for the automatic 11-scenario walkthrough.
The guided page is served by Hubble and queries its existing graph connection.
Its catalog selects query anchors; all rendered nodes and edges come from live
Gremlin responses. Missing data and query failures are displayed explicitly.

Choose a business question or search a named seed entity. Colors distinguish
domains, arrows preserve edge direction, and labels show logical relationship
names. Select nodes/edges for source facts and IDs; enable provenance nodes,
drag nodes, zoom/fit, inspect the relationship table, or export the returned
JSON. Generated read-only Gremlin can be copied into native Hubble.
One-hop results are bounded to 120 relationships, not a full graph export.
Entity selection covers the typed seed, not every ingested source document.

These scenarios cover connected strategy/delivery/runtime, decision lineage,
process deviation, incident/release traceability, API dependency visibility,
test evidence, design and knowledge. They do not establish production-scale
performance, semantic embedding quality, every normalized vendor connector,
automated process mining or complete packaged VSIX/NLQ acceptance. Those
capabilities must be demonstrated and verified separately; loaded fixtures are
not execution evidence.

## Quick verification

```powershell
python -X utf8 -m pytest -q tests/e2e/test_enterprise_demo_scenarios.py
```

With the Docker application running, inspect live readiness:

```powershell
$headers = @{ Authorization = "Bearer $env:EOIP_API_TOKEN" }
Invoke-RestMethod http://localhost:8000/api/v1/demo/scenarios -Headers $headers
```

Every scenario reports `ready: true` only when each expected graph entity is actually present.
