# Secret rotation & git-history purge plan: Vibe-A-Thon/EIOP

| | |
|---|---|
| Findings | **F-01 (Critical)** plaintext RBAC tokens committed. **F-02 (High)** hard-coded bootstrap token |
| Repo | https://github.com/Vibe-A-Thon/EIOP (public, 0 forks and 2 closed PRs observed 2026-10-19) |
| Audited commit | `3ed3acd50e47ab8867aa6885d202f9956358dc3a` (`dev_local`). The remote `dev_local` tip has since moved to `76f8e8b`, so re-check before acting |
| Owner of every step | Repo owner / org admin. **This kit and its agents never push, rotate or contact anyone.** |
| Token values | **Never** written in this plan, in tickets, chat, CI logs or evidence. Refer to them by principal name only. |

## 0. What is exposed (facts from read-only inspection)

| Secret (by principal) | Role / tenant | Where it is in the tree at `3ed3acd` | Introduced |
|---|---|---|---|
| `root-superadmin` | superadmin / `*` (cross-tenant) | `Logins_credentials.keys:69`, `frontend/src/screens/SignIn.tsx:17` (pre-filled, `:30`) + `:20`, `memory/test_credentials.md:9` | 3e42426 (dev_local), 3339d54 (conflict_161026_1710), 2026-10-16 |
| `default-admin` | admin / default | `Logins_credentials.keys:70`, `SignIn.tsx:21`, `memory/test_credentials.md:10` | same |
| `data-steward` | steward / default | `:71`, `SignIn.tsx:22`, `memory/test_credentials.md:11` | same |
| `analyst` | analyst / default | `:72`, `SignIn.tsx:23`, `memory/test_credentials.md:12` | same |
| `viewer` | viewer / default | `:73`, `SignIn.tsx:24`, `memory/test_credentials.md:13` | same |
| bootstrap `EOIP_API_TOKEN` dev placeholder | **superadmin** via `apps/api/asg.py:113-124` | `backend/server.py:22`, `memory/test_credentials.md:16`, `test_reports/iteration_1..5.json` | 8 commits from 7e881b4, 2026-10-16 |

How they are used:
- `apps/api/asg.py:140-144` (`default_keys_path`) falls back to `<repo>/Logins_credentials.keys` when `EOIP_ASG_FILE` is unset.
- `apps/api/main.py:225-235` builds the ASG from that file and checks it **before** the JWT validator.
- `asg.py:113-136` always registers `EOIP_API_TOKEN` as a superadmin.
- `backend/server.py:22` sets that variable to a committed literal when it is unset.
- `deploy/Dockerfile` does not copy the keys file, so images built from it are unaffected by the file. They **are** affected if `EOIP_API_TOKEN` is unset and the image runs through `backend/server.py`, and the web bundle built from `frontend/` embeds the tokens regardless.

Remote refs (from a read-only mirror, 2026-10-19):

| Ref | Contains token values? |
|---|---|
| `dev_local` | **yes** (tree and history) |
| `conflict_161026_1710` | **yes** (tree and history) |
| `main`, `uat`, `pre_uat`, `int_test`, `dev_test`, `jdev_local`, `merge_integration`, `feature/*`, `copilot/*` | not at the tip. History is still rewritten by the purge (see §5) |
| `refs/pull/1/head`, `refs/pull/2/head` | no |
| tags | none exist |

## 1. Immediate containment (first hour, before any code change)

- [ ] **C1** Name an incident owner and open a *private* tracking issue (GitHub Security Advisory draft → "Private vulnerability report"). Do not paste values.
- [ ] **C2** Inventory every running EOIP instance: the supervisor preview (`backend/server.py`, port 8001), local Docker (`deploy/docker-compose*.yml`), Helm (`deploy/helm/eoip`), and any shared or demo hosts. *Discovery: which of these are reachable from the internet is UNKNOWN to the audit.*
- [ ] **C3** For each internet-reachable instance: block it at the edge (IP allow-list or stop it) until rotation completes. Superadmin is cross-tenant, so treat every tenant's data as potentially exposed.
- [ ] **C4** Take snapshots for forensics **before** restarting anything: `<EOIP_DATA_DIR>/audit/audit.jsonl`, reverse-proxy/ingress logs, container logs. Store them read-only and outside the repo.
- [ ] **C5** Make the repo private temporarily (Settings → General → Danger Zone → Change visibility) **only if** collaborators agree. This stops new clones but does not un-leak anything; the purge in §5 is still needed.
- [ ] **C6** Stop publishing any build of `frontend/` (it embeds the tokens). Delete preview deployments built from it.
- [ ] **C7** Copy the current `Logins_credentials.keys` to an encrypted, access-controlled location (e.g. a password-manager secure note) **solely** for the revocation verification in §3. Delete that copy when §3 passes.

