import json

reg = json.load(open('requirements-registry.json', encoding='utf-8'))
by_id = {r['id']: r for r in reg}

wp53_ids = [
    "UI-01", "UI-02", "UI-03", "UI-04",
    "FR-ADMIN-001", "FR-ADMIN-002", "FR-UI-001", "FR-UI-002",
] + [f"G2-ADMIN-{i:03d}" for i in range(2, 18)] + \
    [f"G2-UX-GRAPH-{i:03d}" for i in range(2, 17)] + \
    ["G2-UX-LENS-002", "G2-UX-LENS-003"] + \
    [f"G2-UX-PLAY-{i:03d}" for i in range(2, 6)]

print(f"Total WP 5.3 IDs to check: {len(wp53_ids)}")
for req_id in wp53_ids:
    r = by_id.get(req_id)
    if r:
        print(f"{req_id:15} | {r.get('status'):20} | {r.get('title')[:60]}")
    else:
        print(f"{req_id:15} | MISSING FROM REGISTRY")
