# Cohort 03: Ontology authoring and governance

| Field | Value |
|---|---|
| Cohort ID | COH-03-ONTGOV |
| Workload class | Authoring, review, release and rollback of ontologies, taxonomies and schemas; ontology-as-code (CAP-08..12, 23, 35, 37, 38, 41, 58, 72) |
| Date | 2026-10-26 |
| EOIP reference | BL-32 (ontology-as-code, semantic change records, stewardship), BL-27, BL-29, BL-30 in [01-SYSTEM-BASELINE.md](../01-SYSTEM-BASELINE.md); HEAD `896e06d` status and NB-12 in [01a-BASELINE-DELTA-HEAD.md](../01a-BASELINE-DELTA-HEAD.md) |
| Reference columns | HugeGraph, Neo4j, Neptune (graph stores that hold, but do not govern, the ontology: §2.3) and EOIP @HEAD |
| Members (9) | [Protégé / WebProtégé](../04-COMPETITOR-DEEP-DIVES/C03-protege.md), [TopBraid EDG](../04-COMPETITOR-DEEP-DIVES/C03-topbraid-edg.md), [PoolParty](../04-COMPETITOR-DEEP-DIVES/C03-poolparty.md), [metaphactory](../04-COMPETITOR-DEEP-DIVES/C03-metaphactory.md), [VocBench](../04-COMPETITOR-DEEP-DIVES/C03-vocbench.md), [Timbr](../04-COMPETITOR-DEEP-DIVES/C03-timbr.md), [LinkML](../04-COMPETITOR-DEEP-DIVES/C03-linkml.md), [ROBOT / ODK](../04-COMPETITOR-DEEP-DIVES/C03-robot-odk.md), [Wikibase + Semantic MediaWiki](../04-COMPETITOR-DEEP-DIVES/C03-wikibase.md) |
| Tier C (context) | [C03-tier-c-records-V14](../04-COMPETITOR-DEEP-DIVES/C03-tier-c-records-V14.md): OWL API, Owlready2, OOPS!, Skosmos/Skosify/qSKOS, Widoco, Gra.fo, Ontotext Refine, OntoPortal, OntoUML, KBpedia. ([C03-tier-c-records](../04-COMPETITOR-DEEP-DIVES/C03-tier-c-records.md) has no CLAIM records and is not used) |
| Related | OWL reasoners and pySHACL are in cohort 02 |

CLAIM shorthand: cell suffix uses the column prefix. PR `CLAIM-protege-`, EDG `CLAIM-edg-`, PP `CLAIM-pp-`, MPH `CLAIM-mph-`, VB `CLAIM-vocb-`, TB `CLAIM-timbr-`, LK `CLAIM-linkml-`, RB `CLAIM-robot-`, WK `CLAIM-wiki-`, N4 `CLAIM-neo4j-`. "§n" means a deep-dive section without a CLAIM row.

## 1. Workload class and comparison basis

**Workload.** A tenant needs a controlled ontology: stewards propose changes, a gate rejects unsound ones, approvers release a version, and an operator can roll back. EOIP's answer is ontology GitOps plus stewardship (BL-32) and, at HEAD, a governed pull-request flow, 22 lint rules and a package registry (BL-27, NB-12).

**Why comparable.** All members change a vocabulary, schema or ontology artefact under some review model, or supply a building block for that (LinkML, ROBOT).

**Not like-for-like.**
- Protégé and VocBench are editors with different collaboration models.
- LinkML and ROBOT/ODK are build-time tooling with no UI.
- Timbr is a SQL semantic layer; Wikibase and SMW are wiki-based fact stores. They are kept for patterns, not as governance peers.
- Graph stores (cohort 01) and triple stores (cohort 02) hold ontology artefacts but provide no review workflow.

**Excluded.** Entity resolution and mapping tools (cohort 04). Tier C items are context only: Gra.fo shut down per data.world (CLAIM-grafo not available as CLAIM), Widoco and Skosmos are candidate adjuncts.

## 2. Capability comparison

### 2.1 Authoring and governance platforms

