import json

with open("requirements-registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

by_id = {x["id"]: x for x in reg}

wp72_ids = [
    "PERF-01",
    "G2-PERF-002", "G2-PERF-003", "G2-PERF-004", "G2-PERF-005", "G2-PERF-006", "G2-PERF-007", "G2-PERF-008",
    "G2-REL-002", "G2-REL-003", "G2-REL-004", "G2-REL-005", "G2-REL-006", "G2-REL-007", "G2-REL-008",
    "G2-SLO-002", "G2-SLO-003", "G2-SLO-004", "G2-SLO-005",
    "G2-TEL-002", "G2-TEL-003", "G2-TEL-004", "G2-TEL-005", "G2-TEL-006", "G2-TEL-007", "G2-TEL-008",
    "MVP-FR-023", "MVP-FR-024", "MVP-FR-025", "MVP-FR-026",
    "NFR-OPS-001", "NFR-OPS-002", "NFR-PERF-001", "NFR-REL-001", "NFR-REL-002"
]

print(f"Total WP 7.2 tasks: {len(wp72_ids)}")
for i in wp72_ids:
    item = by_id.get(i)
    if item:
        print(f"{i} | {item.get('title')} | {item.get('status')} | {item.get('test_files')}")
    else:
        print(f"MISSING: {i}")
