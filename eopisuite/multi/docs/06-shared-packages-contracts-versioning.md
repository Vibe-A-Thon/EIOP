# Shared Packages, Contracts and Versioning

## Share Artifacts, Not Sibling Source Trees

Each repository must build in a clean checkout with only its declared dependencies and approved artifact access. Imports such as `../../eoip-ui/src`, a production `PYTHONPATH` pointing into the legacy checkout, and container `COPY ../other-repo` are forbidden target dependencies. Local editable development can be explicit and temporary; release verification uses built artifacts.

| Producer | Proposed distributed output | Consumers |
|---|---|---|
| `eoip-platform` | Existing Python distribution `eoip`, import `eoip.*` | API, worker and narrowly justified internal clients |
| `eoip-ui` | `@avyukthiai/eoip-ui`, `@avyukthiai/eoip-shell` | All first-party portals |
| `eoip-contracts` | Versioned schema/OpenAPI bundle and `@avyukthiai/eoip-app-contracts` | SDK generator, app catalog, gateways and verification |
| `eoip-sdk` | `@avyukthiai/eoip-sdk`, Python distribution `eoip-sdk` with import `eoip_sdk` | Portals, SDK users, CLI, MCP/extension where appropriate |
| `eoip-reva` | Python distribution/import boundary decided and tested as `eoip-reva` / `reva` | Explicitly enabled API/worker integrations and verification clients |

`avyukthiai` is the lowercase package/container namespace for the user-confirmed GitHub organization `AvyukthiAI`, not a change to the legal licensor's name. Container references use `ghcr.io/avyukthiai/<image>`. These names do not establish existing package publication or access. Preserve existing proprietary metadata and validate registry permissions before first publication. Client code should not depend on the whole backend platform just to obtain request types.

## Registry Strategy

Use GitHub's npm registry for private JavaScript packages and GHCR for OCI images after permissions are configured. GitHub's documented registry formats do not include a native PyPI registry. Do not configure pip against a guessed `pypi.pkg.github.com` endpoint. [Supported GitHub package formats](https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages).

For Python bootstrap releases, attach wheels, source distributions and checksums to private GitHub Releases, download with authenticated GitHub tooling, verify the expected digest, then install locally. A managed/private PyPI-compatible registry can replace this later through an ADR; its selection, cost and authentication are not silently assumed here. Customer-installed/offline bundles include an approved complete wheelhouse, not runtime access to a developer's GitHub token.

For npm, store only registry routing and environment-variable interpolation in `.npmrc`:

```ini
@avyukthiai:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
```

The organization scope is now resolved; package publication and consumer permissions still need setup. Load `NODE_AUTH_TOKEN` privately. Local GitHub Packages access currently uses an appropriately scoped classic PAT; Actions can use `GITHUB_TOKEN` when the consuming repository is granted package access. Do not assume an arbitrary fine-grained GitHub token is interchangeable. [GitHub npm authentication and package access](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry).

## Python Packaging Gate

1. Inventory imports, console scripts, resource paths and runtime dependencies of each extracted process.
2. Keep `eoip` as one platform distribution initially; declare optional extras with tested profiles.
3. Classify `config`, `schemas`, migrations, templates and demo data by owner. Immutable defaults needed at runtime become package resources or separately versioned resource bundles. Site-specific settings remain deployment inputs.
4. Replace implicit working-directory assumptions with explicit configuration paths or packaged-resource APIs. `EOIP_CONFIG_DIR` currently is not a universal override; qualify every affected loader.
5. Build the wheel and source distribution with an explicitly pinned build toolchain; inspect contents and applicable notices.
6. Install into a fresh virtual environment from artifacts. Run from outside the source tree with no legacy path on `sys.path`.
7. Exercise query, schema loading, worker dispatch and error paths using the intended entry point. Record missing optional capabilities rather than silently importing a developer-installed dependency.

For a complete, hash-locked offline dependency set, the target installer can use:

```powershell
python -m pip install --no-index --find-links .cache/wheelhouse --require-hashes -r requirements-runtime.lock
```

This requires a newly generated compatible `requirements-runtime.lock` and complete wheelhouse for the specific OS/Python/profile. It is not a claim the current `requirements.lock` already satisfies this contract. Include every transitive requirement and approved hash. Do not add a public extra index for internal package names and assume it prevents dependency confusion.

## Local Shared-Library Development

Normal consumers install published exact versions. To test a platform change locally, install the candidate wheel in the consuming app's own virtual environment. An explicit editable install is permitted for debugging, but record it as a non-release profile and do not let it satisfy clean-install acceptance.

For UI changes, build and `npm pack` the selected package, install the candidate tarball in a disposable consumer branch, and run component/build/browser checks. Before release replace the local tarball reference with the published version and regenerate/review the lockfile. Reject `file:`, `link:` and sibling path entries in release dependencies. React and React DOM must remain compatible peer dependencies for shared components so local packaging does not introduce duplicate React runtimes.

## Contract Authority and Compatibility

Backend request/response models remain owned by their implementation domain. `eoip-contracts` holds reviewed released snapshots generated from a defined runtime profile plus manually owned event/app-manifest schemas where those are authoritative. Every snapshot records source commit, generator version, enabled capabilities and digest. CI checks drift; it must not regenerate a breaking contract and silently approve it.

Preserve `/api/v1`, required Wisdom deep links and `/api/reva/v1` semantics during extraction. Repository naming is not a reason to rename HTTP paths, record IDs, event names or extension command IDs. Preserve canonical cross-programme events rather than adding a parallel suite event bus.

Contract changes must specify field/nullability/default changes, stable error codes, pagination, bounds, authorization, idempotency, cancellation, concurrency preconditions, deprecation and upgrade behavior. A schema-compatible change can still be behaviorally breaking; authorization and side-effect tests remain mandatory.

## Release Policy

- Use semantic versions for component public contracts, with an explicit pre-1.0 compatibility policy.
- Start with **exact** shared-package versions in application manifests and committed lockfiles.
- A suite release pins source commits, artifact digests, contract versions, data migrations and deployment profile.
- Never consume `latest` or a moving Git branch in a release lock.
- Cross-repository changes follow expand -> publish -> update consumers -> verify -> retire, not simultaneous incompatible merges.
- Support only combinations actually tested. Current/previous client skew is a later qualification target, not an automatic promise.
- SDK generation must be deterministic and reviewed; do not overwrite handwritten transport/auth logic on regeneration.

Proof of this boundary: two separate clones, no sibling mounts, no shared node_modules/venv, real artifact installs and successful authenticated API workflows. A package build alone does not demonstrate the application is independent.