## 2. New tokens: generation, storage, fail-closed loaders

### 2.1 Generate (never echo to a terminal, history or logs)

```bash
umask 077
python3 - <<'PY' > /run/secrets/eoip-new-tokens.env   # tmpfs/secure path; never inside the repo
import secrets
def tok(): return "eoip_pat_" + secrets.token_urlsafe(32)   # 256-bit, 52 chars total
print("EOIP_API_TOKEN=" + tok())
for p in ["root-superadmin","default-admin","data-steward","analyst","viewer"]:
    print(f"EOIP_ASG_{p.upper().replace('-','_')}=" + tok())
PY
```

New tokens use a recognisable prefix, `eoip_pat_`, so secret scanning and gitleaks can match them (§6). Do **not** reuse any old value, even partially.

### 2.2 Store (never in the repo)

| Environment | Where | Notes |
|---|---|---|
| Kubernetes / Helm | `kubectl create secret generic eoip-secrets --from-env-file=...` then `config.existingSecret: eoip-secrets` (`deploy/helm/eoip/templates/deployment.yaml:83-93`) | Never use `config.apiToken` in values files |
| Docker Compose | `deploy/.env` (already gitignored, `.gitignore` `.env`/`.env.*`), created by `scripts/container.ps1:188-196` | chmod 600; keep `deploy/.env.example` placeholder-only |
| Supervisor preview | the platform's secret/env settings | `backend/server.py` must **not** default it (§2.3) |
| ASG principals | a hashed ASG file mounted from the secret store, path in `EOIP_ASG_FILE` (e.g. `/run/secrets/eoip-asg`), mode 0400 | Store `sha256:<hex>` digests, not plaintext (§2.3) |
| CI | GitHub Actions *environment* secrets, never repository variables | |

Create the hashed ASG file without echoing values:

```bash
python3 - <<'PY' > /run/secrets/eoip-asg && chmod 400 /run/secrets/eoip-asg
import hashlib, os
roles = {"ROOT_SUPERADMIN":("superadmin","*","root-superadmin"), "DEFAULT_ADMIN":("admin","default","default-admin"),
         "DATA_STEWARD":("steward","default","data-steward"), "ANALYST":("analyst","default","analyst"), "VIEWER":("viewer","default","viewer")}
env = dict(l.strip().split("=",1) for l in open("/run/secrets/eoip-new-tokens.env") if "=" in l)
for k,(role,tenant,user) in roles.items():
    print(f"sha256:{hashlib.sha256(env['EOIP_ASG_'+k].encode()).hexdigest()} | {role} | {tenant} | {user}")
PY
```

Then distribute each plaintext token to its holder through the password manager and delete `/run/secrets/eoip-new-tokens.env`.

### 2.3 Loader changes (fail closed). Implement in one PR *before* the purge

**`apps/api/asg.py`**: no default path, hashed entries, permission check, revocation denylist, opt-in bootstrap superadmin.

