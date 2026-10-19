# Compliance and Distribution Policy

`license-policy.yaml` is a repository policy input, not a legal clearance certificate. First-party ownership/distribution terms are documented in [LICENSE](../LICENSE) and [LICENSING](../LICENSING.md); third-party components retain their own terms and are tracked in [THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md) and [licenses](../licenses/README.md).

Before distributing a wheel, container, frontend bundle, VSIX or model package, inspect its actual resolved contents, dependencies, bundled native libraries, notices and applicable restrictions. Different optional extras and deployment profiles produce different artifacts. Do not infer commercial clearance from an SPDX label or passing installation.

Maintain provenance for dependency versions and preserve notices in the distributed artifact. Run applicable compliance tests, including the current no-CUDA distribution policy when changing dependency locks. Obtain the required owner/legal review for unresolved terms; this README does not reinterpret or replace those terms.

See [release checklist](../docs/release-checklist.md) for evidence and approval boundaries.
