# CI/CD and Coordinated Suite Releases

## Three Validation Layers

| Layer | Trigger | Required outcome |
|---|---|---|
| Component CI | PR in one repository | Clean checkout, actual lint/type/unit/build/package checks, contract validation and scoped security tests |
| Candidate integration | Linked component PRs or a candidate suite-lock PR | Install candidate artifacts with selected unchanged components; run cross-app and boundary journeys |
| Release qualification | Approved exact suite manifest/profile | Fresh install, upgrade, rollback/recovery, denied cases, evidence integrity and artifact/license inventory |

A component PR can pass while the suite candidate fails. Do not set a product-wide completion status from the union of unrelated green unit jobs. A skipped required profile blocks that profile's release.

## Reusable Workflows

Store reusable workflows in `eoip-suite/.github/workflows/`, using `workflow_call` with narrow typed inputs/secrets. Each caller selects a reviewed immutable commit. Enable access for the intended private caller repositories, and verify it with a nonprivileged consumer. Reuse behavior is governed by GitHub's workflow access and caller/callee permissions. [Reusable workflow documentation](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

The following is an intentionally incomplete **caller template** for `AvyukthiAI`. Resolve the real reviewed 40-character commit before materialization; `REVIEWED_40_HEX_COMMIT` is not a valid release pin. The referenced repository/workflow must first be created and implemented with the specified inputs and outputs, and private caller access must be configured.

```yaml
name: component-ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  packages: read
jobs:
  validate:
    uses: AvyukthiAI/eoip-suite/.github/workflows/web-ci.yml@REVIEWED_40_HEX_COMMIT
    with:
      working-directory: .
      node-version: '22.18.0'
```

The Node value reproduces current CI; select a reviewed supported version before production use. Resolve and pin every external action similarly. `web-ci.yml` must install locked dependencies, run real scripts from guide 09, retain diagnostics on failure and emit artifact digest/contract metadata. It must not hardcode legacy `apps/web` paths.

## Cross-Repository Authentication

The ordinary workflow `GITHUB_TOKEN` is scoped to the workflow repository; it is not organization-wide checkout authority. Use a narrowly installed GitHub App with short-lived installation tokens for explicitly allowed private repository reads/dispatch operations, or another approved least-privilege mechanism. Keep installation credentials in protected secrets, never manifest files. [GitHub token scope](https://docs.github.com/en/actions/concepts/security/github_token).

Package access is configured separately: grant consumer workflows access to needed private packages. Do not give every portal a token that can read Fleet source or publish platform releases. Prefer cloud workload identity for deployment when supported and configured; do not assume any cloud or OIDC trust already exists.

Do not execute untrusted PR code with production secrets. Avoid `pull_request_target` checkout/execution of untrusted head commits. Self-hosted runners used for untrusted tests must not retain production credentials, customer state or reusable privileged mounts. Reused caches require integrity/scoping checks.

## Candidate Suite Manifest

This minimal structure is a **non-releasable example**. The implementation must reject its placeholders; all required components, schemas, migration steps, data compatibility and artifact attestations must be recorded before promotion.

```json
{
  "schemaVersion": 1,
  "suiteVersion": "0.1.0-candidate.1",
  "status": "unverified",
  "profile": "local-pilot",
  "components": [
    {
      "repository": "eoip-query-portal",
      "sourceCommit": "REQUIRED_40_HEX_COMMIT",
      "artifact": "REQUIRED_IMMUTABLE_ARTIFACT_REFERENCE",
      "sha256": "REQUIRED_64_HEX_DIGEST",
      "contractVersion": "REQUIRED_PUBLISHED_CONTRACT_VERSION"
    }
  ],
  "migrations": [],
  "evidenceManifest": null,
  "rollbackManifest": null
}
```

Schema validation must reject unknown component IDs, duplicates, missing required dependencies, inaccessible artifacts, mutable tags, invalid digests, unsupported version combinations, absent notices, undeclared migrations and unqualified profile claims. An empty migration list is valid only after an explicit no-data-change assessment, not by default.

## Build and Promote Sequence

1. Build each component once from a clean source commit and lockfile; publish candidate artifacts with checksums, SBOM and source identity.
2. Generate a candidate suite manifest using exact package/image/static bundle/VSIX versions.
3. Provision disposable graph, authority, job and artifact state for the chosen profile.
4. Deploy candidate artifacts without compiling sibling source during deployment.
5. Execute [verification gates](13-verification-and-evidence.md), including negative controls and lifecycle checks.
6. Retain complete redacted evidence in durable controlled storage, with a manifest in the suite release record.
7. Approve the verified manifest using the actual release-owner policy and promote the **same digests**, not a rebuild.
8. Record deployment, observation and rollback/recovery outcome. Mark unsupported modules/profiles unavailable.

## Version Skew and Failure Handling

Initially release one supported component combination. Add compatibility matrices only after testing actual skew: old client/new API, new client/old compatible API, missing optional service and incompatible contract rejection. Never assume semantic version strings alone prove compatibility.

Frontend rollback selects retained old assets and routing configuration. API/worker rollback requires database/resource compatibility. Use expand/contract migrations and tested forward repair where rollback is unsafe. A restore must preserve authority/revocation/lease semantics and prevent replay of previously consumed approvals.

Coordinate all multi-repository PRs with a change ID and explicit merge order. Publish the additive provider first, then update consumers, then retire old behavior. Use candidate artifacts for preview integration; do not merge incompatible consumers merely because another PR is expected soon.

## Initial CI Implementation Checklist

Implement web, Python library/service, extension and suite-verification workflow types. Verify failure propagation by breaking an assertion, removing a resource, providing a mismatched contract and withholding a required evidence artifact. Check that each blocks the correct gate. Branch policies should require these real check names only after the workflows exist and have been exercised.
