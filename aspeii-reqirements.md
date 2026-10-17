# ASPEII Requirements for EOIP / KnowGridFlow

Document: `ASPEII-REQ-1.0`. Prepared: 2026-10-17 (Asia/Calcutta).
Status: normative target specification; all ASPEII requirements initially OPEN.
Revision: 1.0.1 (2026-10-17) — section 10 (tracker integration) appended; sections 1–9 unchanged.
Baseline: `00f18804ca2c7a5d12855c4763973fdfe892deac`.
Companions: [research and evidence](aspeii-research-analysis.md), [implementation plan](aspeii-implementation-plan.md).

The filename preserves the user's requested spelling. EOIP, KGF, and KnowGridFlow name the same application in this document. ASPEII is an internal workstream name for integrating the six researched topics, not a claimed external standard.

Navigation: [completion and scope](#1-outcome-and-completion-contract), [reuse and compatibility](#2-reuse-and-ownership), [contracts](#3-shared-domain-contracts), [36 requirements](#4-requirements-catalog), [API](#5-public-interface-contract), [GUI](#6-gui-information-architecture), [qualification targets](#7-qualification-targets), [16 scenarios](#8-end-to-end-acceptance-scenarios), [release evidence](#9-evidence-required-for-every-release).

## 1. Outcome and Completion Contract

Build an integrated platform capability in which a user can define a measurable goal, delegate bounded work, inspect the evidence behind findings, approve an exact consequential action, verify its actual outcome, and improve the semantic layer through evaluated versioned changes. The implementation must work through EOIP's real API, agent runtime, persistence, worker, MCP, and GUI surfaces.

The research explains why the topics apply and where the published claims stop. The design below chooses concrete behavior. A coding agent must not substitute marketing interpretations, undocumented defaults, generated success objects, or mock-only qualification for these requirements.

### 1.1 Meaning of 100% Completion

Every numbered clause in each `ASPEII-RQ-NNN` section is a separately tracked acceptance obligation, identified as `ASPEII-RQ-NNN.C01` through `.C06`. The six clauses and the section's acceptance examples are mandatory. Shared contracts and end-to-end scenarios are also normative and must be allocated to these clauses by the implementation registry.

Completion requires all applicable clauses to have fresh PASS receipts for the exact release artifact and supported deployment/provider matrix. Status values are `OPEN`, `IN_PROGRESS`, `BLOCKED`, `FAILED`, `VERIFIED`, `STALE`, and `DEFERRED`. Only `VERIFIED` counts in the completion numerator. A waiver or deferral remains visible and prevents a claim of full completion of this version. Adding a file, referencing a symbol, marking a test, passing one unit test, or producing a screenshot alone does not establish integrated completion.

The evidence chain must bind requirement revision -> tested behavior -> build/source manifest -> configuration -> input fixture -> actual observations -> independent verifier result. Do not allow the component under test to supply its own authoritative PASS outcome. External integrations that cannot be exercised remain BLOCKED for their profile. A smaller qualified profile must be named explicitly and must not be reported as completion of every profile.

This specification cannot guarantee absence of all future defects, universal agent safety, support for every possible connector, or factual truth of every enterprise claim. It defines a finite, auditable release scope with explicit extension contracts.

### 1.2 Scope

Mandatory: intent contracts; internal human/agent delegation; typed tool outputs and claims; independent action checking; durable approvals and receipts; real MCP read integration; semantic browsing and governed evolution; CTAR integration; GUI/API/worker deployment; deterministic offline qualification and explicitly configured real-provider qualification.

Extension points are mandatory; arbitrary vendor integrations are not implicitly implemented. Initial effect qualification covers read-only EOIP graph access, reversible EOIP graph mutation, ontology publication/rollback, and one real supported connector write adapter selected from the active connector registry by the plan's selection rule. No payment, unrestricted shell, code deployment, public publication, or automatic code installation is enabled by default. Unqualified effects fail closed.

Optional research extensions are formal theorem-prover plugins, zero-knowledge proofs, public agent markets, payments/escrow, and automated executable-tool generation. Their absence does not reduce the defined core scope because they are explicitly excluded from version 1.0; they must not be advertised as delivered features.

### 1.3 Explicit Decisions and Configuration

These are engineering defaults selected for this workstream, not inferred customer requirements. They are versioned, validated configuration. A lower tenant limit wins; a tenant cannot exceed a platform limit or relax a mandatory security invariant.

| Setting | Default / allowed behavior |
| --- | --- |
| Activation | New workspaces start `READ_ONLY`; consequential actions require `ENFORCED` mode and qualified adapters |
| Model provider | Disabled until configured; local/no-egress and hosted providers implement the same contract; deterministic core works without a model |
| Persistence | SQLite WAL for one-host local installations; PostgreSQL for multi-worker/SaaS; authority data must never depend on in-memory dictionaries |
| Delegation | Maximum depth 2, total tasks 12, concurrent children 4, aggregate wall deadline 300 s, one retry for safely retryable failures |
| Task tools | 8 calls/task, 48 calls/root, maximum 100 returned graph items/call by default; explicit bounded override within platform policy |
| Model budget | 4,096 output tokens/task, 24,576 aggregate/root; provider usage includes failed calls and retries; missing usage produces conservative reservation |
| Monetary budget | No invented currency/amount; paid execution requires configured currency, cap, and price revision; otherwise blocked |
| Worker lease | 30 s lease, renew every 10 s, monotonically increasing fencing token; deadline and revocation checked before dispatch |
| Approval | 15 min maximum validity, one logical effect, exact action digest; policy can shorten, not silently extend |
| Observation freshness | Adapter/tool contract must declare TTL or immutable revision semantics; missing semantics blocks consequential use |
| List APIs | Default 50, maximum 200 items, cursor bound to tenant/filter/snapshot; unauthorized items excluded before pagination |
| Evolution | Off until enabled; at most 3 candidate rounds/run; no active-version mutation during evaluation; no arbitrary code patches |
| Paired evaluation | Frozen >=200 cases and >=50 per declared critical stratum; three repeated runs for nondeterministic agents; inadequate data -> INCONCLUSIVE |
| Promotion margin | Mean task-score improvement >=0.02 on a declared [0,1] metric, paired 95% confidence lower bound >0, no mandatory regression; thresholds frozen before candidate generation |
| Evaluation cost | Candidate token and elapsed-time means <=1.20 times parent, unless a separately approved benchmark profile defines another bound before the run |
| Candidate hard gates | Zero observed new authorization violations, evidence laundering cases, mandatory invariant failures, or schema-compatibility failures |
| Retention | Deployment must configure metadata/evidence retention and deletion policy; no unbounded default production retention |
| UI motion | Respect reduced-motion; normal transition duration 120-200 ms; no animation required to understand risk or status |

Actual tenant identities, production secrets, customer retention rules, allowed destinations, paid-provider budgets, hardware capacity, and vendor permissions cannot be invented. Missing values leave the dependent production capability unavailable while development continues against clearly labeled local fixtures.

## 2. Reuse and Ownership

The current backend entrypoint is `backend/server.py` -> `apps.api.main.create_app`. `apps/api/app.py` also contains related routes; inventory runtime route registration before editing. The current GUI is `frontend/` (React, TypeScript, Vite, TanStack Query, lucide-react). Do not implement these screens only in the separate `apps/web` tree and claim they are integrated.

| Existing ownership | Integration requirement |
| --- | --- |
| `packages/eoip/contracts/agent.py`, `contracts/tool.py` | Extend compatibly or provide explicit v2-to-new-schema adapters; unknown security fields must not disappear |
| `agents/runtime.py`, `tools.py`, `orchestration.py` | Keep one execution/admission path across new and legacy callers |
| `agents/proposals.py`, API proposal routes | Preserve inert proposals; approval is not execution |
| `provenance/trust.py`, `provenance/evidence.py`, `contracts/evidence.py` | Introduce typed support; preserve source identity and access decisions |
| `ontology/drift.py`, `gitops.py`, `stewardship.py` | Use existing review/diff concepts; transactional version publication is a prerequisite |
| `tools_contract/mcp_bridge.py`, `apps/mcp/main.py` | Reconcile external client and exposed server; real transport and policy parity required |
| `jobs.py`, `state/engine.py` | Verify persistence/concurrency behavior; neither filename establishes multi-worker durability |
| `authz/`, `authn/`, tenancy infrastructure | Principal and tenant derive from authenticated context; never trust body identity |
| `frontend/src/screens/Agents.tsx`, `Ask.tsx` | Extend current user journeys with typed responses and visible failures |
| `scripts/verify_requirement_evidence.py`, `verification/` | Preserve MVP verifier behavior; add ASPEII profile and behavioral receipts |

[Community requirements](community-ip-requirements.md) own CTAR invalidation/repair. [Graph Neurons](EOIP-engg-doc-pkg/Graph-Neurons-requirements.md) outputs remain predictions. [CRAr](CRAr.md) and [GUI requirements](GUI-UIX-requirements.md) remain applicable. An overlapping requirement reuses the same implementation and evidence where valid; do not create a second conflicting source of authority.

### 2.1 Compatibility With Concurrent IP Requirements

[ip-requirements.md](ip-requirements.md) and [its plan](ip-requirements-implementation-plan.md) appeared during preparation and define overlapping warrant engineering. Preserve their exact public schemas, IDs, configuration keys and routes. ASPEII adds scoped semantics and execution guarantees through adapters/extensions; it does not silently replace those contracts. These shared obligations allocate to ASPEII-RQ-001.C05, ASPEII-RQ-002.C04, ASPEII-RQ-014.C06 and ASPEII-RQ-030.C01, with associated admission/privacy clauses.

| Existing IP contract | ASPEII binding / required resolution |
| --- | --- |
| `Warrant` schema, `REQ-WAR-010..014` | Reuse warrant-service ownership and store a versioned reference from ClaimRecord/ActionCertificate. Preserve the legacy schema; add extensions through a new version or separate companion record, never undocumented fields |
| `OBSERVED,ATTESTED,PREDICTED,GENERATED,HEARSAY,UNKNOWN` | Retain `warrant.status` and its configured order. Map respectively to observed-source content, human assertion, model hypothesis, generated hypothesis, unverified assertion, unknown origin. Compute ASPEII support, truth and lifecycle separately; an OBSERVED source can contain an unsupported proposition |
| Operator classes including `MODEL` and `HUMAN` | Preserve original class/version. Stochastic model results are GENERATOR production with HYPOTHESIS content; a recorded human attestation is an observed attestation event with HUMAN_ASSERTION content. Do not claim that observing the attestation proves its proposition |
| SASI/NLI-based status inheritance | Retain alignment evidence and original source status where the IP contract requires it; classify model-based alignment as heuristic unless independently checked. It cannot alone discharge a factual or security obligation |
| `lease.*`, `REQ-LSE-*`, `REQ-LVC-*` | Fact-validity leases stay separate from ASPEII worker leases/fences. Action admission checks both where applicable; a 24-hour fact TTL does not extend a 30-second worker lease |
| Consequence `kappa` and `budget.*` | Keep consequence budget distinct from compute/time/money reservations. All applicable budgets must pass; a low consequence score cannot waive identity, evidence or approval |
| `READ_ONLY,ADVISORY,INTERNAL_WRITE,EXTERNAL_WRITE,IRREVERSIBLE` | Map qualified effects to R0/R1/R2/R3 according to sensitivity and destination. Unknown effects are R4 denied; the legacy conservative IRREVERSIBLE classification does not automatically qualify an unknown operation |
| Checkpoint SDK, `REQ-SDK-*` | Extend one shared checkpoint/gateway implementation. Disabling a legacy feature flag cannot bypass mandatory ASPEII admission on ASPEII-enabled effects |
| Answer checkpoint described as never blocked | Interpret this as no block solely for weak epistemic status; current privacy/authorization/egress guards still apply. If the implementation contract intends unrestricted disclosure, record the conflict and block that affected integration until resolved |
| Runtime warrant retention default 30 days | Reuse the key and supported local default; production deployment must explicitly acknowledge effective retention and deletion policy. Do not invent a second competing retention setting |
| Signed export, meaning releases and commitments | Share signer/trusted-key policy and publication service. Commitment fulfilment references verified task outcomes; a promise or dissent decision is not itself evidence of factual truth or execution |
| Dissent diversity by model family | Preserve operational diversity metrics, but evaluate evidentiary independence from source lineage too; different models reading one source are not two independent sources |

When an actual contradiction cannot be resolved by these orthogonal fields/adapters, record both clauses and a `CONFLICT-IP-NNN` decision as required by the IP plan. Pause only the affected integration, keep its status BLOCKED, and continue independent work. This is not permission to weaken either contract or to overwrite the concurrent documents.

## 3. Shared Domain Contracts

### 3.1 Common Record Rules

Use strict Pydantic models and generated JSON Schema; persisted schemas and public schemas carry explicit versions. Reject unknown fields on security-bearing write objects. Every persisted record has a UUID `id`, nonempty server-derived `tenant_id` and `workspace_id`, `schema_version`, positive integer `revision`, UTC RFC3339 `created_at`, authenticated `created_by`, and an immutable content digest. A mutable lifecycle is stored as append-only transitions referring to an immutable content revision. UUIDs are opaque identifiers, not permission grants.

References are `{kind, id, revision, digest}`. Missing revisions never mean latest in an approval, evaluation, or certificate. Human display names are not IDs. Money uses integer minor units plus ISO currency; timestamps, integer bounds, byte sizes, and units are validated. NaN, infinity, duplicate JSON keys, ambiguous encodings, and unbounded nested input are rejected. Strings preserve exact Unicode code points; canonicalization does not silently normalize them.

`dependent DEPENDS_ON input` is the only dependency direction; reverse traversal computes impact. Support alternatives are represented as OR between support sets and AND within each required set. Access authorization is checked separately from logical support. A surviving public source cannot authorize disclosure of a restricted source's hidden content.

### 3.2 Required Records

All fields below are required unless explicitly nullable or defaulted. Common fields above apply to every record. Implementation schemas must encode these rules; prose-only models do not satisfy the requirement.

| Record | Fields and constraints |
| --- | --- |
| `IntentSpec` | `objective_text` 1..8,000 chars; `objective_ref` nullable; `owner_principal`; nonempty `acceptance_predicates`; `non_goals` default []; `scope_refs`; `permitted_effects` enum set; `constraints`; `budget`; `deadline`; `policy_ref`; `unresolved_fields` default []; `lifecycle` |
| `AcceptancePredicate` | Stable `predicate_id`; allowlisted `verifier_id` and version; typed `inputs`; comparison enum `EQ,NE,LT,LE,GT,GE,CONTAINS,SET_EQ`; typed `expected`; `unit` nullable; `mandatory` boolean; `evidence_requirements`; `temporal_scope`; no executable expression string |
| `TaskContract` | `intent_ref`; `parent_task_ref` nullable; `required_capabilities`; `input_refs`; `output_schema_ref`; `acceptance_predicate_refs`; `dependency_task_refs`; `budget_reservation`; `grant_ref`; `accountable_principal`; `assignee_ref` nullable; `lease_ref` nullable; `status` |
| `CapabilityProfile` | `subject_ref`; `capability_id`; tool/model/schema versions; declared and measured capability fields separately; qualification receipts; valid-until; permitted data classes; allowed deployment modes; revocation state |
| `DelegationGrant` | `issuer`, `subject`, `audience`, parent grant nullable; exact task/intent refs; scoped actions/resources; budget ceilings; `issued_at`, `expires_at`; `max_depth`; revocation epoch; secret token hash only; grants cannot expand parent bounds |
| `ToolSemanticContract` | tool/adapter identity and versions; input/output schema refs; production class; effect class; authoritative obligation templates; reversibility; timeout; freshness; destination policy; transport; approval enforceability; independent outcome observer |
| `ClaimRecord` | Structured subject/predicate/object or bounded text plus language; epistemic kind; truth status; context and valid-time; source/support references; source origin group; derivation transform; model provenance nullable; current lifecycle; quality assessment nullable |
| `EvidenceRecord` | Source revision; acquisition method; content digest; locator; observed/recorded time; current access policy; classification; immutable/TTL semantics; origin group; redacted content reference; disposition; verifier receipts |
| `SupportSet` | Claim ref; required premise refs; inference rule/version; applicable boundary; distinct-source grouping; independent check ref nullable; result `SUPPORTED,UNSUPPORTED,CONFLICTED,UNKNOWN`; no cyclic self-foundation |
| `BeliefArtifact` | Requirement/domain claim refs; explicit boundaries; dependencies; owner; falsification specification; challenge-run refs; unresolved failure refs; revision history; release scope; decision refs |
| `ChallengeResult` | Target revision; challenge/verifier version; input digest; observed counterexample or absence within suite; severity; outcome; start/end time; raw evidence references; reproducibility metadata |
| `ActionIntent` | intent/task/grant refs; principal; tool/adapter refs; exact typed arguments; resource/destination/account identity; effect class; expected-state refs; policy ref; obligation refs; scope; deadline; logical idempotency key |
| `ActionCertificate` | Action digest; canonicalization version; verifier/version; obligation results; evidence refs; current authorization result; enforceability mode; approval receipt refs; issue/expiry time; key ID/signature; no model-generated PASS field |
| `ApprovalDecision` | Exact action digest; authenticated reviewer; decision `APPROVE,REJECT`; rationale; current permission/policy revision; decision/expiry times; separation-of-duties result; consumed/revoked state |
| `ExecutionAttempt` | Logical action ref; attempt ID; fenced worker identity; reserved budget; certificate ref; dispatch state; provider idempotency key; start/end time; observed external operation ID nullable; reconciled outcome |
| `OutcomeReceipt` | Action/attempt/certificate refs; observed status; result/artifact digests; independent postcondition results; adapter receipt; externality facts; timestamps; actual usage; audit chain refs; signature/key ID |
| `SemanticVersion` | Immutable parent nullable; scoped content/schema/tool-view digests; ontology/graph mapping refs; target model profile nullable; semantic validation refs; current publication reference held separately |
| `EvolutionCandidate` | Parent and candidate version refs; one change layer; typed patch; hypothesis; triggering trajectories; builder/grant refs; affected scope; reversibility/migration plan; frozen evaluation spec; lifecycle |
| `EvaluationRun` | Parent/candidate refs; fixed case IDs and split digests; evaluator/version; model/tool/config pins; seeds; per-case scores/outcomes/cost; failures/timeouts; statistical procedure; final gate result |
| `EvidenceBundle` | Requirement clauses; build/source/dependency/config manifests; environment; real integration modes; run IDs; raw artifacts/hashes; timestamps; test outcomes; scenario assertions; independent verification result; unresolved gaps |

### 3.3 Epistemic Semantics

Production class is `OBSERVER`, `COMPUTATION`, `GENERATOR`, or `MIXED`. It describes the operation, not truth. Claim kind is `OBSERVATION`, `DERIVED`, `HYPOTHESIS`, `HUMAN_ASSERTION`, or `NORMATIVE_CONSTRAINT`. Truth status is `SUPPORTED`, `REFUTED`, `CONFLICTED`, or `UNKNOWN` relative to a declared boundary. Lifecycle is the CTAR state `CURRENT`, `STALE`, `REVOKED`, `QUARANTINED`, `UNKNOWN`, `SUPERSEDED`, or `PURGED`. These dimensions must not collapse into a single trust number.

An observation means that a source returned specified bytes/state under a particular acquisition contract. It does not automatically mean that the source's proposition is true. Derived claims preserve premises and inference-rule scope. A hypothesis can gain independent supporting evidence, but its original generation record is immutable. Human acceptance can authorize a business decision under policy; it does not turn an unsupported factual proposition into a proven theorem.

Confidence, where used, has `value`, `meaning`, `method`, `dataset_ref`, `calibration_ref`, and applicable domain. Missing calibration means `HEURISTIC`, never an implied probability. Do not infer independence from different tool names, models, URLs, or agent IDs alone. Shared origin groups and common upstream evidence must remain visible.

### 3.4 Action Risk and Enforcement

| Class | Effects | Minimum admission |
| --- | --- | --- |
| R0 | Bounded non-sensitive read | Current authorization and read policy; no interactive approval by default |
| R1 | Sensitive read or private draft creation | Data/egress scope, audit and output restrictions; approval only if policy requires |
| R2 | Reversible in-platform mutation | Independent obligations, exact approval or preauthorized scoped policy, pre-execution gate, postcondition |
| R3 | External write, export, or irreversible change | Human approval; verified account/destination; pre-execution gate; all mandatory obligations; reconciliation plan |
| R4 | Unclassified, unsupported, or prohibited effect | Deny pending classification/qualification; cannot be downgraded by planner input |

This mapping must reconcile the existing `RiskLevel` enum without weakening stricter existing policy. Tool/adapter contracts derive risk, obligations, and reversibility. Planner requests may increase scrutiny, never reduce it. `PRE_EXECUTION_GATE`, `DELEGATED_GATE`, `OBSERVE_ONLY`, and `RUNTIME_CONTROLLED` are explicit EOIP mode names. For R2/R3, delegated gates require authenticated, fresh, contract-bound enforcement receipts and a qualified adapter. Observe-only integrations can import audit data but cannot claim prevention or satisfy approval-required execution.

### 3.5 Canonical Action and Verification Rules

Compute the action digest as SHA-256 over UTF-8 RFC 8785 canonical JSON of the complete security-bearing `ActionIntent` projection, prefixed by the literal domain separator `EOIP-ASPEII-ACTION-v1\n`. Store the algorithm/version, canonical bytes digest, and immutable object. Canonicalization follows the standard's number and Unicode rules; application schemas constrain integers to exact interoperable ranges and represent decimal domain values as typed strings or integer units. Reject unsupported values rather than serializing with Python `repr` or `default=str`. Use a qualified implementation with shared Python/TypeScript test vectors.

The projection includes exact argument values, resolved tenant/workspace, actor, task, target, account, destination, tool and adapter versions, policy, obligations, preconditions, effects, expiry, and logical idempotency key. Exclude only explicitly nonsemantic presentation fields such as localized labels. Review UI and executor must load the same immutable projection. Redaction must not erase information necessary for an authorized reviewer to understand consequences; otherwise approval is unavailable.

Self-referential fields (`digest`, signatures, receipt IDs created after admission) are not part of the action preimage. Specify the complete projection schema in code and shared test vectors: security metadata is included, display-only metadata is an explicitly disjoint object. Signatures bind the resulting digest and certificate payload under a distinct signature-domain/version. Persist one normalized UTC timestamp representation before hashing; clients review the server-resolved immutable object rather than independently guessing normalization.

Mandatory checks are deterministic predicates registered by trusted code: identity/scope, capability, budget, resource ownership, expected revision/ETag, data classification/egress, support freshness, allowed destination, schema validity, approval binding, and effect-specific postconditions. A model can propose evidence or actions but cannot register a trusted verifier, supply the obligation set, or mark its own checks passed. Failing or unknown required predicates deny execution.

Cryptographic receipts use vetted Ed25519 signing through a replaceable signer interface for export verification, with key ID and rotation/revocation metadata. Keep private keys outside model context. Existing HMAC records may be imported as legacy symmetric integrity observations; do not describe them as public third-party non-repudiation. Signature validity establishes integrity/authentication under the trust policy, not the truth of a claim or outcome.

### 3.6 State Machines

| Object | Allowed progression / terminal semantics |
| --- | --- |
| Intent | `DRAFT -> NEEDS_INPUT or VALIDATED -> ACTIVE -> SUCCEEDED/PARTIAL/FAILED/CANCELLED/EXPIRED`; clarification returns a new revision to validation; activated content immutable |
| Task | `PENDING -> READY -> LEASED -> RUNNING -> VERIFYING -> SUCCEEDED/FAILED/ABSTAINED`; may enter `BLOCKED` or `CANCEL_REQUESTED`; cancellation ends `CANCELLED` only after side-effect status is known |
| Action | `PROPOSED -> CHECKING -> DENIED or AWAITING_APPROVAL or ADMITTED -> DISPATCHING -> RECONCILING -> SUCCEEDED/FAILED/UNKNOWN_OUTCOME`; rejection/expiry/revocation before dispatch are terminal with zero new effects |
| Candidate | `DRAFT -> VALIDATING -> EVALUATING -> REJECTED/INCONCLUSIVE/ACCEPTED -> APPROVED -> PUBLISHING -> PUBLISHED`; stale parent -> `CONFLICT`; immutable rejection reasons retained |
| Challenge | `QUEUED -> RUNNING -> PASSED_WITHIN_SCOPE/FAILED/INCONCLUSIVE/CANCELLED`; timeout is never PASS |

All transitions validate expected revision and current authority. Illegal transitions return a conflict without partial mutation. Cancellation, approval revocation, retries, rollback, and external reconciliation have their own recorded events; they do not rewrite history. An unknown external outcome must not be retried blindly or labeled failed simply because the network timed out.

## 4. Requirements Catalog

Each section has six normative clauses. Acceptance examples supplement, rather than replace, the clauses. Implementation work packages in the companion plan cover every ID.

### ASPEII-RQ-001: Baseline, Scope, and Decision Ledger

Priority P0. Dependencies: none.

1. Capture current commit, dirty-file hashes, runtime entrypoints, supported configurations, actual registered routes, and feature flags before implementation.
2. Reproduce AS-G01, AS-G02, and AS-G03 safely and preserve raw outputs; inventory other research gaps as source observations pending verification.
3. Create a clause registry containing every normative requirement, shared-contract allocation, scenario mapping, owner, dependency, status, and missing evidence.
4. Record each changed design default, rejected alternative, migration implication, and acceptance revision in a decision ledger.
5. Preserve concurrent user changes and existing requirement identities; reconcile overlapping CTAR, CRAr, Graph Neurons, and GUI contracts explicitly.
6. Report unsupported integrations and unresolved customer configuration as BLOCKED scoped items; never invent credentials, authorities, licenses, or passing results.

Acceptance: a clean checkout and a dirty checkout produce distinguishable manifests; deletion of one clause or an unknown requirement reference fails registry validation.

### ASPEII-RQ-002: Versioned Shared Contracts

Priority P0. Dependencies: 001.

1. Implement all records and enums in section 3 with strict validation and machine-readable schemas.
2. Generate frontend types from the public contract and validate Python/TypeScript serialization equivalence on canonical vectors.
3. Reject missing identity, malformed references, unknown security fields, unsupported schema versions, invalid numerics, and over-limit input before persistence.
4. Implement explicit legacy agent/tool/proposal adapters; preserve original provenance and flag unmapped assurance as UNKNOWN.
5. Give errors stable codes, sanitized details, a correlation ID, and machine-readable retryability without revealing hidden resource existence.
6. Add schema upgrade/downstream compatibility fixtures and documented removal rules; no silent coercion of ambiguous legacy values.

Acceptance: a v2 request adapts without fabricating approval; a client-supplied tenant or risk downgrade cannot override trusted context.

### ASPEII-RQ-003: Durable Authority and Transactions

Priority P0. Dependencies: 002.

1. Persist intent/task/action/grant/approval/receipt/evaluation/version records in a transactional repository; implement SQLite local and PostgreSQL multi-worker adapters.
2. Atomically update authoritative transitions, budget reservations, and outbox events; use compare-and-swap revisions and unique logical-effect keys.
3. Implement durable leases with fencing and expiry; workers must present the current fence when dispatching or publishing.
4. Project records to the graph asynchronously with idempotent event IDs, visible projection watermark, and rebuild support.
5. Preserve committed data across restart and recover interrupted transitions without manufacturing terminal success.
6. Supply migrations, backup/restore, corruption detection, and rollback compatibility; qualify each storage profile separately.

Acceptance: two workers race on one action and only one acquires dispatch authority; process termination after commit/before projection loses no decision and projection resumes.

### ASPEII-RQ-004: Identity, Tenant, and Permission Boundaries

Priority P0. Dependencies: 002, 003.

1. Resolve principal, tenant, workspace, roles, and service identity from authenticated context for every operation and event consumer.
2. Enforce object/action-level authorization on lists, details, approval, execution, graph paths, evidence downloads, exports, MCP, and historical views.
3. Recheck current permissions at read, admission, dispatch, and evidence retrieval; cached grants cannot survive revocation.
4. Separate proposer, approver, verifier, publisher, and operator permissions; enforce no self-approval for R3 and configured R2 policies.
5. Minimize delegated context and credential exposure; agents receive scoped handles rather than reusable secrets.
6. Return indistinguishable unauthorized/missing object responses where appropriate; no tenant leakage via counts, cursor contents, events, errors, or caches.

Acceptance: two tenants with matching display names cannot see or approve each other's records; forged body `actor_id` is rejected or ignored in favor of authenticated identity.

### ASPEII-RQ-005: Intent Capture and Revision

Priority P1. Dependencies: 002, 004.

1. Provide GUI/API creation of structured intent with all fields in section 3 and links to existing BusinessObjective/BusinessCapability objects.
2. Record ambiguous or absent required values as explicit unresolved fields; allow saving drafts but prevent activation until resolved.
3. Support non-goals, effect boundaries, per-scope data constraints, measurable acceptance predicates, aggregate budgets, and deadline.
4. Let an LLM draft a candidate interpretation; require deterministic validation and authorized acceptance of consequential scope.
5. Version edits immutably and show the changed goal/constraints; invalidate dependent actions when relevant intent fields change.
6. Distinguish user outcome satisfaction from execution status; report partial fulfillment and unavailable measurements visibly.

Acceptance: 'investigate incident without changing systems' allows evidence reads and blocks remediation writes; removing the only measurable predicate prevents activation.

### ASPEII-RQ-006: Intent Compilation and Outcome Verification

Priority P1. Dependencies: 005, 013, 019.

1. Compile accepted intents into typed task contracts using an allowlisted planning interface, preserving all parent constraints.
2. Validate the task graph for missing dependencies, cycles, scope expansion, incompatible outputs, and aggregate budget overflow.
3. Allocate every mandatory acceptance predicate to an independent verifier and concrete observation source.
4. For deterministic predicates, execute the registered verifier; for subjective acceptance, obtain an authorized human decision under an explicit rubric.
5. Prevent the planner from editing goal thresholds, expected results, or evaluator implementations to make its own output pass.
6. Compute intent outcome from predicate results and required tasks; unknown or skipped predicates cannot yield SUCCEEDED.

Acceptance: all children returning SUCCEEDED while a required runtime postcondition fails results in FAILED/PARTIAL intent, with the failed predicate visible.

### ASPEII-RQ-007: Delegated Task Contracts

Priority P1. Dependencies: 002, 004, 005.

1. Create immutable task assignments with accountable owner, scoped inputs, output schema, verifier, grants, and resource reservation.
2. Support human-to-agent, agent-to-agent, and agent-to-human task edges with explicit assignment acceptance/decline.
3. Enforce acyclic dependencies and bounded parent depth; root accounting includes grandchildren and retries.
4. Preserve parent intent and grant lineage through every handoff; omitted constraints are a validation failure.
5. Support blocked, abstained, declined, timed-out, and cancelled outcomes without presenting them as successful delegation.
6. Record observable handoff context and result artifacts, excluding private chain-of-thought and unnecessary source payload.

Acceptance: a child cannot outsource a disallowed export to a grandchild; a human can decline without the workflow fabricating a replacement approval.

### ASPEII-RQ-008: Qualified Capabilities and Assignment

Priority P1. Dependencies: 007, 035.

1. Separate advertised capabilities from measured qualification by task type, tool/model version, deployment, and data class.
2. Select only currently authorized and qualified candidates meeting hard constraints; missing candidates yield BLOCKED.
3. Use a deterministic documented ranking of eligible candidates based on fit, measured quality, remaining capacity, and configured cost/latency priorities.
4. Record selection factors and rejected alternatives without claiming a heuristic rank is a calibrated success probability.
5. Expire capability evidence after relevant model/tool/policy changes; require requalification before consequential work resumes.
6. Keep external identities isolated by provider and tenant; no reputation pooling across tenants without explicit governed aggregate policy.

Acceptance: a stale high-scoring candidate loses eligibility to a freshly qualified candidate; an advertised unsupported tool never becomes executable by ranking alone.

### ASPEII-RQ-009: Attenuated Grants, Budgets, and Revocation

Priority P0. Dependencies: 003, 004, 007.

1. Issue scoped opaque grants whose effective permissions and resource ceilings are the intersection of parent, actor, tool, and current policy.
2. Bind grant to audience, task, tenant, expiry, parent, and revocation epoch; verify all ancestors before consequential dispatch.
3. Reserve aggregate tokens, tool calls, wall time, and configured money atomically before work; settle actual use and conservatively handle unknown cost.
4. Enforce monotonic attenuation across child depth and prohibit alias, retry, or fan-out paths from multiplying authority or budget.
5. Implement root/branch revocation and operator kill switches checked at dispatch independently of asynchronous event delivery.
6. Record denied, expired, exhausted, and revoked grants with sanitized receipts; never log raw bearer secrets.

Acceptance: simultaneous children cannot exceed a root's final available budget; revoking the parent prevents an already queued child action.

### ASPEII-RQ-010: Recoverable Scheduling and Reassignment

Priority P1. Dependencies: 003, 007, 009, 021.

1. Schedule ready tasks with concurrency limits, deadlines, heartbeat leases, and fairness across tenants.
2. Reassign only after fencing the prior worker and reconciling any possibly dispatched effect.
3. Classify retryable failures using adapter contracts; non-idempotent or unknown-outcome effects enter reconciliation.
4. Permit bounded re-planning after a failure through a new plan revision preserving frozen root acceptance and remaining budget.
5. Support cancellation requests and progress events; cancellation acknowledges actual cessation or reports outstanding reconciliation.
6. Prevent oscillating reassignment with attempt limits and recorded backoff; exhausted tasks end visibly incomplete.

Acceptance: pause worker A, expire its lease, dispatch worker B, resume A; A cannot execute or publish with its old fence.

### ASPEII-RQ-011: Human Control and Review Ergonomics

Priority P1. Dependencies: 004, 007, 020.

1. Provide a review queue with ownership, urgency, exact action, affected objects, uncertainty, and independent evidence.
2. Present explicit approve/reject/request-change/defer commands where valid; no preselected or timed-out approval.
3. Route unanswered reviews to configured escalation or expiry; never infer consent from silence.
4. Show which system can actually stop the effect and distinguish observed external actions from pending controllable actions.
5. Make reviewer workload, aged tasks, and pending irreversible operations visible without exposing private cross-tenant activity.
6. Preserve the reviewer's rationale and exact reviewed revision, with accessible keyboard navigation and audit export.

Acceptance: altering a destination after a reviewer opened the screen disables acceptance of the old digest and displays a conflict; expired review cannot dispatch.

### ASPEII-RQ-012: Typed Tool Results and Registry Reconciliation

Priority P0. Dependencies: 002, 004.

1. Register production class, effect, authoritative risk/obligations, transport, freshness, and output schema for every reachable tool.
2. Reconcile the agent tool registry and tool-contract engine through one qualification record; duplicated names cannot bypass policy.
3. Produce structured result envelopes containing content provenance, source revisions, claim refs, actual execution status, and supported assurance mode.
4. Preserve generator origin when a model output is wrapped in HTTP, MCP, a database row, an expert tool, or another agent.
5. For mixed tools, label each output field/claim's origin and reject untyped security-relevant subresults.
6. Treat schema validity as format verification only; qualification requires real execution and independently checked outputs.

Acceptance: an 'expert' MCP tool returning model text remains GENERATOR/HYPOTHESIS even when transport authentication and JSON Schema validation pass.

### ASPEII-RQ-013: Claim and Evidence Registry

Priority P0. Dependencies: 002, 003, 004, 012.

1. Persist scoped claim/evidence records with separate epistemic kind, truth status, lifecycle, acquisition provenance, and valid-time.
2. Resolve every evidence reference to accessible immutable content or a recorded unavailable/retracted state; arbitrary strings are not verified evidence.
3. Support field/row/document-span/page/timecode locators with original media digest and extraction/version history.
4. Track independent origin groups and deduplicate mirrored, copied, cached, or model-rephrased evidence.
5. Preserve contradictions and alternate interpretations instead of overwriting one claim with a higher confidence value.
6. Enforce retention/deletion/classification on raw evidence and derivatives; store only authorized redacted references in receipts.

Acceptance: two URLs mirroring one source count as one origin; an OCR transcription retains the image/page reference and extraction uncertainty.

### ASPEII-RQ-014: Warrant Checking and Anti-Laundering

Priority P0. Dependencies: 013.

1. Evaluate support sets under explicit rules and boundaries; require a grounded acyclic support path for claims used in consequential obligations.
2. Reject self-support and cycles whose only leaves are generated claims, including cycles distributed across agents or caches.
3. Preserve provenance and support limits through aggregation, summaries, embeddings, RAG, memory, and graph projection.
4. Allow independent observations to support a hypothesis through a new verification event; do not rewrite its original production class.
5. Label LLM judges, model confidence, citation counts, and signatures as their actual evidence types; none alone establishes factual support.
6. Replace confidence-only and string-only trust promotion; legacy `CERTIFIED` labels require an explicit scoped verification record to be used as certified evidence.

Acceptance: a fabricated statement routed through generator -> database -> search -> critic cannot become supported merely through this round trip; a genuine independent source can change its support result.

### ASPEII-RQ-015: Temporal Validity and Read-Time Decisions

Priority P0. Dependencies: 004, 013, 014.

1. Enforce valid-time, source revision, observation TTL, policy revision, and CTAR lifecycle whenever claims are retrieved or used in an action.
2. Preserve historical knowledge state while applying current access permissions to historical reads.
3. Mark missing dependency history UNKNOWN and fail closed for consequential use; expose incomplete evidence honestly in read-only exploration.
4. Recompute support from surviving independent support sets after a source correction/retraction without leaking revoked content.
5. Invalidate affected caches by source/policy/ontology/model revision and provide bounded rebuild status.
6. Keep lifecycle transitions attributable and reversible only through authorized new evidence/repair, not a confidence increment.

Acceptance: revoke a source before the repair worker runs; dependent action admission and unauthorized retrieval immediately fail, while independently supported authorized content remains available.

### ASPEII-RQ-016: Epistemic Artifact and Requirement Lifecycle

Priority P1. Dependencies: 013, 014.

1. Represent requirements, architectural decisions, domain hypotheses, and operating assumptions as distinct artifact kinds with explicit boundaries.
2. Link atomic propositions to dependency and falsification records, preserving original wording and revision.
3. Support draft, accepted-for-scope, challenged, revised, and superseded decisions without equating acceptance with empirical verification.
4. Show exact unsupported dependencies and conflicts; heuristic confidence is descriptive and cannot close a requirement.
5. Import existing requirement IDs through a structured parser and preserve overlapping source documents without destructive renumbering.
6. Record scope reductions and waived claims separately from passed acceptance; maintain the original completion denominator.

Acceptance: linking a test filename does not mark its claim verified; superseding a failed requirement produces a visible scope decision rather than erasing failure history.

### ASPEII-RQ-017: Challenges, Contradictions, and Repair Proposals

Priority P1. Dependencies: 016, 019.

1. Register deterministic challenge functions for missing boundaries, missing evidence, unsupported premises, stale support, and structured contradictions.
2. Treat natural-language contradiction detection as a proposal requiring structured confirmation or human adjudication.
3. Record counterexamples, challenge versions, execution outcomes, severity, and exact target revisions.
4. Generate bounded repair proposals with before/after claims, affected dependents, and revalidation obligations; never self-approve repairs.
5. Bound challenge iterations and resources; report no-new-failures only for the executed suite and scope.
6. Prevent evaluation or requirement changes from being used to retroactively pass a previously failed run.

Acceptance: contradictory structured constraints fail deterministically; an inconclusive model critique remains INCONCLUSIVE; a loop hitting its budget cannot report convergence.

### ASPEII-RQ-018: Canonical Action Identity

Priority P0. Dependencies: 002, 012.

1. Implement the complete canonical projection and digest rules in section 3.5 using a qualified canonical JSON implementation.
2. Bind resolved identity, account, destination, arguments, tool/adapter/policy versions, obligations, pre-state, grant, and expiry.
3. Test cross-language equivalence, nested-key ordering, Unicode, null/absent distinctions, exact numeric bounds, arrays, and invalid JSON values.
4. Create a new digest for any material change; do not reuse approvals across wrappers, retries with changed effects, or normalized arguments unless equivalence is proven by the contract.
5. Store immutable canonical payloads behind authorized reads and display their digest in review/audit details.
6. Reject unknown canonicalization versions and parsing discrepancies; never fall back to unstable string representations.

Acceptance: changing account, tenant, nested argument, or destination changes identity; reordering JSON object keys alone does not; array order remains significant.

### ASPEII-RQ-019: Independent Obligation Checker

Priority P0. Dependencies: 004, 012, 014, 015, 018.

1. Derive obligations from trusted tool contracts and current policy, never from the planner's requested subset.
2. Check each required predicate against current scoped evidence and pre-state using a registered versioned verifier.
3. Return per-obligation PASS/FAIL/UNKNOWN plus evidence, rule, boundary, and reason; unknown mandatory predicates deny.
4. Keep the checker independent of planner generation and prevent it from modifying source facts, policy, or evaluation expectations.
5. Explicitly model the trusted base, including adapters, clocks, identity, state reads, verifier code, and key material; publish limitations in qualification records.
6. Support optional formal checker plugins only with bounded proof language, trusted-axiom manifest, timeout and independent proof replay; unsupported proofs remain unusable.

Acceptance: omitted precondition, contradictory premises, risk downgrade, stale state, or forged verifier output prevents the actual adapter call, regardless of persuasive model text.

### ASPEII-RQ-020: Approval Binding and Admission

Priority P0. Dependencies: 003, 004, 018, 019.

1. Record review decisions bound to the exact action digest, approver identity/permission, policy revision, expiry, and separation-of-duties result.
2. Resolve approval IDs server-side and reject nonexistent, cross-tenant, expired, revoked, already-consumed, or mismatched decisions.
3. Atomically reserve admission for a logical effect and issue a certificate only after all required obligations and approvals pass.
4. Distinguish human approval from scoped standing policy authority; show the actual authority in receipts and UI.
5. Recheck state and authority immediately before dispatch; changed preconditions require renewed checking and, where action identity changes, new approval.
6. Reject observer-only approval-required execution and preserve all denials/expirations as auditable outcomes.

Acceptance: `approval_id='nonexistent-approval'` cannot trigger even an in-memory effect handler; one genuine approval cannot authorize a second logical action.

### ASPEII-RQ-021: Execution Gateway and Reconciliation

Priority P0. Dependencies: 003, 009, 020.

1. Route all consequential paths through one gateway, including API, workers, MCP, retries, scheduled loops, legacy tools, and ontology publication.
2. Enforce certificate freshness, action digest, worker fence, current grants, and risk-specific dispatch conditions at the last controllable boundary.
3. Use provider idempotency and conditional updates where supported; persist attempt state before dispatch and observed external IDs afterward.
4. On uncertain external result, enter UNKNOWN_OUTCOME, reconcile through an independent read/status endpoint, and forbid blind resubmission.
5. Verify postconditions independently before declaring success; distinguish accepted, dispatched, observed effect, and verified outcome.
6. Implement rollback/compensation only for qualified effects; compensation is a new governed action and cannot erase an external effect's history.

Acceptance: timeout after remote commit does not duplicate a write; HTTP 200 with unmet postcondition is not SUCCEEDED; restart resumes reconciliation.

### ASPEII-RQ-022: Integrity, Receipts, and Offline Verification

Priority P0. Dependencies: 003, 018, 020, 021.

1. Persist certificates, approvals, attempts, denial outcomes, and closure receipts with complete digest bindings and ordered audit events.
2. Use managed or protected private keys, key IDs, rotation/revocation, signed checkpoints, and authenticated export manifests; no default production signing secret.
3. Provide offline verification of payload hashes, signatures, chain continuity, schema versions, and record bindings with a supplied trusted-key set.
4. Label integrity/authenticity/authorization/obligation/outcome results separately; verification of one must not imply the others.
5. Detect deletion, truncation, reordering, replacement, and stale checkpoint attacks to the declared assurance level; a local hash chain alone cannot detect total-history replacement without a trusted anchor.
6. Export privacy-filtered bundles with redaction manifests and access checks; missing protected payload may produce LIMITED_VERIFICATION, never fabricated full verification.

Acceptance: modify an action, outcome, metadata field, or predecessor link and verification fails; a valid signature on an unsupported claim does not pass factual checking.

### ASPEII-RQ-023: Real MCP and Runtime Adapters

Priority P0. Dependencies: 004, 012, 020, 021, 022.

1. Implement actual MCP initialization, capability negotiation, tool discovery, invocation, error handling, and disconnect behavior for supported transports.
2. Qualify stdio and HTTP transports separately; use explicit process/server allowlists, authenticated sessions, audience checks, network/egress policy, and bounded responses.
3. Remove or clearly isolate synthetic successful external calls from production paths; unavailable servers report unavailable, never connected/success.
4. Pin discovered tool schemas and implementation identity; changes invalidate dependent grants, certificates, and qualification as specified by policy.
5. Classify adapter enforcement mode and demonstrate it; imported after-the-fact logs cannot become pre-execution approvals.
6. Keep caller permissions and result provenance across EOIP MCP server and external MCP client, including malicious tool descriptions and nested calls.

Acceptance: an unreachable `.invalid` server fails connection/invocation; an actual local MCP server's independently observed call log matches the receipt; changed schema prevents reuse of old approval.

### ASPEII-RQ-024: Semantic Views and Browse/Resolve

Priority P1. Dependencies: 013, 015, 023.

1. Expose typed terms, mappings, constraints, evidence, and relationships as versioned views over EOIP ontology/graph records.
2. Provide bounded semantic browse and resolve APIs/MCP tools returning IDs, revisions, source locators, ambiguity, support state, and access-filtered related objects.
3. Return a compact session manifest with version/capabilities and no hidden tenant data; load detail on demand.
4. Keep source schema, business ontology, agent content view, and executable-tool catalog distinct with explicit mappings.
5. Preserve ambiguous mappings and unsupported vocabulary as reviewable records; never invent a fallback relation merely to connect nodes.
6. Pin a semantic snapshot per task while checking current permissions; report version changes and incomplete/truncated retrieval.

Acceptance: two ambiguous terms produce alternatives, not an invented unique mapping; a hidden linked record cannot leak through resolve counts, labels, or paths.

### ASPEII-RQ-025: Evidence-Grounded Semantic Builder

Priority P1. Dependencies: 019, 024.

1. Generate initial semantic proposals from authorized source metadata and approved workload examples using a pluggable builder.
2. Use read-only bounded probes against actual source revisions; record query, schema, sample limitations, and result digests.
3. Treat labels, mappings, units, join paths, and business constraints as separate claims with supporting evidence.
4. Keep unsupported proposals quarantined; require domain-owner acceptance for semantic business rules that data profiling cannot establish.
5. Validate candidates through existing ontology/schema tooling and action governance before initial publication, including version zero.
6. Support deterministic/manual authoring without a model and disclose provider/model/usage for AI-assisted proposals.

Acceptance: plausible but nonexistent database columns fail grounding; a statistically common pattern does not automatically become a mandatory business constraint.

### ASPEII-RQ-026: Trajectory Capture and Attribution

Priority P1. Dependencies: 007, 013, 021, 024.

1. Capture authorized tool-level trajectories with task, semantic version, model/tool configuration, result claims, observations, failures, and outcome predicates.
2. Redact secrets and sensitive payloads; exclude private chain-of-thought while retaining reproducible inputs permitted by policy.
3. Attribute recurring failures to content, schema, tool exposure, source quality, permissions, model behavior, or infrastructure as explicit hypotheses.
4. Separate observations from inferred causes and support human correction of attribution through a new record.
5. Freeze selected trajectories before an evolution run; track origin groups and exclude test/validation feedback from construction input.
6. Support incremental ingestion, duplicate detection, missing trajectory disclosure, and CTAR invalidation on source correction.

Acceptance: a permission-denied source access is not automatically repaired by widening ontology/tool access; a repeated trace is counted once.

### ASPEII-RQ-027: Isolated Evolution Candidates

Priority P1. Dependencies: 025, 026.

1. Create immutable candidates against exact parents with a single declared change layer and a falsifiable improvement hypothesis.
2. Limit content/schema patches to typed operations; tool-layer patches may only configure already reviewed tool implementations within existing permissions.
3. Prevent candidates from modifying policies, grants, trusted verifiers, benchmark labels, evaluation splits, approval requirements, or active versions.
4. Validate structural consistency, scope, licensing of imported artifacts, migration effects, and reversibility before evaluation.
5. Execute candidates in isolated storage/source snapshots with denied production egress and no side effects beyond the evaluation sandbox.
6. Bound rounds/resources and persist rejection/inconclusive reasons; no synthetic passing candidate when search budget expires.

Acceptance: a patch adding an arbitrary Python tool or disabling a failed check is rejected; evaluating a candidate leaves the published semantic digest unchanged.

### ASPEII-RQ-028: Paired Evaluation and Promotion Gate

Priority P1. Dependencies: 027, 035.

1. Freeze parent, candidate, tasks, datasets, evaluator, model/tool versions, seeds, decoding, interaction budgets, and thresholds before comparison.
2. Separate construction, validation, and final qualification data; use origin/time-aware splits and prevent labels or evaluation feedback leaking to builders.
3. Evaluate identical paired tasks with comparable resource budgets and retain all cases, including timeout/error/abstention outcomes.
4. Apply section 1.3 thresholds, paired uncertainty estimates, critical-stratum checks, and hard security/schema gates; insufficient evidence is INCONCLUSIVE.
5. Use model judges only as advisory scores unless independently adjudicated to the required task rubric; no safety or factual-support gate may rely solely on a generator.
6. Qualify each target model/domain profile independently and rotate/refresh validation reserves to limit repeated-search overfitting; final qualification data remains untouched until candidate selection ends.

Acceptance: a mean gain hiding a critical-domain regression fails; changing the evaluator after seeing scores invalidates the run; an interrupted comparison cannot publish.

### ASPEII-RQ-029: Atomic Publication and Rollback

Priority P0. Dependencies: 020, 021, 028, 030.

1. Publish only an accepted, approved, fully validated candidate whose parent still matches the active version.
2. Atomically commit publication reference, lineage, migration state, and outbox event; never overwrite a published snapshot.
3. Support progressive read-only exposure by configured workspace/model profile with observable error and rollback thresholds.
4. Revalidate affected mappings, queries, agent contracts, action obligations, and cached artifacts before allowing consequential use.
5. Roll back through a new governed version-selection event with compatibility checks; do not erase prior versions or imply external effects were undone.
6. Recover partial publication after restart using persisted intent and transactional state; prevent two candidates from both winning the same parent revision.

Acceptance: two accepted candidates race; one publishes and one receives CONFLICT; rollback restores the correct semantic view and triggers derivative invalidation.

### ASPEII-RQ-030: CTAR and Neural-Output Integration

Priority P0. Dependencies: 003, 013, 015.

1. Add explicit CTAR artifact mappings for intent/task/grant/tool contract/claim/certificate/receipt/semantic candidate/evaluation/version records.
2. Capture dependency revisions for prompts, models, sources, policies, ontologies, evaluators, and tool schemas without copying private payloads.
3. On a relevant change, invalidate action admission immediately and schedule bounded downstream repair using the existing CTAR direction and lifecycle.
4. Treat neural predictions and similarity scores as hypotheses with model provenance; existing verified graph facts remain separately represented.
5. Preserve independently supported authorized alternatives and distinguish corrected information from revoked authorization.
6. Integrate with AMRB scenarios and explicitly reconcile external effects; no automatic historical action reversal.

Acceptance: a model update invalidates qualification for its predictions without erasing source observations; source revocation blocks a pending certificate before background repair completes.

### ASPEII-RQ-031: API, Events, CLI, and Public Contracts

Priority P1. Dependencies: 002, 004, 006, 010, 022, 029.

1. Implement section 5 endpoints through the active app factory and publish validated OpenAPI schemas with typed request/response examples.
2. Apply authorization, cursor pagination, idempotency, expected revisions, rate limits, and sanitized error contracts consistently.
3. Expose durable progress/audit events with resumable cursor, sequence, tenant filtering, replay bounds, and explicit gap detection.
4. Provide CLI operations for inspection, verification, evaluation, and authorized workflow submission; CLI uses the same services and never bypasses admission.
5. Maintain backward-compatible read adapters and explicit deprecation errors for unsafe legacy mutation routes.
6. Run contract tests against real HTTP/MCP transport and packaged CLI, including reverse-proxy deployment and offline evidence verification.

Acceptance: duplicate idempotent submission returns the original logical operation; same key with different payload returns 409; API and CLI cannot disagree on approval validity.

### ASPEII-RQ-032: Integrated Operational GUI

Priority P1. Dependencies: 011, 024, 031.

1. Extend the existing frontend with Intent workspace, Run detail, Evidence inspector, Action review, Evolution comparison, and Assurance views described in section 6.
2. Use generated types, authenticated tenant-aware query keys, current API field names, and explicit loading/empty/error/denied/stale/conflict states.
3. Display consequences, destination/account, exact revision, evidence limits, enforcement mode, and actual outcome before presenting approval or success.
4. Use accessible native controls and existing lucide icons, visible focus, keyboard operation, reduced-motion support, and responsive unclipped layouts.
5. Preserve navigation and query state, cancel/refresh safely, prevent duplicate submission, and show mutation failures instead of swallowing errors.
6. Demonstrate full user journeys in a real browser against the real API, including two tenants, revocation, stale review, worker restart, and mobile layout.

Acceptance: approve/reject uses `proposal_id` or the explicitly versioned new DTO ID; a failed mutation remains visibly failed; no mocked network response can satisfy GUI integration qualification.

### ASPEII-RQ-033: Operations, Deployment, and Recovery

Priority P1. Dependencies: 003, 009, 022, 031.

1. Package local/customer-installed and SaaS profiles with explicit storage, key, model, egress, backup, migration, and adapter configuration.
2. Expose metrics for queue age, leases, denied actions, unknown outcomes, support invalidation, evaluator failures, and projection lag without high-cardinality secrets.
3. Provide health/readiness checks that distinguish connected dependencies from synthetic/demo state; unavailable required authority storage fails readiness.
4. Document and exercise key rotation, source revocation, checker outage, storage outage, unknown external outcome, failed publish, and restore runbooks.
5. Measure section 7 performance targets on declared hardware; quotas and admission must remain correct under load/backpressure.
6. Restore backup into an isolated environment and verify authority/evidence consistency before reopening execution; restored consumed approvals must not become reusable.

Acceptance: loss of verifier/storage blocks consequential dispatch; restoration preserves consumed action identity and denies duplicate execution.

### ASPEII-RQ-034: Adversarial and Supply-Chain Boundaries

Priority P0. Dependencies: 004, 012, 019, 023, 027.

1. Treat retrieved text, documents, media transcripts, tool descriptions, and external agent messages as untrusted data rather than policy instructions.
2. Defend adapters against SSRF, token forwarding, confused-deputy access, schema substitution, oversize payloads, subprocess injection, and unauthorized egress.
3. Verify pinned third-party artifacts, licenses, transitive dependencies, hashes, and model/data usage terms before incorporation; preserve EOIP commercial ownership boundaries.
4. Ensure builders/evaluators cannot modify each other's inputs, hidden labels, execution gateway, or signing keys through shared volumes or credentials.
5. Exercise cross-tenant, replay, race, revocation, stale-state, poisoned-knowledge, colluding-agent, and fake-receipt attacks at real boundaries.
6. Document residual threats and control scope; neither signing nor a finite red-team suite supports a universal safety claim.

Acceptance: a source instructing the agent to disable approvals has no effect on admission; a malicious MCP redirect cannot reuse a token for a different audience.

### ASPEII-RQ-035: Independent Behavioral Qualification

Priority P0. Dependencies: 001, 002.

1. Build deterministic fixtures and independent expected results for section 8 scenarios, with source provenance and immutable fixture digests.
2. Separate unit, API, worker, storage, real-adapter, browser, adversarial, recovery, and performance outcomes; each applicable layer is required.
3. Verify absence of forbidden effects through independent adapter/server/store observations, not the action service's self-reported DENIED result alone.
4. Include deliberate negative controls that would pass a stub, such as fake approval IDs, fabricated external success, constant evaluators, and confidence-only certification; the harness must catch them.
5. Capture raw outputs, seeds, per-case results, source/build/config/dependency hashes, timestamps, integration modes, and known limitations.
6. Repeat only as justified by nondeterminism or changed artifacts; mark mismatched/stale/skipped/flaky/inconclusive evidence non-PASS and retain earlier failures.

Acceptance: replacing a real adapter with a success-returning stub makes qualification fail; changing a covered implementation file invalidates its previous receipt.

### ASPEII-RQ-036: Release Evidence and Honest Completion

Priority P0. Dependencies: 001, 031, 032, 033, 034, 035.

1. Implement a scope-aware evidence verifier covering all 216 numbered clauses plus allocated shared contracts and scenario obligations.
2. Require the actual deployable build, supported profiles, migrations, API/UI integration, operational restore, and real adapter evidence for release qualification.
3. Publish exact completion numerator/denominator, per-profile matrix, remaining gaps, and verifier version; do not average security failures away.
4. Fail release verification on missing artifacts, mismatched hashes, unresolved mandatory failures, orphaned clauses, unqualified adapters, or stale receipts.
5. Update operator/developer/user documentation to actual measured behavior and retain source provenance/licensing notices for imported artifacts.
6. Provide a fresh-agent handoff containing exact next steps for every incomplete clause; only declare 100% for this frozen scope when every required check is VERIFIED.

Acceptance: 215/216 verified clauses is not 100%; a perfectly formatted plan or a directory full of tests produces no implementation completion credit without qualifying observations.

## 5. Public Interface Contract

These are proposed interfaces to implement, not claims that endpoints currently exist. All paths begin `/api/v1/aspeii`. Route registration must be checked for collision. Public writes reject caller-supplied identity fields. Authenticated actor and tenant are injected by the server. New records return 201, durable asynchronous work returns 202 with operation ID/location, reads return 200; there is no success response before durable acceptance.

| Method and path | Request / behavior | Permission |
| --- | --- | --- |
| POST `/intents` | Draft IntentSpec content; server assigns identity | `intent:create` |
| GET `/intents` and `/intents/{id}` | Scoped cursor list or authorized detail/revision | `intent:read` |
| PATCH `/intents/{id}` | Typed revision patch plus `If-Match`; no active in-place mutation | `intent:edit` |
| POST `/intents/{id}/validate` | Exact revision; unresolved fields and predicate allocation result | `intent:edit` |
| POST `/intents/{id}/activate` | Exact validated revision and idempotency key | `intent:execute` |
| POST `/intents/{id}/cancel` | Cancellation reason, expected revision | `intent:cancel` |
| GET `/tasks/{id}` | Contract, safe progress, lease state, verification and child refs | `task:read` |
| POST `/tasks/{id}/responses` | Human task accept/decline/result with expected revision | `task:respond` |
| GET `/claims/{id}` and `/claims/{id}/support` | Typed claim and caller-filtered support DAG | `evidence:read` |
| POST `/claims/{id}/challenges` | Registered challenge ID/version and bounded input refs | `claim:challenge` |
| GET `/actions/{id}` | Canonical review projection, risk, enforcement, obligations | `action:read` |
| POST `/actions/{id}/decisions` | Action digest, APPROVE/REJECT, rationale, expected revision | `action:approve` |
| POST `/actions/{id}/execute` | Exact admitted action ref, idempotency key; cannot change args | `action:execute` |
| GET `/actions/{id}/receipts` | Approval/attempt/outcome records; no secrets | `audit:read` |
| POST `/receipts/verify` | Bounded authorized bundle ref, trust profile; no arbitrary file path | `audit:verify` |
| GET `/semantics/manifest` | Snapshot/capability manifest | `semantic:read` |
| POST `/semantics/browse` | Query <=2,000 chars, kind, version, limit <=200, cursor | `semantic:read` |
| POST `/semantics/resolve` | <=100 term IDs/mentions, context refs, version | `semantic:read` |
| POST `/evolution/runs` | Parent ref, frozen authorized workload, profile and budget | `semantic:propose` |
| GET `/evolution/runs/{id}` | Candidate comparisons, gate outcomes, missing evidence | `semantic:read` |
| POST `/evolution/candidates/{id}/evaluate` | Frozen EvaluationSpec ref; job submission | `semantic:evaluate` |
| POST `/evolution/candidates/{id}/publish` | Exact approved certificate and expected active version | `semantic:publish` |
| POST `/semantics/rollback` | Target version, impact report, governed action ref | `semantic:publish` |
| GET `/events` | Authenticated SSE with `Last-Event-ID`, bounded replay and gap event | `audit:read` plus per-object checks |
| GET `/qualification` | Clauses/profiles/evidence freshness summary | `qualification:read` |

Implement an idempotent trusted internal `propose_action(ActionIntent)` service; external clients submit workflows, not arbitrary new executable tool definitions. CLI/MCP reads use the same services; consequential MCP actions submit governed proposals and cannot accept approvals through model-generated tool arguments alone.

Errors: 401 authentication, 403 authorization where disclosure is safe, 404 hidden/missing object, 409 revision/idempotency/state conflict, 410 explicitly accessible expired resource where appropriate, 413 payload limit, 422 invalid schema, 429 quota, 503 required dependency unavailable. A response error contains `code`, `message`, `correlation_id`, `retryable`, and authorized `details`. Detailed hidden denial reasons remain in restricted audit records.

POST commands require `Idempotency-Key`; scope is tenant + actor + route + logical operation. Same key/same canonical request returns original result; same key/different request conflicts. Conditional commands require `If-Match` containing the last observed revision; omit it -> 428. Never delete idempotency records while their logical effects could be retried. SSE event data includes event ID, sequence, kind, object ref, timestamp, safe summary and revision; reconnect rechecks permissions.

## 6. GUI Information Architecture

Add these as routes or tabs inside existing product navigation; keep operational lists dense and readable. Reuse current visual tokens and controls, not a separate demo application.

| View | Required content and workflow |
| --- | --- |
| Intents | Filterable list: title, owner, status, deadline, acceptance progress, blocked reason; create/edit with outcome, non-goals, scope, limits and advanced settings progressively disclosed |
| Intent detail / Run | Task dependency view plus accessible table, current assignee, remaining aggregate budget, actual progress, blocked tasks, cancel control, acceptance results |
| Evidence inspector | Claim text, type, support/conflict state, freshness, permitted source locator, derivation path, independent origins, challenge history; no unsupported certainty badge |
| Action review | Exact effect and destination/account, changed fields, current/pre-state, risk, enforceability, required obligations, evidence, expiry, reviewer decision; show conflict if revision changes |
| Evolution | Parent/candidate diff by content/schema/tool view, hypothesis, isolated scope, paired per-case results, uncertainty, hard gate failures, approval/publication/rollback state |
| Assurance | Requirement/profile status, evidence timestamps and hashes, unsupported integrations, export/verify commands, restore qualification and unresolved failures |

Required states in every affected view: initial loading, empty, partial/truncated, retryable failure, denied, offline, stale, conflicting revision, background operation, cancelled, and verified result. No generated prose may imply completion while a worker or independent postcondition is unresolved.

Desktop acceptance: 1440x900 and 1920x1080. Mobile: 390x844 and 360x800. Test keyboard-only operation, 200% zoom, reduced motion, long identifiers, long translated text, empty and large result sets. Use textual status alongside color, labeled icon buttons and focus-visible controls. Graph visualizations require equivalent tabular navigation; validation must check actual rendered content, not just the existence of a canvas.

## 7. Qualification Targets

These are selected acceptance targets to measure, not current capacity claims or contractual SLAs. Use an isolated named environment with hardware, OS, Python/Node versions, database settings, and container/build digest recorded. Reference local profile: 8 logical CPUs, 16 GiB memory, SSD, 1 API process, 2 workers, PostgreSQL on the same test host; single-worker SQLite is measured separately. No model-provider time is hidden inside a control-plane latency claim.

| Scenario | Target |
| --- | --- |
| 100,000 claims, 300,000 support/dependency edges, 10,000 stored actions, 20 concurrent local clients | Report cardinalities and seeds; fixtures span at least 2 tenants |
| Cached-schema admission/checking, <=20 obligations and <=100 evidence refs | p95 <=250 ms, p99 <=500 ms after warm-up; measure total including authority persistence, excluding external model/tool network execution |
| Browse/resolve with <=50 returned objects | p95 <=750 ms under same load; no unauthorized results |
| Task cancellation before dispatch | No subsequent dispatch after committed revocation is observed by mandatory final check; already dispatched effects explicitly reconciled |
| Worker recovery | Expired lease reacquired within 60 s after failure detection, preserving fencing and idempotency |
| Candidate comparison | Complete per-case outcomes, equal budgets and required sample counts; no fixed completion time promised for provider-bound evaluation |
| Local control-plane resources | No unbounded queue or memory growth; report memory plateau, queue depth, throughput and error distribution over 30 min |
| Browser | Primary workflow usable within 3 s on the named local test setup after API ready; no route crash, horizontal page overflow, hidden approval error or inaccessible critical control |
| Authorization/security invariants | Zero observed forbidden effects in mandatory adversarial corpus; any violation blocks release regardless of averages |

Performance suite: 2 min warm-up, 10 min recorded measurement per standard load run; report at least 10,000 admission samples when measuring its percentiles. Keep timeout and failure samples in denominators. If the host cannot run this profile, record performance BLOCKED and provide measured smaller-profile results separately.

## 8. End-to-End Acceptance Scenarios

The plan supplies implementation and evidence instructions. Each scenario must observe the real path and independent state. Synthetic fixtures are permitted for controlled ground truth; synthetic adapter responses cannot stand in for actual transport qualification.

| ID | Scenario | Required observable outcome |
| --- | --- | --- |
| ASPEII-E2E-01 | Read-only incident investigation from intent through delegated analysis to GUI | Typed evidence, bounded tasks, acceptance results, no mutation; restart retains run |
| ASPEII-E2E-02 | Ambiguous goal and missing budget/destination | Draft saved; consequential activation blocked with actionable missing fields |
| ASPEII-E2E-03 | Evidence laundering across generator, MCP, database, RAG and critic | Origin preserved; no factual promotion or action approval from circular support |
| ASPEII-E2E-04 | Reversible graph correction with genuine approval | Exact action approved, single mutation observed, independent postcondition and signed receipt |
| ASPEII-E2E-05 | Fake/stale/cross-tenant approval and changed arguments | Denied with zero independent handler calls and no data mutation |
| ASPEII-E2E-06 | Concurrent delegation, exhausted root budget and expired worker | Only eligible fenced worker acts; aggregate ceiling respected |
| ASPEII-E2E-07 | External write commits then times out | UNKNOWN_OUTCOME then reconciliation; no blind retry/duplicate effect |
| ASPEII-E2E-08 | Source correction, permission revocation and surviving support | Immediate access/admission denial where required; correct CTAR impact and preserved authorized support |
| ASPEII-E2E-09 | Build initial semantic layer from table/document sources | Real read probes, typed mappings and unsupported proposals; approval-gated version zero |
| ASPEII-E2E-10 | Candidate improves held-out tasks but violates a security invariant | Rejected; parent remains active; failure visible in GUI |
| ASPEII-E2E-11 | Qualified candidate publishes, then governed rollback | Atomic version change, correct invalidation, durable lineage and restored semantics |
| ASPEII-E2E-12 | Conflicting requirements and finite challenge budget | Counterexample recorded; unresolved claim stays incomplete; no universal-convergence claim |
| ASPEII-E2E-13 | Actual stdio and HTTP MCP sessions | Real server logs match calls; unreachable/malicious/schema-changing server fails safely |
| ASPEII-E2E-14 | Receipt tamper, key rotation and restore | Independent verification catches tampering; valid historical keys handled by trust policy; consumed approval not replayable |
| ASPEII-E2E-15 | No-egress installation with models disabled/local model | Deterministic core usable; unavailable provider visible; no undeclared network traffic |
| ASPEII-E2E-16 | Full GUI and release-verifier negative controls | Real backend workflow succeeds; removal/staleness of one mandatory receipt prevents 100% completion |

## 9. Evidence Required for Every Release

The independent verifier must inspect:

1. Frozen requirement/contract/scenario registry and scope/profile declarations.
2. Source/build/dependency/configuration manifests, migration version, environment and integration modes.
3. Executed case records and raw output, not just test source paths or manually edited PASS flags.
4. Real HTTP/MCP/worker/store and browser observations with identity and revision bindings.
5. Independent effect counters, before/after state, external reconciliation observations, and absence-of-effect assertions for denial cases.
6. Restart/concurrency/restore/revocation/tamper outcomes and performance measurements.
7. Clause-level mappings and reasons for every incomplete, blocked, deferred, stale, flaky, skipped, or inconclusive item.
8. Signed export/checkpoint metadata where configured, with explicit verification limitations.

No current ASPEII implementation percentage is asserted by this document. The three local helper probes in the research report are gap evidence, not proof that the future implementation passes. Refer to the companion plan for the executable work order and fresh-agent handoff protocol.

<!-- tracker-integration -->

## 10. Tracker Integration and Honest Completion Reporting

This section adds identifiers and reporting rules for the EOIP programme tracker. It does not change sections 1–9. The tracker's parser stops at the marker above this heading, so nothing below is a requirement.

### 10.1 Tracked Identifiers

| Item | Identifier | Count | Defined by |
| --- | --- | --- | --- |
| Clause | `ASPEII-RQ-NNN.C01` … `.C06` = numbered items 1–6 of each requirement, in order | 216 | §1.1 |
| Acceptance example | `ASPEII-RQ-NNN.ACC` = the requirement's `Acceptance:` line | 36 | §1.1 ("the section's acceptance examples are mandatory") |
| Scenario | `ASPEII-E2E-01` … `ASPEII-E2E-16` | 16 | §8 |
| Work-package gate | `ASPEII-WP01.GATE` … `ASPEII-WP18.GATE` | 18 | plan §4 |
| Release profile | `ASPEII-PROF-01` … `ASPEII-PROF-09` (plan §11 rows in order; ids listed in plan §13.2) | 9 | plan §11 |

The completion numerator stays `VERIFIED clauses / 216` (§1.1, ASPEII-RQ-036). A full-completion claim also needs every acceptance example, scenario, gate and supported profile VERIFIED (ASPEII-RQ-036 clauses 2 and 6, §9). 215/216 is not 100%.

### 10.2 Status Reporting

ASPEII keeps its own status values. The tracker stores one canonical state per item and reports the ASPEII value:

| Tracker canonical state | Status written in this programme's own ledger |
|---|---|
| OPEN | `OPEN` |
| IN_PROGRESS, CODE_COMPLETE, EVIDENCED | `IN_PROGRESS` |
| VERIFIED | `VERIFIED` |
| BLOCKED | `BLOCKED` |
| FAILED | `FAILED` |
| STALE | `STALE` |
| DEFERRED | `DEFERRED` |

The IP status mapping in plan §8 is unchanged and is the only way an IP status affects an ASPEII clause.

### 10.3 What Moves a Clause

A file path, class or function name, test-file name, test count, commit hash, green CI badge, screenshot or an agent's statement is never proof of completion on its own. The tracker and the verifier refuse EVIDENCED unless an executed run is recorded (command, exit code 0, environment, evidence path and its SHA-256, bound to the current requirement text), and refuse VERIFIED unless a reviewer who is not the producer re-ran it and recorded the verification reference.

| Target state | Required evidence (checked by the tracker and by `verify_programme_ledger.mjs`) |
|---|---|
| IN_PROGRESS | Owner and work reference (task card, branch, ledger draft or DR id). |
| CODE_COMPLETE | 40-hex commit and the changed paths. The paths are navigation only and are never proof. |
| EVIDENCED (reported IN_PROGRESS) | Commit; evidence path inside `.audit-scratch/aspeii/<run-id>/`; its SHA-256; producer; exact command; exit code 0; environment; release profile id (§13.2 of the plan); completion level L2–L6 (L0 design/source references and L1 static checks are not evidence, plan §1.1); executed case ids from `cases.jsonl`; attestation that it ran against the real boundary with no skipped, flaky, stale, inconclusive or mismatched case. |
| VERIFIED | Everything above plus: reviewer different from the producer, review date, verification reference `.audit-scratch/aspeii/<run-id>/verifier-result.json` produced by `scripts/verify_aspeii_evidence.py` with exit 0, and the reviewer's re-run attestation. `.ACC` items additionally need all six clauses VERIFIED. |
| FAILED | Failure note with the observed numbers or error, and a reference to the failing run. |
| BLOCKED | The blocking dependency, decision id or missing input. |
| STALE | What changed (source, artifact, environment or requirement text). |

### 10.4 Cross-Programme Decisions Holding ASPEII Items

| Decision | Subject | Items held below VERIFIED until DECIDED | Record as |
|---|---|---|---|
| XP-02 | Prediction / fact status models differ | `ASPEII-RQ-030.C04` | CONFLICT-IP-NNN (next free number in docs/ip/ip-progress-ledger.md) |
| XP-11 | One change stream for leases, CTAR and revocation | `ASPEII-RQ-030.C03` | DR-IP (REQ-LSE-002) + CIP ADR (P0.3) |
| XP-22 | External model endpoints | `ASPEII-PROF-07` | CONFLICT-IP-NNN (next free number in docs/ip/ip-progress-ledger.md) |
| XP-24 | Referenced documents not in this package | `ASPEII-WP01.GATE` | Owner to supply |

The compatibility rules of §2.1 already settle XP-10 (fact vs worker leases), XP-12 (undeclared actions are R4-denied for ASPEII effects), XP-13 (answer checkpoint), XP-14 (IP flags cannot bypass ASPEII admission), XP-23 (one signer), XP-25 (retention), XP-26 (dissent independence) and XP-27 (commitment fulfilment); the tracker asks the owner to confirm them. `aspeii-research-analysis.md` and `GUI-UIX-requirements.md` are referenced but were not part of this package (XP-24): WP01 stays BLOCKED until the research analysis is supplied, and no agent may reconstruct its probes from memory.
