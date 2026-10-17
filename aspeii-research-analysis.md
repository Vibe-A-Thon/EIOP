# ASPEII Research and EOIP Applicability

Research date: 2026-10-17 (Asia/Calcutta). Repository baseline: `00f18804ca2c7a5d12855c4763973fdfe892deac`.

Companions: [requirements](aspeii-reqirements.md) and [implementation plan](aspeii-implementation-plan.md). The requested spelling `reqirements` is intentional. ASPEII is a project workstream identifier, not a standard, third-party product, or claim of invention.

## 1. Decision

All six topics are applicable, with different maturity and assurance boundaries. Build one integrated EOIP/KnowGridFlow capability: explicit user intent, bounded delegation, typed knowledge, evidence-dependent action admission, and evaluated semantic evolution. Preserve the existing graph, agent, API, UI, and community repair concepts. Neither a research paper nor installation of a research package establishes production readiness.

The proposed implementation is an EOIP-specific design. The source summaries below describe the literature; the normative contracts in the companion documents are original engineering decisions for this repository. They are not claims that a cited author implemented or proved the proposed EOIP system.

| Topic | Decision | First EOIP use | Restriction |
| --- | --- | --- | --- |
| Intelligent AI Delegation | Adopt its delegation problem framing | Incident investigation with accountable child tasks | No unconstrained recursive delegation or agent marketplace required |
| Intent engineering | Adopt explicit outcome contracts | Turn a business objective into measurable completion predicates | Natural-language goals do not grant permissions |
| EvoOntology | Adapt architecture; qualify any imported package independently | Versioned semantic browsing and evaluated mapping improvements | No direct agent rewrite of published ontology, policy, evaluator, or executable tools |
| Proof-Carrying Agent Actions | Combine action identity and independently checked obligations | Approval-bound graph mutation and connector writeback | A signed record is not proof of factual correctness or successful external execution |
| Semantic laundering research | Adopt typed-result and support-preservation controls | Prevent model claims becoming facts through tools, memory, or citations | Observed database content can itself be false or model-generated |
| Applied Epistemic Engineering | Adopt explicit claims, challenges, and revision history | Requirements and domain claims linked to falsifying evidence | No universal convergence guarantee or calibrated probability from heuristic scores |

## 2. Method and Evidence Limits

Research traversed supplied URLs, linked primary papers, official documentation, repositories, pinned repository files, primary technical illustrations, and official podcast/video listings. Searches also covered demonstrations, talks, and audio. Technical conclusions rely on primary material. The supplied PyShine article was inspected as a discovery source, then checked against the authors' paper and repository.

Evidence labels:

- `SOURCE`: a statement made by the linked author/project, not independently reproduced here.
- `LOCAL`: source inspection of this EOIP checkout, limited to the paths described below.
- `PROBE`: a bounded local execution performed during this research.
- `DESIGN`: selected EOIP behavior to implement and verify.
- `UNVERIFIED`: unavailable content, unresolved factual claim, unexecuted integration, or unmeasured performance.

This was not an exhaustive audit of every project file or every publication on these topics. No vendor benchmark, complete paper experiment, production environment, live connector writeback, or external code dependency was executed. No application code was changed. Existing untracked community and Graph Neurons documents were preserved.

Multimedia coverage is deliberately precise: the EvoOntology architecture PNG was downloaded and visually inspected; the official DeepMind podcast's episode description and chapter metadata were read. Its YouTube page was found but direct retrieval was throttled. The EvoOntology MP4 link was found in the pinned README but could not be fetched by the browser tool. Neither recording was listened to or watched, and neither is used as empirical evidence. PDF text was available; PDF screenshot requests failed, so relevant delegation sections were also checked in arXiv HTML. No inaccessible material is counted as reviewed content.

## 3. Research Findings

### 3.1 Intelligent AI Delegation

