# C05 Secret scanners (gitleaks, TruffleHog, detect-secrets; Betterleaks noted)

| Field | Value |
|---|---|
| Registry ID | T-C05-secret-scanners |
| Tier | B (secret detection at ingest; grouped) |
| Versions examined | gitleaks v8.30.1 (2026-03-21); TruffleHog v3.99.7 (2026-10-24); detect-secrets 1.5.0 (2024-05-06); Betterleaks (no release shown) |
| Verified on | 2026-10-18 (re-read 2026-10-26) |
| Worker | V17 |

## 1. Identity, current status, tier, and sources
| Tool | Owner | Licence | Status |
|---|---|---|---|
| gitleaks | Zachary Rice (gitleaks org) | MIT | "feature complete", security patches only; maintainer moving focus to Betterleaks [CLAIM-sec-01] |
| Betterleaks (successor candidate) | betterleaks org, by gitleaks team | MIT | v2 in development on main, v1.x maintained; no stable v2 [CLAIM-sec-02] |
| TruffleHog | Truffle Security | **AGPL-3.0 since v3.0** (earlier GPL-2.0); Enterprise product separate | very active, v3.99.7 24 Oct; v3.99.5 tag unpublished [CLAIM-sec-03] |
| detect-secrets | Yelp | Apache-2.0 | last PyPI release 1.5.0 (2024-05-06); 99 open issues, 91 open PRs [CLAIM-sec-04] |
Overlap with EOIP `egress/dlp.py` (BL-45) and `privacy/scanner.py` (BL-46). Related C19 scanners belong to another worker.

## 2. Primary problem, workloads, workflows
Find credentials in git history, files and text. EOIP ingest use: scan raw capture of each SourceEvent payload before it reaches the graph or an LLM, quarantine or redact, and emit a finding as an evidence-linked governance event, never persist the secret.

## 3. Feature inventory
| Feature | gitleaks | TruffleHog | detect-secrets |
|---|---|---|---|
| Scan git history, dir/file | git, dir, stdin [CLAIM-sec-01] | git, filesystem, many sources [CLAIM-sec-03] | files, staged diffs, baseline |
| Scan arbitrary text on stdin (ingest fit) | yes [CLAIM-sec-01] | filesystem only on page read (stdin UNVERIFIED) | library API (UNVERIFIED) |
| Rules | TOML, `[[rules]]`, allowlists, entropy, keywords, composite rules from v8.28 [CLAIM-sec-01] | 800+ secret types; 700+ detectors with active verification [CLAIM-sec-03] | 27 plugins [CLAIM-sec-04] |
| Verification | none (core) | calls the service API; `--no-verification` to disable [CLAIM-sec-03] | optional network verify; `--no-verify` [CLAIM-sec-04] |
| Baseline of known secrets | allowlists | n/a | `.secrets.baseline`, audit workflow [CLAIM-sec-04] |
| Match location | line/column in report (UNVERIFIED in docs read) | source metadata (UNVERIFIED) | line number (UNVERIFIED) |
| Update check network call | not stated | yes; `--no-update` [CLAIM-sec-03] | no |

## 4. Architecture
```
source (git|dir|stdin) -> chunker -> keyword prefilter -> regex/entropy rules
 -> [allowlist / baseline filter] -> (TruffleHog: verify via vendor APIs)
 -> report JSON/SARIF -> exit code
```

## 5. Under-the-hood reconstruction
All three are stateless scanners. Gitleaks: keyword prefilter then regex with optional entropy and path scopes, TOML-extendable [CLAIM-sec-01]. TruffleHog: detector per credential type; results classed verified / unverified / unknown (network failure); private-key check via Driftwood; custom regex detectors can POST to a webhook [CLAIM-sec-03]. Detect-secrets: plugin set + baseline of hashed secrets (hash behaviour from knowledge, UNVERIFIED here). Betterleaks adds Expr-based validation, BPE filtering of natural-language false positives, analysis of valid credentials [CLAIM-sec-02]. Hypothesis for ingest: run scanners in a sandboxed subprocess on the raw payload file, parse report offsets.

## 6. Requirements inferred
FR: offsets for redaction; rule extension per tenant; no raw secret in logs/findings; verification off by default. NFR: zero egress (including update checks); deterministic output; throughput per MB.

## 7. Performance and resource model
Independent: ESEM 2023 study (SecretBench, 5 OSS + 4 commercial tools): gitleaks recall 88% / precision 46%; TruffleHog recall 52%; GitHub Secret Scanner precision 75%; false positives from generic regex and weak entropy, false negatives from rules and skipped file types [CLAIM-sec-05]. Versions are 2023-era; a later paper's baselines gave precision <50% and recall <41% but that paper promotes its own tool [CLAIM-sec-05]. Throughput and memory: NOT PUBLICLY VERIFIED here.

## 8. Strengths
Gitleaks: single static MIT binary, stdin mode, TOML rules. TruffleHog: breadth and verification (lowers false positives for triage). Detect-secrets: baseline/audit workflow, Python-embeddable. Match: reuse rules, not engines; exceed with tenant rule packs and evidence-linked findings.

## 9. Limitations
Licensing: TruffleHog AGPL-3.0 [CLAIM-sec-03] (legal-review trigger: network copyleft, binding or linking is the question; separate-process use is a legal question, not concluded here). Verification sends live credentials to third-party APIs: incompatible with air-gap and egress default S0. Maintenance: gitleaks feature-frozen, detect-secrets stale, Betterleaks unreleased. Accuracy: high false positives on generic rules [CLAIM-sec-05]. Multi-line secrets are a known detect-secrets gap [CLAIM-sec-04].

