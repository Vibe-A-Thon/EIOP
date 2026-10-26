# C19 — Cedar and Cerbos

| Field | Value |
|---|---|
| Registry ID | T-C19-cedar-cerbos |
| Tier | B (policy languages/engines) |
| Versions examined | Cedar: cedar-policy-cli v4.14.0 (17 Oct), docs guide v4.6; Cerbos v0.57.0 (23 Oct); years not shown, 2026 inferred |
| Verified on | 2026-10-26 |
| Worker | V11 |

## 1. Identity, status, sources
| Member | Owner / governance | Licence | Status |
|---|---|---|---|
| Cedar | AWS-originated; **CNCF Sandbox** (accepted 2025-10-08) [CLAIM-cc-01]; Rust | Apache-2.0 (project knowledge, not confirmed on docs page read; 0.8) | active |
| Cerbos | Cerbos Ltd; "open-core authorization management platform" | Apache-2.0 for `cerbos/cerbos` (verified) [CLAIM-cc-03] | active, 4.6k stars |
Cerbos Hub and Synapse are separate (commercial) components [CLAIM-cc-04]; which features sit behind them is NOT PUBLICLY VERIFIED here.

## 2. Problem and workflows
Application-level fine-grained authorization with human-readable policy: "can principal P do action A on resource R given context C". Cedar is a language + evaluation library embedded in the app; Cerbos is a stateless PDP service (sidecar/service/Lambda) with YAML policies. Workflow: EOIP API authorises `view` on `document` with attributes (classification, source ACL group, tenant) -> decision plus audit record.

## 3. Feature inventory
| Capability | Cedar | Cerbos |
|---|---|---|
| Policy language | Cedar DSL (permit/forbid, principal-action-resource-context) | YAML + CEL conditions (CEL: project knowledge, 0.7) |
| Schema validation of policies | present; schema not used at evaluation [CLAIM-cc-02] | present (schemas for attributes, optional) |
| Decision API | library call `is_authorized` | `CheckResources` (default 50 resources x 50 actions per request) [CLAIM-cc-04] |
| List-what-can-I-access | partial-evaluation support exists in Cedar ecosystem (UNVERIFIED) | **PlanResources**: ALWAYS_ALLOWED/DENIED/CONDITIONAL with condition AST; adapters Prisma, Drizzle, Mongoose, Convex, LangChain/ChromaDB, SQLAlchemy [CLAIM-cc-04] |
| Relationship (ReBAC) store | absent (entities passed in request) [CLAIM-cc-02] | absent (attributes passed in) |
| Audit | via embedding app | audit log with `cerbosCallId` [CLAIM-cc-04] |
| Policy storage | app-managed | disk, object store, git, SQLite [CLAIM-cc-03] |

## 4. Architecture
```
Cedar:  App --(policies, entities, request)--> cedar lib (in-process) --> Allow/Deny + diagnostics
Cerbos: App --gRPC/HTTP--> [Cerbos PDP: policy store (git/disk)] --> effect per action + audit log
        App --PlanResources--> condition AST --> adapter --> DB/vector-store filter
```

## 5. Under-the-hood reconstruction
- Cedar semantics: default deny; any matching `forbid` overrides `permit`; evaluation is a pure function of (policies, entities, request), no side effects, bounded latency; policies can be indexed for retrieval [CLAIM-cc-02]. Designed to be analysable (symbolic analysis; Lean/Dafny-based verification of the Rust implementation reported by AWS - not confirmed on the docs page read, UNVERIFIED 0.6).
- Entities (hierarchy of principals/groups/resources with attributes) must be supplied per request: the application resolves membership first, so deep group graphs are the caller's problem (contrast ReBAC engines).
- Cerbos: resource policies by kind, derived roles, principal policies, scopes (docs index; detail not re-verified). Evaluation: request carries principal and resource attributes; conditions evaluated by a CEL-style engine (hypothesis); stateless PDP scales horizontally; `PlanResources` partially evaluates policies with resource attributes unknown and returns a condition tree combined (AND across actions) [CLAIM-cc-04].
- Consistency: none beyond the policy-bundle version; no tokens. Security: signed/hosted policy via Hub (commercial); deny by default.

## 6. Requirements inferred
FR: ABAC with classification/tenant/ACL-group attributes; query-plan for listing; audit trail. NFR: microsecond-to-millisecond decisions in process; policy tests; offline.

## 7. Performance and resource model
No benchmark fetched for either; vendor claims not collected: **UNVERIFIED**. Cedar claims "fast and scalable, bounded latency" (docs, no numbers) [CLAIM-cc-02]. Single node: Cedar in-process (negligible); Cerbos single static binary (size NOT VERIFIED). Failure modes: entity-set construction cost per request; PlanResources conditions unsupported by a target store.

## 8. Strengths
Cedar: analysable, side-effect-free semantics, forbid-overrides-permit safety. Cerbos: readable policies, PlanResources query plans (directly usable for retrieval prefilters and LangChain/Chroma adapters), audit trail, git-managed policy. Match: EOIP `authz/core.py` already has YAML statements; the gap is the plan/partial-eval output and policy analysis.

## 9. Limitations
| Class | Item |
|---|---|
| Algorithmic | neither stores relationships; nested groups resolved by caller; conditions in plans limited to the adapter's operators |
| Operational | Cerbos extra service; Cedar needs a host language binding (Rust; Python bindings status UNVERIFIED) |
| Friction | two more DSLs (Cedar; YAML+CEL) beside EOIP's own |
| Licensing/governance | Cerbos open-core split; Cedar sandbox maturity |

