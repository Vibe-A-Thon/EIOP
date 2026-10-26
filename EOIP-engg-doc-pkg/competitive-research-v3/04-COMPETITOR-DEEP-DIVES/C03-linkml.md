| Field | Value |
|---|---|
| Registry ID | T-C03-linkml |
| Tier | B (schema-as-code; ontology-as-code reference) |
| Versions examined | linkml 1.12.1 (2026-10-13); 1.12.0 (2026-10-08); 1.11.1 (2026-05-20); 1.11.0 yanked |
| Verified on | 2026-10-26 (actual access date) |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
LinkML ("Linked Open Data Modeling Language") is a YAML-based, object-oriented modelling language and Python toolchain, repo `linkml/linkml`, Apache-2.0, Python >=3.10 [CLAIM-linkml-01]. Releases are frequent: 1.12.0rc1 2026-10-02, 1.12.0 2026-10-08, 1.12.1 2026-10-13; 1.11.0 (2026-05-13) was yanked ("release grounded to wrong commit") [CLAIM-linkml-02]. Repo shows ~668 stars. Governance, funding and steering body: NOT VERIFIED here. Tier B: reference for the ontology-as-code inversion.
Sources: PyPI JSON `https://pypi.org/pypi/linkml/json`; `https://github.com/linkml/linkml`; `https://linkml.io/linkml/generators/index.html`.

## 2. Problem, workloads, workflows
One YAML schema (classes, slots, enums, types, mixins, `is_a` inheritance, rules, expressions) generates many artefacts so data models do not drift. Workflows: author schema in Git; CI runs `gen-*` generators and `linkml-validate`; downstream teams get Pydantic/JSON Schema/SQL DDL/SHACL/OWL from one source. Heavily used by biomedical and research-data projects (adoption breadth NOT quantified here).

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| YAML metamodel with inheritance, mixins, enums, constraints | present | [CLAIM-linkml-01] |
| Generators: JSON Schema, ProtoBuf, GraphQL, OpenAPI | present | [CLAIM-linkml-03] |
| Generators: JSON-LD context/JSON-LD, RDF, SPARQL, ShEx, SHACL, OWL, YARRRML | present | [CLAIM-linkml-03] |
| Generators: Python, Pydantic, Java, Go, TypeScript, Rust | present | [CLAIM-linkml-03] |
| Generators: SQL DDL, SQLAlchemy, BigQuery DDL, TypeQL, TerminusDB, SSSOM, Pandera, Excel, CSV | present | [CLAIM-linkml-03] |
| Docs, ER diagrams, PlantUML | present | [CLAIM-linkml-03] |
| Generator feature dashboard (per-generator metamodel coverage) | present | [CLAIM-linkml-03] |
| Data validation CLI (`linkml-validate`), data loaders/dumpers | present (not described on the page I fetched) | UNVERIFIED |
| Reasoning | absent as engine (OWL generator output goes to external reasoners) | inference |
| Visual editor | absent / not verified | UNVERIFIED |
| Semantic diff / schema migration tool | not verified in this run | UNVERIFIED |

## 4. Architecture diagram
```
 schema.yaml (+ imports, prefixes) --> SchemaView (resolved, induced slots)
     |--> generators: owl / shacl / shex / jsonschema / pydantic / sql / graphql / ... --> artefacts
     |--> validator: schema + data (YAML/JSON/CSV/RDF) --> report
     `--> docs site, diagrams
 Git repo + CI (generate, validate, publish package)
