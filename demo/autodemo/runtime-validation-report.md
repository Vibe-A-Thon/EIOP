# VS Code Auto-Demo Validation

Author-executed on 2026-10-04, at checkout HEAD
`776b55789b33aaf8403aff3bec8778d10eb35bfb` with uncommitted scoped edits.
This is not independent QA, installed-VSIX acceptance or whole-product certification.
Snapshot: `2026-10-04T21:05:25.5450404+05:30`.

Update on 2026-10-05 at clean `dev_local` HEAD
`e61d049c76131c41fe6fd99961a9344761478643`: `npm --prefix apps\vscode-extension test`
exited 0 with 7 native protocol/driver tests and 5 real-host fixture journeys.
Fresh fixture receipt:
`test-results/extension-host-51c66c37-a20e-43e5-be80-f6dbd08b1efb.json`.
The live desktop NLQ/MCP run below was not rerun in this continuation.

| Check | Result | Exit code | Evidence |
|---|---|---|---|
| Native Node protocol and driver tests | PASS, 4 tests | 0 | `npm.cmd test` in `apps\vscode-extension` |
| Real VS Code host contract tests | PASS, 5 journeys | 0 | [Fixture receipt](../../test-results/extension-host-9a3d8608-f8a2-40b3-afcf-05e175194980.json) |
| Visible live desktop demo | PASS, 3 steps | 0 | [Live receipt](../../test-results/vscode-live-demo-0356a3be-5f5b-42aa-99b7-5fbcf0632012.json) |
| Full and manual launcher dry-run | PASS | 0 | `run-demo.bat --mode full --dry-run` and `--mode manual --dry-run` |
| JavaScript syntax and whitespace | PASS | 0 | `node --check` on desktop scripts; `git diff --check` |

## Live scope

`node .\demo\autodemo\vscode-demo.js` launched the updated EOIP 0.1.0
source extension in cached VS Code 1.96.4 with a disposable profile.
It exercised authenticated local API NLQ and actual MCP JSON-RPC initialization,
initialized notification, discovery, search and lineage. Both NLQ and MCP search
resolved the live `urn:eoip:work:item:jira:PAY-142` anchor; lineage returned graph
nodes. NLQ engine: `query_plan`; MCP protocol: `2024-11-05`.
Results appeared in real JSON editors with a 2.5-second pause per step.

The first live attempt explicitly failed because PAY-202 was absent in the
deployed graph (search returned zero nodes). The driver now reads the ready
intent-to-runtime scenario from the live catalog instead of assuming the console
fixture dataset is deployed. Two subsequent live runs passed.

The first host regression exposed the existing read-only POST assertion's missing
NLQ/MCP allowlist entries; these were updated without relaxing the read-only
boundary. One subsequent host startup exited 1 without an assertion diagnostic.
Failure receipts now preserve journey detail. The final two host runs passed.
Cached VS Code still reports mutex, deprecated N-API and API-proposal warnings;
passing receipts do not mean these platform warnings were eliminated.

## Environment and boundaries

```text
environment:
  docker: AVAILABLE - documented user-local docker.exe info returned 29.8.1
  node: AVAILABLE - node --version returned v26.8.2
  playwright: SKIPPED - no web UI changes; desktop uses real VS Code host
  infra-tier: PRIMARY(existing local deployed API/MCP); no restart/rebuild
  browser-tier: SKIPPED - prior web/browser checks not rerun
startup: PASS - exit_code: 0; isolated VS Code host loaded the source extension; startup timing not separately measured
integration: PASS - exit_code: 0; 4 native tests + 5 fixture host journeys; no live claim for fixtures
e2e: PASS - exit_code: 0; 3 live isolated desktop steps, 0 failures
overall: NEEDS_SIGNOFF - scoped implementation verified; independent QA/installed VSIX/full launcher deployment path remain unverified
```

The bare Docker command and Program Files fallback were unavailable; the
runbook's user-local executable worked. No Docker services, graph data or normal
VS Code profile were changed. No dependencies were installed, runtime downloaded,
VSIX rebuilt/installed, commit made or PR published. The full batch launcher's
Docker rebuild plus console path was not re-executed; only its dry-run and the
standalone live desktop phase were run in this pass.

Receipts are ignored local evidence and may not exist in another checkout.
Reproduce with the commands above and prerequisites in [README](README.md).