| CAP | Protégé (PR) | TopBraid EDG (EDG) | PoolParty (PP) | metaphactory (MPH) | VocBench 3 (VB) |
|---|---|---|---|---|---|
| CAP-09 ontology modelling | native OWL 2 editing -01 | native forms; OWL reasoning unknown -10 | partial/unknown (Graph Modeler) | native visual editor -03 | native OWL, SKOS-XL, OntoLex -05 |
| CAP-10 SHACL | absent in core -01 | native Core + SPARQL; SHACL 1.2 features in 9.2 -04, -10 | unknown | positioned, depth unverified -02 | partial -04 |
| CAP-12 SKOS/taxonomy | **Implemented** — `ontology/skos.py` (1,417 lines @HEAD): concepts/schemes, broader/narrower/related, polyhierarchy, BCP-47 labels, mappings, deprecation/replacement, SKOS-XL/OntoLex-Lemon profiles, versioned vocabularies with rollback; `tests/unit/test_skos_taxonomy.py` + `tests/semantic/test_skos_governance.py` pass (BL-32 @HEAD) | native -01 | native SKOS-XL -02 | native vocabulary editor -06 | native -05 |
| CAP-35 branch/diff/merge/rollback | absent; Git via VCS, light branch display -08 | partial: working copies, time-travel, partial commit; Git is file sync; no merge model documented -03, -05, -08 | not found: history only, no snapshot or restore -07 | not found: version pages and snapshots, no branch or rollback -04, -05 | partial: time machine and undo; no Git -04 |
| Semantic diff | absent (both apps) | not documented | not found -07 | schema snapshot diff with mapping impact (6.1) -04 | not documented |
| CAP-37 evolution/migration | absent -08 | partial: change history, undo -04 | partial -07 | partial -04 | unknown |
| CAP-41 review/approve/release | partial: WebProtégé comments and issue threads -11 | native workflows, roles, templates -05 | native approval; deletion bypasses approval -07 | editorial states and review comments -05 | native validation workflow -05 |
| CAP-72 co-editing/visual | WebProtégé live shared projects, mechanism undocumented -11 | visual editor new in 9.3, details unverified -02; co-editing unknown | unknown | concurrent editing beta -03 | partial; CRDT not verified |
| CAP-58 AI-assisted | none | MCP (9.3) -02 | LLM taxonomy generation; model hosting undisclosed -03 | proposal-preview-confirm assistant, NL2SPARQL; hosted LLMs named, local unconfirmed -06 | none |
| CAP-45 roles | local / Keycloak (Web) -10 | roles per workflow stage -05 | custom roles (10.1) -03 | database ACL experimental -06 | roles -05 |
| Deployment footprint | Desktop: one JVM; WebProtégé: 14-service Docker stack -10 | one Tomcat WAR + TDB, sizing gated -06, -07 | 16-32 GB across GraphDB, Elasticsearch, Keycloak -05, -06 | Docker/Helm, triple store required -08 | Java/Angular server plus a triple store (§10) |
| Licence | BSD-2-Clause -04 | proprietary; Apache-2.0 SHACL API -10 | proprietary | proprietary subscription | BSD-3 -03 |

### 2.2 Ontology-as-code and adjacent tools

| CAP | LinkML (LK) | ROBOT / ODK (RB) | Timbr (TB) | Wikibase / SMW (WK) |
|---|---|---|---|---|
| CAP-08/09 schema, OWL | native YAML schema; OWL generator -01, -03 | n/a (operates on OWL files) | partial: OWL-DL and some OWL 2 via rewriting -03 | no OWL reasoning (§3) |
| CAP-10 SHACL | SHACL and ShEx generators -03 | absent / unverified | unknown | ShEx, constraints unverified |
| CAP-23 reasoner gate | absent (output to external reasoners) | native: ELK default, HermiT, JFact, Whelk; fails build on incoherence -04 | rewriting inference | absent |
| CAP-35 diff/merge/rollback | absent; Git is the layer | native semantic `diff` (plain, html, markdown); merge via Git -05 | absent: no versioning; Git deployment planned -03 | MediaWiki revision history -01 |
| CAP-37 evolution | partial; no migration tool verified -03 | partial via ODK pipeline -03 | immediate propagation, no control -03 | n/a |
| CAP-41 review/release | absent | partial via PR and CI (ODK release pipeline) -03 | unknown | wiki-level rights only |
| CAP-38 provenance | n/a | n/a | n/a | native ranks, qualifiers, references -01 |
| CAP-58 AI | none | none | NL2SQL; LLM data flow undocumented -03 | none |
| Footprint | pure Python library | Java CLI; large Docker image | 4 CPU/16 GB; MySQL metadata DB mandatory -04 | PHP/MariaDB + search + query service -02 |
| Licence | Apache-2.0 -01 | BSD-3 -01, -03 | proprietary -02 | GPL-2.0-or-later -01 |

