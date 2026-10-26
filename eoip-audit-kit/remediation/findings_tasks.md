# Finding & defect tasks (hand-written)

Audited commit `3ed3acd50e47ab8867aa6885d202f9956358dc3a`. Source: findings_tasks.json. 34 tasks; 30 failing test node(s) covered by a task; 28 test cases fail in `test_results_merged/`; 0 environment-only failure(s) remain.

## FT-F01 [P0] Rotate committed RBAC tokens, make ASG loading fail closed, purge history

| Field | Value |
|---|---|
| ID | FT-F01 (finding F-01, epic EPIC-FIND-SECURITY) |
| Type | Security |
| Priority | P0 |
| Description | Five plaintext bearer tokens (root-superadmin cross-tenant, default-admin, data-steward, analyst, viewer) are committed in Logins_credentials.keys, hard-coded in frontend/src/screens/SignIn.tsx (superadmin pre-filled) and in memory/test_credentials.md, on a public repo (refs dev_local, conflict_161026_1710). The API loads the file from the repo root by default and checks it before JWT validation. Execute remediation/SECRET_ROTATION_AND_PURGE_PLAN.md. |
| API contracts | Authorization: Bearer <token> unchanged for clients. Old tokens → 401. Server refuses to start without configured principals (startup contract change). |
| Data model | ASG file entries change from '<plaintext> / roles / tenant / user' to 'sha256:<hex> / roles / tenant / user'; new env EOIP_ASG_FILE (required), EOIP_REVOKED_TOKEN_SHA256_FILE, EOIP_BOOTSTRAP_SUPERADMIN (opt-in), EOIP_ASG_ALLOW_PLAINTEXT (dev only). |
| Performance targets | Auth check stays O(n principals) constant-time; no measurable latency change (<0.1 ms per request). |
| Observability | Log ASG load summary (usernames/roles count only) and startup refusals; alert on 401 bursts for retired usernames. Add client_ip/user_agent to AuditEvent (follow-up). |
| Backward compatibility | Breaking for anyone using old tokens or relying on the repo-root default file: intended. Clients must re-clone after the history rewrite. |
| Preconditions | • Incident owner named; private advisory opened<br>• Deployment inventory (plan C2). UNKNOWN which instances are internet-reachable: discovery step C2<br>• Repo admin available for force-push and GitHub Support ticket |
| Acceptance criteria | • Every old token returns 401 on every probed endpoint in every environment<br>• No token value in tree or in any blob of a fresh mirror (0 occurrences)<br>• Logins_credentials.keys and memory/test_credentials.md absent from all history; ignored by .gitignore<br>• Server exits non-zero when EOIP_ASG_FILE is world/group-readable, contains plaintext outside dev, contains a revoked digest, or no principals exist<br>• SignIn.tsx contains no tokens; built bundle contains none<br>• Secret scanning + push protection + gitleaks pre-commit + CI job active<br>• Access-log review completed and signed |
| Automated tests | • tests/unit/test_asg_fail_closed.py (new): missing path, perms, plaintext, revoked, bootstrap opt-in, hashed authenticate<br>• tests/unit/test_no_committed_secrets.py (new): ASG-line regex + eoip_pat_ over git ls-files<br>• CI: .github/workflows/secret-scan.yml (gitleaks full history) |
| Security controls | • Tokens ≥256-bit from secrets.token_urlsafe, prefix eoip_pat_<br>• Stored only in secret store / k8s Secret / gitignored deploy/.env<br>• SHA-256 digests at rest, constant-time compare<br>• Revocation denylist by digest<br>• GitHub push protection + custom patterns<br>• Dual control: L5 reviewer ≠ implementer |
| Implementation notes (file:line) | • Logins_credentials.keys:69-73 (values never to be copied)<br>• apps/api/asg.py:93-137 load_asg (never raises, always adds bootstrap superadmin); :140-144 default_keys_path repo-root fallback<br>• apps/api/main.py:221-235 create_app → ASG checked before TokenValidator<br>• frontend/src/screens/SignIn.tsx:17,19-24,30<br>• memory/test_credentials.md:9-16<br>• Purge rehearsal: filter-repo --invert-paths + --replace-text on a mirror → 0 occurrences / 0 commits |
| Proof plan | **required_for_closure**: Critical: L2 + L3 (same commit) + L5 (reviewer ≠ agent); L4 revocation matrix strongly expected<br>**L1**: code links to fail-closed loader, SignIn.tsx, .gitignore<br>**L2**: local pytest of new tests + gitleaks on fresh clone<br>**L3**: secret-scan.yml green on fix commit<br>**L4**: 401 matrix per environment, startup-refusal logs<br>**L5**: independent security sign-off<br>**template**: remediation/evidence.secret-rotation.template.json |
| Estimated effort | 24 h (L) – 8h code+tests, 4h rotation across envs, 4h purge window + coordination, 4h log review, 4h review/sign-off; UNKNOWN env count may add time |

## FT-F02 [P0] Remove the hard-coded bootstrap token from backend/server.py; fail closed

| Field | Value |
|---|---|
| ID | FT-F02 (finding F-02, epic EPIC-FIND-SECURITY) |
| Type | Security |
| Priority | P0 |
| Description | backend/server.py:22 sets EOIP_API_TOKEN to a committed literal if unset; asg.py registers EOIP_API_TOKEN as superadmin unconditionally. The same literal is in memory/test_credentials.md:16 and test_reports/iteration_1..5.json. |
| API contracts | Startup contract: supervisor preview must inject EOIP_API_TOKEN, or run with EOIP_ENV=dev (ephemeral random token written to <data>/dev-token mode 600). |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Startup log line 'bootstrap superadmin: enabled/disabled' (no value). |
| Backward compatibility | Preview environments that relied on the default must now set the env var: document in backend/README.md. |
| Preconditions | • FT-F01 loader PR open (shared code) |
| Acceptance criteria | • No literal token in backend/server.py or any tracked file<br>• Importing backend.server without EOIP_API_TOKEN and EOIP_ENV≠dev exits non-zero<br>• EOIP_ENV=dev generates a per-process random token, never printed<br>• EOIP_LOAD_DEMO default false<br>• runtime.api_token rejects <32 chars and revoked digests |
| Automated tests | • tests/unit/test_backend_shim_fail_closed.py (new, subprocess import with clean env)<br>• extend tests/unit/test_runtime*.py for 32-char minimum + denylist (UNKNOWN existing file name: discovery `git grep -l api_token tests`) |
| Security controls | • No default credentials (CWE-798)<br>• Bootstrap superadmin opt-in via EOIP_BOOTSTRAP_SUPERADMIN=true |
| Implementation notes (file:line) | • backend/server.py:17-29<br>• packages/eoip/runtime.py:17-21<br>• apps/api/asg.py:113-136<br>• test_reports/iteration_1.json:23 (scrub or delete generated reports) |
| Proof plan | **required_for_closure**: High: L2 + (L3 same commit or L4)<br>**L2**: shim fail-closed test passes<br>**L3**: secret-scan.yml fail-closed-tests job green<br>**L4**: preview restart log showing refusal without token |
| Estimated effort | 4 h (S) |

## FT-F03 [P1] Isolate sandbox workers in their own process group before killpg

