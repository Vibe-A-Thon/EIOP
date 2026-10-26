# 16 — Security & Privacy Threat Model (KnowGridFlow / EOIP)

| Field | Value |
|---|---|
| Document | 16-SECURITY-PRIVACY-THREAT-MODEL.md |
| Status | **PROPOSED threat model and control plan.** No penetration test, red-team exercise, or formal security audit has been run against EOIP in this research programme. Every "existing control" citation below is a static-code finding (file:line), not a verified runtime guarantee; every "proposed control" is a design decision pending implementation and benchmarking per `15-VALIDATION-BENCHMARK-PLAN.md` BM-18/BM-19. |
| Methodology | Assets -> trust boundaries -> actors -> a STRIDE-tagged pass over the 11 P0 self-inversion cards in `09-CON-TO-PRO-INVERSION-REGISTER.md` §3, plus five named cross-cutting threats; referenced against OWASP Top 10 for LLM Applications (2025 edition) and MITRE ATLAS per `04-COMPETITOR-DEEP-DIVES/C19-llm-threat-guidance.md`. |
| Prior placeholder notice | A pass on 2026-10-19 wrote an earlier version of this file describing controls (HMAC/OIDC verification "on every hop", RFC 8785 Merkle warrants, a tripwire canary kill-switch) as though in force. This version replaces it in full and marks each claim against the code evidence actually found. |

---

## 1. Assets

| Asset | Where it lives | Why it matters |
|---|---|---|
| Graph facts (vertices, edges, properties) | HugeGraph / Neo4j / Neptune / JanusGraph / Fuseki / GraphDB adapters (`graph/*.py`) | The core knowledge product; leakage or tampering corrupts every downstream answer |
| Evidence spans and provenance (source document offsets, lineage) | `provenance/evidence.py`, `provenance/lineage.py` | Without this, an answer cannot be trusted or audited; it is also itself sensitive (may point back to a restricted source document) |
| Embeddings and vector indexes | `retrieval/tenant_index.py`, `retrieval/hybrid_vector_service.py` | Embeddings can leak source content via inversion attacks (OWASP LLM08) even when the source text is access-controlled |
| Agent memory records | `memory_eng/engine.py`, `reasoning/memory.py`, `agents/memory.py` | Currently carries no ACL/tenant/evidence/validity fields (GAP-34); a persistent, under-governed copy of whatever an agent has seen |
| Egress credentials and tokenisation vault contents | `egress/vault.py`, `egress/gateway.py` | Reversible tokenisation means the vault key is the single point of failure for every tokenised value ever sent externally |
| Ontology (schema, SHACL shapes, governance history) | `ontology/manifest.py`, `ontology/gitops.py`, `ontology/governance.py` | Tampering here silently redefines what every future fact means |
| Audit trail | not yet hash-chained (GAP-20) | The record of who did what; currently not tamper-evident, which is itself the threat |
| Per-tenant secrets, data keys, API tokens | `tenancy/layers.py` (AES-256-GCM per-tenant key), `authn/credentials.py`, `authn/tokens.py` | Compromise of one tenant's key or token must not expose another tenant |
| MCP tool-call surface and bootstrap token | `apps/mcp/main.py` | A single shared bearer token today authenticates every MCP caller as the same principal (GAP-09) |
| Source connector credentials | `connectors/*.py` | Connectors read from Jira/Confluence/GitHub/ServiceNow/etc. with live credentials; compromise here is compromise of the source system too |

## 2. Trust boundaries

