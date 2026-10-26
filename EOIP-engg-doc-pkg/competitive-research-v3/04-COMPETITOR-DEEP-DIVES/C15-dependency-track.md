# C15 - Dependency-Track, SBOM graphs, deps.dev, OSV

| Field | Value |
|---|---|
| Registry ID | T-C15-dependency-track |
| Tier | B - dependency-risk graph; direct comparison with EOIP `compliance/sbom.py` and `connectors/sbom.py` |
| Versions examined | Dependency-Track 5.2.1 and 4.14.6 (both 2026-10-25), 5.2.0 (2026-10-08), v5 GA announced 2026-06-09; OSV schema 1.9.2 (2026-10-13); deps.dev API v3 |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V29 |

## 1. Identity, status, tier, sources

| Item | Finding | Claim |
|---|---|---|
| Dependency-Track (DT) | OWASP project, "intelligent Component Analysis platform"; ~4.3k stars, Apache-2.0, pushed 2026-10-25; v4 and v5 lines both released | [CLAIM-dt-01] |
| v5 ("Hyades") | GA 2026-06-09: stateless API instances coordinating via PostgreSQL only, no message broker; embedded durable execution engine; PostgreSQL the only database (H2/MySQL/MSSQL dropped); no in-place upgrade from v4; v4.14.x security fixes for ~6 months | [CLAIM-dt-02] |
| deps.dev | Google service: package/version metadata, resolved dependency graphs, advisories, project scorecards; ecosystems GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET; generated data CC-BY 4.0; API under Google API Terms | [CLAIM-dt-04] |
| OSV | open vulnerability schema (v1.9.2) and aggregator osv.dev; per-source data licences (e.g. GHSA CC-BY 4.0, Rust CC0, Chainguard CC-BY-NC-ND 4.0); full dump `gs://osv-vulnerabilities/all.zip` | [CLAIM-dt-05][CLAIM-dt-06] |
| SBOM formats | CycloneDX and SPDX are the SBOM standards; DT docs v4: consumes/produces CycloneDX SBOM and VEX; SPDX only for licence IDs | [CLAIM-dt-03] |
| Name collision | none; Hyades = v5 codename | |

## 2. Problem and workloads

Portfolio-wide component inventory, continuous vulnerability and licence/operational policy evaluation, VEX, notifications, CI upload of SBOMs via REST. EU CRA SBOM obligations cited by project [CLAIM-dt-02]. Workflows: CI uploads CycloneDX BOM -> DT matches components (purl/CPE) against NVD/GHSA/OSV/OSS Index/Snyk/Trivy/VulnDB -> policy -> Slack/Teams/webhook/Jira alert [CLAIM-dt-03].

## 3. Feature inventory

| Feature | Status |
|---|---|
| CycloneDX SBOM + VEX in/out, REST/OpenAPI, CI plugins | present |
| SPDX SBOM ingest | absent in v4 docs (UNVERIFIED for v5) |
| Vulnerability sources: NVD, GitHub Advisories, OSV, OSS Index, Snyk, Trivy; EPSS | present (VulnDB commercial) |
| Policies: security, licence, operational; v5 CEL expression policies | present |
| v5 supply-chain integrity check (published-hash mismatch) | present |
| Notifications, Prometheus, secrets provider, portfolio ACL (v5), OIDC/LDAP | present |
| Graph query language; code reachability | absent |

## 4. Architecture

```
CI -> REST (BOM/VEX upload) -> API instances (stateless, v5)
   -> PostgreSQL (state, search, cache, metrics, durable-execution queue)
   -> mirrors: NVD, GHSA, OSV, OSS Index, Snyk, Trivy -> matching -> policy (CEL) -> notifications
deps.dev / OSV.dev: external reference graphs queried by API or dump
```

## 5. Under-the-hood reconstruction

DT data model: Project (versioned) -> Components (purl, hashes, licences, optional parent/dependency graph from BOM) -> Findings (component x vulnerability, analysis state, suppression); policies evaluate conditions per component/vulnerability. Matching uses purl and CPE with internal analyzers; known fixes mention CPE wildcards, PyPI name normalisation, NuGet case-insensitivity (5.1.2) [CLAIM-dt-01]. v5 stores search/cache/metrics in PostgreSQL, drops Lucene fuzzy matching, uses Protobuf notifications and a durable workflow ("dex") with retries, 20k SBOM/hour claimed by early adopters (vendor) [CLAIM-dt-02]. OSV model: `id`, `aliases`, `affected[package{ecosystem,name,purl}, ranges{SEMVER|ECOSYSTEM|GIT: introduced/fixed/last_affected/limit}, versions]`, `severity[CVSS_V2/V3/V4]`, `references`; `fixed` preferred to `last_affected` [CLAIM-dt-05]. deps.dev: GetPackage/GetVersion/GetRequirements/GetDependencies (resolved graph; npm, Cargo, Maven, PyPI)/GetProject/GetAdvisory/Query by hash [CLAIM-dt-04]. Security: API keys, OIDC; v5 service accounts, workload identity federation, HMAC-signed webhooks (5.2.0) [CLAIM-dt-01].

