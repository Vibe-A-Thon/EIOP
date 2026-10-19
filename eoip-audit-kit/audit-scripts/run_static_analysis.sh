#!/usr/bin/env bash
# Run available static analysis tools; skip missing ones with a note.
set -u
REPO_ROOT="${1:-.}"
if [[ "${1:-}" == "--repo-root" ]]; then
  REPO_ROOT="${2:-.}"
fi
cd "$REPO_ROOT" || exit 1

echo "=== EOIP static analysis ==="
echo "repo: $(pwd)"
echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

run_tool() {
  local name="$1"; shift
  if command -v "$name" >/dev/null 2>&1; then
    echo "--- $name ---"
    "$@" 2>&1 || echo "(exit $? — continuing)"
    echo
  else
    echo "--- $name --- SKIPPED (not installed)"
    echo
  fi
}

run_tool ruff ruff check .
run_tool flake8 flake8 .
run_tool bandit bandit -r . -q -x './.venv,./node_modules,./audit-output'
run_tool pip-audit pip-audit || true
if [[ -f package.json ]]; then
  if command -v npm >/dev/null 2>&1; then
    echo "--- npm audit ---"
    npm audit --json 2>&1 | head -c 200000 || echo "(npm audit failed)"
    echo
  else
    echo "--- npm audit --- SKIPPED (npm not installed)"
    echo
  fi
else
  echo "--- npm audit --- SKIPPED (no package.json)"
  echo
fi
run_tool gitleaks gitleaks detect --no-git -v || true
run_tool trufflehog echo "trufflehog present but not auto-run (needs config)"

echo "=== end static analysis ==="
