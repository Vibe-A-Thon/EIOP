import json
from pathlib import Path

families = ["G2-CAUSE", "G2-EVOL", "G2-JOURNAL", "G2-OEVO", "G2-TIME"]

with open("requirements-registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

for fam in families:
    print(f"\n=== Family: {fam} ===")
    items = [item for item in reg if item.get("family") == fam or item["id"].startswith(fam)]
    for item in items:
        print(f"{item['id']}: {item['title']} | status: {item.get('status')} | code_paths: {item.get('code_paths')} | test_files: {item.get('test_files')}")