```python
# asg.py — proposed (sketch)
import hashlib, stat

REVOKED_SHA256_FILE_ENV = "EOIP_REVOKED_TOKEN_SHA256_FILE"   # newline list of sha256 hex of revoked tokens

def _digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def default_keys_path() -> str | None:
    return os.environ.get("EOIP_ASG_FILE") or None            # was: <repo>/Logins_credentials.keys

def _revoked() -> set[str]:
    p = os.environ.get(REVOKED_SHA256_FILE_ENV)
    return {l.strip() for l in Path(p).read_text().splitlines() if l.strip()} if p else set()

def _parse_line(line):                                       # entries become sha256:<hex>
    ...
    if token.startswith("sha256:"):
        digest = token[7:].lower()
    elif os.environ.get("EOIP_ENV") == "dev" and os.environ.get("EOIP_ASG_ALLOW_PLAINTEXT") == "true":
        digest = _digest(token.removeprefix("plain:"))
    else:
        raise ValueError("plaintext ASG token rejected; store sha256:<hex>")
    return ASGEntry(token_sha256=digest, ...)

def load_asg(path, bootstrap_token):
    """Fail closed: a configured but unreadable/insecure/invalid file is FATAL."""
    revoked, entries = _revoked(), []
    if path:
        p = Path(path)
        mode = p.stat().st_mode
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            raise RuntimeError(f"{p} must not be group/world accessible (chmod 400)")
        for raw in p.read_text(encoding="utf-8").splitlines():
            ...  # parse errors -> raise, not print-and-continue (current asg.py:110-111)
    if any(e.token_sha256 in revoked for e in entries):
        raise RuntimeError("ASG contains a revoked token")
    if bootstrap_token:
        if len(bootstrap_token) < 32 or _digest(bootstrap_token) in revoked:
            raise RuntimeError("EOIP_API_TOKEN is weak or revoked")
        if os.environ.get("EOIP_BOOTSTRAP_SUPERADMIN") == "true":     # was: always superadmin
            entries.append(ASGEntry(token_sha256=_digest(bootstrap_token), roles=expand_roles(("superadmin",)), ...))
    if not entries:
        raise RuntimeError("no principals configured; refusing to start")
    return ASG(entries)

class ASG:
    def authenticate(self, supplied):
        if not supplied or len(supplied) > 16_384:
            return None
        d = _digest(supplied).encode()
        hit = None
        for e in self.entries:                                     # constant-time, no early exit
            if hmac.compare_digest(d, e.token_sha256.encode()):
                hit = e
        return hit
```

**`apps/api/main.py:221-226`**: keep `api_token()` (it already raises below 24 chars, `packages/eoip/runtime.py:17-21`). Raise the minimum to 32. Call `load_asg(default_keys_path(), token)` with no repo fallback. Log only `asg.summary()` (usernames and roles), never tokens.

**`packages/eoip/runtime.py:17-21`**: `len(value) < 32` → raise. Also raise if `sha256(value)` is in the revoked file.

**`backend/server.py:22`**: delete the `setdefault("EOIP_API_TOKEN", …)`. Replace it with:

```python
if not os.environ.get("EOIP_API_TOKEN"):
    if os.environ.get("EOIP_ENV") != "dev":
        raise SystemExit("EOIP_API_TOKEN is required (inject from the secret store)")
    import secrets
    os.environ["EOIP_API_TOKEN"] = secrets.token_urlsafe(32)        # ephemeral, per process, never printed
    (_DATA_DIR / "dev-token").write_text(os.environ["EOIP_API_TOKEN"]); os.chmod(_DATA_DIR / "dev-token", 0o600)
os.environ.setdefault("EOIP_LOAD_DEMO", "false")                    # was "true"
```

**`frontend/src/screens/SignIn.tsx:17-30`**: remove `DEV_TOKEN` and the `token` fields of `DEMO_ROLES`. Initialise the field empty (`useState("")`). If quick-login is still wanted in dev, read `import.meta.env.VITE_DEV_TOKEN` from an untracked `.env.local`, and only when `import.meta.env.DEV`.

**Delete** `memory/test_credentials.md`. Scrub `test_reports/iteration_*.json`, or delete them; they are generated artefacts.

**Tests to add** (they become the L2 evidence):
- `tests/unit/test_asg_fail_closed.py`:
  - no path and no token → `RuntimeError`;
  - world-readable file → error;
  - plaintext entry outside dev → error;
  - revoked digest → error;
  - bootstrap is not superadmin unless opted in;
  - `authenticate()` accepts the digest-matched token and rejects others.
- `tests/unit/test_backend_shim_fail_closed.py`: importing `backend.server` without `EOIP_API_TOKEN` and with `EOIP_ENV` unset exits.
- `tests/unit/test_no_committed_secrets.py`: scans `git ls-files` for the ASG line regex in §6.3 and for `eoip_pat_`.

## 3. Revoke the old tokens and prove they fail

Tokens are static bearer strings with no server-side session store. **Revocation means removing them from every running instance's ASG file and `EOIP_API_TOKEN`, then adding their digests to the denylist.**

