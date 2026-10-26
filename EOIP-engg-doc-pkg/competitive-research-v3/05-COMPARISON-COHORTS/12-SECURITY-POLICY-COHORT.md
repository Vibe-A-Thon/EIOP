# Cohort 12 - Security, policy, identity and supply chain

| Field | Value |
|---|---|
| Cohort ID | COH-12 |
| Workload class | Source-permission enforcement in retrieval and answers, tenant isolation, identity and SSO, secrets, audit and observability, software supply chain, LLM-specific threat guidance |
| Members | [keycloak](../04-COMPETITOR-DEEP-DIVES/C19-keycloak.md), [opa](../04-COMPETITOR-DEEP-DIVES/C19-opa.md), [rebac](../04-COMPETITOR-DEEP-DIVES/C19-rebac.md) (Zanzibar, OpenFGA, SpiceDB, Permify), [cedar-cerbos](../04-COMPETITOR-DEEP-DIVES/C19-cedar-cerbos.md), [vault-openbao](../04-COMPETITOR-DEEP-DIVES/C19-vault-openbao.md), [supply-chain](../04-COMPETITOR-DEEP-DIVES/C19-supply-chain.md) (Sigstore, SLSA, in-toto, Syft, Grype, Trivy), [opentelemetry](../04-COMPETITOR-DEEP-DIVES/C19-opentelemetry.md) (OTel, Prometheus, Grafana), [llm-threat-guidance](../04-COMPETITOR-DEEP-DIVES/C19-llm-threat-guidance.md) (OWASP LLM and Agentic lists, MITRE ATLAS) |
| Tier C | [C19-tier-c-records-V11](../04-COMPETITOR-DEEP-DIVES/C19-tier-c-records-V11.md): authorization-aware search (pre-filter, post-filter, ACL-embedded index) |
| Cross-referenced permission patterns | [C07-onyx](../04-COMPETITOR-DEEP-DIVES/C07-onyx.md), [C10-opensearch](../04-COMPETITOR-DEEP-DIVES/C10-opensearch.md), [C10-pgvector](../04-COMPETITOR-DEEP-DIVES/C10-pgvector.md), [C02-allegrograph](../04-COMPETITOR-DEEP-DIVES/C02-allegrograph.md), [C01-puppygraph](../04-COMPETITOR-DEEP-DIVES/C01-puppygraph.md), [C09-mcp](../04-COMPETITOR-DEEP-DIVES/C09-mcp.md), [C09-guardrails](../04-COMPETITOR-DEEP-DIVES/C09-guardrails.md) |
| Reference columns | HugeGraph, Neo4j, Neptune, EOIP @HEAD 896e06d (BL-IDs from `01-SYSTEM-BASELINE.md`, status from `01a-BASELINE-DELTA-HEAD.md`) |
| Date | 2026-10-26 |

## 1. Workload class and comparison basis

**Customer workloads.** (a) Search and answers that show a user only what the source system would show them; (b) multiple tenants on one deployment with zero cross-tenant leakage (a P0 defect by Master Prompt 4.3 item 9); (c) agents and MCP clients acting for a user; (d) secrets, keys and audit; (e) shipping a white-labelled product with a trustworthy supply chain.

**Why comparable.** These members are not substitutes for each other. They are the building blocks for one decision: where source permissions are enforced and by what. Section 2.1 therefore compares enforcement patterns; section 2.2 compares the supporting capabilities by member.

**Excluded.** Hosted-only services (Styra commercial layer, Cerbos Hub, Zep Cloud) are mentioned only where their state affects a dependency decision (CLAIM-opa-02/03, CLAIM-cc-04). OWASP and ATLAS are documents, not software; their licences are unverified, so no text is to be copied (CLAIM-lt-01..04).

**Evidence rules.** No member benchmarks were fetched in the C19 dives (performance sections say UNVERIFIED), so this cohort compares design and licence, not speed. EOIP status comes from `01a-BASELINE-DELTA-HEAD.md`, which supersedes the original baseline where they differ.

## 2. Capability comparison

### 2.1 Permission-enforcement patterns for retrieval (CAP-46)

