# GitLab connector

Status: implemented with fixture/MockTransport integration coverage. Live verification requires an
operator-provided GitLab.com, GitLab Dedicated, or self-managed endpoint and an authorized token;
the implementation does not claim a live enterprise connection without those credentials.

## Supported surface

- Project and recursive group discovery.
- Projects/repositories, branches, tags, commits, merge requests and changed-file metadata.
- Issues/work items, pipelines, jobs, artifact metadata, deployments and releases.
- Project wiki content, README content, Pages configuration/domains, and optional allowlisted crawl
  of the published GitLab Pages site.
- Baseline, checkpoint polling, signed webhooks, replay, reconciliation, immutable capture,
  provenance evidence, and temporal graph revisions.
- Deterministic links across Jira keys, merge requests, commits, changed files, pipelines, jobs,
  artifacts, and deployments. When the code parser uses the same registry repository ID
  (`gitlab:{source_id}:{path_with_namespace}`), its File and CodeSymbol facts join this chain.

The API root must include `/api/v4`, for example `https://gitlab.example/api/v4`. EOIP uses bearer
authentication and read-only calls. Project paths and record identifiers are URL encoded.

## Registry example

```json
{
  "schema_version": "1.0",
  "source_id": "gitlab-prod",
  "source_type": "gitlab",
  "name": "Production GitLab",
  "base_url": "https://gitlab.example/api/v4",
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
    "projects": ["example/platform"],
    "groups": [],
    "include_wikis": true,
    "include_pages": true,
    "include_readme": true,
    "include_merge_request_diffs": true,
    "page_size": 100,
    "max_pages": 1000,
    "max_document_bytes": 2000000,
    "pages_scopes": {
      "example/platform": {
        "start_urls": ["https://example.gitlab.io/platform/"],
        "allowed_hosts": ["example.gitlab.io"],
        "include_paths": ["/platform/"],
        "exclude_paths": [],
        "max_depth": 2,
        "page_limit": 100,
        "mime_types": ["text/html"],
        "max_page_bytes": 2000000
      }
    }
  },
  "secret_refs": {
    "token": "env://EOIP_GITLAB_TOKEN",
    "webhook_signing": "env://EOIP_GITLAB_WEBHOOK_SIGNING"
  }
}
```

## Webhooks

Send GitLab webhooks to `/api/v1/sources/{source_id}/webhooks`. For current GitLab versions, EOIP
validates the Standard Webhooks `webhook-signature` over `webhook-id.webhook-timestamp.body`,
rejects timestamps outside the five-minute replay window, deduplicates the delivery ID, persists
the receipt, and then queues processing. Store the `whsec_...` signing token under the
`webhook_signing` secret reference.

Older GitLab installations can use `X-Gitlab-Token` with a `webhook_hmac` secret reference. This
mode authenticates the sender but, because GitLab sends the legacy token as plain text, does not
independently authenticate the body; signed webhooks are preferred.

Mapped webhook kinds include push, tag push/delete, merge request, issue, pipeline, job/build,
deployment, release, and wiki page events.

## Safety and operational limits

- API and Pages start URLs must use explicitly configured HTTPS/HTTP scopes; API URLs require
  HTTPS and reject embedded credentials.
- API pagination is bounded and follows GitLab's server-provided next link/header. A bounded
  fallback handles GitLab.com responses where pagination headers are omitted.
- Published Pages crawling uses the shared hostname allowlist, DNS/IP SSRF checks, redirect checks,
  depth/page/body limits, and a separate client that never receives the GitLab API token.
- README content is bounded before capture. Artifacts are metadata-only; binaries are not
  downloaded.
- API errors expose stable categories, not response bodies or credentials.

Official references:

- https://docs.gitlab.com/api/rest/
- https://docs.gitlab.com/api/api_resources/
- https://docs.gitlab.com/user/project/integrations/webhooks/
- https://docs.gitlab.com/user/project/integrations/webhook_events/
- https://docs.gitlab.com/api/jobs/
- https://docs.gitlab.com/api/deployments/
- https://docs.gitlab.com/api/pages_domains/
- https://docs.gitlab.com/user/project/pages/
