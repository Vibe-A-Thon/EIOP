# Rally (Broadcom Agile Central) API Research & Qualification Specification

*Researched per CRA-005.2, CRA-005.4, CRA-005.7. Complies with ADR-004 and ONT-005.*

## Official API Specifications & Pinned Versions
- **Rally WSAPI**: Version 2.0 (`https://techdocs.broadcom.com/us/en/ca-enterprise-software/agile-development-and-management/rally-platform-ca-agile-central/wsapi.html`)
  - Base Endpoint: `/slm/webservice/v2.0`
  - Core Object Endpoints:
    - `/slm/webservice/v2.0/HierarchicalRequirement` (User Story)
    - `/slm/webservice/v2.0/PortfolioItem/Feature` (Feature)
    - `/slm/webservice/v2.0/PortfolioItem/Epic` (Epic)
    - `/slm/webservice/v2.0/Defect` (Defect)
    - `/slm/webservice/v2.0/Task` (Task)
    - `/slm/webservice/v2.0/Iteration` (Sprint/Iteration)
    - `/slm/webservice/v2.0/Release` (Release)
    - `/slm/webservice/v2.0/Milestone` (Milestone)

## Authentication & Authorization
- **API Key**: Passed via header `zsessionid: <api_key>` or `Authorization: Bearer <api_key>`.
- **Scoping**: Mandatory `workspace` and `project` scoping query parameters (`/workspace/{id}`, `/project/{id}`) to isolate enterprise tenants.
- **Hierarchy Propagation**: Parent-child epic-feature-story relationships preserved via `Parent` and `PortfolioItem` references.

## Pagination & Incremental Cursor Semantics
- 1-based start index (`start=1`, `pagesize=200`, capped at 2000).
- Incremental filtering: `(LastUpdateDate >= "{watermark}") AND (LastUpdateDate <= "{now}") ORDER BY LastUpdateDate ASC`.
- Rate Limiting: 429 response handling with exponential backoff and jitter.
