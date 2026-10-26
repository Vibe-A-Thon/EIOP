# EPIC-CRARCPCCAGGCC-CI: CRAr_cpccaggcc-requirements.md · needs_ci_l3

*Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close.* 45 tasks, ~74.0 h, priorities {'P0': 33, 'P1': 11, 'P2': 1}. Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`.

**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.

## RT-CRA-003 [P0] CRA-003: Identity, Scope and Derived-Data Authorization

- **Source:** `CRAr_cpccaggcc-requirements.md:555-596` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-003; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-003. Identity, Scope and Derived-Data Authorization

*Aggregated title: Zero-Trust Principal, Tenancy & Derivation ACL Authorization*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/002 | B (Safe platform) | M1 | G15, G16 | — | — | INV-05, INV-19, INV-20, INV-23, INV-24, INV-39, INV-43 | X-11 | — |

**Base statement:** Priority P0. Depends on CRA-001/002. Source G15/G16 and INV-19/20/24/39/43.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-003.1** `[CRAr]` Implement trusted principal/session/IdP integration, memberships and tenant/workspace grants, preserving existing approved authentication contracts. Distinguish deployment-token access from a production user session.
- **CRA-003.2** `[CRAr]` Enforce deny-by-default authorization at every canonical read/write, traversal, count, search/vector candidate, semantic job, event, report/export, raw download, administration and action boundary.
- **CRA-003.3** `[CRAr]` Compose source ACLs and classifications on every derivative. Derived facts and evidence cannot be visible merely because their final subject is visible. Support alternate permitted proofs explicitly; never reveal a restricted proof.
- **CRA-003.4** `[CRAr]` Bind caches, drafts, saved views, cursors and local state to authorized scope and policy epoch. Scope switching/disconnect aborts pending work and discards late results. Migrate ambiguous legacy browser data without inferring ownership.
- **CRA-003.5** `[CRAr]` Propagate revocation/ACL changes through every index, cache, inference, job and stream; deny unsafe stale access while projections lag. Reauthorize long-running downloads/jobs/actions before sensitive delivery/commit.
- **CRA-003.6** `[CRAr]` Test same-backend tenants with identical external IDs, malicious tenant fields, unauthorized graph names and cross-workspace membership changes. Audit defaults such as global/system scopes; do not assume names exempt isolation safely.
- **CRA-003.7** `[AGG]` `TrustedScope` (fields in section 6) is derived only server-side from a validated session, JWT or mTLS identity. Tenant, workspace, roles and ACLs in request bodies, connector payloads, LLM output or browser state are ignored for authorization.
- **CRA-003.8** `[RES]` Derived-fact visibility rule (resolves X-11): for one justification, a derived fact is visible only if the principal satisfies the ACL of ever
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-003

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001/002. Source G15/G16 and INV-19/20/24/39/43.
- [ ] CRA-003.1 [CRAr] Implement trusted principal/session/IdP integration, memberships and tenant/workspace grants, preserving existing approved authentication contracts. Distinguish deployment-token access from a production user session
- [ ] CRA-003.2 [CRAr] Enforce deny-by-default authorization at every canonical read/write, traversal, count, search/vector candidate, semantic job, event, report/export, raw download, administration and action boundary
- [ ] CRA-003.3 [CRAr] Compose source ACLs and classifications on every derivative. Derived facts and evidence cannot be visible merely because their final subject is visible. Support alternate permitted proofs explicitly; never reveal a restricted proof
- [ ] CRA-003.4 [CRAr] Bind caches, drafts, saved views, cursors and local state to authorized scope and policy epoch. Scope switching/disconnect aborts pending work and discards late results. Migrate ambiguous legacy browser data without inferring ownership
- [ ] CRA-003.5 [CRAr] Propagate revocation/ACL changes through every index, cache, inference, job and stream; deny unsafe stale access while projections lag. Reauthorize long-running downloads/jobs/actions before sensitive delivery/commit
- [ ] CRA-003.6 [CRAr] Test same-backend tenants with identical external IDs, malicious tenant fields, unauthorized graph names and cross-workspace membership changes. Audit defaults such as global/system scopes; do not assume names exempt isolation safely
- [ ] CRA-003.7 [AGG] TrustedScope (fields in section 6) is derived only server-side from a validated session, JWT or mTLS identity. Tenant, workspace, roles and ACLs in request bodies, connector payloads, LLM output or browser state are ignored for authorization
- [ ] CRA-003.8 [RES] Derived-fact visibility rule (resolves X-11): for one justification, a derived fact is visible only if the principal satisfies the ACL of every premise (intersection). With several justifications it is visible if at least one complete justification is fully visible. Explanations show only a fully visible justification. Classification is the maximum classification of the justificati
- [ ] CRA-003.9 [AGG] Each tenant has a monotonically increasing policyepoch, incremented on any ACL, membership, classification or policy change. Caches, cursors, vector results, inferred facts and query results carry the epoch they were computed under; reads under a newer epoch must re-filter or deny. Serving a stale-epoch result without re-check is prohibited
- [ ] CRA-003.10 [AGG] Scope filters are injected into the typed query plan before execution for SPARQL, SQL, Cypher, EOQL/EQL/OSQL and vector search. User-supplied GRAPH/FROM/named-graph or index selection outside the caller's scope is rejected
- [ ] CRA-003.11 [RES] Probing another tenant's identifier returns a response indistinguishable from a non-existent resource (HTTP 404 with the same body shape and timing class), so existence is not leaked
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/authz/pdp.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/authz/pdp.py#L1-L1), [`scripts/build_master_suite.py:244`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L244-L244), [`scripts/enhance_master_suite.py:167`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L167-L167), [`scripts/patch_suite_and_dashboard.py:33`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L33-L33), [`scripts/update_matrix_caps.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L24-L24), [`scripts/verify_22_caps.py:134`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/verify_22_caps.py#L134-L134)
- tests: `scripts/test_cap_enrichment.py:113`, `scripts/test_master_caps_enrichment.py:127`, `tests/security/test_multi_tenant_isolation_hardened.py:1`, `tests/security/test_tenancy_and_derivation_acls.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-004 [P0] CRA-004: Connection Factory and Conformance SDK

- **Source:** `CRAr_cpccaggcc-requirements.md:599-642` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-004; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-004. Connection Factory and Conformance SDK

*Aggregated title: Universal Connection Factory & Conformance SDK*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | C (First acquisition slice) | M2 | F5, G07, G08 | ONT-005 | I6, I8 | INV-42, INV-43 | X-12 | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Source G07/G08 and INV-27/31/42/43/45. Investigate existing `connectors/factory.py`, base, registry and source contracts.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-004.1** `[CRAr]` Extend the existing factory with explicit per-capability descriptors: discover, baseline, poll, webhook, CDC, ACL, deletion, attachment, lineage, write-back, resume and health. State supported resource and API versions.
- **CRA-004.2** `[CRAr]` Validate configuration/secret references before instantiation. Do not swallow specialization failures and silently switch to a generic endpoint. Fallback requires an explicit configured policy and visible capability downgrade.
- **CRA-004.3** `[CRAr]` Provide generic protocol adapters for REST/OpenAPI, GraphQL, SOAP, JDBC/ODBC, SFTP/files/object storage and event/CDC sources through isolated qualified drivers. Unsupported protocols return actionable unavailable states.
- **CRA-004.4** `[CRAr]` Implement conformance fixtures and a sandbox runner covering auth, pagination, rate limits, retry, rename/delete, ACL change, ordering, duplicate events, cursor durability, attachment and resource budgets.
- **CRA-004.5** `[CRAr]` Store provider version/config digest and qualification receipts with each source instance. Successful connection/authentication is not baseline sync certification, and sync is not write-back approval.
- **CRA-004.6** `[CRAr]` Provide authoring templates, contract validation and mock fixtures for a new custom source, followed by separate real-system qualification. Unknown business products must not be advertised as fully supported via `api/entities` defaults.
- **CRA-004.7** `[AGG]` `ConnectorDescriptor` fields: `provider_id`, `display_name`, `version`, `supported_product_versions`, `capabilities` (discovery, baseline_sync, polling_sync, webhook_push, cdc_stream, acl_preservation, attachments, delete, lineage, write_back, resumable_cursor, health), `auth_schemes` (oauth2, bearer, basic, mtls, app_installation), `config_schema` (JSON Schema), `default_concurrency_lim
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-004

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/003. Source G07/G08 and INV-27/31/42/43/45. Investigate existing connectors/factory.py, base, registry and source contracts.
- [ ] CRA-004.1 [CRAr] Extend the existing factory with explicit per-capability descriptors: discover, baseline, poll, webhook, CDC, ACL, deletion, attachment, lineage, write-back, resume and health. State supported resource and API versions
- [ ] CRA-004.2 [CRAr] Validate configuration/secret references before instantiation. Do not swallow specialization failures and silently switch to a generic endpoint. Fallback requires an explicit configured policy and visible capability downgrade
- [ ] CRA-004.3 [CRAr] Provide generic protocol adapters for REST/OpenAPI, GraphQL, SOAP, JDBC/ODBC, SFTP/files/object storage and event/CDC sources through isolated qualified drivers. Unsupported protocols return actionable unavailable states
- [ ] CRA-004.4 [CRAr] Implement conformance fixtures and a sandbox runner covering auth, pagination, rate limits, retry, rename/delete, ACL change, ordering, duplicate events, cursor durability, attachment and resource budgets
- [ ] CRA-004.5 [CRAr] Store provider version/config digest and qualification receipts with each source instance. Successful connection/authentication is not baseline sync certification, and sync is not write-back approval
- [ ] CRA-004.6 [CRAr] Provide authoring templates, contract validation and mock fixtures for a new custom source, followed by separate real-system qualification. Unknown business products must not be advertised as fully supported via api/entities defaults
- [ ] CRA-004.7 [AGG] ConnectorDescriptor fields: providerid, displayname, version, supportedproductversions, capabilities (discovery, baselinesync, pollingsync, webhookpush, cdcstream, aclpreservation, attachments, delete, lineage, writeback, resumablecursor, health), authschemes (oauth2, bearer, basic, mtls, appinstallation), configschema (JSON Schema), defaultconcurrencylimit (2), ratelimitperminute 
- [ ] CRA-004.8 [AGG] Per-source-instance token-bucket rate limiter honouring Retry-After and vendor rate-limit headers; HTTP 429/503 trigger exponential backoff with full jitter (base 1 s, cap 300 s) without exceeding the configured budget
- [ ] CRA-004.9 [AGG] SDK: abstract BaseConnector with discover(), baseline(cursor), poll(cursor), handlewebhook(event), fetchacl(resource), fetchattachment(ref), write(intent) (only when writeback is declared) and health(). Third-party connectors are discovered through the Python entry-point group eoip.connectors and must carry a signed manifest (CRA-002)
- [ ] CRA-004.10 [OCA] Inventory all 38 existing connector modules and connectors/factory.py (8 application categories) into a connector qualification table (provider, versions, capability states, mapping location, receipts). Extend these; do not create a parallel factory
- [ ] CRA-004.11 [CRA] G07 closure: remove the broad exception handler that converts specialization errors into a generic REST fallback. Fallback happens only when fallbackpolicy: explicit is configured, and then the capability downgrade is surfaced in API, UI and telemetry
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/custom_system.py:6`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/custom_system.py#L6-L6), [`packages/eoip/connectors/descriptor.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/descriptor.py#L3-L3), [`packages/eoip/connectors/errors.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/errors.py#L3-L3)
- tests: `tests/connectors/test_connector_factory_acceptance.py:4`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-005 [P0] CRA-005: Work-Tracking and Test-System Adapters

- **Source:** `CRAr_cpccaggcc-requirements.md:643-680` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-005; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-005. Work-Tracking and Test-System Adapters

*Aggregated title: Issue Tracking & Agile Connectors (Jira & Rally)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011 | G (Named sources, media and actions) | M2 | G08 | ONT-005 | — | — | X-12 | H-11 |

**Base statement:** Priority P1. Depends on CRA-004/010/011. Sources Jira, Rally and qTest; source requirement attachment line 123.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-005.1** `[CRAr]` Qualify Jira Cloud and separately selected Data Center versions for projects, issues, links, comments, custom fields and attachments. Retrieve permission context with authorized scopes and preserve issue/source revision identity.
- **CRA-005.2** `[CRAr]` Qualify Rally workspace/project resource types and hierarchy. Preserve artifact relationships and version/cursor semantics; configuration must select actual API version and resource scope.
- **CRA-005.3** `[CRAr]` Qualify qTest projects, tests, runs/results and defect associations. Distinguish test definitions from execution results and preserve updates/deletes and project authorization.
- **CRA-005.4** `[CRAr]` Research the official API/version/auth/scopes and acquire licensed test access for each product. Store a compatibility manifest and vendor-response fixtures with secrets removed.
- **CRA-005.5** `[CRAr]` Demonstrate bounded baseline and incremental acquisition, pagination, rate limits, ACL-only change, deleted/renamed items, attachments and replay. A generic Agile profile cannot substitute for actual vendor semantics.
- **CRA-005.6** `[AGG]` Jira: Cloud REST API v3 and a separately pinned Data Center REST version; webhooks for issue created/updated/deleted and comment events; incremental JQL `updated >= watermark` with an overlap window (default 5 min) and deduplication by issue ID plus updated timestamp. Map Issue, Project, Sprint, Component, Version, Worklog, User and issue links (blocks, is blocked by, relates to, duplicates, clones) to a reviewed `jira:` vocabulary package; issue security levels and project permission schemes populate `acl_vector`; attachments go to the raw vault.
- **CRA-005.7** `[AGG]` Rally: WSAPI v2.0; HierarchicalRequirement, Defect, Task, Iteration, Release, Milestone and PortfolioItem types; preserve parent/child epic hierarchies, defect associations and workspace/project scope.
- **CRA-005
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-005

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-004/010/011. Sources Jira, Rally and qTest; source requirement attachment line 123.
- [ ] CRA-005.1 [CRAr] Qualify Jira Cloud and separately selected Data Center versions for projects, issues, links, comments, custom fields and attachments. Retrieve permission context with authorized scopes and preserve issue/source revision identity
- [ ] CRA-005.2 [CRAr] Qualify Rally workspace/project resource types and hierarchy. Preserve artifact relationships and version/cursor semantics; configuration must select actual API version and resource scope
- [ ] CRA-005.3 [CRAr] Qualify qTest projects, tests, runs/results and defect associations. Distinguish test definitions from execution results and preserve updates/deletes and project authorization
- [ ] CRA-005.4 [CRAr] Research the official API/version/auth/scopes and acquire licensed test access for each product. Store a compatibility manifest and vendor-response fixtures with secrets removed
- [ ] CRA-005.5 [CRAr] Demonstrate bounded baseline and incremental acquisition, pagination, rate limits, ACL-only change, deleted/renamed items, attachments and replay. A generic Agile profile cannot substitute for actual vendor semantics
- [ ] CRA-005.6 [AGG] Jira: Cloud REST API v3 and a separately pinned Data Center REST version; webhooks for issue created/updated/deleted and comment events; incremental JQL updated >= watermark with an overlap window (default 5 min) and deduplication by issue ID plus updated timestamp. Map Issue, Project, Sprint, Component, Version, Worklog, User and issue links (blocks, is blocked by, relates to, dup
- [ ] CRA-005.7 [AGG] Rally: WSAPI v2.0; HierarchicalRequirement, Defect, Task, Iteration, Release, Milestone and PortfolioItem types; preserve parent/child epic hierarchies, defect associations and workspace/project scope
- [ ] CRA-005.8 [AGG] qTest: projects, test cases, test runs, executions/results and defect links; qtest:verifiesRequirement links to Jira issues only when the identifier resolves to an ingested Jira resource; definitions and executions remain distinct entity types
- [ ] CRA-005.9 [OCA] All three adapters express payload-to-ontology mapping in CML (CRA-017), with a parity test proving the CML output equals the previous hand-coded mapping output on a fixture corpus
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/jira.py:513`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/jira.py#L513-L513), [`packages/eoip/connectors/qtest.py:114`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/qtest.py#L114-L114)
- tests: `tests/acceptance/test_work_tracking_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-006 [P0] CRA-006: Wiki, Content, Chat and Document Repositories

- **Source:** `CRAr_cpccaggcc-requirements.md:681-717` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-006; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-006. Wiki, Content, Chat and Document Repositories

*Aggregated title: Knowledge & Content Repository Connectors (Confluence, Wiki, Slack & Documentum)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011/012/013 | G (Named sources, media and actions) | M2 | G08 | — | — | — | X-12 | H-11, H-13 |

**Base statement:** Priority P1. Depends on CRA-004/010/011/012/013. Sources wiki, Confluence, Slack and Documentum.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-006.1** `[CRAr]` Provide generic wiki acquisition plus Confluence-specific spaces, pages, versions, links, comments and attachments with inherited/restricted-page permissions and body/macro fidelity diagnostics.
- **CRA-006.2** `[CRAr]` Qualify Slack through approved application scopes/events/history APIs. Preserve conversation membership, message/file edits/deletes, threads, pagination and rate limits. Private/direct messages are excluded by default unless explicitly authorized and legally permitted.
- **CRA-006.3** `[CRAr]` Qualify Documentum's licensed selected API for object IDs, versions/renditions, folders, relationships, ACL inheritance, checkout and retention/legal holds. Do not reduce document identity to filename or URL.
- **CRA-006.4** `[CRAr]` Preserve message/document part and attachment provenance through nested parsing. Redact restricted content before indexing or invoking external providers. Synchronize permissions independently of content changes.
- **CRA-006.5** `[CRAr]` Display unsupported macros/renditions, inaccessible content and partial crawl honestly; do not fabricate plain-text equivalents or claim all wiki products share a single API.
- **CRA-006.6** `[AGG]` Confluence and generic wiki: CQL plus REST for Space, Page, BlogPost, Comment, Attachment and Version; page tree (`wiki:childOf`), links and mentions; space permissions and page-level view/edit restrictions populate `acl_vector`; embedded attachments and macros go to multiformat decoding with fidelity diagnostics.
- **CRA-006.7** `[AGG]` Documentum: Documentum REST Services and CMIS at pinned licensed versions; Cabinet, Folder, sysobject, rendition and version chain; Documentum ACLs, domain groups, folder inheritance, retention and legal-hold flags.
- **CRA-006.8** `[AGG]` Slack: Events API (`message.channels`, edits, deletes, `file_shared`) plus `conversations.history`/`replies`; 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-006

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-004/010/011/012/013. Sources wiki, Confluence, Slack and Documentum.
- [ ] CRA-006.1 [CRAr] Provide generic wiki acquisition plus Confluence-specific spaces, pages, versions, links, comments and attachments with inherited/restricted-page permissions and body/macro fidelity diagnostics
- [ ] CRA-006.2 [CRAr] Qualify Slack through approved application scopes/events/history APIs. Preserve conversation membership, message/file edits/deletes, threads, pagination and rate limits. Private/direct messages are excluded by default unless explicitly authorized and legally permitted
- [ ] CRA-006.3 [CRAr] Qualify Documentum's licensed selected API for object IDs, versions/renditions, folders, relationships, ACL inheritance, checkout and retention/legal holds. Do not reduce document identity to filename or URL
- [ ] CRA-006.4 [CRAr] Preserve message/document part and attachment provenance through nested parsing. Redact restricted content before indexing or invoking external providers. Synchronize permissions independently of content changes
- [ ] CRA-006.5 [CRAr] Display unsupported macros/renditions, inaccessible content and partial crawl honestly; do not fabricate plain-text equivalents or claim all wiki products share a single API
- [ ] CRA-006.6 [AGG] Confluence and generic wiki: CQL plus REST for Space, Page, BlogPost, Comment, Attachment and Version; page tree (wiki:childOf), links and mentions; space permissions and page-level view/edit restrictions populate aclvector; embedded attachments and macros go to multiformat decoding with fidelity diagnostics
- [ ] CRA-006.7 [AGG] Documentum: Documentum REST Services and CMIS at pinned licensed versions; Cabinet, Folder, sysobject, rendition and version chain; Documentum ACLs, domain groups, folder inheritance, retention and legal-hold flags
- [ ] CRA-006.8 [AGG] Slack: Events API (message.channels, edits, deletes, fileshared) plus conversations.history/replies; private channels and direct messages are blocked by default and can be enabled only with configuration plus a recorded legal/compliance approval reference; entity mentions are linked through CRA-023 as proposals
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/confluence.py:188`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/confluence.py#L188-L188), [`packages/eoip/connectors/documentum.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/documentum.py#L1-L1), [`packages/eoip/connectors/slack.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/slack.py#L1-L1)
- tests: `tests/acceptance/test_content_chat_documents_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-007 [P0] CRA-007: Code, Build, Artifact and API-Portal Adapters

- **Source:** `CRAr_cpccaggcc-requirements.md:718-755` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-007; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-007. Code, Build, Artifact and API-Portal Adapters

*Aggregated title: Code, Pipeline & Artifact Connectors (GitHub, GitLab, Artifactory & API Portal)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011 | G (Named sources, media and actions) | M2 | G08 | — | — | — | X-12, X-13 | H-07, H-11 |

**Base statement:** Priority P1. Depends on CRA-004/010/011. Sources GitHub, GitLab, Artifactory and API Portal.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-007.1** `[CRAr]` Qualify GitHub/GitLab selected editions for repository/project identity, commits/branches, pull/merge requests, issues, CI metadata and permitted artifacts. Preserve immutable commit references and moving-branch observations separately.
- **CRA-007.2** `[CRAr]` Support source-native app/project/repository authorization, installation scope, signed webhook verification, cursor/rate-limit behavior and rename/delete/fork semantics.
- **CRA-007.3** `[CRAr]` Qualify Artifactory repository/build/artifact metadata, checksum identity and authorized content, including promotion/deletion and repository ACLs. Never extract/store credentials from build metadata.
- **CRA-007.4** `[CRAr]` Treat API Portal as a configurable provider family until its product/API is identified. Support governed OpenAPI/schema/documentation ingestion, API/version relationships and approved discovery without pretending a universal portal endpoint exists.
- **CRA-007.5** `[CRAr]` Integrate code/document/schema parsing with provenance to commit/artifact/version and explicit language/format capability. Reject unsupported binaries and untrusted executable content.
- **CRA-007.6** `[AGG]` GitHub (REST plus GraphQL API v4) and GitLab (REST v4/GraphQL): Repository, Branch, Commit, Pull/Merge Request, Issue, Workflow/Pipeline run, Release; relations `git:modifiesFile`, `git:authoredBy`, `git:mergesInto`, `git:referencesIssue`; repository visibility (public/internal/private) populates `acl_vector`.
- **CRA-007.7** `[AGG]` Cross-system issue references: extract issue keys from commit messages/PR titles with a configurable pattern (default `\b[A-Z][A-Z0-9_]+-\d+\b`) restricted to an allowlist of project keys; each match becomes a proposed link with an evidence locator (message span) and is asserted only when the key resolves to an ingested issue.
- **CRA-007.8** `[AGG]` Artifactory: AQL plus storag
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-007

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-004/010/011. Sources GitHub, GitLab, Artifactory and API Portal.
- [ ] CRA-007.1 [CRAr] Qualify GitHub/GitLab selected editions for repository/project identity, commits/branches, pull/merge requests, issues, CI metadata and permitted artifacts. Preserve immutable commit references and moving-branch observations separately
- [ ] CRA-007.3 [CRAr] Qualify Artifactory repository/build/artifact metadata, checksum identity and authorized content, including promotion/deletion and repository ACLs. Never extract/store credentials from build metadata
- [ ] CRA-007.4 [CRAr] Treat API Portal as a configurable provider family until its product/API is identified. Support governed OpenAPI/schema/documentation ingestion, API/version relationships and approved discovery without pretending a universal portal endpoint exists
- [ ] CRA-007.5 [CRAr] Integrate code/document/schema parsing with provenance to commit/artifact/version and explicit language/format capability. Reject unsupported binaries and untrusted executable content
- [ ] CRA-007.6 [AGG] GitHub (REST plus GraphQL API v4) and GitLab (REST v4/GraphQL): Repository, Branch, Commit, Pull/Merge Request, Issue, Workflow/Pipeline run, Release; relations git:modifiesFile, git:authoredBy, git:mergesInto, git:referencesIssue; repository visibility (public/internal/private) populates aclvector
- [ ] CRA-007.7 [AGG] Cross-system issue references: extract issue keys from commit messages/PR titles with a configurable pattern (default \b[A-Z][A-Z0-9]+-\d+\b) restricted to an allowlist of project keys; each match becomes a proposed link with an evidence locator (message span) and is asserted only when the key resolves to an ingested issue
- [ ] CRA-007.8 [AGG] Artifactory: AQL plus storage webhooks; Repository, Artifact, Docker image/manifest, BuildInfo; art:builtFromCommit from build-info VCS revision; artifact identity by SHA-256 checksum
- [ ] CRA-007.9 [RES] API Portal: candidate provider profiles Kong, Apigee, SwaggerHub and a generic OpenAPI 3.0/3.1 crawler. The adapter remains UNQUALIFIED until the actual product is identified (decision H-07); api:Service, api:Endpoint, api:Operation, api:SchemaModel are the proposed vocabulary
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/api_portal.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/api_portal.py#L24-L24), [`packages/eoip/connectors/artifactory.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/artifactory.py#L1-L1), [`packages/eoip/connectors/git_references.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/git_references.py#L1-L1), [`packages/eoip/connectors/github.py:79`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/github.py#L79-L79), [`packages/eoip/connectors/gitlab.py:505`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/gitlab.py#L505-L505)
- tests: `tests/acceptance/test_code_build_artifacts_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-008 [P0] CRA-008: Observability and Operational-System Adapters

- **Source:** `CRAr_cpccaggcc-requirements.md:756-787` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-008; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-008. Observability and Operational-System Adapters

*Aggregated title: ITSM, Operational & Monitoring Connectors (ServiceNow, Splunk, Kibana & Grafana)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/010/011/040 | G (Named sources, media and actions) | M2 | G08 | — | — | — | X-12 | H-11 |

**Base statement:** Priority P1. Depends on CRA-004/010/011/040. Sources ServiceNow, Splunk, Kibana and Grafana.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-008.1** `[CRAr]` Qualify ServiceNow table/CMDB/incident/change/knowledge profiles with actual row/field ACLs and domain separation. Avoid broad table-service-account rights in default profiles.
- **CRA-008.2** `[CRAr]` Qualify Splunk searches/knowledge objects and permitted event metadata under query/time/result budgets. Sensitive log content is separately authorized; credentials and PII must not enter normal graph labels or telemetry.
- **CRA-008.3** `[CRAr]` Qualify Kibana saved objects/spaces separately from Elasticsearch/OpenSearch data authority. An authenticated dashboard connection does not authorize every backing index.
- **CRA-008.4** `[CRAr]` Qualify Grafana organizations/folders/dashboards and authorized data-source metadata/query results. Never retrieve or expose stored data-source secrets as ordinary metadata.
- **CRA-008.5** `[CRAr]` Keep observed telemetry separate from inferred incident causality. Preserve timestamps, source sampling, staleness, missing data and uncertainty. Any write-back/provisioning uses CRA-027.
- **CRA-008.6** `[AGG]` ServiceNow Table API profiles: `cmdb_ci*`, `cmdb_rel_ci` (Depends on::Used by, Runs on::Hosts), `incident`, `change_request`, `problem`, `kb_knowledge`; ServiceNow user criteria and roles (`itil`, `cmdb_read`) populate ACLs; write-back only through CRA-027.
- **CRA-008.7** `[AGG]` Splunk saved searches, alerts and dashboards; Grafana `/api/search` and `/api/dashboards/uid/{uid}`; Kibana saved objects per space. Dashboard panels link to CMDB services and microservices as proposals with evidence.
- **CRA-008.8** `[AGG]` Secret and PII redaction is applied to ingested query strings and log snippets before persistence (API keys, tokens, passwords, connection strings, emails per classification policy) and produces a redaction receipt with counts, never the removed values.
- **CRA-008.9** `[RES]` The CI dependency structure is st
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-008

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-004/010/011/040. Sources ServiceNow, Splunk, Kibana and Grafana.
- [ ] CRA-008.1 [CRAr] Qualify ServiceNow table/CMDB/incident/change/knowledge profiles with actual row/field ACLs and domain separation. Avoid broad table-service-account rights in default profiles
- [ ] CRA-008.2 [CRAr] Qualify Splunk searches/knowledge objects and permitted event metadata under query/time/result budgets. Sensitive log content is separately authorized; credentials and PII must not enter normal graph labels or telemetry
- [ ] CRA-008.3 [CRAr] Qualify Kibana saved objects/spaces separately from Elasticsearch/OpenSearch data authority. An authenticated dashboard connection does not authorize every backing index
- [ ] CRA-008.4 [CRAr] Qualify Grafana organizations/folders/dashboards and authorized data-source metadata/query results. Never retrieve or expose stored data-source secrets as ordinary metadata
- [ ] CRA-008.5 [CRAr] Keep observed telemetry separate from inferred incident causality. Preserve timestamps, source sampling, staleness, missing data and uncertainty. Any write-back/provisioning uses CRA-027
- [ ] CRA-008.6 [AGG] ServiceNow Table API profiles: cmdbci, cmdbrelci (Depends on::Used by, Runs on::Hosts), incident, changerequest, problem, kbknowledge; ServiceNow user criteria and roles (itil, cmdbread) populate ACLs; write-back only through CRA-027
- [ ] CRA-008.7 [AGG] Splunk saved searches, alerts and dashboards; Grafana /api/search and /api/dashboards/uid/{uid}; Kibana saved objects per space. Dashboard panels link to CMDB services and microservices as proposals with evidence
- [ ] CRA-008.8 [AGG] Secret and PII redaction is applied to ingested query strings and log snippets before persistence (API keys, tokens, passwords, connection strings, emails per classification policy) and produces a redaction receipt with counts, never the removed values
- [ ] CRA-008.9 [RES] The CI dependency structure is stored as a directed graph; cycles present in the CMDB are detected and reported as data-quality findings, never silently dropped to force a DAG
- [ ] obligation CRA-008.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] build an incident -> service -> deployment -> dashboard/log evidence journey. Exercise data-source denial, partial/stale telemetry, truncation and ACL revocation; no made-up operational status or causal conclusion is permitted
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/connectors/grafana.py:135`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/grafana.py#L135-L135), [`packages/eoip/connectors/kibana.py:153`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/kibana.py#L153-L153), [`packages/eoip/connectors/servicenow.py:195`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/servicenow.py#L195-L195), [`packages/eoip/connectors/splunk.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/splunk.py#L1-L1), [`packages/eoip/observability/telemetry_separation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/observability/telemetry_separation.py#L1-L1)
- tests: `tests/acceptance/test_observability_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-009 [P0] CRA-009: Warehouses, Catalog Federation and Custom Systems

- **Source:** `CRAr_cpccaggcc-requirements.md:788-823` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-009; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-009. Warehouses, Catalog Federation and Custom Systems

*Aggregated title: Data Warehouse, Messaging & Custom Connectors (Snowflake, Fortuna & custom systems)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-004/024/029 | G (Named sources, media and actions) | M2 | G08 | — | — | INV-42, INV-43, INV-45 | X-12, X-14 | H-06, H-11 |

**Base statement:** Priority P1. Depends on CRA-004/024/029. Sources Snowflake, Fortuna and other enterprise systems.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-009.1** `[CRAr]` Qualify Snowflake metadata and separately authorized data/query-history access with role/warehouse scope, masking/row policies, identifiers, costs and selected SQL/API versions.
- **CRA-009.2** `[CRAr]` Provide metadata-only, sampled-data and virtual-query modes with separate permissions, retention and provider readiness. Sampling/query history must be opt-in and redacted before downstream use.
- **CRA-009.3** `[CRAr]` Require a real product identity, interface/schema and network/auth contract for Fortuna. Until supplied, expose the configured custom-system adapter and missing-input reason, not an invented Fortuna API.
- **CRA-009.4** `[CRAr]` Integrate external catalogs such as OpenMetadata/DataHub/Atlas or commercial platforms through documented public interfaces and explicit ownership/precedence mappings. Do not duplicate their internal metadata model blindly.
- **CRA-009.5** `[CRAr]` Certify custom REST/GraphQL/SOAP/database/file/event providers using CRA-004 and scope-aware source fixtures. A signed plugin plus connectivity does not imply complete domain mappings or authorization fidelity.
- **CRA-009.6** `[AGG]` Snowflake: `INFORMATION_SCHEMA` and, where the role allows, `ACCOUNT_USAGE`; query history feeds CRA-029 lineage parsing; live virtualization through JDBC or Arrow Flight SQL under CRA-024 with statement timeout (default 30 s) and a credit/cost guard.
- **CRA-009.7** `[AGG]` Generic protocol adapters configurable with the mapping IR: REST/OpenAPI, GraphQL, SOAP 1.2, JDBC/ODBC, SFTP/files/object storage, Kafka/RabbitMQ events.
- **CRA-009.8** `[RES]` Fortuna remains a blocked product-specific adapter until decision H-06 supplies product identity, interface and auth contract; meanwhile the generic custom-system adapter is offered with the missing-input reason displayed.

**Configuration defaults:**

| Sett
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-009

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-004/024/029. Sources Snowflake, Fortuna and other enterprise systems.
- [ ] CRA-009.1 [CRAr] Qualify Snowflake metadata and separately authorized data/query-history access with role/warehouse scope, masking/row policies, identifiers, costs and selected SQL/API versions
- [ ] CRA-009.2 [CRAr] Provide metadata-only, sampled-data and virtual-query modes with separate permissions, retention and provider readiness. Sampling/query history must be opt-in and redacted before downstream use
- [ ] CRA-009.3 [CRAr] Require a real product identity, interface/schema and network/auth contract for Fortuna. Until supplied, expose the configured custom-system adapter and missing-input reason, not an invented Fortuna API
- [ ] CRA-009.4 [CRAr] Integrate external catalogs such as OpenMetadata/DataHub/Atlas or commercial platforms through documented public interfaces and explicit ownership/precedence mappings. Do not duplicate their internal metadata model blindly
- [ ] CRA-009.5 [CRAr] Certify custom REST/GraphQL/SOAP/database/file/event providers using CRA-004 and scope-aware source fixtures. A signed plugin plus connectivity does not imply complete domain mappings or authorization fidelity
- [ ] CRA-009.6 [AGG] Snowflake: INFORMATIONSCHEMA and, where the role allows, ACCOUNTUSAGE; query history feeds CRA-029 lineage parsing; live virtualization through JDBC or Arrow Flight SQL under CRA-024 with statement timeout (default 30 s) and a credit/cost guard
- [ ] CRA-009.7 [AGG] Generic protocol adapters configurable with the mapping IR: REST/OpenAPI, GraphQL, SOAP 1.2, JDBC/ODBC, SFTP/files/object storage, Kafka/RabbitMQ events
- [ ] CRA-009.8 [RES] Fortuna remains a blocked product-specific adapter until decision H-06 supplies product identity, interface and auth contract; meanwhile the generic custom-system adapter is offered with the missing-input reason displayed
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/catalog/federation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/federation.py#L1-L1), [`packages/eoip/connectors/custom_system.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/custom_system.py#L1-L1), [`packages/eoip/connectors/fortuna.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/fortuna.py#L1-L1), [`packages/eoip/connectors/snowflake.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/snowflake.py#L3-L3), [`scripts/build_master_suite.py:202`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L202-L202), [`scripts/enhance_master_suite.py:171`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L171-L171), [`scripts/patch_suite_and_dashboard.py:37`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L37-L37), [`scripts/update_matrix_caps.py:17`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/update_matrix_caps.py#L17-L17)
- tests: `scripts/test_cap_enrichment.py:71`, `scripts/test_master_caps_enrichment.py:85`, `tests/acceptance/test_warehouses_catalogs_acceptance.py:1`, `tests/query/test_ast_compiler.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-010 [P0] CRA-010: Durable Source Events and Incremental Synchronization

- **Source:** `CRAr_cpccaggcc-requirements.md:826-856` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-010; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-010. Durable Source Events and Incremental Synchronization

*Aggregated title: Bitemporal Event Journal & Resumable Checkpoint Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/004/031 | C (First acquisition slice) | M3 | G16 | — | — | INV-24, INV-31, INV-38, INV-40, INV-44, INV-52 | — | H-14 |

**Base statement:** Priority P0. Depends on CRA-003/004/031. Sources INV-31/39/40/44.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-010.1** `[CRAr]` Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, source/resource revision, observed time, payload hash/reference and cursor.
- **CRA-010.2** `[CRAr]` Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable. A content hash cannot hide ACL changes or repeated temporal events.
- **CRA-010.3** `[CRAr]` Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boundary; reconcile crash windows instead of claiming distributed exactly-once.
- **CRA-010.4** `[CRAr]` Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline absence as deletion.
- **CRA-010.5** `[CRAr]` Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy epochs without resurrecting data.
- **CRA-010.6** `[AGG]` Every pushed or pulled event is appended to an immutable append-only event journal; per source instance, each entry stores the SHA-256 of the previous entry so tampering or gaps are detectable.
- **CRA-010.7** `[AGG]` Bitemporal stamping: `observed_at` (platform receipt time) and `source_timestamp` (source-recorded time) are both stored; neither is inferred from the other.
- **CRA-010.8** `[AGG]` A persistent high-watermark checkpoint per connector instance is written transactionally with (or reconciled against) the publication intent so that a crashed worker resumes from the last durable checkpoint with zero loss and zero duplicate published assertions.

**Acceptance obligation CRA-010.A** (only after every clause above is ACCEPTED):

- `[CRAr]
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-010

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-003/004/031. Sources INV-31/39/40/44.
- [ ] CRA-010.1 [CRAr] Version the SourceEvent contract for upsert, delete, ACL-only change, rename/move and reconciliation. Include source instance, stable event identity, source/resource revision, observed time, payload hash/reference and cursor
- [ ] CRA-010.2 [CRAr] Preserve event order guarantees exactly as supplied; use stable deduplication and explicit conflict handling when revisions are opaque or incomparable. A content hash cannot hide ACL changes or repeated temporal events
- [ ] CRA-010.3 [CRAr] Implement durable checkpoints/leases and at-least-once acquisition with idempotent published effects. Acknowledge only after the declared durable boundary; reconcile crash windows instead of claiming distributed exactly-once
- [ ] CRA-010.4 [CRAr] Handle source absence, partial pages, invalid cursors and expired history with visible reconciliation/backfill states. Do not treat partial baseline absence as deletion
- [ ] CRA-010.5 [CRAr] Bind accepted assertions and projections to source/ontology/policy revisions and expose freshness/watermarks. Replay must preserve deletion and policy epochs without resurrecting data
- [ ] CRA-010.6 [AGG] Every pushed or pulled event is appended to an immutable append-only event journal; per source instance, each entry stores the SHA-256 of the previous entry so tampering or gaps are detectable
- [ ] CRA-010.7 [AGG] Bitemporal stamping: observedat (platform receipt time) and sourcetimestamp (source-recorded time) are both stored; neither is inferred from the other
- [ ] CRA-010.8 [AGG] A persistent high-watermark checkpoint per connector instance is written transactionally with (or reconciled against) the publication intent so that a crashed worker resumes from the last durable checkpoint with zero loss and zero duplicate published assertions
- [ ] obligation CRA-010.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] inject crashes before/after raw persistence, graph publication, outbox delivery and cursor acknowledgement. Replay duplicate/reordered/ACL/delete events and compare canonical graph and projections with independently computed expected state
- [ ] [MERGED] Kill the ingestion worker at ~50% of a baseline sync, restart, and compare the canonical graph with an independently computed expected graph: zero duplicates, zero gaps, deletes and ACL changes preserved (AGG + CRAr)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/journal/event_journal.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/journal/event_journal.py#L3-L3)
- tests: `tests/integration/test_event_journal_resilience.py:4`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-011 [P0] CRA-011: Safe Push, Crawl and Network Access

- **Source:** `CRAr_cpccaggcc-requirements.md:857-894` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-011. Safe Push, Crawl and Network Access

*Aggregated title: Push Webhook Gateway & Sandboxed Crawler Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/004 | C (First acquisition slice) | M3 | — | — | — | — | — | — |

**Base statement:** Priority P0. Depends on CRA-003/004. Sources source-acquisition objective and INV-07/49/52.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-011.1** `[CRAr]` Authenticate push/webhook sources, validate signature/timestamp/body limits and prevent replay. Apply backpressure and never enqueue unbounded payloads.
- **CRA-011.2** `[CRAr]` Restrict crawler schemes, hosts, ports, credentials, depth, pages, bytes, time and request concurrency. Respect authorized source policies and prefer source APIs where available.
- **CRA-011.3** `[CRAr]` Revalidate destination/DNS/redirect policy for every request and attachment URL, including IPv6, private/loopback/link-local/cloud metadata and proxy behavior. Never forward credentials to another origin by default.
- **CRA-011.4** `[CRAr]` Disable browser scripting and arbitrary resource fetching unless an isolated, explicitly permitted adapter requires it. Keep robots/terms/authorization decisions separate; robots permission is not access authorization.
- **CRA-011.5** `[CRAr]` Record crawl coverage, denied/skipped/failed resources and observation times. Partial results cannot become a clean/successful full-source statement.
- **CRA-011.6** `[AGG]` Webhook signature verification: GitHub `X-Hub-Signature-256` (HMAC-SHA256), GitLab `X-Gitlab-Token`, Slack v0 signing secret with timestamp skew <= 5 min, Jira shared secret/JWT per installation type. Failures return HTTP 401 and an audit event; delivery IDs are cached for replay rejection (default TTL 24 h); body limit default 10 MiB; sliding-window rate limit per source.
- **CRA-011.7** `[AGG]` Crawler defaults: max depth 5, max pages 10,000, max 50 MiB per resource, concurrency 2 per host, domain allowlist mandatory, robots.txt honoured but never treated as authorization.
- **CRA-011.8** `[AGG]` Egress block list re-evaluated per request and redirect: RFC 1918, loopback, link-local 169.254.0.0/16 including 169.254.169.254, IPv6 loopback/ULA/link-local, 0.0.0.0, and cloud metadata hostnames; DNS answers pinned for the connection; blocked attempts emit `EGRESS_BLOCKED` audit events.

**Configuration defa
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-011

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-003/004. Sources source-acquisition objective and INV-07/49/52.
- [ ] CRA-011.1 [CRAr] Authenticate push/webhook sources, validate signature/timestamp/body limits and prevent replay. Apply backpressure and never enqueue unbounded payloads
- [ ] CRA-011.2 [CRAr] Restrict crawler schemes, hosts, ports, credentials, depth, pages, bytes, time and request concurrency. Respect authorized source policies and prefer source APIs where available
- [ ] CRA-011.3 [CRAr] Revalidate destination/DNS/redirect policy for every request and attachment URL, including IPv6, private/loopback/link-local/cloud metadata and proxy behavior. Never forward credentials to another origin by default
- [ ] CRA-011.4 [CRAr] Disable browser scripting and arbitrary resource fetching unless an isolated, explicitly permitted adapter requires it. Keep robots/terms/authorization decisions separate; robots permission is not access authorization
- [ ] CRA-011.5 [CRAr] Record crawl coverage, denied/skipped/failed resources and observation times. Partial results cannot become a clean/successful full-source statement
- [ ] CRA-011.7 [AGG] Crawler defaults: max depth 5, max pages 10,000, max 50 MiB per resource, concurrency 2 per host, domain allowlist mandatory, robots.txt honoured but never treated as authorization
- [ ] CRA-011.8 [AGG] Egress block list re-evaluated per request and redirect: RFC 1918, loopback, link-local 169.254.0.0/16 including 169.254.169.254, IPv6 loopback/ULA/link-local, 0.0.0.0, and cloud metadata hostnames; DNS answers pinned for the connection; blocked attempts emit EGRESSBLOCKED audit events
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/connectors/test_safe_push_crawl_acceptance.py:4`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-012 [P0] CRA-012: Safe Text, Structured Data and Office Parsing

- **Source:** `CRAr_cpccaggcc-requirements.md:895-932` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-012. Safe Text, Structured Data and Office Parsing

*Aggregated title: Structured Data & Rich Office Document Decoders*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/010/011 | C (First acquisition slice) | M3 | G09, G11 | — | — | — | — | — |

**Base statement:** Priority P0. Depends on CRA-002/010/011. Sources G09/G11 and INV-30/47/49.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-012.1** `[CRAr]` Extend the existing format engine rather than creating duplicate parsers. Support TXT/CSV/JSON/XML/HTML/RTF, DOC/DOCX, PPT/PPTX and XLS/XLSX through qualified adapters, with explicit dependency readiness and format detection.
- **CRA-012.2** `[CRAr]` Preserve paragraph/table/row/column/sheet/slide locators, source encoding and parse/config versions. Distinguish spreadsheet formulas from cached/evaluated values; do not execute macros or embedded code.
- **CRA-012.3** `[CRAr]` Apply global input/expanded/member/depth/text/row/section/time budgets across nesting. Use safe XML/HTML parsing and prevent external-entity/remote-resource execution.
- **CRA-012.4** `[CRAr]` Repair and test chunking progress/termination. Validate `0 <= overlap < chunk_size`; the final chunk exits; empty, boundary, Unicode and long-unbroken inputs terminate without duplicate infinite suffixes.
- **CRA-012.5** `[CRAr]` Model partial extraction and unsupported content explicitly. Preserve raw bytes and warnings so a parser upgrade can rebuild results. A converter exit zero does not certify semantic fidelity.
- **CRA-012.6** `[RES]` Core format set (from the original source requirement): TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX. Extended set (from AGG, required for programme completeness, priority P2): TSV, YAML, JSON-LD (as data), XHTML, Markdown, AsciiDoc, ODT, ODP, ODS and text-layer PDF. Each format has its own capability entry and readiness state.
- **CRA-012.7** `[AGG]` Candidate libraries (each subject to CRA-035 license review and pinned versions): python-docx, python-pptx, openpyxl and/or calamine, defusedxml or lxml with entity resolution disabled, BeautifulSoup over a safe parser, and LibreOffice headless or Apache Tika for legacy DOC/PPT/XLS executed only in `heavy` workers.
- **CRA-012.8** `[AGG]` Every chunk carries an `EvidenceLocator` (document ID, source system, source revision, page/slide/sheet/cell/paragraph/run
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-012

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/010/011. Sources G09/G11 and INV-30/47/49.
- [ ] CRA-012.1 [CRAr] Extend the existing format engine rather than creating duplicate parsers. Support TXT/CSV/JSON/XML/HTML/RTF, DOC/DOCX, PPT/PPTX and XLS/XLSX through qualified adapters, with explicit dependency readiness and format detection
- [ ] CRA-012.2 [CRAr] Preserve paragraph/table/row/column/sheet/slide locators, source encoding and parse/config versions. Distinguish spreadsheet formulas from cached/evaluated values; do not execute macros or embedded code
- [ ] CRA-012.3 [CRAr] Apply global input/expanded/member/depth/text/row/section/time budgets across nesting. Use safe XML/HTML parsing and prevent external-entity/remote-resource execution
- [ ] CRA-012.4 [CRAr] Repair and test chunking progress/termination. Validate 0 <= overlap < chunksize; the final chunk exits; empty, boundary, Unicode and long-unbroken inputs terminate without duplicate infinite suffixes
- [ ] CRA-012.5 [CRAr] Model partial extraction and unsupported content explicitly. Preserve raw bytes and warnings so a parser upgrade can rebuild results. A converter exit zero does not certify semantic fidelity
- [ ] CRA-012.6 [RES] Core format set (from the original source requirement): TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX. Extended set (from AGG, required for programme completeness, priority P2): TSV, YAML, JSON-LD (as data), XHTML, Markdown, AsciiDoc, ODT, ODP, ODS and text-layer PDF. Each format has its own capability entry and readiness state
- [ ] CRA-012.7 [AGG] Candidate libraries (each subject to CRA-035 license review and pinned versions): python-docx, python-pptx, openpyxl and/or calamine, defusedxml or lxml with entity resolution disabled, BeautifulSoup over a safe parser, and LibreOffice headless or Apache Tika for legacy DOC/PPT/XLS executed only in heavy workers
- [ ] CRA-012.8 [AGG] Every chunk carries an EvidenceLocator (document ID, source system, source revision, page/slide/sheet/cell/paragraph/run index, charstart/charend)
- [ ] CRA-012.9 [AGG] Qualification target on P0 reference hardware: a 10 MB DOCX and a 50-sheet XLSX are fully extracted with locators in <= 5 s each (benchmark manifest target, not a claim until measured)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/acceptance/test_safe_parsing_acceptance.py:1`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-013 [P0] CRA-013: Email, Containers and Nested Provenance

- **Source:** `CRAr_cpccaggcc-requirements.md:933-968` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-013. Email, Containers and Nested Provenance

*Aggregated title: Email, Mailbox Container & Archive Parsers*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-012/035/040 | C (First acquisition slice) | M3 | — | — | — | — | X-16 | H-09 |

**Base statement:** Priority P0. Depends on CRA-012/035/040. Sources attachment format requirements and G17.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-013.1** `[CRAr]` Parse EML/MIME and approved mailbox protocols with stable message/thread/header/body-part identity. Support MSG only through an explicitly licensed and qualified adapter; do not silently clear existing dependency concerns.
- **CRA-013.2** `[CRAr]` Preserve parent message/archive/document relationships, attachment content hashes, original names, source locators and inherited ACL/retention/legal-hold metadata.
- **CRA-013.3** `[CRAr]` Enforce combined archive/container expansion, depth, member count and path-safety limits, including duplicate names, symlinks and format confusion. Do not extract untrusted paths into the application filesystem.
- **CRA-013.4** `[CRAr]` Handle encrypted/unreadable attachments, malformed MIME, embedded messages and converter failure with per-item diagnostics and aggregate partial/failed status.
- **CRA-013.5** `[CRAr]` Prevent automatic remote-image loading, active HTML/script execution and credential extraction from messages. Every attachment download rechecks source authorization.
- **CRA-013.6** `[AGG]` Formats: EML/MIME and MBOX; MSG only through an explicitly licensed adapter (`extract-msg` remains disabled until its distribution terms are cleared under CRA-035, conflict X-16).
- **CRA-013.7** `[AGG]` Extract headers `From`, `To`, `Cc`, `Bcc` (only where the source exposes it and policy allows), `Subject`, `Date`, `Message-ID`, `In-Reply-To`, `References`; plain-text body; sanitized HTML body; nested attachments recursively queued with inherited ACLs.
- **CRA-013.8** `[AGG]` Archives: ZIP, TAR, GZ, BZ2, 7Z with streaming decompression and combined limits: total expanded size 2 GiB, nesting depth 3, 10,000 members, per-member compression ratio 100:1; reject absolute paths, `..`, drive letters, symlinks/hardlinks and duplicate-name overwrite.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| archive limits | 2 GiB / depth 3 / 10,000 members / 100:1 | AGG + RES |

[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-013

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-012/035/040. Sources attachment format requirements and G17.
- [ ] CRA-013.1 [CRAr] Parse EML/MIME and approved mailbox protocols with stable message/thread/header/body-part identity. Support MSG only through an explicitly licensed and qualified adapter; do not silently clear existing dependency concerns
- [ ] CRA-013.2 [CRAr] Preserve parent message/archive/document relationships, attachment content hashes, original names, source locators and inherited ACL/retention/legal-hold metadata
- [ ] CRA-013.3 [CRAr] Enforce combined archive/container expansion, depth, member count and path-safety limits, including duplicate names, symlinks and format confusion. Do not extract untrusted paths into the application filesystem
- [ ] CRA-013.4 [CRAr] Handle encrypted/unreadable attachments, malformed MIME, embedded messages and converter failure with per-item diagnostics and aggregate partial/failed status
- [ ] CRA-013.5 [CRAr] Prevent automatic remote-image loading, active HTML/script execution and credential extraction from messages. Every attachment download rechecks source authorization
- [ ] CRA-013.6 [AGG] Formats: EML/MIME and MBOX; MSG only through an explicitly licensed adapter (extract-msg remains disabled until its distribution terms are cleared under CRA-035, conflict X-16)
- [ ] CRA-013.7 [AGG] Extract headers From, To, Cc, Bcc (only where the source exposes it and policy allows), Subject, Date, Message-ID, In-Reply-To, References; plain-text body; sanitized HTML body; nested attachments recursively queued with inherited ACLs
- [ ] CRA-013.8 [AGG] Archives: ZIP, TAR, GZ, BZ2, 7Z with streaming decompression and combined limits: total expanded size 2 GiB, nesting depth 3, 10,000 members, per-member compression ratio 100:1; reject absolute paths, .., drive letters, symlinks/hardlinks and duplicate-name overwrite
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/acceptance/test_email_containers_acceptance.py:1`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-014 [P0] CRA-014: Images, Audio and Video

- **Source:** `CRAr_cpccaggcc-requirements.md:969-1001` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-014. Images, Audio and Video

*Aggregated title: Multimedia, Speech-to-Text & Computer Vision OCR Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-002/012/026/035/040 | G (Named sources, media and actions) | M3 | G09 | — | — | INV-51, INV-52 | — | — |

**Base statement:** Priority P1. Depends on CRA-002/012/026/035/040. Sources INV-51/52.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-014.1** `[CRAr]` Provide capability-specific image metadata, OCR, audio transcription, video decode/frame sampling and optional visual extraction adapters. Report exactly which tasks/providers are configured, rather than one multimodal flag.
- **CRA-014.2** `[CRAr]` Retain coordinates/page/frame/time spans, language, confidence, provider/model/config revisions and raw evidence references. Transcript/visual outputs remain proposed unless approved by applicable publication policy.
- **CRA-014.3** `[CRAr]` Isolate codecs/OCR/ML execution, enforce duration/resolution/frame/sample/output budgets and prohibit unapproved model downloads/network calls. Required model assets must be available in offline bundles.
- **CRA-014.4** `[CRAr]` Support cancellation/progress based on actual work and explicit partial output. Preserve unsupported or low-quality segments; never fabricate text, timestamps or diagram topology.
- **CRA-014.5** `[CRAr]` Evaluate WER/CER, entity/fact precision/recall and visual task accuracy on licensed domain/language corpora with held-out splits. Apply section 4's selected thresholds through per-task/profile manifests, not as an unsupported universal quality claim.
- **CRA-014.6** `[AGG]` OCR for PNG, JPG/JPEG, TIFF, WEBP and scanned PDF using a license-reviewed engine (Tesseract or PaddleOCR candidates); each line/paragraph carries a normalized bounding box `[ymin, xmin, ymax, xmax]` in 0.0-1.0 plus page number and confidence.
- **CRA-014.7** `[AGG]` Audio/video: audio extraction with FFmpeg (build flags determine LGPL/GPL obligations, reviewed under CRA-035) for MP4, MKV, MP3, WAV, M4A; transcription with a locally hosted Whisper-family model in an isolated worker; segments carry start/end milliseconds.
- **CRA-014.8** `[AGG]` All OCR/ASR/vision models run on-premises or inside the customer VPC from hash-pinned offline bundles; zero external API calls in no-egress mode.
- **CRA-014.9** `[GN]` OCR, ASR and vision models req
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-014

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-002/012/026/035/040. Sources INV-51/52.
- [ ] CRA-014.1 [CRAr] Provide capability-specific image metadata, OCR, audio transcription, video decode/frame sampling and optional visual extraction adapters. Report exactly which tasks/providers are configured, rather than one multimodal flag
- [ ] CRA-014.2 [CRAr] Retain coordinates/page/frame/time spans, language, confidence, provider/model/config revisions and raw evidence references. Transcript/visual outputs remain proposed unless approved by applicable publication policy
- [ ] CRA-014.3 [CRAr] Isolate codecs/OCR/ML execution, enforce duration/resolution/frame/sample/output budgets and prohibit unapproved model downloads/network calls. Required model assets must be available in offline bundles
- [ ] CRA-014.4 [CRAr] Support cancellation/progress based on actual work and explicit partial output. Preserve unsupported or low-quality segments; never fabricate text, timestamps or diagram topology
- [ ] CRA-014.5 [CRAr] Evaluate WER/CER, entity/fact precision/recall and visual task accuracy on licensed domain/language corpora with held-out splits. Apply section 4's selected thresholds through per-task/profile manifests, not as an unsupported universal quality claim
- [ ] CRA-014.6 [AGG] OCR for PNG, JPG/JPEG, TIFF, WEBP and scanned PDF using a license-reviewed engine (Tesseract or PaddleOCR candidates); each line/paragraph carries a normalized bounding box [ymin, xmin, ymax, xmax] in 0.0-1.0 plus page number and confidence
- [ ] CRA-014.7 [AGG] Audio/video: audio extraction with FFmpeg (build flags determine LGPL/GPL obligations, reviewed under CRA-035) for MP4, MKV, MP3, WAV, M4A; transcription with a locally hosted Whisper-family model in an isolated worker; segments carry start/end milliseconds
- [ ] CRA-014.8 [AGG] All OCR/ASR/vision models run on-premises or inside the customer VPC from hash-pinned offline bundles; zero external API calls in no-egress mode
- [ ] CRA-014.9 [GN] OCR, ASR and vision models require the CRA-043 tiers they depend on plus offline bundles; a missing tier sets the task capability to UNAVAILABLE with the tier named, never a metadata-only result labelled as understanding
- [ ] obligation CRA-014.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] real permitted media files, degraded scans/noise/unsupported codecs and large/hostile inputs. Verify no external call in no-egress mode, correct evidence locators, timeout cleanup and dependency-unavailable states. File metadata alone does not satisfy OCR/transcription/understanding
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ingestion/multimodal_audio.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ingestion/multimodal_audio.py#L1-L1)
- tests: `tests/acceptance/test_multimodal_media_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-016 [P0] CRA-016: RDF Terms, Parsing and Standards Fidelity

- **Source:** `CRAr_cpccaggcc-requirements.md:1034-1073` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 32, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-016; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-016. RDF Terms, Parsing and Standards Fidelity

*Aggregated title: RDF 1.1 / RDF-Star Terms & Lexical Fidelity Engine*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | D (Semantic core) | M4 | F1, G03, G05 | ONT-001, ONT-019 | I1, I10 | INV-01, INV-20, INV-26, INV-37, INV-55 | X-17, X-29 | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Sources G03/G05 and INV-01/23/26/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-016.1** `[CRAr]` Use a proven standards parser for the selected RDF/JSON-LD serializations and validate exact supported syntax/profile. Do not describe the EOIP-specific compact JSON-LD importer as a general implementation.
- **CRA-016.2** `[CRAr]` Preserve IRI lexical identity, case, blank-node scope, language tags, datatype and literal lexical/value distinctions, RDF lists, named graph identity and annotations. Normalized display labels never mutate canonical IDs.
- **CRA-016.3** `[CRAr]` Restrict JSON-LD contexts and ontology imports by the approved resolver policy, hash-pin approved external resources and support disconnected resolution. Block SSRF and remote context changes.
- **CRA-016.4** `[CRAr]` Distinguish syntax validity, ontology profile membership, logical consistency and instance-shape validity with separate outcomes.
- **CRA-016.5** `[CRAr]` Qualify export/import using independent parsers and canonical/isomorphic dataset comparisons plus semantic competency queries. Report bounds, truncation, unsupported constructs and loss counts explicitly.
- **CRA-016.6** `[OCA]` Adopt `rdflib>=7` (BSD-3, pinned) as default parser/serializer for Turtle, RDF/XML, N-Triples, N-Quads, JSON-LD 1.1 and TriG in new module `packages/eoip/ontology/serialization.py` (`RDFSerializer`, `RDFDeserializer`). RDF/XML and any XML input are parsed with external entity resolution disabled, size caps and a parse timeout (XXE and entity-expansion defence).
- **CRA-016.7** `[OCA]` API: `POST /ontology/import` (`format`, `content` or `artifact_ref`) returns an import report (triple/quad counts, named graphs, losses, unsupported constructs); `GET /ontology/export?format=turtle|rdfxml|nt|nq|jsonld|trig` emits valid output. `rdf.py:jsonld_to_property_graph` may be reused as an internal pivot only after its behaviour is covered by independent tests.
- **CRA-016.8** `[AGG]` RDF-star is an optional named profil
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-016

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/003. Sources G03/G05 and INV-01/23/26/55.
- [ ] CRA-016.1 [CRAr] Use a proven standards parser for the selected RDF/JSON-LD serializations and validate exact supported syntax/profile. Do not describe the EOIP-specific compact JSON-LD importer as a general implementation
- [ ] CRA-016.2 [CRAr] Preserve IRI lexical identity, case, blank-node scope, language tags, datatype and literal lexical/value distinctions, RDF lists, named graph identity and annotations. Normalized display labels never mutate canonical IDs
- [ ] CRA-016.3 [CRAr] Restrict JSON-LD contexts and ontology imports by the approved resolver policy, hash-pin approved external resources and support disconnected resolution. Block SSRF and remote context changes
- [ ] CRA-016.4 [CRAr] Distinguish syntax validity, ontology profile membership, logical consistency and instance-shape validity with separate outcomes
- [ ] CRA-016.5 [CRAr] Qualify export/import using independent parsers and canonical/isomorphic dataset comparisons plus semantic competency queries. Report bounds, truncation, unsupported constructs and loss counts explicitly
- [ ] CRA-016.6 [OCA] Adopt rdflib>=7 (BSD-3, pinned) as default parser/serializer for Turtle, RDF/XML, N-Triples, N-Quads, JSON-LD 1.1 and TriG in new module packages/eoip/ontology/serialization.py (RDFSerializer, RDFDeserializer). RDF/XML and any XML input are parsed with external entity resolution disabled, size caps and a parse timeout (XXE and entity-expansion defence)
- [ ] CRA-016.8 [AGG] RDF-star is an optional named profile rdf-star (disabled by default) with its own conformance tests; when disabled, statement-level annotations use named-graph assertion reification (X-17)
- [ ] CRA-016.9 [OCA] Round-trip corpus (ONT-001/ONT-019): pinned gist release, pinned schema.org release, FOAF, Dublin Core, a >= 10k-triple SKOS thesaurus and a FIBO subset. Exported OWL loads without error in Protégé 5.6 (manual review record) and in OWL API inside a semantic worker (automated)
- [ ] CRA-016.10 [RES] Fidelity rule (resolves X-29): 100% term/axiom fidelity on the declared supported subset; corpus-level fidelity reported with every loss enumerated (unsupported constructs stay in the denominator); CI fails if corpus fidelity regresses by more than 1 percentage point versus the last ACCEPTED report (ONT-019)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/registry.py:21`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/registry.py#L21-L21), [`packages/eoip/contracts/canonical.py:36`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/contracts/canonical.py#L36-L36), [`packages/eoip/ontology/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/__init__.py#L1-L1), [`packages/eoip/ontology/rdf.py:709`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/rdf.py#L709-L709), [`packages/eoip/ontology/serialization.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/serialization.py#L1-L1), [`packages/eoip/ontology/skos.py:13`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/skos.py#L13-L13)
- tests: `tests/acceptance/test_claims_governance_acceptance.py:92`, `tests/semantic/test_rdf_fidelity.py:1`, `tests/semantic/test_shacl_strict.py:1`, `tests/semantic/test_skos_governance.py:11`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-017 [P0] CRA-017: Mapping IR, RDF/LPG Projection and OBDA Inputs

- **Source:** `CRAr_cpccaggcc-requirements.md:1074-1113` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-017; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-017. Mapping IR, RDF/LPG Projection and OBDA Inputs

*Aggregated title: Declarative Mapping IR & Relational OBDA Virtualization*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-010/016 | D (Semantic core) | M4 | G05, G10, G13 | ONT-005, ONT-006, ONT-017, ONT-018 | I1, I7, I8, I9, I12 | INV-03, INV-07, INV-16, INV-21, INV-23, INV-26, INV-27, INV-28, INV-30, INV-31, INV-32, INV-34, INV-35 | X-17 | — |

**Base statement:** Priority P0. Depends on CRA-010/016. Sources G05/G10/G13 and INV-03/16/26/27/28/30/31/35.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-017.1** `[CRAr]` Define a versioned, engine-neutral mapping representation for source schema/records to ontology terms, including stable identity, joins, nulls, datatypes, language, provenance and graph policy.
- **CRA-017.2** `[CRAr]` Support qualified R2RML/RML adapters and explicit source-dialect/config compatibility. User-defined functions run through CRA-002 with approved capabilities.
- **CRA-017.3** `[CRAr]` Preserve multigraph/relationship assertion IDs, edge properties and evidence when projecting to/from property graphs. Record every unsupported construct and lossy coercion; block lossless claims when any loss exists.
- **CRA-017.4** `[CRAr]` Separate virtual mappings from materialized ingestion, including source access policy, transaction/snapshot/freshness semantics and resource costs. Do not pretend source rows are copied when queries are virtualized, or vice versa.
- **CRA-017.5** `[CRAr]` Provide mapping test cases, dry-run/sample preview, field diagnostics and source-drift analysis. Bind approval/publication to source schema and ontology/mapping revisions.
- **CRA-017.6** `[OCA]` Connector Mapping Language (CML), YAML: `source`, `version`, `subject_map{template, class}`, `property_maps[{path, predicate, datatype, required, vocab}]`, `relation_maps[{path, predicate, object_template, object_class}]`, `provenance{emit, confidence}`, `governance{classification, pii_fields}`. Paths use a documented JSONPath subset; templates use `{field}` substitution with IRI-safe encoding and a whitelist of functions (lower, upper, trim, concat, split, date_parse, iri_safe). Templates are never evaluated as code.
- **CRA-017.7** `[RES]` CML compiles into the engine-neutral mapping IR; R2RML/RML (and RML-star when enabled) import translates into the same IR with an unsupported
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-017

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-010/016. Sources G05/G10/G13 and INV-03/16/26/27/28/30/31/35.
- [ ] CRA-017.1 [CRAr] Define a versioned, engine-neutral mapping representation for source schema/records to ontology terms, including stable identity, joins, nulls, datatypes, language, provenance and graph policy
- [ ] CRA-017.2 [CRAr] Support qualified R2RML/RML adapters and explicit source-dialect/config compatibility. User-defined functions run through CRA-002 with approved capabilities
- [ ] CRA-017.3 [CRAr] Preserve multigraph/relationship assertion IDs, edge properties and evidence when projecting to/from property graphs. Record every unsupported construct and lossy coercion; block lossless claims when any loss exists
- [ ] CRA-017.4 [CRAr] Separate virtual mappings from materialized ingestion, including source access policy, transaction/snapshot/freshness semantics and resource costs. Do not pretend source rows are copied when queries are virtualized, or vice versa
- [ ] CRA-017.5 [CRAr] Provide mapping test cases, dry-run/sample preview, field diagnostics and source-drift analysis. Bind approval/publication to source schema and ontology/mapping revisions
- [ ] CRA-017.6 [OCA] Connector Mapping Language (CML), YAML: source, version, subjectmap{template, class}, propertymaps[{path, predicate, datatype, required, vocab}], relationmaps[{path, predicate, objecttemplate, objectclass}], provenance{emit, confidence}, governance{classification, piifields}. Paths use a documented JSONPath subset; templates use {field} substitution with IRI-safe encoding and a whi
- [ ] CRA-017.7 [RES] CML compiles into the engine-neutral mapping IR; R2RML/RML (and RML-star when enabled) import translates into the same IR with an unsupported-construct report (ONT-017). One IR, many front-ends
- [ ] CRA-017.8 [OCA] LPG <-> RDF projection scheme: vertex IRI eoip:entity/{Label}/{id} (id percent-encoded) with rdf:type eoip:class/{Label}; vertex property eoip:property/{name} as typed literal from the manifest; edge without properties -> direct triple eoip:relation/{label}; edge with properties -> RDF-star when the profile is enabled, otherwise a named graph per edge assertion urn:eoip:assertion:{
- [ ] CRA-017.9 [OCA] W3C PROV-O on every mined triple (ONT-018): prov:wasDerivedFrom source resource revision, prov:wasGeneratedBy mapping-run activity (mapping revision, connector run ID), prov:wasAttributedTo connector agent; provenance survives RDF export
- [ ] CRA-017.10 [OCA] AI-suggested mappings (ONT-006): sample bounded, redacted payloads and propose CML with per-field confidence; suggestions never auto-activate. Evaluation target: >= 70% of suggested property maps accepted without edit on Jira and ServiceNow corpora
- [ ] CRA-017.11 [AGG] Benchmark targets recorded in the manifest: CML execution >= 10,000 records/s on 1M Jira issues (OCA); vectorized batch materialization (Morph-KGC-class) >= 100,000 triples/s on CSV/JSON (AGG); OBDA point query on a 10M-row indexed PostgreSQL table < 50 ms via SQL pushdown (AGG)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/mapping/cml.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/cml.py#L1-L1), [`packages/eoip/mapping/diagnostics.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/diagnostics.py#L1-L1), [`packages/eoip/mapping/executor.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/executor.py#L1-L1), [`packages/eoip/mapping/ir.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/ir.py#L1-L1), [`packages/eoip/mapping/r2rml.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/r2rml.py#L1-L1), [`packages/eoip/mapping/virtualization.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/mapping/virtualization.py#L1-L1)
- tests: `tests/mapping/test_cml_language.py:1`, `tests/mapping/test_mapping_advanced.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-018 [P0] CRA-018: Durable Ontology Registry and Packages

- **Source:** `CRAr_cpccaggcc-requirements.md:1114-1143` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-018; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-018. Durable Ontology Registry and Packages

*Aggregated title: Immutable Ontology Package Registry & Semantic Versioning*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-016/031/035 | D (Semantic core) | M4 | F1 | ONT-010 | I15, I20 | INV-01, INV-02, INV-06, INV-08, INV-09, INV-15, INV-25, INV-33, INV-46, INV-50, INV-55 | X-03, X-30 | — |

**Base statement:** Priority P0. Depends on CRA-016/031/035. Sources INV-02/15/25/46/50/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-018.1** `[CRAr]` Persist ontology/version IRIs, imports/checksums, axioms, annotations, shapes, rules, mappings, namespace ownership, profile and license metadata in a canonical registry.
- **CRA-018.2** `[CRAr]` Package immutable releases with full import closure, engine/profile/config references, provenance, validation/reasoning reports and publication signatures/manifests.
- **CRA-018.3** `[CRAr]` Keep drafts, accepted releases and source/derived graph revisions separate. No mutable global singleton or browser localStorage may be the sole authority.
- **CRA-018.4** `[CRAr]` Support domain packs and optional pinned upper ontologies such as gist, preserving upstream terms, namespaces, attribution and migration notes. Do not imply importing an upper ontology models the entire enterprise.
- **CRA-018.5** `[CRAr]` Resolve and install packages atomically with compatibility and signature checks, approved repositories and offline availability. Reject missing/tampered/unlicensed dependencies with explicit diagnostics.
- **CRA-018.6** `[AGG]` A release bundle contains: primary ontology document(s), pinned transitive import closure with SHA-256 digests, SHACL shapes package, mapping definitions, release manifest and signature. Tampering with any member causes signature mismatch and activation halts.
- **CRA-018.7** `[OCA]` Semantic versioning (SemVer 2.0) is computed from the semantic diff using the existing `compute_next_semver` (gitops.py:733) after it is verified by fixtures: major for breaking changes (removal, domain/range or cardinality tightening, type change), minor for additive changes, patch for annotation-only changes.
- **CRA-018.8** `[OCA]` Domain packs (ONT-010) via existing `packs.py`, `domain_pack_manager.py` and `industry_templates.py`: gist (CC BY 4.0, attribution in NOTICE and docs), FIBO and schema.org (license terms verified per exact a
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-018

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-016/031/035. Sources INV-02/15/25/46/50/55.
- [ ] CRA-018.1 [CRAr] Persist ontology/version IRIs, imports/checksums, axioms, annotations, shapes, rules, mappings, namespace ownership, profile and license metadata in a canonical registry
- [ ] CRA-018.2 [CRAr] Package immutable releases with full import closure, engine/profile/config references, provenance, validation/reasoning reports and publication signatures/manifests
- [ ] CRA-018.3 [CRAr] Keep drafts, accepted releases and source/derived graph revisions separate. No mutable global singleton or browser localStorage may be the sole authority
- [ ] CRA-018.4 [CRAr] Support domain packs and optional pinned upper ontologies such as gist, preserving upstream terms, namespaces, attribution and migration notes. Do not imply importing an upper ontology models the entire enterprise
- [ ] CRA-018.5 [CRAr] Resolve and install packages atomically with compatibility and signature checks, approved repositories and offline availability. Reject missing/tampered/unlicensed dependencies with explicit diagnostics
- [ ] CRA-018.6 [AGG] A release bundle contains: primary ontology document(s), pinned transitive import closure with SHA-256 digests, SHACL shapes package, mapping definitions, release manifest and signature. Tampering with any member causes signature mismatch and activation halts
- [ ] CRA-018.7 [OCA] Semantic versioning (SemVer 2.0) is computed from the semantic diff using the existing computenextsemver (gitops.py:733) after it is verified by fixtures: major for breaking changes (removal, domain/range or cardinality tightening, type change), minor for additive changes, patch for annotation-only changes
- [ ] CRA-018.8 [OCA] Domain packs (ONT-010) via existing packs.py, domainpackmanager.py and industrytemplates.py: gist (CC BY 4.0, attribution in NOTICE and docs), FIBO and schema.org (license terms verified per exact artifact, X-30), SNOMED-CT only when customer-provided under the customer's affiliate license and never redistributed
- [ ] obligation CRA-018.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] clean restart and fresh-node restore retrieve the same package/release by hash; missing import, changed remote document or incompatible engine cannot silently publish. Compare independently opened package contents and release metadata, not only a database row
- [ ] [MERGED] Each domain pack installs, validates under its declared profile and records attribution; a tampered import file triggers signature mismatch and halts activation (AGG)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/__init__.py#L1-L1), [`packages/eoip/ontology/package_registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/package_registry.py#L1-L1)
- tests: `tests/unit/test_ontology_packages.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-019 [P0] CRA-019: Profile-Correct Reasoning and Explanations

- **Source:** `CRAr_cpccaggcc-requirements.md:1144-1186` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-019; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-019. Profile-Correct Reasoning and Explanations

*Aggregated title: Hybrid Tiered Reasoning Engine (HTRE) & Dependency Retraction*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/016/018 | D (Semantic core) | M4 | F2, G03, G04 | ONT-007, ONT-008 | I4, I5, I18 | INV-01, INV-03, INV-04, INV-05, INV-17, INV-18, INV-19, INV-20, INV-22, INV-27, INV-46, INV-48, INV-53, INV-55 | X-10, X-28 | H-02 |

**Base statement:** Priority P0. Depends on CRA-002/016/018. Sources G03/G04 and INV-01/04/17/18/19/20/22/46/48/53/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-019.1** `[CRAr]` Replace or clearly scope the custom helper; do not advertise it as complete OWL DL. Use qualified engines for RDFS, OWL 2 RL/EL/QL/DL tasks with explicit supported profiles and limits.
- **CRA-019.2** `[CRAr]` Preserve exact identifiers, load pinned import closure, check profile membership and distinguish consistency, unsatisfiable classes, classification and entailment tasks.
- **CRA-019.3** `[CRAr]` Return engine/version/profile, asserted versus inferred statements, explanations/support dependencies, revision and unsupported/error/timeout/cancel status. Timeouts cannot become negative entailment or a clean consistency result.
- **CRA-019.4** `[CRAr]` Keep inferred graphs separate and implement dependency-aware invalidation/retraction after source, ontology, identity or ACL changes. Handle multiple justifications correctly.
- **CRA-019.5** `[CRAr]` Offer materialized/query-time modes only where supported and measured. Expose resulting plan, amplification and freshness rather than hiding expensive work.
- **CRA-019.6** `[CRAr]` Enforce CRA-003 on inference inputs/outputs/explanations. Prevent restricted supporting facts from leaking through an otherwise visible conclusion.
- **CRA-019.7** `[OCA]` Define `ReasonerPort` in `packages/eoip/ontology/reasoning/port.py`: `classify()`, `is_consistent()`, `unsatisfiable_classes()`, `realize()`, `entails(axiom)`, `explain(axiom)`, each returning typed results with engine, version, profile, status (OK, INCONSISTENT, UNSUPPORTED, TIMEOUT, CANCELLED, ERROR) and revision bindings.
- **CRA-019.8** `[OCA]` Adapters: ELK (Apache-2.0, OWL 2 EL, default for classification), Openllet (license verified, OWL 2 DL alternative), HermiT (LGPL, optional separately installed plugin only), Jena rules for OWL 2 RL/RDFS, and `Nat
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-019

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/016/018. Sources G03/G04 and INV-01/04/17/18/19/20/22/46/48/53/55.
- [ ] CRA-019.1 [CRAr] Replace or clearly scope the custom helper; do not advertise it as complete OWL DL. Use qualified engines for RDFS, OWL 2 RL/EL/QL/DL tasks with explicit supported profiles and limits
- [ ] CRA-019.2 [CRAr] Preserve exact identifiers, load pinned import closure, check profile membership and distinguish consistency, unsatisfiable classes, classification and entailment tasks
- [ ] CRA-019.3 [CRAr] Return engine/version/profile, asserted versus inferred statements, explanations/support dependencies, revision and unsupported/error/timeout/cancel status. Timeouts cannot become negative entailment or a clean consistency result
- [ ] CRA-019.4 [CRAr] Keep inferred graphs separate and implement dependency-aware invalidation/retraction after source, ontology, identity or ACL changes. Handle multiple justifications correctly
- [ ] CRA-019.5 [CRAr] Offer materialized/query-time modes only where supported and measured. Expose resulting plan, amplification and freshness rather than hiding expensive work
- [ ] CRA-019.6 [CRAr] Enforce CRA-003 on inference inputs/outputs/explanations. Prevent restricted supporting facts from leaking through an otherwise visible conclusion
- [ ] CRA-019.7 [OCA] Define ReasonerPort in packages/eoip/ontology/reasoning/port.py: classify(), isconsistent(), unsatisfiableclasses(), realize(), entails(axiom), explain(axiom), each returning typed results with engine, version, profile, status (OK, INCONSISTENT, UNSUPPORTED, TIMEOUT, CANCELLED, ERROR) and revision bindings
- [ ] CRA-019.8 [OCA] Adapters: ELK (Apache-2.0, OWL 2 EL, default for classification), Openllet (license verified, OWL 2 DL alternative), HermiT (LGPL, optional separately installed plugin only), Jena rules for OWL 2 RL/RDFS, and NativeAdapter wrapping the existing OWLReasoner restricted to and labelled as profile eoip-native-rdfs-subset
- [ ] CRA-019.9 [OCA] Remove the hardcoded domain axioms of OWLReasoner.bootstrapcoreaxioms() (Microservice, Engineer, RelationalDatabase; rdf.py:598-700) from all production paths; axioms come from the manifest and installed packages. The old axioms may remain only as a named test fixture
- [ ] CRA-019.10 [AGG] Hybrid mode (ONT-008 / AGG HTRE): a per-rule strategy table (materialize or querytime) chosen by a documented cost model (estimated amplification, volatility, fan-out, query frequency); a TBox change recomputes only affected rules; benchmarked against pure forward and pure backward chaining
- [ ] CRA-019.11 [RES] Retraction uses stored justification sets (supportingassertionids); cost is proportional to affected derivations and is measured, replacing the unproven AGG 'O(1)' claim (X-10)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/rdf.py:692`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/rdf.py#L692-L692), [`packages/eoip/ontology/reasoning/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/reasoning/__init__.py#L1-L1), [`packages/eoip/ontology/reasoning/adapters.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/reasoning/adapters.py#L1-L1), [`packages/eoip/ontology/reasoning/hybrid.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/reasoning/hybrid.py#L1-L1), [`packages/eoip/ontology/reasoning/port.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/reasoning/port.py#L1-L1), [`scripts/build_master_suite.py:214`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L214-L214), [`scripts/enhance_master_suite.py:242`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L242-L242), [`scripts/patch_suite_and_dashboard.py:135`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L135-L135)
- tests: `scripts/test_cap_enrichment.py:83`, `scripts/test_master_caps_enrichment.py:97`, `tests/semantic/test_reasoning_gold.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-020 [P0] CRA-020: Transactional Shape Validation

- **Source:** `CRAr_cpccaggcc-requirements.md:1187-1220` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 27, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-020. Transactional Shape Validation

*Aggregated title: Strict Transactional W3C SHACL Core 2017 Validator*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/016/018/031 | D (Semantic core) | M4 | F3, G01, G02 | ONT-004 | I10 | INV-02, INV-06, INV-08, INV-17, INV-20, INV-22, INV-26, INV-47, INV-48, INV-49 | — | — |

**Base statement:** Priority P0. Depends on CRA-002/016/018/031. Sources G01/G02 and INV-22/47/48/49.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-020.1** `[CRAr]` Use a proven validator for declared SHACL Core 2017 coverage; keep extensions/profile versions explicit. A custom Python property checker must be labelled as such until replaced/qualified.
- **CRA-020.2** `[CRAr]` Enforce min/max cardinality, datatype/node kind, class, value sets, language/length/pattern/numeric bounds, logical and property-path constraints for the declared profile. Unsupported constraints must produce an explicit unsupported result, never `conforms=true`.
- **CRA-020.3** `[CRAr]` Produce standards-compatible reports with focus node, result path/value, source shape/constraint, severity and message, plus revision/engine/config and explicit truncation. Unknown datatype names fail validation setup.
- **CRA-020.4** `[CRAr]` Validate the candidate against required existing data and shape/ontology revision. Publication requires revision recheck or transactional isolation so concurrent individually valid writes cannot jointly violate a constraint.
- **CRA-020.5** `[CRAr]` Revalidate affected data on shape changes; clearly distinguish incremental supported validation from a full check. Timeout, runtime failure, cancellation and unavailable validator block required publication.
- **CRA-020.6** `[CRAr]` Bound CPU/memory/report size and restrict remote imports/SPARQL/JS/UDF execution. Required advanced profiles receive separate qualification rather than implicit enabling.
- **CRA-020.7** `[OCA]` Adopt pySHACL (Apache-2.0, pinned) as default validator inside an isolated worker; TopBraid SHACL API (Apache-2.0, JVM) is the differential oracle for the common profile (INV-48).
- **CRA-020.8** `[OCA]` Fix `export_shacl_shapes()` (rdf.py:369-425): emit `sh:datatype`, `sh:nodeKind`, `sh:minCount`, `sh:maxCount`, `sh:pattern`, `sh:class`, `sh:in`; convert `eoip:allowedEndpointPairs` into conformant `sh:targetSubjectsOf`/`sh:targetObjectsOf` plus `s
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-020

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/016/018/031. Sources G01/G02 and INV-22/47/48/49.
- [ ] CRA-020.1 [CRAr] Use a proven validator for declared SHACL Core 2017 coverage; keep extensions/profile versions explicit. A custom Python property checker must be labelled as such until replaced/qualified
- [ ] CRA-020.2 [CRAr] Enforce min/max cardinality, datatype/node kind, class, value sets, language/length/pattern/numeric bounds, logical and property-path constraints for the declared profile. Unsupported constraints must produce an explicit unsupported result, never conforms=true
- [ ] CRA-020.3 [CRAr] Produce standards-compatible reports with focus node, result path/value, source shape/constraint, severity and message, plus revision/engine/config and explicit truncation. Unknown datatype names fail validation setup
- [ ] CRA-020.4 [CRAr] Validate the candidate against required existing data and shape/ontology revision. Publication requires revision recheck or transactional isolation so concurrent individually valid writes cannot jointly violate a constraint
- [ ] CRA-020.5 [CRAr] Revalidate affected data on shape changes; clearly distinguish incremental supported validation from a full check. Timeout, runtime failure, cancellation and unavailable validator block required publication
- [ ] CRA-020.6 [CRAr] Bound CPU/memory/report size and restrict remote imports/SPARQL/JS/UDF execution. Required advanced profiles receive separate qualification rather than implicit enabling
- [ ] CRA-020.7 [OCA] Adopt pySHACL (Apache-2.0, pinned) as default validator inside an isolated worker; TopBraid SHACL API (Apache-2.0, JVM) is the differential oracle for the common profile (INV-48)
- [ ] CRA-020.8 [OCA] Fix exportshaclshapes() (rdf.py:369-425): emit sh:datatype, sh:nodeKind, sh:minCount, sh:maxCount, sh:pattern, sh:class, sh:in; convert eoip:allowedEndpointPairs into conformant sh:targetSubjectsOf/sh:targetObjectsOf plus sh:class constraints, and keep any remaining eoip: terms in a separately named extension profile (F3)
- [ ] CRA-020.9 [OCA] Keep SHACLValidationReport as the public type and the existing /ontology/validate contract unchanged (contract test); add POST /ontology/validate/shacl and the asynchronous POST /api/v1/semantic/validations (Idempotency-Key required) from the CRA OpenAPI fragment
- [ ] CRA-020.10 [AGG] Mutation API semantics: violation -> HTTP 422 with a W3C sh:ValidationReport and per-result codes (e.g. SHACLCARDINALITYVIOLATION, SHACLDATATYPEVIOLATION); unsupported constraint -> 422 UNSUPPORTEDCONSTRAINT; validator unavailable -> 503; zero triples committed in every failure case
- [ ] CRA-020.11 [OCA] Throughput qualification target: >= 20,000 nodes/s on 10M nodes with 500 shapes (benchmark manifest target)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/registry.py:24`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/registry.py#L24-L24), [`packages/eoip/claims/scanner.py:97`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/scanner.py#L97-L97), [`packages/eoip/claims/schema.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/schema.py#L42-L42), [`packages/eoip/ontology/rdf.py:381`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/rdf.py#L381-L381), [`packages/eoip/ontology/shacl_validator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/shacl_validator.py#L1-L1), [`scripts/build_master_suite.py:166`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L166-L166), [`scripts/enhance_master_suite.py:177`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L177-L177), [`scripts/patch_suite_and_dashboard.py:43`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L43-L43)
- tests: `scripts/test_cap_enrichment.py:35`, `scripts/test_master_caps_enrichment.py:49`, `tests/acceptance/test_claims_governance_acceptance.py:91`, `tests/contract/test_ontology_validate_contract.py:1`, `tests/integration/test_shacl_transactional.py:1`, `tests/semantic/test_shacl_benchmark.py:1`, `tests/semantic/test_shacl_differential.py:1`, `tests/semantic/test_shacl_strict.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-022 [P0] CRA-022: Ontology and Mapping Change Governance

- **Source:** `CRAr_cpccaggcc-requirements.md:1253-1289` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 36, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-022; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-022. Ontology and Mapping Change Governance

*Aggregated title: Ontology Change Governance, Visual Diffs & Pull-Request Workflows*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/018/019/020/031 | E (Governed knowledge) | M5 | F4 | ONT-012, ONT-013 | I14, I15, I16 | INV-01, INV-02, INV-03, INV-04, INV-07, INV-08, INV-09, INV-11, INV-12, INV-14, INV-15, INV-16, INV-22, INV-25, INV-32, INV-34, INV-38, INV-40, INV-41, INV-46, INV-48, INV-49, INV-50, INV-53 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/018/019/020/031. Sources INV-02/08/12/15/16/25/34/40/46.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-022.1** `[CRAr]` Implement durable draft -> validation -> review -> approval -> publication -> superseded/rollback lifecycle with explicit roles, separation of duties and audited decisions.
- **CRA-022.2** `[CRAr]` Diff semantic statements, imports, shapes, mappings, labels and policy implications rather than only text files. Display impacted data, queries, indexes, sources and actions with bounded analysis.
- **CRA-022.3** `[CRAr]` Bind approval to exact candidate, base, ontology, shapes, mapping and policy revisions. Concurrent edits produce conflict/precondition errors; stale approval cannot authorize changed content.
- **CRA-022.4** `[CRAr]` Support scheduled/atomic publication and compatible rollback with immutable manifests, consumer acknowledgement, explicit partial failure and repair. Retain history and tenant isolation through restart.
- **CRA-022.5** `[CRAr]` Run competency questions, profile/consistency/shapes checks, domain review and migration dry-runs as release gates. No generated or agent-written ontology bypasses these gates.
- **CRA-022.6** `[OCA]` Preserve the existing GitOps core (`gitops.py`, 793 LOC: branches, PRs with review gates, semantic diff, impact analysis `run_ontology_impact_analysis`, migration-script generation gitops.py:545, rollback receipts gitops.py:613-733, semver gitops.py:733, release packaging) and `gitops_router.py` endpoints. New capabilities attach through ports. Any change to `gitops.py`, `manifest.py` or `packs.py` requires a recorded Lead Developer review (OR7).
- **CRA-022.7** `[OCA]` Offline ontology pitfall scanner (ONT-013, INV-49) in `packages/eoip/ontology/lint/` detecting at least 20 antipattern classes (including missing domain/range, circular hierarc
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-022

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/018/019/020/031. Sources INV-02/08/12/15/16/25/34/40/46.
- [ ] CRA-022.1 [CRAr] Implement durable draft -> validation -> review -> approval -> publication -> superseded/rollback lifecycle with explicit roles, separation of duties and audited decisions
- [ ] CRA-022.2 [CRAr] Diff semantic statements, imports, shapes, mappings, labels and policy implications rather than only text files. Display impacted data, queries, indexes, sources and actions with bounded analysis
- [ ] CRA-022.3 [CRAr] Bind approval to exact candidate, base, ontology, shapes, mapping and policy revisions. Concurrent edits produce conflict/precondition errors; stale approval cannot authorize changed content
- [ ] CRA-022.4 [CRAr] Support scheduled/atomic publication and compatible rollback with immutable manifests, consumer acknowledgement, explicit partial failure and repair. Retain history and tenant isolation through restart
- [ ] CRA-022.5 [CRAr] Run competency questions, profile/consistency/shapes checks, domain review and migration dry-runs as release gates. No generated or agent-written ontology bypasses these gates
- [ ] CRA-022.6 [OCA] Preserve the existing GitOps core (gitops.py, 793 LOC: branches, PRs with review gates, semantic diff, impact analysis runontologyimpactanalysis, migration-script generation gitops.py:545, rollback receipts gitops.py:613-733, semver gitops.py:733, release packaging) and gitopsrouter.py endpoints. New capabilities attach through ports. Any change to gitops.py, manifest.py or packs.p
- [ ] CRA-022.7 [OCA] Offline ontology pitfall scanner (ONT-013, INV-49) in packages/eoip/ontology/lint/ detecting at least 20 antipattern classes (including missing domain/range, circular hierarchy, equivalent-class loops, unconnected elements, naming inconsistency, missing labels/definitions, deprecated-term use, inverse-property conflicts); every finding has severity and remediation hint; it runs as 
- [ ] CRA-022.8 [AGG] PR gate pipeline: profile check, consistency (CRA-019), SHACL instance regression (CRA-020), pitfall lint, competency questions, semantic diff and impact; production-branch merge requires two distinct steward approvals
- [ ] CRA-022.9 [AGG] Semantic AST diff (added/removed classes and properties, changed cardinalities, changed subsumption) is shown visually in the UI (CRA-030), not only as text lines
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/positioning_pack.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/positioning_pack.py#L10-L10), [`packages/eoip/ontology/governance.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/governance.py#L1-L1), [`packages/eoip/ontology/lint/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/lint/__init__.py#L1-L1), [`packages/eoip/ontology/lint/rules.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/lint/rules.py#L1-L1), [`packages/eoip/ontology/lint/scanner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/lint/scanner.py#L1-L1), [`scripts/build_master_suite.py:232`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L232-L232), [`scripts/enhance_master_suite.py:238`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L238-L238), [`scripts/patch_suite_and_dashboard.py:153`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L153-L153)
- tests: `scripts/test_cap_enrichment.py:101`, `scripts/test_master_caps_enrichment.py:115`, `tests/acceptance/test_claims_governance_acceptance.py:156`, `tests/integration/test_gitops_pr_gate.py:1`, `tests/semantic/test_lint_rules.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-024 [P0] CRA-024: Typed Query, Federation and Semantic Planning

- **Source:** `CRAr_cpccaggcc-requirements.md:1328-1368` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-024; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-024. Typed Query, Federation and Semantic Planning

*Aggregated title: Cost-Based Federated Query Engine (SPARQL 1.1, ANSI SQL & openCypher)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/016/017/019/031 | F (Usable value) | M5 | G06, G13 | ONT-002, ONT-003 | I2, I3 | INV-03, INV-16, INV-17, INV-18, INV-19, INV-21, INV-23, INV-26, INV-27, INV-28, INV-29, INV-33, INV-34, INV-35, INV-42 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/016/017/019/031. Sources G06/G13 and INV-18/19/21/23/27/28/29/35.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-024.1** `[CRAr]` Publish an exact grammar/capability manifest per dialect/backend: supported EQL/EOQL/OSQL subsets, qualified SPARQL and optional SQL/Cypher/Gremlin/GQL adapters. A language name or exported template is not an executable implementation.
- **CRA-024.2** `[CRAr]` Use typed parsed plans and parameterization; reject unsupported constructs and unauthorized operations. No concatenated raw user strings enter privileged backend code.
- **CRA-024.3** `[CRAr]` Provide validate/explain/cost/profile/execute/cancel with actual execution information, bounded depth/rows/time and source budgets. Explain output must correspond to the actual plan and reasoning mode.
- **CRA-024.4** `[CRAr]` Implement qualified OBDA/federation with source auth delegation, null/bag/set/type semantics, join pushdown, partial-source outcomes, snapshot/freshness and schema-drift handling.
- **CRA-024.5** `[CRAr]` Scope templates/history/results and caches; redact sensitive literals. Prevent unauthorized source or graph selection and export of hidden intermediate facts.
- **CRA-024.6** `[CRAr]` Separate warmed endpoint benchmarks from CLI startup/setup. Compare materialized and virtual results on declared semantics, not only query syntax.
- **CRA-024.7** `[OCA]` SPARQL 1.1 endpoint `GET/POST /sparql` per the SPARQL 1.1 Protocol, executed on a qualified RDF backend or translated to the LPG plan; passes the W3C protocol tests in scope; unbounded property paths are rejected with a clear error, never hang.
- **CRA-024.8** `[AGG]` Optional adapters, each with an exact grammar manifest: ANSI SQL views over the ontology (DataFusion/Trino candidates), openCypher/GQL over the property projection, GraphQL generated from shapes (extending `schema_gen.py`).
- **CRA-024.9** `[AGG]` Default budgets: d
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-024

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/016/017/019/031. Sources G06/G13 and INV-18/19/21/23/27/28/29/35.
- [ ] CRA-024.1 [CRAr] Publish an exact grammar/capability manifest per dialect/backend: supported EQL/EOQL/OSQL subsets, qualified SPARQL and optional SQL/Cypher/Gremlin/GQL adapters. A language name or exported template is not an executable implementation
- [ ] CRA-024.2 [CRAr] Use typed parsed plans and parameterization; reject unsupported constructs and unauthorized operations. No concatenated raw user strings enter privileged backend code
- [ ] CRA-024.3 [CRAr] Provide validate/explain/cost/profile/execute/cancel with actual execution information, bounded depth/rows/time and source budgets. Explain output must correspond to the actual plan and reasoning mode
- [ ] CRA-024.4 [CRAr] Implement qualified OBDA/federation with source auth delegation, null/bag/set/type semantics, join pushdown, partial-source outcomes, snapshot/freshness and schema-drift handling
- [ ] CRA-024.5 [CRAr] Scope templates/history/results and caches; redact sensitive literals. Prevent unauthorized source or graph selection and export of hidden intermediate facts
- [ ] CRA-024.6 [CRAr] Separate warmed endpoint benchmarks from CLI startup/setup. Compare materialized and virtual results on declared semantics, not only query syntax
- [ ] CRA-024.7 [OCA] SPARQL 1.1 endpoint GET/POST /sparql per the SPARQL 1.1 Protocol, executed on a qualified RDF backend or translated to the LPG plan; passes the W3C protocol tests in scope; unbounded property paths are rejected with a clear error, never hang
- [ ] CRA-024.8 [AGG] Optional adapters, each with an exact grammar manifest: ANSI SQL views over the ontology (DataFusion/Trino candidates), openCypher/GQL over the property projection, GraphQL generated from shapes (extending schemagen.py)
- [ ] CRA-024.9 [AGG] Default budgets: deadline 30 s, memory 4 GiB per query, 10,000 rows per page, traversal depth 3; tenant quotas may only lower them; budgets reuse the existing tokenbudget/ mechanism where applicable
- [ ] test with a recorded session)
- [ ] CRA-024.11 [OCA] RDF backend port (ONT-003): Apache Jena Fuseki reference, GraphDB certified option; a customer's existing GraphDB is targetable by configuration alone
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/registry.py:26`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/registry.py#L26-L26), [`packages/eoip/federation/obda.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/federation/obda.py#L1-L1), [`packages/eoip/graph/backends.py:363`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/backends.py#L363-L363), [`packages/eoip/graph/rdf_backend.py:246`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/graph/rdf_backend.py#L246-L246), [`packages/eoip/qlang/manifest_registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qlang/manifest_registry.py#L1-L1), [`packages/eoip/query/benchmarks.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/benchmarks.py#L1-L1), [`packages/eoip/query/bi_connectivity.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/bi_connectivity.py#L1-L1), [`packages/eoip/query/plan_engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/query/plan_engine.py#L1-L1)
- tests: `tests/query/test_query_semantics_oracle.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-026 [P0] CRA-026: Evidence-Bound AI and Ontology Learning

- **Source:** `CRAr_cpccaggcc-requirements.md:1409-1454` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 13, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-026; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-026. Evidence-Bound AI and Ontology Learning

*Aggregated title: Evidence-Bound GraphRAG & Calibrated Context Assembly*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/014/019/020/023/025/040 | F (Usable value) | M6 | — | ONT-006 | I9, I12, I13 | INV-04, INV-10, INV-11, INV-13, INV-14, INV-16, INV-34, INV-49, INV-51, INV-52, INV-53, INV-54 | X-15 | — |

**Base statement:** Priority P1. Depends on CRA-003/014/019/020/023/025/040. Sources INV-04/11/14/16/49/51/52/53/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-026.1** `[CRAr]` Keep extraction/classification/alignment/answer suggestions distinct from asserted facts and logical entailments. Record provider/model/prompt/tool/config revisions, evidence spans and policy context.
- **CRA-026.2** `[CRAr]` Build bounded authorized context with token budgets, evidence prioritization, freshness and conflicts. Emit clause-level evidence links to actual permitted source revisions; unknown/insufficient evidence produces abstention or explicit uncertainty.
- **CRA-026.3** `[CRAr]` Support true streaming/cancellation where configured with cleanup and accurate lifecycle. A graph event feed or simulated token timer is not answer streaming. Prevent partial cancelled output from being saved as an accepted complete answer.
- **CRA-026.4** `[CRAr]` Apply independent egress/DLP policy before provider calls. No unapproved endpoint/model downloads or external linting services in no-egress mode; record provider usage/cost without leaking raw data.
- **CRA-026.5** `[CRAr]` Treat retrieved documents and tool outputs as untrusted data. Prompt instructions cannot grant tools, alter trusted scope or bypass publication/action approval.
- **CRA-026.6** `[CRAr]` Evaluate factual/evidence correctness, abstention, prompt-injection resistance, calibration, domain/language coverage and quality drift against held-out data. Do not call a raw classifier score a probability without calibration evidence.
- **CRA-026.7** `[AGG]` GraphRAG pipeline: vector entry points -> bounded multi-hop traversal (default depth 2, max 200 nodes) -> ACL pruning -> context assembly; every sentence cites a `CanonicalAssertion` ID and an `EvidenceLocator`.
- **CRA-026.8** `[RES]` Abstention: when evidence is insufficient or calibrated confidence is below the configured threshold the answer states that it cannot be answered fr
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-026

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/014/019/020/023/025/040. Sources INV-04/11/14/16/49/51/52/53/54.
- [ ] CRA-026.1 [CRAr] Keep extraction/classification/alignment/answer suggestions distinct from asserted facts and logical entailments. Record provider/model/prompt/tool/config revisions, evidence spans and policy context
- [ ] CRA-026.2 [CRAr] Build bounded authorized context with token budgets, evidence prioritization, freshness and conflicts. Emit clause-level evidence links to actual permitted source revisions; unknown/insufficient evidence produces abstention or explicit uncertainty
- [ ] CRA-026.3 [CRAr] Support true streaming/cancellation where configured with cleanup and accurate lifecycle. A graph event feed or simulated token timer is not answer streaming. Prevent partial cancelled output from being saved as an accepted complete answer
- [ ] CRA-026.4 [CRAr] Apply independent egress/DLP policy before provider calls. No unapproved endpoint/model downloads or external linting services in no-egress mode; record provider usage/cost without leaking raw data
- [ ] CRA-026.5 [CRAr] Treat retrieved documents and tool outputs as untrusted data. Prompt instructions cannot grant tools, alter trusted scope or bypass publication/action approval
- [ ] CRA-026.6 [CRAr] Evaluate factual/evidence correctness, abstention, prompt-injection resistance, calibration, domain/language coverage and quality drift against held-out data. Do not call a raw classifier score a probability without calibration evidence
- [ ] CRA-026.7 [AGG] GraphRAG pipeline: vector entry points -> bounded multi-hop traversal (default depth 2, max 200 nodes) -> ACL pruning -> context assembly; every sentence cites a CanonicalAssertion ID and an EvidenceLocator
- [ ] CRA-026.8 [RES] Abstention: when evidence is insufficient or calibrated confidence is below the configured threshold the answer states that it cannot be answered from authorized knowledge. The AGG threshold 0.85 is the initial value only after calibration on the held-out set; gates are CRAr's evidence precision >= 0.98, coverage >= 0.95 and abstention >= 0.95 (X-15)
- [ ] CRA-026.9 [AGG] Air-gapped deployments route generation only to self-hosted model servers (vLLM, Ollama or TGI candidates) with zero external traffic
- [ ] CRA-026.10 [PRM] Context-window governance per configured model: maximum input and output token limits come from the provider/model manifest and are recorded with the model revision; budgets are measured with that model's own tokenizer (character or word estimates are not budgets); a context that would exceed the limit is reduced by a declared policy (prioritize evidence, then deduplicate, then dr
- [ ] CRA-026.11 [PRM] Reduction is disclosed: when authorized evidence is dropped to fit the window, the answer states that evidence was omitted and how many items, and offers the omitted list to the principal; an answer built from a reduced context is not labelled complete. Restricted evidence is filtered before budgeting so the budget and the omission count never reveal its existence
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ai/graphrag.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ai/graphrag.py#L1-L1), [`packages/eoip/rag/dual_level_diffusion.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/rag/dual_level_diffusion.py#L1-L1), [`scripts/build_master_suite.py:262`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L262-L262), [`scripts/enhance_master_suite.py:175`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L175-L175), [`scripts/patch_suite_and_dashboard.py:41`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_suite_and_dashboard.py#L41-L41)
- tests: `scripts/test_master_caps_enrichment.py:145`, `tests/ai/test_dual_level_hipporag.py:1`, `tests/ai/test_graphrag_grounding.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-028 [P0] CRA-028: Temporal Knowledge, Impact and Simulation

- **Source:** `CRAr_cpccaggcc-requirements.md:1494-1525` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 5, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-028; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-028. Temporal Knowledge, Impact and Simulation

*Aggregated title: Bitemporal Graph Navigation, Blast-Radius Simulation & Time Travel*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-010/019/023/031 | E (Governed knowledge) | M6 | G14 | — | — | INV-25, INV-36, INV-37, INV-38, INV-40 | — | — |

**Base statement:** Priority P1. Depends on CRA-010/019/023/031. Sources G14 and INV-25/36/37/38/40.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-028.1** `[CRAr]` Model valid time, transaction/observation time, corrections, retractions, source revision and lineage explicitly. Timestamp fields alone do not establish bitemporal query behavior.
- **CRA-028.2** `[CRAr]` Support authorized as-of queries, version diffs, provenance and bounded historical snapshots. Retention/hold/deletion rules constrain what history may be served.
- **CRA-028.3** `[CRAr]` Separate observed relationships, deterministic graph impact, heuristic paths, stochastic estimates and domain simulation outputs in both API and GUI.
- **CRA-028.4** `[CRAr]` Simulations require versioned model/assumptions/inputs, seed, uncertainty and validation protocol. Random-walk frequency is not a calibrated failure probability or a causal intervention estimate.
- **CRA-028.5** `[CRAr]` Preserve actual path/hop evidence and cost semantics; do not summarize a multi-hop result as a fabricated two-node explanation. Approval/execution of operational action remains CRA-027.
- **CRA-028.6** `[AGG]` Historical reads use an explicit `as_of` parameter on the query API (and an `eoip:asOf` service parameter for SPARQL, because standard SPARQL has no AS OF clause), returning the authorized state at that valid/transaction time.
- **CRA-028.7** `[AGG]` Deterministic graph algorithms (BFS, Dijkstra, PageRank, Tarjan SCC) replace heuristic random-walk summaries for impact paths (G14); existing `graph/paths.py`, `algorithms.py`, `community.py`, `process_mining.py` are reused and qualified.
- **CRA-028.8** `[AGG]` Blast-radius output lists impacted services, teams and processes with severity scores explicitly labelled heuristic unless a validated model exists.
- **CRA-028.9** `[GN]` Learned impact propagation (CRA-044) is returned as a proposed, labelled estimate beside the deterministic blast radius of CRA-028.7/028.8 with its dual-path status (CRA-045.3); it never replaces or reorders the determ
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-028

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-010/019/023/031. Sources G14 and INV-25/36/37/38/40.
- [ ] CRA-028.1 [CRAr] Model valid time, transaction/observation time, corrections, retractions, source revision and lineage explicitly. Timestamp fields alone do not establish bitemporal query behavior
- [ ] CRA-028.2 [CRAr] Support authorized as-of queries, version diffs, provenance and bounded historical snapshots. Retention/hold/deletion rules constrain what history may be served
- [ ] CRA-028.3 [CRAr] Separate observed relationships, deterministic graph impact, heuristic paths, stochastic estimates and domain simulation outputs in both API and GUI
- [ ] CRA-028.4 [CRAr] Simulations require versioned model/assumptions/inputs, seed, uncertainty and validation protocol. Random-walk frequency is not a calibrated failure probability or a causal intervention estimate
- [ ] CRA-028.5 [CRAr] Preserve actual path/hop evidence and cost semantics; do not summarize a multi-hop result as a fabricated two-node explanation. Approval/execution of operational action remains CRA-027
- [ ] CRA-028.6 [AGG] Historical reads use an explicit asof parameter on the query API (and an eoip:asOf service parameter for SPARQL, because standard SPARQL has no AS OF clause), returning the authorized state at that valid/transaction time
- [ ] CRA-028.7 [AGG] Deterministic graph algorithms (BFS, Dijkstra, PageRank, Tarjan SCC) replace heuristic random-walk summaries for impact paths (G14); existing graph/paths.py, algorithms.py, community.py, processmining.py are reused and qualified
- [ ] CRA-028.8 [AGG] Blast-radius output lists impacted services, teams and processes with severity scores explicitly labelled heuristic unless a validated model exists
- [ ] CRA-028.9 [GN] Learned impact propagation (CRA-044) is returned as a proposed, labelled estimate beside the deterministic blast radius of CRA-028.7/028.8 with its dual-path status (CRA-045.3); it never replaces or reorders the deterministic result
- [ ] obligation CRA-028.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] late events, corrections, clock skew, merges/splits, permission changes and retention across historical reads. Repeat seeded runs, compare sensitivity/gold scenarios, cancel expensive work and ensure simulated facts cannot enter asserted production knowledge without review
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/temporal/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/temporal/__init__.py#L1-L1), [`packages/eoip/temporal/authorized_as_of.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/temporal/authorized_as_of.py#L1-L1), [`packages/eoip/temporal/deterministic_graph.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/temporal/deterministic_graph.py#L1-L1), [`packages/eoip/temporal/impact_simulator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/temporal/impact_simulator.py#L1-L1), [`packages/eoip/temporal/models.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/temporal/models.py#L1-L1)
- tests: `tests/semantic/test_temporal_simulation.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-031 [P0] CRA-031: Durable Jobs, Publication and Event Delivery

- **Source:** `CRAr_cpccaggcc-requirements.md:1592-1626` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-031; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-031. Durable Jobs, Publication and Event Delivery

*Aggregated title: Durable Distributed Jobs & Dead-Letter Queue (DLQ)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-002/003 | B (Safe platform) | M8 | G16 | — | — | INV-12, INV-22, INV-29, INV-30, INV-31, INV-36, INV-39, INV-41, INV-44, INV-45, INV-47 | — | — |

**Base statement:** Priority P0. Depends on CRA-002/003. Sources G16 and INV-12/25/29/30/31/36/39/41/44/45.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-031.1** `[CRAr]` Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status. No process-local state as the only job authority in real deployments.
- **CRA-031.2** `[CRAr]` Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/reconciliation and expose incomplete states.
- **CRA-031.3** `[CRAr]` Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer credentials in URLs.
- **CRA-031.4** `[CRAr]` Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue authority and audit.
- **CRA-031.5** `[CRAr]` Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on the selected real durable backend.
- **CRA-031.6** `[AGG]` All jobs live in a durable database queue; workers hold leases with heartbeats every 10 s (lease TTL 30 s); an expired lease is reclaimed from the last valid checkpoint.
- **CRA-031.7** `[AGG]` Repeatedly failing payloads move to a governed DLQ with redacted diagnostics (stack trace with secrets removed), reason, attempt count and replay authority.

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| heartbeat / lease TTL | 10 s / 30 s | AGG + RES |

**Acceptance obligation CRA-031.A** (only after every clause above is ACCEPTED):

- `[CRAr]` kill process/network/storage at each commit boundary; race two workers; replay a DLQ item; cancel and revoke scope mid-job. Demonstrate expected published effects, event sequence, cursor and restored job state using independent read-back.
- `
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-031

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-002/003. Sources G16 and INV-12/25/29/30/31/36/39/41/44/45.
- [ ] CRA-031.1 [CRAr] Reuse and qualify the existing job/control plane for durable queueing, scope, leases, heartbeats, deadlines, retries, cancellation and terminal status. No process-local state as the only job authority in real deployments
- [ ] CRA-031.2 [CRAr] Persist publication intent/mutation/outbox identity consistently. Use a real transaction where available; otherwise implement documented idempotency/reconciliation and expose incomplete states
- [ ] CRA-031.3 [CRAr] Define replay/resume/retention/gap semantics for events and consumers, bounded buffers and per-principal authorization. Never put durable bearer credentials in URLs
- [ ] CRA-031.4 [CRAr] Enforce retry policy by operation safety; do not blindly retry mutations. Preserve poison events in a governed DLQ with reason, redaction, requeue authority and audit
- [ ] CRA-031.5 [CRAr] Fence expired leases/workers and prevent cancelled/revoked jobs from committing later. API/worker restarts and multi-instance claims must be tested on the selected real durable backend
- [ ] CRA-031.6 [AGG] All jobs live in a durable database queue; workers hold leases with heartbeats every 10 s (lease TTL 30 s); an expired lease is reclaimed from the last valid checkpoint
- [ ] CRA-031.7 [AGG] Repeatedly failing payloads move to a governed DLQ with redacted diagnostics (stack trace with secrets removed), reason, attempt count and replay authority
- [ ] obligation CRA-031.A (only after every clause above is ACCEPTED)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/jobs.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/jobs.py#L1-L1), [`scripts/build_master_suite.py:91`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L91-L91), [`scripts/enhance_master_suite.py:7`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L7-L7), [`scripts/patch_dashboard_html.py:117`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/patch_dashboard_html.py#L117-L117)
- tests: `tests/integration/test_durable_jobs.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-032 [P0] CRA-032: Observability and Operational Truth

- **Source:** `CRAr_cpccaggcc-requirements.md:1627-1657` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 7, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-032; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-032. Observability and Operational Truth

*Aggregated title: OpenTelemetry Tracing, Prometheus Metrics & Audit Observability*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/003/031 | B (Safe platform) | M8 | — | — | — | INV-44 | — | — |

**Base statement:** Priority P0. Depends on CRA-001/003/031. Sources INV-39/44/45 and all D16 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-032.1** `[CRAr]` Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and stage timings.
- **CRA-032.2** `[CRAr]` Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference amplification and model cost/quality. Unknown/stale telemetry is distinct from zero/healthy.
- **CRA-032.3** `[CRAr]` Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query literals/raw prompts unless explicitly authorized under retention policy.
- **CRA-032.4** `[CRAr]` Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success health endpoints.
- **CRA-032.5** `[CRAr]` Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry alone.
- **CRA-032.6** `[AGG]` Prometheus metrics (bounded labels): `eoip_ingestion_triples_total{source,status}`, `eoip_shacl_validation_duration_seconds{shape_id,conforms}`, `eoip_query_execution_duration_seconds{dialect}` (tenant only in access-controlled traces, not unbounded labels), `eoip_reasoning_amplification_ratio{ruleset}`, `eoip_acl_derivation_pruned_triples_total`, `eoip_outbox_action_lag_seconds{target_system}`.
- **CRA-032.7** `[AGG]` Every API response carries a W3C `traceparent`; security-relevant events (login, permission change, ontology merge, action execution) emit structured JSON audit records with principal, timestamp, action and payload digest.
- **CRA-032.8** `[OCA]` Alerting rules (currently absent) are defined for queue age, projection/policy lag, connector failure, validator unavailability and outbox lag, each linked to a runbook.

**Acceptance obligation CRA-032.A** (only af
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-032

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001/003/031. Sources INV-39/44/45 and all D16 gaps.
- [ ] CRA-032.1 [CRAr] Integrate existing structured logging, OpenTelemetry and metrics with source event/job/semantic/publication/projection/query/action correlation and stage timings
- [ ] CRA-032.2 [CRAr] Record latency/throughput/error/cancel/denied/unsupported/timeout, queue age, source freshness, projection/policy lag, resource usage, inference amplification and model cost/quality. Unknown/stale telemetry is distinct from zero/healthy
- [ ] CRA-032.3 [CRAr] Restrict metrics-label cardinality and sensitive content; protect tenant-specific diagnostics, traces and support bundles. Redact credentials/query literals/raw prompts unless explicitly authorized under retention policy
- [ ] CRA-032.4 [CRAr] Provide dashboards and alerts tied to actual measured service behavior, thresholds and runbooks. Avoid initialized example metrics or always-success health endpoints
- [ ] CRA-032.5 [CRAr] Test collector absence/backpressure without corrupting critical data flows. Audit and publication durability must not depend on best-effort telemetry alone
- [ ] CRA-032.6 [AGG] Prometheus metrics (bounded labels): eoipingestiontriplestotal{source,status}, eoipshaclvalidationdurationseconds{shapeid,conforms}, eoipqueryexecutiondurationseconds{dialect} (tenant only in access-controlled traces, not unbounded labels), eoipreasoningamplificationratio{ruleset}, eoipaclderivationprunedtriplestotal, eoipoutboxactionlagseconds{targetsystem}
- [ ] CRA-032.7 [AGG] Every API response carries a W3C traceparent; security-relevant events (login, permission change, ontology merge, action execution) emit structured JSON audit records with principal, timestamp, action and payload digest
- [ ] CRA-032.8 [OCA] Alerting rules (currently absent) are defined for queue age, projection/policy lag, connector failure, validator unavailability and outbox lag, each linked to a runbook
- [ ] obligation CRA-032.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] trigger a real failed connector, timeout validator, stuck lease and policy-stale index. Confirm trace correlation, correct alert/state and no secrets in logs/metrics/bundles. Validate observed metric values against independent counters/workload timestamps
- [ ] [MERGED] /metrics conforms to the Prometheus text format; a sampled request's traceparent resolves to a complete trace (AGG)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/observability/truth.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/observability/truth.py#L1-L1)
- tests: `tests/integration/test_observability_truth.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-033 [P0] CRA-033: Backup, Restore and Failure Recovery

- **Source:** `CRAr_cpccaggcc-requirements.md:1658-1693` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-033; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-033. Backup, Restore and Failure Recovery

*Aggregated title: Enterprise Backup, Point-In-Time Recovery (PITR) & Disaster Recovery*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-018/031/032/040 | H (Deploy and migrate) | M8 | — | — | — | INV-12, INV-20, INV-23, INV-25, INV-37, INV-45 | X-09 | — |

**Base statement:** Priority P0. Depends on CRA-018/031/032/040. Sources INV-12/20/23/25/37/45 and D18 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-033.1** `[CRAr]` Inventory authoritative state: canonical graph, control database, ontology/import/release packages, raw references, identity/policy, outbox/cursors, secrets/KMS recovery metadata and rebuild watermarks.
- **CRA-033.2** `[CRAr]` Define consistent encrypted backups/snapshots and retention for each supported deployment/backend, with access controls, immutability where appropriate and off-site failure separation.
- **CRA-033.3** `[CRAr]` Implement restore into a clean environment with revision/checksum/query/ACL consistency checks and projection rebuild. Restore secrets through the approved process, not by copying plaintext into bundles.
- **CRA-033.4** `[CRAr]` Measure P1 RPO <=15 min and RTO <=4 h for the declared tested failure model; document observed values, exceptions and exact data loss. Do not infer P2/region HA from a local restore.
- **CRA-033.5** `[CRAr]` Rehearse partial backup failure, corrupt snapshot, lost key, concurrent writes, API/worker restart and failed upgrade. Fence old writers and prevent event replay from resurrecting deleted/revoked records.
- **CRA-033.6** `[AGG]` Online non-blocking snapshots plus transaction-journal replay provide point-in-time recovery; default PITR window 30 days, shortened automatically where retention/deletion policy requires.
- **CRA-033.7** `[RES]` P1 objectives RPO <= 15 min and RTO <= 4 h (CRAr). The AGG figure 'RTO <= 4 h for a 500M-triple restore' is a P2 qualification target, not a P1 claim (X-09).

**Configuration defaults:**

| Setting | Default | Origin |
|---|---|---|
| PITR window | 30 days (policy-limited) | AGG |

**Acceptance obligation CRA-033.A** (only after every clause above is ACCEPTED):

- `[CRAr]` timed independent restore with business queries, ontology revisions, source cursors and adversarial authorization checked after recovery. An archive file or successful backup API response alone is
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-033

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-018/031/032/040. Sources INV-12/20/23/25/37/45 and D18 gaps.
- [ ] CRA-033.1 [CRAr] Inventory authoritative state: canonical graph, control database, ontology/import/release packages, raw references, identity/policy, outbox/cursors, secrets/KMS recovery metadata and rebuild watermarks
- [ ] CRA-033.2 [CRAr] Define consistent encrypted backups/snapshots and retention for each supported deployment/backend, with access controls, immutability where appropriate and off-site failure separation
- [ ] CRA-033.3 [CRAr] Implement restore into a clean environment with revision/checksum/query/ACL consistency checks and projection rebuild. Restore secrets through the approved process, not by copying plaintext into bundles
- [ ] CRA-033.4 [CRAr] Measure P1 RPO <=15 min and RTO <=4 h for the declared tested failure model; document observed values, exceptions and exact data loss. Do not infer P2/region HA from a local restore
- [ ] CRA-033.5 [CRAr] Rehearse partial backup failure, corrupt snapshot, lost key, concurrent writes, API/worker restart and failed upgrade. Fence old writers and prevent event replay from resurrecting deleted/revoked records
- [ ] CRA-033.6 [AGG] Online non-blocking snapshots plus transaction-journal replay provide point-in-time recovery; default PITR window 30 days, shortened automatically where retention/deletion policy requires
- [ ] CRA-033.7 [RES] P1 objectives RPO <= 15 min and RTO <= 4 h (CRAr). The AGG figure 'RTO <= 4 h for a 500M-triple restore' is a P2 qualification target, not a P1 claim (X-09)
- [ ] obligation CRA-033.A (only after every clause above is ACCEPTED)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/recovery/enterprise_recovery.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/recovery/enterprise_recovery.py#L1-L1)
- tests: `tests/acceptance/test_backup_restore_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-035 [P0] CRA-035: Commercial Packaging and Supply-Chain Compliance

- **Source:** `CRAr_cpccaggcc-requirements.md:1730-1762` (heading) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-035; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-035. Commercial Packaging and Supply-Chain Compliance

*Aggregated title: Supply-Chain Compliance, SBOM & Licensing Isolation*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/002 | B (Safe platform) | M8 | G17 | — | I11, I19 | INV-02, INV-05, INV-07, INV-10, INV-13, INV-15, INV-21, INV-23, INV-28, INV-32, INV-35, INV-45, INV-46, INV-47, INV-49, INV-50, INV-52, INV-54, INV-55 | X-01, X-02, X-16, X-21, X-30 | H-04 |

**Base statement:** Priority P0. Depends on CRA-001/002. Sources G17 and INV-02/05/13/15/21/32/35/46/49/50/54/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-035.1** `[CRAr]` Preserve proprietary EOIP-owned licensing and upstream component rights. Do not relabel third-party files or assume all files in an owned directory are owned.
- **CRA-035.2** `[CRAr]` Produce exact shipped SBOMs and license/notices/source-obligation records for Python, npm/browser bundles, VSIX, OS/container packages, JVM/WASM/native engines, plugins, models, datasets, vocabularies and assets.
- **CRA-035.3** `[CRAr]` Resolve GPL/AGPL/LGPL/OEM/embedding/redistribution and data/model terms for the actual integration and both SaaS/installed profiles. Existing `extract-msg` and ownership/contract questions require explicit resolution, not automated green status.
- **CRA-035.4** `[CRAr]` Sign/hash release artifacts and plugin packages, retain build provenance and dependency locks, and make notices available online and offline as appropriate. An installed dependency list is not proof of notices shipped to customers.
- **CRA-035.5** `[CRAr]` Qualify installation/upgrade/uninstall and air-gap operation with no unapproved runtime downloads. Entitlements must disable unavailable modules truthfully without granting data access.
- **CRA-035.6** `[AGG]` Generate CycloneDX or SPDX SBOMs for Python, npm/browser bundles, containers, JVM workers, models and datasets with tools such as syft and a license checker; CI fails on unapproved licenses.
- **CRA-035.7** `[OCA]` Copyleft policy: GPL/AGPL code is never linked into or bundled with the distributed core; GPL/AGPL servers (Neo4j Community GPLv3, Virtuoso OSE GPLv2) are reachable only over network protocols; WebProtégé is not integrated; HermiT (LGPL) is an optional separately installed plugin; TerminusDB is blocked pending Legal; SNOMED-CT is customer-provided only.
- **CRA-035.8** `[OCA]` Depende
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-035

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001/002. Sources G17 and INV-02/05/13/15/21/32/35/46/49/50/54/55.
- [ ] CRA-035.1 [CRAr] Preserve proprietary EOIP-owned licensing and upstream component rights. Do not relabel third-party files or assume all files in an owned directory are owned
- [ ] CRA-035.2 [CRAr] Produce exact shipped SBOMs and license/notices/source-obligation records for Python, npm/browser bundles, VSIX, OS/container packages, JVM/WASM/native engines, plugins, models, datasets, vocabularies and assets
- [ ] CRA-035.3 [CRAr] Resolve GPL/AGPL/LGPL/OEM/embedding/redistribution and data/model terms for the actual integration and both SaaS/installed profiles. Existing extract-msg and ownership/contract questions require explicit resolution, not automated green status
- [ ] CRA-035.4 [CRAr] Sign/hash release artifacts and plugin packages, retain build provenance and dependency locks, and make notices available online and offline as appropriate. An installed dependency list is not proof of notices shipped to customers
- [ ] CRA-035.5 [CRAr] Qualify installation/upgrade/uninstall and air-gap operation with no unapproved runtime downloads. Entitlements must disable unavailable modules truthfully without granting data access
- [ ] CRA-035.6 [AGG] Generate CycloneDX or SPDX SBOMs for Python, npm/browser bundles, containers, JVM workers, models and datasets with tools such as syft and a license checker; CI fails on unapproved licenses
- [ ] CRA-035.7 [OCA] Copyleft policy: GPL/AGPL code is never linked into or bundled with the distributed core; GPL/AGPL servers (Neo4j Community GPLv3, Virtuoso OSE GPLv2) are reachable only over network protocols; WebProtégé is not integrated; HermiT (LGPL) is an optional separately installed plugin; TerminusDB is blocked pending Legal; SNOMED-CT is customer-provided only
- [ ] CRA-035.8 [OCA] Dependency decision table (section 13) is the authoritative allowlist input to the CI license gate; every row cites the exact artifact and license snapshot
- [ ] CRA-035.9 [GN] The numerical stack (section 13 rows for numpy, scipy, scikit-learn, torch, torch-geometric, transformers, sentence-transformers, snntorch) enters the SBOM per tier; CUDA-dependent nvidia- packages are excluded from every artifact EOIP distributes (decision H-16 accepted: not redistributable); DGL and networkx are not added
- [ ] obligation CRA-035.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] inspect actual wheel/image/browser/VSIX/air-gap artifacts and compare embedded inventories/notices with SBOM. Tamper with a plugin/artifact and reject activation. Obtain documented legal/owner approvals; agent-written licensing documents alone cannot clear distribution rights
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/compliance/sbom.py:3`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/compliance/sbom.py#L3-L3), [`packages/eoip/fileparse/media.py:54`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/fileparse/media.py#L54-L54)
- tests: `tests/acceptance/test_safe_parsing_acceptance.py:350`, `tests/compliance/test_supply_chain_compliance.py:3`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-036 [P0] CRA-036: Correctness, Performance and Scale Qualification

- **Source:** `CRAr_cpccaggcc-requirements.md:1763-1796` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 19, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-036; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-036. Correctness, Performance and Scale Qualification

*Aggregated title: Performance, Scale & 500M Triple Scale Qualification*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | the feature under qualification and CRA-001/032/037 | I (Independent acceptance) | M8 | G18 | ONT-020 | I3 | INV-11, INV-13, INV-14, INV-17, INV-18, INV-19, INV-20, INV-21, INV-22, INV-27, INV-29, INV-30, INV-31, INV-35, INV-36, INV-53, INV-54 | X-05, X-06, X-07, X-32 | H-01 |

**Base statement:** Priority P0. Depends on the feature under qualification and CRA-001/032/037. Sources G18 and all D06/D14/D22 gaps.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-036.1** `[CRAr]` Implement a reproducible workload harness with pinned dataset/generator/license, seed, expected answers, hardware/OS/runtime, engine/config and built-artifact identity.
- **CRA-036.2** `[CRAr]` Qualify P0 then P1 then P2 separately using the research profiles. Count asserted/inferred triples, raw/index/vector/history bytes, replicas and cold/hot residency independently.
- **CRA-036.3** `[CRAr]` Measure p50/p95/p99, successful/failed/cancelled operations, throughput, source/index lag, peak resources, amplification and cost units. Include cold/warm trials, concurrency, skew, ACL selectivity, updates/deletes and failure/restart.
- **CRA-036.4** `[CRAr]` Enforce the selected profile's point-read, bounded graph and approved-query targets without suppressing errors or weakening semantics/security/durability. Do not extrapolate a 1M memory fixture to 500M production capacity.
- **CRA-036.5** `[CRAr]` Run independent oracle/differential semantic checks before timing and retain at least three repeated measured trials with variability. Competitive published claims require equivalent semantics/features/hardware and license/publication review.
- **CRA-036.6** `[CRAr]` Evaluate parser/OCR/linking/RAG/simulation quality with declared labelled corpora and task-specific thresholds. Use section 4's selected defaults for listed tasks; new simulation/domain/language profiles require explicit additional thresholds before qualification, not arbitrary universal accuracy promises.
- **CRA-036.7** `[OCA]` Benchmark suites with committed generator commands, fixed seeds and expected-output hashes under `tests/benchmarks/ontology/` (ONT-020): LUBM (load >= 50k triples/s; Q1-Q14 p95 < 500 ms), BSBM (>= 1,000 QMp
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-036

**Acceptance criteria**
- [ ] Priority P0. Depends on the feature under qualification and CRA-001/032/037. Sources G18 and all D06/D14/D22 gaps.
- [ ] Base statement: Priority P0. Depends on the feature under qualification and CRA-001/032/037. Sources G18 and all D06/D14/D22 gaps
- [ ] CRA-036.1 [CRAr] Implement a reproducible workload harness with pinned dataset/generator/license, seed, expected answers, hardware/OS/runtime, engine/config and built-artifact identity
- [ ] CRA-036.2 [CRAr] Qualify P0 then P1 then P2 separately using the research profiles. Count asserted/inferred triples, raw/index/vector/history bytes, replicas and cold/hot residency independently
- [ ] CRA-036.3 [CRAr] Measure p50/p95/p99, successful/failed/cancelled operations, throughput, source/index lag, peak resources, amplification and cost units. Include cold/warm trials, concurrency, skew, ACL selectivity, updates/deletes and failure/restart
- [ ] CRA-036.4 [CRAr] Enforce the selected profile's point-read, bounded graph and approved-query targets without suppressing errors or weakening semantics/security/durability. Do not extrapolate a 1M memory fixture to 500M production capacity
- [ ] CRA-036.5 [CRAr] Run independent oracle/differential semantic checks before timing and retain at least three repeated measured trials with variability. Competitive published claims require equivalent semantics/features/hardware and license/publication review
- [ ] CRA-036.6 [CRAr] Evaluate parser/OCR/linking/RAG/simulation quality with declared labelled corpora and task-specific thresholds. Use section 4's selected defaults for listed tasks; new simulation/domain/language profiles require explicit additional thresholds before qualification, not arbitrary universal accuracy promises
- [ ] CRA-036.7 [OCA] Benchmark suites with committed generator commands, fixed seeds and expected-output hashes under tests/benchmarks/ontology/ (ONT-020): LUBM (load >= 50k triples/s; Q1-Q14 p95 < 500 ms), BSBM (>= 1,000 QMpH at 100M triples), SP2Bench (no query > 30 s at 50M), SHACL throughput, classification, round-trip fidelity, CML throughput
- [ ] CRA-036.8 [RES] Binding latency gates are the CRAr profile targets (P0/P1/P2). AGG/OCA stricter numbers (point read p95 < 20 ms at P1/P2; P2 bounded 2-hop p95 < 250 ms; ingestion > 50,000 triples/s at P2) are stretch objectives recorded in the manifest; they become binding only by decision H-01 (X-05, X-06)
- [ ] CRA-036.9 [AGG] Sustained 4-hour load test (wrk and/or Locust) per profile with memory-stability checks; CI regression gate fails on > 10% p95 latency regression versus the last accepted run (OCA)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/qualification/harness.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qualification/harness.py#L1-L1), [`scripts/build_master_suite.py:391`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L391-L391), [`scripts/enhance_master_suite.py:244`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L244-L244)
- tests: `tests/acceptance/test_claims_governance_acceptance.py:70`, `tests/acceptance/test_correctness_performance_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-037 [P0] CRA-037: Independent QA and Evidence Verification

- **Source:** `CRAr_cpccaggcc-requirements.md:1797-1837` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 12, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-037; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-037. Independent QA and Evidence Verification

*Aggregated title: Independent Test Oracles & Regression Prevention*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001 and each changed feature | I (Independent acceptance) | M8 | — | ONT-019 | — | INV-07, INV-46, INV-47, INV-48, INV-49 | X-18 | — |

**Base statement:** Priority P0. Depends on CRA-001 and each changed feature. Sources all INV IDs and explicit attachment completion instruction.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-037.1** `[CRAr]` Maintain unit/property/fuzz, differential semantics, contract, real-backend/vendor integration, security/tenancy, real browser, migration/restore, chaos and performance suites with scope labels.
- **CRA-037.2** `[CRAr]` Separate mock tests from actual integration; independently author gold fixtures/oracles so implementation and expected output do not share the same faulty helper. A code change that only alters expected values is not proof of correctness.
- **CRA-037.3** `[CRAr]` Build once and verify the exact promoted artifact in each supported deployment/backend/profile, with actual persistence and negative cases. Development-server checks are not release-artifact acceptance.
- **CRA-037.4** `[CRAr]` Validate source stability, artifact freshness/hashes, exit codes, skip/error counts, fixtures/environment and review records. Missing/invalid/stale/contradictory evidence fails closed.
- **CRA-037.5** `[CRAr]` Perform manual domain, security, accessibility/AT, usability, operations and legal reviews where automated evidence is insufficient. Record reviewer/date/scope, defects and remediation, not a blanket approval checkbox.
- **CRA-037.6** `[CRAr]` On concurrent source changes, preserve edits and report the run as unbound; restart affected services and rerun relevant qualification on a stable revision. Historical passes remain historical.
- **CRA-037.7** `[AGG]` Property-based fuzzing (Hypothesis) of parsers, serializers, chunkers and query planners; mutation testing on semantic core modules.
- **CRA-037.8** `[RES]` Hygiene thresholds from AGG (line coverage >= 85% for `packages/eoip`, mutation score >= 80% on semantic core) are CI hygiene gates only; meeting them never constitutes acceptance evidence (X-18).
- **CRA-037.9** `[AGG]` Zero-skip policy: CI fails when a required test is skipped, xfailed without an open defect 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-037

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001 and each changed feature. Sources all INV IDs and explicit attachment completion instruction.
- [ ] Base statement: Priority P0. Depends on CRA-001 and each changed feature. Sources all INV IDs and explicit attachment completion instruction
- [ ] CRA-037.1 [CRAr] Maintain unit/property/fuzz, differential semantics, contract, real-backend/vendor integration, security/tenancy, real browser, migration/restore, chaos and performance suites with scope labels
- [ ] CRA-037.2 [CRAr] Separate mock tests from actual integration; independently author gold fixtures/oracles so implementation and expected output do not share the same faulty helper. A code change that only alters expected values is not proof of correctness
- [ ] CRA-037.4 [CRAr] Validate source stability, artifact freshness/hashes, exit codes, skip/error counts, fixtures/environment and review records. Missing/invalid/stale/contradictory evidence fails closed
- [ ] CRA-037.5 [CRAr] Perform manual domain, security, accessibility/AT, usability, operations and legal reviews where automated evidence is insufficient. Record reviewer/date/scope, defects and remediation, not a blanket approval checkbox
- [ ] CRA-037.6 [CRAr] On concurrent source changes, preserve edits and report the run as unbound; restart affected services and rerun relevant qualification on a stable revision. Historical passes remain historical
- [ ] CRA-037.7 [AGG] Property-based fuzzing (Hypothesis) of parsers, serializers, chunkers and query planners; mutation testing on semantic core modules
- [ ] CRA-037.9 [AGG] Zero-skip policy: CI fails when a required test is skipped, xfailed without an open defect ID, errors or times out
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/qa/verification_gate.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/qa/verification_gate.py#L1-L1)
- tests: `tests/acceptance/test_independent_qa_acceptance.py:1`, `tests/oracles/graph_oracle.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-038 [P0] CRA-038: Support, Service Objectives and Operator Readiness

- **Source:** `CRAr_cpccaggcc-requirements.md:1838-1867` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-038; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-038. Support, Service Objectives and Operator Readiness

*Aggregated title: Support Runbooks, SLA Enforcement & Disaster Drills*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-032/033/035/037 | I (Independent acceptance) | M8 | — | — | I11 | — | X-08 | H-08 |

**Base statement:** Priority P1. Depends on CRA-032/033/035/037. Sources D21 gaps and research playbooks.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-038.1** `[CRAr]` Define supported versions/deployments, lifecycle/deprecation, service ownership, incident severity, escalation and customer versus vendor responsibility.
- **CRA-038.2** `[CRAr]` Implement documented incident, scaling, upgrade, backup/restore, credential compromise, poisoned data/model and projection-lag playbooks with diagnostic prerequisites and stop/rollback conditions.
- **CRA-038.3** `[CRAr]` Treat 99.9% monthly availability and initial response objectives as engineering proposals until staffing, measurement, exclusions and signed contracts support them. Response is not resolution, and installed customer infrastructure is a separate responsibility boundary.
- **CRA-038.4** `[CRAr]` Produce redacted support bundles with authorization, consent, retention and no secrets/customer raw data by default. Provide offline documentation for disconnected customers.
- **CRA-038.5** `[CRAr]` Rehearse operational incidents and restore with someone other than the implementer where feasible, recording actual observations and unresolved failures. Agent role-playing is not operator sign-off.
- **CRA-038.6** `[AGG]` Runbooks: ingestion backlog/consumer lag, store memory exhaustion and query kill, compromised source credentials, inconsistent ontology rollback, stuck publication, split-brain recovery, policy-lag index.
- **CRA-038.7** `[AGG]` Design `eoip-admin support-bundle` producing an encrypted, redacted diagnostic bundle (logs, metrics, configuration) with consent and retention metadata.
- **CRA-038.8** `[RES]` Severity response objectives remain proposals until signed: CRAr (P1 1 h, P2 4 business hours, P3 2 business days) and AGG (P1 < 15 min 24x7, P2 < 1 business hour, P3 < 4 business hours, P4 < 1 business day) are presented side by side for decision H-08 (X-08).

**Acceptance obligation CRA-038.A** (only after every clause above is ACCEPTED):

- `[CRAr]` real drill of a source credential compromise, stuc
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-038

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-032/033/035/037. Sources D21 gaps and research playbooks.
- [ ] Base statement: Priority P1. Depends on CRA-032/033/035/037. Sources D21 gaps and research playbooks
- [ ] CRA-038.1 [CRAr] Define supported versions/deployments, lifecycle/deprecation, service ownership, incident severity, escalation and customer versus vendor responsibility
- [ ] CRA-038.2 [CRAr] Implement documented incident, scaling, upgrade, backup/restore, credential compromise, poisoned data/model and projection-lag playbooks with diagnostic prerequisites and stop/rollback conditions
- [ ] CRA-038.3 [CRAr] Treat 99.9% monthly availability and initial response objectives as engineering proposals until staffing, measurement, exclusions and signed contracts support them. Response is not resolution, and installed customer infrastructure is a separate responsibility boundary
- [ ] CRA-038.4 [CRAr] Produce redacted support bundles with authorization, consent, retention and no secrets/customer raw data by default. Provide offline documentation for disconnected customers
- [ ] CRA-038.5 [CRAr] Rehearse operational incidents and restore with someone other than the implementer where feasible, recording actual observations and unresolved failures. Agent role-playing is not operator sign-off
- [ ] CRA-038.6 [AGG] Runbooks: ingestion backlog/consumer lag, store memory exhaustion and query kill, compromised source credentials, inconsistent ontology rollback, stuck publication, split-brain recovery, policy-lag index
- [ ] CRA-038.7 [AGG] Design eoip-admin support-bundle producing an encrypted, redacted diagnostic bundle (logs, metrics, configuration) with consent and retention metadata
- [ ] CRA-038.8 [RES] Severity response objectives remain proposals until signed: CRAr (P1 1 h, P2 4 business hours, P3 2 business days) and AGG (P1 < 15 min 24x7, P2 < 1 business hour, P3 < 4 business hours, P4 < 1 business day) are presented side by side for decision H-08 (X-08)
- [ ] obligation CRA-038.A (only after every clause above is ACCEPTED)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ops/readiness.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ops/readiness.py#L1-L1)
- tests: `tests/acceptance/test_operator_readiness_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-039 [P0] CRA-039: Public APIs, SDKs and Developer Ecosystem

- **Source:** `CRAr_cpccaggcc-requirements.md:1868-1898` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-039; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-039. Public APIs, SDKs and Developer Ecosystem

*Aggregated title: Developer Platform: Python & TypeScript SDKs, OpenAPI & MCP Server*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001/002/003/035/037 | H (Deploy and migrate) | M8 | — | ONT-011, ONT-014 | I14 | INV-02, INV-05, INV-08, INV-10, INV-33, INV-39, INV-41, INV-44, INV-50 | — | — |

**Base statement:** Priority P1. Depends on CRA-001/002/003/035/037. Sources INV-08/10/33/39/41/44/50/55.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-039.1** `[CRAr]` Generate published OpenAPI/JSON schemas and Python/TypeScript SDKs from the composed real application contract. Version public APIs, errors, events and compatibility/deprecation independently from internal endpoints.
- **CRA-039.2** `[CRAr]` Expose authorized MCP tools with typed inputs/outputs, provenance and budgets. Tools cannot change trusted identity or obtain broader rights through natural-language arguments.
- **CRA-039.3** `[CRAr]` Provide plugin/connector templates, synthetic fixtures, conformance runner, supported-version tables and a documented qualification process. Uncertified community modules remain visibly unqualified.
- **CRA-039.4** `[CRAr]` Generate ontology/API/help documentation from exact signed release artifacts, sanitize authored content and support offline/no-egress generation. Follow LODE/WIDOCO version/license transitions explicitly if adopted.
- **CRA-039.5** `[CRAr]` Define contribution, vulnerability disclosure, ownership and marketplace policies consistent with proprietary core licensing and upstream obligations. Do not publish customer models/content as examples.
- **CRA-039.6** `[AGG]` Generated SDKs: TypeScript (proposed package `@eoip/sdk-typescript`) and Python (proposed `eoip-python`); names verified for availability and trademark before publication.
- **CRA-039.7** `[OCA]` MCP server (ONT-011) over existing `tools_contract/` and `sdk/` exposing ontology, graph and governed actions; actions invoked through MCP pass exactly the same autonomy, approval and policy gates as direct invocation.
- **CRA-039.8** `[OCA]` Offline Widoco-class HTML ontology documentation generator (ONT-014) producing cross-referenced specs with diagrams and provenance from signed releases; `GET /ontology/docs` serves them.

**Acceptance obligation CRA-039.A** (only after every clause above is ACCEPTED):

- 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-039

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-001/002/003/035/037. Sources INV-08/10/33/39/41/44/50/55.
- [ ] CRA-039.1 [CRAr] Generate published OpenAPI/JSON schemas and Python/TypeScript SDKs from the composed real application contract. Version public APIs, errors, events and compatibility/deprecation independently from internal endpoints
- [ ] CRA-039.2 [CRAr] Expose authorized MCP tools with typed inputs/outputs, provenance and budgets. Tools cannot change trusted identity or obtain broader rights through natural-language arguments
- [ ] CRA-039.3 [CRAr] Provide plugin/connector templates, synthetic fixtures, conformance runner, supported-version tables and a documented qualification process. Uncertified community modules remain visibly unqualified
- [ ] CRA-039.4 [CRAr] Generate ontology/API/help documentation from exact signed release artifacts, sanitize authored content and support offline/no-egress generation. Follow LODE/WIDOCO version/license transitions explicitly if adopted
- [ ] CRA-039.5 [CRAr] Define contribution, vulnerability disclosure, ownership and marketplace policies consistent with proprietary core licensing and upstream obligations. Do not publish customer models/content as examples
- [ ] CRA-039.6 [AGG] Generated SDKs: TypeScript (proposed package @eoip/sdk-typescript) and Python (proposed eoip-python); names verified for availability and trademark before publication
- [ ] CRA-039.7 [OCA] MCP server (ONT-011) over existing toolscontract/ and sdk/ exposing ontology, graph and governed actions; actions invoked through MCP pass exactly the same autonomy, approval and policy gates as direct invocation
- [ ] CRA-039.8 [OCA] Offline Widoco-class HTML ontology documentation generator (ONT-014) producing cross-referenced specs with diagrams and provenance from signed releases; GET /ontology/docs serves them
- [ ] obligation CRA-039.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] independently build a client and sample plugin from released schemas/templates, run a real scoped task and reject deprecated/incompatible/unauthorized calls. Compare generated docs/SDKs with actual runtime and artifact digest; a static schema file alone is insufficient
- [ ] [MERGED] An external agent (Claude or LangGraph client) answers a business question through the MCP server and an attempted destructive action is held for approval (AGG + OCA)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/doc_generator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/doc_generator.py#L1-L1), [`packages/eoip/plugins/conformance.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/plugins/conformance.py#L1-L1), [`packages/eoip/policies/ecosystem_policies.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/policies/ecosystem_policies.py#L1-L1), [`packages/eoip/sdk/openapi_generator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/sdk/openapi_generator.py#L1-L1), [`packages/eoip/sdk/package_verifier.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/sdk/package_verifier.py#L1-L1), [`packages/eoip/sdk/python_client.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/sdk/python_client.py#L1-L1), [`packages/eoip/sdk/typescript_client.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/sdk/typescript_client.py#L1-L1), [`packages/eoip/tools_contract/mcp_server.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tools_contract/mcp_server.py#L1-L1)
- tests: `tests/acceptance/test_developer_ecosystem_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-040 [P0] CRA-040: Privacy, Retention, Deletion and No-Egress Guarantees

- **Source:** `CRAr_cpccaggcc-requirements.md:1899-1928` (heading) · **Type:** Security · **Severity:** Critical
- **Now:** Partially Implemented / L2 (tests passed 6, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-040; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence; Critical: L5 independent dual-control review missing
- **Depends on:** FT-F04, FT-F09 · **Effort:** 2.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-040. Privacy, Retention, Deletion and No-Egress Guarantees

*Aggregated title: Data Privacy, Right-to-be-Forgotten & Strict No-Egress Firewalls*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-003/010/018/031 | B (Safe platform) | M8 | — | — | — | INV-11, INV-24, INV-25, INV-37, INV-42, INV-43, INV-49, INV-51, INV-52 | — | — |

**Base statement:** Priority P0. Depends on CRA-003/010/018/031. Sources INV-13/24/25/37/42/43/49/51/52/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-040.1** `[CRAr]` Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/model/dataset/content licenses are distinct.
- **CRA-040.2** `[CRAr]` Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at the network boundary, not inferred from configuration.
- **CRA-040.3** `[CRAr]` Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. A deletion workflow must locate and process each according to retention/hold policy.
- **CRA-040.4** `[CRAr]` Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/access treatment; it is not an excuse to ignore erasure obligations.
- **CRA-040.5** `[CRAr]` Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal hold. Do not claim regulatory certification from a policy module name.
- **CRA-040.6** `[AGG]` Erasure cascade: a deletion request for a subject locates and processes every derivative across the eight graph planes (raw, canonical, schema references, provenance, lineage, policy, temporal, vector), caches, exports and backups under retention/hold policy, producing a scoped report.
- **CRA-040.7** `[AGG]` No-egress verification: a network socket monitor records zero external bytes during a full ingestion plus GraphRAG cycle in no-egress mode; allowed destinations are limited to configured enterprise systems.

**Acceptance obligation CRA-040.A** (only after every clause above is ACCEPTED):

- `[CRAr]` delete and revoke a subject/source while jobs and 
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-040

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-003/010/018/031. Sources INV-13/24/25/37/42/43/49/51/52/54.
- [ ] CRA-040.1 [CRAr] Classify source data and derivatives, record lawful/contractual handling policy, residence, retention, consent where applicable and legal holds. Code/model/dataset/content licenses are distinct
- [ ] CRA-040.2 [CRAr] Enforce egress policy for connectors, parsers/imports, model calls, linting, telemetry, docs and support bundles. No-egress mode must be measured at the network boundary, not inferred from configuration
- [ ] CRA-040.3 [CRAr] Track all copies/derivatives including graph assertions/inferences, raw objects, indexes/vectors, caches, answers, exports, jobs, traces and backups. A deletion workflow must locate and process each according to retention/hold policy
- [ ] CRA-040.4 [CRAr] Prevent replay, restore, re-embedding or resynchronization from resurrecting deleted/revoked content. Immutable history requires documented retention/access treatment; it is not an excuse to ignore erasure obligations
- [ ] CRA-040.5 [CRAr] Support data-subject/administrative access and deletion workflows with authorization, audit, scoped reports and explicit conflict/escalation for legal hold. Do not claim regulatory certification from a policy module name
- [ ] CRA-040.6 [AGG] Erasure cascade: a deletion request for a subject locates and processes every derivative across the eight graph planes (raw, canonical, schema references, provenance, lineage, policy, temporal, vector), caches, exports and backups under retention/hold policy, producing a scoped report
- [ ] obligation CRA-040.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] delete and revoke a subject/source while jobs and streams are active, restore/replay older state, then inspect every derivative and network log. Demonstrate retained held material is restricted and reported accurately, with reviewed retention/backup exceptions
- [ ] [MERGED] After a GDPR purge, a deep sweep across graph, vector, cache and object store finds zero remaining records except documented held material (AGG)
- [ ] Not evidence of completion
- [ ] Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/privacy/governance.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/privacy/governance.py#L1-L1), [`scripts/build_master_suite.py:390`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L390-L390), [`scripts/enhance_master_suite.py:243`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L243-L243)
- tests: `tests/integration/test_privacy_governance_and_no_egress.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']; missing ['L3 (same commit) or L4', 'L5 (reviewer ≠ producer)']

## RT-CRA-043 [P0] CRA-043: Numerical Compute Stack, Determinism and Hardware Profiles

- **Source:** `CRAr_cpccaggcc-requirements.md:1991-2035` (heading) · **Type:** Non-Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 27, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-043; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-043. Numerical Compute Stack, Determinism and Hardware Profiles

*Aggregated title: (new in v3.1) Tiered Numerical Substrate for Probabilistic AI*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P0 | CRA-001/002/035 | B (Safe platform) | M10 | G20 | — | — | — | X-39, X-42 | H-15, H-16, H-17 |

**Base statement:** Priority P0. Depends on CRA-001/002/035. Sources GN-010..GN-016 and G20. CRA-014 (OCR/ASR), CRA-023.6/023.7 (embedding and structural similarity, DeepOnto), CRA-025 (dense retrieval), CRA-026 (local models) and CRA-044 all presuppose a numerical stack the repository does not have.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-043.1** `[GN]` Introduce the numerical stack as four separately installable optional extras, never as core dependencies: N0 `numerics` (numpy, scipy, scikit-learn; installed-size budget <= 150 MB), N1 `neural` (N0 plus CPU-only torch and torch-geometric; installed-size budget <= 2.5 GB), N2 `neural-text` (N1 plus transformers and sentence-transformers), N3 `neural-research` (N1 plus snntorch; research environments only, never in customer profiles, bundles or images — H-15). Tiers compose through self-referencing extras with exactly one version constraint per package. `pip install -e .` must resolve to an unchanged package set, proven by diffing `pip freeze`.
- **CRA-043.2** `[GN]` CPU-only builds are the only builds EOIP distributes (decision H-16, accepted 2026-10-18: CUDA packages cannot be redistributed; `docs/decisions/ADR-H16-no-cuda-redistribution.md`). No `nvidia-*` package, CUDA runtime or CUDA-enabled torch build appears in any EOIP wheel, distribution lock file, offline bundle, container image or mirror, and EOIP documentation publishes no CUDA install command. A CUDA build the customer installs from upstream under their own NVIDIA terms is detected as `TORCH_CUDA`, reported as unqualified and never required.
- **CRA-043.3** `[GN]` Provide a hash-pinned lock file (`requirements-neural.lock` via `pip-compile --generate-hashes` or the project's equivalent) and an offline wheel bundle per supported platform and tier. Installation from the bundle succeeds on a network-isolated host, and no model weights are fetched at first run (CRA-014.3, CRA-040.2). The lock file, every bundle manifest and every image SBOM are scanned and must list zero `nvidia-*` packages (H-16).
- **CRA-043.4** `[GN]` Regi
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-043

**Acceptance criteria**
- [ ] Priority P0. Depends on CRA-001/002/035. Sources GN-010..GN-016 and G20. CRA-014 (OCR/ASR), CRA-023.6/023.7 (embedding and structural similarity, DeepOnto), CRA-025 (dense retrieval), CRA-026 (local models) and CRA-044 all presuppose a numerical stack the repository does not have.
- [ ] CRA-043.1 [GN] Introduce the numerical stack as four separately installable optional extras, never as core dependencies: N0 numerics (numpy, scipy, scikit-learn; installed-size budget <= 150 MB), N1 neural (N0 plus CPU-only torch and torch-geometric; installed-size budget <= 2.5 GB), N2 neural-text (N1 plus transformers and sentence-transformers), N3 neural-research (N1 plus snntorch; research env
- [ ] CRA-043.2 [GN] CPU-only builds are the only builds EOIP distributes (decision H-16, accepted 2026-10-18: CUDA packages cannot be redistributed; docs/decisions/ADR-H16-no-cuda-redistribution.md). No nvidia- package, CUDA runtime or CUDA-enabled torch build appears in any EOIP wheel, distribution lock file, offline bundle, container image or mirror, and EOIP documentation publishes no CUDA install c
- [ ] CRA-043.3 [GN] Provide a hash-pinned lock file (requirements-neural.lock via pip-compile --generate-hashes or the project's equivalent) and an offline wheel bundle per supported platform and tier. Installation from the bundle succeeds on a network-isolated host, and no model weights are fetched at first run (CRA-014.3, CRA-040.2). The lock file, every bundle manifest and every image SBOM are scann
- [ ] CRA-043.4 [GN] Register each tier as capabilities (CRA-001). A missing tier is capability state UNAVAILABLE, returned as HTTP 503 CAPABILITYUNAVAILABLE with the missing tier and its install command in details (X-39). Endpoints declare their minimum tier, so N0-only deployments keep metrics, baselines and embedding lookup working. Silent fallback to a non-learned heuristic or to hashing is prohibit
- [ ] CRA-043.5 [GN] Array discipline: float32 for stored and served vectors; float64 only for metric accumulation; no Python-level element loops in hot paths (similarity, normalization, aggregation, batching); list[float] only at serialization boundaries; every array crossing a module boundary is checked finite
- [ ] CRA-043.6 [GN] Determinism: a single seeding entry point seeds Python, numpy, torch and CUDA, enables deterministic algorithms where available, records any operation that fell back to a non-deterministic kernel, and stores the seed bundle and an environment capture (library versions, BLAS vendor, device, thread counts) in every training and evaluation receipt
- [ ] CRA-043.7 [GN] BLAS thread governance: OMPNUMTHREADS, OPENBLASNUMTHREADS, MKLNUMTHREADS and NUMEXPRNUMTHREADS are set together before numpy is first imported. Serving processes default to 1 thread per worker; training and batch workers to min(8, CPU count). The effective count is reported by the capability route
- [ ] CRA-043.8 [GN] Numerical stability: max-subtracted softmax, epsilon-guarded logarithms and normalizations, int64 node indices, and a documented result for empty inputs; no reduction returns NaN
- [ ] CRA-043.9 [GN] Memory and accelerator lifecycle: estimate peak memory before training or full-graph inference and refuse, naming a workable batch size, when the estimate exceeds 80% of available memory; release accelerator memory after each job; derive batch sizes from measured capacity, never hardcode them; record peak RSS and accelerator memory in performance receipts. All numerical and model wo
- [ ] CRA-043.10 [RES] Qualify the platform matrix by CI jobs, not assertion: Linux x8664 (N0-N2 required), Windows x8664 and macOS arm64 (N0-N1 required), Linux arm64 (N0 required). No platform requires a GPU; a customer-provisioned GPU job, if run, is labelled unqualified and non-binding (H-17)
- [ ] CRA-043.11 [RES] CPU-first qualification (decision H-15 accepted; H-17 open): every binding gate in sections 5.2 and 5.3 and in CRA-026, CRA-043 and CRA-044 is qualified on CPU-only reference hardware with no GPU visible to the process, and receipts record device=cpu. Results obtained with a GPU are recorded separately and are non-binding until H-17 is decided; a capability that meets its gates on
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/neural/numerics.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/numerics.py#L1-L1), [`packages/eoip/neural/runtime.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/runtime.py#L1-L1)
- tests: `tests/compliance/test_no_cuda_packages.py:1`, `tests/neural/test_antistub.py:127`, `tests/neural/test_determinism.py:1`, `tests/neural/test_numerical_stack_acceptance.py:1`, `tests/neural/test_numerics.py:1`, `tests/neural/test_runtime_tiers.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-044 [P0] CRA-044: Learned Graph Intelligence over the Graph Planes

- **Source:** `CRAr_cpccaggcc-requirements.md:2036-2081` (heading) · **Type:** Security · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 22, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-044; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-044. Learned Graph Intelligence over the Graph Planes

*Aggregated title: (new in v3.1) Neural Fabric — GNN, Transformer, Temporal, Convolutional, Generative and Spiking Models on Graphs*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/019/020/023/025/043/045 | F (Usable value) | M10 | G12, G19 | — | — | INV-19, INV-53 | X-34, X-35, X-36, X-37, X-38, X-40, X-41 | H-17 |

**Base statement:** Priority P1. Depends on CRA-003/019/020/023/025/043/045. Sources GN-001..GN-007, GN-101..GN-706, the two neural-architecture research inputs summarised in Graph-Neurons, and G19. Where GN-REQ-v1 and this document differ, this document governs (X-34..X-41).

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-044.1** `[GN]` Remove the hash-based graph embedding stand-ins from production paths. `GraphEmbedder._deterministic_vector`, `embed_node2vec` and `embed_transe` in `packages/eoip/gnn/engine.py` compute SHA-256 digests of identifiers and walk strings with no objective, optimiser or learning. Retain them only as the `HashBaseline` test fixture, and keep `get_gnn_engine()` importable as a thin re-export of the new implementation so existing callers do not break (X-40).
- **CRA-044.2** `[GN]` Map the four graph levels of the research inputs onto the graph planes of section 8.2 — GL0 instance graph to planes 1-2; GL1 meta-graph to plane 3; GL2 living brain (the cross-source unified graph) to plane 2 across sources; GL3 enterprise ontology to plane 3 axioms and shapes; the temporal axis GLT to plane 7 — and train only on authorized, policy-epoch-bound snapshots of those planes. A parallel temporal store duplicating plane 2 is not permitted.
- **CRA-044.3** `[GN]` Every learned model passes four anti-stub probes before any quality claim: loss descent (final loss <= 70% of initial); parameter change (>= 90% of tensors move); label-permutation control (the true-label primary metric beats the permuted-label metric by >= 0.10 absolute); structural coherence (two automorphic nodes have embedding cosine >= 0.90). The probe harness must itself score the existing hash stub as failing all four.
- **CRA-044.4** `[GN]` Snapshot and split discipline: content-addressed snapshots; strictly event-time temporal splits validated on every batch, so a deliberately leaked edge raises; type-constrained negative sampling against `ontology/manifest.py:edge_endpoi
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-044

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/019/020/023/025/043/045. Sources GN-001..GN-007, GN-101..GN-706, the two neural-architecture research inputs summarised in Graph-Neurons, and G19. Where GN-REQ-v1 and this document differ, this document governs (X-34..X-41).
- [ ] CRA-044.1 [GN] Remove the hash-based graph embedding stand-ins from production paths. GraphEmbedder.deterministicvector, embednode2vec and embedtranse in packages/eoip/gnn/engine.py compute SHA-256 digests of identifiers and walk strings with no objective, optimiser or learning. Retain them only as the HashBaseline test fixture, and keep getgnnengine() importable as a thin re-export of the new imp
- [ ] CRA-044.2 [GN] Map the four graph levels of the research inputs onto the graph planes of section 8.2 — GL0 instance graph to planes 1-2; GL1 meta-graph to plane 3; GL2 living brain (the cross-source unified graph) to plane 2 across sources; GL3 enterprise ontology to plane 3 axioms and shapes; the temporal axis GLT to plane 7 — and train only on authorized, policy-epoch-bound snapshots of those pl
- [ ] CRA-044.3 [GN] Every learned model passes four anti-stub probes before any quality claim: loss descent (final loss <= 70% of initial); parameter change (>= 90% of tensors move); label-permutation control (the true-label primary metric beats the permuted-label metric by >= 0.10 absolute); structural coherence (two automorphic nodes have embedding cosine >= 0.90). The probe harness must itself score
- [ ] CRA-044.4 [GN] Snapshot and split discipline: content-addressed snapshots; strictly event-time temporal splits validated on every batch, so a deliberately leaked edge raises; type-constrained negative sampling against ontology/manifest.py:edgeendpointsvalid as the default for every reported metric
- [ ] CRA-044.5 [GN] Evaluation discipline: AUPRC is primary for link prediction and anomaly detection and AUROC is never reported alone; Macro-F1 for node classification; time-filtered MRR for temporal prediction. Five baselines are reported beside every model on the same split: random, degree, common-neighbours/Adamic-Adar, HashBaseline, and the existing deterministic rule or traversal. A score become
- [ ] CRA-044.6 [GN] Core encoders: R-GCN with basis decomposition (defaults 2 layers, 128 hidden units, 30 bases) and inductive GraphSAGE for continuously ingested entities, the latter proven by embedding new nodes with an unchanged weight hash. A model that does not beat both the common-neighbours and rule baselines by >= 0.05 on the primary metric is recorded FAILED with its numbers, not shipped
- [ ] CRA-044.7 [GN] Bake-off-gated architectures, each promoted only on a measured margin over the R-GCN default on the same split and otherwise recorded FAILED: relational graph attention (attention weights retrievable per prediction); heterogeneous graph transformer (>= 0.03 on a fixture spanning >= 3 domains); GraphGPS-style local-plus-global transformer (>= 0.03 on tasks with shortest-path distance
- [ ] CRA-044.8 [GN] Generative and spiking work: an adversarial plausibility discriminator may act as a write-path quality filter (precision >= 0.80 at recall >= 0.70; <= 5 ms per triple; flagged triples quarantined for review, never deleted; the ontology domain/range veto overrides the learned score) only after CRA-044.6 is ACCEPTED. Triple generators and spiking-network encoders are research-only, ru
- [ ] CRA-044.9 [GN] Model lineage and lifecycle: models, embeddings and calibrators are registered with snapshot ID, code commit, seed bundle, environment, training-data scope and gate report, extending packages/eoip/mlops/experimenttracker.py. Promotion requires every gate in clauses 3-6 plus the security and explainability gates; rollback restores the prior version and serving reflects it within 60 s
- [ ] CRA-044.10 [GN] Explainability: >= 95% of served predictions carry evidence paths, and a faithfulness probe shows that removing the identified evidence subgraph lowers the prediction score by >= 50%; otherwise the explanation is reported as not faithful
- [ ] CRA-044.11 [GN] Incremental operation and failure-mode guards: graph changes invalidate only the affected k-hop embeddings; retraining is triggered by measured drift, scheduled evaluation or quality degradation, not by every write. Oversmoothing (default depth 2; embedding variance measured at 2, 4 and 8 layers), oversquashing (long-range accuracy reported separately) and popularity shortcuts (deg
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/neural/antistub.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/antistub.py#L1-L1), [`packages/eoip/neural/datasets.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/datasets.py#L1-L1), [`packages/eoip/neural/discriminator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/discriminator.py#L1-L1), [`packages/eoip/neural/encoders.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/encoders.py#L1-L1), [`packages/eoip/neural/evaluation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/evaluation.py#L1-L1), [`packages/eoip/neural/explain.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/explain.py#L1-L1), [`packages/eoip/neural/lifecycle.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/lifecycle.py#L1-L1), [`packages/eoip/neural/planes.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/neural/planes.py#L1-L1)
- tests: `tests/acceptance/test_independent_qa_acceptance.py:271`, `tests/acceptance/test_verify_ledger.py:242`, `tests/neural/test_antistub.py:1`, `tests/neural/test_learned_graph_intelligence.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-ONT-012 [P0] ONT-012: Position & document Ontology-as-Code · P0 · XS

- **Source:** `CRAr_cpccaggcc-requirements.md:2631-2631` (table_row) · **Type:** Functional · **Severity:** High
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ONT-012; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-012 | Position & document Ontology-as-Code | P0 | XS | Tier 1 — Differentiators | none | CRA-041 | CRA-041.4
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ONT-012

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-012 | Position & document Ontology-as-Code | P0 | XS | Tier 1 — Differentiators | none | CRA-041 | CRA-041.4»
- [ ] Position & document Ontology-as-Code
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/positioning_pack.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/positioning_pack.py#L1-L1)
- tests: `tests/acceptance/test_claims_governance_acceptance.py:187`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-015 [P1] CRA-015: Engineering Diagram Semantics

- **Source:** `CRAr_cpccaggcc-requirements.md:1002-1031` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-015; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-015. Engineering Diagram Semantics

*Aggregated title: Engineering Diagram & Architecture Visual Parser*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-012/014/016/017 | G (Named sources, media and actions) | M3 | G10 | — | — | INV-07 | — | — |

**Base statement:** Priority P1. Depends on CRA-012/014/016/017. Sources G10 and INV-07/32.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-015.1** `[CRAr]` Support notation-specific structured diagrams, initially diagrams.net/Chowlk-compatible conceptual diagrams plus declared Mermaid/PlantUML subsets; retain the exact source and parser coverage.
- **CRA-015.2** `[CRAr]` Parse components, ports, containment, directions, cardinalities, sequence/event meaning and labels only where supported. Never silently coerce every box to Service or unknown relation to CALLS.
- **CRA-015.3** `[CRAr]` Visual extraction from images/video creates candidates with bounding regions, uncertainty and reviewer controls. Distinguish inferred visual interpretation from formal notation semantics.
- **CRA-015.4** `[CRAr]` Show a source-versus-graph diff and loss ledger. Unsupported constructs block claims of lossless conversion; the reviewer may explicitly accept a limited projection without altering the source.
- **CRA-015.5** `[CRAr]` Round-trip supported models to editable diagrams or maintain a documented non-round-trippable status. Escape/sanitize all generated markup and labels.
- **CRA-015.6** `[AGG]` Structured formats: draw.io/diagrams.net XML (including Chowlk notation), declared PlantUML and Mermaid subsets; Visio VSDX as an extended P2 format. Parse into a diagram AST of shapes, labels, ports, containers and connectors with direction.
- **CRA-015.7** `[AGG]` A configurable, versioned shape/connector mapping table proposes ontology terms (for example cylinder -> `ex:Database`, rectangle -> `ex:Service`, arrow label 'calls' -> `ex:calls`); mappings are proposals reviewed before publication.
- **CRA-015.8** `[AGG]` Unrecognized connectors are preserved as generic directed edges (`eoip:connectsTo`) with all visual attributes and an entry in the loss ledger; never coerced to `CALLS` or `Service` (G10). A vision-LLM fallback for raster diagrams produces only reviewed candidates with bounding regions.

**Acceptance obligation CRA-015.A** (only after every clause above is ACCEPTED):

- `[CRAr]` independ
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-015

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-012/014/016/017. Sources G10 and INV-07/32.
- [ ] CRA-015.1 [CRAr] Support notation-specific structured diagrams, initially diagrams.net/Chowlk-compatible conceptual diagrams plus declared Mermaid/PlantUML subsets; retain the exact source and parser coverage
- [ ] CRA-015.2 [CRAr] Parse components, ports, containment, directions, cardinalities, sequence/event meaning and labels only where supported. Never silently coerce every box to Service or unknown relation to CALLS
- [ ] CRA-015.3 [CRAr] Visual extraction from images/video creates candidates with bounding regions, uncertainty and reviewer controls. Distinguish inferred visual interpretation from formal notation semantics
- [ ] CRA-015.4 [CRAr] Show a source-versus-graph diff and loss ledger. Unsupported constructs block claims of lossless conversion; the reviewer may explicitly accept a limited projection without altering the source
- [ ] CRA-015.5 [CRAr] Round-trip supported models to editable diagrams or maintain a documented non-round-trippable status. Escape/sanitize all generated markup and labels
- [ ] CRA-015.6 [AGG] Structured formats: draw.io/diagrams.net XML (including Chowlk notation), declared PlantUML and Mermaid subsets; Visio VSDX as an extended P2 format. Parse into a diagram AST of shapes, labels, ports, containers and connectors with direction
- [ ] CRA-015.7 [AGG] A configurable, versioned shape/connector mapping table proposes ontology terms (for example cylinder -> ex:Database, rectangle -> ex:Service, arrow label 'calls' -> ex:calls); mappings are proposals reviewed before publication
- [ ] CRA-015.8 [AGG] Unrecognized connectors are preserved as generic directed edges (eoip:connectsTo) with all visual attributes and an entry in the loss ledger; never coerced to CALLS or Service (G10). A vision-LLM fallback for raster diagrams produces only reviewed candidates with bounding regions
- [ ] obligation CRA-015.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] independently specified gold diagrams with parallel/directed edges, labels/metacharacters, nesting and intentionally unsupported constructs. Compare formal axioms and business meaning, not just vertex counts or rendered screenshots. Verify correction/rejection propagates to graph/provenance/indexes
- [ ] [MERGED] Parse a microservice architecture diagram; reviewed output compiles into valid OWL 2/RDF assertions whose formal comparison with an independently authored gold model shows 100% fidelity for the supported subset and an explicit loss ledger for the rest (AGG + CRAr)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/fileparse/diagram_parser.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/fileparse/diagram_parser.py#L1-L1)
- tests: `tests/acceptance/test_engineering_diagram_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-021 [P1] CRA-021: Vocabulary, Taxonomy and Multilingual Stewardship

- **Source:** `CRAr_cpccaggcc-requirements.md:1223-1252` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-021; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-021. Vocabulary, Taxonomy and Multilingual Stewardship

*Aggregated title: Multilingual Taxonomy & Controlled Vocabulary Stewardship (SKOS / SKOS-XL)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-018/020/022 | E (Governed knowledge) | M5 | F1 | ONT-016 | I17 | INV-04, INV-06, INV-09, INV-10, INV-11, INV-12, INV-13, INV-14, INV-15, INV-51, INV-54 | — | — |

**Base statement:** Priority P1. Depends on CRA-018/020/022. Sources INV-06/09/10/11/12/13/14/15/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-021.1** `[CRAr]` Support SKOS concepts/schemes, broader/narrower/related, polyhierarchy, preferred/alternative/hidden labels with language tags, mappings, deprecation/replacement and explicit concept-versus-label identity.
- **CRA-021.2** `[CRAr]` Provide SKOS-XL and OntoLex-Lemon through qualified optional profiles where required; reject unsupported export/import rather than flattening silently.
- **CRA-021.3** `[CRAr]` Support candidate terms, definitions, synonyms, crosswalk proposals, provenance, domain ownership and review. Model suggestions must not auto-create equivalence or upstream namespace terms.
- **CRA-021.4** `[CRAr]` Version vocabularies with classifier/embedding/index dependencies and publication receipts. Record consumer acknowledgement and stale projection state after change.
- **CRA-021.5** `[CRAr]` Provide language-aware search/editing and Unicode/RTL-safe presentation, label uniqueness policies and stable IDs independent of translated labels.
- **CRA-021.6** `[OCA]` Wire the existing SKOS object model (`skos.py`, 450 LOC: Concept, ConceptScheme, Collection, mappings, integrity issues, label conflicts) to the CRA-016 serializer (ONT-016): a 10k-concept SKOS thesaurus imports and re-exports losslessly and SKOS-XL labels are preserved.
- **CRA-021.7** `[AGG]` Labels per BCP-47 language tag; deprecation via `owl:deprecated true` plus `dct:isReplacedBy`; audited editorial notes; ISO 25964-style thesaurus import fixture.
- **CRA-021.8** `[OCA]` Existing drift detection (`drift.py`, `embedding_drift.py`) emits evolution proposals into CRA-022 review; proposals are never auto-applied (I17).

**Acceptance obligation CRA-021.A** (only after every clause above is ACCEPTED):

- `[CRAr]` multilingual import/edit/export, same-label distinct concepts, cyclic taxonomy policy, polyhierarchy, retired terms and concurre
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-021

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-018/020/022. Sources INV-06/09/10/11/12/13/14/15/54.
- [ ] CRA-021.1 [CRAr] Support SKOS concepts/schemes, broader/narrower/related, polyhierarchy, preferred/alternative/hidden labels with language tags, mappings, deprecation/replacement and explicit concept-versus-label identity
- [ ] CRA-021.2 [CRAr] Provide SKOS-XL and OntoLex-Lemon through qualified optional profiles where required; reject unsupported export/import rather than flattening silently
- [ ] CRA-021.3 [CRAr] Support candidate terms, definitions, synonyms, crosswalk proposals, provenance, domain ownership and review. Model suggestions must not auto-create equivalence or upstream namespace terms
- [ ] CRA-021.4 [CRAr] Version vocabularies with classifier/embedding/index dependencies and publication receipts. Record consumer acknowledgement and stale projection state after change
- [ ] CRA-021.5 [CRAr] Provide language-aware search/editing and Unicode/RTL-safe presentation, label uniqueness policies and stable IDs independent of translated labels
- [ ] CRA-021.6 [OCA] Wire the existing SKOS object model (skos.py, 450 LOC: Concept, ConceptScheme, Collection, mappings, integrity issues, label conflicts) to the CRA-016 serializer (ONT-016): a 10k-concept SKOS thesaurus imports and re-exports losslessly and SKOS-XL labels are preserved
- [ ] CRA-021.7 [AGG] Labels per BCP-47 language tag; deprecation via owl:deprecated true plus dct:isReplacedBy; audited editorial notes; ISO 25964-style thesaurus import fixture
- [ ] CRA-021.8 [OCA] Existing drift detection (drift.py, embeddingdrift.py) emits evolution proposals into CRA-022 review; proposals are never auto-applied (I17)
- [ ] obligation CRA-021.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] multilingual import/edit/export, same-label distinct concepts, cyclic taxonomy policy, polyhierarchy, retired terms and concurrent edits. Change a vocabulary and verify dependent classifier/search output, rollback and evidence preservation. Evaluate domain-specific vocabularies separately from software license rights
- [ ] [MERGED] 10k-concept multilingual round-trip is isomorphic; a drift proposal appears in the review queue and changes nothing until approved
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/skos.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/skos.py#L1-L1)
- tests: `tests/semantic/test_skos_governance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-023 [P1] CRA-023: Canonical Identity, Alignment and Reversible Resolution

- **Source:** `CRAr_cpccaggcc-requirements.md:1290-1327` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-023; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-023. Canonical Identity, Alignment and Reversible Resolution

*Aggregated title: Canonical Identity Resolution & Reversible Entity Merging*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/010/016/019/022 | E (Governed knowledge) | M5 | — | ONT-015 | — | INV-13, INV-37, INV-52, INV-53, INV-54 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/010/016/019/022. Sources INV-13/37/52/53/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-023.1** `[CRAr]` Define scoped source identity and canonical-ID mapping with deterministic idempotency, aliases and source-instance boundaries. Same textual ID in two systems/tenants is not one entity.
- **CRA-023.2** `[CRAr]` Generate alignment/merge candidates with lexical/structural/model evidence, uncertainty, domain rules and NIL/no-match outcomes. Never infer `owl:sameAs` or merge solely from label or vector similarity.
- **CRA-023.3** `[CRAr]` Require approval for high-impact identity/schema changes and run consistency/constraint checks on proposed mappings. Preserve conflicting source claims instead of overwriting them silently.
- **CRA-023.4** `[CRAr]` Support reversible merge/split with relationship assertion/evidence/provenance preservation, temporal history and retraction/rebuild of dependent inferences and indexes.
- **CRA-023.5** `[CRAr]` Evaluate candidate precision/recall/calibration by tenant/domain/language and adverse ambiguity, with held-out gold data. Model changes require reevaluation and versioned review results.
- **CRA-023.6** `[AGG]` Candidate generation combines deterministic keys (email, employee ID, account ID) with probabilistic features (Jaro-Winkler and normalized labels, embedding similarity, neighbourhood structural similarity) and always supports a NIL/no-match outcome.
- **CRA-023.7** `[OCA]` Schema/pack alignment uses a DeepOnto (BERTMap/BERTSubs) service in an isolated GPU/CPU worker (ONT-015); entity linking in text uses spaCy EntityLinker with a tenant-scoped knowledge base generated from the graph (INV-54). All outputs are candidates.
- **CRA-023.8** `[AGG]` An immutable `IdentityMergeLedger` records every merge/split; a split restores the original nodes, edges, evidence and dependent inferences atomically.
- **CRA-023.9** `[GN]` The probabilistic features of CRA-023.6 (embedding similarity, neighbourhood structural similarity) and the al
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-023

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/010/016/019/022. Sources INV-13/37/52/53/54.
- [ ] CRA-023.1 [CRAr] Define scoped source identity and canonical-ID mapping with deterministic idempotency, aliases and source-instance boundaries. Same textual ID in two systems/tenants is not one entity
- [ ] CRA-023.2 [CRAr] Generate alignment/merge candidates with lexical/structural/model evidence, uncertainty, domain rules and NIL/no-match outcomes. Never infer owl:sameAs or merge solely from label or vector similarity
- [ ] CRA-023.3 [CRAr] Require approval for high-impact identity/schema changes and run consistency/constraint checks on proposed mappings. Preserve conflicting source claims instead of overwriting them silently
- [ ] CRA-023.4 [CRAr] Support reversible merge/split with relationship assertion/evidence/provenance preservation, temporal history and retraction/rebuild of dependent inferences and indexes
- [ ] CRA-023.5 [CRAr] Evaluate candidate precision/recall/calibration by tenant/domain/language and adverse ambiguity, with held-out gold data. Model changes require reevaluation and versioned review results
- [ ] CRA-023.6 [AGG] Candidate generation combines deterministic keys (email, employee ID, account ID) with probabilistic features (Jaro-Winkler and normalized labels, embedding similarity, neighbourhood structural similarity) and always supports a NIL/no-match outcome
- [ ] CRA-023.7 [OCA] Schema/pack alignment uses a DeepOnto (BERTMap/BERTSubs) service in an isolated GPU/CPU worker (ONT-015); entity linking in text uses spaCy EntityLinker with a tenant-scoped knowledge base generated from the graph (INV-54). All outputs are candidates
- [ ] CRA-023.8 [AGG] An immutable IdentityMergeLedger records every merge/split; a split restores the original nodes, edges, evidence and dependent inferences atomically
- [ ] CRA-023.9 [GN] The probabilistic features of CRA-023.6 (embedding similarity, neighbourhood structural similarity) and the alignment worker of CRA-023.7 require CRA-043 tiers and, for structural similarity, a CRA-044 model that passed its anti-stub probes; when unavailable the candidate generator reports the reduced feature set used and never substitutes hash or random similarity
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/er/splink_engine.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/er/splink_engine.py#L1-L1), [`packages/eoip/identity/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/__init__.py#L1-L1), [`packages/eoip/identity/alignment.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/alignment.py#L1-L1), [`packages/eoip/identity/evaluation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/evaluation.py#L1-L1), [`packages/eoip/identity/merger.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/merger.py#L1-L1), [`packages/eoip/identity/scoped_table.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/identity/scoped_table.py#L1-L1), [`scripts/build_master_suite.py:226`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/build_master_suite.py#L226-L226), [`scripts/enhance_master_suite.py:173`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/scripts/enhance_master_suite.py#L173-L173)
- tests: `scripts/test_cap_enrichment.py:95`, `scripts/test_master_caps_enrichment.py:109`, `tests/acceptance/test_content_chat_documents_acceptance.py:323`, `tests/semantic/test_identity_resolution.py:1`, `tests/unit/test_splink_er_engine.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-025 [P1] CRA-025: Search, Embeddings and Projection Fidelity

- **Source:** `CRAr_cpccaggcc-requirements.md:1371-1408` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 10, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 3 other site(s): see duplicate task DUP-CRA-025; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-025. Search, Embeddings and Projection Fidelity

*Aggregated title: Tenant-Scoped Vector Similarity & Hybrid Search Projections*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/010/018/023/031 | F (Usable value) | M6 | G12 | — | — | INV-09, INV-10, INV-12, INV-19, INV-39 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/010/018/023/031. Sources G12 and INV-10/39/44/54.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-025.1** `[CRAr]` Version keyword/vector indexes by scope, source/ontology/policy revision, provider/model/tokenizer, dimension, normalization and distance metric.
- **CRA-025.2** `[CRAr]` Distinguish deterministic hashing fixtures from real semantic providers. Provider-disabled/unavailable or dimension mismatch cannot silently populate a production semantic index with hashing or zeros.
- **CRA-025.3** `[CRAr]` Enforce permission filtering at candidate generation and final delivery, with scoped caches and policy-epoch revocation. Do not retrieve unrestricted candidates into externally visible prompts or diagnostics.
- **CRA-025.4** `[CRAr]` Support resumable indexing, deletion, model re-embedding, shadow index evaluation and atomic cutover/rollback. Keep watermarks and explicit stale/unavailable states; projections rebuild from authoritative records.
- **CRA-025.5** `[CRAr]` Evaluate recall@k/nDCG/latency by domain/language and ACL selectivity using a labelled corpus. Record corpus splits and model/config changes; do not use graph proximity as relevance gold automatically.
- **CRA-025.6** `[AGG]` Configurable dense providers (local sentence-transformers models or approved external) plus BM25 sparse retrieval; fusion by Reciprocal Rank Fusion (k = 60 default) with optional graph-centrality signal; vector stores (Qdrant or pgvector candidates) partitioned by tenant.
- **CRA-025.7** `[RES]` The deterministic hashing embedder is renamed and labelled `test-hashing`; the production profile refuses it at startup.
- **CRA-025.8** `[GN]` Graph-structure embeddings (CRA-044) and text embeddings are distinct index families with separate metadata (model, snapshot, dimension, metric) under CRA-025.1; similarity search never mixes vectors from different families or model versions.
- **CRA-025.9** `[GN]` The hash-based vectors of `packages/eoip/gnn/engine.py` (`_deterministic_vector`, `embed_node2vec`, `embed_
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-025

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/010/018/023/031. Sources G12 and INV-10/39/44/54.
- [ ] CRA-025.1 [CRAr] Version keyword/vector indexes by scope, source/ontology/policy revision, provider/model/tokenizer, dimension, normalization and distance metric
- [ ] CRA-025.2 [CRAr] Distinguish deterministic hashing fixtures from real semantic providers. Provider-disabled/unavailable or dimension mismatch cannot silently populate a production semantic index with hashing or zeros
- [ ] CRA-025.3 [CRAr] Enforce permission filtering at candidate generation and final delivery, with scoped caches and policy-epoch revocation. Do not retrieve unrestricted candidates into externally visible prompts or diagnostics
- [ ] CRA-025.4 [CRAr] Support resumable indexing, deletion, model re-embedding, shadow index evaluation and atomic cutover/rollback. Keep watermarks and explicit stale/unavailable states; projections rebuild from authoritative records
- [ ] CRA-025.5 [CRAr] Evaluate recall@k/nDCG/latency by domain/language and ACL selectivity using a labelled corpus. Record corpus splits and model/config changes; do not use graph proximity as relevance gold automatically
- [ ] CRA-025.6 [AGG] Configurable dense providers (local sentence-transformers models or approved external) plus BM25 sparse retrieval; fusion by Reciprocal Rank Fusion (k = 60 default) with optional graph-centrality signal; vector stores (Qdrant or pgvector candidates) partitioned by tenant
- [ ] CRA-025.7 [RES] The deterministic hashing embedder is renamed and labelled test-hashing; the production profile refuses it at startup
- [ ] CRA-025.8 [GN] Graph-structure embeddings (CRA-044) and text embeddings are distinct index families with separate metadata (model, snapshot, dimension, metric) under CRA-025.1; similarity search never mixes vectors from different families or model versions
- [ ] CRA-025.9 [GN] The hash-based vectors of packages/eoip/gnn/engine.py (deterministicvector, embednode2vec, embedtranse) fall under CRA-025.7: removed from production paths, retained only as the HashBaseline test fixture and refused by the production profile at startup (X-40)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/gnn/engine.py:40`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/gnn/engine.py#L40-L40), [`packages/eoip/retrieval/hybrid_vector_service.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/retrieval/hybrid_vector_service.py#L1-L1)
- tests: `tests/retrieval/test_hybrid_vector_search.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-029 [P1] CRA-029: Catalog, Lineage and Enterprise Context

- **Source:** `CRAr_cpccaggcc-requirements.md:1528-1557` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 14, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-029; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-029. Catalog, Lineage and Enterprise Context

*Aggregated title: Enterprise Context Layer & Data Catalog Projections*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-003/010/017/018/024/031 | E (Governed knowledge) | M7 | — | — | I18 | INV-18, INV-24, INV-28, INV-38, INV-39, INV-40, INV-42, INV-43, INV-44, INV-45 | — | — |

**Base statement:** Priority P1. Depends on CRA-003/010/017/018/024/031. Sources INV-24/28/38/39/40/42/43/44/45.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-029.1** `[CRAr]` Maintain technical assets, business terms, owners, classifications, quality observations and lineage as typed linked entities with source/freshness and allowed scope.
- **CRA-029.2** `[CRAr]` Distinguish observed/base metadata, human curation and effective merged view; define field-level precedence, conflict and reset-to-source behavior. A human override cannot silently hide changed source truth indefinitely.
- **CRA-029.3** `[CRAr]` Parse lineage only for supported source/query semantics. Unknown/dynamic statements yield uncertainty and diagnostics, not guessed source-target edges.
- **CRA-029.4** `[CRAr]` Expose data-graph versus schema/meta-graph versus provenance/security graph views with stable links and correct object types. Do not relabel the same graph as different capabilities.
- **CRA-029.5** `[CRAr]` Federate external catalogs through public versioned APIs with authoritative ownership rules, mappings, duplicate prevention and deletion/ACL propagation.
- **CRA-029.6** `[AGG]` Three metadata layers: base (crawler-observed), edit (human curation), merged (effective view by documented precedence) with reset-to-source and conflict indicators; human edits survive later crawls without hiding changed source truth.
- **CRA-029.7** `[AGG]` Propagated classifications (Atlas pattern, INV-45): tagging an asset PII cascades along lineage to downstream columns/views/dashboards through an event trigger, recording provenance so removal reverses the cascade.
- **CRA-029.8** `[AGG]` Metadata projections compatible with OpenMetadata, DataHub and Apache Atlas public APIs.

**Acceptance obligation CRA-029.A** (only after every clause above is ACCEPTED):

- `[CRAr]` source rename after human override, stale owner, conflicting glossary, denied lineage source and failed projection. Show the effective value's supporting layer and revision, rep
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-029

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-003/010/017/018/024/031. Sources INV-24/28/38/39/40/42/43/44/45.
- [ ] CRA-029.1 [CRAr] Maintain technical assets, business terms, owners, classifications, quality observations and lineage as typed linked entities with source/freshness and allowed scope
- [ ] CRA-029.2 [CRAr] Distinguish observed/base metadata, human curation and effective merged view; define field-level precedence, conflict and reset-to-source behavior. A human override cannot silently hide changed source truth indefinitely
- [ ] CRA-029.3 [CRAr] Parse lineage only for supported source/query semantics. Unknown/dynamic statements yield uncertainty and diagnostics, not guessed source-target edges
- [ ] CRA-029.4 [CRAr] Expose data-graph versus schema/meta-graph versus provenance/security graph views with stable links and correct object types. Do not relabel the same graph as different capabilities
- [ ] CRA-029.5 [CRAr] Federate external catalogs through public versioned APIs with authoritative ownership rules, mappings, duplicate prevention and deletion/ACL propagation
- [ ] CRA-029.6 [AGG] Three metadata layers: base (crawler-observed), edit (human curation), merged (effective view by documented precedence) with reset-to-source and conflict indicators; human edits survive later crawls without hiding changed source truth
- [ ] CRA-029.7 [AGG] Propagated classifications (Atlas pattern, INV-45): tagging an asset PII cascades along lineage to downstream columns/views/dashboards through an event trigger, recording provenance so removal reverses the cascade
- [ ] CRA-029.8 [AGG] Metadata projections compatible with OpenMetadata, DataHub and Apache Atlas public APIs
- [ ] obligation CRA-029.A (only after every clause above is ACCEPTED)
- [ ] [CRAr] source rename after human override, stale owner, conflicting glossary, denied lineage source and failed projection. Show the effective value's supporting layer and revision, repair after replay and demonstrate permitted query results through real API/UI/MCP
- [ ] [MERGED] A human description in the edit layer survives the next crawler run while the conflict indicator shows a changed source value (AGG)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/catalog/__init__.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/__init__.py#L1-L1), [`packages/eoip/catalog/classification_propagation.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/classification_propagation.py#L1-L1), [`packages/eoip/catalog/layered_metadata.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/layered_metadata.py#L1-L1), [`packages/eoip/catalog/lineage_parser.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/lineage_parser.py#L1-L1), [`packages/eoip/catalog/multi_graph_views.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/multi_graph_views.py#L1-L1), [`packages/eoip/catalog/projections.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/catalog/projections.py#L1-L1), [`packages/eoip/connectors/snowflake.py:10`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/connectors/snowflake.py#L10-L10)
- tests: `tests/acceptance/test_warehouses_catalogs_acceptance.py:292`, `tests/semantic/test_catalog_lineage_context.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-034 [P1] CRA-034: Migration, Portability and Rollback

- **Source:** `CRAr_cpccaggcc-requirements.md:1694-1729` (heading) · **Type:** Non-Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-034; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-034. Migration, Portability and Rollback

*Aggregated title: Migration CLI & Zero-Downtime Cutover Tooling*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-016/017/018/022/033/035 | H (Deploy and migrate) | M8 | — | ONT-001, ONT-017 | I10 | INV-06, INV-14, INV-15, INV-16, INV-26, INV-32, INV-33, INV-34, INV-35, INV-40 | — | — |

**Base statement:** Priority P1. Depends on CRA-016/017/018/022/033/035. Sources INV-01/15/16/25/26/32/34/35/40.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-034.1** `[CRAr]` Implement documented export/convert/validate/compare/replay/cutover/rollback tooling using the existing CLI conventions, with dry-run and explicit source/target scope. Do not document nonexistent executable commands as available.
- **CRA-034.2** `[CRAr]` Preserve source IDs/IRIs, blank-node semantics, literals/languages/datatypes, named graphs, edge assertions, provenance, ACL/retention and ontology history to the declared fidelity profile.
- **CRA-034.3** `[CRAr]` Generate a feature/loss/unsupported ledger and source-target reconciliation counts plus independent semantic/query comparisons. Never declare migration lossless when required constructs are dropped/coerced.
- **CRA-034.4** `[CRAr]` Stage and shadow-read from a pinned source watermark; replay deltas including ACL/delete events. Bind cutover approval to exact source, mapping, target and policy revision.
- **CRA-034.5** `[CRAr]` Support rollback of routing and compatible data/projections, with separately governed external-action compensation. Retain source until qualified restore/query/ACL checks pass.
- **CRA-034.6** `[AGG]` Design the `eoip-migrate` CLI (status PROPOSED until implemented): `discover --source <uri>`, `export --output <path>` (canonical Turtle/N-Quads with SHA-256 manifest), `validate --input <path>`, `compare`, `replay`, `cutover`, `rollback`; documentation must not present it as available before it exists.
- **CRA-034.7** `[AGG]` Eight-stage protocol: discovery and pin; format extraction with hashes; mapping synthesis with loss analysis; staged loading; semantic-equivalence verification with golden queries; CDC catch-up; atomic cutover; rollback window (default 14 days, read-only shadow source).
- **CRA-034.8** `[OCA]` R2RML/RML imports from Ontop, Morph-KGC and RMLStreamer users translate into CML/IR (ONT-017) with unsupported constructs reported
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-034

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-016/017/018/022/033/035. Sources INV-01/15/16/25/26/32/34/35/40.
- [ ] CRA-034.1 [CRAr] Implement documented export/convert/validate/compare/replay/cutover/rollback tooling using the existing CLI conventions, with dry-run and explicit source/target scope. Do not document nonexistent executable commands as available
- [ ] CRA-034.2 [CRAr] Preserve source IDs/IRIs, blank-node semantics, literals/languages/datatypes, named graphs, edge assertions, provenance, ACL/retention and ontology history to the declared fidelity profile
- [ ] CRA-034.3 [CRAr] Generate a feature/loss/unsupported ledger and source-target reconciliation counts plus independent semantic/query comparisons. Never declare migration lossless when required constructs are dropped/coerced
- [ ] CRA-034.4 [CRAr] Stage and shadow-read from a pinned source watermark; replay deltas including ACL/delete events. Bind cutover approval to exact source, mapping, target and policy revision
- [ ] CRA-034.5 [CRAr] Support rollback of routing and compatible data/projections, with separately governed external-action compensation. Retain source until qualified restore/query/ACL checks pass
- [ ] CRA-034.6 [AGG] Design the eoip-migrate CLI (status PROPOSED until implemented): discover --source <uri>, export --output <path> (canonical Turtle/N-Quads with SHA-256 manifest), validate --input <path>, compare, replay, cutover, rollback; documentation must not present it as available before it exists
- [ ] CRA-034.8 [OCA] R2RML/RML imports from Ontop, Morph-KGC and RMLStreamer users translate into CML/IR (ONT-017) with unsupported constructs reported
- [ ] obligation CRA-034.A (only after every clause above is ACCEPTED)
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/migration/cli.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/migration/cli.py#L1-L1), [`packages/eoip/migration/protocol.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/migration/protocol.py#L1-L1), [`packages/eoip/migration/r2rml_importer.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/migration/r2rml_importer.py#L1-L1)
- tests: `tests/acceptance/test_migration_portability_acceptance.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-041 [P1] CRA-041: Truthful Positioning, Competitive Claims and Disclosure Governance

- **Source:** `CRAr_cpccaggcc-requirements.md:1931-1958` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 8, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-041; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-041. Truthful Positioning, Competitive Claims and Disclosure Governance

*Aggregated title: (new in combined specification)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001/035/036/037/042 | I (Independent acceptance) | M9 | F4, F5 | ONT-012 | I1, I3, I6, I11, I13, I15, I16, I17 | — | X-19, X-20 | H-05, H-12 |

**Base statement:** Priority P1. Depends on CRA-001/035/036/037/042. Sources OCA ONT-012, risk OR6, inversions I1-I20 'already won' list, OCA evidence caveat, OCA section 8.3 patent candidates, CRA section 1 'do not advertise superiority'.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-041.1** `[RES]` Maintain a versioned Claims Register in the repository (`docs/claims/claims-register.yaml`). Every externally visible statement about EOIP capability, standards conformance, performance, cost, security or competitive position has a claim ID, exact wording, scope (edition/profile/deployment), evidence references (ledger clause IDs, benchmark receipt digests, review records), owner, approval and expiry date.
- **CRA-041.2** `[RES]` No standards-conformance claim (RDF 1.1, JSON-LD 1.1, OWL 2 profile, SHACL Core, SPARQL 1.1, WCAG 2.2 AA) may be published until the corresponding requirements (CRA-016, CRA-019, CRA-020, CRA-024, CRA-030) and the round-trip certification gate (CRA-016 clause for ONT-019) are ACCEPTED for the declared profile. This closes risk OR6.
- **CRA-041.3** `[RES]` The seven inversions labelled 'already won' in the indicative analysis (I1, I3, I6, I13, I15, I16, I17) are hypotheses until re-verified on the pinned baseline commit with receipts. They may be positioned only with the scoped wording approved in the Claims Register; 'no competitor has this' wording requires a dated, sourced competitor review (CRA-042) and Legal approval.
- **CRA-041.4** `[RES]` The Ontology-as-Code positioning package (ONT-012) consists of: a factual capability description of the existing GitOps layer (branch, PR, review gate, semantic diff, impact analysis, migration-script generation, rollback receipts, semver computation, release packaging), a dated comparison table against TopBraid EDG, Protégé/WebProtégé and Chowlk/OnToology with source links, and a limitations section. It is published only after CRA-022 clauses covering those capabilities are ACCEPTED.
- **CRA-041.5** `[RES]` Competitor performance, TCO, pricing or
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-041

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-001/035/036/037/042. Sources OCA ONT-012, risk OR6, inversions I1-I20 'already won' list, OCA evidence caveat, OCA section 8.3 patent candidates, CRA section 1 'do not advertise superiority'.
- [ ] Base statement: Priority P1. Depends on CRA-001/035/036/037/042. Sources OCA ONT-012, risk OR6, inversions I1-I20 'already won' list, OCA evidence caveat, OCA section 8.3 patent candidates, CRA section 1 'do not advertise superiority'
- [ ] CRA-041.1 [RES] Maintain a versioned Claims Register in the repository (docs/claims/claims-register.yaml). Every externally visible statement about EOIP capability, standards conformance, performance, cost, security or competitive position has a claim ID, exact wording, scope (edition/profile/deployment), evidence references (ledger clause IDs, benchmark receipt digests, review records), owner, ap
- [ ] CRA-041.2 [RES] No standards-conformance claim (RDF 1.1, JSON-LD 1.1, OWL 2 profile, SHACL Core, SPARQL 1.1, WCAG 2.2 AA) may be published until the corresponding requirements (CRA-016, CRA-019, CRA-020, CRA-024, CRA-030) and the round-trip certification gate (CRA-016 clause for ONT-019) are ACCEPTED for the declared profile. This closes risk OR6
- [ ] CRA-041.3 [RES] The seven inversions labelled 'already won' in the indicative analysis (I1, I3, I6, I13, I15, I16, I17) are hypotheses until re-verified on the pinned baseline commit with receipts. They may be positioned only with the scoped wording approved in the Claims Register; 'no competitor has this' wording requires a dated, sourced competitor review (CRA-042) and Legal approval
- [ ] CRA-041.4 [RES] The Ontology-as-Code positioning package (ONT-012) consists of: a factual capability description of the existing GitOps layer (branch, PR, review gate, semantic diff, impact analysis, migration-script generation, rollback receipts, semver computation, release packaging), a dated comparison table against TopBraid EDG, Protégé/WebProtégé and Chowlk/OnToology with source links, and a 
- [ ] CRA-041.5 [RES] Competitor performance, TCO, pricing or revenue figures that originate from vendor or self-interested sources (for example negotiation-consultancy TCO claims) are marked UNVERIFIED and may not appear in customer-facing material unless independently verified, attributed and Legal-approved
- [ ] CRA-041.6 [RES] Patent-candidate disclosure control: the five candidates listed in OCA section 8.3 (semver from semantic diff; migration-script generation from ontology diff; hybrid per-rule materialize/virtualize reasoning with a cost model; AI-suggested declarative source-to-ontology mappings; combined structural plus embedding drift driving evolution proposals) are recorded in a restricted regi
- [ ] CRA-041.7 [RES] Indicative scorecards (ontology-comparison-matrix.csv, the aggregated master matrix, EOIP self-scores 2.9/3.6/4.2) are internal planning aids. Any external use requires evidence-qualified rescoring under CRA-042 and must state the scoring method, date and evidence confidence
- [ ] obligation CRA-041.A (only after every clause above is ACCEPTED)
- [ ] [RES] Attempt to publish (a) a SHACL conformance claim while CRA-020 is not ACCEPTED, (b) an 'already won' inversion without a receipt, (c) a competitor TCO figure marked UNVERIFIED, and (d) a document describing a patent-candidate mechanism without a Legal decision. The claims check (CI job over docs/ and release notes) must block all four with specific reasons. Legal and Marketing review records
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/positioning_pack.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/positioning_pack.py#L1-L1), [`packages/eoip/claims/registry.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/registry.py#L1-L1), [`packages/eoip/claims/scanner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/scanner.py#L1-L1), [`packages/eoip/claims/schema.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/schema.py#L1-L1), [`tools/claims/check_claims.py:2`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/tools/claims/check_claims.py#L2-L2)
- tests: `tests/acceptance/test_claims_governance_acceptance.py:2`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-CRA-042 [P1] CRA-042: Competitive Research Qualification and Maintenance

- **Source:** `CRAr_cpccaggcc-requirements.md:1959-1986` (heading) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 21, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 4 other site(s): see duplicate task DUP-CRA-042; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.5 h (S, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
#### CRA-042. Competitive Research Qualification and Maintenance

*Aggregated title: (new in combined specification)*

| Priority | Depends on | Gate | Module | Gaps | ONT | I | INV | Conflicts | Decisions |
|---|---|---|---|---|---|---|---|---|---|
| P1 | CRA-001 | A (Truthful baseline) | M9 | — | — | — | — | X-22, X-23, X-24, X-25 | — |

**Base statement:** Priority P1. Depends on CRA-001. Sources CRA sections 2.2, 5, 6.1, 19 'remaining research'; competitive-research-matrix.csv (ND values); ontology-comparison-matrix.csv; AGG section 4 master matrix; conflict register X-01..X-33.

**Clauses** (each is an independently tracked acceptance obligation):

- **CRA-042.1** `[RES]` Maintain one research record per tool family C01-C55 under `research/competitive/<id>.yaml`: tool family, category, reviewed baseline date, pinned product/edition/version or commit, license snapshot (file hash and URL), primary evidence URLs, 22 dimension scores each either 1-5 with written rationale and confidence, or `ND` with the missing evidence named.
- **CRA-042.2** `[RES]` Keep the three scoring datasets separate and labelled: evidence-qualified (competitive-research-matrix.csv, 7 scored dimensions, 15 ND), indicative (ontology-comparison-matrix.csv, all dimensions scored, 'not audited'), aggregated (AGG master matrix, all dimensions scored, unsourced). They must never be averaged, merged into one league table, or used to replace an ND value.
- **CRA-042.3** `[RES]` Resolve every item in the version and investigation register (CRA section 6.1): pin exact release, artifact checksum, source/license snapshot and lifecycle before any tool is procured, embedded, benchmarked or named as a certified backend.
- **CRA-042.4** `[RES]` Re-verify each conflict-register item marked RESEARCH (licenses for WebProtégé, LODE, TerminusDB, FIBO, schema.org, Openllet, extract-msg; gist size; vendor ownership changes) against primary sources and record the dated outcome. A verified outcome that changes a decision triggers a change to this specification through CRA-022-style review.
- **CRA-042.5** `[RES]` Perform hands-on qualification for every third-party engine EOIP will depend on or certify (at minimum rdflib, pySHACL, OWL API, ELK, Apache Jena/Fuseki, GraphDB as certified backend, Ontop, Morph-KGC, DeepOnto, spaCy, chosen OCR/ASR engines) using pinned artifacts, licensed evaluation rights and the CRA-036 harness; record results as receipts.
- **CRA-042.6** `[RES]` Record unavailable or contra
[… truncated, see requirement_tasks.json]
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-CRA-042

**Acceptance criteria**
- [ ] Priority P1. Depends on CRA-001. Sources CRA sections 2.2, 5, 6.1, 19 'remaining research'; competitive-research-matrix.csv (ND values); ontology-comparison-matrix.csv; AGG section 4 master matrix; conflict register X-01..X-33.
- [ ] CRA-042.1 [RES] Maintain one research record per tool family C01-C55 under research/competitive/<id>.yaml: tool family, category, reviewed baseline date, pinned product/edition/version or commit, license snapshot (file hash and URL), primary evidence URLs, 22 dimension scores each either 1-5 with written rationale and confidence, or ND with the missing evidence named
- [ ] CRA-042.2 [RES] Keep the three scoring datasets separate and labelled: evidence-qualified (competitive-research-matrix.csv, 7 scored dimensions, 15 ND), indicative (ontology-comparison-matrix.csv, all dimensions scored, 'not audited'), aggregated (AGG master matrix, all dimensions scored, unsourced). They must never be averaged, merged into one league table, or used to replace an ND value
- [ ] CRA-042.3 [RES] Resolve every item in the version and investigation register (CRA section 6.1): pin exact release, artifact checksum, source/license snapshot and lifecycle before any tool is procured, embedded, benchmarked or named as a certified backend
- [ ] CRA-042.4 [RES] Re-verify each conflict-register item marked RESEARCH (licenses for WebProtégé, LODE, TerminusDB, FIBO, schema.org, Openllet, extract-msg; gist size; vendor ownership changes) against primary sources and record the dated outcome. A verified outcome that changes a decision triggers a change to this specification through CRA-022-style review
- [ ] CRA-042.5 [RES] Perform hands-on qualification for every third-party engine EOIP will depend on or certify (at minimum rdflib, pySHACL, OWL API, ELK, Apache Jena/Fuseki, GraphDB as certified backend, Ontop, Morph-KGC, DeepOnto, spaCy, chosen OCR/ASR engines) using pinned artifacts, licensed evaluation rights and the CRA-036 harness; record results as receipts
- [ ] CRA-042.6 [RES] Record unavailable or contradictory sources (for example the OnToology site timing out, Fabric preview limits, vendor marketing scale claims) as explicit evidence gaps rather than negative findings or positive scores
- [ ] CRA-042.7 [RES] Refresh every research record at least every 6 months or on a major competitor release; each refresh produces a dated delta entry. Stale records (>6 months) are shown as STALE in the tracker and dashboard
- [ ] obligation CRA-042.A (only after every clause above is ACCEPTED)
- [ ] [RES] Run the research-dataset validator: every score is an integer 1-5 with rationale or ND with a named gap; no record lacks a reviewed date; no tool named as a dependency/backend lacks a pinned artifact and license snapshot; conflict items marked RESEARCH have dated outcomes or remain OPEN. Introduce a fixture record with a blank score, an averaged score and an unpinned dependency; the validato
- [ ] Not evidence of completion
- [ ] Existence of a file, class, function, route, test file, test name, UI control, registry entry or commit message
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/claims/registry.py:187`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/registry.py#L187-L187), [`packages/eoip/claims/scanner.py:172`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/scanner.py#L172-L172), [`packages/eoip/claims/schema.py:42`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/claims/schema.py#L42-L42), [`tools/research/validate_research.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/tools/research/validate_research.py#L1-L1)
- tests: `tests/acceptance/test_claims_governance_acceptance.py:173`, `tests/research/test_competitive_research_acceptance.py:3`, `tests/research/test_validate_research.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-ONT-011 [P1] ONT-011: MCP server for ontology + Actions · P1 · S

- **Source:** `CRAr_cpccaggcc-requirements.md:2630-2630` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ONT-011; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-011 | MCP server for ontology + Actions | P1 | S | Tier 1 — Differentiators | ONT-009 | CRA-039 | CRA-039.7
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ONT-011

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-011 | MCP server for ontology + Actions | P1 | S | Tier 1 — Differentiators | ONT-009 | CRA-039 | CRA-039.7»
- [ ] MCP server for ontology + Actions
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/tools_contract/mcp_server.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/tools_contract/mcp_server.py#L1-L1)
- tests: `tests/acceptance/test_developer_ecosystem_acceptance.py:323`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-ONT-013 [P1] ONT-013: Ontology pitfall scanner · P1 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2632-2632` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 22, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ONT-013; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-013 | Ontology pitfall scanner | P1 | M | Tier 1 — Differentiators | ONT-001 | CRA-022 | CRA-022.7
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ONT-013

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-013 | Ontology pitfall scanner | P1 | M | Tier 1 — Differentiators | ONT-001 | CRA-022 | CRA-022.7»
- [ ] Tier 1 — Differentiators
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/lint/rules.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/lint/rules.py#L1-L1), [`packages/eoip/ontology/lint/scanner.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/lint/scanner.py#L1-L1)
- tests: `tests/semantic/test_lint_rules.py:1`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-ONT-020 [P1] ONT-020: Ontology benchmark harness · P1 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2639-2639` (table_row) · **Type:** Functional · **Severity:** Medium
- **Now:** Partially Implemented / L2 (tests passed 11, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ONT-020; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-020 | Ontology benchmark harness | P1 | M | Tier 2 — Completeness | ONT-002 | CRA-036 | CRA-036.7
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ONT-020

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-020 | Ontology benchmark harness | P1 | M | Tier 2 — Completeness | ONT-002 | CRA-036 | CRA-036.7»
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- tests: `tests/acceptance/test_correctness_performance_acceptance.py:188`

**Proof plan (1.1):** have ['L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

## RT-ONT-014 [P2] ONT-014: HTML ontology documentation generator · P2 · M

- **Source:** `CRAr_cpccaggcc-requirements.md:2633-2633` (table_row) · **Type:** Functional · **Severity:** Low
- **Now:** Partially Implemented / L2 (tests passed 9, failed 0)
- **Gaps:** Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close; ID defined at 1 other site(s): see duplicate task DUP-ONT-014; No L3: no L3-eligible CI workflow green on the audited commit; No L4 non-prod runtime evidence
- **Depends on:** FT-F04, FT-F09 · **Effort:** 1.0 h (XS, medium confidence)

<details><summary>Requirement text (verbatim)</summary>

```text
ONT-014 | HTML ontology documentation generator | P2 | M | Tier 2 — Completeness | ONT-001 | CRA-039 | CRA-039.8
```
</details>

**Next steps**
1. Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow (validation-evidence.yml, ci.yml)
2. Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions
3. Record the green run id as L3 on the same commit as the L2 run
4. Resolve duplicate definition first: DUP-ONT-014

**Acceptance criteria**
- [ ] Row contract holds exactly as specified: «ONT-014 | HTML ontology documentation generator | P2 | M | Tier 2 — Completeness | ONT-001 | CRA-039 | CRA-039.8»
- [ ] HTML ontology documentation generator
- [ ] Tier 2 — Completeness
- [ ] At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)

**Mapped paths**
- code: [`packages/eoip/ontology/doc_generator.py:1`](https://github.com/Vibe-A-Thon/EIOP/blob/3ed3acd50e47ab8867aa6885d202f9956358dc3a/packages/eoip/ontology/doc_generator.py#L1-L1)
- tests: `tests/acceptance/test_developer_ecosystem_acceptance.py:368`

**Proof plan (1.1):** have ['L1', 'L2']; needs ['L2', 'L3 (same commit) or L4']; missing ['L3 (same commit) or L4']

