# EOIP Third-Party Notices Index

Prepared: 2026-10-14. **PRELIMINARY INDEX; NOT A COMPLETE RELEASE ATTRIBUTION BUNDLE OR COMPATIBILITY APPROVAL.**

Third-party authors retain their rights. The EOIP proprietary notice applies only to owned material. Actual upstream licenses and notices, not this summary, control third-party components. This index does not grant permission to relicense them.

## Dependency Evidence Locations

| Component group | Repository evidence | Required release action |
|---|---|---|
| Python API/runtime | `pyproject.toml`, `requirements.lock` | Inspect exact installed release distributions and their transitive dependencies; retain license/notice texts and provenance |
| Optional numerical N0 tier | `pyproject.toml` extra `numerics`; `requirements-neural.lock` (generation pending) | Review the exact resolved wheel set and bundled native-library notices before distribution; see the specific N0 findings below |
| RDF serialization and canonical actions | `rdflib==7.6.0` (BSD-3-Clause), `rfc8785==0.1.4` (Apache-2.0), `licenses/rdflib-7.6.0.md`, `licenses/rfc8785-0.1.4.md` | Verify the resolved artifacts and included license texts in each shipped wheel/image; this source index does not itself constitute release clearance |
| Optional document/archive/email parsing | `pyproject.toml` fileparse extra, `requirements-fileparse.lock` | Resolve copyleft and executable-tool obligations; do not assume optional means absent from delivery |
| Report generation | `pyproject.toml` reports extra | Inventory ReportLab, python-docx, python-pptx, dependencies and embedded fonts separately |
| Web runtime | `apps/web/package.json`, `apps/web/package-lock.json` | Inventory actual bundled code, including React, React DOM, Cytoscape, Graphology, Sigma and transitive runtime modules |
| VS Code extension | `apps/vscode-extension/package.json`, `apps/vscode-extension/package-lock.json` | Inspect the actual VSIX; distinguish development tools from code included in it |
| Containers/deployment | `deploy/Dockerfile`, `apps/web/Dockerfile`, `deploy/hubble/Dockerfile`, deployment manifests | Include base images, OS packages, server products and modified upstream UI material |
| Models, fonts, images, datasets and native utilities | Actual release and configured runtime assets | Collect each component's own terms, provenance, commercial permissions and redistribution restrictions |

The specification `EOIP-engg-doc-pkg/69-dependency-license-sbom.md` describes a governance process. It is not a populated, approved SBOM for the current release.

## Optional Numerical N0 Development Profile

The new `numerics` extra was installed and exercised on Windows x86_64 / Python 3.11 with NumPy 2.4.6, SciPy 1.17.1, and scikit-learn 1.9.1. Their exact upstream license files from those installed wheels are retained at `licenses/numpy-2.4.6-LICENSE.txt`, `licenses/scipy-1.17.1-LICENSE.txt`, and `licenses/scikit-learn-1.9.1-COPYING.txt`; each repository copy was SHA-256 compared with its source file in the installed distribution.

The NumPy and SciPy Windows wheel license files report bundled OpenBLAS (BSD-3-Clause), LAPACK (BSD-3-Clause-Open-MPI), and GCC runtime files under `GPL-3.0-or-later WITH GCC-exception-3.1`; the scikit-learn wheel also reports Microsoft Visual C++ runtime files. This is a transitive binary-wheel notice and compatibility review item, not a conclusion that the N0 distribution is cleared or prohibited. Assess the exact artifacts and delivery mode under `licenses/THIRD-PARTY-POLICY.md` before distribution. The current development wheel set must not be presented as a cleared commercial release.

## Known Distribution Concern

`requirements-fileparse.lock` pins `extract-msg==0.56.1`; [upstream metadata identifies GPL licensing](https://pypi.org/project/extract-msg/0.56.1/). `deploy/Dockerfile` currently installs that lockfile into the default runtime image. This is an active distribution-review concern, not merely an unused development dependency.

Inspect the exact upstream artifact, version-specific terms and the actual Python integration. Options requiring approval include replacing the integration with a suitable alternative, obtaining sufficient alternative rights where available, excluding the feature and its dependencies from a particular release, or meeting applicable copyleft obligations where compatible with the intended distribution. This document does not select or certify an option. A process boundary, customer-side install instruction or separate container is not automatically sufficient.

`RTFDE`, `oletools`, archive components, external RAR/office/OCR utilities, fonts and all transitive dependencies also require inspection; this index does not assign them unverified license classifications.

## Why Local Metadata Is Not a Release Inventory

At preparation time, the development environment had FastAPI 0.115.6 and Uvicorn 0.34.0, while `requirements.lock` selects FastAPI 0.142.2 and Uvicorn 0.54.0. Copying licenses from that development environment and labeling them as the locked release would be misleading. `extract-msg` was not installed locally even though the Dockerfile selects it.

Collect notices from the exact resolved build environment/artifacts. Missing packages, a different version, a metadata label without a license file, or a missing transitive component must remain unresolved, not assumed permissive.

## Required Final Bundle

GUI implementation additions, 2026-10-16: `lucide-react` 0.468.0 is a runtime dependency; its package-supplied license is retained at `apps/web/public/legal/third-party/lucide-react-0.468.0-LICENSE.txt` and copied by the web build. TypeScript 5.9.3 and `@axe-core/playwright` 4.10.2 are development tools in this batch. The axe Playwright package reports MPL-2.0 in its installed metadata; distinguish development/test tooling from distributed runtime code and review actual artifacts. This addition does not complete the release inventory or clear the existing distribution concerns.

Each distributed artifact must have an associated component inventory recording name, version, source/provenance, artifact digest, shipped location, license expression/evidence, modifications, upstream copyright/NOTICE files, and required source/offer delivery.

Include the full applicable license texts and required notices, preserving their wording. An SPDX identifier, website link, this index, or a generic MIT/Apache text without the component's required attribution is not a substitute for the required materials. Do not invent a source offer that cannot be fulfilled.

Use [licenses/THIRD-PARTY-POLICY.md](licenses/THIRD-PARTY-POLICY.md) and [licenses/RELEASE-CHECKLIST.md](licenses/RELEASE-CHECKLIST.md). No claim of complete dependency clearance is made by the presence of this file.