| Pattern and example | How it works | Stage | Known failure modes | Evidence | Licence |
|---|---|---|---|---|---|
| Post-filter with live check (ReBAC `Check` loop) | Retrieve top-K, ask the PDP per hit, drop denied | after ranking | Recall collapse at high deny ratio; count and timing leaks | CLAIM-aas-05 (reasoned, confidence 0.5) | n/a |
| Pre-filter from reverse lookup (OpenFGA `ListObjects`, SpiceDB `LookupResources`) | Authorisation engine returns allowed IDs | before ranking | Defaults cap at 1,000 results; OpenFGA deadline 3 s; SpiceDB `lr3` experimental | CLAIM-rebac-05, -06; CLAIM-aas-02 | Apache-2.0 (rebac-02, -03) |
| Pre-filter from compiled policy (OPA partial evaluation; Cerbos `PlanResources`) | Policy with unknowns becomes a condition tree applied inside the store | before ranking | Adapter must map operators; OpenSearch target unconfirmed; conditions limited to adapter operators | CLAIM-opa-05, CLAIM-cc-04, CLAIM-aas-03 | Apache-2.0 |
| ACL-embedded index (Onyx) | `ExternalAccess` principal strings stored per chunk, `to_acl()` prefixed, empty means private; v5.0.0 query-time access filter behind shadow/enforce flag | in engine | Staleness on ACL change; group expansion explodes at index time (Leopard analogue) | CLAIM-onyx-07, -08; CLAIM-aas-01 | Permission sync is Enterprise Edition for 14 connectors (CLAIM-onyx-03); `ee` directories under a separate licence (CLAIM-onyx-02) |
| Engine DLS (OpenSearch; Elasticsearch) | Role query or attribute substitution applied by the engine | in engine | Read-only: writers can modify hidden documents; OR across roles widens access; no statement on DLS with kNN | CLAIM-opensearch-04; CLAIM-elasticsearch-04 | Apache-2.0 / Elastic licence choice; paid tier officially unstated |
| Engine row-level security (pgvector on PostgreSQL) | Default-deny policies per row | in engine | Owner, superuser and BYPASSRLS bypass; RI side channels; policy shape drives performance | CLAIM-pgvector-04 | PostgreSQL License |
| Graph and vector under one security filter (AllegroGraph) | Security filters shared by graph and vector data | in engine | Third-party source only; not independently verified | CLAIM-allegrograph-02, -03 | Commercial |
| Source-side row security with caller identity (PuppyGraph) | Pass identity to the relational source | at source | Engine not public; editions gate features | CLAIM-puppygraph-02, -03 | Closed engine |
| Tenant or collection RBAC only (Qdrant JWT, Weaviate, Milvus) | Role per collection or tenant | coarse | ACL is a caller-supplied filter convention | CLAIM-qdrant-08, CLAIM-weaviate-07, CLAIM-milvus-05 | Apache-2.0 / BSD-3 |

The tier C record's recommended hybrid (inference, confidence 0.5): index `acl_principals` on every chunk and fact for coarse engine-enforced filtering, then verify survivors with the native PDP at answer time using a revision token (CLAIM-aas-05).

### 2.2 Capabilities by member

