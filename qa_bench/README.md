# KnowGridFlow / EOIP — Enterprise QA Automation Test Bench

An enterprise-grade, multi-tier automated QA test harness built specifically for the **KnowGridFlow** platform and its Swiss High-Density Data Workbench GUI.

---

## 1. Test Architecture & Tier Pyramid

```
                       ┌─────────────────────────────────────┐
                       │   Tier 4: End-to-End Workflows     │  Full user journey
                       │       (qa_bench/e2e_workflows)      │  (Auth -> Model -> Proof)
                       ├─────────────────────────────────────┤
                       │   Tier 3: Performance & Stress      │  Concurrency, P50/P95/P99
                       │    (qa_bench/performance_bench)     │  latency profiling
                       ├─────────────────────────────────────┤
                       │   Tier 1: Selenium Web UI (POM)     │  Headless Chrome / Edge,
                       │        (qa_bench/selenium)          │  22+ screen audit, themes
                       ├─────────────────────────────────────┤
                       │   Tier 2: API & Contract Testing    │  RBAC, SHACL, Warrants,
                       │      (qa_bench/api_functional)      │  Multi-tenant isolation
                       └─────────────────────────────────────┘
```

---

## 2. Directory Structure

```
qa_bench/
├── config.py                          # Global credentials, tokens, URLs, timeouts
├── conftest.py                        # Pytest hooks, fixtures, driver lifecycle, screenshots
├── run_qa_bench.py                    # Master CLI orchestrator & diagnostic runner
├── run_qa_bench.ps1                   # Native PowerShell runner for Windows
├── README.md                          # Complete documentation and execution guide
│
├── selenium/                          # Tier 1: Selenium Browser Automation
│   ├── pages/                         # Page Object Model (POM)
│   │   ├── base_page.py               # Robust waits, JS click, theme & error inspectors
│   │   ├── auth_page.py               # /signin form, demo role picker, token validation
│   │   ├── shell_page.py              # Navigation rail, topbar, theme switcher, tenant scope
│   │   ├── graph_explorer_page.py     # Sigma.js WebGL canvas, domain/fact lens, seed search
│   │   ├── ask_ai_page.py             # Ask AI query composer, answer mode toggle, suggestions
│   │   └── query_page.py              # EQL / SPARQL query sandbox, Run execution
│   └── tests/
│       ├── test_auth_and_rbac.py        # Sign-in presets, persona switching, invalid tokens
│       ├── test_workbench_navigation.py # 22-screen audit: verifies rendering without exceptions
│       ├── test_ui_theme_density.py     # 4 themes: dark, light, hc-dark, hc-light
│       ├── test_graph_and_queries.py    # WebGL canvas rendering, lens toggle, EQL queries
│       └── test_ask_ai_citations.py     # Prompt submission, deterministic/narrated modes
│
├── api_functional/                    # Tier 2: API Contract & Functional Tests
│   ├── test_auth_contract.py          # /whoami, RBAC roles, 401 unauthenticated checks
│   ├── test_graph_and_sparql.py       # /graph/backend, /graph/schema, /query/history
│   ├── test_reva_merkle_warrants.py   # REVA Merkle DAG warrant integrity & SHA-256
│   ├── test_multi_tenancy_isolation.py# Strict cross-tenant 403 boundary enforcement
│   ├── test_shacl_validation.py       # SHACL shape export & constraint checking
│   └── test_system_health.py          # Platform vitals & storage tier telemetry
│
├── performance_bench/                 # Tier 3: Concurrency & Stress Profiling
│   ├── test_query_throughput.py       # Concurrent query load, P50/P95/P99 latency checks
│   └── test_supernode_resilience.py   # High-frequency sequential request pooling
│
├── e2e_workflows/                     # Tier 4: End-to-End Enterprise Scenarios
│   └── test_full_lifecycle.py         # Full enterprise investigation lifecycle
│
└── reports/                           # Output test reports and failure artifacts
    └── screenshots/                   # Auto-captured full-page screenshots on test failure
```

---

## 3. Quickstart & Execution Commands

### Prerequisites
1. **Python 3.11+** with dependencies installed:
   ```powershell
   pip install selenium webdriver-manager pytest httpx
   ```
2. **Google Chrome** or **Microsoft Edge** installed.

---

### Running via the Master QA Orchestrator (`run_qa_bench.py`)

#### 1. Run API Contract & Functional Tests (Fast, In-Process)
```powershell
python qa_bench/run_qa_bench.py --suite api
```

#### 2. Run Selenium UI Browser Tests (Headless Chrome)
```powershell
python qa_bench/run_qa_bench.py --suite selenium --headless
```

#### 3. Run Performance & Latency Benchmarks
```powershell
python qa_bench/run_qa_bench.py --suite perf
```

#### 4. Run End-to-End Workflows
```powershell
python qa_bench/run_qa_bench.py --suite e2e
```

#### 5. Run Entire Automation Test Bench with HTML Report
```powershell
python qa_bench/run_qa_bench.py --suite all --headless --report-html
```

---

### Running via PowerShell (`run_qa_bench.ps1`)

```powershell
# Run API suite
.\qa_bench\run_qa_bench.ps1 -Suite api

# Run Selenium suite with visible window (debugging mode)
.\qa_bench\run_qa_bench.ps1 -Suite selenium -Headless $false

# Filter specific tests by keyword
.\qa_bench\run_qa_bench.ps1 -Suite selenium -Filter "test_theme"
```

---

## 4. Test Personas & Role Matrix

| Persona | Role | Default Tenant | Token |
|---|---|---|---|
| **Super Admin** | `superadmin` / `admin` | `*` (All tenants) | `$QA_BENCH_TOKEN_SUPERADMIN` (env var; never committed) |
| **Admin** | `admin` | `default` | `$QA_BENCH_TOKEN_ADMIN` (env var; never committed) |
| **Steward** | `steward` | `default` | `$QA_BENCH_TOKEN_STEWARD` (env var; never committed) |
| **Analyst** | `analyst` | `default` | `$QA_BENCH_TOKEN_ANALYST` (env var; never committed) |
| **Viewer** | `viewer` | `default` | `$QA_BENCH_TOKEN_VIEWER` (env var; never committed) |
| **Bootstrap Root** | `admin` | `default` | `$QA_BENCH_TOKEN_BOOTSTRAP` (env var; never committed) |

---

## 5. Failure Diagnostics & Artifacts

- **Automatic Failure Screenshots:** Whenever any Selenium UI test fails, the test runner automatically captures the browser viewport and saves it to:
  `qa_bench/reports/screenshots/fail_<test_name>.png`
- **Browser Console Audit:** The test runner monitors the browser's console logs and asserts that no `SEVERE` or `Uncaught` JavaScript exceptions occurred during route transitions.
- **HTML Summary Report:** Pass `--report-html` to generate an interactive report at `qa_bench/reports/qa_test_report.html`.
