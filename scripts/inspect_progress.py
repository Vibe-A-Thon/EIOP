import json

with open("requirements-registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

for item in reg:
    if item["id"] == "KGR-G-011":
        print(json.dumps(item, indent=2))
