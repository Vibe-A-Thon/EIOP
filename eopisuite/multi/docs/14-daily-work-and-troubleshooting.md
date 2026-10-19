# Daily Development and Troubleshooting

## Start a Work Session

1. Open the pilot/full `.code-workspace`, not the plain parent folder as a new monorepo.
2. Inspect each relevant repository's branch and dirty state. Preserve unrelated changes.
3. Identify the work package, source owners, contract versions and permitted repositories.
4. Install locked dependencies in each selected repository's own environment.
5. Start only the runtime profile/apps needed for the task; verify health and authenticated behavior.
6. Work on a feature branch in each affected repository and link them by one change ID.

Read-only status inspection from the workspace parent:

```powershell
$Names = @('eoip-suite','eoip-contracts','eoip-ui','eoip-query-portal','eoip-knowledge-portal')
foreach ($Name in $Names) {
    Write-Host "Repository: $Name"
    git -C $Name status --short --branch
    if ($LASTEXITCODE -ne 0) { throw "Cannot inspect $Name" }
}
```

Do not issue parent-wide `git add`, `reset`, `clean`, pulls or branch switches. Inspect and commit one repository at a time. An editor workspace does not combine Git histories or transactions.

## Change a Shared Contract

Create an additive provider change, contract snapshot and SDK candidate. Run consumers against the published candidate artifacts. Open dependent PRs with explicit versions and merge order; promote a tested suite-lock change only after integration. Keep the old contract until its retirement criteria pass. If a breaking change is unavoidable, document the compatibility adapter/migration instead of relying on synchronized developer checkouts.

## Bring a New Developer Onboard

Grant only required org/repo/package access, confirm GitHub identity, run bootstrap, open the workspace, select per-folder interpreters and install locked packages. Have the developer build one app without sibling source access, run a real authorized/denied API journey, make a small branch change and reproduce a known failure. This exercises the setup more meaningfully than opening files successfully.

## Troubleshooting Matrix

| Problem | Diagnose | Resolution / evidence |
|---|---|---|
| Repo clone denied | Correct org/account, membership, SSO authorization if configured, repository visibility | Fix minimal access; never make repo public as a workaround |
| npm package 401/404 | Correct lowercase scope, registry, package access and supported token type | Grant only intended consumer access; prove install without logging token |
| pip cannot find internal package | Private wheel source/index actually exists; expected artifact/version | Download verified wheel or configure approved registry; no imaginary GitHub PyPI endpoint |
| Works only in full workspace | Sibling imports, editable dependency, cwd-relative data or missing wheel resources | Fix packaging and reproduce in a clean isolated checkout |
| API import fails after move | Application namespace, platform version and package discovery | Correct declared package/entry point; do not restore a global legacy PYTHONPATH |
| Worker writes invisible to API | Separate memory graph or mismatched backend/data configuration | Use qualified shared persistence; re-run source-to-query effect check |
| Shared queue corrupts under more workers | Existing local file topology exceeded | Stop scaling; qualify durable claims/fencing/recovery before multi-worker release |
| Browser deep link 404 | Vite base, router basename, proxy prefix and static fallback | Preserve assigned root and test actual refresh/assets through gateway |
| Vite hot reload fails through gateway | Websocket routing and public HMR address | Test per-app path and gateway port; do not expose arbitrary hosts |
| Logout seems successful but another app works | Browser token/session state, server invalidation, cached grants | Implement actual revocation and cross-app negative tests |
| Database/Fleet visible to ordinary admin | Catalog and server trust-plane policy | Deny both navigation and direct privileged API access; audit attempts |
| REVA health is green but requests fail | Optional mount, kernel initialization, settings, keys and principal binding | Follow REVA integration gates; static health is not readiness |
| Independent CI passes, suite fails | Different artifacts/contracts/config/migrations | Reproduce exact suite lock; fix compatibility, not evidence thresholds |
| Extension opens wrong source root | Active document root, duplicate paths and workspace mapping | Use explicit selected root and path confinement; test non-first folder |
| Missing release evidence | Retention expired, local-only paths, digest mismatch | Rerun appropriate verification; never reconstruct a passing receipt from memory |
| Local port conflict | Existing process and effective profile map | Choose a coherent alternative profile; do not kill unrelated processes |

## Stop and Resume

Stop dev tasks explicitly. Preserve graph/authority/job volumes; do not routinely use volume-deleting teardown. Record long-running jobs and any interruption semantics. On resume verify branch/artifact/profile alignment before using old evidence or cached builds.

## Handover Checklist

Record changed repositories/commits, linked PRs, exact artifacts, migrations, commands executed, observed results, evidence locations, failures/skips, rollback and remaining decisions. Preserve state distinctions: scaffolded, implemented, executed, verified. A maintenance team must be able to reproduce the selected deployment without access to the original developer's machine.
