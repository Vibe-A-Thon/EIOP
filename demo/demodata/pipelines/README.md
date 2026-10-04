# Pipeline Demo Data — Northstar Commerce

Scenario: **Northstar Retail Group** operates an e-commerce platform with checkout,
risk decisioning, and payment services. The data covers a production latency incident
after a risk service release, pipeline-driven CI/CD, and multi-service observability.

This folder demonstrates **automated pipeline ingestion** where a pipeline configuration
orchestrates multi-source data loading with validation gates between stages.

## Source Systems

| File | Source System | Connector | Records |
|------|--------------|-----------|---------|
| jira.json | Jira | JiraJsonConnector | 5 issues (SHOP project) |
| gitlab.json | GitLab | GitLabJsonConnector | 4 MRs, 4 pipelines |
| servicenow.json | ServiceNow | ServiceNowConnector | 2 incidents, 2 changes |
| confluence.json | Confluence | ConfluenceConnector | 3 wiki pages |
| figma.json | Figma | FigmaConnector | 1 file, 2 pages, 4 components |
| qtest.json | qTest | qTestConnector | 2 suites, 4 test cases, 2 runs |
| rally.json | Rally | RallyConnector | 1 epic, 2 features, 3 user stories |
| code-graph.json | Code (JSON) | ScenarioPack loader | Checkout service code graph |
| api-portal.json | API Portal | APIPortalConnector | 4 services, 8 endpoints |
| observability.json | Grafana/Datadog/Kibana | Observability connectors | Production dashboards/monitors |
| crawler-portal.json | Web Crawler | CrawlerConnector | 3 crawled developer portal pages |
| pipeline-config.json | Pipeline | PipelineOrchestrator | 8-stage ingestion pipeline |

## Scenario Summary

Northstar released checkout risk decisioning v2 (SHOP-301), which introduced a latency
spike (INC0071042) due to unbounded retry fan-out to the Risk Decision API. The incident
required an emergency change (CHG0081088) deploying a bounded fallback. The demo shows
the full digital thread from Rally portfolio planning through code, CI/CD, deployment,
observability, and incident resolution.

### Key Entities
- **People:** Maya Chen (dev), Liam Patel (SRE), Jordan Blake (PM), Sam Torres (QA)
- **Work:** SHOP-301 through SHOP-305 (checkout modernization stories/tasks)
- **Incident:** INC0071042 — checkout latency spike after risk release
- **Design:** Checkout Experience v2 (Figma)
- **APIs:** Checkout API, Risk Decision API, Payment Auth API, Inventory API
- **Tests:** Checkout regression, contract tests, resilience tests
