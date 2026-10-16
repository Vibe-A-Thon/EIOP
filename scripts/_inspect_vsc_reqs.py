import json

reg = json.load(open("requirements-registry.json", encoding="utf-8"))
vsc_ids = [
    "FR-VSCODE-001", "FR-VSCODE-002",
    "G2-VSC-002", "G2-VSC-003", "G2-VSC-004", "G2-VSC-005", "G2-VSC-006", "G2-VSC-007", "G2-VSC-008",
    "MVP-FR-019"
]
for item in reg:
    if item["id"] in vsc_ids:
        print(f"=== {item['id']}: {item['title']} ===")
        for k in ["family", "priority", "spec_source", "code_paths", "test_files", "api_route", "ui_surface"]:
            print(f"  {k}: {item.get(k)}")
