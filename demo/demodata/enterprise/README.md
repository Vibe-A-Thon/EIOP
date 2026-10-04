# Northstar enterprise demo pack

This directory is the executable, synthetic sales-demo corpus loaded by the normal EOIP `DEMO` worker job. It contains no real customer data or credentials.

## What is included

- `scenario-pack.json` is the canonical graph seed: 8 stories, 56 entities, and 92 relationships across WORK, CODE, CICD, TEST, DESIGN, OPS, KNOWLEDGE, IDENTITY, and META.
- `source-fixtures/` contains representative Jira, GitLab, Confluence, ServiceNow, observability, qTest, Figma, and API-portal exports for connector demonstrations.
- `project-code/` provides a small risk-aware checkout implementation and tests.
- `api/checkout-openapi.json` provides the API contract linked from the graph.
- `wiki/` provides the architecture page and operational runbook represented by knowledge entities.

The loader validates `scenario-pack.json` against `schemas/demo_scenario_pack.schema.json`, then validates every graph label, property, endpoint, and scenario reference against the runtime ontology. It captures the source pack before writing, uses the canonical normalized mutation boundary, adds ingestion and domain links, and is idempotent.

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
