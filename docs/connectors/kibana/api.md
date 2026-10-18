# Kibana Saved Objects Connector Specification

*Researched per CRA-008.3, CRA-008.7. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **Kibana / OpenSearch Dashboards**: Saved Objects API pinned to Elastic 8.x / OpenSearch 2.x baseline.
  - Endpoints: `/api/saved_objects/_find` or `/s/{space_id}/api/saved_objects/_find`.
  - Core types: `dashboard`, `search`, `index-pattern`.

## Spaces vs Index Authority Separation
- **Space Scoping**: Permissions are explicitly scoped to Kibana spaces (e.g. `kibana:space:{space_id}`).
- **Strict Index Separation**: Authenticating to a dashboard or viewing saved object metadata does NOT grant authority to query or read underlying Elasticsearch/OpenSearch indices. Every ingested event marks `index_authority_separated: True` and `backing_indices_authorized: False`.

## CMDB Service Proposals
- Dashboard search sources and panel definitions are scanned for microservices and CMDB service references.
- These references are emitted as provisional links (`status: PROPOSED`, `relationship: visualizesEntity`) supported by character-span evidence locators.
