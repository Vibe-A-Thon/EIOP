| Field | Value |
|---|---|
| Registry ID | T-C03-pyshacl |
| Tier | B (direct REUSE candidate for BL-29; Python SHACL engine) |
| Versions examined | pySHACL 0.40.1 (2026-07-28); 0.40.0 (2026-07-08); 0.31.0 (2026-01-16); repo `master` with an unreleased entry |
| Verified on | 2026-10-26 (actual access date; brief default 2026-10-18) |
| Worker | V13 |

## 1. Identity, current status, tier, and sources
pySHACL is a Python validator and rule engine for W3C SHACL, owned by the RDFLib GitHub organisation (lead Ashley Sommer, support Nicholas Car) [CLAIM-pyshacl-01]. Latest release 0.40.1 on 2026-07-28; the changelog also has an unreleased item [CLAIM-pyshacl-02]. Licence Apache-2.0, requires Python >=3.9, depends on `rdflib>=7.3,<8`, `owlrl>=7.6.2`, `packaging`, `prettytable` [CLAIM-pyshacl-03]. Active, with a release roughly every 2-6 months. Tier B: small, single-purpose library but the one named in BL-29.
Sources: PyPI JSON `https://pypi.org/pypi/pyshacl/json`; repo `https://github.com/RDFLib/pySHACL`; `CHANGELOG.md`; `FEATURES.md`.

## 2. Primary problem, target workloads, example workflows
Validate an RDF data graph against a SHACL shapes graph and emit a W3C `sh:ValidationReport`; optionally run SHACL-AF rules to infer triples. Workloads: CI validation of vocabularies, pre-load validation of RDF batches, data-quality gates. Examples: `pyshacl -s shapes.ttl -e ont.ttl data.ttl`; library call `validate(data, shacl_graph=..., inference='rdfs')`; HTTP service via the `http` extra [CLAIM-pyshacl-04].

## 3. Feature inventory
| Feature | Status | Evidence |
|---|---|---|
| SHACL Core constraints and all property-path types | present (non-validating `sh:order`, `sh:group`, `sh:defaultValue` missing) | [CLAIM-pyshacl-05] |
| SHACL-SPARQL (`sh:sparql`, `sh:select`, `sh:ask`, validators) | present | [CLAIM-pyshacl-05] |
| SHACL-AF rules (`sh:TripleRule`, `sh:SPARQLRule`, condition, order, deactivated) | present; `sh:entailment` and annotation properties missing | [CLAIM-pyshacl-05] |
| SHACL functions, node expressions | present (union/intersection/filterShape "not tested") | [CLAIM-pyshacl-05] |
| SHACL-JS | optional (`pyshacl[js]`) | [CLAIM-pyshacl-05] |
| RDFS/OWL-RL pre-inference | present via `owlrl` | [CLAIM-pyshacl-03] |
| Oxigraph-backed data graph | optional extra (0.40.0) | [CLAIM-pyshacl-06] |
| SPARQL remote graph mode | present, disables inference/rules/JS | [CLAIM-pyshacl-07] |
| CLI, HTTP (OpenAPI) service, focus-node filtering, shape selection | present | [CLAIM-pyshacl-04] |
| Incremental validation | absent / not documented | UNVERIFIED |
| Property-graph (LPG) input | absent; RDF only | inference |

## 4. Architecture diagram
```
 data graph (rdflib Graph | Oxigraph | SPARQL endpoint)   shapes graph (rdflib)   ont graph
          \                                  |                       /
           +--> [optional RDFS / OWL-RL expansion (owlrl)] --> [shape loader: targets, paths]
                        --> [per-shape constraint components (Python classes)] --> SPARQL via rdflib engine
                        --> [SHACL-AF rule engine, optional iterate to fixpoint] --> sh:ValidationReport (Graph + text)
```

## 5. Under-the-hood reconstruction
Data model: rdflib `Graph`/`Dataset`; shapes parsed into `Shape` objects (node and property shapes) from the shapes graph; constraint components map to Python classes keyed by their parameter predicates. Flow (documented behaviour, internals hypothesis beyond that): resolve target nodes (class, node, subjectsOf, objectsOf, custom targets), compute value nodes via the property path, evaluate each component, collect `sh:ValidationResult`s. SPARQL-based constraints run through rdflib's pure-Python SPARQL engine, which is why 0.40.0 added an Oxigraph-backed data graph "for faster SPARQL execution" [CLAIM-pyshacl-06]. Rules: SHACL-AF rules run in `order`, adding triples to the data graph (in place or on a copy). No persistence, concurrency control, caching or security layer: it is a stateless library; SPARQL constraints are code-injection-prone if shapes are untrusted (SHACL-JS especially). Entry points: `pyshacl/validate.py`, `pyshacl/constraints/`, `pyshacl/rules/` (paths from repository layout; not opened at a pinned tag in this run: confidence reduced).