1. Build the denylist from the secured copy (C7) without printing values:
   ```bash
   umask 077
   python3 - <<'PY' > /run/secrets/eoip-revoked.sha256
   import hashlib, re
   lines = open("/secure/old/Logins_credentials.keys").read().splitlines()
   toks = [l.split("|")[0].strip() for l in lines if "|" in l and not l.lstrip().startswith("#")]
   toks.append(re.search(r'EOIP_API_TOKEN",\s*"([^"]+)"', open("/secure/old/server.py").read()).group(1))
   for t in toks: print(hashlib.sha256(t.encode()).hexdigest())
   PY
   ```
   Digests of 38-char random tokens do not reveal them, but keep the file in the secret store anyway.
2. Deploy the §2.3 build everywhere with `EOIP_ASG_FILE`, the new `EOIP_API_TOKEN` and `EOIP_REVOKED_TOKEN_SHA256_FILE`. Restart (`sudo supervisorctl restart backend` on the preview).
3. **Verify** against each environment. This prints status codes only:
   ```bash
   python3 - <<'PY'
   import urllib.request, urllib.error
   BASE = "https://<host>"                                  # each environment from C2
   lines = open("/secure/old/Logins_credentials.keys").read().splitlines()
   olds = [(l.split("|")[3].strip(), l.split("|")[0].strip()) for l in lines if "|" in l and not l.lstrip().startswith("#")]
   for user, tok in olds:
       for path in ("/api/v1/admin/jobs", "/auth/me", "/api/v1/graph/stats"):
           req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + tok})
           try: code = urllib.request.urlopen(req, timeout=10).status
           except urllib.error.HTTPError as e: code = e.code
           print(f"{user:16} {path:28} {code}")              # expected: 401 for every row
   PY
   ```
   Expected: **401 on every row**. Then repeat with one **new** token per role and expect 200 or 403 according to the role. *Discovery: confirm the exact authenticated paths per deployment, since route names above are UNKNOWN for every env.*
4. Save the output (codes only) as `audit-output/evidence/remediation/F-01-revocation-<env>.txt`. This is the **L4** artefact.
5. Delete the C7 copy. Keep only the digest file.

## 4. Remove the files and ignore them

