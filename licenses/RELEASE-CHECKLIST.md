# Commercial Licensing Release Checklist

Prepared: 2026-10-14. **Current disposition: NOT CLEARED FOR COMMERCIAL DISTRIBUTION.**

This disposition concerns licensing review, not whether the application compiles or its tests pass. It is a documented gate, not an implemented automated publishing block.

## Release Identity

| Field | Value |
|---|---|
| Release/version and source revision | TO BE COMPLETED |
| Artifact names/digests and target platforms | TO BE COMPLETED |
| SaaS / on-premises / desktop / VSIX / source / OEM profiles | TO BE COMPLETED |
| Licensor and authorized reviewer | TO BE COMPLETED |
| Customer agreement/order version | TO BE COMPLETED |

## Ownership and Customer Terms

- [x] Project owner selected proprietary licensing for owned code.
- [x] Project owner supplied Avyukthi AI and Murthy Ravinder kumar as the relevant names.
- [x] Both SaaS and installed deployment modes are represented in the draft documents.
- [ ] Confirm legal entity/trading-name relationship and authority to contract.
- [ ] Complete first-party ownership and contribution provenance review.
- [ ] Review earlier releases and preserve existing license grants.
- [ ] Approve commercial terms and complete the order, financial, support, liability and jurisdiction fields.
- [ ] Complete SaaS privacy/data-processing/security terms where applicable.
- [ ] Obtain required signatures; do not treat these drafts as accepted contracts.

## Third-Party Clearance

- [ ] Inventory exact artifacts, transitive packages, base images, native utilities, fonts, assets, datasets and models.
- [ ] Resolve `extract-msg` and the actual default Docker image's GPL-related compatibility obligations.
- [ ] Review the optional N0 numerical wheel bundle's bundled GCC runtime (GPL-3.0-or-later with GCC exception), OpenBLAS/LAPACK notices, and Microsoft runtime terms for each shipped platform.
- [ ] Review all other copyleft, source-available, custom, unknown and conflicting licenses.
- [ ] Record the approved license option for multi-licensed components.
- [ ] Collect exact upstream texts/notices and preserve modification attributions where required.
- [ ] Deliver corresponding source or valid source offers when required; verify they can be fulfilled.
- [ ] Generate and approve artifact-specific SBOMs and notices indexes.

## Package Inspection

- [ ] Python wheel/sdist contains the first-party licensing documents and correct metadata.
- [ ] API/worker image contains the license materials, including dependencies and base layers actually shipped.
- [ ] Static browser bundle includes accessible third-party license/attribution materials for bundled code/assets.
- [ ] VSIX includes the first-party notice and applicable embedded-code third-party notices.
- [ ] Hubble/customized upstream UI retains its upstream terms and marks modifications where required.
- [ ] Air-gap/archive/installer includes offline-readable notices and required source-related materials.
- [ ] Signed customer terms or the agreed authoritative reference accompany delivery; internal drafts are not misrepresented.
- [ ] No package labels the entire dependency tree as EOIP-owned or Apache-licensed first-party code.

## Approval Record

| Review | Approver | Date | Evidence | Decision |
|---|---|---|---|---|
| Ownership and licensor authority | Pending | Pending | Pending | Pending |
| Commercial terms | Pending | Pending | Pending | Pending |
| Third-party compatibility and obligations | Pending | Pending | Pending | Pending |
| Final artifact contents | Pending | Pending | Pending | Pending |
| Release authorization | Pending | Pending | Pending | Pending |

Successful tests, a generated document, or the presence of a root LICENSE do not replace these approvals. No dependencies or features were removed automatically by the licensing-document change.
