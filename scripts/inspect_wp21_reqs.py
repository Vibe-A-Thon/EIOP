import json

with open('requirements-registry.json', encoding='utf-8') as f:
    reg = json.load(f)

reg_by_id = {r['id']: r for r in reg if isinstance(r, dict)}

wp21_ids = [
    'G2-EKAF-003', 'G2-EKAF-010', 'G2-EKAF-014', 'G2-EKAF-016', 
    'G2-EKAF-023', 'G2-EKAF-024', 'G2-EKAF-025', 'G2-EKAF-026'
]

for tid in wp21_ids:
    item = reg_by_id.get(tid, {})
    print(f"=== {tid}: {item.get('title')} ===")
    print(f"Priority: {item.get('priority')}")
    print(f"Spec source: {item.get('spec_source')}")
    print(f"Description/Summary: {item.get('description', item.get('summary', item.get('text', '')))}")
    print(f"Code paths: {item.get('code_paths')}")
    print(f"Test files: {item.get('test_files')}")
    print()