| Field | Value |
|---|---|
| ID | FT-F03 (finding F-03, epic EPIC-FIND-RELIABILITY) |
| Type | Reliability |
| Priority | P1 |
| Description | WorkerSupervisor spawns workers without start_new_session on POSIX; kill_process_tree() then SIGKILLs os.getpgid(child), i.e. the host's own group, killing the API/worker host and siblings. Reproduced: pytest killed with exit 137 twice by tests/security/test_worker_isolation.py::test_infinite_loop_timeout_killed_within_one_second. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | Kill latency ≤1 s from deadline (unchanged requirement). |
| Observability | Counter worker_kills_total{reason} already in stats(); add log with child pgid. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • Worker Popen uses start_new_session=True on POSIX<br>• kill_process_tree refuses to signal a pgid equal to os.getpgrp() (falls back to os.kill(pid))<br>• After a watchdog kill the parent process is alive and serving<br>• Infinite-loop worker killed ≤1 s after deadline (CRA-002.8)<br>• tests/security/test_worker_isolation.py passes in a normal pytest run (no exclusion needed)<br>• tests/security/test_worker_isolation.py::test_memory_balloon_terminated_safely passes<br>• Whole file runs in one pytest process (no setsid wrapper) with exit 0 |
| Automated tests | • tests/security/test_worker_isolation.py (existing) runs to completion<br>• new: test_watchdog_does_not_kill_parent: spawn timeout, assert os.getpid() alive and os.getpgid(child) != os.getpgrp()<br>• same check for reva/sandbox/runner.py (uses preexec on POSIX: verify) |
| Security controls | • Tenant workload cannot terminate the host (cross-tenant DoS) |
| Implementation notes (file:line) | • packages/eoip/workers/supervisor.py:77-94 kill_process_tree<br>• packages/eoip/workers/supervisor.py:185-198 Popen (creationflags only on win32)<br>• tests/security/test_worker_isolation.py:32-44<br>• packages/eoip/workers/supervisor.py:184-198 (POSIX Popen sets only creationflags; no start_new_session/process_group)<br>• packages/eoip/workers/supervisor.py:89-90 (os.killpg(os.getpgid(pid), SIGKILL))<br>• Fix shown by diagnostic: Popen(..., start_new_session=(sys.platform != 'win32')); diag helper in audit-output/test_results_extended/diag/ (not repo code) |
| Proof plan | **required_for_closure**: High: L2 + L3<br>**L2**: worker isolation tests pass locally without killing the runner<br>**L3**: ci.yml / validation-evidence green on fix commit incl. this file<br>**L4**: optional: kill a runaway job on a staging API and show the API stays healthy |
| Estimated effort | 2 h (S) – fix confirmed by diagnostic; mostly test + guard |
| Failing tests covered | `tests/security/test_worker_isolation.py::test_infinite_loop_timeout_killed_within_one_second`<br>`tests/security/test_worker_isolation.py::test_memory_balloon_terminated_safely` |
| Extended run (X-01) | Reproduced on Python 3.11 + locked deps: whole-file run of tests/security/test_worker_isolation.py exits 137 after ~1 s inside setsid with a 120 s outer timeout (the two watchdog tests SIGKILL their own pytest process group). Run per test in its own session: 4/6 pass, 2 fail. DIAGNOSTIC ONLY (not repo code, not proof): a plugin injecting start_new_session=True into the supervisor Popen gives 6/6 pass in 16.4 s, confirming the fix. |

## FT-F04 [P1] Make CI real: replace reva-* placeholders, run ci.yml on dev_local, fix validation-evidence

| Field | Value |
|---|---|
| ID | FT-F04 (finding F-04, epic EPIC-FIND-CI) |
| Type | DevOps |
| Priority | P1 |
| Description | 10 reva-*.yml jobs only echo; ci.yml triggers only main/develop; validation-evidence.yml (windows-latest, full pytest) failed on 3ed3acd at 'Run source-bound regression'. Root cause UNKNOWN (logs need auth): candidates are missing numerics extra (line 29/67), the deadlock in FT-D01 hanging the run, or FT-F03 on POSIX (not applicable on Windows). |
| API contracts | N/A |
| Data model | None changed. |
| Performance targets | PR CI wall-clock ≤20 min (UNKNOWN current baseline: discovery from run durations). |
| Observability | Upload junit + reportlog artifacts on every run (already partial: validation receipts). |
| Backward compatibility | No impact. |
| Preconditions | • Repo admin access to Actions logs (discovery: `gh run view 39298370898 --log-failed`) |
| Acceptance criteria | • Every reva-*.yml either runs the named suite (e.g. pytest tests/reva/unit) or is deleted<br>• ci.yml triggers on dev_local pushes and PRs to dev_local<br>• validation-evidence installs .[dev,codeparse,fileparse,numerics] (or uses requirements.lock) and is green<br>• Branch protection requires ci + validation-evidence + secret-scan on main and dev_local<br>• audit-config.json ci.l3_eligible_workflows updated to the real workflows |
| Automated tests | • CI itself: green runs on dev_local head<br>• actionlint in ci.yml lint job |
| Security controls | • permissions: contents: read on all workflows<br>• pin third-party actions by SHA |
| Implementation notes (file:line) | • .github/workflows/reva-unit.yml:13-14 (echo placeholder; same for the other 9)<br>• .github/workflows/ci.yml:3-7 triggers<br>• .github/workflows/validation-evidence.yml:14,29,42-49,67<br>• failed run https://github.com/Vibe-A-Thon/EIOP/actions/runs/39298370898 |
| Proof plan | **required_for_closure**: High: L2 + L3<br>**L2**: act/local run of each workflow command<br>**L3**: green runs on the fix commit for each workflow (links) |
| Estimated effort | 10 h (M) |

## FT-F05 [P1] Replace hand-written '100% Implemented & Verified' claims with evidence-derived status

| Field | Value |
|---|---|
| ID | FT-F05 (finding F-05, epic EPIC-FIND-GOVERNANCE) |
| Type | Governance |
| Priority | P1 |
| Description | EOIP-master-requirements.md:22,39-41 claims '1,661 Verified Items' and '100% Implemented & Verified'; requirements-registry.json audit_baseline says MISSED 1567 / IMPLEMENTED-UNVERIFIED 966 / IMPLEMENTED 137; this audit has 0 Implemented under policy 1.1. The repo's own P0 completion gate is red (FT-D06) and CRA-001 ledger references missing receipts (FT-D08). |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • FT-F04 (CI) for L3 evidence to exist |
| Acceptance criteria | • No status wording in any requirements .md that isn't generated from registry+evidence<br>• A script regenerates the status column from requirements-registry.json + audit-memory.json; CI fails on drift<br>• Master spec headline counts equal registry counts |
| Automated tests | • new tests/unit/test_requirements_status_not_hand_edited.py: compare doc status cells with generated output |
| Security controls | • N/A |
| Implementation notes (file:line) | • EOIP-master-requirements.md:22,39-41<br>• requirements-registry.json (audit_baseline block)<br>• eoip-audit-kit/audit-output/audit-memory.json (policy-1.1 statuses) |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: drift test passes locally<br>**L3**: drift test green in CI |
| Estimated effort | 6 h (M) |

## FT-F06 [P1] Make the documented install run the whole test suite (and pin dependencies)

| Field | Value |
|---|---|
| ID | FT-F06 (finding F-06, epic EPIC-FIND-BUILD) |
| Type | DevOps |
| Priority | P1 |
| Description | README.md:68 and docs/getting-started.md:57 install .[dev]; tests then fail to collect (numpy, defusedxml). pyproject ranges (e.g. fastapi>=0.110,<1.0 at pyproject.toml:12) let pip resolve versions newer than requirements.lock (fastapi 0.142.2), which broke a test (FT-D15). pyshacl is imported but declared nowhere (FT-D14). |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • One documented command installs everything the default test selection needs (e.g. .[test] or pip install -r requirements.lock + -e . --no-deps)<br>• Fresh venv + documented command → `pytest -m 'not integration and not slow and not performance'` collects with 0 errors<br>• Optional-dependency tests use pytest.importorskip<br>• README/getting-started updated |
| Automated tests | • CI job 'install-from-docs' that runs the README commands verbatim in a clean venv and collects tests |
| Security controls | • Use hash-pinned lock (requirements.lock already has hashes for neural lock: verify) |
| Implementation notes (file:line) | • README.md:68,107-112<br>• docs/getting-started.md:57<br>• pyproject.toml:12 (fastapi range), :29-84 extras<br>• requirements.lock:11,37 (fastapi/starlette pins) |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: clean-venv collect-only shows 0 errors<br>**L3**: install-from-docs CI job green |
| Estimated effort | 4 h (S) |

## FT-F07 [P1] Fix NameErrors: ConnectorError in GitHub connector, asdict in NLP pipeline

| Field | Value |
|---|---|
| ID | FT-F07 (finding F-07, epic EPIC-FIND-CORRECTNESS) |
| Type | Bug |
| Priority | P1 |
| Description | packages/eoip/connectors/github.py raises ConnectorError at 14 sites without importing it; every error path raises NameError (confirmed by failing test tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe, crash at github.py:294 via :195). packages/eoip/nlp/pipeline.py:405 uses asdict; line 12 imports only dataclass, field. |
| API contracts | Connector error contract: ConnectorError(source_system, category, correlation_id) (packages/eoip/connectors/errors.py:10). |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • `from eoip.connectors.errors import ConnectorError` in github.py<br>• `asdict` imported in pipeline.py<br>• ruff F821 = 0 for non-annotation names; F821 made blocking in CI<br>• failing test passes; a new test covers pipeline to_dict path at :405 |
| Automated tests | • tests/unit/test_github_connector.py (existing)<br>• new tests/unit/test_nlp_pipeline_serialization.py |
| Security controls | • Error categories stay safe (no token/URL leakage), as asserted by the existing test |
| Implementation notes (file:line) | • packages/eoip/connectors/github.py:16-21 imports; :195,:197,:206,:294 raise sites<br>• packages/eoip/connectors/errors.py:10<br>• packages/eoip/nlp/pipeline.py:12,405<br>• packages/eoip/connectors/github.py:16-21 (import block lacks ConnectorError)<br>• raise sites confirmed by the extended run: github.py:197,206,257,263,294 |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: the two tests pass<br>**L3**: CI green incl. ruff F821 gate |
| Estimated effort | 1.5 h (XS) |
| Failing tests covered | `tests/unit/test_github_connector.py::test_github_webhook_delete_and_error_categories_are_safe` |
| Extended run (X-06) | Confirmed on 3.11: test_github_webhook_delete_and_error_categories_are_safe fails with NameError ConnectorError. |

