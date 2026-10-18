# GitHub & GitLab Connector API Research & Qualification Specification

*Researched per CRA-007.1, CRA-007.2, CRA-007.6. Complies with ADR-004, ONT-007.*

## Official API Specifications & Pinned Versions
- **GitHub**: REST API (`https://api.github.com`) pinned to API version `2022-11-28`, plus GraphQL API v4.
  - Core resources: `/repos/{owner}/{repo}`, `/commits`, `/branches`, `/pulls`, `/issues`, `/releases`, `/actions/runs`
  - Webhooks: Signed with HMAC-SHA256 (`X-Hub-Signature-256`) and delivery UUID replay protection.
- **GitLab**: REST API v4 (`https://gitlab.com/api/v4`), plus GraphQL.
  - Core resources: `/projects`, `/repository/commits`, `/repository/branches`, `/merge_requests`, `/issues`, `/pipelines`

## Commit References vs Moving Branches
- **Commit Invariance**: Commits are identified by immutable cryptographic commit hashes (`sha`) with provenance metadata (`immutable: true`).
- **Branch Observations**: Branches are observed states pointing to moving commit heads (`moving_ref: true`).

## Repository Visibility & ACL Vectors
- Public repositories: `PUBLIC` visibility with `role:everyone`.
- Internal repositories: `INTERNAL` visibility with organizational ACL (e.g. `github:org:{org}`).
- Private repositories: `RESTRICTED` visibility with repository-specific ACL (`github:repo:{repo}`).

## Cross-System Issue References
- Commit messages and PR titles are scanned for issue keys using configurable regex `\b[A-Z][A-Z0-9_]+-\d+\b`.
- Cross-references are asserted when resolved against ingested issues; otherwise tracked as proposals.