| CAP | Keycloak | OPA | OpenFGA / SpiceDB | Cedar / Cerbos | Vault / OpenBao | Supply chain | OTel / Prometheus / Grafana | HugeGraph | Neo4j | Neptune | EOIP @HEAD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CAP-44 authn and SSO | native OIDC, SAML 2.0, token exchange, Organizations (keycloak-01) | absent | absent | absent | absent | n/a | n/a | optional auth, off unless configured (hugegraph-14, -32) | native; LDAP, Kerberos EE (neo4j-15) | IAM SigV4 required when enabled (neptune-07) | **Implemented, strengthened**: argon2id credentials, signed sessions, API tokens, deny-by-default route policy (BL-19, NB-04, NB-05); `authn/sso.py` live-unverified; **no SigV4 path to Neptune** (BL-04) |
| CAP-45 RBAC and ABAC | partial (keycloak dive) | native Rego (opa-04) | partial (rebac dive) | native (cc-02, cc-03) | policies in HCL | n/a | n/a | auth model with groups, targets, accesses (hugegraph-14) | EE RBAC with label, type, property, value privileges (neo4j-14) | IAM actions ReadDataViaQuery and others (neptune-09) | Implemented in `authz/core.py` (BL-19) |
| CAP-46 source ACL | absent (identity only) | partial via partial evaluation (opa-05) | native ReBAC (rebac-05, -06) | absent / partial via plans (cc-04) | n/a | n/a | n/a | absent | EE privileges, defence in depth only (neo4j-14) | finer control left to application (neptune-12) | **Partial**: `authz/pdp.py` and `derivation_acl.py` exist; applied only in the graph branch when `scope` is passed; no deployed caller passes it (BL-18, U-04, NB-17) |
| CAP-47 tenancy | partial, realms (keycloak dive) | n/a | partial (rebac dive) | n/a | n/a | n/a | n/a | graphspaces (hugegraph dive) | EE database per tenant (neo4j-13) | silo or pool models (neptune-32) | **Partial improved**: embedded layers per tenant (BL-20, NB-11); graph adapters tenant-blind; API-layer `NamedGraphStore` wrapper |
| CAP-48 audit integrity | n/a | decision logs (opa dive) | n/a | audit log with `cerbosCallId` (cc-04) | audit devices (vo dive) | n/a | absent: observability is not audit (ot dive) | unknown | unknown | unknown | Partial: audit sink separate from telemetry in `observability/truth.py`; library-level, mount unverified (BL-49) |
| CAP-49 injection defence | n/a | n/a | n/a | n/a | n/a | n/a | partial redaction (ot dive) | n/a | n/a | n/a | Partial: `PromptInjectionFence`, `models/guardrails.py`, regex `KnowledgeFirewall` (INV-grd-01); no executable red-team corpus |
| CAP-50/51 air-gap and egress | native self-host (CAP mapping in keycloak dive) | air-gap viable | air-gap viable | air-gap viable | Shamir unseal for air-gap | key-based signing plus mirrored DB, to be proven (sc dive) | no cloud dependency | n/a | n/a | managed only | Implemented gateway, kill switch, contract-term disable (BL-45) |
| Secrets | n/a | n/a | n/a | n/a | transit encryption, dynamic leases (vo-03) | n/a | n/a | n/a | n/a | KMS | **Weak**: `egress/vault.py:24-33` uses an unauthenticated XOR keystream; its own docstring says to replace it with AES-GCM via KMS (BL-45, U-17); per-tenant AES-256-GCM key exists in `tenancy/layers.py` (BL-20) |
| CAP-79 supply chain | n/a | n/a | n/a | n/a | n/a | native: Sigstore, SLSA 1.2, in-toto, Syft, Grype, Trivy (sc-01..07) | n/a | n/a | n/a | n/a | **Library-only**: `compliance/sbom.py` generates CycloneDX 1.5; no CI workflow calls it (NB-14) |
| CAP-75 observability | n/a | n/a | n/a | n/a | n/a | n/a | native (ot-01) | n/a | Prometheus metrics EE (neo4j dive) | n/a | Implemented metrics, JSON logs, optional OTel (BL-49) |

### 2.3 MCP and agent authentication (cross-reference C09-mcp)

| Aspect | MCP specification 2026-07-28 | Third-party servers | EOIP @HEAD |
|---|---|---|---|
| Authorization | Optional; when used, protected-resource metadata (RFC 9728) and resource indicators (RFC 8707) MUST; servers MUST validate audience and MUST NOT accept other tokens (mcp-06) | FalkorDB MCP: bearer key, empty disables, read-only by default but overridable (mcp-10); Neptune MCP: not read-only, scope via IAM (mcp-12); mcp-neo4j: Labs, runs read/write Cypher (mcp-09) | **One shared static bootstrap token**; every caller acts as that principal; no per-user identity or tenant propagates (BL-47, mcp-17) |
| Token handling | Token passthrough forbidden; bind handles to principal (mcp-08) | n/a | Each tool forwards the shared token to REST |
| Tool metadata | Annotations (`readOnlyHint` default false) untrusted unless from trusted servers (mcp-03) | n/a | 18 tools, **no annotations** (mcp-17) |
| Separate tool contract | n/a | n/a | `tools_contract/mcp_server.py` with identity-spoof checks exists but is **not mounted**, and constructs `ActionEngine(write_back_enabled=True)` (BL-47, NB-03) |

