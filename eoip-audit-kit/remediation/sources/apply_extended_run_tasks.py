"""Apply extended-run (worker C, defects X-01..X-12) results to remediation/findings_tasks.json.

Idempotent: updates overlapping tasks in place (adds `extended_run` evidence) and upserts new
hand-written FT tasks. Audited commit 3ed3acd. Source: audit-output/test_results_extended/.
Run: python3 remediation/sources/apply_extended_run_tasks.py
"""
import json
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
P = KIT / "remediation" / "findings_tasks.json"
EXT = "audit-output/test_results_extended"
ENV = "Python 3.11.17, requirements.lock (fastapi 0.142.2 / starlette 1.7.0), EOIP_DATA_DIR set"
d = json.loads(P.read_text(encoding="utf-8"))
tasks = {t["id"]: t for t in d["tasks"]}
BASE = {k: tasks["FT-D03"][k] for k in ("api_contracts", "data_model", "backward_compatibility",
                                         "performance_targets", "observability")}


def upd(tid, xid, *, evidence, add_notes=(), add_ac=(), add_tests=(), add_cov=(), **fields):
    t = tasks[tid]
    t.update(fields)
    t["extended_run"] = {"defect": xid, "evidence": evidence, "source": f"{EXT}/defects.json", "env": ENV}
    for k, extra in (("implementation_notes", add_notes), ("acceptance_criteria", add_ac),
                     ("automated_tests", add_tests), ("tests_covered", add_cov)):
        cur = list(t.get(k) or [])
        t[k] = cur + [x for x in extra if x not in cur]


def new(**k):
    t = dict(BASE, status="Open", owner="UNASSIGNED", finding=None, preconditions=[], security_controls=[],
             proof_plan={"required_for_closure": "L2 + L3"}, tests_covered=[])
    t.update(k)
    tasks[t["id"]] = t


# ---------------- updates to existing tasks ----------------
upd("FT-F03", "X-01",
    evidence="Reproduced on Python 3.11 + locked deps: whole-file run of tests/security/test_worker_isolation.py exits 137 "
             "after ~1 s inside setsid with a 120 s outer timeout (the two watchdog tests SIGKILL their own pytest process "
             "group). Run per test in its own session: 4/6 pass, 2 fail. DIAGNOSTIC ONLY (not repo code, not proof): a plugin "
             "injecting start_new_session=True into the supervisor Popen gives 6/6 pass in 16.4 s, confirming the fix.",
    add_notes=["packages/eoip/workers/supervisor.py:184-198 (POSIX Popen sets only creationflags; no start_new_session/process_group)",
               "packages/eoip/workers/supervisor.py:89-90 (os.killpg(os.getpgid(pid), SIGKILL))",
               "Fix shown by diagnostic: Popen(..., start_new_session=(sys.platform != 'win32')); diag helper in "
               f"{EXT}/diag/ (not repo code)"],
    add_ac=["tests/security/test_worker_isolation.py::test_memory_balloon_terminated_safely passes",
            "Whole file runs in one pytest process (no setsid wrapper) with exit 0"],
    add_cov=["tests/security/test_worker_isolation.py::test_infinite_loop_timeout_killed_within_one_second",
             "tests/security/test_worker_isolation.py::test_memory_balloon_terminated_safely"],
    estimated_effort={"hours": 2, "band": "S", "notes": "fix confirmed by diagnostic; mostly test + guard"})
upd("FT-D01", "X-02",
    evidence="Confirmed on Python 3.11 + locked deps: the 3 tests hang until pytest-timeout (120 s and 300 s); the stack ends "
             "in engine.py:627 (success_rate acquiring self._lock held by stats()).",
    add_notes=["packages/eoip/intelligence_eng/engine.py:598 (threading.Lock), call chain :646 -> :652 -> :627"])