`SOURCE`: Tomasev, Franklin, and Osindero's February 2026 DeepMind paper treats delegation as allocation plus authority, responsibility, accountability, monitoring, and verification. It discusses decomposition, capability matching, changing conditions, trust, permissions, and human participation. This is a framework proposal, not a deployable EOIP orchestration library or a performance guarantee. Its enterprise-facing implications are also discussed by a coauthor in Google's August 2026 article. [Paper](https://arxiv.org/html/2602.11865v1), [Google Cloud article](https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better/).

`DESIGN`: represent a task as a contract with a verifier, current authority, measurable budgets, dependencies, and an accountable owner. Reassignment must fence the previous executor; cancelling a task must prevent subsequent side effects. Human review is a first-class task with a decline/escalation route. Success is an independently evaluated result, not simply all child processes returning normally. Internal scheduling precedes any external-agent federation.

Applicability is high because EOIP already has typed agent contracts and bounded orchestration. The missing work is contract-level outcome semantics, durable authority transfer, current capability qualification, aggregate budgets, and recoverable execution.

### 3.2 Intent Engineering

`SOURCE`: the supplied Concepts article defines intent around desired outcomes, constraints, and success criteria. It explicitly describes an emerging practice with limited benchmark validation. It does not define a normative wire format, security model, or universal compilation algorithm. [Supplied concept](https://concepts.dsebastien.net/concept/intent-engineering/).

`DESIGN`: keep a human-readable goal, but execute only a validated `IntentSpec` containing scope, permitted effects, acceptance predicates, non-goals, budgets, and unresolved fields. The compiler may propose interpretations, but cannot infer a production tenant, approval, monetary budget, or data-export authority from a general request. Business objectives remain linked graph objects; they are not silently repurposed as execution grants. A revised intent gets a new revision and invalidates dependent execution decisions as appropriate.

### 3.3 EvoOntology

`SOURCE`: the September 2026 paper proposes a queryable ontology layer and workload-based evolution, with candidate/parent comparison under fixed evaluation conditions. Its experiments are author-reported, not EOIP results. The abstract describes four backbones while the experimental setup lists six; the pinned README distinguishes a four-backbone analysis subset from full six-backbone results. Do not merge their denominators or transplant their gains. [Paper](https://arxiv.org/html/2609.15779v1).

The pinned architecture documents put deterministic storage, validation, and lifecycle code in Python, while construction and evolution intelligence live in agent skills. Evaluation can use ground truth or LLM judging. That makes evaluator independence an integration issue, particularly for operational semantics. [Architecture](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/docs/architecture.md).

`DESIGN`: use EOIP-owned semantic views over existing graph and ontology records. Add bounded browse/resolve operations, evidence-backed builder proposals, trajectory attribution, immutable candidate versions, isolated evaluation, and transactional publication. A schema candidate, content candidate, and tool configuration candidate are different types. Tool candidates may select preinstalled reviewed implementations; they cannot install code or widen their own authority. Model-specific optimizations stay in model-specific overlays unless validated across all supported consumers.

`SOURCE`: inspected repository revision is `c94389b764394379086ff25e50d0e0f4396167b4`, commit date 2026-10-09. Root license is MIT, copyright Meiduo Chong. This is not a blanket conclusion about benchmark datasets, bundled dependencies, model access, or all redistributed artifacts. [Pinned license](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/LICENSE).

### 3.4 Proof-Carrying Agent Actions: Distinct Uses of the Name

`SOURCE`: Wang's June 2026 PCAA paper organizes runtime governance around action certificates, explicit approval enforceability, and replayable receipts. It distinguishes pre-execution control from observation after execution. Its empirical corpus is protected rather than fully published, limiting independent reproduction. CAVA is a related July paper concerning canonical runtime action identity. These are proposals, not an established universal PCAA standard. [PCAA](https://arxiv.org/html/2606.04104v1), [CAVA](https://arxiv.org/abs/2607.13716).

`SOURCE`: a separate Kadyrbek/Mansurova Scientific Reports article, published 2026-10-13 as an early accepted article, uses PCAA for typed action certificates checked independently of the planner. Its abstract describes invocation binding, authoritative tool obligations, and a small semantic/structural evaluation battery. Its local timing measurements do not establish end-to-end EOIP latency. Full implementation and experimental reproduction were not performed here. [Publisher article](https://www.nature.com/articles/s41598-026-74900-x).

`DESIGN`: combine exact invocation binding with independent policy/evidence checks. Clearly distinguish four assurance objects: authorization decision, obligation verification, execution observation, and cryptographic integrity. None substitutes for another. EOIP's profile does not claim protocol compatibility with either PCAA publication. A formal proof plugin may later discharge a precisely modeled predicate, but must publish its logic, assumptions, checker, and trusted base. It cannot prove arbitrary real-world truth from an LLM explanation.

### 3.5 Semantic Laundering

`SOURCE`: Romanchuk and Bondar describe propositions gaining apparent warrant merely by crossing trusted architectural channels. They distinguish observing, computing, and generating, and analyze circular validation under stated assumptions. The paper's theorem is conditional on its model; it is not evidence that every possible agent system fails or that typing alone guarantees truthful data. A related warrant-carrying architecture appears as an IETF Internet-Draft, not an adopted RFC. [Paper](https://arxiv.org/html/2601.08333v1), [draft](https://datatracker.ietf.org/doc/html/draft-bondar-wca-00).

`DESIGN`: record how a result was produced separately from what its content warrants. An API can authentically return an unsupported model claim. A calculator can correctly transform wrong inputs. A signed receipt can faithfully describe an ungrounded answer. Preserve input lineage through summaries, caches, retrieval, memory, ontology proposals, and agent handoffs. Duplicate copies of one source do not count as independent support. A model judge is advisory evidence about an output, not a new observation establishing the output's truth.

### 3.6 Applied Epistemic Engineering

`SOURCE`: the Specsmith primer proposes explicit belief artifacts, boundaries, stress tests, reconstruction, confidence propagation, and trace sealing. Its contradiction detector is described as heuristic, and its certainty score uses assigned weights. Its convergence axiom and seal mechanism do not establish universal termination, empirical calibration, or factual truth. [Primer](https://specsmith.readthedocs.io/stable/aee-primer/).

`DESIGN`: create an EOIP claim/challenge lifecycle with finite evaluation budgets, independently recorded counterexamples, and versioned decisions. Detect exact structured contradictions deterministically; expose natural-language contradictions as candidates. Report `NO_NEW_FAILURES_IN_EXECUTED_SUITE`, never `ALL_FAILURES_ELIMINATED`. Preserve requirement clauses even when an implementation is deferred; changes to the acceptance scope are decisions, not evidence of completion.

The repository linked by current documentation resolves to `layer1labs/specsmith`. Inspected revision: `1e8ada569d4dfcb1a1fedddde4bd35c49fbec2a1`, commit date 2026-07-29. Its root license is MIT. EOIP can reuse ideas without making Specsmith a runtime dependency. Any selected code import must be pinned and reviewed separately. [Repository](https://github.com/layer1labs/specsmith), [pinned license](https://raw.githubusercontent.com/layer1labs/specsmith/1e8ada569d4dfcb1a1fedddde4bd35c49fbec2a1/LICENSE).

## 4. EOIP Baseline and Integration Gaps

These findings identify implementation starting points, not release qualification. Line numbers can move; the symbols and baseline commit identify the inspected code. Runtime probes below exercised helpers in an isolated Python process, not public production endpoints.

| ID | Evidence | Observation | Required response |
| --- | --- | --- | --- |
| AS-G01 | LOCAL/PROBE: `packages/eoip/provenance/trust.py:promote_fact` | Confidence >= 0.8 alone can set `CERTIFIED`; an arbitrary nonempty rule/approver string is also accepted by the helper | Replace scalar promotion with resolved, authorized, scoped verification records; migrate legacy certificates without endorsing them |
| AS-G02 | LOCAL/PROBE: `packages/eoip/agents/tools.py:ToolRegistry.invoke` | Approval gate checks presence of `approval_id`, not a bound approval decision | Resolve approval under tenant, actor, policy, action digest, expiry, and current preconditions before dispatch |
| AS-G03 | LOCAL/PROBE: `packages/eoip/tools_contract/mcp_bridge.py:ExternalMCPClient` | Registration reports connected; invocation returns a constructed success object without server transport | Qualify real MCP adapters; label/remove synthetic production success paths |
| AS-G04 | LOCAL: same file, `ToolExecutionAttestor` | Hard-coded default HMAC secret; in-memory certificates; signed payload omits metadata | Remove default secret; document HMAC assurance correctly; durable, fully bound, independently verifiable receipts |
| AS-G05 | LOCAL: `packages/eoip/agents/tools.py:arguments_digest` | Uses Python `repr(sorted(...))`, not cross-runtime canonical JSON | Add versioned canonicalization and cross-language vectors |
| AS-G06 | LOCAL: `packages/eoip/contracts/agent.py` | Agent contracts have risk/budgets; goal is a string; result evidence is references | Extend with intent, task, typed claim, and verified-outcome references |
| AS-G07 | LOCAL: `packages/eoip/agents/orchestration.py` | Sequential bounded child execution; aggregate status derives from child status | Add durable DAG tasks, leases, aggregate budgets, and acceptance verification |
| AS-G08 | LOCAL: `packages/eoip/agents/proposals.py` | JSON-file decisions intentionally do not execute mutations | Preserve proposal/execute separation; bind immutable decision to execution |
| AS-G09 | LOCAL: `apps/api/main.py` proposal routes | Route passes body `actor_id` to decision store | Resolve authenticated identity server-side; verify middleware and object permissions through public APIs |
| AS-G10 | LOCAL: `frontend/src/screens/Agents.tsx` | Proposal UI uses `p.id`, while `ChangeProposal` defines `proposal_id`; decision errors are swallowed | Correct DTO integration and show conflicts/failures in browser tests |
| AS-G11 | LOCAL: `packages/eoip/ontology/drift.py`, `gitops.py` | Drift proposals and semantic diff/version helpers exist | Add held-out evaluation, durable publication transaction, provenance and rollback integration |
| AS-G12 | LOCAL: `packages/eoip/agents/governed.py:EvidenceVerificationAgent` | Checks existence of provenance properties, not support for each proposition | Separate provenance completeness from evidentiary verification |
| AS-G13 | LOCAL: `packages/eoip/agents/runtime.py:_explain` | Confidence includes fixed values based on result status/evidence presence | Label heuristics; never make them authorization or truth gates |
| AS-G14 | LOCAL: `packages/eoip/graph/business_intent.py` | Objective/capability traceability exists | Add executable outcome contracts without replacing business taxonomy |
| AS-G15 | LOCAL: `packages/eoip/state/engine.py` | Inspected state engine stores events and snapshots in Python containers | Do not infer durable storage from its name; use qualified transactional persistence |
| AS-G16 | LOCAL: `packages/eoip/jobs.py` | File-backed queue identifies itself as single-worker | Reuse only within its verified limits; distributed lease/outbox behavior requires additional work |
| AS-G17 | LOCAL: `scripts/verify_requirement_evidence.py` | Explicitly verifies test evidence, with MVP-specific IDs | Extend evidence tooling through a new scoped profile; do not call test mapping product completion |
| AS-G18 | LOCAL: `backend/server.py` | Development shim exports `apps.api.main.create_app`; demo/memory defaults | Integrate active app and real production config; do not count demo success as durable operation |

### 4.1 Reproduced Helper Behavior

Executed with `PYTHONPATH=.;packages` in this checkout. The registered test handler only appended to an in-memory list. The MCP endpoint used the reserved `.invalid` domain. There were no external side effects.

```json
{
  "confidence_only_promotion": "CERTIFIED",
  "arbitrary_approval_status": "SUCCEEDED",
  "in_memory_handler_calls": 1,
  "external_connection_status": "connected",
  "external_call_status": "success"
}
```

Reproduction outline: call `promote_fact({}, "CERTIFIED", confidence=0.8)`; register a non-read-only R2 `ToolContract` with an in-memory handler, invoke it with `approval_id="nonexistent-approval"`; construct `ExternalMCPClient`, register one tool at `https://invalid.example.invalid/mcp`, and invoke that tool. These observations demonstrate helper weaknesses. They do not establish that a remotely reachable attacker can exploit every path; production reachability and middleware require separate tests.

### 4.2 Reconcile Existing Work

| Existing document | Relationship |
| --- | --- |
| [Community requirements](community-ip-requirements.md) and [plan](community-ip-implementation-plan.md) | CTAR owns change-triggered invalidation/repair and AMRB. Use its `dependent DEPENDS_ON input` direction and current-authorization rules; add ASPEII artifact kinds through a versioned mapping |
| [CRAr.md](CRAr.md) | Reuse its evidence, governed actions, ontology review, and independent QA requirements; ASPEII specifies the intent/delegation/evidence-action behavior in more detail |
| [Graph Neurons requirements](EOIP-engg-doc-pkg/Graph-Neurons-requirements.md) | Neural outputs stay predictions; a high score does not publish a fact or approve an action |
| [GUI requirements](GUI-UIX-requirements.md) and [plan](GUI-UIX-implementation-plan.md) | Extend existing screens, accessible controls, error handling, evidence capture, and browser verification |
| [Licensing](LICENSING.md) | First-party commercial licensing remains; selected third-party artifacts retain their own terms |
| [IP requirements](ip-requirements.md) and [IP plan](ip-requirements-implementation-plan.md) | Appeared as concurrent untracked documents during this task. Targeted review found overlapping warrant, checkpoint, fact-lease, consequence-budget and signed-export contracts. Reuse those owners through the explicit compatibility rules in the ASPEII requirements; do not create competing authority services |

An existing requirement is not complete merely because it overlaps ASPEII. Reuse the same actual verification receipt where it proves both clauses, and retain both requirement identities. Do not overwrite these documents during implementation without reconciling their semantics.

The concurrent IP documents were inspected selectively for overlap, not audited in full. Their warrant status order describes a separate contract from ASPEII's truth/support/lifecycle dimensions. Their fact-validity leases are different from worker execution leases. Their consequence budgets are different from token/time/money budgets. Conflating these concepts would create implementation errors; the compatibility table in the requirements specifies how to keep and enforce both.

## 5. Integrated Design and Tradeoffs

```text
User / service principal
        |
        v
Intent revision -> task DAG -> qualified delegate + attenuated grant
        |                           |
        |                           v
        |                  proposed typed action
        |                           |
        v                           v
Acceptance verifier <--- claim/evidence graph ---> admission checker
                                    |                   |
                  current support / policy / state      v
                                               execution gateway
                                                       |
                                                 real adapter
                                                       |
                                               outcome reconciliation
                                                       |
                                             durable receipt + outbox
                                                       |
                                                CTAR dependencies

Redacted trajectories -> isolated semantic candidate -> paired evaluation
                                           -> reviewed publish / reject
```

The application retains a graph projection for navigation and dependencies. Transactional records govern leases, approvals, budget reservations, execution attempts, and publication. A graph projection lag must never authorize an action. One narrow admission service covers API, worker, MCP, retries, scheduled jobs, and legacy proposal application.

Adopt typed evidence before autonomous evolution: otherwise the learning loop can amplify unsupported claims. Complete bounded internal delegation before external agents: external reputation, payment settlement, and unrestricted peer discovery introduce requirements outside the current product need. Support local and hosted model providers through the same typed interfaces. Missing providers produce an explicit unavailable state.

The design trades some latency and storage for attributable execution. Mitigate that cost with bounded manifests, digest-addressed immutable blobs, indexed support edges, asynchronous graph projection, and caching keyed by identity/policy/revision. Never cache a positive approval across changed authority or state. Measure the added cost rather than quoting research microbenchmarks.

## 6. Research Questions That Remain Open

| Question | Engineering resolution |
| --- | --- |
| Does semantic evolution improve EOIP workloads? | Compare raw retrieval, static semantics, and candidate semantics on the same frozen workload; accept only measured benefit and no mandatory regression |
| Does independent checking catch real action mistakes? | Include argument, destination, actor, state, tool-version, risk and evidence substitution attacks; observe the actual adapter invocation count |
| Can a remote system be prevented from acting? | Qualify its exact enforcement mode; observation-only adapters cannot satisfy mandatory pre-execution gating |
| Are confidence estimates useful? | Evaluate calibration and abstention by task/domain; uncalibrated scores remain labels rather than probabilities |
| Is a semantic candidate generally better? | Require evidence for each supported model/tool/domain combination; do not generalize from one model |
| Can changing evidence invalidate outputs promptly? | Exercise CTAR revocation and correction before worker propagation; read/action gates consult current authority |
| Is the research code commercially distributable in the chosen package? | Review pinned files, dependencies, datasets, notices and deployment model before importing; root licenses alone are insufficient |
| Can all user environments be supported now? | Declare a qualification matrix; unavailable customer systems remain blocked integrations, not passing mocks |

## 7. Source and Media Register

All access dates: 2026-10-17. Mutable documentation is a reviewed snapshot, not a release pin. Titles identify research provenance, not certification.

| ID | Source / medium | Used for / access qualification |
| --- | --- | --- |
| S01 | [DeepMind delegation PDF](https://arxiv.org/pdf/2602.11865) and [v1 HTML](https://arxiv.org/html/2602.11865v1) | Primary framework; PDF text and HTML inspected; PDF screenshot unavailable |
| S02 | [Google Cloud coauthor article](https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better/) | Primary enterprise discussion; published 2026-08-21 |
| S03 | [DeepMind podcast episode](https://podcasts.apple.com/ca/podcast/when-millions-of-ai-agents-meet/id1476316441?i=1000773931778) | Official audio listing, 2026-06-23; metadata/chapters only; delegation chapter starts 15:46 |
| S04 | [Official video](https://www.youtube.com/watch?v=V04bm-3d6EQ) | Search-discovered video; direct page retrieval throttled; not watched |
| S05 | [Intent engineering](https://concepts.dsebastien.net/concept/intent-engineering/) | Supplied author's concept definition; not a standard |
| S06 | [PyShine EvoOntology article](https://pyshine.com/EvoOntology-A-Self-Evolving-Ontology-Layer-For-Data-Agents/) | Supplied secondary discovery source; no technical claim relies on it alone |
| S07 | [EvoOntology paper v1](https://arxiv.org/html/2609.15779v1) | Primary design and experimental method; experiments not reproduced |
| S08 | [Pinned EvoOntology README](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/README.md) | Repository architecture, subset caveat, links to media |
| S09 | [Pinned architecture](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/docs/architecture.md) | Deterministic-core/agent-skill split and evaluation modes |
| S10 | [Pinned usage guide](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/USAGE.md) | Lifecycle and operational boundaries; not installed |
| S11 | [Architecture illustration](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/assets/evoontology-framework.png) | Visually inspected primary PNG; depiction is not runtime evidence |
| S12 | [Repository demo video](https://github.com/user-attachments/assets/e15f4acd-7161-4ae1-ba41-f2f3ea05488b) | Located through pinned README; fetch failed; no playback claim |
| S13 | [EvoOntology MIT license](https://raw.githubusercontent.com/ruc-datalab/EvoOntology/c94389b764394379086ff25e50d0e0f4396167b4/LICENSE) | Inspected root artifact license |
| S14 | [Wang PCAA v1](https://arxiv.org/html/2606.04104v1) | Governance certificates and bounded disclosure; submitted 2026-06-02 |
| S15 | [CAVA abstract](https://arxiv.org/abs/2607.13716) | Related action canonicalization research; submitted 2026-07-15 |
| S16 | [Author's PCAA article](https://ond.cc/research/pcaa) | Author explanation; page date 2026-06-24 is not arXiv submission date |
| S17 | [Kadyrbek/Mansurova PCAA](https://www.nature.com/articles/s41598-026-74900-x) | Publisher early-article abstract/metadata; separate work; 2026-10-13 |
| S18 | [Semantic laundering v1](https://arxiv.org/html/2601.08333v1) | Typed epistemic boundaries and conditional argument |
| S19 | [Warrant-carrying architecture draft](https://datatracker.ietf.org/doc/html/draft-bondar-wca-00) | Related primary draft; not a standards compliance target |
| S20 | [Specsmith AEE primer](https://specsmith.readthedocs.io/stable/aee-primer/) | Method, heuristic limitations, trace design |
| S21 | [Specsmith repository](https://github.com/layer1labs/specsmith) | Current linked project identity; revision recorded above |
| S22 | [Specsmith MIT license](https://raw.githubusercontent.com/layer1labs/specsmith/1e8ada569d4dfcb1a1fedddde4bd35c49fbec2a1/LICENSE) | Inspected root license; optional components require separate review |
| S23 | [AEE origin website](https://appliedepistemicengineering.com/) | Linked by primer; retrieval failed; not used as reviewed evidence |
| S24 | [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) | JSON canonicalization basis; informative RFC, use exact defined behavior |
| S25 | [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Provenance interoperability vocabulary; does not prove truth |
| S26 | [MCP security guidance, 2025-11-25](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) | Adapter security baseline; qualify the exact implemented protocol version |

The two raw EvoOntology URLs initially attempted on `main` returned 404; GitHub repository metadata identified `master`, and the pinned files above were then read successfully. Search results did not provide a verified primary transcript for every topic. Secondary summaries and generated explanations were excluded from technical assurance claims.

## 8. Recommended Delivery Order

1. Capture baseline and reproduce the unsafe helper paths with regression tests.
2. Establish typed claims, tenant-scoped evidence, immutable action identity, and durable authority.
3. Integrate the action gate and real transport before enabling any new write-capable agent.
4. Add intent contracts and bounded recoverable delegation.
5. Add semantic browse/resolve, builder proposals, and isolated learning experiments.
6. Qualify evaluated publication, CTAR invalidation, operator UI, recovery, and release evidence.

The implementation plan makes this order executable. The requirements remain OPEN until their acceptance behavior is demonstrated on the actual release artifact.
