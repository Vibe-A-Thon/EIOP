# EOIP Licensing Guide

Updated: 2026-10-14. Product licensing direction approved by the project owner: proprietary commercial licensing for owned code, with both hosted SaaS and customer-installed deployments.

Named rights holders supplied by the project owner: **Avyukthi AI and Murthy Ravinder kumar**. These names are used as supplied; no company registration, ownership assignment, or authority to bind either party has been inferred.

## The Simple Explanation

The product has multiple licensing layers, not one license that overwrites everything:

| Material | Applicable terms | What a customer receives |
|---|---|---|
| Original code and documentation you own | [Root proprietary notice](LICENSE), plus the executed commercial agreement | Only the usage/source/redistribution rights actually granted in the agreement |
| Third-party libraries and incorporated code | Each component's original license | Those licenses, required notices, and any required source-related materials |
| Fonts, icons, models, datasets, images, containers and external programs | Their respective licenses or contracts | Applicable attribution, restrictions, and any separately required delivery materials |
| Customer data | The customer agreement and applicable data-protection terms | No claim of ownership merely because EOIP processes the data |

For example, a customer can receive a proprietary EOIP application containing a separately licensed permissive library. The library stays under its original terms. This does not automatically give the customer rights to EOIP's original code. Conversely, the EOIP agreement must not remove the customer's rights in that library. Copyleft combinations require additional review; this example is not clearance for GPL-linked code.

This is **not dual licensing the entire product** under a choice of Apache or commercial terms. It is proprietary first-party licensing alongside independent third-party licenses.

## Document Map

| File | Role | Status |
|---|---|---|
| [LICENSE](LICENSE) | Current first-party proprietary notice; no public license grant | Applied to owned material only |
| [NOTICE](NOTICE) | Ownership boundary and important distribution warning | Not a substitute for upstream notices |
| [Commercial terms](licenses/COMMERCIAL-LICENSE-DRAFT.md) | Proposed common terms for SaaS and installed software | Draft; needs owner/counsel approval and an executed order |
| [Order form](licenses/ORDER-FORM-TEMPLATE.md) | Customer, licensor, deployment, price, term, support and agreed exceptions | Template; no rights granted until completed and executed |
| [Third-party notices index](THIRD_PARTY_NOTICES.md) | Known dependencies, evidence locations and unresolved obligations | Preliminary; not a complete release SBOM |
| [Third-party policy](licenses/THIRD-PARTY-POLICY.md) | How to collect and preserve component-specific licenses | Release preparation procedure |
| [Ownership register](licenses/OWNERSHIP-REGISTER.md) | Evidence of rights and the identity of the contracting licensor | Relationship/authority confirmation still needed |
| [Release checklist](licenses/RELEASE-CHECKLIST.md) | Distribution-specific checks and outstanding blockers | Not yet a passed release gate |

## How Scope Works Across the Repository

The root notice follows first-party material in `apps/`, `packages/`, `scripts/`, `config/`, `deploy/`, `tests/` and owned documentation. Directory location alone does not prove ownership. Existing third-party headers, copied code, vendored components, sample data, assets and separately licensed files are excluded from any unsupported ownership claim.

Do not replace upstream LICENSE files in `node_modules`, installed Python distributions, container layers, model directories or vendored source. Do not insert proprietary headers into someone else's files. Preserve provenance when modifying third-party code.

For new original files, the following header may be used where a header is appropriate, after ownership is confirmed:

```text
Copyright (c) 2026 Avyukthi AI and Murthy Ravinder kumar.
SPDX-License-Identifier: LicenseRef-EOIP-Proprietary
```

`LicenseRef-EOIP-Proprietary` is a local identifier for the accompanying notice, not an OSI-approved license or a statement about dependencies. Existing files have not been mass-stamped.

## What to Ship

| Delivery | Licensing materials and decisions |
|---|---|
| Hosted SaaS | Executed subscription/order terms, privacy/data-processing terms where applicable, and accessible notices for code/assets delivered to browsers. Review server-side licenses too; hosting is not a universal exemption. |
| Python wheel/source package | First-party notice and supporting documents in package license metadata; separate dependencies retain their own notices. A wheel is not a clearance certificate for its installed dependency environment. |
| On-premises container or air-gap bundle | First-party notice, customer agreement, exact image/package/model inventory, component license texts/notices, required source or offers, and an offline-readable notices location. Review base-image OS packages as well as pip/npm packages. |
| Browser/static bundle | First-party notice plus notices/license texts for third-party code actually included in the compiled bundle, including fonts/assets. A `node_modules` directory left on the build machine does not deliver notices to the customer. |
| VS Code extension | Module notice and the approved commercial terms/reference, plus notices for code actually embedded in the VSIX. Build-only dependencies must be distinguished from shipped code. |
| Source access or OEM/resale | Explicit order-form permissions for source, modifications, redistribution, sublicensing, branding and downstream notices; do not assume ordinary internal-use rights cover these activities. |

The Python package configuration includes the first-party licensing documents. The API Docker build copies them before packaging. Module-level notices are supplied for the web app and VS Code extension. These steps do **not** assemble or approve a complete third-party notice bundle for every delivery channel.

## Decisions Still Needed

1. Confirm whether Avyukthi AI is a registered legal entity, a trading name of Murthy Ravinder kumar, or a separate rights holder; identify who signs customer agreements and who owns each first-party contribution.
2. Complete customer-specific fees, subscription/perpetual rights, permitted deployments, renewal, support, warranty/liability terms, data-processing requirements, governing law and dispute terms.
3. Resolve the `extract-msg` GPL issue before distributing the default API image; review all other exact component versions and their transitive dependencies.
4. Approve actual release inventories and notices. The current documents do not certify all dependencies as compatible.
5. Check prior releases and contribution terms. This change cannot revoke rights previously granted to recipients.

These documents establish a practical licensing structure and drafting starting point. They are not a legal opinion or an executed customer contract. Obtain software-licensing counsel review for your business jurisdiction and intended customer markets before external release.

## Source References

- [Apache License 2.0, sections 2 and 4](https://www.apache.org/licenses/LICENSE-2.0.html): existing grants and redistribution conditions remain relevant to Apache components and earlier releases.
- [extract-msg 0.56.1 metadata](https://pypi.org/project/extract-msg/0.56.1/): upstream identifies the package as GPL; inspect the exact distribution's license and integration before approval.
- [npm license metadata](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/#license): `UNLICENSED` communicates no public license grant; it does not mean public domain or eliminate a separate commercial contract.
