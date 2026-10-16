import json

with open("requirements-registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

by_id = {x["id"]: x for x in reg}

wp71_ids = ["S-01", "S-02", "S-03", "S-04", "S-05"]
for i in wp71_ids:
    item = by_id.get(i)
    if item:
        print(f"{i} | {item.get('title')} | {item.get('status')} | {item.get('code_paths')} | {item.get('test_files')}")
    else:
        print(f"MISSING: {i}")