upd("FT-D03", "X-05",
    evidence="Confirmed in-process on 3.11 and LIVE: the repo's DLQ acceptance flow (deploy/docker-compose.dlq-acceptance.yml, "
             "isolated graph + fixture upstreams) fails both ServiceNow tests (job FAILED); the other 14 live DLQ tests pass.",
    add_notes=["packages/eoip/connectors/servicenow.py:14-19 (DEFAULT_TABLES), :81 (sync iterates every table)",
               "packages/eoip/connectors/rest.py:118 (non-2xx raises ConnectorError and aborts the sync)"],
    add_ac=["Live DLQ acceptance: both ServiceNow tests pass (deploy/docker-compose.dlq-acceptance.yml)"],
    add_tests=["tests/runtime_dlq/test_servicenow_acquisition.py::test_servicenow_http_baseline_incremental_and_replay (live)",
               "tests/runtime_dlq/test_servicenow_rejection.py::test_servicenow_fetched_rejection_and_admission_controls (live)"],
    add_cov=["tests/runtime_dlq/test_servicenow_acquisition.py::test_servicenow_http_baseline_incremental_and_replay",
             "tests/runtime_dlq/test_servicenow_rejection.py::test_servicenow_fetched_rejection_and_admission_controls"],
    proof_plan={"required_for_closure": "L2 (unit + live DLQ) + L3", "l4_candidate": "live DLQ acceptance receipt on the fix commit"})
upd("FT-F07", "X-06",
    evidence="Confirmed on 3.11: test_github_webhook_delete_and_error_categories_are_safe fails with NameError ConnectorError.",
    add_notes=["packages/eoip/connectors/github.py:16-21 (import block lacks ConnectorError)",
               "raise sites confirmed by the extended run: github.py:197,206,257,263,294"])
upd("FT-D07", "X-08",
    evidence="Confirmed on 3.11 (X-08 = this task; no new task). Test fails with 'Audit digest changed; explicitly reconcile "
             "the baseline before importing'.",
    add_notes=["packages/eoip/verification/cp_registry.py:16 (AUDIT_SHA256 pin), :83-84 (digest compare + raise)"],
    add_ac=["Reconciliation recorded with reason + old/new digest and AUDIT_COUNT in the commit message or a baseline log"])
upd("FT-D08", "X-09",
    evidence="Covered by this task (X-09 = FT-D08; no new task). Confirmed on 3.11: the receipt "
             ".audit-scratch/receipts/CRA-001.1/run-20261018T080214Z-86eedb6d.json referenced by the tracked ledger is not in "
             "the repo, so test_cra_001_9 fails.",
    add_notes=["tests/acceptance/test_cra_001_acceptance.py:122 (receipt existence + sha256 assertion)"])
upd("FT-D10", "X-harness (test_authn)",
    evidence="Confirmed order-dependent on 3.11: passes alone, fails in the suite once cryptography submodules are imported "
             "(sys.modules['cryptography']=None does not block cached cryptography.* submodules).",
    add_notes=["tests/unit/test_authn.py:293-296"])
upd("FT-D13", "env-only resolved",
    evidence="Passes in the extended run with a `python` shim on PATH, which confirms the diagnosis. Root fix (sys.executable) "
             "still needed: CI images often ship only python3.")
upd("FT-D14", "env-only resolved",
    evidence="Passes in the extended run once pyshacl is installed, which confirms the diagnosis. Root fix (declare + lock, or "
             "importorskip) still needed.")
upd("FT-D15", "X-harness (governed_actions)",
    evidence="Fails identically on Python 3.11 with requirements.lock (fastapi 0.142.2, starlette 1.7.0): 'fastapi_middleware_astack not found in request scope'. The earlier 'unpinned FastAPI' diagnosis was wrong.",
    title="Governed-actions acceptance test builds TestClient on a bare APIRouter (fails under the pinned FastAPI too)",
    type="Test",
    description="Corrected diagnosis (extended run): test_cra_027_9 also fails under the LOCKED fastapi 0.142.2 / starlette 1.7.0 "
                "with 'fastapi_middleware_astack not found in request scope', so dependency drift is not the cause. "
                "tests/acceptance/test_governed_actions_acceptance.py:285 calls TestClient(router) on a bare APIRouter; current "
                "FastAPI needs the router mounted on a FastAPI app for its middleware stack. CRA-027.9 (canonical routes + OCA "
                "aliases) is therefore unverified. Secondary: pyproject.toml:12 still allows fastapi>=0.110,<1.0 while the "
                "lock pins 0.142.2.",
    preconditions=[],
    acceptance_criteria=["Test mounts the router: app = FastAPI(); app.include_router(router); TestClient(app)",
                         "test passes under requirements.lock AND under the latest version pyproject allows",
                         "pyproject upper bound narrowed to the tested minor, or a CI matrix job tests latest-allowed"],
    implementation_notes=["tests/acceptance/test_governed_actions_acceptance.py:285 (TestClient(router))",
                          "pyproject.toml:12 (fastapi>=0.110,<1.0)", "requirements.lock (fastapi 0.142.2, starlette 1.7.0)"],
    estimated_effort={"hours": 1, "band": "XS"})
