# GitHub connector

Status: implemented with fixture/MockTransport integration coverage. A live connection is only
considered verified after an operator supplies an authorized GitHub or GitHub Enterprise endpoint
and the health/baseline/reconciliation jobs succeed.

## Supported surface

- GitHub.com REST API and GitHub Enterprise Server REST base URLs.
- Repository and organization discovery.
- Repositories, ownership, branches, tags, commits, pull requests, issues, releases, Actions runs,
  Pages configuration and README content.
- Baseline, checkpoint polling, HMAC webhooks, replay and reconciliation.
- Temporal graph revisions, provenance evidence and deterministic Jira-key links.

The connector sends `Accept: application/vnd.github+json` and a configurable
`X-GitHub-Api-Version` (default `2022-11-28`). Configure a different supported version for the
target installation when required. Password authentication is not supported.

## Minimum access

Use a fine-grained token or GitHub App installation token restricted to the configured
repositories. Metadata read access is required. Add read access for Contents, Pull requests,
Issues, Actions, Releases and Pages only for enabled scopes. EOIP never requests write access.

## Registry example

```json
{
  "schema_version": "1.0",
  "source_id": "github-prod",
  "source_type": "github",
  "name": "Production GitHub",
  "base_url": "https://api.github.com",
  "enabled": true,
  "capabilities": {
    "baseline": true,
    "polling": true,
    "webhooks": true,
    "deletion_events": true,
    "permission_events": false,
    "discovery": true,
    "reconciliation": true,
    "replay": true
  },
  "config": {
    "repositories": ["example/platform"],
    "organizations": [],
    "include_pages": true,
    "include_readme": true,
    "page_size": 100,
    "max_pages": 1000,
    "max_document_bytes": 2000000,
    "api_version": "2022-11-28"
  },
  "secret_refs": {
    "token": "env://EOIP_GITHUB_TOKEN",
    "webhook_hmac": "env://EOIP_GITHUB_WEBHOOK_SECRET"
  }
}
```

For GitHub Enterprise Server, use its REST root, normally
`https://github.example.com/api/v3`.

## Webhooks

Send GitHub webhooks to `/api/v1/sources/{source_id}/webhooks`. The gateway validates
`X-Hub-Signature-256`, deduplicates `X-GitHub-Delivery`, persists the receipt before queueing and
uses `X-GitHub-Event` for deterministic mapping. Supported events are repository, push,
pull_request, issues, workflow_run, release, create and delete.

## Safety limits

- HTTPS endpoints only; embedded URL credentials are rejected.
- Pagination and document sizes are capped.
- README base64 is decoded locally and bounded before capture.
- Tokens remain environment references and are never serialized into jobs or events.
- API errors use stable categories without response bodies or credentials.

Official references:

- https://docs.github.com/en/rest/repos
- https://docs.github.com/en/rest/repos/contents
- https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps
