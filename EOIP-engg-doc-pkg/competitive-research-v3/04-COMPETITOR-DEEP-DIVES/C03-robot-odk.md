| Field | Value |
|---|---|
| Registry ID | T-C03-robot-odk |
| Tier | B (ontology CI/release tooling reference) |
| Versions examined | ROBOT 1.9.11 (Maven Central 2026-10-01; 1.9.10 2026-02-19, 1.9.9 2026-02-18); ODK v1.6.1 (10 Mar 2026), v1.6, v1.5.4 (7 Dec 2024) |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
ROBOT: "command-line tool and library for automating ontology development tasks", `ontodev/robot`, BSD-3-Clause, Java, built on the OWL API [CLAIM-robot-01]. Latest 1.9.11, Maven metadata updated 2026-10-01 [CLAIM-robot-02]. ODK: `INCATools/ontology-development-kit`, "Ontology lifecycle management", BSD-3-Clause, bundles ROBOT, owltools, dosdp-tools in Docker images `obolibrary/odklite` and `odkfull`, plus a seed script, Makefiles and GitHub Actions workflows [CLAIM-robot-03]. Latest ODK release listed v1.6.1 (March 2026). Both active, not archived. Governed by the OBO/INCATools community (formal governance NOT verified).
Sources: `https://github.com/ontodev/robot`, `https://robot.obolibrary.org/`, `https://github.com/INCATools/ontology-development-kit`, Maven Central metadata.

## 2. Problem, workloads, workflows
Make ontology maintenance a build pipeline: edit source file -> merge imports -> extract modules -> reason -> QC report -> release artefacts with version IRIs. Real workflow: contributor PR changes `*-edit.owl`; GitHub Actions in the ODK container runs `make test`; release job produces `*.owl`, `*-base`, `*-full`, diffs against previous release.

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| `reason` with ELK (default), HermiT, JFact, Whelk, EMR, Structural; fails on inconsistency/unsatisfiable | present | [CLAIM-robot-04] |
| `diff` semantic (structure-insensitive) compare; plain/pretty/html/markdown output | present | [CLAIM-robot-05] |
| `report` QC rules, `verify` SPARQL checks, `template`, `extract` modules, `merge`, `convert`, `annotate`, `release` helpers | present (named from ROBOT documentation index; only reason and diff pages opened) | UNVERIFIED for individual commands except reason/diff |
| ODK seed script, repo template, Makefile pipeline, dynamic imports, Docker, GitHub Actions | present | [CLAIM-robot-03] |
| SHACL validation | absent / not verified | UNVERIFIED |
| GUI | absent | inference |
| Multi-user live editing | absent (Git is the collaboration layer) | inference |

## 4. Architecture diagram
```
 Git repo (src/ontology/<id>-edit.owl, imports/, components/, config yaml)
   -> ODK Docker image (ROBOT + owltools + dosdp + make)
       make: merge -> extract/import modules -> reason(ELK) -> report/verify(SPARQL) -> release(version IRI)
   -> GitHub Actions CI -> release artefacts (OWL, OBO, JSON) + diff vs last release
```

## 5. Under-the-hood reconstruction
Data model: OWL API in-memory ontology; ROBOT commands are chained ("command chaining") passing the ontology object between steps, so a pipeline is a single JVM invocation (documented design: Commands and Operations; hypothesis for chaining internals). `diff` compares axiom sets, not text, so reformatting does not register [CLAIM-robot-05]. `reason` first checks consistency/coherence, fails with non-zero exit, optionally writes inferred axioms into a separate ontology or annotates them `is_inferred` [CLAIM-robot-04]: this is an inferred/asserted separation worth copying. ODK orchestrates with Make targets and a repo-layout convention, giving reproducible builds via pinned container versions. Concurrency, transactions, storage, security: N/A (batch tool). Versioning: version IRIs per release plus Git history. Entry points not opened at a pinned tag.

## 6. Inferred requirements
Deterministic builds in a container; non-zero exit for gate failures; machine-readable and human-readable diffs; separation of asserted, inferred, base and full releases; offline imports via catalog files (`--left-catalog` option) [CLAIM-robot-05].

## 7. Performance and resource model
No benchmarks found. JVM memory scales with ontology size (OWL API object model); ELK default keeps reasoning fast on EL ontologies. Failure modes: out-of-memory on large ontologies; non-EL constructs ignored by ELK; HermiT-only tautology exclusion is slower [CLAIM-robot-04].

## 8. Strengths
Mature, community-proven ontology release discipline; semantic diff; reasoner gate; reproducible container; BSD-3. Match: reproduce the pipeline stages in EOIP gitops CI; exceed with tenant-aware branches, SHACL gates and evidence manifests.

## 9. Limitations
Verified: edit workflow assumes Git literacy and file-based OWL; reasoner ELK default is EL-only [CLAIM-robot-04]; diff page does not document exit codes [CLAIM-robot-05]. Hypotheses: OWL API in-memory ceiling; no built-in approval workflow beyond PRs; ODK image is large and Java/Make-heavy (size not measured). Friction: Make/Docker skills required; configuration learning curve.

## 10. Deployment, licensing, viability
BSD-3 for both: redistribution-safe. Bundled third-party tools in ODK images carry their own licences (not audited): check SBOM before shipping the image. Air-gap: yes with pre-pulled images and local catalogs. Java/Docker adds runtime to a Python product; use as dev-time CI tool, not runtime dependency.