for c in ("FT-D04", "FT-D05", "FT-D06", "FT-D09", "FT-D11", "FT-D12"):
    tasks[c]["parent"] = "FT-X10"

# ---------------- new tasks ----------------
new(id="FT-X03", epic="EPIC-EXT-DEPLOY", type="Bug", priority="P1",
    title="API runtime image crash-loops: numpy imported unconditionally but not installed in the runtime image",
    description="deploy/Dockerfile:5-6 installs only requirements.lock + requirements-fileparse.lock; numpy lives in the "
                "optional 'numerics' extra (pyproject.toml:29-33) and in no runtime lock. packages/eoip/processing/service.py:14 "
                "imports numpy at module level and apps/api/extended.py:1487 mounts the processing router at startup, so eoip-api "
                "dies with ModuleNotFoundError: numpy and compose reports 'dependency failed to start: eoip-api is unhealthy' "
                "(logs/compose_up3.log). A derived image with the numerics extras became healthy (diagnostic, not repo code).",
    preconditions=["Decide: numerics is a required runtime dependency, or processing routes are optional"],
    acceptance_criteria=["Either a requirements-numerics.lock (hash-pinned) is installed in the runtime stage, or numpy is "
                         "imported lazily and the processing router is mounted only when numerics is available (with a "
                         "truthful 'unavailable' capability state)",
                         "Fresh `docker compose -f deploy/docker-compose.yml up --build --wait` reaches healthy for eoip-api, "
                         "eoip-worker and eoip-mcp with no extra packages",
                         "CI job builds the runtime image and probes /health/ready (no test-stage deps)"],
    automated_tests=["new: container smoke in CI: build runtime target, run, GET /health/ready == 200",
                     "new: unit test importing apps.api.main.create_app in an env without numpy (if the lazy option is chosen)"],
    security_controls=["Lock file hash-pinned (pip --require-hashes)"],
    implementation_notes=["deploy/Dockerfile:5-6", "packages/eoip/processing/service.py:14 (import numpy as np)",
                          "apps/api/extended.py:1486-1487 (build_processing_router)", "pyproject.toml:29-33 (numerics extra)",
                          f"evidence: {EXT}/logs/compose_up3.log"],
    proof_plan={"required_for_closure": "L2 (container smoke) + L3 (CI image job)", "l4_candidate": "healthy compose stack on fix commit"},
    estimated_effort={"hours": 3, "band": "S"},
    extended_run={"defect": "X-03", "severity": "High", "source": f"{EXT}/defects.json"})
