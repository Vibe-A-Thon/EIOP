# C15 — Semgrep

| Field | Value |
|---|---|
| Registry ID | T-C15-semgrep |
| Tier | B — pattern-based code analysis; CE engine vs rules licence split |
| Versions examined | Semgrep CE v1.182.0 (2026-10-20); `semgrep/semgrep-rules` pushed 2026-10-24 |
| Verified on | 2026-10-26 (brief date 2026-10-18) |
| Worker | V28 (W27 scope) |

## 1. Identity, current status, tier, and sources

| Item | Finding | Claim |
|---|---|---|
| Identity | Semgrep (Semgrep, Inc.): pattern matcher over syntax trees with YAML rules; products: Community Edition (CE) CLI, Semgrep Code (AppSec Platform), Supply Chain, Secrets | [CLAIM-semgrep-01][CLAIM-semgrep-02] |
| Status | Active; v1.182.0 on 2026-10-20; 17.3k stars | [CLAIM-semgrep-01] |
| Engine licence | LGPL-2.1 (repo) | [CLAIM-semgrep-01] |
| Rules licence | `semgrep-rules` repo carries "Semgrep Rules License v1.0" (not an OSI licence); registry rules are described by docs as open-source-licensed, Pro rules proprietary: docs and repo differ | [CLAIM-semgrep-03][CLAIM-semgrep-02] |
| Platform licence | Semgrep Code "proprietary software suite"; free for up to 10 contributors | [CLAIM-semgrep-02] |

## 2. Primary problem, workloads, workflows

Fast SAST, secret and policy checks with readable rules. Workflows: `semgrep scan` in CI; custom rules for house conventions; EOIP J10: rule that finds callers of a business-rule function, results become evidence nodes.

## 3. Feature inventory

| Feature | CE | Platform/Pro | Claim |
|---|---|---|---|
| Single-file pattern matching, 30+ languages | present | 35+ (Apex only here) | [CLAIM-semgrep-02] |
| Taint analysis | single function | cross-function, cross-file | [CLAIM-semgrep-02] |
| Constant propagation | cross-function within one file | cross-file | [CLAIM-semgrep-02] |
| Cross-file analysis | absent | present | [CLAIM-semgrep-02] |
| Pro rules | absent | present (docs give 600+ via CLI login and 20,000+ in Platform; unreconciled) | [CLAIM-semgrep-01] |
| AI triage (Assistant) | absent | present | [CLAIM-semgrep-01] |
| Local scanning, code not uploaded by default | present | present | [CLAIM-semgrep-01] |
| Metrics to semgrep.dev | registry configs send pseudonymous rule metrics; `--metrics=off` | n/a | [CLAIM-semgrep-01] |

## 4. Architecture diagram

```
 rules (YAML) + files --> tree-sitter-based parse (recalled) --> generic AST --> matcher (OCaml engine, recalled)
 CE: per-file/per-function ; Pro engine (proprietary): inter-file indexing, needs login
 findings (JSON/SARIF) --> CI / Platform dashboard
```

## 5. Under-the-hood reconstruction

- Data model: rules over a language-generic AST; metavariables, patterns, taint sources/sinks/sanitizers (recalled from rule syntax; UNVERIFIED here).
- Pipeline: parse, normalise to generic AST, match patterns with metavariable unification; taint is intra-procedural in CE [CLAIM-semgrep-02]. Engine implementation language (OCaml) and use of Tree-sitter are recalled, UNVERIFIED in this run.
- Storage: none (stateless scan); Platform stores findings (proprietary, NOT PUBLICLY VERIFIED).
- Concurrency/partitioning: per-file parallel scan (recalled, UNVERIFIED). Security: runs locally; remote rule configs trigger metrics [CLAIM-semgrep-01].
- Reasoning/versioning/caching: N/A.

## 6. Requirements inferred

Rules as code in VCS; CI-speed scanning; per-language syntax support.

## 7. Performance and resource model

Vendor claims of speed not retrieved. NOT PUBLICLY VERIFIED. Failure modes: CE misses cross-file flows [CLAIM-semgrep-02]; findings without cross-file context raise false positives (vendor statement that cross-file reduces them).

## 8. Strengths

| Strength | Match or exceed |
|---|---|
| Readable rules, low barrier | EOIP could emit rules from ontology constraints (reasoned) |
| LGPL engine embeddable as CLI | INTEGRATE as external process |
| Fast local scan | cheap rule-evidence on each commit |

## 9. Limitations

| Class | Finding | Claim |
|---|---|---|
| Licensing | Rules licence restricts use to internal business, forbids distribution and offering as service | [CLAIM-semgrep-03] |
| Edition split | Cross-file and cross-function taint are not in CE | [CLAIM-semgrep-02] |
| Operational | Pro features need login (implies network); offline Pro not stated | [CLAIM-semgrep-01] |
| Telemetry | Default registry metrics | [CLAIM-semgrep-01] |

## 10. Deployment, licensing, redistribution

