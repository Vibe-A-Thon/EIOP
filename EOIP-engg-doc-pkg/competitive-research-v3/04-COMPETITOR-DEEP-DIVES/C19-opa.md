# C19 — Open Policy Agent / Rego

| Field | Value |
|---|---|
| Registry ID | T-C19-opa |
| Tier | B (policy-as-code reference; EOIP has in-house YAML policy engine) |
| Versions examined | OPA v1.21.4 (release page "23 October", year not shown, 2026 inferred) |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
OPA: general-purpose policy engine, Rego language, embeddable Go library or daemon. CNCF **Graduated** (accepted 2018-03-29) [CLAIM-opa-01]. Licence Apache-2.0 (from project knowledge; LICENSE not re-fetched, confidence 0.85). **Governance change:** in 2025 Apple hired Styra's co-founders and senior engineers; the official OPA blog says OPA stays a CNCF graduated project, no change to governance or licensing, and no change to the maintainer list except affiliation Styra -> Apple for those who moved [CLAIM-opa-02]. One third-party July 2026 post claims styra.com DNS fails and the StyraInc GitHub org returns 404 (single unofficial source; UNVERIFIED, confidence 0.3) [CLAIM-opa-03]. Consequence: commercial Styra DAS/EOPA support path is uncertain; the open project continues (v1.21.4 released days ago).

## 2. Problem, workloads, workflows
Decouple authorization/admission/config policy from code: service sends `input` JSON, OPA returns decision. Workflows: API gateway allow/deny, Kubernetes admission (Gatekeeper), CI policy, and **data filtering** (compile policy to SQL conditions) [CLAIM-opa-05].

## 3. Feature inventory
| Capability | Status |
|---|---|
| Rego evaluation, REST server, Go embed | present |
| Bundles (signed, polled), decision logs | present |
| WASM compilation | present (not re-verified) |
| Partial evaluation / data-filter compile to SQL (UCAST) | present; Elasticsearch/OpenSearch target NOT confirmed [CLAIM-opa-05] |
| Policy testing, `opa bench`, profiling | present [CLAIM-opa-04] |
| Relationship graph storage / Zanzibar-style recursion at scale | absent (data lives in memory) |
| Per-tenant isolation | partial: caller-supplied `input`/bundle per tenant |
| UI | absent (Styra DAS commercial; fate uncertain) |

## 4. Architecture
```
App/PEP --input JSON--> [OPA: in-memory store (data.json from bundles/push) + compiled Rego] --decision--> App
Control: bundle server (HTTP/S3/OCI) --signed bundle--> OPA ; OPA --decision logs--> sink
Filtering: PEP --compile(query, unknowns)--> residual conditions --> SQL WHERE
```

## 5. Under-the-hood reconstruction
- Model: Rego is Datalog-derived, declarative; rules over JSON documents `input` and `data`. Policies compiled to an AST/IR then evaluated top-down with backtracking; **evaluation is single-threaded per query**, concurrency from the server [CLAIM-opa-04].
- Indexing: equality, glob, prefix/suffix, membership, `and`/`or` are indexed; negated expressions never; linear fragment gives near-constant time as rules grow; partial evaluation (`-O=1`) pre-inlines [CLAIM-opa-04].
- Data/memory: JSON in OPA costs about 20x its compact size (8 MB JSON for 100,000 permissions ~160 MB RAM); 10,000 ACL-style rules ~130 MB, 100,000 ~1.1 GB, linear in rule count [CLAIM-opa-04]. Hence OPA is a good **policy** evaluator but a poor store for millions of per-document grants.
- Partial evaluation: known inputs resolved, expressions over declared unknowns become conditions per rule body; groups OR-ed and translated to SQL [CLAIM-opa-05]. A retrieval PEP could emit `WHERE acl && principals` style filters; hypothesis for vector/BM25 engines.
- Consistency: bundle version only; no zookie; staleness bounded by polling interval. Security: signed bundles, TLS/authn on server; decision logs for audit.

## 6. Requirements inferred
FR: deterministic decision, explain trace, policy test harness, versioned bundles. NFR: sub-ms decisions on warm rules, bounded memory, hermetic offline operation.

## 7. Performance and resource model
Vendor guidance only (above); no hardware-qualified latency figure fetched, so none is quoted. Use `opa bench` for per-policy ns/op. Failure modes: unindexed negations, large `data` blowing RAM/GC (`GOMEMLIMIT` advice), array scans.

## 8. Strengths
General-purpose, testable policy-as-code usable for egress, admission, ABAC and masking; compile-to-filter pattern; graduated governance; rich ecosystem (Regal linter, Gatekeeper). Match: EOIP `authz/core.py` `PolicyStatement` YAML has role/action/Condition only; exceed with Rego-grade expressiveness only if required, else keep native.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | not a relationship index; deep group recursion is evaluated in-memory per query |
| Operational | RAM linear in data; bundle push staleness |
| Friction | Rego learning curve; unfamiliar to enterprise admins |
| Governance | Styra commercial layer in doubt [CLAIM-opa-02/03] |

## 10. Deployment, licensing, viability
Apache-2.0 permissive; single Go binary; fully air-gap viable; embeddable via Go (EOIP is Python: sidecar or WASM). No GPL/AGPL. Redistribution OK subject to licence notices; no legal trigger.