## 3. Operational and licensing comparison

| Member | Licence | Redistribution / OEM trigger | One-node footprint | Air-gap | Maintenance |
|---|---|---|---|---|---|
| Keycloak | Apache-2.0 | None; Red Hat build is optional commercial | JVM plus RDBMS; heavy for tiny deployments (keycloak dive; 1 to 2 GB is a hypothesis) | Viable; check theme and font CDN use | 26.8.1 is mostly security fixes (keycloak-02); CNCF incubating |
| OPA | Apache-2.0 | None | Single Go binary; memory about 130 MB per 10k rules, 1.1 GB per 100k (opa-04) | Yes | v1.21.4; CNCF graduated; Styra founders moved to Apple and Styra web presence failed in 2026 (opa-02, -03) |
| OpenFGA / SpiceDB | Apache-2.0 | None | Go plus PostgreSQL or SQLite; second stateful service | Yes | OpenFGA CNCF incubating 2025-10-28; SpiceDB v1.57.0 |
| **Permify** | **AGPL-3.0**; acquired by FusionAuth (rebac-04) | **Reject as embedded dependency** | n/a | n/a | v1.7.5 |
| Cedar / Cerbos | Apache-2.0 core | Cerbos open-core boundary to review; Cedar is CNCF Sandbox (cc-01) | Cedar in-process; Cerbos single binary | Yes | Cerbos v0.57.0 |
| **Vault** | **BUSL 1.1**, IBM licensor; v2.2.1 (vo-01, -02) | **Do not embed** in a competing OEM product | Go binary; unseal ceremony | Shamir unseal | Active |
| OpenBao | MPL-2.0 (file-level copyleft) | Customer-deployed integration, legal review before bundling (vo-03, -04) | Go binary | Yes | v2.7.1 |
| Sigstore / SLSA / in-toto / Syft / Grype / Trivy | Apache-2.0 | None identified | CLIs | Key-based signing and mirrored DB, to be proven | **Trivy compromised March 2026** (sc-05) |
| OTel / Prometheus | Permissive | None | Collector adds one hop | Yes | Graduated CNCF projects (ot-01) |
| **Grafana, Loki, Tempo** | **AGPL-3.0-only** since 2021-04-20 (ot-02, -03) | **Ship dashboards as JSON, leave Grafana customer-installed** | Optional container | Yes | v13.2.4 |
| OWASP / ATLAS | Unverified | Do not copy text | n/a | Trivial | 2025 list official; "2026" edition and ATLAS version naming conflict between sources (lt-01, -02, -04) |
| Neo4j CE (reference) | GPLv3; EE privileges and multi-DB commercial (neo4j dives) | GPL duties if bundled | n/a | n/a | n/a |

## 4. Performance evidence

None of the nine C19 dives collected comparable performance figures. The only numbers are:

| Figure | Source | Class | Use |
|---|---|---|---|
| Keycloak: 1M users at 300 requests/s tested; 30M users, 1,000 logins/s, 20,000 refreshes/s on six pods of 40 vCPU, 8 GB, Aurora PostgreSQL | keycloak-03 | Vendor documentation | Scale-out only; no one-node figure |
| Zanzibar: over 2 trillion tuples, over 10M QPS, Check p50/p95/p99/p99.9 about 3/11/20/93 ms | rebac-01 | Peer-reviewed, Google scale | Not transferable to open-source engines |
| OPA memory: 130 MB per 10k rules, 1.1 GB per 100k | opa-04 | Vendor documentation | Sizing only |

No latency or recall measurement exists for ACL-filtered retrieval in any candidate, nor for EOIP's own `can_read` evaluator at scale (U-06). Tests such as the permission-leakage test J5 and tenant test J13 are PROPOSED, not run.

## 5. Findings