In one PR to every affected long-lived branch (`dev_local`, plus any branch you keep; `conflict_161026_1710` should probably be deleted, which is the owner's decision):

```bash
git rm --cached Logins_credentials.keys memory/test_credentials.md
git rm test_reports/iteration_*.json        # or scrub them
cat >> .gitignore <<'EOF'

# Secrets: never commit (F-01)
Logins_credentials.keys
*.keys
!*.keys.example
/memory/test_credentials.md
.eoip-data/dev-token
/run/
EOF
cp /dev/null Logins_credentials.keys.example && echo '# sha256:<hex> | <role> | <tenant|*> | <username>' > Logins_credentials.keys.example
```

Also update the docs that tell people to edit the file: the header of the old file, `memory/`, `README.md`, `docs/getting-started.md`. Point them at `EOIP_ASG_FILE` plus the secret store.

## 5. Purge history with git-filter-repo

> ⚠️ **Force-push warning.** This rewrites **every branch**; all 12 branch heads change, including `main`, because the bootstrap placeholder appears in shared history. Every clone, fork, open PR and CI cache becomes incompatible. Do it once, in a scheduled window, after §2–§4 are merged and every collaborator has been told.

Rehearsed by the audit on a throwaway mirror in `/tmp` (no remote, no push). With the commands below, 4993 blobs were scanned afterwards with **0** remaining occurrences, and `Logins_credentials.keys` was in **0** commits. The rehearsal copy and its replacements file were deleted.

```bash
# 0. Pre-flight (repo admin, clean machine)
pip install git-filter-repo            # >= 2.38
gh api repos/Vibe-A-Thon/EIOP --jq '.forks_count'               # expect 0; else see 5.4
gh api repos/Vibe-A-Thon/EIOP/branches --paginate --jq '.[].name' > branches.before.txt
#    Temporarily allow force-push on protected branches (Settings → Branches / Rulesets)

# 1. Fresh mirror (filter-repo refuses non-fresh clones; never run it in a working clone)
git clone --mirror https://github.com/Vibe-A-Thon/EIOP.git eiop-purge.git && cd eiop-purge.git

# 2. Replacement rules built from the secured old copy; values never printed or typed
umask 077
python3 - <<'PY' > /run/secrets/replacements.txt
import re
lines = open("/secure/old/Logins_credentials.keys").read().splitlines()
toks = [l.split("|")[0].strip() for l in lines if "|" in l and not l.lstrip().startswith("#")]
toks.append(re.search(r'EOIP_API_TOKEN",\s*"([^"]+)"', open("/secure/old/server.py").read()).group(1))
for t in toks: print(f"{t}==>REDACTED-ROTATED-TOKEN")
PY

# 3. Rewrite ALL refs: drop the files everywhere, replace values that live inside other files
git filter-repo --force \
  --invert-paths --path Logins_credentials.keys --path memory/test_credentials.md \
  --replace-text /run/secrets/replacements.txt
#   (add --path-glob 'test_reports/iteration_*.json' to --invert-paths if you deleted them in §4)

# 4. Verify locally BEFORE pushing: must print 0 / 0
git log --all --oneline -- Logins_credentials.keys | wc -l
python3 - <<'PY'
import subprocess
rules=[l.split("==>")[0] for l in open("/run/secrets/replacements.txt").read().splitlines()]
objs=subprocess.check_output(["git","cat-file","--batch-all-objects","--batch-check=%(objectname) %(objecttype)"]).decode().split("\n")
blobs=[o.split()[0] for o in objs if o.endswith(" blob")]
p=subprocess.Popen(["git","cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
data,_=p.communicate(("\n".join(blobs)+"\n").encode())
print(sum(data.count(r.encode()) for r in rules))
PY
gitleaks git --redact -v . || true     # second opinion (v8.19+; older: gitleaks detect --source . --redact)

# 5. Push the rewritten history: all branches and all tags (none today). Never --mirror,
#    because refs/pull/* are read-only on GitHub and --mirror would also delete remote-only refs.
git remote add origin https://github.com/Vibe-A-Thon/EIOP.git   # filter-repo removes origin
git push --force --all origin
git push --force --tags origin
shred -u /run/secrets/replacements.txt

# 6. Post-push check from a NEW clone
cd .. && git clone https://github.com/Vibe-A-Thon/EIOP.git verify && cd verify
git log --all --oneline -- Logins_credentials.keys | wc -l        # 0
```

### 5.1 Collaborators
- Announce the window at least 24 h ahead, with a freeze on pushes.
- Afterwards everyone must **re-clone**. Do not `git pull` or rebase old clones: a stale clone that pushes re-introduces the history.
- Ask each collaborator to delete their old clones and any local copies of the file. Verify in their re-clone with `git log --all -- Logins_credentials.keys | wc -l` → 0.
- Re-create open work from patches (`git format-patch` against the old base, then `git am` on the new one), not by merging old branches.

### 5.2 PRs
- PRs #1 and #2 are closed, and their head refs do not contain the values; leave them.
- Any PR opened before the purge must be closed and re-opened from a fresh branch.
- PR head refs (`refs/pull/*`) cannot be force-updated. If one ever contains a value, only GitHub Support can remove it (5.4).

### 5.3 CI and caches
- Delete Actions caches: `gh cache delete --all`.
- Delete old workflow artifacts that may contain built `frontend/` bundles: `gh api repos/Vibe-A-Thon/EIOP/actions/artifacts --paginate`, then DELETE each.
- Re-run CI on the new heads.

### 5.4 Forks and GitHub Support
- `forks_count` was 0 on 2026-10-19. Re-check right before pushing. For any fork, ask the owner to delete it, or report it to GitHub if it is out of your control.
- Old commit SHAs (`3e42426`, `3339d54`, and every descendant) stay viewable by SHA URL until GitHub garbage-collects them. Open a ticket at https://support.github.com/contact (category "Removing sensitive data") asking them to:
  1. remove cached views of the listed SHAs;
  2. dereference and garbage-collect orphaned commits;
  3. purge PR refs if needed.
  Give them the affected SHAs and file paths, **never the values**. This is GitHub's documented "Removing sensitive data from a repository" process.
- Rewriting history does **not** make leaked tokens safe. §3 rotation is the real fix; the purge only limits further spread.

## 6. Prevent recurrence

### 6.1 GitHub secret scanning and push protection
- Settings → Code security → **Secret Protection**: enable *Secret scanning* and *Push protection*. Both are free for public repositories.
- Add **custom patterns** (Settings → Code security → Custom patterns):
  - `eoip_pat_[A-Za-z0-9_\-]{43}` (new token format);
  - ASG line format: `(?m)^\s*[A-Za-z0-9_\-:]{24,}\s*\|\s*(superadmin|admin|system|steward|analyst|viewer)\b`.
- Turn on push protection for the custom patterns too.
- Review existing alerts under Security → Secret scanning.

### 6.2 gitleaks pre-commit hook

`.gitleaks.toml` (repo root):

```toml
[extend]
useDefault = true

[[rules]]
id = "eoip-pat"
description = "EOIP personal access token"
regex = '''eoip_pat_[A-Za-z0-9_\-]{43}'''

[[rules]]
id = "eoip-asg-plaintext-line"
description = "Plaintext ASG principal line (token | role | tenant | user)"
regex = '''(?m)^\s*[A-Za-z0-9_\-]{24,}\s*\|\s*(superadmin|admin|system|steward|analyst|viewer)\b'''

[allowlist]
paths = ['''Logins_credentials\.keys\.example''']
```

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.0          # pin to the latest release when adopting
    hooks:
      - id: gitleaks
```

Each developer then runs `pip install pre-commit && pre-commit install`.

### 6.3 CI job (`.github/workflows/secret-scan.yml`)

This uses the gitleaks CLI rather than `gitleaks-action`, which needs a paid licence for organisation accounts.

```yaml
name: secret-scan
on:
  push: { branches: ['**'] }
  pull_request:
permissions: { contents: read }
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: gitleaks (full history, redacted)
        run: |
          docker run --rm -v "$PWD:/repo" ghcr.io/gitleaks/gitleaks:v8.24.0 \
            git /repo --redact --no-banner --exit-code 1 --report-path /repo/gitleaks.sarif --report-format sarif
      - name: upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: gitleaks.sarif }
  fail-closed-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: python -m pip install -e ".[dev]"
      - run: python -m pytest -q tests/unit/test_asg_fail_closed.py tests/unit/test_backend_shim_fail_closed.py tests/unit/test_no_committed_secrets.py
