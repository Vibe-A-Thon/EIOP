# Grafana API Connector Specification

*Researched per CRA-008.4, CRA-008.7. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **Grafana**: HTTP REST API pinned to Grafana 10.x baseline.
  - Endpoints: `/api/search`, `/api/dashboards/uid/{uid}`, `/api/ruler/grafana/api/v1/rules`, `/api/datasources`.
  - Core types: `dashboard`, `alert_rule`, `datasource`.

## Credential Protection & Secret Scrubbing
- Stored data source secrets (`secureJsonData`, `password`, `basicAuthPassword`, tokens, keys) are strictly scrubbed before persistence via `scrub_datasource_secrets()`.
- Credential fields are never exposed as ordinary metadata or stored in graph attributes.

## Service Proposals with Evidence Locators
- Dashboard panel definitions and target queries are parsed for CMDB service and microservice mentions.
- Detected references produce provisional links (`status: PROPOSED`, `relationship: tracksService`) with contextual evidence snippets.