1. **EOIP's P0 gap is wiring, not missing code.** The evaluator exists (`authz/pdp.py:107` `can_read`, `derivation_acl.py:167`), but `retrieval/service.py:575` applies it only in the graph traversal branch when `scope` is passed, and `apps/api/extended.py:906-913`, `/api/v1/rag`, `agents/governed.py:250` and MCP do not pass it; keyword, vector and hybrid candidates are filtered by tenant ownership only (BL-18, U-04). Falsifier: a J5 test showing zero leakage on all four paths.
2. **No retrieval engine in the cohort enforces source ACLs by itself; the strongest primitives (DLS, RLS, security filters) each leave a gap.** DLS is read-only and OR-combined across roles (opensearch-04); RLS is bypassable by owners and superusers (pgvector-04); AllegroGraph's claim is third-party only (allegrograph-02). EOIP must own the policy decision and treat engines as defence in depth.
3. **Post-filtering alone is not acceptable; pre-filtering alone is incomplete.** Post-filter collapses recall at high deny ratios; reverse lookups cap at 1,000 by default (OpenFGA, SpiceDB) (aas-02, rebac-06); ACL-embedded indexes go stale. The three-way trade-off (aas-05) favours the hybrid in section 2.1, with a revision token so revocation beats index staleness (STR-rebac-01).
4. **The MCP surface violates the specification's own audience and passthrough rules.** One static token, no principal, no tool annotations, while the 2026-07-28 spec requires audience validation and forbids token passthrough (mcp-06, mcp-08, mcp-17). The unmounted `tools_contract/mcp_server.py` is a better contract but also instantiates an `ActionEngine` with write-back enabled (BL-47).
5. **The egress vault cipher is the weakest cryptographic component in the repository.** XOR with a SHA-256 counter keystream, no authentication tag, malleable (`egress/vault.py:24-33,68,84`); AES-GCM is already implemented for tenant data keys (BL-20) and `cryptography` is available in the local environment (01a), so replacing it needs no new dependency (U-17, STR-vo-01).
6. **Three licence blockers are confirmed: Vault (BUSL 1.1), Grafana (AGPL-3.0), Permify (AGPL-3.0).** Elasticsearch (AGPL/SSPL/ELv2) is a fourth from cohort 10 (elasticsearch-02), and Onyx's permission sync is Enterprise-only (onyx-03). All have permissive alternatives in this cohort: OpenBao as a customer-deployed option, OpenFGA or SpiceDB, Prometheus plus JSON dashboards, OpenSearch.
7. **The supply-chain tooling itself is an attack surface.** The March 2026 Trivy compromise affected the scanner action and binary (sc-05); EOIP has an SBOM generator that no CI step calls (NB-14). Pin scanners by digest, verify signatures, run without secrets (INV-sc-01).
8. **Identity is not the weak point; enforcement downstream of identity is.** EOIP's authn was strengthened (argon2id, sessions, route policy) while keycloak, as an optional IdP, adds only credential lifecycle and token exchange and is heavy for one node (keycloak dive; INV-keycloak-01). Keycloak is a compose profile candidate, not a core dependency.
9. **Tenant isolation is enforced for embedded layers and the API-layer graph wrapper but not in any graph adapter.** Zero tenant handling in HugeGraph, Neo4j, Neptune, Fuseki adapters (BL-20). Neo4j's database-per-tenant is EE-only (neo4j-13), HugeGraph auth is optional (hugegraph-14), Neptune has no per-tenant primitive beyond clusters or a tenant property (neptune-12, -32), so adapter-level enforcement must be EOIP's.
10. **No executable LLM-threat conformance exists in the cohort.** OWASP and ATLAS describe risks only; their editions conflict between sources (lt dives). The test corpus (injected connector documents, cross-tenant probes, tool-abuse prompts) must be built (INV-lt-02) and tagged with ATLAS technique IDs (STR-lt-02).

## 6. Implications for EOIP

