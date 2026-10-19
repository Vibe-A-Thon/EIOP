"""Analyze the exact list of partial requirements to see what can be implemented/tested right now.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(".").resolve()

# Load discovered req_to_tests and req_to_codes from deep scan
import sys
sys.path.insert(0, ".")
from scripts.map_all_repo_requirements import req_to_tests, req_to_codes

with open("requirements-registry.json", "r", encoding="utf-8") as f:
    raw_reqs = json.load(f)

has_code_no_test = []
has_test_no_code = []

for r in raw_reqs:
    rid = r["id"]
    cps = [p for p in r.get("code_paths", []) if (ROOT / p).exists()]
    tfs = [t for t in r.get("test_files", []) if (ROOT / t).exists()]
    if rid in req_to_codes and req_to_codes[rid]:
        cps.extend(list(req_to_codes[rid]))
    if rid in req_to_tests and req_to_tests[rid]:
        tfs.extend(list(req_to_tests[rid]))
    
    cps = list(set(cps))
    tfs = list(set(tfs))

    if cps and not tfs:
        has_code_no_test.append((rid, r.get("title", ""), cps[0]))
    elif tfs and not cps:
        has_test_no_code.append((rid, r.get("title", ""), tfs[0]))

print(f"Has code on disk, but no direct test found: {len(has_code_no_test)}")
for it in has_code_no_test[:25]:
    print("  CODE_NO_TEST:", it)

print(f"\nHas test on disk, but no direct code found: {len(has_test_no_code)}")
for it in has_test_no_code[:25]:
    print("  TEST_NO_CODE:", it)