## FT-F08 [P2] Parameterise or remove f-string SQL/AQL translation in UniversalDatabaseAdapter

| Field | Value |
|---|---|
| ID | FT-F08 (finding F-08, epic EPIC-FIND-SECURITY) |
| Type | Security |
| Priority | P2 |
| Description | _cypher_to_sql/_cypher_to_aql build queries with f-strings (bandit B608 ×11). Code reading (2026-10-19) lowers the risk: identifiers are \w+ and the value regex [^'"}\s]+ forbids quotes and whitespace, so quote break-out looks blocked; UniversalDatabaseAdapter has no callers outside its own module (dead code?). Still unsafe by construction. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Discovery: confirm no runtime path constructs UniversalDatabaseAdapter (`git grep -n UniversalDatabaseAdapter`, plugin registry, config) |
| Acceptance criteria | • Either the adapter is deleted, or values are passed as bound parameters and identifiers are allow-listed<br>• bandit B608 = 0 in packages/eoip/graph/database_adapters.py<br>• Injection tests with payloads like `1 OR 1=1`, `x'--`, unicode quotes all treated as literal values |
| Automated tests | • new tests/security/test_database_adapter_injection.py |
| Security controls | • Parameter binding (CWE-89)<br>• Identifier allow-list |
| Implementation notes (file:line) | • packages/eoip/graph/database_adapters.py:247-262 (_cypher_to_aql), :264-274 (_cypher_to_sql), :334,:339 call sites |
| Proof plan | **required_for_closure**: L2 + L3 (Medium)<br>**L2**: injection tests pass; bandit clean<br>**L3**: CI green |
| Estimated effort | 3 h (S) |

## FT-F09 [P2] Make requirement IDs unique and traceable

| Field | Value |
|---|---|
| ID | FT-F09 (finding F-09, epic EPIC-FIND-GOVERNANCE) |
| Type | Governance |
| Priority | P2 |
| Description | 629 IDs are defined at more than one site (1297 extra sites: 884 cross-doc, 413 same-doc). Sub-clause numbering such as CRA-001.1 (1193 sites) is not a duplicate. Generic prefixes (AC-, INT-) collide; 1933 IDs have no code/test/infra reference; 146 test-referenced IDs exist in no doc. See remediation/duplicate_id_tasks.json (one task per duplicate ID) and orphan_test_ids.json. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Owner decision on canonical registry (requirements-registry.json is the obvious candidate) |
| Acceptance criteria | • Every ID defined exactly once (other sites reference it)<br>• Generic per-doc IDs namespaced (e.g. GUI-INT-001, KGR-AC-01)<br>• CI check fails on duplicates and on P0 IDs without a mapped test |
| Automated tests | • new scripts/check_requirement_ids.py + CI step |
| Security controls | • N/A |
| Implementation notes (file:line) | • remediation/duplicate_id_tasks.json (generated)<br>• eoip-audit-kit/audit-output/requirements_index.json duplicate_definitions field<br>• requirements-test-map.json (1330 mappings)<br>• remediation/orphan_test_ids.json (146 IDs) |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: checker passes locally<br>**L3**: checker green in CI |
| Estimated effort | 16 h (L) – mostly doc edits; 629 duplicate tasks at ~0.5-1.5 h each are tracked separately as DUP-* |

## FT-F10 [P2] Stop committing runtime data and scratch output; classify existing data

| Field | Value |
|---|---|
| ID | FT-F10 (finding F-10, epic EPIC-FIND-HYGIENE) |
| Type | Governance |
| Priority | P2 |
| Description | .eoip-data (339 files, ~8 MB ingest output incl. audit.jsonl), .tmp (109) and .audit-scratch (187, ignored by .gitignore:29 but tracked) are committed. Classification of the data (synthetic vs real) is UNKNOWN. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Discovery: data owner confirms whether .eoip-data/raw/{git,jira,documents} is synthetic |
| Acceptance criteria | • Data classified and recorded<br>• `git rm -r --cached .eoip-data .tmp .audit-scratch` (keep needed fixtures under tests/fixtures)<br>• .gitignore covers /.eoip-data/ and /.tmp/<br>• If any real data: include in the FT-F01 purge window (filter-repo --path) |
| Automated tests | • tests/unit/test_no_runtime_data_tracked.py: git ls-files has no paths under .eoip-data/.tmp/.audit-scratch |
| Security controls | • Data minimisation; PII review if non-synthetic |
| Implementation notes (file:line) | • .gitignore:29<br>• tests that read .audit-scratch (e.g. tests/acceptance/test_cra_001_acceptance.py:110-122) must move to fixtures: see FT-D08 |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: guard test passes<br>**L3**: CI green |
| Estimated effort | 4 h (S) |

## FT-F11 [P3] Lint ratchet, non-security hashes, and no tests in the runtime image

| Field | Value |
|---|---|
| ID | FT-F11 (finding F-11, epic EPIC-FIND-HYGIENE) |
| Type | Chore |
| Priority | P3 |
| Description | ruff 4290 issues (UP006 914, F401 780, UP045 690, UP035 426); bandit HIGH: 7× B324 (MD5/SHA1) and 1× B202 likely false positive; deploy/Dockerfile:29 copies tests/ into the image. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • ruff --fix for UP*/F401 applied; CI fails on new violations (ratchet)<br>• B324 sites pass usedforsecurity=False or switch to sha256<br>• B202 site annotated with justification (# nosec B202 + reason)<br>• Runtime image has no tests/ directory |
| Automated tests | • ruff check in CI<br>• container test: `docker run --rm img test ! -d /app/tests` |
| Security controls | • Smaller attack surface in image |
| Implementation notes (file:line) | • packages/eoip/ci/pipeline.py:209; embeddings/engine.py:229; graph/partitioning.py:253; model_management/registry.py:459; models/self_llm.py:338; retrieval/vectors.py:99; truth/engine.py:22 (B324)<br>• packages/eoip/fileparse/archives.py:177 (B202)<br>• deploy/Dockerfile:29 |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: ruff/bandit clean locally<br>**L3**: CI lint job green |
| Estimated effort | 5 h (S) |

## FT-D01 [P1] Deadlock: ExecutionTracker.stats() re-acquires a non-reentrant lock

| Field | Value |
|---|---|
| ID | FT-D01 (finding F-06, epic EPIC-DEFECTS) |
| Type | Bug |
| Priority | P1 |
| Description | ExecutionTracker.stats() holds self._lock (threading.Lock, engine.py:598) and calls self.success_rate(), which acquires self._lock again (engine.py:627) → permanent hang. Reached from IntelligenceEngine.stats() (engine.py:752-757) and Brain OS kernel (brain/brain_os.py:576). Three tests hit the 30 s timeout. Likely also behind the xdist hang seen in the audit and a possible cause of the CI failure (FT-F04). |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | stats() < 5 ms for 10k records. |
| Observability | None. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • stats() computes success_rate without re-locking (inline under the lock, or _success_rate_unlocked helper), or the lock becomes RLock<br>• The 3 tests finish in <1 s each<br>• Static check: no method calls another lock-taking method while holding the same Lock in intelligence_eng/engine.py (same pattern at :674, :814, :987, :1144 reviewed) |
| Automated tests | • tests/unit/test_engineering_disciplines.py::TestIntelligenceEngineering::test_stats<br>• tests/unit/test_brain_and_living_system.py::test_brain_os_kernel<br>• tests/unit/test_cognitive_narrator.py::test_brain_kernel_cognitive_narrator_integration<br>• new: test_execution_tracker_stats_no_deadlock (thread + join(timeout=2)) |
| Security controls | • Availability: any caller of /stats-style endpoints could hang worker threads |
| Implementation notes (file:line) | • packages/eoip/intelligence_eng/engine.py:594-598 (Lock), :626-631 success_rate, :646-653 stats<br>• packages/eoip/brain/brain_os.py:576<br>• packages/eoip/intelligence_eng/engine.py:598 (threading.Lock), call chain :646 -> :652 -> :627 |
| Proof plan | **required_for_closure**: L2 + L3<br>**L2**: 3 tests + new deadlock test pass<br>**L3**: CI green |
| Estimated effort | 1 h (XS) |
| Failing tests covered | `tests/unit/test_engineering_disciplines.py::TestIntelligenceEngineering::test_stats`<br>`tests/unit/test_brain_and_living_system.py::test_brain_os_kernel`<br>`tests/unit/test_cognitive_narrator.py::test_brain_kernel_cognitive_narrator_integration` |
| Extended run (X-02) | Confirmed on Python 3.11 + locked deps: the 3 tests hang until pytest-timeout (120 s and 300 s); the stack ends in engine.py:627 (success_rate acquiring self._lock held by stats()). |

## FT-D03 [P2] ServiceNow connector: cmdb_ci added to mandatory default tables breaks sync and fixtures

| Field | Value |
|---|---|
| ID | FT-D03 (finding n/a, epic EPIC-DEFECTS) |
| Type | Bug |
| Priority | P2 |
| Description | Commit 06319d7 (2026-10-18) added 'cmdb_ci' to DEFAULT_TABLES (servicenow.py:19). sync() iterates all tables (servicenow.py:81) and any 4xx/5xx raises ConnectorError (rest.py:100-118), so instances/fixtures without cmdb_ci abort the whole sync. FR-SNOW-001 (03-functional-requirements.md:91-94) scopes incident/problem/change/KB only. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • Product decision: is CMDB in scope for FR-SNOW-001? (UNKNOWN → discovery with requirement owner) |
| Acceptance criteria | • Either cmdb_ci is opt-in (not in DEFAULT_TABLES) or fixtures + spec updated to include it<br>• A missing/forbidden optional table yields a per-table warning, not a failed sync<br>• 3 failing tests pass<br>• Live DLQ acceptance: both ServiceNow tests pass (deploy/docker-compose.dlq-acceptance.yml) |
| Automated tests | • tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records<br>• tests/unit/test_servicenow_upstream_fixture.py::test_fixture_paginates_and_filters_incremental_queries<br>• tests/unit/test_servicenow_upstream_fixture.py::test_fixture_returns_genuine_mapping_rejection<br>• tests/runtime_dlq/test_servicenow_acquisition.py::test_servicenow_http_baseline_incremental_and_replay (live)<br>• tests/runtime_dlq/test_servicenow_rejection.py::test_servicenow_fetched_rejection_and_admission_controls (live) |
| Security controls | • Least privilege: do not require CMDB read scope by default |
| Implementation notes (file:line) | • packages/eoip/connectors/servicenow.py:19,49,81-90,123<br>• packages/eoip/connectors/rest.py:100-118<br>• tests/unit/test_phase2_connectors.py:146-152<br>• packages/eoip/connectors/servicenow.py:14-19 (DEFAULT_TABLES), :81 (sync iterates every table)<br>• packages/eoip/connectors/rest.py:118 (non-2xx raises ConnectorError and aborts the sync) |
| Proof plan | **required_for_closure**: L2 (unit + live DLQ) + L3<br>**l4_candidate**: live DLQ acceptance receipt on the fix commit |
| Estimated effort | 2 h (S) |
| Failing tests covered | `tests/unit/test_phase2_connectors.py::test_servicenow_sync_paginates_supported_tables_and_maps_records`<br>`tests/unit/test_servicenow_upstream_fixture.py::test_fixture_paginates_and_filters_incremental_queries`<br>`tests/unit/test_servicenow_upstream_fixture.py::test_fixture_returns_genuine_mapping_rejection`<br>`tests/runtime_dlq/test_servicenow_acquisition.py::test_servicenow_http_baseline_incremental_and_replay`<br>`tests/runtime_dlq/test_servicenow_rejection.py::test_servicenow_fetched_rejection_and_admission_controls` |
| Extended run (X-05) | Confirmed in-process on 3.11 and LIVE: the repo's DLQ acceptance flow (deploy/docker-compose.dlq-acceptance.yml, isolated graph + fixture upstreams) fails both ServiceNow tests (job FAILED); the other 14 live DLQ tests pass. |

## FT-D04 [P2] Product capability catalog advertises /api/v1/loops/catalog but the route is not mounted

| Field | Value |
|---|---|
| ID | FT-D04 (finding n/a, epic EPIC-DEFECTS) |
| Type | Bug |
| Priority | P2 |
| Description | packages/eoip/product/intelligence.py:73 lists '/api/v1/loops/catalog' as a deployed public entrypoint; create_app() does not register it (tests/unit/test_product_intelligence.py:128-133). |
| API contracts | GET /api/v1/loops/catalog → 200 JSON catalog (auth: analyst+); UNKNOWN schema: derive from the loops module. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Discovery: find the intended router (`git grep -n "loops" apps/api packages/eoip/loops*`) |
| Acceptance criteria | • Route registered and authenticated, or removed from the catalog<br>• test passes<br>• OpenAPI lists the route |
| Automated tests | • tests/unit/test_product_intelligence.py::test_deployed_route_surface_contains_product_gate_routes |
| Security controls | • Same auth dependency as sibling /api/v1 routes |
| Implementation notes (file:line) | • packages/eoip/product/intelligence.py:73<br>• apps/api/main.py (router registration; exact line UNKNOWN) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 2 h (S) |
| Failing tests covered | `tests/unit/test_product_intelligence.py::test_deployed_route_surface_contains_product_gate_routes` |
| Parent | FT-X10 |

## FT-D05 [P3] OpenAPI security scheme renamed HTTPBearer → SafeHTTPBearer

| Field | Value |
|---|---|
| ID | FT-D05 (finding n/a, epic EPIC-DEFECTS) |
| Type | Bug |
| Priority | P3 |
| Description | create_app() subclasses HTTPBearer as SafeHTTPBearer (main.py:258-262); FastAPI uses the class name as the scheme key, changing components.securitySchemes and breaking generated clients/tests. |
| API contracts | components.securitySchemes key must stay 'HTTPBearer' (or a documented stable name). |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | Restores compatibility for generated clients. |
| Preconditions | • None |
| Acceptance criteria | • Instantiate with scheme_name='HTTPBearer'<br>• test passes<br>• No other OpenAPI diffs (snapshot) |
| Automated tests | • tests/unit/test_deployment_api.py::test_admin_and_read_routes_require_token_and_jobs_are_durable<br>• new OpenAPI snapshot test |
| Security controls | • Unchanged |
| Implementation notes (file:line) | • apps/api/main.py:258-262<br>• tests/unit/test_deployment_api.py:42 |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 0.5 h (XS) |
| Failing tests covered | `tests/unit/test_deployment_api.py::test_admin_and_read_routes_require_token_and_jobs_are_durable` |
| Parent | FT-X10 |

## FT-D06 [P2] Repo's own P0 completion gate is red: GAP-STUDIO-005 lacks implementation trace

| Field | Value |
|---|---|
| ID | FT-D06 (finding F-05, epic EPIC-DEFECTS) |
| Type | Governance |
| Priority | P2 |
| Description | build_gap_coverage_report().completion_gate('P0') returns passed=False, blocked_total=1: GAP-STUDIO-005 (SKOS taxonomy, gaps-requirements.md:607) has test_refs (tests/unit/test_skos_taxonomy.py) but no implementation_refs, although packages/eoip/ontology/skos.py implements SKOS and is imported by that test. Four gap_coverage tests assert the gate passes. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • skos.py carries the GAP-STUDIO-005 trace marker the coverage scanner recognises (format UNKNOWN: discovery in packages/eoip/gaps/coverage.py)<br>• completion_gate(P0).passed is True<br>• 4 tests pass |
| Automated tests | • tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence<br>• tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues<br>• tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0<br>• tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report |
| Security controls | • N/A |
| Implementation notes (file:line) | • packages/eoip/ontology/skos.py<br>• EOIP-engg-doc-pkg/gaps-requirements.md:607<br>• packages/eoip/gaps/coverage.py (scanner)<br>• tests/unit/test_gap_coverage.py:74-96,259,285 |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 1 h (XS) |
| Failing tests covered | `tests/unit/test_gap_coverage.py::test_gap_coverage_report_distinguishes_code_and_test_evidence`<br>`tests/unit/test_gap_coverage.py::test_gap_completion_gate_reports_blocking_acceptance_issues`<br>`tests/unit/test_gap_coverage.py::test_gap_coverage_cli_writes_json_and_can_fail_planned_p0`<br>`tests/unit/test_gap_coverage.py::test_gap_coverage_api_exposes_filtered_report` |
| Parent | FT-X10 |

## FT-D07 [P3] cp_registry baseline digest is stale vs gaps-audit-cp.md

| Field | Value |
|---|---|
| ID | FT-D07 (finding F-05, epic EPIC-DEFECTS) |
| Type | Governance |
| Priority | P3 |
| Description | load_audit() pins AUDIT_SHA256/AUDIT_COUNT (cp_registry.py:14-17) and raises when gaps-audit-cp.md changes (:81-83). The file was edited without reconciling the baseline. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Owner decides whether the doc edit is intended |
| Acceptance criteria | • Baseline reconciled through the documented process (new digest + count committed with a reason) or doc reverted<br>• test passes<br>• Reconciliation recorded with reason + old/new digest and AUDIT_COUNT in the commit message or a baseline log |
| Automated tests | • tests/unit/test_cp_registry.py::test_real_registry_roundtrip_is_bounded_and_independent_of_git_history |
| Security controls | • Integrity gate kept (do not remove the check) |
| Implementation notes (file:line) | • packages/eoip/verification/cp_registry.py:14-17,78-83<br>• gaps-audit-cp.md<br>• packages/eoip/verification/cp_registry.py:16 (AUDIT_SHA256 pin), :83-84 (digest compare + raise) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 1 h (XS) |
| Failing tests covered | `tests/unit/test_cp_registry.py::test_real_registry_roundtrip_is_bounded_and_independent_of_git_history` |
| Extended run (X-08) | Confirmed on 3.11 (X-08 = this task; no new task). Test fails with 'Audit digest changed; explicitly reconcile the baseline before importing'. |

## FT-D08 [P2] CRA-001 ledger marks items ACCEPTED with receipts that are not in the repo

| Field | Value |
|---|---|
| ID | FT-D08 (finding F-05, epic EPIC-DEFECTS) |
| Type | Governance |
| Priority | P2 |
| Description | tests/acceptance/test_cra_001_acceptance.py:110-122 requires every ACCEPTED ledger item's receipt to exist with matching sha256; .audit-scratch/ledger.json (tracked) references .audit-scratch/receipts/CRA-001.1/run-20261018T080214Z-86eedb6d.json which is not tracked (.audit-scratch is gitignored, .gitignore:29). Acceptance claims are unverifiable from the repo. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Discovery: locate the missing receipts (developer machine / CI artifacts) |
| Acceptance criteria | • Receipts stored in a tracked, non-ignored evidence location (or CI artifact with URL + sha256 in the ledger)<br>• Items without a retrievable receipt revert from ACCEPTED<br>• test passes |
| Automated tests | • tests/acceptance/test_cra_001_acceptance.py::test_cra_001_9_ledger_and_receipts_storage_contract |
| Security controls | • Evidence integrity via sha256 |
| Implementation notes (file:line) | • .audit-scratch/ledger.json<br>• .gitignore:29<br>• tests/acceptance/test_cra_001_acceptance.py:110-122<br>• tests/acceptance/test_cra_001_acceptance.py:122 (receipt existence + sha256 assertion) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 2 h (S) |
| Failing tests covered | `tests/acceptance/test_cra_001_acceptance.py::test_cra_001_9_ledger_and_receipts_storage_contract` |
| Extended run (X-09) | Covered by this task (X-09 = FT-D08; no new task). Confirmed on 3.11: the receipt .audit-scratch/receipts/CRA-001.1/run-20261018T080214Z-86eedb6d.json referenced by the tracked ledger is not in the repo, so test_cra_001_9 fails. |

## FT-D09 [P3] pyproject license must be an SPDX string (PEP 639), not a table

| Field | Value |
|---|---|
| ID | FT-D09 (finding n/a, epic EPIC-DEFECTS) |
| Type | Chore |
| Priority | P3 |
| Description | pyproject.toml:10 has license = { text = ... }; tests/unit/test_license_documents.py:16 expects the PEP 639 string form; setuptools ≥77 deprecates the table form. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • build-system requires setuptools>=77 (pyproject.toml:2 currently >=65) |
| Acceptance criteria | • license = "LicenseRef-EOIP-Proprietary"; license-files kept<br>• build succeeds; test passes |
| Automated tests | • tests/unit/test_license_documents.py::test_python_license_metadata_includes_every_policy_document<br>• python -m build smoke |
| Security controls | • N/A |
| Implementation notes (file:line) | • pyproject.toml:2,10,85 |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 0.5 h (XS) |
| Failing tests covered | `tests/unit/test_license_documents.py::test_python_license_metadata_includes_every_policy_document` |
| Parent | FT-X10 |

## FT-D10 [P2] Security test for the 'cryptography not deployed' path is order-dependent

| Field | Value |
|---|---|
| ID | FT-D10 (finding n/a, epic EPIC-DEFECTS) |
| Type | Test |
| Priority | P2 |
| Description | test_cryptography_verifier_not_available_path sets sys.modules['cryptography']=None, but submodules (cryptography.hazmat...) already cached by earlier tests still import, so CryptographyVerifier does not raise. GAP-SEC-002's NotAvailable path is therefore not actually verified in a full run. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • Test blocks all cryptography.* entries (monkeypatch every key starting with 'cryptography') or injects an importer that raises<br>• Passes alone and in the full suite (pytest -p no:randomly and with random order) |
| Automated tests | • tests/unit/test_authn.py::TestOidcJwtValidator::test_cryptography_verifier_not_available_path |
| Security controls | • Verifies fail-closed auth when crypto backend is missing |
| Implementation notes (file:line) | • tests/unit/test_authn.py:292-297<br>• packages/eoip/authn/__init__.py:410-424<br>• tests/unit/test_authn.py:293-296 |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 0.5 h (XS) |
| Failing tests covered | `tests/unit/test_authn.py::TestOidcJwtValidator::test_cryptography_verifier_not_available_path` |
| Extended run (X-harness (test_authn)) | Confirmed order-dependent on 3.11: passes alone, fails in the suite once cryptography submodules are imported (sys.modules['cryptography']=None does not block cached cryptography.* submodules). |

## FT-D11 [P3] UI/doc drift: tests expect content that was removed (export PDF, security dashboard title, Prerequisites)

| Field | Value |
|---|---|
| ID | FT-D11 (finding n/a, epic EPIC-DEFECTS) |
| Type | Bug |
| Priority | P3 |
| Description | Three tests assert artefact content that no longer exists: 'pdf' in apps/web/src/kgr/components/ExportMenu.jsx; 'Enterprise Security & Token Governance' in apps/web/src/admin/SecurityGovernanceDashboard.jsx; 'Prerequisites' heading in docs/getting-started.md (last changed a52d962, 2026-10-19). Which side is correct is UNKNOWN. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Discovery per item: `git log -S'pdf' -- apps/web/src/kgr/components/ExportMenu.jsx` etc. to see whether removal was intentional |
| Acceptance criteria | • For each: restore the feature/text, or update the test and the linked requirement (KGR export formats; GAP-SEC-012; S-04) in the same PR<br>• 3 tests pass |
| Automated tests | • tests/unit/test_kgr_export.py::test_export_menu_has_7_formats<br>• tests/unit/test_enterprise_security_wp55.py::test_gap_sec_012_security_rest_api_and_dashboard<br>• tests/unit/test_scale_and_polish_wp71.py::test_s_04_developer_documentation |
| Security controls | • N/A |
| Implementation notes (file:line) | • tests/unit/test_kgr_export.py:30-37<br>• tests/unit/test_enterprise_security_wp55.py:155-160<br>• tests/unit/test_scale_and_polish_wp71.py:100-105 |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 2 h (S) |
| Failing tests covered | `tests/unit/test_kgr_export.py::test_export_menu_has_7_formats`<br>`tests/unit/test_enterprise_security_wp55.py::test_gap_sec_012_security_rest_api_and_dashboard`<br>`tests/unit/test_scale_and_polish_wp71.py::test_s_04_developer_documentation` |
| Parent | FT-X10 |

## FT-D12 [P3] Bitemporal context slate misses modified keys

| Field | Value |
|---|---|
| ID | FT-D12 (finding n/a, epic EPIC-DEFECTS) |
| Type | Bug |
| Priority | P3 |
| Description | test_feature_4_bitemporal_context_slate expects tax_rate in modified_keys between t_past and t_now; result is []. Root cause UNKNOWN: either as-of boundary semantics (t_past is taken before the first record) or global singleton state shared across tests (get_state_engine()). |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Discovery: run the test alone vs in-file; read build_slate boundary handling |
| Acceptance criteria | • Documented as-of semantics (inclusive/exclusive) in the bitemporal module<br>• Test isolated from singleton state (fresh engine fixture)<br>• Test passes alone and in suite |
| Automated tests | • tests/unit/test_suggested_advanced_capabilities.py::test_feature_4_bitemporal_context_slate |
| Security controls | • N/A |
| Implementation notes (file:line) | • tests/unit/test_suggested_advanced_capabilities.py:111-124<br>• bitemporal slate implementation (path UNKNOWN: `git grep -n get_bitemporal_context_slate packages`) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 2 h (S) |
| Failing tests covered | `tests/unit/test_suggested_advanced_capabilities.py::test_feature_4_bitemporal_context_slate` |
| Parent | FT-X10 |

## FT-D13 [P3] REVA sandbox test assumes a 'python' executable on PATH

| Field | Value |
|---|---|
| ID | FT-D13 (finding n/a, epic EPIC-DEFECTS) |
| Type | Test |
| Priority | P3 |
| Description | tests/reva/unit/pd/test_pd_suite.py:136 passes argv ['python', ...] to reva/sandbox/runner.py:135 Popen; fails where only python3 exists. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • None |
| Acceptance criteria | • Test uses sys.executable<br>• Runner documents that argv[0] must be absolute or resolvable<br>• test passes on Linux CI |
| Automated tests | • tests/reva/unit/pd/test_pd_suite.py::test_sandbox_runner_process |
| Security controls | • Prefer absolute interpreter paths in sandboxes (PATH hijack) |
| Implementation notes (file:line) | • tests/reva/unit/pd/test_pd_suite.py:136<br>• reva/sandbox/runner.py:128-137 |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 0.5 h (XS) |
| Failing tests covered | `tests/reva/unit/pd/test_pd_suite.py::test_sandbox_runner_process` |
| Extended run (env-only resolved) | Passes in the extended run with a `python` shim on PATH, which confirms the diagnosis. Root fix (sys.executable) still needed: CI images often ship only python3. |

## FT-D14 [P3] pyshacl imported but not declared in any extra or lock

| Field | Value |
|---|---|
| ID | FT-D14 (finding F-06, epic EPIC-DEFECTS) |
| Type | Chore |
| Priority | P3 |
| Description | packages/eoip/ontology/shacl_validator.py:788 imports pyshacl; it is absent from pyproject.toml and all *.lock files, so the differential-oracle test fails with ModuleNotFoundError. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • Licence check for pyshacl (Apache-2.0) vs project policy |
| Acceptance criteria | • pyshacl declared in a 'semantic' (or existing) extra and locked, or the test importorskips it<br>• test passes or is skipped with reason |
| Automated tests | • tests/semantic/test_shacl_differential.py::test_pyshacl_adapter_and_differential_oracle |
| Security controls | • Hash-pinned lock entry |
| Implementation notes (file:line) | • packages/eoip/ontology/shacl_validator.py:788,827-828<br>• pyproject.toml optional-dependencies (:29-84) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 0.5 h (XS) |
| Failing tests covered | `tests/semantic/test_shacl_differential.py::test_pyshacl_adapter_and_differential_oracle` |
| Extended run (env-only resolved) | Passes in the extended run once pyshacl is installed, which confirms the diagnosis. Root fix (declare + lock, or importorskip) still needed. |

## FT-D15 [P2] Governed-actions acceptance test builds TestClient on a bare APIRouter (fails under the pinned FastAPI too)

| Field | Value |
|---|---|
| ID | FT-D15 (finding F-06, epic EPIC-DEFECTS) |
| Type | Test |
| Priority | P2 |
| Description | Corrected diagnosis (extended run): test_cra_027_9 also fails under the LOCKED fastapi 0.142.2 / starlette 1.7.0 with 'fastapi_middleware_astack not found in request scope', so dependency drift is not the cause. tests/acceptance/test_governed_actions_acceptance.py:285 calls TestClient(router) on a bare APIRouter; current FastAPI needs the router mounted on a FastAPI app for its middleware stack. CRA-027.9 (canonical routes + OCA aliases) is therefore unverified. Secondary: pyproject.toml:12 still allows fastapi>=0.110,<1.0 while the lock pins 0.142.2. |
| API contracts | None changed. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | No change required. |
| Backward compatibility | No impact. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Test mounts the router: app = FastAPI(); app.include_router(router); TestClient(app)<br>• test passes under requirements.lock AND under the latest version pyproject allows<br>• pyproject upper bound narrowed to the tested minor, or a CI matrix job tests latest-allowed |
| Automated tests | • tests/acceptance/test_governed_actions_acceptance.py::test_cra_027_9_canonical_routes_and_oca_aliases |
| Security controls | • Dependency pinning |
| Implementation notes (file:line) | • tests/acceptance/test_governed_actions_acceptance.py:285 (TestClient(router))<br>• pyproject.toml:12 (fastapi>=0.110,<1.0)<br>• requirements.lock (fastapi 0.142.2, starlette 1.7.0) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 1 h (XS) |
| Failing tests covered | `tests/acceptance/test_governed_actions_acceptance.py::test_cra_027_9_canonical_routes_and_oca_aliases` |
| Extended run (X-harness (governed_actions)) | Fails identically on Python 3.11 with requirements.lock (fastapi 0.142.2, starlette 1.7.0): 'fastapi_middleware_astack not found in request scope'. The earlier 'unpinned FastAPI' diagnosis was wrong. |

## FT-X03 [P1] API runtime image crash-loops: numpy imported unconditionally but not installed in the runtime image

| Field | Value |
|---|---|
| ID | FT-X03 (finding n/a, epic EPIC-EXT-DEPLOY) |
| Type | Bug |
| Priority | P1 |
| Description | deploy/Dockerfile:5-6 installs only requirements.lock + requirements-fileparse.lock; numpy lives in the optional 'numerics' extra (pyproject.toml:29-33) and in no runtime lock. packages/eoip/processing/service.py:14 imports numpy at module level and apps/api/extended.py:1487 mounts the processing router at startup, so eoip-api dies with ModuleNotFoundError: numpy and compose reports 'dependency failed to start: eoip-api is unhealthy' (logs/compose_up3.log). A derived image with the numerics extras became healthy (diagnostic, not repo code). |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • Decide: numerics is a required runtime dependency, or processing routes are optional |
| Acceptance criteria | • Either a requirements-numerics.lock (hash-pinned) is installed in the runtime stage, or numpy is imported lazily and the processing router is mounted only when numerics is available (with a truthful 'unavailable' capability state)<br>• Fresh `docker compose -f deploy/docker-compose.yml up --build --wait` reaches healthy for eoip-api, eoip-worker and eoip-mcp with no extra packages<br>• CI job builds the runtime image and probes /health/ready (no test-stage deps) |
| Automated tests | • new: container smoke in CI: build runtime target, run, GET /health/ready == 200<br>• new: unit test importing apps.api.main.create_app in an env without numpy (if the lazy option is chosen) |
| Security controls | • Lock file hash-pinned (pip --require-hashes) |
| Implementation notes (file:line) | • deploy/Dockerfile:5-6<br>• packages/eoip/processing/service.py:14 (import numpy as np)<br>• apps/api/extended.py:1486-1487 (build_processing_router)<br>• pyproject.toml:29-33 (numerics extra)<br>• evidence: audit-output/test_results_extended/logs/compose_up3.log |
| Proof plan | **required_for_closure**: L2 (container smoke) + L3 (CI image job)<br>**l4_candidate**: healthy compose stack on fix commit |
| Estimated effort | 3 h (S) |
| Extended run (X-03) | severity High; source audit-output/test_results_extended/defects.json |

## FT-X04 [P1] Generated HugeGraph password (64 hex chars) exceeds Hubble's VARCHAR(48): hubble-init fails, so a fresh stack never starts

| Field | Value |
|---|---|
| ID | FT-X04 (finding n/a, epic EPIC-EXT-DEPLOY) |
| Type | Bug |
| Priority | P1 |
| Description | scripts/container.ps1:187-194 generates HUGEGRAPH_PASSWORD from 32 random bytes as 64 hex chars. scripts/setup_hubble.py:55-67 stores it in a Hubble connection; Hubble rejects it with 400 'Value too long for column PASSWORD VARCHAR(48)' (logs/compose_up2.log). eoip-api depends on hubble-init completing successfully (deploy/docker-compose.yml:109-111), so every first-run `container.ps1 up` fails. Worker C rated it Medium; raised to P1 here because it blocks the documented install path. Works with a 40-char password. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Generated password is ≤48 chars with ≥192 bits of entropy (e.g. 24 random bytes -> 48 hex, or base64url 32 chars)<br>• setup_hubble.py validates the length up front with a clear error instead of a Hubble 400<br>• Fresh `container.ps1 up` (and a bash equivalent) reaches healthy end to end<br>• Existing deploy/.env files with 64-char passwords get a documented rotation path |
| Automated tests | • new: unit test for the generator: length ≤48, charset, entropy<br>• new: setup_hubble rejects >48-char password with a clear message |
| Security controls | • Password stays random (CSPRNG); never logged |
| Implementation notes (file:line) | • scripts/container.ps1:187-194<br>• scripts/setup_hubble.py:55-67<br>• deploy/docker-compose.yml:109-111<br>• evidence: audit-output/test_results_extended/logs/compose_up2.log |
| Proof plan | **required_for_closure**: L2 + L4 (fresh stack healthy) |
| Estimated effort | 2 h (S) |
| Extended run (X-04) | severity Medium; source audit-output/test_results_extended/defects.json |

## FT-X07 [P2] Locust load scenarios call non-existent routes and send no auth (TEST-002 load evidence impossible)

| Field | Value |
|---|---|
| ID | FT-X07 (finding n/a, epic EPIC-EXT-DEPLOY) |
| Type | Test |
| Priority | P2 |
| Description | tests/load/locustfile.py:12,22,29 posts to /api/v1/query/multi_paradigm, /api/v1/routing/classify and /api/v1/token_formats/serialize with no Authorization header. 30 s / 5 users on localhost: 518/518 failed (401) as-is; 513/513 failed (404, some 401) with a bearer token. The real routes appear to be /api/v1/query/multi-paradigm (packages/eoip/enterprise/advanced_router.py:97), /routing/classify-and-route (packages/eoip/platform_router.py:1897) and /token-formats/serialize (platform_router.py:1855). Mount prefixes still need to be confirmed against /openapi.json. No NFR-PERF requirement can get load evidence until this is fixed. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Each scenario targets a route present in /openapi.json (asserted at locust on_start)<br>• Bearer token read from an env var (EOIP_LOAD_TOKEN), never hard-coded; on_start fails fast if unset<br>• A 30 s / 5-user run against the local stack has failure rate < 1% and reports p50/p95<br>• k6 scenarios (if kept) get the same route + auth review |
| Automated tests | • new: unit test parsing locustfile route constants and asserting each exists in create_app().openapi() |
| Security controls | • Token from env/secret store only |
| Implementation notes (file:line) | • tests/load/locustfile.py:12,22,29<br>• packages/eoip/enterprise/advanced_router.py:97<br>• packages/eoip/platform_router.py:1855,1897<br>• evidence: audit-output/test_results_extended/load/ (locust CSVs) |
| Proof plan | **required_for_closure**: L2 + L4 (load run on non-prod stack with CSV artifact) |
| Estimated effort | 2 h (S) |
| Extended run (X-07) | severity Medium; source audit-output/test_results_extended/defects.json |

## FT-X10 [P2] Code/test/doc drift: 11 failing tests, each needs a recorded decision (fix code vs update test + requirement)

| Field | Value |
|---|---|
| ID | FT-X10 (finding n/a, epic EPIC-DEFECTS) |
| Type | Governance |
| Priority | P2 |
| Description | Parent task for X-10. Each of the 11 tests asserts a feature or claim the code/docs no longer have. For every sub-item, an owner must decide which side is wrong and record it in the sub-item's 'decision' before the child task is worked. Child tasks hold the technical detail: FT-D04, FT-D05, FT-D06 (4 tests), FT-D09, FT-D11 (3 tests), FT-D12. All 11 still fail on Python 3.11 with locked deps, so they are not environment noise. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Every sub-item has decision ∈ {restore_code, update_test_and_requirement, remove_requirement} with decider + date<br>• If a test is changed, the linked requirement text changes in the same PR<br>• All 11 tests pass (or are deleted together with their requirement, with a changelog note) |
| Automated tests | • tests/unit/test_product_intelligence.py:133<br>• tests/unit/test_deployment_api.py:42<br>• tests/unit/test_kgr_export.py:37<br>• tests/unit/test_enterprise_security_wp55.py:160<br>• tests/unit/test_suggested_advanced_capabilities.py:123<br>• tests/unit/test_scale_and_polish_wp71.py:105<br>• tests/unit/test_license_documents.py:16<br>• tests/unit/test_gap_coverage.py:82<br>• tests/unit/test_gap_coverage.py:95<br>• tests/unit/test_gap_coverage.py:259<br>• tests/unit/test_gap_coverage.py:285 |
| Security controls | • UNKNOWN |
| Implementation notes (file:line) | • tests/unit/test_product_intelligence.py:133: /api/v1/loops/catalog absent from deployed route surface -> FT-D04<br>• tests/unit/test_deployment_api.py:42: expects OpenAPI scheme 'HTTPBearer'; app exposes 'SafeHTTPBearer' -> FT-D05<br>• tests/unit/test_kgr_export.py:37: 'pdf' export format missing from KGR export menu -> FT-D11<br>• tests/unit/test_enterprise_security_wp55.py:160: 'Enterprise Security & Token Governance' heading missing -> FT-D11<br>• tests/unit/test_suggested_advanced_capabilities.py:123: bitemporal context slate missing 'tax_rate' -> FT-D12<br>• tests/unit/test_scale_and_polish_wp71.py:105: docs/getting-started.md lacks 'Prerequisites' section -> FT-D11<br>• tests/unit/test_license_documents.py:16: pyproject.toml:10 license is a table; test expects SPDX string -> FT-D09<br>• tests/unit/test_gap_coverage.py:82: gap-coverage report returns blocking issue (GAP-STUDIO-005) -> FT-D06<br>• tests/unit/test_gap_coverage.py:95: completion_gate('P0') not passed -> FT-D06<br>• tests/unit/test_gap_coverage.py:259: CLI --fail-on-gate exits 1 -> FT-D06<br>• tests/unit/test_gap_coverage.py:285: gap-coverage API reports blocking issue -> FT-D06 |
| Proof plan | **required_for_closure**: children closed + decisions recorded (L2 per child) |
| Estimated effort | 1.5 h (S) – decision triage only; child effort counted on the children |
| Child tasks | FT-D04, FT-D05, FT-D06, FT-D09, FT-D11, FT-D12 |
| Extended run (X-10) | severity Low-Medium; source audit-output/test_results_extended/defects.json |

| Sub-item test | Issue | Child task | Decision |
|---|---|---|---|
| `tests/unit/test_product_intelligence.py:133` | /api/v1/loops/catalog absent from deployed route surface | FT-D04 | PENDING |
| `tests/unit/test_deployment_api.py:42` | expects OpenAPI scheme 'HTTPBearer'; app exposes 'SafeHTTPBearer' | FT-D05 | PENDING |
| `tests/unit/test_kgr_export.py:37` | 'pdf' export format missing from KGR export menu | FT-D11 | PENDING |
| `tests/unit/test_enterprise_security_wp55.py:160` | 'Enterprise Security & Token Governance' heading missing | FT-D11 | PENDING |
| `tests/unit/test_suggested_advanced_capabilities.py:123` | bitemporal context slate missing 'tax_rate' | FT-D12 | PENDING |
| `tests/unit/test_scale_and_polish_wp71.py:105` | docs/getting-started.md lacks 'Prerequisites' section | FT-D11 | PENDING |
| `tests/unit/test_license_documents.py:16` | pyproject.toml:10 license is a table; test expects SPDX string | FT-D09 | PENDING |
| `tests/unit/test_gap_coverage.py:82` | gap-coverage report returns blocking issue (GAP-STUDIO-005) | FT-D06 | PENDING |
| `tests/unit/test_gap_coverage.py:95` | completion_gate('P0') not passed | FT-D06 | PENDING |
| `tests/unit/test_gap_coverage.py:259` | CLI --fail-on-gate exits 1 | FT-D06 | PENDING |
| `tests/unit/test_gap_coverage.py:285` | gap-coverage API reports blocking issue | FT-D06 | PENDING |

## FT-X11 [P3] DLQ acceptance writes results as uid 10001 into a host bind mount: PermissionError on Linux hosts

| Field | Value |
|---|---|
| ID | FT-X11 (finding n/a, epic EPIC-EXT-DEPLOY) |
| Type | Bug |
| Priority | P3 |
| Description | deploy/docker-compose.dlq-acceptance.yml:100 bind-mounts ../test-results to /results; the test image runs as uid 10001 (deploy/Dockerfile:22-23), so on Linux hosts where the dir is owned by the invoking user the junit and JSON report writes fail. Worked around in the copy with chmod 777 (not acceptable as a fix). |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Results written to a named volume and copied out with `docker compose cp`, or the service runs with user: "${UID}:${GID}", or an init step creates the dir with the right owner<br>• `dlq-acceptance` flow writes its report on a fresh Linux host with no manual chmod |
| Automated tests | • CI job (ubuntu runner) runs the DLQ acceptance flow and uploads /results as an artifact |
| Security controls | • UNKNOWN |
| Implementation notes (file:line) | • deploy/docker-compose.dlq-acceptance.yml:100<br>• deploy/Dockerfile:22-23 (uid 10001) |
| Proof plan | **required_for_closure**: L3 (CI artifact present) |
| Estimated effort | 1 h (XS) |
| Extended run (X-11) | severity Low; source audit-output/test_results_extended/defects.json |

## FT-X12 [P3] dlq-graph healthcheck probes /versions, so schema-init can start before the graph API is ready

| Field | Value |
|---|---|
| ID | FT-X12 (finding n/a, epic EPIC-EXT-DEPLOY) |
| Type | Reliability |
| Priority | P3 |
| Description | deploy/docker-compose.dlq-acceptance.yml:57 marks dlq-graph healthy when /versions answers; schema-init then hit 400 on schema/vertexlabels in 2 of the cold starts (logs/dlq_acceptance2.log, dlq_acceptance3.log). Likely cause, NOT proven. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • Discovery: confirm by repeated cold starts with a readiness probe on the graph's schema endpoint |
| Acceptance criteria | • Healthcheck probes an endpoint that needs the graph backend ready (e.g. GET /graphs/hugegraph/schema) or schema-init retries with bounded backoff on 400/503<br>• 10 consecutive cold starts with no schema-init failure (log attached) |
| Automated tests | • scripted cold-start loop (10x) in CI or a documented manual receipt |
| Security controls | • UNKNOWN |
| Implementation notes (file:line) | • deploy/docker-compose.dlq-acceptance.yml:57<br>• evidence: audit-output/test_results_extended/logs/dlq_acceptance2.log, dlq_acceptance3.log |
| Proof plan | **required_for_closure**: L4 (10x cold-start receipt) |
| Estimated effort | 1.5 h (S) |
| Extended run (X-12) | severity Low; source audit-output/test_results_extended/defects.json |

## FT-H01 [P2] GUI workbench acceptance runs a list argv with shell=True: on POSIX it executes bare `npm`, so it always fails on Linux/CI

| Field | Value |
|---|---|
| ID | FT-H01 (finding n/a, epic EPIC-DEFECTS) |
| Type | Test |
| Priority | P2 |
| Description | tests/gui/test_gui_workbench_acceptance.py:70-76 and :265-271 call subprocess.run(['npm','run','test:unit'], shell=True). On POSIX, shell=True with a list runs only argv[0] ('npm', which prints usage and exits 1); the rest become shell positional args. `npm run test:unit` itself passes 20/20 (web_unit.junit.xml). Previously listed as environment-only; the extended run shows it is a test defect. The CRA-030.2 and CRA-030.A gates can never pass on Linux. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • subprocess.run(['npm','run','test:unit'], shell=(os.name == 'nt')) or shutil.which('npm') resolution<br>• Both tests pass on Linux with node 22 (repo needs --experimental-strip-types; system node 20 rejects it)<br>• Test skips with a clear reason when npm/node is missing, instead of failing |
| Automated tests | • tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states<br>• tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate |
| Security controls | • UNKNOWN |
| Implementation notes (file:line) | • tests/gui/test_gui_workbench_acceptance.py:70-76<br>• tests/gui/test_gui_workbench_acceptance.py:265-271<br>• node >= 22 needed by apps/web test:unit (see extended_summary.json environment.node) |
| Proof plan | **required_for_closure**: L2 + L3 |
| Estimated effort | 0.5 h (XS) |
| Failing tests covered | `tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states`<br>`tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate` |
| Extended run (test-harness) | severity n/a; source audit-output/test_results_extended/defects.json |

## FT-SEC-HUBBLE [P2] 'hubble-local-admin' action resets the HugeGraph admin account to admin/admin and writes it to deploy/.env

| Field | Value |
|---|---|
| ID | FT-SEC-HUBBLE (finding n/a, epic EPIC-FIND-SECURITY) |
| Type | Security |
| Priority | P2 |
| Description | scripts/container.ps1:254-266 runs scripts.setup_hubble --rotate-local-admin, which sets the graph 'admin' user's password to the literal 'admin' (scripts/setup_hubble.py:20-34), then rewrites HUGEGRAPH_PASSWORD=admin in deploy/.env and recreates the stack. The result is a well-known default credential (CWE-1392/CWE-798) on the graph that holds all ingested data. Mitigations seen: ports bind to 127.0.0.1 (deploy/docker-compose.yml:85), the action is opt-in and prints a warning, and deploy/.env is gitignored. Residual risk: any local process or container on the backend network gets graph admin, and the state persists in volumes after the demo. Priority P2: loopback-only and opt-in, but it persists silently. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Action sets a random password (CSPRNG, ≤48 chars, see FT-X04) instead of 'admin', or requires an explicit --i-understand-demo-credentials flag and refuses when any port binds beyond 127.0.0.1<br>• Hubble UI login uses a separate generated credential that is shown once<br>• A `hubble-local-admin --revert` path (or `up`) restores a random password; docs updated<br>• No literal 'admin' password remains in setup_hubble.py (grep check in CI) |
| Automated tests | • new: unit test: rotate_local_admin never sends user_password == 'admin'<br>• new: container.ps1 lint/pester test: action refuses when EOIP_*_PORT binds 0.0.0.0 |
| Security controls | • No default credentials<br>• Credential never echoed to logs<br>• Loopback-only binding enforced |
| Implementation notes (file:line) | • scripts/container.ps1:254-266<br>• scripts/setup_hubble.py:20-34 (rotate_local_admin, literal admin/admin)<br>• deploy/docker-compose.yml:85 (127.0.0.1 binding)<br>• .gitignore:54 (.env) |
| Proof plan | **required_for_closure**: L2 + L3 + L5 (security reviewer ≠ implementer) |
| Estimated effort | 3 h (S) |
| Extended run (X-04 note) | severity n/a; source audit-output/test_results_extended/defects.json |

## FT-K01 [P2] Audit kit: run_tests_and_map.py required Python ≥3.12 (backslash inside f-string expression)

| Field | Value |
|---|---|
| ID | FT-K01 (finding n/a, epic EPIC-KIT) |
| Type | Chore |
| Priority | P2 |
| Description | audit-scripts/run_tests_and_map.py:79 used re.sub(r'\[.*\]$', ...) inside an f-string expression, which is a SyntaxError before Python 3.12; worker C had to run it with 3.13. Kit-only defect, no repo impact. |
| API contracts | ServiceNowConnector(tables=...) override contract unchanged; default set changes. |
| Data model | None changed. |
| Performance targets | No regression (p95 of affected paths within ±5% of baseline). |
| Observability | Per-table sync counters and skipped-table warnings. |
| Backward compatibility | Deployments that started syncing cmdb_ci after 06319d7 need explicit tables= config. |
| Preconditions | • UNKNOWN |
| Acceptance criteria | • Every audit-scripts/*.py compiles on Python 3.11<br>• run_tests_and_map.py works on 3.11 in --reuse-junit and live-run modes, parametrized ids still stripped |
| Automated tests | • py_compile of all audit-scripts on CPython 3.11.17<br>• --reuse-junit on audit-output/test_results_merged (4329 cases)<br>• audit-scripts/selftest/selftest_run_tests_and_map.sh <python3.11> <python-with-pytest> (live --isolate + --reuse-junit, parametrized ids) |
| Security controls | • UNKNOWN |
| Implementation notes (file:line) | • audit-scripts/run_tests_and_map.py: regex hoisted to module constant _PARAM_SUFFIX_RE; case_key() builds the name before the f-string |
| Proof plan | **required_for_closure**: L2 (kit self-test)<br>**result**: PASS on CPython 3.11.17, 2026-10-19 |
| Estimated effort | 0.5 h (XS) |
| Status | Done (owner grok-bot-audit-kit) |
| Extended run (kit_issue) | severity n/a; source audit-output/test_results_extended/defects.json |

## Environment-only failures (no product task)

| Test | Reason |
|---|---|
| (none) | |

## Environment-only failures resolved by the extended run

| Test | Fix |
|---|---|
| `tests/semantic/test_shacl_differential.py::test_pyshacl_adapter_and_differential_oracle` | pyshacl installed (root cause tracked in FT-D14) |
| `tests/reva/unit/pd/test_pd_suite.py::test_sandbox_runner_process` | python shim on PATH (root cause tracked in FT-D13) |
| `tests/acceptance/test_developer_ecosystem_acceptance.py::test_cra_039_8_widoco_html_ontology_docs_and_route_serving` | py3.11 + full extras + EOIP_DATA_DIR set; residual test-isolation note: the test should use tmp_path rather than the /data default (packages/eoip/runtime.py:13-14) |

Reclassified from env_only_failures to **FT-H01**: `tests/gui/test_gui_workbench_acceptance.py::test_cra_030_2_typed_contracts_and_truthful_states`, `tests/gui/test_gui_workbench_acceptance.py::test_cra_030_a_acceptance_gate`. extended run: shell=True + list argv runs bare npm on POSIX; npm test:unit itself passes.
