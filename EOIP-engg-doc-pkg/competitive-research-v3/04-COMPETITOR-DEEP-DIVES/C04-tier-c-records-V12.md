# C04 — Tier C records (batch V12)

Verified 2026-10-18. Worker V12. Members: SPARQL-Generate, Karma, py_entitymatching (Magellan), recordlinkage.

### T-C04-sparql-generate — SPARQL-Generate

| Field | Value |
|---|---|
| Official URL | https://github.com/sparql-generate/sparql-generate |
| Owner | MINES Saint-Étienne (copyright 2020) |
| Latest version + date | v2.1.1, 2025-09-29 (next snapshot 2.1.2 started same day) |
| Status | active, low cadence |
| Licence + class | Apache-2.0, permissive |
| Deployment | Java CLI/library, Docker |
| Air-gap viable | yes (file inputs; remote iterators optional) |
| Tier reason | alternative mapping language to RML; template-based RDF generation from heterogeneous sources |

SPARQL-Generate extends SPARQL with GENERATE/ITERATOR/SOURCE clauses so a single SPARQL-like query turns JSON, CSV, XML and other documents into RDF or text. It is an alternative to RML for declarative mapping and shows that mapping can be expressed in an existing query language. For EOIP it is a design reference for BL-33 (CML/IR); no import path is warranted since RML/R2RML has wider tooling (see `C04-rml-tools.md`). Touches CAP-29, CAP-26.
**Decision:** REFERENCE-ONLY. Do not build an importer unless a customer brings SPARQL-Generate mappings.

| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-spg-01 | v2.1.1 | Apache-2.0, copyright 2020 MINES Saint-Étienne; release 2025-09-29 | Officially documented | https://github.com/sparql-generate/sparql-generate | 2026-10-18 | 0.85 | none |
| CLAIM-spg-02 | v2.1.1 | language adds GENERATE/ITERATOR/SOURCE to SPARQL | Reasoned inference (project knowledge; README not opened) | same | 2026-10-18 | 0.5 | none |

### T-C04-karma — Karma (Web-Karma, USC ISI)

| Field | Value |
|---|---|
| Official URL | https://github.com/usc-isi-i2/Web-Karma |
| Owner | USC Information Sciences Institute |
| Latest version + date | Karma Release 2.5.8, 2024-01-25; latest commit seen 2025-04-16 (README edit) |
| Status | **maintenance / low activity** (development activity beyond README edits NOT PUBLICLY VERIFIED) |
| Licence + class | Apache-2.0, permissive |
| Deployment | Java web app, local server |
| Air-gap viable | yes (source files); some features use web APIs |
| Tier reason | semi-automatic source-to-ontology modelling with a learning component |

Karma lets a user map databases, spreadsheets, delimited text, XML, JSON, KML and Web APIs to ontologies; it proposes semantic-type and relationship assignments and the user refines them, outputting R2RML and RDF (ISI/other project descriptions). It is the closest published precedent for EOIP journey J12 (propose, review, promote) with a ranking of candidate semantic models. Its learning approach is not independently reproduced here. Touches CAP-28, CAP-29, CAP-71.
**Decision:** REFERENCE-ONLY. Take the interaction pattern (ranked candidate models, user correction feeds learning) into the J12 review UX; do not depend on the code.

| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-karma-01 | Release 2.5.8 | Apache-2.0; release 2024-01-25; last commit 2025-04-16 | Officially documented | https://github.com/usc-isi-i2/Web-Karma (LICENSE.txt, releases.atom, commits.atom) | 2026-10-18 | 0.9 | none |
| CLAIM-karma-02 | n/a | integrates databases, spreadsheets, text, XML, JSON, KML, Web APIs; proposes ontology mappings user can refine | Third-party report (search results) | https://www.isi.edu/centers-ckg/resources/downloads/ | 2026-10-18 | 0.6 | no current activity evidence |

### T-C04-magellan — py_entitymatching (Magellan)

| Field | Value |
|---|---|
| Official URL | https://github.com/anhaidgroup/py_entitymatching |
| Owner | AnHai Doan group (University of Wisconsin-Madison) |
| Latest version + date | v0.4.2, 2024-02-07; last commit 2024-02-07 |
| Status | **dormant** (no activity after 2024-02) |
| Licence + class | BSD (PyPI metadata; exact variant UNVERIFIED), permissive |
| Deployment | Python library |
| Air-gap viable | yes |
| Tier reason | EM research toolkit; source of ER-Magellan benchmark family |

Magellan is an end-to-end entity-matching "how-to" toolkit: blocking, feature generation, labelling, ML matcher selection and debugging, built on pandas/scikit-learn. Its main current value is the benchmark datasets reused by Ditto and LLM matching papers (`C04-ditto.md`, `C04-llm-entity-matching.md`), which EOIP should use in the validation plan. Touches CAP-31, CAP-78.
**Decision:** REFERENCE-ONLY (datasets: REUSE). Not a matcher candidate: Splink or Zingg cover BL-36.

| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-mag-01 | 0.4.2 | release and last commit 2024-02-07; PyPI licence BSD | Officially documented | https://github.com/anhaidgroup/py_entitymatching ; https://pypi.org/project/py-entitymatching/ | 2026-10-18 | 0.9 | none |
| CLAIM-mag-02 | n/a | workflow stages blocking/features/labelling/matchers | Reasoned inference (prior knowledge) | n/a | 2026-10-18 | 0.5 | none |

### T-C04-recordlinkage — recordlinkage (Python Record Linkage Toolkit)

| Field | Value |
|---|---|
| Official URL | https://github.com/J535D165/recordlinkage |
| Owner | Jonathan de Bruin (J535D165) and contributors |
| Latest version + date | v0.16, 2023-07-20; last commit 2023-07-20 |
| Status | **dormant** (3+ years on release page; no later commits seen) |
| Licence + class | BSD-3-Clause (PyPI), permissive |
| Deployment | Python library |
| Air-gap viable | yes |
| Tier reason | small linkage library: indexing (blocking), comparison, classifiers (including unsupervised ECM and Naive Bayes) |

recordlinkage is a pandas-based toolkit for indexing, comparison and classification of record pairs. It is a lightweight, readable teaching implementation but dormant and pandas-bound, so it does not scale like Splink (see `C04-splink.md`). Relevance: reference for API design of a comparison-vector layer. Touches CAP-31.
**Decision:** REFERENCE-ONLY.

| CLAIM | product/version/date | claim | class | source | dates | conf | contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-rl-01 | v0.16 | release 2023-07-20; last commit 2023-07-20; BSD-3-Clause | Officially documented | https://github.com/J535D165/recordlinkage ; https://pypi.org/project/recordlinkage/ | 2026-10-18 | 0.9 | none |
| CLAIM-rl-02 | n/a | indexing, comparison, classification workflow; unsupervised classifiers | Reasoned inference (prior knowledge) | n/a | 2026-10-18 | 0.5 | none |