## 10. Deployment, licensing, viability
Gitleaks MIT and detect-secrets Apache-2.0: redistributable, air-gap viable (rules local). TruffleHog: only with `--no-verification --no-update`, and only after legal review; EOIP should not ship it. Betterleaks MIT: candidate, wait for stable v2.

## 11. Competitive delta
EOIP `egress/dlp.py`: ~9 regex classes (AWS key, JWT, generic key=value, SSN, card...) plus Shannon entropy and dictionary terms, stdlib only, over the egress payload (BL-45). It runs at egress, not at ingest; no git-history scan; no rule corpus. Gitleaks rules are a ready, MIT-licensed corpus of provider patterns. EOIP has no ingest-time secret quarantine (gap to BL-23/24 pipeline).

## 12. Cards
STR-sec-01 | gitleaks | MIT rule corpus + stdin scan | CLAIM-sec-01 | provider-specific patterns at low cost | integrate/reuse | run as sandboxed subprocess or import rules into `DlpScanner` | recall >=0.88 on SecretBench-like set at precision >=0.5.
STR-sec-02 | detect-secrets | baseline+audit triage | CLAIM-sec-04 | tame false positives | match | per-tenant baseline of reviewed non-secrets | FP rate falls >50% after one review pass.
INV-sec-01 | AGPL + live verification in TruffleHog (proven) | root: licensing/semantics | options: quick (exclude), native (offline format-validation of well-known keys, e.g. checksums), long-term (opt-in tenant-hosted verifier under egress policy). Select quick+native. Benchmark: precision gain of offline validators on SecretBench subset. Decision REJECT TruffleHog; EXPERIMENT offline validators.
INV-sec-02 | maintenance fragmentation (proven) | root: maturity | vendor rules into EOIP-owned pack with provenance. ADOPT.

## 13. Per-capability decisions
CAP-33 secret detection at ingest: BUILD ingest gate; REUSE gitleaks rule corpus (and INTEGRATE gitleaks binary optional); EXPERIMENT Betterleaks; REJECT TruffleHog bundling; detect-secrets baseline idea: REUSE pattern. CAP-51: reuse egress policy for any verification.

## 14. Tests / PoC
Build 500-sample corpus (real-format fake keys in code, logs, docs, JSON) plus 500 benign high-entropy items; run in-house DLP, gitleaks (default rules), detect-secrets, Betterleaks; record P/R, offsets usable for redaction, wall time; packet capture proves zero egress. Accept: best configuration >= in-house recall by 20 points, no raw secret in any stored finding.

## 15. Risks / open questions
Licence reading for AGPL (legal); Betterleaks stability; offset availability per tool; adversarial encodings; prompt text containing secrets; scanner as attack surface (parsing untrusted blobs).

## Appendix A. Dimension coverage
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1 | MIT / AGPL / Apache; maintenance mixed |
| D2 | 2 | ingest scan |
| D3 | 4 | scanner pipeline |
| D4-D8 | N/A | stateless |
| D9 | 2 | ingest gate |
| D10 | 2,12 | secret handling |
| D11 | N/A | none |
| D12 | N/A | rules, entropy |
| D13-D17 | N/A | none |
| D18 | 9 | verification egress |
| D19 | 12 | tenant rule packs |
| D20 | 7 | no numbers |
| D21 | 9,10 | AGPL, enterprise |
| D22 | 10 | JSON/SARIF |
| D23 | N/A | none |
| D24 | 7 | 2023 study |

## Appendix B. Capability mapping
| CAP | This tech | CLAIM | EOIP baseline | Decision | P |
|---|---|---|---|---|---|
| CAP-33 | native | 01,03,04 | BL-45 partial, BL-46 | REUSE rules / BUILD gate | P1 |
| CAP-50 | partial | 03 | BL-45 | INTEGRATE (verification off) | P1 |
| CAP-51 | partial | 03 | BL-45 | INTEGRATE | P2 |
| CAP-79 | partial | 01 | n/a | DEFER | P3 |

## Appendix C. Evidence records
| CLAIM | Product/version/date | Claim | Class | Source | Dates | Confidence | Contra |
|---|---|---|---|---|---|---|---|
| sec-01 | gitleaks 8.30.1 | MIT; feature complete; stdin/dir/git; TOML; v8.30.1 21 Mar | Officially documented | https://github.com/gitleaks/gitleaks ; /releases | 2026-10-26 | 0.8 | year inferred |
| sec-02 | Betterleaks | MIT; v2 in dev; validation, BPE filter | Officially documented | https://github.com/betterleaks/betterleaks | 10-26 | 0.7 | no release |
| sec-03 | TruffleHog v3.99.7 | AGPL-3.0 since v3.0; verification calls APIs; flags; 24 Oct | Officially documented | https://github.com/trufflesecurity/trufflehog ; /releases | 10-26 | 0.85 | LICENSE file not fetched |
| sec-04 | detect-secrets 1.5.0 | Apache-2.0; 27 plugins; baseline; gaps; 2024-05-06 | Officially documented | https://github.com/Yelp/detect-secrets ; https://pypi.org/pypi/detect-secrets/json | 10-26 | 0.85 | none |
| sec-05 | SecretBench study | recall/precision numbers | Independent paper | https://arxiv.org/pdf/2307.00714 (via search) | 10-26 | 0.6 | 2023 versions |

## Appendix D. Assumptions
Years for GitHub release dates inferred as 2026. Match-location fields marked UNVERIFIED rather than assumed.
