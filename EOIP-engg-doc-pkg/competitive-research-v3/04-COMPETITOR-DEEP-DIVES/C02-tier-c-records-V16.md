# C02 — Tier C Records (batch V16)

| Field | Value |
|---|---|
| Category | C02 — RDF stores, semantic database engines and inference engines |
| Batch | V16 |
| Access date | 2026-10-26 |
| Note | This file was accidentally deleted during the coordinator's final cleanup pass and has been regenerated from the surviving machine-readable registry fragment `_work/registry-fragments/V16.json` (which was not affected). No new research was performed; every field below is a direct, unaltered reformat of that fragment's data. No CLAIM-ID evidence records survived the deletion, so none are fabricated here — confidence scores and source lists below are carried over from the fragment as-is. |

### T-C02-blazegraph — Blazegraph

| Field | Value |
|---|---|
| Official URL | https://github.com/blazegraph/database |
| Owner | Blazegraph project (archived) |
| Latest version | UNVERIFIED (README cites 2.0.0 on Maven Central) |
| Status | **archived** |
| Licence | GPL-2.0 (strong-copyleft) |
| Deployment modes | self-hosted, embedded |
| Air-gap viable | yes |
| Maturity | historical |

**Relevance note:** repository archived 2026-03-23. The Wikidata Query Service backend (long associated with Blazegraph) is being replaced by QLever (see `C02-qlever.md`), with Wikimedia's own pages disagreeing on exactly when Blazegraph maintenance ceased (2016 vs 2018). Touches CAP-02, CAP-15.

**Decision:** REJECT as a backend (archived, GPL-2.0); REFERENCE-ONLY for migration lessons (what a Blazegraph→QLever-style engine swap requires).

**Legal-review trigger:** yes — GPL-2.0 and project abandonment.