### 2.3 Reference columns and EOIP

| CAP | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|
| Ontology storage and enforcement | strict schema only (CLAIM-apache-hugegraph-13); no ontology layer | GRAPH TYPE (enterprise-only, open semantics) -23; n10s Labs for OWL/SHACL import -31 | no constraints beyond ID uniqueness (CLAIM-amazon-neptune-12) | fixed label manifest `ontology/manifest.py`; validation gate checks labels and required properties (BL-28) |
| CAP-35/37 versioning | none | none (offline format migrations only, N4-18) | none | `ontology/gitops.py`: structural diff of manifest snapshots classified additive / potentially_breaking / breaking; branches and PRs held in a dict (`_branches`); semver, rollback with receipts, migration scripts (BL-32, read in `gitops.py`). Status Partial (BL-32) |
| CAP-41 governance | none | none | none | `ontology/governance.py` `GovernedPullRequest`: dual-steward approval, no self-approval, unsatisfiable-class gate, model-authorship gate; PR flow not mounted; package registry mounted (BL-27, NB-12) |
| CAP-10/09 | none | partial via n10s | none | in-house SHACL subset + optional pySHACL; native RDFS-subset reasoner (BL-29, BL-30) |
| CAP-12 SKOS | none | n10s | none | **Implemented**: `ontology/skos.py` (1,417 lines @HEAD) with governance tests passing (BL-32 @HEAD) — corrected from an earlier draft of this row, which read "absent" |
| Lint and docs | none | none | none | 22 lint rules in `lint/rules.py` (docstring: at least 21), scanner, Widoco-style HTML docs route `GET /api/v1/ontology/docs` (BL-32) |
| CAP-72 co-editing | Hubble UI | Browser, Bloom commercial | notebooks | annotations and workspaces, no co-editing (BL-53) |
| CAP-58 AI proposal | text2gremlin (CLAIM-apache-hugegraph-28) | GenAI plugin (N4-19) | none | ontology proposal from JSON with PROPOSED-until-promoted; governance not end to end (BL-27, BL-40) |

## 3. Operational and licensing comparison

| Member | Deployment | Air-gap | Licence class and OEM trigger | Maintenance |
|---|---|---|---|---|
| Protégé | Desktop JVM; WebProtégé 14 services | yes (Web if self-hosted) | BSD-2; low (PR-04) | Desktop 5.6.9 (2026-03-07); 6.0.0-alpha-1 (2026-09-28); WebProtégé release line stale at v4.0.2 (PR-01, PR-02, PR-09) |
| TopBraid EDG | one WAR on Tomcat, Java 21 | viable in principle; egress of AI features unverified | proprietary subscription; cannot be embedded; Apache-2.0 SHACL API reusable (EDG-10) | 9.3 (change log 2026-08) |
| PoolParty | Linux multi-service; Windows dropped | classic stack yes; LLM builder egress unverified | proprietary; OEM unknown | 10.2; Graphwise merger (PP-01) |
| metaphactory | Docker, Helm, Marketplace | AI features need external LLM APIs, not verified offline | proprietary; historical LGPL+Commons Clause (MPH-09) | 6.1 (2026-09-30) |
| VocBench | Java server + store | yes once store is local | BSD-3 (VB-03) | v15.1 (2026-05-07) |
| Timbr | Docker/K8s | LLM flow undocumented | proprietary; pricing unpublished (TB-02) | version not published |
| LinkML | pip | yes | Apache-2.0 | 1.12.1 (2026-10-13); 1.11.0 yanked (LK-02) |
| ROBOT / ODK | CLI, Docker | yes with pinned images | BSD-3; image contents need SBOM | ROBOT 1.9.11 (2026-10-01) (RB-02) |
| Wikibase / SMW | PHP stack | feasible; OAuth tools need hostnames | GPL; trigger | WBS 8.0 (date inferred, WK-05) |

