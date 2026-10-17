# CRAr_cpccaggcc — Combined Competitive-Research Requirements for EOIP / KnowGridFlow (KGF)

| Field | Value |
|---|---|
| Document | `CRAr_cpccaggcc-requirements.md` — the single canonical requirements specification |
| Companion | `CRAr_cpccaggcc-implementation.md` (how to build and prove it), `CRAr_cpccaggcc-tracker.html` (progress view), `ontology-analysis-dashboard.html` (analysis view) |
| Version | 3.2-COMBINED |
| Date | 2026-10-18 (Asia/Calcutta) for v3.2 and v3.1; v3.0 dated 2026-10-17 |
| Status | Development specification. **Every clause starts OPEN.** Nothing in this document is accepted by the act of writing it. |
| Owner | Vikram (Avyukthi AI); files credited to Ravaleedhar Reddy |
| Baseline revision named by sources | `ccf9e2891070b9b10eb05791ef8cf4cd1ca08731` (must be re-captured by the agent; see CRA-001). HEAD observed when v3.1 was prepared (2026-10-18): `d771fd66ab57d7e860b17f301815fb2421152688` |
| Change in 3.1 | Module M10 (CRA-043..CRA-045), 12 appended `[GN]`/`[PRM]` clauses, gaps G19-G21, conflicts X-34..X-42, decisions H-15..H-17, scenarios E13-E14, CRA-005.8 origin corrected, re-measured repository facts; see section 22 |
| Change in 3.2 | Decisions applied: H-15 accepted (tiered CPU-first numerical stack, delegated), H-16 accepted (CUDA packages not redistributed), H-17 open with an interim CPU-only policy; CRA-043.11, CRA-044.13 and CRA-026.13 added; decision records in `docs/decisions/`; see section 22 |

### Contents

0. How this document was produced · 1. Objective and scope · 2. Completion contract · 3. Agent protocol · 4. Baseline and gaps · 5. Defaults, profiles, quality gates · 6. Canonical contracts · 7. Detailed requirements CRA-001..CRA-042 · 8. Architecture · 9. Connection factory coverage · 10. Multiformat acquisition · 11. API surface · 12. Threat register · 13. Licensing decisions · 14. Benchmarks and QA · 15. Observability and operations · 16. Gates, roadmap, cost · 17. Scenarios and release checklist · 18. Conflicts and human decisions · 19. Traceability · 20. Reproduction probe and fixtures · 21. Source coverage · 22. Change log

## 0. How This Document Was Produced and How to Read It

### 0.1 Source files consumed (every line read)

| # | Source file | Lines / rows | SHA-256 | Nature | Tag |
|---|---|---|---|---|---|
| 1 | `CRAr.md` | 656 lines; 40 requirements, 210 numbered clauses | `71407892dc0c3bec39c0697dd5b908221f6bfbd4ac318f1fef6fa23943dc556d` | Evidence-disciplined execution spec | CRAr |
| 2 | `CRAragg.md` | 941 lines; same 40 IDs | `89adc08dcf5d6b4959beefee24331efeb5b16ff8ef25439eaac145a0fece7cf8` | Aggregated spec: concrete defaults, contracts, connector detail; several over-claims | AGG |
| 3 | `competitive-research-analysis.md` | 1,290 lines | `82199722c8424a74e8163e8f7c70f305da639eb564e2bfdde8e02add29e0061f` | Evidence-labelled research (DOC/LOCAL/PROBE/ND) | CRA |
| 4 | `competitive-research-analysis-agg.md` | 1,993 lines; 55 x 22 master matrix | `b5684435454c3f8acef9878f7bfab5cb4cab97bc85027ffcd704a28e97169b49` | Aggregated dossier; all dimensions scored without sources | AGG |
| 5 | `ontology-competitive-analysis.md` | 803 lines | `5ff2402ecfb0021c126cc5528e9f2a7165c760f112fd9e0ee4941e7f3b9f81bf` | Repository-measured ontology analysis; F1-F5, ONT-001..020, I1-I20 | OCA |
| 6 | `ontology-analysis-dashboard.html` | 636 lines | `1109fa46de1fa836c0cf5d3d8ce78baeaf6a0d5ba1f9a7bebb223dd81d2acba8` | Scorecard/backlog/inversions/gaps view of OCA | OCA |
| 7 | `competitive-research-matrix.csv` | 55 rows x 31 columns | `69965d8f6cb308e94fa963e150573e5a8da078ae0b2adef566bbaadc4bf96162` | Evidence-qualified scores (7 dims scored, 15 ND) | CRA |
| 8 | `ontology-comparison-matrix.csv` | 58 rows x 28 columns | `e4ca9dce070c298bf7450e018579b12e866abaf8e411badbc78efcd72334c4a3` | Indicative scores incl. 3 EOIP rows | OCA |
| 9 | `crarprompt.txt` | 610 lines | `c1e36628113e68929fb4b4600a3fe65fcc674bacd79315cc0d8bf716af215155` | The original attachment (role, rubric, 16 deliverables, eight tool categories, enterprise-source list) and its closing instruction on deterministic semantics plus probabilistic AI; previously consumed through CRAr.md, final instruction now traced explicitly (v3.1) | PRM |
| 10 | `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md` | 1233 lines; 36 requirements GN-001..GN-706 | `d4c5f674844aa7987a0e623f327df46be4878d8662ba8eedb5b3bc879a1413a7` | Neural-fabric engineering spec: tiered numerical stack, anti-stub verification, learned graph models on graphs, meta-graphs, living brain and ontology; repository-measured hash-stub finding (v3.1) Revised v1.1 for decisions H-15..H-17 (v3.2). | GN |
| 11 | `EOIP-engg-doc-pkg/Graph-Neurons-implementation-plan.md` | 454 lines | `a5cc120ce71607576bc14af41b36094e6f834c9b878ed8640fa5b8e2327157e3` | Phases, evidence ledger, prohibitions and risks NR1-NR18 for the neural fabric (v3.1) Revised v1.1 for decisions H-15..H-17 (v3.2). | GN |

### 0.2 Combination rules (binding)

1. **CRAr.md is the base.** Its 40 requirements and 210 numbered clauses are reproduced **verbatim** with their original numbers (`CRA-020.3` means the same obligation in CRAr.md and here).
2. **Additions are appended, never renumbered.** Content from AGG, OCA and CRA that adds a concrete obligation is appended as further numbered clauses after the CRAr clauses, each tagged with its origin (`[AGG]`, `[OCA]`, `[CRA]`, `[RES]`, and from v3.1 `[GN]` for Graph-Neurons and `[PRM]` for the original prompt). `[RES]` marks a reconciliation decision made in this document.
3. **Two new requirements** carry obligations no source requirement owned: **CRA-041** (truthful positioning, claims and disclosure governance — ONT-012, OR6, patent candidates) and **CRA-042** (competitive research qualification and maintenance — ND scores, version pins, license conflicts). Total: **42 requirements**. **v3.1** adds Module M10 with three requirements that no existing requirement owned — **CRA-043** (numerical compute stack), **CRA-044** (learned graph intelligence) and **CRA-045** (deterministic–probabilistic boundary) — plus clauses appended to CRA-001/014/023/025/026/028/035/036/037. Total: **45 requirements**.
4. **Contradictions are never silently merged.** Each is recorded in the conflict register (section 18) with the binding resolution. Where a decision belongs to a human (budget, SLA, legal, product identity) it becomes a decision item `H-xx` and the dependent clauses stay BLOCKED until it is recorded.
5. **Evidence discipline wins over aspiration.** Where AGG/OCA state a capability, score or number without evidence, it is adopted only as a *target*, *default* or *hypothesis*, never as a fact or completion claim.
6. **The ONT-001..ONT-020 backlog, F1-F5 findings, I1-I20 inversions, G01-G18 gaps and INV-01..INV-55 inversions** are all traced to requirement clauses (section 19). Nothing from any source is dropped.

### 0.3 Precedence when two statements conflict

`Normative W3C/IETF standard` > `PROBE/LOCAL evidence (CRA, CRAr)` > `repository-measured facts (OCA)` > `documented vendor facts (DOC)` > `this document's [RES] decisions` > `aggregated targets (AGG)` > `indicative scores`. A later human decision recorded in the ledger (`H-xx`) overrides `[RES]` decisions in its scope. `[GN]` repository-measured facts rank with OCA; `[GN]` design defaults and thresholds rank with AGG targets (adopted as defaults, never as facts). Where Graph-Neurons and this document differ, this document governs (X-34..X-42).

### 0.4 Glossary

