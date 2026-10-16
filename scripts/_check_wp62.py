import json

with open("requirements-registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

ids = [
    "MS-15", "MS-18", "MS-19", "MS-21", "MS-22", "MS-23", "MS-24", "MS-29", "MS-30",
    "G2-IMMUNE-002", "G2-IMMUNE-003", "G2-IMMUNE-004", "G2-IMMUNE-005", "G2-IMMUNE-006",
    "G2-IMMUNE-007", "G2-IMMUNE-008", "G2-IMMUNE-009", "G2-IMMUNE-010", "G2-IMMUNE-011",
    "G2-IMMUNE-012", "G2-IMMUNE-013",
    "G2-SIM-002", "G2-SIM-003", "G2-SIM-004", "G2-SIM-005", "G2-SIM-006", "G2-SIM-007",
    "G2-TWIN-002", "G2-TWIN-003", "G2-TWIN-004", "G2-TWIN-005"
]

by_id = {x["id"]: x for x in reg}
for i in ids:
    item = by_id.get(i)
    if not item:
        print(f"MISSING: {i}")
    else:
        title = item.get("title", "")
        desc = item.get("description", "")
        print(f"{i} | {title} | {desc}")