## 4. Performance evidence

None of the nine deep dives holds a comparable figure. Recorded exceptions, none usable for ranking:
- Protégé wiki scalability numbers describe frames-era 3.x and are outdated for OWL (PR-07).
- PoolParty publishes RAM guidance only (8-16 GB / 16-32 GB, PP-06). Timbr gives 4 CPU/16 GB and 8 CPU/32 GB sizing (TB-04). EDG states internal TDB suits "tens of millions" of triples and defers sizing to purchase (EDG-06, EDG-07).
- metaphactory publishes business outcomes, not performance (MPH-02).

EOIP: no ontology-scale or governance-flow benchmark exists. `OntologyGitOpsWorkflow` keeps branches in process memory (`gitops.py`, dict `_branches`), so concurrency and size limits are untested. PROPOSED.

## 5. Findings

1. **Branch, merge and rollback of ontology releases come from Git, not from the authoring tools.** Protégé (PR-08), PoolParty (PP-07), metaphactory (MPH-04) and Timbr (TB-03) document none; EDG offers time-travel and partial commit (EDG-03) but branch switching stays outside the UI (EDG-08). Only ROBOT/ODK and LinkML ride on Git. Falsified by a member documenting release branches with rollback.
2. **EOIP's classified diff goes beyond ROBOT's documented output, but at a different layer.** ROBOT `diff` is a structure-insensitive OWL comparison with report formats (RB-05) and documents no breaking/additive classification. EOIP classifies manifest changes (BL-32), not OWL axioms. Falsified by an EOIP diff over arbitrary OWL files, or by a ROBOT classification feature.
3. **Governance controls in EOIP exist at HEAD, mostly unmounted.** `GovernedPullRequest` implements dual-steward approval, no self-approval, unsatisfiable-class gate and model-authorship gate (BL-27). None of the competitor deep dives document separation-of-duty rules in the sources read. The PR flow is not mounted (01a). So this is a library advantage, not a product one.
4. **EOIP's branch and PR state is in memory.** Competitor INV-edg-01 criticises EDG for governance state locked in a server store; EOIP's `_branches` dict is weaker until persisted (BL-32). Falsified by a persistence layer test.
5. **Collaboration has no verified conflict model.** WebProtégé live editing (PR-11), metaphactory beta (MPH-03), EDG concurrent editing unknown, PoolParty unknown, VocBench unverified. EOIP has none either (BL-53). Falsified by documentation of a merge or CRDT mechanism.
6. **Footprint separates tools into three groups.** Library or CLI (LinkML, ROBOT), one server (EDG, VocBench, metaphactory with a store) and stacks (WebProtégé with 14 services, PoolParty 16-32 GB). Seed claim "EDG is heavy" is not demonstrable: no public sizing (EDG §9).
7. **AI-assisted modelling is proposal-preview-confirm at best, and data flow is unclear.** metaphactory's assistant names hosted models (MPH-06), PoolParty's LLM builder hides hosting (PP-03), Timbr documents no data flow (TB-03). EOIP's egress gateway default S0 and PROPOSED-until-promoted contract (BL-45, BL-40) differ, but ontology proposals are not end to end (BL-27).
8. **SHACL gating of workflows is documented only by EDG.** SHACL bound to workflow stages with severity blocking (EDG-04, STR-edg-02). EOIP's release gates list SHACL regressions in code docstring only; pySHACL is outside the runtime image (BL-29, 01a §0).
9. **Corrected: CAP-12 SKOS is Implemented, not absent.** An earlier draft of this cohort read SKOS management in EOIP as absent (Appendix B rows for CAP-12). `ontology/skos.py` is 1,417 lines @HEAD with `tests/unit/test_skos_taxonomy.py` and `tests/semantic/test_skos_governance.py` both passing (BL-32, 01a) — concepts/schemes, broader/narrower/related, polyhierarchy, BCP-47 labels, mappings, deprecation/replacement, SKOS-XL/OntoLex-Lemon profiles and versioned vocabularies with rollback are all implemented. The tables above and the capability-decision row below are corrected accordingly; this is a real strength, not a gap.
10. **Licensing makes the commercial tools references, not components.** Only Protégé, VocBench, LinkML, ROBOT/ODK (and the Apache-2.0 TopBraid SHACL API) are redistribution-safe; EDG, PoolParty, metaphactory, Timbr are proprietary; Wikibase is GPL.

