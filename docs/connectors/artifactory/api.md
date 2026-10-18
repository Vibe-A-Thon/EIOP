# JFrog Artifactory Connector API Research & Qualification Specification

*Researched per CRA-007.3, CRA-007.8. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **JFrog Artifactory REST API & Artifactory Query Language (AQL)**:
  - Base paths: `/api/repositories`, `/api/search/aql`, `/api/build/{buildName}/{buildNumber}`
  - Storage Webhooks: `artifact:deployed`, `artifact:promoted`, `artifact:deleted`

## Artifact Identity & VCS Provenance
- **Checksum Rooting**: Artifact identity is strictly determined by cryptographic SHA-256 checksums (`sha256`), never reduced to file path or repo URL alone.
- **Build VCS Linkage**: BuildInfo parses `vcs.revision` to establish `art:builtFromCommit` links to source git commits.

## Security & Credential Hygiene
- Build metadata and environment variables are strictly scrubbed to prevent credential or secret leakage into the graph or knowledge logs.
- Repository permissions map into `PermissionMetadata.principal_refs` as `artifactory:repo:{repo_key}`.
