#!/usr/bin/env bash
# Run available static analysis tools; skip missing ones with a note. Never modifies the repo.
# Usage: run_static_analysis.sh [--repo-root DIR] [--paths "apps packages"] [--tools-bin DIR] [--out-dir DIR]
set -u
REPO_ROOT="."; PATHS=""; OUT_DIR=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root) REPO_ROOT="$2"; shift 2;;
    --paths) PATHS="$2"; shift 2;;
    --tools-bin) export PATH="$2:$PATH"; shift 2;;
    --out-dir) OUT_DIR="$2"; shift 2;;
    *) REPO_ROOT="$1"; shift;;
  esac
done
cd "$REPO_ROOT" || exit 1
[[ -z "$PATHS" ]] && PATHS="."
[[ -n "$OUT_DIR" ]] && mkdir -p "$OUT_DIR"
EXCL=".git,node_modules,audit-output,.venv,venv,.tmp,.audit-scratch,.eoip-data,__pycache__"

echo "=== EOIP static analysis ==="
echo "repo: $(pwd)"
echo "commit: $(git rev-parse HEAD 2>/dev/null || echo n/a)"
echo "paths: $PATHS"
echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

have() { command -v "$1" >/dev/null 2>&1; }
section() { echo "--- $1 ---"; }

section ruff
if have ruff; then
  ruff --version
  # shellcheck disable=SC2086
  ruff check $PATHS --no-cache --exit-zero --output-format concise --extend-exclude "$EXCL" 2>&1 | tail -n 400
  if [[ -n "$OUT_DIR" ]]; then ruff check $PATHS --no-cache --exit-zero --output-format json --extend-exclude "$EXCL" > "$OUT_DIR/ruff.json" 2>/dev/null; fi
else echo "SKIPPED (not installed)"; fi
echo

section flake8
if have flake8; then flake8 $PATHS --exclude "$EXCL" --count --exit-zero | tail -n 50; else echo "SKIPPED (not installed; ruff covers pyflakes/pycodestyle rules)"; fi
echo

section bandit
if have bandit; then
  bandit --version 2>&1 | head -1
  # shellcheck disable=SC2086
  bandit -r $PATHS -q -x "./tests,./.venv,./node_modules,./.tmp,./.audit-scratch" -f txt 2>&1 | tail -n 200
  if [[ -n "$OUT_DIR" ]]; then bandit -r $PATHS -q -x "./tests,./.venv,./node_modules,./.tmp,./.audit-scratch" -f json -o "$OUT_DIR/bandit.json" >/dev/null 2>&1; fi
else echo "SKIPPED (not installed)"; fi
echo

section pip-audit
if have pip-audit; then
  for req in requirements.lock requirements*.lock requirements.txt; do
    [[ -f "$req" ]] || continue
    echo "# $req"
    pip-audit -r "$req" --no-deps --disable-pip --progress-spinner off 2>&1 | tail -n 60 || true
  done
else echo "SKIPPED (not installed)"; fi
echo

section "npm audit"
if [[ -f package.json || -f apps/web/package-lock.json ]]; then
  if have npm; then
    for d in . apps/web; do [[ -f "$d/package-lock.json" ]] && (cd "$d" && echo "# $d" && npm audit --omit=dev 2>&1 | tail -n 40); done
  else echo "SKIPPED (npm not installed)"; fi
else echo "SKIPPED (no package.json)"; fi
echo

section gitleaks
if have gitleaks; then gitleaks detect --no-git --redact -v 2>&1 | tail -n 60 || true
else echo "SKIPPED (not installed) — see kit secret heuristics in evidence/secret_scan.json"; fi
echo
echo "=== end static analysis ==="
