import json

reg = json.load(open("requirements-registry.json", encoding="utf-8"))
sec_items = [r for r in reg if r["id"].startswith("GAP-SEC")]
print(f"Total GAP-SEC items in registry: {len(sec_items)}")
for r in sec_items:
    print(r["id"], r.get("title"), r.get("status"), r.get("work_package"), r.get("code_paths"), r.get("test_files"))