```
Source systems (Jira, Confluence, GitLab, GitHub, ServiceNow, Datadog, Grafana, Kibana,
                OTel, CI/CD, SBOM, K8s, files, web, JSON)
        │  TRUST BOUNDARY 1: connector credential + SourceEvent emission
        │  connectors/*.py never write the graph directly; PermissionMetadata/acl_hash
        │  captured at ingest (BL-17, Implemented)
        ▼
Ingest (validation/gate.py, identity/resolver.py, mapping/cml.py)
        │  TRUST BOUNDARY 2: validation gate — label/required-property checks only
        │  (BL-28); NOT a typed constraint layer (GAP-12); NOT SHACL-at-write-time
        ▼
Graph (HugeGraph/Neo4j/Neptune/JanusGraph/Fuseki/GraphDB/Memory adapters)
        │  TRUST BOUNDARY 3: tenant isolation — enforced at the embedded-layer
        │  (tenancy/layers.py) and at the API-layer named-graph wrapper
        │  (apps/api/main.py:680), NOT inside any graph adapter itself (GAP-03,
        │  INV-SELF-02 — zero `tenant` references in hugegraph.py/neo4j.py/
        │  neptune.py/memory.py/store.py/rdf_backend.py/janusgraph.py)
        ▼
Retrieval / MCP (retrieval/service.py, apps/mcp/main.py, agents/governed.py)
        │  TRUST BOUNDARY 4: source-ACL enforcement — code exists (authz/pdp.py,
        │  authz/derivation_acl.py) but is called only inside one branch of
        │  retrieve() and only when a `scope` argument is passed; no deployed
        │  caller passes it today (GAP-02, INV-SELF-01, BL-18/U-04)
        ▼
Agents / UI (agents/*, apps/web, apps/vscode-extension)
        │  TRUST BOUNDARY 5: MCP authentication — one shared static bootstrap
        │  token for every caller (GAP-09, INV-SELF-04); egress gateway default
        │  sharing level S0 = none (BL-45, Implemented)
        ▼
Customer (end user, downstream export, white-label deployment)
```

Each numbered boundary is a place where a principal's authority should narrow and currently either does narrow (boundary 1, partially boundary 3 for the embedded layers) or does not yet narrow in the deployed path (boundaries 2 and 4 narrow in library code only; boundary 5 does not narrow at all — every MCP caller is the same principal).

## 3. Actors

| Actor | Capability assumed | Primary concern |
|---|---|---|
| End user | Authenticated via `authn/credentials.py` (argon2id), holds a role (ADMIN/READ/ANALYST/WRITE per `apps/api/route_policy.py`) | Should see only facts their source ACLs and tenant permit |
| Agent (LLM-driven, via MCP or in-process) | Acts under whatever principal context is passed to it — today effectively the MCP bootstrap token's principal, not the invoking user's | Confused-deputy risk: an agent with more authority than the user who prompted it |
| Admin / platform operator | Full route-policy ADMIN class; can read egress manifests, DSAR records, tenant quotas | Insider risk and audit-trail integrity (GAP-20) |
| Attacker-as-tenant | A legitimate tenant account attempting to read or affect another tenant's data | Primary target of BM-05; currently unconfirmed to fail reliably at the adapter layer (GAP-03) |
| Attacker-as-source | A compromised or malicious upstream source system (e.g. a poisoned Confluence page, a crafted webhook payload) | Primary target of the validation gate (BL-28) and the PROPOSED-until-promoted epistemic boundary (BL-40); also the entry point for prompt-injection-via-retrieved-content |

## 4. Threat register — the 11 P0 self-inversion cards

Every P0 gap in `07-GAP-REGISTER.md` has a self-inversion card in `09-CON-TO-PRO-INVERSION-REGISTER.md` §3; this section re-reads each as a STRIDE-tagged threat with likelihood/impact, existing control, proposed control, residual risk, and a detection hook. "Existing control" cites the code evidence already on record; "proposed control" is the card's own selected option, not a new decision made here.