## 6. Inferred requirements

purl join key; offline vuln mirror; audited per-component analysis state; idempotent batch ingest.

## 7. Performance and resource model

Vendor claims only: >20,000 SBOMs/hour, >250,000 SBOMs per instance; hardware and SBOM size unstated [CLAIM-dt-02]. Failure modes: stale mirrors, name-normalisation false negatives.

## 8. Strengths

STR-dt-01 purl-keyed component x vulnerability finding model with analysis state/suppression. STR-dt-02 locally mirrored feeds. STR-dt-03 CEL policies. STR-osv-01 OSV range semantics incl. GIT ranges that bind vulnerabilities to commits (links to code graph). STR-depsdev-01 resolved transitive graph as service.

## 9. Limitations

| Class | Finding |
|---|---|
| Algorithmic | match quality depends on purl/CPE; `last_affected` ranges yield false negatives (OSV note) |
| Operational | v5 requires PostgreSQL and a no-in-place migration; v4 single server |
| Friction | CycloneDX-centric; SPDX not ingested natively (v4 docs) |
| Licensing | Apache-2.0 DT; OSV data per-source licences incl. NC-ND (Chainguard) - legal review; deps.dev under Google API ToS, online only |

## 10. Deployment, licensing, viability

DT: Docker/Kubernetes/WAR, self-hosted, Apache-2.0, redistribution-safe; air-gap viable with internal mirror of feeds (mirroring docs not read - UNVERIFIED). OSV: offline via `all.zip` dump; scanner offline mode UNVERIFIED. deps.dev: cloud API/BigQuery - optional online enrichment only, not air-gap.

## 11. Delta vs EOIP baseline (code read this run)

| Area | DT / OSV / deps.dev | EOIP |
|---|---|---|
| SBOM generation | not its role | `compliance/sbom.py`: `SbomManager.generate_cyclonedx_sbom` CycloneDX 1.5 incl. models/datasets, licence-policy `verify_compliance`, copyleft isolation, notice bundle, SHA-256 provenance (268 lines); library-only per 01a headline 1 |
| SBOM ingestion | CycloneDX BOM/VEX with dependency graph | `connectors/sbom.py` `SBOMConnector`: SPDX `packages` and CycloneDX `components` + `vulnerabilities` to `SourceEventV2` (one event per component; deterministic event ids); **does not read** SPDX `relationships` or CycloneDX `dependencies`, so no component-to-component edges; no VEX; no hashes dedup across projects |
| Vulnerability matching | NVD/GHSA/OSV/OSS Index/Snyk/Trivy | none: no OSV/deps.dev/DT reference in `packages/eoip` (grep) |
| Policy | licence + vuln + operational CEL | licence-policy YAML only |
| Code link | none | BL-42 symbols; no component-to-symbol import edges tied to purl |
| Permissions | portfolio ACL (v5) | BL-18 Partial; connector emits events, BL-23 respected |

## 12. Cards

| ID | Card |
|---|---|
| STR-dt-01 | [CLAIM-dt-01,03] finding = component x vuln with analysis state; **integrate**: DT as optional source system (REST export of findings/projects) through a new connector; test: fixture BOM with known CVE yields `Finding` node with evidence (BOM serial, feed id, retrieval date) |
| STR-osv-01 | [CLAIM-dt-05] GIT ranges; **match**: map `introduced/fixed` commits to code-graph revisions so "which functions touched since the vulnerable commit"; test: GHSA with git range resolves affected symbol set on fixture repo |
| INV-dt-01 | Target EOIP SBOM connector (own) vs DT. Limitation: EOIP ingests components but no dependency edges or vulnerability matching [code 2026-10-26]; cause coupling/maturity (proven by file read). Options: (a) integrate DT findings via connector; (b) native OSV-dump matcher on purl; (c) joint graph: Service -> Component (with transitive edges) -> Vulnerability -> Symbol -> Incident. Selected (b)+(c), DT optional. Benchmark: 1,000-component BOM vs `all.zip`: match set equals `osv-scanner`-class tool output; <5 min offline on one node. Dependencies: license metadata of feeds, tenant-scoped storage, BL-25 tombstones. Defensibility: joins to code, ownership and incidents. ADOPT. |
| INV-dt-02 | v5 no in-place upgrade and PostgreSQL-only [CLAIM-dt-02]; cause deployment. Mitigation: treat DT as external/optional source; do not embed. ADOPT. No 10.5 seed applies. |

