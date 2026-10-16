import json

reg = json.load(open("requirements-registry.json", encoding="utf-8"))
p6_items = [r for r in reg if "Phase 6" in str(r.get("phase"))]
print(f"Total Phase 6 items in registry: {len(p6_items)}")
for r in p6_items:
    print(f"{r['id']:<15} | {r.get('work_package', ''):<55} | {r.get('title', '')}")
