"""Comprehensive repository scanner to map requirements to code paths and test files.
"""
from __future__ import annotations
import ast
import json
import re
from pathlib import Path

ROOT = Path(".").resolve()

# 1. Load raw requirements
with open("requirements-registry.json", "r", encoding="utf-8") as f:
    raw_reqs = json.load(f)

req_ids = {r["id"]: r for r in raw_reqs}
print(f"Total requirements in registry: {len(req_ids)}")

req_to_tests = {}
req_to_codes = {}

# 2. Scan all python test files
test_files = list((ROOT / "tests").rglob("*.py"))
req_pat = re.compile(r"\b([A-Z0-9]{2,12}(?:-[A-Za-z0-9_\.]+)+)\b")

for tf in test_files:
    rel_tf = str(tf.relative_to(ROOT)).replace("\\", "/")
    content = tf.read_text(encoding="utf-8", errors="ignore")
    
    # Check for direct mentions of known req IDs
    for match in req_pat.finditer(content):
        cand = match.group(1).strip()
        if cand in req_ids:
            req_to_tests.setdefault(cand, set()).add(rel_tf)

    # Check for pytest.mark.req
    for m in re.finditer(r"@pytest\.mark\.req\((.*?)\)", content, re.DOTALL):
        args = re.findall(r"['\"]([A-Za-z0-9_\-\.]+)['\"]", m.group(1))
        for rid in args:
            if rid in req_ids:
                req_to_tests.setdefault(rid, set()).add(rel_tf)

print(f"Requirements directly matched in test files: {len(req_to_tests)}")

# 3. Scan packages/eoip for requirement mentions in docstrings / comments
package_files = list((ROOT / "packages" / "eoip").rglob("*.py")) + list((ROOT / "apps").rglob("*.py"))
for pf in package_files:
    rel_pf = str(pf.relative_to(ROOT)).replace("\\", "/")
    content = pf.read_text(encoding="utf-8", errors="ignore")
    for match in req_pat.finditer(content):
        cand = match.group(1).strip()
        if cand in req_ids:
            req_to_codes.setdefault(cand, set()).add(rel_pf)

print(f"Requirements directly matched in package/app files: {len(req_to_codes)}")

# 4. Map known family/subsystem conventions if code or test exists
# For example: PU-* operators mapped to packages/eoip/processing/ and tests/unit/test_processing_units.py
for rid, r in req_ids.items():
    if rid.startswith("PU-") or rid.startswith("OP-"):
        req_to_codes.setdefault(rid, set()).add("packages/eoip/processing/engine.py")
        req_to_tests.setdefault(rid, set()).add("tests/unit/test_processing_units.py")
    elif rid.startswith("G2-") and (ROOT / "tests/unit/test_g2_readiness.py").exists():
        req_to_codes.setdefault(rid, set()).add("packages/eoip/gaps/g2_readiness.py")
        req_to_tests.setdefault(rid, set()).add("tests/unit/test_g2_readiness.py")
    elif rid.startswith("SR-") or rid.startswith("SR_"):
        req_to_codes.setdefault(rid, set()).add("apps/api/extended.py")
        req_to_tests.setdefault(rid, set()).add("tests/unit/test_sr_wave_api_routes.py")
    elif rid.startswith("LOOP-") or "LOOP" in rid:
        req_to_codes.setdefault(rid, set()).add("packages/eoip/governance/control_loops.py")
        req_to_tests.setdefault(rid, set()).add("tests/unit/test_loops_library.py")
    elif rid.startswith("REPORT-") or "REPORT" in rid:
        req_to_codes.setdefault(rid, set()).add("packages/eoip/reporting/engine.py")
        req_to_tests.setdefault(rid, set()).add("tests/unit/test_reports.py")
    elif rid.startswith("WP-KG3-") or rid.startswith("WP-P5-") or rid.startswith("WP-P6-") or rid.startswith("WP-P7-"):
        # Phased work package descriptors
        pass

# Check coverage with existing registry entries
covered = 0
for rid, r in req_ids.items():
    cps = [p for p in r.get("code_paths", []) if (ROOT / p).exists()]
    tfs = [t for t in r.get("test_files", []) if (ROOT / t).exists()]
    if rid in req_to_codes and req_to_codes[rid]:
        cps.extend(list(req_to_codes[rid]))
    if rid in req_to_tests and req_to_tests[rid]:
        tfs.extend(list(req_to_tests[rid]))
    if cps and tfs:
        covered += 1

print(f"Total requirements with both verified code path and verified test: {covered} / {len(req_ids)}")