new(id="FT-X04", epic="EPIC-EXT-DEPLOY", type="Bug", priority="P1",
    title="Generated HugeGraph password (64 hex chars) exceeds Hubble's VARCHAR(48): hubble-init fails, so a fresh stack never starts",
    description="scripts/container.ps1:187-194 generates HUGEGRAPH_PASSWORD from 32 random bytes as 64 hex chars. "
                "scripts/setup_hubble.py:55-67 stores it in a Hubble connection; Hubble rejects it with 400 'Value too long for "
                "column PASSWORD VARCHAR(48)' (logs/compose_up2.log). eoip-api depends on hubble-init completing successfully "
                "(deploy/docker-compose.yml:109-111), so every first-run `container.ps1 up` fails. Worker C rated it Medium; raised "
                "to P1 here because it blocks the documented install path. Works with a 40-char password.",
    acceptance_criteria=["Generated password is ≤48 chars with ≥192 bits of entropy (e.g. 24 random bytes -> 48 hex, or base64url 32 chars)",
                         "setup_hubble.py validates the length up front with a clear error instead of a Hubble 400",
                         "Fresh `container.ps1 up` (and a bash equivalent) reaches healthy end to end",
                         "Existing deploy/.env files with 64-char passwords get a documented rotation path"],
    automated_tests=["new: unit test for the generator: length ≤48, charset, entropy",
                     "new: setup_hubble rejects >48-char password with a clear message"],
    security_controls=["Password stays random (CSPRNG); never logged"],
    implementation_notes=["scripts/container.ps1:187-194", "scripts/setup_hubble.py:55-67", "deploy/docker-compose.yml:109-111",
                          f"evidence: {EXT}/logs/compose_up2.log"],
    proof_plan={"required_for_closure": "L2 + L4 (fresh stack healthy)"},
    estimated_effort={"hours": 2, "band": "S"},
    extended_run={"defect": "X-04", "severity": "Medium", "source": f"{EXT}/defects.json"})
new(id="FT-SEC-HUBBLE", epic="EPIC-FIND-SECURITY", type="Security", priority="P2",
    title="'hubble-local-admin' action resets the HugeGraph admin account to admin/admin and writes it to deploy/.env",
    description="scripts/container.ps1:254-266 runs scripts.setup_hubble --rotate-local-admin, which sets the graph 'admin' "
                "user's password to the literal 'admin' (scripts/setup_hubble.py:20-34), then rewrites HUGEGRAPH_PASSWORD=admin in "
                "deploy/.env and recreates the stack. The result is a well-known default credential (CWE-1392/CWE-798) on the graph "
                "that holds all ingested data. Mitigations seen: ports bind to 127.0.0.1 (deploy/docker-compose.yml:85), the action "
                "is opt-in and prints a warning, and deploy/.env is gitignored. Residual risk: any local process or container on "
                "the backend network gets graph admin, and the state persists in volumes after the demo. Priority P2: loopback-only "
                "and opt-in, but it persists silently.",
    acceptance_criteria=["Action sets a random password (CSPRNG, ≤48 chars, see FT-X04) instead of 'admin', or requires an explicit "
                         "--i-understand-demo-credentials flag and refuses when any port binds beyond 127.0.0.1",
                         "Hubble UI login uses a separate generated credential that is shown once",
                         "A `hubble-local-admin --revert` path (or `up`) restores a random password; docs updated",
                         "No literal 'admin' password remains in setup_hubble.py (grep check in CI)"],
    automated_tests=["new: unit test: rotate_local_admin never sends user_password == 'admin'",
                     "new: container.ps1 lint/pester test: action refuses when EOIP_*_PORT binds 0.0.0.0"],
    security_controls=["No default credentials", "Credential never echoed to logs", "Loopback-only binding enforced"],
    implementation_notes=["scripts/container.ps1:254-266", "scripts/setup_hubble.py:20-34 (rotate_local_admin, literal admin/admin)",
                          "deploy/docker-compose.yml:85 (127.0.0.1 binding)", ".gitignore:54 (.env)"],
    proof_plan={"required_for_closure": "L2 + L3 + L5 (security reviewer ≠ implementer)"},
    estimated_effort={"hours": 3, "band": "S"},
    extended_run={"defect": "X-04 note", "source": f"{EXT}/defects.json"})