## 6. Inferred requirements
FR: parse Turtle/JSON-LD shapes, produce standard reports, support SHACL-SPARQL and rules. NFR: pure-Python install, Python >=3.9, single process, no network.

## 7. Performance and resource model
No numbers verified. The repo ships a benchmark script comparing four inferencing options but publishes no results [CLAIM-pyshacl-06]. Cost model hypothesis: validation is linear in (shapes x focus nodes x path fan-out) plus SPARQL constraint cost; memory is the whole rdflib graph in RAM (rdflib's in-memory store is a Python dict index; large graphs are costly). Failure modes: slow SPARQL constraints, deep recursion in shape cycles (spec leaves recursion undefined), memory on >millions of triples. EOIP must benchmark on its own graph sizes (proposed BM).

## 8. Strengths
Apache-2.0 and permissive; near-complete SHACL Core + SPARQL + AF coverage; known-failure list is explicit (two W3C-suite failures) [CLAIM-pyshacl-08]; standard reports; small dependency set; active. Match/exceed: use as conformance oracle for the in-house subset (the existing differential test already assumes that).

## 9. Limitations
Verified: RDF-only; rdflib speed; two W3C-suite failures; `sh:entailment` missing [CLAIM-pyshacl-05][CLAIM-pyshacl-08]; 0.40.0 dropped `rdflib.ConjunctiveGraph` (breaking) [CLAIM-pyshacl-09]. Algorithmic: no incremental validation (full re-validate). Operational: whole graph in RAM. Friction: results are RDF graphs, need mapping to EOIP issue model; no tenant/ACL notion. No overall W3C pass rate is published: absence of claim, not proof of failure.

## 10. Deployment, licensing, viability
Apache-2.0: redistribution-safe; transitive `rdflib` (BSD-3) and `owlrl` (W3C licence per project; UNVERIFIED here). Air-gapped: yes (pure Python, no network unless SPARQL remote mode). One-node: yes. Legal-review trigger: none for pyshacl itself; confirm owlrl licence in SBOM.

## 11. Competitive delta vs baseline
BL-29: in-house subset over `MemoryGraphStore` plus optional adapter at `ontology/shacl_validator.py:788` that imports `rdflib` and `pyshacl`; library absent from `requirements.lock`; test `test_pyshacl_adapter_and_differential_oracle` failed with `ModuleNotFoundError` (baseline §2.1). Note: recent commits mention embedded rdflib for SPARQL (git log 099eb38); lock status after those commits not re-checked (U-07). pySHACL gives conformance for the full SHACL spec, which the subset lacks. BL-28 gate is label/required-property only. BL-32 has no CI SHACL suite.

## 12. Cards
**STR-pyshacl-01** | pySHACL | broad, permissively-licensed SHACL Core/SPARQL/AF engine | [CLAIM-pyshacl-05] | standards-conformant validation and rules for customers who import vocabularies | integrate | install as optional extra `eoip[shacl]`; keep in-house subset as fast path for LPG-shaped checks; pySHACL as oracle and as engine for imported shapes | acceptance: differential suite green on W3C SHACL data-shapes tests, divergences listed.
**INV-pyshacl-01** | pySHACL 0.40.1, large RDF graphs | in-RAM rdflib, full re-validation | [CLAIM-pyshacl-06] | root cause: storage/algorithm (*hypothesis*, benchmark script has no published numbers) | alternative: validate only the delta subgraph at mutation gate (changed focus nodes + shape-dependent neighbourhood), engine unchanged; worse when shapes use cross-graph SPARQL | options: (a) Oxigraph extra; (b) delta-scoped validation in `OntologyGitOps` CI and mutation gate; (c) push SHACL-to-SPARQL into the triplestore (Fuseki/GraphDB, BL-06) | selected (b) | POC: 1M-triple synthetic graph, 1% delta; success = delta validation <10% of full time with identical results; baseline = full pyshacl run | risks: shape dependency analysis wrong -> missed violations (fail-open must be forbidden: fall back to full) | defensibility: tenant-aware delta gate | decision EXPERIMENT. Seed hypothesis "TopBraid: CI SHACL tests" supported: pySHACL is the CI engine.

## 13. Per-capability decisions
| Capability | Decision |
|---|---|
| CAP-10 SHACL validation (full spec, oracle) | REUSE (pySHACL, optional extra) |
| CAP-10 LPG-native constraint enforcement in mutation gate | BUILD (keep subset) |
| CAP-22 SHACL-AF rules | EXPERIMENT |
| CAP-37 CI gating of ontology changes | INTEGRATE into gitops CI |

## 14. Tests and acceptance
(PROPOSED, none run.) T1 add `pyshacl` to an extras lock; the failing differential test must pass. T2 run W3C data-shapes core+sparql manifests through the adapter; record pass rate and the two documented failures. T3 benchmark 10k/100k/1M triples. T4 untrusted shapes: reject `sh:js` and bound SPARQL timeouts (adapter already has `timeout_seconds`). T5 SBOM and licence scan.

## 15. Risks and open questions
rdflib major-version pinning (`<8`); ConjunctiveGraph removal breaks older code; owlrl licence; SPARQL-constraint injection; mapping LPG to RDF without semantic loss; actual throughput unknown.

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Apache-2.0, active, RDFLib org |
| D2 | 2 | Validation and rules |
| D3 | 4 | Library pipeline |
| D4 | 5 | N/A: uses rdflib stores |
| D5 | 3,5 | SHACL Core/SPARQL/AF |
| D6 | 5 | SPARQL via rdflib/Oxigraph |
| D7 | 3,5 | RDFS/OWL-RL pre-inference, AF rules |
| D8 | N/A | Stateless library |
| D9 | N/A | No ingestion |
| D10 | N/A | No provenance beyond report |
| D11 | N/A | No versioning |
| D12 | N/A | Not applicable |
| D13 | N/A | Not applicable |
| D14 | N/A | Not applicable |
| D15 | 8,13 | Shapes as governance artefacts |
| D16 | 3 | CLI only |
| D17 | 2,14 | CLI, HTTP, library |
| D18 | 5,15 | SHACL-JS/SPARQL injection |
| D19 | N/A | No tenancy |
| D20 | 7 | No verified numbers |
| D21 | 10 | Free |
| D22 | 9 | RDF only; LPG bridge loss |
| D23 | N/A | None identified |
| D24 | App. C | Official docs, changelog; code not opened |

## Appendix B. Capability mapping
| CAP-ID | This technology | CLAIM | EOIP baseline | Decision | Priority |
|---|---|---|---|---|---|
| CAP-10 | native | 05 | BL-29 Partial | REUSE | P1 |
| CAP-22 | partial (AF rules) | 05 | BL-30 Partial | EXPERIMENT | P2 |
| CAP-37 | plugin (CI) | 05 | BL-32 Partial | INTEGRATE | P1 |
| CAP-08 | partial | 05 | BL-28 Implemented | BUILD (keep) | P1 |

## Appendix C. Evidence records
| CLAIM-ID | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| CLAIM-pyshacl-01 | pySHACL repo | Owned by RDFLib org; leads A. Sommer, N. Car | Officially documented | GitHub README https://github.com/RDFLib/pySHACL | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-pyshacl-02 | 0.40.1 / 2026-07-28 | Latest release 0.40.1; unreleased Oxigraph fix | Officially documented | CHANGELOG https://github.com/RDFLib/pySHACL/blob/master/CHANGELOG.md | 2026-07-28 / 2026-10-26 | 0.8 | README CLI text said 0.27.0 (stale) |
| CLAIM-pyshacl-03 | 0.40.1 | Apache-2.0; Python>=3.9; deps rdflib>=7.3,<8, owlrl>=7.6.2 | Officially documented | PyPI JSON https://pypi.org/pypi/pyshacl/json | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-pyshacl-04 | 0.40.1 | CLI, HTTP service extra, focus-node filtering, shape selection | Officially documented | README | 2026-10-26 | 0.75 | none |
| CLAIM-pyshacl-05 | master | Core complete bar non-validating props; SPARQL complete; AF rules mostly complete; JS optional | Officially documented | FEATURES.md https://github.com/RDFLib/pySHACL/blob/master/FEATURES.md | 2026-10-26 | 0.75 | self-reported |
| CLAIM-pyshacl-06 | 0.40.0 | Oxigraph-backed graph for faster SPARQL; benchmark script without numbers | Officially documented | CHANGELOG, README | 2026-07-08 / 2026-10-26 | 0.7 | no independent benchmark found |
| CLAIM-pyshacl-07 | master | Remote graph mode disables inference, rules, JS | Officially documented | README | 2026-10-26 | 0.75 | none |
| CLAIM-pyshacl-08 | master | Two known W3C-suite failures (ill-formed datatype, `$shapesGraph` pre-binding); no pass rate | Officially documented | FEATURES.md | 2026-10-26 | 0.7 | other failures may be undocumented |
| CLAIM-pyshacl-09 | 0.40.0 | Dropped `rdflib.ConjunctiveGraph` support | Officially documented | CHANGELOG | 2026-07-08 | 0.75 | none |

## Appendix D. Assumptions
Access date recorded as the real date (2026-10-26). Source code not opened at a tag; section 5 internals are partly hypothesis. owlrl licence not verified. Whether EOIP's lock now includes rdflib/pyshacl after recent commits was not re-checked.
