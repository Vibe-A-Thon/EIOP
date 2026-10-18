# 22 — Open Questions and Assumptions

Every assumption made instead of asking a question (Master Prompt §3.1), with its impact if wrong. Worker-level assumptions are recorded in appendix D of each deep dive; the ones that affect programme-level decisions are lifted here.

## 1. Programme-level assumptions

| A-ID | Assumption | Basis | Impact if wrong | How to confirm |
|---|---|---|---|---|
| A-01 | The product name in all artifacts stays "KnowGridFlow / EOIP"; "Semaplexvell" is not used until its spelling is confirmed | Master Prompt header: "confirm spelling before use in any artifact" | Rename pass needed across the package (text only) | Product owner confirms the name |
| A-02 | Output location is `EOIP-engg-doc-pkg/competitive-research-v3/` (the prompt names files, not a folder) | Existing documentation package lives in `EOIP-engg-doc-pkg/`; a subfolder avoids colliding with `00-specification-audit…` and `01-project-vision.md` | Files can be moved without content changes | User preference |
| A-03 | "Do not modify production source code" covers all of `packages/`, `apps/`, `config/`, `deploy/`, `schemas/`, `tests/`; only new documentation under the output folder is written | Master Prompt §0 | None — conservative | — |
| A-04 | Parallel research used 35 worker agents, one per coherent batch, instead of one per technology | Environment allowed 20 concurrent subagents; one worker per technology (329 entries) was not practical | Depth per Tier A item could be lower than with one worker each; the depth gate in §17 is checked per file in `00-EXECUTIVE-SUMMARY.md` | Gate check results |
| A-05 | No proofs of concept or benchmarks are executed in this run; they are specified as PROPOSED | Master Prompt §16 item 21 says "run only if authorized and possible"; no authorisation to install engines was given | All performance statements stay at documented/vendor-claim level | Separate, explicit authorisation |
| A-06 | Commercial SaaS products are researched from public documentation only (no trial accounts) | Lawful-research constraint; no credentials were provided | Some internals remain NOT PUBLICLY VERIFIED | Authorised trials |
| A-07 | Interim compute policy is CPU-only (ADR-H15 accepted, ADR-H16 accepted, ADR-H17 open) | `docs/decisions/` | GPU-dependent options are DEFER until H-17 is decided | Decision on H-17 |
| A-08 | Neptune is treated as a required **supported** backend even though it cannot run air-gapped; air-gapped deployments use HugeGraph or Neo4j | Constraint 1 (air-gap) vs §4.2 (Neptune required) | If a customer needs Neptune and air-gap at once, there is no answer — flagged as a conflict | Product decision |
| A-09 | Customer segments: regulated enterprises (finance, public sector, healthcare, industrial) first, then general enterprise; non-IT journeys (J15) are first-class | Master Prompt §2.1 ("any organisation") | Priority scores for IT-only capabilities would rise | Product strategy input |
| A-10 | Scale target for the one-node tier: up to ~10M nodes / ~50M edges per tenant; larger needs distributed tiers | Master Prompt §12 data tiers (100k / 1M / 10M+), §4.3 item 10 | Sizing in `17-OPERATIONS-SRE-COST-MODEL.md` changes | Customer data |
| A-11 | Legal conclusions on licences are out of scope; the package records licence facts and legal-review triggers only | Master Prompt §7 dimension 23, §17 licensing gate | — | Legal review |
| A-12 | Existing ADR numbering (ADR-001..010, ADR-H15..H17) is preserved; this package uses ADR-KG3-NN | Avoid collisions with `EOIP-engg-doc-pkg/64-decisions-and-adrs.md` and `docs/decisions/` | — | — |

## 2. Baseline uncertainties carried forward

See `01-SYSTEM-BASELINE.md` § BASELINE_UNCERTAINTIES (U-01..U-12). Every later artifact that depends on one of them is labelled **PROVISIONAL** and names the U-ID.

## 3. Open questions for the product owner (not blocking this run)

| Q-ID | Question | Default used in this package |
|---|---|---|
| Q-01 | Which backend is the default for air-gapped installs: HugeGraph or Neo4j Community? | HugeGraph stays the default (ADR-001/002); Neo4j Community is offered as an option with its GPL-3.0 terms flagged |
| Q-02 | Is a GPL/AGPL component acceptable if it runs as a separate, unmodified service that the customer installs? | Treated as a legal-review trigger, never as accepted |
| Q-03 | Is an RDF/OWL sidecar a product feature or an export/validation tool only? | Optional module (constraint 7), off by default |
| Q-04 | Will EOIP sell a managed/SaaS edition? | Self-hosted first; SaaS terms of licences still recorded |
| Q-05 | Target pricing/packaging tiers for white-label partners | Not modelled beyond TCO inputs |

## 4. Worker-level assumptions lifted to programme level

WORKER-ASSUMPTIONS-PLACEHOLDER