```

## 5. Under-the-hood reconstruction
Data model: the LinkML metamodel is itself a LinkML schema; Python dataclasses generated from it are the schema objects. `SchemaView` resolves imports, inheritance and "induced" slots (slot restricted per class via `slot_usage`). Generators are visitors over resolved schema emitting a target; per-generator coverage varies (hence the dashboard) [CLAIM-linkml-03]. Mapping to constraints: cardinality, ranges, patterns and `rules` map to SHACL/JSON Schema/SQL where the target can express them; hypothesis: complex `rules` and expressions are lossy in some targets. Storage, query, concurrency, security: N/A (build-time toolchain; related `linkml-store` not verified). Versioning is by Git; the schema carries a `version` field (hypothesis). Source entry points at pinned tag not opened in this run: confidence limited.

## 6. Inferred requirements
Deterministic generation (same schema -> same output), import resolution offline, generator parity tests, stable metamodel versioning, Python 3.10+.

## 7. Performance and resource model
Build-time only; no performance data collected or found. Generation cost scales with schema size; typical use on a laptop. Failure mode: generator lossy on unsupported metamodel features; a yanked release (1.11.0) shows release-process risk [CLAIM-linkml-02].

## 8. Strengths
Single source -> many targets; Apache-2.0; broad generator set; frequent releases; data-model-first (not triplestore-first), fits Git/CI. Match: adopt LinkML (or its shape) as the authoring syntax in EOIP gitops; exceed: tie generators to the tenant mutation gate and the epistemic planes.

## 9. Limitations
Verified: generator coverage is uneven (dashboard exists) [CLAIM-linkml-03]; release 1.11.0 yanked [CLAIM-linkml-02]. Hypotheses: lossy OWL/SHACL for complex rules; no built-in governance workflow (review/approve/rollback); no built-in semantic diff/classification of breaking changes; no runtime enforcement. Friction: new DSL to learn; two-way round trip from OWL not guaranteed (not verified).

## 10. Deployment, licensing, viability
Apache-2.0 permissive; pure Python library/CLI; air-gap safe once installed; one-node. No legal-review trigger identified; transitive dependency licences not scanned.

## 11. Competitive delta vs baseline
BL-32: EOIP has `ontology/gitops.py:31` (semantic diff, branches, PRs), `ontology/manifest.py` fixed `VERTEX_LABELS`, `scripts/ontology_diff.py`; ontology authored in Python manifest, not a declarative schema language. BL-28 gate checks labels/required properties; LinkML would add declarative cardinality/range/enum definition and generation of validators. BL-29: LinkML can emit SHACL for pySHACL (see C03-pyshacl). Cross-reference INV-edg-01 in `C03-topbraid-edg.md` (OntologyGitOpsWorkflow branches in a Python dict): LinkML supplies the file format, not the branch store.

## 12. Cards
**STR-linkml-01** | LinkML | one declarative schema generates validators, docs, OWL, SHACL, Pydantic, SQL | [CLAIM-linkml-03] | customers get consistent contracts across API, store and ontology | integrate | accept LinkML YAML as an input format in the CML/mapping layer; compile to EOIP manifest + SHACL; keep EOIP manifest as runtime truth | acceptance: round-trip a 50-class schema with zero loss report items, or listed losses.
**INV-linkml-01** | LinkML 1.12.x | no governance/approval/semantic-diff layer around the schema files | evidence: absence in the docs I read (UNVERIFIED, not exhaustive) | root cause governance (*hypothesis*) | alternative: EOIP gitops adds classified diff (`diff_manifests`), review gate, tenant branches over LinkML files; worse for teams with no Git skills | options: (a) LinkML + CI scripts; (b) persist OntologyGitOpsWorkflow on a real Git repo with LinkML as format; (c) visual editor writing commits | selected (b) | POC: 200 historical schema changes from a public LinkML schema; success = 100% breaking changes flagged, CI <60 s | decision ADOPT (combined with INV-edg-01). Seed hypothesis "TopBraid: ontology-as-code (Turtle/LinkML/YAML)" supported as a direction, not tested.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-08 declarative schema/constraints | INTEGRATE (LinkML input) |
| CAP-37 schema evolution | BUILD on gitops |
| CAP-35 branch/diff/merge | BUILD (real Git) |
| CAP-10 SHACL generation | REUSE generator |
| CAP-09 OWL export | REUSE generator |
| CAP-72 visual editing | DEFER |

## 14. Tests
(PROPOSED.) Generate OWL+SHACL from a fixture schema and validate with pySHACL; compare against hand-written shapes; verify deterministic output (byte-identical on two runs); loss report for unsupported features; pin and SBOM check; confirm Python 3.11 compatibility with the lock.

## 15. Risks and open questions
Metamodel churn between minor versions; generator fidelity; governance of project unverified; dependency weight (many transitive packages); whether EOIP's fixed manifest can express LinkML features (multivalued, inlined, rules).

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, active |
| D2 | 2 | Schema-first modelling |
| D3 | 4 | Toolchain |
| D4 | N/A | No storage |
| D5 | 3,5 | Metamodel and constraints |
| D6 | N/A | Generates SPARQL only |
| D7 | 3 | None; OWL output only |
| D8 | N/A | Build tool |
| D9 | 3 | Data loaders UNVERIFIED |
| D10 | N/A | None |
| D11 | 5,9 | Git only |
| D12 | N/A | None |
| D13 | N/A | None |
| D14 | N/A | None |
| D15 | 9 | No workflow |
| D16 | 3 | Docs/diagrams |
| D17 | 2,3 | Core strength |
| D18 | N/A | None |
| D19 | N/A | None |
| D20 | 7 | No data |
| D21 | 10 | Free |
| D22 | 3,9 | Many targets, lossy risk |
| D23 | N/A | None identified |
| D24 | App. C | PyPI/docs; code not opened |

## Appendix B. Capability mapping
| CAP-ID | Technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-08 | native | 01 | BL-28 | INTEGRATE | P1 |
| CAP-09 | partial (OWL gen) | 03 | BL-30 | REUSE | P2 |
| CAP-10 | partial (SHACL gen) | 03 | BL-29 | REUSE | P1 |
| CAP-37 | partial | 03 | BL-32 | BUILD | P1 |
| CAP-35 | absent | n/a | BL-32 | BUILD | P1 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-linkml-01 | 1.12.1 | Apache-2.0; Python>=3.10; YAML OO modelling language | Officially documented | https://pypi.org/pypi/linkml/json ; https://github.com/linkml/linkml | 2026-10-13 / 2026-10-26 | 0.85 | none |
| CLAIM-linkml-02 | 1.11.0-1.12.1 | 1.11.0 yanked; 1.12.0 2026-10-08; 1.12.1 2026-10-13 | Officially documented | PyPI JSON | 2026-10-13 / 2026-10-26 | 0.85 | none |
| CLAIM-linkml-03 | docs | Generator list incl. OWL, SHACL, ShEx, JSON Schema, Pydantic, SQL DDL, TypeQL, TerminusDB; feature dashboard | Officially documented | https://linkml.io/linkml/generators/index.html | n/a / 2026-10-26 | 0.8 | page gives no per-generator limitations |

## Appendix D. Assumptions
Governance, linkml-validate/store behaviour and loss characteristics were not verified. Access date is the real date. Section 5 is partly hypothesis because source was not opened.
