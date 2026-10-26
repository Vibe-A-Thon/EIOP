#!/usr/bin/env bash
# Self-test for run_tests_and_map.py on a given interpreter (default: python3.11).
# Usage: audit-scripts/selftest/selftest_run_tests_and_map.sh [/path/to/python3.11] [/path/to/python-with-pytest]
set -euo pipefail
PY=${1:-python3.11}; PYTEST_PY=${2:-$PY}
HERE=$(cd "$(dirname "$0")/.." && pwd); T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
mkdir -p "$T/repo/tests"
cat > "$T/repo/tests/test_demo.py" <<'EOF'
import pytest
def test_req_a_pass():
    assert True
@pytest.mark.parametrize("v", [1, 2])
def test_req_b_param(v):
    assert v in (1, 2)
def test_req_c_fail():
    assert False
EOF
echo '{"requirements":[{"id":"REQ-A","title":"a"},{"id":"REQ-B","title":"b"},{"id":"REQ-C","title":"c"}]}' > "$T/reqs.json"
echo '{"REQ-A":["tests/test_demo.py::test_req_a_pass"],"REQ-B":["tests/test_demo.py::test_req_b_param"],"REQ-C":["tests/test_demo.py::test_req_c_fail"]}' > "$T/map.json"
"$PY" -m py_compile "$HERE"/*.py
"$PY" "$HERE/run_tests_and_map.py" --repo-root "$T/repo" --requirements "$T/reqs.json" --test-map "$T/map.json" \
  --out "$T/out" --python "$PYTEST_PY" --isolate --timeout 120 --commit selftest >/dev/null
"$PY" - "$T/out/per_requirement.json" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
assert d["REQ-A"]["passed"] == 1 and d["REQ-A"]["failed"] == 0, d["REQ-A"]
assert d["REQ-B"]["passed"] == 2 and set(d["REQ-B"]["tests"]) == {"tests.test_demo::test_req_b_param"}, d["REQ-B"]
assert d["REQ-C"]["failed"] == 1, d["REQ-C"]
print("SELFTEST PASS:", sys.version.split()[0])
EOF
"$PY" "$HERE/run_tests_and_map.py" --repo-root "$T/repo" --requirements "$T/reqs.json" --test-map "$T/map.json" --out "$T/out" --reuse-junit --commit selftest >/dev/null
echo "reuse-junit PASS"