**Sources:** Blazegraph repo (https://github.com/blazegraph/database, accessed 2026-10-26); WDQS backend replacement page (https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/WDQS_backend_update/Backend_Replacement, accessed 2026-10-26). Verification confidence: 0.8.

---

### T-C02-millenniumdb — MillenniumDB

| Field | Value |
|---|---|
| Official URL | https://github.com/MillenniumDB/MillenniumDB |
| Owner | Academic group (not re-verified) |
| Latest version | UNVERIFIED |
| Status | unknown |
| Licence | GPL-2.0 (strong-copyleft) |
| Deployment modes | self-hosted |
| Air-gap viable | yes |
| Maturity | research |

**Relevance note:** a research-grade graph database; no current release or maintenance cadence was reconfirmed. Touches CAP-01, CAP-02.

**Decision:** REFERENCE-ONLY.

**Legal-review trigger:** yes — GPL-2.0.

**Sources:** MillenniumDB repo (https://github.com/MillenniumDB/MillenniumDB, accessed 2026-10-26). Verification confidence: 0.55.

---

### T-C02-corese — Corese

| Field | Value |
|---|---|
| Official URL | https://github.com/Corese-stack |
| Owner | Inria Wimmics team and contributors |
| Latest version | corese-core 4.6.5 (unconfirmed snippet); 4.5.0 confirmed at 2023-12-14 |
| Status | active |
| Licence | CeCILL-C (weak-copyleft, LGPL-like) |
| Deployment modes | embedded, self-hosted, desktop |
| Air-gap viable | yes |
| Maturity | early-production |

**Relevance note:** a French semantic-web engine (SPARQL, SHACL, rule-based reasoning) with components corese-core, corese-command, corese-server, corese-gui, corese-python. The original Wimmics/corese repository was archived in January 2025; development continues under the Corese-stack organisation. Touches CAP-02, CAP-10, CAP-15, CAP-22.

**Decision:** REFERENCE-ONLY; EXPERIMENT as an optional SHACL conformance oracle alongside pySHACL.

**Legal-review trigger:** yes — CeCILL-C copyleft before any bundling.

**Sources:** Corese-stack org (https://github.com/Corese-stack, accessed 2026-10-26); corese-core (https://github.com/Corese-stack/corese-core, accessed 2026-10-26). Verification confidence: 0.6.

---

### T-C02-hdt — HDT (compressed RDF)

| Field | Value |
|---|---|
| Official URL | https://github.com/rdfhdt/hdt-cpp |
| Owner | rdfhdt community |
| Latest version | hdt-java 3.0.7 (2022-12-12); hdt-cpp version UNVERIFIED |
| Status | maintenance |
| Licence | LGPL (hdt-cpp, hdt-java core, hdt-jena); Apache-2.0 (hdt-java api/cli) — mixed |
| Deployment modes | embedded, self-hosted |
| Air-gap viable | yes |
| Maturity | early-production |

**Relevance note:** a compressed binary RDF serialisation and index format (header-dictionary-triples). rdfhdt.org's TLS certificate had expired at fetch time, so some claims rest on the GitHub repos only. Touches CAP-02, CAP-15.

**Decision:** EXPERIMENT as an optional compact snapshot/export format for RDF data.

**Legal-review trigger:** yes — mixed LGPL/Apache-2.0 modules; LGPL linking terms need review before static linking.

**Sources:** hdt-cpp (https://github.com/rdfhdt/hdt-cpp, accessed 2026-10-26); hdt-java (https://github.com/rdfhdt/hdt-java, accessed 2026-10-26); hdt-java 3.0.7 on Zenodo (https://zenodo.org/records/7428791, accessed 2026-10-26). Verification confidence: 0.55.

---

### T-C02-comunica — Comunica

| Field | Value |
|---|---|
| Official URL | https://comunica.dev/ |
| Owner | Comunica Association / community (not re-verified) |
| Latest version | 5.4 (2026-09-14) |
| Status | active |
| Licence | MIT (permissive) |
| Deployment modes | embedded, self-hosted |
| Air-gap viable | yes |
| Maturity | production |

**Relevance note:** a modular federated SPARQL query engine (`@comunica/query-sparql`, `@comunica/query-sparql-rdfjs`), releasing roughly 2–3 times a year (5.0 in January, 5.2 in April, 5.4 in September 2026). Touches CAP-15, CAP-21 (federation).

**Decision:** REFERENCE-ONLY; EXPERIMENT for federation/virtualisation tests alongside Ontop.

**Legal-review trigger:** no — permissive MIT.

**Sources:** Comunica blog (https://comunica.dev/blog/, accessed 2026-10-26). Verification confidence: 0.8.

---

### T-C02-nemo — Nemo (Datalog reasoner)

| Field | Value |
|---|---|
| Official URL | https://github.com/knowsys/nemo |
| Owner | Knowledge-Based Systems Group, TU Dresden |
| Latest version | 0.10.1 (date UNVERIFIED; GitHub shows "01 Aug", year inferred 2026) |
| Status | active |
| Licence | Apache-2.0 OR MIT (permissive, dual) |
| Deployment modes | embedded, self-hosted |
| Air-gap viable | yes |
| Maturity | early-production |

**Relevance note:** a Rust Datalog reasoner (CLI `nmo`, `nemo-web`, language bindings), releasing several times a year. This is the key REUSE/EXPERIMENT candidate for EOIP's incremental rule-materialisation gap (GAP-22), as a permissively licensed alternative to RDFox. Touches CAP-22.

**Decision:** EXPERIMENT as a Tier-1 Datalog worker for incremental rule materialisation.

**Legal-review trigger:** no — permissive dual licence.

**Sources:** Nemo repo (https://github.com/knowsys/nemo, accessed 2026-10-26); Nemo releases (https://github.com/knowsys/nemo/releases, accessed 2026-10-26). Verification confidence: 0.75.

---

### T-C02-vlog — VLog

| Field | Value |
|---|---|
| Official URL | https://github.com/karmaresearch/vlog |
| Owner | karmaresearch GitHub org; TU Dresden / VU Amsterdam |
| Latest version | 1.3.7 (per a 2023 review) |
| Status | maintenance |
| Licence | Apache-2.0 (permissive) |
| Deployment modes | self-hosted, Docker |
| Air-gap viable | yes |
| Maturity | research |

**Relevance note:** a Datalog/rule reasoner (C++ core with a Java API). TU Dresden's own project page names Nemo as VLog's successor. Touches CAP-22.

**Decision:** REFERENCE-ONLY; prefer Nemo for new work.

**Legal-review trigger:** no — permissive Apache-2.0.

**Sources:** VLog repo (https://github.com/karmaresearch/vlog, accessed 2026-10-26); VLog page, TU Dresden (https://iccl.inf.tu-dresden.de/web/VLog, accessed 2026-10-26). Verification confidence: 0.5.

---

### T-C02-souffle — Souffle

| Field | Value |
|---|---|
| Official URL | https://github.com/souffle-lang/souffle |
| Owner | Souffle community (originated at Oracle Labs) |
| Latest version | 2.5 (date UNVERIFIED; GitHub shows "24 Mar", year not shown) |
| Status | active |
| Licence | UPL-1.0 per distribution packages (LICENSE file itself not opened — verify before relying on this) |
| Deployment modes | self-hosted |
| Air-gap viable | yes |
| Maturity | production |

**Relevance note:** a Datalog compiler (not an interpreter) originally from Oracle Labs; the `oracle/souffle` repository is deprecated in favour of the active `souffle-lang/souffle` org. Releases about 1–2 times a year. Relevant as a reference for compiling rules to native code rather than interpreting them. Touches CAP-22.

**Decision:** REFERENCE-ONLY.

**Legal-review trigger:** no (tentatively) — permissive per distribution packages, but the LICENSE file itself was not opened in the original research; confirm before any dependency decision.

**Sources:** Souffle releases (https://github.com/souffle-lang/souffle/releases, accessed 2026-10-26). Verification confidence: 0.6.

---

## Evidence records

| CLAIM-ID | Product/version/date | Claim | Class | Source | Pub/access | Conf | Contradictory |
|---|---|---|---|---|---|---|---|
| CLAIM-blazegraph-01 | Blazegraph database | GitHub repository archived 2026-03-23; status archived, no further releases | Observed in source code | blazegraph/database repo | 2026-03-23 / 2026-10-26 | 0.8 | none |
| CLAIM-blazegraph-02 | Blazegraph / Wikidata Query Service | WDQS backend being replaced by QLever (2026–27); Wikimedia's own pages disagree on when Blazegraph maintenance ceased (2016 vs 2018) | Officially documented | Wikidata WDQS backend-replacement page | unverified date / 2026-10-26 | 0.7 | two Wikimedia pages disagree on the maintenance-cessation date |
| CLAIM-millenniumdb-01 | MillenniumDB | Research-grade graph database; no current release/maintenance cadence confirmed | Unverified | MillenniumDB/MillenniumDB repo | unverified / 2026-10-26 | 0.55 | none |
| CLAIM-corese-01 | Corese-stack (corese-core 4.6.5 unconfirmed; 4.5.0 confirmed) | Original Wimmics/corese repo archived January 2025; development continues under the Corese-stack org; CeCILL-C licence | Observed in source code | Corese-stack org + corese-core repo | 2025-01 / 2026-10-26 | 0.6 | latest version snippet (4.6.5) unconfirmed against a dated release |
| CLAIM-hdt-01 | hdt-java 3.0.7 / hdt-cpp (version unverified) | Mixed licensing: LGPL for hdt-cpp, hdt-java core and hdt-jena; Apache-2.0 for hdt-java api/cli | Observed in source code | rdfhdt/hdt-cpp, rdfhdt/hdt-java repos; Zenodo record | 2022-12-12 / 2026-10-26 | 0.55 | rdfhdt.org's own site was unreachable (expired TLS certificate) at fetch time |
| CLAIM-comunica-01 | Comunica 5.4 | MIT-licensed, releasing roughly 2–3 times a year (5.0 Jan, 5.2 Apr, 5.4 Sep 2026) | Officially documented | Comunica blog | 2026-09-14 / 2026-10-26 | 0.8 | none |
| CLAIM-nemo-01 | Nemo 0.10.1 | Apache-2.0 OR MIT dual-licensed Rust Datalog reasoner; several releases per year | Officially documented | knowsys/nemo repo and releases page | year inferred 2026 / 2026-10-26 | 0.75 | exact release date not shown on GitHub (day/month only) |
| CLAIM-vlog-01 | VLog 1.3.7 | Apache-2.0 C++/Java Datalog reasoner; TU Dresden's own project page names Nemo as its successor | Officially documented | karmaresearch/vlog repo; TU Dresden VLog page | 2022-12 / 2026-10-26 | 0.5 | none |
| CLAIM-souffle-01 | Souffle 2.5 | Datalog compiler (not interpreter); `oracle/souffle` deprecated in favour of `souffle-lang/souffle`; UPL-1.0 per distribution packages | Officially documented | souffle-lang/souffle releases page | year not shown / 2026-10-26 | 0.6 | the LICENSE file itself was not opened to confirm UPL-1.0 directly |
