# Confluence Connector API Research & Qualification Specification

*Researched per CRA-006.1, CRA-006.5, CRA-006.6. Complies with ADR-004, ONT-006.*

## Official API Specifications & Pinned Versions
- **Confluence Data Center & Cloud REST API v1/v2**:
  - Base paths: `/rest/api/space`, `/rest/api/content/search`, `/rest/api/content/{id}`, `/rest/api/content/{id}/restriction/byOperation`
  - Content Types: `Space`, `Page`, `BlogPost`, `Comment`, `Attachment`, `Version`
  - Search Syntax: Confluence Query Language (CQL), e.g. `space = "DEV" AND type = page AND lastModified >= "2026-10-01 00:00"`

## Authentication & Authorization
- **Data Center**: Personal Access Token (PAT) via Bearer token, or HTTP Basic service accounts.
- **Cloud**: API Token or OAuth 2.0 with scopes `read:confluence-space.summary`, `read:confluence-content.all`, `read:confluence-props`.

## Page Tree & Relationships
- Hierarchical page navigation via `ancestors` array and `wiki:childOf` predicate.
- Intra-wiki links (`ac:link`) and mentions (`ri:user`) resolved deterministically.

## Permissions & ACL Vectors
- Space permissions: default access envelope `confluence:space:{key}`.
- Page restrictions: Granular view/edit restrictions extracted from `/rest/api/content/{id}/restriction/byOperation`.
  - Read restrictions populate `PermissionMetadata.principal_refs` with `confluence:user:{key}` and `confluence:group:{name}`.
  - Non-restricted pages inherit space-level ACLs.
- Independent permission sync: ACL changes emit `PERMISSION_UPDATE` events without touching page content.

## Macro Fidelity & Diagnostics
- Storage format parsed deterministically without dynamic script execution.
- Macros evaluated against supported capabilities; unsupported macros (e.g. unknown third-party plugins) are honestly reported in `diagnostics["unsupported_macros"]` without fabricating false plain-text interpretations.
