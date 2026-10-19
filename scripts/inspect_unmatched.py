import json
from pathlib import Path
from collections import Counter

ROOT = Path(".").resolve()
with open("requirements-registry.json", "r", encoding="utf-8") as f:
    raw_reqs = json.load(f)

# Load discovered req_to_tests and req_to_codes from deep scan
import sys
sys.path.insert(0, ".")
from scripts.map_all_repo_requirements import req_to_tests, req_to_codes

unmatched = []
for r in raw_reqs:
    rid = r["id"]
    cps = [p for p in r.get("code_paths", []) if (ROOT / p).exists()]
    tfs = [t for t in r.get("test_files", []) if (ROOT / t).exists()]
    if rid in req_to_codes and req_to_codes[rid]:
        cps.extend(list(req_to_codes[rid]))
    if rid in req_to_tests and req_to_tests[rid]:
        tfs.extend(list(req_to_tests[rid]))
    if not (cps and tfs):
        unmatched.append(r)

print(f"Unmatched count: {len(unmatched)}")

family_counts = Counter()
prefix_counts = Counter()

for r in unmatched:
    rid = r["id"]
    prefix = rid.split("-")[0] if "-" in rid else rid
    prefix_counts[prefix] += 1
    family_counts[r.get("family", "UNKNOWN")] += 1

print("\nTop 20 unmatched prefixes:")
for p, c in prefix_counts.most_common(20):
    print(f"  {p}: {c}")

print("\nTop 20 unmatched families:")
for fam, c in family_counts.most_common(20):
    print(f"  {fam}: {c}")

print("\nSample 15 unmatched requirements:")
for r in unmatched[:15]:
    print(f"  ID: {r['id']} | Family: {r.get('family')} | Title: {r.get('title')[:60]}")