## 11. Competitive delta vs baseline
BL-32: `ontology/gitops.py:31` has `diff_manifests`, breaking-change verdict (`PUBLISH_OK` / `BREAKING_CHANGE_REFUSED`), branch and PR objects held in memory (dict-backed, per INV-edg-01 in C03-topbraid-edg.md; not re-verified in code here beyond `source_branch`/`target_branch` dataclass fields), `scripts/ontology_diff.py`. Missing against ROBOT/ODK: persisted release artefacts with version IRIs, asserted/inferred/base/full variants, reason gate on a standard reasoner (BL-30), QC report catalogue, SPARQL `verify` checks, and reproducible container build. EOIP differs: the manifest is an LPG label list, not OWL.

## 12. Cards
**STR-robot-01** | ROBOT/ODK | one reproducible pipeline: merge, module extraction, reason gate, QC, release with diff | [CLAIM-robot-03][CLAIM-robot-04] | auditable ontology releases | match | implement stages as gitops CI steps (parse, SHACL, diff classify, reason, impact report, tag) | acceptance: replay 200 real changes, 100% breaking flagged, <60 s per run on one node.
**STR-robot-02** | ROBOT `diff` | semantic comparison ignoring serialisation | [CLAIM-robot-05] | stewards review meaning not text | exceed | classified diff (breaking/additive) already exists; add canonical serialisation so Git diffs match | acceptance: re-ordered Turtle yields empty diff.
**INV-robot-01** | ROBOT/ODK 2026 | Git/Make/Docker-only authoring excludes non-technical stewards; no tenant concept | evidence: workflow design [CLAIM-robot-03]; no complaints cited | root cause UX/governance (*hypothesis*) | alternative: web editor that writes commits to the same repo and runs the same CI; worse for fully offline individual curators | options (a) wrap ODK container in EOIP CI; (b) gitops over real repo with web approval UI; (c) multi-tenant release service | selected (b) | POC: time-to-first-published-change for a non-Git user vs ODK baseline | decision EXPERIMENT.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-41 governance (review, release, rollback) | BUILD on gitops; reference ROBOT/ODK |
| CAP-35 diff/merge/rollback | BUILD |
| CAP-37 evolution/migration | BUILD |
| CAP-23 reasoner gate | INTEGRATE ELK via ROBOT in CI (dev-time) |
| CAP-79 supply chain (pinned build images) | REUSE pattern |

## 14. Tests
(PROPOSED.) Run ODK on a fixture ontology in an offline container; compare ROBOT `diff` verdicts to `diff_manifests` on the same change corpus; inject an unsatisfiable class and require refusal; verify re-serialised files produce empty diff; measure CI time and image size.

## 15. Risks and open questions
Java toolchain in a Python product; ODK image licence audit; whether OWL files map losslessly to the EOIP LPG manifest; ODK release dates for v1.6 year not shown on page (inferred 2025); exit-code semantics of `diff` unverified.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | BSD-3, active |
| D2 | 2 | Release pipelines |
| D3 | 4 | Make + container |
| D4 | N/A | Files only |
| D5 | 5 | OWL files |
| D6 | 3 | SPARQL verify (UNVERIFIED) |
| D7 | 3,5 | Reason gate |
| D8 | N/A | Batch |
| D9 | 3 | Imports, templates |
| D10 | N/A | None |
| D11 | 5 | Version IRIs, Git |
| D12 | N/A | None |
| D13 | N/A | None |
| D14 | N/A | None |
| D15 | 2,9 | PR-based governance |
| D16 | 9 | CLI only |
| D17 | 2,3 | CI/GitOps core |
| D18 | N/A | None |
| D19 | N/A | None |
| D20 | 7 | No data |
| D21 | 10 | Free |
| D22 | 11 | OWL-centric |
| D23 | N/A | None identified |
| D24 | App. C | Docs and Maven; source not opened |

## Appendix B. Capability mapping
| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-41 | partial (via PR) | 03 | BL-32 Partial | BUILD | P1 |
| CAP-35 | native diff, Git merge | 05 | BL-32 | BUILD | P1 |
| CAP-37 | partial | 03 | BL-32 | BUILD | P1 |
| CAP-23 | plugin (ELK) | 04 | BL-30 | INTEGRATE | P2 |
| CAP-79 | partial (container) | 03 | none | REUSE pattern | P2 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-robot-01 | ROBOT | CLI and library for ontology automation; BSD-3-Clause | Officially documented | https://github.com/ontodev/robot | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-robot-02 | 1.9.11 | Maven latest/release 1.9.11, updated 2026-10-01; 1.9.10 2026-02-19 | Officially documented | https://repo1.maven.org/maven2/org/obolibrary/robot/robot-core/maven-metadata.xml ; search result citing Maven listing | 2026-10-01 / 2026-10-26 | 0.85 | GitHub releases page showed no year |
| CLAIM-robot-03 | ODK v1.6.1 | BSD-3; bundles ROBOT, owltools, dosdp-tools; odklite/odkfull images; seed, Makefiles, GH Actions; releases v1.6.1 (10 Mar 2026), v1.5.4 (7 Dec 2024) | Officially documented | https://github.com/INCATools/ontology-development-kit and /releases | 2026-03-10 / 2026-10-26 | 0.8 | year of v1.6 not shown |
| CLAIM-robot-04 | ROBOT reason | ELK default; HermiT, JFact, Whelk, EMR, Structural; fails on incoherence; inferred axioms separable/annotated; ELK EL-only | Officially documented | https://robot.obolibrary.org/reason | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-robot-05 | ROBOT diff | Compares ontologies semantically, formats plain/pretty/html/markdown, catalog options; exit codes undocumented on page | Officially documented | https://robot.obolibrary.org/diff | n/a / 2026-10-26 | 0.8 | none |

## Appendix D. Assumptions
Access date is the real date. Command inventory beyond reason/diff taken as unverified. EOIP `gitops.py` branch storage taken from C03-topbraid-edg.md INV-edg-01 and the dataclass fields seen; not fully re-audited.