new(id="FT-X07", epic="EPIC-EXT-DEPLOY", type="Test", priority="P2",
    title="Locust load scenarios call non-existent routes and send no auth (TEST-002 load evidence impossible)",
    description="tests/load/locustfile.py:12,22,29 posts to /api/v1/query/multi_paradigm, /api/v1/routing/classify and "
                "/api/v1/token_formats/serialize with no Authorization header. 30 s / 5 users on localhost: 518/518 failed (401) "
                "as-is; 513/513 failed (404, some 401) with a bearer token. The real routes appear to be "
                "/api/v1/query/multi-paradigm (packages/eoip/enterprise/advanced_router.py:97), "
                "/routing/classify-and-route (packages/eoip/platform_router.py:1897) and /token-formats/serialize "
                "(platform_router.py:1855). Mount prefixes still need to be confirmed against /openapi.json. No NFR-PERF requirement "
                "can get load evidence until this is fixed.",
    acceptance_criteria=["Each scenario targets a route present in /openapi.json (asserted at locust on_start)",
                         "Bearer token read from an env var (EOIP_LOAD_TOKEN), never hard-coded; on_start fails fast if unset",
                         "A 30 s / 5-user run against the local stack has failure rate < 1% and reports p50/p95",
                         "k6 scenarios (if kept) get the same route + auth review"],
    automated_tests=["new: unit test parsing locustfile route constants and asserting each exists in create_app().openapi()"],
    security_controls=["Token from env/secret store only"],
    implementation_notes=["tests/load/locustfile.py:12,22,29", "packages/eoip/enterprise/advanced_router.py:97",
                          "packages/eoip/platform_router.py:1855,1897", f"evidence: {EXT}/load/ (locust CSVs)"],
    proof_plan={"required_for_closure": "L2 + L4 (load run on non-prod stack with CSV artifact)"},
    estimated_effort={"hours": 2, "band": "S"},
    extended_run={"defect": "X-07", "severity": "Medium", "source": f"{EXT}/defects.json"})
X10_ITEMS = [
    ("tests/unit/test_product_intelligence.py:133", "/api/v1/loops/catalog absent from deployed route surface", "FT-D04"),
    ("tests/unit/test_deployment_api.py:42", "expects OpenAPI scheme 'HTTPBearer'; app exposes 'SafeHTTPBearer'", "FT-D05"),
    ("tests/unit/test_kgr_export.py:37", "'pdf' export format missing from KGR export menu", "FT-D11"),
    ("tests/unit/test_enterprise_security_wp55.py:160", "'Enterprise Security & Token Governance' heading missing", "FT-D11"),
    ("tests/unit/test_suggested_advanced_capabilities.py:123", "bitemporal context slate missing 'tax_rate'", "FT-D12"),
    ("tests/unit/test_scale_and_polish_wp71.py:105", "docs/getting-started.md lacks 'Prerequisites' section", "FT-D11"),
    ("tests/unit/test_license_documents.py:16", "pyproject.toml:10 license is a table; test expects SPDX string", "FT-D09"),
    ("tests/unit/test_gap_coverage.py:82", "gap-coverage report returns blocking issue (GAP-STUDIO-005)", "FT-D06"),
    ("tests/unit/test_gap_coverage.py:95", "completion_gate('P0') not passed", "FT-D06"),
    ("tests/unit/test_gap_coverage.py:259", "CLI --fail-on-gate exits 1", "FT-D06"),
    ("tests/unit/test_gap_coverage.py:285", "gap-coverage API reports blocking issue", "FT-D06"),
]
new(id="FT-X10", epic="EPIC-DEFECTS", type="Governance", priority="P2",
    title="Code/test/doc drift: 11 failing tests, each needs a recorded decision (fix code vs update test + requirement)",
    description="Parent task for X-10. Each of the 11 tests asserts a feature or claim the code/docs no longer have. For every "
                "sub-item, an owner must decide which side is wrong and record it in the sub-item's 'decision' before the child "
                "task is worked. Child tasks hold the technical detail: FT-D04, FT-D05, FT-D06 (4 tests), FT-D09, FT-D11 (3 tests), "
                "FT-D12. All 11 still fail on Python 3.11 with locked deps, so they are not environment noise.",
    acceptance_criteria=["Every sub-item has decision ∈ {restore_code, update_test_and_requirement, remove_requirement} with "
                         "decider + date", "If a test is changed, the linked requirement text changes in the same PR",
                         "All 11 tests pass (or are deleted together with their requirement, with a changelog note)"],
    automated_tests=[i[0] for i in X10_ITEMS],
    implementation_notes=[f"{i[0]}: {i[1]} -> {i[2]}" for i in X10_ITEMS],
    sub_items=[{"test": i[0], "issue": i[1], "child_task": i[2], "decision": "PENDING", "decided_by": None} for i in X10_ITEMS],
    children=sorted({i[2] for i in X10_ITEMS}),
    proof_plan={"required_for_closure": "children closed + decisions recorded (L2 per child)"},
    estimated_effort={"hours": 1.5, "band": "S", "notes": "decision triage only; child effort counted on the children"},
    extended_run={"defect": "X-10", "severity": "Low-Medium", "source": f"{EXT}/defects.json"})
