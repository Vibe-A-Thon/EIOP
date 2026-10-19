"""Deep Scan of tests, packages, and requirements mappings
"""
from __future__ import annotations
import ast
import json
import re
from pathlib import Path

ROOT = Path(".").resolve()

req_to_tests = {}
pattern = re.compile(r"@pytest\.mark\.req\((.*?)\)", re.DOTALL)
req_id_pat = re.compile(r"['\"]([A-Za-z0-9_\-\.]+)['\"]")

# Also look for module docstrings or comments mentioning requirements
req_comment_pat = re.compile(r"(?:req|requirement|satisfies|covers)\s*[:=]?\s*([A-Za-z0-9_\-\.]+)", re.IGNORECASE)

test_files = list((ROOT / "tests").rglob("*.py"))
for tf in test_files:
    rel_tf = str(tf.relative_to(ROOT)).replace("\\", "/")
    content = tf.read_text(encoding="utf-8", errors="ignore")
    
    # 1. pytest markers
    for match in pattern.finditer(content):
        args_str = match.group(1)
        for rid in req_id_pat.findall(args_str):
            req_to_tests.setdefault(rid, set()).add(rel_tf)

    # 2. test names with requirement IDs (e.g. test_g2_t0001 or test_wp21_...)
    for func in re.findall(r"def\s+(test_[a-zA-Z0-9_]+)", content):
        parts = func.upper().split("_")
        for p in parts:
            if "-" in p or any(c.isdigit() for c in p):
                pass

print(f"Total requirements marked directly in tests via @pytest.mark.req: {len(req_to_tests)}")

# Let's inspect test_files to see what packages they import
test_to_imports = {}
for tf in test_files:
    rel_tf = str(tf.relative_to(ROOT)).replace("\\", "/")
    content = tf.read_text(encoding="utf-8", errors="ignore")
    try:
        tree = ast.parse(content)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    if n.name.startswith("eoip"):
                        imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and (node.module.startswith("eoip") or node.module.startswith("apps")):
                    imports.append(node.module)
        test_to_imports[rel_tf] = imports
    except Exception:
        pass

print(f"Parsed imports for {len(test_to_imports)} test files.")

# Load raw reqs
with open("requirements-registry.json", "r", encoding="utf-8") as f:
    raw_reqs = json.load(f)

# Check how many reqs can find their code path from tests
found_cp_count = 0
for r in raw_reqs:
    rid = r.get("id")
    # check existing valid cp
    cps = r.get("code_paths", [])
    valid_cp = [p for p in cps if (ROOT / p).exists()]
    if not valid_cp:
        pe = r.get("implementation", {}).get("public_entrypoints", [])
        valid_cp = [p for p in pe if (ROOT / p).exists()]
    if not valid_cp:
        # Check if any test for this req imports eoip modules
        tests_for_r = req_to_tests.get(rid, set())
        inferred_cps = set()
        for t in tests_for_r:
            for imp in test_to_imports.get(t, []):
                # map eoip.foo.bar to packages/eoip/foo/bar.py or packages/eoip/foo.py
                parts = imp.split(".")
                cand1 = ROOT / "packages" / "/".join(parts) + ".py" if False else ROOT / "packages" / Path(*parts).with_suffix(".py")
                cand2 = ROOT / "packages" / Path(*parts) / "__init__.py"
                cand3 = ROOT / Path(*parts).with_suffix(".py")
                if cand1.exists():
                    inferred_cps.add(str(cand1.relative_to(ROOT)).replace("\\", "/"))
                elif cand2.exists():
                    inferred_cps.add(str(cand2.relative_to(ROOT)).replace("\\", "/"))
                elif cand3.exists():
                    inferred_cps.add(str(cand3.relative_to(ROOT)).replace("\\", "/"))
        if inferred_cps:
            found_cp_count += 1

print(f"Requirements with no code_path originally, but with code inferred from test imports: {found_cp_count}")
