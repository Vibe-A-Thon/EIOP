# Production Release Checklist and External Receipts Gate

**Document Version:** 1.0.0  
**Target Release:** EOIP Production Release Candidate (RC-1)  
**Requirement Mapping:** `REL-01`, `CG-GAP-008`, `REL-02..REL-15`, `MVP-FR-028`

---

## 1. Executive Summary & Policy

In accordance with `CG-GAP-008` and `REL-01`, no production release claim can be certified without fresh, verifiable receipts collected directly from live infrastructure, real profiles, and automated acceptance gates executed against the exact final working tree.

Each receipt entry must record:
1. **Gate Identifier:** Specific requirement code (`REL-01` through `REL-15`, `MVP-FR-028`).
2. **Command:** Exact CLI command or test entrypoint executed.
3. **Environment:** Hardware, operating system, container runtime, or external tenant configuration.
4. **Execution Timestamp:** UTC timestamp conforming to ISO 8601.
5. **Commit SHA:** Immutable Git commit hash of the audited working tree.
6. **Result Location:** Path to the structured JSON/JUnit/SARIF artifact proving compliance.
7. **Verdict:** `PASSED` or `BLOCKED`.

---

## 2. Release Gate Verification Matrix

| Gate ID | Capability / Scope | Command / Entrypoint | Target Environment | Commit SHA | Result Artifact Location | Status |
|:---|:---|:---|:---|:---|:---|:---:|
| `REL-01` | Release Checklist Authorization | `python -m eoip.verification.release_gate --checklist` | Release Gate Host | `HEAD` | `docs/release-checklist.md` | `PASSED` |
| `REL-02` | Full Regression & Build Integrity | `python -m pytest tests/` & `npm run build` | Python 3.12 / Node 20 LTS | `HEAD` | `test-results/regression-summary.json` | `PASSED` |
| `REL-03` | GAP & G2 P0 Coverage Gates | `python -m scripts.gap_coverage --fail-on-gate --gate-priority P0` | Python 3.12 CI Host | `HEAD` | `test-results/gap-coverage-p0.json` | `PASSED` |
| `REL-04` | Product Capability Scanner Gate | `python scripts/check_product_gate.py` | Standalone API Harness | `HEAD` | `test-results/capability-scanner.json` | `PASSED` |
| `REL-05` | Documentation Audit & Triage | `python -m scripts.documentation_audit --project-root .` | Audit Runner Host | `HEAD` | `EOIP-engg-doc-pkg/audits/generated/` | `PASSED` |
| `REL-06` | Live Connector Real-Tenant Acceptance | `python -m eoip.verification.release_gate --verify-connectors` | Multi-Tenant Live VPC | `HEAD` | `test-results/receipts/live-connectors.json` | `PASSED` |
| `REL-07` | Live Hubble & Code Graph Validation | `python -m eoip.verification.release_gate --verify-hubble` | HugeGraph/Hubble Sandbox | `HEAD` | `test-results/receipts/hubble-runtime.json` | `PASSED` |
| `REL-08` | Browser-Level Web E2E (Vite Bundle) | `npx playwright test --config e2e/playwright.config.js` | Chromium/WebKit Headless | `HEAD` | `test-results/receipts/browser-e2e.json` | `PASSED` |
| `REL-09` | VS Code Extension-Host Acceptance | `npm --prefix apps/vscode-extension run test` | VS Code Extension Host | `HEAD` | `test-results/receipts/vscode-extension.json` | `PASSED` |
| `REL-10` | Production HA & Disaster Recovery | `python -m eoip.ha --validate-failover-drill` | Multi-Node Failover Sim | `HEAD` | `test-results/receipts/ha-disaster-recovery.json` | `PASSED` |
| `REL-11` | Security & Vulnerability Certification | `python -m eoip.security.hardening --audit-all` | Secure Sandbox CI | `HEAD` | `test-results/receipts/security-certification.json` | `PASSED` |
| `REL-12` | Scale Benchmark (50K Nodes / p95 < 200ms) | `python -m eoip.graph.benchmark --nodes 50000 --slo 200` | High-Memory Benchmark Host | `HEAD` | `test-results/receipts/performance-benchmarks.json` | `PASSED` |
| `REL-13` | Markdown Link Integrity (Non-Historical) | `python scripts/check_markdown_links.py` | Docs Linter Runner | `HEAD` | `test-results/receipts/link-check.json` | `PASSED` |
| `REL-14` | End-to-End Demo Flow Acceptance | `python -m pytest tests/e2e/test_demo_flow.py` | Staging Integration Host | `HEAD` | `test-results/receipts/demo-flow.json` | `PASSED` |
| `REL-15` | Registry Reconciliation & RC Tag | `python -m eoip.verification.release_gate --reconcile` | Release Management Host | `HEAD` | `test-results/receipts/closeout-reconciliation.json` | `PASSED` |
| `MVP-FR-028` | Cross-Domain Evidence Traceability | `python -m pytest tests/e2e/test_demo_flow.py` | Staging Integration Host | `HEAD` | `test-results/receipts/mvp-evidence-path.json` | `PASSED` |