| CAP | Parity needed (STR-IDs) | Exploitable weakness (INV-IDs) | Decision | Candidate gap statement |
|---|---|---|---|---|
| CAP-46 retrieval ACL | STR-onyx-01 (per-chunk principals), STR-onyx-02 (shadow/enforce rollout), STR-rebac-01 (revision token), STR-rebac-02 (reverse lookup when allowed set under 1,000), STR-cc-01 and STR-opa-01 (compiled filters), STR-allegrograph-01 | INV-onyx-01 (permission sync gated to Enterprise), INV-rebac-01 (lookup truncation), INV-pgvector-01 | **BUILD, P0**: ACL pre-filter in keyword, vector, hybrid and graph stages plus PDP recheck at answer time; **INTEGRATE** a ReBAC engine for group inheritance; **EXPERIMENT** with compiled filters | Wire `scope` and ACL principals through every deployed retrieval path, and prove it with J5 and shadow mode before enforcing. |
| CAP-46 in the agent path | STR-lt-01 (ACL filter precedes ranking and generation) | INV-hipporag-02, INV-msgraphrag-02 (propagation and summaries cross ACL groups) | **BUILD, P0** | Governed agents and MCP must pass principal and tenant; `agents/governed.py:250` currently passes neither. |
| CAP-47 tenancy | STR-qdrant-02, STR-weaviate-01 (cohort 10); STR-neo4j-07 (database per tenant, EE) | Adapters tenant-blind | **BUILD, P0**: adapter-level tenant graph test J13 | Zero cross-tenant leakage across HugeGraph, Neo4j, Neptune and RDF adapters, not only the API wrapper. |
| CAP-59 MCP auth | STR-mcp-02 (audience binding, scope step-up), STR-mcp-03 (annotations), STR-keycloak-02 (token exchange) | INV-mcp-02 (confused deputy via single shared token), INV-mcp-01 (tool poisoning), INV-mcp-03 (raw-query servers; EOIP QueryPlan templates are the inversion) | **BUILD, P0**: resource-server mode, per-user tokens, annotate all 18 tools; mount or retire `tools_contract/mcp_server.py` | MCP front door must carry a per-user principal and tenant, and reject tokens for other audiences. |
| Secrets | STR-vo-01 (Transit via a `SecretsPort`), STR-vo-02 (leased credentials) | INV-vo-01 (BUSL), INV-vo-02 | **BUILD** an AES-GCM default behind `SecretsPort`; **INTEGRATE** OpenBao as customer-deployed; **REJECT** Vault bundling | Replace the XOR vault cipher now; no new service required. |
| CAP-48 audit | CLAIM-cc-04 (`cerbosCallId` audit), OPA decision logs (opa dive); no STR card | Observability is not audit (ot dive) | **BUILD, P1** | Tamper-evident audit separate from telemetry; verify the mount of `observability/truth.py`. |
| CAP-79 supply chain | STR-sc-01 (Syft/Grype, OpenVEX), STR-sc-02 (cosign, in-toto, SLSA) | INV-sc-01 (scanner attack surface), INV-sc-02 (air-gap gap) | **INTEGRATE, P1**: call `compliance/sbom.py` from CI, sign releases key-based first | SBOM generation exists but is not in CI (NB-14). |
| CAP-75/77 observability and licence | STR-ot-01 (Collector redaction), STR-ot-02 (rules as code) | INV-ot-01 (Grafana AGPL), INV-ot-02 (labels leak tenant data) | **REUSE** Prometheus and OTel; **REJECT** bundling Grafana | Redact tenant and ACL attributes before export. |
| CAP-49 injection defence | STR-grd-01 (rails at input, retrieval, execution, output), STR-lt-02 (ATLAS-tagged tests) | INV-grd-01 (regex firewall brittle), INV-lt-02 (no conformance) | **BUILD, P1**: red-team corpus; optional customer-supplied classifier (Llama Prompt Guard is gated, grd-04) | Build `security/redteam` and gate releases on it. |
| CAP-44 identity | STR-keycloak-01 | INV-keycloak-01 (footprint) | **INTEGRATE** as optional compose profile; keep built-in OIDC for one node | Add Neptune SigV4 (BL-04, U-03) as an opt-in extra. |

## 7. Open questions

1. Does OpenSearch DLS act before or after ANN candidate generation (INV-opensearch-02)? Required before relying on DLS for vector search.
2. Which Cerbos and SpiceDB features are open-core only? Neither dive confirmed (cc, rebac dives).
3. Can OpenBao Transit be deployed in a one-node profile within memory limits (INV-vo-02)?
4. Is the official "OWASP LLM Top 10 2026" real, and under which licence may its text be reused (lt-02)?
5. Who owns the decision to mount or retire `tools_contract/mcp_server.py` and its write-back-enabled `ActionEngine` (U-14)?
6. How should the revision token be defined across tenants, sources and the PDP policy epoch so that revocation always beats index staleness?
