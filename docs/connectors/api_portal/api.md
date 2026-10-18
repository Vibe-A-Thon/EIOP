# API Portal Connector Research & Qualification Specification

*Researched per CRA-007.4, CRA-007.9. Complies with ADR-004, ONT-007, Decision H-07.*

## Candidate Profiles & Pinned Qualification State
- **Current State**: UNQUALIFIED (pending vendor product identification under Decision H-07).
- **Candidate Profiles**:
  - `kong`: Kong Gateway Admin & Portal APIs.
  - `apigee`: Google Cloud Apigee Management APIs.
  - `swaggerhub`: SmartBear SwaggerHub Registry API.
  - `openapi3_crawler`: Generic OpenAPI 3.0 / 3.1 specification crawler.

## Proposed Semantic Vocabulary
- `api:Service`: Core business API service catalog item.
- `api:Endpoint`: Addressable URI template exposing API operations.
- `api:Operation`: HTTP method and execution semantics (`GET`, `POST`, `PUT`, `DELETE`).
- `api:SchemaModel`: Governed request and response data contracts.

## Content Safety & Binary Rejection
- All executable binaries, shell scripts, and DOS/ELF headers are strictly rejected to prevent untrusted execution.
