# C19 — Supply chain: Sigstore/cosign, Syft, Grype, Trivy, SLSA, in-toto

| Field | Value |
|---|---|
| Registry ID | T-C19-supply-chain |
| Tier | B (SBOM and signing) |
| Versions examined | cosign v3.1.4 (20 Oct); Syft v1.55.0 (19 Oct); Grype v0.121.0 (19 Oct); Trivy v0.76.1 (21 Oct); SLSA spec v1.2; in-toto release page shows v3.1.0-rc (04 May; tag naming inconsistent). Years not shown, 2026 inferred |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
| Member | Owner / governance | Licence | Status |
|---|---|---|---|
| Sigstore (cosign, Fulcio, Rekor, Gitsign) | OpenSSF / Linux Foundation; contributors Google, Red Hat, Chainguard, GitHub, Purdue [CLAIM-sc-01] | Apache-2.0 (project knowledge, 0.85) | active |
| Syft | Anchore | Apache-2.0 (project knowledge; Grype verified Apache-2.0) | active |
| Grype | Anchore, 13.1k stars | Apache-2.0 [CLAIM-sc-03] | active |
| Trivy | Aqua Security | Apache-2.0 [CLAIM-sc-04] | active; **March 2026 compromise** (trivy-action tags force-pushed, setup-trivy and Trivy v0.69.4 backdoored for ~12 h; safe: trivy v0.69.3, trivy-action v0.35.0, setup-trivy v0.2.6) [CLAIM-sc-05] |
| SLSA | OpenSSF specification; **v1.2 Approved** (Build Track, Source Track) [CLAIM-sc-02] | spec (CC-style, UNVERIFIED) | active |
| in-toto | CNCF **Graduated** (accepted 2019-08-14) [CLAIM-sc-06] | Apache-2.0 (project knowledge) | active |
Names unambiguous. Cross-category note: Syft/Grype/Trivy feed CAP-68 (dependency and SBOM risk), signing feeds CAP-79.

## 2. Problem and workflows
Prove what is in EOIP releases and that they were built and signed by the claimed pipeline, including for air-gapped customers. Workflow: CI builds image -> Syft emits SPDX/CycloneDX SBOM -> Grype/Trivy scan with offline DB -> cosign signs image and attests SBOM/provenance (in-toto statement, SLSA predicate) -> customer verifies offline.

## 3. Feature inventory
| Capability | Status |
|---|---|
| Keyless signing (Fulcio short-lived certs + Rekor log) | present [CLAIM-sc-01] |
| Key-based signing, bundles for offline verification | present (bundle format linked; private/air-gapped deployment NOT covered on pages read) |
| SBOM generation (Syft) | present (formats not enumerated on page read) |
| Vulnerability scan from SBOM (Grype) with OpenVEX filtering | present [CLAIM-sc-03] |
| Trivy: SBOM, CVE, IaC, secrets, licences; images, FS, Git, VM, K8s | present [CLAIM-sc-04] |
| SLSA provenance, Verification Summary Attestation | spec, "recommended, not required" formats [CLAIM-sc-02] |
| in-toto layouts and link metadata | present (framework) |
| Air-gap: offline vulnerability DB mirror | Grype/Trivy page captures silent: UNVERIFIED |

## 4. Architecture
```
Source -> CI builder -> artifact(image)
   |-> Syft -> SBOM ----> Grype/Trivy (vuln DB mirror) -> report/VEX
   |-> provenance (in-toto statement, SLSA predicate)
   `-> cosign sign/attest -> registry (OCI referrers) ; Rekor log (public or private instance)