## 6. Implications for EOIP

| CAP | Parity needed (STR) | Exploitable weakness (INV) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-41 governance workflow | STR-edg-01, STR-edg-02, STR-vocb-01, STR-pp-01 | INV-edg-01, INV-pp-01, INV-mph-01 | BUILD: mount `GovernedPullRequest`, persist state, add configurable stage templates | Operability: governance PR flow not mounted, branch state in memory (BL-27, BL-32) |
| CAP-35 diff/branch/rollback | STR-edg-04 (canonical Turtle round trip), STR-robot-02, STR-edg-06 | INV-protege-02, INV-edg-02 | BUILD persistence and canonical serialisation; EXPERIMENT OWL-level diff via ROBOT in CI | Partial: manifest-level diff only; no OWL-axiom diff |
| CAP-37 evolution/migration | STR-mph-04, STR-robot-01 | INV-linkml-01, INV-timbr-01 | BUILD on gitops and migration protocol (NB-09) | Partial: migrations are a harness, not run on live sources |
| CAP-10 SHACL | STR-edg-02 | INV-edg-01 | REUSE pySHACL; INTEGRATE Apache-2.0 TopBraid SHACL API as an option | Quality: W3C suite not run (U-07) |
| CAP-12 SKOS | STR-pp-01 | INV-pp-02 | REUSE (own) — `skos.py` already implements the lifecycle; adopt PoolParty's deprecated-URI-never-reused rule on top | **Implemented** @HEAD (1,417 lines, tests pass, BL-32) — a differentiator (§2), not a gap |
| CAP-23 reasoner gate | STR-robot-01, STR-owlr-02 (cohort 02) | INV-owlr-01 (cohort 02) | INTEGRATE ELK via ROBOT as a dev-time CI step | Partial: Openllet/HermiT/Jena adapters return canned OK (BL-30) |
| CAP-08/09 ontology-as-code | STR-linkml-01 | INV-linkml-01 | EXPERIMENT: LinkML as an optional input format generating OWL and SHACL | Interoperability: authoring is a Python manifest (BL-32) |
| CAP-58 AI proposals | STR-mph-01, STR-mph-03 | INV-timbr-02, INV-mph-01 | EXPERIMENT: render proposals as semantic diffs for approval | Partial: no end-to-end proposal governance (BL-27) |
| CAP-72 co-editing | STR-protege-03, STR-mph-07 | INV-protege-03 | DEFER; REJECT embedding WebProtégé | UX: entity-level comment threads only |
| CAP-38 provenance | STR-wiki-01 | INV-wiki-01 | BUILD/keep (BL-39, BL-41) | none beyond confirming rank/qualifier shape |

## 7. Open questions

1. Are `GovernedPullRequest` and the lint scanner meant to be mounted, with persistence (U-14)?
2. Does EOIP need OWL-level diff (ROBOT-style) or is manifest-level diff enough for the target tenants?
3. Is WebProtégé's multi-user editing conflict-free, and what is its revert capability (PR-11)?
4. What is TopBraid EDG's real footprint and pricing (EDG-07)?
5. Can metaphactory or PoolParty LLM features run against a local OpenAI-compatible endpoint (MPH-06, PP-03)?
6. Does `ontology/skos.py` pass a SKOS lifecycle and URI-tombstone test as claimed by the deep dives' STR-pp-01 gap?
7. Which stewardship roles must map to tenant-specific templates (EDG-05)?
