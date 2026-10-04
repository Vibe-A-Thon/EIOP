# Manual Demo Data — TechNova HealthTech

Scenario: **TechNova Health** is a healthcare SaaS company building a HIPAA-compliant
patient portal. The data covers a patient-data-sync incident, portal UI redesign,
compliance testing, and microservices architecture.

This folder demonstrates **manual, file-based ingestion** where an operator loads
JSON fixtures one at a time through the admin UI or CLI.

## Source Systems

| File | Source System | Connector | Records |
|------|--------------|-----------|---------|
| jira.json | Jira | JiraJsonConnector | 6 issues (HLTH project) |
| gitlab.json | GitLab | GitLabJsonConnector | 3 MRs, 3 pipelines |
| servicenow.json | ServiceNow | ServiceNowConnector | 2 incidents, 2 changes |
| confluence.json | Confluence | ConfluenceConnector | 3 wiki pages |
| figma.json | Figma | FigmaConnector | 1 file, 2 pages, 3 components |
| qtest.json | qTest | qTestConnector | 2 suites, 4 test cases, 2 runs |
| rally.json | Rally | RallyConnector | 1 epic, 2 features, 2 user stories |
| code-graph.json | Code (JSON) | ScenarioPack loader | Code graph as JSON vertices/edges |
| api-portal.json | API Portal | APIPortalConnector | 3 services, 6 endpoints |
| observability.json | Grafana/Datadog/Kibana | Observability connectors | Dashboards, monitors, saved objects |
| crawler-wiki.json | Web Crawler | CrawlerConnector | 3 crawled wiki/portal pages |

## Scenario Summary

TechNova Health is migrating its patient portal from a monolith to microservices.
During a release of the new Patient Records API v2, a data sync failure caused
appointment records to become stale. The incident (INC0050201) triggered an emergency
change (CHG0060301), a HIPAA compliance review, and a redesign of the sync architecture.

### Key Entities
- **People:** Dr. Aisha Rahman (architect), Kai Nakamura (dev), Priya Sharma (QA), Carlos Mendez (SRE)
- **Work:** HLTH-101 through HLTH-106 (patient portal stories/tasks)
- **Incident:** INC0050201 — patient appointment data sync failure
- **Design:** Patient Dashboard Experience (Figma)
- **APIs:** Patient API, Records API, Appointments API
- **Tests:** HIPAA compliance suite, data encryption tests