Verifier: cosign verify + policy (identity, issuer, predicate) -> admit/deny
```

## 5. Under-the-hood reconstruction
- Keyless flow: signer authenticates via OIDC, Fulcio issues a short-lived certificate binding identity to an ephemeral public key, artifact signed, entry recorded in Rekor; verifier checks signature, certificate identity vs expectation, chain to the root of trust (TUF-distributed), and Rekor inclusion proof [CLAIM-sc-01]. Air-gap needs private Fulcio/Rekor/TUF or key-based/bundle verification (design inference, not confirmed on pages read).
- Attestations: in-toto Statement {subject digests, predicateType, predicate}; SLSA Build provenance and VSA are predicate types; cosign attaches them as signed envelopes (DSSE; project knowledge, 0.8).
- SBOM scanning: Syft catalogues packages by cataloguer per ecosystem into a graph, serialises SBOM; Grype matches package identifiers (CPE/PURL) to a vulnerability DB built from feeds; Trivy bundles scanner and DB with its own matching. Matching is heuristic: false positives/negatives depend on identifiers (hypothesis from general knowledge).
- SLSA: Build L1-L3 increasing provenance integrity and builder isolation; Source Track in v1.2 [CLAIM-sc-02]; levels detail not listed on the page read.

## 6. Requirements inferred
FR: SBOM per release; signed images/wheels; provenance; scan gate in CI; offline verify. NFR: deterministic reproducible builds where feasible; pinned action SHAs; scanner DB freshness workflow for offline sites.

## 7. Performance and resource model
No benchmark evidence collected: **UNVERIFIED** (scan time scales with image size/package count; Trivy/Grype DB size hundreds of MB, hypothesis). Failure modes: stale DB, SBOM completeness gaps for Python vendored code, Rekor availability for keyless verification, compromised scanner action (observed in Trivy incident).

## 8. Strengths
Standard formats; free tooling; ecosystem adoption; cryptographic transparency. Match: EOIP has `requirements.lock` and licensing signatures (BL-22) but no SBOM/signing/scan tooling in `.github`, `scripts`, `deploy` (case-insensitive grep for cosign, sbom, syft, trivy, grype found only an unrelated script). Exceed: ship verifiable SBOM + attestations inside the offline installer.

## 9. Limitations
| Class | Item |
|---|---|
| Security incident (verified, third-party reports) | Trivy supply-chain compromise Mar 2026 [CLAIM-sc-05] |
| Operational | keyless verification expects public infrastructure; private stack is extra ops |
| Friction | many overlapping formats (SPDX, CycloneDX, VEX variants); SLSA levels need builder support |
| Scope | scanners find known CVEs, not malicious logic; no runtime guarantee |
| Licensing | all Apache-2.0 here; no copyleft trigger identified |

## 10. Deployment, licensing, viability
Self-hostable CLIs/containers; Apache-2.0 allows redistribution. Air-gap: viable via key-based signing and mirrored vulnerability DB (to be proven). Use pinned digests and verify scanner provenance (lesson from CLAIM-sc-05).

## 11. Delta vs EOIP baseline
No baseline BL covers SBOM or signing; CAP-79 is therefore **Absent** (not itemised in 01-SYSTEM-BASELINE; consider new BL). BL-42 code graph has a dependency view (CAP-68 partial). BL-22 offline licensing is licence-key, not artefact signing.

## 12. Cards
**STR-sc-01** | Syft+Grype | SBOM-first scanning, OpenVEX filtering | CLAIM-sc-03 | customer-auditable SBOM, fewer false alarms | integrate | CI emits CycloneDX/SPDX + VEX per release | SBOM lists all lock entries; known-vulnerable test dep flagged.
**STR-sc-02** | cosign/in-toto/SLSA | signed provenance attestations | CLAIM-sc-01,02,06 | trust in offline installer | integrate | key-based signing first, keyless optional | tampered image fails `verify` offline.
**INV-sc-01** (scanner as attack surface, proven by Trivy incident) | pin by digest/SHA, verify signatures of scanner releases, run scanners without secrets, egress-restricted. Option 2: use two independent scanners. Decision ADOPT. Defensibility: process, not code.
**INV-sc-02** (air-gap gap, hypothesis) | private TUF/Rekor too heavy; option: key/bundle offline verification plus DB mirror job. Benchmark: fresh VM, no network, verify + scan passes. Decision EXPERIMENT.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-79 SBOM | INTEGRATE Syft |
| CAP-68 vuln matching | INTEGRATE Grype (primary), Trivy EXPERIMENT (pin after incident) |
| Signing | INTEGRATE cosign (key-based default) |
| SLSA / in-toto | EXPERIMENT (provenance level target L2 first) |
| Own scanner | REJECT |

## 14. Tests
SBOM completeness diff vs `requirements.lock`; offline signature verification; tamper test; CI gate on high CVEs; pinned-SHA lint on workflows; Trivy digest check.

## 15. Risks
DB freshness offline; format churn; Sigstore client v3 behaviour changes (tag v3.1.4); in-toto release naming ambiguity.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1,D21 | 1,10 | owners, incident, all Apache-2.0 |
| D2-D3,D17 | 2,4,8 | release trust pipeline |
| D18 | 5,9 | supply chain |
| D20,D24 | 7,C | UNVERIFIED; vendor/secondary |
| D22 | 5 | formats |
| Others | N/A | not applicable |

## Appendix B — Capabilities
| CAP | Native? | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-79 | native | 01-04,06 | Absent (no BL) | INTEGRATE | P1 |
| CAP-68 | native | 03,04 | BL-42 Partial | INTEGRATE | P2 |
| CAP-50 | partial | 01 | - | EXPERIMENT | P2 |
| CAP-52 | provides trust | 02 | BL-21 | INTEGRATE | P2 |

## Appendix C — Evidence
| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-sc-01 | Sigstore, cosign v3.1.4 | components, keyless flow, OpenSSF backing | Officially documented | https://docs.sigstore.dev/ ; https://github.com/sigstore/cosign/releases/latest | 20 Oct / 2026-10-26 | 0.85 | air-gap not covered |
| CLAIM-sc-02 | SLSA v1.2 | Approved; Build and Source tracks; provenance/VSA recommended not required | Officially documented | https://slsa.dev/spec/v1.2/ | n/a / 2026-10-26 | 0.85 | levels not listed |
| CLAIM-sc-03 | Grype v0.121.0 | Apache-2.0; scans SBOMs; OpenVEX | Officially documented | https://github.com/anchore/grype | 19 Oct / 2026-10-26 | 0.85 | offline not covered |
| CLAIM-sc-04 | Trivy v0.76.1 | Apache-2.0; scanner types and targets | Officially documented | https://github.com/aquasecurity/trivy | 21 Oct / 2026-10-26 | 0.85 | none |
| CLAIM-sc-05 | Trivy 0.69.4 | Mar 19-20 2026 compromise of trivy-action, setup-trivy, binary | Third-party report | https://snyk.io/articles/trivy-github-actions-supply-chain-compromise/ ; https://wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack | 2026-03 / 2026-10-26 | 0.8 | Aqua postmortem not read |
| CLAIM-sc-06 | in-toto | CNCF Graduated (2019-08-14); release page v3.1.0-rc | Officially documented | https://www.cncf.io/projects/ ; https://github.com/in-toto/in-toto/releases/latest | n/a / 2026-10-26 | 0.7 | tag naming inconsistent |
| CLAIM-sc-07 | Syft v1.55.0 | latest release 19 Oct | Officially documented | https://github.com/anchore/syft/releases/latest | year not shown | 0.8 | licence not fetched |

## Appendix D — Assumptions
Syft, cosign and in-toto licences assumed Apache-2.0 from project knowledge. Years inferred.