## 11. Delta vs EOIP baseline
BL-19: `authz/core.py` PolicyEnforcer (YAML statements with `Condition.matches` on resource attrs) = API-action RBAC/ABAC. `authz/pdp.py` `can_read` deny-by-default with classification levels and `PolicyEpochRegistry` is an in-house PDP; EOIP lacks decision logs as a separate artefact comparable to OPA's, policy bundle signing, and a policy test/bench tool. `egress/policy.py` is a matrix engine (data class x task type). BL-18/BL-20: OPA does not close them by itself; it would evaluate rules, while the grant data still must be stored and filtered at the index.

## 12. Cards
**STR-opa-01** | OPA | Compile-to-filter (partial evaluation) | CLAIM-05 | policy-defined retrieval pre-filters | experiment | PEP asks OPA to partially evaluate with `input.doc` unknown, translate residual to index filter | for 1,000 mixed-ACL docs, filter results equal full per-doc evaluation (differential test).
**STR-opa-02** | OPA | Policy test + bench + signed bundles | CLAIM-04 | auditable egress/ABAC policy | match | add policy unit-test and signature to `authz/core` loader | tampered bundle rejected.
**INV-opa-01** (data-in-memory, proven by vendor memory table) | not a ReBAC store; options: (1) keep grants in ReBAC engine, OPA only for attribute rules; (2) native `can_read` index; (3) differentiated: ReBAC lookup + OPA residual. Selected 1. Benchmark: 100k grants latency and RAM. Defensible via integration. Decision ADOPT boundary. Failure case: stale bundle grants removed access late.
**INV-opa-02** (vendor continuity, hypothesis) | Mitigation: depend only on the CNCF open project, vendor no Styra product. Decision ADOPT.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-45 ABAC policy language | EXPERIMENT (Rego for egress/ABAC rules); keep native YAML default |
| Policy-to-filter compile | EXPERIMENT |
| CAP-46 grant storage | REJECT OPA for this (use ReBAC) |
| Decision logging | BUILD in `authz` (OPA-style records) |

## 14. Tests
1. Differential test: compiled filter vs per-doc eval. 2. `opa bench` budget per policy. 3. Offline bundle load/verify. 4. Rego policy for egress matrix equals `egress/policy.py` decisions on a golden corpus.

## 15. Risks / open questions
Python embedding path; Elasticsearch/OpenSearch filter target unconfirmed; Styra status; Rego skills.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | graduated, Apache-2.0, Apple affiliation |
| D2 | 2 | policy decisions |
| D3 | 4 | PEP/PDP/bundle |
| D4,D9-D12,D14,D19 | N/A | not data store |
| D5-D7 | 5 | Rego semantics, indexing |
| D8 | 5,7 | memory model, single-thread eval |
| D13 | 5,11 | filter compile |
| D15-D17 | 3,8 | tests, linter |
| D18 | 5 | signed bundles, decision logs |
| D20 | 7 | vendor figures |
| D21 | 10 | permissive |
| D22 | 8 | WASM portability |
| D23 | N/A | none found |
| D24 | App C | docs only |

## Appendix B — Capabilities
| CAP | OPA | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-45 | native | 04 | BL-19 Implemented | EXPERIMENT | P2 |
| CAP-46 | partial (filters) | 05 | BL-18 Absent/partial | EXPERIMENT | P0 support |
| CAP-48 | partial (decision logs) | 04 | BL-19 | BUILD | P2 |
| CAP-51 | native | 04 | BL-45 Implemented | REFERENCE | P3 |

## Appendix C — Evidence
| CLAIM | product/date | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-opa-01 | OPA | CNCF Graduated, accepted 2018-03-29 | Officially documented | https://www.cncf.io/projects/ | n/a / 2026-10-26 | 0.9 | none |
| CLAIM-opa-02 | OPA 2025 | Apple hired Styra founders; OPA remains CNCF graduated, no governance/licence change, maintainer list unchanged except affiliation | Officially documented + press | https://openpolicyagent.org/blog/note-from-teemu-tim-and-torin-to-the-open-policy-agent-community-2dbbfe494371 ; https://www.opensourceforu.com/2025/08/apple-acquires-open-policy-agent-developers-while-cncf-retains-control-of-open-source-project/ | 2025-08 / 2026-10-26 | 0.8 | press says "acquired developers" vs "not company" |
| CLAIM-opa-03 | Styra | styra.com DNS fails, StyraInc org 404 (Jul 2026) | Third-party report | https://www.youngju.dev/blog/2026-07-17-opa-post-styra-apple-acquihire-reality.en | 2026-07-17 / 2026-10-26 | 0.3 single unofficial source | none |
| CLAIM-opa-04 | OPA docs | indexing rules, single-threaded eval, memory figures 20x, 130 MB/10k rules, 1.1 GB/100k rules, GOMEMLIMIT | Officially documented | https://www.openpolicyagent.org/docs/policy-performance | n/a / 2026-10-26 | 0.85 | vendor guidance |
| CLAIM-opa-05 | OPA docs | partial eval with unknowns produces condition groups OR-ed into SQL; ES/OpenSearch target not stated | Officially documented | https://www.openpolicyagent.org/docs/filtering/partial-evaluation | n/a / 2026-10-26 | 0.8 | none |
| CLAIM-opa-06 | OPA v1.21.4 | latest release tag, 23 Oct | Officially documented | https://github.com/open-policy-agent/opa/releases/latest | year not shown | 0.8 | none |

## Appendix D — Assumptions
Apache-2.0 assumed from project knowledge; release year inferred; Styra continuity treated as UNVERIFIED.