## 10. Deployment and licensing
Both Apache-2.0 core, self-hostable, air-gap viable. Cerbos Hub (hosted) not needed; flag open-core boundary for legal/product review (no legal conclusion). Redistribution of Cerbos binary as part of EOIP: permissible under Apache-2.0 subject to notices (confirm NOTICE).

## 11. Delta vs EOIP baseline
BL-19: `authz/core.py` `PolicyEnforcer.enforce(user, action, resource_attrs)` with `Condition.matches` is equivalent to a minimal Cerbos/Cedar PDP on API actions, no forbid-overrides ordering described, no static analysis. `authz/pdp.py` `can_read(scope, acl_vector, classification)` is ABAC-ish tag intersection (deny-by-default, tenant-gated). BL-18: a Cerbos-style plan output (condition tree) would let `retrieval` build index filters instead of post-filtering. See C19-rebac for relationship data and C19-opa for Rego.

## 12. Cards
**STR-cc-01** | Cerbos | PlanResources conditional filter AST | CLAIM-cc-04 | policy-driven pre-filter for lexical/vector/graph retrieval | match | native `plan_resources(scope, action, kind)` returning conditions over `acl_principals`, `classification`, `tenant_id` | plan-filtered results equal per-doc `can_read` on 1,000 docs.
**STR-cc-02** | Cedar | forbid-overrides-permit + analysable policies | CLAIM-cc-02 | provable "no path grants X" checks in CI | match (concept) | add explicit `forbid` statements and a policy lint that rejects unreachable/contradictory rules | injected conflicting policy fails CI.
**INV-cc-01** (no relationship storage, proven by docs) | policies need caller-resolved entities; alternative is ReBAC engine for membership + Cedar/Cerbos for attribute rules. Selected: native conditions over ReBAC output. Benchmark: 100k-doc plan latency. Decision DEFER (adopt concept, not engine). When worse: single-tenant small deployments where flat tags suffice.
**INV-cc-02** (DSL proliferation, friction/hypothesis) | do not add third DSL; extend YAML. Decision ADOPT as constraint.

## 13. Decisions
| Capability | Decision |
|---|---|
| CAP-45 policy engine | REUSE native `authz`; REFERENCE Cedar semantics |
| Query-plan output | BUILD (Cerbos pattern) |
| Cerbos as service | EXPERIMENT (optional adapter) |
| Cedar library | DEFER (Python binding unverified) |
| CAP-46 relationships | INTEGRATE ReBAC (not these) |

## 14. Tests
Differential test of plan vs per-doc evaluation; forbid-precedence tests; policy-lint test; PlanResources round-trip against a vector-store filter; offline Cerbos container.

## 15. Risks
Open-core feature drift; Cedar Python bindings; plan operators not mapping to OpenSearch/Neo4j filters.

## Appendix A — Dimensions
| Dim | Sections | Summary |
|---|---|---|
| D1 | 1,10 | owners, licences |
| D2 | 2 | app-level authz |
| D3 | 4 | lib vs PDP |
| D5 | 5 | schema vs policy |
| D6 | 5 | partial evaluation / plans |
| D13 | 3,11 | retrieval filter |
| D15-17 | 3 | policy tests (partial) |
| D18 | 5,9 | deny-by-default |
| D20 | 7 | UNVERIFIED |
| D21 | 10 | open-core |
| D23 | N/A | none found |
| D24 | App C | docs-level |
| D4,D7-D12,D14,D19,D22 | N/A | not applicable |

## Appendix B — Capabilities
| CAP | Cedar / Cerbos | CLAIM | EOIP | Decision | Pri |
|---|---|---|---|---|---|
| CAP-45 | native / native | 02,04 | BL-19 Implemented | REUSE | P2 |
| CAP-46 | absent / partial (plans) | 04 | BL-18 partial | BUILD pattern | P0 |
| CAP-48 | via host / audit log | 04 | BL-19 | REFERENCE | P2 |

## Appendix C — Evidence
| CLAIM | product | claim | class | source | dates | conf | contra |
|---|---|---|---|---|---|---|---|
| CLAIM-cc-01 | Cedar | accepted to CNCF 2025-10-08 at Sandbox; no evidence of advancement | Officially documented | https://www.cncf.io/projects/cedar/ ; https://infoq.com/news/2026/01/cedar-joins-cncf-sandbox/ | 2025-10-08 / 2026-10-26 | 0.8 | InfoQ dated 2026-01 |
| CLAIM-cc-02 | Cedar guide 4.6 | schema validates only at policy time; entities supplied per request; analysable; bounded latency; CLI v4.14.0 | Officially documented | https://docs.cedarpolicy.com/ ; https://github.com/cedar-policy/cedar/releases/latest | 17 Oct / 2026-10-26 | 0.8 | licence not on page |
| CLAIM-cc-03 | Cerbos | Apache-2.0; PDP as k8s/sidecar/systemd/Lambda; policy stores disk/object/git/SQLite; 4.6k stars | Officially documented | https://github.com/cerbos/cerbos | n/a / 2026-10-26 | 0.85 | none |
| CLAIM-cc-04 | Cerbos API | CheckResources limits 50x50; PlanResources kinds and adapters; cerbosCallId audit; Hub/Synapse separate | Officially documented | https://docs.cerbos.dev/cerbos/latest/api/index.html | n/a / 2026-10-26 | 0.85 | enterprise gating not stated |
| CLAIM-cc-05 | Cerbos v0.57.0 | latest release 23 Oct | Officially documented | https://github.com/cerbos/cerbos/releases/latest | year not shown | 0.8 | none |

## Appendix D — Assumptions
Cedar licence and Lean verification from project knowledge, flagged lower confidence. Years inferred.