CE engine: LGPL-2.1, runs offline with local rules and `--metrics=off`; linking/distribution obligations of LGPL need legal review if shipped inside a product (shipping as unmodified separate binary is the usual lower-risk path; not a legal conclusion). Rules: Semgrep Rules License v1.0 (semgrep.dev/legal/rules-license, read 2026-10-26): non-exclusive, royalty-free, worldwide, non-sublicensable, non-transferable licence "for your own internal business purposes"; modifications allowed with prominent modification notices; "does not allow you to distribute the rules, or to make them available to others as a service"; notices must not be removed; patent licence terminates if you claim the rules or Semgrep infringe a patent; competing-product use not addressed. Consequence: EOIP cannot bundle or white-label the Semgrep registry rules; it may ship its own rules written for CE, and let customers fetch registry rules for their internal use. Legal-review trigger: yes. Pro engine/Platform: proprietary, not redistributable [CLAIM-semgrep-02].

## 11. Competitive delta against EOIP baseline

BL-42 has no pattern/rule scan. Semgrep supplies cheap, rules-driven findings; tree-sitter-based EOIP parser (C15-tree-sitter.md) could host equivalent matching, but reimplementing 30+ languages is poor value. See C15-codeql.md and C15-joern.md for deeper flow tools.

## 12. Cards

`STR-semgrep-01 | Semgrep CE | low-friction rule engine, LGPL | CLAIM-01,02 | house-rule checks for J10 | integrate | subprocess runner, JSON output into SourceEvent with PROPOSED status, rules authored in-house | 20 custom rules on fixture; each finding has span; metrics off verified by network capture`

INV-semgrep-01: target CE 1.182.0; workload cross-file taint. Limitation: single-function taint (proven, CLAIM-02). Root cause: edition split (licensing/product). Alternative: Joern flows or EOIP graph joins over call edges; worse for subtle sanitiser logic. Options: (a) CE only, (b) CE plus Joern for flows, (c) native call-graph join. Selected (b). POC: 10 seeded cross-file flows; metric recall vs CE alone. Decision: EXPERIMENT. Seed hypotheses in §10.5 do not target Semgrep.

## 13. Decisions

| Capability | Decision |
|---|---|
| Pattern scan engine | INTEGRATE (CE, external process) |
| Registry rules bundling | REJECT |
| Own ruleset | BUILD |

## 14. Tests and acceptance

Offline scan with `--metrics=off` and no network (verify with egress capture, BL-45); licence inventory of shipped rules; SBOM entry for engine.

## 15. Risks and open questions

Rules-licence reading across registry subsets; LGPL distribution form; Pro engine offline availability; future licence changes.

## Appendix A — Dimension coverage

| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | Active; LGPL/proprietary split |
| D2 | 2 | SAST/policy |
| D3 | 4 | CLI plus Platform |
| D4 | N/A | Stateless |
| D5 | 5 | Rule syntax |
| D6 | 5 | Pattern matching |
| D7 | N/A | None |
| D8 | N/A | Batch |
| D9 | N/A | File scan |
| D10 | N/A | None |
| D11 | N/A | None |
| D12 | N/A | AI triage only (Pro) |
| D13 | 3 | Assistant |
| D14 | N/A | Absent |
| D15 | 3 | Platform policy |
| D16 | 3 | CLI/dashboard |
| D17 | 3 | YAML rules |
| D18 | 3,9 | Metrics, login |
| D19 | N/A | Platform only |
| D20 | 7 | No figures |
| D21 | 10 | Rules licence quoted |
| D22 | 3 | JSON/SARIF recalled |
| D23 | N/A | Not checked |
| D24 | 15 | Docs-level |

## Appendix B — Capability mapping

| CAP | Technology | Claim | EOIP baseline | Decision | Pri |
|---|---|---|---|---|---|
| CAP-66 | partial | 02 | BL-42 | INTEGRATE | P3 |
| CAP-33 | plugin (secrets) | 02 | BL-46 | DEFER | P3 |
| CAP-77 | n/a | 03 | BL-22 | REJECT rules bundling | P1 |

## Appendix C — Evidence records

| CLAIM | product/version/date | claim | class | source | dates | confidence | contradiction |
|---|---|---|---|---|---|---|---|
| 01 | CE 1.182.0 | LGPL-2.1, 30+ languages, Pro login, metrics, v1.182.0 on 2026-10-20 | Officially documented | https://github.com/semgrep/semgrep | 2026-10-20 / 2026-10-26 | 0.85 | rule counts unreconciled |
| 02 | docs | CE vs Semgrep Code table | Officially documented | https://docs.semgrep.dev/semgrep-pro-vs-oss | 2026-10-26 | 0.85 | none |
| 03 | Rules License v1.0 | internal use only, no distribution/service | Officially documented | https://semgrep.dev/legal/rules-license ; repo LICENSE https://github.com/semgrep/semgrep-rules | 2026-10-26 | 0.85 | docs page says registry rules have open source licences |

## Appendix D — Assumptions

Tree-sitter/OCaml internals recalled not verified; rule-licence applicability to every registry rule not checked.