## 13. Decisions

CAP-68 dependency/SBOM risk: BUILD native OSV matcher (REUSE OSV schema, data under per-source licences) + INTEGRATE DT as optional connector. CAP-79 supply chain: REUSE existing `compliance/sbom.py`; extend with SPDX output - EXPERIMENT. CAP-69: BUILD. CAP-40 lineage: BUILD component-to-commit linkage. deps.dev: EXPERIMENT as optional online enrichment (egress policy, CAP-51). Policy engine CEL: REFERENCE.

## 14. Tests/POC

(1) Extend connector to parse `dependencies`/`relationships`; assert graph edges equal BOM tree on a 500-component fixture. (2) OSV matcher on `all.zip` snapshot vs DT 5.2.1 findings for the same BOM; accept >= 95% agreement, differences explained. (3) air-gap run with network denied. (4) tenant B sees no tenant A components.

## 15. Risks

Feed licences (CC-BY-NC-ND) restrict redistribution; purl drift; DT v4/v5 split. Open: DT v5 SPDX support, graph-export API.

## Appendix A - Dimensions

| Dim | Sec | Summary |
|---|---|---|
| D1 | 1 | Apache-2.0 / OWASP, active |
| D2 | 2 | portfolio risk |
| D3 | 4 | stateless API + PostgreSQL |
| D4 | 5 | relational |
| D5 | 5 | OSV ranges, purl |
| D6 | N/A | REST |
| D7 | N/A | none |
| D8 | 5,7 | v5 scale-out |
| D9 | 2,5 | CI upload, feed mirror |
| D10 | 5 | analysis state |
| D11 | 5 | project versions |
| D12 | 3 | EPSS |
| D13 | N/A | none |
| D14 | N/A | none |
| D15 | 3 | policies |
| D16 | 3 | web UI |
| D17 | 3 | OpenAPI |
| D18 | 5 | OIDC, HMAC webhooks |
| D19 | 3 | portfolio ACL |
| D20 | 7 | vendor numbers |
| D21 | 10 | free |
| D22 | 3,9 | CycloneDX focus |
| D23 | N/A | none found |
| D24 | 7 | docs and announcement |

## Appendix B - Capabilities

| CAP | Tech | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-68 | native | 01,03 | partial: connector only | BUILD+INTEGRATE | P1 |
| CAP-79 | partial | 03 | `compliance/sbom.py` implemented | REUSE | P2 |
| CAP-69 | partial | 05 | BL-41/42 | BUILD | P1 |
| CAP-26 | native | 01 | BL-23 | INTEGRATE | P2 |
| CAP-40 | absent | 03 | BL-41 | BUILD | P2 |

## Appendix C - Evidence

| ID | Product/date | Claim | Class | Source | Dates/conf | Contra |
|---|---|---|---|---|---|---|
| CLAIM-dt-01 | DT 5.2.1/5.2.0/5.1.2 | releases, fixes, Apache-2.0 | Officially documented | https://github.com/DependencyTrack/dependency-track/releases | 2026-10-26, 0.8 | page shows no year |
| CLAIM-dt-02 | DT v5 | architecture, PostgreSQL only, migration | Officially documented | https://owasp.github.io/blog/2026/06/09/dependency-track-v5 | 2026-06-09 / 0.85 | none |
| CLAIM-dt-03 | DT v4.x docs | CycloneDX, sources, policies | Officially documented | https://docs.dependencytrack.org/ | 0.8 | v5 docs separate |
| CLAIM-dt-04 | deps.dev v3 | endpoints, ecosystems, CC-BY | Officially documented | https://docs.deps.dev/api/v3/ | 0.8 | rate limits unstated |
| CLAIM-dt-05 | OSV schema 1.9.2 | fields, ranges | Officially documented | https://ossf.github.io/osv-schema/ | 2026-10-13 / 0.9 | none |
| CLAIM-dt-06 | osv.dev | per-source licences, dump | Officially documented | https://google.github.io/osv.dev/data/ | 0.85 | none |
| CLAIM-dt-07 | EOIP code | SBOM modules behaviour | Observed in source code | `packages/eoip/compliance/sbom.py`, `packages/eoip/connectors/sbom.py` at HEAD 896e06d | 2026-10-26 / 0.9 | none |

## Appendix D - Assumptions

Dependency-Track v5 SPDX and mirroring behaviour not read; "dex" taken from release notes. 01a delta used for library-only status.