### T-01 — Source-ACL enforcement not applied on deployed paths (GAP-02 / INV-SELF-01)
- **STRIDE:** Information Disclosure.
- **Likelihood / impact:** High / Critical — every deployed retrieval, answer, export, and MCP call today filters by tenant ownership only, not by source ACL or classification (`retrieval/service.py:~440-520`); this is the single largest confirmed gap in the package.
- **Existing control:** `authz/pdp.py:107` `can_read` (tenant, policy epoch, classification clearance, ACL intersect, deny-by-default) and `authz/derivation_acl.py:167` `filter_graph_contexts` exist and pass their own unit tests, but are reached only via `retrieval/service.py:575`, gated on a `scope` argument that `apps/api/extended.py:906-913`, `apps/api/main.py:1770` (`/api/v1/rag`), and `agents/governed.py:250` all omit (BL-18, U-04).
- **Proposed control:** propagate ACL principals through every candidate-generation stage (keyword, vector, hybrid, graph), add a delivery-time re-check, and add a consistency token checked on permission revocation (INV-SELF-01's selected option 2, with option 3 — ACL-embedded indexes per STR-onyx-01/STR-opensearch-01 and Zanzibar-style consistency per STR-rebac-01 — as the target architecture).
- **Residual risk:** until every call site passes `scope`, a new deployed caller can silently reintroduce the gap; the consistency token design does not yet exist, so a revoked user's prior session grants are not provably invalidated.
- **Detection hook:** BM-04 (zero-leakage retrieval test) as a standing CI gate; an observability counter on `retrieve()` calls that omit `scope`, alerting if any production route calls it without ACL scoping.
- **OWASP/ATLAS reference:** LLM08 (Vector and Embedding Weaknesses) names exactly this class of risk (`C19-llm-threat-guidance.md`: "per-document source-ACL enforcement at lexical/vector stage not confirmed").

### T-02 — Tenant isolation not enforced in graph adapters (GAP-03 / INV-SELF-02)
- **STRIDE:** Information Disclosure, Elevation of Privilege.
- **Likelihood / impact:** High / Critical — `tenancy/isolation.py` defines a placement contract (SILO/BRIDGE/POOL) but physical enforcement is explicitly documented as an "External gate"; zero `tenant` references exist in any graph adapter.
- **Existing control:** `tenancy/layers.py:54` enforces isolation for embedded vector/search/SQLite/object/event/secret/cache/log/backup/export layers; `apps/api/main.py:680` wraps non-system-tenant graph access in a `NamedGraphStore` at the API layer. None of this reaches the HugeGraph/Neo4j/Neptune/RDF adapters themselves.
- **Proposed control:** per-backend native isolation unit chosen by `IsolationPlacement` (HugeGraph graph space, Neo4j multi-db, Neptune cluster-per-tenant) immediately for new POOL/BRIDGE deployments, with a tenant-aware `GraphStore` protocol that refuses any call without a resolved tenant context as the long-term target (INV-SELF-02 options 2 and 3).
- **Residual risk:** SILO deployments (dedicated stack per tenant) are adequately protected by the operational convention today; POOL/BRIDGE deployments are not, and the gap is invisible until a cross-tenant adversarial test (BM-05) is actually run.
- **Detection hook:** BM-05; an adapter-level assertion that raises if a query executes with no tenant context bound, added as a defence-in-depth check even before full per-backend isolation lands.
- **OWASP/ATLAS reference:** maps to the "Information Disclosure" class generally; most directly comparable to the cross-tenant risks documented for Azure Cosmos DB Gremlin's shared multi-tenant gateway (`C01-azure-cosmos-db-gremlin.md` INV-azure-cosmos-db-gremlin-02) and Apache AGE/FalkorDB's native space-based isolation that EOIP does not yet replicate.

### T-03 — Egress vault uses an unauthenticated XOR keystream cipher (GAP-08 / INV-SELF-03)
- **STRIDE:** Tampering, Information Disclosure.
- **Likelihood / impact:** Medium (requires an attacker with access to the vault's ciphertext stream or a keystream-reuse condition) / High (reversible tokenisation is specifically meant to protect values sent to external LLM providers; a broken cipher defeats the entire purpose of the vault).
- **Existing control:** `egress/vault.py:24-33,68,84` — XOR with a SHA-256-counter keystream, PBKDF2-derived key, no authentication tag (malleable ciphertext); the module's own docstring already says "ADR-gated: replace with AES-GCM via KMS" (`01a-BASELINE-DELTA-HEAD.md` BL-45 note). `cryptography 50.0.2` (AES-256-GCM) is already installed and already used elsewhere in the same repo (`tenancy/layers.py`), so two crypto standards coexist.
- **Proposed control:** swap to AES-GCM (or ChaCha20-Poly1305) from the already-installed `cryptography` package immediately; add key rotation and envelope encryption; optionally integrate OpenBao (MPL-2.0) Transit for customers wanting a managed KMS, keeping native AEAD as the default (HashiCorp Vault itself is BUSL and excluded from bundling — INV-SELF-03 option 3).
- **Residual risk:** key-management story (where keys are stored, rotated, and who can access them) is not yet designed; swapping ciphers alone does not solve key custody.
- **Detection hook:** BM-18's cryptographic review checklist plus a known-plaintext-recovery test that must fail against the new cipher.
- **OWASP/ATLAS reference:** LLM02 Sensitive Information Disclosure.

### T-04 — MCP surface authenticates one shared bearer token (GAP-09 / INV-SELF-04)
- **STRIDE:** Spoofing, Elevation of Privilege (confused deputy).
- **Likelihood / impact:** High (the MCP surface is the primary agent-facing interface and is designed to grow) / Critical — every MCP caller acts as the same principal; there is no per-user authorization and tools carry no read-only/write annotations.
- **Existing control:** `apps/mcp/main.py:220-223` compares the caller's bearer token via `hmac.compare_digest` against one static bootstrap token (`runtime.py:32`); write tools are absent by design (ADR-007) which limits blast radius for mutation but not for read-side confused-deputy or ACL bypass. Separately, `tools_contract/mcp_server.py:89` `EOIPMCPServer` registers `action.propose`/`action.execute` tools and is in-process only, not mounted by `apps/mcp` — so it is not reachable today, but it is the template any future mount must not repeat the token model of.
- **Proposed control:** OAuth 2.1 resource-server model (per the MCP spec's own authorization extension) giving each agent/user its own token with scopes mapped to the existing RBAC/ABAC model, closing both the confused-deputy risk and the GAP-02 ACL gap for the MCP surface specifically; signed, hash-pinned tool manifests plus server-enforced read-only tool annotations alongside (INV-SELF-04 options 2 and 3).
- **Residual risk:** any legacy integration that only supports the shared-token model remains a weak point until migrated; OAuth 2.1 resource-server support must itself be implemented and tested before the risk is actually closed.
- **Detection hook:** BM-18's malicious tool-poisoning and confused-deputy test suite — pass requires every tool call to be attributable to a real end-user principal and ACL-checked.
- **OWASP/ATLAS reference:** OWASP Top 10 for Agentic Applications (ASI) names tool misuse and privilege abuse directly (`C19-llm-threat-guidance.md` §3); LLM06 Excessive Agency is the LLM-Top-10 analogue.

### T-05 — Backend adapters unproven live; known adapter defects (GAP-01 / INV-SELF-05)
- **STRIDE:** Tampering (silent truncation/mismatch), Denial of Service (if a defect causes a crash under load).
- **Likelihood / impact:** Medium (requires the specific adapter/query shape; not yet confirmed live) / High (silent data loss or wrong results are worse than a visible failure, because they corrupt downstream answers without any error signal).
- **Existing control:** none of the three named defects has a dedicated regression test today: JanusGraph writes `p_`-prefixed property keys but reads unprefixed ones; Neptune adapter has no SigV4 signing and filters edge labels after applying `LIMIT` (silent truncation); HugeGraph forces a Groovy closure that will not run on gremlin-lang-only backends.
- **Proposed control:** patch the three named defects immediately; add a shared conformance test suite (BM-01) run in CI against live containers of each backend; the typed query-IR compiler (GAP-04) removes an entire class of per-backend string-building defects by construction as the structural fix (INV-SELF-05 options 1, 2, 3).
- **Residual risk:** live container access in CI is not available in this research run (U-01); until BM-01 actually executes against live engines, severity remains unconfirmed, not disproven.
- **Detection hook:** BM-01 as a standing CI gate against live containers once available.
- **OWASP/ATLAS reference:** not an LLM-specific threat; standard data-integrity risk, but relevant to LLM09 Misinformation if a silently-truncated result set is cited as complete evidence in a generated answer.

### T-06 — Epistemic planes not enforced store-wide (GAP-07 / INV-SELF-06)
- **STRIDE:** Tampering (fact contamination).
- **Likelihood / impact:** Medium (requires bypassing the mutation gateway, which is not the normal write path) / High — a write that bypasses `ai/boundary.py` could land as an "observed" fact without going through PROPOSED-until-promoted review, corrupting the trust basis for every downstream GraphRAG answer.
- **Existing control:** PROPOSED-until-promoted is enforced in `ai/boundary.py`'s own logic (`:6,77,113,135`) but is not a storage-level plane (label/namespace) on every backend.
- **Proposed control:** a required `epistemic_state` property enforced by `validation/gate.py` immediately; per-backend namespace/label separation for PROPOSED vs CORROBORATED facts as the near-term target; a promotion workflow with audit trail and reviewer sign-off feeding `provenance/warrant_composition.py` as the long-term target (INV-SELF-06 options 1, 2, 3).
- **Residual risk:** interacts with GAP-34 (agent memory has the same class of problem for memory records, see T-09 below); until the storage-level guarantee lands, the contract remains an application convention that a bug or a new write path could silently violate.
- **Detection hook:** BM-15 — attempt to write an "approved" fact through every ingestion path without going through promotion; all attempts must fail.
- **OWASP/ATLAS reference:** LLM04 Data and Model Poisoning; MITRE ATLAS's data-poisoning tactics (version-unverified, per `C19-llm-threat-guidance.md`'s own caveat on ATLAS version naming).

### T-07 — No unified evaluation harness with regression gates (GAP-43 / INV-SELF-07)
- **STRIDE:** Repudiation (no gate means no reliable record that a security property held at release time).
- **Likelihood / impact:** High (this is a certainty today — the harness does not exist) / High — every other claim in this threat model and in `15-VALIDATION-BENCHMARK-PLAN.md` is unverifiable at scale, under adversarial input, or across backends, because nothing runs BM-01 through BM-22 together with regression thresholds in CI.
- **Existing control:** `qa_bench/` and `retrieval/eval.py` provide deterministic RAG evaluation only; no cross-cutting harness.
- **Proposed control:** wire existing ad hoc tests into one marker set with thresholds immediately; a dedicated harness project with fixtures, generators, and reproducibility metadata as the near-term target; a public, LDBC-trademark-compliant benchmark dashboard as a later credibility move (INV-SELF-07 options 1, 2, 3).
- **Residual risk:** every other self-inversion card's benchmark depends on this harness existing; until it does, "PROPOSED" is the only honest status for any number in this package, including this threat model's own residual-risk ratings.
- **Detection hook:** the harness's own test is "does every BM-ID in `15-VALIDATION-BENCHMARK-PLAN.md` execute and gate a release" (BM-22).
- **OWASP/ATLAS reference:** not a named OWASP/ATLAS item; this is the infrastructure precondition for proving every other control in this document actually holds.

### T-08 — String-built Gremlin and regex-only injection defences (GAP-05 / INV-SELF-08)
- **STRIDE:** Tampering, Elevation of Privilege (query/prompt injection).
- **Likelihood / impact:** Medium (requires attacker-controlled property keys or labels reaching the two named call sites) / High — a successful injection could escape the intended query boundary and execute arbitrary Gremlin/Groovy.
- **Existing control:** property keys and labels are spliced into Gremlin/Groovy scripts as strings in `adapters/janusgraph.py:192,276` and `graph/hugegraph.py:525-551`; `agents/firewall.py` relies on regex patterns only for the separate agent-prompt-injection surface.
- **Proposed control:** parameterise the two named call sites immediately; route every backend call through the `QueryPlan` compiler so no hand-built script ever reaches a backend, as the structural fix; adopt gremlin-lang + typed parameters as the only wire format once TinkerPop 4.0 is stable (currently beta) as the long-term target (INV-SELF-08 options 1, 2, 3).
- **Residual risk:** option 2 depends on GAP-04 (query-IR compiler) landing; TinkerPop 4.0 beta status means option 3 is not yet actionable.
- **Detection hook:** BM-18/BM-07's injection corpus (malicious property keys/labels) run against every adapter; zero successful injections is the pass condition.
- **OWASP/ATLAS reference:** LLM01 Prompt Injection is the LLM-facing analogue (GraphRAG context is separately fenced via `PromptInjectionFence`, `ai/graphrag.py:177`, commit c264c07); this specific threat is closer to classic query injection and is tagged against OWASP's broader injection guidance rather than LLM01 directly, since it does not require an LLM in the loop.

### T-09 — Agent memory lacks ACL, tenant, evidence and validity fields (GAP-34 / INV-SELF-09)
- **STRIDE:** Information Disclosure, Repudiation (memory persists without an evidence trail).
- **Likelihood / impact:** High (every agent-memory competitor researched — Cognee, Mem0, Graphiti/Zep, Letta — shows the same structural gap, so this is an industry-wide pattern, not an EOIP-specific oversight, but that does not reduce impact) / High — a revoked user's prior conversation memory can remain accessible indefinitely with no ACL, tenant, evidence, or validity field to check against.
- **Existing control:** none specific; memory records in `memory_eng/engine.py`, `reasoning/memory.py`, `agents/memory.py` carry no ACL principal set, tenant scope, evidence pointer, or validity window.
- **Proposed control:** add ACL/tenant/evidence/validity fields to the existing memory schema immediately; route memory writes through the same mutation gateway and promotion workflow as graph facts (propose-not-write, guarding against the "dreaming" subagent risk documented for Letta, `C08-letta.md` INV-letta-01) as the near-term target; treat memory as a queryable view over the governed graph rather than a separate store as a research direction (INV-SELF-09 options 1, 2, 3).
- **Residual risk:** depends on GAP-02 and GAP-07 landing first (T-01, T-06); until then, memory is a second, ungoverned copy of whatever an agent has seen, independent of how well graph-level ACLs are enforced.
- **Detection hook:** BM-04/BM-05 extended to memory — a revoked user's prior memory must become inaccessible immediately via the same consistency-token check proposed for T-01.
- **OWASP/ATLAS reference:** OWASP Agentic Top 10's memory-poisoning category (`C19-llm-threat-guidance.md` §3, entries named "memory poisoning" in secondary sources, confidence 0.4 on the entry list itself).

### T-10 — Local model runtime pinned to an old, root, unauthenticated Ollama (GAP-36 / INV-SELF-10)
- **STRIDE:** Elevation of Privilege, Tampering.
- **Likelihood / impact:** Medium (requires network reachability to the model-serving port) / High — the pin (`ollama/ollama:0.12.3`) is roughly a year old as of this research, runs as root, has no built-in authentication, and a documented path-traversal CVE (CVE-2026-103663, per `04-COMPETITOR-DEEP-DIVES/C09-ollama.md`) affects versions in this range.
- **Existing control:** none beyond Docker's default container boundary; the image runs as root inside that boundary.
- **Proposed control:** bump the pin past the patched version, run as non-root, restrict network policy to internal services only, immediately; front the model port with an authenticating reverse proxy soon after; a `ModelPort` abstraction supporting both Ollama and llama.cpp (a lighter CPU-only alternative, `C09-llama-cpp` STR-llcpp-01) selected per deployment, as the target architecture (INV-SELF-10 options 1, 2, 3).
- **Residual risk:** none blocking — this is an isolated operational fix with no cross-dependency on other P0 items.
- **Detection hook:** BM-14's CVE/vulnerability scan of the pinned image, re-checked on every release as a standing CI gate, not a one-time check.
- **OWASP/ATLAS reference:** LLM03 Supply Chain (the model-runtime dependency itself); see also T-11/T-12 below for the broader supply-chain surface.

### T-11 — No licence allow-list in CI; several attractive components block OEM (GAP-19 / INV-SELF-11)
- **STRIDE:** Tampering (of the build/licence posture), with downstream legal and commercial impact rather than a direct data-security one.
- **Likelihood / impact:** High (the research package itself documents numerous AGPL/SSPL/BUSL/ELv2/commercial-only components already under discussion for adoption) / High — silently reintroducing a blocked licence (Zingg AGPL-3.0, FalkorDB SSPL, HashiCorp Vault BUSL, Grafana AGPL-3.0, Elasticsearch AGPL/SSPL/ELv2, Airbyte mixed ELv2/MIT, Redpanda BUSL, TruffleHog AGPL-3.0, PM4Py AGPL-3.0, igraph GPL-2.0, Raphtory GPL-3.0, Logseq AGPL-3.0, several OWL reasoners LGPL/AGPL) would block the white-label OEM business model that is itself a differentiator (CAP-52).
- **Existing control:** none — no automated licence check exists; licence review has been manual and ad hoc, scattered across `02-TECHNOLOGY-REGISTRY.md`'s per-feature decisions.
- **Proposed control:** a licence-checker CI step against an allow-list derived from `02-TECHNOLOGY-REGISTRY.md` §3 immediately; extend the check to container images and bundled binaries, not just language-package manifests, soon after; an automated SBOM cross-checked against the allow-list on every release as the long-term target, sharing infrastructure with GAP-44/T-12 (INV-SELF-11 options 1, 2, 3).
- **Residual risk:** legal review still has final say on any exception; an allow-list is only as good as its own completeness, which depends on `02-TECHNOLOGY-REGISTRY.md` staying current as new dependencies are proposed.
- **Detection hook:** BM-20 — introduce a dependency with a known-blocked licence on a test branch; the CI gate must fail the build.
- **OWASP/ATLAS reference:** LLM03 Supply Chain (licence risk is a named sub-category of supply-chain risk in the OWASP guidance, though the entries are not individually re-read here).

## 5. Cross-cutting threats named in scope beyond the 11 self-inversion cards

### T-12 — Supply-chain compromise (GAP-19 / GAP-44)
- **STRIDE:** Tampering (of the build artefact or the tooling that attests it).
- **Likelihood / impact:** Medium (a repeat of a 2026-class incident, not a daily occurrence) / Critical — the March 2026 Trivy compromise (`04-COMPETITOR-DEEP-DIVES/C19-supply-chain.md` CLAIM-sc-05) force-pushed `trivy-action` tags and backdoored `setup-trivy` and Trivy v0.69.4 for roughly 12 hours; a CI pipeline that trusted a floating tag rather than a pinned digest during that window would have ingested the backdoor into its own supply-chain tooling, the exact class of risk GAP-44 names as open (no SBOM/signing pipeline; scanners unpinned).
- **Existing control:** `compliance/sbom.py:69` `SbomManager.generate_cyclonedx_sbom` and `verify_compliance` exist but are library-only — referenced only by `compliance/__init__.py` and their own tests; no CI workflow calls them (`01a-BASELINE-DELTA-HEAD.md` NB-14). `requirements.lock` and `requirements-numerics.lock`/`requirements-neural.lock` exist as a dependency record but are not cross-checked against a vulnerability database or a signature in CI.
- **Proposed control:** INTEGRATE Syft for SBOM generation (CycloneDX/SPDX), Grype as the primary vulnerability scanner with Trivy as a second, independently-pinned scanner (never the sole scanner, learning directly from the Trivy incident), cosign for key-based signing by default (keyless/Fulcio/Rekor optional, since air-gapped customers cannot reach public Sigstore infrastructure), and pin every CI Action by commit SHA, not by floating tag (`C19-supply-chain.md` §12-13, cards STR-sc-01, STR-sc-02, INV-sc-01).
- **Residual risk:** scanner databases need a freshness workflow for air-gapped sites (INV-sc-02, unresolved — "private TUF/Rekor too heavy" is the stated concern, with key/bundle offline verification plus a DB-mirror job as the proposed answer, not yet built); scanners find known CVEs, not malicious logic, so this control does not substitute for code review.
- **Detection hook:** BM-20's supply-chain drill (SBOM completeness diff, offline signature verification, tamper test, pinned-SHA lint on workflow files).
- **OWASP/ATLAS reference:** LLM03 Supply Chain directly; MITRE ATLAS's supply-chain tactics (version-unverified per the standing caveat in `C19-llm-threat-guidance.md`).

### T-13 — Query/prompt injection (GAP-05) — cross-referenced
Covered in full at T-08 above; listed here only to confirm it is explicitly in scope per the brief's cross-cutting list, not omitted.

### T-14 — Tool poisoning / confused deputy on MCP (GAP-09) — cross-referenced
Covered in full at T-04 above; listed here only to confirm it is explicitly in scope per the brief's cross-cutting list, not omitted.

### T-15 — Cross-tenant and cross-user leakage (GAP-02 / GAP-03) — cross-referenced
Covered in full at T-01 and T-02 above. The distinct cross-*user* dimension (two users of the same tenant with different source-ACL clearance — the exact INV-SELF-01 benchmark construction) is realised concretely as POC-02 under `20-POC-EXPERIMENTS/` (see that README).

### T-16 — Egress data exfiltration (GAP-08) — cross-referenced
Covered in full at T-03 above for the vault-cipher dimension. The broader egress-exfiltration surface (a malicious or compromised model provider, a crafted prompt attempting to smuggle tenant data through an otherwise-permitted egress call) is additionally covered by `egress/gateway.py`'s existing controls: default sharing level S0 (none), a platform kill switch (`PlatformKillSwitch`), per-endpoint contract-term amendment that disables an endpoint until re-approved, a plugin data-flow manifest enforced at runtime, a sealed immutable manifest per call, and response DLP scanning with re-identification checks (`01a-BASELINE-DELTA-HEAD.md` BL-45 note — all confirmed strengthened at HEAD, with `tests/unit/test_egress_gateway.py` passing). The residual risk is that none of this has been red-teamed with an adversarial exfiltration corpus; that corpus is INV-lt-02's proposed `security/redteam` build (`C19-llm-threat-guidance.md`), targeted at BM-18.

## 6. Summary table

| Threat | STRIDE | GAP-ID(s) | Likelihood | Impact | Benchmark gate |
|---|---|---|---|---|---|
| T-01 Source-ACL not enforced on deployed paths | Info disclosure | GAP-02 | High | Critical | BM-04 |
| T-02 Tenant isolation not enforced in adapters | Info disclosure, EoP | GAP-03 | High | Critical | BM-05 |
| T-03 Unauthenticated XOR egress vault | Tampering, info disclosure | GAP-08 | Medium | High | BM-18 |
| T-04 MCP single shared bearer token | Spoofing, EoP | GAP-09 | High | Critical | BM-18 |
| T-05 Adapter defects unproven live | Tampering, DoS | GAP-01 | Medium | High | BM-01 |
| T-06 Epistemic planes not store-wide | Tampering | GAP-07 | Medium | High | BM-15 |
| T-07 No evaluation harness | Repudiation | GAP-43 | High (certain today) | High | BM-22 |
| T-08 String-built Gremlin / weak injection defence | Tampering, EoP | GAP-05 | Medium | High | BM-18/BM-07 |
| T-09 Agent memory lacks ACL/tenant/evidence/validity | Info disclosure, repudiation | GAP-34 | High | High | BM-04/BM-05 extended |
| T-10 Old root unauthenticated Ollama | EoP, tampering | GAP-36 | Medium | High | BM-14 |
| T-11 No licence allow-list in CI | Tampering (build posture) | GAP-19 | High | High | BM-20 |
| T-12 Supply-chain compromise (SBOM/signing absent) | Tampering | GAP-19/GAP-44 | Medium | Critical | BM-20 |

No threat in this table has a confirmed-zero residual risk today; every row's "detection hook" points at a benchmark that has not yet been run, per `15-VALIDATION-BENCHMARK-PLAN.md`'s own status line. This threat model will be re-issued, not amended in place, once BM-18/BM-19 produce a first real result.
