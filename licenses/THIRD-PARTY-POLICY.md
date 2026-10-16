# Third-Party Licensing and Distribution Policy

Status: release preparation policy, 2026-10-14. Scope: all EOIP delivery modes. This policy grants no license in third-party material and is not a legal compatibility opinion.

## Independent License Layers

Keep owned EOIP material under the proprietary notice and executed customer terms. Preserve separately applicable upstream terms for all third-party material. The customer agreement must expressly carve out upstream rights; never state that every byte in a container or browser bundle is exclusively owned by EOIP's rights holders.

If a combined distribution is incompatible with the intended proprietary terms, extra paperwork does not cure it. Resolve the combination, permissions or distribution plan before release.

## Inventory Procedure

1. Identify the exact release artifact, source revision, platform, installed extras, build options, base-image digests, model/asset versions and delivery mode.
2. Enumerate actual installed and bundled components, not only top-level manifest entries. Include transitive dependencies, vendored code, generated code containing upstream material, fonts, data, native libraries and external tools.
3. Distinguish build-only tools from shipped material, but inspect generated/bundled outputs before concluding a tool has no distribution implications.
4. Obtain original license and NOTICE/copyright files from each exact component artifact. Preserve evidence of source, version, modifications, checksums and retrieval date.
5. Record applicable license expressions and exceptions, source obligations, notice obligations, patent clauses, commercial/hosting restrictions and unresolved questions.
6. Have an authorized reviewer approve a disposition for every shipped component. Unknown or conflicting evidence is a blocker, not a permissive-license default.
7. Generate an SPDX or CycloneDX SBOM where feasible, and a human-readable notices index. An SBOM alone does not supply full license texts or required corresponding source.
8. Package the reviewed materials with the actual artifact and inspect the finished wheel, VSIX, static bundle, installer, image or air-gap archive.

## Review Categories

| Category | Required treatment |
|---|---|
| Permissive licenses | Check the exact terms; preserve required copyrights, disclaimers, license texts, notices and modification markings. Do not assume every permissive license has identical conditions. |
| LGPL or other limited copyleft | Review modifications, linkage, relinking/replacement requirements, license version and distribution mechanics. Neither automatic rejection nor automatic clearance is appropriate. |
| GPL | Review the combined work/integration and distribution. Resolve any source and downstream licensing obligations before proprietary delivery. |
| AGPL/network clauses | Review remote interaction and modified/combined work obligations for SaaS as well as installed delivery. Hosting is not a blanket exemption. |
| Source-available, noncommercial or custom terms | Inspect commercial use, competing-service, redistribution, field-of-use and approval restrictions. Do not classify these automatically as open source or proprietary-compatible. |
| Dual/multiple licenses | Record which permitted option is chosen and why it covers the exact version/use; retain the evidence. |
| Models, datasets and assets | Review independently from the inference engine/application library; include fonts embedded in reports and assets embedded in exports. |
| Unknown/missing/conflicting terms | Hold release of the affected artifact until resolved. |

## Notice Bundle Layout

Suggested layout for each approved release:

```text
legal/
  LICENSE                         # EOIP proprietary notice
  NOTICE                          # EOIP boundary notice
  THIRD_PARTY_NOTICES.md           # Final artifact-specific index
  sbom.spdx.json                  # Or CycloneDX equivalent
  third-party/
    <ecosystem>-<component>-<version>/
      LICENSE                     # Exact upstream text
      NOTICE                      # When supplied/required upstream
      COPYRIGHT                   # When supplied/required upstream
      MODIFICATIONS.md            # When needed
  source-delivery-manifest.json   # When source obligations apply
```

This example is a target layout, not a claim that those files currently exist or are complete. Required source must be delivered/offered in a manner permitted by the applicable license; an empty manifest is not compliance.

## Customer Communication

- State clearly that EOIP is proprietary but includes independently licensed components.
- Do not remove upstream attribution to create the appearance of exclusive ownership.
- Provide offline-readable notices for offline distributions and an accessible notice path for browser-delivered code.
- Do not prohibit upstream-permitted copying or modification of third-party material through the EULA.
- Do not promise a dependency is commercially licensed, patent-cleared or indemnified unless evidence supports that promise.
- Keep signed customer terms separate from draft internal templates and preserve the exact accepted versions.

## Current Blockers

The default API image includes the `extract-msg` selection from `requirements-fileparse.lock`. The proprietary compatibility decision is unresolved. This policy is not an automated CI blocker; the current build can still produce an uncleared image. Do not publish it as cleared merely because the build succeeds.

All release profiles also need a complete artifact-specific inventory and notice/source bundle. No exhaustive dependency review is claimed in this change.

## References

- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.html)
- [GNU licensing FAQ](https://www.gnu.org/licenses/gpl-faq.en.html)
- [extract-msg 0.56.1 metadata](https://pypi.org/project/extract-msg/0.56.1/)

These references assist review; the exact shipped artifact's applicable terms and qualified legal advice remain necessary.