| Term | Meaning |
|---|---|
| EOIP / KGF | Enterprise Ontology & Intelligence Platform, also KnowGridFlow — the target application |
| Clause | One numbered obligation `CRA-xxx.n`; the unit of tracking and acceptance |
| Acceptance obligation | `CRA-xxx.A` — the requirement-level acceptance test(s); it can only be accepted after every clause of the requirement |
| Receipt | Machine-readable evidence JSON produced by an actual run (section 2.3) |
| Ledger | `.audit-scratch/ledger.json` — the state of every tracked item and its receipts |
| Profile P0/P1/P2 | Developer / enterprise / scale qualification profiles (section 5) |
| ND | Not determined; never a zero, never averaged |
| LPG | Labeled property graph (EOIP's current native model) |
| CML | Connector Mapping Language (ONT-005) — YAML front-end of the mapping IR |
| GN / PRM | Origin tags (v3.1): Graph-Neurons specification and plan / the original prompt (`crarprompt.txt`) |
| Producer class | Deterministic (exact parsing, validation, reasoning, query, traversal, mapping) or probabilistic (embeddings, LLMs, learned graph models, OCR/ASR/vision, sampled traversal) — CRA-045.1 |
| Dual path | Running the deterministic path beside the probabilistic one and reporting CORROBORATED, DISPUTED or UNCORROBORATED — CRA-045.3 |
| Anti-stub probes | Loss descent, parameter change, label-permutation control and structural coherence — the four checks proving a learned model learned (CRA-044.3) |
| Tier N0-N3 | Optional numerical-stack extras: `numerics`, `neural`, `neural-text`, `neural-research` (CRA-043.1) |

## 1. Objective, Scope and Authority

Develop a commercially distributed, modular enterprise knowledge graph and ontology platform — a **governed, neuro-symbolic "enterprise living brain"** — that:

1. Acquires enterprise information through qualified **push** (webhooks, event streams, CDC) and **pull** (bounded, permission-preserving polling and crawling) adapters for Jira, Confluence/Wiki, Rally, ServiceNow, Snowflake, GitLab, GitHub, qTest, API Portal, Artifactory, Splunk, Slack, Kibana, Fortuna, Grafana, Documentum and any custom system through an extensible **universal connection factory**.
2. Decodes TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX, EML/email, MSG (license-gated), images, scanned documents, audio, video and engineering diagrams into source-located evidence.
3. Maintains linked graph planes: raw resource graph, canonical domain knowledge graph, schema/meta-graph, provenance and derivation graph, lineage graph, policy/security graph, temporal/event graph and vector similarity projections.
4. Unifies **deterministic semantics** (RDF 1.1, JSON-LD 1.1, SPARQL 1.1, OWL 2 profiles, SHACL Core 2017, transactional publication) with **probabilistic AI** (embeddings, hybrid retrieval, GraphRAG, extraction, alignment), keeping proposals separate from facts and entailments.
5. Preserves source permissions, provenance, revisions, deletions and no-egress boundaries across every derivative, and exposes accessible, truthful, governed operational workflows including approved write-back actions.

**Strategic position (OCA verdict, adopted):** become standards-compatible at the boundary while widening the moat in the middle — enterprise source coverage, ontology-as-code lifecycle, multi-format ingestion and agentic grounding. Do **not** build a new native quad store, DL tableau reasoner, Protégé-class editor or VocBench-class thesaurus suite; integrate qualified engines behind ports.

**Deterministic and probabilistic semantics (v3.1).** The original attachment closes with: *"my architecture should be capable enough to handle deterministic semantics (W3C standard ontologies, schema enforcement) and probabilistic AI (vector embeddings, LLM context windows, and graph traversals)."* Item 4 above states the unification; v3.1 assigns owners to the parts no requirement held: **CRA-045** (the boundary, promotion rules and dual-path arbitration), **CRA-026.10-026.12** (LLM context windows), **CRA-043** (the numerical substrate that every probabilistic capability presupposes and the repository does not have) and **CRA-044** (learned models over the graph planes). Graph traversal is deterministic as an exact algorithm and part of the probabilistic pipeline when it assembles LLM context or uses learned or sampled weights; it keeps its exactness label in both uses (CRA-045).

**Compute policy (v3.2, decisions H-15 to H-17).** EOIP distributes CPU-only numerical builds, never redistributes CUDA packages, and qualifies every binding gate on CPU-only hardware. GPU acceleration is optional, customer-provisioned and unqualified until H-17 is decided (CRA-043.2, CRA-043.11; `docs/decisions/`).

**Not authorized by this document:** production crawling, customer-data export, source-system write-back, paid cloud provisioning, publication of claims, open-sourcing, or public disclosure of patent-candidate mechanisms. Each needs environment access, business authorization and the gates in CRA-027, CRA-040 and CRA-041.

The owner delegated design decisions. Defaults chosen here are explicit engineering decisions, not statements about customer environments, budgets, staff, credentials, licenses or contracts. Missing environment-specific inputs must produce actionable configuration/qualification states — never guessed defaults or silent feature substitution. Existing EOIP-owned code remains proprietary (`LicenseRef-EOIP-Proprietary`); third-party components keep their own terms. Both SaaS and customer-installed (including disconnected) profiles matter.

## 2. Mandatory Completion Contract

> **CODE AND TEST-FILE REFERENCES ALONE ARE NEVER PROOF OF COMPLETION.**
> A file, class, route, test name, UI button, registry entry, commit message, requirement ID in a checklist, screenshot or mock returning success proves only that text was written. Only the **execution** of the real implementation, producing a **verifiable receipt** that an **independent reviewer** accepts, completes a clause.

### 2.1 States

`OPEN -> DESIGNED -> IMPLEMENTED -> VERIFIED -> ACCEPTED`, plus `BLOCKED` (dependency, owner and remediation recorded), `FAILED` (attempted acceptance did not pass), `UNQUALIFIED` (implemented locally but a required external qualification — vendor sandbox, license, hardware — is missing), `DEFERRED` and `WAIVED` (visible, never counted as implemented).

| State | Entry condition (all required) |
|---|---|
| DESIGNED | Contract/schema/algorithm written and reviewed; negative cases enumerated; decision records exist for choices |
| IMPLEMENTED | Real production code on the canonical owner path (no mock, stub, feature-flag substitute, hashing fake or demo data); code review record |
| VERIFIED | Positive and negative tests executed against the real backend/profile; receipt produced; zero required skips/xfails/errors/timeouts; source unchanged during run |
| ACCEPTED | Independent reviewer (not the implementer) re-runs or read-backs the evidence, checks every applicable evidence category, signs the receipt; all child clauses ACCEPTED for a parent |

Rules: never close a parent while any child is open, blocked, failed, unqualified or stale. A stale receipt (artifact or source changed) drops the clause back to IMPLEMENTED. No agent may claim 100% completion by counting files, functions, routes, markers, test names, screenshots or registry entries. No agent may reduce scope silently, replace a real provider with hashing/fake output, mark skipped tests passed, or call unavailable behaviour complete. If an external dependency prevents verification, finish safe local work and leave the affected clause BLOCKED or UNQUALIFIED with exact instructions.

### 2.2 Evidence categories per clause

Every ACCEPTED clause needs each applicable category, or a precise reviewed reason why it does not apply: (1) reviewed contract/design; (2) real implementation; (3) positive behaviour; (4) negative/adversarial behaviour; (5) actual integration and persistence; (6) authorization and tenant isolation; (7) failure and recovery; (8) user workflow; (9) performance/profile limits; (10) deployment compatibility (SaaS and installed); (11) independent review.

### 2.3 Receipt schema (union of CRAr and AGG schemas)

Location: `.audit-scratch/receipts/<clause-id>/<run-id>.json`. Do not store secrets, raw restricted documents or unredacted customer prompts in receipts.

```json
{
  "$schema": "https://eoip.enterprise.internal/schemas/verification-receipt-v3.json",
  "receipt_id": "rcpt-<uuid4>",
  "requirement_clause": "CRA-020.3",
  "state_claimed": "VERIFIED",
  "profile": "P1",
  "source_commit": "<40-hex git sha>",
  "source_tree_dirty": false,
  "source_fingerprint": "sha256 of sorted (path, blob-sha) inventory of tracked files",
  "source_unchanged_during_run": true,
  "artifact_digest": "sha256 of the built wheel/image/bundle actually exercised",
  "runtime": {
    "os": "linux-x86_64",
    "python_version": "3.11.x",
    "backend": "configured-real-backend-name",
    "engine": "pySHACL",
    "engine_version": "pinned",
    "config_digest": "sha256"
  },
  "fixture": {"id": "independent-cardinality-corpus", "digest": "sha256", "license": "reviewed"},
  "execution": {
    "command": ["python", "-m", "pytest", "tests/unit/test_shacl_strict.py", "-k", "cardinality"],
    "exit_code": 0,
    "started_at": "2026-10-17T10:00:00Z",
    "completed_at": "2026-10-17T10:00:02Z"
  },
  "results": {"tests_total": 8, "tests_passed": 8, "tests_failed": 0, "tests_skipped": 0, "tests_xfailed": 0, "tests_errors": 0, "duration_ms": 1420},
  "verified_invariants": ["minCount violation rejected with HTTP 422", "zero triples committed on failure"],
  "negative_cases": [{"name": "below-minCount", "expected": 422, "actual": 422, "error_code": "SHACL_CARDINALITY_VIOLATION"}],
  "evidence_files": [{"path": ".audit-scratch/evidence/CRA-020.3/<run-id>/junit.xml", "sha256": "..."}],
  "evidence_categories": {"design": "ref", "implementation": "ref", "positive": "ref", "negative": "ref", "integration": "ref", "authorization": "ref", "failure_recovery": "n/a: reason", "workflow": "ref", "performance": "ref", "deployment": "ref", "review": "pending"},
  "limitations": [],
  "producer": "agent-or-ci-identity",
  "reviewer": null,
  "review_signature": null
}
```

Validity rules (the ledger verifier must enforce all): every `evidence_files` entry exists, parses and matches its hash; `artifact_digest` equals the artifact recorded by the build step of the same run; `source_unchanged_during_run` is computed by comparing fingerprints before and after the run; `tests_skipped + tests_xfailed + tests_errors == 0` for required tests; `completed_at` is after the artifact build time; ACCEPTED requires a non-null `reviewer` different from `producer` and a signature; content-bound dirty-worktree runs are labelled `source_tree_dirty: true` and cannot qualify a release.

### 2.4 Ledger entry

```json
{
  "id": "CRA-020.3",
  "kind": "clause",
  "parent": "CRA-020",
  "state": "OPEN",
  "owner": null,
  "blocked_by": [],
  "receipts": [{"path": ".audit-scratch/receipts/CRA-020.3/run-..json", "sha256": "..."}],
  "notes": "",
  "updated_at": "2026-10-17T00:00:00Z"
}
```

Item kinds: `clause`, `acceptance`, `scenario` (E01-E14), `decision` (H-01..H-17), `research` (R-C01..R-C55), `conflict` (X-01..X-42). The tracker HTML reads and writes this format.

### 2.5 Refusal conditions (release is refused if any is observed)

Fabricated examples presented as live results; invalid data accepted as conformant; unsupported features treated as pass; cross-tenant or cross-ACL leak (including via inference, counts, vectors, events, exports or raw downloads); uncontrolled egress; unbounded parser/plugin execution; unauthorized or replayed action; unqualified durable-store fallback to memory; missing, stale or source-changed receipts; required test skipped; unsigned or tampered release; unresolved required license or regulatory approval; external claim without CRA-041 evidence; learned model promoted without passing its anti-stub probes and baselines (CRA-044); probabilistic output exposed as an asserted fact, or context truncation not disclosed (CRA-045, CRA-026); an `nvidia-*` package in any distributed artifact (H-16); a binding gate met only with a GPU while H-17 is open (CRA-043.11).

## 3. Agent Execution Protocol (summary; full procedure in the implementation document)

1. Read this entire file, the implementation file, and the relevant existing CP/GUI plans (`GUI-UIX-implementation-plan.md`, `GUI-UIX-audit-2026-10-16.md`, `LICENSING.md`) and, for Module M10, `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md` and `Graph-Neurons-implementation-plan.md` before editing. Capture `git status` and `HEAD`; preserve concurrent work. Do not infer completion from earlier audit labels.
2. Enumerate existing composed routes, contracts (`packages/eoip/contracts/`), stores, connectors, validators, model providers, frontend screens and real tests. Identify one canonical owner per capability and extend it before creating anything new.
3. Create the clause-level ledger, dependency map and decision records. Implement Gate A then Gate B foundations, then one complete source -> evidence -> accepted graph -> query -> UI journey (E01) before widening.
4. For each change define inputs/outputs, tenant boundary, persistence, cancellation, compatibility, resource limits and negative cases before writing production code.
5. Add focused tests, run them, then real integration and workflow tests; rebuild and exercise the exact release artifact for release acceptance. Keep mock/component tests labelled separately.
6. Update the ledger and documentation with actual outcomes; explain open dependencies and failures; never change unrelated business behaviour or licensing to make tests green.
7. Re-evaluate the dependency graph after each accepted slice; continue all feasible work; a blocked external item never blocks unrelated implementation.

## 4. EOIP Baseline and Unified Gap Register

### 4.1 Inspected technology (CRA + OCA, to be re-measured under CRA-001)

| Layer | Evidence from sources | Conservative assessment |
|---|---|---|
| API/runtime | `pyproject.toml`: Python >=3.11, FastAPI, Pydantic v2, httpx, Uvicorn, MCP; `platform_router.py` 133+ paths | Reuse; dependency ranges are not locked versions |
| Graph | `packages/eoip/graph/store.py`, `backends.py:189-245`: HugeGraph, Neo4j, Neptune, memory; LPG with manifest-governed labels (`ontology/manifest.py`, 505 LOC) | Reuse the adapter boundary; capability strings are not conformance |
| Ontology | 14 modules ~3,400 LOC: `gitops.py` 793, `rdf.py` 700, `skos.py` 450, `gitops_router.py` 376, `packs.py` 326, `domain_pack_manager.py` 323, `shacl_validator.py` 194, `studio.py` 177, `drift.py` 152, `stewardship.py` 151, `industry_templates.py` 139, `embedding_drift.py` 134, `schema_gen.py` 127 | GitOps, drift and schema-gen are differentiators; RDF I/O, reasoning and SHACL are not standards-grade |
| Acquisition | `connectors/` 38 modules (measured 2026-10-18: 38 `.py` files including `__init__.py` and infrastructure such as base, config, errors, registry and sync; CRA-001.13), `factory.py` 1,135 LOC, 8 application categories; base, registry, webhooks, crawlers | Factory exists; generic REST fallback is not arbitrary-system support |
| Files | `fileparse/` 13 modules incl. `engine.py`, text/office/archive/email/image adapters, budgets | Real paths exist; tool-dependent formats and media qualification partial |
| Retrieval/models | Hashing vector index default; optional Ollama and sentence-transformers; `gnn/engine.py` node2vec/TransE are SHA-256 digests (G19) | Hashing is not semantic embedding or graph learning |
| Numerical stack | None: no numpy, scipy, scikit-learn, torch, torch-geometric or networkx declared or importable (measured 2026-10-18) | Introduce as tiered optional extras (CRA-043), never core |
| Query | `qlang/`: EQL, EOQL, OSQL, JQLite, JSONPath, Lucene, taxonomy DSL; **no SPARQL** | Restricted grammars; names do not prove SPARQL/SQL/Cypher equivalence |
| Cognitive | `brain/`, `intelligence_eng/`, 35 agent types, 14 control loops, 9 reasoning strategies, verification engine, `tools_contract/`, `sdk/`, `authz/`, `token_budget/`, `graph_graph/`, `moonshot/ontology_induction.py` | Existing assets to reuse; capabilities still need receipts before claims |
| Frontend | React/Vite, 90+ components, 146 ARIA attributes, zero i18n; GUI audit partial | Rich UI is not complete journeys |
| Ops/security | Tenancy, policy, jobs, reports, egress, observability (Prometheus/OTel present, alerting absent), WAL exists, no DR drills | Reuse and audit |
| Tests | 239 test files asserted; 302 `test_*.py` measured at `d771fd6` on 2026-10-18 (CRA-001.13); collection 60-120 s; some pre-existing failures | Track, do not delete |
| Licensing | `LicenseRef-EOIP-Proprietary`, `LICENSING.md`; dependency audit pending; `extract-msg` unresolved | Owned code commercial; upstream terms separate |

### 4.2 Gaps and findings (all closed through requirements)

| ID | Finding (source) | Evidence | Closure |
|---|---|---|---|
| F1 | No RDF I/O: no rdflib/pySHACL/owlready2; no Turtle/RDF-XML/N-Triples/OWL-XML parser; external ontologies unimportable (OCA) | dependency grep, zero hits | CRA-016 (ONT-001), CRA-018, CRA-021 |
| F2 | OWL reasoner is a demo: hardcoded axioms, transitive subsumption + 2-step chains (OCA) | `rdf.py:598-700` | CRA-019 (ONT-007/008) |
| F3 | SHACL export is SHACL-shaped, not SHACL (OCA) | `rdf.py:369-425` | CRA-020 (ONT-004) |
| F4 | Strength: ontology GitOps (branch, PR, review, semantic diff, impact, migration scripts, rollback receipts, semver, release packaging) (OCA) | `gitops.py:220-383, 545, 613-733, 733` | Preserve (CRA-022); position only via CRA-041 |
| F5 | Strength: connector reach (38 + factory) and multiformat parsing (OCA) | `connectors/`, `fileparse/` | Qualify (CRA-004..015); position via CRA-041 |
| G01 | `SHACLShape.min_counts/max_counts` declared but not enforced; invalid data gets `conforms=true` (CRA, PROBE) | probe section 20 | CRA-020 |
| G02 | `_check_datatype` returns true for unknown datatype (CRA, PROBE) | probe | CRA-020 |
| G03 | `OWLReasoner.is_subclass_of('urn:example:A','urn:example:a')` true via lowercasing (CRA, PROBE) | probe | CRA-016, CRA-019 |
| G04 | Reasoner bootstraps example axioms, limited chains (CRA, LOCAL) | `rdf.py` | CRA-019 |
| G05 | JSON-LD import handles an EOIP-specific compact form only (CRA, LOCAL) | `rdf.py` | CRA-016, CRA-017 |
| G06 | Backend capability lists overstate executable semantics (CRA, LOCAL) | `backends.py` exports | CRA-001, CRA-024 |
| G07 | Specialization errors caught broadly, fall back to generic REST (CRA, LOCAL) | `factory.py` | CRA-004 |
| G08 | Unknown apps default to `api/entities`; generic Agile profile assumptions (CRA, LOCAL) | `factory.py` | CRA-005..009 |
| G09 | Parser catalog does not establish video or scanned-diagram understanding (CRA, LOCAL) | `fileparse/` | CRA-012..015 |
| G10 | Diagram parser maps unmatched relations to CALLS and vertices to Service (CRA, LOCAL) | diagram parser | CRA-015, CRA-017 |
| G11 | Multimodal `_chunk_text` sets `start=end-overlap` with no end-of-input exit; non-termination suspected (CRA, LOCAL, not executed) | multimodal module | CRA-012, CRA-014 |
| G12 | Default vectors are deterministic hashing (CRA, LOCAL) | vector index | CRA-025, CRA-026 |
| G13 | Limited EOQL grammar; not full SQL/federation (CRA, LOCAL) | `qlang/` | CRA-024 |
| G14 | Stochastic dispatcher random walks/heuristic hop summaries (CRA, LOCAL) | dispatcher | CRA-028 |
| G15 | Many GUI screens, source contracts and tenant lifecycle partial (CRA, historical audit) | GUI audit | CRA-030, CRA-037 |
| G16 | Governance/jobs/recovery modules not qualified (CRA) | — | CRA-003, CRA-031..033, CRA-040 |
| G17 | Component/distribution licensing unresolved (CRA) | `LICENSING.md` | CRA-035 |
| G18 | Target scale, measured workload and staffing not supplied (CRA) | — | CRA-001, CRA-036, H-01, H-10 |
| G19 | `gnn/engine.py` presents node2vec, TransE, link prediction and node classification but computes SHA-256 digests of identifiers and walk strings: no objective, optimiser or learning; structurally identical nodes receive uncorrelated vectors (GN, LOCAL, measured 2026-10-18) | `gnn/engine.py:33-131` | CRA-044, CRA-025.9 |
| G20 | No numerical stack: numpy, scipy, scikit-learn, torch, torch-geometric and networkx are absent from `pyproject.toml` and the environment, although CRA-014, CRA-023.6/023.7, CRA-025 and CRA-026 presuppose one (GN, LOCAL) | import check; `pyproject.toml` | CRA-043 |
| G21 | No requirement owned the deterministic–probabilistic boundary: dual-path arbitration, promotion of probabilistic output, and LLM context-window limits, tokenizer-accurate budgets and truncation disclosure were unspecified (PRM) | `crarprompt.txt` closing instruction; section 1 item 4 | CRA-045, CRA-026.10-026.12 |

## 5. Chosen Defaults, Profiles and Quality Gates

### 5.1 Engineering defaults

| Concern | Binding default | Configurability / validation |
|---|---|---|
| Application structure | Existing Python/FastAPI + React/Vite; modular application with isolated heavy/untrusted workers | Replace providers behind contracts; no blanket rewrite or mandatory microservice split |
| Standards baseline | RDF 1.1, JSON-LD 1.1, SPARQL 1.1, OWL 2 profile-specific, SHACL Core 2017 | New standards (RDF-star, SHACL-AF, SPARQL-star) are named, disabled-by-default profiles with conformance tests |
| RDF library | rdflib >= 7 (pinned) | Alternatives behind the serializer port |
| SHACL | pySHACL in worker; TopBraid SHACL API as differential oracle | Unsupported constraint -> explicit status |
| Reasoning | ELK (EL) default classifier; Jena rules for RL; Openllet/HermiT optional; native subset labelled | Profile mismatch rejected |
| Source data | Source-authoritative ACL and revision; metadata-only discovery first | Broader scopes separately authorized |
| AI | Provider-disabled / no-egress until an approved provider is configured | Explicit provider/model revision |
| Numerical stack | Tiered optional extras N0-N3 (H-15 accepted); CPU-only builds in every distributed artifact (H-16); never a core dependency | GPU optional, customer-provisioned and unqualified until H-17; every binding gate met on CPU (CRA-043.11) |
| Probabilistic output | `proposed` knowledge state; dual path wherever a deterministic path exists | Promotion only through deterministic validation plus review (CRA-045) |
| LLM context window | Limits from the model manifest; budgets measured with the model tokenizer; reduction disclosed | Per model revision (CRA-026.10-026.12) |
| Learned models | Anti-stub probes, five baselines and calibration before promotion | Thresholds change only by recorded review (CRA-044) |
| Publishing | Stage -> validate -> review when required -> publish exact revision | Low-risk auto-publication only via audited rule |
| Query | 30 s online deadline; 4 GiB memory; 10,000 rows/page; depth 3; longer work is a job | Tenant quotas and source limits only lower these |
| Acquisition | 2 concurrent operations per source; 120 req/min unless vendor says less; full-jitter backoff 1-300 s | Vendor limits, Retry-After, budgets |
| Crawling | depth 5, 10,000 pages, 50 MiB/resource, allowlist mandatory | Lower per source |
| Workers | `standard` 2 GiB/2 CPU/30 s; `heavy` 8 GiB/4 CPU/600 s job | Per tenant/class |
| Archives | 2 GiB expanded, depth 3, 10,000 members, 100:1 ratio | Lower only |
| Jobs | Durable queue; heartbeat 10 s; lease TTL 30 s; DLQ | Backend per H-14 |
| Plugins | Disabled/untrusted until signature, contract and permission validation | No main-process execution of untrusted code |
| Storage | Durable canonical/control storage for real deployments | Memory only for named test harnesses; no automatic fallback |
| Write-back | Disabled (read-only) | Enabled per H-03 and CRA-027 |
| Presentation | Existing design system; semantic states; reduced motion; accessible alternatives | Theme/density/locale versioned and scoped |
| Licensing | Proprietary first-party; GPL/AGPL never linked or bundled | Per-artifact SBOM, notices, obligations |

`Fortuna` and `API Portal` have no uniquely identified product contract: keep those adapters UNQUALIFIED until H-06/H-07, while building the generic protocol framework. Customer-specific required inputs (source product/edition/API version, identity and scopes, URLs/network policy, IdP, residence/retention, secret references, enabled plugins/providers, data-license grants, source ACL model) are rejected with field-specific diagnostics when missing.

### 5.2 Qualification profiles (binding gates; stretch objectives recorded separately)

| Metric | P0 developer | P1 enterprise (initial release gate) | P2 scale qualification | Stretch (AGG/OCA, non-binding until H-01) |
|---|---|---|---|---|
| Asserted triples | 1M | 50M | 500M | — |
| Classes / axioms | 1k / 10k | 10k / 75k | 20k / 150k | — |
| Concurrent users | 5 | 100 | 500 | — |
| Source instances | 2 | 20 | 100 | — |
| Reference compute (starting experiment) | 8 vCPU, 32 GiB | 3 x 16 vCPU / 128 GiB data nodes + separate API/workers | 3 x 32 vCPU / 256 GiB + measured API/workers/index | AGG P2: 6 x 32 vCPU / 256 GiB |
| Accelerator (v3.2) | none — CPU only | none — CPU only | none — CPU only | GPU only after H-17 |
| Point read p95 | <= 250 ms | <= 250 ms | <= 500 ms | < 20 ms (P1 and P2) |
| Bounded graph page p95 | <= 750 ms (1-hop) | <= 1 s | <= 2 s | P1 < 150 ms, P2 < 250 ms |
| Approved query suite p95 | — | <= 3 s | <= 10 s | P1 < 1.5 s, P2 < 3 s |
| Accepted-to-searchable p95 | — | <= 60 s | measured | — |
| Ingestion throughput | 5,000 triples/s target | 25,000 triples/s target | 50,000 triples/s target | — |
| Availability objective | none | 99.9% monthly (proposal, not SLA) | measured | AGG 99.99% |
| RPO / RTO | — | <= 15 min / <= 4 h | separate qualification | AGG: 4 h for 500M restore |

Count asserted, inferred, named graphs, raw bytes, vector bytes, replicas, index amplification, retained revisions and hot/cold residency separately. A 500M-triple target does not mean a browser renders 500M nodes; browser scenes are bounded with aggregation/LOD.

### 5.3 Initial quality gates (task manifests; change only by recorded review)

| Task | Gate on approved held-out corpus | Boundary |
|---|---|---|
| Supported structured-diagram and RDF term round trip | 100% fidelity on declared subset; corpus fidelity reported; > 1 pt regression fails CI | Unsupported constructs counted, never omitted |
| Reviewed entity/fact linking | Precision >= 0.99, recall >= 0.80 | High-impact automatic merges disabled; NIL tested |
| Grounded answer clauses | Evidence precision >= 0.98, coverage >= 0.95, unanswerable abstention >= 0.95 | Any unauthorized disclosure fails safety gate |
| Clean printed OCR | CER <= 0.05 per language/document stratum | Handwriting/degraded need separate profiles |
| Clean-speech ASR | WER <= 0.15 per language/acoustic stratum | Noisy/multispeaker separate |
| Visual diagram candidates | Relation precision >= 0.95, recall >= 0.85 | Human review before publication |
| AI-suggested mappings (ONT-006) | >= 70% property maps accepted unedited (Jira, ServiceNow) | Never auto-activated |
| Pitfall lint (ONT-013) | >= 20 antipattern classes with gold fixtures | Error severity blocks merge |
| Learned link prediction / classification (CRA-044) | Primary metric >= common-neighbours + 0.05 and >= rule baseline + 0.05; ECE <= 0.10; label-permutation gap >= 0.10 | AUPRC primary; five baselines; type-constrained negatives |
| Seeded reproducibility (CRA-043) | Same seed in separate processes reproduces metrics within 1e-4 | Non-deterministic kernels listed in the receipt |
| Explanation faithfulness (CRA-044.10) | >= 95% of predictions with evidence paths; removing the evidence subgraph lowers the score >= 50% | Otherwise labelled not faithful |
| Context assembly (CRA-026.10-026.12) | 100% of reduced contexts disclosed; zero mid-assertion cuts; manifest token count equals the model tokenizer count | Restricted evidence filtered before budgeting |

Start with at least 200 independently annotated items per enabled AI task (>= 50 per release-critical stratum), negative/unanswerable/adversarial cases, two-reviewer adjudication and uncertainty intervals.

## 6. Canonical Cross-Module Contracts

Reuse `packages/eoip/contracts/` through compatible extensions; do not create duplicate classes. Never derive trusted scope from connector payloads, LLM output, browser-selected tenant text or raw graph names. Durable identifiers are stable across retries; canonical RDF terms are never lowercased or rewritten by display preferences.

| Contract | Mandatory fields / behaviour |
|---|---|
| TrustedScope | tenant_id, workspace_id, principal_id, principal_type (user, service_account, agent), roles, effective_acls, memberships/grants, policy_epoch, delegation_chain, autonomy_level (agents), expires_at; server-derived only |
| ConnectorManifest / ConnectorDescriptor | provider_id, display_name, version, supported product/API versions, auth schemes/scopes, config JSON Schema, capabilities, limits, license, signature, qualification receipts, derived `is_certified` |
| SourceEvent | event_id (source-scoped), source_instance_id, source_system_type, operation (upsert, delete, acl_update, rename, reconcile), resource_id, resource_revision, observed_at, source_timestamp, content_sha256, acl_vector, acl_revision, raw_payload_ref (`cas://sha256/...`), cursor_watermark, correlation_id, tenant_id (validated, never trusted for routing) |
| ExtractedDocument | raw content hash/reference, MIME + detected format, parser/version/config, sections and EvidenceLocators, parent/attachment chain, warnings/errors/budgets, partial flag, source ACL |
| EvidenceLocator | document_id, source_system, source_revision, page, slide, sheet, cell, paragraph/run index, char_start, char_end, bounding_box [ymin,xmin,ymax,xmax] 0-1, media_timestamp_ms start/end, snippet (policy-limited) |
| RDFTerm | kind (iri, blank_node, literal, triple when rdf-star profile), value (exact lexical form), datatype, language |
| CanonicalAssertion | assertion_id (`urn:eoip:assertion:<uuid>`), graph_iri, subject, predicate, object, knowledge_state (asserted, inferred, proposed, rejected, historical), is_inferred, justification sets (supporting_assertion_ids), evidence, extraction model/revision, confidence (calibrated flag), tenant_id, source_acl_vector, security_classification, policy_epoch, source/ontology/mapping/rule revisions, valid_from/valid_to, tx_from/tx_to |
| OntologyPackage | ontology IRI, version IRI, profile, import closure with checksums, axioms/shapes/mappings, license/attribution, change/reviewer/validation records, release manifest, signature |
| SemanticRun | authorized revision inputs, engine/version/profile, budget, status (OK, VIOLATIONS, INCONSISTENT, UNSUPPORTED, TIMEOUT, CANCELLED, ERROR), unsupported coverage, result/report hash, partial/truncation |
| Publication | expected base revision, mutation digest, validation/approval/policy bindings, idempotency key, durable outcome, outbox sequence |
| QueryResult | dialect/profile/plan, authorized scope, revision/freshness/watermark, pagination/partial state, evidence, actual execution metrics |
| ActionIntent | action_id, action_shape_iri, target_system_id, idempotency_key (16-128), parameters + parameters_sha256, preconditions, source/base/policy revisions, status (PROPOSED, STAGED, APPROVED, EXECUTING, COMPLETED, FAILED, COMPENSATED, UNKNOWN_OUTCOME), requested_by, approved_by, approval timestamp/signature/nonce/expiry, dry_run, read_back query, compensation_action_id, tenant_id |
| CapabilityEntry | capability_id, provider_id, provider_version, profile, state (section CRA-001), last_probe_at, receipt_ref |
| ModelLineage | model_id, model_version, producer_class (deterministic, probabilistic), trained_at, graph_snapshot_id, code_commit, seed_bundle, environment_digest, calibrator_id (nullable), gate_report_ref |
| DualPathResult | question digest, deterministic result or `none_available`, probabilistic result, agreement (CORROBORATED, DISPUTED, UNCORROBORATED), evidence and producer class for each path |
| ContextManifest | model revision, tokenizer, max input/output tokens, ordered evidence entries (assertion_id, locator, tokens), template revision, retrieval parameters, reduction applied, omitted count, digest |

Reference Pydantic v2 skeleton (merge into existing contracts, do not duplicate):

```python
from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

class PrincipalType(str, Enum):
    USER = "user"; SERVICE_ACCOUNT = "service_account"; AGENT = "agent"

class TrustedScope(BaseModel):
    tenant_id: str = Field(min_length=1)
    workspace_id: str = Field(min_length=1)
    principal_id: str = Field(min_length=1)
    principal_type: PrincipalType
    roles: list[str] = Field(default_factory=list)
    effective_acls: list[str] = Field(default_factory=list)
    policy_epoch: int = Field(ge=1)
    delegation_chain: list[str] = Field(default_factory=list)
    autonomy_level: str | None = None
    expires_at: datetime

class SourceOperation(str, Enum):
    UPSERT = "upsert"; DELETE = "delete"; ACL_UPDATE = "acl_update"; RENAME = "rename"; RECONCILE = "reconcile"

class SourceEvent(BaseModel):
    event_id: str
    source_instance_id: str
    source_system_type: str
    operation: SourceOperation
    resource_id: str
    resource_revision: str
    observed_at: datetime
    source_timestamp: datetime | None = None
    content_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    acl_vector: list[str] = Field(default_factory=list)
    acl_revision: str | None = None
    raw_payload_ref: str | None = Field(default=None, pattern=r"^cas://sha256/[0-9a-f]{64}$")
    cursor_watermark: str
    correlation_id: str | None = None
    tenant_id: str

class TermKind(str, Enum):
    IRI = "iri"; BLANK_NODE = "blank_node"; LITERAL = "literal"; TRIPLE = "triple"

class RDFTerm(BaseModel):
    kind: TermKind
    value: str                      # exact lexical form; never case-folded
    datatype: str | None = None
    language: str | None = None

class EvidenceLocator(BaseModel):
    document_id: str
    source_system: str
    source_revision: str
    page_number: int | None = None
    slide_number: int | None = None
    sheet_name: str | None = None
    cell: str | None = None
    paragraph_index: int | None = None
    char_start: int | None = None
    char_end: int | None = None
    bounding_box: list[float] | None = None   # [ymin, xmin, ymax, xmax] in 0..1
    media_start_ms: int | None = None
    media_end_ms: int | None = None

class KnowledgeState(str, Enum):
    ASSERTED = "asserted"; INFERRED = "inferred"; PROPOSED = "proposed"; REJECTED = "rejected"; HISTORICAL = "historical"

class CanonicalAssertion(BaseModel):
    assertion_id: str
    graph_iri: str
    subject: RDFTerm
    predicate: RDFTerm
    object: RDFTerm
    knowledge_state: KnowledgeState
    justifications: list[list[str]] = Field(default_factory=list)   # each inner list = one justification
    evidence: list[EvidenceLocator] = Field(default_factory=list)
    extraction_model: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    confidence_calibrated: bool = False
    tenant_id: str
    source_acl_vector: list[str]
    security_classification: str = "INTERNAL"
    policy_epoch: int
    source_revision: str | None = None
    ontology_revision: str | None = None
    mapping_revision: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    tx_from: datetime = Field(default_factory=_utcnow)
    tx_to: datetime | None = None

class ActionStatus(str, Enum):
    PROPOSED = "proposed"; STAGED = "staged"; APPROVED = "approved"; EXECUTING = "executing"
    COMPLETED = "completed"; FAILED = "failed"; COMPENSATED = "compensated"; UNKNOWN_OUTCOME = "unknown_outcome"

class ActionIntent(BaseModel):
    action_id: str
    action_shape_iri: str
    target_system_id: str
    idempotency_key: str = Field(min_length=16, max_length=128)
    parameters: dict[str, Any]
    parameters_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    base_revisions: dict[str, str]
    status: ActionStatus = ActionStatus.PROPOSED
    requested_by: str
    approved_by: str | None = None
    approval_signature: str | None = None
    approval_nonce: str | None = None
    approval_expires_at: datetime | None = None
    dry_run: bool = False
    read_back_query: str | None = None
    compensation_action_id: str | None = None
    tenant_id: str
```

Note: `datetime.utcnow` (used in CRAragg) is deprecated in Python 3.12+; use timezone-aware `datetime.now(timezone.utc)` as above.

Graph-Neurons `AssertionStatus` and `PredictedEdge` (GN-002) are implemented as a mapping onto `CanonicalAssertion`/`KnowledgeState`, never as a parallel enum (X-34): OBSERVED -> asserted, DERIVED -> inferred, PREDICTED -> proposed, REJECTED -> rejected, CONFIRMED -> asserted with the promotion approver and prior `proposed` state recorded.

## 7. Detailed Requirements

All requirements and clauses start **OPEN**. Existing code paths are investigation/reuse locations only, not proof of acceptance. Dependencies are order constraints, not permission to block independent work. Universal non-evidence (applies to every clause): Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message. Mock, stub, fake, hashing or in-memory substitutes standing in for the real backend/provider. Skipped, xfailed, errored or timed-out required tests; results from a different backend or a stale artifact. Screenshots, markdown ticks, tracker/dashboard state or agent self-assessment without an independently reviewed receipt.

### 7.1 Module M1 — Platform foundations, capabilities and zero-trust security

#### CRA-001. Baseline, Decisions and Acceptance Ledger

*Aggregated title: Truthful Capabilities Registry, Baseline & Audit Ledger*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | none | A (Truthful baseline) | M1 | G06, G18 | — | — | INV-39 | X-04, X-26, X-33 | — |

**Base statement:** Priority P0. Depends on none. Source gaps G06/G18 and all unqualified comparison dimensions. Reuse verification and requirements-registry tooling.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-001.1** `[CRAr]` Inventory the actual runtime composition and all advertised features, including provider/backend/profile, license, deployment and integration status. Separate implemented, configured, exercised and accepted states.
- **CRA-001.2** `[CRAr]` Create decision records for profiles, semantic engines, storage authority, event durability, identity, plugin execution, retention and model policies. State tradeoffs and replacement path. Pin artifact versions/checksums for actual execution; a latest tag is invalid release evidence.
- **CRA-001.3** `[CRAr]` Create one ledger entry per numbered CRA clause, with dependency, owner and required evidence categories. Preserve open historical CP/GUI requirements and link overlaps without claiming this specification replaces them.
- **CRA-001.4** `[CRAr]` Expose capability discovery based on configuration and runtime readiness. Unsupported, unlicensed, unavailable and unqualified are distinct states; a source name or exported string is not a supported capability.
- **CRA-001.5** `[CRAr]` Adopt the selected P0/P1/P2 target profiles as versioned manifests. Record measured outcomes separately. Reject capability declarations not backed by contract tests and appropriate qualification.
- **CRA-001.6** `[AGG]` Implement a runtime `CapabilityRegistry`. Every adapter (graph backends, semantic engines, connectors, parsers, model providers) registers its declared feature matrix at startup and a health probe; the registry stores per capability: capability ID, provider ID, provider version, profile, state, last probe time and qualification receipt reference.
- **CRA-001.7** `[RES]` Capability state is exactly one of `SUPPORTED_QUALIFIED`, `SUPPORTED_UNQUALIFIED`, `DISABLED`, `UNAVAILABLE`, `UNLICENSED`, `UNSUPPORTED`. `SUPPORTED_QUALIFIED` can only be set by the ledger verifier from an ACCEPTED receipt; it can never be authored in configuration.
- **CRA-001.8** `[AGG]` A request needing a capability that is not usable returns a structured error and never an empty success: unsupported construct in a valid request -> HTTP 422 `UNSUPPORTED_CAPABILITY` naming `unsupported_construct`; configured but down -> HTTP 503 `CAPABILITY_UNAVAILABLE`; not entitled -> HTTP 403 `CAPABILITY_NOT_ENTITLED`; disabled by configuration -> HTTP 409 `CAPABILITY_DISABLED`.
- **CRA-001.9** `[RES]` Ledger location: `.audit-scratch/ledger.json`; receipts: `.audit-scratch/receipts/<clause-id>/<run-id>.json` (one directory per clause so repeated runs are retained). The ledger references each receipt by SHA-256. The CRAragg single-file path `.audit-scratch/receipts/{clause_id}.json` is accepted as a read-only legacy alias only.
- **CRA-001.10** `[RES]` The ledger covers every clause `CRA-xxx.n` of CRA-001..CRA-042, every acceptance obligation `CRA-xxx.A`, end-to-end scenarios E01-E12, human decisions H-01..H-14 and research records R-C01..R-C55. (v3.1: CRA-001..CRA-045, E01-E14, H-01..H-17, X-01..X-42.) The tracker HTML (`CRAr_cpccaggcc-tracker.html`) imports and exports this exact schema; the tracker is a view and is never evidence.
- **CRA-001.11** `[OCA]` Re-measure, at the pinned baseline commit, the repository facts asserted by the source analyses and record measured value versus asserted value: Python requirement (pyproject `>=3.11` vs asserted 3.12+), 587 `.py` files under `packages/`, 133+ API paths, 38 connector modules, `connectors/factory.py` 1,135 LOC with 8 application categories, `ontology/` 14 modules ~3,400 LOC, 13 `fileparse/` modules, 239 test files, 90+ React components, 146 ARIA attributes, zero i18n. Discrepancies are recorded, never silently corrected.
- **CRA-001.12** `[CRA]` Run the G01-G03 reproduction probe (combined requirements section 19) at baseline and store its raw output as the baseline defect receipt; later remediation receipts must reference it.
- **CRA-001.13** `[GN]` Record the facts re-measured at `d771fd66ab57d7e860b17f301815fb2421152688` on 2026-10-18 beside the asserted values (CRA-001.11): 302 `test_*.py` files (asserted 239); 38 `.py` files in `connectors/` including `__init__.py` and infrastructure modules (base, config, errors, registry, conflicts, drift, reconciliation, sync), so '38 connector modules' overstates the connector count; no numerical library declared or importable (G20); hash-based embeddings in `gnn/engine.py` (G19); demo axioms still in `ontology/rdf.py` (G04). These feed the CRA-001.11 facts file; they do not correct the sources.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| ledger path | .audit-scratch/ledger.json | RES |
| receipt path | .audit-scratch/receipts/<clause-id>/<run-id>.json | RES |
| capability probe interval | 60 s (configurable) | RES |

**Acceptance obligation CRA-001.A** (only after every clause above is ACCEPTED):

- `[CRAr]` inspect an actual instance where a provider is disabled, unavailable and healthy; the UI/API must accurately distinguish all three. Corrupt a receipt or change source during verification and demonstrate that acceptance is rejected. Ledger coverage must reconcile all 40 requirements and their children without treating coverage as completion.
- `[MERGED]` Ledger verifier rejects, with distinct reason codes, fixture ledgers containing: an ACCEPTED clause with no receipt; a receipt whose artifact digest does not match; a receipt whose `source_unchanged_during_run` is false; a receipt with `tests_skipped > 0` for a required test; a receipt older than the referenced artifact.
- `[MERGED]` `GET /api/v1/capabilities` (or the existing equivalent route) returns all six states for a fixture configuration and the UI renders each distinctly.
- `[GN]` The facts file reproduces the five CRA-001.13 values from commands stored with the receipt.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A capability string list or `owl_supported=true` flag in code.
- The ledger file existing or the tracker showing ACCEPTED.
- A markdown checklist with ticks.

#### CRA-002. Modularity and Safe Plugin Runtime

*Aggregated title: Sandboxed Micro-Worker Runtime & Resource Fencing*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001 | B (Safe platform) | M1 | G11 | ONT-003 | — | INV-05, INV-08, INV-10, INV-21, INV-23, INV-29, INV-30, INV-34, INV-35, INV-41, INV-44, INV-45, INV-47, INV-48, INV-55 | X-27 | — |

**Base statement:** Priority P0. Depends on CRA-001. Sources INV-05/08/10/21/23/29/39/44/45/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-002.1** `[CRAr]` Define versioned interfaces for connector, parser, mapper, graph store, semantic engine, search/vector index, model provider, workflow/action and UI contribution. Declare compatibility ranges and capability negotiation.
- **CRA-002.2** `[CRAr]` Keep heavy parsers, JVM reasoners, native codecs, model/GPU work and untrusted extensions outside the request process. Enforce CPU/memory/time/output/file/network budgets and terminate safely.
- **CRA-002.3** `[CRAr]` Require signed plugin manifests, publisher identity, digest, dependency inventory, permissions, configuration schema and migration/uninstall behavior. Verify signatures/digests before activation and after retrieval.
- **CRA-002.4** `[CRAr]` Provide declarative configuration for ordinary customization. A configuration field must not become arbitrary import/eval/shell execution. Custom code uses a separately authorized isolated execution path.
- **CRA-002.5** `[CRAr]` Persist plugin state through owned repositories, scope it by tenant/workspace and version schema migrations. Disable/uninstall must revoke permissions, stop jobs and preserve or safely migrate owned data.
- **CRA-002.6** `[CRAr]` Qualify replacement of one engine/plugin without altering domain APIs or corrupting canonical state. Separate licensing entitlements from authorization; neither grants the other's privileges.
- **CRA-002.7** `[AGG]` Default worker resource classes: `standard` <= 2 GiB RSS, <= 2 CPU, 30 s wall clock per item; `heavy` (OCR, ASR, JVM reasoners, large office conversion) <= 8 GiB, <= 4 CPU, 600 s, always executed as a durable job. Limits are configurable per class and per tenant; the lower of tenant and class limit wins.
- **CRA-002.8** `[AGG]` On any limit breach the orchestrator terminates the whole worker process tree within 1 s of detection, releases leases, file descriptors and temp directories, records outcome `TIMEOUT`, `OOM` or `LIMIT_EXCEEDED`, returns HTTP 504 for synchronous calls or marks the job FAILED with the reason, and respawns a healthy worker. The API process keeps serving.
- **CRA-002.9** `[AGG]` Semantic micro-worker protocol (INV-55): JVM engines (OWL API, ELK, optional HermiT/Openllet, ROBOT, optional Jena/TopBraid SHACL) run only behind a versioned worker contract (gRPC or stdio JSON-RPC) carrying request ID, deadline, input artifact hashes, engine name/version/profile and resource class. No JVM runs inside the API process.
- **CRA-002.10** `[OCA]` Graph backend ports: existing adapters (in-memory, HugeGraph, Neo4j, Neptune in `packages/eoip/graph/backends.py`) and a new RDF-store port (Apache Jena Fuseki as reference implementation, GraphDB as certified commercial option per ONT-003) declare capabilities through the same negotiation. GPL/AGPL servers (Neo4j Community, Virtuoso OSE) are reachable only over their network protocol and are never linked, vendored or bundled.
- **CRA-002.11** `[OCA]` Preserve existing conventions: Pydantic request models at module level (required for FastAPI OpenAPI schema resolution), thread-safe singleton accessors, and a `stats()` method on every engine wired into `brain_os.py` telemetry.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| standard worker | 2 GiB / 2 CPU / 30 s | AGG |
| heavy worker | 8 GiB / 4 CPU / 600 s, durable job | RES |
| kill latency | <= 1 s after breach detection | AGG |

**Acceptance obligation CRA-002.A** (only after every clause above is ACCEPTED):

- `[CRAr]` run a benign plugin then malicious timeout/memory/network/path-escape cases. Reject a modified signature and incompatible contract. Crash/restart a worker, disable its plugin while work is pending and verify no orphan side effects or leaked tenant state. No plugin marketplace listing alone qualifies execution safety.
- `[MERGED]` Run fork-bomb, memory-balloon, infinite-loop, outbound-network and `../../etc/passwd` path-escape plugins inside a worker. Each is killed or denied; API `/health` p95 stays within 20% of baseline during the attack; respawn counter increments; no orphan temp files or processes remain (verified by process table and temp-dir listing).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A `timeout=` argument in code or a container `mem_limit` that was never exercised under attack.

#### CRA-003. Identity, Scope and Derived-Data Authorization

*Aggregated title: Zero-Trust Principal, Tenancy & Derivation ACL Authorization*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/002 | B (Safe platform) | M1 | G15, G16 | — | — | INV-05, INV-19, INV-20, INV-23, INV-24, INV-39, INV-43 | X-11 | — |

**Base statement:** Priority P0. Depends on CRA-001/002. Source G15/G16 and INV-19/20/24/39/43.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-003.1** `[CRAr]` Implement trusted principal/session/IdP integration, memberships and tenant/workspace grants, preserving existing approved authentication contracts. Distinguish deployment-token access from a production user session.
- **CRA-003.2** `[CRAr]` Enforce deny-by-default authorization at every canonical read/write, traversal, count, search/vector candidate, semantic job, event, report/export, raw download, administration and action boundary.
- **CRA-003.3** `[CRAr]` Compose source ACLs and classifications on every derivative. Derived facts and evidence cannot be visible merely because their final subject is visible. Support alternate permitted proofs explicitly; never reveal a restricted proof.
- **CRA-003.4** `[CRAr]` Bind caches, drafts, saved views, cursors and local state to authorized scope and policy epoch. Scope switching/disconnect aborts pending work and discards late results. Migrate ambiguous legacy browser data without inferring ownership.
- **CRA-003.5** `[CRAr]` Propagate revocation/ACL changes through every index, cache, inference, job and stream; deny unsafe stale access while projections lag. Reauthorize long-running downloads/jobs/actions before sensitive delivery/commit.
- **CRA-003.6** `[CRAr]` Test same-backend tenants with identical external IDs, malicious tenant fields, unauthorized graph names and cross-workspace membership changes. Audit defaults such as global/system scopes; do not assume names exempt isolation safely.
- **CRA-003.7** `[AGG]` `TrustedScope` (fields in section 6) is derived only server-side from a validated session, JWT or mTLS identity. Tenant, workspace, roles and ACLs in request bodies, connector payloads, LLM output or browser state are ignored for authorization.
- **CRA-003.8** `[RES]` Derived-fact visibility rule (resolves X-11): for one justification, a derived fact is visible only if the principal satisfies the ACL of every premise (intersection). With several justifications it is visible if at least one complete justification is fully visible. Explanations show only a fully visible justification. Classification is the maximum classification of the justification used.
- **CRA-003.9** `[AGG]` Each tenant has a monotonically increasing `policy_epoch`, incremented on any ACL, membership, classification or policy change. Caches, cursors, vector results, inferred facts and query results carry the epoch they were computed under; reads under a newer epoch must re-filter or deny. Serving a stale-epoch result without re-check is prohibited.
- **CRA-003.10** `[AGG]` Scope filters are injected into the typed query plan before execution for SPARQL, SQL, Cypher, EOQL/EQL/OSQL and vector search. User-supplied `GRAPH`/`FROM`/named-graph or index selection outside the caller's scope is rejected.
- **CRA-003.11** `[RES]` Probing another tenant's identifier returns a response indistinguishable from a non-existent resource (HTTP 404 with the same body shape and timing class), so existence is not leaked.
- **CRA-003.12** `[OCA]` TriG/N-Quads exports preserve tenant graph IRIs (`urn:eoip:tenant:{id}`) and never merge tenants; covered by a contract test.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| policy epoch scope | per tenant | AGG |

**Acceptance obligation CRA-003.A** (only after every clause above is ACCEPTED):

- `[CRAr]` two real principals/tenants exercise every boundary, including hidden intermediate nodes, aggregate counts, inferred links, vector neighbors and raw artifacts. Revoke source access during a job and active UI session; previously visible data must not reappear through late results or exports. Review actual persistence/cache/event backends, not one in-memory store.
- `[MERGED]` Tenant A cannot read Tenant B data even when guessing internal URIs (AGG).
- `[MERGED]` User X, permitted premise A and denied premise B, cannot see inferred fact C derived only from A and B, in API, search counts, vector neighbors, exports or answers; after adding an alternate fully permitted justification, C becomes visible with only that justification explained.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A middleware file named `authz.py`; tests run only against the in-memory store.

### 7.2 Module M2 — Universal connection factory and enterprise adapters

#### CRA-004. Connection Factory and Conformance SDK

*Aggregated title: Universal Connection Factory & Conformance SDK*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | C (First acquisition slice) | M2 | F5, G07, G08 | ONT-005 | I6, I8 | INV-42, INV-43 | X-12 | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Source G07/G08 and INV-27/31/42/43/45. Investigate existing `connectors/factory.py`, base, registry and source contracts.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-004.1** `[CRAr]` Extend the existing factory with explicit per-capability descriptors: discover, baseline, poll, webhook, CDC, ACL, deletion, attachment, lineage, write-back, resume and health. State supported resource and API versions.
- **CRA-004.2** `[CRAr]` Validate configuration/secret references before instantiation. Do not swallow specialization failures and silently switch to a generic endpoint. Fallback requires an explicit configured policy and visible capability downgrade.
- **CRA-004.3** `[CRAr]` Provide generic protocol adapters for REST/OpenAPI, GraphQL, SOAP, JDBC/ODBC, SFTP/files/object storage and event/CDC sources through isolated qualified drivers. Unsupported protocols return actionable unavailable states.
- **CRA-004.4** `[CRAr]` Implement conformance fixtures and a sandbox runner covering auth, pagination, rate limits, retry, rename/delete, ACL change, ordering, duplicate events, cursor durability, attachment and resource budgets.
- **CRA-004.5** `[CRAr]` Store provider version/config digest and qualification receipts with each source instance. Successful connection/authentication is not baseline sync certification, and sync is not write-back approval.
- **CRA-004.6** `[CRAr]` Provide authoring templates, contract validation and mock fixtures for a new custom source, followed by separate real-system qualification. Unknown business products must not be advertised as fully supported via `api/entities` defaults.
- **CRA-004.7** `[AGG]` `ConnectorDescriptor` fields: `provider_id`, `display_name`, `version`, `supported_product_versions`, `capabilities` (discovery, baseline_sync, polling_sync, webhook_push, cdc_stream, acl_preservation, attachments, delete, lineage, write_back, resumable_cursor, health), `auth_schemes` (oauth2, bearer, basic, mtls, app_installation), `config_schema` (JSON Schema), `default_concurrency_limit` (2), `rate_limit_per_minute` (120 unless vendor headers say less), and a derived read-only `is_certified` computed from receipts.
- **CRA-004.8** `[AGG]` Per-source-instance token-bucket rate limiter honouring `Retry-After` and vendor rate-limit headers; HTTP 429/503 trigger exponential backoff with full jitter (base 1 s, cap 300 s) without exceeding the configured budget.
- **CRA-004.9** `[AGG]` SDK: abstract `BaseConnector` with `discover()`, `baseline(cursor)`, `poll(cursor)`, `handle_webhook(event)`, `fetch_acl(resource)`, `fetch_attachment(ref)`, `write(intent)` (only when write_back is declared) and `health()`. Third-party connectors are discovered through the Python entry-point group `eoip.connectors` and must carry a signed manifest (CRA-002).
- **CRA-004.10** `[OCA]` Inventory all 38 existing connector modules and `connectors/factory.py` (8 application categories) into a connector qualification table (provider, versions, capability states, mapping location, receipts). Extend these; do not create a parallel factory.
- **CRA-004.11** `[CRA]` G07 closure: remove the broad exception handler that converts specialization errors into a generic REST fallback. Fallback happens only when `fallback_policy: explicit` is configured, and then the capability downgrade is surfaced in API, UI and telemetry.
- **CRA-004.12** `[OCA]` Payload-to-ontology mapping for every connector is expressed in the declarative mapping language of CRA-017 (CML), not hard-coded in connector bodies; a new source is onboarded by configuration plus a mapping file, with Python only for genuinely new protocols (I8).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| concurrency per source | 2 | CRAr |
| rate limit default | 120 requests/min, lowered by vendor headers | AGG |
| backoff | full jitter, base 1 s, cap 300 s | RES |

**Acceptance obligation CRA-004.A** (only after every clause above is ACCEPTED):

- `[CRAr]` add a synthetic custom provider without core changes, then a real permitted vendor adapter. Demonstrate invalid credential, incompatible version, unsupported capability and specialization error with no fabricated fallback data. Resume after worker restart without duplicates or skipped resources.
- `[MERGED]` Invalid credential surfaces `CONNECTOR_AUTH_FAILED`; incompatible version surfaces `CONNECTOR_VERSION_UNSUPPORTED`; undeclared capability surfaces `UNSUPPORTED_CAPABILITY`; a specialization exception surfaces `CONNECTOR_SPECIALIZATION_FAILED`; in none of these cases is fallback data produced.
- `[MERGED]` A connector installed only via an entry point loads, passes the conformance runner against fixtures, and executes a dry-run sync.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A registry entry with a product name; a successful authentication test (that is not baseline-sync certification).

#### CRA-005. Work-Tracking and Test-System Adapters

*Aggregated title: Issue Tracking & Agile Connectors (Jira & Rally)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011 | G (Named sources, media and actions) | M2 | G08 | ONT-005 | — | — | X-12 | H-11 |

**Base statement:** Priority P1. Depends on CRA-004/010/011. Sources Jira, Rally and qTest; source requirement attachment line 123.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-005.1** `[CRAr]` Qualify Jira Cloud and separately selected Data Center versions for projects, issues, links, comments, custom fields and attachments. Retrieve permission context with authorized scopes and preserve issue/source revision identity.
- **CRA-005.2** `[CRAr]` Qualify Rally workspace/project resource types and hierarchy. Preserve artifact relationships and version/cursor semantics; configuration must select actual API version and resource scope.
- **CRA-005.3** `[CRAr]` Qualify qTest projects, tests, runs/results and defect associations. Distinguish test definitions from execution results and preserve updates/deletes and project authorization.
- **CRA-005.4** `[CRAr]` Research the official API/version/auth/scopes and acquire licensed test access for each product. Store a compatibility manifest and vendor-response fixtures with secrets removed.
- **CRA-005.5** `[CRAr]` Demonstrate bounded baseline and incremental acquisition, pagination, rate limits, ACL-only change, deleted/renamed items, attachments and replay. A generic Agile profile cannot substitute for actual vendor semantics.
- **CRA-005.6** `[AGG]` Jira: Cloud REST API v3 and a separately pinned Data Center REST version; webhooks for issue created/updated/deleted and comment events; incremental JQL `updated >= watermark` with an overlap window (default 5 min) and deduplication by issue ID plus updated timestamp. Map Issue, Project, Sprint, Component, Version, Worklog, User and issue links (blocks, is blocked by, relates to, duplicates, clones) to a reviewed `jira:` vocabulary package; issue security levels and project permission schemes populate `acl_vector`; attachments go to the raw vault.
- **CRA-005.7** `[AGG]` Rally: WSAPI v2.0; HierarchicalRequirement, Defect, Task, Iteration, Release, Milestone and PortfolioItem types; preserve parent/child epic hierarchies, defect associations and workspace/project scope.
- **CRA-005.8** `[AGG]` qTest: projects, test cases, test runs, executions/results and defect links; `qtest:verifiesRequirement` links to Jira issues only when the identifier resolves to an ingested Jira resource; definitions and executions remain distinct entity types.
- **CRA-005.9** `[OCA]` All three adapters express payload-to-ontology mapping in CML (CRA-017), with a parity test proving the CML output equals the previous hand-coded mapping output on a fixture corpus.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| Jira overlap window | 5 min | RES |

**Acceptance obligation CRA-005.A** (only after every clause above is ACCEPTED):

- `[CRAr]` one live/sandbox end-to-end journey per product and selected edition, followed by restart/replay and access revocation. If a sandbox is unavailable, contract code and mock tests may be IMPLEMENTED, but that product's integration clauses remain BLOCKED/UNQUALIFIED.
- `[MERGED]` Incremental sync retrieves only issues updated after the watermark; overlap duplicates are removed; a security-level-only change propagates as an ACL_UPDATE event without a content change (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Generic Agile profile output labelled as Jira or Rally support.

#### CRA-006. Wiki, Content, Chat and Document Repositories

*Aggregated title: Knowledge & Content Repository Connectors (Confluence, Wiki, Slack & Documentum)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011/012/013 | G (Named sources, media and actions) | M2 | G08 | — | — | — | X-12 | H-11, H-13 |

**Base statement:** Priority P1. Depends on CRA-004/010/011/012/013. Sources wiki, Confluence, Slack and Documentum.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-006.1** `[CRAr]` Provide generic wiki acquisition plus Confluence-specific spaces, pages, versions, links, comments and attachments with inherited/restricted-page permissions and body/macro fidelity diagnostics.
- **CRA-006.2** `[CRAr]` Qualify Slack through approved application scopes/events/history APIs. Preserve conversation membership, message/file edits/deletes, threads, pagination and rate limits. Private/direct messages are excluded by default unless explicitly authorized and legally permitted.
- **CRA-006.3** `[CRAr]` Qualify Documentum's licensed selected API for object IDs, versions/renditions, folders, relationships, ACL inheritance, checkout and retention/legal holds. Do not reduce document identity to filename or URL.
- **CRA-006.4** `[CRAr]` Preserve message/document part and attachment provenance through nested parsing. Redact restricted content before indexing or invoking external providers. Synchronize permissions independently of content changes.
- **CRA-006.5** `[CRAr]` Display unsupported macros/renditions, inaccessible content and partial crawl honestly; do not fabricate plain-text equivalents or claim all wiki products share a single API.
- **CRA-006.6** `[AGG]` Confluence and generic wiki: CQL plus REST for Space, Page, BlogPost, Comment, Attachment and Version; page tree (`wiki:childOf`), links and mentions; space permissions and page-level view/edit restrictions populate `acl_vector`; embedded attachments and macros go to multiformat decoding with fidelity diagnostics.
- **CRA-006.7** `[AGG]` Documentum: Documentum REST Services and CMIS at pinned licensed versions; Cabinet, Folder, sysobject, rendition and version chain; Documentum ACLs, domain groups, folder inheritance, retention and legal-hold flags.
- **CRA-006.8** `[AGG]` Slack: Events API (`message.channels`, edits, deletes, `file_shared`) plus `conversations.history`/`replies`; private channels and direct messages are blocked by default and can be enabled only with configuration plus a recorded legal/compliance approval reference; entity mentions are linked through CRA-023 as proposals.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| Slack private/DM ingestion | disabled | CRAr |

**Acceptance obligation CRA-006.A** (only after every clause above is ACCEPTED):

- `[CRAr]` restricted page/channel/document cannot appear through raw downloads, graph neighbors, counts or answers. Modify/delete/rename a source and change its ACL; verify all derivatives and historical access rules after restart.
- `[MERGED]` A restricted Confluence page is absent from search, graph, counts and answers for an unauthorized user (AGG). Enabling Slack private-channel ingestion without an approval reference is refused.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Ingesting a public page via the generic crawler and calling it Confluence support.

#### CRA-007. Code, Build, Artifact and API-Portal Adapters

*Aggregated title: Code, Pipeline & Artifact Connectors (GitHub, GitLab, Artifactory & API Portal)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011 | G (Named sources, media and actions) | M2 | G08 | — | — | — | X-12, X-13 | H-07, H-11 |

**Base statement:** Priority P1. Depends on CRA-004/010/011. Sources GitHub, GitLab, Artifactory and API Portal.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-007.1** `[CRAr]` Qualify GitHub/GitLab selected editions for repository/project identity, commits/branches, pull/merge requests, issues, CI metadata and permitted artifacts. Preserve immutable commit references and moving-branch observations separately.
- **CRA-007.2** `[CRAr]` Support source-native app/project/repository authorization, installation scope, signed webhook verification, cursor/rate-limit behavior and rename/delete/fork semantics.
- **CRA-007.3** `[CRAr]` Qualify Artifactory repository/build/artifact metadata, checksum identity and authorized content, including promotion/deletion and repository ACLs. Never extract/store credentials from build metadata.
- **CRA-007.4** `[CRAr]` Treat API Portal as a configurable provider family until its product/API is identified. Support governed OpenAPI/schema/documentation ingestion, API/version relationships and approved discovery without pretending a universal portal endpoint exists.
- **CRA-007.5** `[CRAr]` Integrate code/document/schema parsing with provenance to commit/artifact/version and explicit language/format capability. Reject unsupported binaries and untrusted executable content.
- **CRA-007.6** `[AGG]` GitHub (REST plus GraphQL API v4) and GitLab (REST v4/GraphQL): Repository, Branch, Commit, Pull/Merge Request, Issue, Workflow/Pipeline run, Release; relations `git:modifiesFile`, `git:authoredBy`, `git:mergesInto`, `git:referencesIssue`; repository visibility (public/internal/private) populates `acl_vector`.
- **CRA-007.7** `[AGG]` Cross-system issue references: extract issue keys from commit messages/PR titles with a configurable pattern (default `\b[A-Z][A-Z0-9_]+-\d+\b`) restricted to an allowlist of project keys; each match becomes a proposed link with an evidence locator (message span) and is asserted only when the key resolves to an ingested issue.
- **CRA-007.8** `[AGG]` Artifactory: AQL plus storage webhooks; Repository, Artifact, Docker image/manifest, BuildInfo; `art:builtFromCommit` from build-info VCS revision; artifact identity by SHA-256 checksum.
- **CRA-007.9** `[RES]` API Portal: candidate provider profiles Kong, Apigee, SwaggerHub and a generic OpenAPI 3.0/3.1 crawler. The adapter remains UNQUALIFIED until the actual product is identified (decision H-07); `api:Service`, `api:Endpoint`, `api:Operation`, `api:SchemaModel` are the proposed vocabulary.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| issue key pattern | \b[A-Z][A-Z0-9_]+-\d+\b + project allowlist | AGG |

**Acceptance obligation CRA-007.A** (only after every clause above is ACCEPTED):

- `[CRAr]` show a source change linked to an API/artifact/business entity with exact revision evidence. Revoke private-repository access and prove it disappears from retrieval and exports. Verify signed webhook replay protection and real vendor sandbox data, not only local JSON fixtures.
- `[MERGED]` Multi-hop query from an Artifactory binary to its Git commit to the Jira ticket returns exact revision evidence for every hop (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Local JSON fixtures only, without a vendor sandbox run.

#### CRA-008. Observability and Operational-System Adapters

*Aggregated title: ITSM, Operational & Monitoring Connectors (ServiceNow, Splunk, Kibana & Grafana)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011/040 | G (Named sources, media and actions) | M2 | G08 | — | — | — | X-12 | H-11 |

**Base statement:** Priority P1. Depends on CRA-004/010/011/040. Sources ServiceNow, Splunk, Kibana and Grafana.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-008.1** `[CRAr]` Qualify ServiceNow table/CMDB/incident/change/knowledge profiles with actual row/field ACLs and domain separation. Avoid broad table-service-account rights in default profiles.
- **CRA-008.2** `[CRAr]` Qualify Splunk searches/knowledge objects and permitted event metadata under query/time/result budgets. Sensitive log content is separately authorized; credentials and PII must not enter normal graph labels or telemetry.
- **CRA-008.3** `[CRAr]` Qualify Kibana saved objects/spaces separately from Elasticsearch/OpenSearch data authority. An authenticated dashboard connection does not authorize every backing index.
- **CRA-008.4** `[CRAr]` Qualify Grafana organizations/folders/dashboards and authorized data-source metadata/query results. Never retrieve or expose stored data-source secrets as ordinary metadata.
- **CRA-008.5** `[CRAr]` Keep observed telemetry separate from inferred incident causality. Preserve timestamps, source sampling, staleness, missing data and uncertainty. Any write-back/provisioning uses CRA-027.
- **CRA-008.6** `[AGG]` ServiceNow Table API profiles: `cmdb_ci*`, `cmdb_rel_ci` (Depends on::Used by, Runs on::Hosts), `incident`, `change_request`, `problem`, `kb_knowledge`; ServiceNow user criteria and roles (`itil`, `cmdb_read`) populate ACLs; write-back only through CRA-027.
- **CRA-008.7** `[AGG]` Splunk saved searches, alerts and dashboards; Grafana `/api/search` and `/api/dashboards/uid/{uid}`; Kibana saved objects per space. Dashboard panels link to CMDB services and microservices as proposals with evidence.
- **CRA-008.8** `[AGG]` Secret and PII redaction is applied to ingested query strings and log snippets before persistence (API keys, tokens, passwords, connection strings, emails per classification policy) and produces a redaction receipt with counts, never the removed values.
- **CRA-008.9** `[RES]` The CI dependency structure is stored as a directed graph; cycles present in the CMDB are detected and reported as data-quality findings, never silently dropped to force a DAG.

**Acceptance obligation CRA-008.A** (only after every clause above is ACCEPTED):

- `[CRAr]` build an incident -> service -> deployment -> dashboard/log evidence journey. Exercise data-source denial, partial/stale telemetry, truncation and ACL revocation; no made-up operational status or causal conclusion is permitted.
- `[MERGED]` A saved-search fixture containing a token and password never surfaces those values in graph, index, logs, metrics or support bundles (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Dashboard metadata ingested without data-source permission checks.

#### CRA-009. Warehouses, Catalog Federation and Custom Systems

*Aggregated title: Data Warehouse, Messaging & Custom Connectors (Snowflake, Fortuna & custom systems)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/024/029 | G (Named sources, media and actions) | M2 | G08 | — | — | INV-42, INV-43, INV-45 | X-12, X-14 | H-06, H-11 |

**Base statement:** Priority P1. Depends on CRA-004/024/029. Sources Snowflake, Fortuna and other enterprise systems.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-009.1** `[CRAr]` Qualify Snowflake metadata and separately authorized data/query-history access with role/warehouse scope, masking/row policies, identifiers, costs and selected SQL/API versions.
- **CRA-009.2** `[CRAr]` Provide metadata-only, sampled-data and virtual-query modes with separate permissions, retention and provider readiness. Sampling/query history must be opt-in and redacted before downstream use.
- **CRA-009.3** `[CRAr]` Require a real product identity, interface/schema and network/auth contract for Fortuna. Until supplied, expose the configured custom-system adapter and missing-input reason, not an invented Fortuna API.
- **CRA-009.4** `[CRAr]` Integrate external catalogs such as OpenMetadata/DataHub/Atlas or commercial platforms through documented public interfaces and explicit ownership/precedence mappings. Do not duplicate their internal metadata model blindly.
- **CRA-009.5** `[CRAr]` Certify custom REST/GraphQL/SOAP/database/file/event providers using CRA-004 and scope-aware source fixtures. A signed plugin plus connectivity does not imply complete domain mappings or authorization fidelity.
- **CRA-009.6** `[AGG]` Snowflake: `INFORMATION_SCHEMA` and, where the role allows, `ACCOUNT_USAGE`; query history feeds CRA-029 lineage parsing; live virtualization through JDBC or Arrow Flight SQL under CRA-024 with statement timeout (default 30 s) and a credit/cost guard.
- **CRA-009.7** `[AGG]` Generic protocol adapters configurable with the mapping IR: REST/OpenAPI, GraphQL, SOAP 1.2, JDBC/ODBC, SFTP/files/object storage, Kafka/RabbitMQ events.
- **CRA-009.8** `[RES]` Fortuna remains a blocked product-specific adapter until decision H-06 supplies product identity, interface and auth contract; meanwhile the generic custom-system adapter is offered with the missing-input reason displayed.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| Snowflake statement timeout | 30 s | RES |

**Acceptance obligation CRA-009.A** (only after every clause above is ACCEPTED):

- `[CRAr]` virtual and materialized queries over the same approved source yield equivalent declared results under masking/null/join cases. Demonstrate source denial, source drift and cost cancellation. Mark product-specific missing access as blocked without blocking the generic factory.
- `[MERGED]` A SPARQL query over Snowflake via OBDA and the same query over a materialized copy return equivalent declared results on null/join/masking fixtures (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

### 7.3 Module M3 — Acquisition, events and multiformat ingestion

#### CRA-010. Durable Source Events and Incremental Synchronization

*Aggregated title: Bitemporal Event Journal & Resumable Checkpoint Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/004/031 | C (First acquisition slice) | M3 | G16 | — | — | INV-24, INV-31, INV-38, INV-40, INV-44, INV-52 | — | H-14 |

**Base statement:** Priority P0. Depends on CRA-003/004/031. Sources INV-31/39/40/44.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-010.1** `[CRAr]` Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, source/resource revision, observed time, payload hash/reference and cursor.
- **CRA-010.2** `[CRAr]` Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable. A content hash cannot hide ACL changes or repeated temporal events.
- **CRA-010.3** `[CRAr]` Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boundary; reconcile crash windows instead of claiming distributed exactly-once.
- **CRA-010.4** `[CRAr]` Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline absence as deletion.
- **CRA-010.5** `[CRAr]` Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy epochs without resurrecting data.
- **CRA-010.6** `[AGG]` Every pushed or pulled event is appended to an immutable append-only event journal; per source instance, each entry stores the SHA-256 of the previous entry so tampering or gaps are detectable.
- **CRA-010.7** `[AGG]` Bitemporal stamping: `observed_at` (platform receipt time) and `source_timestamp` (source-recorded time) are both stored; neither is inferred from the other.
- **CRA-010.8** `[AGG]` A persistent high-watermark checkpoint per connector instance is written transactionally with (or reconciled against) the publication intent so that a crashed worker resumes from the last durable checkpoint with zero loss and zero duplicate published assertions.

**Acceptance obligation CRA-010.A** (only after every clause above is ACCEPTED):

- `[CRAr]` inject crashes before/after raw persistence, graph publication, outbox delivery and cursor acknowledgement. Replay duplicate/reordered/ACL/delete events and compare canonical graph and projections with independently computed expected state.
- `[MERGED]` Kill the ingestion worker at ~50% of a baseline sync, restart, and compare the canonical graph with an independently computed expected graph: zero duplicates, zero gaps, deletes and ACL changes preserved (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A cursor field in a database table that was never crash-tested.

#### CRA-011. Safe Push, Crawl and Network Access

*Aggregated title: Push Webhook Gateway & Sandboxed Crawler Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/004 | C (First acquisition slice) | M3 | — | — | — | — | — | — |

**Base statement:** Priority P0. Depends on CRA-003/004. Sources source-acquisition objective and INV-07/49/52.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-011.1** `[CRAr]` Authenticate push/webhook sources, validate signature/timestamp/body limits and prevent replay. Apply backpressure and never enqueue unbounded payloads.
- **CRA-011.2** `[CRAr]` Restrict crawler schemes, hosts, ports, credentials, depth, pages, bytes, time and request concurrency. Respect authorized source policies and prefer source APIs where available.
- **CRA-011.3** `[CRAr]` Revalidate destination/DNS/redirect policy for every request and attachment URL, including IPv6, private/loopback/link-local/cloud metadata and proxy behavior. Never forward credentials to another origin by default.
- **CRA-011.4** `[CRAr]` Disable browser scripting and arbitrary resource fetching unless an isolated, explicitly permitted adapter requires it. Keep robots/terms/authorization decisions separate; robots permission is not access authorization.
- **CRA-011.5** `[CRAr]` Record crawl coverage, denied/skipped/failed resources and observation times. Partial results cannot become a clean/successful full-source statement.
- **CRA-011.6** `[AGG]` Webhook signature verification: GitHub `X-Hub-Signature-256` (HMAC-SHA256), GitLab `X-Gitlab-Token`, Slack v0 signing secret with timestamp skew <= 5 min, Jira shared secret/JWT per installation type. Failures return HTTP 401 and an audit event; delivery IDs are cached for replay rejection (default TTL 24 h); body limit default 10 MiB; sliding-window rate limit per source.
- **CRA-011.7** `[AGG]` Crawler defaults: max depth 5, max pages 10,000, max 50 MiB per resource, concurrency 2 per host, domain allowlist mandatory, robots.txt honoured but never treated as authorization.
- **CRA-011.8** `[AGG]` Egress block list re-evaluated per request and redirect: RFC 1918, loopback, link-local 169.254.0.0/16 including 169.254.169.254, IPv6 loopback/ULA/link-local, 0.0.0.0, and cloud metadata hostnames; DNS answers pinned for the connection; blocked attempts emit `EGRESS_BLOCKED` audit events.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| crawl depth / pages | 5 / 10,000 | AGG |
| webhook body limit | 10 MiB | RES |
| replay cache TTL | 24 h | RES |

**Acceptance obligation CRA-011.A** (only after every clause above is ACCEPTED):

- `[CRAr]` hostile webhook/replay, redirect/DNS rebinding, zip attachment and credential-forwarding cases are rejected under real network-policy tests. Verify a paused/cancelled crawl releases leases and does not restart itself after cleanup.
- `[MERGED]` A forged HMAC webhook returns 401; a crawl seeded with `http://127.0.0.1/` or `http://169.254.169.254/` is blocked immediately and audited (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-012. Safe Text, Structured Data and Office Parsing

*Aggregated title: Structured Data & Rich Office Document Decoders*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/010/011 | C (First acquisition slice) | M3 | G09, G11 | — | — | — | — | — |

**Base statement:** Priority P0. Depends on CRA-002/010/011. Sources G09/G11 and INV-30/47/49.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-012.1** `[CRAr]` Extend the existing format engine rather than creating duplicate parsers. Support TXT/CSV/JSON/XML/HTML/RTF, DOC/DOCX, PPT/PPTX and XLS/XLSX through qualified adapters, with explicit dependency readiness and format detection.
- **CRA-012.2** `[CRAr]` Preserve paragraph/table/row/column/sheet/slide locators, source encoding and parse/config versions. Distinguish spreadsheet formulas from cached/evaluated values; do not execute macros or embedded code.
- **CRA-012.3** `[CRAr]` Apply global input/expanded/member/depth/text/row/section/time budgets across nesting. Use safe XML/HTML parsing and prevent external-entity/remote-resource execution.
- **CRA-012.4** `[CRAr]` Repair and test chunking progress/termination. Validate `0 <= overlap < chunk_size`; the final chunk exits; empty, boundary, Unicode and long-unbroken inputs terminate without duplicate infinite suffixes.
- **CRA-012.5** `[CRAr]` Model partial extraction and unsupported content explicitly. Preserve raw bytes and warnings so a parser upgrade can rebuild results. A converter exit zero does not certify semantic fidelity.
- **CRA-012.6** `[RES]` Core format set (from the original source requirement): TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX. Extended set (from AGG, required for programme completeness, priority P2): TSV, YAML, JSON-LD (as data), XHTML, Markdown, AsciiDoc, ODT, ODP, ODS and text-layer PDF. Each format has its own capability entry and readiness state.
- **CRA-012.7** `[AGG]` Candidate libraries (each subject to CRA-035 license review and pinned versions): python-docx, python-pptx, openpyxl and/or calamine, defusedxml or lxml with entity resolution disabled, BeautifulSoup over a safe parser, and LibreOffice headless or Apache Tika for legacy DOC/PPT/XLS executed only in `heavy` workers.
- **CRA-012.8** `[AGG]` Every chunk carries an `EvidenceLocator` (document ID, source system, source revision, page/slide/sheet/cell/paragraph/run index, char_start/char_end).
- **CRA-012.9** `[AGG]` Qualification target on P0 reference hardware: a 10 MB DOCX and a 50-sheet XLSX are fully extracted with locators in <= 5 s each (benchmark manifest target, not a claim until measured).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| chunk invariant | 0 <= overlap < chunk_size | CRAr |

**Acceptance obligation CRA-012.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independently authored golden files for every format plus corrupted, encrypted, malformed and oversized inputs. Run the suspected long-input loop reproduction in a timeout-isolated process, then prove bounded termination and complete intended text coverage. Missing optional tools must yield UNAVAILABLE, not empty successful documents.
- `[MERGED]` Property-based (Hypothesis) chunker tests over random Unicode strings, overlaps and sizes prove termination, progress and full coverage; the G11 long-input reproduction runs in a timeout-isolated process before and after the fix.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A parser registered for an extension with no golden-file test.

#### CRA-013. Email, Containers and Nested Provenance

*Aggregated title: Email, Mailbox Container & Archive Parsers*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-012/035/040 | C (First acquisition slice) | M3 | — | — | — | — | X-16 | H-09 |

**Base statement:** Priority P0. Depends on CRA-012/035/040. Sources attachment format requirements and G17.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-013.1** `[CRAr]` Parse EML/MIME and approved mailbox protocols with stable message/thread/header/body-part identity. Support MSG only through an explicitly licensed and qualified adapter; do not silently clear existing dependency concerns.
- **CRA-013.2** `[CRAr]` Preserve parent message/archive/document relationships, attachment content hashes, original names, source locators and inherited ACL/retention/legal-hold metadata.
- **CRA-013.3** `[CRAr]` Enforce combined archive/container expansion, depth, member count and path-safety limits, including duplicate names, symlinks and format confusion. Do not extract untrusted paths into the application filesystem.
- **CRA-013.4** `[CRAr]` Handle encrypted/unreadable attachments, malformed MIME, embedded messages and converter failure with per-item diagnostics and aggregate partial/failed status.
- **CRA-013.5** `[CRAr]` Prevent automatic remote-image loading, active HTML/script execution and credential extraction from messages. Every attachment download rechecks source authorization.
- **CRA-013.6** `[AGG]` Formats: EML/MIME and MBOX; MSG only through an explicitly licensed adapter (`extract-msg` remains disabled until its distribution terms are cleared under CRA-035, conflict X-16).
- **CRA-013.7** `[AGG]` Extract headers `From`, `To`, `Cc`, `Bcc` (only where the source exposes it and policy allows), `Subject`, `Date`, `Message-ID`, `In-Reply-To`, `References`; plain-text body; sanitized HTML body; nested attachments recursively queued with inherited ACLs.
- **CRA-013.8** `[AGG]` Archives: ZIP, TAR, GZ, BZ2, 7Z with streaming decompression and combined limits: total expanded size 2 GiB, nesting depth 3, 10,000 members, per-member compression ratio 100:1; reject absolute paths, `..`, drive letters, symlinks/hardlinks and duplicate-name overwrite.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| archive limits | 2 GiB / depth 3 / 10,000 members / 100:1 | AGG + RES |

**Acceptance obligation CRA-013.A** (only after every clause above is ACCEPTED):

- `[CRAr]` nested email/archive bombs, traversal, duplicate members, malformed encodings and restricted attachments fail safely. Demonstrate source email deletion/hold behavior across every nested derivative and artifact; preserve separately licensed component obligations.
- `[MERGED]` An EML with an attached ZIP containing a PDF and an XLSX is indexed at all three levels with correct parent-child provenance and inherited ACL (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-014. Images, Audio and Video

*Aggregated title: Multimedia, Speech-to-Text & Computer Vision OCR Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-002/012/026/035/040 | G (Named sources, media and actions) | M3 | G09 | — | — | INV-51, INV-52 | — | — |

**Base statement:** Priority P1. Depends on CRA-002/012/026/035/040. Sources INV-51/52.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-014.1** `[CRAr]` Provide capability-specific image metadata, OCR, audio transcription, video decode/frame sampling and optional visual extraction adapters. Report exactly which tasks/providers are configured, rather than one multimodal flag.
- **CRA-014.2** `[CRAr]` Retain coordinates/page/frame/time spans, language, confidence, provider/model/config revisions and raw evidence references. Transcript/visual outputs remain proposed unless approved by applicable publication policy.
- **CRA-014.3** `[CRAr]` Isolate codecs/OCR/ML execution, enforce duration/resolution/frame/sample/output budgets and prohibit unapproved model downloads/network calls. Required model assets must be available in offline bundles.
- **CRA-014.4** `[CRAr]` Support cancellation/progress based on actual work and explicit partial output. Preserve unsupported or low-quality segments; never fabricate text, timestamps or diagram topology.
- **CRA-014.5** `[CRAr]` Evaluate WER/CER, entity/fact precision/recall and visual task accuracy on licensed domain/language corpora with held-out splits. Apply section 4's selected thresholds through per-task/profile manifests, not as an unsupported universal quality claim.
- **CRA-014.6** `[AGG]` OCR for PNG, JPG/JPEG, TIFF, WEBP and scanned PDF using a license-reviewed engine (Tesseract or PaddleOCR candidates); each line/paragraph carries a normalized bounding box `[ymin, xmin, ymax, xmax]` in 0.0-1.0 plus page number and confidence.
- **CRA-014.7** `[AGG]` Audio/video: audio extraction with FFmpeg (build flags determine LGPL/GPL obligations, reviewed under CRA-035) for MP4, MKV, MP3, WAV, M4A; transcription with a locally hosted Whisper-family model in an isolated worker; segments carry start/end milliseconds.
- **CRA-014.8** `[AGG]` All OCR/ASR/vision models run on-premises or inside the customer VPC from hash-pinned offline bundles; zero external API calls in no-egress mode.
- **CRA-014.9** `[GN]` OCR, ASR and vision models require the CRA-043 tiers they depend on plus offline bundles; a missing tier sets the task capability to UNAVAILABLE with the tier named, never a metadata-only result labelled as understanding.

**Acceptance obligation CRA-014.A** (only after every clause above is ACCEPTED):

- `[CRAr]` real permitted media files, degraded scans/noise/unsupported codecs and large/hostile inputs. Verify no external call in no-egress mode, correct evidence locators, timeout cleanup and dependency-unavailable states. File metadata alone does not satisfy OCR/transcription/understanding.
- `[MERGED]` Searching a spoken phrase returns the exact media file and millisecond timestamp, visible only to authorized principals (AGG).
- `[GN]` With the required tier absent, OCR/ASR requests return 503 naming the tier; with it present and networking disabled, transcription succeeds from the offline bundle.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- File metadata extraction labelled as OCR/transcription.

#### CRA-015. Engineering Diagram Semantics

*Aggregated title: Engineering Diagram & Architecture Visual Parser*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-012/014/016/017 | G (Named sources, media and actions) | M3 | G10 | — | — | INV-07 | — | — |

**Base statement:** Priority P1. Depends on CRA-012/014/016/017. Sources G10 and INV-07/32.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-015.1** `[CRAr]` Support notation-specific structured diagrams, initially diagrams.net/Chowlk-compatible conceptual diagrams plus declared Mermaid/PlantUML subsets; retain the exact source and parser coverage.
- **CRA-015.2** `[CRAr]` Parse components, ports, containment, directions, cardinalities, sequence/event meaning and labels only where supported. Never silently coerce every box to Service or unknown relation to CALLS.
- **CRA-015.3** `[CRAr]` Visual extraction from images/video creates candidates with bounding regions, uncertainty and reviewer controls. Distinguish inferred visual interpretation from formal notation semantics.
- **CRA-015.4** `[CRAr]` Show a source-versus-graph diff and loss ledger. Unsupported constructs block claims of lossless conversion; the reviewer may explicitly accept a limited projection without altering the source.
- **CRA-015.5** `[CRAr]` Round-trip supported models to editable diagrams or maintain a documented non-round-trippable status. Escape/sanitize all generated markup and labels.
- **CRA-015.6** `[AGG]` Structured formats: draw.io/diagrams.net XML (including Chowlk notation), declared PlantUML and Mermaid subsets; Visio VSDX as an extended P2 format. Parse into a diagram AST of shapes, labels, ports, containers and connectors with direction.
- **CRA-015.7** `[AGG]` A configurable, versioned shape/connector mapping table proposes ontology terms (for example cylinder -> `ex:Database`, rectangle -> `ex:Service`, arrow label 'calls' -> `ex:calls`); mappings are proposals reviewed before publication.
- **CRA-015.8** `[AGG]` Unrecognized connectors are preserved as generic directed edges (`eoip:connectsTo`) with all visual attributes and an entry in the loss ledger; never coerced to `CALLS` or `Service` (G10). A vision-LLM fallback for raster diagrams produces only reviewed candidates with bounding regions.

**Acceptance obligation CRA-015.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independently specified gold diagrams with parallel/directed edges, labels/metacharacters, nesting and intentionally unsupported constructs. Compare formal axioms and business meaning, not just vertex counts or rendered screenshots. Verify correction/rejection propagates to graph/provenance/indexes.
- `[MERGED]` Parse a microservice architecture diagram; reviewed output compiles into valid OWL 2/RDF assertions whose formal comparison with an independently authored gold model shows 100% fidelity for the supported subset and an explicit loss ledger for the rest (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

### 7.4 Module M4 — Canonical semantics: RDF, mapping, registry, reasoning, SHACL

#### CRA-016. RDF Terms, Parsing and Standards Fidelity

*Aggregated title: RDF 1.1 / RDF-Star Terms & Lexical Fidelity Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | D (Semantic core) | M4 | F1, G03, G05 | ONT-001, ONT-019 | I1, I10 | INV-01, INV-20, INV-26, INV-37, INV-55 | X-17, X-29 | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Sources G03/G05 and INV-01/23/26/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-016.1** `[CRAr]` Use a proven standards parser for the selected RDF/JSON-LD serializations and validate exact supported syntax/profile. Do not describe the EOIP-specific compact JSON-LD importer as a general implementation.
- **CRA-016.2** `[CRAr]` Preserve IRI lexical identity, case, blank-node scope, language tags, datatype and literal lexical/value distinctions, RDF lists, named graph identity and annotations. Normalized display labels never mutate canonical IDs.
- **CRA-016.3** `[CRAr]` Restrict JSON-LD contexts and ontology imports by the approved resolver policy, hash-pin approved external resources and support disconnected resolution. Block SSRF and remote context changes.
- **CRA-016.4** `[CRAr]` Distinguish syntax validity, ontology profile membership, logical consistency and instance-shape validity with separate outcomes.
- **CRA-016.5** `[CRAr]` Qualify export/import using independent parsers and canonical/isomorphic dataset comparisons plus semantic competency queries. Report bounds, truncation, unsupported constructs and loss counts explicitly.
- **CRA-016.6** `[OCA]` Adopt `rdflib>=7` (BSD-3, pinned) as default parser/serializer for Turtle, RDF/XML, N-Triples, N-Quads, JSON-LD 1.1 and TriG in new module `packages/eoip/ontology/serialization.py` (`RDFSerializer`, `RDFDeserializer`). RDF/XML and any XML input are parsed with external entity resolution disabled, size caps and a parse timeout (XXE and entity-expansion defence).
- **CRA-016.7** `[OCA]` API: `POST /ontology/import` (`format`, `content` or `artifact_ref`) returns an import report (triple/quad counts, named graphs, losses, unsupported constructs); `GET /ontology/export?format=turtle|rdfxml|nt|nq|jsonld|trig` emits valid output. `rdf.py:jsonld_to_property_graph` may be reused as an internal pivot only after its behaviour is covered by independent tests.
- **CRA-016.8** `[AGG]` RDF-star is an optional named profile `rdf-star` (disabled by default) with its own conformance tests; when disabled, statement-level annotations use named-graph assertion reification (X-17).
- **CRA-016.9** `[OCA]` Round-trip corpus (ONT-001/ONT-019): pinned gist release, pinned schema.org release, FOAF, Dublin Core, a >= 10k-triple SKOS thesaurus and a FIBO subset. Exported OWL loads without error in Protégé 5.6 (manual review record) and in OWL API inside a semantic worker (automated).
- **CRA-016.10** `[RES]` Fidelity rule (resolves X-29): 100% term/axiom fidelity on the declared supported subset; corpus-level fidelity reported with every loss enumerated (unsupported constructs stay in the denominator); CI fails if corpus fidelity regresses by more than 1 percentage point versus the last ACCEPTED report (ONT-019).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| rdf-star profile | disabled | RES |
| parse timeout | 30 s online / job beyond | RES |

**Acceptance obligation CRA-016.A** (only after every clause above is ACCEPTED):

- `[CRAr]` case-distinct IRIs remain distinct; equivalent blank-node relabellings compare correctly; datatype/language/named graph round trips preserve meaning. Hostile/cyclic/remote contexts and malformed literals fail safely. A standards-shaped JSON object is not conformance evidence.
- `[MERGED]` Import/export of every format in the corpus passes isomorphism checks with an independent parser; a hostile RDF/XML with an external entity and a billion-laughs payload is rejected within the time cap.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- An EOIP compact JSON-LD importer described as general JSON-LD support.

#### CRA-017. Mapping IR, RDF/LPG Projection and OBDA Inputs

*Aggregated title: Declarative Mapping IR & Relational OBDA Virtualization*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-010/016 | D (Semantic core) | M4 | G05, G10, G13 | ONT-005, ONT-006, ONT-017, ONT-018 | I1, I7, I8, I9, I12 | INV-03, INV-07, INV-16, INV-21, INV-23, INV-26, INV-27, INV-28, INV-30, INV-31, INV-32, INV-34, INV-35 | X-17 | — |

**Base statement:** Priority P0. Depends on CRA-010/016. Sources G05/G10/G13 and INV-03/16/26/27/28/30/31/35.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-017.1** `[CRAr]` Define a versioned, engine-neutral mapping representation for source schema/records to ontology terms, including stable identity, joins, nulls, datatypes, language, provenance and graph policy.
- **CRA-017.2** `[CRAr]` Support qualified R2RML/RML adapters and explicit source-dialect/config compatibility. User-defined functions run through CRA-002 with approved capabilities.
- **CRA-017.3** `[CRAr]` Preserve multigraph/relationship assertion IDs, edge properties and evidence when projecting to/from property graphs. Record every unsupported construct and lossy coercion; block lossless claims when any loss exists.
- **CRA-017.4** `[CRAr]` Separate virtual mappings from materialized ingestion, including source access policy, transaction/snapshot/freshness semantics and resource costs. Do not pretend source rows are copied when queries are virtualized, or vice versa.
- **CRA-017.5** `[CRAr]` Provide mapping test cases, dry-run/sample preview, field diagnostics and source-drift analysis. Bind approval/publication to source schema and ontology/mapping revisions.
- **CRA-017.6** `[OCA]` Connector Mapping Language (CML), YAML: `source`, `version`, `subject_map{template, class}`, `property_maps[{path, predicate, datatype, required, vocab}]`, `relation_maps[{path, predicate, object_template, object_class}]`, `provenance{emit, confidence}`, `governance{classification, pii_fields}`. Paths use a documented JSONPath subset; templates use `{field}` substitution with IRI-safe encoding and a whitelist of functions (lower, upper, trim, concat, split, date_parse, iri_safe). Templates are never evaluated as code.
- **CRA-017.7** `[RES]` CML compiles into the engine-neutral mapping IR; R2RML/RML (and RML-star when enabled) import translates into the same IR with an unsupported-construct report (ONT-017). One IR, many front-ends.
- **CRA-017.8** `[OCA]` LPG <-> RDF projection scheme: vertex IRI `eoip:entity/{Label}/{id}` (id percent-encoded) with `rdf:type eoip:class/{Label}`; vertex property `eoip:property/{name}` as typed literal from the manifest; edge without properties -> direct triple `eoip:relation/{label}`; edge with properties -> RDF-star when the profile is enabled, otherwise a named graph per edge assertion `urn:eoip:assertion:{id}`; tenant named graph `urn:eoip:tenant:{id}`. Parallel same-label edges keep distinct assertion IDs (I1).
- **CRA-017.9** `[OCA]` W3C PROV-O on every mined triple (ONT-018): `prov:wasDerivedFrom` source resource revision, `prov:wasGeneratedBy` mapping-run activity (mapping revision, connector run ID), `prov:wasAttributedTo` connector agent; provenance survives RDF export.
- **CRA-017.10** `[OCA]` AI-suggested mappings (ONT-006): sample bounded, redacted payloads and propose CML with per-field confidence; suggestions never auto-activate. Evaluation target: >= 70% of suggested property maps accepted without edit on Jira and ServiceNow corpora.
- **CRA-017.11** `[AGG]` Benchmark targets recorded in the manifest: CML execution >= 10,000 records/s on 1M Jira issues (OCA); vectorized batch materialization (Morph-KGC-class) >= 100,000 triples/s on CSV/JSON (AGG); OBDA point query on a 10M-row indexed PostgreSQL table < 50 ms via SQL pushdown (AGG).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| CML template functions | lower, upper, trim, concat, split, date_parse, iri_safe | OCA + RES |

**Acceptance obligation CRA-017.A** (only after every clause above is ACCEPTED):

- `[CRAr]` nulls, multi-value joins, language/datatype literals, blank nodes, duplicate/parallel edges and restricted fields are compared against independent expected RDF and query results. Same approved mapping executes through two qualified adapters with documented equivalence or explicit differences.
- `[MERGED]` Jira, Confluence and ServiceNow mappings expressed in CML pass parity tests; PII fields declared in CML are removed by the export filter; a template containing `__import__` or `{0.__class__}` is rejected at parse time.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Mapping logic hidden inside connector Python counted as declarative mapping support.

#### CRA-018. Durable Ontology Registry and Packages

*Aggregated title: Immutable Ontology Package Registry & Semantic Versioning*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-016/031/035 | D (Semantic core) | M4 | F1 | ONT-010 | I15, I20 | INV-01, INV-02, INV-06, INV-08, INV-09, INV-15, INV-25, INV-33, INV-46, INV-50, INV-55 | X-03, X-30 | — |

**Base statement:** Priority P0. Depends on CRA-016/031/035. Sources INV-02/15/25/46/50/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-018.1** `[CRAr]` Persist ontology/version IRIs, imports/checksums, axioms, annotations, shapes, rules, mappings, namespace ownership, profile and license metadata in a canonical registry.
- **CRA-018.2** `[CRAr]` Package immutable releases with full import closure, engine/profile/config references, provenance, validation/reasoning reports and publication signatures/manifests.
- **CRA-018.3** `[CRAr]` Keep drafts, accepted releases and source/derived graph revisions separate. No mutable global singleton or browser localStorage may be the sole authority.
- **CRA-018.4** `[CRAr]` Support domain packs and optional pinned upper ontologies such as gist, preserving upstream terms, namespaces, attribution and migration notes. Do not imply importing an upper ontology models the entire enterprise.
- **CRA-018.5** `[CRAr]` Resolve and install packages atomically with compatibility and signature checks, approved repositories and offline availability. Reject missing/tampered/unlicensed dependencies with explicit diagnostics.
- **CRA-018.6** `[AGG]` A release bundle contains: primary ontology document(s), pinned transitive import closure with SHA-256 digests, SHACL shapes package, mapping definitions, release manifest and signature. Tampering with any member causes signature mismatch and activation halts.
- **CRA-018.7** `[OCA]` Semantic versioning (SemVer 2.0) is computed from the semantic diff using the existing `compute_next_semver` (gitops.py:733) after it is verified by fixtures: major for breaking changes (removal, domain/range or cardinality tightening, type change), minor for additive changes, patch for annotation-only changes.
- **CRA-018.8** `[OCA]` Domain packs (ONT-010) via existing `packs.py`, `domain_pack_manager.py` and `industry_templates.py`: gist (CC BY 4.0, attribution in NOTICE and docs), FIBO and schema.org (license terms verified per exact artifact, X-30), SNOMED-CT only when customer-provided under the customer's affiliate license and never redistributed.

**Acceptance obligation CRA-018.A** (only after every clause above is ACCEPTED):

- `[CRAr]` clean restart and fresh-node restore retrieve the same package/release by hash; missing import, changed remote document or incompatible engine cannot silently publish. Compare independently opened package contents and release metadata, not only a database row.
- `[MERGED]` Each domain pack installs, validates under its declared profile and records attribution; a tampered import file triggers signature mismatch and halts activation (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-019. Profile-Correct Reasoning and Explanations

*Aggregated title: Hybrid Tiered Reasoning Engine (HTRE) & Dependency Retraction*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/016/018 | D (Semantic core) | M4 | F2, G03, G04 | ONT-007, ONT-008 | I4, I5, I18 | INV-01, INV-03, INV-04, INV-05, INV-17, INV-18, INV-19, INV-20, INV-22, INV-27, INV-46, INV-48, INV-53, INV-55 | X-10, X-28 | H-02 |

**Base statement:** Priority P0. Depends on CRA-002/016/018. Sources G03/G04 and INV-01/04/17/18/19/20/22/46/48/53/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-019.1** `[CRAr]` Replace or clearly scope the custom helper; do not advertise it as complete OWL DL. Use qualified engines for RDFS, OWL 2 RL/EL/QL/DL tasks with explicit supported profiles and limits.
- **CRA-019.2** `[CRAr]` Preserve exact identifiers, load pinned import closure, check profile membership and distinguish consistency, unsatisfiable classes, classification and entailment tasks.
- **CRA-019.3** `[CRAr]` Return engine/version/profile, asserted versus inferred statements, explanations/support dependencies, revision and unsupported/error/timeout/cancel status. Timeouts cannot become negative entailment or a clean consistency result.
- **CRA-019.4** `[CRAr]` Keep inferred graphs separate and implement dependency-aware invalidation/retraction after source, ontology, identity or ACL changes. Handle multiple justifications correctly.
- **CRA-019.5** `[CRAr]` Offer materialized/query-time modes only where supported and measured. Expose resulting plan, amplification and freshness rather than hiding expensive work.
- **CRA-019.6** `[CRAr]` Enforce CRA-003 on inference inputs/outputs/explanations. Prevent restricted supporting facts from leaking through an otherwise visible conclusion.
- **CRA-019.7** `[OCA]` Define `ReasonerPort` in `packages/eoip/ontology/reasoning/port.py`: `classify()`, `is_consistent()`, `unsatisfiable_classes()`, `realize()`, `entails(axiom)`, `explain(axiom)`, each returning typed results with engine, version, profile, status (OK, INCONSISTENT, UNSUPPORTED, TIMEOUT, CANCELLED, ERROR) and revision bindings.
- **CRA-019.8** `[OCA]` Adapters: ELK (Apache-2.0, OWL 2 EL, default for classification), Openllet (license verified, OWL 2 DL alternative), HermiT (LGPL, optional separately installed plugin only), Jena rules for OWL 2 RL/RDFS, and `NativeAdapter` wrapping the existing `OWLReasoner` restricted to and labelled as profile `eoip-native-rdfs-subset`.
- **CRA-019.9** `[OCA]` Remove the hardcoded domain axioms of `OWLReasoner._bootstrap_core_axioms()` (Microservice, Engineer, RelationalDatabase; rdf.py:598-700) from all production paths; axioms come from the manifest and installed packages. The old axioms may remain only as a named test fixture.
- **CRA-019.10** `[AGG]` Hybrid mode (ONT-008 / AGG HTRE): a per-rule strategy table (`materialize` or `query_time`) chosen by a documented cost model (estimated amplification, volatility, fan-out, query frequency); a TBox change recomputes only affected rules; benchmarked against pure forward and pure backward chaining.
- **CRA-019.11** `[RES]` Retraction uses stored justification sets (`supporting_assertion_ids`); cost is proportional to affected derivations and is measured, replacing the unproven AGG 'O(1)' claim (X-10).
- **CRA-019.12** `[AGG]` Consistency failures abort publication with an `InconsistentOntologyException`-equivalent typed error that lists a minimal conflicting axiom set whenever the engine supports justification extraction; otherwise it states that justification is unavailable.
- **CRA-019.13** `[OCA]` Qualification target: classify a 20k-class / 150k-axiom EL ontology in < 60 s with ELK on the P1 reference node. If JVM workers are forbidden (decision H-02), the platform reports an explicit degraded profile, never a silent fallback.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| default classifier | ELK (EL profile) | OCA |
| reasoning deadline | 30 s online, otherwise durable job | CRAr |

**Acceptance obligation CRA-019.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independent gold entailments, non-entailments, incoherence, profile violations, chains/cycles, duplicate support and retraction. The observed case-folding probe must no longer conflate distinct IRIs. Compare a qualified independent engine on the common profile and retain exact differing cases; never replace disagreement with a blanket pass.
- `[MERGED]` Known-inconsistent fixture is detected; unsatisfiable classes are reported; `grep` over production modules finds no hardcoded domain axioms; the case-folding probe (G03) returns false.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A reasoner class named OWLReasoner; transitive subclass closure described as OWL DL.

#### CRA-020. Transactional Shape Validation

*Aggregated title: Strict Transactional W3C SHACL Core 2017 Validator*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/016/018/031 | D (Semantic core) | M4 | F3, G01, G02 | ONT-004 | I10 | INV-02, INV-06, INV-08, INV-17, INV-20, INV-22, INV-26, INV-47, INV-48, INV-49 | — | — |

**Base statement:** Priority P0. Depends on CRA-002/016/018/031. Sources G01/G02 and INV-22/47/48/49.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-020.1** `[CRAr]` Use a proven validator for declared SHACL Core 2017 coverage; keep extensions/profile versions explicit. A custom Python property checker must be labelled as such until replaced/qualified.
- **CRA-020.2** `[CRAr]` Enforce min/max cardinality, datatype/node kind, class, value sets, language/length/pattern/numeric bounds, logical and property-path constraints for the declared profile. Unsupported constraints must produce an explicit unsupported result, never `conforms=true`.
- **CRA-020.3** `[CRAr]` Produce standards-compatible reports with focus node, result path/value, source shape/constraint, severity and message, plus revision/engine/config and explicit truncation. Unknown datatype names fail validation setup.
- **CRA-020.4** `[CRAr]` Validate the candidate against required existing data and shape/ontology revision. Publication requires revision recheck or transactional isolation so concurrent individually valid writes cannot jointly violate a constraint.
- **CRA-020.5** `[CRAr]` Revalidate affected data on shape changes; clearly distinguish incremental supported validation from a full check. Timeout, runtime failure, cancellation and unavailable validator block required publication.
- **CRA-020.6** `[CRAr]` Bound CPU/memory/report size and restrict remote imports/SPARQL/JS/UDF execution. Required advanced profiles receive separate qualification rather than implicit enabling.
- **CRA-020.7** `[OCA]` Adopt pySHACL (Apache-2.0, pinned) as default validator inside an isolated worker; TopBraid SHACL API (Apache-2.0, JVM) is the differential oracle for the common profile (INV-48).
- **CRA-020.8** `[OCA]` Fix `export_shacl_shapes()` (rdf.py:369-425): emit `sh:datatype`, `sh:nodeKind`, `sh:minCount`, `sh:maxCount`, `sh:pattern`, `sh:class`, `sh:in`; convert `eoip:allowedEndpointPairs` into conformant `sh:targetSubjectsOf`/`sh:targetObjectsOf` plus `sh:class` constraints, and keep any remaining `eoip:` terms in a separately named extension profile (F3).
- **CRA-020.9** `[OCA]` Keep `SHACLValidationReport` as the public type and the existing `/ontology/validate` contract unchanged (contract test); add `POST /ontology/validate/shacl` and the asynchronous `POST /api/v1/semantic/validations` (Idempotency-Key required) from the CRA OpenAPI fragment.
- **CRA-020.10** `[AGG]` Mutation API semantics: violation -> HTTP 422 with a W3C `sh:ValidationReport` and per-result codes (e.g. `SHACL_CARDINALITY_VIOLATION`, `SHACL_DATATYPE_VIOLATION`); unsupported constraint -> 422 `UNSUPPORTED_CONSTRAINT`; validator unavailable -> 503; zero triples committed in every failure case.
- **CRA-020.11** `[OCA]` Throughput qualification target: >= 20,000 nodes/s on 10M nodes with 500 shapes (benchmark manifest target).

**Acceptance obligation CRA-020.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independently authored min/max counts including zero/multivalues, invalid datatypes, paths, shape updates and concurrent conflicts. Reproduce G01/G02 separately, then demonstrate rejection and unchanged canonical graph after failure. Compare results against an independent validator for the common declared profile.
- `[MERGED]` Exported shapes parse with an independent SHACL processor and produce the same violations as reference pySHACL on an invalid fixture; existing `/ontology/validate` callers pass unchanged.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A custom validator returning `conforms=true` for an unrecognized datatype (G02).

### 7.5 Module M5 — Vocabulary, governance, identity and query

#### CRA-021. Vocabulary, Taxonomy and Multilingual Stewardship

*Aggregated title: Multilingual Taxonomy & Controlled Vocabulary Stewardship (SKOS / SKOS-XL)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-018/020/022 | E (Governed knowledge) | M5 | F1 | ONT-016 | I17 | INV-04, INV-06, INV-09, INV-10, INV-11, INV-12, INV-13, INV-14, INV-15, INV-51, INV-54 | — | — |

**Base statement:** Priority P1. Depends on CRA-018/020/022. Sources INV-06/09/10/11/12/13/14/15/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-021.1** `[CRAr]` Support SKOS concepts/schemes, broader/narrower/related, polyhierarchy, preferred/alternative/hidden labels with language tags, mappings, deprecation/replacement and explicit concept-versus-label identity.
- **CRA-021.2** `[CRAr]` Provide SKOS-XL and OntoLex-Lemon through qualified optional profiles where required; reject unsupported export/import rather than flattening silently.
- **CRA-021.3** `[CRAr]` Support candidate terms, definitions, synonyms, crosswalk proposals, provenance, domain ownership and review. Model suggestions must not auto-create equivalence or upstream namespace terms.
- **CRA-021.4** `[CRAr]` Version vocabularies with classifier/embedding/index dependencies and publication receipts. Record consumer acknowledgement and stale projection state after change.
- **CRA-021.5** `[CRAr]` Provide language-aware search/editing and Unicode/RTL-safe presentation, label uniqueness policies and stable IDs independent of translated labels.
- **CRA-021.6** `[OCA]` Wire the existing SKOS object model (`skos.py`, 450 LOC: Concept, ConceptScheme, Collection, mappings, integrity issues, label conflicts) to the CRA-016 serializer (ONT-016): a 10k-concept SKOS thesaurus imports and re-exports losslessly and SKOS-XL labels are preserved.
- **CRA-021.7** `[AGG]` Labels per BCP-47 language tag; deprecation via `owl:deprecated true` plus `dct:isReplacedBy`; audited editorial notes; ISO 25964-style thesaurus import fixture.
- **CRA-021.8** `[OCA]` Existing drift detection (`drift.py`, `embedding_drift.py`) emits evolution proposals into CRA-022 review; proposals are never auto-applied (I17).

**Acceptance obligation CRA-021.A** (only after every clause above is ACCEPTED):

- `[CRAr]` multilingual import/edit/export, same-label distinct concepts, cyclic taxonomy policy, polyhierarchy, retired terms and concurrent edits. Change a vocabulary and verify dependent classifier/search output, rollback and evidence preservation. Evaluate domain-specific vocabularies separately from software license rights.
- `[MERGED]` 10k-concept multilingual round-trip is isomorphic; a drift proposal appears in the review queue and changes nothing until approved.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-022. Ontology and Mapping Change Governance

*Aggregated title: Ontology Change Governance, Visual Diffs & Pull-Request Workflows*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/018/019/020/031 | E (Governed knowledge) | M5 | F4 | ONT-012, ONT-013 | I14, I15, I16 | INV-01, INV-02, INV-03, INV-04, INV-07, INV-08, INV-09, INV-11, INV-12, INV-14, INV-15, INV-16, INV-22, INV-25, INV-32, INV-34, INV-38, INV-40, INV-41, INV-46, INV-48, INV-49, INV-50, INV-53 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/018/019/020/031. Sources INV-02/08/12/15/16/25/34/40/46.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-022.1** `[CRAr]` Implement durable draft -> validation -> review -> approval -> publication -> superseded/rollback lifecycle with explicit roles, separation of duties and audited decisions.
- **CRA-022.2** `[CRAr]` Diff semantic statements, imports, shapes, mappings, labels and policy implications rather than only text files. Display impacted data, queries, indexes, sources and actions with bounded analysis.
- **CRA-022.3** `[CRAr]` Bind approval to exact candidate, base, ontology, shapes, mapping and policy revisions. Concurrent edits produce conflict/precondition errors; stale approval cannot authorize changed content.
- **CRA-022.4** `[CRAr]` Support scheduled/atomic publication and compatible rollback with immutable manifests, consumer acknowledgement, explicit partial failure and repair. Retain history and tenant isolation through restart.
- **CRA-022.5** `[CRAr]` Run competency questions, profile/consistency/shapes checks, domain review and migration dry-runs as release gates. No generated or agent-written ontology bypasses these gates.
- **CRA-022.6** `[OCA]` Preserve the existing GitOps core (`gitops.py`, 793 LOC: branches, PRs with review gates, semantic diff, impact analysis `run_ontology_impact_analysis`, migration-script generation gitops.py:545, rollback receipts gitops.py:613-733, semver gitops.py:733, release packaging) and `gitops_router.py` endpoints. New capabilities attach through ports. Any change to `gitops.py`, `manifest.py` or `packs.py` requires a recorded Lead Developer review (OR7).
- **CRA-022.7** `[OCA]` Offline ontology pitfall scanner (ONT-013, INV-49) in `packages/eoip/ontology/lint/` detecting at least 20 antipattern classes (including missing domain/range, circular hierarchy, equivalent-class loops, unconnected elements, naming inconsistency, missing labels/definitions, deprecated-term use, inverse-property conflicts); every finding has severity and remediation hint; it runs as a PR gate blocking merge at severity >= error.
- **CRA-022.8** `[AGG]` PR gate pipeline: profile check, consistency (CRA-019), SHACL instance regression (CRA-020), pitfall lint, competency questions, semantic diff and impact; production-branch merge requires two distinct steward approvals.
- **CRA-022.9** `[AGG]` Semantic AST diff (added/removed classes and properties, changed cardinalities, changed subsumption) is shown visually in the UI (CRA-030), not only as text lines.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| production merge approvals | 2 distinct stewards | AGG |

**Acceptance obligation CRA-022.A** (only after every clause above is ACCEPTED):

- `[CRAr]` two editors conflict, reviewer denies, approval expires, policy changes, publication crashes and consumer fails. Prove old/new versions remain reproducible and rollback restores business queries without falsely undoing external actions. A save button or append-only policy call is not governed publication.
- `[MERGED]` Create a branch that introduces an unsatisfiable class, open a PR: the gate blocks merge with an explanation report (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-023. Canonical Identity, Alignment and Reversible Resolution

*Aggregated title: Canonical Identity Resolution & Reversible Entity Merging*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/010/016/019/022 | E (Governed knowledge) | M5 | — | ONT-015 | — | INV-13, INV-37, INV-52, INV-53, INV-54 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/010/016/019/022. Sources INV-13/37/52/53/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-023.1** `[CRAr]` Define scoped source identity and canonical-ID mapping with deterministic idempotency, aliases and source-instance boundaries. Same textual ID in two systems/tenants is not one entity.
- **CRA-023.2** `[CRAr]` Generate alignment/merge candidates with lexical/structural/model evidence, uncertainty, domain rules and NIL/no-match outcomes. Never infer `owl:sameAs` or merge solely from label or vector similarity.
- **CRA-023.3** `[CRAr]` Require approval for high-impact identity/schema changes and run consistency/constraint checks on proposed mappings. Preserve conflicting source claims instead of overwriting them silently.
- **CRA-023.4** `[CRAr]` Support reversible merge/split with relationship assertion/evidence/provenance preservation, temporal history and retraction/rebuild of dependent inferences and indexes.
- **CRA-023.5** `[CRAr]` Evaluate candidate precision/recall/calibration by tenant/domain/language and adverse ambiguity, with held-out gold data. Model changes require reevaluation and versioned review results.
- **CRA-023.6** `[AGG]` Candidate generation combines deterministic keys (email, employee ID, account ID) with probabilistic features (Jaro-Winkler and normalized labels, embedding similarity, neighbourhood structural similarity) and always supports a NIL/no-match outcome.
- **CRA-023.7** `[OCA]` Schema/pack alignment uses a DeepOnto (BERTMap/BERTSubs) service in an isolated GPU/CPU worker (ONT-015); entity linking in text uses spaCy EntityLinker with a tenant-scoped knowledge base generated from the graph (INV-54). All outputs are candidates.
- **CRA-023.8** `[AGG]` An immutable `IdentityMergeLedger` records every merge/split; a split restores the original nodes, edges, evidence and dependent inferences atomically.
- **CRA-023.9** `[GN]` The probabilistic features of CRA-023.6 (embedding similarity, neighbourhood structural similarity) and the alignment worker of CRA-023.7 require CRA-043 tiers and, for structural similarity, a CRA-044 model that passed its anti-stub probes; when unavailable the candidate generator reports the reduced feature set used and never substitutes hash or random similarity.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| linking gate | precision >= 0.99, recall >= 0.80 | CRA |

**Acceptance obligation CRA-023.A** (only after every clause above is ACCEPTED):

- `[CRAr]` ambiguous abbreviations, same-name entities, conflicting identifiers and wrong high-confidence matches. Merge then split across restart and compare every edge/evidence/reference with the original. Denied/rejected candidates must never appear as accepted facts.
- `[MERGED]` Merge two entities, query unified properties, split, and verify the original state is restored exactly (AGG).
- `[GN]` With the structural model unavailable, candidates list only deterministic and lexical features and the response names the missing feature.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-024. Typed Query, Federation and Semantic Planning

*Aggregated title: Cost-Based Federated Query Engine (SPARQL 1.1, ANSI SQL & openCypher)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/016/017/019/031 | F (Usable value) | M5 | G06, G13 | ONT-002, ONT-003 | I2, I3 | INV-03, INV-16, INV-17, INV-18, INV-19, INV-21, INV-23, INV-26, INV-27, INV-28, INV-29, INV-33, INV-34, INV-35, INV-42 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/016/017/019/031. Sources G06/G13 and INV-18/19/21/23/27/28/29/35.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-024.1** `[CRAr]` Publish an exact grammar/capability manifest per dialect/backend: supported EQL/EOQL/OSQL subsets, qualified SPARQL and optional SQL/Cypher/Gremlin/GQL adapters. A language name or exported template is not an executable implementation.
- **CRA-024.2** `[CRAr]` Use typed parsed plans and parameterization; reject unsupported constructs and unauthorized operations. No concatenated raw user strings enter privileged backend code.
- **CRA-024.3** `[CRAr]` Provide validate/explain/cost/profile/execute/cancel with actual execution information, bounded depth/rows/time and source budgets. Explain output must correspond to the actual plan and reasoning mode.
- **CRA-024.4** `[CRAr]` Implement qualified OBDA/federation with source auth delegation, null/bag/set/type semantics, join pushdown, partial-source outcomes, snapshot/freshness and schema-drift handling.
- **CRA-024.5** `[CRAr]` Scope templates/history/results and caches; redact sensitive literals. Prevent unauthorized source or graph selection and export of hidden intermediate facts.
- **CRA-024.6** `[CRAr]` Separate warmed endpoint benchmarks from CLI startup/setup. Compare materialized and virtual results on declared semantics, not only query syntax.
- **CRA-024.7** `[OCA]` SPARQL 1.1 endpoint `GET/POST /sparql` per the SPARQL 1.1 Protocol, executed on a qualified RDF backend or translated to the LPG plan; passes the W3C protocol tests in scope; unbounded property paths are rejected with a clear error, never hang.
- **CRA-024.8** `[AGG]` Optional adapters, each with an exact grammar manifest: ANSI SQL views over the ontology (DataFusion/Trino candidates), openCypher/GQL over the property projection, GraphQL generated from shapes (extending `schema_gen.py`).
- **CRA-024.9** `[AGG]` Default budgets: deadline 30 s, memory 4 GiB per query, 10,000 rows per page, traversal depth 3; tenant quotas may only lower them; budgets reuse the existing `token_budget/` mechanism where applicable.
- **CRA-024.10** `[OCA]` BI connectivity: Tableau and Power BI connect through the SQL or SPARQL interface (acceptance test with a recorded session).
- **CRA-024.11** `[OCA]` RDF backend port (ONT-003): Apache Jena Fuseki reference, GraphDB certified option; a customer's existing GraphDB is targetable by configuration alone.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| query deadline | 30 s | CRAr |
| query memory | 4 GiB | AGG |

**Acceptance obligation CRA-024.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independent result corpus covering optional/join/null/cardinality/path/aggregate/order/limit cases, source failures and injection. Run against real qualified backends; unsupported dialect constructs must fail clearly. Exercise cost limit and cancellation with backend resource release.
- `[MERGED]` SP2Bench in-scope queries run with none exceeding 30 s; a federated query joining local Jira nodes with virtualized Snowflake tables returns correct results within the deadline (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A language name in an exported template list.

### 7.6 Module M6 — Retrieval, AI, actions and temporal knowledge

#### CRA-025. Search, Embeddings and Projection Fidelity

*Aggregated title: Tenant-Scoped Vector Similarity & Hybrid Search Projections*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/010/018/023/031 | F (Usable value) | M6 | G12 | — | — | INV-09, INV-10, INV-12, INV-19, INV-39 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/010/018/023/031. Sources G12 and INV-10/39/44/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-025.1** `[CRAr]` Version keyword/vector indexes by scope, source/ontology/policy revision, provider/model/tokenizer, dimension, normalization and distance metric.
- **CRA-025.2** `[CRAr]` Distinguish deterministic hashing fixtures from real semantic providers. Provider-disabled/unavailable or dimension mismatch cannot silently populate a production semantic index with hashing or zeros.
- **CRA-025.3** `[CRAr]` Enforce permission filtering at candidate generation and final delivery, with scoped caches and policy-epoch revocation. Do not retrieve unrestricted candidates into externally visible prompts or diagnostics.
- **CRA-025.4** `[CRAr]` Support resumable indexing, deletion, model re-embedding, shadow index evaluation and atomic cutover/rollback. Keep watermarks and explicit stale/unavailable states; projections rebuild from authoritative records.
- **CRA-025.5** `[CRAr]` Evaluate recall@k/nDCG/latency by domain/language and ACL selectivity using a labelled corpus. Record corpus splits and model/config changes; do not use graph proximity as relevance gold automatically.
- **CRA-025.6** `[AGG]` Configurable dense providers (local sentence-transformers models or approved external) plus BM25 sparse retrieval; fusion by Reciprocal Rank Fusion (k = 60 default) with optional graph-centrality signal; vector stores (Qdrant or pgvector candidates) partitioned by tenant.
- **CRA-025.7** `[RES]` The deterministic hashing embedder is renamed and labelled `test-hashing`; the production profile refuses it at startup.
- **CRA-025.8** `[GN]` Graph-structure embeddings (CRA-044) and text embeddings are distinct index families with separate metadata (model, snapshot, dimension, metric) under CRA-025.1; similarity search never mixes vectors from different families or model versions.
- **CRA-025.9** `[GN]` The hash-based vectors of `packages/eoip/gnn/engine.py` (`_deterministic_vector`, `embed_node2vec`, `embed_transe`) fall under CRA-025.7: removed from production paths, retained only as the `HashBaseline` test fixture and refused by the production profile at startup (X-40).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| RRF k | 60 | RES |

**Acceptance obligation CRA-025.A** (only after every clause above is ACCEPTED):

- `[CRAr]` real configured provider, missing provider, vector shape errors, source delete/ACL change, re-embedding crash and rollback. Demonstrate no cross-tenant vector neighbor/count/answer leakage and correct read-back after restart/rebuild.
- `[MERGED]` Vector search returns relevant chunks with exact document citations and no cross-tenant neighbours (AGG + CRAr).
- `[GN]` Starting the production profile with the hash embedder or graph hash vectors configured fails startup with a named error; a query mixing two embedding families is rejected.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-026. Evidence-Bound AI and Ontology Learning

*Aggregated title: Evidence-Bound GraphRAG & Calibrated Context Assembly*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/014/019/020/023/025/040 | F (Usable value) | M6 | — | ONT-006 | I9, I12, I13 | INV-04, INV-10, INV-11, INV-13, INV-14, INV-16, INV-34, INV-49, INV-51, INV-52, INV-53, INV-54 | X-15 | — |

**Base statement:** Priority P1. Depends on CRA-003/014/019/020/023/025/040. Sources INV-04/11/14/16/49/51/52/53/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-026.1** `[CRAr]` Keep extraction/classification/alignment/answer suggestions distinct from asserted facts and logical entailments. Record provider/model/prompt/tool/config revisions, evidence spans and policy context.
- **CRA-026.2** `[CRAr]` Build bounded authorized context with token budgets, evidence prioritization, freshness and conflicts. Emit clause-level evidence links to actual permitted source revisions; unknown/insufficient evidence produces abstention or explicit uncertainty.
- **CRA-026.3** `[CRAr]` Support true streaming/cancellation where configured with cleanup and accurate lifecycle. A graph event feed or simulated token timer is not answer streaming. Prevent partial cancelled output from being saved as an accepted complete answer.
- **CRA-026.4** `[CRAr]` Apply independent egress/DLP policy before provider calls. No unapproved endpoint/model downloads or external linting services in no-egress mode; record provider usage/cost without leaking raw data.
- **CRA-026.5** `[CRAr]` Treat retrieved documents and tool outputs as untrusted data. Prompt instructions cannot grant tools, alter trusted scope or bypass publication/action approval.
- **CRA-026.6** `[CRAr]` Evaluate factual/evidence correctness, abstention, prompt-injection resistance, calibration, domain/language coverage and quality drift against held-out data. Do not call a raw classifier score a probability without calibration evidence.
- **CRA-026.7** `[AGG]` GraphRAG pipeline: vector entry points -> bounded multi-hop traversal (default depth 2, max 200 nodes) -> ACL pruning -> context assembly; every sentence cites a `CanonicalAssertion` ID and an `EvidenceLocator`.
- **CRA-026.8** `[RES]` Abstention: when evidence is insufficient or calibrated confidence is below the configured threshold the answer states that it cannot be answered from authorized knowledge. The AGG threshold 0.85 is the initial value only after calibration on the held-out set; gates are CRAr's evidence precision >= 0.98, coverage >= 0.95 and abstention >= 0.95 (X-15).
- **CRA-026.9** `[AGG]` Air-gapped deployments route generation only to self-hosted model servers (vLLM, Ollama or TGI candidates) with zero external traffic.
- **CRA-026.10** `[PRM]` Context-window governance per configured model: maximum input and output token limits come from the provider/model manifest and are recorded with the model revision; budgets are measured with that model's own tokenizer (character or word estimates are not budgets); a context that would exceed the limit is reduced by a declared policy (prioritize evidence, then deduplicate, then drop whole lowest-priority items) and never overflows silently or is cut mid-assertion.
- **CRA-026.11** `[PRM]` Reduction is disclosed: when authorized evidence is dropped to fit the window, the answer states that evidence was omitted and how many items, and offers the omitted list to the principal; an answer built from a reduced context is not labelled complete. Restricted evidence is filtered before budgeting so the budget and the omission count never reveal its existence.
- **CRA-026.12** `[PRM]` Each answer stores a `ContextManifest` (section 6) — ordered `assertion_id`/EvidenceLocator entries with token counts, template revision, retrieval parameters and the reduction applied — referenced by digest from the answer so the exact context can be rebuilt under the same authorization.
- **CRA-026.13** `[RES]` Self-hosted generation under the H-17 interim policy: the qualified air-gapped generation path uses CPU-capable inference runtimes (llama.cpp/Ollama-class candidates, subject to CRA-035 review); the GPU-oriented servers named in CRA-026.9 (vLLM, TGI) stay `UNQUALIFIED` until H-17; quality gates are measured on CPU reference hardware and latency is recorded against the CRA-036 manifest target, with model size chosen to meet them.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| traversal | depth 2, max 200 nodes | AGG |
| context reduction policy | prioritize -> deduplicate -> drop whole lowest-priority items | PRM |
| self-hosted generation runtime | CPU-capable (H-17 interim) | RES |

**Acceptance obligation CRA-026.A** (only after every clause above is ACCEPTED):

- `[CRAr]` real local or approved external model traces with actual responses, malicious documents, missing evidence, contradictory sources, unavailable provider and cancellation. Verify the cited span supports the claim and is visible to the current principal at delivery. No scripted canned answers qualify provider integration.
- `[MERGED]` Prompt-injection documents fail to hijack the model or leak unauthorized facts (AGG).
- `[PRM]` With authorized evidence exceeding the model context limit, the answer discloses the omission count, the context manifest reproduces the prompt token count with the model tokenizer, and no assertion is cut mid-statement; a restricted item never changes the budget or the disclosed count for an unauthorized principal.
- `[RES]` In an air-gapped, GPU-free environment the qualified CPU runtime produces a grounded, cited answer and its latency is recorded against the CRA-036 manifest target; selecting a GPU-only server reports `UNQUALIFIED`.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Scripted canned answers or a timer simulating token streaming.

#### CRA-027. Governed Actions and Write-Back

*Aggregated title: Two-Phase Operational Write-Back Outbox & Action Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/004/022/031/040 | G (Named sources, media and actions) | M6 | — | ONT-009 | — | INV-05, INV-33, INV-36, INV-41, INV-43 | — | H-03 |

**Base statement:** Priority P1. Depends on CRA-003/004/022/031/040. Sources INV-33/36/41/43.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-027.1** `[CRAr]` Define declarative action types, target source/capability, allowed argument schema, preconditions, risk class, execution scope, approval rules and compensation/read-back semantics.
- **CRA-027.2** `[CRAr]` Default all sources to read-only. Write-back and source-policy provisioning require explicit configuration, separate permissions and qualified vendor integration.
- **CRA-027.3** `[CRAr]` Bind approval to exact intent/arguments digest, source/base/policy revisions, principal/delegation, expiry and nonce. Reauthorize immediately before execution; reject modified/replayed/expired intents.
- **CRA-027.4** `[CRAr]` Persist intent/execution/outcome/compensation journals, enforce idempotency and expose honest partial/unknown state for uncertain remote outcomes. Read back the source-system effect before reporting confirmed success.
- **CRA-027.5** `[CRAr]` Provide dry-run/impact preview, cancellation before commit, irreversible-action warnings and authorized operator recovery. A graph transaction cannot compensate an external change by itself.
- **CRA-027.6** `[AGG]` `ActionIntent` (section 6) lifecycle: PROPOSED -> STAGED -> APPROVED -> EXECUTING -> COMPLETED | FAILED | COMPENSATED, plus `UNKNOWN_OUTCOME` for uncertain remote results.
- **CRA-027.7** `[OCA]` Action types are declared as SHACL action shapes (`OntologyAction`, ONT-009) with SHACL preconditions, declared effects (classes/properties mutated), target connector, approval policy keyed to the existing `AutonomyLevel` ladder (destructive actions require the human-controlled level, HCTL) and an immutable audit receipt.
- **CRA-027.8** `[AGG]` `Idempotency-Key` header (16-128 chars) is mandatory; approvals carry a signature, nonce and default 5-minute expiry; replay or parameter change after approval is rejected.
- **CRA-027.9** `[RES]` Route consolidation: canonical routes `POST /api/v1/actions/execute`, `GET /api/v1/actions`, `POST /api/v1/actions/{id}/approve`; OCA aliases `POST /ontology/actions/{id}/invoke` and `GET /ontology/actions` forward to them. Write-back stays disabled until decision H-03.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| approval expiry | 5 min | AGG |
| write-back | disabled (read-only) | CRAr |

**Acceptance obligation CRA-027.A** (only after every clause above is ACCEPTED):

- `[CRAr]` changed arguments, denied permission, revoked credential, stale source, duplicate request, remote timeout after commit and compensation failure. Demonstrate exactly one intended effect through vendor read-back and complete audit, not a returned 200 alone.
- `[MERGED]` Trigger an action, approve it, simulate a remote timeout after commit, observe idempotent retry, read-back confirmation and exactly one remote effect (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- An HTTP 200 from the target without read-back.

#### CRA-028. Temporal Knowledge, Impact and Simulation

*Aggregated title: Bitemporal Graph Navigation, Blast-Radius Simulation & Time Travel*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-010/019/023/031 | E (Governed knowledge) | M6 | G14 | — | — | INV-25, INV-36, INV-37, INV-38, INV-40 | — | — |

**Base statement:** Priority P1. Depends on CRA-010/019/023/031. Sources G14 and INV-25/36/37/38/40.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-028.1** `[CRAr]` Model valid time, transaction/observation time, corrections, retractions, source revision and lineage explicitly. Timestamp fields alone do not establish bitemporal query behavior.
- **CRA-028.2** `[CRAr]` Support authorized as-of queries, version diffs, provenance and bounded historical snapshots. Retention/hold/deletion rules constrain what history may be served.
- **CRA-028.3** `[CRAr]` Separate observed relationships, deterministic graph impact, heuristic paths, stochastic estimates and domain simulation outputs in both API and GUI.
- **CRA-028.4** `[CRAr]` Simulations require versioned model/assumptions/inputs, seed, uncertainty and validation protocol. Random-walk frequency is not a calibrated failure probability or a causal intervention estimate.
- **CRA-028.5** `[CRAr]` Preserve actual path/hop evidence and cost semantics; do not summarize a multi-hop result as a fabricated two-node explanation. Approval/execution of operational action remains CRA-027.
- **CRA-028.6** `[AGG]` Historical reads use an explicit `as_of` parameter on the query API (and an `eoip:asOf` service parameter for SPARQL, because standard SPARQL has no AS OF clause), returning the authorized state at that valid/transaction time.
- **CRA-028.7** `[AGG]` Deterministic graph algorithms (BFS, Dijkstra, PageRank, Tarjan SCC) replace heuristic random-walk summaries for impact paths (G14); existing `graph/paths.py`, `algorithms.py`, `community.py`, `process_mining.py` are reused and qualified.
- **CRA-028.8** `[AGG]` Blast-radius output lists impacted services, teams and processes with severity scores explicitly labelled heuristic unless a validated model exists.
- **CRA-028.9** `[GN]` Learned impact propagation (CRA-044) is returned as a proposed, labelled estimate beside the deterministic blast radius of CRA-028.7/028.8 with its dual-path status (CRA-045.3); it never replaces or reorders the deterministic result.

**Acceptance obligation CRA-028.A** (only after every clause above is ACCEPTED):

- `[CRAr]` late events, corrections, clock skew, merges/splits, permission changes and retention across historical reads. Repeat seeded runs, compare sensitivity/gold scenarios, cancel expensive work and ensure simulated facts cannot enter asserted production knowledge without review.
- `[MERGED]` A point-in-time query shows a since-deleted node in the historical view only to principals authorized at both times (AGG + CRAr).
- `[GN]` For a change event both the deterministic blast radius and the learned estimate are returned; a node present only in the learned estimate is labelled proposed and uncorroborated.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

### 7.7 Module M7 — Catalog/context and accessible GUI

#### CRA-029. Catalog, Lineage and Enterprise Context

*Aggregated title: Enterprise Context Layer & Data Catalog Projections*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/010/017/018/024/031 | E (Governed knowledge) | M7 | — | — | I18 | INV-18, INV-24, INV-28, INV-38, INV-39, INV-40, INV-42, INV-43, INV-44, INV-45 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/010/017/018/024/031. Sources INV-24/28/38/39/40/42/43/44/45.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-029.1** `[CRAr]` Maintain technical assets, business terms, owners, classifications, quality observations and lineage as typed linked entities with source/freshness and allowed scope.
- **CRA-029.2** `[CRAr]` Distinguish observed/base metadata, human curation and effective merged view; define field-level precedence, conflict and reset-to-source behavior. A human override cannot silently hide changed source truth indefinitely.
- **CRA-029.3** `[CRAr]` Parse lineage only for supported source/query semantics. Unknown/dynamic statements yield uncertainty and diagnostics, not guessed source-target edges.
- **CRA-029.4** `[CRAr]` Expose data-graph versus schema/meta-graph versus provenance/security graph views with stable links and correct object types. Do not relabel the same graph as different capabilities.
- **CRA-029.5** `[CRAr]` Federate external catalogs through public versioned APIs with authoritative ownership rules, mappings, duplicate prevention and deletion/ACL propagation.
- **CRA-029.6** `[AGG]` Three metadata layers: base (crawler-observed), edit (human curation), merged (effective view by documented precedence) with reset-to-source and conflict indicators; human edits survive later crawls without hiding changed source truth.
- **CRA-029.7** `[AGG]` Propagated classifications (Atlas pattern, INV-45): tagging an asset PII cascades along lineage to downstream columns/views/dashboards through an event trigger, recording provenance so removal reverses the cascade.
- **CRA-029.8** `[AGG]` Metadata projections compatible with OpenMetadata, DataHub and Apache Atlas public APIs.

**Acceptance obligation CRA-029.A** (only after every clause above is ACCEPTED):

- `[CRAr]` source rename after human override, stale owner, conflicting glossary, denied lineage source and failed projection. Show the effective value's supporting layer and revision, repair after replay and demonstrate permitted query results through real API/UI/MCP.
- `[MERGED]` A human description in the edit layer survives the next crawler run while the conflict indicator shows a changed source value (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-030. Modular, Accessible and Truthful GUI

*Aggregated title: Accessible Multi-View Enterprise UI Workbench (WCAG 2.2 AA)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001/003 and the domain requirement exposed by each screen | F (Usable value) | M7 | G15 | — | — | INV-01, INV-03, INV-04, INV-05, INV-06, INV-08, INV-09, INV-28, INV-32, INV-38, INV-50, INV-51 | — | — |

**Base statement:** Priority P1. Depends on CRA-001/003 and the domain requirement exposed by each screen. Preserve [GUI-UIX-implementation-plan.md](GUI-UIX-implementation-plan.md) and later approved GUI requirements.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-030.1** `[CRAr]` Deliver complete task routes for source discovery/configuration/runs, ingestion review, ontology/vocabulary authoring, validation/reasoning, graph/entity/evidence, query/answer, changes/impact, actions/jobs, governance, reports, settings and support. Reconcile all existing 27-screen obligations; no duplicate marketing shell.
- **CRA-030.2** `[CRAr]` Use shared typed API contracts, authorization/capability-aware navigation, route boundaries, cancellable requests and explicit loading/empty/partial/stale/denied/error/success states. Never populate unavailable administration panels with examples presented as real records.
- **CRA-030.3** `[CRAr]` Provide simple task forms plus expert model/query views over the same server state. Display exact revisions, consequences, validation and approval status; preserve unsupported model constructs instead of rewriting them through a simplified editor.
- **CRA-030.4** `[CRAr]` Keep graph/table/tree alternatives equivalent for inspection and supported actions. Bound graph scenes; support keyboard navigation, focus/selection identity, screen-reader naming, reflow and readable theme/contrast.
- **CRA-030.5** `[CRAr]` Target WCAG 2.2 AA across the supported product, with automated checks plus manual AT and usability qualification. Localize resources/formats, test pseudo-expansion/RTL, and honor reduced motion in CSS and JS/graph animation.
- **CRA-030.6** `[CRAr]` Version and scope theme/density/locale/white-label/plugin preferences. Safely validate brand assets and contrast, support preview/rollback and show only real controls backed by supported operations.
- **CRA-030.7** `[AGG]` Workbenches: Source Management; Ontology Modeler (bounded graph canvas plus expert Manchester-syntax editor); Knowledge Explorer; Ask AI with side-by-side evidence/citation panels; Action Governance (approval queues, dry-run diffs, audit timelines).
- **CRA-030.8** `[OCA]` Baseline audit of the existing 90+ React components and 146 ARIA attributes; add an i18n framework (currently zero i18n) with pseudo-locale and RTL tests.
- **CRA-030.9** `[AGG]` Automated checks: Playwright end-to-end and axe accessibility suites exposed as `npm run test:e2e` and `npm run test:a11y` (create the scripts if absent); no placeholder or mock records in production builds.

**Acceptance obligation CRA-030.A** (only after every clause above is ACCEPTED):

- `[CRAr]` real browser against real services and built artifacts across desktop/mobile, four supported themes, reduced motion, keyboard and manual AT. Complete source -> review -> publish -> ask -> evidence -> authorized export/action journeys with failure/restart cases. Screenshots alone do not qualify semantics, persistence, accessibility or usability.
- `[MERGED]` Zero automated axe violations at WCAG 2.2 AA on every route plus manual assistive-technology review records (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Screenshots alone.

### 7.8 Module M8 — Durability, operations, deployment and qualification

#### CRA-031. Durable Jobs, Publication and Event Delivery

*Aggregated title: Durable Distributed Jobs & Dead-Letter Queue (DLQ)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | B (Safe platform) | M8 | G16 | — | — | INV-12, INV-22, INV-29, INV-30, INV-31, INV-36, INV-39, INV-41, INV-44, INV-45, INV-47 | — | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Sources G16 and INV-12/25/29/30/31/36/39/41/44/45.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-031.1** `[CRAr]` Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status. No process-local state as the only job authority in real deployments.
- **CRA-031.2** `[CRAr]` Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/reconciliation and expose incomplete states.
- **CRA-031.3** `[CRAr]` Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer credentials in URLs.
- **CRA-031.4** `[CRAr]` Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue authority and audit.
- **CRA-031.5** `[CRAr]` Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on the selected real durable backend.
- **CRA-031.6** `[AGG]` All jobs live in a durable database queue; workers hold leases with heartbeats every 10 s (lease TTL 30 s); an expired lease is reclaimed from the last valid checkpoint.
- **CRA-031.7** `[AGG]` Repeatedly failing payloads move to a governed DLQ with redacted diagnostics (stack trace with secrets removed), reason, attempt count and replay authority.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| heartbeat / lease TTL | 10 s / 30 s | AGG + RES |

**Acceptance obligation CRA-031.A** (only after every clause above is ACCEPTED):

- `[CRAr]` kill process/network/storage at each commit boundary; race two workers; replay a DLQ item; cancel and revoke scope mid-job. Demonstrate expected published effects, event sequence, cursor and restored job state using independent read-back.
- `[MERGED]` `tests/unit/test_job_queue_tenancy.py` and `tests/integration/test_durable_jobs.py` (create if absent) pass on the real durable backend, including two-worker races (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-032. Observability and Operational Truth

*Aggregated title: OpenTelemetry Tracing, Prometheus Metrics & Audit Observability*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/003/031 | B (Safe platform) | M8 | — | — | — | INV-44 | — | — |

**Base statement:** Priority P0. Depends on CRA-001/003/031. Sources INV-39/44/45 and all D16 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-032.1** `[CRAr]` Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and stage timings.
- **CRA-032.2** `[CRAr]` Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference amplification and model cost/quality. Unknown/stale telemetry is distinct from zero/healthy.
- **CRA-032.3** `[CRAr]` Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query literals/raw prompts unless explicitly authorized under retention policy.
- **CRA-032.4** `[CRAr]` Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success health endpoints.
- **CRA-032.5** `[CRAr]` Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry alone.
- **CRA-032.6** `[AGG]` Prometheus metrics (bounded labels): `eoip_ingestion_triples_total{source,status}`, `eoip_shacl_validation_duration_seconds{shape_id,conforms}`, `eoip_query_execution_duration_seconds{dialect}` (tenant only in access-controlled traces, not unbounded labels), `eoip_reasoning_amplification_ratio{ruleset}`, `eoip_acl_derivation_pruned_triples_total`, `eoip_outbox_action_lag_seconds{target_system}`.
- **CRA-032.7** `[AGG]` Every API response carries a W3C `traceparent`; security-relevant events (login, permission change, ontology merge, action execution) emit structured JSON audit records with principal, timestamp, action and payload digest.
- **CRA-032.8** `[OCA]` Alerting rules (currently absent) are defined for queue age, projection/policy lag, connector failure, validator unavailability and outbox lag, each linked to a runbook.

**Acceptance obligation CRA-032.A** (only after every clause above is ACCEPTED):

- `[CRAr]` trigger a real failed connector, timeout validator, stuck lease and policy-stale index. Confirm trace correlation, correct alert/state and no secrets in logs/metrics/bundles. Validate observed metric values against independent counters/workload timestamps.
- `[MERGED]` `/metrics` conforms to the Prometheus text format; a sampled request's `traceparent` resolves to a complete trace (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Initialized example metrics or an always-200 health endpoint.

#### CRA-033. Backup, Restore and Failure Recovery

*Aggregated title: Enterprise Backup, Point-In-Time Recovery (PITR) & Disaster Recovery*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-018/031/032/040 | H (Deploy and migrate) | M8 | — | — | — | INV-12, INV-20, INV-23, INV-25, INV-37, INV-45 | X-09 | — |

**Base statement:** Priority P0. Depends on CRA-018/031/032/040. Sources INV-12/20/23/25/37/45 and D18 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-033.1** `[CRAr]` Inventory authoritative state: canonical graph, control database, ontology/import/release packages, raw references, identity/policy, outbox/cursors, secrets/KMS recovery metadata and rebuild watermarks.
- **CRA-033.2** `[CRAr]` Define consistent encrypted backups/snapshots and retention for each supported deployment/backend, with access controls, immutability where appropriate and off-site failure separation.
- **CRA-033.3** `[CRAr]` Implement restore into a clean environment with revision/checksum/query/ACL consistency checks and projection rebuild. Restore secrets through the approved process, not by copying plaintext into bundles.
- **CRA-033.4** `[CRAr]` Measure P1 RPO <=15 min and RTO <=4 h for the declared tested failure model; document observed values, exceptions and exact data loss. Do not infer P2/region HA from a local restore.
- **CRA-033.5** `[CRAr]` Rehearse partial backup failure, corrupt snapshot, lost key, concurrent writes, API/worker restart and failed upgrade. Fence old writers and prevent event replay from resurrecting deleted/revoked records.
- **CRA-033.6** `[AGG]` Online non-blocking snapshots plus transaction-journal replay provide point-in-time recovery; default PITR window 30 days, shortened automatically where retention/deletion policy requires.
- **CRA-033.7** `[RES]` P1 objectives RPO <= 15 min and RTO <= 4 h (CRAr). The AGG figure 'RTO <= 4 h for a 500M-triple restore' is a P2 qualification target, not a P1 claim (X-09).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| PITR window | 30 days (policy-limited) | AGG |

**Acceptance obligation CRA-033.A** (only after every clause above is ACCEPTED):

- `[CRAr]` timed independent restore with business queries, ontology revisions, source cursors and adversarial authorization checked after recovery. An archive file or successful backup API response alone is not acceptance.
- `[MERGED]` Automated drill: snapshot, simulate store corruption, restore, verify graph, query, ACL and revision consistency (AGG + CRAr).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A successful backup API response.

#### CRA-034. Migration, Portability and Rollback

*Aggregated title: Migration CLI & Zero-Downtime Cutover Tooling*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-016/017/018/022/033/035 | H (Deploy and migrate) | M8 | — | ONT-001, ONT-017 | I10 | INV-06, INV-14, INV-15, INV-16, INV-26, INV-32, INV-33, INV-34, INV-35, INV-40 | — | — |

**Base statement:** Priority P1. Depends on CRA-016/017/018/022/033/035. Sources INV-01/15/16/25/26/32/34/35/40.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-034.1** `[CRAr]` Implement documented export/convert/validate/compare/replay/cutover/rollback tooling using the existing CLI conventions, with dry-run and explicit source/target scope. Do not document nonexistent executable commands as available.
- **CRA-034.2** `[CRAr]` Preserve source IDs/IRIs, blank-node semantics, literals/languages/datatypes, named graphs, edge assertions, provenance, ACL/retention and ontology history to the declared fidelity profile.
- **CRA-034.3** `[CRAr]` Generate a feature/loss/unsupported ledger and source-target reconciliation counts plus independent semantic/query comparisons. Never declare migration lossless when required constructs are dropped/coerced.
- **CRA-034.4** `[CRAr]` Stage and shadow-read from a pinned source watermark; replay deltas including ACL/delete events. Bind cutover approval to exact source, mapping, target and policy revision.
- **CRA-034.5** `[CRAr]` Support rollback of routing and compatible data/projections, with separately governed external-action compensation. Retain source until qualified restore/query/ACL checks pass.
- **CRA-034.6** `[AGG]` Design the `eoip-migrate` CLI (status PROPOSED until implemented): `discover --source <uri>`, `export --output <path>` (canonical Turtle/N-Quads with SHA-256 manifest), `validate --input <path>`, `compare`, `replay`, `cutover`, `rollback`; documentation must not present it as available before it exists.
- **CRA-034.7** `[AGG]` Eight-stage protocol: discovery and pin; format extraction with hashes; mapping synthesis with loss analysis; staged loading; semantic-equivalence verification with golden queries; CDC catch-up; atomic cutover; rollback window (default 14 days, read-only shadow source).
- **CRA-034.8** `[OCA]` R2RML/RML imports from Ontop, Morph-KGC and RMLStreamer users translate into CML/IR (ONT-017) with unsupported constructs reported.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| rollback window | 14 days | AGG |

**Acceptance obligation CRA-034.A** (only after every clause above is ACCEPTED):

- `[CRAr]` migrate a standards ontology and a named property-graph corpus through two qualified stores; compare independent output. Inject mapping failure, drift, denied record, partial cutover and rollback. Run on isolated synthetic/licensed data, never customer production by default.
- `[MERGED]` Synthetic migration of a 50M-triple GraphDB-format corpus through `eoip-migrate` yields zero dropped triples within the declared fidelity profile and zero golden-query divergence (AGG, synthetic data only).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-035. Commercial Packaging and Supply-Chain Compliance

*Aggregated title: Supply-Chain Compliance, SBOM & Licensing Isolation*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/002 | B (Safe platform) | M8 | G17 | — | I11, I19 | INV-02, INV-05, INV-07, INV-10, INV-13, INV-15, INV-21, INV-23, INV-28, INV-32, INV-35, INV-45, INV-46, INV-47, INV-49, INV-50, INV-52, INV-54, INV-55 | X-01, X-02, X-16, X-21, X-30 | H-04 |

**Base statement:** Priority P0. Depends on CRA-001/002. Sources G17 and INV-02/05/13/15/21/32/35/46/49/50/54/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-035.1** `[CRAr]` Preserve proprietary EOIP-owned licensing and upstream component rights. Do not relabel third-party files or assume all files in an owned directory are owned.
- **CRA-035.2** `[CRAr]` Produce exact shipped SBOMs and license/notices/source-obligation records for Python, npm/browser bundles, VSIX, OS/container packages, JVM/WASM/native engines, plugins, models, datasets, vocabularies and assets.
- **CRA-035.3** `[CRAr]` Resolve GPL/AGPL/LGPL/OEM/embedding/redistribution and data/model terms for the actual integration and both SaaS/installed profiles. Existing `extract-msg` and ownership/contract questions require explicit resolution, not automated green status.
- **CRA-035.4** `[CRAr]` Sign/hash release artifacts and plugin packages, retain build provenance and dependency locks, and make notices available online and offline as appropriate. An installed dependency list is not proof of notices shipped to customers.
- **CRA-035.5** `[CRAr]` Qualify installation/upgrade/uninstall and air-gap operation with no unapproved runtime downloads. Entitlements must disable unavailable modules truthfully without granting data access.
- **CRA-035.6** `[AGG]` Generate CycloneDX or SPDX SBOMs for Python, npm/browser bundles, containers, JVM workers, models and datasets with tools such as syft and a license checker; CI fails on unapproved licenses.
- **CRA-035.7** `[OCA]` Copyleft policy: GPL/AGPL code is never linked into or bundled with the distributed core; GPL/AGPL servers (Neo4j Community GPLv3, Virtuoso OSE GPLv2) are reachable only over network protocols; WebProtégé is not integrated; HermiT (LGPL) is an optional separately installed plugin; TerminusDB is blocked pending Legal; SNOMED-CT is customer-provided only.
- **CRA-035.8** `[OCA]` Dependency decision table (section 13) is the authoritative allowlist input to the CI license gate; every row cites the exact artifact and license snapshot.
- **CRA-035.9** `[GN]` The numerical stack (section 13 rows for numpy, scipy, scikit-learn, torch, torch-geometric, transformers, sentence-transformers, snntorch) enters the SBOM per tier; CUDA-dependent `nvidia-*` packages are excluded from every artifact EOIP distributes (decision H-16 accepted: not redistributable); DGL and networkx are not added.

**Acceptance obligation CRA-035.A** (only after every clause above is ACCEPTED):

- `[CRAr]` inspect actual wheel/image/browser/VSIX/air-gap artifacts and compare embedded inventories/notices with SBOM. Tamper with a plugin/artifact and reject activation. Obtain documented legal/owner approvals; agent-written licensing documents alone cannot clear distribution rights.
- `[MERGED]` `syft` (or equivalent) SBOM of the built image matches the dependency decision table; a test dependency with an AGPL license fails the CI gate (AGG + OCA).
- `[GN]` The SBOM of the default CPU image contains no `nvidia-*` package; adding one to any distributed build fails the license gate.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- An installed dependency list without shipped notices.

#### CRA-036. Correctness, Performance and Scale Qualification

*Aggregated title: Performance, Scale & 500M Triple Scale Qualification*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | the feature under qualification and CRA-001/032/037 | I (Independent acceptance) | M8 | G18 | ONT-020 | I3 | INV-11, INV-13, INV-14, INV-17, INV-18, INV-19, INV-20, INV-21, INV-22, INV-27, INV-29, INV-30, INV-31, INV-35, INV-36, INV-53, INV-54 | X-05, X-06, X-07, X-32 | H-01 |

**Base statement:** Priority P0. Depends on the feature under qualification and CRA-001/032/037. Sources G18 and all D06/D14/D22 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-036.1** `[CRAr]` Implement a reproducible workload harness with pinned dataset/generator/license, seed, expected answers, hardware/OS/runtime, engine/config and built-artifact identity.
- **CRA-036.2** `[CRAr]` Qualify P0 then P1 then P2 separately using the research profiles. Count asserted/inferred triples, raw/index/vector/history bytes, replicas and cold/hot residency independently.
- **CRA-036.3** `[CRAr]` Measure p50/p95/p99, successful/failed/cancelled operations, throughput, source/index lag, peak resources, amplification and cost units. Include cold/warm trials, concurrency, skew, ACL selectivity, updates/deletes and failure/restart.
- **CRA-036.4** `[CRAr]` Enforce the selected profile's point-read, bounded graph and approved-query targets without suppressing errors or weakening semantics/security/durability. Do not extrapolate a 1M memory fixture to 500M production capacity.
- **CRA-036.5** `[CRAr]` Run independent oracle/differential semantic checks before timing and retain at least three repeated measured trials with variability. Competitive published claims require equivalent semantics/features/hardware and license/publication review.
- **CRA-036.6** `[CRAr]` Evaluate parser/OCR/linking/RAG/simulation quality with declared labelled corpora and task-specific thresholds. Use section 4's selected defaults for listed tasks; new simulation/domain/language profiles require explicit additional thresholds before qualification, not arbitrary universal accuracy promises.
- **CRA-036.7** `[OCA]` Benchmark suites with committed generator commands, fixed seeds and expected-output hashes under `tests/benchmarks/ontology/` (ONT-020): LUBM (load >= 50k triples/s; Q1-Q14 p95 < 500 ms), BSBM (>= 1,000 QMpH at 100M triples), SP2Bench (no query > 30 s at 50M), SHACL throughput, classification, round-trip fidelity, CML throughput.
- **CRA-036.8** `[RES]` Binding latency gates are the CRAr profile targets (P0/P1/P2). AGG/OCA stricter numbers (point read p95 < 20 ms at P1/P2; P2 bounded 2-hop p95 < 250 ms; ingestion > 50,000 triples/s at P2) are stretch objectives recorded in the manifest; they become binding only by decision H-01 (X-05, X-06).
- **CRA-036.9** `[AGG]` Sustained 4-hour load test (wrk and/or Locust) per profile with memory-stability checks; CI regression gate fails on > 10% p95 latency regression versus the last accepted run (OCA).
- **CRA-036.10** `[GN]` Learned-model qualification follows CRA-044.5: primary metrics, the five mandatory baselines, calibration error and at least three seeded trials with variability are part of the benchmark manifest; results without baselines do not qualify.

**Acceptance obligation CRA-036.A** (only after every clause above is ACCEPTED):

- `[CRAr]` raw machine-readable results and independent expected-answer checks bound to manifests. Any wrong answer, leakage, required timeout or missing artifact fails the corresponding gate even when median latency is fast. Vendor benchmark PDFs are comparison evidence, not EOIP execution results.
- `[MERGED]` Machine-readable benchmark report with raw trials, oracle checks and manifests stored as receipts (AGG + CRAr).
- `[GN]` Model benchmark receipts contain the baseline rows and three seeded trials with variability.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- Vendor benchmark PDFs; a single warm run.

#### CRA-037. Independent QA and Evidence Verification

*Aggregated title: Independent Test Oracles & Regression Prevention*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001 and each changed feature | I (Independent acceptance) | M8 | — | ONT-019 | — | INV-07, INV-46, INV-47, INV-48, INV-49 | X-18 | — |

**Base statement:** Priority P0. Depends on CRA-001 and each changed feature. Sources all INV IDs and explicit attachment completion instruction.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-037.1** `[CRAr]` Maintain unit/property/fuzz, differential semantics, contract, real-backend/vendor integration, security/tenancy, real browser, migration/restore, chaos and performance suites with scope labels.
- **CRA-037.2** `[CRAr]` Separate mock tests from actual integration; independently author gold fixtures/oracles so implementation and expected output do not share the same faulty helper. A code change that only alters expected values is not proof of correctness.
- **CRA-037.3** `[CRAr]` Build once and verify the exact promoted artifact in each supported deployment/backend/profile, with actual persistence and negative cases. Development-server checks are not release-artifact acceptance.
- **CRA-037.4** `[CRAr]` Validate source stability, artifact freshness/hashes, exit codes, skip/error counts, fixtures/environment and review records. Missing/invalid/stale/contradictory evidence fails closed.
- **CRA-037.5** `[CRAr]` Perform manual domain, security, accessibility/AT, usability, operations and legal reviews where automated evidence is insufficient. Record reviewer/date/scope, defects and remediation, not a blanket approval checkbox.
- **CRA-037.6** `[CRAr]` On concurrent source changes, preserve edits and report the run as unbound; restart affected services and rerun relevant qualification on a stable revision. Historical passes remain historical.
- **CRA-037.7** `[AGG]` Property-based fuzzing (Hypothesis) of parsers, serializers, chunkers and query planners; mutation testing on semantic core modules.
- **CRA-037.8** `[RES]` Hygiene thresholds from AGG (line coverage >= 85% for `packages/eoip`, mutation score >= 80% on semantic core) are CI hygiene gates only; meeting them never constitutes acceptance evidence (X-18).
- **CRA-037.9** `[AGG]` Zero-skip policy: CI fails when a required test is skipped, xfailed without an open defect ID, errors or times out.
- **CRA-037.10** `[OCA]` Track and reduce test collection time (currently 60-120 s) and quarantine known pre-existing failures with tracked IDs rather than deleting them.
- **CRA-037.11** `[GN]` Anti-stub probes (CRA-044.3) are a required QA layer for every learned component, including retrieval embedders and rerankers; the probe harness has its own negative test and must fail the hash stub.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| coverage hygiene | >= 85% | AGG |
| mutation hygiene | >= 80% | AGG |

**Acceptance obligation CRA-037.A** (only after every clause above is ACCEPTED):

- `[CRAr]` deliberately tamper with a result, reuse stale artifacts, skip a required test, run against memory instead of production backend, edit source mid-run and fail a negative case. The gate must refuse acceptance each time. Verify every claimed ACCEPTED clause can be independently reproduced/read back.
- `[MERGED]` The gate refuses acceptance when a required test is skipped, a receipt is tampered, an artifact is stale or the source changed mid-run (CRAr + AGG).
- `[GN]` Substituting the hash stub for a trained model in CI makes the gate refuse acceptance.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-038. Support, Service Objectives and Operator Readiness

*Aggregated title: Support Runbooks, SLA Enforcement & Disaster Drills*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-032/033/035/037 | I (Independent acceptance) | M8 | — | — | I11 | — | X-08 | H-08 |

**Base statement:** Priority P1. Depends on CRA-032/033/035/037. Sources D21 gaps and research playbooks.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-038.1** `[CRAr]` Define supported versions/deployments, lifecycle/deprecation, service ownership, incident severity, escalation and customer versus vendor responsibility.
- **CRA-038.2** `[CRAr]` Implement documented incident, scaling, upgrade, backup/restore, credential compromise, poisoned data/model and projection-lag playbooks with diagnostic prerequisites and stop/rollback conditions.
- **CRA-038.3** `[CRAr]` Treat 99.9% monthly availability and initial response objectives as engineering proposals until staffing, measurement, exclusions and signed contracts support them. Response is not resolution, and installed customer infrastructure is a separate responsibility boundary.
- **CRA-038.4** `[CRAr]` Produce redacted support bundles with authorization, consent, retention and no secrets/customer raw data by default. Provide offline documentation for disconnected customers.
- **CRA-038.5** `[CRAr]` Rehearse operational incidents and restore with someone other than the implementer where feasible, recording actual observations and unresolved failures. Agent role-playing is not operator sign-off.
- **CRA-038.6** `[AGG]` Runbooks: ingestion backlog/consumer lag, store memory exhaustion and query kill, compromised source credentials, inconsistent ontology rollback, stuck publication, split-brain recovery, policy-lag index.
- **CRA-038.7** `[AGG]` Design `eoip-admin support-bundle` producing an encrypted, redacted diagnostic bundle (logs, metrics, configuration) with consent and retention metadata.
- **CRA-038.8** `[RES]` Severity response objectives remain proposals until signed: CRAr (P1 1 h, P2 4 business hours, P3 2 business days) and AGG (P1 < 15 min 24x7, P2 < 1 business hour, P3 < 4 business hours, P4 < 1 business day) are presented side by side for decision H-08 (X-08).

**Acceptance obligation CRA-038.A** (only after every clause above is ACCEPTED):

- `[CRAr]` real drill of a source credential compromise, stuck publication and lost store. An authorized operator follows the runbook and proves recovery/denial targets from raw observations. Commercial/counsel approval of SLA and support schedules remains a human external gate.
- `[MERGED]` An operator who did not implement the system recovers a simulated split-brain within the runbook's target (AGG proposal 30 min) from raw observations.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-039. Public APIs, SDKs and Developer Ecosystem

*Aggregated title: Developer Platform: Python & TypeScript SDKs, OpenAPI & MCP Server*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001/002/003/035/037 | H (Deploy and migrate) | M8 | — | ONT-011, ONT-014 | I14 | INV-02, INV-05, INV-08, INV-10, INV-33, INV-39, INV-41, INV-44, INV-50 | — | — |

**Base statement:** Priority P1. Depends on CRA-001/002/003/035/037. Sources INV-08/10/33/39/41/44/50/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-039.1** `[CRAr]` Generate published OpenAPI/JSON schemas and Python/TypeScript SDKs from the composed real application contract. Version public APIs, errors, events and compatibility/deprecation independently from internal endpoints.
- **CRA-039.2** `[CRAr]` Expose authorized MCP tools with typed inputs/outputs, provenance and budgets. Tools cannot change trusted identity or obtain broader rights through natural-language arguments.
- **CRA-039.3** `[CRAr]` Provide plugin/connector templates, synthetic fixtures, conformance runner, supported-version tables and a documented qualification process. Uncertified community modules remain visibly unqualified.
- **CRA-039.4** `[CRAr]` Generate ontology/API/help documentation from exact signed release artifacts, sanitize authored content and support offline/no-egress generation. Follow LODE/WIDOCO version/license transitions explicitly if adopted.
- **CRA-039.5** `[CRAr]` Define contribution, vulnerability disclosure, ownership and marketplace policies consistent with proprietary core licensing and upstream obligations. Do not publish customer models/content as examples.
- **CRA-039.6** `[AGG]` Generated SDKs: TypeScript (proposed package `@eoip/sdk-typescript`) and Python (proposed `eoip-python`); names verified for availability and trademark before publication.
- **CRA-039.7** `[OCA]` MCP server (ONT-011) over existing `tools_contract/` and `sdk/` exposing ontology, graph and governed actions; actions invoked through MCP pass exactly the same autonomy, approval and policy gates as direct invocation.
- **CRA-039.8** `[OCA]` Offline Widoco-class HTML ontology documentation generator (ONT-014) producing cross-referenced specs with diagrams and provenance from signed releases; `GET /ontology/docs` serves them.

**Acceptance obligation CRA-039.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independently build a client and sample plugin from released schemas/templates, run a real scoped task and reject deprecated/incompatible/unauthorized calls. Compare generated docs/SDKs with actual runtime and artifact digest; a static schema file alone is insufficient.
- `[MERGED]` An external agent (Claude or LangGraph client) answers a business question through the MCP server and an attempted destructive action is held for approval (AGG + OCA).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A static schema file.

#### CRA-040. Privacy, Retention, Deletion and No-Egress Guarantees

*Aggregated title: Data Privacy, Right-to-be-Forgotten & Strict No-Egress Firewalls*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/010/018/031 | B (Safe platform) | M8 | — | — | — | INV-11, INV-24, INV-25, INV-37, INV-42, INV-43, INV-49, INV-51, INV-52 | — | — |

**Base statement:** Priority P0. Depends on CRA-003/010/018/031. Sources INV-13/24/25/37/42/43/49/51/52/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-040.1** `[CRAr]` Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/model/dataset/content licenses are distinct.
- **CRA-040.2** `[CRAr]` Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at the network boundary, not inferred from configuration.
- **CRA-040.3** `[CRAr]` Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. A deletion workflow must locate and process each according to retention/hold policy.
- **CRA-040.4** `[CRAr]` Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/access treatment; it is not an excuse to ignore erasure obligations.
- **CRA-040.5** `[CRAr]` Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal hold. Do not claim regulatory certification from a policy module name.
- **CRA-040.6** `[AGG]` Erasure cascade: a deletion request for a subject locates and processes every derivative across the eight graph planes (raw, canonical, schema references, provenance, lineage, policy, temporal, vector), caches, exports and backups under retention/hold policy, producing a scoped report.
- **CRA-040.7** `[AGG]` No-egress verification: a network socket monitor records zero external bytes during a full ingestion plus GraphRAG cycle in no-egress mode; allowed destinations are limited to configured enterprise systems.

**Acceptance obligation CRA-040.A** (only after every clause above is ACCEPTED):

- `[CRAr]` delete and revoke a subject/source while jobs and streams are active, restore/replay older state, then inspect every derivative and network log. Demonstrate retained held material is restricted and reported accurately, with reviewed retention/backup exceptions.
- `[MERGED]` After a GDPR purge, a deep sweep across graph, vector, cache and object store finds zero remaining records except documented held material (AGG).

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A policy module name or configuration flag.

### 7.9 Module M9 — Claims governance and research qualification

#### CRA-041. Truthful Positioning, Competitive Claims and Disclosure Governance

*Aggregated title: (new in combined specification)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001/035/036/037/042 | I (Independent acceptance) | M9 | F4, F5 | ONT-012 | I1, I3, I6, I11, I13, I15, I16, I17 | — | X-19, X-20 | H-05, H-12 |

**Base statement:** Priority P1. Depends on CRA-001/035/036/037/042. Sources OCA ONT-012, risk OR6, inversions I1-I20 'already won' list, OCA evidence caveat, OCA section 8.3 patent candidates, CRA section 1 'do not advertise superiority'.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-041.1** `[RES]` Maintain a versioned Claims Register in the repository (`docs/claims/claims-register.yaml`). Every externally visible statement about EOIP capability, standards conformance, performance, cost, security or competitive position has a claim ID, exact wording, scope (edition/profile/deployment), evidence references (ledger clause IDs, benchmark receipt digests, review records), owner, approval and expiry date.
- **CRA-041.2** `[RES]` No standards-conformance claim (RDF 1.1, JSON-LD 1.1, OWL 2 profile, SHACL Core, SPARQL 1.1, WCAG 2.2 AA) may be published until the corresponding requirements (CRA-016, CRA-019, CRA-020, CRA-024, CRA-030) and the round-trip certification gate (CRA-016 clause for ONT-019) are ACCEPTED for the declared profile. This closes risk OR6.
- **CRA-041.3** `[RES]` The seven inversions labelled 'already won' in the indicative analysis (I1, I3, I6, I13, I15, I16, I17) are hypotheses until re-verified on the pinned baseline commit with receipts. They may be positioned only with the scoped wording approved in the Claims Register; 'no competitor has this' wording requires a dated, sourced competitor review (CRA-042) and Legal approval.
- **CRA-041.4** `[RES]` The Ontology-as-Code positioning package (ONT-012) consists of: a factual capability description of the existing GitOps layer (branch, PR, review gate, semantic diff, impact analysis, migration-script generation, rollback receipts, semver computation, release packaging), a dated comparison table against TopBraid EDG, Protégé/WebProtégé and Chowlk/OnToology with source links, and a limitations section. It is published only after CRA-022 clauses covering those capabilities are ACCEPTED.
- **CRA-041.5** `[RES]` Competitor performance, TCO, pricing or revenue figures that originate from vendor or self-interested sources (for example negotiation-consultancy TCO claims) are marked UNVERIFIED and may not appear in customer-facing material unless independently verified, attributed and Legal-approved.
- **CRA-041.6** `[RES]` Patent-candidate disclosure control: the five candidates listed in OCA section 8.3 (semver from semantic diff; migration-script generation from ontology diff; hybrid per-rule materialize/virtualize reasoning with a cost model; AI-suggested declarative source-to-ontology mappings; combined structural plus embedding drift driving evolution proposals) are recorded in a restricted register. Public disclosure (docs site, blog, talk, open-source release, white paper) of their mechanisms is blocked until a recorded Legal decision exists for each (decision H-12).
- **CRA-041.7** `[RES]` Indicative scorecards (ontology-comparison-matrix.csv, the aggregated master matrix, EOIP self-scores 2.9/3.6/4.2) are internal planning aids. Any external use requires evidence-qualified rescoring under CRA-042 and must state the scoring method, date and evidence confidence.

**Acceptance obligation CRA-041.A** (only after every clause above is ACCEPTED):

- `[RES]` Attempt to publish (a) a SHACL conformance claim while CRA-020 is not ACCEPTED, (b) an 'already won' inversion without a receipt, (c) a competitor TCO figure marked UNVERIFIED, and (d) a document describing a patent-candidate mechanism without a Legal decision. The claims check (CI job over `docs/` and release notes) must block all four with specific reasons. Legal and Marketing review records exist for every published claim.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

#### CRA-042. Competitive Research Qualification and Maintenance

*Aggregated title: (new in combined specification)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001 | A (Truthful baseline) | M9 | — | — | — | — | X-22, X-23, X-24, X-25 | — |

**Base statement:** Priority P1. Depends on CRA-001. Sources CRA sections 2.2, 5, 6.1, 19 'remaining research'; competitive-research-matrix.csv (ND values); ontology-comparison-matrix.csv; AGG section 4 master matrix; conflict register X-01..X-33.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-042.1** `[RES]` Maintain one research record per tool family C01-C55 under `research/competitive/<id>.yaml`: tool family, category, reviewed baseline date, pinned product/edition/version or commit, license snapshot (file hash and URL), primary evidence URLs, 22 dimension scores each either 1-5 with written rationale and confidence, or `ND` with the missing evidence named.
- **CRA-042.2** `[RES]` Keep the three scoring datasets separate and labelled: evidence-qualified (competitive-research-matrix.csv, 7 scored dimensions, 15 ND), indicative (ontology-comparison-matrix.csv, all dimensions scored, 'not audited'), aggregated (AGG master matrix, all dimensions scored, unsourced). They must never be averaged, merged into one league table, or used to replace an ND value.
- **CRA-042.3** `[RES]` Resolve every item in the version and investigation register (CRA section 6.1): pin exact release, artifact checksum, source/license snapshot and lifecycle before any tool is procured, embedded, benchmarked or named as a certified backend.
- **CRA-042.4** `[RES]` Re-verify each conflict-register item marked RESEARCH (licenses for WebProtégé, LODE, TerminusDB, FIBO, schema.org, Openllet, extract-msg; gist size; vendor ownership changes) against primary sources and record the dated outcome. A verified outcome that changes a decision triggers a change to this specification through CRA-022-style review.
- **CRA-042.5** `[RES]` Perform hands-on qualification for every third-party engine EOIP will depend on or certify (at minimum rdflib, pySHACL, OWL API, ELK, Apache Jena/Fuseki, GraphDB as certified backend, Ontop, Morph-KGC, DeepOnto, spaCy, chosen OCR/ASR engines) using pinned artifacts, licensed evaluation rights and the CRA-036 harness; record results as receipts.
- **CRA-042.6** `[RES]` Record unavailable or contradictory sources (for example the OnToology site timing out, Fabric preview limits, vendor marketing scale claims) as explicit evidence gaps rather than negative findings or positive scores.
- **CRA-042.7** `[RES]` Refresh every research record at least every 6 months or on a major competitor release; each refresh produces a dated delta entry. Stale records (>6 months) are shown as STALE in the tracker and dashboard.

**Acceptance obligation CRA-042.A** (only after every clause above is ACCEPTED):

- `[RES]` Run the research-dataset validator: every score is an integer 1-5 with rationale or `ND` with a named gap; no record lacks a reviewed date; no tool named as a dependency/backend lacks a pinned artifact and license snapshot; conflict items marked RESEARCH have dated outcomes or remain OPEN. Introduce a fixture record with a blank score, an averaged score and an unpinned dependency; the validator must reject all three.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.

### 7.10 Module M10 — Probabilistic intelligence substrate and neuro-symbolic arbitration

Added in v3.1. These requirements own obligations no earlier requirement held: the numerical stack every probabilistic capability presupposes (G20), learned models over the graph planes with proof that they learned (G19), and the boundary between deterministic semantics and probabilistic AI named by the original prompt (G21). `EOIP-engg-doc-pkg/Graph-Neurons-requirements.md` (GN-REQ-v1) is the detailed engineering reference; section 19.7 maps every GN requirement to a clause here.

#### CRA-043. Numerical Compute Stack, Determinism and Hardware Profiles

*Aggregated title: (new in v3.1) Tiered Numerical Substrate for Probabilistic AI*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/002/035 | B (Safe platform) | M10 | G20 | — | — | — | X-39, X-42 | H-15, H-16, H-17 |

**Base statement:** Priority P0. Depends on CRA-001/002/035. Sources GN-010..GN-016 and G20. CRA-014 (OCR/ASR), CRA-023.6/023.7 (embedding and structural similarity, DeepOnto), CRA-025 (dense retrieval), CRA-026 (local models) and CRA-044 all presuppose a numerical stack the repository does not have.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-043.1** `[GN]` Introduce the numerical stack as four separately installable optional extras, never as core dependencies: N0 `numerics` (numpy, scipy, scikit-learn; installed-size budget <= 150 MB), N1 `neural` (N0 plus CPU-only torch and torch-geometric; installed-size budget <= 2.5 GB), N2 `neural-text` (N1 plus transformers and sentence-transformers), N3 `neural-research` (N1 plus snntorch; research environments only, never in customer profiles, bundles or images — H-15). Tiers compose through self-referencing extras with exactly one version constraint per package. `pip install -e .` must resolve to an unchanged package set, proven by diffing `pip freeze`.
- **CRA-043.2** `[GN]` CPU-only builds are the only builds EOIP distributes (decision H-16, accepted 2026-10-18: CUDA packages cannot be redistributed; `docs/decisions/ADR-H16-no-cuda-redistribution.md`). No `nvidia-*` package, CUDA runtime or CUDA-enabled torch build appears in any EOIP wheel, distribution lock file, offline bundle, container image or mirror, and EOIP documentation publishes no CUDA install command. A CUDA build the customer installs from upstream under their own NVIDIA terms is detected as `TORCH_CUDA`, reported as unqualified and never required.
- **CRA-043.3** `[GN]` Provide a hash-pinned lock file (`requirements-neural.lock` via `pip-compile --generate-hashes` or the project's equivalent) and an offline wheel bundle per supported platform and tier. Installation from the bundle succeeds on a network-isolated host, and no model weights are fetched at first run (CRA-014.3, CRA-040.2). The lock file, every bundle manifest and every image SBOM are scanned and must list zero `nvidia-*` packages (H-16).
- **CRA-043.4** `[GN]` Register each tier as capabilities (CRA-001). A missing tier is capability state `UNAVAILABLE`, returned as HTTP 503 `CAPABILITY_UNAVAILABLE` with the missing tier and its install command in `details` (X-39). Endpoints declare their minimum tier, so N0-only deployments keep metrics, baselines and embedding lookup working. Silent fallback to a non-learned heuristic or to hashing is prohibited (CRA-025.2).
- **CRA-043.5** `[GN]` Array discipline: float32 for stored and served vectors; float64 only for metric accumulation; no Python-level element loops in hot paths (similarity, normalization, aggregation, batching); `list[float]` only at serialization boundaries; every array crossing a module boundary is checked finite.
- **CRA-043.6** `[GN]` Determinism: a single seeding entry point seeds Python, numpy, torch and CUDA, enables deterministic algorithms where available, records any operation that fell back to a non-deterministic kernel, and stores the seed bundle and an environment capture (library versions, BLAS vendor, device, thread counts) in every training and evaluation receipt.
- **CRA-043.7** `[GN]` BLAS thread governance: `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` and `NUMEXPR_NUM_THREADS` are set together before numpy is first imported. Serving processes default to 1 thread per worker; training and batch workers to min(8, CPU count). The effective count is reported by the capability route.
- **CRA-043.8** `[GN]` Numerical stability: max-subtracted softmax, epsilon-guarded logarithms and normalizations, int64 node indices, and a documented result for empty inputs; no reduction returns NaN.
- **CRA-043.9** `[GN]` Memory and accelerator lifecycle: estimate peak memory before training or full-graph inference and refuse, naming a workable batch size, when the estimate exceeds 80% of available memory; release accelerator memory after each job; derive batch sizes from measured capacity, never hardcode them; record peak RSS and accelerator memory in performance receipts. All numerical and model work runs in CRA-002 `heavy` workers, never in the API process.
- **CRA-043.10** `[RES]` Qualify the platform matrix by CI jobs, not assertion: Linux x86_64 (N0-N2 required), Windows x86_64 and macOS arm64 (N0-N1 required), Linux arm64 (N0 required). No platform requires a GPU; a customer-provisioned GPU job, if run, is labelled unqualified and non-binding (H-17).
- **CRA-043.11** `[RES]` CPU-first qualification (decision H-15 accepted; H-17 open): every binding gate in sections 5.2 and 5.3 and in CRA-026, CRA-043 and CRA-044 is qualified on CPU-only reference hardware with no GPU visible to the process, and receipts record `device=cpu`. Results obtained with a GPU are recorded separately and are non-binding until H-17 is decided; a capability that meets its gates only with a GPU is `UNQUALIFIED` in CPU profiles. Interim policy: `docs/decisions/ADR-H17-gpu-availability.md`.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| distributed builds | CPU-only; zero `nvidia-*` packages (H-16) | GN |
| accelerator | none required; GPU unqualified until H-17 | RES |
| serving BLAS threads | 1 per worker | GN |
| training BLAS threads | min(8, CPU count) | GN |
| stored vector dtype | float32 | GN |
| memory refusal threshold | 80% of available | GN |

**Acceptance obligation CRA-043.A** (only after every clause above is ACCEPTED):

- `[GN]` In four isolated environments (no extras, N0, N0+N1, N0+N1+N2) the capability route reports the correct tier; core EOIP imports and serves in the empty environment; an N0-only endpoint returns 200 and an N1 endpoint returns 503 naming the tier. Two runs with the same seed in separate processes reproduce metrics within 1e-4 and a different seed changes them. An oversized job is refused before allocation. Offline installation from the wheel bundle succeeds with networking disabled. An oversubscription probe (concurrent inference with and without thread limits) is measured and recorded.
- `[GN]` The lock file, every offline bundle manifest and the default image SBOM list zero `nvidia-*` packages, and a fixture lock file containing one fails the licence gate; every acceptance run above executes on a host with no GPU visible and its receipt records `device=cpu`.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A dependency entry for torch that was never installed in a clean environment; GPU figures quoted from vendor documentation.

#### CRA-044. Learned Graph Intelligence over the Graph Planes

*Aggregated title: (new in v3.1) Neural Fabric — GNN, Transformer, Temporal, Convolutional, Generative and Spiking Models on Graphs*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/019/020/023/025/043/045 | F (Usable value) | M10 | G12, G19 | — | — | INV-19, INV-53 | X-34, X-35, X-36, X-37, X-38, X-40, X-41 | H-17 |

**Base statement:** Priority P1. Depends on CRA-003/019/020/023/025/043/045. Sources GN-001..GN-007, GN-101..GN-706, the two neural-architecture research inputs summarised in Graph-Neurons, and G19. Where GN-REQ-v1 and this document differ, this document governs (X-34..X-41).

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-044.1** `[GN]` Remove the hash-based graph embedding stand-ins from production paths. `GraphEmbedder._deterministic_vector`, `embed_node2vec` and `embed_transe` in `packages/eoip/gnn/engine.py` compute SHA-256 digests of identifiers and walk strings with no objective, optimiser or learning. Retain them only as the `HashBaseline` test fixture, and keep `get_gnn_engine()` importable as a thin re-export of the new implementation so existing callers do not break (X-40).
- **CRA-044.2** `[GN]` Map the four graph levels of the research inputs onto the graph planes of section 8.2 — GL0 instance graph to planes 1-2; GL1 meta-graph to plane 3; GL2 living brain (the cross-source unified graph) to plane 2 across sources; GL3 enterprise ontology to plane 3 axioms and shapes; the temporal axis GLT to plane 7 — and train only on authorized, policy-epoch-bound snapshots of those planes. A parallel temporal store duplicating plane 2 is not permitted.
- **CRA-044.3** `[GN]` Every learned model passes four anti-stub probes before any quality claim: loss descent (final loss <= 70% of initial); parameter change (>= 90% of tensors move); label-permutation control (the true-label primary metric beats the permuted-label metric by >= 0.10 absolute); structural coherence (two automorphic nodes have embedding cosine >= 0.90). The probe harness must itself score the existing hash stub as failing all four.
- **CRA-044.4** `[GN]` Snapshot and split discipline: content-addressed snapshots; strictly event-time temporal splits validated on every batch, so a deliberately leaked edge raises; type-constrained negative sampling against `ontology/manifest.py:edge_endpoints_valid` as the default for every reported metric.
- **CRA-044.5** `[GN]` Evaluation discipline: AUPRC is primary for link prediction and anomaly detection and AUROC is never reported alone; Macro-F1 for node classification; time-filtered MRR for temporal prediction. Five baselines are reported beside every model on the same split: random, degree, common-neighbours/Adamic-Adar, `HashBaseline`, and the existing deterministic rule or traversal. A score becomes a probability only after calibration on the validation split with expected calibration error <= 0.10.
- **CRA-044.6** `[GN]` Core encoders: R-GCN with basis decomposition (defaults 2 layers, 128 hidden units, 30 bases) and inductive GraphSAGE for continuously ingested entities, the latter proven by embedding new nodes with an unchanged weight hash. A model that does not beat both the common-neighbours and rule baselines by >= 0.05 on the primary metric is recorded FAILED with its numbers, not shipped.
- **CRA-044.7** `[GN]` Bake-off-gated architectures, each promoted only on a measured margin over the R-GCN default on the same split and otherwise recorded FAILED: relational graph attention (attention weights retrievable per prediction); heterogeneous graph transformer (>= 0.03 on a fixture spanning >= 3 domains); GraphGPS-style local-plus-global transformer (>= 0.03 on tasks with shortest-path distance >= 4; no dense O(n^2) attention above 10,000 nodes); path-aware knowledge-graph attention; GRU/LSTM event encoders and temporal graph networks; recurrent event networks; ChebNet spectral filters for ontology structural anomalies (zero false positives on a clean control); ConvE completion (parameter efficiency measured, not cited); vision encoders feeding CRA-015 candidates.
- **CRA-044.8** `[GN]` Generative and spiking work: an adversarial plausibility discriminator may act as a write-path quality filter (precision >= 0.80 at recall >= 0.70; <= 5 ms per triple; flagged triples quarantined for review, never deleted; the ontology domain/range veto overrides the learned score) only after CRA-044.6 is ACCEPTED. Triple generators and spiking-network encoders are research-only, run in a sandbox tenant with an import-graph test proving no production dependency, and report measured efficiency on the hardware in use. "Not justified" is an acceptable recorded outcome.
- **CRA-044.9** `[GN]` Model lineage and lifecycle: models, embeddings and calibrators are registered with snapshot ID, code commit, seed bundle, environment, training-data scope and gate report, extending `packages/eoip/mlops/experiment_tracker.py`. Promotion requires every gate in clauses 3-6 plus the security and explainability gates; rollback restores the prior version and serving reflects it within 60 s. Graph-embedding vectors are a rebuildable plane-8 projection in the vector store chosen under CRA-025.6, partitioned by tenant (X-41).
- **CRA-044.10** `[GN]` Explainability: >= 95% of served predictions carry evidence paths, and a faithfulness probe shows that removing the identified evidence subgraph lowers the prediction score by >= 50%; otherwise the explanation is reported as not faithful.
- **CRA-044.11** `[GN]` Incremental operation and failure-mode guards: graph changes invalidate only the affected k-hop embeddings; retraining is triggered by measured drift, scheduled evaluation or quality degradation, not by every write. Oversmoothing (default depth 2; embedding variance measured at 2, 4 and 8 layers), oversquashing (long-range accuracy reported separately) and popularity shortcuts (degree baseline mandatory) are measured, not assumed away.
- **CRA-044.12** `[RES]` Every model output enters the knowledge model only as `knowledge_state=proposed` with `ModelLineage` (CRA-045). The GN-002 `AssertionStatus` is implemented as a mapping onto `KnowledgeState`, not as a parallel enum (X-34).
- **CRA-044.13** `[RES]` CPU feasibility (decisions H-15, H-17): every architecture records its training time, inference latency and peak memory on CPU reference hardware, and defaults are chosen for CPU (neighbour sampling where full-batch training misses its budget). An architecture that meets its bake-off margin or budgets only with a GPU is recorded `DEFERRED (H-17)` with its CPU numbers and is never promoted to a CPU profile; those numbers are inputs to H-17.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| R-GCN depth / hidden / bases | 2 / 128 / 30 | GN |
| negative sampling | type-constrained, ratio 1 | GN |
| primary link metric | AUPRC | GN |
| calibration ECE ceiling | 0.10 | GN |
| promotion lift | +0.05 over common-neighbours and rule baselines | GN |

**Acceptance obligation CRA-044.A** (only after every clause above is ACCEPTED):

- `[GN]` On the frozen reference snapshot: the anti-stub harness fails the existing hash stub on all four probes and passes the R-GCN model on all four; the receipt shows all five baselines beside the model with AUPRC primary; a deliberately leaked split raises; new nodes are embedded without a weight-hash change; a prediction appears only as a proposed assertion with lineage and evidence paths and never in an asserted-only query; removing its evidence subgraph at least halves its score; an unauthorized principal cannot infer a restricted node through embeddings, neighbour counts, latency or error differences (CRA-003); `grep -r _deterministic_vector packages/` finds it only under `tests/`.
- `[GN]` The R-GCN default meets its gates on CPU-only reference hardware (receipt `device=cpu`); every architecture recorded `DEFERRED (H-17)` carries its CPU measurements.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A checkpoint or headline metric without the five baselines and the anti-stub report; an AUROC figure on its own; a notebook result.

#### CRA-045. Deterministic–Probabilistic Boundary and Neuro-Symbolic Arbitration

*Aggregated title: (new in v3.1) Dual-Path Semantics — W3C Determinism plus Probabilistic AI*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/016/019/020/024/025/026/043 | F (Usable value) | M10 | G21 | — | I2, I18 | INV-19 | X-34, X-35, X-36 | — |

**Base statement:** Priority P0. Depends on CRA-003/016/019/020/024/025/026/043. Source: the closing instruction of the original attachment, `crarprompt.txt` — *"my architecture should be capable enough to handle deterministic semantics (W3C standard ontologies, schema enforcement) and probabilistic AI (vector embeddings, LLM context windows, and graph traversals)"* — and G21. Interpretation (binding): graph traversal is deterministic when executed as an exact algorithm (CRA-024, CRA-028.7) and belongs to the probabilistic pipeline when it assembles LLM context (CRA-026.7) or uses learned or sampled weights (CRA-028.4, CRA-044); the traversal result keeps its exactness label in both uses.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-045.1** `[PRM]` Classify every producer of knowledge or answers as deterministic (RDF parsing and serialization, SHACL validation, profile-qualified reasoning, exact query and traversal, deterministic mapping) or probabilistic (embeddings and similarity, LLM generation and extraction, learned graph models, OCR/ASR/vision, sampled or heuristic traversal, alignment suggestions). The class is part of each producer's capability registration (CRA-001) and appears in every result payload.
- **CRA-045.2** `[PRM]` Probabilistic output is never asserted directly. It enters as `knowledge_state=proposed` with `ModelLineage`, calibrated confidence where calibration exists, and evidence. Promotion to `asserted` requires deterministic validation — SHACL (CRA-020), profile and consistency checks (CRA-019), identity rules (CRA-023) — followed by the review policy of CRA-022. A promoted assertion keeps its probabilistic origin and its approver.
- **CRA-045.3** `[PRM]` Dual-path answering: wherever an exact deterministic path exists for a question (SPARQL/EQL query, bounded traversal, entailment check), it runs beside the probabilistic path and both results are returned with their producer class. Agreement is reported as `CORROBORATED`, disagreement as `DISPUTED` with both results and their evidence, and a probabilistic-only answer as `UNCORROBORATED`. Disagreement is shown to the user, never resolved silently in favour of either path.
- **CRA-045.4** `[PRM]` Deterministic constraints bound probabilistic proposals before display: a candidate that violates ontology domain/range, disjointness or a SHACL constraint is shown as rejected-by-constraint with the violated shape or axiom, not as a ranked suggestion.
- **CRA-045.5** `[PRM]` Separation holds in storage, query and export: asserted-only queries, the SPARQL endpoint and RDF exports exclude proposed statements unless the caller explicitly asks for them, and exported proposed statements carry their knowledge state and lineage in a named graph (`urn:eoip:proposed:{tenant}`) so they cannot be mistaken for facts downstream.
- **CRA-045.6** `[PRM]` Calibration honesty: a raw model output is labelled `score`, never `probability` or `confidence`, until a calibrator exists for that model and task with recorded calibration error (CRA-026.6, CRA-044.5).
- **CRA-045.7** `[PRM]` Reproducibility: every probabilistic result records model or provider revision, input or prompt digest, context-manifest digest (CRA-026.12), seed where applicable and the deterministic inputs (snapshot, ontology and policy revisions), so a reviewer can rerun it; non-reproducible providers are labelled as such.
- **CRA-045.8** `[RES]` Explanations state which path produced each part of an answer and, for probabilistic parts, the evidence and calibration status. The GUI (CRA-030) shows deterministic and probabilistic results side by side with distinct text labels, not colour alone.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| probabilistic output state | proposed | PRM |
| dual path | on wherever a deterministic path exists | PRM |
| proposed statements in exports | excluded unless requested; named graph when included | RES |

**Acceptance obligation CRA-045.A** (only after every clause above is ACCEPTED):

- `[PRM]` For a fixture question with a known exact answer, the API returns the deterministic and the probabilistic result with producer classes; injecting a misleading embedding neighbour produces `DISPUTED`, not a silent override; a probabilistic candidate violating a SHACL shape is shown as rejected-by-constraint; an asserted-only SPARQL query and a TriG export contain no proposed statements; a proposal promoted through review keeps its lineage and approver; an uncalibrated score is never labelled a probability in the API or UI.

**Not evidence of completion:**

- Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message.
- A `knowledge_state` column no query filters on; UI copy labelling a raw score as confidence.

## 8. Target Architecture and Module Boundaries

### 8.1 Planes

```text
Enterprise systems -- push/webhooks/CDC --+-- bounded poll/crawl agents
                                          |
                   Universal connection factory gateway (auth, signatures, rate limits, egress policy, ACL mirroring)
                                          |
                   Raw artifact vault (CAS, sha256) + append-only bitemporal source event journal + cursors
                                          |
                   Isolated parser / extractor / mapping workers (office, email, archive, OCR, ASR, diagram, NLP)
                                          |
                   Staged candidates + evidence locators + source ACLs + provenance (PROV-O)
                                          |
                   SHACL validation | reasoning (ReasonerPort) | identity review | approval
                                          |
                   Authorized publication boundary (expected base revision, idempotency, outbox)
                                          |
     +--------------------+---------------+-------------------+------------------+
     | Canonical graph    | Ontology/package registry         | Control DB (jobs, ledger, policy, cursors)
     +--------------------+---------------+-------------------+------------------+
                                          |
                   Durable outbox -> scoped projection workers (policy epoch, watermarks)
                                          |
                   Search + vector + catalog/lineage + analytics projections (rebuildable)
                                          |
                   Typed query / federation / GraphRAG / governed actions / MCP / SDK
                                          |
                   Accessible modular React workbenches (truthful states, i18n, WCAG 2.2 AA)

Cross-cutting: TrustedScope + policy epochs, secrets/egress, audit, budgets, telemetry, recovery, SBOM/licensing, entitlements.
Probabilistic plane (v3.1): numerical-tier workers (CRA-043) host embedding, learned-graph, OCR/ASR and local-model work;
their outputs return to the staged-candidate stage as proposals, and dual-path arbitration (CRA-045) sits at the query/answer layer.
```

### 8.2 Graph planes (AGG, adopted)

| # | Plane | Contents | Authority |
|---|---|---|---|
| 1 | Raw resource graph | Source IDs, revisions, structure as extracted | Mirror of source; immutable history |
| 2 | Canonical domain knowledge graph (A-Box) | Harmonized entities and accepted assertions | Canonical |
| 3 | Schema / meta-graph (T-Box, shapes) | Ontology versions, classes, properties, shapes, mappings, profiles | Registry (CRA-018) |
| 4 | Provenance and derivation graph | PROV-O, justifications, extraction runs | Canonical |
| 5 | Lineage graph | Data movement from sources through transforms to dashboards | Canonical + catalog layers |
| 6 | Policy and security graph | ACLs, classifications, tenants, policy epochs | Source-authoritative + policy store |
| 7 | Temporal and event graph | valid/transaction time, events, corrections | Journal + canonical |
| 8 | Vector similarity index | Dense/sparse text embeddings of chunks/entities and graph-structure embeddings (CRA-044) | Derived projection, rebuildable |

A meta-graph is not the data graph relabelled: its objects are models, types, predicates, mappings, profiles and versions.

Graph levels used by the neural-fabric inputs map onto these planes (CRA-044.2): GL0 instance graph -> planes 1-2; GL1 meta-graph -> plane 3; GL2 living brain -> plane 2 across sources; GL3 enterprise ontology -> plane 3 axioms and shapes; temporal axis GLT -> plane 7. Learned models read authorized snapshots of these planes and write only proposals and plane-8 projections.

### 8.3 State ownership

| Boundary | Owns | Must not own |
|---|---|---|
| Connector factory | Provider registration, config validation, capability selection | A claim that every registered source is certified |
| Acquisition worker | Vendor cursor/lease and received source events | Final publication or broad service-account authority |
| Raw vault | Immutable revision bytes, checksums, access metadata, retention | Guessable public download URLs |
| Parser/extractor | Bounded extraction results, locators, warnings | Automatic acceptance of model claims |
| Semantic worker | Pinned parse/reason/validate runs and artifacts | Tenant routing from untrusted text |
| Registry/governance | Releases, imports, review, publication manifests | Mutable unversioned global model singleton |
| Canonical graph | Authorized accepted assertions and stable identities | Hidden vector fallback presented as fact |
| Query/retrieval | Typed plan, filtered results, evidence selection | Remote unrestricted execution of user strings |
| Action executor | Specific authorized side effects and compensation journal | General privileged code execution |
| GUI | Task state, accessible views, authorized drafts | Truth, capability or authorization decisions |
| Numerical / model worker (v3.1) | Training runs, model artifacts, embeddings as rebuildable projections, gate reports | Asserted facts, tenant routing, API-process memory |

### 8.4 Target module layout (OCA, extended)

```text
packages/eoip/ontology/
  serialization.py        CRA-016 / ONT-001  rdflib bridge (TTL, RDF/XML, NT, NQ, JSON-LD, TriG)
  reasoning/              CRA-019 / ONT-007  port.py, elk_adapter.py, openllet_adapter.py, jena_rules_adapter.py,
                                             native_adapter.py, hybrid.py (ONT-008), worker_client.py
  mapping/                CRA-017 / ONT-005  language.py (CML), ir.py, compiler.py, executor.py, provenance.py (ONT-018),
                                             suggest.py (ONT-006), r2rml_import.py (ONT-017), lpg_rdf.py
  actions/                CRA-027 / ONT-009  model.py, registry.py, executor.py, outbox.py, readback.py
  lint/                   CRA-022 / ONT-013  rules/, scanner.py
  sparql/                 CRA-024 / ONT-002  protocol.py, planner.py, lpg_translate.py
  docs/                   CRA-039 / ONT-014  generator.py, templates/
  alignment/              CRA-023 / ONT-015  deeponto_client.py
  mcp_server.py           CRA-039 / ONT-011
  shacl_validator.py      CRA-020 / ONT-004  public API kept; delegates to worker running pySHACL
  gitops.py, manifest.py, packs.py           preserved core (ports only; Lead Dev review)
packages/eoip/capabilities/                  CRA-001 registry + discovery route
packages/eoip/workers/                       CRA-002 supervisor, resource classes, worker protocol
packages/eoip/acceptance/ (or tools/acceptance/)  CRA-001/037 ledger + receipt verifier
packages/eoip/neural/                        CRA-043/044/045 (v3.1): numerics.py, runtime.py, contracts.py, antistub.py,
                                             featurestore.py, datasets.py, evaluation.py, registry.py, encoders/, temporal/,
                                             conv/, transformer/, generative/, spiking/, explain/, fusion.py, security.py,
                                             router.py  (detail: GN-REQ-v1 section 1.2)
packages/eoip/gnn/engine.py                  CRA-044.1: thin re-export of eoip.neural; hash functions move to tests only
```

All paths for new modules are proposals: the agent must first search for an existing canonical owner and extend it (CRAr protocol step 2).

## 9. Universal Connection Factory — Source Coverage

"Universal" means an open contract for adding systems, not prebuilt support for every undocumented API. Each connector declares discovery, baseline, polling, webhook, CDC, delete, ACL, attachment, lineage, write-back and resume independently, with supported versions, scopes, limits, qualification receipt and a truthful unavailable reason.

| Source | Requirement | Ingestion modes | Entities / relations (proposed vocab) | ACL model | Critical qualification |
|---|---|---|---|---|---|
| Jira (Cloud, DC) | CRA-005 | Webhooks + JQL polling | Issue, Project, Sprint, Component, Version, Worklog, User; blocks, relatesTo, duplicates, clones, subtaskOf | Project permission schemes, issue security levels | Pagination, custom fields, deletes, overlap windows |
| Rally | CRA-005 | WSAPI v2.0 polling | HierarchicalRequirement, Defect, Task, Iteration, Release, PortfolioItem; parent, blockedBy, associatedDefect | Workspace/project scope | Throttling, revision checkpoints |
| qTest | CRA-005 | REST polling | TestCase, TestRun, Execution, DefectLink; verifiesRequirement | Project ACL | Definition vs execution, incremental results |
| Confluence / Wiki | CRA-006 | Webhooks + CQL crawl; generic wiki API/crawl | Page, Space, BlogPost, Comment, Attachment, Version; childOf, linksTo, mentions | Space perms, inherited/page restrictions | Macro fidelity, deleted versions |
| Slack | CRA-006 | Events API + history | Channel, Message, Thread, File; postedIn, repliesTo, referencesTicket | Channel membership; private/DM blocked by default | Edits/deletes, retention, legal approval (H-13) |
| Documentum | CRA-006 | REST Services + CMIS | Cabinet, Folder, Document, Version, Rendition; locatedIn, hasRendition, supersedes | Documentum ACLs, inheritance, retention/legal hold | Licensed API, checkout/version |
| GitHub / GitLab | CRA-007 | Webhooks + REST/GraphQL | Repository, Commit, Branch, PR/MR, Issue, Pipeline, Release; modifiesFile, authoredBy, mergesInto, referencesIssue | Installation/project scopes, visibility | Rename/delete/fork, rate limits, signed webhooks |
| Artifactory | CRA-007 | AQL + webhooks | Repository, Artifact, DockerImage, BuildInfo; builtFromCommit, containsPackage, deployedToEnv | Repository ACL | Checksum identity, promotion/deletion |
| API Portal | CRA-007 | OpenAPI crawler + admin APIs | Service, Endpoint, Operation, SchemaModel | Portal/product ACL | Product identity H-07 |
| ServiceNow | CRA-008 | Table API polling + outbound business rules | ConfigurationItem, Incident, ChangeRequest, Problem, Knowledge; dependsOn, causedBy, affectsCI | ACLs, user criteria, domain separation | Least privilege, approved writes only |
| Splunk | CRA-008 | Saved search REST + HEC | SavedSearch, Alert, Dashboard; monitorsService | App/role permissions | Search budgets, secrets redaction |
| Kibana | CRA-008 | Saved objects API | Dashboard, SavedObject; visualizesEntity | Spaces vs index permissions | Index data authority separate |
| Grafana | CRA-008 | REST API | Dashboard, Panel, DataSource; queriesSource, tracksService | Org/folder/data-source perms | No credential extraction |
| Snowflake | CRA-009 | Metadata crawl + Streams/Tasks + virtual query | Database, Schema, Table, Column, View; contains, derivedFrom | Roles, masking/row policies | Cost, SQL dialect, query-history scope |
| Fortuna | CRA-009 | Generic custom adapter until identified | — | — | Product identity H-06 |
| Any other system | CRA-004/009 | REST/OpenAPI, GraphQL, SOAP 1.2, JDBC/ODBC, SFTP/object store, Kafka/RabbitMQ/CDC | via CML | per protocol | Provider-specific mapping; no fake certification |

Prefer APIs and source-native event/CDC mechanisms over scraping. Store cursors separately from credentials; secrets are references, never configuration values or browser storage. Existing adapter names are discovery leads, not proof of completion.

## 10. Multiformat Acquisition and Knowledge Construction

Sequence: accept -> quarantine/scan -> identify actual format -> bounded decode -> source-located sections/frames/transcripts -> extract candidates -> normalize/map -> resolve -> validate -> review -> publish -> update graph/meta-graph/search/vector projections -> acknowledge cursor.

| Input | Engine candidates (license-reviewed) | Minimum meaningful result | Never called complete when |
|---|---|---|---|
| TXT/JSON/CSV/TSV/YAML | stdlib, streaming parsers, Polars | Encoding/schema-aware structure with line/column/key locators | Bytes decoded without field meaning |
| HTML/XML/XHTML/Markdown | defusedxml/lxml (no entities), BeautifulSoup | Sanitized structure, DOM path locators | Scripts rendered or external entities resolved |
| DOCX/PPTX/XLSX | python-docx, python-pptx, openpyxl/calamine | Paragraphs/slides/sheets/tables; formulas separate from cached values | Extension recognized only |
| DOC/PPT/XLS/RTF/ODF | LibreOffice headless / Tika in heavy worker | Converted content + fidelity diagnostics | Legacy conversion assumed lossless |
| EML/MBOX/MSG | stdlib email; MSG license-gated | Message identity, headers, parts, nested attachment provenance | Single MIME part treated as whole message |
| ZIP/TAR/GZ/BZ2/7Z | streaming, bounded | Members with safe names and provenance | Per-member limits allow total over budget |
| Images / scanned PDF | Tesseract or PaddleOCR | OCR text with normalized bbox and confidence | Metadata-only labelled understanding |
| Audio / video | FFmpeg + local Whisper-family ASR | Timestamped transcript, sampled frames | Filename or unsupported codec yields success |
| Engineering diagrams | draw.io/Chowlk XML, PlantUML, Mermaid subsets, VSDX (P2), reviewed vision candidates | Components, ports, links with uncertainty and loss ledger | Every box -> Service, every arrow -> CALLS |

Images and video do not automatically yield correct engineering topology. Preserve raw bytes and extraction versions so corrections rebuild all derivatives.

## 11. API Surface (consolidated; proposed until implemented and receipted)

| Method and path | Purpose | Requirement |
|---|---|---|
| GET `/api/v1/capabilities` | Capability registry with states | CRA-001 |
| POST `/ontology/import` | Import RDF/OWL/SKOS in six formats -> import report | CRA-016 |
| GET `/ontology/export?format=turtle\|rdfxml\|nt\|nq\|jsonld\|trig` | Export with tenant graphs | CRA-016 |
| POST `/ontology/validate` | Existing contract, unchanged | CRA-020 |
| POST `/ontology/validate/shacl` | Synchronous bounded SHACL validation | CRA-020 |
| POST `/api/v1/semantic/validations` (+ GET status) | Durable validation job, Idempotency-Key required | CRA-020/031 |
| POST `/ontology/reason/classify` | Classification + unsatisfiable classes | CRA-019 |
| POST `/ontology/reason/explain` | Justification for an entailment | CRA-019 |
| GET/POST `/sparql` | SPARQL 1.1 Protocol | CRA-024 |
| POST `/ontology/mapping`, GET `/ontology/mapping/{source}` | CML validation + dry-run triples | CRA-017 |
| POST `/ontology/mapping/suggest` | AI-suggested CML (proposal only) | CRA-017/026 |
| POST `/ontology/lint` | Pitfall findings | CRA-022 |
| GET `/ontology/docs` | Generated ontology documentation | CRA-039 |
| POST `/api/v1/actions/execute`, POST `/api/v1/actions/{id}/approve`, GET `/api/v1/actions` | Governed actions (aliases `/ontology/actions/...`) | CRA-027 |
| GET `/metrics` | Prometheus text format | CRA-032 |
| MCP server | Ontology, graph, actions with identical gates | CRA-039 |
| GET `/api/v1/neural/runtime` | Numerical tier, backend, device, BLAS threads | CRA-043 |
| POST `/api/v1/neural/predict/links`, `/predict/impact`, `/classify/node`, `/anomaly/scan` | Learned predictions returned as proposed assertions with lineage | CRA-044 |
| GET `/api/v1/neural/explain/{prediction_id}` | Evidence subgraph and faithfulness status | CRA-044 |
| GET `/api/v1/neural/models`, POST `/api/v1/neural/models/{id}/promote`, `/rollback` | Model registry with gate reports | CRA-044 |
| POST `/api/v1/answers` (or the existing ask route) | Dual-path answer with producer classes and context-manifest digest | CRA-026/045 |
| POST `/api/v1/proposals/{id}/promote`, `/reject` | Proposed -> asserted only through validation and review | CRA-045 |

Proposed OpenAPI 3.1 fragment for the semantic validation job (CRA section 11.4, retained):

```yaml
openapi: 3.1.0
info: {title: EOIP Semantic Jobs - proposed, version: 1.0.0}
paths:
  /api/v1/semantic/validations:
    post:
      operationId: submitSemanticValidation
      security: [{bearerAuth: []}]
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema: {type: string, minLength: 1, maxLength: 128}
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              additionalProperties: false
              required: [dataset_revision, ontology_revision, shapes_revision, profile]
              properties:
                dataset_revision: {type: string, minLength: 1}
                ontology_revision: {type: string, minLength: 1}
                shapes_revision: {type: string, minLength: 1}
                profile: {enum: [shacl-core-2017]}
      responses:
        '202': {description: Authorized durable job accepted; not a validation pass}
        '403': {description: Scope or capability denied}
        '409': {description: Revision or idempotency payload conflict}
        '422': {description: Invalid request or unsupported declared profile}
        '503': {description: Required validator unavailable}
components:
  securitySchemes:
    bearerAuth: {type: http, scheme: bearer}
```

Every status/download/cancel URL requires the same trusted scope. Error payloads carry stable codes, field pointers and correlation IDs without secrets. Bearer authentication in the fragment is an interface example, not the production session design.

## 12. Security Threat Register (merged CRA + OCA + AGG)

| Threat | Required design | Acceptance attack | Req |
|---|---|---|---|
| Tenant/source ACL leak | TrustedScope, deny-by-default, plan-level filters, scoped projections | Colliding IDs; hidden intermediate traversal; aggregate/count leak | CRA-003 |
| Inference side channel | Justification-based ACL composition, policy epochs | Remove one premise permission; probe answers/indexes/exports | CRA-003/019 |
| SSRF / crawl escape | Egress allowlist, per-request DNS/redirect checks, metadata ranges blocked | Redirect, DNS rebinding, IPv6, proxy, embedded URL, cross-origin auth | CRA-011 |
| XXE / entity expansion via RDF/XML | Entity resolution disabled, size caps, parse timeout | External entity, billion laughs | CRA-016 |
| Malicious file / plugin / ontology | Quarantine, safe parsers, budgets, isolated workers, pinned imports | Zip/XML bombs, macros, traversal, hostile JS/rules/imports | CRA-002/012/013 |
| SPARQL injection / DoS | Typed parameterized plans; cost estimator, deadline, row caps | Concatenated input, unbounded OPTIONAL/property paths | CRA-024 |
| Reasoner DoS | Profile pre-check, axiom-count check, deadline, worker kill | Exponential classification ontology | CRA-019 |
| CML template injection | Restricted grammar, whitelisted functions, never eval | `{0.__class__}`, `__import__` | CRA-017 |
| Prompt injection | Retrieved text is untrusted data; tools use server policy | Document instructs export/action | CRA-026 |
| Action replay / confused deputy | Digest-bound approval, nonce, expiry, idempotency, autonomy gate | Changed params after approval; replay; revoke before execution | CRA-027 |
| PII leakage on export | Classification-aware export filter honouring CML governance | Export classified fields | CRA-017/040 |
| Cross-tenant export | TriG preserves tenant graphs | Merge attempt | CRA-003/016 |
| Tampered update / supply chain | Signed manifests, SBOM, provenance | Modified image/plugin/config, dependency confusion | CRA-002/035 |
| Silent data loss | Checksums, loss ledger, partial states, reconciliation | Unsupported type, dropped mapping, failed projection | CRA-010/016/017 |
| Retention / deletion failure | Derivative inventory and deletion workflow incl. backups | Delete subject, check every store | CRA-040 |
| Embedding / model membership inference | Entitlement filtering before featurization and training; embeddings influenced by restricted neighbours never served to unentitled principals | Probe existence via neighbour counts, latency, error text | CRA-003/044 |
| Training-data poisoning | Train only on accepted plane 2/3 snapshots; anti-stub and baseline gates; drift monitoring | Inject crafted edges through a source | CRA-044 |
| Context-window evidence displacement | Restricted evidence filtered before budgeting; disclosed reduction; retrieved text cannot change priority | Oversized malicious document crowds out evidence | CRA-026/045 |
| Accelerator / memory exhaustion | Pre-allocation memory estimate and refusal; heavy workers only | Oversized training or full-graph job | CRA-043 |

## 13. Licensing and Dependency Decisions

| Component | License (as stated by sources) | Decision | Notes / conflict |
|---|---|---|---|
| rdflib | BSD-3 | Adopt (pinned) | — |
| pySHACL | Apache-2.0 | Adopt (worker) | — |
| ELK | Apache-2.0 | Adopt as default EL classifier (JVM worker) | H-02 air-gap |
| Openllet | Apache-2.0 per OCA | Optional DL adapter after license verification | R-research |
| HermiT | LGPL | Optional separately installed plugin only | Never bundled |
| OWL API | LGPLv3/Apache-2.0 dual (per sources) | Worker dependency after exact-artifact review | — |
| ROBOT | BSD-3 | CI/worker tooling | Bundled reasoners reviewed separately |
| TopBraid SHACL API | Apache-2.0 | Differential oracle | JVM |
| Apache Jena / Fuseki | Apache-2.0 | Reference RDF backend | Single-node TDB2 |
| Eclipse RDF4J | EDL/EPL/BSD-style | Acceptable | — |
| GraphDB | Commercial / free edition | Certified external backend option | Edition terms |
| Neo4j Community | GPLv3 | Network protocol only; never linked/bundled | n10s Apache-2.0 separate |
| Virtuoso OSE | GPLv2 | Network protocol only | — |
| WebProtégé | BSD-style vs AGPL (X-01) | Do not integrate | Verify |
| TerminusDB | Disputed (X-21) | Blocked pending Legal | H-04 |
| Ontop, Morph-KGC | Apache-2.0 | Candidate adapters | — |
| RMLStreamer / SDM-RDFizer | Open source (verify each) | Candidates | Separate licenses |
| Karma | Apache-2.0, archived 2025-04-16 | Do not adopt runtime | Concept only |
| DeepOnto | Apache-2.0 | Optional alignment worker | CPU mode qualified until H-17; JVM bridge |
| spaCy / textacy | MIT | Adopt with model license review | Models separate |
| extract-msg | Unresolved | Disabled | H-09, X-16 |
| FFmpeg | LGPL/GPL by build | Reviewed build only | — |
| gist | CC BY 4.0 | Adopt as domain pack with attribution | X-03 |
| FIBO, schema.org | Verify exact artifacts | Packs after verification | X-30 |
| SNOMED-CT | Affiliate license | Customer-provided only | Never redistribute |
| LODE / WIDOCO | ISC (legacy LODE) / Apache-2.0 | Doc generation candidates | X-02 |
| numpy, scipy, scikit-learn | BSD-3 | Adopt as tier N0 optional extra | Never core (CRA-043) |
| torch | BSD-3 | Adopt as tier N1; CPU-only builds distributed (H-15, H-16) | CUDA builds never distributed |
| torch-geometric | MIT | Adopt as tier N1 | — |
| transformers, sentence-transformers | Apache-2.0 | Adopt as tier N2 | Model weights licensed separately |
| snntorch | MIT | Tier N3, research sandbox only | — |
| `nvidia-*` CUDA runtime packages | NVIDIA Software License Agreement | **Never bundled, mirrored or redistributed (H-16 decided 2026-10-18)** | Customer-provisioned only; unqualified until H-17 |
| llama.cpp / Ollama, whisper.cpp / faster-whisper | MIT per upstream (verify exact artifacts) | Candidate CPU inference runtimes for generation and ASR (CRA-026.13, CRA-014) | CRA-035 and CRA-042 review before adoption |
| DGL | Apache-2.0 | Do not add | PyG sufficient |
| networkx | BSD-3 | Prefer not to add | Baselines implemented with numpy |

A process or network boundary is not a blanket copyleft exemption; obligations depend on the actual integration and distribution (SaaS and installed). Publicly readable source is not permission to copy. No patent freedom-to-operate opinion is given. Clean-room rule: record public facts and independent designs; never copy proprietary code or UI assets.

## 14. Benchmark, Quality and QA Plan

Datasets: small authored enterprise ontology (gold entailments, inconsistency, competency questions); W3C RDF/SPARQL/SHACL/OWL profile test suites (exact revisions); LUBM, BSBM, SP2Bench, WatDiv (licenses verified before acquisition); synthetic enterprise source/ACL corpus (Jira/wiki/code/incident joins, tenant collisions, revocation truth); mapping corpus (CSV/SQL/JSON/XML with nulls, joins, duplicates); labelled multimodal corpus (OCR, linking, diagram topology); reference ontologies for round-trip (gist, schema.org, FOAF, Dublin Core, SKOS thesaurus, FIBO subset, SNOMED subset only if customer-provided).

Measure p50/p95/p99, successful/failed/cancelled counts, timeouts, CPU, peak RSS, disk/GPU bytes, index/inference amplification, projection lag, source cost, cache state and restore time; cold and warm phases; concurrency ramps; skew; updates/deletes; stale mappings; throttling; crash/restart. Fast wrong answers fail. Do not benchmark Ontop by repeatedly invoking its setup-heavy query CLI; use a warmed endpoint. At least three measured trials per configuration with variability reported; competitive comparisons require equivalent semantics, authorization, durability, replication, paid features and reviewed publication terms.

Benchmark targets (manifest values, OCA + AGG): LUBM load >= 50k triples/s and Q1-Q14 p95 < 500 ms; BSBM >= 1,000 QMpH at 100M; SP2Bench no query > 30 s at 50M; SHACL >= 20k nodes/s (10M nodes, 500 shapes); ELK classification of 20k classes/150k axioms < 60 s; round-trip per section 5.3; CML >= 10k records/s; batch materialization >= 100k triples/s; OBDA point query < 50 ms; sustained 4-hour load stability; CI regression gate > 10% p95.

QA layers: unit; property/fuzz (Hypothesis); differential semantics across independent engines; contract; real-backend and vendor-sandbox integration; security/tenancy; real-browser workflow and accessibility (Playwright + axe + manual AT); migration/restore; chaos; performance. Mocks are a separate labelled category. A skipped, xfailed, mocked-at-boundary, stale, unseeded or wrong-backend test cannot qualify a requirement.

Learned-model evaluation (CRA-043/044, v3.1): frozen, content-addressed reference snapshot; event-time splits validated per batch; type-constrained negatives; the five mandatory baselines; AUPRC, Macro-F1 or time-filtered MRR as primary; calibration error; at least three seeded trials; independently authored fixtures (known graph with removed edges, automorphic node pair, leaky split, clean and broken ontology, implausible triples, multi-domain graph). A model that only ties the degree baseline learned popularity and fails.

## 15. Observability, Delivery, Recovery and Operations

OpenTelemetry traces, structured logs and Prometheus metrics correlate source event -> job -> parser -> semantic run -> publication -> projection -> query/action. Record IDs and hashes, never tokens, raw sensitive content or unredacted prompts. Bounded metric cardinality; tenant detail only in access-controlled traces/logs. Dashboards: acquisition freshness and denied scopes; parser failures/budgets; validation unsupported/timeouts; ontology release health; inference amplification/retraction; job queue/lease age; projection policy/revision lag; model cost/quality; query latency/errors; pending actions/compensation; backup/restore observations. Unknown or stale telemetry is never shown as a healthy zero.

CI stages: static checks -> contracts -> unit/fuzz -> independent semantics -> real-backend integration -> security/tenancy -> browser/accessibility -> migration/restore -> workload/performance -> signed artifact/SBOM/notices -> source-bound evidence verification. Build once; promote the exact digest; qualify SaaS and installed profiles separately.

Backups include canonical graph, control DB, ontology packages/import locks, raw references, secrets/KMS recovery procedure, event/outbox state and projection rebuild watermarks; encrypted, access-controlled, retention-aware, periodically restored into a clean environment.

Operational playbooks (each: trigger, containment, recovery, proof): cross-tenant/ACL leak; source credential compromise; poisoned ontology/model proposal; parser exploit/decompression spike; query overload/OOM; stuck/duplicate jobs; index/policy lag; regional/store loss; failed upgrade; ingestion backlog (AGG: scale workers, pause deep media, preserve raw blobs); inconsistent ontology panic (AGG: quarantine release, fall back to previous stable revision, halt dependent actions, run justification extraction). Scaling and upgrade playbooks: observe -> confirm correctness -> choose lever -> load test -> staged rollout -> rollback on invariant/SLO breach.

Support proposals (decision H-08): CRAr tiers (community/no SLA; standard business hours; enterprise 24x7 critical escalation) with P1 1 h, P2 4 business hours, P3 2 business days; AGG matrix P1 < 15 min / workaround < 2 h / fix < 24 h, P2 < 1 business hour, P3 < 4 business hours, P4 < 1 business day. Availability metric = successful eligible requests / all eligible requests per calendar month with declared endpoints, locations and exclusions; response is not resolution; installed deployments define customer versus vendor responsibility.

## 16. Delivery Sequence, Roadmap and Cost Model

### 16.1 Gates (dependency order; not a calendar)

| Gate | Name | Requirements | Required exit evidence |
|---|---|---|---|
| A | Truthful baseline | CRA-001, CRA-042 | Complete open ledger; real capability discovery; agreed defaults; research records pinned for chosen dependencies |
| B | Safe platform | CRA-002/003/031/032/035/040/043 | Principal/scope, isolated worker, durable state, supply-chain and privacy negative tests; numerical tiers installable with truthful capability states; CPU-only builds with zero `nvidia-*` packages in distributed artifacts |
| C | First acquisition slice | CRA-004/010/011/012/013 + one real source | Push/pull -> raw -> parse -> staged evidence -> replay after crash |
| D | Semantic core | CRA-016/017/018/019/020 | Independent syntax/term/entailment/shape correctness; no invalid publication |
| E | Governed knowledge | CRA-021/022/023/028/029 | Reviewed release, source conflict, identity undo, historical authorization |
| F | Usable value | CRA-024/025/026/030/044/045 | Real query/answer/evidence/save/export with denial and restart; dual-path answers; a learned model passing anti-stub and baseline gates on CPU-only hardware |
| G | Named sources, media and actions | CRA-005..009/014/015/027 | Every named adapter/media task qualified or explicitly blocked |
| H | Deploy and migrate | CRA-033/034/039 (+035) | Actual artifact install, migration, rollback, restore and SDK task |
| I | Independent acceptance | CRA-036/037/038/041 + remaining GUI/CP | Stable-revision real-profile evidence; manual reviews; support readiness; claims register |

Cycles are iteration boundaries, not deadlocks: CRA-031 provides the durable substrate for CRA-010; CRA-021/022 share the registry foundation; CRA-037 runs from Gate A onward. First close observed semantic defects (G01-G03, F1-F3) and one trustworthy vertical slice (E01); nothing deferred disappears from the programme.

### 16.2 OCA quarter plan mapped to gates

| OCA quarter | ONT sequence | Gate(s) | Exit criteria (all receipt-backed) |
|---|---|---|---|
| Q1 Credibility | ONT-001 -> 004 -> 007 -> 016 -> 019 -> 012 | D (+A, B prerequisites) | gist, FIBO, schema.org round-trip within fidelity rule; exported shapes pass independent SHACL processing; no hardcoded axioms; positioning only after CRA-041 evidence |
| Q2 Differentiation | ONT-005 -> 006 -> 009 -> 011 -> 013 -> 010 | C, E, G | New source onboarded by one CML file; governed audited actions (if H-03 allows); MCP live with identical gates |
| Q3 Scale and completeness | ONT-002 -> 003 -> 008 -> 018 -> 020 -> 014 -> 015 -> 017 | F, H, I | SPARQL protocol tests; LUBM published as receipt; customer GraphDB targetable by config |

### 16.3 Capacity and cost (planning estimate, not a quote)

| Stage | Work | Person-weeks |
|---|---|---|
| M0 | Decisions, capability inventory, ledger | 8 |
| M1 | Principal/policy, plugin boundaries, durable control plane | 24 |
| M2 | Event factory + initial certified connectors | 40 |
| M3 | All named source families + SDK certification | 60 |
| M4 | Safe multimodal/diagram ingestion | 45 |
| M5 | RDF/mapping/reasoning/validation engines | 40 |
| M6 | Ontology/vocabulary lifecycle, identity, migration | 50 |
| M7 | Query/OBDA/catalog/context projections | 35 |
| M8 | Retrieval/AI/actions/simulation | 40 |
| M9 | Modular accessible GUI | 30 |
| M10 | Performance, HA/restore, supply chain, both deployment modes | 35 |
| M11 | Independent acceptance, support, rollout | 25 |
| M12 | Numerical substrate, learned graph intelligence and dual-path arbitration (v3.1: CRA-043, CRA-044, CRA-045, CRA-026.10-026.12) | 46 |
| | **Total** | **478** (range 380-770 until M0/M2 recalibration; M12 range 30-70, bake-off-gated work in CRA-044.7/044.8 only if pursued) |

With 8 FTE at 70% availability: about 68-138 working weeks before critical-path and vendor constraints. AGG's three-quarter milestone plan (M0-M9) is an optimistic alternative, not a commitment. Cost: `engineering = sum(person_weeks x loaded_rate)`; `runtime = compute + storage + model/provider + backup + network + observability + commercial engines/support`; `programme = engineering + runtime + security/legal/accessibility reviews + licensed datasets/sandboxes + contingency`. AGG's indicative AWS P1 baseline (~USD 49,560/year infrastructure) is an unverified estimate; rates and quotes are inputs (H-10). Runtime estimates assume CPU-only compute until H-17; any GPU cost is a separate scenario.

## 17. End-to-End Scenarios and Release Checklist

| ID | Scenario | Steps | Independent checks |
|---|---|---|---|
| E01 | Source-to-answer | Configure permitted source, discover/select, baseline, parse, review, validate, publish, index, ask and inspect source evidence | Exact source revision, accepted assertions, real model/provider and source ACL |
| E02 | Live change | Edit source content then ACL, ingest incrementally and query again | Correct cursor/watermark, no duplicate or stale forbidden answer |
| E03 | Bad semantics | Invalid cardinality/datatype/profile and inconsistent ontology | Explicit failed/unsupported report; unchanged accepted graph |
| E04 | Model release | Concurrent draft edits, impact, review, signed publish, failed consumer and rollback | Exact revision approval, conflict, no partial hidden state |
| E05 | Identity correction | Ambiguous entities, reviewed merge, source updates, split | Every relationship/evidence/history restored correctly |
| E06 | Action | Dry-run, review, approval, source mutation, timeout/retry and read-back | Exact approved arguments, one effect, compensation/unknown outcome truth |
| E07 | Isolation | Colliding IDs and hidden intermediate facts across tenants/workspaces | No API/UI/search/vector/inference/count/event/export/raw leakage |
| E08 | Recovery | Kill API/worker/store during acquisition/publication; restore clean node | Durable job/cursor/outbox/revision/ACL consistency and measured RPO/RTO |
| E09 | Migration | Export different model/store, stage/compare, catch up, cutover and rollback | Declared fidelity, loss ledger, gold queries, no action side effects |
| E10 | Media | Office/email/archives/images/audio/video/diagram processing | Bounds, locators, dependency readiness, reviewed candidates and no covert egress |
| E11 | Deletion | Delete/revoke while jobs run, rebuild indexes and restore old backup | No resurrection, reviewed hold policy and complete derivative accounting |
| E12 | Customization | Install qualified connector/parser/UI/provider plugin and change theme/locale | No core edit required, compatible contracts, sandbox, accessibility and rollback |
| E13 | Neuro-symbolic arbitration | Ask a question with a known exact answer; run deterministic and probabilistic paths; inject a misleading embedding neighbour; try to publish a model proposal that violates a shape | Both results with producer classes; DISPUTED surfaced; constraint rejection shown; asserted-only query and export exclude proposals |
| E14 | Numerical tiers and learned model | On a host with no GPU, install core only, then N0, then N1 from the offline bundle; train and evaluate the default graph model; substitute the hash stub | Correct tier states and 503s; seeded reproducibility; anti-stub probes pass for the model and fail for the stub; five baselines reported; zero `nvidia-*` packages in the bundle; receipts record `device=cpu` |

Final acceptance uses real permitted backends and source/model integrations; small synthetic fixtures serve fast tests. E01's API return values never substitute for E07/E08 evidence.

Release handoff: exact commit/source inventory; reproducible build and artifact digests; supported profile/backend/source/model versions; migration/rollback/restore instructions; SBOM and notices; raw correctness/security/performance/browser results; manual review records; operational playbooks; acceptance ledger; claims register; known limitations and blocked/deferred work with owners. A scoped P1 release is never described as 100% of the programme; programme completion additionally requires P2 and external/manual obligations.

## 18. Conflict Register and Human Decisions

### 18.1 Conflict register

| ID | Topic | What the sources say | Binding resolution | Status | Affects |
|---|---|---|---|---|---|
| X-01 | WebProtégé license | CRA: classic repo inspected is BSD-style. OCA: AGPL. AGG: AGPLv3/BSD version dependent. | Treat as unresolved per exact artifact; EOIP does not integrate WebProtégé regardless; R-C01 verifies. | RESEARCH | CRA-035/042 |
| X-02 | LODE license | CRA and AGG: ISC (legacy repo), moved to OpenCitations Aug 2026. OCA/CSV: Apache/MIT. | ISC per inspected legacy repo; successor and WIDOCO-bundled copy verified separately. | RESEARCH | CRA-035/042 |
| X-03 | gist size and version | AGG: ~100 classes/~100 properties/~1,000 axioms. OCA: ~200 concepts. CRA: 14.1.0, Apr 2026, CC BY 4.0. | Pin the artifact and count from it; no size claims until counted. | RESEARCH | CRA-018/042 |
| X-04 | Python version | CRA: pyproject `>=3.11`. OCA: Python 3.12+ syntax. | pyproject is authoritative; CRA-001 re-measures; code must run on the declared minimum. | DECIDED | CRA-001 |
| X-05 | P1/P2 point-read latency | CRAr: P1 <= 250 ms, P2 <= 500 ms. AGG: P1 < 20 ms, P2 < 20 ms. OCA: p95 < 20 ms assumed (to confirm). | CRAr targets are binding gates; 20 ms is a stretch objective until decision H-01. | DECIDED | CRA-036 |
| X-06 | Bounded graph page / query latency | CRAr P2: graph page <= 2 s, query suite <= 10 s. AGG P2: 2-hop < 250 ms, query < 3 s. | As X-05. | DECIDED | CRA-036 |
| X-07 | Ingestion throughput | AGG: P1 25k, P2 50k triples/s. OCA: LUBM load >= 50k/s. CRAr: none. | Adopted as benchmark manifest targets; failures leave the clause unqualified, not the product unusable. | DECIDED | CRA-036 |
| X-08 | Support response objectives | CRAr: P1 1 h. AGG: P1 < 15 min 24x7. | Both are proposals; human commercial decision H-08. | HUMAN | CRA-038 |
| X-09 | RTO scope | CRAr: P1 RTO <= 4 h. AGG: <= 4 h for 500M-triple restore. | P1 binding; 500M restore is a P2 target. | DECIDED | CRA-033 |
| X-10 | Reasoning architecture | AGG: custom HTRE with O(1) retraction. CRAr: qualified engines, no hand-rolled OWL DL claims. OCA: ELK default + hybrid ONT-008. | Qualified engines behind ReasonerPort; hybrid strategy allowed; retraction cost measured, no O(1) claim. | DECIDED | CRA-019 |
| X-11 | Derived-fact ACL | AGG: intersection of premise ACLs. CRAr: all supporting facts of the explanation; alternate permitted proofs explicit. | Intersection within a justification; union across justifications; never expose restricted proof. | DECIDED | CRA-003 |
| X-12 | Connector allocation | AGG puts Slack and Kibana in CRA-009 and omits qTest. CRAr: Slack in CRA-006, Kibana in CRA-008, qTest in CRA-005. | CRAr allocation retained; AGG content merged into those requirements. | DECIDED | CRA-005..009 |
| X-13 | API Portal identity | AGG: Kong/Apigee/SwaggerHub. CRAr: unidentified product. | Candidate profiles only; adapter unqualified until H-07. | HUMAN | CRA-007 |
| X-14 | Fortuna identity | AGG: generic custom connector. CRAr: unidentified. | Generic adapter offered; product adapter blocked until H-06. | HUMAN | CRA-009 |
| X-15 | Abstention threshold | AGG: confidence < 0.85 abstains. CRAr: calibrated gates (abstention >= 0.95 on unanswerable). | 0.85 is an initial post-calibration setting; CRAr metrics are the gate. | DECIDED | CRA-026 |
| X-16 | MSG parsing | AGG: extract-msg. CRAr: extract-msg distribution question unresolved. | MSG adapter disabled until Legal clearance. | HUMAN | CRA-013/035 |
| X-17 | RDF-star | AGG: core model. CRAr: RDF 1.1 baseline; new standards as named profiles. OCA: RDF-star when target supports it else reification. | Optional named profile, disabled by default; named-graph assertion fallback. | DECIDED | CRA-016/017 |
| X-18 | Coverage / mutation thresholds | AGG: 85% coverage, 80% mutation as acceptance. CRAr: counts never prove completion. | Hygiene gates only. | DECIDED | CRA-037 |
| X-19 | EOIP self-scores | OCA: 2.9 today, 3.6 post-Q1, 4.2 post-Q3. AGG: target 5 on all dimensions. CRA: no weighted league tables; ND preferred. | Internal indicative only; no external use without CRA-042 rescoring. | DECIDED | CRA-041/042 |
| X-20 | 'No competitor has this' claims | OCA: GitOps, migration scripts, drift unique. CRAr: no superiority claims without reproducible evaluation. | Claims Register + evidence gate (CRA-041). | DECIDED | CRA-041 |
| X-21 | TerminusDB license | OCA: disputed (Apache vs GPLv3). AGG: Apache 2.0. CRA: not asserted. | Blocked until Legal verifies exact artifact. | RESEARCH | CRA-035/042 |
| X-22 | Anzo ownership | OCA: Altair acquired Cambridge Semantics (Apr 2024). CRA/AGG: Cambridge Semantics docs. | Record both; verify current vendor before procurement. | RESEARCH | CRA-042 |
| X-23 | Ontosphere reasoning | Attachment: simple OWL-RL. CRA: README describes Konclude-based DL. | Use CRA reading; verify release. | RESEARCH | CRA-042 |
| X-24 | OntoStudio architecture | Attachment/AGG: Eclipse-based. CRA: current OntoStudio X is spreadsheet-native. | Distinguish historical vs current product. | DECIDED | CRA-042 |
| X-25 | VocBench backend | Attachment: Jena. CRA/AGG: RDF4J via Semantic Turkey. | RDF4J per maintainer docs. | DECIDED | CRA-042 |
| X-26 | Receipt file layout | AGG: receipts/{clause_id}.json. Combined spec: receipts/<clause-id>/<run-id>.json. | Directory per clause; legacy path read-only alias. | DECIDED | CRA-001 |
| X-27 | Worker limits | AGG: 2 GiB / 2 CPU / 30 s. CRAr: budgets without numbers. | AGG numbers adopted as `standard` class defaults; `heavy` class added. | DECIDED | CRA-002 |
| X-28 | Hardcoded reasoner axioms | OCA: delete. CRAr: replace or clearly scope. | Removed from production; retained only as named fixture. | DECIDED | CRA-019 |
| X-29 | Round-trip fidelity threshold | OCA: >= 99% with enumerated losses. CRAr: 100% on supported subset, unsupported in denominator. | 100% supported subset + reported corpus fidelity + >1 pt regression gate. | DECIDED | CRA-016 |
| X-30 | FIBO / schema.org licenses | OCA: FIBO MIT; schema.org unspecified. | Verify exact artifact licenses before packaging. | RESEARCH | CRA-018/035 |
| X-31 | Supersession claims | AGG claims to supersede all prior research; CRAr is the evidence-based execution spec. | This combined document is canonical; sources retained as inputs. | DECIDED | all |
| X-32 | Benchmark tooling | AGG: wrk with a Lua SPARQL script; OCA: LUBM/BSBM/SP2Bench; CRA: LUBM/BSBM/WatDiv + W3C suites. | Union adopted; licenses of datasets verified before acquisition. | DECIDED | CRA-036 |
| X-33 | Repository facts | OCA counts (587 files, 38 connectors, 239 tests, etc.) vs CRA 'not re-audited'. | Re-measured at pinned commit under CRA-001. | DECIDED | CRA-001 |
| X-34 | Assertion status vocabulary | GN-002: `AssertionStatus` OBSERVED/DERIVED/PREDICTED/REJECTED/CONFIRMED. Section 6: `KnowledgeState` asserted/inferred/proposed/rejected/historical. | `KnowledgeState` is canonical; GN statuses are a mapping (OBSERVED->asserted, DERIVED->inferred, PREDICTED->proposed, REJECTED->rejected, CONFIRMED->asserted with promotion approver); no parallel enum. | DECIDED | CRA-044/045 |
| X-35 | Completion evidence format | GN: markdown Evidence Ledger `EOIP-engg-doc-pkg/evidence/GN-<id>.md`. This spec: JSON receipts under `.audit-scratch/receipts/`. | JSON receipts are the only acceptance evidence; a GN markdown ledger may be generated from receipts as a readable view and is never evidence. | DECIDED | CRA-001/044 |
| X-36 | Verification taxonomy | GN: levels V1-V7. This spec: lifecycle states plus 11 evidence categories. | Section 2 governs; GN V2-V7 map onto positive/negative, performance, integration and deployment categories; V5 anti-stub is required evidence for learned components (CRA-044.3, CRA-037.11); V1 is never evidence. | DECIDED | CRA-037/044 |
| X-37 | Learned-model quality gates | GN-006/007 thresholds (baseline +0.05, ECE <= 0.10, permutation gap >= 0.10) absent from section 5.3. | Adopted into section 5.3 as initial task-manifest gates; change only by recorded review. | DECIDED | CRA-036/044 |
| X-38 | Neural route prefix | GN-704: `/neural/...`. This spec: versioned `/api/v1/...` for new canonical routes (CRA-027.9 precedent). | Canonical `/api/v1/neural/...` with GN paths as suffixes; public versioning per CRA-039.1. | DECIDED | CRA-039/044 |
| X-39 | Missing-tier error | GN-001: HTTP 503. CRA-001.8: distinct code per capability state. | A missing installed tier is capability state UNAVAILABLE -> HTTP 503 `CAPABILITY_UNAVAILABLE` with tier and install command in details. | DECIDED | CRA-001/043 |
| X-40 | Hash embeddings disposition | GN-101: delete. CRA-025.7: rename `test-hashing`, refuse in production. X-28 precedent. | Removed from production paths; retained only as the `HashBaseline` fixture; production profile refuses at startup. | DECIDED | CRA-025/044 |
| X-41 | Embedding storage | GN-004: feature store defaulting to a graph-store sidecar. Section 5.1 and CRA-025.6: durable store, Qdrant/pgvector candidates, tenant-partitioned. | Graph embeddings are a rebuildable plane-8 projection in the CRA-025.6 vector store, tenant-partitioned; no new database without a decision record. | DECIDED | CRA-025/044 |
| X-42 | Effort and roadmap | GN plan: relative effort only. Section 16.3: no stage for the numerical stack or learned models. | Planning stage M12 added (46 person-weeks, range 30-70); inputs per H-10. | DECIDED | Section 16 |

### 18.2 Human decisions (dependent clauses stay BLOCKED until recorded in the ledger)

| ID | Decision needed | Owner | Blocks | Status |
|---|---|---|---|---|
| H-01 | Confirm target scale and whether stretch latency objectives (p95 < 20 ms) become binding | CTO | CRA-036, X-05/X-06 | OPEN |
| H-02 | Air-gap: may customer deployments run JVM worker sidecars (ELK, OWL API, ROBOT)? | CTO / Security | CRA-019 | OPEN |
| H-03 | Is write-back (CRA-027) in v1 scope or read-only until SOC 2? | Security Officer | CRA-027 | OPEN |
| H-04 | TerminusDB license verification; remove or admit | Legal | CRA-035, X-21 | OPEN |
| H-05 | Accept gating all standards messaging on certification (OR6) | Marketing + Legal | CRA-041 | OPEN |
| H-06 | Identify Fortuna product, API, auth and data contract | Product owner | CRA-009, X-14 | OPEN |
| H-07 | Identify the API Portal product(s) in use | Product owner | CRA-007, X-13 | OPEN |
| H-08 | Approve support tiers, response objectives, availability and service credits | Commercial + Counsel | CRA-038, X-08 | OPEN |
| H-09 | Clear extract-msg and other open component distribution terms | Legal | CRA-013/035, X-16 | OPEN |
| H-10 | Approve staffing, rates and budget inputs for the cost model | Delivery manager | CRAr section 17 | OPEN |
| H-11 | Approve vendor sandbox / licensed test access per named source | Procurement | CRA-005..009 | OPEN |
| H-12 | Patent provisional filing decisions before any public disclosure | Legal / IP | CRA-041 | OPEN |
| H-13 | Approve legal basis for Slack private channels / DMs if ever needed | Legal / Compliance | CRA-006 | OPEN |
| H-14 | Choose the durable event backbone per deployment profile (DB outbox vs Kafka/Redpanda) | Architect | CRA-010/031, INV-44 | OPEN |
| H-15 | Adopt the tiered numerical stack (N0-N3) as optional extras — **accepted 2026-10-18**: CPU-first; N0 required where probabilistic features are enabled; N1/N2 CPU-only builds; N3 research only; every binding gate qualified on CPU (`docs/decisions/ADR-H15-numerical-stack-tiers.md`; decided by the engineering agent under delegation from Ravaleedhar Reddy) | CTO / Product owner | CRA-043 | DECIDED |
| H-16 | Redistribution of CUDA `nvidia-*` packages — **decided 2026-10-18: not redistributed** in any EOIP artifact; customer-provisioned CUDA only, unqualified (`docs/decisions/ADR-H16-no-cuda-redistribution.md`; decided by Ravaleedhar Reddy) | Legal | CRA-043.2, CRA-043.3, CRA-035.9 | DECIDED |
| H-17 | Select GPU availability per deployment profile (none, optional, required) — **open**; interim CPU-only policy in force (`docs/decisions/ADR-H17-gpu-availability.md`) | CTO / Infrastructure | CRA-043.10, CRA-043.11, CRA-044.13, CRA-026.13 | OPEN |

Rows marked DECIDED are recorded in `docs/decisions/`. Import `docs/decisions/decisions-ledger-import.json` into the tracker, or merge its items into `.audit-scratch/ledger.json`, to record them in the ledger.

## 19. Traceability

### 19.1 Requirement summary

| ID | Title | P | Gate | Module | Clauses | CRAr / added |
|---|---|---|---|---|---|---|
| CRA-001 | Baseline, Decisions and Acceptance Ledger | P0 | A | M1 | 14 | 5 / 8 |
| CRA-002 | Modularity and Safe Plugin Runtime | P0 | B | M1 | 12 | 6 / 5 |
| CRA-003 | Identity, Scope and Derived-Data Authorization | P0 | B | M1 | 13 | 6 / 6 |
| CRA-004 | Connection Factory and Conformance SDK | P0 | C | M2 | 13 | 6 / 6 |
| CRA-005 | Work-Tracking and Test-System Adapters | P1 | G | M2 | 10 | 5 / 4 |
| CRA-006 | Wiki, Content, Chat and Document Repositories | P1 | G | M2 | 9 | 5 / 3 |
| CRA-007 | Code, Build, Artifact and API-Portal Adapters | P1 | G | M2 | 10 | 5 / 4 |
| CRA-008 | Observability and Operational-System Adapters | P1 | G | M2 | 10 | 5 / 4 |
| CRA-009 | Warehouses, Catalog Federation and Custom Systems | P1 | G | M2 | 9 | 5 / 3 |
| CRA-010 | Durable Source Events and Incremental Synchronization | P0 | C | M3 | 9 | 5 / 3 |
| CRA-011 | Safe Push, Crawl and Network Access | P0 | C | M3 | 9 | 5 / 3 |
| CRA-012 | Safe Text, Structured Data and Office Parsing | P0 | C | M3 | 10 | 5 / 4 |
| CRA-013 | Email, Containers and Nested Provenance | P0 | C | M3 | 9 | 5 / 3 |
| CRA-014 | Images, Audio and Video | P1 | G | M3 | 10 | 5 / 4 |
| CRA-015 | Engineering Diagram Semantics | P1 | G | M3 | 9 | 5 / 3 |
| CRA-016 | RDF Terms, Parsing and Standards Fidelity | P0 | D | M4 | 11 | 5 / 5 |
| CRA-017 | Mapping IR, RDF/LPG Projection and OBDA Inputs | P0 | D | M4 | 12 | 5 / 6 |
| CRA-018 | Durable Ontology Registry and Packages | P0 | D | M4 | 9 | 5 / 3 |
| CRA-019 | Profile-Correct Reasoning and Explanations | P0 | D | M4 | 14 | 6 / 7 |
| CRA-020 | Transactional Shape Validation | P0 | D | M4 | 12 | 6 / 5 |
| CRA-021 | Vocabulary, Taxonomy and Multilingual Stewardship | P1 | E | M5 | 9 | 5 / 3 |
| CRA-022 | Ontology and Mapping Change Governance | P1 | E | M5 | 10 | 5 / 4 |
| CRA-023 | Canonical Identity, Alignment and Reversible Resolution | P1 | E | M5 | 10 | 5 / 4 |
| CRA-024 | Typed Query, Federation and Semantic Planning | P1 | F | M5 | 12 | 6 / 5 |
| CRA-025 | Search, Embeddings and Projection Fidelity | P1 | F | M6 | 10 | 5 / 4 |
| CRA-026 | Evidence-Bound AI and Ontology Learning | P1 | F | M6 | 14 | 6 / 7 |
| CRA-027 | Governed Actions and Write-Back | P1 | G | M6 | 10 | 5 / 4 |
| CRA-028 | Temporal Knowledge, Impact and Simulation | P1 | E | M6 | 10 | 5 / 4 |
| CRA-029 | Catalog, Lineage and Enterprise Context | P1 | E | M7 | 9 | 5 / 3 |
| CRA-030 | Modular, Accessible and Truthful GUI | P1 | F | M7 | 10 | 6 / 3 |
| CRA-031 | Durable Jobs, Publication and Event Delivery | P0 | B | M8 | 8 | 5 / 2 |
| CRA-032 | Observability and Operational Truth | P0 | B | M8 | 9 | 5 / 3 |
| CRA-033 | Backup, Restore and Failure Recovery | P0 | H | M8 | 8 | 5 / 2 |
| CRA-034 | Migration, Portability and Rollback | P1 | H | M8 | 9 | 5 / 3 |
| CRA-035 | Commercial Packaging and Supply-Chain Compliance | P0 | B | M8 | 10 | 5 / 4 |
| CRA-036 | Correctness, Performance and Scale Qualification | P0 | I | M8 | 11 | 6 / 4 |
| CRA-037 | Independent QA and Evidence Verification | P0 | I | M8 | 12 | 6 / 5 |
| CRA-038 | Support, Service Objectives and Operator Readiness | P1 | I | M8 | 9 | 5 / 3 |
| CRA-039 | Public APIs, SDKs and Developer Ecosystem | P1 | H | M8 | 9 | 5 / 3 |
| CRA-040 | Privacy, Retention, Deletion and No-Egress Guarantees | P0 | B | M8 | 8 | 5 / 2 |
| CRA-041 | Truthful Positioning, Competitive Claims and Disclosure Governance | P1 | I | M9 | 8 | 0 / 7 |
| CRA-042 | Competitive Research Qualification and Maintenance | P1 | A | M9 | 8 | 0 / 7 |
| CRA-043 | Numerical Compute Stack, Determinism and Hardware Profiles | P0 | B | M10 | 12 | 0 / 11 |
| CRA-044 | Learned Graph Intelligence over the Graph Planes | P1 | F | M10 | 14 | 0 / 13 |
| CRA-045 | Deterministic–Probabilistic Boundary and Neuro-Symbolic Arbitration | P0 | F | M10 | 9 | 0 / 8 |

Totals (v3.2): 45 requirements, 417 clauses (210 verbatim from CRAr.md, 207 added), 45 acceptance obligations, 14 scenarios, 17 human decisions (2 decided), 42 conflict records, 55 research records.

### 19.2 ONT backlog -> requirements

| ONT | Title | P | Cx | Tier | Depends | Requirement | Clauses naming it |
|---|---|---|---|---|---|---|---|
| ONT-001 | W3C serialization bridge (rdflib) | P0 | M | Tier 0 — Credibility | none | CRA-016 (+CRA-034) | CRA-016.9 |
| ONT-002 | SPARQL 1.1 endpoint over the LPG store | P1 | L | Tier 1 — Differentiators | ONT-001 | CRA-024 | requirement-level |
| ONT-003 | RDF backend port (Fuseki reference) | P1 | M | Tier 1 — Differentiators | ONT-001 | CRA-024 (+CRA-002) | CRA-002.10, CRA-024.11 |
| ONT-004 | Conformant SHACL via pySHACL | P0 | S | Tier 0 — Credibility | ONT-001 | CRA-020 | requirement-level |
| ONT-005 | Connector Mapping Language (CML) | P0 | L | Tier 1 — Differentiators | ONT-001 | CRA-017 (+CRA-004/005) | requirement-level |
| ONT-006 | AI-suggested CML mappings | P1 | M | Tier 1 — Differentiators | ONT-005 | CRA-017 (+CRA-026) | CRA-017.10 |
| ONT-007 | Pluggable reasoner port (ELK default) | P0 | M | Tier 0 — Credibility | ONT-001 | CRA-019 | requirement-level |
| ONT-008 | Hybrid materialize / virtualize reasoning | P1 | M | Tier 1 — Differentiators | ONT-007 | CRA-019 | CRA-019.10 |
| ONT-009 | Governed Action layer (write-back) | P0 | L | Tier 1 — Differentiators | ONT-005 | CRA-027 | CRA-027.7 |
| ONT-010 | Ship gist, FIBO and schema.org as domain packs | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-018 | CRA-018.8 |
| ONT-011 | MCP server for ontology + Actions | P1 | S | Tier 1 — Differentiators | ONT-009 | CRA-039 | CRA-039.7 |
| ONT-012 | Position & document Ontology-as-Code | P0 | XS | Tier 1 — Differentiators | none | CRA-041 | CRA-041.4 |
| ONT-013 | Ontology pitfall scanner | P1 | M | Tier 1 — Differentiators | ONT-001 | CRA-022 | CRA-022.7 |
| ONT-014 | HTML ontology documentation generator | P2 | M | Tier 2 — Completeness | ONT-001 | CRA-039 | CRA-039.8 |
| ONT-015 | DeepOnto alignment for pack merging | P2 | L | Tier 2 — Completeness | ONT-007 | CRA-023 | CRA-023.7 |
| ONT-016 | SKOS RDF import / export | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-021 | CRA-021.6 |
| ONT-017 | R2RML / RML import to CML | P2 | M | Tier 2 — Completeness | ONT-005 | CRA-034 (+CRA-017) | CRA-017.7, CRA-034.8 |
| ONT-018 | PROV-O provenance on every mined triple | P1 | M | Tier 2 — Completeness | ONT-005 | CRA-017 | CRA-017.9 |
| ONT-019 | OWL round-trip certification CI gate | P1 | S | Tier 2 — Completeness | ONT-001 | CRA-016 (+CRA-037/041) | CRA-016.9, CRA-016.10, CRA-041.2 |
| ONT-020 | Ontology benchmark harness | P1 | M | Tier 2 — Completeness | ONT-002 | CRA-036 | CRA-036.7 |

### 19.3 OCA inversions I1-I20 -> requirements

| I | Competitor con | Who | EOIP inversion | Requirements | Status rule |
|---|---|---|---|---|---|
| I1 | RDF cannot give identity to parallel same-type relationships; reification bloat | All triplestores | Native LPG — edges have identity + properties with zero overhead. "No reification tax." | CRA-016/017/041 | Hypothesis: re-verify then claim via CRA-041 |
| I2 | SPARQL reasoning has no termination guarantee | Triplestores | Hard token/time budgets with graceful degradation via `token_budget/` + control loops | CRA-024 | Build |
| I3 | Triplestores are weak at traversal | Conceded by Ontotext | Traversal-native: `paths.py`, `algorithms.py`, `community.py`, `process_mining.py` | CRA-024/036/041 | Hypothesis: re-verify then claim via CRA-041 |
| I4 | Forward-chaining stalls on TBox change (full recompute) | GraphDB | Hybrid: materialize stable inferences, rewrite volatile ones at query time | CRA-019 | Build |
| I5 | Query-time reasoning costs per-query latency | Stardog, Ontop | Same hybrid, decided per-rule by cost model | CRA-019 | Build |
| I6 | Ontology tools assume the data has already arrived | Protégé, TopBraid, VocBench | 38 connectors + universal factory + crawler; the ontology comes to the data | CRA-004/041 | Hypothesis: re-verify then claim via CRA-041 |
| I7 | OBDA limited to OWL 2 QL over relational sources | Ontop | CML maps *any* connector payload; per-source materialize/virtualize choice | CRA-017 | Build |
| I8 | New source = new hand-written integration | Everyone | New source = a YAML file | CRA-004/017 | Build |
| I9 | ML-assisted mapping never productized | Karma | AI-suggested mappings from sampled payloads | CRA-017/026 | Build |
| I10 | Proprietary formats; migration out is hard | Palantir, Reltio, Collibra | Every artifact exports to an open standard | CRA-016/020/034 | Build |
| I11 | High TCO; per-seat pricing cliffs | Palantir, MarkLogic | Self-hostable, 4-tier, published TCO calculator | CRA-035/038/041 | Build |
| I12 | Months-to-a-year implementation; manual relationship modeling | Palantir | Ontology induction mines the model, humans curate it | CRA-017/026 | Build |
| I13 | Agent tooling described as basic | Palantir AIP | 35 agents, 14 control loops, 9 reasoning strategies, verification engine | CRA-026/041 | Hypothesis: re-verify then claim via CRA-041 |
| I14 | Ontology CI/CD requires assembling 4+ separate CLI tools | ROBOT+pySHACL+OOPS!+Widoco | One integrated governed workflow | CRA-022/039 | Build |
| I15 | Change workflow without version-control semantics | TopBraid EDG | Branch/PR/merge/semver/rollback-receipt | CRA-018/022/041 | Hypothesis: re-verify then claim via CRA-041 |
| I16 | No migration scripts generated on schema change | All | `generate_ontology_migration_script` | CRA-022/041 | Hypothesis: re-verify then claim via CRA-041 |
| I17 | Ontology silently drifts from reality | All | `drift.py` + `embedding_drift.py` detect and propose evolution | CRA-021/041 | Hypothesis: re-verify then claim via CRA-041 |
| I18 | Catalogs describe but cannot reason | Collibra, Alation, Atlas | Catalog + ontology + reasoner + agents in one system | CRA-019/029 | Build |
| I19 | WebProtégé is AGPL; Neo4j CE is GPLv3; Virtuoso is GPLv2 | — | Permissive-only dependency policy; ELK over HermiT; Fuseki over Neo4j as reference | CRA-035 | Build |
| I20 | Life-science / publishing verticals locked to specialist tools | SciBite, Data Harmony | Domain packs + industry templates make verticals a config artifact | CRA-018 | Build |

### 19.4 Competitive landscape C01-C55 -> inversion -> requirements

Evidence scores are from `competitive-research-matrix.csv` (D01 core, D03 model, D04 reasoning, D05 interop, D15 differentiators; ND = not determined). Indicative mean is from `ontology-comparison-matrix.csv` and is not audited. Neither may be averaged with the other.

| ID | Tool family | Category | D01 | D03 | D04 | D05 | D15 | Indicative mean | Indicative lesson | INV | Requirements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | Protege / WebProtege | 1_authoring | 4 | 4 | 4 | 4 | 4 | 3.3 / 3.3 | Reasoner port + round-trip target / AGPL - never integrate | INV-01 | CRA-016/018/019/022/030 |
| C02 | TopBraid Composer | 1_authoring | 4 | 4 | 3 | 4 | 3 | 3.4 | Eclipse IDE pattern | INV-02 | CRA-018/020/022/035/039 |
| C03 | OntoStudio / OntoStudio X | 1_authoring | 3 | 3 | 3 | 3 | 4 | 2.7 | F-Logic rules - declining | INV-03 | CRA-017/019/022/024/030 |
| C04 | Fluent Editor | 1_authoring | 3 | 4 | 3 | 3 | 4 | 2.7 | Controlled Natural Language idea worth stealing | INV-04 | CRA-019/021/022/026/030 |
| C05 | Ontosphere | 1_authoring | 3 | 4 | 4 | 4 | 4 | 3.2 | MCP hook for agents - becoming table stakes | INV-05 | CRA-002/003/019/027/030/035/039 |
| C06 | Graphologi | 1_authoring | 4 | 4 | ND | 3 | 3 | 3.2 | Polyhierarchy UX | INV-06 | CRA-018/020/021/030/034 |
| C07 | Chowlk / OnToology | 1_authoring | 3 | 4 | ND | 4 | 4 | 3.0 | Overlaps GitOps - EOIP is a superset | INV-07 | CRA-015/017/022/035/037 |
| C08 | TopBraid EDG | 2_governance | 4 | 4 | 3 | 4 | 4 | 3.8 | Closest competitor - SHACL as universal metamodel | INV-08 | CRA-002/018/020/022/030/039 |
| C09 | VocBench 3 | 2_governance | 4 | 4 | ND | 4 | 4 | 3.4 | Multilingual RBAC workflow | INV-09 | CRA-018/021/022/025/030 |
| C10 | PoolParty / Graphwise | 2_governance | 4 | 4 | 3 | 4 | 4 | 3.6 | NLP-driven taxonomy expansion + GraphRAG | INV-10 | CRA-002/021/025/026/035/039 |
| C11 | Progress Semaphore | 2_governance | 4 | 3 | 3 | 3 | 4 | 3.3 | PII redaction at petabyte scale | INV-11 | CRA-021/022/026/036/040 |
| C12 | Synaptica Graphite | 2_governance | 4 | 4 | ND | 4 | 4 | 3.0 | ISO 25964 crosswalk mapping | INV-12 | CRA-021/022/025/031/033 |
| C13 | SciBite CENtree / TERMite | 2_governance | 4 | 4 | ND | 3 | 4 | 3.3 | Vertical depth = domain pack pattern | INV-13 | CRA-021/023/026/035/036 |
| C14 | Data Harmony | 2_governance | 3 | 3 | ND | 3 | 3 | 2.8 | Rule-based indexing | INV-14 | CRA-021/022/026/034/036 |
| C15 | Semantic Arts / gist | 2_governance | 3 | 4 | ND | 4 | 4 | 3.2 | ADOPT as domain pack - solves root-class problem | INV-15 | CRA-018/021/022/034/035 |
| C16 | Reltio Ontology Builder | 2_governance | 3 | 3 | ND | 3 | 4 | 3.3 | MDM schema-to-ontology automation | INV-16 | CRA-017/022/024/026/034 |
| C17 | GraphDB | 3_storage_reasoning | 4 | 4 | 4 | 4 | 4 | 4.0 | Forward-chaining materialization; certify as backend | INV-17 | CRA-019/020/024/036 |
| C18 | Stardog / Studio | 3_storage_reasoning | 4 | 4 | 4 | 4 | 4 | 4.0 | Query-time reasoning + proof trees + virtual graphs | INV-18 | CRA-019/024/029/036 |
| C19 | AllegroGraph | 3_storage_reasoning | 4 | 4 | 4 | 4 | 4 | 3.6 | Neuro-symbolic: Prolog + vectors | INV-19 | CRA-003/019/024/025/036 |
| C20 | Apache Jena / TDB2 / Fuseki | 3_storage_reasoning | 4 | 4 | 3 | 4 | 4 | 3.6 | REFERENCE RDF BACKEND - zero license risk | INV-20 | CRA-003/016/019/020/033/036 |
| C21 | Virtuoso | 3_storage_reasoning | 4 | 4 | 3 | 4 | 4 | 3.3 | GPLv2 - network boundary only | INV-21 | CRA-002/017/024/035/036 |
| C22 | Eclipse RDF4J | 3_storage_reasoning | 4 | 4 | 3 | 4 | 4 | 3.6 | Sail pluggable-storage architecture = port pattern | INV-22 | CRA-019/020/022/031/036 |
| C23 | Amazon Neptune | 3_storage_reasoning | 4 | 4 | ND | 4 | 4 | 3.8 | Managed ops; weak inference | INV-23 | CRA-002/003/017/024/033/035 |
| C24 | MarkLogic | 3_storage_reasoning | 4 | 4 | 3 | 4 | 4 | 3.4 | Universal index across JSON/XML/RDF | INV-24 | CRA-003/010/029/040 |
| C25 | TerminusDB | 3_storage_reasoning | 4 | 3 | 3 | 3 | 4 | 3.0 | Git-like data versioning - BLOCKED pending Legal | INV-25 | CRA-018/022/028/033/040 |
| C26 | Neo4j / n10s | 3_storage_reasoning | 4 | 4 | 3 | 4 | 4 | 3.5 | GPLv3 - never link; wire-protocol only | INV-26 | CRA-016/017/020/024/034 |
| C27 | Ontop | 4_obda_mapping | 4 | 4 | 4 | 4 | 4 | 3.3 | OBDA unfold-optimize-emit = CML blueprint | INV-27 | CRA-017/019/024/036 |
| C28 | Timbr | 4_obda_mapping | 4 | 3 | 3 | 4 | 4 | 3.3 | SQL-native semantic views for BI tools | INV-28 | CRA-017/024/029/030/035 |
| C29 | Anzo / AnzoGraph | 4_obda_mapping | 4 | 4 | ND | 4 | 4 | 3.6 | MPP distributed graph compute | INV-29 | CRA-002/024/031/036 |
| C30 | Morph-KGC | 4_obda_mapping | 4 | 4 | ND | 4 | 4 | 3.0 | Vectorized Pandas triple materialization | INV-30 | CRA-002/017/031/036 |
| C31 | RMLStreamer / SDM-RDFizer | 4_obda_mapping | 4 | 4 | ND | 4 | 4 | 3.0 | Streaming RML over Kafka/Flink | INV-31 | CRA-010/017/031/036 |
| C32 | Karma | 4_obda_mapping | 3 | 4 | ND | 4 | 4 | 2.7 | ML-assisted mapping - never productized; EOIP should | INV-32 | CRA-017/022/030/034/035 |
| C33 | Palantir Foundry / AIP | 5_operational | 4 | 3 | ND | 3 | 4 | 4.0 | Ontology as agent safety boundary + Actions layer | INV-33 | CRA-018/024/027/034/039 |
| C34 | Microsoft Fabric / IQ | 5_operational | 4 | 3 | ND | 3 | 4 | 3.9 | Bundling distribution advantage | INV-34 | CRA-002/017/022/024/026/034 |
| C35 | Oracle graph / AI Data Platform | 5_operational | 4 | 4 | 3 | 4 | 4 | 4.0 | Trillion-triple scale inside the DB | INV-35 | CRA-002/017/024/034/035/036 |
| C36 | Cosmo Tech | 5_operational | 3 | 3 | ND | 3 | 4 | 3.1 | Simulation over ontology graph | INV-36 | CRA-027/028/031/036 |
| C37 | Cinchapi Concourse | 5_operational | 4 | 3 | ND | 3 | 4 | 3.0 | Temporal/time-travel operational records | INV-37 | CRA-016/023/028/033/040 |
| C38 | Essential Cloud | 5_operational | 4 | 3 | ND | 3 | 4 | 2.8 | EA meta-model for capability mapping | INV-38 | CRA-010/022/028/029/030 |
| C39 | OpenMetadata | 6_catalogs | 4 | 3 | ND | 4 | 4 | 3.7 | MCP server pattern - study it | INV-39 | CRA-001/003/025/029/031/039 |
| C40 | data.world | 6_catalogs | 4 | 4 | ND | 4 | 4 | 3.7 | RDF-native catalog backplane | INV-40 | CRA-010/022/028/029/034 |
| C41 | Collibra | 6_catalogs | 4 | 3 | ND | 4 | 4 | 3.6 | Governance workflow depth | INV-41 | CRA-002/022/027/031/039 |
| C42 | Alation | 6_catalogs | 4 | 3 | ND | 4 | 4 | 3.3 | Behavioral intelligence from query logs | INV-42 | CRA-004/009/024/029/040 |
| C43 | OvalEdge | 6_catalogs | 4 | 3 | ND | 3 | 4 | 3.0 | Automated synonym resolution agents | INV-43 | CRA-003/004/009/027/029/040 |
| C44 | DataHub | 6_catalogs | 4 | 3 | ND | 4 | 4 | 3.5 | Kafka event-driven metadata streaming | INV-44 | CRA-002/010/029/031/032/039 |
| C45 | Apache Atlas | 6_catalogs | 4 | 3 | ND | 4 | 4 | 2.8 | Typed meta-model + classification tags | INV-45 | CRA-002/009/029/031/033/035 |
| C46 | ROBOT | 7_ontology_ci | 4 | 4 | 4 | 4 | 4 | 3.1 | CLI ontology build pipeline | INV-46 | CRA-018/019/022/035/037 |
| C47 | pySHACL | 7_ontology_ci | 4 | 4 | 3 | 4 | 4 | 2.8 | ADOPT - reference SHACL implementation | INV-47 | CRA-002/020/031/035/037 |
| C48 | TopBraid SHACL API | 7_ontology_ci | 4 | 4 | 3 | 4 | 4 | 2.8 | JVM only - not needed for Python stack | INV-48 | CRA-002/019/020/022/037 |
| C49 | OOPS! | 7_ontology_ci | 3 | 3 | ND | 3 | 4 | 2.5 | BUILD EQUIVALENT - ONT-013 | INV-49 | CRA-020/022/026/035/037/040 |
| C50 | WIDOCO / LODE | 7_ontology_ci | 4 | 4 | ND | 4 | 4 | 2.6 | BUILD EQUIVALENT - ONT-014 | INV-50 | CRA-018/022/030/035/039 |
| C51 | Mondeca suite / CAM | 8_enrichment | 4 | 4 | 3 | 4 | 4 | 3.0 | Content-to-ontology auto-classification | INV-51 | CRA-014/021/026/030/040 |
| C52 | Diffbot | 8_enrichment | 4 | 3 | ND | 3 | 4 | 3.4 | Autonomous web-to-entity extraction | INV-52 | CRA-010/014/023/026/035/040 |
| C53 | DeepOnto | 8_enrichment | 4 | 4 | 4 | 4 | 4 | 2.9 | ADOPT - BERT ontology alignment + subsumption prediction | INV-53 | CRA-019/022/023/026/036 |
| C54 | spaCy / textacy | 8_enrichment | 4 | 2 | ND | 3 | 4 | 3.3 | Entity linking pipeline to custom KB | INV-54 | CRA-021/023/026/035/036 |
| C55 | OWL API | supplemental_library | 4 | 4 | 3 | 4 | 4 | — | — | INV-55 | CRA-002/016/018/019/035 |

### 19.5 Research backlog B01-B17 (competitive-research-analysis.md section 7) -> requirements

| Backlog | P | Scope and acceptance summary | Inversions addressed | Requirements |
|---|---|---|---|---|
| B01 | P0 | Versioned contracts, decision records, truthful capability discovery and qualified plugin execution | INV 05, 08, 10, 21, 23, 29, 39, 44, 45, 55 | CRA-001/002/039 |
| B02 | P0 | Identity/workspace/source ACL policy enforced across data, derivations, indexes, jobs and exports | INV 05, 19, 20, 24, 39, 43 | CRA-003/010/040 |
| B03 | P0 | Existing connection factory audited; explicit fallbacks, vendor auth, sandboxed push/pull, conformance suite | INV 07, 27, 31, 42, 43, 45 | CRA-004..011 |
| B04 | P0 | Bounded safe parsers and dependency readiness; no silent data loss or unbounded chunk loop | INV 07, 30, 49, 51, 52 | CRA-012..015 |
| B05 | P0 | Standards-based RDF term fidelity and explicit LPG mapping losses | INV 01, 03, 16, 23, 26, 35, 55 | CRA-016/017 |
| B06 | P0 | Real profile-qualified reasoning and constraint enforcement, including unsupported/error states | INV 01, 04, 17, 18, 20, 22, 46, 47, 48, 55 | CRA-019/020 |
| B07 | P1 | Durable ontology registry, governed changes, term stewardship and migration | INV 02, 06, 08, 09, 10, 12, 13, 14, 15, 16, 25, 32, 34, 46, 49, 50 | CRA-018/021/022/034 |
| B08 | P1 | Identity resolution with evidence, reversible merge/split and inferred-dependency repair | INV 13, 25, 37, 52, 53, 54 | CRA-023/028/040 |
| B09 | P1 | Scoped bounded query/federation with visible plans and qualified dialects | INV 03, 18, 19, 21, 23, 27, 28, 29, 35 | CRA-024 |
| B10 | P1 | Real versioned retrieval and evidence-bound AI with no hidden provider fallback | INV 04, 10, 11, 14, 16, 39, 51, 52, 53, 54 | CRA-025/026 |
| B11 | P1 | Governed operational actions and honest temporal/simulation capabilities | INV 33, 36, 37, 38, 41, 43 | CRA-027/028 |
| B12 | P1 | Catalog/context/lineage with observed versus curated precedence and freshness | INV 18, 24, 28, 38, 39, 40, 42, 43, 44, 45 | CRA-029 |
| B13 | P1 | Complete accessible modular UI flows and customization across supported profiles | INV 01, 03, 06, 09, 16, 28, 32, 38, 50, 51 | CRA-030 |
| B14 | P0 | Durable jobs, replay/outbox, truthful telemetry and tested restore | INV 12, 20, 23, 25, 29, 30, 31, 36, 39, 41, 44, 45 | CRA-031..033 |
| B15 | P0 | Commercial distribution, SBOM, signed packages, no unlawful dependency relabelling | INV 02, 05, 13, 15, 21, 32, 35, 46, 49, 50, 54, 55 | CRA-035 |
| B16 | P0 | Independent correctness/performance/security qualification and content-bound receipts | INV 01..55,  especially 17, 22, 27, 46, 47, 48 | CRA-036/037 |
| B17 | P1 | Honest support/service commitments, SDK/developer ecosystem and operator handoff | INV 02, 10, 23, 35, 41, 44, 45, 50 | CRA-038/039 |

### 19.6 Requested deliverables (original attachment) -> location

| # | Deliverable | Where satisfied | Open limitation |
|---|---|---|---|
| 1 | Executive summaries and verdict | Section 1; dossiers in `competitive-research-analysis.md` C01-C55 (retained as input) | Hands-on product validation (CRA-042) |
| 2 | Technical dossier | Sections 8-11; source dossiers | Closed-source internals unknown |
| 3 | Markdown + CSV matrix | Section 19.4; dashboard; both CSVs | ND values unresolved (CRA-042) |
| 4 | Gap backlog | Section 4.2; requirements | — |
| 5 | Designs/API/schema/UX | Sections 6, 8, 11; implementation doc | Proposed until receipted |
| 6 | Migration/integration | CRA-034; section 9 | CLI to be built |
| 7 | Security/legal/compliance | Sections 12-13; CRA-035/040 | Not legal certification |
| 8 | Performance plan | Sections 5.2, 14; CRA-036 | No results invented |
| 9 | Observability/ops | Section 15; CRA-032/038 | Drills pending |
| 10 | QA plan | Section 14; CRA-037 | — |
| 11 | Roadmap/cost | Section 16 | Rates/staff inputs (H-10) |
| 12 | Playbooks | Section 15 | Operator rehearsal |
| 13 | Support/SLA | Section 15; CRA-038 | Human approval H-08 |
| 14 | Ecosystem strategy | CRA-039 | Not launched |
| 15 | Cons-to-pros | Sections 19.3-19.4 | Hypotheses labelled |
| 16 | Appendices/reproduction | Sections 0, 20 | External evaluations open |

### 19.7 Graph-Neurons requirements -> requirements (v3.1)

`GN-REQ-v1` remains the detailed engineering reference; acceptance is tracked only through the clauses below.

| GN | Title (abridged) | Requirement clauses | Note |
|---|---|---|---|
| GN-010 | Numerical stack provisioning and platform matrix | CRA-043.1, 043.2, 043.3, 043.10, 043.11 | Tiers N0-N3, CPU-only distribution (H-16) |
| GN-011 | Array backend and dtype discipline | CRA-043.5 | float32 storage, no Python loops |
| GN-012 | Determinism and reproducibility | CRA-043.6 | Cross-process 1e-4 gate (section 5.3) |
| GN-013 | BLAS thread governance | CRA-043.7 | Set before numpy import |
| GN-014 | Air-gapped installation | CRA-043.3 | Wheel bundle + hash lock |
| GN-015 | Numerical correctness and stability | CRA-043.8 | — |
| GN-016 | Memory and tensor lifecycle | CRA-043.9 | Refuse before allocation |
| GN-001 | Neural runtime and degradation contract | CRA-043.4 | X-39 |
| GN-002 | Assertion contract (prediction is not fact) | CRA-044.12, CRA-045.2 | X-34 |
| GN-003 | Anti-stub harness | CRA-044.3, CRA-037.11 | Must fail the hash stub |
| GN-004 | Versioned feature and embedding store | CRA-044.9, CRA-025.8 | X-41 |
| GN-005 | Snapshots, temporal splits, negative sampling | CRA-044.4 | — |
| GN-006 | Evaluation harness and calibration | CRA-044.5, CRA-036.10 | X-37 |
| GN-007 | Model registry, promotion, rollback | CRA-044.9 | — |
| GN-101, GN-102 | R-GCN (replaces hash stub), GraphSAGE | CRA-044.1, 044.6, CRA-025.9 | X-40 |
| GN-103, GN-104, GN-201, GN-202 | R-GAT, HGT, graph transformer, path-aware attention | CRA-044.7 | Bake-off gated |
| GN-203 | Natural-language bridge | CRA-026, CRA-045.3 | Grounded, cited, dual path |
| GN-301, GN-302, GN-303 | GRU/LSTM, TGN, RE-Net | CRA-044.7, CRA-028.9 | Bake-off gated |
| GN-401, GN-402, GN-403 | ChebNet, ConvE, vision bridge | CRA-044.7, CRA-015 | Bake-off gated |
| GN-501 | Adversarial quality discriminator | CRA-044.8 | After CRA-044.6 |
| GN-502, GN-601 | Triple generator, spiking encoder | CRA-044.8 | Research sandbox |
| GN-701 | Explainability | CRA-044.10 | Faithfulness probe |
| GN-702 | Fusion and arbitration | CRA-045.3 | DISPUTED surfaced |
| GN-703 | Security and entitlements | CRA-003, CRA-044.A | Membership-inference probe |
| GN-704 | API surface | Section 11 | X-38 |
| GN-705 | Performance budgets | CRA-036 | Manifest targets |
| GN-706 | Known failure-mode guards | CRA-044.11 | — |

## 20. Reproduction Probe and Independent Semantic Fixture

Baseline defect probe (run from repository root, PowerShell; it reproduces the defect and is not a passing acceptance test):

```powershell
$env:PYTHONPATH='.;packages'
python -c "from types import SimpleNamespace; from eoip.ontology.shacl_validator import SHACLValidator, SHACLShape; from eoip.ontology.rdf import OWLReasoner; v=SHACLValidator(); v.shapes={}; v.register_shape(SHACLShape(shape_id='count',target_class='Service',min_counts={'name':2},max_counts={'tag':1})); s=SimpleNamespace(find_vertices=lambda:[{'label':'Service','canonical_id':'urn:test:a','properties':{'name':'only-one','tag':['a','b']}}]); print(v.validate(s).to_dict()); print(v._check_datatype('text','unsupported_type')); print(OWLReasoner().is_subclass_of('urn:example:A','urn:example:a'))"
```

Bash equivalent: `PYTHONPATH=.:packages python -c "<same program>"`.

Observed at the source baseline: zero violations / `conforms` true; unknown datatype true; case-distinct subclass true. After remediation: invalid cardinalities rejected, unsupported datatypes explicit errors, distinct IRIs never equated without an axiom. Test each separately.

Fixture files (materialize under `tests/fixtures/semantic/independent/`; they were not engine-executed by the source research):

`ontology.ttl`

```turtle
@prefix ex: <urn:example:> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:Ontology a owl:Ontology .
ex:Service a owl:Class .
ex:Database a owl:Class ; rdfs:subClassOf ex:Service .
ex:Person a owl:Class ; owl:disjointWith ex:Service .
ex:name a owl:DatatypeProperty ; rdfs:range xsd:string .
ex:dependsOn a owl:ObjectProperty, owl:TransitiveProperty .
```

`data.ttl`

```turtle
@prefix ex: <urn:example:> .
ex:Orders a ex:Service ; ex:name "Orders" ; ex:dependsOn ex:Ledger .
ex:Ledger a ex:Database ; ex:name "Ledger" ; ex:dependsOn ex:Cache .
ex:Cache a ex:Service ; ex:name "Cache" .
```

`shapes.ttl`

```turtle
@prefix ex: <urn:example:> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:ServiceShape a sh:NodeShape ;
  sh:targetClass ex:Service ;
  sh:property [ sh:path ex:name ; sh:datatype xsd:string ;
                sh:minCount 1 ; sh:maxCount 1 ] .
```

Expected under RDFS + transitivity: `ex:Ledger a ex:Service` and `ex:Orders ex:dependsOn ex:Cache`; data conform. Add a second name to Orders -> maxCount violation. Remove its name -> minCount violation (note: whether `ex:Ledger` is a validation target depends on whether validation runs over the inferred closure; the test must declare that mode). Add `ex:Orders a ex:Person` -> inconsistency under disjointness (separate from shape validation). `urn:example:A` and `urn:example:a` remain distinct terms.

Normative references: [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/), [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/), [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/), [SHACL](https://www.w3.org/TR/shacl/), [SPARQL 1.1 Overview](https://www.w3.org/TR/sparql11-overview/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## 21. Source Coverage Statement

| Source | Section(s) | Where it lands here |
|---|---|---|
| CRAr.md | 1 Objective | Section 1 |
| CRAr.md | 2 Completion contract, 2.2 evidence record | Section 2 (union schema) |
| CRAr.md | 3 Agent protocol | Section 3; implementation doc section 1 |
| CRAr.md | 4 Defaults, quality gates | Sections 5.1-5.3 |
| CRAr.md | 5 Contracts | Section 6 |
| CRAr.md | 6 CRA-001..040 (210 clauses) | Section 7, verbatim with original numbers |
| CRAr.md | 7 Programme gates, 8 scenarios, 9 handoff | Sections 16.1, 17 |
| CRAragg.md | 1.1-1.3 mission, contract, receipt schema | Sections 1, 2.3 |
| CRAragg.md | 2 Pydantic contracts | Section 6 (merged, utcnow fixed) |
| CRAragg.md | 3 CRA-001..040 specs + verification | Appended `[AGG]` clauses and acceptance in section 7 |
| CRAragg.md | 4 Autonomous protocol | Section 3; implementation doc |
| competitive-research-analysis.md | 1-2 decision, scope, evidence labels | Sections 0, 1, 2 |
| competitive-research-analysis.md | 3 baseline, G01-G18 | Section 4 |
| competitive-research-analysis.md | 4 profiles | Section 5.2 |
| competitive-research-analysis.md | 5 rubric/matrix | Section 19.4; CRA-042; dashboard |
| competitive-research-analysis.md | 6 dossiers C01-C55, INV-01..55, version register | Section 19.4; CRA-042; tracker research items |
| competitive-research-analysis.md | 7 backlog B01-B17 | Gates and requirements (section 16) |
| competitive-research-analysis.md | 8-11 architecture, connectors, formats, designs, API, UX | Sections 8-11; implementation doc |
| competitive-research-analysis.md | 12-17 migration, security, benchmark, observability, playbooks, roadmap | CRA-034; sections 12-16 |
| competitive-research-analysis.md | 18-19 deliverables, reproduction | Sections 19.5, 20 |
| competitive-research-analysis-agg.md | Executive summary, top 5 inversions | Sections 1, 19.4 (as hypotheses) |
| competitive-research-analysis-agg.md | 2 rubric (22 dims) | CRA-042; dashboard (aggregated dataset) |
| competitive-research-analysis-agg.md | 3 dossiers + INV blueprints | Section 19.4; CRA-042 |
| competitive-research-analysis-agg.md | 4 master matrix | Dashboard dataset 'Aggregated'; CRA-042.2 |
| competitive-research-analysis-agg.md | 5 architecture, connection factory, formats, 8 graph planes, neuro-symbolic cycle | Sections 8-10 |
| competitive-research-analysis-agg.md | 6 contracts, HTRE algorithm, OpenAPI | Section 6; CRA-019; section 11 |
| competitive-research-analysis-agg.md | 7-13 migration, threat, sizing, telemetry, playbooks, support, roadmap/cost | CRA-034; sections 12-16 |
| ontology-competitive-analysis.md | 0 verdict, F1-F5, top 5, don't-build | Sections 1, 4.2 |
| ontology-competitive-analysis.md | 1 measured baseline, constraints | Section 4.1; CRA-001; H-01 |
| ontology-competitive-analysis.md | 2 rubric, EOIP self-assessment | CRA-041/042; dashboard |
| ontology-competitive-analysis.md | 3 category reconstructions, CML sketch | CRA-017; sections 8-9 |
| ontology-competitive-analysis.md | 4 ONT-001..020 | Section 19.2; `[OCA]` clauses |
| ontology-competitive-analysis.md | 5 I1-I20 | Section 19.3 |
| ontology-competitive-analysis.md | 6 module layout, API, LPG<->RDF scheme | Sections 8.4, 11; CRA-017 |
| ontology-competitive-analysis.md | 7 benchmarks | Section 14; CRA-036 |
| ontology-competitive-analysis.md | 8 licensing, threats, patents | Sections 12-13; CRA-035/041 |
| ontology-competitive-analysis.md | 9 roadmap, OR1-OR7 | Section 16.2; CRA-016/022/035/041 |
| ontology-competitive-analysis.md | 10 evidence index, sources, open questions | Section 4; H-01..H-05 |
| ontology-analysis-dashboard.html | Scorecard, backlog, inversions, gaps | Updated dashboard + tracker |
| competitive-research-matrix.csv | 55 rows | Section 19.4; dashboard; tracker R-items |
| ontology-comparison-matrix.csv | 58 rows | Section 19.4 indicative mean; dashboard |
| crarprompt.txt | Closing instruction: deterministic semantics plus probabilistic AI | Section 1; CRA-045; CRA-026.10-026.12; G21 |
| Graph-Neurons-requirements.md | 0.3 hash-stub finding; 0.5 measured baseline | G19, G20; CRA-001.13; CRA-044.1; CRA-025.9 |
| Graph-Neurons-requirements.md | 1.3, 3.1 GN-010..GN-016 numerical stack | CRA-043; section 13 |
| Graph-Neurons-requirements.md | 2, 3.2-10 GN-001..GN-007, GN-101..GN-706 | CRA-044, CRA-045; appended `[GN]` clauses; section 19.7 |
| Graph-Neurons-implementation-plan.md | Phases, evidence ledger, prohibitions, risks NR1-NR18 | Implementation guide WP-043..WP-045; X-35, X-36 |

## 22. Change Log

### v3.2-COMBINED (2026-10-18)

| Change | Where | Reason |
|---|---|---|
| H-15 **accepted**: tiered CPU-first numerical stack as optional extras; N3 never shipped to customers | Section 18.2; `docs/decisions/ADR-H15-numerical-stack-tiers.md` | Decision delegated to the engineering agent by the owner |
| H-16 **accepted**: CUDA `nvidia-*` packages are not redistributed in any artifact | CRA-043.2, CRA-043.3, CRA-035.9, section 13; `ADR-H16-no-cuda-redistribution.md` | Owner decision: redistribution not possible |
| H-17 **open**; interim CPU-only policy | CRA-043.10; new CRA-043.11, CRA-044.13, CRA-026.13; section 5.2 accelerator row; `ADR-H17-gpu-availability.md` | GPU availability unknown |
| Status column added to the decisions table | Section 18.2 | Make decided and open items explicit |
| Install-size figures replaced by measured budgets (N0 <= 150 MB, N1 CPU <= 2.5 GB) | CRA-043.1 | Earlier ~70 MB and ~2 GB figures were unmeasured; ~2 GB described CUDA builds |
| Graph-Neurons documents revised to v1.1 and their SHA-256 refreshed | Section 0.1 rows 10-11 | Keep the engineering reference consistent with the decisions |
| Gate B/F exit evidence, E14 and section 16.3 updated for CPU-only qualification | Sections 16, 17 | Consequence of H-16 and H-17 |

### v3.1-COMBINED (2026-10-18)

| Change | Where | Reason |
|---|---|---|
| Module M10 with CRA-043 (numerical stack), CRA-044 (learned graph intelligence), CRA-045 (deterministic–probabilistic boundary) | Section 7.10 | Closing instruction of `crarprompt.txt` had no owning requirement; Graph-Neurons specification not yet combined |
| 12 appended clauses: CRA-001.13, 014.9, 023.9, 025.8-025.9, 026.10-026.12, 028.9, 035.9, 036.10, 037.11 | Section 7 | Existing requirements depended on capabilities v3.0 did not specify |
| Gaps G19 (hash-based GNN), G20 (no numerical stack), G21 (unowned boundary) | Section 4.2 | Repository measurement at `d771fd6` and prompt trace |
| Conflicts X-34..X-42; decisions H-15..H-17; scenarios E13-E14 | Sections 17, 18 | Graph-Neurons vs this specification reconciled explicitly |
| CRA-005.8 origin `[CRAr]` -> `[AGG]` | CRA-005 | Text originates in `competitive-research-analysis-agg.md`; CRAr.md has five CRA-005 clauses. Restores the 210-verbatim count stated in section 0.2 |
| Re-measured facts (302 test files vs 239 asserted; connector-file composition; numerical stack absent) | Section 4.1; CRA-001.13 | CRA-001.11 records discrepancies instead of correcting sources |
| CRA-001.10 coverage ranges extended | CRA-001 | Ledger must cover the new items |
| Section 19.1 counts regenerated; section 19.7 GN map added | Section 19 | Traceability |
| Sources 9-11 added with SHA-256 | Section 0.1 | Provenance |
| The previous `EOIP-engg-doc-pkg/ontology-analysis-dashboard.html` (source 6, SHA `1109fa46…`) remains recoverable from git commit `a9d1c0f`; that path now carries a synchronized copy of the combined dashboard | Companion files | The previous version showed 'already won' inversions and unlabelled self-scores that CRA-041.3/041.7 prohibit externally |

*End of requirements document. Completion is observable, reproducible and authorized behaviour in the actual supported deployment — not the volume of code or documentation produced.*
