# Security, Configuration, Data and Licensing

## Trust Plan

| Boundary | Required control |
|---|---|
| GitHub organization | Least-privilege source/package/release access; reviewed automation and credential recovery |
| Customer browser | Reviewed session integration; no deployment-wide secret embedded in JavaScript |
| API | Authenticated principal, trusted tenant/workspace grants, domain authorization and bounded input |
| Worker | Scoped service authority, validated job payload, durable ownership/recovery appropriate to profile |
| MCP/SDK/CLI/extension | Resource-appropriate identity, limits and revocation; no caller-supplied privilege upgrade |
| Database/Fleet operator surfaces | Separate deployed origins/credentials/network policy and audited elevated actions |
| Evidence/artifacts | Tenant-aware access, retention, integrity and controlled download; redact secrets and customer content |

Same-origin paths are a shared browser trust zone. A compromised first-party portal can affect that origin; a different Git repository does not isolate it. Untrusted extensions must not execute in the customer session origin. Shared GitHub ownership also does not grant customer tenant access.

## Session Boundary Must Be Built

The current API token path is a bootstrap compatibility mode. The suite target requires a reviewed identity-provider integration and a server-side session boundary. Provider selection remains a recorded deployment decision because hosted SaaS and disconnected customer installations have different operational constraints.

The implementation must specify login/callback validation, issuer/audience, redirect allowlist, CSRF/origin protection, Secure/HttpOnly cookie scope under deployed HTTPS, logout, expiry, revocation, service credentials, refresh behavior and tenant switching. The backend validates context grants; an app manifest, tenant header or hidden menu is not authorization. Fail closed when identity lookup fails. Do not synthesize an administrator UI principal.

Local HTTP exceptions are restricted to loopback and documented development profiles. They do not weaken production cookie/session policy. No shared parent-domain cookie across customer and operator origins.

## Configuration Ownership

Separate these inputs explicitly:

| Class | Owner | Distribution |
|---|---|---|
| Immutable application defaults/resources | Component/domain repository | Versioned package/image or resource bundle |
| Deployment topology and public endpoints | `eoip-suite` profile | Reviewed configuration with exact compatible artifacts |
| Tenant settings and revisions | Owning domain service | Authenticated API, versioned persistence, audit and rollback |
| Secrets and signing keys | Approved operator/secret system | Private provisioning, access controls and rotation; never Git/browser assets |
| Developer-specific overrides | Developer local profile | Ignored files/environment, no production credentials |

Each loader must document precedence, validation, restart/reload semantics and masking. Do not claim `EOIP_CONFIG_DIR` controls every current loader. Preserve existing meaningful environment variable names until a documented compatibility migration. Do not blindly concatenate local `.env` files from multiple repositories.

## Data and Schema Ownership

The knowledge core owns graph writes and provenance; ontology owns semantic publication; identity owns grants; authority services own approvals, leases and receipts; acquisition owns jobs/checkpoints; reporting owns derived artifacts; REVA owns its warranted/evidence records subject to qualified integration. Portals have no direct database credentials and no independent copies of authoritative approval state.

Repository extraction is not a data migration. Keep database endpoints and state ownership unchanged during the first UI split. Before changing persistence, inventory schemas, migration versions, retention, backup coverage, pending jobs and effect/replay risks. Test restore to an isolated target, not the only original database. Sharing a network filesystem does not prove multi-host queue correctness.

Use the existing ASPEII single-host versus multi-worker authority decisions and their required evidence. Do not introduce a competing suite authority database just to make each application look independent. Do not claim atomic transactions across SQL and an external graph without the required outbox/recovery/reconciliation protocol.

## Deployment and Distribution Profiles

| Profile | Required qualification |
|---|---|
| Local development | Disposable data, explicit bootstrap auth, selected apps, no SaaS assurance claim |
| Customer-installed standard | Supported bundle, fresh install, upgrade, restore and operator procedures |
| Customer-installed offline | Complete packages/images/assets/docs/notices; no undeclared auth, font, model or licensing network dependency |
| Hosted SaaS | Trusted session, tenancy, durable worker/authority semantics, operator isolation and recovery |
| Dedicated/isolated enterprise | Explicit agreed isolation/residency/support scope, then tested topology |

GitHub is the development/distribution source, not a mandatory runtime dependency for installed customers. Offline support is per connector/model/module; unavailable integrations must be explicit.

## Existing License Boundaries

Apply the repository's existing [licensing policy](../../../LICENSING.md), [first-party license](../../../LICENSE) and [third-party notices](../../../THIRD_PARTY_NOTICES.md) to extracted artifacts. This handbook does not create new commercial terms or decide legal ownership. Preserve the existing approved owner wording; do not substitute the GitHub organization handle for the licensor.

Every published wheel, npm package, static app, VSIX, image and offline bundle needs an artifact-specific dependency/license inventory, applicable notices and source/provenance records. Rebuilding an image can change bundled dependencies even if application source is unchanged. Public SDK/extension distribution needs an explicit visibility/license decision; it is not automatically permitted because it is a separate repository.

Any proposed change to license grants, customer agreements or third-party redistribution obligations requires the existing legal/compliance review process. Repository privacy and npm `UNLICENSED` metadata alone do not constitute a customer commercial agreement.

## Security Exit Conditions

Run direct API denied cases, not only hidden-button tests. Verify two tenants, different roles, expired/revoked sessions, cross-app navigation, export download after revocation, scope-aware caches, unavailable identity service, operator access refusal and secret absence from browser artifacts/logs. An identity or evidence failure must not become synthetic success.
