# Catalog Federation & Precedence Specification

*Researched per CRA-009.4, CRA-009.5, CRA-009.7. Complies with ADR-004, ONT-007.*

## Supported External Catalog Platforms
- **OpenMetadata**: REST API (`/api/v1/tables`, `/api/v1/glossaryTerms`)
- **DataHub**: GraphQL & OpenAPI (`/entities?action=search`)
- **Apache Atlas**: REST API (`/api/atlas/v2/entity`)

## Precedence Resolution (CRA-009.4)
- Rather than duplicating external schemas blindly, external catalog assets are unified using deterministic precedence ranking:
  1. `eoip_ontology` (Authoritative core ontology)
  2. `datahub`
  3. `openmetadata`
  4. `apache_atlas`
- When multiple catalogs report the same asset (e.g. data table or column), core attributes (owner, description, classification) are resolved based on the highest-priority catalog, while sparse tags and technical properties are merged with full source provenance preserved.

## Generic Protocol Adapters (CRA-009.7)
- Supports certified generic protocol endpoints:
  - `REST/OpenAPI`
  - `GraphQL`
  - `SOAP 1.2`
  - `JDBC/ODBC`
  - `Files/SFTP/ObjectStorage`
  - `Events (Kafka/RabbitMQ)`
- Conformance certification runner tests connectivity, schema mapping fidelity, and CRA-004 error contracts.