```

Add `secret-scan.yml` to `audit-config.json → ci.l3_eligible_workflows`, so a green run on the fix commit counts as **L3**. Make it a required status check on `main` and `dev_local`.

## 7. Check access logs for misuse

**Window:** from the first public push of 3e42426 / 3339d54 / 7e881b4 (all 2026-10-16; *exact push time UNKNOWN; get it from `gh api repos/Vibe-A-Thon/EIOP/events` or the audit log of the org*) until §3 completes.

1. **App audit trail.**
   - Each instance writes `<EOIP_DATA_DIR>/audit/audit.jsonl`, a hash-chained JSONL with fields `actor, event_type, operation, outcome, path, reason_code, timestamp, correlation_id, _prev_hash, _chain_hash` (`apps/api/main.py:380-406`).
   - `actor` is the ASG **username**, so filter on the leaked principals:
     ```bash
     python3 - <<'PY'
     import json, collections, hashlib
     LEAKED = {"root-superadmin","default-admin","data-steward","analyst","viewer","bootstrap-superadmin","bootstrap-admin"}
     hits = collections.Counter(); first = {}
     for l in open("audit.jsonl"):
         e = json.loads(l)
         if e.get("actor") in LEAKED and e.get("timestamp","") >= "2026-10-16":
             k = (e["actor"], e.get("event_type"), e.get("outcome")); hits[k] += 1; first.setdefault(k, e["timestamp"])
     for k, n in hits.most_common(): print(n, k, "first:", first[k])
     PY
     ```
   - Focus on destructive or cross-tenant operations: ontology publish/rollback, snapshots restore/delete, marketplace install, tenant/brand admin, and admin ingestion.
   - Verify chain integrity (`_prev_hash` of each record equals the previous record's `_chain_hash`, per `AuditSink._compute_chain_hash`). A broken chain means tampering or truncation.
   - Baseline: the committed preview log `.eoip-data/audit/audit.jsonl` already has 1867 events (root-superadmin 5, viewer 7, default-admin 1, bootstrap-superadmin 1, bootstrap-admin 505). Use it to tell normal developer use from anomalies.
2. **Limitation:** the audit record has **no source IP or user-agent**. Correlate by `correlation_id` and timestamp with reverse-proxy/ingress logs (nginx/traefik/k8s ingress, cloud load balancer). Look for leaked-principal activity from IPs outside the team. Follow-up task: add `client_ip` and `user_agent` to `AuditEvent`.
3. **GitHub side** (repo admin): `gh api repos/Vibe-A-Thon/EIOP/traffic/clones` and `/traffic/views` (last 14 days), plus the org audit log. These show exposure volume, not identities.
4. **Data checks:**
   - graph and ontology change journals (`<data>/journal/semantic-changes.ndjson`) for unexpected writes;
   - `state/source-registry.json` for new connectors (exfiltration paths);
   - job queue `<data>/jobs/*.json`.
5. If misuse is found, it becomes a data-breach process: tenant notification, legal. That is outside this plan, and the owner decides.

## 8. Verification checklist (all must pass)

| # | Check | Command / method | Expected |
|---|---|---|---|
| V1 | Old tokens rejected in every env | §3 step 3 script | 401 for every principal and path |
| V2 | New tokens work per role | same script with new tokens | 200/403 per RBAC matrix |
| V3 | Server refuses to start insecurely | start without `EOIP_API_TOKEN`; with a world-readable ASG file; with a plaintext entry; with a revoked token | process exits non-zero with a clear error |
| V4 | No secret in tree | `git grep -nE 'eoip_pat_|\|\s*superadmin' $(git rev-parse HEAD)` and `gitleaks dir . --redact` | no matches |
| V5 | No secret in history | §5 step 4 on a fresh clone | 0 / 0 |
| V6 | Web bundle clean | `npm --prefix frontend run build`, then run the §5 step-4 count script with `data` = the bytes of every file under `frontend/dist` (it compares against the secured rule file, so no literal values are typed); also `grep -rl 'eoip_pat_' frontend/dist` | 0 occurrences |
| V7 | Push protection active | try pushing a commit with a dummy `eoip_pat_` + 43 chars | push blocked |
| V8 | CI gate green | `secret-scan` workflow on the fix commit | success |
| V9 | Logs reviewed | §7 report signed by incident owner | no unexplained use, or incident opened |
| V10 | GitHub Support ticket | ticket ID recorded | cached views purged |

## 9. Closure evidence (proof policy 1.1)

F-01 is **Critical**. Closure as *Implemented* needs **L2 + L3 on the same commit (or L4) + L5 by a reviewer whose id ≠ the producing agent**. F-02 (High) needs L2 + (L3 or L4).

| Tier | Evidence | Artefact (no secret values) |
|---|---|---|
| L1 | Code links to the fail-closed loader changes and the .gitignore entry, pinned to the fix commit | GitHub line links |
| L2 | Local run of the three new test files (pass) plus a local `gitleaks git --redact` on a fresh clone (0 findings) | junit XML, gitleaks SARIF summary |
| L3 | `secret-scan.yml` (gitleaks + fail-closed tests) green on the fix commit | Actions run URL |
| L4 | §3 revocation output per environment (401 matrix), V3 startup refusal logs, V5 history check | `F-01-revocation-<env>.txt` |
| L5 | Independent security reviewer signs off on the diff, the purge verification, the §7 log review and the Support ticket | signed review note; `reviewer_id` ≠ agent id |
| negative_proof | History scan: 0 occurrences in all blobs of a fresh mirror; 0 commits touching the file | scan output (counts only) |

The matching template is `remediation/evidence.secret-rotation.template.json`. Replace every `0000000…` commit, every `<…>` placeholder and every `REPLACE` note. Validate with:

```bash
python3 audit-scripts/validate_evidence.py --schema schemas/evidence.schema.json \
  --in remediation/evidence.secret-rotation.json --audited-commit <fix-commit>
```

## 10. Decisions for the owner

1. Make the repo private during the incident (C5)?
2. Delete `conflict_161026_1710` instead of rewriting it?
3. Keep a demo quick-login at all? If yes, only via an untracked `.env.local` in dev builds.
4. Which instances were internet-reachable since 2026-10-16 (C2)? This drives the §7 scope and any notification duty.