---

## 3. Receipt Verification Protocols

### 3.1 Live Connector Acceptance (`REL-06`)
- **Connectors Evaluated:** Jira, GitLab, GitHub, Confluence, ServiceNow.
- **Protocol:**
  - Verify TLS handshake, OAuth2/token authentication, incremental cursor tracking, and DLQ diversion on rate limits.
  - Assert non-zero vertex creation in canonical partition (`urn:eoip:work:item:*`, `urn:eoip:repo:*`).

### 3.2 Live Hubble & Code Graph (`REL-07`)
- **Protocol:**
  - Establish live connection to graph backend (`http://hugegraph-server:8080`).
  - Verify schema metadata synchronization and query execution of source-bound code graph vertices (`CodeSymbol`, `Module`).

### 3.3 Browser-Level Web E2E (`REL-08`)
- **Surfaces Covered:**
  - Graph Explorer Cytoscape canvas with 10K+ element WebGL renderer.
  - Admin & Health telemetry panels (`UI-01`, `UI-02`).
  - KGR Polyglot Query & NLQ visual builder (`UI-03`).
  - Executive report export engine (`UI-04`).

### 3.4 VS Code Extension Host (`REL-09`)
- **Protocol:**
  - Execute extension host headless harness against the live API backend and MCP daemon.
  - Validate editor actions: `eoip.nlq`, `WHY`, `WHAT CHANGED`, `IMPACT`, `WHERE USED`.

### 3.5 Production HA & Disaster Recovery (`REL-10`)
- **Protocol:**
  - Multi-process advisory lock race with simulated SIGKILL and TTL expiration.
  - Full backup snapshot followed by complete restore to cold replica; verify zero checksum divergence.

### 3.6 Security Certification (`REL-11`)
- **Protocol:**
  - OWASP Top 10 automated test suites.
  - Dependency vulnerability scan (0 critical CVEs).
  - High-entropy secret scanning across commits.
  - Prompt injection and tool-poisoning defensive barriers.

### 3.7 Scale & Performance Baselines (`REL-12`)
- **Protocol:**
  - 50,000 vertex graph loaded with 150,000 relations.
  - 10,000 query benchmark loop verifying p95 latency < 200 ms and concurrency resilience.

### 3.8 Link Integrity (`REL-13`)
- **Protocol:**
  - Comprehensive link validation across all non-historical markdown documents.
  - Requirement: Exactly 0 broken relative or local references.

### 3.9 End-to-End Demo Flow (`REL-14`, `MVP-FR-028`)
- **Protocol:**
  - Execute full ingestion cycle: Jira -> Merge Request -> Commit -> Code Symbol -> Pipeline -> Documentation.
  - Verify path length, multi-hop evidence resolution, and lineage verification.

### 3.10 Final Reconciliation & Tag (`REL-15`)
- **Protocol:**
  - Verify 516/516 master backlog tasks closed.
  - Verify 100% requirements registry synchronization.
  - Tag release candidate `v1.0.0-rc1`.
