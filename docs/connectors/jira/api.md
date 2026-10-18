# Jira Connector API Research & Qualification Specification

*Researched per CRA-005.1, CRA-005.4, CRA-005.6. Complies with ADR-004 and ONT-005.*

## Official API Specifications & Pinned Versions
- **Jira Cloud**: REST API v3 (`https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/`)
  - Endpoints: `/rest/api/3/search`, `/rest/api/3/project`, `/rest/api/3/issue/{issueIdOrKey}`, `/rest/api/3/mypermissions`
  - Pagination: Enhanced search with `nextPageToken` or `startAt` + `maxResults` (capped at 100).
- **Jira Data Center / Server**: REST API v2 (`https://docs.atlassian.com/software/jira/docs/api/REST/latest/`)
  - Endpoints: `/rest/api/2/search`, `/rest/api/2/project`, `/rest/api/2/issue/{issueIdOrKey}`
  - Pagination: `startAt` + `maxResults` (capped at 100).

## Authentication & Authorized Scopes
- **Cloud Authentication**:
  - API Token via HTTP Basic: `username:api_token` encoded base64.
  - OAuth 2.0 (3LO): Bearer token with scopes `read:jira-work`, `read:jira-user`, `offline_access`.
- **Data Center Authentication**:
  - Personal Access Token (PAT): `Authorization: Bearer <PAT>`.
  - HTTP Basic (service accounts with least privilege).

## Webhooks
- Events: `jira:issue_created`, `jira:issue_updated`, `jira:issue_deleted`, `comment_created`, `comment_updated`, `comment_deleted`.
- Signature verification: HMAC-SHA256 payload verification with shared secret.

## Incremental Sync & Overlap Deduplication
- Incremental JQL: `project in ({projects}) AND updated >= '{watermark}' ORDER BY updated ASC`.
- Overlap window: Default 5 minutes (`overlap_minutes=5`) to prevent missing in-flight mutations.
- Deduplication: Ingested events deduplicated by `(issue_id, updated_timestamp)`.

## Permissions & ACL Propagation
- Issue Security Levels: Mapped to `acl_vector` entries (e.g., `jira:security_level:{id}`).
- Project Permission Schemes: Retrieved via `/rest/api/3/mypermissions` or project permission schemes; mapped to `acl_vector` (e.g., `jira:project:{key}:browse`).

## Raw Evidence Vault
- Attachments: Retrieved via `/rest/api/3/attachment/content/{id}` and preserved in raw vault with sha256 checksum and mime type.