new(id="FT-X11", epic="EPIC-EXT-DEPLOY", type="Bug", priority="P3",
    title="DLQ acceptance writes results as uid 10001 into a host bind mount: PermissionError on Linux hosts",
    description="deploy/docker-compose.dlq-acceptance.yml:100 bind-mounts ../test-results to /results; the test image runs as "
                "uid 10001 (deploy/Dockerfile:22-23), so on Linux hosts where the dir is owned by the invoking user the junit "
                "and JSON report writes fail. Worked around in the copy with chmod 777 (not acceptable as a fix).",
    acceptance_criteria=["Results written to a named volume and copied out with `docker compose cp`, or the service runs with "
                         "user: \"${UID}:${GID}\", or an init step creates the dir with the right owner",
                         "`dlq-acceptance` flow writes its report on a fresh Linux host with no manual chmod"],
    automated_tests=["CI job (ubuntu runner) runs the DLQ acceptance flow and uploads /results as an artifact"],
    implementation_notes=["deploy/docker-compose.dlq-acceptance.yml:100", "deploy/Dockerfile:22-23 (uid 10001)"],
    proof_plan={"required_for_closure": "L3 (CI artifact present)"},
    estimated_effort={"hours": 1, "band": "XS"},
    extended_run={"defect": "X-11", "severity": "Low", "source": f"{EXT}/defects.json"})
new(id="FT-X12", epic="EPIC-EXT-DEPLOY", type="Reliability", priority="P3",
    title="dlq-graph healthcheck probes /versions, so schema-init can start before the graph API is ready",
    description="deploy/docker-compose.dlq-acceptance.yml:57 marks dlq-graph healthy when /versions answers; schema-init then hit "
                "400 on schema/vertexlabels in 2 of the cold starts (logs/dlq_acceptance2.log, dlq_acceptance3.log). Likely cause, "
                "NOT proven.",
    preconditions=["Discovery: confirm by repeated cold starts with a readiness probe on the graph's schema endpoint"],
    acceptance_criteria=["Healthcheck probes an endpoint that needs the graph backend ready (e.g. GET /graphs/hugegraph/schema) "
                         "or schema-init retries with bounded backoff on 400/503",
                         "10 consecutive cold starts with no schema-init failure (log attached)"],
    automated_tests=["scripted cold-start loop (10x) in CI or a documented manual receipt"],
    implementation_notes=["deploy/docker-compose.dlq-acceptance.yml:57", f"evidence: {EXT}/logs/dlq_acceptance2.log, dlq_acceptance3.log"],
    proof_plan={"required_for_closure": "L4 (10x cold-start receipt)"},
    estimated_effort={"hours": 1.5, "band": "S"},
    extended_run={"defect": "X-12", "severity": "Low", "source": f"{EXT}/defects.json"})
new(id="FT-H01", epic="EPIC-DEFECTS", type="Test", priority="P2",
    title="GUI workbench acceptance runs a list argv with shell=True: on POSIX it executes bare `npm`, so it always fails on Linux/CI",
    description="tests/gui/test_gui_workbench_acceptance.py:70-76 and :265-271 call subprocess.run(['npm','run','test:unit'], "
                "shell=True). On POSIX, shell=True with a list runs only argv[0] ('npm', which prints usage and exits 1); the "
                "rest become shell positional args. `npm run test:unit` itself passes 20/20 (web_unit.junit.xml). Previously "
                "listed as environment-only; the extended run shows it is a test defect. The CRA-030.2 and CRA-030.A gates can "
                "never pass on Linux.",
    acceptance_criteria=["subprocess.run(['npm','run','test:unit'], shell=(os.name == 'nt')) or shutil.which('npm') resolution",
                         "Both tests pass on Linux with node 22 (repo needs --experimental-strip-types; system node 20 rejects it)",
                         "Test skips with a clear reason when npm/node is missing, instead of failing"],
    automated_tests=["tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states",
                     "tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate"],
    implementation_notes=["tests/gui/test_gui_workbench_acceptance.py:70-76", "tests/gui/test_gui_workbench_acceptance.py:265-271",
                          "node >= 22 needed by apps/web test:unit (see extended_summary.json environment.node)"],
    tests_covered=["tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states",
                   "tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate"],
    estimated_effort={"hours": 0.5, "band": "XS"},
    extended_run={"defect": "test-harness", "source": f"{EXT}/defects.json"})
