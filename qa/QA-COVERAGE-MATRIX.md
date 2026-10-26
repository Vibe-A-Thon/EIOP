# EOIP QA coverage and completion matrix

This matrix identifies the automation surface for the application suite. `qa/manifest.json` is the executable source of suite IDs and safety gates; `qa/test-catalog.json` indexes existing test files. **Existence of a test, command or receipt does not establish feature completion.** An area closes only after its real environment, assertions, failure modes, evidence and owner review are satisfied.

| QA discipline | Current automated evidence | Gap or release condition |
|---|---|---|
| Unit and component | `tests/unit`, `apps/web` unit tests, `vscode-unit`; `qa.portfolio` runs them | Map critical modules and negative branches to owners; track mutation score separately |
| API route inventory | `api-surface` pins all 751 OpenAPI method/path pairs; `probe-coverage` maps 14 dedicated QA request operations; disabled Postman blueprint catalog covers request design | 737 operations lack a dedicated bench probe; add reviewed tests by risk/usage, not indiscriminate mutation. A blueprint is not a test. |
| API documentation quality | `schema-quality` pins 237 empty schemas and two success responses without content | Replace empty schemas with typed response contracts and verify body semantics |
| Postman read-only | 17 verified GET probes for health, auth, admin, graph, query, reporting and product | Expand only through reviewed safe allowlists; never infer a GET is side-effect-free solely from its method |
| Postman functional workflow | Seven-step source CRUD collection with loopback/disposable guard | Newman dependency audit is currently unacceptable for CI; use the Python equivalent until an approved runtime exists |
| In-process functional workflow | `source-workflow` creates, reads, duplicates, renames, lists, deletes and verifies absence in temp storage | Add further high-value workflows by module, with cleanup and no shared data |
| Python contract tests | `tests/contract`, plus current OpenAPI pins | Add independent consumers and serialized schema migration tests |
| HTTP security and RBAC | `tests/security`; missing/invalid bearer denial matrix across all protected OpenAPI operations | Complete per-persona/tenant positive and negative permissions; source webhooks have separate trust rules; 401 correlation header is currently absent |
| Privacy and LLM no-egress | Existing `tests/integration/test_privacy_governance_and_no_egress.py` | Run seeded canaries in a controlled network sandbox; verify logs, exports, telemetry and providers |
| Supply chain and licensing | `tests/compliance`, policy/SBOM code | Fresh advisory scan, signed release artifacts, artifact-specific SBOM and legal review still required |
| Fuzz/property | `tests/fuzz` and property-oriented tests | Add corpus minimization, continuous fuzz budgets and parser-specific coverage targets |
| Integration and protocols | `tests/integration`, `mcp` suite invokes all 18 MCP tools over streamable HTTP with mocked upstream request assertions | Validate each tool's real API semantics, external MCP peers and service versions in an isolated topology |
| Connector conformance | `tests/connectors` | Certify real sandbox accounts with synthetic data, rate limits, outages and permissions |
| Graph/semantic/query | `domain-engines` suite, query and semantic tests | Gold datasets, migration/dialect matrix, precision/recall and large graph scale |
| AI, RAG and neural | `ai-evals` suite and oracle tests | Versioned datasets, groundedness/citation grading, bias/safety, model drift and reproducibility thresholds |
| Frontend unit/build | `web-unit`, `web-build` | Component-level interaction and visual acceptance evidence |
| Browser UI and accessibility | `browser-quality`, existing Playwright GUI tests, axe | Manual screen-reader, keyboard, contrast and reduced-motion review; supported browser/device matrix |
| VS Code extension | `vscode-unit`; extension-host test exists as `vscode-ui` | Install/test on supported VS Code/OS versions and real local MCP/API endpoints |
| Reporting/analytics | Existing API/browser/acceptance tests indexed by catalog | Golden exports, large datasets, schedule delivery and permission matrix |
| Performance smoke | `bounded-load` k6 GET-only 2 VUs/30s; `performance-inprocess` tests | Define production SLOs from representative workload and run isolated capacity tests |
| Stress, soak and scalability | Existing graph benchmark script | Approved multi-hour budget, resource telemetry, saturation/failure criteria, rollback |
| Resilience and DLQ | `resilience-unit`, existing fault injector | Multi-service chaos in disposable environment, failover recovery and real dependency outages |
| Backup, restore and migration | Existing backup/restore acceptance tests | Full restore to a fresh deployment, measured RPO/RTO, downgrade/upgrade and data reconciliation |
| Deployment and packaging | CI build plus deployment scripts | Customer-installed, SaaS, air-gap, upgrade and rollback matrix with signed artifacts |
| Observability and audit | Existing observability acceptance/integration tests; live header capture | Correlation across denied requests, logs/traces/metrics, alert delivery and retention/privacy review |
| Internationalization | Web unit tests include i18n module | Locale expansion, long text, RTL if supported, number/date formatting and accessibility review |
| Cross-browser/device | Chromium Playwright quality checks | Firefox/WebKit/Edge and physical mobile/desktop devices per product support policy |
| DAST and penetration | No approved automated scan in this bench | Authorized scope, isolated deployment, scanner policy, human triage and remediation verification |
| Compliance and entitlements | Existing compliance tests | Release-artifact license notices, customer entitlement paths, legal sign-off |
| Documentation and usability | Static docs/manuals and browser checks | Task-based user observation, install instructions executed by a clean-room team |

## Gate rules

1. **Quick CI:** harness, route drift, probe inventory, schema-quality regression and disposable source workflow. No customer data or external system required.
2. **Extended local/CI:** named contract, security, privacy, compliance, frontend, extension and other existing suites. Expensive suites require `--allow-expensive`; infrastructure suites require `--allow-infrastructure`.
3. **Release candidate:** attach suite receipts to a specific commit and deployment, record dataset/fixture hashes, capture defects and owner sign-off. A blocked category stays blocked. Do not translate a static test count into a completion percentage.
4. **External and destructive QA:** require an isolated account/topology, non-production synthetic data, approved target and timeout, rollback/cleanup, egress/secret controls and explicit go/no-go criteria.
5. **Completeness inventory:** `python -m qa.completeness report` enumerates every current API operation, MCP registration, Python module and web/extension source module. `python -m qa.completeness gate` remains blocked until every item has current executed behavioral evidence, required failure/security paths and reviewed release sign-off. Coverage percentages or static references alone cannot clear it.

## Prioritized automation backlog

1. Remove embedded role tokens and tracked runtime-data defaults from `qa_bench/`, then promote its API/Selenium/E2E suites only after an isolated rerun.
2. Type the 239 successful-response schema findings, starting with auth, admin, sources, query, reporting and export routes; add runtime schema probes as each contract becomes real.
3. Define supported SaaS and customer-installed deployment matrices, then automate clean install, upgrade, backup restore and rollback against disposable stacks.
4. Add approved dependency advisory/SBOM/signature scanning for exact release artifacts; do not depend on a Newman tree with known critical advisories.
5. Establish representative workload SLOs and datasets before making scale or latency claims; run soak/chaos only in approved infrastructure.
6. Add manual assistive-technology, security and usability sign-offs, with defects linked to reproducible evidence.
