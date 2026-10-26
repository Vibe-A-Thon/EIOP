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

Every worker recorded its access date as 2026-10-26 (the actual session date) rather than the programme's nominal baseline date of 2026-10-18, and noted this in its own evidence appendix. This affects no conclusion; it is recorded once here rather than in all ~200 deep dives.

A prior, non-evidence-based process wrote placeholder content into this package on 2026-10-19 (39 deep-dive files with no CLAIM records, plus draft versions of `00`, `02`, `05`–`23`, the ADRs and one POC). Every one of these was identified and overwritten with evidence-based content during this run, with one exception caught and corrected in place: the CAP-12 (SKOS) row in `05-COMPARISON-COHORTS/03-ONTOLOGY-GOVERNANCE-COHORT.md` originally read "absent"; it is corrected to "Implemented" (see `01a-BASELINE-DELTA-HEAD.md` and §5 below). A fabricated "POC-01 PASS" claim in `20-POC-EXPERIMENTS/poc-01-multi-backend-compilation/run_poc.py` (output hardcoded independent of input) was replaced with an honest specification stub.

## 5. Evidence conflicts found between independent deep dives (not resolved further; flagged for re-verification)

These did not change any decision in the gap register or matrix, but a reader comparing two deep dives will see them and should know they are tracked, not missed.

| Conflict | Sources | Status |
|---|---|---|
| EOIP's own SKOS capability (CAP-12) | Baseline delta (`01a-BASELINE-DELTA-HEAD.md`) says Implemented, 1,417 lines, tests passing; an early draft of the ontology-governance cohort said absent | **Resolved in this run** — cohort file corrected; see §4 above |
| GraphScope throughput | Vendor blog claims >80,000 QPS; vendor's own docs cite 33,180.87 ops/s for the same benchmark | Unreconciled — neither figure adopted anywhere in this package |
| Dgraph licence | v25 release notes say the whole codebase is Apache-2.0; the official licensing page still describes a Community License split for enterprise features | Unreconciled — registry records both statements |
| QLever licence | The project's own documentation says Apache-2.0; a third-party catalogue (DBDB) says MIT | Resolved by preference — the project's own LICENSE file is authoritative; treat as Apache-2.0 |
| Senzing PostgreSQL version requirement | Differs across Senzing's own documentation pages | Unreconciled |
| Splink 5.0.0 release date | PyPI and GitHub release pages disagree | Unreconciled |
| Onyx connector count | Stated as 56, "40+" and "50+" across different pages | Unreconciled |
| DataHub backend support | Docs disagree on MySQL/Postgres and Elasticsearch/OpenSearch support | Unreconciled |
| TerminusDB current maintainer | Named three different ways across sources (team/individual naming varies) | Unreconciled |
| Gephi licence | Stated as GPL-3.0 (GitHub), dual CDDL 1.0/GPL v3 (project wiki), and GPL only (gephi.org) in three different official sources | Unreconciled — legal review should read the actual LICENSE file before any bundling decision |
| Neo4j Cypher-25-default rollout date | One deep dive gives 2026.02 (confidence 0.6); another gives a related but different GA date of 2026.06 for GRAPH TYPE | Unreconciled, low-stakes |
| Mem0 LoCoMo scores | Mem0's own pages report 92.5 and 91.6 in different places; Zep/Mem0/Letta each report incompatible numbers for one another's systems; one independent audit found the LLM judge accepted 62.81% of deliberately wrong answers | **Treated as contested evidence throughout this package** — the entire LoCoMo memory-benchmark literature is excluded from ranking claims in `15-VALIDATION-BENCHMARK-PLAN.md`; task-completion and citation-accuracy measures are used instead |
| Cognee `forget` failure behaviour | Docs say best-effort cleanup on failure; the v1.6.6rc1 release notes say `forget` now fails if history-purge fails | Unreconciled — treat the release notes (more recent) as the likely current behaviour, unverified |

## 6. Corrections made to EOIP's own capability status during this run

| Item | Before | After | Why |
|---|---|---|---|
| CAP-12 SKOS/taxonomy management | Partial / absent (in an early cohort draft) | **Implemented** | `packages/eoip/ontology/skos.py` (1,417 lines @HEAD) with two passing test files (BL-32 @HEAD); verified by direct code and test inspection, not inferred |
| Egress "embedding" path (`RealSemanticProvider`) | Assumed to be a real (if weak) embedding model | **Confirmed to be a SHA-256 hash simulation**, not a model at all | Found during the GraphRAG/vector-search cohort review; sharpens GAP-46 and the baseline's hashing-embedder-default finding rather than contradicting it |
| `packages/eoip/jobs.py` (DurableJobStore) | Not in the original baseline or its HEAD delta | **Added as a relevant capability**: SQLite-WAL job store with leases, fencing tokens, heartbeats, checkpoints, a transactional outbox and a governed DLQ with `replay_dlq` | Found during the CDC/streaming research batch (V27); the baseline re-audit (B0) had not covered this file |
| `packages/eoip/connectors/sbom.py` + `compliance/sbom.py` | Assumed SBOM support was comparably shallow everywhere | **Clarified**: the connector parses CycloneDX/SPDX components into SourceEvents but never reads dependency/relationship edges, and no OSV/deps.dev/NVD vulnerability matching exists anywhere in the tree | Found during the code-intelligence research batch (V29), cross-checked against Dependency-Track |