new(id="FT-K01", epic="EPIC-KIT", type="Chore", priority="P2", status="Done", owner="grok-bot-audit-kit",
    title="Audit kit: run_tests_and_map.py required Python ≥3.12 (backslash inside f-string expression)",
    description="audit-scripts/run_tests_and_map.py:79 used re.sub(r'\\[.*\\]$', ...) inside an f-string expression, which is a "
                "SyntaxError before Python 3.12; worker C had to run it with 3.13. Kit-only defect, no repo impact.",
    acceptance_criteria=["Every audit-scripts/*.py compiles on Python 3.11", "run_tests_and_map.py works on 3.11 in --reuse-junit "
                         "and live-run modes, parametrized ids still stripped"],
    automated_tests=["py_compile of all audit-scripts on CPython 3.11.17",
                     "--reuse-junit on audit-output/test_results_merged (4329 cases)",
                     "audit-scripts/selftest/selftest_run_tests_and_map.sh <python3.11> <python-with-pytest> (live --isolate + --reuse-junit, parametrized ids)"],
    implementation_notes=["audit-scripts/run_tests_and_map.py: regex hoisted to module constant _PARAM_SUFFIX_RE; case_key() "
                          "builds the name before the f-string"],
    proof_plan={"required_for_closure": "L2 (kit self-test)", "result": "PASS on CPython 3.11.17, 2026-10-19"},
    estimated_effort={"hours": 0.5, "band": "XS"},
    extended_run={"defect": "kit_issue", "source": f"{EXT}/defects.json"})

# env-only list: resolved ones move out; GUI ones are now FT-H01
d["env_only_failures"] = []
d["env_only_resolved"] = [
    {"test": "tests/semantic/test_shacl_differential.py::test_pyshacl_adapter_and_differential_oracle",
     "fix": "pyshacl installed (root cause tracked in FT-D14)"},
    {"test": "tests/reva/unit/pd/test_pd_suite.py::test_sandbox_runner_process",
     "fix": "python shim on PATH (root cause tracked in FT-D13)"},
    {"test": "tests/acceptance/test_developer_ecosystem_acceptance.py::test_cra_039_8_widoco_html_ontology_docs_and_route_serving",
     "fix": "py3.11 + full extras + EOIP_DATA_DIR set; residual test-isolation note: the test should use tmp_path rather than "
            "the /data default (packages/eoip/runtime.py:13-14)"},
]
d["reclassified"] = [{"tests": tasks["FT-H01"]["tests_covered"], "from": "env_only_failures", "to": "FT-H01",
                      "why": "extended run: shell=True + list argv runs bare npm on POSIX; npm test:unit itself passes"}]
order = {"FT-F": 0, "FT-D": 1, "FT-X": 2, "FT-H": 3, "FT-S": 4, "FT-K": 5}
d["tasks"] = sorted(tasks.values(), key=lambda t: (order.get(t["id"][:4], 9), t["id"]))
d["extended_run_applied"] = {"date": "2026-10-19", "source": f"{EXT}/defects.json",
                             "updated": ["FT-F03", "FT-D01", "FT-D03", "FT-F07", "FT-D07", "FT-D08", "FT-D10", "FT-D13", "FT-D14", "FT-D15"],
                             "new": ["FT-X03", "FT-X04", "FT-SEC-HUBBLE", "FT-X07", "FT-X10", "FT-X11", "FT-X12", "FT-H01", "FT-K01"]}
P.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
print(len(d["tasks"]), "tasks")
